---
title: 'Investing in Internal Documentation: A Brick-by-Brick Guide for Startups'
title_original: 'Investing in Internal Documentation: A Brick-by-Brick Guide for Startups'
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/investing-in-internal-documentation-a-brick-by-brick-guide-for-startups/
author: ''
summary: '[翻译失败，原文如下]


  It’s the middle of the night when the on-call engineer jolts awake as their phone
  flashes and chimes with a flurry of push notifications,...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-16T07:27:07.612390'
---

[翻译失败，原文如下]

It’s the middle of the night when the on-call engineer jolts awake as their phone flashes and chimes with a flurry of push notifications, text messages, and phone calls. The production server is down and they’re responsible for getting it back up as fast as possible. With bleary eyes and a foggy mind, the engineer frantically searches for answers in Slack, Google Docs, and GitHub but they only turn up vague mentions of the error. With no meaningful information to orient around, they’re forced to wait anxiously for one of the veteran engineers to wake up as the outage drags on.

Mission-critical knowledge trapped in an early hire’s head is an all-too-common problem that startup engineering orgs know well. But investing in internal documentation is often a chicken-and-egg scenario. In the earliest days of a fledgling business, there’s a golden opportunity to write things down in the moment as you’re gaining valuable knowledge and charting your course.Each new hire who joinsquickly takes on heaps of responsibility, and these documents can be a critical resource for getting up and running quickly without slowing down the pace of business.

But with a bafflingly long to-do list and small teams, carving out time to document these lessons quickly falls to the wish-list pile, and those best-laid plans to write as you go tend to evaporate. Put on the back burner, these critical insights are lost to time.

As an early docs leader for companies like Stripe, Uber and Salesforce,David Nunezhas seen this cycle repeat time and time again — and he’s often been brought in with the mandate to clean up the internal documentation debt. (In the spirit of practicing what you preach, Nunez even wrote down his lessons, co-authoring the book “Docs for Developers,” a handbook for technical writing.)

Companies like Stripe have made delightful developer documentation one of the secret weapons in a crowded market. But there’s one common pattern Nunez has seen over and over again that plague startups of all, well, stripes. “A lot of early-stage employees become the heroes of the company. They build a lot of features, solve major outages and come up with novel ways to improve the infrastructure. As the company grows, more folks come in and, without things written down, that old guard gets bombarded with questions. It creates a vicious cycle where new hiresquickly realize that the fastest way to get answersis to just ask the old guard,” says Nunez. “Suddenly, all of the value these early heroes delivered initially, which was building and shipping, they now have much less time for.”

Another common pitfall? By the very nature of the documentation being internal, it’s more difficult to borrow from established playbooks of other successful companies. Companies like Stripe andAmazon have become renowned for their writing culturethat up-and-coming startups envy — but there’s no clear roadmap to follow if you’re looking to replicate their approach.

“It’s inherently harder to emulate other companies doing this well because the documentation is hidden away internally. Instead, you’ll have a CEO who meets with a leader at Stripe or Amazon and comes back and says, ‘Documentation's really important — we're going to focus on it.’ The intentions are good. But there's no clear, practical direction or follow through,” says Nunez.

And to be clear, Nunez is not just singling out early- or mid-stage startups here — BigCos can be just as guilty of creating a documentation caste system. “If you go to any meaningfully successful company with longevity, they’re going to have at least passable external documentation, like an onboarding guide or troubleshooting instructions, because users depend on it. But time and time again, you see enterprise companies with 100 tech writers and a 20-person engineering team working on external docs — but zero people are working on internal docs, like explaining how the systems architecture works,” says Nunez.

In this exclusive interview, Nunez outlines specific steps for creating a culture of good internal documentation hygiene. Pulling from his own playbooks as Uber’s first dedicated docs hire and the first-ever Head of Docs Content for Stripe, he shares ultra-tactical advice for each part of the process: from building the habit and incentivizing engineers to make the effort, to keeping things organized. While his guidance is specifically geared towards startups without a dedicated documentation team, there are plenty of tactics for larger orgs who have gotten off course and want to right the ship.

