---
title: How Constellation is building a governed data foundation on Databricks
title_original: How Constellation is building a governed data foundation on Databricks
date: '2026-11-12'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-constellation-building-governed-data-foundation-databricks
author: ''
summary: '[翻译失败，原文如下]


  - Constellation’s team built strong data capabilities within their own domains,
  but questions that cross domains, like “How many customer...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-13T09:19:35.815657'
---

[翻译失败，原文如下]

- Constellation’s team built strong data capabilities within their own domains, but questions that cross domains, like “How many customers do we have?”, need shared definitions.
- Constellation is building a governed Enterprise Data Platform on Databricks, using Unity Catalog for lineage, access control, and shared business context.
- On that foundation, the team is developing AI use cases for nuclear engineering, outage planning, and sales.

Constellation operates the largest nuclear fleet in the United States. For them, one of the hardest parts of preparing for AI wasn’t choosing models, it was agreeing on what the data means. Constellation’s team is building a governed Enterprise Data Platform (EDP) on Databricks to make data consistent and usable across the business, and its approach offers a practical roadmap for other enterprises.

## Who Constellation is

Constellation is the nation's largest producer of clean and reliable energy, with generating capacity equivalent to the needs of 27 million homes and approximately 2.5 million retail customer accounts. That breadth of operations and customer relationships is why shared definitions and governance matter to their data work.

Constellation collects data from asset management, supply chain, commercial and trading systems, and operations across the fleet. These are feeding everything from near-real-time market models to nuclear telemetry. In a business where safety and reliability come first, getting definitions and governance right matters. That risk profile drives every architectural choice that follows.

## The problem: High-quality data, no shared semantics

Teams across Constellation built strong data capabilities for their own work. However, questions that spanned those teams still required additional effort to connect information and reconcile differences in how it is defined. Data sat in dozens of places, with no shared semantic layer defining what it meant across domains.

Constellation faced a problem that many organizations still struggle with: a simple question with no single answer: “How many customers do we have?” Retail keys on the billing meter, wholesale on the counterparty and the CRM on an account or user. Three correct answers with three different meanings. The issue only compounded as Constellation grew through acquisitions, including Calpine in 2026, which had 79 power plants across 22 states and 27 GW of capacity. A completely separate stack with its own definitions, warehouses and modeling conventions. The EDP suddenly had to absorb an entity roughly Constellation’s own size. Bringing meaning to data and governance is the shift Constellation is making as it develops the EDP on Databricks.

## The foundation: An enterprise data platform on Databricks

Constellation's answer is a governed EDP built on Databricks.The EDP is the shared foundation that connects previously siloed systems and provides the business with a single shared understanding of its data. It's the deliberate shift from many disconnected, well-built systems to a governed foundation where data carries shared meaning across the enterprise.

The platform decision itself took only weeks. Constellation chose Databricks because it gave them room to experiment, grow, and mature as they went and, just as importantly, because it could interoperate with their existing architecture instead of forcing a rip-and-replace. Three architectural pillars stood out:

- Shared meaning as conforming semantics.Rather than forcing each domain onto one definition, Constellation’s EDP team works with business leaders to define governed, conformed entities - agreeing on what a "customer" means across retail, wholesale, gas and CRM - and replicate those definitions across the enterprise. On top of that, Constellation built a semantic knowledge layer that maps the business relationships - customer, contract, asset and how they connect across domains.The team uses Data Vault as their modeling method which is used selectively for critical, reusable entities that need to flex as systems change. Not every dataset is vaulted. The modeling choice is deliberate and depends on whether the entity will be reused, audited, or evolved over time.
- Governance is the ownership model, not just access control.A major decision factor for Constellation was choosing a service that went beyond traditional access control to convey semantic meaning to its stakeholders. With that criterion identified,Unity Catalogwas the obvious choice. Unity Catalog provides the lineage, fine-grained access and single permission model. Constellation went beyond the technical layer to answer the question that other platforms struggle with: who owns the meaning? With Unity Catalogmetric views, it is even easier. Different data domains call for different access and governance controls. Constellation’s team designed the platform to support those requirements as it brings new use cases onto the foundation. Establishing internal approvals and governance became the trust anchor.
- Multi-workspaces on one governed foundation.The same governed datasets, surfaced across separate workspaces and business semantics are defined once and consumed many times.

For Constellation, Databricks supports both data engineering and governance, giving teams a controlled environment to build AI.

## Three example use cases built on the same foundation:

On the same governed foundation, three early use cases are showing what’s possible across very different parts of the business.

### 1. Nuclear engineering assistant

Constellation is developing an assistant, built withDatabricks Genieand governed through Unity Catalog, to help engineering teams find and use approved technical information more easily, reducing the effort involved in answering complex questions.

### 2. Outage planning: Planned nuclear maintenance management

Planned outages are among the most complex operations Constellation runs. They happen for refueling, major maintenance, regulatory inspections, and equipment work. Each one brings large crews and many work orders together at one site on a tight schedule. Coordinating them means drawing on scheduling, work execution, and asset health data from different systems. The team is bringing that data together in Databricks to help planners analyze schedules and coordinate work, with decisions remaining with the outage teams.

### 3. Sales intelligence: Opportunity prioritization & next best action

In sales, bringing together relevant customer and commercial information helps teams prepare for conversations and identify growth opportunities. The team is developing AI capabilities on Databricks to make this information more consistent, accessible, and actionable - supporting outcomes such as prioritizing high-value opportunities and recommending the next best action. All of this is built on the same governed data foundation in Databricks, with appropriate data guardrails.

## Main takeaways

Constellation’s experience underscores that an enterprise data platform is as much about meaning and governance as technology. Its team is building the definitions, controls, and reusable data foundation needed to support useful analytics and AI across different parts of the business. Databricks with Unity Catalog makes the data trusted and discoverable for business users.

This governed foundation also enables data scientists to build machine learning and agentic AI solutions with Databricks, includingGenie OneandGenie Agents. The team is using these capabilities as it develops use cases in sales, maintenance planning, and engineering support.

## Looking forward

Constellation is exploringGenie Ontology, a self-learning knowledge graph that adds business context and Unity CatalogPages, which centrally manages business definitions in Unity Catalog. Together, these capabilities extend the semantic layer by making data more meaningful, consistent and easier to use.

[翻译失败，原文如下]

Learn more about their story in thisblogpost by Constellation leaders Jay Cavalcanto, SVP & CIO and Vineeth Vijaykumar, VP - IT Business Management Office.

WatchConstellation's Databricks Data + AI Summit presentation(Minute marker 56.23)

Solutions,Data Science and ML,Energy,InsightsandEvents

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[How Constellation is building a governed data foundation on Databricks](https://www.databricks.com/blog/how-constellation-building-governed-data-foundation-databricks)
> 
> 翻译时间：2026-11-13 09:19
