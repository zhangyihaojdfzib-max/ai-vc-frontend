---
title: How I Structured Engineering Teams at LinkedIn and AdMob for Success
title_original: How I Structured Engineering Teams at LinkedIn and AdMob for Success
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/how-i-structured-engineering-teams-at-linkedin-and-admob-for-success/
author: ''
summary: '[翻译失败，原文如下]


  Picture a startup in the middle of hyper-growth. It’s adding engineers to keep up,
  but because its team is outgrowing the limited process...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-21T07:48:43.576577'
---

[翻译失败，原文如下]

Picture a startup in the middle of hyper-growth. It’s adding engineers to keep up, but because its team is outgrowing the limited process it has in place, its product release cadence starts to slow. It’s taking longer to check-in and deploy code. Features — then entire products — stop making it all the way to customers.

Now imagine that same company recently hit the 100-million user mark, posted $90 million in revenue the previous quarter and is about to go public in the next quarter at a valuation of $2.5 billion. That’s the situation LinkedIn was staring down in 2011.

“It was a sort of harrowing moment in our history,” saysKevin Scott, who joinedLinkedInas VP of Engineering three months before the company rang the bell at the New York Stock Exchange. AtAdMob, he led software, operations and research engineering until the company was acquired by Google and he was charged with reshaping and further expanding the engineering team.

For the last dozen years, Scott has structured engineering teams at companies in hyper-growth and transition, and he has the war stories to prove it. At First Round’s CTO Summit,he boiled these experiences down to offer four pieces of wisdom for engineering leaders to live by as they approach, enter and get swept up in the chaos of rapid growth:

## Stop confusing building technology with building a company.

Over his career, Scott has worked with hundreds of engineers — many whose titles have changed while their perspective on development has not. “Just think about your engineering career. If you’re a CTO or VP of engineering, it’s very likely you started your career as an engineer,” says Scott. “And when you think about your job as an engineer, you think about writing the best possible code and designing scalable, elegant systems.”

For engineers at heart, it’s easy to make beautiful code the be-all-and-end-all. But for managers of engineering teams, this is a dangerous trap. “It’s tempting to make everything link back to your tech roots, whether that’s building brilliant and engaging products, arguing with product managers about dates, or debating which text editor is best or whether Darth Vader could kill Superman if they got into a fight."

All of these conversations and decisions are very important to creating technology and building technology teams, but they all still miss the greater point.“Your job as an engineer and your purpose as a technology team is to help your company win,” Scott says. “If you lead a team of engineers, it’s better to take a CEO’s perspective. Your job is to figure out what it is that your company, your business, your marketplace, your competitive environment needs. Apply that to your engineering team in order for your company to win.”

## Always ask yourself ‘how’ before ‘what.’

Scott has found that the paradigm shift needed for an engineer to lead a team is often thwarted by that developer’s training. By and large, he’s found that engineers focus a lot on the “what” — which in a hyper-growth company, may change frequently. Examples include:

- What document store are we going to use?
- What sharding strategy is best for our database?
- What programming languages are we going to standardize on?

“All of these are ‘what’ questions — but it’s not entirely surprising,” says Scott. “This is how we're educated. A computer science education is mostly about ‘the what,’ and less about ‘the how.’”

If an engineering manager and her team can start asking ‘how’ questions, they’ll work their way towards thoughtful answers and more durable solutions. Examples include:

- How are we going to collaborate?
- How are we going to resolve conflict?
- How are we going to make sure our code base stays clean as we go from five developers to 50 to 500?

“There are so many ‘how’ questions that we have to resolve. Compared to ‘what’ questions, there is very little about ‘how’ in the way of education and training,” says Scott.

## Iteration works for engineering but not for engineering culture.

Scott’s team developed LinkedIn’s graph database, which is the distributed infrastructure that’s used to model relationships between professionals, companies, and other entities. For example, the graph database helps indicate when two people are connected on LinkedIn.

