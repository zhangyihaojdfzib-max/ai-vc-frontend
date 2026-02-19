---
title: 我们如何将WebStreams性能提升10倍
title_original: We Ralph Wiggumed WebStreams to make them 10x faster - Vercel
date: '2026-02-18'
source: Vercel Blog
source_url: https://vercel.com/blog/we-ralph-wiggumed-webstreams-to-make-them-10x-faster
author: ''
summary: 本文介绍了Vercel团队针对Node.js中WebStreams API性能问题的优化工作。他们发现原生WebStreams在处理数据块时存在大量Promise分配和微任务跳转开销，导致其性能比传统Node.js流慢12倍。为此，团队开发了fast-webstreams库，通过底层使用优化的Node.js流并实现快速路径路由，在保持API兼容性的同时消除了常见情况下的Promise开销。最终，这项工作的部分优化已通过上游PR贡献给Node.js核心。
categories:
- AI基础设施
tags:
- WebStreams
- 性能优化
- Node.js
- Vercel
- 服务器端渲染
draft: false
translated_at: '2026-02-19T04:44:31.824618'
---

今年早些时候，当我们开始分析 Next.js 的服务端渲染性能时，火焰图中反复出现一个东西：WebStreams。不是运行在其中的应用程序代码，而是流本身。那些 Promise 链、每个数据块的对象分配、微任务队列的跳转。在 Theo Browne 的服务端渲染基准测试突显了框架开销占用了多少计算时间之后，我们开始探究这些时间具体花在了哪里。很大一部分就在流上。

事实证明，WebStreams 拥有一个极其完备的测试套件，这使得它们成为以纯测试驱动和基准驱动方式进行基于 AI 的重新实现的绝佳候选。这篇文章是关于我们所做的性能工作、我们的发现，以及这项工作如何通过 Matteo Collina 的上游 PR 已经进入 Node.js 本身。

## 问题所在

Node.js 有两套流式 API。较旧的一套（`stream.Readable`、`stream.Writable`、`stream.Transform`）已经存在了十多年，并且经过了深度优化。数据通过 C++ 内部机制流动。背压是一个布尔值。管道连接是一个单一的函数调用。

较新的一套是 WHATWG Streams API：`ReadableStream`、`WritableStream`、`TransformStream`。这是 Web 标准。它驱动着 `fetch()` 的响应体、`CompressionStream`、`TextDecoderStream`，并且越来越多地用于 Next.js 和 React 等框架的服务端渲染。

Web 标准是正确的、需要统一的 API。但在服务器端，它的速度比实际需要的要慢。

要理解原因，请考虑在 Node.js 中调用原生 WebStream 的 `reader.read()` 时会发生什么。即使数据已经存在于缓冲区中：

1.  会分配一个带有三个回调槽的 `ReadableStreamDefaultReadRequest` 对象
2.  该请求被排入流的内部队列
3.  分配并返回一个新的 Promise
4.  解析过程需要通过微任务队列

为了返回已经存在的数据，这需要四次分配和一次微任务跳转。现在，将这个开销乘以流经渲染管道中每个转换的每个数据块。

或者考虑 `pipeTo()`。每个数据块都要经过一个完整的 Promise 链：读取、写入、检查背压、重复。每次读取都会分配一个 `{value, done}` 结果对象。错误传播会创建额外的 Promise 分支。

这些做法本身没有错。在浏览器环境中，这些保证很重要，因为流会跨越安全边界，取消语义需要严密无缺，而且你无法控制管道的两端。但在服务器端，当你以 1KB 的数据块大小，通过三个转换来传输 React 服务器组件时，成本就会累积起来。

我们基准测试了原生 WebStream `pipeThrough` 对于 1KB 数据块的性能：**630 MB/s**。使用相同直通转换的 Node.js `pipeline()`：**~7,900 MB/s**。这是 12 倍的差距，而这个差异几乎完全来自 Promise 和对象分配的开销。

## 我们构建了什么

我们一直在开发一个名为 `fast-webstreams` 的库，它内部使用 Node.js 流来实现 WHATWG 的 `ReadableStream`、`WritableStream` 和 `TransformStream` API。相同的 API，相同的错误传播，相同的规范遵从性。对于常见情况，开销被消除了。

