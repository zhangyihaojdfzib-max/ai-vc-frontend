---
title: JavaScript 需要更好的流式 API
title_original: We deserve a better streams API for JavaScript
date: '2026-02-27'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/a-better-web-streams-api/
author: ''
summary: 本文批判性地分析了当前 WHATWG 流标准（Web 流）存在的根本性可用性和性能问题，指出其设计受限于 ES2018 之前缺乏异步迭代等语言特性的历史背景。作者提出了一种围绕现代
  JavaScript 语言原语构建的替代方案，该方案在多个主流运行时中的性能表现远超现有标准（快 2 到 120 倍），旨在引发关于未来流式 API 设计可能性的讨论。文章核心观点是，基于过时设计决策的
  API 已成为开发负担，我们值得拥有一个更简洁、高效且符合现代 JavaScript 开发模式的流式处理方案。
categories:
- 技术趋势
tags:
- JavaScript
- Web 标准
- 性能优化
- API 设计
- 流式处理
draft: false
translated_at: '2026-02-28T04:33:04.706792'
---

# 我们值得为 JavaScript 拥有更好的流式 API

2026-02-27

- James M Snell

![](/images/posts/08bf723125c7.png)

以流式方式处理数据是我们构建应用程序的基础。为了让流式处理能在各处工作，WHATWG 流标准（非正式地称为“Web 流”）旨在建立一个跨浏览器和服务器工作的通用 API。它已内置在浏览器中，并被 Cloudflare Workers、Node.js、Deno 和 Bun 采用，并成为 `fetch()` 等 API 的基础。这是一项重要的工作，设计它的人们在当时面临的约束和拥有的工具条件下，解决了许多难题。

但在基于 Web 流构建多年之后——在 Node.js 和 Cloudflare Workers 中实现它们，为客户和运行时调试生产问题，并帮助开发者解决太多常见陷阱——我开始相信，标准 API 存在根本性的可用性和性能问题，这些问题无法仅通过增量改进轻易修复。这些问题并非缺陷；它们是设计决策的结果，这些决策在十年前可能是有道理的，但与当今 JavaScript 开发者编写代码的方式不符。

这篇文章探讨了我所看到的 Web 流的一些根本问题，并提出了一种围绕 JavaScript 语言原语构建的替代方法，以证明更好的方案是可能的。

在基准测试中，这种替代方案在我测试过的每个运行时（包括 Cloudflare Workers、Node.js、Deno、Bun 和所有主流浏览器）中，其运行速度都比 Web 流快 2 倍到 120 倍不等。这些改进并非源于巧妙的优化，而是根本不同的设计选择，更有效地利用了现代 JavaScript 语言特性。我并非要贬低前人的工作；我是想开启一场关于未来可能性的对话。

## 我们的起点

流标准在 2014 年至 2016 年间制定，其雄心勃勃的目标是提供“用于创建、组合和使用数据流的 API，这些数据流能高效地映射到底层 I/O 原语”。在 Web 流出现之前，Web 平台没有处理流数据的标准方法。

当时 Node.js 已经拥有自己的流式 API，并且也被移植到浏览器中工作，但 WHATWG 选择不以其为起点，因为其章程规定只考虑 Web 浏览器的需求。服务器端运行时后来才采用 Web 流，这是在 Cloudflare Workers 和 Deno 各自出现并原生支持 Web 流，且跨运行时兼容性成为优先事项之后。

Web 流的设计早于 JavaScript 中的异步迭代。`for await...of` 语法直到 ES2018 才落地，这比流标准最初定稿晚了两年。这个时间点意味着该 API 最初无法利用后来成为 JavaScript 中消费异步序列的惯用方式。相反，规范引入了自己的读取器/写入器获取模型，而这个决定波及了 API 的方方面面。

#### 常见操作过于繁琐

使用流最常见的任务是将其读取到完成。以下是使用 Web 流的样子：

```JavaScript
// 首先，我们获取一个读取器，它赋予对流的独占锁...
const reader = stream.getReader();
const chunks = [];
try {
  // 其次，我们重复调用 read 并等待返回的 promise，
  // 以产生一个数据块或表明我们已经完成。
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    chunks.push(value);
  }
} finally {
  // 最后，我们释放流上的锁
  reader.releaseLock();
}
```

你可能会认为这种模式是流式处理固有的。其实不然。读取器获取、锁管理和 `{ value, done }` 协议都只是设计选择，而非必需。它们是 Web 流规范编写方式和时间的产物。异步迭代的存在正是为了处理随时间到达的序列，但在编写流规范时，异步迭代尚未存在。这里的复杂性纯粹是 API 开销，而非根本性必需。

考虑一下现在 Web 流确实支持 `for await...of` 的替代方法：

```JavaScript
const chunks = [];
for await (const chunk of stream) {
  chunks.push(chunk);
}
```

这更好，因为样板代码少得多，但它并不能解决所有问题。异步迭代被改造到一个并非为其设计的 API 上，这一点显而易见。像 BYOB（自带缓冲区）读取这样的功能无法通过迭代访问。读取器、锁和控制器的底层复杂性仍然存在，只是被隐藏了。当确实出现问题时，或者当需要 API 的额外功能时，开发者会发现自己又回到了原始 API 的复杂细节中，试图理解为什么他们的流被“锁定”，或者为什么 `releaseLock()` 没有按预期工作，或者在不受他们控制的代码中寻找瓶颈。

#### 锁定问题

Web 流使用锁定模型来防止多个消费者交错读取。当你调用 `getReader()` 时，流就会被锁定。在锁定状态下，其他任何代码都无法直接从流中读取、通过管道传输它，甚至取消它——只有实际持有读取器的代码可以。

这听起来很合理，直到你看到它多么容易出错：

```JavaScript
async function peekFirstChunk(stream) {
  const reader = stream.getReader();
  const { value } = await reader.read();
  // 糟糕——忘记调用 reader.releaseLock()
  // 并且当我们返回时，读取器不再可用
  return value;
}

const first = await peekFirstChunk(stream);
// TypeError: 无法获取锁——流被永久锁定
for await (const chunk of stream) { /* 永远不会运行 */ }
```

忘记 `releaseLock()` 会永久破坏流。`locked` 属性告诉你流被锁定，但不会告诉你原因、被谁锁定，或者锁是否仍然可用。管道操作在内部获取锁，使得流在管道操作期间以不明显的方式变得不可用。

关于释放带有待处理读取的锁的语义多年来也不明确。如果你调用了 read() 但没有等待它，然后调用了 releaseLock()，会发生什么？规范最近澄清为在锁释放时取消待处理的读取——但实现各不相同，依赖先前未指定行为的代码可能会中断。

