---
title: Hyper-Growth Done Right - Lessons From the Man Who Scaled Engineering at Dropbox
  and Facebook
title_original: Hyper-Growth Done Right - Lessons From the Man Who Scaled Engineering
  at Dropbox and Facebook
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/hyper-growth-done-right-lessons-from-the-man-who-scaled-engineering-at-dropbox-and-facebook/
author: ''
summary: '[翻译失败，原文如下]


  Radical expansion must be inAditya Agarwal’s genes. When he started as an engineer
  atFacebook, the company had fewer than 15 people. With...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-17T06:58:48.292479'
---

[翻译失败，原文如下]

Radical expansion must be inAditya Agarwal’s genes. When he started as an engineer atFacebook, the company had fewer than 15 people. Within 6 years, he had risen to Director of Product Engineering, leading 2,000 employees to reach 700 million users. In 2012, whenDropboxacquired his startup Cove, the cloud storage incumbent staffed 30 engineers building for 50 million users. Now Agarwal directs an engineering arsenal of 200+ to protect the data of over 200 million people — and he just worked on yesterday's big launch ofCarousel.

“Most of what I’ve learned in my career has been during a period of hyper growth and change,” Agarwal says.

To grow this fast, leaders need to plan day-by-day for the business they want to be in six months — not what they are right now, he says. How do you build an engineering team to constantly rotate and expand? How do you adjust a product strategy when your company transforms weekly, monthly, quarterly? At First Round’s last CTO Summit, Agarwal shared the secrets he’s tapped to keep his team aligned and productive during the fastest of sprints.

## To build a team, break the model. Then break it again.

When a startup first builds out its core team, the new hires are generally from the founder’s first degree network. At Dropbox, many early employees fit the profile of the MIT engineer, just like co-foundersDrew HoustonandArash Ferdowsi. But eventually you’ll need to expand your talent search outside of the founders’ extended circle, and your interview process will need to change. Someone who has built three amazing iOS apps may not be able to show his work on a white board the way you’re used to. And hiring managers can’t spend hours reviewing elaborate homework assignments submitted by candidates. To adjust, Dropbox has tailored its engineering interview process for both diversity and scalability.

“At Dropbox, we have experienced engineers do the equivalent of a design exercise — walk us through your career and tell us about three systems that you have built, what worked and what didn’t.”

It’s easy to screen for whether someone can write code quickly and build systems that scale. But during a hyper-growth phase, what really carries an engineer is a passion for what your company is doing both for the technology and the product, Agarwal says. Past experience says a lot about whether someone fits the ideal profile you’re looking for:

- You need quick learners.
- You need people who are very comfortable with change.
- You need people who can roll with ambiguity and improvise.

“We want people who are comfortable going end-to-end. Who can think about the product all the way down to the infrastructure.”

Up until about a year ago, Dropbox organized itself based on platforms, with an infrastructure team, a web team, an iOS team, an Android team and a desktop client team. After coming up with a product roadmap, each team focused on the product work for it’s own platform.

“We ran into the problem that you'd anticipate,” Agarwal says in hindsight. "We didn’t have enough cross-platform coordination, and there was a reluctance for engineers to expand outside of their core expertise. We had to blow that up."

“The key was to essentially break that model, where somebody thought that they could only work on one particular platform,” says Agarwal. “This was painful, but we had to pay that learning cost. I think we have gone now from maybe 3 or 4 engineers regularly contributing to the iOS code base to probably closer to 25 or 30 right now.”

## Through boom and bust, build resilience.

A rapidly growing company cycles through days or months where users are flooding in and features seem to be humming along seamlessly.But the pendulum will swing the other way, Agarwal warns.Hyper-growth invariably requires expanding beyond individual areas of expertise, both for companies and for individuals. Setbacks can deflate the exhilaration of a breakneck development schedule.

“Be cognizant of the fact that there’s a cycle here. The key part is, when you’re doing well, don’t get complacent, and when you’re not going as well, don’t get depressed,” Agarwal says.

The first engineer on a project influences its culture. A generalist with a deep passion for the technology, who doesn’t get dragged down by small failures, can grow a team around her. Emphasize fluidity and flexibility, he says. At a larger company, you invariably get more siloed and specialized, but the opportunity to go broad is the reason people want to work at a startup in the first place. Give people an opportunity to learn, and they’ll become experts if they're strong.

To be an effective leader in this environment, you should:

- Scale quickly outside your skill own set, and accept failure as part of the process.
- Attack opportunities to learn, and don’t punt when you come up against a problem you can’t fix by yourself.
- Keep your emotions in check. When something’s hard, remember that’s part of the deal.

“We just keep on repeating that the biggest skill you can learn at Dropbox is basically going broad. So learn web code, iOS code and back-end code,” Agarwal says.

## Plan against a moving target.

Dropbox plans in sprints. Interval training lets an engineering team stack short-term goals toward the bigger picture. The question is always: What can you get done in the next six weeks?

“Teams figure out what they want to do themselves, and we give them feedback as to whether they’re being too ambitious or too conservative,” Agarwal says.

Moving fast in the development process doesn’t have to mean unleashing a half-baked feature on your users.

“We set a high bar for releases, but we can really move fast between interim milestones.”

Dropbox’s desktop client, for instance, has a four-step release process when a new update looks ready:

