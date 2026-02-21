---
title: OpenAI发布全新开源模型系列GPT OSS
title_original: Welcome GPT OSS, the new open-source model family from OpenAI!
date: '2025-08-05'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/welcome-openai-gpt-oss
author: ''
summary: OpenAI正式推出全新开源模型系列GPT OSS，包含1170亿参数和210亿参数两个版本，均采用专家混合架构和4位量化技术，旨在实现高效推理与智能体任务。模型以Apache
  2.0许可证发布，支持本地部署与多样化开发者用例，并可通过Hugging Face等平台进行API访问、微调与评估。此次发布被视为OpenAI推动AI民主化的重要举措。
categories:
- AI产品
tags:
- OpenAI
- 开源模型
- GPT OSS
- MoE
- Hugging Face
draft: false
translated_at: '2026-02-21T04:19:58.357983'
---

# 欢迎 GPT OSS，OpenAI 推出的全新开源模型系列！

GPT OSS 是 OpenAI 备受期待的开源权重发布，专为强大的推理、Agent（智能体）任务和多样化的开发者用例而设计。它包含两个模型：一个拥有 1170 亿参数的大型模型（gpt-oss-120b），以及一个拥有 210 亿参数的小型模型（gpt-oss-20b）。两者均采用专家混合（MoEs）架构，并使用 4 位量化方案（MXFP4），在保持低资源占用的同时实现了快速推理（得益于更少的激活参数，详见下文）。大型模型可适配单张 H100 GPU，而小型模型仅需 16GB 内存即可运行，非常适合消费级硬件和设备端应用。

为了让社区能更好地使用并产生更大影响，这些模型采用 Apache 2.0 许可证发布，并附带一项最低使用政策：

> 我们的目标是让工具能够安全、负责任且民主地被使用，同时最大限度地让您掌控使用方式。使用 gpt-oss 即表示您同意遵守所有适用法律。

根据 OpenAI 的说法，此次发布是他们致力于开源生态系统的重要一步，符合其让 AI 惠及大众的既定使命。许多用例依赖于私有和/或本地部署，我们 Hugging Face 团队非常激动地欢迎 OpenAI 加入社区。我们相信这些模型将是长寿、鼓舞人心且具有深远影响的。

## 目录

-   简介
-   概述
-   通过推理服务提供商进行 API 访问
-   本地推理
    -   使用 transformers
        -   Flash Attention 3
        -   其他优化
        -   AMD ROCm 支持
        -   优化总结
    -   llama.cpp
    -   vLLM
    -   transformers serve
-   微调
-   在 Hugging Face 合作伙伴上部署
    -   Azure
    -   Dell
-   评估模型
-   聊天与聊天模板
    -   系统消息和开发者消息
    -   使用 transformers 进行工具调用

## 能力与架构概述

-   210 亿和 1170 亿总参数，分别对应 36 亿和 51 亿激活参数。
-   使用 mxfp4 格式的 4 位量化方案。仅应用于 MoE 权重。如前所述，120B 模型可适配单张 80 GB GPU，20B 模型可适配单张 16GB GPU。
-   纯文本推理模型；支持思维链和可调节的推理努力级别。
-   支持指令遵循和工具调用。
-   支持使用 transformers、vLLM、llama.cpp 和 ollama 进行推理。
-   推荐使用 Responses API 进行推理。
-   许可证：Apache 2.0，附带一项小型补充使用政策。

架构

-   采用 SwiGLU 激活函数的 Token-choice MoE。
-   计算 MoE 权重时，对选定的专家进行 softmax 操作（softmax-after-topk）。
-   每个注意力层使用 RoPE，上下文窗口为 128K。
-   交替的注意力层：全上下文层和滑动 128-token 窗口层。
-   注意力层使用每个头一个可学习的注意力汇聚，其中 softmax 的分母有一个额外的附加值。
-   使用与 GPT-4o 和其他 OpenAI API 模型相同的分词器。已加入一些新的 token 以实现与 Responses API 的兼容性。

![OpenAI GPT OSS 模型的基准测试结果，与 o3 和 o4-mini 对比（来源：OpenAI）。](/images/posts/df67257e7821.png)

## 通过推理服务提供商进行 API 访问

OpenAI GPT OSS 模型可通过 Hugging Face 的 Inference Providers 服务访问，允许您使用相同的 JavaScript 或 Python 代码向任何受支持的提供商发送请求。这与为 OpenAI 在 gpt-oss.com 上的官方演示提供支持的基础设施相同，您也可以将其用于自己的项目。

