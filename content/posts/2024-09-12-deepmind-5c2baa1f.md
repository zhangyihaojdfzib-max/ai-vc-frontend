---
title: 机器人灵巧性新突破：ALOHA Unleashed与DemoStart系统
title_original: Our latest advances in robot dexterity
date: '2024-09-12'
source: Google DeepMind
source_url: https://deepmind.google/blog/advances-in-robot-dexterity/
author: ''
summary: 本文介绍了Google DeepMind在机器人灵巧性方面的两项最新AI进展。ALOHA Unleashed系统基于低成本开源双臂硬件平台，通过改进的人体工程学设计和扩散学习方法，使机器人能够从人类演示中学习并执行系鞋带、挂衣服等复杂双臂任务。DemoStart系统则利用强化学习与少量模拟演示，在MuJoCo模拟器中训练多指机器人手掌握精细操作技能，并成功迁移到现实世界，大幅降低了物理实验的成本与时间。这些进展为机器人在动态环境中执行实用任务奠定了基础。
categories:
- AI研究
tags:
- 机器人学习
- 模仿学习
- 强化学习
- 灵巧操作
- 模拟到现实迁移
draft: false
translated_at: '2026-02-13T04:21:26.620738'
---

# 我们在机器人灵巧性方面的最新进展

机器人团队

![](/images/posts/a4554779261b.jpg)

两个新的人工智能系统，ALOHA Unleashed 和 DemoStart，帮助机器人学习执行需要灵巧运动的复杂任务。

人们每天执行许多任务，例如系鞋带或拧紧螺丝。但对于机器人来说，学习这些高度灵巧的任务极其困难。为了让机器人在人们的生活中更有用，它们需要更好地在动态环境中与物理物体进行接触。

今天，我们介绍两篇新论文，展示了我们在机器人灵巧性研究领域的最新人工智能进展：**ALOHA Unleashed** 帮助机器人学习执行复杂新颖的双臂操作任务；以及 **DemoStart** 利用模拟来提升多指机器人手在现实世界中的性能。

通过帮助机器人从人类演示中学习并将图像转化为动作，这些系统为能够执行各种有用任务的机器人铺平了道路。

## 利用两个机械臂改进模仿学习

迄今为止，大多数先进的人工智能机器人只能使用单臂抓取和放置物体。在我们的新论文中，我们提出了 ALOHA Unleashed，它在双臂操作中实现了高度的灵巧性。通过这种新方法，我们的机器人学会了系鞋带、挂衬衫、修理另一个机器人、插入齿轮，甚至清洁厨房。

一个双臂机器人整理鞋带并将其系成蝴蝶结的示例。

一个双臂机器人将一件 Polo 衫在桌上铺开、挂上衣架然后挂到架子上的示例。

一个双臂机器人修理另一个机器人的示例。

ALOHA Unleashed 方法建立在我们基于斯坦福大学原始 **ALOHA**（一个低成本开源的双臂遥操作硬件系统）的 **ALOHA 2** 平台之上。

ALOHA 2 比之前的系统灵巧得多，因为它有两只可以轻松进行遥操作以用于训练和数据收集目的的手，并且它允许机器人用更少的演示来学习如何执行新任务。

在我们最新的系统中，我们还改进了机器人硬件的人体工程学并增强了学习过程。首先，我们通过远程操作机器人的行为来收集演示数据，执行诸如系鞋带和挂T恤等困难任务。接下来，我们应用了一种扩散方法，从随机噪声中预测机器人动作，类似于我们的 **Imagen** 模型生成图像的方式。这有助于机器人从数据中学习，从而能够独立执行相同的任务。

## 从少量模拟演示中学习机器人行为

控制一个灵巧的机器人手是一项复杂的任务，每增加一个手指、关节和传感器，复杂性都会增加。在另一篇新论文中，我们提出了 DemoStart，它使用强化学习算法帮助机器人在模拟中获得灵巧行为。这些习得的行为对于复杂的实体（如多指手）特别有用。

