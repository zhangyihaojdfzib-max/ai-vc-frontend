---
title: LeRobot v0.6.0：闭环机器人学习新突破
title_original: 'LeRobot v0.6.0: Imagine, Evaluate, Improve'
date: '2026-07-07'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/lerobot-release-v060
author: ''
summary: LeRobot v0.6.0版本推出多项重大更新，旨在闭环机器人学习流程。新版本引入了能够想象未来策略的世界模型（如VLA-JEPA、FastWAM、LingBot-VA），新增一批VLA模型和奖励模型API（Robometer、TOPReward），提供六个新模拟基准测试，并推出部署CLI、FSDP训练和云端训练支持。数据集方面获得深度感知、自动语言标注、自定义视频编码和2倍加载速度提升。整体安装更精简，代码库更清晰。
categories:
- AI产品
tags:
- LeRobot
- 机器人学习
- 世界模型
- VLA
- 开源工具
draft: false
translated_at: '2026-07-08T05:24:11.554287'
---

# LeRobot v0.6.0：想象、评估、改进

此新版本旨在闭环机器人学习流程：在行动前想象未来的策略、告知您机器人何时成功的奖励模型、将失败转化为训练数据的部署CLI，以及用于全面衡量的六个新模拟基准测试。它还带来了深度感知、基于VLM的数据集标注、自定义视频编码、基于HF Jobs的云端训练，以及更精简的安装。

## TL;DR

LeRobot v0.6.0 引入了学习想象未来的世界模型策略（VLA-JEPA、FastWAM、LingBot-VA），一批新的VLA（GR00T N1.7、MolmoAct2、EO-1、EVO1、Multitask DiT），以及一个新的奖励模型API（Robometer、TOPReward）。它提供了六个新的模拟基准测试，统一在 `lerobot-eval` 下，以及带有DAgger风格人在回路修正的 `lerobot-rollout` CLI、FSDP训练和基于HF Jobs的云端训练。数据集获得了深度支持、自动语言标注流水线、自定义视频编码，以及高达2倍的数据加载速度提升，所有这些都基于更精简的安装。

![LeRobot 0.6.0](/images/posts/08aa7ad88d87.png)

- LeRobot v0.6.0：想象、评估、改进TL;DR目录世界模型：会想象的策略VLA-JEPALingBot-VAFastWAMVLA：不断壮大的模型动物园GR00T N1.7MolmoAct2EO-1Multitask DiTEVO1奖励模型：知晓机器人何时成功RobometerTOPReward数据集：更快加载，更丰富数据你的编解码器，你的规则深度支持，端到端大规模语言标注高达2倍更快的数据加载基准测试：一个CLI评估所有训练与推理lerobot-rollout：部署拥有自己的CLIFSDP：训练比GPU更大的模型基于HF Jobs的云端训练代码库：更精简、更清晰社区与生态系统结语

- TL;DR
- 世界模型：会想象的策略VLA-JEPALingBot-VAFastWAM
- VLA：不断壮大的模型动物园GR00T N1.7MolmoAct2EO-1Multitask DiTEVO1
- 奖励模型：知晓机器人何时成功RobometerTOPReward
- 数据集：更快加载，更丰富数据你的编解码器，你的规则深度支持，端到端大规模语言标注高达2倍更快的数据加载
- 基准测试：一个CLI评估所有
- 训练与推理lerobot-rollout：部署拥有自己的CLIFSDP：训练比GPU更大的模型基于HF Jobs的云端训练
- 代码库：更精简、更清晰
- 社区与生态系统
- 结语

- VLA-JEPA
- LingBot-VA
- FastWAM

- GR00T N1.7
- MolmoAct2
- EO-1
- Multitask DiT
- EVO1

- Robometer
- TOPReward

- 你的编解码器，你的规则
- 深度支持，端到端
- 大规模语言标注
- 高达2倍更快的数据加载

- lerobot-rollout：部署拥有自己的CLI
- FSDP：训练比GPU更大的模型
- 基于HF Jobs的云端训练

## 世界模型：会想象的策略

机器人领域正在提出一个大问题：世界模型真的有助于机器人策略吗？v0.6.0 为 LeRobot 带来了三种策略来帮助回答这个问题。每一种都在训练过程中学习想象未来，并且每一种都采取了不同的路径来使这种想象变得可行。

