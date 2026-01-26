---
title: 用文件系统和bash构建Agent：更简单高效的架构
title_original: How to build agents with filesystems and bash - Vercel
date: '2026-01-09'
source: Vercel Blog
source_url: https://vercel.com/blog/how-to-build-agents-with-filesystems-and-bash
author: ''
summary: 本文提出了一种创新的Agent架构设计思路：利用文件系统和bash命令替代复杂的定制工具。作者发现，LLM经过海量代码训练后，已具备出色的文件系统操作能力。通过将客户支持工单、销售记录等数据结构化映射到文件目录，让Agent使用ls、find、grep等Unix命令自主探索和检索所需上下文，不仅将销售通话摘要Agent的成本从1美元降至0.25美元，还提升了输出质量。这种方法避免了提示词过长或向量搜索不精确的问题，实现了精确检索和最小化上下文加载。
categories:
- AI产品
tags:
- Agent架构
- 文件系统
- LLM应用
- 成本优化
- 上下文管理
draft: false
translated_at: '2026-01-10T04:12:47.003713'
---

最佳的Agent架构早已存在于你的终端中

我们许多人都构建了复杂的工具来为Agent提供正确的信息。这种做法很脆弱，因为我们在猜测模型需要什么，而不是让它自己寻找所需。我们找到了一种更简单的方法。我们用文件系统工具和bash工具替换了内部Agent中的大部分定制工具。我们的销售通话摘要Agent在Claude Opus 4.5上，每次通话的成本从约1美元降至约0.25美元，并且输出质量有所提升。我们对我们的文本转SQL Agent `d0` 也采用了同样的方法。

这背后的理念是，LLM（大语言模型）已经接受了海量代码的训练。它们花费了无数时间来浏览目录、在文件中搜索以及管理复杂代码库的状态。如果Agent擅长处理代码的文件系统操作，那么它们也擅长处理任何事物的文件系统操作。Agent已经理解了文件系统。

客户支持工单、销售通话记录、CRM数据、对话历史。将它们结构化为文件，给Agent提供bash，模型就会运用其在代码导航中使用的相同能力。

## Agent如何读取文件系统

Agent在一个沙箱中运行，你的数据被结构化为文件。当它需要上下文时，它会使用Unix命令探索文件系统，提取相关内容，并将其发送给LLM。

```
1Agent接收任务2    ↓3探索文件系统 (ls, find)4    ↓5搜索相关内容 (grep, cat)6    ↓7发送上下文 + 请求给LLM8    ↓9返回结构化输出
```

Agent及其工具执行运行在独立的计算资源上。你信任Agent的推理能力，但沙箱隔离了它实际能执行的操作。

## 为何文件系统适用于上下文管理

处理Agent上下文的典型方法要么是将所有内容塞入提示词，要么是使用向量搜索。塞入提示词会触及Token限制。向量搜索适用于语义相似性，但当需要从结构化数据中获取特定值时，返回的结果不够精确。

文件系统提供了不同的权衡。

结构匹配你的领域。客户记录、工单历史、CRM数据。这些都有自然的层次结构，可以直接映射到目录。你不是将关系扁平化为嵌入。

检索是精确的。`grep -r "pricing objection" transcripts/` 返回精确匹配。当你需要一个特定值时，你就能得到那个值。

上下文保持最小化。Agent按需加载文件。一个大型记录不会预先进入提示词。Agent读取元数据，搜索相关部分，然后只提取所需内容。

## 将你的领域映射到文件

让我们看一些具体示例，了解不同领域如何映射到文件系统结构。

示例1：客户支持系统

与其将原始JSON丢给Agent，不如将其结构化：

```
1/customers/2  /cust_12345/3    profile.json          # 高层级信息4    tickets/5      ticket_001.md       # 每个工单6      ticket_002.md7    conversations/8      2024-01-15.txt      # 每日对话日志9    preferences.json
```

当客户询问“我的问题是如何解决的？”时，Agent可以`ls`工单目录，`grep`搜索“resolved”，并且只读取相关文件。

示例2：文档分析系统

