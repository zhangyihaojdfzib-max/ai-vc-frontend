---
title: Mux如何利用@mux/ai SDK与Vercel实现持久化视频AI工作流
title_original: How Mux shipped durable video workflows with their @mux/ai SDK - Vercel
date: '2026-01-12'
source: Vercel Blog
source_url: https://vercel.com/blog/how-mux-shipped-durable-video-workflows-with-their-mux-ai-sdk
author: ''
summary: 本文介绍了Mux如何通过其开源SDK @mux/ai解决AI视频工作流中常见的执行中断问题。文章指出，传统AI工作流容易因网络超时、速率限制等原因中途失败，导致开发者需要处理复杂的重试和状态管理。Mux选择Vercel的Workflow
  DevKit作为解决方案，该工具允许开发者在普通Node.js环境中编写代码，并通过简单的“use workflow”指令即可在支持的环境中自动获得持久化执行、状态管理和可观测性能力，无需绑定特定基础设施或学习新的DSL。
categories:
- AI基础设施
tags:
- 视频处理
- AI工作流
- 持久化执行
- Vercel
- Mux
draft: false
translated_at: '2026-01-13T04:34:49.209794'
---

我们邀请了来自 Mux 的 Dylan Jhaveri 来分享他们如何通过其 `@mux/ai` SDK 交付持久化的工作流。

AI 工作流有一个令人沮丧的习惯：它们常常会在中途失败。你的内容审核检查通过了，正在生成视频章节，然后却遇到了网络超时、速率限制，或者某个服务提供商“状态不佳”而随机返回 500 错误。现在你卡住了。你是从头开始重启，并再次为审核检查付费？还是写一堆状态管理代码来记住上次中断的位置？

这正是持久化执行改变一切的地方。

当我们着手构建 `@mux/ai`（一个旨在帮助客户在 Mux 视频基础设施之上构建 AI 功能的开源 SDK）时，我们面临一个根本性问题：如何以一种易于开发者采用、且不迫使他们做出复杂基础设施决策的方式，来交付持久化的工作流？

答案是 Vercel 的 Workflow DevKit。

## AI 视频处理流程的痛点

一个典型的视频 AI 工作流可能如下所示：

1.  使用 Mux API 获取视频元数据
2.  使用 Mux API 自动生成字幕
3.  使用 Mux API 获取视频的缩略图和/或故事板
4.  使用 LLM 进行内容审核，以确保视频符合你的内容政策
5.  使用 LLM 生成摘要和标签
6.  使用 LLM 生成章节
7.  使用 LLM 生成其他语言的翻译字幕

为了正确实现这一点，你需要使用消息队列、状态机、重试逻辑和可观测性来构建自定义编排。这些都是为长时间运行任务构建生产级基础设施所需的一切。而这并不是开发者在尝试交付功能时所想要的。

## 为什么 Workflow DevKit 是合适的选择

在评估解决方案时，我们有明确的原则：

*   **无硬性基础设施要求**。你应该能够在任何 Node.js 环境中运行 `@mux/ai` 中的函数，就像使用普通 SDK 一样。
*   **可选的持久化**。如果你需要持久性、可观测性和错误处理，那么添加这些功能应该是轻而易举的。
*   **熟悉的模式**。没有新的 DSL，没有 YAML，没有状态机定义。只用 JavaScript。

Workflow DevKit 满足了所有这些要求。`"use workflow"` 和 `"use step"` 指令让我们可以在 SDK 中标记函数以实现持久化执行，而无需改变你编写代码的方式。如果你在标准的 Node 环境中，这些指令会被忽略。它不会产生任何操作。如果你在 Workflow DevKit 环境中运行，它们会为你提供自动重试、状态持久化和可观测性。

这是 Workflow DevKit 的关键洞察：同一份代码可以在任何地方运行，但在部署到正确的环境时会获得持久性保证。并且我们支持 Workflow DevKit，而无需承担明确的依赖。如果你在使用 Workflow DevKit：很好，你将获得随之而来的所有好处。如果你没有使用：没关系，你仍然可以将 `@mux/ai` 作为普通的 Node 包使用。

我们考虑过的所有其他选项，要么需要承担特定的第三方依赖并将我们自己绑定到一个选项上，要么需要构建更复杂的 API 接口，以便开发者可以在每个离散步骤周围添加包装函数。这并非不可能，但需要付出更大的努力并做出一整套新的决策。

## 实际运作方式

以下是使用 `@mux/ai` 的持久化视频 AI 工作流示例：

