---
title: How partners use Genie's free tier on Azure Databricks
title_original: How partners use Genie's free tier on Azure Databricks
date: '2026-11-19'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-partners-use-genies-free-tier-azure-databricks
author: ''
summary: '[翻译失败，原文如下]


  - Every Azure Databricks user gets $10 of free Genie usage a month, and Genie budgets
  let admins control any spend beyond it.

  - The Genie...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-20T09:31:29.573157'
---

[翻译失败，原文如下]

- Every Azure Databricks user gets $10 of free Genie usage a month, and Genie budgets let admins control any spend beyond it.
- The Genie ontology reduces AI spend by “saving the work” the whole company has already done in a governed memory.
- With smart routing and open-weight models, Genie keeps getting cheaper, and the more customers use it, the more efficient it becomes.

Every Azure Databricks user gets $10 of free Genie usage each month, usage that many AI tools charge for. And Genie is built to get cheaper as customers use it. The Genie ontology saves the work the whole company has already done, so Genie doesn't redo it for every question. Smart routing and open-weight models keep lowering the cost of each answer, and the more customers use Genie, the more efficient it becomes. Genie budgets let admins decide whether anyone spends beyond the free allowance. For partners, that turns the cost question into a reason to roll Genie out broadly.

If you advise customers on AI, you’ve likely seen this: once they experience what Genie can do, they want it everywhere, in front of every employee and not just a pilot team. What they need next is a path to scale it within cost boundaries. Some customers block consumption-based AI tools entirely, and others hold off on a trial because they worry about what happens to costs as usage grows.

That concern is reasonable. As AI moves from a few pilot users to the whole workforce, finance teams want predictable costs and clear guardrails before they say yes. Genie is built to meet that bar: every user gets free monthly usage so everyone can benefit, and budget controls are ready for when usage ramps.

For partners, that means you can help customers adopt AI across their enterprise without cost limiting the conversation. You can start broad with cost controls in place from day one, which builds trust and makes it easier to scale. Genie’s pricing also complements the Microsoft 365 investments customers have already made.

Which Genie experience fits each customer?

- Genie One:The AI coworker that gives every business user instant access to governed data and AI, with business context built in. For partners, it's the broadest entry point: roll it out to an entire customer org and let users ask questions in natural language, with no setup per user.
- Genie Agents:No-code agents where data teams set up trusted data, metrics and business rules that power Genie One answers. For partners, this is where delivery work lives: configuring the right tables, metrics and instructions so the customer's business users get accurate, governed answers.
- Genie Code:The autonomous AI agent that helps data teams plan, build and run data engineering, machine learning and AI workflows on Azure Databricks. For partners, it accelerates delivery: developers and data engineers use it to write, debug and ship pipelines faster.

All three are governed through Unity Catalog, so partners can match the right experience to each customer conversation and know the same access rules apply throughout.

### How much does Genie cost on Azure Databricks?

Every identified user gets $10 of free Genie usage each month, and it resets on the first of every month. Even better, through January 31, 2027, Genie One and Genie Agents are free for users, so the full $10 goes to Genie Code. After that, the $10 allowance is shared across Genie One, Genie Agents and Genie Code.

Budgets apply only to pay-as-you-go usage above the free allowance. They can't remove it, so every user keeps the same free starting point.

### Why Genie gets cheaper over time

Genie's cost story improves as customers use it:

- The ontology saves the work.Genie keeps the context the whole company has built, such as trusted data, metrics and business rules, in a governed memory, so answers don't have to be recomputed from raw data or documents every time.
- Smart routing and open-weight models.Genie sends each request to a cost-efficient model that can handle it, and open-weight models keep lowering the cost of each answer.
- More use, more efficiency.The more people use Genie, the more saved context it can reuse, so each answer gets more efficient.

### How Genie budgets control AI spend

Genie budgets live in the account console and give admins tools to monitor spending, set limits and manage billable Genie usage:

- Stay on the free allowance.Set a $0 per-user threshold with Block usage enabled. Users get their full free allowance, and Genie Code usage pauses once it runs out and resumes on the first of the month. Genie One and Genie Agents usage by users stays free through January 31, 2027.
- Add headroom per user.A $30 per-user threshold sets a monthly spending limit of $30 per user, on top of the free allowance.
- Set limits by group.Combine a shared threshold, a default per-user limit and higher overrides for specific users or groups.
- Alert before blocking.Use alert-only thresholds to watch usage trends before setting limits.

A few details are worth telling customers up front. Budgets track each user’s spend in near real time and block new requests once a threshold is reached. Because tracking is an estimate, actual spend can land slightly above or below the threshold, and requests already in progress finish. Budgets are built for near-real-time spend control rather than as an absolute cap, and warehouse compute is billed separately. Service principals don’t get the free allowance, so automated usage is billed.

Start with spend control, not a procurement cycle

Most enterprise AI projects begin with a business case and a procurement cycle. With Genie, customers can start with spend control instead: set the pay-as-you-go threshold to $0, roll Genie out broadly on the free allowance, learn how people actually use it and add budget only where the value is clear.

