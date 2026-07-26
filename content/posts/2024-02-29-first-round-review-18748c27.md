---
title: The Right Way to Ship Software
title_original: The Right Way to Ship Software
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/the-right-way-to-ship-software/
author: ''
summary: '[翻译失败，原文如下]


  This article is byJocelyn Goldfein, angel investor and former engineering executive
  at Facebook and VMware. She’s well known for helping ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-07-26T05:25:57.377858'
---

[翻译失败，原文如下]

This article is byJocelyn Goldfein, angel investor and former engineering executive at Facebook and VMware. She’s well known for helping engineering teams scale their operations through periods of hyper-growth. At First Round’s last CTO Summit, she shared her experiences shipping software in different environments, and offered startups advice on how to structure their own release process.

I’ve been around the block and shipped a lot of software. I’ve worked at tech companies ranging from three to 10,000+ employees. I’ve built software that’s been given away for free and sold for $50M license fees — and just about every price point in between. Every one of these products was developed and delivered differently, and after having the chance to compare and contrast them all, I’d love to reveal the one true way to ship software.

I’m abashed to confess that I cannot.

I’ve discovered and rediscovered the “right” way to build and ship software many times. I’ve found near-religious zeal for certain practices (say, precise coding estimates, thoroughly detailed specs or UI design via A/B test) only to find the magic gone when I tried to apply it to some other product.

In a profession where we carry out decade-spanning holy wars over tab widths and capitalization, it’s no surprise that people get attached to their development and release habits. But if shipping so much software has taught me one thing, it’s to be an agnostic. Different methodologies optimize for different goals, and all of them have downsides. If you maximize for schedule predictability, you’ll lose on engineer productivity (as this turns out to be a classic time/space tradeoff). Even when you aren’t dealing with textbook tradeoffs, all investments of effort trade against something else you could be spending the time on, whether it’s building an automated test suite or triaging bugs.

Consider two of my past lives:

- When it was a startup, VMware needed to offer predictable dates and high reliability because they had to convince conservative enterprises to buy operating systems from an upstart new vendor. (At the time, virtualization sounded like science fiction!)
- In Facebook’s startup days, they needed to move quickly because first-mover advantage meant everything for a product based on network effects.

One of them put a ton of engineering emphasis on predictability and reliability; the other put its effort toward driving user engagement. Not hard to guess which was which. As you might imagine, the development practices at these two companies could not have been more different. Neither one was right or wrong — they both made appropriate tradeoffs for what they wanted to accomplish, and each company’s practices would have been ineffective or disastrous if applied to the other company’s products.

## First, Take a Look at Who the Customer Is

To determine “the right way to develop software,” you’ve got to understand what matters for your product and how to optimize for that. This isn’t based on personal preference. Ultimately it stems from your company’s mission, and the way you make money is a reasonable proxy for that.

Chances are, if you sell software at a high price tag, you are selling to businesses that are buying your software based on theirneed. The more expensive your software is, the more mission critical it is for your customers, the more likely you have to optimize for reliability, functionality and a predictable schedule. You might think business customers would like your software as soon as possible, but because they have a lot of dependencies — deployment, training, integration — it is generally much more important to them that you bepredictablethan you befast.Larger deal sizes also go hand in hand with fewer customers, meaning that each customer has comparatively more power over you and satisfying their needs is more crucial to your startup’s survival.

Many of the most traditional, old school software process methods are aimed at ensuring schedule predictability: careful specification of features and estimation of tasks, dependency analysis and long soak times. More modern techniques like continuous integration, comprehensive unit testing and beta testing can also help surface technical risks earlier. In my seven years at VMware, all our effort rested on a three-legged stool, whose legs were: schedule, features and quality. All of them had to be served, which came at a high price in engineering effort and developer productivity at times seemed mysteriously low. We dabbled with new techniques that boasted faster cycle times, but they came with a tradeoff: a lack of foresight. That just wasn’t acceptable to our customers.