核心思想是根据你实际执行的操作，通过不同的快速路径来路由操作：

### 当你在快速流之间建立管道时：零 Promise

这是最大的收益。当你在快速流之间链接 `pipeThrough` 和 `pipeTo` 时，库不会立即开始管道传输。相反，它会记录上游链接：

source → transform1 → transform2 → ...

当在链的末端调用 `pipeTo()` 时，它会向上游遍历，收集底层的 Node.js 流对象，并发出一个单一的 `pipeline()` 调用。一个函数调用。每个数据块零 Promise。数据流经 Node.js 优化的 C++ 路径。

```
1const source = new ReadableStream({
2  pull(controller) {
3    controller.enqueue(generateChunk());
4  }
5});
6
7const transform = new TransformStream({
8  transform(chunk, controller) {
9    controller.enqueue(process(chunk));
10  }
11});
12
13const sink = new WritableStream({
14  write(chunk) { consume(chunk); }
15});
16
1718await source.pipeThrough(transform).pipeTo(sink);
```

结果：**~6,200 MB/s**。这比原生 WebStreams 快约 10 倍，接近原始 Node.js pipeline 的性能。

如果链中的任何流不是快速流（例如，原生的 `CompressionStream`），库会回退到原生的 `pipeThrough` 或一个符合规范的 `pipeTo` 实现。

### 当你逐块读取时：同步解析

当你调用 `reader.read()` 时，库会尝试同步调用 `nodeReadable.read()`。如果数据存在，你会得到 `Promise.resolve({value, done})`。无需事件循环往返。无需分配请求对象。只有当缓冲区为空时，它才会注册监听器并返回一个待定的 Promise。

```
1const reader = stream.getReader();
2while (true) {
3  const { value, done } = await reader.read();
4  if (done) break;
5  
6  
7  processChunk(value);
8}
```

结果：**~12,400 MB/s**，比原生快 3.7 倍。

### React Flight 模式：差距最大的地方

这对 Next.js 来说是最重要的。React 服务器组件使用一种特定的字节流模式：创建一个 `type: 'bytes'` 的 `ReadableStream`，在 `start()` 中捕获控制器，然后在渲染过程中从外部将数据块排入队列。

```
1let ctrl;
2const stream = new ReadableStream({
3  type: 'bytes',
4  start(c) { ctrl = c; }
5});
6
78ctrl.enqueue(new Uint8Array(payload1));
9ctrl.enqueue(new Uint8Array(payload2));
10ctrl.close();
```

原生 WebStreams：**~110 MB/s**。fast-webstreams：**~1,600 MB/s**。对于生产环境服务端渲染中使用的确切模式，这快了 **14.6 倍**。

速度的提升来自 `LiteReadable`，这是我们编写的一个基于数组的最小化缓冲区，用于替代 Node.js 的 `Readable` 处理字节流。它使用直接回调分发而不是 EventEmitter，支持基于拉取的需求和 BYOB 读取器，并且每次构建大约减少 5 微秒的开销。当 React Flight 每个请求创建数百个字节流时，这一点很重要。

### Fetch 响应体：非自行构造的流

上面的例子都以 `new ReadableStream(...)` 开始。但在服务器端，大多数流并非如此开始。它们始于 `fetch()`。响应体是由 Node.js 的 HTTP 层拥有的原生字节流。你无法替换它。

这是服务端渲染中的一个常见模式：从上游服务获取数据，将响应通过一个或多个转换进行管道传输，然后将结果转发给客户端。

```
1const upstream = await fetch('<https://api.example.com/data>');
2
34const transformed = upstream.body
5  .pipeThrough(new TransformStream({ transform(chunk, ctrl) {  ctrl.enqueue(chunk); } }))
6  .pipeThrough(new TransformStream({ transform(chunk, ctrl) {  ctrl.enqueue(chunk); } }))
7  .pipeThrough(new TransformStream({ transform(chunk, ctrl) {  ctrl.enqueue(chunk); } }));
8
9return new Response(transformed);
```

