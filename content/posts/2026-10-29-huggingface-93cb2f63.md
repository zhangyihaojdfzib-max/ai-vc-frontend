---
title: 'Announcing Project ProtoStar: Making Publicly Funded Science AI-Ready'
title_original: 'Announcing Project ProtoStar: Making Publicly Funded Science AI-Ready'
date: '2026-10-29'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/announcing-project-protostar
author: ''
summary: '[翻译失败，原文如下]


  # Announcing Project ProtoStar: Making Publicly Funded Science AI-Ready


  An initiative bringing together universities, research organizat...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-30T08:47:43.909589'
---

[翻译失败，原文如下]

# Announcing Project ProtoStar: Making Publicly Funded Science AI-Ready

An initiative bringing together universities, research organizations, industry, and the open science community to make publicly funded research easier to discover, reuse, and build upon.

Today, we're announcingProject ProtoStar, an initiative to unlock the potential of publicly funded scientific research by making datasets, models, and code more accessible and reusable, particularly for AI-driven research. ProtoStar brings together research institutions, industry, and the open science community to support the release of scientific artifacts in AI-ready, machine-actionable formats, and to demonstrate their value through a series of open challenges. The first challenge, hosted byCarnegie Mellon University, opens on November 2. SeeHow to Participatebelow.

The initiative's founding partners includeCarnegie Mellon University,Purdue University,Georgia Institute of Technology,Arizona State University, andThe George Washington University, all working through theOpen Forum for AI (OFAI)as the university coalition partner; theAstera Institute;Hugging Faceas the infrastructure partner; and theOpen Research Community Accelerator (ORCA), through itsFostering Innovation Network, as the community partner.

Participating organizations formalize their involvement through a memorandum of understanding supporting the release of suitable scientific datasets, models, and code in AI-ready formats on open infrastructure. Organizations interested in joining Project ProtoStar can reach out toprotostar@orcaopen.org.

## Making publicly funded science more usable

The U.S. federal government invests approximately$190 billion annually in research and development, and federal policy increasingly expects the results to be shared publicly. Agencies such as theNational Institutes of Health (NIH)andNational Science Foundation (NSF)have strengthened public-access requirements for funded research publications and require researchers to plan for sharing the underlying data. Hugging Face is among theten generalist repositories listed by NIHfor sharing research data.

But making research publicly available does not automatically make it usable.Scientific datasets, models, and code are often scattered across incompatible systems, stored in static or legacy formats, or released without the documentation, metadata, and provenance needed to understand and reuse them. These limitations make it harder for researchers to build on existing work, and harder still for AI systems to discover, interpret, and combine scientific resources across disciplines.

Project ProtoStar aims to help close this gap by encouraging systematic sharing of publicly funded scientific artifacts in AI-ready formats, supported by open infrastructure and practical publishing guidance. It builds on efforts such as theNational Cancer Institute's AI Data-Readiness ChallengeandHugging Face's guide to preparing public-sector data for AI. The goal is to make it easier for research organizations to meet existing public-access expectations while increasing the scientific value of the work they release.

The demand for reusable scientific resources is already evident.Hugging Facehosts more than 17,000 public datasets across core scientific domains, including genomics, protein design, chemistry, weather and climate, Earth observation, and astronomy. That figure approaches 29,000 when medicine and mathematics are included, alongside a comparable number of scientific models.

The pace of sharing is also accelerating.Researchers shared more than three times as many new science datasets on Hugging Face in the first nine months of 2026 as in the same period of 2025, with growth remaining substantial even after excluding the largest individual uploader.

Figure 1. New public science datasets on Hugging Face per quarter, by domain (Q1 2023–Q3 2026). Counts datasets still public, by creation date. Source: Hugging Face Hub data, October 2026.Explore the data.

When organizations share research in reusable formats, the scientific community can build on it at scale. The 18 public repositories maintained by NIH'sNational Center for Biotechnology Information (NCBI)on Hugging Face have collectively received more than 11 million downloads, whileNASA IMPACT's27 repositories have received approximately 770,000 downloads, as of October 26, 2026. Documentation is also an important part of making these resources useful:90% of dataset downloads on Hugging Face are from fully documented datasets.

