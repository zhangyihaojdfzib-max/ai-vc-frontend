---
title: AI Gateway now supports asynchronous video generation - Vercel
title_original: AI Gateway now supports asynchronous video generation - Vercel
date: '2026-08-25'
source: Vercel Blog
source_url: https://vercel.com/changelog/ai-gateway-now-supports-asynchronous-video-generation
author: ''
summary: '[翻译失败，原文如下]


  Video generationon AI Gateway can now run asynchronously.


  By default,generateVideokeeps one HTTP request to AI Gateway open until the re...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T03:11:35.829608'
---

[翻译失败，原文如下]

Video generationon AI Gateway can now run asynchronously.

By default,generateVideokeeps one HTTP request to AI Gateway open until the result is ready. Because video generation can take seconds or minutes, that request can exceed request timeouts.

With asynchronous generation, your application can receive a webhook, poll for completion, or start a generation and retrieve the result in a later request.

Choose an option based on whether your process can keep running and whether your application can receive webhooks:

Option

What waits

When you get the job ID

Best for

startVideowith Workflow SDK

Nothing

On the start response, inside the step

Durable runs with no receiver to build

generateVideowithwebhook(new)

The call, until your endpoint receives the completion event

In the webhook event and the final result

Returning videos from one call without polling

generateVideowithpoll(new)

The call, while the SDK sends short status requests

In the final result, after rendering completes

Processes that can wait but cannot receive webhooks

startVideoandgetVideoStatus(new)

Nothing,startVideoreturns immediately

In the start response, before rendering begins

Serverless functions, queues, and parallel jobs that must outlive the calling process

generateVideowith no options

One request stays open until rendering completes

Scripts and other processes that can keep a request open

ExistinggenerateVideocalls continue to work as before. All four options support text-to-video, image-to-video, reference-to-video, and other video inputs.

## Copy link to headingUpgrade the SDK

Install the latest versions of the AI SDK and AI Gateway provider:

```
pnpm add ai@latest @ai-sdk/gateway@latest
```

## Copy link to headingUse asynchronous video generation

### Copy link to headingWait for completion in a Workflow

An easy way to consume the completion webhook is aWorkflow SDK. The workflow creates its own webhook URL, passes it tostartVideo, and suspends until AI Gateway delivers the completion event.Install the Workflow SDK alongside the AI SDK:

```
pnpm add workflow
```

```
1import {2  experimental_getVideoStatus as getVideoStatus,3  experimental_startVideo as startVideo,4  type StartVideoResult,5} from 'ai';6import { createWebhook } from 'workflow';7
8const model = 'klingai/kling-v3.0-t2v';9export async function videoWorkflow(prompt: string) {10  'use workflow';11  12  using webhook = createWebhook();13  const { operation } = await startJob(prompt, webhook.url);14  15  await webhook;16  const { status, videos } = await fetchResult(operation);17  if (status !== 'completed') {18    throw new Error(`Video generation ${status}`);19  }20  return videos;21}22async function startJob(prompt: string, webhookUrl: string) {23  'use step';24  const { operation } = await startVideo({ model, prompt, webhookUrl });25  return { operation };26}27async function fetchResult(operation: StartVideoResult['operation']) {28  'use step';29  return await getVideoStatus(model, { operation });30}
```

While the video renders, the workflow run is suspended and resumes when AI Gateway delivers the terminal event.

### Copy link to headingUse a webhook withgenerateVideo

PasswebhooktogenerateVideoto wait for a completion event without polling. AI Gateway sends an event when the job completes or fails. The SDK waits for that event, fetches the generated videos, and resolves the originalgenerateVideocall.