## STEP 1: START WITH A CULTURAL SHIFT.

Documentation is often seen as a nice-to-have — a can you can kick down the road until "you have some free time," or, worse, until a critical outage forces the organization to reckon with it. “A lot of times people wake up to the need for documentation resources when something terrible happens and things go perfectly wrong,” Nunez says.

Uber is now famous for how it deployed meticulous internal playbooks for launching its service in a new city. Employees could land in a city with no Uber footprint, armed with a playbook chock-full of documentation on what had worked well in San Francisco and New York. But despite these early wins, the company got a painful wake-up call that they needed to invest even more in internal documentation.

“At Uber, we were starting to pay attention to documentation and assembling some resources, but the engineering team was growing way faster than the documentation team could keep up,” says Nunez. “Then there was an outage because a data center in China was overheating. An engineer followed the steps in the runbook, and they actually made the outage worse and totally melted down the data center.”

A root cause analysis uncovered an unlikely culprit. “The runbook was inaccurate and had the steps listed out of order. The runbook was obviously very sloppily written, and it woke leadership up that we needed to get a handle on our documentation standards,” says Nunez.

It might seem like the immediate fix is hiring folks to solve the problem. But rather than kicking off a recruiting sprint to find your first documentation hires, Nunez suggests a different approach. “The default is that companies under-resource documentation efforts which, of course, leads to weak documentation. But I’ve also witnessed companies that do throw a lot of money at documentation, but not in the right areas or with the right approach, so engineers don’t regularly use the docs,” he says.

“I wouldn’t recommend early-stage startups just go out and hire a full-time docs writer. I’ve learned that, especially in high-performance environments, changing the culture is the highest leverage investment you can make,” he says.

Changing the culture can seem like a fuzzy, woo-woo kind of solution to a complex problem. But Nunez outlines two key steps for getting started:

### Model good writing habits.

“You can’t have a strong documentation culture without a strong writing culture. The most effective approach I’ve found in embedding this into your culture is ensuring that leaders, from the founders to the frontline manager,take their own writing seriously,” says Nunez.

Try these two regular habits for getting started:

- Recap regularly.“The most effective way for leaders to sharpen and exemplify their writing and knowledge-sharing skills is to take meeting notes and follow-ups more seriously. Sharing your own action items and takeaways from the meeting will give others a nudge to model this behavior.”
- Get existential.“What did you learn recently? What is your interpretation of current company goals? What recent shifts have you made to the strategy? Sharing musings on a regular cadence offers important context, and they also reinforce the importance of writing and sharing knowledge, which will trickle down to the rest of the org.”

### Get in the habit of editing.

[翻译失败，原文如下]

“Going back to school, you typically had the Scantron crew, who were happy when a test was multiple choice. And then you had the paper crew, who were happy when they could write an essay. Usually, this was very polarized,” says Nunez. “People who don’t think they’re great writers tend to write less and less and are terrified of having their writing critiqued.”

But editing is critical to the writing process — whether you’re a natural with prose or always dreaded writing essays in school. “Every professional writer has had their writing picked apart over the years, from their professors to coworkers and peers. They accept that it’s just part of the writing process to produce something that’s of high quality.Letting others critique your writing is a vulnerable position to be in, but practicing your writing and getting feedback is the only way to get better,”he says.

Foreng folks looking to bolster their writing chops, Nunez suggests a bit of reverse engineering. “Look for examples of good pieces of writing internally or externally and try to diagnose why it was so effective. How did they convey the information so clearly? How did they retain your attention well? Was the language concise? Did they write an engaging intro?” says Nunez.

And when you’re working on your own document, try to bring in a test case. “An easy exercise is to give a draft of your document to a peer and ask them to explain what they read. If they’re confused, you know you have work to do. If they understood the key points you wanted to get across, you accomplished your goal,” says Nunez. “Don’t get too hung up on being a natural writer — focus on becoming a great editor of your own work.”

