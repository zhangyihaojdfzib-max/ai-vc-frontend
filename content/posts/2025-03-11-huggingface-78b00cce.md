---
title: 全球最大开源自动驾驶数据集L2D发布
title_original: 'LeRobot goes to driving school: World’s largest open-source self-driving
  dataset'
date: '2025-03-11'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/lerobot-goes-to-driving-school
author: ''
summary: 文章介绍了由Yaak与Hugging Face LeRobot团队合作推出的全球最大开源自动驾驶数据集L2D（学习驾驶）。该数据集包含来自德国30个城市、超过90TB的多模态驾驶数据（5000+小时），涵盖6个高清摄像头、车辆状态、环境条件及自然语言指令。数据集特别区分了专家（驾校教练）和学生（学员驾驶员）策略，旨在为端到端自动驾驶模型训练提供高质量、多样化的开源资源，推动机器人AI在汽车领域的应用。
categories:
- AI基础设施
tags:
- 自动驾驶
- 开源数据集
- 端到端模型
- 多模态数据
- LeRobot
draft: false
translated_at: '2026-05-10T05:37:10.882359'
---

# LeRobot 驾校启程

L2D 的 TL;DR——全球最大的自动驾驶数据集！

- 来自德国30个城市的90+TB多模态数据（5000+小时驾驶数据）
- 6个环绕高清摄像头及完整车辆状态：速度/航向/GPS/IMU
- 连续动作：油门/刹车/转向，离散动作：档位/转向灯
- 环境状态：车道数量、道路类型（高速公路|住宅区）、路面状况（沥青、鹅卵石、石块）、最高限速
- 环境条件：降水量、天气状况（雪、晴、雨）、光照条件（黎明、白天、黄昏）
- 专为训练基于自然语言指令或未来路径点的端到端模型而设计
- 自然语言指令。例如：每个片段对应"绿灯亮时，驶过电车轨道，然后通过环岛"
- 未来路径点映射到OpenStreetMap图，额外以鸟瞰视角渲染
- 专家（驾校教练）和学生（学员驾驶员）策略

最先进的视觉语言模型和大语言模型是在从互联网获取的开源图像-文本语料库上训练的，这推动了近期开源AI的加速发展。尽管取得了这些突破，端到端AI在机器人和汽车领域的应用仍然较低，主要原因是缺乏像OXE这样高质量、大规模的多模态数据集。

为了释放机器人AI的潜力，Yaak与🤗的LeRobot团队合作，并激动地向机器人AI社区宣布推出"学习驾驶"（L2D）。L2D是全球最大的多模态数据集，旨在为汽车领域构建开源空间智能，并优先支持🤗的LeRobot训练流程和模型。借鉴源代码版本控制的最佳实践，Yaak还邀请AI社区搜索和发现我们整个数据集（>1 PB）中的新颖片段，并将收集的片段排队等待审核，以便合并到未来版本（R5+）中。

表1：开源自动驾驶数据集（*不包括激光雷达和雷达）。来源

L2D是通过安装在德国30个城市驾校运营的60辆电动车上的相同传感器套件，在3年时间内收集的。L2D中的策略分为两组——由驾校教练执行的专家策略和由学员驾驶员执行的学生策略。两组策略都包含驾驶任务的自然语言指令。例如，"当你拥有先行权时，从环岛第三个出口驶出，小心驶过人行横道"。

图1：可视化：Nutron（为清晰起见，仅显示6个摄像头中的3个）
  指令："当你拥有先行权时，驶过环岛并从第三个出口驶出"。

专家策略没有驾驶错误，被认为是最优的，而学生策略则存在已知的次优性（图2）。

图2：学生策略出现转向抖动，以防止驶入对面来车的车道

两组策略都涵盖了在欧盟（德国版本）内获得驾驶执照所必需完成的所有驾驶场景，例如超车、环岛和铁路道口。在发布版本（见下方R3+）中，对于次优的学生策略，将包含次优性的自然语言推理说明。例如，"在接近对向来车时方向盘操作不正确/抖动"（图2）

