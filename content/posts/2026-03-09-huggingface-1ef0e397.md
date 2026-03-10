---
title: Ulysses序列并行：实现百万Token上下文的高效训练
title_original: 'Ulysses Sequence Parallelism: Training with Million-Token Contexts'
date: '2026-03-09'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ulysses-sp
author: ''
summary: 本文介绍了Ulysses序列并行技术，这是一种解决大语言模型在超长序列（如百万Token）上训练时内存挑战的创新方法。Ulysses通过将输入序列沿序列维度分割到多个GPU上，并利用注意力头的独立性，通过全对全通信交换键值对，使每个GPU仅计算部分注意力头，从而显著降低内存需求。文章详细阐述了其工作原理、通信复杂度，并探讨了其与Hugging
  Face生态系统（如Accelerate、Transformers Trainer和TRL SFTTrainer）的集成，为文档分析、代码理解等需要超长上下文的任务提供了可行的训练方案。
categories:
- AI基础设施
tags:
- 序列并行
- 长上下文训练
- 大语言模型
- 分布式训练
- 注意力机制
draft: false
translated_at: '2026-03-10T04:42:55.794298'
---

# Ulysses序列并行：百万Token上下文训练

在长序列上训练大语言模型已成为构建强大AI系统的关键。随着模型越来越多地用于文档分析、代码理解、复杂推理和RAG（检索增强生成）等工作负载，处理数十万甚至数百万Token序列的需求急剧增长。举个例子，一本平均长度的书大约有25万个Token，因此要在多文档上下文或书籍长度的输入上进行训练，就需要处理远超单个GPU容量的序列。然而，使用如此长的上下文进行训练带来了巨大的内存挑战：注意力计算与序列长度呈平方级增长，对于超过数万个Token的上下文，很快就会超出GPU内存。

Ulysses序列并行（源自Snowflake AI Research的Arctic长序列训练协议的一部分）通过注意力头并行将注意力计算分布到多个GPU上，提供了一个优雅的解决方案。在本文中，我们将探讨Ulysses的工作原理，以及它如何集成到Hugging Face生态系统中——从Accelerate到Transformers Trainer和TRL的SFTTrainer。

## 目录

- 长序列训练的挑战
- Ulysses的工作原理
- 与Accelerate的集成
- 与Transformers Trainer的集成
- 与TRL的SFTTrainer的集成
- Ulysses与环形注意力的比较
- 最佳实践
- 基准测试
- 资源

## 长序列训练的挑战

Transformer中的注意力机制与序列长度呈平方级扩展。对于一个长度为 n 的序列，标准注意力需要 O(n²) FLOPs 和 O(n²) 内存来计算和存储注意力分数矩阵。像FlashAttention这样的优化实现通过分块计算且从不具体化完整的注意力矩阵，将内存需求降低到 O(n)——但 O(n²) 的计算量依然存在。对于超长序列（32k+ Token），即使使用FlashAttention，训练仍然会触及单GPU内存的极限。

考虑以下长上下文训练至关重要的场景：

- 文档理解：处理整本书、法律文件或研究论文
- 代码分析：理解包含多个互连文件的大型代码库
- 推理任务：模型在推理过程中"逐步思考"可能会生成数千个Token
- 检索增强生成：将许多检索到的段落整合到上下文中

传统的数据并行在这里没有帮助——每个GPU仍然需要在注意力块内处理完整的序列。我们需要一种将序列本身拆分到多个设备上的方法。

## Ulysses的工作原理

Ulysses序列并行（SP）在DeepSpeed Ulysses论文中提出，采用了一种巧妙的方法：除了在序列维度上进行分割外，它还将注意力头分配到多个GPU上。

![Ulysses沿序列维度分割输入序列，并使用全对全通信交换键值对，使每个GPU能够计算一个注意力头子集。（来源：Snowflake Engineering Blog）](/images/posts/7d9fa1f66201.png)

其工作原理如下：

