---
title: When Can You Ship on Offline Evals Alone? | Spotify Engineering
title_original: When Can You Ship on Offline Evals Alone? | Spotify Engineering
date: '2026-11-19'
source: Spotify Engineering
source_url: https://engineering.atspotify.com/2026/11/when-can-you-ship-on-offline-evals-alone/
author: ''
summary: '[翻译失败，原文如下]


  # When Can You Ship on Offline Evals Alone?


  ![Feature Image](/images/posts/7f433fe6d967.png)


  TL;DRTeams building AI features want to sk...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-20T09:31:33.280112'
---

[翻译失败，原文如下]

# When Can You Ship on Offline Evals Alone?

![Feature Image](/images/posts/7f433fe6d967.png)

TL;DRTeams building AI features want to skip slow A/B tests and decide from offline evals alone. This post looks at when that’s possible while keeping the risk of harming the online metric low. It can work, but only under strong assumptions that are hard to verify and can change over time. Noise is a problem too, because it can hide a strong link between offline and online results. In our example, a naive estimate says the eval explains 24% of the variation in online results, when the true figure is 60%.

As agentic and LLM-based products and features become increasingly common, there is growing discussion about how to iterate on them efficiently. To assess product quality and the impact of changes, offline evals have become a standard part of the toolkit, alongside human evaluations, online A/B tests, and surveys.

When we change an AI feature, say a new prompt or a different underlying LLM, there are two main ways to check whether it got better. Offline evals are quick tests run on a fixed set of sample prompts before any real user sees the change, often with other LLM-as-judges grading the answers. A/B tests give the new version to a random group of real users and compare how they behave against users on the old version.

A question that frequently comes up is whether we can rely more heavily on offline evals and less on alternatives that are more time-consuming and resource-intensive. More specifically,can we skip A/B tests and rely only on offline evals to make product decisions?And if so, when?

The potential upside is substantial. Offline evals take hours; A/B tests often take days or weeks.

If we could confidently make product decisions based on offline evals alone, we could shorten feedback loops and iterate much faster. But what exactly do we mean by“canwe make decisions on evals alone”?

![Figure 1: The idealistic decision flow with offline evals and an A/B test in sequence for each product decision.](/images/posts/4f3788fe4a03.png)

The goal of this post is twofold. First, to formalize what guarantees we would want from a decision to ship a change based on offline evals, without an A/B test.

Second, to understand what we need to know, assume, or estimate to achieve such a guarantee, and the major challenges and pitfalls involved.

In our paper,When Can You Ship on Evals Alone?, we work through this problem in detail. The approach is general and aims to help build intuition for any team building LLM-based products.

## What do we need to know?

We formalize the “when we can ship based on eval alone” as follows:We want to make shipping decisions based on the offline eval while bounding the risk of shipping something that actually harms the online metric.

If we want to bound the risk of shipping something that harms the online metric, ideally we need to know the conditional distribution of the true online treatment effect, given the observed offline eval treatment effect. If we know this distribution, we can directly assess and bound the risk of making a harmful shipping decision given any observed eval effect. In plain terms: for any eval result, we want to know how likely it is that the change actually helps or hurts real users, in terms of some specific online metric.

![Figure 2: the joint distribution of observed offline eval effects and true online effects. The “slice” at any given eval effect is the conditional distribution of the true online effect given the observed offline effect.](/images/posts/5193e769a7c2.png)

So how can we learn this relationship? This is where things get nuanced.

The first challenge is that we need paired observations of offline eval effects and online treatment effects, all coming from the same underlying relationship. We cannot have a heterogeneous set of experiments where, for some types of changes, an improvement in the eval corresponds to an improvement in the online outcome, while for others the relationship is different or even reversed.

The second challenge is measurement error. Both numbers are noisy estimates, not exact values. Offline eval scores have sampling errors from several sources, including randomly sampling examples from a larger eval set, and using an LLM to grade the answers (LLM-as-a-judge). Online treatment effects are estimated with sampling error too. We need to account for these errors when learning the relationship.

To build intuition for these challenges, and for what happens when our assumptions fail, we introduce a simplified working model.

## A simplified working model

This model makes a few strong simplifying assumptions. Readers who want to skip the statistics can jump to the next section. All the details are in the paper.

- First, we assume that we have a sufficiently large, homogeneous pool of paired offline eval effects and online treatment effects. And, we assume that any future changes for which we want to make eval-based decisions come from the same class, with the same underlying relationship between offline and online effects (also called exchangeability).
- Second, we assume that the true offline and online treatment effects follow a bivariate normal distribution.
- Third, we assume that measurement errors are centered at zero with known variances, independent across interventions.
- Finally, we assume that any errors introduced by using an LLM as a judge are independent of the treatment arm.

