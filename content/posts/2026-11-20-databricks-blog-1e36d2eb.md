---
title: Interactive Databricks Reference Architectures Across 70 Industries
title_original: Interactive Databricks Reference Architectures Across 70 Industries
date: '2026-11-20'
source: Databricks Blog
source_url: https://www.databricks.com/blog/interactive-databricks-reference-architectures-across-70-industries
author: ''
summary: '[翻译失败，原文如下]


  - Start from your industry.Pick one of 70 industries and a cloud and the board shows
  the source systems, teams, use cases, and Databricks...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-21T09:25:35.725632'
---

[翻译失败，原文如下]

- Start from your industry.Pick one of 70 industries and a cloud and the board shows the source systems, teams, use cases, and Databricks products that go with it.
- See what runs in your region.Pick a region and get the list of products and features available there, with each one's release stage and a link to the docs that say so.
- Take it into your next meeting.Export the board as a PowerPoint or PDF deck, an image, or an editable draw.io, Visio, or Excalidraw file, in any of 16 languages.

## Why we built it

Most Databricks architecture talks used to start with the same slide: ingestion on the left, the lakehouse in the middle, BI and AI on the right. The slide is correct, but it doesn't specify where a bank's core banking ledger and SWIFT payment messages go. A hospital wants to know what happens to the HL7 messages from its electronic health record (EHR) system and to its DICOM medical images. A utility asks about smart meter reads and the SCADA data coming off the grid.

So people redrew the slide for each industry, and the copies drifted apart. They went out of date with every product release, lived on individual laptops, and there was no way to tell which one was current.

The Databricks Reference Architecture simplifies this journey. It's a public, interactive board with a version for each of the 70 industries, updated from the Databricks docs, so it doesn't go stale. Every box opens a panel with what it is, who uses it, and where to learn more. You can also copy any board and change it to fit your own systems.

![Opening the electronic health record (EHR) source on the healthcare board](/images/posts/cccf87f37b58.gif)

## Seventy industries in eleven sectors

The architecture board covers 70 industries across 11 economic sectors as of November 16th 2026. Click a name to open its board.

You'll find the same list in the industry picker at the top of the board. You can search for any industry of interest and interact with it. There is also the Standard Reference Architecture, which is the architecture board with no industry bias.

![Searching the industry picker for pharmaceuticals](/images/posts/525f6f2ddd48.gif)

## What changes when you pick an industry

The Databricks Platform in the middle is the same across industries. What changes are the things surrounding it.

The sources are the systems that industry actually runs: 964 different ones across the 70 boards as of the release of this blog. They're grouped the way people in that sector talk about them. Like EHR, imaging, and revenue cycle in healthcare, or metering, SCADA, and outage management at a utility. Most source boxes also specify what data they send: whether it's batch or streaming, its shape, how much, and how often. By default, a source shows its type, such as Electronic Health Record (EHR). Switch to Branded to see the vendor products instead.

The boards also list the data formats each industry exchanges, 186 in all. They run from FIX and ISO 20022 in finance toHL7,FHIRandDICOMin healthcare and OPC UA in manufacturing, and each one links to the body that publishes it.

The teams carry the names each sector uses, like Treasury and ALM at a bank or Grid Operations at a utility, with 1,538 personas across the 70 boards.

The medallion layers use the industry's own terms too. On the banking board, Gold holds net interest margin and liquidity ratios. On the healthcare board, it holds length of stay and patient outcomes. And every board has 10 use cases, 4 Genie Agents, 4 AI/BI Dashboards, and 4 Databricks Apps written for that industry.

Here's how six of them compare, from the sources to the Silver layer:

## Two views of every board: Simplified and Detailed

Every board opens in Simplified. It shows what you need to read the industry: the first entries in each group, key systems like a bank's core banking system, the use cases with Databricks customer stories, and the core cloud services.

Detailed view adds everything else such as CI/CD, monitoring, and operational stores, along with captions, capability tags, and descriptions. Switch views in the toolbar. Shared links and exports follow the view on screen.

## Use cases and Genie Agents you can open

All 700 use cases say what problem they solve, which team benefits, and how they're built on Databricks, with a link to every product they use. 581 of them link to at least one Databricks customer story and those are listed first. When there's a Databricks Solution Accelerator for a use case the panel links to it so that you can start from working code.

![Predictive Maintenance & Asset Health on the oil and gas upstream board, with its Solution Accelerator and customer stories](/images/posts/bc978280c0bb.gif)

Genie Agents work the same way. On the pharmaceuticals board, the Trial Enrollment Agent reads the electronic data capture and clinical trial management systems for the clinical operations team, biopharma leaders, and clinical trial managers. Its panel lists the questions those teams would ask it, such as which sites are under-enrolling this month.

![The Trial Enrollment Agent on the pharmaceuticals board](/images/posts/91fc56f90b93.gif)

## Teams and what they need to learn

Click a team to see the people in it, the use cases they own, and the Databricks products they use, with a line on what each product is for. The panel also builds a learning path for that team from free Databricks Academy courses and certifications, adds the customer stories, demos, and videos that matter to them.

![The Clinical Operations team on the healthcare board, with its learning path](/images/posts/f1df274c3e5c.gif)

## From the board to the data model