以下是一个使用 Python 和超高速 Cerebras 提供商的示例。更多信息和额外代码片段，请查看模型卡中的推理服务提供商部分以及我们为这些模型编写的专用指南。

```py
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b:cerebras",
    messages=[
        {
            "role": "user",
            "content": "How many rs are in the word 'strawberry'?",
        }
    ],
)

print(completion.choices[0].message)

```

Inference Providers 还实现了与 OpenAI 兼容的 Responses API，这是用于聊天模型的最先进的 OpenAI 接口，旨在实现更灵活、更直观的交互。以下是使用 Fireworks AI 提供商的 Responses API 示例。更多详情，请查看开源项目 responses.js。

```py
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

response = client.responses.create(
    model="openai/gpt-oss-20b:fireworks-ai",
    input="How many rs are in the word 'strawberry'?",
)

print(response)

```

## 本地推理

### 使用 Transformers

您需要安装最新的 transformers 版本（v4.55.1 或更高），以及 accelerate 和 kernels。我们还建议安装 triton 3.4 或更高版本，因为它解锁了对 CUDA 硬件上 mxfp4 量化的支持：

```shell
pip install --upgrade transformers kernels accelerate "triton>=3.4"

```

模型权重以 mxfp4 格式量化，该格式最初在 Hopper 或 Blackwell 系列 GPU 上可用，但现在也适用于之前的 CUDA 架构（包括 Ada、Ampere 和 Tesla）。安装 triton 3.4 和 kernels 库后，可以在首次使用时下载优化的 mxfp4 内核，从而实现大幅内存节省。有了这些组件，您就可以在拥有 16 GB RAM 的 GPU 上运行 20B 模型。这包括许多消费级显卡（3090、4090、5080）以及 Colab 和 Kaggle！

如果未安装上述库（或者您没有兼容的 GPU），加载模型将回退到 bfloat16 精度，并从量化权重中解包。

以下代码片段展示了使用 20B 模型进行简单推理的示例。如前所述，使用 mxfp4 时，它可在 16 GB GPU 上运行；使用 bfloat16 时，约需 48 GB。

```py
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "openai/gpt-oss-20b"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype="auto",
)

messages = [
    {"role": "user", "content": "How many rs are in the word 'strawberry'?"},
]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True,
).to(model.device)

generated = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(generated[0][inputs["input_ids"].shape[-1]:]))

```

#### Flash Attention 3

这些模型使用了注意力汇聚技术，vLLM 团队已使该技术与 Flash Attention 3 兼容。我们已将他们的优化内核打包并集成到 kernels-community/vllm-flash-attn3 中。截至撰写本文时，这个超快内核已在 Hopper 显卡上使用 PyTorch 2.7 和 2.8 进行了测试。我们预计未来几天会扩大支持范围。如果您在 Hopper 显卡（例如 H100 或 H200）上运行模型，需要执行 `pip install --upgrade kernels`，并在代码片段中添加以下行：

```diff
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "openai/gpt-oss-20b"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype="auto",
+    # Flash Attention with Sinks
+    attn_implementation="kernels-community/vllm-flash-attn3",
)

messages = [
    {"role": "user", "content": "How many rs are in the word 'strawberry'?"},
]
```

```python
inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True,
).to(model.device)

generated = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(generated[0][inputs["input_ids"].shape[-1]:]))
```

这段代码将从 `kernels-community` 下载优化过的预编译内核代码，正如我们之前的博客文章所解释的那样。`transformers` 团队已经构建、打包并测试了该代码，因此您可以完全放心地使用。

#### 其他优化

如果您的 GPU 支持 `mxfp4`，我们建议您使用它。如果您还能使用 Flash Attention 3，那么请务必启用它！

如果您的 GPU 与 `mxfp4` 不兼容，那么我们建议您使用 MegaBlocks MoE 内核来获得不错的加速效果。为此，您只需像这样调整您的推理代码：

```diff
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "openai/gpt-oss-20b"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype="auto",
+    # 使用可下载的 `MegaBlocksMoeMLP` 优化 MoE 层
+    use_kernels=True,
)

messages = [
    {"role": "user", "content": "How many rs are in the word 'strawberry'?"},
]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_tensors="pt",
    return_dict=True,
).to(model.device)

generated = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(generated[0][inputs["input_ids"].shape[-1]:]))
```

