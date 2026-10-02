---
title: Connecting customer context to measurable ROI with agentic marketing
title_original: Connecting customer context to measurable ROI with agentic marketing
date: '2026-10-01'
source: Databricks Blog
source_url: https://www.databricks.com/blog/connecting-customer-context-measurable-roi-agentic-marketing
author: ''
summary: '[翻译失败，原文如下]


  - Agentic marketing uses AI agents grounded in trusted customer, business, and decision
  context to recommend the next best action for eac...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-02T08:10:48.933521'
---

[翻译失败，原文如下]

- Agentic marketing uses AI agents grounded in trusted customer, business, and decision context to recommend the next best action for each customer, within guardrails that marketers set.
- Identity resolution becomes more important in an agentic model, because agents can only act as intended when grounded in real-time, governed context that connects known and anonymous signals.
- Measurement moves into the decision loop, where incrementality shows what changed because marketing acted and gives marketing and finance a shared basis for investment decisions.

Marketing leaders today face greater complexity than ever before. They work with more customer data, more channels, and more measurement tools than at any point in the discipline's history, while customer journeys have become less linear, with identity signals quickly decaying as people change devices and contact details. Marketers have spent the last two decades building commercial martech tools to keep pace - 15,000+ by martech expert estimates, not including the countless MCP integrations for agents (State of Martech 2026). Yet confidence in what is working has not kept pace, as each new system brings another copy of customer data, another set of definitions, and another handoff between teams.

Meanwhile, the economics of marketing are also changing. Value is shifting from an impression currency, where success is measured by reach and frequency, to a prediction economy - a new model that “rewards the ability to predict what a customer needs, act on it in the moment, deliver that personalized message, prove the business outcome that drove it, and then use that as the accelerant for what comes next,” explainsJake LaDuke, Global GTM Lead for Media, Entertainment & Advertising at Databricks. At the same time, consumers are beginning to use AI agents of their own to compare options and buy in seconds, shrinking the window for brands to predict, act, and measure the outcome.

But despite this mounting pressure, finance still needs to know whether marketing spend has created incremental revenue and margin, and whether the next dollar should stay in marketing, move to another growth lever, or return to the bottom line. The struggle for marketers becomes how to cut through the complexity to deliver answers that everyone can trust.

As AI and agents proliferate across every industry and line of business, they present a powerful opportunity for marketers to provide this clarity. With the right customer, business, and decision context, agents can recommend or take the next best action for each customer in near-real-time, within goals and guardrails defined by the marketers themselves. Each action is measured against what would have happened without it, and that result feeds back into the context used for the next decision. The end result is better decisions made consistently across millions of customer moments, and clear measurement showing those decisions drove incremental impact.

## Why identity resolution is the foundation of agentic marketing

An agent can only act as well as the context it is given; identity is what holds that context together.Zachary Van Doren, SVP of Product Strategy and Ecosystem atAcxiom, frames this as "identity powering the action.” Without this identity foundation, he says, “you don’t have context that is operational, that can be used by agents.” Identity resolution is often treated as a profile-building project with a finish line, but in an agentic model, its purpose is action: the ability to consistently recognize, engage, measure, and re-engage a customer across channels. A perfectly assembled profile that can't support those steps can’t deliver the best results.

The challenge, however, is that identity is constantly evolving. People move, switch devices, and change email addresses, and their behavior evolves along with their circumstances. Identity therefore has to be maintained continuously instead of resolved once and left alone. Brands also need to connect known customer records with pseudonymous intent signals, such as anonymous app sessions or ad exposure, without compromising privacy, governance, or consumer trust.

Even with a strong identity foundation, simply connecting signals to a persisted profile still isn't enough. The same customer may warrant a very different action depending on timing, recent behavior, channel, prior exposure to advertising, and the business objective at hand. Where and how someone is engaging matters just as much as who they are, which is why the old choice between person vs content-based targeting is giving way to a need for both. The most useful identity strategies focus on building better context for decisions, with a connected and persistent profile serving that goal.

Acxiom offers a useful example of how this foundation is being modernized. Working with Lovelytics, Acxiom rebuilt its data and identity services as a native application layer on Databricks, improving time-to-market for actionable customer insights byroughly 30%andreducing operational costs by about 15%.Acxiom's Real ID identity resolution enginenow also runs natively within Databricks, so brands can resolve and enrich customer data where it already lives instead of exporting it to a separate environment.

“Each of us brings a different piece,” saysJay Goebel, Practice Lead for Communications and Media atLovelytics. “Databricks brings the platform, Acxiom brings trusted identity, and Lovelytics brings the delivery experience to put it into production. As early launch partners for CustomerLake, we’re working together so marketers can act on customer context and prove what that action is worth.”

