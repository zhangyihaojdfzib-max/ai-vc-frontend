---
title: 为智能体引入Markdown：优化AI内容获取的新标准
title_original: Introducing Markdown for Agents
date: '2026-02-12'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/markdown-for-agents/
author: ''
summary: 本文介绍了Cloudflare推出的“为智能体提供Markdown”功能，旨在解决AI爬虫和智能体从非结构化HTML网页中提取信息的低效问题。文章指出，传统HTML页面包含大量无语义价值的标签，导致AI处理时消耗过多Token和计算资源。通过启用内容协商头，AI系统可直接请求Markdown格式内容，实现高达80%的Token节省，提升处理效率并降低成本。这一举措标志着网络内容开始将智能体视为一等公民，推动结构化数据分发的标准化。
categories:
- AI基础设施
tags:
- Markdown
- AI智能体
- 内容优化
- Cloudflare
- Token效率
draft: false
translated_at: '2026-02-13T04:30:02.888636'
---

# 为智能体引入Markdown

2026-02-12

- Celso Martinho
- Will Allen

![](/images/posts/45a6487262ca.png)

在线内容和业务的发现方式正在迅速改变。过去，流量主要来自传统搜索引擎，SEO决定了谁会被优先发现。如今，流量越来越多地来自AI爬虫和智能体，它们需要从为人类构建的、通常是非结构化的网络中获取结构化数据。

作为企业，为了持续保持领先，现在不仅要考虑人类访客或传统的SEO优化策略，更应该开始将智能体视为一等公民。

## 为什么Markdown很重要

将原始HTML喂给AI，就像按字数付费去读包装而不是里面的信件。在Markdown中，页面上的一个简单`## About Us`大约消耗3个Token；而其等效的HTML代码`<h2 class="section-title" id="about">About Us</h2>`则会消耗12-15个Token，这还没算上那些包裹每个真实网页、毫无语义价值的`<div>`包装器、导航栏和脚本标签。

您正在阅读的这篇博客文章，其HTML版本需要16,180个Token，而转换为Markdown后仅需3,150个Token。这减少了80%的Token使用量。

Markdown已迅速成为整个智能体和AI系统的通用语言。这种格式的明确结构使其非常适合AI处理，最终能带来更好的结果，同时最大限度地减少Token浪费。

问题在于，网络是由HTML构成的，而不是Markdown，而且页面体积多年来一直在稳步增长，使得页面难以解析。对于智能体来说，它们的目标是过滤掉所有非必要元素，并扫描相关内容。

将HTML转换为Markdown现在已成为任何AI流程的常见步骤。然而，这个过程远非理想：它浪费计算资源，增加成本和处理复杂性，最重要的是，这可能并非内容创作者最初希望其内容被使用的方式。

如果AI智能体能够绕过意图分析和文档转换的复杂性，直接从源头接收结构化的Markdown，那会怎样？

## 自动将HTML转换为Markdown

Cloudflare的网络现在支持在源头进行实时内容转换，适用于启用了内容协商头的区域。现在，当AI系统从任何使用Cloudflare并启用了"为智能体提供Markdown"功能的网站请求页面时，它们可以在请求中表达对`text/markdown`的偏好。我们的网络将尽可能自动、高效地将HTML即时转换为Markdown。

以下是其工作原理。要从启用了"为智能体提供Markdown"功能的区域获取任何页面的Markdown版本，客户端需要在请求中添加`Accept`协商头，并将`text/markdown`作为选项之一。Cloudflare会检测到此请求，从源站获取原始HTML版本，并在将其提供给客户端之前将其转换为Markdown。

这是一个使用`Accept`协商头从我们的开发者文档请求页面的curl示例：

```typescript
curl https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/ \
  -H "Accept: text/markdown"

```

或者，如果您正在使用Workers构建AI智能体，可以使用TypeScript：

```javascript
const r = await fetch(
  `https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents/`,
  {
    headers: {
      Accept: "text/markdown, text/html",
    },
  },
);
const tokenCount = r.headers.get("x-markdown-tokens");
const markdown = await r.text();

```

我们已经看到当今一些最流行的编码智能体——如Claude Code和OpenCode——在请求内容时发送这些Accept头。现在，对此请求的响应将以Markdown格式返回。就这么简单。

```typescript
HTTP/2 200
date: Wed, 11 Feb 2026 11:44:48 GMT
content-type: text/markdown; charset=utf-8
content-length: 2899
vary: accept
x-markdown-tokens: 725
content-signal: ai-train=yes, search=yes, ai-input=yes

---
title: Markdown for Agents · Cloudflare Agents docs
---

## What is Markdown for Agents

The ability to parse and convert HTML to Markdown has become foundational for AI.
...

```

