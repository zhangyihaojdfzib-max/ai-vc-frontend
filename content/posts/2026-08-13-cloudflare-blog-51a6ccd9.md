---
title: Certificate Transparency Monitoring is now generally available
title_original: Certificate Transparency Monitoring is now generally available
date: '2026-08-13'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/certificate-transparency-monitoring-ga/
author: ''
summary: '[翻译失败，原文如下]


  Since we launchedCertificate Transparency Monitoring in public betain 2019, we''ve
  been emailing subscribers whenever a new TLS certificat...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-19T03:07:51.329433'
---

[翻译失败，原文如下]

Since we launchedCertificate Transparency Monitoring in public betain 2019, we've been emailing subscribers whenever a new TLS certificate appears in a publicCertificate Transparency(CT) log for one of their domains. Today, it's turned on for more than 650,000 customer domains. It's an early warning that someone, somewhere, has issued a certificate for a hostname in your zone, giving you a chance to spot a mis-issued certificate early.

It's a useful signal, but it had a noise problem, and we felt it ourselves. Cloudflare issues a large volume of certificates on your behalf: Universal SSL renewals, certificates from Advanced Certificate Manager, and backup certificates. All of them are logged to public CT logs by design, because a certificate that isn't logged won't be trusted by major browsers like Google Chrome and Apple's Safari. So the same transparency that lets you monitor for mis-issuance also surfaces every certificate we issue for you.

And issuance isn't a one-time event. Certificates are short-lived and renew automatically: a single Universal SSL certificate canrenew as often as every 60 days, up to about six times a year. That cadence is set to increase, with theCA/Browser Forumhaving voted to cut the maximum certificate lifetime to 47 days by 2029, multiplying the routine renewals that flow through those logs. Every one of those renewals generated an alert. But at the scale Cloudflare issues certificates, a genuinely suspicious one could look just like a routine renewal, and the alert that mattered was easy to miss.

We heard the same thing from customers. On our community forum, one described disabling the feature across all their sites because they were "tired of regularly getting spammed with tons of completely normal certificate renewals," adding "I wasn't even actually reading them by the end." That noise came from Cloudflare's own certificates.

Today, we're changing that. Certificate Transparency Monitoring now filters out the certificates Cloudflare issued on your behalf before an alert is sent. The alerts that reach your inbox are the ones that deserve your attention: a certificate you didn't expect, that Cloudflare didn't issue. With that fix in place, Certificate Transparency Monitoring is generally available.

## Filter out the certificates Cloudflare manages

The goal is to identify and eliminate noisy alerts for routine, Cloudflare-managed certificate issuances and renewals while ensuring we catch all external certificates managed outside our system.

### Why couldn't we just identify and filter these out previously?

There are two independent systems built to serve separate products: certificate management, which deals with internal certificate issuance data, and CT alerting service, which parses data from public CT logs.

![Before: separate issuance and alerting flows](/images/posts/822e6feb5122.jpg)

The two flows handle the same certificate, but never at the same moment and never with the same information. When the alerting flow is deciding whether to email you, all it has is what it pulled from the log. It has no signal from the issuance flow saying "the ordering service just created this one." That missing link was the problem.

### What is the lifecycle of a certificate?

As shown above,certificate issuancehappens in two stages:

1. Certificate Authority (CA) creates a pre-certificate, writes to logs and receivesSCTs(Signed Certificate Timestamps).
2. CA embeds those SCTs into the final certificate and logs it.

Thus, the alerting service sees two log entries for a single certificate order: 1) pre-certificate and 2) final certificate. To avoid alerting twice per pair, an internal identifier calledstripped_fingerprintis storedfordeduplicationpurposes. This fingerprint is the hashed value of DER (Distinguished Encoding Rules)-encoded TBSCertificate (to be signed certificate). This value is consistent and unique for a pre-certificate/final certificate pair that belongs to the same certificate order. Therefore, this is one identifier which is already present, and it sits entirely inside the alerting flow.

### Why does the obvious fix fail?Â

The intuitive shortcut is to copystripped_fingerprintinto the ordering service so the alerter can look it up. But that doesn't work because the ordering service doesnât receive the pre-certificate, so it can't produce this value when the alerting service receives it.

![Problem: stripped_fingerprint arrives too late.](/images/posts/61319d97603f.jpg)

So even if this is used as an identifier, it can only be recorded after the final certificate is received by the ordering service. In that window between pre-cert and final cert log entries, if the alerting service looks upstripped_fingerprint(precert)inthe ordering serviceâs database,then it is not going to find any information matching this identifier to confirm that it is issued by us â and this leads to an extra alert again.

