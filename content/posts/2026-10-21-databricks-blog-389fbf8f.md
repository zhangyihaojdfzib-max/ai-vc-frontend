---
title: AI Runtime is Generally Available
title_original: AI Runtime is Generally Available
date: '2026-10-21'
source: Databricks Blog
source_url: https://www.databricks.com/blog/ai-runtime-generally-available
author: ''
summary: '[翻译失败，原文如下]


  - AI Runtime is now generally available, bringing high-performance GPU infrastructure
  directly into Databricks.

  - Scale reliably and expe...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-22T06:56:03.601315'
---

[翻译失败，原文如下]

- AI Runtime is now generally available, bringing high-performance GPU infrastructure directly into Databricks.
- Scale reliably and experiment faster with seconds-level launches, flexible environments, and integrated observability — without the overhead of managing GPU infrastructure.
- Keep every training workload secure and governed with built-in Unity Catalog controls and workload isolation — in a new era of agent-led training.

Today, we’re excited to announce the General Availability of AI Runtime (AIR),bringing fully managed GPU infrastructure directly into Databricks so customers can train their most demanding models where their enterprise data already lives.

Too often, AI teams spend more time securing GPU capacity, managing failures, and waiting for experiments to launch than improving their models. Running GPU infrastructure separately from their Lakehouse adds governance gaps and puts sensitive training data at risk. Ascoding agents drive more training experiments, these bottlenecks andrisksgrow — making reliable, fast, and governed infrastructure essential.

AIR brings GPU infrastructure, developer tools, and data governance together so teams can train at scale, iterate faster, and secure every workload without managing a separate GPU stack. Hundreds of companies, including Robinhood, PicPay, Merck,Flo Health,TinyFish, andFactSet, already use AIR to train and ship deep learning models to production, with use cases spanning healthcare, manufacturing, and consumer-facing agents. Our ownDatabricks AI Research team uses AIRto train the models behind KARL and AI Parse.

With AIR, customers can:

- Train at scale with hassle-free GPU infrastructure:Serverless, on-demand access to advanced GPUs backed byreliable multinode training, optimizedperformance, and battle-tested by 100,000+ GPU-hour training runs.
- Experiment faster with near-instant launch latency and easy debugging:Bring your own code, containers, and Ray workloads – and obtain seconds-level launch latency on RDMA-enabled GPUs. Environment caching and built-in debugging tools to save time on every training loop.
- Secure and govern every GPU workload:AIR operates within the governance perimeter of Databricks and Unity Catalog, and is backed by years of investment in Serverless security. AIR helps ensure GPU workloads protect valuable training data, comply with access policies, and are tracked/auditable.

## Hassle-free GPU infrastructure

Managing GPU infrastructure requires significant operational overhead, from capacity planning and node maintenance to networking and monitoring.

With AIR, Databricks takes on the operational work of provisioning GPUs, maintaining healthy infrastructure, and optimizing the workload, so your team can focus on training:

- Get the GPU capacity you need, on demand.Databricks handles GPU procurement, cluster configuration, and networking so your team can start training without building and operating a full GPU platform.
- Scale with confidence on healthy infrastructure.Databricks runsdozens of checks for GPU and network health before and during training, so your workloads can scale to hundreds of GPUs reliably.
- Efficient training by default:Built-in data loaders stream and cache training data to reduce time spent waiting on I/O. Use tools such asUCVolumeDatasetto improve data throughput without building a custom loading pipeline.

![AI Runtime validates GPUs before scheduling, continuously monitors active workloads, and periodically tests idle GPUs to detect and remove unhealthy nodes.](/images/posts/5854b82532a2.gif)

Use GPUs wherever you work

Access GPUs via CLI or interactively within Notebooks or IDEs. Your first workload just requires a single CLI command. WithDatabricks AIR Skills, migrating from a K8S or SLURM cluster just takes a single natural language prompt.

