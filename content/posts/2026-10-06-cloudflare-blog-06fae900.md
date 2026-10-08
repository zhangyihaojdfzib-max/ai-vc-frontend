---
title: The keys to the Internet changeÂ on October 11, 2026. Are you ready?
title_original: The keys to the Internet changeÂ on October 11, 2026. Are you ready?
date: '2026-10-06'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/root-ksk-2024-rollover/
author: ''
summary: '[翻译失败，原文如下]


  On October 11, 2026, the DNS root is scheduled to change its key-signing key (KSK)
  for only the second time ever. This key anchors DNSSEC...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-08T08:39:28.625626'
---

[翻译失败，原文如下]

On October 11, 2026, the DNS root is scheduled to change its key-signing key (KSK) for only the second time ever. This key anchors DNSSECâs chain of trust, which lets DNS resolvers authenticate answers using cryptographic signatures. The change is called a KSK rollover. Validating resolvers need to trust the new key before the switch, as otherwise healthy websites could become unreachable.

When wewrote about the first root KSK rollover in 2018, we had seen resolvers lose their learned trust in the new key during software upgrades or moves between machines. Publishing the key well in advance was only part of the job. We also needed to know whether resolvers had retained it, and we couldnât give users a practical way to check.

Most website operators do not need to make any changes for this rollover. If you run a DNSSEC-validating resolver, check that it trusts the new root key, KSK-2024, and follow your software vendorâs instructions to update its trust anchors if the key is missing.Â If you use Cloudflare for your domain's DNS or rely on 1.1.1.1 and Gateway DNS, you do not need to take any action â our systems already trust KSK-2024.

To check ahead of time, visit ourrollover readiness test. It asks the resolver your browser uses whether it trusts the new key. The test usesRFC 8509: A Root Key Trust Anchor Sentinel for DNSSEC, which weâve implemented in 1.1.1.1 ahead of the rollover.

## Where DNSSEC trust begins

A DNS resolver looks up the addresses of websites and other services for your device. DNSSEC lets it check digital signatures on DNS records to verify that they are authentic and have not been changed. The resolver also needs to check that the public keys used to verify those signatures belong to the right domains.

Forcloudflare.com, this follows a chain of trust from the DNS root to.com, then tocloudflare.com. Each parent publishes a Delegation Signer (DS) record containing a fingerprint of its childâs public key. For example,.comÂ publishes the DS record forcloudflare.com, allowing the resolver to check that domainâs key.

That chain needs a starting point. The root, however, has no parent to confirm which keys belong to it. Instead, a resolver checking DNSSEC starts with a root public key, or its fingerprint, that it already trusts. This is called a trust anchor.

![](/images/posts/c23610ce4ffa.jpg)

The rootâs signing keys have two different jobs. The zone-signing key (ZSK) signs the rootâs DNS records, including the DS records for top-level domains such as.com. The key-signing key (KSK) signs the list of public keys published by the root, called the DNSKEY record set. The resolver uses its trusted KSK to verify that list, then uses the ZSK from the list to verify the rootâs other records.

The diagram below shows the arrangement for a typical signed zone. For the root, trust comes from the resolverâs trust anchor rather than a DS record in a parent zone.

![](/images/posts/7e13e6288f50.jpg)

Our posts about the.deÂ and the.alÂ rollover failures showed the consequence of failed DNSSEC checks: websites can be working normally but still be unreachable. The root KSK rollover changes the starting point of those checks. If a resolver does not trust the replacement key, its users may be unable to reach websites underanyÂ top-level domain.

The new key isKSK-2024, identified by key tag38696. It will replace KSK-2017, key tag20326, as the signer of the rootâs DNSKEY set. Validating resolvers need to trust the new key before that switch.

## How resolvers get the new root key

RFC 5011Â lets resolvers learn a new root trust anchor automatically. The root publishes the new KSK alongside the existing one in its DNSKEY set. The existing KSK continues signing that set, so a resolver can use the key it already trusts to verify the records containing the replacement.

Before accepting the new key as a trust anchor, the resolver waits at least 30 days and keeps checking the rootâs signed DNSKEY records. The new key must remain in the records it checks during that period. After the wait, the resolver must successfully verify the records containing the new key again before accepting it.

For this rollover,KSK-2024 has been published in the rootâs DNSKEY set since January 11, 2025. That gave resolvers with automatic trust-anchor updates time to discover and accept it ahead of the scheduled October 11, 2026 signing change. Each resolverâs waiting period starts when it first sees and verifies the new key.

For our resolver, we added KSK-2024 directly to the softwareâs built-in trust anchors in July 2024, alongside KSK-2017. A resolver running the updated software therefore has the new anchor available from startup.

We chose this approach because of our experience during preparations for the first rollover. As described inour 2018 post,Â software upgrades and moves between machines caused some resolvers to lose their learned trust-anchor state. We fixed that by updating the software to include the new anchor by default. Including KSK-2024 in the software likewise avoids depending on each resolver retaining a key it learned automatically.

Even though we added KSK-2024 to our resolverâs built-in trust anchors in July 2024, users of 1.1.1.1 andGateway DNSÂ had no direct way to check whether the resolver answering their queries trusted the new key.

## This time, ask the resolver

RFC 8509Â defines the root key trust anchor sentinel, a way to ask a supporting resolver whether it trusts a particular root key. It uses ordinary DNS queries with specially named domains.

