---
title: 用本地模型免费分类OpenClaw仓库
title_original: We got local models to triage the OpenClaw repo for FREE!*
date: '2026-06-22'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/local-models-pr-triage
author: ''
summary: 本文介绍了如何在Agent框架中使用Gemma和Qwen等本地开源模型，对OpenClaw仓库的issue和PR进行实时分类和通知。作者利用自有硬件（如DGX
  Spark）运行本地模型，避免了每月200美元的闭源模型订阅费用，同时实现了近乎即时的响应。文章详细描述了分类流程、工具选择（如reposhell限制bash权限）以及性能优化，强调本地模型在AI基础设施中的重要性日益提升。
categories:
- AI基础设施
tags:
- 本地模型
- 开源AI
- Agent框架
- 分类任务
- OpenClaw
draft: false
translated_at: '2026-06-24T06:09:35.875780'
---

# 我们让本地模型免费对 OpenClaw 仓库进行分类！*

*免费如啤酒，不包括电费，且假设你已拥有硬件

2026年6月将被铭记为人们意识到闭源模型可以被收回的时刻。随着 Anthropic 最新旗舰模型 Claude Fable 5 被下架的记忆犹新，不难理解为什么拥有自己的 AI 技术栈并能在本地运行模型比以往任何时候都更重要，尤其是当你正在 AI 之上构建业务时。

基于此，我们想分享如何在 Agent（智能体）框架中使用 Gemma 和 Qwen 等本地模型来执行分类任务[^1]。这种方法不同于使用 BERT 等模型进行分类。在像 Pi 这样的 Agent（智能体）框架中，本地模型可以与结构化输出配合使用来分配标签。我们选择这种方法是因为我们已经拥有本地模型和框架，并且坚信随着本地模型能力的提升，类似的配置将越来越受欢迎。[^2]

我们的起点是 OpenClaw 仓库中的开源贡献。OpenClaw 每天收到数百个 issue 和 PR，需要对其进行分类、优先级排序并分配给维护者。我，Onur，正在努力让本地模型与 OpenClaw 良好配合。作为这个特定领域的维护者，我需要快速响应任何 P0 问题。

使用像 GPT-5、Opus 或 Sonnet 这样的 SOTA 闭源模型，这是一个相当直接的任务。但我恰好拥有 128 GB 的统一内存，即 NVIDIA GB10。所以我接受了这个挑战：

我能否构建一个实时通知系统，仅过滤并通知我负责的 issue……使用本地开源权重模型？

![这个小盒子，又名 DGX Spark，可以高并发运行 gemma-4-26b-a4b，每秒生成数百个 Token。](/images/posts/67c8dfa37b33.png)

如果我设置我的 OpenClaw 主 Agent（智能体）运行在每月 200 美元的 ChatGPT Pro 套餐上，在每个新 issue 或 PR 时触发任务，那会耗尽我的配额。我可能改为设置每 2 小时或每 6 小时运行一次。这样会将 issue 批量处理更长时间，因此我们是用延迟处理来换取实时通知。

如果我在已有的硬件上使用本地模型运行此任务，我不仅能获得近乎即时的通知，还能免费完成（或者说，只需支付电费）。

## 对 issue 和 PR 进行分类

我们提出了一组有限的标签，代表我们需要分类的 issue 类别，然后使用本地模型将每个 issue 分类到其中一个类别，例如 `local_models`、`self_hosted_inference`、`acp`、`agent_runtime`、`codex`、`ui_tui` 等等。[^3]

但如何对拉取请求进行分类？只需向 Chat Completions 端点发送一个带有工具 JSON schema（以主题作为枚举）的简单请求？

差不多。但现在是 2026 年，不是 2023 年，我们有 AGENT（智能体）。我们可以做得更好！

对于本地模型的选择，我们测试了 `gemma-4-26b-a4b` 和 `qwen3.6-35b-a3b`。通过性能优化，两者都可以在本地每秒生成数百个 Token。

我们使用 Agent（智能体）框架来驱动分类运行。为此，我们将 `pi` 作为框架打包，它可以调用本地模型端点。

Agent（智能体）默认在第一个提示词中接收 PR 标题、正文和 PR diff 的截取片段。然后，它可以选择使用 `bash` 工具对 OpenClaw 仓库执行只读操作（如果需要查看代码库），或使用 `final_json` 工具提交最终分类结果。

