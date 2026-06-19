---
title: Vercel开源Agent框架eve：文件即智能体
title_original: Introducing eve, an open-source agent framework - Vercel
date: '2026-06-17'
source: Vercel Blog
source_url: https://vercel.com/changelog/introducing-eve-an-open-source-agent-framework
author: ''
summary: Vercel发布了开源Agent框架eve，该框架将智能体定义为文件目录，内置持久化执行、沙箱计算、人工审批、子Agent和评估等生产级能力。用户只需创建模型和指令两个文件即可运行最小Agent，通过添加文件即可扩展工具、技能、渠道和计划。eve基于TypeScript，可一键初始化项目，并支持直接部署到Vercel生产环境。该框架已被Vercel用于构建和运行自身Agent，旨在简化Agent开发与部署流程。
categories:
- AI基础设施
tags:
- Vercel
- 开源框架
- Agent
- 智能体
- TypeScript
draft: false
translated_at: '2026-06-19T07:08:59.830746'
---

eve 现已公开预览。

eve 是一个用于构建、运行和扩展 Agent（智能体）的开源框架。Agent（智能体）只是一个文件目录，生产级能力已内置其中：

- 持久化执行
- 沙箱化计算
- 人工介入审批
- 子 Agent（智能体）
- 评估

持久化执行

沙箱化计算

人工介入审批

子 Agent（智能体）

评估

```
agent/  agent.ts                   # 它运行的模型  instructions.md            # 它是谁  tools/    run_sql.ts               # 它能做什么    post_chart.ts  skills/    revenue-definitions.md   # 它知道什么  subagents/    investigator/            # 它委托给谁  channels/    slack.ts                 # 它在哪里  schedules/    monday-summary.ts        # 它何时自主行动
```

一个数据分析师 Agent（智能体），一目了然

能运行的最小 Agent（智能体）只需两个文件：一个模型和一组指令。

```
1import { defineAgent } from "eve";2
3export default defineAgent({4  model: "anthropic/claude-opus-4.8",5});
```

在一个文件中配置 Agent（智能体）及其模型

```
你是一位高级数据分析师。你回答关于团队数据的问题。
- 优先使用精确数字而非模糊表述。如果可以计算，就计算出来。- 报告任何数字时，说明其背后的假设（日期范围、筛选条件、粒度）。- 使用你拥有的工具，而不是猜测。如果无法从数据中回答，请直说。
```

Agent（智能体）的身份和固定规则，每次模型调用时前置添加

通过添加文件来增加工具、技能、渠道或计划。eve 在构建时自动识别并为你连接它们，因此无需样板代码来注册。

你可以通过一条命令快速搭建并启动一个新的 Agent（智能体）。它会安装依赖、搭建项目并启动开发服务器，让你在一分钟内就能在本地运行一个 Agent（智能体）。

```
npx eve@latest init my-agent
```

你的第一个 eve Agent（智能体）

或者，你可以让你的编码 Agent（智能体）为你设置。给它这个提示词：

```
为用户设置一个 Eve agent。Eve 是一个基于文件系统的 TypeScript 框架，用于构建持久化 agent，以 npm 包 eve 发布。阅读其文档：安装 eve 后，文档位于 node_modules/eve/docs 中；在安装 eve 之前，请阅读已发布的 Introduction 和 Getting Started 页面。如果项目没有 Eve 应用，使用 `npx eve@latest init <name>` 搭建一个；仅当用户需要 Web Chat 时添加 `--channel-web-nextjs`。init 命令会安装依赖、初始化 Git 并启动开发服务器，因此请在一个可控进程中运行它，并在编辑前停止它。要将 Eve 添加到现有应用，运行 `npm install eve@latest`。确保 agent/agent.ts 和 agent/instructions.md 存在，然后使用 eve/tools 中的 defineTool 在 agent/tools/get_weather.ts 添加第一个带类型工具，包含 Zod inputSchema 和内联 execute。再次启动开发服务器，然后测试 HTTP API：使用 POST /eve/v1/session 创建会话，连接到 GET /eve/v1/session/:id/stream，并使用返回的 continuationToken 发送后续消息。使用项目的类型检查进行验证，根据项目调整模型和提供商选择，除非用户要求，否则不要提交。
```

给你的编码 Agent（智能体）的起始提示词

由于 eve Agent（智能体）是一个普通的 Vercel 项目，vercel 部署可以将其原样部署到生产环境，就像在你机器上运行一样。

eve 是 Vercel 用来构建和运行自身 Agent（智能体）的框架。如需全面了解，请阅读公告或文档，你也可以在 github.com/vercel/eve 上关注其公开开发进程。

构建你的第一个 Agent（智能体）

Agent（智能体）是一个文件目录，eve 以持久化执行、沙箱、审批和内置评估来运行它。适用于任何模型、任何 MCP 服务器，以及 Slack、Discord 和 GitHub 等渠道。

开始使用

---

> 本文由AI自动翻译，原文链接：[Introducing eve, an open-source agent framework - Vercel](https://vercel.com/changelog/introducing-eve-an-open-source-agent-framework)
> 
> 翻译时间：2026-06-19 07:08
