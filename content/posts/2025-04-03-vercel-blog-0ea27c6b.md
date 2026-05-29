---
title: Vercel Secure Compute 支持多环境网络隔离
title_original: Vercel Secure Compute now supports multiple environments - Vercel
date: '2025-04-03'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-secure-compute-now-supports-multiple-environments
author: ''
summary: Vercel 宣布其 Secure Compute 功能现已支持多环境配置，团队可在项目设置中为 Production、Preview 及自定义环境分别关联不同的安全网络。该更新简化了基于环境的网络隔离，用户可为每个环境选择活跃网络、可选备用网络以实现故障转移，并可将构建容器纳入网络。此举提升了云部署的安全性与灵活性，尤其适合需要精细网络控制的企业级应用。
categories:
- AI基础设施
tags:
- Vercel
- Secure Compute
- 网络隔离
- 多环境部署
- 云基础设施
draft: false
translated_at: '2026-05-29T06:13:24.787373'
---

![](/images/posts/dfd280afa38b.jpg)

![](/images/posts/2b5f942517e4.jpg)

使用 Vercel Secure Compute 的团队现在可以直接在项目设置中，将每个项目环境（Production、Preview 以及自定义环境）与不同的 Secure Compute 网络关联。这简化了单个项目内基于环境的网络隔离。

要将项目的环境连接到 Secure Compute：

1. 导航至项目的 Secure Compute 设置
2. 对于每个要连接到 Secure Compute 的环境：选择一个活跃网络；可选地，选择一个备用网络以启用故障转移；可选地，启用构建以将项目的构建容器纳入网络
3. 点击保存以持久化更改

导航至项目的 Secure Compute 设置

对于每个要连接到 Secure Compute 的环境：

- 选择一个活跃网络
- 可选地，选择一个备用网络以启用故障转移
- 可选地，启用构建以将项目的构建容器纳入网络

选择一个活跃网络

可选地，选择一个备用网络以启用故障转移

可选地，启用构建以将项目的构建容器纳入网络

点击保存以持久化更改

了解更多关于 Secure Compute 的信息。

---

> 本文由AI自动翻译，原文链接：[Vercel Secure Compute now supports multiple environments - Vercel](https://vercel.com/changelog/vercel-secure-compute-now-supports-multiple-environments)
> 
> 翻译时间：2026-05-29 06:13