在这种高吞吐量设置下，你不会想给本地模型完全的 bash 访问权限，因为一个被提示注入的 issue 或 PR 可能会引导模型执行与分类无关的操作。

因此，我们使用 `reposhell` 代替 `bash`：一个受限的类 `bash` shell，只允许对 OpenClaw 仓库执行只读操作（`ls`、`find`、`cat`、`grep` 等）。模型认为它在使用 `bash`，但任何不允许的操作都会被拒绝：

```
reposhell 绑定 cwd=/repo/openclaw 仓库=openclaw
输入 help 查看允许的命令；exit 或 quit 退出

reposhell /repo/openclaw> help
允许: pwd, ls, find, rg, grep, sed -n, cat, head, tail, wc -l, git status --short, git show --name-only, git grep, git ls-files
搜索: rg -n -i "lm studio" 或 grep -R -n -i "lm studio" .
文件: rg --files -g "*.ts" 或 git ls-files src
示例: rg -n reposhell README.md | sed 不允许；一次使用一个简单命令

reposhell /repo/openclaw> head README.md
# 🦞 OpenClaw — 个人 AI 助手

<p align="center">
    <picture>
        <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/openclaw/openclaw/main/docs/assets/openclaw-logo-text-dark.svg">
        <img src="https://raw.githubusercontent.com/openclaw/openclaw/main/docs/assets/openclaw-logo-text.svg" alt="OpenClaw" width="500">
    </picture>
</p>

<p align="center">

reposhell /repo/openclaw> curl localhost
reposhell 策略拒绝命令: 不支持的命令 "curl"
exit_code=2

reposhell /repo/openclaw>

```

这里有一个具体的例子说明了这一点的重要性。在一个已保存的会话示例中，`qwen3.6-35b-a3b` 正在分类 `openclaw/openclaw#84621`，标题为 `Fix Kimi tool-call rewriting stop reason handling`。思考块显示模型最初考虑 `coding_agent_integrations`，因为更改路径 `extensions/kimi-coding` 看起来合理。模型使用 reposhell 通过简单的只读命令（如 `ls extensions`、`ls extensions/kimi-coding` 和 `cat extensions/kimi-coding/package.json`）检查本地仓库。该包元数据显示扩展实际上是 `@openclaw/kimi-provider`，一个 OpenClaw Kimi 提供者插件。因此模型将最终标签修正为 `inference_api` 和 `tool_calling`，并明确排除了 `coding_agent_integrations`。

我们之前提到过，我们打包了一个特定的 `pi` 配置，只能执行只读操作并返回分类输出。我们称之为 `localpager-agent`，以主要项目 `localpager` 命名。每个 PR 和 issue 生成一个提示词，然后与其他参数一起传递给 CLI，如下所示：

```bash
localpager-agent \
  --model "<模型-id>" \
  --base-url "<兼容openai的基础-url>" \
  --session-dir "<会话输出目录>" \
  --final-schema "<运行时-schema.json>" \
  --tools bash,final_json \
  --reposhell-socket "<reposhell.sock>" \
  --reposhell-default-repo "<仓库-id>" \
  --reposhell-visible-repos "<仓库-id>[,<仓库-id>...]" \
  -p "$(cat <渲染后的提示词.md>)"

```

## 处理传入的 PR 和 issue

那么，在传入的 PR/issue 和最终 Discord 通知之间，是什么在协调一切？

![这是最终过滤后的 Discord 通知的样子：一个关于所需领域的 PR 被路由给我。](/images/posts/36340dfa7da7.jpg)

围绕此的编排非常简单；只有分类步骤涉及 LLM：

1. 我们使用 `openclaw/gitcrawl` 作为仓库的本地镜像。每当有新 PR 或 issue 时，每个项目都被规范化为相同格式并写入 localpager 自己的 SQLite 数据库。如果项目是新的，localpager 会为其创建一个分类任务。
2. 然后一个工作线程从该队列中领取任务。它构建一个包含 issue 或 PR 标题、正文、标签、作者、状态以及可选评论、更改文件和选定 diff 片段的 GitHub 上下文对象。这意味着本地模型大多数时候不需要浏览 GitHub 或自行打开 URL。它被提供了所有相关上下文。
3. 上下文对象被渲染成提示词并传递给 `localpager-agent`，如上一节所述。Agent（智能体）可以思考并使用 reposhell，但最终必须输出符合定义 schema 的分类结果。
4. 输出被存储回 localpager SQLite 数据库，并根据用户配置的通知策略（即通知我这些主题，但不通知其他主题）转发到 Discord。