## The context agents need goes beyond a customer record

A traditional customer record captures who someone is and what they have done. For an agent to make a decision a marketer would stand behind, it needs four kinds of context.

- Customer contextcovers identity, behavior (historical and in-the-moment), preferences, consent status, and lifecycle stage.
- Business contextcovers growth objectives, margin implications, brand rules, inventory, and channel constraints.
- Decision contextcaptures the offers and actions a customer has already received, how they responded, and why earlier decisions were made.
- Controlis the layer of intent, guardrails, permissions, and approval points that people define and agents must respect.

The volume of that context adds up quickly. A single transaction can carry 30 to 50 metadata parameters, so one customer profile can easily run to thousands of columns of context, far more than any marketer can work through unaided.

From the marketer's point of view, a more complete profile only earns its keep when it improves a decision. That decision usually comes down to whether to engage at all, which message or offer is most relevant, which channel to use, and whether the action can create value without undermining the customer experience, the economics of the offer, or the customer's consent.

## A practical example: re-engaging a lapsed quick-service restaurant customer

Consider a frequent customer of a quick-service restaurant (QSR) brand who has stopped ordering but recently came back to browse the app. The reflexive move is to send another discount. A better approach starts with the decision the brand is actually trying to make. It works through five considerations:

[翻译失败，原文如下]

- The decision.Should the brand engage this customer now? If so, the options include a reminder, a different message, an incentive, a different channel, or some combination.
- The context.Purchase history is connected with pre-purchase signals, including app and website behavior, items viewed or left in a cart, previous offers, media engagement, lifecycle status, channel preferences, and communication permissions.
- The economic judgment.The brand needs to know whether an incentive would change behavior or simply subsidize an order the customer was going to place anyway. It also needs to know whether continued paid or owned media spend against this customer is still producing a return.
- The action and guardrails.The recommended message, offer, timing, and channel all operate within marketer-defined limits on eligibility, discount depth, contact frequency, consent, brand standards, and the points where human approval is required.
- The measurement.The brand determines whether the action produced an incremental order, revenue, margin, or repeat visit compared with taking no action, and that result goes back into the customer's context to inform the next decision across owned and paid channels.

Different customers in this situation call for different responses. If a customer who usually orders every Friday misses one week, then browses their usual order on Thursday, a well-timed reminder may be enough. If that same customer hasn't ordered in six weeks and is browsing a family meal without completing the order, an incentive on a bundle or a free side may help rebuild the habit. A customer who has seen repeated messages without responding may be signaling that the brand should change the message, switch channels, or stop spending against them for now.

A skilled marketing team can reason through all of this for one customer, but no team can apply the same care by hand to millions of customer moments every day. Agentic marketing is designed to close that gap by applying consistent, well-informed judgment at scale, keeping guardrails in human hands, and learning from every outcome.

## How an agentic CDP turns customer context into governed action

The customer data platform is where this shift is most visible in the marketing stack. Traditional CDPs help unify profiles and activate audiences, but they typically sit outside a company's core data and AI platform, which creates another copy of sensitive customer data to integrate, secure, and reconcile. Agents need governed access to identity, predictive models, business logic, activation endpoints, and performance signals in one place.

That’s the principle behindCustomerLake, the Agentic CDP from Databricks. CustomerLake is embedded in the Databricks lakehouse and governed byUnity Catalog, so marketing engagement and personalization operate on the same data and AI foundation the rest of the business already relies on. It is organized around two types of agents.

- Profile Agentsconvert fragmented customer data into business ready Customer 360 profiles. Using Agentic Identity Resolution, they blend deterministic, probabilistic, and agentic matching with Acxiom’s graph-based identity, hygiene, matching, and enrichment capabilities to create a complete and accurate view of each customer.
- Campaign Agentsuse governed customer context to build audiences, recommend next-best actions, activate across channels, and continuously optimize around business goals.

Marketers can use natural language to explore customer context and build audiences throughGenie, reducing the need to wait for custom data pulls. They define the strategy, goals, and guardrails that guide agent execution.

CustomerLake powers what Databricks calls Infinity Campaigns, which are always-on engagement loops that replace the cycle of building, launching, and rebuilding one-off campaigns. A marketer starts with a goal, such as reactivating lapsed customers. Agents then identify the right audience, account for eligibility or inventory constraints, recommend the next-best offer or channel, activate across destinations, and optimize or suppress based on performance.

CustomerLake is also designed to work with the identity, activation, measurement, and customer experience partners that brands already use, so trusted customer context can flow across channels without creating a new silo. It launched with an open partner ecosystem including Acxiom, and is supported by services partners including Lovelytics.