# L2D：学习驾驶

L2D（R2+）旨在成为最大的开源自动驾驶数据集，为AI社区提供独特且多样化的"片段"，用于训练端到端空间智能。通过包含完整的驾驶策略谱系（学生和专家），L2D捕捉了安全操作车辆的复杂性。为了充分代表运营中的自动驾驶车队，我们包含了具有多样化环境条件、传感器故障、施工区域和故障交通信号的片段。

专家和学生策略组均使用下表中详述的相同传感器配置进行采集。六个RGB摄像头以360度捕捉车辆环境，车载GPS捕捉车辆位置和航向。IMU收集车辆动态信息，我们从车辆的CAN接口读取速度、油门/刹车踏板、转向角、转向灯和档位。我们使用各自对应的Unix纪元时间戳将所有模态类型与前左摄像头（observation.images.front_left）同步。我们还对可行数据点进行了插值以提高精度（见表2），并最终将采样率降低至10赫兹。

图3：多模态数据可视化，使用Visualization：Nutron（为清晰起见，仅显示6个摄像头中的3个）

表2：模态类型、LeRobot v3.0键、形状和插值策略

L2D遵循官方德国驾驶任务目录（详细版本）对驾驶任务、驾驶子任务和任务定义的定义。我们为所有片段分配唯一的任务ID和自然语言指令。所有片段的LeRobot：任务设置为"在遵守交通规则和法规的同时跟随路径点"。下表展示了几个示例片段、它们的自然语言指令、驾驶任务和子任务。对于相似场景，专家和学生策略具有相同的任务ID，而指令则随片段变化。

表3：L2D中的示例片段、它们的指令以及源自欧盟驾驶任务目录的任务ID

我们使用车辆位置（GPS）、开源路由引擎、OpenStreetMap和大语言模型（LLM）自动构建指令和路径点（见下文）。自然语言查询的构建方式紧密遵循大多数GPS导航设备中可用的逐向导航。路径点（图4）通过将原始GPS轨迹地图匹配到OSM图，并从车辆当前位置（绿色）向前100米范围内采样10个等距点（橙色）计算得出，作为行驶路径点。

图4：L2D 6个RGB摄像头、路径点（橙色）和车辆位置（绿色）
  指令：直行至停车标志处，然后当你拥有先行权时，汇入左侧行驶的车流

# 搜索与筛选

我们使用由60辆起亚E-niro驾校车辆组成的车队收集了专家和学生策略，这些车辆在德国30个城市运营，配备相同的传感器套件。使用车队收集的多模态日志是非结构化的，不包含任何任务或指令信息。为了搜索和筛选片段，我们通过将GPS轨迹与OSRM进行地图匹配，并从OSM分配节点和路径标签（见下一节）来提取信息，从而丰富原始多模态日志。结合LLM，这一丰富步骤使得能够通过任务的自然语言描述来搜索片段。

## OpenStreetMap

为了高效搜索相关片段，我们通过使用OSRM对轨迹进行地图匹配获取转向信息，从而丰富GPS轨迹。我们还使用地图匹配的路线，并通过OSM为轨迹分配路线特征、路线限制和路线操作（统称为路线任务）（参见示例地图）。附录A1-A2提供了有关我们分配给GPS轨迹的路线任务的更多详细信息。

图5：分配给原始GPS轨迹的驾驶任务（查看地图）

分配给地图匹配路线的路线任务，会被分配开始和结束时间戳（Unix纪元），这相当于车辆进入和退出任务定义的地理空间线串或点的时间（图6）。

**图 6：粉色：GNSS 轨迹，蓝色：匹配路线，任务：让行、火车道口和环岛（查看地图）**

## 多模态搜索