1. 序列分片：输入序列沿序列维度在 P 个GPU上进行分割。每个GPU i 持有令牌 [i⋅n/P, (i+1)⋅n/P)。
2. QKV投影：每个GPU为其本地序列块计算查询、键和值投影。
3. 全对全通信：一个全对全集合操作重新分配数据，使得每个GPU在投影后持有所有序列位置，但仅针对一个注意力头子集。
4. 本地注意力：每个GPU使用标准注意力机制（FlashAttention或SDPA）为其分配的注意力头计算注意力。
5. 全对全通信：另一个全对全操作反转重新分配过程，返回到序列分片格式。
6. 输出投影：每个GPU为其本地序列块计算输出投影。

序列分片：输入序列沿序列维度在 P 个GPU上进行分割。每个GPU i 持有令牌 [i⋅n/P, (i+1)⋅n/P)。

QKV投影：每个GPU为其本地序列块计算查询、键和值投影。

全对全通信：一个全对全集合操作重新分配数据，使得每个GPU在投影后持有所有序列位置，但仅针对一个注意力头子集。

本地注意力：每个GPU使用标准注意力机制（FlashAttention或SDPA）为其分配的注意力头计算注意力。

全对全通信：另一个全对全操作反转重新分配过程，返回到序列分片格式。

输出投影：每个GPU为其本地序列块计算输出投影。

关键见解在于注意力头是独立的——每个头可以单独计算。通过用序列局部性换取头局部性，Ulysses能够以相对较低的通信开销实现高效的并行化。

### 通信复杂度

Ulysses每个注意力层需要两次全对全操作，每个GPU的总通信量为 O(n⋅d/P)，其中：

- n 是序列长度
- d 是隐藏维度
- P 是并行度

环形注意力通过 P-1 次顺序的点对点传输，每个GPU通信 O(n⋅d)——多出 P 倍。Ulysses还受益于更低的延迟，因为全对全操作可以在单个集合步骤中利用全二分带宽，而环形注意力则需要串行化经过 P-1 跳。

## 与Accelerate的集成

Accelerate通过其ParallelismConfig类和DeepSpeed集成，为Ulysses序列并行提供了基础。

### 配置

```python
from accelerate import Accelerator
from accelerate.utils import ParallelismConfig, DeepSpeedSequenceParallelConfig

parallelism_config = ParallelismConfig(
    sp_backend="deepspeed",
    sp_size=4,  
    dp_shard_size=1,  
    sp_handler=DeepSpeedSequenceParallelConfig(
        sp_seq_length=None,  
        sp_seq_length_is_variable=True,
        sp_attn_implementation="flash_attention_2",  
    ),
)

accelerator = Accelerator(parallelism_config=parallelism_config)

```

### 关键参数

### 使用Accelerator

当你调用 `accelerator.prepare()` 时，Ulysses会自动设置：

```python
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)


model, optimizer, dataloader = accelerator.prepare(model, optimizer, dataloader)

```

`prepare()` 调用会：

1. 使用DeepSpeed的 `UlyssesSPAttentionHF` 注册模型
2. 用 `UlyssesSPDataLoaderAdapter` 包装数据加载器以处理序列分片
3. 自动注入 `shift_labels` 以进行正确的损失计算

### 损失聚合

使用Ulysses时，每个GPU在序列的不同部分计算损失。必须根据每个秩的有效Token数量对损失进行加权聚合。如果你使用Transformers的 `Trainer` 或TRL的 `SFTTrainer`，这会自动处理——下面的代码仅在编写自定义的Accelerate训练循环时才需要：

```python
sp_size = parallelism_config.sp_size
if sp_size > 1:
    from deepspeed.utils import groups

    sp_group = groups._get_sequence_parallel_group()

    
    losses_per_rank = torch.distributed.nn.functional.all_gather(loss, group=sp_group)
    good_tokens = (batch["shift_labels"] != -100).view(-1).sum()
    good_tokens_per_rank = torch.distributed.nn.functional.all_gather(good_tokens, group=sp_group)

    
    total_loss = sum(
        losses_per_rank[i] * good_tokens_per_rank[i]
        for i in range(sp_size)
        if good_tokens_per_rank[i] > 0
    )
    loss = total_loss / max(sum(good_tokens_per_rank), 1)

accelerator.backward(loss)

```

