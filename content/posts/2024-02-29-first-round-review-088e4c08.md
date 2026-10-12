---
title: Instagram Co-founder Mike Krieger on engineering team growth
title_original: Instagram Co-founder Mike Krieger on engineering team growth
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/how-instagram-co-founder-mike-krieger-took-its-engineering-org-from-0-to-300-people/
author: ''
summary: '[翻译失败，原文如下]


  By any measure,Instagram’s major milestones are staggering. The entire startup ecosystem
  sat up and took notice when Facebook acquired it...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-12T08:22:20.201871'
---

[翻译失败，原文如下]

By any measure,Instagram’s major milestones are staggering. The entire startup ecosystem sat up and took notice when Facebook acquired it for $1B only a year and a half after its founding. But that was both the result and beginning of mind-boggling, exponential growth in its user base, from 30 million monthly active users when it was acquired in 2012 to 200 million two years later — to over 700 million today.

Internally, co-founder and CTOMike Kriegerhas his own set of milestones that mattered — tied closely to how his technical team scaled and evolved to reach its massive audience. At the time of the acquisition,he had just six generalist developers. Today, he’s at the helm of a 300+ person engineering team rapidly launching new features and products. In just seven years, Krieger himself went from first-time manager to leading a multi-layered organization of specialized engineers, many of whom are the best in their fields.

In this exclusive interview, he shares what he learned from this experience —and what he wishes he could go back and tell himself in 2010. For other startups looking to replicate this scaling success, he covers how to gracefully transition from an early to a more mature technical team, how to introduce new tiers of management, and how to build an engine for unrelenting improvement and innovation.

## Build Your Early Team to Match Your Early Needs

To get a startup off the ground, you need a few things in ample supply — diligence, energy, and problem-solving chief among them. Specialized engineers? Usually not. Generalists excel at this stage Krieger defined a few key traits and abilities that, in his experience, are critical to building the team of generalists that will carry your startup to the next phase:

1. Knowing when to shave the yak.

“Have you heard that expression, ‘shaving the yak’?” Krieger says. “Sometimes programming means solving super complex technical problems. But a lot of times, you end up with a long string of tasks that are necessary to get where you’re going, i.e. ‘I need to get this iPhone app running on my device, which means I need to generate this provisioning profile, which means I need to set up for this account, and on and on.’ In the end, you’re shaving a yak to accomplish that original action — you’re so detached from it.”

When you’re building a generalist engineering team, you need people who are ready and willing to follow those threads all the way to the end. You need people who are eager to learn things they don’t know — things that might be outside their job description — to execute a task.

To find these people, here are a few interview questions you can try out:

- Talk to them about a recent side-project or work project; what “yaks” did they have to shave before getting started on the real stuff?
- Ask them about a time when they’ve taken a project across multiple disciplines, even ones they weren’t familiar with before starting on the project.

2. Knowing when the yak isn’t worth shaving.

That being said, there is nothing more valuable to an early-stage startup than engineering time, and you want to be sure you’re using yours wisely. “People can get addicted to yak shaving,” says Krieger.An effective engineering generalist knows when to move on.

Krieger recalls a moment in the early Instagram days when he’d just gotten what he still views as one of his best pieces of advice:monitor everything.

Initially, this translated into spending four or five hours trying to implementNagios, a leading infrastructure monitoring service. “Finally I was like, ‘I’ve got to get back to building the product. I'm going to settle for a slightly less good alerting solution that's not quite as flexible, which I know I can get done today, and then move on.”

Similarly, you may encounter cases where you could build something yourself. But if a good solution already exists, should you? “Early on, we thought, ‘Well, we could figure out how to do our own push notifications. But Urban Airship is right here.’” Put pride aside and keep your eye on your real goal. “The goal is not to set up Nagios or Munin. The goal is to ship software so that you can get people using it.”

Here's his best litmus test for identifying yak-shaving addicts:

