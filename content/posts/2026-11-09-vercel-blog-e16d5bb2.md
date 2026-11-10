---
title: Decision models take 26% of requests; Anthropic now wins new teams 2:1
title_original: Decision models take 26% of requests; Anthropic now wins new teams
  2:1
date: '2026-11-09'
source: Vercel Blog
source_url: https://vercel.com/blog/ai-gateway-production-index-november-2026
author: ''
summary: '[翻译失败，原文如下]


  AI Gateway Production Index — November 2026


  Every month,AI Gatewayroutes more than 100 trillion tokens between production applications
  a...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-10T09:31:43.407409'
---

[翻译失败，原文如下]

AI Gateway Production Index — November 2026

Every month,AI Gatewayroutes more than 100 trillion tokens between production applications and AI labs. That traffic gives us a view of what AI usage looks like in today’s enterprise and startup landscape across language, decision, voice, image, and video models. We publish it here monthly. See the Production Index reports fromAugust,September, andOctober.

### Copy link to headingNovember 2026 Summary

- In six weeks, decision models grew toone in fourgateway requests, while accounting forhalf a centof every dollar spent.Close to a thirdof all paid teams used one in October. Among teams processing over 10 billion tokens a month,seven in tenused a decision model.
- About11%of paid teams used a voice model in October, up from4%in July.
- OpenAI and Anthropic now reach about thesame shareof paid teams, and new teams in October picked Anthropicnearly two to one. OpenAI’s share of gateway spend, meanwhile, is up bytwo-thirdssince December.
- More than halfof language-model requests went to models less than two months old, up from less than three in ten. Within one month of a typical model’s peak usage,three in fourof the teams using it have moved on.

In six weeks, decision models grew toone in fourgateway requests, while accounting forhalf a centof every dollar spent.Close to a thirdof all paid teams used one in October. Among teams processing over 10 billion tokens a month,seven in tenused a decision model.

About11%of paid teams used a voice model in October, up from4%in July.

OpenAI and Anthropic now reach about thesame shareof paid teams, and new teams in October picked Anthropicnearly two to one. OpenAI’s share of gateway spend, meanwhile, is up bytwo-thirdssince December.

More than halfof language-model requests went to models less than two months old, up from less than three in ten. Within one month of a typical model’s peak usage,three in fourof the teams using it have moved on.

## Copy link to headingDecision models account for 26% of all requests

Production AI is splitting into two jobs: generation and judgment. Until recently, when software needed to make a quick call, a team could use either a fixed rule that was cheap but rigid, or a language model that was smart but slow and expensive.

Decision models are now a third option. They classify, score, or pick between choices instead of generating text, and cost about a seventieth as much per request as a language model.

They arrived on AI Gateway in mid-September, and there are now 15 decision models available from eight different vendors. In October, nearly a third of paid teams on AI Gateway used a decision model. About 11% of paid teams used a decision model without sending a single request to a text-generating model.

Decision models cost far less per token and give very short answers, so even though they received about one in four gateway requests in October, they accounted for just 0.53% of total spend.

Almost all of that request volume went to Jev from TypeSafe AI, which alone received nearly four times Anthropic’s total requests. For every $1 teams spent on Jev, they spent $64 on Anthropic models.

Decision models are most common among the teams that run the most AI. Just over one in five teams running fewer than 10 million tokens used a decision model in October. At 100 million to 1 billion tokens, nearly half used one. Above 10 billion, seven in ten did.

This is partly because big teams use more of everything. The top 1% of teams by spend use a median of 29 different models, and the bottom tenth use only one. It’s also volume. The more requests a team sends, the more it has to gain from a model that makes simple decisions faster and far more cost-effectively.

## Copy link to headingVoice adoption is up 2.6x since July

About one in nine paid teams used a voice model in October, up from one in 24 in July, an increase of 161%.

New teams are using voice, and existing teams are adding it. Among teams that paid in both July and October, the share using voice went from 5% to 14%.

Teams that use voice are also using more of it. The share of teams sending at least 100 voice requests a month grew fivefold, and six in ten of September’s voice teams returned in October, up from fewer than half in July.

A spoken conversation with an AI app takes three steps:

- A voice model turns the user’s speech into text
- A language model writes the reply
- Another voice model reads the reply back to the user

A voice model turns the user’s speech into text

A language model writes the reply

Another voice model reads the reply back to the user

Most voice teams use just one or two of these pieces. Use of speech-to-text models has nearly tripled since July, and text-to-speech has more than tripled.

Some models do all three steps on their own. In July, about a quarter of voice teams used one of these all-in-one models, and one in six assembled the pieces themselves. By October, those numbers had swapped.

For most teams, voice is a new way for users to talk to an app or agent they already have. Teams’ preferred language models stay in the middle, and they can add voice at one end or both.

## Copy link to headingAnthropic wins new teams two to one, and OpenAI’s share of spend is up two-thirds

Last December, 70 of every 100 paid teams on AI Gateway used an OpenAI model and 48 used an Anthropic model. By October, the two labs were nearly level, with OpenAI at 55 and Anthropic at 54.

Both labs now reach more of the teams that have been on the gateway since December, but Anthropic’s reach grew more. The share of these teams using Anthropic rose from about half to two-thirds, while OpenAI’s rose from about three in four to four in five.

Most of Anthropic’s gain came from new teams. In October, it was the first-choice lab for nearly twice as many of them as OpenAI.

