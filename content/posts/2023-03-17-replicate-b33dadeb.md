---
title: 微调LLaMA让霍默·辛普森附体
title_original: Fine-tune LLaMA to speak like Homer Simpson – Replicate blog
date: '2023-03-17'
source: Replicate Blog
source_url: https://replicate.com/blog/fine-tune-llama-to-speak-like-homer-simpson
author: ''
summary: 本文介绍了如何通过微调开源语言模型LLaMA，使其模仿《辛普森一家》中霍默·辛普森的口吻说话。作者使用Kaggle上的剧本数据集，提取前12季共6.1万行对话，并修改训练提示词，让模型在场景上下文中完成角色台词。整个微调过程仅需90分钟和少量数据，就能生成具有角色特色的文本。文章强调开源模型让这种个性化定制变得简单快捷，并鼓励读者尝试类似应用。
categories:
- AI研究
tags:
- LLaMA
- 微调
- 开源模型
- 角色生成
- 自然语言处理
draft: false
translated_at: '2026-06-03T06:52:09.340582'
---

- Replicate  
- 博客  

# 微调LLaMA，让它像霍默·辛普森一样说话  

- bfirsh  

昨天我们解释了如何复现Alpaca，这是一个经过微调的LLaMA版本，能够遵循指令。  

它是在一组指令和答案的数据集上训练而成的，目的是将其转变为助手。事实证明，你可以用电视剧的剧本替换这个数据集，它就会以该电视剧角色的口吻说话。  

我们对这个过程如此简单感到惊讶。只需少量数据（约6万行对话）和90分钟的微调，就能让LLaMA以数据集中的口吻输出文本。  

它变成了一个非常出色的霍默·辛普森机器人。偶尔还挺有趣的：  

以下是我们的制作方法。  

## 我们做了什么  

首先，从Kaggle的《辛普森一家》数据集中获取`simpso ns_script_lines.csv`。这个文件包含了截至第27季的所有《辛普森一家》剧集的剧本。  

我们只提取了第1到12季的数据，因为这几季是精华。最终的数据集包含6.1万行对话和110万个Token。  

我们希望训练LLaMA来复现角色的口吻。LLaMA最初被设计成一个有用的助手，而这项任务略有不同。  

为了实现这一点，我们为数据集中的所有场景生成了一个数据集，包含给定场景中的前面对话、下一句台词的角色以及该台词。以下是一个示例：  

```
{'previous': 'Marge Simpson: Ooo, careful, Homer.',
 'character': 'Homer Simpson',
 'line': "There's no time to be careful."}
```  

这里有一个笔记本，展示了解析过程。  

解析完这些台词后，我们修改了现有Alpaca代码库中的训练提示词和脚本，使模型被提示在场景上下文中完成台词。  

提示词如下：  

```
"Below is a script from the American animated sitcom The Simpsons.\
 Write a response that completes {character}'s last line in the \
conversation. \n\n{previous}\n{character}:";

```  

从这里开始，后续流程与训练Alpaca相同，我们在昨天的博客文章中已经介绍过。  

我们对训练脚本做了一些修改，因此在你检出仓库后，需要切换到`homerbot`分支：  

```
git clone https://github.com/replicate/cog_stanford_alpaca
cd cog_stanford_alpaca
git checkout homerbot
```  

一旦你有了训练好的模型，就可以通过类似以下的cog predict命令生成剧本：  

```
cog predict -i "Marge Simpson: how was your day, Homer?" -i max_length=512 -i character="Homer Simpson"
```  

## 下一步  

原版LLaMA和GPT-4难以生成具有《辛普森一家》口吻的输出。微调LLaMA使其拥有特定角色的口吻出乎意料地快速且简单，而这之所以可能，完全是因为它是开源的。  

我们将发布更多关于调整开源语言模型的指南。在Twitter上关注我们以获取最新动态。  

我们也迫不及待想看到你的作品。加入Discord上的#llama频道，分享你的成果。

---

> 本文由AI自动翻译，原文链接：[Fine-tune LLaMA to speak like Homer Simpson – Replicate blog](https://replicate.com/blog/fine-tune-llama-to-speak-like-homer-simpson)
> 
> 翻译时间：2026-06-03 06:52
