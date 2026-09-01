---
title: 'Introducing Adaptive Intelligence: undermining the economics of every bot
  attack'
title_original: 'Introducing Adaptive Intelligence: undermining the economics of every
  bot attack'
date: '2026-08-31'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/introducing-adaptive-intelligence/
author: ''
summary: '[翻译失败，原文如下]


  Modern bot threats are increasingly driven by determined, sophisticated attackers.
  Often it is not even one person, but a group trading t...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-01T07:05:10.457979'
---

[翻译失败，原文如下]

Modern bot threats are increasingly driven by determined, sophisticated attackers. Often it is not even one person, but a group trading techniques with each other or a commercial service sold to anyone willing to pay. For many of them, getting past bot detection is a full-time job they genuinely enjoy. Block them and they get to work, finding a workaround. AI has simplified this further, making it even easier to set up complex configurations for attackers, lowering the overhead of an attack.Â

This shift puts defenders at an economic disadvantage. Responding and adapting to new attacks takes care, evidence, and effort to ensure efforts to block attackers donât impact real users on the way. Attackers have no such concerns and are primarily constrained by their time and their pool of proxies, and ensuring their infrastructure providers donât shut down their accounts.

Their advantage is the cost of adaptation. Attackers can adapt as often and continuously as they need, while most defenses are deployed in discrete, managed releases. Cloudflare analyzes more than a trillion requests a day for signs of automated abuse, so we see how fast attackers change tactics. That gap in responsiveness is widening.

The inconvenient truth: bot detection across the industry often rests on a hopeful assumption that if you make the wall tall enough, attackers stay out. In reality, a determined attack always finds a way through.The question is not whether a determined attacker can get through. They will. The question is what happens when they do.

Today we are launching Adaptive Intelligence, a new bot detection engine that starts from the opposite idea. Rather than betting on a wall that keeps every attacker out, Adaptive Intelligence makes getting through so slow and costly that the attack stops being worth running.

We believe that no other bot detection works this way.

### One attacker, many disguises

Not every attack is obvious to spot. The most sophisticated ones are built to disappear into ordinary traffic.

An attacker can spread requests across a large residential proxy network, keep the rate from each address low, and move patiently through a login, checkout, or account-recovery flow. Every request comes from a different address, often with a fresh user agent or a new bot fingerprint, so each one looks like a new visitor. No single source ever crosses a rate limit.

This is what makes the shape so hard to stop. Tighten the thresholds too far and real customers are turned away, which is the outcome you are trying hardest to avoid. The attack lives in the space between one request and the next, and a defense that studies each request on its own will never see it.

### The flaw of deterministic detection

The challenge with rule-based systems is that they hand the attacker a stationary target. They iterate in days while the model waits months for its next update, so by the time it catches up, the tooling has already moved on.

Bot detection has always answered a new attack technique by writing a rule to catch it. That works, until the attacker studies the signal, learns how to circumvent it, and forces another rule to be written. Some of the most advanced attackers have even created tooling to semi-automate this process. The defender appears permanently disadvantaged.

This kind of detection is âdeterministicâ, meaning that the same input always produces the same output. A defense that never changes teaches the attacker how to beat it and indirectly drives bot operators to build more capable automated attacks. Against a deterministic defense, automated probes return a clean yes or no, and over enough attempts that feedback teaches an attacker exactly where the edges of the system are. The economics are in the attackerâs favor.

## Changing the economics of attack

Adaptive Intelligence aims to reverse the economics and put them back in the defender's favor.

A defense that keeps changing flips that calculation, but only if two things are true at once. First, it has to cost the defender less to react than it costs the attacker to work around it. Second, attackers must be starved of the feedback they use to adapt, so they cannot simply learn their way back in. Get both right and the attacker's own loop turns against them: nothing they learned stays true, and each new attempt costs more than the last, until the attack is no longer worth running.

Part of that is giving an attacker less to learn from. Adaptive Intelligence can recognize a bot from a signal without visibly reacting to it, so the attacker keeps relying on a tell they do not realize we can see. And it treats detection as a statistical judgment rather than a fixed rule. That makes it non-deterministic. It weighs many signals at once, so there is no single piece of logic for an attacker to isolate and beat.

