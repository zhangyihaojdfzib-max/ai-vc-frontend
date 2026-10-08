---
title: 'Start With a Prompt: Inside Warp’s AI Coding Mandate'
title_original: 'Start With a Prompt: Inside Warp’s AI Coding Mandate'
date: '2026-10-07'
source: First Round Review
source_url: https://review.firstround.com/warp-ai/
author: ''
summary: '[翻译失败，原文如下]


  WhenWarp’sZach Lloydnoticed senior engineers were reluctant to adopt AI tools, he
  rolled out a slightly more pointed new policy: Every co...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-08T08:37:52.986365'
---

[翻译失败，原文如下]

WhenWarp’sZach Lloydnoticed senior engineers were reluctant to adopt AI tools, he rolled out a slightly more pointed new policy: Every coding task needs to start with a prompt.AI mandates from CEOs are nothing new. But Warp’s founder goes further than most by actually following it himself.

“The most enthusiastic initial adopters of AI at Warp were designers, PMs and me,” Lloyd says. “I was a principal engineer at Google, and I still write code at Warp, getting about one coding change in a week, and I’m using this new generation of tools constantly.I personally only code by prompt now, but it’s a recent development.”

Lloyd says it’s only within the last couple months where the product itself has gotten good enough to build Warp within Warp. “We are now building much of Warp starting with a prompt these days, which is a bit wild since it’s over a million lines of Rust with a custom UI framework,” he says.

Warp’s business has transformed alongside Lloyd’s personal coding practices, evolving from reimagining the terminal to building what they call an “agentic development environment” (ADE). That places the devtool company squarely in the middle of the seismic shift that’s currently upending engineering workflows. “We went from building an experience for users to tell their computer what to do with commands in machine language, to letting them tell their machine what to do in natural language,” he says.

The impact has been explosive. “It wasn’t until we started really embracing agentic development that our revenue took off,” Lloyd says. “The first $1M in ARR took 300+ days, but we’re now adding $1M every 5-6 days, with revenue up 19x this year.” Warp users launch almost 3M agents per day, generating 250M lines of code weekly with a 97% acceptance rate of agent-suggested diffs.

But this isn’t a product or a revenue story. It’s a story about how Warp’s developers transformed their own internal practices — and about how Lloyd visibly drove that change from the CEO’s seat.

To further proselytize adoption, he builds in public for all to see — at All Hands, in customer calls, in prompt-based developmenttutorials, even on weekly YouTube livestreams. And as it turns out, in media interviews, too.

When we interviewed him recently on how they were using AI internally, Lloyd took the liberty of sending over a video he made just for Applied Intelligence readers, showing — not telling — how the “How Warp Uses Warp to Build Warp” guidelines steer product development at the company.

Following his own coding mandate step-by-step, he built a fix for Warp’s tab renaming interface, speaking his prompts rather than typing them.

![](/images/posts/ace932aa8766.png)

The coding mandate he and Warp’s developers follow is both simple and surprisingly nuanced. Below, Lloyd shares a detailed look at how the eng team now works differently, along with his biggest takeaways after more than three months of personally adhering to it.

## The (senior developer) resistance problem:

The mandate’s origin story stems from Lloyd’s observation that senior developers were the ones resisting AI most strongly. When Lloydpostedabout this problem a few months ago, hundreds weighed in in the comments, with many confirming they were facing the same struggles in their own organizations.

It makes sense that non-engineers gravitate towards these tools most, because they make the impossible possible, he says. “One of our designers recently helped build the new version of the terminal multimodal input, and he didn’t handwrite a single line of code. The idea that our designers would be building features and fixing bugs on their own would have been very hard to imagine a few years ago.”

Whereas for senior devs, AI is at best a speedup. “On the surface, these engineers ‘need’ AI the least because they know what they are doing,” he says. They also have wildly different dispositions toward AI. “Developers are a very diverse group of people when it comes to how they like to work. I find these tools very fun to use personally, but some folks — if you look at this summer’sStack Overflow survey— are pretty against AI on principle,” he says.