DemoStart 首先从简单的状态学习，随着时间的推移，开始从更困难的状态学习，直到尽其所能掌握一项任务。与通常为相同目的从现实世界示例中学习所需的数量相比，它在模拟中学习如何解决一项任务所需的模拟演示数量减少了 100 倍。

该机器人在模拟中的许多不同任务上取得了超过 98% 的成功率，包括重新定向以显示特定颜色的立方体、拧紧螺母和螺栓以及整理工具。在现实世界设置中，它在立方体重定向和提升任务上取得了 97% 的成功率，在需要高度手指协调和精度的插头-插座插入任务上取得了 64% 的成功率。

一个机械臂学习在模拟中（左）和现实世界设置中（右）成功插入黄色连接器的示例。

一个机械臂学习在模拟中拧紧螺丝上的螺栓的示例。

我们使用我们的开源物理模拟器 **MuJoCo** 开发了 DemoStart。在掌握了模拟中的一系列任务并使用标准技术（如领域随机化）来缩小模拟到现实的差距后，我们的方法能够以近乎零样本的方式迁移到物理世界。

在模拟中进行机器人学习可以减少运行实际物理实验所需的成本和时间。但设计这些模拟很困难，而且它们并不总能成功地转化回现实世界的性能。通过将强化学习与少量演示学习相结合，DemoStart 的渐进式学习自动生成一个弥合模拟到现实差距的课程，使得将知识从模拟迁移到物理机器人变得更加容易，并减少了运行物理实验所需的成本和时间。

为了通过密集实验实现更先进的机器人学习，我们在一个名为 **DEX-EE** 的三指机器人手上测试了这种新方法，该机器人手是与 **Shadow Robot** 合作开发的。

![由 Shadow Robot 与 Google DeepMind 机器人团队合作开发的 DEX-EE 灵巧机器人手的图片（图片来源：Shadow Robot）。](/images/posts/5d63b90627a8.jpg)

由 Shadow Robot 与 Google DeepMind 机器人团队合作开发的 DEX-EE 灵巧机器人手的图片（图片来源：Shadow Robot）。

## 机器人灵巧性的未来

机器人学是人工智能研究中一个独特的领域，它展示了我们的方法在现实世界中的效果。例如，一个大语言模型可以告诉你如何拧紧螺栓或系鞋带，但即使它被嵌入到机器人中，它自己也无法执行这些任务。

有一天，人工智能机器人将帮助人们在家里、工作场所等地方完成各种任务。灵巧性研究，包括我们今天描述的高效通用学习方法，将有助于实现那个未来。

在机器人能够像人一样轻松精确地抓取和处理物体之前，我们还有很长的路要走，但我们正在取得重大进展，每一项突破性的创新都是朝着正确方向迈出的又一步。

致谢

DemoStart 的作者：Maria Bauza, Jose Enrique Chen, Valentin Dalibard, Nimrod Gileadi, Roland Hafner, Antoine Laurens, Murilo F. Martins, Joss Moore, Rugile Pevceviciute, Dushyant Rao, Martina Zambelli, Martin Riedmiller, Jon Scholz, Konstantinos Bousmalis, Francesco Nori, Nicolas Heess.

Aloha Unleashed 的作者：Tony Z. Zhao, Jonathan Tompson, Danny Driess, Pete Florence, Kamyar Ghasemipour, Chelsea Finn, Ayzaan Wahid.

### 塑造先进机器人技术的未来

![](/images/posts/abcbf8e5b8e9.jpg)

### 跨多种不同类型机器人扩展学习

![](/images/posts/05b5ef6be392.jpg)

### RT-2：将视觉和语言转化为行动的新模型

![](/images/posts/9fb35913e737.jpg)

### RoboCat：一个自我改进的机器人智能体

![](/images/posts/bc9a15585a66.jpg)

---

> 本文由AI自动翻译，原文链接：[Our latest advances in robot dexterity](https://deepmind.google/blog/advances-in-robot-dexterity/)
> 
> 翻译时间：2026-02-13 04:21