请注意，我们在转换后的响应中包含了一个`x-markdown-tokens`头，它指示了Markdown文档中估计的Token数量。您可以在您的流程中使用这个值，例如计算上下文窗口的大小或决定分块策略。

以下是其工作原理的示意图：

### 内容信号策略

在我们上一个生日周期间，Cloudflare宣布了内容信号——一个允许任何人在其内容被访问后表达对其使用方式的偏好的框架。

当您返回Markdown时，您希望确保您的内容正在被智能体或AI爬虫使用。这就是为什么"为智能体提供Markdown"转换后的响应包含`Content-Signal: ai-train=yes, search=yes, ai-input=yes`头，表示该内容可用于AI训练、搜索结果和AI输入（包括智能体使用）。"为智能体提供Markdown"功能未来将提供定义自定义内容信号策略的选项。

请查看我们专门的内容信号页面以获取有关此框架的更多信息。

### 在Cloudflare博客和开发者文档中试用

我们已在我们的开发者文档和博客中启用了此功能，邀请所有AI爬虫和智能体使用Markdown而非HTML来消费我们的内容。

现在就可以通过使用`Accept: text/markdown`请求此博客来试用。

```typescript
curl https://blog.cloudflare.com/markdown-for-agents/ \
  -H "Accept: text/markdown"
```

结果是：

```typescript
---
description: The way content is discovered online is shifting, from traditional search engines to AI agents that need structured data from a Web built for humans. Itâs time to consider not just human visitors, but start to treat agents as first-class citizens. Markdown for Agents automatically converts any HTML page requested from our network to markdown.
title: Introducing Markdown for Agents
image: https://blog.cloudflare.com/images/markdown-for-agents.png
---

# Introducing Markdown for Agents

The way content and businesses are discovered online is changing rapidly. In the past, traffic originated from traditional search engines and SEO determined who got found first. Now the traffic is increasingly coming from AI crawlers and agents that demand structured data within the often-unstructured Web that was built for humans.

...
```

### 转换为Markdown的其他方式

如果您正在构建需要从Cloudflare外部进行任意文档转换的AI系统，或者内容源不提供"为智能体提供Markdown"功能，我们为您的应用程序提供了其他将文档转换为Markdown的方式：

- Workers AI的`AI.toMarkdown()`支持多种文档类型（不仅仅是HTML）以及摘要生成。
- 浏览器渲染的`/markdown` REST API支持Markdown转换，如果您需要在真实浏览器中渲染动态页面或应用程序后再进行转换。

Workers AI的`AI.toMarkdown()`支持多种文档类型（不仅仅是HTML）以及摘要生成。

浏览器渲染的`/markdown` REST API支持Markdown转换，如果您需要在真实浏览器中渲染动态页面或应用程序后再进行转换。

## 跟踪Markdown使用情况

预计到AI系统浏览网络的方式将发生转变，Cloudflare Radar现在包含了针对AI机器人和爬虫流量的内容类型洞察，既在AI洞察页面上提供全球数据，也在单个机器人信息页面中提供。

新的`content_type`维度和过滤器显示了返回给AI智能体和爬虫的内容类型分布，按MIME类型类别分组。

您还可以查看特定智能体或爬虫过滤后的Markdown请求。以下是返回给OAI-Searchbot（OpenAI用于驱动ChatGPT搜索的爬虫）的Markdown请求：

这些新数据将使我们能够追踪AI机器人、爬虫和Agent（智能体）随时间推移如何消费网络内容的演变过程。与往常一样，Radar上的所有数据均可通过公开API和数据浏览器免费访问。

## 立即开始使用

要为您的区域启用Agent（智能体）Markdown功能，请登录Cloudflare仪表板，选择您的账户，选择区域，找到"快速操作"并切换"Agent（智能体）Markdown"按钮以启用。该功能今日起以Beta版本免费提供给Pro、Business和Enterprise套餐用户，以及SSL for SaaS客户。

您可以在我们的开发者文档中找到关于Agent（智能体）Markdown的更多信息。我们欢迎您提供反馈，以帮助我们持续完善和增强此功能。我们期待观察AI爬虫和Agent（智能体）如何随着网络发展，适应并驾驭其非结构化的特性。

---

> 本文由AI自动翻译，原文链接：[Introducing Markdown for Agents](https://blog.cloudflare.com/markdown-for-agents/)
> 
> 翻译时间：2026-02-13 04:30
