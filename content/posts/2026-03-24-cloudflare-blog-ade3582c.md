---
title: Cloudflare推出轻量级AI智能体沙箱，速度提升100倍
title_original: 'The Cloudflare Blog: Sandboxing AI agents, 100x faster'
date: '2026-03-24'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/dynamic-workers/
author: ''
summary: 本文介绍了Cloudflare推出的动态Worker加载器API，该功能现已进入公开测试阶段。它利用与Cloudflare Workers平台相同的底层隔离技术，为AI智能体或MCP服务器执行动态生成的代码提供了一个安全、轻量的沙箱环境。相比传统的容器方案，该沙箱的启动速度快约100倍，内存效率高出10-100倍，且支持无限扩展，无需预热或复用，能够满足消费者规模智能体应用对高性能和强安全隔离的需求。
categories:
- AI基础设施
tags:
- AI智能体
- 沙箱技术
- Cloudflare Workers
- 代码模式
- 边缘计算
draft: false
translated_at: '2026-03-25T04:43:01.261425'
---

# 为AI智能体构建沙箱，速度提升100倍

2026-03-24

- Kenton Varda
- Sunil Pai
- Ketan Gupta

![](/images/posts/8ca7784d0b4b.png)

去年九月，我们推出了代码模式（Code Mode）——其核心理念是智能体不应通过调用工具来执行任务，而应通过编写调用API的代码来实现。我们已证明，仅将MCP服务器转换为TypeScript API即可将Token使用量减少81%。我们还展示了代码模式不仅可以在MCP服务器前端运行，也能在其后端运行，从而创建了全新的Cloudflare MCP服务器，仅用两个工具和不到1000个Token就能暴露整个Cloudflare API。

但如果一个智能体（或MCP服务器）要执行由AI动态生成的代码来完成任务，这些代码就需要在某个地方运行，而这个地方必须是安全的。你不能直接在应用中使用`eval()`执行AI生成的代码：恶意用户可以轻易诱导AI注入漏洞。

你需要一个沙箱：一个用于执行代码的隔离环境，它独立于你的应用程序和外部世界，仅允许代码访问特定的预设能力。

沙箱化是AI行业的热门话题。对于这项任务，大多数人选择使用容器。借助基于Linux的容器，你可以启动任何所需的代码执行环境。为此，Cloudflare甚至提供了我们的容器运行时和沙箱SDK。

但容器启动成本高且速度慢，需要数百毫秒的启动时间和数百兆字节的内存。你可能需要保持容器预热以避免延迟，并且可能倾向于复用现有容器处理多个任务，但这会牺牲安全性。

如果我们想要支持消费者规模的智能体应用——即每个终端用户都拥有一个（或多个！）智能体，且每个智能体都会编写代码——那么容器方案是远远不够的。我们需要更轻量的解决方案。

###### 而我们已拥有它。

## 动态Worker加载器：一个轻量级沙箱

在我们去年九月关于代码模式的博文中，悄然发布了一项新的实验性功能：动态Worker加载器API。该API允许Cloudflare Worker在运行时动态实例化一个新的Worker，该Worker运行在独立的沙箱中，代码可在运行时指定。

动态Worker加载器现已进入公开测试阶段，对所有付费Workers用户开放。

请查阅文档了解完整细节，以下是其基本用法示例：

```javascript
// 让你的LLM生成如下代码。
let agentCode: string = `
  export default {
    async myAgent(param, env, ctx) {
      // ...
    }
  }
`;

// 获取代表智能体应能访问的API的RPC存根。
//（这可以是您定义的任何Workers RPC API。）
let chatRoomRpcStub = ...;

// 使用worker加载器绑定加载一个Worker来运行代码。
let worker = env.LOADER.load({
  // 指定代码。
  compatibilityDate: "2026-03-01",
  mainModule: "agent.js",
  modules: { "agent.js": agentCode },

  // 授予智能体访问聊天室API的权限。
  env: { CHAT_ROOM: chatRoomRpcStub },

  // 阻止互联网访问。（您也可以拦截它。）
  globalOutbound: null,
});

// 调用由智能体代码导出的RPC方法。
await worker.getEntrypoint().myAgent(param);

```

就这么简单。

### 速度提升100倍

