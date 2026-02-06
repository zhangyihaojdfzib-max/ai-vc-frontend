---
title: LeRobotDataset v3.0发布：支持流式访问的大规模机器人数据集格式
title_original: '`LeRobotDataset:v3.0`: Bringing large-scale datasets to `lerobot`'
date: '2025-09-16'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/lerobot-datasets-v3
author: ''
summary: Hugging Face机器人团队发布LeRobotDataset v3.0，解决了大规模机器人数据集的文件系统限制问题。新格式将多个回合数据打包到单个文件中，利用关系型元数据实现高效检索，并原生支持流式访问模式，允许动态处理超大数据集而无需全部下载。该格式与PyTorch生态系统无缝集成，支持多模态机器人数据，包括机械臂、人形机器人和自动驾驶数据，是推动机器人学习研究可访问性的重要里程碑。
categories:
- AI基础设施
tags:
- 机器人学习
- 数据集
- Hugging Face
- 开源工具
- 机器学习基础设施
draft: false
translated_at: '2026-02-06T04:16:37.254608'
---

# LeRobotDataset:v3.0：将大规模数据集引入 lerobot

TL;DR 今天我们发布 LeRobotDataset:v3！在我们之前的 LeRobotDataset:v2 版本中，每个文件存储一个回合（episode），当数据集扩展到数百万个回合时，会遇到文件系统限制。LeRobotDataset:v3 将多个回合打包到单个文件中，利用关系型元数据从多回合文件中检索单个回合级别的信息。新格式还原生支持以流式模式访问数据集，允许动态处理大型数据集。我们提供了一个单行命令工具，可将所有 LeRobotDataset 格式的数据集转换为新格式，并非常高兴能在下一个稳定版本发布之前与社区分享这一里程碑！

- 安装 lerobot 并记录数据集
- （新）格式设计
- 致谢
- 将您的数据集转换为 v3.0
- 代码示例：将 LeRobotDataset 与 torch.utils.data.DataLoader 结合使用
- 总结

## LeRobotDataset, v3.0

LeRobotDataset 是一种标准化的数据集格式，旨在满足机器人学习的特定需求，它提供了跨模态（包括感觉运动读数、多摄像头数据流和遥操作状态）的统一且便捷的机器人数据访问。
我们的数据集格式还存储有关数据收集方式（元数据）的通用信息，包括对所执行任务的文本描述、所用机器人的类型以及测量细节（如图像和机器人状态流采样的帧率）。
元数据对于在 Hugging Face Hub 上索引和搜索机器人数据集非常有用！

在 Hugging Face 正在开发的机器人库 lerobot 中，LeRobotDataset 为处理多模态时间序列数据提供了统一的接口，并与 Hugging Face 和 Pytorch 生态系统无缝集成。
该数据集格式设计为易于扩展和定制，并且已经支持来自各种机器人平台的开源可用数据集——包括 SO-100 机械臂和 ALOHA-2 设置等操作器平台、真实世界人形机器人数据、仿真数据集，甚至自动驾驶汽车数据！
您可以使用数据集可视化工具探索社区当前贡献的数据集！🔗

除了规模，LeRobotDataset 的这个新版本还支持流式功能，允许动态处理大型数据集的数据批次，而无需将过大的数据集合下载到磁盘。
您可以通过专用的 StreamingLeRobotDataset 接口，以流式模式访问和使用任何 v3.0 版本的数据集！
流式数据集是实现更易访问的机器人学习的关键里程碑，我们很高兴能与社区分享 🤗

![从基于回合的数据集到基于文件的数据集](/images/posts/2519099e9592.png)

![我们直接从 Hugging Face Hub 启用数据集流式传输，以便进行动态处理。](/images/posts/d159f13fbde0.png)

## 安装 lerobot 并记录数据集

lerobot 是 Hugging Face 开发的端到端机器人库，支持真实世界机器人技术以及最先进的机器人学习算法。
该库允许直接在真实世界机器人上本地记录数据集，并将数据集存储在 Hugging Face Hub 上。
您可以在此处阅读更多关于我们当前支持的机器人的信息！

LeRobotDataset:v3 将从 lerobot-v0.4.0 开始成为 lerobot 库的一部分，我们非常高兴能提前与社区分享。您可以使用以下命令直接从 PyPI 安装支持此新数据集格式的最新 lerobot-v0.3.x：

