---
title: Unify your marketing data with Lakeflow Connect
title_original: Unify your marketing data with Lakeflow Connect
date: '2026-09-11'
source: Databricks Blog
source_url: https://www.databricks.com/blog/unify-your-marketing-data-lakeflow-connect
author: ''
summary: '[翻译失败，原文如下]


  - Marketing is one of the most fragmented data stacks in the enterprise, traditionally
  requiring a custom API integration for every CRM, ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-17T07:00:29.670487'
---

[翻译失败，原文如下]

- Marketing is one of the most fragmented data stacks in the enterprise, traditionally requiring a custom API integration for every CRM, ad, and analytics source.
- Lakeflow Connect provides native, fully managed connectors for Salesforce, Salesforce Marketing Cloud, HubSpot, Dynamics 365, Google Ads, Meta Ads, TikTok Ads, Reddit Ads, LinkedIn Ads, Google Analytics, Google Search Console, Marketo, SendGrid, Amplitude, Zendesk Support, and Pendo that land governed data directly in Unity Catalog, with no infrastructure to manage.
- With the Ad-Genie solution accelerator, you can go from raw ad data to a governed customer 360 and a natural-language Genie agent in just 3 steps.

This is the first post in a new series exploring howLakeflow Connectbrings fully managed data ingestion to every line of business. Each post focuses on a specific domain, showing you how to unify scattered data sources with native connectors and activate that foundation for downstream workloads — from reporting dashboards to conversational analytics withDatabricks Genie. We are kicking things off with the most notoriously fragmented stack of all: Customer 360.

## One platform, any source

![Screenshot of Lakeflow Connect UI](/images/posts/c353f581bd05.png)

Lakeflow Connectprovides a comprehensive suite of fully managed native connectors across SaaS applications, databases, and file sources that ingest your data directly into theDatabricks Platform. Each connector can be set up via a point-and-click UI or a simple API. From there, your data is incrementally ingested as governed, managed tables inUnity Catalog, with no infrastructure for you to provision, manage, or scale.

![Any Saas or database source, one platform](/images/posts/26bb4f209666.png)

Prioritized by customer demand, Lakeflow Connect’s ingestion connectors span every line of business, including Productivity, Operations, Finance, and — perhaps the most fragmented of them all — Customer 360.

## Craft a complete customer 360 with Lakeflow Connect

The modern marketing stack is a sprawl of ad platforms, analytics tools, and CRMs, each capturing only a slice of the customer. Painting a full picture has historically required a patchwork of custom ingestion pipelines and brittle scripts that data teams must both build and maintain. This drains engineering resources and slows down marketing analysts, who need answers fast: which campaigns actually drive retention? Which customers are about to churn?

Lakeflow Connect resolves this by providing built-in connectors to ingest seamlessly from every stage of the customer journey:

- ACQUISITION:How do customers find you?Google Analytics,Meta Ads,TikTok Ads,Reddit Ads,LinkedIn Ads,Google Ads, andGoogle Search Console
- ENGAGEMENT:How do you engage with your customers?Salesforce Marketing Cloud,SendGrid, andMarketo
- RELATIONSHIP:Who are your customers?Salesforce,HubSpot, andDynamics 365
- EXPERIENCE:How do customers experience your product?Zendesk Support,Amplitude, andPendo

![](/images/posts/bc940a9894b6.png)

With this breadth of martech connectors, Lakeflow Connect becomes the critical ingestion engine that powers a complete customer 360, without the integration bottlenecks that traditionally slow teams down.

For example, EcoVadis, a globally trusted provider of business sustainability ratings and supply chain intelligence, uses Lakeflow Connect to ingest its marketing and CRM data quickly and reliably.

Another Databricks customer, iManage, a leading cloud-based knowledge work platform for legal and professional services, is also using Lakeflow Connect to reduce data engineering overhead and accelerate their ingestion pipelines.

## Cross-channel ad reports out of the box

Ad reports sit at the heart of marketing analytics, and our ad connectors provide them out of the box. The Lakeflow Connect Google Ads, Meta Ads, TikTok Ads, Reddit Ads, and LinkedIn Ads connectors deliver report tables with spend, impressions, clicks, and conversions, already aggregated and ready to analyze. Each report lands as its own governed Delta table and refreshes incrementally. The ad connectors support two types of reports:

- Pre-built reports:These cover the most common analytics needs with no configuration needed. For example, the TikTok Ads connector offers a ready-madecampaign_report_dailyreport for daily campaign performance, or acampaign_age_gender_reportreport to split those metrics by audience.
- Custom reports:These let analysts tailor the exact level, dimensions, breakdowns, and metrics of a report, for more specialized needs. For example, the Meta Ads connector allows an analyst to set the attribution window and timeframe so the data matches how they measure performance.

Today, the Meta Ads, Google Ads, and TikTok Ads connectors also support a managed authentication flow that streamlines setup to just an OAuth sign-in. From there, every report lands as a consistent, governed Unity Catalog table, ready for downstream analysis. To keep things cleanly organized, you can route each ad account's tables to its own destination schema — this is already possible via API, with UI support rolling out soon.

The Krazy Coupon Lady, a leading shopping intelligence company that helps millions of consumers find the best deals, relies on Lakeflow Connect’s Meta Ads and Salesforce connectors to streamline its marketing data pipelines.

## One data foundation, every analytics answer

Once campaign spend, CRM activity, and product behavior sit in the same governed tables, that unified data becomes the foundation for downstream analytics. Business stakeholders can buildAI/BI dashboardson it, or askGeniequestions in natural language and get instant, reliable answers.

Our newAd-Genie solution acceleratormakes this even easier for Lakeflow Connect’s ad connectors: it refines the ingested bronze tables into silver and gold tables that power an out-of-the-box AI/BI dashboard and Genie agent, all backed by governedmetric views in Unity Catalog. To learn more about how to set up this accelerator and optimize your ad spend, check out our step-by-step guide in this Databricks community blog,Tutorial: Transform your Lakeflow Connect ad data into visual and conversational analytics.

Lakeflow Connect is launching new connectors across every line of business, with support for even more Customer 360 sources like Adobe Campaign and Adobe Analytics! TryLakeflow Connect for freenow and deploy theAd-Genie solution accelerator.

Watch for the next post in this Lakeflow Connect blog series to keep learning how to bring all your enterprise data into Databricks and give your AI agents the full context they need.

---

> 本文由AI自动翻译，原文链接：[Unify your marketing data with Lakeflow Connect](https://www.databricks.com/blog/unify-your-marketing-data-lakeflow-connect)
> 
> 翻译时间：2026-09-17 07:00
