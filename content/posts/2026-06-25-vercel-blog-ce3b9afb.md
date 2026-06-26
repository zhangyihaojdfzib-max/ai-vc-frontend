---
title: AI SDK 7发布：五大维度提升智能体开发深度
title_original: AI SDK 7 is now available
date: '2026-06-25'
source: Vercel Blog
source_url: https://vercel.com/blog/ai-sdk-7
author: ''
summary: Vercel开源AI SDK 7正式发布，该SDK每周下载量超1600万次，是跨模型提供商构建AI应用的TypeScript工具。新版在五个方面为智能体开发增加生产级深度：支持推理控制、工具与运行时上下文、MCP应用等开发能力；提供工具审批、持久化、超时等运行管理；可集成Codex、Claude
  Code等任何智能体框架；支持遥测、追踪等观测功能；并实现与提供商无关的实时语音和视频生成。文章还介绍了从v6升级的迁移工具。
categories:
- AI产品
tags:
- AI SDK
- 智能体开发
- Vercel
- TypeScript
- 开源框架
draft: false
translated_at: '2026-06-26T06:13:25.301146'
---

AI SDK 每周下载量超过1600万次，是用于跨任何模型提供商构建AI应用、功能、框架和Agent（智能体）的TypeScript SDK。Vercel的开源Agent（智能体）框架也构建于同一层之上。

AI SDK 7在五个方面为Agent（智能体）工作增加了生产级深度：

- 开发Agent（智能体）：支持推理控制、工具和运行时上下文、提供商文件和技能支持、MCP应用以及终端UI。
- 运行Agent（智能体）：支持工具审批、持久化（WorkflowAgent）、超时和沙箱支持。
- 集成任何Agent（智能体）框架：例如Codex、Claude Code、Deep Agents、OpenCode或Pi。
- 观测Agent（智能体）：支持遥测、Node.js追踪通道、生命周期事件和性能统计。
- 超越文本Agent（智能体）：支持与提供商无关的实时语音和视频生成。

开发Agent（智能体）：支持推理控制、工具和运行时上下文、提供商文件和技能支持、MCP应用以及终端UI。

运行Agent（智能体）：支持工具审批、持久化（WorkflowAgent）、超时和沙箱支持。

集成任何Agent（智能体）框架：例如Codex、Claude Code、Deep Agents、OpenCode或Pi。

观测Agent（智能体）：支持遥测、Node.js追踪通道、生命周期事件和性能统计。

超越文本Agent（智能体）：支持与提供商无关的实时语音和视频生成。

```
pnpm add ai@latest
```

安装AI SDK 7

从AI SDK 6升级？运行`npx @ai-sdk/codemod v7`可自动迁移，代码改动最小，或使用迁移技能：`npx skills add vercel/ai --skill migrate-ai-sdk-v6-to-v7`

## 链接到标题开发Agent（智能体）

构建行为良好的Agent（智能体）需要对模型推理、工具上下文和文件处理进行精细控制。

### 链接到标题推理控制

大多数前沿模型支持可配置的推理，但每个提供商API的暴露方式不同。

AI SDK 7通过为`generateText`和`streamText`提供`reasoning`选项来标准化这一点。它映射到提供商原生的推理设置，让你用一行代码控制推理力度。当你需要更详细的提供商特定推理配置时，你仍然可以回退到提供商选项。

```
1import { generateText } from 'ai';2const result = await generateText({3  model,4  prompt,5  reasoning: 'high',6});
```

使用单个选项设置推理力度

在`reasoning`文档中了解更多。

### 链接到标题工具上下文

工具越来越多地独立于特定Agent（智能体）或应用进行开发。例如，第三方公司提供工具，使Agent（智能体）能够使用他们的API。因此，工具需要LLM（大语言模型）无法生成的额外输入，例如API密钥或配置设置。

AI SDK 7添加了一个完全类型化的工具上下文，可以通过模式为每个工具指定。该上下文仅限于该工具，以防止第三方工具访问它们不需要的上下文。

```
1const agent = new ToolLoopAgent({2  model,3  tools: {4    weather: tool({5      description,6      inputSchema,7      contextSchema: z.object({8        apiKey: z.string(),9      }),10      execute: async (input, { context: { apiKey } }) => {11        12      },13    }),14  },15  toolsContext: {16    weather: { apiKey: process.env.WEATHER_API_KEY! },17  },18});
```

将API密钥限定到需要它的工具

