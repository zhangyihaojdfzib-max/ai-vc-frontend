---
title: 开放评估标准：用NeMo Evaluator基准测试Nemotron 3 Nano
title_original: 'The Open Evaluation Standard: Benchmarking NVIDIA Nemotron 3 Nano
  with NeMo Evaluator'
date: '2025-12-17'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/nemotron-3-nano-evaluation-recipe
author: null
summary: 本文介绍了NVIDIA为Nemotron 3 Nano 30B A3B模型推出的开放评估方法。通过开源NeMo Evaluator库和完整的评估方案，NVIDIA旨在解决模型评估中因配置、数据集或工具差异导致的结果不可比问题。文章阐述了该工具如何提供一致、透明且可复现的评估工作流，使开发者能够独立验证结果、进行有意义的模型比较，并构建自己的标准化评估流程，从而推动AI领域的开放创新与可靠进步。
categories:
- AI研究
tags:
- 模型评估
- NVIDIA
- 开源工具
- 基准测试
- 可复现性
draft: false
---

开放评估标准：使用NeMo Evaluator对NVIDIA Nemotron 3 Nano进行基准测试
评估模型所报告的改进是反映了真正的进步，还是源于评估条件、数据集构成或训练数据（这些数据可能模仿了基准任务）的差异，正变得越来越具有挑战性。NVIDIA Nemotron的开放方法通过发布透明且可复现的评估方案来解决这一问题，使得结果能够被独立验证。
NVIDIA发布了Nemotron 3 Nano 30B A3B，并采用了明确的开放评估方法，以使这种区别清晰可见。除了模型卡片，我们还发布了用于生成结果的完整评估方案，该方案基于NVIDIA NeMo Evaluator库构建，因此任何人都可以重新运行评估流程、检查相关产物并独立分析结果。
我们相信开放创新是AI进步的基石。这种程度的透明度至关重要，因为大多数模型评估都省略了关键细节。配置、提示词、评估工具版本、运行时设置和日志常常缺失或未明确说明，而这些参数的微小差异都可能实质性地改变结果。没有一个完整的方案，几乎不可能判断一个模型是真正更智能，还是仅仅针对某个基准测试进行了优化。
这篇博客向开发者展示了如何完全使用开放的工具、配置和产物来复现Nemotron 3 Nano 30B A3B背后的评估过程。您将了解评估是如何运行的、方法论为何重要，以及如何使用NeMo Evaluator库执行相同的端到端工作流，从而验证结果、一致地比较模型，并构建您自己透明的评估流程。

使用NeMo Evaluator构建一致且透明的评估工作流
一个单一、一致的评估系统
开发者和研究人员需要的是他们可以依赖的评估工作流，而不是针对不同模型表现各异的临时脚本。NeMo Evaluator提供了一种统一的方式，可以一次性定义基准测试、提示词、配置和运行时行为，然后在不同模型和版本中复用该方法论。这避免了常见的场景：评估设置在多次运行之间悄然改变，使得跨时间比较变得困难或具有误导性。
独立于推理设置的方法论
模型的输出可能因推理后端和配置而异，因此评估工具绝不应绑定到单一的推理解决方案。将评估工具锁定在一个推理解决方案上会限制其用途。NeMo Evaluator通过将评估流程与推理后端分离来避免这个问题，允许相同的配置针对托管端点、本地部署或第三方提供商运行。这种分离使得即使在您更换基础设施或推理引擎时，也能进行有意义的比较。
为超越一次性实验的规模化而构建
许多评估流程在初次运行时有效，但随着范围扩大就会失效。NeMo Evaluator的设计旨在从快速的单一基准验证扩展到完整的模型卡片套件，以及对多个模型的重复评估。启动器、产物布局和配置模型支持持续的工作流，而不仅仅是孤立的实验，因此团队可以随着时间的推移保持一致的评估实践。
通过结构化产物和日志实现可审计性
透明的评估需要的不仅仅是最终分数。默认情况下，每次评估运行都会产生结构化的结果和日志，便于检查分数是如何计算的、理解分数计算过程、调试意外行为以及进行更深入的分析。评估的每个组成部分都被捕获并可复现。
一个共享的评估标准
通过发布Nemotron 3 Nano 30B A3B及其完整的评估方案，NVIDIA提供了一个可供社区运行、检查和构建的参考方法论。使用相同的配置和工具，为基准测试的选择、执行和解释带来了一致性，从而能够在不同模型、提供商和版本之间进行更可靠的比较。

