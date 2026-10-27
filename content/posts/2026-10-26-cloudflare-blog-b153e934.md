---
title: Cross-request KV cache exposure in the GLM-5.3 Workers AI model, and our remediation
  with SGLang
title_original: Cross-request KV cache exposure in the GLM-5.3 Workers AI model, and
  our remediation with SGLang
date: '2026-10-26'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/kv-cache-exposure-remediation/
author: ''
summary: '[翻译失败，原文如下]


  On September 8, 2026, we were alerted by a security researcher, Gadi Evron from
  Knostic, to a tenant isolation issue affecting the GLM-5....'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-27T07:09:00.057169'
---

[翻译失败，原文如下]

On September 8, 2026, we were alerted by a security researcher, Gadi Evron from Knostic, to a tenant isolation issue affecting the GLM-5.3 Workers AI model (@cf/zai-org/glm-5.3) starting on August 27, 2026. We have remediated the issue, and we restored the model on September 9. We have confirmed that no other model hosted on Workers AI was affected.

Between August 27 and September 9, a small number of customers using the GLM 5.3 Workers AI model received responses that contained data from other customers' requests made to the same model shortly before theirs. In total, 155 responses were affected, all to prompts longer than 681,280 tokens.

After excluding our own testing and the researcher's, the requests we identified are consistent in timing and volume with ordinary long-context use, not with someone repeatedly exploiting the bug. We found no evidence of deliberate exploitation.

Today we are publishing this report alongside a post fromÂ SGLang, the open-source inference engine that we use, as a coordinated disclosure.Â This post describes the bug that caused this issue, our response timeline, and the subsequent hardening we have conducted on our production SGLang deployments. We also detail our continued efforts with the upstream maintainers of SGLang to address this and similar bugs.

## What happened

GLM is a text generation model fromZ.aiÂ that is built for agentic coding workflows; it is one of the manymodelsÂ available through Workers AI. Gadi Evron submitted a report on September 8 through our HackerOne program stating that very long prompts sent to@cf/zai-org/glm-5.3Â on Workers AI sometimes returned text that belonged to other users' sessions. Cloudflare reproduced the issue the next morning and took the model offline within 40 minutes of declaring an incident. We then deployed a corrected configuration and a patched inference engine, and restored service the same day. Â

This specific report of cross-request KV cache exposure was the result of two overlapping issues. The first was a misconfiguration of the open-source inference engine, SGLang, used by Cloudflare. We deployed GLM 5.3 with a 1,048,576-token context window, but the KV cache pool on our prefill GPUs only had room for 681,280 tokens. We were aware of this mismatch before launch. We expected the engine to return an error for any prompt it could not process, and our long-context tests returned successful responses, so we did not believe this to be an issue.

The second was a bug in how SGLang handled the resulting over-length requests in disaggregated prefill/decode mode. A prompt that did not fit the pool was internally marked as rejected and replaced with a one-token placeholder, but instead of aborting the request and returning a client error, prefill generated the KV cache for the placeholder prompt and transferred it to the decode node. The decode node received a "transfer complete" message and assumed that prefill overwrote the KV cache from previous requests with the full prompt for this request, when in fact it left the majority of the previous state intact. The decode node subsequently generated a response while attending over stale cache pages that still held data from earlier requests. As a result, responses to prompts longer than 681,280 tokens could contain data from other users' GLM 5.3 sessions.

## Immediate remediation

Afterdisabling the model, we took the following actions to correct this vulnerability before restoring public access to it:

To fix our configuration, we made the pool hold the full context.Â We adjusted our GLM 5.3 configuration to match our GLM 5.2 configuration, which freed enough GPU memory that the prefill KV pool now holds about 2.04 million tokens, roughly twice the 1,048,576-token context length. A prompt that fits the context window now always fits the pool, so the rejection path is never reached for a valid request. This alone prevents the bug from being exercised.

