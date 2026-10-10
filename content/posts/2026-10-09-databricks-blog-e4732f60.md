---
title: How California built its Behavioral Health Public County Profile on Databricks
title_original: How California built its Behavioral Health Public County Profile on
  Databricks
date: '2026-10-09'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-california-built-its-behavioral-health-public-county-profile-databricks
author: ''
summary: '[翻译失败，原文如下]


  - California launched the Behavioral Health Public County Profile, a unified public-facing
  dashboard powered by Databricks to bring count...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-10T08:17:48.520747'
---

[翻译失败，原文如下]

- California launched the Behavioral Health Public County Profile, a unified public-facing dashboard powered by Databricks to bring county behavioral health data together into one accessible location.
- Built to support the Behavioral Health Services Act (BHSA) following Proposition 1, the dashboard resolves data fragmentation across all 58 counties, enabling transparent tracking of local funding, service delivery, and homelessness initiatives.
- The platform establishes standardized metrics, robust governance, and end-to-end data lineage across disparate county systems, creating a scalable model for data-driven government and public oversight.

The California Department of Health Care Services (DHCS) built theBehavioral Health Public County Profileon the Databricks platform, a first-of-its-kind public dashboard that brings behavioral health data from all 58 counties into one place for nearly 40 million Californians.

On October 1, 2026, Governor Gavin Newsom announced the launch of the County Profile, calling it a tool that empowers people to see how their counties plan, fund, and deliver behavioral health services and to hold government accountable for results.

## Data and accountability at your fingertips

For years, behavioral health data in California was scattered across disparate systems, difficult to access, and nearly impossible for the public to interpret. County spending plans, demographic breakdowns, homelessness and housing-related services data, and performance measures lived in silos making it hard for policymakers, advocates, and everyday Californians to understand how their behavioral health system was actually performing.

The Behavioral Health Public County Profile changes that. It consolidates county-reported data that was previously fragmented into a single, intuitive dashboard where anyone can:

- Compare counties on behavioral health planning, funding, service delivery, and progress toward statewide goals
- Explore demographics and understand who is being served and who isn't
- Track homelessness and housing-related behavioral health services at the local level
- Review BHSA Integrated Plans - the three-year roadmaps counties are required to create under the new Behavioral Health Services Act (BHSA)
- Monitor performance measures that tie county investments to real outcomes

## From Proposition 1 to production: A data platform built for transformation

The release of the County Profile is not an isolated event; it is the culmination of a sweeping transformation in how California approaches behavioral health.

In 2024, California voters approved Proposition 1, transitioning the state from the Mental Health Services Act to the new Behavioral Health Services Act (BHSA). The BHSA fundamentally restructures how counties invest in behavioral health by tying funding to statewide goals for outcomes, equity, and transparency. On July 1, 2026, all 58 California counties officially began operating under this new framework, integrating planning across all behavioral health funding sources, targeting resources toward the highest-need populations, and explicitly including substance use disorder services and housing supports.

The County Profile is the accountability engine for this transformation. It is built on data that counties are required to report under the BHSA, making it not just a dashboard, but a mechanism for democratic oversight. Californians can now see whether their county's behavioral health investments are aligned with statewide goals and whether those investments are translating into better care.

### The Technology Behind the Transparency

Building a statewide behavioral health dashboard that serves all 58 counties — each with different data systems, reporting cadences, and population sizes — is no small technical feat. The California Department of Health Care Services (DHCS) choseDatabricksto power this initiative, leveraging its capabilities for large-scale data integration, governed analytics, and public-facing data products — all running on aFedRAMP-authorizedenvironment that meets the rigorous security and compliance standards required for government health data.

Key technical elements of the solution include:

- Unified data ingestion withSpark Declarative PipelinesandLakeflow Connect: Bringing together behavioral health data from dozens of county-level sources into a single, governed data platform using Spark Declarative Pipelines for reliable, automated ETL and Lakeflow Connect for seamless connectivity to external systems.
- Standardized metric definitions with Semantic Views:Establishing governed, consistent metrics across all 58 counties using Semantic Views to define business logic once and reuse it everywhere, so that when a Californian compares Los Angeles County to Fresno County, they are comparing apples to apples.
- Serverless Compute: Enabling DHCS teams to process and transform data at scale without managing infrastructure, reducing operational overhead and allowing engineers to focus on the data products that matter rather than managing infrastructure
- Scalable, production-grade infrastructure: Supporting both the internal analytics needs of DHCS and the public-facing County Profile application that serves millions of potential users
- Data quality and lineage: Ensuring that every number in the dashboard can be traced back to its source, with clear documentation of how it was transformed and validated
- FedRAMP-authorized security: Operating within a compliance framework that safeguards sensitive behavioral health data, meeting federal standards for confidentiality, integrity, and availability that government agencies require when handling protected health information

This is data engineering in service of public trust. When a governor quotes your dashboard in a press release, the data has to be right, it has to be secure, and the platform has to be built to ensure it stays that way as new data flows in from counties across the state.

## A model for data-driven government

California's Behavioral Health Public County Profile represents something larger than a single dashboard. It is a proof point for what happens whengovernment agencies invest in modern data platformsand treat data transparency as a core public service.

The BHSA requires counties to create Integrated Plans: three-year roadmaps for behavioral health services, programs, and investments. These plans specify how counties will use behavioral health funding to address local mental health and substance use disorder needs, improve access to care, and strengthen services across the care continuum. The County Profile makes these plans visible and comparable, creating a feedback loop between policy intent and measurable outcomes.

This approach mirrors a broader trend inpublic sector data modernization: moving from static, periodic reports to living, interactive data products that empower stakeholders at every level - from state legislators to county administrators to the families seeking care for their loved ones.

## What’s next for California’s Behavioral Health Data

The County Profile is a living tool. DHCS has indicated that additional measures will be added over time as more data becomes available and as the BHSA matures. The foundation is in place: a governed, scalable data platform that can grow with California's ambitions for behavioral health transformation.

For Databricks, this partnership with DHCS demonstrates the power of the platform in one of the most consequential domains imaginable: helping a state of nearly 40 million people build a behavioral health system grounded in data, accountability, and the belief that every person deserves access to care.

As Governor Newsom put it: Knowledge is power, and we are far from powerless.

Explore the Behavioral Health Public County Profile:county-profile.mes.dhcs.ca.gov

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[How California built its Behavioral Health Public County Profile on Databricks](https://www.databricks.com/blog/how-california-built-its-behavioral-health-public-county-profile-databricks)
> 
> 翻译时间：2026-10-10 08:17
