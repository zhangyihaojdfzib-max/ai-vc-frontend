---
title: How to Size and Assess Teams From an Eng Lead at Stripe, Uber and Digg
title_original: How to Size and Assess Teams From an Eng Lead at Stripe, Uber and
  Digg
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/how-to-size-and-assess-teams-from-an-eng-lead-at-stripe-uber-and-digg/
author: ''
summary: '[翻译失败，原文如下]


  Say your startup has an on-call rotation that follows the sun. Someone’salwayson.
  One day, a member of your team gets an alert that disk ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:39:30.739447'
---

[翻译失败，原文如下]

Say your startup has an on-call rotation that follows the sun. Someone’salwayson. One day, a member of your team gets an alert that disk space will run out on the primary PostgreSQL server in two hours. An hour later, he gets another page. Then thirty minutes later, disk space runs out and your entire site goes down. For 18 hours. The silver lining is that your two-tier architecture can keep your site and app online, but the backend of your business has come to a halt. Your CTO is furious. He says you must fire the engineer who was on call to make a point.

This is a difficult situation, but it’s about to get harder. This wasn’t the lapse of one of your best people, who you could chide, but ultimately defend with their track record. Your report who was on call during the outage is not a strong performer — and generally hadn’t been doing a good job. In one fell swoop, you could discipline for the outage, trigger a possibly fated termination, and act in accordance with your manager. But is thatright? What do you say to your CTO?

The point is less the ultimateoutcome: thatWill Larsontook responsibility and asked the CTO to fire him. Or that he and his report kept their jobs, and that the engineer was talked to and better trained. It’s to show how complex management can become — and why, when done right, it’s a deeply ethical profession. Here’s some of Larson’s calculus behind his split-second response to the CTO: If I fire the engineer, the message to the team is that we unequivocally punish mistakes. Say the engineer may soon be let go anyway. If true, firing him now would be doing the right thing for the wrong reason. For all involved, we’ll lose the message entirely. If that’s the case, the damage to the team will be such that I wouldn’t feel comfortable leading it.

This mode of reasoning is more likely found in philosophy texts than in business cases. While his approach to management is most tested in moments like hiring and firing, it’s been forged over a decade of growing and leading fast growing engineering teams. Some highlights: AtDigg, he hired and led a team of 14 infrastructure and UI/UX engineers who were responsible for the entirety of Digg.com, APIs and mobile applications. AtUber, he led and scaled the SRE and Platform Engineering team from five to over 70, as Uber’s Engineering team grew tenfold to more than 2,000 people. Now atStripe, Larson leads Foundation Engineering, which creates external and internal developer tools, data and infrastructure. His team totals 170 engineers, based in Dublin, San Francisco, Seattle andremotelyacross 18 cities.

In this exclusive interview, Larson digs into two critical components of organization design. Specifically, he shares his system for gauging thesizeandstateof engineering teams — in not only a highly efficient and effective way, but also with a deeply empathetic and ethical approach. Larson builds on excerpts from his book,An Elegant Puzzle: Systems of Engineering Management(released today) to bring ratios and frameworks to structuring team size, combining and spinning up teams, and assessing and accelerating team progress. He offers precise and thorough thinking on team design for the new and seasoned manager alike. Let’s dive in.

## SIZING TEAMS IS AT THE CORE OF ORGANIZATIONAL DESIGN

When managers dig into organizational design, they frequently reach for something abstract, like a mission, to create and orient a team. “Many managers form teams around a cohesive, unified vision. Who hasn’t gone through the mission statement exercise, either for a team or company? First you cover what you’re trying to do, then how you want to do it,” says Larson. “Inevitably someone brings upEnron’s values— and how principles that look like your own can go sideways. Then you get to work, and rarely revisit those statements and principles again.”

The other track that managers often take is to design teams according to the product or technology in front of them. “There’sConway’s Law, which basically states that the product reflects the organization. Well, the phenomenon can go both ways,” says Larson. “The reverse of that is that the organization is built to reflect the product. But if you design too much around your current offering or technology, you set yourself up for repeated change, especially as the product iterates, evolves, spins off or sunsets. This can put a team in a perpetual spin cycle.”