### How Genie works in Microsoft Teams and Microsoft 365 Copilot

Genie brings governed Azure Databricks data into Microsoft Teams, Microsoft 365 Copilot and Copilot Cowork, Excel and Copilot Studio, with Unity Catalog permissions applied throughout. Users ask questions where they already work, and the answers respect the same access rules as the rest of their data. TheAzure Databricks Genie Plugin, now generally available, gives partners a one-step way to bring Genie into a customer's Teams and Microsoft 365 Copilot environment, so the first conversation can happen in minutes.

For example, business users can ask questions about their company's data directly from Teams or Copilot, bring Genie results into Excel, or use Genie to power agents built in Copilot Studio. Some integrations are in preview and may require additional setup or licensing.

For partners, this opens opportunities to connect AI to existing business workflows, build new solutions and help customers get more value from their Microsoft and Databricks investments. Plugging Genie into Microsoft 365 Copilot doesn't mean paying twice: Copilot routes the questions Genie can answer to Genie, so customers avoid those costs on the Copilot side.

### What's in it for partners

[翻译失败，原文如下]

- A free starting point for every customer.Every user gets $10 of free Genie usage a month, and Genie One and Genie Agents are free for users through January 31, 2027, so partners can open the AI conversation without a cost hurdle.
- An answer to the finance question.Starting at a $0 pay-as-you-go threshold lets partners address cost concerns before they come up.
- Confidence to scale.Alert-only thresholds let real usage set the limits, so budgets are based on data rather than guesses.
- A way into Microsoft 365 conversations.Genie connects governed data to the tools customers already use.
- The right Genie for every audience.Genie One for business users, Genie Agents for the data teams who set up trusted data, and Genie Code for data engineers and developers.
- A cost story that improves over time.The ontology, smart routing and open-weight models make Genie more efficient as customers use it, so the cost case gets stronger as adoption grows.

For SIs:Genie is a low-friction way into every Microsoft 365 account. Open with a broad rollout at $0 in pay-as-you-go spend, then build services around it: budget and persona design, Unity Catalog governance, Genie setup and expansion into new use cases.

For ISVs:If your product works with Unity Catalog data, Genie can bring that governed data into Teams and Copilot for your joint customers.

Learn:Manage budgets and cost controls for Genie, theGenie consumption guideand theGenie cost and budgets FAQ

For partners: Get enabled onGenieandAzure Databricksthrough partner training on the Databricks Partner Academy, and talk to your Databricks partner team or Partner Solutions Architect about demos and co-sell.

### Is Genie free on Azure Databricks?

Genie has a free monthly allowance, but it isn't unlimited. Through January 31, 2027, Genie One and Genie Agents are free for users. Every identified user also gets $10 of free Genie Code usage each month. After that date, the $10 monthly allowance is shared across Genie One, Genie Agents and Genie Code. Each user has their own allowance, and it resets on the first of every month. Usage above it is billed pay-as-you-go, and admins can control that spend with Genie budgets. The allowance covers Genie's AI usage only. SQL warehouse compute is billed separately, and service principals don't get a free allowance.

### How do Genie budgets work?

Genie budgets let admins set spending thresholds in the account console for pay-as-you-go Genie usage above the free allowance. Admins can set shared, per-user and group thresholds, use alert-only thresholds or block usage once a threshold is reached. Budgets can't remove a user's free allowance.

### Can admins keep users on the free allowance only?

Yes. Set a $0 per-user threshold with Block usage enabled. Users get their full free allowance, and Genie Code usage pauses once it runs out and resumes on the first of the month.

### Are Genie budgets a hard spending cap?

No. Budgets track each user's spend in near real time and block new requests once a threshold is reached, but tracking is an estimate, so actual spend can land slightly above or below the threshold. Requests already in progress finish, and warehouse compute is billed separately.

### Does Genie work in Microsoft Teams and Microsoft 365 Copilot?

Yes. Genie brings governed Azure Databricks data into Microsoft Teams, Microsoft 365 Copilot, Excel and Copilot Studio, with Unity Catalog permissions applied throughout. The Azure Databricks Genie Plugin gives partners a one-step way to add Genie to a customer's Teams and Microsoft 365 Copilot environment. Some integrations are in preview and may require additional setup or licensing.

### If I plug Genie into Microsoft 365 Copilot do I get billed twice for the same work?

No. First, the Genie ontology is a built-in cost saver, since the AI doesn’t have to compute answers from raw data or documents. Further, Copilot knows what Genie can answer and routes appropriate questions to Genie, avoiding those costs on the Copilot side. And because Genie is consumption-priced with no per-user license, customers don't pay for a second set of user licenses either.

Genie,Unity CatalogandPartners

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[How partners use Genie's free tier on Azure Databricks](https://www.databricks.com/blog/how-partners-use-genies-free-tier-azure-databricks)
> 
> 翻译时间：2026-11-20 09:31