- Krieger and team would have engineers spend a few hours working on building something like a simple mobile app or backend system with full access to the Instagram team if they had questions. “It helped spot the pragmatic engineers from the ones who (no joke) spent two out of the four hours setting up their editor environment,” he says.Pay attention to whether they used their time wisely, not just the results.

3. Action-oriented focus.

You can’t do everything at once, so what are the primary, secondary and tertiary tasks that your startup needs to tackle first? Your system for recording them doesn’t need to be elaborate, but you do need to have one.In the early days of Instagram, Krieger and and his team recorded their action items in a rolling Google Doc, organized by themes.

“One of our themes was being the fastest photo-sharing app in the world. What are we working toward within that theme? Next, we wanted to make the photos look incredible, way beyond what you'd expect from a cell phone. What are we doing on that? Anything that didn't fit into those things went by the wayside. And you want engineers who are okay with that.”

The Google Doc was the perfect minimally viable product for tracking all tasks as a team — and making sure that every single one of them rolled up to one of the organization’s most important goals or priorities. It was broken up into days, and under days into themes. Uncompleted tasks under each theme were migrated to the next day. Highest priority tasks were labeled as such. That way, nothing got lost in the mix, it was easy for people to comment and ask questions, and their eyes were always fixed on what was next for the goals they needed to achieve.

It was vital for Krieger to build a team early on that could roll with this type of system and stay focused on the never-ending firefight of tasks relevant to the company’s success. This meant not hiring or working with people who would go off and do their own thing without paying attention to the company-wide execution plan, or people who would waste time picking off less pressing tasks just to get things done.

Here’s what to ask for people capable of this type of action-oriented focus:

- Tell us about a time when you were particularly proud of the balance you struck between feature completeness, polish, and timing. “The answer to look for is one that’s nuanced rather than absolutist,” says Krieger. “I.e. ‘We only ship when it’s ready’ or ‘We hit every deadline.’ I’ve heard both.”

## Recruiting Passionate and Flexible Generalists

While bigger companies have the benefit of mechanized recruiting teams, startups have their own advantage: they can think and hire outside the box — people who may not match existing open reqs to a T. Krieger recalls his and Co-founderKevin Systrom’s first engineering hire,Shayne Sweeney, as a quintessential example here. “He never finished college. He was a totally self-taught programmer. We met him because we were incubated atDogpatch Labsover on Pier 38, and he had the desk across from us. But he embodied the startup ethos of ‘I have an idea, and I will learn anything to make it happen.’”

Short of observing someone at the desk across from you, though, how can you assess for that kind of drive? In Krieger’s experience,it correlates closely with general and obvious curiosity as a basic personality trait. So for starters, listen for signs of natural inquisitiveness in conversation. “The candidates we got excited about were the ones who would say, ‘This week I was really interested in the game Go, so I built a Go prototype and learned this thing.’ Rather than, ‘Well, the company I work at uses React, so I'm using React.’”

[翻译失败，原文如下]

You can suss out curiosity with a few strategic interview questions, too. “I like to ask, especially at the early stage, ‘What are the side projects you're excited about? When was the last time you went down the rabbit hole on a particular project? What did you learn?’” says Krieger.

Flexibility is crucial at the outset, too — and that might meannothiring some of your most skilled candidates (and being okay with that).

“We interviewed a guy I knew, who was one of the best iOS engineers I’ve ever met. But in our conversations, he basically said, ‘Just so you know, I refuse to do server-side work. I think it's a waste of my time.’ And that's a valid opinion,” says Krieger. Trouble is, that mindset was too specialized for where Instagram was at the time. “We didn’t want people who would hit a wall and then say, ‘Hey, I need server-side work here.’”

Hiring people who can hop between stacks keeps early engineering orgs agile. It also helps you avoid a couple of pitfalls. “I remember talking toKevin Roseabout Digg, and he said one of the biggest mistakes they made early on was recruiting engineers who were too finely matched to the technology that they were using,” says Krieger. “That's a problem for two reasons. One, you're going to eventually want to evolve your technology. And two, if people tie their own job security to, say, staying on PHP, you'll end up making the wrong technology choices.”