使用原生 WebStreams，此链中的每个跳转都要支付每个数据块的完整 Promise 成本。三个转换意味着每个数据块大约有 6-9 个 Promise。对于 1KB 的数据块，这只能达到 **~260 MB/s**。

该库通过延迟解析来处理这种情况。当 `patchGlobalWebStreams()` 激活时，`Response.prototype.body` 返回一个包装原生字节流的轻量级快速外壳。调用 `pipeThrough()` 不会立即开始管道传输。它只是记录链接。只有当在末端调用 `pipeTo()` 或 `getReader()` 时，库才会解析整个链：它创建一个从原生读取器到 Node.js `pipeline()` 的单一桥梁来处理转换跳转，然后同步地从缓冲的输出中提供读取。

成本模型：在原生边界处使用一个 Promise 来拉取数据。通过转换链时零 Promise。在输出端同步读取。

结果：在三种转换的获取模式中，速度约为 830 MB/s，比原生实现**快 3.2 倍**。对于没有转换的简单响应转发，速度**快 2.0 倍**（850 MB/s 对比 430 MB/s）。

## 基准测试

所有数字均为 Node.js v22 上 1KB 数据块的吞吐量（MB/s）。数值越高越好。

### 核心操作

| 操作 | Node.js 流 | 原生 | fast vs native |
| :--- | :--- | :--- | :--- |
| read 循环 | 26,400 | 12,400 | 3,300 |
| write 循环 | 26,500 | 5,500 | 2,300 |
| pipeThrough | 7,900 | 6,200 | 1.3x |
| pipeTo | 14,000 | 2,500 | 5.6x |
| for-await-of | 4,100 | 3,000 | 1.4x |

### 转换链

逐块 Promise 的开销会随着链的深度而叠加：

| 深度 | 3 个转换 | 2,900 | 2.8x |
| :--- | :--- | :--- | :--- |
| 8 个转换 | 1,000 | 8.0x |

### 字节流

| 模式 | start + enqueue (React Flight) | 1,600 | 14.6x |
| :--- | :--- | :--- | :--- |
| 字节读取循环 | 1,200 | 1.2x |
| 字节分流 | 1,200 | 1.2x |

### 响应体模式

| 模式 | Response.text() | 1,200 | 1.2x |
| :--- | :--- | :--- | :--- |
| 响应转发 | 850 | 2.0x |
| fetch → 3 个转换 | 830 | 3.2x |

### 流构造

创建流的速度也更快，这对于短生命周期的流很重要：

| 构造 | ReadableStream | 2,100 | 2.1x |
| :--- | :--- | :--- | :--- |
| WritableStream | 1,300 | 1.3x |
| TransformStream | 1,300 | 1.3x |

## 规范符合性

fast-webstreams 通过了 **1,100 项**（共 1,116 项）Web 平台测试。Node.js 的原生实现通过了 1,099 项。剩余的 16 项失败要么是与原生实现共有的（例如未实现的 `type: 'owning'` 传输模式），要么是不影响实际应用程序的架构差异。

## 我们如何部署此库

该库可以修补全局的 `ReadableStream`、`WritableStream` 和 `TransformStream` 构造函数：

```
1import { patchGlobalWebStreams } from 'fast-webstreams';2
3patchGlobalWebStreams();456
```

该补丁还会拦截 `Response.prototype.body`，将原生 fetch 响应体包装在 fast stream 外壳中，因此 `fetch()` → `pipeThrough()` → `pipeTo()` 链会自动进入快速路径管道。

在 Vercel，我们正在考虑在整个服务集群中推广此方案。我们将谨慎且逐步地进行。流原语位于请求处理、响应渲染和压缩的基础层。我们从差距最大的模式开始：React 服务器组件流式传输、响应体转发和多转换链。我们将在生产环境中进行测量，然后再进一步扩展。

## 正确的修复在于上游

一个用户态库不应该是这里的长期解决方案。正确的修复在于 Node.js 本身。

相关工作已经在进行中。在 X 上的一次讨论后，Matteo Collina 提交了 nodejs/node#61807，"stream: add fast paths for webstreams read and pipeTo"。该 PR 将此项目的两个想法直接应用到 Node.js 的原生 WebStreams 中：

