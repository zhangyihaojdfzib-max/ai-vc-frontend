---
title: 'Automatic Key Exchange: faster, post-quantum secure origin handshakes for
  45 billion daily connections (and counting)'
title_original: 'Automatic Key Exchange: faster, post-quantum secure origin handshakes
  for 45 billion daily connections (and counting)'
date: '2026-09-08'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/automatic-key-exchange-for-origins/
author: ''
summary: '[翻译失败，原文如下]


  Every time Cloudflare opens a new TLS 1.3 connection to an origin server, we have
  to make a guess: the protocol requires us to commit to ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-10T07:13:44.568756'
---

[翻译失败，原文如下]

Every time Cloudflare opens a new TLS 1.3 connection to an origin server, we have to make a guess: the protocol requires us to commit to a key agreement algorithm in the very first packet we send, before the origin has told us anything about itself or what it can support. If we guess right, the handshake completes in one round trip. Guess wrong, and the origin replies with aHelloRetryRequest, we start over, and the connection costs two round trips.

For years, our guess was the same for every origin on the Internet:X25519. Widely supported, but as it turns out,suboptimal for roughly 30%of the origin connections we've since measured.

Today we're announcingAutomatic Key Exchange, an extension ofAutomatic SSL/TLSthat replaces the guess with a measurement. We probe each origin to learn which key agreement algorithms it supports and prefers, then lead with that algorithm on the first try, preferring thepost-quantum hybridX25519MLKEM768wherever the origin can speak it.Â

With the ongoing rollout of Automatic Key Exchange across origin connections, HelloRetryRequests fell from roughly 52% to 3.7%, cutting more than 150 ms off connection handshake latency at p90. In addition, as part of our ongoing rollout, hundreds of thousands of domains now have post-quantum origin connections that nobody had to configure, with that number growing daily.

While the milliseconds are important, that second part may matter more. Somewhere right now, an adversary is recording encrypted traffic it can't read yet, betting that it will be able to in the future (an attack known asharvest-now, decrypt-later). Cloudflare is sprinting to make the Internetquantum-secure by 2029, the year some industry experts estimate classical encryption algorithms could be breached. That day has a name: Q-Day. Meeting that deadline can't depend on millions of website operators each becoming expert cryptographers.It has to be automatic.Until today, preferring post-quantum connections required a manual setting: eitheryou turn them on from Cloudflareâs side, or you have your origin server insist upon them. It was easy to get wrong. But today itâs just â¦ automatic!

## TLS 1.3 handshake: guessing the key exchange algorithm

Every secure web connection starts with a TLS handshake, which authenticates the server and derives a shared secret key.Our previous Automatic SSL/TLS blog postscover that process in detail.

As Cloudflare operates as a reverse proxy, what appears to be a single secure connection is actually two: one between the visitor and Cloudflare, and a second between Cloudflare and the origin server. Each connection operates independently, with its own handshake, identity checks, and encryption keys.

![BLOG-3300 2.png](/images/posts/97b50e65a337.jpg)

Automatic Key Exchangeaffects the second connection. When Cloudflare connects to the origin, Cloudflare acts as the TLS client and must begin the handshake. We initiate the connectionby sending a ClientHello messagecontaining the hostname and a list of supported key agreement algorithms.

In the happy path, TLS 1.3 can establish a new encrypted connection in just one network round trip (shown on the left in the diagram above). In this case, Cloudflare sends a ClientHello listing its supported key agreement algorithms, along with one or moreclient keyshares. If the origin accepts that choice, it responds and the handshake completes.This predictive key exchange is an innovation of TLS 1.3, and a large part of why itâs faster than TLS 1.2.

Otherwise, if the origin prefers a different option, it sends aHelloRetryRequest(HRR) and asks Cloudflare to try again (the flow on the right in the diagram above). Cloudflare then sends a second ClientHello, generating a newclient keysharebased on the key agreement algorithm specified by the origin. The connection still succeeds, but the retry adds a full network round trip before Cloudflare can fetch content. This is like missing a shortcut in Mario Kart: you still reach the finish line, but you lose the time the shortcut was supposed to save.

Either way, using theclient keyshare,the server generates the shared key. The server then returns aserver keysharewith which the client can also compute the shared key. This shared key is used to protect the rest of the connection using symmetric cryptography, such asAES.

## The cost of the safe guess

