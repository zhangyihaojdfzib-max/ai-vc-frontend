---
title: 'Follow the thread: a new dashboard to investigate account abuse'
title_original: 'Follow the thread: a new dashboard to investigate account abuse'
date: '2026-10-02'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/account-abuse-protection-dashboard/
author: ''
summary: '[翻译失败，原文如下]


  Traditionally, preventing online fraud relied on point-in-time proof of identity:
  enter the correct password, complete a biometric verifi...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-05T08:02:29.365849'
---

[翻译失败，原文如下]

Traditionally, preventing online fraud relied on point-in-time proof of identity: enter the correct password, complete a biometric verification, or pass a liveness check, and gain access. To defeat these controls, fraudsters had to steal credentials and other identity evidence from a real user, which was difficult to execute and scale. Today, widespread access to AI enables fraudsters to fabricate or imitate legitimate identities by combining exposed credentials with synthetic media designed to evade identity verification. Consequently,Â identity checks are no longer sufficient as they capture a moment in time. Even when someone passes a check, it does not mean the account itself can be trusted.

OneÂ convincing interaction can be faked. A consistent pattern of legitimate behavior is much harder to manufacture.Â Modern fraud prevention must move beyond stateless decisions toward a stateful trust model. Traditional identity verification asks, âCan this person pass the check right now?â A stateful approach additionally asks, âDoes it fit what we know about this account and its established behavior?â At Cloudflare, trustÂ is continually earned and reassessed at each interaction against historical behavioral, network, and device patterns.

Cloudflareâs Account Abuse Protection (AAP) creates stateful account overviews to help website owners detect and investigate abuse across login and signup activity. Customers configure an identifier from their existing login or signup flow, such as an email address, username, or phone number. Cloudflare cryptographically hashes that value to create a privacy-preserving, per-domainHashed User ID. Within AAP, a Hashed User ID represents an account and anchors its activity. With each login or signup, AAP adds the event and relevant network and device signals observed at Cloudflareâs edge. Over time, this accumulated history establishes context for the accountâs typical behavior, making meaningful deviations easier to identify and giving fraud teamsÂ (i.e., the designated personnel for Security Intelligence, Investigations, Trust & Safety, or Risk & Compliance) a stronger foundation for investigation.

Today, we are introducing a new fraud dashboard for Account Abuse Protection, available first to Early Access customers. The workspace brings together account overviews built from activity observed across a websiteâs configured login and signup flows. It allows fraud analysts to view their entire user population, identify suspicious trends, and move from aggregate activity patterns into specific account investigations.

## Dashboard overview: From population visibility to individual account depth

The dashboard is designed as an investigative funnel. When a suspicious event has been identified, fraud teams can review the account population overview to understand the scale and shape of suspicious patterns without needing to investigate every account individually.

Teams can review total login and signup volume, see how many accounts generated those events, and view the unique IP addresses and devices observed across those accounts. Country and ASN breakdowns provide additional context about where the activity was observed.

The account population overview helps fraud teams answer questions such as:

- Did login or signup volume change unexpectedly?
- Are failed logins or leaked credential matches increasing?
- Which accounts show the highest login failure rates?
- Are events concentrated in particular countries, ASNs, or times of day?
- Did a sudden signup increase coincide with shared characteristics?
- Which accounts may have been affected by the attack?

From there, fraud teams can determine the campaignâs scope, prioritize accounts for manual review, reconstruct what happened within those accounts, and decide how to respond.

![](/images/posts/0599e0095227.jpg)

### AAP in Action: Investigating a credential stuffing attack

Consider a fraud prevention or security analyst team investigating unusual login activity. The team opens the Account Abuse Protection dashboard to determine how broadly a credential stuffing attack may have affected its users. The dashboard allows analysts to investigate from total event traffic all the way to individual accounts that warrant review. The individual account view provides the history and context needed to reconstruct what happened and determine the appropriate response.

1. Spot the anomaly. The investigation begins in the account population overview, where the fraud team determines whether suspicious activity is isolated or part of a broader campaign. An increase in failed login activity prompts the team to examine Leaked credential check results on login events.