Nemotron 3 Nano的开放评估
开放评估意味着不仅要发布最终结果，还要发布其背后的完整方法论，以便基准测试能够一致地运行，并且结果能够随着时间的推移进行有意义的比较。对于Nemotron 3 Nano 30B A3B，这包括开源的评估工具、透明的配置以及任何人都可以端到端运行的可复现产物。
开源模型评估工具
NeMo Evaluator是一个开源库，旨在对生成模型进行稳健、可复现和可扩展的评估。它并非引入另一个独立的基准测试运行器，而是作为一个统一的编排层，将多个评估工具整合到一个一致的单接口下。
在此架构下，NeMo Evaluator集成并协调了来自多个广泛使用的评估工具的数百个基准测试，包括用于Nemotron指令遵循、工具使用和智能体评估的NeMo Skills，用于基础模型和预训练基准测试的LM Evaluation Harness，以及许多其他工具（完整基准测试目录）。每个工具都保留了其原生逻辑、数据集和评分语义，而NeMo Evaluator则标准化了它们的配置、执行和日志记录方式。
这带来了两个实际优势：团队可以使用单一配置运行多样化的基准测试类别，而无需重写自定义评估脚本；来自不同工具的结果以一致、可预测的方式存储和检查，即使底层任务不同。NVIDIA Nemotron研究和模型评估团队内部使用的同一编排框架现已向社区开放，使开发者能够通过共享的、可审计的工作流运行异构的、多工具的评估。
开放配置
我们发布了用于Nemotron 3 Nano 30B A3B模型卡片评估的确切YAML配置（使用NeMo Evaluator）。这包括：
- 模型推理和部署设置
- 基准测试和任务选择
- 特定于基准测试的参数，如采样、重复次数和提示词模板
- 运行时控制，包括并行度、超时和重试
- 输出路径和产物布局
使用相同的配置意味着运行相同的评估方法论。
开放日志和产物
每次评估运行都会产生结构化的、可检查的输出，包括：
- 每个任务的`results.json`文件
- 用于调试和审计的执行日志
- 按任务组织的产物，便于比较
这种结构使得不仅能够理解最终分数，还能了解这些分数是如何产生的，并对模型行为进行更深入的分析。

可复现性工作流
复现Nemotron 3 Nano 30B A3B模型卡片结果遵循一个简单的循环：
- 从发布的模型检查点或托管端点开始
- 使用已发布的NeMo Evaluator配置
- 通过单个CLI命令执行评估
- 检查日志和产物，并将结果与模型卡片进行比较
相同的工作流适用于您使用NeMo Evaluator评估的任何模型。您可以将评估指向托管端点或本地部署，包括常见的推理提供商，如HuggingFace、build.nvidia.com和OpenRouter。关键要求是能够访问模型，无论是可以作为权重提供服务，还是可以作为端点调用。在本教程中，我们使用build.nvidia.com上的托管端点。

复现Nemotron 3 Nano基准测试结果
本教程使用NeMo Evaluator复现NVIDIA Nemotron 3 Nano 30B A3B的评估结果。包含用于模型卡片评估的已发布配置的分步教程可在GitHub上找到。

虽然本教程主要聚焦于Nemotron 3 Nano 30B A3B，但我们也发布了基础模型的评估方案。
本指南将使用以下基准测试，对NVIDIA Nemotron 3 Nano 30B A3B模型卡评估所用的已发布配置，运行一套全面的评估套件：

