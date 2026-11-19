---
title: Helping AI coding agents work smarter, for less
title_original: Helping AI coding agents work smarter, for less
date: '2026-11-16'
source: Microsoft Research
source_url: https://www.microsoft.com/en-us/research/blog/tokeneconomizer-learning-from-experience-to-make-ai-coding-agents-more-efficient/
author: ''
summary: '[翻译失败，原文如下]


  ## At a glance


  - Developers use AI coding agents in the same codebases day after day, yet agents
  often start each session from scratch: ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-19T09:43:31.495521'
---

[翻译失败，原文如下]

## At a glance

- Developers use AI coding agents in the same codebases day after day, yet agents often start each session from scratch: rediscovering familiar facts, loading unused tools, and repeating unsuccessful approaches.
- TokenEconomizer is an open-source plugin that learns from an agent’s past sessions in a repository to reduce waste in future sessions, without modifying the agent or its underlying model.
- Across 277 real bug-fixing tasks, TokenEconomizer reduced costs by 18.4–30.9% across multiple AI coding agents. Costs fell in every repository tested, while task success rates remained broadly stable.

AI coding agents are increasingly helping developers fix bugs and build features largely on their own, but every interaction with their models consumestokens. In each session, an agent sends instructions, tool descriptions, and session history to its model. Most efforts to reduce this cost focus on individual tasks. Yet developers return to the same repositories, giving agents an opportunity to learn from previous work. Without that learning, an agent may repeatedly rediscover how to run tests, load tools it never uses, or spend dozens of turns revisiting the same error.

In our paper,TokenEconomizer: Experience-Driven Black-Box Cost Control for Coding Agents, we ask a simple question: can experience in a repository help an agent solve future tasks more efficiently? TokenEconomizer, an open-source plugin from UC Berkeley, Microsoft Research, and Microsoft Security, turns completed sessions into guidance for subsequent ones. It reduces waste without changing the agent or its underlying model, so developers can use it alongside the coding agents they already rely on.

![Figure 1. Each finished session teaches TokenEconomizer something about the repository, so later sessions cost less tokens.](/images/posts/46434dfe4b67.png)

## Where the tokens go

We first profiled Claude Code on 60 tasks from SWE-Bench, a benchmark of real bug fixes in open-source Python projects, running each repository’s tasks in sequence. Three kinds of waste recurred:

- Rediscovering the same facts. After a repository had accumulated at least five completed tasks, 30% of tool calls repeated an action from an earlier task in that repository. Only 7% matched an action in another repository’s history.
- Paying for unused tools. The agent received 23 tool descriptions on every turn, but 16 were never called.
- Getting stuck on failures. The 17% of tasks that failed accounted for 32% of the spending.

We also tested three popular open-source plugins, each built around a fixed cost-saving strategy. Each lowered costs in some repositories but not others. Together, these findings suggest that effective cost control must adapt to the repository, rather than apply the same strategy everywhere.

## How TokenEconomizer works

After each session, TokenEconomizer reads the session’s log and updates what it knows about the repository. It then acts through three mechanisms, using only interfaces the agent already provides, as illustrated in Figure 2.

Micro-skillscapture repository-specific knowledge in one-line notes. TokenEconomizer identifies recurring patterns across sessions and proposes corresponding notes. They are added to the agent’s starting context only after several sessions have confirmed the pattern, and retires the note if later evidence contradicts it.

Tool pruningremoves tools that repository history suggests the agent is unlikely touse, while always retaining core tools for running commands and editing files. Removed tools can be restored if needed.

Failure-loop interventionwatches for an agent that keeps hitting the same failure. A judge model decides whether the agent is truly stuck or still making progress. If it is stuck, the agent gets a short note suggesting a different approach. In the open-source plugin, if the agent is still stuck after the note, TokenEconomizer alerts the developer rather than stopping the work itself.

![Figure 2. TokenEconomizer works alongside an unchanged coding agent. Micro-skills add learned facts, tool pruning trims the loaded tools, and failure-loop intervention redirects stuck work. Each finished session updates all three.](/images/posts/33f48bcede9e.png)

The controller is designed to revise its decisions as new evidence arrives. Reported savings also account for the cost of TokenEconomizer’s own model calls.

## Saving costs in every repository

We evaluated TokenEconomizer on 277 SWE-Bench tasks from six repositories, using five different AI coding agent and model combinations. For each repository, TokenEconomizer started with no prior session history.

TokenEconomizer lowered the average cost by 18.4–30.9%, as shown in Figure 3, and saved the most in all 30 repository-combination pairs without performance loss. By contrast, lowering the model’s reasoning effort saved similar or larger amounts but led to substantial performance degradation.

![Figure 3. On SWE-Bench, TokenEconomizer lowered mean cost per task by 18.4–30.9% across five agent–model combinations (left), while Pass@1 rose in four of them (right).](/images/posts/d619dc14488c.png)

Savings grow as experience accumulates. Early tasks can cost more while TokenEconomizer learns, but cumulative costs fell below the default in every repository by the sixth task, shown inFigure 4. Each mechanism contributes savings on its own, and combining all three delivers the largest reduction.

![Figure 4. Cumulative cost change relative to default over each repository’s tasks, using Claude Code. Starting with no history, every repository becomes cheaper by the sixth task.](/images/posts/dd4d1eac1763.png)

The savings also carried over to sequential web development, with costs 16.0–21.2% lower on Web-Bench. On security auditing, where every task is in a new repository, costs were 6.4–19.6% lower.

## Looking ahead

TokenEconomizer opens a path toward coding agents that learn not only how to solve tasks, but also how to spend computation more effectively. Its lightweight controller shows how experience can improve efficiency without changing the underlying agent or model.

The open-source plugin makes these directions accessible to developers and researchers. It is designed to run alongside existing AI coding agents without modifying their underlying models, requires no API key of its own, and keeps what it learns on the developer’s machine. We invite the community to use it as a starting point for exploring agents that become more resourceful with experience, adapting how they work, as well as what they know.

## Meet the authors

### Aaron J. Li

Research Intern

### Weijia Xu

Senior Researcher

### Chandan Singh

Staff Research Scientist

Voyage AI

### Zixiao Chen

### Jeevana Priya Inala

### Bin Yu

Professor

UC Berkeley

### Ion Stoica

University of California, Berkeley

### Michel Galley

Senior Principal Research Manager

### Jianfeng Gao

Technical Fellow & Corporate Vice President

---

> 本文由AI自动翻译，原文链接：[Helping AI coding agents work smarter, for less](https://www.microsoft.com/en-us/research/blog/tokeneconomizer-learning-from-experience-to-make-ai-coding-agents-more-efficient/)
> 
> 翻译时间：2026-11-19 09:43