His last tip is to prioritize hiring for diversity way sooner than new companies typically do. The benefits of hiring a diverse team are manifold and amply covered in recent tech literature. But in the frenzied early days, startups might think those lessons don’t apply to them — or it still falls to the bottom of the priority list.

“We didn’t put enough of an emphasis on hiring a diverse team in the early stages,” says Krieger. This made it all the harder to bring on women and underrepresented minorities and backgrounds once they’d grown. “If you’re interviewing your first female engineer, and she shows up and thinks, ‘Wow, this team is huge and all guys,’ that just makes the barrier even higher. That really does happen, and if you can avoid that, you’re in much better shape.”

Build a diverse team early though, and you’ll reap the benefits of a virtuous cycle. “Once a couple of women had joined the team, we were excited to bring on many more women much more easily,” says Krieger. “From doing events to interviewing to writing tech blogs and just being visible, it catalyzed a stronger team.” Don’t underestimate the value of being vocal about this. Just saying it’s a priority during recruiting conversations won’t build your pipeline or generate interest from the candidates you really want.It won’t start to sink in for prospective candidates until they’ve heard it or seen it from you at least twice, probably three times — and until your team is reflective of your goals.

## Don’t Fight the Need to Specialize

The next part of Instagram’s story is now part of Silicon Valley lore: In 2012, the then 13-person company was acquired by Facebook. At that point, Krieger and Systrom could recruit both independently and from Facebook’s bootcamp. And with a bonafide brand name on their hands, they were also suddenly faced with candidates who came to them with a different set of expectations.Of course, not every startup will have these conditions, but what happened next in terms of diversifying and specializing their tech team is relevant no matter your circumstances.

With more demands for features and growth, the team felt the need to bring specific and focused skills into the fold — namely, career iOS and Android engineers who could break up pieces of the product and make them better than ever before. This is a common enough moment in the life of a startup. Tell-tale signs that you need to move in this direction include:

- You’re inventing something that goes beyond the abilities typically offered by the platforms you’re working within.
- You start moving into new markets that require highly-tuned code. In Instagram’s case, this was making video work well in emerging markets.
- Your codebase has scaled and needs technical leads to shepherd future growth.

As more specialized experts (i.e. career iOS and Android engineers) came on board at Instagram, the existing team’s can-do, generalist energy bumped up against specialization for the first time.

“We learned that there are canonical ways of doing things. Sometimes it's dogma; sometimes it's there for a good reason,” says Krieger. He recalls one simple, even silly, example: Instagram was his and Systrom’s first big Python project, so they’d settled on some code conventions together early on. “Later, Python engineers would say, ‘Why do you put spaces around your equals signs?’ We just thought it looked better. They were like, ‘Nobody does that.’”

Eventually, you want to navigate your way toward industry standards, because that makes it easier for newcomers to join your team. (Yes, Krieger eventually did go back and make his Python code look like everybody else’s.) You may be tempted to resist specialization on some level, to hang onto your early, scrappy ways. Fight that temptation.You hired specialists for a reason, so let them bring their expertise to bear.

When it comes to slotting existing team members into an increasingly specialized structure, that typically takes care of itself. “Even our generalists preferred one area over the others.” It was simply a matter of explaining to each engineer what the maturing organization needed and seeing where they were automatically magnetized. Some were clearly drawn to iOS, others to infrastructure, etc. Once you observe this, sit them down and very specifically say that you could use their brain on that particular area full time if they’re open to it. Acknowledge how rarefied their skill set is and what benefit they would create for the company.

Specialization also doesn’t mean ditching all of the flexibility that got you off the ground, or putting up hard walls just for the sake of it. “The fact that your early generalists have broad awareness makes them far better engineers,” says Krieger.

Take his first hire, Shayne. “At one point we were trying to make our test cycle faster. Building and deploying was taking a long time. The solution ended up being an infrastructure one, which required a bunch of Python scripting. Instead of dragging in somebody from the infrastructure team, I just said, ‘Shayne, you know end-to-end stuff. You're going to come up with those ideas and you're going to create the MacBuildServer at your desk.’”

