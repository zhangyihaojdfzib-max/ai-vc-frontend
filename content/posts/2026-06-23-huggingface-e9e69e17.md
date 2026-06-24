---
title: 每周发布huggingface_hub：AI与人工审核的协作实践
title_original: Shipping huggingface_hub every week with AI, open tools, and a human
  in the loop
date: '2026-06-23'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/huggingface-hub-release-ci
author: ''
summary: 本文介绍了Hugging Face团队如何通过GitHub Actions工作流实现huggingface_hub的每周发布。旧流程每4-6周发布一次，手动操作繁琐，尤其是编写发布说明耗时费力。新流程将机械性步骤完全自动化，并利用开源AI模型起草发布说明和公告，但保留人工审核以确保准确性。整个技术栈基于开放工具和开放权重模型，无需闭源API或专有平台，旨在让其他维护者也能复用。文章详细描述了流水线设计原则和具体步骤，展示了AI与人类判断力结合的高效发布模式。
categories:
- AI基础设施
tags:
- huggingface_hub
- 自动化发布
- AI辅助
- 开源工具
- 人工审核
draft: false
translated_at: '2026-06-24T06:08:56.198778'
---

# 每周发布 huggingface_hub：AI、开源工具与人工审核相结合

huggingface_hub 是 Hugging Face 生态系统底层的 Python 客户端。transformers、datasets、diffusers、sentence-transformers 以及数十个其他库都依赖它与 Hub 进行通信。如果我们每周不发布新版本，就意味着修复和功能更新被卡在 main 分支上。

很长一段时间里，我们每 4 到 6 周发布一次。现在，我们通过一个 GitHub Actions 工作流实现每周发布。我们使用开源工具和开放权重模型构建了这一流程，并在需要判断力的环节保留了人工审核。本文中没有任何内容需要供应商合同、闭源模型或你无法自行运行的基础设施。这从一开始就是我们的设计目标，因为我们希望其他维护者能够借鉴并适配这一工作流。

读完本文，你将掌握构建自己版本所需的一切。

## 我们的起点

旧流程是部分自动化、大部分手动的。

已在 CI 中的部分：
- 推送标签后自动发布到 PyPI。
- 在下游库中打开测试分支，并固定候选版本。

每次仍需手动操作的部分：
- 创建发布分支，更新 `__init__.py` 中的版本号，提交、打标签、推送。
- 监控下游 CI 运行并分类处理失败情况。
- 阅读自上次发布以来合并的所有 PR，手动编写发布说明：按主题分组，提供上下文，用不像 git log 转储的语言撰写。
- 在候选版本期结束后发布稳定版本。
- 起草内部 Slack 公告和社交媒体帖子。
- 打开发布后 PR，将 main 分支更新到下一个 dev0 版本。

为新版本撰写好的发布说明是最繁重的部分，需要汇总涉及不同主题的数十个 PR。技术上并不困难，但需要数小时的专注注意力。再加上公告环节，一个小版本更新很容易变成分散在几天内的半天工作量。

## 两类工作

因此，我们决定简化整个流程。审视上述列表，工作可分为两类。

有些步骤纯粹是机械性的，可以自动化：更新版本号、提交、打标签、推送、打开下游测试分支、打开发布后 PR。这些步骤不需要思考，只需每次按正确顺序执行——这正是 CI 工作流擅长的。

其余部分则不同。编写发布说明、决定突出哪些内容、以面向人类受众的方式撰写公告：这些是脑力工作。正是这种判断力让发布流程多年来一直保持手动。这就是 AI 的用武之地，它能在几秒钟内将空白页面变成扎实的初稿。但我们也需要谨慎，因为一份看似自信却暗藏错误的草稿比没有草稿更糟糕。

## 设计原则：开放组件，人人可复用

当我们决定解决这个问题时，设定了一个前置约束：每个活动部件都必须能让任何维护者自行运行。不能使用我们无法替换的闭源模型 API，不能使用专有发布平台，不能有秘密配方。

以下是整个技术栈：

第二个原则：模型起草，人类决策。语言模型擅长将三十个简洁的 PR 标题转化为可读的发布说明。但它们不适合被盲目信任。因此，工作流采用人工监督方式：模型进行初稿，确定性脚本检查其工作，人类在发布前进行审核和编辑（下文详述）。

## 流水线概览

完整工作流是一个文件 `.github/workflows/release.yml`，通过 Actions UI 手动触发。它只接受一个输入：

```yaml
on:
  workflow_dispatch:
    inputs:
      release_type:
        type: choice
        options:
          - minor-prerelease   
          - minor-release      
          - patch-release      

```

此后，任务大致按以下顺序运行：

