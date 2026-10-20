---
title: How to get the most out of running dbt on Databricks
title_original: How to get the most out of running dbt on Databricks
date: '2026-10-19'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-get-most-out-running-dbt-databricks
author: ''
summary: '[翻译失败，原文如下]


  - Avoid stitching separate tools together and keep the whole pipeline in one dbt
  project on Databricks, from streaming ingestion through ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-20T07:22:34.451968'
---

[翻译失败，原文如下]

- Avoid stitching separate tools together and keep the whole pipeline in one dbt project on Databricks, from streaming ingestion through governed metric definitions
- Orchestrate dbt natively in Lakeflow Jobs without the need for an external orchestrator.
- Define governance in the dbt project itself, so access rules are enforced by Unity Catalog straight from your project configs.

Tens of thousands of organizations rely ondbtfor data transformation. Where you run it shapes everything: how much it costs to run your dbt pipelines, how fast they ship, and how much operational work they carry. Running dbt on Databricks gives your dbt workloads anopen platform and a unified pipeline.

Over 3000 organizations run dbt on Databricks, and most teams could be getting a lot more out of it. This blog highlights the practices that make dbt pipelines cheaper, faster, and simpler to operate on Databricks.

## Make your dbt pipelines cheaper and faster

dbt bills climb from work you don't need to repeat. Full rebuilds recompute data that hasn't changed, keeping queries fast takes manual-tuning, and when the bill spikes there's no clear attribution back to the dbt models that caused it. Adopt the practices in this section and your pipelines will:

- Rebuild only the data that actually changed
- Stay fast without you choosing or reworking partition keys
- Run table maintenance automatically without post-hooks
- race every dollar of spend to a specific model

### 1. Build only what changed with incremental strategies

Full table rebuilds are the largest avoidable cost in most dbt projects. When only a small fraction of the data changes between runs, recomputing the entire table wastes your compute and increases your bill.dbt's incremental strategies, all supported on dbt-databricks, let each model process only new data, and the right choice depends on how your data actually arrives.

Strategy

Use it when

append

Rows are only ever inserted, never updated

merge

The same key can arrive more than once and needs upserting (slowly changing dimensions, dedupe, late-arriving updates)

replace_where

(dbt-databricks specific)

The model re-derives a narrow time window each run, such as the last few days of activity

insert_overwrite

Your query returns whole partitions

delete+insert

You want records replaced by key, without column-level update logic

microbatch

Time-series data with anevent_timecolumn and structured backfill needs

Most projects default tomergewhen a narrower strategy would do. If you can describe the changed data with a predicate,replace_wheredoes less work than amergethat has to scan the target to find matches. If you can't,incremental_predicateson themergenarrows that scan considerably.

Every strategy above is a decision you make and have to maintain. The next practice lets the platform take care of this for you.

### 2. Let materialized views handle incrementalization for you

Materialized viewsautomate incrementalization. You can define the model as plain SQL, and Databricks tracks which underlying data has changed and refreshes only the affected results. On dbt-databricks, a materialized view is anative materialization, so this is a one-line config change:

Materialized views fit best at the serving layer: aggregations over frequently changing sources, especially the expensive ones that back dashboards and need to stay fresh. In our TPC-DI benchmark, switching full recomputes to materialized views at the serving layer delivered 17x speedup.

![Bar chart showing materialized views at the serving layer delivered 17x speedup](/images/posts/d448d77e93eb.png)

### 3. Automate data layout for performance tuning

Choosing partition keys, reworking them when query patterns change, and schedulingOPTIMIZE,VACUUM, andANALYZEin post-hooks all take engineering time.

Predictive OptimizationrunsOPTIMIZE,VACUUM, and statistics collection on managed tables automatically, choosing what to run and when based on how each table is queried. Enable it once at the catalog or schema level, and the post-hooks that dbt projects usually accumulate for table maintenance can be retired.

For data layout,Liquid Clusteringreplaces partition design with a self-tuning layout. It organizes data based on how the table is actually queried, sidesteps the small-file explosion that over-partitioned tables hit, and adapts as query patterns drift. Or let Databricks choose and adjust them from query history withautomatic Liquid Clustering(CLUSTER BY AUTO), powered by Predictive Optimization. A single project-level config clusters every new table the project builds.

Both features are designed as one-time decisions. WithAutomatic upgrades, Unity Catalog managed tables keep picking up new optimizations as Databricks ships them.

### 4. Attribute every dollar with query tags

At the end of the quarter, finance asks why the warehouse bill went up. In most setups nobody can answer, because a query in the usage data carries no connection to the dbt model that issued it.

Query tagsmake the connection automatic. Every query dbt runs on Databricks isautomatically stampedwith the model name, dbt version, and materialization type. Add your own DIY custom tags for the dimensions your organization budgets by:

