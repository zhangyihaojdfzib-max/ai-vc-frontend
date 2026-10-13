---
title: 'Building for good: How civil society organizations are automating on Cloudflare'
title_original: 'Building for good: How civil society organizations are automating
  on Cloudflare'
date: '2026-10-02'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/civil-society-automation/
author: ''
summary: '[翻译失败，原文如下]


  Tracking how governments target dissidents living in exile. Helping people in crisis
  find mental health support. Advocating for legislati...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-13T08:48:20.290155'
---

[翻译失败，原文如下]

Tracking how governments target dissidents living in exile. Helping people in crisis find mental health support. Advocating for legislation that protects free expression online. These are a few examples of how some of the world's leading organizations are building the future of non-profit work with Cloudflare.

AI is changing how people do their work. The goal of Cloudflare Impact is to help ensure that non-profit organizations are among the first to benefit. Today, weâre sharing what dozens of civil society organizations have built using our developer services with more than $7.5 million of Cloudflare credits. These stories show what is possible when AI applications are accessible, secure, and affordable to build and run.

## From "keep us secure" to "help us build"

We believe a better Internet is one that allows people to express themselves online and access a diverseÂ range of viewpoints. A key part of Cloudflare's mission has been making security services available for everyone and helping ensure thatÂ individuals and organizations working for the public interest are not forced offline by those more powerful. Today,Project Galileo, which provides free cybersecurity services to civil society organizations, protects more than 3,400 domains across more than 120 countries.

Through these partnerships, organizations have shared with us how their needs have evolved from not only wanting to secure existing applications, but wanting to build new ones. AI has allowed non-technical teams to design, build, and scale tools tailored specifically for their workstreams and to advance their mission.

This opportunity is arriving at a challenging moment for the sector. Many organizationsreportÂ operating under financialstrainÂ after major reductions in government funding contributed tolayoffsÂ and closing of programs. As groups rebuild their work in a new environment, some havereportedÂ using AI to help do more with less. But adoption remains ad hoc. In a CIVICUSsurvey, more than half of civil society respondents viewed privacy concerns as a barrier to use. These groups hold sensitive data, like the location of activists or the identities of anonymous sources, and are disproportionately at risk of cyberattacks, according to our ownCloudflare data. Additionally, the cost of building and running complex automation workflows can be prohibitive. Among those surveyed by CIVICUS, 48% cited financial constraints limiting their adoption.

Cloudflare helps address these concerns. Our developer services incorporate security and privacy protections from the outset. By running on our global network, applications are automatically protected fromdistributed denial-of-serviceÂ attacks and attempts to gain unauthorized access to internal systems. Civil society groups can also build and run applications more cost effectively. Our lightweight and serverless architecture scales with demand without requiring organizations to provision or pay for idle infrastructure.Workers AIÂ also removes the need to operate dedicated GPU infrastructure, whileAI GatewayÂ provides rate limits, observability into how teams are using AI, and intelligent model routing to reduce unnecessary model calls and keep costs under control.

## Awarding $7.5 million for the next generation of civil society work

During Birthday Week last year, weexpandedÂ Cloudflare for Startups to include non-profit and public interest organizations, providing each of them with up to $250,000 in credits for our developer services. We are proud to announce that we selected 30 organizations to participate in our first non-profit, startup cohort, and we have been thrilled to watch their ideas and tools designed to tackle problems in climate science, humanitarian aid, mental health, civic engagement, and education come to life.

Here is what a few of these non-profits have built.

- LebTownÂ â local news, rebuilt on automation:ÂLebTownÂ is an independent non-profit newsroom covering Lebanon County, Pennsylvania. Until this year, the editorial team ran its entire operation across two Google Docs, a Google Calendar, Discord, and Gmail. LebTown is replacing that with a custom-built editorial management system that follows stories from pitch to publication, tracks audience reach, and lets reporters log community impact directly from their app or via Discord. The team has also built tools that convert county real-estate transfer records from PDF exports into structured data, and a real-time copyeditor agent that integrates with LebTown's WordPress site.

![](/images/posts/a26737ce4bca.jpg)

