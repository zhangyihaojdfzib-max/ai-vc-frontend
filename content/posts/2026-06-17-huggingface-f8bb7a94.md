---
title: 从Hugging Face到实体机器人：Strands Agents实战
title_original: From the Hugging Face Hub to robot hardware with Strands Agents and
  LeRobot
date: '2026-06-17'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/amazon/strands-lerobot-hub-to-hardware
author: ''
summary: 本文介绍了Strands Robots SDK如何将LeRobot技术栈集成到Agent循环中，实现从Hugging Face Hub数据集到实体机器人的端到端工作流。通过统一的AgentTools，开发者可以在仿真中录制演示数据、训练策略、测试部署，并仅通过修改一个关键字参数将相同代码部署到实体机器人。文章详细讲解了五个核心步骤，并提供了无需硬件的可运行示例，展示了如何利用对等网格协调多机器人集群。
categories:
- AI基础设施
tags:
- 机器人
- Hugging Face
- LeRobot
- Strands Agents
- 仿真到真实
draft: false
translated_at: '2026-06-18T06:53:06.918017'
---

# 从 Hugging Face Hub 到机器人硬件：Strands Agents 与 LeRobot 实战

通过 Strands Robots 中的 LeRobot 集成进行逐步讲解——一个 Agent 循环，从 Hub 数据集到实体机器人，采用相同磁盘格式的仿真到真实数据集，以及只需一个字符串即可切换的策略。

你有一个机器人、Hugging Face Hub 上的一份演示数据文件夹，以及一个希望它学习的新任务。如今这需要五个独立的工具：一个用于录制新的演示数据，一个用于训练，一个用于在仿真中测试，一个用于在硬件上部署的自定义代码，还有一个用于在拥有多个机器人时进行协调。这些组件各自独立运行，彼此之间无法通信。

Strands Robots 是来自 AWS 的开源 SDK（Apache 2.0 许可），它将机器人抽象、仿真以及 LeRobot 技术栈暴露为 AgentTools，你可以将它们组合成一个单一的 Strands agent。这种集成设计得非常精简：LeRobot 自身的脚本负责硬件录制和标定，而 Strands AgentTools 则用于处理 agent 实际编排的部分。仿真工具以 LeRobot 在硬件上写入的相同格式录制 LeRobotDataset。GR00T 和 LerobotLocal 在统一的接口背后提供策略推理服务，MolmoAct2 检查点则通过 LerobotLocal 路径运行。一个对等网格将 agent 扩展到远程机器人。数据集格式完全保持 LeRobot 写入时的原样；agent 循环则是粘合剂。

本文将通过一个 agent 内部的五个步骤进行讲解：基于 LeRobot AgentTools 构建 agent，在仿真中录制演示数据作为 LeRobotDataset，在同一机器人上运行策略，通过更改一个关键字参数将相同的 agent 代码部署到实体 SO-101 机器人上，并通过 Zenoh 网格向整个机器人集群广播指令。最后，你可以从 GitHub 克隆可运行的应用示例，并在笔记本电脑上的仿真环境中运行。默认路径无需硬件、无需 GPU、无需 Hugging Face 凭证。本文的可运行配套文件位于 `examples/lerobot/hub_to_hardware.py` 和 `hub_to_hardware.ipynb`。该笔记本默认仅使用仿真环境和 Mock 策略。

## 你将构建什么

Strands Robots SDK 将 LeRobot 技术栈暴露为 AgentTools，你可以将它们组合成一个 Strands agent。本文中的示例 agent 执行四项任务：在仿真中录制新的演示数据，将结果作为 LeRobotDataset 推送到 Hub，在仿真中针对相同格式运行策略，以及通过更改一个关键字参数将相同的 agent 代码部署到实体机器人。当你拥有多个机器人时，该 agent 可以通过内置的对等网格协调整个机器人集群。对于硬件录制和标定，LeRobot 自身的 CLI 工具（`lerobot-record`、`lerobot-calibrate`）负责启动工作；agent 从那里接手。

![arch_hugginface](/images/posts/eb73f606b1f3.png)