话虽如此，重要的是要认识到锁定本身并非坏事。事实上，它确实服务于一个重要目的，即确保应用程序正确有序地消费或生产数据。关键挑战在于最初使用 `getReader()` 和 `releaseLock()` 等 API 的手动实现。随着异步可迭代对象自动锁和读取器管理的出现，从用户的角度处理锁变得容易得多。

对于实现者来说，锁定模型增加了相当多的非平凡内部簿记工作。每个操作都必须检查锁定状态，必须跟踪读取器，并且锁、取消和错误状态之间的相互作用产生了一系列必须正确处理的各种边界情况。

#### BYOB：付出复杂性却无回报

BYOB（自带缓冲区）读取旨在让开发者在从流中读取时重用内存缓冲区，这是为高吞吐量场景设计的一项重要优化。这个想法是合理的：不是为每个数据块分配新的缓冲区，而是提供你自己的缓冲区，由流来填充它。

实际上（是的，总会有例外情况），BYOB 很少被使用到能带来任何可衡量的好处。其 API 比默认读取要复杂得多，需要单独的读取器类型（`ReadableStreamBYOBReader`）和其他专门的类（例如 `ReadableStreamBYOBRequest`）、仔细的缓冲区生命周期管理，以及对 `ArrayBuffer` 分离语义的理解。当你将一个缓冲区传递给 BYOB 读取操作时，该缓冲区会变得分离——即被转移给流——而你得到的是一个可能指向不同内存的新视图。这种基于转移的模型容易出错且令人困惑：

```JavaScript
const reader = stream.getReader({ mode: 'byob' });
const buffer = new ArrayBuffer(1024);
let view = new Uint8Array(buffer);

const result = await reader.read(view);
// 'view' 现在应该已经分离且不可用
//（并非所有实现中总是如此）
// result.value 是一个新的视图，可能指向不同的内存
view = result.value; // 必须重新赋值
```

BYOB 也不能与异步迭代或 `TransformStream` 一起使用，因此希望实现零拷贝读取的开发者被迫回到手动读取器循环的模式。

对于实现者来说，BYOB 增加了显著的复杂性。流必须跟踪待处理的 BYOB 请求、处理部分填充、正确管理缓冲区分离，并在 BYOB 读取器与底层源之间进行协调。针对可读字节流的 Web 平台测试包含了专门针对 BYOB 边界情况的测试文件：分离的缓冲区、错误的视图、入队后的响应顺序等等。

BYOB 最终对用户和实现者来说都很复杂，但在实践中却很少被采用。大多数开发者坚持使用默认读取，并接受分配开销。

大多数用户态的自定义 `ReadableStream` 实例实现通常不会费心去正确地在一个流中同时实现默认读取和 BYOB 读取支持所需的所有繁琐步骤——这是有充分理由的。这很难做对，而且大部分耗时代码通常都会回退到默认读取路径。下面的例子展示了一个“正确”实现需要做的事情。它庞大、复杂且容易出错，这不是典型开发者真正愿意处理的复杂度级别：

```JavaScript
new ReadableStream({
    type: 'bytes',
    
    async pull(controller: ReadableByteStreamController) {      
      if (offset >= totalBytes) {
        controller.close();
        return;
      }
      
      // 首先检查 BYOB 请求
      const byobRequest = controller.byobRequest;
      
      if (byobRequest) {
        // === BYOB 路径 ===
        // 消费者提供了一个缓冲区 - 我们必须填充它（或部分填充）
        const view = byobRequest.view!;
        const bytesAvailable = totalBytes - offset;
        const bytesToWrite = Math.min(view.byteLength, bytesAvailable);
        
        // 在消费者的缓冲区上创建一个视图并填充它
        // 当 bytesToWrite != view.byteLength 时，这样做虽非必需但更安全
        const dest = new Uint8Array(
          view.buffer,
          view.byteOffset,
          bytesToWrite
        );
        
        // 用连续的字节填充（我们的“数据源”）
        // 这里可以是任何写入视图的操作
        for (let i = 0; i < bytesToWrite; i++) {
          dest[i] = (offset + i) & 0xFF;
        }
        
        offset += bytesToWrite;
        
        // 通知我们写入了多少字节
        byobRequest.respond(bytesToWrite);
        
      } else {
        // === 默认读取器路径 ===
        // 没有 BYOB 请求 - 分配并排队一个数据块
        const bytesAvailable = totalBytes - offset;
        const chunkSize = Math.min(1024, bytesAvailable);
        
        const chunk = new Uint8Array(chunkSize);
        for (let i = 0; i < chunkSize; i++) {
          chunk[i] = (offset + i) & 0xFF;
        }
        
        offset += chunkSize;
        controller.enqueue(chunk);
      }
    },
    
    cancel(reason) {
      console.log('Stream canceled:', reason);
    }
  });
```

当宿主运行时从运行时本身提供一个面向字节的 `ReadableStream` 时（例如，作为 fetch `Response` 的 `body`），运行时本身提供一个优化的 BYOB 读取实现通常要容易得多，但这些实现仍然需要能够处理默认和 BYOB 两种读取模式，而这个要求本身就带来了相当多的复杂性。

#### 背压：理论上很好，实践中失效

背压——即慢速消费者能够向快速生产者发出信号使其减速——是 Web 流中的一等概念。理论上如此。但在实践中，这个模型存在一些严重的缺陷。

主要的信号是控制器上的 `desiredSize`。它可以是正数（需要数据）、零（达到容量）、负数（超过容量）或 null（已关闭）。生产者应该检查这个值，并在其不为正时停止入队。但没有任何机制强制执行这一点：`controller.enqueue()` 总是成功，即使 `desiredSize` 是很大的负数。

```JavaScript
new ReadableStream({
  start(controller) {
    // 没有什么能阻止你这样做
    while (true) {
      controller.enqueue(generateData()); // desiredSize: -999999
    }
  }
});
```

流的实现可以也确实会忽略背压；并且一些规范定义的功能明确地破坏了背压。例如，`tee()` 从一个流创建两个分支。如果一个分支读取速度比另一个快，数据会在一个没有限制的内部缓冲区中累积。当慢速消费者追赶时，快速消费者可能导致无限制的内存增长，除了取消较慢的分支外，无法配置此行为或选择退出。

Web 流确实以 `highWaterMark` 选项和可定制的尺寸计算形式提供了调整背压行为的明确机制，但这些机制和 `desiredSize` 一样容易被忽略，许多应用程序根本不去关注它们。

