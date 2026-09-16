---
title: How Databricks’ marketers use data 3x more with Genie, an AI analytics assistant
title_original: How Databricks’ marketers use data 3x more with Genie, an AI analytics
  assistant
date: '2026-09-15'
source: Databricks Blog
source_url: https://www.databricks.com/blog/databricks-marketers-use-data-3x-genie-ai-analytics-assistant
author: ''
summary: '[翻译失败，原文如下]


  - Databricks built Marge, an AI analytics assistant powered by Genie Agents, on
  a governed Marketing Lakehouse. It gives marketers truste...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-16T07:28:55.877814'
---

[翻译失败，原文如下]

- Databricks built Marge, an AI analytics assistant powered by Genie Agents, on a governed Marketing Lakehouse. It gives marketers trusted answers in seconds through natural-language questions, reducing repetitive analytics requests.
- Databricks marketers now use data 3x more often in decisions, adoption exceeds 85% of the marketing organization, and the team scaled access to insights without adding analytics headcount.
- Scaling self-service analytics works best when starting with one high-value use case, defining business context, then validating answers. Embed the assistant into existing workflows and continuously improve it through user feedback.

Most marketing teams aspire to be data-driven. In practice, getting a trusted answer, at the moment a decision needs to be made, can still take days.

At Databricks, we addressed this challenge by unifying our marketing data in a governed lakehouse and building Marge, our marketing implementation ofGenie Agents. Marge lets marketers ask questions in natural language and receive governed answers in seconds.

The results have changed how our organization works:

- Marketers use data 3 times more often to make decisions.
- More than 85% of the marketing organization uses Marge.
- Usage has grown 50% quarter over quarter.
- Marge handles more than 800 questions each month and has answered over 5,000 in total.
- Flagged incorrect responses have decreased by 25% as the system has improved.
- We have scaled access to insights without adding analytics headcount.

These outcomes came from treating conversational analytics as an ongoing product and operating model. We built on governed data, taught Genie our business language, earned trust one use case at a time, and embedded it directly into the way marketers already work.

I'm Liz Dobbs, Databricks’ AVP of Marketing Technology, and in this video I share a practical playbook on how my team helped the Databricks marketing department use data 3X more often in decisions:

## First, why is self-service marketing analytics so difficult?

Marketing data spans campaign platforms, web analytics, CRM systems, event tools, advertising channels and sales data. Each system brings its own definitions, identifiers and reporting logic. Even when dashboards exist, marketers often struggle to know which metric is current, which source is authoritative or how to answer the next question that the dashboard wasn’t designed to address.

Our marketing organization faced the same challenges:

- Data and reporting lived in multiple places.
- Dashboards were sometimes stale or inconsistent.
- Marketers didn’t always know which numbers to trust.
- Analytics and engineering teams spent significant time on repetitive requests.
- Demand for insights grew faster than the analytics team could support it.

We first created a Marketing Lakehouse within the company-wide Databricks lakehouse shared across Marketing, Finance, Sales and Product. It became the governed source of truth for our go-to-market data, aligning campaign and sales information around consistent definitions and metrics.

That foundation made Marge possible.

## What is Marge, the Databricks Marketing Genie?

Marge is a conversational analytics assistant built with Genie Agents. It’s grounded in the data and business context in our Marketing Lakehouse, including the definitions Databricks marketers use for regions, products, channels, campaigns, fiscal periods and pipeline.

Marketers can ask questions in plain English, such as:

- How did my email campaign perform?
- Which programs influenced pipeline this quarter?
- How did event registration compare across regions?
- Where should we adjust campaign spend?

Marge translates those questions into analytical queries and returns answers based on governed enterprise data.Unity Catalogprovides centralized governance, lineage and role-based access controls, so each user sees only the data they are authorized to access.

Marketers access Marge throughGenie One, the AI cowork experience for business users that brings together dashboards, Genie Agents, apps and deeper analysis. Genie One automatically routes each request to the appropriate Genie Agent when applicable. We have also created focused agents for domains such as web performance, digital analytics and marketing planning, allowing each one to operate with narrower and more relevant context.

