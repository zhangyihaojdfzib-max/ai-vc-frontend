---
title: The Lakehouse for AI
title_original: The Lakehouse for AI
date: '2026-11-17'
source: Tomasz Tunguz
source_url: https://tomtunguz.com/the-lakehouse-for-ai/
author: ''
summary: '[翻译失败，原文如下]


  In short :LanceDB raised a $57.5m Series B ($98.5m total) after growing revenue
  >10x YoY & open-source downloads 6x to 120m+. Across Exa,...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-19T09:43:06.697737'
---

[翻译失败，原文如下]

In short :LanceDB raised a $57.5m Series B ($98.5m total) after growing revenue >10x YoY & open-source downloads 6x to 120m+. Across Exa, Runway, Microsoft AI, Adobe & NVIDIA, teams are replacing fragmented blob, Parquet & vector copies with a single multimodal lakehouse supporting 100b rows, 40b+ vectors & 8k+ GPUs training in parallel.

Across the largest AI labs & AI infrastructure companies, there is a common component : a lakehouse that stores data for training & inference called Lance.

Lance allows companies to manipulate massive collections of files in the most efficient way possible for AI.

![The LanceDB Multimodal Lakehouse unifying curation, feature engineering, training & search](/images/posts/5cd4cad408b3.jpg)

Five production deployments show how that architecture runs at frontier scale :

Exastores 35pb in Lance tables across 100b semantic web pages with crawl-to-search latency under five minutes.1Index lead Jan van der Vegt explained :

“These column backfills allow us to keep the old data in place & only write what is new.”

Runwayruns Lance & LanceDB Enterprise across its video-generation stack. CTO Kamil Sindi noted :2

“We first started using the Lance format in 2024 because it was the only option that handled unstructured data, column appends, distributed reads & ad-hoc SQL all at once.”

Microsoft AIruns LanceDB inside its own tenant & security boundary. Head of Data Platform Suqiang “Jack” Song shared :3

“We rely on LanceDB as the data layer for training across billions of rows of image & code data, with distributed inference reading the format directly across thousands of nodes.”

Adobemanages 40pb to 50pb across 800k tables & 220b daily events, contributing 20+ pull requests upstream.4As Adobe’s platform team put it :

“Where should the AI-native data live? Our answer is in the same lakehouse, under the same contract as everything else.”

NVIDIAclosed the loop on physical AI. Cosmos tech lead Max Li explained :5

“First ever, we train on thousands & tens of thousands of GPUs at scale with Lance tables directly.”

Since its Series A last June, LanceDB has grown revenue more than 10x year over year across Netflix, Microsoft AI, Runway, Luma AI & Midjourney, while open-source downloads grew 6x past 120m.6

Theory partnered with Chang She & Lei Xu at Seed & led their $30m Series A.7Today we are thrilled to join Bessemer Venture Partners & Innovation Endeavors, alongside Dimension, Swift Ventures, CRV & Y Combinator, in LanceDB’s $57.5m Series B.

Learn more about how to use Lancehere.

1. Jan van der Vegt (Exa),Managing an Index of 100s of Billions of Pages with Exa Skeleton, Reverie Summit, November 5, 2026.↩︎
2. Ethan Rosenthal (Runway),Scalable, Multimodal Data Curation, Reverie Summit, November 5, 2026, & Kamil Sindi (CTO, Runway) in LanceDB’s Series B announcement.↩︎
3. Suqiang “Jack” Song (Head of Data Platform, Microsoft AI),Building the Data Flywheel for Frontier AI Model, Reverie Summit, November 5, 2026, & LanceDB Series B announcement.↩︎
4. Jing Chen He & Miao Wang (Adobe),How Adobe Built a Multimodal Lakehouse for AI-Native Experiences, Reverie Summit, November 5, 2026.↩︎
5. Max Li (Technical Lead, NVIDIA Cosmos),Cosmos : Omnimodal World Models for Physical AI, Reverie Summit, November 5, 2026, & LanceDB Series B announcement.↩︎
6. Chang She, “LanceDB Raises $57.5m as AI Research Outgrows the Modern Data Stack,” November 2026, & Yichen Wang (Luma AI),From Raw Delivery to the Training Loop : Luma’s Data Platform on Lance, Reverie Summit, November 5, 2026.↩︎
7. Tomasz Tunguz,A Data Foundation for Multimodal AI : Our Series A Investment in LanceDB, June 24, 2025.↩︎

Jan van der Vegt (Exa),Managing an Index of 100s of Billions of Pages with Exa Skeleton, Reverie Summit, November 5, 2026.↩︎

Ethan Rosenthal (Runway),Scalable, Multimodal Data Curation, Reverie Summit, November 5, 2026, & Kamil Sindi (CTO, Runway) in LanceDB’s Series B announcement.↩︎

Suqiang “Jack” Song (Head of Data Platform, Microsoft AI),Building the Data Flywheel for Frontier AI Model, Reverie Summit, November 5, 2026, & LanceDB Series B announcement.↩︎

Jing Chen He & Miao Wang (Adobe),How Adobe Built a Multimodal Lakehouse for AI-Native Experiences, Reverie Summit, November 5, 2026.↩︎

Max Li (Technical Lead, NVIDIA Cosmos),Cosmos : Omnimodal World Models for Physical AI, Reverie Summit, November 5, 2026, & LanceDB Series B announcement.↩︎

Chang She, “LanceDB Raises $57.5m as AI Research Outgrows the Modern Data Stack,” November 2026, & Yichen Wang (Luma AI),From Raw Delivery to the Training Loop : Luma’s Data Platform on Lance, Reverie Summit, November 5, 2026.↩︎

Tomasz Tunguz,A Data Foundation for Multimodal AI : Our Series A Investment in LanceDB, June 24, 2025.↩︎

---

> 本文由AI自动翻译，原文链接：[The Lakehouse for AI](https://tomtunguz.com/the-lakehouse-for-ai/)
> 
> 翻译时间：2026-11-19 09:43
