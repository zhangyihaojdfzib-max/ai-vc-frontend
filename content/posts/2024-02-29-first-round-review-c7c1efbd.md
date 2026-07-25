---
title: The Five Mistakes Startups Make When Building for Mobile
title_original: The Five Mistakes Startups Make When Building for Mobile
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/what-you-think-you-know-about-mobile-engineering-is-wrong/
author: ''
summary: '[翻译失败，原文如下]


  This article was published in 2014. As he recently sharedin a new Review article,
  Thawar has since updated his thinking here.


  In 2009,Fa...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-07-25T05:19:28.163382'
---

[翻译失败，原文如下]

This article was published in 2014. As he recently sharedin a new Review article, Thawar has since updated his thinking here.

In 2009,Farhan Thawarjoined mobile development firmXtreme Labsas VP of Engineering. At the time, it handled accounts for some of the biggest brands in the world — a roster including the largest social networks and popular sports organizations. And they all had one thing in common: They all sensed the urgency to break into mobile in a big way.

This trend has borne itself out. Facebook reported last year that78% of its daily users in the U.S. access the site from their phones. For Twitter,the figure is 75%, with mobile representing 65% of its ad revenues.

Unfortunately, there are so many misconceptions around mobile development that many newer startups end up squandering time and money they simply can’t afford, says Thawar. Today he helms engineering forPivotal LabsCanada following Xtreme’s acquisition, and after years observing what works and what doesn’t, he’s honed in on thetop five myths that startups must bust to do mobile right.

MYTH #1:Building apps natively per platform is a waste of time and money.

REALITY:If you want a five-star app, build natively. Period.

The benefits of building a cross-platform app seem clear. You only have to code something once and you can push it out to everyone using any device. Sounds simple. Logical.Facebookthought so initially, as didLinkedInandSouthwest Airlines. But the ease was countered by some pretty dramatic downsides. In later times,Mark Zuckerberg called the company’s over-reliance on HTML5 once of its biggest mistakes.

Initially, Southwest used a cross-platform toolkit to code and distribute its app across devices. Thawar remembers distinctly, at every conference he attended, people would continually use it as the example of the worst app in the App Store.

“It was horrible across every metric: functionality, performance, UI,” he says.

Southwest has since re-developed its app to create a much better experience, as did Facebook and LinkedIn. But cross-platform approaches still lure startups that don’t want to invest more time and money developing separately for every OS. Instead, they rely on HTML5, hybrid applications and cross-platform toolkits, but none of these work well enough to build the high-end mobile experiences users expect, Thawar says. They will eventually, but they don’t right now.

Each of these solutions comes with its own set of drawbacks:

- HTML5:Cross-browser compatibility issues are difficult to resolve, and you end up needing to optimize for each platform anyway.
- Hybrid Apps:There’s a leaky abstraction layer (an example being the URL bar shows up every time you refresh), and the communication layer between the app and web view is complex and littered with errors.
- Cross-Platform Toolkits:They require large amounts of custom code per platform, making it easier and faster to write native code for each.

“In every case when you create a prototype on any of these tools, and you compare them from a speed and polish perspective against doing it natively, native wins every time,” Thawar says. “It’s the fastest way to build apps that look and feel great, and the easiest way to customize them after you launch.”

The takeaway:Instead of going broad and writing something once, spend the time and go deeper on your most popular platform first. Then expand from there. “You want to pick the platform that resonates most with your users — it might be iOS or Android — but you’d be surprised how often it isn’t.” Thawar has worked with a number of clients who realized, only after doing their research, that their key platforms were Blackberry or Windows Phone. It all depends on what you want the app to do and the audience it’s designed to reach.

Figuring out your optimal platform means you need to dig into the demographics of your user base. You need to see firsthand that different users’ habits are largely driven by the platforms they use. Android users look for functionality in different places than iOS users, and so on.

“Spend the time developing deeply on one platform,” Thawar advises. “Then, once you’ve nailed that, you can branch out. From both a speed and quality perspective this is the only way to go.”

