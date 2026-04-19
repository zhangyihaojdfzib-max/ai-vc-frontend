---
title: 为智能体添加实时语音功能
title_original: Add voice to your agent
date: '2026-04-15'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/voice-agents/
author: ''
summary: Cloudflare发布实验性语音管道@cloudflare/voice，允许开发者为现有的Agents SDK智能体架构添加实时语音交互能力。该工具提供语音转文字、文字转语音及完整对话功能，支持通过WebSocket连接实现用户与智能体的实时语音对话，同时保持原有的工具、持久性和对话历史记录。其设计采用模块化提供商接口，旨在避免技术栈锁定，并内置了基于Workers
  AI的语音识别与合成服务。
categories:
- AI产品
tags:
- 智能体
- 语音交互
- Cloudflare
- 实时通信
- AI开发
draft: false
translated_at: '2026-04-19T04:50:15.953369'
---

# 为你的智能体添加语音功能

2026-04-15

- Sunil Pai
- Korinne Alpers

![](/images/posts/7405117525fe.png)

对我们许多人来说，初次接触 AI 智能体（Agent）是通过在聊天框中输入文字。对于那些日常使用智能体的人来说，我们很可能已经非常擅长编写详细的提示词（Prompt）或 Markdown 文件来引导它们。

但是，智能体最能派上用场的场景，并不总是以文字为先。你可能正在长途通勤，同时处理多个会话，或者只是想自然地与智能体对话，让它回应你，并继续互动。

为智能体添加语音功能，不应要求将其迁移到一个独立的语音框架中。今天，我们为 Agents SDK 发布了一个实验性的语音管道。

通过 `@cloudflare/voice`，你可以为你已经使用的同一套智能体架构添加实时语音功能。语音只是变成了与你同一个 Durable Object 对话的另一种方式，拥有相同的工具、持久性和 WebSocket 连接模型，这些都是 Agents SDK 已经提供的。

`@cloudflare/voice` 是 Agents SDK 的一个实验性包，它提供：

*   `withVoice(Agent)`：用于完整的对话语音智能体
*   `withVoiceInput(Agent)`：用于仅语音转文字的用例，如听写或语音搜索
*   `useVoiceAgent` 和 `useVoiceInput` 钩子，用于 React 应用
*   `VoiceClient`：用于与框架无关的客户端
*   内置的 Workers AI 提供商，让你无需外部 API 密钥即可开始使用：
    *   使用 Deepgram Flux 进行连续语音识别
    *   使用 Deepgram Nova 3 进行连续语音识别
    *   使用 Deepgram Aura 进行文本转语音

这意味着你现在可以构建一个智能体，用户可以通过单一的 WebSocket 连接实时与之对话，同时保持相同的智能体类、Durable Object 实例以及相同的基于 SQLite 的对话历史记录。

同样重要的是，我们希望这不仅仅是一个固定的默认技术栈。`@cloudflare/voice` 中的提供商接口有意设计得很小，我们希望语音、电话和传输提供商能与我们共同构建，这样开发者就可以根据他们的用例混合搭配合适的组件，而不是被锁定在单一的语音架构中。

## 开始使用语音功能

以下是 Agents SDK 中语音智能体的最小服务器端模式：

```javascript
import { Agent, routeAgentRequest } from "agents";
import {
  withVoice,
  WorkersAIFluxSTT,
  WorkersAITTS,
  type VoiceTurnContext
} from "@cloudflare/voice";

const VoiceAgent = withVoice(Agent);

export class MyAgent extends VoiceAgent<Env> {
  transcriber = new WorkersAIFluxSTT(this.env.AI);
  tts = new WorkersAITTS(this.env.AI);

  async onTurn(transcript: string, context: VoiceTurnContext) {
    return `You said: ${transcript}`;
  }
}

export default {
  async fetch(request: Request, env: Env) {
    return (
      (await routeAgentRequest(request, env)) ??
      new Response("Not found", { status: 404 })
    );
  }
} satisfies ExportedHandler<Env>;
```

