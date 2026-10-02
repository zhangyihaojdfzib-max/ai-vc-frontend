---
title: 'One year later: Sovereign AI and the fight for choice'
title_original: 'One year later: Sovereign AI and the fight for choice'
date: '2026-10-01'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/sovereign-ai-choice-one-year-later/
author: ''
summary: '[翻译失败，原文如下]


  It''s Birthday Week, when we traditionally ship presents to the Internet. This year,
  two of them come from Europe: EuroLLM, which covers a...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-02T08:10:39.153290'
---

[翻译失败，原文如下]

It's Birthday Week, when we traditionally ship presents to the Internet. This year, two of them come from Europe: EuroLLM, which covers all 24 official EU languages, and Apertus, Switzerland's fully open model, trained on more than 1,500 languages. Both were built by public universities and research institutions. Both are coming to Workers AI, and you can request accessÂ today.

We're also launching hands-on workshops that help government cyber agencies and critical infrastructure operators build AI defenses that work with any model. The first runs in Singapore in October.

Today's announcements follow from an argument we madea year ago, when questions about AI access and sovereignty were swirling in national capitals. Our answer was choice: the freedom to pick the right tools for the job, and to switch when you need to.

Since then, those conversations have hardened. Attackers have used frontier models to run cyber attacks. Access to some frontier models now depends on where you are. Calls to restrict open models are getting louder. Put it all together and it's easy to conclude that AI sovereignty is zero-sum: every model another country controls is one you can't count on, so the safe move is to build walls.

We think the past year can point the other way. India, Japan and Singapore focused on open-sourced models, and people across Asia-Pacific built tools on them for rural citizens, elderly patients and the nurses who care for them. Our own security team built AI defenses that work with any model, so losing access to one doesn't mean losing your defenses.

Helping build a better Internet has always meant more options, not fewer. That's why we work on open standards that preventvendor lock-in, why so much of what we build is free to start with, and why ournetworkÂ runs in more than 335 cities across 125+ countries, with GPUs for AI inference in more than 230 of them. We don't think any country should have to depend on one company for its AI. That includes us.

## Two European open models on Workers AI

In February, Matthew Prince told the India AI Impact Summit 2026 in New Delhi that decentralized, affordable access to AI is a matter of national resilience. The models from India, Japan and Singapore we'd added a few months earlier were our first proof. The summit series moves toGenevaÂ in June 2027, with a mission of "prosperity and progress for all."

EuroLLMÂ supports 35 languages, including all 24 official EU languages, many of which are underserved by existing open models. It was developed with support from Horizon Europe, the European Research Council and EuroHPC by a consortium that includes Instituto Superior TÃ©cnico, the University of Edinburgh, Instituto de TelecomunicaÃ§Ãµes, UniversitÃ© Paris-Saclay, Unbabel, Sorbonne University, Naver Labs and the University of Amsterdam. It was trained on the MareNostrum 5 supercomputer and, according to the consortium, outperforms similar-sized models on EU multilingual benchmarks and machine translation.

You can request access to EuroLLM on Workers AIhere.

ApertusÂ (Latin for "open") is Switzerland's first large-scale, fully open, multilingual language model. It was trained on more than 15 trillion tokens across more than 1,500 languages, with 40% of training data in languages other than English. It was developed by ETH Zurich, EPFL and the Swiss National Supercomputing Centre (CSCS) as part of theSwiss AI Initiative: built by public institutions, for the public good. Its architecture, weights, training data and methods are all published. It was designed with Swiss and European rules such as the EU AI Act and GDPR in mind, which means respecting training opt-outs, removing personal data and preventing memorization. It was trained on CSCS's Alps supercomputer (more than 10,000 GH200 GPUs), and its developers report that it significantly outperforms leading closed and open models on rare and regional languages, from Romansh and Swiss German to low-resource languages across Asia and Africa.

You can request access to Apertus on Workers AIhere.

## What people built last year

Last year's national models didn't sit on a shelf. Since we added them to Workers AI, hundreds of students, startups, small businesses and public servants across Asia-Pacific have built on them, many at buildathons we ran with local partners. Three of them:

- Government forms, no reading required âForm MitraÂ (India): Benefit forms written in dense English shut out many of the rural, low-literacy and visually impaired citizens they're meant for. Students at the Indian Institute of Technology Delhi built Form Mitra at a buildathon we ran withCyberPeace: a voice-guided assistant that walks people through the form in any of 22 Indian languages, usingAI4Bharat's IndicTrans2Â model.
- Care in the patient's own dialect âMedBridgeÂ (Singapore): Many of the nurses caring for Singapore's elderly patients come from across Southeast Asia and don't speak the local dialects, so critical clinical information can get lost in translation. MedBridge guides patients through health conversations in 14 languages, including Hokkien and Cantonese.
- The right public service, in one tap â Anshin Concierge (Japan): For elderly residents, people with disabilities and anyone less comfortable with digital tools, working out which public service to call in a moment of need can be overwhelming.Â Built as a hackathon prototype, Anshin Concierge lets people describe the problem in their own words ("my knees hurt", "a strange screen appeared on my phone") and connects them to the right Tokyo Metropolitan Government support desk, by phone or web page, in one tap.Â

## AI defenses that don't depend on one model

Governments want to use AI to defend essential services and national infrastructure. The frontier models that can find vulnerabilities at scale can find them fordefendersÂ too. But a defense built on one model is only as dependable as your access to that model, and governments have watched access to critical models get constrained with little warning.

We had the same problem, and in security we are always our own first customer. Over the past year, our Security team, working with teams across the company, set out to build AI defenses that don't depend on any one model. We built a harness: an orchestration layer that coordinates multiple AI models working in parallel to hunt for vulnerabilities, verify findings and prioritize threats. Wepublished what we learnedÂ about using frontier and open models together,open-sourced the harnessÂ so any organization can run it with the models of its choice, and laid out thelayered architectureÂ we use to stop attackers armed with frontier models from finding vulnerabilities in the first place.

Because the harness works with any model, closed or open, losing access to one provider doesn't switch your defenses off. When we walked governments through it, the most common reaction was relief. Then came the practical questions: how to stand it up in their own environments, under their own rules. Briefings quickly turned into requests for hands-on training.

So today we're launching a program of hands-on workshops for government cybersecurity agencies and critical infrastructure operators. Participants build their own AI security harness and layered defenses, and leave knowing how to adapt both to their organization. The modules are plug-and-play, designed to slot into national AI skilling and cyber resilience programs. The first workshop runs in Singapore this October, at Singapore International Cyber Week.

## Come build with us

None of this happened alone. Partners likeCyberPeaceÂ in India andCode for JapanÂ helped turn open models into working tools. If you run a national AI program, a cyber agency or critical infrastructure, and you'd like more options than you have today, write to us at policy-team@cloudflare.com. Request accessÂ to EuroLLM and Apertus, or start with theharness.

[翻译失败，原文如下]

A year ago, we said choice is the path to AI sovereignty. This year showed it's the path to AI security, too.

## Related tags

Follow on Social Media

- Cloudflare
- Petra Arts

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[One year later: Sovereign AI and the fight for choice](https://blog.cloudflare.com/sovereign-ai-choice-one-year-later/)
> 
> 翻译时间：2026-10-02 08:10