```
1/documents/2  /uploaded/3    contract_abc123.pdf4    invoice_def456.pdf5  /extracted/6    contract_abc123.txt7    invoice_def456.txt8  /analysis/9    contract_abc123/10      summary.md11      key_terms.json12      risk_assessment.md13  14/templates/15  contract_analysis_prompt.md16  invoice_validation_rules.md
```

原始输入放在一处，处理后的输出放在结构化目录中。Agent可以参考之前的分析而无需重新处理。

## 案例研究：销售通话摘要Agent

我们使用此架构构建了一个[销售通话摘要模板](https://vercel.com/templates/ai/sales-call-summary)。Agent分析销售通话记录，并生成包含异议、行动项和见解的结构化摘要。

Agent看到这样的文件结构：

```
1gong-calls/2  demo-call-001-companyname-product-demo.md     # 当前通话记录3  metadata.json                                 # 通话元数据4  previous-calls/5    demo-call-000-discovery-call.md             # 之前的发现通话6    demo-call-intro-initial-call.md             # 初始介绍通话7
8salesforce/9  account.md                                    # CRM账户记录10  opportunity.md                                # 交易/商机详情11  contacts.md                                   # 联系人资料12
13slack/14  slack-channel.md                              # Slack历史15
16research/17  company-research.md                           # 公司背景18  competitive-intel.md                          # 竞品分析19
20playbooks/21  sales-playbook.md                             # 内部销售手册22

```

Agent像探索代码库一样探索这个结构：

```
1# 探索可用的内容2$ ls sales-calls/3customer-call-123456-q4.md4metadata.json5
6# 读取元数据7$ cat sales-calls/metadata.json8
9# 查找异议10$ grep -i "concern\|worried\|issue\|problem" sales-calls/*.md
```

其理念是，Agent将通话记录视为代码库。它搜索模式、读取部分内容并构建上下文，就像调试代码一样。无需自定义检索逻辑。Agent使用它已经知道如何使用的工具来决定需要什么上下文。它能处理我们从未预料到的边缘情况，因为它处理的是原始信息，而不是我们定义的参数。

我们将在另一篇文章中更深入地探讨销售通话摘要Agent。

## 为何你应该使用bash和文件系统

原生模型能力。`grep`、`cat`、`find`、`awk`。这些不是我们要教的新技能。LLM在训练过程中已经见过这些工具数十亿次。它们是原生操作，不是附加行为。

面向未来的架构。随着模型在编码方面变得更好，你的Agent也会变得更好。代码理解能力的每一次提升都能直接转化。你是在利用训练分布，而不是与之对抗。

可调试性。当Agent失败时，你可以确切地看到它读取了哪些文件以及运行了哪些命令。执行路径是可见的。没有黑盒。

通过隔离实现安全性。沙箱允许Agent探索文件，而无需访问生产系统。你信任的是推理能力，而不是执行环境。

需要维护的代码更少。无需为每种数据类型构建检索管道，你只需将文件写入目录结构。Agent会处理其余的事情。

## 开始使用

每个Agent都需要文件系统和bash。如果你正在构建一个Agent，请抵制创建自定义工具的冲动。相反，问问自己：我能将其表示为文件吗？

我们最近开源了 `bash-tool`，这是一个支持此模式的专用工具。

1.  [AI SDK](https://sdk.vercel.ai/docs) 用于工具执行和模型调用
2.  [bash-tool](https://github.com/vercel-labs/bash-tool) 用于沙箱化文件系统访问
3.  [销售通话摘要模板](https://vercel.com/templates/ai/sales-call-summary) 用于查看完整模式并一键开始使用

Agent的未来可能简单得出奇。也许最好的架构就是几乎没有架构。仅仅是文件系统和bash。

[开始使用文件系统Agent](https://vercel.com/templates/ai/sales-call-summary)

销售通话摘要模板展示了生产环境中的文件系统和bash模式。将其部署在Vercel上，实时观察Agent探索文件。


> 本文由AI自动翻译，原文链接：[How to build agents with filesystems and bash - Vercel](https://vercel.com/blog/how-to-build-agents-with-filesystems-and-bash)
> 
> 翻译时间：2026-01-10 04:12
