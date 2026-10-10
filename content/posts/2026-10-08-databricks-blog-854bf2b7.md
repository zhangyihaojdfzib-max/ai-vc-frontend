---
title: 'Introducing Funke: Native HL7v2 Parsing on Databricks'
title_original: 'Introducing Funke: Native HL7v2 Parsing on Databricks'
date: '2026-10-08'
source: Databricks Blog
source_url: https://www.databricks.com/blog/introducing-funke-native-hl7v2-parsing-databricks
author: ''
summary: '[翻译失败，原文如下]


  - Funke parses HL7v2 electronic health record messages directly into native Spark
  types on the Databricks Lakehouse, preserving the full ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-10T08:17:49.392414'
---

[翻译失败，原文如下]

- Funke parses HL7v2 electronic health record messages directly into native Spark types on the Databricks Lakehouse, preserving the full segment, field, component, and subcomponent hierarchy of the original message.
- It is the successor to Smolder, our 2021 Scala library, rebuilt in Python and PySpark around Unity Catalog, Declarative Automation Bundles, and Spark Declarative Pipelines.
- Funke is open source and ships with a runnable demo, so you can stand up an end-to-end HL7 ingestion pipeline and explore parsed clinical data in minutes.

## The HL7v2 problem in the lakehouse

HL7v2 is the messaging standard that quietly runs healthcare. It’s how clinical systems tell each other that a patient was admitted, that a lab order was placed, or that a result came back. Decades after it was introduced, it remains the most widely deployed integration standard in the industry, and the vast majority of care organizations still depend on it for the routine flow of operational data.

It is also hard to work with. An HL7v2 message is a nested, delimiter-encoded structure: segments made of fields, fields made of components and repetitions, components made of subcomponents, all separated by a small set of special characters that the message itself declares in its header. The specification leaves room for flexibility, so real-world messages vary from one sending system to the next.

When teams want that data in a modern format, they usually reach for one of two workarounds. They convert everything to FHIR first, which adds a translation layer and can drop detail that never had a clean FHIR equivalent. Or they hand the messages to a third-party engine that flattens the hierarchy into wide tables, which means paying another vendor, moving data out of the platform, and losing direct access to the granular structure underneath. Both paths add cost, add latency, and put distance between you and your own clinical data.

## From Smolder to Funke

In 2021 we open-sourcedSmolder, a Spark library that loaded HL7v2 messages into DataFrames so healthcare teams could run analytics on real-time EHR feeds without hand-coding parsers. Smolder made it possible to use HL7 data in the lakehouse at a time when parsing messages was a major barrier to adoption.

The platform has moved a long way since then. Unity Catalog governs data, volumes, and models. Declarative Automation Bundles package and deploy projects as code. Spark Declarative Pipelines handle streaming ingestion declaratively. But Smolder predates all of it and wasn’t built to be able to fit in cleanly with the modern Databricks platform.

Funke is the successor, rebuilt for the platform as it is today. The name is a small nod to its lineage:Funkeis German forspark. Where Smolder was a Scala data source, Funke is a Python and PySpark library plus a ready-to-deploy pipeline. It parses into native Spark types, deploys as an DAB, ingests through a Declarative Pipeline, and stores everything in Unity Catalog. Users can go from nothing to a scalable, streaming HL7 pipeline in minutes.

The idea Smolder started, HL7 as first-class lakehouse data, is the same. The implementation is new.

## What makes Funke different

Funke parses an HL7v2 message directly into a native Spark type and keeps the entire hierarchy intact. The parsing is designed to be lossless, with the goal to retain all of the original structure as far into the pipeline as possible.

A parsed message is modeled as a map from segment name to the repetitions of that segment. Each field is itself a map, addressable by field number, then repetition, then component, then subcomponent. In Spark terms:

Because the parsed message is a normal Spark column, every element is reachable with ordinary DataFrame or SQL expressions, and the parser handles the HL7 encoding rules for you: the field, component, repetition, and subcomponent separators declared in the MSH header, plus the standard escape sequences. Funke supports every HL7 message type and version, so the same pipeline can accept messages across the range of versions a health system typically receives.