Well, what if your customers aren’t demanding enterprises? As you charge less and less (from millions to thousands, to hundreds, to freemium and free), your market goes higher volume and involves smaller businesses or consumers. For these products, schedules can be less important since people will generally accept your latest enhancements whenever they materialize. The influence of a single customer is small, so you might deprioritize a niche platform or bugs that affect only a few people.

However, you can’t just decide quality is no longer a priority because you charge less. If your product is inexpensive or free, people probably use it because theywant to,not because theyhave to. Historically user experience (UX) has been much more important in consumer than enterprise products. Enterprise vendors are catching on to the value of great UX, but there’s a reason they describe excellence as “consumer grade UI.” You will find different practices that work to ensure UX quality, including empowerment of the design team, prototyping and iteration before committing to dates, close collaboration between design and engineering and user testing.

Stage matters here, too. If you are growing quickly, trading off quality might be acceptable if 80% of your users one year from now will be new and won’t remember your mistakes. On the other hand, if repeat business (aka recurring revenue) is your game, you’d better make sure current customers are delighted.

## Next, Assess How You Deploy and How Much You’re Willing to Risk

There is another, equally fundamental difference between tech companies that affect your release tradeoffs, and that is your deployment model. Deploying in the cloud means you have total control over the runtime environment of your software. It means you don’t have to have the words “test matrix” in your vocabulary, which exponentially reduces testing time and volume of bugs to fix. You can update whenever you like; distribution is instantaneous and universal (and doesn’t require effort from users.) Code that you delete actually goes away. You don’t have to worry about fixing bugs in code that you abandoned two releases ago because a user has not moved on. Deploying onto a customer’s device (which includes everything from native mobile apps to operating systems) means the once and future cost of doing a release is radically higher.

You want reliability? Instead of weeks of lab-based stress testing, just ship to production and gradually turn up the load. Turn it down and fix the problem when you run into bottlenecks.

You want efficient testing? Well, you can probably catch 80% of the bugs with 20% of the testing, then quickly spot and fix the few that escape.

You want design quality? Expose yourself to quick feedback loops by putting prototypes in production for a small number of users and see how it works.

[翻译失败，原文如下]

Of course, you don’t have the freedom to choose to deploy in the cloud just because it makes life easier for you. Some products (operating systems or video game consoles) simply can’t exist entirely in the cloud. If you build for consumers on mobile, you’ll probably choose a native app so you can deliver the best UX, because at least in consumer, rich UX trumps engineering productivity. I know it sounds preposterous, but be prepared for shipping mobile apps to have more in common with shipping operating systems than with shipping for the web. That’s why even if you are mobile first, you want all of the brains of your mobile apps to live on the server where you can easily change them.

Facebook’s struggle pivoting to mobile illustrates the potential for trouble. Facebook’s speedy, individualistic and iterative way of designing and shipping software was deeply embedded in product team culture. If you worked in the web tier, the cost of releasing was pretty close to zero and literally everything else about the way you worked was optimized to take advantage of that assumption. As the company’s focus shifted to native mobile apps, the engineers hired for their mobile expertise insisted on a heretofore unknown process like feature and UI freeze, functional specs and QA.

Learning new programming languages and frameworks wasn’t what made it hard for Facebook engineers to pivot to mobile. It was hard because they had to undo all their assumptions about how to make software. I’d like to tell you there was a cool-headed analysis of the merits of various practices given the constraints of native app development and what would be best for Facebook’s user community. What actually happened more closely resembled a discussion of religion or politics over the Thanksgiving dinner table. We were all family but violently disagreed in fundamental ways.

At the heart of that debate were different assumptions about tolerance for risk. Appetite for risk was baked into Facebook’s culture — after all, this company brought you the slogan “Move Fast and Break Things!” Longtime Facebook engineers viewed embracing risk as an essential cultural trait — and at the time, did not realize that mode of operating relied on assumptions about the universe that were true for the web but not for mobile.

