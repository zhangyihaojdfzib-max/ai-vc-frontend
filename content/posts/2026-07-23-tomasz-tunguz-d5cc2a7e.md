---
title: AI模型市场分化：旧模型为何仍占三分之一流量
title_original: Yeltsin in the AI Aisle
date: '2026-07-23'
source: Tomasz Tunguz
source_url: https://www.tomtunguz.com/yeltsin-in-the-ai-aisle/
author: ''
summary: 文章以OpenRouter平台数据为例，指出一年前的GPT-OSS-120b仍占据Claude Opus 4.8流量的36%，揭示AI推理市场已按成本、速度和精度分化。混合专家架构使118B模型以26B模型的解码成本运行，大幅提升本地部署能力。作者通过实测发现，Laguna
  S 2.1相比Gemma 4 26B将工具调用错误率降低7个百分点。竞争推动下，前沿模型不再服务所有Token，本地层级天花板被抬高。
categories:
- 技术趋势
tags:
- 模型分化
- 混合专家架构
- 本地部署
- Token市场
- 开源模型
draft: false
translated_at: '2026-07-29T05:30:43.186760'
---

简而言之：一年前的GPT-OSS-120b在OpenRouter上仍占据Claude Opus 4.8每日Token流量的36%，因为推理市场已按成本、速度和精度发生分化。GLM 5.2如今以每日4950亿Token的规模超越前沿模型，而Opus 5的发布则意在争夺开源权重领域。混合专家架构使一个118B模型能以26B模型的解码成本运行，从而拓展了本地部署的边界。

1989年，鲍里斯·叶利钦在休斯顿的一家Randalls超市驻足，被琳琅满目的冰淇淋所震撼。¹OpenRouter之于AI，正如那家超市的冰柜货架。

而购物者的选择出人意料：OpenAI一年前的开源模型GPT-OSS 120b²占据了Anthropic的Opus 4.8流量的36%。³

为何一个2025年8月的模型，仍能保有数周前刚发布的前沿模型三分之一的流量？

Token市场已经分化。

![OpenRouter上每日Token服务量（7日平均值）：GLM 5.2以4950亿居首，Claude Opus 4.8为1996亿；一年前的GPT-OSS-120b持有713亿，约为Opus的三分之一，Gemma 4 26B为500亿，其余开源模型递减至Phi-4的9000万](/images/posts/576c1ffa0eb4.jpg)

分化源于买家需求的多样性。

在竞争驱动下，这种分化正在加速。上周，Anthropic发布了更小、更便宜的Opus 5，⁴明确对标Moonshot的Kimi 3所瞄准的市场。⁵在中型模型市场，Poolside推出了Laguna S 2.1，一款面向美国中端市场的模型。⁶

规模（小、中、大、超大）、来源（美国vs中国）、架构（密集vs稀疏）、精度（专注编码或通用）、速度（每秒Token数）、模态（纯文本或视觉）——AI有着众多风味。

我花了一个周末替换驱动我Agent的模型。原模型是Gemma 4 26b；挑战者是Laguna S 2.1，一个1180亿参数的模型。根据所有我认为重要的指标，118B模型本应更慢。

但在我的M5 Max上，两者生成速度相同，因为Laguna采用了混合专家架构：1180亿参数驻留内存，但每个Token仅激活80亿。一个118B模型如今以26B模型的解码成本运行，将前沿级别的质量拉低至本地层级。

精度在关键之处显现。我的本地栈运行着一个基于工具调用的编码与邮件Agent，在我轮换测试的模型中，随着激活参数的增加，工具调用失败率从29.4%降至20.1%。⁷Laguna相比它所替代的26B模型，将错误率降低了7个百分点。

![驱动生产自动化栈的本地模型的MCP工具调用失败率（基于真实流量测量）：Ornith-1.0 35B为29.4%，Gemma 4 26B为27.1%，Laguna S 2.1为20.1%，比Gemma减少约四分之一](/images/posts/ea9f8a354e06.jpg)

分化是健康竞争市场的标志。前沿模型仍在服务世界上最难的Token，但它不再需要服务所有Token。而我笔记本电脑上的本地层级，其天花板已被大幅抬高——这一趋势将在竞争推动下不可阻挡地向前发展。

1. 鲍里斯·叶利钦1989年访问休斯顿一家杂货店，位于克利尔湖的Randalls，1989年9月16日。↩︎
2. 介绍gpt-oss（OpenAI），2025年8月5日发布。↩︎
3. OpenRouter模型活动页面，7日平均值，检索于2026年7月27日：GPT-OSS-120b，GLM 5.2，Claude Opus 4.8。↩︎
4. Anthropic以半价推出Claude Opus 5，2026年7月24日发布。↩︎
5. Moonshot的Kimi 3预计将缩小与Anthropic的Opus 4.8的差距（TechCrunch）。↩︎
6. 介绍Laguna S 2.1（Poolside），一个总参数118B、激活参数8B的开源权重模型，2026年7月22日发布。↩︎
7. 作者的生产数据：来自本地编码与邮件Agent的MCP工具调用日志，在五个月内对三个本地模型进行测量。↩︎

鲍里斯·叶利钦1989年访问休斯顿一家杂货店，位于克利尔湖的Randalls，1989年9月16日。↩︎

介绍gpt-oss（OpenAI），2025年8月5日发布。↩︎

OpenRouter模型活动页面，7日平均值，检索于2026年7月27日：GPT-OSS-120b，GLM 5.2，Claude Opus 4.8。↩︎

Anthropic以半价推出Claude Opus 5，2026年7月24日发布。↩︎

Moonshot的Kimi 3预计将缩小与Anthropic的Opus 4.8的差距（TechCrunch）。↩︎

介绍Laguna S 2.1（Poolside），一个总参数118B、激活参数8B的开源权重模型，2026年7月22日发布。↩︎

作者的生产数据：来自本地编码与邮件Agent的MCP工具调用日志，在五个月内对三个本地模型进行测量。↩︎

---

> 本文由AI自动翻译，原文链接：[Yeltsin in the AI Aisle](https://www.tomtunguz.com/yeltsin-in-the-ai-aisle/)
> 
> 翻译时间：2026-07-29 05:30
