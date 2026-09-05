---
title: Compute that takes any shape
title_original: Compute that takes any shape
date: '2026-09-01'
source: Vercel Blog
source_url: https://vercel.com/blog/fluid-compute-takes-any-shape
author: ''
summary: '[翻译失败，原文如下]


  Iteration velocity is now set by how quickly you can provision the computer your
  app or agent needs.


  Workloads differ in how long they r...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-05T06:35:27.947898'
---

[翻译失败，原文如下]

Iteration velocity is now set by how quickly you can provision the computer your app or agent needs.

Workloads differ in how long they run, how much memory they take, and how much of the environment they control. That previously meant a different compute primitive for each job, so product iterations required provisioning infrastructure, not just working on a feature.

We built Vercel so that none of this has to be your problem. The compute layer is a single system with a simple job. Take any workload, assemble the machine it needs, swap configuration on the fly, and absorb burst capacity in real time.

We call thisFluid.

Builds ran on it first, then sandboxes, and now functions. If you've shipped on Vercel, you've been on Fluid without knowing it.

Fluid compute now runs over 15 million builds a day, 25 million sandboxes a week, and a trillion requests a month.

![Diagram of Vercel Fluid. Functions, Sandboxes, and Builds feed into Fluid below. Fluid has two parts: how it runs (Fluid compute, the execution model) and the components (Hive, hardware; Fluid images, environment; Vercel Drives, storage).](/images/posts/b8c0bc58d2a3.jpg)

![Diagram of Vercel Fluid. Functions, Sandboxes, and Builds feed into Fluid below. Fluid has two parts: how it runs (Fluid compute, the execution model) and the components (Hive, hardware; Fluid images, environment; Vercel Drives, storage).](/images/posts/c2a850a8b2be.jpg)

![Diagram of Vercel Fluid. Functions, Sandboxes, and Builds feed into Fluid below. Fluid has two parts: how it runs (Fluid compute, the execution model) and the components (Hive, hardware; Fluid images, environment; Vercel Drives, storage).](/images/posts/add5c9fc6d98.jpg)

![Diagram of Vercel Fluid. Functions, Sandboxes, and Builds feed into Fluid below. Fluid has two parts: how it runs (Fluid compute, the execution model) and the components (Hive, hardware; Fluid images, environment; Vercel Drives, storage).](/images/posts/8dee31cbfc72.jpg)

## Copy link to headingA history of compute

Changing a machine used to mean changing it by hand. You went down to the computer store, bought a hard drive or a stick of RAM, and swapped it in yourself.

Then you could rent bare metal when you needed it, and use it to serve a website, host a database, or send email.

Then the cloud let you request a machine in any configuration you wanted, choose its operating system, use it, and throw it away when you were done.

For agents, even the cloud is too slow. A standard VM can't provision fast enough to keep up with how they work, but this is where Fluid excels.

## Copy link to headingHow a workload runs on Fluid

When a workload comes in, Fluid assembles a machine to fit its shape. If an agent needs to run code, Hive provides an isolated VM, usually one already warm, so it's ready instantly. Your own image boots on top as the environment. A Drive connects, and your files are right where you left them, because storage was never tied to the machine.

Each workload needs something different. A build is compute-bound, so it wants a beefy machine, heavy on CPU and memory. A function is IO-bound, loading specific code to run the instant a request lands, usually on a small VM. A sandbox is flexibility-bound, taking whatever configuration the work calls for with a Drive attached for user data.

Fluid compute is the execution model that all of this leans on. Many requests run on one instance, instead of each spinning up its own. Work starts immediately, and with Active CPU pricing, you pay for CPU only while your code is working, not while it waits on a database or a model.

### Copy link to headingHive

Hiveis the "hardware." We built it to control our own compute. It provisions the isolated machines every workload runs on. It picks the right machine for the job, keeps each one isolated in our multitenant environment, and does it at global scale. Hive gives every product one control-plane API, so our teams build on the same foundation instead of each maintaining their own.

### Copy link to headingFluid images

Fluid imagesis the environment. Until now the OS was fixed. You ran the one the cloud gave you, not the one you chose. Now you push your own image toVercel Container Registry, and run it across sandboxes and functions. In the background, Vercel converts images into a Fluid image in a format we call VHS (Vercel Hive Snapshot), the optimized boot format behind Dockerfile deploys and sandbox custom images, so it can resume rather than boot and a custom machine is ready in milliseconds. It uses the same technology behind Sandbox Snapshots, so optimizations in one product carry to the rest.v0already uses it to build and run its own development environments.

### Copy link to headingVercel Drives

Vercel Drivesis the storage. Your files live in portable, durable storage that travels with the workload instead of being stranded on one machine's disk. Storage that outlives the compute attached to it is what makes the rest of the system work. Drives aren't bound to a single machine, you can swap the compute underneath it and pick up exactly where you left off in the next session. Drives attach to sandboxes today, in private beta, and extend to the rest of Fluid from there.

## Copy link to headingOne system underneath

These are different shapes of the same system, not separate platforms. Because it's one compute layer underneath every product, a gain in boot time, isolation, scheduling, or caching lands across functions, sandboxes, and builds at once, instead of being rebuilt three times. New shapes of compute can be added without rebuilding the foundation. You don't end up with separate primitives that drift apart.

And it's real, not a diagram: Hive provisions a full VM in milliseconds and brings your filesystem state along with it, so you get isolation stronger than an isolate or a container, without paying for it in startup time.

## Copy link to headingThe agent workload

For an agent to move fast, it needs the right machine, and it needs it immediately. The faster the machine assembles, the faster the agent works.

An agent runs untrusted code, so the machine needs a secure boundary. It brings its own tools, so the machine needs its own environment. And because an agent spins up and tears down constantly, its state has to outlive the compute. Fluid assembles that machine immediately, and then a fresh one for the next task.

For years, the machine was a fixed thing, and you fit your work to it.

In Fluid you describe the work, and the machine forms around it.

## Contributors

Kevin Sundstrom

---

> 本文由AI自动翻译，原文链接：[Compute that takes any shape](https://vercel.com/blog/fluid-compute-takes-any-shape)
> 
> 翻译时间：2026-09-05 06:35
