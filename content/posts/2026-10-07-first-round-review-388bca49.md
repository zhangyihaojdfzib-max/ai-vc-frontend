---
title: 'Scale Smarter, Not Bigger: How Linktree is Using AI to Accelerate'
title_original: 'Scale Smarter, Not Bigger: How Linktree is Using AI to Accelerate'
date: '2026-10-07'
source: First Round Review
source_url: https://review.firstround.com/linktree-ai/
author: ''
summary: '[翻译失败，原文如下]


  A few weeks ago,Farnaz Azmoodehsaw the flash of a Slack notification on her screen.
  For months,Linktree’s CTO had been tracking the engin...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-08T08:38:28.297676'
---

[翻译失败，原文如下]

A few weeks ago,Farnaz Azmoodehsaw the flash of a Slack notification on her screen. For months,Linktree’s CTO had been tracking the engineering organization’s AI usage through a dashboard she’d vibe coded to better understand adoption and where to bring in new tools.

“We have this amazing principal engineer who’s been the most prolific in terms of just the pure number of PRs he gets in every week. It’s really remarkable how fast he is able to ship,” Azmoodeh says. But when she got the automated Slack ping to check the dashboard that day, for the first timeshe saw a new name on top of the PR leaderboard: Devin.

The AI agent— the one Linktree’s engineers had likened to a “bad intern” only months earlier — had outpaced a top human developer, sort of. “Of course, the complexity of the PRs that Devin was contributing to were much lower than what our engineers typically accomplish day to day, it's not a real comparison. At least for now though, AI is handling the most repetitive and low-leverage aspects of software engineering, freeing developers to focus on higher-order problem solving,” Azmoodeh says.

But still, the symbolism mattered. For Azmoodeh, it was an early proof point of a new strategy that Linktree started pursuing at the beginning of the year.

Going into annual planning for 2025, Linktree’s executive team found itself at a bit of a crossroads. Linktree had started as a simple link-in-bio tool, but over the years, it has quietlyevolvedinto a far more ambitious platform for creators and businesses to run their whole digital presence, supporting 70 million users.

“We’ve been building out a massive array of functionality. But Linktree is a prosumer product. So things really depend on shipping product at high velocity,” saysJiaona Zhang, who was Linktree's Chief Product Officer during this transformation (she has since recently joinedLaurel, the AI-powered time-keeping platform).

More specifically, the Linktree team has been building out a two-sided marketplace. On one side, creators needed to be able to monetize through affiliate commerce (earning commissions from third-parties like Amazon, Walmart, and Target) or selling their own courses and digital downloads directly. On the brand side, Linktree wanted to enable companies like Hulu to pay creators for link placement and also run influencer campaigns at scale, even messaging creators directly within the tool.

“When you're building a platform, you don't have the ability to carve off one little sliver. We couldn’t go an inch deep and a mile wide. We needed to be more like 10-feet deep across all these areas to really pull it off in a compelling, high-craft way,” says Zhang.

That expansive product surface area initially pointed toward significant resourcing needs, which is why early plans called for sizable headcount growth in 2025.But rather than default to scale, the team decided to experiment to see if they could stay lean.

“At our sub-200 person size, we were at a sweet spot where we hadn’t yet run into some of the common cultural and organizational challenges that come with a larger org, and picking up new skills was still relatively easier. We bet on being able to drive more impact by leaning into AI more aggressively, instead of paying the price of scaling,” says Azmoodeh.

Now, more than halfway through the year, the strategy seems to be bearing fruit. Here’s a snapshot:

![Instead of significantly increasing, headcount has remained steady throughout the year at 190 total, with 100 engineers.  75% of engineers are using Cursor daily, while the rest of the org uses other tools of choice. Devin is generating roughly two pull requests per engineer per week.  Product velocity increased to one major Tier 1 launch per quarter and multiple T2’s in between. Customer support tickets naturally climbed in step, climbing up by 80%. But that increased support volume was manageable with new tooling, with Lorikeet handling 50% of customer support tickets and targeting 75% by year-end. Content moderation costs dropped 25x (from $520K to $20K annually) by switching to Gemini 2.0 Flash. ](/images/posts/ff270370aab1.jpg)

