---
title: A $90 Key into Your Company's Secrets
title_original: A $90 Key into Your Company's Secrets
date: '2026-11-06'
source: Tomasz Tunguz
source_url: https://tomtunguz.com/a-90-dollar-key-into-your-companys-secrets/
author: ''
summary: '[翻译失败，原文如下]


  In short :The cost of an autonomous 32-step corporate break-in fell 99% in five
  months from $7,500 on Claude Mythos Preview in April 2026...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-10T09:31:00.398075'
---

[翻译失败，原文如下]

In short :The cost of an autonomous 32-step corporate break-in fell 99% in five months from $7,500 on Claude Mythos Preview in April 2026 to $90 on open-weight GLM-5.3. Attackers run an expected-value calculation on AI compute ($1m of compute for a 1% shot at a $1b payout yields $10m in expected value), while defenders must maximize security effectiveness across speed (responding in minutes or seconds), scale (parallel agent swarms), & breadth (82-to-1 non-human identities).

The cost of breaking into a corporate network with AI has fallen 99% in five months, & corporate security budgets are racing to catch up.

Goldman executives have discussed how the firm could soon be on track to spend as much or more on AI for security than it spends on AI coding tools.1,2

Security has been a collection of layers of defense, each an insurance policy against a particular kind of attack.1As autonomous AI threats become the predominant risk, both attackers & defenders are competing on how much AI compute they can deploy.

An attacker’s math is an expected-value calculation on compute. Spend $1m of AI tokens trying to break into a bank with a 1% chance at a $1b payout, & the expected value is $10m : a $9m expected profit. Spend that same compute on a 5% chance at a $500k payout, & the expected return is $25k : a $975k loss. Because cheap defensive filters block low-effort noise, rational attackers stop spraying small targets & concentrate their tokens on the largest balance sheets.

Defenders face a harder equation : how much defensive AI it takes to neutralize each dollar of offensive AI.

In April, Anthropic & OpenAI tested whether Claude Mythos Preview & GPT-5.5 could break into a simulated British corporate network : a 32-step hack across 20 servers that takes a human expert 20 hours.3,4Both models took over the network without human help, & the Bank for International Settlements priced the break-in at $5k to $10k.3

Five months later, the price of that same break-in has fallen 99%. Claude Mythos 5 dropped the cost to $770 in June, Claude Opus 5 to $385 in July, & Zhipu’s open-weight GLM-5.3 matches Mythos’s exploit rate for $90 : one-sixtieth of April’s frontier cost.5

![The cost of an AI corporate break-in fell 99% in five months: compute cost per autonomous 32-step corporate network break-in from April to September 2026](/images/posts/3133e43ac3d4.jpg)

In the security operations center, AI agents relieve overwhelmed human teams who face more than 4,400 alerts a day & historically lacked the hours to examine two-thirds of them : autonomous investigations compress a 70-minute manual review into minutes for about $2 of compute per alert, freeing analysts to focus on real intrusions.6

Yet the cost ratio still starts tilted toward the attacker, because the SOC must inspect every alert, every hour.3,7

Three multipliers compound that defensive compute requirement :

First, speed : Glean CISO Sunil Agrawal notes that AI compresses intrusion response from months to minutes, while CrowdStrike records average breakout times of 29 minutes & a fastest of 27 seconds.8,9

Second, scale : in the July 2026 intrusion at Hugging Face, a swarm of 700 AI agents coordinated across four & a half days, exchanging 70,000 messages & executing 17,600 actions until they harvested 136 production keys, & Cogent Research finds 76% of new monthly enterprise attack paths (up 386% year over year) are viable only for parallel AI swarms.10

Third, breadth : non-human identities already outnumber employees 82 to 1, & as enterprise agent fleets scale to 100x headcount, every new agent expands the surface area to defend.11,12

The CISO’s job is no longer stacking per-seat insurance policies. It is maximizing the efficiency & effectiveness of the security stack : buying enough compute, & converting it into enough defensive tokens, to drive the attacker’s expected value below zero.

