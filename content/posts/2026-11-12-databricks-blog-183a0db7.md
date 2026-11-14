---
title: How H6.ai builds AI-powered financial automation with Lakebase Postgres
title_original: How H6.ai builds AI-powered financial automation with Lakebase Postgres
date: '2026-11-12'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-h6ai-builds-ai-powered-financial-automation-lakebase-postgres
author: ''
summary: '[翻译失败，原文如下]


  - H6.ai gives every customer a dedicated Lakebase Postgres database, which keeps
  each customer''s financial data isolated on a multi-tenan...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-14T08:49:36.744496'
---

[翻译失败，原文如下]

- H6.ai gives every customer a dedicated Lakebase Postgres database, which keeps each customer's financial data isolated on a multi-tenant AP automation platform.
- Copy-on-write branches save the exact database state behind any invoice issue, so the team can replay real customer cases without mocks and without touching live data or the ERP.
- Disposable, schema-migrated branches and a panel of AI judges let H6.ai test new models and engine changes against real cases before they reach production.

Traditional accounts payable and invoice processing tools often force companies into a trade-off: moving quickly using AI automation and risk losing control, or maintaining tedious manual oversight.H6.aiwas founded to solve this problem.

H6.ai automates accounts payable on top of a company's existing ERP. It reads each invoice, matches it to a purchase order, assigns its lines to the right accounts and checks it against the company's own policies. Our approach combines AI-assisted understanding with approved, deterministic and auditable policy execution. Our challenge was finding a backend solution that could support frequent regression testing at scale.

## The challenge: financial data never stands still

In this industry, no two customers look alike. Each has its own ERP, suppliers, purchase orders, chart of accounts and policies. Invoices range from a one-line service bill to documents with hundreds of lines.

And the data keeps moving. At 10 AM an invoice matches an open purchase order with enough quantity left. By the afternoon that order may be partly consumed, amended or closed. Process the same invoice again and the answer changes, even though our code has not.

That makes regression testing hard. When a result changes, we need to know whether our change caused it or the customer's data did.

## The solution: Lakebase architecture

Our engineering team needed a scalable solution that could isolate our customers' data and allow us to investigate errors. After learning about thelakebase architecturewhich separates storage from compute, scales idle compute to zero, and enables branching, we selected it as the core system of record for our platform.

Today, every H6.ai customer has a dedicatedLakebase Postgresdatabase. It holds their whole financial context: purchase orders and suppliers synced from the ERP, the chart of accounts and dimensions, past transactions, and their H6 policies. A database per customer keeps each customer's data isolated.

It also allows us to freeze snapshots. ALakebase branchis a copy-on-write copy of a database at a point in time. Creating one copies no data: the branch shares storage with its parent and only stores what changes on it.

When we find an invoice H6 handled incorrectly, we branch that customer's database and keep the branch as a snapshot. A purchase order that was open stays open in the snapshot, with the same remaining quantities and prices, even after the ERP closes it. The same holds for suppliers, accounts, dimensions, history and policy settings. We no longer try to recreate the conditions behind an issue. We keep them.

![image1.png](/images/posts/8d07beb3ae63.png)

Every box in the shaded band is a branch of the same customer database. The harness branches the live database once to take a snapshot and never writes to it. Everything a test writes stays on its own run branch and is deleted with it.

## How an invoice processing test runs

Each test case in our harness pairs one invoice with one snapshot and the outcome we expect: which purchase order it should match, which accounts its lines belong to, and whether it should be held for review. A run has four steps:

1. Bring the snapshot up to date.Our database schema keeps evolving, so a snapshot taken months ago is behind the code under test. We branch the snapshot once, apply the current migrations to that branch, and reuse it for every run on the same code version. We migrate once and fork many times. The snapshot itself is never changed.
2. Fork a run branch.Each run gets its own short-lived branch of that up-to-date copy.
3. Process the invoice for real.The candidate version of our pipeline reads and writes the run branch as if it were the customer's database. It extracts, matches, classifies and validates the original invoice file exactly as it would in production.
4. Judge the result and delete the branch.We compare what the pipeline did with what we expected, then delete the run branch. The snapshot stays as it was, ready for the next run.

A test plan can mix cases from many customers, ERPs and invoice formats, each running against its own preserved database. Because every run starts from the same frozen state, the same test gives the same starting point today, next week and next quarter.

