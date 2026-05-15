---
title: Hugging Face新增三家无服务器推理提供商
title_original: 'Introducing Three New Serverless Inference Providers: Hyperbolic,
  Nebius AI Studio, and Novita 🔥'
date: '2025-02-18'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/inference-providers-nebius-novita-hyperbolic
author: ''
summary: Hugging Face Hub宣布新增Hyperbolic、Nebius AI Studio和Novita三家无服务器推理提供商，扩展了模型推理的生态能力。新提供商支持DeepSeek-R1、Flux.1等热门模型，并已集成到Hugging
  Face的JS和Python SDK中。用户可在账户设置中配置自定义API密钥或通过HF路由请求，按偏好排序提供商。文章提供了Python代码示例，展示如何通过InferenceClient使用新提供商进行文本生成和图像生成任务。
categories:
- AI基础设施
tags:
- 无服务器推理
- Hugging Face
- 模型部署
- API集成
- AI基础设施
draft: false
translated_at: '2026-05-15T05:56:57.597820'
---

# 推出三个新的无服务器推理提供商：Hyperbolic、Nebius AI Studio 和 Novita 🔥

我们激动地宣布，Hugging Face Hub 新增了三个出色的无服务器推理提供商：Hyperbolic、Nebius AI Studio 和 Novita。这些提供商加入我们不断发展的生态系统，增强了 Hub 模型页面上无服务器推理的广度和能力。它们也已无缝集成到我们的客户端 SDK（适用于 JS 和 Python）中，使您能够轻松使用各种模型与您偏好的提供商。

这些合作伙伴加入了我们现有提供商的行列，包括 Together AI、Sambanova、Replicate、fal 和 Fireworks.ai。

新合作伙伴支持一系列新模型：DeepSeek-R1、Flux.1 等。以下是它们支持的所有模型：

- Nebius AI Studio
- Novita
- Hyperbolic

我们非常期待看到您使用这些新提供商构建的成果！

## 工作原理

### 在网站 UI 中

1. 在您的用户账户设置中，您可以：

- 为您注册的提供商设置自己的 API 密钥。如果未设置自定义密钥，您的请求将通过 HF 路由。
- 按偏好对提供商排序。这适用于模型页面中的小部件和代码片段。

![推理提供商](/images/posts/ffb2ed6fa1d1.png)

1. 如前所述，调用推理 API 时有两种模式：

- 自定义密钥（请求直接发送到推理提供商，使用您自己的对应推理提供商的 API 密钥）
- 由 HF 路由（在这种情况下，您不需要提供商的 Token，费用直接计入您的 HF 账户而非提供商账户）

![推理提供商](/images/posts/d2717fd3c654.png)

1. 模型页面展示第三方推理提供商（与当前模型兼容的提供商，按用户偏好排序）

### 从客户端 SDK

#### 从 Python，使用 huggingface_hub

以下示例展示了如何使用 Hyperbolic 作为推理提供商来使用 DeepSeek-R1。您可以使用 Hugging Face Token 通过 Hugging Face 自动路由，或者如果您有 Hyperbolic API 密钥，也可以使用自己的密钥。

从源码安装 huggingface_hub（参见说明）。官方支持将在 v0.29.0 版本中很快发布。

```python
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="hyperbolic",
    api_key="xxxxxxxxxxxxxxxxxxxxxxxx"
)

messages = [
    {
        "role": "user",
        "content": "法国的首都是什么？"
    }
]

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1", 
    messages=messages, 
    max_tokens=500
)

print(completion.choices[0].message)

```

以下示例展示了如何使用运行在 Nebius AI Studio 上的 FLUX.1-dev 从文本提示词生成图像：

```python
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="nebius",
    api_key="xxxxxxxxxxxxxxxxxxxxxxxx"
)

image = client.text_to_image(
    "以约翰内斯·维米尔画作风格的鲍勃·马利",
    model="black-forest-labs/FLUX.1-schnell"
)

```

要切换到不同的提供商，您只需更改提供商名称，其他一切保持不变：

```diff
from huggingface_hub import InferenceClient

client = InferenceClient(
-	provider="nebius",
+   provider="hyperbolic",
    api_key="xxxxxxxxxxxxxxxxxxxxxxxx"
)

```

#### 从 JS，使用 @huggingface/inference

```js
import { HfInference } from "@huggingface/inference";

const client = new HfInference("xxxxxxxxxxxxxxxxxxxxxxxx");

const chatCompletion = await client.chatCompletion({
    model: "deepseek-ai/DeepSeek-R1",
    messages: [
        {
            role: "user",
            content: "法国的首都是什么？"
        }
    ],
    provider: "novita",
    max_tokens: 500
});

console.log(chatCompletion.choices[0].message);

```

## 计费

对于直接请求，即当您使用推理提供商的密钥时，由相应提供商向您收费。例如，如果您使用 Nebius AI Studio 的密钥，费用将计入您的 Nebius AI Studio 账户。

对于路由请求，即当您通过 Hub 进行身份验证时，您只需支付标准的提供商 API 费率。我们不会额外加价，只是直接传递提供商成本。（未来，我们可能会与提供商合作伙伴建立收入分成协议。）

重要提示‼️ PRO 用户每月可获得价值 2 美元的推理积分。您可以在各提供商之间使用它们。🔥

订阅 Hugging Face PRO 计划，即可获得推理积分、ZeroGPU、Spaces Dev Mode、20 倍更高的限制等。

我们还为已登录的免费用户提供少量免费推理配额，但如果可以，请升级到 PRO！

## 反馈与后续步骤

我们非常希望收到您的反馈！以下是您可以使用的 Hub 讨论：https://huggingface.co/spaces/huggingface/HuggingDiscussions/discussions/49

---

> 本文由AI自动翻译，原文链接：[Introducing Three New Serverless Inference Providers: Hyperbolic, Nebius AI Studio, and Novita 🔥](https://huggingface.co/blog/inference-providers-nebius-novita-hyperbolic)
> 
> 翻译时间：2026-05-15 05:56
