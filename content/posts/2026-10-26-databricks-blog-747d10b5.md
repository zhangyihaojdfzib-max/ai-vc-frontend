---
title: Unify your productivity and AI data with Lakeflow Connect
title_original: Unify your productivity and AI data with Lakeflow Connect
date: '2026-10-26'
source: Databricks Blog
source_url: https://www.databricks.com/blog/unify-your-productivity-and-ai-data-lakeflow-connect
author: ''
summary: '[翻译失败，原文如下]


  - Productivity and collaboration tools hold your most valuable enterprise knowledge,
  but this data has been historically siloed across do...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-27T07:09:09.866532'
---

[翻译失败，原文如下]

- Productivity and collaboration tools hold your most valuable enterprise knowledge, but this data has been historically siloed across dozens of separate applications, behind a custom API integration for every source.
- Lakeflow Connect provides native, fully managed connectors for Atlassian (Jira, Confluence), Microsoft (SharePoint), Google Workspace (Drive, Outlook, Gmail), GitHub, and major AI providers (OpenAI, Anthropic) with unified governance and no infrastructure to manage.
- Since both unstructured and structured data lands directly in Unity Catalog, data teams can easily power enterprise knowledge bases, AI agents and developer productivity dashboards without building or maintaining custom data pipelines.

This is the second post in our series on how Lakeflow Connect brings fully managed data ingestion to every line of business. Following our deep dive intounifying marketing data, this post focuses on unlocking the enterprise knowledge trapped within your organization's productivity stack. We’ll explore how native connectors for wikis, project management tools, and AI foundation models give your downstream AI agents the complete business context they need.

## One platform, any source

![Screenshot of Jira connector from Lakeflow Connect](/images/posts/c2753be5ddca.png)

Lakeflow Connectprovides a comprehensive suite of fully managed native connectors across SaaS applications, databases, and file sources that ingest your data directly into theDatabricks Platform. Each connector can be set up via a point-and-click UI or a simple API. From there, your data is incrementally ingested as governed, managed tables inUnity Catalog, with no infrastructure for you to provision, manage, or scale.

![Any SaaS, database, or file source on one platform](/images/posts/91b348cf74eb.png)

Prioritized by customer demand, Lakeflow Connect's ingestion connectors span every line of business, including Customer 360, Operations, Finance, and Productivity—the stack closest to day-to-day work.

## One platform, every productivity tool

The average company's productivity stack is a sprawl of project trackers, wikis, document stores, inboxes, and AI tools, each holding only a slice of how work gets done. Getting that data out has historically required a patchwork of custom pipelines that are slow to build and painful to maintain. The bar is high enough that the most impactful use cases stay out of reach, for example: AI agents powered by your enterprise's internal knowledge or visibility into operational analytics.

Lakeflow Connect resolves this by providing built-in connectors to ingest seamlessly from across the productivity stack:

- COLLABORATION:How does work get tracked and shipped?Jira,Monday.com,Smartsheet,Aha!, andGitHub
- ENTERPRISE KNOWLEDGE:What collective expertise does your company run on?Confluence,Notion,Glean,SharePoint, andGoogle Drive
- EMAIL:How do your teams communicate?OutlookandGmail
- AI:How is your organization adopting AI?OpenAIandAnthropic

![Productivity data in, governed AI and analytics out](/images/posts/cea17d90ae1e.png)

With this breadth of connectors, Lakeflow Connect becomes the ingestion engine that brings scattered productivity data into one governed foundation, without the integration bottlenecks that traditionally slow teams down.

For example,Toyota Finance Australia, the financing arm of one of the world's largest automakers, uses Lakeflow Connect to bring its Jira data into Databricks as a fully managed, zero-maintenance pipeline.

Another customer,VaxCare, a vaccine management company runs the largest primary-care vaccination network in the U.S., and uses Lakeflow Connect's Confluence connector to feed its internal knowledge base into Databricks and ground an AI agent in it.

## Unstructured content, AI-ready out of the box

AI agents can provide instant, grounded answers from your company's collective knowledge without employees having to hunt across wikis, drives, and inboxes. But an agent is only as good as the data behind it, and most of that is unstructured. With Lakeflow Connect, this is not a problem; our connectors can land unstructured content like files, pages, and messages as governed tables in Unity Catalog. The exact data, and the format it arrives in, varies by source:

