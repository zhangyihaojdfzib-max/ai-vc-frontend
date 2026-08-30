---
title: Fast, fault-tolerant PyTorch training on AI Runtime
title_original: Fast, fault-tolerant PyTorch training on AI Runtime
date: '2026-08-28'
source: Databricks Blog
source_url: https://www.databricks.com/blog/fast-fault-tolerant-pytorch-training-ai-runtime
author: ''
summary: '[翻译失败，原文如下]


  - At scale, GPU failures are the expected case, not the exception, code must be
  built to survive them.

  - Torch’s distributed asynchronous...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-30T07:44:59.462547'
---

[翻译失败，原文如下]

- At scale, GPU failures are the expected case, not the exception, code must be built to survive them.
- Torch’s distributed asynchronous checkpoint saves make frequent checkpointing nearly free, enabling more frequent checkpointing and cutting recovery cost.
- Model checkpointing by itself is not sufficient, checkpointing the data pipeline prevents silent training-data corruption on resume.

At scale, your training efficiency is determined by a single metric: "goodput", the proportion of time your GPUs spend on productive computation rather than waiting or recovering from failures. Because GPU failures are the expected case at scale, the ability to rapidly and automatically recover from a failure is the only way to maintain high goodput and manage your total GPU spend.

Two subsystems make or break that recovery, yet both are routinely treated as afterthoughts: the data pipeline that feeds your accelerators, and the checkpointing mechanism that snapshots state so a job can resume. Get either one wrong and every failure costs you far more idle GPU time than it should. Even outside of failure scenarios, a data pipeline that can't keep pace with your accelerators will silently starve your GPUs and erode goodput just as surely as a crash would. We'll walk through the mechanisms and trade-offs of both, and how each one shapes your goodput and total GPU spend. See the companionTraining performance and resiliency guidefor code pointers and examples.

For theinfrastructureside of the same problem, how a fleet detects and isolates unhealthy GPUs before they take down a job, see the companion post,How we keep GPUs reliable across Databricks AI.

## Why failures are the expected case at scale

As the number of GPUs in a job grows, the probability that it survives its full duration without an interruption falls rapidly. A useful back-of-the-envelope model from the companion Databricks post assumes each GPU carries roughly a 1% annualized failure rate. Under that assumption,the post notesthat "a 256-GPU job running for 30 days has about a 19% chance of seeing a failure. At 1,024 GPUs, that climbs to 57%." and these are just infrastructure level issues.

To ground that estimate in reality, the608 H100 GPUs delta super computersaw failures every 1.9 hours, this means that for a 32 GPU job, the average time to failure would be 36 hours. The main take away, is that your training job will likely fail at some point and making the correct decisions can make your model resilient and reduce the total time lost when it happens.

## Impact 1: Checkpoint format decides how often you can afford to save

Checkpointing is where resilience is won or lost, and the mechanism you choose has a first-order effect on how frequently you can save. This is the single biggest lever on your goodput: if you checkpoint once a day, then a failure requires rerunning on average 12 hours of duplicate work to bring your back to the state it was in when the failure occurred.

### The monolithic torch.save bottleneck

The first checkpoint most teams write is a simple torch.save on rank 0. Depending on how your model is trained, potentially two issues:

1. For distributed training, it gathers all states to rank 0 and writes a single file.
2. A single process writes the entire checkpoint to sync synchronously. This can be blocked on things like network transfers when saving to remote object stores like Unity Catalog (UC).

![image6.png](/images/posts/07d7f2a59458.png)

This blocking behaviour leaves your GPUs idle, reducing your goodput. But there is a way to reduce the amount of time your GPU spends checkpointing: Torch’s distributed checkpoint API.

### Distributed checkpoint (DCP): every rank writes its own shard

PyTorch's distributed checkpoint inverts the design. Every rank writes its own distinct shard in parallel, alongside a small.metadatafile describing how the shards compose into the full tensors.

![image1.png](/images/posts/18823b8b987a.png)

