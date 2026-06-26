---
title: Vercel发布AI SDK 7：构建生产级智能体平台
title_original: AI SDK 7 is now available - Vercel
date: '2026-06-25'
source: Vercel Blog
source_url: https://vercel.com/changelog/ai-sdk-7
author: ''
summary: Vercel正式推出AI SDK 7，这是一个用于TypeScript构建生产级智能体的重大版本更新。SDK从模型调用和聊天原语扩展为涵盖开发、运行、集成和观测智能体的完整平台，支持文本、音频、实时、图像和视频等多种模态。新版本引入推理控制、工具审批、持久化执行、MCP应用、遥测观测等功能，并支持集成Codex、Claude
  Code等外部框架。升级需Node.js 22和ESM导入，提供codemods辅助迁移。
categories:
- AI基础设施
tags:
- Vercel
- AI SDK
- 智能体
- TypeScript
- 多模态
draft: false
translated_at: '2026-06-26T06:13:37.726496'
---

AI SDK 7 是一个用于在 TypeScript 中构建生产级 Agent（智能体）的主要版本。该 SDK 已从模型调用和聊天原语发展成为一个更广泛的 Agent（智能体）平台，用于开发、运行、集成和观测跨文本、音频、实时、图像和视频的 Agent（智能体）。每个主流提供商都提供开箱即用的支持。

## Link to heading概览

- **开发 Agent（智能体）**：支持推理控制、工具和运行时上下文、提供商文件和技能支持、MCP 应用以及终端 UI。
- **运行 Agent（智能体）**：支持工具审批、持久化 WorkflowAgent 执行、一流的超时机制和沙箱支持。
- **集成任何 Agent（智能体）框架**：例如 Codex、Claude Code、Deep Agents、OpenCode 或 Pi。
- **观测 Agent（智能体）行为**：通过重新设计的遥测、@ai-sdk/otel、Node.js 追踪通道支持、生命周期回调和步骤性能统计。
- **超越文本的构建**：通过稳定的语音/转录 API、更丰富的文件部分、图像生成与编辑、多模态嵌入（Embedding）、重排序、实时语音（实验性）和视频生成（实验性）。
- **通过更清晰的 API 升级**：通过新的迁移技能、codemods 以及针对 ESM、Node.js 22、instructions、telemetry、stream、finalStep、runtimeContext 和 toolsContext 的迁移路径。

**开发 Agent（智能体）**：支持推理控制、工具和运行时上下文、提供商文件和技能支持、MCP 应用以及终端 UI。

**运行 Agent（智能体）**：支持工具审批、持久化 WorkflowAgent 执行、一流的超时机制和沙箱支持。

**集成任何 Agent（智能体）框架**：例如 Codex、Claude Code、Deep Agents、OpenCode 或 Pi。

**观测 Agent（智能体）行为**：通过重新设计的遥测、@ai-sdk/otel、Node.js 追踪通道支持、生命周期回调和步骤性能统计。

**超越文本的构建**：通过稳定的语音/转录 API、更丰富的文件部分、图像生成与编辑、多模态嵌入（Embedding）、重排序、实时语音（实验性）和视频生成（实验性）。

**通过更清晰的 API 升级**：通过新的迁移技能、codemods 以及针对 ESM、Node.js 22、instructions、telemetry、stream、finalStep、runtimeContext 和 toolsContext 的迁移路径。

## Link to heading升级前须知

AI SDK 7 引入了两个破坏性要求：

- **最低 Node.js 22 版本**：需要 Node 22，因为 SDK 依赖于未向后移植到早期 LTS 版本的 API（包括原生 fetch 实现和改进的 AsyncLocalStorage 语义）。
- **需要 ESM 导入**：AI SDK 7 需要 ESM 导入（import 语法或 .mjs 文件）。不支持 CommonJS require()。请更新您的 package.json 以包含 "type": "module"，或将单个文件迁移为 .mjs。

**最低 Node.js 22 版本**：需要 Node 22，因为 SDK 依赖于未向后移植到早期 LTS 版本的 API（包括原生 fetch 实现和改进的 AsyncLocalStorage 语义）。

**需要 ESM 导入**：AI SDK 7 需要 ESM 导入（import 语法或 .mjs 文件）。不支持 CommonJS require()。请更新您的 package.json 以包含 "type": "module"，或将单个文件迁移为 .mjs。

运行 v7 codemods 以自动化大部分导入和重命名更改，然后手动审查语义迁移项。请参阅完整的 v7 迁移指南。

## Link to heading开发 Agent（智能体）

