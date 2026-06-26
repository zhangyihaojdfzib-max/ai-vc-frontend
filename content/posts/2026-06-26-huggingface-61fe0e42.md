---
title: 一键在HF Jobs上运行vLLM服务器
title_original: Run a vLLM Server on HF Jobs in One Command
date: '2026-06-26'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/vllm-jobs
author: ''
summary: 本文介绍了如何通过一条命令在Hugging Face基础设施上快速启动私有的、兼容OpenAI的LLM端点，无需配置服务器或Kubernetes，按秒付费。文章详细说明了前置条件、启动服务器的具体命令（使用vllm/vllm-openai镜像和--expose暴露端口），以及如何通过curl或Python
  OpenAI客户端从任何地方查询该服务器。该方法适用于测试、评估或批量生成，而生产级服务则推荐使用Inference Endpoints。
categories:
- AI基础设施
tags:
- vLLM
- Hugging Face Jobs
- LLM部署
- OpenAI兼容API
- AI基础设施
draft: false
translated_at: '2026-06-26T06:11:15.446240'
---

# 一条命令在 HF Jobs 上运行 vLLM 服务器

你可以通过一条命令在 Hugging Face 基础设施上启动一个私有的、兼容 OpenAI 的 LLM 端点——无需配置服务器，无需 Kubernetes，按秒付费。启动后，你可以从笔记本电脑、笔记本或任何其他地方查询它。

这是为测试、评估或批量生成搭建模型的最快方式。（如果你需要的是托管的生产级服务，那么 Inference Endpoints 更适合——文末会说明何时选择哪种方案。）

以下是完整的端到端流程。

## 前置条件

- 一种支付方式或正值的预付费余额（Jobs 按硬件使用量以分钟计费）。
- huggingface_hub >= 1.20.0：`pip install -U "huggingface_hub>=1.20.0"`。
- 本地登录：`hf auth login`。

## 启动服务器

`hf jobs run` 是 HF 基础设施上的 `docker run`。我们使用官方的 `vllm/vllm-openai` 镜像，通过 `--flavor` 请求 GPU，并通过 `--expose` 暴露 vLLM 的端口：

```bash
hf jobs run --flavor a10g-large --expose 8000 --timeout 2h \
  vllm/vllm-openai:latest \
  vllm serve Qwen/Qwen3-4B --host 0.0.0.0 --port 8000
```

`--expose 8000` 将容器的端口路由到 HF 的公共 jobs 代理（完整参考请参见《Serve Models 指南》）。该命令会打印你的服务器可访问的 URL：

```
✓ Job started
  id: 6a381ca1953ed90bfb947332
  url: https://huggingface.co/jobs/qgallouedec/6a381ca1953ed90bfb947332
提示：暴露的端口可通过以下地址访问（需要具有作业读取权限的 HF Token）：
  https://6a381ca1953ed90bfb947332--8000.hf.jobs
```

`6a381ca1953ed90bfb947332` 是你的作业 ID。请记住它，后续会用到。在本文其余部分，我们将用 `<job_id>` 作为它的占位符。

给它几分钟时间下载权重并启动。当日志显示 `Application startup complete` 时，说明已上线。

## 从任何地方查询它

vLLM 使用 OpenAI API，每个请求只需将你的 HF Token 作为 Bearer Token 传递。最快的方式是使用 curl：

```bash
curl https://<job_id>--8000.hf.jobs/v1/chat/completions \
  -H "Authorization: Bearer $(hf auth token)" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen/Qwen3-4B",
    "messages": [{"role": "user", "content": "Hello!"}],
    "chat_template_kwargs": {"enable_thinking": false}
  }'
```

这将返回标准的 OpenAI 风格 JSON，其中 `choices[0].message.content` 包含 `"Hello! How can I assist you today? 😊"`。

或者，在 Python 中，将 OpenAI 客户端指向暴露的 URL，并将 Token 作为 API 密钥传递：

```python
from huggingface_hub import get_token
from openai import OpenAI

client = OpenAI(
    base_url="https://<job_id>--8000.hf.jobs/v1",
    api_key=get_token(),
)
resp = client.chat.completions.create(
    model="Qwen/Qwen3-4B",
    messages=[{"role": "user", "content": "Hello!"}],
    extra_body={"chat_template_kwargs": {"enable_thinking": False}},
)
print(resp.choices[0].message.content)
```

