---
title: An updated Clairic and Clairic-flash are now open-weight, from the new Workers
  AI Superintelligence team
title_original: An updated Clairic and Clairic-flash are now open-weight, from the
  new Workers AI Superintelligence team
date: '2026-11-18'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/open-clairic/
author: ''
summary: "[翻译失败，原文如下]\n\nCloudflare has become a neolab.Â Weâ\x80\x99re building our\
  \ own frontier AI models for our customers and the open-source community.\n\nToday,\
  \ weâ..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-19T09:43:44.352420'
---

[翻译失败，原文如下]

Cloudflare has become a neolab.Â Weâre building our own frontier AI models for our customers and the open-source community.

Today, weâre announcing two open-weight model releases:

- Weâre introducing an updated version ofClairic. Since the preview, weâve improved extraction from complex documents including images and PDFs (new!), with more reliable handling of tables, lists, and dates, and better grounding of answers in the source material.
- Weâre introducingClairic-flash, a lighter, faster version of Clairic that delivers strong extraction and prediction performance in a compact, 9-billion-parameter model.

Both extraction models are hosted on Workers AI and full open weights areavailable on Hugging Face.

Weâre also excited to re-introduce ourselves asÂ the Workers AIÂ superintelligence team, the frontier AI research team behindClef, Clairic, and lots more in the works.Â This team is working quickly to push the AI frontier and build useful models for Cloudflareâs customers and the open source community.

## A new version of Clairic: redesigned after the preview release

Sinceannouncing ClairicÂ in preview, we have received a ton of use cases and helpful feedback on how customers wanted to use an extraction model. We heard about use cases ranging from extracting data from images like receipts to reading values from support tickets. We knew that we wanted extraction to be the clear focus for the model, so it had to excel at reading from unstructured data.

We decided to go back to the drawing board with Clairic and redesigned our architecture, differentiating this new version of Clairic from our preview release. For ordinary text and number extraction fields, we now useparallel slot autoregressive generationÂ instead of a single forward pass. Each field uses the tokens it has already written to choose its next token, then stops at its own end marker. All the fields advance together in the serving batch, still giving lightning-fast latency per request. This boosted our accuracy in extraction for both text and images, and the trade-off in accuracy offsets the small latency cost. For computation, estimation, and extraction use cases, we trained special heads that can handle estimates, forecasts, durations, calculated dates, and explicit arithmetic.

Although the model architecture evolved, we kept the parts of the typed API interface that make the answers useful: confidence scores, character spans, and probabilities are still intact with every request. The model is still incredibly fast and cheap. From the evals below, you can see how our newer versions of Clairic have greatly improved on extraction across text, images, PDFs, and more.

Clairic-preview

Clairic

Clairic-flash

D1.2 + OCR

ScaleDown

Fresh text fields, 96 requests

295/336

335/336

328/336

304/336

259/336

Internal eval (mchen) - mixed-input fields, 36 requests

207/226

221/226

213/226

116/226

156/226

Tracked customer assertions, 139 request shapes

1,033/1,263

1,263/1,263

973/1,263

653/1,263

Synthetic receipt fields in text and images

369/576

576/576

397/576

280/576

There are no public extraction benchmarks yet, but we ran our internal evals for other emerging extraction models on the market, such asLiquid AIâs D1.2(pipelined with Apple Vision for optical character recognition)Â andScaledownâs Extract. Our Clairic models excel across extraction use cases, but takeÂ these evals as directional guidance since they are self-reported. We wanted to show an illustrative picture of how Clairic is performing across generalized extraction use cases and celebrate the fact that other companies are releasing extraction models as well â confirming our original hypothesis that extraction was a pain point for LLM users because of the cost, latency, and accuracy.

### But is it fast?

We ran latency tests for Clairic and Clairic-flash, measuring complete HTTP response from a self-hosted server, including all fields in the request. Even with the redesigned architecture, you can expect responses in under one second â much faster than typical LLM responses for similar workloads.

Eval set

Requests per model

Clairic p50 / p95

Clairic-flash p50 / p95

Fresh text fields

358 / 736 ms

155 / 328 ms

Fresh image fields

453 / 976 ms

305 / 605 ms

Commercial leases

691 / 803 ms

379 / 519 ms

Loan pricing

395 / 407 ms

188 / 192 ms

Traffic forecasting

532 / 585 ms

243 / 261 ms

Expense audit, development

632 / 742 ms

393 / 512 ms

### Better extraction for images and PDFs

In ourpreview blog post, Clairic read a photo of a receipt. Now the Clairic family of models can read PDFs too, so you can ask for the supplier, line items, and total in one request, even when they appear on different pages. You can include up to four images or PDF pages in total, and line items can come back as rows that keep each description, quantity, and price together. Due to Clairicâs new architecture, image reading accuracy has improved from 207 errors to 0 on our internal benchmarks, explicitly covering text and images.

![clairic-image-extraction-comparison.png](/images/posts/e84d0219e9ea.jpg)

### Promotional pricing on Clairic for a limited time

When we first launched our preview endpoint of Clairic at@cf/cloudflare/clairic, we hosted the 9B variant as it was faster and easier to train, at the preview price of $0.10 per M input tokens. Weâre now moving the 9B model to the@cf/cloudflare/clairic-flashÂ endpoint and the 27B model will live at@cf/cloudflare/clairic.

The 27B ClairicÂ model will be priced at $0.24 per M input tokens, while the 9B Clairic-flash model will be priced at $0.10 per M input tokens. Although the model does technically generate output tokens, we decided to keep theSystem OneÂ pricing principles and are only charging on input tokens: we eat the cost of the output token generation.

In order to make this a seamless swap, weâre offering a promotional discount on Clairic â until December 1, 2026, both Clairic and Clairic-flash will cost $0.10 per M input tokens. This means you get to try out the higher quality variant of Clairic at the same price. If your applications are hooked up to the ClairicÂ endpoint that we released in preview, you will automatically benefit from the better extraction capabilities of our new model, which weâre rolling out in place.

If youâd like to move more cost-sensitive workloads to the cheaper 9B Clairic-flash variant, we encourage you to do so. On December 1, weâll be ending the promotional discount for ClairicÂ and pricing will resume at $0.24 per M input tokens instead of the discounted $0.10 per M input tokens.

### Clairic and Clairic-flash (new) are open-weight

Both Clairic models are nowopen-weight on Hugging FaceÂ as well. We have seen an outpouring of experiments and tuned models from our release of Clef, and weâre happy to continue supporting teams and research with our open-weight release of Clairic.

Our mission with these System One models is to help people augment their expensive LLM usage with smaller, faster, cheaper models that are purpose-built for a specific task. We hope that releasing these models open-weight encourages others to experiment and build on our ideas as well.

## Try them out

Clairic and Clairic-flash are available on Workers AI as@cf/cloudflare/clairicÂ and@cf/cloudflare/clairic-flash. ThedeveloperÂ documentationÂ has the full API schemas, which remain unchanged from our preview endpoint. Weâre also publishing the open-weight releases forClairicÂ andClairic-flashÂ on Hugging Face.Â

The team behind these models â the Workers AI superintelligence team âÂ is just getting started, and growing fast to push frontier AI research at Cloudflare.Join us earlyÂ and help shape what the superintelligence team becomes.

- Cloudflare
- Alex Reneau
- Michelle Chen

---

> 本文由AI自动翻译，原文链接：[An updated Clairic and Clairic-flash are now open-weight, from the new Workers AI Superintelligence team](https://blog.cloudflare.com/open-clairic/)
> 
> 翻译时间：2026-11-19 09:43
