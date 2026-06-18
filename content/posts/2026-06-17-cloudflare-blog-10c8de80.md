---
title: Cloudflare引入Flue框架，构建生产级AI Agent三层架构
title_original: Bringing more agent harnesses to Cloudflare, starting with Flue
date: '2026-06-17'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/agents-platform-flue-sdk/
author: ''
summary: Cloudflare基于其Agents SDK推出三层架构，用于构建生产级AI Agent：底层为运行时/平台（Agents SDK），中间为工具框架（如Pi、Project
  Think），上层为框架（如Flue）。Flue作为首个基于该架构的开源框架，采用声明式模型，支持Slack、GitHub等渠道集成，并提供前端UI钩子，使开发者无需编写编排循环即可构建可自主解决任务的Agent。
categories:
- AI基础设施
tags:
- Cloudflare
- Flue
- Agent框架
- 生产级AI
- 三层架构
draft: false
translated_at: '2026-06-18T06:53:42.551257'
---

# 为 Cloudflare 引入更多 Agent（智能体）工具框架，从 Flue 开始

2026-06-17

- Thomas Gauvin

![](/images/posts/f1883326152b.png)

2026 年是 Agent（智能体）工具框架投入生产的一年。控制模型对外部世界访问权限的软件——如 Codex、Claude Code、OpenCode、Pi 和 Project Think 等工具框架——已经成熟到团队将 Agent（智能体）部署为真正的、承载实际负载的基础设施，而不仅仅是原型。

但构建能够在生产环境中存活的 Agent（智能体）是困难的。

我们在构建 Project Think 作为第一方 Agent（智能体）工具框架时亲身学到了这一点。在与客户合作在生产环境中运行 Agent（智能体）的过程中，我们发现每个 Agent（智能体）在云端运行时都会面临一系列通用的分布式系统问题。当 Agent（智能体）被中断时，它如何能够自动且优雅地从中断处恢复，而不会丢失上下文或浪费 Token？Agent（智能体）如何安全地运行不受信任的代码？Agent（智能体）如何使用它们被训练过的工具？

一个工具框架本身无法解决这些问题。它们与状态、存储和计算紧密相关——这意味着它们依赖于 Agent（智能体）运行的平台。这就是为什么我们将从 Project Think 生产环境加固中获得的经验，作为基础层引入 Cloudflare Agents SDK。持久化执行、动态代码执行、持久化文件系统和动态工作流，现在可供任何基于 Agents SDK 构建的工具框架使用。

与此同时，在工具框架之上出现了一个新层次。像 Flue 这样的框架用项目结构、约定、集成和开发者体验来包装工具框架，使 Agent（智能体）的构建更加高效。

为了解决这些扩展挑战，一个用于构建生产级 AI 的新型三层架构正在形成。以下是各层如何组合在一起，从面向用户的开发者体验到底层平台原语：

- **框架（Flue）**——项目结构、约定、集成、CLI 以及构建 Agent（智能体）的开发者体验。
- **工具框架（Pi, Project Think）**——调用工具、读取结果、管理上下文并持续执行直到任务完成的智能循环。
- **运行时/平台（Cloudflare Agents SDK）**——上述所有层所依赖的计算、状态和存储原语。

框架（Flue）——项目结构、约定、集成、CLI 以及构建 Agent（智能体）的开发者体验。

工具框架（Pi, Project Think）——调用工具、读取结果、管理上下文并持续执行直到任务完成的智能循环。

运行时/平台（Cloudflare Agents SDK）——上述所有层所依赖的计算、状态和存储原语。

Agents SDK 就是底层：它使持久化执行等原语可供任何工具框架和任何框架使用。Flue，我们来自 Astro 团队的新开源框架，是第一个基于它构建的框架。以下是具体实现方式。

Flue 本周发布了 1.0 Beta 版本，基于 Pi 工具框架构建，该框架与 OpenClaw 所使用的相同。它作为 Agent（智能体）框架的不同之处在于其方法：你不是编写脚本告诉 Agent（智能体）做什么，而是描述它知道什么。定义 Agent（智能体）所需的上下文——它的模型、技能、沙箱和指令——它就会自主解决你交给它的任何任务。无需编写编排循环。

