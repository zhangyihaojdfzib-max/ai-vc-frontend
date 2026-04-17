---
title: Artifacts：专为AI智能体设计的Git版本化存储系统
title_original: 'Artifacts: versioned storage that speaks Git'
date: '2026-04-16'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/artifacts-git-for-agents-beta/
author: ''
summary: 本文介绍了Cloudflare推出的Artifacts，一个专为AI智能体构建的分布式、版本化文件系统。该系统基于Git数据模型，旨在解决传统源代码控制平台无法应对AI智能体大规模、自动化代码生成挑战的问题。Artifacts提供REST
  API和原生Workers API，支持动态创建仓库、导入现有项目、创建隔离分支等功能，使智能体、沙箱和无服务器函数能够高效地进行版本控制和状态持久化。
categories:
- AI基础设施
tags:
- Git
- 版本控制
- AI智能体
- 云存储
- Cloudflare
draft: false
translated_at: '2026-04-17T04:53:00.964446'
---

# Artifacts：支持 Git 的版本化存储

2026-04-16

- Dillon Mulroy
- Matt Carey
- Matt Silverlock

![](/images/posts/669fc5fb23a2.png)

Agent（智能体）已经改变了我们对源代码控制、文件系统和状态持久化的思考方式。开发者和Agent正在生成比以往更多的代码——未来5年编写的代码量将超过整个编程历史的总和——这推动了对满足此需求的系统规模产生数量级的变化。源代码控制平台在这方面尤其吃力：它们是为满足人类需求而构建的，而非为应对由永不睡眠、可同时处理多个问题且不知疲倦的Agent驱动的10倍量级变化。

我们认为需要一种新的基础构件：一个分布式、版本化的文件系统，它首先为Agent构建，并能服务于当今正在构建的各类应用程序。

我们称之为 Artifacts：一个支持 Git 的版本化文件系统。你可以通过编程方式创建仓库，与你的Agent、沙箱、Workers 或任何其他计算范式一起使用，并从任何常规 Git 客户端连接到它。

想为每个Agent会话分配一个仓库吗？Artifacts 可以做到。每个沙箱实例？同样可以用 Artifacts。想从一个已知良好的起点创建10,000个分支吗？你猜对了：还是 Artifacts。Artifacts 提供了 REST API 和原生 Workers API，用于在 Git 客户端不适用（例如在任何无服务器函数中）的环境中创建仓库、生成凭证和提交。

Artifacts 现已面向付费 Workers 计划的所有开发者开放私有测试版，我们的目标是在五月初将其作为公开测试版开放。

```Typescript
// 创建一个仓库
const repo = await env.AGENT_REPOS.create(name)
// 将令牌和远程地址传回给你的Agent
return { repo.remote, repo.token }
```

```Shell
# 克隆它，并像使用任何常规 git 远程仓库一样使用它
$ git clone https://x:${TOKEN}@123def456abc.artifacts.cloudflare.net/git/repo-13194.git

```

就是这样。一个裸仓库，随时可用，动态创建，任何 git 客户端都可以对其进行操作。

如果你想从现有的 git 仓库引导一个 Artifacts 仓库，以便你的Agent可以独立处理并推送独立的更改，你也可以通过 .import() 来实现：

```Typescript
interface Env {
  ARTIFACTS: Artifacts
}

export default {
  async fetch(request: Request, env: Env) {
    // 从 GitHub 导入
    const { remote, token } = await env.ARTIFACTS.import({
      source: {
        url: "https://github.com/cloudflare/workers-sdk",
        branch: "main",
      },
      target: {
        name: "workers-sdk",
      },
    })

    // 获取导入仓库的句柄
    const repo = await env.ARTIFACTS.get("workers-sdk")

    // 分叉到一个隔离的、只读的副本
    const fork = await repo.fork("workers-sdk-review", {
      readOnly: true,
    })

    return Response.json({ remote: fork.remote, token: fork.token })
  },
}
```

