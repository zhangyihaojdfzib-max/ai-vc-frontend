---
title: What is Data Transformation?
title_original: What is Data Transformation?
date: '2026-09-03'
source: Databricks Blog
source_url: https://www.databricks.com/blog/what-is-data-transformation
author: ''
summary: '[翻译失败，原文如下]


  - Data transformation turns raw, inconsistent data from multiple sources into standardized,
  high-quality datasets that are ready for stor...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-04T07:07:58.754465'
---

[翻译失败，原文如下]

- Data transformation turns raw, inconsistent data from multiple sources into standardized, high-quality datasets that are ready for storage, analytics and decision-making.
- Data transformation spans a wide range of operations — from cleansing, de-duplication and validation to aggregation, enrichment, joining and format changes — to improve usability, compatibility and trust in the data.
- Effective data transformation combines robust ETL patterns, performance optimizations and modern tooling (like Spark Declarative Pipelines and Lakeflow Jobs) to handle batch and streaming workloads at scale on the Data + AI Platform.

## What is data transformation?

Data transformation is the process of taking raw data that has been extracted from data sources and turning it into usable datasets. Data pipelines often include multiple data transformations, changing messy information into clean, quality, trusted data that organizations can use to meet operational needs and create actionable insights. The data transformation process is a key process indata engineering.

## Why is data transformation important?

The data transformation process is critical for realizing value from raw data. Organizations collect vast amounts of data that may include inconsistencies, missing values or duplicates. By cleaning and transforming datasets, leaders can be assured they are making decisions based on trustworthy, timely and accurate data.

Data transformation helps improve data quality by enhancing its compatibility and usability. By standardizing formats to ensure consistency across different data sources, it becomes easier for leaders to analyze and integrate quality data into their decisions.

Standardized data also reduces friction between collecting and storing data across various systems. In a business environment where data is sourced from multiple channels, maintaining uniform data is essential to achieving a cohesive understanding of information. By resolving inconsistencies and preparing it for storage in a data warehouse or data lake, data transformation creates a robust foundation for analytics, reporting and decision-making.

Data transformation is also crucial for identifying and removing any duplicate records and cleaning up any missing values within a dataset. Missing or duplicate data can skew analysis and hinder the ability to draw meaningful conclusions.

Additionally, data transformation ensures compatibility with various analytical tools and techniques. Raw data, for instance, often exists in disparate formats or structures, and this can be difficult to integrate with different analytical software or platforms. Standardizing data helps seamlessly integrate it across platforms so it can be mined for patterns and insights.

## Data transformation and ETL

Data transformation is at the heart of extract, transform, load (ETL). This is the process data engineers use to pull data from different sources, transform it into a usable and trusted resource and load that data into the systems end users can access and use downstream to solve business problems. In the transform stage, data gets cleansed, mapped and transformed, often to a specific schema.

## Data transformation examples

Several different types of transformation can be used to ensure the quality and integrity of data. These range from data de-duplication, which increases data quality and performance by removing duplicated data, to data refining, which increases quality by filtering out data that is irrelevant, to data integration, in which different data types are merged into the same structure.

### Data transformation in practice: Navy Federal Credit Union

Navy Federal Credit Union is the largest credit union in the world, serving 13 million member-owners. Their priority is to provide a personalized, omnichannel experience to their members. But to understand their members better, they needed to ingest and analyze online telemetry data in real time. To accomplish that, Navy Federal turned to Spark Declarative Pipelines and Databricks SQL.

Using Spark Declarative Pipelines, Navy Federal was able to complete a proof of concept in a week; develop, test and figure out a CI/CD process in three weeks; deploy the pipeline to production just before the start date of the first wave migration; and release the dashboard just a few days later. “The simplicity of the Spark Declarative Pipelines programming model combined with its service capabilities resulted in an incredibly fast turnaround time,” Jian (Miracle) Zhou, Senior Engineering Manager at Navy Federal Credit Union, said. “It truly allowed us to get a whole new type of workload to production in record time with good quality.”

For more types of data transformation and their definitions, see the next section.

### The agentic AI playbook for the enterprise

![ai](/images/posts/739dac6fa259.png)

## Types of data transformation

The data transformation process can be accomplished via several different techniques, depending on the data and end transformation goal. These may include:

- Bucketing/binning:Dividing a numeric series into smaller “buckets” or “bins.” This is done by changing numeric features into categorical features using a set of thresholds.
- Data aggregation:The process of summarizing data so it can be better used in reporting and visualization. Aggregation can be achieved by using different methods, such as using the sum, average or median of values over time, space or other dimensions.
- Data cleansing:The process of increasing data accuracy and quality by deleting inaccurate, incomplete or out-of-date information.
- Data de-duplication:A compression process in which duplicate copies of data are identified and removed to speed up the data transfer process.
- Data derivation:Creating rules to extract only the specific information needed from the data source.
- Data enrichment:A process of enhancing existing data using external data sources to expand a data field or supplement missing data fields.
- Data filtering:Refining data to eliminate irrelevant data to display only the information that is needed.
- Data integration:Merging different data types into the same structure. Data integration standardizes disparate data so that it can be analyzed as a whole.
- Data joining:An operation that merges multiple database tables using a common data field into a single dataset.
- Data splitting:Dividing a single column into multiple columns in order to analyze the data. This can be useful for analyzing large amounts of data gathered over time.
- Data summarization:A type of data aggregation in which different business metrics are created by calculating value totals.
- Data validation:Ensuring data quality by creating automated rules that generate responses to specific data issues.
- Format revision:The process of changing formats to solve problems related to fields containing different data types.
- Key restructuring:The process of changing keys with built-in meanings to generic keys (random numbers that reference the information in the source database) to prevent slowdowns in the data system.

