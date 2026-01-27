---
title: Skills v1.1.1发布：交互式技能发现、开源及智能体支持
title_original: 'Skills v1.1.1: Interactive discovery, open source release, and agent
  support - Vercel'
date: '2026-01-26'
source: Vercel Blog
source_url: https://vercel.com/changelog/skills-v1-1-1-interactive-discovery-open-source-release-and-agent-support
author: ''
summary: Vercel推出的Skills工具包发布v1.1.1版本，核心更新包括：新增交互式技能发现功能，开发者可通过`npx skills find`命令实时搜索并集成技能；为AI智能体提供编程化技能发现路径，包含元“find-skills”技能及非交互模式，支持27个编码智能体；简化维护流程，引入`npx
  skills update`命令自动刷新本地技能。此外，项目已在GitHub完全开源，并弃用旧版`npx add-skill`命令，推动开发者体验与自动化工作流的融合。
categories:
- AI基础设施
tags:
- Vercel
- AI智能体
- 开源工具
- 开发者工具
- 技能发现
draft: false
translated_at: '2026-01-27T00:56:56.575671'
---

![](/images/posts/eaea1c3d22be.jpg)

![](/images/posts/86bb5827f832.jpg)

skills@1.1.1 版本新增了交互式技能发现功能，现已完全开源。

新的交互式发现功能为开发者保持了简洁的工作流程，同时通过用更新的 `npx skills` 接口取代已弃用的 `npx add-skill` 命令，为 Agent（智能体）提供了一条清晰的、以编程方式发现技能的路径。

现在，您可以使用 `npx skills find` 在输入时进行搜索并交互式地发现技能。对于 AI Agent（智能体），Skills 包含一个元 "find-skills" 技能，以及一个为自动化工作流设计的非交互模式，并支持 27 个编码 Agent（智能体）。

借助新的 `npx skills update` 命令，Skills 的维护也变得更加简单，该命令无需手动步骤即可刷新您的本地技能。

完整代码库已在 GitHub 上的 Skills 仓库中提供。

### 迁移

之前的 `npx add-skill` 命令已被弃用。请使用 `npx skills find` 进行交互式发现，并使用 `npx skills update` 来刷新现有技能。

通过 `npx skills@latest` 开始使用，或探索 Skills 仓库。

```
1npx skills add vercel-labs/agent-skills
```

---

> 本文由AI自动翻译，原文链接：[Skills v1.1.1: Interactive discovery, open source release, and agent support - Vercel](https://vercel.com/changelog/skills-v1-1-1-interactive-discovery-open-source-release-and-agent-support)
> 
> 翻译时间：2026-01-27 00:56
