---
title: 前沿模型在企业IT任务基准测试中得分不足50%
title_original: 'ITBench-AA: Frontier Models Score Below 50% on the First Benchmark
  for Agentic Enterprise IT Tasks — by Artificial Analysis and IBM'
date: '2026-05-27'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ibm-research/itbench-aa
author: ''
summary: Artificial Analysis与IBM联合推出ITBench-AA，首个评估模型在企业IT任务中Agent能力的基准测试，聚焦站点可靠性工程（SRE）任务。测试显示，所有前沿模型得分均低于50%，其中Claude
  Opus 4.7以47%领先。模型需通过读取日志、追踪依赖关系诊断Kubernetes事件根因。研究发现，更长推理轨迹并未提升准确性，过度调查反而导致误报。开源模型Gemma
  4 31B在成本效率上表现突出。
categories:
- AI研究
tags:
- ITBench-AA
- 企业IT
- Agent基准测试
- 站点可靠性工程
- 前沿模型
draft: false
translated_at: '2026-05-28T06:09:34.902703'
---

# ITBench-AA：前沿模型在首个企业IT任务Agent基准测试中得分低于50%——来自Artificial Analysis和IBM

Artificial Analysis与IBM软件创新实验室联合推出ITBench-AA，这是评估模型在企业IT任务中Agent能力的新系列基准测试中的首个，从站点可靠性工程任务开始，前沿模型得分低于50%。

ITBench-AA的SRE任务对模型在Kubernetes事件响应中的表现进行基准测试，模型和Agent必须通过读取日志、追踪依赖关系以及识别复杂基础设施中的根因实体来诊断实时系统。底层ITBench数据集由IBM开发，利用了其在企业IT运营方面的深厚专业知识。

Artificial Analysis在过去6个月中与IBM密切合作，开发了用于前沿AI评估的数据集实现，从站点可靠性工程开始，并将逐步扩展到财务运营和首席信息安全官任务。

![image](/images/posts/42751824258a.png)

## 主要发现：

1. Claude Opus 4.7（自适应推理，最大努力）以47%领先，其次是GPT-5.5（xhigh）46%和Qwen3.7 Max 42%。
2. 所有前沿模型得分均低于50%，使ITBench-AA SRE成为我们套件中饱和度最低的Agent基准之一。作为对比，前沿模型在Terminal-Bench上的得分要高得多。
3. 轮次变化近3倍，更长的轨迹并未转化为更高的准确性。GPT-5.5（xhigh）平均每任务31轮，准确率46%，而Gemini 3.1 Pro Preview平均83轮，准确率30%。过度调查的模型往往会将上游故障注入机制或并发症状作为误报呈现。
4. GLM-5.1（推理）以40%领先开源权重模型，与Gemini 3.5 Flash（高）基本持平。DeepSeek V4 Pro（推理，最大努力）以38%紧随其后，Gemma 4 31B（推理）以37%位列其后，领先于Gemini 3.1 Pro Preview的30%。

## ITBench-AA SRE概述：

- 共59个SRE任务：40个公开任务和19个全新、保留任务
- 每个任务提供一个Kubernetes事件快照，包含告警、事件、追踪、指标、日志和应用拓扑。模型必须识别导致事件的最小独立根因Kubernetes实体集。
- 故障涵盖典型的SRE故障模式，包括基础设施、服务、应用和混沌注入事件，如资源配额耗尽、部署失败、连接池耗尽和网络分区。
方法细节：
- Agent框架：每个任务由模型在我们的开源Stirrup参考框架中运行解决，具有对包含相关日志和快照的沙盒文件系统的shell访问权限。每任务100轮上限，每任务3次重复。
- 模型和Agent提交他们认为导致事件的根因实体列表（Kubernetes部署、服务、Pod等）。每次提交与IBM提供的真实根因集进行比较。
- 评分使用全召回率下的平均精度：如果模型遗漏任何真实根因，则该次重复得分为0.0。如果识别出所有根因，则获得等于其精度的分数——提交实体中实际根因的比例，即真阳性/（真阳性+假阳性）。标题分数是59个任务×3次重复的平均值。
- 框架（Stirrup）在所有评估模型中保持不变，实现模型间的公平比较。

## 亮点

1. 任务要求Agent通过shell命令调查Kubernetes事件快照，并提交结构化的JSON诊断结果，识别负责的根因实体。
在一个公开的SRE任务中，Agent看到前端路径中的用户可见故障。它使用shell命令检查离线快照：查看告警显示事件窗口，然后追踪/日志将故障缩小到前端流量。拓扑确定了受影响的服务，Kubernetes清单显示阻止前端的网络策略。成功诊断识别出负责的根因实体：otel-demo/NetworkPolicy/frontend-block-all-ports。

![image](/images/posts/2b9ab0e7ab7e.png)

1. 更多轮次并不意味着更好的答案。提交超出真实根因的额外贡献实体的模型会受到惩罚：识别出正确根因但添加上游机制（例如，chaos-mesh控制器）或并发症状在召回率门控精度下被视为误报。这就是为什么一些长轨迹模型表现不如简洁模型：Gemini 3.1 Pro Preview平均83轮，得分30%，而Gemma 4 31B（推理）平均58轮，得分37%。

![image](/images/posts/96b1015a021c.png)

![image](/images/posts/54479e14a891.png)

1. 开源权重模型处于ITBench-AA SRE的成本前沿。Gemma 4 31B（推理）以每任务0.14美元得分37%，在得分和成本上均优于Gemini 3.1 Pro Preview（每任务2.23美元，30%）。GLM-5.1（推理）以每任务1.23美元得分40%，以更低成本匹配Gemini 3.5 Flash（高）（1.70美元）的得分。Claude Opus 4.7（自适应推理，最大努力）以47%领先排行榜，但也是最昂贵的，每任务5.38美元。

![image](/images/posts/1157e35ea55a.png)

### ITBench-AA与@IBM基于其ITBench基准合作构建。

- 更多信息请参见：ITBench论文 on arXiv:https://arxiv.org/abs/2502.05352
- GitHub:https://github.com/itbench-hub/ITBench
- ITBench-AA排行榜:https://artificialanalysis.ai/evaluations/itbench-aa
- ITBench-AA HuggingFace仓库:https://huggingface.co/datasets/ArtificialAnalysis/ITBench-AA/tree/main/sre

---

> 本文由AI自动翻译，原文链接：[ITBench-AA: Frontier Models Score Below 50% on the First Benchmark for Agentic Enterprise IT Tasks — by Artificial Analysis and IBM](https://huggingface.co/blog/ibm-research/itbench-aa)
> 
> 翻译时间：2026-05-28 06:09
