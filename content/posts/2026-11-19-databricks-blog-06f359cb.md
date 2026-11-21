---
title: Java4Shell vulnerability (CVE-2026-114938) assessment
title_original: Java4Shell vulnerability (CVE-2026-114938) assessment
date: '2026-11-19'
source: Databricks Blog
source_url: https://www.databricks.com/blog/java4shell-vulnerability-cve-2026-114938-assessment
author: ''
summary: '[翻译失败，原文如下]


  As of November 19 at 10 AM Pacific Time:


  Prior toJava4Shell’s public disclosure (CVE-2026-114938), Databricks was already
  addressing the...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-21T09:25:33.781082'
---

[翻译失败，原文如下]

As of November 19 at 10 AM Pacific Time:

Prior toJava4Shell’s public disclosure (CVE-2026-114938), Databricks was already addressing the industry-wideOpenJDKvulnerability.

Databricks is protecting customers in two phases: quick mitigation to disable use of the vulnerable code, and then patching to replace the vulnerable code.

- Mitigation:We have applied the mitigation to our platform, disabling use of vulnerable code for allsupported versions of Databricks Runtime. We do not expect the mitigation to have a meaningful performance impact on customers. In order to apply the mitigation as quickly as possible, we have taken the rare step of proactively restarting affected clusters.
- Patching:While the mitigation blocks the attack, in an abundance of caution, we will be providing patched versions of supported Databricks Runtimes. Customers on our serverless platform will automatically get them. Customers with classic clusters will need to restart their clusters.

We are also reaching out to customers running custom images.

We have no evidence to indicate any unauthorized access to Databricks products, services, or customers' data.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Java4Shell vulnerability (CVE-2026-114938) assessment](https://www.databricks.com/blog/java4shell-vulnerability-cve-2026-114938-assessment)
> 
> 翻译时间：2026-11-21 09:25