下图展示了localpager的整体架构：

该架构是半Agent（智能体）化的。标签标注采用Agent（智能体）方式完成，而发送通知则由确定性规则处理。这样设计是为了在任务中最直接的部分省去推理需求，从而加快通知管道的速度。本地推理是免费的，但每个任务都存在资源争用成本：GPU带宽应保留给绝对需要推理的任务。这也能降低通知环节出现错误的概率。

## 本地模型能否对PR进行分类？

坦白说：这个系统的早期本地版本噪声很大。首个测试的模型——gemma-4-e4b-it——有助于让端到端的本地管道跑通，但它也倾向于给PR或Issue添加过多无关标签。误报标签会让Discord信息流变得嘈杂，无法将我的注意力集中在正确的问题上。这促使我们转向测试更大的本地模型，包括gemma-4-26b-a4b和qwen3.6-35b-a3b，并在下面这个包含330行的评估集上进行了测试。

在早期的提示词工作中，我们还通过antirez DS4实现[^4]使用了DeepSeek-V4-Flash来创建早期的数据集标签。该方案通过CUDA运行DS4服务器。我们最终放弃了将DS4作为标签标注器，因为它在不同运行中的标注结果不一致。我们也没有将其作为主要的localpager-agent模型，因为它体积太大，无法在我们的硬件上获得足够的吞吐量：DS4服务器给我们提供的速度约为每秒14个Token，最大并发数为1。

为了测试模型性能，我们选取了330个GitHub Issue和PR并生成了标签。每个项目被标注了五次（3次GPT-5.5和2次Opus 4.8），且模型之间需要达成一致才能被接受。这个过程涉及人工裁决、改进标签定义，并突出模型所需的内部产品设计选择。这为我们提供了一套稳定、可复现的标签，用于与较小的模型进行比较。

在对gemma-4-26b-a4b或qwen3.6-35b-a3b进行提示词优化之前，我们无需在此评估集上获得有用结果。使用相同的路由提示词，Gemma的召回率更高，每行的挂钟时间更短；而Qwen的精确率更高，精确匹配更多，误报更少。我们还运行了DeepSeek-V4-Flash作为参考。它的误报最少，但模型大小和吞吐量使其无法在NVIDIA GB10上实时执行这些任务。由于每行可以有多个标签，误报和漏报是所有行的标签总数。下面的Qwen结果是重试结构化输出失败（模型在调用final_json之前输出Token耗尽）后的结果。对于Gemma和Qwen，多次运行的指标报告了三次运行的平均值±样本标准差。DeepSeek-V4-Flash作为参考仅运行一次。

这里的吞吐量和挂钟时间并非这些模型在此硬件上的最终最大性能数据。它们是我们当时使用的设置以及可用的优化方案。例如，在另一次探测中，gemma-4-26b-a4b也支持并发数32，并达到了每秒超过700个聚合输出Token。

对于Gemma基准测试，我们使用vLLM服务gemma-4-26b-a4b，并采用了为此设置找到的可用优化。其中很大一部分是NVFP4量化：在GB10级Blackwell硬件上，它不仅是一个更小的模型文件，而且是一种硬件友好的格式，可以比Q4_K_M等便携式GGUF量化更直接地使用NVIDIA/vLLM执行路径。在实践中，这意味着更少的内存流量和更大的批处理空间。我们还启用了前缀缓存、FP8 KV缓存、CUTLASS MoE后端以及仅语言模型模式。完整的330行运行在并发数16下大约7.5分钟完成。

## 使用OpenClaw跟踪和验证实时性能

我们之前提到过，不必为每个新的Issue或PR都运行本地模型的任务，我们可以每隔n小时（例如每2小时）使用OpenClaw中运行的SOTA云端模型（如GPT-5.5）运行一个批处理任务，以达到同样的目的。[^5]

在这种情况下，我们需要一个ChatGPT Pro计划。由于模型是SOTA的，尽管将2小时的Issue/PR批量处理在一起，我们仍可以预期其表现合理。

因为我们想了解本地分类器与GPT-5.5相比表现如何，所以我们同时运行两者，并让GPT-5.5每2小时判断一次误报和漏报。

