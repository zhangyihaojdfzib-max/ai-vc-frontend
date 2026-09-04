---
title: The Ads Model for Prompts Vertically Integrates AI
title_original: The Ads Model for Prompts Vertically Integrates AI
date: '2026-09-03'
source: Tomasz Tunguz
source_url: https://tomtunguz.com/the-ads-model-for-prompts-vertically-integrates-ai/
author: ''
summary: '[翻译失败，原文如下]


  In short :Meta''s Muse Spark 1.3 prices inference at two levels : $1.25/$4.25 per
  million tokens for private data, & $0.10/$0.20 for train...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-04T07:06:32.212588'
---

[翻译失败，原文如下]

In short :Meta's Muse Spark 1.3 prices inference at two levels : $1.25/$4.25 per million tokens for private data, & $0.10/$0.20 for training consent : a 92% price spread. Michael Mauboussin taught that market prices contain information about underlying expectations. This spread establishes a liquid clearing price of $1.24/m tokens for user & agent prompt data, allowing Meta to vertically integrate the AI data supply chain & acquire post-training data at pennies on the dollar compared to specialized data labs.

Meta launched two things yesterday : a state-of-the-art model & a new pricing system for foundation models.1Muse Spark propels US open source models to the frontier. Meanwhile, the pricing system resets the industry’s economics.

For thirty years, enterprise software operated on strict licensing fees with a guarantee of total privacy & zero data retention.2Consumer technology operated on the opposite principle : free software in exchange for behavioral data. Consumers trade queries for convenience, but enterprises fiercely protect their intellectual property.

Now that model is coming to AI with a twist.

Meta’s new pricing makes the barter explicit through a two-tier pricing structure with & without privacy :3

1. The Standard Tier (muse-spark-1.3) :$1.25/m input tokens & $4.25/m output tokens. Your prompts & completions are never used to train Meta’s foundation models.
2. The Contributor Tier (muse-spark-1.3-contributor) :$0.10/m input tokens & $0.20/m output tokens. In exchange for a 92% discount on input & a 95% discount on output, Meta retains the right to train future models on your data.

No other foundation model provider currently offers this kind of explicit barter on its API. This is the ads model coming to AI.

![The 92% Privacy Surcharge Across Daily Token Volumes](/images/posts/1f23ea54ac9e.jpg)

As Michael Mauboussin writes in Expectations Investing, there is information in prices.4When Meta charges two radically different prices for the same AI, the difference in price tells us the value of the data.

At an agentic 30:1 input-to-output ratio,5the blended standard tier costs $1.35/m tokens, while the contributor tier costs $0.103/m. The difference is a $1.24/m token spread, an effective 92.3% subsidy.

For an enterprise processing 1b tokens per day, opting into Zero Data Retention (ZDR) is a $454,000 annual privacy surcharge. That difference is how Meta values incoming customer data : $1.24/m tokens.

This unbundles the $20 monthly consumer subscription. Labs absorbed compute losses on flat-rate consumer plans because default terms granted training rights, an implicit data subsidy that Meta has now formalized per token.6

Why surrender 92% of inference revenue? It is not out of altruism.

The public web has been exhaustively crawled ; frontier gains now come from post-training, reinforcement learning from AI feedback, & user usage patterns. Estimates place the market for training data & human labeling at $10b in annual revenue.7

![The Vertical Integration of the AI Data Supply Chain](/images/posts/eeb9f5b75f8d.jpg)

Meta’s pricing model bypasses this intermediary. Just as search & social platforms vertically integrated the digital advertising supply chain by capturing behavioral data directly from users, Meta is vertically integrating the AI data supply chain. Instead of paying labeling vendors to simulate human behavior, Meta turns its inference network into a self-funding data flywheel.

At $1.24/m tokens of subsidy,8Meta acquires organic reasoning traces at pennies on the dollar compared to specialized data labs, while undercutting closed foundation models on inference price.

Compute is no longer sold simply as an infrastructure utility. It has become a currency traded directly for the training tokens needed to build the next frontier model.

Ultimately, this solves the business model for American open source. Just like ads, the barter is simple : subsidized access in exchange for data.

1. Open Models Tack Toward the Frontier.↩︎
2. Enterprise master services agreements & compliance frameworks (SOC 2, ISO 27001, HIPAA) require zero data retention & prohibit vendor model training on customer data.↩︎
3. Meta Model API, Pricing & Data Terms.↩︎
4. Michael Mauboussin, Expectations Investing.↩︎
5. The Hungry, Hungry AI Model.↩︎
6. At an individual volume of 10m tokens/month, the $1.24/m spread yields a $12/month subsidy. For power users consuming 20m–50m tokens/month, the data subsidy reaches $25–$62/month, matching the consumer subscription discount.↩︎
7. @deedydas on X, Every Single Startup Selling AI Training Data.↩︎
8. At $1.24 per million tokens, Meta’s effective subsidy is $0.0037 per 3,000-token interaction trace. By comparison, specialized human labeling vendors charge $25 to $100+ per hour for domain experts, yielding $5 to $50 per verified reasoning trajectory.↩︎

Open Models Tack Toward the Frontier.↩︎

Enterprise master services agreements & compliance frameworks (SOC 2, ISO 27001, HIPAA) require zero data retention & prohibit vendor model training on customer data.↩︎

Meta Model API, Pricing & Data Terms.↩︎

Michael Mauboussin, Expectations Investing.↩︎

The Hungry, Hungry AI Model.↩︎

At an individual volume of 10m tokens/month, the $1.24/m spread yields a $12/month subsidy. For power users consuming 20m–50m tokens/month, the data subsidy reaches $25–$62/month, matching the consumer subscription discount.↩︎

@deedydas on X, Every Single Startup Selling AI Training Data.↩︎

At $1.24 per million tokens, Meta’s effective subsidy is $0.0037 per 3,000-token interaction trace. By comparison, specialized human labeling vendors charge $25 to $100+ per hour for domain experts, yielding $5 to $50 per verified reasoning trajectory.↩︎

---

> 本文由AI自动翻译，原文链接：[The Ads Model for Prompts Vertically Integrates AI](https://tomtunguz.com/the-ads-model-for-prompts-vertically-integrates-ai/)
> 
> 翻译时间：2026-09-04 07:06
