---
title: Microsoft AI models are now available on AI Gateway - Vercel
title_original: Microsoft AI models are now available on AI Gateway - Vercel
date: '2026-10-01'
source: Vercel Blog
source_url: https://vercel.com/changelog/microsoft-ai-models-are-now-available-on-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  Vercel and Microsoft AI (MAI) have partnered to make MAI models available on AI
  Gateway. AI Gateway is one of a limited number of platfor...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-02T08:10:45.034608'
---

[翻译失败，原文如下]

Vercel and Microsoft AI (MAI) have partnered to make MAI models available on AI Gateway. AI Gateway is one of a limited number of platforms offering access to MAI models.

MAI's focus on security and zero data retention (ZDR) align with Vercel's goal of giving AI Gateway users control over their data and transparency in how it is used for training.

## Copy link to headingMAI models on AI Gateway

MAI's latest audio modelsare now supported on AI Gateway. MAI-Voice-2.1 and MAI-Voice-2.1-Flash generate speech, while MAI-Transcribe-2 Streaming returns transcript updates as audio arrives.

- MAI-Voice-2.1(microsoft/mai-voice-2.1) generates expressive speech in 23 languages and keeps a consistent speaker across longer passages. Use it for narration, audiobooks, podcasts, and lessons where delivery matters from start to finish.
- MAI-Voice-2.1-Flash(microsoft/mai-voice-2.1-flash) brings the same multilingual speech generation to lower-latency interactions. It is suited to voice agents, assistants, and spoken replies that need to arrive quickly.
- MAI-Transcribe-2 Streaming(microsoft/mai-transcribe-2-streaming) returns partial transcripts while audio is still arriving. Applications can show live captions or follow a conversation as it happens, without waiting for the full recording.

MAI-Voice-2.1(microsoft/mai-voice-2.1) generates expressive speech in 23 languages and keeps a consistent speaker across longer passages. Use it for narration, audiobooks, podcasts, and lessons where delivery matters from start to finish.

MAI-Voice-2.1-Flash(microsoft/mai-voice-2.1-flash) brings the same multilingual speech generation to lower-latency interactions. It is suited to voice agents, assistants, and spoken replies that need to arrive quickly.

MAI-Transcribe-2 Streaming(microsoft/mai-transcribe-2-streaming) returns partial transcripts while audio is still arriving. Applications can show live captions or follow a conversation as it happens, without waiting for the full recording.

AI Gateway bills these models at their listed rates, with no platform fee or markup on inference.

## Copy link to headingGet started

UsegenerateSpeechin AI SDK 7 with MAI-Voice-2.1-Flash to create a spoken response. The voice name selects Microsoft's Harper voice with the Flash model:

```
1import { experimental_generateSpeech as generateSpeech } from 'ai';2import { writeFile } from 'node:fs/promises';3
4const result = await generateSpeech({5  model: 'microsoft/mai-voice-2.1-flash',6  text: 'Your order is ready for pickup.',7  voice: 'en-US-Harper:MAI-Voice-2.1-Flash',8  outputFormat: 'mp3',9});10
11await writeFile('response.mp3', result.audio.uint8Array);
```

For longer audio such as narration, usemicrosoft/mai-voice-2.1.

### Copy link to headingTranscribe live audio

streamTranscribetakes a stream of audio chunks and returns transcript updates as the audio arrives. This example assumesmicrophoneStreamis aReadableStreamof 16 kHz, 16-bit PCM audio:

```
1import { experimental_streamTranscribe as streamTranscribe } from 'ai';2
3const stream = streamTranscribe({4  model: 'microsoft/mai-transcribe-2-streaming',5  audio: microphoneStream,6  inputAudioFormat: { type: 'audio/pcm', rate: 16000 },7});8
9for await (const part of stream.fullStream) {10  if (part.type === 'transcript-partial') {11    process.stdout.write(`\r${part.text}`);12  }13}14
15console.log(await stream.text);
```

Partial transcripts can change as more audio arrives, so replace the displayed text when a new partial arrives.

## Copy link to headingAdditional resources

ExploreMAI-Voice-2.1-Flashfor speech generation andMAI-Transcribe-2 Streamingfor live transcription. See theMAI model pagefor the full family, or follow thespeech quickstartto get started.

AI Gateway provides one API for calling models, tracking usage and cost, and viewing request traces. It also supports routing, retries, and failover across available providers.

---

> 本文由AI自动翻译，原文链接：[Microsoft AI models are now available on AI Gateway - Vercel](https://vercel.com/changelog/microsoft-ai-models-are-now-available-on-ai-gateway)
> 
> 翻译时间：2026-10-02 08:10
