---
title: hf CLI重构：为AI Agent优化的Hub交互工具
title_original: Designing the hf CLI as an agent-optimized way to work with the Hub
date: '2026-06-04'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/hf-cli-for-agents
author: ''
summary: Hugging Face团队重构了其官方命令行工具hf CLI，使其同时服务于人类用户和编码Agent（如Claude Code、Codex等）。文章介绍了自2026年4月起追踪的Agent流量数据，显示Claude
  Code和Codex是最大的两个Agent用户群体。为满足两类用户的不同需求，hf CLI在检测到Agent驱动时自动切换输出格式：去除ANSI颜色、表格截断和交互提示，采用紧凑结构化输出以节省Token。基准测试表明，在复杂多步骤任务中，使用hf
  CLI相比手动调用curl或Python SDK可节省6倍的Token消耗。
categories:
- AI基础设施
tags:
- Hugging Face
- CLI工具
- AI Agent
- Token优化
- 开发者体验
draft: false
translated_at: '2026-06-05T06:20:58.022618'
---

# 将 hf CLI 设计为与 Hub 交互的 Agent 优化方式

`hf` 是 Hugging Face Hub 的官方命令行入口。任何你能通过 Python SDK 在 Hub 上完成的操作，都能在终端中完成：下载和上传模型、数据集和 Spaces；创建和管理仓库、分支、标签和拉取请求；在 HF 基础设施上运行任务；管理 Buckets、Collections、webhooks 和推理端点。

`hf` CLI 多年来主要面向我们的用户构建。但现在它越来越多地被编码 Agent 使用：Claude Code、Codex、Cursor 等。因此我们对其进行了重构，使其能同时服务于两类用户。这篇博文总结了我们的工作内容以及基准测试结果。我们发现，在复杂的多步骤任务中，不使用 CLI 的基线方案（Agent 手动调用 `curl` 或 Python SDK）消耗的 Token 数量是使用 `hf` CLI 的 **6 倍**。

## Hub 上的 AI Agent 流量

我们从 2026 年 4 月开始追踪 Hub 上的 Agent 使用情况。`hf` CLI（以及其底层构建的 `huggingface_hub` Python SDK）通过读取 Agent 设置的环境变量来检测是否为编码 Agent 在驱动：`CLAUDECODE`/`CLAUDE_CODE` 对应 Claude Code，`CODEX_SANDBOX` 对应 Codex，此外还有 Cursor、Gemini、Pi 以及通用的 `AI_AGENT`。这个单一信号完成两项工作：它塑造 CLI 的输出格式（下文详述），并为每个 Hub 请求打上 `agent/<name>` 的用户代理标签，这样我们就能将流量归因于驱动它的 Agent。按独立用户数计算，最大的两个是 **Claude Code 和 Codex**，远超其他 Agent，它们也是本文后续进行基准测试的两个 Agent。

![自 2026 年 4 月以来，按编码 Agent 划分的 Hugging Face Hub 独立用户数。Claude Code 以 39.5k 用户和 4860 万次请求领先，其次是 Codex，拥有 34.8k 用户和 3640 万次请求，随后是 antigravity、cursor-cli、openclaw、cursor、gemini 和 pi。](/images/posts/c4ce34dc2d63.png)

![自 2026 年 4 月以来，按编码 Agent 划分的 Hugging Face Hub 独立用户数。Claude Code 以 39.5k 用户和 4860 万次请求领先，其次是 Codex，拥有 34.8k 用户和 3640 万次请求，随后是 antigravity、cursor-cli、openclaw、cursor、gemini 和 pi。](/images/posts/9d7c35475425.png)

条形图统计每个 Agent 的独立用户数；请求量显示在副标签中。仅 Claude Code 就有约 4 万用户和近 4900 万次请求，Codex 紧随其后。这些是早期数据（我们直到 2026 年 4 月才开始归因 Agent 流量），但规模已经相当可观，我们预计随着编码 Agent 成为与 Hub 交互的标准方式，这一数字将持续增长。

## 为人类和 Agent 构建

人类和编码 Agent 对相同的 `hf` 命令期望不同的输出。人类希望看到丰富的终端输出：ANSI 颜色、为适应屏幕而截断的填充表格、成功时的绿色 ✅、布尔值的 ✔、进度条、文字提示。Agent 则希望相反：无 ANSI、无截断、每个值完整显示（因为 Agent 能处理比人类更密集的输出）、保持紧凑和结构化以节省 Token。它也无法回答 CLI 提示，并且在超时后会愉快地重新运行命令。本节其余部分介绍 `hf` 如何满足双方的需求。我们在 `hf` v1.9.0 中引入了 Agent 模式输出，并在后续版本中逐步将 CLI 的其余部分迁移到该模式。