### VLA-JEPA

VLA-JEPA 教会一个紧凑的VLA（基于 Qwen3-VL-2B）在学习行动的同时在潜在空间中预测未来：在训练期间，一个JEPA世界模型必须根据模型自身的行动预测即将到来的帧。其诀窍在于，世界模型在推理时消失，因此你以零额外推理成本获得了世界模型的监督。Hub上有三个即用型检查点，包括一个用于微调的经过DROID预训练的基座：

```bash
lerobot-train \
  --policy.path=lerobot/VLA-JEPA-Pretrain \
  --dataset.repo_id=${HF_USER}/my_dataset \
  --policy.repo_id=${HF_USER}/my_finetuned_policy

```

查看 VLA-JEPA 文档和论文以了解更多。

### LingBot-VA

LingBot-VA 更进一步：一个自回归视频-动作模型，逐块预测未来的视频和动作，并反馈真实观测以保持其想象力接地。你甚至可以保存机器人想象的内容（`--policy.save_predicted_video=true`）并与实际发生的情况进行比较。推理在单个24–32 GB GPU上运行。查看文档和论文以了解技术细节。

![LingBot-VA 想象 rollout 与真实 rollout 对比](/images/posts/1f0f18829c3e.gif)

### FastWAM

FastWAM 在其论文标题中提出了问题：世界动作模型需要测试时的未来想象吗？它将一个约5B的视频生成专家与一个紧凑的动作专家配对在单个网络中，因此模型实际上学会了梦想自己的rollout。在推理时，它完全跳过梦想，直接对动作块进行去噪。从 `lerobot/fastwam_base` 进行微调，并在文档中阅读更多信息。

## VLA：不断壮大的模型动物园

### GR00T N1.7

我们将 NVIDIA GR00T 集成升级到了 GR00T N1.7，这是 NVIDIA 跨具身基础模型的最新开源版本。N1.7 将之前的VLM替换为 Cosmos-Reason2-2B（基于 Qwen3-VL），为流匹配动作头提供输入，并且我们的集成已与 NVIDIA 原始的 Isaac-GR00T 实现进行了对等测试：相同的输入，相同的输出。Flash-attention 现在是可选的，因此 `pip install 'lerobot[groot]'` 即可正常工作，并且你可以直接加载 NVIDIA 发布的检查点。

GR00T N1.7 在 LeRobot 中取代了 N1.5。如果你需要 N1.5，请锁定 `lerobot==0.5.1`。

### MolmoAct2

MolmoAct2，艾伦人工智能研究所的视觉-语言-动作模型，现已移植到 LeRobot，覆盖了完整的生命周期：微调（全量或LoRA）、评估和真实机器人部署。内置校准修正的即用型检查点意味着你可以在 SO-100/101 上零样本运行它：

```bash
lerobot-rollout \
  --policy.path=lerobot/MolmoAct2-SO100_101-LeRobot \
  --robot.type=so100_follower \
  --robot.port=/dev/ttyACM0 \
  --robot.cameras='{cam0: {type: opencv, index_or_path: 0, width: 640, height: 480, fps: 30}, cam1: {type: opencv, index_or_path: 2, width: 640, height: 480, fps: 30}}' \
  --task="pick up the red cube" --duration=30

```

推理在 bf16 下适配约12 GB，LoRA 微调适配单个24 GB GPU。查看 MolmoAct2 文档以获取完整部署指南。

![LeRobot 中的 MolmoAct2 零样本](/images/posts/d5e6766c8227.gif)

EO-1，一个在交错视觉-文本-动作数据上进行上游预训练的VLA，加入了 LeRobot：一个 Qwen2.5-VL-3B 骨干网络，带有流匹配动作头，由论文作者之一贡献。使用标准的 `lerobot-train` 工作流，通过 `--policy.type=eo1` 进行训练。详情见文档和论文。

### Multitask DiT

Multitask Diffusion Transformer 策略将 TRI Large Behavior Models 配方带到了 LeRobot：一个约450M参数的扩散Transformer，以CLIP视觉和语言嵌入为条件，因此一个模型可以学习通过自然语言选择的多个任务。它支持扩散和流匹配目标，并且足够小，可以自行训练。参见文档。

