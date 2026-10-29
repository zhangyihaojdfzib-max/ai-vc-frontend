---
title: How Supabase became the essential infrastructure for the AI era | Paul Copplestone
  (Co-founder, CEO)
title_original: How Supabase became the essential infrastructure for the AI era |
  Paul Copplestone (Co-founder, CEO)
date: '2026-10-29'
source: First Round Review
source_url: https://review.firstround.com/podcast/how-supabase-became-the-essential-infrastructure-for-the-ai-era-paul-copplestone-co-founder-ceo/
author: ''
summary: '[翻译失败，原文如下]


  In this episode of In Depth, Brett sits down with Paul Copplestone, co-founder and
  CEO of Supabase, the open-source Postgres platform now...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-29T08:14:59.269655'
---

[翻译失败，原文如下]

In this episode of In Depth, Brett sits down with Paul Copplestone, co-founder and CEO of Supabase, the open-source Postgres platform now serving more than seven million developers. Before Supabase, Paul launched a Thumbtack-style marketplace in Southeast Asia and co-founded an office-management startup called Nimbus, experiences that taught him to separate fundraising from building and to find product-market fit before blitzscaling. He breaks down how a single tagline change for Supabase unlocked product-market fit, why he runs a fully distributed async team with near-zero attrition, and how he turned PLG signals into a product-led sales motion comped only on incremental uplift.

In today's episode, we discuss:

- How changing one tagline helped Supabase go to #1 in Hacker News - an early sign of product market fit
- Why Paul ran Supabase like it had only $100K in the bank despite raising real money
- How Supabase rode three distinct AI waves, from pgvector to Bolt and Lovable, to Claude Code
- Why Supabase built a sales team comped only on the incremental uplift over a control group
- What the Toyota production system's "kaizen" taught Paul about unblocking a scaling team

References:

- Ant Wilson:https://www.linkedin.com/in/ant-wilson-46179937
- Bolt:https://bolt.new/
- Claude Code:https://www.anthropic.com/claude-code
- Codex:https://openai.com/codex/
- Entrepreneurs First:https://www.joinef.com/
- Firebase:https://firebase.google.com/
- Lovable:https://lovable.dev/
- MongoDB:https://www.mongodb.com/
- Next.js:https://nextjs.org/
- PostgreSQL:https://www.postgresql.org/
- Supabase:https://supabase.com/
- Thumbtack:https://www.thumbtack.com/
- Y Combinator:https://www.ycombinator.com/

Where to find Paul:

- LinkedIn:https://www.linkedin.com/in/paulcopplestone
- Twitter/X:https://x.com/kiwicopple

Where to find Brett:

- LinkedIn:https://www.linkedin.com/in/brett-berson-9986094/
- Twitter/X:https://twitter.com/brettberson

Where to find First Round Capital:

- Website:https://firstround.com/
- First Round Review:https://review.firstround.com/
- Twitter/X:https://twitter.com/firstround
- YouTube:https://www.youtube.com/@FirstRoundCapital
- This podcast on all platforms:https://review.firstround.com/podcast

Timestamps:

00:00 Introduction

01:32 Why Paul's earlier startups were never destined to be huge

07:14 Unlearning the "tall poppy" mindset and going all-in on async

09:54 Reverse-engineering why Supabase was an outstanding idea

12:04 The accidental Hacker News launch and tagline lesson

13:58 Where the early roadmap came from: demand vs. technical taste

17:28 Skill vs. luck, and operating like you have $100K in the bank

21:42 What actually makes a great developer experience

23:10 Solving the "graduation problem" Firebase never could

24:58 The role of open source in Supabase's success

26:10 The three distinct AI tailwinds: From pgvector to Claude Code

35:24 Supabase’s egoless, hyper-competitive open-source culture

42:58 A tactical playbook for raising capital

48:37 Product-led sales comped on incremental uplift only

59:27 The production philosophy behind Supabase’s operations

Paul:We though we're getting DDoSed at the time, actually, because we just saw this customer launching lots and lots of databases.

Brett:For today's episode, I'm sitting down with Paul Copplestone, co-founder and CEO of Supabase, the open-source backend platform that millions of developers now build on. The company started as a side project, and now, it's the backend for a huge slice of the internet.

Paul:It was obvious to me how hard it was for developers to use databases. If the problem exists, then the opportunity exists.

Brett:But it wasn't always like this. Before Supabase, Paul built other startups that never took off in the same way.

Paul:There's something painful about the chewing glass of trying to find product-market fit and you're trying everything, and sometimes, you just don't know what else to do.

Brett:When AI app builders like Bolt and Lovable launched, every new app needed a backend and many chose Supabase.

Paul:These are the tools that are using more of the CLI, MCP-type workload now happening off a base of seven, eight million developers.

Brett:In our conversation, Paul reverse-engineers why Supabase worked. He shares why he refuses to lock in customers and how he's building towards self-driving databases run by agents.

Paul:We want to build a generational database company.

Brett:He also gets into the chaos of hypergrowth and how he tackled the success problems that come with scaling too fast without losing himself in the process.

Paul:I want to look back at the end of my life and think, "Oh, not only did I build a big fucking company, but I also did it my way."

Brett:Let's dive in.You worked on multiple companies before you started Supabase that were seemingly less successful than this company, depending on how you measure it. What are your reflections on the value of a good idea or a few of the foundational things that clicked into place with this company that didn't click into place with other companies?

Paul:Well, I think a successful startup takes a thousand things to go right and a lot of luck. The first ones were probably never destined to be as big. The ambition behind them was not as large, so they could have been successful in a local maxima.

Brett:Why is that?

Paul:Well, they're geographically constrained for starters. The first one was a marketplace in Southeast Asia. The reason why that first one didn't go well was it didn't have pure product-market fit. We're modeling against one here in the US actually called Thumbtack, which is, of course, markets are all different the way things operate. There's a different mentality to how you do things in the US versus, say, even Malaysia or Thailand.

Brett:When you were working on it in the early days, did you have a less ambitious mindset-

Paul:No.

Brett:... versus where you started? All of that was ... You're just saying that it turned out to be less ambitious, not the intention.

