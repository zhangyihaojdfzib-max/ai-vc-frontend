---
title: 'ALTK-Evolve: How learned memory tops the τ²-bench leaderboard on customer
  service tasks without a frontier model'
title_original: 'ALTK-Evolve: How learned memory tops the τ²-bench leaderboard on
  customer service tasks without a frontier model'
date: '2026-10-20'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ibm-research/altk-evolve-bc
author: ''
summary: '[翻译失败，原文如下]


  # ALTK-Evolve: How learned memory tops the τ²-bench leaderboard on customer service
  tasks without a frontier model


  ALTK-Evolve learns an...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-21T06:57:57.344674'
---

[翻译失败，原文如下]

# ALTK-Evolve: How learned memory tops the τ²-bench leaderboard on customer service tasks without a frontier model

ALTK-Evolve learns and applies a playbook using GPT-4.1, outperforming the retail entries on τ²-bench, a customer service agent benchmark—without updating model weights.

## Learned memory takes a basic ReAct agent with GPT-4.1 to the top

Using GPT-4.1, an older, non-reasoning model, a basic customer-service agent reaches67.5% Pass^4 on τ²-bench retail— meaning it solves the task onall fourindependent attempts for 67.5% of tasks. It scores above every retail entry in our October 12, 2026 leaderboard snapshot. It runs on the benchmark's stock ReAct scaffold, with learned guidelines appended to its system prompt.

ALTK-Evolvebuilds that playbook using GPT-4.1.It analyzes the agent's training-task attempts and uses the model to distill successes and failures into short behavioral rules: how to authenticate a customer, confirm a transaction, or handle a return. Those guidelines are then added to the agent's prompt for subsequent conversations. The same model powers both guideline extraction and the agent; no weight updates or human annotation are needed.

Ourprevious workdemonstrated this approach on coding agents. Here, we test it on customer service, where success requires following domain policies, understanding a customer's request, and executing the right tool actions.

## τ²-bench tests policy-bound customer service

τ²-bench(from Sierra) measures how well an agent handlescustomer-service conversationsunder real constraints. Each task pairs the agent with an LLM-simulatedcustomerwho has a goal in mind, a set ofdomain tools(look up an order, issue a refund, rebook a flight), and a writtenpolicy documentthe agent must follow. The agent has to draw out the right details, stay within policy, and take the correct — often irreversible — actions; a task counts as solved only when the final database state matches the expected outcome, a strict binary reward. We use its two customer-service domains,retailandairline.

We run τ²-bench's own implementation of a basic ReAct agent with a two-phaseTHINK → ACTloop, usinggpt-4.1as the agent model andgpt-5.5as the customer-simulator model;4 trialsper task.The only change we makeis a block of learned guidelines appended to the system prompt — everything else (policy, tools, scaffold) is stock τ²-bench. Concretely, the learned guidelines are tacked on after the domain policy as a plain markdown list:

```text
You are a customer service agent that helps users according to the policy below.
Always follow the policy strictly. Use the provided tools when needed.

<policy>
# Retail agent policy

As a retail agent, you can help users:
- cancel or modify pending orders
- return or exchange delivered orders
- modify their default user address
…
</policy>

## Guidelines learned from past task attempts (follow these carefully):
- Authenticate the user before taking any order-related action. If email is unavailable, verify identity via full name and zip code using the find_user_id_by_name_zip API.
- Always confirm all intended changes (modify, cancel, return, exchange) with a clear, structured summary, and require explicit user approval before executing any database-updating action.
- When processing a return or exchange, communicate the refund with an itemized breakdown and clarify refund timing — don't wait for the user to ask.
- Take one action per step: never combine a tool call with a user-facing message in the same turn, and wait for the tool's result before replying.
- Before looking a user up, parse and clean their name — e.g. split a combined handle like `daiki_johnson_9523` into first/last name — and after a couple of failed lookups, state the exact format you need.
…

```

We extract guidelines from the agent's trajectories on τ²-benchtraintasks usinggpt-4.1, the same model that powers the agent, then apply them unchanged on the held-outtestset.

## Guidelines improve capability and reliability

In aprior post, we talked about how different models / tasks require different dosage of guidance. Inline with the idea, we also evaluate different amounts of guidelines provided to the model.