Although the certificate ordering service is the right system to answer âIs this ours?â, the match key with which this information was being uniquely identified is not winning the race. So the problem reframed itself. The question was no longer where to store the fingerprint, but what is that one identifier which can be persisted from order creation to the final logged certificate.

### What is the right key?

The right key had to check these boxes:Â

1. Early: recorded before anything reaches the log, i.e., present at key generation.
2. Consistent: throughout all stages from pre-certificate to final certificate.
3. Reproducible: the CT alerting service can recompute it independently, from the log entries alone.
4. Unique: to each certificate order.

Thepublic keyis one such identifier that checks all those boxes. It travels inside a structure calledSubjectPublicKeyInfo(SPKI).

![Solution: SPKI stays consistent and reproducible](/images/posts/305abe3f8531.jpg)

Consistency: As the diagram above shows,SubjectPublicKeyInfo(SPKI) is present from the first step and stays the same through the CSR (Certificate Signing Request), pre-certificate, and final certificate.Â

Uniqueness and Safety: Cloudflare generates a fresh keypair for every issuance, so the public key is effectively unique. Since only Cloudflare has the private key, a certificate with a matching SPKI must have come from a Cloudflare issuance only. A collision is astronomically unlikely, and no outsider could create a valid signing request without the private key.Â

So the identifier we record isspki_sha256â an SHA-256 hash of the DER-encoded SPKI, a short fixed-length value that's cheap to index. The ordering service computes it straight off the CSR and writes it at key generation, before issuance begins.

### How do both flows agree on the value?

Recording the key early solves this in the certificate ordering. With that in place, the alerting flow performs an extra step. When the alerter sees a log entry, it recomputesspki_sha256from the certificate's public key and looks it up to see if the ordering service has recorded this value in its database â on:

- Matchâ the ordering service recorded this key, so the certificate is ours. Suppress the alert.
- Nomatchâ key not found âÂ  alert, exactly as before.

Because the key is identical in the pre-certificate and the final certificate, it no longer matters which one arrives first.

![After: known Cloudflare certificates are filtered](/images/posts/127376ef886e.jpg)

Three things follow, all toward less noise:

[翻译失败，原文如下]

- Certificates we manage no longer alert you. Universal SSL, Advanced Certificate Manager, Total TLS, and Backup Certificates all match a recorded key and pass silently.
- Abandoned pre-certificates no longer alert you. Sometimes a pre-certificate is logged but issuance never completes. Those alerts used to look like unexplained certificates; now they match a record and stay quiet. The event is still recorded on our side; we just don't email you about something we already know is ours.
- Custom certificates you upload still alert you. We didn't generate those keys, so there's no record on the issuance side and nothing to suppress. That's exactly the case CT monitoring and alerting exists for, and it's untouched.

Most of the work here wasn't writing the fix; it was understanding both flows well enough to see that the key connecting them was a field we'd been carrying the whole time. Once we picked the identifier that's early and shared, the rest was bookkeeping.

CT alerting should fire only on issuance we can't account for. With this change, it does.

## Alerts are now easier to review

Updated emails identify the affected hostname in the subject line, include certificate details in the message, and link to the certificate in the Cloudflare dashboard, so you can review it and take action as needed.

![Screenshot of alert email](/images/posts/e042a1c73b1d.jpg)

## What's next

We plan to bring Certificate Transparency Monitoring toCloudflare Notifications. This would let teams route CT alerts to webhooks, PagerDuty, or additional email destinations, just as they manage other Cloudflare alerts, instead of relying on todayâs email-only channel.

## Try it

Already using Certificate Transparency Monitoring? There is nothing you need to do. Filtering is already enabled. Starting today, you will only be notified of certificates issued outside of Cloudflare's automated systems.Â Â

Not using it yet? In theCloudflare dashboard, go to SSL/TLS â Edge Certificates â Certificate Transparency Monitoring and turn it on. Available on every plan at no extra cost, with unified settings across plan tiers, so you can manage alert recipients in one consistent view.

![Screenshot of CT monitor setting](/images/posts/106f0db487dc.jpg)

If you have thoughts on how Certificate Transparency Monitoring should evolve, let us know through your account team or theCloudflare Community. That input will shape the customization controls we build next.

- Cloudflare

---

> 本文由AI自动翻译，原文链接：[Certificate Transparency Monitoring is now generally available](https://blog.cloudflare.com/certificate-transparency-monitoring-ga/)
> 
> 翻译时间：2026-08-19 03:07
