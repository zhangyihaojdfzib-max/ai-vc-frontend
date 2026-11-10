---
title: 'AI Product Management at Spotify: A View From Three Angles | Spotify Engineering'
title_original: 'AI Product Management at Spotify: A View From Three Angles | Spotify
  Engineering'
date: '2026-11-09'
source: Spotify Engineering
source_url: https://engineering.atspotify.com/2026/11/ai-product-management-at-spotify-a-view-from-three-angles/
author: ''
summary: '[翻译失败，原文如下]


  # AI Product Management at Spotify: A View From Three Angles


  ![Feature Image](/images/posts/c5bddf5e39c6.png)


  Almost every article or p...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-10T09:31:49.470214'
---

[翻译失败，原文如下]

# AI Product Management at Spotify: A View From Three Angles

![Feature Image](/images/posts/c5bddf5e39c6.png)

Almost every article or podcast about product management and AI refers to "the AI PM" as one job. But what that job looks like depends on what you’re building.

The three of us work at the same company, on the same technology stack, and in the same part of the organization. We talk constantly, but our day-to-day work, and what success looks like, is quite different.

Henok leads product in Tech Research, where success might be a team making the right technology choice, a methodology that helps several teams work with greater confidence, or a result that shows the organization what is possible. Divita leads product for a recommendation foundation model, shaping what it learns and how its capabilities help teams build better experiences for listeners. Humberto builds the experience users actually interact with, bringing model capabilities, interaction design, and user feedback together into something users find valuable and trustworthy

We share more than the technology. We’re working toward the same company priorities, and ultimately, serving the same external users. Our work is deeply connected: an idea from research can become a reusable model capability that opens up a new possibility in the user experience. Getting it to ship takes collaboration across all three.

That closeness can make the differences between our roles easy to miss, especially when we use the same PM vocabulary. We all talk about “quality”, “evals”, and “shipping”, but their meaning shifts with the problem space each of us owns. Even impact looks different. A shift in what the organization believes or where it invests can be a major research win; for a model PM, the payoff comes when a model improvement translates into better recommendations across multiple user experiences. And for an experience PM, it comes down to whether users love the product and come back.

The fundamentals of product management still apply. But building AI products requires different kinds of specialization depending on what you own. Below, each of us shares what that looks like in practice.

## The research layer: where the product is technical leverage

Henok, Principal Product Manager, Tech Research, Personalization

As the product lead for Tech Research, I work with product teams on today's needs while looking at what might matter next as AI changes what’s possible. I think of our product as technical leverage: applying scientific expertise where it can change what Spotify builds or how confidently we build it.

### 1. AI is changing which problems need research

Better models and tools mean product teams can increasingly do work that previously required deep involvement from research. This allows research to focus more on shared methods, system design, and emerging capabilities where the right approach remains unclear.

The questions that matter tend to span several teams, further changing the research-product team dynamic. Two examples are how to evaluate open-ended model behavior, and how to represent users and content in ways that several products can use.

AI makes it easy to build an exciting prototype quickly. However, the gap between that prototype and a product that works reliably for hundreds of millions of users can be significant. Similarly, a more complex model might look great in a demo, without any meaningful difference on the production tasks that matter. With this in mind, evaluation, latency, cost, data, and integration all become part of the research question. This is what helps us make informed investment decisions.

### 2. A promising model architecture is not a roadmap

One project has made this particularly clear to me. We have been exploring an architecture that brings together capabilities currently spread across different systems. At first, the question was whether it could work. As the evidence grew, a harder product question emerged: what should the organization do with it? A new architecture may affect infrastructure, evaluation, interfaces, and several teams' plans, and it sits alongside systems that already work.

My job is to turn the bigger idea into decisions the organization can reasonably make: start with a concrete problem, find a useful test, and agree on what evidence would justify the next step. It isn’t all or nothing. The methods and components we develop along the way can already improve existing systems, even while the larger questions stay open.

What began as exploration now informs model and experience teams, and its methods and components can improve existing systems even while the larger architecture question remains open. The harder work is finding a credible path through product needs, technical constraints, and existing commitments.

### 3. Long feedback loops in a field that moves quickly

