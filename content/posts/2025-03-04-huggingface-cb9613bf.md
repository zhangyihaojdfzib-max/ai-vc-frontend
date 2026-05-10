---
title: Hugging Face与JFrog合作提升AI安全透明度
title_original: Hugging Face and JFrog partner to make AI Security more transparent
date: '2025-03-04'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/jfrog
author: ''
summary: Hugging Face宣布与软件供应链平台JFrog合作，将JFrog的扫描器集成到Hugging Face Hub中，以提升AI模型共享的安全性。JFrog的扫描器能解析并分析模型权重中的代码，检测潜在恶意用途，减少误报。所有公共模型仓库将自动被扫描，无需用户操作。此举旨在为机器学习社区提供更安全可靠的平台，推动模型共享领域的发展。
categories:
- AI基础设施
tags:
- Hugging Face
- JFrog
- AI安全
- 模型扫描
- 供应链安全
draft: false
translated_at: '2026-05-10T05:36:16.863114'
---

# Hugging Face 与 JFrog 合作，提升 AI 安全性透明度

我们很高兴宣布与 JFrog（JFrog 软件供应链平台的创建者）达成合作，这是我们长期致力于为机器学习社区提供安全可靠平台的一部分。

我们决定将 JFrog 的扫描器集成到我们的平台中，以持续提升 Hugging Face Hub 的安全性。JFrog 的扫描器带来了新的扫描功能，旨在减少 Hub 上的误报。实际上，我们目前观察到，模型权重可能包含在反序列化时执行的代码，有时还会在推理时执行，具体取决于格式。这类代码通常对开发者来说是无害的实用功能。由于我们的 picklescan 扫描器仅对模块名称进行模式匹配，我们无法始终确认某个函数或模块的使用是否具有恶意。JFrog 则更进一步，它会解析并分析模型权重中的代码，以检查是否存在潜在的恶意用途。

有兴趣加入我们的安全合作 / 在 Hub 上提供扫描信息吗？请通过 security@huggingface.co 与我们联系。

![](/images/posts/259c2430e765.png)

## 模型安全回顾

为了共享模型，我们对权重、配置以及用于与模型交互的其他数据结构进行序列化，以便于存储和传输。某些序列化格式容易受到恶意攻击，例如任意代码执行（说的就是你，pickle），这使得使用这些格式的共享模型可能存在危险。

由于 Hugging Face 已成为流行的模型共享平台，我们希望帮助社区免受此类威胁，因此我们开发了像 picklescan 这样的工具，并将 JFrog 集成到我们的扫描工具套件中。

Pickle 并非唯一可被利用的格式，请参考如何利用 Keras Lambda 层实现任意代码执行。好消息是，JFrog 能够捕获这两种攻击，并在更多文件格式中检测其他威胁——请参阅他们的模型威胁页面以获取最新的扫描信息。

在此阅读我们关于安全性的全部文档：https://huggingface.co/docs/hub/security🔥

## 集成

您无需进行任何操作即可受益！所有公共模型仓库将在您将文件推送到 Hub 时自动由 JFrog 扫描。以下是一个示例仓库，您可以查看该功能的实际效果：mcpotato/42-eicar-street。

![](/images/posts/ab61ec2a39b5.png)

请注意，您可能暂时看不到自己模型的扫描结果，因为我们拥有数百万个模型仓库。可能需要一些时间才能完成全部扫描 😅。

总体而言，我们已经扫描了数亿个文件，因为我们相信，赋能社区以安全且无障碍的方式共享模型，将推动整个领域的发展。

---

> 本文由AI自动翻译，原文链接：[Hugging Face and JFrog partner to make AI Security more transparent](https://huggingface.co/blog/jfrog)
> 
> 翻译时间：2026-05-10 05:36
