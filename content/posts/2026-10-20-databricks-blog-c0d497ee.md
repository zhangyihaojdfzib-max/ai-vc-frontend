---
title: How Hamlet uses Databricks Lakebase Postgres to test changes against production
  data
title_original: How Hamlet uses Databricks Lakebase Postgres to test changes against
  production data
date: '2026-10-20'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-hamlet-uses-databricks-lakebase-postgres-test-changes-against-production-data
author: ''
summary: '[翻译失败，原文如下]


  - Hamlet gives every pull request its own Lakebase Postgres branch of production
  data, so engineers test changes against the data that ca...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-21T06:58:28.075436'
---

[翻译失败，原文如下]

- Hamlet gives every pull request its own Lakebase Postgres branch of production data, so engineers test changes against the data that caused a bug without touching production.
- AI coding agents run the pipelines and check their work on each branch before a person approves the merge.
- Hamlet is exploring Lakebase Search for vector and text search in Postgres, branching for object storage and a home for longer agentic jobs.

Hamlet, an AI-powered platform that makes local government decision-making accessible and searchable, uses DatabricksLakebase Postgresto give every pull request its own branch of production data. Engineers and AI coding agents test changes against real data without touching production, and a person still approves every merge.

I spoke with CEO Sunil Rajaraman, Lead Developer Erich Douglass and Senior AI Engineer Jeff Hui about how they work.

## What is Hamlet?

Hamletis an AI-powered technology platform that makes local government decision-making accessible and searchable. By indexing and transcribing thousands of city council, planning commission, and zoning board meetings across the U.S., Hamlet allows real estate developers, journalists, researchers, and citizens to instantly search meeting transcripts, track local policy developments, and set up real-time alerts for specific topics, addresses, or businesses.

## Why is local government data so hard to standardize?

Sara Steffen: Hamlet indexes meetings from more than 7,200 governing bodies across every state. What does that data landscape look like, and why is it so hard to make sense of?

Sunil Rajaraman: There are 19,000 city governments, 3,000 county governments and roughly 80,000 special districts in the United States. Pick any two of their websites and they won’t look alike. That’s the original sin of local government. A handful of CMS providers decided every site should be different, and the result is an internet of government that’s completely balkanized. Hamlet pulls all of it together and standardizes it.

## How is a civic intelligence platform different from a transcription tool?

Sara: Hamlet describes itself as a civic intelligence platform. How is that different from a transcription tool, and why does the distinction matter?

Sunil: A lot of govtech companies are an arbitrage of municipal data. They write brittle scrapers for 1998-era websites and put a modern coat of paint on top. Scraping and storing the data doesn’t add much on its own. You have to tell a story, and it has to be based on fact. That means knowing who’s speaking and how they feel about an issue. If you’re a developer, you want to know whether a council member will approve your housing project, why or why not, and what history the city has that might make it hesitate.

Look at permitting. A lot of venture money has gone into permitting data, and permitting timelines have still gotten worse over the past decade. Many companies have built monuments to the symptoms. We want to get to the underlying problem, which is understanding people. The question we’re trying to answer is how cities fundamentally work.

## What makes messy public data so hard to work with?

Sara Steffen: What makes local government data so difficult to work with?

Sunil Rajaraman: Pick any two of their websites and they won’t look alike. Hamlet pulls it all together and standardizes it.

Erich Douglass: You can’t just integrate with one provider. Seven or eight of them cover about 75% of the market. After that it’s a massive long tail of custom setups. Sometimes a clerk uploads a PDF of the agenda. Sometimes they scan a paper copy and upload that. You get some really weird artifacts.

## What do customers need from meeting data?

Sara: What do customers need from that data?

Sunil: Our customers are private companies like real estate developers, data center developers and retailers. Nearly all of them are trying to get a project approved faster or find a new opportunity. Without Hamlet, someone sits through hours of meetings, waits for their project to come up and watches the officials’ body language. We identify who spoke, take you to the timestamp and show you the receipts.

Erich: They also want precedent. Has a project like theirs been approved or rejected before? Why? What changes did the council ask for? If we can show what’s really going on, that’s a lot of value.

## How does Hamlet keep AI answers tied to the source?

Sara: How do you help customers trust the insights they find?

Jeff Hui: We use it in almost every part of the process. Early on, Hamlet did this work by hand, and that doesn’t scale to thousands of places. For a lot of these governments, the video is the primary source of truth. Getting it into a structured form we can use is the most important part. The average meeting runs about three and a half hours. Nobody wants to watch all of it. AI points people to the parts worth their time, and the video is always there to back it up. We can show exactly what was said, which a lot of AI systems struggle to do.

## Context makes the difference

Sara: How do you identify speakers accurately across thousands of meetings?

Jeff: Context makes the biggest difference. For speaker identification, we know which council or committee is meeting and who was on it at the time. That helps with names, which are hard to get right even for a person listening to a recording. You can’t hand a model a video and hope for the best. You have to collect everything around it that helps it make the right call. It’s a forever challenge.

## Checking AI interpretations

Sara: How do you check the AI’s interpretation of what officials say?

Sunil: Accurate transcription comes first. For sentiment, we use multiple AI models to confirm a comment is about a given topic, say data centers. Then they look at the surrounding context to decide whether it’s for or against.

