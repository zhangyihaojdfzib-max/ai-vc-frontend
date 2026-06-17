---
title: 本地编码栈崛起：免费替代Claude/GPT
title_original: '5x for Free : The Local Coding Stack'
date: '2026-06-16'
source: Tomasz Tunguz
source_url: https://www.tomtunguz.com/local-coding-models/
author: ''
summary: Hacker News上关于用本地模型替代Claude/GPT进行日常编码的讨论揭示了本地编码栈的成熟图景。Qwen 3.6 35B-A3B以33%提及率成为主流模型，Pi和OpenCode是领先的轻量级Agent框架。本地模型在SWE-bench测试中接近前沿性能，虽与Claude
  Opus存在差距，但提供隐私、零成本和离线能力，对许多开发者而言是值得的权衡。
categories:
- 技术趋势
tags:
- 本地模型
- 编码Agent
- Qwen
- 开源AI
- 开发者工具
draft: false
translated_at: '2026-06-17T07:06:49.466828'
---

今天，Hacker News 上一个帖子提出了一个简单的问题：“有人已经用本地模型取代 Claude/GPT 进行日常编码了吗？”在 1500 多条评论之后，本地编码栈的清晰图景浮现了出来。

![Qwen3.6 35B-A3B 在本地编码设置中的模型提及率占主导地位](/images/posts/178116495908.jpg)

Qwen 3.6 35B-A3B 以 33% 的提及率占据主导地位，其次是 27B 变体，占 20%。DeepSeek Pro 和 Gemma4 31B 位列前四。共同点是：混合专家架构，能在消费级硬件上快速运行。

![Pi 和 OpenCode 引领本地编码 Agent](/images/posts/a7cd67b83e44.jpg)

在 Agent 方面，Pi 以 49% 领先，OpenCode 紧随其后，占 45%。两者都是为本地推理设计的轻量级框架。

这个帖子揭示了一个有趣的权衡。一位评论者完美地捕捉了这一点：

将 Agent 化的 Qwen3.6 35b 与 Claude Opus 进行比较，就像是一个知识面广但需要你大力引导的初级开发者，与一个能与你一起思考架构的高级开发者。如果 Opus 带来 15 倍的加速，那么本地且完全离线的 Qwen 则带来 5 倍的加速。

但对许多人来说，这种权衡是值得的。隐私、零成本和完全离线能力很重要。

考虑到它完全免费，这仍然让我感到难以置信。

本地编码栈正在快速成熟。Qwen 3.6 35B-A3B 已成为事实上的标准，而 Pi 是领先的框架。

![本地模型在 SWE-bench Verified 上接近前沿性能](/images/posts/b4ef9babed60.jpg)

基准数据支持了这一观点。Qwen3.6 27B 得分为 77.2%，而 MoE 变体 Qwen3.6 35B-A3B 达到了 73.4%。这两个本地模型与 Claude Sonnet 4.6（79.6%）的差距微乎其微。

这是最小可行模式在实时上演。它不仅仅适用于 CRM 更新和网络研究。当前一代的本地模型对于合理的编码任务已经足够好。

1. https://news.ycombinator.com/item?id=48542100↩︎
2. MoE 模型是只激活总参数中一小部分的大模型。Qwen 3.6 35B-A3B 总共有 350 亿参数，但在推理时仅激活 30 亿，而 27B 变体每次运行全部 270 亿参数。↩︎
3. SWE-bench Verified 分数来自 llm-stats.com 和 morphllm.com，2026 年 6 月。↩︎

https://news.ycombinator.com/item?id=48542100↩︎

MoE 模型是只激活总参数中一小部分的大模型。Qwen 3.6 35B-A3B 总共有 350 亿参数，但在推理时仅激活 30 亿，而 27B 变体每次运行全部 270 亿参数。↩︎

SWE-bench Verified 分数来自 llm-stats.com 和 morphllm.com，2026 年 6 月。↩︎

---

> 本文由AI自动翻译，原文链接：[5x for Free : The Local Coding Stack](https://www.tomtunguz.com/local-coding-models/)
> 
> 翻译时间：2026-06-17 07:06