加权损失聚合确保了当Token在各并行秩上分布不均时（例如，某些秩仅包含填充或被掩码的提示词Token），梯度计算依然正确。

Ulysses和Ring Attention在训练期间都使用`position_ids`而非`attention_mask`进行因果掩码。在这些序列长度下，一个4D的注意力掩码张量将和注意力分数张量本身一样庞大且难以处理——对于128k个Token，这又是另一个约1TB的张量。使用位置ID可以在实现相同因果行为的同时，将内存占用从O(n^2)降低到O(n)。在评估/推理阶段，DeepSpeed的SP注意力层可以完全绕过SP操作（通过`disable_in_eval`参数），并回退到模型默认的注意力实现。

## 与Transformers Trainer集成

Transformers的`Trainer`通过`TrainingArguments.parallelism_config`提供了无缝的Ulysses集成。它会自动处理所有SP相关的细节——数据加载器包装、序列分片和损失聚合——因此你无需编写任何如上所示的自定义损失代码。

只需将上面相同的`parallelism_config`传入`TrainingArguments`即可：

```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    parallelism_config=parallelism_config,  
    per_device_train_batch_size=1,
)

```

### Trainer自动处理的内容

1. 数据加载器包装：模型准备完成后，Trainer会用`UlyssesSPDataLoaderAdapter`包装数据加载器。
2. 损失计算：`compute_loss`方法会检测SP模式，并路由到专门的`_deepspeed_sp_compute_loss`函数，该函数负责：跨SP秩收集损失、计算每个秩的有效Token数量、进行加权损失聚合。
3. 批次大小计算：有效的并行数据世界大小会考虑SP的影响：`dp_world_size = world_size // sp_size`。
4. 数据加载器长度调整：训练步数的计算会根据SP对迭代次数的影响进行调整。

数据加载器包装：模型准备完成后，Trainer会用`UlyssesSPDataLoaderAdapter`包装数据加载器。

损失计算：`compute_loss`方法会检测SP模式，并路由到专门的`_deepspeed_sp_compute_loss`函数，该函数负责：
- 跨SP秩收集损失
- 计算每个秩的有效Token数量
- 进行加权损失聚合

批次大小计算：有效的并行数据世界大小会考虑SP的影响：

```python
dp_world_size = world_size // sp_size

```

数据加载器长度调整：训练步数的计算会根据SP对迭代次数的影响进行调整。

### 启动命令

使用accelerate配置文件或命令行参数：

```bash
accelerate launch \
    --config_file deepspeed_ulysses.yaml \
    train.py \
    --per_device_train_batch_size 1

```

## 与TRL SFTTrainer集成

TRL的`SFTTrainer`基于Transformers Trainer构建，并针对长序列的监督微调添加了特定的优化。

```python
from trl import SFTConfig, SFTTrainer
from accelerate.utils import ParallelismConfig, DeepSpeedSequenceParallelConfig

parallelism_config = ParallelismConfig(
    sp_backend="deepspeed",
    sp_size=2,
    dp_shard_size=2,  
    sp_handler=DeepSpeedSequenceParallelConfig(
        sp_seq_length_is_variable=True,
        sp_attn_implementation="flash_attention_2",
    ),
)

training_args = SFTConfig(
    ...,
    parallelism_config=parallelism_config,
    max_length=32768,
    pad_to_multiple_of=2,  
    per_device_train_batch_size=1,
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
)
trainer.train()

```

### Ulysses的关键SFTConfig参数

### Accelerate配置文件

创建`alst_ulysses_4gpu.yaml`：

```yaml
compute_environment: LOCAL_MACHINE
distributed_type: DEEPSPEED
mixed_precision: bf16
num_processes: 4
deepspeed_config:
  zero_stage: 3
  seq_parallel_communication_data_type: bf16
parallelism_config:
  parallelism_config_sp_size: 2
  parallelism_config_sp_backend: deepspeed
  parallelism_config_dp_shard_size: 2
  parallelism_config_sp_seq_length_is_variable: true
  parallelism_config_sp_attn_implementation: flash_attention_2

```

### 完整的训练命令

