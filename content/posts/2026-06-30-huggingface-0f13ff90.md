---
title: Hugging Face模型页全面集成评估结果
title_original: Featuring Every Eval Ever Results on Hugging Face Model Pages
date: '2026-06-30'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/eee-community-evals
author: ''
summary: 文章介绍了“每个评估结果”（EEE）项目与Hugging Face社区评估的互通。EEE作为EvalEval联盟项目，提供标准化的JSON模式记录评估结果，涵盖运行者、模型、生成设置等关键信息。Hugging
  Face社区评估则通过YAML文件在模型页面和基准排行榜上展示分数。两者结合后，贡献者可将EEE记录自动转换为Hugging Face格式，结果带有来源标记和验证标识，解决了评估结果分散、格式不统一、难以复现的问题，提升了AI评估的可信度和可用性。
categories:
- AI基础设施
tags:
- 评估标准化
- Hugging Face
- 模型评估
- 开源工具
- AI治理
draft: false
translated_at: '2026-07-01T06:48:17.689487'
---

# 每个评估结果现已登上 Hugging Face 模型页面

每个评估结果（EEE）与 Hugging Face 社区评估现已实现互通。我们支持评估结果的交叉发布与解读，同时链接到开源模型、排行榜以及统一的标准化元数据存储库。

EEE 于 2026 年 2 月作为 EvalEval 联盟的一个项目启动，这是首个跨机构合作项目，旨在改善 AI 评估结果由第一方和第三方评估者报告的方式。Hugging Face 于 2026 年 2 月推出了社区评估，旨在将 Hub 上基准分数的报告方式去中心化。两者结合，弥补了用户、研究人员和政策制定者在信任、理解和选择评估与模型方面的缺口。

评估结果是我们衡量模型能力、对比模型优劣以及推理安全与治理的方式，然而它们却分散且难以比较。它们存在于论文、排行榜、博客文章和测试日志中，各有各的格式。同一模型在同一基准上，因运行者和运行方式不同，往往返回不同的分数；例如 LLaMA 65B 在 MMLU 上的报告分数既有 63.7 也有 48.8。这些差异可能源于我们发现的通常未被报告的评估设置。

EEE 是我们针对报告端的解决方案。它是一个用于评估结果的 JSON 模式，记录以下内容：

- 谁运行的
- 哪个模型
- 如何访问的
- 生成设置
- 指标的实际含义
- [推荐] 每个样本输出的配套 JSONL 文件

该模式是在研究人员和政策研究人员的反馈下构建的，可接收任何来源的结果，因此测试日志、排行榜抓取数据和论文数据最终都能统一格式。GitHub 仓库提供了转换器、示例和贡献指南。自发布以来，Hugging Face 上的数据存储库已增长至约 229,000 条评估结果，涵盖超过 22,000 个模型和 2,200 个基准，来自 31 种不同的报告格式。仅从头复现这些运行就需要数十万美元的成本，这充分说明了数据一旦有人付费生成就不应再分散的理由。

了解更多关于该模式及如何贡献的信息，请点击此处。

现在，它带来了更好的集成和归属功能。贡献者现在可以将 EEE 结果发送到 Hugging Face 社区评估。我们构建了一个转换器，可获取您的 EEE 记录并生成 Hugging Face 所需的小型 YAML 文件，这样您就不必手动以两种格式维护同一结果。

![评估卡上的已验证评估者](/images/posts/bcd5f3cc5476.gif)

这是面向所有报告或阅读评估的用户的新功能，不仅限于现有的 EEE 贡献者。报告自身模型的第一方评估者和报告他人模型的第三方评估者都可以向社区评估和 EEE 提交数据，而浏览 Hub 的任何人都能获取追溯到完整记录的结果。当您通过所在组织的官方 Hugging Face 账户提交数据时，您的结果将在 EvalEval 上显示已验证的勾选标记，向读者表明这些数字直接来自源头。本文其余部分将介绍什么是社区评估以及转换器的作用。

## Hugging Face 社区评估如何与 EvalEval 协同工作

Hugging Face 社区评估包含两个方面。

基准存在于一个数据集仓库中，该仓库通过添加 `eval.yaml` 进行注册。注册后，该数据集页面会收集并显示 Hub 上针对该基准报告的所有分数的排行榜。官方基准列表会随时间增长。

模型的分数存在于模型仓库内的 `.eval_results/*.yaml` 中。它们会显示在模型卡上，并汇入匹配的基准排行榜。模型作者自身的结果以及通过拉取请求提交的其他人的结果都会被汇总，每个分数都带有标记，标明是作者提交、社区提交还是独立验证。任何人都可以通过提交包含正确 YAML 文件的 PR 为任何模型添加分数，模型作者可以关闭 PR 或在其自己的仓库中隐藏结果。