Our readiness test websiteÂ uses this protocol to check for KSK-2024. Two names ask opposite questions:is-ta-38696Â asks whether the key is trusted,not-ta-38696Â asks whether it is not trusted.

![](/images/posts/dff591ca3705.jpg)

Both names have valid DNSSEC-signed address records. A resolver that supports the sentinel first validates those records, then either returns the response directly or replaces the answer withSERVFAIL, depending on whether it trusts the key.

For a validating resolver with sentinel support, the expected results are:

Query

KSK-2024 is trusted

KSK-2024 is not trusted

is-ta-38696

Returns a valid response

ReturnsSERVFAIL

not-ta-38696

For a validating resolver with sentinel support,SERVFAILÂ fornot-ta-38696Â is expected when KSK-2024 is trusted. The resolver deliberately rejects the ânot trustedâ query.

Sentinel labels such asroot-key-sentinel-is-ta-38696can be used under any DNSSEC-signed domain. We usednstest.devÂ for our tests. You can run the two queries directly against 1.1.1.1:

```
$ dig @1.1.1.1 root-key-sentinel-is-ta-38696.dnstest.dev. A +noall +comments +answer

; <<>> DiG 9.10.6 <<>> @1.1.1.1 root-key-sentinel-is-ta-38696.dnstest.dev. A +noall +comments +answer
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 44476
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; ANSWER SECTION:
root-key-sentinel-is-ta-38696.dnstest.dev. 300 IN A 104.18.6.197
root-key-sentinel-is-ta-38696.dnstest.dev. 300 IN A 104.18.7.197

$ dig @1.1.1.1 root-key-sentinel-not-ta-38696.dnstest.dev. A +noall +comments +answer

; <<>> DiG 9.10.6 <<>> @1.1.1.1 root-key-sentinel-not-ta-38696.dnstest.dev. A +noall +comments +answer
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 3285
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
```

[翻译失败，原文如下]

The website also checks that an ordinary signed name resolves, that a deliberately invalid DNSSEC name is rejected, and that the resolver responds to a sentinel query for the current root key. These controls help distinguish a meaningful result from a failed lookup or unsupported protocol. If sentinel support cannot be established, the result is inconclusive; it does not mean the new key is missing.

The browser test checks the resolver your browser uses, which may be affected by Secure DNS or a VPN. ThedigÂ commands above explicitly query 1.1.1.1. Both provide a snapshot of the resolver path answering those requests.

## New key, same algorithm

KSK-2017 and KSK-2024 both use RSA/SHA-256. The rollover replaces the key pair while keeping the same method for creating and verifying signatures.

Inour 2018 post, we wrote that a successful rollover would open the door to discussing an algorithm change. Eight years later, the root still uses RSA.

Replacing the key remains useful. It limits how long a single private key stays in use and exercises the process of distributing new trust anchors, updating resolvers, and retiring old keys. As the first rollover showed, those steps can fail even when the cryptography itself works correctly.

The Internet Assigned Numbers Authority (IANA) plans an idealized three-year rollover interval, balancing regular practice against the work and risk of changing the root key too frequently. The gap since 2018 has been longer.The Internet Corporation for Assigned Names and Numbers (ICANN) attributes the delayÂ to pandemic disruption and upgrades to the hardware that protects the private signing keys.

Changing algorithms means resolvers need both a new trust anchor and software that can verify the new signatures. Regular key rollovers let operators test the trust-anchor updates while keeping the algorithm the same.

## What comes after October

The October 11 switch changes which KSK signs the rootâs DNSKEY set. The rollover continues into 2027, whenICANN plans to revoke KSK-2017, remove it from the root zone, and delete its private key. Stopping a key from signing and removing trust in that key are separate steps.

ICANN has alsoproposed a future root algorithm rollover to ECDSA P-256.ECDSAÂ produces smaller keys and signatures than the RSA algorithm used today. That proposal is separate from this Octoberâs key replacement, and ECDSA is not a post-quantum algorithm.

1.1.1.1 now validates ML-DSA-44 signatures, which are designed to remain secure against attacks using quantum computers. For DNSSECâs whole chain of trust to become post-quantum secure, signed domains, their parent zones, and the root must adopt post-quantum cryptography too. At the root, that means introducing a post-quantum KSK and getting resolvers to trust it.

That will require another root key rollover. The rollovers we perform now let operators test how they distribute replacement trust anchors, check that resolvers have accepted them, and retire the old keys. This Octoberâs rollover keeps RSA, but exercises the trust-anchor updates we will need when the root moves to post-quantum cryptography. The sentinel gives us a way to check whether resolvers followed those updates.

We encourage DNS providers and resolver developers to supportRFC 8509 trust anchor sentinels. If your resolver does not support them, ask your provider or software vendor to add support. Users should be able to check whether their resolver trusts the next root key before a rollover.

For now, the next deadline is October 11. You can check your resolverâs readiness athttps://dnstest.dev/ksk-2024. If you operate a DNSSEC-validating resolver, confirm that it trusts KSK-2024, key tag38696, and followICANNâs guidanceÂ and your software vendorâs instructions if the key is missing.

- Cloudflare

---

> 本文由AI自动翻译，原文链接：[The keys to the Internet changeÂ on October 11, 2026. Are you ready?](https://blog.cloudflare.com/root-ksk-2024-rollover/)
> 
> 翻译时间：2026-10-08 08:39