了解更多关于工具上下文的信息

### 链接到标题运行时上下文

对于更复杂的Agent（智能体）循环，你通常需要可以在`prepareStep`中访问和修改变量，以调整提示词、模型选择等。

AI SDK 7引入了一个类型化的运行时上下文，可在步骤准备和工具审批函数期间使用，并支持可选的遥测功能。这使你能够将更多逻辑封装在`ToolLoopAgent`中，并与该内部逻辑共享这些Agent（智能体）。

```
1const agent = new ToolLoopAgent({2  3  runtimeContext: {4    var1: "something",5  },6  prepareStep: async ({ runtimeContext, steps }) => {7    8    9  },10});
```

跨步骤访问和更新类型化变量

了解更多关于运行时上下文的信息。

### 链接到标题提供商文件上传

许多Agent（智能体）工作流需要处理大型输入，例如PDF、图像、数据集或其他工件。内联发送这些文件既慢又浪费，特别是对于无状态推理，它们会被反复发送。

AI SDK 7添加了一个顶级`uploadFile`API，允许你上传文件一次，然后将轻量级引用传递给后续模型调用。这避免了重复上传相同的字节，使推理更快，并在重复或多步骤运行期间节省带宽。

`uploadFile`可以与任何提供文件上传端点的提供商一起使用。该函数返回一个可在提供商之间移植的提供商引用对象。

```
1const { providerReference } = await uploadFile({2  api: openai.files(),3  data: readFileSync('./photo.png'),4  filename: 'photo.png',5});6const result = await streamText({7  model: openai.responses('gpt-5.5'),8  messages: [9    {10      role: 'user',11      content: [12        { type: 'text', text: 'Describe what you see in this image.' },13        { type: 'file', mediaType: 'image', data: providerReference },14      ],15    },16  ],17});
```

上传文件一次，将引用传递给后续模型调用

了解更多关于提供商文件上传的信息

### 链接到标题提供商技能上传

在每次请求中将技能内联发送到提供商管理的容器环境，与内联发送文件存在相同的开销问题。

AI SDK 7添加了一个顶级`uploadSkill`API，允许你上传技能一次，然后在后续推理调用中使用对它的引用。与`uploadFile`类似，该函数返回一个提供商引用对象。

```
1const { providerReference } = await uploadSkill({2  api: anthropic.skills(),3  files: [4    {5      path: 'my-skill/SKILL.md',6      content: readFileSync('./SKILL.md'),7    },8  ],9  displayTitle: 'My Skill',10});11const result = await streamText({12  model: anthropic('claude-sonnet-4-6'),13  tools: {14    code_execution: anthropic.tools.codeExecution_20260120(),15  },16  prompt: 'Use the my-skill skill to complete the task.',17  providerOptions: {18    anthropic: {19      container: {20        skills: [{ type: 'custom', providerReference }],21      },22    } satisfies AnthropicLanguageModelOptions,23  },24});
```

上传技能一次，跨推理调用引用它

了解更多关于提供商技能上传的信息。

### 链接到标题MCP应用

MCP已成为将Agent（智能体）连接到工具和资源的常用方式。但并非每个工具都应对模型可见，并且某些MCP服务器需要在其工具旁边暴露专门的UI。

AI SDK 7增加了对MCP应用的支持。MCP服务器现在可以分离模型可见的工具和仅限应用的工具，保留应用元数据，并在沙箱化的iframe中渲染应用UI。一个JSON-RPC桥接器连接工具、资源和显示交互。

这使你能够构建更丰富的Agent（智能体）体验，其中模型可以使用它需要的工具，而用户则可以看到一个特定于应用的界面，用于审查、配置或交互。

![一个MCP应用在沙箱化iframe中渲染仪表板UI，旁边是Agent（智能体）输出](/images/posts/11db8c0aab93.jpg)

![一个MCP应用在沙箱化iframe中渲染仪表板UI，旁边是Agent（智能体）输出](/images/posts/b41721b35ffb.jpg)

```
1import { experimental_MCPAppRenderer as MCPAppRenderer } from '@ai-sdk/react';2import { isToolUIPart } from 'ai';3{4  messages.map(message =>5    message.parts.map(part =>6      isToolUIPart(part) ? (7        <MCPAppRenderer8          key={part.toolCallId}9          part={part}10          sandbox={{ url: '/mcp-app-sandbox', className: 'h-96 w-full' }}11          loadResource={app => fetch(`/api/mcp-apps?uri=${app.resourceUri}`)}12          handlers={{ allowedTools: ['refreshDashboard'] }}13        />14      ) : null,15    ),16  );17}
```

