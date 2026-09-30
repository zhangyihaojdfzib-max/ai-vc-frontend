---
title: Using AI to chart a course for our post-quantum migration
title_original: Using AI to chart a course for our post-quantum migration
date: '2026-09-29'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/ai-driven-cryptography-discovery/
author: ''
summary: '[翻译失败，原文如下]


  As laboratories around the world race to build out acryptographically relevant quantum
  computer, we at Cloudflare are racingÂ towards a20...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-30T08:14:42.935065'
---

[翻译失败，原文如下]

As laboratories around the world race to build out acryptographically relevant quantum computer, we at Cloudflare are racingÂ towards a2029 target deadline for full post-quantum readiness. While weâve already transitioned many of ourproductsÂ to post-quantum encryption, we still have work to do to supportpost-quantum authenticationÂ and achieve full post-quantum readiness across our platform.

Weâre taking a maximalist stance (âPQ everything!â), because as an infrastructure provider to the world, we want to give our customers the peace of mind that using Cloudflare ensures that their traffic is future-proofed against quantum adversaries.

But how does one accomplish such a massive migration at an organization of our size and scale? After all, cryptographyÂ is the base layer for almost all of the worldâs digital systems, including the software services and the networking protocols that power our platform.

To drive our PQ migration, we have three key goals.

First, we want to helpÂ our product and engineering teams understand how cryptography is being used and how they should be upgrading it. This should cover both the upgrades to post-quantum encryption and to post-quantum authentication. Many of our products have already been upgraded topost-quantum encryptionÂ overTLSÂ 1.3, but we still want to cover the long tail of TLS connections, as well as upgrade any other uses of public-key encryption. Meanwhile, itâs stillearlyÂdaysÂ for our deployment of post-quantum authentication.

Next, we want to provide progress metrics for the migration. These might include per-repository and per-product counts of the use of classical and post-quantum cryptography.

Finally, we want to surface prerequisites early. If our products or platform rely on protocols that donât yet have a PQ migration plan (because PQ variants of the system have not yet been considered, because PQ standards do not exist or lack consensus, or because software libraries or other key ecosystem components do not yet have PQ support), then we need to know now. That way we can work with the relevant stakeholders, standards bodies and ecosystems to help drive their PQ migration plans, so that we can meet our own 2029 PQ migration timeline.

This post is the story of how weâre going about this. We explain how we turned to AI to help us solve some of our problems and how weâre developing an internal tool calledCryptoLabeÂ to help us. CryptoLabe is named after the marinerâs astrolabe, a navigation instrument refined by Portuguese navigators. Just as an astrolabe helped sailors determine where they were and chart a course, CryptoLabe helps us discover cryptography in our code, understand how it is used, and chart a path to post-quantum migration.

CryptoLabe is highly specialized to our internal systems (our repositories, our ticketing systems, and internal documentation processes) and still evolving as we continue its development, so we arenât making it available to customers. Nevertheless, weÂ are sharing our learnings so that other organizations can build upon our efforts as they work through their own PQ migration journey.

## The scale of the problem

The software that powers most Cloudflare products lives inside our single centralized source control management platform.Â This means we can find most uses of cryptography across our platform by just looking through our codebase.

While the centralization of our codebase is a marked advantage for us, we still need to contend with three challenges that come with the scale of this problem. First, our code is spread across many repositories.Â Second, cryptography rarely announces itself plainly in the code. Instead, it hides in

- shared libraries that a repository imports but may or may not actually call
- upstream and protocol defaults, like a TLS 1.3 listener that is configured to negotiate a classical key exchange such as X25519 rather than post-quantum X25519MLKEM768
- configuration files that select algorithms far away from the code that uses them, like a TLS responder whose key exchange protocols are pinned in a YAML file stored in a different repository
- code paths that are dead, test-only, or on a path to being deprecated

Third, cryptography discovery is about more than just pattern matching.Â GreppingÂ for certain algorithm names (e.g. âRSAâ or âX25519â) overcounts, because it finds cryptography in unused code. Grepping also undercounts, because it misses defaults and indirect uses in dependencies and configuration. Most importantly, it can't tell you how the cryptography is used. A classicalECDSAÂ signature could be part of aJWT,IPsec,TLS, orSSH, and each has a completely different migration path. Many uses also depend on the other side of the connection: a TLS server may support both post-quantum key exchange and classical key exchange; the one it chooses to use would depend on the client.

