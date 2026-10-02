---
title: IP Functions are Generally Available, bringing high-performance network analytics
  to the Lakehouse
title_original: IP Functions are Generally Available, bringing high-performance network
  analytics to the Lakehouse
date: '2026-10-01'
source: Databricks Blog
source_url: https://www.databricks.com/blog/ip-functions-are-generally-available-bringing-high-performance-network-analytics-lakehouse
author: ''
summary: '[翻译失败，原文如下]


  - Databricks now includes a family of native, built-in IP functions for parsing,
  validating, canonicalizing, and joining IPv4 and IPv6 ad...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-02T08:10:48.202058'
---

[翻译失败，原文如下]

- Databricks now includes a family of native, built-in IP functions for parsing, validating, canonicalizing, and joining IPv4 and IPv6 addresses and CIDR blocks - no UDFs, no regex, no brittle bitwise math.
- The first-class SQL, PySpark, and Scala functions are optimized in Photon so that demanding network workloads run in seconds instead of minutes.In head-to-head benchmarks, Databricks completed IP CIDR joins up to 3.1x faster and up to 6.4x cheaper than another leading cloud data warehouse.
- Generally available today on Databricks Runtime 18 LTS or later.

## IP data is warehousing data

Every firewall, load balancer, VPN, CDN edge, DNS resolver, Kubernetes cluster, and application server all emit a stream of records keyed on one thing:an IP address. For a large enterprise, these streams collectively generate tens of billions of events a day and are the foundation of some of the most valuable analytics an organization runs, including threat detection, fraud investigation, and network observability. Historically, the industry treated these network observability use cases as specialized use cases that required a specialized stack, leading to silos, fragmented governance, and lock-in.

That changes now. Today,IP Functionsare available Generally Available. With this launch, IP address analytics becomes a first-class, high-performance SQL workload on the lakehouse, letting security teams parse, enrich, and analyze their highest-volume IP data alongside the rest of their analytics, under one governance model.

## Why network analytics used to be painful

In the past, IP addresses were deceptively hard to handle in SQL. An IPv4 address looks like a string but behaves like a 32-bit integer; IPv6 is 128 bits. A CIDR block like 10.0.0.0/8 isn't a value at all - it's a range of 16 million addresses. Asking "is this IP inside that subnet?" is a range containment problem hiding behind a piece of text.

Without native support, teams were forced into one of a few brittle patterns - each of which trades away correctness, performance, or maintainability:

Common workaround

What it costs you

Regex parsingto pull octets out of strings

Slow, fragile, silently wrong on malformed or IPv6 input

Manual bitwise mathto convert addresses to integers

Unreadable SQL that only the author understands; breaks on the v4/v6 boundary

Custom UDFsfor CIDR containment

Kills vectorization and query-optimizer awareness; a black box the planner can't push down or broadcast

Pre-expanding CIDRs to rangesin external pipelines

A separate pipeline to maintain

Dropping IPv6 entirely

Whole classes of modern traffic silently excluded from analysis

The result was a lose-lose. SQL-only analysts were locked out of basic IP filtering because it required procedural code. Data engineers burned cycles maintaining UDF libraries and CIDR-expansion jobs. Above all, the critical workloads, like enriching billions of events against threat-intelligence and geo-IP tables, would run forover an hourwhen the business needed answers in minutes. At a petabyte scale, that gap is the difference between catching an intrusion in progress and reading about it in the post-mortem.

## Native IP functions, built into SQL

Databricks introduces a complete set of built-inIP functionsthat make network data a first-class citizen of the lakehouse. They handleIPv4 and IPv6 uniformly, accept both human-readableSTRINGand compactBINARYrepresentations, understand CIDR notation natively, and are implemented in the engine itself so the optimizer and Photon can accelerate them.

The example below enriches raw network flow logs with threat intelligence and then identifies suspicious source networks that are scanning large numbers of destinations and ports. What previously required custom parsing logic and bespoke IP libraries can now be expressed directly in SQL using native IP and CIDR operations.

No UDF. No regex. No integer gymnastics. It reads like the question the analyst is actually asking.

### The functions

The GA release ships the full toolkit needed to parse, normalize, inspect, and join IP data:

Containment and joins

- ip_cidr_contains(cidr, needle)- tests whether an IP addressoranother CIDR block falls within a CIDR block. This is the single predicate behind CIDR block joins and high-volume filtering, and the function the entire optimization effort centers on.

Parsing and canonicalization

- ip_host(ip)- normalizes an IPv4 or IPv6 address to its standard form (e.g., collapses 2001:0db8:0000::1 to 2001:db8::1).
- ip_cidr(cidr)- produces the canonical representation of a CIDR block.

Inspecting a CIDR