Paul:Yeah. I mean, the mindset's still the same. I mean, the ambitiousness, could we build that to be a hundred-billion-dollar company? No. So I think my ability to assess a market dynamic is much more honed now. In fact, I think I even worked, I would say, harder on that when I was building 90-hour weeks or something like that to make it work. So we're definitely ambitious, and I learned a lot from that one. I had a co-founder who was extremely ambitious, great salesperson, extremely good at fundraising, and all of these things were assets that I picked up from him.

Brett:What about the second experience?

Paul:Yeah, it's funny because the journey trickles on to Supabase. My country manager for my first startup said, "I'm building this company and it's going to be ..." He explained it and it's like an office management tool, but also owning the services. So very similar to the first one, but fixing or de-risking a lot of the things that were in the first one. And he had to moat some permission from the government to do certain things. So that was good. But I said to him, "Look, I'm a developer. I'm going to launch a DevTools company."

Brett:That's what you were thinking about doing at the time.

Paul:Yep. Yeah. He said to me, "Well, just give me a couple of years. Come brainstorm, build it and just build with us on the side or inside." And so that's actually where I started building. I took a lot of those learnings from all those companies that I was launching. And then I honed the tech stack and I built the second company. It's called Nimbus. I built Nimbus with the same tech stack, and that tech stack now is what is Supabase.

Brett:Talk more about how that actually unfolded.

[翻译失败，原文如下]

Paul:I was building a chat application. As I said, many of them, actually in Southeast Asia, operate via messaging. And so essentially, what I was building was a platform, but it felt more like a chat app. We were using Postgres for most of our database workload, but then for the chat side, I was using Firebase because it's got this nice real-time functionality. It's very cool actually. But as we started scaling up, I had some scaling limits on that particular piece, and then I thought, all right, I have to figure out how to fix this. And then I was looking at our tech stack and Postgres, and I realized I could build this real-time feature on top of Postgres itself. I needed to use this framework, a language called Elixir, framework of Phoenix, and I built it and I open-sourced it, and it worked very well for our use case, and it started getting some traction on how can you use just the open source part of it.And so I thought, okay, timing seems good. There's interest, developer interest. I know what I want to build. I want to build a database startup. I knew I wanted to do it on Postgres. And so when all of these things just lined up, I reached out to my now co-founder who I had met at Entrepreneur First, and I lived with him and I said, "This is what I'm going to build." I thought at the time, again, to de-risk things. I thought I'm going to build the most Y Combinator-friendly team and apply for YC, and that will help from a DevTool point of view. I think that's the pitch that actually convinced him. He really wanted to go to YC. And so we started and we were fortunate to get into YC very early on.

Brett:When you came across this opportunity and you were starting what is now Supabase, was it very obvious to you and was it high conviction, or was it like, "Well, this seems interesting. I could see it going ..." What was the feeling in your own psychology at the time?

Paul:It was obvious to me how hard it was for developers to use databases. Yeah. And I just knew if the problem exists, then the opportunity exists. What I couldn't have picked is how successful Postgres has been. We definitely rode that wave, and hopefully, we contributed a little bit to that wave as well. So in that way, we've had a lot of tailwinds and we've been pretty deliberate to try to capture as many of these tailwinds as possible. So each time, it feels like the opportunity's getting bigger and bigger. I felt like there was definitely a big business in it, but probably not or definitely at the time not at the scale that I know we can reach now.

Brett:You were talking a little bit about this, but how were you different as a founder when you started Supabase versus when you were working on your first company?

Paul:Well, first of all, when I started on my first startup, I don't know how familiar you are with the Kiwi mindset, the New Zealand mindset. I'm from New Zealand. And we've got this thing called tall poppy where you don't ever want to be the tallest poppy because then you get cut down. So you always make yourself smaller, or I don't know, it's a hard culture to explain. I quickly unlearned that in my first startup. I remember my co-founder, as I said, he was very good at fundraising. I learned a lot from him how to fundraise, and it's a little bit like sales. It's slightly different, but I had to learn that. So actually, that's one thing. I treat the process of fundraising and building a business as two distinct things. Now, hopefully both of them, you do phenomenally, but you could do one or the other separately quite well. I learned really the dynamics of fundraising, investors, why it's important, when to raise.I also learned the value of not blitzscaling too early. So find product-market fit before you blitzscale. I probably learned that lesson a little bit too hard at Supabase. We're very small, and we've got to ramp up really fast for our scale. Yeah, I held that lesson too long, I think, at Supabase where we've got a lot of growth across everywhere and a lot of people are stretched. But it was good to see that internally at my first startup, like how we hired maybe too fast on too many areas that didn't matter.What was good on that one, my co-founder was very diligent about keeping the bar extremely high. That one has always stuck. I think that one's universal, if you can keep the best people. It was at YC yesterday and someone was saying, "Should I take someone who's high agency, or should I take someone who's high performance?" And it's very clear to me it's both. You just don't compromise on any of those.So we, at Supabase, are a fully distributed team. We have no offices. So we're in three countries in my first startup, and we had an HQ in Malaysia. And whenever I'd visit Singapore or Thailand, they'd always feel like decisions were made away from them because the gravity of the co-founders is too high. Of course, everyone went fully distributed during COVID, and then there was a big push to go back in or do hybrid. It was very clear to me. No, you don't half-ass it. You just go all in if you're going to do remote. We went completely async, and now, actually, I think it's a superpower for us.

Brett:What about if you take a crack at reverse-engineering why Supabase was an outstanding idea that maybe you didn't even fully grok at the time, but now you have the benefit of hindsight? And so dissecting it and saying, "Okay, here's actually why it turned out to be so good." How would you articulate it?

Paul:With the benefit of hindsight, lots of tailwinds, that's always good. Hard problem to solve is also good. We have competition, but it's not like a competitor can spin up. So for example, now, if I was building in the AI area, there's a lot of things that are getting launched fast. That means a competitor can get launched fast. Where we are is not in the build space. We're in the operate space. We operate the databases. So it's not just enough to launch something. You have to prove that you can operate it over many years and do it at scale. So there's this kind of moat that was important.We also leaned very hard into our community and the PLG motion. So that was good, not trying to split our focus between let's go upmarket really fast. We've just kept our finger on the pulse of the community and the PLG motion, even though we get a lot of pressure all the time to move really fast across and win all types of workloads. And this was important because, as well, Postgres is so versatile that it can serve anything that enterprises wanted. You can use it for this thing, that thing, whatever. And so we're often trying to find out exactly what their ICP should be and only build increments on top. So it's like a onion getting larger rather than splitting our focus all around. So from this point, I think it was beneficial that we just had a lot of market drag, a lot of market pull anyway. And in my earlier startups, when you don't have product-market fit, you lose focus because nothing is clearly winning. So you're jumping around a lot.