But getting to this point required more than just slowing down hiring and sending out an “Everyone needs to use AI” memo. We sat down with Azmoodeh and Zhang to unpack precisely how Linktree pulled off this change, distilling what other companies can learn from their experiment.

## Try many paths, but then prune

Linktree’s AI journey had a more conventional start. “We brought in GitHub Copilot first, about two and a half years ago when I first joined the company,” Azmoodeh says.

“I generally am not a fan of having a large number of tools. It creates complexity, it increases your risk exposure. It’s just a bad idea,” she says. “But with AI, we were feeling that it was important to lean into the multitude of tools available, so we brought on Cursor soon after it was released, Replit while it was still in beta, then Devin and many more.”

Adoption of tools started slowly. For example, Cursor usage started out at 10% and stayed there the first few weeks, but Azmoodeh felt the numbers were moving in the right direction.To unlock the next level of adoption, she had a series of 1:1 conversations to find out why folks weren’t taking advantage of the new tooling.

“We realized that folks wanted to try out different tools but felt blocked. So we got much faster at reviewing AI tools with our IT and Security teams, so we could onboard them much more quickly than we normally would,” she says. “Our security and IT teams committed to 4-6 hours of review per tool once they get access to all the info they need.”

Sometimes this strategy required going the extra mile. “We tried Bolt, Lovable, Replit, and V0 — Lovable’s probably the current favorite. But for a while, there was a group on the design team who preferred to stay within Figma,” says Zhang. “So I pingedYuhkiand managed to get early access toFigma Makejust to try to meet people where they are.”

But Azmoodeh always intended to reduce the sheer number of AI tools they use. “About a year ago, it became pretty clear that Cursor was the winner for us. They’re a smaller company, they’re much faster moving. The code completion and ability to hold all of the context of the whole code base has really been a game changer for us,” she says. “And it was clear in our usage numbers as well that people were preferring it to the other tools. So once that was the case,we retired some of these other tools and encouraged the team to use Cursor as their IDE.”

Linktree is going through the same exercise for automated QA testing right now, testing out several tools but also building their own in-house tool. “Many SaaS offerings are increasingly expensive and often add only a thin layer of specialization on top of existing foundational models. Building internally can be a more frugal and precisely tailored path forward, so that’s something we’re exploring more right now,” says Azmoodeh.

## Set your agents up for success

Through this trial and (sometimes expensive) error, Linktree discovered which AI tools excel at specific types of work and which ones fail spectacularly at others — at least initially. While some companies have seen mixed results with certain tools, the Linktree team reports getting a lot of mileage out of Devin.

At first, Devin couldn’t handle the right level of complexity to be net-useful. “But there’s been a step-function change with the recent updates,” Azmoodeh says. These days, Linktree’s engineers find that Devin excels at many types of repetitive work. It’s proven particularly effective in the following areas:

[翻译失败，原文如下]

1. Prototyping new features and bug fixes:Linktree’s engineers often use Devin to spike feature ideas or test bug fixes. The output may be far from ship-ready, but it provides a solid starting point. “Having a rough implementation grounds discussions, surfaces trade-offs, and makes project estimation more accurate,” says Azmoodeh.
2. Upgrading dependencies:“We had so many dependencies across our code base that were out of date. Our Node.js version was old, and there are so many problems that come along with that. Upgrades are costly. With all these different repos, you have to go and change any APIs that have changed,” she says. “Devin does an excellent job with it. And it does even better if you do the upgrade manually in a couple of repos and then just use those changes as an example, getting Devin to update it everywhere else.”
3. Identifying and fixing security vulnerabilities:With a small security team, Linktree faced an endless stream of vulnerabilities potentially replicating. “During code reviews, it’s also good when you prompt it to look for security vulnerabilities, even getting specific about which types to look for in a code base,” she says. “Once one area is fixed and we have an example to show AI, and then we can rinse and repeat across the other code bases and repos, so that's been super handy.”
4. Debugging:"Most of the time you can just ask the agents to reason through how a bug can happen. This is still much faster than reproducing the bug, which needs a lot of setup. I’ve also seen engineers prompting Devin to use Datadog’s MCP to assess the scale of a bug’s impact,” she says.