- **提供商无关的推理控制**：generateText 和 streamText 现在支持顶层的 reasoning 选项，该选项映射到 OpenAI、Anthropic、Google、Groq、xAI、Bedrock、Fireworks、DeepSeek、Open Responses 以及兼容 OpenAI 的提供商的提供商原生设置。请注意，确切的行为和可用参数因提供商而异。

**提供商无关的推理控制**：generateText 和 streamText 现在支持顶层的 reasoning 选项，该选项映射到 OpenAI、Anthropic、Google、Groq、xAI、Bedrock、Fireworks、DeepSeek、Open Responses 以及兼容 OpenAI 的提供商的提供商原生设置。请注意，确切的行为和可用参数因提供商而异。

```
import { generateText } from 'ai';const result = await generateText({  model: 'openai/gpt-5.5',  prompt: 'Plan a launch checklist.',  reasoning: 'high',});
```

- **类型化的运行时上下文**：共享编排状态存在于 runtimeContext 中，并流经 prepareStep、审批函数、生命周期回调、遥测、ToolLoopAgent 和 WorkflowAgent。

**类型化的运行时上下文**：共享编排状态存在于 runtimeContext 中，并流经 prepareStep、审批函数、生命周期回调、遥测、ToolLoopAgent 和 WorkflowAgent。

```
import { ToolLoopAgent } from 'ai';const agent = new ToolLoopAgent({  model: 'openai/gpt-5.5',  runtimeContext: {    audience: 'developers',  },  prepareStep({ runtimeContext }) {    return {      instructions: `Write for ${runtimeContext.audience}.`,    };  },});
```

- **作用域工具上下文**：工具可以声明一个 contextSchema，调用者通过 toolsContext 提供每个工具的值，这样第三方工具只接收它们需要的密钥或配置。

**作用域工具上下文**：工具可以声明一个 contextSchema，调用者通过 toolsContext 提供每个工具的值，这样第三方工具只接收它们需要的密钥或配置。

```
import { generateText, tool } from 'ai';import * as z from 'zod/v4';const result = await generateText({  model: 'openai/gpt-5.5',  tools: {    weather: tool({      inputSchema: z.object({ city: z.string() }),      contextSchema: z.object({ apiKey: z.string() }),      execute: async ({ city }, { context }) =>        getWeather(city, context.apiKey),    }),  },  toolsContext: {    weather: {      apiKey: process.env.WEATHER_API_KEY,    },  },  prompt: 'What is the weather in SF?',});
```

- **提供商文件上传**：uploadFile 一次性上传大型输入，并在后续调用中重用提供商引用，从而减少重复 PDF、数据集、图像和多步骤工作流中的冗余上传。

**提供商文件上传**：uploadFile 一次性上传大型输入，并在后续调用中重用提供商引用，从而减少重复 PDF、数据集、图像和多步骤工作流中的冗余上传。

```
import { readFile } from 'node:fs/promises';import { openai } from '@ai-sdk/openai';import { streamText, uploadFile } from 'ai';const { providerReference } = await uploadFile({  api: openai.files(),  data: await readFile('./brief.pdf'),  filename: 'brief.pdf',});const result = await streamText({  model: 'openai/gpt-5.5',  messages: [    {      role: 'user',      content: [        { type: 'text', text: 'Summarize this brief.' },        {          type: 'file',          mediaType: 'application/pdf',          data: providerReference,        },      ],    },  ],});
```

- **提供商技能上传**：uploadSkill 将相同的模式引入到提供商管理的技能环境中。

**提供商技能上传**：uploadSkill 将相同的模式引入到提供商管理的技能环境中。

```
import { readFile } from 'node:fs/promises';import {  anthropic,  type AnthropicLanguageModelOptions,} from '@ai-sdk/anthropic';import { streamText, uploadSkill } from 'ai';const { providerReference } = await uploadSkill({  api: anthropic.skills(),  files: [    {      path: 'my-skill/SKILL.md',      content: await readFile('./SKILL.md'),    },  ],  displayTitle: 'My Skill',});const result = await streamText({  model: anthropic('claude-sonnet-4-6'),  prompt: 'Use my-skill to complete the task.',  providerOptions: {    anthropic: {      container: {        skills: [{ type: 'custom', providerReference }],      },    } satisfies AnthropicLanguageModelOptions,  },});
```

- **MCP 应用**：MCP 支持现在包括模型可见工具与应用专用工具、应用元数据、沙箱化 iframe 渲染，以及用于工具、资源、日志和显示更新的 JSON-RPC 通信。

