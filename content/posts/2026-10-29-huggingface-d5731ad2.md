---
title: Granite Switch 4.1.1 — Update models like you update software
title_original: Granite Switch 4.1.1 — Update models like you update software
date: '2026-10-29'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ibm-granite/granite-switch-4-1-1
author: ''
summary: '[翻译失败，原文如下]


  # Granite Switch 4.1.1 — Update models like you update software


  ![granite_switch_adapter_swap](/images/posts/f20febec465e.png)


  Just ove...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-30T08:47:42.839377'
---

[翻译失败，原文如下]

# Granite Switch 4.1.1 — Update models like you update software

![granite_switch_adapter_swap](/images/posts/f20febec465e.png)

Just over a week ago, we releasedGranite Switch 4.1, showing that our modular Switch architecture lets you configure a language model with specialized, cache-efficient adapters — adding new expertise on a single endpoint.

Granite Switch 4.1.1is a patch release. The version number means what it means in software: fully backwards compatible with 4.1, no migration, incremental improvements under the hood.

1. Updated Granite Speech ASR model— multilingual speech-to-text across 10 languages with native punctuation and capitalization, so transcripts are ready for downstream models without a formatting pass.
2. Updated Decision adapter ingranitelib-core—  featuring improved overall performance on the Jev Decision Index test set.

While we are excited about these new features, what is notable is the speed and efficiency with which our teams could release this update. Apart from training the new ASR model and Decision adapter, nothing was recomputed: the base model is untouched. You compose the latest adapters you want and deploy.

This pattern can power far more than patch releases to an IBM-provided model. We're working on tutorials and an Adapter SDK so developers and third-party providers can build their own adapters — iterate on versions, test features, and ship updates the way you ship software. More soon.

Until then, test out ourlatest models, and try out the new multilingual and punctuation capabilities powering ourSpeech-to-Decisionsdemo.

---

> 本文由AI自动翻译，原文链接：[Granite Switch 4.1.1 — Update models like you update software](https://huggingface.co/blog/ibm-granite/granite-switch-4-1-1)
> 
> 翻译时间：2026-10-30 08:47