在模型输出旁边渲染MCP应用UI

立即开始使用AI SDK构建你的第一个MCP应用。

### 链接到标题TUI

在开发 Agent（智能体）时，您需要能够快速测试它们，而无需编写完整的应用程序。AI SDK 7 新增了一个终端 UI（TUI）包，只需几行代码即可运行 Agent（智能体）：

该 TUI 是交互式的，支持推理和工具，并将 Markdown 渲染为格式化文本。

![Agent（智能体）在终端 UI 中交互运行，显示推理步骤和工具调用](/images/posts/75174d26361a.jpg)

```
1import { runAgentTUI } from '@ai-sdk/tui';2await runAgentTUI({ agent });
```

在终端中运行 Agent（智能体）

了解更多关于创建您自己的终端 Agent（智能体）的信息。

## 链接到标题运行 Agent（智能体）

随着 Agent（智能体）变得更加自主和运行时间更长，对审批、持久性、沙箱和鲁棒性的需求也随之增加。

### 链接到标题工具审批

AI SDK 7 支持 Agent（智能体）级别的工具审批，可以是自动的，也可以让人参与其中，审批类型如下：

- 针对特定工具的简单用户审批。
- 针对特定工具的工具审批函数，可以自动批准、自动拒绝或转发给用户审批。
- 通用的兜底工具审批函数。

针对特定工具的简单用户审批。

针对特定工具的工具审批函数，可以自动批准、自动拒绝或转发给用户审批。

通用的兜底工具审批函数。

工具审批在 `ToolLoopAgent`、`generateText` 和 `streamText` 上定义，因为特定工具的使用场景驱动了对审批的需求。

```
1const agent = new ToolLoopAgent({2  model,3  tools: { weather: weatherTool },4  toolApproval: {5    weather: 'user-approval',6  },7});
```

在工具执行前要求用户审批

对于更高风险的工作流，AI SDK 7 引入了可选的 HMAC 签名工具审批，以防止伪造审批。SDK 还通过在继续执行前重新验证工具输入和策略来强化重放行为。

了解工具审批的工作原理。

### 链接到标题 WorkflowAgent（持久性）

当一个 Agent（智能体）运行跨越多个步骤或等待人工审批时，在此过程中进程重启或部署意味着需要重新开始。AI SDK 7 引入了 `@ai-sdk/workflow` 和 `WorkflowAgent`，用于持久化、可恢复的 Agent（智能体）执行，能够承受进程重启、部署、中断和延迟审批。

`WorkflowAgent` 支持基于工作流的流式传输、工具、审批、回调、`prepareCall` 以及跨工作流步骤边界的提供商模型序列化。它还支持类型化的运行时上下文，用于共享 Agent（智能体）状态和稳定的遥测。

回调现在包含更丰富的执行数据，例如步骤编号、先前结果、持续时间以及成功或失败信息。无效的工具调用会被保留，但不会执行无效工具，并且工具 `toModelOutput` 转换可以保留原始输出以供 UI 和回调使用。

了解如何使用 WorkflowAgent 构建 Agent（智能体）。

### 链接到标题超时

Agent（智能体）可能以比简单请求更多的方式停滞：提供商可能打开一个流然后停止发送数据块，工具可能挂起，或者多步骤运行可能超过其总预算。

AI SDK 7 在文本生成和 Agent（智能体）API 中增加了第一等的超时配置，包括总时间、每步时间、每数据块时间和每工具时间限制。超时中止使用 `TimeoutError`，并且中止原因会通过流和 UI 协议传播。

```
1const result = await generateText({2  model,3  tools: { weather: weatherTool, slowApi: slowApiTool },4  timeout: {5    totalMs: 60000, 6    stepMs: 10000, 7    chunkMs: 2000, 8    toolMs: 5000, 9    tools: {10      weatherMs: 3000, 11      slowApiMs: 10000, 12    },13  },14  prompt: 'What is the weather in San Francisco?',15});
```

配置总时间、每步时间和每工具超时限制

了解更多关于超时的信息。

### 链接到标题沙箱支持

