---
title: What is AI analytics? Why it only works on governed data
title_original: What is AI analytics? Why it only works on governed data
date: '2026-09-15'
source: Databricks Blog
source_url: https://www.databricks.com/blog/what-ai-analytics-why-it-only-works-governed-data
author: ''
summary: '[翻译失败，原文如下]


  - AI analytics isn''t BI with a chatbot bolted on. It shifts who does the analytical
  work, from a human navigating dashboards to a system ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-22T07:37:49.317435'
---

[翻译失败，原文如下]

- AI analytics isn't BI with a chatbot bolted on. It shifts who does the analytical work, from a human navigating dashboards to a system that can understand intent, investigate, and increasingly act on its own.
- Trustworthy AI analytics depends on four things: governed data, shared business context, permission-aware execution, and verifiable evidence. Better models alone don't get you there.
- Fragmented business definitions were always a BI problem. AI turns it into a bigger one, because the system now has to resolve organizational disagreements on its own, and the wrong answer can look completely reasonable.

AI analytics is the practice of applying artificial intelligence and machine learning to data analysis, enabling systems to surface patterns, generate insights, and answer questions in natural language without manual query-building. It shifts analytics from retrospective dashboards toward automated, conversational, and predictive workflows that a broader set of business users can act on directly.

Every BI vendor can demo a natural-language query today. Ask a question, get a chart, look impressive in a room. The harder question, the one that separates a category-defining platform from a good demo, is what happens when that same system meets a real enterprise: conflicting metric definitions, five tables that could plausibly answer the question, and a user who technically shouldn't see half the underlying data.

Richard Tomlinson leads product marketing for Databricks' business intelligence and analytics products. In this conversation, we talked through what changes when BI becomes AI-native, why governance turns out to matter more with AI rather than less, and what a data leader should be asking vendors instead of which foundation model they use.

## How is AI analytics different from traditional BI?

BI has always been able to tell you what happened. What's actually different about AI analytics, and why is it more than just BI with a chatbot bolted on?

Richard Tomlinson:Good BI has always helped people understand more than simply what happened. The real limitation is that traditional BI generally requires a human to navigate the analytical path. Someone has to decide which dashboard to open, which filters to apply, which dimensions to drill into, what follow-up query to run, and often when to involve an analyst.

AI analytics changes who does that work. Instead of presenting a predefined view of the data, an AI-powered system can understand the intent behind a business question, determine what data and business context are relevant, generate and execute the necessary queries, and increasingly conduct a multi-step investigation on the user's behalf.

That last part is where agentic analytics becomes important. If I ask, "Why did margin fall in the Northeast last quarter?", an agentic system doesn't have to translate that into one SQL query and return a chart. It can form hypotheses, investigate product mix, discounting, customer segments, or costs, learn from each result, and synthesize the evidence into an explanation.

So the evolution is roughly:

- Dashboards: show me what we already decided to measure.
- Conversational analytics: let me ask a new question.
- Agentic analytics: investigate the question for me.

That's a much more fundamental shift than putting a chat box on a dashboard.

So if dashboards show what happened, what does that investigation surface? What can AI-powered analytics tell a decision-maker that a dashboard never could?

Richard Tomlinson:The biggest change is moving from observation toward investigation. A dashboard might tell a retailer that gross margin is down three points. That's useful, but it still leaves the decision-maker asking why.

An AI-powered system can investigate whether the decline is concentrated in particular stores, products, or customer segments, test whether discounting changed, determine whether product mix shifted, compare the timing against promotions or supplier changes, and synthesize those findings into an explanation. The valuable output isn't another chart. It might be something closer to:margin is down primarily because a higher proportion of sales shifted toward two heavily discounted product categories in the Northeast, while unit volume and acquisition remained stable.That's much closer to the information a decision actually requires.

I'd describe the progression as: what happened, what changed, why did it change, what should I investigate or decide next. And I'd stop short of implying that every AI analytics system can autonomously make or execute the decision itself. The meaningful near-term advance is dramatically reducing the analytical work required to get from a signal to a well-supported decision.

## What does it mean for AI to interpret data semantically?

You've talked about AI analytics interpreting data semantically. What does that mean in practice?

Richard Tomlinson:AI analytics absolutely still queries data. The difference is that it needs to understand what the datameansbefore deciding how to query it.