But the resistance can run deeper than just lingering skepticism. “When you first try to do things by prompt, there's a high likelihood it will fail, or actually take you more time,” Lloyd says. “It’s not like if you try it just once you’re going to be instantly converted. That’s why many senior devs tend to think the code these tools produce is not very good, and that they can do it faster themselves.”

But in Lloyd’s view, that attitude won’t carry very far. “No one developing software going forward should be doing it all by hand. In fact, the more code a developer is writing by hand, the less productive they will be relative to peers who are embracing agentic development,” he says.

Lloyd thinks that senior engineers should in fact be AI’s power users. “If you as a senior engineer already know how to architect these things, you’ll know how to guide AI more effectively. You understand what good code looks like.”

“I’m thinking of someone likeJeffon our revenue team. He built our entire admin panel via prompt, without handwriting any React code,” says Lloyd. “This was an important enterprise feature that allows our enterprise customers to control security features, and unlike the main Warp app — which runs on the desktop — it’s a web app we had to build from scratch.”

## The coding mandate:

Motivated to move the needle on internal adoption, Lloyd circulated the following guidelines, which are published in fullhere(along with several other Notion guides on how the Warp team operates internally). “If you’re a founder or eng leader trying to get your team to use agentic tools, you need to set very clear expectations, probably much more explicitly than you think. I had to push pretty hard. It’s the difference between success and failure,” he says.

“We go over this mandate every week at our team meeting because we really want to get people in the habit of working in this new way, and emphasize over and over that it’s not going to work well initially, that there’s a whole bunch of skill in how you use it. The guidelines in our mandate will change over time as the models improve, but they represent our best practices today.”

Here’s the quick snapshot:

### Step 1: Every coding task should start with a prompt in Warp

“You better give people a reason to change their behavior,” says Lloyd. At Warp, he outlined three core reasons:

The first centers on productivity. “It’s still a bit squishy to measure, but I’m convinced it’s actually faster for many tasks and should increase overall engineering output, he says. The main reason here is it allows for multi-threaded development. “Especially for someone like me where coding isn’t my main thing anymore, I can now have multiple things going at once. I can literally be in a meeting and have the change I want to make running in the background,” says Lloyd.

Second, it’s especially useful when you’re trying a new skill or working on areas of code you are less familiar with. “Given how quickly our codebase grows, that’s likely a lot,” says Lloyd.

“And some of the more senior engineers have really come to like starting by prompt when they’re trying something new. For example, we built an entire BERT classifier model by prompt that we now ship with Warp to figure out if input is command line or natural language. No one on the team had experience building this kind of model before, but one of our senior engineers figured out how to use our agent to do it.”

[翻译失败，原文如下]

Third — and more unique to Warp’s case, given the product they’re building — is that dogfooding their product is the best way to improve it. “A not insignificant part of my reasoning for the mandate is to encourage everyone to use and give feedback on what we are building.We are asking our users to work this way and betting our business on it, so we had better believe enough in the workflow that we are willing to use it ourselves,” he says.

After three months, it's starting to have an impact. “Every single programming test that we’re doing right now to build Warp is starting with a prompt in Warp. Not every task is finished by prompting, to be clear, but the completion rate is getting higher week over week. I’d estimate we’re around 40-50%,” Lloyd says.

He shares a few specific examples from his own recent PRs:

- “I fixed a bug with our input where one of the settings around whether to show the model selector wasn’t being respected,” he says.
- “I had another PR I finished on around supporting the editor environment variable for opening file links in Warp,” he says.
- “I just wrapped up a more involved PR where I was adding the ability in Warp to hit Command-Shift-Alt T if you accidentally close one of your terminal panes, and it will come back as long as you do that within a minute. We had this already in Windows, but I was expanding it to work with panes. I built that one mostly by prompt, it was like an 800-line PR, but I had to do a lot of hand editing,” he says. “I had to spend a bunch of time upfront working with the agent to understand the code and then suggest the right way to implement it. I hit some bugs along the way where it was doing stuff that was causing crashes or there were tests that were failing, or I was overlooking things.”

