---
title: Project Think：在Cloudflare上构建下一代AI Agent
title_original: 'Project Think: building the next generation of AI agents on Cloudflare'
date: '2026-04-15'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/project-think/
author: ''
summary: Cloudflare推出Project Think，这是一套用于构建下一代AI Agent的SDK。它解决了当前编码Agent存在的三大障碍：难以共享协作、空闲成本高昂以及管理复杂。通过提供持久化执行、子Agent、沙盒化代码执行等新原语，并基于Durable
  Objects实现按需唤醒和零闲置成本，Project Think旨在为大规模、长期运行的AI Agent提供可持续的基础设施，使其从临时工具转变为真正的智能助手。
categories:
- AI基础设施
tags:
- AI Agent
- Cloudflare
- 开发者工具
- 无服务器计算
- 人工智能基础设施
draft: false
translated_at: '2026-04-16T05:03:09.948989'
---

# Project Think：在 Cloudflare 上构建下一代 AI Agent

2026-04-15

- Sunil Pai
- Kate Reznykova

![](/images/posts/53fe598d827e.png)

今天，我们推出 Project Think：下一代 Agents SDK。Project Think 是一套用于构建长期运行 Agent 的新原语（持久化执行、子 Agent、沙盒化代码执行、持久化会话）以及一个将它们连接起来的、有明确设计理念的基类。您可以使用这些原语精确构建所需功能，也可以使用基类快速上手。

今年早些时候发生了一些事情，改变了我们对 AI 的思考方式。像 Pi、OpenClaw、Claude Code 和 Codex 这样的工具证明了一个简单而强大的理念：赋予 LLM（大语言模型）读取文件、编写代码、执行代码以及记住所学内容的能力，你会得到一种看起来不那么像开发工具，而更像通用助手的东西。

这些编码 Agent 不再仅仅是编写代码。人们正在使用它们来管理日历、分析数据集、协商采购、报税以及自动化整个业务工作流。模式总是相同的：Agent 读取上下文，进行推理，编写代码以采取行动，观察结果，然后迭代。代码是行动的通用媒介。

我们的团队每天都在使用这些编码 Agent。并且我们不断遇到同样的障碍：

-   它们只能在您的笔记本电脑或昂贵的 VPS 上运行：无法共享、无法协作、无法在设备间交接。
-   它们在空闲时成本高昂：无论 Agent 是否在工作，都有固定的月成本。将其扩展到团队或公司，成本会迅速累积。
-   它们需要管理和手动设置：安装依赖项、管理更新、配置身份和密钥。

它们只能在您的笔记本电脑或昂贵的 VPS 上运行：无法共享、无法协作、无法在设备间交接。

它们在空闲时成本高昂：无论 Agent 是否在工作，都有固定的月成本。将其扩展到团队或公司，成本会迅速累积。

它们需要管理和手动设置：安装依赖项、管理更新、配置身份和密钥。

并且存在更深层次的结构性问题。传统应用程序从一个实例服务许多用户。正如我们在《欢迎来到 Agent 周》博文中提到的，Agent 是一对一的。每个 Agent 都是一个独特的实例，服务一个用户，运行一个任务。一家餐厅有一个菜单和一个为批量生产菜肴而优化的厨房。而 Agent 更像是一位私人厨师：每次都有不同的食材、不同的技术、不同的工具。

这从根本上改变了扩展的计算方式。如果一亿知识工作者每人使用一个 Agent 助手，即使并发量不大，您也需要数千万个同时会话的容量。按照当前每个容器的成本，这是不可持续的。我们需要一个不同的基础。

这就是我们一直在构建的。

## 介绍 Project Think

Project Think 为 Agents SDK 提供了一套新原语：

-   使用纤程的持久化执行：崩溃恢复、检查点、自动保活
-   子 Agent：拥有自己的 SQLite 和类型化 RPC 的隔离子 Agent
-   持久化会话：树状结构消息、分叉、压缩、全文搜索
-   沙盒化代码执行：动态 Workers、代码模式、运行时 npm 解析
-   执行阶梯：工作区、隔离环境、npm、浏览器、沙盒
-   自编写扩展：在运行时编写自己工具的 Agent

使用纤程的持久化执行：崩溃恢复、检查点、自动保活

子 Agent：拥有自己的 SQLite 和类型化 RPC 的隔离子 Agent