动态Worker使用了与整个Cloudflare Workers平台自八年前推出以来一直依赖的底层沙箱机制相同的技术：隔离（isolates）。一个隔离是V8 JavaScript执行引擎的一个实例，与Google Chrome使用的引擎相同。它们正是Workers的运行基础。

一个隔离的启动仅需几毫秒，内存占用仅几兆字节。这比典型容器快了约100倍，内存效率高出10到100倍。

这意味着，你可以为每个用户请求按需启动一个新的隔离来运行一段代码，然后立即销毁它。

### 无限扩展性

许多基于容器的沙箱提供商会对全局并发沙箱数量和沙箱创建速率施加限制。动态Worker加载器没有此类限制。它不需要，因为它本质上只是对我们平台长期使用的同一技术提供的API，该技术始终支持Workers无缝扩展到每秒数百万请求。

想要每秒处理一百万个请求，且每个请求都加载一个独立的动态Worker沙箱并同时运行？没问题！

### 零延迟

一次性动态Worker通常在与创建它们的Worker相同的机器——甚至是同一个线程上运行。无需在全球范围内通信寻找预热沙箱。隔离是如此轻量，我们可以在请求到达的任何地方运行它们。动态Worker在Cloudflare全球数百个数据中心均得到支持。

### 纯JavaScript环境

与容器相比，唯一的限制是你的智能体需要编写JavaScript。

从技术上讲，Worker（包括动态Worker）可以使用Python和WebAssembly，但对于小段代码——例如由智能体按需编写的代码——JavaScript的加载和运行速度要快得多。

我们人类往往对编程语言有强烈的偏好，虽然许多人喜欢JavaScript，但其他人可能更喜欢Python、Rust或无数其他语言。

但我们这里讨论的不是人类。我们讨论的是AI。AI可以编写你想要的任何语言。LLM精通所有主流语言。它们在JavaScript方面的训练数据是海量的。

JavaScript因其在Web上的特性，天生就被设计为可沙箱化。它是这项工作的正确语言选择。

### 用TypeScript定义工具

如果我们希望智能体能够执行任何有用的任务，它需要与外部API通信。我们如何告知它可以访问哪些API？

MCP为扁平的工具调用定义了模式，但不涉及编程API。OpenAPI提供了一种表达REST API的方式，但其模式本身以及调用它所需编写的代码都过于冗长。

对于暴露给JavaScript的API，有一个单一且显而易见的答案：TypeScript。

智能体理解TypeScript。TypeScript设计简洁。只需极少的Token，你就能让智能体精确理解你的API。

```Typescript
// 与聊天室交互的接口。
interface ChatRoom {
  // 获取聊天记录中最后`limit`条消息。
  getHistory(limit: number): Promise<Message[]>;

  // 订阅新消息。处置返回的对象以取消订阅。
  subscribe(callback: (msg: Message) => void): Promise<Disposable>;

  // 向聊天室发送消息。
  post(text: string): Promise<void>;
}

type Message = {
  author: string;
  time: Date;
  text: string;
}

```

将其与等效的OpenAPI规范进行比较（后者冗长到需要滚动才能看完）：

```

openapi: 3.1.0
info:
  title: ChatRoom API
  description: >
    Interface to interact with a chat room.
  version: 1.0.0

paths:
  /messages:
    get:
      operationId: getHistory
      summary: Get recent chat history
      description: Returns the last `limit` messages from the chat log, newest first.
      parameters:
        - name: limit
          in: query
          required: true
          schema:
            type: integer
            minimum: 1
      responses:
        "200":
          description: A list of messages.
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/Message"

    post:
      operationId: postMessage
      summary: Post a message to the chat room
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - text
              properties:
                text:
                  type: string
      responses:
        "204":
          description: Message posted successfully.

/messages/stream:
    get:
      operationId: subscribeMessages
      summary: 通过SSE订阅新消息
      description: >
        打开一个服务器发送事件流。每个事件携带一个JSON编码的Message对象。客户端通过关闭连接来取消订阅。
      responses:
        "200":
          description: 新消息的SSE流。
          content:
            text/event-stream:
              schema:
                description: >
                  每个SSE的`data`字段包含一个JSON编码的Message对象。
                $ref: "#/components/schemas/Message"

components:
  schemas:
    Message:
      type: object
      required:
        - author
        - time
        - text
      properties:
        author:
          type: string
        time:
          type: string
          format: date-time
        text:
          type: string

```