### Make writing a part of the job ladder.

Eager to fix their flawed internal docs, plenty of leaders jump right to tactics — trying to build the perfect process for baking docs into the software development cycle or swapping out a tool hoping it solves the problems.

Instead, start further upstream: with your hiring andpromotion processes. “I’ve found that if you codify knowledge-sharing expectations in job descriptions and job ladders, folks will inherently look to fulfill those responsibilities on their ladder,” says Nunez.

Through trial and error, he now advocates kicking off your documentation efforts with this step. “At one point, Uber was revising the software engineering ladder. I was able to collaborate with the engineer who was leading the refresh efforts and we put documentation expectations at each level. Overnight, people were coming to us saying, ‘I want to meet expectations for my role.What can I do to meet these requirements?’ It was like a lightbulb went off,” says Nunez. “So when I joined Stripe, I took this step in the first week.I put one line about documentation on each level of the job ladder,’” says Nunez. Here are his suggestions for language you can borrow in your own job ladders:

- IC new grad:Make sure your code is well-documented, with helpful code comments and READMEs.
- Senior IC:Make sure your services and systems are well-documented, with diagrams and end-to-end guides.
- Eng leader:Make sure your team has sound documentation practices, from code review to incident review.

With performance reviews and promotions now on the line, folks started prioritizing this sort of work. “I quickly saw many different documentation ideas and projects I would not have considered on my own arising from an engineering org — like building a Slack integration to automatically suggest relevant documentation when asking a question. Just tell engineers, ‘This is important — you're being evaluated for this.’Then watch what happens,” he says.

Nunez also suggests two other tactical ideas for teams to try:

- Shine a spotlight, even outside of performance review season.“One manager included their ‘doc star of the week’ in each weekly update she sent. It’s such an easy thing to just call people out, and folks love to be recognized — especially for doing something outside of their comfort zone.”
- Carve out the time.He’s also seen other teams do “docs bashes” (like bug bashes) where the whole team will spend a day, or even a week, just working on documentation. “Make a leaderboard and see how motivated engineers get to contribute.”

## STEP 2: GET STARTED PAYING DOWN YOUR DOCS DEBT WITH A MVP APPROACH.

Even with a cultural shift in motion, you’re likely still facing down tons of documentation debt that’s built up after months (or years) of deprioritizing this work. It may feel like trying to get a 16-wheeler to make a sudden U-turn.

Nunez suggests navigating this bend gradually, so as to not tip the truck over. Start by identifying the most critical topics to tackle first. “Send out a survey to engineers, or look at the most common internal questions popping up in Slack. You’ll likely have 100+ topics with poor documentation that engineers complain about, but in the beginning, you have to align most of your resources behind a narrower focus.Try to identify the top five to 10 technical topics that engineers are struggling with the most and invest in those,” he says.

Resist the urge to just make assumptions about what folks need. “When we were getting started with this work at Uber, we looked at the internal data for what engineers were searching for the most, and the data really surprised us,” says Nunez.

“We found that engineers were struggling mightily with an arcane technology they had to use for server configuration and management. At larger companies, you’d have an operations admin or team of specialists with expertise in this software, but at the startup stage, every engineer needed to use it at some point to deploy changes. It was horrifying for them because if an engineer made the wrong change, they could cause a huge outage to the service — and they often did,” says Nunez. “We identified this need, bolstered the documentation, incorporated feedback, and immediately saw complaints about this topic go down, as well as heavily decreased mentions of this software in root-cause analyses for outage incidents.”

### Focus on quality, not quantity to set the bar.

As a bonus, by identifying the most critical topics, you’ll make more meaningful progress faster and develop high-quality examples of documentation that others in your organization can emulate. “When you start focusing on documentation, justifiably, engineers are going to say, ‘I've never done this before. Give me an example.’ By putting more effort behind fewer, high-quality resources, you show people what ‘great’ looks like. You raise the floor really quickly,” he says.

