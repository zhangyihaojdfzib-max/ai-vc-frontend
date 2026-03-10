---
title: LeRobot v0.5.0发布：全方位扩展机器人硬件、策略与基础设施
title_original: 'LeRobot v0.5.0: Scaling Every Dimension'
date: '2026-03-09'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/lerobot-release-v050
author: ''
summary: LeRobot v0.5.0是其迄今为止最大的版本更新，实现了全方位的扩展。该版本首次支持Unitree G1人形机器人，新增了包括自回归VLA模型Pi0-FAST在内的多种策略，并引入了流式视频编码以加速数据录制。同时，推出了EnvHub以便从Hugging
  Face Hub直接加载仿真环境，集成了NVIDIA IsaacLab-Arena，并对代码库进行了现代化改造，支持Python 3.12和Transformers
  v5，旨在为仿真训练和真实硬件部署提供更强大的支持。
categories:
- AI基础设施
tags:
- 机器人学习
- 具身智能
- 开源框架
- 人形机器人
- 强化学习
draft: false
translated_at: '2026-03-10T04:42:11.410233'
---

# LeRobot v0.5.0：全方位扩展

自 v0.4.0 版本以来，我们合并了超过 200 个 PR，迎来了超过 50 位新贡献者，LeRobot v0.5.0 是我们迄今为止最大的版本发布——同时在各个维度进行扩展。支持更多机器人（包括我们的首个人形机器人）、更多策略（包括自回归 VLA 的回归）、更快的数据集、可直接从 Hub 加载的仿真环境，以及运行在 Python 3.12 和 Transformers v5 上的现代化代码库。无论您是在仿真中训练策略，还是在真实硬件上部署它们，v0.5.0 都能满足您的需求。

## 内容提要

LeRobot v0.5.0 增加了对 Unitree G1 人形机器人的完整支持（全身控制模型），新增了策略——包括 Pi0-FAST 自回归 VLA 和用于响应式推理的实时分块技术——以及消除了录制片段间等待时间的流式视频编码。此版本还引入了 EnvHub，用于从 Hugging Face Hub 加载仿真环境，集成了 NVIDIA IsaacLab-Arena，并进行了重大的代码库现代化改造，支持 Python 3.12+、Transformers v5 和第三方策略插件。

- LeRobot v0.5.0：全方位扩展内容提要目录硬件：前所未有的丰富机器人阵容Unitree G1 人形机器人OpenArm 与 OpenArm Mini更多机器人CAN 总线电机策略：不断增长的模型库Pi0-FAST：自回归 VLA实时分块 (RTC)Wall-XX-VLASARMPEFT 支持数据集：更快的录制，更快的训练流式视频编码图像训练速度提升 10 倍，编码速度提升 3 倍新的数据集工具EnvHub：从 Hub 加载环境NVIDIA IsaacLab-Arena代码库：现代化的基础社区与生态系统结语

- 内容提要
- 硬件：前所未有的丰富机器人阵容Unitree G1 人形机器人OpenArm 与 OpenArm Mini更多机器人CAN 总线电机
- 策略：不断增长的模型库Pi0-FAST：自回归 VLA实时分块 (RTC)Wall-XX-VLASARMPEFT 支持
- 数据集：更快的录制，更快的训练流式视频编码图像训练速度提升 10 倍，编码速度提升 3 倍新的数据集工具
- EnvHub：从 Hub 加载环境NVIDIA IsaacLab-Arena
- 代码库：现代化的基础
- 社区与生态系统
- 结语

- Unitree G1 人形机器人
- OpenArm 与 OpenArm Mini
- 更多机器人
- CAN 总线电机

- Pi0-FAST：自回归 VLA
- 实时分块 (RTC)
- Wall-X
- X-VLA
- SARM
- PEFT 支持

- 流式视频编码
- 图像训练速度提升 10 倍，编码速度提升 3 倍
- 新的数据集工具

- NVIDIA IsaacLab-Arena

## 硬件：前所未有的丰富机器人阵容

LeRobot v0.5.0 极大地扩展了支持的硬件阵容——从机械臂和移动机器人到完整的人形机器人。

### Unitree G1 人形机器人

