---
title: 'Lakebase branching for CI/CD: lessons from 100 PR databases'
title_original: 'Lakebase branching for CI/CD: lessons from 100 PR databases'
date: '2026-10-31'
source: Databricks Blog
source_url: https://www.databricks.com/blog/lakebase-branching-cicd-lessons-100-pr-databases
author: ''
summary: '[翻译失败，原文如下]


  - Snorkel AI''s CI/CD pipeline gives every open pull request its own Lakebase Postgres
  branch, a full read/write copy of production data t...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-03T09:14:48.290001'
---

[翻译失败，原文如下]

- Snorkel AI's CI/CD pipeline gives every open pull request its own Lakebase Postgres branch, a full read/write copy of production data that's ready in under a minute instead of over 30 minutes or longer, due to which they were never able to enable copy per PR.
- Lakebase branches are copy-on-write, so 100 concurrent PR databases on a ~2.5 TB production dataset only add storage for the data each branch changes. Branch expiration (TTL) cleans up each branch automatically when its PR is done, so storage stays close to the size of production plus the changes from active PRs.
- Private connectivity and Okta SSO support provide a governed and secure environment

#### The problem: testing against production data shouldn't take over 30 minutes

Snorkel AI builds data development tools for AI teams, used by expert data annotators and frontier model providers. In this specific use case, Snorkel ships code through a CI pipeline built on Kubernetes. Every open pull request, plus ad-hoc commits, gets its own ephemeral Kubernetes namespace (a "PR namespace"). Developers deploy their branch there and run the full test suite before merging.

These tests are most useful when they run against real data. Snorkel's production database is an Amazon Aurora PostgreSQL cluster. Giving each PR namespace its own copy of that database was the hard part. Restoring a copy took about 20 minutes per environment, which is too slow when developers open PRs all day and the merge queue needs a fresh environment for each run. The alternatives (shared staging databases, trimmed fixtures, or synthetic data) bring back the problems production-like testing is supposed to solve: tests interfering with each other, stale schemas, and bugs that only show up with real data shapes.

#### Success criteria

Snorkel would consider Lakebase a success for CI/CD if it met these criteria:

- Fast provisioning:A new PR branch is ready in under 60 seconds (p95).
- Scale:About 100 concurrent PR branches at peak, each with independent reads and writes.
- Compatibility:The existing application and CI suite run against Lakebase over standard Postgres, with performance comparable to Aurora and support for large JSONB/LOB columns.
- Fresh data:The main branch stays within about 2 minutes of production Aurora through continuous DMS replication.
- Security:Production data stays on private networking and never crosses the public internet, developers sign in with Okta SSO, CI pipelines authenticate as service principals.

#### Why database branching fits CI/CD

Lakebase is Databricks' serverless Postgres database. Its storage and compute are separate, and it supports branching: you can create a new, isolated, writable branch of a database from any point in time, the same way you create a Git branch.

Branches are copy-on-write. Creating a branch is a metadata operation, so no data is copied when the branch is created. A new branch shares storage pages with its parent, and only the pages that the branch changes are written as new storage. For CI, this means:

- Creating a branch takes seconds, not minutes.It doesn't depend on the size of the database.
- Storage grows with the changes each branch makes, not the database size.Each of Snorkel's PR branches writes about 5 to 10 GB of changes on top of a ~1 TB base.
- Compute is per branch and scales to zero.Each branch has its own autoscaling compute, which scales down to zero between CI runs. Even with 100 provisioned branches, Snorkel expects only about 20 to 30 to serve traffic at the same time, at around 5 queries per second each at peak.

#### The architecture

![image1.png](/images/posts/2aa62e0b8d20.png)

1. Keep a fresh copy of production on the main branch.Lakebase is standard Postgres, so it works as a target for AWS DMS with no custom tooling. Snorkel points a DMS task at its production Aurora database and replicates it into the Lakebase project's main branch: a full load first, then ongoing change data capture that keeps main within about 2 minutes of production. Full LOB mode carries over the 10 to 20 MB JSONB values. The team already runs DMS, so there was no new replication pipeline to build or maintain. The main branch is the "golden copy" every PR branch starts from.

2. Create a branch when a PR opens.When a developer opens a PR, the CI pipeline calls the Lakebase API to create a branch from main, sets an expiration time on it, and passes the branch's connection details to the PR namespace. The branch is ready in under a minute.

3. Run tests against real data.The application in the PR namespace connects to its branch over standard Postgres. Tests can run migrations, write data, and change schemas without affecting production, main, or any other PR.

4. Delete the branch when the PR closes or test passes, with TTL as a backstop.When the PR is merged or closed, the pipeline deletes the branch. If that cleanup step doesn't run, the branch expires on its own when its TTL runs out.

#### Security: private networking and identity for humans and pipelines

Two security requirements ruled out other options, so they deserve their own section.