图 1. `Robot("so100")` 默认返回一个基于 MuJoCo 的仿真环境；`mode="real"` 则返回由 LeRobot 驱动的硬件机器人。两种模式共享相同的 DatasetRecorder 和相同的策略提供器，因此在仿真中捕获的数据集和在硬件上捕获的数据集使用相同的磁盘 LeRobotDataset 格式。

两个设计选择使这一切得以实现。首先，`Robot("so100")` 默认返回仿真环境（无需硬件，无风险），而 `mode="real"` 返回由 LeRobot 驱动的硬件机器人。agent 代码在两种模式下完全相同。其次，写入 LeRobotDataset 的 DatasetRecorder 在仿真路径和 LeRobot 自身的硬件录制之间共享，因此在 MuJoCo 中捕获的数据集和从实体 SO-101 捕获的数据集采用相同的格式。

整个工作流程只需五行 Python 代码：

```python
from strands_robots import Robot
from strands import Agent

arm = Robot("so100") 
agent = Agent(tools=[arm])
agent("Pick up the red cube")
```

接下来将逐步揭示该调用内部实际发生的事情。

## 前置条件

#### 最低要求（默认仿真路径）

- Python 3.12+，Linux 或 macOS（Apple Silicon 支持 MuJoCo 后端）。
- 用于 agent 推理的 Strands 兼容模型提供器。使用 AWS 凭证的 Amazon Bedrock、Anthropic API、OpenAI 或本地运行的 Ollama。
- 通过安装额外组件安装 Strands Robots：`uv pip install "strands-robots[sim-mujoco,lerobot,mesh]"`

仅此而已。本文中的示例在满足以上三个条件的笔记本电脑上即可端到端运行。

#### 高级要求（硬件部署、真实策略、Hub 推送）

- 一个具有写入权限的 Hugging Face 账户和 Token，用于从 Hub 推送数据集和拉取策略检查点。
- 对于硬件路径：一对 SO-101 从动臂和主控臂，或任何其他 LeRobot 支持的机器人。两个设备都需要在 `~/.cache/huggingface/lerobot/calibration/` 下存放标定文件。
- 对于本地 GR00T 推理：一块至少 16 GB 显存的 NVIDIA GPU 并安装 Docker。本文使用 gr00t_inference 工具的 `lifecycle="full"` 操作，该操作会在一次调用中拉取镜像、下载检查点并启动容器。

## 步骤 1 - 设置示例

安装 Strands Robots 并获取示例文件：

```bash
uv pip install "strands-robots[sim-mujoco,lerobot,mesh]"
git clone https://github.com/strands-labs/robots.git
cd robots
```

如果你希望 agent 从 Hub 推送数据集或拉取策略，请导出你的 Hugging Face Token。对于本文的默认仿真路径，这是可选的；该示例使用 Mock 策略端到端运行，并将数据集写入本地缓存，无需访问 Hub。

```bash
export HF_TOKEN=hf_...
```

可运行示例位于 `strands-labs/robots` 仓库中的 `examples/lerobot/hub_to_hardware.py`（Python 脚本）和 `hub_to_hardware.ipynb`（笔记本），与 MuJoCo 和 LIBERO 示例放在一起。推荐从笔记本开始：在 JupyterLab 中打开它，在仿真模式下从上到下运行单元格，无需连接任何硬件。

## 步骤 2 - 录制演示数据并推送到 Hub

仿真工具以 LeRobot 在硬件上写入的相同格式录制 LeRobotDataset。无需硬件。Simulation 工具的 `start_recording` 操作通过相同的 `DatasetRecorder` 类写入数据：关节状态和动作采用相同的 parquet 模式，每个摄像头采用相同的 MP4 布局。agent 提示几乎相同：

```python
from strands import Agent
from strands_robots import Robot

robot = Robot("so100")  
agent = Agent(tools=[robot])

agent(
    "Record a demonstration of 'pick the red cube and place it in the box' "
    "using the Mock policy provider at FPS 30. Write the dataset to "
    "my_user/cube_picking_sim and push to the Hub when done."
)
```

![sim_scene](/images/posts/7d0d0a0141e6.png)

图 2. MuJoCo 仿真中的录制场景：SO-100 机械臂伸向地面上的红色方块，捕获为 LeRobotDataset。此默认路径无需硬件、无需 GPU、无需 Hugging Face 凭证。