同样的问题也存在于 `WritableStream` 端。一个 `WritableStream` 有 `highWaterMark` 和 `desiredSize`。有一个 `writer.ready` promise，数据的生产者应该关注它，但往往没有。

```JavaScript
const writable = getWritableStreamSomehow();
const writer = writable.getWriter();

// 生产者应该等待 writer.ready
// 它是一个 promise，当其解决时，表明
// 可写流的内部背压已清除，
// 可以写入更多数据了
await writer.ready;
await writer.write(...);
```

对于实现者来说，背压增加了复杂性却没有提供保证。必须正确实现跟踪队列大小、计算 `desiredSize` 以及在正确时间调用 `pull()` 的机制。然而，由于这些信号只是建议性的，所有这些工作实际上并不能防止背压本应解决的问题。

#### Promise 的隐藏成本

Web 流规范要求在多个点创建 promise，通常是在热点路径上，并且对用户通常是不可见的。每次 `read()` 调用不仅仅返回一个 promise；在内部，实现还会为队列管理、`pull()` 协调和背压信号创建额外的 promise。

这种开销是由规范依赖 promise 进行缓冲区管理、完成和背压信号所规定的。虽然其中一些是特定于实现的，但如果你按照规范编写的方式遵循，很多开销是不可避免的。对于高频流——视频帧、网络数据包、实时数据——这种开销是显著的。

这个问题在管道中会加剧。每个 `TransformStream` 都会在源和汇之间增加另一层 promise 机制。规范没有定义同步快速路径，因此即使数据立即可用，promise 机制仍然会运行。

对于实现者而言，这种重度依赖Promise的设计限制了优化空间。规范强制规定了特定的Promise解决顺序，使得批量操作或跳过不必要的异步边界变得困难，且可能引发难以察觉的合规性问题。虽然实现者确实会进行许多隐藏的内部优化，但这些优化往往复杂且难以正确实现。

在我撰写这篇博客文章时，Vercel的Malte Ubl发布了他们自己的博客文章，描述了Vercel在提升Node.js Web流实现性能方面的一些研究工作。他们在文章中讨论了每个Web流实现都面临的根本性性能优化问题：

"或者考虑pipeTo()。每个数据块都需要经过完整的Promise链：读取、写入、检查背压、重复。每次读取都会分配一个{value, done}结果对象。错误传播还会创建额外的Promise分支。

这些设计本身没有错。在浏览器环境中，这些保证至关重要——流可能跨越安全边界、取消语义必须严密、你无法控制管道的两端。但在服务器端，当你以1KB数据块的形式通过三个转换层传输React服务器组件时，这些开销就会累积。

我们对原生WebStream的pipeThrough进行了基准测试，处理1KB数据块时速度为630 MB/s。而使用相同直通转换的Node.js pipeline()速度约为7,900 MB/s。存在12倍的差距，这几乎完全是由Promise和对象分配开销造成的。"
- Malte Ubl, https://vercel.com/blog/we-ralph-wiggumed-webstreams-to-make-them-10x-faster

作为研究的一部分，他们为Node.js的Web流实现提出了一系列改进方案，将在特定代码路径中消除Promise的使用，从而带来高达10倍的显著性能提升。这恰恰证明：Promise虽然有用，但会带来显著开销。作为Node.js的核心维护者之一，我期待帮助Malte和Vercel团队落地这些改进方案！

在最近对Cloudflare Workers的更新中，我对内部数据管道进行了类似修改，在某些应用场景中将创建的JavaScript Promise数量减少了高达200倍。这使得相关应用的性能获得了数量级的提升。

### 现实中的故障案例

#### 未消费响应体导致的资源耗尽

当`fetch()`返回响应时，响应体是一个`ReadableStream`。如果只检查状态而不消费或取消响应体，会发生什么？具体表现因实现而异，但常见后果是资源泄漏。

```JavaScript
async function checkEndpoint(url) {
  const response = await fetch(url);
  return response.ok; // 响应体从未被消费或取消
}

// 在循环中执行可能导致连接池耗尽
for (const url of urls) {
  await checkEndpoint(url);
}
```

这种模式在使用undici（Node.js内置的`fetch()`实现）的Node.js应用中曾导致连接池耗尽，其他运行时也出现过类似问题。流会持有底层连接的引用，如果没有显式消费或取消，连接可能会一直保留直到垃圾回收——而在高负载下，垃圾回收可能不会及时发生。

某些API会隐式创建流分支，使问题更加复杂。`Request.clone()`和`Response.clone()`会对响应体流执行隐式的`tee()`操作——这个细节很容易被忽略。为日志记录或重试逻辑而克隆请求的代码，可能会在不知情的情况下创建需要独立消费的分支流，从而成倍增加资源管理负担。

需要明确的是，这类问题属于实现缺陷。连接泄漏确实是undici需要在其实现中修复的问题，但规范的复杂性使得处理这类问题并不容易。

"在Node.js的fetch()实现中克隆流比看起来更复杂。当你克隆请求或响应体时，实际上是在调用tee()——这会将单个流拆分为两个需要同时消费的分支。如果一个消费者读取速度比另一个快，数据就会在内存中无限制地缓冲，等待慢速分支。如果没有正确消费两个分支，底层连接就会泄漏。两个读取器共享同一源所需的协调机制，很容易意外破坏原始请求或耗尽连接池。这是一个看似简单的API调用，但其底层机制复杂且难以正确实现。" - Matteo Collina博士 - Platformatic联合创始人兼CTO，Node.js技术指导委员会主席

#### 从tee()内存悬崖跌落

`tee()`将流拆分为两个分支。这看似简单，但实现需要缓冲机制：如果一个分支读取速度快于另一个，数据必须暂存直到慢速分支赶上。

```JavaScript
const [forHash, forStorage] = response.body.tee();

// 哈希计算很快
const hash = await computeHash(forHash);

// 存储写入很慢——在此期间，整个流
// 可能都在内存中缓冲等待这个分支
await writeToStorage(forStorage);
```

规范没有为`tee()`规定缓冲限制。公平地说，规范允许实现以任何他们认为合适的方式实现`tee()`和其他API的实际内部机制，只要满足规范的可观察规范性要求。但如果实现选择按照流规范描述的具体方式实现`tee()`，那么`tee()`就会带来固有的内存管理问题，且难以规避。

各实现不得不制定自己的应对策略。Firefox最初采用链表方式，导致内存增长与消费速率差成O(n)比例。在Cloudflare Workers中，我们选择实现共享缓冲模型，由最慢的消费者而非最快的消费者发出背压信号。

#### 转换流的背压间隙

