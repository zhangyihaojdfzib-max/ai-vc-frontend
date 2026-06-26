---
title: Llama 3.2发布：多模态与设备端小模型齐登场
title_original: Llama can now see and run on your device - welcome Llama 3.2
date: '2024-09-25'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/llama32
author: ''
summary: Meta与Hugging Face合作发布Llama 3.2，包含多模态视觉模型（11B/90B）和轻量级纯文本模型（1B/3B），支持设备端运行。视觉模型具备图像理解、文档推理等能力，小模型适合边缘部署。文章介绍了模型特性、许可证变更（欧盟受限）、集成方式（Transformers、TGI、Inference
  Endpoints）及微调支持，强调开放权重与多平台兼容性。
categories:
- AI产品
tags:
- Llama 3.2
- 多模态模型
- 设备端AI
- Meta
- Hugging Face
draft: false
translated_at: '2026-06-26T06:11:32.972032'
---

# Llama 现在可以看见并运行在你的设备上——欢迎 Llama 3.2

Llama 3.2 发布了！今天，我们欢迎 Llama 系列的下一个迭代版本来到 Hugging Face。这一次，我们很高兴与 Meta 合作发布多模态和小型模型。Hub 上提供了十个开放权重模型（5 个多模态模型和 5 个纯文本模型）。

Llama 3.2 Vision 提供两种尺寸：11B 适用于消费级 GPU 的高效部署和开发，90B 适用于大规模应用。两个版本都有基础版和指令微调版。除了四个多模态模型外，Meta 还发布了支持视觉功能的新版 Llama Guard。Llama Guard 3 是一个安全防护模型，可以对模型输入和生成内容进行分类，包括检测有害的多模态提示词或助手回复。

Llama 3.2 还包括可以在设备上运行的小型纯文本语言模型。它们有两种新尺寸（1B 和 3B），提供基础版和指令版，并且在其尺寸下具有强大的能力。还有一个 1B 的小型 Llama Guard 版本，可以在生产用例中与这些模型或更大的文本模型一起部署。

在发布的功能和集成中，我们包括：

- Hub 上的模型检查点
- 视觉模型的 Hugging Face Transformers 和 TGI 集成
- 与 Inference Endpoints、Google Cloud、Amazon SageMaker 和 DELL Enterprise Hub 的推理与部署集成
- 在单 GPU 上使用 transformers🤗 和 TRL 微调 Llama 3.2 11B Vision

