---
title: 'From Memo to Movement: Shopify’s Cultural Adoption of AI'
title_original: 'From Memo to Movement: Shopify’s Cultural Adoption of AI'
date: '2026-10-07'
source: First Round Review
source_url: https://review.firstround.com/shopify-ai/
author: ''
summary: '[翻译失败，原文如下]


  When Shopify co-founder and CEO Tobi Lütke publiclyreleased an internal memodeclaring
  reflexive AI usage a baseline expectation at Shopif...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-11T08:05:42.334154'
---

[翻译失败，原文如下]

When Shopify co-founder and CEO Tobi Lütke publiclyreleased an internal memodeclaring reflexive AI usage a baseline expectation at Shopify, the format became a genre —Box,Fiverrand even thePrime Minister of Canadaquickly shared their own versions externally, while many more companies did so internally.We wanted to find out what happened inside the companyafterLütke hit send.

![](/images/posts/07668fa8931e.jpg)

As it turns out, Shopify’s internal response had been years in the making. The memo certainly accelerated things, but the company had already been an early and eager AI adopter. Shopify’s VP & Head of EngineeringFarhan Thawarbrought GitHub Copilot into Shopify so early that he couldn’t even pay for the product yet.

“A year before the release of ChatGPT, we were already using Copilot. Pretty quickly, our adoption increased to 80% and GitHub started asking us how we did that,” says Thawar. “At the time, I thought it was terrible.20% of engineers still aren’t using Copilot?But we got to 80% so quickly because people were finding value quickly.”

For years now, Shopify has been learning what makes AI work within a company. We sat down with Thawar to learn how three non-obvious insights led to the specific tactics and workflows the company used to bring Lütke’s memo to life.

## Let anyone use the expensive models

Many companies grant org-wide access to the most basic AI tools, reserving the more powerful models and apps for only technical teams. Instead, Shopify allows anyone to use every tool and model.

The thesis is that high-value use cases can come from anywhere in the company, and you have no idea which will emerge as the most impactful and most worthy of the good models.

To actually get people to use the best and latest models, Shopify used these three tactics:

### Tactic: Get your lawyers to say “yes” by default

It starts at the top: the entire senior leadership team needs to agree that AI adoption is the most important thing you can do, which includes legal teams. Alignment at the highest level means everyone understands you have to find a way to get to “yes,” including the key conversations around security and privacy. “If you don’t default to ‘yes,’ you’re defaulting to ‘no,’” says Thawar. “If left undefined, which is what most companies do, that’s basically a ‘no.’”

When Thawar wanted to adopt GitHub Copilot in late 2021 his conversation with Shopify’s legal team was straightforward: “The first thing I said was, ‘Hey, we’re likely going to do this. How can we do it safely?’” says Thawar. “They said, ‘Let’s figure out a way.’ There was no opposition.”

This sentiment contrasts starkly with experiences from CTOs at other top-tier tech companies facing legal obstacles, which Thawar hears from his respective peers in a WhatsApp group.

### Tactic: Unlimited spend on AI tools

![](/images/posts/c8ba81b98235.png)

Wall-to-wall AI use comes with a price. As Cursor adoption spread within the company, internally there was some fear that it’d get too expensive. But that’s the opposite of what Thawar wants: everyone using AI if they’re getting value from it.

Thawar can see the people getting value by using an internal leaderboard of who’s spending the most on additional Cursor tokens.“We don’t have a quota. And I don’t want people to gamify it with scripts, but it’s a cool proxy for value. We don’t want any friction for people using AI as much as they want or using the latest large models,” Thawar says. “I know folks who are proud to show up on the top 10 token spend leaderboard due to valuable work being done.” Recently, one of those people was Shopify CTOMikhail Parakhin.

“I’m seeing a concerning trend in talking to CTOs and CEOs about the cost of tokens,” says Thawar. "They’re thinking, ‘Can I afford an extra $1,000 - $10,000 per month per engineer as they use tools like Cursor, Windsurf, GitHub Copilot, and more?’ So they clamp down on spending.”

This mindset is at odds with the goal of driving AI adoption. “If your engineers are spending $1,000 per month more because of LLMs and they are 10% more productive, that’s too cheap. Anyone would kill for a 10% increase in productivity for only $1,000 per month.” (In fact, if your engineers are spending $10,000 per month and getting value, Thawar wants you toDM himso he can learn what you’re doing.)

### Tactic: One AI interface and MCPs for everything

