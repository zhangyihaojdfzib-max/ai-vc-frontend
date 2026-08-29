---
title: "How we saved 100 terabytes of memory by optimizing 1.1.1.1â\x80\x99s DNS cache"
title_original: "How we saved 100 terabytes of memory by optimizing 1.1.1.1â\x80\x99\
  s DNS cache"
date: '2026-08-27'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/dns-cache-memory-optimization-1111/
author: ''
summary: '[翻译失败，原文如下]


  Big Pineapple, the platform behind1.1.1.1,Gateway DNS,DNS Firewall,AS112, and several
  other Cloudflare DNS services, stores over 250 bill...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-29T08:49:19.950878'
---

[翻译失败，原文如下]

Big Pineapple, the platform behind1.1.1.1,Gateway DNS,DNS Firewall,AS112, and several other Cloudflare DNS services, stores over 250 billion DNS cache entries at any given time. At that scale, wasting a single byte per entry costs more than 250 gigabytes of memory across our fleet.

Five successive changes to how cache entries are stored in memory cut the per-entry footprint by over 50%. Across our fleet, these changes freed up roughly 100 terabytes of memory, equivalent to the amount of RAM in 130 of ourGen 13 servers. The cache also got faster. Insert throughput rose 43% and lookup latency dropped 19%, as fewer allocations and better memory locality meant we did not trade speed for space.

## What we cache

On cold start, Big Pineapple starts out with an empty cache. As DNS queries arrive, the cache fills until it hits its maximum entry count, at which point we evict older or less popular items to make room.

The exact cache size varies by data center. WhenEDNS Client Subnet (ECS)is in use, authoritative servers return different answers depending on the client's network, so we cache multiple versions of the same query. This increases both the number of entries and the memory each one consumes, making the optimizations in this post especially impactful for ECS-heavy locations.

Each item in the cache is a key-value pair. The key identifies what was queried:

```
pub struct CacheKey {
    qname: Name,
    qtype: Rtype,
    authenticated: bool,
    tag: Vec<u8>,
}
```

The value stores the DNS response itself: the answer, authority, and additional record sections, along with metadata like the creation time, a hit counter, and the Time-to-Live (TTL).

```
pub struct CacheEntry {
    timestamp: UnixTimeStamp,
    pub inception: Instant,
    pub ttl: Ttl,
    pub hits: u32,
    pub answers: Vec<Record>,
    pub authority: Vec<Record>,
    pub additional: Vec<Record>,
    pub errors: Vec<ExtendedError>,
    ...
}
```

Both structs have room for improvement. Several fields use types that carry overhead we don't need once the entry is stored.

## Benchmarking memory usage

To measure the impact of each change, we benchmark by filling the cache with randomly generated entries that roughly match the traffic distribution we see in production: 56%Arecords, 25%AAAA, and 19%TXT. Each entry contains between one and four records.

TXTrecords serve as a stand-in for all non-A/AAAArecord types in the benchmark. Their size is randomized between 64 and 224 bytes, close to the average response size we see for variable-length record types.

We track memory usage using acustom allocatorthat wraps RustâsSystemallocatorand records the number and size of allocations per cache entry. Alongside memory, we measure insert throughput and lookup latency across the full cache flow to make sure memory savings donât come at the cost of performance.

These inputs approximate production rather than reproduce it exactly. Process memory also depends on traffic mix, cache occupancy, allocator state, and memory used outside the cache. We therefore measured resident memory across production instances during the rollout.

## The cost of capacity

Vec<T>stores three fields: a pointer to heap-allocated data, the current length, and the total capacity. When you push an item,Vecchecks whether the length exceeds the capacity and reallocates if needed. If thereâs room, it just appends the item and increments the length.

![1.png](/images/posts/c065e76c2d73.jpg)

Once we store a DNS response in the cache, however, we never modify it again. The capacity field serves no purpose, but still costs 8 bytes perVec. The over-allocated heap space is wasted as well, as aVecwith capacity for eight items but only five stored leaves three slots unused on the heap.

![2.png](/images/posts/61e562703d3f.jpg)

UsingBox<[T]>solves both problems. It canât grow after creation, so it doesnât need a capacity field or reserve space for future elements. The same applies toString, which also carries a capacity field.Box<str>drops it.

Each cache entry stores 8VecandStringfields. Replacing them withBox<[T]>andBox<str>saves 8 bytes per field, 64 bytes per entry. It also eliminates the excess heap memory thatVecreserves for future growth. The combined savings add up to over 15 terabytes with over 250 billion cache entries.

## Fewer lists, fewer pointers

Rather than storing the answer, authority, and additional sections in separate lists, we can store a single list with offsets to the start of each section. Since DNS record counts per section fit in au16, we can use au16(2 bytes) for each offset, compared to the 8-byte pointer and 8-byte length that each separateBox<[T]>requires.

![3.png](/images/posts/c7cf7ad6edb9.jpg)

This removes two lists, each with an 8-byte pointer and 8-byte length, and replaces them with two 2-byte offsets, saving 28 bytes per entry.

