---
title: Vercel Flags 新增 JSON 值支持，简化功能标志管理
title_original: Vercel Flags now supports JSON values - Vercel
date: '2026-05-07'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-flags-now-supports-json-values
author: ''
summary: Vercel Flags 现已支持存储 JSON 值，在原有布尔值、字符串和数值的基础上扩展了数据类型。这一更新允许开发者将多个相关的功能标志合并为单个标志，例如通过一个
  JSON 对象统一管理 AI 模型的 ID、温度、最大 token 数等参数，从而简化 A/B 测试、流量路由和模型切换等场景的配置。此举提升了功能标志的灵活性和可维护性，尤其适用于需要精细控制多个参数的应用场景。
categories:
- AI基础设施
tags:
- Vercel
- 功能标志
- A/B测试
- JSON
- 基础设施
draft: false
translated_at: '2026-05-08T04:53:35.441087'
---

你现在可以在Vercel Flags中存储JSON值，这扩展了原有的对布尔值、字符串和数值的支持。这使得你可以将原本需要多个相关标志（flag）管理的内容，合并到单个功能标志中。

例如，为了对不同模型的表现进行A/B测试，你现在可以定义一个单独的`model`标志。这样，你只需管理一个提供完整对象的标志，而无需分别管理`ai_model`、`ai_temperature`和`ai_max_tokens`：

```
12{3  "id": "claude-sonnet-4-6",4  "temperature": 0.7, 5  "maxTokens": 1024,6  "systemPrompt": "You are a helpful shopping assistant."7}8
910{11  "id": "claude-opus-4-6",12  "temperature": 0.8, 13  "maxTokens": 2048,14  "systemPrompt": "You help with shopping."15}
```

一个在其变体中包含JSON配置的功能标志

使用Vercel Flags逐步将流量路由到新模型、进行A/B测试，或在某个供应商出现问题时快速切换模型。

立即尝试或了解更多关于Vercel Flags的信息。

---

> 本文由AI自动翻译，原文链接：[Vercel Flags now supports JSON values - Vercel](https://vercel.com/changelog/vercel-flags-now-supports-json-values)
> 
> 翻译时间：2026-05-08 04:53
