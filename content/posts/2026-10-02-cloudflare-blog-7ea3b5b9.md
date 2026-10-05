---
title: "Announcing Cloudflare OHTTP Gateway â\x80\x93 expanding access to Cloudflareâ\x80\
  \x99s privacy-preserving infrastructure"
title_original: "Announcing Cloudflare OHTTP Gateway â\x80\x93 expanding access to\
  \ Cloudflareâ\x80\x99s privacy-preserving infrastructure"
date: '2026-10-02'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/announcing-cloudflare-ohttp-gateway/
author: ''
summary: '[翻译失败，原文如下]


  Today, end users carry too muchÂ of the burden of online privacy. To avoid third-party
  trackers or targeted ads, users are instructed to ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-05T08:02:26.735689'
---

[翻译失败，原文如下]

Today, end users carry too muchÂ of the burden of online privacy. To avoid third-party trackers or targeted ads, users are instructed to use a VPN, disable cookies, or install adblockers. Meanwhile, some app developers end up knowing more about their users than theyâd care to: a typical client-server exchange creates a trail of user data, like the clientâs IP addressÂ or TLS fingerprint. This level of visibility can be a burden.

Thatâs why Cloudflare builds infrastructure that helps developers bake privacy into their apps. Oblivious HTTP (OHTTP) is anIETF standardÂ designed to enable app backends to receive HTTP requests without seeing user IP addresses.

This fall, weâre launching the Cloudflare OHTTP Gateway. Customers will be able to enable our new OHTTP Gateway as a paid add-on to their zone and start receiving OHTTP traffic with just a few clicks. Register throughour formÂ to join our waitlist. Read on to learn more.

## Expanding our OHTTP product suite

With OHTTP, requests travel through two independently-operated hops: a relay and a gateway. An OHTTP relay blindly forwards encrypted requests in order to hide client identifiers from app servers. An OHTTP gateway performs the cryptographic work of decapsulating encrypted requests and encapsulating responses such that app servers can handle OHTTP requests as if they were plain HTTP. The separation of trust between relay and gateway is critical: it ensures that no single party sees both client identifiers and request contents.

In 2022, we launched an OHTTP relay product,Privacy Gateway. Privacy Gateway enables our customers to offer more privacy-preserving experiences to their users. For example, Flo Health uses OHTTP for their appâsAnonymous Mode, and AppleâsPrivate Cloud ComputeÂ uses OHTTP to disassociate AI inference requests from user identities. But customers who are already protecting their servers behind Cloudflare canât also use a Cloudflare-operated relay â they need an OHTTP gateway instead.

![](/images/posts/c6dbe67a41b5.jpg)

In our experience running OHTTP relays, weâve seen how difficult it can be to build and operate a secure, performant OHTTP gateway at scale. Today, weâre launchingÂ the closed beta for our self-serve Cloudflare OHTTP Gateway. Weâre also renaming ourÂ âPrivacy Gatewayâ to âCloudflare OHTTP Relayâ to better distinguish the two products.Â

Now, customers who want an OHTTP architecture with the necessary separation of trust have two options:

1. Use Cloudflareâs OHTTP Relay (formerly Cloudflare Privacy Gateway) and run your gateway yourself. This is best if your application servers are hosted off Cloudflare, and youâre able to run your own OHTTP gateway.
2. Use Cloudflareâs new OHTTP Gateway with a third-party relay. This is best if your app servers are already behind Cloudflare (on our CDN or Workers, for example), if youâre accepting OHTTP requests from a third party (like AppleâsLiveCallerID), or if you want a managed gateway to minimize latency and operational overhead. Â

Weâre working to raise the bar for privacy across the Internet, and we believe that protocols like OHTTP can help â if we make them easy enough to adopt. Itâs always been our goal to expand our OHTTP product suite and make our trusted privacy infrastructure accessible to a broader swath of the Internet.

## Why we built the Cloudflare OHTTP Gateway

SinceÂ we launched our OHTTP Relay product,Â weâve observed a few things.

First, weâve seen that there's a growing appetite among developers for accessible, usable privacy infrastructure. Developers of privacy-oriented apps want to bake network privacy into their applications by default, but doing so remains harder than it should be. Â

