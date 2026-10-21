---
title: 8 eMudhra certificates are compromised. Here's what you need to know
title_original: 8 eMudhra certificates are compromised. Here's what you need to know
date: '2026-10-20'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/emudhra-certificate-compromise/
author: ''
summary: '[翻译失败，原文如下]


  OnÂ October 19, 2026, at approximatelyÂ 17:00 UTC, Cloudflare became aware that
  private keys associated with eight eMudhra intermediate c...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-21T06:58:06.605165'
---

[翻译失败，原文如下]

OnÂ October 19, 2026, at approximatelyÂ 17:00 UTC, Cloudflare became aware that private keys associated with eight eMudhra intermediate certificates were compromised. These certificates were widely trusted by browsers, operating systems, and also within Cloudflare. Because the keys themselves are weak, an attacker can create a forged certificate for any domain and use it to impersonate servers to intercept or modify traffic. This is a serious security incident with implications across the Internet. For reference,here is a linkÂ to more information about how SSL certificates work and why they are so critical to the operation of the Internet.

We immediately prioritized patching critical services across Cloudflare to protect our customers ahead of the public disclosure of the vulnerability. Our security review has not identified active exploitation of this issue on Cloudflare services.

We have released updates for the Cloudflare One Clients, also known as WARP or the 1.1.1.1 app, and Cloudflare Tunnel, also known as cloudflared. We have also deployed mitigations across our CDN, Developer, and Zero Trust products. If you are using Cloudflare Zero Trust with Gateway and an up-to-date client (see below), you are automatically protected.

## Our response

We prioritized updating services that use public certificates to authenticate remote endpoints, including proxies connecting to origins and applications calling external APIs. In parallel, we updated shared trust stores, base images, and other shared foundations, providing a common mitigation path for services that inherit their certificate trust from those sources. We paired these updates with reloads, restarts, and image deployments needed to activate them. Applications with bundled or custom trust stores received separate assessment and updates. This work addresses certificate-based authentication, not a weakness in TLSâs encryption algorithms.

Teams across Cloudflare are presently working on further remediation. We are making progress, but there's much work still to be done.Some customers will need to take action on software or trust configurations that they operate, especially on their origin servers.Â The recommended actions are summarized below.

## What customers should do

Cloudflare One Client: Upgrade to: v2.5.6 (Android), v1.12.16 (iOS),Windows Desktop (2026.8.2115.0),macOS (2026.8.2115.0),Linux (2026.8.2115.0)

1.1.1.1 app: Upgrade to: v6.38.10 (Android), v6.31.7 (iOS),Windows Desktop (2026.8.2115.0),macOS (2026.8.2115.0),Linux (2026.8.2115.0)

Customers using Cloudflare Containers, including Sandboxes, should review their container images and application dependencies for affected certificate trust stores and apply updates based on your deployed image.

Customers can also enableHTTPS egress interceptionÂ to route outbound HTTPS requests through Cloudflare, moving remote-server certificate validation from the application to Cloudflare-managed infrastructure. This allows Cloudflareâs trust-store mitigations to protect intercepted connections. Containers that have this enabled are already protected.

## Developer guidance

For developers, look beneath the SDK.

An API client may delegate certificate verification to an HTTP library, a language runtime, the operating system, or a custom trust configuration. Updating the SDK alone may not change the underlying policy.

Once you patch, you may notice certificate errors in your dashboards.It's important to not resolve these errors by disabling verification.That would remove the authentication protection these updates are intended to restore.

This incident affects many software stacks that rely on the WebPKI for authentication. Mozillaâs Dennis Jackson has crowdsourceda list of commonly used packagesÂ that have been patched.Â We advise readers to upgrade as soon as possible. (Note that some of these may be indirect dependencies of your software stack, so look at the dependency tree.) Apply the relevant dependency updates, rebuild affected images, and confirm whether applications require a reload, restart, or redeployment.

Dennis Jacksonâstest siteÂ providesÂ browser checks, non-browser testing instructions, and package update information. Results apply to the verification path being tested, not every application on the device. Validate through the applicationâs actual TLS path. A successful browser test does not prove that a background service is protected. Neither does a curl test if the application uses a different verifier.

## Timeline

The timeline of events so far is below.

Date and Time

Event

October 19, approximately 17:00 UTC

Cloudflare becomes aware of the compromise and begins assessment.

October 20, 02:00 UTC

Cloudflare One Client and WARP app security updates published across platforms (except Cloudflare One Agent on iOS, for which app review is still pending).

October 20 09:15 UTC

Cloudflare Tunnel (cloudflared) security update published.

October 20 19:20 UTC

CDN and server-side Zero Trust mitigations fully deployed.

## Looking forward

The impact of this incident is not felt equally. Browser maintainers were able to remediate the issue with a flip of a switch. They of course have justoneÂ application to update, instead of hundreds, but they do have a neat trick up their sleeves: most browsers use quick-revocation mechanisms (like Chrome CRLSets). At Cloudflare we also use such a mechanism for some of our products. To bring it to more systems at Cloudflare and industry, weâre excited about projects likeupkiÂ that understand a trust store canât be a static list of root certificate authorities, but needs the ability to be quickly updated with information like revocation and certificate transparency keys.

## Related tags

Follow on Social Media

- Cloudflare
- Bas Westerbaan

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[8 eMudhra certificates are compromised. Here's what you need to know](https://blog.cloudflare.com/emudhra-certificate-compromise/)
> 
> 翻译时间：2026-10-21 06:58