`TransformStream`创建了一对可读/可写端，中间包含处理逻辑。`transform()`函数在写入时执行，而非读取时。无论消费者是否就绪，数据到达时转换处理都会立即进行。当消费者处理缓慢时，这会导致不必要的工作负载，且两端之间的背压信号传递存在间隙，在高负载下可能造成无限制缓冲。规范期望数据生产者关注转换流可写端的`writer.ready`信号，但生产者往往直接忽略该信号。

如果转换的`transform()`操作是同步的且总是立即将输出加入队列，即使下游消费者处理缓慢，它也永远不会向可写端传递背压信号。这是许多开发者完全忽视的规范设计后果。在浏览器环境中，通常只有单一用户且任意时刻只有少量流管道处于活动状态，这类隐患往往无关紧要。但在服务数千并发请求的服务器端或边缘运行时中，这会对性能产生重大影响。

```JavaScript
const fastTransform = new TransformStream({
  transform(chunk, controller) {
    // 同步加入队列——这永远不会施加背压
    // 即使可读端缓冲区已满，操作仍会成功
    controller.enqueue(processChunk(chunk));
  }
});

// 将快速源通过转换流传输到慢速接收端
fastSource
  .pipeThrough(fastTransform)
  .pipeTo(slowSink);  // 缓冲区无限制增长
```

TransformStream本应检查控制器上的背压，并使用Promise将背压信号传递回写入端：

```JavaScript
const fastTransform = new TransformStream({
  async transform(chunk, controller) {
    if (controller.desiredSize <= 0) {
      // 以某种方式等待背压消除
    }

    controller.enqueue(processChunk(chunk));
  }
});
```

然而，这里的一个难点是，`TransformStreamDefaultController` 不像 Writer 那样拥有就绪（ready）Promise 机制；因此 `TransformStream` 的实现需要实现一个轮询机制，来定期检查 `controller.desiredSize` 何时再次变为正值。

在管道中，问题会变得更糟。当你链接多个转换流时——例如，解析、转换，然后序列化——每个 `TransformStream` 都有其内部的可读和可写缓冲区。如果实现者严格遵循规范，数据会以面向推送（push-oriented）的方式在这些缓冲区中逐级流动：源数据推送到转换流 A，A 推送到 B，B 推送到 C，每个转换流都在最终消费者开始拉取之前，在中间缓冲区中积累数据。对于三个转换流，你可能会同时有六个内部缓冲区被填满。

使用流 API 的开发者被期望记住在创建源、转换流和可写目标时使用诸如 `highWaterMark` 之类的选项，但他们常常要么忘记，要么干脆选择忽略它。

```JavaScript
source
  .pipeThrough(parse)      // 缓冲区正在填充...
  .pipeThrough(transform)  // 更多缓冲区正在填充...
  .pipeThrough(serialize)  // 甚至更多缓冲区...
  .pipeTo(destination);    // 消费者尚未开始
```

各实现已经找到了优化转换流管道的方法，例如折叠恒等转换、短路不可观测的路径、延迟缓冲区分配，或者回退到完全不运行 JavaScript 的本地代码。Deno、Bun 和 Cloudflare Workers 都已成功实现了“本地路径”优化，这有助于消除大部分开销，而 Vercel 最近的 `fast-webstreams` 研究也正在为 Node.js 进行类似的优化。但这些优化本身增加了显著的复杂性，并且仍然无法完全摆脱 TransformStream 使用的固有的面向推送的模型。

#### 服务器端渲染中的 GC 抖动

流式服务器端渲染（SSR）是一个特别棘手的情况。典型的 SSR 流可能会渲染数千个小的 HTML 片段，每个片段都会经过流处理机制：

```JavaScript
// 每个组件入队一个小数据块
function renderComponent(controller) {
  controller.enqueue(encoder.encode(`<div>${content}</div>`));
}

// 数百个组件 = 数百次 enqueue 调用
// 每次调用都会在内部触发 Promise 机制
for (const component of components) {
  renderComponent(controller);  // 创建 Promise，分配对象
}
```

每个片段都意味着为 `read()` 调用创建 Promise、为背压协调创建 Promise、分配中间缓冲区以及创建 `{ value, done }` 结果对象——其中大多数几乎立即变成了垃圾。

在高负载下，这会产生 GC 压力，可能严重降低吞吐量。JavaScript 引擎花费大量时间收集短命对象，而不是做有用的工作。由于 GC 暂停会中断请求处理，延迟变得不可预测。我曾见过一些 SSR 工作负载，其中垃圾收集占用了每个请求总 CPU 时间的相当大一部分（高达甚至超过 50%）。这些时间本可以用来实际渲染内容。

讽刺的是，流式 SSR 本应通过增量发送内容来提高性能。但流处理机制的开销可能会抵消这些收益，特别是对于包含许多小组件的页面。开发者有时会发现，缓冲整个响应实际上比通过 Web 流进行流式传输更快，这完全违背了初衷。

### 优化困境

为了获得可用的性能，每个主要的运行时都不得不对 Web 流采用非标准的内部优化。Node.js、Deno、Bun 和 Cloudflare Workers 都开发了自己的变通方案。对于连接到系统级 I/O 的流来说尤其如此，因为其中大部分机制是不可观测的，并且可以被短路。

寻找这些优化机会本身可能是一项艰巨的任务。它需要对规范有端到端的理解，以识别哪些行为是可观测的，哪些可以安全地省略。即便如此，给定的优化是否真正符合规范也常常不清楚。实现者必须做出判断，决定可以放宽哪些语义而不破坏兼容性。这给运行时团队带来了巨大压力，他们必须成为规范专家，才能获得可接受的性能。

这些优化难以实现，常常容易出错，并导致不同运行时之间的行为不一致。Bun 的“直接流”（Direct Streams）优化采取了一种刻意且可观测的非标准方法，完全绕过了规范的大部分机制。Cloudflare Workers 的 `IdentityTransformStream` 为直通转换提供了快速路径，但它是 Workers 特有的，并且实现的行为并非 `TransformStream` 的标准行为。每个运行时都有自己的技巧集，自然的趋势是走向非标准解决方案，因为这通常是使事情变快的唯一途径。

这种碎片化损害了可移植性。在一个运行时上表现良好的代码，在另一个运行时上可能表现不同（或很差），即使它使用的是“标准”API。运行时实现者的复杂性负担是巨大的，而微妙的行为差异给试图编写跨运行时代码的开发者带来了摩擦，特别是对于那些维护必须在许多运行时环境中高效运行的框架的开发者。