Second, weâve learned that building and operating an OHTTP gateway can be tough for customers. Any proxying architecture introduces some latency because requests must travel an extra hop or two around the Internet. Combine that with the cost to decrypt requests and encrypt responses, and the latency hit of a homegrown OHTTP setup can be significant. Weâre well-positioned to solve this problem: the same building blocks that enable us to operate fast, reliable privacy infrastructure for products like1.1.1.1Â andiCloud Private RelayÂ make us a good home for an OHTTP gateway. Because of CloudflareâsanycastÂ approach, our OHTTP Gateway will run on every server on Cloudflareâs global edge network, minimizing latency in relay-to-gateway hops. If you use our CDN, user requests can be decrypted by our Gateway and resolved by your app servers on the same Cloudflare metals, saving gateway-to-origin latency.

Finally, recall that OHTTPâsprivacy modelÂ requiresÂ that the relay and app server be operated by separate, non-colluding parties. We want to provide our customers with the best possible range of options for their privacy infrastructure. Before, developers who protected their app servers behind Cloudflare werenât able to use our OHTTP Relay, because Cloudflare would see both client metadata and the decrypted contents of requests, breaking OHTTPâs privacy model. Now, developers can choose whether a Cloudflare OHTTP Relay or Gateway is a better fit for their architecture.

## A primer on OHTTP

A typical interaction between a client and application server reveals information about the client. When a client and app server talk to one another, the app server learns the clientâs IP address because each packet in which data is sent is labeled with a source IP â similar to the âfromâ label on an envelope. App servers can also âfingerprintâ a client based on attributes like supported TLS versions or cipher suites. These signals make it possible for app servers to link multiple requests back to the same user.

But what if I wanted to build an app that really doesnât know much about my users? For example: Flo Health wanted to build anAnonymous ModeÂ to enable users to access personal health data without it being linkable to possible user identifiers. Â

OHTTP introduces a proxy, called a ârelay,â that forwards requests and responses between client and app server to obfuscate the clientâs identity from the app server. The relay sees client identifiers like IP address and TLS fingerprint, but strips themÂ before forwarding on requests. This prevents app servers from linking multiple requests back to the same user, and means that request contents canât be associated with the userâs IP address.

For example, a regular client-server exchange might reveal the following information about a client:

```
- ipAddress: 192.0.2.33 # the clientâs IP address 
- ASN: 7922
- tlsCipher: AEAD-CHACHA20-POLY1305-SHA256 # potentially unique
- tlsVersion: TLSv1.3
- Country: US
- Region: California # the client's location
- City: Campbell
```

A request first sent through an OHTTP relay would reveal only the relayâs information to the app server receiving the request:

```
- ipAddress: 128.62.37.13 # the relay's IP address & fingerprint 
- ASN: 18 
- tlsCipher: AEAD-AES-128-GCM-SHA256 
- tlsVersion: TLSv1.3 
- Country: US
- Region: Texas  # the relay's location
- City: Austin
```

This means that for each request, the app server doesnât learn the location and TLS fingerprint of the end user. Plus, if many different users are sending requests through the relay, the app server wonât be able to distinguish which requests are coming from whom, limiting their ability to trace app activity back to a single end user. This creates a strong privacy boundary.

[翻译失败，原文如下]

What really differentiates OHTTP from a basic forwarding proxy, however, is the encryption of data between client and app server. Requests and responses are encapsulated using Hybrid Public Key EncryptionÂ (HPKE)Â such that only the client and app server can see plaintext, and the relay sees only a jumble of ciphertext. A âgatewayâ sits between the relay and app server to handle all of this cryptography â decapsulating requests, encapsulating responses â and the app server handles only plain HTTP. Â

This creates a âdouble-blindâ privacy model: the relay sees only client identifiers; the gateway and app server see only request contents; no party sees both.

![](/images/posts/b8ce46a46ed9.jpg)

## How we built the OHTTP Gateway

In building our OHTTP gateway-as-a-service, our goal is to bring our secure, performant privacy infrastructure to a broader swath of the Internet. Performance and easy onboarding are critical. So, we built our GatewayÂ as a flexible service deployed across our global network. With just a couple of clicks, you can enable the Gateway on your zone and start sending OHTTP tohttps://your-zone.com/.well-known/ohttp-gateway. Weâll scale the service up and down automatically, so you donât need to worry about capacity.

We had a few other user needs in mind, informed by the pain points weâd seen OHTTP Relay customers run into when operating their own OHTTP gateways.