MYTH #2:My backend infrastructure is ready to support mobile apps.

REALITY:You will need to change, upgrade, or completely rebuild your backend to create the best mobile experience.

“Most engineering companies aren’t used to building the type of backend infrastructure that creates top mobile apps,” says Thawar. “Without the right API design and implementation, an app will perform poorly in the real world.” Some companies see increases in mobile traffic that are 200% higher — or more — than their website. Take banks as an example: Whereas customers would check their account weekly online, they now check it 50 times a day on their phone. Your infrastructure needs to be able to handle that kind of workload.

Thawar remembers one client that had great infrastructure supporting its website. But once they started hitting the backend from the mobile app, they realized the server was sending back 1.4 MB of data per request. Even over wi-fi and a powerful smartphone, it’s nearly impossible to get a great mobile experience with that magnitude of data being exchanged.

To avoid these issues, Thawar has a checklist of items he recommends companies consider when refactoring their server APIs:

Maximum payload size:In mobile, the best experiences are the ones where the minimum amount of data is sent. A good API for mobile should allow the client to specify the maximum payload size returned from the server (4 KB is usually enough).

Pagination:Data should never be returned en masse. Any sort of list return type should allow cursor-type and paginated results (e.g. I want 25 results, starting at page 4).

Retry:Given the flakiness of network connectivity, the client should be allowed to send the same API call to the server multiple times for certainty. Retrying the same API call should not mean two calls on the same server end (e.g. posting the same Facebook status message twice).

Low latency:Bandwidth isn’t the only networking issue when dealing with mobile devices. The lower the latency on each API call, the snappier your app will feel.

Single API call per screen:This requires tighter coupling between the client and the server, but can make for a very compelling mobile experience. Ideally, every screen on mobile would make at most one API call to the backend. To loosen the coupling, the API could be designed to allow variable return data, with much of the heavy lifting done on the server side.

API version number in parameters:It may be routine to update the server environment, but given that many mobile operating systems do not update applications in the background, it’s possible for some very old clients to be hitting the server. Having an API version number in the parameters can prevent the experience from breaking for those users.

MYTH #3:You can build your mobile app internally as fast as an outside firm.

REALITY:Building your app yourself will take 4x the time.

Thawar is a data guy. Over the many years he’s been helping companies define their mobile presence, he’s recorded and catalogued their various experiences — even for companies that have chosen not to work with his team.

“Lots of folks come to us and ask how long something will take to make. We might come back and say it'll take us a month, or three months for one platform. Then they’d come back to us and say they had decided to build internally. We’d keep tabs on these companies to see when they finally launched in the App Store, and typically we’d see a 4x delay.”

[翻译失败，原文如下]

“Don’t make the mistake of thinking just because you have HTML, CSS and JavaScript capabilities on your team that mobile will be plug-and-play for you. Unless you have a dedicated, built-out mobile team, this will probably not be the case,” Thawar says. And very few startups have this luxury. When they decide to go internal, they’re essentially choosing to pay with time instead of money.

Why does it take startups so much longer to do it on their own? They don’t anticipate their most critical need: Hiring.

Thawar has followed up with a number of companies that decided not to use Pivotal Labs’ services, and this is the challenge that popped up the most. “They didn’t account for the time it takes to ramp up folks with the skills they needed. In terms of salary alone, this route represents significant sunk costs.”

So, if you are planning to build internally, you want to be confident that you already have the people and skill sets you need to execute, Thawar says. This isn’t just about engineering talent either. You need to have people with mobile product experience, mobile QA, and mobile design chops. “You need all of these people working together with tight feedback loops to put out a great product. Otherwise your engineers may head down one road only to discover they had the wrong product vision, or they hadn’t even thought of QA,” he says.

When you bring in a development firm, you essentially inherit experts in all of these areas who can work in parallel to iterate quickly, deploy internally, and iterate some more.

You get designers who know how and why things need to be different from the web, who have experience building for smaller screens and different user interactions. Having a mobile product manager keeps you focused on the three to five (maximum!) core functionalities an app should have. And having mobile engineering expertise is critical.

