---
title: 'From post-training to production: How TinyFish runs its web-native model on
  Databricks AI Runtime'
title_original: 'From post-training to production: How TinyFish runs its web-native
  model on Databricks AI Runtime'
date: '2026-10-09'
source: Databricks Blog
source_url: https://www.databricks.com/blog/post-training-production-how-tinyfish-runs-its-web-native-model-databricks-ai-runtime
author: ''
summary: '[翻译失败，原文如下]


  - TinyFish uses Databricks AI Runtime to train and fine-tune its web-native model
  on managed GPU infrastructure, with MLflow for evaluati...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-13T08:48:28.539272'
---

[翻译失败，原文如下]

- TinyFish uses Databricks AI Runtime to train and fine-tune its web-native model on managed GPU infrastructure, with MLflow for evaluation and Databricks Model Serving for production inference.
- Bringing these workflows together gives TinyFish a continuous path from production agent behavior to post-training, evaluation, and deployment.
- In TinyFish's internal go/no-go benchmark, its web-native model achieved a 77.6% task-success rate across 2,178 web-agent tasks, measuring whether the full agent successfully completed the requested work.

TinyFish builds infrastructure for enterprises that need agents to work across the live web. Its Search, Fetch, Browser, and Agent APIs support large-scale, authenticated web workflows, where an agent may need to navigate dynamic sites, retrieve information, interact with applications, and carry out a task across multiple steps.

TinyFish is developing its own specialized web-native model for these agent tasks. As the company expanded its model work, the team also had to build the infrastructure around it: GPU compute for post-training, evaluation that could measure the behavior of the full agent, production serving, and the data needed to understand how the system was performing.

Rather than manage those pieces across separate systems, TinyFish began building its model development lifecycle on Databricks.AI Runtimeprovides managed GPU infrastructure for training and fine-tuning, while MLflow supports evaluation and Databricks Model Serving provides the production serving layer.

## Turning agent behavior into better models

TinyFish started post-training its web-native model with supervised fine-tuning and is moving toward Direct Preference Optimization, or DPO. The team runs these workloads on Databricks-managed GPUs through AI Runtime, allowing researchers to work with GPU infrastructure without having to operate a separate training platform themselves.

The training work is closely connected to how TinyFish evaluates its model. Because the model operates as part of a larger web agent, evaluating an individual model response only tells part of the story. TinyFish instead evaluates whether the full agent successfully completes the requested task.

In its internal go/no-go benchmark, TinyFish's web-native model successfully completed 1,691 of 2,178 web-agent tasks, for a 77.6% task-success rate. A separate LLM judge reviews the original request, the agent's action history, and its final result. A task passes only when the requested action is completed or the correct answer is returned with all requirements satisfied; partial completion, incorrect answers, and invalid results count as failures.

That gives TinyFish a useful signal for model development. The team can see how changes to its model affect the performance of the full agent and use those results to guide subsequent post-training.

Successful model iterations can then move into production through Databricks Model Serving. TinyFish already serves production models on Databricks, including its search reranker and query rewriter. The team also hosts and serves its web-native model on the platform.

Over a recent 15-day period, TinyFish recorded 294,781 agent runs involving its web-native model across 6.4 million tool steps. The estimated model-serving cost during that period was $0.088 per run, or $0.0040 per tool step. These figures reflect serving costs for TinyFish's web-native model only, not the full agent stack, and give the team a consistent way to track serving economics alongside quality and usage data in Databricks.

Together, these capabilities give TinyFish a continuous path from agent behavior to post-training, evaluation, and deployment. Evaluation results, usage data, and cost reporting can remain in Databricks alongside the serving workload, giving the team a common foundation for understanding how its model performs and informing subsequent model development.

## Building models for the work agents actually perform

General-purpose foundation models still play an important role in TinyFish's agent architecture, but its web-native model gives the team a system it can optimize specifically for web-agent tasks.

TinyFish can develop and evaluate its model against the tasks its product actually needs to perform, rather than relying exclusively on external foundation model APIs throughout the agent. Supporting that approach requires more than GPU capacity. The development cycle spans post-training, evaluation, production serving, and the operational data around the model.

AI Runtime gives TinyFish managed GPU infrastructure inside the same Databricks environment it uses for the surrounding ML lifecycle. This lets the team keep training and serving closer to the evaluation and operational data it uses to understand how its model is performing, rather than building a separate deep learning stack around the model.

Alongside its own models, TinyFish is consolidating access to external foundation models through Unity Gateway for centralized cost tracking, key management, and governance. This gives the team a more consistent way to manage model traffic as the agent stack expands.

For a growing AI company, the benefit is practical: fewer standalone systems to operate means more engineering time can stay focused on the models and product behavior that differentiate TinyFish.

## Building for the next model iteration

TinyFish continues to evolve its approach to developing its web-native model, expanding beyond supervised fine-tuning into DPO and exploring larger training workloads as the model develops.

The underlying workflow is designed to stay consistent as those techniques change. Agent evaluation can show where the model performs well and where further work is needed. That information can feed into post-training, new versions can be evaluated against complete tasks, and models ready for production can be served from the same environment.

By running that lifecycle on Databricks, TinyFish can treat GPU infrastructure as part of its ML platform rather than as a separate system the team has to assemble and maintain. That gives the team a more direct path from what it learns about its model in production to the next iteration of the model.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[From post-training to production: How TinyFish runs its web-native model on Databricks AI Runtime](https://www.databricks.com/blog/post-training-production-how-tinyfish-runs-its-web-native-model-databricks-ai-runtime)
> 
> 翻译时间：2026-10-13 08:48
