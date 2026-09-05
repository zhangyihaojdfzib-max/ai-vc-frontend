---
title: How the FDA is building a secure, AI-ready data foundation on Databricks for
  Government
title_original: How the FDA is building a secure, AI-ready data foundation on Databricks
  for Government
date: '2026-09-01'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-fda-building-secure-ai-ready-data-foundation-databricks-government
author: ''
summary: '[翻译失败，原文如下]


  - What it is:The FDA built HALO (Harmonized AI and Lifecycle Operations for Data),
  an enterprise-grade data platform powered by Databrick...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-05T06:35:32.218068'
---

[翻译失败，原文如下]

- What it is:The FDA built HALO (Harmonized AI and Lifecycle Operations for Data), an enterprise-grade data platform powered by Databricks on AWS GovCloud that utilizes Unity Catalog to provide a unified, secure, and governed foundation for AI and analytics.
- The challenge it solves:The agency needed to modernize its fragmented data landscape—siloed data, inconsistent pipelines, and high operational overhead—while simultaneously supporting its mission-critical regulatory work without any service disruption or downtime.
- Results and outcomes:The modernization enabled the FDA to scale to over 6,000 users, while achieving measurable operational gains, including a 30% increase in SQL query speeds, a 20% reduction in compute costs, and a 75% decrease in time spent on data provisioning and sharing.

Modernizing a federal data platform is a little like steering an aircraft carrier while rebuilding the engine mid-ocean: the mission cannot stop, even as the underlying systems are being transformed. That is the challenge the U.S. Food and Drug Administration (FDA) described in its Data + AI Summit session onHow the FDA is scaling secure AI with Databricks for Government.

For the FDA, the stakes are unusually high. One in three Americans is touched by an FDA decision every day, it regulates 20 cents of every dollar of U.S. consumer spending, and its more than 16,000 employees work across 200 offices and labs covering more than 300 product categories. In that environment, data is not a back-office function; it is a public health imperative.

That is why the conversation around AI in government is shifting. The question is no longer whether agencies should use AI, but how they can operationalize it securely in environments that demand strong governance, auditability, and compliance from day one. This blog outlines the core building blocks required to support secure, mission-critical AI workloads in FedRAMP and IL5 environments: infrastructure-as-code security patterns, governed model access, lineage and auditability, and the networking configurations needed to connect Unity Catalog to the right data sources.

## Why secure AI in government starts with platform readiness

Government agencies often operate under some of the most stringent requirements in the world.Databricks on AWS GovCloudis designed for such regulated workloads that process and analyze export-controlled data (ITAR/EAR), data that is regulated under FedRAMP High, DoD IL5, or processes other sensitive information like healthcare records and federal financial systems which cannot be handled in a standard cloud environment.

![Databricks on AWS GovCloud](/images/posts/b804e1533678.png)

But compliance alone is not the story. The bigger point is speed to value. As part of this session, Databricks highlighted a security reference architecture and Terraform-based deployment model designed to help customers stand up a hardened, production-ready, audit-ready environment quickly, with controls such asPrivateLink,customer-managed keys, and thecompliance security profilebaked in.

## The FDA’s challenge: modernize without disrupting the mission

The FDA’s modernization journey began with a familiar problem: siloed data, duplicated effort, inconsistent pipelines, and too much operational overhead spread across multiple centers and programs. Analysts and scientists were spending too much time finding and reconciling data instead of deriving insight from it. At the same time, the gap between the agency’s scientific and regulatory mission and what its infrastructure could support was widening.

The agency’s response was to buildHALO(Harmonized AI and Lifecycle Operations for Data), its enterprise data platform, as a secure, governed, AI-ready foundation. After starting its journey with Databricks in 2020 with the modernization of a legacy environment, the FDA’s move to Databricks on AWS GovCloud in 2025 unlocked the benefits of Unity Catalog and additional capabilities in the Databricks environment. Unity Catalog gave FDA a single, open governance layer for data and AI so they can securely discover, manage, and share trusted assets across regions, formats, and tools with less complexity and lower cost, while improving the time-to-insights.

The architecture the FDA adopted is multi-tenant: multiple regulatory centers share a common platform foundation while maintaining their own secured, governed spaces. In the session, FDA described it as an apartment complex model, where everyone shares the infrastructure but each tenant has its own lock and policies. With Unity Catalog, it became much easier to share data across centers without losing governance.