Research impact can take months to appear, often in another team's roadmap or metrics. During that time, the technology and the organization's priorities may change. This makes influence a critical part of the role.

Within the research team, I provide product and strategic context without prescribing the answer. Outside it, I connect the work to decisions and involve the relevant teams early, while being clear about what the evidence does and does not show. If that starts only when the research is complete, the decision window may have closed.

The pace of AI also requires me to understand the technology more deeply than in many of my previous PM roles. AI tools help me work through papers and prototypes, and I stay close to one or two projects at a time to judge the choices and obstacles involved.

The role calls for technical depth and organizational judgment: seeing which questions matter across teams, testing ideas before they become commitments, and connecting evidence to decisions in time. When we get that right, the impact compounds through the methods teams use, the technology they choose, and the experiences they build.

## The model layer: where the product is a capability and the customer is another team

Divita, Principal Product Manager, AI Foundation, Personalization

I lead product for a foundation model, a language model that is purpose-built for recommendations, designed to reference real items on Spotify. Like any platform team, everything we build reaches users through other product teams. What makes this platform different is the product itself. Its behavior is shaped through data, its outputs are probabilistic, and quality means something different to every team that integrates it. That combination is what shapes the job.

My customers are internal teams that build the surfaces and experiences Spotify users interact with every day. They have their own roadmaps and metrics, and the same model needs to serve different definitions of a good recommendation.My job is to understand those needs and decide where a shared capability can serve them well. A request from one team can point to something useful across several experiences; recognizing those opportunities helps shape the model’s direction.

This is where the product fundamentals become concrete. Product-market fit means understanding which problems teams can solve with the model. A clear value proposition means explaining what it offers for their particular experience. And business impact comes through what they ship with it. Understanding those needs gives us direction. Translating them into model behavior is where the work changes.

### 1. You cannot spec model behavior. You shape it, and then you prove it matters.

[翻译失败，原文如下]

In a traditional product role, I would define what the system should do and work with engineers to build it. Here, behavior is learned through training rather than specified directly in code. If we want to improve the relevance of recommendations, a spec alone won’t get us there. I work with the team to decide what the model needs to learn, which data could help it learn that, and how we’ll know whether it has. Training takes time, so those decisions shape what we prioritize for each cycle.

The two real levers are what you teach the model and how you check what it learned. Data and evals. A large part of my job is deciding what those evals should measure. What makes a recommendation good for a particular listener, in a particular moment? A plausible recommendation is only the starting point. We need to understand how well it fits the listener’s context, balances familiarity with discovery, and stays relevant over time. Designing evals means turning those expectations into criteria we can consistently assess.

Then we need to connect what we measure in the model to what listeners experience. Offline evals help us understand model behavior, while online metrics show how that translates into the user experience. I work with partner teams to understand which model improvements make a difference in their products. What we learn together helps us prioritize the next training cycle.

### 2. Show what a shared model makes possible

The promise of a shared recommendation model is that an improvement can benefit multiple experiences. But each team already has a system optimized for its own needs. Our first task is to show that the shared model can meet that experience’s requirements for quality, latency, and cost. I work with partner teams to define those criteria and agree on how we’ll assess them.

Meeting those requirements establishes a starting point. The longer-term question is what teams gain by building on the same model. Can something we learn in one experience improve recommendations in another? Can a team build on an existing capability to try something new? Part of my job is turning that promise into specific questions we can test.

A single evaluation can’t answer all of them. We need to track how the model develops across training cycles and how those changes translate across experiences. That gives us a way to distinguish a promising result from a pattern we can plan around.

A foundation model takes time and resources, and the benefits build as more teams use it. Being clear about where those benefits are showing up, and what we still need to establish, helps us decide what to prioritize next. That is how we make the case for the model over time: through evidence teams can use in their own product decisions.

### 3. Good is not enough if nobody ships with it

Success means getting teams to ship with your model. A good model is essential, but its value depends on whether another team can use it to solve a problem that matters to them.

Much of the work that makes that happen looks nothing like model work. It means finding a team whose current system has hit a ceiling on a metric they care about, then making the model a compelling, practical path forward. That requires agreeing on what the capability needs to deliver, defining the integration contract, and taking responsibility for testing the riskiest assumptions before asking the partner team to commit.