Saving time decreases roughly as 1/N with the number of ranks and, because the.metadatafile records the global layout, the same checkpoint can reload onto adifferentnumber of GPUs. DCP re-plans which bytes each new rank needs, so recovering onto a reduced-capacity cluster after losing nodes just works.

### DCP is worth it even for plain data-parallel jobs

A common assumption is that DCP is only for sharded models, that a data-parallel (DDP) job, where every rank holds an identical replica of the weights, has nothing to gain. Not so, DCP shards the model state and writes it in parallel across each worker even for DDP training tasks.

It is also the same API you will need the day you move to FSDP or tensor parallelism, so adopting it early means you never rewrite resilience code at the worst possible time.

### Asynchronous saves make frequency nearly free

Even with parallel writes, a synchronous save blocks training until the bytes are durable in storage, for a large checkpoint to a remote volume, tens of seconds of idle accelerator time.async_savesplits the operation: a fast copy to a staging buffer, then a background upload that overlaps continued training.

![image4.png](/images/posts/44f51ca55b3d.png)

The training loop pays only for the staging copy, not the upload. A checkpoint that used to cost tens of seconds of idle time now costs almost nothing, which is exactly what makes the frequent checkpointing in the next section affordable.

On AI Runtime,UCVolumeWriterandUCVolumeReaderimplement DCP against UC volumes, staging I/O through local NVMe and marking a checkpoint complete only once its data has fully landed. See theperformance and resiliency guidefor full details and code examples.

The above excludes the network storage time for torch.save.

## Impact 2: Checkpoint frequency decides your recovery cost

This is where the pieces compound. When a job fails, it loses everything since the last valid checkpoint and must recompute it. So theexpectedwasted work per failure is about half the checkpoint interval and cheap async saves let you make that interval small.

Cutting the interval by a factor of 10 cuts expected time to recover by a factor of 10. Recall the Llama 3 figure of ~8.6 interruptions per day: at that failure rate, checkpointing every 2 hours means you expect to waste 8.6 hours per day on retraining, a goodput of 64%. Checkpointing every 30 minutes, you only spend 2.15 hours, a goodput of 91%.

The recovery must also beautomatic. On restart, the job should find the most recent checkpoint that finished writing, skipping any left half-written by the crash, and resume from it with no human in the loop. DCP makes this reliable: the.metadatafile is written only after all shards land, so its presence is a trustworthy "this save is complete" marker to select on.

![image5.png](/images/posts/6b703d78ff6d.png)

## Impact 3: Dataloading decides whether your GPUs are ever idle

A training job proceeds at the speed of its slowest input. When accelerators wait on the next batch, your goodput is reduced as your GPUs are simply idle. The only way to fix this issue is to ensure that your input pipeline overlaps data preparation for the next step with computation on the current one as seen in the figure below:

![image2.png](/images/posts/c79daafdebf1.png)

We often see customers that shift to overlapping dataloading with compute see a 20–50% decrease in wall-clock time.

### The cost of reading straight from remote storage

On a governed platform, training data lives in remote object storage. On AI Runtime, Unity Catalog (UC) volumes are surfaced as network mounts.

Reading files directly from that mount on every access binds your step time to network latency and re-downloads the same files every epoch. The fix is a dataloader that copies each file to fast local storage on first access, serves subsequent reads from that local cache, and fetches upcoming files in parallel while the GPU computes.

[翻译失败，原文如下]

![image7.png](/images/posts/1c5d0a067fef.png)

With AI Runtime,UCVolumeDatasetandDataLoaderdo exactly this (seethe guidefor code examples) .UCVolumeDatasetstreams files from a UC volume, caching each one to local NVMe on first access, and partitions files across ranks and workers so every accelerator gets a disjoint, non-overlapping slice. OurDataLoaderis a drop-in subclass of the PyTorchDataLoaderwhosedefaults are tuned for this path, so files are fetched and cached concurrently while the GPU computes instead of one at a time on the training thread.

### Example: training an image model off UC files

