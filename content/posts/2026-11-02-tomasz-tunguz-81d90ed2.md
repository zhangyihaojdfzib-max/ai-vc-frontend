---
title: The Four Questions of AI
title_original: The Four Questions of AI
date: '2026-11-02'
source: Tomasz Tunguz
source_url: https://tomtunguz.com/the-four-questions-of-ai/
author: ''
summary: '[翻译失败，原文如下]


  In short :AI consists of four layers: application, harness & context, model, & data
  center. Each layer faces an unresolved economic quest...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-03T09:14:04.997565'
---

[翻译失败，原文如下]

In short :AI consists of four layers: application, harness & context, model, & data center. Each layer faces an unresolved economic question, & the four layers interplay directly: rising GPU financing costs increase the value of the harness, while model & inference co-design multiplies how many users the same data center hardware can serve.

There are 4 layers in the AI stack, each with a fundamental question before it.

![The Four Layers of AI & the Question Facing Each](/images/posts/77b8e79bc238.jpg)

Application

Breakout hits appear overnight. The next model release can erase them just as fast. Thin wrappers die when the model absorbs their feature. To build a moat, app companies must decide whether to build a brand, disrupt incumbents through pricing, develop their own models, or expand faster than competitors.

Agents do the work with headless software. Will a user interface survive, or do all applications collapse into middleware harnesses1?

Harness & Context

If applications collapse into middleware, the fight moves to who owns the harness. Model makers claim their native harness wins. The benchmarks say otherwise. In the same week, both OpenAI & Anthropic models scored higher in Cursor than in their creators’ own harnesses2. Because input context is up to 98% of all tokens2, a smart harness cuts the cost of the same answer by 71% & lifts gross margin from 38% to 75%3.

Beyond the model makers, enterprises are starting to lay claim to the harness to build corporate sovereign AI4. No CIO wants to ship company secrets out the door in a prompt. Owning the context layer lets a company keep its memory & permissions in house while swapping models underneath.

Model

For foundation models, the question is at what point training costs don’t pay back. Training a state-of-the-art model costs billions5. Recursive self-improvement, AI models training better AI, has not yet bailed out the big labs. AI writes 75% of Google DeepMind’s production code, yet Google sees no end-to-end speedup in AI research6.

On the demand side, Rich Sutton’s Bitter Lesson argues that general models scaled with massive compute always win7. Yet SOTA models are losing token share on public gateways because they cost too much to run8. About 83% of agent tasks now route to smaller or domain-specific models fine-tuned to do one job for a fraction of the bill9.

Challengers are attacking the training bill through process & architecture. One startup used coding agents to pre-train a competitive coding model with a single researcher for under $10m10. New architectures like diffusion models11& JEPA, where a 109m model beat 72b LLMs with 42x less data12, bypass brute-force scaling.

Still, the bull case for scaling the frontier sits in Anthropic’s S-1. Opus 5.5 cut customer cost per task by 40%, & when Opus 4.5 delivered more capability at a lower cost per task than Opus 4.1, Jevons paradox kicked in & sequential quarterly revenue growth accelerated from 48% to 132%13.

Data Center

Below the models, the question is whether credit & power can keep up with GPU demand. With concrete prices up 3x, electrical grids strained, & backlogs on turbines, generators, & reciprocating engines, the answer for now is no14.

Unrestrained growth in AI requires $4t in new debt over five years, making the AI credit market larger than global private credit & equal to 91% of the US municipal bond market15. Are there enough lenders left at attractive rates? Risk strains insurance costs. Five-year credit default swap spreads have hit records from Meta (108 bps) to Oracle (322 bps) & CoreWeave (1,090 bps)16.

On the ground, local politics & grid delays are blocking new sites, while Ornn’s B300 index has climbed to $12.29 per GPU-hour (~20% CMGR since June)17.

Meanwhile, three open questions hang over the math : whether cash flows match the duration of twenty-year debt & leases15, whether GPUs last five years, & whether the price of a GPU-hour will increase or decrease18.

How the Layers Interplay

None of these four questions stands alone. Applications that generate tremendous profits at the top can sustain inflation in GPU prices & higher borrowing costs at the bottom. New, more efficient architectures19can decrease the need for concrete & copper. Surging GPU prices can swing the economics of the whole stack.