### 同一命令，多种渲染方式

当 `hf` 自动检测到 Agent 使用（通过上述环境变量）时，它会以不同方式渲染**同一命令**。它无需传递标志即可为人类或 Agent 优化输出格式：

```text
# 人类（终端默认）：对齐表格，截断以适应屏幕，带提示
> hf models ls --author Qwen --sort downloads --limit 3
ID                       CREATED_AT DOWNLOADS LIBRARY_NAME LIKES PIPELINE_TAG    PRIVATE TAGS
------------------------ ---------- --------- ------------ ----- --------------- ------- -------------------------
Qwen/Qwen3-0.6B          2025-04-27  21156913 transformers  1285 text-generation         transformers, safetens...
Qwen/Qwen2.5-1.5B-Ins... 2024-09-17  15143953 transformers   725 text-generation         transformers, safetens...
Qwen/Qwen3-4B            2025-04-27  14808352 transformers   625 text-generation         transformers, safetens...
提示：使用 `--no-truncate` 或 `--format json` 显示完整值。

# Agent（自动检测）：TSV 格式，完整 ID + ISO 时间戳 + 每个标签，无截断
$ hf models ls --author Qwen --sort downloads --limit 3
id      created_at      downloads       library_name    likes   pipeline_tag    private tags
Qwen/Qwen3-0.6B 2025-04-27T03:40:08+00:00       21156913        transformers    1285    text-generation False   ['transformers', 'safetensors', 'qwen3', 'text-generation', 'conversational', 'arxiv:2505.09388', 'base_model:Qwen/Qwen3-0.6B-Base', 'base_model:finetune:Qwen/Qwen3-0.6B-Base', 'license:apache-2.0', 'text-generation-inference', 'endpoints_compatible', 'deploy:azure', 'region:us']
Qwen/Qwen2.5-1.5B-Instruct      2024-09-17T14:10:29+00:00       15143953        transformers    725     text-generation False['transformers', 'safetensors', 'qwen2', 'text-generation', 'chat', 'conversational', 'en', 'arxiv:2407.10671', 'base_model:Qwen/Qwen2.5-1.5B', 'base_model:finetune:Qwen/Qwen2.5-1.5B', 'license:apache-2.0', 'text-generation-inference', 'endpoints_compatible', 'deploy:azure', 'region:us']
Qwen/Qwen3-4B   2025-04-27T03:41:29+00:00       14808352        transformers    625     text-generation False   ['transformers', 'safetensors', 'text-generation', 'arxiv:2309.00071', 'arxiv:2505.09388', 'base_model:Qwen/Qwen3-4B-Base', 'base_model:finetune:Qwen/Qwen3-4B-Base', 'license:apache-2.0', 'endpoints_compatible', 'deploy:azure', 'region:us']

```

**人类**获得一个对齐的表格，截断以适应终端，并附带如何查看更多信息的提示，状态有颜色提示（成功时绿色 ✓，错误时红色）。**Agent** 获得完整的 TSV 格式记录：完整的仓库 ID、完整的 ISO 时间戳、每个标签、无 ANSI 代码、无截断、易于解析且节省 Token。

在实践中，我们实现了诸如 `.table(...)`、`.result(...)`、`.json()` 等日志方法，它们接收原始数据作为输入并处理格式化。除了人类和 Agent 模式，我们还引入了 `--json` 和 `--quiet` 选项，以便更容易地串联命令。默认模式根据上下文自动选择，但用户始终可以通过 `--format human | agent | json | quiet` 强制选择他们喜欢的格式。

### 下一步命令提示

CLI 命令很少孤立运行：一个步骤通常暗示下一步（`git add`，然后 `git commit`）。现在许多 `hf` 命令都以一个**提示**结尾：接下来要运行的确切命令，并预填了你刚刚使用的 ID，这样用户或 Agent 可以直接链接到下一步，而无需从头开始推导。在后台启动一个任务，它会指向其日志；创建一个 Space，它会指向其启动状态：