He shares an example for building this muscle memory from his Uber days. “At the very beginning, we started with a document simply on how to set up your environment and set up your dev box so you can actually start committing production code. It was a task that every new engineer would have to do, and without the documentation, folks were just sitting in a room helping the new engineer do it manually,” says Nunez.

“Once we helped that team create a clear getting-started guide, that was well-organized and easy to read, we were able to use that as a golden reference for other teams looking to pay down their documentation debt,” says Nunez. Other ideas for getting started with your documentation include:

- Code style guides:“Standardizing your coding styles reduces cognitive overhead during development and code reviews and creates a much cleaner codebase.”
- Glossary:“Every company has their own terminology and vernacular for systems and services. Creating a glossary is such a simple way to create a source of truth for important definitions.”

### Act as a journalist.

[翻译失败，原文如下]

Simple topics like setting up your dev environment can be fairly straightforward. But others (like Nunez’s earlier example about an arcane server management technology) can be much more complicated to start capturing. Rather than tracking down scraps of outdated memos, mixed with emails, Slack messages and emails, Nunez suggests finding one source of truth.

“We would sit down with the person who had the most knowledge on the topic and whiteboard to get the main points down. Then the doc writer would have a genesis of a document and probably a handful of other engineers’ names as leads for more information. Pretty quickly, you’d publish a documentation set engineers could rely on that didn’t exist before,” says Nunez. “We had one writer who churned out documentation so quickly because she would record the meetings with engineers, transcribe the audio to text, and just clean it up a bit and publish before moving on to the next doc.”

You can apply this same practice to much more complex documentation feats, too: “At Uber, we had no canonical document or diagram of what our service architecture looked like. Things had grown and changed so fast — it wouldn’t be described the same from person to person. This is problematic because you can’t build for security and reliability when you don’t know how all the pieces fit together,” says Nunez.

“We started with one knowledgeable tenured engineer to theorize on a whiteboard with us and describe how thingsusedto work. Then we used this as a baseline to track down other folks who could help fill in the gaps. Within weeks we had a pretty good document on our architecture and, just as importantly, an accurate diagram for engineers to understand the systems in play.”

### Empower your senior engineers.

As you climb your way out of your documentation debt, rather than anointing one person on the team as the documentation deputy, Nunez strongly encourages bringing senior folks into the fold.

“Educate your senior engineers and hear them out on what they need to help build a strong documentation culture, and keep up a dialogue to maintain these new norms. Having senior engineers enforcing doc standards during architecture discussions and code reviews is a great way to solidify documentation in the development lifecycle. Pretty quickly, it will be so commonplace that engineers won’t even think of it as an extra step anymore. And new engineers who come in will quickly follow suit,” he says.

## STEP 3: STOP THE RANDOM ACTS OF DOCUMENTATION AND GET ORGANIZED.

Getting into the habit of writing things down is just half the battle — organizing your docs in a logical, easily-searchable manner is another stumbling block engineering teams face. Without an agreed-upon organization system, you’ll find yourself with an ever-expanding pile of docs with no sense of what’s current and accurate.

“This is terrifying for a lot of teams to tackle because this has nothing to do with writing anymore. Now you have to figure out how people can actually find it. And I've learned that giving the advanced course on information architecture is extremely overwhelming for engineers. They don't even want to start, because they realize they can't envision what the end state looks like — but they know it's going to be a lot of work,” says Nunez.

But curating and organizing content can be a major win — particularly for organizations that are a bit iffy on whether documentation should be a priority in the first place. “If you focus on curation first, rather than trying to write up tons of net-new docs, you can make such a wide-reaching impact in a relatively short period of time. And you don’t need as much context to do this well. Take inventory of what exists, merge the duplicate content, remove outdated content, clean up and update some important content, and then organize it into a neat structure,” says Nunez.

