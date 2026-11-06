---
title: 'Which Data Collaboration Tool: OpenSharing, Clean Rooms, Marketplace'
title_original: 'Which Data Collaboration Tool: OpenSharing, Clean Rooms, Marketplace'
date: '2026-11-05'
source: Databricks Blog
source_url: https://www.databricks.com/blog/which-data-collaboration-tool-opensharing-clean-rooms-marketplace
author: ''
summary: '[翻译失败，原文如下]


  - Databricks has three primary ways to share data and AI assets: OpenSharing, Clean
  Rooms, and Marketplace. Each one fits a different kin...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-06T09:06:23.789825'
---

[翻译失败，原文如下]

- Databricks has three primary ways to share data and AI assets: OpenSharing, Clean Rooms, and Marketplace. Each one fits a different kind of relationship with the party on the other side.
- Picking the wrong tool can waste an engineering sprint or expose data you meant to protect. These tools also remove the old work of copying data and building pipelines for every consumer.
- Let the relationship decide how you share data: use OpenSharing for live, read-only access with a known recipient. Use Clean Rooms when partners want to combine data without exposing all of it. Use Marketplace to reach, or find, audiences you don't know yet.

The world of sharing has extended far past tables. We can now securely share all kinds of data and AI assets, from models to notebooks to AI agents, and the appetite to do so only keeps growing. While in the past, it may have been difficult to get just a table to or from a partnering business, these days it's easier than ever to provide access.

With this growing demand, we have seen three methods of sharing pop up in Databricks: OpenSharing, Clean Rooms, and Marketplace. With the emergence of these three, the question arises: “When do I use one over the other?” Picking the wrong one can cost you a wasted engineering sprint, or worse, expose data you meant to keep protected. In this blog, we'll dive into the three different sharing options and how they can apply to your business and your partnerships. As we'll see, the right choice usually comes down to one thing: the relationship you have with whoever is on the other side of the data.

## OpenSharing

First, we have OpenSharing, the simplest way to share data assets. Essentially, you create a share, associate assets with it, and provide access to that share to recipients. OpenSharing will handle the access, even if that recipient isn't on Databricks. This changes the paradigm as you no longer need to stand up pipelines to ship data to each consumer. Instead, consumers get direct read-only access to the original live asset once you've granted it, so what they see is always up to date.

Even popular BI tools like Power BI and Tableau can read directly from OpenShared tables. So a partner can directly connect their BI to the data you share with them.

You may have noticed I used the word “data assets." That is because you can share more than just tables with businesses outside your organization, including tables (Delta or Iceberg), Views, Volumes, Notebooks, UDFs, and even AI Models. This is also not limited to outside organizations; several businesses use OpenSharing to share data with different business units.

Across industries, we have seen businesses utilize or ingest data from partnered businesses via OpenSharing:

- Retail: Businesses sharing point-of-sale data with their CPG suppliers
- Healthcare: Hospital networks handing de-identified data to a named research partner
- Manufacturing: sharing demand forecasts and inventory positions with their key suppliers

You might be thinking you could do this yourself by standing up a pipeline to share data out and managing credentials. And you would be correct, but the point of OpenSharing is to remove that overhead. You do not need to make copies of your data and spend unnecessary money. You share in minutes, and revoke just as fast.

![image3.png](/images/posts/ee5428c7a24d.png)

## Databricks Clean Rooms

Next, we have the Databricks Clean Rooms, which is much like it sounds: a sealed, neutral space where two or more businesses (up to ten) can bring their data together and run only the code every party has approved. Everyone benefits from the results, but no one ever sees another party's full underlying data. Let's say my company has proprietary data, and a business we partner with frequently has data they want to marry with ours to maximize value. Neither of us wants to share a full dataset, but we believe there is value in sharing snippets of data or joining our data on select fields. Instead of sending the full dataset over, we both share our table’s names and columns with each other and collaborate on authoring a notebook. For anything to run, we both have to give a thumbs-up of approval.

That, in essence, is how Clean Rooms operate. They let us collaborate with another business and intermingle data that is proprietary to each of us, while limiting what we share to only what we agreed to in that handshake. This is extremely common across a few industries:

- Advertising and media: measuring campaign reach and audience overlap without exchanging entire customer lists
- Healthcare: combining patient or clinical-trial data across organizations under strict privacy controls
- Retail and CPG: matching loyalty and sell-through data to plan joint promotions

Reach for a clean room when combining data is valuable, but neither side wants to expose its full underlying data. The key difference is that, rather than giving the recipient direct access to the object itself, you only see the results of code that both sides have approved.

![image4.png](/images/posts/c56445f7002c.png)

## Databricks Marketplace

Last, we have the Databricks Marketplace. Think of it as a public storefront where you can share Files, Tables, Models, MCP (Model Context Protocol) Servers, Notebooks, Apps, and SaaS software. OpenSharing and Clean Rooms are options when you have an existing relationship with your customer. The Databricks Marketplace is about the ones you do not. It is an open exchange where data providers, software vendors, and technology partners publish offerings that any Databricks customer can discover, evaluate, and connect to directly from their workspace.

If you are a provider, it is a storefront that puts your assets in front of a broad audience. On the other side, if you are a consumer, you can find data and AI products to plug into your own work. Either way, what sets Marketplace apart is that it is public and discoverable: with OpenSharing and Clean Rooms, you already know who is on the other side, but on Marketplace, anyone can find your listing without you ever having met them.

Common examples of Marketplace:

- A financial-data vendor monetizing market datasets
- A weather forecasting service listing global weather datasets
- A consultancy packaging an industry-specific ML model or Genie agent
- A software vendor publishing a ready-to-run analytics app that customers launch in their own workspace
- A SaaS vendor publishing an MCP Server that plugs into your own AI agents

Reach for Marketplace when you do not have a specific recipient in mind: you either want to be found, or you want to go find data and AI products yourself.

![image2.png](/images/posts/64b35bd9ca3b.png)

## Here's the quick side-by-side:

![image1.png](/images/posts/d56846348c62.png)

## Conclusion

If you are still on the fence about which approach to use, let the relationship decide. If you already know exactly who should receive the data and you're comfortable sharing a read-only version, reach for OpenSharing. If you have a specific partner but neither side wants to expose its full underlying data, use a Clean Room. And if you don't have a specific recipient yet but want to be discovered, or you want to discover data and AI products yourself, that's Marketplace. Lastly, these are not mutually exclusive; the same business can use different tools for different relationships.

At the end of the day, these are all tools meant to enable your business and prevent slowdown from the traditional burdens of data sharing. So if you ever have customers asking for data, think about the relationship and match it to the right tool!

Best Practices

---

> 本文由AI自动翻译，原文链接：[Which Data Collaboration Tool: OpenSharing, Clean Rooms, Marketplace](https://www.databricks.com/blog/which-data-collaboration-tool-opensharing-clean-rooms-marketplace)
> 
> 翻译时间：2026-11-06 09:06
