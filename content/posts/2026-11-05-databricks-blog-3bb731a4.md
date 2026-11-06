---
title: 'From Delta Sharing to OpenSharing: what changed, what''s next'
title_original: 'From Delta Sharing to OpenSharing: what changed, what''s next'
date: '2026-11-05'
source: Databricks Blog
source_url: https://www.databricks.com/blog/delta-sharing-opensharing-what-changed-whats-next
author: ''
summary: '[翻译失败，原文如下]


  - OpenSharing is the evolution of Delta Sharing into an open, Linux Foundation-governed
  protocol for sharing data and AI assets, includin...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-06T09:06:23.522001'
---

[翻译失败，原文如下]

- OpenSharing is the evolution of Delta Sharing into an open, Linux Foundation-governed protocol for sharing data and AI assets, including agent skills and models, not just tables.
- As teams build agents, they need to share AI assets across platforms, Iceberg engines, and on-premises storage without copying data or building custom pipelines for every partner.
- OpenSharing is additive. Existing Delta Sharing setups keep working, and you enable the new asset types on a Unity Catalog metastore using the same share, recipient, and grant workflow.

Delta Sharing has been the way thousands of organizations exchange live data across clouds and platforms without copying it. In June 2026, Databricks and the Linux Foundation announced that Delta Sharing has evolved intoOpenSharing, an open, vendor-neutral protocol for sharing not just tables, but the broader set of assets that AI teams now depend on: agent skills, AI models, and unstructured data. If you already share data with Delta Sharing, or you're evaluating how to collaborate with partners on both data and AI assets, this post walks through what OpenSharing actually is, what's changed under the hood, and where the project is headed.

### A quick recap: what Delta Sharing solved

When Databricks introduced Delta Sharing at Data + AI Summit 2021, the core problem it addressed was simple to state and hard to solve well: organizations wanted to share live data with partners, customers, and other teams, without exporting files, standing up brittle ETL jobs, or forcing every recipient onto the same platform. Delta Sharing was contributed to the Linux Foundation as an open protocol, built on Delta Lake and Parquet, so a provider could grant access to a table and a recipient could query it directly, in real time, from tools like Apache Spark, Power BI, Tableau, pandas, and many others.

That open, zero-copy model resonated. Delta Sharing grew into the most widely adopted open protocol for secure data sharing, used by organizations including Amadeus, Atlassian, LSEG, SAP, Stripe, and The Trade Desk for cross-cloud and cross-platform collaboration, according to Databricks (Databricks press release). By the time Databricks announced OpenSharing in June 2026, Delta Sharing had reached more than 28,000 data recipients, with roughly a third of shares flowing across platforms through open connectors rather than staying inside Databricks-to-Databricks sharing (Databricks blog).

### Why Delta Sharing needed to evolve

Sharing had already grown well beyond tables. Through Databricks-to-Databricks sharing, teams were exchanging views, volumes of unstructured files, notebooks, and registered ML models years before agents entered the picture, so structured data was never the whole story. What agents changed was the kind of asset that needed to move, and how far it needed to travel. Agent skills, the agents themselves, and the semantic context they run on all called for the same governed, zero-copy access that sharing had already proven out. Enterprises also wanted that access to reach across platforms and beyond Databricks-to-Databricks connections, and the open protocol still centered on tables, so these newer assets sat outside what open, cross-platform sharing could actually deliver.

At the same time, enterprises kept asking for two related things: broader interoperability with formats like Apache Iceberg, and a way to bring data that lives on premises or in private clouds into the same governed sharing model, without migrating it first. Addressing both of these gaps meant rethinking Delta Sharing's scope, not just adding features to it.

### What OpenSharing actually is

On June 10, 2026, Databricks and the Linux Foundation jointly announced OpenSharing as the next evolution of Delta Sharing (Databricks press release,Linux Foundation press release). Precision matters here, because OpenSharing operates at two distinct layers:

1. An open source protocol and specification, contributed by Databricks and now developed as a project under the Linux Foundation AI & Data Foundation. The spec is Apache 2.0 licensed and lives on GitHub, where any vendor or community member can implement it independent of Databricks entirely (GitHub, OpenSharing).
2. Databricks OpenSharing, the enterprise implementation of that protocol inside the Databricks platform, integrated with Unity Catalog, Databricks Marketplace, and Clean Rooms.