The first version was written in Java and Oracle. So join-oriented queries, such as requesting someone’s first and second degree network, were sent directly to the database on each request. The second version was written in C++. Everything was stored in memory on a single machine, which was faster than the relational database, but failed as soon as the graph got too big. The team then rewrote the system in Scala and split the graph data up across hundreds of machines. The limiting factor then became the Java Virtual Machine’s (JVM) garbage collector which caused service interruptions when individual graph shards paused to reclaim unused memory. To solve that problem, the team built a log-structured, off-heap memory management system to completely bypass the JVM and its garbage collector. And they didn’t stop there.

“There’s absolutely no way we could have anticipated the direction and resources needed to make the most current version of the graph function from the vantage point of where the team started,” says Scott. “We couldn't even have begun to imagine it. What we did have was this nice, natural sequence of opportunities when we were building this piece of large scale technology to correct mistakes. You can fix fundamental things about the technology at each one of these milestones of growth.”

There are levers and mechanisms to fine-tune technology. But with engineering culture, it is much, much more difficult to discard the first version you build.

“With a piece of technology, you may be able to do red-line testing and look at a traffic forecast and say, ‘Five months from now this piece of sh*t’s going to fall over. I've got to start rebuilding it now so I can continue to run my business.' There is no equivalent analysis that will let you look at a piece of your engineering culture and say, 'When I add the next 50 engineers, this particular part is going to break. If I don't fix it right now I'm going to collapse into ruin.’”

There isn’t a set of natural mechanisms to fix culture problems like there is for technology problems. Yet the consequences can be as dire. “When you have culture problems inside a fast growing company, they can metastasize the same way that bad technology decisions can ruin you and cause things to tip over,” Scott says. “You've got this natural cycle for tech turning over, but you have to get the culture right as well, otherwise you may not have the opportunity or the capability to rebuild these systems.”

Over his career, Scott has observed this high-stakes phenomenon with engineering culture repeatedly —not only on different engineering teams, but across companies. The difference is that mistakes while building technology are inevitable. As he says, “The second that you decide to build something, and if you are in high growth mode, you are guaren-f*cking-teed to have to rebuild it.”

The best companies lean on their engineering culture—versus just their engineering prowess—to help their engineering teams weather hyper-growth. How? They create a cultural manifesto.

## Don’t wait to write your manifesto.

![Elements of a Cultural Manifesto](/images/posts/3b2b1897c7ee.png)

“The single most valuable management tool while you’re scaling your engineering team is something I call a cultural manifesto,” says Scott. “This is a document or a set of materials to help your entire engineering team get on the same page about how you make and operate things, and how you function as a team.”

When Scott joined AdMob in 2007, it had an MVP in the market, customers, revenue and really fast growth. But it didn’t have a manifesto.

[翻译失败，原文如下]

“To keep up with demand, we were writing new features for customers as fast as possible,” recounts Scott. “A significant chunk of our work involved one-off, advertiser-specific features. So, a sales guy would get a lead on $100K, and we would have to say yes or no to building ad units where users could shake their phone and a guy’s trousers would drop in an ad for khakis. Awesome stuff, really inspiring.”

The fast growth catapulted AdMob’s sales, but sent hairline cracks through its engineering infrastructure. “We were executing all this non-leverageable work on features until our engineering team became completely and utterly strained,” he says. “We were in firefighting mode around the clock. We had a hard time keeping up with everything that was being thrown at us. The engineering team was demoralized and on the verge of quitting because they were completely burned out.”

For Scott, a big part of the problem was that there was no cultural manifesto at the company at the time. There were key areas on the operational side where the team just didn't have concrete, documented opinions. “Everyone had different and inconsistent beliefs about growth forecasting and scale planning. Or how we thought about automated fault tolerance versus manual recovery. Or how we did monitoring and alerting. Or… the list went on and on.”

Once AdMob addressed all of these scenarios, Scott remembers that “life got much, much better.” Here is his advice on how to build a manifesto to guide and galvanize an engineering team at a hyper-growth company:

