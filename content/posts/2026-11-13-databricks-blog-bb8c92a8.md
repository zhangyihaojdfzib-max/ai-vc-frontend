---
title: 'OpenAI and Databricks: Enterprise AI on your governed data'
title_original: 'OpenAI and Databricks: Enterprise AI on your governed data'
date: '2026-11-13'
source: Databricks Blog
source_url: https://www.databricks.com/blog/openai-and-databricks-enterprise-ai-your-governed-data
author: ''
summary: '[翻译失败，原文如下]


  - OpenAI brings frontier intelligence. Databricks brings enterprise data, context,
  and governance. Together, they help enterprises deploy...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-14T08:49:37.005963'
---

[翻译失败，原文如下]

- OpenAI brings frontier intelligence. Databricks brings enterprise data, context, and governance. Together, they help enterprises deploy AI that understands the business and can act on it.
- Three enterprise adoption patterns: accelerating work for business users with ChatGPT and the Genie plugin, coding with enterprise-level governance through Codex and Unity Gateway, and transforming business processes with GPT models and Databricks Apps.
- Ali Ghodsi, co-founder and CEO of Databricks, and Greg Brockman, co-founder and president of OpenAI, discussed best practices for rolling out enterprise AI

Greg Brockman, co-founder and President of OpenAI, has a simple way to describe AI without company data: “it's like hiring someone with 20 PhDs and never inviting them to a meeting.”

Enterprises want to use frontier OpenAI models on the business data they already govern in Databricks, and they want to roll AI out to far more of their employees. OpenAI and Databricksformed their partnershipto make that possible. OpenAI builds the frontier models, Codex, and ChatGPT that people use every day. Databricks provides the context those tools need to work inside a company: governed data, business definitions, and access rules. Genie Ontology is the context layer in Databricks that holds those definitions and shows how the company's data fits together, so ChatGPT using Genie knows what “revenue” or “active customer” means at your company before it starts working.

Ali Ghodsi, co-founder and CEO of Databricks, and Greg Brockman, discussed the shift from chatbots to autonomous agents, and what enterprises need to get real value from them, in a conversation released earlier this week. You can watch it below.

## Three key enterprise adoption patterns

Most companies start with OpenAI and Databricks in one of three ways:

1. Accelerate work for business users
2. Coding with enterprise-level governance,
3. Custom agents that transform business processes.

Each one is covered below.

![image3.png](/images/posts/949b987c9836.png)

### 1. Accelerate work for business users with ChatGPT and the Genie plugin

Historically employees who needed numbers to make decisions couldn’t write SQL, so they looped in analysts or pasted data into AI tools that didn't know the company's definitions. Waiting on analysts slowed decisions down, and answers built on the wrong definitions led to the wrong decisions.

Now, they can ask these questions themselves in ChatGPT using the Databricks Genie plugin. This lets a product manager ask questions like, “How is weekly active user adoption tracking against target by plan tier?” ChatGPT will use Genie to understand the company’s metric definitions, find the relevant data, run the query in Databricks and return results back in visual graphs and charts. The plugin runs on theGenie MCP. Where once decision-making was slow, now employees can act quickly and with greater confidence in the underlying data.

Genie uses Genie Ontology, the context layer in Databricks that stores a company's approved metrics, business definitions, and how its data fits together. Genie applies the company's own definitions, so revenue in ChatGPT matches revenue in the finance reports. Users only see data they already have permission to see, and each answer links to its sources in Databricks.

Because ChatGPT has the business context from Genie Ontology, it can do more than answer. Users can ask ChatGPT Work for recommended next steps and who should be involved, share findings through Slack or email, and carry out the actions they approve through connected tools.

![image5.png](/images/posts/b93af7434ce7.png)

To get started, install theDatabricks Genie pluginin ChatGPT.

### 2. Coding with enterprise level governance using OpenAI Codex and Databricks Unity Gateway

AI coding agents usually spread one team at a time, and leaders lose track of who uses them, what they cost, and where code and data end up. Databricks Unity Gateway makes it easy to manage this rollout allowing a company to give OpenAI Codex to every engineer while keeping visibility and control. Developers use Codex as they do today. Codex signs in with a Databricks credential, the OpenAI key stays in the Gateway, and every request is logged. Engineering leaders set budgets, review spend by team, and pick which GPT model handles which task.

