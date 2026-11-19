---
title: 'What''s new for Genie in Microsoft: Copilot Cowork and Chat, Microsoft Teams,
  and Excel.'
title_original: 'What''s new for Genie in Microsoft: Copilot Cowork and Chat, Microsoft
  Teams, and Excel.'
date: '2026-11-18'
source: Databricks Blog
source_url: https://www.databricks.com/blog/whats-new-genie-microsoft-copilot-cowork-and-chat-microsoft-teams-and-excel
author: ''
summary: '[翻译失败，原文如下]


  - Genie works in the Microsoft tools you already use: Genie is available in Copilot
  Cowork, Microsoft Teams, Excel, and Copilot Studio.

  -...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-19T09:43:51.694141'
---

[翻译失败，原文如下]

- Genie works in the Microsoft tools you already use: Genie is available in Copilot Cowork, Microsoft Teams, Excel, and Copilot Studio.
- Genie in Microsoft Teams is generally available: DM the Databricks Genie app or @mention it in a channel or group chat to get governed insights without leaving Teams. The same app also works in Microsoft 365 Copilot.
- Governed answers in Microsoft Cowork, in a few clicks: The Azure Databricks Genie plugin connects Genie One to Microsoft Copilot Cowork and chat, so users get governed insights from across their data estate.

Most AI assistants can read a person's email, files, and calendar, but it can't tell which revenue table is certified or how finance defines net retention. This leads to inconsistent outcomes, low adoption, and a lack of trust among business users.Genie Ontologysolves this context problem forGenieby combining the business semantics teams explicitly define with context learned from everyday work, so answers are grounded in a full understanding of the business.

Once that context is unified, the next step is putting it to work. As AI assistants and agents spread across the business, organizations need to control data access, spend, and tool usage at scale. Without that control, sensitive data can reach the wrong people, AI spend becomes hard to predict, and agents can connect to tools no one has approved. In Genie, Unity Catalog enforces each user's data permissions, andUnity Gatewaygives admins the traces, MCP policies, and budget controls they need to manage AI across the organization.

Genie brings both essential context and governance into the Microsoft tools your teams already use with the Azure Databricks Genie plugin, which connects Microsoft Copilot and Copilot Cowork to Genie One. Genie also works in Microsoft Teams, Microsoft Excel, and Microsoft Copilot Studio.

## Genie in Microsoft Teams: governed answers in every channel and DM

TheDatabricks Genie app for Microsoft Teamsis now generally available, bringing Genie into the conversations where teams already make decisions. Users can send Genie a direct message or mention @Databricks Genie in a channel or group chat, and Genie replies in the thread with answers grounded in the organization’s governed business context.

With Genie in Teams, users unlock real-time collaboration with knowledge from across their data estate. For example, a sales manager can post in a channel, "Which open leads over $100K haven't had a follow-up this week?" Instead of someone manually pulling the pipeline report, cross-checking it against the CRM, searching meeting notes, and messaging reps one by one, she can now simply tag @Genie. Genie answers in the thread with the matching leads, their latest activity, and links to the sources it used, not only saving the team time and effort, but also allowing the work to happen right where the question was originally asked.

Genie in Teams goes beyond answers, enabling users to turn insights into work right from their Teams workspace:

- Schedule recurring analyses:Click “Run this analysis on a schedule” under an answer, or ask in your own words, for example "send me this analysis every Monday at 9 AM." Results arrive in your DM.
- Work with files:Attach a file for Genie to analyze, and get documents such as PDFs back in the thread.
- Share charts in a thread:Genie returns visualizations directly in Teams, so the chart is ready when your team needs it.

## The Azure Databricks Genie plugin: Governed answers in Copilot Cowork and Chat

TheAzure Databricks Genie plugin for Microsoft Copilot Coworkand Copilot Chat brings trusted business answers into the Copilot experience users may already rely on. Instead of Copilot searching for correct answers on its own, it can delegate work to Genie One. Genie leverages Genie Ontology to provide accurate insights based on certified definitions, metric views, and context learned from everyday work, all governed by Unity Catalog.

Together, Genie and Copilot can unlock new workflows for teams. For example, imagine an account team preparing for client meetings. An account director asks Copilot Cowork for a briefing ahead of a customer meeting, which delegates to Genie. Genie pulls usage, spend, and account trends from Azure Databricks using certified metric definitions, then reads recent customer email threads in Outlook through its Microsoft 365 connector to flag open escalations. Cowork turns those insights into a Word doc brief, an Excel overview with charts, and a client-ready presentation. Every figure comes from Genie, keeping the deliverables consistent with the numbers finance and the account team already report.

## Genie in Microsoft Excel: governed answers inside the workbook

Many teams plan, forecast, and report in Excel, but getting trusted data into a workbook often means exporting files, copying numbers, and hoping they match the source. WithGenie One in the Azure Databricks Excel Add-in, analysts can ask questions in plain English and get answers from governed Azure Databricks data without hunting for tables or writing SQL. Every answer includes citations that show where the numbers came from, and analysts can refine their analysis with follow-up questions, resume past conversations, and load table results directly into the workbook for further modeling.

The Excel Add-in also lets teams:

- Build live pivotson Unity Catalog metric views and tables. Results populate as fields are dragged in, with no refresh button.
- Schedule refreshesso recurring reports, forecasts, and scorecards stay current with the latest data.
- Write backfinalized inputs, such as forecast assumptions or planning updates, to Databricks tables.

Together, these capabilities bring governed Azure Databricks data into the spreadsheet workflows teams already rely on, without exports or manual data movement.

## Microsoft Copilot Studio: build custom agents connected to Genie Agents