To fix the engine, we also made the rejection path safe.Â Relying on pool size alone is fragile: any change to quantization, tensor parallelism, CUDA graph sizes, or a future model version changes the pool size in a way that's easy to miss. Furthermore, there may be other situations in which the prefill scheduler can reject a request and trigger the same bug. To prevent this, we also patched the engine so that a request carrying a pending rejection is retired at the disaggregation admission queue, with its original error, before any bootstrap, allocation, or KV transfer happens. We proposed this upstream as#38704, which also had the decode node verify that the number of tokens transferred matches the number it reserved. The fix was already on SGLangmainin#36988, merged September 6 for a related failure path but not yet released. The maintainers also merged#38935, which rejects these requests earlier, following our approach.

We validated both changes against the researcher's reproduction script and our own canary-marker tests before restoring the model.

## Background: how we serve GLM 5.3

Workers AI runs GLM 5.3 with SGLang in a disaggregated configuration: a pool of prefill GPUs processes the prompt and produces the model's KV cache for it, then hands that cache over remote direct memory access (RDMA), viaMooncake, to a pool of decode GPUs that generate the response. We have written about this architecture before in our posts onhigh-performance LLMsÂ andÂsmaller, faster, safer models.

The KV cache in GPU memory is a shared pool of fixed-size pages. Each request is assigned pages when it is admitted and releases them when it finishes. Pages are not currently zeroed between requests; the next request that gets a page simply overwrites it. This approach is common among inference engines and is necessary to achieve the best performance, but it means that the inference engine is responsible for tracking ownership of these memory pages. KV cache page ownership and lifetime tracking has to deal with not just shared ownership within a node (KV cache offload and token generation both access the memory with different lifetimes), but also ownership that is technically shared with the remote prefill node (which holds a simultaneous mutable reference to the page).

Furthermore, the size of this pool is not a configuration value. SGLang sizes it at startup from whatever GPU memory remains after loading the model weights. The model's advertised context length is a separate configuration value. Nothing forces the two to agree, and it is our job to check that they do.

## Issue one: misconfiguration

On our GLM 5.3 prefill nodes with our configuration, the pool came to 681,280 tokens while the model's context length is 1,048,576 tokens. The selected KV pool size is printed by SGLang in logs during startup and exposed as a metric. We were aware of this size mismatch; however, during pre-launch testing we observed successful HTTP status codes and a streaming body with no error frames during benchmarking. We assumed that the engine was capable of gracefully handling the difference between the KV cache pool and requested context window via streaming or some other mechanism.

This was one critical gap in our testing: we only validated HTTP response codes and engine performance at long contexts, without validating model output and coherence.Â We now check KV pool size against context length directly, from the running engine, before any disaggregated deployment change ships, rather than inferring it from response codes.

## Issue two: SGLang bug

In v0.5.21, the SGLang team has now addressed this bug in how it was handling prompts longer than the KV pool size. Hereâs what was happening before.

[翻译失败，原文如下]

When a prompt arrived that was longer than the KV pool could hold, SGLang's scheduler rejected it. The rejection path (Req.set_finish_with_abort) recorded the error to be returned to the client and swapped the prompt for a one-token placeholder so that the request could drain through the normal batch machinery without allocating real memory. On a single-node deployment this worked: the placeholder ran, the batch finished, and the client received an error.

![](/images/posts/e0f5a99b354f.jpg)

In disaggregated modeÂ such as we operate, the admission queues on both prefill and decode checked whether a request wasfinished, not whether it wasrejected. A rejected request reported itself as live. So:

1. Bootstrap.Â The router told the decode node the prompt length (8 pages in the diagram). Decode reserved 8 KV pages for the request.
2. Prefill admission.Â The prefill admission queue admitted any request wherereq.finished()Â was False. A rejected request stored its rejection into_finish, notfinished_reason, sofinished()Â still returned False. The rejected request was admitted.
3. Prefill forward pass.Â Rejection had already replaced the prompt with a one-token placeholder. Prefill ran a trivial forward pass on that one token.
4. KV transfer.Â Prefill sent one page of KV to decode and signaled that the transfer was complete.
5. Decode admission.Â Decode's admission queue had the samefinished()Â check, so it accepted the handoff.
6. Decode attention.Â Decode started generating and attention read all 8 reserved pages. Only page P0 had been written by this request. Pages P1 to P7 still held what earlier requests left in them: other users' prompts and partial generations.
7. Response.Â The client got HTTP 200 instead of HTTP 400.prompt_tokensÂ matched the long prompt and the reply was coherent. It arrived faster than an 8-page prefill should take, and it contained content from other users' KV pages.

Every request over the threshold behaved this way. This bug had been reported to SGLang by another user as issue#30233Â on July 6, 2026, which Cloudflare noticed while investigating this incident. We had been flagging these types of issues with SGLang since v0.5.10 and this security incident sped up work that Cloudflare had already started in collaboration with the SGLang team. The patch for this issue was released in SGLang v0.5.20, with follow-ups in v0.5.21 and v0.5.22, and is available for all other operators dependent on SGLang to use. We highly recommend all operators update SGLang dependencies to v0.5.22 or later. For more details on specific PRs, read on below.

GLM 5.3 was the only model affected by this bug. Every other disaggregated deployment on Workers AI has KV pools larger than its context length on both prefill and decode, so no request could reach the rejection path. We have applied the engine fix and the hardening described below to every model we serve with SGLang, and our deployment checks require them for every new deployment.

## Timeline

All times UTC.

Aug 27, 2026

GLM 5.3 launched on Workers AI with a prefill KV pool smaller than its context window. The exposure was present from launch.

Sep 8, 2026 - 23:11

Report received via HackerOne.

Sep 9, 2026 - 08:00

Cloudflare begins verifying the HackerOne report.

Sep 9, 2026 - 13:22

Security incident declared. Product Security reproduced the leak using two independent accounts within 25 minutes.

Sep 9, 2026 - 14:00

After confirming the scope of the issue, GLM 5.3 was setÂ to private. Requests return HTTP 400. Status page updated.

Sep 9, 2026 - 14:35

Root cause identified as the prefill pool being smaller than the context length. Canary prefill node with a larger pool confirmed not susceptible.

Sep 9, 2026 - 14:52

All prefill nodes rolled to the corrected configuration.

Sep 9, 2026 - 19:04

Full deployment rebuilt with the corrected configuration plus a Cloudflare-authored engine patch that correctly returns errors for requests rejected by the prefill scheduler. Validated against the researcher's reproduction script.

Sep 9, 2026 - 19:40

Model restored to public.

Sep 10, 2026Â - 23:30

Meeting with the SGLang maintainers (RadixArk CTO and core engineers) to agree on upstream fixes.

Sep 11-19, 2026

Additional hardening rolled to all production SGLang deployments (details below).

Sep 16-Oct 12, 2026

Upstream SGLang merges the admission fix, per-transfer checksums, abort-ACK preservation, and turns deferred KV release on by default.

Oct 2, 2026

SGLang v0.5.21 released.

Oct 19, 2026

SGLang v0.5.22 released.

Oct 26, 2026

Coordinated publication with the researcher and RadixArk.

## Ongoing hardening effort

This bug belongs to a class of KV cache memory-safety bugs that Cloudflare has been working to address for several months. In each case, a page is freed, reused, or read while something else still has a claim on it. We see two common causes.

