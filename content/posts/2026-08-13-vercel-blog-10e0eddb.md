---
title: Vercel AI SDK新增Grok Build支持，统一编码Agent接口
title_original: Grok Build is now available in the AI SDK harness layer - Vercel
date: '2026-08-13'
source: Vercel Blog
source_url: https://vercel.com/changelog/grok-build-harness-adapter
author: ''
summary: Vercel的AI SDK harness层新增对Grok Build的支持，允许开发者通过统一的HarnessAgent接口运行Grok Build编码Agent，无需修改应用代码即可切换运行时。该适配器基于ACP构建，目前支持的harness包括Claude
  Code、Codex、Deep Agents、Grok Build、OpenCode和Pi等。此举简化了多Agent集成的复杂性，提升了开发效率。
categories:
- AI基础设施
tags:
- AI SDK
- Grok Build
- 编码Agent
- Vercel
- Harness层
draft: false
translated_at: '2026-08-16T03:01:23.247262'
---

AI SDK 的 harness 层让您能够通过统一接口运行成熟的编码 Agent 运行时，从而无需更改应用程序代码即可切换运行时。今天，我们新增了对 Grok Build 的支持，它通过与其他所有受支持的 harness 相同的 `HarnessAgent` 接口运行。

`@ai-sdk/harness-grok-build` 是 Grok Build 的官方 harness 适配器，构建于 ACP harness 适配器（`@ai-sdk/harness-acp`）之上。

```
1import { HarnessAgent } from '@ai-sdk/harness/agent';2import { grokBuild } from '@ai-sdk/harness-grok-build';3
4const agent = new HarnessAgent({5  harness: grokBuild,6});
```

使用 HarnessAgent 与 Grok Build 的基本示例

阅读 Grok Build harness 文档以开始使用。

目前受支持的 harness 完整列表为：Claude Code、Codex、Deep Agents、Grok Build、OpenCode、Pi，更多即将推出。

---

> 本文由AI自动翻译，原文链接：[Grok Build is now available in the AI SDK harness layer - Vercel](https://vercel.com/changelog/grok-build-harness-adapter)
> 
> 翻译时间：2026-08-16 03:01
