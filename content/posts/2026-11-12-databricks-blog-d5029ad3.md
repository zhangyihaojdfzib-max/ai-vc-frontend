---
title: 'Genie in Slack is now Generally Available: Governed AI cowork, right where
  work happens'
title_original: 'Genie in Slack is now Generally Available: Governed AI cowork, right
  where work happens'
date: '2026-11-12'
source: Databricks Blog
source_url: https://www.databricks.com/blog/genie-slack-now-generally-available-governed-ai-cowork-right-where-work-happens
author: ''
summary: '[翻译失败，原文如下]


  • Genie in Slack is generally available: DM Genie or @mention it in a channel to
  get governed answers grounded in your business context w...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-16T08:50:37.936078'
---

[翻译失败，原文如下]

• Genie in Slack is generally available: DM Genie or @mention it in a channel to get governed answers grounded in your business context without leaving Slack.• From answers to action: Genie updates documents and tickets through MCP connectors after you approve, and works with files and runs analyses on a schedule.• Governed by design: Every question runs with the asker's permissions, so Unity Catalog and source permissions apply in DMs and channels alike.

Many business questions can’t be started and answered within the same conversation. A manager asks her team in Slack why revenue growth slowed last month across active customers. To answer, someone needs to find the right dashboard, check it against the number finance reported, and search last week's meeting notes for the explanation. Two hours later, they paste their findings back into the thread, but the conversation has already moved on.

The delay doesn't come from the question being hard, it comes from having to piece together data from multiple scattered sources. The revenue numbers live in your data platform, the explanation for the slowdown lives in documents and tickets, the definition of “active customer” varies across teams, and decisions happen in Slack.

Today, we’re making it easier than ever for teams to answer questions right where they start, with the General Availability of theDatabricks Genie app for Slack.Genienow answers in the channel, thread, or DM where questions are asked, with the same governedcontextand permissions it uses directly in Databricks.

## Genie brings governed answers into Slack

The Databricks Genie app for Slack brings the power of Genie directly into your Slack workspace. You can start a DM with Genie or @mention it in a channel, and Genie responds directly in the thread, with answers grounded in the governed business context you have access to through Unity Catalog and any outside tool source permissions.

Every answer cites its sources, so you can scan the context Genie used to compile your results without leaving Slack, or click directly on a source to explore deeper in Genie One.

How to Use Genie in Slack

## Collaborate with your team in channels

Teams can work with Genie together in any channel Genie has been added to. Anyone who has connected their Databricks account can type @Genie, and Genie replies directly in the thread with a response. Genie will only read the context of the channels it has been invited to, and responds to each question within the context of the channel it was asked in.

Genie answers in the thread it's called from, so follow-up questions keep their context and move the conversation along. Responses are visible to everyone in the channel by default, giving the team shared context for decisions. For more privacy, admins can set responses to be private to the person who asked as the default for the whole workspace.

Each channel has its own configuration. You choose which Databricks workspace the channel connects to, and whether questions go to Genie One or to a specificGenie Agent. By default, channels use Genie One, which routes questions across Genie Search, Genie Agents, and more, for a comprehensive view of results across your data estate. For domain-specific channels such as "Product FAQs" or "Employee Benefits,” you can pin a curated Genie Agent to a channel, so answers stay scoped to that agent's data and instructions.

## Work with Genie in a direct message

Users can work privately with Genie right from a DM. You can ask questions about your data, search the enterprise knowledge sources you've connected, see results as tables and charts, upload files for Genie to analyze and take action in other tools from the same chat. DM answers use your permissions and stay private to you, just as a chat would in Genie One or Genie Agents.

![image3.gif](/images/posts/14704f16af3f.gif)

## From answer to action, without leaving Slack

Of course, a trusted answer is useful only if someone acts on it. With Genie embedded directly in Slack, users can turn insights into work right from their Slack workspace:

- Take action across your tools: ThroughMCP connectors, Genie can create or update documents, comment on tickets and update records with your own credentials. It prepares each change for your approval before it runs.
- Schedule recurring analyses:Click “Run this analysis on a schedule” under an answer, or ask in your own words, for example "Send me this analysis every Monday at 9 AM." Results arrive in your DM.
- Work with files:Attach a file for Genie to analyze, and get documents such as PDFs back in the thread.
- Share charts in a thread:Genie returns visualizations directly in Slack, so the chart is ready when your team needs it.

