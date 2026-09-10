---
title: Why Spotify Is Not Using Bayesian A/B Testing | Spotify Engineering
title_original: Why Spotify Is Not Using Bayesian A/B Testing | Spotify Engineering
date: '2026-09-08'
source: Spotify Engineering
source_url: https://engineering.atspotify.com/2026/9/why-spotify-is-not-using-bayesian-a-b-testing/
author: ''
summary: '[翻译失败，原文如下]


  # Why Spotify Is Not Using Bayesian A/B Testing


  ![Feature Image](/images/posts/770901fb5715.png)


  In recent years, amid growing interest...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-10T07:13:57.543072'
---

[翻译失败，原文如下]

# Why Spotify Is Not Using Bayesian A/B Testing

![Feature Image](/images/posts/770901fb5715.png)

In recent years, amid growing interest in Bayesian interference for A/B testing, many commercial experimentation platforms have added a Bayesian mode, includingGrowthBook,LaunchDarkly,PostHog,Amplitude Experiment,Optimizely,VWO,Statsig, andEppo.

The main argument is that Bayesian A/B testing is modern, flexible, and easier to interpret than frequentist statistics. In addition, it’s often claimed that many of the frequentist complexities, like multiple testing and sequential testing, fall out naturally in the Bayesian way of thinking.

This blog post aims to interrogate these claims and to posit a counterargument: in Bayesian A/B testing, there is a theme of oversimplification that frequently leads to bad inference practice that is no better than peeking in frequentist statistics.

This post is derived froma paper we recently wrotethat found that Bayesian and frequentist frameworks are much closer than the debate suggests.

We’ll break down the paper’s findings in five steps:

- First, we examine some generic claims about Bayesian A/B testing and show exactly when and how they apply.
- Second, we organize Bayesian configurations into tiers that provide different guarantees for the experiment program.
- Third, we show how Bayesian decision theoretic formulations can be translated into equivalent frequentist formulations.
- Fourth, we make the broader point that Bayesian and frequentist experimentation overlap.

First, we examine some generic claims about Bayesian A/B testing and show exactly when and how they apply.

Second, we organize Bayesian configurations into tiers that provide different guarantees for the experiment program.

Third, we show how Bayesian decision theoretic formulations can be translated into equivalent frequentist formulations.

Fourth, we make the broader point that Bayesian and frequentist experimentation overlap.

We see many companies debating whether they need both Bayesian and frequentist modes while not yet nailing the basics of either. Many are drawn to tools with flexibility without accounting for their complexity. Our goal in this post is to articulate this complexity, to explain why Spotify currently sees no need to add Bayesian inference alongside existing frequentist tooling, and to help companies seeking to run experiments understand how to choose the best mode for their needs.

## Clarifying what Bayesian inference for A/B testing is

The question of whether to use Bayesian A/B testing arises when a company wants to launch or enhancean experiment program, a series of experiments over time. Many companies have been led by the online discourse to believe that Bayesian inference is by default the best approach.

The problem is thatBayesian inference for A/B testing is not one thing.It is a family of configurations, each defined by a stopping rule, a prior, and a likelihood. Rather than starting with the tool (Bayesian A/B testing), a company should start by asking: whatgoalsare important for my experiment program? For example:

- The program should limit the number of shipped features with no effect
- Impact should be estimated with a certain precision
- A certain cost function should be minimized over time

The program should limit the number of shipped features with no effect

Impact should be estimated with a certain precision

A certain cost function should be minimized over time

The statistical configuration that is best for the company then depends on the goalsand constraints of the experimentation program.

Online discussion about Bayesian A/B testing is confusing because it implicitly mixesgoalsandconfigurations. Non-stats-savvy readers are left thinking that Bayes is an almost mystical form of inference that avoids the problems associated with frequentism. A claim that sounds like a fact about Bayesian A/B testing is often a fact about one goal paired with one configuration. For example:

- A flat-prior that stops on a posterior-probability threshold, the default in almost every platform offering Bayes, reproduces the false positive rate of frequentist peeking.Bayes factor stoppingcompares the evidence for a treatment effect against the null; as it is a martingale under the null,Bayes factorthresholding provides false positive rate control under peeking (also called ‘optional stopping’).
- A calibrated empirical Bayes prior can shrink effect estimates to counter winner’s curse bias and bound the false discovery rate.
- Decision-theoretic approaches derive stopping rules to minimize a chosen cost function and sometimes control frequentistic rates, and sometimes not.

A flat-prior that stops on a posterior-probability threshold, the default in almost every platform offering Bayes, reproduces the false positive rate of frequentist peeking.Bayes factor stoppingcompares the evidence for a treatment effect against the null; as it is a martingale under the null,Bayes factorthresholding provides false positive rate control under peeking (also called ‘optional stopping’).

A calibrated empirical Bayes prior can shrink effect estimates to counter winner’s curse bias and bound the false discovery rate.

Decision-theoretic approaches derive stopping rules to minimize a chosen cost function and sometimes control frequentistic rates, and sometimes not.

These are not variations on a theme. They are differentconfigurationswith different guarantees to meet differentgoals. In fact, the Bayesian inference framework covers everything from state-of-the-art sequential methods to procedures that are numerically identical to bad frequentist practice. We think understanding the Bayesian experimentation discourse lies in understanding these intricacies.

Further, we think it is important to realize thatfrequentistic error rates are not only for frequentists: Any experimentation program produces false positive and false negative results over time, regardless of whether its inference is based on Bayesian or frequentist philosophy, it is simply a classification of errors. The relevant question is whether the goal of the program is to control those rates, and whether the chosen configuration has parameters that control them.

## Dissecting common claims about Bayesian A/B testing

In each of the four examples below, we take a claim, dissect it, and show under what conditions it holds.

### 1. Peeking

Common claim:“Bayesian A/B testing does not require peeking correction.”

This can mean two very different things. You simply may not care about controlling the false positive rate under peeking. Or you may be using a Bayesian configuration, such as Bayes factor stopping, that controls it automatically.

Those are not the same argument. The first implies thegoal. The second implies theconfiguration. Treating both as a generic property of “Bayes” is where the confusion starts.

The likelihood principle

The usual justification for not caring about the false positive rate is theLikelihood Principle: the posterior remains a valid belief update regardless of when or why data collection stopped.

This is correct, but it is a narrow guarantee. Error-rate control, estimation precision, and decision-theoretic performance all depend on the prior and stopping rule. A coherent posterior is rarely the only goal of an experiment program, and by itself it provides none of those other guarantees.

A clearer claim would be

“I only care that my posterior is valid when I stop, and the Likelihood Principle gives me that.”

False positive control with Bayes factor stopping

Bayesian A/B testing has many configurations, including configurations explicitly designed to control the false positive rate under peeking, and others that do not. If you want to control the false positive rate under peeking, Bayes-factor stopping is that natural Bayesian configuration.

[翻译失败，原文如下]

Interestingly, we are not aware of any platform that offers Bayes-factor stopping. Note that there is no contradiction between the likelihood principle and bounding the false positive rate, with Bayes-factor stopping you get both.

A more formal approach to Bayesian inference is decision theory. It allows you to formulate goals as cost functions and then derive the optimal stopping rule. It turns out that for several common cost functions the optimal stopping rule is Bayes-factor stopping, which then indirectly bounds the error rates. (We return to this in the section about decision theory.)

A clearer claim would be:“Bounding the false positive rate under peeking is not my primary goal, but I’m using Bayes-factor stopping so I get that guarantee anyway”.

![Figure 1: Monte Carlo simulation of false positive rate under peeking for 5 different configurations. Two frequentist: fixed-sample inference and group sequential testing. Three Bayesian: flat prior with posterior probability stopping, two versions of Bayes factor (BF) stopping with a weekly informative prior and the perfectly estimated empirical Bayes prior (see more in the section below). The Likelihood principle applies to all three Bayesian configurations, but two additionally bound the false positive rate below alpha.](/images/posts/1e971307c57c.png)