**MCP 应用**：MCP 支持现在包括模型可见工具与应用专用工具、应用元数据、沙箱化 iframe 渲染，以及用于工具、资源、日志和显示更新的 JSON-RPC 通信。

```
import { experimental_MCPAppRenderer as MCPAppRenderer } from '@ai-sdk/react';import { isToolUIPart } from 'ai';{  messages.map(message =>    message.parts.map(part =>      isToolUIPart(part) ? (        <MCPAppRenderer          key={part.toolCallId}          part={part}          sandbox={{ url: '/mcp-app-sandbox' }}          loadResource={app => fetch(`/api/mcp-apps?uri=${app.resourceUri}`)}          handlers={{ allowedTools: ['refreshDashboard'] }}        />      ) : null,    ),  );}
```

- 终端Agent开发：@ai-sdk/tui 在交互式终端UI中运行AI SDK Agent，让你在构建完整应用之前测试推理、工具和Markdown输出。

终端Agent开发：@ai-sdk/tui 在交互式终端UI中运行AI SDK Agent，让你在构建完整应用之前测试推理、工具和Markdown输出。

```
import { ToolLoopAgent } from 'ai';import { runAgentTUI } from '@ai-sdk/tui';const agent = new ToolLoopAgent({  model: 'openai/gpt-5.5',});await runAgentTUI({ agent });
```

## Link to heading在生产环境中运行Agent

AI SDK 7 为Agent在离开本地演示后所需的原语提供了支持。

- 工具审批：generateText、streamText和ToolLoopAgent可以在调用或Agent级别定义审批策略。策略可以要求用户审批、自动审批、自动拒绝或委托给类型化的审批函数。

工具审批：generateText、streamText和ToolLoopAgent可以在调用或Agent级别定义审批策略。策略可以要求用户审批、自动审批、自动拒绝或委托给类型化的审批函数。

```
import { generateText } from 'ai';const result = await generateText({  model: 'openai/gpt-5.5',  tools: { deleteFile },  toolApproval: {    deleteFile: 'user-approval',  },  prompt: 'Remove stale temporary files.',});
```

- 强化审批重放：较高风险的审批流程可以在继续执行前重新验证工具输入和策略，使用WorkflowAgent审批验证，并选择加入HMAC签名。HMAC签名以加密方式将原始工具输入绑定到审批Token，防止在审批请求和恢复之间篡改工具参数。
- 持久化执行：@ai-sdk/workflow引入了WorkflowAgent用于长时间运行的Agent。执行状态在步骤之间持久化到持久化存储中，因此Agent能够经受部署、进程重启、中断和延迟审批。要了解更多信息，请参阅WorkflowAgent文档。

强化审批重放：较高风险的审批流程可以在继续执行前重新验证工具输入和策略，使用WorkflowAgent审批验证，并选择加入HMAC签名。HMAC签名以加密方式将原始工具输入绑定到审批Token，防止在审批请求和恢复之间篡改工具参数。

持久化执行：@ai-sdk/workflow引入了WorkflowAgent用于长时间运行的Agent。执行状态在步骤之间持久化到持久化存储中，因此Agent能够经受部署、进程重启、中断和延迟审批。要了解更多信息，请参阅WorkflowAgent文档。

```
import { WorkflowAgent } from '@ai-sdk/workflow';const agent = new WorkflowAgent({  model: 'openai/gpt-5.5',  tools,  runtimeContext: {    userId: 'user_123',  },});
```

- 工作流感知的Agent特性：WorkflowAgent支持流式传输、工具、审批、类型化运行时和工具上下文、生命周期回调、稳定遥测、提供者执行的审批恢复以及工具结果转换。
- 一流的超时机制：文本生成和Agent API可以定义总超时、每步超时、每块超时、默认工具超时和每个工具超时预算。超时中止使用TimeoutError，中止原因会流经流和UI协议。

工作流感知的Agent特性：WorkflowAgent支持流式传输、工具、审批、类型化运行时和工具上下文、生命周期回调、稳定遥测、提供者执行的审批恢复以及工具结果转换。

一流的超时机制：文本生成和Agent API可以定义总超时、每步超时、每块超时、默认工具超时和每个工具超时预算。超时中止使用TimeoutError，中止原因会流经流和UI协议。

```
import { generateText } from 'ai';const result = await generateText({  model: 'openai/gpt-5.5',  timeout: {    totalMs: 60_000,    stepMs: 10_000,    chunkMs: 2_000,    toolMs: 5_000,  },  prompt: 'Research this issue and summarize it.',});
```