These same capabilities empower AI cowork directly in Genie One, so you can orchestrate and review your workflows from whichever system you prefer.

## Governed and secure

Genie in Slack follows the same governance as every other Genie surface. Every question runs using the identity of the person who asked it, across Unity Catalog and each connected source, so Genie uses only information that person is allowed to see. In channels, answers use the permissions of whoever asked, and each channel can choose whether responses are shared with the channel or sent privately to the asker. Workspace admins can set this default for the whole workspace.

Admins can govern AI usage centrally inUnity Gateway, including MCP policies, cost controls, and monitoring. MCP policies decide which MCP servers and tools Genie can use, which users can access them and which actions require human approval, and traces record what Genie did and who asked for it. Workspaces that use Private Link are supported throughcontext-based ingress policies.

## Genie and Slack: better together

Questions about your company's data and knowledge don't come up in isolation, so they shouldn't be answered in isolation either. The Databricks Genie app for Slack brings governed answers and actions into the conversation where your team already makes decisions, with no new tool to learn and no new permissions model to manage.

Get started today:

1. Admins:Install theDatabricks Genie appfrom the Slack Marketplace and configure channels and response visibility. Review ourdocumentationfor more information.
2. Users:DM Genie or @mention it in a channel. The first time, sign in to Databricks and pick a workspace.

To learn more about the Databricks Genie App for Slack, join our webinar: "Just Ask Your Data: Bring Databricks Genie into Slack"

### How do I get started?

1. Admins:Install the Databricks Genie app in your Slack workspace.
2. Users:DM Genie or @mention it in a channel. The first time, sign in to Databricks and pick a workspace.

### Does the Databricks Slack app support Genie One and Genie Agents?

Yes. Genie One is the default. It looks across your entire data estate to answer each question. You can also pin a conversation or channel to a specific Genie Agent. Questions are then sent to that agent through the Genie Agentic API, so answers stay scoped to that agent's curated data and instructions.

### What can the Databricks Slack app do?

Genie in Slack does much more than answer questions. You can:

[翻译失败，原文如下]

- Discover and visualize insights:Get answers, tables, and charts from your Databricks data in a DM or channel thread.
- Search your company's knowledge:Pull in context from connected sources such as Google Drive, Confluence, or Jira.
- Take action in other tools:Create or update a document, comment on a ticket, or update a record through MCP connectors. Genie asks for your approval before it makes a change.
- Schedule recurring analyses:Run an analysis on a schedule and get the results in your DM.
- Work with files:Upload a file for Genie to analyze, and get documents such as PDFs back in the thread.
- Pick the right expert:Use Genie One across your whole data estate, or pin a conversation or channel to a specific Genie Agent.
- Get notifications:Receive Databricks platform notifications in Slack (documentation).
- Give feedback:Rate answers with a thumbs up or down to help improve Genie.

### How do I get recurring insights from Databricks Genie sent to my Slack DMs?

You have two options:

- In Slack:In a DM with Genie, clickRun this analysis on a scheduleunder an answer, or ask in your own words, for example, "Send me this analysis every Monday at 9 AM."
- In Databricks:Create a scheduled task in Genie One and choose Slack as where results are delivered.

Either way, results arrive in your Genie DM. You need to sign in to the Genie app from a DM once before results can be delivered.

### Does it support workspaces that use Private Link?

Yes. A Databricks account admin needs to create a context-based ingress policy to allow secure connectivity between Slack and your Databricks workspace. See thedocumentationfor setup steps.

### Is my data secure?

Yes. Every question runs as the user who asked it, so Genie only uses data that person is allowed to see, based on Unity Catalog and source permissions. Questions are processed inside your Databricks workspace. The service that routes messages between Slack and Databricks doesn't store questions or answers.

---

> 本文由AI自动翻译，原文链接：[Genie in Slack is now Generally Available: Governed AI cowork, right where work happens](https://www.databricks.com/blog/genie-slack-now-generally-available-governed-ai-cowork-right-where-work-happens)
> 
> 翻译时间：2026-11-16 08:50