### 2. Multiple metrics

Common claim:“Bayesian testing handles multiple metrics automatically.”

This claim mainly hides how specific and demanding the relevant Bayesian configuration is. It’s like saying “peeking doesn’t inflate the false positive rate” for frequentist experiments. It’s true for some configurations of frequentist inference, and false for others: it’s not a statement about the framework itself.

There are two aspects of this statement that makes it muddle the frequentist vs Bayes discourse: First, the error rate that can be bounded without an explicit multiple-testing correction isthe false discovery rate, not the false positive rate that many readers will assume. Second, the configuration that delivers false discovery rate control is very specific andfarmore demanding than the claim suggests.

You need Bayes-factor stopping and a well-calibratedEmpirical Bayes priorfitted from a program's historical experiments. The prior needs apoint-mass componentrepresenting the fraction of historical metric observations that are null. That fraction absorbs the multiplicity correction: it is not an absence of correction, but a very sophisticated and intricate version of one. When the prior is well-calibrated, this delivers false discovery rate control across metrics without an explicit multiple-testing adjustment. When it is poorly calibrated, the false positive rate is not bounded.

In summary, the setup that delivers the claim requires a maintained historical archive of experiment results, no inappropriate pooling across heterogeneous programs or metrics, no undetected drift, and no winner-biased corpus. Without that, you don’t get the guarantees you started out with as requirements. We return to the details of the failure modes in the section about the Empirical Bayes prior below.

A clearer claim would be:“If you have a well-calibrated empirical Bayes prior that applies to all metrics and use Bayes factor stopping, you can bound the false discovery rate without explicitly correcting for the number of metrics.”

### 3. The winner’s curse

Common claim:“Bayes fixes the winner’s curse.”

This is the least problematic claim.Any informative prior shrinks the effect estimate toward the prior mean, and that shrinkage works against the winner’s curse. With a reasonable informative prior, shipped effect estimates will be less inflated than estimates from a flat prior or a frequentist point estimate.

The problem is that most teams using Bayesian A/B testing run the platform default, which usually means a flat prior. A flat prior provides no shrinkage. Its posterior mean equals the maximum likelihood estimate, so the winner’s curse is just as severe as in the frequentist case. The claim “Bayes fixes the winner’s curse” is only true for people using an informative prior, and the degree of correction depends entirely on the quality of that prior. A well-calibrated empirical Bayes prior goes further by calibrating the amount of shrinkage to the program’s effect-size distribution. It shrinks toward the right target by the right amount.

In our simulations, a well-calibrated historical prior achieved the lowest estimation error of any configuration we tested. But a misspecified prior made things precision and detection worse, not just comparable to having no prior, but actively worse than baseline group sequential testing (GST). We tested two common failure modes of prior estimation: One archive included only experiments that had already won. Another pooled different programs. Both degraded estimation accuracy.

![Figure 2: Monte Carlo simulation results for the empirical power and estimation accuracy across four Bayesian configurations with Bayes-factor stopping contrasted against frequentist group sequential tests. For details see the paper.](/images/posts/c5d9bde9d8a3.png)

In summary, the estimation-accuracy advantage of an informative prior is clear, but incorrect pooling in a historical prior can make the accuracy worse. Even with an oracle historical prior, the best possible prior for the program, showed no power advantage over GST.

A clearer claim would be:“Any Bayes with a zero-centered informative prior reduces the winner’s-curse bias, and a well-calibrated empirical prior can often counter it completely.”

Why organizations may struggle to implement empirical Bayes

The two sections above both point to that Bayes-factor stopping with a well-calibrated empirical Bayes prior offers genuine advantages that frequentist methods do not replicate as neatly. The problem is that estimating such a prior with sufficient quality to obtain the benefits is challenging.

The corpus must be large (sometimes >200 experiments) and representative. Even with enough experiments, the prior estimation can fail in ways that more data cannot fix. The most obvious challenge is avoiding pooling the prior across experiments that come from programs with different treatment effect distributions, or pooling across metrics from the same program but still have different effect distributions.