![](/images/posts/d665ca881b29.png)

Shopify makes it easy for people to access, use and build with the latest tooling by putting everything in one place — the company’s internal LLM proxy, a tool that allows users to easily interact with a wide variety of models and switch between them through a single access point. In production, the proxy helps with scaling, tracking, and failover use cases as well.

Employees can use the LLM proxy to build the workflows they need. They can select from different models, which are updated with the latest versions as soon as they’re released. There’s a collection of MCPs, and all it takes is asking the proxy (or another tool like Cursor) to access them. There’s even a stable of agents already created by other people for anyone to use. It’s a one-stop shop for everything someone needs to use AI.

![](/images/posts/8157180fb0dd.jpg)

MCP servers are an important infrastructure layer that connects all the company’s internal tooling. “MCP everything,” says Thawar. “We make every single piece of data inside the company available, even though that data lives inside all these different tools. It’s ready for people to interrogate and figure out their own workflows.”

![](/images/posts/448000897063.jpg)

With this MCP, Cursor and chat infrastructure in place, people across the company can accelerate their work rapidly, whether they’re technical or not. Some notable examples fromoutsidethe R&D team include:

Workflow: A site audit tool that changes how prospecting works

Shopify uses website performance benchmarking as an important tool in the sales process. When they claim industry-leading site speed to prospective merchants, they’ve got to analyze the prospect’s site and show how Shopify performs better. Previously, a human had to compile this data via site audits, which is time and labor intensive.

Recently, a non-technical sales rep used Cursor to build a tool that generates detailed performance comparisons automatically. It pulls data from the prospect’s website, compares that against Shopify’s benchmarks and even provides talking points to assist in the sales process by tapping into internal documentation.

Shopify CROBobby Morrisonhas praised this kind of thinking and approach to working with AI: “Our top commercial builders are transforming every aspect of our work, from analyzing markets and identifying opportunities to developing strategies and creating solutions for merchants. The most successful are those who embrace AI fluency — people who intuitively collaborate with these tools and evolve at AI's speed. They don't see AI as separate; it's simply how work gets done.”

As Shopify sees it, the real opportunity is that it allows you to rethink how you sell.“For example, in an upsell situation, a rep might be on the phone while an agent gets data that used to take a long time to fetch, but now takes seconds. This kind of sales data used to be scarce, now it’s abundant,” says Thawar.

“How might that change the sales approach? You could speak more authoritatively on something, which means you take a different path through the organization, which means you might structure the way you do cold calls differently.”

Workflow: A sales engineer’s “What should I do today?” page

A sales engineer brought the MCPs of his most frequently used tools — GSuite Drive, Slack, Salesforce, and more — into a Cursor-built dashboard that prioritizes his tasks using real-time context from all these tools.

[翻译失败，原文如下]

Normally, he’d have to bounce between these different apps. Instead, he asks his dashboard “What should I do today?” It looks at Salesforce to see an almost-closed opportunity, but notices he hasn’t responded to an email from that prospect, so it prompts him to respond to that email. “He literally doesn’t work in any of those other tools anymore. He works in Cursor as his homepage. He doesn’t go into email. It’s insane,” says Thawar.

This is exactly the kind of impact Shopify wants to see from its investment in AI infrastructure, especially from a companyknown for building infrastructure. “It’s logical for us to also build out our internal AI capabilities infrastructure-first,” Thawar says.

“Instead of just building the feature, which might take a few weeks, we’d rather spend longer building the infra. In this case, we have the LLM proxy, we have the MCP servers — we’re trying to build this into a system that people can just reuse. For example, once someone creates the Slack MCP, everyone can use it.”

Workflow: Request For Proposal agent removes toil and increases win rate

RFPs are a fact of life when you’re selling to big brands. And each one has hundreds of questions and asks for customization, institutional context and cross-functional collaboration to execute well.

So the Revenue Tooling team created an agent that answers multiple RFP questions at once. Built usingLibreChat(to which Shopify is a core contributor), the agent gives solution engineers a way to generate fast, context-rich responses without manual toil. It leverages an internal content repository to automate the entire process, looking at Shopify’s public documentation, help docs, case studies and more, citing those sources so users can confirm them.

When questions get answered, the agent also assigns those responses a certainty score — showing that it either had, or didn’t have, enough information to answer the question accurately.The best part is that it learns from previous answers that have led to RFP wins, and then the resulting RFP goes into the repository to make future RFP responses better.

