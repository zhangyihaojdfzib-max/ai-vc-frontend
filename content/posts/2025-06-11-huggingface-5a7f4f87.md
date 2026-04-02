---
title: 为LeRobot机械臂微调Isaac GR00T N1.5模型教程
title_original: Post-Training Isaac GR00T N1.5 for LeRobot SO-101 Arm
date: '2025-06-11'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/gr00t-n1-5-so101-tuning
author: ''
summary: 本文介绍了如何利用NVIDIA开源的Isaac GR00T N1.5机器人基础模型，通过后训练（微调）将其适配到LeRobot SO-101机械臂上。文章提供了从环境安装、数据集准备到模型适配的完整分步教程，重点演示了如何使用桌面清理任务的遥操作数据对模型进行定制，展示了GR00T平台通过“具身标签系统”灵活适配不同机器人硬件的能力。
categories:
- AI研究
tags:
- 机器人学习
- 基础模型
- 模型微调
- NVIDIA Isaac
- 具身智能
draft: false
translated_at: '2026-04-02T05:00:49.046966'
---

# 为LeRobot SO-101机械臂进行Isaac GR00T N1.5的后训练

## 简介

![image/png](/images/posts/8f658a68e6b7.png)

NVIDIA Isaac GR00T（通用机器人00技术）是一个用于构建机器人基础模型和数据管道的研发平台，旨在加速智能、适应性强的机器人的创建。

今天，我们宣布推出Isaac GR00T N1.5，这是世界上首个面向通用人形机器人推理与技能的开源基础模型Isaac GR00T N1的首次重大更新。这个跨具身模型处理包括语言和图像在内的多模态输入，以在不同环境中执行操作任务。它可以通过针对特定具身、任务和环境的后训练进行适配。

在本博客中，我们将演示如何使用来自单个SO-101机械臂的遥操作数据对GR00T N1.5进行后训练（微调）。

![image/gif](/images/posts/575955d7724a.gif)

GR00T N1.5技术博客：https://research.nvidia.com/labs/gear/gr00t-n1_5/

## 分步教程

现在，使用各种机器人形态的开发者都可以访问GR00T N1.5，并可以利用经济实惠的开源LeRobot SO-101机械臂轻松进行微调和适配。

这种灵活性得益于**具身标签系统**，它允许为不同的机器人平台无缝定制模型，使爱好者、研究人员和工程师能够将先进的人形推理和操作能力适配到他们自己的硬件上。

### 步骤 0：安装

在继续安装之前，请检查您是否满足**先决条件**。

#### 0.1 克隆Isaac-GR00T仓库

```bash
git clone https://github.com/NVIDIA/Isaac-GR00T
cd Isaac-GR00T

```

#### 0.2 创建环境

```bash
conda create -n gr00t python=3.10
conda activate gr00t
pip install --upgrade setuptools
pip install -e .[base]
pip install --no-build-isolation flash-attn==2.7.1.post4 

```

### 步骤 1：数据集准备

用户可以使用任何LeRobot数据集来微调GROOT N1.5。在本教程中，我们将以**桌面清理任务**作为微调示例。

需要注意的是，SO-100或SO-101的数据集不在GR00T N1.5的初始预训练范围内。因此，我们将把它作为一个**新具身**进行训练。

![image/png](/images/posts/78fd6b875ceb.png)

#### 1.1 创建或下载您的数据集

对于本教程，您可以通过遵循这些**说明**（推荐）开始创建自己的自定义数据集，或者从Hugging Face下载**so101-table-cleanup**数据集。`--local-dir`参数指定了数据集在您机器上的保存位置。

```bash
huggingface-cli download \
    --repo-type dataset youliangtan/so101-table-cleanup \
    --local-dir ./demo_data/so101-table-cleanup

```

#### 1.2 配置模态文件

`modality.json`文件提供了关于状态和动作模态的额外信息，以使其“兼容GR00T”。使用以下命令将`getting_started/examples/so100_dualcam__modality.json`复制到数据集`<DATASET_PATH>/meta/modality.json`：

```bash
cp getting_started/examples/so100_dualcam__modality.json ./demo_data/so101-table-cleanup/meta/modality.json

```

