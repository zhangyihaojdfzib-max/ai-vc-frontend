---
title: Vercel Daemons is now in public beta - Vercel
title_original: Vercel Daemons is now in public beta - Vercel
date: '2026-10-15'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-daemons-is-now-in-public-beta
author: ''
summary: '[翻译失败，原文如下]


  Vercel Daemonsis now in public beta, allowing you to run long-running processes
  that pull and execute work fromVercel Queues, databases, ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-23T07:13:49.146208'
---

[翻译失败，原文如下]

Vercel Daemonsis now in public beta, allowing you to run long-running processes that pull and execute work fromVercel Queues, databases, or third-party systems without requiring an HTTP server:

- Consumers usingVercel Queues poll mode, Celery, BullMQ, RabbitMQ, or Kafka.
- Temporal or Cadence workers that long-poll their task queues.
- Self-hosted CI runners for GitHub Actions, GitLab, or CircleCI that poll for jobs without requiring inbound connections.

Consumers usingVercel Queues poll mode, Celery, BullMQ, RabbitMQ, or Kafka.

Temporal or Cadence workers that long-poll their task queues.

Self-hosted CI runners for GitHub Actions, GitLab, or CircleCI that poll for jobs without requiring inbound connections.

Daemons run containers on Fluid compute and deploy alongside your app in the same project. Vercel builds your image and maintains the instance count you configure in each region, restarting instances that exit or crash.

Get started by packaging your application and dependencies in a Dockerfile or Containerfile, then adding adaemonsentry to one configuration file at your project root. This example usesworker/Dockerfileto run one Celery worker iniad1(Washington, D.C.):

```
12[daemons.celery]3root = "worker/"4entrypoint = "Dockerfile"5command = ["celery", "-A", "app", "worker", "--loglevel=info"]6instances.iad1 = 1
```

A Celery worker on Vercel

Set any connection details your worker needs in your project's production environment variables, then deploy to production. Vercel starts the configured instances, and their output appears in your project'sLogs. CPU and memory metrics are available withObservability Plus.

Learn more in theVercel Daemons documentation.

---

> 本文由AI自动翻译，原文链接：[Vercel Daemons is now in public beta - Vercel](https://vercel.com/changelog/vercel-daemons-is-now-in-public-beta)
> 
> 翻译时间：2026-10-23 07:13