Lloyd also shares a couple tactical pointers for getting started:

1. Set yourself up to multithread:“You either want multiple copies of your codebase or git worktrees so you can have multiple agents running at once,” he says. But set limits. “Anything more than 3-4 agents right now gets hard to manage in my experience.”
2. Lean into voice:"I would say I’m voice-pilled. Many tools have this now, but we built in a hotkey in Warp where you can just activate voice, so I speak most of the time when I’m coding now. Especially for long, involved prompts, where you would be typing so much, it really is quite helpful,” says Lloyd.

### Step 2: If the coding task succeeds, great! Share the success in #warped-it

Spinning up a Slack channel dedicated to AI wins has become standard fare across most companies by now. Explicitly making this behavior part of the coding mandate was important for Lloyd.

“Coding by prompt is a totally new discipline and we all have different instincts on how to do it well,” he says. “I’m in the channel posting my own PRs when I can, but I’m always lurking to get a more informal feel for the progress we’re making in using these agentic tools.”

Here’s a recent example:

![](/images/posts/b0e56128cad7.png)

“One thing that we do is we will take videos of success from this channel and repurpose them forWarp University, so there is a public facing aspect here, too,” he says.

Beyond the Slack usage, Lloyd’s other pointer here is simple: Show cool shit. “We’ve always had more of a ‘working in public’ demo culture at Warp,” he says. “Standups are mainly for demos, so the new flavor now is demoing what you built with AI.” He shares one of those very demos below:

![](/images/posts/5c0c95480dad.png)

### Step 3: If, after 10 minutes, you feel like you are wasting time by prompting…

1. Please share feedback with the relevant #feedback- channel on what failed
2. Please also share your prompt, conversation id, and so on so we can learn where the issue was and possibly build an eval around it
3. This is also a chance for folks to give each other tips on how best to use Warp to code

This is where the mandate gets practical. The 10-minute rule serves as a pressure release valve. “You could be running into server errors or client bugs. The agent might be going in circles, burning requests, forgetting context, and wasting time. Maybe you’re missing functionality that would help you achieve the task,” says Lloyd.

“The 10-minute rule is shorthand for ‘I gave this a try but I'm smart enough to know that it's not really going to save me time on this task,’” he says. “I’m trying to balance the imperative of ‘Try this new thing!’ with ‘I trust you as a smart person who knows what’s best to deliver business value.’”

Knowing where you're likely to run into problems is key here. “The likelihood of success at a given task is a bit proportional to the amount of public training data that there is on the kind of problem you’re working on,” Lloyd says.

“If you’re using a very well-known function, like Tailwind, there’s tons of public training data, and the models tend to do pretty well with these types of things. The bread-and-butter use case of one of these agents right now is building a React web app,” says Lloyd. “If you’re on a more bespoke language — and Warp has this problem being in Rust with a custom UI framework — the agent needs more guidance.”

Really large code bases tend to be very difficult, as well. “These agents still have relatively limited context windows, and so you need to do smart stuff around selectively adding context, or sometimes summarizing, or truncating,” he says.

When running into code by prompting roadblocks, the mandate requires devs at Warp to share feedback. “Too often things get lost in sort of an individual engineer’s frustration, and aren’t bubbled up to the whole team. I learn a lot more personally from the feedback channel,” says Lloyd.

He shares an example of a product fix that emerged from this channel: “I personally built this feature by prompt to allow users to use their terminal editor to open files. $EDITOR might be vim or emacs for instance, and this allows you to click on a file link in Warp and open it inside that editor.”

![](/images/posts/9615fb0fb150.png)

### Step 4: Try another AI coding tool (e.g. Cursor, Claude) and see if you have more luck — if you do, please report what went well and what didn’t.

“Using competitor products builds our understanding of where our product might improve and what’s possible. I think it's interesting for people to know if they can do the task better on Claude Code or Cusor,” says Lloyd.

“The main other tool people use is autocomplete in their IDE, typically Cursor. That’s the fallback that I go to if doing something agentically in Warp really isn’t working.”