First, we assume that we have a sufficiently large, homogeneous pool of paired offline eval effects and online treatment effects. And, we assume that any future changes for which we want to make eval-based decisions come from the same class, with the same underlying relationship between offline and online effects (also called exchangeability).

Second, we assume that the true offline and online treatment effects follow a bivariate normal distribution.

Third, we assume that measurement errors are centered at zero with known variances, independent across interventions.

Finally, we assume that any errors introduced by using an LLM as a judge are independent of the treatment arm.

These are strong assumptions and we will return to what happens when they are violated or relaxed.

## The importance of handling measurement error correctly

The short version: if we ignore noise, a strong offline-online relation can look weak.

To understand how important the measurement error handling is, a good starting point is to consider how to estimate the strength of the relationship between offline and online outcomes.

Under the assumptions, the conditional distribution of the online effect given the eval effect is fully specified. The squared correlation (R², roughly how much of the online result the eval explains, from 0 to 100%) determines how much uncertainty remains in the online effect after observing the eval. A high R² means the eval is highly informative about the online outcome. A low R² means substantial uncertainty remains, regardless of how precisely we measure the eval.

Using a naive estimator, we find that the squared correlation is only 24% in the working example of the paper, whereas the true value is 60%. More generally, we show that the naive squared correlation estimator is attenuated by measurement errors: noise in both measurements dilutes the correlation we observe.

This matters even at the initial stage, when we simply want to assess whether offline evals might be good enough proxies for A/B test outcomes. Without properly accounting for measurement error, we risk substantially underestimating the strength of an existing relationship.

Under our working model, we can use classical meta-analytic methods to model the error structure and adjust for measurement errors when estimating the underlying relationship.

## Constructing a decision gate

[翻译失败，原文如下]

Say we believe that the assumptions of the working model are fulfilled. How would we construct a decision rule based on the offline eval?

Under our assumptions, we can estimate the conditional distribution of the true online treatment effect, given the observed offline eval effect.

We can then construct a decision gate that bounds the risk of shipping something harmful, or killing (deciding not to ship) something that would actually improve the online metric.

Unless the squared correlation is one, there will be cases where a positive offline eval effect does not correspond to a positive online effect, and vice versa. Making decisions based on weakly positive or negative eval effects will therefore not achieve the guarantees we want.

Instead, the thresholds for shipping and killing need to depend on the strength of the surrogate relationship.

![Figure 3: Thresholds for the offline eval effects needed to bound the risk of harm in the online effect for different strengths of the offline/online correlation.](/images/posts/fbde0aeff514.png)

If surrogacy is perfect, we can test directly on the offline eval using the usual significance levels and obtain corresponding guarantees for the online effect. But the weaker the relationship, the stronger the evidence we need from the offline eval before making a decision.

![Figure 4: The offline-eval based decision making gate. It uses thresholds on the offline eval effect to make a ship, kill, or A/B test decision.](/images/posts/25abd96a9f14.png)

We end up with a gate where sufficiently positive offline eval effects lead to shipping, sufficiently negative effects lead to killing, and the cases in between go to an A/B test.

## Questioning the assumptions: The importance of a homogeneous dataset

Returning to the first fundamental challenge: what happens if we don't have a clean, homogeneous dataset?

Suppose we have experiments from several different classes of changes, where the relationship between offline and online treatment effects differs across classes. We can get Simpson's-paradox-type effects, where a trend appears in the pooled data but not within any individual group.

There might be no relationship between offline and online effects within any individual class, but when we pool them together, we observe a strong relationship.

![Figure 5: An example of how pooling across two experimentation programs with different offline/online relations can “fool” naive estimators into indicating a strong relation where there is none.](/images/posts/0e529859f54d.png)

The pooled dataset might therefore suggest very strong surrogacy, even though the offline eval has no predictive relationship with the online outcome within any of the individual classes.

Unless we're sufficiently certain that our experiments are homogeneous, we risk badly misestimating the strength of the surrogate relationship. We can inspect the relationship within different classes, but measurement error makes this harder.

There is a parallel here to maintaining a historical Bayes prior, as we discussed inthis blog post on Bayesian A/B testing. In both cases, the properties of our decisions depend on the quality of the historical corpus, which can be difficult to assess and maintain.

## Questioning the assumptions: Bias from LLMs as judges