```
1import { experimental_generateVideo as generateVideo } from 'ai';2import { randomUUID } from 'node:crypto';3
456const token = randomUUID();7
8const result = await generateVideo({9  model: 'klingai/kling-v3.0-t2v',10  prompt: 'A lighthouse beam sweeping across a foggy coast at night',11  webhook: async () => ({12    url: `https://example.com/api/video-webhook?token=${token}`,13    received: waitForDelivery(token), 14  }),15});
```

The calling process and webhook handler need a shared token and store so the delivery can be matched to the correct generation.generateVideodoes not expose the signing secret for this job. See thewebhook verification documentationfor the complete receiver pattern.

Both the polling and webhook options forgenerateVideoreturnresult.videosasGeneratedFileobjects. The SDK downloads provider-hosted videos, makinguint8Array,base64, andmediaTypeavailable in either job.

### Copy link to headingPoll withgenerateVideo

Addpollto an existinggenerateVideocall:

```
1const result = await generateVideo({2  model: 'spacexai/grok-imagine-video-1.5',3  prompt: {4    image: 'https://example.com/balloon.jpg',5    text: 'The camera pushes in as the balloon drifts upward',6  },7  duration: 5,8  poll: {9    intervalMs: 5000, 10    timeoutMs: 600000, 11  },12});
```

Poll AI Gateway every five seconds until the video is ready or the ten-minute timeout is reached.

AI Gateway starts an asynchronous job, and the SDK sends a short status request at each interval until the job finishes. The calling process must remain running untilgenerateVideoresolves, but no individual request to AI Gateway stays open for the full generation.

### Copy link to headingStart a job and retrieve it later

startVideoreturns an operation as soon as AI Gateway accepts the job, without waiting for rendering to finish. Store that operation and pass it togetVideoStatuslater from the same process or another one:

```
1import {2  experimental_getVideoStatus as getVideoStatus,3  experimental_startVideo as startVideo,4} from 'ai';5
6const model = 'bytedance/seedance-2.5';7
8const { operation } = await startVideo({9  model,10  prompt: 'A paper plane looping over a city at dusk',11});12
1314const status = await getVideoStatus(model, { operation });15if (status.status === 'completed') {16  console.log(status.videos);17}
```

Start a video generation and check its status later using the returned operation.

The operation is JSON-serializable, so it can be stored in a database or passed through a queue. Your application controls how long to keep checking the job because it has no built-in timeout.

You can also passwebhookUrltostartVideoto receive a completion event instead of checking the status. The start response includes the signing secret needed to verify the webhook.

UnlikegenerateVideo,getVideoStatusdoes not download hosted videos. It returns provider URLs or inline bytes. Hosted URLs can expire, so download any videos you need to keep.

## Copy link to headingMonitor asynchronous jobs

Every asynchronous generation appears on theAI Gateway Logs pageas soon as it starts. Jobs show as Running while generation is in progress and update when they complete or fail.

![Asynchronous pending requests show up as 'Running' at the top of the AI Gateway logs page ](/images/posts/e502ceaeb9b3.jpg)

![Asynchronous pending requests show up as 'Running' at the top of the AI Gateway logs page ](/images/posts/0b85647aedbe.jpg)

![Asynchronous pending requests show up as 'Running' at the top of the AI Gateway logs page ](/images/posts/f3d51b1eef8c.jpg)

![Asynchronous pending requests show up as 'Running' at the top of the AI Gateway logs page ](/images/posts/87135d24348d.jpg)

UnderRequest Mode, selectAsyncto show only asynchronous jobs. Opening an entry shows the job ID and the request details.

![AI Gateway logs filtered on Request Mode: 'Async' to show completed requests and details](/images/posts/dff59862f2e2.jpg)

![AI Gateway logs filtered on Request Mode: 'Async' to show completed requests and details](/images/posts/7bd7e9fd620d.jpg)

Only asynchronous requests create jobs. A standardgenerateVideocall appears as a single completed request after the video is ready.

For size limits, idempotency for retried job starts, webhook delivery retries, and other operational details, read theasynchronous video generation documentationorbrowse all video models.

---

> 本文由AI自动翻译，原文链接：[AI Gateway now supports asynchronous video generation - Vercel](https://vercel.com/changelog/ai-gateway-now-supports-asynchronous-video-generation)
> 
> 翻译时间：2026-08-26 03:11