```bash
pip install "https://github.com/huggingface/lerobot/archive/33cad37054c2b594ceba57463e8f11ee374fa93c.zip"  

```

在此处关注社区向库的稳定版本迈进的进展 🤗

一旦安装了支持新数据集格式的 lerobot 版本，您就可以通过遥操作，按照以下说明使用我们的标志性机器人手臂 SO-101 记录数据集：

```bash
lerobot-record \
    --robot.type=so101_follower \
    --robot.port=/dev/tty.usbmodem585A0076841 \
    --robot.id=my_awesome_follower_arm \
    --robot.cameras="{ front: {type: opencv, index_or_path: 0, width: 1920, height: 1080, fps: 30}}" \
    --teleop.type=so101_leader \
    --teleop.port=/dev/tty.usbmodem58760431551 \
    --teleop.id=my_awesome_leader_arm \
    --display_data=true \
    --dataset.repo_id=${HF_USER}/record-test \
    --dataset.num_episodes=5 \
    --dataset.single_task="Grab the black cube"

```

请前往官方文档查看如何为您的用例记录数据集。

# （新）格式设计

LeRobotDataset 背后的一个核心设计选择是将底层数据存储与面向用户的 API 分离。
这允许高效的序列化和存储，同时以直观、即用的格式呈现数据。数据集被组织成三个主要部分：

1.  表格数据：低维、高频数据（如关节状态和动作）存储在高效的 Apache Parquet 文件中，通常卸载到更成熟的 datasets 库，提供快速的、内存映射访问或基于流的访问。
2.  视觉数据：为了处理大量的摄像头数据，帧被连接并编码成 MP4 文件。来自同一回合的帧始终被分组到同一个视频中，而多个视频则按摄像头分组。为了减轻文件系统的压力，同一摄像头视图的视频组也会被分解到多个子目录中。
3.  元数据：一组 JSON 文件，从元数据角度描述数据集的结构，作为数据表格维度和视觉维度的关系对应部分。元数据包括不同的特征模式、帧率、归一化统计数据和回合边界。

![](/images/posts/67a7c738322c.png)

为了支持可能包含数百万个回合（导致数亿/数十亿个独立帧）的数据集，我们将来自不同回合的数据合并到相同的高级结构中。
具体来说，这意味着任何给定的表格集合和视频将不只包含一个回合的信息，而是多个回合可用信息的串联。
这使得文件系统（无论是本地还是像 Hugging Face 这样的远程存储提供商）的压力保持在可控范围内。
然后，我们可以利用元数据来收集特定回合的信息，例如某个回合在特定视频中开始或结束的时间戳。

数据集被组织为包含以下内容的代码仓库：

- meta/info.json：这是核心元数据文件。它包含完整的数据集架构，定义了所有特征（例如observation.state、action）及其形状和数据类型。同时存储关键信息，如数据集的帧率（fps）、代码库版本以及用于定位数据和视频文件的路径模板。
- meta/stats.json：该文件存储整个数据集中每个特征的聚合统计信息（均值、标准差、最小值、最大值）。这些数据用于数据归一化，可通过dataset.meta.stats访问。
- meta/tasks.jsonl：包含从自然语言任务描述到整数任务索引的映射关系，用于任务条件策略训练。
- meta/episodes/：此目录包含每个独立片段（episode）的元数据，如其长度、对应任务以及数据存储位置的指针。为提升可扩展性，这些信息以分块Parquet文件形式存储，而非单个大型JSON文件。
- data/：以Parquet文件形式存储核心的逐帧表格数据。为提高性能并处理大型数据集，多个片段的数据被合并到更大的文件中。这些文件组织到分块子目录中，以保持文件大小可控。因此，单个文件通常包含多个片段的数据。
- videos/：包含所有视觉观察流的MP4视频文件。与data/目录类似，多个片段的视频片段被合并到单个MP4文件中。此策略显著减少了数据集中的文件数量，这对现代文件系统更为高效。路径结构（/videos/<camera_key>/<chunk>/file_...mp4）使数据加载器能够定位正确的视频文件，并跳转到给定帧的精确时间戳。

## 将您的v2.1数据集迁移至v3.0

LeRobotDataset:v3.0将随lerobot-v0.4.0一同发布，届时将能够轻松地将当前托管在Hugging Face Hub上的任何数据集转换为新的v3.0格式，使用以下命令：

