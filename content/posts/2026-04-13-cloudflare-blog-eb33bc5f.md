---
title: 智能体专属计算机：Cloudflare Sandboxes正式发布
title_original: Agents have their own computers with Sandboxes GA
date: '2026-04-13'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/sandbox-ga/
author: ''
summary: Cloudflare正式发布Sandboxes和Cloudflare Containers，为AI智能体提供安全、可扩展的专属计算环境。该服务解决了智能体在代码开发与执行中的突发性需求、快速状态恢复、安全凭证管理、生命周期控制等核心难题，并新增了安全凭证注入、PTY终端支持、持久化代码解释器、快照功能等关键特性。通过与Figma等合作伙伴的实践，Sandboxes旨在为大规模部署智能体集群提供可靠的基础设施支持，且采用活跃CPU计费模式，优化成本。
categories:
- AI基础设施
tags:
- AI智能体
- 云计算
- 开发工具
- 安全沙箱
- Cloudflare
draft: false
translated_at: '2026-04-14T04:43:30.404909'
---

# Agent（智能体）现拥有专属计算机：Sandboxes 正式发布

2026-04-13

- Kate Reznykova
- Mike Nomitch
- Naresh Ramesh

![](/images/posts/26374d6af832.png)

去年六月我们推出 Cloudflare Sandboxes 时，核心理念很简单：AI Agent（智能体）需要开发和运行代码，它们需要一个安全的环境来执行这些操作。

如果 Agent（智能体）要扮演开发者的角色，就意味着需要克隆代码仓库、用多种语言构建代码、运行开发服务器等。为了高效完成这些任务，它们通常需要一台完整的计算机（如果不需要，也可以选择更轻量的方案！）。

许多开发者正在组合使用虚拟机或现有容器解决方案，但这面临诸多难题：

- **突发性需求** - 每个会话都需要独立的沙箱，经常需要快速启动大量沙箱，但又不想为闲置的备用计算资源付费。
- **快速状态恢复** - 每个会话都应能快速启动和重启，并能恢复之前的状态。
- **安全性** - Agent（智能体）需要安全地访问服务，但不能被信任持有凭证。
- **控制能力** - 需要能通过编程方式简单控制沙箱生命周期、执行命令、处理文件等。
- **易用性** - 需要为人类和 Agent（智能体）提供简单接口来执行常见操作。

我们已投入时间解决这些问题，让您无需再为此烦恼。自首次发布以来，我们已将 Sandboxes 打造成更适合大规模运行 Agent（智能体）的环境。我们与 Figma 等初期合作伙伴合作，他们在 Figma Make 的容器中运行 Agent（智能体）：

“Figma Make 旨在帮助各种背景的构建者和创造者更快地从想法走向生产。为实现这一目标，我们需要一种能提供可靠、高度可扩展沙箱的基础设施解决方案，以便运行不受信任的 Agent（智能体）和用户编写的代码。Cloudflare Containers 正是这样的解决方案。”

- Alex Mullans，Figma AI 与开发者平台负责人

我们希望将 Sandboxes 带给更多优秀组织，因此今天很高兴地宣布：**Sandboxes 和 Cloudflare Containers 均已正式发布**。

让我们看看 Sandboxes 近期的一些重要更新：

- **安全凭证注入** - 允许进行身份验证调用，而 Agent（智能体）始终无法直接访问凭证
- **PTY 支持** - 为您和您的 Agent（智能体）提供真实的终端环境
- **持久化代码解释器** - 为 Agent（智能体）提供开箱即用的有状态 Python、JavaScript 和 TypeScript 执行环境
- **后台进程与实时预览 URL** - 提供与开发服务器交互并验证实时更改的简单方式
- **文件系统监控** - 在 Agent（智能体）进行更改时提升迭代速度
- **快照功能** - 让您快速恢复 Agent（智能体）的编码会话
- **更高限制与活跃 CPU 计费** - 支持大规模部署 Agent（智能体）集群，且无需为未使用的 CPU 周期付费