Publicly available genomic data has proved important in contributing to research that further advances fields such as biological research; researchers at Hugging Face have been building on openly available scientific resources, including recent releases fromHuggingFaceBiosuch asCarbon-AandCarbon-X. By releasing the resulting models, datasets, and tools openly, these efforts demonstrate how existing scientific resources can support new research that others can build upon.

This is the kind of activity that we are further catalyzing via Project ProtoStar through institutional policies adopted by participating orgs. As an early example of institutional commitment, CMU's Open Source Programs Office is encouraging its researchers to share suitable datasets, AI models, and other research outputs on Hugging Face, while recognizing the continued importance of domain-specific repositories.

## Open Science Challenges

Making scientific artifacts AI-readyis an important first step. We also want to demonstrate what researchers, developers, and the broader scientific community can accomplish when those resources are made available for reuse.

A central question for ProtoStar is:Can publicly funded scientific datasets, models, and code, released in AI-ready formats, be readily discovered, reused, combined, and extended to accelerate scientific discovery and public benefit?

To explore this, ProtoStar will organize a series of open challenges, each hosted by a participating research institution and built around scientific resources that the institution has released openly. The challenges have two complementary goals:

- Demonstrate scientific reuse.Produce concrete examples of researchers and developers building on publicly funded scientific artifacts, including applications that combine resources across institutions or disciplines.
- Learn what makes reuse possible.Identify technical barriers, documentation gaps, interoperability challenges, and successful practices that can inform future research infrastructure, funding decisions, and public policy.

The resulting projects and lessons learned will help build a practical evidence base for making publicly funded science more accessible and useful.

### The first challenge: Climate Risk Intelligence

![CMU Climate Risk Intelligence Challenge, November 2–13, 2026](/images/posts/e645064cc636.jpg)

Hosted byCarnegie Mellon University| November 2–13, 2026

The inaugural ProtoStar challenge invites participants to test whether AI can improve predictions of urban climate conditions using historical weather data from 210 U.S. cities. Building onresearch by Carnegie Mellon University, teams will use climate records through 2018 to predict actual conditions from 2019 to 2026, allowing their models to be evaluated against observed weather rather than hypothetical future scenarios.

Participants will forecast four indicators relevant to urban planning: average annual temperature, total annual precipitation, the hottest day of the year, and cooling degree days, a measure of demand for air conditioning. Their predictions will be compared against simple statistical baselines, including historical averages and linear trends, to assess whether AI approaches offer meaningful improvements in accuracy.

[翻译失败，原文如下]

Beyond forecasting, participants will also propose a short climate adaptation policy idea informed by what they learned from the data. This component encourages teams to connect scientific analysis with practical public benefits, such as preparing cities for extreme heat, improving energy efficiency, or managing changing precipitation patterns.

Teams will submit a Hugging Face dataset with these outputs. Forecasting performance will be assessed through a public leaderboard measuring prediction errors against established baselines, while policy ideas will receive separate consideration. Final forecasting results will be published in early 2027, once the complete 2026 weather records are available.

Explore the CMU Climate Risk Intelligence Challenge

The CMU challenge is the first in this series. Other participating institutions will host their own challenges sequentially, each highlighting different publicly funded scientific resources and opportunities for reuse. Future challenges will be announced through theProject ProtoStar page on Hugging Face.

## How to Join Project ProtoStar

Whether you're an academic researcher, student, independent developer, or company building on open scientific infrastructure, ProtoStar offers opportunities to put publicly funded research to work and help us learn what is needed to make AI-ready open science more widely useful.

We also welcome universities, federal research agencies, national laboratories, nonprofits, and other research organizations interested in making their scientific resources more accessible and reusable.To explore participation or collaboration, reach out toprotostar@orcaopen.org.

Our hope is that ProtoStar will make it easier for publicly funded scientific work to reach the people and tools that can build on it, while generating practical evidence about the infrastructure and practices needed to support open science at scale.

---

> 本文由AI自动翻译，原文链接：[Announcing Project ProtoStar: Making Publicly Funded Science AI-Ready](https://huggingface.co/blog/announcing-project-protostar)
> 
> 翻译时间：2026-10-30 08:47
