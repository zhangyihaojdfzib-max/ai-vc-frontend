---
title: 从结构中学习：Discord的实体关系嵌入技术
title_original: 'Learning From Structure: Discord’s Entity-Relationship Embeddings'
date: '2024-09-19'
source: Discord Engineering
source_url: https://discord.com/blog/learning-from-structure-discords-entity-relationship-embeddings
author: ''
summary: 本文介绍了Discord开发的DERE（Discord实体关系嵌入）技术，该技术借鉴了大语言模型中词嵌入的思想，将服务器、用户、游戏等实体及其关系表示为向量。与自然语言处理中通过邻近词定义关系类似，DERE通过实体间的交互关系构建嵌入表示，使机器学习工程师能够更高效地构建模型并从数据中获取洞察。这项技术为处理复杂结构化数据提供了新的思路，提升了机器学习应用的开发效率。
categories:
- AI基础设施
tags:
- 嵌入技术
- 实体关系
- 机器学习
- Discord
- 向量表示
draft: false
translated_at: '2026-01-28T04:46:05.251321'
---

得益于大语言模型（或称LLM），嵌入已变得司空见惯。嵌入是一种简单而强大的结构，能将复杂数据捕获为一系列数字——即向量——并且是在机器学习模型中表示多种事物的自然方式。在LLM中，嵌入代表单词（或Token）。在Discord，我们构建了DERE，即Discord的实体关系嵌入，它用于表示服务器（本文中将使用其技术术语“公会”）、用户、游戏及其他实体。正如LLM的嵌入使得快速轻松地构建基于文本的应用程序变得容易一样，这些嵌入也让Discord的机器学习工程师能够比以往更快地构建模型并从数据中生成洞察。

![一张折线图，展示了20年间对“嵌入”一词兴趣程度的变化。](/images/posts/4a74357682ab.png)

如果您熟悉自然语言处理，这项技术常用于从文本中构建预训练的词表示。在自然语言处理设置中，词与词之间的关系由任何给定词的邻近词定义。因此，在句子“the cat sat”中，可以说“cat”与“the”和“sat”存在关系。

![自然语言处理中关系的一个示例。单词“the”是“cat”的邻近词，“cat”是“sat”的邻近词。这等同于一种传递关系，即“the”与“sat”相关，因为“cat”与两者都相关。](/images/posts/0cffccba2255.png)

---

> 本文由AI自动翻译，原文链接：[Learning From Structure: Discord’s Entity-Relationship Embeddings](https://discord.com/blog/learning-from-structure-discords-entity-relationship-embeddings)
> 
> 翻译时间：2026-01-28 04:46
