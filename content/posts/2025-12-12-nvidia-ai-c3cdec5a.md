---
title: AI调酒师ADAM亮相NHL赛场，NVIDIA技术驱动机器人服务创新
title_original: 'Cheers to AI: ADAM Robot Bartender Makes Drinks at Vegas Golden Knights
  Game'
date: '2025-12-12'
source: NVIDIA AI Blog
source_url: https://blogs.nvidia.com/blog/adam-robot-vegas-golden-knights-thor/
author: Scott Martin
summary: 本文介绍了在拉斯维加斯金骑士队比赛中投入使用的机器人调酒师ADAM。它由Richtech Robotics基于NVIDIA Isaac平台开发，通过Isaac
  Sim进行仿真训练，并搭载Jetson AGX Orin边缘AI平台实现实时感知与精准操作，以应对酒店业劳动力短缺并提升客户体验。文章还提及了该公司基于新一代Jetson
  Thor处理器开发的工业人形机器人Dex，展现了NVIDIA技术在服务与工业机器人领域的广泛应用。
categories:
- AI产品
tags:
- 服务机器人
- NVIDIA Isaac
- 边缘AI
- 机器人仿真
- 工业自动化
draft: false
translated_at: '2026-01-06T00:56:46.895Z'
---

在拉斯维加斯的T-Mobile体育馆，金骑士队的球迷们获得的不仅仅是冰球比赛——他们正在体验未来。ADAM，一个利用NVIDIA Isaac库开发的机器人，正在这个NHL最激动人心的场馆之一倾倒饮品，并吸引着众人的目光。

ADAM，全称是"自动化双臂调酒师"，由总部位于拉斯维加斯的Richtech Robotics开发。它不仅仅是个新奇事物——它是针对酒店服务业现实挑战的解决方案：劳动力短缺和对独特客户体验的需求。

"酒店业面临着巨大的劳动力挑战，而ADAM正是我们在满足这些需求的同时提升客户体验的答案，"Richtech Robotics总裁Matt Casella表示。"借助NVIDIA的Isaac平台，我们开发出了一个可扩展、稳定且坦率地说能为球迷创造难忘时刻的解决方案。在T-Mobile体育馆的反响非常惊人——人们喜欢与ADAM互动。"

**在模拟中学习调酒**
在ADAM真正倒出第一杯饮料之前，它在一个虚拟酒吧里接受了训练。Richtech使用了NVIDIA Isaac Sim——一个基于NVIDIA Omniverse构建的开源机器人仿真参考框架——来构建一个高保真、物理精确的ADAM工作站模拟环境，其中包含杯子、器具和不同的光照条件。团队生成了合成数据，以教会ADAM即使在眩光或反光等棘手条件下也能识别物体。

ADAM的倾倒和摇晃等技能，通过使用NVIDIA的开源机器人学习框架Isaac Lab在模拟中得到了完善。结果是：一个不仅能遵循指令，还能精确适应环境的机器人。

**利用Jetson在边缘运行实时AI**
ADAM运行在NVIDIA Jetson AGX Orin上，这是一个强大的边缘AI平台，计算能力高达275 TOPS。通过使用Isaac ROS 2库，ADAM能够实时捕捉摄像头画面、检测物体并校准工作空间。ADAM的感知栈——使用TAO Toolkit构建并通过TensorRT优化——使其能够以低于40毫秒的延迟识别杯子、测量液位并调整动作。

这意味着ADAM能够发现放错位置的杯子，检测泡沫何时到达杯沿，并纠正倾倒动作——所有这些都流畅无阻。

**利用NVIDIA Thor创造工业灵巧性**
当ADAM在金骑士队的比赛中忙于服务饮品时，Richtech Robotics也在工业自动化领域取得了重大进展，推出了Dex——一款专为工厂和仓库环境打造的新型移动人形机器人。

最近在GTC DC上亮相的Dex，结合了自主轮式平台的移动性和双臂灵巧操作的精确性。它旨在处理轻到中度的工业任务，如机器操作、零件分拣、物料搬运和包装——并且具备灵活性，可以适应不同的工具和工作流程。

Dex运行在NVIDIA Jetson Thor上，这是一款下一代机器人处理器，使其能够在动态工业环境中进行实时传感器处理和AI推理。

Dex的训练数据融合了来自真实世界和由Isaac Sim生成的合成数据。这使得Dex的模型能够泛化到多种场景中。

了解更多关于Jetson Thor的信息以及Jetson平台节日促销价格。


> 本文由AI自动翻译，原文链接：[Cheers to AI: ADAM Robot Bartender Makes Drinks at Vegas Golden Knights Game](https://blogs.nvidia.com/blog/adam-robot-vegas-golden-knights-thor/)
> 
> 翻译时间：2026-01-06 00:56