我们按照图 5 中描述的路线任务，对我们的多模态数据执行语义时空索引。
此步骤提供了我们多模态数据的丰富语义概览。为了在语义空间中根据指令搜索代表性片段，
例如，“驶向环岛，在拥有先行权时右转”，
我们构建了一个基于 LLM（大语言模型）的多模态自然语言搜索，用于搜索我们所有的驾驶数据（> 1 PB）并检索匹配的片段。

我们结构化自然语言查询（指令），使其与 GPS 导航设备中可用的逐向导航高度相似。为了将指令转换为路线任务，
我们使用指令提示 LLM（大语言模型），并将其输出引导至路线特征、
路线限制、路线操作的列表，并检索分配给这些路线任务的片段。我们使用
pydantic 模型对 LLM（大语言模型）的输出进行严格验证，以最小化幻觉。
具体来说，我们使用 llama-3.3-70b，
并将其输出引导至由 pydantic 模型定义的架构。为了进一步提高结构化输出的质量，
我们使用了大约 30 对已知的自然语言查询和路线任务进行上下文学习。附录 A.2 提供了我们使用的上下文学习对的详细信息。

![自然语言搜索](/images/posts/3de47bdb00cb.gif)

指令：驶向环岛，在拥有先行权时右转

## LeRobot

🤗 上的 L2D 已转换为 LeRobotDataset v2.1 和 LeRobotDataset v3.0 格式，以充分利用
LeRobot 内当前和未来支持的模型。
AI 社区现在可以构建端到端的自动驾驶模型，利用最先进的模仿学习
和强化学习模型，用于现实世界的机器人技术，例如 ACT、Diffusion Policy 和 Pi0。

现有的自动驾驶数据集（下表）侧重于中间感知和规划任务，如 2D/3D 目标检测、
跟踪、分割和运动规划，这些任务需要高质量的标注，因此难以扩展。
相反，L2D 专注于端到端学习的发展，该学习直接从传感器输入学习预测动作（策略）（表 1）。
这些模型利用互联网预训练的 VLM 和 VLAM。

# 发布

机器人 AI 模型的性能受限于训练集中片段的质量。
为确保最高质量的片段，我们计划对 L2D 进行分阶段发布。每次新发布都会增加关于片段的
附加信息。每个版本 R1+ 都是先前版本的超集，以确保清晰的片段历史。

1. 指令：驾驶任务的自然语言指令
2. task_id：将片段映射到欧盟规定的驾驶任务 Task ID
3. observation.state.route：来自 OSM 的车道数量、转弯车道信息
4. suboptimal：导致次优策略原因的自然语言描述

**表 5：L2D 发布日期**

Yaak 使用驾校车队收集的整个多模态数据集比计划发布的
数据量大 5 倍。为了推动 L2D 超越 R4 的发展，我们邀请 AI 社区
在我们整个数据收集中搜索并发现场景，并构建一个社区驱动的开源 L2D。
AI 社区现在可以通过我们的自然语言搜索搜索片段，
并将他们的收藏排队等待社区审查，以便合并到即将发布的版本中。借助 L2D，我们希望为空间智能解锁一个
ImageNet 时刻。

![自然语言搜索](/images/posts/4ac40d62cd0e.gif)

**图 7：通过自然语言指令搜索片段**

# 使用 L2D 与 HF/LeRobot

对于 R0、R1，我们建议使用 LeRobotDataset，并指定 revision=[R0|R1]，可以直接从 LeRobot 的 pypi 版本中使用。对于 R2+，请按照此处概述的安装步骤操作，或从 main 分支安装，如下所示，因为我们建议使用 StreamingLeRobotDataset，因为 R3 是 Dataset v3.0 格式。

