---
title: 谁在买最先进的AI模型？
title_original: Honestly, Who Buys SOTA?
date: '2026-08-14'
source: Tomasz Tunguz
source_url: https://www.tomtunguz.com/model-release-exhaustion/
author: ''
summary: 文章指出，尽管最先进AI模型性能持续快速提升，但OpenRouter上84%的Token流量来自非前沿模型。六个主流模型以极低成本提供约77%的前沿性能，显示市场对价格高度敏感。企业整合支出，开源模型性能追赶，应用部署更注重性价比。前沿模型在软件架构和安全设计上仍有优势，但经济模型面临挑战，训练投入需赢得市场份额才能回收。
categories:
- AI基础设施
tags:
- AI模型
- 成本效益
- 市场趋势
- 开源模型
- 前沿性能
draft: false
translated_at: '2026-08-15T03:00:56.097648'
---

简而言之：最先进的模型比去年11月聪明了三分之二，实验室每三天发布两个新模型。但OpenRouter上84%的Token并非来自最先进的模型。承载绝大多数流量的六个模型，以Claude Fable 5价格2.5%的成本，提供了约77%的前沿性能。Ramp的数据显示了市场的价格弹性。前沿模型在软件架构和安全设计上仍然胜出；应用部署则优化了另一条帕累托前沿——价格优先于性能。

最先进的模型比去年11月聪明了三分之二。这种狂热的改进步伐持续不减，每三天就有两个新模型问世。¹

![自2025年11月以来主要实验室每月模型发布情况，平均每月约20个](/images/posts/c5273ef41c1c.jpg)

但OpenRouter上84%的Token并非来自最先进的模型。²³

事实上，用户选择用来生成绝大多数Token的六个模型，提供了约77%的前沿性能。它们的成本仅为Claude Fable 5的2.5%。²

指数持续攀升。大约每季度就会出现一次三到五个Artificial Analysis分数的大幅跃升。较小的步进填补了其间空白。

![新模型刷新Artificial Analysis智能前沿时的步进增益](/images/posts/6ddd0d08815e.jpg)

在8月10日那一周，六个模型承载了80%的流量。它们的混合价格为每百万Token 0.50美元，而Fable 5为20美元。

![OpenRouter头部模型以Fable四十分之一的价格提供最先进质量77%的性能](/images/posts/5eb7b3cd2e52.jpg)

Ramp的数据显示买家具有价格弹性。Fable 5以约每百万Token 10美元的价格，在发布一个月后占据了Anthropic Token流量的6%和Anthropic支出的11%。GPT-5.6 Sol作为OpenAI最昂贵的主流层级，保持了OpenAI约四分之一的Token流量。⁴

7月份，Fable 5产生的模型归属收入约为GPT-5.6 Sol的75%，尽管其价格要高得多。

每一次新的最先进版本发布，其市场份额变动都应小于前一次。

企业将整合支出。合同集中在少数一两个供应商手中，就像云计算时代一样，一旦某个模型通过了高价值任务的考验，工作负载就会留在那里。

性能在有意义的折扣下已经足够好。差距持续从下方收窄。最佳开源权重模型在5月份达到了前沿分数的80%，而一年前这一数字仅为48%。²

应用部署则是另一回事。越来越多的投资组合公司和初创企业默认选择较小的模型、微调模型和开源模型。它们在优化另一条不同的帕累托前沿——价格优先于性能。

如果市场份额停止转移，且“够用就好”持续成立，那么最先进模型的经济学就会改变。一次九位数的训练投入必须赢得市场份额才能收回成本，而这个门槛将随着时间推移不断提高。

这个标题有些轻率。很多人确实购买最先进的模型，而且理由充分。软件工程架构和安全设计是最明显的案例，在这些领域，最好的可用模型物有所值。

但我们确实拥有的公开数据表明，真正重要的前沿是另一条。

---

1. Artificial Analysis模型目录与智能指数。主要实验室月度发布数量与前沿路径。样本起始于2025年11月1日。发布速率趋势平稳。大型（≥3分）前沿跃升之间的中位间隔约为3.5个月。Intelligence Index↩︎

2. 最先进指给定一周内可获得的最高Artificial Analysis分数；当某个模型的分数在该周最佳命名模型的10%以内时，即视为接近前沿。OpenRouter每周命名头部模型与Artificial Analysis分数匹配，取OpenRouter轮播图头部而非每个API。份额序列，2025年11月3日至2026年5月25日（n=30），仅限命名模型，排除Others。前十三周与后十三周对比：接近前沿的比例约为17.5%对14.6%（外部约82-85%）。集中度快照，2026年8月10日当周，覆盖前约80%命名Token的模型。Token加权Artificial Analysis分数落后全球目录最先进水平约23%（约为前沿质量的77%），落后该OpenRouter列表最佳模型约10%。混合篮子约每百万Token 0.50美元，对比Fable 5的每百万Token 20美元（约40倍）。2026年5月历史核查，落后本地列表领先者约16%。最佳开源权重模型在前十三周达到前沿分数的47.5%，后十三周为70.9%；单周最佳为2026年5月25日，DeepSeek V4 Pro得分45.27对比前沿56.31（80.4%）。OpenRouter rankings↩︎↩︎↩︎

3. 这些数据源未涵盖第一方云服务，即OpenAI、Anthropic和Google自有服务。运行在原生API上的前沿流量从未进入OpenRouter排名，因此数据存在偏差。↩︎

4. Ramp Economics Lab，AI指数2026年8月（Fable 5采用情况）。econlab.substack.com/p/ai-index-august-2026↩︎

---

Artificial Analysis模型目录与智能指数。主要实验室月度发布数量与前沿路径。样本起始于2025年11月1日。发布速率趋势平稳。大型（≥3分）前沿跃升之间的中位间隔约为3.5个月。Intelligence Index↩︎

最先进指给定一周内可获得的最高Artificial Analysis分数；当某个模型的分数在该周最佳命名模型的10%以内时，即视为接近前沿。OpenRouter每周命名头部模型与Artificial Analysis分数匹配，取OpenRouter轮播图头部而非每个API。份额序列，2025年11月3日至2026年5月25日（n=30），仅限命名模型，排除Others。前十三周与后十三周对比：接近前沿的比例约为17.5%对14.6%（外部约82-85%）。集中度快照，2026年8月10日当周，覆盖前约80%命名Token的模型。Token加权Artificial Analysis分数落后全球目录最先进水平约23%（约为前沿质量的77%），落后该OpenRouter列表最佳模型约10%。混合篮子约每百万Token 0.50美元，对比Fable 5的每百万Token 20美元（约40倍）。2026年5月历史核查，落后本地列表领先者约16%。最佳开源权重模型在前十三周达到前沿分数的47.5%，后十三周为70.9%；单周最佳为2026年5月25日，DeepSeek V4 Pro得分45.27对比前沿56.31（80.4%）。OpenRouter rankings↩︎↩︎↩︎

这些数据源未涵盖第一方云服务，即OpenAI、Anthropic和Google自有服务。运行在原生API上的前沿流量从未进入OpenRouter排名，因此数据存在偏差。↩︎

Ramp Economics Lab，AI指数2026年8月（Fable 5采用情况）。econlab.substack.com/p/ai-index-august-2026↩︎

---

> 本文由AI自动翻译，原文链接：[Honestly, Who Buys SOTA?](https://www.tomtunguz.com/model-release-exhaustion/)
> 
> 翻译时间：2026-08-15 03:00
