---
title: 'Cloudflare DDoS Threat Report 2026 Q3: More swarms, fewer giants'
title_original: 'Cloudflare DDoS Threat Report 2026 Q3: More swarms, fewer giants'
date: '2026-10-29'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/ddos-threat-report-2026-q3/
author: ''
summary: "[翻译失败，原文如下]\n\nWelcome to the 26th edition of Cloudflare's DDoS Threat Report.\
  \ This edition covers the third quarter of 2026 â\x80\x94 July, August, and Septe..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-30T08:47:52.507178'
---

[翻译失败，原文如下]

Welcome to the 26th edition of Cloudflare's DDoS Threat Report. This edition covers the third quarter of 2026 â July, August, and September â and returns the series to its quarterly cadence following the combined H1 2026 volume. The analysis is produced byCloudforce One, Cloudflare's Threat Intelligence organization, providing a comprehensive analysis of the evolving threat landscape ofDistributed Denial of Service (DDoS) attacksÂ based on data from theCloudflare network.

## Key insights

1. Short-burst, low-bandwidth attacks lasting under 10 minutes and 1 Gbps surged by 208%. Conversely, hyper-volumetric attacks exceeding 1 Tbps plummeted by nearly 69% from Q2, possibly a reflection of law enforcement actions against four major Internet of Things (IoT) botnets earlier in the year. However, variants continue to emerge, proving that IoT botnets remain a durable, high-volume threat to network infrastructure.
2. Threat actors dramatically shifted their reflection and amplification tactics, abruptly abandoning CLDAP floods, which collapsed by 99.5% quarter-over-quarter. Instead, attackers pivoted heavily toward other connectionless protocols, driving a 215% surge in DNS amplification and a 122% increase in general UDP floods.
3. Attack targets broadened significantly across both industries and geographies, with the United States reclaiming the most-attacked position from China. Canada and Israel experienced sharp spikes in targeted attacks â jumping 10 and 7 spots respectively â while juggling geopolitical tensions, trade disputes, and contentious domestic events. At the same time, the operational focus shifted away from media organizations toward a wider array of industry targets, including consumer services, Internet infrastructure, and adult entertainment.

## Q3 by the numbers: 8,200 DDoS attacks every hour

Across its network in the third quarter of 2026, Cloudflare autonomously mitigated 18.2 million network-layer DDoS attacks and 14.4 trillion HTTPÂ DDoS requests. That works out to approximately 8,226 network-layer DDoS attacks per hour, or about 197,400 per day â one attack every 0.44 seconds. The quarter's mitigated traffic totaled 272.6 PB at the network layer and 95.1 PB at the HTTP layer.

![](/images/posts/adba13d9684d.jpg)

![](/images/posts/4097c9278be3.jpg)

## More swarms, fewer giants

Short-burst, mid-range, high-count attacks â the operational signature of DDoS-for-hire "booter" services â accelerated this quarter. These attacks primarily targeted computer software, gambling and casinos, and information technology industries. Cloudflare autonomously mitigated 18.2 million network-layer DDoS attacks in Q3 2026, a +208% increase fromthe same quarter in 2025:

- 96% ended in under 10 minutes
- 98%Â stayed under 1 Gbps, more than enough to overwhelm a server or website

![](/images/posts/15b8d33755b8.jpg)

On the other hand, network-level hyper-volumetric attacks (those exceeding 1 Tbps) reversed course, dropping to 251 attacks in Q3 from805 in Q2Â â coinciding withlaw enforcement actionÂ in early 2026 that dismantled four of the largest IoT DDoS botnets: Aisuru, KimWolf, JackSkid, and Mossad.

Still, IoT-based botnets remain a durable high-volume threat as the ecosystem churns through new variants such asDysphoriaÂ andEvooo1Bot.Mirai-classified mitigation peaked in August at 57.23 PB, representing 46.5% of all mitigated network-layer bytes in Q3, including four days â August 16, 19, 23, and 25 â that each cleared three petabytes. The quarter's longest sustained Mirai attack ran 49.7 hours between August 19 and August 21.

