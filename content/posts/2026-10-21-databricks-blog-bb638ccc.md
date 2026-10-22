---
title: Databricks AI Runtime and NVIDIA make it easier to customize open models with
  enterprise data
title_original: Databricks AI Runtime and NVIDIA make it easier to customize open
  models with enterprise data
date: '2026-10-21'
source: Databricks Blog
source_url: https://www.databricks.com/blog/databricks-ai-runtime-nvidia-train-fine-tune-models
author: ''
summary: '[翻译失败，原文如下]


  - Databricks AI Runtime (AIR) is now Generally Available (GA), helping teams train
  and fine-tune models faster on serverless NVIDIA GPUs ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-22T06:56:02.960489'
---

[翻译失败，原文如下]

- Databricks AI Runtime (AIR) is now Generally Available (GA), helping teams train and fine-tune models faster on serverless NVIDIA GPUs without the complexity of managing GPU infrastructure.
- AIR supports NVIDIA NeMo and containers so teams can train and fine tune models on serverless NVIDIA GPUs alongside governed enterprise data.
- Databricks uses NVIDIA Kumo open models to accelerate predictions from structured data and NVIDIA Nemotron Retriever models to find relevant evidence from unstructured data, enabling agents to make informed decisions and take action within Databricks workflows.
- Developers can leverage Genie Code, NVIDIA-specific Agent Skills and our joint Nemotron cookbooks to get started with model customization on AIR.

GPUs power today's most advanced AI workloads, from cutting-edge language models to multimodal AI systems and agents. Increasingly, enterprises are adapting open models to their own data and business needs. But securing GPU access is only part of the challenge. Teams also need to configure training jobs, govern data access, and manage GPU infrastructure, leaving less time to experiment with models and evaluate how well they meet business needs.

Databricks and NVIDIA provide a seamless path from enterprise data to customized AI models, from fine-tuning smaller models to large-scale distributed training. Through Unity Gateway, Databricks provides developers with governed access to frontier and open-source models. For teams that need to customize models, AI Runtime (AIR) brings NVIDIA’s AI software ecosystem and serverless GPUs to enterprise data. Teams can experiment, fine-tune, and evaluate models on AIR, then deploy them for real-time inference through Databricks Model Serving — all within the Databricks Platform, with less infrastructure and governance work to manage.

Today at GTC Berlin, Databricks and NVIDIA are expanding their collaboration to make it easier for enterprises to customize open models.Databricks AIR is now generally available: developers can use NVIDIA NeMo, NGC containers, and new Nemotron cookbooks to train and fine-tune open models on serverless NVIDIA GPUs. Together, these capabilities give teams more flexibility to adapt models to business-specific tasks and put them to work in applications and agents.

## Train and fine-tune faster with AI Runtime

AIR provides serverless NVIDIA GPUs for training and fine-tuning, so developers can run their existing code and containers at scale without managing GPU infrastructure. With support for multi-node distributed training, teams can scale larger workloads across GPU nodes. NVIDIA Quantum InfiniBand provides high-bandwidth, low-latency networking with remote direct memory access (RDMA), while NVIDIA Collective Communications Library (NCCL) handles communication between GPUs. Databricks manages the underlying clusters and networking.

For example, an enterprise building a technical support agent could start with an NVIDIA Nemotron open model and fine-tune it on labeled support tickets usingNVIDIA NeMoon AIR. The team could experiment with different training approaches and use MLflow to track results as they adapt the model to their specific support workflows.

Developers can prepare Lakehouse data and experiment in GPU-powered notebooks or through the AIR CLI, using high-performance data loading and standard environments that include PyTorch and CUDA. They can use distributed training frameworks or bring their own libraries and custom training loops.When experiments are ready for repeatable execution, Lakeflow Jobs can orchestrate training alongside upstream data preparation and downstream evaluation, turning individual runs into repeatable workflows. Declarative Automation Bundles support CI/CD for deploying and updating those workflows.MLflow tracks training experiments and GPU utilization, helping teams compare model results and compute performance. Unity Catalog governs access to training data, and native system tables provide visibility into CPU and GPU usage. Together, these integrations let teams use the data, governance, and operational tools they already rely on in Databricks.