## Data transformation performance optimizations

The data transformation process can be both time- and resource-consuming, so optimizing data transformation performance is crucial to reduce costs and save time. Performance optimization techniques include:

[翻译失败，原文如下]

- Data compaction:This technique involves reducing data’s storage footprint by consolidating smaller files into larger ones, eliminating redundant or unnecessary data, and optimizing the format for efficient reading and writing.
- Partitioning:This involves dividing a large dataset into smaller, more manageable partitions based on specific criteria, such as date, region or category. This can improve query performance by allowing for parallel processing and reducing the amount of data that needs to be scanned.
- File size tuning:This involves adjusting file sizes to balance performance and resource utilization. This can involve splitting large files into smaller chunks or combining small files into larger ones.
- Data skipping and pruning:This technique involves skipping over irrelevant data or pruning unnecessary data to minimize the amount of data read and processed. By leveraging approaches such as metadata, indexing or partitioning, the system can eliminate unnecessary data scans that result in significant performance gains.
- Data caching:This refers to the process of storing frequently accessed data in memory or fast-access storage layers, reducing the need to reprocess or fetch data from slower sources repeatedly. This can significantly improve read performance and reduce latency.

Learn more about optimizing data transformation performance with ourcomprehensive guide.

## Data transformation tools

Data transformation is critical for creating reliable data that organizations can use for insights. However, the data transformation process and the entire ETL process present serious challenges, from building and maintaining reliable data pipelines to managing data quality in increasingly complex pipeline architectures. Data transformation tools streamline and democratize transformation and simplify the ETL lifecycle. However, there are some key differences among the way ETL tools may operate.

### Batch processing vs. streaming

Batch processing refers to the process of extracting, transforming and loading data in chunks and at intervals. This is an excellent tool for processing large amounts of data efficiently and is ideal when data does not need to be processed in real time.

Streaming means that data is processed as it is received. This continuous data extraction is best for organizations that need up-to-date information, such as in a live dashboard or real-time monitoring and alerting.

Some ETL tools can handle both batch and streaming processing, while others are more tailored for one or the other.

### On-premises vs. cloud

On-premises ETL runs within an organization ’s own infrastructure. This model gives you full control over data security, storage and processing, but it also requires significant hardware and maintenance costs.

ETL tools in the cloud offer businesses more flexibility and cost efficiency. They integrate seamlessly with cloud storage solutions and cloud data warehouses and often have built-in automation features to make data processing more efficient.

### Open source vs. proprietary

Open source tools are ideal for businesses that want flexibility and customization. Engineers can study the source code to determine the precise build of the infrastructure and modify its capabilities to best suit an organization’s data needs. Keep in mind that the documentation and functionality may vary in these tools, since they are often created by a decentralized group of developers.

There are numerous proprietary ETL systems. Since these tools are backed by major organizations — and not a diffuse group of engineers — customers usually benefit from smoother implementation and maintenance, as well as customer support and frequent updates.

### No-code/low-code vs. codable

No-code tools are great for less technical users or those without data engineering experience. Instead of code, these use graphical user interfaces (GUIs) where users can drag and drop components to design ETL workflows. While they aren’t as customizable as low-code tools, they do offer simple solutions for organizations that need quick and simple data integration tools.

Fully codable ETL tools allow users to take full control over their ETL pipelines and write custom code to define precise instructions for their data. These tools are designed for more technical users, such as data engineers or developers.

In the middle lie low-code ETL tools, geared toward semi-technical users who may have some coding experience but who want to avoid extensive manual coding. Low-code ETL tools provide a mix of visual interfaces and coding options. Users can still build workflows with drag-and-drop elements, but also have the option to customize certain steps through scripting or pre-built code snippets.

## Data transformation on the Data + AI Platform

Databricks offers essential tools for implementing and orchestrating data transformations and ETL on theData + AI Platform.

Spark Declarative Pipelineshelps data engineering teams easily build and manage reliable batch and streaming data pipelines that deliver high-quality data on the Data + AI Platform. Spark Declarative Pipelines simplifies ETL development and management with declarative pipeline development, automatic testing and deep visibility for monitoring and recovery.

The transformation process can be complex. Make sure you’re equipped with the following features to get the results you need:

Data quality checks.These guarantee that data input into tables meets quality standards. For instance,Spark Declarative Pipelineshas a feature called Expectations, which ensures data quality checks are applied to every record passing through a query.

Easy-to-understand architecture.This ensures that data is stored in a logical and accessible manner. For instance, with themedallion architecture, data quality is incrementally improved as it passes through each layer.

Different update modes.Options such as triggered mode (where processing is halted after refreshing tables, ensuring updates are in line with available data at the start of the update) and continuous mode (where new data is processed as soon as it arrives) allow for better control over your data.

Lakeflow Jobsis a fully integrated managed orchestration service that empowers data teams to better automate and orchestrate data pipelines.Lakeflow Jobshelps users easily define, manage and monitor multitask workflows for ETL, analytics and machine learning pipelines to boost productivity. Lakeflow Jobs can easily integrate with other popular tools likedbtorCoalesce.

## Additional Resources

- Data Engineering on the Data + AI Platform

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[What is Data Transformation?](https://www.databricks.com/blog/what-is-data-transformation)
> 
> 翻译时间：2026-09-04 07:07