```bash
python -m lerobot.datasets.v30.convert_dataset_v21_to_v30--repo-id=<HFUSER/DATASET_ID>

```

我们非常兴奋能尽早与社区分享这一新格式！在我们开发lerobot-v0.4.0期间，您仍然可以通过使用最新的lerobot-v0.3.x将您的数据集转换为新更新的版本，该版本直接从PyPI支持此新数据集格式：

```bash
pip install "https://github.com/huggingface/lerobot/archive/33cad37054c2b594ceba57463e8f11ee374fa93c.zip"  
python -m lerobot.datasets.v30.convert_dataset_v21_to_v30 --repo-id=<HFUSER/DATASET_ID>

```

请注意，这是一个预发布版本，通常不稳定。您可以在此处关注我们下一个稳定版本的开发状态！

转换脚本convert_dataset_v21_to_v30.py将多个片段episode-0000.mp4、episode-0001.mp4、episode-0002.mp4、.../episode-0000.parquet、episode-0001.parquet、episode-0002.parquet、episode-0003.parquet、...聚合到单个文件file-0000.mp4/file-0000.parquet中，并相应更新元数据，以便能够从更高级别的文件中检索特定片段的信息。

### 代码示例：将LeRobotDataset与torch.utils.data.DataLoader结合使用

Hugging Face Hub上包含上述三大支柱（表格和视觉数据，以及关系元数据）的任何数据集，都可以通过一行代码访问。

大多数基于强化学习（RL）或行为克隆（BC）的机器人学习算法，倾向于在观察和动作的堆栈上操作。
例如，RL算法通常使用先前观察的历史o_{t-H_o:t}，而
BC算法则通常被训练来回归多个动作的块。
为了适应机器人学习训练的特殊性，LeRobotDataset提供了一个原生的窗口操作，通过使用delta_timestamps参数，我们可以使用任何给定观察前后若干秒的数据。

方便的是，通过将LeRobotDataset与PyTorch的DataLoader结合使用，可以自动将数据集中的单个样本字典整理成批处理张量的单个字典。

```python
from lerobot.datasets.lerobot_dataset import LeRobotDataset

repo_id = "yaak-ai/L2D-v3"


dataset = LeRobotDataset(repo_id)


sample = dataset[100]
print(sample)








delta_timestamps = {
    "observation.images.front_left": [-0.2, -0.1, 0.0]  
}
dataset = LeRobotDataset(
    repo_id
    delta_timestamps=delta_timestamps
)


sample = dataset[100]



print(sample['observation.images.front_left'].shape)

batch_size=16

data_loader = torch.utils.data.DataLoader(
    dataset,
    batch_size=batch_size
)


num_epochs = 1
device = "cuda" if torch.cuda.is_available() else "cpu"

for epoch in range(num_epochs):
    for batch in data_loader:
        
        

        
        

        
        observations = batch['observation.state.vehicle'].to(device)
        actions = batch['action.continuous'].to(device)
        images = batch['observation.images.front_left'].to(device)

        
        ...

```

## 流式传输

您还可以使用StreamingLeRobotDataset类，以流式模式使用任何v3.0格式的数据集，而无需在本地下载。

```python
from lerobot.datasets.streaming_dataset import StreamingLeRobotDataset

repo_id = "yaak-ai/L2D-v3"
dataset = StreamingLeRobotDataset(repo_id)

```

## 结论

LeRobotDataset v3.0是扩大LeRobot支持的机器人数据集规模的一个里程碑。通过提供一种存储和访问大规模机器人数据集合的格式，我们正在朝着民主化机器人技术的方向迈进，允许社区在可能数百万个片段上进行训练，甚至无需下载数据本身！

您可以通过安装最新的lerobot-v0.3.x来尝试新的数据集格式，并在GitHub或我们的Discord服务器上分享任何反馈！🤗

## 致谢

我们感谢出色的yaak.ai团队在开发LeRobotDataset:v3期间提供的宝贵支持和反馈。
请前往Hugging Face Hub关注他们的组织！
我们始终期待与社区合作并分享早期功能。如果您有兴趣合作，请联系我们 😊

---

> 本文由AI自动翻译，原文链接：[`LeRobotDataset:v3.0`: Bringing large-scale datasets to `lerobot`](https://huggingface.co/blog/lerobot-datasets-v3)
> 
> 翻译时间：2026-02-06 04:16
