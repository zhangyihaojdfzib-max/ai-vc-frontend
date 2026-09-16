---
title: 'Beyond the model: Engineering AI infra with scientific judgement'
title_original: 'Beyond the model: Engineering AI infra with scientific judgement'
date: '2026-09-15'
source: Airbnb Engineering
source_url: https://medium.com/airbnb-engineering/beyond-the-model-engineering-ai-infra-with-scientific-judgement-371316d43261?source=rss----53c7c27702d5---4
author: ''
summary: '[翻译失败，原文如下]


  # Beyond the model: Engineering AI infra with scientific judgement


  ## How Airbnb’s agent harness transforms unstructured data exploratio...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-16T07:28:43.424219'
---

[翻译失败，原文如下]

# Beyond the model: Engineering AI infra with scientific judgement

## How Airbnb’s agent harness transforms unstructured data exploration by encoding scientific methodology into scalable, reproducible, and audit-ready infrastructure.

Listen

By:Wren Dougherty

Ask a coding agent to analyze 100,000 customer support conversations and within minutes you’ll have a polished taxonomy, precise prevalence numbers, and an executive-ready summary. What you can’t see is the investigation that produced them: the methods it chose, the evidence it weighed, how much to trust it, or whether a second request would agree. All that reaches you is the polish. The model is undeniably intelligent, but intelligence without methodology is not science.

LLMs certainly make for confident scientists, but we need them to be responsible ones. Smarter models help, but intelligence has never been the whole of science, in people or in machines. The method is as much the product as the answer. That is the idea behind theagent harnesswe built for data science:the methodology itself, built as infrastructure around the model. It governs how an AI agent operates, from framing a question to selecting evidence to recording decisions, so results can be reproduced, audited, and challenged, and the method shared, inspected, and built on.

## The challenge of unstructured data exploration

In 2025, Airbnb was preparing to launch anAI customer service assistant. Before it could ship, we needed to understand exactly what kinds of situations it would face in the real world. That included rare events that could be risky for AI to interact with, and involved examining their taxonomy and prevalence to create the datasets that would help us build a more responsible product.

The investigative work to do this was rigorous, but the process was deeply artisanal. Months of high-touch iteration went into each investigation, from finding the right data, reviewing samples with experts, and generating representative datasets, and the method was manually curated across notebooks, tables, docs, and individual judgment.

This was fine for one investigation — but as we carried the same investigation into new languages, new geographies, and new LLM-based products at a near-weekly cadence, the workload outgrew the process. To bring the same rigor, thought, and quality at this new pace, and involve more people, we needed to make each investigation less bespoke. In short, we needed a way to replicate the methodology itself.

## Insight Miner: Agent harness for unstructured text understanding

Insight Miner starts with the engineering (the queries, the scaled labeling and embedding, the clustering and tracking), so that no one has to learn new infrastructure to run analysis at scale. The core method is well established: extract, embed, cluster. Around that core we assembled the methods we had come to rely on, drawn from internal investigations and industry research: prompt tuning, hard-example mining, contrastive labeling, and how to start with unsupervised exploration then mature into classification. These pieces used to live in separate notebooks, manually iterated and shared by copy and paste. Now they are in one shared package, which gets updated whenever an individual investigation teaches us a better technique.

An investigation begins with a research question in a chat session, with an agent that is at once research partner, executor, and expert in the methods the harness holds. Insight Miner isn’t tied to a single dataset, domain, or question: it runs over any unstructured text source, through whatever lens the question needs, with the same rigor behind every investigation.

As we expanded our community support AI assistant tonew languages and countries, we used Insight Miner to carry out investigations that used to take months in just a matter of days. But its bigger impact was ensuring that rigor and speed both increased, instead of trading off.

With this harness, data scientists were able to shift their focus from executing analyses to improving the techniques used for each step of the process. Because the mechanical parts of investigations can scale and parallelize, we are able to spend more time on the careful parts of an investigation: directly inspecting the most ambiguous or strategic data that helps us deeply understand the product, testing hypotheses and groupings, and building a robust qualitative and quantitative understanding of our data and products. Rather than automating analysis, we’re increasing the amount of human judgment in the most strategic parts of it.

## Going beyond technical teams

Insight Miner was initially designed as a tool for data science teams. However, it quickly evolved beyond that: a year in, dozens of teams are using it for hundreds of types of investigations. In fact, it has more users outside of technical roles than within them, with a particularly heavy representation among operations and product-insights teams. A UI to make data exploration and agent conversations more accessible further increases expert participation.

Subject matter experts who have never written a line of code have been able to directly conduct scaled analyses rather than waiting on scarce eng or DS resourcing. Projects that were previously unresourced or were informed by the manual review of hundreds of examples can instead use our shared best practices and work across several orders of magnitude more data. Use cases span coding open ended survey answers, evaluating model performance, understanding fraud patterns, and many more.

## A new category of infrastructure

Harnesses like Insight Miner are full-stack systems, a new type of infrastructure that must be developed, maintained, evaluated, and continually improved. This type of work is a natural fit for other agentic systems. For Insight Miner, separate agentic systems help us update instructions for new model releases, fold in new best practices, review live use to identify pain points, and watch for, reproduce, and propose fixes for new bugs. These systems form a larger agentic environment reshaping our day to day work in domains well beyond just data science.

A harness can be useful wherever experts carry a methodology worth encoding: legal review, policy analysis, any field where the method is as much the product as the answer. Such systems are critical to adopting AI-first knowledge work. Our CTOhas writtenthat as models commoditize, what endures is proprietary data, deep workflow integration, and above all taste. A harness is where all three accumulate. Expert taste becomes the method every team runs, the workflows deepen with every adopter, and the feedback loops are built in: every run can leave the harness improved for everyone.

If this type of work interests you, check out some of ourrelated positions!

All product names, logos, and brands are property of their respective owners. All company, product, and service names used in this website are for identification purposes only. Use of these names, logos, and brands does not imply endorsement.

---

> 本文由AI自动翻译，原文链接：[Beyond the model: Engineering AI infra with scientific judgement](https://medium.com/airbnb-engineering/beyond-the-model-engineering-ai-infra-with-scientific-judgement-371316d43261?source=rss----53c7c27702d5---4)
> 
> 翻译时间：2026-09-16 07:28
