---
title: How we raised Databricks cluster rate limits by 7.5×
title_original: How we raised Databricks cluster rate limits by 7.5×
date: '2026-11-18'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-we-raised-databricks-cluster-rate-limits-75
author: ''
summary: '[翻译失败，原文如下]


  - Adaptive concurrency limits track long-running cluster-creation workflows and
  adjust how much work can run as system health changes.

  - ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-19T09:43:54.985415'
---

[翻译失败，原文如下]

- Adaptive concurrency limits track long-running cluster-creation workflows and adjust how much work can run as system health changes.
- Bounded queues and fair scheduling help absorb bursts and share capacity. A fixed API request-rate ceiling remains a customer-facing guardrail.
- Databricks raised default cluster-creation request-rate limits by 7.5× and removed over a hundred customer-specific overrides in the reported scope.

As part of the Compute Platform team at Databricks, we turn cloud infrastructure into clusters ready to run customer workloads. Our day-to-day work includes provisioning virtual machines and coordinating cluster creation across AWS, Azure, and Google Cloud. Our goal is to keep these systems available while letting customers use as much capacity as we can safely provide.

In this post, we'll explore why fixed request-rate limits can fall short for these long-running operations, how adaptive concurrency limits help, and what we learned applying them to cluster creation for Databricks classic compute. You don't need to know any of this to use Databricks, but if you're curious about what happens behind a Databricks Runtime cluster launch, join us for a look inside the kitchen.

Historically, we protected the system with fixed request-rate limits, tested against different load patterns and failure scenarios. We scaled our services primarily by adding resources and adjusting per-customer limits.

The combination of workloads and dependency failures made these limits increasingly difficult to test and tune. Conservative limits turned away customer requests despite spare capacity, yet kept accepting requests when our services or dependencies, such as cloud providers, slowed down. Engineers manually lowered limits to shed load during incidents and raised them again after recovery.

Adaptive concurrency limits account for both unfinished work and changing system health. They let more work start when capacity is available and slow the pace when the system struggles, helping the service make progress with less manual tuning. A fixed API request-rate ceiling remains as a final safety guardrail against exceptionally high incoming traffic.

Think of our compute platform as a kitchen, aiming to serve as many orders as its cooks and equipment can handle. The manager posts a fixed rule: accept at most ten new orders per minute, whatever is happening at the stove.

Even with spare cooking capacity, the rule turns orders away. When an oven breaks, it keeps accepting orders faster than the remaining cooks and equipment can finish them. The manager has to keep rewriting the sign each time.

![Figure 1. The same rule turns away useful work when capacity is available and accepts too much when capacity falls. Someone has to keep adjusting it. The kitchen and its rate limit are illustrative.](/images/posts/41745ab30544.png)

A better kitchen keeps a short queue and limits how many meals are being prepared at once. If an oven breaks, fewer meals start; as capacity returns, more can begin. Orders can wait briefly, but only while there is still time to serve them.

For long-running operations,a fixed request rate is a poor model of capacity.The goal is to let customers run at full throttle when capacity allows, then ease off enough to keep useful work moving during degradation.

## Background

An API call can launch much more work than the handler performs itself. For cluster creation, the handler validates the request, records a work item, and returns. A background workflow coordinates services, updates state, and provisions resources such as cloud virtual machines. These operations complete asynchronously, and their duration depends on the health and capacity of their dependencies. The API call may take milliseconds; the workflow itself may take minutes.

A request-rate limiter at the API entry point caps requests per time window. That is useful for enforcing quotas, preventing abuse, and protecting the resources used to handle API calls.

## The problem

A fixed request-rate limit is easier to tune when available capacity and the work behind each request stay reasonably predictable. Cluster creation makes both difficult: one request may provision a few VMs and another many more, while cloud-provider health changes how long provisioning takes. During a shared slowdown, many workflows take longer at the same time. The same incoming request rate can therefore leave much more work in flight, even as the system’s ability to finish it falls.

![Figure 2. Longer operations increase the work in flight while fewer healthy processors reduce capacity. A fixed request-rate limit does not adjust to either change. The timelines are illustrative.](/images/posts/8190d9dddd27.png)

On the left, arrivals stay fixed at one operation per time unit. Increasing duration from two to six time units triples the work in flight. On the right, processors become slow or unavailable, reducing the capacity available to handle that work.

When a dependency degrades, more calls fail or time out. Long-running workflows retry those calls to recover from temporary faults. Across many active workflows, those retries add pressure to the struggling dependency, causing more failures and yet more retries—aretry storm.

