---
title: Solving a 31-year-old grand challenge in mathematics – the KLS conjecture -
  Microsoft Research
title_original: Solving a 31-year-old grand challenge in mathematics – the KLS conjecture
  - Microsoft Research
date: '2026-10-21'
source: Microsoft Research
source_url: https://www.microsoft.com/en-us/research/blog/solving-a-31-year-old-grand-challenge-in-mathematics-the-kls-conjecture/
author: ''
summary: '[翻译失败，原文如下]


  ## Microsoft researcher and collaborator combine new mathematical ideas with human-directed
  AI to resolve a central problem in high-dimen...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-22T06:55:39.053646'
---

[翻译失败，原文如下]

## Microsoft researcher and collaborator combine new mathematical ideas with human-directed AI to resolve a central problem in high-dimensional geometry and probability

## At a glance

- Fundamental scientific breakthrough:Researchers resolved the Kannan-Lovász-Simonovits (KLS) conjecture, a 31-year-old problem widely regarded as one of the central open questions in high-dimensional geometry, with implications for statistics, optimization, algorithms, and computer science.
- A universal geometric principle:The result establishes a universal geometric principle for log-concave distributions, showing that simple flat cuts can capture their narrowest bottlenecks within a fixed factor, regardless of dimension.
- Human-AI collaboration:The breakthrough emerged from a human-directed agentic research process in which AI systems explored mathematical possibilities while researchers evaluated, pruned, and redirected the search.
- Independent confirmation:Multiple independent researchers have validated this research, identifying its central criterion as the key breakthrough, followed by a machine-checked formal verification.

For decades, a fundamental question about the difficulty of computing in high-dimensional spaces has resisted proof. New research resolves this question, removing a major theoretical obstacle to understanding the efficiency of randomized algorithms used across science and computing.

The Kannan–Lovász–Simonovits (KLS) conjecture was proposed in 1995. It asks whether, for a broad class of high-dimensional probability distributions, the best flat or hyperplane cut is always nearly as effective as the best cut of any shape. More precisely, KLS predicts that the two differ by no more than a universal constant, regardless of the number of dimensions. This would establish a dimension-free geometric principle with important consequences for high-dimensional geometry, probability, and theoretical computer science. Because the geometry of these cuts governs how quickly random walks can explore a distribution, KLS also plays a central role in the theory of high-dimensional sampling.

Since 1995, mathematicians have accumulated evidence that the conjecture was true, but a complete proof remained elusive. Now, two researchers, including Xinzhi Zhang from the Machine Learning and Optimization group at Microsoft Research, haveproved the KLS conjecture(opens in new tab). They have shown that the relationship holds with a fixed bound, regardless of how many dimensions a shape has. Before this work, thebest known result(opens in new tab), established in July 2026, allowed that bound to grow slowly as the number of dimensions increased. This work establishes a fundamental geometric principle: high-dimensional spaces are better behaved than previously known, and the obstacles to navigating them do not grow without bound as dimensions increase.

![Microsoft Research at BUILD 2026 | abstract pattern on a purple background](/images/posts/921376f45eb1.jpg)

## Microsoft Research at BUILD 2026

Giving developers a hands-on look at some of the many AI-based models and tools they can use to accelerate innovation, enhance their capabilities, and quickly transform ideas into prototypes.

The importance of the KLS conjecture was recognized across the field long before it was resolved. In its 2017-18 Annual Report, theMathematical Sciences Research Institute (MSRI)(opens in new tab)called it “a central open problem in high-dimensional convex geometry.” TheSimons Institute(opens in new tab)described it as “one of the most important open problems in convex geometry.” In the proceedings of the2022 International Congress of Mathematicians (ICM)(opens in new tab), Ronen Eldan noted its broad implications for high-dimensional convex and computational geometry.Quanta Magazine(opens in new tab)wrote that KLS “lies at the heart of many questions in statistics and computer science.”

## Technical details

