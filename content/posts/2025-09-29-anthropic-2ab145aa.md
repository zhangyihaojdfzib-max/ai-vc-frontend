---
title: Claude Code升级：更自主的AI编程助手
title_original: Enabling Claude Code to work more autonomously
date: '2025-09-29'
source: Anthropic
source_url: https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously
author: ''
summary: 本文介绍了Claude Code的多项重要升级，包括原生VS Code扩展、增强的终端界面2.0版本以及用于自主操作的检查点功能。在Sonnet
  4.5模型驱动下，Claude Code现在能够处理更长、更复杂的开发任务。新功能包括检查点系统（支持代码状态回滚）、子智能体并行开发、钩子自动触发操作以及后台任务管理。这些改进使开发者能够更放心地将大规模重构、功能探索等复杂任务委托给AI助手，同时保持对开发流程的控制。
categories:
- AI产品
tags:
- Claude Code
- AI编程助手
- VS Code扩展
- 自主智能体
- 开发工具
draft: false
translated_at: '2026-02-09T04:32:27.567224'
---

# 让 Claude Code 更自主地工作

我们为 Claude Code 引入了多项升级：一个原生的 VS Code 扩展、我们终端界面的 2.0 版本，以及用于自主操作的检查点。在 Sonnet 4.5 的驱动下，Claude Code 现在可以在您的终端和 IDE 中处理更长、更复杂的开发任务。

## Claude Code 登陆更多平台

**VS Code 扩展**

我们正在推出一个**原生 VS Code 扩展**（测试版），它将 Claude Code 直接带入您的 IDE。现在，您可以通过一个带有内联差异显示的专用侧边栏面板，实时查看 Claude 所做的更改。该扩展为那些更喜欢在 IDE 而非终端中工作的用户提供了更丰富、更具图形化的 Claude Code 体验。

**增强的终端体验**

我们还更新了 Claude Code 的终端界面。更新后的界面具有改进的状态可见性和可搜索的提示词历史记录（Ctrl+r），使得重用或编辑之前的提示词变得更加容易。

![新 Claude Code 终端用户体验图片](/images/posts/2e50abb1c37b.jpg)

**Claude Agent SDK**

对于希望创建自定义智能体体验的团队，Claude Agent SDK（原 Claude Code SDK）提供了与驱动 Claude Code 相同的核心工具、上下文管理系统和权限框架。我们还发布了针对子智能体和钩子的 SDK 支持，使其在为您特定工作流程构建智能体时更具可定制性。

开发者们已经**开始使用该 SDK 构建智能体**，应用于广泛的用例，包括金融合规智能体、网络安全智能体和代码调试智能体。

## 自信地执行长期运行的任务

随着 Claude Code 承担越来越复杂的任务，我们发布了检查点功能，以帮助您在保持控制的同时，放心地将任务委托给 Claude Code。结合最近发布的功能，Claude Code 现在更有能力处理复杂的任务。

**检查点**

复杂的开发通常涉及探索和迭代。我们新的检查点系统会在每次更改前自动保存您的代码状态，您可以通过按两次 Esc 键或使用 /rewind 命令立即回滚到之前的版本。检查点让您可以放心地追求更宏大、更广泛的任务，因为您知道总是可以返回到之前的代码状态。

当您回滚到某个检查点时，可以选择将代码、对话或两者都恢复到之前的状态。检查点仅适用于 Claude 的编辑，不适用于用户编辑或 bash 命令，我们建议将其与版本控制结合使用。

**子智能体、钩子和后台任务**

当与 Claude Code 支持自主工作的最新功能结合使用时，检查点尤其有用：

- **子智能体**可以委托专门任务——例如在主智能体构建前端时启动后端 API——从而实现并行开发工作流程。
- **钩子**可以在特定点自动触发操作，例如在代码更改后运行测试套件，或在提交前进行代码检查。
- **后台任务**可以保持长时间运行的进程（如开发服务器）处于活动状态，而不会阻塞 Claude Code 在其他工作上的进展。

这些功能共同作用，让您可以放心地将广泛的任务（如大规模重构或功能探索）委托给 Claude Code。

## 开始使用

这些更新现已面向所有 Claude Code 用户提供。

- **Claude Sonnet 4.5** 现在是 Claude Code 中的新默认模型。运行 /model 命令可以切换模型。
- **VS Code 扩展**（测试版）：从 **VS Code 扩展市场**下载即可开始使用。
- 终端更新，包括视觉刷新和检查点功能，对所有 Claude Code 用户可用——只需更新您的本地安装即可。
- **Claude Agent SDK**：请参阅文档以开始使用。

## 相关内容

### 介绍 Claude Opus 4.6

我们正在升级我们最智能的模型。在智能体编码、计算机使用、工具使用、搜索和金融领域，Opus 4.6 都是一个行业领先的模型，通常优势明显。

### Claude 是一个思考的空间

我们做出了一个选择：Claude 将保持无广告。我们解释了为什么广告激励与真正有用的 AI 助手不相容，以及我们计划如何在不妨碍用户信任的情况下扩大访问范围。

### Apple 的 Xcode 现已支持 Claude Agent SDK

---

> 本文由AI自动翻译，原文链接：[Enabling Claude Code to work more autonomously](https://www.anthropic.com/news/enabling-claude-code-to-work-more-autonomously)
> 
> 翻译时间：2026-02-09 04:32