使用 Mock 策略是有意为之：它生成占位关节动作，使工作流程无需训练好的检查点即可端到端运行。机器人执行随机运动而非完成抓取，录制在结构上是完整的（有效的关节状态、有效的摄像头帧、格式良好的 LeRobotDataset 片段），但演示数据本身不能用作训练数据。下面的步骤 3 将替换为 GR00T 或 LerobotLocal 以实现真实的抓取行为。要在此步骤中看到实际的方块拾取，请运行 `--policy lerobot_local --checkpoint allenai/MolmoAct2-SO100_101`（一个 MolmoAct2 检查点，从其 config.json 自动检测并通过 LerobotLocal 路径路由）；提示、数据集格式和 agent 代码保持不变。

接下来发生的事情就是证明。LeRobot 自身的数据集加载器可以读取仿真录制的数据，无需任何 Strands 特定的代码路径：

```python
from lerobot.datasets.lerobot_dataset import LeRobotDataset

dataset = LeRobotDataset("my_user/cube_picking_sim")
print(dataset.features)
```

该特征字典与Hub上任何LeRobot数据集的形状完全相同：相同的列名、相同的parquet+MP4布局、相同的加载器路径。使用硬件录制数据的训练脚本无需修改即可使用模拟录制数据。如果您希望如此，从模拟环境推送的数据集可以与硬件录制数据存放在同一个Hub仓库中。

从录制的LeRobotDataset中回放单个片段，通过记录器写入的每个摄像头的MP4文件播放，训练脚本读取的也是相同的磁盘视频文件。

#### 在硬件上录制

要在物理SO-101机器人而非模拟环境中录制演示数据，请直接使用LeRobot的录制命令行工具。Strands集成并未将该命令封装为AgentTool，因为LeRobot已经很好地完成了这项工作：

```bash
lerobot-calibrate --robot.type=so101_follower --robot.id=my_follower
lerobot-calibrate --robot.type=so101_leader   --robot.id=my_leader

lerobot-record \
  --robot.type=so101_follower --robot.id=my_follower \
  --teleop.type=so101_leader  --teleop.id=my_leader \
  --dataset.repo_id=my_user/cube_picking \
  --dataset.single_task='Pick up the red cube and place it in the box' \
  --dataset.num_episodes=25 \
  --dataset.push_to_hub=true

```

通过此命令上传到Hub的数据集与模拟录制的数据格式相同。要在此基础上微调策略，请运行LeRobot的训练命令行工具（lerobot-train）；训练本身不在本文讨论范围内，遵循标准的LeRobot工作流程。从步骤3开始，Agent可以互换使用原始检查点或微调后的检查点。有关完整的SO-101硬件设置、校准指南和故障排除，请参阅示例文件夹中的README文件。

## 步骤3 - 在模拟环境中运行策略

数据集上传到Hub后，下一步是运行策略。该示例使用默认模拟模式下的`Robot()`工厂，然后附加`gr00t_inference`，以便Agent管理推理容器：

```python
from strands import Agent
from strands_robots import Robot, gr00t_inference

robot = Robot("so100")  
agent = Agent(tools=[robot, gr00t_inference])

agent(
    "Start GR00T inference on port 5555 with the cube-picking checkpoint "
    "from my_user/cube-picker. Then ask the robot to pick up the red cube."
)

```

在底层，Agent运行`gr00t_inference(action="lifecycle", lifecycle="full", ...)`来拉取GR00T容器镜像，从Hub下载检查点，并启动推理服务。然后，它在模拟机器人上以`policy_provider="groot"`执行`run_policy`动作，在`policy_config`字典中传递GR00T服务的主机和端口（容器可通过端口5555访问）。模拟过程使用策略的动作块进行，结果渲染可通过`Simulation.render`查看。

![sim_grasp](/images/posts/e6233a60a1b9.png)

图3. 使用训练好的策略（GR00T或MolmoAct2检查点），Agent驱动SO-100在模拟环境中抓取红色立方体，这是Mock策略所模拟的行为。

对于偏好进程内推理（无需容器，无需ZeroMQ (ZMQ)）的开发者，可以将`gr00t_inference`替换为从Hub仓库加载的`LerobotLocalPolicy`实例。该提供程序会将任何以`lerobot/`开头的模型ID路由到进程内路径：

