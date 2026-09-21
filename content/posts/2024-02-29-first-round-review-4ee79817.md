---
title: Your Data Is Your Lifeblood — Set up the Analytics It Deserves
title_original: Your Data Is Your Lifeblood — Set up the Analytics It Deserves
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/your-data-is-your-lifeblood-set-up-the-analytics-it-deserves/
author: ''
summary: '[翻译失败，原文如下]


  Ben Porterfield''s LinkedIn profile simply identifies him as an “experienced surfer”
  — and that''s an accurate moniker. In addition to regu...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-21T07:48:11.079806'
---

[翻译失败，原文如下]

Ben Porterfield's LinkedIn profile simply identifies him as an “experienced surfer” — and that's an accurate moniker. In addition to regularly riding the waves off the Santa Cruz coast, he's surfed the swells at a number of startups. First as the lead engineer atSticky, Inc., and then co-founder of Rally Up (a mobile startup acquired byAOLin 2010) he's the kind of guy who makes serial entrepreneurism look easy even when it's not.

Today as a Co-founder and VP Engineering atLooker, Porterfield leads a tribe of engineers building business intelligence software that helps companies make better decisions. With customers ranging from early stage startups to today’s juggernauts (Etsy, Sony, Disney, and Yahoo, to name a few), the company has seen how myriad companies choose to set up their analytics, where they go wrong, and why it's critical to start early.

Analytics is something that's easy to put off. When you're actively building a company and trying to figure out your value proposition, collecting and splicing data can seem non-critical or premature. But then, all of a sudden, you hit a point where things get complex, you need to understand your customers much better, and you have lots of unusable data because you captured it the wrong way — or didn’t capture it at all.

In this exclusive interview, Porterfield explains how all founders can nail down an analytics infrastructure from the very beginning — and shares his wisdom on where to store data, the best tools to use, common mistakes to dodge, and what you should measure to start making the right moves today.

## Seriously, Do Not Wait

As soon as your company has users, you need to set up a solid analytics framework. It's not a waste of time or money.

Your impulse might be to save your resources and have your existing engineers cobble together an in-house solution that will do the job, tracking and storing only a sparse set of the most essential metrics. Porterfield has seen a number of companies cave to this temptation and it doesn't end well. It's well worth the time and money to find proven tools that have stability and support from the outset. Here's why:

Everyone on your team benefits from easy access to data.

Making analytics a priority means making it accessible to everyone in your company — not just technical folks. “You want everyone to be able to look at the data and make sense out of it,” says Porterfield. “It should be a value everyone has at your company, especially people interfacing directly with customers. There shouldn’t be any silos where engineers translate the data before handing it over to sales or customer service. That wastes precious time.”The right tools make it easy for anyone in your company to find the information they need and act on it — not just engineering.

When building an analytics framework, a self-service tool for accessing data is key because the people closest to the questions are often the ones running the revenue side of the business. “I’m always going to advocate for self-service tools. Game changing insights don’t always come from the analysts or data science group,” says Porterfield. “They often come from the users who are closest to the problem, understand the product process and know how to formulate the right questions.”

When you embed data directly in the everyday applications where your employees perform most of their work, you’re not just encouraging usage, you’re also creating a data-driven culture, Porterfield says.

From a business operations standpoint, a self-service platform can help IT and data scientists allocate their time in a way that's better for everyone. They can focus more of their attention on the product roadmap or more complex problems.

The right tools eliminate bottlenecks.

“Data teams too often create bottlenecks for the rest of the company. IT shouldn’t be doing the work of librarians, retrieving and interpreting data for those requesting it,” says Porterfield.

Todd Lehr, Senior VP Engineering atDollar Shave Clubshared a relevant story with Porterfield: “We have a developer named Juan and any reports we needed would flow through him. When he got backlogged, we’d call it a ‘Juan Problem’ because our teams didn’t have access to the data immediately."

With a self-service tool, a company will drastically reduce the query queue a developer like Juan needs to manage. Engineers can then prioritize building out the product and bringing things to market faster.

