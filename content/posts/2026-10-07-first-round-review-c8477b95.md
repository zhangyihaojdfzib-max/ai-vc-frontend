---
title: 'Context Before Code: How to Build Better Tools'
title_original: 'Context Before Code: How to Build Better Tools'
date: '2026-10-07'
source: First Round Review
source_url: https://review.firstround.com/notion-ai/
author: ''
summary: '[翻译失败，原文如下]


  Theo Bleier,an AI software engineer at Notion, made 40 cold calls on his second
  day as a member of the sales team. He didn’t land any mee...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-11T08:05:47.891777'
---

[翻译失败，原文如下]

Theo Bleier,an AI software engineer at Notion, made 40 cold calls on his second day as a member of the sales team. He didn’t land any meetings.

“These are amateur numbers. But it was brutal,” says Bleier. “I got one person on the line who didn’t hang up immediately. The conversation went on for about four minutes, mostly because they confused ‘Notion’ for ‘Motion.’”

Bleier made this call from his new desk in the sales pod. For one month, he became a card-carrying member of the sales team, but initially, he found himself there as a curiosity. “I’ve been very interested in how AI affects the way people work. That was one of the reasons I joined Notion originally,” he says. “I’ve been on the AI team for over two years, and have an idea of what this means for product and engineering — but what’s it mean for everyone else?”

In a lunch conversation with Notion’s Head of Global SalesPravesh Mistryand co-founderAkshay Kothari, Bleier learned other folks in the company were also thinking about the same thing: How could AI help every corner of the org be more effective and impactful? (Frankly, this is a question that all companies are asking themselves right now.)

This simultaneous invention catalyzed a series of events that would have Bleier embed within the sales team to uncover the root challenges in their workflows and build internal AI tools to help solve them.

Theo Bleier, Software Engineer - AI, Notion

He'd eventually create a Chrome extension to fix the papercut problem of copy-pasting information between the many pieces of software reps used when writing outreach emails. But his more impactful internal product would be a new bet that changed the sales process, using product signals to identify the right time to reach out to an account (combined with custom research and email drafts).

In this essay, we learn why Bleier and Mistry knew they couldn't just throw an AI tool at the sales team and expect to see results — instead embedding an engineer to deeply understand the problems the team faced before doing any building. If you’re developing internal AI tools, Bleier’s process is a clear example of how to find the real problem before writing a single line of code. Let’s dive in.

## Required learning: the sales process

Notion, the productivity software and AI workspace valued at $11B, is regarded as one of themost impressive PLG companiesout there, but it's also been building out a sales-led motion.

Mistry says this requires a change in focus (which is especially important for such a horizontal product): having the sales team spend more time on upmarket opportunities and moving from a model that's heavily inbound to heavily outbound. “You have to narrow this horizontal focus into an ICP that you can really go attack, and get very specific about who you want to go after. You want the selling team to spend time on opportunities that have the highest probability to close,” says Mistry. “Today, Notion serves everyone from the largest enterprises in the world all the way to a monastery in Tibet. So we have to be focused with our outbound efforts to ensure it’s time well-spent.”

![Nick Keomahavong — Buddhist monk, psychotherapist and author — visits NotionHQ with a colleague.](/images/posts/2df86adafc36.jpg)

The company learned that engineering, product and design teams showed strong product usage signals that were especially important to Notion's upmarket move — more depth of usage (using databases and collaboration features) as opposed to breadth of usage (more seats to an account). Proactively outbounding this group showed promising results: “Win rates, deal volume and deal sizes went up, and speed to close went down. So we were winning more, winning bigger and winning quicker,” says Mistry.

But Mistry — like many sales leaders right now — wanted to accelerate the success by using AI to bring even more sophistication to how they selected which accounts to go after and when to engage them.

He took a mental step back. Notion is building an AI product, and the people building it have a deep understanding of how these tools work. “Why don’t we just bring one of those folks into our team who already has an inclination and desire to solve these types of business problems?” he says. “Let’s embed an engineer within our organization as a full-time employee and let them actually experience what the arena feels like, actually go through the process of moving from an inbound motion to an outbound motion.”