These internal retries come from work already accepted, so the API request-rate limiter does not see them. They can sustain overload even after incoming traffic returns to normal. Limiting active workflows helps contain that pressure and gives unfinished work a chance to drain.

Setting a lower rate does not solve the mismatch. It buys headroom by rejecting more work during healthy periods, and a large enough slowdown can still exhaust that headroom. Raising the rate makes better use of healthy capacity but accepts more work during degradation. One number has to cover both days.

## Terminology

“Rate limiting” is sometimes used broadly to include limits on concurrent work. Here, we distinguish the two mechanisms by what they count.

Either kind of limit can be fixed or adaptive. Our comparison is between fixed request-rate limits and adaptive concurrency limits for protecting long-running work.

## Solution

The kitchen needs to track meals still being prepared and the capacity available to finish them. In Databricks classic compute, the equivalent is the set of cluster-creation workflows still provisioning infrastructure. We give each active workflow a slot and adjust the number of slots as conditions change.

### Track active operations with slots

Consider a CreateCluster request for a cluster with a driver and several worker VMs. Once the request is accepted, its provisioning workflow waits for a slot before it starts. We track whether that work is queued, actively processing, or complete.

If all slots are occupied, the request stays queued. An active workflow keeps its slot while it provisions VMs and waits for dependencies. Once the workflow finishes, its slot becomes available for another cluster launch. A successfully launched cluster can keep running customer workloads for hours without occupying that provisioning slot.

The slot must cover thewhole provisioning operation, including background work after the API returns. Tracking a slot does not require holding a thread.

This controller counts active provisioning workflows. Running clusters, allocated VMs, and vCPUs are separate measures. One workflow can provision many VMs, so one slot does not imply a fixed resource cost.

### Adapt to available capacity

Now suppose a cloud provider takes longer to provision VMs. Active workflows hold their slots longer, so new cluster launches start less often even if the slot limit stays fixed. Customers see longer launch waits as accepted requests queue.

[翻译失败，原文如下]

Adaptive control also changes the slot limit. For cluster creation, useful signals include how long provisioning takes and whether critical thread pools are saturated. When these signals indicate congestion, the controller reduces the number of concurrent provisioning workflows. As conditions recover, it cautiously allows more. Capacity pressure changes when accepted work starts; RPC rate-limit rejections are reserved for exceptionally high incoming request rates.

![Figure 3. A completed provisioning workflow frees a slot for another cluster launch. Health feedback adjusts how many workflows can run at once.](/images/posts/5aecdc381ca1.png)

Reducing the limit prevents new operations from starting until active work falls below it; existing operations still need time to finish. This response time matters when workflows last minutes. Retries also need backoff and a limit on attempts so active workflows do not keep overwhelming a recovering dependency. Concurrency limiting cannot repair an unavailable dependency, but it can limit the extra pressure while that dependency recovers.

## Devil’s in the details

The control loop answers how much work to start. Building a useful service also means deciding who waits, how long they wait, and what we tell them.

### Explain why a request is being throttled

“Too many requests” can hide two very different situations.

In the first, a customer sends its usual traffic, but a shared dependency slows down. Capacity has fallen. Asking the customer to fix its traffic pattern misattributes a service problem.

In the second, a customer submits an unusually large burst while the service remains healthy. Other customers are competing for the same resources. Throttling that burst protects their fair share.

![Figure 4. The same symptom can have different causes. System degradation and a tenant’s excess demand should be visible separately; both can occur together.](/images/posts/2da045730cac.png)

To tell these cases apart, track system health, each tenant’s incoming demand, and the scheduling decision separately. A large number of in-flight operations alone does not prove that a customer sent too much: those operations may be stuck behind a slow dependency. Likewise, a burst need not be throttled for fairness if spare capacity is available and policy permits it.

This distinction belongs in metrics and customer-facing explanations. It tells operators whether to investigate lost capacity or an unusual workload, and tells customers whether changing their behavior will help. Count failures caused by service degradation in service reliability metrics, even when they surface as throttling. For accepted requests that wait in the queue, measure the impact on cluster launch latency.

### Buffer while the request still has time to succeed

For an operation that takes minutes, a short wait is often preferable to an immediate error followed by a retry. A queue can absorb a burst and let the system catch up.

That only works if waiting fits the request’s deadline. Bound the queue’s size and each request’s waiting time, make progress visible, and reject or expire work when it can no longer finish usefully. A queue cannot turn sustained overload into capacity; an unbounded one can turn a brief disruption into hours of delay.

