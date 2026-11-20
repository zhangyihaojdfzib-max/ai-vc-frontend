---
title: Why PostgreSQL 19 shipped late
title_original: Why PostgreSQL 19 shipped late
date: '2026-11-19'
source: Databricks Blog
source_url: https://www.databricks.com/blog/why-postgresql-19-shipped-late
author: ''
summary: '[翻译失败，原文如下]


  - PostgreSQL 19 shipped about a month after the usual September to October window
  for major PostgreSQL releases. The delay came from the ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-20T09:31:27.495525'
---

[翻译失败，原文如下]

- PostgreSQL 19 shipped about a month after the usual September to October window for major PostgreSQL releases. The delay came from the project's focus on quality.
- Starting around February 2026, AI made bugs and security issues far easier to find. CVEs fixed per quarterly update release went from one to four up to 28 by August 2026, and commits back-patched to the release branch rose 61%.
- Contributors spent time fixing those bugs that would have gone into reviewing new features. The project is adapting, and AI scrutiny is a chance to make PostgreSQL better than it's ever been.

PostgreSQL 19 is nowgenerally available, and there are some really cool things in it:

- REPACK rebuilds bloated tables while normal reads and writes continue
- Query plan advice lets you stabilize the plan for a critical query without changing application SQL
- WAIT FOR LSN gives you read-your-writes on replicas without polling or arbitrary sleeps
- Logical replication can now synchronize sequences, which removes a common migration headache

We walked you through what's new on PostgreSQL 19here. In this post, we take a step back; as PostgreSQL contributors, we want to share some backstory on how a major release comes together, and some reflections on PostgreSQL 19 and what made this release different.

## How a PostgreSQL release comes together

Over the past decade, the timing of PostgreSQL major releases has become very predictable: no earlier than the middle of September, and no later than the middle of October. This year was different: PostgreSQL 19 shipped more than a month after that window closed. So, what happened?

To answer that, it helps to know what a normal year looks like.

PostgreSQL started in the 1980s as the POSTGRES project at UC Berkeley, and it has been developed in the open since 1996. No single company owns it. A worldwide community of developers builds it, and that community values reliability and predictability. Part of that predictability is the calendar: one major release a year, at about the same time each year.

Each release takes 14 to 15 months from the first commits to general availability, and that time splits into two phases:

- Development: there are five commitfests - in July, September, November, January, and March/April - each focused on reviewing and committing patches. Feature freeze follows the last one, in April.
- StabilizationBeta 1 typically ships in MayThe release branch is cut in June, around Beta 2 - this also opens up new development on the next releaseBeta 3 follows in AugustThere’s a release candidate in SeptemberGeneral availability happens late September or October

- Beta 1 typically ships in May
- The release branch is cut in June, around Beta 2 - this also opens up new development on the next release
- Beta 3 follows in August
- There’s a release candidate in September
- General availability happens late September or October

When a feature can't be stabilized in time, the usual practice is to defer it to a future major version and keep the release on schedule.

![The PostgreSQL release cycle, about 14 to 15 months in total](/images/posts/ff6a995bf341.png)

## So, what happened with PostgreSQL 19?

### LLMs got good at finding bugs

All software contains bugs, and PostgreSQL's code base is large, complex, and old. Our git history – converted from CVS – now reaches back more than 30 years, and the first code was written a decade before that. There's a huge amount of code, and that code contains a huge number of bugs.

That's always been true, and it hasn't stopped PostgreSQL from being popular or successful. What's different now is that it's become vastly easier to find those bugs. Fixing them has also gotten easier, but not to the same degree.

The change came quickly. Around February 2026, developers started noticing that the latest models were good enough to write real code, that the code going to production wasn't as buggy, and that the models were helping them move faster.

Reviewing code and researching security issues used to take a lot of human expertise. With AI, they take much less, and how much AI can discover on its own has gone up sharply.

![AI lowered the expertise needed to find bugs and security issues](/images/posts/617244e99e3e.gif)

### A flood of bug fixes

You can see the result in PostgreSQL's quarterly update releases. From August 2023 through November 2025, each one fixed between one and four CVEs. In 2026, that went to 5 in February, 11 in May, and 28 in August. Bug fixes per update release followed the same curve, from roughly 50 to 75 per release to about 140 in August 2026.

Not every CVE is equally severe though. Many of the bug fixes are long-tail issues. But the volume is still higher than we’re used to.

The commit history shows the same thing. Between April 8th, 2025 and September 25, 2025, there were 1037 commits to PostgreSQL's master branch and 724 commits to REL_18_STABLE. In 2026, during the same date range, there were 1443 commits to the master branch and 1169 commits to REL_19_STABLE. In other words, if you look at the number of commits that went into the master branch only between feature freeze and September 25th, it actually declined slightly from last year to this year, but the number of back-patched commits jumped by more than 60%.

![CVEs and bug fixes in each PostgreSQL quarterly update release, from August 2023 to August 2026](/images/posts/2ed4b036c053.gif)

![Commits to master between feature freeze and September 25. Commits back-patched to the release branch rose 61%](/images/posts/1ce26f12c700.gif)

It's possible that some of this jump is the result of committers making more mistakes this year than they did last year, but that’s unlikely. Rather, it seems likely that PostgreSQL committers were about as conservative in 2026 as they were in preceding years, but a lot more of the mistakes they made were quickly found by LLMs.

And it isn't just mistakes in the latest release. In the same time period, during 2025, there were 248 commits to REL_17_STABLE, and during 2026, there were 433 commits to REL_18_STABLE. In other words, the number of commits being back-patched not just to the release in progress but also to at least one prior release jumped by more than 74% in a single year.

![Commits back-patched to the previous release branch over the same period rose 75% in a year](/images/posts/a5d8d8efaaab.gif)

The reason for this is simply that a huge number of people on the Internet are now reporting bugs in PostgreSQL that they found using LLMs, and the PostgreSQL committers have been very busy fixing them.

### PostgreSQL developers are stretched thin

Time that would have gone into reviewing what was going into PostgreSQL 19 went into fixing security issues and other bugs in the back branches instead. A few features that were in progress this cycle weren't ready in time, so the project did what it always does and deferred them to a future release.

The fixes kept coming right up to the end. The November 12 update release for the supported branches included so many fixes that the release team put out a second release candidate so PostgreSQL 19 could ship with them.

## What next

In the end, we got PostgreSQL 19 out the door, a few weeks later than usual, and the delay came directly from the project's concern for quality. The way we all develop software has changed, and the PostgreSQL community is adapting.

Nobody knows yet exactly how open source software development will change, but contributors across the PostgreSQL project are working hard to figure it out. LLMs are going to push every PostgreSQL developer, and to some extent every software developer, to raise their game. Every feature we write from now on will be scrutinized by AI, and bugs that would have gone unnoticed forever in an earlier era will now be found, sometimes in a matter of hours.

[翻译失败，原文如下]

That's a big challenge, and an even bigger opportunity to make PostgreSQL better than it's ever been. We're excited to be part of it.

Lakebase

---

> 本文由AI自动翻译，原文链接：[Why PostgreSQL 19 shipped late](https://www.databricks.com/blog/why-postgresql-19-shipped-late)
> 
> 翻译时间：2026-11-20 09:31
