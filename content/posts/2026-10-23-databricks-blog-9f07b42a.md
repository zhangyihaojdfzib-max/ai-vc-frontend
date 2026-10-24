---
title: 'Built for Agents: The Case for Spark Declarative Pipelines'
title_original: 'Built for Agents: The Case for Spark Declarative Pipelines'
date: '2026-10-23'
source: Databricks Blog
source_url: https://www.databricks.com/blog/built-agents-case-spark-declarative-pipelines
author: ''
summary: '[翻译失败，原文如下]


  - Procedural pipelines burned about 34x as much compute time as declarative pipelines,
  primarily because errors in structurally invalid d...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-24T07:04:58.096857'
---

[翻译失败，原文如下]

- Procedural pipelines burned about 34x as much compute time as declarative pipelines, primarily because errors in structurally invalid declarative pipelines are caught by a cheap “dry run” which does not fully execute them.
- Declarative pipelines contain 51% less code for the same pipeline, so there is far less to read and review.
- Together, these efficiencies make declarative frameworks like SDP the clear architectural choice for autonomous agents building production pipelines.

AI agents now write a growing share of production data pipelines (over 70% of SDP pipelineson Databricks are now created by agents) which raises the stakes in two areas: (1) every attempt an agent makes costs compute and time, so iterations need to be cheap and efficient to run; and (2) code review become a critical gate, so the code needs to be succinct, readable, and correct. Apache Spark® offers two programming models to author your pipelines, procedural and declarative, and they differ in what you write, in what Spark can check before it runs, and in how much a mistake costs. We benchmarked both with the same agent on the same jobs, and declarative came out safer, cheaper, and leaner.

A procedural pipeline is code that tells Spark how to build each dataset, step by step. The only way to know whether it works is to run it.

A declarative pipeline describes the datasets you want and leaves Spark to decide how to build them. This is akin to when you prompt an LLM, and it figures out how to do it (by using the right skills & tools). This is best illustrated in code to see how a simple typo will fail:

```
bronze = spark.read.parquet(RAW)
bronze.write.saveAsTable("bronze")
silver = 
bronze.withColumnRenamed("revenue", 
"revenues")  # typo
silver.write.saveAsTable("silver")
gold = 
spark.read.table("silver").groupBy("revenue")
.sum("revenue")
gold.write.saveAsTable("gold")  
# runtime error

```

```
@dp.materialized_view(name="gold")
def gold():
    return 
spark.read.table("silver").groupBy("revenue")
.sum("revenue")
```

## 1. Declarative pipelines can be validated before they run

Bugs come in two flavors. Structural ones you can catch by reading the pipeline: an unresolved column reference, a table that doesn’t exist yet, a config change that is not allowed. Silent ones only show up in the output when the run finishes and the answer is wrong.

A declarative pipeline can be checked for structural bugs before it runs, similar to how data flow in a typed language like Rust can be checked at compile time. Because a declarative pipeline is a description rather than a run, Spark can answer three kinds of questions by reading it:

- Every column reference is resolved against the schema of the dataset it reads from, so a column that does not exist is a rejection rather than a runtime failure.
- Every dependency between datasets is matched to a producer in the graph, so a reference to a table that nothing declares is caught before the pipeline starts.
- The graph is checked for completeness and ordering, so the engine determines what runs when rather than trusting the order in which the model happened to write things.

## 2. Declarative pipelines offload boilerplate tasks to Spark

In procedural PySpark, the AI coding agent writes the data operations, such as filtering invalid rows and joining tables. It also writes code to run the pipeline’s steps in the right order and save their results. This supporting code repeats much of the same boilerplate across pipelines.

In declarative pipelines, the AI agent defines each dataset and the query that produces it. Spark handles the execution order and saves the results. With Spark handling that boilerplate, the agent writes less code, and the team has less to review and maintain.

## What we tested

We tested 22 data engineering tasks. Each task looked like a real ticket: it described a problem and specified the table, column names, and data types that the pipeline had to produce. The agent could choose any implementation as long as the output matched those requirements.

For each task, we generated 12 different input datasets with the kinds of messy values found in production data. The agent wrote a new pipeline for every dataset using procedural PySpark and another using Spark Declarative Pipelines. That produced 264 builds per approach and 528 in total: 22 tasks × 12 datasets × 2 approaches. All builds used Opus 4.8.

We ran each pipeline and checked its output against the required table. The automated grader did not know which approach had produced the result. Declarative pipelines first went through Spark's dry run. If a build failed, the agent could revise it and try again, up to a fixed limit.

You can rerun the whole thing yourself from thepublic repository: the setup, prompts, datasets, grader, and the results behind every number.

### Results

Both ways finished nearly every task, with 255 of 264 completed procedurally and 258 of 264 completed declaratively, so either one gets you to a working pipeline. What differs is everything around that: when mistakes surfaced, how much code it took to fix, and how consistent the output was. We cover the three advantages of declarative pipelines below, followed by two caveats.