此版本中最大的硬件新增内容：**完整的 Unitree G1 人形机器人支持**。这是 LeRobot 首次集成人形机器人，并且功能全面：

- **运动**：行走、导航和在环境中移动。
- **操作**：执行灵巧的物体操作任务。
- **遥操作**：通过直观的遥操作界面远程控制 G1。
- **全身控制 (WBC)**：为复杂的现实世界任务同时协调运动和操作。

G1 的集成标志着 LeRobot 向通用机器人技术迈出了重要一步——从桌面机械臂扩展到全身具身智能。请按照[文档](https://huggingface.co/docs/lerobot/en/hardware/unitree_g1)亲自尝试。

![unitree-boss](/images/posts/0eb2d637f050.jpg)

### OpenArm 与 OpenArm Mini

我们增加了对 **OpenArm** 机器人及其配套 **OpenArm Mini** 遥操作器的支持。OpenArm 是一个功能强大的机器人手臂，具有完整的 LeRobot 集成，而 Mini 则作为其天然的遥操作设备。两者都支持**双手配置**，可实现双臂设置以应对更复杂的操作任务。请在[文档](https://huggingface.co/docs/lerobot/en/hardware/open_arm)中查看。

### 更多机器人

硬件生态系统持续增长：

- **Earth Rover**：我们的首个移动机器人集成，将 LeRobot 带入户外导航和地面机器人领域。
- **OMX Robot**：一款新的机器人手臂，具有可配置的夹爪设置和校准支持。
- **SO-100/SO-101 整合**：我们将 SO-100 和 SO-101 的实现统一到了一个更简洁的代码库中——包括双手设置。减少了代码重复，更易于维护，机器人同样出色。

### CAN 总线电机

通过 CAN（控制器局域网）总线新增的电机控制器支持，为更高性能的执行器打开了大门：

- **RobStride**：用于高扭矩应用的基于 CAN 的电机控制器。
- **Damiao**：另一个 CAN 总线电机控制器，扩展了兼容硬件的范围。

这些新增意味着 LeRobot 现在可以驱动比现有 Dynamixel 和 Feetech 生态系统更广泛的各种专业级执行器。

## 策略：不断增长的模型库

此版本为 LeRobot 带来了六种新的策略和技术，突破了开源机器人学习的可能性边界。

### Pi0-FAST：自回归 VLA

**Pi0-FAST** 通过 **FAST**（频域动作序列标记化）将自回归视觉-语言-动作模型引入 LeRobot。与 Pi0 的流匹配方法不同，Pi0-FAST 使用一个自回归动作专家（基于 Gemma 300M）来生成离散化的动作 Token，从而实现：

- **FAST 标记化**：动作被标记化以进行自回归解码，并配有专用的 FAST 动作标记器。
- **灵活解码**：可配置的温度和最大解码步数，以平衡速度和质量。
- **兼容 RTC**：可与实时分块（见下一节）配合使用，实现响应式推理。

```bash
lerobot-train \
  --policy.type=pi0_fast \
  --dataset.repo_id=lerobot/aloha_sim_insertion_human \
  --policy.device=cuda

```

### 实时分块 (RTC)

**实时分块** 是来自 **Physical Intelligence** 的一种推理时技术，它使流匹配策略的响应速度显著提高。RTC 不是等待整个动作块完成后再重新规划，而是持续地将新预测与正在执行的动作混合，从而产生更平滑、反应更迅速的行为。

RTC 不是一个独立的策略——它是一个可以插入现有流匹配策略（Pi0 系列、SmolVLA 和 Diffusion）的增强功能。通过 `--policy.rtc_config.enabled=true` 进行配置。

这对于延迟至关重要的现实世界部署来说是一个改变游戏规则的技术。请阅读[原始论文](https://arxiv.org/abs/2501.15981)了解技术细节和我们的[文档](https://huggingface.co/docs/lerobot/en/policies/real_time_chunking)。

### Wall-X

**Wall-X** 是一个基于 **Qwen2.5-VL** 并采用流匹配动作预测的新 VLA 策略。它结合了 Qwen2.5-VL 强大的视觉-语言理解能力和用于跨具身机器人控制的流匹配头部。

```bash
pip install lerobot[wall_x]
lerobot-train \
  --policy.type=wall_x \
  --dataset.repo_id=lerobot/aloha_sim_insertion_human

```

### X-VLA

**X-VLA** 将一个基于 **Florence2** 的 VLA 引入 LeRobot。基于微软的 Florence-2 视觉-语言模型构建，X-VLA 为 VLA 策略提供了另一种骨干网络选择，扩展了可用于机器人学习的基础模型的多样性。请查看[训练指南](https://huggingface.co/docs/lerobot/en/policies/xvla)了解设置说明和[基础模型](https://huggingface.co/lerobot/xvla)。

```bash
pip install lerobot[xvla]
lerobot-train \
  --policy.type=xvla \
  --dataset.repo_id=lerobot/bimanual-so100-handover-cube

```

**SARM（阶段感知奖励建模）** 解决了机器人学习中最棘手的问题之一：长视野任务。它不是在整个片段上使用单一的全局线性进度信号，而是通过预测任务阶段和该阶段内的进度，以阶段感知的方式对进度进行建模。这使得为复杂的多步骤操作任务训练策略变得容易得多。请按照[文档](https://huggingface.co/docs/lerobot/en/policies/sarm)开始实验。

![sarm-community](/images/posts/eaaba24da58d.gif)

### PEFT 支持

您现在可以使用 **LoRA**（和其他 PEFT 方法）**微调**大型 VLA，而无需修改核心训练流程。PEFT 配置位于策略级别，使得用一小部分计算量就能将庞大的基础模型适配到您的特定机器人和任务上。阅读[文档](https://huggingface.co/docs/lerobot/en/policies/peft)了解更多。

```bash
lerobot-train \
  --policy.type=pi0 \
  --policy.peft_config.use_peft=true \
  --dataset.repo_id=lerobot/aloha_sim_insertion_human

```

## 数据集：更快的录制，更快的训练

本次发布中，数据集流水线获得了重大的性能提升，使得数据收集和训练速度都显著加快。

### 流式视频编码

此前，录制数据集意味着在每一幕（episode）结束后都需要等待视频编码完成。现在不再需要了。通过流式视频编码，帧在捕获时即被实时编码——这意味着幕与幕之间的等待时间为零。只需完成一幕，即可立即开始下一幕。

流式编码还支持**硬件编码器自动检测**，因此如果您的系统拥有GPU加速的视频编码器，LeRobot将自动使用它：

```python
dataset = LeRobotDataset.create(
    repo_id="my/dataset",
    fps=30,
    video_backend="auto",       
    streaming_encoding=True,    
)

```

### 图像训练速度提升10倍，编码速度提升3倍

在底层，我们修复了关键的数据访问瓶颈并彻底改进了图像处理：

- **图像训练速度提升10倍**：改进了图像变换支持，并修复了那些在无形中拖慢训练速度的数据访问瓶颈。
- **编码速度提升3倍**：在不使用流式编码时，并行编码现已成为所有平台的默认选项，并采用动态压缩级别以适应您的数据集类型（视频 vs 图像）。
- **更好的CPU利用率**：在录制和数据集创建过程中实现更高效的资源使用。

### 新的数据集工具

数据集编辑工具包持续扩展：

- **子任务支持**：在单幕内标注和查询子任务，用于分层任务学习。
- **图像转视频转换**：将现有的基于图像的数据集转换为视频格式以提高存储效率，并支持每个视频文件包含多幕。
- **更多编辑操作**：新增用于检查数据集的`info`操作、任务修改工具，以及对现有操作（分割、合并、特征编辑）的大量修复。
- **暴露更多选项**：可配置的视频编解码器、容差设置和元数据缓冲区大小，用于对数据集创建进行细粒度控制。

## EnvHub：来自 Hub 的环境

**EnvHub** 是 LeRobot 中使用仿真环境的一种新方式：直接从 Hugging Face Hub 加载它们。无需在本地安装环境包并进行注册配置，您现在只需将 LeRobot 指向 Hub 上的一个仓库，它就会处理一切——下载环境代码、在 Gymnasium 中注册，并使其可用于训练和评估。

Hub 环境使用 `HubEnvConfig`，它会下载并执行远程的 `make_env` 函数：

```bash
lerobot-train \
  --env.type=hub \
  --env.hub_path="username/my-custom-env" \
  --policy.type=act

```

这降低了与社区共享自定义仿真环境的门槛。将您的环境打包，推送到 Hub，任何人都可以在其上训练。查看[文档](https://huggingface.co/docs/lerobot)以了解更多。这里有一个入门示例：[LeIsaac x LeRobot EnvHub 教程](https://huggingface.co/docs/lerobot)。

### NVIDIA IsaacLab-Arena

我们集成了 **NVIDIA IsaacLab-Arena**，为 LeRobot 带来了 GPU 加速的仿真。IsaacLab-Arena 提供了一系列在 NVIDIA Isaac Sim 上运行的操控任务，提供大规模并行的环境实例以实现快速强化学习。该集成包括专用的预处理/后处理步骤，并与 LeRobot 的训练流水线完全兼容。查看[文档](https://huggingface.co/docs/lerobot)。

## 代码库：现代化的基础

本次发布对代码库进行了现代化改造：

- **Python 3.12+**：LeRobot 现在要求 Python 3.12 作为最低版本，以启用现代语法和获得更好性能。
- **Transformers v5**：我们已迁移至 Hugging Face Transformers v5，与最新的模型生态系统保持同步。
- **第三方策略插件**：就像 v0.4.0 的硬件插件系统一样，您现在可以将自定义策略注册为可安装包——`pip install lerobot_policy_mypolicy` 并通过 `--policy.type=mypolicy` 使用它。无需更改核心库。按照[文档](https://huggingface.co/docs/lerobot)学习如何操作。
- **远程 Rerun 可视化**：使用 Rerun 远程可视化机器人的遥测数据，支持压缩图像以实现带宽高效的流式传输。
- **安装改进**：增加了 `uv` 安装说明，明确了设置步骤，并改进了依赖管理。顺序安装步骤现已清晰记录。
- **文档版本化**：文档现已版本化，因此您总能找到与已安装版本匹配的文档。
- **PyTorch 版本升级**：更新了 PyTorch 版本范围以支持 NVIDIA Blackwell GPU。

## 社区与生态系统

- **现代化的 Discord**：更新了最活跃的社区中心，拥有更好的频道组织。
- **GitHub README、模板与自动化标签**：全新的 README、新的 Issue 和 PR 模板、贡献指南，以及工单的自动标签——让每个人都能更轻松地做出贡献。
- **ICLR 2026 论文录用**：LeRobot 论文已被 ICLR 2026 录用！
- **LeRobot Visualizer 更新**：可视化工具进行了更新，增加了新的数据集可视化徽章并改进了功能。[查看一下](https://huggingface.co/spaces/lerobotics/lerobot-visualizer)！
- **LeRobot Annotation Studio**：一个 HuggingFace Space，旨在用自然语言子任务轻松标注数据集的每一时刻。[查看一下](https://huggingface.co/spaces/lerobotics/lerobot-annotation-studio)！

![visualizer](/images/posts/a3e499e0fae4.gif)

## 最后的话

除了这些主要特性，v0.5.0 还包含了数百个错误修复、文档改进、CI/CD 增强以及整个代码库的易用性改进。从更好的类型检查到更健壮的测试基础设施，我们正在投资于那些能让 LeRobot 在扩展时保持可靠和可维护性的基础。

我们想向社区中的每一个人——贡献者、用户和协作者——致以**巨大的感谢**，感谢你们帮助 LeRobot 成长为今天的样子。每一个错误报告、PR 和讨论都让这个项目变得更好。

敬请期待更多内容 🤗 从这里[开始](https://huggingface.co/lerobotics)吧！
– LeRobot 团队 ❤️

一个大惊喜即将到来，敬请期待！ 👕

---

> 本文由AI自动翻译，原文链接：[LeRobot v0.5.0: Scaling Every Dimension](https://huggingface.co/blog/lerobot-release-v050)
> 
> 翻译时间：2026-03-10 04:42