这就是整个服务器。你添加一个连续转录器、一个文本转语音提供商，并实现 `onTurn()` 方法。

在客户端，你可以使用 React 钩子连接到它：

```Typescript
import { useVoiceAgent } from "@cloudflare/voice/react";

function App() {
  const {
    status,
    transcript,
    interimTranscript,
    startCall,
    endCall,
    toggleMute
  } = useVoiceAgent({ agent: "my-agent" });

  return (
    <div>
      <p>Status: {status}</p>
      {interimTranscript && <p><em>{interimTranscript}</em></p>}
      <ul>
        {transcript.map((msg, i) => (
          <li key={i}>
            <strong>{msg.role}:</strong> {msg.text}
          </li>
        ))}
      </ul>
      <button onClick={startCall}>Start Call</button>
      <button onClick={endCall}>End Call</button>
      <button onClick={toggleMute}>Mute / Unmute</button>
    </div>
  );
}
```

如果你不使用 React，可以直接从 `@cloudflare/voice/client` 使用 `VoiceClient`。

## 语音管道的工作原理

在 Agents SDK 中，每个智能体都是一个 Durable Object —— 一个具有状态、可寻址的服务器实例，拥有自己的 SQLite 数据库、WebSocket 连接和应用逻辑。语音管道扩展了这个模型，而不是取代它。

从高层次看，流程如下：

以下是管道逐步分解的说明：

1.  **音频传输**：浏览器捕获麦克风音频，并通过智能体已经使用的同一 WebSocket 连接流式传输 16 kHz 单声道 PCM 音频。
2.  **语音识别会话设置**：当通话开始时，智能体会创建一个持续整个通话期间的连续转录器会话。
3.  **语音识别输入**：音频持续流入该会话。
4.  **语音识别轮次检测**：语音转文本模型本身决定用户何时完成一段话语，并为该轮次生成一个稳定的转录文本。
5.  **大语言模型/应用逻辑**：语音管道将该转录文本传递给你的 `onTurn()` 方法。
6.  **文本转语音输出**：你的响应被合成为音频并发送回客户端。如果 `onTurn()` 返回一个流，管道会将其按句子分块，并在句子准备就绪时开始发送音频。
7.  **持久化**：用户和智能体的消息都保存在 SQLite 中，因此对话历史记录在重新连接和部署后依然存在。

## 为什么语音功能应随你的智能体一同发展

许多语音框架专注于语音循环本身：音频输入、转录、模型响应、音频输出。这些是重要的基础组件，但智能体远不止语音。

在生产环境中运行的真实智能体会不断发展。它们需要状态管理、调度、持久化、工具、工作流、电话集成，以及跨渠道保持所有这些一致性的方法。随着你的智能体复杂性增加，语音不再是一个独立的功能，而成为更大系统的一部分。

我们希望 Agents SDK 中的语音功能从这个假设出发。我们没有将语音构建为一个独立的堆栈，而是将其构建在同一个基于 Durable Object 的智能体平台之上，这样你就可以引入所需的其他基础组件，而无需在以后重新架构应用程序。

### 语音和文本共享相同状态

用户可能从打字开始，切换到语音，然后又回到文本。使用 Agents SDK，这些都只是同一智能体的不同输入。相同的对话历史记录存在于 SQLite 中，相同的工具可用。这为你提供了一个更清晰的心智模型，以及一个更简单、更易于理解的应用程序架构。

## 更低延迟来自...

### 更短的网络路径

语音体验的好坏很快就能感受到。一旦用户停止说话，系统需要快速完成转录、思考并开始回应，才能感觉像在对话。

许多语音延迟并非纯粹的模型推理时间，而是音频与文本在不同地域服务间传输所产生的开销。音频需传输至语音识别（STT）服务，转写的文本需发送给LLM（大语言模型），生成的回复又需传递给语音合成（TTS）模型——每次交接都会增加网络开销。