MegaBlocks 优化的 MoE 内核要求模型在 `bfloat16` 上运行，因此内存消耗将高于在 `mxfp4` 上运行。如果可能，我们建议您使用 `mxfp4`，否则请通过 `use_kernels=True` 选择使用 MegaBlocks。

#### AMD ROCm 支持

OpenAI GPT OSS 已在 AMD Instinct 硬件上得到验证，我们很高兴地宣布，在我们的内核库中初步支持 AMD 的 ROCm 平台，为 Transformers 中即将推出的优化 ROCm 内核奠定了基础。MegaBlocks MoE 内核加速已可用于 AMD Instinct（例如 MI300 系列）上的 OpenAI GPT OSS，从而实现更好的训练和推理性能。您可以使用上面显示的相同推理代码进行测试。

AMD 还准备了一个 Hugging Face Space，供用户在 AMD 硬件上试用该模型。

#### 可用优化总结

在撰写本文时，下表根据 GPU 兼容性和我们的测试总结了我们的建议。我们预计 Flash Attention 3（带 sink attention）将与更多 GPU 兼容。

尽管 120B 模型可以放在单个 H100 GPU 上（使用 `mxfp4`），但您也可以使用 `accelerate` 或 `torchrun` 轻松地在多个 GPU 上运行它。Transformers 提供了默认的并行化方案，您也可以利用优化的注意力内核。以下代码片段可以在具有 4 个 GPU 的系统上使用 `torchrun --nproc_per_node=4 generate.py` 运行：

```py
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.distributed import DistributedConfig
import torch

model_path = "openai/gpt-oss-120b"
tokenizer = AutoTokenizer.from_pretrained(model_path, padding_side="left")

device_map = {
    "tp_plan": "auto",    
}

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype="auto",
    attn_implementation="kernels-community/vllm-flash-attn3",
    **device_map,
)

messages = [
     {"role": "user", "content": "Explain how expert parallelism works in large language models."}
]

inputs = tokenizer.apply_chat_template(
    messages,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True,
).to(model.device)

outputs = model.generate(**inputs, max_new_tokens=1000)


response = tokenizer.decode(outputs[0])
print("Model response:", response.split("<|channel|>final<|message|>")[-1].strip())
```

OpenAI GPT OSS 模型经过了广泛的训练，以利用工具使用作为其推理工作的一部分。我们为 transformers 精心设计的聊天模板提供了很大的灵活性，请查看本文后面专门的章节。

### Llama.cpp

Llama.cpp 提供原生 MXFP4 支持并集成 Flash Attention，从发布首日（day-0）起就在 Metal、CUDA 和 Vulkan 等各种后端上提供最佳性能。

要安装它，请遵循 llama.cpp Github 仓库中的指南。

```
# MacOS
brew install llama.cpp

# Windows
winget install llama.cpp

```

推荐的方式是通过 llama-server 使用它：

```
llama-server -hf ggml-org/gpt-oss-120b-GGUF -c 0 -fa --jinja --reasoning-format none

# 然后，访问 http://localhost:8080

```

我们同时支持 120B 和 20B 模型。更多详细信息，请访问此 PR 或 GGUF 模型集合。

如前所述，vLLM 开发了支持 sink attention 的优化 Flash Attention 3 内核，因此您将在 Hopper 架构的显卡上获得最佳效果。Chat Completion 和 Responses API 均受支持。您可以使用以下代码片段安装并启动服务器，该片段假设使用 2 个 H100 GPU：

```shell
vllm serve openai/gpt-oss-120b --tensor-parallel-size 2

```

或者，直接在 Python 中像这样使用：

```py
from vllm import LLM
llm = LLM("openai/gpt-oss-120b", tensor_parallel_size=2)
output = llm.generate("San Francisco is a")

```

### transformers serve

您可以使用 `transformers serve` 在本地试验模型，无需任何其他依赖项。您只需运行以下命令即可启动服务器：

```shell
transformers serve

```

然后您可以使用 Responses API 向其发送请求。

```shell
# responses API
curl -X POST http://localhost:8000/v1/responses \
-H "Content-Type: application/json" \
-d '{"input": [{"role": "system", "content": "hello"}], "temperature": 1.0, "stream": true, "model": "openai/gpt-oss-120b"}'

```

您也可以使用标准的 Completions API 发送请求：

```shell
# completions API
curl -X POST http://localhost:8000/v1/chat/completions \
-H "Content-Type: application/json" \
-d '{"messages": [{"role": "system", "content": "hello"}], "temperature": 1.0, "max_tokens": 1000, "stream": true, "model": "openai/gpt-oss-120b"}'

```

## 微调

