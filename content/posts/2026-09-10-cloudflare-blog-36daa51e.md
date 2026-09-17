---
title: 1.1.1.1 now supports post-quantum DNSSEC, all 2,420 bytes of it
title_original: 1.1.1.1 now supports post-quantum DNSSEC, all 2,420 bytes of it
date: '2026-09-10'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/post-quantum-dnssec-1111/
author: ''
summary: '[翻译失败，原文如下]


  1.1.1.1 now validatesDNSSECsignatures made withML-DSA-44, a post-quantum signature
  algorithm standardized by theNational Institute of Sta...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-17T07:00:17.321752'
---

[翻译失败，原文如下]

1.1.1.1 now validatesDNSSECsignatures made withML-DSA-44, a post-quantum signature algorithm standardized by theNational Institute of Standards and Technology (NIST). This is a first step toward preparing DNSSEC for a future in which todayâs signature algorithms are no longer secure.

Cloudflare plans to achievefull post-quantum security by 2029. Much of the work so far has focused on TLS, but public-key cryptography is used in many other systems, including DNSSEC.

While we beganexperimenting with post-quantum key agreement in TLS in 2019and enabled support for all customers in 2022, post-quantum signatures have not yet received comparable testing in DNSSEC. There is also some urgency. Widespread client adoption of post-quantum TLS took years, partly because larger messages exposed assumptions and bugs in existing network software. That experience showed why early large-scale testing matters. We cannot wait until quantum computers become an immediate threat.

The problem is that post-quantum signatures are large. Each ML-DSA-44 signature is 2,420 bytes, exceeding common DNS-over-UDPlimits before the response includes anything else. At the same time, zones will need to publish conventional signatures for older resolvers for years, creating a potential downgrade path if not validated correctly. The challenge is carrying these much larger responses reliably, without allowing compatibility with older resolvers to weaken protection for newer ones.

With ML-DSA-44 validation enabled, 1.1.1.1 lets us test both challenges at Internet scale: carrying larger DNS responses and preventing fallback to conventional signatures.

## Why post-quantum DNSSEC matters

DNS responses are not authenticated by default. An attacker who can forge a response may be able to redirect users to an address of their choosing. DNSSEC prevents this by signing DNS records. A validating resolver such as 1.1.1.1 follows a chain of signed records from the DNS root to the requested domain, checking that the answer is authentic and has not been modified.

DNSSEC supports multiple signature algorithms, but nearly all of those used today are vulnerable to future quantum computers.RSA and ECDSArely on mathematical problems that are believed to be infeasible for conventional computers to solve at deployed key sizes. We are preparing for the possibility that in 2030 a sufficiently powerful quantum computer could be built that breaks these keys. An attacker could then recover the corresponding private key and create forged signatures that validators would accept. The attack path is shown below.

![3500_2.png](/images/posts/a3dac55529a0.jpg)

Quantum computers capable of carrying out these attacks do not exist today. DNSSEC provides authenticity rather than confidentiality, so it is not subject to âharvest now, decrypt laterâ attacks. The reason to begin now is that changing DNSSEC requires coordination across authoritative servers, registries, registrars, and validating resolvers. The migration must eventually reach the top of the DNS hierarchy, where a compromised key has the greatest impact. An attacker who recovers a root zone signing key using a quantum computer could forge a validation path to any zone below it: âbreak once, forge everywhereâ. ML-DSA-44 gives that migration a standardized starting point, and supporting it in 1.1.1.1 lets us, and the DNS ecosystem at large, gain operational experience.

## Why replacing the algorithm is difficult

DNSSEC was designed to support new algorithms. In principle, supporting ML-DSA-44 means publishing its public key and teaching validators to verify its signatures. In practice, two properties make the transition difficult: the signatures are large, and the old algorithm cannot always be removed safely.

### A 2,420-byte signature changes the packet

DNSSEC algorithms commonly used today produce relatively small signatures.ECDSA P-256, for example, produces a 64-byte signature. An ML-DSA-44 signature is 2,420 bytes, almost 38 times larger.