Don’t wait for disaster to strike. Take note of Scott’s early experience at AdMob. “The mistake of ignoring your engineering culture can silently break you. Take a very active step towards proactively drafting a manifesto, because deciding to write one when a crisis hits can be very hard. Make time for conversations around culture — and start early.”

Debate and amend your manifesto frequently. The manifesto serves as a way to refine your engineering culture over time. “Don’t expect to nail your culture perfectly the moment your company comes into existence, but do talk about it from the beginning. Even if you've done it a half dozen times, I guarantee you that each company context is slightly different. Use the framework to discuss how you make, operate and function as a team, not just to codify rules.”

Seek coordination, not consensus. Getting everyone on the same page doesn’t mean getting everyone to agree. “You're not necessarily going to get consensus because you will invariably take stances in your cultural manifesto that irritate the crap out of parts of your engineering team. Remember, it’s not a catalog of opinions, it’s a commitment in print.”

Clearly define the role of engineering. Early on at AdMob, Scott recalls how the company was competing in a market where there were established incumbents and the barrier to entry to serving a mobile ad was really low. “The marketplace itself was evolving super rapidly. You could have a sales guy who hired a PHP programmer who could write enough PHP code to serve one ad and, voila, you had a mobile advertising business,” he says. “On the other side, you had advertising technology titans with network effects and engineering millennia of a head start on us."

The marketplace helped AdMob’s engineering team clearly articulate its culture’s calling card. At the beginning, the company didn't really understand the role of engineering. But after taking a sober look at the marketplace, it became clear: “We needed the engineering team to allow us to take every possible first mover advantage. That was the characteristic that was going to define our culture. We needed agility and that meant a technology platform that would let us move fast and take huge amounts of risk.”

According to Scott, the cultural manifestos at LinkedIn, Google or AdMob were completely different.

“We focused on a different set of factors at each place because the context was unique,” recalls Scott. “At LinkedIn, we weren't looking to take a sequence of first mover advantages. Instead, we asked ourselves how we could leverage a huge set of high quality data to build a suite of products for power users of LinkedIn. That implied a completely different set of technical and operational perspectives.”

Yet even over a short chapter of a company’s story, the reality for an engineering team can drastically change. It’s the leader’s responsibility to be able to sense when the winds shift.Six months after the LinkedIn IPO, Scott launched Operation InVersionto inject the beginnings of a cultural manifesto into his team’s engineering culture. There would be no new feature development until LinkedIn’s computing architecture was revamped -- it’s what the businessandhis team needed. With all eyes on the newly minted public company, Scott took a stand. It paid off, giving LinkedIn impressive engineering agility and boosting its valuation.

Whether at LinkedIn or elsewhere, Scott knows that building technology at a company that is scaling rapidly is really hard. But structuring technical teams in hyper-growth mode is much harder. “Calling all engineering leaders: please start spending a disproportionate amount of your management time thinking about culture as a design process. A manifesto is a pretty damn good way of structuring your points of view and giving yourself a way to evolve,” he says.

If you are leading a team of engineers at your company, start with yourself. Ask ‘how,’ not ‘what’ and let that line of inquiry reorient your team’s collective mindset to helping your startup win.

Startups will have different cultural manifestos, but they should create and debate them early — especially if they plan to build big technology companies. A manifesto is the anchor for a fast-growing company, and, for Scott, part of a greater and much-needed shift.

“As a worldwide Internet industry engineering consortium, we spend way more time collectively thinking about building technology versus designing our engineering teams and our technology cultures,” he says. “That needs to change wholesale."

---

> 本文由AI自动翻译，原文链接：[How I Structured Engineering Teams at LinkedIn and AdMob for Success](https://review.firstround.com/how-i-structured-engineering-teams-at-linkedin-and-admob-for-success/)
> 
> 翻译时间：2026-09-21 07:48