Brett:What's your definition of product-market fit?

Paul:I don't really have a definition, but you just know it, like when things are growing a lot faster and when you're doing nothing and it continues to accelerate. That's how it feels.

Brett:What was the very first moment that you felt that real pull? What was the product maturity at that point? What's the story if there was a day or a number of days that it felt like the ball started rolling down the hill?

[翻译失败，原文如下]

Paul:I can peg a few key dates at the start of 2020. We got into YC, and we did this accidental launch. Someone put us on Hacker News, and usually you do a launch Hacker News. Someone put us on Hacker News, and it was the day after I changed the tagline. I changed the tagline to "Open-source Firebase alternative," and someone put it on Hacker News that next day, and immediately, it went to the top of Hacker News. It was very upvoted, lots of comments. And that was the first lesson in that product-market fit often is just like a product-positioning fit. Sometimes, you can just change some things, and that's all that matters. And there are some people in the world that want whatever you're building, even if it's a niche product. You just need to find them and tell them in the right way. So that was the first thing, a good lesson as well just on how to position things for developers.From there, a lot of people in those threads said, "Oh, we really need Auth." This is a product that Firebase have because we now put the Firebase positioning out there. They actually wanted these other things. And of course, I only really wanted to build the database offering, but Auth made sense because I thought we could do a better product for the market by putting your Auth users in your Postgres database. Actually, something that I never really understood from other Auth providers keeping your users outside your database. So we did it and we managed to launch that before the Y Combinator demo day. And again, we just saw the slope of the chart change, and we thought, "All right, these launches are clearly things that work." So off the back of that, we said, "All right, demo day's gone. In three months time, we'll just move from Alpha to Beta, and we'll say all the things we've shipped on this one day."

Brett:Just keep launching.

Paul:Yeah. And we ship, ship, ship. And then on that day, we just rolled everything up into a single page and put it on Hacker News, and it went up again, and we thought, "Oh, that's great. Well, we launched, and why don't we just turn this into instead of one launch, can we do a launch every day for a week?" And then that was our first launch week, maybe I think four months later. Again, we just kept seeing these 20% bumps each time we would do these product launches. So it felt like sometimes inside those launches, there were some things that fired really well, some things that didn't. You can tell those ones that have product-market fit just have direct demand.

Brett:Did the early roadmap come from people just saying, "I need this and I need that." Or did it come from more of a technical taste perspective, like you had an opinion on how this thing should work and what we should build and so you just manifested it in the world?

Paul:A bit of both. Yeah. It was a hybrid. So we knew as well, again, because of our positioning, all the things that Firebase had, we didn't want to do all of them because we wanted to keep the database side. And I just thought of some ways to do it, or as well the team had some ideas that they wanted to build and they seemed to fit. And we largely think in primitives. We try to offer just pure primitives rather than products, and the primitives can be mixed and matched to allow developers to do many, many things. I think the only one that was really, really demanded from the community was functions. We went through our Edge Functions. We went through three launch weeks and people kept saying, "Oh, I hope they launch Edge Functions this launch week." And we were thinking, "No, we don't want to because we're a database." And we're telling them use Next.js or use whatever you're using. In the end, the demands were so high that we had to launch it, so yeah. And this turned out to be a great product.

Brett:When you think about the first year building the first product, starting to launch, what felt at the time very hard and what felt somewhat easy?

Paul:I mean, it was a grind, lots of [inaudible 00:15:37]. It didn't really feel that hard if I'm honest. Once we felt like we had product-market fit, I mean, it's all problems of scale, right? It's really just about navigating community and feature requests and building as fast as you can. And these things are largely exciting, and we had a lot of people joining the team. I remember this is how I know it wasn't necessarily hard.A lot of those ex-founders were coming to us and they were burnt out. I remember one in particular who was burnt out from doing his own company for five years and we said, "Ah, just come help us. We've got so much work to do. Just spend a bit of time if you want, take a break from your own company." And he came in and instantly, he was reinvigorated because he no longer had to deal with product-market fit. It was just solving these cool technical problems for our customers, and he joined Supabase. Time and time again, I saw this from founders where they were burnt out from their own thing.

Brett:They were burned out from it just not working, not-

Paul:Just not working. Yeah.

Brett:... working on it.

Paul:There's something painful about the chewing glass of trying to find product-market fit and you're trying everything, and sometimes, you just don't know what else to do maybe because there is no way to get your vision into the hands of the right people, but we didn't have that. It was just problems of shipping as fast as we could.

Brett:What is your reflection now on the interplay between skill and luck specifically and originally getting into product-market fit?

Paul:Well, it depends on the time of the market. The things that I'm uniquely served to solve might not be perfect for the timing. What happens when you get product-market fit is usually ... Or even the funding, like for example, if I just went out and raised a lot of money, then the temptation is, "Okay. Well, let's hire lots of people." 10 people don't help you solve product-market fit, right? You have to iterate, you have to do it small. So we're launching a product at the moment, and there's just no engineers on it. It's just a product person engineering it, and people say, "Oh, should we staff this up?" And I said, "Well, absolutely not." They don't have the idea baked yet. And so it needs to be really a fast and tight feedback loop.What we did well and what I would do I think if I was to start again is, yes, I'd raise the funds, that's important, but I'd still operate as if I only have 100,000 in the bank account, where you just got to iterate really fast with a small group of people to try find that thing, and then you've got to be really honest about whether you actually got fit or not. As we've said, it means many things. So whether people will use something, whether they'll pay for something, whether they'll upgrade on that thing, whether they'll want to take it into an enterprise, all of these are different stages of fit that you need to de-risk.

Brett:What else did you learn, if anything, about the relationship between you as a founder and what you should actually work on? And this may be sort of too reductive, but it sounds like the first company was just not as perfectly fit to you as Supabase. Do you have any reflections on that?

Paul:I think that's okay, because as the CTO, me being a techie, of course, I want to work on tech things. But there are so many opportunities outside of the tech bubble that need to be techified. Well, maybe, we're seeing that now with AI, and that can leak out into these domains, but I don't think they necessarily failed because I wasn't passionate about the space. And in fact, the second one is quite successful. Of course, not to the degree that Supabase is, but my co-founder there's done a phenomenal job of scaling it. And I helped them a lot. I really like this space. I like helping service workers. But yeah, I'm passionate about tech.

