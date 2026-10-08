---
title: Welcome RL Environments to the hub
title_original: Welcome RL Environments to the hub
date: '2026-09-28'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/rl-environments
author: ''
summary: '[翻译失败，原文如下]


  # Welcome RL Environments to the hub


  Reinforcement Learning environments give new capabilities to agentic AI systems,
  and they’re a grea...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-08T08:39:23.700830'
---

[翻译失败，原文如下]

# Welcome RL Environments to the hub

Reinforcement Learning environments give new capabilities to agentic AI systems, and they’re a great way to measure and improve performance in your agents. Therefore, Hugging Face Hub now has a special place for RL Environments.

An environment gives an agent a task, responds to its actions with observations, and scores the outcome. The resulting rewards can measure an agent's performance during evaluation or provide a learning signal during training. For an introduction to this interaction loop, seeour blogpost on environments. Within the environment, the agent will perform a set of tasks that are represented as datasets. Therefore, environments can be split into broadly two parts: tasksets and runtimes. In this release, we are focusing on the tasksets.

![Browsing the RL Environments filter on the Hugging Face Hub](/images/posts/8f82840ad840.gif)

An RL environment on the Hub is a dataset repo that shows up in the newRL Environments filter. TheUse this datasetbutton gives you the command to run it in that framework. There is no new repo type, no registry, and no sign-up. There are already environments in Harbor, Verifiers, and NVIDIA NeMo Gym.

## Stop building environment registries

Every RL paper or framework uses its own way to find environments. Custom hubs, runtime registries, independent task datasets, or a GitHub list of tasks with a custom loader. This means that many of the published environments are siloed: if you publish an environment for one framework, users of the other three can’t load it. If you want to train on an environment from another framework or a new paper, you’ll need to port it by hand.

We think this is the wrong shape. An environment is tasks, tests, containers, and a reward rule, which are data with a runtime on top. The Hub already stores data, versions it, gates it, previews it, and serves it to millions of people. It does not need a second system to hold environments. It needs a way to say "this data is an environment, and here is how you run it."

The frameworks keep doing what they are good at. The Hub does what it is good at, which is hosting, discovery, and versioning. Nobody has to own the catalogue. In fact, catalogues can run on other platforms too, powered by the hub.

The dataset repository hosts your environment files. The framework runs them locally or on a supported cloud backend.Hugging Face Jobscan run cloud workloads, andHugging Face Sandboxes, built on Jobs, provide interactive command execution. The tags describe compatibility and generate loading commands; adding a tag does not start a job or sandbox.

## What shipped

The RL Environments filter.Go tohuggingface.co/datasets?other=rl-environment. Every dataset with therl-environmenttag appears there, whatever framework it works with.

Framework tags.Four environment frameworks are registered as dataset libraries:

Each framework tag puts the framework's icon on the dataset page and adds a generated snippet toUse this dataset.

A dataset can carry more than one framework tag. That is the point. Tags describe compatibility, and compatibility is not exclusive. Each listed framework must support the files in the repository; adding a tag does not convert them.

## Run an environment and inspect its reward

Choose the example for your framework and run it in a separate Python environment with the prerequisites listed below.

### Harbor: run a reference solution

Harborcan load task directories from a Hub repository. The oracle agent runs the task's reference solution, then the verifier scores the result. It does not call a model.

```sh
uv tool install --python 3.13 'harbor==0.21.0'
harbor run \
    --repo https://huggingface.co/datasets/harborframework/terminal-bench-2.1 \
    --dataset terminal-bench-2.1@2.1.0 \
    --include-task-name '*regex-log' \
    --agent oracle --env docker --jobs-dir results/harbor
harbor view results/harbor

```

The viewer shows the task's reward, verifier output, and logs. This checks the task and its reference solution before you try a model agent.

### Verifiers: run a model on the same task

The Harbor integration ofverifiers v1can run the same task directories in different runtimes, such as Docker. It also supports different harnesses, including a minimal bash harness.

```sh
uvx --python 3.13 --from 'verifiers[harbor]' eval harbor \
    --env.taskset.repo https://huggingface.co/datasets/harborframework/terminal-bench-2.1 \
    --env.taskset.dataset terminal-bench-2.1@2.1.0 \
    --env.taskset.tasks '["regex-log"]' \
    --env.agent.runtime.type docker \
    --env.agent.harness.id bash \
    --model "$MODEL" \
    --client.base-url "$LLM_URL"

```