## The 6 Mistakes Smart People Make with Their Analytics

Intelligent people mess up their analytics infrastructure all the time. It's not easy to get it right from day one. It takes time that many companies don't think they have. It gets really complicated really soon. After talking to a huge range of companies dealing with these problems, Porterfield has distilled the top six ways companies often mess up their data.

1. You move too fast.

Maybe you're not even looking at data in the first place. A surprising number of companies don't collect and consult data until they absolutely have to.

“Early stage companies tend to have the same mantra, ‘Build, build, build.’ But because startups are in such a hurry most of the time, they don't truly understand engagement — how the product is being used, what parts of it are working, and why your users are coming back,” says Porterfield. “Engagement tells a really important story about how people are responding to a product. Without looking at the data there’s no way to know.”

2. You don't track enough things.

You can't just give your team a snapshot of your top-line metrics or aggregate sales numbers. If you do, without digging into how things have changed over time (even from day to day), you won't spot the underlying forces that are actually making things happen. There won't be any way for you to see how granular changes to the product or trends in the market affected sales or engagement. There’s also no excuse for tracking too little. Data storage is so cheap, that’s not an issue anymore.

There's no risk to analyzing many things at once. “People seem afraid of tracking a lot of stuff because they think they’ll run out of space, bog the system down or take too long to query — but it’s cheap — so it’s always a win to track more,” says Porterfield. “If you don’t track enough you won’t learn enough.”

Don't be afraid of volume.“Running out of space shouldn’t be a concern at this point,” he says. “A startup usually doesn’t deal with big data, only under certain circumstances if you're analyzing millions of transactions per second or if you turn on the Twitter fire hose. But if that’s the case, then you can probably useHadoop. Still, very few startups have this volume of data to contend with — if you do, then consider yourself lucky.”

3. Most of your team is still flying blind.

“A lot of companies think they can throw data intoMixpanelorKissmetricsor Google Analytics and that's all they need, but they don't really think through who on their team needs access to insights,” says Porterfield. “You really have to make a point of telling everyone at your company that they should be consulting your data and making data-driven decisions all the time. Otherwise, your product team will just build, hoping for the best, and never truly understand why things succeed or fail.”

Let's say you're running a company that needs to acquire more users. You decide to apply proven viral app techniques and tap into existing users' contacts to pull them in too. Suddenly you see new users flood in, which is great, but if you're not measuring the right things, you might completely ignore how this feature impacts existing users. In this case, people sign up, get spammed repeatedly to connect their other networks to your product, and end up dropping out. Your product team might declare the feature a success even though it's spiking churn.

[翻译失败，原文如下]

You may also be gaining a bunch of users who aren't worth the users you lost in the process. These are elementary mistakes that occur all the time. But they can easily be fixed by making your analytics infrastructure easy and intuitive for everyone to access and leverage to answer the questions that are most important totheirjobs.

4. You're storing things in the wrong place.

First, let's look at who's doing this the right way. Porterfield cites one Looker client who uses a tailored analytics architecture built from a unique combination ofNoSQL,Redshift,Kinesis, and Looker. This framework not only captures and stores its own data at scale, but can handle clickstream data for millions of monthly visitors, and allows anyone to make queries. This tactic also allows even non-SQL speakers (business users and analysts) to dive into the meaning of data.

“Essentially, if you can’t access the data with SQL, the lingua franca for analytics, you’re screwed,” says Porterfield. “If it’s going to require engineering work to get the data out (for Hadoop, it may require writing jobs) then you’re putting yourself behind the eight-ball.”

In this case, engineers have to do a lot more work to get their business users the information they need. And, even if you can access the raw data, engineers will likely have to build or buy a tool to help business users understand it. This makes running experiments to optimize marketing or sales a complicated ordeal, and end users simply won’t be using data at the same level.