GPT OSS 模型已完全集成到 `trl` 中。我们使用 `SFTTrainer` 开发了几个微调示例来帮助您入门：

- OpenAI 烹饪书中的一个 LoRA 示例，展示了如何对模型进行微调以使其能够用多种语言进行推理。
- 一个基本的微调脚本，您可以对其进行调整以满足您的需求。

## 在 Hugging Face 合作伙伴上部署

### Azure

Hugging Face 与 Azure 在其 Azure AI 模型目录上合作，将最受欢迎的开源模型（涵盖文本、视觉、语音和多模态任务）直接引入客户环境，以便部署到托管的在线端点，利用 Azure 的企业级基础设施、自动扩展和监控功能。

GPT OSS 模型现已可在 Azure AI 模型目录中使用（GPT OSS 20B, GPT OSS 120B），随时可以部署到在线端点进行实时推理。

![model card in azure ai model catalog](/images/posts/03c1441aee65.png)

Dell Enterprise Hub 是一个安全的在线门户，它简化了使用戴尔平台在本地训练和部署最新开源 AI 模型的过程。它是与戴尔合作开发的，提供优化的容器、对戴尔硬件的原生支持以及企业级安全功能。

GPT OSS 模型现已可在 Dell Enterprise Hub 上使用，随时可以在本地使用戴尔平台进行部署。

![model card in dell enterprise hub](/images/posts/90ba759f8fbb.png)

## 评估模型

GPT OSS模型是推理模型：因此评估时需要非常大的生成规模（新Token的最大数量），因为其生成内容会先包含推理过程，再给出实际答案。若生成规模设置过小，可能导致推理过程中断预测，从而产生假阴性结果。在计算评估指标前，应从模型答案中移除推理痕迹，以避免解析错误——这在数学或指令评估中尤为关键。

以下是通过lighteval评估模型的示例（需从源码安装）：

```shell
git clone https://github.com/huggingface/lighteval
pip install -e .[dev] # 请确保已安装正确版本的transformers！
lighteval accelerate \
    "model_name=openai/gpt-oss-20b,max_length=16384,skip_special_tokens=False,generation_parameters={temperature:1,top_p:1,top_k:40,min_p:0,max_new_tokens:16384}" \ 
    "extended|ifeval|0|0,lighteval|aime25|0|0" \
    --save-details --output-dir "openai_scores" \
    --remove-reasoning-tags --reasoning-tags="[('<|channel|>analysis<|message|>','<|end|><|start|>assistant<|channel|>final<|message|>')]" 

```

对于200亿参数模型，此操作应使IFEval（严格提示）得分为69.5（±1.9），AIME25（pass@1）得分为63.3（±8.9），这符合该规模推理模型的预期分数范围。

若需编写自定义评估脚本，请注意：为正确过滤推理标签，需在分词器中设置`skip_special_tokens=False`以获取完整的模型输出痕迹（从而使用与上例相同的字符串对过滤推理内容）——下文将解释具体原因。

## 对话与对话模板

OpenAI GPT OSS在其输出中采用“频道”概念。多数情况下，您会看到包含非面向最终用户内容（如思维链）的“分析”频道，以及包含实际面向用户消息的“最终”频道。

假设未使用工具，模型输出结构如下所示：

```
<|start|>assistant<|channel|>analysis<|message|>思维链<|end|><|start|>assistant<|channel|>final<|message|>实际消息
```

大多数情况下，您应忽略`<|channel|>final<|message|>`之后文本以外的所有内容。仅该文本应作为助手消息附加至对话历史，或展示给用户。但此规则有两个例外：在**训练**期间或模型**调用外部工具**时，可能需要将**分析**消息纳入历史记录。

**训练时**：若为训练格式化示例，通常需将思维链包含在最终消息中。正确做法是在`thinking`键中处理：

```py
chat = [
    {"role": "user", "content": "你好！"},
    {"role": "assistant", "content": "你好！"},
    {"role": "user", "content": "能思考这个问题吗？"},
    {"role": "assistant", "thinking": "正在认真思考...", "content": "好的！"}
]

inputs = tokenizer.apply_chat_template(chat, add_generation_prompt=False)
```

您可随意在先前轮次中包含`thinking`键，或在推理（非训练）时使用，但它们通常会被忽略。对话模板仅会包含最近的思维链，且仅在训练时（当`add_generation_prompt=False`且最终轮次为助手轮次时）生效。

