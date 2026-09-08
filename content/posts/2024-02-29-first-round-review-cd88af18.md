---
title: Making Engineering Team Communication Clearer, Faster, Better
title_original: Making Engineering Team Communication Clearer, Faster, Better
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/making-engineering-team-communication-clearer-faster-better/
author: ''
summary: '[翻译失败，原文如下]


  15 engineers.


  That’s the size things start to go sideways on a startup engineering team, according
  toDerek Parham, former Deputy CTO for...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-08T07:04:37.992660'
---

[翻译失败，原文如下]

15 engineers.

That’s the size things start to go sideways on a startup engineering team, according toDerek Parham, former Deputy CTO for Hillary Clinton’s presidential campaign. A new engineer will change the code and break something because they don’t know the context that came before; engineers will overlap, working on similar problems without realizing it; and significant time (particularly for the senior engineers untangling the mess) will be wasted.

“Engineering teams fall into unhealthy patterns due to the team growing in size and products growing in scope,” Parham says. “It’s like when you grow out of your clothes as a kid. You don't wake up one day and suddenly your shoes are too small. It’s a slow creeping, inconsequential pain until you realize, ‘Something has to change.’”

Parham is very familiar with the challenges of organizing and managing large engineering teams. Hillary for America rapidly recruited an 80-person tech team, and he was responsible for the engagement, data infrastructure, mobile, ops, and security divisions — on top of a 500+ tech volunteer group calledDevProgress. Before that, he helped start and was the Technical Lead for the G Suite from Google — focused on bringing productivity apps to all companies, schools and organizations. Today, he advises a number of rapidly-growing companies.

With a focus on engineering architecture, team growth, and product development, he’s seen the same pain points emerge over and over again. In this interview, he sharesthe technical design review system(including a critical in-person component) he’s seen be the most successful for keeping engineering teams healthy, communicating clearly, and effective even as they absorb more people and projects.

## Heading into the Wilderness

Most engineering teams rely on design documents to describe, scope, and approve projects or features. Those aren’t new in and of themselves (they're just the foundation of what we'll talk about here). Kicking off a project without one would be like a hiker heading into the forest without a map. Engineering teams don’t have that kind of time. For those who are new to the concept,here’s a good example of one.

Design docs are helpful for a variety of reasons:

- Alignment:As a team gets bigger and starts working on multiple facets of a product, the right hand stops knowing everything the left hand is doing. Code and systems can conflict if people aren’t able to understand everything that’s going on. Design docs serve as a single place that can be discussed, consulted and understood team-wide.
- Critical context:If catalogued historically, they can be the best way for new engineers to get up to speed on why a product or feature was built, why it operates a certain way, what experiments were tried, and why certain decisions were made. They can memorialize the choices of employees who may no longer be at your company.
- Making tradeoffs: “Everything from optimization of a system to new features requires tradeoffs,” Parham explains. “Maybe you need to save time, or people, or launch earlier than you’d otherwise want and have to accept tech debt to pull it off.” If you record your tradeoffs, you put a stake in the ground that makes your team’s priorities clear. Then, when circumstances change, it’s easy to go back and review whether you need to keep making the same tradeoffs.

In short, design documents can cut paths through the wilderness and give you trail markers so you know why twists and turns were made and where they led. If your engineering team doesn’t already have a design doc and review process, you should start one, Parham says. But basic design docs aren’t enough to beat back the chaos. In fact, they can cause their own degree of mayhem if not handled right.

## Design Docs That Work

In practice, creating these documents can become a bit of a hot potato — often, no one wants to take the reigns of authoring one of these things. It can seem onerous, time-intensive, distracting from the code.And at many companies, they’re written up and sent out only to receive resounding silence from the rest of team.

