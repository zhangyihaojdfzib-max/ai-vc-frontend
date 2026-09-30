---
title: Building a certificate authority for the whole Internet
title_original: Building a certificate authority for the whole Internet
date: '2026-09-29'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/cloudflare-certificate-authority/
author: ''
summary: '[翻译失败，原文如下]


  Twelve years ago, during Birthday Week 2014,we turned on Universal SSLÂ and nearly
  doubled the number of encrypted sites on the web overn...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-30T08:14:42.145511'
---

[翻译失败，原文如下]

Twelve years ago, during Birthday Week 2014,we turned on Universal SSLÂ and nearly doubled the number of encrypted sites on the web overnight, giving free TLS to every site behind Cloudflare, including the ones that never paid us a cent. Encryption stopped being an expensive, time-intensive undertaking and instead became the default.

For Birthday Week this year, we are taking the next step on that path. For more than a decade we have been one of the largest consumers of publicly trusted certificates on the Internet, and have never issued a single one ourselves. That is changing. Cloudflare is announcing our intent to become a public certificate authority (CA).

Today we are announcing the first concrete milestones in that effort: We have applied for inclusion in the Chrome, Apple, Microsoft, and Mozilla root programs, and we have signed a definitive agreement to acquire an established, broadly trusted root from GlobalSign, so that we can offer certificates with the widest possible device reach the day we begin issuing. Weâre also announcing our plans to be one of the first CAsÂ to serve post-quantum certificates, targeting Chromeâs recently announcedQuantum-resistant Root Program.

We are not issuing certificates yet, and it will be a little while before we do. What we are doing is committing to the work in public, sharing the milestones as they land, and telling you exactly what we are building while working with the root programs and other members of the WebPKI community to achieve this.

## Two paths to trust

A brand-new root is not widely useful for years. Even after a root program accepts it, that root has to propagate out into the world's operating systems, browsers, and devices, and it never reaches the large set of devices that have stopped receiving updates, or never received them in the first place. That long tail of older clients is where a great deal of the worldâs Internet traffic originates, and where a correspondingly large set of avoidable breakage lives. We believe that all clients deserve the highest level of security possible, regardless of their manufacturer, operating system, or time since last update.

AcquiringÂ an existing root with a high degree of trust store coverage across a diverse set of clients solves that on day one. The existing GlobalSign root has beenÂ trustedÂ across browsers, operating systems, and devices since 2012, and it reaches older clients that a fresh root never will. The new root that we will be submitting for inclusion in root key programs is built for where the ecosystem is heading, including the programs that are starting to cap how old a trusted root may be. The established root gives us reach across the devices of the past. The new roots give us standing under the policies of the future. We want both to ensure certificates issued by our CA provide the widest set of customer compatibility possible.

## A new source of free certificates

The free-of-charge, automated certificate model now carries most of the encrypted web, and much of it runs through one remarkable operator. Let's Encrypt issues on the order of ten million certificates a day, serves more than 500 million sites, and passed four billion active certificates in 2025. It is one of the best things to happen to the Internet in twenty years, and we say that as one of its largest users.

![](/images/posts/daf658faa860.jpg)

That success comes with some systemic risk: if the dominant free certificate authority had a bad week, much of the web would have no comparable free, automated alternative ready to take the load. At the certificate pack level, we have spent years building exactly this kind of redundancyÂ for our own customers. Every Cloudflare Universal SSL certificate already ships with a backup certificate, wrapped with a separate key and issued from a different authority, ready to deploy automatically if the primary is ever revoked or compromised. A public CA is that same idea, but at the scale of the whole Internet.

To make it easy to adopt, we will be AutomatedÂ Certificate Management Environment (ACME)-first, an open standard protocol that is widely accepted. Automated issuance and renewal through ACME will be the way you get a certificate from us, which means anyone already pointed at any existing free CA can move to us by changing a directory URL, with no new tooling and nothing to re-architect.

## Certificate growth projections are huge

Cloudflare sits in front of more than 20 percent of global Internet request traffic and terminates TLS for millions of domains, relying on millions of certificates per yearÂ to do so. We provision those certificates through multiple CAs, with primary and backup paths so customer services stay up through CA outages and revocation events.

That has taught us not just how the WebPKI ecosystem works, but also that it occasionally fails, from the consuming side, the hard way. We have dealt with rate limits, validation edge cases, revocation latency, chain building, and root distribution lag. We have lived through the CA churn of recent years and felt it through our customers. We know what reliable issuance has to look like from the outside, because our customers' uptime has depended on us being resilient and responsive when an issuer has a bad day.