通过Agents SDK的语音处理流水线，智能体（Agent）可直接运行在Cloudflare网络上，且内置服务提供商使用Workers AI绑定。这使得流水线更紧凑，减少了需要自行拼接的基础设施组件。

### 内置流式处理

若语音智能体（Agent）能快速说出第一句话（也称为"首次音频时间"），交互体验会自然得多。当`onTurn()`返回流数据时，流水线会将其按句子切分，并在句子完整时立即开始合成。这意味着用户可以在答案后半部分仍在生成时，就已听到开头的回答。

## 更贴近实际的后端示例

以下是一个更完整的示例，它流式传输LLM（大语言模型）的回复，并逐句开始语音播报：

```Typescript
import { Agent, routeAgentRequest } from "agents";
import {
  withVoice,
  WorkersAIFluxSTT,
  WorkersAITTS,
  type VoiceTurnContext
} from "@cloudflare/voice";
import { streamText } from "ai";
import { createWorkersAI } from "workers-ai-provider";

const VoiceAgent = withVoice(Agent);

export class MyAgent extends VoiceAgent<Env> {
  transcriber = new WorkersAIFluxSTT(this.env.AI);
  tts = new WorkersAITTS(this.env.AI);

  async onTurn(transcript: string, context: VoiceTurnContext) {
    const ai = createWorkersAI({ binding: this.env.AI });

    const result = streamText({
      model: ai("@cf/cloudflare/gpt-oss-20b"),
      system: "You are a helpful voice assistant. Be concise.",
      messages: [
        ...context.messages.map((m) => ({
          role: m.role as "user" | "assistant",
          content: m.content
        })),
        { role: "user" as const, content: transcript }
      ],
      abortSignal: context.signal
    });

    return result.textStream;
  }
}

export default {
  async fetch(request: Request, env: Env) {
    return (
      (await routeAgentRequest(request, env)) ??
      new Response("Not found", { status: 404 })
    );
  }
} satisfies ExportedHandler<Env>;
```

`context.messages`提供基于SQLite的近期对话历史记录，而`context.signal`可在用户打断时通知流水线中止LLM（大语言模型）调用。

## 语音作为输入：`withVoiceInput`

并非所有语音交互界面都需要语音回复。有时您可能只需要听写、转录或语音搜索功能。针对这些用例，可以使用`withVoiceInput`：

```Typescript
import { Agent, type Connection } from "agents";
import { withVoiceInput, WorkersAINova3STT } from "@cloudflare/voice";

const InputAgent = withVoiceInput(Agent);

export class DictationAgent extends InputAgent<Env> {
  transcriber = new WorkersAINova3STT(this.env.AI);

  onTranscript(text: string, _connection: Connection) {
    console.log("User said:", text);
  }
}
```

在客户端，`useVoiceInput`提供了一个专注于转录的轻量级接口：

```Typescript
import { useVoiceInput } from "@cloudflare/voice/react";

const { transcript, interimTranscript, isListening, start, stop, clear } =
  useVoiceInput({ agent: "DictationAgent" });
```

当语音仅作为输入方式，且不需要完整的对话循环时，这非常有用。

## 同一连接上的语音与文本

同一客户端可以调用`sendText("What's the weather?")`，这将绕过语音识别（STT）直接发送文本到`onTurn()`。在通话过程中，回复可以同时被播报并显示为文本。在非通话状态下，则可以保持纯文本交互。

这使您能够构建真正的多模态智能体（Agent），而无需将实现拆分为不同的代码路径。

## 还能构建什么？

由于语音智能体（Agent）本质上仍是智能体（Agent），所有常规Agents SDK功能仍然适用。

### 工具与调度

您可以在会话开始时问候来电者：