- 沙箱化执行：沙箱抽象支持命令执行、流式输出、工作目录、环境变量、中止信号以及步骤级沙箱覆盖。

沙箱化执行：沙箱抽象支持命令执行、流式输出、工作目录、环境变量、中止信号以及步骤级沙箱覆盖。

```
import { generateText, tool } from 'ai';import * as z from 'zod/v4';const result = await generateText({  model: 'openai/gpt-5.5',  tools: {    runCommand: tool({      inputSchema: z.object({ command: z.string() }),      execute: async ({ command }, { experimental_sandbox }) => {        if (experimental_sandbox == null) {          throw new Error('Sandbox is not available');        }        return experimental_sandbox.run({ command });      },    }),  },  experimental_sandbox: sandbox,  prompt: 'Run the tests and summarize the result.',});
```

## Link to heading集成Agent框架

AI SDK 7 引入了一个框架层，用于将成熟的Agent引入AI SDK生态系统。将Claude Code、Codex、Deep Agents、OpenCode和Pi等框架封装在AI SDK其余部分使用的相同Agent接口之后。

- HarnessAgent：通过AI SDK Agent接口运行外部Agent框架，提供标准的generate和stream结果。

HarnessAgent：通过AI SDK Agent接口运行外部Agent框架，提供标准的generate和stream结果。

```
import { HarnessAgent } from '@ai-sdk/harness/agent';import { claudeCode } from '@ai-sdk/harness-claude-code';import { createVercelSandbox } from '@ai-sdk/sandbox-vercel';const agent = new HarnessAgent({  harness: claudeCode,  sandbox: createVercelSandbox({ runtime: 'node24' }),  instructions: 'Review the repository and make a small, safe fix.',});const result = await agent.generate({  prompt: 'Fix the failing unit test.',});
```

- Agent适配器：Claude Code、Codex、Deep Agents、OpenCode和Pi框架适配器让团队能够将现有的Agent运行时插入AI SDK应用。
- 可配置的框架运行：框架Agent可以接收沙箱、指令、自定义技能和工具，因此同一个运行时可以根据不同的产品和工作流程进行定制。
- 持久化、可恢复的会话：工作流工具、会话桥接以及用于中断轮次继续的API使框架运行适用于更长时间的任务。
- 网关就绪的身份验证：框架适配器支持用于AI Gateway的Vercel OIDC，简化了托管和沙箱化Agent的执行。

Agent适配器：Claude Code、Codex、Deep Agents、OpenCode和Pi框架适配器让团队能够将现有的Agent运行时插入AI SDK应用。

可配置的框架运行：框架Agent可以接收沙箱、指令、自定义技能和工具，因此同一个运行时可以根据不同的产品和工作流程进行定制。

持久化、可恢复的会话：工作流工具、会话桥接以及用于中断轮次继续的API使框架运行适用于更长时间的任务。

网关就绪的身份验证：框架适配器支持用于AI Gateway的Vercel OIDC，简化了托管和沙箱化Agent的执行。

## Link to heading观测Agent

- 全局遥测集成：注册一次遥测，即可接收跨模型调用、步骤、工具、嵌入、重排序和Agent执行的结构化事件。

全局遥测集成：注册一次遥测，即可接收跨模型调用、步骤、工具、嵌入、重排序和Agent执行的结构化事件。

```
import { generateText, registerTelemetry } from 'ai';import { LangfuseVercelAiSdkIntegration } from '@langfuse/vercel-ai-sdk';registerTelemetry(new LangfuseVercelAiSdkIntegration());const result = await generateText({  model: 'openai/gpt-5.5',  prompt: '撰写一则发布公告。',  telemetry: {    functionId: 'launch-copy-agent',  },});
```

- 专用 OpenTelemetry 包：OpenTelemetry 支持现已迁移至 `@ai-sdk/otel`，包含 GenAI 语义约定跨度与指标、补充的 AI SDK 属性以及跨度丰富钩子。了解更多信息，请参阅 `@ai-sdk/otel` 文档。

专用 OpenTelemetry 包：OpenTelemetry 支持现已迁移至 `@ai-sdk/otel`，包含 GenAI 语义约定跨度与指标、补充的 AI SDK 属性以及跨度丰富钩子。了解更多信息，请参阅 `@ai-sdk/otel` 文档。

```
import { generateText, registerTelemetry } from 'ai';import { OpenTelemetry } from '@ai-sdk/otel';registerTelemetry(new OpenTelemetry());const result = await generateText({  model: 'openai/gpt-5.5',  prompt: '撰写一则发布公告。',});
```