持久化会话：树状结构消息、分叉、压缩、全文搜索

沙盒化代码执行：动态 Workers、代码模式、运行时 npm 解析

执行阶梯：工作区、隔离环境、npm、浏览器、沙盒

自编写扩展：在运行时编写自己工具的 Agent

其中每一项都可以直接与 Agent 基类一起使用。使用原语精确构建您需要的功能，或者使用 Think 基类快速上手。让我们看看每一项的功能。

## 长期运行的 Agent

目前存在的 Agent 是短暂的。它们运行一个会话，绑定到单个进程或设备，然后就消失了。一个在您笔记本电脑休眠时就会死掉的编码 Agent，那只是一个工具。而一个能够持久存在——可以按需唤醒、在中断后继续工作、并且在不依赖本地运行时的情况下保持状态——的 Agent，开始看起来像基础设施。这完全改变了 Agent 的扩展模型。

Agents SDK 建立在 Durable Objects 之上，为每个 Agent 提供身份、持久化状态以及按消息唤醒的能力。这是 Actor 模型：每个 Agent 都是一个可寻址的实体，拥有自己的 SQLite 数据库。它在休眠时不消耗任何计算资源。当有事件发生时（HTTP 请求、WebSocket 消息、计划警报、入站电子邮件），平台会唤醒 Agent，加载其状态，并将事件传递给它。Agent 完成工作后，便再次进入休眠状态。

虚拟机 / 容器

Durable Objects

空闲成本

始终全额计算成本

零（休眠时）

扩展

预配和管理容量

自动，按 Agent

状态

需要外部数据库

内置 SQLite

恢复

您需要构建（进程管理器、健康检查）

平台重启，状态保留

身份 / 路由

您需要构建（负载均衡器、粘性会话）

内置（名称 → Agent）

10,000 个 Agent，每个活跃时间 1%

10,000 个始终在线的实例

任何时刻约 100 个活跃实例

这改变了大规模运行 Agent 的经济性。您可以从“每个高级用户一个昂贵的 Agent”转变为构建“每个客户一个 Agent”或“每个任务一个 Agent”或“每个电子邮件线程一个 Agent”。生成新 Agent 的边际成本实际上为零。

### 在崩溃中存活：使用纤程的持久化执行

一次 LLM 调用可能需要 30 秒。一个多轮次的 Agent 循环可以运行更长时间。在该时间窗口内的任何时刻，执行环境都可能消失：部署、平台重启、达到资源限制。与模型提供者的上游连接被永久切断，内存中的状态丢失，连接的客户端看到流停止而没有任何解释。

`runFiber()` 解决了这个问题。纤程是一个持久化的函数调用：在执行开始前在 SQLite 中注册，可以通过 `stash()` 在任何时刻设置检查点，并且可以通过 `onFiberRecovered` 在重启时恢复。

```Typescript
import { Agent } from "agents";

export class ResearchAgent extends Agent {
  async startResearch(topic: string) {
    void this.runFiber("research", async (ctx) => {
      const findings = [];

      for (let i = 0; i < 10; i++) {
        const result = await this.callLLM(`Research step ${i}: ${topic}`);
        findings.push(result);

        // Checkpoint: if evicted, we resume from here
        ctx.stash({ findings, step: i, topic });

        this.broadcast({ type: "progress", step: i });
      }

      return { findings };
    });
  }

  async onFiberRecovered(ctx) {
    if (ctx.name === "research" && ctx.snapshot) {
      const { topic } = ctx.snapshot;
      await this.startResearch(topic);
    }
  }
}
```

SDK 在纤程执行期间会自动保持 Agent 存活，无需特殊配置。对于以分钟计的工作，`keepAlive()` / `keepAliveWhile()` 可以防止在活动工作期间被驱逐。对于更长时间的操作（CI 流水线、设计评审、视频生成），Agent 可以启动工作，持久化作业 ID，休眠，并在回调时唤醒。

### 委派工作：通过 Facets 实现子 Agent

单个 Agent 不应自己完成所有事情。子 Agent 是通过 Facets 与父 Agent 共置的子 Durable Objects，每个子 Agent 都有自己的隔离 SQLite 和执行上下文：