“Someone once asked me if I would get my auto mechanic to fix my washing machine. Of course not! So then why would I ask my server-side Java engineer to write an Android app? They have to deal with lower power conditions, less memory, a less reliable network stack. You need someone specialized.”

In addition to all this manpower, an external firm gives you the ability to test your app on different form factors, chipsets, and carriers. According to Thawar, it’s not uncommon for top mobile firms to have over 1,000 test devices with 50+ port USB hubs automatically running test cases for every build. You end up with something much better much faster.

Speed isn’t just important for its own sake either. The sooner you get your app into the App Store or on Google Play, the sooner you get to see people’s reactions to it. The faster you can gather that feedback, the closer you are to your next release.

There’s also the chance that you’ll realize halfway through that your company simply doesn’t have the people or resources to finish an app it’s started. Then you have to call in a firm for what Thawar calls “a rescue.” It doesn’t sound good — because it isn’t.

“Imagine building a house on an empty lot. You hire a builder and they can get to work right away. Now imagine bringing someone in to finish a half-built house. That’s much harder. You have to determine what you can salvage, what you can re-use. People get attached to certain pieces of code, or there’s an API they’ve developed on the backend. But, honestly, it’s almost always easier to tear things down and start over. That’s why most times a rescue can take longer than starting from scratch. Suddenly you’re paying more when your goal was to save money.”

This doesn’t mean that working with any outside developer will do, says Thawar — even Pivotal Labs isn’t going to be right for everyone. When choosing a firm, you’re really choosing a partner. You need to look at:

- Culture fit: Does the firm share your values and goals?
- Communication style: Can the firm offer you tight feedback loops to make sure development stays on the right path?
- Track record: Have they developed successful and popular apps before? If so, have they done it in your sector?

All of these attributes are critical — especially, in Thawar’s experience, the ability to communicate rapidly.

“Developing an app with an outside firm is like sitting in an optometrist’s chair,” he says. “Neither of you know your prescription at the start, but then they ask you to read through a lens. They ask you what’s clearer — lens A or lens B? Lens C or lend D? Through rapid feedback, you both get enough data to arrive at the right prescription. When you work with a mobile development firm, you want this type of speed. You can’t wait two weeks between every feedback loop.”

Thawar has heard of companies working with firms that toil on something for months before asking for feedback. “If this is the case, it could take you years to develop a coherent app strategy,” he says.

He givesChipotle’s appas a prime example. The restaurant released the first iteration of its app in 2009, and didn’t release a follow-up until early 2013 — a four year delay. “It happens to the biggest names out there, but users expect to see a really quick turnaround, especially from brands they respect. Especially now with automatic updates, people are used to seeing constant improvements in functionality and performance."

To make sure you end up working with the right partner, Thawar suggests asking every firm a series of probing questions:

- How do they learn as they develop new mobile capabilities?
- How do they capture and leverage the data from their previous projects and experiences? What have they learned from working with other clients?
- Do they offer the ability to co-innovate (pairing their own staff with the client’s to develop, design, and test)?
- Do they follow agile methodologies (test driven development, quick iterations, constant communication)?
- What was their number one mistake?

This last one is especially helpful, Thawar says. “Whenever you’re evaluating a vendor, you should make them tell you about a project that went completely sideways. How did they recover? Ask them if they ever made a mistake they couldn’t recover from. It’s a test of honesty and transparency and will represent the type of feedback loop you can expect from them.”

For all of these questions, the “right” answer is not a one-size-fits-all, but the one that best suits your business. At agile development firms, internal knowledge sharing is accomplished through a combination of human and technical means: lunch and learns, demos, company-wide standups, wikis, an internal Quora-like site, and rotating staff across projects to expose them to a wide range of experiences. You want answers that make it clear that it's easy and encouraged for clients to participate.

MYTH #4:If I outsource to a mobile development firm, I won't have to do any work.

REALITY: For the best outcomes, clients need to be heavily involved with the firms they've contracted.