这种声明式模型使得编写 Agent（智能体）变得简单：以下是一个分诊 Agent（智能体），它拦截错误报告，在沙箱中复现问题，并在不到 25 行代码内诊断问题。

### Flue 的开发者体验

Flue 的强大之处在于 Agent（智能体）并非孤立存在。它们被构建为存在于用户已经工作的地方，并与你偏好的工具集成：

- **随处可用的 Agent（智能体）**：将你的 Agent（智能体）放入 Slack、GitHub、Linear 或 Discord，使用预配置的 Channels 自动处理事件验证和分发样板代码。
- **无头但支持 UI**：Agent（智能体）不应存在于黑盒中。Flue Agent（智能体）可以完全无头运行以处理后台任务，但 `@flue/react` 提供了原生前端钩子，可将 Agent（智能体）的状态、工具执行和实时消息直接流式传输到你的前端应用中，无需从头构建自定义实时管道。
- **生态就绪**：Flue 通过 `flue add channel slack` 等命令轻松添加和升级集成，生成一个 Markdown 蓝图，你自己的编码 Agent（智能体）可以读取、修改并干净地集成到你的代码库中。

随处可用的 Agent（智能体）：将你的 Agent（智能体）放入 Slack、GitHub、Linear 或 Discord，使用预配置的 Channels 自动处理事件验证和分发样板代码。

无头但支持 UI：Agent（智能体）不应存在于黑盒中。Flue Agent（智能体）可以完全无头运行以处理后台任务，但 `@flue/react` 提供了原生前端钩子，可将 Agent（智能体）的状态、工具执行和实时消息直接流式传输到你的前端应用中，无需从头构建自定义实时管道。

生态就绪：Flue 通过 `flue add channel slack` 等命令轻松添加和升级集成，生成一个 Markdown 蓝图，你自己的编码 Agent（智能体）可以读取、修改并干净地集成到你的代码库中。

### 为生产环境设计，而非仅限原型

将 Agent（智能体）从本地终端迁移到生产生态系统会引入传统的分布式系统故障。主机崩溃、来自 LLM 提供商的 API 超时以及意外重启，都可能抹去正在运行的 Agent（智能体）轮次的短期记忆。

Flue 通过 Durable Streams 解决了这个问题。执行历史中的每个事件都被添加到一个仅追加的日志中。通过将每个提示词、工具响应和模型选择作为不可更改的账本处理，Agent（智能体）的状态永远不会是易失性的。如果进程死亡，另一个进程只需拾取日志并从它离开的确切步骤继续执行。

### 随处部署，包括 Cloudflare

Flue 是一个多云框架。在 Node.js 上，每个 Agent（智能体）作为一个长期运行的进程运行。你可以将其部署到任何 VM 或容器，在 GitHub Actions 中运行，或嵌入到现有服务器上。但当目标平台是 Cloudflare 时，每个 Agent（智能体）都会成为一个 Durable Object。

通过将每个 Flue Agent（智能体）运行在其自己的 Durable Object 内，Cloudflare 可以自动扩展到你所需的任意数量的 Agent（智能体），每个 Agent（智能体）都有自己独立的存储和计算。你无需配置服务器、管理粘性会话或担心噪声邻居。当 Flue Agent（智能体）部署到 Cloudflare 时，它们使用 Agents SDK 的 `runFiber()`、`stash()` 和 `onFiberRecovered()` 方法实现持久化执行。Flue 还使用 `@cloudflare/codemode` 和 `@cloudflare/shell` 在持久化工作区内进行沙箱化代码执行。

## 工具框架对 Agent（智能体）平台的需求

Flue 的 Cloudflare 目标之所以如此有效，是因为它清晰地映射到我们在 Agents SDK 中构建的核心原语。你甚至可以深入查看 Flue 源代码，以了解底层工具框架 Pi 如何适配在 Cloudflare Agents SDK 上运行。

以下是 Flue 如何在底层利用 Agents SDK，以及可靠地大规模运行任何现代 Agent（智能体）工具框架所需的条件。

### 每个 Agent（智能体）工具框架都需要持久化执行