These savings do not always map directly to the number of bytes removed from individual fields. Rust insertspadding to satisfy alignment requirementsand rounds a structâs size up to a multiple of its alignment. Removing a small field can therefore eliminate additional padding. For example, we also packed several boolean fields into a singlebitflag. This reduced the surrounding padding, causing the struct to shrink by more than the size of the individual booleans.

## Dropping the owner

Each DNS record has an owner, the domain the record belongs to. In many cases, this owner is identical to the domain being queried. For example, a query forexample.com Areturns two records with the same owner:

```
$ dig example.com A

;; ANSWER SECTION:
example.com.        300    IN    A        198.51.100.1
example.com.        300    IN    A        198.51.100.2
```

But when aCNAMEis involved, for example, the record owner can differ from the queried domain:

```
$ dig example.com A

;; ANSWER SECTION:
example.com.        300    IN    CNAME    cdn.example.com.
cdn.example.com.    300    IN    A        198.51.100.1
cdn.example.com.    300    IN    A        198.51.100.2
```

The DNS wire format handles repeated owners using name compression, as defined inRFC 1035. Rather than encoding the same domain twice, subsequent occurrences store a 2-byte pointer to the first occurrence. A domain likewww.example.comcan encode justwwwfollowed by a pointer to whereexample.comalready appeared in the message.

This works well on the wire, but in our cache we store the full owner name alongside each record. Following compression pointers during cache lookups is expensive on the hot path, so we trade memory for speed.

Most records, however, have an owner identical to the queried domain. For those, we can drop the owner entirely and infer it at read time. When the owner differs, such as theArecords behind aCNAME, we store the full name.

```
pub struct Record {
    owner: Option<Box<Name>>,
    class: Class,
    ttl: Ttl,
    rtype: Rtype,
    data: RecordData,
}
```

WhenownerisNone, response construction restores the queried domain from the cache key, avoiding a heap allocation. This means the record is no longer self-contained, but the cache key is already available during every lookup. When the owner differs,Somestores a pointer to the full name on the heap.

![4.png](/images/posts/e9d826914de3.jpg)

In practice, most cached records have an owner identical to the queried domain, so the majority require no heap allocation for the owner field.

## Enum sizing

Rust enums aresum types: each variant can carry different data, but the enum is always the size of its largest variant.

```
pub enum Option<T> {
    Some(T),
    None,
}
```

Optionis eitherSomeand holds a value, orNoneand holds nothing. Both variants take the same amount of memory. The enum stores a tag indicating the active variant, followed by space large enough for the largest variantâs data. When the variant isNone, that space is unused.

For record data, it seems natural to store each DNS record type as an enum variant:

[翻译失败，原文如下]

```
pub enum RecordData {
    A(Ipv4Addr),
    Aaaa(Ipv6Addr),
    Txt(Txt),
    Naptr(Naptr),
    Svcb(Svcb),
    // ...
}
```

But the enum is always as large as its largest variant. In our case, thatâsNAPTRat 136 bytes. It stores three variable-length text fields, a domain name, and two integers. As a result, the full enum, including the variant tag and padding, becomes 144 bytes.

![5.png](/images/posts/7c665ef950f6.jpg)

AnArecord only needs 4 bytes, and anAAAArecord needs 16 bytes.AandAAAAmake up over 80% of our traffic, so most records waste over 120 bytes on padding. Since a single cache entry can store many records this quickly adds up.

### Boxing the variants

To solve this problem, we can box the larger variants of the enum, moving them to a separate heap allocation. The enum then stores an 8-byte pointer to the heap, where the data takes up only the size it actually requires.

```
pub enum RecordData {
    // Small and common variants are stored inline
    A(Ipv4Addr),
    Aaaa(Ipv6Addr),
    // Large variants are stored on the heap
    Txt(Box<Txt>),
    Naptr(Box<Naptr>),
    Svcb(Box<Svcb>),
    // ...
}
```

ForAandAAAArecords, this saves 120 bytes per record. Smaller variant types likeTXTandCNAMEalso benefit. They still occupy the 24-byte enum, but their heap allocation is sized to their actual data rather than padded to 144 bytes.NAPTR, the largest variant, actually pays slightly more. It now adds the cost of a heap pointer and allocation overhead. ButNAPTRrecords are rare in practice, so the tradeoff is worth it.

![6.png](/images/posts/cd020e36e1e0.jpg)

But boxing the larger record variants introduces costs of its own.

### The costs of boxing

Boxing has two costs. The first is allocator overhead. Each boxed variant becomes a separate heap allocation, and allocators round up to the nearest size class. Big Pineapple usesjemalloc, an allocator designed for multithreaded, allocation-heavy workloads. jemalloc groups allocations of similar sizes into fixed-size bins. ATXTrecord requests 32 bytes and fits exactly into a 32-byte bin, wasting nothing, but anMXrecord requests 40 bytes and rounds up to 48, wasting 8 bytes.