Algorithm

Number

Public key size

Signature size

RSA-2048/SHA-256

260 bytes

256 bytes

ECDSA P-256

64 bytes

ML-DSA-44

1,312 bytes

2,420 bytes

That difference matters because many of the systems that send, carry, and receive DNS messages are sensitive to message size. DNS originallyrestricted messages sent over UDP to 512 bytes.EDNS(0)later allowed a resolver to advertise the largest UDP response it is willing to accept from a nameserver. Many DNS implementations use aconservative UDP payload limit of 1,232 bytes, chosen to fit within IPv6âsminimum MTU (maximum transmission unit) of 1,280 bytes. More recently,RFC 9715recommended a maximum of 1,400 bytes for DNS over UDP. An ML-DSA-44 signature exceeds that budget on its own, before accounting for the signed RRset, domain names, DNS headers, and other DNSSEC records. Sending such a response as fragmented UDP isunreliable and should be avoided. Instead, the authoritative server should return a truncated response, prompting the resolver to retry using another transport protocol, usually TCP.

The effect is most visible in DNSKEY responses, which contain the keys a resolver needs to validate the zone. An ML-DSA-44 public key is 1,312 bytes, and the DNSKEY RRset also carries a 2,420-byte signature. ML-DSA-44 cannot fully replace conventional signing algorithms until it is widely supported across the DNS ecosystem, a process likely to take years. Until then, DNSKEY responses may contain both conventional and post-quantum keys and signatures to remain compatible with older validators. Key rollovers can add still more keys, making these responses larger again.

Handling DNS over transports other than UDP is not itself unusual.Cloudflare Radarshows that around 85% of queries to 1.1.1.1 arrive over UDP. The platform behind 1.1.1.1,Big Pineapple, also powers other DNS services, includingGateway DNS. Across all services handled by Big Pineapple, around 60% of queries arrive over UDP. The remaining 40% use transports such as TCP, DNS over TLS (DoT), and DNS over HTTPS (DoH).

Those figures describe how queries reach Cloudflareâs resolver services, not how 1.1.1.1 communicates with authoritative servers. Large ML-DSA-44 responses can still cause additional TCP retries on that side, but handling DNS over transports other than UDP is already a normal part of operating 1.1.1.1 at scale.

### Supporting two algorithms introduces a downgrade risk

Replacing an existing DNSSEC algorithm cannot happen all at once. If a zone publishes only ML-DSA-44, resolvers that do not support it cannot validate the zone. The practical migration path is therefore to publish conventional and post-quantum keys and signatures together.

That preserves compatibility, but it does not provide post-quantum security by itself.RFC 6840specifies that âvalidators SHOULD accept any single valid path.â This rule lets validators use whichever published algorithm they support.

Once a conventional algorithm such as ECDSA is no longer secure, however, the same behavior creates a downgrade path. An attacker could forge an ECDSA-only answer that a resolver accepts despite supporting ML-DSA-44, as illustrated below.

Preventing this downgrade requires an authenticated signal that a zone should be validated with ML-DSA-44. 1.1.1.1 uses DS records published by the parent zone for this purpose. If the authenticated DS RRset contains a record for a supported post-quantum algorithm, the signal is present.

1.1.1.1 then deliberately applies a morerestrictivelocal validation policy. It requires at least one valid post-quantum validation path; a conventional path is no longer sufficient. If no ML-DSA-44 path validates, validation fails. This is not (yet) normal DNSSEC validation behavior, butRFC 4035 allows local resolver policyto determine whether additional signatures must be checked and how conflicting results are handled.

[翻译失败，原文如下]

Conventional signatures can remain available for older resolvers without allowing post-quantum-capable resolvers to fall back to them. The downgrade signal is only post-quantum secure if ML-DSA-44 deployment and downgrade protection extend from the trust anchor through every delegation. Rotating the zone key more frequently does not solve the problem: an attacker can target a vulnerable key anywhere higher in the chain and forge every delegation below it.