[翻译失败，原文如下]

Brett:How do you now approach building new products at Supabase and getting those into product-market fit?

Paul:We could just push things out and people would adopt them, and we didn't have to worry about eight million developers trying something out on day one now, and also, we've got a very well-functioning business. So-

Brett:But back then, it was a little bit more improvisational and you would have one or two engineers work on something that you thought was good, the customers thought was interesting, and just put it out in the world, and that was that?

Paul:I think in our second launch week, one of our engineers had built Supabase Storage, somewhere where you could store ... I think it was storage. I can't remember exactly, but for storing files and videos and things like that, because you can't stick them in your database. I remember we're about to launch it for launch week, and literally, two hours before we launched it, he wasn't happy with the DX of the client libraries and he just rewrote them and launched them after that to be more like Supabase. So it was very much like that. We're just bouncing ideas off each other trying to make a perfect integrated suite, and we could test these things out, and we weren't too scared to put something new out into the world.

Brett:And so then how does it work today running at an at-scale business when you're building something new?

Paul:You have to be able to scale up. That's rule number one. You probably need billing on it. People will abuse things, strong security guard rails. There's all these things that you need to think about before you can really push it out. And so now, where we're moving towards is more like a pipeline. We used to have this pipeline which is Private Alpha, Public Alpha, into Beta. Now, we're thinking, well, just put it out into labs where we'll have a smaller subset and people might discover it organically, but it doesn't necessarily have to have the full marketing weight behind it. And then we get feedback from that, and then it could start moving natively into the platform.

Brett:What do you think makes a great developer experience? If you had to talk about it in the most concrete specific way or you were teaching someone like your ideas about what it means for something to be truly incredible from a developer experience perspective, what are the underpinnings?

Paul:I think the key metric is time to value. You want to get the developer to their aha moment as soon as possible without getting blocked. You know what a bad developer experience is just a ton of paper cuts where you're getting blocked all the time. You're trying to achieve a goal. You usually have a goal in mind. I want to build a to-do app and you just get stuck on three or four things and then you give up. So a good developer experience is take any one of those, whatever their goal is, and the ability to get them to that point as soon as possible.

Brett:What did you do in building the product or from a product strategy perspective to solve the graduation problem? Where I think a lot of people's early critique would be, "Oh, Supabase, great to hack on the weekends and get going." But when you're doing real and production workloads at scale, you're eventually going to move away and you guys have managed to keep just incredible customers at incredible scale. Did you think a lot about that, or did you just make the product better and better? Or what was true about what you did where Firebase, obviously that was a critique for a long time, which is a great place to get started, but not a great place to scale?

Paul:Yeah, we thought a lot about this, and it's actually, right from the start, part of our strategy. So we want to build a generational database company. We had seen many database companies come at it and say, "I'm going to build a bigger, better whatever, and then people want to use us," and they didn't really succeed. If you look back over the past 20 years, probably, the only database companies that have really managed to do well are Firebase and Mongo, and they did well because they targeted these day-zero workloads there. You would choose them before you even knew what you were going to build back when you were a developer.So we knew if we wanted to build that bigger, better experience, we first had to win the day-zero experience, like the Mongos and the Firebases. So that's where the positioning "Open-source Firebase alternative" came from, where we just pushed that quite hard because we knew that people were choosing Firebase at the start. Well, let's give them another option. And then we smuggled Postgres, and at the start, we didn't promote too much that it was Postgres. We weren't sure if people would understand it necessarily why we were doing that, or they might even say, "I don't want Postgres. I want MySQL," at the time, was more popular.Over time, it became clear the Postgres was winning. And so we slowly started to migrate our tagline from "Open-source Firebase alternative" to just this "Build in a weekend, scale to millions." And the positioning helped that slow positioning and we started doing a lot of our marketing as largely around Memes, a lot of Postgres memes, just talking about Postgres, promoting Postgres, doing what we could to promote it to developers and sticking up for Postgres where we could in the ecosystem and defending it for different things and leaning into its features as much as possible.

Brett:What is the role of open source in the company's history, and how has that been such a input driver to the success of the company?

Paul:So everything we develop is open source. We have either a MIT, Apache 2 or Postgres license, with the exception of the platform code or the billing and everything like that. But if you want a Supabase stack, you just can do docker compose up and you get the Supabase experience. We don't put any tracking on that. If you want to use it, you get it for free. We try to stack it with as many features as possible. If features aren't there, it's just because we haven't quite got around to it, and sometimes, things move faster. So there's no real strategy like, oh, we'll use it as an onboarding tool to get people on and we'll gate some features. It's really just because Ant and I have philosophically aligned with open source and I love open source. Postgres itself is open source. So we get a lot from it and we want to as well contribute back to the ecosystem as much as possible. It means that we can employ a bunch of open-source maintainers from around the world, and that's nice as well. We hope that we can employ more and more open-source maintainers, which I think is really just good for the world.

Brett:Would love you to talk more about the incredible AI tailwind that emerged for the business. What was the story behind what it was like on the inside? Because you obviously built the company, were having a lot of success before everybody started vibe coding and DIYing, and it seems like it just created just incredibly explosive growth. And then did it cause you to rethink the roadmap and direction? Or maybe you could talk a little bit about that experience kind of reaccelerating years into building the company.

Paul:I see it in three distinct phases. So phase one was the kind of everyone was getting into embeddings on the database side, vectors and embeddings. So we were one of the first to offer pgvector. In fact, I think we were the first. And helping to promote that, we put that out, and that saw a lot of uptick as well. End of 2024 was when the likes of Bolt and Lovable launched, and that was also an interesting ... That was the second tailwind. We thought we were getting DDoSed at the time actually because we just saw this customer launching lots and lots of databases or these two customers.

Brett:And they chose, when they launched, to have you all as the standard, had you just want to set up a Supabase instance?

[翻译失败，原文如下]

