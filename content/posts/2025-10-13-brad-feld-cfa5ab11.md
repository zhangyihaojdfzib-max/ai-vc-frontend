---
title: 从氛围编程到AI结对编程：我的五阶升级之路
title_original: Leveling Up in the Vibe Coding Video Game
date: '2025-10-13'
source: Brad Feld
source_url: https://feld.com/archives/2025/10/leveling-up-in-the-vibe-coding-video-game/
author: ''
summary: 作者回顾了从零开始借助AI工具学习现代软件开发的过程，经历了从Cursor、Claude到ChatGPT等多种工具的尝试与挫折。最初将这种模式称为“氛围编程”，但在实践中发现需要持续监督、反馈和协作，最终将其重新定义为“AI结对编程”。文章详细描述了五个阶段的演进，包括工具选择、代码质量挑战、成本控制以及协作方式的转变，最终在Claude
  Code 2的帮助下实现了真正的协作突破，强调了AI作为编程伙伴而非替代者的核心观点。
categories:
- 技术趋势
tags:
- AI编程
- 结对编程
- 开发者工具
- Cursor
- Claude
draft: false
translated_at: '2026-03-07T04:26:58.657546'
---

虽然"氛围编程"这个词初次听到时很抓耳，但总让我感觉有些误导性。如今，在33年未写代码后重新升级为"合格个体软件开发者"的我，认为这个说法并不准确。我更倾向于将这种模式称为AI结对编程。

去年圣诞节开始接触AI编程工具时（主要是因为无聊），我对现代软件开发技能一窍不通。尽管自1992年以来就没写过生产代码，但我每隔几年都会尝试新语言：Perl、Ruby、Ruby on Rails（勉强算吧）、Python、Clojure。我只会写"Hello World"和简单功能，始终没突破CSS基础、工具链或部署这些关卡。虽有Github账户偶尔折腾，但总因懒得研究PR细节而放弃——命令行工具实在太多了。

**第一阶**：下载Cursor。在试图搞懂Django运作原理（又一套线上课程）失败后，转用Next.js。这让我接触到Vercel，几位20多岁的朋友也证实酷孩子们都在用（虽然Render、Digital Ocean和AWS都刷过我的信用卡）。很快我就用Cursor与Vercel、Supabase、Clerk、Github搏斗。发现Auto模式无趣后，转向Claude 3.5，结果搞出恐龙代码（满是安全漏洞...）

**第二阶**：开始认真些。发现Linear工具，与Notion缠斗，形成几个创意和更宏观的构想，并做出了v0.1版本。

**第三阶**：鉴于人人都在谈论Lovable，我以为它比Cursor更优。浪费200美元后，靠氛围编程做出酷炫设计，却目睹它在处理数据复杂性和AI调用的实际功能时陷入混乱。考虑尝试Bolt和Replit时，经大量调研意识到可能遭遇同样问题。

于是回归Cursor，全力优化系统提示词，持续调整。见证Cursor在多方面快速进化（MCP功能——太棒了！默认Agent模式——终于来了），同时看着账单上涨。当发现阿斯彭餐厅人均消费至少100美元时，很容易就决定升级到Max模式——月费从20美元跳到200美元。

**第四阶**：徘徊良久。Cursor持续改进，Claude 4发布。Auto模式仍会脱轨毁掉代码。开始重构时发现代码废料堆积如山，小bug在让Cursor修复时演变成致命缺陷。学会了"git reset --hard HEAD"，耗费大量时间在localhost:3000的配置问题上（至少搞定了让Cursor始终在此端口启动）。开始用Docker，困惑于Cursor记不住昨日指令，但理性理解这是记忆机制使然。

这阶段的快乐终结于ChatGPT 5发布并在Cursor免费开放一周时。初体验极速流畅，大量改动看似有效。但几天后——天啊，它生成的代码乱成一团！为何所有API路由突然崩溃？控制台语句遍地开花？相同功能的UI组件在不同位置长得完全不同？回归Claude进行代码审查和大重构，遭遇无数Vercel构建错误，最终拥抱CI/CD、Prettier和Husky。当月Cursor额度耗尽转为按量计费，消费800美元后醒悟：根本不需要为这些工作调用Opus或思考模型。

第四阶煎熬漫长，却正是我开始视之为AI结对编程的转折点。AI（或智能体/子智能体）成为我的键盘搭档，打字远快于我。但我必须全程监督，不断检查，提供反馈，指出修改方向，并记录重要事项。

直到九月底Claude Code 2伴随Sonnet 4.5发布，我才迎来突破。经历ChatGPT 5风波后回归Claude（Sonnet版），开始称这位结对伙伴为"Claudia"。我将Claudia视作人类程序员搭档来相处，彻底改变协作方式。当在终端加载Claude Code 2（只需输入"Claude"），瞬间再次升级。

至此，我抵达这场游戏的**第五阶**。它已从氛围编程蜕变为真正的AI结对编程——而且依然充满乐趣！

---

> 本文由AI自动翻译，原文链接：[Leveling Up in the Vibe Coding Video Game](https://feld.com/archives/2025/10/leveling-up-in-the-vibe-coding-video-game/)
> 
> 翻译时间：2026-03-07 04:26
