---
title: 构建自动驾驶的技能排行榜：Vercel上的大规模自动化运营
title_original: Building a self-driving skills.sh leaderboard - Vercel
date: '2026-02-09'
source: Vercel Blog
source_url: https://vercel.com/blog/building-a-self-driving-skills-sh-leaderboard
author: ''
summary: 本文介绍了skills.sh这一面向编程AI智能体的开源技能排行榜如何通过自动化系统处理大规模、开放环境下的运营挑战。核心机制包括：利用Claude
  AI自动审核每个安装技能的内容，重点识别“不可审核性”模式（如混淆代码、未解释的远程执行命令等），而非限制功能本身；同时构建AI智能体持续分析安装数据，从时间分布、数量一致性、行为指纹等多维度检测刷量等恶意行为，确保排行榜的完整性。文章展示了在无需人工审核的情况下，通过AI驱动流程维护开放生态系统的可行方案。
categories:
- AI基础设施
tags:
- AI审核
- 开源生态
- Vercel
- 自动化运营
- 排行榜
draft: false
translated_at: '2026-02-11T04:34:47.231739'
---

skills.sh 是一个面向 Claude Code、Cursor、Codex 及其他 35 款以上编程 Agent（智能体）的技能排行榜。任何人都可以将技能发布到自己的 GitHub 仓库，如果有人安装，它就会显示在榜上。这是一个排行榜，而非注册表。这种开放性正是其意义所在，但也意味着系统需要处理规模、杂乱数据以及恶意行为，而无需我们手动审核每一次安装。自上线以来，我们已在排行榜上追踪了超过 45,000 个独立技能。

让我们来谈谈如何在这种规模下，自动化运营一个开放排行榜的操作层面。

## AI 驱动的技能审核

每个被安装的技能都会由 Claude 自动审核。

审核流程由一个由每次遥测事件触发的 Vercel Workflow 实现。它会比较技能文件夹的哈希值与上次审核的版本，如果未发生变化，则跳过。如果内容发生更改，则重新审核。

系统会启动一个 Vercel Sandbox，进行浅层 git 克隆，并读取技能文件夹中的每个文本文件（脚本、配置文件、Markdown 文件、代码）。文件会被设定优先级（SKILL.md 优先，然后是脚本、配置文件、其他 Markdown 文件），所有内容都会连同系统提示词一起发送给 LLM（大语言模型）。结构化的输出包括一个判定结果（安全或可疑）、理由，以及一个包含具体文件路径、行号和代码片段的关注事项数组。

我们曾制作了一个恶意技能，它隐藏了一条运行本地辅助脚本的指令，该脚本会获取并执行任意代码。在实施了安全审核流程后，该恶意技能立即被标记出来。

![](/images/posts/448c52948902.jpg)

![](/images/posts/e061b6abbd10.jpg)

审核提示词的关键洞见在于我们**不**寻找什么。技能本质上就是提示词注入。获取 API、读取环境变量、使用断言性语言、教授黑客技术或逆向工程都是允许的。核心问题是用户能否通过阅读技能内容来理解它将执行什么操作。

我们标记的是**不可审核性**：

- 被解码并执行的 Base64 编码字符串
- 无法阅读的压缩或混淆代码
- 未解释其作用的 `curl URL | bash` 命令
- 仅包含“访问此 URL”而无实际内容的技能
- 硬编码的 API 密钥或凭据
- 任何“相信我，直接运行这个”的模式

Base64-encoded strings that get decoded and executed

Minified or obfuscated code that can’t be read

curl URL | bashwith no explanation of what it does

Skills that are just “go to this URL” with no actual content

Hardcoded API keys or credentials

Any “trust me, just run this” pattern

排行榜会从排名和搜索结果中隐藏可疑和恶意的技能。它们仍可通过直接 URL 访问，但会显示警告横幅。安全的技能则无需人工干预，自动通过审核。

技能遵循与网络类似的安全模型。最终，用户在安装前需要自行判断是否信任发布者并阅读技能的实际内容。

技能审核处理的是每个技能内部的内容。但一个公开的排行榜还需要处理安装数字是否真实的问题。

## AI 辅助的排行榜完整性

上线几天内，我们就观察到有人试图虚增其安装量。一个带有真实数字的公开排行榜对某些人来说是无法抗拒的。

我们没有采用硬编码规则进行“打地鼠”式的对抗，而是构建了一个 AI Agent（智能体），定期分析完整的安装数据集以发现异常。该 Agent（智能体）接收原始遥测数据（每次安装事件的时间戳、来源、技能名称和匿名标识符），并寻找偏离有机行为的模式。它从多个维度进行检查：

