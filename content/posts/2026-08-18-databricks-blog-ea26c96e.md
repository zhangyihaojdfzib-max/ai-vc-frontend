---
title: Evaluating AI Agents Live at the Grounded Reasoning Cup
title_original: Evaluating AI Agents Live at the Grounded Reasoning Cup
date: '2026-08-18'
source: Databricks Blog
source_url: https://www.databricks.com/blog/evaluating-ai-agents-live-grounded-reasoning-cup
author: ''
summary: '[翻译失败，原文如下]


  - The Grounded Reasoning Cup challenged 11 academic teams to apply agents developed
  on OfficeQA Pro to OfficeQA Pro V2, a newly released ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-19T03:08:00.392453'
---

[翻译失败，原文如下]

- The Grounded Reasoning Cup challenged 11 academic teams to apply agents developed on OfficeQA Pro to OfficeQA Pro V2, a newly released benchmark built from approximately 120,000 pages of U.S. Treasury documents.
- Results showed that generalization cannot be assumed. Approaches developed on a familiar benchmark did not always transfer reliably to a new corpus, and out-of-the-box frontier agents averaged less than 30% accuracy.
- Stanford’s winning team achieved 63.3% accuracy through an end-to-end agent optimization strategy that combined a library of reusable skills, targeted document-representation fallbacks, and adaptive verification.

This year, Databricks hosted the inauguralGrounded Reasoning Cup, a first-of-its-kind live AI competitionto evaluate AI agents’ ability to reason over complex, enterprise-style document collections. By testing agents on a newly released corpus under live competition conditions, the Grounded Reasoning Cup was designed to help answer one of the hardest questions in AI evaluation: how well do performance improvements on a benchmark generalize to similar, real-world tasks?

The competition brought together 11 top academic teams from across the U.S. and Canada, paired with resources and mentorship from frontier labs including OpenAI, Anthropic, and Google DeepMind. Over the course of two months, teams developed and optimized their agents onOfficeQA, our flagship grounded-reasoning benchmark designed to reflect economically valuable enterprise workflows. On competition day, they were challenged to apply those systems in real time to a newly released grounded-reasoning benchmark,OfficeQA Pro V2, designed to test whether their improvements generalized.

Stanford won with a system that achieved 63.3% accuracy, beating out the average team by approximately +22 points, and the average frontier agent offline baseline by approximately +35 points. The top teams demonstrated substantial gains through document preprocessing, targeted retrieval, parallel agents, structured tool use, and verification. At the same time, 18.8% of questions went unsolved by every team, underscoring how much headroom remains in enterprise grounded reasoning.

![Performance of baseline offline AI agents (agents powered by frontier models available at the time of the competition), along with Grounded Reasoning Cup teams. The top 3 teams: Yale, UMass, and Stanford, were able to outperform both baselines and the average of remaining teams by ~20+ points. One caveat is that the offline setting that baselines were run in is not directly comparable with the competition setting teams were tasked with. In our offline agent evaluations, a frozen agent configuration is run once across the full test set, with no round structure, no pauses, and no chance to react to intermediate failures.](/images/posts/cd099beb7a7f.png)

In this blog post, we recap the competition and discuss agent optimization strategies and insights from the Grounded Reasoning Cup’s winning teams: Stanford, University of Massachusetts Amherst, and Yale.

In general, we find the following:

- Generalization requires representative, held-out evaluations.Techniques developed on OfficeQA did not always transfer reliably to our new benchmark. This stresses the importance of utilizing held out test sets like OfficeQA Pro V2 to ensure solutions generalize to new examples.
- Agent performance depends on the full system, not only the model.The average gap between the top scoring and lowest scoring teams using the same model was 30.4 points. Parsing, retrieval, tool use, verification, parallelism, and operational infrastructure all made the difference in whether agents could successfully complete end-to-end grounded reasoning tasks.
- Enterprise grounded reasoning remains far from solved.Even winning teams struggled with many of the benchmark’s retrieval, parsing, and analytical demands, leaving substantial room for continued research and improvement. We encourage practitioners to use the publicly available OfficeQA benchmark suite to continue advancing this work.

## The Competition Setup

The goal of the Grounded Reasoning Cup was to bring together top academic teams to develop generalizable approaches to grounded reasoning – a common task in enterprise settings that involves answering complex questions using evidence from large, often proprietary, document collections.

Teams of 2-4 people representing their academic institution were paired with an industry partner from OpenAI, Anthropic, or Google DeepMind, who provided access to their models and mentorship throughout the development period. Teams had approximately two months to build an agent using any approaches they saw fit, with the one constraint that they must use their partner lab’s model family exclusively to power their agent. During this period, they used the OfficeQA benchmark to evaluate new techniques they believed would generalize to similar grounded reasoning tasks.