Like a double pendulum20, the four layers form a coupled system : simple in each part, yet complex, chaotic, & unpredictable in motion.

[翻译失败，原文如下]

1. A harness is the software runtime around the model, such as Claude Code, Codex, or Cursor, that governs what context flows into the prompt, which tools the agent calls, & how session trajectories are cached & logged. See Tomasz Tunguz,The Harness Is the New Battleground, July 14, 2026.↩︎
2. Tomasz Tunguz,Aftermarket Harnesses, July 28, 2026, citing Endor Labs’ Agent Security League benchmark (GPT-5.5 scoring 61.5% in OpenAI’s Codex vs. 87.2% in Cursor ; Claude Opus 4.7 scoring 87.2% in Claude Code vs. 91.1% in Cursor) & OpenRouter token composition data (input tokens representing 85.7% to 98.2% of volume).↩︎↩︎
3. Tomasz Tunguz,The Harness Margin Opportunity, September 17, 2026, citing UC Berkeley’sHarnessTaxstudy (71% lower cost for the same resolved SWE-bench task with no statistically significant quality difference across 42 comparisons) & AI associate contract gross-margin modeling (38% vs. 75% on a $250k contract).↩︎
4. Tomasz Tunguz,The Price of Entry to the Frontier, August 31, 2026, on enterprise data sovereignty mandates, Zero Data Retention policies, & model access segmentation.↩︎
5. Frontier training & R&D scale : Anthropic’s S-1 (filed October 26, 2026) discloses $8.1b in FY2025 operating losses & $637b in total compute commitments (Anthropic S-1 Analysis), while OpenAI projects $278b in cumulative cash burn through 2030 & Epoch AI estimates individual next-generation frontier training runs crossing $1b+ as training compute grows ~5x per year (Epoch AI).↩︎
6. Google DeepMind, Gemini 4 Argon Safety & Security Report, October 2026 : AI generates more than 75% of DeepMind production code & fully delegated pull requests rose from 7.5% to 11.9% over five months, with no significant end-to-end acceleration of AI research timelines.↩︎
7. Rich Sutton,The Bitter Lesson, March 13, 2019 : general methods that leverage computation ultimately beat methods that embed human domain knowledge by a large margin.↩︎
8. Tomasz Tunguz,The Most Important Market in AI Is the Middle, September 23, 2026, &Honestly, Who Buys SOTA?, August 14, 2026 : 84% of tokens on OpenRouter are not state of the art, Anthropic’s flagship Fable 5.1 captured only 3.7% of gateway spending in its first twelve days (while its predecessor fell from 13.2% to 4.9% within a month), & among large corporate accounts frontier models fell from 53% of token consumption in early August to 45% by September.↩︎
9. Tomasz Tunguz,The Most Important Market in AI Is the Middle, September 23, 2026, &9 Observations Using AI Agents, 2026 : Cursor’s Composer 2 fine-tuned open-weight Kimi K2.5 to cut costs 86% vs. its prior model, Harvey fine-tuned a domain model to cut cost per cell 55% vs. Sonnet 5 while outscoring Fable 5, & an 8b Qwen 3 model fine-tuned for task classification beat zero-shot GPT-5.2 locally on a laptop.↩︎
10. Mirendil,Pretraining at Scale Without a Pretraining Team, October 21, 2026 : one researcher paired with coding agents (which wrote 99% of the repository) pre-trained Mirendil-Base (100b to 500b parameters) from scratch in 3.5 months for under $10m all-in compute & token spend, beating GLM-5.3 (0.242 bits/byte), DeepSeek-V4-Pro (0.243), & Nemotron-550B (0.247) on held-out post-cutoff code repositories (averaging 0.222 bits/byte vs. 0.193 for Kimi-K3).↩︎
11. Diffusion language models generate & refine blocks of tokens in parallel rather than one token at a time : Inception Labs’ Mercury 2.5 (launched September 8, 2026) reaches 414 to 1,107 tokens/sec on Nvidia GPUs at $0.20/$0.75 per million tokens, roughly 9x cheaper & 3x faster than comparable autoregressive models (Inception Labs).↩︎
12. Randall Balestriero & Yann LeCun,The Platonic Representation Theorem : Joint-Embedding Predictive Architectures Converge to a Shared World Model, October 29, 2026 : by predicting compressed latent embeddings rather than surface tokens, a 109m-parameter text JEPA aligns with DINOv2 & CLIP vision encoders better than any tested autoregressive LLM up to 72b parameters (660x larger) while requiring 42x fewer training samples.↩︎
13. Tomasz Tunguz,Anthropic S-1 Analysis : How 7 Key Metrics Stack Up, October 26, 2026, quoting Anthropic’s S-1 : “With the release of Claude Fable 5.1 in September 2026, we reduced the cost of typical workloads by approximately 25% compared to Fable 5, with savings of up to 45% for complex coding & highly agentic tasks. Similarly, with the release of Opus 5.5 that same month, we reduced customers’ cost per task by approximately 40% compared to Opus 5.” When Opus 4.5 launched with more capability & lower cost per task than Opus 4.1, Anthropic’s sequential quarterly revenue growth accelerated from 48% to 132%.↩︎
14. Tomasz Tunguz,The AI Bullwhip, August 23, 2026 : data center shell & concrete construction costs have tripled to $1,033 per square foot excluding land (US Census Bureau & RSMeans Construction Cost Indices), electrical systems consume half of a $20b-per-gigawatt facility budget, generator step-up transformers average nearly three-year lead times (Wood Mackenzie), & GE Vernova & Siemens Energy have sold out gas turbine production through 2029 with order books stretching to 2031 (POWER Magazine, CNBC, & Caterpillar/Cummins data center backup generator & reciprocating engine backlog disclosures).↩︎
15. Tomasz Tunguz,Concrete, Silicon, & Leverage, September 4, 2026 : $4t in projected five-year AI data center debt equals 286% of US commercial paper, 143% of the global private credit market, & 91% of the $4.4t US municipal bond market, requiring $1.2t to $1.5t in annual AI revenue by 2030 to cover interest at a 3x coverage ratio.↩︎↩︎
16. Financial Times,AI debt worries spark surge in default insurance trading, October 20, 2026, citing Morgan Stanley Research ($466b YTD AI-linked debt issuance) & S&P Global Market Intelligence (5-year CDS spreads at record highs of 108 bps for Meta, 226 bps for SpaceX, 322 bps for Oracle, & 1,090 bps for CoreWeave) ; CNBC,AI debt outlook : Oracle, Alphabet & Amazon in focus, October 27, 2026.↩︎
17. Ornn B300 Compute Price Index (settled October 30, 2026) : the weekly B300 index stands at $12.29 per GPU-hour, up from ~$5.53 in mid-June 2026 (a 20.1% compound monthly growth rate over 4.4 months) & $10.47 on August 28, 2026 (an 8.1% CMGR over the past two months, & -$0.12 or -0.97% over the past month) ; see also Tomasz Tunguz,How GPU Prices Can Double While AI Gets Cheaper, September 28, 2026, on B200 rates doubling from $4.40 to $8.08 per hour & Oracle’s six-month force majeure delay on its New Mexico data center campus.↩︎
18. Even as the Ornn B300 index sits at $12.29 per GPU-hour (20.1% CMGR since June, 8.1% CMGR since August 28, & -0.97% over the past month), spot quotes in the secondary market can swing sharply : on November 1, 2026, Jaber (@Akashi203 on X) noted that a month after begging GPU providers for B300s at $7.90 an hour, providers were offering them at $4.60 an hour with no commitment.↩︎
19. DeepSeek-AI,Insights into DeepSeek-V3 : Scaling Challenges & Reflections on Hardware for AI Architectures, May 14, 2025 (Multi-head Latent Attention reducing KV cache to 70 KB per token vs. 327 KB for Qwen-2.5 72B & 516 KB for Llama-3.1 405B), &DeepSeek-V3/R1 Inference System Overview, February 28, 2025 (776b total tokens/day : 608b input & 168b output across 226.75 average H800 nodes for $87,072/day).↩︎
20. Adouble pendulumis a pendulum with a second pendulum attached to its end : although each arm obeys simple deterministic laws, the coupled system exhibits chaotic motion where tiny shifts in one arm produce large, unpredictable swings across the whole system.↩︎