执行 shell 命令、读写文件或执行生成代码的 Agent（智能体）需要一个一致的执行环境，但底层沙箱在本地开发、CI 和生产环境中经常发生变化。AI SDK 7 增加了一个第一等的 `SandboxSession` 抽象，用于在工具和 Agent（智能体）中实现可移植的命令执行。工具可以独立于任何特定沙箱进行开发，并且您可以将任何支持沙箱的工具与任何沙箱提供商一起使用。

沙箱环境，例如 Vercel Sandbox，非常适合此目的。

## 链接到标题集成任何 Agent（智能体）框架

Agent（智能体）运行时正在超越单个应用服务器。团队希望在编码环境、托管沙箱、本地会话和第三方框架中运行相同的 Agent（智能体）逻辑。

### 链接到标题 HarnessAgent

AI SDK 7 引入了实验性的框架抽象和 `HarnessAgent`：一个 API 即可运行完全配置的、成熟的 Agent（智能体）框架，例如 Claude Code、Codex 和 Pi。框架可配置沙箱以在其中运行、自定义指令、技能和工具。通过一致的接口运行成熟的框架，独立配置每个框架，并在不更改集成层的情况下进行切换。

在底层，该抽象由一个 v1 适配器规范、桥接支持和用于创建和恢复会话的扩展沙箱会话原语组成。框架会话可以暂停和恢复，甚至单个轮次也可以在运行过程中中断和恢复。

`HarnessAgent` 实现了 AI SDK 的 `Agent` 接口，因此其 `generate` 和 `stream` 返回值与现有的 AI SDK 集成完全兼容，并且 `useChat()` 和新的 TUI 无需任何额外接线即可工作。

```
1const agent = new HarnessAgent({2  harness: claudeCode,3  sandbox: createVercelSandbox({4    runtime: 'node24',5    ports: [4000],6  }),7  instructions:8    'You are a careful coding assistant. Prefer small changes and explain tradeoffs.',9  skills: [10    {11      name: 'review-github-pr',12      description: 'Review a GitHub pull request. Use when asked to review a pull request.',13      content:14        'Use the `readGitHubPullRequest` tool to fetch the context about the relevant pull request the user has asked you to review. ' +15        'If the pull request refers to an issue, fetch the relevant issue context as well using the `readGitHubIssue` tool.',16    },17  ],18  tools: { readGitHubIssue, readGitHubPullRequest },19});
```

将 Claude Code 配置为带有沙箱和自定义技能的 HarnessAgent

了解更多关于 AI SDK 框架的信息。

## 链接到标题观测 Agent（智能体）

了解您的 Agent（智能体）在生产环境中的行为是具有挑战性的。AI SDK 7 将可观测性作为构建 Agent（智能体）的第一等特性。

### 链接到标题遥测

AI SDK 7 围绕一个单一的、可扩展的集成系统重构了遥测。无需将生命周期回调连接到每个 `generateText` 或 `streamText` 调用中，而是在应用程序启动时注册一次遥测：

```
1import { registerTelemetry, generateText } from 'ai';2import { OpenTelemetry } from '@ai-sdk/otel';3registerTelemetry(new OpenTelemetry());4const result = await generateText({5  model: "google/gemini-3.5-flash",6  prompt: 'Write a short story about a cat.',7  telemetry: {8    functionId: `story-agent`,9  },10});
```

在应用程序启动时注册一次 OpenTelemetry

重新设计包括：

- 用于第三方提供商集成的专用遥测接口
- 通过一次注册覆盖所有 AI SDK 功能
- 使用最新的 GenAI 语义约定的可选 OpenTelemetry 集成
- Node.js 追踪通道支持

用于第三方提供商集成的专用遥测接口

通过一次注册覆盖所有 AI SDK 功能

使用最新的 GenAI 语义约定的可选 OpenTelemetry 集成

Node.js 追踪通道支持

可观测性集成：Datadog、Langfuse、Braintrust、Raindrop、Sentry、Laminar、Langsmith。

追踪现在捕获 AI 操作的完整形态，包括根生成、每个模型调用、各个步骤、工具执行、嵌入/向量、重排序、使用情况、错误以及选定的运行时或工具上下文。

![Langfuse 中的 Agent（智能体）追踪，显示多个步骤和工具调用](/images/posts/252e087a0d11.jpg)

![Langfuse 中的 Agent 追踪记录，展示多个步骤和工具调用](/images/posts/17ea8798ec03.jpg)

你可以在 AI SDK 遥测文档中找到更多详情。

### 链接到标题 Node.js 追踪通道

