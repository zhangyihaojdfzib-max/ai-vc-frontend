---
title: 开源安全工具deepsec：用AI Agent挖掘代码漏洞
title_original: 'Introducing deepsec: The security harness for finding vulnerabilities
  in your codebase'
date: '2026-05-04'
source: Vercel Blog
source_url: https://vercel.com/blog/introducing-deepsec-find-and-fix-vulnerabilities-in-your-code-base
author: ''
summary: Vercel开源了deepsec，一个由编码Agent驱动的安全防护工具，可在本地基础设施上运行，无需将源代码上传至云端。它利用Claude和Codex等模型，通过静态扫描、Agent调查、重新验证等流程，发现大型代码库中的安全隐患。支持自定义插件和扩展至Vercel
  Sandbox并行执行，误报率约10-20%。已在Vercel及客户代码库中验证有效性，适合应用和服务的安全审计。
categories:
- AI产品
tags:
- deepsec
- 代码安全
- AI Agent
- 开源工具
- 漏洞检测
draft: false
translated_at: '2026-05-05T05:08:08.305412'
---

今天我们开源了 **deepsec**：一个由编码 Agent（智能体）驱动的安全防护工具。它运行在你自己的基础设施上，能够发现大型代码库中难以察觉的问题。

你可以在笔记本电脑上运行 **deepsec**，无需为特权源代码访问搭建云服务。推理方面，你可以直接使用现有的 Claude 或 Codex 订阅，无需额外设置。

在单台机器上扫描大型仓库可能需要数天时间。为了并行运行研究任务，**deepsec** 支持可选地扩展到 Vercel Sandbox 进行远程执行。在 Vercel 的代码库上，扫描通常会扩展到 1000 个以上的并发 Sandbox。

## 链接到标题架构

核心上，**deepsec** 使用 Claude 和 Codex，通过 Opus 4.7（最大努力）和 GPT 5.5（极高推理能力）对代码库进行定制化调查。

扫描从静态分析开始，识别安全敏感文件，然后编码 Agent（智能体）调查每个候选文件，追踪数据流，检查缓解措施，并生成带有严重性评级的可操作发现。以下是工作流程：

- **扫描**：首先对所有文件执行仅基于正则表达式的扫描，识别后续步骤将关注的安全敏感区域。
- **调查**：Agent（智能体）调查扫描中识别的每个文件。
- **重新验证**：第二次 Agent（智能体）运行验证调查结果，以消除误报并重新分类严重性。
- **丰富**：调查完成后，Agent（智能体）使用 git 元数据和其他可选服务，识别负责修复每个问题的贡献者。
- **导出**：`export` 命令将发现格式化为指令，以便将其转化为供人类和编码 Agent（智能体）处理的工单。

**扫描**：首先对所有文件执行仅基于正则表达式的扫描，识别后续步骤将关注的安全敏感区域。

**调查**：Agent（智能体）调查扫描中识别的每个文件。

**重新验证**：第二次 Agent（智能体）运行验证调查结果，以消除误报并重新分类严重性。

**丰富**：调查完成后，Agent（智能体）使用 git 元数据和其他可选服务，识别负责修复每个问题的贡献者。

**导出**：`export` 命令将发现格式化为指令，以便将其转化为供人类和编码 Agent（智能体）处理的工单。

![](/images/posts/d5d392340b92.jpg)

![](/images/posts/a572fee7b799.jpg)

![](/images/posts/73e9ab177fef.jpg)

![](/images/posts/de513f0d14fe.jpg)

## 链接到标题在生产代码上运行 deepsec

**deepsec** 在我们自己的单体仓库以及客户的代码库中都非常有用。在开发过程中，我们在 Vercel 客户和合作伙伴的几个开源仓库上运行了 **deepsec**。

例如，**deepsec** 扫描了 dub.co 的开源版本。Dub 是一个面向联盟营销和短链接的市场归因平台，也以 SaaS 形式提供。它具有认证访问功能，与数据库交互，并运行多个后端服务，形成了庞大的安全面。当我们与创始人 Steven Tey 分享 **deepsec** 的发现时，他回复道：

在针对 Vercel 自己的单体仓库运行时，**deepsec** 识别出了认证条件中的细微边界情况，这促使我们开发了一个自定义扫描器插件，覆盖了代码中的所有认证路径。

### 链接到标题误报与最佳用途

**deepsec** 的部分发现会是误报。根据我们的经验，误报率大约在 10-20%。考虑到在我们自己的研究中真实发现的潜在影响，我们对这个结果感到满意，并且我们构建了重新验证步骤，让 Agent（智能体）进一步验证其发现以减少误报。

**deepsec** 最适合用于应用和服务。它可能也适用于库和框架，但这可能需要自定义提示词和扫描器。

## 链接到标题自定义与插件

**deepsec** 附带一个插件系统，用于使其适应你的代码库。最常见的插件是自定义扫描器：针对你的认证模型、数据层或团队约定进行调整的正则表达式匹配器。我们建议将 **deepsec** 与你的编码 Agent（智能体）结合使用，并让它根据初始扫描的发现编写这些匹配器：

```
1检查之前针对 ./my-app 的运行结果。2我们是否应该添加自定义的 deepsec 匹配器，3以找到更多潜在的漏洞候选？
```

## 链接到标题我需要访问特殊的“网络模型”吗？

Anthropic 和 OpenAI 都提供其最强模型的“网络”版本，这些版本经过微调，可以接受基础模型不会接受的安全任务。**deepsec** 可以与这些模型一起使用，但也完全兼容现成的模型。

**deepsec** 附带一个分类器，用于在每个研究步骤后检查任务是否被拒绝。根据我们的经验，对于 **deepsec** 使用的提示词，Opus 4.7 和 GPT 5.5 的拒绝都不是问题。

## 链接到标题开始使用

要开始使用，请在仓库根目录运行 `npx deepsec init`。这将创建一个名为 `./.deepsec` 的目录，用于配置系统并存储你的 **deepsec** 调查目录。然后，按照命令的输出进行操作。在 Github 上阅读完整文档。

## 链接到标题欢迎反馈

虽然我们已经广泛使用了 **deepsec**，但它仍处于早期开发阶段。欢迎在 GitHub 上提供反馈和贡献。

---

> 本文由AI自动翻译，原文链接：[Introducing deepsec: The security harness for finding vulnerabilities in your codebase](https://vercel.com/blog/introducing-deepsec-find-and-fix-vulnerabilities-in-your-code-base)
> 
> 翻译时间：2026-05-05 05:08