## Sandboxes 基础入门

在深入了解近期更新前，我们先快速了解基础知识。

Cloudflare Sandbox 是由 **Cloudflare Containers** 驱动的持久化隔离环境。您可以通过名称请求沙箱。如果正在运行，您会直接获得；如果未运行，它将启动。闲置时会自动休眠，收到请求时自动唤醒。通过 `exec`、`gitClone`、`writeFile` 等方法，可以轻松以编程方式与沙箱交互。

```Typescript
import { getSandbox } from "@cloudflare/sandbox";
export { Sandbox } from "@cloudflare/sandbox";

export default {
  async fetch(request: Request, env: Env) {
    // 按名称请求沙箱，按需启动
    const sandbox = getSandbox(env.Sandbox, "agent-session-47");

    // 将代码仓库克隆到沙箱中
    await sandbox.gitCheckout("https://github.com/org/repo", {
      targetDir: "/workspace",
      depth: 1,
    });

    // 运行测试套件，实时流式传输输出
    return sandbox.exec("npm", ["test"], { stream: true });
  },
};
```

只要提供相同的 ID，后续请求就可以从世界任何地方访问同一个沙箱。

## 安全凭证注入

Agent（智能体）工作负载中最棘手的问题之一是身份验证。您经常需要 Agent（智能体）访问私有服务，但不能完全信任它们持有原始凭证。

Sandboxes 通过使用可编程出口代理在网络层注入凭证来解决此问题。这意味着沙箱 Agent（智能体）永远无法访问凭证，您可以完全按需自定义身份验证逻辑：

```javascript
class OpenCodeInABox extends Sandbox {
  static outboundByHost = {
    "my-internal-vcs.dev": (request, env, ctx) => {
      const headersWithAuth = new Headers(request.headers);
      headersWithAuth.set("x-auth-token", env.SECRET);
      return fetch(request, { headers: headersWithAuth });
    }
  }
}
```

如需深入了解其工作原理——包括身份感知凭证注入、动态修改规则以及与 Workers 绑定的集成——请阅读我们近期关于 **Sandbox 身份验证** 的博客文章。

## 真实终端，而非模拟

早期的 Agent（智能体）系统通常将 shell 访问建模为请求-响应循环：运行命令、等待输出、将记录反馈给提示词、重复。这种方式可行，但并非开发者实际使用终端的方式。

人类会运行命令、观察输出流、中断操作、稍后重新连接并继续。Agent（智能体）同样受益于这种反馈循环。

今年二月，我们发布了 PTY 支持。这是在 Sandbox 中通过 WebSocket 代理的伪终端会话，兼容 `xterm.js`。

只需调用 `sandbox.terminal` 即可提供后端服务：

```Typescript
// Worker：将 WebSocket 连接升级为实时终端会话
export default {
  async fetch(request: Request, env: Env) {
    const url = new URL(request.url);
    if (url.pathname === "/terminal") {
      const sandbox = getSandbox(env.Sandbox, "my-session");
      return sandbox.terminal(request, { cols: 80, rows: 24 });
    }
    return new Response("Not found", { status: 404 });
  },
};
```

并使用 `xterm` 插件从客户端调用：

```Typescript
// 浏览器：将 xterm.js 连接到沙箱 shell
import { Terminal } from "xterm";
import { SandboxAddon } from "@cloudflare/sandbox/xterm";

const term = new Terminal();
const addon = new SandboxAddon({
  getWebSocketUrl: ({ origin }) => `${origin}/terminal`,
});

term.loadAddon(addon);
term.open(document.getElementById("terminal-container")!);
addon.connect({ sandboxId: "my-session" });
```

这使得 Agent（智能体）和开发者能够使用完整的 PTY 实时调试会话。