The open ecosystem reaches beyond the protocol itself. Open source Unity Catalog, an Apache 2.0 project also governed under the Linux Foundation, provides a vendor-neutral catalog and governance layer for these assets, so a team can pair it with an open sharing server and run governed sharing entirely outside Databricks (GitHub, Unity Catalog).

Databricks Co-founder and CTO Matei Zaharia framed the move this way: "Delta Sharing proved the industry would choose open over locked-in. OpenSharing extends that principle to the full AI stack, while expanding the cross-platform ecosystem to Iceberg recipients and on-premises providers" (Databricks press release). Linux Foundation CEO Jim Zemlin added that the goal is "a common, vendor-neutral framework that enables organizations to exchange AI assets securely and interoperably across platforms and ecosystems" (Linux Foundation press release).

One clarification worth making up front: existing Delta Sharing clients and integrations remain compatible with OpenSharing. This is an evolution of the protocol, not a break from it, and thedelta-io/delta-sharingrepository continues to exist alongside the newOpenSharing-IO/OpenSharingGitHub organization.

![image2.jpg](/images/posts/7a525db2a976.jpg)

Diagram: Delta Sharing evolves into OpenSharing, which operates as an open protocol layer on GitHub plus a Databricks enterprise implementation layer, with new reach into Iceberg REST Catalog clients and on-premises or private cloud storage.

### What changed technically

A broader asset model.The original open Delta Sharing protocol centered on tables, even as Databricks-to-Databricks sharing had grown to cover more asset types. OpenSharing brings that broader model into the open specification itself and introduces aShare → Schema → Assethierarchy that extends sharing beyond Tables to new asset types, including Volumes (directories of files in any format), Agent Skills, and AI models (GitHub, OpenSharing). This means a provider can package a data product that includes both the underlying tables and the AI assets built on top of them, and share the whole thing through one protocol.

![image1.jpg](/images/posts/4909c0482786.jpg)

Diagram: OpenSharing's asset hierarchy. Table, Volume, Agent Skill, and Model are specified asset types today. Agent and Page or Glossary types are listed as community proposals still under discussion.

Iceberg REST Catalog support.OpenSharing adds support for Apache Iceberg REST Catalog (IRC) compatible clients, so providers can share data to any Iceberg-compatible engine, not only Delta Sharing native clients. Databricks describes this as extending the reach of open sharing to organizations standardized on Iceberg tooling (Databricks product page).

On-premises and private cloud reach.Through the Databricks Storage Ecosystem, storage vendors can run an OpenSharing server that connects directly to Unity Catalog, so data that lives on premises or in a private cloud can be governed and shared without first migrating it (Databricks blog). MinIO's AIStor integration is generally available, with additional storage partners in preview or committed for later in 2026.

Zero-copy credential vending stays the model.Providers don't move data to share it. The sharing server issues temporary, scoped credentials, and the server itself sits outside the data path, consistent with how Delta Sharing worked (GitHub, OpenSharing).

New sharing capabilities.Alongside the protocol change, Databricks introduced several capabilities on top of OpenSharing:

[翻译失败，原文如下]

- SecureConnect(generally available), a Databricks-managed proxy that removes the need to configure firewall or network rules for every new recipient (Databricks blog).
- Global Distribution(Private Preview), which replicates shared data closer to recipients across regions and clouds to reduce latency and make egress costs more predictable.
- Genie Agent Sharing(Beta), which lets providers share conversational, natural-language access to their data with external partners, with controls over quotas and what underlying logic is exposed.
- Lakebase table and change data feed sharing(Public Preview), for sharing live operational data without a separate ETL step.

Governance moved to the Linux Foundation.OpenSharing has been contributed to the Linux Foundation AI & Data Foundation, where it is currently at the sandbox stage, the entry point for new projects under that foundation before they progress to incubation (GitHub, OpenSharingandopensharing.io). Changes to the spec go through a public proposal and review process rather than being decided unilaterally, which is the same governance pattern Delta Lake and Delta Sharing already followed as Linux Foundation projects.

