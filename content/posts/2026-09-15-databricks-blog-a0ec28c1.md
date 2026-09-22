---
title: 'Data Ontology defined: The context layer your AI agents are missing'
title_original: 'Data Ontology defined: The context layer your AI agents are missing'
date: '2026-09-15'
source: Databricks Blog
source_url: https://www.databricks.com/blog/data-ontology-defined-context-layer-your-ai-agents-are-missing
author: ''
summary: '[翻译失败，原文如下]


  - Enterprise data architecture has always assumed a knowledgeable human sits between
  the data and the decision, supplying the context a s...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-22T07:37:48.491844'
---

[翻译失败，原文如下]

- Enterprise data architecture has always assumed a knowledgeable human sits between the data and the decision, supplying the context a schema can't. AI agents remove that human, and the assumption breaks.
- Semantic layers and knowledge graphs tried to solve this before and often became shelfware, because modeling an entire enterprise by hand can't keep pace with how fast a business changes.
- The fix isn't a bigger documentation project. It's an ontology that governs the small set of concepts that can't be wrong and continuously learns the rest from how the organization already works, the model Databricks has built into Genie Ontology.

Ask five people at the same company what "revenue" means and there's a chance you'll get five different answers, each one correct within its own context and incompatible with the others. For as long as a human analyst has sat between that ambiguity and the final report, the ambiguity has been manageable. It's tribal knowledge: the kind of thing a good analyst just knows.

AI agents don't know it. And that's the problem.

Richard Tomlinson has spent his career thinking about the layer of enterprise data that never quite shows up in the schema. In this conversation, he walks through why that layer, the ontology, is suddenly the most important piece of infrastructure most companies haven't built yet, why the last generation of attempts to build it largely stalled, and what has to be true of an ontology for it to hold up once agents start relying on it.

## Why do AI agents need business context that a schema can't provide?

What's the assumption about enterprise data that AI agents are quietly breaking?

Richard Tomlinson: For decades, enterprise data architecture has operated on an implicit assumption: if you organize the data correctly, an intelligent user can figure out what it means. Tables, schemas, catalogs and dashboards provide structure, while humans supply the missing context. An analyst knows which of five revenue tables Finance trusts, what "active customer" means this quarter, or why one calculation should be used instead of another.

AI agents break that assumption because there may be no knowledgeable human sitting between the data and the decision. The agent has to discover the meaning itself. Giving an agent access to more data doesn't solve this. It needs the business context humans have historically carried in their heads: definitions, relationships, calculations, authoritative sources, expertise and permissions. That's why enterprise context is becoming as important to AI architecture as the data itself.

## What is a data ontology, and how is it different from a schema?

How do you define a data ontology, and what does it capture that a schema never could?

Richard Tomlinson: A schema describes how data is structured. An ontology describes what that data means in the context of the business. It connects technical assets such as tables, metrics and queries to business concepts: definitions, relationships, calculations, sources of expertise and rules about how those concepts should be interpreted.

A schema might tell an agent that a table contains net_rev, gross_rev and recog_rev. An ontology can help it understand which definition of revenue applies to the question, which source Finance considers authoritative, how the calculation is normally performed and whether the person asking is even permitted to access it. The schema is the map of the data. The ontology is closer to a map of how the organization understands and uses that data.

## Why did semantic layers and knowledge graphs struggle to scale?

Semantic layers and enterprise knowledge graphs promised "one version of the truth" years ago and mostly became shelfware. What has to be true of an ontology for it not to suffer the same fate?

Richard Tomlinson: I'd soften that premise slightly. Semantic layers and knowledge graphs have delivered real value, particularly for business-critical concepts. The problem comes when organizations try to manually model the entire enterprise. Business knowledge changes too quickly and is spread across too many places. The important logic may be in a dashboard, a SQL query, a notebook, a ticket or simply the way a team repeatedly works. No central team can document all of that and keep it current.

The more scalable model is to “model the head and learn the tail.” Humans should explicitly define and govern the small set of concepts that cannot be wrong, things like revenue, compliance rules and core KPIs. The broader ontology should continuously learn the long tail from how the organization operates, while still ranking knowledge by authority and respecting governance. If maintaining the ontology becomes a separate enterprise data-modeling project, it will eventually fall behind the business it's supposed to describe.