But among the biggest teams, both labs already have nearly everyone. More than nine in ten of the top 1% by spend use both Anthropic and OpenAI. With these teams, the labs now compete for how much of the work each one gets.

On that measure, Anthropic still leads, but OpenAI has gained ground. OpenAI now takes nearly 15 cents of every dollar spent on the gateway, up from about 9 in December, while Anthropic’s halved to about 32 cents over the same period.

## Copy link to headingMost AI traffic now runs on models less than two months old

Teams are moving to new models almost as fast as labs release them. More than half of October’s language-model requests went to models less than 60 days old. Before September, that share had never passed three in ten.

Within each model family, a new version arrives every 61 days at the median, and a typical model peaks within a month of launch. Four weeks later, three in four of the teams using it at its peak aren’t using it anymore, whether or not a successor has shipped in the family. Most of those teams are still on AI Gateway, using other models.

Teams switch models frequently, usually to something newer, and often to another lab. In October, about half of teams running at least 10 million tokens a month changed their most-used model. Four in five of those moved to a more recent release, and six in ten moved to a different lab.

Older models stay in use, often alongside a newer primary model. Seven in ten teams running at least 10 million tokens a month still used a model at least ten months old in October, but for the typical team it ran less than 3% of its tokens.

AI models now have a half-life of about six weeks. That means that, to the teams using them, labs are only as good as their latest model and have to re-earn their business with every new one.

## Copy link to headingAlso in October’s data

[翻译失败，原文如下]

- Opus 5.5 was the top model by spend in its first full month. It took about one in seven dollars across all teams. Four of the six most widely used models on AI Gateway are Anthropic’s: Sonnet 5.5 (reaching 26% of paid teams), Haiku 5.5 (22%), Haiku 4.5 (20%), and Opus 5.5 (18%). Jev (28%) and GPT-6 Luna (19%) are the other two.
- Image and video both had their biggest month yet on AI Gateway. More teams than ever are putting spend on them, and the largest teams are adopting them the fastest. About a third of the top 1% of teams by spend now use an image model, up from a quarter in July. One in six use a video model, up from one in ten.
- OpenAI’s newest image model, GPT-Image-2.5 Sunburst, took the lead in image spend in its first full month, followed by its Flare and GPT-Image-2 models. ByteDance’s Seedance 2.5 led video spend for a third month running, ahead of Google’s Veo 3.1 and Kuaishou’s Kling 3.0.

Opus 5.5 was the top model by spend in its first full month. It took about one in seven dollars across all teams. Four of the six most widely used models on AI Gateway are Anthropic’s: Sonnet 5.5 (reaching 26% of paid teams), Haiku 5.5 (22%), Haiku 4.5 (20%), and Opus 5.5 (18%). Jev (28%) and GPT-6 Luna (19%) are the other two.

Image and video both had their biggest month yet on AI Gateway. More teams than ever are putting spend on them, and the largest teams are adopting them the fastest. About a third of the top 1% of teams by spend now use an image model, up from a quarter in July. One in six use a video model, up from one in ten.

OpenAI’s newest image model, GPT-Image-2.5 Sunburst, took the lead in image spend in its first full month, followed by its Flare and GPT-Image-2 models. ByteDance’s Seedance 2.5 led video spend for a third month running, ahead of Google’s Veo 3.1 and Kuaishou’s Kling 3.0.

### Copy link to headingAbout this data

This report uses anonymized, aggregate traffic routed through Vercel AI Gateway through October 2026.

A few notes on measurement:

- Spend is estimated at published list prices; actual bills may differ.
- Paid teams are teams with at least one paid request in the month. Team size is measured by a team’s total tokens that month.
- Decision models are the models classified as decision models in the AI Gateway model list.
- Each model version is counted separately. A model’s age is measured from that version’s first day on AI Gateway, and gateway history begins October 20, 2025.
- Switching rates compare paid teams with at least 10 million tokens in both September and October. A team’s most-used model is measured by tokens.
- Voice figures begin June 22, 2026. Teams that “assembled the pieces” used speech-to-text, a language model, and text-to-speech on the same day.
- A new team’s first-choice lab is the lab it sent the most language-model requests to in its first month.
- All figures use the most recent data and protocol available; prior months may be revised as methodology is updated.

Spend is estimated at published list prices; actual bills may differ.

Paid teams are teams with at least one paid request in the month. Team size is measured by a team’s total tokens that month.

Decision models are the models classified as decision models in the AI Gateway model list.

Each model version is counted separately. A model’s age is measured from that version’s first day on AI Gateway, and gateway history begins October 20, 2025.

Switching rates compare paid teams with at least 10 million tokens in both September and October. A team’s most-used model is measured by tokens.

Voice figures begin June 22, 2026. Teams that “assembled the pieces” used speech-to-text, a language model, and text-to-speech on the same day.

A new team’s first-choice lab is the lab it sent the most language-model requests to in its first month.

All figures use the most recent data and protocol available; prior months may be revised as methodology is updated.

Read more about ourmethodology, andexplore or download the public data.

## Contributors

Eric Dodds

---

> 本文由AI自动翻译，原文链接：[Decision models take 26% of requests; Anthropic now wins new teams 2:1](https://vercel.com/blog/ai-gateway-production-index-november-2026)
> 
> 翻译时间：2026-11-10 09:31