Paul:Yeah. The experience would be you'd come in, you click a Connect to Supabase, and it would bring back your database credentials so then you could build on top of it and you just prompt your way through a backend. It's gone through several iterations, but yeah, I mean the growth was very strong immediately.And it's always vague. I mean, in hindsight you think, "Oh, it's very clear this is the right move. We should definitely support all these platforms." But I remember at the time, even internally, people were saying, "Ah, these are just prototypes, vibe coding." Lots of slop back then, lots of slop now sometimes, but I mean, good products and bad products being built.The thing that was clear for us was that principle that we had at the start. We want to be there when people are getting started and then make sure that they never want to leave. So even if they were getting started building things that weren't going to be huge businesses, we still needed to be in that space to learn, to understand. And as well, I mean, a lot of thinking, do we need our own front end? But we're clear that we just want to be a database company. This is all we want to do.So that helps to hone what we should be in that wave, which was just this platform that will supply the backend for all of these AI builders. And that became the focus of 2025, and we built out this product called Supabase for Platforms. It looks like an enterprise offering where an enterprise might need a single pane of glass to see all their databases and which ones are secure and tools around them and usage and everything. So this was the thing that helped us. We knew that we could map this product that we're building for platforms. It was mapping to our enterprise roadmap anyway, but on different sequencing and a slight twist. So we just got to work building that product, and it was a huge growth lever for 2025.And then phase three has largely from January this year, the likes of Claude Code and Codex and everything that are just ramping up really, really fast. And these are the tools that are using more of the CLI, MCP-type workload, and we're seeing huge adoption from them, in fact, acceleration, the likes of what we saw even at YC, but now happening off a base of seven, eight million developers.

Brett:So is it just year after year, it feels like there's just so much more that you need to do than you can get done at any given point in time and it just feels quite chaotic even at this scale?

Paul:Pretty much. Yeah. So now, of course, I mean, at these scales that you start getting to, then you've got these success problems, which is just keeping up with the growth really and strange things like in certain areas, we're going to run out of IP addresses in four months or something like that, and you've got to quickly solve all these problems; otherwise, the whole business can't launch another database. Lots of things that just crop up that you have to swat away all the time, and they take a lot of focus away from that product marketing, like launch, launch, launch, but that's just the phase that we're in. I think you see it with all the AI companies now, where you're either launching a lot or your stability is not so high. And so from our point of view, now, we're just making sure that we can scale to the next 10, 100 million developers.

Brett:If you break apart the company's life into a few chapters, how has your time spent changed in any given week?

Paul:Yeah. Chapter 1 was pretty clear. I was just building, and there's a lot of fun, because as well, there's nothing more fun than building for people who want what you're building. We spent a lot of time doing that iteration. When we got to around probably 50 people, we started splitting into teams, and I was maybe doing a bit of a hybrid of managing people.

Brett:But weren't you doing a tremendous amount of recruiting then if you had 50 people or no?

Paul:We've never really had problems recruiting. I think we've got so many reasons to work at Supabase. The brand is well-loved, it's open source, it's developer tools, we're fully distributed. So a lot of the time, we're finding people who they were either building a tool that we needed or they were contributing to our repositories, and we could see that they were doing a phenomenal job, and we just said, "Oh, do you want a job?" Or a lot of ex-founders actually were just coming to us asking to work at Supabase. So I don't think we were doing a ton of outbound, if I'm honest. But eventually, that became more of a thing, and my co-founder's very good at that, and he is very keen on keeping the culture very distinct as well. So we shared that between the two of us, and we're both developers so we know what we want in terms of the culture of the company.Yeah. So recruiting became a big thing probably more last year. We had in the early stages, I said at the start, I had these scars from blitzscaling without product-market fit. And we had this idea that we'd only hire when we had a hair-on-fire problem for the first probably four or five years. And so we got to maybe 200 people with that mentality or 150 people with that mentality. And then we quickly had to change. Halfway through last year, we just said, "All right. There's just way more work than anyone can do, so we just need to get people in as fast as possible." And then yeah, hiring became a top priority, not just for us, but for all of the team.

Brett:Do you think given how much technology is changing, it's productive to spend time thinking about a three-year time horizon?

Paul:Yes, in some ways. I don't think you need to think about exactly what products to push out. We don't need to think about exactly what product to push out, but we need to think how our platform will evolve. So a good example is when we started, the company was very dashboard-first. Developers would come in, they'd launch the database from the dashboard, they'd use it. Now, with agents, they're becoming very CLI-first. And so this one's obvious to everyone, but what spills out the other side of this is, okay, what that means is that everything is very code-first, it's very Git-first.And so what we want is on the CLI, for example, one thing that I want the whole thing to shift towards is that if you use the CLI, you get the Supabase folder and that should be a pure representation of everything that's on your platform, so in code, essentially infrastructure as code inside your folder. And that should include your database schema, declarative schemas. Everything should be there for the agent to understand. It shouldn't have to reach out to the platform. So what this means is that we just get parity across every surface area that we can - dashboard, CLI, MCP. All of them should match.Then what spills out the other side of that? Okay, well, people want to branch on Git. So everything needs to be branchable. Whether it's buckets for images, your database needs to be branchable. You need to have testing environments that are very cheap and ephemeral for doing these branches. And then of course, there's the obvious stuff. If agents are building now, then they'll probably be operating in the future. So at the moment, maybe developers in looking at things whether the database is healthy or not, but of course, they probably don't want to be doing that. And that's actually where most developers don't want to spend any of their time is looking at whether things are healthy or not. So building out the infrastructure that will have self-driving databases on all vectors, the performance could be improved, the reliability, the security of it can all be improved by agents essentially, and then you can choose where you want to be inserted into the agentic flow.

Brett:What is distinctive about the Supabase culture, and why have you chosen it to be that way?

[翻译失败，原文如下]

Paul:We're completely distributed and asynchronous. We chose this one largely because of it's a bit of path dependency. We started during COVID, and then out of that, we continued on this way.

Brett:Do you think if COVID didn't happen, you would be a traditional in-office company?