The answer was sitting on another floor of the office building. Bleier's interest in learning how to solve other teams' problems with AI led him to that lunch table conversation. “If I were building a company that creates sales tools, the first thing I would do is beg all my founder friends to just let me sit in with their sales teams,” Bleier says. “So that’s what I did.”

## From observing workflows to doing the work

Mistry invited Bleier to sit in on the sales team’s “outbound day,” where sales reps all make cold calls together. Green to any professional selling, Bleier was surprised by two things.

1. How differently salespeople work than engineers

“There’s this joke that hiring lazy engineers is actually the move, because they’ll work as hard as possible to automate their job and not have to work,” says Bleier. “Salespeople are excited about this too, but often don’t know where to start. The answer is always, ‘Hell yeah, please help me get rid of this thing that’s wasting my time.’” Even the simple task of copy-pasting information was something they knew was annoying and time-consuming and needed fixing, but it was seen as a necessary evil of the outbounding process. They were hyper-focused on quotas and numbers, not fixing papercuts.

Part of this copy-pasting happened between different tools — and the tool sprawl in the GTM org was also new to Bleier. On the engineering side, things mostly run on Notion. They don't use another task-tracking app.

“I watched folks copy-paste text and contacts between many different tools into their browsers,” he says. “I also noticed folks going to Notion AI and using that to generate something, copy-pasting it back somewhere else and getting more information from their browser.”

Watching these processes led to one of Bleier’s early insights about where he could apply AI.

2. More research led to more success (or at least Bleier initially thought)

Building an outbound muscle can be painful at first; it's a meaningful transition to go from cold emailing to picking up the phone. But some reps performed much better than others.

“We had one person calling, calling, calling, calling. They had the highest number of calls but the lowest hit rate. Then we had another person calling less but hitting more,” says Mistry.

As an engineering outsider to the sales process, Bleier was struck by the disproportionate amount of research some reps did leading up to the calls. "Some folks were going down the list, hitting every person they could find in the CRM. But another rep had spent the night before figuring out who each person was, what they did and exactly what they were going to say to them," he says.

Of course, there are many tools that arm salespeople with this kind of knowledge. But Mistry is keenly aware of not adding to the tool sprawl. He isn't averse to buying new tools, he just wants to make sure they're the right ones that fit Notion's sales motion. Sometimes that means building them yourself. He likens it to a house: "We have this beautiful house with a great foundation. So much of what we need to do now is build the plumbing and wiring," he says. "You've got systems, you've got data, you've got tools and you've got how they all talk together. If you just buy these five things people tell you that you should have, you've just made the problem worse. And you're killing the one thing you value more than anything else: sellers' time."

Pravesh Mistry, Head of Global Sales, Notion

[翻译失败，原文如下]

### Joining the sales team, and learning the real reason more research = more impact

After some days of arms-length observation, Bleier had a few ideas about the problems the sales team was facing. But to really validate those, he’d need to fully embed within the org.

There was some back-and-forth on length of the embed, but they decided to try it out for a month and revisit if Bleier and the sales team weren’t getting value. So Bleier wrote a short proposal and passed it up to Mistry and Notion’s CRO and its co-founder, who quickly approved it. “Notion is very bottoms-up,” he says.

Bleier spent a month as a full-blown BDR. He had a desk on the sales floor. He carried a quota with named accounts. He listened to sales calls, joined meetings and learned about objection handling. He interviewed reps and managers and leadership. Even his work hours changed, coming in earlier like the rest of the sales org (a contrast from the often-later hours of an engineer).

He developed a habit of frequently sharing with Mistry new things he’d discovered. “He’d say, ‘I’m not going to stand for this copy-pasting. It’s ludicrous work to be doing. But the sales team says that they’ve got to close deals and don’t have time to figure out a better way to do it,’” Mistry says. “Theo wanted to address the root cause.”

After a few weeks, he pulled Mistry into a room that had a whiteboard scrawled with his learnings.

"It’s a very simple taxonomy because all the steps depend on each other,” says Bleier. “It’s easy to focus on down-funnel messaging. But it doesn’t matter if you have the best email in the world if you don’t reach out to the right account that fits your wedge and you don’t reach out to them at the right time.”