A database can tell an AI system there's a column called net_rev, another called bookings, and a relationship between two tables. It can't tell it what the company means by "revenue," whether executives use booked or recognized revenue, which fiscal calendar applies, which customer hierarchy is authoritative, or whether cancelled orders should be included. Those are semantic questions. They're the business meaning that sits between a user's language and the physical data.

In practice, a strong AI analytics system needs governed definitions of metrics and KPIs, dimensions and relationships between business entities, the terminology and synonyms the business uses, business rules and calculation logic, authoritative sources, permissions and governance, and often institutional knowledge captured from how people have historically used the data. That context is what lets the system translate "How are enterprise renewals performing?" into the right interpretation ofenterprise,renewal, andperformingbefore it ever constructs a query.

This is why semantics become more important with AI, not less.

## How do you make AI-generated analytics trustworthy?

If a data leader asked you point-blank, "how do I make AI-generated analytics trustworthy?", what's your honest answer?

Richard Tomlinson:Don't start with the model. Start with the foundation the model is allowed to reason over. I think trustworthy AI analytics comes down to four things.

First, trustworthy data: the AI needs governed access to the same enterprise data you'd trust for an executive report, not copies exported into a separate AI environment. Second, trustworthy business context: shared definitions for the metrics, entities, and terminology that matter to the business. Giving an LLM a database schema isn't the same thing as teaching it how the business works. Third, trustworthy execution: governance and permissions need to carry through from the user to the data. An AI system shouldn't circumvent existing access controls just because someone asked a question in natural language. Fourth, verifiability: users and data teams need evidence they can inspect, the source data, the calculations or queries behind the answer, citations where appropriate, and a way to evaluate answers systematically against known-good questions.

That last point matters even more as analytics becomes agentic. A single bad query produces one wrong answer. An agent can make multiple analytical decisions during an investigation, so you need mechanisms for grounding and validating that whole process, not just the final output.

The key idea is that trust is a system property, not a model property. A more capable LLM alone doesn't make enterprise analytics trustworthy.

Why does it fall apart when it isn't grounded in governed data? What goes wrong, concretely?

[翻译失败，原文如下]

Richard Tomlinson:I'd make one distinction here: governance is necessary, but it isn't sufficient on its own. You can have perfectly governed data and still get a confidently wrong answer if the AI doesn't understand what that data means.

Without a governed foundation, several things can go wrong at once. The system may select an outdated table instead of the certified one. Two users may get answers calculated from different versions of the same KPI. Sensitive information may be exposed to someone who shouldn't see it. And when an answer looks wrong, the data team may have no reliable way to trace which data or calculation produced it.

AI amplifies these problems because it dramatically expands who can query data and how many questions can be asked. Previously, ambiguity might have meant an analyst asked for clarification. An AI system can instead make a plausible assumption and confidently continue.

That's why the foundation needs governanceplussemantics: control over what data can be used and who can access it, and a shared understanding of what that data means. The goal isn't merely to stop hallucinations. It's to make sure AI-generated analytics operate under the same definitions, permissions, and standards of evidence the organization already expects from human-generated analytics.

## What happens when teams define the same metric differently?

A lot of organizations have different business definitions living in different BI tools. What's the risk once AI enters the picture, and how should a data leader think about standardizing those definitions?

Richard Tomlinson:AI turns a long-standing BI problem into a much larger one. Organizations have always struggled with competing definitions of things like revenue, active customer, churn, or conversion. With dashboards, those inconsistencies are at least relatively bounded. Finance has its dashboard, Sales has another, and people eventually learn which one to use.

AI removes those boundaries. A user simply asks, "What was revenue last quarter?" Now the AI has to decide which definition, dataset, and calculation represents the organization's intended meaning. If those definitions are fragmented across individual BI tools, semantic models, and dashboards, the AI is effectively being asked to resolve an organizational disagreement on its own. That's dangerous, because the answer may still look completely reasonable.

The answer isn't necessarily one gigantic semantic model that tries to describe the entire company. It's moving critical business meaning into shared, governed semantic definitions that live close to the underlying data and are reusable across analytical and AI experiences. That becomes even more important as companies deploy more AI agents. You don't want every dashboard, copilot, and agent independently learning what "net revenue" means. You want them all drawing from the same shared business context.

This is one of the biggest architectural changes AI creates for analytics: semantics can no longer live exclusively inside the presentation layer.