一个 Agent（智能体）轮次并非单个请求。模型流式传输 Token、调用工具、等待结果、可能请求人工批准，或将工作委托给子 Agent（智能体）。这个序列可能需要几秒或几分钟，并且在任何时刻进程都可能被中断或崩溃。当这种情况发生时，所有在内存中的 Agent（智能体）状态都会丢失：流式连接、待处理的工具调用、Agent（智能体）在其轮次中的位置。当然，对话历史会持久化到磁盘，但用户会看到一个永远无法解析的旋转加载图标。这是一种糟糕的用户体验。

Fiber通过在Agent底层的Durable Object内部提供原生的检查点机制来解决这个问题。`runFiber()`在Agent轮次工作开始之前将进度记录到Durable Object的SQLite存储中，并随着轮次的推进使用`stash()`设置检查点。当新的Agent实例在中断后启动时，`onFiberRecovered()`会传递最后一个检查点，这样你的Agent就知道某个轮次被中断了、中断到了哪里，并可以决定如何继续执行。

```javascript
import { Agent } from "agents";
import type { FiberRecoveryContext } from "agents";

class MyAgent extends Agent {
  async doWork() {
    await this.runFiber("my-task", async (ctx) => {
      const step1 = await expensiveOperation();
      ctx.stash({ step1 });

      const step2 = await anotherExpensiveOperation(step1);
      this.setState({ ...this.state, result: step2 });
    });
  }

  async onFiberRecovered(ctx: FiberRecoveryContext) {
    if (ctx.name !== "my-task") return;

    const { step1 } = (ctx.snapshot ?? {}) as { step1?: unknown };
    if (step1) {
      const step2 = await anotherExpensiveOperation(step1);
      this.setState({ ...this.state, result: step2 });
    }
  }
}
```

Flue在其Cloudflare目标上正是使用了`runFiber()`来实现这一点。借助`onFiberRecovered()`钩子，你的框架可以决定如何恢复轮次的执行，无论是像Project Think那样尝试完全重建模型来修复轮次状态，还是重放轮次的某些部分。

### 执行代码比给Agent塞满工具更好

Agent框架通过工具让模型访问外部世界。但工具列表增长迅速，随着列表变长以及上下文窗口被工具定义填满，模型在选择正确工具方面的表现会变差。一个更好的模式是：给模型一个执行代码的工具。模型编写一个TypeScript函数来调用它所需的API，然后由框架来执行。我们在引入Code Mode时曾写过这一点。

问题在于这段代码在哪里运行。为了安全地运行LLM生成的代码，你需要一个沙箱。但典型的沙箱对于每次工具调用来说，速度慢、成本高且效率低下。这就是为什么Agents SDK提供了`@cloudflare/codemode`，它封装了Dynamic Workers，在你提供的绑定范围内，在其自己的Worker隔离环境中执行LLM生成的代码。

Code Mode为每个代码片段创建一个全新的Dynamic Worker，运行它，然后将其丢弃。隔离环境在10毫秒内启动，每次加载成本为$0.002，相比每次Agent需要执行一小段代码时启动一个容器，执行速度显著更快，成本也更低。Flue在其Cloudflare目标上使用`@cloudflare/codemode`来驱动其代码工具。Agent针对工作区编写JavaScript，并通过Code Mode运行它。

### 大多数工作区任务不需要完整的容器

Agent框架通常需要一个文件系统，无论是用于读取文件、写入输出、搜索代码还是理解差异。特别是编码Agent，它们活在文件系统中。但如果框架运行在无服务器环境中，它如何获得一个跨执行持久化的文件系统呢？

通常的答案是使用容器。这可行，但对于Agent主要做的事情来说成本高昂。Agent轮次中的大多数文件系统操作都是文本操作。考虑一个审查Agent，它读取文件、通过源码进行grep搜索，或者编写补丁。你不需要为此启动一个完整的Linux系统。

`@cloudflare/shell`为你的Agent在其Durable Object内部提供了一个由SQLite支持的持久化虚拟文件系统。它提供了类型化的文件操作——读取、写入、编辑、搜索、grep、差异比较——Agent框架可以将其作为工具使用。

