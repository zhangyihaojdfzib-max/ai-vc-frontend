---
title: 'Watts in Store for 2027 : The AI Ceiling'
title_original: 'Watts in Store for 2027 : The AI Ceiling'
date: '2026-11-04'
source: Tomasz Tunguz
source_url: https://tomtunguz.com/watts-in-store-for-2027-inference/
author: ''
summary: '[翻译失败，原文如下]


  In short :US AI capacity grows from 38gw today to an 81gw ceiling in 2027. Because
  40% of compute serves inference & new Blackwell & Rubi...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-06T09:05:17.814257'
---

[翻译失败，原文如下]

In short :US AI capacity grows from 38gw today to an 81gw ceiling in 2027. Because 40% of compute serves inference & new Blackwell & Rubin racks lift blended monetization from $9.4b to $15.1b per inference gigawatt, theoretical US inference revenue rises 3.4x from $0.14t to $0.49t.

The ceiling for AI in 2027 is about 80gw : doubling all the compute built in the history of the country in twelve months.

Yet even at this historic pace, the hourly cost of GPUs has doubled in the last six months : short-term rental rates have jumped from $3 to $12-13 per hour, pushing Anthropic’s blended GPU-hour cost up 82% in just two quarters.1Finished server racks are already sitting unpowered in staging warehouses because data centers lack the energized utility power to turn them on.

When supply doubles & prices still double, demand is fundamentally outrunning physical reality. There will consistently be an active ceiling on energized compute, which will keep structural upward pressure on GPU prices per hour.

On last night’s All-In election livestream, Brad Gerstner framed that buildout in gigawatts :

“The consensus forecast is a total of 43 gigawatts coming online in 2027… the total gigawatts online at the end of ‘26, the cumulative in the United States, is about 38 … I think we could see at least 10 to 15 gigawatts of the expected build not come online.”2

![Watts in store : 81 GW lifts inference revenue 3.4x to $0.49t](/images/posts/cfb1118886b7.jpg)

What does a ceiling like this mean for AI?

First, there’s a theoretical maximum amount of revenue we can generate from AI. A GPU can perform two types of tasks for AI : inference & training. Today, 40% of GPU hours are inference : AI sold to customers.3The other 60% develops models.

Today’s 38gw fleet earns about $140b, while the 43gw to be added in 2027 will run on chips that are 3-5x more powerful & should deliver an annualized earnings capability of about $350b, for a total of nearly $500b.4

As GPU prices continue to rise, foundation model companies may need to shift the fraction of GPU hours to inference from training. This might limit the pace of innovation at the frontier.

Second, latency becomes the release valve for too much demand. Internet access is priced in terms of bandwidth (gigabytes of files you can download) & speed (how quickly you can download it). AI may be priced the same way. We see this already with products focused on low-latency inference & those on long-horizon tasks.5

Third, limitations in compute availability will encourage algorithmic innovation. Chinese models like DeepSeek, Qwen, & Kimi have demonstrated material architectural advantages that drive near-state-of-the-art performance on much smaller models & new architectures.6

Fourth, the harness becomes critical to deliver state-of-the-art performance on limited GPU availability. Responsible for more than half of system performance, the software around the model can extract tremendous efficiency.7

Fifth, the economics of vibe-coding face a reality check. When inference becomes more expensive, off-the-shelf software (with AI) can be less expensive than bespoke built & maintained internal software.

In 2027, AI’s constraint will be access to powered GPUs. As the prices for renting GPUs continues to increase faster than efficiency can fight, watts in store for 2027? Efficiency as the dominant motif up & down the stack.