## What happens when an AI agent lacks business context?

Can you describe a moment where an agent gave a confident, wrong answer because it lacked real business context? What made it convincing enough that someone almost trusted it?

Richard Tomlinson: One example from our own internal testing was asking several AI systems to prepare a briefing for an upcoming Product Advisory Board. One assistant produced a polished report almost immediately and stated that 24 customers were participating. It included the kinds of details you'd expect in an executive brief, so at first glance the answer looked credible. When we challenged the system to explain where the number 24 came from, it admitted it had fabricated it.

That's the dangerous failure mode. The answer isn't obviously absurd. It's fluent, specific and presented alongside legitimate information. The problem is that the model doesn't know which internal source contains the ground truth, so it fills the gap with inference. In enterprise AI, a plausible answer can be more dangerous than no answer at all.

## How can you tell if your organization is missing a context layer?

If a data leader wanted to know whether their own organization has this problem, what would they look for? Is there a tell that signals the context layer is missing?

Richard Tomlinson: The clearest signal is how often a simple business question requires a knowledgeable person to translate it before the data can answer it. If someone asks, "What was revenue last quarter?" and the analyst immediately responds with "Which revenue?" or "For which business unit?", that translation step is business context. The same is true when analysts know which dashboard to trust, which table is deprecated, or which definition one team uses versus another.

Other tells: duplicated dashboards, conflicting KPI definitions, analysts repeatedly answering the same questions and business users distrusting self-service because different tools return different answers. The underlying issue is often not that the company lacks data. It's that the knowledge required to interpret the data lives in tribal knowledge, disconnected artifacts and individual experts, rather than in a context layer that AI can reliably use.

### The agentic AI playbook for the enterprise

![ai](/images/posts/739dac6fa259.png)

## What does missing business context cost companies today?

What is this costing companies today, even before they've deployed agents at scale? Is it slower decisions, duplicated analyst work, eroded trust in dashboards?

Richard Tomlinson: All of the above. Organizations already pay a "context tax." Analysts spend time rediscovering definitions, locating authoritative sources, reconciling conflicting reports and explaining business logic that exists somewhere else in the organization. Different teams recreate the same semantics inside different BI tools. Business users wait for analysts because self-service stops working as soon as the question becomes nuanced.

[翻译失败，原文如下]

AI makes this existing problem more visible. Without context, agents repeat much of the same discovery process computationally: exploring schemas, reading documents, trying queries and reconsidering assumptions. That creates additional latency, token consumption and cost without guaranteeing the correct answer. The larger cost, though, is trust. Once users discover that a dashboard or AI assistant can confidently produce the wrong number, they go back to asking a human.

## What changes when AI agents can be trusted to act, not just report?

What changes for a business the moment its agents can be trusted to act, not just report?

Richard Tomlinson: The value of AI changes dramatically. Reporting saves someone the time required to find an answer. Trusted action can remove entire steps from a workflow. An agent can calculate the latest numbers, prepare the weekly business review, investigate an anomaly, update a ticket, contact the right people and repeat that process every Monday without someone orchestrating each step manually.

That also changes the economics of expertise. A finance expert, product manager or operations leader can encode critical methods once and combine them with an agent that understands the broader business context. Their expertise can then be applied across far more decisions and workflows than that individual could personally support. The key qualifier is "trusted": autonomy only becomes useful when the agent understands the business well enough, and is governed tightly enough, to act within appropriate boundaries.

## What's the right way to start building a data ontology?

What's the wrong way to start, the instinct that leads to another shelfware initiative, versus the right first move?

Richard Tomlinson: The wrong instinct is: "Before we can use AI, we need to model the entire enterprise." That turns business context into a multiyear documentation project. By the time every term, relationship and rule has been modeled, large portions of the model are already stale.

The better approach is to start with the knowledge you already have. Govern the small number of concepts that truly cannot be wrong, such as critical KPIs and business definitions, then let the broader context layer learn from the dashboards, queries, notebooks, documents and operational activity your teams are already producing. Don't require the business to document everything before AI can become useful. Let actual usage help build and continuously improve the business understanding the agents consume.

