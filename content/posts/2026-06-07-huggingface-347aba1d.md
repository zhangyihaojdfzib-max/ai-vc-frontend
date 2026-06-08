---
title: 神奇数字假牙：一个失败项目的反思
title_original: Amazing Digital Dentures (a failed project)
date: '2026-06-07'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/build-small-hackathon/amazingdigitaldentures
author: ''
summary: 本文作者受动画《神奇数字马戏团》启发，尝试开发一个AI驱动的数字宠物，旨在通过生成冒险任务提升用户生产力。项目最初设想为游戏化的待办清单，后转向纯冒险生成，但屡遭失败：使用Nemotron
  30b模型时，长提示词导致游戏无法运行；引入技能卡片和RAG技术后，仍因上下文限制或生成内容不完整而失败。最终项目降级为简单的HTML玩具制作器，仅能生成基础小游戏。作者分享了技术挑战与转型过程，并寻求建议。
categories:
- AI产品
tags:
- AI项目
- 失败经验
- 游戏开发
- Nemotron
- RAG
draft: false
translated_at: '2026-06-08T06:33:13.379237'
---

# 神奇数字假牙（一个失败的项目）

我的想法既简单又有些复杂。你们看过《神奇数字马戏团》吗？这是一部动画片，片中有一副名为凯恩的AI假牙，它生活在一个虚拟马戏团里，与一些真实人类的数字克隆体为伴，每天为它们创造并发送冒险任务。我的项目正是受此启发。

一个数字宠物，它会给你发送冒险任务，这些任务可能对你现实世界的生产力有所帮助——就像一个伪装成游戏的过度设计的待办清单。

后来我放弃了待办清单的部分，完全投入到"创造冒险"的功能上，结果适得其反。我当时使用的是Nemotron 30b模型。

我希望它能用Three.js创建完整的游戏，我尝试了很多方法。

首先是简单的长提示词，写一段长提示词解释要做什么以及怎么做，但模型经常给出无法运行的游戏，失败了。

然后我尝试添加技能卡片，就是这个：https://github.com/github/awesome-copilot/blob/main/skills/game-engine/SKILL.md，但也失败了，它撑爆了我为节省算力而设置的短上下文窗口，结果适得其反。于是我增加了上下文窗口，但问题依然没有解决。

所以我用Codex将这些技能提炼到一个文本文件中，并使用RAG（检索增强生成）来处理，这确实有效，但生成的游戏仍然无法完全运行，总有些问题导致最终画面一片空白。

现在我已经放弃了，这个项目变成了别的东西——一个简单的HTML玩具制作器。它可以一次性生成简单的HTML内容，但不是游戏。我用它制作了时钟、待办清单、贪吃蛇和打砖块这类东西，但更复杂的如俄罗斯方块就会出错：https://huggingface.co/spaces/build-small-hackathon/AmazingDigitalPetDentures

我现在正在考虑转向一个不同的想法，如果能得到任何建议，我将不胜感激。

---

> 本文由AI自动翻译，原文链接：[Amazing Digital Dentures (a failed project)](https://huggingface.co/blog/build-small-hackathon/amazingdigitaldentures)
> 
> 翻译时间：2026-06-08 06:33