## Turning to AI

It turns out that AI is pretty good at doing more than just grepping. A model can search a codebase, follow evidence across files, and return structured analysis. It can also enrich findings by pulling information from other sources, like our internal documentation and ticketing systems. In fact, AI can even explain how cryptography is being used and how it should be updated. Weâve been putting that idea to the test as we develop CryptoLabe.

As we said before, our first two goals are to (1) discover and understand the use of cryptography in our codebase, and also (2) to get metrics on the state of our PQ migration. Towards these goals, our current implementation of CryptoLabe performs scans in two stages, as shown in the figure below.

![](/images/posts/158005269d05.jpg)

The first âdiscoveryâ stage starts by mapping the repository. It then searches for cryptography through source, configuration, manifests, lockfiles, scripts, tests, and documentation. AmongÂ other things, the scan looks for the use of cryptography like key agreement, signatures, asymmetric encryption,PKI, tokens, credentials, hardware security module integrations, and more. This discovery stage produces a set of "raw observations."

Each raw observation feeds a run of the second stage. This âanalysisâ stage first re-checks the observation against the source code. It then investigates how the cryptographic operation is used at runtime, what role the repository plays, and which internal or external parties it depends on. When necessary, it can inspect related code in other repositories to complete the analysis. Finally, it takes a pass over its own conclusions, searching for missing or conflicting evidence such as configuration overrides, test-only code, or incorrect assumptions about runtime behavior.

Next, the model assigns a classification to the finding. If there is not enough evidence to assign a classification, the model assignsMore evidence needed,External dependency, orUnknownÂ rather than guessing.

This is the current list of classifications used by CryptoLabe, containing catch-all classifiers which will likely be refined as we proceed through our migration. (As an example, we could refine our classifiers by splitting the âencryptionâ classifier intokey agreementÂ andHPKE; you get the idea.)

Classification

Examples

Classical encryption

This is a catch-all category that finds cases of elliptic-curveDiffie-Hellman key exchange (ECDHE)Â (e.g., X25519, P-256, P-384), RSA key agreement or other uses of public-key encryption (e.g.,HPKE). These are broken by a quantum computer runningShor's algorithm, which puts them at risk ofharvest-now-decrypt-later attacks.

Classical signature

This is a catch-all category that finds use of an RSA signature or elliptic-curve (ECDSA) signatureÂ in anything, for example a certificate, a TLS handshake, another protocol handshake. These signatures are broken by Shor's algorithm.

Classical token

[翻译失败，原文如下]

We found a lot ofRS256 or ES256 JWT tokens, so we created a special classification for them. These are JWTs that use classicalÂ RSA and ECDSA signatures;RFC 9964Â defines a post-quantum replacement usingML-DSA.

PQ-ready hybrid key exchange

Finds hybrid post-quantum key exchange in TLS 1.3, i.e.X25519MLKEM768. This is the most prevalent use of PQ encryption in our codebase.

PQ-ready

Finds other uses of post-quantum cryptography that are notX25519MLKEM768Â in TLS 1.3, likeML-DSA.

Finally, it generates a report that serves two audiences: (1) product managers who need to understand what the migration means for their product, and (2) engineers that need enough detail to execute the migration. Â

Hereâs a (cropped) view of one of our reports:

![](/images/posts/8f084688373d.jpg)

While weâve been iteratively reviewing findings against the source code and with relevant engineers, we do not yet have a ground-truth dataset for reproducibly comparing different versions of the prompts weâve tried for CryptoLabe.

## Built on Cloudflareâs Developer Platform

We built CryptoLabe onCloudflare's Developer Platform. Hereâs the architecture:

![](/images/posts/7d459e958bba.jpg)

CryptoLabe runs across two CloudflareWorkers. Thereâs a scanner WorkerÂ that runs the scans. And thereâs an inventory Worker that serves the dashboard, exposes the API, and stores everything in aD1Â database. The two communicate throughService Bindings. A scan starts when someone requests it from the dashboard, and the inventory Worker passes the request to the scanner.

### Orchestrating a scan

We need a way to keep a scan alive and on track from start to finish, without building our own job orchestration system. We did this withAgents SDK. Each repository gets its own persistent coordinator built on aDurable Object (DO). A bounded queue in front of the coordinators limits how many scans run at once. When a scan's turn comes, the coordinator tracks its progress and handles cancellation, retries, and recovery.