Builders can connect Genie Agents to Microsoft Copilot Studio using theAzure Databricks connector for Power Platform. Adding Genie as a tool lets a Copilot Studio assistant delegate questions about Azure Databricks data toGenie Agents, which answer using curated data and instructions and governance enforced by Unity Catalog.

## Better together: Microsoft + Genie

Business questions rarely stay in one tool, so the answers shouldn't either. Together, Microsoft and Genie bring governed business context from Azure Databricks into the tools every employee already uses: Copilot Chat, Copilot Cowork, Teams, and Excel. Genie Ontology makes sure every answer is grounded in your enterprise context, and Unity Catalog and Unity Gateway enforce governance for every answer and action. Now, wherever a question starts, whether in a Teams thread, a Copilot chat, or an Excel workbook, users get the same trusted, governed answer.

What is Genie Ontology?Genie Ontology is the enterprise context layer that gives Genie and other AI agents a shared understanding of your business. Agents build it from everyday work, people govern it, and every agent can use it. It combines business semantics that teams define, such as metric views and certified definitions, with context learned from dashboards, queries, and documents. Genie Ontology is now generally available.

How does Genie Ontology help Microsoft Copilot give better answers?It gives Copilot the business meaning behind the data. When Copilot or Copilot Cowork asks Genie a question, Genie answers with the certified definition, such as how finance defines net retention, instead of guessing from table names. Teams get consistent answers in every Microsoft tool.

How do admins govern Genie across Microsoft tools?Through Unity Gateway. Admins manage AI usage centrally with MCP policies, cost controls, and monitoring. MCP policies decide which MCP servers and tools Genie can use, who can access them, and which actions need human approval. Traces record what Genie did and who asked for it.

[翻译失败，原文如下]

How do I get started with Genie in Microsoft Teams?

Admins add the Databricks Genie app to Microsoft Teams and choose the default visibility for responses. Users then send Genie a direct message or mention @Databricks Genie in a channel or group chat. The first time, they sign in to Databricks and pick a workspace.

Does Genie in Teams support Genie One and Genie Agents?Yes. Genie One is the default. It looks across your entire data estate to answer each question. You can also pin a conversation or channel to a specific Genie Agent. Questions are then sent to that agent through the Genie Agentic API, so answers stay scoped to that agent's curated data and instructions.

What can Genie do in Microsoft Teams?Genie in Teams does much more than answer questions. You can:

- Discover and visualize insights:Get answers, tables, and charts from your Databricks data in a direct message or channel.
- Search your company's knowledge:Pull in context from connected sources.
- Take action in other tools:Create or update a document, comment on a ticket, or update a record through MCP connectors. Genie asks for your approval before it makes a change.
- Schedule recurring analyses:Run an analysis on a schedule and get the results in your DM. To set up, ask Genie to "Send me this analysis every Monday at 9 AM."
- Work with files:Attach PDF, Word, or CSV files for Genie to analyze, and get documents such as PDFs back.
- Pick the right expert:Use Genie One across your whole data estate, or pin a conversation or channel to a specific Genie Agent.
- Give feedback:Rate answers with a thumbs up or down to help improve Genie.

Does Genie in Microsoft Teams support workspaces that use Private Link?Yes. A Databricks account admin needs to create a context-based ingress policy to allow secure connectivity between Teams and your Databricks workspace.

Is my data secure for Genie in Microsoft Teams?Yes. Every question runs as the user who asked it, so Genie only uses data that person is allowed to see, based on Unity Catalog and source permissions. Questions are processed inside your Databricks workspace. The service that routes messages between Teams and Databricks doesn't store questions or answers.

Should I use the Databricks Genie app in Teams, or publish a Copilot Studio agent to Teams?Use the Databricks Genie app in Microsoft Teams by default. It's a native app that chats directly with Genie One, so users get answers from across their data estate with no extra agent in between. It also works in Microsoft 365 Copilot. The app supports pinned Genie Agents, charts, file uploads, and MCP actions, and it doesn't require a Copilot Studio license. Choose Copilot Studio when you're building a custom agent that combines Genie Agents with other tools not available within Azure Databricks.

How do users get started with the Azure Databricks Genie plugin?Users can get started in a few clicks. In Copilot Cowork, they turn on the Azure Databricks Genie plugin, click Connect, and sign in with their Azure Databricks credentials. The plugin doesn't require an OAuth app registration or manifest edits.

Which Microsoft tools work with Genie?Genie works across Copilot Chat, Copilot Cowork, and Microsoft 365 apps. It's also available in Microsoft Teams, Microsoft Excel, Microsoft Copilot Studio, Microsoft Power Platform, and Microsoft Agent 365. Genie One in Microsoft Foundry brings the same governed context to agents built in Foundry.

How does Genie work with Microsoft Foundry?Genie works with Microsoft Foundry in both directions. Agents built in Foundry can use Genie One to get governed Azure Databricks data while acting as the signed-in user. Microsoft Foundry models are also available in Azure Databricks through Unity Gateway.

Can Genie connect to Work IQ over MCP?Genie will soon connect to Work IQ over MCP, through Model Context Protocol, so organizations that use Work IQ can bring Microsoft 365 context into Genie alongside governed Azure Databricks data. That context includes email, meetings, documents, Teams messages, and people and organizational context. Each request runs under the signed-in user's Microsoft Entra ID identity, so Microsoft 365 permissions, sensitivity labels, and compliance policies continue to apply while Unity Catalog governs the Azure Databricks data.

Partners

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[What's new for Genie in Microsoft: Copilot Cowork and Chat, Microsoft Teams, and Excel.](https://www.databricks.com/blog/whats-new-genie-microsoft-copilot-cowork-and-chat-microsoft-teams-and-excel)
> 
> 翻译时间：2026-11-19 09:43
