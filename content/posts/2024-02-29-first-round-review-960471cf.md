---
title: The Three Infrastructure Mistakes Your Company Must Not Make
title_original: The Three Infrastructure Mistakes Your Company Must Not Make
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/the-three-infrastructure-mistakes-your-company-must-not-make/
author: ''
summary: '[翻译失败，原文如下]


  WhenAvi Freedmanwas getting ready to graduate Temple University in 1992, there was
  no way to buy internet service in Philadelphia. Litera...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-08T06:48:07.959940'
---

[翻译失败，原文如下]

WhenAvi Freedmanwas getting ready to graduate Temple University in 1992, there was no way to buy internet service in Philadelphia. Literally. If you wanted to send someone money to get a dial-up account, there was nobody to send it to. But Freedman had already been running public access Unix machines and letting people he knew log into them. So he decided to turn his personal frustration into a company that would offer dial-up Internet access to everyone in the area.

He thought, “Well, it can’t be that hard. I’ll just buy a commercial 24-7 internet access link and add some modems.” Not long afterward, Freedman founded Philadelphia’s first ISP. That early experience has served him well. Netaxs and many similar ISPs that built out the commercial internet spawned a community of people that now run some of the largest enterprise, web, and cloud and service provider infrastructures around the world.

Freedman has since wended his way through the networking world. He ran engineering for AboveNet, a global backbone provider (now part of Zayo); spent 10 years atAkamai, running the network group and creating infrastructure-focused services; and then served as CTO for the hosting and cloud company ServerCentral. Two and a half years ago, he foundedKentikto give companies complete visibility into their network traffic, performance and security. Having seen over 100 startups scale their infrastructure, he's one of the best sources of advice we could have found to talk about technical infrastructure.

In this exclusive article, Freedman shares the three biggest (often company-ending) mistakes startups make when it comes to setting up their systems:

- They land themselves in Cloud Jail.
- They get sucked in by “hipster tools.”
- They don’t design for monitorability.

But don’t worry if you spot symptoms of these where you work. It’s possible to avoid these pitfalls if you're aware of them as you build your company.

## WELCOME TO CLOUD JAIL

“It’s a story I see repeat itself over and over: A startup gets a $250,000 credit to set up their infrastructure on the cloud. It’s awesome. It’s beautiful. And it’s only $20,000 a month to start,” says Freedman. “But then they grow, and it becomes $50,000 — then $100,000 month. Suddenly, they’re out of credit. It goes to $150,000, $200,000. That’s when their board swoops in saying, ‘Wait wait wait, what happened? People are supposed to be your biggest cost and you’re pouring it all into the cloud!’ So the startup scrambles, squishing and squeezing until they get down to $80,000 a month — optimizing their database-as-a-service use, buying spot or reserved instances, tuning their instance types, tracking down and deleting unused object and block storage. After a while, they get to a hard packed $80,000+ and still growing — leaving no room for further easy optimization.”

If they want to keep growing as fast as they and their board want, they’ll be back up to and blowing past the high water mark in no time — and there’s nothing they can do easily about it. It becomes hard to afford the infrastructure they need to stay in business — especially in 2016, with an increased focus on margin and unit economics.

As an example, five years ago, a company doing video encoding and streaming came to Freedman with a $300,000/mo. and rising bill in their hand, which was driving negative margin — the faster they grew, the faster they’d lose money. He helped them move 500TB and 10 gigabits/sec of streaming from their public cloud provider to their own infrastructure, and in the process brought their bill to under $100,000/mo., including staff that knew how to handle their physical infrastructure and routers. Today, they spend $250,000/mo. for infrastructure and bandwidth and estimate that their Amazon bill would be well over $1,000,000/mo.

What they said after the ordeal was key: “Man, we wish we’d spent the time upfront to run at least some infrastructure on our own so we weren’t trapped — and had the ability to more easily migrate once we scaled.” In modern terms, they would have preferred to run a “hybrid” of some cloud-based infrastructure and their own servers — or at the very least a multi-cloud system.

“Cloud Jail is waking up to discover you’re spending way too much money on infrastructure and are completely beholden to your cloud provider,” says Freedman. “It’s not easy to switch once this happens. You’re using their specific services and environments. You’re hooked on what they do for you, and it can be incredibly difficult and expensive to migrate.”