查看文档以开始使用，或者如果你想了解 Artifacts 如何被使用、它是如何构建的以及其底层工作原理：请继续阅读。

## 为什么是 Git？什么是版本化文件系统？

Agent了解 Git。它深植于大多数模型的训练数据中。Agent熟知其常规路径和边缘情况，并且针对代码优化的模型（和/或框架）特别擅长使用 git。

此外，Git 的数据模型不仅适用于源代码控制，也适用于任何需要跟踪状态、时间旅行和持久化大量小数据的场景。代码、配置、会话提示词和Agent历史记录：所有这些都是你通常希望以小数据块（"提交"）存储，并能够回退或回滚（"历史记录"）的东西（"对象"）。

我们本可以发明一个全新的、定制的协议……但那样你就会遇到引导问题。AI 模型不了解它，因此你必须分发技能、CLI，或者希望用户连接到你的文档 MCP……所有这些都会增加摩擦。

但是，如果我们能给Agent一个经过身份验证的、安全的 HTTPS Git 远程 URL，并让它们像操作 Git 仓库一样操作呢？事实证明这效果很好。而对于非 Git 客户端——例如 Cloudflare Worker、Lambda 函数或 Node.js 应用——我们提供了 REST API 和（即将推出的）特定语言 SDK。这些客户端也可以使用 `isomorphic-git`，但在许多情况下，一个更简单的 TypeScript API 可以减少所需的 API 表面。

### 不仅限于源代码控制

Artifacts 的 Git API 可能会让你认为它只用于源代码控制，但事实证明，Git API 和数据模型是一种强大的方式来持久化状态，允许你对任何数据进行分叉、时间旅行和状态差异比较。

在 Cloudflare 内部，我们正在为我们的内部Agent使用 Artifacts：自动将文件系统的当前状态和会话历史记录持久化在每个会话的 Artifacts 仓库中。这使我们能够：

- 持久化沙箱状态，而无需配置（和维护）块存储。
- 与他人共享会话，并允许他们通过会话（提示词）状态和文件状态进行时间旅行，无论是否对"实际"仓库（源代码控制）进行了提交。
- 最棒的是：从任意点分叉一个会话，允许我们的团队与同事共享会话，并让他们接手。正在调试某些东西并需要另一双眼睛？发送一个 URL 并分叉它。想对一个 API 进行即兴创作？让同事分叉它并从你离开的地方继续。

持久化沙箱状态，而无需配置（和维护）块存储。

与他人共享会话，并允许他们通过会话（提示词）状态和文件状态进行时间旅行，无论是否对"实际"仓库（源代码控制）进行了提交。

最棒的是：从任意点分叉一个会话，允许我们的团队与同事共享会话，并让他们接手。正在调试某些东西并需要另一双眼睛？发送一个 URL 并分叉它。想对一个 API 进行即兴创作？让同事分叉它并从你离开的地方继续。

我们还与一些团队交流过，他们希望在完全不需要 Git 协议，但需要其语义（回滚、克隆、差异比较）的场景中使用 Artifacts。将每个客户的配置作为产品的一部分存储，并希望拥有回滚能力？Artifacts 可以很好地表示这一点。

我们很高兴看到团队探索 Artifacts 的非 Git 用例，就像探索专注于 Git 的用例一样。

## 底层原理

Artifacts 构建在 Durable Objects 之上。创建数百万（或数千万+）个有状态、隔离的计算实例的能力是 Durable Objects 当前工作方式所固有的，而这正是我们支持每个命名空间数百万个 Git 仓库所需要的。

美国职业棒球大联盟（用于实时比赛分发）、Confluence Whiteboards 以及我们自己的 Agents SDK 都在大规模地使用 Durable Objects，因此我们正在一个我们已经生产环境中使用了一段时间的基础构件上构建此功能。