- Node.js 追踪通道：AI SDK 7 通过 Node.js 追踪通道发出结构化遥测数据，允许可观测性提供者一次性订阅，同时在流式传输和工具执行过程中保持异步上下文。

Node.js 追踪通道：AI SDK 7 通过 Node.js 追踪通道发出结构化遥测数据，允许可观测性提供者一次性订阅，同时在流式传输和工具执行过程中保持异步上下文。

```
import { tracingChannel } from 'node:diagnostics_channel';import {  AI_SDK_TELEMETRY_TRACING_CHANNEL,  type TelemetryTracingChannelMessage,} from 'ai';tracingChannel(AI_SDK_TELEMETRY_TRACING_CHANNEL).subscribe({  start(message) {    const { type, event } = message as TelemetryTracingChannelMessage;    console.log(`AI SDK ${type} 已启动`, event);  },});
```

- 敏感上下文控制：运行环境和工具上下文可以有选择地包含在遥测数据中，并带有控制机制，默认防止机密信息泄露。

敏感上下文控制：运行环境和工具上下文可以有选择地包含在遥测数据中，并带有控制机制，默认防止机密信息泄露。

```
import { generateText } from 'ai';const result = await generateText({  model: 'openai/gpt-5.5',  prompt: '撰写一则发布公告。',  runtimeContext: {    userId: 'user_123',    feature: 'launch-copy',  },  telemetry: {    includeRuntimeContext: {      userId: true,      feature: true,    },  },});
```

- 生命周期回调：回调在核心函数、Agent（智能体）、工具、嵌入/向量、重排序、结构化输出和 UI 流中更加一致。回调负载为步骤、用量、内容、文件、来源、警告、工具、模型调用和错误事件提供更丰富的数据。

生命周期回调：回调在核心函数、Agent（智能体）、工具、嵌入/向量、重排序、结构化输出和 UI 流中更加一致。回调负载为步骤、用量、内容、文件、来源、警告、工具、模型调用和错误事件提供更丰富的数据。

```
import { generateText } from 'ai';const result = await generateText({  model: 'openai/gpt-5.5',  prompt: 'AI SDK 7 有哪些变化？',  onStart({ callId, modelId }) {    console.log('已启动', { callId, modelId });  },  onStepEnd({ stepNumber, finishReason, usage }) {    console.log('步骤完成', { stepNumber, finishReason, usage });  },  onEnd({ usage, finishReason }) {    console.log('已完成', { usage, finishReason });  },});
```

- 性能统计：步骤结果公开了计时和吞吐量指标，包括响应时间、总步骤时间、工具执行时间、首次输出时间以及每秒输出 Token 数。

性能统计：步骤结果公开了计时和吞吐量指标，包括响应时间、总步骤时间、工具执行时间、首次输出时间以及每秒输出 Token 数。

```
import { streamText } from 'ai';const result = streamText({  model: 'openai/gpt-5.5',  prompt: '用两段话解释部分预渲染。',  onLanguageModelCallEnd({ usage, performance }) {    console.log({      totalTokens: usage.totalTokens,      responseTimeMs: performance.responseTimeMs,      outputTokensPerSecond: performance.outputTokensPerSecond,    });  },});
```

## 链接到标题超越文本构建

AI SDK 7 将 SDK 扩展到实时、视频、语音、转录、图像、文件、嵌入/向量和结构化输出领域。

- 实时（实验性）：面向 OpenAI、Google 和 xAI 的浏览器到提供者 WebSocket 会话，支持音频/文本对话、客户端驱动的工具调用，以及通过 AI Gateway 进行标准化路由。

实时（实验性）：面向 OpenAI、Google 和 xAI 的浏览器到提供者 WebSocket 会话，支持音频/文本对话、客户端驱动的工具调用，以及通过 AI Gateway 进行标准化路由。

```
import { gateway } from '@ai-sdk/gateway';import { experimental_useRealtime } from '@ai-sdk/react';const realtime = experimental_useRealtime({  model: gateway.experimental_realtime('openai/gpt-realtime-2'),  api: {    token: '/api/realtime/setup',  },});
```

- 视频生成（实验性）：视频生成适用于 AI Gateway、Google AI Studio、Google Vertex、fal、Replicate、ByteDance Seedance、Kling AI、Prodia 和 xAI，支持长时间运行的 SSE 响应和更安全的有界下载。

视频生成（实验性）：视频生成适用于 AI Gateway、Google AI Studio、Google Vertex、fal、Replicate、ByteDance Seedance、Kling AI、Prodia 和 xAI，支持长时间运行的 SSE 响应和更安全的有界下载。

