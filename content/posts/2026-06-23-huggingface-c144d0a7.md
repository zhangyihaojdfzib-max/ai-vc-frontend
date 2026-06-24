---
title: Transformers.js跨源存储API实验：解决模型缓存重复问题
title_original: Experimenting with the proposed Cross-Origin Storage API in Transformers.js
date: '2026-06-23'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/cross-origin-storage
author: ''
summary: 本文介绍了Transformers.js在浏览器中运行AI模型时面临的缓存挑战：不同源的应用会重复下载相同的模型资源和Wasm运行时文件，导致带宽和存储浪费。作者通过实验展示了跨源存储API的潜在解决方案，该API允许不同源共享已缓存的资源，从而避免冗余下载。文章强调了这一API对提升Web
  AI应用性能和用户体验的重要性。
categories:
- AI基础设施
tags:
- Transformers.js
- 跨源存储API
- 模型缓存
- WebAssembly
- 浏览器AI
draft: false
translated_at: '2026-06-24T06:09:04.739950'
---

# 在 Transformers.js 中实验提议的跨源存储 API

（本文是谷歌 Chrome 团队开发者关系工程师 Thomas Steiner 的客座文章。）

Transformers.js 为 Web 开发者提供了一种简单的方式，通过特定任务的管道（pipeline）在其 Web 应用中使用 Transformer 的强大功能。为了在浏览器中运行推理，开发者创建 `pipeline()` 的实例并指定要使用该管道的任务。作为一个具体示例，以下代码片段展示了如何设置自动语音识别（ASR）管道。

```js
import { pipeline } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@4.2.0';

const asr = await pipeline(
  'automatic-speech-recognition',
  'Xenova/whisper-tiny.en',
  { device: 'webgpu' },
);
const result = await asr('jfk.wav');
console.log(result);

```

![自动语音识别管道的极简示例。](/images/posts/40c2e6e530b2.png)

## 缓存挑战

你会注意到，在源代码中我指定了 `Xenova/whisper-tiny.en` 作为模型，这对于常见的英语自动语音识别任务来说是一个非常合适的选择。事实上，根据链接的摘录，按照 Transformers.js 的默认模型解析规则，它甚至是默认模型。

### 模型资源

当你在浏览器中运行此示例时，Transformers.js 会自动处理相关模型资源和 Wasm 文件的下载与缓存。以下截图显示了访问应用后 Chrome DevTools 的缓存存储部分。当你重新加载页面时，资源会从缓存 API 中提供，模型几乎立即返回结果。

![Chrome DevTools 缓存存储部分，显示访问应用后的 Whisper AI 模型资源和 Wasm 运行时文件。](/images/posts/4daaa57c2d26.png)

然而，`Xenova/whisper-tiny.en` 是一个流行的模型（如前所述，甚至是 Transformers.js 中 ASR 的默认模型），你可以想象，你访问的不仅仅是一个应用会使用它。为了模拟这种情况，这里是之前相同的示例应用，但从不同的源提供服务。当你访问这个不同源的应用时，浏览器无法几乎立即使用，而是必须再次下载并缓存所有模型资源，即使它们与之前逐字节相同。即使在这个玩具示例中，这也导致了 177 MB 的重复下载和存储，你可以在 Chrome DevTools 应用面板的存储部分中查看。你可以想象这种情况会迅速累积。

![Chrome DevTools 存储概览，显示 177 MB 的已用存储。](/images/posts/1e920e43e4f8.png)

### Wasm 运行时资源

但情况更糟。让我们在玩具示例中添加第二个管道：情感分析。情感分析默认使用 `Xenova/distilbert-base-uncased-finetuned-sst-2-english` 模型。通过不指定模型，Transformers.js 的默认模型解析会自动为你选择它。

```js
const classifier = await pipeline('sentiment-analysis');
const sentiment = await classifier(result.text);
pre.append('\n\n' + JSON.stringify(sentiment, null, 2));

```

![image](/images/posts/3f74633aed02.png)

两个完全不同的 AI 模型，但它们依赖于相同的 4,733 kB `ort-wasm-simd-threaded.asyncify.wasm` WebAssembly（Wasm）运行时文件，该文件来自 Transformers.js 所基于的底层 ONNX 运行时库。在不同源上打开扩展演示，你会注意到在网络选项卡中，Wasm 运行时也被再次下载和缓存。

![Chrome DevTools 网络面板，显示 Wasm 运行时资源的下载。](/images/posts/51a1f4735d73.png)

因此，即使你运行的应用不共享相同的 AI 模型，你的浏览器仍然会对你已有的共享 Wasm 资源发出冗余请求，并且还会再次缓存它们，这会消耗硬盘空间。

