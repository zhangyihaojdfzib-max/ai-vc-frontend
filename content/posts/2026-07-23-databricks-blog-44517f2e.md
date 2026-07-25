---
title: Why A Frontier Data Agent Outperforms General Coding Agents in Quality and
  Cost
title_original: Why A Frontier Data Agent Outperforms General Coding Agents in Quality
  and Cost
date: '2026-07-23'
source: Databricks Blog
source_url: https://www.databricks.com/blog/why-frontier-data-agent-outperforms-general-coding-agents-quality-and-cost
author: ''
summary: '[翻译失败，原文如下]


  - Genie Code is Databricks'' data agent for the full spectrum of data work — from
  basic data analysis, to workspace-wide data exploration,...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-07-25T05:00:50.158444'
---

[翻译失败，原文如下]

- Genie Code is Databricks' data agent for the full spectrum of data work — from basic data analysis, to workspace-wide data exploration, to data engineering tasks like building pipelines, debugging failures, and shipping dashboards.
- Across 400+ tasks from real internal usage, Genie Code was both the most accurate agent we tested and the cheapest, delivering a correct answer at less than half the cost of other agents.
- Because of deep semantic understanding of enterprise context, Genie Code can skip the brute-force schema exploration that drives other agents' errors and high costs, leading to more accurate answers at significantly lower cost.

Conventional wisdom in agentic AI says that better answers cost more tokens: let the agent explore longer, verify more, and retry more, and accuracy will always go up. When we evaluated Genie Code head-to-head against three widely used coding agents from major AI labs on 400+ real data tasks from our internal usage, we found the opposite: Genie Code was both the most accurate agent we tested and also the most cost efficient.

![Genie Code outperforms coding agents on 400+ real data tasks](/images/posts/0ca8a167ac8a.png)

The reason is that data agents must work in a new paradigm where general coding agents struggle. As weshared before, data agents face unique challenges: they must discover the right assets in a dynamic, constantly evolving workspace with hundreds of thousands of tables, notebooks, dashboards, and documents, they must determine the source of truth across metadata and documents that can be outdated or contradictory, and they must do it all without the verifiable tests that coding agents lean on.

To address those challenges, we provided Genie Code with capabilities that allow it to skip the random walk exploration that general coding agents fall back on: semantic search over the catalog and workspace assets, persistent memory of the tables and business logic users rely on, and deep semantic understanding of enterprise context.

We observe this difference directly in the sessions from this evaluation. In one example, Genie Code efficiently finds the right table leveraging semantic search and metadata, writes one SQL query, and lands the correct answer in five tool calls, while none of the three general-purpose agents recovers from exploration.

![Genie Code skips the random walk](/images/posts/8cab276210da.png)

Below, we dive deeper into how we evaluated Genie Code on a wide spectrum of real-world user tasks.

## We evaluated the agents on 400+ real tasks from real usage

We deliberately built an evaluation set to span awide distribution of real user tasks on Genie Code. We distilled 401 self-contained tasks from real internal usage at Databricks, spanning everyday questions and the harder problems power users tackle: discovery tasks where the the agent must find the right assets , creating and modifying code and queries, debugging code, understanding and explaining existing code, precise data lookups that require pulling exact numbers from tables, and more.

![Distribution of evaluation tasks](/images/posts/72c01176f34c.png)

## Results

We ran each agent on all 401 tasks, with the coding agents using their own harnesses, the latest models from leading frontier labs, and augmented with Databricks MCP. Every agent was given the same 20-minute wall-clock budget per task. Answers were graded by an independent judge based on whether the response was correct and useful, and a task that times out counts as a failure. The dollar figures in this analysis are estimates for what a user would pay for each agent, and they are more informative in relative terms.

Agent

Accuracy

Mean $/task

Genie Code

76.6%

$0.55

Coding Agent 1

72.1%

$1.09

Coding Agent 2

55.9%

$0.91

Coding Agent 3

56.1%

$1.16

![Genie Code costs about half as much as other agents](/images/posts/3dfe6dcb251c.png)

Genie Code is the most accurate agent on this benchmark and the cheapest: it’s roughly half the cost per task of its closest competitor, and less than half its cost per correct answer. The other two coding agents land in the mid-50s on accuracy, dragged down in large part by wall-clock timeouts on long-running scans, often due to inefficient, uncapped queries against very large tables.

For this particular benchmark, we observed that the median task costs $0.34, the p99 is $2.72, the most expensive task is $3.87, and only 4% of tasks exceed $2. The other agents put 33–40% of their tasks over $1 (vs. 16% for Genie Code), and one coding agent's deep deep exploration runs top out at a significantly higher cost of $9.49. Since all the agents have access to the same tier of frontier-level models, variations in cost come down to efficiency: taking fewer turns and spending fewer tokens to get to an answer.

![Genie Code remains efficient across the entire task distribution](/images/posts/f034afdcdacc.png)

The gap is driven by how each agent finds the data it needs. The hardest tasks in the set don't name the assets explicitly, and the agent must locate the right tables, notebooks, or dashboards, along with the relevant business logic before it can answer. On those tasks, the general-purpose agents fall back on inefficient workspace exploration, and that exploration results in both lower accuracy and higher cost.

Genie Code's understanding of the workspace context — semantic search over the catalog and persistent memory of the workspace's data — let it skip most of that, averaging just 8.3 tool calls per task — fewer than any agent we tested. That's also what the cost tails above are made of: every agent's expensive runs are dominated by these discovery tasks, and Genie Code's tail is the shortest. We expect this advantage to be further strengthened by theGenie Ontology; we disabled the Ontology during this run as it is not yet globally available to all our customers.

## Conclusion

When we started our investigation, we expected a trade-off between accuracy and cost. Instead, across a wide distribution of real user tasks we find that Genie Code is able to use its strong semantic understanding of the data to outperform general coding agents to be more accurate and cheaper.

Genie Code is built as a frontier data agent, optimized for operating in a highly dynamic and ambiguous environment like the Databricks workspace. General coding agents struggle in these environments: they end up spending their turns and tokens rediscovering context that Genie Code already has. That expertise compounds into accuracy, speed, and cost at once, with no trade-off in general-purpose capability.

Finally, like ourcoding-agent benchmark on the Databricks codebase, the broader lesson is that generic leaderboards can't measure users' everyday experience. We're expanding our evaluations every day based on real-world tasks, and will continue to publish what we learn.

---

> 本文由AI自动翻译，原文链接：[Why A Frontier Data Agent Outperforms General Coding Agents in Quality and Cost](https://www.databricks.com/blog/why-frontier-data-agent-outperforms-general-coding-agents-quality-and-cost)
> 
> 翻译时间：2026-07-25 05:00
