---
title: Introducing Clef-omni with full multimodality, plus a faster Clef and a cheaper
  Clef-flash
title_original: Introducing Clef-omni with full multimodality, plus a faster Clef
  and a cheaper Clef-flash
date: '2026-10-09'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/clef-faster-cheaper-multimodal/
author: ''
summary: "[翻译失败，原文如下]\n\nFollowing last weekâ\x80\x99srelease of Clef and Clef-flash,\
  \ Cloudflareâ\x80\x99s open-weight decision models, we decided to bring forth more\
  \ gifts. ..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-10T08:17:41.526508'
---

[翻译失败，原文如下]

Following last weekâsrelease of Clef and Clef-flash, Cloudflareâs open-weight decision models, we decided to bring forth more gifts. Today, weâre releasing Clef-omni, which takes in audio and video input alongside text and image. We also cut the price of Clef-flash so it is now cheaper than Jev, and we made Clef faster.

Although the model game is still early for Cloudflare, innovation and iteration is in our DNA, and we apply these principles to everything we do. In fact, the story of Clef came together over the course of less than a week. We decided we wanted to do something in the decision model space on a Friday evening, trained the model over the weekend, and launched it on Thursday. Even with such a short timeline, we were able to ship performant, high-quality, open-weight models for the community â imagine what more we can do in the future.

For today, weâre excited to keep up the momentum with new additions and improvements to our Clef family of models. This is just the beginning, and weâll continue to get better, faster, cheaper, and more innovative.

## Clef-omni takes audio, video, image, and text input

Our new Clef-omni model is able to take audio, video, image, and text input. This changes the paradigm for decision models, which have been largely text-only since the debut of Jev from TypeSafe. With Clef, we supported images and video frame arrays, but Clef-omni is able to take in audio (wav or mp3) and video (mp4 or webm) alongside text and images.

Instead of setting up cascading pipelines of models that transcribe speech-to-text, or splitting audio and image channels from video, you can just call one model to make decisions across any modality. We are now one step closer to a model that is able to interact with the world as we experience it â through audio, visual, and textual communication, all in one.

Check out our developer docs for the newClef-omniÂ model. We also released the modelopen-weights on HuggingFace. For a quick start, hereâs how you can send new modality inputs to Clef-omni:

```
curl https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/ai/run/@cf/cloudflare/clef-omni \
  -X POST \
  -H "Authorization: Bearer $CLOUDFLARE_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "clef-omni",
    "state": "Review the installation: a photo of the unit, an audio recording of it running, and a video of the fan.",
    "images": ["data:image/png;base64,<base64-png>"],
    "audio": ["data:audio/mpeg;base64,<base64-mp3>"],
    "videos": ["data:video/mp4;base64,<base64-mp4>"],
    "questions": {
      "label_visible": {"type": "noul", "instructions": "Is the model and serial number label visible in the photo?"},
      "sounds_normal": {"type": "noul", "instructions": "Does the unit sound like it is running smoothly, without rattling or grinding?"},
      "fan_running": {"type": "noul", "instructions": "Is the fan running in the video?"}
    }
  }'
```

Clef-omni expands our open-weight decision architecture to natively handle multimodal workflows. We built this on a Qwen3-Omni-30B-A3B-Instruct mixture-of-experts (MoE) foundation, where the model was already capable of processing text, imagery, audio, and video directly within a single pipeline. However, we adopt the primary comprehension backbone while discarding the text-to-speech output components. In production, Clef-omni executes a quick prefill pass across the complete payload, scoring all modalities and valid parameter options simultaneously.

Because we skip output token generation since Clef models are not Large Language Models (LLMs), we remove the overhead of transcribing or captioning incoming files. Media elements map straight into the unified sequence, where video and audio are synced with visual frames for joint processing. Clef-omni then pulls candidate values directly from internal embeddings using our two-stage attention routing: every valid option gathers key evidence from the input (regardless if they are buried in text snippets, visual elements, or audio streams) before field vectors cross-attendÂ across the full context to compute confidence scores. We add a built-in lexical grammarÂ that preserves option semantics, so that we can deliver fast, schema-constrained scoring across every input type.

We train the model with the same techniques as we did with Clef â freezing the Qwen3 backbone, training low-rank adapters (LoRA), and applying our standard post-training approach: combining label-smoothed cross-entropy loss with Brier score calibration. The result is a model that is resilient and designed to succeed regardless of schema variations, field ordering, and prompt structures.

This brings several core upgrades to the Clef model family. Calibrated, schema-bound decisions now seamlessly handle text, images, audio, and synchronized video in a single API call.Â It's also fast. Text-only decisions return in about 130 ms at the median, image inputs in about 150 ms, and audio clips in a few hundred milliseconds. Even a full 21-second video clip with sound is scored in about 1.5 seconds, all in a single API call.

Our benchmarking shows strong performance across benchmarks, even with new modalities and MoE architecture.