## Protecting financial data

We don't mock the database or the pipeline. Isolation does that job. Everything a test writes (review items, validation results, draft documents) lands on the run branch and is deleted with it. A test never posts to the customer's ERP, and the live database is never written to.

This matters for a financial platform. We can test against copies of production customer data with the same code paths production uses, while the customer's books stay untouched. Branch management uses dedicated service principals with least-privilege access, and the branching guards refuse to touch a customer's live branch.

## Testing AI beyond pass or fail

Checking that an invoice was processed is not enough. An invoice can be read perfectly and still be matched to the wrong purchase order, assigned to the wrong account, or processed in breach of the customer's policies.

So each run is judged two ways:

- Deterministic assertions check the facts we can state exactly, such as the document's final status, the purchase order it matched and the totals.
- A panel of AI judges built on models from different providers reviews the full outcome against the expected result and returns pass, fail or inconclusive, with its reasoning.

Together they tell us whether the outcome was right, not only whether processing finished. That lets us try new models, improve extraction, cut cost and change our matching and policy engines, and spot a regression on a real customer case before it reaches production.

## Every unusual invoice becomes a regression test

We don't fix an issue and move on. We keep its database state as a snapshot, add the invoice and the expected outcome, and it becomes a permanent test case. As we onboard more customers, ERPs and invoice formats, test coverage grows with the complexity of the businesses we serve.

Lakebase Postgres gives us four things we rely on:

- Isolation:one database per customer, as a multi-tenant financial platform needs.
- Frozen state:a branch keeps the exact financial picture behind an issue, however much the live data changes afterwards.
- Cheap, disposable copies:copy-on-write branches let every run start from a clean, identical state and be thrown away afterwards.
- Schema-safe replays:an old snapshot can be migrated forward on its own branch, so it stays usable as our code evolves.

For H6.ai, Lakebase’s database branching isn't just an infrastructure convenience. It is how we build AI-powered financial automation that customers can trust.

In the future, we look forward to leveraging Lakehouse//RT queries on Lakebase tables which will allow us to run read-only analytical queries on Lakebase without copying data. This will allow us to get fresh analytics without a pipeline.

If you’d like to learn more about what we are building at H6.ai, visit ourwebsite. If you want to learn more about database branching with Lakebase Postgres, watch thisvideo.

1. What is a lakebase?

[翻译失败，原文如下]

A lakebase is a transactional database that keeps its data on the lake, for a modern, agentic app stack. Traditional databases run on single machines. A lakebase runs a stateless database engine and keeps data in durable cloud object storage, so compute can scale on its own and storage is used on demand.

2. What is Lakebase Postgres?

Lakebase Postgres is a fully-managed, serverless Postgres database integrated into the Databricks platform. Teams use it to build real-time transactional applications alongside their lakehouse data. It includes autoscaling, scale-to-zero, instant branching, read replicas, instant restore, high availability and native Unity Catalog integration.

3. Is Lakebase Postgres a good fit for AI use cases?

Yes. Lakebase serves as the backend for agent memory and real-time feature serving. Agents can store conversation state and long-term memory in Postgres, and models can read low-latency feature data through online feature stores powered by Lakebase. Branching also makes it easier to test AI systems. H6.ai, for example, replays real invoice cases against frozen database snapshots to catch regressions when it changes models or logic.

4. How does branching work?

A Lakebase branch is an instant, isolated copy of a database, much like a Git branch for your data. It uses copy-on-write: a new branch shares storage with its parent, and only changed data is written separately. As a result, branches appear instantly no matter how large the database is, and creating one doesn't slow down production. Teams use branches for development, testing and schema changes. They can also create a new branch from any point in time within the history window.

5. Does Lakebase Postgres support multi-tenancy?

Yes, in two ways. You can give each tenant its own database, as H6.ai does with a dedicated Lakebase Postgres database per customer to keep each customer's data isolated. Or you can keep tenants in shared tables and use PostgreSQL row-level security so users see only their own or their organization's data. Scale-to-zero suspends inactive compute, which keeps per-tenant databases cost-efficient.

Customers

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[How H6.ai builds AI-powered financial automation with Lakebase Postgres](https://www.databricks.com/blog/how-h6ai-builds-ai-powered-financial-automation-lakebase-postgres)
> 
> 翻译时间：2026-11-14 08:49