![](/images/posts/4557940bbc4f.gif)

Orchestrate GPU workloads with confidence with Lakeflow

AIR integrates natively withLakeflowso you can keep GPU workloads in sync with upstream and downstream pipelines. Moving to production requires just a few extra lines of YAML, with built in priority/pre-emption that minimize idle GPU time and monitoring tools likeGenie ZeroOpsthat lower operational toil.

![](/images/posts/08b069b38411.png)

## Experiment, debug, and iterate faster

Distributed training workloads are painful to set up and launch. AI teams waste time configuring training environments, waiting for GPU clusters to spin up, and debugging issues across the stack.

AIR helps you get from code to training in seconds. You can use pre-built environments orbring your own container, and benefit from highly optimized environment caching so you just need to build environments once. AIR is compatible with all major frameworks, including Ray, so you can bring code over with minimal configuration.

Launch your next experiment in seconds

When you iterate and develop a training script, every second of delay is felt repeatedly. And so, we’veoptimized every layer of the provisioning stackto make workloads, even large scale RDMA-enabled clusters with dozens of GPUs, spin up in seconds.

![Unlike legacy GPU stacks that require full container image downloads before running code, AI Runtime uses warm serverless GPU pools and lazy image loading to start workloads in seconds, while continuing to load the remaining image data in the background.](/images/posts/ff1a113764ea.gif)

Debug distributed training in one place

We’ve built an entirely new observability experience in MLflow, the industry’s leading experiment tracking tool. With this new experience, debugging your logs, which stream seconds after submission, is as simple as adding–watchto your AIR command. For deeper investigation, you can use our new logs viewer, tailor-built for multinode training.

![Genie Code accelerates debugging by analyzing AI Runtime training logs, identifying issues, and recommending next steps directly within Databricks.](/images/posts/906fbaee3ddf.png)

Agentic debugging with built-in Genie Code

Genie Code is embedded into the entire user experience, and comes pre-packaged with agent skills to help you debug issues and optimize GPU training performance. These skills include insights that our research and performance teams discover, like how wereduced Qwen training time by 6x on AIR.

![](/images/posts/08fd88a19c7c.png)

## Secure and govern every GPU workload as part of the Lakehouse

Managing GPU infrastructure separately from enterprise data creates governance gaps, fragmented access controls, and unnecessary data copies. As agents run hundreds of training experiments in parallel, teams need to ensure sensitive data stays governed and workloads remain securely isolated, without relying on manual oversight.The OpenAI Huggingface incidentunderscores this risk.

AIR extends your trusted data controls and governance to every GPU workload. Unity Catalog enforces consistent read/write permissions on all aspects of a GPU workload (data access, checkpoints, logs, etc.), so your GPU platform and data governance layer now speak the exact same language.

Isolate workloads and control network access

AIR is backed by years ofinvestment in serverless security, isolation, and private networking. Unlike GPU isolation mechanisms that expose the host kernel, AIR has VM-level isolation, supports PrivateLink and serverless egress controls. Thus AIR offers much stronger protections for training workloads compared to conventional systems.

Understand where your GPU budget goes

Track AIR usage and costs throughDatabricks billing system tables, alongside your other Databricks workloads. Use workload-level usage records to identify which training workloads consume your GPU budget and guide decisions about future runs.

## Get started with your first GPU workload

To help you get started, we’ve put together several template notebooks and starter guides:

[翻译失败，原文如下]

- Please see ourquickstartto get started, and connect to AI Runtime in seconds.
- To learn more about AI Runtime, watch our3-minute demoand visit ourweb page.
- Interested in trying AIR out on an example?Clone our cookbook repoto get started in just one CLI command!

Please reach out to your account team to learn more or if you have any questions!

---

> 本文由AI自动翻译，原文链接：[AI Runtime is Generally Available](https://www.databricks.com/blog/ai-runtime-generally-available)
> 
> 翻译时间：2026-10-22 06:56