My team’s best result this year came from a surface team that wanted an outcome we were positioned to deliver. The collaboration worked because we agreed on how we would measure success before we agreed on the architecture. That gave us a shared basis for deciding what to build and whether it was working.

That is the version of the job I would describe to someone considering it. You own the model, but you also own the work of turning its capabilities into something another team can confidently ship, and users can benefit from.

## The experience layer: where the customer is the user and the model is one ingredient among many

Humberto, Principal Product Manager, Sessions, Personalization

If the research layer creates technical leverage and the model layer creates a reusable capability, the experience layer is where all of it has to work for Spotify's hundreds of million of users. I build the product users actually interact with: the surface where a vague mood becomes a set of songs and where the system has to do something useful even when the request is ambiguous.

My customers are Spotify's users, directly. That is the simplest difference from the other two roles, and it changes almost everything about the job. The research and model layers are my base technology, and my job is to turn that technology into something delightful. Because the experience team is closest to the user, we have the most direct view of which model gaps and unanswered research questions matter most right now. That makes the dependency on the other layers less of a bottleneck and more of a shared prioritization signal across the stack.

### 1. Designing for infinite input

The biggest shift from previous product work is the nature of the input. In a traditional product, the user's action is constrained: they tap a button, select from a menu, type a search keyword. The system's response is predictable, and so is the test. You know what the user did, you know what the system should do, and you can verify it.

In an AI experience, the input is open-ended. Users make vague, underspecified, or complex requests that do not map to any single entity in the catalog. Agents interpret what the user likely meant and construct a response.

That reshapes constraints you thought were fixed. Latency that’s unacceptable in a keyword search turns out to be perfectly tolerable in a conversational interaction, because users understand they are asking for something harder. But questions like how the system should respond when it is not confident, and how you recover when something goes wrong, do not have stable answers - and they belong to the product, not the model.

### 2. Evaluation is a product, not just a process

A/B testing and offline evaluation still matter, but they are not sufficient on their own. When the input space is open-ended, you cannot predefine every scenario worth testing.

So we build new instruments. We build datasets from real usage patterns and design feedback loops that show where the system misunderstood a request or fell short. We build LLM-based judges and custom evaluators tuned to the specific interactions our product supports, then use them to measure whether changes are actually improvements or just different.

Evaluation is not a phase that happens before launch; it is a continuous product in itself. A general-purpose eval that works across the foundation model's many use cases is a starting point, not the finish line. The experience team has to close the gap between "the model is generally good" and "this specific interaction was good for this specific user."

### 3. Conversation makes feedback natural

In a conversational product, users do not just interact with the system. They talk to it. When things go wrong, they say so, in their own words, in real time. That directness did not exist in previous product surfaces, and it changes what is possible.

User frustration with a specific interaction is feedback on the experience, the model, and potentially the training data all at once. A user telling the system "that is not what I meant" is not just a product issue to fix locally. The job is to build mechanisms that detect that signal at scale, interpret it, and pass it back through the collaboration chain so that every layer improves.

[翻译失败，原文如下]

This is the version of the role I would describe to someone considering it. You have the most direct line to the user and the most tangible ownership of the outcome. But you are building on top of systems you influence rather than control, for users whose expectations are being shaped in real time by every other AI product they touch. The craft is in making something trustworthy out of ingredients that are, by nature, probabilistic.

## Overall reflections

The longer we work across this stack, the more we understand that there isn’t one simple new “AI PM” skillset. Product Management is the same craft it has always been: defining the problem clearly, knowing your customer deeply, measuring what matters, and building conviction through evidence rather than enthusiasm. But what the AI stack adds is not a different job. It is a layer of specialization on top of the fundamentals and those layers come in more flavors than people realize, and vary from product to product. AI Product Management is a varied and complex role which only gets more exciting with the rate of change.

---

> 本文由AI自动翻译，原文链接：[AI Product Management at Spotify: A View From Three Angles | Spotify Engineering](https://engineering.atspotify.com/2026/11/ai-product-management-at-spotify-a-view-from-three-angles/)
> 
> 翻译时间：2026-11-10 09:31