Let’s say the same hypothetical company that didn’t notice the impact of its viral techniques also didn’t have all their data in the same schema, so they couldn’t easily create queries to understand how their events were related to one another. They couldn’t see these numbers side by side so they weren’t in a position to query across both operational and events data.

“Many companies send data off to a service to store it, but once it’s stored, it’s no longer accessible in the same form; it would require engineering to get it back,” Porterfield says. “Too much of this is event data — metrics showing what happened with your site or product. This is super valuable stuff. When you combine event data with your operational transactions in a database, you learn which events triggered conversions. The value of combining your operational data with your event data is that you get to understand your user's journey through your product or service — there are few things more important.”

Operational data could include number of shipments going out, returns coming in, any action your company is taking. Event data is all about how customers and users are behaving on your site. The two are closely linked, and the healthiest companies know exactly how they are impacting each other at all times.

Even so, about half of the companies Porterfield has seen keep their operational data and event data separate. These customers are still able to can draw conclusions, but they aren’t able to get the fullest picture of why their users make certain decisions. If a company wants to know which events lead up to a conversion, then they need to combine this data in the same central location.

There are hazards with only looking at one or the other. “If you’re not looking at operational data, then you don’t have control over your business and that's a big problem,” says Porterfield. “If you’re not looking at event data, then you don’t understand your product usage, and you can't make good decisions about what to build next. They go hand in hand.”

5. You're not looking far enough ahead.

Any good analytics system is designed and built for longevity. “Yes, you can always change your analytics framework, but remember that data is heavy. The more you have, the harder it is to move around from system to system. If you decide to change things up, it's going to be a real pain in the ass that gets worse the older your company gets.”

Moving data costs lots of people lots of time. And often, while making a transition, you have to track your data in two different places — the old repository and the new. That's the only way to ensure that you're not losing anything in transit.

This is incentive for getting things right from the start. The best move is to throw everything into an analytical database that you can scale as you grow. “Don't waste precious time choosing between a ton of different database solutions. Just choose one that allows you to expand capacity instead of moving everything somewhere new,” Porterfield says. “All you need at the beginning is a way to track events and put that data next to your transactional database so you can query across them both. That should last most companies one to two years at least.”

When this is no longer a viable solution, just add capacity. You don't have to haul anything anywhere. And you capture what's most important: How different actions and product changes impacted interactions and transactions. That's what companies can learn from the most to devise better product roadmaps and marketing strategies.

6. You over-summarize.

While this problem is more common at companies with big data science teams, it's a cautionary tale for early stage startups too. When you try to make your data simpler or reduce size by rolling it up, you risk losing a lot of important information.

Think about it: How many companies track average sales per minute rather than the number of sales that happened every specific minute? “This is an old school analytics practice,” says Porterfield. “In the past, companies had to cube or roll up data because their systems were too slow to process it any other way. That's not an issue anymore. Now it's actually possible to freeze frame what's going on with your business in every passing minute. And looking into these snapshots can tell you an awful lot about why conversions dipped or spiked, etc.”

When you pre-aggregate, you lose the ability to drill down and see outliers that tell you if something is broken, or if something works amazingly well. You lose your most educational indicators.

It’s common for teams to look at high-level metrics — like number of sales displayed on a dashboard. This can be casually informative, motivating, and helpful. But you shouldn't make any major decisions off of that type of intelligence, Porterfield says. He's always been skeptical of dashboards.

“You shouldn't waste your time looking at numbers just to feel good about yourself. You should be looking at numbers to learn how to do something differently. A good dashboard changes behavior by showing you the outliers.”

Resist the urge to over-summarize. It buries gems that have the potential to transform your company.

## The 3 Easiest Ways to Avoid These Mistakes

First of all, dodging these errors will save you much more than you think, Porterfield says.

Not only will they cost you control over how your business and operating day to day, it's easy to sink massive engineering time and resources into patching up a flawed system. If you don't watch out, your engineers could be spending expensive hours deciphering data for your sales team. Your marketers could be missing out on all kinds of opportunities to maximize engagement. Don't risk it.