These may seem like cosmetic changes, but they can offer a big bang for your buck. “It allows  engineers to find and understand important documentation much easier, which will be immediately evident and provide immediate value — which will allow you to invest more in better tools, processes, and even dedicated documentation resources down the line,” he says.

### Assemble your list.

Start with the organization basics, rather than trying to get too complex too quickly. “Just put all of the important docs that you have listed in a spreadsheet,” says Nunez. The goal here is to centralize everything in one place, rather than having folks commit “random acts of documentation” that become a disorganized mess.

“That gives you some wet clay to come up with some structure and eventually migrate those documents over to a content repository. But for the time being, you can quickly identify in the spreadsheet which docs are redundant, if there are any significant gaps, and opportunities for a better structure.It's very low stakes because you're just dealing with some URLs and you can get feedback from folks, but it’s much better than having countless people just putting docs wherever they want,” says Nunez.

As you’re tracking down documentation to add to your spreadsheet, keep in mind these five documentation buckets that exist at most decently-sized companies. (Nunez notes that smaller startups might not have all of these in their arsenal just yet.)

- Onboarding documentation.“These types of documents are often overlooked, but they are just as, if not more important, than any other type of content. Onboarding docs create an efficient path for new hires,” says Nunez. He suggests a low-lift, unstructured method for getting started: “As you grow your team, ask each new hire to just write down what they’ve learned after the first few months. Each hire will build on what was documented before. After just a few hires, that’s a really solid onboarding guide,” he says.

- Task-based documentation:For example, instructions for your internal users on how to build a new endpoint, integrate with an interface, or use a new feature.
- Runbooks:How to perform a set of tasks in a specific order to perform a common operational task like spinning up a new server or resolving a common error.
- Architecture and design documents:This is the backbone documentation that provides useful context for all other documents and knowledge capture, describing how a system works.
- Wiki-style team documents:Including meeting notes, memos, musings, proposals. Nunez’s tip: “Write these liberally, but keep them separate from the other docs listed above. These are great resources for teams to quickly capture and share knowledge, but they can be highly noisy.”

And if tracking down all kinds of docs across the engineering org to add to your spreadsheet seems impossible, he boils it down to simple marching orders. “Any curation and organization is better than none at all. If you don’t want to sort through hundreds of docs,for a quick win, just look for the top 50 most popular documents. This can be done in a day and yield immediate impact,” says Nunez.(Most content tools have some sort of analytics out of the box — or if you’re storing your docs in a database, you can run a query to get this list.)

### Identify ownership.

You can spend hours of time assembling a thorough, clear document. But too often, folks skip over one of the most important components: The author name. “You can get fancy with a ledger that records which team owns which document, but even if you manually input a team name at the top of a document, you’re creating more accountability and also allowing people to track down the team if a doc needs updating,” says Nunez.

[翻译失败，原文如下]

And for folks looking to level up, he suggests assigning a team in the page’s metadata, which then allows the owner to be automatically notified to review their docs on a scheduled cadence or when the code changes. “As the company grows, you have reorgs every few months. And the team’s name changes or folks rotate off. That's when you want to build something a little more sophisticated,” says Nunez.

### Assign a rotating docs czar.

To keep things centralized and accessible, identifying a central owner of not just each individual doc, but also the central spreadsheet is essential — even if you’re not quite ready to make a dedicated docs hire just yet. “If you have 10 teams responsible for their own content organization, no one is focusing on how those 10 documentation sets form a cohesive whole,” says Nunez.

He sketches out an example of why that can cause heartburn: “With infrastructure projects, engineers are often looking to perform end-to-end tasks and they’re likely going to need to work with interfaces built by multiple teams. If the documentation is fragmented by team, it’s going to be extremely painful to get these kinds of end-to-end tasks done.”

But if no particular engineer or product leader raises their hand to own the docs spreadsheet, try a communal approach, with a rotating owner responsible for monitoring and maintaining the spreadsheet for the week before passing the role onto the next person in line. “You’re the basic moderator and you’re looking for outliers, ‘Oh, somebody created a new doc for this topic, but I know this other document already exists.’ Or, ‘Somebody made this a child of the home page, but it actually should be nested under this other thing, over here,’” says Nunez.