然而，我们确实需要一个可以在 Cloudflare Workers 上运行的 Git 实现。它需要小巧、尽可能完整、可扩展（支持 notes、LFS）且高效。因此，我们用 Zig 构建了一个，并将其编译为 Wasm。

为什么我们使用 Zig？三个原因：

1. 整个 git 协议引擎完全用纯 Zig 编写（无 libc），编译为约 100KB 的 WASM 二进制文件（仍有优化空间！）。它实现了 SHA-1、zlib 压缩/解压、增量编码/解码、包解析以及完整的 git 智能 HTTP 协议——全部从零开始，除了标准库外没有任何外部依赖。

2. Zig 让我们能够手动控制内存分配，这在 Durable Objects 这类受限环境中至关重要。Zig 构建系统使我们能够轻松地在 WASM 运行时（生产环境）和原生构建（针对 libgit2 进行正确性验证测试）之间共享代码。

3. WASM 模块通过一个精简的回调接口与 JS 宿主通信：11 个用于存储操作的主机导入函数（host_get_object、host_put_object 等）以及一个用于流式输出的函数（host_emit_bytes）。WASM 端可以完全独立地进行测试。

整个 git 协议引擎完全用纯 Zig 编写（无 libc），编译为约 100KB 的 WASM 二进制文件（仍有优化空间！）。它实现了 SHA-1、zlib 压缩/解压、增量编码/解码、包解析以及完整的 git 智能 HTTP 协议——全部从零开始，除了标准库外没有任何外部依赖。

Zig 让我们能够手动控制内存分配，这在 Durable Objects 这类受限环境中至关重要。Zig 构建系统使我们能够轻松地在 WASM 运行时（生产环境）和原生构建（针对 libgit2 进行正确性验证测试）之间共享代码。

WASM 模块通过一个精简的回调接口与 JS 宿主通信：11 个用于存储操作的主机导入函数（host_get_object、host_put_object 等）以及一个用于流式输出的函数（host_emit_bytes）。WASM 端可以完全独立地进行测试。

在底层，Artifacts 还使用了 R2（用于快照）和 KV（用于跟踪认证令牌）：

Artifacts 的工作原理（Workers、Durable Objects 和 WebAssembly）

一个 Worker 充当前端，处理身份验证与授权、关键指标（错误、延迟）并动态查找每个 Artifacts 仓库（Durable Object）。

具体来说：

- 文件存储在底层的 Durable Object 的 SQLite 数据库中。Durable Object 存储的单行数据最大为 2MB，因此大型 Git 对象会被分块并存储在多行中。我们使用了同步 KV API（state.storage.kv），其底层由 SQLite 支持。
- Durable Objects 有约 128MB 的内存限制：这意味着我们可以启动数千万个实例（它们快速且轻量），但必须在这些限制内工作。我们在 fetch 和 push 路径中都大量使用流式传输，直接返回由原始 WASM 输出块构建的 `ReadableStream<Uint8Array>`。我们避免自行计算 git 增量，而是将原始增量数据和基础哈希值与已解析的对象一起持久化存储。在 fetch 时，如果请求客户端已拥有基础对象，Zig 会发送增量数据而非完整对象，从而节省带宽和内存。
- 支持 git 协议的 v1 和 v2 版本。我们支持的功能包括 ls-refs、浅克隆（deepen、deepen-since、deepen-relative）以及通过 have/want 协商进行的增量获取。我们拥有广泛的测试套件，包括针对 git 客户端的符合性测试和针对 libgit2 服务器的验证测试，旨在验证协议支持。

文件存储在底层的 Durable Object 的 SQLite 数据库中。

- Durable Object 存储的单行数据最大为 2MB，因此大型 Git 对象会被分块并存储在多行中。
- 我们使用了同步 KV API（state.storage.kv），其底层由 SQLite 支持。

Durable Object 存储的单行数据最大为 2MB，因此大型 Git 对象会被分块并存储在多行中。

我们使用了同步 KV API（state.storage.kv），其底层由 SQLite 支持。