Paul:I think we would have been forced to through YC. They really want you to come to SF and be based here and build here, and that is the right approach, I think, for 99.9% of the companies. I think for us, it's worked well because we're open source. We hire a lot of database people. Those people are spread out around the world, so it's worked well. Yeah. And now, it's a bit of a superpower because our attrition is extremely low, but the leaning into the async culture has helped because everything's written, everything's recorded, everything's captured in Slack or Notion, or one of our sales meetings is ingested into our warehouses.And this solves the Metcalfe's Law issue as we scale up. So because everything's there ready to be searchable, AI has solved this for us. Instead of our CFO coming to me and saying, "Hey, when is Multigres going to launch?" Then I can say, "Oh, you can just ask the AI the timelines," and he can do it without reaching out to a developer." And him being non-technical, he might not even understand all of the intricacies of a product and he can ask the AI, "Oh, can you explain it to me from a finance point of view? What does it mean?" And so this body of knowledge, the whole history of Supabase has now been embedded and you can search through it. And I think that's going to be a critical thing as we continue to scale up.

Brett:What about distinctive in the sense of how you behave, who is a great fit for Supabase and who isn't? What behaviors are celebrated? What gets someone exited? How did you land on those type of distinctive things?

Paul:First of all, of course, learned very early that not everyone are built for, async and you have to be of a certain ilk to really love it. And if you didn't love it, you just weren't going to love Supabase. So that's the trade-off. I mean, you just have to be clear about that with people, and you'll miss out on some people who just could be good, but they won't work at your company.The other thing that is really important to us is we have quite an egoless culture, which often people think means unambitious or something like that. But actually, Supabase is hyper-competitive. It boils down to the open-source mentality, especially old-school open-source people who you're out there probably grinding in public, putting out your code for free, but you want it to be top-notch. That's a certain mindset. It's hard to explain and hard to find, but you can definitely find it in the open-source ecosystem. So we've tried to really capture that ethos inside our company as well.

Brett:How do you figure out if somebody has that before they join?

Paul:You can talk about, in the past, the projects they've worked on, problems, conflicts that they'd had, how they dealt with them, even knowing how they talk about things inside the interview. Is it lots of me, me, me? Is it the team and putting the team first and things that we worked on? Yeah, there's lots of little tells, I guess.

Brett:Do you think it's relatively easy?

Paul:Well, especially for my co-founder. He's the key bar raiser, and he can-

Brett:Suss it out.

Paul:He can suss it out very well. Yeah.

Brett:Why is that so important to you?

Paul:I could be doing this business for 30 more years, and I want to work with people like that. I don't want to work with assholes.

Brett:There seems to be this kind of warm, kind quality about you in my conversation with you. Do you feel like that is who you are?

Paul:I guess so. I mean, if you feel it, then yeah.

Brett:Well, there could be a whole different side of you. I mean, the thread I'm pulling on is I find that a lot of conventionally successful and ambitious CEOs are very difficult, oftentimes cruel at times, and I'm not experiencing that in our interaction.

Paul:Yeah.

Brett:Maybe, you actually are that. Maybe it's some of that New Zealand sort of generous spirit. Do you think a lot about that at all in the context of your identity as a CEO? You're building one of the most spectacular infrastructure companies. There's a certain kind of kindness about you that comes through.

Paul:Yeah. I think probably, as you point out, because I'm from New Zealand. We're generally sort of is a kind population. A lot of CEOs I know are definitely ... As you say, they can be cruel or Machiavellian or something like this. And I see that. I mean, even with the CEOs that I interact with, or in the space that we're in, there's a lot of that. I don't think we need to be like that. I'm very much a rising tide. We'll raise all ships. The database space is going to grow phenomenally for everyone. I want to look back at the end of my life and think, "Oh, not only did I build a big fucking company, but I also did it my way and ways that people will look back and say, 'Oh, that's actually respectful.'" And I have a certain affinity to, especially the ... I've actually been doing tech for a long time. The old-school open-source mentality where people are just out there building things and putting their code there and contributing and-

Brett:Because they love it.

Paul:Yeah, because they love it. And I love what we're building and I love the space. I love seeing what people are building. I've got no qualms with anyone operating their way, but inside the realm, the sphere that I'm operating in, I just want to operate like a good human and see other good humans succeed.

Brett:And so do you think ultimately, the culture is just a reflection of you two and your values and who you want to work with and-

Paul:Yeah. I think it comes down a lot to that. And of course, then you hire a couple of people who are like that as well who are-

Brett:Self-perpetuates.

Paul:Yeah. And self-perpetuate. We've got some values like egoless, truth-seeking, batteries included. And we did this thing at our offsite, where we got everyone to rank the five different values. I'm pretty sure they ranked them in the same order that I had ranked them personally inside the company, which is crazy because one of them is just to be undeniable, means so great that you can't be denied. And we have a few examples of those people who are just titans of industry, undeniably good and yet still, the egoless part of it was the thing at the top and that was the thing that someone got off and said, "I've never been at a company that is so successful and yet puts that on top." And so you can see that you get people around you that are of that mindset.It's obvious to a lot of people. Of course, if you could have both an undeniable culture and an egoless culture, why would you not want that? I think it's just that many people think that these two are at odds with each other and they can't coexist, but that's the thing that I think is untrue. It got pushed a lot by our investors, and I just said, "No, no, no, this is not true. This is how it's going to be."

Brett:You just mentioned investors. You talked at the beginning about fundraising. If you had to teach somebody how to be excellent in raising capital, what's the little course that you would run?

Paul:Oh, little playbook.

Brett:Other than the most obvious thing as build a spectacular business that investors are tripping over themselves.

Paul:That's rule number one. If I was to do a tactical playbook, it's probably, first of all, you need to be in touch with a lot of investors; otherwise, you don't have any of your lead gen. So I probably start meeting a lot of investors. And you really treat it like a completely different play from startups. You switch mentality from builder to fundraiser.

Brett:What does that mean?

[翻译失败，原文如下]

Paul:I will normally, especially talking to developers, underplay a lot of what we're doing, but with developers, that hedging is to your detriment. In fact, they'll discount anything you say anyway. So if you tell them, "We're going to be a billion-dollar company," they'll probably think, "Well, they'll only be a 500 million-dollar company." You say 10 billion, they'll probably think, "Oh, only a billion-dollar company." Whereas with a developer, I'll always underpromise and overdeliver.

Brett:What do you think makes a great pitch? Or when you're telling your story or you're having a catch-up with someone at coffee and you want them excited about the Supabase story, what is different about that than when you're talking to customers or people that you may recruit other than maybe what you said, which is you have to be maximally ambitious because of the discount that an investor might apply in their own brain?