Benchmark

Clef-omni

Clef-flash

BFCL Â· case exact

98.47

98.76

95.75

ToolRet Â· nDCG@10

69.19

66.43

65.28

API-Bank Â· accuracy

91.93

93.11

88.19

Home appliances Â· case exact

82.95

97.73

52.27

When2Call Â· accuracy

72.37

65.58

80.97

BANKING77 Â· macro-F1

94.20

90.93

79.74

CLINC150+OOS Â· macro-F1

97.43

66.77

89.27

BRIGHT Â· nDCG@10

45.91

39.26

47.52

Amazon ESCI Â· macro-F1

57.48

57.39

55.21

PhishNChips Â· accuracy

79.60

75.05

62.55

We also benchmarked against theTypeSafe evalsto show how Clef-omni performs.

Workflow

Metric

Clef-Omni

Invoice processing

Exact actions

Primary action

Customer service

Security incidents

Agent trace observability

## Clef-flash model is now cheaper

We heard your feedback â you want a decision model affordable enough to incorporate into any workflow. Weâve made a few optimizations and can now offer Clef-flash at cheaper prices. We want Clef to be able to make decisions that scale for you across all your agentic workflows, and now our pricing also incentivizes that.

We were able to optimize the model to the point where Clef-flash is nowcheaperÂ than Jev while still being performant and high-quality. Check out thedeveloper docsÂ for the most up-to-date pricing information at all times, including more detail on how image and audio modalities are converted to input tokens for pricing.

- Clef-flash â originally $0.09 per M input tokens, now$0.038 per M input tokens
- Clef â remains at$0.24 per M input tokens
- Clef-omni â launched today at$0.15 per M input tokens

However, one trade-off we have to make in order to have cheaper pricing is to cut the context window of Clef-flash. The hosted version of Clef-flash now has a context window of 24k, instead of 64k as previously advertised. The model weights on Hugging Face are untouched and were trained to support a 256k context window should you choose to self-host it.

From our usage data, we see that only 0.24% of requests exceed 24k input tokens. Based on this data, we decided to make the call to drop the context window to 24k for Clef-flash in order to price it at a more accessible entry point. Our Clef model remains at a 64k context window, and we encourage folks with larger context needs to switch to Clef instead of Clef-flash.

## Clef model is now faster

Speeds are also faster for the Clef model, with new optimizations to the hosted version of Clef on Workers AI. No new model weights are released because most of the optimizations we made are at the serving infrastructure layer, not materially to the model weights or architecture. Check out our new speeds below:

Input size

Before: median / p95 (ms)

Now: median / p95 (ms)

Median speedup

~800 tokens

[翻译失败，原文如下]

262 / 438

152 / 351

1.7Ã

~3,400 tokens

616 / 777

305 / 531

2.0Ã

~16,000 tokens

2,721 / 3,250

1,635 / 1,805

One of the optimizations we made was to move to SGLang for serving the model. We worked with the SGLang team and made pull requests to incorporate Clef (PR#42721), which will be released in SGLang 0.5.22. You can also self-host Clef since we released the weights, and the new SGLang launch commands are available on ourupdated Hugging Face repoÂ as well as theSGLang cookbooks.

## How are people using Clef?

At Cloudflare, weâve had teams experimenting with Clef as a model that can help classify over general domains. The coolest thing about watching teams adopt Clef is that the capability to do detections and classifications have moved into the model layer, where it is accessible for anyone to start incorporating decision models into their use cases. Previously, even with zero-shot classifiers, the small models may not have been powerful enough to classify across any domain without further tuning. You might have needed to stand up a specialized machine learning team to help train over your particular domain, and gather a corpus of data in order to train a better model. Now, all you need to do is call a model to instantly parse through input data with precision.

A few highlights of how teams at Cloudflare are using Clef: Our public GitHub docs repo uses Clef to instantlydetect and close spam issues.Â EmDash, our content management system,moderates plugin libraries for phishing. Our data loss prevention team is scanning data for potential personally identifiable information (PII) like government IDs. And our threat intelligence team is using Clef to help detect malicious domains.

## Give it a try!

Weâre excited to bring you more from the Clef family of models, including new modalities like audio and video, as well as making the model more accessible with cheaper pricing and faster speeds. Clef is fully Jev-API compatible and available via AI Gateway, so it is as simple as changing the model ID to try out Clef today. Check out ourdeveloper docsÂ for more information.

Thank you for all the love and warm reception around Cloudflareâs first models â we are focused on bringing you more. Try out our Clef family of models, and tell us what you think.

## Related tags

Follow on Social Media

- Cloudflare
- Michelle Chen

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Introducing Clef-omni with full multimodality, plus a faster Clef and a cheaper Clef-flash](https://blog.cloudflare.com/clef-faster-cheaper-multimodal/)
> 
> 翻译时间：2026-10-10 08:17
