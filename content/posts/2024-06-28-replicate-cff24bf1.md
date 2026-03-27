---
title: Replicate情报第6期：Gemma2发布、模型排行更新与推理优化
title_original: 'Replicate Intelligence #6 – Replicate blog'
date: '2024-06-28'
source: Replicate Blog
source_url: https://replicate.com/blog/replicate-intelligence-2024-06-28
author: ''
summary: 本文是Replicate的每周AI简报，由deepfates汇总。主要内容包括：谷歌发布新的Gemma2语言模型（9B和27B规格），并探讨其训练特点；Huggingface更新了语言模型排行榜，引入更难的评估基准，Qwen
  72B表现领先；Character.AI分享了如何优化AI推理以实现每秒处理2万个查询的技术细节；以及关于如何从Stable Diffusion 3获得最佳效果的实用指南。
categories:
- 技术趋势
tags:
- AI模型
- 语言模型
- 推理优化
- 开源工具
- 每周简报
draft: false
translated_at: '2026-03-27T05:07:25.508604'
---

- Replicate
- Blog

# Replicate 情报 #6

- deepfates

欢迎来到 Replicate 的每周简报！每周，我们将为您带来最新的开源AI模型、工具和研究动态。人们正在创造很酷的东西，我们想与您分享。闲话少叙，有请我们的驻场黑客 deepfates，带来他对本周AI领域的无滤镜解读。

## 编者按

对我来说这是漫长的一周，在真正能处理完所有事情之前，我还有更多忙碌的日子。请原谅我给您发送如此简短的信件。我实在不忍心什么都不发。

---deepfates

## 趋势模型

## 谷歌发布新语言模型

新的 Gemma2 模型发布了 9b 和 27b 两种规格。它们似乎在 Token 上训练过度了，这至少从 Llama3 以来似乎已成趋势。它们也是从更大的 Gemini 模型蒸馏出来的吗？每个人都在谈论交替的全局/局部注意力层，这在 Character.AI 的博客文章（见下文）中也有提及……

post|paper|try on replicate

## 酷炫工具

## 语言模型排行榜更新

Huggingface 更新了他们之前的元基准测试，纳入了更难的评估。他们选择了高质量、可靠、未被广泛污染到数据集中、并能衡量有趣技能的评估。到目前为止，排名符合我的直觉判断：Qwen 72b 遥遥领先于 Meta LLama 3，而后者又略微领先于 Mixtral 8x22B，依此类推。

post|leaderboard

## 研究雷达

## 如何真正优化AI推理

Character.AI 每秒处理 20,000 个推理查询。这是一份简洁而具体的指南，介绍了他们为实现此目标所使用的优化技术——包括前面提到的混合注意力，以及针对他们必须在对话的每一轮都包含的冗长、重复的聊天历史所采用的状态缓存。

## 更新日志

## 如何从 Stable Diffusion 3 获得最佳效果

Stable Diffusion 3 已经发布几周了。我们的内部AI实验员 @fofrAI 已经取得了一些很棒的结果，但这并不总是那么容易。在我们的博客文章中，了解如何选择合适的版本、制作高质量的提示词并进行正确的设置。

## 暂时告别

就这样。这周真的就发生了这些事。我说错了吗？回复告诉我。我下周会致歉。

--- deepfates

---

> 本文由AI自动翻译，原文链接：[Replicate Intelligence #6 – Replicate blog](https://replicate.com/blog/replicate-intelligence-2024-06-28)
> 
> 翻译时间：2026-03-27 05:07