### Keep queueing and cleanup inexpensive

A queued request should be a small record, not a running worker holding scarce resources. A larger backlog should not make every active operation more expensive through repeated scans or competition for threads and connections.

Cleanup needs the same attention. If a large backlog expires together, the service must be able to discard it within a predictable time. Plan for the worst backlog, keep expiration and rejection cheap, and avoid doing expensive setup for work whose deadline has already passed. Otherwise, the queue can keep the service busy long after the original congestion has ended.

### Decide what “fair” means for the product

Suppose a service must delay a hundred requests. Is it better for a hundred customers to each see one slow request, or for one customer to see a hundred slow requests?

The aggregate metric may look the same. The customer experience will not.

A scheduler makes this choice whether we specify it or not. Define which work should go first, what share each tenant should receive under contention, and how lower-priority work avoids waiting forever. Let tenants use otherwise idle capacity where the policy allows it, while preserving fair access when other tenants need their share.

## Current state and future work

We applied these ideas to an integrated load management system for cluster creation on Databricks classic compute. A short API request starts a much longer workflow that coordinates several dependencies, including public clouds, to provision compute resources.

The system combines queued requests, adaptive concurrency limits, and fair scheduling. It uses the work already in flight and system health to decide when queued operations can start.

We kept the API request-rate limit as a final line of defense against exceptionally high incoming traffic. It provides a request-rate boundary we can communicate to customers. Adaptive concurrency limits stay inside the service and govern when accepted work starts. A successful API response does not guarantee an immediate cluster launch or completion within a fixed time.

The initial rollout analysis reported three outcomes:

- 7.5× higher default cluster-creation request-rate limits.
- More than 99.99% fewer cluster-creation rate-limit errors in the reported scope.
- Over a hundred customer-specific rate-limit overrides in scope removed.

Adaptive concurrency control made the 7.5× increase possible by protecting the long-running workflows as conditions changed. Since that increase, few customers have hit the higher cluster-creation request-rate limits, and we have added no new manual overrides for those limits. Customers have more room to scale, with less need for individually tuned exceptions.

Applying this approach to other kinds of long-running work raises further design questions. When operations have very different resource costs, counting each as one slot may be too coarse; weighted slots or separate limits are possible extensions. For workflows with several bottlenecks, another design question is where to apply control so a slow dependency does not hold up unrelated work.

During a cloud-provider slowdown, workflows already provisioning VMs can keep retrying even after new launches slow down. Pair concurrency limits with retry backoff and a limit on attempts to reduce that pressure during recovery.

### What is the difference between request-rate and concurrency limits?

A request-rate limit caps how many requests are accepted per unit time; a concurrency limit caps how many operations are active at once. Each active operation holds a slot until it finishes, including time spent waiting on dependencies.

### Why must a concurrency slot cover the whole cluster-creation workflow?

A CreateCluster workflow holds its slot while provisioning VMs, including time spent waiting on dependencies after the API returns. When provisioning finishes, the slot is released even though the cluster may continue running customer workloads. The controller counts active provisioning workflows; it does not count all running clusters or allocated VMs and vCPUs. Tracking a slot does not require holding a thread.

### How do adaptive concurrency limits respond to system degradation?

When a cloud provider slows down, provisioning workflows hold their slots longer and accepted requests wait longer to launch. The controller also reduces the slot limit when congestion signals, such as provisioning latency or thread pool saturation, indicate pressure. As conditions recover, it cautiously allows more concurrent work.

### Why does Databricks still keep a fixed API request-rate limit?

[翻译失败，原文如下]

The fixed API request-rate limit protects against exceptionally high incoming traffic and provides a request-rate boundary we can communicate to customers. Adaptive concurrency limits work inside the service: capacity pressure queues accepted requests and delays provisioning. A successful API response does not guarantee an immediate cluster launch or completion within a fixed time.

### What results did Databricks report after adopting adaptive concurrency limits?

The initial rollout analysis reported 7.5× higher default cluster-creation request-rate limits, more than 99.99% fewer cluster-creation rate-limit errors in the reported scope, and removal of over a hundred customer-specific rate-limit overrides in scope. Since the increase, few customers have hit the higher limits, and no new manual overrides have been added for those limits.

For the complementary problem of enforcing API quotas at scale, readHigh Performance Ratelimiting at Databricks.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[How we raised Databricks cluster rate limits by 7.5×](https://www.databricks.com/blog/how-we-raised-databricks-cluster-rate-limits-75)
> 
> 翻译时间：2026-11-19 09:43
