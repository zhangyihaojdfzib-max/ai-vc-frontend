---
title: Internet traffic and attacks during the 2026 U.S. midterm elections
title_original: Internet traffic and attacks during the 2026 U.S. midterm elections
date: '2026-11-19'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/internet-traffic-2026-us-election/
author: ''
summary: '[翻译失败，原文如下]


  Visitors to government election websites surged 363% on November 3, the date of
  the 2026 midterm elections in the United States. Across C...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-20T09:31:19.746441'
---

[翻译失败，原文如下]

Visitors to government election websites surged 363% on November 3, the date of the 2026 midterm elections in the United States. Across Cloudflare's election protection programs, we also detected a significant shift in the types and timing of cyberattacks throughout 2026.

Unlike what we saw in other recent elections, attackers focused on gaining access to internal systems and data, rather than knocking websites offline. Government election websites faced website vulnerability attempts 180 times more often than denial-of-service (DDoS) attacks, and at roughly ten times the rate of Cloudflare's broader customer base. We also found evidence of at least one attempt to exploit a recently disclosed critical PHP vulnerability on a state government voting website in the Western United States.

These attacks peaked in late October, several weeks before the election. Vulnerability exploit attempts climbed steadily throughout 2026: from 200,000 per day in January, to2 million per dayÂ in October. However, on Election Day in the U.S., Cloudflare detected no escalation in attack volume and zero major DDoS incidents across protected election sites, marking a sharp contrast to other recent elections, such as inMoldovaÂ last year.

Our data regarding cyberattacks on election institutions came from organizations participating in Cloudflare's free cybersecurity programs: theAthenian Project,Cloudflare for Campaigns, andProject Galileo. Together, these initiatives helped protect more than 1,400 election-related websites during the 2026 U.S. midterm elections, including those belonging to state and local governments, candidates, political parties, voting-rights advocates, journalists, and civil society groups.

Cloudflare launched its first election protection program in 2016 after widespread reports of cyberattacks targeting the U.S. elections. A decade later, it is remarkable to see how far governments and campaigns have come in securing their digital infrastructure. We are proud to help protect democratic institutions and are encouraged that cyberattacks were once again not a disruptive factor in 2026.

In this post, we examine traffic and attacks observed against those organizations on Election Day, analyze the most common types of attacks of the 2026 cycle, and provide recommendations based on those findings.

## Election Day: significant voter traffic, minimal attacks

Ordinary user traffic to state and local government election websites was higher on Election DayÂ (November 3) than any other day in 2026. Traffic to those sites increased to approximately 602 million requests, up from 130 million on November 1. By comparison, traffic across the rest of Cloudflareâs global network rose by only 12% over the same period.

State and local government election websites provide authoritative information to voters on how to register, where to vote, and who won. Because of their critical role, these platforms are often targeted by those seeking to suppress voter turnout, disrupt the reporting of results, or steal sensitive information.

On Election Day itself, Cloudflare did not record a single significant distributed denial-of-service (DDoS) attack across any of its 1,400 election-related websites. The only significant DDoS attack occurred on November 2, targeting a candidate for the U.S. House of Representatives in CaliforniaÂ and totaled 520,000 requests. By comparison, the Moldovan Election Commission experienced more thanÂ 898 million malicious requests in a single 12-hour period on their Election Day in 2025, with attacks peaking at 324,333 requests per second.

## Prior to Election Day: the most common attacks in the 2026 cycle

Website vulnerability scans were by far the most common attack observed by Cloudflare in the 2026 U.S. election cycle. In the 12 months leading up to the election, Cloudflare mitigated 392 million such attacks on government election websites alone.

Website vulnerability attacks exploit outdated or vulnerable website code to gain access to internal systems and data. For example, cross-site scripting attacks inject malicious code into web pages in order to capture administrator credentials or deface site content.SQL injectionÂ manipulates database queries allowing attackers to potentially extract voter records or alter data.

