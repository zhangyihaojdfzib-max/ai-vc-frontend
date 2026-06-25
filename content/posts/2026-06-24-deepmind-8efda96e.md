---
title: Gemini 3.5 Flash内置计算机使用功能
title_original: Introducing computer use in Gemini 3.5 Flash
date: '2026-06-24'
source: Google DeepMind
source_url: https://deepmind.google/blog/introducing-computer-use-in-gemini-3-5-flash/
author: ''
summary: Google在Gemini 3.5 Flash中原生集成了计算机使用功能，使开发者能够构建跨浏览器、移动和桌面环境的智能体。该功能此前仅作为独立模型提供，现已成为内置工具，在OSWorld等基准测试中表现优异。文章还介绍了针对提示词注入的定向对抗训练、企业级安全防护系统，以及来自Browserbase、Browser
  Use和UIPath等客户的正面反馈。开发者可通过Gemini API和Enterprise Agent Platform开始使用。
categories:
- AI产品
tags:
- Gemini 3.5 Flash
- 计算机使用
- 智能体
- Google AI
- 企业自动化
draft: false
translated_at: '2026-06-25T06:05:44.779083'
---

# 在 Gemini 3.5 Flash 中引入计算机使用功能

2026年6月24日

计算机使用现已成为 Gemini 3.5 Flash 的内置工具，用于构建能够跨平台交互的 Agent（智能体）。

您的浏览器不支持音频元素。

计算机使用现已成为 Gemini 3.5 Flash 支持的内置工具，为 Agent（智能体）计算机使用任务提供了我们迄今为止最佳的性能。此前仅作为独立的 Gemini 2.5 计算机使用模型提供，计算机使用功能现已原生集成到主要的 Gemini Flash 模型中。Gemini 已经在函数调用以及使用搜索和地图等内置工具方面表现出色。借助内置的计算机使用能力，开发者现在可以使用 3.5 Flash 可靠地构建能够跨浏览器、移动和桌面环境进行观察、推理和采取行动的定制 Agent（智能体）。这为长期和企业自动化任务（如持续软件测试和跨专业应用的知识工作）解锁了改进的性能。

![Gemini 3.5 基准测试](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5__benchmark-OSWorld-Ver.width-100.format-webp.webp)

开发者和企业可以通过 Gemini API 和 Gemini Enterprise Agent Platform 开始在 3.5 Flash 中使用计算机使用功能。

3.5 Flash 使用计算机使用功能分析 Gemini 应用并返回分类后的功能列表。

具备计算机使用功能的 3.5 Flash 对其自身文档进行无障碍性审计。

## 确保 3.5 Flash 中计算机使用功能的安全性

为了降低在实时环境中运行的 Agent（智能体）面临的某些提示词注入风险，我们在 Gemini 3.5 Flash 中针对计算机使用功能采用了定向对抗训练。我们还发布了两个可选的企业级安全防护系统，使企业能够：

- 对敏感或不可逆的操作要求明确的用户确认。
- 在检测到间接提示词注入时自动停止任务。

采用"纵深防御"的方法，我们鼓励开发者将这些功能与安全沙箱、人工参与验证和严格的访问控制相结合。有关安全措施的更多信息，请参阅我们的最佳实践文档。

我们已经看到客户通过计算机使用功能获得价值。以下是一些客户的声音：

![来自 Browserbase 的 Migual Gonzalez Fernandez 的引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gemini_3.5_Flash_BrowserBase_v2.width-100.format-webp.webp)

![来自 Browser Use CEO Magnus Muller 的引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gemini_3.5_Flash_Browser_Use_1.width-100.format-webp.webp)

![来自 UIPath 高级总监 Alvin Stanescu 的引述](/images/posts/74ca9cdbfe0f.webp)

立即开始使用计算机功能进行构建：

- 立即尝试：在 Browserbase 托管的演示环境中测试各项能力。
- 开始构建：通过 Gemini API 和 Gemini Enterprise Agent Platform 深入了解我们的参考实现和文档。

![](https://deepmind.google/static/blogv2/images/newsletter-envelope-back.svg?version=pr20260624-1707)

![](https://deepmind.google/static/blogv2/images/newsletter-envelope-letter-approved.svg?version=pr20260624-1707)

![](https://deepmind.google/static/blogv2/images/newsletter-envelope-letter-google.svg?version=pr20260624-1707)

![](https://deepmind.google/static/blogv2/images/newsletter-envelope-front.svg?version=pr20260624-1707)

## 在收件箱中获取更多来自 Google 的故事。在收件箱中获取更多来自 Google 的故事。

您的信息将按照 Google 的隐私政策使用。

完成。只需再一步。

检查您的收件箱以确认订阅。

您已订阅我们的新闻通讯。

您也可以使用不同的电子邮件地址订阅。

---

> 本文由AI自动翻译，原文链接：[Introducing computer use in Gemini 3.5 Flash](https://deepmind.google/blog/introducing-computer-use-in-gemini-3-5-flash/)
> 
> 翻译时间：2026-06-25 06:05
