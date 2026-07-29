---
title: AI工具框架：比模型更关键的性能骑手
title_original: Aftermarket Harnesses
date: '2026-07-28'
source: Tomasz Tunguz
source_url: https://www.tomtunguz.com/aftermarket-harnesses/
author: ''
summary: 文章指出，AI工具框架对编程基准测试的影响已超过模型本身。通过对比GPT-5.5和Claude Opus 4.7在不同框架中的表现，发现工具框架能显著提升功能正确率（最高达25.7个百分点）。此外，输入Token占LLM流量的86-98%，智能缓存策略可节省40-80%成本。工具框架通过控制上下文、缓存和信息检索，成为影响成本、质量和准确性的关键支点，第三方框架也能达到与第一方协同设计同等的效果。
categories:
- AI基础设施
tags:
- 工具框架
- AI性能
- 缓存策略
- 编程基准测试
- 成本优化
draft: false
translated_at: '2026-07-29T05:30:42.517445'
---

简而言之：当前，工具框架对编程基准测试的影响已超过模型本身。Endor Labs的Agent安全联盟发现，GPT-5.5在Codex中的功能正确率为61.5%，在Cursor中为87.2%；Claude Opus 4.7在Claude Code中为87.2%，在Cursor中为91.1%。输入Token占OpenRouter流量的86-98%，因此工具框架通过缓存策略控制着大部分成本。第一方协同设计能带来真实的缓存命中率，但第三方工具框架也能达到同等水平。

AI工具框架对性能的影响已超过模型本身。

Endor Labs在同一周内通过两个工具框架运行了相同的模型。OpenAI的GPT-5.5在其原生Codex工具框架中的功能正确率为61.5%，而在Cursor中为87.2%，仅因运行环境不同就产生了25.7个百分点的波动。Anthropic的Opus 4.7在Claude Code中为87.2%，在Cursor中为91.1%。¹

两个前沿模型在竞争对手的工具框架中表现均优于其制造商自带的框架。

工具框架是AI技术栈中的支点。它们影响着成本、质量和准确性。

输入Token占OpenRouter上LLM流量的86-98%。输出每个Token的成本是输入的5倍，但由于输入量巨大，它仍然主导着账单。一年前，我在《饥饿的AI模型》一文中曾思考过这个比例。²从业者表示输入占95%，输出占5%。在规模化场景下，他们是对的。

因此，控制输入成本是一个有价值的命题。模型本身不控制这些成本，但工具框架可以。³工具框架决定发送哪些上下文。这些上下文中很大一部分在多次查询中重复出现。智能缓存可以节省40-80%的成本。一项针对500个长周期Agent会话的研究发现，成本降低41-80%，首Token响应时间加快13-31%，且节省效果在500到50,000个Token的提示词中呈线性增长。⁴最佳方案是仅缓存稳定前缀，并将动态内容置于缓存断点之后。

工具框架还负责信息检索：要读取的代码、风格指南、投资简报中需要分析的部分。内容越简洁精准，成本越低。

Cursor的工具框架在技术细节上与Claude Code一一对应：动态工具获取、基于优先级的组合前缀、双层缓存。这就是为什么Opus 4.7在Cursor中的得分高于Claude Code，也是为什么GPT-5.5在Codex之外的功能正确率几乎翻倍。

捆绑方案并非没有优点。Claude Code将缓存命中率视为运行时间指标，在真实会话中命中率约为96%，同一版本的用户共享系统提示词缓存，并以99%的字节一致性构建分支子Agent，节省90%的成本。⁵

协同设计工具框架、缓存API和模型能带来真正的缓存策略。但策略本身存在于工具框架中，第三方工具框架也能达到同等水平，Cursor的数据证明了这一点。

工具框架已不再是简单的模型包装器；它是一位骑手，将AI性能推向了育种者未曾想象的高度。

¹ Endor Labs，“GPT-5.5在Agent安全联盟中借助Cursor而非Codex创下代码安全新纪录”，2026年4月27日，https://www.endorlabs.com/learn/gpt-5-5-sets-a-new-code-security-record-with-cursor-not-codex-in-agent-security-league。Agent安全联盟基准测试，基于卡内基梅隆大学的Open SusVibes框架。↩︎
² Tomasz Tunguz，“饥饿的AI模型”，2025年7月8日，https://tomtunguz.com/input-output-ratio/↩︎
³ Tomasz Tunguz，“工具框架是新的战场”，https://tomtunguz.com/the-harness-is-the-new-battleground/↩︎
⁴ Lumer等人，“不要破坏缓存：长周期Agent任务中提示词缓存的评估”，arXiv:2601.06007，2026年。https://arxiv.org/abs/2601.06007↩︎
⁵ Anthropic，“构建Claude Code的经验教训：提示词缓存至关重要”，2026年4月，https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything；交换税数据来自Digital Applied，“提示词缓存经济学：缓存优先的Agent设计”，2026年7月，https://www.digitalapplied.com/blog/prompt-caching-economics-cache-first-agent-architecture-2026。↩︎

Endor Labs，“GPT-5.5在Agent安全联盟中借助Cursor而非Codex创下代码安全新纪录”，2026年4月27日，https://www.endorlabs.com/learn/gpt-5-5-sets-a-new-code-security-record-with-cursor-not-codex-in-agent-security-league。Agent安全联盟基准测试，基于卡内基梅隆大学的Open SusVibes框架。↩︎

Tomasz Tunguz，“饥饿的AI模型”，2025年7月8日，https://tomtunguz.com/input-output-ratio/↩︎

Tomasz Tunguz，“工具框架是新的战场”，https://tomtunguz.com/the-harness-is-the-new-battleground/↩︎

Lumer等人，“不要破坏缓存：长周期Agent任务中提示词缓存的评估”，arXiv:2601.06007，2026年。https://arxiv.org/abs/2601.06007↩︎

Anthropic，“构建Claude Code的经验教训：提示词缓存至关重要”，2026年4月，https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything；交换税数据来自Digital Applied，“提示词缓存经济学：缓存优先的Agent设计”，2026年7月，https://www.digitalapplied.com/blog/prompt-caching-economics-cache-first-agent-architecture-2026。↩︎

---

> 本文由AI自动翻译，原文链接：[Aftermarket Harnesses](https://www.tomtunguz.com/aftermarket-harnesses/)
> 
> 翻译时间：2026-07-29 05:30
