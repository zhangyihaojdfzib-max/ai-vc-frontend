---
title: Facebook VP of Engineering on Solving Hard Things Early
title_original: Facebook VP of Engineering on Solving Hard Things Early
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/facebook-vp-of-engineering-on-solving-hard-things-early/
author: ''
summary: '[翻译失败，原文如下]


  This article is by Cory Ondrejka, former director of mobile engineering in Facebook.
  He also was the Chief Technology Officer of Linden L...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-17T06:59:02.614186'
---

[翻译失败，原文如下]

This article is by Cory Ondrejka, former director of mobile engineering in Facebook. He also was the Chief Technology Officer of Linden Lab, maker of Second Life. He blogshereand tweetshere.

January 2002. AtLinden Lab, we were still referring to Second Life as Linden World, our furnace-less office was near freezing because the space heaters kept popping breakers, the Dot-Bomb crash was in full swing, DEMO 2002 was 4 weeks away, and 10 programmers were trying to duct tape everything together. Little did we know it was never going to get easier to fix the truly hard problems companies face. I talked about this, among other engineering challenges, at First Round Capital's last CTO Summit.

## From Build to Growth

Companies go through many transitions over time, but the most transformative is the rapid switch from build phase to growth phase. Build phase is defined as that time before shipping. The team has just come together, united by a change-the-world vision. Everyone is ready to do whatever is needed to get version 1.0 — or perhaps version 0.4.2 alpha — into the hands of real people.

But once people are using the product, a company immediately hits growth phase. The clarity of “ship version 1” splinters into the competing demands of new features, quality improvements, additional product lines, new markets, and company expansion — all focused on the need to grow revenue and users.

Suddenly, attention is focused on keeping ahead of the competition. Crucial steps like laying the foundation for great management or shaping a sustainable culture get shifted to the back burner, creating management debt just as real and damaging as the technical debt startups strive to avoid.

The demands of building an initial product can make it easy for founders and CEOs to postpone non-product decisions. Worse, the nature of small companies hides existing and emerging problems.

Early in my career, I helped build one of two game development teams at a new company. While these teams had entangled dependencies and overlapping goals, our small size and excitement hid the inefficiencies and conflict between them. As we grew, the challenges only increased. Because we didn't have clear leadership at the company level to create priorities between teams, we were left to duke it out on own. And we never built effective habits around how to reach decisions or resolve discrepancies, so minor problems quickly escalated. While we were ultimately able to ship one title, we squandered the talents of a great group of engineers and designers.

Every early stage company thinks it has reinvented management. Blog posts abound explaining how managers are not needed or how metrics and automated systems will suffice on their own.

It's easy to fall into the tempting trap of the small, build-phase startup: managing 20 people is easy. Shared mission, small numbers, and the startup grind keep people focused with nearly any structure, including no structure at all. Management is the first hard thing that is easy to get right early.

Establishing Early Management

Three ideas to help startup teams nail management out of the gate:

- Build management and organizational structures around the strengths your company needs to succeed.
- Recognize and plan for the weaknesses that you know are inherent in the structures you pick.
- Build great habits around communication and decision-making when everyone still knows each other well.

Challenges related to vague, inconsistent, or missing management become acute as companies increase headcount and accelerate hiring. When the organization is just the CEO and founders, the CEO’s decisions are clearly heard and information does not have far to travel. Unfortunately, scale makes all of this more difficult.

Even at 15 employees, different personalities lead to communication hubs and nodes, creating information choke points. By 50, people don't know everyone they work with well or exactly what they do, increasing communication overhead and requiring much more time to be allocated to status updates, coordination, and trust building.

Being a good manager means making honest and fast decisions about what strengths and weaknesses an organization has. No single structure or style is best. If it were, every large, successful company would be organized in the same way. Nor will every employee or founder equally support the style the CEO chooses. So make hard choices early, when the team is small, the focus is on shipping, and people know and trust each other.

Lack of successful management and organizational structure becomes obvious in growth mode. Attrition spikes, because retaining great employees requires managers worthy of them, and not every early employee will excel at management. Small mistakes in communication blossom into politics. Efficiency starts dropping as product development losesfocusand agility plummets. Most dangerously, the CEO is suddenly running an inflexible and unhappy company — one profoundly worse than what they dreamed of building.

Building great products is hard enough without allowing the ease of early management to fool founders into thinking they invented something new. Build great management, train new managers, and introduce sustainable, scalable structure now. Do not wait until world-class managers and radical re-orgs are needed to fix poor information flow or productivity problems.

When I joined game developer PCP&L early on, our CEO was clear about responsibility and management. Project leads owned shipping their games. The buck stopped with them. As expected, this structure ended up with less collaboration and common tooling than we would have wanted, but unlike my prior experience, our CEO anticipated this challenge. Along with the VP of Engineering, he focused on coordination between teams. This helped uncover and bolster the organization’s true strengths: project leads with responsibility and accountability leading fast-moving, confident teams that shipped successful games.

## Good Culture from the Start

Next to establishing strong management principles, creating a sustainable culture is vital. To do this:

- The CEO must own encoding and transmitting culture.
- Write down what makes your company different.
- Describe culture in ways that make people think and debate rather than universally agree.

Culture always stems from the behavior of founders. When the company is small and employees have enough overlap with each other, culture is transmitted directly from the founders to new employees.

This is sufficient until either scale or growth impact the ability of new employees to learn directly from founders. Instead, they start learning from other new employees and — without clear and reinforced messaging — information gets lost. Absent documentation, culture starts to drift and becomes very difficult to restore.

From the earliest days of Linden Lab, we gathered together for end-of-week whiteboard sessions where we listed our most critical open tasks. We went around the room and let people grab the action items they wanted, making sure nothing was left unclaimed. The sense of accountability from picking tasks yourself and the certainty of weekly check-ins helped us keep development velocity high while giving individuals lots of choice about what they worked on.

Years later, in the midst of rapid company growth, we tried to encode this combination of responsibility and freedom as “choose your own work.” Unfortunately, there was an assumed but unwritten clause stating: “from this pre-formed list of most important tasks.” This caveat was obvious to old-timers but not understood by new hires. Before long, we had a split culture in engineering that took years to fix.

Address these issues by defining culture early. Do this by recording statements that cause people to think and ask questions rather than obvious statements everyone agrees with.

[翻译失败，原文如下]

Facebook’s “Move Fast and Break Things” tagline is a canonical example. It has challenged every new employee to realize it's worth some amount of risk to keep innovating, experimenting and moving forward. And to avoid becoming overly conservative even when a mistake could impact a billion people.

“Move Fast and Break Things” helped us make decisions during the mobile transition. We built out infrastructure and tooling as safeguards to help every product team take ownership of their components within the mobile applications. It was only after these changes were instituted in 2013 that we were able to dissolve the specialized mobile team and transition Facebook into a truly mobile company.

Building great management and great culture is never easy nor complete, but both are much harder to tackle when product has already shipped. Take advantage of the benefits of build phase to start early and tackle these hard problems before they become so massive they put the company’s success on the line.

---

> 本文由AI自动翻译，原文链接：[Facebook VP of Engineering on Solving Hard Things Early](https://review.firstround.com/facebook-vp-of-engineering-on-solving-hard-things-early/)
> 
> 翻译时间：2026-09-17 06:59
