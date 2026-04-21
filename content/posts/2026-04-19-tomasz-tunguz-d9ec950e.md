---
title: 精度的代价：大模型效率与成本的锯齿博弈
title_original: The Price of Precision
date: '2026-04-19'
source: Tomasz Tunguz
source_url: https://www.tomtunguz.com/hidden-cost-smarter-ai/
author: ''
summary: 本文探讨了大型语言模型发展中效率与成本的动态关系。文章指出，模型智能提升（如Claude Opus 4.5）通常带来任务所需Token数减少，从而降低实际使用成本。然而，后续版本（如Opus
  4.7）引入更精细的分词器以提高精度，导致相同文本的Token数量增加约1.46倍，成本随之上升。这揭示了AI模型演进中“效率提升降低成本”与“精度提升增加成本”之间的锯齿状波动模式，核心矛盾在于智能增长带来的效率收益与追求精度导致的Token膨胀之间的平衡。
categories:
- AI研究
tags:
- 大语言模型
- 分词器
- 成本分析
- 模型效率
- Anthropic
draft: false
translated_at: '2026-04-21T04:56:28.744863'
---

“随着模型变得更智能，它们能用更少的步骤解决问题：减少回溯、减少冗余探索、减少冗长推理。Claude Opus 4.5 达到相似或更好结果时，使用的 Token 数量显著少于其前代模型。”¹

当 Anthropic 在 2025 年 11 月发布 Opus 4.5 时，这个更大、更昂贵的模型实际使用成本反而更低。

按每个 Token 计算，Opus 4.5 的成本比 Sonnet 高 67%。² 但 Opus 4.5 达到相同结果时少用了 76% 的 Token。¹ 一项在 Sonnet 上花费 1 美元的任务，在 Opus 上仅需 0.4 美元。

各厂商的趋势是模型越智能，每项任务使用的 Token 越少。

随后 Opus 4.7 发布，这个更智能的模型却变得昂贵得多。原因在于：新的分词器——一种将文本拆解成计算机能理解的片段的软件。⁶

![How tokenizers break text into pieces - showing unbelievable split into un, belie, vable](/images/posts/93d0601d93ea.jpg)

更细小的片段迫使模型更仔细地关注每个单词，就像逐字阅读合同而非浏览段落。模型能更精确地遵循指令，在编码任务上犯错更少。代价是：Token 数量增加，成本上升。

“对于相同文本内容，我观察到 Token 数量增加了 1.46 倍。实践中预计成本将增加约 40%。”——Simon Willison⁷

Claude Code 的创建者 Boris Cherny 承认，Anthropic 提高了速率限制“以作补偿”。

更智能的模型会因精度提升而越来越贵，还是因更智能而更便宜？分辨率提升使其更昂贵，随后效率增益又降低成本——形成锯齿状波动模式。但无论如何，这都意味着生成更多 Token。

1. Anthropic, Introducing Claude Opus 4.5↩︎↩︎↩︎
2. Opus 4.5 : $5/$25 per million tokens vs Sonnet : $3/$15.Anthropic Pricing↩︎
3. NxCode, GPT 5.4 Complete Guide 2026↩︎
4. Google Cloud Medium, Gemini 3 vs 2.5↩︎
5. Claude Code Camp, I Measured Claude 4.7’s New Tokenizer↩︎
6. 以单词“unbelievable”为例。分词器可能将其拆分为 un、believe 和 able。这有助于计算机理解该词是核心概念（believe）的反面（un），且具有可能性（able）。↩︎
7. Simon Willison’s Weblog↩︎

Anthropic, Introducing Claude Opus 4.5↩︎↩︎↩︎

Opus 4.5 : $5/$25 per million tokens vs Sonnet : $3/$15.Anthropic Pricing↩︎

NxCode, GPT 5.4 Complete Guide 2026↩︎

Google Cloud Medium, Gemini 3 vs 2.5↩︎

Claude Code Camp, I Measured Claude 4.7’s New Tokenizer↩︎

Take the word “unbelievable.” A tokenizer might break it into un, believe, & able. This helps the computer understand that the word is the opposite (un) of a core concept (believe) that is possible (able).↩︎

Simon Willison’s Weblog↩︎

---

> 本文由AI自动翻译，原文链接：[The Price of Precision](https://www.tomtunguz.com/hidden-cost-smarter-ai/)
> 
> 翻译时间：2026-04-21 04:56