The coordinator doesn't do the analysis itself. It hands the work toCloudflare Workflows, so that they can persist progress and automatically retry failed steps. The coordinator moves each repository through four stages:

1. discovery Workflow (the first scanning stage that produces raw observations)
2. deep analysis Workflow (the second stage, run on each raw observation)
3. merge Workflow (that builds a list of findings for a given repository, including combining repeated or similar finds)
4. publish workflow (that hands results back to the inventory Worker)

The first two workflows need the model to have access to the repository's code. We want this access to be isolated, so we donât risk damaging the codebase. Thatâs why CryptoLabe downloads the repository once, at an exact commit, at the start of each scan, and then stores that snapshot inR2. Each Workflow then restores the snapshot into a fresh, short-livedCloudflare Sandbox, an isolated container. The model then works with the Sandbox through a small set of read-only tools on an immutable snapshot of the code, even if the codebase changes while the scan is still running.

### Calling the model at scale

If we want to scan through all of our (many!) repositories, we have to worry about both cost and capacity.

For cost, the model loop sends its requests throughAI GatewayÂ to cost-effective open-weight models hosted onWorkers AI. Putting the model behind AI Gateway also makes it easy to switch models as better or cheaper ones become available. Â

Capacity became a problem once we scanned many repositories at once. Bursts of model requests began triggering HTTP 429 (rate limit) responses from AI Gateway, and scans retrying independently only made the bursts worse. We solved this with a single, global Durable Object that paces every model request across all scans, including retries. When any scan hits a rate limit, the cooldown is shared and all scans back off together, so concurrent scans share the available capacity instead of competing for it.

## Prerequisites and hard cases

Letâs now get into our third goal: surfacing prerequisites and hard cases early.

A lot of ink has been spilled aboutecosystem readinessÂ for the PQ migration, and we are now going to spill some more. As everyone knows, a PQ migration cannot happen in a vacuum. For migration to succeed, post-quantum cryptography must be supported in relevant software libraries (e.g. BoringSSL) and across parties that participate in the ecosystem (e.g. clients, browsers, origins, cloud proxies, certificate authorities, etc.). Standards are also an important indicator of ecosystem support, although a standard that is still in âdraftâ state does not necessarily mean deployment cannot proceed. As an example, we deployed X25519MLKEM768 in TLS 1.3 back in 2022 when it was still a âdraftâ at the Internet Engineering Task Force (IETF) while it was only finalized asRFC 10024Â in 2026.

Either way, our point is that in order to upgrade a system to PQ cryptography, we need to understand its dependencies and level of ecosystem support.Â

Thatâs why CryptoLabe uses the concept of âprerequisitesâ to highlight findings that cannot be immediately remediated by an individual product team working alone.

A prerequisite can be something as straightforward as âwe are currently blocked on migrating to post-quantum JWTs.â We say this is straightforward because there is already a standard (RFC 9964) for post-quantum JWTs. Nevertheless, if our software libraries donât yet support validating post-quantum JWTs, or if weâre using a token issuer that does not yet issue post-quantum JWTs, we canât go company-wide and ask each of our product teams to start PQ-ing their JWTs. This migration is blocked until we solve its core prerequisites. CryptoLabe lets us group together findings that (likely) have the same prerequisite, which also helps us decide how to prioritize resolving these prerequisites.

For example, the snapshot below shows the six findings from CryptoLabe that have post-quantumSAMLÂ as a prerequisite. (SAML is a protocol for single sign-on (SSO).)

![](/images/posts/505b60543935.jpg)

On the other hand, there may be uses of cryptography that lack even a basicÂ level of ecosystem support. Weâve been calling these âhard cases.â To find them, we wrote a separate prompt that ignores âvanillaâ uses of cryptography (e.g. ordinary TLS between internal systems) and instead looks for custom cryptographic protocols, keys, or signatures used in size-constrained fields, cryptography built into hardware, specialized cryptographic constructions (likeblind signatures), protocols without a PQ standard, and dependencies on external parties that do not yet support PQ cryptography.

This prompt is shorter and simpler than those used for CryptoLabe, since its only job is to find hard cases. Â In our qualitative review, we found that it got better results when it ran in one fell swoop against all our repositories, while also taking in context from our internal ticketing and documentation system. Â