我们认为TypeScript API更好。它使用的Token更少，并且（无论对Agent还是人类来说）都更容易理解。

动态工作负载加载器使得在你自己的Worker中实现这样的TypeScript API变得很容易，然后你可以将其作为方法参数或环境对象传递给动态工作负载。Workers运行时将在沙箱和你的控制代码之间自动建立一个Cap'n Web RPC桥接，这样Agent就可以跨安全边界调用你的API，而无需意识到它使用的不是本地库。

这意味着你的Agent可以编写如下代码：

```javascript
// 思考：用户要求我总结Alice最近的聊天消息。
// 我将在代码中过滤最近的消息历史记录，以便只读取相关消息。
let history = await env.CHAT_ROOM.getHistory(1000);
return history.filter(msg => msg.author == "alice");

```

### HTTP过滤与凭证注入

如果你更倾向于为你的Agent提供HTTP API，这也是完全支持的。使用工作负载加载器API的`globalOutbound`选项，你可以注册一个回调函数，该函数会在每个HTTP请求时被调用，你可以在其中检查请求、重写请求、注入认证密钥、直接响应请求、阻止请求，或执行任何你需要的操作。

例如，你可以使用这个功能来实现**凭证注入**（Token注入）：当Agent向一个需要授权的服务发起HTTP请求时，你在请求发出时为其添加凭证。这样，Agent本身永远不会知道秘密凭证，因此也就无法泄露它们。

当Agent与其训练集中已知的API通信时，或者当你希望Agent使用基于REST API构建的库时（该库可以在Agent的沙箱内运行），使用普通的HTTP接口可能是可取的。

尽管如此，**在没有兼容性要求的情况下，TypeScript RPC接口优于HTTP接口**：

-   如上所示，描述一个TypeScript接口所需的Token远少于描述一个HTTP接口。
-   Agent编写代码调用TypeScript接口所需的Token也远少于调用等效HTTP接口。
-   使用TypeScript接口时，由于你无论如何都在定义自己的包装接口，因此更容易缩小接口范围，精确地暴露你希望提供给Agent的能力，这既是为了简化也是为了安全。而使用HTTP时，你更可能是在实现针对某个现有API的请求**过滤**。这很困难，因为你的代理必须完全解释每个API调用的含义才能正确决定是否允许它，而HTTP请求很复杂，包含许多可能都有意义的头部和其他参数。最终，直接编写一个仅实现你允许的功能的TypeScript包装器反而更容易。

### 久经考验的安全性

强化基于隔离的沙箱是棘手的，因为它比硬件虚拟机拥有更复杂的攻击面。尽管所有沙箱机制都存在漏洞，但V8中的安全漏洞比典型虚拟机管理程序中的安全漏洞更为常见。当使用隔离来沙箱化可能恶意的代码时，拥有额外的深度防御层非常重要。例如，谷歌Chrome就因此实现了严格的进程隔离，但这并非唯一的解决方案。

我们在保护基于隔离的平台方面拥有近十年的经验。我们的系统能在几小时内自动将V8安全补丁部署到生产环境——比Chrome本身更快。我们的**安全架构**采用定制的第二层沙箱，并根据风险评估动态隔离租户。我们**扩展了V8沙箱本身**以利用MPK等硬件特性。我们与（并聘请了）顶尖研究人员合作，开发了**针对Spectre的新型防御措施**。我们还有系统可以扫描代码中的恶意模式，并自动阻止它们或应用额外的沙箱层。等等。

当你在Cloudflare上使用动态工作负载时，你将自动获得所有这些保护。

## 辅助库

我们构建了一些库，你在使用动态工作负载时可能会发现它们很有用：

### 代码模式

`@cloudflare/codemode` 简化了使用动态工作负载针对AI工具运行模型生成的代码。其核心是 `DynamicWorkerExecutor()`，它构建了一个专用的沙箱，具有代码规范化功能以处理常见的格式错误，并可直接访问 `globalOutbound` fetcher 来控制沙箱内的 `fetch()` 行为——将其设置为 `null` 以实现完全隔离，或传递一个 `Fetcher` 绑定来路由、拦截或丰富来自沙箱的出站请求。