为了安全起见，我们在沙箱中运行OpenClaw任务，仅允许其访问我们报告结果的public repo。在我们的案例中，我们让OpenClaw任务更新一个机器可读的文件，然后一个简单的脚本读取Codex分配的标签，并计算误报/漏报状态。示例输出如下：

漏报

- Issue #88499 openai-responses provider: 404 on previous_response_id when store=false (default)inventory area: OpenAI-compatible/proxy; notifier topics: agent_runtime, api_surface, sessions; notification: none

- inventory area: OpenAI-compatible/proxy; notifier topics: agent_runtime, api_surface, sessions; notification: none

误报

- PR #88275 fix(models-config): allow self-hosted providers without apiKey in models.json (#88267)notifier interest: i0; topics: self_hosted_inference, local_model_providers, config; notification: sent
- PR #88266 refactor: extract model catalog core packagenotifier interest: i1; topics: config, api_surface, local_model_providers; notification: sent
- PR #88247 feat: add hosted model providersnotifier interest: i0; topics: local_model_providers, model_serving, docs, api_surface; notification: sent

- notifier interest: i0; topics: self_hosted_inference, local_model_providers, config; notification: sent

- notifier interest: i1; topics: config, api_surface, local_model_providers; notification: sent

- notifier interest: i0; topics: local_model_providers, model_serving, docs, api_surface; notification: sent

关于如何分类、编辑机器可读文件、使用脚本获取误报和漏报的说明，都包含在一个agent skill中，该skill被一个每2小时运行一次的OpenClaw cron job所引用。然后，OpenClaw Agent会摄取任何新的Issue或PR，将其添加到带有适当标签的JSON文件中，运行脚本，并在同一个Discord频道中报告结果。这样，我们可以每隔几小时观察本地模型的性能，并收到遗漏通知。

## 结论

我们认为Issue/PR分类任务是更广泛任务集（我们称之为“高吞吐量分类”）中的一个特例。本文探讨了使用本地模型在单一领域（即开源贡献）中实时过滤信息的想法。像gemma-4-26b-a4b和qwen3.6-35b-a3b这样的中等规模本地模型，无需任何微调就能以良好的准确率进行一次性分类，这使它们成为快速原型开发的优选，之后再转向更具成本效益的传统分类器模型。

然而，同样的方法也可以应用于其他领域：

- 新闻业的新闻分类
- 在社交媒体和论坛（如X或Reddit）中过滤感兴趣的帖子
- 分类客户支持工单
- 分类内容审核申诉
- 在销售过程中过滤潜在客户
- 在研究时过滤arXiv上的特定主题

这个列表还可以扩展，但我们认为思路应该很清晰了。

除了分类之外，我们还探索了如何使用Agent harness以安全的方式运行快速本地模型进行分类。这种方法的一个恰当命名是Agent（智能体）分类：模型并非一开始就被喂入全部信息，而是可以在返回结构化数据之前搜索更多上下文。虽然我们不能完全称其为一种新颖的方法，但我们希望这篇博文能成为特定Pi+a restricted shell+final_json方案的优秀参考。

[^1]: 对于本文中的用例，我们发现，以能够正确理解和标注产品表面的方式分解PR/Issue是一个难题。  
[^2]: 尽管在我们的测试中并未出现这种情况——但模型完全有理由推断出下一步需要收集信息，并使用外部分类器。Agent（智能体）方法与传统方法并非互斥。  
[^3]: 请在此处查看完整主题列表及其他配置。  
[^4]: 我们使用了来自antirez/deepseek-v4-gguf的DeepSeek-V4-Flash-IQ2XXS-w2Q2K-AProjQ8-SExpQ8-OutQ8-chat-v2.gguf模型。  
[^5]: 尽管我们意识到使用LLM（大语言模型）作为评判者会削弱“免费”这一特性，但我们的具体实现出于研究目的采用了这种方式。在实践中，可以在试用期内同时使用更大、更昂贵的模型进行校准，之后系统将完全过渡到较小的模型。在最近的运行中，此审计循环每2小时检查大约消耗4万个GPT-5.5 Token（主要为缓存上下文），按API定价每次运行成本约2-3美分，若每天运行12次，则每月成本约9美元。这是对所有新项目进行的一次性批量审计，而非逐项调用评判；若逐项进行，成本可能会高出数倍。

---

> 本文由AI自动翻译，原文链接：[We got local models to triage the OpenClaw repo for FREE!*](https://huggingface.co/blog/local-models-pr-triage)
> 
> 翻译时间：2026-06-24 06:09