Instead, Larson believes that the fundamental challenge — and cornerstone — of organizational design is sizing teams. “The most powerful unit of work is a gelled team. People who know how to work together and are practiced at working together can accomplish truly remarkable things,” says Larson. “When managers design too literally around the current product or architecture, they churn people and lose what I think is the only truly renewable source of energy in the world: people who really love — and know how — to work together.”

There are many great guides out there onhiringandrecruitingthat speak to thequalityof people on a team, but Larson noticed that thequantityof people on a team is as critical to get right. He fully recognized the importance of sizing teams as he moved from supporting a team to supporting an organization. That’s when a new set of challenges — and questions — emerge:

- How many teams should we have?
- Should we create a new team for this initiative, or ask an existing team to take it on?
- What is the boundary between these two teams?

For Larson, these questions all led back to sizing teams — not only when forming teams, but also in response to reorganizations, hiring freezes or sprints, and launches. While he admits that there’s no unified law of team sizing, Larson has developed a framework, which has solved most of the cases he’s faced — and what happens when teams grow too large or too small.

Here’s Larson's playbook in his own words, via an excerpt from his book:

## Managers should support six to eight engineers.

This gives them enough time for active coaching, coordinating, and furthering their team’s mission by writing strategies, leading change, and so on.

- Tech Lead Managers (TLMs). Managers supporting fewer than four engineers tend to function as TLMs, taking on a share of design and implementation work. For some folks, this role can uniquely leverage their strengths, but it’s a role with limited career opportunities. To progress as a manager, they’ll want more time to focus on developing their management skills. Alternatively, to progress toward staff engineering roles, they’ll find it difficult to spend enough time on the technical details.
- Coaches. Managers supporting more than eight or nine engineers typically act as coaches and safety nets for problems. They are too busy to actively invest in their team or their team’s area of responsibility. It’s reasonable to ask managers to support larger teams during the transition to a more stable configuration, but it is a bad status quo.

## Managers-of-managers should support four to six managers.

This gives them enough time to coach, to align with stakeholders, and to do a reasonable amount of investment in their organization. On the other hand, it will also keep them busy enough that they won’t be tempted to create work for their team.

- Ramping up. Managers supporting fewer than four other managers should be in a period of active learning on either the problem domain or on transitioning from supporting engineers to supporting managers. In the steady state, this can lead to folks feeling underutilized, or being tempted to meddle in daily operations.
- Coaches. Similar to supporting a large team of engineers, supporting a large team of managers leaves you functioning purely as a problem-solving coach.

## On-call rotations want eight engineers.

[翻译失败，原文如下]

For production on-call responsibilities, I’ve found that two-tier 24/7 support requires eight engineers. As teams holding their own pagers have become increasingly mainstream, this has become an important sizing constraint, and I try to ensure that every engineering team’s steady state is eight people.

- Shared rotations. It is sometimes necessary to pool multiple teams together to reach the eight engineers necessary for a 24/7 on-call rotation. This is an effective intermediate step toward teams owning their own on-call rotations, but it is not a good long-term solution. Most folks find being on-call for components that they’re unfamiliar with to be disproportionately stressful.

## Small teams (fewer than four members) are not teams.

I’ve sponsored quite a few teams of one or two people, and each time I’ve regretted it. To repeat: I have regretted it every single time. An important property of teams is that they abstract the complexities of the individuals that compose them. Teams with fewer than four individuals are a sufficiently leaky abstraction that they function indistinguishably from individuals. To reason about a small team’s delivery, you’ll have to know about each on-call shift, vacation, and interruption.

They are also fragile, with one departure easily moving them from innovation back into toiling to maintain technical debt.

## Keep innovation and maintenance together.

A frequent practice is to spin up a new team to innovate while existing teams are bogged down in maintenance. I’ve historically done this myself, but I’ve moved toward innovating within existing teams. This requires very deliberate decision-making and some bravery, but in exchange you’ll get higher morale and a culture of learning, and will avoid creating a two tiered class system of innovators and maintainers.

Fitting together those guiding principles, the playbook that I’ve developed is surprisingly simple and effective:

- Teams should be six to eight during steady state.
- To create a new team, grow an existing team to eight to ten, and then bud into two teams of four or five.
- Never create empty teams.
- Never leave managers supporting more than eight individuals.