```text
$ hf jobs run --detach python:3.12 python train.py
✓ 任务已启动
  id: 6f3a1c2e9b
  url: https://huggingface.co/jobs/celinah/6f3a1c2e9b
提示：使用 `hf jobs logs 6f3a1c2e9b` 获取日志。

```

对人类来说，这是一种便利。对 Agent 来说，这是一个轨道：下一个动作已被命名，用正确的 ID 参数化，并准备好运行，因此推导下一步所需的步骤更少。错误也以相同方式处理，指出修复方法而不是仅仅失败：

```
错误：未登录。请先运行 `hf auth login`。

```

提示、警告和错误都输出到 stderr，而数据输出到 stdout，因此这些指导信息不会污染 Agent 正在解析的输出。

### 非阻塞且可安全重试

`hf` 不会坐在交互式提示符前等待一个 Agent 无法按下的按键。破坏性命令仍会要求人工确认，但在 Agent 模式下，它会快速失败，并在消息中提供修复方法（使用 `--yes` 跳过确认），而 `-y`/`--yes` 则直接跳过。并且，由于 Agent 会在超时或丢失上下文时重试，操作被设计为可安全重复执行：`hf repos create --exist-ok` 在仓库已存在时不会执行任何操作，重新运行上传会干净地重新提交。此外，移动真实数据的命令会提供 `--dry-run` 选项，在执行前精确显示将要传输的内容，这对人类和 Agent 都很方便，因为两者都不必承诺执行长时间的下载或盲目同步：

```text
# agent mode: a destructive command without --yes refuses, with the fix in the message
$ hf repos delete my-org/old-model
Error: You are about to permanently delete model 'my-org/old-model'. Proceed? Use --yes to skip confirmation.

# commands that move data take --dry-run to preview the transfer first
$ hf download deepseek-ai/DeepSeek-V4-Pro config.json --dry-run
[dry-run] Will download 1 files (out of 1) totalling 1.8K.
file         size
config.json  1.8K

```

### 可发现、可预测的命令

`hf` 被设计为可探查的：运行 `hf` 查看资源组，在需要的资源组上运行 `--help`，每个 `--help` 都以真实、可复制粘贴的示例结尾（Agent 匹配这些示例的速度远快于解析描述）：

```
$ hf models ls --help
...
Examples
  $ hf models ls --sort downloads --limit 10
  $ hf models ls --search "qwen" --author Qwen
  $ hf models ls Qwen/Qwen3-4B --tree

```

命令树是一致的，采用 `resource + verb` 结构，并带有明显的别名（`hf models ls`，`hf repos create`，`hf jobs ps`，`hf collections delete`；`list`/`ls`，`remove`/`rm`），因此一旦 Agent 学会一个命令，它就能推断出其余命令。并且输出是可组合的：`-q` 每行打印一个 ID 以便通过管道传递给下一个命令，`--json` 提供可传递给 `jq` 的内容。

```text
$ hf models ls --author Qwen -q | head -3
Qwen/Qwen3-0.6B
Qwen/Qwen2.5-1.5B-Instruct
Qwen/Qwen3-4B

```

## 为编码 Agent 对 hf CLI 进行基准测试

为了确定 `hf` CLI 是否真的对 Agent 更高效，我们对其进行了测量。我们构建了一个小型评估框架，并通过每种驱动 Hub 的方式多次运行同一组 Hub 任务，针对实时 Hub 对每次运行进行评分。在介绍方法论之前，先给出主要结论：在两种 Agent 上，`hf` CLI 都表现更优，在复杂、多步骤的任务上最为明显，它使用的 Token 要少得多。

（自我报告错误 = Agent 报告 17 个可解决任务成功，但 Hub 显示并非如此。`hf` CLI 行是安装了其技能的 CLI；技能在裸 CLI 基础上增加的内容（主要是更少的工具调用）在下面的技能部分中详细说明。代表性记录发布在此存储桶中。）

### 设置

我们定义了 18 个非平凡的 Hub 任务。不是“下载一个文件”，而是你实际会要求的那种：汇总一个热门组织的模型，检查仓库的文件及其大小，使用包含/排除规则上传文件夹，删除文件，跨仓库复制文件，打开一个添加许可证的 PR，创建一个带有分支和标签的仓库，同步并修剪一个存储桶，构建一个集合。每个任务都会交给一个全新的编码 Agent，并且只能通过**一种**方式与 Hub 通信：