The good news is, if you keep analytics top of mind when you first start acquiring users or customers, you can put three simple safeguards in place to sidestep these pitfalls:

1. Appoint a business intelligence engineer.

If you choose one person who has an interest in analytics and charge them with figuring out the most effective way to log data, you'll save everyone a ton of time. Analytics support won't be spread out across your entire engineering team, and this one person will have more incentive to figure out the lowest-lift way to capture the insights you need.

[翻译失败，原文如下]

“At Looker, this person wrote a script to log all events in our product,” says Porterfield. “That made it easy to put all of these logs in a single database where we know we can get that data back out when we need it. It saved everyone a huge amount of time and ended up being the easiest solution."

2. Own your data.

It's highly recommended to use open-source analytics platforms that let you track all the events related to your product in real time, like Snowplow. It's relatively easy to use, it's well-supported, it scales, and — best of all — it's free. It's also compatible with the rest of the framework you're probably using.

3. Get your data into Redshift or another massively parallel processing databaseASAP.

For early-stage companies, cloud-hosted MPPs like Redshift are often the best solution, because they're low-cost, easy to deploy and manage, and they scale well. Ideally, you want your event and operational data in Amazon Redshift from the very beginning of your company's recorded history. “The advantage to using Redshift is that the platform is cheap, fast and easily accessible,” says Porterfield. Additionally, for those in AWS, it hooks up seamlessly to your existing infrastructure, so it's easy to build a pipeline of data straight into the system where it will be easy to analyze.

“Redshift gives you the flexibility to store a tremendous amount of very granular data without charging you based on arbitrary things like event volume,” he says. “Other solutions will charge you by the number of events you're storing, so eventually the cost skyrockets when you have more and more people using and taking actions with your product.”