AI SDK 7 通过 `node:diagnostics_channel` 增加了对 Node.js 追踪通道的支持。该 SDK 在 `ai:telemetry` 通道上为 `generateText`、`streamText`、模型调用、工具执行、嵌入和重排序发出结构化的遥测事件。

可观测性提供商可以通过其检测包一次性订阅，并自动将 AI SDK 活动转换为追踪记录，同时在流式响应和工具调用中保持异步上下文。

```
1import { tracingChannel } from 'node:diagnostics_channel';2import {3  AI_SDK_TELEMETRY_TRACING_CHANNEL,4  type TelemetryTracingChannelMessage,5} from 'ai';6tracingChannel(AI_SDK_TELEMETRY_TRACING_CHANNEL).subscribe({7  start(message) {8    const { type, event } = message as TelemetryTracingChannelMessage;9    console.log(`AI SDK ${type} started`, event);10  },11  asyncEnd(message) {12    const { type } = message as TelemetryTracingChannelMessage;13    console.log(`AI SDK ${type} completed`);14  },15});
```

通过 Node.js 追踪通道订阅 AI SDK 遥测事件

你可以在追踪通道文档中了解更多。

### 链接到标题 性能统计

AI SDK 7 增加了针对模型输出、流式行为和工具执行的逐步骤性能统计。你可以回答诸如：模型开始响应花了多长时间？Token 到达速度有多快？哪个工具耗时最长？

```
1import { streamText } from 'ai';2const result = streamText({3  model: 'openai/gpt-5',4  prompt: 'Write a short product announcement.',5});6for await (const chunk of result.textStream) {7  process.stdout.write(chunk);8}9const { performance } = await result.finalStep;10console.log({11  responseTimeMs: performance.responseTimeMs,12  outputTokensPerSecond: performance.outputTokensPerSecond,13  timeToFirstOutputMs: performance.timeToFirstOutputMs,14});
```

从流式响应中获取逐步骤延迟和吞吐量

了解更多关于性能统计的信息。

### 链接到标题 生命周期事件

生产环境中的 Agent 需要生命周期钩子，因为记录状态、计费和调试都依赖于准确了解运行、步骤和工具何时开始和结束。AI SDK 7 使得回调在模型调用、Agent、工具和其他函数中一致触发，因此你可以观察每个事件何时开始、哪个模型运行、使用了多少 Token 以及如何结束。

```
1import { generateText } from 'ai';2const result = await generateText({3  model: 'openai/gpt-5',4  prompt: 'What is the meaning of life',5  runtimeContext: {6    userId: 'user_123',7    feature: 'launch-copy',8  },9  onStart({ callId, modelId, runtimeContext }) {10    console.log('Request started', {11      callId,12      modelId,13      userId: runtimeContext.userId,14    });15  },16  onEnd({ callId, usage, finishReason }) {17    console.log('Request finished', {18      callId,19      finishReason,20      totalTokens: usage.totalTokens,21    });22  },23});
```

观察请求何时开始和结束

你可以在生命周期回调文档中找到更多详情。

## 链接到标题 与提供商无关的实时支持

实时模型 API 功能强大，但每个提供商在会话、音频、工具和浏览器认证方面的实现方式各不相同。

AI SDK 7 增加了实验性的、与提供商无关的实时支持，用于浏览器直接 WebSocket 会话。该 SDK 支持服务器创建的临时 Token、针对 OpenAI、Google 和 xAI 的提供商实现，以及一个返回 `UIMessage[]` 的 React 实时 Hook。

实时会话支持音频转录和客户端驱动的工具调用，因此你可以构建语音 Agent、协作式 Copilot 和低延迟交互界面，而无需将 UI 绑定到某个提供商的事件格式。

AI Gateway 还通过 `gateway.experimental_realtime()` 支持标准化的实时会话，包括 WebSocket 子协议认证、模型查询选择和经过验证的提供商选项。

```
1const realtime = experimental_useRealtime({2  model: gateway.experimental_realtime('openai/gpt-realtime-2'),3  api: {4    token: '/api/realtime/setup',5  },6  onToolCall: async ({ toolCall }) => {7    8  },9});
```

从浏览器连接到实时会话

了解更多关于实时的信息。

## 链接到标题 视频生成

AI 应用正在超越文本和图像。AI SDK 7 引入了实验性的 `generateVideo` 支持，并提供了针对 fal、Google AI Studio、Google Vertex 和 Replicate 的提供商实现。