- **准备**。计算下一个版本号，创建或复用发布分支，更新 `__version__`，提交、打标签、推送。
- **发布到 PyPI**。构建并上传 `huggingface_hub`。同时，将 `hfCLI` 作为独立的 PyPI 包构建并上传。
- **发布说明**。对比自上次标签以来的提交范围，从 GitHub API 拉取 PR 元数据，让模型起草结构化的变更日志（这是最近的一份）。保存为草稿版 GitHub 发布。
- **下游测试分支**。对于候选版本，在 `transformers`、`datasets`、`diffusers`、`sentence-transformers` 中打开分支并固定候选版本，以便它们的 CI 能快速告知我们是否破坏了某些功能。
- **Slack 公告**。阅读发布说明，以我们团队的风格生成内部公告。
- **归档说明**。将原始 AI 草稿和人工编辑版本并排上传到 Hugging Face Bucket。
- **发布后版本更新**。稳定版本发布后，在 main 分支上打开 PR，更新到下一个 dev0 版本。
- **在已发布的 PR 上评论**。在发布中包含的每个 PR 上留下"此内容已在 vX.Y.Z 中发布"的评论。
- **同步 CLI 文档**。在我们的 skills 仓库中打开 PR，更新重新生成的 hfCLI 技能文档。
- **报告到 Slack**。每个步骤将其状态发布为线程回复；最后一个任务用 ✅ 或 ❌ 更新根消息。

剩余的手动步骤是审核和发布草稿版发布说明，以及审核和发布内部 Slack 消息。这两个步骤是我们希望保留人工审核的环节。

## 信任但验证：人工审核的核心

以下是每个人对 AI 生成的发布说明的担忧：模型悄悄遗漏了一个 PR，或者凭空捏造了一个不属于本次发布的 PR。一份几乎正确的变更日志比没有变更日志更糟糕，因为没人会重新检查它。

我们不信任生成的发布说明在第一次尝试时就完整无缺，而是通过确定性方式验证。在模型运行之前，一个 Python 脚本会检索属于本次发布的所有 PR，并将其存储为基准事实。

```python

PR_NUMBER_PATTERN = re.compile(r"\(#(\d+)\)$")

pr_numbers = [
    int(m.group(1))
    for commit in commits_since_last_tag
    if (m := PR_NUMBER_PATTERN.search(commit.title))
]
save_manifest(pr_numbers)  

```

然后模型根据这些 PR 起草发布说明。完成后，我们将其输出与初始 PR 列表进行比对：

```python
expected = set(load_manifest())          
found    = extract_pr_refs(notes_md)     

missing = expected - found               
extra   = found - expected               

```

如果有遗漏或多余的内容，我们不会失败，也不会发布错误的文件。我们会将差异反馈给 Agent，并要求它仅修复这些 PR：

```python
for _ in range(MAX_ITERATIONS):
    missing, extra = validate(notes)
    if not missing and not extra:
        break  
    run_agent_fix(missing_prs=missing, extra_prs=extra)

```

这就是让整个流程值得信赖的模式：一个非确定性模型被包裹在确定性护栏中。模型擅长撰写文字，但不擅长做到详尽无遗。因此，我们让它写作，让代码强制执行一致性。

## 约束模型，防止捏造

完整性是一方面，准确性是另一方面。一个仅根据 PR 标题进行总结的模型会愉快地编造出与实际 API 不符的代码示例。

为防止这种情况，我们在获取 PR 元数据时，还会拉取每个 PR 的实际文档差异：该 PR 修改的 `docs/` 目录下任何 `.md` 文件的统一差异。

```python
def fetch_doc_diffs(pr):
    return [
        {"filename": f.filename, "status": f.status, "patch": f.patch}
        for f in pr.get_files()
        if f.filename.startswith("docs/") and f.filename.endswith(".md") and f.patch
    ]

```

该差异会进入模型的上下文，这样当它写"以下是新的 CLI 命令"时，引用的是 PR 作者在文档中实际编写的示例。这与之前的逻辑相同：给模型真实的源材料和一个明确的任务。

提示词本身以技能的形式存在：即仓库中的小型Markdown文件（SKILL.md加上参考模板）。发布说明技能详细说明了如何挑选亮点、如何组织章节结构、何时添加文档链接等。它读起来就像入职指南，而这正是最恰当的思维模型。

## 人工检查点

在RC（候选版本）发布后，草稿版的GitHub发布页面会保留AI的初稿内容。这时就需要人工介入了：

1. 审阅者阅读草稿，调整语气和重点，修正模型过度强调或忽略的内容。
2. 只有在完成上述修改后，才会触发`minor-release`运行，将RC升级为正式版本。

审阅者的时间用于打磨优化，将半天的写作工作缩短为十五分钟的编辑环节。

