---
title: Fireworks.ai 入驻 Hugging Face Hub，提供极速推理服务
title_original: Welcome Fireworks.ai on the Hub 🎆
date: '2025-02-14'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/fireworks-ai
author: ''
summary: Hugging Face 宣布 Fireworks.ai 成为其 Hub 上新的推理提供商，为用户在模型页面及整个生态系统中提供极速无服务器推理。文章介绍了如何通过网站
  UI、Python 和 JavaScript SDK 以及 HTTP 调用使用 Fireworks.ai 服务，并列举了首批支持的模型，包括 DeepSeek-R1、DeepSeek-V3
  等。用户可使用 Hugging Face Token 自动路由或自有 API 密钥进行调用，极大简化了模型推理流程。
categories:
- AI基础设施
tags:
- Fireworks.ai
- 推理提供商
- Hugging Face Hub
- 无服务器推理
- AI基础设施
draft: false
translated_at: '2026-05-15T05:57:07.796541'
---

# 欢迎 Fireworks.ai 入驻 Hub 🎆

继我们近期宣布 Hub 上的推理提供商后，我们激动地分享 Fireworks.ai 现已成为 HF Hub 上受支持的推理提供商！

Fireworks.ai 直接在模型页面以及整个 HF 库和工具生态系统中提供极速的无服务器推理，让您比以往更轻松地在喜爱的模型上运行推理。

从现在起，您可以通过 Fireworks.ai 对以下模型运行无服务器推理：

- deepseek-ai/DeepSeek-R1
- deepseek-ai/DeepSeek-V3
- mistralai/Mistral-Small-24B-Instruct-2501
- Qwen/Qwen2.5-Coder-32B-Instruct
- meta-llama/Llama-3.2-90B-Vision-Instruct

以及更多模型，完整列表请点击此处。

立即用 Fireworks.ai 点亮您的项目吧！

## 工作原理

### 在网站 UI 中

![Fireworks.ai 推理提供商 UI](/images/posts/829b0b7baed2.png)

在此处搜索 HF 上 Fireworks 支持的所有模型。

### 通过客户端 SDK

#### 使用 Python 和 huggingface_hub

以下示例展示了如何使用 Fireworks.ai 作为推理提供商来使用 DeepSeek-R1。您可以使用 Hugging Face Token 通过 Hugging Face 自动路由，或者如果您有自己的 Fireworks.ai API 密钥，也可以使用它。

从源码安装 huggingface_hub：

```bash
pip install git+https://github.com/huggingface/huggingface_hub

```

通过定义 provider 参数，使用 huggingface_hub Python 库调用 Fireworks.ai 端点。

```python
from huggingface_hub import InferenceClient

client = InferenceClient(
    provider="fireworks-ai",
    api_key="xxxxxxxxxxxxxxxxxxxxxxxx"
)

messages = [
    {
        "role": "user",
        "content": "法国的首都是哪里？"
    }
]

completion = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1", 
    messages=messages, 
    max_tokens=500
)

print(completion.choices[0].message)

```

#### 使用 JS 和 @huggingface/inference

```js
import { HfInference } from "@huggingface/inference";

const client = new HfInference("xxxxxxxxxxxxxxxxxxxxxxxx");

const chatCompletion = await client.chatCompletion({
    model: "deepseek-ai/DeepSeek-R1",
    messages: [
        {
            role: "user",
            content: "如何制作超辣蛋黄酱？"
        }
    ],
    provider: "fireworks-ai",
    max_tokens: 500
});

console.log(chatCompletion.choices[0].message);

```

### 通过 HTTP 调用

以下是通过 cURL 使用 Fireworks.ai 作为推理提供商调用 Llama-3.3-70B-Instruct 的方法。

```
curl 'https://router.huggingface.co/fireworks-ai/v1/chat/completions' \
-H 'Authorization: Bearer xxxxxxxxxxxxxxxxxxxxxxxx' \
-H 'Content-Type: application/json' \
--data '{
    "model": "accounts/fireworks/models/llama-v3p3-70b-instruct",
    "messages": [
        {
            "role": "user",
            "content": "如果你是一条狗，生命的意义是什么？"
        }
    ],
    "max_tokens": 500,
    "stream": false
}'

```

## 计费

对于直接请求（即您使用 Fireworks 密钥时），您将直接在 Fireworks 账户上计费。

对于路由请求（即您通过 Hub 进行身份验证时），您只需支付标准的 Fireworks API 费用。我们不会额外加价，只是直接传递提供商成本。（未来，我们可能会与提供商合作伙伴建立收入分成协议。）

重要提示 ‼️ PRO 用户每月可获得价值 2 美元的推理积分。您可以在不同提供商之间使用它们。🔥

订阅 Hugging Face PRO 计划，即可获得推理积分、ZeroGPU、Spaces 开发模式、20 倍更高的限制等更多权益。

---

> 本文由AI自动翻译，原文链接：[Welcome Fireworks.ai on the Hub 🎆](https://huggingface.co/blog/fireworks-ai)
> 
> 翻译时间：2026-05-15 05:57
