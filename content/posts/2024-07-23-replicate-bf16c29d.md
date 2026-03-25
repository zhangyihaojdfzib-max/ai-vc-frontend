---
title: 通过Replicate API运行Meta Llama 3.1 405B大模型
title_original: Run Meta Llama 3.1 405B with an API – Replicate blog
date: '2024-07-23'
source: Replicate Blog
source_url: https://replicate.com/blog/run-llama-3-1-with-an-api
author: ''
summary: 本文介绍了如何在Replicate平台上通过API运行Meta最新发布的Llama 3.1 405B大语言模型。文章详细说明了该模型拥有4050亿参数、8000个Token上下文窗口，并提供了三种使用方式：在API游乐场交互体验、使用JavaScript客户端、Python客户端以及直接通过cURL调用HTTP
  API。文中包含具体的代码示例和环境配置步骤，帮助开发者快速上手这一性能媲美GPT-4的先进模型。
categories:
- AI基础设施
tags:
- Llama 3.1
- 大语言模型
- Replicate
- API调用
- AI开发
draft: false
translated_at: '2026-03-25T04:40:04.050276'
---

- Replicate
- 博客

# 通过 API 运行 Meta Llama 3.1 405B

- deepfates

Llama 3.1 是 Meta 发布的最新语言模型。它拥有高达 4050 亿参数的庞大模型，在质量上可与 GPT-4 媲美，并具备 8000 个 Token 的上下文窗口。

通过 Replicate，您只需一行代码即可在云端运行 Llama 3.1。

## 在我们的 API 游乐场中尝试 Llama 3.1

在深入使用之前，您可以在我们的 API 游乐场中先体验一下 Llama 3.1。

尝试调整提示词，看看 Llama 3.1 如何回应。Replicate 上的大多数模型都提供类似的交互式 API 游乐场，您可以在模型页面找到它：https://replicate.com/meta/meta-llama-3.1-405b-instruct

API 游乐场是了解模型功能的好方法，它提供了多种语言的可复制代码片段，帮助您快速上手。

## 使用 JavaScript 运行 Llama 3.1

您可以使用我们的官方 JavaScript 客户端运行 Llama 3.1：

安装 Replicate 的 Node.js 客户端库

```
npm install replicate
```

设置 `REPLICATE_API_TOKEN` 环境变量

```
export REPLICATE_API_TOKEN=r8_9wm**********************************
```

（您可以在账户中生成 API 令牌。请妥善保管。）

导入并设置客户端

```
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});
```

使用 Replicate 的 API 运行 meta/meta-llama-3.1-405b-instruct。请查看模型架构以了解输入和输出的概览。

```
const input = {
  prompt: "Although you can hear and feel me but not see or smell me, everybody has a taste for me. I can be learned once, but only remembered after that. What exactly am I?"
};

for await (const event of replicate.stream("meta/meta-llama-3.1-405b-instruct", { input })) {
  process.stdout.write(event.toString());
};
```

要了解更多信息，请查看 Node.js 入门指南。

## 使用 Python 运行 Llama 3.1

您可以使用我们的官方 Python 客户端运行 Llama 3.1：

安装 Replicate 的 Python 客户端库

```
pip install replicate
```

```
export REPLICATE_API_TOKEN=r8_9wm**********************************
```

导入客户端

```
import replicate
```

```
# meta/meta-llama-3.1-405b-instruct 模型可以在运行时流式输出。
for event in replicate.stream(
    "meta/meta-llama-3.1-405b-instruct",
    input={
        "prompt": "Although you can hear and feel me but not see or smell me, everybody has a taste for me. I can be learned once, but only remembered after that. What exactly am I?"
    },
):
    print(str(event), end="")
```

要了解更多信息，请查看 Python 入门指南。

## 使用 cURL 运行 Llama 3.1

您也可以直接使用 cURL 等工具调用 HTTP API：

```
export REPLICATE_API_TOKEN=r8_9wm**********************************
```

```
curl -s -X POST\
  -H "Authorization: Bearer $REPLICATE_API_TOKEN"\
  -H "Content-Type: application/json"\
  -H "Prefer: wait"\
  -d $'{
    "input": {
      "prompt": "Although you can hear and feel me but not see or smell me, everybody has a taste for me. I can be learned once, but only remembered after that. What exactly am I?"
    }
  }'\
  https://api.replicate.com/v1/models/meta/meta-llama-3.1-405b-instruct/predictions
```

要了解更多信息，请查看 Replicate 的 HTTP API 参考文档。

您也可以使用 Replicate 提供的其他客户端库（如 Go、Swift 等）来运行 Llama。

## 关于 Llama 3.1 405B

Llama 3.1 405B 是目前 Replicate 上唯一可用的变体。该模型代表了开源语言模型的前沿水平：

- **4050 亿参数**：如此庞大的模型规模为开源模型带来了前所未有的能力。
- **指令微调**：针对聊天和遵循指令的任务进行了优化。
- **GPT-4 级别的质量**：在许多基准测试中，Llama 3.1 405B 接近或达到了 GPT-4 的性能水平。
- **多语言支持**：支持 8 种语言的训练，包括英语、德语、法语、意大利语、葡萄牙语、印地语、西班牙语和泰语。
- **广泛的训练**：基于超过 15 万亿 Token 的数据进行训练。

## 负责任的人工智能与安全

Llama 3.1 非常注重负责任的人工智能开发。Meta 引入了多种工具和资源，帮助开发者安全、合乎道德地使用该模型：

- **Purple Llama**：一个开源项目，包含用于生成式 AI 模型的安全工具和评估。
- **Llama Guard 3**：一个更新的输入/输出安全模型。
- **Code Shield**：一个帮助防止生成不安全代码的工具。
- **负责任使用指南**：模型伦理使用的指导原则。

我们建议在使用 Llama 3.1 构建应用程序时查阅这些资源。更多信息，请查看 Purple Llama GitHub 仓库。

## 示例聊天应用

如果您想找一个起点，我们已经在 Next.js 中构建了一个演示聊天应用，可以部署在 Vercel 上：

![Llama 聊天](/images/posts/da585df886e8.webp)

您可以在 llama3.replicate.dev 上试用。查看 GitHub README 以了解如何自定义和部署它。

## 保持同步

- 在 Twitter/X 上关注我们，获取 Llamaverse 的最新动态。
- 加入我们的 Discord，一起讨论 Llama。

祝您探索愉快！🦙

---

> 本文由AI自动翻译，原文链接：[Run Meta Llama 3.1 405B with an API – Replicate blog](https://replicate.com/blog/run-llama-3-1-with-an-api)
> 
> 翻译时间：2026-03-25 04:40