```
# uv 用于 python 依赖
curl -LsSf https://astral.sh/uv/install.sh | sh
# 安装 python 版本并固定
uv init && uv python install 3.12.4 && uv python pin 3.12.4
# 为 R0、R1 添加 lerobot 依赖
uv add lerobot
# 对于 R2+
GIT_LFS_SKIP_SMUDGE=1 uv add "git+https://github.com/huggingface/lerobot.git@main"
uv run python
>>> from lerobot.datasets.streaming_dataset import StreamingLeRobotDataset
# 这将加载 3 个片段=[0, 9999, 99999]，要加载所有片段请移除它
>>> dataset = StreamingLeRobotDataset("yaak-ai/L2D", episodes=[0, 9999, 99999], streaming=True, buffer_size=1000)
>>> dataset.meta
LeRobotDatasetMetadata({
    Repository ID: 'yaak-ai/L2D',
    Total episodes: '100000',
    Total frames: '19042712',
    Features: '['observation.state.vehicle', 'observation.state.lanes', 'observation.state.road', 'observation.state.surface', 'observation.state.max_speed', 'observation.state.precipitation', 'observation.state.conditions', 'observation.state.lighting', 'observation.state.waypoints', 'observation.state.timestamp', 'task.policy', 'task.instructions', 'action.continuous', 'action.discrete', 'timestamp', 'frame_index', 'episode_index', 'index', 'task_index', 'observation.images.left_forward', 'observation.images.front_left', 'observation.images.right_forward', 'observation.images.left_backward', 'observation.images.rear', 'observation.images.right_backward', 'observation.images.map']',
})',

```

# 闭环测试

## LeRobot 驱动程序

为了对使用 L2D 和 LeRobot 训练的 AI 模型进行现实世界测试，
我们邀请 AI 社区从 2025 年夏季开始提交模型，在有安全驾驶员的情况下进行闭环测试。
AI 社区将能够将他们的模型排队，在我们的车队上进行闭环测试，并选择他们希望模型接受评估的任务，
例如，在环岛导航或停车。
该模型将在车辆上以推理模式（Jetson AGX 或类似设备）运行。
这些模型将使用 LeRobot 驱动程序以两种模式驾驶车辆：

1. 按航点驾驶：“在给定 observation.state.vehicle.waypoints 的情况下，遵循航点并遵守驾驶规则和法规”
2. 按语言驾驶：“直行，在斑马线处右转”

# 附加资源

- 驾驶任务目录 (Fahraufgabenkatalog)
- 德国官方实际驾驶考试
- Groq

# 参考文献

```bibtex
@article{yaak2023novel,
    author = {Yaak team},
    title ={A novel test for autonomy},
    journal = {https://www.yaak.ai/blog/a-novel-test-for-autonomy},
    year = {2023},
}
@article{yaak2023actiongpt,
    author = {Yaak team},
    title ={Next action prediction with GPTs},
    journal = {https://www.yaak.ai/blog/next-action-prediction-with-gpts},
    year = {2023},
}
@article{yaak2024si-01,
    author = {Yaak team},
    title ={Building spatial intelligence part - 1},
    journal = {https://www.yaak.ai/blog/buildling-spatial-intelligence-part1},
    year = {2024},
}
@article{yaak2024si-01,
    author = {Yaak team},
    title ={Building spatial intelligence part - 2},
    journal = {https://www.yaak.ai/blog/building-spatial-intelligence-part-2},
    year = {2024},
}

```

## 附录

## A.1 路线任务

路线限制列表。如果 OSM 中的路线标签对策略施加了限制，例如速度限制、让行或施工，我们将其视为限制。路线特征是沿线的物理结构，例如坡道、
隧道和斑马线。路线操作是驾驶员在城市环境中正常操作车辆时遇到的不同场景，
例如多车道左转和环岛。

OSM = OpenStreetMap，VLM = 视觉语言模型，衍生：基于 OSM 数据的手工规则

## A.2 LLM（大语言模型）提示词

以下是根据要求翻译的中文内容：

使用groq配置LLM的提示词模板和伪代码，用于将自然语言查询解析为关于路线特征、限制和操作的结构化预测，并配合pydantic模型使用。自然语言查询的构建紧密遵循大多数GPS导航设备中提供的逐向导航指示。

