---
title: Vercel沙箱自定义标签功能上线测试版
title_original: Custom tags available in beta on Vercel Sandbox - Vercel – Vercel
date: '2026-04-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/custom-tags-available-in-beta-on-vercel-sandbox
author: ''
summary: Vercel在沙箱产品中推出自定义标签功能（测试版），允许用户为每个沙箱添加最多五个标签，以按环境、团队、客户等维度组织和管理沙箱。标签可动态更新，并支持按标签筛选沙箱，适用于AI
  Agent工作流追踪、多租户平台隔离、团队成本归因等场景。该功能需升级至beta版SDK和CLI包。
categories:
- AI基础设施
tags:
- Vercel
- 沙箱管理
- 自定义标签
- AI Agent
- 多租户
draft: false
translated_at: '2026-05-01T05:45:57.790424'
---

随着团队为AI Agent（智能体）、代码生成或开发工作流扩展隔离环境时，追踪每个沙箱属于谁以及为何创建变得至关重要。自定义标签让你能够大规模组织、筛选和管理Vercel沙箱。每个沙箱最多支持五个标签。

### 按环境、团队或客户组织

标签在设计上具有灵活性。使用它们来区分预发布环境与生产环境、将使用量归因到特定团队，或在多租户平台中按客户隔离沙箱：

```
1const sandbox = await Sandbox.create({2  name: "my-sandbox",3  tags: { env: "staging" },4});
```

### 随上下文变化更新标签

将沙箱从预发布环境提升至生产环境、重新分配所有权，或标记为待清理，而无需重新创建：

```
1await sandbox.update({2  tags: { env: "production", team: "infra" },3});
```

### 轻松追踪你的沙箱

按任意标签筛选沙箱，快速找到重要的那些。这对于需要查找匹配特定环境或团队的所有沙箱的仪表盘、清理脚本或路由逻辑非常有用：

```
1const productionSandboxes = await Sandbox.list({2  tags: { env: "production" },3});4console.log(5  "Production sandboxes:",6  productionSandboxes.sandboxes.map((s) => s.name),7); 
```

### 使用场景

- 大规模AI Agent（智能体）：按会话、用户或Agent（智能体）运行来标记沙箱，以追踪每个执行环境属于哪个工作流。
- 多租户平台：按客户或工作空间隔离和筛选沙箱，使计费归因和清理变得简单直接。
- 团队级可见性：将沙箱使用量归因到特定团队，用于成本追踪或容量规划。

大规模AI Agent（智能体）：按会话、用户或Agent（智能体）运行来标记沙箱，以追踪每个执行环境属于哪个工作流。

多租户平台：按客户或工作空间隔离和筛选沙箱，使计费归因和清理变得简单直接。

团队级可见性：将沙箱使用量归因到特定团队，用于成本追踪或容量规划。

此功能处于测试阶段，需要升级至beta版SDK和CLI包。在文档中了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Custom tags available in beta on Vercel Sandbox - Vercel – Vercel](https://vercel.com/changelog/custom-tags-available-in-beta-on-vercel-sandbox)
> 
> 翻译时间：2026-05-01 05:45