First: We wanted to abstract away as much of the complexity of OHTTP as possible for your app servers. We wanted developers to be able to start receiving OHTTP while continuing to accept regular HTTP traffic if they chose. So, we designed the Gateway as a feature of yourÂ zone, where clients sendwell-formattedÂ OHTTP requests to a/.well-known/ohttp-gatewayÂ endpoint on your zone. We support both standard andchunked OHTTPÂ â and we recommend using chunked OHTTP for better performance, because it enables us to process requests incrementally (in âchunksâ).

Our Gateway service will intercept each request, decrypt it, issue a subrequest to your app server, and return an encrypted response to the client. All non-OHTTP requests will travel to your server without invoking the Gateway.

Binding your Gateway to your zone also enables us to protect your Gateway from abuse. A client sending requests to your zone `example.com` may send to `foo.example.com` or `bar.example.com`, but notwikipedia.com. Without you needing to worry about it, this prevents unauthorized clients from using your zone as a way to target other domains.

Second: Seamless key management is critical.Â Gateways need to maintain a public HPKE key configuration to enable clients to encrypt requests, but managing keys securely is a challenge. So, we designed the Gateway to fully manage all keys for customers, and to serve public keys as responses to GET requests to Â/.well-known/ohttp-gateway. For stronger privacy, clients can download keys over a different IP than they request the gateway.

Third: Gateways need to be able to authenticate relays. Because the Gateway (by design) knows very little about the client sending a given request, it places trust in the relay to authenticate clients and forward traffic responsibly. But how do you ensure that only trusted relays can send traffic to your gateway?

We designed the Gateway such thatÂCloudflare Access, Cloudflareâs zero trust network access product, runsbeforerequests are decrypted, enabling you to use any standard AccesspoliciesÂ to authenticate incoming traffic and protect your Gateway from abuse. Options include mutual TLS, static service credentials, and custom external logic.

Finally: Mistakes happen, and we anticipated that customers might accidentally break OHTTPâs privacy model by running both their relay and gateway on Cloudflare. So, to preserve OHTTPâs separation of trust and ensure that Cloudflare never seesbothclient identities and decrypted inner requests, our Gateway will refuseÂto decrypt requests sent from Cloudflare Workers or from proxied hosts on Cloudflare.

## When is the OHTTP Gateway a better fit than the OHTTP Relay?

If you want to use Cloudflareâs OHTTP product suite, but youâre wondering why youâd pick Cloudflareâs OHTTP Gateway instead of the OHTTP Relay, here are a couple of considerations.

First, do you want your app servers on Cloudflare â behind our CDN or built on Workers, for example? If so, the OHTTP Gateway is a better fit to ensure adherence to OHTTPâs privacy model.

Second, whatâs your use case? If you want to receive OHTTP requests from a third-party client and relay â to useÂ AppleâsLiveCallerIDÂ SDK, for example â then the OHTTP Gateway is likely the better solution for you. Â

## Getting started

If you have a feature request or would like to register for our waitlist, so we can notify you when the product launches,sign up here.

Then, youâll need to implement an OHTTP client. Seeohttp.infoÂ or oursample client libraryÂ for some examples to help you get started. One flag as you build the client: OHTTP provides privacy at the network level, and doesnât touch the inner request body. So, to preserve user privacy, itâs up to you not to send identifying information (e.g. a userâs email address or username) in the request body.

Next, youâll need to bring your own relay. Relays can run on any infrastructure provider, and theyâre simple: hereâs somesample code. The challenge and the reason you might want a dedicated OHTTP relay provider, is to verifiably promise to your users that you wonât inspect logs with client identifiers. Otherwise, youâd be able to correlate clients at the relay with decrypted requests at your app servers. Â

Finally, once your OHTTP deployment is live, check out ourpvcli clientÂ to help with testing and debugging.Weâre excited to bring accessible privacy infrastructure to developers everywhere.Reach out to usÂ if youâd like to try out the new OHTTP Gateway and raise the bar for privacy online. Â

## Related tags

Follow on Social Media

- Cloudflare
- Lara Schull

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Announcing Cloudflare OHTTP Gateway â expanding access to Cloudflareâs privacy-preserving infrastructure](https://blog.cloudflare.com/announcing-cloudflare-ohttp-gateway/)
> 
> 翻译时间：2026-10-05 08:02
