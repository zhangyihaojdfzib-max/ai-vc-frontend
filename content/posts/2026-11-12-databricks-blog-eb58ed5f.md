---
title: How Block powers collaborative AI agents with Buzz and Unity Gateway
title_original: How Block powers collaborative AI agents with Buzz and Unity Gateway
date: '2026-11-12'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-block-powers-collaborative-ai-agents-buzz-and-unity-gateway
author: ''
summary: '[翻译失败，原文如下]


  Inside Block,Buzz brings employees and AI agents into a shared workspace.With Databricks
  Unity Gateway, employees who use Buzz can access...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-16T08:50:39.442509'
---

[翻译失败，原文如下]

Inside Block,Buzz brings employees and AI agents into a shared workspace.With Databricks Unity Gateway, employees who use Buzz can access frontier and open-weight models, experiment with different agent harnesses, and find the right combination based on the efficiency frontier for each task.

As AI agents become part of everyday work, Block’s teams needed a way to work with agents in the same place they work with each other. Block developedBuzz, an open source collaboration space where people and AI agents can work together in group discussions, focused conversations, and one-on-one exchanges.

Buzz brings agents into the same collaborative environment as employees. Users can create an agent, choose the model or coding harness behind it, and bring that agent into a conversation with colleagues. Rather than switching between different AI tools, teams can work with multiple agents in one place.

At Block,Databricks Unity Gatewayhelps power the Buzz experience by providing access to a broad selection of frontier and open-weight models through a single integration. That gives employees the flexibility to experiment with different models and match them to the work they're trying to accomplish.

## How Block Buzz brings people and AI agents into one environment

Buzz gives people and AI agents a shared workspace to exchange information, contribute context, and work together on tasks.  Employees can create AI agents, work with them individually or alongside colleagues, and bring others into ongoing work. For example, an employee can ask an agent to help with coding or analysis, while colleagues review its work, provide additional information, or ask follow-up questions.

Buzz includes its own built-in agent, which incorporates a lightweight version of Goose, and also supports other coding harnesses and tools. As an open source project, Buzz is model-agnostic and can be self-hosted, meaning it can run privately on your own network or system, giving users flexibility in how they deploy and configure their agents.

At Block, employees are using Buzz for coding, analytics, and other day-to-day work. Many bring agents into the same conversations where colleagues are already collaborating.

![](/images/posts/0081a2ddeb37.png)

## How Block Buzz uses Unity Gateway to access AI models

Buzz lets users choose the model or harness behind each agent. A coding task, an analytical question, and a lightweight everyday request may benefit from different models or agent harnesses. Instead of committing to a single model for every workflow, Buzz lets users make that choice when creating their agents.

Unity Gateway provides the model access layer for this experience. When employees create an agent in Buzz, they can select Databricks as their inference provider and choose from the models available through Unity Gateway. That includes frontier models from OpenAI, Anthropic, and Google, as well as select open-weight models, all accessible through a single integration.

![](/images/posts/6a688819cf87.png)

This flexibility matters as new models become available and teams learn which ones work best for different tasks. Instead of designing every agent around the same model, employees can create a collection of specialized agents, each with its own model or harness, and bring them together in Buzz.

## How Block experiments with multi-agent workflows and model efficiency

Model choice becomes even more interesting when multiple agents collaborate on the same task. Block has been experimenting with different combinations of models and agent harnesses to understand how they affect performance and cost. One approach its engineers have explored is using a more capable model to coordinate work across a team of agents powered by smaller, more efficient models.

The idea is straightforward because not every step of a complex task requires the most expensive model. A coordinating agent can take on the more demanding work, while other agents handle tasks suited to their capabilities. In Buzz, those interactions can take place within the same collaborative environment, where people can see how agents work with each other and participate in the work.

Block has also developed an internal approach to benchmarking these agent teams, giving its engineers a way to experiment with different configurations. This approach reflects a broader shift in how teams are thinking about AI development. The question is no longer just which single model performs best but how to combine models, harnesses, and agents to complete work effectively.

## Rethinking how people work with AI

Buzz reflects a different way to think about AI at work. Rather than treating each agent as an individual tool, Block built an environment where people can create, collaborate with, and coordinate multiple agents in the same place.

With Unity Gateway providing access to frontier and open-weight models, Block employees can experiment with different combinations of models and harnesses to find what works best for each task, all within the collaborative Buzz experience.

Get started with Block Buzz and Unity Gateway

- Try Block Buzz:Explore the open source project onGitHuband start building agents that work alongside your team.
- ExploreDatabricks Unity Gateway:Learn how to access frontier and open-weight AI models through a single API for your own AI applications and agents.

## Frequently Asked Questions

### What is Block Buzz, and how does it support AI agent collaboration?

Block Buzz is an open source collaboration workspace where employees and AI agents can work together in channels, threads, and direct messages. Users can create agents, choose their models or coding harnesses, and collaborate with multiple agents and colleagues in the same environment.

### How does Block use Databricks Unity Gateway with Buzz?

Block uses Databricks Unity Gateway to provide centralized access to frontier and open-weight AI models within Buzz. Employees can select Databricks as their inference provider and choose from available models, including those from OpenAI, Anthropic, and Google, through a single integration.

### How can enterprises use different AI models for different agents?

Enterprises can assign different models to AI agents based on task requirements, performance, and cost. With Buzz and Unity Gateway, Block employees can experiment with different combinations of models and agent harnesses rather than relying on one model for every workflow.

### How can multi-agent workflows help optimize AI costs and performance?

Multi-agent workflows allow teams to use different models for different parts of a task. For example, a more capable model can coordinate complex work while smaller, more efficient models handle simpler tasks. Block is experimenting with these configurations to understand how model and harness selection affects performance and cost.

### Can Block Buzz be self-hosted and used with different AI models?

Yes. Block Buzz is open source, model-agnostic, and can be self-hosted. It supports multiple models and agent harnesses, and organizations can integrate with Databricks Unity Gateway to access frontier and open-weight models through a single API.

Unity GatewayandCustomers

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[How Block powers collaborative AI agents with Buzz and Unity Gateway](https://www.databricks.com/blog/how-block-powers-collaborative-ai-agents-buzz-and-unity-gateway)
> 
> 翻译时间：2026-11-16 08:50