### Get ahead of failure modes

When these tools fail, however, there tend to be more systemic issues at play. Many engineers were initially quite skeptical. And not without reason. “Linktree’s code base has been around for over seven years, with a lot of tech debt piling up. That all adds up to create complexity,” Azmoodeh says. “Fundamentally, AI learns from patterns. When those patterns are a patchwork built up over the years, results can be unpredictable.”

For example, one engineer turned to Devin for help with event logging, and found the task was basically butchered. Digging in, Azmoodeh diagnosed it as challenges with the specific’s case schema design (or lack thereof). “When I looked under the hood, I realized even a human couldn’t easily make sense of things. You need domain knowledge of what these parameters mean. Inconsistent semantics in our schema meant that AI would simply expand these inconsistencies or add to them,” she says.

That’s why Linktree’s eng org isnowexplicitly prioritizing the kind of tech debt work that will help AI. That specifically includes cleaning up naming conventions across repos.

“We’re also ensuring our APIs are complete with GraphQL specs and event schemas have consistent documented definitions. This helps avoid AI contributions that guess at a request or response shape, but then generate code that fails at runtime even though it compiles,” Azmoodeh says. “Another area is upgrading our dependencies — which ironically AI has been helpful with — so that AI tools don’t pull in incompatible APIs.”

Jiaona Zhang, Former CPO, Linktree

Another flavor of failure stemmed from not right-sizing ambition for AI projects. For example, the team attempted to automatically generate pixel-perfect Linktree pages that emulated the beautiful but more customized profiles of famous influencers likeSteph Curry.

“For something like restaurants it might work because you could find the restaurant on Google and then scrape all the info. But it wasn't consistently good, especially at the scale that we have and the number of verticals we have.” says Zhang.

For Azmoodeh, there are two failure modes here: taking a swing that’s too big or too small. “When it’s too big, AI coding agents are more likely to go off the rails and then engineers tend to give up on using them altogether,” she says. “But I also often see the reverse, where a team member only uses AI for generating tests when in reality it could have built 90% of that entire feature.The key is to constantly test the limit and develop an intuition of that jagged boundary.”

## Close the adoption gap

Still, even with all the tools available to Linktree’s engineers, actual usage wasn’t immediately off to the races. “I’m still constantly watching the numbers. When I take a step back, the curve looks impressive now, but navigating the early phase was super tricky,” says Azmoodeh.

Initially, there was a ton of pushback. “In some ways, this is like any other new technology. Engineers are a skeptical bunch, and people get very hooked on their tool of choice. I’m personally that way as well,” she says.

“It was hard for me to get used to new data and analytics tools like Amplitude and Hex which we onboarded recently, but once you are over the hump, they bring so much to the table compared to previous generation options.Old habits die hard though and helping people get over that hump is your number one job as an eng leader right now.”

This sticky habit pattern repeats itself, even within AI tooling. “We just introduced Claude Code more recently, so the jury is still out on that for us. Usage is climbing up slowly, but it’s still very new and many are already set in their ways of using Cursor,” says Azmoodeh.

Farnaz Azmoodeh, CTO, Linktree

For Azmoodeh, this required trial and error to find the right mix of carrots and sticks that would get the team to lean in. Here’s what she learned on that front:

### Pick your targets carefully

Engineering productivity is tricky to define and very gameable. “The moment you declare, ‘We’re going to be looking at lines of code,’ you’ll immediately see more verbosity, more comments,” she says. “If you say you’re tracking the number of PRs, people will start pushing smaller PRs, which could be a good outcome, but you need to think through all the consequences.”