- 什么是 Llama 3.2 Vision？
- Llama 3.2 许可证变更。抱歉，欧盟 :(
- Llama 3.2 1B 和 3B 有什么特别之处？
- 演示
- 使用 Hugging Face Transformers
- Llama 3.2 1B 和 3B 语言模型
- Llama 3.2 Vision
- 设备端
- Llama.cpp 和 Llama-cpp-python
- Transformers.js
- 微调 Llama 3.2
- Hugging Face 合作伙伴集成
- 其他资源
- 致谢

## 什么是 Llama 3.2 Vision？

Llama 3.2 Vision 是 Meta 发布的最强大的开放多模态模型。它具有出色的视觉理解和推理能力，可用于完成各种任务，包括视觉推理和定位、文档问答以及图像文本检索。思维链（CoT）答案通常非常好，这使得视觉推理特别强大。

Llama 3.2 Vision 可用于处理文本和图像，以及仅处理文本。使用图像文本提示词时，模型可以接受英文输入，而仅使用文本提示词时，模型可以处理多种语言。

纯文本模式下的完整语言列表是：

- 英语
- 德语
- 法语
- 意大利语
- 葡萄牙语
- 印地语
- 西班牙语
- 泰语

这些模型的架构基于 Llama 3.1 LLM 与视觉塔和图像适配器的组合。使用的文本模型是 Llama 3.1 8B（用于 Llama 3.2 11B Vision 模型）和 Llama 3.1 70B（用于 3.2 90B Vision 模型）。据我们所知，在训练视觉模型期间，文本模型被冻结以保持纯文本性能。

下面你可以找到来自 11B 指令微调模型的一些推理示例，展示了现实世界知识、文档推理和信息图理解能力。

![](/images/posts/b92839f9bd10.jpg)

![](/images/posts/1610ddbd29d2.png)

![](/images/posts/ad184797225c.png)

视觉模型的上下文窗口长度为 128k Token，允许包含图像的多轮对话。然而，模型在关注单个图像时效果最佳，因此 transformers 实现只关注输入中提供的最后一张图像。这保持了质量并节省了内存。

11B 基础模型支持 448 的图块尺寸，而指令版和 90B 模型都使用 560 的图块尺寸。这些模型在包含 60 亿个图像文本对的大规模数据集上进行了训练，数据混合多样。这使得它们非常适合在下游任务上进行微调。作为参考，你可以看到下面 11B、90B 及其指令微调版本在 Meta 报告的一些基准测试中的对比。请参考模型卡片以获取更多基准测试和详细信息。

我们预计这些模型的文本能力分别与 8B 和 70B Llama 3.1 模型相当，因为据我们了解，在训练视觉模型期间文本模型被冻结。因此，文本基准测试应与 8B 和 70B 保持一致。

## Llama 3.2 许可证变更。抱歉，欧盟 :(

![许可证变更](/images/posts/a056b68cf9be.png)

关于许可条款，Llama 3.2 的许可证与 Llama 3.1 非常相似，但在可接受使用政策上有一个关键区别：任何居住在欧盟的个人或主要营业地在欧盟的公司，均未被授予使用 Llama 3.2 中包含的多模态模型的许可权利。此限制不适用于包含任何此类多模态模型的产品或服务的最终用户，因此人们仍然可以使用视觉变体构建全球产品。

有关完整详情，请务必阅读官方许可证和可接受使用政策。

## Llama 3.2 1B 和 3B 有什么特别之处？

Llama 3.2 系列包括 1B 和 3B 文本模型。这些模型专为设备端用例设计，例如提示词重写、多语言知识检索、摘要任务、工具使用和本地运行的助手。它们在这些尺寸上优于许多可用的开放访问模型，并与大数倍的模型竞争。在后面的章节中，我们将向你展示如何离线运行这些模型。

这些模型遵循与 Llama 3.1 相同的架构。它们使用多达 9 万亿 Token 进行训练，并且仍然支持 128k Token 的长上下文窗口。这些模型是多语言的，支持英语、德语、法语、意大利语、葡萄牙语、印地语、西班牙语和泰语。

还有一个新的小型 Llama Guard 版本，Llama Guard 3 1B，可以与这些模型一起部署，用于评估多轮对话中的最后用户或助手回复。它使用一组预定义的类别（此版本新增），可以根据开发者的用例进行自定义或排除。有关使用 Llama Guard 的更多详情，请参考模型卡片。

额外福利：Llama 3.2 接触到的语言范围比上述 8 种支持语言更广。鼓励开发者针对其特定语言用例微调 Llama 3.2 模型。

我们通过 Open LLM Leaderboard 评估套件运行了基础模型，而指令模型则通过三个衡量指令遵循能力并与 LMSYS Chatbot Arena 相关性良好的流行基准进行了评估：IFEval、AlpacaEval 和 MixEval-Hard。以下是基础模型的结果，以 Llama-3.1-8B 作为参考：

以下是指令模型的结果，以 Llama-3.1-8B-Instruct 作为参考：

值得注意的是，3B 模型在 IFEval 上与 8B 模型一样强大！这使得该模型非常适合 Agent（智能体）应用，在这些应用中遵循指令对于提高可靠性至关重要。对于这种尺寸的模型来说，如此高的 IFEval 分数令人印象深刻。

1B 和 3B 指令微调模型都支持工具使用。工具由用户在零样本设置中指定（模型事先不知道开发者将使用的工具信息）。因此，Llama 3.1 模型中内置的工具（brave_search 和 wolfram_alpha）不再可用。

由于其尺寸，这些小型模型可以用作更大模型的助手，并执行辅助生成（也称为推测解码）。这里有一个使用 Llama 3.2 1B 模型作为 Llama 3.1 8B 模型助手的示例。对于离线用例，请查看本文后面的设备端部分。

你可以在以下演示中尝试三个指令模型：

- 搭载 Llama 3.2 11B Vision Instruct 的 Gradio Space
- 搭载 Llama 3.2 3B 的 Gradio Space
- 在 WebGPU 上运行的 Llama 3.2 3B
- 由 MLC Web-LLM 驱动的 WebGPU Llama 3.2 3B

![演示 GIF](/images/posts/ca90cf0655f4.gif)

## 使用 Hugging Face Transformers

纯文本检查点与之前版本具有相同的架构，因此无需更新环境。然而，鉴于新架构，Llama 3.2 Vision 需要对 Transformers 进行更新。请确保将安装版本升级到 4.45.0 或更高版本。

```bash
pip install "transformers>=4.45.0" --upgrade

```

升级完成后，您就可以使用新的 Llama 3.2 模型，并利用 Hugging Face 生态系统的所有工具。

## Llama 3.2 1B 和 3B 语言模型

您只需几行代码即可通过 Transformers 运行 1B 和 3B 文本模型检查点。模型检查点以 `bfloat16` 精度上传，但您也可以使用 `float16` 或量化权重。内存需求取决于模型大小和权重精度。下表显示了使用不同配置进行推理所需的大致内存：

```python
from transformers import pipeline
import torch

model_id = "meta-llama/Llama-3.2-3B-Instruct"
pipe = pipeline(
    "text-generation",
    model=model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

messages = [
    {"role": "user", "content": "你是谁？请用海盗语回答。"},
]
outputs = pipe(
    messages,
    max_new_tokens=256,
)
response = outputs[0]["generated_text"][-1]["content"]
print(response)


```

几点说明：

- 我们以 `bfloat16` 加载模型。如上所述，这是 Meta 发布的原始检查点所使用的类型，因此是确保最佳精度或进行评估的推荐运行方式。根据您的硬件，`float16` 可能更快。
- 默认情况下，transformers 使用与原始 meta 代码库相同的采样参数（`temperature=0.6` 和 `top_p=0.9`）。我们尚未进行广泛测试，欢迎自行探索！

我们以 `bfloat16` 加载模型。如上所述，这是 Meta 发布的原始检查点所使用的类型，因此是确保最佳精度或进行评估的推荐运行方式。根据您的硬件，`float16` 可能更快。

默认情况下，transformers 使用与原始 meta 代码库相同的采样参数（`temperature=0.6` 和 `top_p=0.9`）。我们尚未进行广泛测试，欢迎自行探索！

## Llama 3.2 Vision

视觉模型更大，因此运行所需的内存比小型文本模型更多。作为参考，11B 视觉模型在 4 位模式下推理时大约需要 10 GB 的 GPU 内存。

对指令微调的 Llama Vision 模型进行推理的最简单方法是使用内置的聊天模板。输入使用 `user` 和 `assistant` 角色来指示对话轮次。与文本模型的一个区别是不支持 `system` 角色。用户轮次可以包含图像-文本或纯文本输入。要指示输入包含图像，请在输入的 `content` 部分添加 `{"type": "image"}`，然后将图像数据传递给 `processor`：

```python
import requests
import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor

model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"
model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device="cuda",
)
processor = AutoProcessor.from_pretrained(model_id)

url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/0052a70beed5bf71b92610a43a52df6d286cd5f3/diffusers/rabbit.jpg"
image = Image.open(requests.get(url, stream=True).raw)

messages = [
    {"role": "user", "content": [
        {"type": "image"},
        {"type": "text", "text": "你能用一句话描述这张图片吗？"}
    ]}
]

input_text = processor.apply_chat_template(
    messages, add_generation_prompt=True,
)
inputs = processor(
    image,
    input_text,
    add_special_tokens=False,
    return_tensors="pt",
).to(model.device)
output = model.generate(**inputs, max_new_tokens=70)

print(processor.decode(output[0][inputs["input_ids"].shape[-1]:]))




```

您可以继续关于这张图片的对话。但请记住，如果您在新的用户轮次中提供一张新图片，模型将从那时起引用新图片。您不能同时查询两张不同的图片。以下是之前对话的延续示例，我们在对话中添加了助手轮次并询问更多细节：

```python
messages = [
    {"role": "user", "content": [
        {"type": "image"},
        {"type": "text", "text": "你能用一句话描述这张图片吗？"}
    ]},
    {"role": "assistant", "content": "这张图片描绘了一只穿着蓝色外套和棕色马甲的兔子，站在一座石头房子前的土路上。"},
    {"role": "user", "content": "背景里有什么？"}
]

input_text = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
)
inputs = processor(image, input_text, return_tensors="pt").to(model.device)
output = model.generate(**inputs, max_new_tokens=70)
print(processor.decode(output[0][inputs["input_ids"].shape[-1]:]))

```

这是我们得到的回复：

```
背景中有一座茅草屋顶的石头房子、一条土路、一片花田和连绵起伏的山丘。

```

您还可以使用 `bitsandbytes` 库自动量化模型，以 8 位甚至 4 位模式加载。以下是如何以 4 位模式加载生成流水线：

```diff
import torch
from transformers import MllamaForConditionalGeneration, AutoProcessor
+from transformers import BitsAndBytesConfig

+bnb_config = BitsAndBytesConfig(
+    load_in_4bit=True,
+    bnb_4bit_quant_type="nf4",
+    bnb_4bit_compute_dtype=torch.bfloat16
)
 
model = MllamaForConditionalGeneration.from_pretrained(
    model_id,
-   torch_dtype=torch.bfloat16,
-   device="cuda",
+   quantization_config=bnb_config,
)

```

然后您可以像之前一样应用聊天模板、使用 processor 并调用模型。

## 设备端运行

您可以使用以下多个开源库，直接在设备的 CPU/GPU/浏览器上运行 Llama 3.2 1B 和 3B。

### Llama.cpp 和 Llama-cpp-python

Llama.cpp 是跨平台设备端机器学习推理的首选框架。我们在本集合中为 1B 和 3B 模型提供了量化的 4 位和 8 位权重。我们期待社区接纳这些模型并创建额外的量化和微调版本。您可以在此处找到所有量化的 Llama 3.2 模型。

以下是如何直接使用 llama.cpp 使用这些检查点。

通过 brew 安装 llama.cpp（适用于 Mac 和 Linux）。

```bash
brew install llama.cpp

```

您可以使用 CLI 运行单次生成，或调用与 OpenAI 消息规范兼容的 llama.cpp 服务器。

您可以使用如下命令运行 CLI：

```bash
llama-cli --hf-repo hugging-quants/Llama-3.2-3B-Instruct-Q8_0-GGUF --hf-file llama-3.2-3b-instruct-q8_0.gguf -p "生命和宇宙的意义是"

```

然后像这样启动服务器：

```bash
llama-server --hf-repo hugging-quants/Llama-3.2-3B-Instruct-Q8_0-GGUF --hf-file llama-3.2-3b-instruct-q8_0.gguf -c 2048

```

您还可以使用 `llama-cpp-python` 在 Python 中以编程方式访问这些模型。通过 PyPI 使用以下命令安装该库：

```bash
pip install llama-cpp-python

```

然后，您可以按如下方式运行模型：

```python
from llama_cpp import Llama

llm = Llama.from_pretrained(
    repo_id="hugging-quants/Llama-3.2-3B-Instruct-Q8_0-GGUF",
    filename="*q8_0.gguf",
)
output = llm.create_chat_completion(
      messages = [
          {
              "role": "user",
              "content": "法国的首都是哪里？"
          }
      ]
)

print(output)

```

### Transformers.js

你甚至可以使用Transformers.js在浏览器（或任何JavaScript运行时，如Node.js、Deno或Bun）中运行Llama 3.2。你可以在Hub上找到ONNX模型。如果尚未安装，你可以通过NPM安装该库：

```bash
npm i @huggingface/transformers
```

```js
import { pipeline } from "@huggingface/transformers";

const generator = await pipeline("text-generation", "onnx-community/Llama-3.2-1B-Instruct");

const messages = [
  { role: "system", content: "You are a helpful assistant." },
  { role: "user", content: "Tell me a joke." },
];

const output = await generator(messages, { max_new_tokens: 128 });
console.log(output[0].generated_text.at(-1).content);
```

```
Here's a joke for you:

What do you call a fake noodle?

An impasta!

I hope that made you laugh! Do you want to hear another one?
```

### MLC.ai Web-LLM

MLC.ai Web-LLM是一个高性能的浏览器内LLM推理引擎，它通过硬件加速将语言模型推理直接引入网页浏览器。一切都在浏览器内运行，无需服务器支持，并通过WebGPU进行加速。

WebLLM与OpenAI API完全兼容。也就是说，你可以在本地任何开源模型上使用相同的OpenAI API，功能包括流式传输、JSON模式、函数调用等。

你可以通过npm安装Web-LLM：

```bash
npm install @mlc/web-llm
```

```js
import * as webllm from "@mlc-ai/web-llm";
import { CreateMLCEngine } from "@mlc-ai/web-llm";

const initProgressCallback = (initProgress) => {
  console.log(initProgress);
}
const selectedModel = "Llama-3.2-3B-Instruct-q4f32_1-MLC";

const engine = await CreateMLCEngine(
  selectedModel,
  { initProgressCallback: initProgressCallback }, 
);
```

成功初始化引擎后，你现在可以通过`engine.chat.completions`接口调用OpenAI风格的聊天API。

```js
const messages = [
  { role: "system", content: "You are a helpful AI assistant." },
  { role: "user", content: "Explain the meaning of life as a pirate!" },
]

const reply = await engine.chat.completions.create({
  messages,
});
console.log(reply.choices[0].message);
console.log(reply.usage);
```

## 微调 Llama 3.2

TRL开箱即支持Llama 3.2文本模型的聊天和微调：

```bash
trl chat --model_name_or_path meta-llama/Llama-3.2-3B

trl sft  --model_name_or_path meta-llama/Llama-3.2-3B \
         --dataset_name HuggingFaceH4/no_robots \
         --output_dir Llama-3.2-3B-Instruct-sft \
         --gradient_checkpointing
```

TRL中也提供了对Llama 3.2 Vision微调的支持，详见此脚本。

```bash
accelerate launch --config_file=examples/accelerate_configs/deepspeed_zero3.yaml \
    examples/scripts/sft_vlm.py \
    --dataset_name HuggingFaceH4/llava-instruct-mix-vsft \
    --model_name_or_path meta-llama/Llama-3.2-11B-Vision-Instruct \
    --per_device_train_batch_size 8 \
    --gradient_accumulation_steps 8 \
    --output_dir Llama-3.2-11B-Vision-Instruct-sft \
    --bf16 \
    --torch_dtype bfloat16 \
    --gradient_checkpointing
```

你也可以查看此笔记本，了解如何使用transformers和PEFT进行LoRA微调。

## Hugging Face 合作伙伴集成

我们目前正与AWS、Google Cloud、Microsoft Azure和DELL的合作伙伴合作，将Llama 3.2 11B、90B添加到Amazon SageMaker、Google Kubernetes Engine、Vertex AI Model Catalog、Azure AI Studio、DELL Enterprise Hub中。一旦容器可用，我们将更新此部分，你也可以订阅Hugging Squad以获取邮件更新。

## 其他资源

- Hub上的模型
- Hugging Face Llama Recipes
- Open LLM Leaderboard
- Meta博客
- 评估数据集

## 致谢

如果没有成千上万的社区成员对transformers、text-generation-inference、vllm、pytorch、LM Eval Harness等众多项目的贡献，发布此类模型并在生态系统中提供支持和评估是不可能的。特别感谢VLLM团队在测试和报告问题方面的帮助。此次发布离不开以下所有人的支持：Clémentine、Alina、Elie和Loubna在LLM评估方面的贡献；Nicolas Patry、Olivier Dehaene和Daniël de Kok在Text Generation Inference方面的贡献；Lysandre、Arthur、Pavel、Edward Beeching、Amy、Benjamin、Joao、Pablo、Raushan Turganbay、Matthew Carrigan和Joshua Lochner在transformers、transformers.js、TRL和PEFT支持方面的贡献；Nathan Sarrazin和Victor在Hugging Chat中提供Llama 3.2的贡献；Brigitte Tousignant和Florent Daudens在沟通方面的贡献；Hub团队的Julien、Simon、Pierric、Eliott、Lucain、Alvaro、Caleb和Mishig在Hub开发和发布功能方面的贡献。

并衷心感谢Meta团队发布Llama 3.2并将其提供给开放AI社区！

---

> 本文由AI自动翻译，原文链接：[Llama can now see and run on your device - welcome Llama 3.2](https://huggingface.co/blog/llama32)
> 
> 翻译时间：2026-06-26 06:11