![](/images/posts/1666b32a5417.jpg)

## Vector shifts: the collapse of CLDAP and rise of UDP

The most dramatic vector shift of the quarter was downward.CLDAPÂ (Connectionless Lightweight Directory Access Protocol) attacks â where small queries with a forged victim IP address trick public domain controllers (UDP 389) into reflecting massive, amplified responses back at the target â experienced a dramatic +580% quarter-over-quarter surge in the first half of the year before collapsing to just 0.05% of attacks in Q3.

Meanwhile,DNS amplificationÂ surged 215% to account for 3.43% of all network-layer attacks, exploiting openDNS resolversÂ in a similar reflection-and-amplification pattern to CLDAP: small spoofed queries, large replies directed at the victim. OtherUDP floodsÂ climbed from 14.06% to 31.31% of network-layer attacks. UDP is a connectionless transport protocol, which makes it a convenient vehicle for raw volumetric attacks: attackers send large numbers of UDP packets to random or specific ports on the target, forcing the target to check for a listening application and respond, consuming its network and compute resources.

![](/images/posts/ebe205356799.jpg)

## Most-attacked industry

While Media, Production & Publishing remained the most-attacked industry in Q3 2026, its overall share is roughly a quarter of its Q2 level, and the focus has moved across a wider set of industries. Internet rose from outside the top 10 to #6; Consumer Services and Adult Entertainment also climbed in, reaching #8 and #9 respectively.

![](/images/posts/fcba3fc0776a.jpg)

## Most-attacked locations

### Geographic surges: Canada and Israel climb the ranks

Adding to an already turbulent period of bilateral trade disputes, Canada jumped from #16 to #6, driven by attacks against its Retail, Telecommunications, Service providers & carriers, and Marketing & advertising industries.

Israel moved 7 spots to take #10 as a result of sustained DDoS activity in mid-September. While this period was marked bycontentious decisionsÂ ahead of parliamentary elections and the Rosh Hashanah holiday, there was also a massive, documentedsurge in hostile cyber warfareÂ targeting Israel this year.

### Top 10

The United States was the most-attacked location in Q3 2026, while China was numberÂ #2 and Indonesia rose into the top three at 2.93% of total attacks. The U.S.-China pairing at the top is consistent with the first half of 2026, when China finished #1 and the U.S. #2; the countries have traded positions as attention and attacker preferences shift.

![](/images/posts/abef9911a129.jpg)

Strengthening global defenses and helping to defend the Internet

Cloudflare's network is designed to absorb this kind of growth in DDoS threats. Every service on our network is protected byfree, unmetered DDoS protectionÂ that runsat every one of our 330+ cities globally, backed by500 Tbps of network capacity. Autonomy is the point: our systems detect and mitigate attackswithout human intervention. And they need to, because as this quarter's distributions make clear, most attacks end long before a human analyst could see the alert, and the largest attacks still regularly exceed 1 Tbps at a cadence measured in hundreds per quarter.

To help hosting providers, cloud computing platforms, and Internet service providers identify and take down the abusive IP addresses and accounts that launch these attacks, we leverage Cloudflare's unique vantage point on DDoS attacks to providea free DDoS Botnet Threat Feed for Service Providers.

Over 800 networks worldwide have signed up for this feed, and we've already seen great collaboration across the community to take down botnet nodes. For a continuously-updated view of attack trends across the Internet, visitCloudflare Radar.

## About Cloudforce One

Driven by a mission to help defend the Internet,Cloudforce OneÂ draws on telemetry from Cloudflare's global network â which protects more than 20% of the web â to drive threat research and operational response, protecting critical systems for millions of organizations worldwide.

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Cloudflare DDoS Threat Report 2026 Q3: More swarms, fewer giants](https://blog.cloudflare.com/ddos-threat-report-2026-q3/)
> 
> 翻译时间：2026-10-30 08:47