Each guideline carries asupportcount — the number of distinct training tasks it was extracted from, so higher support means a rule that generalized across more tasks rather than a one-off. We compare three configurations:baseline(no guidelines),sup3(keep only guidelines with support ≥ 3 — a small, high-confidence core), andlossless(keep every guideline retained after consolidation, i.e. support ≥ 1).

Table 1. Guideline configurations and retained guideline counts by domain.

The metrics we track.Every task is attempted4 times, and we read those trials two ways:

- Mean Accuracy— the average success rate across the 4 trials. This is thecapabilityaxis:how often does the agent get this right?
- Pass^4— the percentage of tasks that passed across all 4 trials. This measures along thereliabilityaxis and the metric the τ²-bench leaderboard reports. It matters here because a support agent that resolves a refund 3 times out of 4 still fails a quarter of real customers — Pass^4 asks whether you can trust the agenteverytime, not just on average.

![Mean Accuracy and Pass^4 on the held-out test tasks, by variant, for Retail and Airline. Lossless lifts retail accuracy +4.4 pp and Pass^4 +10.0 pp; airline accuracy rises +7.5 pp with lossless while sup3 gives the best Pass^4 at +10.0 pp.](/images/posts/2923b25deb74.png)

Figure 1. Mean Accuracy and Pass^4 on held-out retail and airline tasks for agents usinggpt-4.1across four trials per task.

Agent model:gpt-4.1(user simulator:gpt-5.5).

Table 2. Held-out agent performance usinggpt-4.1across four trials per task. Parentheses show percentage-point changes from baseline.

Mean Accuracy climbs in both domains — retail+4.4 pts(78.1 → 82.5) and airline+7.5 pts(57.5 → 65.0). Reliability moves further: the strictPass^4rises+10 ptsin retail (57.5 → 67.5) and+10 ptsin airline (35.0 → 45.0). And the gains come from better-informed calls, not longer conversations — we look at conversation length directly inBetter performance costs more tokens, not more turnsbelow.

### The best amount of guidance depends on the domain

The two domains disagree abouthow muchguidance pays off. Inretail, more is better on every metric — the small sup3 core barely beats baseline on accuracy, and you need thefull lossless setfor the real jump. Inairlinethe picture flips at the reliability end: lossless leads on accuracy (65% vs 60%), but the compactsup3 core (14 guidelines) is the morereliableone, taking Pass^4 to45%against lossless's 40%. Echoing the earlier finding thatdelivery is a dial, not a constant,support count is a knob worth tuning per domain, not a value to hard-code.

## Better performance costs more tokens, not more turns

Guidelines aren't free, but the cost lands where you'd expect — inprompt input tokens, not in a longer, more meandering conversation:

![Cost per conversation grouped by Retail and Airline. Lossless increases cost by 65% and 32%, respectively, over the no-guideline baseline.](/images/posts/550942a71bbb.png)

Figure 2. Total LLM cost per conversation by domain and guideline configuration on the full base split.

Table 3. Total LLM cost per conversation (agent and user simulator) on the full base split across four trials. Lower is better.

Does the agent get there bytalking longer? To answer that cleanly we comparelike for like: the task runs solved underbothbaseline and the guideline variant — identical scenario and seed, a true "same task, done right" set — and count assistant turns on each side.

Table 4. Assistant turns per conversation for matched runs solved under both settings on the test split, pooling four trials.

[翻译失败，原文如下]

The agent isn't talking longer — on the shared set, guidelines make conversationsslightly shorter: lossless trims ~0.3–0.4 turns in both domains (retail 10.59 → 10.16, airline 9.15 → 8.82), and no variant lengthens them. That matters beyond cost: each turn is a sequential LLM round-trip, so fewer turns meanslower end-to-end latency — a faster time-to-completionfor the customer, not just a cheaper one. The only real price is on the input side — the larger system prompt riding on every LLM call: retail's 292-guideline prompt pushes cost from ~$0.084 to ~$0.139 per conversation, while airline's smaller playbook is cheaper. And in production even that is largely reclaimable withprompt caching, since the guideline block is identical across every call.