## You Need Managers Before You Think You Do

Just as your team of engineers will evolve, your leadership needs to mature, too. At the beginning, your organization will likely be flat. Unnecessary management trappings would just compromise the openness and agility that are a small company’s greatest asset. Still, that doesn’t mean that founders can simply leave their early team to lead itself.

How does 'manager behavior' manifest? Take an easy example: one-on-ones. “We were a solid year and a half, two years in before we started doing them,” says Krieger. Finally Matt Cohler, Instagram’s point partner at Benchmark, gave him the nudge. “I remember opening up those first one-on-ones with people and thinking, ‘Wow, there’s a lot beneath the surface that nobody was talking about.’”

[翻译失败，原文如下]

In retrospect, Krieger sees that pressure was building, and they luckily released it in time. “But it was an eye-opening moment for me. When you're a founder, you're implicitly happy — or that's not even a question you ask, because the company is your baby and you're trying to let it grow,” he says. “People who join are invested in its success, but they're also living, breathing humans with desires and needs and problems. That moment of transition between generalist and specialist is when we started having more management. In retrospect, I would have done it much sooner.”

Implementing management behavior is crucial in its own right, but it also serves as a valuable gauge. When you, a founder or early leader, can’t meet the demands of your own work product and your management tasks, it’s time to get another manager on board. And by the time you think youprobablyneed one, nine times out of ten, you really, really do.

“What I’ve seen again and again, at Instagram and at companies I advise, is once you add a management position — one maybe you weren’t even sure you were ready for — you realize that you were only aware of the top 5% of what needed to get done.The other 95% was just not getting done because there was no point person for it,” says Krieger. “For our managers, it was stepping up our recruiting process, planning events, thinking about the future of the app. My one day a week thinking about that stuff was totally insufficient.”

Here’s how he suggests sourcing managers from inside and outside your company:

1. Promoting from within.

Krieger started with this approach, and Instagram’s initial engineering managers were essentially the longest-tenured members of the team. That offered several natural advantages, principally an easy pitch to the rest of the team. “The upside of choosing the people who are most tenured is that they were often the folks who recruited their now-reports. That already feels like manager behavior, and that already tends to be their dynamic with others on the team.”

Still, he acknowledges that he was lucky that approach worked out, as it’s not always the automatic or best move. “Looking at tenure is always an excellent way to identify your technical leads, but it's not necessarily the right way to identify your managers,” he says. You only want to make them managers if they have interest in growing that way. So be sure to suss that out.

Now, Krieger ensures that all of his managers are having career conversations with their teams, and tasks them with finding engineers who have an interest in, or natural affinity for, management. “I’m of the philosophy that if we have engineers who are interested, more often than not we should let them give it a try and set them up with mentoring.”

Check in with new managers, too, and make it known that there’s an off ramp if they need it.Even people who thought they wanted the role may ultimately find that it’s making them miserable. “Create check-ins along the way, say every six months. ‘Are you still happy? Do you want to take on more? Do you want to go back to being an individual contributor?’ Make sure people are working in the capacity that they're most excited about. If they’re not, they'll be unhappy and leave, or their teams will be unhappy.”

2. Hiring from outside.

Even if you start with internal promotions, you will eventually need to look outside for new managers. In Instagram’s case, that time came when its infrastructure team needed a manager — and none of the existing engineers were interested. “If promoting managers internally was scary, hiring our first external manager was 10 times scarier. That was the first manager we interviewed for,” he says.

It’s rare that anyone currently managing a young team will be out looking for a job, so those candidates are few and far between. “If you're at that stage, you're typically hanging on for dear life and trying to grow your team.” Most often, the person you’re looking for in your recruiting pipeline is someone who has been there before and is now managing a much larger org. “Maybe they’re feeling detached from the work and are excited to get back to being in the thick of things. Really audit why it is they want to join your smaller, scrappier team.”