### 缓存隔离

#### AI 模型资源服务

默认情况下，AI 模型资源来自 Hugging Face Hub，最终来自 Hugging Face CDN。浏览器会请求类似 `https://huggingface.co/Xenova/distilbert-base-uncased-finetuned-sst-2-english/resolve/main/config.json` 的资源，然后该请求会被重定向到最终的 CDN URL，例如 `https://huggingface.co/api/resolve-cache/models/Xenova/distilbert-base-uncased-finetuned-sst-2-english/0b6928efcb76139cae2c6881d49cda67fe119f42/config.json?%2FXenova%2Fdistilbert-base-uncased-finetuned-sst-2-english%2Fresolve%2Fmain%2Fconfig.json=&etag=%223c36342ef1f74de2797d667c68c6b7b988d0b87c%22`。

#### Wasm 运行时资源服务

Wasm 运行时资源默认来自 jsDelivr CDN。例如，在撰写本文时，`ort-wasm-simd-threaded.asyncify.wasm` 来自 `https://cdn.jsdelivr.net/npm/onnxruntime-web@1.26.0-dev.20260416-b7804b056c/dist/ort-wasm-simd-threaded.asyncify.wasm`。

现在你可能会说，如果不同的应用，即使运行在不同的源上，最终从相同的 CDN URL 提供其资源，只要最终 URL 相同，缓存就不应该是问题。不幸的是，长期以来浏览器中的缓存并非如此工作。文章《通过分区缓存获得安全性和隐私性》详细介绍了所有细节，但本质上，缓存是按源隔离的，以防止时序攻击：网站响应 HTTP 请求所花费的时间可以揭示浏览器过去是否访问过相同的资源，这使得浏览器容易受到安全和隐私泄露的影响。

#### Chrome 的实现

具体实现可能因浏览器而异，但在 Chrome 中，缓存资源除了资源 URL 之外，还使用网络隔离密钥进行键控。网络隔离密钥由顶级站点和当前帧站点组成。以托管在源 `https://googlechrome.github.io` 和 `https://rawcdn.rawgit.net` 上的先前玩具示例为例。如果它们都使用来自 `https://cdn.jsdelivr.net/npm/onnxruntime-web@1.26.0-dev.20260416-b7804b056c/dist/ort-wasm-simd-threaded.asyncify.wasm` 的 Wasm 运行时，它们的缓存键将如下表所示。

```
https://googlechrome.github.io
```

```
https://googlechrome.github.io
```

```
https://cdn.jsdelivr.net/npm/onnxruntime-web@1.26.0-dev.20260416-b7804b056c/dist/ort-wasm-simd-threaded.asyncify.wasm
```

```
https://rawcdn.rawgit.net
```

```
https://rawcdn.rawgit.net
```

```
https://cdn.jsdelivr.net/npm/onnxruntime-web@1.26.0-dev.20260416-b7804b056c/dist/ort-wasm-simd-threaded.asyncify.wasm
```

因此，即使资源 URL 完全相同，由于网络隔离密钥不匹配，也不会发生缓存命中，这意味着重复下载和重复存储。这就是跨源存储提案旨在解决的挑战。

## 跨源存储 API 登场

💡 注意：跨源存储 API 是一个早期阶段的提案，尚未最终确定。虽然提议的 API 尚未在任何浏览器中原生实现，但你无需等待即可进行实验。安装跨源存储扩展，以在所有页面上注入 `navigator.crossOriginStorage` 填充库，并测试完整流程。

提议的跨源存储（COS）API 引入了一个专用的 `navigator.crossOriginStorage` 接口，通过该接口，Web 应用可以跨源边界存储和检索大文件，这些文件不是通过 URL 标识，而是通过加密哈希标识。

最后一点关于加密哈希是关键。因为 COS 通过文件的哈希而不是其 URL 或源来标识文件，所以你在访问 `https://googlechrome.github.io` 时下载的同一个 `ort-wasm-simd-threaded.asyncify.wasm` Wasm 运行时，会被识别为与 `https://rawcdn.rawgit.net` 即将请求的相同，无论这两个源中的哪一个获取了它。请参阅以下代码片段，它说明了基本流程。

```js
const hash = {
  algorithm: 'SHA-256',
  value: '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4',
};
```

```javascript
try {
  const handle = await navigator.crossOriginStorage.requestFileHandle(hash);
  
  const fileBlob = await handle.getFile();
} catch (err) {
  
  const fileBlob = await fetch('https://cdn.jsdelivr.net/.../ort-wasm-simd-threaded.asyncify.wasm')
    .then(r => r.blob());
  const handle = await navigator.crossOriginStorage.requestFileHandle(
    hash,
    { create: true, origins: '*' },
  );
  const writableStream = await handle.createWritable();
  await writableStream.write(fileBlob);
  await writableStream.close();  
}
```