Consider a program tracking sign-up rate and recommendation click-through rate. Sign-up barely moves in most experiments; click-through moves easily. If you pool both into one corpus, the prior variance is too wide for sign-up and too narrow for click-through, and the null-rate estimate is wrong because the metrics have different true null rates. You end up with a prior calibrated to a distribution that neither metric actually follows. You can estimate one prior per metric, but this requires backfilling many historical experiments each time a new metric is created.

The common assumption is that future experiments areexchangeable drawsfrom the same distribution as past experiments. Since effect distributions often change within a program over time due to hitting diminishing returns and the fact that the world is constantly changing, it’s tricky to assess and detect when a historical program can be considered representative for new experiments and not.

Organizations with one mature program, consistent metric definitions, and statisticians maintaining the prior can get real value from empirical Bayes, but for most organizations, the complexity of maintaining the prior likely outweighs the benefits.

### 4. Decision theory often connects to error-rate control

Common claim:“We need Bayes because we want to take a Decision theory-theoretic approach.”

[翻译失败，原文如下]

Decision theorylets you specify costs instead of error rates. It’s strictly speaking not a Bayesian branch of math, but in A/B testing, the optimal policies turn out to be Bayes rules. For a simple and natural cost function that sums the costs of false positives, false negatives, and sampling, the optimal or near-optimal policy uses Bayes-factor thresholds. Because those thresholds also provide error-rate guarantees, the decision-theoretic and error-rate formulations become two parametrizations of similar configurations.

A frequentist who selects alpha and beta by reasoning about costs has implicitly chosen a cost function. A Bayesian who specifies costs inherits error rates.

The convergence does not hold for every cost function, and the exception is instructive. Expected-loss stopping, as described byStucchio, triggers when the posterior is tight enough that the expected harm is small. Even under no effect it will eventually ship the new variant once the posterior concentrates. With a flat prior the false positive rate is around 50%, but if deploying a null-effect variant is truly costless, this is the optimal stopping rule.

As Figure 2 shows, once that cost exceeds a few percent of a typical real effect, the rule is no longer optimal.

![Figure 3: The expected regret from making decisions under varying costs for shipping false positives using 4 different stopping rules. The expected-loss stopping of Stucchio.](/images/posts/544e47fb64e0.png)

So yet again, the framework needed depends on the goals: in this case, what the cost function implies. For cost functions whose optimal policy is a Bayes-factor threshold, the decision-theoretic and error-rate formulations are two parametrizations of similar rules. Many teams could get most of the value by choosing their alphas and powers based on a cost formulation, without switching framework. For cost functions whose optimal policy is not a Bayes-factor threshold, the decision-theoretic formulation genuinely differs from error-rate control.

A clearer claim would be:“We need Bayes because we use decision theoretic stopping rules that are not equivalent to restricting error rates.”

## Bayes and frequentism are closer than you think

![image2](/images/posts/20f92100c43e.png)

For the configurations most commonly deployed in practice, Bayesian and frequentist A/B testing are far more similar than the debate suggests.

Under a flat prior and the two-group normal model, Bayesian and frequentist procedures produce numerically identical outputs:

- The posterior mean equals the maximum likelihood estimate
- The one-sided posterior probability that B beats A equals one minus the p-value
- A 95% posterior-probability threshold is algebraically equivalent to the one-sided rejection region

The posterior mean equals the maximum likelihood estimate

The one-sided posterior probability that B beats A equals one minus the p-value

A 95% posterior-probability threshold is algebraically equivalent to the one-sided rejection region

An experimenter using flat-prior Bayesian inference with posterior-probability thresholds is running frequentist-equivalent inference under a different vocabulary.

The connection goes deeper than the flat-prior case. The mixture Sequential Probability Ratio Test, one of the most well-known frequentist sequential procedures, isexactlythe Bayes factor stopping under the same prior. A frequentist who selects a mixing distribution to maximize power at the minimum detectable effect is, in Bayesian terms, placing a prior on the treatment effect. The mixing distribution is the prior.