1. Validating before the run made declarative pipelines ~34x less time

A pipeline's mistakes surface before execution, during a run, or not at all. Procedural pipelines stopped none before execution because they have no pre-execution stage. To find a structural error, Spark had to run the pipeline on a cluster until it reached the broken step.

Across the builds we measured, procedural runs used 596 executor-seconds, compared with 17 for declarative runs. Dry-run validation of declarative code caught structural errors early and reduced compute by 34X.

![Procedural Pipelines](/images/posts/91a3efb950c0.png)

2. Declarative pipeline code was half the size of procedural pipelines

Among the completed builds, declarative pipelines were about half the size, with a median of 64 lines compared with 131 for procedural pipelines.

The procedural implementations also varied more. For the same job, some used Spark transformations while others loaded the data into memory and processed it one row at a time. Both passed on the test data, but the in-memory version can fail when the data grows. Across the benchmark, 19 procedural builds used this shortcut. None of the declarative builds did.

Shorter, more consistent code gives a team less to review and one pattern to maintain.

![Declarative Pipeline Code](/images/posts/8db90a9d69ec.png)

3. On logic errors, the two came out level

Those are the two advantages. When running the tests, we also identified two caveats.

First, a dry run can only catch structural mistakes. It cannot catch a silent one: a pipeline that runs cleanly and returns the wrong answer, which is the more dangerous kind. On that count, the two came out even: their silent-error rates were within roughly 15% of each other, a gap too small to be a real difference. Declarative makes structural mistakes cheap to catch; it does nothing for logic, which still needs tests and review.

4. Declarative spends more up front to save more later

Declarative spends more in one place. The agent iterates on the dry run, retrying until the pipeline is sound, so it does more of its thinking in tokens up front rather than discovering problems on a cluster later. The tokens are a fixed, one-time spend, paid while the pipeline is being written; the amount does not change based on your data size or how often the pipeline runs. Wasted cluster compute is the opposite: it recurs on every bad run and grows with the data, so the more you process, the more a bad build costs. Paying a fixed cost up front to avoid one that keeps growing only looks better as your pipelines and data get bigger.

#### Everything we measured, side by side

The complete set of measured differences is shown below.

[翻译失败，原文如下]

Cluster time:~34x higher (up to ~521 executor-seconds on a failed run)

LLM tokens:baseline

Cluster time:baseline (~0.5 executor-seconds on a failed run)

LLM tokens: ~2.3x (median build ≈ $0.50 vs $0.26, Opus 4.8 list rates)

Lines of code:~51% fewer (median)

AST size:~44% smaller

## Conclusion

At production scale, the declarative approach comes out ahead. It costs about 2.3 times more in LLM tokens, and in exchange, it never spends cluster time on a pipeline that was never going to work. At production scale, the declarative approach proves advantageous by trading slightly higher LLM token costs for guaranteed prevention of wasted cluster time on failing pipelines. This becomes increasingly cost-effective as data volumes scale, since compute waste grows proportionally while token costs remain constant.

If you are evaluating agents for pipeline work, treat how the agent writes as seriously as which agent you pick. A better agent makes fewer mistakes; a declarative pipeline makes the mistakes cheap and catches them before they cost anything.

Therepositorydocuments the design, data, and complete provenance. To get started with your agents using Spark Declarative Pipelines, refer to theofficial programming guideand use theSDP skillwith PySpark.

Do I have to trust the AI agent for this to work?

No, and not having to is the point. The declarative agent only ever writes declarative pipeline code — a description of the tables it wants — and Spark itself checks that description before anything runs. The checker is part of the platform: you are trusting Spark's evaluation of the pipeline, not the model. The agent never runs code or reads your data itself.

Is this only about Spark Declarative Pipelines, or does it apply more broadly?

It applies more broadly to declarative approaches: anywhere you can separate "here is what I want" from "now go build it," so the first part can be checked on its own. You see the same shape in SQL itself, in infrastructure-as-code tools, and in schema-first APIs. Spark Declarative Pipelines is the one we benchmarked, but the reasoning holds for any tool built that way.

The declarative agent uses 2.3x the tokens. Isn't that a dealbreaker?

Not at realistic pipeline sizes. The 2.3x comes to roughly $0.50 in tokens per median declarative build, versus $0.26 for procedural, at Opus 4.8 list rates. One failed procedural run burned about 521 executor-seconds, while a rejected declarative one cost roughly half a second — so avoiding a few bad runs covers a lot of extra tokens, and the gap only widens as data volumes grow. Token prices also move around with whatever model service you use, while compute costs are steadier and easier to plan against.

Data EngineeringandOpen Source

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Built for Agents: The Case for Spark Declarative Pipelines](https://www.databricks.com/blog/built-agents-case-spark-declarative-pipelines)
> 
> 翻译时间：2026-10-24 07:04
