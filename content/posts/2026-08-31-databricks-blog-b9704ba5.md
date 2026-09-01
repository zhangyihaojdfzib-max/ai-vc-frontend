---
title: Autoscaling Lakebase Postgres
title_original: Autoscaling Lakebase Postgres
date: '2026-08-31'
source: Databricks Blog
source_url: https://www.databricks.com/blog/autoscaling-lakebase-postgres
author: ''
summary: '[翻译失败，原文如下]


  - Autoscaling architectural requirement

  - When to adjust capacity up and down

  - How to adjust capacity without stopping PostgreSQL


  Choos...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-01T07:05:21.025223'
---

[翻译失败，原文如下]

- Autoscaling architectural requirement
- When to adjust capacity up and down
- How to adjust capacity without stopping PostgreSQL

Choosing a database instance size before you know the workload is an old building pattern. The process is generally wonky and feels very wasteful of compute, especiallynow that compute is becoming a luxury.

Lakebase Postgres omits the sizing experience altogether thanks to autoscaling. Autoscaling responsiveness comes from in-place VM resizing and an algorithm that tracks CPU, memory, and the database’s working set.

![image9.png](/images/posts/8760b6e75a59.png)

How autoscaling looks like for an arbitrary sample of Lakebase Postgres databases. Note how this is only one hour.

## The architectural requirement

Traditional Postgres runs as a stateful process tied to a machine and its disks; replacing or resizing that machine is a database operation because the machine owns both execution and durable state. But theLakebase Postgres architectureseparates those responsibilities:

- The compute layer runs Postgres and executes queries. It uses RAM and local NVMe for low-latency access, and owns no durable state.
- The storage layer owns durability and history. WAL is replicated by safekeepers running on SSDs, pageservers (also SSDs) reconstruct page versions, and object storage keeps the long-term immutable record.(This blog post focuses on compute, butwe wrote a deep dive on the storage pieceif you are also interested.)

A compute node can therefore start, stop, move, or change size without moving the database underneath it. This is an essential foundation.

![image8.png](/images/posts/450831da2067.png)

Now, when it comes to implementing autoscaling, there are two parts to the story: first, one has to determinewhento adjust capacity up and down, and second,howto do it without stopping Postgres.

Let's cover both in order.

## Part I: The algorithm

### The three autoscaling signals

To deduce when to resize, the Lakebase Postgres autoscaling algorithm tracks three signals, with each signal producing its own target compute size:

1. CPU load:cpuGoalCU
2. Memory use:memGoalCU
3. Compute-cache working set size:lfcGoalCU

The final scaling target is the largest of the three,constrained to the minimum and maximum compute sizes that the user has configured for that database (the autoscaling limits):

### CPU (cpuGoalCU)

CPU is the most straightforward of the three signals. The algorithm keeps a close watch on how hard the processor is working:

- Everyfive seconds, the autoscaler-agent reads theVM’s one-minute CPU load average.
- The CPU goal aims to keep that load at or below 90% of available CPU capacity.
- When the load rises above that target,cpuGoalCUincreases. When sustained load falls, the goal falls with it.

Using a one-minute average filters very short fluctuations while still responding to meaningful changes in demand. The five-second polling interval lets the system update the target as that average moves.

CPU alone, however, is not enough to autoscale Postgres properly. A query waiting for data to arrive over the network can show low CPU use while performing poorly. The algorithm also needs to account for memory and cache pressure.

### Memory (memGoalCU)

Memory has a different failure mode from CPU. If demand briefly exceeds the available CPU, queries become slower; but if Postgres allocates more memory than the VM has, the kernel can terminate processes. The autoscaler therefore needs a much faster signal than CPU for memory exhaustion.

So the system watches memory at two frequencies:

- Every five seconds, the autoscaler-agent readsoverall memory metrics from the VM.
- Every 100 milliseconds, the vm-monitor checksmemory used by Postgres.

The memory goal keeps use below 75% of allocated RAM. That headroom gives the system space to respond to new allocations and leaves memory for the guest operating system and other processes.

The vm-monitor also checks every proposed downscale. Memory cannot be removed if doing so would leave the running processes without enough space.

A bit of history:This polling approach replaced an earlier design based on the cgroupmemory.highevent. Crossingmemory.highcaused Linux to reclaim memory and throttle the processes inside the cgroup. Polling proved more predictable and stable while still giving the system a 100-millisecond view of Postgres memory.

### The compute cache (lfcGoalCU)

The third signal measures whether the workload’s active data fits close to Postgres. The high level story is this:

Lakebase Postgres separates storage and compute; when a page is not available locally, the compute requests it from the pageserver; the returned page is cached for subsequent reads. The compute cache, which we originally called the Local File Cache or (LFC), is a disk-backed cache sized to fit in the kernel page cache. It acts as a resizable extension of Postgres shared buffers. When a compute grows, the vm-monitor expands the cache to use part of the added memory.

For many OLTP workloads, performance changes sharply once the working set fits in local memory. This exposes a blind spot in CPU-only autoscaling: cache misses leave queries waiting on network requests, which reduces CPU use. The system may therefore see low CPU pressure at the exact moment when a larger cache would improve performance. So in Lakebase Postgres, there’s a third autoscaling signal that estimates the Postgres working set directly.

This is the most interesting part of the algorithm, so let’s look at how that estimate works.

### Zooming in: how we estimate the Postgres working set

A workload’s working set is the set of database and index pages it accesses repeatedly over a given period. To exactly count every page for the purpose of autoscaling would require too much memory, so the classic way to solve for this is to rely onHyperLogLog, a probabilistic cardinality estimator that can estimate the number of distinct items in a set using a small, fixed amount of state.

For each Postgres page access, a standard HyperLogLog implementation,

1. Hashes the page identifier.
2. Uses the first bits of the hash to select a register.
3. Counts the leading zeroes in the remaining bits.
4. Updates the selected register if this observation exceeds its previous value.

The distribution of those register values would provide an estimate of how many distinct pages have been observed.

![image10.png](/images/posts/379a80a0fd4c.png)

However, there’s an issue with simply using HyerLogLog for autoscaling: a standard HyperLogLog only grows. Once a register has observed a value, it cannot tell which item produced it or when that item was last seen.

That makes it good at answering, “How many distinct pages has this compute accessed since Postgres started?” But autoscaling needs a different answer, closer to “How many distinct pages belong to the workload running now?”

Without a time boundary, an old import or analytical query would remain in the estimate and keep the compute oversized long after that work ended. So we changed what the HyperLogLog registers store.

### Adding time to HyperLogLog

This is how things actually work in Lakebase Postgres:

Instead of setting a bit when a hash is observed, the estimator stores the current timestamp at that position. To estimate cardinality since timeT, it treats positions updated afterTas set and older positions as unset.

![image6.png](/images/posts/88081d2fd219.png)

Modified HyperLogLog in Lakebase Postgres autoscaling.

This produces an estimate for any window ending at the present, including

- Distinct pages accessed in the last minute
- Distinct pages accessed in the last five minutes
- Distinct pages accessed in the last hour

So, going back to the algorithm, this is how the granularity actually works:every 20 seconds, the autoscaler-agent collectsworking-set estimates for windows from one to 60 minutes.

[翻译失败，原文如下]

But the story does not end here. As surely you’re noticing, this is a wide time window. How do we actually choose it?

### Choosing the working set time window

The problem is this: there is no universal window that describes a database’s current working set. If we pick a short window, the autoscaling engine responds quickly when a workload ends, but it would discard cache too aggressively between bursts. If we pick a long window, the algorithm would protect the cache, but it would also keep memory allocated for work that is no longer running.

The algorithm solves this by looking at how the working set changes overtime. For example: for a steady workload, the estimated number of pages initially grows, and then levels off. Extending the window adds time, but few new pages are added, because the same working set is being accessed repeatedly.

![image5.png](/images/posts/1e86bae9bdf6.png)

Now, consider a heavy workload that ended recently. Short windows contain only the current, lighter workload; but once the window reaches far enough into the past to include the previous workload, the estimate jumps. The algorithm searches for that jump, which marks the end of the current plateau.

![image4.png](/images/posts/0341039ee2a5.png)

In short:

The implementation starts its search after five minutes. This prevents the compute from shrinking immediately during a short pause and then regrowing for the next burst. But if the algorithm finds no sharp increase, it uses the 60-minute estimate - that is the expected result for a stable workload whose working set remains active throughout the hour.

![image1.png](/images/posts/5f8998ea2b9f.png)

### Projecting cache growth

There’s one last piece to it. Measuring the current working set lands slightly too late: suppose a workload begins scanning a new set of pages. If the compute cache grows only after those pages have been read, early pages may already have been evicted to make room for later ones. The cache then has to fetch some of the same data again.

So the algorithm alsoprojects working-set growth forward. It examines how the estimate increases from one duration to the next and allocates enough cache for the working set expected by the next control interval.