But that doesn’t mean sidestepping metrics altogether. Azmoodeh still swears by the classic Charlie Munger quote: “Show me the incentives and I'll show you the output.” That’s why in the near term at least, she chose the deliberately temporary metric of AI tool adoption itself.

“We felt it was important to put emphasis on how much you’re leaning into AI,” she says. “So we’ve been looking at adoption of the top AI tools like Cursor, Devin and Claude Code, and then within each tool, we also look at adoption of different features.”

But Azmoodeh plans to keep drilling down here:

- Usage breakdowns: “We have plans to go deeper into Devin and Cursor adoption by looking at things like diff acceptance rate, Bugbot usage, whether it was used for codegen or understanding the code, and so forth. Cursor doesn’t offer these deeper breakdowns out of the box so we have to build it ourselves,” she says.
- Bug bounty budget:“Hopefully we can bring this budget down as we prevent more and more vulnerabilities from getting into production, not just through educating our team on how to uphold security but also by heavily utilizing AI,” she says. “We’ve just started down this path, but the idea is that vulnerability detection will be CI blocking in the future.”

But this usage metrics focus has a built-in expiration date. “I suspect that within three to six months, we won’t even have to look at it anymore. The whole idea is to force ourselves to get our hands dirty and learn about the technology’s capabilities. What’s the level of complexity it can handle? Where does it fail? Once that familiarity bar is cleared, all we’ll care about is the impact that we’re driving.”

[翻译失败，原文如下]

With the usual caveat that it’s tricky to measure EPD productivity, Azmoodeh shares her current thinking on that front: “This approach comes with flaws, butwe’re planning to look at a combo of post-merge bug rate, incident rates, and scope completed per sprint, which will be easier now that we’re much more organized and managing all work via Linear,” she says. “The data will only be directionally accurate as it will rely on us assessing the size and complexity of each project correctly.”

### Leverage usage patterns to start conversations

With a sprawl of tools and a set of metrics to monitor, Azmoodeh set to work to solve visibility. Some tools provided their own analytics, but for comprehensive tracking, she built her own system.

“I built a dashboard for myself where I could monitor our team member’s usage of these tools,” she says. When she spotted engineers who weren’t experimenting yet, she crucially didn't wait for them to come around. “I built this flow where below a certain threshold of usage, I could DM the team on Slack and basically say, ‘Hey, I notice that you aren’t using these tools that much yet, can we chat so I can understand what’s holding things back?’” she says.

One nuance was how the next part was phrased: “What I really appreciated about how Farnaz framed it is she intentionally said, ‘Tell me what you don't like about it. Why are you not using it more?’ She tried to assume that the personhadtried it,just as another subtle touchpoint to reinforce the expectation that theyshouldbe,” says Zhang.

But in Azmoodeh’s experience, most engineers had a specific reason. “Many were like, ‘Oh, I don’t like it for these reasons, and I'm using these other tools instead,’” Azmoodeh says. This feedback was gold, informing her assessment of which tools to keep, which to cull — and which new ones to put on her radar.

### Reframe using agents as “management,” not magic

One pattern eventually emerged from all this data: Seniority mattered, but not in the way Azmoodeh expected.

“I think the conventional wisdom that’s developing is that these tools are useful for less experienced developers, but tend to not be meaningful for more senior folks,” she says. What I’m seeing is that the usage patterns are very bimodal. The new grads are AI natives who are leaning in aggressively,butthe more senior people at Linktree are the ones who are leaning into using AI much more effectively.”

For Azmoodeh, this is the power ofcontext engineeringon full display. “You need to be able to understand things well enough to give sufficient context in terms of how you prompt, and how you determine if a task is the right level of complexity to outsource or not,” she says. “Those are the qualities you develop as you become more senior and start leading other engineers when you become a manager. It's literally that exact skill.”

The pushback she ran into here generally took two forms. “Some folks would say,‘I have to give so much context, I might as well go and do the work myself.’ But that’s the exact trap thatevery new eng managerfalls into. Delegation is hard,” she says.

