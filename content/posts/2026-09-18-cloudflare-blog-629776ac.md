---
title: Saving another 100TB of RAM with math (and Rust)
title_original: Saving another 100TB of RAM with math (and Rust)
date: '2026-09-18'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/saving-100-tb-of-ram-with-math/
author: ''
summary: "[翻译失败，原文如下]\n\nCloudflare operates at a scale so big that even after working\
  \ here for years, it doesnâ\x80\x99t seem real. We have thousands of servers all\
  \ ov..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-19T06:55:32.439016'
---

[翻译失败，原文如下]

Cloudflare operates at a scale so big that even after working here for years, it doesnât seem real. We have thousands of servers all over the world with petabytes of RAM and millions of CPU cores, and all of it is pushed to the max. As vast as those resources feel, they are still finite, and when you need every service to run on every node, it doesnât leave room for wasted space.

At this scale, small improvements are greatly magnified, so even1%-at-a-timeimprovements are worth celebrating. And some tweaks add up to a lot more: in this post, weâll look at how small changes to a single algorithm reduced the memory footprint of one of our Pingora-based services significantly. That allowed us to reclaim more than 100TB of RAM globally, on top of the100TB of memory the DNS team was able to shed last month.

## Waste not

Maintaining equitable resource sharing between teams is not easy, especially in large organizations. One of the ways Cloudflare ensures the balance is kept is through the tireless efforts of the wonderful Performance team.Â

This story starts with a ticket filed byIvanwho found:Excessive memory usage frompingora-ketamain Pingora Backend Router. The finding was that our internal load-balancing service, Pingora Backend Router (yes, PBR), was using significantly more memory than expected â specifically in structures associated with pingora-ketama, which is our open-source library for handling consistent hashing.

In order to talk about how we addressed this seeming overuse of memory, we need to talk about what consistent hashing even is, why we are using it in PBR, and how it became so memory hungry. Along the way, weâll learn some Rust and even a little math.

## Consistent hashing

Consistent hashing is a widely used method for distributing tasks across multiple servers in a way that does not require large changes when servers are added or removed. Internally we use it to route cacheable requests to servers by URL. This allows us to keep only one copy of a file stored per data center and gives a stable way to find the location of each file. We havementionedthissystembefore, but letâs take the time to walk through how and why this algorithm is used and how it works.

The key concept of consistent hashing is that while hash functions can accept any kind of input, their output is limited to a single unsigned integer (32, 64, or 128-bit integers depending on which hash function). This allows us to relate tasks and servers to each other in aconsistentway. Most discussions of consistent hashing have you think of that output space as a continuous, circular ring that wraps around from its max value to zero. This depiction makes for some nice visualizations, but it can also make the simple concept of integer ranges seem more complicated than it needs to be. For our discussion, weâll represent the 32-bit output of our hash function as a number line.

Now, letâs say we have a set of servers, A, B, & C, and a set of tasks t-z. We can map each onto the number line based on the hash of their representative values, so something like IP addresses for servers and cache keys for tasks.

![BLOG-3083 3.png](/images/posts/a8d736f28655.jpg)

Assigning tasks to servers is now just a matter of finding the first server to the left of each task. We can represent this visually by coloring in the region of hashes that will be associated with each server. Notice that the range covered by server C wraps around to the beginning, hence the idea that hashes exist in a ring.

![BLOG-3083 4.png](/images/posts/52ebd2424bc0.jpg)

And thatâs it. At a base level, consistent hashing is this simple â but it doesnât take long to see that there is room for improvement. Notice that the range covered by server A in our example is significantly larger than that of either B or C. This is a problem because the fraction of the requests a server handles is going to be proportional to the size of its range on the number line. Ideally we would like to guarantee each server will have an equal size, but because hashes are essentially random numbers, we have to talk about the size of the regions in terms ofstatistics. ð¨

## Math and consequences

First: donât panic. I promiseI'm not about to lie to youand that we will stay safely within the bounds of a day-one probability lesson. When we talk about statistical distributions, there are two big factors that help us quantify uncertainty in helpful ways:expected valueandstandard deviation. In (over-)simplified terms, expected value gives us a point where measurements based on a distribution will be centered, and standard deviation tells how close to that central point most measurements are likely to be.

For consistent hashing, we can calculate these factors for the fractional size of the range associated with one of N servers. (Details on where this formula comes from later).

