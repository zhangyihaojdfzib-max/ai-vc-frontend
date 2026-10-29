---
title: Introducing the Cloudflare PHP Capture the Flag challenge
title_original: Introducing the Cloudflare PHP Capture the Flag challenge
date: '2026-10-27'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/php-ctf/
author: ''
summary: '[翻译失败，原文如下]


  Last week was one for the Internet security history books. First,eight eMudhra intermediate
  certificates were compromised, creating the p...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-29T08:15:44.397519'
---

[翻译失败，原文如下]

Last week was one for the Internet security history books. First,eight eMudhra intermediate certificates were compromised, creating the possibility of forged certificates that could be used to impersonate servers. Then camephp2shell: serious vulnerabilities in PHP, the runtime behind a large portion of the Web.

Cloudflare worked around the clock as these events unfolded to protect our customers and help protect the Internet. We shipped client updates andmultiple mitigations, updated our web application firewall (WAF) with new rules to block attackers from exploiting the PHP vulnerabilities, and introduced a new feature calledfull transaction detection.

As always in situations like this, these new capabilities were made available on all plans, including Free.

## Put our WAF to the test

Protecting systems from vulnerabilities like these is always an ongoing process, not a one-time event. The widespread adoption of AI allows attackers to discover new vectors with unprecedented speed and efficiency, so collecting real-world data to test our assumptions and strengthen defenses is essential.

Thatâs why today we're launchingÂ theCloudflare PHP Capture the Flag challenge, run through ourBug Bounty program. We've put a deliberately vulnerable PHP installation behind our WAF, and we're inviting security researchers on HackerOne to try to bypass the protections and capture a flag.

## How this Capture the Flag (CTF) works

We are keeping this simple. The challenge focuses onCVE-2026-109618Â andCVE-2026-109619, the two PHP vulnerabilities behindphp2shell. The target runs stockPHP 8.5.11Â (with standard PHP extensions), Apache 2 (via mod_php), and an empty index.php inside aCloudflare Container, with our default WAF protection rules for these vulnerabilities enabled in front of it. Inside the sandbox is a file called/flag.

The sandbox is reset every few minutes, including the flag file.

![](/images/posts/b39ac3797b24.jpg)

Your mission, should you choose to accept it:bypass the WAF protections, exploit the PHP sandbox, and recover the contents of /flag. You can use your own research tools. Thechallenge pageÂ has the environment details, scope, and flag verification form.

## Challenge requirements

ThisÂ limited-time challenge is run viaCloudflare's Bug Bounty program on HackerOne. All aspects of this challenge are subject to HackerOnetermsÂ and the Cloudflare HackerOneprogram rulesÂ the (âBounty Termsâ). If you find an eligible bypass, you must follow these requirements in order to claim the bounty:

1. All participants must sign up for a HackerOne account and review and agree to the BountyÂ TermsbeforeÂ participating in the CTF.
2. Demonstrate attacker-controlled PHP code or command execution inside the sandbox through an authorized POST request.
3. Use that remote code execution (RCE) to recover the current contents of /flag, then successfully verify the flag throughthe CTF user interfaceÂ (UI). Verify promptly before a reset; retain the successful result for later review.
4. Submit a private report to Cloudflare on HackerOne. Include PHP CTF in the title and provide:The endpoint, complete payload, and request sequence, preserving relevant headers, encoding, and body bytes.Raw request/response captures or a readable proof of concept sufficient to reproduce the full chain.An explanation of the WAF bypass, executed code or command, and how that execution recovered /flag.The attempt ID, successful UI verification result, and exploit/verification UTC timestamps. Include the flag privately if needed for verification.What makes the method or payload materially distinct, and related submissions you know about.

1. The endpoint, complete payload, and request sequence, preserving relevant headers, encoding, and body bytes.
2. Raw request/response captures or a readable proof of concept sufficient to reproduce the full chain.
3. An explanation of the WAF bypass, executed code or command, and how that execution recovered /flag.
4. The attempt ID, successful UI verification result, and exploit/verification UTC timestamps. Include the flag privately if needed for verification.
5. What makes the method or payload materially distinct, and related submissions you know about.

UI verification does not submit aHackerOneÂ report or establish reporting priority. File disclosure without RCE, RCE without successful flag recovery and UI verification, local-only exploits, rediscovery of the known PHP vulnerabilities, and WAF detection differences or partial chains without the full objective are not eligible.

Awards require amaterially distinct Firewall (WAF) bypass method, even for the same PHP CVE. Reports using thesame Firewall-bypass mechanism are duplicates, regardless of differences in the PHP exploit, payload, RCE technique, or flag-recovery method. New flags, resets, attempt IDs, or cosmetic changesâincluding equivalent encodingsâdo not qualify as unique. Equivalent submissions are duplicates even if unfixed; only the first complete, reproducible HackerOne report is considered. Cloudflare makes final duplicate and reward decisions.

We record attempted metadata and request payloads to help analyze reports, so please use test data only. Do not send credentials, personal information, or anything else you would not want included in a research record. ReadÂ Cloudflareâsprivacy noticeÂ before testing.

Testing is authorized only against the challenge hostname's WAF-protected/php/*Â endpointsÂ (POST method only). Other Cloudflare services, direct access to the underlying infrastructure, the upstream PHP project, and third-party systems are out of scope. No denial of service, high-volume scanning, persistence, social engineering, or attacks on other participants. If you get a 429 or 503, back off.

In the event of any conflict between this blog post and the Bounty Terms, the Bounty TermsÂ shall prevail.

Cloudflare reserves the right to suspend or terminate this challenge at any time. Once the competition is removed from HackerOne, it is officially terminated, so please refer to the Cloudflare HackerOne page for the most up-to-date information on whether this challenge remains open.

## Not a substitute for patching

Our WAF protects you, but it is not a replacement for fixing vulnerable software. Response blocking can prevent exposed data from reaching an attacker, but it cannot undo actions already performed at the origin. If you run PHP, follow thelatest PHP security advisoriesÂ and apply the relevant updates.

Last week was a reminder that helping build a better Internet often takes many peopleâresearchers, maintainers, and teams across the industryâdoing difficult, urgent work together.

We hope this challenge gives everyone a useful way to join in. Head over tophp-rce.cloudflare.appÂ if you want to participate: the flag is there, and we'd like to know if you can get it.

## Related tags

Follow on Social Media

- Cloudflare
- Celso Martinho
- Sven Sauleau

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Introducing the Cloudflare PHP Capture the Flag challenge](https://blog.cloudflare.com/php-ctf/)
> 
> 翻译时间：2026-10-29 08:15
