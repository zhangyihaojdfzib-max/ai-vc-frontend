---
title: Unlock powerful insights and forecasts with Predictive AI Functions
title_original: Unlock powerful insights and forecasts with Predictive AI Functions
date: '2026-10-14'
source: Databricks Blog
source_url: https://www.databricks.com/blog/unlock-powerful-insights-and-forecasts-predictive-ai-functions
author: ''
summary: '[翻译失败，原文如下]


  - Predictive AI Functions let business users and SQL analysts create forecasts,
  detect anomalies, analyze what''s driving a metric, and ma...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:41:11.124720'
---

[翻译失败，原文如下]

- Predictive AI Functions let business users and SQL analysts create forecasts, detect anomalies, analyze what's driving a metric, and make predictions — all without advanced ML expertise.
- AI Functions are easy to use in Genie and embed in existing workflows without requiring users to build and maintain models
- The launch includes five functions: an upgraded ai_forecast, plus the new ai_top_drivers, ai_detect_anomalies, ai_predict_value, and ai_predict_class.

Data teams all get asked the same questions: "what will sales be next quarter?," "why did this metric move?," and "is this recent data outside the norm of what we typically see?" Answering these advanced analytics questions usually means handing the work to a data science team to build models and manage infrastructure. This creates a bottleneck where business users wait in line and many questions never even get asked.

Predictive AI Functions, now in Beta, remove that bottleneck by letting analysts and business users run advanced analytics like forecasting, driver analysis, and anomaly detection, all through built-in functions backed by state-of-the-art ML models. These SQL-native functions can be called directly in SQL, invoked inGeniewith plain-language questions, or embedded in dashboards. Because Databricks maintains the models centrally, teams get high-quality, consistent answers without building or managing infrastructure.

This launch adds four new SQL native functions and improved accuracy toai_forecast:

- ai_forecast: project a time series into the future
- ai_top_drivers: find which segments most drove a change in a metric
- ai_detect_anomalies: flag outlier rows in temporal data
- ai_predict_value: predict continuous values (regression)
- ai_predict_class: predict categorical values (classification)

To showcase how these functions can be used across Databricks, we'll walk through examples in dashboards, SQL, and Genie using the NYC taxi trips dataset.

## Trustworthy forecasts in dashboards

Dashboards are where teams watch the metrics that run their business, and often where they turn to see where those metrics are headed next. Withai_forecast, teams can project metrics and surface those forecasts alongside the rest of their reporting.

The newai_forecastmakes it easy to get high-quality forecasts without any tuning. It's powered by a transformer-based time series foundation model, pretrained on a huge, diverse collection of time series the way a large language model is trained on text. Because it already recognizes common patterns like seasonality and trends, it produces accurate forecasts on your data with no tuning required.

The visualization below usesai_forecastto project the monthly ride volumes in the NYC taxi trips dataset through the end of 2027. The forecast reveals expected seasonal patterns in taxi demand, providing a data-driven view of where ridership is headed.

![image1.png](/images/posts/5904e90d7203.png)

The newai_forecastnot only handles general patterns automatically, it also introduces features to let teams add factors specific to their business. With built-in holiday support, teams can automatically account for local events like Christmas dips and school-holiday spikes. Teams can also specify external covariates, feeding in the factors that drive a metric, such as pricing changes or marketing spend, so forecasts better reflect their business.

## Powerful predictions from plain language

This launch also introduces four new functions for the ad-hoc advanced analytics questions commonly asked by data teams.

- ai_top_driversexplains why a metric moved
- ai_detect_anomaliesflags values that look off
- ai_predict_valueandai_predict_classfill in missing values by estimating a number or assigning a category.

Each one, likeai_forecast, is a native SQL function. Analysts can call them directly in the SQL editor or a notebook, run them across hundreds of millions of rows, and feed the results into their queries and pipelines alongside the rest of their work. Compared to developing custom models for similar functionality, this compresses development time and increases accessibility to more users.

For example, the query below aggregates NYC taxi trips into a daily revenue time series and passes it toai_detect_anomalies, which automatically fits a model to the data and flags unusual days.

These same functions will be available to business users through Genie (ai_top_driversis available today, withai_forecast,ai_detect_anomalies,ai_predict_value, andai_predict_classcoming soon). Anyone can ask a question in plain language, like why revenue dropped last quarter or which customers are likely to churn, and Genie calls the right function to return a grounded, model-backed answer, with no SQL or ML expertise required.

The query below usesai_top_driversto automatically identify which time-of-day and weekday/weekend segments contributed the most to the change in NYC taxi fare revenue between January and February 2016. It ranks each segment by its absolute and relative revenue impact, revealing that weekday midday hours drove the largest gain while the weekday evening rush was the biggest drag.

![image3.png](/images/posts/e682b89a3cce.png)

Because these functions use tailored machine learning methods, they enable Genie to answer questions a general-purpose LLM cannot reliably handle on its own.

## Industry-leading quality

These functions all deliver high-quality predictions backed by production-grade ML models. Because Databricks maintains those models centrally, that quality stays consistent across every surface, so teams get the same trustworthy result whether a prediction runs in a dashboard, in SQL, or through Genie.

Forecasting shows this most concretely. We usedfev-benchto benchmark the new ai_forecast against functions from a leading cloud data warehouse. Task win rate is defined as the percentage of tasks (measured by scaled quantile loss) where one system achieves a lower probabilistic error than the other. Here's how the options compare:

![image4.jpg](/images/posts/1d42b2e70a1e.jpg)

ai_forecastoutperforms other cloud data warehouse providers as well as the previous version ofai_forecast. With Predictive AI Functions, teams get industry-leading accuracy out of the box, on every surface, with no tuning required.

## Get started today

Predictive AI Functions turn questions that once required a data science team, like what's next, why did it change, what's wrong, and what's the value, into answers business teams can get themselves, right where they already work: in dashboards, in Genie, and in SQL. The result is advanced analytics for everyone: high-quality predictions that are easy to use, with no models to build or infrastructure to manage.

Ready to try it? Get started with Predictive AI Functionshere.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Unlock powerful insights and forecasts with Predictive AI Functions](https://www.databricks.com/blog/unlock-powerful-insights-and-forecasts-predictive-ai-functions)
> 
> 翻译时间：2026-10-16 06:41