如果资源在COS中，你会得到一个`FileSystemFileHandle`，你可以通过`getFile()`直接从中读取blob（生成的`File`继承自`Blob`）。如果资源不在COS中，你会回退到网络，并将资源写入COS，供下一个需要它的应用使用——这个应用可能是你自己的应用，也可能是另一个不相关的应用，甚至可能来自完全不同的源。

该API特意模仿了文件系统标准中的`FileSystemDirectoryHandle.getFileHandle()`，你可能已经从源私有文件系统（OPFS）API中熟悉了它。`hash`参数的作用与OPFS中的`name`参数相同：唯一标识一个资源。`options.create`标志的工作方式也相同：缺失或为`false`表示只读访问，`true`表示你打算写入。

### 控制谁可以读取什么

并非每个资源都应该全局共享。COS通过存储文件时的`origins`选项，让开发者能够精确控制可见性。

- 设置`origins: '*'`使文件全局可用。任何源都可以通过哈希找到它。这对于AI模型资源或Transformers.js示例中的Wasm运行时是正确选择：关键在于每个Web应用都能从单个缓存副本中受益。
- 传递特定的源列表，例如`origins: ['https://write.example.com', 'https://calculate.example.com']`，将访问限制在这些站点。这适用于在公司自有属性间共享的专有资源，不应被其他任何人发现，比如商业办公套件中使用的专有校对AI模型。
- 完全省略`origins`会使文件仅对同站源可用。这是跨组织所有子域共享资源的合理默认设置，但不打算跨越组织边界。

一个重要规则：可见性可以升级，但绝不能降级。如果一个文件已经是全局可用的，后续尝试用受限的`origins`列表存储它会被静默忽略。这可以防止恶意行为者重新存储公共资源并缩小其可用范围。反之是可能的：最初以受限`origins`列表存储的文件，后续可以放宽权限。任何站点（不仅仅是原始存储者）都可以为相同的哈希（哈希并非秘密）调用`requestFileHandle()`，并设置`create: true`和更宽泛的`origins`值，由于浏览器会验证哈希匹配，该资源从那时起将对更广泛的受众可用。请注意，升级站点仍然必须通过返回的句柄写入完整的文件。此要求是为了防止站点利用升级路径作为侧信道来检测特定文件是否已存储在COS中。

### 设计上的完整性

COS的一个微妙但重要的属性是，当你写入文件时，浏览器会验证哈希。如果你写入的数据与声明的哈希不匹配，写入会失败并返回错误。这使得完整性检查自动化：从COS读取文件的应用可以确信它得到了预期的确切字节。这与它在网络下载后自行计算哈希所能获得的保证相同。

这在Transformers.js场景中被证明是双重有用的。如今，在下载模型权重后，大多数应用没有实际方法来验证CDN是否提供了正确的字节。有了COS，存储中的每个文件在写入时都会被隐式验证，无论它来自何处——官方的Hugging Face CDN还是某个随机站点的自托管镜像。

### 不牺牲实用性的隐私保护

当然，跨源共享缓存提出了与分区HTTP缓存相反的问题：如果任何站点都可以通过哈希探测文件是否存在，攻击者难道不能通过检查某个游戏引擎的Wasm模块是否被缓存来了解用户的浏览历史吗？

COS通过两种互补机制解决这个问题：

- 首先，`origins`字段：不应被全局探测的专有资源，就不应该用`origins: '*'`来存储。通过开发者教育，鼓励开发者在合理的情况下考虑这一点。
- 其次，可用性门控：即使对于全局声明的文件，如果该文件尚未在足够多的不同源上出现过，浏览器可能会抑制对文件存在性的确认。仅在一两个站点上出现的文件仍可能作为跨站点标识符，因此浏览器可能会返回错误，仿佛该文件根本不存在，无论磁盘上实际有什么。在Chrome团队中，我们意识到不常见资源可能导致的隐私泄露，并计划通过限制哪些确切资源可以被缓存来普遍缓解这一问题。具体的缓解措施仍在完善中。

关键的是，这意味着错误并非最终答案。它可能意味着“未存储”，也可能意味着“已存储，但浏览器不告诉你”。应用应始终以相同方式处理：回退到网络。

### 这对Transformers.js示例意味着什么

