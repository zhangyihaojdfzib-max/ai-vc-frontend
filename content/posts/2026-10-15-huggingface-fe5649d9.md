---
title: 'Granite Switch 4.1: Chat, Decisions, and Speech from One Endpoint'
title_original: 'Granite Switch 4.1: Chat, Decisions, and Speech from One Endpoint'
date: '2026-10-15'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ibm-granite/granite-switch-4-1
author: ''
summary: '[翻译失败，原文如下]


  # Granite Switch 4.1: Chat, Decisions, and Speech from One Endpoint


  Introduced last spring, theGranite Switchproject enables a modular a...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:40:35.575479'
---

[翻译失败，原文如下]

# Granite Switch 4.1: Chat, Decisions, and Speech from One Endpoint

Introduced last spring, theGranite Switchproject enables a modular approach to model development. NowGranite Switch 4.1models, armed with a Decision adapter and the fastest ASR model on the OpenASR leaderboard, can move efficiently between natural-language responses, general and specialized decisions, and speech-to-text tasks—all from one hosted endpoint.

![granite_switch_adapter_swap](/images/posts/c2491f99ef87.png)

Specifically,Granite-Switch-4.1-8Band-30Bmodels are configured to include:

1. A newDecision aLoRAfor general-purpose decision-making (e.g. v1/systemone),
2. A specializedGuardian aLoRAthat, on average, outperforms Jev 1.13, Microsoft-Decision-1, GPT-Luna-Decisions, and Clef-Flash on safety-related decision tasks, and
3. Granite-Speech-5.0-Turbo-CTC, the fastest ASR model on theOpenASR Leaderboard, embedded for use in transcription tasks.

All three of these technologies (along with the underlying base model) are composed into one model, taking up approximately the same amount of VRAM on a GPU as the base model would by itself. That means more capabilities with fewer GPUs.

And because the Switch adapters were built as cache-efficientActivated LoRAs, the KV cache created from a base model generation can be reused for any subsequent adapter-based decisions. Combined with our team'srecent vLLM contributionsto speed up low rank adapter inferencing, as well as a co-located ASR encoder, Granite Switch 4.1 models canswitchbetween a chat request and a decision request and a spoken request, with blazing fast speeds.

Check out ourSpeech-to-Decisions HF spacewhere granite-switch-4.1-8b transcribes audio, generates summaries, screens for harmful content, and tests 15 other user-defined flags—all running on a single endpoint in real time.

## Granite Libraries: The OG Decision Models

Decision models aren’t new. Our previous release ofGranite Librariesfeatures a repository of specialized “decision model” adapters and other specialized task adapters that can be composed into custom Granite Switch models. And while Jev and other closed decision models focus on generality, we’ve found that many of our specialized granitelib adapters can outperform generalists on specialized classification tasks.

Compare granitelib adapterswith generalist decision models when evaluated on specialized classification tasks.

Because adapters share the base model's KV cache, adding specialists alongside a generalist decision adapter costs almost nothing. You get broad coverage from the generalist and higher accuracy from specialists on the tasks you care about.

In a “Race” between Granite-Switch-4.1-30B (frozen base Granite + 4 specialized aLoRAs) and Jev-27B (frozen base Qwen model + 1 generic decision LoRA), Granite-Switch-4.1-30B was able to complete a real world, 5-step RAG workflow much faster than its competitor.

## Compose and Extend Your Own Granite Switch Model

Granite-Switch-4.1-8B and -30B are released with “batteries included”. They are Granite Switch models that we compiled with a predefined set of helpful adapters. But you don’t need to use our version. Anyone cancompose their own Granite Switch model, mixing and matching adapters from Granite Libraries to best meet their needs.

Moving forward, we see tremendous opportunity for the community to compose and extend Granite Switch models with custom and third party adapters. We plan to release an Adapter SDK for training adapters inMellea, along side other tutorials and Granite Switch support. These adapters could be specialized classification adapters to augment decision-based workflows or adapters for specialized language tasks. You could even use custom adapters to teach a 3B parameter version of Granite to play the classic game Doom.

Similarly to Jev, our custom 3B parameter Granite Switch model made split second decisions to navigate the Doom game, but was able to do so at60 - 100 decisions / second,compared to Jev’s reported 10 decisions / second.1Unlike Jev, this Granite Switch model can also narrate and respond to your questions while it is playing.

## Resources for Getting Started

- Granite Switch 4.1 Model Cards
- Speech-to-Decisions Demo
- Granite Switch GitHub Repo
- Original Granite Switch and Granite Libraries Release Blog
- Create your own aLoRA v LoRA race onColab.

Footnotes

1https://typesafe.ai/blog/introducing-system-one-models-and-jev

---

> 本文由AI自动翻译，原文链接：[Granite Switch 4.1: Chat, Decisions, and Speech from One Endpoint](https://huggingface.co/blog/ibm-granite/granite-switch-4-1)
> 
> 翻译时间：2026-10-16 06:40
