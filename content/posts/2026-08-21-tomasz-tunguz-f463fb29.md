---
title: Mainframes became personal. So will your data center.
title_original: Mainframes became personal. So will your data center.
date: '2026-08-21'
source: Tomasz Tunguz
source_url: https://tomtunguz.com/intelligence-per-watt/
author: ''
summary: '[翻译失败，原文如下]


  In short :Local models now answer 89% of everyday chat & reasoning queries as well
  as frontier models, & their efficiency per watt has im...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-31T07:58:35.288598'
---

[翻译失败，原文如下]

In short :Local models now answer 89% of everyday chat & reasoning queries as well as frontier models, & their efficiency per watt has improved 5.3x in two years.

Local AI models can already answer 89% of everyday chat & reasoning queries as well as a frontier cloud model, a result that holds broadly across more than a million real queries & 20+ local models tested.1

That means we’re generating more intelligence per watt of electricity : more work from the same number of electrons.1

Tracking computing efficiency over time is not new. Koomey’s law found that computing power per watt doubled roughly every 1.5 years for decades, a trend that shrank the power of a mainframe into a laptop’s chassis.23

Just as performance-per-watt guided the mainframe-to-PC transition, intelligence-per-watt will guide AI’s transition to the edge.

— Jon Saad-Falcon, Avanika Narayan, et al., “Intelligence per Watt”

GPUs follow a more languid curve today, doubling efficiency roughly every 2.7 years over the last 15 years, not every 1.5 years.4

The impact is no less impressive : the best local model’s win/tie rate against a frontier model, rose from 23.2% in 2023 to 71.3% in 2025, adding roughly 20 percentage points a year. In 2026, a local model selected for the task by another local AI bumps that number to nearly 90%.5

Efficiency improved alongside the trend line : intelligence-per-watt rose 5.3x over the same period, split into a 3.1x gain from better models & a 1.7x gain from better chips. Computers are faster, models are smarter. And the end user benefits.

![Local models match cloud models on 71.3% of queries in 2025, up from 23.2% in 2023; a 2026 bar shows the ensemble-routed ceiling of 89%, a different metric than the single-model trend](/images/posts/c839686c68ac.jpg)

Cloud remains essential for long multi-step reasoning, the hardest technical domains, & workloads where scale & parallelization matter. Cloud hardware still holds an edge over local hardware in many use cases. Cloud inference delivers a 40% energy efficiency gain relative to local models.6Datacenters batch queries, a trick local hardware serving one user at a time cannot use, yet.

![Local AI efficiency improved 18x in 16 months, split between gains from better accelerators and better models](/images/posts/c5a1e9eebf14.jpg)

But for much of everyday knowledge work, there is no reason to send the query to the data center at all. The combination of local models plus a router is sufficient for the supermajority of work.7

It also cuts energy 80%, compute 77%, & cost 74% against an all-cloud baseline.

Mainframes became personal. So will your data center.

1. Jon Saad-Falcon, Avanika Narayan, et al., “Intelligence per Watt: Measuring Intelligence Efficiency of Local AI,” Stanford University & Together AI, November 2025.arXiv:2511.07885. See also theStanford Hazy Research overview.↩︎↩︎
2. Koomey’s law, Wikipedia.↩︎
3. Watts measure power, the rate energy is drawn, & joules measure the energy itself; Koomey’s original metric was computations per joule, but the underlying trend is the same one intelligence per watt now tracks for AI models.↩︎
4. Anson Ho, Ege Erdil & Tamay Besiroglu, “Limits to the Energy Efficiency of CMOS Microprocessors,” 2023.arXiv:2312.08595.↩︎
5. 71.3% & 89% are two different measurements from the same 2025 data, not the same number at different times. 71.3% is the best single local model’s win/tie rate against a frontier model, the trend line this chart plots (23.2% in 2023, 48.7% in 2024, 71.3% in 2025). 89% is a separate, higher ceiling: routing each query to whichever of the 20+ local models tested handles it best beats any single model by 16.3 to 28.8 percentage points. That gain is a selection effect: the paper notes local routing draws from 20+ diverse models versus three frontier cloud models, so on some benchmarks the best-of-local ensemble even surpasses best-of-cloud. More candidates to choose from, not just smarter routing, is what raises accuracy. Both figures come from the same study & neither supersedes the other.↩︎↩︎
6. Jon Saad-Falcon, Avanika Narayan, et al., “Intelligence per Watt: Measuring Intelligence Efficiency of Local AI,” Stanford University & Together AI, November 2025. Cloud accelerators deliver at least 1.4x higher intelligence-per-watt than local chips running the same models, roughly a 40% efficiency premium.arXiv:2511.07885.↩︎
7. Most AI Work Can Wait, tomtunguz.com.↩︎

Jon Saad-Falcon, Avanika Narayan, et al., “Intelligence per Watt: Measuring Intelligence Efficiency of Local AI,” Stanford University & Together AI, November 2025.arXiv:2511.07885. See also theStanford Hazy Research overview.↩︎↩︎

Koomey’s law, Wikipedia.↩︎

Watts measure power, the rate energy is drawn, & joules measure the energy itself; Koomey’s original metric was computations per joule, but the underlying trend is the same one intelligence per watt now tracks for AI models.↩︎

Anson Ho, Ege Erdil & Tamay Besiroglu, “Limits to the Energy Efficiency of CMOS Microprocessors,” 2023.arXiv:2312.08595.↩︎

71.3% & 89% are two different measurements from the same 2025 data, not the same number at different times. 71.3% is the best single local model’s win/tie rate against a frontier model, the trend line this chart plots (23.2% in 2023, 48.7% in 2024, 71.3% in 2025). 89% is a separate, higher ceiling: routing each query to whichever of the 20+ local models tested handles it best beats any single model by 16.3 to 28.8 percentage points. That gain is a selection effect: the paper notes local routing draws from 20+ diverse models versus three frontier cloud models, so on some benchmarks the best-of-local ensemble even surpasses best-of-cloud. More candidates to choose from, not just smarter routing, is what raises accuracy. Both figures come from the same study & neither supersedes the other.↩︎↩︎

Jon Saad-Falcon, Avanika Narayan, et al., “Intelligence per Watt: Measuring Intelligence Efficiency of Local AI,” Stanford University & Together AI, November 2025. Cloud accelerators deliver at least 1.4x higher intelligence-per-watt than local chips running the same models, roughly a 40% efficiency premium.arXiv:2511.07885.↩︎

Most AI Work Can Wait, tomtunguz.com.↩︎

---

> 本文由AI自动翻译，原文链接：[Mainframes became personal. So will your data center.](https://tomtunguz.com/intelligence-per-watt/)
> 
> 翻译时间：2026-08-31 07:58