同样有必要强调的是，许多优化只有在规范中用户代码不可观测的部分才有可能实现。另一种选择，如 Bun 的“直接流”，是故意偏离规范定义的可观测行为。这意味着优化常常感觉“不完整”。它们在某些场景下有效，但在其他场景下无效；在某些运行时有效，但在其他运行时无效，等等。每一个这样的案例都增加了 Web 流方法整体上不可持续的复杂性，这就是为什么大多数运行时实现者一旦通过一致性测试，就很少投入大量精力进一步改进他们的流实现。

实现者不应该需要经历这些麻烦。当你发现自己需要放宽或绕过规范语义才能获得合理的性能时，这表明规范本身存在问题。一个设计良好的流式 API 应该默认就是高效的，而不需要每个运行时都发明自己的逃生舱口。

### 合规负担

复杂的规范会产生复杂的边缘情况。Web 流的 **Web Platform Tests** 涵盖了超过 70 个测试文件，虽然全面的测试是件好事，但真正说明问题的是需要测试什么。

考虑一些实现必须通过的更晦涩的测试：

- **原型污染防御**：一项测试通过修补 `Object.prototype.then` 来拦截 Promise 的解析，然后验证 `pipeTo()` 和 `tee()` 操作不会通过原型链泄露内部值。这测试了一个仅因规范中大量使用 Promise 的内部机制而存在的攻击面所引发的安全特性。
- **WebAssembly 内存拒绝**：BYOB 读取操作必须明确拒绝由 WebAssembly 内存支持的 ArrayBuffer，这些 ArrayBuffer 看起来像常规缓冲区但无法传输。这个边缘情况的存在是由于规范的缓冲区分离模型——一个更简单的 API 本不需要处理它。
- **状态机冲突导致的崩溃回归**：一项测试专门检查在 `enqueue()` 之后调用 `byobRequest.respond()` 不会导致运行时崩溃。这个操作序列会在内部状态机中产生冲突——`enqueue()` 会完成待处理的读取并使 `byobRequest` 失效，但实现必须优雅地处理后续的 `respond()` 调用，而不是破坏内存，以覆盖开发者很可能没有正确使用这个复杂 API 的可能性。

这些并非测试作者凭空臆造的场景。它们是规范设计的后果，并反映了现实世界中的错误。

对于运行时实现者而言，通过 WPT 测试套件意味着要处理大多数应用程序代码永远不会遇到的复杂边缘情况。这些测试不仅编码了理想路径，还编码了读取器、写入器、控制器、队列、策略以及连接它们的所有 Promise 机制之间完整的交互矩阵。

一个更简单的 API 将意味着更少的概念、概念间更少的交互以及需要正确处理更少的边缘情况，从而更有信心确保实现的行为真正一致。

### 要点

Web 流对用户和实现者来说都很复杂。规范的问题并非错误。它们是在完全按照设计使用 API 时出现的。它们不是仅通过渐进式改进就能解决的问题。它们是基本设计选择的后果。要改进现状，我们需要不同的基础。

## 一个更好的流 API 是可能的

在不同运行时中多次实现 Web 流规范并亲眼目睹痛点之后，我决定是时候探索一下，如果今天从第一性原理出发设计，一个更好的、替代性的流 API 会是什么样子。

以下是一个概念验证：它不是一个完成的标准，不是一个可用于生产的库，甚至不一定是一个具体的新提案，而是一个讨论的起点，旨在证明 Web 流的问题并非流处理本身固有的；它们是特定设计选择的后果，而这些选择本可以不同。这个确切的 API 是否是正确答案，不如它是否能引发一场关于我们真正需要什么样的流处理原语的富有成效的讨论来得重要。

### 什么是流？

在深入 API 设计之前，值得一问：什么是流？

流的核心只是一个随时间到达的数据序列。你无法一次性获得全部数据。你需要在数据可用时逐步处理它。

Unix 管道或许是这个理念最纯粹的表达：

```Shell
cat access.log | grep "error" | sort | uniq -c
```

数据从左向右流动。每个阶段读取输入，执行其工作，写入输出。没有需要获取的管道读取器，没有需要管理的控制器锁。如果下游阶段速度慢，上游阶段自然也会减慢。反压隐含在模型中，而不是一个需要学习（或忽略）的独立机制。

在 JavaScript 中，"随时间到达的事物序列" 的自然原语已经存在于语言中：异步可迭代对象。你可以使用 `for await...of` 来消费它。通过停止迭代来停止消费。

这就是新 API 试图保留的直觉：流应该感觉像迭代，因为它们本来就是。Web 流的复杂性——读取器、写入器、控制器、锁、队列策略——掩盖了这种根本的简单性。一个更好的 API 应该让简单的情况变得简单，并且只在真正需要的地方增加复杂性。

### 设计原则

我围绕一套不同的原则构建了这个概念验证的替代方案。

#### 流是可迭代对象。

没有带有隐藏内部状态的自定义 `ReadableStream` 类。一个可读流就是一个 `AsyncIterable<Uint8Array[]>`。你用 `for await...of` 来消费它。无需获取读取器，无需管理锁。

#### 拉取式转换

转换操作直到消费者拉取时才执行。没有急切求值，没有隐藏的缓冲。数据按需从源头流经转换，到达消费者。如果你停止迭代，处理就停止。

#### 显式反压

反压默认是严格的。当缓冲区满时，写入操作会拒绝，而不是默默地累积。你可以配置替代策略——阻塞直到有可用空间、丢弃最旧的、丢弃最新的——但你必须明确选择。不再有静默的内存增长。

#### 批量块

流不是每次迭代产生一个块，而是产生 `Uint8Array[]`：块的数组。这可以将异步开销分摊到多个块上，减少热点路径中的 Promise 创建和微任务延迟。

#### 仅处理字节

该 API 专门处理字节（`Uint8Array`）。字符串会自动进行 UTF-8 编码。没有"值流"与"字节流"的二分法。如果你想流式传输任意的 JavaScript 值，请直接使用异步可迭代对象。虽然 API 使用 `Uint8Array`，但它将块视为不透明的。没有部分消费，没有 BYOB 模式，没有流处理机制内部的字节级操作。块进去，块出来，除非转换器明确修改它们，否则保持不变。

#### 同步快速路径很重要

该 API 认识到同步数据源既是必要的也是常见的。应用程序不应仅仅因为这是提供的唯一选项，就被迫总是接受异步调度的性能成本。同时，混合同步和异步处理可能是危险的。同步路径应该始终是一个选项，并且应该始终是显式的。

### 新 API 实战

#### 创建和消费流

在 Web 流中，创建一个简单的生产者/消费者对需要 `TransformStream`、手动编码和仔细的锁管理：