A harness is the software runtime around the model, such as Claude Code, Codex, or Cursor, that governs what context flows into the prompt, which tools the agent calls, & how session trajectories are cached & logged. See Tomasz Tunguz,The Harness Is the New Battleground, July 14, 2026.↩︎

[翻译失败，原文如下]

Tomasz Tunguz,Aftermarket Harnesses, July 28, 2026, citing Endor Labs’ Agent Security League benchmark (GPT-5.5 scoring 61.5% in OpenAI’s Codex vs. 87.2% in Cursor ; Claude Opus 4.7 scoring 87.2% in Claude Code vs. 91.1% in Cursor) & OpenRouter token composition data (input tokens representing 85.7% to 98.2% of volume).↩︎↩︎

Tomasz Tunguz,The Harness Margin Opportunity, September 17, 2026, citing UC Berkeley’sHarnessTaxstudy (71% lower cost for the same resolved SWE-bench task with no statistically significant quality difference across 42 comparisons) & AI associate contract gross-margin modeling (38% vs. 75% on a $250k contract).↩︎

Tomasz Tunguz,The Price of Entry to the Frontier, August 31, 2026, on enterprise data sovereignty mandates, Zero Data Retention policies, & model access segmentation.↩︎

Frontier training & R&D scale : Anthropic’s S-1 (filed October 26, 2026) discloses $8.1b in FY2025 operating losses & $637b in total compute commitments (Anthropic S-1 Analysis), while OpenAI projects $278b in cumulative cash burn through 2030 & Epoch AI estimates individual next-generation frontier training runs crossing $1b+ as training compute grows ~5x per year (Epoch AI).↩︎