Screen out anyone who seems turned off by your small team size, and doesn’t see its potential for growth. “If you looked at Instagram in 2012, we had around an 8-person engineering team, and 30 million monthlies. You knew we had to grow. There was no way around hiring someone who could handle that in a hands-on way.”

Krieger recalls a conversation withJim Everingham, whom he hired to be head of engineering in 2015. “He was going from running a thousand-person team at Yahoo and would be joining a 120-person team with us. And he told me, ‘This team is going to be 500 people in a couple of years.’” Krieger himself was surprised by that figure. “But Jim knew,” he says. Those are the strong candidates — the ones you don’t have to sell, because they can already see what’s coming.

In a nutshell, you’re looking for someone with genuine enthusiasm for building something — so much enthusiasm that they’re willing, in many cases, to go from a big, established team to being on call for the first time in years. And in exchange, founders owe those early managers openness and candor.

Everything down to how you structure team meetings is ripe for input in the early days. Don’t try to hide your inexperience from your managers; leverage their know-how instead.

“It was very valuable to build that kind of relationship. To be able to say, ‘Look, we're learning together. I have the context of why Instagram works the way it does. I have intuitions about what we should do. But you have the experience to be able to execute on that intuition.’”

![](/images/posts/55bf43946e3f.jpg)

## Make Your Team Receptive to New Management

Even if you and your early managers have an easy meeting of the minds, you still need to get the rest of your team on board with how fast the environment and their roles are evolving. For starters, don’t be coy. When it’s time to hire a manager, let everyone know that it’s happening. “Always start with a why. ‘I'm overwhelmed. We need somebody to scale the team.’ That sets the groundwork.”

When it comes to hiring itself, there are a few ways you can go. “You can take the consensus-driven path, where you decide that you want all of the engineers on the team to interview candidates. You are deciding to make unanimous agreement that they want to work with someone a hiring criteria.” Remember, though, that those team members aren’t managers themselves, and their assessments will often come down to whether they like a candidate. “It’s hard, and you might not get consensus.”

Krieger favors a related but tempered approach for those early management hires. First, to assess a candidate’s qualifications, lean on experienced leaders; he enlisted other managers at Facebook, though other companies that don’t have this same backing might loop in investors or fellow entrepreneurs. Then, once the offer terms are set — but before anything is signed — bring the candidate into the office for a full day.

“You rarely get jumping-for-joy excitement from the existing team — it's a change, after all. The team used to report straight to you. Now they're reporting to this other person. But you can at least get the red alarm, ‘do not hire this person’ kind of signal,” says Krieger.

You’re unlikely to get that kind of deal-breaker response, but be sensitive to the fact that your engineers might still have concerns — and that their concerns might not be the same. “I’ve worked with the same executive coach for years. One of the things she told me was that if somebody is depleted in one area and you give them an abundance in a different area, it's useless. It's like if somebody's feeling down about their love life, and you say, ‘But your work is going great.’ That’s not what’s bringing them down.”

[翻译失败，原文如下]

(Coaching, incidentally, is one of Krieger’s top recommendations to new leaders. “I went from never having managed a team to managing a team of dozens, and then hundreds. I couldn’t have done it without coaching.” He worked withMaggie Hensleof the Marcus Buckingham Company after being matched through a Facebook management coaching program.)

As you ramp up your first manager or two, in particular, ask yourself: How is this affecting each person on the team.“When we hired our first manager, one of my engineers said, ‘Look, I just came from a company where I had eight managers in two years. Am I going to have another manager two months from now?’ That person needed me to provide surety. So I said, ‘No. I think he’s here for the long run. Here is the plan for continuity. These are the priorities that I'm going to transition over to him. Let’s keep doing our one-on-ones together for a few weeks.”

Moreover, remind your early team that these changes are positive, for the company and for them personally. “Tell them, ‘You're going to learn from this person, too. You’re going to grow,’” says Krieger. “I think all of my early engineers would completely agree that they have.”

## Move from Individual Identities to Team Identities