The medallion layers link to a deployable data model. Open Silver on the banking board and the panel links to the banking model in the Databricks Industry Data Models, with its tables and columns. We introduced those models inJumpstart your Data Modeling with Databricks Industry Data Models, and the agent that builds them inReimagining Data Modeling on the Lakehouse: Introducing Vibe Data Modeling.

![The Silver layer on the banking board, linked to the industry data model](/images/posts/c4ce33899795.gif)

Source boxes go one level down, into the data itself. The process historian on the manufacturing board collects sensor tags from the production lines. Its panel says who uses that data and how much of it arrives, a continuous stream of 10,000 to 100,000 tags a second.

![A process historian on the manufacturing board, with the data it sends](/images/posts/fa301a9265b1.gif)

## Check what runs in your region and what's still in preview

This is the part we use most. Before anyone designs anything, two questions come up: does the product run in the region where we deploy and is it GA or still in preview?

Pick a region from the Region menu. The board dims every product that region can't run and a panel opens with the full list for that region. It lists every product and feature that the Databricks docs publish, along with their release stage and whether they're available there. When the docs add a note, such as a feature that processes data outside your geography, the panel shows it too. Each row links to the docs page it came from.

The list filters like a spreadsheet. Untick GA in the Stage column and you're left with what's in Public Preview or Beta. You can also sort it, search it, and download it to Excel. The address bar keeps your filters, so you can send someone exactly the view you're looking at.

![Picking Johannesburg on Azure, then showing only what isn't GA yet](/images/posts/a4fd6f548031.gif)

If you only want to clean up the board itself, the Stage menu filters the platform by release stage. Turn off Beta and the previews and everything that isn't GA drops out of the picture. That's handy when you need a GA-only architecture for a review.

[翻译失败，原文如下]

Both the stages and the regions come from the public Databricks documentation. We refresh them before every change to the board and the board shows the date of the last refresh.

## Any cloud, in 16 languages

Every board works on Azure, AWS, and GCP. Switch the cloud, ingestion tools change with it, and the docs links point to that cloud's documentation.

The boards are translated into 16 languages, laid out right-to-left for Arabic and Hebrew and the exports are in the language you're reading.

![Switching the banking board to Arabic](/images/posts/1009a1215e5a.gif)

Every industry also has its own share link and preview card. Post the link in Slack, Teams, or LinkedIn and it opens on that industry, with its name on the card.

## Taking an industry board into a meeting

Any board exports as a PowerPoint or PDF deck with a contents page, the board, and a page for each use case, Genie Agent, dashboard, and app. In the PowerPoint, the board slide is built from real shapes so that you can move and relabel the boxes. The board also downloads as a PNG, an animated GIF, interactive HTML, an editable draw.io file, a Visio file, a SVG file, an Excalidraw file, or a YAML file you can edit and import back.

![Exporting the banking board to PowerPoint and pages from the deck](/images/posts/ba489c6a9633.gif)

If you'd rather start from a description the AI Architecture Assistant finds the closest industry for you. Describe the business or attach a whiteboard photo or a PDF and it builds an editable architecture from that industry's board. It runs as a Databricks App in your own workspace and the repository also includes an MCP server that gives AI agents all 70 architectures.

![The AI Architecture Assistant](/images/posts/51917a1ffed8.gif)

## Things to consider

Treat an industry board as a starting point. Every company has its own systems, constraints, and history. A sub-vertical can look quite different from its parent industry. Vendor products change too. If you spot something out of date, tell us through the Feedback button.

## Try it today

Open theDatabricks Reference Architecture, pick your industry and cloud and click any box. The code and an installer for your own workspace are onGitHub. If your industry is missing or a board makes a mistake, use the Feedback button at the top of the board.

## Coming next

We're building pipelines that update the board as products ship, instead of waiting for the next change to the repository.

Explore the interactive reference architecture

What is a Databricks reference architecture?A free, interactive board that shows how Databricks fits a specific industry: the source systems, data formats, teams, use cases and products involved. There's a version for each of 70 industries, and you can export or edit any of them.

Is it free?Yes. The board is public and free to use, and the code and an installer for your own workspace are on GitHub.

Which clouds and regions does it cover?Every board works onAWS,GCPandAzureCloud. Pick a region to see which products and features are available there, and their release stage, straight from the Databricks docs.

Can I tailor a board to my own environment?Yes. UseDownloadto copy an industry board then customize using the tool of your choice. You can also edit and re-import a YAML file.

How can I tell which products are available in my region or release stage?Choose a region to see products that are unavailable there, and use the release-stage filter to check availability stages such as GA, public preview, and beta. Product panels link to the relevant documentation.

How current is the product and regional availability information?Availability information is checked against public Databricks documentation before board updates. Automated update pipelines are planned, so updates are not yet described as live.

Can I use the reference architecture on a different cloud or in another language?Yes. The boards support Azure, AWS, and GCP, and are available in 16 languages, including right-to-left layouts for Arabic and Hebrew.

Can I run the reference architecture in my own workspace?Yes. The source code and an installer are available on GitHub for setting it up in your workspace.

How do I report an error or request an industry that is not listed?Use the Feedback button at the top of the board to report an issue or request an additional industry.

---

> 本文由AI自动翻译，原文链接：[Interactive Databricks Reference Architectures Across 70 Industries](https://www.databricks.com/blog/interactive-databricks-reference-architectures-across-70-industries)
> 
> 翻译时间：2026-11-21 09:25