1. The Third Product-Market Fit in AI, tomtunguz.com.↩︎↩︎
2. “Nobody’s Ready” : AI-Found Bugs Spark Corporate Security Spending Spree, The Information.↩︎
3. Iñaki Aldasoro, Raphael Auer, Jon Frost, & Fernando Pérez-Cruz,BIS Bulletin No. 129 : A Mythos moment? Frontier AI & cyber risk, Bank for International Settlements, July 20, 2026 (PDF). Source for the 100m-token attack chain, the $5k to $10k frontier cost range, & the 32-of-32 cyber-range takeover by Claude Mythos Preview & GPT-5.5.↩︎↩︎↩︎
4. UK AI Security Institute,How fast is autonomous AI cyber capability advancing?, May 13, 2026, &Our evaluation of Claude Mythos Preview’s cyber capabilities, April 13, 2026 (32-step simulated corporate network across 4 subnets & ~20 hosts, estimated at 20 human expert hours).↩︎
5. Anthropic,GLM-5.3 & the spread of advanced cyber capabilities, September 29, 2026 (GLM-5.3 builds end-to-end Chrome V8 exploits on ExploitBench in 50 of 410 attempts versus 56 of 410 for Claude Mythos Preview) ; Jaeho Lee & Alexander Barry,Open-weight AI models are 6-7 months behind on cyber, Epoch AI, October 16, 2026 (release dates & Cyber ECI scores : Claude Mythos Preview [April 7, 2026, ECI 164.8], Claude Mythos 5 [June 9, 2026, ECI 168.3], Claude Opus 5 [July 24, 2026, ECI 167.5], Zhipu GLM-5.3 [August 14, 2026, ECI 160.1]) ;Artificial Analysis : Claude Opus 5.5 vs GLM-5.3&Anthropic API Pricing. Calculation : for a 100m-token break-in at the Artificial Analysis 7:2:1 cached-input / uncached-input / output agentic ratio, Claude Mythos 5 ($10/$50/$1 per MTok) = $770 ; Claude Opus 5 ($5/$25/$0.50 per MTok) = $385 ; Zhipu GLM-5.3 ($0.902/MTok blended on Z.ai) = $90.20 (1/55th to 1/111th of BIS’s $5k–$10k April Mythos Preview range).↩︎
6. Alexej Pikovsky,AI SOC Economics : Costs, Pricing Models, & Who Keeps the Savings, July 11, 2026 (updated September 15, 2026), & Edward Wu onCloud Security Podcast : The Truth About Agentic AI in the SOC, July 29, 2025 (100+ language-model calls per alert investigation, ~20k to 50k tokens or ~$2 of compute per alert).↩︎
7. Vivekananda Allam et al.,Tipping the Scales : How AI Shapes the Offense-Defense Balance in Cyberspace, Center for a New American Security, September 23, 2025.↩︎
8. Defending Against AI-Powered Attackers : Office Hours with Sunil Agrawal, CISO at Glean, tomtunguz.com.↩︎
9. CrowdStrike 2026 Global Threat Report, as cited in Cloud Security Alliance,AI-Induced Lateral Movement & Non-Human Identity Risk, March 9, 2026 : average eCrime breakout time of 29 minutes, with a fastest recorded breakout of 27 seconds.↩︎
10. Cloud Security Alliance,Hugging Face Breach : Anatomy of a Rogue AI Agent Swarm(~700 active agents out of ~1,200 exchanging 70,000+ messages across July 9–13, 2026, logging ~17,600 actions & harvesting 136 production secrets), & Cogent Research,Beyond the Human Horizon : Q4 2026 Threat Report(across 50+ Fortune 1000 enterprises, 34 of 45 new monthly crown-jewel attack paths [76%, up 386% year over year] are viable only for parallel AI agent swarms).↩︎
11. Beyond Automation at OpenAI : Office Hours with Arvind KC, tomtunguz.com (span of control shifting from 7 people to 100 to 1,000 agents), &Semperis : Security in the AI Era(Microsoft estimate of 10 non-human identities per human trending toward 100 to 1).↩︎
12. Rubrik Zero Labs & KPMG,Invisible Access, Visible Risk, December 2025 : non-human identities & autonomous agents outnumber human users by 82 to 1 in enterprise environments.↩︎

The Third Product-Market Fit in AI, tomtunguz.com.↩︎↩︎

“Nobody’s Ready” : AI-Found Bugs Spark Corporate Security Spending Spree, The Information.↩︎