```
import { fal } from '@ai-sdk/fal';import { experimental_generateVideo } from 'ai';const { video } = await experimental_generateVideo({  model: fal.video('luma-dream-machine/ray-2'),  prompt: '一只在跑步机上行走的猫',});
```

- 稳定的语音和转录：`generateSpeech`、`transcribe`、`SpeechResult` 和 `TranscriptionResult` 是稳定的导出项。

稳定的语音和转录：`generateSpeech`、`transcribe`、`SpeechResult` 和 `TranscriptionResult` 是稳定的导出项。

```
import { readFile } from 'node:fs/promises';import { openai } from '@ai-sdk/openai';import { generateSpeech, transcribe } from 'ai';const speech = await generateSpeech({  model: openai.speech('tts-1'),  text: '欢迎使用 AI SDK 7。',});const { text } = await transcribe({  model: openai.transcription('whisper-1'),  audio: await readFile('meeting.mp3'),});
```

- 图像作为文件：图像部分向与其他媒体相同的规范文件模型靠拢。工具输出可以对内联数据、URL、提供者引用和基于文本的内容使用单一的 `file` 形状。
- 更丰富的媒体和模型支持：提供者增加了图像生成、图像编辑、多模态嵌入/向量、语音、转录、重排序、文件引用、推理文件以及特定于提供者的媒体元数据。
- 结构化输出可靠性：针对 Zod 和 Standard Schema 输入的 JSON Schema 后处理更加严格，为结构化输出和工具调用提供了格式错误的 JSON 提取和修复功能，并且数组输出模式保留了转换、强制转换、默认值和管道。

图像作为文件：图像部分向与其他媒体相同的规范文件模型靠拢。工具输出可以对内联数据、URL、提供者引用和基于文本的内容使用单一的 `file` 形状。

更丰富的媒体和模型支持：提供者增加了图像生成、图像编辑、多模态嵌入/向量、语音、转录、重排序、文件引用、推理文件以及特定于提供者的媒体元数据。

结构化输出可靠性：针对 Zod 和 Standard Schema 输入的 JSON Schema 后处理更加严格，为结构化输出和工具调用提供了格式错误的 JSON 提取和修复功能，并且数组输出模式保留了转换、强制转换、默认值和管道。

## 链接到标题UI、流和消息处理

v7 中的 UI 和流式处理工作侧重于使 Agent（智能体）流正确、可组合且可靠。

- 直接 Agent（智能体）传输：`DirectChatTransport` 可以直接从 UI 代码调用 `Agent`（智能体）。

直接Agent传输：DirectChatTransport可以直接从UI代码调用Agent。

```
import { DirectChatTransport, useChat } from '@ai-sdk/react';const { messages, sendMessage } = useChat({  transport: new DirectChatTransport({ agent }),});
```

- UI流程中的工具审批：UI消息支持自动审批响应和改进的审批重放行为。
- 框架改进：React useChat回调会随当前props/state更新；sendAutomaticallyWhen支持异步条件；Vue新增了符合语言习惯的useChat组合式函数；Angular API已与当前AI SDK模式对齐。
- 更可靠的流：在结束块之前结束的提供者流被视为错误，工具执行错误会被可预测地发出并清理，流式推理的边缘情况处理更加一致。
- 提供者元数据保留：提供者元数据在文本生成、UI流、工具调用和多轮提供者ID映射中得以保留。
- 多步结果：顶层的content、tool calls/results、files、sources、warnings和usage现在代表完整运行。仅最终步骤的详细信息可通过finalStep获取。

UI流程中的工具审批：UI消息支持自动审批响应和改进的审批重放行为。

框架改进：React useChat回调会随当前props/state更新；sendAutomaticallyWhen支持异步条件；Vue新增了符合语言习惯的useChat组合式函数；Angular API已与当前AI SDK模式对齐。

更可靠的流：在结束块之前结束的提供者流被视为错误，工具执行错误会被可预测地发出并清理，流式推理的边缘情况处理更加一致。

提供者元数据保留：提供者元数据在文本生成、UI流、工具调用和多轮提供者ID映射中得以保留。

多步结果：顶层的content、tool calls/results、files、sources、warnings和usage现在代表完整运行。仅最终步骤的详细信息可通过finalStep获取。

```
const finalStep = await result.finalStep;console.log({  totalUsage: await result.usage,  finalStepUsage: finalStep.usage,});
```

## 链接到标题配置MCP

MCP包从工具传输层发展为一个更丰富的集成层，用于Agent工具和应用UI。