“Sometimes we have clients who just say, ‘Hey, pretend to be me and make the decisions you think I would make,’” Thawar says. “They just want to hand the whole project over. But what we’ve found is that to do the best work, we need as much information as we can get as fast as we can get it, and that requires client participation.”

In his experience, some of the greatest apps his team has built resulted from Pivotal Labs’ team working very closely with the client’s engineering, design and QA teams. Ideally, they have the opportunity to interview key stakeholders at the client to see what everyone wants and envisions. “We can make some guesses and use tools to help us get closer to what we think the end user might want, but it’s much better not to guess,” he says.

“The best case scenario is actually having our client sit with us every day to work toward building a solution — not just trading emails or checking in every so often over Skype. We call this co-innovation. We want to build together.”

[翻译失败，原文如下]

This doesn’t just make life and work easier for the mobile development firm, either, Thawar says. It’s an enormous mentorship opportunity for a client who wants to branch increasingly into mobile.

“We prioritize this tight feedback loop because we want to learn all about their business, but at the same time they get to learn about what it takes to build something great for mobile. That way, they’ll have more capabilities internally next time. The client has the chance to learn things they can only get from firsthand experience.”

Sometimes clients are so small that they simply don’t have the human resources to spare. In this case, Thawar says, you want to work with a mobile development firm that will help you hire the right people and scale up your own mobile team. Either that, or a firm who can embed people with your company to facilitate quick, in-person communication.

“When you work side by side with someone, trust forms so much faster. It’s so much easier and faster to make decisions and work through issues.”

MYTH #5: Once I start working with a development firm, I'll be stuck with them forever.

REALITY: Working with an external firm at first can make it even easier to build internally in the future.

Ironically, the best mobile development firms are the ones that eventually make themselves obsolete. These are the firms that help clients hire skilled mobile teams of their own. The firms that use pair programming to bring existing engineers up to speed. When this happens, “At some point, clients gain the capability to not need their firm anymore — which is great. When that happens to us, it’s like we’ve enabled someone to do what they weren’t able to do before," Thawar says.

A lot of clients resist outsourcing because they’re afraid they won’t be able to maintain the relationship, mostly because of cost. Justifiably, if you don’t know when that next round of funding will hit the bank, it’s daunting to enter a long-term partnership. But this shouldn’t be as big a concern as it is.

“An external firm’s goal should never be to make a client feel like they have to work with them forever,” he says. “Pair programming between firm and client engineers is one way to empower a client to feel like they can eventually go out on their own. You want to work with a firm that is committed to this approach, because it facilitates a seamless transition if and when the firm has to hand the work back to the internal team.”

Thawar doesn’t just recommend pairing between engineers. If possible designers should work with designers, product managers with product managers, QA with QA. Sometimes in the process, the client will hire people into the company who can immediately be put to work under the mentorship of someone at the external firm. In this way, the two companies are not only building the product together, but also building up capabilities.

“We do all of this so that when we leave, it’s very easy for our former client to know where everything is, how to test everything, and what needs to happen next on the roadmap,” Thawar says. “We can agree that everyone is up to speed, that from here on out they have everything they need to scale up people on their side. Suddenly, we’ll see them putting out whole new releases of their app on their own.”

Ultimately, busting all of these myths depends on finding the right partner. You want someone who gets you, gets your app, and is just as invested in your success as their own. Especially if you’re at a smaller startup, or a company that is only beginning to invest in mobile — especially given the increasing importance of these platforms — finding this exact fit could not only make or break your mobile strategy, but your entire business.

![](/images/posts/c1d54248eede.jpg)

Farhan Thawar is VP of Engineering forPivotal Labs Canada. He held the same post at Xtreme Labs, acquired last year, where he grew the engineering team from 10 to 200.

---

> 本文由AI自动翻译，原文链接：[The Five Mistakes Startups Make When Building for Mobile](https://review.firstround.com/what-you-think-you-know-about-mobile-engineering-is-wrong/)
> 
> 翻译时间：2026-07-25 05:19