## Three milestones that changed the trajectory

In FDA’s journey, three milestones defined the transformation. The first wasFedRAMP Highauthorization sponsorship, which was the prerequisite that unlocked everything else. The second was the AWSGovCloudmigration. The third wasUnity Catalog, which gave the agency the governance foundation it needed for secure, scalable AI.

The scale behind those milestones is what makes the story especially compelling. The FDA migrated more than 5,000 users and more than 8,000 jobs and pipelines with zero downtime, allowing scientists and analysts to continue their work uninterrupted while the agency rebuilt the foundation underneath them. It also refactored more than 1,000 data pipelines and more than 4,000 notebooks as part of the migration to Unity Catalog.

The FDA is using Databricks serverless compute, model serving, Unity Catalog, and Genie to modernize hundreds of legacy dashboards into interactive, AI-powered experiences, eliminating technical debt and accelerating mission impact.

## The Impact - What modernization delivered in practice

For the FDA, this was not just an infrastructure cleanup. It was a measurable operating shift. The agency said that, in just a few months, it onboarded eight centers and 30 programs onto its enterprise data platform and consolidated more than 40 data sources spanning application and submission systems. That consolidation improved collaboration across the agency, increased transparency, and strengthened its security posture.

It also produced quantifiable operational gains. According to the FDA, SQL warehouses improved query response times by more than 30% for BI workloads, compute costs fell by more than 20%, time spent on provisioning, permissioning, and data sharing dropped by more than 75%, and operational overhead declined by more than 35%.

User adoption tells the same story. The FDA started with roughly 500 users in 2020, has now grown to more than 6,000 users on the platform, and expects that number to exceed 10,000 by 2028.

## Enabling responsible AI for regulatory work

One of the most important themes that is worth noting here is that the FDA’s modernization program was not about AI for AI’s sake. It was about enabling responsible AI in a federal regulatory environment. The agency has integrated Halo with Elsa, its enterprise AI platform, to support AI innovation at scale, with AI use cases already in production, in pilot, and more than 10 in flight.

A flagship example is MARS, the FDA’s initiative for modernizing and accelerating regulatory submissions. MARS uses Databricks integrated with Elsa to help reviewers analyze massive volumes of structured and unstructured information associated with drug and device applications, including clinical trial results, safety data, and labeling. The goal is to get the right information to the right reviewer faster, reduce time spent on data wrangling, and support better-informed regulatory decisions.

Just as important, the FDA emphasized a human-in-the-loop approach: AI does the legwork and augments the expertise of scientists and reviewers, but does not replace them.

## Lessons for other agencies scaling secure AI

[翻译失败，原文如下]

The FDA’s journey surfaces several lessons that resonate across the public sector. First, stakeholder engagement is not a one-time event; it is a continuous commitment because every center has different needs, timelines, and risk tolerances. Second, security planning has to start early because, in a FedRAMP High environment, every architectural decision has downstream implications.

The FDA also stressed the importance of building for flexibility instead of hard-coding configurations, adopting wave-based migrations instead of big-bang cutovers, and treating a strong vendor partnership as an operational asset rather than a procurement checkbox.

The closing message from the session was especially clear. Authorization is an accelerant. Governance is the prerequisite for AI. And large-scale modernization can move faster when teams run critical workstreams in parallel instead of waiting for perfection.

## A blueprint for mission-ready AI

The FDA’s story shows that secure AI in government is not about bolting models onto legacy systems. It is about building the governed data foundation, secure architecture, and operational discipline required to make AI useful in high-stakes environments.

For public sector leaders, that may be the most important takeaway of all. When governance is built in from the start, modernization does more than reduce technical debt. It creates the foundation to put AI into the hands of scientists, analysts, and decision-makers securely and responsibly in support of the mission.

## Learn more

Check out the sessionHow the FDA Is Scaling Secure AI with Databricks for Governmentpresented at Data + AI Summit, 2026

- Explore theDatabricks Security and Trust Center
- ReviewDatabricks Security Best Practices
- Follow theSecurity and Trust Blog
- Download theDatabricks AI Security Framework (DASF)

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[How the FDA is building a secure, AI-ready data foundation on Databricks for Government](https://www.databricks.com/blog/how-fda-building-secure-ai-ready-data-foundation-databricks-government)
> 
> 翻译时间：2026-09-05 06:35