```JavaScript
const { readable, writable } = new TransformStream();
const enc = new TextEncoder();
const writer = writable.getWriter();
await writer.write(enc.encode("Hello, World!"));
await writer.close();
writer.releaseLock();

const dec = new TextDecoder();
let text = '';
for await (const chunk of readable) {
  text += dec.decode(chunk, { stream: true });
}
text += dec.decode();
```

即使这个相对简洁的版本也需要：一个 `TransformStream`、手动的 `TextEncoder` 和 `TextDecoder`，以及显式的锁释放。

以下是新API的等效实现：

```JavaScript
import { Stream } from 'new-streams';

// 创建推送流
const { writer, readable } = Stream.push();

// 写入数据 —— 背压机制会强制执行
await writer.write("Hello, World!");
await writer.end();

// 作为文本消费
const text = await Stream.text(readable);
```

`readable` 只是一个异步可迭代对象。你可以将其传递给任何期望此类对象的函数，包括 `Stream.text()`，它会收集并解码整个流。

写入器（writer）具有简单的接口：用于写入的 `write()`、用于批量写入的 `writev()`、用于表示完成的 `end()` 以及用于处理错误的 `abort()`。基本上就是这样。

写入器不是一个具体的类。任何实现了 `write()`、`end()` 和 `abort()` 方法的对象都可以作为写入器，这使得适配现有API或创建专门的实现变得容易，而无需继承。没有复杂的 `UnderlyingSink` 协议，该协议包含必须通过一个控制器来协调的 `start()`、`write()`、`close()` 和 `abort()` 回调，而该控制器的生命周期和状态独立于它所绑定的 `WritableStream`。

以下是一个简单的内存写入器，用于收集所有写入的数据：

```JavaScript
// 一个最小的写入器实现 —— 只是一个包含方法的对象
function createBufferWriter() {
  const chunks = [];
  let totalBytes = 0;
  let closed = false;

  const addChunk = (chunk) => {
    chunks.push(chunk);
    totalBytes += chunk.byteLength;
  };

  return {
    get desiredSize() { return closed ? null : 1; },

    // 异步版本
    write(chunk) { addChunk(chunk); },
    writev(batch) { for (const c of batch) addChunk(c); },
    end() { closed = true; return totalBytes; },
    abort(reason) { closed = true; chunks.length = 0; },

    // 同步版本返回布尔值（true = 已接受）
    writeSync(chunk) { addChunk(chunk); return true; },
    writevSync(batch) { for (const c of batch) addChunk(c); return true; },
    endSync() { closed = true; return totalBytes; },
    abortSync(reason) { closed = true; chunks.length = 0; return true; },

    getChunks() { return chunks; }
  };
}

// 使用它
const writer = createBufferWriter();
await Stream.pipeTo(source, writer);
const allData = writer.getChunks();
```

无需扩展基类，无需实现抽象方法，无需与控制器协调。只是一个具有正确形状的对象。

在新的API设计中，转换器（transform）在数据被消费之前不应执行任何工作。这是一个基本原则。

```JavaScript
// 在迭代开始之前，不会执行任何操作
const output = Stream.pull(source, compress, encrypt);

// 转换器在我们迭代时执行
for await (const chunks of output) {
  for (const chunk of chunks) {
    process(chunk);
  }
}
```

`Stream.pull()` 创建一个惰性管道。`compress` 和 `encrypt` 转换器直到你开始迭代 `output` 时才会运行。每次迭代都会按需从管道中拉取数据。

这与Web流的 `pipeThrough()` 有根本性的不同，后者在你设置管道后就会立即开始主动将数据从源推送到转换器。拉取语义意味着你控制处理何时发生，停止迭代就会停止处理。

转换器可以是无状态的或有状态的。无状态转换器只是一个接收数据块并返回转换后数据块的函数：

```JavaScript
// 无状态转换器 —— 一个纯函数
// 接收数据块或 null（刷新信号）
const toUpperCase = (chunks) => {
  if (chunks === null) return null; // 流结束
  return chunks.map(chunk => {
    const str = new TextDecoder().decode(chunk);
    return new TextEncoder().encode(str.toUpperCase());
  });
};

// 直接使用它
const output = Stream.pull(source, toUpperCase);
```

有状态转换器是具有成员函数的简单对象，这些函数在多次调用之间维护状态：

```JavaScript
// 有状态转换器 —— 一个包装源的生成器
function createLineParser() {
  // 用于连接 Uint8Arrays 的辅助函数
  const concat = (...arrays) => {
    const result = new Uint8Array(arrays.reduce((n, a) => n + a.length, 0));
    let offset = 0;
    for (const arr of arrays) { result.set(arr, offset); offset += arr.length; }
    return result;
  };

  return {
    async *transform(source) {
      let pending = new Uint8Array(0);
      
      for await (const chunks of source) {
        if (chunks === null) {
          // 刷新：产出任何剩余的数据
          if (pending.length > 0) yield [pending];
          continue;
        }
        
        // 将待处理数据与新数据块连接起来
        const combined = concat(pending, ...chunks);
        const lines = [];
        let start = 0;

        for (let i = 0; i < combined.length; i++) {
          if (combined[i] === 0x0a) { // 换行符
            lines.push(combined.slice(start, i));
            start = i + 1;
          }
        }

        pending = combined.slice(start);
        if (lines.length > 0) yield lines;
      }
    }
  };
}

const output = Stream.pull(source, createLineParser());
```

对于需要在终止时进行清理的转换器，添加一个终止处理器：

```JavaScript
// 具有资源清理功能的有状态转换器
function createGzipCompressor() {
  // 假设的压缩 API...
  const deflate = new Deflater({ gzip: true });

  return {
    async *transform(source) {
      for await (const chunks of source) {
        if (chunks === null) {
          // 刷新：完成压缩
          deflate.push(new Uint8Array(0), true);
          if (deflate.result) yield [deflate.result];
        } else {
          for (const chunk of chunks) {
            deflate.push(chunk, false);
            if (deflate.result) yield [deflate.result];
          }
        }
      }
    },
    abort(reason) {
      // 在错误/取消时清理压缩器资源
    }
  };
}
```

对于实现者来说，没有 `Transformer` 协议，该协议包含 `start()`、`transform()`、`flush()` 方法以及传递给 `TransformStream` 类的控制器协调机制，而该类有其自身隐藏的状态机和缓冲机制。转换器只是函数或简单对象：实现和测试要简单得多。

#### 显式的背压策略

当有界缓冲区已满且生产者想要写入更多数据时，你只有几种选择：

1.  拒绝写入：拒绝接受更多数据
2.  等待：阻塞直到有可用空间
3.  丢弃旧数据：驱逐已缓冲的数据以腾出空间
4.  丢弃新数据：丢弃传入的数据

