---
title: Introducing on-demand CPU and memory profilingÂ with flamegraphs for Workers
  and Durable Objects
title_original: Introducing on-demand CPU and memory profilingÂ with flamegraphs for
  Workers and Durable Objects
date: '2026-10-09'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/workers-on-demand-profiling/
author: ''
summary: '[翻译失败，原文如下]


  Understanding why an application is using more resources than expected, whether
  that is CPU or memory, can be challenging. Logs and aggre...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-10T08:17:42.339924'
---

[翻译失败，原文如下]

Understanding why an application is using more resources than expected, whether that is CPU or memory, can be challenging. Logs and aggregate metrics can only get you so far. Thankfully there is a better way: CPU or memory profiling can show you the exact function where your application is using CPU or allocating memory.

Today we are happy to announce support for CPU and memory profiling of Workers and Durable Objects. From the Workers Observability page, you can now request an on-demand CPU or memory profile of an active Worker, inspect it as an interactive flamegraph, and download the profile file for further analysis.

This method of profiling gives you a useful perspective into what your code is doing and how you can improve it in a real-world setting. Thatâs because the best way to understand your application is to profile it in production.

To try this on one of your Workers, you have a choice of using the CLI or the Cloudflare Dashboard.Â

To use the CLI, make sure youhave the cf package installed, then simply run:

```
cf workers versions profile latest \
Â Â Â Â Â --worker-id "$WORKER_ID_OR_NAME" \
Â Â Â Â Â --duration-ms 5000 \
Â Â Â Â Â --profile-type cpu > worker-cpu.pprof
```

To use the dashboard, head to theCloudflare dashboardand then access the list of Workers on your account by navigating through Build â Compute â Workers & Pages.

Select your Worker and navigate to its Observability tab. You can then use the drop down to select âFlamegraphâ:

![](/images/posts/f92753b74779.jpg)

You can then request both CPU and memory profiles for your Worker on this page. The duration determines how long the profiler should run for on your Worker. You can also select different versions of your Worker to be profiled. Your Worker needs plenty of traffic to be successfully profiled, so make sure you choose a version that has enough traffic.

![](/images/posts/d5e464f6752e.jpg)

Once you click the Capture Profile button, the profiler will run for the duration that you have selected, and you will then see a flamegraph representing the results of the profile being rendered. Each rectangle in the flamegraph represents a function call, with the width representing the amount of CPU time or memory being used by that function. You can click on different functions to focus on and hover to see more details about them:

![](/images/posts/3258c66ba1e3.jpg)

Donât be afraid to capture a couple of profiles, then look for the widest functions to determine what is using the most resources in your Worker. You might also find that the table view is useful to get a quick sense of which functions are most commonly seen in the profile.

If your Worker is implemented in TypeScript, then you shouldmake sure that you have source maps enabled for your project, otherwise your profile may show obfuscated function names that arenât easy to understand.

We have already seen multiple teams at Cloudflare using CPU and memory profiling to identify opportunities for optimizing memory and CPU usage, fixing out-of-memory (OOM) errors, and improving performance.Â Below are some examples of this.

### Using CPU profiling to find optimizations

Letâs look at a real example of how you can use CPU profiling to optimize your Workers. We will look at a CPU profile of the Worker that implements the R2 binding. This Worker receives a lot of traffic and so eliminating even the smallest amount of wasted CPU cycles can have a massive impact on its performance.

We set up the profiler to capture CPU traces, with a duration of 50 seconds. Once we received the rendered profile, we saw this:

![](/images/posts/d7a2d6616c50.jpg)

As mentioned previously, the widest boxes are those which are using up most of the CPU time. Some of them arenât surprising, for exampledecryptBlockÂ is R2 decrypting object data on the way out, andfillResponseÂ is just moving bytes. There werenât any clear ways to optimize these functions.

As some of the boxes are less visible, it can be a good idea to take a look at the table view. Sorting by Samples points us atgenericR2JsonReplacer:

![](/images/posts/ef03aef9134c.jpg)

This function represented over 5% of the CPU time, but what caught our attention was the function calling itself recursively. This looked like wasted work, and it was.

![](/images/posts/670e50b0551a.jpg)

Even though the replacer was being called byJSON.stringifyÂ on every node in the JSON tree, the replacer itself was also walking the tree. This meant that a value nested five levels deep was processed five times. Fixing this enabled us to eliminate the duplicate work and make thegenericR2JsonReplacerÂ function 2.7x faster.

The second candidate in the profile that we looked at was a duplicate call tometrics.

![](/images/posts/80d589fb4409.jpg)

When looking at the code, we saw something close to this:

```
function ship() {
  if (!registry.metrics().length) {
    return;
  }

  // ... more code here ...

  return Response(registry.metrics());
}
```

ThemetricsÂ call was heavy enough that just one call represented 1% of the CPU time in the profile. So storing the result of the first call in a variable and then not calling it again saved us a fair chunk of CPU time.

### How we used Worker profiling internally to fix memory problems

Internally we had a WorkerÂ with a memory problem. P999 memory sat around 133 MB against the 128 MB Worker memory limit. This caused the Worker to be evicted frequentlyÂ with an âExceeded Memoryâ error.

