---
title: "Bridging technical depth and usability: The story behind Radarâ\x80\x99s redesign"
title_original: "Bridging technical depth and usability: The story behind Radarâ\x80\
  \x99s redesign"
date: '2026-10-08'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/radar-redesign/
author: ''
summary: "[翻译失败，原文如下]\n\nRadar provides a real-time view into global Internet trends,\
  \ powered by Cloudflareâ\x80\x99s global network. We support Cloudflareâ\x80\x99\
  s mission ..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-13T08:48:18.443560'
---

[翻译失败，原文如下]

Radar provides a real-time view into global Internet trends, powered by Cloudflareâs global network. We support Cloudflareâs mission to help build a better Internet by making web data visible, clear, and actionable for everyone.Since launching in 2020, Radar has found a natural audience amongst expert users with technical backgrounds, such as network operators andacademic researchersÂ who rely on Radar data to observe industry trends and global events.

But Radar also has the potential to be a more regular, self-serve resource for journalists, human rights advocates and policymakers, and everyday users. Making Radar accessible to a wider audience is a core part of our vision, so we knew it was time to reevaluate the user experience: How could we make Radar more approachable to broader audiences, while preserving the depth and rigor that we currently have?

In this blog post, weâll introduce the redesigned Radar, share our design process, and outline our broader vision for the platformâs future.

## Challenges with the previous design

![image3.png](/images/posts/26bb9e78c6b3.jpg)

While the previous landing page was successful at showing the breadth of Radarâs data, the way that information was presented made it difficult to parse. The bento box layout gave everything similar visual weight, the vertical cards disrupted natural reading patterns, and the styling felt disconnected from Cloudflareâs broader brand.

We heard this from users. One external user mentioned that one of his biggest frustrations with Radar was that it was difficult to show to his students. That feedback reinforced the problem that Radar could feel intimidating to people encountering it for the first time. With this in mind, we wanted to create a landing page experience that shaped a clearer path through the content, instead of asking users to interpret everything at once.

But making Radar more accessible wasnât only about reorganizing the content. It was also about making the experience feel more connected to Cloudflare. For external users, consistency directly affects trust and usability. A more cohesive Cloudflare experience helps signal that Radar is an authoritative source, while familiar layout patterns reduce the effort required to move through complex information.

## Introducing Radarâs new landing page

![Radar's homepage map](/images/posts/db9c681e6fba.jpg)

The new and improved Radar uses a visual reference that users of all backgrounds will have a familiarity with â a map. Even though in many ways the Internet operates outside the concept of national borders, its relevance to everyday life is often best understood through geography.

The top section focuses on traffic and outages. We lead with outages as they are one of the most concrete, timely, and salient data points about the state of the Internet. Traffic, meanwhile, communicates the scale and breadth of Radarâs data. The map also acts as a navigation point into the insights below, guiding users from the global view into specific countries, trends, and data stories.

![Guided data exploration](/images/posts/00ad961b5b6b.jpg)

Below the map, we turned the old bento box chart widgets into a tabbed flow that helps users move through the data more deliberately. The tabs provide summary statistics to give the user a sense of Radarâs capabilities, while also giving them a call to action to explore the data in depth. The tabbed structure creates a clearer hierarchy, keeps the page from feeling overwhelming, and previews the range of information Radar provides.

## From concept to reality

### Developing Radarâs design language

To develop Radarâs design language, we looked across Cloudflareâs content ecosystem, which exist in these three pillars:

- Marketing pages (like cloudflare.com)
- Content experiences, like the Cloudflare Blog and Developer Docs
- Product experiences

![](/images/posts/a8af2f3a8b11.jpg)

Where does Radar fit?

Ultimately, we decided that Radar sits at the intersection of all three. At its core, Radar is a data product, but itâs also public-facing and inherently content-rich. The strategy blends design aspects of all three: approachable like marketing, structured and navigable like content, and maintainable by migrating toKumoÂ componentsÂ used by Cloudflareâs product system.

### What we tried along the way

From the outset, we knew the landing needed to communicate Radarâs global perspective. Because Radar helps people understand Internet activity across countries and regions, a map felt like the clearest way to make that scope immediately visible.

The map went through many rounds of iteration as we tried to strike the right balance between data richness and approachability. Early versions were too dense â we were trying to convey credibility through data-heavy visuals. Later versions moved too far toward marketing-style visuals; they felt more approachable, but risked making Radarâs fresh data feel static or overly summarized. The current direction sits between those two poles: it has the feel of live data, but itâs easier to read.

![](/images/posts/e1bb9fc9e43c.jpg)

![](/images/posts/09a3b97021e9.jpg)

## The Radar vision and evolution

Because Cloudflare sits in front of roughly 20% of all web traffic, Radar has the opportunity to tell unique and compelling stories about the Internet. To unlock that value, we want to empower every user with real-time insights across security, performance, and traffic.

This redesign is a foundational step in that direction. Moving forward, Radar will continue to focus on tools, visualizations, and storytelling frameworks that remove friction for new audiences while doubling down on our deep data infrastructure. By pairing our technical rigor with a cleaner, human-centered experience, we are ensuring that more people can explore, understand, and share the state of the Internet.

## Help us make Radar better

This redesign is our first step toward a more intuitive, scannable Radar. But we're just getting started, and we need your input. Whatâs working? What isnât? What insights are still hard to uncover?

You can share feedback with us on social media at@CloudflareRadarÂ on X,radar.cloudflare.comÂ on Bluesky, or email us atradar@cloudflare.com.

- Cloudflare
- Sophia Alfred

---

> 本文由AI自动翻译，原文链接：[Bridging technical depth and usability: The story behind Radarâs redesign](https://blog.cloudflare.com/radar-redesign/)
> 
> 翻译时间：2026-10-13 08:48