The other common refrain was that the code Devin came back with was dead wrong. “But again, that's precisely what happens when you hire an intern or a new grad. By using AI often, you’re cultivating an understanding of when to lean in because the task in hand is too complex, how much context to give, and so on,” Azmoodeh says.

### Create peer pressure through public sharing

Lunch and learns and dedicated Slack channels are becoming fairly standard tactics for pushing for AI adoption internally. (Linktree’s channel is dubbed “AI Wins and Whoopsies” to put failure and success on equal footing.) Azmoodeh and Zhang share two other methods they’ve found effective for building social pressure:

- Overhaul standing meetings into AI demos: “I shifted the product org’s monthly meetings — which used to be product breakdowns and updates on what everyone was working on — to be entirely AI-focused,” says Zhang. “Everyone would go around the horn and share which tools they’re using and what they’ve built. And there’s this social pressure that quickly develops to be able to say you’re using something other than ChatGPT. You can’t say with a straight face that you’re experimenting and trying things out if that’s all you’re doing.”
- Lead by example: “It really helps to get a couple of folks who are senior and extremely credible to become promoters, and crucially, to show, not just tell. Jiayao Yu stands out as an example. We previously worked together at Snap and he is now one of Linktree’s engineering directors,” says Azmoodeh. “He started just building things on the weekend. His first demo, which he built before even starting at Linktree, was an AI-enabled Q&A tool that would answer questions about the business or creator that each Linktree represented. Even though he’s an engineering director who’s mostly managing, he’s on the tools himself, which emphasizes how important it is to be hands-on at the company.”

## Bring it beyond the eng org

Engineering had proven the model, but that same AI-first approach also began spreading throughout the rest of the organization, with some notable results.

### Start with the obvious wins

Customer support typically makes for a good first beachhead for AI tooling, and Linktree was no exception.AI now resolves 50% of customer support tickets, with plans to hit 75% by year-end. More importantly, Linktree can handle their 80,000 weekly signups without having to significantly scale support hiring.

“We ran POCs with Fin AI, Decagon, andLorikeet,” says Zhang. Measuring on the quality of FAQ responses, ability to customize and integrate with other tools and cost, Lorikeet was a clear winner. “It won because of the ‘knobs and dials.’ We could work with it and make it our own. Everyone tried to sell flexibility but with global rules. There’s more setup required with Lorikeet but it wins long term.”

Content moderation delivered another clear-cut victory. With 70 million profiles to moderate for inappropriate content, Linktree faced a challenge that could have easily required hundreds of human reviewers.

“We were relying on basic linear regression models that hit accuracy in the mid-70%. We knew LLMs could push us into the high 80s or low 90s for precision and recall, but it was pretty cost prohibitive at first,” Azmoodeh says. “For one specific adult content classifier, the cost of automated classification of all our links using state of the art LLMs was $520K last year.”

But then smaller, more efficient models emerged. By switching to Gemini 2.0 Flash, Linktree achieved the same performance boost as more expensive models, while the cost dropped 25x to $20K.

### Blur the lines between roles, but bridge the vibe coding gap

There’s also been a general role blending between product, design and front-end engineering, with a focus on equipping non-technical folks to be able to push code.

“There’s been a lot of tech debt in the link builder area of our product, and this designer was feeling very frustrated with it,” Zhang says. “And our best front-end engineer happened to be on his honeymoon, so the designer literally just built what he was envisioning with Cursor.”

Given the whole team has access to dev grade AI tooling, another PM was able to help scale creator partnerships efforts up by creating a system to message thousands of creators. Stringing together Sendbird, ChatGPT, Braze and other systems, Linktree’s now able to identify the top creators to work with, custom create messages and then automatically DM or email them. The PM also came up with an entire new rewards program for creators that she prototyped and automated behind the scenes.

[翻译失败，原文如下]

Still, it’s not as simple as turning these tools loose in the organization. “It’s really easy to go from 0 to 1 with vibe coding tools like V0 or Lovable. And it's easy to go from 99 to 100— meaning you can use Cursor or Devin to fix a label or move a button,” Zhang says. “The hard part is bridging that gap from your prototype to production-ready code.”