```Typescript
import { Agent } from "agents";

export class ResearchAgent extends Agent {
  async search(query: string) { /* ... */ }
}

export class ReviewAgent extends Agent {
  async analyze(query: string) { /* ... */ }
}
```

```typescript
export class Orchestrator extends Agent {
  async handleTask(task: string) {
    const researcher = await this.subAgent(ResearchAgent, "research");
    const reviewer = await this.subAgent(ReviewAgent, "review");

    const [research, review] = await Promise.all([
      researcher.search(task),
      reviewer.analyze(task)
    ]);

    return this.synthesize(research, review);
  }
}
```

子 Agent 在存储层面是隔离的。每个子 Agent 都拥有自己的 SQLite 数据库，它们之间没有隐式的数据共享。这是由运行时强制执行的，其中子 Agent 之间的 RPC 延迟相当于一次函数调用。TypeScript 会在编译时捕获误用。

### 持久化的对话：Session API

需要运行数天或数周的 Agent 需要的不仅仅是典型的扁平化消息列表。实验性的 `Session` API 对此进行了明确建模。该 API 在 Agent 基类上可用，对话以树形结构存储，其中每条消息都有一个 `parent_id`。这使得分支（探索替代方案而不丢失原始路径）、非破坏性压缩（总结旧消息而非删除它们）以及通过 `FTS5` 对对话历史进行全文搜索成为可能。

```Typescript
import { Agent } from "agents";
import { Session, SessionManager } from "agents/experimental/memory/session";

export class MyAgent extends Agent {
  sessions = SessionManager.create(this);

  async onStart() {
    const session = this.sessions.create("main");
    const history = session.getHistory();
    const forked = this.sessions.fork(session.id, messageId, "alternative-approach");
  }
}
```

`Session` 可以直接与 `Agent` 一起使用，并且它是 `Think` 基类所构建的存储层。

## 从工具调用到代码执行

传统的工具调用形式笨拙。模型调用一个工具，通过上下文窗口拉回结果，再调用另一个工具，再拉回结果，如此反复。随着工具表面的增长，这变得既昂贵又笨拙。一百个文件意味着需要一百次往返模型的行程。

但是，**模型更擅长编写代码来使用一个系统，而不是玩工具调用的游戏**。这正是 `@cloudflare/codemode` 背后的洞见：LLM 不是进行顺序的工具调用，而是编写一个处理整个任务的单一程序。

```Typescript
// 这是由 LLM 编写的。它在沙盒化的 Dynamic Worker 中运行。
const files = await tools.find({ pattern: "**/*.ts" });
const results = [];
for (const file of files) {
  const content = await tools.read({ path: file });
  if (content.includes("TODO")) {
    results.push({ file, todos: content.match(/\/\/ TODO:.*/g) });
  }
}
return results;
```

你无需向模型进行 100 次往返，只需运行一个程序。这导致使用的 Token 更少、执行速度更快、结果更好。`Cloudflare API MCP server` 大规模地展示了这一点。我们只暴露两个工具（`search()` 和 `execute()`），它们消耗约 1,000 个 Token，而与之等效的、为每个端点使用一个工具的原始方法则需要约 117 万个 Token。这减少了 99.9%。

### 缺失的原语：安全的沙盒

一旦你接受模型应该代表用户编写代码，问题就变成了：这些代码在哪里运行？不是最终，不是在产品团队将其纳入路线图之后。而是现在，为这个用户，针对这个系统，在严格定义的权限下。

**Dynamic Workers** 就是那个沙盒。一个在运行时启动的全新 V8 隔离环境，只需几毫秒，占用几兆字节内存。这比容器大约快 100 倍，内存效率高达 100 倍。你可以为每个请求启动一个新的隔离环境，运行一段代码，然后将其丢弃。

关键的设计选择是**能力模型**。Dynamic Workers 不是从一个通用的机器开始并试图限制它，而是从几乎没有任何环境权限开始（全局 `Outbound: null`，无网络访问），开发者通过绑定，逐个资源地、明确地授予能力。我们从问“我们如何阻止这个东西做太多事？”转变为“我们到底希望这个东西能做什么？”

这对于 Agent 基础设施来说是正确的问题。

### 执行阶梯

这种能力模型自然引出了一系列计算环境，即一个**执行阶梯**，Agent 可以根据需要逐步提升：