- Kaya Guides â scaling mental health support:ÂKaya GuidesÂ built a WhatsApp-based mental health application that pairs people experiencing depression in India with trained lay counselors, making support accessible without the cost or waitlists of traditional therapy. As of September 2026, the application has supported 10,439 people, with 2,325 currently enrolled. To keep pace with demand, the team migrated its care management system to Cloudflare and now processes around 500,000 WhatsApp messages a month. They built a live AI system that listens to counseling calls and gives counselors real-time feedback to keep sessions on track. According to Kaya, these tools have helped develop a program that is more consistent and self-correcting as it scales, without significant additional cost or complexity.
- The Snorkelling Society âÂ mapping the worldâs snorkeling sites.ÂThe Snorkelling Society, is a UK non-profit building a web and mobile application for the global snorkeling community calledSnorkelMap. This tool will help people discover new places to snorkel, explore information about different locations, and allow users to contribute their experiences. Because the application is built and maintained by volunteers, the Snorkeling Society uses Cloudflare to secure storage to allow for community contributions and uploaded images while also safeguarding against cyberattacks.

![](/images/posts/15b9cec0b103.jpg)

## Working together to build automation tools for human rights

We also heard from larger civil society organizations who wanted to build complex workflows and welcomed extra engineering support. These projects included several variationsÂ of the same problem: large amounts of manually-collected, dispersed information that needed to be integrated, reviewed, and structured in order for effective analysis to be conducted. The data involved was also sensitive, like the names of human rights abuse victims, and the risk of unauthorized access, data leakage, or hallucinations in an output could have serious consequences.

Cloudflare not only provided free access to its developer service to support the development of each of these tools, but also assembled a team of volunteer engineers â product experts, front-end designers, back-end builders, and security advisors â to design and build them. Questions weâre exploring include where automation is helpful, which models align best with each task, how to incorporate the necessary security controls, and where a person must remain involved.

[翻译失败，原文如下]

- Freedom House â tracking transnational repression:ÂFreedom HouseÂ wasÂ founded in 1941 to advance democracy and freedom globally. They created and maintainÂ the world's most comprehensive database oftransnational repressionÂ incidents, which is when governments reach across borders to silence dissent among diaspora and exile communities. Manually identifying incidents and coding patterns of transnational repression â which involves looking at thousands of potential cases â is labor intensive and time consuming. To help automate this process, we are creating an interactive dashboard that can ingest, structure, and flag potential cases of transnational repression from public reporting. The tool is fine-tuned on the organizationâs methodology to improve accuracy, with Freedom House involved in every step of the process. Given the sensitivity of the topic, security and data minimization have been priorities in every decision. Automating this initial stage in the research process can help staff focus on deeper analysis, producing reports, and working with policymakers to address transnational repression.

Prototype of Freedom Houseâs tool tracking transnational repression

- Global Network Initiative â protecting free expression and privacy online:TheGlobal Network InitiativeÂ (GNI)Â is a membership organization of civil society groups, academics, investors, and tech companies (including Cloudflare) working to advance free expression and privacy online. To do this, GNI tracks and responds to a rapidly evolving landscape of regulatory proposals, policy developments, and legal trends across dozens of jurisdictions, from online transparency requirements in the European Union to data localization mandates in the Asia Pacific region. We are building a dashboard that identifies these proposals and recommends opportunities for advocacy based on GNIâs mission and previous work. It surfaces, describes, and categorizes relevant news, calls for comment, and legislative activity. The tool also helps manage each opportunity by tracking the internal review process and alerting staff of upcoming deadlines.

Prototype of GNIâs dashboard that tracks the status of engagement opportunities

- Article One â assessing human rights risk:Article OneÂ is a specialized strategy and management consultancyÂ that advises companies on understanding and mitigating the human rights impacts of their policies, products, and operations. This involves reviewing and summarizing large amounts of documentation, from factory audits to country-context reports. We are working with Article One to build a risk assessment tool that processes and structures this information, identifies salient human rights risks, and generates draft recommendations that staff can review and refine. AI helps structure information, but Article One makes all judgments.

## Whatâs next? Apply to join our second cohort

Itâs incredible to see how civil society organizations are evolving their work in an era of AI. Cloudflare is excited to play a small role in this process. Working directly alongside these organizations not only helps advance their missions, but also helps inform how we think about the security and privacy in high-risk environments and how we can scale similar programs moving forward.

Our first non-profit startup cohort shows how automation can help the next generation of community service organizations use AI and automation to serve the public, and how they can do this securely and affordably.Â

Weâre excited to announceÂ that starting today we are officially opening our startup program to our second Â cohort of non-profit organizations.

If your organization is interested,apply hereÂ and select the non-profit checkbox. Weâd love to build with you!

## Related tags

Follow on Social Media

- Cloudflare
- Jocelyn Woolbright

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Building for good: How civil society organizations are automating on Cloudflare](https://blog.cloudflare.com/civil-society-automation/)
> 
> 翻译时间：2026-10-13 08:48