“People will send out a design doc in an email thread and ask everyone for feedback,” Parham says. “Then you get this game theory problem where everyone thinks that someone else is going to read it and give feedback, so no one does. Engineers then take this silence as acceptance or apathy and build the feature or system without any feedback. Months later, issues come up that could have been prevented if people actually read the doc and talked about it.So it’s very important to make sure you have a process that actually gets people to read the document.”

Because of this cycle, many engineering teams assume design docs aren’t worth it. This mentality often becomes a self-fulfilling prophecy and communication breaks down. That’s why you have to not just create a design document, but also commit fully to a design review process. As Parham has discovered time and again:Engineers will only put in the work if they know it’s going to be properly reviewed by the whole team.

To kick off this new process, he suggests that you stop restricting the feedback you’re looking for to the engineering team only. Expand your reach to other teams that have an interest in (or are touched by) what you’re building — security, operations, front end, back end, or product — so as many people as possible will be incentivized to offer feedback when the time comes. Start simply by informing them that they’ll soon be called on to provide an opinion.

"Let your junior engineers write the original design doc and then the senior engineers act as editors,” he says. “It helps with team dynamics by empowering engineers and frees up time for your senior engineers."

At Google, Parhambuilt a templatefor a detailed design doc that can help your team get started. Regardless, your document should not just be a collection of ideas explained in writing, but actually have distinct sections (consider it a checklist), including:

- Background:Background on the problem you're solving. Why does it need to be solved? What other systems, features or products touch it? Who should be involved throughout?
- Design goals:Requirements and goals of the project. This should also include numbers like traffic assumptions, usage, uptime requirements, etc.
- System diagram:Diagram of all the binaries, databases and third-party services that this design touches. Having a visual helps many folks get the high-level picture and understand what's being impacted a lot more easily.
- Design summary:Summary of the solution in a paragraph or two. This should not go on too long; it’s meant to paint a quickly and easily accessible picture of what’s being built.
- Design details:Where the actual specifics of the design are listed out. This can include a variety of things from detailing subcomponents, code locations, testing strategies, internationalization, scaling tactics, etc.
- Tradeoffs made:This is a great place for disclaimers on why certain choices are being made, what any negative implications might look like, limitations being taken into account, any technical debt that might be earned along the way, and changes that may need to be made in the future as a result.

This format acts as an important forcing function for an engineer to have conversations with other members of the team who may be impacted or have input.They have to go through the motions of gathering information and socializing the project rather than just jotting something down in a vacuum. As a byproduct, communication flows better, bad ideas get weeded out sooner, and any negative surprises get nipped in the bud.

“The design doc is really the documentation of a lot of side conversations and trade-offs that happen anyway,” Parham says. “The doc itself shouldn't actually be presenting a lot of new topics to the team. It should be presenting agreed-upon ideas.”

[翻译失败，原文如下]

This first-draft design doc should ideally have approval from all key parties (i.e. the folks who provided the information that went into the doc, and senior engineers on the project) before you send it out to the extended group.

Then, rather than allowing everyone to comment directly on the document,create a blank Google doc where everyone lists their questions about the design alongside their name.This will serve as the agenda for the upcoming design review. For those who are curious,this is what that doc might look like after people have filled it in but before your design review.

“By the time you send out this design doc, almost all of your unknowns should be figured out through the doc writing process,” Parham says. “The in-person design review process itself isn't meant to make decisions. It's meant to create a better team culture, keep everyone informed, and act as a safety net to catch any hidden or last-minute issues.”

## Set Ground Rules

Once you have a solid design document in place, it’s time to prepare for the review itself. But how do you conduct an in-person review with that many people effectively? Parham is very specific in his recommendations.

First, choose a moderator and note taker for your session. They should be neutral parties with no emotional stake in what you're presenting (but an above average aptitude for guiding and following conversations). Then email the group you want feedback from at least 48 hours before the in-person review is scheduled. Send out the design doc along with the blank Google doc for questions and comments. In that email, set ground rules and expectations for the meeting. He suggests sending your team this list of guidelines in order to ensure a productive session:

- “Everyone should add questions to the Questions doc before the meeting. This doc will be the agenda of the review and allows us to optimize for people’s time by diving straight into the issues. Please add your name next to the question when you add it.”
- "Everyone is welcome to sit and listen, butthere's no talking in the meeting unless you’ve read the design doc. The moderator will jump in and cut off questions if the answer is in the doc. We do this so we don't waste people's time. We have X people in the room, so let’s make the most of it." (As a consequence of this rule, you’ll see many people skimming through the doc in the minutes right before the meeting — better late than never.)
- “No email and no typing except for the note taker. Feel free to have your laptops open, but only to read the design doc. We're here to give the next 45 minutes to this product/feature with all of our attention. You'll appreciate people doing the same for you when you present a design doc in the future."
- "The moderator will keep things moving and might ask for specific discussions to be followed up offline. Again, this is to make the most of the group's time."
- "Hold non-on-topic questions until the end, but feel free to jump in with any questions that pertain to the current discussion. The note taker will try to capture everything."

Parham says that 90% of the team will probably ignore the email at first because they’re busy with other work. But if they get a chance to read the doc, they’ll definitely have questions to add (no design doc is perfect).Watching who adds questions is a good way to track team participation and produces a surprising amount of accountability. You can even use this process to see who has the potential to move from junior to senior engineers by how much they help other teams with their insights and questions.

“My tactic is to watch the questions doc over the next 48 hours and make sure it starts getting filled in,” he says. “You'll typically see the pattern where one or two engineers have the vast majority of questions. That's fine because they're probably asking common questions other people have. But you want to have a diverse group of people who are asking questions — diversity of teams, diversity of experience.”

Be cognizant of your messaging around your review session.One surefire way to have no one excited to attend the review is to make it seem like a formal presentation, rather than a discussion.

“One pattern that people fall into with design reviews is they turn it into a scripted or drawn out sort of presentation with slides and a whole thing,” Parham says. “This doesn’t work well. You want to present it as your team is putting a proposal forward based on a number of conversations that have happened, and you're looking for feedback on that proposal.If people think you’ve already made unchangeable decisions, they aren’t going to be as candid in their feedback.”

Choosing a moderator is a great opportunity to involve different members of your overall team in the process. You want someone who is very clear in their communication, great at controlling a room, understands the technical specifics, and won’t let the conversation devolve into argument or rapid back-and-forth. This is exactly why you want an objective party in this role. When you’re too close to the work, it can be hard to stay unemotional and rational. If you’re defending your work too hard and not collaborating, you want to be called out on it. Lead engineers from other parts of your engineering team are great for the moderator role.

“If the front-end team is proposing a new feature that's integrating with a few systems, have the back-end lead or the operations lead be the moderator,” Parham notes. “Again, this is a team building experience where you can groom your senior engineers to take on more responsibilities. You don't want the CTO to be running this all the time. You actually want your CTO to be a participant rather than a moderator or presenter.”

Before the session begins, simple questions without any need for conversation are best answered ahead of time in the questions doc. For instance, questions about launch dates or client needs that were not detailed out — maybe a diagram or link would be the most efficient way to answer a query or concern, in which case, responding online makes sense. But the author should still be prepared to walk through each question live as well.

## Force Focus

The day of the review, you want to stay organized and keep everyone focused for the full 45 minutes allotted. The only way to do that is to create an agenda and stick to it. Here are the steps Parham recommends to ensure you run a successful in-person design review:

1. Send a reminder.

A few hours before the review starts, send another email reminding the team to add their questions to the specified doc. Typically, this is when most people will actually read it and contribute. Then, about 30 minutes before the review starts,the moderator should go through the questions and batch them according to context.

“What are all your operations related questions? What are all your security questions? What are your user experience questions? There's probably a good logical grouping because during the review itself, you're going to want to discuss similar things at the same time to allow conversations to build upon each other or answer related questions at the same time,” Parham says.