Weeks of spending time with other reps reshaped Bleier’s initial learning.The reps who did a lot of research had higher success with outbound not because of better messaging — it was a better understanding of when to reach out to these accounts and prioritize accordingly.

Mistry says that Bleier’s hypothesis was different before embedding into the sales team, and then changed again after his month of being on the job.

“It starts with tiering the accounts the right way because that actually decides if you’re reaching out to the right accounts at the right time," says Mistry.

Bleier says that if he didn’t actually do the role of a salesperson, he would’ve spent a lot of time “bike-shedding,” which is a way engineers describe working on the wrong, or less important, problem. “I think I would have built something that was focused on account research, but we learned that wasn’t the most important problem to solve,” he says.

## Fixing papercuts & making new bets

The tools Bleier created were rooted in his framework. “Let’s go back to our sales black box. You want to sell, you want to close deals. The black box is where you put in names of companies and take out different ways to engage them and get them to talk to you,” he says. “Inside that black box is this algorithm of right message, right person, right company, right time.”

In his stint as a BDR, he learned about the tool fatigue reps experienced, so he wanted to make sure that anything he introduced would actually be useful to them — thankfully, he gained goodwill within the sales pod and they were more receptive to the tools he created. “I had been on the floor, I understood these problems. That got me in the door,” he says.

He says there are two building approaches: papercuts and new bets. “You can fix papercuts, which improve how you’re doing an existing process. Maybe you want to move faster but you’re not ready to completely rethink the process. New bets completely reinvent how you’re doing something,” he says. “I ended up with one project for each.”

### Chrome extension

This was the first thing Bleier built — which fixes the papercut, copy-paste problem he observed early, quickly pulling inputs from other tools to help reps iterate on messaging for a specific prospect.

A rep might be writing an outbound email, with pieces of context scattered across tabs: their name and company on LinkedIn, notes from previous calls in Notion or Salesforce, Outreach where the email actually gets sent. Instead of needing to repeatedly copy-paste info from these sources, the Chrome extension pulls them into an email draft.

“This started as a rinky-dink little prototype I vibe coded at my desk in the sales pod,” he says. “Almost the entire team adopted this within three weeks of me building it.”

But the hard part here wasn’t actually getting the tool to work, it was deploying the Chrome extension to every sales laptop, which required some changes to mobile device management configuration. “I’m very grateful to our data team. We have a huge team of people who focus on compliance and told me in advance, ‘Here’s the data you’re allowed to use for sales and marketing and here’s what you’re not allowed to use,’” says Bleier.

One interesting thing about the build of the Chrome extension was that Bleier knew he wouldn’t be able to maintain it going forward. “If AI is going to generate all code, software needs to be built in a different way. We’re not there yet. But you need to pretend like you can never work on this thing again after you write it. Make sure it’s maintainable. Write comments,” he says. “For the Chrome extension, I went back over and refactored a whole bunch of that code because I knew that I was going to work on the next thing.”

### Salestino bot

![](/images/posts/7f94e4304191.png)

That next thing was the new bet that ended up being the most impactful. Bleier created a suite of tools he called “Salestino bot,” which automates the parts of his right messaging, right person, right company, right time framework. Salestino bot gives reps specific product signals they use to better prioritize which accounts to reach out to (at the right time) and provides them with customized messaging to edit and use in that outreach.

To build it, Bleier hung up his sales badge for two weeks, retreated back to the engineering floor at NotionHQ, put on his headphones and prototyped — ending up with a custom internal tool.

Product data was its most important input, using Notion's very sophisticated data warehouse and general analytics setup. “You can write SQL queries to find the set of accounts you want to target,” says Bleier. “So I sat down and thought about the types of notifications we’d want.”

It was this product data that’d be the signal for when to reach out. He determined that (among other product signals), if a new Notion workspace was created within a sales-assisted account, a rep should probably reach out to this person; so he wrote an SQL query to get these workspaces. “Without the right signals, you’re trying to solve the prioritization problem on your own,” he says.