So the picture completes itself. The optimal decision rule for many natural cost functions is a Bayes factor threshold. That threshold is the mixture Sequential Probability Ratio Test. The mSPRT is well-approximated bygroup sequential testing(GST). There is a strong relation between costs and error rates. A frequentist, who thinks in alpha and beta, and a Bayesian, who thinks in costs, often land on the same configuration.

The frameworks are not opposites; many of the dominating configurations of both are overlapping in guarantees.

## Isn’t the interpretation nicer under Bayes?

Yes. Saying “there is a 95% probability that the effect lies between 0.2% and 1.1%” is more natural than explaining what “95% confidence” means. That said, we think the value of the probabilistic interpretation is oversold.

Under a flat prior, every probabilistic statement maps one-to-one to a frequentist quantity. The point estimates and interval bounds are the same. The posterior probability that B beats A is one minus the p-value. The probabilistic interpretation only becomes meaningfully different when informed by a good prior, and a good prior is not free: specifying, justifying, maintaining, and explaining it costs complexity. We gain interpretation but we pay in other kinds of complexity.

The Bayesian framework also makes richer quantities natural to compute, including the probability of exceeding a business threshold and the probability that one variant is best. Those are true advantages, but we question how often decisions are made differently because this information is present.

Similarly, we don’t think the interpretation question matters as much in practice as many seem to suggest. We have not seen product decisions deteriorate because someone treated a confidence interval as a probabilistic statement. What matters is thatevidence propagates correctly to decisions, not whether some intermediate step is technically correct.

## Why Spotify has not added Bayesian modes

Historically, all of Spotify’s production experiments are analyzed using frequentist statistics. We have long debated whether Spotify should allow experimenters to choose the mode of inference, or even only support Bayesian statistics in the platform.

To help us decide, we revisited the goals of the Spotify experimentation program:

- We want to minimize the number of experiments that lead to poor business decisions:
- Shipping changes that harm our product
- Shipping and maintaining changes that don’t improve the user experience
- Evidence from experiments should be trusted
- Experiment results should be hard to interpret incorrectly, especially across teams and departments
- Experiments should be easy to plan and configure, but hard to misconfigure

We want to minimize the number of experiments that lead to poor business decisions:

Shipping changes that harm our product

Shipping and maintaining changes that don’t improve the user experience

Evidence from experiments should be trusted

Experiment results should be hard to interpret incorrectly, especially across teams and departments

Experiments should be easy to plan and configure, but hard to misconfigure

Because people at Spotify constantly collaborate in experimentation, both in setting up experiments and consuming results across the company, having two modes has a high cost. Supporting both modes of inference would require different planning, different monitoring, different interpretation, and possibly different-looking outputs. So far, the benefit of a second framework doesn’t outweigh those costs.

That said, there are several Bayesian configurations that would match our existing frequentist setup. One Bayesian configuration that would add a genuine advantage is a well-calibrated empirical Bayes prior for both shrinkage and automatic FDR control. But it requires maintaining a prior at sufficient quality across every metric and program, which, if incorrect, can lead to poor decisions and eventually lower trust. We havewritten beforeabout how sophistication that adds confusion can reduce the strength of evidence rather than increase it.

[翻译失败，原文如下]

We also think the framework debate absorbs attention that would be better spent elsewhere. Is the inference coherent? Does the sample size calculator match how decision rules are actually applied? Are experiments producing learning, not just ship decisions? We have invested heavily in making those pieces work together (read about ourExperiments with Learning framework, our approach tocombining multiple metrics into single product decisions, or our take onwhat makes a good sample size calculator).

The advice we want to give is: Start with the experimentation program you want. Decide which guarantees you need and can maintain consistently. Then ask whether a specific Bayesian configuration meaningfully improves on what you already have. For Spotify today, it does not.

---

> 本文由AI自动翻译，原文链接：[Why Spotify Is Not Using Bayesian A/B Testing | Spotify Engineering](https://engineering.atspotify.com/2026/9/why-spotify-is-not-using-bayesian-a-b-testing/)
> 
> 翻译时间：2026-09-10 07:13
