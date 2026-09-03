---
title: How we could save petabytes of cache storage with Zstandard and Pingora
title_original: How we could save petabytes of cache storage with Zstandard and Pingora
date: '2026-09-01'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/cache-transcoding/
author: ''
summary: '[翻译失败，原文如下]


  Memory costs are increasing dramatically. Both RAM and hard disk drive prices have
  exploded over the past year. At Cloudflare, we run sev...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-03T07:04:09.461506'
---

[翻译失败，原文如下]

Memory costs are increasing dramatically. Both RAM and hard disk drive prices have exploded over the past year. At Cloudflare, we run several massively distributed storage products (including our famous CDN) that rely on making efficient use of the memory we have deployed so we can continue to serve all of our customers.

With this in mind, we prototyped a way to expand effective cache capacity. By encoding eligible assets withZstandardinsidePingora, the architecture trades a minor CPU increase for significant storage and cross-data center bandwidth savings.

We have been prototyping a system called Cache Transcoding, which I built during my internship at Cloudflare as part of the1.1.1.1 Intern Program. When an eligible response enters the cache, we encode it using Zstandard, or zstd, before writing it to disk. We keep that compressed form while the asset lives in the cache and moves between data centers viaTiered Cache, then decode it before serving the response to the client.

In our initial testing, this encoding shrunk eligible assets to â of their original on-disk size on average. The estimated extra CPU cost in our origin-facing proxy was small, but that is the trade. A small increase in CPU gives Cloudflare petabytes of effective cache capacity and reduces the data transferred between our data centers. The encoding cost is paid once when an asset enters the cache. The storage and bandwidth savings continue every single time that asset is reused.

## What is Zstandard?

Zstandard, or zstd, is a lossless compression algorithm developed byYann Collet at Facebookand open sourced in 2016. Lossless means that after compressed data is decoded, every byte is identical to the original. We can change how an asset is represented on disk without changing the asset itself.

Zstd is designed to balance compression ratio with speed. In ourearlier browser compression testing, it compressed data 42% faster thanBrotliwhile producing nearly the same file size, and produced files 11.3% smaller than gzip at a comparable speed. That balance matters because Cache Transcoding would touch a large amount of traffic, so both encoding and decoding need to stay fast.Â

The prototype uses zstd level 3, giving us most of the compression benefit without turning cache fills into a CPU bottleneck.

Cloudflare traditionally stores an asset using the content encoding supplied by its origin. If an origin sends an uncompressed response, we store those uncompressed bytes on disk and transfer them between data centers in the same form. Cache Transcoding adds compression inside the cache itself.

## Not everything is worth compressing

Transcoding does not mean compressing everything. Images, video, and fonts are usually compressed already. In our traffic sample, this media slice represented 21.4% of requests but 63.3% of bytes. Compressing it again would burn CPU for nothing.

Compressible text is different. HTML, JSON, CSS, and JavaScript represented 67.3% of requests and 22.3% of bytes. Within that text slice, approximately 71% arrived uncompressed withContent-Encodingunset and it compresses well.Â

In our controlled test corpus, the eligible assets compressed by roughly 2.8 times.

Measure

Value

Compression ratio

2.834x

Encode cost

4.31 ns per byte, approximately 232 MB/s, paid once per fill

Decode cost

1.56 ns per byte, approximately 641 MB/s, paid on every serve

Encoding is more expensive per byte, but assets are served far more often than they are filled.Â

By changing how assets are represented, existing hardware could store more customer content.

Fewer bytes on disk mean each server can retain more objects. This increases cache density and reduces the likelihood that useful content is evicted because an uncompressed representation consumed more space than necessary.Â

The smaller representation also helps as an asset moves through Tiered Cache because it reduces the data transferred between Cloudflare data centers, making backbone usage more efficient.

## Paying the compression cost once

Compression is never free. Encoding and decoding both use CPU, so the important question is whether the byte savings are worth the processing cost.Â

At zstd level 3 (often the default balance of speed and compression size output), our model kept the extra CPU cost to a few percent under the traffic and reuse assumptions we tested.Â

We initially considered limiting transcoding to popular content, since hot assets are reused more, but it did not help. Decoding happens every time an asset is served, so limiting the feature to only the hottest content reduced the storage saving without cutting CPU by the same amount.Â