For years, our initial client keyshare guess for origin connections using TLS 1.3 was static; we'd always sendX25519while advertising support for other key agreement algorithms. This was a safe strategy becauseover 95% of originssupport X25519, and any origins that didnât could issue a HelloRetryRequest (HRR) without breaking the connection.

However, X25519 is vulnerable to quantum computers. SinceSeptember 2023, we have advertised support of post-quantum key agreement to origins: first as X25519Kyber768Draft00 and today as X25519MLKEM768 (the standardized version of the algorithm). Crucially, advertisingsupportdiffers from leading with a keyshare in the ClientHello. An X25519MLKEM768 keyshare is 1,216 bytes compared to X25519's 32 bytes, pushing the ClientHello past a single network packet. While the TLS standard allows multi-packet segments, some legacy middleboxes and origin serverscan failwhen receiving ClientHello messages split across multiple packets. In ourprevious study, around 0.34% of scanned origins failed to complete the TLS handshake when receiving a post-quantum keyshare first, while the vast majority of origins still relied on classical X25519.

![BLOG-3300 4.png](/images/posts/9399aa5e2bc1.jpg)

Therefore, to prevent any possible breakage of origin connections, we used HRR as a safety valve. We only advertised post-quantum support, sent a classical X25519 keyshare, and required capable origins to request a post-quantum exchange via retry. For origins that did not support the HRR flow, customers had the option tomanually opt into leading with X25519MLKEM768 keyshare. Between 2023 and today, thepercentage of origins supporting post-quantumkey exchange algorithms grew from 0.5% to 12.8%, and we expect that to keep climbing as hosting stacks upgrade to PQ safe algorithms.

While safe, this default of only upgrading to post-quantum secure connections via retry added unnecessary latency for two reasons:

- While allmodern builds of OpenSSL, BoringSSL, and rustlssupport X25519MLKEM768, they handle a classical X25519 keyshare differently. Depending on the build, some older builds may accept it by default unless explicitly configured to prioritize the post-quantum secure keyshares, while newer builds will immediately issue an HRR to prioritize post-quantum connections.
- Over 6%of origins prefer either P-256 or P-384 over X25519, triggering an HRR round trip even for purely classical connections due to our static choice of initial client keyshare.

To eliminate these wasted round trips, we began scanning origin servers to map their exact key agreement capabilities as part ofAutomatic SSL/TLS. Using these scan results, we automatically tailor our initial keyshare on a per-origin basis: maximizing post-quantum connections without risking site outages, all while making our connections faster for applicable domains.

## Extending Automatic SSL/TLS to the post-quantum age

Automatic SSL/TLSnow includesAutomatic Key Exchange. Across millions of origins, guessing different keyshares carries operational risk, because we have no advance knowledge of how any individual origin is configured. So rather than infer capability, we measure it directly, reusing the scanning pipeline that already powers Automatic SSL/TLS.

For a growing number of origins, this delivers post-quantum key agreement on the very first try at connection setup, without extra round trips and without requiring any manual setup.

This is how it works:Â

[翻译失败，原文如下]

1. For each TLS 1.3 capable origin, we run a series of a few lightweight TLS handshakes, each offering exactly one key agreement group: X25519, P-256, P-384, P-521, or X25519MLKEM768. Together these probes tell us the full set of algorithms the origin supports. And because the active scanning happens outside your production traffic path, we confirm that both your origin and the network in between can handle connections with a stronger key agreement before any real traffic depends on it.

1. A single domain often fronts multiple subdomains that may resolve to different origins with varying capabilities. We evaluate each subdomain independently and weight the results by its actual traffic volume. This ensures a domain-wide preference reflects HTTP traffic volume rather than weighing a dormant subdomain equally with your busiest endpoint. For example, if almost all traffic hits your www and api subdomains, those endpoints would heavily determine the key exchange preference for the entire domain.

1. From the key agreement groups an origin supports, we then select the strongest candidate using a strict priority order: post-quantum hybrids (X25519MLKEM768) first, falling back to the fastest classical algorithm accepted by the origin (X25519, P-256, P-384, or P-521).