- ip_network(cidr)/ip_network_first(cidr)- returns the first (network) address of a CIDR block.
- ip_network_last(cidr)- returns the last address of a CIDR block.
- ip_prefix_length(cidr)- returns the prefix length (the number after the /).
- ip_version(ip_or_cidr)- returns 4 or 6 so mixed-protocol addresses can be branched on without special-casing

Representation conversion - for performance

- ip_as_binary(ip_or_cidr)- converts an address or CIDR to its canonical, compact binary form (4 bytes for IPv4, 16 for IPv6). Storing and joining onBINARYskips repeated parsing and shrinks storage.
- ip_as_string(ip_or_cidr)- converts a binary representation back to human-readable text for reporting.

Safe variants for messy data

- try_ip_host(ip),try_ip_cidr(cidr),try_ip_as_binary(ip_or_cidr),try_ip_as_string(ip_or_cidr)- identical to their counterparts, but returnNULLinstead of erroring on invalid input. Essential when ingesting raw logs where a fraction of records are always malformed, so one bad row never fails a billion-row job.

These native functions compose naturally with the rest of SQL, they're available to every SQL user, with no setup, and the optimizer understands them, which is what makes the performance story possible.

Rearc, which helps enterprises develop GenAI, Data, and Cloud platforms, is leveraging the IP Functions to build network observability use cases for large scale customers.

## Built for petabyte scale: seconds, not minutes

A common IP analytics challenge is finding a single address or sub-CIDR within a much larger range, which is critical for quickly detecting threats, investigating fraud, and monitoring network activity at scale. This use case represents a range join, which engines have historically struggled with because standard join algorithms rely on equality. Databricks’ engine supports an optimized range join for IP addresses viaip_cidr_contains.

Databricks’sip_cidr_containsoutperforms traditional warehouses on price and speed across all scales of probe (i.e. “needle”) and block (i.e. “haystack”) tables. We benchmarkedip_cidr_containsacross five representative scenarios:

Scenario

Size of probe table(i.e. number of needles)

Size of CIDR block table(i.e. number of haystacks)

A team's daily access log joined on a curated denylist

10M IPs

1K blocks

A large customer's daily activity joined on mid-level threat intel

1B IPs

100K blocks

Correlating a quarter’s worth of firewall and VPN logs against the set of known cloud-provider ranges

10B IPs

1M blocks

A large enterprise matching all authentication events against a consolidated identity-risk table

5M blocks

A week of traffic joined on larger scale threat intel

10M blocks

The results show that Databricks’ IP Functions’ performance is much stronger than competitors, even at increasing scales. Once the number of probes exceeds 10B IP addresses and the number of blocks goes beyond 1M CIDRs, query speed begins to flatline.

![Relative cost per run charts](/images/posts/78564e73307b.png)

The cost gap is just as stark. Even as workloads scale, Databricks remains2xto as much as6.4x cheaper.

![Relative cost per run charts](/images/posts/e4d6c86edd80.png)

Stanby is quickly saw the value of running their network monitoring use cases directly on the lakehouse, rather than on external systems:

[翻译失败，原文如下]

Ultimately, these highly performant IP Functions enable an entire class of network workloads to be built directly on the lakehouse.

## What this unlocks

With fast, native IP functions, entire workloads move onto the lakehouse that previously couldn't live there:

- CIDR enrichment joins at scale- tag every event with GeoIP, ASN, threat-intelligence, or ownership metadata in seconds, so downstream detection and investigation queries run against enriched data.
- High-volume, real-time filtering- "show me every connection from this suspicious /16 in the last 24 hours" becomes an interactive query instead of a batch job.
- Unified IPv4 and IPv6 analytics- mixed-protocol tables work out of the box, so modern traffic is analyzed, not dropped.
- CIDR-in-CIDR matching- check whether an entire subnet falls within another, at the same performance as IP-in-CIDR, for network-topology and policy analysis.
- First class SQL accessibility- analysts get IP filtering and joins with plain SQL, no procedural code or UDF libraries required.

With these functions natively supported on the lakehouse, these network workloads share one governed copy of the data with the rest of the enterprise - no separate specialized system to license, secure, and keep in sync.

## Get started today

Native IP functions are available nowGenerally Availableon Databricks Runtime LTS or later.

See theIP functions reference documentationfor the full function list and signatures. The network firehose has always been one of your biggest datasets - now it can finally live where the rest of your analytics do.

---

> 本文由AI自动翻译，原文链接：[IP Functions are Generally Available, bringing high-performance network analytics to the Lakehouse](https://www.databricks.com/blog/ip-functions-are-generally-available-bringing-high-performance-network-analytics-lakehouse)
> 
> 翻译时间：2026-10-02 08:10