```bash
accelerate launch --config_file alst_ulysses_4gpu.yaml \
    trl/scripts/sft.py \
    --model_name_or_path meta-llama/Llama-3.1-8B \
    --dataset_name trl-lib/Capybara \
    --max_length 32768 \
    --packing \
    --pad_to_multiple_of 2 \
    --per_device_train_batch_size 1

```

### 标签偏移处理

当启用Ulysses时，SFTTrainer会自动处理预偏移的标签：

```python


labels = inputs["labels"] if "shift_labels" not in inputs else None


if "shift_labels" in inputs:
    shift_logits = outputs.logits.contiguous()
    shift_labels = inputs["shift_labels"]
else:
    shift_logits = outputs.logits[..., :-1, :].contiguous()
    shift_labels = labels[..., 1:].contiguous()

```

## Ulysses与Ring Attention对比

Ulysses和Ring Attention都支持长上下文训练，但它们具有不同的特点：

### 何时选择Ulysses vs Ring Attention

由于在两者之间切换只需要更改accelerate配置，我们建议在你的具体设置上尝试两者，并比较性能和内存使用情况。主要的限制是Ulysses要求`num_heads >= sp_size`，而Ring Attention没有这样的限制。

## 最佳实践

### 1. 序列长度可整除性

始终确保你的序列长度能被`sp_size`整除：

```python
training_args = SFTConfig(
    pad_to_multiple_of=4,  
    max_length=32768,  
)

```

### 2. 使用Flash Attention

Flash Attention 2比SDPA提供了更清晰的输出和更好的性能：

```python
parallelism_config = ParallelismConfig(
    sp_handler=DeepSpeedSequenceParallelConfig(
        sp_attn_implementation="flash_attention_2",
    ),
)

```

对于Hopper架构使用Flash Attention 3，并关注Blackwell架构的Flash Attention 4发布（FA2在Blackwell上相当慢）。

### 3. 与DeepSpeed ZeRO结合

对于非常大的模型，将Ulysses与ZeRO Stage 3结合使用：

```yaml
deepspeed_config:
  zero_stage: 3
  offload_optimizer:
    device: cpu

```

如果模型极其庞大，你还可以通过添加以下配置来卸载参数：

```yaml
  offload_param:
    device: cpu

```

### 5. 使用内存碎片友好的PyTorch分配器

这个环境变量将允许更长的序列长度：

```bash
export PYTORCH_ALLOC_CONF=expandable_segments:True

```

### 6. 2D并行配置

根据你的GPU数量平衡SP和DP：

记住：`dp_replicate_size × dp_shard_size × sp_size = num_processes`

### 7. Liger-Kernel

如果你所需的模型架构被`Liger-Kernel`支持，它完全兼容Ulysses SP，并且可以通过一个标志启用：

```python
training_args = SFTConfig(
    use_liger_kernel=True,
)

```

主要的内存节省来自`FusedLinearCrossEntropy`，它避免了在损失计算过程中物化完整的logits张量。随着序列变长、logits张量变大，节省的内存也越多。

此外，你可以启用`TiledMLP`来进一步扩展序列长度——与`FusedLinearCrossEntropy`类似，它通过平铺大型矩阵运算来节省工作内存。

### 8. Token在各秩间的分布

你无需担心手动平衡Token在SP各秩间的分布——损失聚合代码能够优雅地处理不均匀的分布（包括有效Token数为零的秩）。在合理大小的数据集上进行随机批次处理，Token分布在训练过程中会达到统计上的均衡。

## 基准测试

为了量化Ulysses SP的优势，我们使用TRL的SFTTrainer在`Gutenberg English`流式数据集上训练了`Qwen3-4B`。所有实验均在H100 80GB GPU上运行，使用了DeepSpeed ZeRO-3、CPU优化器卸载、梯度检查点以及flash-attn2作为注意力后端。

### 实验设置

上表中运行的基准测试使用相同的全局批次大小（8个微批次）、余弦学习率调度和随机种子，因此这些基准测试的损失曲线可直接比较。

### 损失曲线匹配诊断（4 GPU）

为了验证序列并行与数据并行的损失等价性，我们进行了受控的4-GPU A/B实验，使用相同的随机种子、模型、优化器、学习率调度和数据顺序。