You also have to define what pro and anti mean before you ask. Take policing. What does being for it mean? We put a lot of care into those questions. Several models now review every sentiment figure before we publish it, and we require high confidence.

## How does Hamlet use Lakebase Postgres?

Lakebaseis the managedPostgresdatabase Hamlet uses to give each pull request its own branch of production data. Engineers can test changes against the data that caused a bug without touching production, while AI coding agents run the pipelines and check their work before a person approves the merge. The team says its previous test-data setup could take several hours per engineer each week.

## How does Hamlet use Lakebase data branching?

Sara: Why did you choose Lakebase, and what changed for your team?

Erich: We had a pretty standard setup on AWS RDS, with one production instance and one staging instance. A lot of our work is tuning data pipelines against very specific data. For every pull request, we’d spend 15 to 30 minutes getting staging into the right state before we could run validations. We’re a small team, and velocity matters to us more than almost anything.

Data branching was the feature that sold us. Every pull request now gets its own branch of production data, connected to its preview environment. When the preview deploys, it’s ready. We can test against production data and even write to it without touching production.

Autoscaling helps too. On RDS, a bigger instance meant a migration that could take a couple of hours. Now we move a slider and get twice as big an instance.

Jeff: The 15 to 30 minutes was the best case, when you happened to copy exactly the right data. Each engineer could spend several hours a week keeping test data current, including cloning pieces of production locally to chase down issues. Now when we hit a bug, we have the exact data that caused it, and we can check the fix against that same data.

## How do AI coding agents test on Lakebase branches?

Sara: How does Lakebase change the way your AI coding agents work?

[翻译失败，原文如下]

Jeff: Branches make our workflow a much better fit for AI coding agents. Each pull request is isolated from production. We give an agent like Claude or Codex access to its branch and let it run its own checks. It runs the data pipelines to completion and looks at whether the change does what it should. Every pull request gets that first pass from an agent. By the time a person looks at it, we’re already fairly confident it works. A human still approves the merge. More and more of the rest is automated, and Lakebase is a big part of what makes that possible.

## What is Hamlet exploring next?

Sara: What are you exploring next with Lakebase?

Erich: Right now most of our data lives in a relational database, and search runs on a separate vector database. The two drift out of sync. Testing search becomes the old staging problem again. I’ve been trying out Lakebase Search which combines vector and text search in Postgres, and having it all in one place has been great.

Sara: Beyond search, what would you like to simplify next?

Erich: Branching has worked so well that we’d love the same thing for the large files we keep in object storage. Every developer has test buckets next to one shared production bucket, and managing state across them is hard.

Jeff: We’re also looking at where to run longer agentic jobs. Part of our ingestion uses AI to drive a web browser and find the right content on government sites. Some runs take a few minutes. Others take 30 or 40, and our current AWS Lambda setup has a 15-minute limit.

## How does Lakebase speed up the path from evidence to insight?

Hamlet’s work starts with the original meeting recording, so customers can trace an AI insight back to what an official said. Lakebase supports the engineering workflow behind that experience: branches of production data let developers and coding agents test changes without touching production, while people still approve the final merge. For a small team working across thousands of governing bodies, that means less time preparing test data and more time improving the product.

## Frequently asked questions

How can you create and automatically delete a Lakebase branch for every pull request?

Add two steps to your continuous integration (CI) pipeline: create a branch from production when a pull request (PR) opens and delete it when the PR merges or closes. You can script both steps with theDatabricks CLIand run them from a tool such asGitHub Actions. Set an expiration, a time-to-live (TTL), when you create the branch so it deletes itself even if the cleanup step never runs. See thebranch-based development workflowtutorial for a full example.

How does database branching work in Postgres?

A Lakebase branch is an independent Postgres environment that starts with the schema and data of its parent and shares storage with it through copy-on-write. Only changes made on the branch are written separately, so creating a branch does not depend on database size. Standard Postgres creates a new database bycopying an existing one, which duplicates the data. Lakebasedatabase branchesavoid that copy, and changes in a child branch never affect its parent.

How do you roll out database branching to a development team?

Start with one branch per pull request, the pattern Hamlet uses, then extend branching to the rest of your workflow. Each pattern replaces a shared staging database with isolated environments.

- One branch per pull request:CI creates the branch when the PR opens and deletes it when the PR closes.
- One branch per developer:each engineer gets an isolated environment with production-like data, and you can reset it from its parent to pull in the latest schema and data.
- One branch per test run:each CI run starts from a fresh, isolated database with no leftover state.

How much does a Lakebase branch cost?

Cost depends on compute and storage. Each branch has its own compute, which scales to zero when idle, so you pay only for active compute hours. For storage, an expiring branch is billed only for the data that changes on it, while a permanent branch with no expiration is billed for its full data size. Keep an expiration on short-lived branches. Seebranch expirationfor the options.

Can AI coding agents test on a Lakebase branch without touching production?

Yes. Each branch is isolated from production, so an agent can apply migrations, run tests and retire the branch when it finishes. A person still approves the merge, and schema changes move to the parent branch through migrations in code rather than by merging the branch.

To learn more about Lakebase, visit theLakebase Postgresproduct page.

Customers

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[How Hamlet uses Databricks Lakebase Postgres to test changes against production data](https://www.databricks.com/blog/how-hamlet-uses-databricks-lakebase-postgres-test-changes-against-production-data)
> 
> 翻译时间：2026-10-21 06:58