Like all guidelines, this is a structure to aid thinking through sizing problems, not a straitjacket to restrict every exception. The context of any situation deserves careful examination, but increasingly I’ve found that the long-term costs of exceptions outweigh what I once considered their strengths.

![Sizing teams and groups of teams using sizing rules](/images/posts/b9a4e3cfbb47.png)

Larson’s basic framework on sizing teams leads not only to organizational health, but also to a more efficient — and ethical — management practice. Here’s what this system can deliver:

Clarity on career tracks.

“The primary goal of leadership in organizations is to allocate access to scarce things. Time and budget are mentioned often, but what's also scarce are management opportunities — and particularly manager-of-managers roles. Take the manager to engineer ratio of 1:8 or the ratio of a manager-of-managers to their reports’ engineers of 1:40. Or that there are only a few tech leads per team or a few staff engineers per organization,” says Larson.

“Almost every career opportunity get scoped when the standard size of teams get set. There will be new types of roles, but groups will grow, bud off, and those team size ratios reset. Given that, managers — and their team — have a clear idea of how andwhenmanagement opportunities open up at an organization. This consistency and transparency serves all involved. Combined withcareer conversations, this system paves a smoother path to setting career expectations.”

Meaningful investment in each report.

“In a fast-growing company, team ratios will fluctuate. Managers may spend more time with new hires than with tenured people. The classic approach, as outlined in Andy Grove’sHigh Output Management, says that managers should spend about half a day a week on each report. That's not literally the time you spendwitheach person, but also includes a manager’s independent time reviewing, developing and reflecting on that person’s area of work,” says Larson. “The bare minimum of in-person time with reports is an hour per week spent with each person on your team, particularly when you're line managing. Then, depending on your structure, you’ll have three or four peers who are really critical, such as a project manager partner. You're going to be spending half an hour with each of these people.”

Now let’s calculate what this means for a manager of eight engineers — and what her calendar looks like alongside her other commitments. “Eight engineers means eight hours of 1:1s. Say you have four peers with whom you’re spending half an hour per week. Now you're up to 10 hours. Then there are weekly team meetings, such as a couple sprint check-ins and a larger team meeting. Now you're up to 12 hours a week. Of course, you’re interviewing, because you're growing quickly. Add three hours of interviewing, and you’re up to 15. Then there’s going to be an All Hands and cross-functional meetings, so let's go up to 20,” says Larson.

“All of a sudden, half of your week is only in meetings. That's a high percentage for someone who also might want to be doing some thinking and doing. If you've been working with a team for a long time, you might be able to condense 1:1s to 30 minutes or switch to an hour 1:1 every other week," he says. "But when the business is growing quickly, there's always context to communicate and act on, so I haven’t found that one can dip below this commitment without creating inefficiency and pressure.That’s why it’s not only productive, but ethical for this manager to keep her team size to eight people.That time’s critical to inform, align, coach and get equipped to accurately and adequately guide and represent their work. Less investment per report or more total reports might be doable in the short-term, but I’ve found it erodes the team over the long-term.”

Moving up and making room.

“We’ve talked mostly about the career path of a manager’s people, but a manager herself must also make time to develop and get promoted. Managers do that by working outside of their team, not just in and on their team. The ethical manager does that only if her team is operating smoothly — another reason for disciplined sizing — but still needs to make time for efforts across the company,” says Larson.

“For busy managers, cross-company work is often still on the list at the end of the week, but it shouldn’t be. Of course, the manager wants to grow like any employee, but theethicalmanager recognizes it’s necessary to her people — and the organization — that she grows into a new position so her role becomes an open opportunity for others on her team or at the organization.”

## ON GAUGING AND ACCELERATING PROGRESS

Standard sizing brings uniformity to the team as a unit of measurement, but what and how that team builds together requires a different system and its own language. In the following framework, Larson offers the four distinct states of teams — and how a manager can identify a team’s current state, guide a team as it transitions between states, and offer distinctly different support for the team’s new state. Here’s Larson’s system, as excerpted from his book:

## Four states of a team

The framework starts with a vocabulary for describing teams and their performance within their surrounding context.

Teams are slotted into a continuum of four states:

A team is falling behind ifeach week their backlog is longer than it was the week before. Typically, people are working extremely hard but not making much progress, morale is low, and your users are vocally dissatisfied.

[翻译失败，原文如下]

