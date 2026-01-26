---
title: MiniMax M2.1模型正式登陆Vercel AI网关
title_original: MiniMax M2.1 now live on Vercel AI Gateway - Vercel
date: '2025-12-22'
source: Vercel Blog
source_url: https://vercel.com/changelog/minimax-m2-1-now-live-on-vercel-ai-gateway
author: Authors
summary: Vercel宣布其AI网关现已支持MiniMax的最新模型M2.1。该模型相比前代M2速度更快，在代码生成、工具调用和多步骤复杂任务方面表现显著提升，尤其擅长多种编程语言及代码重构、错误修复等场景。开发者可通过Vercel
  AI SDK直接调用，利用网关的统一API进行成本追踪、性能优化和故障转移。AI网关还提供模型使用量排行榜，帮助用户了解主流模型趋势。
categories:
- AI基础设施
tags:
- MiniMax
- Vercel
- AI网关
- 大模型
- 代码生成
draft: false
translated_at: '2026-01-05T17:27:25.321Z'
---

1 分钟阅读
您现在可以通过 Vercel 的 AI 网关访问 MiniMax 的最新模型 M2.1，无需其他供应商账户。
MiniMax M2.1 比其前身 M2 速度更快，在编码用例以及涉及工具调用的复杂多步骤任务方面有明显改进。M2.1 编写的代码质量更高，更擅长遵循困难任务的指令，且推理过程更清晰。该模型不仅深入，而且广度兼备，在多种编程语言（Go、C++、JS、C#、TS 等）以及代码重构、功能添加、错误修复和代码审查方面的性能均有提升。
要通过 AI SDK 开始使用 MiniMax M2.1 进行开发，请将模型设置为 minimax/minimax-m2.1
：
import { streamText } from 'ai';
const result = streamText({ model: 'minimax/minimax-m2.1', prompt: `Initialize a React + TypeScript project of a sunrise. Generate assets with an image tool, compute sun position with a time tool, animate it, run tests, and produce a build.`});
AI 网关提供了一个统一的 API，用于调用模型、跟踪使用情况和成本，以及配置重试、故障转移和性能优化，以实现高于供应商的正常运行时间。它包含内置的可观测性、自带密钥支持以及具有自动重试功能的智能供应商路由。
了解更多关于 AI 网关的信息，查看 AI 网关模型排行榜，或在我们的模型游乐场中试用。
AI 网关：按使用量追踪顶级 AI 模型
AI 网关模型排行榜根据通过网关的所有流量的总 Token 量，对一段时间内使用最多的模型进行排名。定期更新。
查看排行榜


> 本文由AI自动翻译，原文链接：[MiniMax M2.1 now live on Vercel AI Gateway - Vercel](https://vercel.com/changelog/minimax-m2-1-now-live-on-vercel-ai-gateway)
> 
> 翻译时间：2026-01-05 17:27