![image2.png](/images/posts/4f366dd4b4b6.png)

To get started, install the Unity Gateway CLI and run ug codex. The steps are inConnect Codex to Unity Gateway.

### 3. Transform business processes with OpenAI GPT models, Model Serving and Databricks Apps

Agents that could change core business processes often stall before production, because the data they need sits behind strict security and governance rules. On Databricks, OpenAI frontier models run next to that data under Unity Catalog governance. When Databricks serves the model, there is no external API key to manage. Teams can build and evaluate agents in Agent Bricks, or write them with the OpenAI Agents SDK and deploy them as Databricks Apps.

![image6.png](/images/posts/6f1d64d5f2f0.png)

To get started, open your Databricks workspace, go to + New > App, and choose the Agent - OpenAI Agents SDK template. Theagent quickstartwalks through it.

## How the OpenAI and Databricks partnership fits together

Behind the three patterns is one partnership. Here are the key facts, how the platform fits together, and the other integrations available today.

### Key facts about the OpenAI and Databricks partnership

### The joint architecture

OpenAI models, Codex, and ChatGPT connect directly to Databricks, and several Databricks products run on OpenAI models. Databricks gets early access to new OpenAI models, and OpenAI models lead on OfficeQA, a Databricks benchmark for real document work.

![image1.png](/images/posts/f867e295df09.png)

ChatGPT is where employees ask questions and get work done, Codex is where engineers write and review code, and Databricks Apps hosts the custom agents and apps that teams build. OpenAI frontier models do the reasoning in all three. Databricks Model Serving runs GPT models next to company data, so teams can call them from SQL, notebooks, and agents without managing a separate API key. Unity Gateway routes every model request, sets budgets by team, and keeps an audit log. The Genie plugin answers business questions in ChatGPT and Codex and gives them the business context from Genie Ontology to act on: the company's definitions, its data, and each person's access rights. The Lakehouse stores company data under Unity Catalog governance, and Lakebase, a managed Postgres database, keeps memory and state for agents.

### Other OpenAI and Databricks integrations

The two companies have also built these integrations:

## What's next

We'll publish a separate post on each pattern over the next few weeks, with architecture details, setup steps, and customer lessons. Teams that already work in ChatGPT and Codex can start with the Genie plugin and Unity Gateway. Teams that build in Databricks can start with OpenAI GPT models there. The same Unity Catalog permissions and Unity Gateway cost controls apply in every case.

### What is the OpenAI and Databricks partnership?

OpenAI and Databricks work together so enterprises can use OpenAI models and tools on governed business data & context in Databricks. OpenAI provides GPT models, Codex, and ChatGPT, and Databricks provides the data platform and governance.

### How do I connect ChatGPT to my Databricks data?

Use the Databricks Genie plugin, which runs on the Genie MCP. A Databricks admin turns on Genie, and users then connect it to ChatGPT. Each person sees only the data they're allowed to see.

### How does Databricks Unity Gateway govern OpenAI Codex?

[翻译失败，原文如下]

Codex sends its requests through Unity Gateway instead of calling OpenAI directly. Developers sign in with a Databricks credential while the OpenAI key stays in the Gateway. Leaders can set budgets and see spend by team, and every request is logged.

### Can I build AI agents with OpenAI models on Databricks?

Yes. Agent Bricks lets you build and evaluate agents, or you can also write agents with the OpenAI Agents SDK and deploy them as Databricks Apps. No external API key is needed when Databricks serves the model.

### Which OpenAI models are available on Databricks?

Databricks serves recent OpenAI GPT models, including the GPT-6 family, and the open-weight gpt-oss models. Thesupported models listshows what's currently available.

See the Databricks Genie plugin at work inside ChatGPT.

Partners

---

> 本文由AI自动翻译，原文链接：[OpenAI and Databricks: Enterprise AI on your governed data](https://www.databricks.com/blog/openai-and-databricks-enterprise-ai-your-governed-data)
> 
> 翻译时间：2026-11-14 08:49