| 基准测试 | 准确率 | 类别 | 描述 |
|---|---|---|---|
| BFCL v4 | 53.8 | 函数调用 | 伯克利函数调用排行榜 v4 |
| LiveCodeBench (v6 2025-08–2025-05) | 68.3 | 代码 | 真实世界编程问题评估 |
| MMLU-Pro | 78.3 | 知识 | 多任务语言理解（10选1） |
| GPQA | 73.0 | 科学 | 研究生级别科学问题 |
| AIME 2025 | 89.1 | 数学 | 美国数学邀请赛 |
| SciCode | 33.3 | 科学编程 | 科学编程挑战 |
| IFBench | 71.5 | 指令遵循 | 指令遵循基准测试 |
| HLE | 10.6 | 人类终极考试 | 跨领域专家级问题 |

有关模型卡的详细信息，请参阅[NVIDIA Nemotron 3 Nano 30B A3B 模型卡](https://huggingface.co/nvidia/Nemotron-3-Nano-30B-A3B)。如需深入了解架构、数据集和基准测试，请阅读完整的[Nemotron 3 Nano 技术报告](https://resources.nvidia.com/en-us-large-language-models/nemotron-3-nano)。

1.  **安装 NeMo Evaluator Launcher**
    ```bash
    pip install nemo-evaluator-launcher
    ```

2.  **设置必要的环境变量**
    ```bash
    # NVIDIA 端点访问
    export NGC_API_KEY="your-ngc-api-key"
    # Hugging Face 访问
    export HF_TOKEN="your-huggingface-token"
    # 仅对基于评判的基准测试（如 HLE）需要
    export JUDGE_API_KEY="your-judge-api-key"
    ```
    可选但建议设置以加速重新运行：
    ```bash
    export HF_HOME="/path/to/your/huggingface/cache"
    ```

3.  **模型端点**
    评估使用托管在 build.nvidia.com 上的 NVIDIA API 端点：
    ```yaml
    target:
      api_endpoint:
        model_id: nvidia/nemotron-nano-3-30b-a3b
        url: https://integrate.api.nvidia.com/v1/chat/completions
        api_key_name: NGC_API_KEY
    ```
    评估可以针对常见的推理服务提供商运行，例如 HuggingFace、build.nvidia.com 或 OpenRouter，或者模型可用的任何端点。
    如果您在本地托管模型或使用不同的端点：
    ```bash
    nemo-evaluator-launcher run \
      --config local_nvidia_nemotron_3_nano_30b_a3b.yaml \
      -o target.api_endpoint.url=http://localhost:8000/v1/chat/completions
    ```

4.  **运行完整评估套件**
    使用 `--dry-run` 预览运行而不实际执行：
    ```bash
    nemo-evaluator-launcher run \
      --config local_nvidia_nemotron_3_nano_30b_a3b.yaml \
      --dry-run
    ```
    从示例目录中，使用提供的 YAML 配置运行评估：
    ```bash
    nemo-evaluator-launcher run \
      --config /path/to/examples/nemotron/local_nvidia_nemotron_3_nano_30b_a3b.yaml
    ```
    注意，为了快速测试，您可以通过设置 `limit_samples` 来限制样本数量：
    ```bash
    nemo-evaluator-launcher run \
      --config local_nvidia_nemotron_3_nano_30b_a3b.yaml \
      -o evaluation.nemo_evaluator_config.config.params.limit_samples=10
    ```

5.  **运行单个基准测试**
    您可以使用 `-t` 标志运行特定的基准测试（从 `examples/nemotron` 目录）：
    ```bash
    # 仅运行 MMLU-Pro
    nemo-evaluator-launcher run --config local_nvidia_nemotron_3_nano_30b_a3b.yaml -t ns_mmlu_pro
    # 仅运行代码基准测试
    nemo-evaluator-launcher run --config local_nvidia_nemotron_3_nano_30b_a3b.yaml -t ns_livecodebench
    # 运行多个特定基准测试
    nemo-evaluator-launcher run --config local_nvidia_nemotron_3_nano_30b_a3b.yaml -t ns_gpqa -t ns_aime2025
    ```

6.  **监控执行并检查结果**
    ```bash
    # 检查特定任务的状态
    nemo-evaluator-launcher status
    # 流式传输特定任务的日志
    nemo-evaluator-launcher logs <job-id>
    ```
    结果写入定义的输出目录：
    ```
    results_nvidia_nemotron_3_nano_30b_a3b/
    ├── artifacts/
    │   └── <task_name>/
    │       └── results.json
    └── logs/
        └── stdout.log
    ```

**解读结果**
在复现评估时，您可能会观察到不同运行之间最终分数存在微小差异。这种差异反映了LLM的概率性本质，而非评估流程的问题。现代评估引入了多个非确定性来源：解码设置、重复试验、基于评判的评分、并行执行以及服务基础设施的差异。所有这些都可能导致轻微的波动。

开放评估的目的不是强制要求比特级完全相同的输出，而是提供方法学上的一致性，并确保评估结果有清晰的来源。为确保您的评估与参考标准一致，请验证以下内容：
*   **配置**：使用已发布的 NeMo Evaluator YAML 文件而不作修改，或明确记录任何更改
*   **基准测试选择**：运行指定的任务、任务版本和提示词模板
*   **推理目标**：验证您正在评估的是预期的模型和端点，包括相关的聊天模板行为和推理设置
*   **执行设置**：保持运行时参数一致，包括重复次数、并行度、超时和重试行为
*   **输出**：确认产物和日志完整，并遵循每个任务的预期结构

当这些要素保持一致时，即使单次运行略有不同，您的结果也代表了该方法的有效复现。NeMo Evaluator 简化了这一过程，将基准测试定义、提示词、运行时设置和推理配置整合到一个可审计的工作流程中，以最大限度地减少不一致性。

**结论：为开源模型建立更透明的标准**
与 Nemotron 3 Nano 一同发布的评估方案，标志着向更透明、更可靠的开源模型评估方法迈出了重要一步。我们正在从评估作为一系列定制化、"黑盒"脚本的集合，转向一个定义明确的系统，其中基准测试选择、提示词和执行语义都被编码到一个透明的工作流程中。

对于开发者和研究人员而言，这种透明度改变了分享结果的意义。一个分数的可信度取决于其背后的方法论，而公开该方法论正是让社区能够验证声明、公平比较模型并在共享基础上继续构建的关键。通过开放的评估配置、开放的产物和开放的工具，Nemotron 3 Nano 展示了这种对开放性的承诺在实践中的样子。

NeMo Evaluator 通过提供跨模型、跨版本和跨推理环境的一致基准测试方法来支持这一转变。目标并非每次运行都得到完全相同的数字，而是对一种明确、可检查、可重复的评估方法充满信心。对于需要自动化或大规模评估流程的组织，一个独立的微服务产品提供了基于相同评估原则构建的企业级 NeMo Evaluator 微服务。

使用已发布的 NeMo Evaluator 评估配置，进行端到端的评估方案演练。

**加入社区！**
NeMo Evaluator 是完全开源的，社区的参与对于塑造开放评估的未来至关重要。如果您希望我们支持某个基准测试，或有改进建议，请提交问题，或直接在 GitHub 上贡献代码。您的贡献有助于加强生态系统，并推进评估生成式模型的共享、透明标准。

---

> 本文由AI自动翻译，原文链接：[The Open Evaluation Standard: Benchmarking NVIDIA Nemotron 3 Nano with NeMo Evaluator](https://huggingface.co/blog/nvidia/nemotron-3-nano-evaluation-recipe)
> 
> 翻译时间：2026-01-05 13:14