```Typescript
import { Agent, type Connection } from "agents";
import { withVoice, WorkersAIFluxSTT, WorkersAITTS } from "@cloudflare/voice";

const VoiceAgent = withVoice(Agent);

export class MyAgent extends VoiceAgent<Env> {
  transcriber = new WorkersAIFluxSTT(this.env.AI);
  tts = new WorkersAITTS(this.env.AI);

  async onTurn(transcript: string) {
    return `You said: ${transcript}`;
  }

  async onCallStart(connection: Connection) {
    await this.speak(connection, "Hi! How can I help you today?");
  }
}
```

您可以安排语音提醒，并像其他智能体（Agent）一样向LLM（大语言模型）暴露工具：

```Typescript
import { Agent } from "agents";
import {
  withVoice,
  WorkersAIFluxSTT,
  WorkersAITTS,
  type VoiceTurnContext
} from "@cloudflare/voice";
import { streamText, tool } from "ai";
import { createWorkersAI } from "workers-ai-provider";
import { z } from "zod";

const VoiceAgent = withVoice(Agent);

export class MyAgent extends VoiceAgent<Env> {
  transcriber = new WorkersAIFluxSTT(this.env.AI);
  tts = new WorkersAITTS(this.env.AI);

  async speakReminder(payload: { message: string }) {
    await this.speakAll(`Reminder: ${payload.message}`);
  }

  async onTurn(transcript: string, context: VoiceTurnContext) {
    const ai = createWorkersAI({ binding: this.env.AI });

    const result = streamText({
      model: ai("@cf/cloudflare/gpt-oss-20b"),
      messages: [
        ...context.messages.map((m) => ({
          role: m.role as "user" | "assistant",
          content: m.content
        })),
        { role: "user" as const, content: transcript }
      ],
      tools: {
        set_reminder: tool({
          description: "Set a spoken reminder after a delay",
          inputSchema: z.object({
            message: z.string(),
            delay_seconds: z.number()
          }),
          execute: async ({ message, delay_seconds }) => {
            await this.schedule(delay_seconds, "speakReminder", { message });
            return { confirmed: true };
          }
        })
      },
      abortSignal: context.signal
    });

    return result.textStream;
  }
}
```

### 运行时模型切换

语音流水线还允许您根据每个连接动态选择转录模型。

例如，您可能更倾向于使用Flux进行对话轮转，而使用Nova 3进行高精度听写。您可以通过重写`createTranscriber()`在运行时切换：

```Typescript
import { Agent, type Connection } from "agents";
import {
  withVoice,
  WorkersAIFluxSTT,
  WorkersAINova3STT,
  WorkersAITTS,
  type Transcriber
} from "@cloudflare/voice";

export class MyAgent extends VoiceAgent<Env> {
  tts = new WorkersAITTS(this.env.AI);

  createTranscriber(connection: Connection): Transcriber {
    const url = new URL(connection.url ?? "http://localhost");
    const model = url.searchParams.get("model");
    if (model === "nova-3") {
      return new WorkersAINova3STT(this.env.AI);
    }
    return new WorkersAIFluxSTT(this.env.AI);
  }
}
```

在客户端，您可以通过钩子传递查询参数：

```Typescript
const voiceAgent = useVoiceAgent({
  agent: "my-voice-agent",
  query: { model: "nova-3" }
});
```

## 流水线钩子

您还可以在阶段之间拦截数据：

- `afterTranscribe(transcript, connection)`
- `beforeSynthesize(text, connection)`
- `afterSynthesize(audio, text, connection)`

这些钩子可用于内容过滤、文本规范化、特定语言转换或自定义日志记录。

## 电话与传输选项

默认情况下，语音流水线使用单个WebSocket连接作为一对一语音智能体（Agent）的最简路径。但这并非唯一选择。

### 通过Twilio接听电话

您可以使用Twilio适配器将电话呼叫连接到同一智能体（Agent）：

```Typescript
import { TwilioAdapter } from "@cloudflare/voice-twilio";
```