1. Anthropic Form S-1/A (filed November 2, 2026), disclosing blended GPU-equivalent costs rising from $3.10 to $5.65 per hour as short-term burst capacity hit $7 to $13 per hour. Under AWS’s Early Rack Receipt program, Amazon took delivery of roughly $5b of Nvidia GB300 server racks in August 2026 alone before facilities had the substation power to activate them (Business Insider, October 20, 2026). See Tomasz Tunguz,The Financial Engineering Essential for AI in 2027, November 3, 2026, &How GPU Prices Can Double While AI Gets Cheaper, September 28, 2026.↩︎
2. Brad Gerstner on the All-In Podcast, “2026 Election Night Livestream with the Besties!” (Nov 3, 2026, 01:32:21) & All-In Summit keynote, “No AI Bubble, Semis Eat the Nasdaq & AI’s Take Off Problem” (Sept 17, 2026).All-In Podcast↩︎
3. SemiAnalysis frontier lab compute workload mix (1Q24 to 4Q26E), published Oct 6, 2026, & Anthropic Form S-1 (filed Oct 26, 2026).OfficeChai↩︎
4. Dylan Patel, SemiAnalysis, on the Dwarkesh Podcast (Aug 25, 2026) & SemiAnalysis Tokenomics Model.Dwarkesh Podcast. New 2027 racks (GB300, Vera Rubin, TPU v7, & Trainium 3) deliver 3-5x higher token throughput per watt than the installed 2026 base ; after token price deflation & a 50/50 mix between frontier labs ($31b/gw) & the broader market ($9.4b/gw), incremental inference capacity monetizes at ~$20.2b per gigawatt ($350b on 17.2gw of new inference), raising total theoretical revenue to nearly $500b ($0.49t).↩︎
5. OpenAI & Cerebras low-latency inference partnership (OpenAI) & Sail Research asynchronous inference queue (Sail Research). See also Tomasz Tunguz,Full Sail on Asynchronous Inference, September 2026.↩︎
6. Architectural innovations include multi-head latent attention (MLA), sparse mixture-of-experts routing, FP4 quantization, & speculative decoding to extract far more performance from the same GPU. On Artificial Analysis’s Intelligence Index, the 27b-parameter Qwen3.8-27B scored 52 : outscoring GLM-5.2 (51), a 753b-parameter frontier model roughly 28 times its size, & landing within 15% of the absolute frontier while running locally on a laptop. See Tomasz Tunguz,Birds Don’t Fly Like Planes. Neither Does AI., October 2026, &Local Coding Models, 2026.↩︎
7. Tomasz Tunguz,Aftermarket Harnesses, July 28, 2026, &The Harness Margin Opportunity, September 17, 2026, citing Endor Labs’ Agent Security League benchmark & UC Berkeley’s HarnessTax study showing the harness cuts the cost of the same resolved task by 71% with no loss of accuracy.↩︎

Anthropic Form S-1/A (filed November 2, 2026), disclosing blended GPU-equivalent costs rising from $3.10 to $5.65 per hour as short-term burst capacity hit $7 to $13 per hour. Under AWS’s Early Rack Receipt program, Amazon took delivery of roughly $5b of Nvidia GB300 server racks in August 2026 alone before facilities had the substation power to activate them (Business Insider, October 20, 2026). See Tomasz Tunguz,The Financial Engineering Essential for AI in 2027, November 3, 2026, &How GPU Prices Can Double While AI Gets Cheaper, September 28, 2026.↩︎

Brad Gerstner on the All-In Podcast, “2026 Election Night Livestream with the Besties!” (Nov 3, 2026, 01:32:21) & All-In Summit keynote, “No AI Bubble, Semis Eat the Nasdaq & AI’s Take Off Problem” (Sept 17, 2026).All-In Podcast↩︎

SemiAnalysis frontier lab compute workload mix (1Q24 to 4Q26E), published Oct 6, 2026, & Anthropic Form S-1 (filed Oct 26, 2026).OfficeChai↩︎

Dylan Patel, SemiAnalysis, on the Dwarkesh Podcast (Aug 25, 2026) & SemiAnalysis Tokenomics Model.Dwarkesh Podcast. New 2027 racks (GB300, Vera Rubin, TPU v7, & Trainium 3) deliver 3-5x higher token throughput per watt than the installed 2026 base ; after token price deflation & a 50/50 mix between frontier labs ($31b/gw) & the broader market ($9.4b/gw), incremental inference capacity monetizes at ~$20.2b per gigawatt ($350b on 17.2gw of new inference), raising total theoretical revenue to nearly $500b ($0.49t).↩︎

OpenAI & Cerebras low-latency inference partnership (OpenAI) & Sail Research asynchronous inference queue (Sail Research). See also Tomasz Tunguz,Full Sail on Asynchronous Inference, September 2026.↩︎

[翻译失败，原文如下]

Architectural innovations include multi-head latent attention (MLA), sparse mixture-of-experts routing, FP4 quantization, & speculative decoding to extract far more performance from the same GPU. On Artificial Analysis’s Intelligence Index, the 27b-parameter Qwen3.8-27B scored 52 : outscoring GLM-5.2 (51), a 753b-parameter frontier model roughly 28 times its size, & landing within 15% of the absolute frontier while running locally on a laptop. See Tomasz Tunguz,Birds Don’t Fly Like Planes. Neither Does AI., October 2026, &Local Coding Models, 2026.↩︎

Tomasz Tunguz,Aftermarket Harnesses, July 28, 2026, &The Harness Margin Opportunity, September 17, 2026, citing Endor Labs’ Agent Security League benchmark & UC Berkeley’s HarnessTax study showing the harness cuts the cost of the same resolved task by 71% with no loss of accuracy.↩︎

---

> 本文由AI自动翻译，原文链接：[Watts in Store for 2027 : The AI Ceiling](https://tomtunguz.com/watts-in-store-for-2027-inference/)
> 
> 翻译时间：2026-11-06 09:05