And ascertificate maximum validity period decreasesÂ over the next few years, agentic activity increases, and PQ certs go mainstream, we expect the raw number of certificates we rely on annually on to continue to grow, quickly â and we are not alone. We want to not just solve this problem for ourselves, but be part of providing this utility to the Internet, and ensure that the certificate supply chain for our customers has even more providers.

## Designing for resilience: transparency and fail small

In taking on this new responsibility of being our own CA, we're committed to making the most reliable and resilient CA possible. We intend to build a certificate authority whose reliability depends not just on avoiding mistakes, but as with the rest of Cloudflareâs products, toÂ âfail smallâÂ and limit the impact of any one issue.

That means instituting processes to design and test recovery before any incident occurs. As an example, we will make renewal automation a condition of issuance. We will only issue to clients that supportACME Renewal Information(ARI), standardized in RFC 9773. Subscribers must maintain automation that polls our renewal endpoint, acts on the renewal windows we publish, and identifies the certificate it is replacing.

We're also learning from what we've observed over the past 16 years. We have seen certificate authorities caught between timely revocation and keeping subscribersâ sites online because too many subscribers could not replace their certificates quickly enough. When certificates need to be retired, whether for a compliance issue or a security incident, we can bring forward renewal windows for the affected certificates, spread replacements across the available time, and track replacement issuance.

This is just one of the many ways we intend to build. We will be transparent with our issuance stack and operations, publish reproducible builds of the software that signs certificates, attest the hardware security modules that hold our keys, and run a public dashboard for issuance health and incidents. Audits are point-in-time and tell you a CA passed, not how it runs on an ordinary Tuesday. We want root programs, researchers, and ordinary site owners to watch how a modern CA actually operates between audits.

![](/images/posts/413f89cee19e.jpg)

## A certificate authority for the post-quantum Internet

We also intend to lead on where certificates are going, not just where they are. We plan to be one of the firstÂ CAs to issue production Merkle Tree Certificates (MTCs), with the first certificates issued in the first quarter of 2027.

[翻译失败，原文如下]

MTCs are a new and far more compact way to deliver publicly trusted certificates, designed for a post-quantum world where traditional certificate chains grow large enough to strain TLS handshakes. We have been championing thestandards-based proposalÂ for MTCs at the IETF, and earlier this year,Chrome named MTCsÂ as the preferred path for post-quantum authentication. Issuing them in production allows us to protect Cloudflare customers as well as the wider Internet against the post-quantum threat, with real volume behind a transition the whole web has to make. Weâve shared much more about MTCs and what this new Web Public Key Infrastructure (PKI) will look likein a blog post on the topic.

We do not expect that transition to be sudden. Much of the Internet will continue to rely on classic certificates and existing WebPKI for many more years. But across that window we expect MTCs to take a steadily growing share of issuance, and that is why we are building one service that does both. By carrying classic certificates and Merkle Tree Certificates under one CA, with one lifecycle and one set of guarantees, customers can adopt at the pace that suits them and help the web make the crossing without a hard cutover. Customers should not have to pick a side of a multi-decade migration, run two systems, or rebuild when the balance shifts.

## As always, Cloudflare will be Customer Zero

In addition to providing certificate packs via Universal SSL for our customers, Cloudflare consumes certificates from many different CAs to run our systems and internal operations. Just like our other products, we will beCustomer ZeroÂ for the new CA and its certificates (both WebPKI and MTC), ensuring that all aspects of the new systems and processes meet our high internal standards, and that our CAâs infrastructure is exercised at Cloudflare scale.

## What happens next

We are working through the application and approval process with each of the core web root key programs. These processes happen in the open, and weâll share more updates as they proceed, through to the first Merkle Tree Certificates in early 2027. If you want to follow this work or be one of the first to use a Cloudflare CA certificate in the future, you canregister for updates. And if youâd like to be part of building out this new capability inside Cloudflare, weârehiring!

As we build out this new capability, we will continue to work closely with the network of partner public CAs we have relied on for many years â 16 in fact! â as we all work together to ensure a trusted and open Internet.

When we launched Universal SSL, the argument was simple: every byte that flows encrypted across the Internet makes it harder to intercept, throttle, or censor, and the open web is something we all build together. A public, redundant, transparent certificate authority is that same argument carried one layer down, to the trust that makes the encrypted web possible in the first place. We have been working toward this for a long time, and we are glad to finally be on the road.

Happy Birthday Week!

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Building a certificate authority for the whole Internet](https://blog.cloudflare.com/cloudflare-certificate-authority/)
> 
> 翻译时间：2026-09-30 08:14
