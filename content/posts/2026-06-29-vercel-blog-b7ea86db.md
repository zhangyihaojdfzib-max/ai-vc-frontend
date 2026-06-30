---
title: Vercel AI Gateway 新增实时语音与转录功能
title_original: Realtime voice, speech, and transcription now supported on AI Gateway
  - Vercel
date: '2026-06-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/realtime-voice-speech-and-transcription-now-supported-on-ai-gateway
author: ''
summary: Vercel 的 AI Gateway 现已支持实时语音、语音合成和语音转文本功能，处于测试阶段。用户可通过 AI SDK 7 构建实时语音智能体、从文本生成语音或转录音频。该服务提供可观测性、支出控制和自带密钥支持，无额外加价。文章介绍了两种入门方式：通过代码示例添加语音智能体，或直接在
  Playground 中无代码试用。
categories:
- AI产品
tags:
- Vercel
- AI Gateway
- 实时语音
- 语音转文本
- AI SDK
draft: false
translated_at: '2026-06-30T06:15:14.264352'
---

AI Gateway 现已支持语音和音频模型。您可以构建实时语音 Agent（智能体）、从文本生成语音，以及将音频转录为文本。与 AI Gateway 中的文本、图像和视频模型一样，这些功能提供相同的可观测性、支出控制以及自带密钥支持，且无加价或平台费用。这些功能目前处于测试阶段，可通过 AI SDK 7 使用。

借助实时支持，单个模型即可实现音频输入和输出，用户能够近乎实时地说话并听到回复，而无需等待一系列独立的模型。

功能

作用

实时语音 Agent（智能体）

模型聆听用户，构思回复，并在实时低延迟对话中将其说出。它可以在对话中途调用您的工具来查找信息或执行操作。useRealtime 钩子负责处理麦克风捕获和播放。

文本转语音

从文本生成语音音频，可选择语音和输出格式（如 MP3）。适用于配音、文字内容的音频版本以及语音回复。

语音转文本

将录音转录为文本，支持文件缓冲区、base64 字符串或 URL。适用于语音笔记或其他转录需求。

两种入门方式：

1.  按照下面的实时示例或实时快速入门，为您的应用添加语音 Agent（智能体）。
2.  使用 Playground。在浏览器中与实时模型对话，无需编写代码，就在 AI Gateway Playground 中。

按照下面的实时示例或实时快速入门，为您的应用添加语音 Agent（智能体）。

使用 Playground。在浏览器中与实时模型对话，无需编写代码，就在 AI Gateway Playground 中。

## 链接到标题实时示例

语音 Agent（智能体）包含两部分：一个用于生成短期令牌的服务端路由（这样您的 API 密钥就不会到达客户端），以及一个与之连接的浏览器组件。

添加令牌路由：

```
1import { gateway } from '@ai-sdk/gateway';2export async function POST() {3  const { token, url } = await gateway.experimental_realtime.getToken({4    model: 'openai/gpt-realtime-2',5  });6  return Response.json({ token, url, tools: [] });7}
```

然后从浏览器进行连接。useRealtime 钩子会获取该路由并管理 WebSocket 连接、麦克风捕获和音频播放：

```
1'use client';2import { experimental_useRealtime as useRealtime } from '@ai-sdk/react';3import { gateway } from '@ai-sdk/gateway';45const { status, connect, startAudioCapture } = useRealtime({6  model: gateway.experimental_realtime('openai/gpt-realtime-2'),7  api: { token: '/api/realtime/token' },8  sessionConfig: { voice: 'alloy', turnDetection: { type: 'server-vad' } },9});10
```

## 链接到标题Playground

您也可以无需编写任何代码来试用音频模型。打开模型页面，点击进入一个模型，直接在浏览器中与之交互：

-   与实时模型对话，进行语音交流
-   发送文本，让转录模型将其朗读出来
-   对音频模型说话，让它转录您的话语

与实时模型对话，进行语音交流

发送文本，让转录模型将其朗读出来

对音频模型说话，让它转录您的话语

![](/images/posts/9f7117c2313c.jpg)

![](/images/posts/4e3e8fb42e8a.jpg)

有关 AI Gateway 上实时语音、语音合成和转录模型的更多信息，请参阅文档。要查看 AI Gateway 上所有支持的实时语音、语音合成和转录模型列表，请在此处查看完整列表。

---

> 本文由AI自动翻译，原文链接：[Realtime voice, speech, and transcription now supported on AI Gateway - Vercel](https://vercel.com/changelog/realtime-voice-speech-and-transcription-now-supported-on-ai-gateway)
> 
> 翻译时间：2026-06-30 06:15