我们还保留了改进过程的书面记录。我们将两个文件并排归档到Hugging Face存储桶中：一个是原始的AI草稿（在RC阶段、任何人修改之前上传），另一个是人工编辑后的版本（在最终版本发布时上传）。

```bash

hf cp release_notes_raw.txt    "hf://buckets/huggingface/releases/huggingface_hub/${V}/release_notes_raw.txt"


hf cp release_notes_edited.txt "hf://buckets/huggingface/releases/huggingface_hub/${V}/release_notes_edited.txt"

```

每周收集这两个文件，我们就能积累一个不断增长的"模型写了什么"与"我们希望它写什么"的对比数据集。这个数据集随后可用于更新Agent（智能体）的技能。

## 开放且安全的管道

重构发布流程也是加强安全性的好机会，特别是针对供应链攻击。

无PyPI令牌。发布采用可信发布机制：PyPI验证GitHub为此特定工作流生成的短期OIDC令牌，并为每个制品签发PEP 740认证/Sigstore来源证明。没有需要泄露或轮换的长期密钥。

```yaml
permissions:
  id-token: write       
  attestations: write   

- uses: pypa/gh-action-pypi-publish@v1.14.0
  with:
    attestations: true  

```

Agent（智能体）运行时被固定并经过验证。我们不会直接`curl | bash`最新版的OpenCode然后碰运气。我们固定一个版本并在运行前检查其SHA256值：

```bash
curl -fsSL https://opencode.ai/install | bash -s -- --version "${OPENCODE_VERSION}"
echo "${OPENCODE_SHA256}  $(which opencode)" | sha256sum -c -

```

开放工具并不意味着可以粗心大意地使用工具。

## 那么，成本是多少？

几乎为零。一次完整的发布（包括发布说明和Slack公告，涉及20-40个PR和几轮提示词交互）在推理提供商上的花费约为0.25美元。采用按需付费的开源权重计费模式，每周唯一真正的问题是"是否有值得发布的内容？"，而答案总是肯定的。

## 实际发生了什么变化

发布节奏从每4到6周一次变为每周一次。有趣的是那些次要影响：

- 发布说明质量提升而非下降。初稿始终存在，因此审阅时间用于打磨。分组更加一致，遗漏的内容也更少。
- 问题更早暴露。每个RC的下游测试分支能在候选窗口期间捕获集成问题。
- 贡献者反馈周期缩短。自动生成的"已在vX.Y.Z版本中发布"评论的重要性超出了我们的预期。当有人在已关闭的PR上报告问题时，每个人都能立即看到修复包含在哪个版本中。过去这需要手动查找标签。

## 让它为你所用

这是最让我们在意的部分。工作流围绕`huggingface_hub`设计，但其结构具有通用性。

几乎可以直接复用的部分：

- 触发器和版本号更新逻辑（`minor-prerelease` -> `minor-release` -> `patch-release`）。
- 信任但验证的循环：确定性清单、模型草稿、验证、重新提示。这是可迁移的核心思想，与你生成的内容无关。
- OIDC可信发布、固定并校验和验证的运行时、Slack线程。
- 基于技能的提示词：替换模板，保留结构。

特定于我们的部分：

- 下游仓库列表及其依赖固定格式。
- 技能中精确的章节分类和语气。
- Slack和存储桶的目标地址。

要适配它：fork工作流文件和脚本，指向你的包，根据你项目的风格重写技能Markdown文件，设置两个仓库变量（模型ID和你的OpenCode版本），在PyPI上设置可信发布，如果没有下游测试则删除下游测试任务。信任但验证的循环是值得原样复用的部分。正是它让生成的制品可以安全发布。

## 下一步计划

- 自动分类下游失败。目前工作流会创建测试分支，由人工查看CI结果。一个明显的下一步是检查失败的日志，并在内部Slack消息中报告它们。
- 扩展该模式。大部分内容都是通用的。我们预计将在生态系统的其他Python库中大量复用这些部分。

## 要点

发布流程中那些曾经需要半天专注人工工作的部分（撰写说明、起草公告、协调下游检查）正是模型擅长的草拟工作。其余的都是机械性工作，适合放在YAML文件中。诀窍从来不只是"让AI来做"。而是让模型起草，让确定性代码验证，让人来做决策。它完全由开源工具和开源权重构建，因此成本几乎为零，任何人都可以运行它。

完整的工作流文件是公开的。如果你维护一个Python库，fork它，适配它，并告诉我们效果如何！

---

> 本文由AI自动翻译，原文链接：[Shipping huggingface_hub every week with AI, open tools, and a human in the loop](https://huggingface.co/blog/huggingface-hub-release-ci)
> 
> 翻译时间：2026-06-24 06:08