1. Once we know the optimal key-agreement an origin prefers, we start rolling it out. The new preference goes to a small share of that origin's traffic first, and the system monitors its failure and HelloRetryRequest (HRR) rate while it runs. If retries climb above that origin's baseline, we roll the change back, the same wayAutomatic SSL/TLSreverts an encryption mode upgrade that may misbehave. At the worst case of rolling back, a bad key-agreement preference costs us an additional round trip latency, not a broken TLS connection for the duration of the rollout phase.

1. Origin configurations change over time: a customer moves to a new load balancer, a TLS library ships post-quantum support in a routine release, an operator turns off an older key-agreement algorithm support. We rescan every origin daily, so a server that adds post-quantum support, or stops supporting the curve we were using, gets a new preference at the next scan.

For most customers, there is nothing to configure. If your origin speaks TLS 1.3, we will automatically negotiate the strongest key exchange it supports, for instance, if an origin supports X25519MLKEM768, Cloudflare prefers it and can establish post-quantum key agreement without any extra round trip latency.

## Configuring Automatic Key Exchange

Automatic Key Exchange is active by default for all existing and new domains, requiring no manual action for most setups. If you want, you can manage these settings independently in the Cloudflare dashboard under SSL/TLS > Overview > Configure >Origin connection & post-quantum encryption.

With the Automatic Key Exchange toggle enabled, Cloudflare scans your origins out-of-band and leads with a dynamically selected keyshare. With it disabled, scanning stops and Cloudflare reverts to a fixed/static default key agreement order.

![BLOG-3300 5.png](/images/posts/1e729c485d52.jpg)

We have also introduced a newCompliance requirements settingunder Automatic Key Exchange. You can filter which key agreements Cloudflare is permitted to use and advertise support for origin connections. When configured, Automatic Key Exchange and all origin-facing traffic strictly observe these rules:

- Post-quantum hybrid: Restricts negotiation exclusively to hybrid post-quantum key agreements (X25519MLKEM768), removing classical algorithms entirely. All your successful origin TLS 1.3 connections will beguaranteedto be post-quantum secure.
- Federal Information Processing Standards (FIPS): Restricts negotiation exclusively toFIPS-compliant key agreements.

Selecting both options requires an algorithm that satisfies both criteria simultaneously; if no overlapping key agreement exists, the configuration is rejected. See theAutomatic Key Exchange documentationfor details.

![BLOG-3300 6.png](/images/posts/9712fbd48393.jpg)

By selecting these options, you configure your intent rather than specific algorithms. This ensures that as compliance standards evolve or new post-quantum algorithms emerge, your configuration stays up to date automatically.Â

However, these requirements are worth approaching carefully. They do not grant an origin new cryptographic capabilities, they only narrow what Cloudflare can negotiate.Â

An important note: Enforcing post-quantum hybrid on an origin that lacks X25519MLKEM768 support leaves no mutually supported algorithm, causingallTLS 1.3 connections to fail.Unless you have a strict policy obligation to enforce post-quantum exchange or FIPS compliance across every connection, leave both options unselected and allow Automatic Key Exchange to negotiate the optimal algorithms safely for you.

## Making the Internet safer and faster, together

Automatic Key Exchange works for domains whose origins speak TLS 1.3 (as predicting preferred key agreement method is aTLS 1.3-only feature). Itâs enabled by default, and our scanning pipeline has already assigned key exchange preferences towell over a million domainswhile enrollment continues across the remaining network.

From that initial cohort, we found that roughly64%of them stayed on the classical X25519 as their preference, so nothing about their connections changed. Around33%of them now have their preference set to X25519MLKEM768, which causes traffic to those origins protected fromharvest-now, decrypt-laterquantum attacks in a single round trip. The remaining3%selected a different classical curve preferred by their origin, such as P-384, P-256, or P-521.

![BLOG-3300 7.png](/images/posts/8ac85930a81f.jpg)

Approximately 9,000 domains each day have their key agreement preference set to a key agreement method other than X25519. Nearly all of these move directly to preferring post-quantum key exchange, while the remainder adopt other classical curves better supported by their originâs TLS configuration.

As we mentioned earlier, prior to Automatic Key Exchange, almost every post-quantum origin handshake required a HelloRetryRequest (HRR) because our static initial guess defaulted to classical X25519. The result was that post-quantum connections paid a mandatory second round trip before completing the TLS handshake.

![BLOG-3300 8.png](/images/posts/f2f2e2d01aae.jpg)

