---
title: The AI Bullwhip
title_original: The AI Bullwhip
date: '2026-08-23'
source: Tomasz Tunguz
source_url: https://www.tomtunguz.com/the-ai-cost-stack/
author: ''
summary: '[翻译失败，原文如下]


  In short :AI hardware bottlenecks cascade in sequential multi-year waves from GPUs
  to memory, SSDs, CPUs, HDDs, and physical data center ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T02:58:58.433791'
---

[翻译失败，原文如下]

In short :AI hardware bottlenecks cascade in sequential multi-year waves from GPUs to memory, SSDs, CPUs, HDDs, and physical data center shells, driving facility buildout costs to $20b per gigawatt through the classic Bullwhip Effect.

The popular narrative of AI infrastructure is a tidy relay race : first GPUs were scarce, then memory choked throughput, then CPUs took the strain, & finally storage started to bite.

The pricing data says the relay is real but slow. Some components plunged before they surged. Each bottleneck freezes the next component’s supply chain, but the lag runs in years, & every wave locks in a higher baseline cost.

![The AI Hardware Bottleneck Is Cascading in Sequence](/images/posts/a663dfedbffd.jpg)

The initial shock in early 2023 belonged to the GPU. When ChatGPT launched, buyers concentrated capital on procuring GPUs, sending on-demand Nvidia H100 rental rates past $9 an hour.1

That monomania starved conventional computing. Server unit shipments fell 22% in 2023 to below 2018 levels as buyers deferred refresh cycles to fund GPUs.2Memory makers, already reeling from a post-pandemic glut that cost the industry more than $20b & forced wafer cuts of up to 40%, lost the server demand that would have absorbed their inventory.3

Eighteen months later, the pressure migrated to memory. To escape that slump & chase AI margins, manufacturers converted cleanrooms & lithography tools toward High Bandwidth Memory (HBM).

HBM consumes roughly three times the wafer capacity per gigabyte of standard DDR5, so every bit of HBM output removes about three bits of conventional supply. Enterprise solid state drive (SSD) contract prices rose 80% in a single quarter, while Micron reported dynamic random-access memory (DRAM) prices climbing in the low-60s percentage range quarter over quarter.4

![An editorial line illustration of four cascading ocean waves rolling in succession, symbolizing the sequential multi-year waves of AI hardware shortages](/images/posts/cba772d6b305.jpg)

By late 2025, agents squeezed server CPUs. Training clusters ran one central processing unit (CPU) to eight GPUs. Agentic workflows invert that : autonomous systems spend their cycles compiling code, calling tools, & managing state, pushing the ratio toward 1:1.5Intel reported server CPU average selling prices (ASPs) rose 27% year over year against falling unit volumes, citing billions in unmet Xeon demand.6

By 2026, the shortage reached bulk storage. Priced out of high-speed flash at $150 per terabyte, cloud architects retreated down the technology ladder into traditional, slower hard disk drives (HDDs) for bulk training data lakes. Western Digital & Seagate confirmed their entire 2026 nearline production is sold out.7

![The Indexed Cost of Data Center Buildouts](/images/posts/75a8a0948417.jpg)

Beyond the server chassis, the story is unambiguous. The fastest-rising cost is the data center’s concrete floor & the reinforced walls.

Data centers now cost upwards of $20b per gigawatt ($20b/GW), with electrical systems consuming half the budget.8Construction costs have tripled to $1,033 per square foot,9excluding land. Outside, generator step-up (GSU) transformers average nearly three year lead times, while GE Vernova & Siemens Energy have sold out turbine production through 2029, with order books stretching to 2031.10

As Barry Powell of Siemens observed of the double bind :

“You’re damned if you do, damned if you don’t: If you don’t build enough, then you’re going to get dinged for losing some market share. And if you build too much, you’re going to get dinged for fixed costs. We understand at some point there could be a bubble and we’re racing to pay back the investments as quickly as possible.”11

This is the Bullwhip Effect in physical hardware.12When a value chain suffers from multi-year manufacturing latency, sudden demand shocks downstream amplify into massive, lagged overreactions upstream. Relieving pressure at one bottleneck pushes it into the next component with a predictable delay. When the wave finally breaks, long-lead-time capital goods are the ones left exposed to overcapacity.