The first is page lifetime within a single node. Several tasks on a decode node can hold the same page at once: token generation, offload to host memory, the KV transfer receiver, and the abort and error paths. If one of them frees the page while another is still using it, a new request can be given that page while it is still being read or written. Our earlier fixes for decode offload (#24226,#30899) and double release on grammar errors (#30937) were of this kind.

The second is a race across nodes. When a request is aborted while prefill is still writing its KV cache to decode over RDMA, the writes already sent cannot be recalled. If decode frees those pages right away, those pages can be given to another request, and the late writes land in that request's KV cache. Cloudflare has contributed to the effort to fix this race through proposed fixes (#31357,#38961) and a reproduction script (#32564). In both cases the result is corrupted output, or one user's data in another user's response, with no error raised. The bug in this incident was different: a rejected request went through the handoff every time, rather than by a timing accident. But it had the same result: decode reading pages this request never wrote. None of these covered the failure in this incident in which prefill rejected the request, and decode never learned of it.

Since the incident, we have:

- Extended deferred release to hold prefill's source pages as well, and to cover every failure type, not just aborts. We proposed it upstream as#38961, which was superseded by#40645,#41402, and#41404.
- Deployed bounded Mooncake transfer batches (#32758, from the SGLang community), so no single transfer call can outlast the release timeout.
- Changed our load balancer so a client disconnect no longer aborts a request mid-transfer. It holds the prefill connection until prefill finishes and the decode connection until the first token, then closes both.
- Added a check to every disaggregated deployment change: KV pool size measured against context length, deferred release on both roles, transfer batch bounds inside the release timeout, and all required patches applied.

All of these changes were released to our disaggregated production deployments.

## Working with the SGLang team

We met with the SGLang maintainers at RadixArk on September 10, the day after the incident. We agreed that RadixArk would investigate the race conditions we had reported, upstream the integrity-checking idea, and build reproduction tests for this class of bug.

The following have landed on SGLangmainto address this incident and related KV cache race conditions, and all but one are included in v0.5.22. Operators running disaggregated SGLang should update to v0.5.22 or backport these patches as needed.Â

Category

Pull request

Release

What it does

Incident

#36988

v0.5.20

Retires aborted prefill requests before their result reaches decode. This stops the exposure in this incident.

#38935

v0.5.21

[翻译失败，原文如下]

Rejects these requests at admission, before any bootstrap, allocation, or KV transfer. Follows the approach in Cloudflare's draft patch,#38704.

#39461,#41612

v0.5.21, v0.5.22

sgl-routerÂ cancels both halves of a request on client disconnect or prefill failure.

#37454,#41023

v0.5.20, v0.5.21

Enables deferred KV release only on backends that support it, then turns it on by default.

#40645,#41402

Fixes cases where the drain confirmation was lost, so releases happen on confirmation instead of waiting out the timeout.

#41404

Holds pages on every transfer failure, not only decode-initiated aborts.

#41618

Fixes a regression in the abort notification path.

#43719

v0.5.22

A failed Mooncake send no longer reports its writes as drained.

#37077

Tags abort messages per request so a reused ID cannot consume a stale confirmation. Adds MORI support.

#36612

Shares the prefill-to-decode failure notification across Mooncake, NIXL, and MORI.

#32758

Optional cap on Mooncake transfer batch size, so one timed-out call cannot leave an unbounded number of writes in flight.

Lifetime

#30899

Decode waits for an in-progress offload to host memory before retracting a request and freeing its pages. Authored by Cloudflare.

#43562

Keeps tensor-parallel ranks in agreement when a host-memory cache restore fails.

Observability

#39500

Adds--disaggregation-enable-kv-checksum: decode verifies a checksum of the transferred KV before generating. Cleanup in#39729, merged and awaiting release.

#38596,#40642

Fixes for SGLang's KV canary, which detects and logs potential corruption.

#41128

Metrics for deferred release: count, duration, and whether each hold ended on drain confirmation or timeout.

These follow-ups are still works in progress:

- #39729Â Additional cleanup for--disaggregation-enable-kv-checksum. Merged, awaiting release.
- Zero KV pages on release, draft proposal:#46435
- Extend KV checksum validation from the prefill-to-decode handoff to every decode step (see Integrity by construction, below)
- Broader KV Canary and KV Checksum model and feature support

## What we recommend to other operators

If you run SGLang in disaggregated prefill/decode mode, we recommend the following:

1. Measure your KV pool and compare it to your context length, on every prefill and decode node, from the engine's startup log, after every change to weights, quantization, parallelism, or memory fraction. If the pool is smaller, lower the context length to fit. Do not rely on a proxy to enforce the limit, and do not assume the engine will reject what does not fit. This is the check we did not enforce.
2. Upgrade to a build that includes#36988and#38935Â (v0.5.22 or later), so an over-length request is rejected before handoff regardless of pool size. This is the engine-side fix, and it is the backstop for the day your check in step one is wrong.
3. Run with deferred KV release on both rolesÂ (default after#41023), and bound your Mooncake transfer batches so a single timed-out call cannot leave an unbounded tail of writes.
4. Turn on corruption detection where your model supports it.Â--disaggregation-enable-kv-checksumÂ and--kv-canaryÂ do not yet cover every model architecture. Check your logs to confirm requests are being verified. We are working with the SGLang team to extend both checks to more architectures, including GLM 5.3, GLM 5.3 Flash, and DeepSeek V4.
5. Ensure your proxy is not generating unnecessary aborts.Configure your load balancer to allow requests to proceed up to the first token, so that you do not trigger an abort that requires cross-node coordination.

## Longer term

### Integrity by construction

Configuration checks and lifecycle fixes reduce the number of ways a page can be misused. They do not make misuse impossible, and this incident is a reminder that the next bug will have a shape we have not seen. The durable answer is for the engine to detect, at read time, that a request is about to attend over a page it does not own, and fail that one request rather than return someone else's data.

We built a prototype of this over the summer anddescribed it in August. Every physical KV page carries a tag that changes when the page is reallocated, each request records the tags it expects, and the mapping is checked before decode reads the cache. In our tests it cost under 1% in throughput and tail latency. We tested it on GLM 5.2 in mid-August, but disabled it shortly afterwards due to reliability issues.

The prototype was also tied to specific attention backends and model architectures, so it could not be a general fix. We are working with the SGLang team to build a production version into the engine that works across every model, rather than maintaining Cloudflare-specific patches. The per-transfer checksum in#39500Â is a first step: it validates the handoff from prefill to decode. Page-level tags go further, because they check every read, including reads long after the transfer.

### Integrity by mathematical impossibility

RDMA copies data directly from one nodeâs memory to anotherâs. Itâs vital for the two machines to agree on where the data goes, how large it is, and when itâs finished; any mismatch can cause the receiver to read the wrong data. This bug is an example of a consistency failure in a distributed system, in which the two machines had inconsistent views of the state of that system.

Elsewhere in Cloudflare, we have put effort into proving the safety of distributed systems using formal verification methods.TopazÂ enables conflict-free IP selection for our authoritative DNS servers. Models ofMeerkatâsÂ QuePaxa implementation have demonstrated consistency bugs that were subsequently fixed.

We are now directing our experience in formal methods to KV cache transfer engines. This will start with modeling and proving the safety of an RDMA-based KV cache transfer protocol. The goal is to model our production SGLangâs distributed KV cache system using Mooncake, then track and fix any divergence from the safety properties we want to guarantee. The aim is to prove â as far as possible â that a bug like this cannot occur again. Realistically, we expect gaps in what the provers can tell us, but proving the rest of the system allows us to more closely review and monitor those gaps.

## Coordinated disclosure

We are publishing this report as part of a coordinated disclosure. We want to thank the researcher, Gadi Evron, who reported this through our HackerOne program with a clear, reproducible script and gave us time to fix it and to coordinate with the SGLang maintainers before publishing. We also want to thank the SGLang team at RadixArk, who treated this as their problem as well as ours and landed the upstream fixes with urgency.

Read more atthe post from the SGLang team.

If you find a security issue in Workers AI, please report it athackerone.com/cloudflare.

## Related tags

Follow on Social Media

- Cloudflare
- Michelle Chen

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Cross-request KV cache exposure in the GLM-5.3 Workers AI model, and our remediation with SGLang](https://blog.cloudflare.com/kv-cache-exposure-remediation/)
> 
> 翻译时间：2026-10-27 07:09