### What this means if you are already using Delta Sharing

If you have shares, recipients, and connectors set up today, none of that goes away. OpenSharing is additive: your existing tables, connectors, and workflows continue to work, and the new asset types and capabilities are available as you choose to adopt them. Enabling OpenSharing for a Unity Catalog metastore is a configuration step, not a migration, and the same Create Share, Create Recipient, and Grant Access workflow you already know still applies to new asset types as they become available (Databricks documentation).

For teams that have been maintaining custom integrations to move agent skills or model artifacts between platforms, the practical value proposition is a single set of open APIs for discovery, authorization, and access, instead of separate, bespoke pipelines for every partner and every asset type.

### What is still on the roadmap

Some capabilities described at the June 2026 announcement are explicitly early stage rather than generally available today. Foreign Iceberg table sharing, which lets providers share tables that live in external catalogs directly, was in Public Preview at launch with general availability described as coming soon. Email-based sharing, where a provider can invite a collaborator by entering an email address rather than a longer setup flow, was also listed as coming soon at announcement time.

Beyond what Databricks has committed to shipping, the OpenSharing project's public roadmap on GitHub lists a set of community proposals that are still open design questions rather than finalized features, including support for sharing evaluation datasets and benchmarks with scoped access, synthetic dataset sharing with provenance metadata, and a proposed asset type for sharing precomputed vector indexes (OpenSharing ROADMAP.md). Because these are community proposals, timelines and final scope can change, and they are worth tracking on GitHub rather than treating as committed dates.

OpenSharing also sits at a specific layer of a broader, fast-moving set of open standards for AI. As Databricks Director of Product Management Akram Chetibi has described it, protocols for agent-to-tool and agent-to-agent communication solve a different problem than OpenSharing does: "OpenSharing provides APIs for discovering and authorizing access to stored assets, such as agent skills or AI models" (diginomica). Understanding that distinction matters if you're designing an architecture that needs both kinds of protocols working together.

### Getting started

If you're new to OpenSharing, the path in is the same one that's worked for Delta Sharing: enable OpenSharing on the Unity Catalog metastore that manages the data you want to share, create a share containing the assets you want to expose, create a recipient, and grant that recipient access (Databricks documentation). From there you can decide whether a given recipient should connect through Databricks-to-Databricks sharing, Databricks-to-Open sharing for non-Databricks recipients, or a self-hosted OpenSharing server if you want to run the protocol entirely outside Databricks. As you read the documentation, note that the protocol and brand are written as one word, OpenSharing, while the platform docs use the lowercase phrase "Databricks-to-Open sharing" for the mode that shares with recipients outside Databricks.

To go deeper:

- Read the original announcement fromDatabricksand theLinux Foundation.
- Review the technical deep dive,Introducing OpenSharing: the Next Evolution of Delta Sharing for the Agentic Era.
- Explore the protocol specification and roadmap onGitHub.
- Walk through setup steps in theDatabricks documentation on OpenSharing.
- Learn about connecting on-premises and private cloud storage through theDatabricks Storage Ecosystem announcement.

Delta Sharing changed how teams thought about moving data between platforms. OpenSharing extends that same open, zero-copy approach to the assets an agentic world runs on. If you're already sharing data with Delta Sharing today, the natural next step is to look at what else in your stack could be shared the same way, whether that's an agent skill, a model, or a set of unstructured files. Try enabling OpenSharing on a Unity Catalog metastore in your workspace, or start by reading through the protocol spec on GitHub to see how a self-hosted implementation might fit into your own platform.

Ready to try OpenSharing? Enable it on a Unity Catalog metastore in your workspace, or read the protocol spec on GitHub to see how a self-hosted implementation could fit your platform. Have questions or feedback? Reach out to your Databricks account team, open an issue on theOpenSharing GitHub repository, or join the discussion in theDatabricks Community.

Insights

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[From Delta Sharing to OpenSharing: what changed, what's next](https://www.databricks.com/blog/delta-sharing-opensharing-what-changed-whats-next)
> 
> 翻译时间：2026-11-06 09:06