Google DeepMind, Gemini 4 Argon Safety & Security Report, October 2026 : AI generates more than 75% of DeepMind production code & fully delegated pull requests rose from 7.5% to 11.9% over five months, with no significant end-to-end acceleration of AI research timelines.↩︎

Rich Sutton,The Bitter Lesson, March 13, 2019 : general methods that leverage computation ultimately beat methods that embed human domain knowledge by a large margin.↩︎

Tomasz Tunguz,The Most Important Market in AI Is the Middle, September 23, 2026, &Honestly, Who Buys SOTA?, August 14, 2026 : 84% of tokens on OpenRouter are not state of the art, Anthropic’s flagship Fable 5.1 captured only 3.7% of gateway spending in its first twelve days (while its predecessor fell from 13.2% to 4.9% within a month), & among large corporate accounts frontier models fell from 53% of token consumption in early August to 45% by September.↩︎

Tomasz Tunguz,The Most Important Market in AI Is the Middle, September 23, 2026, &9 Observations Using AI Agents, 2026 : Cursor’s Composer 2 fine-tuned open-weight Kimi K2.5 to cut costs 86% vs. its prior model, Harvey fine-tuned a domain model to cut cost per cell 55% vs. Sonnet 5 while outscoring Fable 5, & an 8b Qwen 3 model fine-tuned for task classification beat zero-shot GPT-5.2 locally on a laptop.↩︎

Mirendil,Pretraining at Scale Without a Pretraining Team, October 21, 2026 : one researcher paired with coding agents (which wrote 99% of the repository) pre-trained Mirendil-Base (100b to 500b parameters) from scratch in 3.5 months for under $10m all-in compute & token spend, beating GLM-5.3 (0.242 bits/byte), DeepSeek-V4-Pro (0.243), & Nemotron-550B (0.247) on held-out post-cutoff code repositories (averaging 0.222 bits/byte vs. 0.193 for Kimi-K3).↩︎

Diffusion language models generate & refine blocks of tokens in parallel rather than one token at a time : Inception Labs’ Mercury 2.5 (launched September 8, 2026) reaches 414 to 1,107 tokens/sec on Nvidia GPUs at $0.20/$0.75 per million tokens, roughly 9x cheaper & 3x faster than comparable autoregressive models (Inception Labs).↩︎

Randall Balestriero & Yann LeCun,The Platonic Representation Theorem : Joint-Embedding Predictive Architectures Converge to a Shared World Model, October 29, 2026 : by predicting compressed latent embeddings rather than surface tokens, a 109m-parameter text JEPA aligns with DINOv2 & CLIP vision encoders better than any tested autoregressive LLM up to 72b parameters (660x larger) while requiring 42x fewer training samples.↩︎

