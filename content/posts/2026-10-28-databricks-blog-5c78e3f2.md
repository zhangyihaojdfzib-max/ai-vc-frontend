---
title: Voice Agents are here. Context turns them into real customer value.
title_original: Voice Agents are here. Context turns them into real customer value.
date: '2026-10-28'
source: Databricks Blog
source_url: https://www.databricks.com/blog/voice-agents-are-here-context-turns-them-real-customer-value
author: ''
summary: '[翻译失败，原文如下]


  *Voice is already changing how customers interact with brands. People who moved
  from storefronts to websites to apps now expect to simply...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-29T08:15:51.589957'
---

[翻译失败，原文如下]

*Voice is already changing how customers interact with brands. People who moved from storefronts to websites to apps now expect to simply talk to the companies they buy from, and the same shift is reaching suppliers, drivers, and field teams.*Most enterprise AI so far has faced inward. The larger opportunity is in the conversations companies have with customers and partners every day, and each of those conversations can now be captured, understood, and acted on in real time.*Any team can build a voice agent that talks back, but value is created only when the agent has context on who is calling. From there, it can adapt to that person, stay within set rules, and get better with every call.*On Databricks, the agent's brain sits next to your governed data. Context and ontology ground every answer, fast AI decisions tailor each turn, and every call feeds a learning loop.*Getting started is straightforward. Pick one high-volume routine call, measure how well the agent handles it, and use the DIVA blueprint as the starting point for the next one.

## Why voice, and why now

Consider three moments that happen every day in consumer businesses:

- At 6 a.m., a driver running late for a delivery window calls dispatch to move his dock appointment. He’s behind the wheel, so an app isn’t an option. Three other drivers are already on hold, and every minute he waits puts the next delivery at risk.
- At noon, a drive-thru has four cars in line and one employee on the headset, who is also taking payment and handing out orders. Guests can only order by speaking, so the line moves only as fast as one employee can facilitate orders.
- In the evening, a storm grounds flights, and stranded travelers call their hotel to hold rooms and push back arrivals. Standing at a gate with a bag in each hand, a phone call is easier and faster than a website. The reservations team has two people and forty calls coming in.

In each of these moments, voice is the fastest or only way the customer can reach the business. So if voice ultimately serves the customer and business need most effectively, why is it so often not available or, in more recent times, executed poorly?

For years, the answer was that voice was too hard to get right. That is no longer true. Synthetic voices now sound natural, a conversation can be turned into text and acted on while the caller is still on the line, and today's voice agents can keep pace with the roughly200 millisecondsit typically takes people to answer each other in conversation.

What has not caught up is how most companies think about it. Enterprise AI investment has largely faced inward, toward assistants for employees, while the larger opportunity sits in the conversations companies have with customers and partners every day. One of the largest quick-service restaurant brands in the United States is already building toward exactly that, with a voice agent that lets guests add items to their cart, change their order, and check out simply by talking.

![](/images/posts/be1ec0bb07e9.png)

Example use cases where voice agents can create value.

Every one of these calls, from the driver moving a dock appointment to the traveler holding a room after a storm, depends on more than understanding speech. To be useful, the agent needs the same context your best employee would have: who is calling, what is already in motion for them, and what it is allowed to do about it.

## The missing piece is knowing your customer

Most voice agent pilots prove that an agent can hold a conversation. Far fewer prove that it can be trusted with a real customer. Context closes that gap. With it, the agent can adapt to each caller, stay within your rules about what it can see and say, and get better with every call. Without it, even the most natural voice can only give generic answers.

Consider a single call. A loyal customer phones about a late order. The agent already knows who they are, what they ordered, and where the package is. It apologizes, offers a loyalty credit it is authorized to give, and arranges a replacement. If the customer is still frustrated, the agent picks up on it in the moment and decides, in a fraction of a second, to route the call to the next available person. That person picks up with the full context, so the customer neither waits in a queue nor repeats themselves. The same pattern holds when a patient moves an appointment or a subscriber cannot log in after a charge they don't recognize. In each case, the agent picks up when the customer steps away from the app or website and needs an answer now, then hands them back to that same journey when the call is done.

Pulling that context together on a live call is the real challenge. It lives across many systems, the agent needs it in a fraction of a second, and it has to stay governed the whole time. That is where Databricks comes in.

## The brain behind the voice agent: context, ontology, and governance on Databricks

![](/images/posts/299240289fac.png)

A voice agent has two parts. The first is theconversation layer, which handles the call itself: carrying the audio, turning speech into text, and speaking the reply. Specialist partners do this well. In our prototype,LiveKitcarries the call,Deepgramhandles speech-to-text and the default voice, andElevenLabsadds expressive voices. Phone carriers such asTwiliocan bring in regular phone lines.

The second part isthe brain, which Databricks provides. On every turn of the call, it looks up the caller’s context, applies your business rules, and chooses the next step, whether that means answering a question, making an offer, or handing the call to a person. It also records each decision so your teams can review it later. The conversation layer shapes how the agent sounds. The brain decides whether it gets the answer right.

The brain stands on a foundation of three things that already live together on Databricks.

- Contextis the data the agent needs at the moment: the customer, order, product, and policy data that belongs to the person on the line.
- Ontologyis how that data connects. It captures the definitions and relationships your business runs on, such as what makes someone a loyalty member, which store an order belongs to, and which policy applies to which product, so the agent can reason about your business the way your employees do.
- Governancedecides who can see what. On Databricks, an AI agent follows the same access rules in yourenterprise data catalogthat your employees already follow.