## Measurement and attribution in an agentic model

In many organizations, measurement arrives after the fact as a report on what a campaign delivered. In an agentic model, measurement becomes part of the decision loop. What the brand learns about an audience, offer, channel, or level of investment shapes the very next decision.

The concept of incrementality powers this flywheel, and it is also the most useful common language between marketing and finance. It separates the outcomes marketing activity was associated with from the outcomes that changed because the brand acted. Attribution, incrementality testing, and marketing mix modeling each contribute part of the picture, and conversational analytics can help teams explore what happened and why without waiting in a queue for custom analysis. Continuous learning also makes it easier to spot saturation and diminishing returns, and to recognize when investment should shift or activity should stop.

When finance is weighing whether the next dollar belongs in marketing, trade promotion, another growth lever, or the bottom line, CMOs generally need to demonstrate five things.

- Incremental impact:the revenue, margin, or customer behavior that changed because the brand acted, compared with taking no action.
- True profit contribution:the value that remains after media costs, discounts, trade spending, and offer economics are accounted for.
- Contribution by lever:whether marketing created demand, trade helped convert it, or the brand subsidized behavior that would have happened anyway, without giving several activities credit for the same outcome.
- Marginal return:where the next dollar still produces incremental value, and where reach, frequency, or promotional spend has hit diminishing returns.
- Customer value over time:whether the investment produced only an immediate transaction or also improved repeat purchase, retention, and lifetime value.

A measurement foundation built around these questions gives marketing, sales, and finance a shared view of what is creating value and where the next dollar can work hardest. AsDedra Berg, Value Realization Leader at Lovelytics, puts it, “These teams can now start from the same trusted foundation instead of spending half the meeting reconciling the numbers. The goal is not to prove that marketing should always win; it's to show where the next dollar can create the greatest incremental revenue and margin for the business.”

Identity is the final piece of the puzzle. When the same identity framework connects exposure, engagement, and outcome, a result can be traced back to the customer and the decision that produced, allowing the attribution loop to close.

## Where to start with agentic marketing

Few organizations begin with unified identity, clean customer data, and mature measurement already in place, and waiting for all three rarely makes sense. The most practical starting point is a single meaningful decision where better context and faster action could create measurable value. Reactivating lapsed customers is a common choice. Others include suppressing offers that subsidize purchases customers would have made anyway, or shifting spend away from audiences that have reached saturation.

[翻译失败，原文如下]

The sequence from there is fairly consistent. Define the decision and the business outcome it should impact, then assemble the required customer and business context. Set the guardrails and the points where people stay involved. Agree in advance on how incremental value will be measured, and use what you learn to improve the next decision before extending the approach to another use case. Early CustomerLake adopters are following a similar pattern, defining where agents are used first and expanding how much they automate as trust and results build.

The organizational work matters as much as the technology. Agentic marketing tends to succeed when marketing, finance, technology, analytics, privacy, and sales work closely together, when ownership of customer decisions, guardrails, and measurement is clear, and when teams move from isolated pilots toward repeatable workflows tied to business outcomes.

To learn more about transforming your brand with agentic marketing, watch the on-demand webinar →Know Your Audience. Act with Relevance. Measure What Matters

## Frequently asked questions

What is the difference between agentic marketing and marketing automation?Marketing automation executes rules and journeys that people design in advance. Agentic marketing uses AI agents that evaluate current customer and business context to choose the next best action within human-defined guardrails, including the option to take no action, and it uses measured outcomes to improve future decisions.

Why does identity resolution matter for AI agents in marketing?Agents make decisions based on the context available to them. Continuous identity resolution connects known and pseudonymous signals, such as transactions, app behavior, and media exposure, into a coherent view of each customer, which makes agent recommendations more reliable and their outcomes measurable.

What is an agentic CDP?An agentic customer data platform combines core CDP capabilities, including identity resolution, audience building, and activation, with AI agents that analyze customer signals, decide on next-best actions, and act across channels. Databricks CustomerLake is an agentic CDP embedded in the Databricks lakehouse and governed by Unity Catalog.

How do you measure the ROI of agentic marketing?The most reliable measure is incrementality, meaning the difference in revenue, margin, or customer behavior compared with taking no action. Attribution, incrementality testing, and marketing mix modeling each help explain performance, and feeding those results back into customer context allows each decision to improve the next.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Connecting customer context to measurable ROI with agentic marketing](https://www.databricks.com/blog/connecting-customer-context-measurable-roi-agentic-marketing)
> 
> 翻译时间：2026-10-02 08:10
