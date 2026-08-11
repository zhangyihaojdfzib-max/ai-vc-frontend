---
title: Baseten登陆Hugging Face推理提供商
title_original: Baseten on Hugging Face Inference Providers 🔥
date: '2026-08-06'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/baseten
author: ''
summary: Baseten正式成为Hugging Face Hub的推理提供商，支持对话和文本生成任务，用户可通过自定义密钥或HF路由调用模型。集成已覆盖Python和JS
  SDK及主流Agent框架，首批支持Kimi K3、DeepSeek V4 Flash等开放权重LLM，其他任务类型即将推出。
categories:
- AI基础设施
tags:
- Baseten
- Hugging Face
- 推理提供商
- 无服务器AI
- LLM
draft: false
translated_at: '2026-08-11T03:36:38.326417'
---

# Baseten 现已登陆 Hugging Face 推理提供商 🔥

我们非常激动地宣布，Baseten 现已成为 Hugging Face Hub 上受支持的推理提供商！

Baseten 的加入进一步壮大了我们的生态系统，直接在 Hub 的模型页面上增强了无服务器推理的广度和能力。推理提供商也已无缝集成到我们的客户端 SDK（JS 和 Python）中，让您能够极其轻松地使用您偏好的提供商来运行各种模型。

Baseten 是一个 AI 基础设施平台，涵盖无服务器 AI、训练等更多功能。凭借众多前沿模型目录，Baseten 让开发者能够以最少的设置，轻松将广泛的 AI 能力集成到他们的应用程序中。

Baseten 支持多种模型类型——从 LLM 到文本转语音等等。作为此次初步集成的一部分，Baseten 在 Hugging Face 上推出了对**对话和文本生成任务**的支持，使您能够访问流行的开放权重 LLM，例如 **Kimi K3**、最新的 **DeepSeek V4 Flash**、**GLM-5.2** 等。**对其他任务的支持**将很快推出！

查看 Baseten 支持的完整模型列表[此处](here)。

在 Hugging Face 上关注 Baseten：https://huggingface.co/baseten。

## 工作原理

### 在网站 UI 中

1. 在您的用户账户设置中，您可以：

- 为您注册的提供商设置您自己的 API 密钥。如果未设置自定义密钥，您的请求将通过 HF 路由。
- 按偏好顺序排列提供商。这适用于模型页面中的小部件和代码片段。

![推理提供商](/images/posts/7dae06f7c004.png)

1. 如前所述，调用推理提供商时有两种模式：

- 自定义密钥（请求直接发送到推理提供商，使用您在该推理提供商的 API 密钥）
- 由 HF 路由（在这种情况下，您不需要提供商的令牌，费用将直接计入您的 HF 账户，而非提供商账户）

![推理提供商](/images/posts/d2717fd3c654.png)

1. 模型页面展示第三方推理提供商（与当前模型兼容的提供商，按用户偏好排序）

### 从客户端 SDK

Baseten 可通过 Hugging Face SDK 使用——Python 的 `huggingface_hub`（>= 1.26.1）和 JavaScript 的 `@huggingface/inference`。

以下示例展示了如何通过 Baseten 使用最新的 **DeepSeek V4 Flash**。使用 Hugging Face 令牌进行身份验证——请求将自动路由到 Baseten。

#### 从您喜爱的 Agent 框架

Hugging Face 推理提供商已集成到大多数 Agent 框架中——包括 Pi、OpenCode、Hermes Agents、OpenClaw 等。这意味着您可以将 Baseten 托管的模型直接插入您喜爱的工具，无需任何额外的粘合代码。浏览完整的集成列表[此处](here)。

#### 从 Python

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V4-Flash-0731:baseten",
    messages=[
        {
            "role": "user",
            "content": "编写一个Python函数，使用记忆化返回第n个斐波那契数。"
        }
    ],
)

print(completion.choices[0].message)

```

#### 从 JS

```js
import { OpenAI } from "openai";

const client = new OpenAI({
    baseURL: "https://router.huggingface.co/v1",
    apiKey: process.env.HF_TOKEN,
});

const chatCompletion = await client.chat.completions.create({
    model: "deepseek-ai/DeepSeek-V4-Flash-0731:baseten",
    messages: [
        {
            role: "user",
            content: "编写一个JavaScript函数，使用记忆化返回第n个斐波那契数。",
        },
    ],
});

console.log(chatCompletion.choices[0].message);

```

## 计费

对于直接请求，即当您使用推理提供商的密钥时，由相应的提供商向您收费。例如，如果您使用 Baseten API 密钥，则费用计入您的 Baseten 账户。

对于路由请求，即当您通过 Hugging Face Hub 进行身份验证时，您只需支付标准的提供商 API 费率。我们不会额外加价；我们只是直接传递提供商的成本。（未来，我们可能会与我们的提供商合作伙伴建立收入分成协议。）

重要提示‼️ PRO 用户每月可获得价值 $2 的推理积分。您可以在各个提供商之间使用这些积分。🔥

订阅 [Hugging Face PRO 计划](Hugging Face PRO plan) 以获取推理积分、ZeroGPU、Spaces 开发模式、20 倍更高的限额等更多权益。

我们也为登录的免费用户提供少量配额的免费推理，但如果您可以，请升级到 PRO！

## 反馈与后续步骤

我们非常期待您的反馈！在此处分享您的想法和/或评论：https://huggingface.co/spaces/huggingface/HuggingDiscussions/discussions/49

---

> 本文由AI自动翻译，原文链接：[Baseten on Hugging Face Inference Providers 🔥](https://huggingface.co/blog/baseten)
> 
> 翻译时间：2026-08-11 03:36