- Internal users dog-food the new version.
- Forum participants give it a try.
- New users setting up accounts receive the updated version.
- Auto-updates across all of Dropbox roll out, and engineers can take the full measure of their work.

“Each of these has a lag time, so we’re basically looking at performance, regressions, and crash rates,” Agarwal says. “And every new release that goes out must demonstrate improvement along those metrics. We don’t necessarily start out knowing how it will do that. But if we know the opportunity exists, we can go find it.”

## Make organic values formal practices.

“At Facebook, we were famously moving fast and breaking things,” Agarwal says. In Dropbox’s case, the focus is on maintaining quality. Everything the company releases has to be polished, but there’s a trade-off there too — it has at times moved more slowly toward final releases, Agarwal says, and that’s okay, as long as it's done with these core values firmly in mind.

![Dropbox's whimsical office is a core part of its culture.](/images/posts/bedaf53f49c4.jpg)

When a startup is growing into a complex enterprise, an engineering team has two options:

1)You can over-engineer a system for massive scale, putting in time-intensive processes that will make things flow smoothly.

2)You can chase rapid growth with a system constantly stretched over capacity, and accept that it will get messy.

Agarwal is looking to split the difference at Dropbox. He wants to push his team, but not so much that product reliability suffers. Just like sprint training stretches an athlete to the limit in each interval to build a stronger body, keeping an engineering team moving quickly but guided by core values keeps product quality high — even if things break behind the scenes.

Because security and safety defines the product at Dropbox, engineers don’t want to break people’s files and don’t want to lose their data. But high-quality doesn’t mean teams can slow down their pace. Managers have to figure out a way to get both out of their people.

## Scale management accordingly.

[翻译失败，原文如下]

At hyper-growth companies, engineers with expanding departments tend to start leading teams — even communicating, coordinating and planning full-time instead of writing code.

Technical leaders see opportunities to learn more, but at the same time, they have to learn what they shouldn’t do. Not every engineer wants to lead a team of 100, even if a company is doubling in size next month, Agarwal says.

“Shift the conversation away from the size of the team that someone is leading. Ask instead if they’re doing something that they’re passionate about, that is impactful for the company. That’s where prestige should live.”

If you’re able to articulate what your organization values, then you should be able to tell people how they’re doing against those values, he says. It should become clear what they should value in their careers, and how they want to be rewarded for their contributions.Being promoted to manager isn’t always the highest praise. Sometimes being a well-recognized individual contributor is best.

Planning and communicating internally will probably always feel a little bit broken, according to Agarwal. “The rate of growth is so intense that it’s difficult to create a system that's always on-point. It’s really difficult to design a system that’s perfectly right for the size that you are.”

The entire company needs to know what’s going on, but some people want more details on a granular level.To serve these needs as a technical leader:

- Be as transparent as possible, even when it’s really uncomfortable.
- Give people pointers where they can go digging for more information themselves, or introduce them to people who can be helpful; just don’t hide anything.

## Build a 10-year culture during 10x growth.

Companies that develop a distinctive corporate culture when they're small have to decide how tightly they want to hold to early practices.

Identify the things that you really care about and keep an open mind, especially as you start to get more diversity. As you begin hiring people from companies like Google, Facebook or Microsoft, organizations that have had enduring cultures, engage them in helping to define how your own culture should evolve, Agarwal says.

Similar logic applies to successfully bringing in whole companies. Before buyingMailboxlast year, in one of its first major acquisitions, Dropbox did its homework.

“We had surveyed which acquisitions have resulted in long-term, successful products for companies like Facebook or Google or Amazon,” Agarwal says.

Often, they saw successful acquisitions that preserved a technical team with its own identity. Companies like YouTube were allowed to run independently at the same time they were absorbed into a much larger enterprise.

Mailbox foundersScott CannonandGentry Underwoodhad spent two years building an iterative prototyping process that optimized for speed, but not at the expense of quality. That reflected values already highly prized at Dropbox.

“We basically told them, ‘do what you always intended to do — capture the market for email. And by the way, we have resources inside the company like recruiting, user operations and infrastructure. Use those where you think they can be leveraged,’” Agarwal says.

When it comes to culture, your method will always be your message.

In 2004, fresh out of Carnegie Mellon’s computer science program, Agarwal started his career as one of 30,000 employees at Oracle. There, he saw firsthand how a company’s product lifecycle can radically impact culture, especially when it comes to speed and a shipping mentality.

“While I was at Oracle, it took a month before a new engineer would get any code in,” Agarwal says. “It sent this implicit message that it’s okay to take a month to write some code.”

Facebook sent an entirely different message when he came aboard. It’s well known that brand new hires are expected to get up and running writing code immediately. This was true when Agarwal joined and is no different now that the company has exploded in size.

Accepting risk, moving fast and committing code immediately reinforced a culture at Facebook where everyone was invested in the look, feel and efficacy of the product.

“When the boot camp system was first introduced at Facebook, one of the explicit goals was, you will have your first check-in to the code base on day one, so that your code will go out on day two,” Agarwal says. “I thought that was amazing.”

Photography byMichael George.

---

> 本文由AI自动翻译，原文链接：[Hyper-Growth Done Right - Lessons From the Man Who Scaled Engineering at Dropbox and Facebook](https://review.firstround.com/hyper-growth-done-right-lessons-from-the-man-who-scaled-engineering-at-dropbox-and-facebook/)
> 
> 翻译时间：2026-09-17 06:58