VLA 不一定非得很大。EVO1 将其策略压缩到0.77B参数，一个 InternVL3-1B 骨干网络，带有流匹配动作头，足够小，可以在中等GPU上进行微调和实时运行。它开箱即用地支持两阶段微调和实时分块支持。参见 EVO1 文档和论文。

## 奖励模型：知晓机器人何时成功

成功检测和进度估计是机器人学习流程中缺失的部分，v0.6.0 为它们提供了一个家园。LeRobot 现在拥有一个统一的奖励模型API（`lerobot.rewards`），镜像了策略API，在一个接口背后提供了四个奖励模型——HIL-SERL奖励分类器、SARM，以及两个新增的：

### Robometer

Robometer 是一个预训练的通用奖励模型：将 `lerobot/Robometer-4B` 指向任何 LeRobot 数据集，它就能从原始视频加上语言指令中评分任务进度和成功，无需特定任务的训练。它基于 Qwen3-VL-4B，并通过在超过一百万条机器人轨迹的数据集上进行轨迹比较训练而成（RSS 2026 论文）。

![LeRobot Robometer](/images/posts/46435b30ca1e.gif)

### TOPReward

TOPReward 完全实现零样本：完全不需要奖励权重。它封装了一个现成的 VLM（Qwen3-VL），并读取给定轨迹视频和任务指令下 Token "True" 的对数概率。任何有能力的 VLM 都能成为奖励函数。

两者都附带标注脚本，可将逐帧进度曲线写入数据集，为奖励感知行为克隆（RA-BC）、数据集质量检查和进度叠加视频做好准备。请查阅 Robometer 和 TOPReward 文档。

## 数据集：加载更快，数据更丰富

### 你的编解码器，你的规则

录制不再局限于单一硬编码编解码器。新的 `--dataset.rgb_encoder.*` 选项暴露了完整的编码参数（编解码器、质量、像素格式、GOP、预设），并且 `vcodec=auto` 会先探测 NVENC、VideoToolbox、VAAPI 和 QSV 等硬件编码器，再回退到默认的软件 AV1 编码器。对于现有数据集，一条命令即可重新编码所有内容：

```bash
lerobot-edit-dataset \
    --repo_id ${HF_USER}/my_dataset \
    --operation.type reencode_videos \
    --operation.rgb_encoder.vcodec h264 \
    --operation.rgb_encoder.crf 23

```

完整详情请参阅视频编码文档。

### 深度支持，端到端

插入 Intel RealSense，设置 `use_depth: true`，LeRobot 即可端到端记录深度图：以毫米为单位捕获，压缩为紧凑的 12 位深度视频流与 RGB 摄像头同步记录，并在训练时解码回物理单位。深度图在录制期间和 `lerobot-dataset-viz` 中实时渲染，并支持 SO-100/101、Koch、OpenArm、reBot、Unitree G1 等多种机器人。

![LeRobot Depth Camera](/images/posts/ed9740f23725.gif)

### 大规模语言标注

你的数据集不再局限于每段轨迹一个任务字符串。LeRobot 数据集现在原生支持丰富的语言标注（带时间戳的子任务、计划、记忆、修正、语音以及每摄像头的 VQA 对），新的 `lerobot-annotate` CLI 使用 VLM 观看你的轨迹并自动填充这些标注：

```bash
lerobot-annotate \
    --repo_id=${HF_USER}/my_dataset \
    --new_repo_id=${HF_USER}/my_dataset_annotated \
    --vlm.model_id=Qwen/Qwen2.5-VL-7B-Instruct \
    --push_to_hub=true

```

随后，一个 YAML 配方层会在采样时将这些标注渲染成聊天风格的训练消息：这正是未来长时域、可对话机器人策略所需的训练数据。可通过 HF Jobs 进行扩展，并阅读标注流程文档了解更多。

### 数据加载速度提升高达 2 倍

视频数据集训练现可立即实现约 2 倍加速：多摄像头帧并行解码，数据加载器工作进程传输紧凑的 uint8 帧（进程间内存减少 4 倍），持久化工作进程在多个 epoch 间保持解码器缓存。加载大型数据集的子集（`episodes=[...]`）从几分钟缩短到几毫秒（在我们的基准测试中从 275 秒降至 0.06 秒）。采样现在也是确定性的且可恢复，因此中断的训练可以精确地从样本级别重新开始。