Durable Objects 有约 128MB 的内存限制：这意味着我们可以启动数千万个实例（它们快速且轻量），但必须在这些限制内工作。

- 我们在 fetch 和 push 路径中都大量使用流式传输，直接返回由原始 WASM 输出块构建的 `ReadableStream<Uint8Array>`。
- 我们避免自行计算 git 增量，而是将原始增量数据和基础哈希值与已解析的对象一起持久化存储。在 fetch 时，如果请求客户端已拥有基础对象，Zig 会发送增量数据而非完整对象，从而节省带宽和内存。

我们在 fetch 和 push 路径中都大量使用流式传输，直接返回由原始 WASM 输出块构建的 `ReadableStream<Uint8Array>`。

我们避免自行计算 git 增量，而是将原始增量数据和基础哈希值与已解析的对象一起持久化存储。在 fetch 时，如果请求客户端已拥有基础对象，Zig 会发送增量数据而非完整对象，从而节省带宽和内存。

支持 git 协议的 v1 和 v2 版本。

- 我们支持的功能包括 ls-refs、浅克隆（deepen、deepen-since、deepen-relative）以及通过 have/want 协商进行的增量获取。
- 我们拥有广泛的测试套件，包括针对 git 客户端的符合性测试和针对 libgit2 服务器的验证测试，旨在验证协议支持。

我们支持的功能包括 ls-refs、浅克隆（deepen、deepen-since、deepen-relative）以及通过 have/want 协商进行的增量获取。

我们拥有广泛的测试套件，包括针对 git 客户端的符合性测试和针对 libgit2 服务器的验证测试，旨在验证协议支持。

除此之外，我们还原生支持 git-notes。Artifacts 设计为 Agent（智能体）优先，而 notes 使 Agent（智能体）能够向 Git 对象添加注释（元数据）。这包括提示词、Agent（智能体）归属以及其他元数据，这些都可以从仓库中读取/写入，而无需修改对象本身。

## 大型仓库，大问题？认识 ArtifactFS。

大多数仓库并没有那么大，而且 Git 在设计上存储效率极高：大多数仓库最多只需几秒钟即可克隆，而这主要受网络设置时间、身份验证和校验和计算的影响。在大多数 Agent（智能体）或沙盒场景中，这是可行的：只需在沙盒启动时克隆仓库即可开始工作。

但是，对于多 GB 的仓库和/或拥有数百万个对象的仓库呢？我们如何能快速克隆该仓库，而不至于阻塞 Agent（智能体）数分钟无法工作并消耗计算资源？

一个流行的 Web 框架（2.4GB 且历史悠久！）克隆需要近 2 分钟。浅克隆更快，但不足以降到个位数秒，而且我们并不总是希望省略历史记录（Agent（智能体）发现它很有用）。

我们能否将大型仓库的克隆时间降至约 10-15 秒，以便我们的 Agent（智能体）可以开始工作？嗯，是的：通过一些技巧。

作为 Artifacts 发布的一部分，我们开源了 ArtifactFS，这是一个文件系统驱动程序，旨在尽可能快地挂载大型 Git 仓库，动态按需加载文件内容，而不是在初始克隆时阻塞。它非常适合 Agent（智能体）、沙盒、容器以及其他启动时间至关重要的用例。如果你能为每个大型仓库节省约 90-100 秒的沙盒启动时间，并且每月运行 10,000 个这样的沙盒任务：那么就能节省 2,778 个沙盒小时。

你可以将 ArtifactFS 视为“异步 Git 克隆”：

- ArtifactFS 运行一种无数据块（blobless）的 git 仓库克隆：它获取文件树和引用，但不获取文件内容。这可以在沙箱启动期间完成，从而让你的 Agent（智能体）框架可以开始工作。
- 在后台，它通过一个轻量级守护进程并发地开始水合（下载）文件内容。
- 它优先处理 Agent 通常首先需要操作的文件：包清单（package.json, go.mod）、配置文件和代码，并尽可能降低二进制数据块（图像、可执行文件和其他非文本文件）的优先级，以便 Agent 可以在文件本身被水合的同时扫描文件树。
- 如果 Agent 尝试读取文件时，该文件尚未完全水合，读取操作将会阻塞，直到水合完成。