回到之前的玩具示例：`ort-wasm-simd-threaded.asyncify.wasm`运行时大小为4,733 kB，被所有基于Transformers.js的应用共享，无论它们使用哪个AI模型。有了COS，第一个加载它的应用会下载一次，并以`origins: '*'`存储在其SHA-256哈希下。每个后续应用，无论是在`https://googlechrome.github.io`、`https://rawcdn.rawgit.net`还是任何其他源上，都能立即在COS中找到它。那177 MB重复的Whisper模型权重呢？同样的故事：`Xenova/whisper-tiny.en`被下载一次，第二次通过哈希识别，并从COS毫秒级提供。当然，`Xenova/distilbert-base-uncased-finetuned-sst-2-english`也是如此。

Transformers.js本身已经在库级别试用COS API。拉取请求#1549引入了一个实验性的COS缓存后端，位于一个可选标志之后。在设置管道之前，只需一行代码即可启用它：

```js
import { env, pipeline } from "https://cdn.jsdelivr.net/npm/@huggingface/transformers@4.2.0";

env.experimental_useCrossOriginStorage = true;

const asr = await pipeline('automatic-speech-recognition', 'Xenova/whisper-tiny.en', { device: 'webgpu' });
const result = await asr('jfk.wav');
console.log(result);
```

设置该标志后，Transformers.js通过获取原始Xet指针文件（示例原始指针文件）并提取其`oid sha256:`字段，为每个Xet跟踪的模型文件（大型ONNX权重文件）解析SHA-256哈希。然后它使用该哈希作为`navigator.crossOriginStorage`的键。如果模型已在COS中（因为另一个站点先存储了它），则无需网络往返即可立即提供。如果没有，它会回退到常规下载，并将结果存储在COS中供下一个调用者使用。通过这个玩具示例，实际的优势在于`Xenova/whisper-tiny.en`和`Xenova/distilbert-base-uncased-finetuned-sst-2-english`（当然还有`ort-wasm-simd-threaded.asyncify.wasm`）只需要通过网络传输一次，无论有多少不同的源请求它们。

请注意标志上的`experimental_`前缀。这是有意为之，表明底层浏览器API尚未标准化，并且可能在没有主版本号变更的情况下发生变化。

### 立即尝试

COS API 目前尚未在任何浏览器中原生实现，但你无需等待即可进行实验。安装 Cross-Origin Storage 扩展，即可在所有页面上注入 navigator.crossOriginStorage polyfill，并测试完整流程。你可以查看扩展的源代码，并按照使用说明开始操作。

![Cross-Origin Storage 扩展的 Chrome 网上应用店页面。](/images/posts/e0cb25351e79.png)

安装扩展后，你现在就可以体验完整的端到端流程：打开第一个启用了 COS 的示例页面，让它加载 Xenova/whisper-tiny.en，然后从第二个源打开启用了 COS 的示例页面。与之前 177 MB 的重新下载不同，模型现在通过 COS 在毫秒级内提供。当你打开扩展的弹出窗口时，可以看到 COS 的实际运行情况。如果按资源查看，你可以看到 SHA-256 哈希值为 950978b1dbcbf250335358c1236053ba19a7f7849b33dc777f4421b72b7626fa 的资源在 https://googlechrome.github.io 和 https://rawcdn.rawgit.net 之间共享。这可能不太明显，但你可以通过对比 Hugging Face 上的 SHA-256 哈希值来验证，你正在查看的是 https://huggingface.co/Xenova/whisper-tiny.en/blob/main/onnx/decoder_model_merged.onnx。目前，该扩展主要面向像你这样的高级用户。一旦在浏览器中实现，浏览器设置页面将提供更友好的集成。下面的截图显示了扩展的弹出窗口，其中按资源查看选项卡处于激活状态，你可以看到共享资源及其哈希值，以及将其存储在 COS 缓存中的两个源。

## 行动号召

如果你正在构建自己的 Transformers.js 应用，行动号召很简单：在首次调用 pipeline() 之前添加 env.experimental_useCrossOriginStorage = true，安装扩展，然后观察网络选项卡中重复下载的消失。每个选择加入的站点都会让其他站点用户的体验更快、成本更低。选择加入完全没有风险：如果用户未安装 COS 扩展导致 COS API 不受支持，代码会回退到默认路径（Web Cache API）。

Transformers.js 并非唯一在尝试 COS 的项目。WebLLM（选择加入，参见文档）和 wllama（自动，参见 PR）同样对这一提议的 API 感到兴奋。

在 Chrome 团队中，我们正在考虑在浏览器中原生实现 COS API。作为一项早期阶段的提案，我们欢迎对 API 本身以及提案形态的反馈。Cross-Origin Storage 仓库是提交问题、表达支持或发起 PR 的地方。

---

> 本文由AI自动翻译，原文链接：[Experimenting with the proposed Cross-Origin Storage API in Transformers.js](https://huggingface.co/blog/cross-origin-storage)
> 
> 翻译时间：2026-06-24 06:09