For more complex questions, Agent mode can evaluate multiple steps and produce a deeper analysis. The experience gives marketers a faster path from a business question to a grounded answer and recommended next step.

## How did Databricks make Genie accurate and trustworthy for marketing?

Trust has been our top priority from the initial pilot through broad rollout. No AI system will be perfect, so we focused on 4 mechanisms that make Marge more accurate, reliable and transparent:

### 1. Document the data and its relationships

Genie needs the same context a new analyst would need. That starts with a clear data model, including how tables relate and how they should be joined.

We use Unity Catalog to centralize metadata, table descriptions, column annotations, lineage and access controls. AI-generated descriptions gave us a useful first pass, but marketing stakeholders and data experts reviewed and enriched them with the business context that only people inside the organization would know.

Practical examples include documenting:

- The precise meaning of a marketing-qualified lead
- The dates included in each fiscal quarter
- How campaigns map to products and regions
- Which fields represent cost, engagement or attribution
- The approved relationships between campaign, account and sales data

Clear metadata helps Genie interpret a question correctly before it generates a query.

### 2. Encode verified answers and example queries

For common, high-value questions, we provide trusted assets and verified logic that domain experts have reviewed. These cover areas such as conversion rates, customer lifetime value and event registration. Users can see when an answer is based on verified logic, which adds an important signal of trust.

We also add example question-and-query pairs for complex or frequently asked questions. These examples teach Genie how to handle a known scenario and help it generalize the same pattern to similar questions.

As a rule of thumb:

- Use governed metric definitions for standard business concepts.
- Use example SQL for complex or ambiguous questions.
- Use trusted assets when a high-value question requires a consistent, verified answer.

### 3. Teach Genie the language of your business

Every organization has terminology that looks simple but carries specific meaning. “Pipeline,” “region,” “fiscal year” and “campaign” may each have definitions that differ from one company to another.

We give Marge clear behavioral guidance for interpreting these terms and for handling ambiguity. For example, users may say “spend” or “investment” when the underlying field is named “cost.” Marge needs to understand that those words refer to the same concept.

We also instruct Marge to ask a clarifying question when a request is missing critical information, such as the time period, channel or region. The goal is to surface ambiguity rather than guess.

### 4. Create continuous feedback and evaluation loops

Every response gives users an opportunity to provide positive or negative feedback. The marketing analytics team reviews ratings and comments in a monitoring dashboard, investigates issues and updates the agent as needed.

We also run benchmark questions against known answers to evaluate performance systematically. A meaningful decrease in benchmark accuracy signals that the data model, definitions or agent context may need attention.

[翻译失败，原文如下]

This stewardship is lightweight. Today, one BI manager spends approximately one hour per week reviewing feedback and maintaining Marge. That small, consistent investment has helped reduce the rate of flagged incorrect answers by 25%.

## How did Databricks drive adoption of Genie across marketing?

Technical quality was only half of the work. Marketers also needed to believe that Marge understood their needs and could fit naturally into their daily workflow.

As I often tell my peers, this is not a "Field of Dreams"product. Building it does not guarantee that people will use it. We focused on 4 adoption practices:

1. Start with users and their real questions

### Start with users and their real questions

We worked directly with marketers to understand the questions they asked most often, the dashboards they already used and the language they used to describe their work. Their input shaped the data, examples and instructions we used to configure Marge.

This also made marketers active participants in the product. They could see that the experience was being built with them and for them.

1. Begin with one focused use case

### Begin with one focused use case

Our first use case was email campaign performance. We included only the essential campaign, recipient and engagement data required to answer those questions.

Starting with a narrow scope made it easier to validate accuracy, build confidence and show value quickly. We added account data, attribution and other domains later, based largely on what users requested.

1. Put Genie inside an existing workflow

### Put Genie inside an existing workflow

We embedded Marge into our analytics support process. Every marketing analytics ticket receives an automated response asking, “Have you asked Genie?” Analysts only engage after the requester indicates that they’ve tried Genie.

This simple change directs basic questions to self-service analytics and preserves analyst time for more complex work. Our team often describes the difference as moving analysts away from 101- and 201-level requests so they can focus on 301- and 401-level analysis.

1. Act on feedback quickly