拒绝写入：拒绝接受更多数据

等待：阻塞直到有可用空间

丢弃旧数据：驱逐已缓冲的数据以腾出空间

丢弃新数据：丢弃传入的数据

就是这样。任何其他响应要么是这些的变体（如“调整缓冲区大小”，这实际上只是推迟了选择），要么是不属于通用流原语的特定领域逻辑。Web流目前默认总是选择“等待”。

新API要求你明确选择以下四种策略之一：

-   `strict`（默认）：当缓冲区已满且太多写入操作挂起时，拒绝写入。用于捕获生产者忽略背压的“发射后不管”模式。
-   `block`：写入操作等待直到缓冲区有可用空间。当你信任生产者会正确等待写入时使用。
-   `drop-oldest`：丢弃最旧的缓冲数据以腾出空间。适用于实时数据流，其中过时的数据会失去价值。
-   `drop-newest`：当缓冲区满时丢弃传入的数据。适用于你希望处理已有数据而不被淹没的情况。

`strict`（默认）：当缓冲区已满且太多写入操作挂起时，拒绝写入。用于捕获生产者忽略背压的“发射后不管”模式。

`block`：写入操作等待直到缓冲区有可用空间。当你信任生产者会正确等待写入时使用。

`drop-oldest`：丢弃最旧的缓冲数据以腾出空间。适用于实时数据流，其中过时的数据会失去价值。

`drop-newest`：当缓冲区满时丢弃传入的数据。适用于你希望处理已有数据而不被淹没的情况。

```JavaScript
const { writer, readable } = Stream.push({
  highWaterMark: 10,
  backpressure: 'strict' // 或 'block', 'drop-oldest', 'drop-newest'
});
```

无需再寄希望于生产者配合。您选择的策略决定了缓冲区满时的处理方式。

以下是当生产者写入速度快于消费者读取时，每种策略的行为：

```JavaScript
// strict: 捕获那些忽略背压的"发射后不管"式写入
const strict = Stream.push({ highWaterMark: 2, backpressure: 'strict' });
strict.writer.write(chunk1);  // 正常（未等待）
strict.writer.write(chunk2);  // 正常（填满槽位缓冲区）
strict.writer.write(chunk3);  // 正常（进入待处理队列）
strict.writer.write(chunk4);  // 正常（待处理缓冲区填满）
strict.writer.write(chunk5);  // 抛出错误！待处理写入过多

// block: 等待空间（无界待处理队列）
const blocking = Stream.push({ highWaterMark: 2, backpressure: 'block' });
await blocking.writer.write(chunk1);  // 正常
await blocking.writer.write(chunk2);  // 正常
await blocking.writer.write(chunk3);  // 等待消费者读取
await blocking.writer.write(chunk4);  // 等待消费者读取
await blocking.writer.write(chunk5);  // 等待消费者读取

// drop-oldest: 丢弃旧数据以腾出空间
const dropOld = Stream.push({ highWaterMark: 2, backpressure: 'drop-oldest' });
await dropOld.writer.write(chunk1);  // 正常
await dropOld.writer.write(chunk2);  // 正常
await dropOld.writer.write(chunk3);  // 正常，chunk1 被丢弃

// drop-newest: 缓冲区满时丢弃新数据
const dropNew = Stream.push({ highWaterMark: 2, backpressure: 'drop-newest' });
await dropNew.writer.write(chunk1);  // 正常
await dropNew.writer.write(chunk2);  // 正常
await dropNew.writer.write(chunk3);  // 被静默丢弃
```

#### 显式的多消费者模式

```JavaScript
// 通过显式缓冲区管理进行共享
const shared = Stream.share(source, {
  highWaterMark: 100,
  backpressure: 'strict'
});

const consumer1 = shared.pull();
const consumer2 = shared.pull(decompress);
```

您获得的是显式的多消费者原语，而不是带有隐藏无界缓冲区的 `tee()`。`Stream.share()` 是基于拉取的：消费者从一个共享源拉取数据，您可以预先配置缓冲区限制和背压策略。

还有 `Stream.broadcast()` 用于基于推送的多消费者场景。两者都要求您思考当消费者以不同速度运行时会发生什么，因为这是一个不应被隐藏的实际问题。

#### 同步/异步分离

并非所有流处理工作负载都涉及 I/O。当您的源在内存中且您的转换是纯函数时，异步机制会增加开销而没有好处。您为"等待"的协调付出的代价毫无益处。

新 API 提供了完全并行的同步版本：`Stream.pullSync()`、`Stream.bytesSync()`、`Stream.textSync()` 等。如果您的源和转换都是同步的，您可以在不涉及任何 Promise 的情况下处理整个流水线。

```JavaScript
// 异步 —— 当源或转换可能是异步时
const textAsync = await Stream.text(source);

// 同步 —— 当所有组件都是同步时
const textSync = Stream.textSync(source);
```

这是一个完整的同步流水线 —— 压缩、转换和消费，零异步开销：

```JavaScript
// 来自内存数据的同步源
const source = Stream.fromSync([inputBuffer]);

// 同步转换
const compressed = Stream.pullSync(source, zlibCompressSync);
const encrypted = Stream.pullSync(compressed, aesEncryptSync);

// 同步消费 —— 没有 Promise，没有事件循环切换
const result = Stream.bytesSync(encrypted);
```

整个流水线在单个调用栈中执行。没有创建 Promise，没有微任务队列调度，也没有来自短寿命异步机制的 GC 压力。对于 CPU 密集型工作负载，如解析、压缩或内存数据的转换，这可能比等效的 Web 流代码快得多 —— 后者即使每个组件都是同步的，也会强制引入异步边界。

Web 流没有同步路径。即使您的源数据已就绪且您的转换是纯函数，您仍然需要为每次操作支付 Promise 创建和微任务调度的开销。Promise 在确实需要等待的情况下非常出色，但它们并非总是必要的。新 API 让您在需要时可以停留在同步领域。

#### 弥合此方法与 Web 流之间的差距

基于异步迭代器的方法为此替代方法与 Web 流之间提供了天然的桥梁。当从 ReadableStream 转换到这种新方法时，如果 ReadableStream 设置为生成字节，只需将 readable 作为输入传递即可正常工作：

```JavaScript
const readable = getWebReadableStreamSomehow();
const input = Stream.pull(readable, transform1, transform2);
for await (const chunks of input) {
  // 处理数据块
}
```

当适配到 ReadableStream 时，需要多做一点工作，因为替代方法会批量生成数据块，但适配层同样简单明了：