运行在Cloudflare目标上的Flue Agent不是调用单个工具，而是针对工作区虚拟文件状态API编写JavaScript。通过在Durable Object内部运行更多操作，Agent受益于隔离模型更高效的执行过程，完全避免了容器开销：

```javascript
async () => {
  const files = await state.glob("src/**/*.ts");
  const results = [];
  for (const file of files) {
    const content = await state.readFile(file);
    const todos = content.match(/\/\/ TODO:.*/g);
    if (todos) results.push({ file, todos });
  }
  return results;
}
```

这为需要运行Shell和文件系统操作来完成工作的Agent，转化成了一个更快、更具成本效益的沙箱环境。而对于需要完整操作系统（例如运行npm install、git或编译器）的Agent，Cloudflare Containers提供了这种能力。我们还在构建`@cloudflare/workspace`，以使给定Durable Object的虚拟文件系统与容器的文件系统保持同步，从而允许在需要时才从轻量级Workers无缝过渡到Linux环境。

### 动态工作流：让Agent编写自己的工作流以一致地重复任务

但是，当Agent需要做的不仅仅是读取文件或执行单个代码片段时，会发生什么？当它需要编排一个大规模、多步骤的管道，并且该管道必须随着时间的推移一致地重复执行时，比如一个成功解决Bug的代码审查，或一个产生良好结果的研究工作流，会发生什么？框架本身无法提供持久化的多步骤执行。它需要平台来持久化每一步、重试失败并在中断后恢复。

这种模式正越来越受欢迎。Claude Code最近推出了动态工作流，Claude在运行时编写一个JavaScript脚本，将工作分派给数十个子Agent，然后运行时持久化地执行它。`@cloudflare/dynamic-workflows`为任何运行在Agents SDK上的框架提供了此功能。你的Agent在运行时生成一个工作流，Workflows引擎会持久化每一步、重试失败，并且可以休眠数小时或等待外部事件（如人工审批）。

从Agent类中，`runWorkflow()`将你的Agent连接到Workflows引擎。Agent启动工作流后可以进入休眠状态。工作流通过RPC回调Agent以报告进度、更新状态或请求审批。当工作流完成时，Agent带着结果被唤醒。

### 直接访问Cloudflare生态系统

除了计算和存储，Agent框架还需要访问外部能力：网页浏览、电子邮件、记忆、搜索、推理。一个框架不应该需要单独集成每一个能力、为每一个能力管理API密钥，或者担心凭据通过Agent生成的代码泄露。

Agent类通过绑定让你的框架访问Cloudflare的其他部分：用于按Agent跟踪支出和设置限制的AI Gateway、用于网页自动化的Browser Run、用于收件箱工作流的Email Service、用于持久化回忆的Agent Memory、用于检索的AI Search、用于需要完整操作系统的工作负载的Containers，以及跨越14+模型提供商的推理。绑定在不暴露凭据的情况下授予能力：你的Agent使用它们，但密钥永远不会进入Agent生成的代码。

## 将你的Agent带到Agentic云

我们知道这种方法有效，因为它正是我们用来构建Project Think（我们第一方的Agent框架）的确切架构基础。虽然Project Think仍然是我们为原生Cloudflare Agent体验提供的高度优化、开箱即用的解决方案，但Agents SDK确保了更广泛的开源生态系统（包括Flue）能够利用这些完全相同的、久经考验的基元。

如果你今天正在使用Flue构建Agent，只需点击几下即可部署到Cloudflare。如果你正在构建自己的Agent框架或Agent框架，请以Agents SDK为目标，并免费获得平台集成。

- Agents SDK：developers.cloudflare.com/agents
- Flue：flueframework.com，npm install @flue/runtime
- Think：docs
- Cloudflare Community：community.cloudflare.com

Agents SDK：developers.cloudflare.com/agents

Flue：flueframework.com，npm install @flue/runtime

Think：docs

Cloudflare Community：community.cloudflare.com

---

> 本文由AI自动翻译，原文链接：[Bringing more agent harnesses to Cloudflare, starting with Flue](https://blog.cloudflare.com/agents-platform-flue-sdk/)
> 
> 翻译时间：2026-06-18 06:53
