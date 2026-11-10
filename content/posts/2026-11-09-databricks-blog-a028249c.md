---
title: Accelerate GPU training on Unity Catalog tables with UCDataset
title_original: Accelerate GPU training on Unity Catalog tables with UCDataset
date: '2026-11-09'
source: Databricks Blog
source_url: https://www.databricks.com/blog/accelerate-gpu-training-unity-catalog-tables-ucdataset
author: ''
summary: '[翻译失败，原文如下]


  - Accelerate training timesby 10xand reduce compute costs with UCDataset, a native
  data loader currently in beta that streams data direct...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-10T09:31:45.473501'
---

[翻译失败，原文如下]

- Accelerate training timesby 10xand reduce compute costs with UCDataset, a native data loader currently in beta that streams data directly from Unity Catalog tables to your GPUs
- UCDataset plugs directly into standard PyTorch training loops and automatically handles multi-GPU data sharding without requiring custom code
- By reading training data directly from Unity Catalog, you can ensure governance is applied automatically

GPUs are usually the most expensive part of any training run, and most teams can't keep them busy. The bottleneck usually isn't the model. It's getting data from where it lives to the GPU fast enough - and every second those chips sit waiting, you're burning both time and money.

Today we're releasing theUnity Catalog Dataset (UCDataset)in Beta on AI Runtime. UCDataset is a native PyTorch data loader that streams Unity Catalog tables directly to every GPU in your training job, with no exports, no copies, and no custom loader code.

On simulated production workloads, UCDataset cut training time by10xcompared with reading an exported Parquet copy of the same data.

![image5.gif](/images/posts/5a1ba1523d81.gif)

## The problem: Your GPUs are waiting on your data

Most training data for your models already lives in Unity Catalog tables. Getting it into a distributed training job means picking one of three workarounds, and each one costs you time and money:

- Slow, tedious exports before every run:The most common pattern is to export the table to Parquet (or another shard format) in a volume before every run, then point a dataset at the files. You pay to store a second copy, it goes stale the moment new data lands, and it falls outside Unity Catalog lineage.
- Pulling the whole table into memory doesn’t scale:Reading the table into pandas with toPandas() works for small tables and fails on large ones. It also lands everything on one node, which doesn't help a job that trains on 32 GPUs.
- Streaming through a warehouse is slow:Warehouses weren't natively built to feed GPUs and without optimization will get throttled when many GPUs read at once.

![image4.gif](/images/posts/e091387cc4b7.gif)

Then there's the loader itself. Every GPU and every worker needs its own balanced slice of the data. Teams spend time building this by hand, and a subtle bug can mean the model trains on duplicated or skipped rows without anyone noticing.

The result:expensive GPUs sit idle, training takes longer than it should, and ML engineers maintain data plumbing instead of improving models.

## Introducing UCDataset

UCDataset makes Unity Catalog tables a first-class data source for distributed PyTorch training. You describe what to read (a table, the columns you need, and a row filter) and UCDataset streams training-ready batches to every GPU. Benefits include:

- Built for speed:UCDataset reads the table's files directly from cloud storage, so nothing sits between your data and your GPUs. It splits the matching rows evenly across every GPU and data loader worker.
- Train on the lake, not a copy:Point it at the live table. Filters and deletion vectors apply as the data is read, and the next run picks up newly appended rows automatically.
- Governed end to end:Training jobs read data as the identity that runs them, and Unity Catalog permissions apply exactly as they do everywhere else on Databricks.

![image1.gif](/images/posts/e0b5ce4386da.gif)

## Benchmark: Faster training on a recommendation model workload

We benchmarked UCDataset on a simulated production workload, streaming a 300 GB feature table across 8 NVIDIA H100 GPUs to train a recommendation model and saw on average a10x improvement in training timecompared to loading data directly from Parquet.

How to use it:

Say a team keeps user and item features with a click label stored in amain.recsys.ctr_featurestable. New impressions land on the table every day. They want to train a click-through-rate model on 16 GPUs across two nodes, straight from the table.

1. Describe what to read and create the loader.In train.py, pick the table, keep the labeled training rows, and select only the columns the model needs. The filter is applied as the table's files are read, so rows that don't match never reach your training code. UCDataset already yields whole batches, so wrap it in a standard PyTorch DataLoader with batch_size=None.

2. Train and launch on two nodes.Train with a standard PyTorch DDP loop. UCDataset gives each of the 16 GPUs its own share of the matching rows, so there's no sampler or sharding code to write. Describe the job in workload.yaml, which starts train.py with torchrun on every node, and run it with the AI Runtime CLI:

To train on more GPUs, change num_accelerators in workload.yaml. The training code stays the same. The complete train.py and workload.yaml, with a sample table to try them on, are in the AI Runtime cookbook:Click-through-rate model on a Unity Catalog table.

![image3.png](/images/posts/4ecd4612e5ac.png)

## Get started

Install the package from PyPI. In a notebook, run%pip install databricks-uc-dataset.

UCDataset is available in Beta on AI Runtime. To try it:

- Read the docs:Load Unity Catalog tables into PyTorch with UCDataset
- Start from a working example:cookbook recipe
- Talk to your account team, we would love to hear your feedback.

For unstructured data stored in Unity Catalog volumes, useUCVolumeDatasetto stream files with local caching. While UCDataset handles structured tables, we are also expanding it to support multimodal training via theFILE type- allowing you to train on images, audio, and documents directly from a table. The Beta reads Delta tables in Unity Catalog.

### What is UCDataset?

UCDataset (Unity Catalog Dataset) is a native data loader that streams Unity Catalog tables directly to the GPUs in a training job. It's available in Beta on Databricks AI Runtime. You choose a table, the columns you need, and UCDataset delivers training-ready batches with no export step or custom loader code.

### How does UCDataset speed up GPU training?

UCDataset keeps GPUs busy by reading a table's data files directly from cloud storage, without an exported copy in between. It splits the matching rows evenly across every GPU and data loader worker, so each GPU reads only its own share.

### Do I need to export Unity Catalog tables to Parquet to train on them?

No. UCDataset reads the live table in Unity Catalog, so there's no export step and no second copy to store or keep in sync. It applies your filter and the table's deletion vectors as it reads, and each new run picks up rows appended since the last one.

### Does UCDataset enforce Unity Catalog permissions?

Yes. On AI Runtime, training jobs read data as the identity that runs them, and Unity Catalog permissions on the table apply. Because the job reads the governed table directly, there's no exported copy to secure separately. In the Beta, UCDataset can't read tables that have row filters or column masks.

### Which tables can UCDataset read?

UCDataset reads Delta tables registered in Unity Catalog, including tables with deletion vectors.

Announcements,Unity Catalog,Data Science and MLandAI Research

---

> 本文由AI自动翻译，原文链接：[Accelerate GPU training on Unity Catalog tables with UCDataset](https://www.databricks.com/blog/accelerate-gpu-training-unity-catalog-tables-ucdataset)
> 
> 翻译时间：2026-11-10 09:31