In terms of concrete numbers, letâs say we have 100 servers. The formulas above give:

That tells us that we can expect that the range each server handles will be centered around 0.99% of the total and most of the lengths to fall within 1% of what's expected. Thissoundsgood until we realize that thatâs 0.99% of thetotal length. We need to scale the standard deviation by the expected value to see how big the error is as a fraction of the target size. This value is called thecoefficient of variation.

## What if we add hashes?

The simplicity of consistent hashing is a double-edged sword. Itâs easy to understand and implement because everything is turned into easily-relatable hashes on the same numberline, but any improvements to the system will also need to be relatable to that numberline. That means the solution to any consistent hashing problem can only bemore hashes. Itâs less like agolden hammer(a tool with which all problems look like nails) and more like a goldennailin that it turns all tools into hammers.

To solve the problem of imbalanced workloads, we can add multiple hashes to represent each server instead of just one. Weâll get to the math behind this momentarily, but it should make some intuitive sense that while each individual range has a large standard deviation, adding a bunch together should make their total size even out. If we take our three-server example from the above diagrams and add two more hashes at random for each server, we see that it helps even out each serverâs workload.Â

![BLOG-3083 5.png](/images/posts/3bb60594f6c7.jpg)

This is an admittedly contrived example. The random nature of the system means thereâs no guarantee how much improvement you will get from adding 2 additional hashes per server, but it should make some intuitive sense that combining more of these hash segments together produces a more even distribution. Each segment in the sum has a chance of balancing another. Maybe one is too short; maybe one is too long. This is essentially what thelaw of large numberstells us should happenâ¦ The obvious problem is it only works for large numbers. In NGINX, the baseline number of hashes per server ishardcoded to 160, and Pingora uses thesame value as the default. Iâll spare you the math for now, but if we go back to our 100-server example, if we use 160 points per server instead of just one, the coefficient of variation (which we can think of like an error margin) drops from about 99% to about 8%, a significant improvement.

## What if we add more hashes?

[翻译失败，原文如下]

We saw above that increasing the number of hashes per server by a constant amount allows us to improve how evenly workloads are distributed per server, but what if wedonâtwant to distribute the work evenly? In Cloudflareâs case, we have some servers that have more storage space than others, so it would be better to have the number of requests allotted to a server be proportional to its disk space. One way to accomplish this is with the ketama algorithm. The naming is a little funny because the algorithm is named after thelibrary where it was first implemented, and the library was named â¦ well you cangoogle itð¶âð«ï¸.

For us, since we want workload to be scaled based on storage, we can use the disk space as the weight, which is exactly what the Pingora team has been doing for years. Elsewhere in the company where workloads are more compute-intensive, weights might be based on CPU or GPU count.

## What if we add evenmorehashes???

The last problem we need to address is that so far we are working under the assumption that any server can handle any request, but in practice that is not the case. Things like compliance requirements or enabled caching features mean only a subset of servers can handle any particular request. Unfortunately, unlike before, we canât solve this problem by adding more hashes to the same ring. We have to add completelynewrings, and not only that â everycombinationof features potentially needs its own specific ring!

## Storage improvements

One big improvement came fromZaidoon, who had an insight about ourstructfor storing hashes in PBR. That struct looks like this:

```
struct Point {
    hash: u32,
    index: u32,
}

```

```
struct PointV2 {
    hash: u32,
    index: u16,
}

```

Unfortunately, Rust doesnât make it that easy. Changing the size of the index as we did above does nothing to reduce the memory footprint. This is because Rust has alignment rules that require the size of a structure in memory to be a multiple of its largest (or âmost alignedâ) field. In this case, the hash is the largest with four bytes, so when stored in memory, a Point is required to have size $mN \times 4m$, so the minimum size is eight bytes.

Luckily there are well-known ways around this. You (meaning me) might be tempted to use#[repr(packed)], but that is controversial forgood reasons. A safer but less readable solution is to store the hash and index as raw byte array and access them with getters. Both methodscompile to the same thing.

```
struct Point([u8; 6]);

impl Point {
   fn hash(&self) -> u32 {
	u32::from_ne_bytes(self.0[0..4].try_into().unwrap())
   }

   fn index(&self) -> u16 {
	u16::from_ne_bytes(self.0[4..6].try_into().unwrap())
   }
}

```