Tomasz Tunguz,Anthropic S-1 Analysis : How 7 Key Metrics Stack Up, October 26, 2026, quoting Anthropic’s S-1 : “With the release of Claude Fable 5.1 in September 2026, we reduced the cost of typical workloads by approximately 25% compared to Fable 5, with savings of up to 45% for complex coding & highly agentic tasks. Similarly, with the release of Opus 5.5 that same month, we reduced customers’ cost per task by approximately 40% compared to Opus 5.” When Opus 4.5 launched with more capability & lower cost per task than Opus 4.1, Anthropic’s sequential quarterly revenue growth accelerated from 48% to 132%.↩︎

Tomasz Tunguz,The AI Bullwhip, August 23, 2026 : data center shell & concrete construction costs have tripled to $1,033 per square foot excluding land (US Census Bureau & RSMeans Construction Cost Indices), electrical systems consume half of a $20b-per-gigawatt facility budget, generator step-up transformers average nearly three-year lead times (Wood Mackenzie), & GE Vernova & Siemens Energy have sold out gas turbine production through 2029 with order books stretching to 2031 (POWER Magazine, CNBC, & Caterpillar/Cummins data center backup generator & reciprocating engine backlog disclosures).↩︎

Tomasz Tunguz,Concrete, Silicon, & Leverage, September 4, 2026 : $4t in projected five-year AI data center debt equals 286% of US commercial paper, 143% of the global private credit market, & 91% of the $4.4t US municipal bond market, requiring $1.2t to $1.5t in annual AI revenue by 2030 to cover interest at a 3x coverage ratio.↩︎↩︎

Financial Times,AI debt worries spark surge in default insurance trading, October 20, 2026, citing Morgan Stanley Research ($466b YTD AI-linked debt issuance) & S&P Global Market Intelligence (5-year CDS spreads at record highs of 108 bps for Meta, 226 bps for SpaceX, 322 bps for Oracle, & 1,090 bps for CoreWeave) ; CNBC,AI debt outlook : Oracle, Alphabet & Amazon in focus, October 27, 2026.↩︎

Ornn B300 Compute Price Index (settled October 30, 2026) : the weekly B300 index stands at $12.29 per GPU-hour, up from ~$5.53 in mid-June 2026 (a 20.1% compound monthly growth rate over 4.4 months) & $10.47 on August 28, 2026 (an 8.1% CMGR over the past two months, & -$0.12 or -0.97% over the past month) ; see also Tomasz Tunguz,How GPU Prices Can Double While AI Gets Cheaper, September 28, 2026, on B200 rates doubling from $4.40 to $8.08 per hour & Oracle’s six-month force majeure delay on its New Mexico data center campus.↩︎

Even as the Ornn B300 index sits at $12.29 per GPU-hour (20.1% CMGR since June, 8.1% CMGR since August 28, & -0.97% over the past month), spot quotes in the secondary market can swing sharply : on November 1, 2026, Jaber (@Akashi203 on X) noted that a month after begging GPU providers for B300s at $7.90 an hour, providers were offering them at $4.60 an hour with no commitment.↩︎

DeepSeek-AI,Insights into DeepSeek-V3 : Scaling Challenges & Reflections on Hardware for AI Architectures, May 14, 2025 (Multi-head Latent Attention reducing KV cache to 70 KB per token vs. 327 KB for Qwen-2.5 72B & 516 KB for Llama-3.1 405B), &DeepSeek-V3/R1 Inference System Overview, February 28, 2025 (776b total tokens/day : 608b input & 168b output across 226.75 average H800 nodes for $87,072/day).↩︎

Adouble pendulumis a pendulum with a second pendulum attached to its end : although each arm obeys simple deterministic laws, the coupled system exhibits chaotic motion where tiny shifts in one arm produce large, unpredictable swings across the whole system.↩︎

---

> 本文由AI自动翻译，原文链接：[The Four Questions of AI](https://tomtunguz.com/the-four-questions-of-ai/)
> 
> 翻译时间：2026-11-03 09:14