As a result, your raw clinical data lands in the lakehouse with full fidelity, governed by Unity Catalog, ready to query. You get to decide which fields matter for a given use case, rather than accepting whatever shape a converter or a vendor chose for you.

## How it works: the ingestion pipeline

Funke deploys as a Declarative Pipeline that follows the medallion pattern. It defines two tables, and you build gold tables on top for your own use cases.

Figure 1: Funke data flow on the Databricks Lakehouse

![image1.png](/images/posts/396be8a7b11c.png)

Landing to bronze.New HL7 files arrive in a Unity Catalog volume. Auto Loader picks them up, decodes the content, and writes them to theraw_messagestable alongside ingestion metadata including a MD5 hash for tracking a message through the pipeline, an insert timestamp, and a message ID.

Bronze to silver.Theparsed_messagestable reads the raw stream and applies Funke's parser, adding a singlehl7column of the native type shown above. This is where unstructured message text becomes structured, queryable data.

## From a raw message to a gold table

Because thehl7column is native Spark data, you can address any element directly by segment, field, repetition, component, and subcomponent:

The same extraction works in Spark SQL, so analysts who never touch Python can build gold tables and views directly:

Positional index chains are precise, but they are hard to reason with months after development. For that reason Funke ships accessor helpers that help developers cleanly extract content.get_valuetakes the segment, its repetition, the field, the field repetition, the component, and the subcomponent, and returns the value as a column:

There are higher-level helpers too, includingget_segment,get_field,get_component,get_subcomponent, and aparse_hl7_versionhelper that reads the version straight out of the MSH header. You choose the level of abstraction that fits the query.

## See it run end to end

Funke ships with a demo so you can watch the whole flow without wiring up a live EHR feed. It includes a synthetic ADT event generator that simulates admissions, transfers, and discharges across a set of facilities, and a control-room app, built on Databricks Apps, that starts and stops the event stream and traces a message from raw text through parsed structure to gold.

![image2.gif](/images/posts/7407cced8618.gif)

The demo's gold layer is a working example in its own right. It turns the parsed ADT stream into anadt_eventshistory table, then maintains a livecurrent_censustable using change data capture keyed on the visit number, so that a discharge event removes a patient from the census and frees the bed. Abed_utilizationtable joins that live census against facility capacity to show occupied versus available beds per unit, feeding a dashboard. It is a concrete illustration of going from raw HL7 messages to an operational metric that a hospital would actually watch.

## Getting started

Funke is a Databricks Industry Solutions accelerator, deployed as an Asset Bundle:

1. Clone the repository into your Databricks workspace.
2. Open the directory in the DAB editor and clickDeploy. Deployment builds thefunkelibrary and provisions the pipeline, the Unity Catalog schema, and the landing volume for you.
3. Upload HL7 messages to the createdlandingvolume.
4. ClickRunon the HL7 ingestion pipeline.

If you prefer the command line, the same deployment runs with the Databricks CLI:

## What Funke is, and what it is not

[翻译失败，原文如下]

Funke is a parser and an ingestion accelerator. It gives you HL7v2 messages as native, governed, queryable lakehouse data, and a clean pattern for turning them into the gold tables your use cases need. It is not an interface engine, and it does not replace the clinical and HL7 expertise required to interpret those messages correctly. The mapping from a segment and field to a business concept is a decision you make with your own domain knowledge. Funke's job is to make sure that when you make that decision, the data is right there, complete and easy to reach.

## Try it

Funke is open source under the Databricks License. Explore the code, run the demo, and open an issue with feedback or ideas:

https://github.com/databricks-industry-solutions/funke-hl7v2

The test messages used in the demo come from theHL7 v2-to-FHIR project.

---

> 本文由AI自动翻译，原文链接：[Introducing Funke: Native HL7v2 Parsing on Databricks](https://www.databricks.com/blog/introducing-funke-native-hl7v2-parsing-databricks)
> 
> 翻译时间：2026-10-10 08:17