Consider a straightforward image-classification workload: decode JPEGs from a UC volume, augment, and train a vision model. Let’s look at two ways to do this on the same GPU, model, and batch size: the stock PyTorchDatasetreading from a UC volume versusUCVolumeDatasetplus the DatabricksDataLoaderdefaults.

### You don't have to guess where the time goes

As part of engineeringDataLoader, we’ve ensured that it logs its metrics to MLFlow, making it easy to tell at a glance if your data pipeline is blocking training.

![image8.png](/images/posts/bc97f75faaf7.png)

The metricfetch_secondsmeasures explicitly how long it takes the dataloader to produce a batch and during this time your GPU is sitting idle.

## Impact 4: Forgetting the data pipeline silently corrupts your model

There is one last resilience bug that produces no error message, no crash, and no failed job, just a model that is subtly worse than it should be. It happens when you checkpoint the model, optimizer, and step, butnotthe position of your data pipeline within the dataset.

Consider a job interrupted partway through an epoch. It restores the model correctly and resumes the training loop but the dataloader starts over from the beginning of the dataset.

The resumed job re-trains on examples it already saw this epoch and potentially skips the ones it hadn't reached yet. Across the many restarts that scale makes routine, this silently biases your data distribution. The model still trains; it just trains on the wrong sampling of your data, precisely the kind ofsilentfailure that’s the most costly, because the job completes and nobody sees a problem until the metrics are disappointing.

The fix is to treat data position as part of the checkpoint. Depending on your pipeline, that means tracking a sample or shard offset and skipping ahead on resume, having a custom dataset serialize its own position, or checkpointing at epoch boundaries. All of these rest on one prerequisite:determinism.Shuffling and augmentation draw from random number generators, so those seeds and RNG states must be part of the checkpoint too, otherwise the data order after a restart won't match the order before it, and a saved position points at the wrong samples.

Seed, reproducible order, and resumable data pipeline are three expressions of a single idea. Theguidecovers each strategy with code.

## Summary

Fast, fault-tolerant training comes from a handful of decisions that compound:

1. Use Distributed Checkpoint instead oftorch.save, even for DDP, so saves are parallel and cheap rather than a serial bottleneck.
2. Save asynchronously so checkpoints are nearly free, which lets you saveoften.
3. Recover automatically to the most recent valid checkpoint, so a failure costs minutes of recomputation, not hours.
4. Overlap data loading with computeby caching and prefetching from remote storage so accelerators never idle waiting for input. This is recurring GPU-hours saved on every step.
5. Checkpoint the data pipeline and RNG state, so a resumed job continues on the correct data instead of silently corrupting your model.

The unifying principle: frequent, inexpensive, complete checkpoints turn a hardware failure from a job-ending event into a rounding error, and an overlapped input pipeline keeps the accelerators busy in between. Cheap (async) saves make frequency affordable; complete saves (model, data, and RNG) make recovery correct. With both in place, and a fleet thatdetects and isolates failing hardware, your effective training time approaches the ceiling the hardware allows, regardless of how flaky the cluster underneath it is.

## References

- Meta,The Llama 3 Herd of Models(2024): §3.3.1, training reliability and interruption breakdown on up to 16,384 H100 GPUs.
- Characterizing the Resilience of Hopper H100 and Ampere A100 GPUs(2025): 2.5-year field study of the Delta system; MTBE and failure probability by job size.
- Databricks,How we keep GPUs reliable across Databricks AI: fleet-level GPU health checking and the probabilistic failure model.

Ready to try it? See theTraining performance and resiliency guidein the Databricks AI Runtime docs for the full code, and readHow we keep GPUs reliable across Databricks AIfor the infrastructure side of the story.

---

> 本文由AI自动翻译，原文链接：[Fast, fault-tolerant PyTorch training on AI Runtime](https://www.databricks.com/blog/fast-fault-tolerant-pytorch-training-ai-runtime)
> 
> 翻译时间：2026-08-30 07:44
