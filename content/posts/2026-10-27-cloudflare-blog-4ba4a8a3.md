---
title: What Took the Internet Offline in Q3 2026
title_original: What Took the Internet Offline in Q3 2026
date: '2026-10-27'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/q3-2026-internet-disruption-summary/
author: ''
summary: '[翻译失败，原文如下]


  The Internet can feel invisible when everything is working normally. But when connectivity
  breaks, the many systems it depends upon becom...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-29T08:15:44.656296'
---

[翻译失败，原文如下]

The Internet can feel invisible when everything is working normally. But when connectivity breaks, the many systems it depends upon become evident in an instant. Because Cloudflareâs global network handles more than 20% of the webâs traffic, it offers a unique perspective of how Internet traffic is behaving. When failures in infrastructure, power, policy, or security disrupt access to the Internet,Cloudflare RadarÂ can observe the impact by monitoring traffic to our customers. Each quarter, we review the disruptions detected and annotated on Radar, highlighting what happened, where it happened, and the broader conditions that shaped each event.

In this post, we examine the major categories of Internet disruptions observed during the third quarter of 2026, including government-directed shutdowns, power outages and natural disasters.

## Disruptions at a glance

Between July and September, Internet disruptions were largely driven by failures in the systems the Internet depends on. Power grids failed in Cuba, Honduras, Guam, Ukraine, and several other countries. Natural disasters damaged electricity and telecommunications infrastructure from Nepal to Colombia. Government-directed shutdowns remained the most frequent source of disruption, driven largely by exam-related shutdowns in Iraq, while renewed conflict in Ethiopiaâs Tigray region showed how quickly connectivity can become part of a broader political and humanitarian crisis. Outages within the United States, Japan, and Portugal â countries with a relatively strong history of Internet resilience â remind us that no country is immune to disruption.

In total, Cloudflare Radar recorded 49 disruptions during the quarter. Government-directed shutdowns accounted for 19 incidents, including 18 exam shutdowns in Iraq. Power outages followed with 14 incidents, while natural disasters accounted for five.

## Power failure was a leading causeÂ of disruptions

The Internet is designed to be distributed and resilient, but that resilience still depends on electricity. When power fails, routers, mobile base stations, data centers, interconnection facilities, and the networks that connect them can fail with it. Over the past three months, that dependency was one of the clearest patterns in Radarâs disruption data.Power outages were the second-most common cause of disruptions by incident count this quarter, behind government-directed exam shutdowns.

In Cuba, Internet disruptions followed the erratic patterns of an unstable power grid. Radar observed four power-related outages across the quarter, meaning connectivity was affected by grid failures at least once a month. The outages took place July 6, July 14, August 3, and a three-day blackout from September 18 to 20. The traffic volume decreases ranged from 18% on July 14 to 59% on August 3.

Honduras illustrated how a localized infrastructure failure can produce national-level effects. A power failure on September 10 at an interconnection facility affected at least 11 major providers, showing how concentrated traffic exchange points can become single points of failure. The outage lasted approximately three hours, during which HTTP traffic across the country fell by 63%.

Two notable exceptions were the cross-border provider Telecomunicaciones de Guatemala (AS14754) and mobile carrier Celtel (AS52262), which were unaffected. This suggests that their Honduran connectivity may rely more heavily on infrastructure outside the country.

On July 5, a power outage in Sevastopol, Ukraine, caused an eight-hour blackout, with HTTP traffic dropping by 98%. A little over a month later, on August 12, drone strikes targeting energy infrastructure caused another power outage, resulting in a ten-hour Internet disruption and up to a 95% decline in traffic volume. As discussed in more detail below, geopolitical conflict remains a major driver of Internet disruptions. These incidents also show how conflict, energy infrastructure, and Internet connectivity are fundamentally intertwined.

Also of note: on August 13, a cooling system failure at a data center in the U.S. city of Phoenix caused a near-total drop in Internet traffic fromNamecheap (AS22612). Outages such as these will be important to watch as the role of cooling systems becomes increasingly critical.

Beyond the larger outages in Cuba, Honduras, and Ukraine, power-related disruptions also appeared across a wide range of countries, including Eswatini, Botswana, Tajikistan, Kenya, Saint Lucia, Georgia, and Gabon. Some of these events were caused by sudden failures, while others, such as planned load-shedding in Eswatini, reflected deliberate efforts to manage constrained power supply. Their scale and duration varied, but together they point to the same underlying dependency: when power systems become unstable, Internet connectivity often becomes unstable with them.Â In total, Radar observed 14 power-related disruptions across 10 countries during the quarter.

## The physical world takes the virtual world offline

Last quarter,Radar reportedÂ on the impact of Super Typhoon Sinlaku, as it moved through the Mariana Islands, knocking out power and, in turn, Internet connectivity in Guam, whereHTTP traffic took four days to return to typical levels.