The simpler policy performed better. Transcoding all eligible compressible text at or above 4 kibibytes (KiB) captured nearly all of the measured storage benefit, while remaining within the CPU budget.

## How Cache Transcoding works

On a cache miss, our Pingora-based proxyencodes the body using zstdbefore writing it to disk. The cache metadata records that the stored representation is compressed and preserves the original content length. Before the response leaves the proxy, the body isdecoded back to its original identity representation.

On a cache hit, the stored zstd object is read from disk and decoded. With Tiered Cache, the compressed representation is transferred from the upper tier to the lower tier in the compressed form. Decoding only happens on the client-facing hop.

On a full cache miss, the upper tier fetches identity bytes from the origin. Those bytes are encoded once, stored as zstd, and transferred to the lower tier in their compressed form. The lower tier also stores the zstd representation, then decodes it for the request path.

![unnamed (77).png](/images/posts/0283758d30b9.jpg)

If the lower tier misses but the upper tier already has the object, the origin is not involved. The compressed object moves directly between the cache tiers. It remains compressed on the wire and on disk, then is decoded once at the lower tier.

If the lower tier already has the object, no network transfer or encoding is needed. The lower tier reads the zstd bytes from disk, decodes them, and passes the original asset onward.

The storage encoding marker prevents an object from being encoded more than once. A cache layer receiving an object from another tier can see that it is already stored using zstd, and preserve it in that form.

## Why we only transcode certain text

The fastest compression operation is the one we do not need to perform. Cache Transcoding therefore uses a series of eligibility checks to avoid content that is unlikely to benefit.

The prototype only transcodes a200 OKresponse whenContent-Encodingis unset, theContent-Typeis compressible text, and the response has a knownContent-Lengthof at least 4 KiB. Slice subrequests, responses using active upstream compression, range requests, precompressed responses, unknown length bodies, and binary content remain unchanged.

The 4 KiB threshold removed a large number of tiny requests while leaving out only about 1% of the otherwise eligible bytes. Lowering it would add per-object overhead without saving much more storage.

The threshold and zstd level are both parameters rather than permanent limits. We started with zstd level 3 and a 4 KiB minimum because they gave us a conservative way to measure the architecture. With the initial CPU budget understood, we can test whether higher compression levels improve the ratio enough to justify their additional cost.

## Testing over one million requests through the cache

We exercised the prototype against a controlled test zone and correlated each request across request logs, Prometheus metrics, and Jaeger traces.

The correctness campaign covered cache misses, cache hits, single-hop fills, Tiered Cache fills, and more. We varied cache keys to make each request follow a specific path and used traces to confirm where encoding and decoding occurred.

[翻译失败，原文如下]

One performance campaign sent more than a million requests across 10 cache servers. Half of the campaign ran with Tiered Cache disabled and the other half with it enabled. This allowed us to measure local cache behavior separately from transfers between cache tiers.

The two assets were approximately 195 KiB and 272 KiB, and both compressed by roughly 2.8 times. This was deliberately a compressible test corpus. It gave us a clear signal for validating the architecture, but it does not represent every text object on the Internet. A broader corpus is required before treating the measured compression ratio as a fleet-wide constant.

## Compress once, benefit many times

What this experiment showed us is that there are significant efficiencies we can still deploy across our caching service that can benefit all of our customers. What we built for Cache Transcoding shows that the trade is favorable under the conditions we tested. The architecture preserved the content and remained within the CPU budget.

For next steps, we plan to evaluate higher zstd levels, test a broader range of content types and object sizes, tune different parameters from the eligibility criteria and more. Future work can also examine range requests, pre-compressed origin responses, and passing the compressed object directly to downstream components that already support it without decoding.

Throughout my internship, Iâve had the wonderful opportunity to work alongside Cloudflare's engineering teams on the real infrastructure that stores and serves content across our global network. If you want to start your career by helping build a better Internet, explore ourinternship opportunitiesandjob openings.

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[How we could save petabytes of cache storage with Zstandard and Pingora](https://blog.cloudflare.com/cache-transcoding/)
> 
> 翻译时间：2026-09-03 07:04
