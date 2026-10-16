---
title: How our AI Research team uses AI Runtime
title_original: How our AI Research team uses AI Runtime
date: '2026-10-15'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-our-ai-research-team-uses-ai-runtime
author: ''
summary: '[翻译失败，原文如下]


  - Databricks AI Research uses AI Runtime to train and fine-tune models at scale,
  from small experiments to workloads spanning hundreds of...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:41:09.614059'
---

[翻译失败，原文如下]

- Databricks AI Research uses AI Runtime to train and fine-tune models at scale, from small experiments to workloads spanning hundreds of GPUs.
- Built-in GPU reliability, fast job launches, and integrations with MLflow and Unity Catalog help researchers experiment faster.
- Agent-driven research has increased training jobs 8x, with AI Runtime supporting faster, automated experimentation.

At Databricks, we continuously develop and evaluate new AI research techniques to make our products more intelligent, efficient, and useful for customers.

Our research spans products like Genie, Smart Routing, and AI Functions. Recently, we've published how we madesearch 3x faster, developednew techniques for offline reinforcement learning, and pushed thefrontier of complex document extraction.

To build great AI models and manage hundreds of parallel research workstreams, we need infrastructure that can keep pace. That's why we use Databricks AI Runtime (AIR).

In this post, we'll share how AIR helps us experiment quickly, scale to large training workloads, and adapt to agent-led training, along with what we've learned about managing GPU resources across research projects.

## The challenge: many experiments, very different compute needs

Our research team develops models that powerDatabricks AI Functions, includingai_parse_documentandai_extract. For example, Databricks AI Functionsdeliver state-of-the-art document parsing quality, backed by models trained to understand enterprise documents. Achieving that quality requires extensive research across different architectures, datasets, training techniques, and hyperparameters, spanning tens of thousands of training and evaluation runs.

We use supervised fine-tuning (SFT), offline reinforcement learning (RL), and online RL to train models ranging from a few billion parameters to nearly a trillion. Depending on the workload, we use NVIDIA H100 or B300 GPUs, both available through AIR. Our largest training runs can require hundreds of GPUs working together over days or weeks, with high-bandwidth networking to keep training efficient.

Supporting these workloads creates three challenges:

1. Resiliency for long-running training jobs.Training can require thousands of GPU hours. A single node or RDMA network failure can leave hundreds of GPUs idle and force us to restart from an earlier checkpoint, losing hours of progress. For reinforcement learningprojects like KARL, reliable infrastructure is essential.
2. Fast experimentation and prototyping.Improving AI Functions means testing thousands of approaches, from different models and training techniques to data recipes. We need to launch experiments quickly without repeatedly provisioning infrastructure or rebuilding environments.
3. GPU fleet management.We balance multiple research projects with different compute requirements, priorities, and deadlines, while remaining flexible enough to respond to new research techniques or open-source models.

## Adopting AI Runtime to solve these challenges

Our research team has been customer zero of AI Runtime since the product's inception last year. We use AIR to develop, train, and test models that power Databricks AI products, relying on its GPU infrastructure and integration with our existing tools.

Built-in GPU resiliency

AIR performspreflight checks on assigned GPU nodesto ensure they're healthy and can communicate effectively before training starts. It also monitors node health during execution, detecting issues such as NCCL communication failures, thermal or power throttling, and GPU driver problems. If a node becomes unhealthy and causes a job to fail, AIR detects the issue and cordons off the affected node so subsequent jobs aren't scheduled on the same problematic infrastructure.

This is especially important for projects like KARL, where complex rollout generation and post-training of models with more than 100 billion parameters can require thousands of GPU hours. Rather than repeatedly troubleshooting infrastructure failures, we can focus on improving our models.

Fast iteration with the AIR CLI and custom containers

Research requires us to change model configurations, training approaches, and code frequently. With the AIR CLI, we can launch workloads programmatically, specify the GPUs we need, and let AIR handle provisioning and scheduling, including high-bandwidth networking for distributed training across clouds.