```py
prompt_template: "You are parsing natural language driving instructions into PyDantic Model's output=model_dump_json(exclude_none=True) as JSON. Here are a few example pairs of instructions and structured output: {examples}. Based on these examples parse the instructions. The JSON must use the schema: {schema}"
groq:
model: llama-3.3-70b-versatile
temperature: 0.0
seed: 1334
response_format: json_object
max_sequence_len: 60000

```

示例对（展示30对中的3对）用于上下文学习，以引导LLM的结构化预测，其中ParsedInstructionModel是一个pydantic模型。

```py
PROMPT_PAIRS = [
(
            "下雪了。直行通过路口，在无标记路口遵循右侧先行规则",
        ParsedInstructionModel(
            	eventSequence=[
                    EventType(speed=FloatValue(value=10.0, operator="LT", unit="kph")),
                EventType(osmRouteManeuver="RIGHT_BEFORE_LEFT"),
                		EventType(speed=FloatValue(value=25.0, operator="LT", unit="kph")),
            	],
            turnSignal="OFF",
            weatherCondition="Snow",
        ),
        ),
(
            "在停车标志处停车，让行其他车辆，然后右转",
        ParsedInstructionModel(
            eventSequence=[
                	EventType(osmRouteRestriction="STOP"),
                EventType(turnSignal="RIGHT"),
                	EventType(speed=FloatValue(value=5.0, operator="LT", unit="kph")),
                EventType(osmRouteManeuver="RIGHT"),
            ],
            ),
    ),
    (
            "在雨天于双车道道路的坡道上停车",
        ParsedInstructionModel(
            	osmLaneCount=[IntValue(value=2, operator="EQ")],
                osmRouteFeature=["PARKING", "HILL_DRIVE"],
            weatherCondition="Rain",
            ),
    ),
]

EXAMPLES = ""
for idx, (instructions, parsed) in enumerate(PROMPT_PAIRS):
    parsed_json = parsed.model_dump_json(exclude_none=True)
    update = f"instructions: {instructions.lower()} output: {parsed_json}"
    EXAMPLES += update

from groq import Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": prompt_template.format(examples=EXAMPLES, schema=json.dumps(ParsedInstructionModel.model_json_schema(), indent=2))
                    },
                    {
                        "role": "user",
                        "content": f"instructions : 白天。开到红绿灯处，绿灯亮时左转",
                    },
                ],
                model=config["groq"]["model"],
                temperature=config["groq"]['temperature'],
                stream=False,
                seed=config["groq"]['seed'],
                response_format={"type": config['groq']['response_format']},
            )

            parsed_obj = ParsedInstructionModel.model_validate_json(chat_completion.choices[0].message.content)
            parsed_obj = parsed_obj.model_dump(exclude_none=True)

```

## A.2 数据采集硬件

![](/images/posts/679d9ef77d47.png)

车载计算平台：NVIDIA Jetson AGX Xavier

- 8核 @ 2/2.2 GHz，16/64 GB DDR5
- 100 TOPS，8通道 MIPI CSI-2 D-PHY 2.1（最高20Gbps）
- 8路 1080p30 视频编码器（H.265）
- 电源：10-15V DC输入，约90W功耗
- 存储：SSD M.2（4代PCIe 1x4）
- 视频输入 8个摄像头：2个Fakra MATE-AX接口，支持4个GMSL2，带同轴供电

- 2个Fakra MATE-AX接口，支持4个GMSL2，带同轴供电

车载计算平台：连接性

- 多频段、厘米级精度RTK模块
- 5G连接：M.2 USB3模块，最大下行速率3.5Gbps，上行速率900Mbps，双SIM卡

表6：用于数据采集的硬件套件信息

完整硬件套件规格请参见此处

---

> 本文由AI自动翻译，原文链接：[LeRobot goes to driving school: World’s largest open-source self-driving dataset](https://huggingface.co/blog/lerobot-goes-to-driving-school)
> 
> 翻译时间：2026-05-10 05:37