Hereâs an example of a âhard caseâ we found: a certificate carried in an HTTP header. Post-quantum certificates and signatures are larger than their classical counterparts, so if the header (or an intermediary, or the application processing the header) assumes a certificate has a certain size, changing the signature algorithm may break the system. Our next step is to determine whether this code will remain in use in the long term. If it will, we need to measure the relevant size limits and decide how to accommodate the larger certificate.

[翻译失败，原文如下]

An important lesson here is that no single scan finds everything. Our repository-by-repository scans were effective at discovering common uses of cryptography. Meanwhile, this targeted scan worked better for âhard casesâ because it ignored well-understood cryptography and had more context about each product and its dependencies.

The bottom line is that different approaches find different things, and every finding still needs to be checked by the engineers who understand how the system actually works.

## Sharing our prompts

Weâve been messing around with the best way to write prompts for CryptoLabe for the last several months. Â We donât yet have a ground-truth dataset for comparing one promptâs performance against another, and we are not convinced we have 100% coverage of all uses of cryptography in our codebase. Instead, we have iterated by running scans, reviewing findings with the engineers that maintain the repositories, investigating misses that came up during these reviews and revising the prompts. Â  Nevertheless, we decided to publishselected prompts, so other teams can learn from and adapt our approach. These prompts are starting points, not a standalone version of CryptoLabe, and the quality of their results will depend on the model, tools, context, and engineering review available.

## Thinking through your own PQ migration

At Cloudflare, weâre taking a maximalist approach to our PQ migration because of our goal of acting as a provider of post-quantum cryptography for customers and the Internet at large. But most organizationsdo not needÂ to start by finding every use of cryptography in every repositoryÂ in every one of their products. In fact, most organizations should not be doing this, because at this time it's a waste of precious resources.

Before scanning a single repository, you can protect traffic in bulk wherever possible. If your websites run through Cloudflare, we protect your data in transit with post-quantum encryptionalready today; check this out with ournew PQ visibility features. OurSASEÂ platform,Cloudflare One, provides post-quantum encryption for private network traffic. Post-quantum encryption is provided atno additional costÂ and without requiring you to upgrade every origin server or private application on your enterprise network. This gives you a compensatingÂ control while you work through discovering and understanding the use of cryptography inside your own systems.

An exhaustive cryptographic inventory is not a prerequisite for action. Instead,Â organizations should first identify the systems whose compromise would matter most,Â discover their use of cryptography, and then PQ that cryptography in priority order. Here is one way to begin:

1. ChooseÂ a repository for one important system.Â Start with something that handles sensitive or long-lived data, authenticates users or software, or is exposed to the public Internet.
2. Run cryptography discovery against that repository.Â We hope our description of CryptoLabe will be helpful to this effort!
3. Validate the results.Â Ask the team who owns the system to validate the results of cryptography discovery and confirm that the cryptography finding is needed long term and needs to be upgraded to PQ. Itâs important to remember that it mightnotneed to be immediately upgraded to PQ if there is another compensating control in place.
4. Prioritize action.Â Figure out what upgrades you can make now and what upgrades are blocked. Record shared prerequisites that need help from a library, vendor, standards group, or another part of your organization. Prioritize your findings and make a plan for addressing the highest-impact systems and prerequisites first.

That gives you the beginning of a PQ transition plan, without requiring a complete map of every cryptographic operation in your organization. CryptoLabe is still ever-evolving, but its scans and results have been illuminating to us as we plan our migration. We hope these shared learnings will be useful as you continue to work through your own PQ migration.

Acknowledgements: Many people across Cloudflare provided feedback on and contributed to CryptoLabe, including Davide MarquÃªs, Peter Wu, Phil Schmieder, JP Aumasson, Andrew Galloni, Christopher Patton, Luke Valenta, Mari Galicer, VÃ¢nia GonÃ§alves, and theClient,TunnelandGatewayteams who reviewed reports produced by the tool.

- Cloudflare
- Sharon Goldberg
- Tiago Silva

---

> 本文由AI自动翻译，原文链接：[Using AI to chart a course for our post-quantum migration](https://blog.cloudflare.com/ai-driven-cryptography-discovery/)
> 
> 翻译时间：2026-09-30 08:14