![](/images/posts/7f34f9c54e4e.gif)

![](/images/posts/61c2de45ffc1.gif)

## Accelerate workloads with NVIDIA AI software

Training and fine-tuning deep learning models takes more than GPU compute—teams also need flexibility in their frameworks, libraries, and environments. AIR now supports Docker and private registries, allowing developers to bring custom containerized environments to their GPU workloads.

Developers can use GPU-optimized containers from the NVIDIANGC Catalogwith theDatabricks Artifact Registryto bring NVIDIA software into AIR. Environment caching helps these workloads start quickly, reducing setup overhead as teams iterate on training code and rerun experiments.

![](/images/posts/336ee9b876ca.png)

Developers can also install NVIDIA profiling tools to examine GPU execution and investigate performance bottlenecks. Alongside GPU utilization metrics tracked in MLflow, these tools help teams understand where training workloads spend time and identify opportunities to improve performance. Teams can tune their software and training code while AIR manages the underlying GPU infrastructure.

AIR supports customization beyond LLMs, including a validated fine-tuning workflow forNVIDIA Kumo Anomaly, an open research model for time-series anomaly detection, with MLflow tracking and Unity Catalog checkpoints. This supportsNVIDIA’s Agent Knowledge Foundationvision of building an agent knowledge layer. Pairing Kumo-Anomaly with the Genie Ontology offers a path to context-aware agents that connect unusual patterns in time-series data with business meaning to help inform next steps.

## Customize and serve Nemotron models

With the release of Nemotron 3.5 Lightning and Super VL, Databricks customers can load, experiment with, adapt, and serve these models on Databricks from day one.

AIR supports model customization with NVIDIA NeMo andNeMo Automodel, enabling teams to use NVIDIA’s tools and frameworks on serverless NVIDIA GPUs. In the technical support agent example, this means developers could use these tools to fine-tune Nemotron on historical support tickets, helping the model better understand company-specific products, terminology, and troubleshooting workflows. Training stays connected to enterprise data and workflows in Databricks.

Genie Code can also help developers author and adapt the training script directly in a notebook. Developers can describe the changes they need, ask for help configuring a fine-tuning run, and work through errors as they arise. They can review and refine the suggested code before running it on serverless NVIDIA GPUs.

For fine-tuning, AIR combines optimized data loading, checkpointing, and training with integrated observability and debugging tools. Developers can track experiments and GPU metrics in MLflow and use Genie Code to:

- Debug model code and investigate training errors.
- Identify GPU performance bottlenecks, including memory issues and communication overhead.
- Apply NVIDIA-specific guidance onCUDA,cuDNN, NCCL, and profiling tools.

![](/images/posts/2f78bfbc06b7.gif)

After fine-tuning and evaluation, teams can deploy customized models to production through Databricks Model Serving. In our technical support example, the fine-tuned Nemotron model could power an agent that interprets incoming support requests and generates responses informed by the company's products and troubleshooting workflows. This completes the workflow from model customization on serverless NVIDIA GPUs to real-time inference.

## Get started with Databricks AI Runtime and NVIDIA

To learn more, visit ourweb page,AIR documentation, and explore theNemotron 3.5 SuperVLandNemotron 3.5 Lightningcookbooks to get started with GPU training and fine-tuning on Databricks.

---

> 本文由AI自动翻译，原文链接：[Databricks AI Runtime and NVIDIA make it easier to customize open models with enterprise data](https://www.databricks.com/blog/databricks-ai-runtime-nvidia-train-fine-tune-models)
> 
> 翻译时间：2026-10-22 06:56
