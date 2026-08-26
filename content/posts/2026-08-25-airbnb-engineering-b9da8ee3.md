---
title: 'Project Lighthouse — Part 3: Introducing project-lighthouse-anonymize'
title_original: 'Project Lighthouse — Part 3: Introducing project-lighthouse-anonymize'
date: '2026-08-25'
source: Airbnb Engineering
source_url: https://medium.com/airbnb-engineering/project-lighthouse-part-3-introducing-project-lighthouse-anonymize-74f8b26653fb?source=rss----53c7c27702d5---4
author: ''
summary: '[翻译失败，原文如下]


  # Project Lighthouse—Part 3: Introducing project-lighthouse-anonymize


  ## The data in Project Lighthouse is powered by privacy-preserving...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T03:00:19.733010'
---

[翻译失败，原文如下]

# Project Lighthouse—Part 3: Introducing project-lighthouse-anonymize

## The data in Project Lighthouse is powered by privacy-preserving anonymization code. We’ve put this code into open source, and published two new technical papers detailing the scalable algorithms and data quality frameworks behind it.

Listen

By:Adam Bloomston

## Introduction

In 2020, we launched Project Lighthouse, which we developed in partnership with leading civil rights and privacy organizations. As our 2020announcementdetails, Project Lighthouse enables us to measure potential disparities in user experiences. This work uses perceived race data that is never linked to individual accounts; we only use this data for measuring potential disparities, and users who want to opt-out can do so by turning off the data use settings in their account’s Privacy page.Our results, shared in 2024, demonstrate how we use these analyses to measure our progress in mitigating those disparities.

Earlier this year, we open-sourcedproject-lighthouse-anonymize, the Python library that powers Project Lighthouse’s anonymization process. To provide the full technical foundation for this work, we also published two new papers on arXiv alongside the code release. Together with our original 2020 paper, these three papers form a complete story: the foundational methodology, the scalable implementation, and the quality validation framework.

## The foundational methodology (2020)

Our original 2020 paperestablished the privacy-by-design approach for Project Lighthouse and provides the rationale for choosing k-anonymity as the technical privacy model to prevent sensitive attribute disclosure at scale. For an introduction to this paper, see ourfirst blog poston p-sensitive k-anonymity and oursecond blog poston measurement with anonymized data.

## Core Mondrian: Scalable partition-based anonymization (2025)

The first of our new papers,Core Mondrian: Basic Mondrian beyond k-anonymity, presents the k-anonymity algorithm at the heart of the open source library. Core Mondrian extends theclassic Mondrian algorithmwith:

- Extensible architecture, using the Strategy Pattern to support k-anonymity and future privacy model extensions
- Parallel processing, with a hybrid recursive-queue execution model (combining immediate recursive processing for small partitions with queue-based parallel processing for large partitions)
- Other enhancements, including NaN-pattern pre-partitioning (accommodating missing values) and dynamic suppression budget management

This algorithm enables scalable anonymization of large datasets while preserving the ability to use the underlying data for statistical analyses.

## Measuring Data Quality for Project Lighthouse (2025)

The second of the new papers,Measuring Data Quality for Project Lighthouse, addresses a critical question: how do you know if your anonymized data are “good enough” for your analysis?

The paper introduces a comprehensive framework for measuring data quality under anonymization, including:

Three primary metrics:

- Pearson correlation (preserving linear relationships between original and anonymized values)
- Revised Information Loss Metric or RILM (measuring how well the “shape” or geometric size of data is preserved — higher scores mean less distortion)
- Normalized Mutual Information v1 or NMIv1 (measuring entropy preservation, essentially how much information content is retained)

Empirical validation methodology: We reframe data quality assessment as a machine learning classification problem, using synthetic datasets to validate that our metrics and thresholds successfully predict when anonymized data will produce statistically valid results

Default thresholds: The paper and library include the specific threshold values we use for Project Lighthouse, which may serve as useful starting points for others implementing similar systems

This framework enables analysts without deep anonymization expertise to confidently assess whether their anonymized data supports valid statistical conclusions.

## Getting started

The library is available on PyPI and GitHub atgithub.com/airbnb/project-lighthouse-anonymize. With this library, you can successively enforce both technical privacy models fromour 2020 paper:

```
p, k = 2, 5# First technical privacy model: k-anonymityanon_df, dq_metrics, disclosure_metrics = k_anonymize(logger, input_df, qids, k, {}, "row_id")# Second technical privacy model: p-sensitive k-anonymity via perturbationsensitized_df, _, _ = p_sensitize(logger, anon_df, qids, "race", p, k, sens_attr_value_to_prob)
```

The algorithm for enforcing k-anonymity is described inCore Mondrian: Basic Mondrian beyond k-anonymity. And the data quality metrics and thresholds for k-anonymity are described inMeasuring Data Quality for Project Lighthouse:

```
minimum_dq_met, minimum_dq_met_reasons = check_dq_meets_minimum_thresholds(dq_metrics)assert minimum_dq_met, str(minimum_dq_met_reasons)
```

Thegetting started guidebuilds on the code snippets above and provides a complete, runnable example using theUCI Adult dataset.

## Conclusion

We continue to invest in trying to combat potential discrimination and bias users may face when using Airbnb, and in taking steps to enable everyone in our global community to use and enjoy Airbnb. We believe that doing so requires transparency in our methodologies, both to build trust with our users and to encourage other companies to do the same.

If this type of work interests you, check out some of ourrelated positions!

## Acknowledgements

The Airbnb Anti-discrimination & Equity team is Adam Bloomston, Elizabeth Burke, Megan Cacace, Anne Diaz, Wren Dougherty, Matthew Gonzalez, Remington A. Gregg, Yeliz Güngör, Eeway Hsu, Heesoo Kim, Sara Kwasnick, Joanne Lacsina, Demma Rosa Rodriguez, Adam Schiller, Jessica Simon, Maggie Tang, Skyler Wharton, Marilyn Wilcken. I also want to thank Natalija Fijacko, Lauren Mackevich, Laura Rillos, Jessica Simon, Floyd Smith, and Lei Wei for their role in refining and improving this blog post.

The author acknowledges the use of Large Language Models (LLMs) for assistance with literature review, technical writing, and editing.

All product names, logos, and brands are property of their respective owners. All company, product, and service names used in this website are for identification purposes only. Use of these names, logos, and brands does not imply endorsement.

---

> 本文由AI自动翻译，原文链接：[Project Lighthouse — Part 3: Introducing project-lighthouse-anonymize](https://medium.com/airbnb-engineering/project-lighthouse-part-3-introducing-project-lighthouse-anonymize-74f8b26653fb?source=rss----53c7c27702d5---4)
> 
> 翻译时间：2026-08-26 03:00