With the maturation of your org, you’re not just refining your engineers’ roles. You’re also creating a new unit of identity at the team level. “People will feel like they used to work on everything, and now they don’t. Now they have a team.” When that happens, start by refocusing them on impact. “I would tell people, ‘The feature you're working on now? Once it launches, it's going to have more users than all of Instagram did when you started working here,’” says Krieger.

And that’s not just lip service. With growth come even meatier opportunities to shape not only your company’s product but its ethos. Krieger identifies two critical phases in an engineering org’s evolution, each of which has a major impact on a company’s growth:

From generalists to platform teams.The engineers you hire and cultivate at this stage — when you’re on the cusp of scaling — will define your engineering culture for the long haul. “Obviously the early builders got us off the ground. But the fact that we have a successful engineering org today I attribute to setting up the right environment and the right quality standards and the right ethos around engineering at this stage.”

Early on, your yak-shaving generalists might not have the inclination or bandwidth to think about building for scale. As you make the move toward greater specialization, though, it’s critical to create that expectation. “You need to create lanes that people can operate in and not have it be an absolutely chaotic process, where two years from now you’ve created a ton of technical debt.” For Instagram, that meant fostering identity around platforms.

“We created a really strong identity around being an iOS engineer at Instagram, or an Android engineer, or on infrastructure. I wanted people to think, ‘We're only eight Android engineers now, but in a couple of years we'll probably be 30 or 40. What do we need to do today to set us up to solve problems then?’”

By organizing around platforms, Krieger could redouble his teams’ focus on quality. “Take Android, for example. From the very beginning, we wanted to ship an incredibly high-quality, polished Android app, beyond even what the platform would allow us to do at the time.” That focus informed how they worked, and who they hired.

“We talk about doing the simple thing first, striving for simplicity, not over-abstracting. Being proud of the result rather being proud of the abstraction that you created to get there,” says Krieger. Those values, so central to Instagram’s success, were concretized during this phase of the company’s evolution.

From platform teams to product teams.Years later, Instagram has grown past platforms as their core engineering unit. Now they build identity around product teams.

When it comes to that shift, timing is everything. Do it too soon, and you lose the benefits of that culture-building intermediate stage. Do it too late, though, and you may sow the seeds of discord. “We made the switch around 150 engineers, which was too late,” says Krieger. “I think the breaking point — and the clearest sign that this was something that we needed to change — is when your product managers and your engineering managers start hating each other.”

Before the switch, the product manager for any new product had to go to each engineering manager and enlist an engineer from their team. “Great, now you're working with four engineering managers and at least four engineers to get one thing done,” says Krieger. “You've taken really intelligent people and made them human resource allocators.” Meanwhile, no one has a broad view of what the company is working on. “Everybody's trying to make global prioritization decisions, but they only have local visibility.”

By organizing around products, Krieger restored goal-oriented efficiency (and good will). Like that initial move from a generalist to a specialized culture, Krieger has found that it’s largely self-selecting. “All you're doing is making explicit the preferences that were previously implicit,” he says. “For example, we’d say, ‘Who wants to work on modernization?’ Whereas we used to have a ragtag crew of interested people on different platform teams, now they’re working together.”

As you build teams around all of your core products, you will likely also find gaps where no one is super interested — and that’s okay. “Now you have your next action, which is to go recruit people excited to work on, say, growth for iOS.”

At the end of the day, seven years and 300 people later, the mission of Instagram’s engineering org hasn’t changed from the days of that rolling Google Doc of tasks. “You have to remember to ask, again, what's the goal? What problem are you solving? Nobody outside of our walls cares about how we get there, they just care about the quality of the product. As a guiding principle we’ve always structured the engineering team to foster shared responsibility for creating that quality product, and at the end of the day, that’s what you should all be driving toward at any size or stage.”

---

> 本文由AI自动翻译，原文链接：[Instagram Co-founder Mike Krieger on engineering team growth](https://review.firstround.com/how-instagram-co-founder-mike-krieger-took-its-engineering-org-from-0-to-300-people/)
> 
> 翻译时间：2026-10-12 08:22
