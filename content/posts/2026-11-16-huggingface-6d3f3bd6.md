---
title: Hugging Face and OpenRouter join forces to make open-weight models easy to
  run
title_original: Hugging Face and OpenRouter join forces to make open-weight models
  easy to run
date: '2026-11-16'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/openrouter
author: ''
summary: '[翻译失败，原文如下]


  # Hugging Face and OpenRouter join forces to make open-weight models easy to run


  Hugging Face and OpenRouter are teaming up to make open...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-21T09:25:23.921476'
---

[翻译失败，原文如下]

# Hugging Face and OpenRouter join forces to make open-weight models easy to run

Hugging Face and OpenRouter are teaming up to make open-weight models easy to run. Every major open-weight release is already being published on the Hugging Face Hub, andOpenRouterserves those models at scale, routing each request across 80+ providers based on live measurements of each one. Together, every open-weight model on the Hub that a provider serves can be called with your Hugging Face token, through the same API, with the best provider picked for each request.

Today, we are switchingInference Providersfrom our own custom router to OpenRouter's. Requests made to language models now go through OpenRouter, which picks the best provider for each call based on live price, speed and reliability, and retries on another provider if the first one fails. Your code stays the same.

## Run them with the tools you already use

The router supports OpenAI's Chat Completions and Responses APIs and Anthropic's Messages API for every chat model, whatever the provider behind it. Pick your coding agent or SDK and a model, then copy the steps, or copy the whole setup as a prompt for your agent:

Setup guides forClaude Code,Codex,OpenCode,PiandHermes Agent

The same Hugging Face token also gives you storage withStorage Buckets, compute withJobsand dedicated inference withInference Endpoints. PRO, Team and Enterprise plans include monthly credits for compute and inference.

## How open-weight models are used

On OpenRouter, open-weight models went from 26.8% of the tokens served in October 2025 to 71.7% at the end of September 2026, after peaking at 77.5% in July (OpenRouter, October 2026). Over the same period, weekly open-weight volume grew more than 60-fold, against almost tenfold for closed models. This week, the most used model on OpenRouter is an open-weight one, DeepSeek V4.1 Flash 1017, with 59.2 trillion tokens (rankings).

Open-weight models cost about four times less on average: $0.28 per million input tokens and $1.62 per million output tokens, against $1.27 and $6.36 for closed models.

The best open-weight models still trail the best proprietary ones on the hardest benchmarks. On theArtificial Analysis Intelligence Index, Kimi K3.1 Pro, the best open-weight model, scores 46 against 65 for Claude Fable 5.2, at about a seventh of the cost per task ($3.68 against $26.54). For a lot of workloads, that trade-off is worth it.

![Artificial Analysis Intelligence Index against cost per task, for the top proprietary and open-weight models](/images/posts/42d88610d5e8.png)

![Artificial Analysis Intelligence Index against cost per task, for the top proprietary and open-weight models](/images/posts/a22fa6ba64a2.png)

## Routing powered by OpenRouter

OpenRouter serves more than 800 trillion tokens a month to over 10 million users, across 600+ models from 80+ providers. Its routing is based on live measurements of every provider across that traffic.

OpenRouter recentlyrebuilt its provider routing: instead of only looking at the lowest list price, it sends each request to the provider with the best mix of price, speed and reliability.

When a provider slows down or starts failing, traffic moves away from it until it recovers, and a failed try is retried on the next best provider inside the same call. In OpenRouter's measurements, the new routing cut capacity errors by 46% and improved time to first token by 16.9% and throughput by 16.3%.

![Default routing retries on another provider when the first one is rate limited, :cheapest picks the lowest price and :fastest the highest throughput](/images/posts/3dcdce69f58f.gif)

![Default routing retries on another provider when the first one is rate limited, :cheapest picks the lowest price and :fastest the highest throughput](/images/posts/d32ac5443857.gif)

Before, Inference Providers picked one provider for your request and returned its error if it failed. Now, the request is retried on another provider. You can still choose a policy or a provider with a suffix on the model id:

```text
zai-org/GLM-5.3            # default: best mix of price, speed and reliability
zai-org/GLM-5.3:fastest    # highest throughput
zai-org/GLM-5.3:cheapest   # lowest price
zai-org/GLM-5.3:novita     # only Novita

```

Routing is also cache-aware: a conversation stays on the provider that holds its prompt cache. To make it explicit, send a stable UUID per conversation in theX-HF-Session-Idheader (see theprompt caching guide).

## Pricing

Pricing doesn't change: you pay the provider's price on your Hugging Face bill, and Hugging Face doesn't add a markup on top of it. PRO users get $2 of credits every month, and Team and Enterprise organizations get $2 per seat. SeePricing and Billingfor the details.

## Image, video and audio generation

Image, video, and audio generation continue to work exactly as before, directly through Hugging Face Inference Providers without going through OpenRouter. You can keep using the same token and API, and access tens of thousands ofLoRAs.

## See where your requests go

On model pages, you can chat with the model right away in the widget. Two new tabs show what's behind it: Providers lists every provider OpenRouter can route the model to, with its input and output price, speed and uptime over the last 24 hours, and Metrics shows the best price, throughput, time to first token, context length and uptime among them:

Yourusage overviewbreaks your spend down by the provider each request went to:

![Daily Inference Providers spend, broken down by provider](/images/posts/ee12576e0223.png)

![Daily Inference Providers spend, broken down by provider](/images/posts/112f236750f5.png)

In yoursettings, you can turn off any provider you don't want: the router never sends your requests there. Organizations have the same settings, and they apply to every request billed to the organization.

![Inference Providers settings, with a toggle for each provider](/images/posts/055f14235625.png)

![Inference Providers settings, with a toggle for each provider](/images/posts/f8445b71dae0.png)

## Breaking change: custom provider keys

Requests to language models now go through OpenRouter and are billed to your Hugging Face account or organization, so you can no longer use your own API key for a provider with these models. You can still pick a provider with a suffix on the model id (model:provider) or turn providers off in your settings, and your code stays the same. Custom keys for image and video providers keep working.

## What's next

This is the first step of our partnership with OpenRouter. Next:

- Connect your OpenRouter account to Hugging Face.
- More tasks routed through OpenRouter.

Try amodel, or read theInference Providers docsto get started.

---

> 本文由AI自动翻译，原文链接：[Hugging Face and OpenRouter join forces to make open-weight models easy to run](https://huggingface.co/blog/openrouter)
> 
> 翻译时间：2026-11-21 09:25