Private connectivity.Production data moves from Aurora to Lakebase, and from Lakebase to the CI cluster, over private networking instead of the public internet.

Identity.Snorkel has two kinds of database users: developers who connect interactively to debug a PR environment, and CI pipelines that run with no human involved. Okta SSO is built around interactive browser login, so we split the design by user type:

- Developers:Okta is federated to the Databricks account, and users are provisioned through SCIM. Developers sign in with their usual Okta identity.
- CI pipelines:Each PR namespace runs as a Databricks service principal (scoped per team or per repo), also provisioned through SCIM. The PR pod uses the service principal's credentials to get short-lived Lakebase OAuth tokens through the Databricks SDK, and refreshes them during long test runs. There are no long-lived database passwords in CI.
- Auditing:Postgres audit logs record the service principal identity for each query, so every query can be traced to the pipeline that ran it.

#### Why copy-on-write and branch expiration keep CI fast and cheap

Two Lakebase features make this pattern work at scale: copy-on-write branching and branch expiration (TTL).

![image3.png](/images/posts/b862827891b6.png)

Copy-on-write makes branches instant.A new branch doesn't copy any data. It points to its parent's existing storage pages, and only the pages the branch modifies are written as new storage. Creating a branch from a ~1 TB production copy takes about as long as creating one from a 1 GB database: seconds, not the ~20 minutes a full restore took. Each PR namespace gets its own isolated, writable copy of production right away.

Copy-on-write makes branches cheap.Every branch shares most of its data with main, so storage grows with the changes each branch makes, not with the size of the database. For Snorkel, that's about 5 to 10 GB per PR branch on top of the shared base. Compute is per branch and scales to zero when idle, so only the branches that are actively running tests use compute.

Branch expiration keeps it cheap over time.Copy-on-write saves the most when branches are short-lived. A branch keeps the version of data that existed when it was created. As DMS keeps updating main with production changes, a branch that stays around keeps holding those older pages, so the storage it uses grows over time. Setting a TTL on every CI branch means each branch is removed automatically once its PR is done. This keeps storage close to the size of the production base plus the changes from active PRs.

#### The same pattern works for AI agents

PR namespaces aren't the only workloads that need a disposable copy of production. AI agents that write SQL, run migrations, or change data also need a safe place to try things, and copy-on-write branching gives them one.

[翻译失败，原文如下]

One branch per agent task.Each agent run gets its own branch of main. The agent can read real data, write to it, and even change the schema without touching production or any other agent's work. Creating a branch takes seconds no matter how large the database is, so it's practical to create one for every task.

Many agents in parallel.Storage only grows with the pages each branch changes, and each branch's compute scales to zero when it's idle. Running dozens of agents side by side costs about as much as the changes they make, not dozens of copies of the database.

Review the changes, or throw them away.Teams can check what an agent changed on its branch before applying anything to production. If the result isn't right, they delete the branch, and there's nothing to roll back.

TTLs clean up after agents.Agents can create a lot of short-lived branches. An expiration on each branch removes the abandoned ones automatically, the same way TTLs clean up CI branches.

Scoped identity for agents.Like CI pipelines, agents can run as service principals with short-lived OAuth tokens, so every query an agent runs can be traced in the audit logs.

#### Results

- Provisioning time:over 30 minutes before, under 60 seconds with Lakebase [VERIFY p95 measured]
- Scale:Designed for about 100 concurrent PR branches on a ~2.5 TBproduction dataset
- Compatibility:CI suite runs against Lakebase with "no major compatibility issues" / perf compared to Aurora
- Adoption:Rollout to 60 to 70 developers across teams
- Developer quote:"Previously we had to physically copy data and those copying jobs took hours and frequently ran into network and other bottlenecks with various CI platforms (github actions, circle ci etc). We were looking for a solution that passes our security and compliance requirements if data leaves our VPC"

#### Best practices for Lakebase branching in CI/CD

1. One branch per PR, created from a continuously synced main branch.
2. Always set a TTL.Treat expiration as required, not optional. Match it to how long a PR or test run usually lasts.
3. Create a new branch instead of keeping an old one.If a PR needs fresher data, create a new branch from main. It takes seconds.
4. Let compute scale to zero.Most provisioned branches are idle at any given moment.
5. Use service principals and short-lived OAuth tokens for pipelines,and SSO for people.
6. Monitor storage per branchto catch long-lived branches early.

Ready to give every pull request its own production-like database?Get started with Lakebaseand read the branching documentation to set up branch expiration in your CI pipeline.

Technology

---

> 本文由AI自动翻译，原文链接：[Lakebase branching for CI/CD: lessons from 100 PR databases](https://www.databricks.com/blog/lakebase-branching-cicd-lessons-100-pr-databases)
> 
> 翻译时间：2026-11-03 09:14