### Step 5: Finally, just code by hand…we need to actually ship software and if that’s still fastest, you should do it.

“The last rule is to just bail out and do it by hand if you need to,” Lloyd says simply.

## The nuance to making it work:

As with most things, the real meat is in the more nuanced guidelines further down Warp’s mandate doc. “These are all focused on making the code as high quality as possible,” he says.

We’ll walk through each of these, with additional color commentary from Lloyd:

### Principle #1: Avoid outcome-based prompting

“This is a newer one we added in more recently,” says Lloyd. “After the mandate had been in place for a little while, I came to realize thatwe needed to more explicitly forbid what I call outcome-based prompting, where you basically describe how you want the app to work rather than how you want a feature to be built or a bug to be fixed. Devs need to say how a change should be made.”

For one, we’re not yet in a world where the agent understands your code base well enough to consistently pull off outcome-based prompting, Lloyd says. “Just letting the agent goal seek based on the outcome will end up wasting a lot of time by producing code that may ‘work’ but isn’t maintainable, testable, and composable.”

[翻译失败，原文如下]

But second, he’s found it has a real impact on learning. “New folks on the team won’t learn the conventions or the code base, and it’s hard to effectively review an agent’s code if you’re not familiar with this yourself. They need to learn the code base to a point where they’re at the level of skill, confidence and comprehension as a more experienced engineer on the team,” he says.

“At Warp, we want engineers laying out very specific plans for agents to follow, down to the level of, ‘Write this function’ or, ‘The data model should have these fields,’ and so on. What’s the API you want? Where should the code live? What tests should it write?This to me is the essence of engineering: I want to build something. I want it to be composed in a certain way,” says Lloyd.

More tactically, he recommends asking for an explanation or plan before an agentic coding tool starts making changes. “Ask for different approaches to the change. Make sure you get the big picture before it starts making diffs,” he says. “In Warp, our devs might do a big change end-to-end to push on what’s possible, but I still expect they’ll have to go back and break that up into comprehensible pieces post-hoc to meet our quality bar.”

It’s not just a watch-out area for junior devs, either. “I’ve seen too many senior engineers who'll be like, ‘Okay I want you to build this thing for me,’ and then the agent goes and spins its wheels and produces something that’s not up to the coding standards of the team and then they’re like ‘What a waste of my time.’Even with the quality of the models today, it’s still very much a human-in-the-loop, iterative process.”

“There’s this constant tension between context and exploration,” says Lloyd. “These agents need tons of context to succeed, but I also personally discover the best way to build through the act of building it. It’s a balancing act,” he says. “Otherwise it’s like writing a huge design doc for something up front.”

### Principle #2: You own the code. Period.

“I kind of hate the term ‘vibe coding,’” Lloyd admits. “It implies that when you code with AI you shouldn’t even bother understanding the code, and that the right way to develop is by just re-prompting until the thing works. This is fine for low-stakes projects, but definitely not for pro-development. In my view, this is one of the main hurdles deterring pro devs from using agents,” he says.

“It’s easy to get AI to produce something that sort of works, but much harder to get bug-free, well-factored code.We would go short-term faster if we just accepted the vibe coded stuff, but long-term way slower. So we’re just not allowing that at Warp, and this guideline gets at that” he says. “Until we get to a world where the agents are the predominant maintainers — which we are definitely not at right now — this one matters a great deal.”

Here’s what the mandate states:

Any code generated by agent mode must be at the same quality we expect for hand-written code. It must be well-factored. It must be well-tested. It must follow our coding conventions wrt comments, apis, imports, test file location, etc. All of the guidelines in our regularHow We Codestill apply when coding by prompt (small PRs, feature flags, and so on).

“I’m actually a very big proponent that users don’t use code, they use the product that you build. But it's also very much true that as code bases get bigger, it becomes harder and harder to build great products if the code becomes less comprehensible. The number one source of bugs, in my opinion, is repeated code that has slightly different behaviors,” he says.