- `hf` CLI，或者
- `curl` / Python SDK：完全没有 `hf` CLI，因此 Agent 退回到使用 `curl` 调用 REST API 或使用 `huggingface_hub` Python 库。

我们以两种配置运行 `hf` CLI，一种带技能，一种不带技能（一个生成的命令参考，我们将在其自己的部分中讨论）。但下面的主要比较仅仅是 `hf` CLI 与 `curl` / SDK；技能的增量影响足够小，我们将其单独列出，而不是挤入主要结果中。

配置故意保持简洁：每次运行使用全新实例，没有自定义 MCP 服务器，没有 `CLAUDE.md` 或 `AGENTS.md`，上下文中没有任何东西来引导行为。任务和工具被放入单个提示词中，Agent 以 `TASK_COMPLETE` 或 `TASK_FAILED` 标记结束，但我们不信任该标记（Agent 可能会在从未落地的工作上报告成功），因此我们通过**重新查询实时 Hub** 来独立评估每次运行：分支是否真的被创建，文件是否真的被删除，存储桶是否存在？每个任务/工具组合运行 **10 次**，因为编码 Agent 是非确定性的，每个 Agent 大约运行 **520 次**（18 个任务 × 3 个工具 × 10 次重复，减去一个可计费 Jobs 任务的上限），总共约 **1,000 次**评分运行。我们在两个最流行的编码 Agent（使用 Sonnet 4.6 的 Claude Code 和使用 GPT-5.5 的 OpenAI Codex）上完整运行了两次。

### 结果

下面的两个图表分解了上表。首先是 **Sonnet 上的任务成功率**，这是 curl 和 SDK 最吃力的 Agent：

![Claude Code with Sonnet 4.6 上的任务成功率：hf CLI 94%，curl / Python SDK 84%。](/images/posts/64d48cdf8ed1.png)

![Claude Code with Sonnet 4.6 上的任务成功率：hf CLI 94%，curl / Python SDK 84%。](/images/posts/a437f9b8282f.png)

没有 CLI，curl 和 SDK 落后了十个百分点，因为在 Sonnet 上它们根本无法完成部分工作（主要是写入操作），而 `hf` CLI 则能顺利完成。

第二张图展示了 **GPT-5.5 上的 Token 影响**，按任务细分。每个柱状条是 curl/SDK 的 Token 数除以同一任务上 CLI 的 Token 数，因此 `2.4×` 意味着非 `hf` 版本执行相同操作消耗的 Token 数是其 2.4 倍：

![GPT-5.5 上 curl/Python SDK 与 hf CLI 的每个任务 Token 比率，从高到低排序。多步骤任务使 curl/Python SDK 成本高得多：创建+同步+修剪存储桶 6.0x，按趋势模型排名组织 4.1x，创建仓库+分支+标签 / 删除文件 / 跨仓库复制文件各 2.4x。简单的一次性读取接近持平或更便宜：批量模型元数据 0.5x，计数数据集行数 0.3x。](/images/posts/8af4e5e7e1f4.png)

![GPT-5.5 上 curl/Python SDK 与 hf CLI 的每个任务 Token 比率，从高到低排序。多步骤任务使 curl/Python SDK 成本高得多：创建+同步+修剪存储桶 6.0x，按趋势模型排名组织 4.1x，创建仓库+分支+标签 / 删除文件 / 跨仓库复制文件各 2.4x。简单的一次性读取接近持平或更便宜：批量模型元数据 0.5x，计数数据集行数 0.3x。](/images/posts/f98cd5f68d0b.png)

在一次性读取（计数数据集行数，批量元数据）上，curl 和 SDK 表现良好，有时甚至更轻量。但随着任务变得更加复杂并涉及多个依赖步骤，Agent 必须手动构建整个 REST 调用链（或深入挖掘 SDK），成本会急剧上升：在创建带有分支和标签的仓库、删除文件、跨仓库复制或同步存储桶时，成本是 CLI 的 **2.4× 到 6×**。`hf` CLI 允许 Agent 将任务表达为几个更高级别的命令，而不是精心设计一个复杂的工作流。

### 主要发现