#### 公平比较数据并行与序列并行的方法

比较的设置：

- DP=4, SP=1, GAS=1（基线）
- DP=1, SP=4, GAS=4（Ulysses 序列并行）

为了公平比较，`GAS`必须随`SP`缩放：

- Ulysses 序列并行将序列在`SP`个进程间分割，因此每个序列并行进程在每个微步中看到大约`1/SP`的序列Token。
- 如果`GAS`保持不变，序列并行中的每个优化器步聚合的总Token数将少于数据并行基线。
- 设置`GAS=SP`可以保持每个优化器步的有效Token数匹配：
    - DP tokens/step: `dp_world_size * micro_batch * seq_len * GAS = 4 * B * L * 1`
    - SP tokens/step: `dp_world_size * micro_batch * (L/SP) * GAS * SP_ranks = 1 * B * (L/4) * 4 * 4 = 4 * B * L`

![在Gutenberg文本上（20步），`DP=4,SP=1,GAS=1`与`DP=1,SP=4,GAS=4`之间的规范损失在日志精度内匹配。](/images/posts/346c264d27b9.png)

在受控等价性框架下，在4个GPU上测量20步的结果：

结论：在匹配的Token预算下，序列并行和非序列并行在规范化的Token损失上匹配。剩余的差异在于训练器报告的日志（损失），而非底层的交叉熵目标。

### 内存减少

![在相同序列长度下，`SP=4`将每GPU内存减少3.3倍，使得在4× H100 80GB上训练高达96K Token成为可能。在128K时，模型出现内存不足。](/images/posts/8f23386ea55c.png)

在8K Token时，`DP=4`和`SP=4`使用的每GPU内存几乎相同（使用ZeRO-3时约22 GB）。序列并行的优势在于它能够扩展到更长的序列：在96K Token（长12倍）时，峰值内存为66 GB——仍在H100的80 GB容量内。在128K时，模型出现内存不足，这确定了此配置的实际限制。对于此模型，没有序列并行的`DP=4`无法扩展到超过8K。

### 吞吐量

![使用序列并行处理更长的序列，每秒处理的Token数量大幅增加。`SP=4`在64K时实现了基线吞吐量的3.7倍。](/images/posts/b02bbcb134f0.png)

在相同序列长度（8K）下，`SP=4`的吞吐量与单GPU基线相当——在NVLink连接的GPU上，全对全通信开销很小。真正的优势来自更长的序列：随着序列长度增长，二次方的注意力计算主导了通信和其他开销，使得每个训练步的计算效率越来越高。每个步处理的Token数量也成比例增加，因此吞吐量随序列长度扩展。在64K时，`SP=4`每秒处理13,396个Token——是基线的3.7倍。

这些结果仅使用了4个GPU和`SP=4`。使用8个GPU（`SP=8`），可以推向更长的序列——高达256K+ Token——或者使用2D并行（`SP=4, DP=2`）来结合长上下文训练与数据并行吞吐量。

## 要求

- HF Accelerate: `deepspeed>=0.18.1 accelerate>=1.12`
- HF Trainer: `deepspeed>=0.18.1 accelerate>=1.12 transformers>=5.0`
- HF TRL: `deepspeed>=0.18.1 accelerate>=1.12 transformers>=5.0 trl>=0.18.0`

对于Ampere GPU使用`flash_attention_2`，对于Hopper GPU使用`flash_attention_3`。等待Blackwell上的`flash_attention_4` 🕰。

## 资源

### 文档

- Accelerate: 上下文并行指南
- TRL: 分布式训练
- DeepSpeed 序列并行

### 示例

- Accelerate ALST 示例
- TRL Accelerate 配置

### 论文

- Arctic Long Sequence Training: 可扩展且高效的多百万Token序列训练
- DeepSpeed Ulysses: 实现极端长序列Transformer模型训练的系统优化

---

> 本文由AI自动翻译，原文链接：[Ulysses Sequence Parallelism: Training with Million-Token Contexts](https://huggingface.co/blog/ulysses-sp)
> 
> 翻译时间：2026-03-10 04:42