This simple (if wordy) change reduces the amount of memory used for consistent hashing by a whopping25%! In order to do better than that, weâll need to jump back into the math, so everybody hang on to something; this is the home stretch.

## What if we tried fewer hashes?

You may have noticed that we gave the formula for the standard deviation for the case where there is only one hash per server. Deriving the formula for the case where there are $m k m$ hashes per server is not easy, and most sources only give you an approximation or an asymptotic limit, but not us. I might not be a statistician, but I grew up with a calculus teacher (Hi, Mom!), and I wanted to know theactualvalue. The full derivation is in asupplemental post, but here is the payoff.

To see how increasing the hash count improves the accuracy, we need to look again at the coefficient of variation.

![BLOG-3083 6.png](/images/posts/cfca9647da70.jpg)

The predictions from my beautiful math only work if we think about hashes in acontinuousring, but in practice we use 32-bit numbers for the hashes that have the potential for collisions, and the probability of collisions goes up surprisingly quickly as the number of hashes increases (see thebirthday paradox). Collisions matter because in the ideal case, every hash contributes to the volume and distribution of requests handled by the associated server, but a collision means some contributions are randomly dropped, introducing unpredictable error. If we compare some simulated results with 32-bit hashes with the predicted error rate, we can see that for data centers with 2048 servers, the error rate increases: between 10,000 and 100,000 hashes per server.

![BLOG-3083 7.png](/images/posts/710caff4ff28.jpg)

Ultimately, even though this realization feels kind of bad, itâs great news for our plan to reclaim some RAM! Now that we have some math to back it up, we determined that we could decrease the number of hashes we were generating for each server by90%without incurring any appreciable error, so that is what we set out to do.

## Migrating without melting origins

There was one more problem: changing the hash ring changes where some cacheable requests go. Even if the new ring is better, switching the whole network at once would effectively invalidate almost all cached content. It would turn a memory optimization into an apocalyptic increase in origin traffic.

So we did not make this a single global flip. For a while, PBR carried both versions of the cacheable load balancer in memory: the old ketama ring and the new smaller one. Each request used our normal migration framework to decide which ring should select the backend. That meant the rollout decision was stable per request hash, and it also gave us a clean rollback path. If anything looked wrong, we could send new requests back through the old ring without redeploying PBR.

We then rolled the migration out in layers. We started with small validation locations, moved through progressively larger groups of data centers, and only then continued toward the rest of the world.Â

The important part was that we controlled two dimensions independently: how much traffic used the new ring, and where that traffic was allowed to move. A plain global percentage rollout would have spread cache churn everywhere at once. Data-center-scoped rollout kept the blast radius small and made it much easier to tell whether a change was actually safe.

During the migration, we watched backend-selection traces, ring-version counters, PBR connection errors, process memory, startup time, cache behavior, and origin traffic. Once the migration reached 100%, we removed the temporary old-ring path, and voila!

![BLOG-3083 8.png](/images/posts/b28060171a16.jpg)

The chart above shows the comparison of the memory used by PBR the week of the change compared with data from a few weeks before, as well as the result of subtracting one from the other. The sharp drop is the day where the version of PBR with the large (now unused) hash rings was decommissioned forever. Looking at the difference, we get the satisfying result that our changes dropped the used memory by 100TB!

![BLOG-3083 9.png](/images/posts/4f09f6c2a2fd.jpg)

## Try it yourself

All the changes we talked about in this post are available now in thepingora-ketama cratein the form of a (for now) unadvertised cargo feature. Thev2ring has the compacted storage format, a faster sorting method, and the ability to scale the base number of hashes per node. Our focus in making these changes had to be on stability and control, so thev1ring is identical to what pingora ketama has always used, and the library makes it possible to run both simultaneously and decide on a request-by-request basis which to use and when.Â

Beyond trying our literal consistent hashing changes, I would like you to take away from this some inspiration to dig into your own systems to see what âsimpleâ or âobviousâ decisions are hiding potential wins, if youâre willing to get into the numbers. You might not be able to solve all your problems withRust, but math is universal.

## Related tags

Follow on Social Media

- Cloudflare
- Kevin Guthrie
- Mariia Iurchenko

[翻译失败，原文如下]

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Saving another 100TB of RAM with math (and Rust)](https://blog.cloudflare.com/saving-100-tb-of-ram-with-math/)
> 
> 翻译时间：2026-09-19 06:55