- 协议和元数据：MCP客户端支持协议版本2025-11-25、服务器元数据、服务器指令、ping响应、协商的协议头以及公开的listTools()。
- 类型化工具输出：MCP工具可以暴露outputSchema和structuredContent，并且工具定义可以与可执行工具分离。
- 资源内容：工具结果和提示消息可以包含MCP resource_link内容。
- 应用渲染：MCP应用使用工具元数据在沙箱化iframe中渲染特定应用的UI，同时将模型可见工具和仅应用工具分开。
- 传输可靠性：HTTP、SSE和OAuth传输支持自定义fetch、重定向配置、OAuth刷新去重、状态验证、异步客户端认证、更丰富的错误信息以及更好的SSE帧处理。

协议和元数据：MCP客户端支持协议版本2025-11-25、服务器元数据、服务器指令、ping响应、协商的协议头以及公开的listTools()。

类型化工具输出：MCP工具可以暴露outputSchema和structuredContent，并且工具定义可以与可执行工具分离。

资源内容：工具结果和提示消息可以包含MCP resource_link内容。

应用渲染：MCP应用使用工具元数据在沙箱化iframe中渲染特定应用的UI，同时将模型可见工具和仅应用工具分开。

传输可靠性：HTTP、SSE和OAuth传输支持自定义fetch、重定向配置、OAuth刷新去重、状态验证、异步客户端认证、更丰富的错误信息以及更好的SSE帧处理。

## 链接到标题配置运行时和打包

- Node.js 22最低要求：AI SDK包需要Node.js 22或更高版本。
- 需要ESM导入：AI SDK 7需要ESM导入（import语法或.mjs文件）。更新你的package.json以包含"type": "module"，或将单个文件迁移为.mjs。
- 迁移技能可用：提供了一个专门的迁移技能，开发者可以安装并让他们的Agent用于AI SDK v6到v7的升级。
- Codemods可用：v7 codemods涵盖了大部分重命名和清理迁移。

Node.js 22最低要求：AI SDK包需要Node.js 22或更高版本。

需要ESM导入：AI SDK 7需要ESM导入（import语法或.mjs文件）。更新你的package.json以包含"type": "module"，或将单个文件迁移为.mjs。

迁移技能可用：提供了一个专门的迁移技能，开发者可以安装并让他们的Agent用于AI SDK v6到v7的升级。

Codemods可用：v7 codemods涵盖了大部分重命名和清理迁移。

```
npx skills add vercel/ai --skill migrate-ai-sdk-v6-to-v7npx @ai-sdk/codemod v7
```

将此提示发送给你的AI编码Agent以开始：

```
使用 migrate-ai-sdk-v6-to-v7 技能，将我的应用从 AI SDK v6 迁移到 v7。
```

### 链接到标题脱离实验阶段

以下重点内容涵盖了最具影响力的升级：

- experimental_customProvider 变为 customProvider
- experimental_generateImage 变为 generateImage
- experimental_output 变为 output
- experimental_prepareStep 变为 prepareStep
- experimental_telemetry 变为 telemetry

experimental_customProvider 变为 customProvider

experimental_generateImage 变为 generateImage

experimental_output 变为 output

experimental_prepareStep 变为 prepareStep

experimental_telemetry 变为 telemetry

### 链接到标题重命名的API

以下重点内容涵盖了最具影响力的重命名：

- system 选项变为 instructions
- prompt 或 messages 内部的系统消息需要 allowSystemInMessages: true
- onFinish 变为 onEnd
- StreamTextResult.fullStream 变为 stream
- CallSettings 被拆分为模型生成选项和请求/传输选项

system 选项变为 instructions

prompt 或 messages 内部的系统消息需要 allowSystemInMessages: true

onFinish 变为 onEnd

StreamTextResult.fullStream 变为 stream

CallSettings 被拆分为模型生成选项和请求/传输选项

### 链接到标题弃用的API

以下重点内容涵盖了最具影响力的弃用：

- 工具审批：tool()和dynamicTool()上的needsApproval已弃用。将审批逻辑移至generateText、streamText或ToolLoopAgent上的toolApproval。
- 流响应辅助函数：像result.toUIMessageStreamResponse()和result.toTextStreamResponse()这样的结果方法已弃用。使用顶层辅助函数，如createUIMessageStreamResponse和createTextStreamResponse。
- Vue聊天：VueChat类已弃用。改用useChat组合式函数。

工具审批：tool()和dynamicTool()上的needsApproval已弃用。将审批逻辑移至generateText、streamText或ToolLoopAgent上的toolApproval。

