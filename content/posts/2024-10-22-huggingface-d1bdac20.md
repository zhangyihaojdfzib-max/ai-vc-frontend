---
title: Hugging Face联手Protect AI，强化模型安全
title_original: 'Hugging Face Teams Up with Protect AI: Enhancing Model Security for
  the ML Community'
date: '2024-10-22'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/protectai
author: ''
summary: Hugging Face宣布与Protect AI合作，以提升机器学习社区模型共享的安全性。文章指出，模型序列化格式（如pickle）易受恶意攻击，而Protect
  AI的Guardian工具可检测多种文件格式的威胁。集成后，所有公共模型仓库将在推送时自动由Guardian扫描，用户无需额外操作。Hugging Face已扫描数亿文件，致力于在保障安全的前提下推动模型共享与AI发展。
categories:
- AI基础设施
tags:
- Hugging Face
- 模型安全
- Protect AI
- Guardian
- 开源安全
draft: false
translated_at: '2026-06-13T06:19:25.861299'
---

# Hugging Face 与 Protect AI 合作：增强机器学习社区的模型安全性

我们很高兴宣布与 Protect AI 建立合作伙伴关系，这是我们为机器学习社区提供安全可靠平台的长期承诺的一部分。

Protect AI 是一家以创建更安全的 AI 驱动世界为使命而成立的公司。他们正在开发强大的工具，即 Guardian，以确保 AI 创新的快速发展能够在不牺牲安全性的前提下持续进行。

我们决定与 Protect AI 合作，源于他们以社区为导向的安全方法、对开源技术的积极支持，以及在安全与 AI 交叉领域的专业知识。

有兴趣加入我们的安全合作伙伴关系/在 Hub 上提供扫描信息吗？请通过 security@huggingface.co 与我们联系。

## 模型安全概述

为了共享模型，我们对权重、配置以及用于与模型交互的其他数据结构进行序列化，以方便存储和传输。某些序列化格式容易受到恶意攻击，例如任意代码执行（说的就是你，pickle），这使得使用这些格式的共享模型存在潜在危险。

由于 Hugging Face 已成为流行的模型共享平台，我们希望帮助社区免受此类威胁，因此我们开发了 picklescan 等工具，并将 Guardian 集成到我们的扫描工具套件中。

Pickle 并不是唯一可利用的格式，请参考如何利用 Keras Lambda 层实现任意代码执行。好消息是，Guardian 能够捕获这两种攻击以及更多其他文件格式的攻击——请参阅他们的知识库获取最新的扫描器信息。

在此阅读我们关于安全性的所有文档：https://huggingface.co/docs/hub/security🔥

## 集成

在将 Guardian 作为第三方扫描器集成时，我们借此机会重新设计了前端以显示扫描结果。现在的界面如下所示：

![](/images/posts/74f0daa74f02.png)

![](/images/posts/208d775a90b7.png)

从截图中可以看出，您无需进行任何操作即可受益！所有公共模型仓库都将在您将文件推送到 Hub 时自动由 Guardian 进行扫描。以下是一个示例仓库，您可以查看该功能的实际效果：mcpotato/42-eicar-street。

请注意，您可能今天还看不到模型的扫描结果，因为我们有超过 100 万个模型仓库。我们可能需要一些时间来赶上进度😅。

总的来说，我们已经扫描了数亿个文件，因为我们相信，让社区能够以安全且无障碍的方式共享模型，将推动整个领域的发展。

---

> 本文由AI自动翻译，原文链接：[Hugging Face Teams Up with Protect AI: Enhancing Model Security for the ML Community](https://huggingface.co/blog/protectai)
> 
> 翻译时间：2026-06-13 06:19