```python
from strands_robots.policies import create_policy
policy = create_policy("lerobot/act_aloha_sim_transfer_cube_human")

```

`LerobotLocalPolicy`支持ACT、Diffusion Policy、SmolVLA、π0和π0.5，即LeRobot自身策略注册表能从`config.json`解析的任何模型。对于附带`rtc_config`的流匹配策略（π0、SmolVLA），实时分块功能会自动启用。

NVIDIA最近发布的Cosmos 3也可作为同一接口背后的策略提供程序，因此无论您指向哪个提供程序，Agent代码都保持不变。

注意：`LerobotLocalPolicy`加载Hugging Face模型时使用`trust_remote_code=True`。设置`STRANDS_TRUST_REMOTE_CODE=1`以选择加入，并且只加载来自您信任的组织机构的检查点。

## 步骤4 - 将策略部署到物理硬件

此代码与步骤3相同，仅更改了一个关键字参数。`Robot`工厂返回一个由LeRobot的`make_robot_from_config`驱动的硬件支持机器人：

```python
robot = Robot(
    "so100",
    mode="real",
    port="/dev/ttyACM0",
    data_config="so100_dualcam",
    cameras={
        "front": {"type": "opencv", "index_or_path": "/dev/video0", "fps": 30},
        "wrist": {"type": "opencv", "index_or_path": "/dev/video2", "fps": 30},
    },
)
agent = Agent(tools=[robot, gr00t_inference])

agent(
    "Start GR00T inference on port 5555 with the cube-picking checkpoint "
    "from my_user/cube-picker. Then ask the robot to pick up the red cube."
)

```

相同的Agent提示词现在针对物理机械臂运行。硬件路径使用LeRobot的机器人抽象层进行关节命令和摄像头读取，而可通过端口5555访问的GR00T容器则生成动作块。

在针对您的SO-101运行之前，必须完成从动臂和主动臂的校准。每台设备运行一次LeRobot的校准命令（`lerobot-calibrate`）；校准文件存放在`~/.cache/huggingface/lerobot/calibration/`目录下，任何涉及硬件的Strands代码路径都会从此处读取。如果缺少校准，Agent会从LeRobot驱动层抛出错误。

## 步骤5 - 使用网格协调多台机器人

到目前为止，我们一次只驱动一台机器人。网格是Strands Robots处理多台机器人的方式。想象一下，您桌上的主动臂远程操控另一房间的从动臂，或者五台SO-101并行执行相同的仓库任务，或者一个人形机器人与移动底座协调工作。所有这些都属于网格模式。网格基于Zenoh构建，Zenoh是一个开源的点对点协议，您无需管理IP地址、编写发现代码或选择代理；新机器人一上线就会出现在网格上，Agent可以同时与所有机器人通信。

每个`Robot()`和每个`Simulation()`都会自动加入一个Zenoh对等网格。`robot_mesh`工具为Agent提供了用于集群操作的词汇表，例如发现、结构化命令、广播和紧急停止：

```python
agent = Agent(tools=[robot_mesh])

agent(
    "List every robot and simulation on the mesh. "
    "Then send 'go to home pose' to each one in parallel."
)

```

Agent调用`robot_mesh(action="peers")`来枚举本地和已发现的节点，然后调用`robot_mesh(action="broadcast", ...)`向每个节点发送带有超时的结构化命令。添加`[mesh-iot]`扩展包可将此流量路由到AWS IoT Core，用于跨网络集群。项目文档中的`robot_mesh`工具动作参考涵盖了完整的词汇表：订阅、监视、收件箱和结构化点对点命令。

默认情况下，每个物理执行网格动作在执行前都会暂停等待人工批准中断：包括集群范围的广播和紧急停止，以及单节点通信、发送和停止。您可以通过`STRANDS_MESH_HITL_ACTIONS`环境变量调整此集合（设置为`all`、`none`或逗号分隔的子集）。首次运行此示例时，您会在终端中看到`robot_mesh-broadcast-approval`提示；输入`y`（或`yes`/`approve`）以授权广播。该批准通过LLM工具参数之外的带外方式传递，因此试图将批准标志混入命令体的提示注入攻击无法绕过此关卡。

