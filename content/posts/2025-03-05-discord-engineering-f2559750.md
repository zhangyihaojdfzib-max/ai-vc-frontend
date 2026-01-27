---
title: Discord移动端性能优化之路：从React Native迁移到启动时间减半
title_original: 'Supercharging Discord Mobile: Our Journey to a Faster App'
date: '2025-03-05'
source: Discord Engineering
source_url: https://discord.com/blog/supercharging-discord-mobile-our-journey-to-a-faster-app
author: ''
summary: 本文介绍了Discord移动客户端从React Native迁移到Android平台，并成功优化性能的历程。最初因性能顾虑未在Android上使用React
  Native，但随着设备性能提升和Hermes引擎的引入，团队于2022年完成迁移。尽管面临低端设备启动时间等挑战，但通过持续优化，在2023年将中位启动时间缩短了一半。文章还提到团队后续将聚焦于高级用户常用功能的深度优化。
categories:
- 技术趋势
tags:
- React Native
- 性能优化
- 移动开发
- Discord
- Hermes引擎
draft: false
translated_at: '2026-01-20T04:48:55.760662'
---

## Discord 与 React Native

Discord 的桌面端和移动客户端分别使用 React 和 React Native 构建。采用 React 使得我们的团队能够快速地在不同平台上发布功能，但由于容错空间较小，需要特别注意性能优化。

最初，出于对性能的担忧，我们在 Android 平台上回避使用 React Native。但近年来 Android 设备性能的提升，以及 React Native 新 JavaScript 引擎 Hermes 的引入，改变了这一局面。这促使我们在 2022 年将 Android 客户端迁移到了 React Native。

虽然这次转换带来了一些性能上的权衡（尤其是在低端设备上的启动时间），但我们通过努力，在 2023 年将中位启动时间缩短了一半，从而应对了这些挑战——我们将在后续文章中详细讲述这个故事。

最近，我们将注意力转向优化用户最常使用的功能，特别关注那些将 Discord 功能用到极致（有时甚至超出极限）的高级用户。如果你正在阅读本文，你很可能就是其中之一！

> 本文由AI自动翻译，原文链接：[Supercharging Discord Mobile: Our Journey to a Faster App](https://discord.com/blog/supercharging-discord-mobile-our-journey-to-a-faster-app)
> 
> 翻译时间：2026-01-20 04:48