```typescript
export default {
  async fetch(request: Request, env: Env) {
    if (new URL(request.url).pathname === "/twilio") {
      return TwilioAdapter.handleRequest(request, env, "MyAgent");
    }

    return (
      (await routeAgentRequest(request, env)) ??
      new Response("Not found", { status: 404 })
    );
  }
};
```

这使得同一个 Agent（智能体）能够处理网络语音、文本输入和电话呼叫。

需要注意一点：默认的 Workers AI TTS 提供商返回的是 MP3 格式，而 Twilio 期望的是 mulaw 8kHz 音频。对于生产环境的电话系统，您可能需要使用能直接输出 PCM 或 mulaw 格式的 TTS 提供商。

### WebRTC

如果您需要一种更适合恶劣网络条件或需要包含多个参与者的传输方式，语音包也包含了 SFU 工具并支持自定义传输。目前的默认模型是基于 WebSocket 的，但我们计划开发更多适配器来连接到我们的全球 SFU 基础设施。

## 与我们共同构建

语音流水线在设计上是与提供商无关的。

在底层，每个阶段都由一个简单的接口定义：转录器创建一个持续会话并接收到达的音频帧，而 TTS 提供商接收文本并返回音频。如果提供商可以流式传输音频输出，流水线同样可以利用这一点。

```Typescript
interface Transcriber {
  createSession(options?: TranscriberSessionOptions): TranscriberSession;
}

interface TranscriberSession {
  feed(chunk: ArrayBuffer): void;
  close(): void;
}

interface TTSProvider {
  synthesize(text: string, signal?: AbortSignal): Promise<ArrayBuffer | null>;
}
```

我们不希望 Agents SDK 中的语音支持仅适用于一种固定的模型和传输组合。我们希望默认路径简单易用，同时随着生态系统的发展，也能轻松接入其他提供商。

内置的提供商使用 Workers AI，因此您无需外部 API 密钥即可开始使用：

- WorkersAIFluxSTT，用于对话式流式语音转文本
- WorkersAINova3STT，用于听写式流式语音转文本
- WorkersAITTS，用于文本转语音

但更大的目标是实现互操作性。如果您维护一项语音或语音服务，这些接口足够小，无需理解 SDK 的其他内部细节即可实现。如果您的 STT 提供商接受流式音频并能检测话语边界，它就能满足转录器接口的要求。如果您的 TTS 提供商能流式传输音频输出，那就更好了。

我们非常希望与以下方面合作实现互操作性：

- STT 提供商，如 AssemblyAI、Rev.ai、Speechmatics，或任何提供实时转录 API 的服务
- TTS 提供商，如 PlayHT、LMNT、Cartesia、Coqui、Amazon Polly 或 Google Cloud TTS
- 适用于 Vonage、Telnyx 或 Bandwidth 等平台的电话适配器
- 用于 WebRTC 数据通道、SFU 桥接和其他音频传输层的传输实现

我们也对超越单个提供商的合作感兴趣：

- 跨 STT + LLM（大语言模型）+ TTS 组合的延迟基准测试
- 多语言支持以及为非英语语音 Agent（智能体）提供更好的文档
- 无障碍工作，特别是围绕多模态接口和言语障碍方面

如果您正在构建语音基础设施，并希望看到一流的集成，请提交 PR 或联系我们。

## 立即尝试

语音流水线现已作为实验性包提供：

```Shell
npm create cloudflare@latest -- --template cloudflare/agents-starter
```

添加 `@cloudflare/voice`，为您的 Agent（智能体）配置一个转录器和一个 TTS 提供商，部署它，然后开始与它对话。您也可以阅读 API 参考文档。

如果您构建了有趣的东西，请在 github.com/cloudflare/agents 上提交 issue 或 PR。语音功能不应需要一个独立的堆栈，我们认为最好的语音 Agent（智能体）将建立在与其他所有应用相同的持久化应用模型之上。

---

> 本文由AI自动翻译，原文链接：[Add voice to your agent](https://blog.cloudflare.com/voice-agents/)
> 
> 翻译时间：2026-04-19 04:50