如此设计的缘由很微妙：OpenAI gpt-oss模型基于丢弃所有非最终思维链的多轮对话数据训练。这意味着当您想微调OpenAI gpt-oss模型时，应采取相同做法。

- 让对话模板丢弃除最终思维链外的所有内容
- 屏蔽除最终助手轮次外所有轮次的标签，否则模型将在无思维链的先前轮次上训练，导致其学会生成无思维链的响应。这意味着您不能将整个多轮对话作为单个样本训练；而必须将其拆分为每个助手轮次一个样本，且每次仅解除最终助手轮次的屏蔽，使模型能从每轮学习，同时确保每次仅在最终消息中看到思维链。

### 系统与开发者消息

OpenAI GPT OSS的特殊之处在于：它在对话开始时区分“系统”消息与“开发者”消息，而大多数其他模型仅使用“系统”。在GPT OSS中，系统消息遵循严格格式，包含当前日期、模型身份标识和推理力度等级等信息；“开发者”消息则更自由，这使其（极易混淆地）类似于大多数其他模型的“系统”消息。

为使GPT OSS更适配标准API，对话模板会将“system”或“developer”角色的消息视为**开发者**消息。若需修改实际系统消息，可向对话模板传递特定参数`model_identity`或`reasoning_effort`：

```py
chat = [
    {"role": "system", "content": "这实际上会成为开发者消息！"}
]

tokenizer.apply_chat_template(
    chat, 
    model_identity="你是OpenAI GPT OSS。",
    reasoning_effort="high"  
)
```

### Transformers中的工具调用

GPT OSS支持两类工具：内置工具`browser`和`python`，以及用户提供的自定义工具。启用内置工具需将其名称以列表形式传递至对话模板的`builtin_tools`参数，如下所示。传递自定义工具时，可通过`tools`参数以JSON模式或带类型提示和文档字符串的Python函数形式提供。详见[对话模板工具文档](chat template tools documentation)，或直接修改下例：

```py
def get_current_weather(location: str):
    """
    以字符串形式返回指定地点的当前天气状况。

    参数：
        location: 需要查询天气的地点。
    """
    return "陆地气候。"  

chat = [
    {"role": "user", "content": "巴黎现在天气如何？"}
]

inputs = tokenizer.apply_chat_template(
    chat, 
    tools=[weather_tool], 
    builtin_tools=["browser", "python"],
    add_generation_prompt=True,
    return_tensors="pt"
)
```

若模型选择调用工具（以消息以`<|call|>`结尾为标志），则应将工具调用添加至对话历史，执行工具调用，再将工具结果加入对话并重新生成：

```py
tool_call_message = {
    "role": "assistant",
    "tool_calls": [
        {
            "type": "function",
            "function": {
                "name": "get_current_temperature", 
                "arguments": {"location": "Paris, France"}
            }
        }
    ]
}
chat.append(tool_call_message)

tool_output = get_current_weather("Paris, France")

tool_result_message = {
    "role": "tool",
    "content": tool_output
}
chat.append(tool_result_message)
```

## 致谢

本次发布对社区意义重大，跨团队与公司的协同努力使得生态系统能全面支持新模型。

本文作者选自为本文贡献内容的人员，并不代表其对项目的全部投入。除作者列表外，Merve和Sergio等人亦贡献了重要的内容审阅，特此致谢！

本次集成与赋能工作涉及数十位成员。在此不分先后地特别致谢开源团队的Cyril、Lysandre、Arthur、Marc、Mohammed、Nouamane、Harry、Benjamin、Matt；TRL团队的Ed、Lewis和Quentin全程参与；同时感谢评估团队的Clémentine，以及内核团队的David和Daniel。在商业合作方面，Simon、Alvaro、Jeff、Akos、Alvaro和Ivar作出了重要贡献。Hub与产品团队提供了推理服务商支持、llama.cpp支持及多项改进，这得益于Simon、Célina、Pierric、Lucain、Xuan-Son、Chunte和Julien的付出。法律团队的Magda和Anna也参与了相关工作。

Hugging Face的使命是助力社区高效运用这些模型。我们感谢vLLM等推动领域发展的企业，并珍视与推理服务提供商的持续合作，致力于打造更简易的模型构建方式。

当然，我们由衷赞赏OpenAI向广大社区开放这些模型的决策。期待未来涌现更多这样的贡献！

---

> 本文由AI自动翻译，原文链接：[Welcome GPT OSS, the new open-source model family from OpenAI!](https://huggingface.co/blog/welcome-openai-gpt-oss)
> 
> 翻译时间：2026-02-21 04:19