以下是其中一个排行榜的示例：

Hub 上人类最后考试的社区评估排行榜

这就是 EEE 和社区评估的结合点。当您将结果同时发送给两者时，会发生两件事：首先，您的分数会出现在 Hugging Face 模型页面上，并被拉入基准的排行榜。其次，它会带有一个来源标记，直接链接回完整的 EEE 记录，其中包含生成配置、测试版本、可复现性说明以及任何实例级数据。

![SmolLM2 模型页面上的 EvalEval 来源](/images/posts/ac18543cf038.png)

来自 EEE 数据存储库 (a) 的评估（MMLU-Pro）在文件级别交叉链接到 Hugging Face 模型卡 (b)。来源 EvalEval 标记链接到完整的 JSON 记录。

两个目标服务于同一个目标的不同方面。Hugging Face 将您的结果放在人们查看模型的地方，并附上指向来源的链接。EEE 则保留完整的结构化记录，使结果可解读，并在此基础上驱动评估卡。将数据同时发送给两者，同一评估即可同时可见且可读，这正是报告评估的意义所在。

您可以在下方看到这种交叉兼容性。上面模型卡上显示的相同 GPQA 分数也会在评估卡中呈现，评估卡将 EEE 运行数据与基准和模型元数据组合成一个可解读的记录。同一评估，不同展示面：

## 工作原理

Hugging Face 将评估分数以 YAML 格式存储在模型仓库的 `.eval_results/` 目录下。必填字段仅为基准数据集、任务和数值。来源块是创建指向 EEE 反向链接的部分。

```
- dataset:
    id: openai/gsm8k
    task_id: gsm8k
  value: 96.8
  date: '2024-07-16'
  notes: '8-shot CoT'
  source:
    url: https://huggingface.co/datasets/evaleval/EEE_datastore/blob/main/flat/objects/<xx>/<yy>/<uuid>.json
    name: EvalEval

```

转换器会根据您现有的记录填充这些内容。它将 `source_data.hf_repo` 映射到 `dataset.id`，将 `evaluation_name` 映射到 `task_id`，将 `score_details.score` 映射到 `value`，将 `evaluation_timestamp` 映射到 `date`，然后将数据存储对象 URL 作为指向每条记录 EEE JSON 的来源链接插入。它目前支持四个官方基准：MMLU-Pro、GPQA、HLE 和 GSM8K。

转换器所做的不仅仅是重塑字段。您将其指向一个 EEE 数据存储集合，它会下载该集合及其引用的记录，检查对象哈希值，并找到映射到受支持基准的分数。在写入任何实时内容之前，它会审计已存在的内容：它读取模型主分支和开放 PR 中的每个 `.eval_results` YAML，并按数据集和任务进行比较，而不是按文件名。如果分数已存在，则标记为 `already_present`；如果存在不同的分数，则标记为 `score_conflict`；如果模型仓库在 Hub 上无法解析，则标记为 `missing_hf_model`。其他所有内容均标记为 `ready`。

未经您的确认，不会推送任何内容。该工具会写入本地 YAML 预览和可供您检查的审核文件，显示哪些已就绪、哪些需要注意的报告，并且仅在您输入 `OPEN PRS` 并输入提交消息后才会打开 PR。重新运行会重用集合的缓存结果，除非您传递 `--force` 参数。

![转换器的 TUI](/images/posts/f03de01b9717.png)

转换器的审核步骤。排除的条目（此处为没有匹配 Hub 仓库的模型）会列出其 EEE 来源 URL，就绪的 PR 等待明确的 OPEN PRS 确认。

## 从这里开始

将您的完整记录提交到 EEE 数据存储库。

使用 EEE 仅需额外一步，而转换器可大幅自动化完成。社区评估转换器工具可在 GitHub 仓库中找到。要处理一个集合，请执行以下操作：

```shell
uv run tools/hf-community-evals/community_evals_converter.py MMLU-Pro \
  --datastore evaleval/EEE_datastore@main

```

预览生成的报告，确认无误后输入`OPEN PRS`即可提交。关于模式、CLI和转换器的完整文档，请访问evalevalai.com/every_eval_ever/hf-community-evals。

---

> 本文由AI自动翻译，原文链接：[Featuring Every Eval Ever Results on Hugging Face Model Pages](https://huggingface.co/blog/eee-community-evals)
> 
> 翻译时间：2026-07-01 06:48