**第 0 级**是工作区，一个由 SQLite 和 R2 支持的持久化虚拟文件系统。读取、写入、编辑、搜索、grep、diff。由 `@cloudflare/shell` 提供支持。

**第 1 级**是 Dynamic Worker：LLM 生成的 JavaScript 在无网络访问的沙盒化隔离环境中运行。由 `@cloudflare/codemode` 提供支持。

**第 2 级**增加了 npm。`@cloudflare/worker-bundler` 从注册表获取包，使用 esbuild 打包，并将结果加载到 Dynamic Worker 中。Agent 编写 `import { z } from "zod"` 即可正常工作。

**第 3 级**是通过 `Cloudflare Browser Run` 实现的无头浏览器。导航、点击、提取、截图。当服务尚未通过 MCP 或 API 支持 Agent 时很有用。

**第 4 级**是配置了你的工具链、代码库和依赖项的 `Cloudflare Sandbox`：`git clone`、`npm test`、`cargo build`，并与工作区双向同步。

关键的设计原则是：**Agent 应该仅在第 0 级就有用，每一级都是叠加的。** 用户可以逐步添加能力。

### 构建模块，而非框架

所有这些原语都作为独立的包提供。`Dynamic Workers`、`@cloudflare/codemode`、`@cloudflare/worker-bundler` 和 `@cloudflare/shell`（一个带有工具的持久化文件系统）都可以直接与 Agent 基类一起使用。你可以组合它们，为任何 Agent 提供工作区、代码执行和运行时包解析功能，而无需采用一个固执己见的框架。

## 平台

以下是在 Cloudflare 上构建 Agent 的完整技术栈：

| 能力 | 作用 | 由...提供支持 |
| :--- | :--- | :--- |
| **按 Agent 隔离** | 每个 Agent 都是自己的世界 | Durable Objects |
| **空闲时零成本** | 在 Agent 唤醒前费用为 $0 | DO Hibernation |
| **持久化状态** | 可查询、事务性存储 | DO SQLite |
| **持久化文件系统** | 重启后仍存在的文件 | Workspace (SQLite + R2) |
| **沙盒化代码执行** | 安全运行 LLM 生成的代码 | Dynamic Workers + `@cloudflare/codemode` |
| **运行时依赖** | `import * from react` 直接可用 | `@cloudflare/worker-bundler` |
| **Web 自动化** | 浏览、导航、填写表单 | Browser Run |
| **完整操作系统访问** | git、编译器、测试运行器 | Sandboxes |
| **计划执行** | 主动式，而非仅被动响应 | DO Alarms + Fibers |
| **实时流式传输** | 逐 Token 传输到任何客户端 | WebSockets |
| **外部工具** | 连接到任何工具服务器 | MCP |
| **Agent 协调** | Agent 间类型化 RPC | Sub-agents (Facets) |
| **模型访问** | 连接 LLM 为 Agent 提供动力 | AI Gateway + Workers AI (或自带模型) |

每一个都是构建模块。它们共同构成了新的东西：一个平台，任何人都可以构建、部署和运行与今天在你本地机器上运行的 AI Agent 一样强大的 Agent，但它们是**无服务器的、持久化的，并且在构建上是安全的**。

## Think 基类

现在你已经了解了这些原语，接下来看看当把它们全部连接在一起时会发生什么。

`Think` 是一个固执己见的框架，它处理完整的聊天生命周期：Agent 循环、消息持久化、流式传输、工具执行、流恢复和扩展。你可以专注于让你的 Agent 独特的部分。

最小的子类如下所示：

```Typescript
import { Think } from "@cloudflare/think";
import { createWorkersAI } from "workers-ai-provider";

export class MyAgent extends Think<Env> {
  getModel() {
    return createWorkersAI({ binding: this.env.AI })(
      "@cf/moonshotai/kimi-k2.5"
    );
  }
}
```

这实际上就是你拥有一个具有流式传输、持久化、中止/取消、错误处理、可恢复流和内置工作区文件系统的可用聊天 Agent 所需的全部。使用 `npx wrangler deploy` 进行部署。

`Think` 为你做出决策。当你需要更多控制时，可以覆盖你关心的部分：

| 覆盖方法 | 目的 |
| :--- | :--- |
| `getModel()` | 返回要使用的 `LanguageModel` |
| `getSystemPrompt()` | 系统提示词 |