```Typescript
const executor = new DynamicWorkerExecutor({
  loader: env.LOADER,
  globalOutbound: null, // 完全隔离
});

const codemode = createCodeTool({
  tools: myTools,
  executor,
});

return generateText({
  model,
  messages,
  tools: { codemode },
});

```

代码模式SDK还提供了两个服务器端实用函数。`codeMcpServer({ server, executor })` 包装一个现有的MCP服务器，用一个单一的 `code()` 工具替换其工具界面。`openApiMcpServer({ spec, executor, request })` 更进一步：给定一个OpenAPI规范和一个执行器，它构建一个完整的MCP服务器，包含Cloudflare MCP服务器使用的 `search()` 和 `execute()` 工具，更适合大型API。

在这两种情况下，模型生成的代码都在动态工作负载内运行，对外的服务调用通过传递给执行器的RPC绑定进行。

了解更多关于该库及其使用方法的信息。

### 打包

动态工作负载期望预打包的模块。`@cloudflare/worker-bundler` 为你处理这个问题：给它源文件和一个 `package.json`，它会从注册表解析npm依赖项，用 `esbuild` 打包所有内容，并返回工作负载加载器期望的模块映射。

```Typescript
import { createWorker } from "@cloudflare/worker-bundler";

const worker = env.LOADER.get("my-worker", async () => {
  const { mainModule, modules } = await createWorker({
    files: {
      "src/index.ts": `
        import { Hono } from 'hono';
        import { cors } from 'hono/cors';
```

```typescript
const app = new Hono();
        app.use('*', cors());
        app.get('/', (c) => c.text('Hello from Hono!'));
        app.get('/json', (c) => c.json({ message: 'It works!' }));

        export default app;
      `,
      "package.json": JSON.stringify({
        dependencies: { hono: "^4.0.0" }
      })
    }
  });

  return { mainModule, modules, compatibilityDate: "2026-01-01" };
});

await worker.getEntrypoint().fetch(request);

```

它还通过 `createApp` 支持全栈应用——将服务器 Worker、客户端 JavaScript 和静态资源捆绑在一起，并内置了处理内容类型、ETag 和 SPA 路由的资源服务功能。

### 文件操作

`@cloudflare/shell` 为您的 Agent（智能体）在动态 Worker 内部提供了一个虚拟文件系统。Agent 代码通过 `state` 对象调用类型化方法——读取、写入、搜索、替换、差异比较、通配符匹配、JSON 查询/更新、归档——使用结构化的输入和输出，而不是解析字符串。

存储由持久的 `Workspace`（SQLite + R2）支持，因此文件在多次执行之间持久保存。像 `searchFiles`、`replaceInFiles` 和 `planEdits` 这样的粗粒度操作最大限度地减少了 RPC 往返次数——Agent 只需发出一次调用，而不是循环处理单个文件。批量写入默认是事务性的：如果任何写入失败，之前的写入会自动回滚。

```Typescript
import { Workspace } from "@cloudflare/shell";
import { stateTools } from "@cloudflare/shell/workers";
import { DynamicWorkerExecutor, resolveProvider } from "@cloudflare/codemode";

const workspace = new Workspace({
  sql: this.ctx.storage.sql, // 可与任何 DO 的 SqlStorage、D1 或自定义 SQL 后端配合使用
  r2: this.env.MY_BUCKET, // 大文件自动溢出到 R2
  name: () => this.name   // 惰性解析——在需要时解析，而非构造时
});

// 代码在无网络访问的隔离 Worker 沙箱中运行
const executor = new DynamicWorkerExecutor({ loader: env.LOADER });

// LLM（大语言模型）编写此代码；`state.*` 调用通过 RPC 分派回主机
const result = await executor.execute(
  `async () => {
    // 在所有 TypeScript 文件中搜索模式
    const hits = await state.searchFiles("src/**/*.ts", "answer");
    // 将多次编辑计划为单个事务
    const plan = await state.planEdits([
      { kind: "replace", path: "/src/app.ts",
        search: "42", replacement: "43" },
      { kind: "writeJson", path: "/src/config.json",
        value: { version: 2 } }
    ]);
    // 原子性地应用——失败时回滚
    return await state.applyEditPlan(plan);
  }`,
  [resolveProvider(stateTools(workspace))]
);
```