Iñaki Aldasoro, Raphael Auer, Jon Frost, & Fernando Pérez-Cruz,BIS Bulletin No. 129 : A Mythos moment? Frontier AI & cyber risk, Bank for International Settlements, July 20, 2026 (PDF). Source for the 100m-token attack chain, the $5k to $10k frontier cost range, & the 32-of-32 cyber-range takeover by Claude Mythos Preview & GPT-5.5.↩︎↩︎↩︎

[翻译失败，原文如下]

UK AI Security Institute,How fast is autonomous AI cyber capability advancing?, May 13, 2026, &Our evaluation of Claude Mythos Preview’s cyber capabilities, April 13, 2026 (32-step simulated corporate network across 4 subnets & ~20 hosts, estimated at 20 human expert hours).↩︎

Anthropic,GLM-5.3 & the spread of advanced cyber capabilities, September 29, 2026 (GLM-5.3 builds end-to-end Chrome V8 exploits on ExploitBench in 50 of 410 attempts versus 56 of 410 for Claude Mythos Preview) ; Jaeho Lee & Alexander Barry,Open-weight AI models are 6-7 months behind on cyber, Epoch AI, October 16, 2026 (release dates & Cyber ECI scores : Claude Mythos Preview [April 7, 2026, ECI 164.8], Claude Mythos 5 [June 9, 2026, ECI 168.3], Claude Opus 5 [July 24, 2026, ECI 167.5], Zhipu GLM-5.3 [August 14, 2026, ECI 160.1]) ;Artificial Analysis : Claude Opus 5.5 vs GLM-5.3&Anthropic API Pricing. Calculation : for a 100m-token break-in at the Artificial Analysis 7:2:1 cached-input / uncached-input / output agentic ratio, Claude Mythos 5 ($10/$50/$1 per MTok) = $770 ; Claude Opus 5 ($5/$25/$0.50 per MTok) = $385 ; Zhipu GLM-5.3 ($0.902/MTok blended on Z.ai) = $90.20 (1/55th to 1/111th of BIS’s $5k–$10k April Mythos Preview range).↩︎

Alexej Pikovsky,AI SOC Economics : Costs, Pricing Models, & Who Keeps the Savings, July 11, 2026 (updated September 15, 2026), & Edward Wu onCloud Security Podcast : The Truth About Agentic AI in the SOC, July 29, 2025 (100+ language-model calls per alert investigation, ~20k to 50k tokens or ~$2 of compute per alert).↩︎

Vivekananda Allam et al.,Tipping the Scales : How AI Shapes the Offense-Defense Balance in Cyberspace, Center for a New American Security, September 23, 2025.↩︎

Defending Against AI-Powered Attackers : Office Hours with Sunil Agrawal, CISO at Glean, tomtunguz.com.↩︎

CrowdStrike 2026 Global Threat Report, as cited in Cloud Security Alliance,AI-Induced Lateral Movement & Non-Human Identity Risk, March 9, 2026 : average eCrime breakout time of 29 minutes, with a fastest recorded breakout of 27 seconds.↩︎

Cloud Security Alliance,Hugging Face Breach : Anatomy of a Rogue AI Agent Swarm(~700 active agents out of ~1,200 exchanging 70,000+ messages across July 9–13, 2026, logging ~17,600 actions & harvesting 136 production secrets), & Cogent Research,Beyond the Human Horizon : Q4 2026 Threat Report(across 50+ Fortune 1000 enterprises, 34 of 45 new monthly crown-jewel attack paths [76%, up 386% year over year] are viable only for parallel AI agent swarms).↩︎

Beyond Automation at OpenAI : Office Hours with Arvind KC, tomtunguz.com (span of control shifting from 7 people to 100 to 1,000 agents), &Semperis : Security in the AI Era(Microsoft estimate of 10 non-human identities per human trending toward 100 to 1).↩︎

Rubrik Zero Labs & KPMG,Invisible Access, Visible Risk, December 2025 : non-human identities & autonomous agents outnumber human users by 82 to 1 in enterprise environments.↩︎

---

> 本文由AI自动翻译，原文链接：[A $90 Key into Your Company's Secrets](https://tomtunguz.com/a-90-dollar-key-into-your-companys-secrets/)
> 
> 翻译时间：2026-11-10 09:31