LLMs-as-judges are used extensively to evaluate free-text answers from LLMs. There is agrowing body of research on verifying judge quality. For example,Ye et al. (2025)systematically investigates different forms of judge bias. In our paper, we focus on how a biased judge might affect decision making. There are two important cases.

The first is when the LLM judge is biased, but the bias is independent of the treatment arm. In this case, the bias is not a problem for estimating the treatment effect, because it cancels when we take the difference between treatment and control.

The second is when bias depends on the treatment arm. Then it can drastically affect both the observed treatment effect and the estimated strength of the relationship between offline and online effects. It can even flip the sign, making a worse version look better.

The important distinction is not whether the judge is biased, but whether the bias depends on the treatment arm.

This second form of bias is likely more common than one might expect. There is growing evidence thatLLM judges can favor their own generations. However,Chen et al. (2025)show that apparent self-preference can partly reflect genuine differences in output quality, rather than bias alone. This creates a problem when evaluating agentic systems, particularly when comparing different LLMs as the underlying model powering the agent.

Since comparing and switching between underlying LLMs is a common part of developing agentic systems, this type of bias is likely to be widespread in practice. And arm-dependent bias affects the validity of the offline-eval decision gate.

## Questioning the assumptions: What happens once we deploy the gate?

Suppose we construct this gate and deploy it for product decision making. Our assumption of a homogeneous dataset also implied exchangeability between historical and future experiments. We assumed that new changes would come from the same underlying relationship. But that assumption is a snapshot in time.

Unless we blindly assume it holds forever, we need some mechanism to detect drift (changes in the relationship over time). Surrogacy might become stronger or weaker over time, or disappear completely.

But here is the problem. Once we deploy the gate, we stop running A/B tests for changes in the shipping and killing regions. We observe their offline eval effects, but no longer their online treatment effects. We lose ground truth in exactly the regions where the gate makes decisions.

We can still observe the relationship for experiments in the middle region, since those go to A/B testing. But this does not tell us whether the relationship has drifted in the shipping and killing regions.

![Figure 6: The offline-eval based decision making gate with a random audit. A fraction of the offline-based decisions to ship without A/B-tests are still A/B tested to enable monitoring of drift in the online-offline relation in the shipping region.](/images/posts/6f94b9b247a0.png)

One way to handle this is to introduce an audit pool. We randomly select a small proportion of experiments that would otherwise be shipped or killed directly, and still run an A/B test for them. This gives us paired observations across the decision regions, allowing us to continuously validate the gate, detect drift, and update it when necessary.

The downside is that fewer decisions can be made without an A/B test.

## So, when can we ship based on offline evals alone?

Let's return to the question we started with:Can we ship based on offline evals alone while bounding the risk of harming online outcomes?

In principle, yes, provided we're willing to make sufficiently strong assumptions, and believe those assumptions are reasonable in practice. However, several important challenges remain.

In practice, the bar is high. Many of the assumptions are hard to verify, and even if you do verify them at one point, this is something you need to reevaluate continuously as relations between offline/online and distributions drift over time.

First, constructing and maintaining a clean corpus is difficult. We need sufficiently similar changes for their offline and online effects to plausibly follow the same joint distribution. This is difficult to establish, and even harder to maintain over time. Under standard product development, we should expect diminishing returns and other shifts that change the relationship.

[翻译失败，原文如下]

Second, our working model relies on strong distributional assumptions. These can be relaxed, but more robust decision rules would likely come at the cost of efficiency. With relatively weak surrogacy and conservative thresholds, very few changes may qualify for decisions based on offline evals alone. At some point, the efficiency gains may become too small to justify the approach.

Third, reliably characterizing measurement errors and biases introduced by LLM judges remains challenging, particularly when we also need to monitor drift and ensure that our assumptions continue to hold.

At Spotify, we use offline evals extensively to iterate on our LLM-based and generative AI offerings. They play an important role in our development process, but we continue to pair them with online experiments. This allows us not only to manage the risks we care about, but also to evaluate and optimize for longer-term outcomes that offline evals may not adequately capture.

Ultimately, an important distinction remains:A/B tests let us bound risks by design, whereas offline evals can only provide comparable guarantees through additional assumptions about the relationship between offline and online outcomes—assumptions that are often difficult to validate and maintain in practice.

---

> 本文由AI自动翻译，原文链接：[When Can You Ship on Offline Evals Alone? | Spotify Engineering](https://engineering.atspotify.com/2026/11/when-can-you-ship-on-offline-evals-alone/)
> 
> 翻译时间：2026-11-20 09:31