A team is treading water ifthey’re able to get their critical work done, but are not able to start paying down technical debt or begin major new projects. Morale is a bit higher, but people are still working hard, and your users may seem happier because they’ve learned that asking for help won’t go anywhere.

![Four stages of a team’s progress, from falling behind to innovating.](/images/posts/92fb59ccbadd.png)

A team is repaying debt whenthey’re able to startpaying down technical debt, and are beginning to benefit from the debt repayment snowball: each piece of debt you repay leads to more time to repay more debt.

A team is innovating whentheir technical debt is sustainably low, morale is high, and the majority of work is satisfying new user needs.

Teams want to climb fromfalling behindtoinnovating, while entropy drags them backward. Each state requires a different tact.

## System fixes and tactical support

In this framework, teams transition to a new state exclusively by adopting the appropriate system solution for their current state. As a manager, your obligation is to identify the correct system solution for a given transition, initiate that solution, and then support the team as best you can to create space for the solutions to work their magic. If you skip to supporting the team tactically before initiating the correct system solution, you’ll exhaust yourself with no promise of salvation.

For each state, here is the strategic solution that I’ve found most effective, along with some ideas about how to support the team while that solution comes to fruition:

- 1. When the team is falling behind, the system fix is to hire more people until the team moves into treading water. Provide tactical support by setting expectations with users, beating the drum around the easy wins you can find, and injecting optimism. As a caveat, the system fix is to hire net new people, increasing the overall capacity of the company. Sometimes people instead attempt to capture more resources from the existing company, and I’m pretty negative on that. People are not fungible, and generally folks end up in useful places, so I’m skeptical of reassigning existing individuals to drive optimality. By nature, it’s also impossible for this kind of discussion to not become political, even when everyone involved has deep trust in and respect for each other.
- 2.When the team is treading water,the system fix is to consolidate the team’s efforts to finish more things, and to reduce concurrent work until they’re able to begin repaying debt (e.g., limit work in progress). Tactically, the focus here is on helping people transition from a personal view of productivity to a team view.
- 3. When the team is repaying debt,the system fix is to add time. Everything is already working, you just need to find space to allow the compounding value of paying down technical debt to grow. Tactically try to find ways to support your users while also repaying debt, to avoid disappearing into technical debt repayment from your users’ perspective. Especially for a team that started out falling behind and is now repaying debt, your stakeholders are probably antsy waiting for the team to start delivering new stuff, and your obligation is to prevent that impatience from causing a backslide!
- 4.Innovatingis a bit different, because you’ve nominally reached the end of the continuum, but there is still a system fix! In this case, it’s to maintain enough slack in your team’s schedule that the team can build quality into their work, operate continuously in innovation, and avoid backtracking. Tactically, ensure that the work your team is doing is valued: the quickest path out of innovation is to be viewed as a team that builds science projects, which inevitably leads to the team being defunded.

I can’t stress enough that these fixes are slow. This is because systems accumulate months or years of static, and you have to drain that all away. Conversely, the same properties that make these fixes slow to fix make them extremely durable once in effect!

![Will Larson, Foundation Engineering Lead at Stripe](/images/posts/63962a61a900.jpg)

The hard part is maintaining faith in your plan — both your faith and the broader organization’s faith. At some point, you may want to launder accountability through a reorg, or maybe skip out to a new job, but if you do that you’re also skipping the part where you get to learn. Stay the path.

## Beyond the four states

Larson’s system of describing teams and their performance may take practice, but he has a few tips that can help managers speed up their success with his framework.

Seek drainage rates, not inflection points.

Larson admits that the evolutionbetweeneach of the four steps may seem more like leaps than steps, but that’s for a reason: managers should give each transition sufficient time. “Yes, these are big jumps between states. But that’s to factor the patience teams must have as they move between them,” says Larson. “That’s especially true for managers, who may make decisions and expect quick results. That's the scary thing about managing teams: the difference between success and failure is often just having confidence about what you're doing, and waiting a little bit. Maybe that's the terrifying thing: the missing ingredient is often just time.”

To illustrate the point, Larson points to an example from his career. “At one point, our data infrastructure team was having a lot of outages, and we were missing our SLAs frequently. We had a great group on it, but they were feeling really overloaded. It kind of felt there was no hope. They kept getting paged in the middle of the night. We were doing all this technical work, so why wasn't it working?” says Larson. “Turns out that we just had to keep doing it for another two months, and then something flipped. Looking back, we didn’t account for thedrainingof the technical debt. Enough remediations of the incidents needed to pass before it got better.”