## The road to post-quantum DNSSEC

Adding a post-quantum algorithm to DNSSEC requires more than standardizing the cryptography. It needs implementations in cryptographic libraries, an IANA-assigned DNSSEC algorithm number, support from authoritative servers and validating resolvers, and adoption throughout the DNS delegation chain. ML-DSA-44 now has the initial prerequisites for deployment. NIST has standardized it, and common cryptographic libraries implement it. Its use in DNSSEC is described in theML-DSA for DNSSEC Internet-Draft, and IANA recently assigned itDNSSEC algorithm number 18.

Adding ML-DSA-44 validation to resolvers is one of the first deployment steps, but it does not create a complete post-quantum chain of trust. Authoritative servers must sign zones with ML-DSA-44, registrars must accept and submit the corresponding DS records, and registries must publish them in parent zones.

This adoption must extend through every parent zone to the DNS root. The root must adopt ML-DSA-44, and its post-quantum key must become a trust anchor for validating resolvers. Any level without post-quantum protection remains a downgrade point.

There is little value in signing a zone with ML-DSA-44 if no resolver validates its signatures. Enabling ML-DSA-44 validation by default on 1.1.1.1 is therefore an important early step. It lets us measure the operational cost of signature verification, additional bandwidth, and increased TCP use between resolvers and authoritative servers.

As with previous migrations, we will also test real-world deployability using background probes on a small fraction ofCloudflare Challenge Pages. These probes will test whether clients can resolve and reach an ML-DSA-44-signed test domain across real networks. We invite other DNS operators and implementers to begin testing ML-DSA-44 at scale. Together, these measurements will show what adjustments are needed as adoption grows.

## What this means for you

If you use 1.1.1.1, you do not need to change anything. ML-DSA-44 validation happens automatically when a zone publishes the necessary DNSSEC records, while existing DNSSEC zones continue to validate as before.

This work covers the resolver side of DNS. Our next step is adding ML-DSA-44 signing support toCloudflare Authoritative DNSand corresponding DS record support toCloudflare Registrar, which will be available to all customers for free. That will let us test the complete path, from generating signatures and publishing DNSKEY records to transporting and validating them through 1.1.1.1.

Want to see post-quantum DNSSEC in actionâ¦ all 2,420 bytes of it? Query ourdnstest.devzone using 1.1.1.1:

```
$ dig @1.1.1.1 valid.mldsa44.dnstest.dev +dnssec

;; WARNING: truncated reply from 1.1.1.1@53(UDP), retrying over TCP

;; ->>HEADER<<- opcode: QUERY; status: NOERROR; id: 17546
;; Flags: qr rd ra ad; QUERY: 1; ANSWER: 3; AUTHORITY: 0; ADDITIONAL: 1

;; EDNS PSEUDOSECTION:
;; Version: 0; flags: do; UDP size: 1232 B; ext-rcode: NOERROR

;; QUESTION SECTION:
;; valid.mldsa44.dnstest.dev.		IN	A

;; ANSWER SECTION:
valid.mldsa44.dnstest.dev.	0	IN	A	188.114.97.0
valid.mldsa44.dnstest.dev.	0	IN	A	188.114.96.0
valid.mldsa44.dnstest.dev.	0	IN	RRSIG	A 18 4 0 20260910114537 20260909104537 23176 valid.mldsa44.dnstest.dev. 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

;; Received 2563 B
;; Time 2026-09-09 13:45:37 CEST
;; From 1.1.1.1@53(TCP) in 20.7 ms
```

You can also useIs your DNS resolver post-quantum ready?to test your current resolver. The community is tracking ML-DSA-44 software supporton GitHub.

## Related tags

Follow on Social Media

- Cloudflare
- Bas Westerbaan

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[1.1.1.1 now supports post-quantum DNSSEC, all 2,420 bytes of it](https://blog.cloudflare.com/post-quantum-dnssec-1111/)
> 
> 翻译时间：2026-09-17 07:00