In order to make sure the right people participate and actually come to the meeting, you may have to get a little creative. Everyone will have their own methods, but the commonality has to be energy.You should bepumpedfor this occasion. Make it clear it’s important to you, to your team. You’re excited to get feedback so you build the best thing possible. Use whatever tools you have at your disposal to relay this excitement.

“At Google, I would use Nerf weapons to get everyone to go to the design review,” Parham says. “We would just fire at them until they got up and went. I would run around the hallway and say, ‘Design review time! Design review time!’ You can use food, turn off their email accounts, whatever you need to do to get people in there.”

2. Review the rules.

[翻译失败，原文如下]

To kick things off, the moderator should remind the note taker to keep track of key points and insights during the review. With everyone in the room, they should briefly run through the rules to enforce them yet again.

“Emphasize that you shouldn't talk unless you've read the design doc,” Parham said. “This is key because in many design reviews, people who haven’t read the doc will start asking questions that are in there already and have already been answered. It wastes everyone's time. With maybe 20 people in a room, you need to be super efficient. Engineers really appreciate it when their time is respected.”

After you read the rules, a bunch of people will pull up their laptops, open the design doc and start reading it. “People normally go to meetings and just listen, but if you tell them they can't actually provide input unless they do this thing, they'll read it.”

3. Have each person read their question aloud.

During the design review itself, the presenters shouldn’t just go through the questions as you might expect. Instead, the person who wrote the question should ask it themselves.

“Have a human ask the question to the team presenting the design in order to prompt more human answers,” Parham says. “That elicits real, more authentic discussion. If you have someone both read and answer a question one right after the other, they’re more likely to be dismissive, not fully understand the question, and not provide a satisfying answer.”

Push through all the questions this way, with the moderator interrupting if any given contribution goes on too long, and with the note taker documenting any changes or decisions made. Ideally, the note taker writes everything down within the Google Doc that listed all the questions, so you can keep tabs on whose questions got answered and how. This will make the notes easier to parse for everyone after the fact as well — especially those who were not in the room, but who are interested in the project. You can see an example of a filled-in questions dochere.

“If you did a good job on the design doc, there shouldn't actually be that many big broad unanswered questions,” Parham says. “90% of questions will require a very straightforward answer. It could be, ‘Oh, we didn't put that in. Here's the trade-off we made. Here's why. We will add it to the doc, etc.’”

4. Open up the discussion.

Once you’re done reviewing the full list of written questions in the Google Doc, the moderator should open up the discussion to the whole room to ask and answer any other ad hoc questions that come up or provide feedback (if there’s time). Ideally, there shouldn’t be a ton of edits, but there may be.

“At Google, if the design doc clearly had a bunch of issues that people highlighted in the discussion, we'd ask them to come back for a second round with updated changes,” Parham says. “This only applies to large teams, maybe a 100+, where it was really important for everyone to be clear on the details. Then it was okay to go spend a week and get it right, because you might be building a system that has to last for years.”

This is exactly what happened when his team was designing the Google Apps Marketplace a few years ago.

“I remember the design doc went through multiple iterations because it was such a massive project,” he says. “Marketplace was one of our first early remote teams, so there were a bunch of communication breakdowns. The design review process helped with that because we only spent a couple of weeks going back and forth instead of building a system for six months and then launching it only to realize it wouldn’t work, or would break a bunch of other things, or didn’t meet people’s expectations.”

In fact, this type of design review is particularly useful for large teams and those that have a lot of remote workers, he says. Often times, remote workers feel left out of discussions that happen at headquarters, so this process empowers them to learn about everything that's being worked on by the team and have their voices heard.

“It's okay to have that time crunch in the beginning when you’re writing the doc and doing the review, because as soon as you launch the product, everyone knows what was going to be built and understood the trade-offs and why — and could trust that all the necessary discussions had been had and all the engineers with skin in the game were listened to. It avoids so many future issues.”

## Dealing with Dissent

