---
title: Vercel Edge Config更名为Global Config
title_original: Edge Config is now Global Config - Vercel
date: '2026-07-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/edge-config-is-now-global-config
author: ''
summary: Vercel将Edge Config更名为Global Config，以更好地体现其全球复制的数据存储特性，支持约1ms的读取速度，适用于功能开关、重定向等运行时配置。新名称伴随新SDK
  `@vercel/global-config` 和环境变量 `GLOBAL_CONFIG` 的推出，同时提升了各方案的存储限制（最高1MB）和写入次数，但定价不变。现有项目无需操作，主动升级安全且兼容旧版。
categories:
- AI基础设施
tags:
- Vercel
- Global Config
- Edge Config
- 数据存储
- 配置管理
draft: false
translated_at: '2026-07-30T05:02:18.066930'
---

Edge Config 现已更名为 Global Config。此次更名更好地体现了它是一个全球复制的数据存储，在每个区域可实现约 1ms 的读取速度，专为应用在运行时读取的配置而构建，例如功能开关、重定向和实验设置。

Global Config 存储现在在每个方案中最多可容纳 1 MB，Pro 和 Enterprise 团队可以创建无限数量的存储，且每日写入次数更多。此次更名还附带了一个新的服务端 SDK `@vercel/global-config` 和一个新的环境变量。

## 复制链接到标题 变更内容

- **名称**：Global Config 是 Edge Config 的新名称。存储本身未变。
- **包**：`@vercel/global-config` 作为直接替代品取代了 `@vercel/edge-config`。
- **环境变量**：将 Global Config 存储连接到项目会创建 `GLOBAL_CONFIG` 环境变量，而非 `EDGE_CONFIG`。
- **限制**：每个方案的限制均已提高。定价不变。

**名称**：Global Config 是 Edge Config 的新名称。存储本身未变。

**包**：`@vercel/global-config` 作为直接替代品取代了 `@vercel/edge-config`。

**环境变量**：将 Global Config 存储连接到项目会创建 `GLOBAL_CONFIG` 环境变量，而非 `EDGE_CONFIG`。

**限制**：每个方案的限制均已提高。定价不变。

## 复制链接到标题 你需要做什么

- **现有项目**：无需操作。部署、已连接的存储以及 `EDGE_CONFIG` 环境变量将继续正常工作。
- **主动升级是安全的**。新 SDK 默认读取 `GLOBAL_CONFIG`，并回退到 `EDGE_CONFIG`，因此它适用于更名前和更名后连接的存储。你可以在不触碰存储的情况下立即切换包。
- **创建存储和推送新的配置值无需升级即可工作**。这两者都不依赖于你的项目使用的 SDK 版本。
- **在将新存储连接到项目之前请先升级**。现在连接存储会创建 `GLOBAL_CONFIG` 环境变量，而旧版 SDK 默认只读取 `EDGE_CONFIG`。仍在使用 `@vercel/edge-config` 的项目无法读取新连接的存储。

**现有项目**：无需操作。部署、已连接的存储以及 `EDGE_CONFIG` 环境变量将继续正常工作。

**主动升级是安全的**。新 SDK 默认读取 `GLOBAL_CONFIG`，并回退到 `EDGE_CONFIG`，因此它适用于更名前和更名后连接的存储。你可以在不触碰存储的情况下立即切换包。

**创建存储和推送新的配置值无需升级即可工作**。这两者都不依赖于你的项目使用的 SDK 版本。

**在将新存储连接到项目之前请先升级**。现在连接存储会创建 `GLOBAL_CONFIG` 环境变量，而旧版 SDK 默认只读取 `EDGE_CONFIG`。仍在使用 `@vercel/edge-config` 的项目无法读取新连接的存储。

要升级，请安装新包并更新导入：

```
pnpm add @vercel/global-config
```

安装直接替代包

```
- import { get } from '@vercel/edge-config'+ import { get } from '@vercel/global-config'
```

将导入更新为新包

## 复制链接到标题 新限制

| 限制 | Hobby | Pro | Enterprise |
|------|-------|-----|------------|
| 存储数量 | 1（不变） | 无限（原为 3） | 无限（原为 10） |
| 写入次数 | 250/月（不变） | 100/小时（原为 480/天） | 自定义 |
| 存储大小 | 1 MB（原为 8 KB） | 1 MB（原为 64 KB） | 1 MB（原为 512 KB） |

定价不变，仍为每 1,000,000 次读取 3 美元，每 100 次写入 1 美元。

有关自定义设置和完整变更列表，请参阅 [Global Config 迁移指南](https://vercel.com/docs/storage/global-config/migration)。

## 贡献者

Pranav Kanchi, Chris Widmaier

---

> 本文由AI自动翻译，原文链接：[Edge Config is now Global Config - Vercel](https://vercel.com/changelog/edge-config-is-now-global-config)
> 
> 翻译时间：2026-07-30 05:02
