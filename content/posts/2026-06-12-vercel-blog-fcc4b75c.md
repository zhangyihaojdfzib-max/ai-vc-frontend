---
title: AI SDK 7引入HarnessAgent：统一多Agent框架切换
title_original: Program Claude Code, Codex, Pi and other agent harnesses with AI SDK
  - Vercel
date: '2026-06-12'
source: Vercel Blog
source_url: https://vercel.com/changelog/program-agent-harnesses-with-ai-sdk
author: ''
summary: Vercel在AI SDK 7中推出实验性HarnessAgent，提供统一API来运行Claude Code、Codex、Pi等成熟Agent框架。开发者无需重写Agent代码即可在不同框架间切换，并保持相同的沙箱、工具和技能配置。该抽象层规范化了对框架特有能力（如会话管理、权限流程、子Agent等）的访问，支持generate和stream方法，兼容现有AI
  SDK应用。目前为实验性版本，未来将支持更多框架适配器。
categories:
- AI基础设施
tags:
- AI SDK
- HarnessAgent
- Agent框架
- Vercel
- 模型切换
draft: false
translated_at: '2026-06-13T06:20:24.987271'
---

AI SDK 7 引入了 HarnessAgent，这是一个用于运行成熟 Agent 框架（包括 Claude Code、Codex 和 Pi）的统一 API。AI SDK 一直允许你在不重写 Agent 的情况下切换模型。现在，你可以用同样的方式切换框架。

一次编写 Agent。使用当下可用的最佳框架。今天。三个月后。一年后。

框架管理模型调用之上的组件，包括技能、沙箱、会话、权限流程、压缩、运行时配置和子 Agent。AI SDK 通过统一的框架抽象层，规范化对这些能力的访问。

本次实验性版本的初始框架适配器包括 Claude Code、Codex 和 Pi，更多适配器即将推出。

```javascript
1import { HarnessAgent } from '@ai-sdk/harness/agent';
2import { claudeCode } from '@ai-sdk/harness-claude-code';
3import { createVercelSandbox } from '@ai-sdk/sandbox-vercel';
4
5const agent = new HarnessAgent({
6  harness: claudeCode,
7  sandbox: createVercelSandbox({
8    runtime: 'node24',
9    ports: [4000],
10  }),
11  tools: { },
12  skills: [ ],
13});
14
15const session = await agent.createSession();
16
17try {
18  const result = await agent.stream({
19    session,
20    prompt: '检查测试失败原因并修复生产代码。',
21  });
22
23  for await (const part of result.fullStream) {
24    if (part.type === 'text-delta') {
25      process.stdout.write(part.text);
26    }
27  }
28} finally {
29  await session.destroy();
30}
```

使用 Claude Code 创建一个基于框架的 Agent

将 `claudeCode` 替换为 `codex` 或 `pi`，并保持相同的 `HarnessAgent` 流程。每个框架都在沙箱化工作区中运行 Agent，确保宿主环境安全。

`HarnessAgent.generate()` 和 `HarnessAgent.stream()` 都返回兼容 AI SDK 的结果。如果你的应用已使用 `useChat` 或相关 AI SDK 工具，你可以在不更改用户界面代码的情况下替换为 `HarnessAgent`。

`HarnessAgent` 已在 AI SDK canary 版本中可用。阅读 AI SDK 框架文档以开始使用。

Harness 包为实验性版本。随着这个早期 API 的进一步完善，各版本之间可能会出现破坏性变更。

---

> 本文由AI自动翻译，原文链接：[Program Claude Code, Codex, Pi and other agent harnesses with AI SDK - Vercel](https://vercel.com/changelog/program-agent-harnesses-with-ai-sdk)
> 
> 翻译时间：2026-06-13 06:20
