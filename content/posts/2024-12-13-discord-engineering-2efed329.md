---
title: Discord如何为千万用户无缝升级至64位架构
title_original: How Discord Seamlessly Upgraded Millions of Users to 64-Bit Architecture
date: '2024-12-13'
source: Discord Engineering
source_url: https://discord.com/blog/how-discord-seamlessly-upgraded-millions-of-users-to-64-bit-architecture
author: ''
summary: 本文阐述了Discord从32位架构向64位架构升级的背景与决策过程。最初选择32位架构是为了实现广泛的兼容性，但随着技术发展，其内存限制和未来维护风险日益凸显。文章分析了32位应用在性能、内存使用上的局限性，并指出依赖的底层库（如Electron、WebRTC）已转向64位优先，长期停留在32位将面临优化不足和潜在错误。这为后续描述大规模无缝升级的技术方案奠定了基础。
categories:
- 技术趋势
tags:
- 架构升级
- 性能优化
- Electron
- 向后兼容
- 软件工程
draft: false
translated_at: '2026-01-22T05:04:28.780086'
---

## 32位架构的深远影响

如果你点开了这篇博文，很可能已经知道 Discord 是一款用于游戏时交流、娱乐和社交的桌面应用程序。但你是否了解，Discord 在 2015 年首次发布时，仅仅是一个网页应用？

从网页应用起步，让我们能够为用户提供一种通过浏览器便捷性与朋友聊天的方式。然而，为了提供我们期望的用户体验，我们需要跳出浏览器，进军桌面平台。通过使用名为 Electron 的网页封装技术，我们可以在类似浏览器的环境中运行 Discord，同时能够访问所有额外的底层功能，从而实现诸如游戏内覆盖等特性。当我们为 Windows 构建第一个可执行文件时，必须决定是面向 32 位还是 64 位处理器。选择 32 位架构，得益于微软的向后兼容层，可以做到一次编写，几乎随处运行。这对于应用程序的第一个版本来说是合理的——它能在 32 位和 64 位机器上运行，同时只需要维护一个版本的应用。

在性能方面，32 位应用比 64 位应用占用更少的内存，但有时这反而成为缺点：32 位应用对内存使用有严格的限制，而这正是 64 位架构旨在解决的问题。虽然在 64 位机器上以 32 位应用运行能为 Discord 提供额外的内存，但我们偶尔仍会触及内存上限，导致错误甚至崩溃。

Discord 是使用众多库构建的，例如 Electron 和 WebRTC，它们共同帮助我们为您提供理想的桌面 Discord 体验。这些工具支持 64 位构建已有多年，事实上，它们现在默认采用 64 位架构。随着 64 位在越来越多的机器上成为标准，我们预计 64 位架构将获得比 32 位架构多得多的优化和错误修复。如果 Discord 在可预见的未来继续停留在 32 位架构，我们可能会让自己——进而让我们的用户——暴露于新的错误和低效问题之中，这些问题仅仅因为维护 32 位库的人员不足而无法被发现和解决。

> 本文由AI自动翻译，原文链接：[How Discord Seamlessly Upgraded Millions of Users to 64-Bit Architecture](https://discord.com/blog/how-discord-seamlessly-upgraded-millions-of-users-to-64-bit-architecture)
> 
> 翻译时间：2026-01-22 05:04