### Don’t be afraid to delete.

His biggest piece of advice for keeping your docs organized? Empower folks to delete. "Whether it’s realizing that a document explains a system that doesn’t exist anymore, or a doc is completely out of date,people are terrified to just delete a doc, even if it confuses your engineers and muddles search results. At the very least, you should archive it. You’re making the overall system better by removing things that are no longer useful,” says Nunez.

### Level up with landing pages.

After going through the spreadsheet organization exercise, Nunez is a big proponent of landing pages as a way to level up. “Landing pages are often overlooked, but easy to make and highly valuable. These are the guideposts at each major user decision point,” he says. “Most internal hubs are just blobs of documents and you try your best to search for what you need. But your internal search engine and your internal content’s SEO are likely poor. Circumvent this shortcoming by making content easier to browse,” he says.

To keep things simple, try building an internal docs homepage with these landing pages:

- Backend development
- Frontend development
- Security
- Metrics and Monitoring
- Storing and managing data

## STEP 4: BRING DOCS INTO THE DEV CYCLE — DON’T WAIT FOR CODE-COMPLETE.

So far, we’ve discussed fixing your documentation debt by writing up missing docs and organizing them in a way that makes them easy to track down. But truly finding doc nirvana requires moving from a reactive to a proactive documentation habit. That means documentingwhiledeveloping a new feature, rather than just saving it until the end after launch.

But when faced with a time crunch to hit a deadline, most teams tend to postpone documentation until after a feature is released. Or in Nunez's case once, learning his team was on the hook for crucial documentation at an all-hands meeting, along with everyone else on the call. "One time our engineering leadership made the decision to immediately trim our internally sanctioned programming languages from seven down to two. The promise to engineers was that the services written in these two languages would be impeccably documented. Unsurprisingly, on such a short timeline, this promise went unfulfilled at launch," he says

While tempting, leaving documentation for the end is the surest way to deliver shoddy content that frustrates your developers and, ultimately, the users of your product. “There’s always something new to work on instead of taking the time to document what you just built. You’re either looking to improve the feature, you’re fixing bugs, or it’s just code-complete and you don’t want to think about it anymore — you’re working on the next thing,” says Nunez.

### Take a snapshot.

A low-lift way to document while you go, rather than staring down a blank page once you’re code-complete, is what Nunez calls a snapshot document. “Creating a snapshot just means writing down the actual steps required to complete a task as a user. In the early stages, this can be messy, but it should be accurate. You don’t need conceptual context yet, just simply the steps and inputs a user must follow to use the product for the tasks you want them to complete,” he says.

This will save your team lots of time and frustration — and ultimately result in better products. “Not only will this allow you to take a more sustainable and iterative approach with your docs, but you will also gain valuable insight into what it takes to be successful with this product at each stage in its lifecycle. The product may seem simple, but when you document the steps for success, you may find there are 25 discrete steps to accomplish a task that you’ll want to whittle down to five,” he says.

## WRAPPING UP: JUST GET STARTED.

Just like there’s no one tried-and-true path to finding product-market fit, assembling your early team and other startup “firsts,” there’s no one way to build out your documentation process. “In joining engineering orgs as their first docs hire, I’ve started with producing net-new content first, or curation, or implementing better tools, and I’ve started with evangelism first.There’s no one ‘right’ entry point into better internal documentation — it’s just about getting started,”he says.

So as you start paying down your documentation debt, maintain an MVP mindset — laying down your foundation, brick by brick, rather than trying to build Rome in a day.

---

> 本文由AI自动翻译，原文链接：[Investing in Internal Documentation: A Brick-by-Brick Guide for Startups](https://review.firstround.com/investing-in-internal-documentation-a-brick-by-brick-guide-for-startups/)
> 
> 翻译时间：2026-09-16 07:27