Paul:Believing that you are going to be that ambitious is actually the thing that matters and then sequencing of it. So it's a bit ridiculous to be ambitious and think that you're going to get there anytime soon, but where we are today and where we want to get to is going to take 10, 30 years and being deliberate about how we're going to get there and having clarity about the steps to get there is what matters to an investor. So they need to both believe that ambitiousness is true and that I or whoever it is pitching has thought about how to get there.

Brett:Do you enjoy raising capital?

Paul:Yeah, not really at all actually. It's a huge distraction from what really matters. But for a database company, it's a very necessary part.

Brett:Over the life of the company, it seems like you've been very PLG-focused kind of, at least in the early days, didn't get pulled into mega enterprise with an endless roadmap. And obviously, more recently you have companies of almost all scales building on top of Supabase. Did you think much about when you would really think about a Global 10,000 company using the product and what they needed? Was that sequenced in a specific way, or did you just wake up one day and say, "Okay, we're a big company now. We can take something like that on?"

Paul:No, the sequencing was important. So if you think of types of companies from risk-averse enterprise, which will be not even just enterprise, like bank or something like that-

Brett:Yeah, mega enterprise [inaudible 00:44:15].

Paul:... and then like indie developer right down here and then like a bunch of getting-started use cases, so like launching their bank is up here, production workloads. We started down the bottom left, and I think the big problem is that most people try to then jump ... If they're doing PLG, they try to jump as well to the top right. Whereas we just thought of adding these layers. So we're just building out. Even today, of course, we couldn't host a bank on our platform, but I've got no doubt we'll get there one day, and it's just about making sure that we're adding those layers incrementally.So an enterprise actually could come in and be one of those players, and as long as it's one of those workloads that fit within the sphere that we are currently operating in, then we're happy to work with them. Innovation workloads, for example, if they want to get started, even if they're a bank or maybe they've got a big open-source presence and they actually want to understand how they can use some of our open-source tooling, we'll chat to them about it so that we're building the relationship with them.

Brett:But at any given point in time, your resource constraint, like your ambitions and the roadmap is multi-decades long and you can only ship something, so many things in X period of time. How do you think about, do I want to make what we're doing better? Am I willing to go up and move out and sort of the visual that you represented?

Paul:Yeah. As you add more people, then the roadmap is very linear, like small and linear when we are getting started because we only had a few people, so adding products. But then you've got to add all the operational stuff plus the products and get all the certifications. So you need to build out those teams over time. We just saw enterprises coming in and they might say ... Well, not even enterprises. At the start, it was an SMB, and they'd say, "Yeah, we need this," and that type of thing to add whatever they needed might be only say three or four months on the roadmap, and so we knew that we could achieve it. And then we added and it's available then for all of the startups on our platform. Now, if an enterprise comes in, and they say something that is also going to benefit maybe a thousand customers, then we'll add it. But if they say something that's bespoke to them, then of course, we'll just end up saying no because we really want to make sure that everything we're building benefits a huge pool of customers at this stage.

Brett:What about on the go-to-market side? Has that evolved a lot?

Paul:Yes, yes. So we do have now as well an enterprise motion where they'll come in and it's more like a sales-led growth, but in terms of the sales team, their focus on that, it's very much like a 10% of focus, 20% of focus. The key focus for us is moving from PLG, which is just purely organic, people sign up, put down their credit card, to a product-led sales motion. I don't know how popular it is. I think it's not, especially not the way we do it.What we have done is take a lot of signals from our PLG motion. It could be like, for example, someone is ... They're thrashing their disk on the database side or they're hitting CPU limits or something like this. So they're probably having, encountering a problem, and we pick up a lot of these things. We call them triggers, product triggers. And then when we find one of those, if they fit some category, we actually do an automated outreach to them and email saying, "Oh, hey, look, looks like you're having this problem on your database. Do you want to jump on a call with one of our team?" If they respond, then we essentially can get this report from the usage, and we can see all the products that they're using, and we can give it to one of our success team, sales team and say, "Here's all the things that they're having an issue with and just go help them." So our sales actually just looks like support, and that's important. We actually don't really want to sell to people. We want to help them to grow if they want.Then we take the cohort of people who respond, and we rank it against all those who don't respond. So we've got that as a control group. And what we do is we measure those who don't respond, how much did their usage grow? And actually, we know quarter over quarter, it's 25%, versus those who have chatted to a success person, and that's 125%. So we can see the incremental uplift from those who are chatting to our sales team.

Brett:Is the sales team quota-carrying?

Paul:Yeah, on the incremental uplift only, which I think is the big difference from what was traditionally done. On a PLG motion, you could easily say, "Oh, get a salesperson," and so on, reach out to anyone and then you pay them on the revenue generated by that customer. But if that customer was going to pay you $100,000 without talking to a salesperson, then you don't really want to be saying, "Oh, the salesperson could actually just be getting in the way." So we only measure and, over time, want to continue to measure that incremental uplift, and then that's what they get comped on.

Brett:Are they salespeople or are they truly support or technical support or sales engineering style?

[翻译失败，原文如下]

Paul:Sales engineering. Yeah, we've got a mix of both, so account managers and salespeople and customer solution architects. And the most important thing at our stage, especially going from a PLG is very much like a very technical engineer who actually can understand the product, talk to the developer. If it's from maybe a firmographic point of view or someone who is more on the business side and they want to, say, spin up thousands of databases, then it could be more of a salesperson, less technical.

Brett:In the process of helping that customer, are they selling them new products? "Hey, have you thought about using this?" Or "We can help you with that," or-

Paul:They can do, but that's if they understand the workload and it seems relevant, then they can. But developers, they're quite allergic to sales, and so we definitely don't want anything to be forced down anyone's throat. So really, the guiding principle is just be helpful to the customer, and that's all that matters.

Brett:When you zoom out and you think about the trajectory of the company thus far, are there any other unconventional or non-consensus decisions you've made or ways you've organized the company that have mattered a lot to the success of the company?