## A new detection engine

Your bot score already comes from several detection methods working together: machine learning, behavioral validation, JavaScript fingerprinting, a library of heuristics, and checks that recognize known, verified bots like search crawlers.Â

Adaptive Intelligence is a brand new bot detection engine that sits behind bot score. Where every other system is built to keep attackers out by accumulating rules, Adaptive Intelligence is built with the assumption that attackers will eventually get in, and makes that attempt as costly as possible.Â

Below, we explain three components our Adaptive Intelligence detection engine will have, that are unique when compared to traditional models: improving itself, disposable rule generation, and learning from the traffic it protects. Launching today is its first component: the machine learning at the center of your bot score, now retraining continuously instead of shipping as a fixed version. It aggregates network signals from across Cloudflare's network and measures the probability of automated abuse for every request. Where a fixed model sits still, Adaptive Intelligence keeps moving. The second and third components explained below are soon to follow.

### 1. Improving itself

The engine retrains continuously on live traffic. As new bypass tools and bot frameworks appear, it learns from them and folds that knowledge into the model behind your bot score, without waiting for a scheduled release. A technique that shows up this week is one the engine can recognize this week. The score you already build on stays close to what attackers are actually doing, rather than drifting further from reality between updates.

### 2. Disposable rule generation

A disposable rule is a rule that we expect the attacker to adapt to, but doesnât improve the attacker's bot in the process. Adaptive Intelligence is designed to create disposable rules aimed at a specific attack, deploy and retire them at random intervals, and never leave them in place long enough to become a fixed target. Because the rules keep appearing and vanishing, they inject noise into the very signal an attacker relies on to train against us, so an attacker never gets the steady yes-or-no that a static defense leaks. No single rule has to be perfect or unbeatable. It only has to last long enough to do its job, then make way for the next one. By the time an attacker has reverse-engineered a specific pattern, the engine has already moved on, rendering their engineering effort worthless.

### 3. Learning from the traffic it protects

Adaptive Intelligence will also learn from the patterns it sees across millions of sites. When a customer flags a real visitor we scored incorrectly, or our own measurement catches a miss, that correction becomes a training signal. Over time the engine tunes to the problems Cloudflare's customers are actually facing, so the protection you get reflects the current threat landscape instead of a snapshot of an older one.

## How it works

[翻译失败，原文如下]

Adaptive Intelligence runs in a loop: observe, train, deploy, validate. The range of signals it draws on keeps growing as we connect more of the network into it.

![BLOG-3439 2.png](/images/posts/598278b709bd.jpg)

Observe.The engine aggregates Cloudflare network signals, such as JA4 TLS fingerprints, request structures, challenge outcomes, session behavior, network reputation, and higher-level meta signals, alongside client-side telemetry from Turnstile and Precursor. A client that looks ordinary on any single request but moves like a script across a whole session is caught by its behavior over time, even when each request looks legitimate.

Train. We retrain the ML system continuously on live traffic, including the newest bypass tools and bot frameworks as they appear in the wild. The training set is refreshed often, so the system can react much faster to new attack techniques.

Deploy. New model weights roll out across the network on their own. There is no version to choose and no upgrade to schedule, and once you are on it, nothing for you to do. The model scoring your traffic reflects the threats we are seeing right now.

Validate. Before a new version becomes your primary defense, it runs in shadow mode alongside the current one, scoring live traffic without affecting a single visitor. We compare the two and watch signals like challenge solve rates. If a new version would score real people worse, it does not go live.

Cloudflare has run this kind of automated loop against DDoS attacks for years: sample traffic, TLS fingerprint the patterns behind an attack, push protections out across the network, and keep measuring so they can be adjusted or retired as the traffic changes. Bots are a harder version of the problem, because the signals are quieter and the story only shows up over time. Any one signal can look perfectly normal on its own. It is the relationships between them, and the company they keep, that reveal a bot hiding in normal traffic.

