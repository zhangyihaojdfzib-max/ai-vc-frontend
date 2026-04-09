---
title: 通过API运行Code Llama 70B代码生成模型
title_original: Run Code Llama 70B with an API – Replicate blog
date: '2024-01-30'
source: Replicate Blog
source_url: https://replicate.com/blog/run-codellama-with-an-api
author: ''
summary: 本文介绍了Meta最新发布的开源代码生成模型Code Llama 70B，该模型拥有700亿参数，在HumanEval基准测试中得分超越GPT-4。文章详细展示了如何通过Replicate平台，使用JavaScript、Python和cURL三种方式，仅用一行代码即可在云端调用这一高性能模型。同时说明了该模型的三种变体：基础版、Python专用版和指令微调版，为开发者提供了便捷的AI代码生成工具使用指南。
categories:
- AI产品
tags:
- Code Llama
- 代码生成
- 大语言模型
- Replicate
- AI开发工具
draft: false
translated_at: '2026-04-09T04:36:38.437106'
---

- Replicate
- 博客

# 通过 API 运行 Code Llama 70B

- cbh123

Code Llama 是一个基于 Llama 2 构建的代码生成模型。它可以用多种编程语言生成代码和关于代码的自然语言，包括 Python、JavaScript、TypeScript、C++、Java、PHP、C#、Bash 等。

今天，Meta 宣布推出一个更强大的新版本 Code Llama，拥有 700 亿参数。它是性能最高的开源模型之一。Meta 报告其在 HumanEval 上得分为 67.8，这超越了零样本 GPT-4。

通过 Replicate，您可以用一行代码在云端运行 Code Llama 70B。

## 目录

- 目录
- Code Llama 70B 变体
- 使用 JavaScript 运行 Code Llama 70B
- 使用 Python 运行 Code Llama 70B
- 使用 cURL 运行 Code Llama 70B
- 保持同步

## Code Llama 70B 变体

Code Llama 70B 有三种变体。本指南中的代码片段使用 `codellama-70b-instruct`，但所有三种变体都可在 Replicate 上使用：

- **Code Llama 70B Base** 是基础模型。
- **Code Llama 70B Python** 专门针对 Python 代码进行训练。
- **Code Llama 70B Instruct** 经过微调，用于理解自然语言指令。

## 使用 JavaScript 运行 Code Llama 70B

您可以使用我们的官方 JavaScript 客户端运行 Code Llama 70B：

```
npm install replicate
```

设置 `REPLICATE_API_TOKEN` 环境变量：

```
export REPLICATE_API_TOKEN=<your-api-token>
```

导入并设置客户端：

```
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});
```

使用 Replicate 的 API 运行 meta/codellama-70b-instruct：

```
const output = await replicate.run(
  "meta/codellama-70b-instruct:a279116fe47a0f65701a8817188601e2fe8f4b9e04a518789655ea7b995851bf",
  input: {
    prompt:"In Bash, how do I list all text files in the current directory (excluding subdirectories) that have been modified in the last month?",
  }
);
console.log(output);
```

要了解更多信息，请查看 Node.js 入门指南。

## 使用 Python 运行 Code Llama 70B

您可以使用我们的官方 Python 客户端运行 Code Llama 70B：

```
pip install replicate
```

```
export REPLICATE_API_TOKEN=<your-api-token>
```

```
import replicate

output = replicate.run(
    "meta/codellama-70b-instruct:a279116fe47a0f65701a8817188601e2fe8f4b9e04a518789655ea7b995851bf",
    input={
        "prompt": "In Bash, how do I list all text files in the current directory (excluding subdirectories) that have been modified in the last month?",
      }
)
print("".join(output))
```

要了解更多信息，请查看 Python 入门指南。

## 使用 cURL 运行 Code Llama 70B

您可以直接使用 cURL 等工具调用 HTTP API：

```
export REPLICATE_API_TOKEN=<your-api-token>
```

```
curl -s -X POST \
  -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Prefer: wait" \
  -d $'{
    "version": "a279116fe47a0f65701a8817188601e2fe8f4b9e04a518789655ea7b995851bf",
    "input": {
      "top_k": 10,
      "top_p": 0.95,
      "prompt": "In Bash, how do I list all text files in the current directory (excluding subdirectories) that have been modified in the last month?",
      "max_tokens": 500,
      "temperature": 0.8,
      "system_prompt": "",
      "repeat_penalty": 1.1,
      "presence_penalty": 0,
      "frequency_penalty": 0
    }
  }' \
  https://api.replicate.com/v1/predictions
```

要了解更多信息，请查看 Replicate 的 HTTP API 参考文档。

您也可以使用 Replicate 为 Go、Swift 等语言提供的其他客户端库来运行 Code Llama 70B。

## 保持同步

- 查看我们的 Code Llama 70B 模型页面
- 在 Twitter/X 上关注我们，获取 Replicate 的最新动态
- 加入我们的 Discord，讨论 Code Llama 70B

---

> 本文由AI自动翻译，原文链接：[Run Code Llama 70B with an API – Replicate blog](https://replicate.com/blog/run-codellama-with-an-api)
> 
> 翻译时间：2026-04-09 04:36