The second cost is poor memory locality. Without boxing, the record enum values for a cache entry sit in a single contiguous allocation. With boxing, data for each boxed variant lives in a separate heap region. Reading it requires following a pointer, and when that pointer lands far from the rest of the entry, the CPU has to fetch a new cache line. With millions of cache entries, boxed data ends up scattered across the heap rather than packed together.

![7.png](/images/posts/8cd57ce3a43b.jpg)

Neither cost is catastrophic on its own, but eliminating both, as the next section shows, yields a measurable improvement in both memory usage and lookup latency.

## Storing records in wire format

An obvious next step would be to store the full DNS response in wire format, patching only per-client fields like the message ID on each lookup. But this has drawbacks. DNSSEC records are only included when the client sets theDO (DNSSEC OK)flag. Storing a complete wire format message means either caching two variants, one with DNSSEC and one without, or filtering them out of an already-built message. There is also a cost to parsing the full message on every lookup, which the enum approach we just described avoids by storing already-parsed records.

As a middle ground, we store just the record data as raw bytes, while keeping the rest of the cache entry as structured fields. Instead of a list of parsed enum variants, we store the records as a singleBox<[u8]>containing each record encoded as a 2-byte length prefix followed by its raw bytes.

![8.png](/images/posts/4ee91e8741c6.jpg)

This eliminates the per-variant enum overhead and the boxed heap allocations from the previous optimization. The data also becomes packed contiguously, which improves CPU cache locality. The tradeoff is that records can no longer be randomly indexed. We have to iterate through the buffer sequentially. This adds some complexity for features likeround-robinrotation ofA/AAAArecords, but since record counts per entry are small, the cost is negligible.

When building a DNS response from cached records, most record types can be copied directly from the buffer into the outgoing message. Previously, each parsed record had to be serialized field by field back into DNS wire format. The new layout skips that work forA,AAAA,TXT, and all DNSSEC record types by copying their encoded bytes directly. Only records containing domain names, such asCNAME,NS,MX, andSOA, still require parsing so we can apply DNS name compression. Since records that support direct copying make up the vast majority of our traffic, this change reduces work on the lookup path. Combined with improved memory locality, this reduced cache lookup latency by 5% in our benchmarks.

To build the record data buffer, we write into a reusable scratchspace buffer that persists across cache insertions. Since previous writes have already grown it, the buffer rarely needs to be reallocated. Records vary in size, so we do not know the exact buffer size until they have been serialized. Once the records are in the scratchspace buffer, we allocate aBox<[u8]>andmemcpythe data into it. This replaces the separate allocation for each boxed record with one allocation for all record data. It also avoids the waste from shrinking aVec<u8>, where the allocator may not be able to reclaim the unused tail of the original allocation. In our benchmark, this change alone increased cache insert throughput by 13%.

## The results

The production measurements show how the benchmarked per-entry savings translated to whole-process resident memory. The graph below shows p90, p98, and p99 memory usage across Big Pineapple instances. The first dashed line marks the start of the rollout on May 18, 2026, and the second marks its completion across all services on July 6, 2026. Each release introduced one or more of the optimizations described above, so memory usage dropped in steps rather than all at once.

As each release rolled out, restarted instances began with empty caches and consumed more memory as those caches filled. The stable plateaus therefore represent steady-state memory usage better than the initial dips.

![9.png](/images/posts/564715042ee0.jpg)

Per-instance memory usage dropped across all percentiles. At p99, memory dropped from 9.3 GB to 5.3 GB, a 43% reduction in resident memory. At p90, memory dropped from 6.5 GB to 3.8 GB, a 42% reduction. Instances with fuller caches saw the largest absolute savings.

In our benchmarks, these five optimizations reduced the per-entry memory footprint from 953 bytes to 420 bytes, a 56% reduction. Per-entry allocations dropped from 1.1 KB to 461 bytes. The reductions measured in production are smaller because resident memory includes the cache alongside all other process data. After the rollouts settled, aggregate working-set memory across the fleet was roughly 100 terabytes lower.

Performance also improved. Cache insert throughput increased by 43%, while lookup latency dropped by 19%.

Metric

Before

After

Change

Per-entry net footprint

953 bytes

420 bytes

Per-entry allocations

1.1 KB

461 bytes

Cache insert throughput

625,000 entries/s

893,000 entries/s

Cache lookup latency

828 ns

670 ns

We plan to reinvest the freed memory into increasing cache capacity without increasing our memory usage, which improves cache hit rates and reduces upstream query volume. We're also exploring further optimizations to the cache itself.

To learn more about Big Pineapple, seeHow Rust and Wasm power Cloudflare's 1.1.1.1. If you work on DNS or other large systems, share the optimizations that have worked for you in theCloudflare Communityor on theCloudflare Developers Discord.

- Cloudflare

---

> 本文由AI自动翻译，原文链接：[How we saved 100 terabytes of memory by optimizing 1.1.1.1âs DNS cache](https://blog.cloudflare.com/dns-cache-memory-optimization-1111/)
> 
> 翻译时间：2026-08-29 08:49
