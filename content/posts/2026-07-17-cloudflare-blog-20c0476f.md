---
title: Cloudflare WAF protects WordPress applications from two high-severity vulnerabilities
title_original: Cloudflare WAF protects WordPress applications from two high-severity
  vulnerabilities
date: '2026-07-17'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/wordpress-vulnerabilities/
author: ''
summary: '[翻译失败，原文如下]


  Cloudflare has deployed new Web Application Firewall (WAF) protections for two critical
  vulnerabilities affecting WordPress. The protecti...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-07-25T05:00:43.264704'
---

[翻译失败，原文如下]

Cloudflare has deployed new Web Application Firewall (WAF) protections for two critical vulnerabilities affecting WordPress. The protections address an Unauthenticated Remote Code Execution (RCE) vulnerability in WordPress's REST API and a related SQL Injection vulnerability.

The WordPress security team disclosed the vulnerabilities to Cloudflare before public release so that we could prepare protections for customers.Cloudflare has deployed the new rules to protect all customers, including those on free and paid plans, as long as their application traffic is proxied through the Cloudflare WAF.The rules were deployed at 17:03 UTC on July 17 2026.

WAF protections reduce exposure while customers update, but they are not a substitute for patching. WordPress has released fixes in version 7.0.2, with backports to affected earlier branches: 6.9.5, 6.8.6, and 7.1 Beta 2 (see release details). Versions earlier than 6.8 are not affected. WordPress is treating this as its highest-severity, highest-priority class of issue and is forcing automatic updates to affected sites, so most sites will be updated automatically. We still recommend confirming that you are on a patched release or the backports for your branch and follow the guidance in the official WordPress security releaseannouncement.Â

### What you need to know

The vulnerabilities affect different parts of the request path:

- CVE-2026-60137: SQL injection.A vulnerability in WordPress version 6.8 and later allows crafted input to alter a database query. Rating High.
- CVE-2026-63030: Unauthenticated remote code execution.A vulnerability in WordPress version 6.9 and later allows an unauthenticated attacker to execute code through the batch endpoint of the REST API when a persistent object cache is not in use. This vulnerability is related to the SQL injection described above. No login or user interaction is required to exploit this vulnerability. Rating Critical.

The SQL injection vulnerability is present from version 6.8 onwards, while the RCE only affects versions from 6.9. So 6.8.6 addresses the SQLi only since the RCE isn't present on 6.8, while 6.9.5, 7.0.2, and 7.1 Beta 2 get fixes for both.

Cloudflare created two rules to detect requests associated with these vulnerabilities:

Rule description

Rule ID for Managed Ruleset

Rule ID for Free Ruleset

Default action

Wordpress - SQL Injection - CVE:CVE-2026-60137

CVE-2026-60137

1c060d3a371549219ee290d7ed933fcc

db003b39b7774859a8d588ce33697a1a

Block

Wordpress - Remote Code Execution - CVE:CVE-2026-63030

CVE-2026-63030

7dfb2bd4708d4b88b9911dc0550664b6

ebd3f2df15c74ddcbf6220c9b5ec246a

Cloudflare customers running WordPress sites on Pro, Business, or Enterprise plans should ensure that Cloudflare Managed Rules are enabled. Customers can follow the steps in ourWAF Managed Rules documentation. Customers on free plans are automatically protected through the Free Ruleset.

The new rules are deployed with the default Managed Ruleset action of Block. Customers running WordPress sites should review any ruleset-level overrides, including those that change all rules from Block to Log, and ensure the new rules use the recommended action while they update WordPress. Cloudflare customers should also monitor Security Events for requests matching either rule.Â

### Defense in depth while you patch

The SQL injection rule detects crafted parameter values before they reach WordPress. The unauthenticated RCE rule targets requests attempting to reach the remote code execution path. Together, they detect the attack at two different points.

These rules reduce risk while organizations update affected systems; they do not fix the underlying vulnerable code. Updating WordPress remains the most effective way to address the vulnerabilities.If an immediate update is not possible, verify that both Cloudflare rules are active with the recommended action and review logs for suspicious requests to the affected REST API endpoint.

### Looking forward

Cloudflare will monitor matching traffic and test the rules against new attack variations, updating detections when needed.

We thank the WordPress security team for coordinating with Cloudflare and other infrastructure providers to help protect users before details of the vulnerabilities became public.

![](/images/posts/eef42146850a.jpg)

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Cloudflare WAF protects WordPress applications from two high-severity vulnerabilities](https://blog.cloudflare.com/wordpress-vulnerabilities/)
> 
> 翻译时间：2026-07-25 05:00
