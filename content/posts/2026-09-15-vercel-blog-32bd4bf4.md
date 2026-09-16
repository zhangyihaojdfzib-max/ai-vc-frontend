---
title: Gemini 3.8 Live models now available on AI Gateway - Vercel
title_original: Gemini 3.8 Live models now available on AI Gateway - Vercel
date: '2026-09-15'
source: Vercel Blog
source_url: https://vercel.com/changelog/gemini-3-8-live-models-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Gemini 3.8 LiveandGemini 3.8 Live Extended Thinkingfrom Google are now available
  on AI Gateway.


  Both models support real-time spoken int...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-16T07:28:53.042201'
---

[翻译失败，原文如下]

Gemini 3.8 LiveandGemini 3.8 Live Extended Thinkingfrom Google are now available on AI Gateway.

Both models support real-time spoken interactions for voice assistants, conversational experiences, and applications that respond through audio.

- google/gemini-3.8-livesupports real-time audio, visual grounding, automatic switching across 97 languages, and background tool calls while the conversation continues.
- google/gemini-3.8-live-extended-thinkingadds multi-step reasoning that runs in parallel with speech, allowing it to acknowledge requests and narrate progress without interrupting the conversation.

google/gemini-3.8-livesupports real-time audio, visual grounding, automatic switching across 97 languages, and background tool calls while the conversation continues.

google/gemini-3.8-live-extended-thinkingadds multi-step reasoning that runs in parallel with speech, allowing it to acknowledge requests and narrate progress without interrupting the conversation.

Use either model through the AI SDK's realtime API. Install the Gateway provider and a WebSocket client:

```
pnpm add @ai-sdk/gateway@latest ws
```

Mint a short-lived token, open the WebSocket, and use the model adapter to serialize and parse realtime events:

```
1import { gateway } from '@ai-sdk/gateway';2import WebSocket from 'ws';3
4const modelId = 'google/gemini-3.8-live';5const { token, url } = await gateway.experimental_realtime.getToken({6  model: modelId,7});8
9const model = gateway.experimental_realtime(modelId);10const config = model.getWebSocketConfig({ token, url });11const ws = new WebSocket(config.url, config.protocols);12
13const send = async (14  event: Parameters<typeof model.serializeClientEvent>[0],15) => ws.send(JSON.stringify(await model.serializeClientEvent(event)));16
17ws.on('open', async () => {18  await send({19    type: 'session-update',20    config: {21      outputModalities: ['audio'],22      outputAudioTranscription: {},23      24      25      26      27    },28  });29  await send({30    type: 'conversation-item-create',31    item: {32      type: 'text-message',33      role: 'user',34      text: 'Say hello in one sentence.',35    },36  });37});38
39ws.on('message', (data) => {40  const parsed = model.parseServerEvent(JSON.parse(data.toString()));41
42  for (const event of Array.isArray(parsed) ? parsed : [parsed]) {43    if (event.type === 'audio-transcript-delta') {44      process.stdout.write(event.delta);45    }46    if (event.type === 'response-done') {47      console.log();48      ws.close();49    }50    if (event.type === 'error') {51      console.error(event.message);52      ws.close();53    }54  }55});56
57ws.on('close', (code, reason) => {58  if (code !== 1000) {59    console.error(`WebSocket closed (${code}): ${reason.toString()}`);60  }61});
```

See therealtime quickstartfor more details on realtime events and WebSocket connections.

TryGemini 3.8 LiveorGemini 3.8 Live Extended Thinkingin the model playground.

AI Gateway provides a unified API for calling models, tracking usage and cost, and configuring retries, failover, and performance optimizations for higher-than-provider uptime.

---

> 本文由AI自动翻译，原文链接：[Gemini 3.8 Live models now available on AI Gateway - Vercel](https://vercel.com/changelog/gemini-3-8-live-models-now-available-on-ai-gateway)
> 
> 翻译时间：2026-09-16 07:28