每个终端会话都拥有独立的 shell、独立的工作目录和独立的环境。您可以按需打开多个会话，就像在自己的机器上操作一样。输出在服务器端缓冲，重新连接时会重放您错过的内容。

## 具备记忆功能的代码解释器

对于数据分析、脚本编写和探索性工作流，我们还提供了一个更高层次的抽象：一个持久化的代码执行上下文。

关键词是“持久化”。许多代码解释器实现会孤立地运行每个代码片段，因此状态在调用之间会消失。你无法在一步中设置变量，然后在下一步中读取它。

沙盒允许你创建能够持久化状态的“上下文”。变量和导入项在多次调用之间保持持久化，就像在 Jupyter notebook 中一样：

```Typescript
// 创建一个 Python 上下文。在其生命周期内，状态是持久化的。
const ctx = await sandbox.createCodeContext({ language: "python" });

// 第一次执行：加载数据
await sandbox.runCode(`
  import pandas as pd
  df = pd.read_csv('/workspace/sales.csv')
  df['margin'] = (df['revenue'] - df['cost']) / df['revenue']
`, { context: ctx });

// 第二次执行：df 仍然存在
const result = await sandbox.runCode(`
  df.groupby('region')['margin'].mean().sort_values(ascending=False)
`, { context: ctx, onStdout: (line) => console.log(line.text) });

// result 包含 matplotlib 图表、结构化的 json 输出以及 HTML 格式的 Pandas 表格

```

## 启动服务器。获取 URL。交付它。

当 Agent（智能体）能够构建某些东西并立即展示给用户时，它们会更有用。沙盒支持后台进程、就绪状态检查和预览 URL。这使得 Agent（智能体）可以启动开发服务器并分享实时链接，而无需离开对话。

```Typescript
// 将开发服务器作为后台进程启动
const server = await sandbox.startProcess("npm run dev", {
  cwd: "/workspace",
});

// 等待服务器真正就绪——不仅仅是休眠并祈祷
await server.waitForLog(/Local:.*localhost:(\d+)/);

// 通过公共 URL 暴露正在运行的服务
const { url } = await sandbox.exposePort(3000);

// url 是一个 Agent（智能体）可以与用户分享的实时公共 URL
console.log(`Preview: ${url}`);

```

借助 `waitForPort()` 和 `waitForLog()`，Agent（智能体）可以根据运行程序发出的真实信号来安排工作顺序，而不是靠猜测。这比常见的替代方案（通常是某种形式的 `sleep(2000)` 然后祈祷）要好得多。

## 监视文件系统并立即响应

现代开发循环是事件驱动的。保存文件，重新运行构建。编辑配置，重启服务器。更改测试，重新运行测试套件。

我们在三月份发布了 `sandbox.watch()`。它返回一个由原生 `inotify`（Linux 内核用于文件系统事件的机制）支持的 SSE 流。

```Typescript
import { parseSSEStream, type FileWatchSSEEvent } from '@cloudflare/sandbox';

const stream = await sandbox.watch('/workspace/src', {
  recursive: true,
  include: ['*.ts', '*.tsx']
});

for await (const event of parseSSEStream<FileWatchSSEEvent>(stream)) {
  if (event.type === 'modify' && event.path.endsWith('.ts')) {
    await sandbox.exec('npx tsc --noEmit', { cwd: '/workspace' });
  }
}

```

这是那些能悄然改变 Agent（智能体）能力的底层原语之一。一个能够实时观察文件系统的 Agent（智能体）可以像人类开发者一样参与到相同的反馈循环中。

## 通过快照快速唤醒

想象一下，一位（人类）开发者正在他们的笔记本电脑上工作。他们 `git clone` 一个仓库，运行 `npm install`，编写代码，推送一个 PR，然后在等待代码审查时合上笔记本电脑。当需要恢复工作时，他们只需重新打开笔记本电脑，就能从上次中断的地方继续。