## 基准测试：一个 CLI 评估所有

v0.5.0 将 LeRobot 确立为 VLA 评估中心；v0.6.0 通过六个新的模拟基准测试使其名副其实，所有基准测试均可通过同一个 `lerobot-eval` CLI 运行，每个基准测试都配有文档页面、Docker 镜像以及在 CI 中经过冒烟测试的 SmolVLA 基线检查点：

- **LIBERO-plus**：通过约 10,000 个 LIBERO 的扰动变体（涵盖光照、摄像头视角、重写指令等七个维度）对 VLA 进行压力测试。它能告诉你策略何时失效。
- **RoboTwin 2.0**：在 SAPIEN 上覆盖 50 个双臂操作任务，具有大量域随机化，并在 Hub 上提供了超过 10 万条可训练轨迹。
- **RoboCasa 365**：在移动操作器上覆盖 2,500 个程序化生成的厨房中的 365 个厨房任务，是我们系列中任务覆盖面最广的。
- **RoboCerebra**：评估长时域行为，轨迹包含 3 到 6 个在语言引导的中间指令下链接的子目标，并附带一个包含 6,660 条轨迹的数据集。
- **RoboMME**：一项记忆测试：你的策略能否计数重复次数、追踪隐藏物体以及模仿演示流程？涵盖 4 个记忆套件中的 16 个任务。
- **VLABench**：测试操作中的知识和推理能力，从物理问题到像端到端冲泡咖啡这样的复合任务。

```bash
lerobot-eval \
  --policy.path=lerobot/smolvla_robotwin \
  --env.type=robotwin \
  --env.task=beat_block_hammer \
  --eval.n_episodes=100 --eval.batch_size=1

```

模拟器后端需要特定的系统依赖及其各自的安装步骤；每个文档页面都有确切的配方，如果你不想自行配置，每个基准测试都提供了现成的 Docker 镜像。

加上 LIBERO、Meta-World 和 NVIDIA IsaacLab-Arena，这使我们在一个框架下拥有了九个基准测试系列，新的添加新基准测试文档详细说明了如何接入你自己的基准测试。评估也更快了：并行评估现在默认使用异步向量化环境，基准测试显示速度提升高达 2 倍。

![LeRobot benchmarks](/images/posts/030bc763671d.gif)

## 训练与推理

### lerobot-rollout：部署拥有自己的 CLI

部署策略过去是在 `lerobot-record` 之上进行 hack。新的 `lerobot-rollout` CLI 将部署作为独立工作流，具有可插拔策略和推理后端（包括针对慢速兼容 VLA 的实时分块）。`base` 策略仅运行策略。`sentry` 持续记录，轮换轨迹并上传到 Hub。`highlight` 维护一个环形缓冲区，在你按下按键时保存最后 N 秒，因此不会错过任何有趣时刻。`episodic` 镜像经典的轨迹/重置录制工作流。而 `dagger` 将部署转变为数据收集。

使用 DAgger 策略，你可以观察策略运行，在出错时按下按键（或 USB 脚踏开关），用主臂接管并记录修正，然后交还控制权。在你接管之前，主动式主臂会被驱动到从臂的位姿，因此切换过程无抖动。每个修正帧都标有 `intervention` 标志，生成的数据集即可用于下一次微调：

```bash
lerobot-rollout \
    --strategy.type=dagger \
    --policy.path=${HF_USER}/my_policy \
    --robot.type=so100_follower \
    --robot.port=/dev/ttyACM0 \
    --teleop.type=so101_leader \
    --teleop.port=/dev/ttyACM1 \
    --dataset.repo_id=${HF_USER}/dagger_corrections \
    --dataset.single_task="Grasp the block"

```

部署、收集修正、微调、重复：机器人学习飞轮现在只是一个 CLI 标志。阅读部署文档。

### FSDP：训练比 GPU 更大的模型