- **时间分布**：合法的安装遵循人类活动节奏，例如推文发布后的激增、教程带来的逐步增长，以及夜间的平静。刷量行为则表现为全天候的均匀分布，与任何外部事件无关。
- **数量一致性**：Agent（智能体）将每个技能的安装量与独立用户数的比率与生态系统平均值进行比较。一个来自未知仓库的全新技能，没有任何有机增长轨迹却出现在前十名，就值得审查。
- **跨来源关联性**：多个“不同”的仓库在同一时间激增，且标识符分布相似，表明存在协同操作。
- **行为指纹识别**：除了 IP 地址，系统还使用 TLS 指纹（JA4）和用户代理模式来识别自动化流量。来自轮换 IP 的相同指纹是一个明显的迹象。
- **引荐来源分析**：真实的技能会留下痕迹（推文、README、Discord 讨论串）。Agent（智能体）会将安装激增与缺乏任何外部信号的情况进行交叉比对。凭空增长就是一个信号。

Temporal distribution: Legitimate installs follow human rhythms, like spikes after a tweet, gradual rises from tutorials, and quiet nights. Gaming looks like uniform distributions around the clock with no correlation to any external event.

Volume coherence: The agent compares each skill's install-to-unique-user ratio against the ecosystem average. A brand-new skill from an unknown repo appearing in the top 10 with no organic trail deserves scrutiny.

Cross-source correlation: Multiple "different" repos surging at exactly the same time with similar identifier distributions suggests coordination.

Behavioral fingerprinting: Beyond IP addresses, the system uses TLS fingerprints (JA4) and user-agent patterns to identify automated traffic. Identical fingerprints from rotating IPs are a telltale sign.

Referral trail analysis: Real skills leave traces (tweets, READMEs, Discord threads). The agent cross-references install spikes with the absence of any external signal. Growth from nowhere is a signal.

当 Agent（智能体）标记一个来源时，它会生成一份报告，包含检测到的模式、统计证据、严重性评分以及建议采取的措施，措施范围从轻度限制（通过数学函数抑制虚增的计数）到完全从排行榜中排除。人工会审查报告并确认或驳回。确认的操作会成为我们分析管道中的规则，并在后续查询时自动执行。

系统会随着时间的推移而改进，因为已确认的滥用模式会教会 Agent（智能体）下一步寻找什么，而被驳回的误报则会优化阈值。这些规则在 SQL 层中不断积累，成为生态系统所遇到并已处理的每一次刷量尝试的记录。

## 数据标准化

刷量并非唯一的数据完整性问题。同一个技能可能以不同的名称出现，例如仓库重组、所有者重命名其 GitHub 账户，或者技能从多个仓库合并到一个仓库。如果不进行标准化，排行榜会将单个技能的安装量分散到重复的条目中。

一个标准化流程会检测相同的所有者-技能组合是否以不同名称或不同仓库存在，并在查询时合并它们的计数。原始遥测数据保持不变；标准化是一个转换层，我们可以随时更新，而无需修改底层数据。

## 自动驾驶循环

该系统无需每日人工关注：

1.  新技能在首次安装时自动审核。安全的技能会显示。可疑的技能会触发审核。
2.  更新的技能在其内容哈希值发生变化时会重新审核。
3.  一个 AI Agent（智能体）定期分析安装模式，并标记异常以供审核。
4.  对标记来源的人工决策会转化为自动化规则。
5.  过期的审核会自动收到 24 小时提醒。
6.  标准化处理仓库被重命名和重组带来的混乱现实。

New skills get reviewed automatically on first install. Safe ones appear. Suspicious ones trigger a review.

Updated skills get re-reviewed when their content hash changes.

An AI agent periodically analyzes install patterns and flags anomalies for review.

Human decisions on flagged sources become automated rules.

Stale reviews get automatic 24-hour reminders.

规范化处理了仓库被重命名和重组这一混乱的现实。

唯一需要人工介入的环节是：当Slack发出提醒时进行查看（这种情况很少见，因为大多数技能都是安全的），以及确认或驳回滥用检测Agent的发现。系统会随着时间的推移自行加强防御，而每一步都需要人工确认。

其结果是形成了一个基本可以自主运行的排行榜。审查、欺诈检测、规范化和规则执行都无需人工每日关注，并且系统在这些方面会随着时间的推移而不断改进。当我们确实需要介入时，这些决策又会反馈到自动化流程中。

请访问skills.sh浏览排行榜。试试我们的React最佳实践技能：

```
1npx skills add vercel-labs/agent-skills
```

---

> 本文由AI自动翻译，原文链接：[Building a self-driving skills.sh leaderboard - Vercel](https://vercel.com/blog/building-a-self-driving-skills-sh-leaderboard)
> 
> 翻译时间：2026-02-11 04:34
