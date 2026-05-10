---
title: OncoAgent：隐私保护肿瘤临床决策的双层多Agent框架
title_original: '"OncoAgent: A Dual-Tier Multi-Agent Framework for Privacy-Preserving
  Oncology Clinical Decision Support"'
date: '2026-05-09'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/oncoagent-official-paper
author: ''
summary: OncoAgent是一个开源的、隐私保护的肿瘤学临床决策支持系统，采用双层微调LLM架构与多Agent LangGraph拓扑，结合四阶段校正RAG流水线和三层反射安全验证器。系统通过复杂度评分器将查询路由至9B或27B参数模型，基于AMD
  Instinct MI300X硬件在约50分钟内完成全数据集微调，实现56倍吞吐量加速。该系统100%开源可本地部署，消除云API依赖，保障患者数据主权。
categories:
- AI研究
tags:
- 肿瘤学AI
- 多Agent系统
- 检索增强生成
- 隐私保护
- 临床决策支持
draft: false
translated_at: '2026-05-10T05:36:03.706844'
---

# "OncoAgent：一个用于隐私保护肿瘤学临床决策支持的双层多Agent框架"

缩略图：https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/blog/oncoagent-thumbnail.png作者：

- user: oncoagent-research
标签：
- 肿瘤学
- 多Agent
- LangGraph
- RAG（检索增强生成）
- QLoRA
- AMD
- 开源
- 临床AI
- 医疗保健

# OncoAgent：一个用于隐私保护肿瘤学临床决策支持的双层多Agent框架

技术预印本 · 2026年5月 · OncoAgent研究团队

## 摘要

我们提出OncoAgent，一个开源的、隐私保护的肿瘤学临床决策支持系统。OncoAgent将双层微调LLM架构与最先进的多Agent LangGraph拓扑结构、覆盖70余项医师级NCCN和ESMO指南的四阶段校正RAG流水线，以及执行严格零PHI策略的三层反射安全验证器相结合。

该系统通过累加复杂度评分器将临床查询路由至9B参数速度优化模型（第一层）或27B深度推理模型（第二层），两者均通过QLoRA在包含266,854个真实及合成肿瘤病例的语料库上进行微调，使用基于AMD Instinct MI300X硬件（192 GB HBM3）的Unsloth框架完成。

MI300X上的序列打包技术使得全数据集微调在约50分钟内完成——相比基于API的生成实现了56倍吞吐量加速。修复后，CRAG文档评分达到100%成功率，平均RAG置信得分为2.3+。整个系统100%开源且可本地部署，消除了专有云API依赖，保障了患者数据主权。

关键词：临床决策支持，肿瘤学AI，多Agent系统，检索增强生成，QLoRA，AMD ROCm，开源医疗AI，人在回路安全，LangGraph，校正RAG

## 1. 引言

肿瘤学是临床医学中信息密度最高、认知负荷最大的领域之一。从美国国家综合癌症网络（NCCN）到欧洲肿瘤内科学会（ESMO），循证指南的数量、异质性和快速演进，在已发表证据与临床实践之间造成了持续的知识鸿沟。

AI辅助临床决策支持系统在弥合这一鸿沟方面具有变革性潜力，然而大多数商用系统在三个关键方面存在缺陷：

1. 产生未基于已验证指南的幻觉式推荐
2. 依赖云API，无法在隐私敏感的医院环境中进行本地部署
3. 采用单一LLM架构，在处理复杂多合并症病例时易出现上下文饱和

OncoAgent围绕三个核心原则设计：

- 架构分解：临床推理被分解至八个专门的LangGraph节点，每个节点具有边界明确、可审计的功能。
- 有据生成：所有模型输出通过四阶段检索流水线（含显式相关性门控）锚定至精选向量知识库。
- 硬件主权：完整的推理和训练栈原生运行于AMD Instinct MI300X，使用ROCm和开源框架——实现医院部署无需数据外泄。

---

> 本文由AI自动翻译，原文链接：["OncoAgent: A Dual-Tier Multi-Agent Framework for Privacy-Preserving Oncology Clinical Decision Support"](https://huggingface.co/blog/lablab-ai-amd-developer-hackathon/oncoagent-official-paper)
> 
> 翻译时间：2026-05-10 05:36