AI SDK 7 中的视频生成使用视频特定的模型分辨率，支持通过默认提供商进行基于字符串的模型查找，并包含更安全的有界下载处理，具有可配置的大小限制和中止支持。

```
1import { experimental_generateVideo as generateVideo } from 'ai';2const { videos } = await generateVideo({3  model: "google/veo-3.1-generate-001",4  prompt: 'A cat walking on a treadmill',5  aspectRatio: '16:9',6});
```

通过单个 API 调用生成视频

了解更多关于生成视频的信息。

## 链接到标题 快速开始

使用一条命令安装 AI SDK 7。

```
pnpm add ai@latest
```

安装 AI SDK 7

- 开始使用 AI SDK 7
- 查看完整变更日志
- 迁移到 v7
- 加入社区

开始使用 AI SDK 7

查看完整变更日志

迁移到 v7

加入社区

## 链接到标题 贡献者

AI SDK 7 是我们在 Vercel 的核心团队（Gregor、Lars、Felix、Aayush、Josh、Nico）与众多优秀社区贡献者共同努力的成果：

0xr3ngar,31Carlton7,A-Vamshi,Abdulwadood-zawity,abhicris,adithya-tako,AhmadYasser1,ahmedrowaihi,allenzhou101,anaclumos,arnaugomez,auscaster,AVtheking,B-Step62,bb220,ben-vargas,benyebai,bittere,blurrah,bolaabanjo,boylec,BrianHung,BrianP8701,chenxin-yan,christian-bromann,Christian-Sidak,cipher416,CloudFaye,codewarnab,codicecustode,codylittle,cristiandrei1234,csidak,ctate,cyphercodes,defrex,dflynn15,dinmukhamedm,dnukumamras,DongSeonYoo,dukex,edawerd,EdwardIrby,edwardwc,ellis-driscoll,embedder-dev,etairl,EurFelux,eyueldk,fahe1em1,Falven,fran3cc,gdborton,genmin,geraint0923,Ghitahouir,GidianB,grant0417,gsdv,guillemwilly,hank9999,harpreetarora,haydenbleasel,he-yufeng,heiwen,hkd987,hntrl,http-samc,i5d6,ismaelrumzan,Jaaneek,jaderiverstokes,jakobhoeg,Jaksenc,jarod,jaydeep-pipaliya,jeremyphilemon,jerilynzheng,jerome-benoit,jferrettiboke,jlsandri,JoanLaRosa,joaopedroassad,JohnnyHBon,josh-williams,jovanwongzixi,JulesGuesnon,Kage18,kagura-agent,kairosci,kaizen403,karthik-idikuda,kimchnn,kkawamu1,kkdawkins,leog25,leothorp,liaoliaojun,lihuimingxs,Mahendradeokar,MarcACard,marcusschiesser,markmcd,max-programming,MaxwellCalkin,mclenhard,MehediH,Melkeydev,michael-han-dev,michaelcummings12,Mmartinrusso,monadoid,montyanderson,more-by-more,mrpaaradox,msullivan,muniter,muraliavarma,murataslan1,mvanhorn,myprototypewhat,Nezz,nicoloboschi,nielskaspers,Nutlope,nwalters512,ohansFavour,ousugo,pablof7z,Pash10g,patrikdevlin,paulelliotco,pavel-y-ivanov,PierreLeGuen,posva,Pranav-Wadhwa,privatenumber,quuu,R-Taneja,raphaeleidus,reynkonig,Ricardo-M-L,richardsolomou,robechun,rubdos,samjbobb,SamyPesse,seojcarlos,shaper,shrey150,shubham-021,shujanislam,ShyamSathish005,sleitor,Subr1ata,syeddhasnainn,sylviezhang37,szymonrybczak,t-mdo,techwraith,theQuert,thestonechat,timvucina-soniox,tomdale,tresorama,tsuzaki430,turisanapo,Und3rf10w,undo76,ushiromiya-lion,visyat,wong2,Xiang-CH,xlianghang,zapagenrevdale,Zawwarsami16,zirkelc,zxuhan。

你们在 GitHub 上的反馈、错误报告和拉取请求对塑造这个版本起到了关键作用。我们非常期待看到你们利用这些新功能构建出精彩的应用！

---

> 本文由AI自动翻译，原文链接：[AI SDK 7 is now available](https://vercel.com/blog/ai-sdk-7)
> 
> 翻译时间：2026-06-26 06:13