On the day of the competition, teams were then tasked with applying their agents in real time on a new, freshly released benchmark. The competition was governed by the following rules:

- Benchmark release:The new corpus (the U.S. Treasury’s Accounts of Receipts and Expenditures) was released just 36 hours before the competition. This gave teams time to process and index the data while limiting the opportunity for methods to overfit to the new benchmark.
- Design Constraints:Teams could use any agent framework, corpus version(s), retrieval strategy, tool-use setup, or human-in-the-loop workflow, so long as they used models from their assigned industry lab partner.
- Format:The competition consisted of six 15-minute rounds with 15 questions per round. Rounds became progressively harder over the course of the event.
- Scoring:Teams received 1 point for each correct answer. To incentivize low latency, they were also awarded a 0.25-point speed bonus if they were the first to answer a given question correctly. Points were worth 2x points in the final round, which consisted of the most challenging questions. Each team was also allowed 3 resubmissions throughout the competition, which they could choose to apply to correct a previous answer.

## Team Performance & Learnings

The competition made one thing clear: grounded reasoning over enterprise-style document corpora has improved since we released the OfficeQA benchmark 7 months ago, but it is still far from solved. The average team score was ~41%, while the top three teams exceeded 50% accuracy with the Stanford team winning the competition with 63.3% accuracy. These results point towards impressive work from top teams, as well as plenty of remaining headroom to explore.

### Winning Team Strategies

While each took a unique approach, several patterns emerged across the agents built by the top three teams. Strong systems tended to combine careful document preprocessing, targeted retrieval, structured tool use, and answer verification steps. In many cases, performance depended less on a single model call and more on the surrounding system: how documents were parsed, how evidence was retrieved, how intermediate calculations were performed, and how answers were verified before submission. While these were qualities the most performant systems generally had in common, they also each employed distinct and creative strategies, as described below.

![High level summary of winning team strategies.](/images/posts/b5764a15e895.png)

### 1st Place: Stanford University

![Stanford team’s winning approach](/images/posts/1885d82deae9.png)

[翻译失败，原文如下]

The Stanford team’s winning approach came from turning common grounded reasoning failure modes into reusable operating procedures for their Claude Opus 4.8 Claude Code agent to learn from and apply on the competition questions. During their development on the public OfficeQA benchmark, including experiments ablating with Opus 4.8 and even Fable 5 (while available), the team repeatedly traced wrong answers back to the agent’s exact misstep, and then turned those patterns into skills for table localization, answer formatting, clarifications on common financial wordings, etc. The team also integrated skills that would decide when to search across parsed corpus text and markdown-style document representations and when to fall back to the source PDFs if the parsed text lacked full context. By competition day, Stanford had prepared their agent with a playbook of ~100+ skills. They led all teams in accuracy in the 57 correct answers of 88 they attempted.

Despite this in-depth preparation, Stanford still had to adapt its strategy during the competition. In the first three rounds, the team used another Claude Code agent as a verifier to re-extract intermediate values, check common failure modes such as tracing revised values through data lineage and handling unit scaling, and patch calculations when it identified discrepancies. But after earning only two speed bonuses in those rounds, Stanford removed the extra verification pass for the final three. The change significantly reduced latency, helping the team earn speed bonuses on 14 questions and fuel its comeback. The verifier nevertheless proved decisive in the final round, when Stanford switched it back on to correct an answer through a final resubmission, ultimately securing their win.

### 2nd Place: UMass Amherst

![UMass winning approach](/images/posts/8aaec3d1e140.png)

The UMass team made a bet on speed. They used Claude Opus 4.8 Fast as their primary model and preprocessed the corpus to create a metadata catalog that enabled rapid search and filtering over parsed documents. To improve answer quality while preserving low latency, they ran three agents in parallel on each question, followed by a final Opus verification call to select the best answer.

This strategy gave UMass the fastest average submission time for correct answers: four minutes, less than half the team average of eight minutes and 30 seconds. As a result, they earned 36 speed bonuses, worth 0.25 points each, for being the first team to answer correctly, more than twice Stanford’s second-place total of 16. These bonuses helped them build a 10.25-point lead over Stanford by halftime and preserve a 3.75-point advantage entering the final round. UMass held that lead until the final 56 seconds of the competition, when Stanford’s slower, more accurate agent proved decisive on the most challenging questions and pulled ahead to win by 1.75 points.

UMass’s approach demonstrates how faster models, document preprocessing, and test-time scaling can work together to achieve very low latency without sacrificing too much accuracy.