The tags surface insystem.query.history, and joining againstsystem.billing.usageattributes serverless warehouse spend to any grouping the tags support: cost by model, by team, by domain, by materialization. You can see exactly which models cost the most.

![Response showing top 10 dbt models by query count (last 90 days)](/images/posts/38a9cee7e9b1.png)

## Simplify your dbt pipelines

A typical dbt setup leans on a stack of other tools: a separate system to ingest the data, an external orchestrator to run the project, BI tools that each redefine the same metrics, and governance that lives outside your dbt project. Each is one more thing to maintain and one more place for things to drift. Adopt the practices in this section and one dbt project will:

- Ingest data directly into the project
- Run and deploy from Databricks, without a third-party orchestrator to maintain
- Serve one governed metric definition to every tool
- Carry its own governance rules, versioned alongside your dbt models

### 1. Bring ingestion into the dbt project with Streaming Tables

Ingestion is the part of the pipeline that has traditionally lived outside dbt, resulting in a split architecture with no single lineage overview. Thestreaming_table materializationremoves that split. A dbt model materialized as a streaming table incrementally picks up new files or events as they arrive, so ingestion becomes just another model in the DAG.

From there the rest of the pipeline (silver and gold models) can reference the streaming table withref(), tests and documentation apply to every layer, and lineage covers the whole path from raw files to the final mart.

![Diagram of a dbt project from ingestion to gold layer](/images/posts/a57626b7bd5c.png)

### 2. Standardize metrics with Unity Catalog Semantics

Every BI tool, agent, or other consumer of data builds their own definitions of metrics, which leads to confusion and disagreement among stakeholders. Ametric viewmoves the definition into one governed place: you declare the measures and dimensions once, and every consumer queries the same logic.

![Diagram showing metric views moving definitions into one governed model](/images/posts/5da5ce9f57d6.png)

dbt-databricks exposesmetric viewsas a native materialization type, so the definition lives in your dbt project, versioned and reviewed like any other model.

Users can pick their own groupings at query time with theMEASURE()function, so the same definition serves the SQL editor, BI dashboards, notebooks, and Genie.

### 3. Orchestrate dbt natively via Lakeflow Jobs

[翻译失败，原文如下]

A dbt run is rarely the whole pipeline. When upstream and downstream steps live in different tools, the overhead adds up: additional tools to manage, pay for, and secure, with scattered lineage.

Lakeflow Jobs collapses that into one Directed Acyclic Graph (DAG) withdbt as a native task. An ingestion task feeds the dbt task and downstream tasks trigger on completion, with dependencies enforced by the platform. The operational layer comes built in with scheduling, automatic retries, run history, and alerts, with no additional infrastructure to maintain. Jobs supports dbt Core and dbt Platform, and support for dbt Core v2.0 is on the way.

![dbt orchestration diagram](/images/posts/edcaed591e33.png)

### 4. Deploy as code with Declarative Automation Bundles

A job assembled by hand in the UI is hard to version, review, or reproduce.Declarative Automation Bundles(DABs) fix this by making the job definition part of the code repository. Lakeflow Job, its schedule, compute settings, and the dbt project, all declared in YAML and deployed as one package.

Deploying with--target devcreates an isolated copy of the whole pipeline;--target prodpromotes it.

Not every model within a project needs to run on every schedule. Tag models by cadence in dbt YAML and give each cadence its own job that builds only the models carrying its tag. Moving a model from daily to hourly becomes a one-line change:

### 5. Define governance in the project

Governance is usually configured after your models run, separate from the dbt project that builds the data. Because governance sits outside your dbt project, it can drift out of sync with your dbt runs.

Define governance in the dbt project where the models already live. As project config, it ships with the code, gets reviewed like the code, and Unity Catalog enforces it on every query.

Tags, grants, and row and column-level protection all can be defined in project-wide config  indbt_project.yml.databricks_tagsdrives classification and policy,grantscontrols who can read the table, androw_filtersandcolumn_maskscontrol what each user sees:

At scale,attribute-based access control(ABAC) removes the repetition. Define one policy on a governed tag and it applies the right row filters and column masks to every table carrying that tag, so a new model taggedpiiis covered the moment it builds. Reach for per-model filters and masks only when the logic is truly model-specific, like multi-tenant isolation.

The common thread across these practices is handing operational work to the platform: incremental processing, data layout, table maintenance, governance enforcement, and orchestration. What stays in your dbt project is your version-controlled and tested transformation logic. Pick the practice that addresses the pain your project has today and start there.

Join the 3000+ organizations already running dbt on Databricks. Get started with thedbt-databricks adapter.

---

> 本文由AI自动翻译，原文链接：[How to get the most out of running dbt on Databricks](https://www.databricks.com/blog/how-get-most-out-running-dbt-databricks)
> 
> 翻译时间：2026-10-20 07:22