The temptation is to look for inflection points and assign causation. Again, Larson picks up the story. “As managers, we always want to point to this one thing we did. We rolled out this Hadoop upgrade and everything improved,” says Larson. “But in truth, it was this culmination of doing a few things over a stretch of time that led to it flipping ‘all of a sudden.’”

Inflection points deliver better narratives to teams and are easier to track. But Larson advises managers helping teams navigate between states to track the rate of “drainage” or the lag time between states, rather than tether to any single turning point.

“Take the example of going from the state of ‘repaying debt’ to ‘innovating.’ Something I’d think a lot about here is draining incidents. But you don't know how many incidents that haven't happened that are out there,” says Larson. “But in the case of outages, you can look at the times of the root cause for the incidents that do happen — and if the time to the root cause of incidents is getting shorter. You can start to get a proxy of whether you’re draining these latent incidents. Once you have confidence in staying the course, the energy can be put toward finding proxies to validate and predict when the result of a decision is realized. And when a team enters a new state.”

Work morale and user happiness won’t move in tandem.

[翻译失败，原文如下]

In Larson’s system he notes how both team morale and user happiness fluctuates between states. One assumption might be that team and user satisfaction move in conjunction. “Often when you start doing more technical work, the team gets really motivated because they know it needs to happen, but your users tend to get really upset because you're doing even less to help them,” says Larson. “That’s especially the case with earlier states, such as when your team is in a state of ‘falling behind’ or ‘treading water.’ Say you need to hire 10 people to ship what needs to get to your users. Often in this case, you have to do less work for your users, temporarily, in order to get to a place where you can do a lot more work for them.”

That can be a hard discussion to have — both with your team and users. “If you’ve done a lot for your users to date, it can be difficult to explain why they must wait, especially if they’re relying on you. But if your team is in a state of ‘falling behind’ or ‘treading water’ there’s no forward movement in sight anyway,” says Larson. “This is where you have to just make the hard trade-off to not do something. It’s a choice to keep failing today so that you can succeed tomorrow, versus continuing to fail indefinitely. That’s why a manager must know how to guide a team transition through these states. If she does, both users and her team will trust trade-offs.”

## TYING IT ALL TOGETHER

Managers are right to focus on finding and hiring quality people, but they should pay equal attention to the size of the teams that they manage. For example, engineering managers should support six to eight developers, and leads of managers should support four to six managers. Keeping to this uniformity has ramifications not only for the manager and team — career paths, time management, skill development — but across an organization. Once a standard team size is set, managers must gauge and accelerate the progress of their team. There’s a continuum of team states, from “falling behind” to “treading water” and “repaying debt” to “innovating.” Teams want to climb from the first state to the last state, but entropy drags them backward. Each state requires a different tact by a manager — and the patience and confidence to see it through. Taken together, both the sizing framework and performance assessment system lead to not only a more efficient, but also more ethical management practice.

“Once I found myself directly managing 28 people. There was no way to see all those people with any sort of predictable amount of time, let alone do the rest of my work. Looking back, I thrashed my way through it. I found a few tech leads to take some of the management, and spent an hour a week with them. I spoke to the rest of my people an houra month,” says Larson.

“For some, this may not be obviously the wrong choice. But I saw communication and context with my people start to suffer. I didn’t have the context that allowed me to give good feedback. In these situations, managers give either bad feedback or general, prescriptive advice. If you’re self-aware, you hold back, but then you’re useless. Employing standard team sizes and using a system to develop teams are not just tools, but are like taking the manager’s hippocratic oath. It’s committing to do no harm, to build a team effectivelyandconscientiously.”

Excerpts and diagrams fromAn Elegant Puzzle: Systems of Engineering Managementand courtesy ofWill Larson. Photography byEverett Katigbak.

---

> 本文由AI自动翻译，原文链接：[How to Size and Assess Teams From an Eng Lead at Stripe, Uber and Digg](https://review.firstround.com/how-to-size-and-assess-teams-from-an-eng-lead-at-stripe-uber-and-digg/)
> 
> 翻译时间：2026-10-16 06:39
