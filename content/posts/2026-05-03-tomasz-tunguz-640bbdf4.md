---
title: 每天8条广告，就能撑起万亿参数AI模型
title_original: All the AI You Need for 8 Ads per Day
date: '2026-05-03'
source: Tomasz Tunguz
source_url: https://www.tomtunguz.com/ad-supported-ai-works/
author: ''
summary: 本文通过详细的经济模型论证了广告支持型AI商业模式的可行性。作者对比了GPU算力成本与广告CPM数据，指出每40分钟展示一条搜索广告或每3分钟展示一条内容广告即可覆盖万亿参数模型的运行成本。对于更重的负载（如Agent编程），纯广告模式难以支撑，但混合模式（如每月10美元加每天8条广告）仍可覆盖200万Token的消耗。文章认为，结合开源模型、通用GPU和移动端级别的广告频率，广告支持型AI是可行的商业模式。
categories:
- AI基础设施
tags:
- 广告支持型AI
- 商业模式
- GPU成本
- 开源模型
- Token经济
draft: false
translated_at: '2026-05-05T05:05:51.930049'
---

每40分钟展示一条搜索广告，就足以支撑一个万亿参数模型的运行成本。每3分钟展示一条内容广告，效果同样如此。广告支持型AI的商业模式，其经济账比你想象中更划算。

上个月，Anthropic将Claude Code从20美元套餐中移除，这标志着行业的一种共识：前沿智能需要前沿定价。而对于开源模型而言，经济逻辑则截然不同。

一台B200 GPU在现货市场上的价格为每小时4.50美元¹。谷歌搜索广告的CPM（每千次展示成本）为38.40美元²，而谷歌展示广告的CPM为3.12美元³。

这些数字假设服务商运行4台B200 Blackwell GPU，服务300名用户，负载为理论最大值的50%，为流量高峰预留了余量⁴。

为了覆盖这些成本，用户每3到39分钟会看到一条广告。这远低于用户已经能够容忍的频率：超休闲手机游戏每次会话展示6条广告，大约每分钟一条⁵。

其中存在一些细微差别。假设广告填充率（即返回付费广告的广告请求比例）和广告网络收入分成，我们可以模拟出有效CPM为1.50美元。在这个最低水平上，广告频率翻倍。每90秒展示一条内容广告仍能覆盖集群成本，与手机用户已经习惯的频率相当。

在另一个极端，激励视频广告的CPM可达40至50美元，且在游戏领域填充率接近100%。整个集群中一轮激励视频广告的收入，几乎就能覆盖一小时的算力成本⁶。

但这里还存在利用率的问题。所有这些数字都假设集群保持忙碌状态。闲置的GPU会提高每用户成本。

那么更重的负载呢？Agent（智能体）编程消耗的Token量是被动聊天的10到20倍⁷。在这种速率下，纯广告模式无法支撑。但混合模式可行：每月10美元加上每天8条广告，可以覆盖200万Token⁸。这虽然不足以支撑一个“Token消耗狂”的习惯，但足以让你持续交付产品。

广告支持型AI是可行的：开源模型、通用GPU，以及已经与移动端和网页端相当的广告频率。

1. B200 Cloud Pricing: Compare 22+ Providers (2026): 在22家云服务商中，现货市场平均价格为每小时3.40至4.50美元。↩︎
2. Online Advertising Costs In 2026 (Top Draw): 谷歌搜索广告平均CPM为38.40美元（由CPC × 预估CTR推导得出；搜索广告通常按点击付费，此处为便于比较进行了换算）。↩︎
3. Online Advertising Costs In 2026 (Top Draw): 谷歌展示广告平均CPM为3.12美元。↩︎
4. GPU Concurrency Benchmark: H100 vs H200 vs B200 (AIMultiple): Kimi K2.6在4台B200上峰值支持600并发用户；此处使用300作为保守运营目标。↩︎
5. The 2026 AdMob & Mobile Monetization Playbook (MonetizeMore): 超休闲游戏基准为每次会话6条广告，每天3.2次会话。↩︎
6. 计算：300用户 × 每人1次激励展示 × 0.05美元（按50美元CPM计算）= 15美元。集群成本 = 18美元/小时。15美元 ÷ 18美元 = 83%，约等于50分钟。↩︎
7. Claude Code vs Cursor: Speed, Accuracy & Cost Benchmark 2026 (SitePoint): Claude Code每任务使用33K Token；Cursor使用188K Token。重度用户每天执行20到60个任务，活跃会话期间每小时消耗1到2M Token，是被动聊天的10到20倍。↩︎
8. 计算：10美元/月 = 0.33美元/天。仅靠0.33美元/天，集群可支持1309名用户每人每天1M Token，仅为目标的一半。剩余0.33美元/天的缺口由广告填补。按激励视频广告CPM 40美元计算，即每天8次展示。合计：10美元/月 + 8条广告/天 = 每用户每天2M Token。↩︎

B200 Cloud Pricing: Compare 22+ Providers (2026): 在22家云服务商中，现货市场平均价格为每小时3.40至4.50美元。↩︎

Online Advertising Costs In 2026 (Top Draw): 谷歌搜索广告平均CPM为38.40美元（由CPC × 预估CTR推导得出；搜索广告通常按点击付费，此处为便于比较进行了换算）。↩︎

Online Advertising Costs In 2026 (Top Draw): 谷歌展示广告平均CPM为3.12美元。↩︎

GPU Concurrency Benchmark: H100 vs H200 vs B200 (AIMultiple): Kimi K2.6在4台B200上峰值支持600并发用户；此处使用300作为保守运营目标。↩︎

The 2026 AdMob & Mobile Monetization Playbook (MonetizeMore): 超休闲游戏基准为每次会话6条广告，每天3.2次会话。↩︎

计算：300用户 × 每人1次激励展示 × 0.05美元（按50美元CPM计算）= 15美元。集群成本 = 18美元/小时。15美元 ÷ 18美元 = 83%，约等于50分钟。↩︎

Claude Code vs Cursor: Speed, Accuracy & Cost Benchmark 2026 (SitePoint): Claude Code每任务使用33K Token；Cursor使用188K Token。重度用户每天执行20到60个任务，活跃会话期间每小时消耗1到2M Token，是被动聊天的10到20倍。↩︎

计算：10美元/月 = 0.33美元/天。仅靠0.33美元/天，集群可支持1309名用户每人每天1M Token，仅为目标的一半。剩余0.33美元/天的缺口由广告填补。按激励视频广告CPM 40美元计算，即每天8次展示。合计：10美元/月 + 8条广告/天 = 每用户每天2M Token。↩︎

---

> 本文由AI自动翻译，原文链接：[All the AI You Need for 8 Ads per Day](https://www.tomtunguz.com/ad-supported-ai-works/)
> 
> 翻译时间：2026-05-05 05:05