So the trade is a favorable one: for aslightly higher input cost(much of it cached away in practice) the agent landshigher accuracy, higher reliability,andlower time-to-completionat once — not the usual quality-for-latency tradeoff, but all three moving the right way together.

## Learned guidelines also improve agents using frontier models

So far, we have used an older, non-reasoning model —gpt-4.1. A fair objection is that learned guidelines might have less to add to an agent using afrontiermodel: maybe they only patch the gaps of a weaker model. So we tested it directly — we reranairlineusinggpt-5.5for both the agent and guideline extraction, on the same τ²-bench ReAct scaffold, with guidelines re-mined from the agent'sownruns. One detail changes with the model: none of the guidelines extracted in this setup reached support ≥ 3 (they top out at support 2), so the high-support core here issup2rather than sup3.

Table 5. Held-out airline performance for thegpt-5.5agent across four trials per task.

The learned guidelines improve this setup too. On the same held-out test tasks, appending them to the prompt liftsaccuracy +10 pts(72.5 → 82.5) and the strictPass^4 by +15 pts(55.0 → 70.0) — alargerreliability gain than we observed withgpt-4.1on these very tasks (+10 pts), and from a much higher floor. Learning guidelinesaroundthe model can improve an agent even when it starts from a stronger base. And where the baseline's reliability swung between reruns, the lossless configuration reproduced exactly — the gain it buys is dependable, not a lucky draw.

## ALTK-Evolve tops the leaderboard comparison

Submissions are scored on thefull base split(train ∪ test), as τ²-bench requires, and reported atPass^4. Because that covers the full task set rather than the held-out test split, these figures differ from the test-task numbers reported above. This is where the practical upshot shows up — prompt-level memory carries agents using each base modelinto, orpast, current frontier company:

- Retail: #1.On the base split the agent with learned guidelines reachesPass^4 = 67.5%, ahead of every frontier modelandahead ofRAFT-30B-A3B(61.4%), a modelfine-tuned on synthetic τ²-bench retail data. Using stockgpt-4.1and a prompt-appended playbook, it outperforms that fine-tuned system by+6.1 points.
- Airline: #1usinggpt-5.5, #8 usinggpt-4.1Against the published board, the compactsup3 coregives the agent usinggpt-4.1Pass^4 = 44%—8th, beating GPT-5.2 (no reasoning) and nearly matching Claude Sonnet 4.5. Swap in the stronger base and the same approach tops the field outright:the agent usinggpt-5.5reaches 82.0%, clearing every frontier entry (66–72%).

![Saved Pass^4 leaderboard comparison for Retail and Airline, highlighting ALTK-Evolve runs at 67.5% in Retail and 82.0% and 44.0% in Airline.](/images/posts/5e4f597de948.png)

Figure 3. Pass^4 comparison between ALTK-Evolve runs and the τ²-bench leaderboard snapshot from October 12, 2026.

Same message in both domains:learning guidelinesaroundthe model works across different base models— bringing an agent using an older, non-reasoning model into frontier company on retail, and taking an agent using a frontier model to the top on airline.

## Agents can improve without weight updates

Fine-tuning a model on a benchmark is expensive, brittle, and doesn't transfer to the next domain. Here, ALTK-Evolve improves astock agent on a stock modelin both domains — and matches or beats a fine-tuned system on retail — using onlyprompt-level guidelines extracted from the agent's own runs, automatically, without human annotation, and without any test-set leakage.

### Links:

- Prior postsThinking of ACE? We Can Do It with Fewer TokensHow much memory does your agent actually need?
- ALTK-Evolve library—https://github.com/AgentToolkit/altk-evolve
- τ²-bench—https://github.com/sierra-research/tau2-bench
- Retail leaderboard submission—τ²-bench PR #542
- Airline leaderboard submission-τ²-bench PR #551

1. Thinking of ACE? We Can Do It with Fewer Tokens
2. How much memory does your agent actually need?

---

> 本文由AI自动翻译，原文链接：[ALTK-Evolve: How learned memory tops the τ²-bench leaderboard on customer service tasks without a frontier model](https://huggingface.co/blog/ibm-research/altk-evolve-bc)
> 
> 翻译时间：2026-10-21 06:57