As a rule, startups should be aggressive risk takers, for entirely rational reasons. When you have no customers, revenue or brand, the impact of a mistake is immaterial. You had nothing before, you have nothing afterwards. So who cares? But once you have customers, you have to define the cost of a mistake in terms of the pain you cause. Similar kinds of operational mistakes might cause a 5% decline in growth rate for one startup and a 75% decline for another, based on different business and deployment models. If that’s the case, those founders had better be running those companies differently.

In Twitter’s early years, service outages were so common, users coined the term “fail whale” (inspired by the graphic on Twitter’s outage page) as a shorthand for “yet another outage.” The fail whale was ultimately not fatal in Twitter’s business because users patiently gave them a long time to fix it. Yes, we cracked a lot of jokes, but we didn’t leave the service. Imagine if instead a company like Salesforce had a “fail whale” problem. If their customers suffered frequent outages in which they couldn’t book revenue or make sales calls, it could've been game over. Customers would have reverted back to on-premise CRM. When enterprises rely on your software for mission-critical operations, your mistakes can cause them very great pain. So a consumer business can afford a lot more risk than an enterprise software business.

Deployment model affects risk, too. When customers experience problems, the speed with which you fix your mistakes can be as important as how bad the mistake was in the first place. When you can push a hotfix to your server and instantaneously solve the problem for every user, you have an order of magnitude faster remediation than if your release process involves a two-week QA window and an App Store review process for the smallest code change, after which customers install the patch at their own convenience. Twitter as a web-based product was lucky enough to be able to fix their outage problems server-side. Imagine bugs that caused intermittent outages in a client-based consumer product, such as your Apple iPhone, with no solution in sight other than the next phone edition. That buggy phone gets consigned to the junk heap of history.

To crystalize how deployment and risk compound: if you happen to sell on-premise system software to enterprises for lots of money, you have magnitude-of-pain and lengthy time-to-update both working against you. You can count on the same kind of mistake costing you two orders of magnitude more than if you provide a free web-based service to consumers.

It’s probably obvious to the world that VMware is substantially more risk averse than Facebook. Realize that it is not because Diane Greene and Mark Zuckerberg have different personalities, nor because one of them is right and one of them is wrong. They are different businesses with different technology stacks and they appropriately ship software in completely different ways based on how much risk their customers can absorb.

![](/images/posts/c781a958a96e.jpg)

## How You Ship is One Strand of Your Cultural DNA

Now that you’ve inventoried your business model, deployment model and appetite for risk, you’ve got a good framework for analyzing the release processes you’re using. If you’ve survived long enough to achieve product-market fit and some customer traction, chances are you’ve naturally adapted towards practices that make sense. In startups, as in nature, form follows function. You might surprise yourself and find out that you’ve been wasting energy on goals that don’t matter (like schedule predictability for a consumer business)!

Apart from analyzing your current methodology based on this framework, you can also use it as a filter on whose advice to take, which company’s practices to imitate or even which leaders to hire.

You may find this framework particularly helpful if you struggle with multiple technologies or business models. A startup may very well need to support both web AND native mobile apps, or more than one set of customers (say, a two-sided marketplace with different apps for consumers and businesses). In an ideal world, your release process would just vary to match the product under development. But how you ship is not just process, it’s culture and identity. Swapping out a process is easy. Changing culture is hard. And it’s even harder for a small company to embrace different cultures for different teams.

If you find multiple “shipping cultures” in tension in your company, you’re dealing with one of the fundamentally hard execution challenges of building and shipping software. There are no easy answers when people stake out positions grounded on emotions rather than reason. On the plus side: your team’s emotions are engaged! It can be hard to remember that silver lining when the conflict is raging, but it is good news that your engineers care passionately about your company.

Take a deep breath and remind them that release processes come and go, but your company’s mission and values are immutable. Your team hopefully can agree that what ultimately matters is to ship the best product for your users, and that what remains is negotiable. With any luck, this framework will help you negotiate it.

---

> 本文由AI自动翻译，原文链接：[The Right Way to Ship Software](https://review.firstround.com/the-right-way-to-ship-software/)
> 
> 翻译时间：2026-07-26 05:25