```JavaScript
async function* adapt(input) {
  for await (const chunks of input) {
    for (const chunk of chunks) {
      yield chunk;
    }
  }
}

const input = Stream.pull(source, transform1, transform2);
const readable = ReadableStream.from(adapt(input));
```

#### 这如何解决之前提到的现实世界故障

-   **未消费的主体**：拉取语义意味着在您迭代之前什么也不会发生。没有隐藏的资源保留。如果您不消费一个流，就没有后台机制保持连接打开。
-   **`tee()` 内存悬崖**：`Stream.share()` 需要显式的缓冲区配置。您预先选择 `highWaterMark` 和背压策略：当消费者以不同速度运行时，不再有静默的无界增长。
-   **转换背压间隙**：拉取式转换按需执行。数据不会在中间缓冲区级联；它仅在消费者拉取时流动。停止迭代，就停止处理。
-   **SSR 中的 GC 抖动**：批量数据块（Uint8Array[]）分摊了异步开销。通过 `Stream.pullSync()` 实现的同步流水线，对于 CPU 密集型工作负载，完全消除了 Promise 分配。

**未消费的主体**：拉取语义意味着在您迭代之前什么也不会发生。没有隐藏的资源保留。如果您不消费一个流，就没有后台机制保持连接打开。

**`tee()` 内存悬崖**：`Stream.share()` 需要显式的缓冲区配置。您预先选择 `highWaterMark` 和背压策略：当消费者以不同速度运行时，不再有静默的无界增长。

**转换背压间隙**：拉取式转换按需执行。数据不会在中间缓冲区级联；它仅在消费者拉取时流动。停止迭代，就停止处理。

**SSR 中的 GC 抖动**：批量数据块（Uint8Array[]）分摊了异步开销。通过 `Stream.pullSync()` 实现的同步流水线，对于 CPU 密集型工作负载，完全消除了 Promise 分配。

### 性能

设计选择对性能有影响。以下是此可能替代方案的参考实现与 Web 流的基准测试对比（Node.js v24.x，Apple M1 Pro，10 次运行平均值）：

| 场景 | 替代方案 | Web 流 | 差异 |
| :--- | :--- | :--- | :--- |
| 小数据块 (1KB × 5000) | ~13 GB/s | ~4 GB/s | ~3 倍更快 |
| 微小数据块 (100B × 10000) | ~450 MB/s | ~55 MB/s | ~8 倍更快 |
| 异步迭代 (8KB × 1000) | ~530 GB/s | ~35 GB/s | ~15 倍更快 |
| 链式 3× 转换 (8KB × 500) | ~275 GB/s | ~3 GB/s | ~80–90 倍更快 |
| 高频 (64B × 20000) | ~7.5 GB/s | ~280 MB/s | ~25 倍更快 |

链式转换的结果尤其引人注目：拉取式语义消除了困扰 Web 流流水线的中间缓冲。数据按需从消费者流向源，而不是每个 `TransformStream` 急切地填充其内部缓冲区。

公平地说，Node.js 确实尚未投入大量精力来全面优化其 Web 流实现的性能。通过投入一些精力来优化其关键路径，Node.js 的性能结果很可能还有很大的提升空间。尽管如此，在 Deno 和 Bun 中运行这些基准测试也表明，与它们各自的 Web 流实现相比，这种基于迭代器的替代方法也带来了显著的性能提升。

浏览器基准测试（Chrome/Blink，3 次运行平均值）同样显示出一致的性能提升：

推送 3KB 数据块
~135k 次操作/秒
~24k 次操作/秒
~5–6 倍 更快

推送 100KB 数据块
~3k 次操作/秒
~7–8 倍 更快

3 个转换链
~4.6k 次操作/秒
~880 次操作/秒
~5 倍 更快

5 个转换链
~2.4k 次操作/秒
~550 次操作/秒
~4 倍 更快

bytes() 消耗
~73k 次操作/秒
~11k 次操作/秒
~6–7 倍 更快

异步迭代
~1.1M 次操作/秒
~10k 次操作/秒
~40–100 倍 更快

这些基准测试衡量的是受控场景下的吞吐量；实际性能取决于您的具体用例。Node.js 与浏览器性能提升之间的差异，反映了每种环境为 Web 流采取的不同优化路径。

值得注意的是，这些基准测试将新 API 的纯 TypeScript/JavaScript 实现，与各运行时中 Web 流的原生（JavaScript/C++/Rust）实现进行了比较。新 API 的参考实现尚未进行任何性能优化工作；其性能提升完全来自于设计。原生实现可能会带来进一步的改进。

这些提升说明了基本设计选择的复合效应：批处理分摊了异步开销，拉取语义消除了中间缓冲，以及在数据立即可用时实现可以采用同步快速路径的自由度，所有这些都起到了作用。

"我们在提升 Node 流的性能和一致性方面做了很多工作，但白手起家有着独特的力量。新流的方法拥抱了现代运行时的现实，没有历史包袱，这为更简单、高性能和更一致的流模型打开了大门。"
- Robert Nagy，Node.js TSC 成员，Node.js 流贡献者

## 下一步计划

我发布此文是为了开启一场对话。我说对了什么？遗漏了什么？是否有不适合此模型的用例？这种方法的迁移路径会是什么样子？目标是收集那些曾感受过 Web 流之痛、并对更好的 API 应有形态有见解的开发者的反馈。

### 亲自尝试

这种替代方法的参考实现现已可用，可在 https://github.com/jasnell/new-streams 找到。

- API 参考：完整文档请参见 `API.md`
- 示例：`samples` 目录包含常见模式的工作代码

欢迎提交问题、讨论和拉取请求。如果您遇到了我未涵盖的 Web 流问题，或者您认为此方法存在不足，请告诉我。但再次强调，这里的想法不是说"让我们都使用这个闪亮的新对象！"；而是为了发起一场讨论，超越 Web 流的现状，回归基本原则。

Web 流是一个雄心勃勃的项目，在别无他物之时将流式处理带到了 Web 平台。考虑到 2014 年的限制条件——在异步迭代出现之前，在多年的生产经验揭示出边界情况之前——设计者们做出了合理的选择。

但自那时起，我们学到了很多。JavaScript 已经进化。今天设计的流式 API 可以更简单，更符合语言特性，并且对诸如背压和多消费者行为等重要事项更加明确。

我们理应拥有一个更好的流式 API。所以，让我们来探讨一下它可能的样子。

---

> 本文由AI自动翻译，原文链接：[We deserve a better streams API for JavaScript](https://blog.cloudflare.com/a-better-web-streams-api/)
> 
> 翻译时间：2026-02-28 04:33