In this example, a leaked credential summary shows that approximately 2.4K events produced a leaked username or password result, compared with 11.7K events where credentials were classified as clean. This pattern is an investigative lead, not confirmation that every affected account was compromised.

The team can now focus on accounts associated with leaked credential matches. Are multiple accounts connected to the same IP addresses or ASNs? Does an individual account suddenly appear across an unusually high number of IP addresses? These relationships help define the potential scope of the credential stuffing campaign and identify the accounts that should be prioritized for review. Analysts can also look at the dashboard for concentration across particular IP addresses, ASNs, locations, or devices.

2. Narrow the field of investigation.Â  Filters help narrow the account population to specific accounts with the most concerning combination of signals and identify which ones warrant manual review.Â  For example, filters can be set to look at accounts with at least three failed logins, at least three leaked credential matches, and observed from at least five unique IP addresses.

![](/images/posts/401acbb4d9c6.jpg)

![](/images/posts/bbfe5640971f.jpg)

From this filtered cohort, analysts can select the specific Hashed User IDs, whose recent activity requires the most urgent attention.

3. Investigate an account.Analysts can review login attempts, identify new devices or locations, and reconstruct how activity unfolded. Using the event table, they can compare earlier clear events with later suspicious activity, pinpoint when the pattern began, and determine whether it was a single event or a series of repeated attempts. Each event includes a Ray ID that analysts can use to look up associated information in Security Events.

![](/images/posts/dae820157e6b.jpg)

4. Decide how to respond. If review confirms that an account was compromised, analysts can begin their established recovery process. They can also use the Hashed User ID in a WAF rule to challenge or block future requests associated with it.

![](/images/posts/8d3838a83b55.jpg)

### A closer look at an individual account

An individual account view provides another layer of depth for investigation. It summarizes the login and signup activity observed for that account, including its login success rate, leaked credential matches, and most frequently associated networks, locations, and devices. Analysts can then examine the individual events behind the account summary. Each event includes its timestamp, Ray ID, and any mitigation applied. A Cloudflare Ray ID is an identifier given to every request that goes through Cloudflare, that teams can use to look up associated information in Security Events.

![](/images/posts/4c9790ae5331.jpg)

This detailed summary and event log helps answer questions such as:

[翻译失败，原文如下]

- Was this a single login event or part of a series of repeated attempts?
- Did that login introduce a new country, network, IP address, or device?
- Did the userâs behavior change afterward?
- What happened before and after a suspicious event?
- Did concentrated login activity follow shortly after signup?
- Did signup and subsequent login activity use different network or device characteristics?

Viewed together, these signals help fraud teams determine whether an account requires recovery, restricting access, or another response, depending on how the customer wants to treat these accounts. When there is enough evidence, analysts can use the Hashed User ID in a WAF rule to challenge or block future requests associated with that identifier.

### Designed to minimize unnecessary data exposure

Account Abuse Protection provides account level context while also giving Cloudflare customers control over who can access account information. This launch introduces two new rolesÂ (i.e., access levels): Account Abuse Protection and Account Abuse Protection PII. The Account Abuse Protection role controls access to the dashboard, while the Account Abuse Protection PII role controls access to additional account-level PII (e.g., email) . We encourage Customer Administrators to assign these roles on a need-to-know basis, based on what each team member needs to investigate.

The Account Abuse Protection PII role is also required to create or update Logpush jobs containing PII.Â Separating these permissions helps customers apply least privilege access to both dashboard and data export workflows.

### Take the next step in account protection today

The new dashboard is available first to Account Abuse Protection Early Access customers. Bot Management Enterprise customers interested in these capabilities cansign up for Early Access.Â Prospective Bot Management Enterprise customers can use the same form to contact our team.

Bot detections help customers understand whether activity is automated. Account Abuse Protection adds account level overview to help fraud teams investigate whether login and signup activity appears authentic and consistent with legitimate use. Together, these capabilities help website owners address automated and human-driven abuse across account creation and login.

- Cloudflare

---

> 本文由AI自动翻译，原文链接：[Follow the thread: a new dashboard to investigate account abuse](https://blog.cloudflare.com/account-abuse-protection-dashboard/)
> 
> 翻译时间：2026-10-05 08:02
