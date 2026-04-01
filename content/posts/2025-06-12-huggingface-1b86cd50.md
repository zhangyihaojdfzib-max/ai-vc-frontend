---
title: Featherless AI 成为 Hugging Face 推理服务提供商
title_original: Featherless AI on Hugging Face Inference Providers 🔥
date: '2025-06-12'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/inference-providers-featherless
author: ''
summary: Featherless AI 正式成为 Hugging Face Hub 支持的推理服务提供商，为用户提供无服务器 AI 推理服务。它支持 DeepSeek、Meta、Google、Qwen
  等众多开源模型，结合了广泛的模型选择与无服务器定价优势。用户可通过网站界面或客户端 SDK（Python/JS）轻松调用，并支持自定义 API 密钥或通过 Hugging
  Face 路由两种模式。
categories:
- AI基础设施
tags:
- Hugging Face
- AI推理
- 无服务器计算
- 开源模型
- Featherless AI
draft: false
translated_at: '2026-04-01T05:13:57.337280'
---

# Featherless AI 成为 Hugging Face 推理服务提供商 🔥

我们非常高兴地宣布，**Featherless AI** 现已正式成为 Hugging Face Hub 支持的推理服务提供商！
Featherless AI 加入了我们不断壮大的生态系统，直接在 Hub 的模型页面上增强了无服务器推理的广度和能力。推理服务提供商也已无缝集成到我们的客户端 SDK（包括 JS 和 Python 版本）中，让您能够轻松地使用首选提供商的各种模型。

**Featherless AI** 支持多种文本和对话模型，包括来自 DeepSeek、Meta、Google、Qwen 等的最新开源模型。

Featherless AI 是一家无服务器 AI 推理服务提供商，拥有独特的模型加载和 GPU 编排能力，为用户提供了极其庞大的模型目录。其他提供商通常要么以较低成本提供有限模型集合的访问，要么提供无限范围的模型但需要用户自行管理服务器并承担相关运营成本。Featherless 则结合了两者的优点，提供无与伦比的模型范围和多样性，同时采用无服务器定价模式。您可以在其**模型页面**上找到支持的完整模型列表。

我们非常期待看到您将利用这个新提供商构建出怎样的应用！

在其专门的**文档页面**中阅读更多关于如何将 Featherless 用作推理服务提供商的信息。

## 工作原理

### 在网站界面中

1.  在您的用户账户设置中，您可以：
    *   为您已注册的提供商设置您自己的 API 密钥。如果未设置自定义密钥，您的请求将通过 HF 路由。在**文档**中了解更多关于请求类型的信息。
    *   按偏好排序提供商。这适用于模型页面中的小部件和代码片段。

![推理服务提供商](/images/posts/ffb2ed6fa1d1.png)

2.  如前所述，调用推理服务提供商时有两种模式：
    *   自定义密钥（使用您自己的相应推理服务提供商的 API 密钥，调用直接发送给推理服务提供商）
    *   由 HF 路由（在这种情况下，您不需要提供商的令牌，费用将直接计入您的 HF 账户，而不是提供商的账户）

![推理服务提供商](/images/posts/d2717fd3c654.png)

3.  模型页面会展示第三方推理服务提供商（与当前模型兼容的提供商，按用户偏好排序）

### 通过客户端 SDK

#### 使用 Python 和 huggingface_hub

以下示例展示了如何使用 Featherless AI 作为推理服务提供商来使用 DeepSeek-R1。您可以使用 **Hugging Face 令牌**通过 Hugging Face 进行自动路由，或者如果您有的话，也可以使用您自己的 Featherless AI API 密钥。

安装或升级 `huggingface_hub` 以确保您拥有 v0.33.0 或更高版本：`pip install --upgrade huggingface-hub`

```python
import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="featherless-ai",
    api_key=os.environ["HF_TOKEN"]
)

messages = [
    {
        "role": "user",
        "content": "What is the capital of France?"
    }
]

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1-0528", 
    messages=messages, 
)

print(completion.choices[0].message)

```

#### 使用 JS 和 @huggingface/inference

```js
import { InferenceClient } from "@huggingface/inference";

const client = new InferenceClient(process.env.HF_TOKEN);

const chatCompletion = await client.chatCompletion({
    model: "deepseek-ai/DeepSeek-R1-0528",
    messages: [
        {
            role: "user",
            content: "What is the capital of France?"
        }
    ],
    provider: "featherless-ai",
});

console.log(chatCompletion.choices[0].message);

```

## 计费

对于直接请求，即当您使用推理服务提供商的密钥时，您将由相应的提供商计费。例如，如果您使用 Featherless AI API 密钥，费用将计入您的 Featherless AI 账户。

对于路由请求，即当您通过 Hugging Face Hub 进行身份验证时，您只需支付标准的提供商 API 费率。我们不会额外加价，我们只是直接传递提供商的成本。（未来，我们可能会与我们的提供商合作伙伴建立收入分成协议。）

重要提示‼️ PRO 用户每月可获得价值 2 美元的推理额度。您可以在所有提供商中使用这些额度。🔥

订阅 **Hugging Face PRO 计划**，即可获得推理额度、ZeroGPU、Spaces 开发者模式、20 倍更高的限制等权益。

我们也为已登录的免费用户提供少量配额的免费推理，但如果可以的话，请升级到 PRO！

## 反馈与后续步骤

我们非常希望获得您的反馈！请在此处分享您的想法和/或评论：https://huggingface.co/spaces/huggingface/HuggingDiscussions/discussions/49

---

> 本文由AI自动翻译，原文链接：[Featherless AI on Hugging Face Inference Providers 🔥](https://huggingface.co/blog/inference-providers-featherless)
> 
> 翻译时间：2026-04-01 05:13