如果 Agent（智能体）想要在一个简单的容器平台上复制这个工作流，你会遇到一个难题。如何快速恢复到之前的状态？你可以让沙盒保持运行，但那样你需要为闲置的计算资源付费。你也可以从容器镜像重新开始，但那样你必须等待漫长的 `git clone` 和 `npm install`。

我们的答案是快照，该功能将在未来几周内推出。

快照保存容器的完整磁盘状态、操作系统配置、已安装的依赖项、修改过的文件、数据文件等等。然后，它让你可以在以后快速恢复。

你可以配置一个沙盒，使其在休眠时自动创建快照。

```javascript
class AgentDevEnvironment extends Sandbox {
  sleepAfter = "5m";
  persistAcrossSessions = {type: "disk"}; // 你也可以指定单独的目录
}

```

你也可以通过编程方式创建快照并手动恢复它。这对于工作检查点或分叉会话很有用。例如，如果你想并行运行一个 Agent（智能体）的四个实例，你可以轻松地从相同状态启动四个沙盒。

```javascript
class AgentDevEnvironment extends Sandbox {}

async forkDevEnvironment(baseId, numberOfForks) {
  const baseInstance = await getSandbox(baseId);
  const snapshotId = await baseInstance.snapshot();

  const forks = Array.from({ length: numberOfForks }, async (_, i) => {
    const newInstance = await getSandbox(`${baseId}-fork-${i}`);
    return newInstance.start({ snapshot: snapshotId });
  });

  await Promise.all(forks);
}

```

快照存储在您账户内的 R2 中，为您提供持久性和位置独立性。R2 的分层缓存系统允许在全球范围内（Region: Earth）实现快速恢复。

在未来的版本中，还将捕获实时内存状态，允许正在运行的进程从上次中断的地方精确恢复。终端和编辑器将在上次关闭时的确切状态下重新打开。

如果您有兴趣在快照功能正式上线前恢复会话状态，现在就可以使用 `backup` 和 `restore` 方法。这些方法也使用 R2 来持久化和恢复目录，但性能不如真正的虚拟机级别快照。尽管如此，与简单地重新创建会话状态相比，它们仍然可以带来相当可观的速度提升。

启动一个沙盒、克隆 'axios' 并运行 npm install 需要 30 秒。从备份恢复只需要 2 秒。

请关注官方快照版本的发布。

## 更高的限制和活跃 CPU 定价

自最初发布以来，我们一直在稳步增加容量。我们标准定价计划的用户现在可以运行 15,000 个并发轻量级实例、6,000 个基础实例以及超过 1,000 个并发的大型实例。如需运行更多，请联系我们！

我们还更改了定价模型，使其在大规模运行时更具成本效益。沙盒现在仅对活跃使用的 CPU 周期收费。这意味着当您的 Agent（智能体）在等待 LLM（大语言模型）响应时，您无需为闲置的 CPU 付费。

## 这就是计算机应有的样子

九个月前，我们发布了一个可以运行命令和访问文件系统的沙盒。这足以证明概念。

我们现在拥有的东西在本质上已经不同。今天的沙盒是一个完整的开发环境：一个可以连接浏览器的终端、一个具有持久化状态的代码解释器、带有实时预览 URL 的后台进程、一个实时发出变更事件的文件系统、用于安全凭证注入的出口代理，以及一个使热启动几乎瞬间完成的快照机制。

当您在此基础上构建时，会出现一种令人满意的模式：执行真实工程工作的 Agent（智能体）。克隆仓库、安装、运行测试、读取失败信息、编辑代码、再次运行测试。这种让人类工程师高效工作的紧密反馈循环——现在 Agent（智能体）也能拥有了。

我们的 SDK 版本是 0.8.9。您今天就可以开始使用：

npm i @cloudflare/sandbox@latest

---

> 本文由AI自动翻译，原文链接：[Agents have their own computers with Sandboxes GA](https://blog.cloudflare.com/sandbox-ga/)
> 
> 翻译时间：2026-04-14 04:43
