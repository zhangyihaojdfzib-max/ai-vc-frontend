---
title: The Inside Story on How SurveyMonkey Cracked the International Market
title_original: The Inside Story on How SurveyMonkey Cracked the International Market
date: '2024-02-29'
source: First Round Review
source_url: https://review.firstround.com/the-inside-story-on-how-surveymonkey-cracked-the-international-market/
author: ''
summary: '[翻译失败，原文如下]


  WhenSelina TobaccowalajoinedSurveyMonkey, 85% of its business was done in English.
  It was solidly a domestic company making slow inroads ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-07-26T05:25:54.068509'
---

[翻译失败，原文如下]

WhenSelina TobaccowalajoinedSurveyMonkey, 85% of its business was done in English. It was solidly a domestic company making slow inroads overseas. A little over five years later, they are supporting 17 different languages and 28 currencies. Currently, the domestic market is 55% of their business, but they're aiming for it to be just 25% of their business.

Internationalizing is a huge strategic goal for them — full of hard-won lessons for CTO Tobaccowala and the technical organization she runs.

A lot of earlier-stage startups might think, “It's way too early for us to be talking about this.” But they're wrong.

“The biggest piece of advice I can offer is that if you start thinking about this upfront, the investment you'll have to make is fairly minimal,” says Tobaccowala. “On the other hand, if you have to retrofit your application years later, it can be very difficult — and I have nine years of experience doing exactly that before landing at SurveyMonkey. It was pretty painful.”