```
Hello! How can I assist you today? 😊
```

开始前的快速健康检查：`curl https://<job_id>--8000.hf.jobs/v1/models -H "Authorization: Bearer $(hf auth token)"` 应列出模型。

🔐 该端点是受控的，而非公开的。每个请求必须携带一个具有作业命名空间读取权限的 HF Token。直接浏览器访问将被拒绝。实际上，jobs 代理就是你的 API 网关：访问权限仅限于你（和你的组织）。这对私人使用来说没问题，但请妥善处理 URL：不要期望它公开共享而随意传播，也不要在不可信的地方粘贴你的 Token。如果你需要更细粒度或公共访问权限，请在前面放置一个合适的网关。或者参见下面的《HF Jobs 还是 Inference Endpoints？》。

## 清理

Jobs 按秒计费，因此完成后请停止服务器：

```bash
hf jobs cancel <job_id>
```

你设置的 `--timeout` 是一个安全网（它会自动停止），但显式取消更省钱。`a10g-large` 的运行费用为 $1.50/小时——查看 `hf jobs hardware` 获取完整价格列表，并选择适合你模型的最小规格。

## 更进一步：更大的模型

同样的命令可以扩展到更大的模型——选择更强大的 `--flavor`，并通过 `--tensor-parallel-size` 告诉 vLLM 将模型分片到多个 GPU 上。例如，在 2× H200 上运行 122B 的 Qwen3.5 混合专家模型：

```bash
hf jobs run --flavor h200x2 --expose 8000 --timeout 2h \
  vllm/vllm-openai:latest \
  vllm serve Qwen/Qwen3.5-122B-A10B \
  --host 0.0.0.0 --port 8000 --tensor-parallel-size 2 \
  --max-model-len 32768 --max-num-seqs 256
```

`--tensor-parallel-size` 应与 flavor 中的 GPU 数量匹配（`h200x2` → 2，`h200x8` → 8）。运行 `hf jobs hardware` 查看可用选项，并为更大的模型设置更长的 `--timeout`，因为它们需要更长时间下载和加载。对于大型模型，H200 系列通常性价比最高。

`--max-model-len 32768 --max-num-seqs 256` 标志特定于此模型：Qwen3.5-122B 是一种混合 Mamba/注意力架构，默认上下文为 256K Token，这会导致 vLLM 的默认批处理设置内存不足。限制上下文长度和并发序列数量可以使其保持在 GPU 内存范围内。如果模型因内存不足或缓存块错误而无法启动，首先尝试调低这两个参数。其他一切（暴露的 URL、OpenAI 客户端、Token 认证）保持不变。

## 更进一步：在 UI 中聊天

更喜欢聊天窗口而不是 curl？几行 Gradio 代码即可指向同一个端点。在 `vllm serve` 命令中添加 `--reasoning-parser deepseek_r1`，使 Qwen3 的思考过程作为单独字段返回（非必需，但很有用），然后在本地运行此代码（你只需要作业 ID）：

```python
import gradio as gr
from gradio import ChatMessage
from huggingface_hub import get_token
from openai import OpenAI

client = OpenAI(base_url="https://<job_id>--8000.hf.jobs/v1", api_key=get_token())

def chat(message, history):
    messages = [{"role": m["role"], "content": m["content"]} for m in history if not m.get("metadata")]
    messages.append({"role": "user", "content": message})
    stream = client.chat.completions.create(model="Qwen/Qwen3-4B", messages=messages, stream=True)

    thinking, answer = "", ""
    for chunk in stream:
        delta = chunk.choices[0].delta
        thinking += delta.model_extra.get("reasoning", "")
        answer += delta.content or ""
        out = []
        if thinking.strip():
            status = "done" if answer.strip() else "pending"
            out.append(ChatMessage(role="assistant", content=thinking, metadata={"title": "💭 Thinking", "status": status}))
        if answer.strip():
            out.append(ChatMessage(role="assistant", content=answer))
        yield out

gr.ChatInterface(chat).launch()
```

