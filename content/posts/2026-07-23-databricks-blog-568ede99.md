---
title: Connect Amazon S3 data to Databricks with Delegated IAM Permissions
title_original: Connect Amazon S3 data to Databricks with Delegated IAM Permissions
date: '2026-07-23'
source: Databricks Blog
source_url: https://www.databricks.com/blog/connect-amazon-s3-data-databricks-delegated-iam-permissions
author: ''
summary: '[翻译失败，原文如下]


  - Why simpler S3 connectivity matters

  - How AWS IAM temporary delegation for S3 works

  - How to set up an external location with the new f...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-07-25T05:00:49.905709'
---

[翻译失败，原文如下]

- Why simpler S3 connectivity matters
- How AWS IAM temporary delegation for S3 works
- How to set up an external location with the new flow

## Importance of Simpler S3 connectivity

Connecting Amazon S3 is one of the most important setup steps to getting value out of Databricks. External locations provide the governed connection between your S3 bucket and Unity Catalog so Databricks can read and write data securely. This setup is foundational for common workflows, from ingestion and pipelines to analytics and governance. It is also increasingly important as more people adoptLTAP (Lake Transactional/Analytical Processing), a new architecture designed to unify transactional and analytical data on a single governed foundation without the traditional overhead of pipelines, replicas, and ETL.

Today, customers authorize S3 connectivity by creating an external location, a Unity Catalog object that combines a storage path with a storage credential to authorize read and write access to your S3 bucket.

![image1.png](/images/posts/0f178f8673b3.png)

Until now, connecting to S3 has often been one of the most painful parts of getting started on Databricks. Automatic setup helps customers spend less time managing cloud infrastructure, and more time building data intelligence on top of their data.

## How automated S3 connectivity works

Connecting an Amazon S3 bucket to Databricks requires creating an external location, a connection registered in Unity Catalog that governs how Databricks reads and writes your data. Previously, that meant authoring 140-line IAM trust policies, configuring S3 bucket permissions, deploying CloudFormation templates, and toggling between the AWS console and Databricks to register everything correctly.

Now, we’ve made it a few simple clicks:

![image2.gif](/images/posts/641dd542edbe.gif)

### What’s happening under the hood?

This new flow is powered byAWS IAM temporary delegation. After you specify your S3 bucket and access level, you are prompted to log into AWS to verify your permissions. If you have sufficient access, you are able to grant Databricks a temporary, time-bounded authorization to provision the required resources on your behalf. For users that lack sufficient AWS permissions can directly request them from their AWS admin within the flow.

With that delegation in place, Databricks automatically handles the rest:

- Storage credential: An IAM role with least-privilege permissions is created and the cross-account trust policy is correctly configured.
- External location: A fully configured external location registered in Unity Catalog, mapped to your specified bucket. Auto Loader and File Events are enabled automatically.Once the setup completes, the authorization automatically expires. Databricks never holds standing access to your AWS account, and all actions taken during provisioning are logged in AWS CloudTrail.

## What this means in practice

The manual configuration work that previously lived across multiple consoles now happens in a single session natively from the Databricks workspace. Automated provisioning eliminates the most common failure modes like incorrect trust policies, missing bucket permissions, misconfigured ARNs, while also ensuring every IAM role created follows least privilege principles aligned to enterprise security standards.

As more people adopt the LTAP architecture, simpler S3 connectivity removes a key infrastructure barrier by providing a governed cloud storage destination where operational data can be instantly queryable by analytical engines without requiring separate pipelines.

## Learn more

In your workspace, navigate to Catalog Explorer → External Locations → Create (/explore/locations/create) to automatically connect your S3 bucket with automatic setup.

For more information:

- Learn more about external location setup options
- From monolith to Lakebase to LTAP: rethinking the database from storage up
- Learn more about AWS IAM temporary delegation

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Connect Amazon S3 data to Databricks with Delegated IAM Permissions](https://www.databricks.com/blog/connect-amazon-s3-data-databricks-delegated-iam-permissions)
> 
> 翻译时间：2026-07-25 05:00