For example, Amazon (which he picks on simply because it's the industry leader) has a number of addictive attributes. It makes it easy to do things like user identity. Authentication. Queueing. Email. Notifications. Seamless databases. These are all lightweight services that can save you a lot of time, but only if you’re using AWS. The magic (for Amazon) is that they deter people from migrating despite mounting costs for storage and bandwidth. Amazon customers just can’t imagine living without the perks.

“Wake up! Your board is calling asking why your gross margin is never going above 40%, and why you’re spending more on infrastructure than on developers,” he says. “Things were supposed to scale logarithmically, you explain. The costs were supposed to go down as you grew — but that’s not what’s happening.” Especially in today’s VC market, these sorts of befuddled excuses won’t cut it.

For companies whose revenue is tied to bit delivery over the internet, it can become critical to run in a hybrid or multi-cloud mode to be able to control and ensure outstanding customer experience. Modern network performance management tools can detect and pinpoint congestion that is causing degraded user performance, but cloud providers are often unwilling to investigate or fix remote “in the internet” problems with traffic delivery.

This, even more than cost, has been a driver of tens of companies that Freedman has seen migrate the user-facing parts of their systems. This trend is especially pronounced in the SaaS world, where Customer Success and user experience is a core driver of not just renewal and retention, but also of revenue growth.

So, what should you do instead?

“You want to go into infrastructure with your eyes open, knowing that cloud isn’t always cheaper or more performant,” says Freedman. “Just like you have (or should have) a disaster recovery plan or a security contingency plan — know what you’ll do if and when you get to a scale where you can’t run everything in the cloud for cost or performance reasons. Know how you might run at least some of your own infrastructure, and hire early team members who have some familiarity and experience with the options for doing so.”

By this, he doesn’t mean buying a building and installing chillers and racks. He means leasing colocation space in existing facilities run by someone else, and buying or leasing servers and routers. That’s still going to be more cost effective at scale for the non-bursting and especially “monotonically increasing” workloads that are found in many startup infrastructures.

The earlier you start to think about this the better. If you can get away with it, start out running multi-cloud and post initial traction, set up a small infrastructure, cross-connected to your cloud provider(s).

Freedman practices what he preaches. His 2.5-year old company Kentik, for instance, never did put production workload on the public cloud. Running in Equinix facilities, managing petabytes of storage, and analyzing traffic flows for 100 companies, their bandwidth and colocation bill and equipment depreciation costs are both about $20,000 a month. As a 2.5-year-old data analytics company, their gross margin is over 50% and growing — including operations staff — because they decided to skip the public cloud altogether for production workloads.

[翻译失败，原文如下]

“When you decide to run your own starter infrastructure, you spend under $10,000 for the space, power and bandwidth every month,” he says. “Sure, you may have started with $50,000 then grown to $300-500,000 of one-time equipment purchases. But this is actually still so low relative to cloud compute, storage, and bandwidth that you can afford staff to manage your infrastructure fairly early nowadays.”

It’s also much easier to run the actual servers in dedicated infrastructures. While it was exotic 10 years ago, most operations teams now “treat servers as cattle, not pets,” and can flexibly deploy applications using configuration management systems likeChef,Puppet,Salt, orAnsible, or via containerization and container orchestration systems.

Staff makes a difference.Just three to five people hired early on can run both cloud and dedicated infrastructure, and that same team can often run a system 10x as large as when they started. It facilitates scale in a huge way. “Hire a colonel as soon as you can... an infrastructure colonel who has serious history running hybrid — at least some cloud and some physical infrastructure. That way, as your costs grow, someone smart is watching, and they’ll know when to pull the trigger to make changes in the right direction. On the list of things worth your early investment, this is at the top.”

One last tip about public (virtualization-based) cloud migration: “For always-on and especially storage-heavy workloads, consider ‘bare metal’ cloud and dedicated server providers likeSoftLayer,LeaseWeb,OVH,Packet, and others,” Freedman says. “Especially if you’re cash constrained or don’t need or want to run your own networking for control or performance.”

How can you tell you might be headed for Cloud Jail?

Freedman advises startups to watch the following indicators as a measure of whether they may be approaching the danger zone:

- Tally up the portion of your bill that relates to “always on” and “steady state” or constantly-growing workloads. When these items cross the $100,000/mo. mark, you may hit the tipping point sooner than you expect.
- Watch how many infrastructure services you buy from your cloud provider(s) beyond basic compute, network, and storage. Specifically things like authentication, load balancing, SQL and NoSQL services. Do you have alternate options for them? Will the services you are buying now work well over a direct connection to your own infrastructure if and when the time comes?
- Monitor for network performance issues that your current provider(s) can’t or won’t work around, such as packet loss and poor throughput to certain geographies or internet providers. If you can’t resolve these issues by using CDNs and SD-WAN acceleration services, that’s a red flag. For many SaaS and web companies, performance becomes the key driver to running either multi-cloud or at least some dedicated infrastructures to which they can load-balance for performance.

What if you’re already trapped in Cloud Jail?

The solution comes back to staff. If you haven’t already, be prepared to hire a couple “infrastructure operations” folks who know the playbook — they’ve run infrastructure before. They’ll callEquinix,CyrusOne,Switch, or similar providers, get colocation cabinets or cages, provision bandwidth, and select, order, and install servers. Starting from scratch, this can be a 6 to 12 month process — especially if there are petabytes of data to move or a company with a lot of fast-growing revenue.

But Freedman has also seen it get done in 2 to 3 months, albeit with the aid of a good amount of “exigent engineering.” Or, if your footprint is smaller or need for control lower, perhaps they’ll skip the private network/colocation and just start by adding some dedicated servers or “bare metal cloud” into the mix.

Freedman has personally seen 30 web companies go through this type of transition, and most of them have 3 to 5 core people running the network and physical server administration. The great news is that as long as you have the runway, it’s possible to dig out when public cloud fees start eating you alive.

And if you’re spending a lot, aren’t sure you can get to great gross margins with current cloud usage, but can’t recruit infrastructure nerds on staff, don’t despair. “The networking community is very open and people are usually happy to socialize and help,” says Freedman. “Go toNANOG,RIPE,APRICOT, or your local network nerding meetup or conference. Make connections and ask questions, and you can usually find people who can help you analyze and plan your infrastructure."

The Takeaway

Importantly, Freedman is not saying startups shouldn’t use the cloud initially — especially with the credits available when you’re venture-backed.

When you’ve packed your steady-state workloads, your cloud bill is in the hundreds of thousands per month and growing regularly by tens of thousands, it can already be too late. You need to have switched more over to your own infrastructure before that milestone.

“People lose track because they don’t care when it’s just $1 or 2 million/year less efficient. But it can sneak up on you and become an existential threat to your whole company, driving whether you make money or get more funding, or bite the dust. That’s when people have wished they had thought more about it earlier.”

## FALLING FOR HIPSTER TOOLS

“People are suckers for new tools. They hear that an ‘impressive’ web company has developed a technical infrastructure tool to solve a particular problem, and they just have to try it because it sounds convenient and time-saving and hip,” says Freedman. “We’ve fallen for this at Kentik. We saw something that solved specific distributed systems problems and said, ‘Ooh, that looks good — we’ve always wanted something like that!’ Luckily, it only cost us a lot of of time and internal suffering, but didn’t cause outages that were visible to users.” Other companies haven't been so lucky.

“If you decide to use the ‘new hotness’ that you see blowing up on Hacker News, remember this: It was probably shown off in its best possible light, in a situation that was exactly right for it. So only expect it to work if you give it the exact same kind of input, expect the exact same kind of output, and use it in the exact same kind of application,” says Freedman. “If anything deviates from its one awesome use case — which is obviously the way its makers used it — it’s probably going to break.”

A year or so ago, Kentik started using a system developed for service discovery for monitoring. But it was never actually designed for the scale they started using it at. Their operations team wound up spending 5 to 10 hours a week of a year wasting time when the system — designed to glue infrastructure together — started causing micro-outages. Eventually they migrated away from it. He’s seen a number of companies go through for emergency migrations when tools and components result in even worse outages.

Freedman’s one, overarching piece of advice on the matter: When it comes to infrastructure components, keep it as simple as possible. (And have a healthy amount of skepticism.) “When it comes to your infrastructure, especially the core components that glue everything together — storage, load balancing, service discovery — you really need to be using things that are not, themselves, going to cause problems. You probably have enough problems with the rest of your application and components.”

As an executive, if you see your team tempted by a hipster tool, you need to call for a time out and ask: “Exactly how big is the problem we’re trying to solve?” You can use these questions to gauge how you feel about it:

[翻译失败，原文如下]

- How big of a trade-off are you willing to make?
- How big of a risk are you willing to take? Can you lose money? Time? Customers?
- Are you going to have to contribute to the development of the component or tool? Can you afford a part-time worker or more to develop a component into something workable at a different scale?
- How mature is this component, and is it actively in use for the type of application that you’re running?
- What proof do you have that the tool is stable in a variety of situations?
- How much time and effort might the tool save if it works perfectly?
- Is this a tool or component you’ll eventually have to write ourselves because other current options are so painful?
- Can you find people who have documented failure modes? Especially if not, do you have time to invest to figure those out, and the fragilities and recovery paths, on your own?

Almost always, this gauntlet will dissuade you from using a new tool. There are, however, three conditions (ideally combined) that might justify the use of an experimental component:

- You use understood, tested, and reliable components for every other aspect of your infrastructure.
- You need to solve a problem that will put you out of business because of cost or availability. (I.e. you need the rapid scale or economics the component might give you in order to survive.)
- You have a problem you can’t solve that is core to your customer or user experience — in which case, becoming part of the development community for an emerging tool may be cheaper than building from scratch.

In the last two cases, the more expensive choice is not to experiment with tools. But short of a hail mary pass, it’s often a mistake.

“Every component has bugs,” says Freedman. “Unless you have experience with it, especially if it’s in active development and some of those developers are not in-house to you, you’re working without a safety net.”

One of the best defenses is reminding yourself how high the stakes are.

“I’ve seen a number of companies have 3-day outages because of multiple instabilities in layers of infrastructure that were supposed to glue everything else together,” says Freedman.

Sure, it might be fixable, but when your world is on fire as a result, it’s beyond painful. The common response is to rip the offending component out, and that comes with it’s own consequences. He’s seen startups — especially those using untested storage systems — lose critical infrastructure metadata, and worse:customer data. That’s a breach of trust most can’t bounce back from. And, he advises, be extra cautious about storage components.

“If you’re a founder at an early startup, call a huddle of your leadership. Check religion and fun at the door when it comes to tooling, and make a vow to check and balance each other’s decisions about what components to use.” Ask each other the questions above and don’t compromise.

When your company’s a bit larger, it’s also helpful to create an “architecture review board” — essentially, a group of smart, informed people who will approve the use of new components. This is something Akamai excelled at.

“I was on both sides of the ‘arch board’ — submitting a design for review, and for a time representing network architecture. The board functions like a good lawyer does for a CEO,” says Freedman. “They asked for all the details and gave me their judgment, calling out risks and pointing out options and precedent. It helped everyone avoid some bad decisions. At the very least, this kind of process forces explicit discussions around not only system and component architecture, but also around adopting new outside tools and components.”

![Freedman at Kentik HQ.](/images/posts/1109436ff8d7.jpg)

## DESIGN FOR MONITORABILITY

It’s become a modern mantra to do “test-first development.” And there are a lot of good reasons for that. If you don’t understand something well enough to test it, you probably shouldn’t be writing that code. But Freedman argues a slightly different thesis:

“Instead of thinking first only about your ability to test, you also and critically need to think about your ability to monitor,” he says. “If you don’t know how the component is going to run in combination with the rest of your infrastructure, or how to put in the instrumentation you need, it’s probably dangerous to be putting that component in place.”

Testing usually refers to unit testing, which focuses on components in isolation. But many times when things go south, it’s the unintended consequence of how things interact in dynamic systems — not how things behave on their own.

You have to think through all possible interactions, and what instrumentation (giving you visibility into those interactions) will look like in advance of building. Especially in distributed systems, where often the problem shows up far from the actual root cause that triggered a “ripple” effect, causing the symptoms that you’re seeing.

When things go sideways with complex systems, it’s often because a component gives a delayed answer, or a slightly incorrect answer, setting up cascading issues so that a user-facing performance problem pops up at a different place than its root cause. This is the kind of thing proper instrumentation can pin down fast.

Freedman has seen sophisticated instrumentation work at startups as well as at massive scale. At Akamai, developers were first encouraged, and then forced, to write code in every infrastructure component that they (and infrastructure managers) could then query at any time to see what was going on. This worked well enough that developers rarely needed to log into machines for debugging, which could have caused security, performance and scale issues. The key, though, is being proactive about this instrumentation — especially at the interfaces between components. Going back retroactively takes much longer.

“The rigor that it takes to think about how a component is going to work in a distributed system is really healthy,” says Freedman. “Building in proactive or reactive instrumentation can help leap-frog the unit test limitations of believing that a component works because you tested the input you were expected to give it and got the output you expected to get.”

“Before Kentik, I was running readnews, a Usenet company with a system running in 4 locations around the world with 8 different software components that people were using 24-7,” says Freedman. “Eventually we instrumented the components to report in nauseating detail how they were doing and how the components they were providing to — and got service from — were doing. Before that, it would take days on average to debug a performance problem, and often there were issues we simply didn’t have the data to debug.”

Readnews added two specific types of instrumentation to all of its components:

- Tracing of the user, and a unique transaction ID, for every piece of work done in the system, and embedding those elements in log data.
- Adding the network performance data to every transaction (both internal and internet-facing).

The best case scenario is to have every component streaming their detailed logs to you, and to set up a separate system to correlate them. “At the usenet company, once we embedded user and transaction identity, and exported correlated network performance data, that’s when we started to get alerts that were actionable, because we started to catch things the instant they became inconsistent,” he says. “When we did this, the amount of time it took us to run our infrastructure went from 20 hours a week of diagnostics and debugging to a couple hours a week of restarting a component, noting a bug, fixing it, and moving on. It also allowed us to spend time proactively resolving internet performance problems, and we shared detailed logs and our analytics portal with some of our largest wholesale customers so they could handle support issues without our assistance.”

[翻译失败，原文如下]

As it’s becoming more common to break infrastructure into “microservices,” this kind of instrumentation and distributed tracing becomes critical. Especially for companies that collect all of their revenue over the internet, being able to quickly pinpoint whether issues are caused by systems, applications, or local, cloud, or internet networks is key.

Just exporting these additional logs and metrics isn’t sufficient, however — operators need tools that can process and make sense of them to track performance by user, application, and network component.

“APM (Application Performance Monitoring) tools are not sufficient to quickly pinpoint these problems,” says Freedman. “They often don’t understand the custom components people use, or have visibility into the right internal metrics.”

That said, metrics and log processing systems often see only a piece of the puzzle, and today’s network visibility systems don’t do deep dives into application internals. To get a complete picture often requires a synthesis of modern APM, network, metrics, and log processing systems that can interoperate via open APIs, he says.

One key emerging type of tool Freedman advises looking into implementing is a ‘distributed tracing’ system, often modeled after Google’s “Dapper” system. These systems often provide glue to assist preserving the user data and a transaction ID with every bit of work that gets done, and provide correlation and reporting to allow both tracing transactions details, and seeing aggregate trends.

But, Freedman says, even without formal distributed tracing tools, just emitting the right instrumentation in metrics and logs is a great first step and provides the ‘food’ your systems will need to be able to correlate application, network, and system metrics to actual user experience with performance and stability.

While instrumentation could lead you toward using new or “hipster tools,” this does not present as big of an availability risk as those tools highlighted above that essentially glue your system together. “Yes, distributed tracing frameworks are a bit of a new hotness but it’s a pretty safe thing to experiment with. The main caveat is that you need to make sure you provision your monitoring infrastructure to not melt under the added load.” Another trick that can work well is to do ‘sampled’ tracing, where you only emit (or store) data for one in 1,000 or so transaction IDs, and dynamically enable un-sampled tracing for users you’re actively debugging.

## IN SUMMARY

Infrastructure can be a silent killer.One day you’re running a company to deliver something special and new to customers — completely unrelated to the underlying technology making it possible — and the next, you’re stymied by bills or bugs. Not to mention, plagued by performance problems. How disappointing to get taken down by something so foundational when your company is taking off! Yet it happens all the time.

The three mistakes Freedman highlights here are by no means the only ones he’s seen in his storied career. They just happen to be the most common and costly. Fortunately, the lessons they teach can help you avoid any number of other architecture related problems:

- Think about it early. So early you think it’s way too early.
- At the same time, just because Google does it that way doesn’t mean it’s right for you.
- Establish a system of checks and balances. Enlist experts who can tell you when to say when.
- Predict the future to the best of your ability and iterate on it as you grow.
- Play conservatively. Don’t bow to trends. Take your time. Get all the data you can.
- First do no harm. Protect your user experience at all costs. Make their trust sacred.

With this advice, you can control a major piece of your company’s destiny. And the more control you have, the more you can focus on the real problems you set out to solve.

---

> 本文由AI自动翻译，原文链接：[The Three Infrastructure Mistakes Your Company Must Not Make](https://review.firstround.com/the-three-infrastructure-mistakes-your-company-must-not-make/)
> 
> 翻译时间：2026-09-08 06:48
