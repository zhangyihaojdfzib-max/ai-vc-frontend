---
title: AI Changed How Spotify Builds. What We Learned (and Fixed) About Quality at
  Higher Velocity | Spotify Engineering
title_original: AI Changed How Spotify Builds. What We Learned (and Fixed) About Quality
  at Higher Velocity | Spotify Engineering
date: '2026-09-16'
source: Spotify Engineering
source_url: https://engineering.atspotify.com/2026/9/ai-changed-how-spotify-builds-what-we-learned-and-fixed-about-quality-at-higher-velocity/
author: ''
summary: '[翻译失败，原文如下]


  # AI Changed How Spotify Builds. What We Learned (and Fixed) About Quality at Higher
  Velocity


  ![Feature Image](/images/posts/c1807594926...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-18T06:56:57.540808'
---

[翻译失败，原文如下]

# AI Changed How Spotify Builds. What We Learned (and Fixed) About Quality at Higher Velocity

![Feature Image](/images/posts/c18075949269.png)

Quality and reliability have always been a point of pride for Spotify. We run an extraordinarily complex ecosystem of interconnected microservices and data pipelines that all come together in a super app for777 million monthly active usersacross more than2,000 supported devices. At any given moment, our platform serves around100 million concurrent clients, processes 11-12 million backend requests per second, and runs nearly 3,000 production services. Quality at our scale has never been a solved problem. Before AI entered our workflow, a weakness anywhere in the system could reach listeners and creators quickly. Recently, though, four particular areas have tested us at once, and, what may surprise some, AI slop isn’t among those. It’s the pace of change inside Spotify and across the world that has forced us to adapt.

#### What we found and what we’ve changed

##### Content processing

Spotify processes more than 500K new songs, videos, podcasts, and audiobooks every day, and it’s growing rapidly. It's critical to the artists and creators behind this that these become available quickly and reliably.

Pre-existing to this onslaught of content upload, we already had two existing weaknesses that have impacted this process and the people dependent on them. First, processing failures could be masked. For example, a media file we could not process could sometimes fail silently and its impact on publishing go unnoticed for hours because the failure did not page anyone. Second, the pipeline did not have enough capacity for spikes in our growing video catalog processing; valid video episodes could wait in a queue unalerted when transcoding capacity was exhausted.

Ourreportdescribes what happened on June 24, where small changes related to these factors combined: a scheduled batch job was competing with new episodes, a recent quality improvement had increased the compute each episode required, and a scheduling bug reduced throughput by about 10%. Episodes that normally published within minutes were delayed for hours. The root causes were garden variety ones, and ours: subtle misses on failure alerting, challenges in capacity planning, and small gaps in workload controls.

We have since added end to end monitoring so we know of failures before creators do, fixed the scheduler, moved batch jobs to run at a lower priority, and increased capacity. We also reworked service tiering and workload prioritization so critical services and new uploads take precedence when capacity is constrained. Episodes from bad actors are suppressed and lowered in priority greatly reducing overall load and doesn’t compete with higher-priority episodes. AI helped deliver these faster, but, as was the case before we started using agents, these are problems that require distinct judgement, an end to end mindset and skills from our engineers.

##### Fleet Updates

A separate challenge is managing the growing scale of automated change. Our custom Fleet Management framework has for years made large scale changes across our fleet every day, with the vast majority merged automatically after passing safety checks. For over a year now, we have expanded this to support more complex agentic-driven changes, including a recent Java migration across backend services completed in three days. The pace has accelerated even further, shielding engineers from even more mundane tasks.

But that increased automation also creates new failure modes. This year, an automated dependency upgrade passed our checks, but still failed in production, impacting end users. We are responding by strengthening safeguards, expanding rollback capacity, and scheduling automated changes during owning teams’ working hours.

##### Compute shortages

Across the industry, the use of AI has triggered a huge spike in demand, without commensurate supply increases, on both CPUs and GPUs, reducing spare capacity. Spotify has long operated in an environment where compute capacity was generally available when we needed it. As industry demand has grown, that capacity is less predictable.When a single region fails, we shift traffic to another region to handle the load. While in one sense a regional failover is a significant event, we’ve designed this to minimize customer impact.

Earlier this year, when Spotify executed regional failovers, this lack of capacity exacerbated issues that were previously trivial and unnoticeable. In this new environment of capacity constraints, our end users noticed. This is an impact of AI to our quality of service, but an indirect one, not one that matches those commonly cited.

As a result, we have had to review our network edge and tiering approaches. Now, when we failover, we must accept that there may not be capacity for the lower tiers of services. We are also strengthening resilience across our production services. We doubled reserved edge capacity after a May incident. Today we can shift part of our internal service-mesh traffic manually; extending that control to edge traffic and testing regional spillover are still under way. The goal is to move traffic gradually while ensuring receiving regions can absorb the additional load while maintaining stability.

##### The Mobile App Experience

For over a decade we’ve seen an ebb and flow in our mobile app quality. We get intense about shipping amazing new features fast, and this can introduce trade-offs with the quality of the experience. As these new negative quality signals build, we then shift capacity and incentives toward quality. We broaden our guardrail metrics, push to recover, and get back to a good state with broader guardrails. Over time, new issues emerge outside those that existing metrics and guardrails capture, and the cycle repeats.

AI has increased the pace of change, which means this cycle moves at a higher frequency and gaps surface faster. The issue isn’t that AI-assisted code is inherently lower quality; it’s that our systems for measuring and maintaining quality need to keep pace with how quickly we can now build and ship.

Our release process already has deliberate checkpoints before production. What our recent work highlighted is that individual releases can look healthy while smaller regressions accumulate over time, affect particular phones, or sit outside the signals we are watching.  We have now broadened those quality signals and added longer-term trends to those decisions so we can identify deterioration earlier.

#### AI's role

Moving to AI-assisted development at this scale raised a fair question inside the company and outside it: what does this do to quality? Google Cloud's 2025 DORAresearchfound that AI adoption was associated with higher delivery throughput and product performance, but lower software delivery stability. But every company is different, so we decided to answer the quality question by looking at our own data.

##### What the data tells us

First and foremost, we looked at production incidents, as these are the ultimate measures of quality. Every month we run a retrospective of all major incidents. During our AI ramp-up, we began asking two additional questions: Did AI-authored code directly contribute to the incident? And did the increased volume of change put additional pressure on review, testing, rollout, or observability?

Across the incidents reviewed so far, we did not identify AI-authored code as a material direct contributor. We did, however, observe the second risk:the volume of change increased faster than some of our verification controls could adapt. In response, we are strengthening the entire delivery system, including review, testing, rollout, observability, and rollback.

[翻译失败，原文如下]

Next, looked for evidence of a quality-for-velocity trade offs further up the pipeline. We classify every merged PR by the work it contains: features, code quality and optimization, maintenance, and documentation. Total merged changes more than doubled year over year in August, from roughly 8,100 to 17,000. Quality and optimization work rose from 27% of that mix to 31%, which means engineers put more than twice as much absolute work into code quality this August as last. Feature work grew as well. Maintenance and configuration fell from 31% of the mix to 25%. The increase in both the absolute and relative time spent on code quality and optimization is one reason we believe we are not seeing a simple quality-for-velocity trade-off.

We also rebuilt our rework rate metric to separate genuine rework from new work and legacy refactoring. Code churn measures how much code gets removed relative to what gets added. Rework rate weighs the age of the code being changed, which is a better proxy for whether recent work holds up. TheFAROS 2026 reportfound a sharp industry-wide rise in code churn, but we see no corresponding rise in rework rate. That is a clear signal that we are not accumulating AI-induced quality debt.

There are two warning signals we are watching: code complexity and PR size are both creeping up. Pre-AI, those were unambiguous quality concerns. Now a larger PR may just mean a human and an agent reasoned together and delivered a bigger unit of work safely, and complexity thresholds calibrated for what one person could hold in their head may no longer apply. We don't have conviction in either hypothesis, so we are deliberately not rewriting the thresholds to make ourselves feel better. We'll continue to watch these metrics to see if they are truly leading indicators.

#### What we've learned

Earlier this year, we didn’t live up to our quality standards everywhere we’d have liked. So, we investigated and continue to remediate and improve. The causes were from the mundane to, in hindsight, the predictable, given the more rapid pace. What may surprise some, is that data does not show a distinct direct AI-authored failure signature.

AI increased the capacity to produce change. The next constraint became our ability to verify it. Keeping the delivery system aligned with that increased pace of change is now a continuous effort, automated safeguards, rollback, observability, failover, and quality measurement. The work now is to ensure those controls operate at the same pace as development.

---

> 本文由AI自动翻译，原文链接：[AI Changed How Spotify Builds. What We Learned (and Fixed) About Quality at Higher Velocity | Spotify Engineering](https://engineering.atspotify.com/2026/9/ai-changed-how-spotify-builds-what-we-learned-and-fixed-about-quality-at-higher-velocity/)
> 
> 翻译时间：2026-09-18 06:56
