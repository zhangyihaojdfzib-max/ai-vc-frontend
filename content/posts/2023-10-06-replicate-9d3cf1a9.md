---
title: 如何通过API运行Mistral 7B：性能优势与实战指南
title_original: How to run Mistral 7B with an API – Replicate blog
date: '2023-10-06'
source: Replicate Blog
source_url: https://replicate.com/blog/run-mistral-7b-with-api
author: ''
summary: 本文介绍了Mistral AI发布的开源语言模型Mistral 7B及其指令微调版Mistral 7B Instruct。文章重点阐述了该模型在训练数据时效性、推理速度以及代码生成能力方面的优势，并提供了通过Replicate平台使用JavaScript、Python客户端或直接调用HTTP
  API来运行该模型的详细代码示例。
categories:
- AI基础设施
tags:
- Mistral 7B
- API调用
- 开源模型
- Replicate
- 语言模型
draft: false
translated_at: '2026-04-16T04:59:21.221955'
---

-   Replicate
-   Blog

# 如何通过 API 运行 Mistral 7B

-   daanelson
-   zeke

Mistral 7B 是来自 **Mistral AI** 的一款新的开源语言模型，其性能不仅超越了所有其他 70 亿参数的语言模型，也超越了 Llama 2 13B，有时甚至超越了原始的 Llama 34B。在编码任务上，它接近 CodeLlama 7B 的性能。

还有 **Mistral 7B Instruct**，这是一个为聊天补全进行微调的模型。其性能可与为聊天微调的 **Llama 2 13B** 相媲美。

@a16z-infra 已将 **Mistral 7B** 和 **Mistral 7B Instruct** 推送至 Replicate。让我们先看看 Mistral 7B 的突出之处，然后我们将展示如何通过 API 运行它。

## 它拥有更新的训练数据

Mistral 7B 的训练数据截止时间大约在 2023 年，因此它了解今年发生的事情。

![在 Replicate 上尝试此提示词](/images/posts/41617eb0a947.webp)

请记住，Mistral 只是一个语言模型，因此容易出现幻觉。尽管它的训练数据更新到 2023 年，但这并不意味着它能可靠地复述那些事情。😃

## 它速度更快

Mistral 7B 使用分组查询注意力（grouped-query attention）和滑动窗口注意力（sliding window attention）来提高速度并减少内存使用。Mistral 团队发现，使用滑动窗口注意力使他们在 16k Token 序列长度上的推理速度提高了一倍。有关这些技术的更多细节，以及对 Mistral 7B 和 Llama 的深入比较，请查看 **Mistral AI 的发布博客文章**。

## 它擅长编写代码

我们发现 Mistral 7B 编写代码的能力很好，而且还有点风格。以下是 Mistral 在像一个海盗一样说话时，编写一个计算斐波那契数列的 Python 函数：

![在 Replicate 上尝试此提示词](/images/posts/ce325034c484.webp)

并且，作为对其能力的最后一点展示，它在生成食谱方面做得非常好，即使使用非传统的食材：

![在 Replicate 上尝试此提示词](/images/posts/c25f69dca8bc.webp)

Mistral 7B 已在 Replicate 上，您可以用一行代码在云端运行它。

您可以使用我们的 **JavaScript 客户端** 运行它：

```
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});

const input = {
  prompt:
    "Write a poem about open source machine learning in the style of Mary Oliver.",
};

for await (const event of replicate.stream(
  "mistralai/mistral-7b-instruct-v0.2",
  {
    input,
  }
)) {
  process.stdout.write(event.toString());
}
```

或者，使用我们的 **Python 客户端**：

```
import replicate

# The mistralai/mistral-7b-instruct-v0.2 model can stream output as it's running.
for event in replicate.stream(
    "mistralai/mistral-7b-instruct-v0.2",
    input={"prompt": "how are you doing today?"},
):
    print(str(event), end="")
```

或者，您可以使用 cURL 等工具 **直接调用 HTTP API**：

```
curl -s -X POST \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: wait" \
  -d $'{
    "input": {
      "prompt": "how are you doing today? "
    }
  }' \
  https://api.replicate.com/v1/models/mistralai/mistral-7b-instruct-v0.2/predictions
```

您也可以使用 **Replicate 为 Go、Swift、Elixir 等语言提供的其他客户端库** 来运行 Mistral。

## 后续步骤

-   查看 Replicate 上的 **a16z-infra/mistral-7b-v0.1** 和 **a16z-infra/mistral-7b-instruct-v0.1**。
-   Mistral 7B 的微调版本也正在兴起。**nateraw/mistral-7b-openorca** 是在 **Open Orca 数据集** 上为聊天进行微调的。
-   🥊 想将 Mistral 与 Llama 进行比较吗？我们建立了一个名为 **LLM Boxing** 的网站，让语言模型在盲测中相互竞争，并由您决定哪个模型更好。在发布本文时，Mistral 7b Instruct 以 3985 比 3335 领先于 Llama 2 13b Chat。这个领先优势能保持吗？**亲自查看并判断吧**。

---

> 本文由AI自动翻译，原文链接：[How to run Mistral 7B with an API – Replicate blog](https://replicate.com/blog/run-mistral-7b-with-api)
> 
> 翻译时间：2026-04-16 04:59