1.  **`read()` 快速路径**：当数据已经缓冲时，直接返回一个已解决的 Promise，而无需创建 `ReadableStreamDefaultReadRequest` 对象。这是符合规范的，因为 `read()` 无论如何都会返回一个 Promise，而已解决的 Promise 仍然会在微任务队列中运行回调。
2.  **`pipeTo()` 批量读取**：当数据被缓冲时，从控制器队列中批量读取多个数据块，而无需为每个数据块创建请求对象。通过在每个写入后检查 `desiredSize` 来遵守背压。

该 PR 显示缓冲读取**快约 17-20%**，`pipeTo`**快约 11%**。这些改进将免费惠及所有 Node.js 用户。无需安装库，无需打补丁，没有风险。

James Snell 的 Node.js 性能问题 #134 概述了几个额外的机会：用于内部来源流的 C++ 级别管道、惰性缓冲、消除 WritableStream 适配器中的双重缓冲。每一项都可能进一步缩小差距。

我们将继续向上游贡献想法。目标不是让 fast-webstreams 永远存在。目标是让 WebStreams 足够快，以至于不再需要它。

## 我们艰难获得的经验

规范比看起来更聪明。我们尝试了许多捷径。几乎每一个都破坏了 Web 平台测试，而测试通常是对的。`ReadableStreamDefaultReadRequest` 模式、逐次读取的 Promise 设计、谨慎的错误传播：它们之所以存在，是因为读取期间的取消、通过锁定流的错误标识以及 thenable 拦截都是真实代码会遇到的实际边界情况。

`Promise.resolve(obj)` 总是检查 thenable。这是你无法避免的语言级行为。如果你用来解析的对象具有 `.then` 属性，Promise 机制将会调用它。一些 WPT 测试故意在读取结果上放置 `.then`，并验证流能正确处理它。我们必须在热路径中非常小心 `{value, done}` 对象的创建位置。

Node.js `pipeline()` 无法替代 WHATWG `pipeTo`。我们曾希望使用 `pipeline()` 进行所有管道操作。它导致了 72 项 WPT 失败。错误传播、流锁定和取消语义从根本上就不同。`pipeline()` 仅在我们控制整个链时才是安全的，这就是为什么我们收集上游链接并仅将其用于完整的 fast-stream 链。

使用 `Reflect.apply`，而不是 `.call()`。WPT 套件会猴子补丁 `Function.prototype.call`，并验证实现不使用它来调用用户提供的回调。`Reflect.apply` 是唯一安全的方式。这是一个真实的规范要求。

## 我们主要使用 AI 构建了 fast-webstreams

两件事使之成为可能：

出色的 **Web 平台测试**为我们提供了 1,116 项测试，作为对"我们是否破坏了什么？"这个问题的即时、机器可验证的答案。并且我们很早就构建了一个基准测试套件，以便能够衡量每次更改是否真的提高了吞吐量。开发循环是：实现优化 → 运行 WPT 套件 → 运行基准测试。当测试失败时，我们知道违反了哪条规范不变性。当基准测试没有变化时，我们就回退。

WHATWG Streams 规范冗长而密集。有趣的优化机会存在于规范*要求*的内容与当前实现*所做*的内容之间的差距中。`read()` 必须返回一个 Promise，但规范并未规定当数据已缓冲时，该 Promise 不能已经是已解决状态。当你能够要求 AI 分析算法步骤，找出在哪些地方可以用更少的分配来保持可观察行为时，这类观察就变得直接明了。

## 试试看

fast-webstreams 已在 npm 上以 **experimental-fast-webstreams** 的名称提供。"experimental" 前缀是有意为之的。我们对正确性有信心，但这是一个活跃开发的领域。

如果你正在构建服务器端 JavaScript 框架或运行时，并遇到了 WebStreams 的性能限制，我们很乐意听取你的意见。如果你有兴趣改进 Node.js 本身的 WebStreams，Matteo 的 PR 是一个很好的起点。

---

> 本文由AI自动翻译，原文链接：[We Ralph Wiggumed WebStreams to make them 10x faster - Vercel](https://vercel.com/blog/we-ralph-wiggumed-webstreams-to-make-them-10x-faster)
> 
> 翻译时间：2026-02-19 04:44