Super Typhoon Bavi followed Sinlaku by less than three months, giving Guam two major storm-related connectivity disruptions in a single year. Officials appeared to take earlier preparedness steps ahead of Bavi, including declaring a state of emergency before peak storm conditions. Even so, the storm caused widespread power outages. TheGuam Power AuthorityÂ reported that strong winds brought down key transmission lines, leaving only about 25% of distribution feeders online at one point. From a connectivity perspective, the outcome was familiar: widespread power outages, downed transmission lines, and a multi-day recovery period for Internet traffic.

In Japan, an earthquake of similar magnitude, 7.1, prompted evacuation orders affecting roughly150,000 people in Kumamoto. The impact on Internet connectivity primarily appeared in desktop traffic, while mobile traffic remained largely unaffected.

In Colombia, a magnitude 7.4 earthquake in August caused building collapses, injuries, mass evacuations, and a four-and-a-half-day Internet disruption. Damage to fiber-optic infrastructure, compounded by the wider earthquake aftermath, drove asignificant drop in traffic from Colombia Telecomunicaciones (AS3816).

Finally, in Nepal, sudden flash floods swept through the Bhote Koshi and Trishuli river systems on August 26, affecting communities across Rasuwa, Nuwakot, and Dhading districts. The flooding damaged homes, infrastructure, and essential services, including power, which in turn disrupted regional Internet connectivity. The outage recorded on Radar lasted two hours, during which HTTP traffic dropped by up to 18%.

## Exam shutdowns continue in Iraq

Government-directed shutdowns were the largest cause of disruptions in Q3, the majority of which occurred in Iraq with separate scheduled shutdowns occurring throughout the quarter. The shutdowns took place on a strict scheduleÂ 03:30â04:00 UTC, lasting about 15-90 min each. The majority occurred between August 26 and September 28, with three occurring between July 1 and 8.

PerInternet Society Pulse, âIn avideo message, Minister Mustafa Sanad, Iraq's Minister of Communication, confirmed the shutdown and vowed to develop a digital system that would eliminate the need for centralized exam distribution and, by extension, the need to shut down Internet access on exam days.â Cloudflare Radar will continue to monitor the countryâs networks as the development of the new system progresses.

[翻译失败，原文如下]

Notably, Syria and Sudan, two countries that have also frequently used exam-related Internet shutdowns in recent years, did not record similar disruptions this quarter. However, this likely reflects differences in exam calendars rather than a clear shift in policy. Radar will continue to monitor whether future national exam periods bring renewed shutdowns in either country.

## Disruptions coincide with political events Â

In Ethiopia, renewed conflict in the Tigray region was accompanied by a government-directed Internet shutdown that lasted 10 days. Traffic dropped by 100%, signaling a full-scale shutdown.

The disruption revived memories of the extensive blockade imposed during Ethiopiaâs civil war from 2020 to 2022, when Tigray was largely cut off from telecommunications, electricity, banking services, fuel, and humanitarian aid (France24), which the World Health OrganizationdescribedÂ as a âde facto blockade.â Although this latest outage appears to have remained localized to Tigray, its impact was still visible in country-level traffic, with HTTP traffic falling by up to 30%.

On September 19, during nationwide elections, fiber-optic cable damage in Russiaâs Far East caused regional connectivity disruptions affecting Chukotka, Magadan Oblast, Kamchatka Krai, and Sakhalin Oblast. RostelecomdescribedÂ the incidents as deliberate damage to backbone fiber lines and said connectivity was restored using backup channels. Radar data alone cannot determine whether the cable damage was related to the elections, but the timing is notable.

## A quarter shaped by shutdowns and power outages, but also resilience

Across Q3 2026, government-directed shutdowns were the most frequent source of disruption, driven largely by Iraqâs exam-related shutdowns. Power outages were close behind, affecting networks across Cuba, Honduras, Ukraine, Eswatini, Botswana, Tajikistan, Kenya, Saint Lucia, Georgia, and Gabon. Natural disasters and conflict added another layer of disruption, reminding us that Internet resilience depends on far more than routers and cables. It depends on electricity, physical infrastructure, policy decisions, and the ability of networks to route around failure.

Radar also observed outages inside individual networks, includingOne Communications (AS19863)Â in Guyana following acable cut,MEO (AS3243) in PortugalÂ following a reported âmass attackâ,Digicel Haiti (AS27653),TurkNet (AS12735)Â in Turkey, andFanap Telecom (AS206065)Â in Iran.

Each of these events demonstrates the Internetâs fragility, but also its resilience. Many disruptions were brief: 14 saw traffic return to typical levels in under an hour, and 16 recovered in less than three hours. But short outages can still have real consequences for the people affected, especially during storms, earthquakes, conflict, or political unrest. Access to the Internet is often access to information, coordination, safety, and help.

Cloudflare Radar will continue to monitor Internet disruptions around the world and share what we see from Cloudflareâs global network. Follow Cloudflare Radar on X@CloudflareRadarÂ and Bluesky@radar.cloudflare.comÂ for updates.

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[What Took the Internet Offline in Q3 2026](https://blog.cloudflare.com/q3-2026-internet-disruption-summary/)
> 
> 翻译时间：2026-10-29 08:15