该包还提供了预构建的 TypeScript 类型声明和一个系统提示词模板，因此您只需少量 Token 即可将完整的 `state` API 放入您的 LLM（大语言模型）上下文中。

## 人们如何使用它？

开发者希望他们的 Agent（智能体）能够针对工具 API 编写和执行代码，而不是逐个进行顺序工具调用。借助动态 Worker，LLM（大语言模型）生成一个将多个 API 调用链接在一起的单个 TypeScript 函数，在动态 Worker 中运行它，并将最终结果返回给 Agent（智能体）。因此，只有输出（而非每个中间步骤）会进入上下文窗口。这既降低了延迟又减少了 Token 使用量，并且能产生更好的结果，尤其是在工具表面很大时。

我们自己的 Cloudflare MCP 服务器正是以这种方式构建的：它仅通过两个工具——搜索和执行——就暴露了整个 Cloudflare API，且 Token 数不到 1000，因为 Agent（智能体）是针对类型化 API 编写代码，而不是在数百个单独的工具定义中导航。

#### 构建自定义自动化

开发者正在使用动态 Worker 让 Agent（智能体）即时构建自定义自动化。例如，Zite 正在构建一个应用平台，用户通过聊天界面进行交互——LLM（大语言模型）在后台编写 TypeScript 来构建 CRUD 应用、连接到 Stripe、Airtable 和 Google Calendar 等服务，并运行后端逻辑，而用户完全看不到一行代码。每个自动化都在其自己的动态 Worker 中运行，仅能访问该端点所需的特定服务和库。

“为了启用 Zite 由 LLM（大语言模型）生成的应用的服务器端代码，我们需要一个即时、隔离且安全的执行层。Cloudflare 的动态 Worker 在这三点上都达到了要求，并且在速度和库支持方面，其性能超过了我们基准测试的所有其他平台。NodeJS 兼容的运行时支持 Zite 的所有工作流，允许数百个第三方集成，同时不牺牲启动时间。得益于动态 Worker，Zite 现在每天处理数百万次执行请求。”

——Antony Toron，Zite 首席技术官兼联合创始人

#### 运行 AI 生成的应用

开发者正在构建从 AI 生成完整应用程序的平台——无论是为他们的客户还是为构建原型的内部团队。借助动态 Worker，每个应用都可以按需启动，然后在不再调用时放回冷存储。快速的启动时间使得在活跃开发期间预览更改变得容易。平台还可以阻止或拦截生成代码发出的任何网络请求，确保 AI 生成的应用安全运行。

## 定价

动态加载的 Worker 定价为每天每个加载的唯一 Worker 0.002 美元（截至本文发布时），此外还需支付常规 Worker 通常的 CPU 时间和调用费用。

对于 AI 生成的“代码模式”用例，其中每个 Worker 都是唯一的、一次性的，这意味着价格为每个加载的 Worker 0.002 美元（加上 CPU 和调用费用）。与生成代码的推理成本相比，这笔费用通常可以忽略不计。

在测试期间，0.002 美元的费用被免除。由于定价可能发生变化，请务必查看我们的动态 Worker 定价页面以获取最新信息。

## 开始使用

如果您使用的是 Workers 付费计划，今天就可以开始使用动态 Worker。

#### 动态 Worker 入门模板

使用这个“hello world”入门模板来部署一个能够加载和执行动态 Worker 的 Worker。

#### 动态 Worker 演练场

您也可以部署动态 Worker 演练场，在那里您可以编写或导入代码，在运行时使用 `@cloudflare/worker-bundler` 进行捆绑，通过动态 Worker 执行，并查看实时响应和执行日志。

动态 Worker 快速、可扩展且轻量。如果您有任何问题，请在 Discord 上找到我们。我们很期待看到您的构建成果！

---

> 本文由AI自动翻译，原文链接：[The Cloudflare Blog: Sandboxing AI agents, 100x faster](https://blog.cloudflare.com/dynamic-workers/)
> 
> 翻译时间：2026-03-25 04:43
