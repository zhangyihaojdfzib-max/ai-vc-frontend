---
title: 'Introducing Governance Hub: Intelligent, account-level governance over your
  Databricks estate'
title_original: 'Introducing Governance Hub: Intelligent, account-level governance
  over your Databricks estate'
date: '2026-08-26'
source: Databricks Blog
source_url: https://www.databricks.com/blog/introducing-governance-hub-intelligent-account-level-governance-over-your-databricks-estate
author: ''
summary: '[翻译失败，原文如下]


  - Governance Hub provides a unified, account-level view of data governance, AI usage,
  and cost across your entire Databricks estate

  - Eac...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T03:00:37.481296'
---

[翻译失败，原文如下]

- Governance Hub provides a unified, account-level view of data governance, AI usage, and cost across your entire Databricks estate
- Each vertical surfaces high-level KPIs and detailed drill-downs, so teams can assess governance health and act, without building custom dashboards
- Genie delivers deep agentic insights into governance health, anomalies, gaps, enriched with contextual knowledge of your assets and workloads

Your FinOps lead needs to easily drill-down into Databricks spend and identify what’s driving costs, without maintaining dozens of queries and dashboards. Your data governance team built their own tools to track classification coverage, and they're already stale. Your AI deployment team needs to understand what models and agents are being used by developers.

These are the conversations we heard again and again from customers. The teams responsible for governing the Databricks estate across 100s of workspaces over multiple regions often can't access the insights they need. And when they can, the data is scattered across system tables, workspace-level views, and third-party tools. This is whereGovernance Hubcomes in. It's a centralized, account-level view of data health, AI usage, and cost, with prioritized recommendations, across AWS, Azure, and GCP. Now available in Beta.

![image5.png](/images/posts/a15ec4659ff9.png)

Built for the teams who need it most.Governance Hub is designed for platform and governance teams who are responsible for governance across their domain, giving them the ability to drill into what matters without being constrained by a single workspace. It also supports administrators who need to oversee the account, delegate, and keep the organization compliant without becoming the bottleneck.

## Spot the metadata gaps hiding across your estate

Before Governance Hub, knowing which tables were missing tags, ownership, or documentation meant querying system tables yourself, or finding out the hard way when an audit or access request stalled. Now, the Data page shows you at a glance: how many assets you have, what percentage are tagged, owned, and classified, and which ones are falling behind. The real power is in the drill-downs. Click into asset inventory to see exactly which tables and schemas are missing required tags or descriptions, and where to start closing the gap. Click into data quality to surface unhealthy or undocumented metastores. Manage governed tags: create policies, edit values, grant permissions, all without leaving the page.

![image1.png](/images/posts/ce2bac08e9e5.png)

## View Access Insights by Principal

Answering "What can this user actually query?" used to mean unioning data from a dozen sources, manually resolving group memberships, and tracing ownership across individual securables. As your account grows, this question becomes both much more difficult to answer, and much more important.

Access Insights replaces that with a single principal-centric view. Select any user, group, or service principal to see everything they can access across your account, including direct grants, inherited access through group membership, and objects they own.

Filter by catalog or privilege to answer real questions in seconds: debug why an end user can or cannot access a table, review a group's access before onboarding a vendor, audit what a service principal can access, or identify everything a departing employee owns before offboarding.

Access insights in the Governance Hub helps you answer these questions and more through a single surface.

## Catch AI cost surprises early

AI adoption is accelerating and so is the question of how it’s actually being used across the organization.Unity AI Gatewayprovides a singular governance pane for managing usage, access, and cost across models, agents, tools, MCPs. Whether your organization is using Databricks-hosted models, or externally-hosted models, the AI Gateway provides unified governance across all your AI traffic.

The AI vertical in the Governance Hub provides detailed observability into the traffic flowing through Unity AI Gateway. The AI page tracks token consumption, model activity, per-user spend, and guardrail coverage in one place. See which models are most active, which users are driving cost, and whether your AI budgets are on track. When a user exceeds their threshold, it's surfaced immediately.

![image7.gif](/images/posts/698661e3fb6d.gif)

## Find the untagged spend you didn't know about

TheCostpage gives you your 30-day spend, month-to-date, and daily average, each compared to the prior period. But one of the most valuable insights istagged spend: what percentage of your cost is actually attributed? Click through, and Governance Hub automatically filters to untagged resources, surfacing the spend that's invisible to your chargeback and budgeting processes.

From any tile, openExplorerto slice by product, workspace, resource, or tag. Go from a high-level KPI to the specifics: the top jobs, clusters, endpoints, and warehouses in your workspace, in two clicks.

![image2.png](/images/posts/69893b0e405f.png)

## Leverage Genie for autonomous, agentic governance

Governance Hub is integrated withGenie, so you can go beyond pre-built views and static dashboards. Ask questions like"Why has there been a spike in costs”or"Show me tables with sensitive data that lack masking policies", and get answers, and recommendations, grounded in your actual governance data. No SQL required. Soon, Genie will be able to even take actions for you - configuring policies, setting up alerts, and implementing recommendations.

Genie understands the context of each vertical (Data, AI, and Cost), so whether you're investigating a spike in token usage or tracking down unclassified assets, you can get to the answer in seconds instead of writing queries.

![image8.png](/images/posts/42780510790b.png)

## Get started

An account admin can enable Governance Hub from thePreviewspage in the Account Console. Account admins get full access; workspace admins see Cost and AI for their workspaces; metastore admins see Data for their metastores. Governance Hub respects existing permissions: no new access controls to configure.

We're just getting started. Features coming soon include insights into performance, security, actionable recommendations that can be delegated, and agentic capabilities for governance at-scale.

Enable Governance Hub in your Account Console today

---

> 本文由AI自动翻译，原文链接：[Introducing Governance Hub: Intelligent, account-level governance over your Databricks estate](https://www.databricks.com/blog/introducing-governance-hub-intelligent-account-level-governance-over-your-databricks-estate)
> 
> 翻译时间：2026-08-26 03:00