Phishing and other malicious emails targeting political campaigns protected by the company occurred at rates consistent with Cloudflare's broader network, but showed signs of sophistication. In the 90 days leading up to the election, 3.9% of emails sent to organizations participating in Cloudflare for Campaigns were identified as malicious, closely tracking the 4.8 percent baseline across other Cloudflare customers. However, nearly 42% of those malicious emails managed to bypass basic email authentication checks, such as verifying sender identity or preventing in-transit tampering. These threats were nonetheless identified by Cloudflareâs advanced phishing detection tools.

Although website vulnerabilities were the most common attack overall, for journalism and election-related civil society organizations, DDoS was the most common. Over the same 12-month period, Cloudflare mitigated over 10.8 billion DDoS requests targeting these groups. The largest single attack occurred on September 10, 2026, hitting a U.S.-based news organization with 3.04 billion requests. This pattern is consistent withCloudflare researchÂ released earlier this year, which found that among all Project Galileo entities in 120 countries, DDoS were by far the most common attack seen, accounting for 81% of all attacks.

## PHP vulnerability

On October 21, security researchers disclosed serious vulnerabilities (known asphp2shell) in PHP, an open source back-end programming language used by 70% of the world's websites. The flaws reportedly could allow attackers to execute malicious code on vulnerable servers, expose customer data, or disrupt services. CloudflaredeployedÂ Web Application Firewall (WAF) protections for all customers, prior to public disclosure of the vulnerability.

On October 22, Cloudflare's PHP defense was triggered more than 9,000 times on a state government election website in the Western U.S. This attack was only detected on one election-related site and appears to have been an isolated incident rather than part of a broader trend.

## Recommendations

Cloudflare research consistently shows that individuals and organizations participating in democratic elections face significant risk of cyberattack. Data gathered during the 2026 U.S. midterm election suggests those attacks continue to evolve, occur throughout an election cycle and not only on Election Day, and can vary depending on the type of organization targeted.

Based on the recent cyberattack trends in the 2026 U.S. midterms and other elections, we make the following recommendations: Â

- Prepare for surges in user traffic. Legitimate voter interest can create traffic spikes that overwhelm unprepared infrastructure and make essential election websites inaccessible. Organizations should prepare scalable, efficient infrastructure to handle Election Day traffic increases without straining budgets or staff. Â
- Maintain security protections year-round, not just on Election Day.Cyberattacks targeting democratic institutions occur across the entire election cycle, not just around voting windows. Defensive postures must remain active continuously rather than treated as a short-term, seasonal measure.
- Deploy automated defenses to counter rapid threats.AI has made it easier for attackers to find and exploit new vulnerabilities. Organizations should implement security services that update automatically, likemanaged rules, to ensure new protections deploy by default.

[翻译失败，原文如下]

Ensuring voters have access to reliable information about elections not only helps encourage participation and deliver timely, accurate results, but also protects voter confidence in the democratic process itself. As more officials, more institutions, and the public increasingly rely on the Internet for those services, keeping that digital infrastructure stable, secure, and accessible becomes an essential civic priority.

State and local election offices, political campaigns, party organizations, journalists, and voting rights groups in need of cybersecurity services can access them from Cloudflare at no cost. Visit theÂAthenian ProjectÂ (for state and local election websites),ÂCloudflare for CampaignsÂ (for political campaigns), orÂProject GalileoÂ (for civil society, democracy, and journalism organizations) to learn more about eligibility and sign up today.

## Related tags

Follow on Social Media

- Cloudflare
- Jocelyn Woolbright

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! You're all set to receive our newest blog posts.

---

> 本文由AI自动翻译，原文链接：[Internet traffic and attacks during the 2026 U.S. midterm elections](https://blog.cloudflare.com/internet-traffic-2026-us-election/)
> 
> 翻译时间：2026-11-20 09:31