![Porterfield on the roof of Looker's Santa Cruz headquarters.](/images/posts/4cc0a614d3fa.jpg)

## How to Use Metrics to Win Your Market

Analytics are only as good as what they help your company do.At a startup, all data should be leveraged to achieve what you've defined as success for every stage of your company. “Success metrics are anything that you want to have happening — and that's usually engagement,” Porterfield says.

For example, a delivery company probably wants to track the average time it takes to deliver something. This is useful, but only in the proper context (after all, a recipient may be a block away or hundreds of miles away). Delivery time isn't nearly as important as the happiness of the person who received the package. Make sure that your success metrics capture the right thing.

Identify your key desired outcomes:What do you want your customers to experience? Some common success metrics based on desired outcome are conversion rate (how likely someone is to buy if they do X), time to transaction (how long until a user buys), and churn (users who will likely never buy again). You want conversion rate to be high while you want the other two to be low and dropping.

Focus only on engagement that matters:Different companies value different levels of engagement. What's important to you? You probably want someone to come back to our app repeatedly, or you want repeat customers. Look at the numbers that will surface these relationships

“Upworthy, for example, redefined the type of engagement they were interested in,” Porterfield says. “Usually media sites base their success on sheer page views, but they started looking at what they called 'attention minutes' — how much time people were seemingly engaged with a page, whether they were highlighting words, scrolling, clicking their mouse, watching a video, etc. They didn't just want to see how long someone stayed on a page, they wanted to track how long people were obviously interested by what they saw on each page.”

This has helped the site pioneer new types of headlines, layouts and content choices — all geared toward holding people's attention for longer amounts of time. In doing so, they've revolutionized how media sites in general measure and speak to their audiences.

Measure retention and behavior of repeat visitors:Success metrics can also be bucketed into operational and event metrics. Make sure you're looking at both to really understand what forces are at play.

“If you're only looking at operational metrics, you'll know if someone came back to your site and if they bought something,” Porterfield explains. “That's all well and good, but you always want to know how many people came back and browsed but didn't buy anything. Why did they do that? This is a huge argument for merging your data. You can't find these answers without combining operational and event data.”

Event data will show you how non-buying visitors navigated their way through your site or application, what grabbed their attention, where they clicked, and what happened right before they left. When you track this route, you can modify behavior. For example, you can show them something different next time that will increase their chances of buying.

Invent new metrics: In order to track what is most valuable and impactful for your business, you have to create unique metrics specific to you. Three things go into this:

- Identifying a type of user behavior.
- Measuring the percentage of your audience exhibiting that behavior.
- Experimenting with the numbers to see if this is actually crucial information to capture.

Sometimes, inventing a new metric can make a big difference for your company. Just askVenmo.

A while ago, the payment app's support team started hearing from users that many of them were accidentally paying their friends instead of requesting payment from them. The buttons were right next to each other. It was easy to slip. While the company knew this was happening, they weren't sure how widespread the problem was or if it was worth prioritizing a fix. To find out more, they tapped into their analytics.

The Venmo team was able to invent a new metric around the pay/charge mistake to see how often the issue occurred. To do this, they hypothesized that there was confusion around the buttons, and they highlighted instances where a user would pay someone a certain amount and then eventually charge that person twice that amount. The behavior isolated this particular confusion, and the team was able to see that it was indeed a big problem. In their next software update, they got rid of the side-by-side buttons, defaulting to payment. The same new metric showed that the problem quickly resolved.

## Make Your Metrics Sharable

Analytics will only be useful if you can share them throughout your company. “When you're sharing metrics, the number one troublemaker is misnaming your terms,” says Porterfield. “You have to have incredible clarity around what every single thing means.” To achieve this, he recommends creating an analytics glossary on your wiki or somewhere else central so that people know the terms you're using and how to interpret the data you share.

“I've seen data given absurd names where the words don't even accurately describe what the thing is,” he says. “People like to use the word 'ratio' a lot instead of more accurately saying they are looking at one value over another value. This is the kind of thing that can lead to serious, pervasive confusion.”

Data is the lifeblood of successful companies. Sharing it not only creates a healthy sense of transparency, it also creates alignment between business units that should be working together. What you don't want is everyone struggling to find data through multiple sources.

It's not uncommon for two marketers at the same company — both concerned with clickthrough rates — to track down this data through different means. Maybe one found it through a BI tool while the other asked an engineer for help. In the end, they'll probably surface two different answers to the same question.

[翻译失败，原文如下]

You can't stop at making data universally available either — you have to make insights drawn from this data easy to share as well, Porterfield says. “An insight is a contextualized data point that makes you change something or take an action. It's the insight that is important to most people at your company, not the raw numbers.”

The right analytics infrastructure is one that makes it just as easy to share insightful data visualizations (graphs, charts) as it is to dig down into the most granular details. Visualizations are a way to make data meaningful for your entire team.

“Most people can see things much more clearly in the form of a graph than in a table. Databases present data. Visualizations are what help you understand it,” Porterfield says. “Whatever analytics system you choose, know that visualization capabilities will make sharing that much easier, more frequent and fluid.”

This is toxic and it happens all too often.You know you've chosen the right system if your least tech-savvy business user can intuitively create a cohort chart and immediately understand it.That's the baseline of ease you should be looking for when choosing analytics tools or software.

Most importantly, the right system is so user-friendly and sharable that it makes your entire company more customer and product-centric. More than anything, you want your data to drive everyone to ask the same question: “What's next?”

“Analytics are what will make people come more prepared to meetings. It's what makes teams ask better questions about how they can do what users need and want most,” says Porterfield. “It takes the guessing out of the equation. People no longer have to guess at what their users are looking for or what's making them buy or click or leave prematurely. They don't have to guess at what their co-workers know or don't know. That's the payoff of doing analytics right the first time — it's significant.”

Photography byMichael George.

---

> 本文由AI自动翻译，原文链接：[Your Data Is Your Lifeblood — Set up the Analytics It Deserves](https://review.firstround.com/your-data-is-your-lifeblood-set-up-the-analytics-it-deserves/)
> 
> 翻译时间：2026-09-21 07:48