With the rollout underway, that latency penalty is virtually gone for almost allpost-quantum capableorigins:99.2% of post-quantum TLS 1.3 connections of the currently scanned cohort of origins now complete in a single round trip. Beyond removing the extra round trip, we see that across that cohort, post-quantum origin traffic keeps growing from roughly 25 billion connections to45 billion per day.A significant part of that growth has come from Automatic Key Exchange upgrading classical connections to a post-quantum preference for scanned origins.

Many origins support multiple key agreement algorithms without preferring one over another. For example, an origin that supports post-quantum key agreement may still accept a classical (X25519) key share without rejecting it or issuing an HRR. Passive observation, therefore, cannot reveal the originâs full capabilities. Active probing allowed Automatic Key Exchange to uncover thousands of origins whose post-quantum support never appeared in their origin traffic.

![BLOG-3300 9.png](/images/posts/cace60eaca8f.jpg)

[翻译失败，原文如下]

Once our scanner discovered such origins, and updated their client keyshare preference, post-quantum connections quickly accounted for the vast majority of traffic to these origins. Other classical key agreement algorithms represent a much smaller share for these upgraded domains, primarily driven by multi-origin setups with a mix of post-quantum and classical-only backends.Automatic Key Exchange does more than just drive post-quantum adoption. It also helps pair origins with their preferred classical curve (other than X25519), reducing overall HRR rates across all scanned origins.

![BLOG-3300 10.png](/images/posts/5d9c55cc013c.jpg)

Before we enabled Automatic Key Exchange, roughly 52% of origin connections for the scanned domains required an HRR. That rate fell to just 3.7%. Avoiding an HRR removes an entire round trip from TLS connection setup,reducing p90 latency more than 150 ms for the scanned origins.This particularly benefits dynamic requests and CDN cache misses that may require a new TLS 1.3 connection to the origin, ultimately reducing latency for eyeballs. Requests sent over existing keep-alive connections do not require a new handshake and are therefore unaffected.

## Is the server post-quantum capable?

There are a number of different tools to use to find out if a server supports post-quantum key agreement.We offer one of these tools via Cloudflare Radar. Enter the hostname or IP addresses of your server, and we will check if it supports post-quantum TLS key exchange. Note that if you enter a hostname proxied by Cloudflare, Radar will check the connection to Cloudflare rather than your origin server behind it.

![BLOG-3300 11.png](/images/posts/1b96f077be2e.jpg)

Beyond verifying algorithm support, we have added the ability in the tool to check forpost-quantum TLS implementation bugs. If the results come back negative, it will also try to characterize the reason for the failure. Failures often stem from legacy middleboxes, firewalls, or server buffers dropping multi-packet payloads or failing to reassemble a ClientHello split across TCP segments. Other times the origin gives up on an unrecognized key share instead of sending a HelloRetryRequest as TLS 1.3 requires, or sends one and then cannot finish the handshake.

Radar gives you a clear picture of whether the network path handles post-quantum traffic cleanly. Automatic Key Exchange will not switch a domain whose origin fails these checks, so clearing them is what lets the upgrade happen.

## What if your origin doesn't support post-quantum key agreement yet?

Even if your origin does not yet support post-quantum encryption today, the good news is that enabling Auto Key Exchange will still be beneficial.Automatic Key Exchangefinds what your origin supports. If X25519MLKEM768 is unavailable, Cloudflare continues using a compatible classical key agreement and can still avoid unnecessary HelloRetryRequest round trips by learning which one your origin prefers.

However, Automatic Key Exchange can only prefer post-quantum connections when your origin server already supports the key agreement algorithm. Today, we see over12% of individual originsacross our network support post-quantum encryption. Post-quantum secure algorithmssupport in TLS server implementationsis increasing as recent versions ofBoringSSL,OpenSSL, andrustlsinclude support. The enterprise origin stacks, cloud load balancers, and embedded TLS terminators are upgrading on their own timelines.

If you want to add post-quantum protection capability for your domainâs origin-facing connections, you have two options:

- You can use Cloudflare Tunnel.The connection between cloudflared and Cloudflarealready uses post-quantum key agreement. This is the simplest option when you cannot change the TLS software on your public origin endpoint.

![BLOG-3300 12.png](/images/posts/7a69ede5c2f2.jpg)