### The agentic AI playbook for the enterprise

![ai](/images/posts/739dac6fa259.png)

## Why do users need to see how an AI reached its answer?

Beyond accuracy, why does it matter that a business user can see how the AI arrived at an answer, not just the answer itself?

Richard Tomlinson:Because analytics isn't only about getting an answer, it's about having enough evidence to make a decision from that answer. If an AI tells a sales leader enterprise churn increased 14%, the natural next questions are: compared with what period, which customers are included, how is churn defined, what data supports that conclusion, and can I drill into it? A trustworthy system should make those questions answerable.

I'd be precise about what "show how the AI got there" means. It doesn't mean exposing the model's private reasoning or chain of thought. What users need is provenance and evidence: the data sources used, the calculations or queries executed, relevant citations, supporting tables and visualizations, and the assumptions that materially affect the result.

This matters even more with agentic analytics. If an agent performs a ten-step investigation, the user shouldn't have to blindly trust the final paragraph. They should be able to inspect the evidence behind the important conclusions. Transparency also changes user behavior. It turns AI from an oracle into an analytical partner. People can challenge an answer, investigate further, and decide for themselves whether the evidence is strong enough to act on.

## How does an AI analytics system decide which data source to trust?

When there are multiple plausible answers or sources, how does your AI know what to trust?

Richard Tomlinson:Almost every vendor can show an impressive natural-language demo. The hard part is what happens when the real enterprise environment is messy. What if Finance and Sales calculate revenue differently? What if there are five tables that could answer the question? What if one source is certified and another was created yesterday? What if the person asking only has permission to see some of the underlying data?

The vendor should be able to explain how its system understands business definitions, determines source authority, applies user permissions, handles ambiguity, and shows evidence for the resulting answer. If the answer is essentially "the LLM figures it out," I'd be very cautious. For agentic systems this becomes an even bigger issue, because the system isn't making one retrieval decision, it may be making dozens of decisions about what data to examine and what hypothesis to pursue.

That question gets much closer to whether an AI analytics platform will survive contact with a real enterprise than asking which foundation model it runs on.

## Do better AI models remove the need for business context?

What's something most data leaders currently believe about AI analytics that you think is wrong or overstated?

Richard Tomlinson:The biggest misconception is that better AI models will eliminate the need to model and curate business context. The opposite is happening. LLMs are remarkably good at understanding language and reasoning over information, but they can't infer an organization's private business definitions with certainty. They don't inherently know which of your five revenue calculations the CFO considers authoritative, what "active customer" means at your company, or which dataset should be trusted for a board meeting. As AI becomes more capable and more autonomous, that context becomes more important, because the AI is making more decisions on the user's behalf.

A second misconception is that AI makes dashboards obsolete. I don't think it does. Dashboards remain extremely effective when you know what you want to monitor: revenue, pipeline, utilization, churn, inventory, service levels. AI becomes most powerful when the question isn't already encoded in the dashboard, particularly when someone asks why, wants to explore an unexpected change, or needs an investigation spanning multiple dimensions.

The future of BI isn't chat instead of dashboards. It's a continuum in which dashboards handle known questions, conversational analytics handles ad hoc questions, and agents increasingly handle complex investigations. That's a more credible definition of the next generation of BI than simply replacing every dashboard with a chatbot.

## AI analytics doesn't remove the hard work of BI, it relocates it

The thread running through all of this is that AI analytics doesn't remove the hard work of BI, it relocates it. The work of defining metrics, governing access, and agreeing on what "revenue" means doesn't go away when you add a natural-language interface. It becomes more important, because the system is now making judgment calls a human analyst used to make, at a scale no analyst team could match.

[翻译失败，原文如下]

For data leaders evaluating AI-first platforms, the question isn't whether the demo looks good. It's whether the system underneath it, the governed data, the shared semantics, the permission-aware execution, the verifiable evidence, was built to survive contact with a messy, real enterprise. That's the foundation that turns AI analytics from an impressive query engine into something that can be trusted to inform a decision.

See how AI-powered dashboards and conversational analytics work directly on governed data. ExploreDatabricks AI/BI

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[What is AI analytics? Why it only works on governed data](https://www.databricks.com/blog/what-ai-analytics-why-it-only-works-governed-data)
> 
> 翻译时间：2026-09-22 07:37