文件系统不会尝试将文件“同步”回远程仓库：对于成千上万甚至数百万个对象，这通常非常慢，而且既然我们讨论的是 git，我们也不需要这样做。你的 Agent 只需要像操作任何仓库一样进行提交和推送。无需学习新的 API。

重要的是，ArtifactFS 适用于任何 Git 远程仓库，不仅仅是我们自己的 Artifacts。如果你正在从 GitHub、GitLab 或自托管的 Git 基础设施克隆大型仓库：你仍然可以使用 ArtifactFS。

## 即将推出什么？

我们今天发布的只是测试版，并且我们已经在开发一些功能，你将在未来几周内看到它们落地：

- 扩展我们公开的可用指标。今天我们发布了针对每个命名空间的关键操作计数、每个仓库的关键操作计数以及每个仓库的存储字节数的指标，以便管理数百万个 Artifact 不再繁琐。
- 支持仓库级别事件的**事件订阅**，这样我们就可以对命名空间内任何仓库的推送、拉取、克隆和分叉发出事件。这也将允许你消费事件、编写 webhook，并使用这些事件来通知最终用户、驱动产品内的生命周期事件，和/或运行推送后作业（如 CI/CD）。
- 用于与 Artifacts API 交互的原生 TypeScript、Go 和 Python 客户端 SDK。
- 仓库级别的搜索 API 和命名空间范围的搜索 API，例如“查找所有包含 `package.json` 文件的仓库”。

我们还在规划一个用于 **Workers Builds** 的 API，允许你在任何 Agent 驱动的工作流上运行 CI/CD 作业。

## 费用是多少？

我们的 Artifacts 服务仍处于早期阶段，但我们希望我们的定价能够适应 Agent 的规模：拥有数百万个仓库需要具有成本效益，未使用（或很少使用）的仓库不应成为负担，并且我们的定价应该与 Agent 的大规模单租户性质相匹配。

你也不应该需要考虑一个仓库是否会被使用、它是热数据还是冷数据、或者 Agent 是否会唤醒它。我们将根据你消耗的存储空间以及对每个仓库执行的操作（例如克隆、分叉、推送和拉取）向你收费。

**$/单位**

**包含**

**操作**

每 1,000 次操作 0.15 美元

每月前 10,000 次操作包含在内

**存储**

0.50 美元/GB-月

前 1GB 包含在内。

无论你拥有 1,000、100,000 还是 1000 万个仓库，大型、活跃的仓库将比小型、不常用的仓库花费更多。

随着测试版的推进，我们还将把 Artifacts 引入 Workers 免费计划（附带一些合理的限制），并且如果此定价发生变化或在开始对任何使用量计费之前，我们将在整个测试期间提供更新。

## 从哪里开始？

Artifacts 正在启动私有测试版，我们预计公开测试版将在五月初（明确一下，是 2026 年！）准备就绪。我们将在未来几周内逐步允许客户加入，你可以直接注册对私有测试版的兴趣。

同时，你可以通过以下方式了解更多关于 Artifacts 的信息：

- 阅读文档中的入门指南。
- 访问 Cloudflare 仪表板（Build > Storage & Databases > Artifacts）。
- 阅读 REST API 示例。
- 深入了解 Artifacts 的工作原理。

关注更新日志以跟踪测试版的进展。

## 在 Cloudflare TV 上观看

---

> 本文由AI自动翻译，原文链接：[Artifacts: versioned storage that speaks Git](https://blog.cloudflare.com/artifacts-git-for-agents-beta/)
> 
> 翻译时间：2026-04-17 04:53