### Act on feedback quickly

We continuously update metadata, examples, trusted answers and instructions based on user feedback. Quick improvements show marketers that their input matters and help Marge become more useful with every iteration.

The feedback loop also helps us expand with discipline. We add data and capabilities in response to demonstrated demand instead of trying to anticipate every possible question at launch.

## What business impact has marketing achieved with Genie?

Marge has become the single biggest time saver for our Marketing Analytics team. Marketers get governed answers in seconds, while analysts and engineers spend less time fulfilling repetitive data pulls.

That capacity has shifted toward higher-value work, including experimentation, model design and improvements to foundational data products. Technical bandwidth is no longer a bottleneck for common activities such as campaign launches and quarterly business reviews.

Marketers can also act faster. Easier access to trusted data supports quicker campaign adjustments, smarter segmentation and more informed budget allocation. Most importantly, data has become part of more day-to-day decisions across the organization.

## A practical rollout sequence for Genie in marketing

For martech and data teams beginning a similar journey, we recommend this sequence:

1. Choose one bounded, high-frequency use case.Start with a question marketers ask often and data you understand well.
2. Select the minimum required data.Include only the tables and fields needed to answer that first set of questions.
3. Document the business context.Define relationships, metrics, fiscal periods, regions and domain-specific language.
4. Add verified logic for important questions.Use metric definitions, example SQL and trusted assets where consistency matters most.
5. Pilot with a small user group.Observe their actual questions, confusion points and language before expanding.
6. Measure quality and behavior.Track usage, feedback, flagged answers and benchmark accuracy.
7. Embed Genie into an existing workflow.Make it the natural first stop for common analytics questions.
8. Expand based on demand.Add new data and focused Genie Agents as users demonstrate a need for them.

## What should teams know before launching Genie for marketing?

Three lessons stand out from our experience.

First, self-service analytics depends on a strong data foundation. The underlying data needs to be governed, trustworthy and connected through consistent definitions. AI makes that context easier to access, but it doesn’t compensate for conflicting source data and unclear business logic.

Second, central governance helps teams expand access with confidence. Unity Catalog gave us one place to manage definitions, lineage and role-based access to sensitive data as adoption grew.

Third, trust is earned through the user experience. Start small, observe how marketers actually work and improve the system based on what they tell you. When users see that an agent understands their language, respects their access permissions and becomes more useful through their feedback, adoption follows.

Marge began as a prototype for 10 users and one use case. Today, it supports more than 85% of our marketing organization and has answered over 5,000 questions. The path from pilot to scale was built one trusted answer at a time.

Watch the full interview with Liz Dobbs, exploreGenie Agent documentation, or check out these related blogs:

- Five ways marketers can use Genie One
- Unified context: The missing layer for enterprise AI coworkers

### What is Databricks Genie for marketing?

Genie Agents give marketing and business teams a natural-language interface for governed business data. Marketers can ask questions about campaign performance, pipeline, web activity, events and other approved data without writing SQL. Each response respects the user’s Unity Catalog permissions.

### What is the best first use case for a marketing Genie?

Choose a frequent, well-defined question supported by a small set of trusted data. Databricks began with email campaign performance using campaign, recipient and engagement tables, then expanded based on user demand.

### How can teams improve the accuracy of Genie?

Document tables and relationships, define business metrics, add example SQL and trusted assets, give specific clarification instructions, review user feedback and test against benchmark questions. Accuracy improves through focused context and ongoing evaluation.

### Does Genie replace marketing analysts?

Genie handles many repetitive and lower-complexity questions, allowing analysts to spend more time on experimentation, model design and strategic analysis. At Databricks, this shift helped the marketing analytics team support broader usage without adding headcount.

### How much ongoing maintenance does a marketing Genie require?

The effort depends on scope and data complexity. At Databricks, ongoing stewardship currently requires about one hour per week from one BI manager to review feedback, investigate issues and update context.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[How Databricks’ marketers use data 3x more with Genie, an AI analytics assistant](https://www.databricks.com/blog/databricks-marketers-use-data-3x-genie-ai-analytics-assistant)
> 
> 翻译时间：2026-09-16 07:28
