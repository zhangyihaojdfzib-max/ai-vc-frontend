---
title: LangSmith发布CLI与技能集，大幅提升AI编程Agent能力
title_original: LangSmith CLI & Skills
date: '2026-03-04'
source: LangChain Blog
source_url: https://blog.langchain.com/langsmith-cli-skills/
author: ''
summary: 本文介绍了LangSmith新推出的CLI工具和首批技能集，旨在增强AI编程Agent在LangSmith生态系统中的专业能力。CLI为Agent提供了追踪、数据集管理和实验运行等基础模块，而技能集则通过动态加载的指令和脚本，显著提升了Agent在追踪、数据集构建和性能评估三大核心任务上的表现。文章展示了使用技能后，Claude
  Code在相关任务上的性能从17%提升至92%，并阐述了如何通过技能实现Agent开发的良性循环。
categories:
- AI产品
tags:
- LangSmith
- AI编程Agent
- CLI
- 技能集
- AI开发工具
draft: false
translated_at: '2026-03-05T04:45:16.626781'
---

我们发布了CLI以及首批技能集，旨在让AI编程Agent（智能体）在LangSmith生态系统中获得专业能力。这包括为Agent添加追踪功能、理解其执行过程、构建测试集以及评估性能。在我们的评估集上，这项改进将Claude Code在这些任务上的表现从17%提升至92%。

## LangSmith CLI

其核心是我们全新的LangSmith CLI。该CLI专为Agent原生设计：它为编程Agent（及开发者）提供了在LangSmith生态内进行任何操作所需的基础模块，包括获取追踪记录、整理数据集和运行实验。当与技能集中的指导相结合时，编程Agent能够完全通过终端流畅地操作LangSmith。我们认为，实现这一点对Agent开发的未来至关重要，因为我们预计Agent的改进循环将越来越多地由其他优先使用终端的Agent驱动。

您可以通过以下安装脚本安装CLI：

```
curl -sSL https://raw.githubusercontent.com/langchain-ai/langsmith-cli/main/scripts/install.sh | sh
```

## 什么是技能？

技能是经过精心设计的指令、脚本和资源，用于提升编程Agent在特定领域的表现。重要的是，技能通过渐进式披露动态加载——Agent仅在任务相关时才会检索相应技能。这增强了Agent的能力，因为历史上给予Agent过多工具反而会导致其性能下降。

技能具有可移植性和可共享性——它们由可按需检索的Markdown文件和脚本组成。我们分享了一套LangSmith技能集，可移植到任何支持技能功能的编程Agent中。

## LangSmith技能集

在langsmith-skills代码库中，我们维护了3项核心技能：

- trace：为现有代码添加追踪功能，并查询追踪记录
- dataset：构建示例数据集
- evaluator：基于这些数据集评估Agent性能

这三个领域代表了LangSmith AI工程的三大核心方向。我们将持续扩充这套技能集。

## 技能效果

通过使用技能，我们观察到Claude Code在基础LangSmith任务上的性能得到了显著提升。

这些技能使编程Agent能够在Agent开发中形成良性循环。您的编程Agent可以利用LangChain和LangSmith技能实现：

1. 为Agent添加追踪逻辑
2. 通过Agent生成追踪记录，并有效用于调试行为
3. 利用生成的追踪记录创建系统化测试数据集
4. 创建评估器在数据集上运行并验证Agent准确性
5. 基于评估结果和人工反馈进一步迭代Agent架构

这个循环是加速Agent开发的强大工具。要查看实际演示，请参阅我们的技能演示：

## 安装

您可以使用npx skills安装这些技能：

本地（当前项目）：

```bash
npx skills add langchain-ai/langsmith-skills --skill '*' --yes

```

全局（所有项目）：

```bash
npx skills add langchain-ai/langsmith-skills --skill '*' --yes --global

```

将技能关联到特定Agent（例如Claude Code）：

```bash
npx skills add langchain-ai/langsmith-skills --agent claude-code --skill '*' --yes --global

```

## 结语

我们期待社区使用LangChain和LangSmith来提升在我们生态系统中构建应用的体验。随着LangSmith新增功能，我们计划持续扩充技能内容。同时，我们还发布了用于与LangChain开源库（LangChain、LangGraph和DeepAgents）交互的技能集。如果您对新增技能或改进有任何想法，我们非常乐意听取您的意见！

### 加入我们的新闻通讯

获取LangChain团队及社区的最新动态

正在处理您的请求...

成功！请查收邮件并点击链接确认订阅。

抱歉，出现错误。请重试。

---

> 本文由AI自动翻译，原文链接：[LangSmith CLI & Skills](https://blog.langchain.com/langsmith-cli-skills/)
> 
> 翻译时间：2026-03-05 04:45