- SharePoint: The SharePoint connector brings in the unstructured files themselves (PDFs, Word documents, slide decks, and images). Each unstructured file lands as one row, with its raw bytes stored in acontentcolumn (either asBINARYorFILEtype), with per-file metadata stored alongside. Structured files (Excel files, CSVs, etc.) can also be landed directly as Delta tables.
- Google Drive: The Google Drive connector works the same way for unstructured files, landing each document’s raw bytes as one row in acontentcolumn. Structured files (Google Sheets, CSVs, etc.) can also be landed directly as Delta tables.
- Confluence: The Confluence connector brings in the content of every page and blog post asSTRUCTtype in abodyfield of thepagesandblogpoststables.
- Outlook: The Outlook connector stores the email body in afull_body_contentcolumn as a text string (either HTML or plain text), and it stores the attachments in anattachmentscolumn asBINARYtype. Both live in theemail_messagestable.
- Gmail: The Gmail connector brings in the full message body as a text string, held in themessagestable. It also ingests a reference to each attachment as anattachmentId.
- GitHub: The GitHub connector brings in repository text files (source code, Markdown, and config), stored in thecontentcolumn of therepo_contentstable.

Whatever the source, the content lands in Unity Catalog as a governed table, where you can begin to transform it for downstream AI use cases.

- Text that comes in (like Confluence pages, email bodies, and GitHub source files) is ready to chunk and embed after light cleanup.
- On the other hand, document files that arrive as raw bytes (like the files from SharePoint and Google Drive or the attachments from Outlook), are first turned into text withai_parse_document, Databricks' built-in document intelligence.

Either way you end up with text you can index for retrieval and put behind an agent. For a deeper look at document processing, watch this on-demand session,Intelligent Document Processing with Lakeflow; and for more on how to get started, read thedownstream RAG guide.

M3 Accounting, a leading provider of hospitality software, uses Lakeflow Connect's GitHub and SharePoint connectors to unify its engineering and product documentation into Databricks.

## Govern what you spend on AI with Lakeflow Connect

As AI agents and generative tools spread across teams, so do the questions about the models powering them: what are we spending, who's using what, is it compliant? To help answer these, Lakeflow Connect provides connectors for the biggest foundation model providers:

- OpenAI: The OpenAI connector brings in usage, costs, API keys, projects, users, and audit logs, so you can attribute AI spend by team and track adoption.
- Anthropic: The Anthropic connector brings in audit logs, your organization's users and roles, and the content of claude.ai chats and messages, so you can govern how the tool is used.

Concretely, this enables a single, unified view of how AI usage and adoption are trending within your organiztion, so you can measure and report the ROI of your AI investments to stakeholders.

## Build a complete picture of your Atlassian data

Lakeflow Connect’s depth of ecosystem coverage also extends to Atlassian—one of the most widely used suites in any engineering or product org:

- Jira:The Jira connector brings in issues, comments, sprints, boards, and custom fields, so you can track delivery and build dashboards across projects.
- Confluence:The Confluence connector brings in the full text of pages and blog posts, along with their spaces, labels, and attachments, so your team's written knowledge comes in ready to search and analyze.

[翻译失败，原文如下]

With both connectors, you get a complete picture of your Atlassian data, the delivery and the documentation that surrounds it, side by side. From there you can track launches, bottlenecks, and resolution times across projects. You can also build AI/BI dashboards, and ask Genie about any of it in natural language.

For example,Digicert, a global leader in digital security, uses Lakeflow Connect’s Confluence connector to reliably power its internal AI Knowledge Assistants without the overhead of custom pipelines.

Another customer,Orizon, a Brazilian healthcare technology company, uses Lakeflow Connect's Jira connector to feed its leadership dashboards.

For a step-by-step setup and tuning guide for the Jira connector, seeUnify Your Engineering Data: Jira Ingestion Best Practices.

## One foundation, every analytics or AI question

Because every connector lands its data as governed Delta tables inUnity Catalog, the productivity and AI data you ingest becomes part of the same foundation as the rest of your enterprise data. From there you can query it directly in Databricks SQL alongside your other sources, ask questions of it in natural language withGenie One, and ground the agents you build withAgent Bricksin current company knowledge.

And because governance, lineage, and access control all come from Unity Catalog, access stays consistent regardless of the team or tool from where the data originally came.

TRegs, a financial technology platform for treasury, risk, and regulatory reporting, is already building on that foundation.

Lakeflow Connect is actively rolling out new connectors across every line of business, with support for even more connectors coming soon! TryLakeflow Connect for freenow.

Watch for the next post in this Lakeflow Connect blog series to keep learning how to bring all your enterprise data into Databricks and give your AI agents the full context they need.

Lakeflow

---

> 本文由AI自动翻译，原文链接：[Unify your productivity and AI data with Lakeflow Connect](https://www.databricks.com/blog/unify-your-productivity-and-ai-data-lakeflow-connect)
> 
> 翻译时间：2026-10-27 07:09