- You can upgrade your TLS endpoint. Many current frameworks and TLS libraries enable X25519MLKEM768 by default. However, if you previously configured allowed curves manually for your serverâs TLS configuration, those legacy settings might override the new defaults. It is important to audit every device terminating or inspecting TLSâincluding load balancers, WAF appliances, and other middleboxesâto ensure X25519MLKEM768 is enabled on everything that sits between your origin and Cloudflare. If youâre on a managed hosting service, ask your provider whether it supports X25519MLKEM768 (many do).

SeePost-quantum cryptography between Cloudflare and your originfor supported software, configuration examples, and verification steps.

## What's next

Weâve been building Automatic SSL/TLSin public since 2024. Automatic Key Exchange is the second step in a longer arc, not the last. Weâve been public about whatâs on the roadmap since then and will continue to provide updates as we ship. A few specific things weâre working on:

### Per-origin preference granularityÂ

Today, Automatic SSL/TLS makes its decisions at the domain level. One origin server's behavior can hold the whole domain back. We're working on a per-subdomain/per origin granularity so that key agreement (andSSL/TLS encryption modes) can vary across the multiple origins that serve a single domain.

### On-demand scans

If you've just upgraded your origin's TLS stack, you shouldn't have to wait for the next scheduled scan by Automatic SSL/TLS. Originally, we wanted to scan enough to keep up with changes on the origin, but not too much so as to burden origins who ultimately return the same security information. We're building an option to trigger an on-demand rescan from the dashboard or API, so post origin upgrade you can move to the better key agreement immediately rather than waiting for our system to catch up.

Beyond triggering instant updates, this on-demand scan will live directly in your Cloudflare dashboard as a diagnostic tool. It will let you test your own origin server's behavior on demand and see exactly which key agreements it can successfully negotiate, and characterize the reasons for any failures (similar to theexternal Cloudflare Radar scanning tool).

### Automatic post-quantum origin authenticationÂ Â

Post-quantum key agreement keeps today's traffic from being decrypted by a future quantum computer. It does nothing about an attacker who uses one to forge a certificate and impersonate your origin. Closing that gap takes post-quantum authentication, whichcame to origin connections earlier this yearwhen Authenticated Origin Pulls and Custom Origin Trust Store gained support forML-DSA certificates.

There is an important issue to deal with here:downgrades. Imagine your origin server supports both a classicalRSA/ECDSA certificateand a new post-quantum ML-DSA certificate so legacy clients don't break. On Q-Day, an active adversary sitting between Cloudflare and your origin could intercept the TLS handshake and silently drop the post-quantum offer. Cloudflare, seeing only a classical response, would fall back to validating the legacy RSA/ECDSA certificate, which the attacker can forge using a quantum computer.

Preventing this downgrade in the broader WebPKI is complicated. One proposed path involves Certificate Authorities (CAs) placing a post-quantum signature on a classical certificate to prove that a legacy server truly doesn't support PQ yet. While this is a likely direction for the public web, it will take some time and coordination. Whatâs quicker (if possible!) is tostop trusting classical certificates altogether.

And for origin connections, we can! We plan to extend Automatic SSL/TLS scanning to detect origin support for post-quantum authentication (ML-DSA certificates; and in futureMerkle Tree Certificates). Once our scanner identifies such an origin, Cloudflare can automatically disable classical fallback for customers who want strict post-quantum protection, eliminating downgrade risks without disrupting un-upgraded endpoints.

## Check it out

[翻译失败，原文如下]

At Cloudflare, we believe that strong security on the Internet should be free, automatic, and on by default.Universal SSLmade encryption-by-default real for the browser-to-Cloudflare connection. Automatic SSL/TLS is doing the same for the Cloudflare-to-origin connections, and now extends that work to post-quantum key agreement.

If you want to see what your origin encryption level looks like today, check theSSL/TLS sectionof your dashboard. If you want to verify your origin's post-quantum readiness directly,Cloudflare Radarwill tell you if you need to update your server stacks. And if your origin already supports post-quantum, Automatic Key Exchange will tell Cloudflare so that we will connect to your origin faster and more securely.

## Related tags

Follow on Social Media

- Cloudflare
- Suleman Ahmad
- Yawar Jamal
- Alex Krivit

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Automatic Key Exchange: faster, post-quantum secure origin handshakes for 45 billion daily connections (and counting)](https://blog.cloudflare.com/automatic-key-exchange-for-origins/)
> 
> 翻译时间：2026-09-10 07:13