AI SDK 兼容的 Agent（智能体）循环工具集

maxSteps

每轮最大工具调用次数

configureSession()

上下文块、压缩、搜索、技能

底层原理上，Think 在每一轮都运行完整的 Agent（智能体）循环：它组装上下文（基础指令 + 工具描述 + 技能 + 记忆 + 对话历史），调用 `streamText`，执行工具调用（并截断输出以防止上下文爆炸），追加结果，循环直到模型完成或达到步数限制。所有消息在每一轮后都会被持久化。

### 生命周期钩子

Think 在聊天轮次的每个阶段都为你提供了钩子，而无需你掌控整个流水线：

```Typescript
beforeTurn()
  → streamText()
    → beforeToolCall()
    → afterToolCall()
  → onStepFinish()
→ onChatResponse()
```

切换到成本更低的模型进行后续轮次，限制其可使用的工具，并在每一轮传入客户端上下文。同时，将每次工具调用记录到分析系统，并在模型完成后自动触发一次额外的后续轮次，所有这些都无需替换 `onChatMessage`。

### 持久化记忆与长对话

Think 基于 `Session` API 构建，作为其存储层，为你提供了内置分支的树状结构消息。

在此基础上，它通过**上下文块**增加了持久化记忆。这些是系统提示词的结构化部分，模型可以随时间读取和更新，并且它们在休眠期间持续存在。模型会看到“MEMORY (Important facts, use set_context to update) [42%, 462/1100 tokens]”，并能够主动记住信息。

```Typescript
configureSession(session: Session) {
  return session
    .withContext("soul", {
      provider: { get: async () => "You are a helpful coding assistant." }
    })
    .withContext("memory", {
      description: "Important facts learned during conversation.",
      maxTokens: 2000
    })
    .withCachedPrompt();
}
```

会话非常灵活。你可以为每个 Agent（智能体）运行多个对话，并分叉它们以尝试不同方向，而不会丢失原始对话。

随着上下文增长，Think 通过非破坏性压缩来处理限制。较早的消息会被总结而非删除，而完整的历史记录仍存储在 SQLite 中。

搜索功能也已内置。使用 FTS5，你可以在一个会话内或跨所有会话查询对话历史。Agent（智能体）也能够使用 `search_context` 工具搜索自己的过去。

### 完整的执行阶梯，已集成

Think 将整个执行阶梯集成到单个 `getTools()` 返回中：

```Typescript
import { Think } from "@cloudflare/think";
import { createWorkspaceTools } from "@cloudflare/think/tools/workspace";
import { createExecuteTool } from "@cloudflare/think/tools/execute";
import { createBrowserTools } from "@cloudflare/think/tools/browser";
import { createSandboxTools } from "@cloudflare/think/tools/sandbox";
import { createExtensionTools } from "@cloudflare/think/tools/extensions";

export class MyAgent extends Think<Env> {
  extensionLoader = this.env.LOADER;

  getModel() {
    /* ... */
  }

  getTools() {
    return {
      execute: createExecuteTool({
        tools: createWorkspaceTools(this.workspace),
        loader: this.env.LOADER
      }),
      ...createBrowserTools(this.env.BROWSER),
      ...createSandboxTools(this.env.SANDBOX), // 按 Agent（智能体）配置：工具链、仓库、快照
      ...createExtensionTools({ manager: this.extensionManager! }),
      ...this.extensionManager!.getTools()
    };
  }
}
```

### 自编写扩展

Think 将代码执行更进一步。一个 Agent（智能体）可以编写自己的扩展：这是在动态 Worker 中运行的 TypeScript 程序，声明了网络访问和工作空间操作的权限。

```JSON
{
  "name": "github",
  "description": "GitHub integration: PRs, issues, repos",
  "tools": ["create_pr", "list_issues", "review_pr"],
  "permissions": {
    "network": ["api.github.com"],
    "workspace": "read-write"
  }
}
```

Think 的 `ExtensionManager` 会打包扩展（可选地通过 `@cloudflare/worker-bundler` 包含 npm 依赖），将其加载到动态 Worker 中，并注册新工具。该扩展持久化存储在 Durable Object 存储中，并在休眠后依然存在。下次用户询问拉取请求时，Agent（智能体）就拥有了一个 30 秒前还不存在的 `github_create_pr` 工具。