Paul:It's literally embedded in our product principles in the docs. We don't like lock-in. We try to build on protocols and open standards. So if you ever have an issue, you can, like with our Postgres, pg_dump and take it somewhere else, it's your data. And this forces us to build a great experience and compete on that experience.To be honest, again, I don't know if this is a strategy that works. In fact, sometimes, I see it doesn't work and you never really learn the counterfactual. I don't see many people online saying, "Oh, thank God, Supabase have this principle, and now, I'm going to do everything with them." But for me, I just know if I was to use myself as a model of the customer that I want to build for, I think that's just important from the ethos of how the platform should feel that everything feels like simple primitives, protocols and can work without lock-in. And I think developers feel lock-in very early on in their investigation of a platform and it scares them away. It scares me away from things that I feel too locked in. So, yeah.And it's hard for us as well because, of course, when it comes to developer experience, I love to just do something that Postgres completely does not do to achieve some goals that we want from the product side, but it's hard for us to do it in the Postgres way. But if we can pull it off, then there's a certain elegance about it, like a craftsmanship that I think seeps through, and maybe that's the one that I can point to. I see online people pointing out how the elegance of the platform that is using these open protocols and primitives, but somehow makes it feel very integrated in it like a single product.

Brett:And that's what's really guided these decisions?

Paul:Yeah, yeah. very much so.

Brett:What have you found to be very hard? Have there been these intense pivotal moments? It feels like so much of it has been immense amount of work, but not like soul-crushing or near-death experiences, or there's a calmness about what's happened with the company you've built. I don't know how you would articulate it, but in the rear view, have there been these intense crossroad moments, these very hard, tricky things, or has it just felt very natural and just flowed out?

Paul:No, I think, I mean, it's hard to emphasize how painful it can be for a lot of people scaling. This is a success problem, but scaling for some people, like myself included in the early days, meant grinding for very long hours. And yeah. I mean, we've got some people in the company who, going through periods, get burnt out because there's just so much to do, because as I said, we had this hiring philosophy that didn't allow them to offload. And then you get this hero culture internally where they're the only ones that can solve it, but it's very hard to solve because the only people that can solve a hero culture is the heroes themselves. They have to hire those people and train them up and offload a bunch of stuff. So this is like a mini thing where my painful experience was giving away my Lego and all the things that I wanted to do, and they as well have to learn to do that themselves, even though they might just be an engineer and they don't think about having to do that. They don't get people telling them all the time, "This is how you escape a hero culture."So a lot of the hard periods is just hitting these scaling dynamics, and that can lead to all sorts of issues, I mean, whether it's running out of capacity on, as I said, the IP addresses or literally just servers capacity and things like this. And these things are very hard to deal with because they're unsolvable in many ways and we have to scramble to do all sorts of things, but you want to make sure that you're doing your best for your customers, and for a customer-centric company, to not be able to do an amazing job in some areas, that's what I take painfully. Yeah.

Brett:What about you has made the company work? You've been, to date, immensely successful as the founder and CEO of this business. And so what about you or your temperament, skills, abilities do you think is the input driver?

Paul:I think the main thing that matters is I think in processes. So I think a lot of people think in outputs or fixed points and things like that, and I very rarely think this way. It's more ... We have a term which comes from the Toyota production system that we use a lot, which is called Kaizen. Kaizen means to incrementally improve all things from the CEO to the assembly line workers. So in the Toyota production system, they literally mean down to the cleaner will look for perfection in how they clean and doing it as a system. So I love this way of operating and thinking of things always like, well, things go up, things go down, they're just processes. How much they go up and down is what we need to matter. There are control targets on all of these things.So I largely, for a long time, thought in Kaizen and used that a lot internally. So from the product side, just increment the product, make small improvements, ship and shout to the business itself. We've got processes. The RFC process is broken. Let's change it. Just make a small change and never trying to make anything a big-bang change. It's always just incremental.Then from there, you can map your business into processes. So that's where we're at at this stage which are more isolated. You can look at your top of funnel and that's isolated maybe to the marketing team or the DevRel team, and you might look at your churn as a process, and that could be isolated to the product itself. And then largely, towards the tail end of this year, even now, starting to think more in systems, so going up a level again. And the system is from what end-to-end does it matter? It's no good, for example, automating some small part of the business. What actually matters is making sure that a full end-to-end part of the business can be completely automated. So that includes the system of, especially as we've grown now into multiple teams, product team, engineering team, design. How do these three teams operate as a single unit from one end of the spectrum to another, and the handoff between the teams then becomes what is the most important thing. Anyone can iterate really fast in a small ecosystem like a startup does, but as you grow, what matters most is having these improvement cycles within the entire system.

Brett:Talk more about why you think this way of seeing the world has mattered so much for the company.

[翻译失败，原文如下]

Paul:I think because people unblock themselves a lot. If I always scope things down to being small improvement, small improvement, you always see people getting blocked on the big things. They'll try to do something really ambitious, and it's obvious why it happens. I call them like we do RFCs, requests for comments, which are like our PRDs. The design team might put something out, and I might like a hundred things inside what they've done if it's a huge thing, and I might dislike that one thing, and I just comment on that one thing that I dislike. So it's obvious where things get blocked. You want to have small changes which can easily get through the systems of blockers.Avoiding the blockers and giving people a mentality to avoid those blockers so that they continue to ship is important, and then enabling other leaders in the company to remove those blockers if necessary is also a critical part. So defrag, we call it in Supabases. From the product side, but also from the business side, we went through a cycle of looking at all the systems that are a bit broken and like a defrag, the old defrag in computers, tightening those up.

Brett:So I just wanted to wrap up with what is it that you want your customers to say about you and your team members when you're not around?

Paul:Me personally?

Brett:Yeah. What's like the North Star for you?

Paul:For my team, I would hope that they don't say much about me. I would hope that they think we did it. That's more important to me than like, "Oh, Copple was in and he's such a good leader," or something like that. I would far rather them feel like, "Oh, we're smashing it." So that's way, way more important to me than anything that they would say.From the customer point of view, I think the thing that I would want them to think ... I don't need them to say anything about me, but to think that I actually want to solve their problems. That's pretty much it. And just to feel that I'm in the community with them, I'm like them. That's how I feel like. I'm just a builder as well, and I'm in there just to fix some hard problems, and over time, I would hope that I'm building the platform that they want to see the world.

Brett:Cool. Thank you so much for doing this.

Paul:Thank you.

Brett:I really appreciate it. This was great.

Hacker News

---

> 本文由AI自动翻译，原文链接：[How Supabase became the essential infrastructure for the AI era | Paul Copplestone (Co-founder, CEO)](https://review.firstround.com/podcast/how-supabase-became-the-essential-infrastructure-for-the-ai-era-paul-copplestone-co-founder-ceo/)
> 
> 翻译时间：2026-10-29 08:14