“And the number one thing I’m finding that the code review process catches these days is agent code that could be duplicative of something else in our code base,” says Lloyd. “It might not follow the patterns that are in the rest of the code base, and it’s going to create tech debt if the agent writes it.”

### Principle #3: Babysitting beats one-shotting

“When I first started making changes with prompts, I would do a thing where I would just prompt, not really look very closely at the code, let it run, see if the feature worked, and kind of go round and round and round with the agent until the feature worked,” says Lloyd. “And then I made the mistake of looking at the code and was, ‘Oh my god, this is being done in what I consider a very hacky way that's going to be really hard for other people on the team to understand or use.’”

What he should have done, Lloyd says, was spend a bunch of time prototyping with the agent, understanding the code and then giving it specific instructions, either via iterating with it to form a plan and or giving it a file to use as its plan to then follow, then iterating with it as the agent goes to carefully check each diff.

“You kind of have to babysit it on harder changes right now, and if you don’t do that, you run a high risk of putting a bunch of time in trying to get the thing to work, only to look at the code and be left feeling that it technically works, but it’s not really useful, or it can't be merged,” he says.

“It depends on the type of task and code base. Some tasks are going to be fully automatable, and some even are right now, like simpler things like dead code deletion or flag cleanup. But for the bread and butter engineering work of building features and fixing bugs, you’re better off right now if you’re watching what the agent is doing closely and steering it,” he says.

This is an explicit point of emphasis in Warp’s product roadmap right now. “The thesis is that this approach works way better than starting the agent, going to make coffee, coming back an hour later and looking at a huge mass of code.”

Instead, think of it like managing a junior developer. “You don’t just give them free rein. You check in incrementally,” says Lloyd. “Ask the agent to make small, self-contained changes and commits and verify it is on the right track frequently. Having the agent frequently write tests as it goes is a good way of forcing it to work incrementally. (At Warp, the author of the PR needs to clearly explain how it works and the reviewer needs to follow theinternal code review guidelines.) Frequently look at the change that’s in progress to make sure it’s proceeding how it would if you were to write it by hand.”

## The future of engineering:

While Lloyd’s pleased with the progress to date, he’s got more changes on deck for Warp’s eng team. In addition to tracking more concrete productivity measurements, he’s looking at implementing a new technical interview session. “We’ll likely ask engineering candidates to build something by prompt before the end of the year, we just haven’t spec’d it out or calibrated how to do that interview yet,” he says.

“We already do a thing we call a ‘Product Session,’ where every engineer goes through something that’s a little bit more like a product manager interview. We’ve always tried to hire product-first engineers who can talk to users, understand the problem they’re solving, and who can make good decisions when there’s ambiguity around mocks,” Lloyd says.

“In the past, we’ve asked them to come in with a couple of ideas on how to improve Warp, and what I want to see these days is for them to suggest problems that we could solve with agents rather than terminal UI or collaboration ideas, which is historically what a lot of folks have come in with,” he says. “I want to make sure we’re hiring folks who understand this powerful new lever we have for helping users.”

That mentality might not be a fit for all candidates. “Those who think of coding and development as synonymous will see this as a big shift in what the engineer’s job is and may resist.But in my view software engineering != writing code,” says Lloyd.

[翻译失败，原文如下]

“Coding — literally the act of typing code — is not the essence of the software engineering role and it kind of never has been in some sense. Good engineering, however, is central to the job, and that won't change. And that’s about understanding specifically whatproblem you’re solving for a userand being able to build a piece of software that effectively solves that for them,” he says.

“And that task doesn't change at all in a world where you're asking an agent to do work for you. If anything, it becomes more important as coding is delegated to agents. I see us moving to more of a model where everyone becomes a tech lead in a way. Agents will do some, maybe even all, of the tasks, and the engineer job will increasingly be about multi-threading. And the best engineers will still thrive because they are great problem solvers and system thinkers.”

---

> 本文由AI自动翻译，原文链接：[Start With a Prompt: Inside Warp’s AI Coding Mandate](https://review.firstround.com/warp-ai/)
> 
> 翻译时间：2026-10-08 08:37