![](/images/posts/8b52aa04326d.jpg)

## Make AI show its work, not hide it

![](/images/posts/de416922e603.jpg)

A real concern many people have is that reflexively using AI for everything all the time disengages your brain or cognitively disassociates you from the work being done. But the counterintuitive flip side to that is AI done properly can show you even more details and get you even more engaged.

“Most people will tell you the ideal UX for both internal and user-facing products is for you to ask a question and receive the answer, not the messy details,” says Thawar. “But if your goal is to teach people how to master something, showing them those details is better.”

### Tactic: Context engineering humans

Shopify recognized that driving effective AI use isn't just about better prompts, it's about turning what Lütke has come to call "context engineering" into a systematic practice.

Here's an example: Project champions write updates every week, which makes the company’s project management system an information superhighway. Now, an AI agent ingests all the pull requests from GitHub, docs and comments, Github issues and information about a project from the Slack channel to automatically write these updates.

On Fridays, project champions are provided with an AI-written update with specific prompts, which challenge project champions, “What did you get done this week?” in a way where those champions critically engage with the summary to make it better. They’re incentivized to bring misalignments forward and expose unobvious risks, and not just mindlessly accept completions, because they care about their work being understood correctly.

“With that information, the AI writes a new update.Then we try to do a diff on how much the actual final update was rewritten by the human, and the AI gets smarter based on that rewriting,” says Thawar. These updates would’ve required a significant amount of context-gathering and content creation, and instead, project champions can focus on the parthumansneed to do, which is critically engaging and challenging the work to be better.

#### Workflow: “Roasting” your code (and teaching you at the same time)

Shopify runs one of the largest Ruby on Rails applications in the world. It constantly pushes the limits of how many engineers can practically contribute and maintain a single codebase of its kind. This is a particularly interesting challenge in Ruby, which optimizes for individual developer empowerment over rigid configurations that scale safely.

Shopify engineers realized that AI could be a powerful companion tool for maintaining “convention over configuration” for unit tests, code updates and more. But on its own, AI wasn’t trustworthy either — it needed explicit structure and the right pairing with deterministic tools and principles.

So Shopify builtRoast, an open-source AI orchestration framework for checking, fixing and iterating code contributions. It derives its name from an internal AI tool that “roasted” existing code and unit tests, providing constructive criticism and recommendations for improvement. Rather than leaning on a single prompt that has to do everything, Roast lets developers design and run repeatable feedback loops with small, targeted steps that have a high probability of success:

- Roast structures workflows in steps, showing the AI’s reasoning at each one.
- Workflow steps build up a conversation history, which lets engineers trace how AI came to its conclusions.
- The CodeAgent (built with Claude Code) summarizes its actions and why it took them.
- For something like test grading, Roast gives detailed feedback on why something scored well or poorly. It’ll surface the “why” and “how” before offering final results.

“Using deterministic and AI tools in tandem is a wildly powerful combination — one can inform the other and cover the gaps,” saysSamuel Schmidt, Staff Developer at Shopify, who helped build Roast. Roast simplifies the use of agents and shows its work to engineers pairing with it, making it easier to execute processes in a repeatable, scalable manner.

The tool has solved tactical challenges for Shopify engineers internally, helping them analyze thousands of test files and automatically fix common issues to increase test coverage across the board. But while solving those challenges, the team also identified a way to use AI more reliably for complex engineering tasks — a new paradigm many teams are encountering. So Shopify made Roast open-source, inviting the community to help shape the future of AI-assisted task execution.

![](/images/posts/4887782353ca.jpg)

## Foster a beginner’s mindset (and hire more beginners)

Shopify is increasing both the actual number of beginners and changing the product-building process to focus more on prototyping (which is an act of actually putting yourself in a beginner’s mindset) — the real rate-limiting step to finding your way through problems.

### Tactic: Hire more entry-level people, not fewer

![](/images/posts/01942b1befa8.jpg)

Internally, this is the one place where Shopify has consciously diverged from the originally-written memo — instead adopting, “Show you can use AI more and then you’ll get more resources.”

Conventional wisdom says AI is destroying entry-level jobs; there’s an “impending doom” feeling around AI for engineering grads, as they feel there are fewer places for them to go post-graduation. But Shopify is hiring more interns because they’re the ones who are using AI in the most interesting ways and have a beginner’s mindset by nature.