运行它，打开 `http://127.0.0.1:7860`，然后聊天——思考过程会流式传输到可折叠面板中，答案在下方。

## 更进一步：SSH 进入正在运行的服务器

需要调试启动失败、查看 GPU 内存或交互式查看日志？你可以直接打开一个 shell 进入正在运行的作业。使用 `--ssh` 启动它，并确保你的公钥已在 `huggingface.co/settings/keys` 注册：

```bash
hf jobs run --flavor a10g-large --expose 8000 --timeout 2h --ssh \
  vllm/vllm-openai:latest \
  vllm serve Qwen/Qwen3-4B --host 0.0.0.0 --port 8000
```

然后使用作业 ID 连接：

```bash
hf jobs ssh <job_id>
```

你现在位于容器内部，可以运行 `nvidia-smi`、检查进程或直接操作模型——这使得调试和监控比从外部读取日志容易得多。SSH 支持需要 `huggingface_hub >= 1.20.0`。

## 更进一步：与 Pi 一起用作编码 Agent 后端

同一个端点可以作为终端编码 Agent 的后端。Pi 是一个与提供商无关的 Agent 框架。将其指向作业，你就可以获得一个在你自托管模型上运行的 Read/Write/Edit/Bash Agent。

首先需要明确一点：Agent（智能体）通过工具调用驱动模型，而vLLM仅在服务器启动时启用了工具调用功能才会接受这些调用。因此，需要重新启动服务器，并添加`--enable-auto-tool-choice`参数以及匹配模型系列的`--tool-call-parser`参数（Qwen3使用`hermes`）。Agent（智能体）也受益于更强的模型，因此这里适合引入更大的模型：

```bash
hf jobs run --flavor h200x2 --expose 8000 --timeout 2h \
  vllm/vllm-openai:latest \
  vllm serve Qwen/Qwen3.5-122B-A10B \
  --host 0.0.0.0 --port 8000 --tensor-parallel-size 2 \
  --max-model-len 32768 --max-num-seqs 256 \
  --reasoning-parser deepseek_r1 \
  --enable-auto-tool-choice --tool-call-parser hermes

```

然后在`~/.pi/agent/models.json`中将该任务添加为自定义提供商：

```json
{
  "providers": {
    "hf-jobs": {
      "baseUrl": "https://<job_id>--8000.hf.jobs/v1",
      "api": "openai-completions",
      "apiKey": "!hf auth token",
      "models": [
        { "id": "Qwen/Qwen3.5-122B-A10B" }
      ]
    }
  }
}

```

然后启动Agent（智能体）并指向它：

你刚才通过几条命令启动的模型，现在正在你的终端中驱动一个交互式编码Agent（智能体）。

## HF Jobs 还是 Inference Endpoints？

HF Jobs 并不是在 Hugging Face 上部署模型的唯一方式。Inference Endpoints 是我们针对相同任务提供的托管产品，选择哪个取决于你的需求。

当你希望获得最大灵活性和控制权时，请选择HF Jobs：它本质上是在 HF 基础设施上运行`docker run`，因此你可以选择镜像、精确的`vllm serve`参数以及硬件，并按任务运行时长按秒付费。这使得它非常适合实验、一次性评估、批量生成，或在正式投入之前对模型进行初步测试。

当你需要更接近生产环境的产品时，请选择Inference Endpoints。它们提供了长期运行服务所需的运维便利：更细粒度的访问控制（端点可以是公开、受保护或私有的），以及缩放到零功能，这样在无活动期间你不会被计费。如果你要搭建一个持久化的端点而非运行一个临时任务，那么这是你应该使用的工具。

## 延伸阅读

本文主要介绍 vLLM，但同样的暴露端口模式适用于任何兼容 OpenAI 的服务器。如果你想使用 llama.cpp 部署 GGUFs 或运行 SGLang，请参阅《在 Jobs 上部署模型》指南，该指南详细介绍了这些后端。

---

> 本文由AI自动翻译，原文链接：[Run a vLLM Server on HF Jobs in One Command](https://huggingface.co/blog/vllm-jobs)
> 
> 翻译时间：2026-06-26 06:11