For Databricks customers, there is no new platform to stand up. The agent runs where your data already lives and connects to the systems you already run, such as ordering, loyalty, and CRM, through approved, read-only lookups.

### Pillar 1: Grounding every answer in your business

During a customer interaction, the agent uses your context and ontology to look up this person’s orders, your policies, and your product information, so every answer reflects your business rather than general knowledge from the internet. The agent only sees the records that belong to the caller, and it confirms who they are by checking your systems rather than taking their word for it. Your business decides which offers the agent can make, how much credit it can give, and the point at which a person takes over.

If the agent cannot find the answer in your data, it tells the caller so and transfers them to a person rather than guessing. Every answer it does give can be traced back to the record it came from. Sensitive topics, such as medical, financial, or safety questions, are routed to a human by design, and the agent is built never to give medical advice. Only the conversation passes through speech partners, and customer data stays on your governed platform.

### Pillar 2: Tailoring every conversation with fast AI decisions

[翻译失败，原文如下]

A voice agent needs two kinds of thinking. Some decisions have to happen in a fraction of a second, like whether a driver with a dock problem or an upset caller should go to a person right now. Others need careful reasoning, like working out the right fix for a delayed order. Researchers call thisfast and slow thinking, or System 1 and System 2, and AI is now being built the same way. Large language models (System 2) do the careful reasoning, while a new class of fast decision models (System 1), such as Jev fromTypeSafe AI, handles the quick calls. Databricks brings System 1 decision making to your governed data withai_decide, so the agent can make a quick call and show how confident it is.

In a voice agent, the two work side by side on every turn of the conversation.

- A loyal member or returning guest gets their full history and the offers they qualify for, backed by your most capable model, while a routine question gets a quick, accurate answer at lower cost.
- An upset caller is handed to a person, along with the order or reservation, any earlier complaints, and any offers already made.
- A caller who switches languages hears the agent switch with them.
- A subscriber who sees a charge they don't recognize and can't log in is verified against your records and moved straight to account recovery, instead of waiting in a general queue.
- A subscriber who calls to cancel hears the save offer they actually qualify for, at the moment it can still change their mind.
- A patient who asks whether a symptom is serious is transferred to a nurse with the full transcript.
- A driver reporting a dock incident is escalated immediately, before it costs you a shipment.

This lets you use your most capable models where they make a real difference to the customer, and faster, lower-cost models for everything else.

### Pillar 3: Creating a learning loop with every call

Every one of those decisions is recorded. With caller consent and recording disclosure handled at the phone layer, each call can be captured in one governed place: what was said, what was looked up, which model answered, and why each decision was made. Your teams control who can access those records and how long they are kept, using the same policies that already govern the rest of your data. The agent inherits the Databricks platform's security and compliance programs, includingHIPAAandSOC 2 Type IIoptions, described in theDatabricks Trust Center. Speech partners carry their own certifications that need to be reviewed as part of your rollout.

That record is what lets the agent improve. Every call can be scored for quality automatically, and contact center and customer experience leaders can ask questions about their calls in natural language, such as why refund requests spiked last Tuesday. Those insights can then be fed back into better prompts and models, further improving the effectiveness of the voice agent.

## Getting started with voice agents on Databricks

Getting started does not require a large program. The building blocks are available today, and theDatabricks Intelligent Voice Agents (DIVA) blueprint, which is open source on GitHub, gives your teams a working starting point. Voice then becomes a new channel on top of the systems you already have.

The voice agent is there to take on the routine calls that fill the queue, such as order status, refills, and rebookings, so your staff can focus on the conversations that need a human: an upset customer, a complex request, or a caller who would simply rather talk to a person. When a staff member picks up, the full history is already on their screen, and if anything goes wrong, the call moves to a person with the full transcript.

This is where customer service is heading.Gartnerpredicts that by 2029, agentic AI willautonomously resolve 80% of common customer service issueswithout human intervention, leading to a30% reduction in operational costs.

Databricks industry engineers recommend starting with a 90-day pilot that covers one channel, one team, and your highest-volume routine call, such as order status, a driver check-in, or a supplier confirmation. Before the pilot begins, record today's cost per call, handle time, and customer satisfaction, and track whether callers come back and buy again, so you can compare the results at the end. Once the results hold up, you can extend the same governed setup to more locations and more types of calls.

Three questions for your next leadership meeting

1. Which customer and partner conversations do we handle most often, and which of them could an agent answer accurately today?
2. If a voice agent answered on our behalf tomorrow, would it know who it was talking to, and would it follow the same rules as our employees?
3. Can we trace every decision an agent makes on a call and show that it was governed?

To see it in action, watch the full demo and share theDIVA blueprint on GitHubwith your technical team. It includes ready-made instructions that coding agents can follow. Then reach out to your Databricks account team to discuss and brainstorm your first use case.

Your customers will soon be talking to an AI agent on your behalf. What matters is how well that agent knows them.

Retail & Consumer Goods

---

> 本文由AI自动翻译，原文链接：[Voice Agents are here. Context turns them into real customer value.](https://www.databricks.com/blog/voice-agents-are-here-context-turns-them-real-customer-value)
> 
> 翻译时间：2026-10-29 08:15