![](/images/posts/74c77cbf1269.jpg)

The image above shows a screenshot of the âErrors by invocation statusâ graph, with the number of âExceeded Memoryâ errors clearly dropping as a result of the fixes identified through profiling.

What was hard to work out was what was causing these errors. The errors and metrics pointed at memory as the source of the problem, but it didnât explain which part of the code caused it.

The team took a heap profile of one of the Workers running in production and opened it withpprof. They saw that their Prometheus code accounted for roughly 66.7% of allocations in the profile. This code was supposed to be disabled, but enough of it was still running that it created a problem. Because it was instrumenting a lot of the code paths in the Worker, it ended up using a lot of its memory, even though the collected data never actually left the Worker.

This code wasnât suspected as a culprit of the memory issues, because it was thought to have been disabled. The profiler showed that the code was only partially disabled, with the memory cost still being paid as if it was fully enabled.

The team removed the Prometheus code path completely. This quickly improved the memory usage of the Worker:

Percentile

Before (MB)

After (MB)

![](/images/posts/4e1b493caf1b.jpg)

This gave the P999 about 10 MB of headroom below the 128 MB limit.

### Following a profiling request to the edge

Workers have supported local profiling through Chrome DevTools for a while, but it has not been possible to start a profiling session on Workers running in production. While profiling a Worker locally is useful, the Worker does not receive the same kinds nor number of requests as one does in production. So how do we profile a Worker or a Durable Object running there?

One of the best features of Workers is that their requests are routed to the data center that is nearest to the requesting client. This reduces latency, but it does mean that Workers must be replicated across different data centers and metals (physical servers). In addition, when a Worker is receiving a lot of requests in a particular data center, it can be replicated in a particular metal multiple times to handle all the traffic.

Durable Objects add another layer of indirection: they can be placed dynamically and can move.

This and a few other features of Workers means that before we can start a profiling session, we need to first answer a few questions:

[翻译失败，原文如下]

- Which version does the developer want to profile?
- In which data center has that version run recently?
- Is the Workerâs isolate still loaded in that data center?
- Does the isolate belong exclusively to the requesting account?
- For a Durable Object, where is the exact live primary actor?

A few of these questions are answered by the client making the profiling request. In most cases this will be the dashboard, but you can also send these requests yourself (or have your coding agent do it for you). An example request might look something like this:

```
curl 'https://api.cloudflare.com/client/v4/accounts/<account_id>/workers/workers/<worker_name>/versions/latest/profile' \
  --data-raw '{"duration_ms":5000,"profile_type":"cpu"}'
```

Notably, this specifies both the script name and version that should be profiled as part of the request URL.

Right now, a new isolate is not started to produce a profile, because the goal is to observe real production execution.Â This means that if your Worker is receiving very little traffic, you may find that it is hard to profile. So itâs important you pick a version of your Worker that is deployed.

### Profiling an isolate without stopping the Worker

A profile is useful only if the application can continue to execute while samples are collected. The Workers Runtime therefore holds the isolate lock only for profiler lifecycle operations. For a CPU profile, the process looks like this:

1. Acquire the isolate and its lock.
2. Create a V8 CPU profiler and begin sampling at a one millisecond interval.
3. Release the lock so normal requests can run.
4. Wait for the requested duration.
5. Reacquire the lock and stop profiling.
6. Release the lock and serialize the result outside the critical section.

Holding the lock through the duration of the profile would prevent JavaScript execution from continuing, which would make the profile useless.

### Durable Objects

Durable ObjectsÂ are different from Workers. Regular Workers are stateless: no one Worker is special or different from the rest, and we pick a running isolate of the requested Worker at random. Durable Objects are stateful, and they have a name. That provides us with the very helpful ability to grab a profile of a specific isolate and a specific object anywhere in the world. When profiling a Durable Object, you can choose by name which object to profile. The runtime will then route the profiling request to the right metal that owns the specific actor and provide a profile of the specific isolate running that object.

### Whatâs next?

On-demand profiling is just the start. It enables you to explore your Workers performance in ways that have not been possible before. But it does have some limitations worth noting:

- You must explicitly start the profiling session. This can mean that you miss important time periods in which your Worker is misbehaving, and where you would like to see a profile to understand what went wrong.
- The memory profiler can only show you allocations that occurred during the profiling window. So if your Worker is allocating a lot during start-up, you will not see it.

In order to resolve this we are already working on something new: continuous profiling. The idea is that we will capture profiling samples for your Worker automatically, so that you can simply explore the profiles in the dashboard. This should make it easier to capture more rare events.

To learn more about profiling in Workers, including the feature presented in this blog post,check out our documentation.

Special thanks to the Workers Control Plane team and the Cloudflare Observability Platform team, in particular William Perron, who helped with dashboard implementation for this project.

- Cloudflare
- Dominik Picheta

---

> 本文由AI自动翻译，原文链接：[Introducing on-demand CPU and memory profilingÂ with flamegraphs for Workers and Durable Objects](https://blog.cloudflare.com/workers-on-demand-profiling/)
> 
> 翻译时间：2026-10-10 08:17