### 3rd Place: Yale University

![Yale winning approach](/images/posts/1f2a97590d7c.png)

The Yale team built a multi-arm verification harness designed to remain robust when any individual agent failed. The system ran four independent arms in parallel, spanning two agentic strategies. Two arms used autonomous ReAct agents: one powered by Gemini 3.1 Pro and the other by Gemini 3.5 Flash. The remaining arms used a more structured planner-verifier pipeline, with Gemini 3.1 Pro powering all LLM calls. In this pipeline, the planner inspected and contextualized the source documents, assembling a scratchpad containing the evidence needed to answer the question. The verifier then checked the cited sources and performed the final calculations.

A Gemini 3.1 Pro meta-verifier reviewed the answers and reasoning produced by all four arms and selected the final response. To reduce the risk of introducing a new unsupported answer, the meta-verifier could only select an answer proposed by one of the existing arms. When it could not do so, the system fell back to a majority vote. By combining distinct agent architectures with independent, partially decorrelated failure modes, Yale emphasized consistent, grounded verification. The approach earned the team third place, with 49 of 90 questions answered correctly and a top-three correctness ranking in four of the competition’s six rounds.

### Summary of Winning Team Strategies

One of the core takeaways from these winning approaches is that applying an agent successfully to end-to-end grounded reasoning tasks requires holistic systems thinking, rather than model choice alone. Across the winning approaches, a few key design levers stood out as especially important:

- Parsing quality:Top teams used pre-parsed documents and often augmented these parsed representations to include additional metadata (e.g. descriptions of charts or page level metadata) and preserved paths back to source PDFs to fall back to when parsed text was incomplete. In our own studies on OfficeQA Pro V2, we find that pre-parsing documents withai_parsecontributes significantly to Genie’s performance improvement of 24.0 pt over baseline frontier agents.
- Retrieval quality:Strong systems didn't rely on generic top-k chunk search. They instead used some form of lexical retrieval (e.g. grep), often paired with dense retrieval for a hybrid approach.
- Tool use:Successful agents generally delegated search, document inspection, calculations, comparison, and submission to specialized tools.
- Verification strategies:Several teams built in some form of explicit verification check via a verification agent or LLM call to boost answer quality.
- Robust harness:Under live deadline pressure, operational details like preprocessing, retry logic, parallelism, and submission scaffolding were necessary to ensure correct answers actually made it through in time.

These factors determined whether the model could reliably find the right evidence, perform the right calculation, and submit the right answer under deadline pressure.

## Impact and Next Steps

In summary, the results of the Grounded Reasoning Cup demonstrate a number of broader lessons:

- Generalization must be tested, not assumed.Improvements on OfficeQA did not always transfer to OfficeQA Pro V2, and frontier agents still answered fewer than half of its questions correctly on average. Progress on a familiar benchmark does not necessarily translate to a new corpus or task distribution.
- Representative, held-out evaluations are critical.They should evaluate the forms of generalization that matter, ideally keeping core qualities of the task fixed (i.e. grounded reasoning over documents), while varying elements of the task that can change, like the corpus. In our post describing OfficeQA Pro V2, we discuss how we leverage synthetic data, combined with our knowledge of customer workflows, to scale these representative evaluations quickly.
- Agent performance depends on the full system.Performance depends not only on the model, but also on parsing, retrieval, tool use, verification, and the quality of the underlying data and infrastructure. Winning teams optimized these components holistically. Similarly,Genie significantly outperforms baseline frontier agentswhen using tools likeai_parseto pre-parse documents, and additional harness optimization strategies.

[翻译失败，原文如下]

We are grateful to all of the teams and industry sponsors, including OpenAI, Google DeepMind, and Anthropic, who participated in Databricks’s inaugural Grounded Reasoning Cup and helped push the field forward. We also thank USAFacts for their continued partnership, from helping us identify a new corpus and create relevant questions for OfficeQA Pro V2, to partnering with us on the competition itself. Finally, we thank the U.S. Treasury for helping identify the U.S. Accounts of Receipts and Expenditures as the foundation for the competition benchmark, and for releasing the dataset as a cohesive collection for the first time.

Authors: Krista Opsahl-Ong, Arnav Singhvi, Josh Joseph, Jasmine Collins, Ivan Zhou, Brooke Wenig, Denny Lee, Michael Bendersky, Erich Elsen, Xing Chen, Matei Zaharia

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Evaluating AI Agents Live at the Grounded Reasoning Cup](https://www.databricks.com/blog/evaluating-ai-agents-live-grounded-reasoning-cup)
> 
> 翻译时间：2026-08-19 03:08