Because cache metrics are fetched every 20 seconds, the projection covers only a fraction of a minute. Longer projections would react earlier, but they would also amplify brief spikes and make the compute oscillate.

![image2.png](/images/posts/49c56f2c0f8a.png)

The projected size (finally!) becomeslfcGoalCU. And the algorithmic goal is to fit the working set within the portion of memory available to the compute cache, up to 75% of the compute’s RAM.

## Part II: Resizing the running compute

To recap: the scaling target was,

Those three signals tell the system what size to aim for. Applying that size means changing CPU and memory on a running VM without interrupting Postgres.

Each Postgres instance in Lakebase Postgres runs inside its own virtual machine in a Kubernetes cluster. We use VMs because they provide a strong isolation boundary and, unlike a conventional container allocation, allow CPU and memory to be added to or removed from a running guest.

Four components coordinate each compute resize:

1. The autoscaler-agentruns on every Kubernetes node. It collects metrics from the Postgres VMs on that node, calculates target sizes, and initiates scaling.
2. The vm-monitorruns inside each VM. It watches Postgres memory closely, validates downscaling requests, and resizes the compute cache.
3. A modified Kubernetes schedulermaintains the global view of available resources. Every upscale must be approved by the scheduler before memory is committed.
4. NeonVMapplies the change. It is a custom Kubernetes resource and controller, built with QEMU and KVM, that can add or remove CPU and memory from a running VM. (Disclaimer: Lakebase Postgres architecture started in Neon and the resource/controller name remains the same).

![image3.png](/images/posts/e78ddf6643a2.png)

### Scaling up

As we just saw, scaling up happens when one of the three goals calls for more compute than the VM currently has. An upscale follows this sequence:

1. The autoscaler-agent calculates the new target from the CPU, memory, and working-set goals.
2. The Kubernetes scheduler checks whether the node can satisfy the request without overcommitting memory.
3. Once approved, the autoscaler-agent updates the NeonVM resource.
4. The NeonVM controller adds CPU and memory to the running VM.
5. The vm-monitor expands the compute cache to use the new capacity.

The scheduler is the single source of truth for allocation. It sees both ordinary Kubernetes scheduling and autoscaling requests. Without that coordination, the scheduler could place a new workload on a node at the same moment the autoscaler committed the remaining memory to a Postgres VM.

If a node is too full to grow in place, NeonVM can live-migrate the VM to another node. The VM keeps its IP address, so existing connections stay open. Lakebase Postgres computes have little durable local state to move, so migration is mostly VM memory and runtime state.

### Scaling down

A downscale uses the exact same components, with one extra check inside the VM. The vm-monitor confirms that removing memory will still leave enough for Postgres and the rest of the guest. If it would not, the downscale does not proceed.

Admonition: Scaling down counts as much as scaling up.Some autoscaling systems are quick to add capacity but slow to give it back, leaving databases oversized long after a spike has passed. Lakebase Postgres treats both directions the same way. The goal is to track the workload as closely as possible moment to moment, so you stop paying for capacity as soon as you stop needing it.

## Wrap up

Lakebase Postgres watches the workload as it runs and resizes compute to match in real time. The lakebase architecture makes this possible: since storage is decoupled and durable on its own, compute is free to move without worrying about the data.

The resulting system scales in both directions, on a live database, without dropping connections. Most importantly, it looks past the obvious signal: tracking CPU alone would miss a workload stalled on cache misses, so the algorithm also tracks memory pressure and a time-aware estimate of the working set.

The final loop runs at three timescales:

- 100 milliseconds: the vm-monitor checks Postgres memory to catch rapid allocation
- 5 seconds: the autoscaler-agent reads CPU and overall memory
- 20 seconds: the autoscaler-agent evaluates working-set estimates across windows from one to 60 minutes

That is how a production database can change size more than32,000 times per month.

![image7.png](/images/posts/dc7906613b9a.png)

As compute gets more expensive and more contested, paying for a peak you rarely reach is a building pattern that might not be possible very soon. Autoscaling prepares Postgres for workloads where wasted compute is not an option.

## Run it

Ask your agent to deploy Lakebase Postgres and put it autoscaling to the test.Get started here.

Lakebase Postgres can be used as a standalone database, and you can also integrate it with the rest of the Databricks Data + AI Platform: Unity Catalog governance, lakehouse analytics, notebooks, and AI workflows.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Autoscaling Lakebase Postgres](https://www.databricks.com/blog/autoscaling-lakebase-postgres)
> 
> 翻译时间：2026-09-01 07:05
