---
title: AI工程生产力：从20%到3倍的跃迁
title_original: AI Engineering Productivity is Anything But Normal
date: '2026-07-21'
source: Tomasz Tunguz
source_url: https://www.tomtunguz.com/ai-engineering-productivity-anything-but-normal/
author: ''
summary: 文章指出AI工程生产力成果分为三个层级：部署AI IDE仅带来20-46%的平均提升；围绕Agent构建运营层的公司实现2.5-3倍前沿水平；而将Agent作为一级组织单元的软件工厂则达到8倍以上提升。差距不在模型本身，而在于运营规范。NVIDIA、Amplitude、Anthropic等公司数据表明，多数团队应从20%提升迁移到3倍生产力，这并非正常现象。
categories:
- 技术趋势
tags:
- AI工程
- 生产力提升
- AI Agent
- 软件工厂
- 运营规范
draft: false
translated_at: '2026-07-24T05:27:30.323188'
---

简而言之：AI工程生产力成果可分为三个层级：平均提升20-46%来自部署IDE，2.5-3倍前沿水平来自围绕Agent（智能体）构建运营层的公司（Replit、NVIDIA、Amplitude、Anthropic），以及8倍以上的工厂层级，其中Agent（智能体）作为一级组织单元运作（Nubank与Devin）。差距不在于模型本身，而在于围绕模型构建的运营规范。

我们现在正处于一个应当期待彼此产出提升3倍的时代。

过去六个月里，数据点接踵而至：

- NVIDIA报告称，在30,000名开发者中，提交代码量提升了3倍，而缺陷率保持稳定。¹
- Amplitude的每周生产提交量增加了两倍，AI Agent（智能体）现已成为代码库的前三大贡献者之一。²
- Anthropic衡量发现，自内部采用Claude Code以来，每位工程师编写的代码量增加了2.5倍，质量保持稳定。³
- Replit在同一时期团队规模翻倍，每位工程师的产出增加了两倍，而审查时间、回滚次数和事故数量均保持平稳。⁴

![ai-eng-productivity-distribution](/images/posts/d5c20cc3eed5.jpg)

上图将生态系统划分为三个不等的层级，每个层级由公司捕获模型能力的程度所定义。⁵

第一个层级是当今大多数公司的体验。分发一个AI IDE，其他一切不变，结果较为有限。

“工程领导者曾期望AI带来2-3倍的生产力提升，但实际结果更接近30%。”

— Augment Code⁶

Faros对22,000名开发者的遥测数据证实了这一点：工程师完成大型任务的效率提升了66%，但每位开发者的缺陷数增加了54%。⁷谷歌的随机对照试验给出的数字是21%，接近GitHub的24%。⁸⁹这是默认结果。

接下来是前沿层级。此处的公司围绕模型构建了控制框架，编排在GitHub、Linear和Slack之间共享上下文的Agent（智能体）；并将问题升级给工程师进行判断。

“每位员工都有一个管理Agent（智能体），它会循环生成工作Agent（智能体）。我们的内部Agent（智能体）在安全测试和事故分类方面以十分之一的成本超越了七位数的SaaS工具。”

— Amjad Masad, Replit, “The Self-Driving Company”⁴

人工PR审查时间下降了30%。复杂支持处理时间下降了60%。总代码贡献量提升了5.8倍。这就是3倍数字所在之处。

第三个层级是软件工厂，这个名称恰如其分。它们是机械式生产软件的AI机器。Cognition的Devin端到端重构单体代码库。Factory.ai正在NVIDIA、Adobe、Blackstone和EY部署软件工厂。¹⁰

“Nubank使用Devin进行大规模重构，实现了工程效率8倍的提升和成本20倍的降低。”

— Contrary Research, 2026年1月¹¹

高盛正在与12,000名人类开发者一起试点Devin，并公开估计Agent（智能体）AI的交付速度可能达到先前工具的3-4倍。¹²

AI工程生产力的提升已经到来。初步数据显示了预期：大多数团队应从20%的生产力提升迁移到3倍的生产力提升，而这并非正常现象。

1. Cursor, “How NVIDIA uses Cursor,” 2026年2月。↩︎
2. Cursor, “Amplitude and Cursor cloud agents,” 2026年4月。↩︎
3. Boris Cherny, Claude Code负责人, 在Big Technology播客中, 2026年7月。↩︎
4. Amjad Masad, “The Self-Driving Company,” 2026年7月16日。↩︎↩︎
5. 上述分布为示意性质，非统计数据。每个数据点均来自已发表研究、随机对照试验或公司披露的倍数报告。并非来自抽样总体，曲线是对报告结果模式（而非原始数据）的右偏对数正态拟合。请将其视为形态论证，而非估算器。↩︎
6. Augment Code在X平台, 2026年。↩︎
7. Faros, “AI Engineering Report 2026”。↩︎
8. 谷歌内部随机对照试验, 约100名工程师, 2024年。引用自DORA报告；汇总于Value Add VC。↩︎
9. GitHub、微软和埃森哲与一家大型金融科技公司的研究, 约450名开发者, 2024年。↩︎
10. Factory.ai, “Factory 2.0: From coding agents to software factories”。↩︎
11. Contrary Research, “Cognition”, 2026年1月。↩︎
12. CNBC, “Goldman Sachs is piloting its first autonomous coder in major AI milestone for Wall Street,” 2025年7月。↩︎

Cursor, “How NVIDIA uses Cursor,” 2026年2月。↩︎

Cursor, “Amplitude and Cursor cloud agents,” 2026年4月。↩︎

Boris Cherny, Claude Code负责人, 在Big Technology播客中, 2026年7月。↩︎

Amjad Masad, “The Self-Driving Company,” 2026年7月16日。↩︎↩︎

上述分布为示意性质，非统计数据。每个数据点均来自已发表研究、随机对照试验或公司披露的倍数报告。并非来自抽样总体，曲线是对报告结果模式（而非原始数据）的右偏对数正态拟合。请将其视为形态论证，而非估算器。↩︎

Augment Code在X平台, 2026年。↩︎

Faros, “AI Engineering Report 2026”。↩︎

谷歌内部随机对照试验, 约100名工程师, 2024年。引用自DORA报告；汇总于Value Add VC。↩︎

GitHub、微软和埃森哲与一家大型金融科技公司的研究, 约450名开发者, 2024年。↩︎

Factory.ai, “Factory 2.0: From coding agents to software factories”。↩︎

Contrary Research, “Cognition”, 2026年1月。↩︎

CNBC, “Goldman Sachs is piloting its first autonomous coder in major AI milestone for Wall Street,” 2025年7月。↩︎

---

> 本文由AI自动翻译，原文链接：[AI Engineering Productivity is Anything But Normal](https://www.tomtunguz.com/ai-engineering-productivity-anything-but-normal/)
> 
> 翻译时间：2026-07-24 05:27