After cycling through multiple prompts in Lovable to nail the prototype, Zhang and designers and PMs on her team started asking the tool for something specific: “Give me a prompt that’s a summary of all the back and forth we’ve done.” They then take that consolidated prompt to Cursor or Devin, which are connected to Linktree’s actual repositories. “You avoid having to go through the same iterative process twice. The summary becomes your blueprint for the real implementation,” she says.

This approach has been particularly powerful for non-engineers. "Lovable is way more accessible because you don't have to spin up an IDE. So Linktree’s designers and PMs can vibe code their ideas, and then we have a clear path to turn those prototypes into actual PRs,” she says.

### Rethink the PRD

“Prototype > PRD” is a consensus view these days. But for Zhang, there’s a nuance that’s getting lost in this conversation.

“The new PRD isn’t the prototype, it’s the prompt.That’s the mindset shift you’re actually making here. And that prompt is only good if you’re very clear in your written description, which is still in English, not pixels,” she says. “You need to have the right degree of accuracy in what you’re describing as you’re prompting Lovable or Figma Make to give you the right prototype. Every ambiguous phrase or fuzzy requirement immediately shows up in your prototype.”

“We still have PRDs at Linktree, we just make them much shorter— one-page ideally — and share them along with the prototype for that additional context. And even that you can use AI to help generate,” says Zhang. “Let’s say you cycled through a bunch of prompts, tweaking back and forth to get to what you want the prototype to look like. What I do in my process now is I go back and say, ‘Now take all these prompts and generate a concise one-pager version of this prompt.’ And that’s the start of your new PRD.”

The most eager adopter of prototyping at Linktree has surprisingly been the CEO,Alex Zaccaria. “It’s really unlocked something, because he’s a very visual person, and he would previously be sitting there explaining his ideas to us and now he can just go show us,” says Zhang.

The power of this shift was best captured during a critical pricing and packaging overhaul. “When you do pricing and packaging for a company like ours, you need the founder's mind on it. Your roadmap flows from there, it impacts how you position the company, there's just so much that comes out of it,” Zhang says.

For weeks, the globally distributed team spun their wheels. “We were going back and forth like, ‘Should we test this?’ and then Alex would be like, ‘No, that's not what I had in mind.’ A lot of this stems from the fact that the way you write a strategy document on pricing and packaging is different from how you actually display the package,” says Zhang. “It sends a certain signal if the free plan is positioned on one side, or if all the plans are hidden and just one is emphasized. And it’s hard to get at that with only words.”

Using Figma Make, Zaccaria was able to quickly put together his own visual for how he thinks about the plans, in Linktree’s signature style. The prototype revealed dozens of micro-decisions — visual hierarchy, emphasis, flow — that was hard for a PRD alone to adequately convey.

![Linktree CEO's Figma Make pricing prototype](/images/posts/4b57ba889367.png)

## The bottom line

Linktree’s 2025 annual planning exercise resulted in a bet on scaling the talent of their current team utilising AI instead of solely relying on scaling headcount. In a show of just how much progress they’ve made, 2026’s planning process will be powered by AI itself, automating much of thescorecard ritualthey use for example (see more on that topic in thisannual planning deep-divefrom Zhang over on The Review).

There are a few notable takeaways here. One, the turning point came when the company slowed its hiring pace. “When you create that kind of constraint, you’re pushed to fix the underlying system and improve output, not just add more people to work around inefficiencies,” Azmoodeh says.

Two, while the tools exist and the playbook is emerging, adoption won't happen organically. Someone has to drive it. “The tools are there, but tools don’t change habits. You need to be willing to champion an unpopular path for a few months. Track the usage, send the annoying DMs, never stop talking about it in meetings,” she says.

---

> 本文由AI自动翻译，原文链接：[Scale Smarter, Not Bigger: How Linktree is Using AI to Accelerate](https://review.firstround.com/linktree-ai/)
> 
> 翻译时间：2026-10-08 08:38