流响应辅助函数：像result.toUIMessageStreamResponse()和result.toTextStreamResponse()这样的结果方法已弃用。使用顶层辅助函数，如createUIMessageStreamResponse和createTextStreamResponse。

Vue聊天：VueChat类已弃用。改用useChat组合式函数。

### 链接到标题其他迁移主题

- 推理配置已集中化：顶层`reasoning`选项取代了各提供商特定的重叠推理设置，除非有意指定提供商级别的覆盖配置。
- OpenTelemetry 已迁移至 `@ai-sdk/otel`：OpenTelemetry 跨度采集不再内置于 `ai` 包中。遥测功能全局注册，自定义追踪器移至 `OpenTelemetry` 构造函数中。
- 请求与响应体保留为可选加入：文本生成结果默认不包含请求和响应体。
- 多步骤结果现代表完整运行：顶层 `usage`、`content`、工具调用/结果、文件、来源及警告信息会跨所有步骤累积；仅最终步骤的数据位于 `finalStep` 下。
- 消息部分更加规范化：传统媒体和图像特定部分逐步迁移至带媒体类型的 `file` 部分。
- 包特定行为已变更：MCP HTTP/SSE 重定向被视为错误，OpenAI Responses 推理摘要默认设为详细，Anthropic 缓存创建 Token 元数据移至标准使用字段。

推理配置已集中化：顶层`reasoning`选项取代了各提供商特定的重叠推理设置，除非有意指定提供商级别的覆盖配置。

OpenTelemetry 已迁移至 `@ai-sdk/otel`：OpenTelemetry 跨度采集不再内置于 `ai` 包中。遥测功能全局注册，自定义追踪器移至 `OpenTelemetry` 构造函数中。

请求与响应体保留为可选加入：文本生成结果默认不包含请求和响应体。

多步骤结果现代表完整运行：顶层 `usage`、`content`、工具调用/结果、文件、来源及警告信息会跨所有步骤累积；仅最终步骤的数据位于 `finalStep` 下。

消息部分更加规范化：传统媒体和图像特定部分逐步迁移至带媒体类型的 `file` 部分。

包特定行为已变更：MCP HTTP/SSE 重定向被视为错误，OpenAI Responses 推理摘要默认设为详细，Anthropic 缓存创建 Token 元数据移至标准使用字段。

## 升级路径

请按照以下步骤将现有项目迁移至 AI SDK 7：

1. 将 Node.js 更新至 22+：在升级包之前，请确认您的运行时和 CI 环境满足最低要求。
2. 更新包：在 `package.json` 中将 `ai` 及所有 `@ai-sdk/*` 包升级至 v7 版本。
3. 运行 v7 codemods：codemods 可自动完成大部分重命名、导入变更及 API 迁移。提交前请审查差异。
4. 迁移 OpenTelemetry：如果您使用追踪功能，请将配置迁移至 `@ai-sdk/otel` 并全局注册遥测。有关属性详情，请参阅 `@ai-sdk/otel` 文档及 OpenTelemetry 跨度模式。
5. 手动审查语义变更：codemods 无法完全决定运行时需求、ESM 导入、指令/消息行为、运行时/工具上下文分离、审批策略放置、流辅助工具使用及多步骤结果形状。请参阅完整的 v7 迁移指南。

将 Node.js 更新至 22+：在升级包之前，请确认您的运行时和 CI 环境满足最低要求。

更新包：在 `package.json` 中将 `ai` 及所有 `@ai-sdk/*` 包升级至 v7 版本。

运行 v7 codemods：codemods 可自动完成大部分重命名、导入变更及 API 迁移。提交前请审查差异。

迁移 OpenTelemetry：如果您使用追踪功能，请将配置迁移至 `@ai-sdk/otel` 并全局注册遥测。有关属性详情，请参阅 `@ai-sdk/otel` 文档及 OpenTelemetry 跨度模式。

手动审查语义变更：codemods 无法完全决定运行时需求、ESM 导入、指令/消息行为、运行时/工具上下文分离、审批策略放置、流辅助工具使用及多步骤结果形状。请参阅完整的 v7 迁移指南。

```
npx @ai-sdk/codemod v7
```

如需引导式迁移，请安装 AI SDK v7 迁移技能，并让您的 Agent（智能体）将其应用于您的应用：

```
npx skills add vercel/ai --skill migrate-ai-sdk-v6-to-v7
```

---

> 本文由AI自动翻译，原文链接：[AI SDK 7 is now available - Vercel](https://vercel.com/changelog/ai-sdk-7)
> 
> 翻译时间：2026-06-26 06:13