## How should data leaders rethink data architecture for AI agents?

How should a data leader think differently about their data architecture now that context, not just structure, is the thing worth investing in?

Richard Tomlinson: For years, data architecture focused heavily on making data accessible, reliable and governed. Those remain essential, but AI adds another requirement: the architecture must also make business meaning accessible. An agent needs to know not only where data lives, but how the organization interprets it, what relationships matter, which definitions are authoritative, and what evidence supports them.

That means assets that were previously viewed primarily as governance or analytics infrastructure become strategic AI assets. Metric definitions, documentation, lineage, certifications, usage patterns and business glossaries collectively teach AI how the company works. The emerging architecture is therefore not just a data plane plus an AI model. It also needs a shared context layer that can serve the same business understanding to many agents and applications.

Does data ontology actually improve agent accuracy?

Richard Tomlinson: An ontology by itself doesn't magically make an agent accurate. What improves accuracy is supplying the agent with the right, authoritative context at the point where it's reasoning. If the ontology can tell the agent which definition applies, where the trusted data lives, and which relationships or calculations matter, the agent spends less time guessing and exploring incorrect paths.

We have evidence of that effect withGenie Ontology, the automatic context layer underneath Databricks' Genie One and Genie Agents. In an internal Databricks benchmark using 28 real-world enterprise data-analysis questions, Genie with Ontology answered 84.5% correctly on the first attempt. The strongest general-purpose coding agent in the same evaluation scored 52.4%. Genie was also roughly twice as fast as that agent. That's an internal benchmark rather than a universal accuracy guarantee, but it illustrates the core principle: better enterprise context can matter as much as, or more than, simply giving the model more time to reason.

Do you need to build a formal ontology from scratch?

Richard Tomlinson: No, and requiring that would recreate the scalability problem we're trying to solve. Most companies have already created a large amount of their business understanding. It exists in metric definitions, certified data, dashboards, queries, notebooks, documentation and the repeated ways teams use those assets.

The goal should be to preserve human control over the concepts that matter most while automatically learning much of the long tail. WithGenie Ontology, that means explicitly modeling critical KPIs and business terms while the inferred layer learns additional definitions, rules, relationships and authoritative sources from existing work. You get value from the knowledge the organization already has, rather than waiting for a separate ontology project to finish.

## What role does governance play in an ontology-grounded AI agent?

How does governance fit into an ontology-grounded agent?

Richard Tomlinson: Governance has two jobs. The obvious one is access: the ontology should never become a back door around existing permissions. If a user can't access the source information, the agent shouldn't be able to retrieve context derived from it. With Genie Ontology, permissions are enforced during retrieval, using the governance of the underlying sources, includingUnity Catalog. Two employees can therefore ask the same question and appropriately receive different answers based on what each is authorized to see.

The second job is just as important: governance helps AI understand what to trust. Certification, authoritative definitions, lineage, usage, expertise and source provenance become signals that help distinguish the official revenue definition from a one-off calculation someone created six months ago. In the AI era, governance is no longer only about controlling data. It's increasingly part of the mechanism that teaches AI which business knowledge deserves authority.

## Why is data ontology becoming AI infrastructure?

The word "ontology" used to belong to semantic modeling teams and taxonomy debates. It's quickly becoming something closer to infrastructure: the layer that decides whether an agent's answer reflects how the business actually works, or just a plausible guess dressed up as one. Organizations that treat context as something to be governed and continuously learned, not documented once and left to go stale, will be the ones whose agents can be trusted to act, not just report.

See how Genie ontology grounds AI answers in what your business actually means.Explore Genie.

Read next:

- Introducing OfficeQA: A Benchmark for End-to-End Grounded Reasoning
- Introducing OfficeQA Pro V2: A New Benchmark for Enterprise Grounded-Reasoning
- Genie One product page
- Genie Ontology overview

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Data Ontology defined: The context layer your AI agents are missing](https://www.databricks.com/blog/data-ontology-defined-context-layer-your-ai-agents-are-missing)
> 
> 翻译时间：2026-09-22 07:37
