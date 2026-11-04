---
title: 'CWE-bench v2: More coverage, quality, and transparency'
title_original: 'CWE-bench v2: More coverage, quality, and transparency'
date: '2026-11-03'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/cwe-bench
author: ''
summary: '[翻译失败，原文如下]


  # CWE-bench v2: More coverage, quality, and transparency


  CWE-benchis designed to test the limits of frontier cyber capabilities. In our ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-04T08:50:29.600150'
---

[翻译失败，原文如下]

# CWE-bench v2: More coverage, quality, and transparency

CWE-benchis designed to test the limits of frontier cyber capabilities. In our continued pursuit to push the horizon atCollinear AI, CWE-bench v2 opens up apublic set of 100 tasksthat anyone can run and evaluate their models on. The setup is the same as before. An agent gets a checkout of a real open-source repository and a short instruction, with the goal of finding and fixing a security weakness without breaking existing functionality. Scoring is fully programmatic, so results are deterministic and anyone can reproduce them without extra cost. All our programmatic checks have been curated with the help of LLM judge panels that shape them towards the direction of hardness and fairness. We also maintain aheld-out set, so that we can keep tracking progress on tasks no model has seen. To evaluate your model on the held-out set, contactcyber@collinear.ai.

Our goal is to be exhaustive. A defender has to anticipate the ways an attacker could get in, and get it right every single time. These 100 tasks cover 91 different CWEs, spanning a wide range of vulnerability classes. A model that does well here has to understand the multiple weakness surfaces that a potential attacker can exploit. Recognising a familiar pattern is not enough.

As part of our meticulous effort to keep improving quality, for every task we checked that the following questions were true:

- Does the instruction read like a realistic instruction and not an evaluation setting?
- Can every graded behaviour be inferred from the instruction?
- Does the verifier check for correct behaviour and not for specific structure of one fix?
- Does the starter code fail and the reference fix pass?
- Does the original functionality still work with the new fix?
- Do the verifiers fail memorized solutions like the known upstream patch?

Every task was also reviewed by hand. Open-sourcing the set is part of the same effort to improve quality. We welcome feedback on any task, and contributions to the public set.

## Results

Results are tracked in two places on the Hub. Theleaderboard on the CWE-bench dataset pagecovers open-weight models and updates on its own: labs and the community add a result by opening a PR on the model's repo with a results file (how). For the full comparison, including API-only models such as Gemini, Claude and GPT, see theCWE-bench leaderboard Space, where new models are added through a PR on the Space.

Open-weight models, from the dataset page:

All evaluated models, including API-only ones:

Of the 11 models evaluated, Gemini 4 Argon leads with 67.8% pass@1 and 81.0% pass@4, just ahead of Claude Opus 5.5 (67.3% pass@1, 78.0% pass@4). 95 tasks are solved by at least one model, an indication that the tasks are indeed solvable. However, even the leader fails 19% of the set on every attempt, so the long tail is far from solved. The public set, the grader and the harness are open. Run your model, and tell us where it stands.

![CWE-bench v2: pass@1 against average cost per rollout, with the Pareto frontier](/images/posts/687a322c7c97.png)

On cost, DeepSeek V4.1 Flash (1017), Claude Opus 5.5 and Gemini 4 Argon form the Pareto frontier: DeepSeek reaches 57.0% pass@1 at $0.04 per rollout, Opus adds ten points at $1.83, and Gemini edges ahead at $3.92.

## Run it from the Hub

Every task is a self-containedHarbortask (a Dockerized environment, an instruction, and a deterministic verifier), and the dataset ships aregistry.json. Harbor can therefore run the whole benchmark straight from the Hugging Face repo, without cloning anything yourself:

```bash
harbor run --repo "https://huggingface.co/datasets/collinear-ai/cwe-bench" -d cwe-bench@2.0 -k 4 \
  --agent <agent> --model <model> --env docker \
  --allow-agent-host <model API host>

```

-k 4runs 4 attempts per task, and the reported score is the mean reward over all 400 trials. The dataset is gated: accept its access conditions on thedataset pagefirst. Harbor fetches the tasks with git, so also save your HF token to git's credential helper once:

```bash
hf auth login --token $HF_TOKEN --add-to-git-credential

```

The tasks are also taggedrl-environment: the same environments and verifiers can provide rewards for training defensive agents, not just for evaluating them.

---

> 本文由AI自动翻译，原文链接：[CWE-bench v2: More coverage, quality, and transparency](https://huggingface.co/blog/cwe-bench)
> 
> 翻译时间：2026-11-04 08:50
