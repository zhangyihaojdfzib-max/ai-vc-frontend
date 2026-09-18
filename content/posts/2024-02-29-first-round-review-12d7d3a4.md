---
title: Evernote’s CTO on Your Biggest Security Worries From 3 to 300 Employees
title_original: Evernote’s CTO on Your Biggest Security Worries From 3 to 300 Employees
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/evernotes-cto-on-your-biggest-security-worries-from-three-employees-to-300/
author: ''
summary: '[翻译失败，原文如下]


  Dave Engbergknows a lot about security. Before he took the CTO spot atEvernote,
  he designed and developed credential validation systems f...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-18T06:55:50.606605'
---

[翻译失败，原文如下]

Dave Engbergknows a lot about security. Before he took the CTO spot atEvernote, he designed and developed credential validation systems for the U.S. government. If anyone in Silicon Valley knows the value of secure access and keeping information safe, it’s him.

Especially now, with publications like TechCrunch reporting breaches and attacks as soon as they happen, these types of events can crush a startup’s potential, especially if they are mishandled. Yet many companies don’t start thinking about building defenses until it’s way too late. After observing his fair share of incidents, and experiencing one firsthand earlier this year, Engberg wondered why there wasn’t a comprehensive guide for how startups should approach security at every stage — starting at the earliest.

With this in mind, he gave an exclusive talk at the recent First Round CTO Summit about security and the right way for growing startups to stay safe without needlessly expending valuable resources.

When it comes to security, size matters. A tiny startup has much different needs than a company likeSquareorDropbox.To right-size security strategy, Engberg refers to the rule of tripling. It’s a concept he got from Hiroshi Mikitani, CEO of Japanese e-commerce giantRakuten.

“Basically, he said whenever a company triples, from 3 to 10 or from 30 to 100, the entire tenor of the company changes,” Engberg explains. “As I look back, I really feel like that’s true from what I’ve experienced. How you think about your company at 30 is so different from 100 or 300. That’s how I think the approach to security should be broken down too.”

There’s one rule, however, that applies to all startups across the board:

As Engberg puts it, every startup is probably aware of some vulnerability they have — either minor or major — that is simply not worth fixing right now. “There are things we could optimize, but it ends up not being worth our engineers’time,” he says. “As a company grows, the number of security concerns worth that time grows too.”

1 to 3 Employees

“At this stage, you’re just trying to make things work,” Engberg says. “And from a security standpoint, you shouldn’t be doing very much.”

When you’re just starting out, you have very little time and money. It’s unclear whether you’ll get something off the ground and running at all. And in most cases, your eyes need to be fixed on funding and product functionality and that’s it. "In terms of security, the only thing you need to do is make sure you don’t do anything stupidly, horribly wrong."

That’s the worst case scenario. Luckily, it can be prevented with minimal vigilance. It’s important to keep eventual security needs in the back of your head — especially if you need to stretch seed funding into the next stage — but that’s it.

However, if you’re a CTO, this responsibility belongs to you. There’s no way your company can or should hire someone with the word “security” in their title at this point, so that person is you. No one else will have their eye on potential security concerns and how they will scale with your company. Use this time to bone up on what you’ll need to know.

4 to 10 employees

“Okay, now you’ve got a prototype out there, and definitely some seed funding to work with,” Engberg says. “This is when you’re going to need to make some core product decisions that will affect you down the line. You need to take a couple days to think about these things and get them right. If you choose wrong and have to retrofit or rip things out when you get to 60 people, it’s going to be a gigantic nightmare and you’ll hate yourself.”

All that said, this doesn’t call for major action specifically around security — just a few core product hygiene decisions that you'll need to make anyway.

“This includes something as simple as platform selection,” he says. “For example, how are you storing passwords? If you have users who are creating accounts, make sure to store their passwords or a representation of their passwords — something that can validate their password in a form that is secure because you don’t want to ask them for a replacement. Doing that has its costs.”

Engberg urges early startup teams to choose the tools and libraries that will do the right thing out of the box. One no-brainer is to use SSL for all network communications. As he puts it, “It’s 2013, for goodness sake, there’s no reason to use plain text anywhere for anything anymore.”

SQL is another a prime example.

“Don’t let anyone in your company concatenate strings together to make a SQL query,” he says. “There’s no reason to do that either. Use an abstraction library that will always ensure there are no injection possibilities, prepared statements, things like that.