机器人基础模型正在超越单 GPU 的容量。LeRobot 训练现在通过 Accelerate 支持 FSDP（全分片数据并行）：参数、梯度和优化器状态在多个 GPU 间分片，检查点被合并回一个普通的单文件 `model.safetensors`，加载方式与任何其他策略相同。你甚至可以在不同数量的 GPU 上恢复 FSDP 运行。请参阅多 GPU 训练文档。

### 使用 HF Jobs 进行云端训练

没有 GPU？没问题。只需添加一个标志，完全相同的 `lerobot-train` 命令即可在云端运行：

```bash
lerobot-train \
  --dataset.repo_id=${HF_USER}/so101_test \
  --policy.type=act \
  --policy.repo_id=${HF_USER}/my_policy \
  --job.target=a10g-small

```

如有需要，LeRobot 会将你的本地数据集推送到私有 Hub 仓库，提交任务，将日志流式传输到你的终端，并在最后将训练好的策略推送到 Hub。通过 `--job.target` 选择从 T4 到 8x H200 的任何配置（计算按需付费）。查看文档

## 代码库：更精简、更清晰

- `pip install lerobot` 现在真正轻量化了，基础依赖减少了约40%。按功能划分的额外组件（`[training]`、`[core_scripts]`、`[evaluation]`等）覆盖了其余功能，缺失依赖的错误会明确告诉你需要添加哪个额外组件。如果你只使用LeRobot数据集，不再需要安装与硬件相关的依赖；）
- 支持的PyTorch版本更新至2.7–2.11，Linux系统通过`uv`安装时默认锁定CUDA 12.8的wheel包。`--policy.dtype=bfloat16`现在可通过Accelerate驱动真正的混合精度训练。
- 提交的`uv.lock`文件是CI、Docker和开发环境的权威依赖规范，文档中每一步都提供了`uv`安装路径，甚至可以通过单个标志选择CUDA wheel包。
- `--display_mode=foxglove`可将遥操作、记录和回放流式传输到Foxglove——这款可视化工具已被机器人领域广泛使用。它支持远程配置，并且`lerobot-dataset-viz`提供了可拖拽播放的数据集回放功能。
- 可通过pip安装的`lerobot_env_*`包现在会自动注册其环境。该插件系统覆盖所有五种组件类型：机器人、相机、遥操作器、策略和环境。
- 录制期间的键盘控制现在可在Wayland、SSH、无头设备以及无需辅助功能权限的macOS上使用。

请查看[发布说明](https://github.com/huggingface/lerobot/releases)获取完整列表及破坏性变更的迁移指南。

![LeLab——LeRobot的图形用户界面](/images/posts/1fdd4796959d.gif)

## 社区与生态系统

- LeLab将整个LeRobot工作流程（标定、遥操作、记录、本地或HF Jobs训练、部署）集成在浏览器UI中，无需命令行。目前支持SO-ARM101。[立即试用！](https://huggingface.co/lerobot)
- Isaac Teleop允许你通过NVIDIA的Isaac Teleop堆栈，借助VR控制器在CloudXR/OpenXR上遥操作SO-101，这是与NVIDIA团队合作的成果。请参阅[文档](https://docs.lerobot.ai)。
- 全新的[计算硬件指南](https://docs.lerobot.ai/hardware)解答了每位新手都会问的两个问题：我需要什么GPU？训练需要多长时间？它提供了每种策略家族的实测显存占用范围，以及从RTX 4090到4×H100的参考训练时间。
- 重写的[添加策略指南](https://docs.lerobot.ai/add-policy)展示了如何发布自己的策略，既可直接集成到代码库中，也可作为无需提交PR的插件包。

## 总结

除了上述主要功能外，v0.6.0还包含了数百项bug修复、文档改进和代码库质量提升，从更智能的默认设置到更可靠的CI。

我们衷心感谢社区中的每一位成员。本次发布包含了学术界、工业界和爱好者团队的工作，他们选择LeRobot作为其模型和基准测试的平台。每一次PR和bug报告都在推动开源机器人技术向前发展。

敬请期待更多更新 🤗 [从这里开始！](https://github.com/huggingface/lerobot)
– LeRobot团队 ❤️

---

> 本文由AI自动翻译，原文链接：[LeRobot v0.6.0: Imagine, Evaluate, Improve](https://huggingface.co/blog/lerobot-release-v060)
> 
> 翻译时间：2026-07-08 05:24
