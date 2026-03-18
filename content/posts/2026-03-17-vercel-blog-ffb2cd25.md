---
title: Vercel推出AI编程助手插件，增强项目理解能力
title_original: Introducing the Vercel plugin for coding agents - Vercel
date: '2026-03-17'
source: Vercel Blog
source_url: https://vercel.com/changelog/introducing-vercel-plugin-for-coding-agents
author: ''
summary: Vercel发布了一款专为AI编程助手设计的插件，该插件通过实时监控文件编辑和终端命令，将Vercel平台知识动态注入到Claude Code和Cursor等智能体的上下文中。插件采用关系型知识图谱，涵盖47项以上平台技能，包括Next.js、AI
  SDK等关键技术，并提供三个专业智能体和五个斜杠命令。其独特之处在于通过模式匹配器和优先级注入管道实现精准知识触发，而非传统检索方式，同时具备代码验证功能，能实时检测过时模式。该插件目前支持Claude
  Code和Cursor，即将扩展至OpenAI Codex。
categories:
- AI产品
tags:
- Vercel
- AI编程助手
- 知识图谱
- 代码生成
- 开发工具
draft: false
translated_at: '2026-03-18T04:59:16.344106'
---

Claude Code 和 Cursor 现在可以通过新的 Vercel 插件和一个完整的平台知识图谱，进一步理解 Vercel 项目。

该插件通过观察实时活动（包括文件编辑和终端命令），将 Vercel 知识动态注入到 Agent（智能体）的上下文中。其主要功能包括：

- **平台知识**：通过关系型知识图谱，访问涵盖 Vercel 平台的 47 项以上技能，包括 Next.js、AI SDK、Turborepo、Vercel Functions 和 Routing Middleware。
- **专用工具**：使用三个专业 Agent（智能体）（AI 架构师、部署专家、性能优化器）和五个斜杠命令（/bootstrap、/deploy、/env、/status、/marketplace）。
- **上下文管理**：注入引擎和项目分析器对加载的上下文进行排序、去重和预算控制。
- **代码验证**：PostToolUse 验证功能可实时捕获已弃用的模式、停止维护的软件包和过时的 API。

该插件并非采用标准检索方式，而是在构建时编译模式匹配器，并在七个生命周期钩子中运行优先级排序的注入管道。当全局模式、bash 正则表达式、导入语句或提示词信号匹配时，相关技能便会触发，并在整个会话期间进行去重，以确保 Agent（智能体）响应的准确性。

该插件目前支持 Claude Code 和 Cursor，即将支持 OpenAI Codex。

通过 npx 安装插件：

```
1npx plugins add vercel/vercel-plugin
```

在 Claude Code 中通过官方市场直接安装：

```
1/plugin install vercel
```

或在 Cursor 中直接安装：

```
1/add-plugin vercel
```

请在 Vercel 插件仓库中探索源代码。

---

> 本文由AI自动翻译，原文链接：[Introducing the Vercel plugin for coding agents - Vercel](https://vercel.com/changelog/introducing-vercel-plugin-for-coding-agents)
> 
> 翻译时间：2026-03-18 04:59