- **`hf` CLI 比 curl 或 SDK 精简得多。** 对于相同的任务，在成功率相同或更高的情况下，curl 和 SDK 消耗的 Token 大约多 **1.3× 到 1.8×**。在简单的读取任务上它们表现良好，但在真正的多步骤工作上，它们要多付出 **2× 到 6×** 的代价：CLI 将 REST 调用链组合成几个高级命令，而 curl 或 SDK 每次运行都需要手动重新推导这个链。
- **在更强的模型上，curl 和 SDK 可以工作，但仍然浪费。** 在 Sonnet 上它们无法完成部分工作（主要是写入操作）；在 GPT-5.5 上它们大多能成功，能正确手动构建 REST 调用（或使用 SDK），但 Token 消耗仍然远高于 CLI。

## hf-cli 技能

`hf` 附带一个**技能**：整个命令表面的紧凑参考，Agent 将其作为上下文加载。它是从实时的 `hf` 命令树**自动生成**的，每个命令一行（其签名、一行描述以及重要的标志），按资源分组，并附带一个常用选项的简短词汇表。它故意跳过不言自明的标志，以保持简洁并节省上下文，并且每个版本都会重新生成。运行 `hf skills preview` 来打印它，或使用以下命令安装：

```bash

hf skills add

hf skills add --claude

```

这能带来什么好处？主要在于，Agent（智能体）不再需要猜测。最清晰的单一视图是，在拥有和没有该技能的情况下，每次运行所需的命令数量：

![每次运行的平均命令数（工具调用），在两个Agent上分别使用和不使用 hf-cli 技能。Claude Code (Sonnet 4.6)：不使用技能时为10.4，使用技能时为6.9。Codex (GPT-5.5)：不使用技能时为10.1，使用技能时为7.3。数值越低越好。](/images/posts/bf626da5e9f1.png)

![每次运行的平均命令数（工具调用），在两个Agent上分别使用和不使用 hf-cli 技能。Claude Code (Sonnet 4.6)：不使用技能时为10.4，使用技能时为6.9。Codex (GPT-5.5)：不使用技能时为10.1，使用技能时为7.3。数值越低越好。](/images/posts/3b223b40a694.png)

在两个Agent上，每个任务的命令数从大约十条减少到大约七条，工具调用减少了约30%。这是因为Agent不再需要试探——技能帮助它找到正确的命令和参数。技能不会减少你的Token消耗，因为它会在上下文中预先附加一段固定的信息，因此对于相同任务，Token数量大致保持不变或略有增加。技能也不会让CLI变得更可靠，但它能帮助Agent将时间花在执行你的任务上，而不是去弄清楚工具的工作原理。当使用`hf`与本地模型时，这一点尤其有用。

我们在全新的会话中运行了每个任务，因此技能在每个任务上都付出了其上下文成本。在真实的多任务会话中，这种成本会被摊销（Agent只需学习一次命令界面），因此Token消耗情况可能会有所改善；我们没有测量这种情况。

## 亲自尝试

我们进行所有这些基准测试，是因为我们认为这很重要。Agent正在成为Hub的真实用户：它们训练模型、构建和清理数据集，并以Spaces的形式发布演示，这些几乎总是代表人类完成的。一个对Agent友好的Hub，同样也会让使用Agent的人体验更好。Agent的工具越好，它能为你做的事情就越多。

如果你的Agent与Hugging Face Hub交互，我们建议你为其提供`hf` CLI：

```bash
curl -LsSf https://hf.co/cli/install.sh | bash
```

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://hf.co/cli/install.ps1 | iex"
```

然后，将技能交给它，这样它从第一轮对话开始就能了解整个命令界面：

```bash
hf skills add            
hf skills add --claude   
```

接着，将你的Agent指向Hub，让它开始工作。确保你已经登录（`hf auth login`），然后给它一个类似这样的提示词：

```text
使用 `hf` 列出我的 Hugging Face Hub 模型、数据集和 Spaces。
看看我目前是如何使用 Hub 的，并建议一些你可以帮助我的方式。
```

它会自行找出命令，并返回一些有用的内容。

完整的命令参考位于 `hf` CLI 指南中。

## 注册一个Agent框架

正在构建一个Agent框架？请注册它！这样 `hf` 才能学会检测它，Hub 才能将其流量归因于你的框架。你只需要提交一个小型 PR，在 `agent-harnesses.ts` 中添加一个条目即可。阅读《注册你的Agent框架》指南以获取更多详细信息。

---

> 本文由AI自动翻译，原文链接：[Designing the hf CLI as an agent-optimized way to work with the Hub](https://huggingface.co/blog/hf-cli-for-agents)
> 
> 翻译时间：2026-06-05 06:20
