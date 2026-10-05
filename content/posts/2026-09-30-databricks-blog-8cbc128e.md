---
title: 'Introducing ai_decide: make fast decisions on your governed data'
title_original: 'Introducing ai_decide: make fast decisions on your governed data'
date: '2026-09-30'
source: Databricks Blog
source_url: https://www.databricks.com/blog/introducing-aidecide-make-fast-decisions-your-governed-data
author: ''
summary: '[翻译失败，原文如下]


  - ai_decide is a new Databricks AI Function that makes fast decisions directly on
  your data. It takes unstructured text and returns struc...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-05T08:02:38.137056'
---

[翻译失败，原文如下]

- ai_decide is a new Databricks AI Function that makes fast decisions directly on your data. It takes unstructured text and returns structured decisions in a fraction of a second.
- Because it's optimized for decisions rather than text generation, ai_decide is faster and lower cost than LLMs on similar tasks.
- Use ai_decide when you need fast, low-cost decisions over governed data: routing prompts to the right model, tagging customer reviews with metadata, or evaluating agent quality—at batch scale in SQL or in real-time over REST.

Today, we’re launching a new Databricks AI Functionai_decidethat makes fast decisions over your governed data.

We see a lot of teams use LLMs for tasks that do not require complex reasoning and text generation.Which category does this support ticket belong to? Does this document need human review? Which model should handle this prompt?

These questions power many of our customer’s high-scale enterprise workflows from processing millions of documents to controlling real-time app logic. However, using LLMs for these smaller, structured decisions means paying for additional latency and cost that compounds at enterprise scale. A decision model like TypeSafe AI'sJevcloses that gap: instead of generating text, it takes unstructured input and a set of questions and returns decisions and their probabilities directly.

ai_decideis a new Databricks AI Function powered by a decision model. It evaluates one or more questions against text in a fraction of a second, and for each question, it returns either a probability, a choice from named criteria, or a score on an ordered scale. Becauseai_decideis optimized for fast decisions, it yields lower latency and cost than an LLM on similar tasks.

## Tryai_decidetoday

ai_decideis now available on Databricks in Beta. Call it fromSQLto make structured decisions at scale on your data or through theREST APIfor real-time applications and agents. For teams already building with the TypeSafe AI API, theai_decidefunction is directly compatible.

Not sure where to start? If you have unstructured data and need to classify it, score it, or decide what happens next,ai_decideis a good fit. Here are a few use cases you can try today:

### Analyze customer reviews to identify recurring product issues

You receive thousands of product reviews each month. Customers describe everything from confusing setup instructions to incorrect billing charges.

Withai_decide, you can tag each review with its primary issue and whether the customer is looking to return the product in one SQL query. Aggregate those tags by product and month to track recurring complaints and see which issues appear most often alongside reported returns.

![figure 1](/images/posts/a877692b6c1c.png)

### Route user prompts to the right model

Let’s say you’re a software company building an AI assistant. Your users ask the assistant to do everything from rewriting a sentence to designing a database architecture. You have several models available with different costs and capabilities and want to choose an appropriate model for each request.

Useai_decideto determine the prompt reasoning level and difficulty. Then route the request to the corresponding model.

An example resultresponse.answers:

### Evaluate AI-generated answers with a judge

Let’s say you run an online retailer with an AI support assistant. Before releasing a new version, you want to evaluate its answers against your refund policy. You have a set of customer questions, generated answers, and reference policies.

Useai_decideas a judge to check whether an answer follows the policy and score how completely it addresses the customer’s request.

Here is an example resulting row, showingresponse.answers:

### Determine the next action in real-time applications

Becauseai_decidereturns a decision in a fraction of a second, it's fast enough to drive an application in real time, where each decision depends on the state of the moment before.

To demonstrate, we built a live demo of Snake, hosted on Databricks Apps.ai_decideplays the game: on every tick, the app sends the current board toai_decideand asks, which direction should the snake move next?

![Snake game built with ai_decide](/images/posts/44d178848238.gif)

Because the whole decision loop closes in a fraction of a second, you can putai_decidebehind any real-time decision an agent or application needs to make: which tool to call, which branch to take, which action comes next.

## Get started

ai_decideis available now in Beta. Use it in SQL to classify, score, and make decisions across governed data at scale, or call the REST API to add fast decisions to real-time applications and agents. Beyond the managed function, there's a broad and growing ecosystem of open-weight decision models, and you can serve and run any of them directly in SQL on Databricks. See our recent open-Jev walkthroughhere.

Explore theai_decide SQL documentationorget started with the REST API.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Introducing ai_decide: make fast decisions on your governed data](https://www.databricks.com/blog/introducing-aidecide-make-fast-decisions-your-governed-data)
> 
> 翻译时间：2026-10-05 08:02