传输层可扩展，无需修改Agent代码。内置的Zenoh网格是自动回退方案：在局域网中，Zenoh多播无需代理即可处理节点发现；添加`[mesh-iot]`扩展包后，流量通过AWS IoT Core（基于mTLS的MQTT5）路由用于云端集群，并附带一个BridgeTransport，通过单一API连接局域网和云端（通过`STRANDS_MESH_BACKEND=bridge`选择）。

对于生产集群，Device Connect（与Arm合作开发的设备感知网络层）负责处理设备发现、在线状态、结构化RPC、事件路由及安全控制。当Device Connect可用时，相同的robot_mesh工具会通过它进行调度，否则将回退至内置的Zenoh网格，因此本文中的Agent（智能体）代码在两种情况下均无需修改。有关设置和当前可用性，请参阅Device Connect文档。

## 使用示例应用程序进行尝试

完整示例代码位于GitHub的strands-labs/robots仓库的examples/lerobot/文件夹中。它将全部五个步骤打包为一个CLI脚本（hub_to_hardware.py）和一个Notebook（hub_to_hardware.ipynb）。CLI默认使用Mock策略在模拟环境中端到端运行。无需GPU、Docker或Hugging Face凭证。

```bash
uv pip install "strands-robots[sim-mujoco,lerobot,mesh]"
git clone https://github.com/strands-labs/robots.git
cd robots

export STRANDS_MESH_LOCAL_DEV=1

python examples/lerobot/hub_to_hardware.py

```

录制数据集将保存在~/.cache/huggingface/lerobot/local/strands-cube-pick/目录下。若要将数据推送到Hugging Face Hub而非本地保存，请在导出具有写入权限的HF_TOKEN后，添加--hf-user <your-user>参数。对于步骤3中的真实抓取行为，请使用--policy groot --checkpoint <hf_repo>（需要Docker + NVIDIA GPU）或--policy lerobot_local --checkpoint <hf_repo>（需要GPU和STRANDS_TRUST_REMOTE_CODE=1）。

Notebook（examples/lerobot/hub_to_hardware.ipynb）以单元格为单位逐步演示相同的工作流程，并在每个步骤之间提供说明。在JupyterLab中打开它，并在模拟模式下从头到尾运行。

## 安全注意事项

本文展示的代码片段是使用HuggingFace设置Strands Robots的“hello world”示例。对于更严肃、面向生产环境的用例，用户应注意以下重要事项：

#### 提示词注入

向Agent（智能体）提供不可信数据可能导致提示词注入，即不可信的上下文被当作LLM（大语言模型）指令处理。鉴于这些机器人在物理空间中的驱动能力，这是一个需要关注的重要风险。为缓解此问题，开发者应谨慎确保仅向机器人提供来自可信来源的数据。如果无法信任所有输入数据，开发者应限制Agent（智能体）可用的工具，以防止机器人执行安全关键操作。

#### 机器人网格认证行为

本文代码片段中使用的STRANDS_MESH_LOCAL_DEV=1设置会在无认证或访问控制的情况下初始化机器人网格。这意味着同一网络上的任何设备都可以向机器人集群发送指令。这对于受信任的开发环境是可接受的，但不适用于不受信任的网络或生产环境。对于这些用例，需要使用STRANDS_MESH_AUTH_MODE=mtls。

#### 集群范围操作的操作员审批

robot_mesh工具的物理驱动操作会影响网络上的对等节点：广播和紧急停止会到达所有对等节点，而告知、发送和停止则仅针对单个对等节点。为防止Agent（智能体）自主（或在提示词注入下）发出这些命令，默认情况下所有五个操作都通过人工介入中断进行控制。当Agent（智能体）调用受控操作时，Strands运行时会暂停Agent（智能体）循环，并要求操作员在LLM（大语言模型）工具参数之外进行批准。您可以使用STRANDS_MESH_HITL_ACTIONS环境变量（可选值为all、none或逗号分隔的子集）来调整受控操作集。每次操作的速率限制、命令验证和审计跟踪与中断机制并行运行。在Agent（智能体）循环之外（如裸脚本或单元测试），受控操作将默认失败。