After bringing in a group of 25 engineering interns with success, Lütke asked Thawar how big they could scale the program. “Without new infrastructure, I originally said we could support 75 interns. Then I took it back. Iupdated my answer to 1,000,” says Thawar.

[翻译失败，原文如下]

Thawar has run a lot of intern programs. He’s learned that interns bring energy, drive and intensity that pushes the whole team forward. But in this new, post-LLM world, they bring another skill: they’re AI centaurs. “They’re always interested in new tools and shortcuts. I want them to be lazy and use the latest tooling,” he says. “We saw this happen in mobile. I hired lots of interns back then because I knew they were mobile native.”

![](/images/posts/15ad2eac47aa.jpg)

### Tactic: Prototype more to find the best path forward

![](/images/posts/8c3af79ff147.jpg)

More prototypes are now part of Shopify's product-building process — specifically, increasing the ratio of prototyped attempts to build attempts. This enables one of Shopify’s principles, the “green path of product-building,” where the only way to figure out a problem is by trying many things. Lütke has told Thawar, “There are an infinite number of bad solutions and probably 10,000 good ones. Your job is to find the best solution among the 10,000.What you just showed me is thefirstone that worked vs. the best one. Why did you stop there?”

Thawar adds: “You’re facing 100 different variables and layers of a problem and you have to find different paths through, which might yield similar looking final products, but have very different tradeoffs.”

For example, Shopify’sinternal AI chat tooloriginated as a prototype, with Senior EngineerMatt Burnettexperimenting with open-source tools to improve internal access to LLMs. He iterated early versions through data loss and scalability issues, and exposed architectural flaws by getting it in the hands of teammates early. Eventually, it became so widely adopted that a dedicated engineering team now runs it.

#### Workflow: AI in performance reviews

As a way to measure different elements of engineering productivity across the org, Thawar uses an engineering activity dashboard — who’s pair programming, who’s doing interviews, and going back to a previous example, who’s using Copilot.

Shopify has years of data that shows pair programming increases the rate of learning. Using the engineering dashboard, Shopify did an analysis looking at time spent pair programming as it correlated to positive and negative performance reviews. They found that the more engineers pair programmed, the higher their impact was; the less engineers pair programmed, the lower their impact.

The dashboard now also measures who’s using AI tools like Cursor, Claude Code and the LLM proxy.Shopify ran an analysis that showed those who used AI tools had a positive correlation with impact.This helps identify the tools that are driving value, and how they correlate to performance reviews.

Shopify has incorporated questions about AI as part of the 360 review cycle, so managers and peers are asked to rate their colleagues on how “AI native” or “AI reflexive” they are. They expect to do another analysis on AI use correlated to impact after gathering a few years of data.

Thawar also uses pair programming as a way to model behavior, and now, uses it as a way to show people how he uses AI. “I paired with an engineer just to see how they were approaching a problem, but also to push my agenda. I have a tab open for ChatGPT and in practice, will show how I’m pairing with AI all the time.”

## The pursuit of discovering “process power”

If you were to analyze every single movement of how a professional sports team trains, or chefs working on the line at a Michelin starred restaurant, you’d notice they’re operating at something like 80% efficiency of motion. Now think about a business; at most, it’s operating at 20% efficiency.

“There’s an unbelievable amount of waste, just because you haven’t discovered the right patterns for how to do things,” says Thawar. “Anyone can see the value of AI speeding up processes. But the non-obvious value is you discover that your process should be done in a different order or should be done with different assumptions. And that’s when something clicks — maybe you can skip a huge amount of work or reorder the process.”

Think about the site audit tool. Thawar considers how it could change the entire sales process. “When site audits are trivially cheap to create, you might change who in the sales process is bringing those numbers to the forefront. Or you might change when it happens, like earlier in the sales funnel, because normally you’d only do it for really qualified leads. Then SDRs might be talking to different people,” he says. “It becomes a different sales process. But the only enabling change was being able to produce site audits trivially cheap.”

He gives the example of theToyota Production System. It’s revered, but notoriously difficult to replicate. AI might be changing that. “It fundamentally changes assumptions. You can attack the combinatorics of whatever your production line is, making it 1,000 times faster. That’s where the real magic is. The pursuit of discovering process power.”

---

> 本文由AI自动翻译，原文链接：[From Memo to Movement: Shopify’s Cultural Adoption of AI](https://review.firstround.com/shopify-ai/)
> 
> 翻译时间：2026-10-11 08:05