We also rely on custom Docker containers for local development. AIR lets us use those same images for training, ensuring compatibility without recreating our environments. We can upload our codebase, execute custom code in those containers, and use Databricks Artifact Registry to register and share images across experiments. AIR's investments in launch latency and container optimization help us start training jobs in seconds, shortening feedback loops as we test new ideas.

MLflow and logging for experiment tracking

We use MLflow to track our research experiments. AIR automatically creates and manages MLflow experiments for our training jobs, eliminating separate configuration.

We can monitor job status, stream and inspect training logs, and retrieve metrics to understand how experiments are progressing. This also gives our AI agents access to the information they need to evaluate results and determine what to try next.

Seamless, governed access to research data

All of our research data is stored in Unity Catalog. Through Unity Catalog FUSE mounting, AIR lets us access that data as though it were part of a local filesystem, even when working across different Databricks workspaces.

This keeps our data accessible, tracked, shareable, and governed without changing how our training code interacts with files. Combined with MLflow and our Docker-based environments, it gives us a consistent workflow from local development to distributed training.

Managing GPU capacity across research projects

Our workloads have very different resource needs. A debugging experiment may require only a few GPUs, while a large training run might need hundreds for days or weeks. Different projects also have competing timelines and priorities.

AIR's workload prioritization and preemption capabilities help us allocate resources across projects, prioritize time-sensitive experiments, and use excess capacity when it's available. For example, spare capacity can support additional exploratory experiments over a weekend without disrupting higher-priority work. Our goal is to keep GPU resources available for the experiments that matter, without requiring researchers to manually coordinate infrastructure.

## Scaling on AIR with agent-led training

Popularized by Andrej Karpathy,autoresearchis changing how we develop AI models. Instead of researchers manually launching and evaluating every experiment, we're increasingly using agents to propose changes, run experiments, evaluate results, and determine what to try next.

![](/images/posts/c9a9dffe8b5f.png)

This shift has dramatically increased our experimentation volume. Across our AI Functions research workloads, the number of training jobs has grown by8x.

![](/images/posts/deb6cc2bb4b2.png)

As agents take on more of the research process, our infrastructure needs to keep up. A slow startup or confusing configuration error might be manageable when a researcher launches a handful of experiments. When agents launch hundreds, those same issues quickly become bottlenecks.

Agent-driven research requires fast job launches, programmatic interfaces, clear and actionable errors, reliable execution, and accessible training results.

Our autoresearch workflow follows a continuous cycle:

[翻译失败，原文如下]

1. Propose:Agents identify potential improvements to models or training approaches.
2. Launch trials:They submit multiple experiments to AIR in parallel.
3. Learn:They evaluate training metrics to identify what improves performance.
4. Update the plan:They use the results to refine their approach and launch new experiments.

![](/images/posts/57078d63f3f4.png)

AIR is particularly well suited to this workflow because agents can interact with it programmatically and benefit from its fast job launches, built-in reliability, and ability to scale. Through the Databricks CLI anddatabricks-air-skills, our agents can launch concurrent workloads, monitor job status, retrieve MLflow metrics, and iterate based on the results.

This lets us run more experiments while our researchers focus on developing new ideas and improving model quality. As we move further toward agent-driven research, AIR gives us the infrastructure to support both larger models and a faster pace of experimentation.

## Get started today

Our experience using AI Runtime has shown us how much reliable, flexible GPU infrastructure matters for research. From large-scale training and governed data access to agent-driven experimentation, AIR lets us spend less time managing infrastructure and more time developing better models.

If you're training or fine-tuning your own models, check out theAI Runtime documentationto get started.

AI Runtime has also powered our research across areas likefaster search,reinforcement learning, anddocument understanding. Explore more of our work atDatabricks AI Research,

---

> 本文由AI自动翻译，原文链接：[How our AI Research team uses AI Runtime](https://www.databricks.com/blog/how-our-ai-research-team-uses-ai-runtime)
> 
> 翻译时间：2026-10-16 06:41
