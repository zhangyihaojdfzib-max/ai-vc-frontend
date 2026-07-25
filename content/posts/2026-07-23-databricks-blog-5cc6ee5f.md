---
title: Introducing AI spend controls with Unity AI Gateway
title_original: Introducing AI spend controls with Unity AI Gateway
date: '2026-07-23'
source: Databricks Blog
source_url: https://www.databricks.com/blog/introducing-ai-spend-controls-unity-ai-gateway
author: ''
summary: '[翻译失败，原文如下]


  • AI workloads create new cost management challenges, such as runaway retry loops
  to uncontrolled agent experimentation, making tradition...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-07-25T05:00:50.549879'
---

[翻译失败，原文如下]

• AI workloads create new cost management challenges, such as runaway retry loops to uncontrolled agent experimentation, making traditional cloud budget controls insufficient for modern AI adoption• Unity AI Gateway AI Spend Controls introduce proactive budget alerts across users, workspaces, use cases, and entire accounts, helping organizations monitor and contain AI costs before they become business risks• Combined with Unity Catalog system tables and Databricks budgets, Unity AI Gateway provides unified governance for AI usage, cost visibility, and operational accountability across models, agents, MCPs, and providers

Today, we're announcingAI Spend Controls in Unity AI Gateway. This release extends Unity AI Gateway's existing cost visibility withproactive budget alertsto give you full control over your organization's AI spend across all your models - from the coding agents your developers use every day, to the production agents serving your customers, to the batch jobs running overnight:

![](/images/posts/bb690414c6f9.png)

AI workloads deliver disproportionate value - but their cost profile is fundamentally more challenging to manage than your traditional cloud spend:

- Your nightly batch job translating call transcripts may run perfectly for a month, then start failing halfway through and trigger retry logic that multiplies its cost 10x overnight.
- Your engineering org's coding agents save thousands of developer hours a week - but the same agents make it easy for one engineer to kick off an accidental multi-agent experiment Friday night that burns through the team's monthly budget by Sunday.
- And with AI leaderboards popping up across orgs, "tokenmaxxing" is encouraging engineers to burn through tokens to top the charts. What’s impressive on the leaderboard is less so on the invoice.

Employees across engineering, support, sales, and ops are onboarding to AI faster than any technology in the last decade, unlocking net-new use cases week over week. But that adoption brings a management challenge: foundation model usage now spans dozens of teams, hundreds of users, and thousands of agents with a shifting mix of providers and model tiers. Spend controls need to apply uniformly across all AI workloads, so your organization can confidently lean into AI without worrying about surprises on the bill.

## Configure Budget Alerts at Every Granularity

While spend controls need to apply uniformly, different parts of your organization need different cost controls. A platform team cares about workspace-wide totals. A FinOps lead cares about the org-level monthly burn. An engineering manager cares about per-developer experimentation budgets. AI Spend Controls let you set them all from one place and is deeply integrated withDatabricks’ existing budgets:

- Per user:Set budgets for individual experimentation — for example, $2000 per user per month for the engineering org. Catch the developer whose agent is stuck in a loop before it shows up on the P&L.
- Per use case:Get alerted if your organizations’ spend on coding agents like codex or claude code exceeds $1000 per user per month
- Per workspace:Hold each unit to its own budget. Production gets $50,000/month; sandbox gets $5,000.
- Per account:Set a top-line ceiling — say, $200,000/month across every model, every provider, every workspace — and get alerted long before you approach it.

And when alerting isn't enough, you can enforcehard spend caps: once a budget is exceeded, Unity AI Gateway automatically stops further requests until you raise the limit or the next billing period begins.

## Get Started with Unity AI Gateway Budgets Today

To track your organization’s AI spend, follow these steps:

### Create your Unity AI Gateway Budget

- Open your account settings, navigate toUsagein the sidebar and open theBudgetstab
- Create a Budget and select “Unity AI Gateway” as the Resource type
- Optionally apply the budget only to a subset of workspaces
- Optionally apply “Resource tags” to configure budgets for a subset of your AI Gateway LLMs. Only AI Gateway LLMs whose tags match your budget tags will count towards the budget. This is useful to configure use-case specific budgets.
- Configure a “Shared threshold” that sets the monthly spend limitgloballyacross all resources in your selected workspace(s) that match the resource tags
- Configure a “Per-user threshold” that sets a monthly spend limitper user in your account
- Configure email addresses that receive alerts when the thresholds are exceeded

![](/images/posts/b468b50dbcb7.gif)

### Once created, look out for budget alerts

When one of your budgets is exceeded you will receive a notification email:

![](/images/posts/e2661763e69a.png)

### Analyze your active budgets

TheCostsection of your account console lets you respond to budget alert emails or proactively monitor the status of your live budgets. On theBudgetspage, you see at a glance how your budgets are trending:

![](/images/posts/f7ecb16aac2f.png)

Open up any budget to see how your AI spend is trending:

![](/images/posts/b25acc74b152.png)

If you configured per-user level budget thresholds, the Budget detail page will show you how your organization’s users' individual AI spend is trending. When users exceed their individual threshold, their status and spend are clearly surfaced so you can act quickly:

![](/images/posts/8625c00f5fbc.png)

To increase a budget’s threshold, you can simply edit the Budget and modify its spend limits.

### Analyze your organization’s AI Spend in detail

Unity AI Gateway Budgets give you a high-level overview of per-user and per-budget spend. To further analyze which users, models or use cases are driving your spend, you can use Unity AI Gateway’s existing cost tracking capabilities. Every request gets logged to Unity Catalog system tables with DBU costs and not just token counts. Provisioned throughput, uptime, pay-per-token usage, and even the token costs of external model providers are all automatically calculated. You can slice the data however your organization tracks spend:

- Identity:Aggregate by user or service principal — map spend to the people and systems driving it.
- Workspace, endpoint and tags:Group by team, environment, or cost center.
- Model and provider:See which models (Opus vs. Sonnet) and providers (Anthropic vs. OpenAI vs. open source) are driving costs.
- Request tags:Dynamic attribution for SaaS platforms proxying to end customers.

Access the Cost Analytics dashboard by navigating to the Unity AI Gateway page in your Databricks workspace and click on “View Dashboard”:

![](/images/posts/de9654b59263.png)

This opens up a usage & cost analytics dashboard that you can fully customize:

![](/images/posts/76bdbf6e2304.png)

## One platform to govern data and AI

AI Spend Controls are a natural extension of the governance capabilities you already use in Databricks:

- Unity AI Gatewayis your organization’s central AI Gateway to manage and access LLMs and MCPs.
- Unity Catalogis your central catalog to register and discover your organization’s data and AI assets. Access permissions, audit logs and usage data all live in Unity Catalog.
- Databricks budgetsprovide the foundation for cost monitoring and alerting. With this release,Databricks budgetsnow allow you to configure AI-tailored budgets for your organization’s AI workloads.

Databricks provides you with a single, consistent system for governing what your agents can do, who they can do it for, and how much they can spend doing it.Get started today!

---

> 本文由AI自动翻译，原文链接：[Introducing AI spend controls with Unity AI Gateway](https://www.databricks.com/blog/introducing-ai-spend-controls-unity-ai-gateway)
> 
> 翻译时间：2026-07-25 05:00
