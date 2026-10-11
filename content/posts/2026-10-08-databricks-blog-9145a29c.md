---
title: 'Lakebase and Agentic SDLC: Branching Databases for Coding Agents'
title_original: 'Lakebase and Agentic SDLC: Branching Databases for Coding Agents'
date: '2026-10-08'
source: Databricks Blog
source_url: https://www.databricks.com/blog/lakebase-and-agentic-sdlc-branching-databases-coding-agents
author: ''
summary: '[翻译失败，原文如下]


  - Why the database is the overlooked bottleneck when running coding agents in parallel,
  and how Lakebase copy-on-write branching (sub-sec...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-11T08:06:34.855768'
---

[翻译失败，原文如下]

- Why the database is the overlooked bottleneck when running coding agents in parallel, and how Lakebase copy-on-write branching (sub-second, scale-to-zero) gives every agent an isolated database.
- An end-to-end development loop: Git worktrees + a Claude Code hook that auto-creates a Lakebase branch per agent, then GitHub Actions that create an ephemeral branch per PR, run Drizzle migrations, deploy a preview app on Databricks Apps, and post a schema diff.
- Further branching workflows: point-in-time bug reproduction, safe schema-migration testing, and production-derived data with Unity Catalog masking.

AI has changed how software gets built. As coding agents take on a growing share of development work, developers are increasingly shifting toward orchestrating them. Running multiple agents in parallel is becoming the norm, and the tooling has evolved with it, from skills and hooks to MCPs, subagents, all designed to make agents safer and more effective.

Yet, one mission-critical part in the development workflow is still often overlooked: the database.

Each concurrent agent needs to write code, apply schema changes, and run tests against a database. With shared environments, such as a single development or staging database typical of traditional database setups, this creates real challenges. Agents can conflict on schema changes, interfere with one another's, or fall back to mocks that do not reflect real-world data. These were already pain points for developers, but they are exacerbated by coding agents. Agents move faster, operate in parallel and need a safe environment to avoid putting production data at risk or exposing sensitive data.

TheLakebase Postgresarchitecture solves this with database branching. Just as Git lets you branch code, Lakebase lets you branch an entire database in under a second, regardless of its size. It uses copy-on-write, so branches share the parent branch data but only consume additional storage as they diverge. In addition, they can scale-to-zero, meaning idle branches incur no compute cost. This is important as you run several agents at the same time. Each branch is fully isolated, allowing an agent to apply migrations, run tests, and retire the branch when they’re done.

In this article, I'll show you what this looks like in practice with an end-to-end workflow for a Lakebase development loop built around coding agents. Anexample repositoryis available here with examples of Github Actions workflows to achieve what is described in the following sections.

Prefer to see it in action? Watch the video walkthrough below.

Before we dive in, a note on environments with Databricks. A common setup when using Lakebase Postgres is to use one Databricks workspace per environment, such as dev, staging, and prod. Most teams will want to leverage workspaces for various reasons like security and compliance, although it is also possible to use a single workspace. Similarly, branching from a seeded database instead of the production database is also common, to avoid exposing sensitive data like PII. In this article, we’ll use a single workspace for simplicity, but the same core concepts apply to multi-workspace setups and can be implemented just as easily.

![Figure 1: Development Loop with Lakebase branching: Every agent and PR gets an isolated ephemeral database.](/images/posts/831e154e449c.png)

## Safe, Isolated Databases for Parallel Coding Agents

The main disruption to traditional databases comes from multiple coding agents working concurrently. When developing new features or fixing issues, each agent often needs to read the database schema, apply changes, seed data, and run tests. Without isolation, these agents can interfere with one another or corrupt a shared database. Database branching gives each agent an isolated environment to work independently without affecting other agents running at the same time.

A practical way to avoid code conflict locally is to leverage Git worktrees. A worktree gives each agent its own directory with its own branch checked out, so there's no file-level conflict between them. Git worktrees solve code isolation for parallel agents. Lakebase branching solves the other half: database isolation. By adding a post-checkout hook to the repository, each new worktree automatically gets its own database branch. Once the development is done, the agent will open a PR. Agent behavior can be guided through repository instruction files such as AGENTS.md orCLAUDE.md.

![Figure 2: A branch per agent set up using Git worktrees, Lakebase branching and Claude Code hooks and Github Actions.](/images/posts/4b0a853e0488.png)

Here is an example workflow usingClaude Code, worktreesandLakebase branchingfor safe AI development:

- Agent runs claude -worktree feature-123
- Git creates a worktree for the feature-123 branch
- Apost-checkouthook fires automatically, creating a database branch
- The agent now has its own code directory and its own database fully isolated

![Figure 3: Claude sessions running in parallel using Git worktrees and Lakebase branches for isolation.](/images/posts/99aade00fb34.png)

When the agent is done, it will create PR. This behavior is provided in therepository instruction file. Once the PR is created, both the worktree and the database branch can be retired. One important difference from Git is that Lakebase branches are not merged back to the main branch. Because the parent and child can both change independently, reconciling their data can quickly become impractical. Instead, schema changes are tracked in code alongside the application logic, then promoted to the parent branch through migrations using tools such as Drizzle, Flyway, Liquibase, or Alembic.

In our example, we use Drizzle. When a schema change is needed, the agent adds the corresponding migration to the codebase. The deployment automation then applies that migration when deploying the preview application and again when the change is merged into the main branch.

## Ephemeral Databases for Every Pull Request

Once a Pull Request (PR) is opened, we want to automatically validate and test the code against a real database before anything reaches production.

Using continuous integration tooling, in this case, Github Actions, an ephemeral Lakebase branch is created for each PR, as a child of the production branch. That branch becomes the database environment for the PR. Automated tests can run against it, a preview application can be deployed, and reviewers can validate the change against a real database.

Because the branch starts from production, the schema migration can also be applied and tested before the change reaches production.

Once the PR is approved and merged, the feature code and migration instructions are promoted, and the temporary Lakebase branch is deleted.

A commonGitHub Actionsworkflow looks like this:

- A PR is opened against main
- CI calls the Lakebase CLI to create a branch like pr-123
- The migration tool (Drizzle, Alembic, etc.) runs against the new dedicated database branch
- A preview app is deployed, pointed at the branch's connection string
- A schema diff is generated and posted as a PR comment showing exactly which tables, columns, or indexes changed
- The reviewer validates both the code and the database changes
- When the PR is closed or merged, CI deletes the branch

![Figure 4: Schema diff comment generated in the Pull-Request](/images/posts/4d8bdc12b87c.png)

In the repository example, we deploy the application withDatabricks Apps, but the concept applies to any other hosting platforms like Vercel, Netlify, Cloudflare and more.

## Bug Reproduction, Migrations, and Testing with Database Branches

[翻译失败，原文如下]

Beyond development tasks, database branching can support several other useful workflows. These are not implemented in the example repository, but they can be valuable additions to a Lakebase development workflow. For example, with database branching, you can create an isolated branch from production at a point in time, typically right before a bug appeared, and investigate the issue against the real data, reproduce the bug safely, and retire the branch once the fix is validated.

Branching can also make schema migrations safer. Before deploying a change to production, you can automatically create a database branch, apply the migration, run tests, and verify that the application still behaves as expected. Once the migration is validated, the same change can be promoted to production.

These workflows are powerful because they let developers work with production-like, or production-derived data using Unity Catalog masking for example, without putting the live database at risk. Each branch is isolated, ephemeral, making it a safe environment for debugging, testing, and validation.

## Conclusion

Together, these patterns form the Lakebase development loop: a branch per agent, a branch per PR, and isolated branches for production validation.

For the Agentic SDLC, database branching provides a safe and flexible foundation for development teams working with coding agents.Try branching out for yourself.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Lakebase and Agentic SDLC: Branching Databases for Coding Agents](https://www.databricks.com/blog/lakebase-and-agentic-sdlc-branching-databases-coding-agents)
> 
> 翻译时间：2026-10-11 08:06