```
1import { getSummaryAndTags, getModerationScores } from '@mux/ai/workflows';2
3export async function processVideo(assetId: string) {4  "use workflow";5  6  const summaryResp = await getSummaryAndTags(assetId);7  // ✅ 步骤成功。summaryResp 被持久化。8  9  const moderationResp = await getModerationScores(assetId, {10    thresholds: { sexual: 0.7, violence: 0.8 }11  });12  // ❌ 步骤失败。工作流被挂起。13  // ✅ 重放发生，并从此处恢复，14  //    无需重新执行上面的 getSummaryAndTags 工作。15  // ✅ 步骤成功。moderationResp 被持久化。16
17  // 使用 Workflow DevKit，你可以在一个更大的 "use workflow" 中18  // 嵌套你自己的 "use workflow" 和 "use step" 函数19  const emailResp = await emailUser(assetId);20  // ✅ 嵌套的工作流成功。你 emailUser 工作流中的每个步骤21  //    都被视为一个独立的步骤。22
23  return { summaryResp, moderationResp, emailResp };24}
```

当一个步骤首次运行失败，然后在 2 秒后重试并成功时，在可观测性仪表板中看起来是这样的：

每个 `"use step"` 函数都是独立运行的。如果在生成摘要和标签后，审核 API 失败了，工作流会从上次中断的地方恢复。你不会丢失已经付费完成的工作。执行分布在多个无服务器函数调用中，因此长时间运行的 AI 操作永远不会触及超时限制。

`@mux/ai` SDK 还**内置了基础单元**，这些是更低层次的单一工作单元，例如 `fetchTranscriptForAsset` 和 `getStoryboardUrl`。这些函数已通过 `"use step"` 指令导出，因此你可以将它们引入到自己的工作流中，并将其视为离散步骤。

## 随处部署，在 Vercel 上扩展

Workflow DevKit 通过“世界”的概念设计时考虑了可移植性。一个“世界”是存储工作流状态的地方。在本地，它是磁盘上的 JSON 文件。在 Vercel 上，它会为你管理。或者你可以**使用 Postgres、Redis 自托管，或构建你自己的**。最简单的路径是使用本地世界在本地开发和测试，然后部署到 Vercel，在那里所有资源（包括可观测性仪表板）都会自动配置。这是默认的零配置体验。

对于部署到 Vercel 的团队来说，这意味着：

*   **零基础设施配置**。Vercel 检测持久化函数并为你处理资源调配。
*   **内置可观测性**。每次工作流运行的跟踪、日志和指标。通过重放执行或状态时间旅行进行调试。
*   **自动扩展**。无论你是处理十个视频还是一万个，平台都能自动适应，无需人工干预。

## 你可以构建什么

`@mux/ai` 内置了**针对常见视频 AI 任务的预构建工作流**：

*   **摘要和标签**：自动理解并分类你的视频库
*   **章节生成**：基于内容结构创建导航点
*   **内容审核**：在问题内容触达用户之前进行标记
*   **翻译和配音**：使视频支持多种语言
*   **嵌入/向量**：为最近邻搜索生成嵌入/向量

嵌入/向量：为最近邻搜索生成嵌入向量

所有工作流均与模型无关。根据任务需求，可使用OpenAI、Anthropic或Gemini。所有代码均在Apache 2.0协议下开源，您可以根据需要进行分支、修改和扩展。

## 快速开始

在本地开发环境中，工作流无需额外配置即可运行。若需在Vercel上启用持久化功能，请为项目添加Workflow DevKit集成模块。您在本地测试的代码在规模化部署时将保持完全一致的行为特性。

查阅完整文档获取全面指南和示例。我们通过实时评估结果、公开CI流程和完整测试覆盖率进行开源共建，欢迎提交PR。

## 下一步计划

视频AI仅是起点。这种持久化执行模式适用于任何包含外部依赖的多步骤流程：文档处理流水线、数据同步工作流、智能体编排等。Workflow DevKit提供基础框架，具体应用场景由您定义。

我们期待看到您的创作成果。欢迎来信分享您的项目进展，并告知我们尚未涵盖的工作流类型。

## 资源链接

- Mux博客：发布持久化AI工作流
- Next.js模板（含代码示例）
- 演示视频
- @mux/ai产品公告
- GitHub代码库

发布持久化AI工作流

Next.js模板（含代码示例）

@mux/ai产品公告

本文由Dylan Jhaveri与Mux团队共同撰写。Mux致力于为开发者构建视频基础设施，@mux/ai通过与Workflow DevKit集成，使AI视频工作流无需额外基础设施即可投入生产环境。

> 本文由AI自动翻译，原文链接：[How Mux shipped durable video workflows with their @mux/ai SDK - Vercel](https://vercel.com/blog/how-mux-shipped-durable-video-workflows-with-their-mux-ai-sdk)
> 
> 翻译时间：2026-01-13 04:34