The authors began by improving the July 2026 result in order to make the mathematical bound more precise. Working with AI agents in a structured, human-directed process, they explored more than 100 candidate approaches, many involving lengthy calculations with higher-order tensors. This produced a new mathematical criterion that became the foundation of the final proof.

The authors then discovered that the new criterion could be applied recursively. Each improved bound could be fed back into the same argument to produce a still tighter one. In the October 1, 2026 version of the paper, this reduced the dependence on dimension to the iterated logarithm. This function grows extraordinarily slowly, but it still grows with the dimension and therefore did not yet fully resolve the conjecture.

The final step was to repeat the entire recursive refinement, rather than applying it only once. This idea was inspired by the authors’ earlier work on fast algorithms for linear programming. The authors proved that the small errors introduced at each stage shrink fast enough that their total remains bounded by a universal constant, independent of the dimension. This eliminated the dependence on the number of dimensions and completed the proof in the October 4, 2026 version of the paper.

The recursive method, its repeated application, and the proof that the accumulated errors remain bounded are original contributions of the researchers. AI tools helped explore candidate approaches, carry out detailed derivations, prepare the manuscript, and perform internal proof checks. The researchers determined the mathematical direction, selected the promising ideas, assembled them into the final argument, and verified the proof.

## Independent confirmation

On the same day that the authors posted their complete proof, a separate group of leading expertsposted a full proof(opens in new tab)that they developed in parallel. Their work built upon the findings in thefirst version(opens in new tab)of the Microsoft paper, calling it “the crucial step in the proof.” Athird proof(opens in new tab)which appeared separately on the same day relies on a closely related idea. In addition, aLean 4 formalization(opens in new tab)was subsequently released, combining the key criterion from the first Microsoft paper with additional research.

Independent proofs are among mathematics’ strongest forms of validation because they demonstrate that a result does not rest on a single chain of reasoning. The subsequent appearance of alternative approaches and formal verification further strengthens confidence that the field has uncovered a genuine underlying principle rather than a fragile technical argument. The authors have also shortened their proof and verified the streamlined argument in Lean; they plan to release both after final review. Together, these developments provide complementary forms of confirmation.

## Human-AI guidance

In the process of proving KLS, this research also demonstrates the power of having researchers direct AI rather than simply asking AI to solve a complex problem through a single end-to-end run of a frontier model or agent. The authors used an agentic search process with iterative, human-assisted “pruning”: As multiple agents explored variations of an idea in parallel, the researcher examined their intermediate result, eliminated unpromising directions, and passed the most promising result to the next round. Roughly one hundred research trajectories were explored before the key breakthrough emerged.

In a separate track of the project, the authors made repeated unguided attempts to solve the same problem with several leading AI models, using roughly the same total token budget as the main process. That effort fell short of the goal. The eventual success depended on both the capabilities of the AI systems and the mathematical judgment of the researchers.

## Conclusion

[翻译失败，原文如下]

Taken together, resolving KLS settles a central problem in high-dimensional geometry. A wide range of results that previously relied on the conjecture as an assumption can now be stated unconditionally. The proof therefore provides a stronger foundation for research in convex geometry, probability, and theoretical computer science.

The work also demonstrates how carefully guided human-AI collaboration can contribute to genuine scientific discovery while reinforcing, rather than replacing human insight. It highlights the continuing importance of scientific judgment in identifying promising directions, recognizing conceptual connections, and seeing when a partial insight points toward a deeper result. The authors are now simplifying the proof and extending its formal verification so that the mathematics and theoretical computer science communities can more easily examine the result and build on it.

## Acknowledgements

Thank you to our co-author Zhao Song for his contributions to this work, andVictor Reis(opens in new tab)andIshai Menachefor helpful discussions throughout the project.

## Meet the authors

### Xinzhi Zhang

Senior Researcher

---

> 本文由AI自动翻译，原文链接：[Solving a 31-year-old grand challenge in mathematics – the KLS conjecture - Microsoft Research](https://www.microsoft.com/en-us/research/blog/solving-a-31-year-old-grand-challenge-in-mathematics-the-kls-conjecture/)
> 
> 翻译时间：2026-10-22 06:55