正是这种自我改进循环，使得 Agent（智能体）随着时间的推移真正变得更有用。不是通过微调或 RLHF（人类反馈强化学习），而是通过代码。Agent（智能体）能够为自己编写新的能力，全部都在沙盒化、可审计、可撤销的 TypeScript 中完成。

### 子 Agent（智能体）RPC

Think 也可以作为子 Agent（智能体）工作，通过 RPC 从父级调用 `chat()`，并通过回调进行流式事件传输：

```Typescript
const researcher = await this.subAgent(ResearchSession, "research");
const result = await researcher.chat(`Research this: ${task}`, streamRelay);
```

每个子 Agent（智能体）都有自己的对话树、记忆、工具和模型。父级无需了解细节。

### 开始使用

Project Think 是实验性的。其 API 接口是稳定的，但在未来几天和几周内会持续演进。我们已经在内部使用它来构建我们自己的后台 Agent（智能体）基础设施，并提前分享出来，以便你可以与我们一同构建。

```Shell
npm install @cloudflare/think agents ai @cloudflare/shell zod workers-ai-provider
```

```Typescript
// src/server.ts
import { Think } from "@cloudflare/think";
import { createWorkersAI } from "workers-ai-provider";
import { routeAgentRequest } from "agents";

export class MyAgent extends Think<Env> {
  getModel() {
    return createWorkersAI({ binding: this.env.AI })(
      "@cf/moonshotai/kimi-k2.5"
    );
  }
}

export default {
  async fetch(request: Request, env: Env) {
    return (
      (await routeAgentRequest(request, env)) ||
      new Response("Not found", { status: 404 })
    );
  }
} satisfies ExportedHandler<Env>;
```

```Typescript
// src/client.tsx
import { useAgent } from "agents/react";
import { useAgentChat } from "@cloudflare/ai-chat/react";

function Chat() {
  const agent = useAgent({ agent: "MyAgent" });
  const { messages, sendMessage, status } = useAgentChat({ agent });
  // 渲染你的聊天界面
}
```

Think 使用与 `@cloudflare/ai-chat` 相同的 WebSocket 协议，因此现有的 UI 组件可以开箱即用。如果你是基于 `AIChatAgent` 构建的，你的客户端代码无需更改。

## 第三波浪潮

我们看到 AI Agent（智能体）的三波浪潮：

第一波浪潮是聊天机器人。它们是无状态的、被动的且脆弱的。每次对话都从头开始，没有记忆，没有工具，也没有行动能力。这使得它们对于回答问题很有用，但也将其限制在只能回答问题。

第二波浪潮是编码 Agent（智能体）。这些是有状态的、使用工具的、能力强大得多的工具，如 Pi、Claude Code、OpenClaw 和 Codex。这些 Agent（智能体）可以读取代码库、编写代码、执行代码并迭代。这些证明了配备合适工具的 LLM（大语言模型）是一台通用机器，但它们在你的笔记本电脑上运行，面向单一用户，且没有持久性保证。

现在我们正在进入第三波浪潮：**作为基础设施的 Agent（智能体）**。持久的、分布式的、结构安全的、无服务器的。这些 Agent（智能体）在互联网上运行，能在故障中存活，空闲时成本为零，并通过架构而非行为来强制执行安全性。任何开发者都可以为任意数量的用户构建和部署的 Agent（智能体）。

这就是我们押注的方向。

Agents SDK 已经在为数以千计的生产环境 Agent（智能体）提供支持。通过 Project Think 及其引入的原语，我们正在添加缺失的部分，以显著增强这些 Agent（智能体）的能力：持久化工作空间、沙盒化代码执行、持久化的长时间运行任务、结构性安全、子 Agent（智能体）协调以及自编写扩展。

它现在已提供预览版。我们与你一同构建，并且我们真诚地希望看到你（以及你的编码 Agent（智能体））用它创造出什么。

Think 是 Cloudflare Agents SDK 的一部分，可通过 @cloudflare/think 获取。本文描述的功能目前处于预览阶段。随着我们吸收反馈，API 可能会发生变化。请查阅文档和示例以开始使用。

---

> 本文由AI自动翻译，原文链接：[Project Think: building the next generation of AI agents on Cloudflare](https://blog.cloudflare.com/project-think/)
> 
> 翻译时间：2026-04-16 05:03