Adaptive Intelligence evaluates traffic over several time windows at once. A short window catches a sudden burst as it develops. A longer window reveals the behavior that repeats across thousands of addresses, clients, and sessions that have no reason to behave alike, and ties those scattered requests back to a single source. The same engine that spots an obvious scraping spike also surfaces a slow, distributed credential-stuffing attack sending only a handful of requests from each address.

### Building new detections automatically

As the next parts of Adaptive Intelligence come online, mining systems will search recent, labeled traffic for combinations of signals that separate an emerging attack from real users.

Often, a useful detection comes from the relationship between signals we already know, rather than a signal we have never seen before. A client might claim to be one browser while producing the network or JavaScript signals of another. A request might look normal on its own but form an odd sequence alongside the rest of the session. Automated mining lets us test many of these combinations and turn the strongest into candidate detections.

These candidates are deliberately narrow. They do not need to catch every bot on the Internet, or even every request in the current attack. That makes them quick to build and easy to replace when an attack changes tactics.

### It remembers

Attackers do not attack once. They pause, retool, and come back. Retiring a detection does not mean forgetting the pattern behind it. The engine keeps a memory of past attacks even after their detections stop firing, so an attacker cannot escape just by flipping between two profiles and betting the second one looks new.

That memory gives the system a head start when a familiar attack returns or a related one appears. A detection can expire when it stops earning its place, while the evidence behind it stays available to build the next one. Nothing piles up as stale rules in production, and the system never has to learn an old attack from scratch.

The result is one automated loop that can react to an obvious spike or quietly gather evidence on a patient, distributed attack that stays under traditional thresholds.Â

### Deploying safely

Constant change only helps if every change is safe, and the bar is high. Customers can live with the occasional bot slipping through, but a real visitor wrongly turned away is the failure that actually costs. That is the worry that makes teams cautious about automatic updates, so a new detection has to earn its place before it affects anyone.Â

We test each candidate against recent real traffic and measure how much known automation it catches and how often it would flag a genuine visitor by mistake. It rolls out gradually as an input to your bot score while we watch score distributions, challenge outcomes, and customer feedback, and we can pause or roll it back before it reaches your whole network. Every update has to prove it is at least as good as the one it replaces, on the measures that matter for this kind of system, precision and recall among them.

## One vision: Adaptive Intelligence and Precursor

This engine does not work alone. Last month we introducedPrecursor, a continuous behavioral validation engine for bot management built with privacy in mind, which measures automated abuse based on how a visitor behaves once they reach the browser: the timing, the movement, the small human signals that automation struggles to fake. Precursor and Adaptive Intelligence were built as two parts of one idea to detect malicious automation. Precursor does so through measuring continuous session-behavior; Adaptive Intelligence learns from bot detection signals across the whole network, and the signals from one make the other harder to fool.Â

It also reflects how we think about the problem: the bot detection engine should shrink what gets through, and keep adapting faster than the attacker on the other side.

## What's coming next

Continuous retraining is the foundation, and more of the engine comes online from here. We are expanding automatic detection generation for bots, connecting more of what Cloudflare sees across the network, the challenge, and the browser into a single view of a session, and giving you more ways to act on what the engine finds.

Knowing that no defense will keep every determined attacker out lets us aim for something more useful: making each attempt short-lived while costing the attacker more than it will ever return. Adaptive Intelligence reacts faster to new techniques, and gives attackers less to learn from each time it makes a change. The attacker who never quits now faces a defense that is different each time they return, so their persistence stops paying off.

## Getting started

Enterprise customers should turn on "Auto Update Machine Learning" in theBot Management dashboard. With it on, you get Adaptive Intelligence automatically, with no version to migrate and nothing to configure, and the bot score you already build on keeps working unchanged. If you are not sure it is enabled, check now so you are covered from day one.

## Related tags

Follow on Social Media

- Cloudflare
- Chris Pope

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Introducing Adaptive Intelligence: undermining the economics of every bot attack](https://blog.cloudflare.com/introducing-adaptive-intelligence/)
> 
> 翻译时间：2026-09-01 07:05