“It’s the same thing if you’re using HTML — or whatever you chose to spit out pretty webpages — pick something so that the next engineer you hire won’t just naturally take a string out of the database and concatenate it with the HTML output stream.”

![Dave Engberg speaking at the 2013 CTO Summit.](/images/posts/200dac246594.jpg)

While there are no bullet-proof solutions — and there are sure to be some cross-site scripting vulnerabilities left behind — just choosing the right resources at the beginning makes life so much easier all the way through.

11 to 30 Employees

“At this point, you still have a direct relationship with everyone,” Engberg says. “And, assuming you’ve hired people who are sort of like you, you’re still rolling mostly on personal trust. You can say, ‘I know that guy — he’s not going to do anything stupid. I don’t have to babysit every single line of code.’”

Even though that’s the case past 10 employees, 11 is the marker where you should start revving up the engine for growth, and the requisite security. When you have that aha moment that “this might actually be a real thing,” you need to start taking real precautions. This is almost entirely about infrastructure.

"There are some really easy things you can do at this stage. Probably 80% of startup teams are using Google Apps for their employees’ email and calendaring. So setting up two-factor authentication for logins is just a matter ofturning on that setting as an administrator. So many people know that setting is there, that it can be enforced for all employees instantly, but they still don’t do it. There’s no excuse.

"If you have 30 employees, at least three of them are using the same password for their corporate email as they used for something that's already been compromised in the past."

Reusing passwords completely negates whether they are strong or weak. It makes it really easy for someone to take a list of stolen passwords and find a company to try them against. To nip this in the bud, Engberg advises using a password manager.

“LastPassand1Passwordhave good designs,” Engberg says of the service that generates strong, secure passwords. “But the real point is that your people shouldn’t be choosing their own passwords at this stage anymore. You should have a nice button that spits out a password that looks like gobble-dee-gook. It’s worth it to pay for it.”

On top of that, employees should stop sharing accounts. When you’re a scrappier operation, it might make sense for three people doing server administration to all connect via the same account. But by 30 employees, everyone should have identified accounts.

“It’ll make your life so much easier, especially when you’re big enough for people to start leaving the company,” Engberg says. “If you start doing it now, you won’t have to worry about it later.”

31 to 100 employees

“You’ve probably gotten to the next stage of funding,” Engberg says. “You’re thinking things are going to be super awesome.”

They can be, if you take action in advance. The best thing you can do is designate someone to be in charge of security. As a CTO, it might still be you. It’s not necessarily someone’s full-time job. But everyone in the company should know who to call when something goes wrong.

[翻译失败，原文如下]

“By this point, you should be tracking vulnerabilities in your various stacks. For example, if you’re using Apache, you need to get onSecunia’s list so you can keep your eyes on your version of Apache and what could happen.”

Secunia is a particularly valuable tool, keeping you up to date on potential attacks, vulnerabilities and the patches you can integrate to fend them off.

“Typically, if you’re a 25-person company, no one will care enough to attack you — which is a good defense for a while. But past this, you’ll have enough attention that people are going to at least casually try to troll you,” Engberg warns. “Keep track of low-hanging fruit software vulnerabilities.”

Here are some other considerations for mid-size startups:

- Invest more in internal IT so that you have people to work on problems if there is an attack or something breaks.
- All devices in your company should have encryption turned on.
- There should be decent password-locking screensavers on all computers. That way a smash-and-grab computer theft only amounts to a $1,500 asset loss, no critical data loss.
- Spend the time to ensure the hardware you’re giving people is patched and reasonable and secure.
- Continue using hosted cloud services to save the time you’d spend running an internal server. These services probably have better security professionals anyway.
- You should have a strong audit trail in your source repository so you can go back through and tell who did everything and track back through time.

100 Employees

Now you’ve hit the hyper-growth stage, and things get serious. If you didn’t put in the necessary time and effort earlier on, this is where it'll come back to bite you. For example, if you haven’t already, you should move everything behind a VPN to ensure that all employees are going through two-factor authentication.

But the key change here:You should build in some way for external people to report security vulnerabilities to you. Whether you have a form on your website, or create an email address like[email protected], the mechanism doesn’t really matter.

“Particularly, if you’re working at a consumer-facing brand like Evernote, people will report things to you. People come out of the woodwork. We get notes from researchers in Japan who happily identify cross-site scripting vulnerabilities. We’ll go in and fix them and say thanks. Then they’ll send another one two minutes later.”