## 清理

上述工作流程会启动一个GR00T容器，打开硬件上的串行端口，并写入本地数据集缓存。要将环境恢复到干净状态：

- 停止GR00T推理容器：agent.tool.gr00t_inference(action="stop", port=5555)，或使用lifecycle="teardown"同时移除容器。
- 释放串行端口：如果您运行了硬件路径，请断开SO-101从站和主站的连接。
- （可选）删除本地数据集缓存：录制的数据集位于~/.cache/huggingface/lerobot/<repo_id>下。您推送到Hub的数据集不受影响。

## 集成原理

该集成的核心设计选择是Strands Robots不会重新实现LeRobot已提供的功能。硬件抽象、校准和数据集格式保持在上游。Strands添加了AgentTool接口，使其能够通过自然语言进行组合。

这带来了两个结果。对于用户而言，Hub上的每个数据集都是Agent（智能体）可以扩展、微调并部署的资产，无需任何转换步骤。对于开发者而言，模拟数据和硬件数据共享单一文件格式，因此为一种数据编写的训练脚本可直接用于另一种数据。模拟与现实之间的界限变成了部署细节，而非架构鸿沟。

## 后续方向

![集群](/images/posts/9b6d97092206.png)

图4. Strands Robots产品目录涵盖机械臂、人形机器人、四足机器人和灵巧手，全部在相同的MuJoCo模拟环境中，并位于相同的Robot()工厂之后。本文中的SO-100是众多支持的具身形态之一。

完整的Strands Robots文档深入介绍了机器人目录、模拟、策略提供者、网格和Device Connect。对于更大规模的工作负载，strands-labs/robots-sim仓库托管了更重的模拟后端，包括Isaac Sim和Newton，以及一个LIBERO基准测试示例。这两个后端都接入本文所示的相同Robot抽象，因此随着规模扩展，Agent（智能体）代码保持不变。

欢迎在Apache 2.0许可下贡献代码。如果您使用此工作流程构建了某些内容，请通过Issue告知哪些有效、哪些无效。当开发者的反馈直接作用于需要改进的界面时，SDK的改进速度最快。

## 资源

- Strands Robots（SDK、AgentTools、Robot工厂）：github.com/strands-labs/robots，Apache 2.0
- Strands Robots文档（完整文档）：strands-labs.github.io/robots
- Strands Robots Sim（示例、模拟后端）：github.com/strands-labs/robots-sim
- 示例：examples/lerobot/hub_to_hardware.py和hub_to_hardware.ipynb
- 如何构建物理AI Agent（智能体）：真实世界机器人的自然语言：直播和博客
- 深入探讨物理AI | S1E4 | 使用NVIDIA NeMo Agent Toolkit和Bedrock AgentCore实现自动化：直播
- LeRobot：github.com/huggingface/lerobot - 数据集、策略、硬件驱动
- Strands Agents SDK：github.com/strands-agents/harness-sdk
- SmolVLA：SmolVLA
- Pi0：Pi0
- NVIDIA Isaac-GR00T N1.7：GR00T N1.7
- NVIDIA Cosmos3 Nano：Cosmos 3 Nano

## 作者

Cagatay Cali是AWS的研究工程师，专注于Agentic AI和机器人技术。他设计将AI Agent（智能体）连接到物理机器人的接口，使开发者能够通过自然语言控制机器人系统，并使Agent（智能体）和机器人开发对任何技能水平的构建者都触手可及。

Sundar Raghavan是AWS Agentic AI Foundations团队的高级解决方案架构师。他负责Amazon Bedrock AgentCore的开发者体验，拥有SDK和CLI的所有权，并推动框架和生态系统集成战略。他专注于开发者如何在AWS上构建、部署和扩展生产级AI Agent（智能体）。目前，他正将这一关注点扩展到物理AI领域，通过合作开发Strands Robots，将相同的Agent（智能体）开发者体验引入机器人技术。

---

> 本文由AI自动翻译，原文链接：[From the Hugging Face Hub to robot hardware with Strands Agents and LeRobot](https://huggingface.co/blog/amazon/strands-lerobot-hub-to-hardware)
> 
> 翻译时间：2026-06-18 06:53