One of the natural parts (but greatest enemies) of a design review is active and sometimes argumentative discussions. Passionate conversation cuts both ways in this context. If the in-person discussion goes on for too long when there are a lot of questions to get through, you have to make sure the moderator steps in. If they don’t, then a senior engineer in the room should play traffic cop.

“If there is a big argument that breaks out in the middle of a review, it’s the moderator’s job to keep control of the conversation,” he says. “The recommendation is for them to acknowledge the key point being surfaced and then say, ‘Look, we need to move on. Please take this offline.’"

Typically, this much dissent in a review means that someone who’s a stakeholder wasn’t consulted early on in the process. You may need to go back to the beginning — redo that part of the design doc by meeting with them one-on-one to go over the trade-offs and integrate their feedback. To quell confrontation, tell the person in question you’ll be putting time on their calendar to go back over that part of the document with their input.

“If the design doc process was optimal, a design review would generate no questions because everyone would simply say, ‘This is perfect. Great job,’" Parham says. “But obviously we're all human and that will never happen. Checks and balances will always be necessary. People will have different feedback depending on the point in the process they were consulted. Ideas are sometimes late to the party. Don’t let it ruffle your feathers. Know it’s all part of the plan.”

When you first institute design reviews, some arguments will inevitably happen. But as you get better at the process, these big issues will become rarer and rarer.

“Even arguments are really a good thing,” Parham says. “I call them design review magic moments.Those are moments when you realize, wow, that would have been a disaster three months from now and we just tackled it here with no coding. All we've done is spent a couple of days writing a doc.”

These conversations also give all members of the team — including junior and non-engineers — the ability to see in detail how technical plans and tradeoffs are made.

## The Benefits for Your Team

“Just imagine how many companies have launched something huge and didn’t gather feedback beforehand so they missed a key issue,” Parham says. “All that time is wasted and you have to go back to the drawing board.Any wasted code at a startup is a big loss of productivity. You have to remember that."

This design review process — starting with the doc and following through to the in-person meeting — has a number of benefits, including:

- Improved org-wide communication
- Better understanding of underlying technical infrastructure (particularly for non-engineering review attendees)
- Knowledge of legacy work and current projects
- Better design of new features and products
- Time and effort saved by engineering (particularly senior members of the team)

The steps in this process also enable all of the engineers on your team to contribute, not just the most assertive ones.

[翻译失败，原文如下]

“Most tech leaders understand you'll have your vocal engineers and you'll have your quieter engineers,” Parham says. “And a lot of times, the quieter ones are your deep thinkers. If you have a discussion without any structure to it or an email thread where people are yelling at each other, sometimes quieter engineers won't get their comments in. This particular design review process makes it frictionless for the quietest or the loudest person to jump in with questions.”

Writing a design document and having a solid design review can save time and immediately improve communication across every function at your company.

“Most engineers just want to be heard and have the ability to give their input. Even if their prior participation in design docs doesn’t reflect that, most wish they were able to contribute,”Parham said. “The trade-offs and decisions might be made at higher levels, but you need to facilitate a culture where everyone gets to provide input into the process, instead of just being told what to do. Design reviews help create a good engineering culture for that reason.”

These benefits aren’t limited to your technical staff. By pulling in members of the marketing, sales, communications, and design teams (and others), you’re promoting a tremendously open cross-functional flow of information that actually scales.

“We didn’t exclude anybody from design reviews on the campaign. Anyone who might have had an insight or good question was included,” Parham says. “You never know where good ideas will come from. I love including designers and product people because it helps them learn and truly understand how and why you’re building things at the core of your company.”

Photo by Thomas Barwick/Stone Collection/Getty Images.

---

> 本文由AI自动翻译，原文链接：[Making Engineering Team Communication Clearer, Faster, Better](https://review.firstround.com/making-engineering-team-communication-clearer-faster-better/)
> 
> 翻译时间：2026-09-08 07:04