The opportunity cost of not internationalizing is stark — but only recently became apparent (according to Mary Meeker's 2014 Internet Trends Report):

- At the start of 2013,nine out of the top 10internet properties in the world were based in the U.S. (think Google, Facebook, etc.), but 79% of their users were international.
- A year later, only6 of the top 10were in the U.S. and86%of their users were not.
- The trend in mobile is even more staggering.188 million smart phone users are in the U.S.but the growth rate is only 12% year over year.
- Internationally, there are1.6 billion smart phone usersand the growth rate is 24% year over year.

In order for U.S.-based companies to establish and maintain their leadership, theyhaveto think international. It's worth the engineering resources. “As Albert Einstein said, 'A clever person solves a problem. A wise person avoids it,'” Tobaccowala quotes. In this case, the wise thing to do is avoid the quagmire of delayed internationalization.

At First Round's Recent CTO Summit, Tobaccowala drew on her experiences at SurveyMonkey andTicketmasterbefore that, to share the non-obvious steps startups should take to achieve a strong global presence.

## DESIGN & MARKETING

“No matter who you are, or whether you have a commerce app or a content app, you definitely have sites where you're trying to sell people on your product or your company. The sites have to be different for every market.”

Japanese homepages are consistently filled with dense images and content. That’s a stark contrast to U.S. websites, which typically have a clean design. The difference in aesthetics can change the way people perceive your brand.

Along similar lines, one of SurveyMonkey's selling points for recruitment in the U.S. is that employees love working there. When they tested this language in Russia, it didn't have the same resonance.

“To create a flexible marketing site, you have to think about the content management system you're using,” says Tobaccowala. “You need to pick something that will let you display different content to different markets. It's not just about translation, but truly different content for each market.” Given how much work it takes, you don't want to switch content systems later in the game, even if you're not going global right now.

You also want to make sure you can lock down the ideal domain taxonomy for your site. Buying a domain within the country you're working in is critical to good SEO rankings. For example,SurveyMonkey.deorSurveyMonkey.co.ukare way more searchable than any funky alternatives.The lesson:If you think there's ever a chance you'll expand to new territory, stake your claim as soon as you know, or buying domains back can get pricey.

When it comes to your core application, however, the critical thing is knowing where people do things similarly across borders. At Ticketmaster, Tobaccowala saw that the way people searched and browsed for content was fairly uniform in different markets. At SurveyMonkey, they were able to prove that the way people create surveys and understand their data is nearly the same no matter where they are located. Wherever you see these types of similarities, direct translation will work for you, but there are still some things to consider.

This means you need to pull in your design team as well. “Work with your front-end engineers to establish the fact that right up front, you’ll need to leave one and a half times on average the space in your UI, because building that in later is going to be a pain.” Generally speaking — aside from these tweaks — your core application can be very consistent between countries.

And don't forget about encoding. It's also very simple if you take care of this at the start. But if you try to do it later through your whole app, especially if you're like SurveyMonkey with a bunch of form inputs, it gets nontrivial fast. You can save yourself a ton of design and technical debt if you focus on just these few simple areas that change between markets.

![](/images/posts/1f9478167f21.jpg)

## PAYMENTS & PRICING

Payments and pricing are vastly different around the world. You have to do a lot of customization as you start thinking about conversion rates and international conversion funnels.

“Did you know that every person in the Netherlands walks around with a little calculator in their pocket? Every time they go to make an online payment, they type it into this calculator and they get a unique, secure code from their bank to use with the payment.It's totally normal for Dutch people to do this, and actually 60% of people on the planet do this every time they make an online transaction,” Tobaccowalasays.

As another example, Germans rarely pay with credit. It's a holdover from the history around World War II when a lot of financial systems went bust, but it still impacts how people buy things today. They prefer to pay via bank transfer. In France, the more common card type is something called Carte Bleu, which most Americans have never heard of. The big question for companies is how they're going to support all these different methods.

“Regardless of the payment service providers you use today, you're going to have to use a different one for other countries,” says Tobaccowala. “This sounds easy enough, but it requires abstracting payments in your app so you can connect to a different PSP later. If you think about it early enough, you can create the abstract layer and avoid rebuilding your entire checkout system.” This will make launching in new countries significantly easier.

Pricing also varies wildly.In the U.S., a copy of The Hunger Games on Amazon costs about $12.50. On Amazon's U.K. site, they're charging over 15 pounds for the same book — the equivalent of $25.

“Why?” Tobaccowala asks. “I don't know why. It could be because the market will bear the higher price. It could be because they have to pay a content guild or the author differently. When you're building and selling an app, your system needs to be able to support a host of different prices and skews for reasons you can't even think of now.”

At SurveyMonkey, the team has done a massive amount of A/B testing in this area. The company has 150 different variations of its pricing page to support various languages, currencies and product packages. “The conversion rates and how you talk to your customers, and the packages you can sell will change by market.”

![](/images/posts/902eee6787ca.png)

[翻译失败，原文如下]

There are a couple challenges to know about when you do. When you do A/B testing, you'll probably discover that your international sample is smaller than your domestic sample. Part of that is because, individually, each of these countries — except for a few like China and India — are, in fact, much smaller than the U.S. On top of that, most A/B testing platforms are cookie-based. This is a problem internationally where more people access websites from multiple devices. This means many of them will see multiple versions of your pricing page — which could send harmful mixed messages.

To tackle these challenges, SurveyMonkey is making a big change: it designed its A/B testing so that pricing and packages would always be the same for the same users — it’s persistent on the user level instead of the cookie level. This is something you should absolutely consider doing if you're going to invest in building price experiments anyway.

You also can't think about international pricing without facing foreign exchange head on. “If your business has any variable costs, then you need to think about currency before it's too late,” Tobaccowala says.

![](/images/posts/0a9d36914ce5.png)

“The Euro here is at an all-time low. So even companies like Apple had to raise its prices in Euros — both because of tax changes and because of the falling currency,” she says. “So when you think about your payment systems, you may not just need to change prices on new users but on existing users too. You have to invest a lot in abstracting this stuff out and making sure you're flexible enough to make granular changes to all of these things. It's extremely important.”

## STORING YOUR DATA

“Unfortunately — especially if you're running an enterprise business — international customers are extremely wary of the NSA and the Patriot Act,” says Tobaccowala. “It has hurt U.S. businesses, especially internet companies. It's a big thing that comes up in sales. Even when I was at Ticketmaster, I would get the same concerns over and over: 'How are you storing my data? Where are you storing my data?'”

There are a couple different models you can follow here to assuage fears:

1.You can keep local data local.You can contain things if you do localized business in one country or another. Take Ticketmaster or Amazon for example. If, for example, you log intoTicketmaster.co.ukor Amazon.co.uk, that is a separate account from if you logged intoTicketmaster.comandAmazon.comas a user. Your data is totally segregated. This solution works if you're building a local commerce company. But most aren't.

2.Keep one customer profile,anonymizedacross borders.When people are conducting business across borders you can separate users from their personally identifiable data so that they are effectively anonymized. More importantly, you have to make sure you have a data storage plan that allows for rapid and massive scale of this solution. And always ensure the data is stored safely and securely regardless of where it is stored.

Whichever route you go down, you have to be vocal about how you're storing things. People don't mess around with their personal information, and trust in companies is fragile. Building a security and storage plan for a global market is therefore not just about a flexible, elastic system, but about scaling your communication about that system as well.

## WINNING AT MOBILE

All of this is especially critical as more and more services and sites are accessed from mobile devices — particularly outside the U.S.

Higher mobile use also means a higher Android share internationally — in fact, it's dramatically higher: 52% in the U.S. versus 84% worldwide. This makes the question of whether early-stage companies should focus more on iOS or Android development pretty thorny. Most of them can't do both. Or if they can, they can't stay up to date and maintain quality across both all the time.

Tobaccowala's take on this question is nuanced.

“If you look at Android, you have about 2X the amount of app downloads on that platform — especially if you look at things like messaging apps, you get a lot more penetration if you go with Android first because the raw user base is broader,” she says. “But if you're a subscription based business and you're trying to do commerce, iOS still has 2X the transactions going through it. You have to prioritize based on your business model.”

Knowing that you will eventually need to go international will inevitably help define your mobile strategy. You'll have to create a plan that includes Android development. But, on the upside, you'll have time to consider technologies likeReact Native, or others that allow you run parallel development cycles quicker and easier. “Android is a key part of any international strategy. Non-optional.”

This sounds like a lot to start thinking about at an early stage — but it doesn't have to be daunting, Tobaccowala says. “All it really takes is sitting down with your team for one hour and saying, 'Okay, if we want to go international in a year, two years or three years from now, it's going to require these things.'” Just make a simple list of all the things that fit into the buckets above, tailored to your model: design and marketing, payments and pricing, data storage and mobile. Then build them into your plan going forward.

“To become a worldwide business — one of those top ten internet companies in the world, you have to constantly be thinking one thing: What can we do now to make sure that things are much easier once we get there?”

---

> 本文由AI自动翻译，原文链接：[The Inside Story on How SurveyMonkey Cracked the International Market](https://review.firstround.com/the-inside-story-on-how-surveymonkey-cracked-the-international-market/)
> 
> 翻译时间：2026-07-26 05:25