Opening a communication channel with people who want to help can be an incredibly cheap, easy solution to a lot of security woes. The important thing is to acknowledge their contributions. If you give them a public nod, they’ll keep hunting down problems, and the cost-to-benefit ratio is low.

At the same time, you should contract someone outside the company to run vulnerability analysis and intentionally try to breach your system. One of the best services out there isiSEC Partners.

“Yes, this is kind of expensive,” Engberg admits. “When you see the hourly rates these folks are making to run scripts against your servers, you’ll think, ‘God, I could do that.’ But you can’t. You don’t have time. So pay the $20 or $30K. You’ll get a bunch of valuable results.”

This will free up your time to focus on everything else you need to be doing — product prioritization, team management, and setting the groundwork for an internal security hire.

Evernote has been on the lookout for a good one for a while, but this isn’t just another hire. To avoid rushing it, a company’s best bet is to work with a firm likeiSEC. But this is only a stop-gap.

“You want someone who’s technical enough that they’re not just shuffling paperwork. And you want someone who’s actually been in the industry who wouldn’t rather be billing $300 an hour doing independent security analysis. At 100 people, you need to start looking. Go through the usual channels. Talk to people. This is something that takes a long time, so you want to get in front of it.”

300 Employees and Beyond

“Now, ideally, you’ve got that person with the word security in their title telling you what to do next — and not someone like me,” Engberg jokes. “But there are a few more low-hanging fruit items you can focus on.”

These items include device management, getting software onto every computer so you can quickly detect malware, tapping into DNS to see if there’s malware on your laptops. Malware typically needs to “phone home” to something, and that will typically trigger a DNS look-up.

At an even earlier stage, Evernote used to install FileVault on all of the MacBooks it handed out to employees to encrypt the contents of their drives. Before they had device management, employees would need to actively turn this off, but few would.

Today, he recommends theCasper Suite from JAMFas the best platform for managing Mac devices.

“That sort of thing lets you know which of your employees has FileVault turned on and even enforce it. It helps you enact and maintain policies better. There’s an equivalent for Windows too,” Engberg says. “I know there are more technical ways of doing it, but getting a massive AD infrastructure in place just to lock down everyone’s computers is a little unrealistic. Why not just hand them something that’s set up properly at the beginning and give them five minutes of training?”

All of these safeguards will keep your machines clean to an extent.

But the best part about having a security chief on board is that they’ll take over training and making everyone aware of the risks. This is absolutely critical at a company big enough to employ one to two bad actors, or the simply negligent.

“We just had our very first targeted spear-phishing attack training for executives,” Engberg says. “It looked like our CEO sent out an email saying ‘Hey, read this article on the BBC.’ If you clicked on it, it went to a reproduction of our Google apps login page with our logo and everything. The goal was to get the person to enter their Google Apps credentials. It was a simulation, but that’s the sort of thing that’s really hard to prevent from a purely technical standpoint. That’s why you’ve got to start increasing awareness.”

When you’ve grown to this size, people start to trump technology as your biggest concern, both inside and outside the company.

On one hand, you don’t want to take up too much of their time or bandwidth with security concerns, but on the other, you always have to be thinking ahead.

As Engberg sees it, “You’ve got all these people who are getting paid and eating and paying rent in the Bay Area, and you assume their obligation is to make the company succeed so they can keep getting paid, but ultimately you always need to be avoiding that catastrophic thing down the road.”

And if, at any point, you wonder why you’re investing all of this time and money in security efforts, Engberg says look no further than your users. A solid security strategy starts with a thorough, even emotional understanding of what you need to protect.

“At Evernote, we’re driven by user data,”he says. “I’m not worried about you stealing our super secret source code. I don’t want you looking at it, of course, but if you do get a copy of our entire Android application and use it to become the Evernote of pet management or something, I don’t care. I care about the integrity of our user data. This might be different, depending on your business, but you should always have a mental model of what is important to you.”

---

> 本文由AI自动翻译，原文链接：[Evernote’s CTO on Your Biggest Security Worries From 3 to 300 Employees](https://review.firstround.com/evernotes-cto-on-your-biggest-security-worries-from-three-employees-to-300/)
> 
> 翻译时间：2026-09-18 06:55