注意：对于像`so100_strawberry_grape`这样的单摄像头设置，请运行：

```bash
cp getting_started/examples/so100__modality.json ./demo_data/<DATASET_PATH>/meta/modality.json

```

完成这些步骤后，可以使用GR00T的`LeRobotSingleDataset`类加载数据集。这里展示了一个加载数据集的示例脚本：

```bash
python scripts/load_dataset.py --dataset-path ./demo_data/so101-table-cleanup --plot-state-action --video-backend torchvision_av

```

## 步骤 2：微调模型

可以使用Python脚本`scripts/gr00t_finetune.py`执行GR00T N1.5的微调。要开始微调，请在终端中执行以下命令：

```bash
python scripts/gr00t_finetune.py \
   --dataset-path ./demo_data/so101-table-cleanup/ \
   --num-gpus 1 \
   --output-dir ./so101-checkpoints  \
   --max-steps 10000 \
   --data-config so100_dualcam \
   --video-backend torchvision_av

```

提示：默认的微调设置需要约25G的显存。如果您没有那么多显存，可以尝试在`gr00t_finetune.py`脚本中添加`--no-tune_diffusion_model`标志。

## 步骤 3：开环评估

训练完成并生成微调后的策略后，您可以通过运行以下命令在开环设置中可视化其性能：

```bash
python scripts/eval_policy.py --plot \
   --embodiment_tag new_embodiment \
   --model_path ./so101-checkpoints \
   --data_config so100_dualcam \
   --dataset_path ./demo_data/so101-table-cleanup/ \
   --video_backend torchvision_av \
   --modality_keys single_arm gripper

```

恭喜！您已成功在新具身上微调了GR00T-N1.5。

## 步骤 4：部署

成功微调和评估您的策略后，最后一步是将其部署到您的物理机器人上以进行实际执行。

要连接您的**SO-101**机器人并开始评估，请在终端中执行以下命令：

1.  首先将策略作为服务器运行：

```bash
python scripts/inference_service.py --server \
    --model_path ./so101-checkpoints \
    --embodiment-tag new_embodiment \
    --data-config so100_dualcam \
    --denoising-steps 4

```

2.  在另一个终端上，将评估脚本作为客户端运行。请确保更新机器人的端口和ID，以及摄像头的索引和参数，以匹配您的配置。

```bash
python getting_started/examples/eval_lerobot.py \
    --robot.type=so100_follower \
    --robot.port=/dev/ttyACM0 \
    --robot.id=my_awesome_follower_arm \
    --robot.cameras="{ wrist: {type: opencv, index_or_path: 9, width: 640, height: 480, fps: 30}, front: {type: opencv, index_or_path: 15, width: 640, height: 480, fps: 30}}" \
    --policy_host=10.112.209.136 \
    --lang_instruction="Grab pens and place into pen holder."

```

由于我们使用不同的语言指令微调了GRO0T-N1.5，用户可以通过使用**数据集中**的任务提示词之一来引导策略，例如：

"Grab tapes and place into pen holder".

![image/gif](/images/posts/927202479c62.gif)

有关详细的分步教程，请查看：https://github.com/NVIDIA/Isaac-GR00T/tree/main/getting_started

## 🎉 祝您探索愉快！💻🛠️

## 立即开始

准备好用NVIDIA的GR00T N1.5提升您的机器人项目了吗？通过这些重要资源深入了解：

*   **GR00T N1.5模型**：直接从**Hugging Face**下载最新模型。
*   **微调资源**：在我们的**GitHub**上找到用于微调的示例数据集和PyTorch脚本。
*   **贡献数据集**：通过向Hugging Face贡献您自己的数据集，赋能机器人社区。
*   **LeRobot黑客松**：加入全球社区，参与即将到来的LeRobot黑客松，应用您的技能。

通过关注Hugging Face上的**NVIDIA**，随时了解最新动态。

---

> 本文由AI自动翻译，原文链接：[Post-Training Isaac GR00T N1.5 for LeRobot SO-101 Arm](https://huggingface.co/blog/nvidia/gr00t-n1-5-so101-tuning)
> 
> 翻译时间：2026-04-02 05:00