Over $2b in domestic transformer expansions, next-generation 300-layer NAND fabs, & new turbine production lines will deliver in 2027 & 2028. If end-user software revenues do not keep pace with $20b per gigawatt facilities, capital expenditure will face a classic crack of the whip.

1. Silicon Data H100 & B200 GPU Rental Price Indices (2026) & NVIDIA hardware disclosures.↩︎
2. Omdia Data Center Server Tracker, December 2023. 2023 server shipments fell 22% year over year to under 11m units, 5% below 2018 levels.↩︎
3. Samsung Electronics FY2023 results (14.88tn won semiconductor division operating loss), SK hynix FY2023 results (7.73tn won operating loss), Micron Technology FY2023 Form 10-K ($5.83b net loss), & Western Digital FY2023 results ($1.7b loss).↩︎
4. TrendForce, “AI Agent Boom Triggers Enterprise SSD Supply Crunch,” June 11, 2026 ; Micron Technology, Form 10-Q for the quarterly period ended May 28, 2026, Results of Operations.↩︎
5. Intel Corporation (Lip-Bu Tan) & AMD (Lisa Su) Q1 2026 Earnings Disclosures.↩︎
6. Intel Corporation SEC Form 10-Q for the quarterly period ended March 28, 2026.↩︎
7. Western Digital & Seagate Technology Q4 2025 / Q1 2026 Earnings Calls.↩︎
8. iRecruit & Data Center Construction Cost Benchmark Reports (2026). High-density AI facility cost analysis ($20m/MW or $20b/GW).↩︎
9. U.S. Census Bureau & RSMeans Construction Cost Indices for specialized mission-critical facilities.↩︎
10. Wood Mackenzie, POWER Magazine, & CNBC GE Vernova turbine backlog disclosures.↩︎
11. Brooke Sutherland, “AI Jitters Have Suppliers Preparing for Data Center Boom to Go Bust,” Bloomberg Industrial Strength, August 21, 2026.↩︎
12. Tomasz Tunguz, “Bullwhip and Base Rates — The Two Major Forces Impacting Startups,”tomtunguz.com, April 2020. See also“How to Create Competitive Advantage with Proxy Metrics”.↩︎

Silicon Data H100 & B200 GPU Rental Price Indices (2026) & NVIDIA hardware disclosures.↩︎

Omdia Data Center Server Tracker, December 2023. 2023 server shipments fell 22% year over year to under 11m units, 5% below 2018 levels.↩︎

Samsung Electronics FY2023 results (14.88tn won semiconductor division operating loss), SK hynix FY2023 results (7.73tn won operating loss), Micron Technology FY2023 Form 10-K ($5.83b net loss), & Western Digital FY2023 results ($1.7b loss).↩︎

TrendForce, “AI Agent Boom Triggers Enterprise SSD Supply Crunch,” June 11, 2026 ; Micron Technology, Form 10-Q for the quarterly period ended May 28, 2026, Results of Operations.↩︎

Intel Corporation (Lip-Bu Tan) & AMD (Lisa Su) Q1 2026 Earnings Disclosures.↩︎

Intel Corporation SEC Form 10-Q for the quarterly period ended March 28, 2026.↩︎

Western Digital & Seagate Technology Q4 2025 / Q1 2026 Earnings Calls.↩︎

iRecruit & Data Center Construction Cost Benchmark Reports (2026). High-density AI facility cost analysis ($20m/MW or $20b/GW).↩︎

U.S. Census Bureau & RSMeans Construction Cost Indices for specialized mission-critical facilities.↩︎

Wood Mackenzie, POWER Magazine, & CNBC GE Vernova turbine backlog disclosures.↩︎

Brooke Sutherland, “AI Jitters Have Suppliers Preparing for Data Center Boom to Go Bust,” Bloomberg Industrial Strength, August 21, 2026.↩︎

Tomasz Tunguz, “Bullwhip and Base Rates — The Two Major Forces Impacting Startups,”tomtunguz.com, April 2020. See also“How to Create Competitive Advantage with Proxy Metrics”.↩︎

---

> 本文由AI自动翻译，原文链接：[The AI Bullwhip](https://www.tomtunguz.com/the-ai-cost-stack/)
> 
> 翻译时间：2026-08-26 02:58