But Bleier reminds us the steps in the framework are connected, so “right time” — even if it’s step zero — wasn’t all the reps needed. To better prioritize accounts, there’s still a fair amount of research required. “The basic thing you can do is just immediately send a rep a notification that someone created an account, but the primary thing you’re trying to figure out is if you should actually reach out to them,” says Bleier. “You’ve still got to do the research on the person and the company. It’s very time-consuming.So you need both to be automated in order for it to be useful,” says Bleier.

[翻译失败，原文如下]

The next step was building a research agent to gather relevant information on the company and the person reps would be reaching out to. This came down to a decision of using a more limited dataset versus access to the open web. “One solution is to give the model access to an internal tool using a very limited set of parameters — like providing first name, last name, email,” he says. “Another solution is to give it access to the open web. In that case, I might find something my limited data sources will not. But if I give the model instructions to find information on a person, I might spend 15 search turns digging from different angles to figure out who this person is or if the information is going to be accurate.”

In the end, the open web won — by constraining the agent around the number of times it could run searches so it didn’t go off the rails. “I wanted a research agent that was very constrained in the sources it looked at. It also needed to plug into the rest of the system,” he says.

So he built a very simple GPT-5 agent, spending almost two weeks trying to get it to work. Constrained parameters help reduce noise and hallucinations, lead to faster results and reduce the need for definition control — but they were also a tricky problem to solve. For example, the agent needed to disambiguate between companies that might have the same name and pick the correct one. And when searching the open web for notable company news, Bleier had to very specifically define “notable.”

With the research report in hand, the next step was writing emails, giving reps kickstarters with messaging they could use in outreach. “The number one thing that’s useful with the signals is prioritization. But number two is research and then customizing messaging based on those first two steps,” Bleier says.

For example, this messaging agent has access to every single customer story Notion has ever created, so that when a rep reaches out to a customer, they’re providing the most relevant one (instead of wasting time trying to find the right one). Bleier also created a prompt for the agent to write strong emails, full of his learnings from spending time doing exactly this type of cold outreach. The agent provides the rep with three different drafts of an email for them to choose from and customize.

“We go to the rep with: this is what just happened in your account. Here’s all the information about the company and person. Here are some suggestions for messaging you can send,” Bleier says. “We don’t want to send irrelevant information. It’s very important to us that there’s a human in the loop.”

All of this comes in a single Slack message. “But I’m sure people are familiar with what happens when you have 20 messages pending in a DM. It sucks. So we’re working on a better solution for it,” he says.

![Salestino bot dashboard](/images/posts/7709f81a5f26.png)

While it’s early days for the tool, it’s being tested and used by about 30 sales reps. Bleier says an informal survey he sent out shows that people are finding it very useful. But interestingly, he and Mistry didn’t set out with specific metrics the tool should achieve. “This is the way we build products at Notion. Show it to customers, put it into beta and then we’ll look at the metrics,” he says. “If you start with ‘was this worth it’ too early on, you won’t get the insights that you need to figure out what’s important. And I probably would’ve built something less helpful and wouldn’t have gotten to something that we’re as enthusiastic about.”

## Right hammer, right nail

Mistry could’ve easily thrown more tools at the problem but instead, worked with Bleier to figure out the right problem to solve. “Don’t make decisions from the armchair. I need you in the arena,” Mistry told Bleier. From the outset, it seemed that AI would be able to help write better emails or give reps faster research — but only creating tools for those problems wouldn’t have addressed the root cause.

In aprevious essay, we spoke with Shopify’s Head of Engineering, Farhan Thawar about how the company is bringing co-founder and CEO Tobi Lütke's publicly-released internal memo to life. One of the company’s insights was that Shopify wasn’t just speeding up processes; AI forced them to completely rethink those processes: “Anyone can see the value of AI speeding up processes. But the non-obvious value is you discover that your process should be done in a different order or should be done with different assumptions. And that’s when something clicks,” Thawar says.

Notion took the same approach, finding the right problem to solve by thinking about the core elements of the process, not just haphazardly introducing AI in hopes of speeding things up. “We took this approach because we knew that jumping right in and building tools haphazardly would’ve put us in the bad spot,” says Bleier. “We slowed down to speed up.”

---

> 本文由AI自动翻译，原文链接：[Context Before Code: How to Build Better Tools](https://review.firstround.com/notion-ai/)
> 
> 翻译时间：2026-10-11 08:05