Here repo is the full Hugging Face Git URL, while dataset is the name and version in that repo's registry.json. This loader uses Harbor's registry conventions, so a bare Hub repo ID cannot replace both values.

### OpenEnv: run an agent and inspect its reward

OpenEnv's Harbor integrationcan run the same task directories with an agent such as OpenCode and return the verifier's reward alongside the agent's trace.

```sh
pip install "openenv[harbor]==0.7.0"

openenv harbor rollout \
    --llm-url "$LLM_URL" \
    --model "$MODEL" \
    --dataset harborframework/terminal-bench-2.1 \
    --task-index 0 \
    --harness opencode \
    --sandbox docker \
    --out rollout.json

```

The command downloads the dataset'stasks/directories, runs one task in Docker, and writes the result. The default connection uses a temporary Gradio tunnel so the sandboxed agent can reach OpenEnv's model proxy. Read the verifier result and the number of model calls:

```py
import json
from pathlib import Path

result = json.loads(Path("rollout.json").read_text())[0]
print("Reward:", result["reward"])
print("Model calls:", result["n_turns"])
print("Error:", result["error"])

```

A reward ofNonemeans no verifier reward was produced; inspecterrorbefore interpreting the run as a model failure. This path expects Harbor task directories.

### NeMo Gym: generate responses and inspect rewards

NeMo Gymsupports evaluation and RL training: its environments collect trajectories and compute rewards, while a training framework updates model weights. For example, theStructured Outputs datasetpairs prompts with JSON schemas. Its verifier rewards schema adherence; it does not check whether the generated content is factually correct.

The best part is that this gives one repo and one discussion tab where people report broken tasks from all major frameworks. So when an author fixes a bad test, every framework gets the fix on the next pull.

## Tag your environment

Open your dataset card and add this to the YAML header:

```
---
pretty_name: Terminal-Bench 2.0
tags:
- rl-environment
- harbor
- verifiers
---

```

That is the whole integration. Keeprl-environment, then list every framework that can load your files. If your environment works with a framework we have not registered yet, open a PR to thelist of supported libraries.

Thedocshave the full reference.

## Already on the Hub

We opened PRs to tag some of the environments people already train on. If you maintain one of these, merge the PR and your environment shows up in the filter.

Harbor

- BeyondSWE: the BeyondSWE benchmark as Harbor task directories, one folder per instance.
- Terminal-Lego: Terminal-Bench-style tasks built from real StackOverflow issues, kept only after Docker round-trip verification.
- Harbor-Mix: 100 hard agentic tasks picked from the Harbor adapters pool, cheaper to run than a full multi-benchmark sweep.
- NatureBench: the 90 NatureBench tasks prebuilt for Harbor.

Verifiers

[翻译失败，原文如下]

- Reverse-Text-RL: the small reversal task prime-rl uses in CI to debug RL training.
- Multi-SWE-RL-Verified: 2,232 of 4,703 Multi-SWE-RL rows that pass gold-patch validation across C, Go, Java, JavaScript, Rust, and TypeScript.
- R2E-Gym-Subset-Verified: a verified R2E-Gym subset.
- Scale-SWE-Verified: 17,202 of 20,181 Python issue-resolving tasks that give a clean reward signal end to end.

NeMo Gym

- Workplace Assistant: a multi-step tool-use sandbox with five databases, 26 tools, and 690 business tasks.
- Structured Outputs: instruction following with structured outputs.
- CFBench: multilingual constraint following.
- SysBench: multi-turn system message following.

## What comes next

The first version generates onedefaultsnippet per framework. Per-config snippets are next, so a repo with several task sets can show the right command for each. After that we will look at structural detection for frameworks with strict layouts. It would also be really cool build custom task UIs, we’ve been experimenting with this here:

The bigger goal is for framework tagging to be automatic everywhere. OpenEnv already does it on upload. If you maintain Harbor, Verifiers, Nemo Gym, or any other environment framework, add the tags in your push path. It is a few lines, and every environment your users publish becomes visible to everyone else.

If you train agents, go browse thefilter. If you build environments, publish and tag them, whether they cover coding, tool use, games, robotics, or another task. Include the files, a working run command, and the rule that produces the reward so others can use them. If your framework is missing, contribute it to thelist of supported libraries.

---

> 本文由AI自动翻译，原文链接：[Welcome RL Environments to the hub](https://huggingface.co/blog/rl-environments)
> 
> 翻译时间：2026-10-08 08:39
