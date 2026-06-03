---
title: PyTorch GPU内存可视化与优化指南
title_original: Visualize and understand GPU memory in PyTorch
date: '2024-12-24'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/train_memory
author: ''
summary: 本文详细介绍了如何在PyTorch中可视化GPU内存使用情况，通过实际代码示例和内存快照分析，解释了模型创建、前向传播、激活值保留等环节的内存变化规律。文章还涵盖了训练过程中的内存行为，帮助开发者理解内存瓶颈原因，并提供了估算和优化GPU内存的实用方法，适用于深度学习模型训练中的内存管理。
categories:
- AI基础设施
tags:
- PyTorch
- GPU内存
- 内存优化
- 深度学习训练
- 可视化工具
draft: false
translated_at: '2026-06-03T06:51:05.174078'
---

# 可视化并理解 PyTorch 中的 GPU 内存

你一定对这个消息很熟悉 🤬：

```log
RuntimeError: CUDA out of memory. Tried to allocate 20.00 MiB (GPU 0; 7.93 GiB total capacity; 6.00 GiB already allocated; 14.88 MiB free; 6.00 GiB reserved in total by PyTorch)

```

虽然很容易看出 GPU 内存已满，但理解其原因以及如何修复则更具挑战性。在本教程中，我们将逐步介绍如何在训练过程中可视化并理解 PyTorch 中的 GPU 内存使用情况。我们还将了解如何估算内存需求并优化 GPU 内存使用。

## 🔎 PyTorch 可视化工具

PyTorch 提供了一个方便的工具来可视化 GPU 内存使用情况：

```python
import torch
from torch import nn


torch.cuda.memory._record_memory_history(max_entries=100000)

model = nn.Linear(10_000, 50_000, device ="cuda")
for _ in range(3):
    inputs = torch.randn(5_000, 10_000, device="cuda")
    outputs = model(inputs)


torch.cuda.memory._dump_snapshot("profile.pkl")
torch.cuda.memory._record_memory_history(enabled=None)

```

运行这段代码会生成一个 `profile.pkl` 文件，其中包含执行期间 GPU 内存使用的历史记录。你可以在以下网址可视化该历史记录：https://pytorch.org/memory_viz。

通过拖放你的 `profile.pkl` 文件，你会看到如下图表：

让我们将这个图表分解为几个关键部分：

1. **模型创建**：内存增加 2 GB，对应模型大小：`10,000 × 50,000 个权重 + 50,000 个偏置，使用 float32（4 字节）⟹ (5 × 10⁸) × 4 字节 = 2 GB`。这部分内存（蓝色）在整个执行过程中保持不变。
2. **输入张量创建（第 1 次循环）**：内存增加 200 MB，对应输入张量大小：`5,000 × 10,000 个元素，使用 float32（4 字节）⟹ (5 × 10⁷) × 4 字节 = 0.2 GB`。
3. **前向传播（第 1 次循环）**：内存增加 1 GB，用于输出张量：`5,000 × 50,000 个元素，使用 float32（4 字节）⟹ (25 × 10⁷) × 4 字节 = 1 GB`。
4. **输入张量创建（第 2 次循环）**：内存增加 200 MB，用于新的输入张量。此时，你可能期望步骤 2 中的输入张量被释放。但事实并非如此：模型保留了其激活值，因此即使张量不再赋值给变量 `inputs`，它仍然被模型的前向传播计算所引用。模型保留其激活值是因为这些张量是神经网络反向传播过程所必需的。尝试使用 `torch.no_grad()` 来观察差异。
5. **前向传播（第 2 次循环）**：内存增加 1 GB，用于新的输出张量，计算方式同步骤 3。
6. **释放第 1 次循环激活值**：在第二次循环的前向传播之后，第一次循环中的输入张量（步骤 2）可以被释放。模型保存第一个输入张量的激活值被第二次循环的输入覆盖。一旦第二次循环完成，第一个张量不再被引用，其内存可以被释放。
7. **更新 output**：步骤 3 中的输出张量被重新赋值给变量 `output`。之前的张量不再被引用并被删除，释放其内存。
8. **输入张量创建（第 3 次循环）**：同步骤 4。
9. **前向传播（第 3 次循环）**：同步骤 5。
10. **释放第 2 次循环激活值**：步骤 4 中的输入张量被释放。
11. **再次更新 output**：步骤 5 中的输出张量被重新赋值给变量 `output`，释放之前的张量。
12. **代码执行结束**：所有内存被释放。

## 📊 训练过程中的内存可视化

前面的例子是简化版本。在真实场景中，我们通常训练复杂的模型，而不是单个线性层。此外，前面的例子没有包含训练过程。在这里，我们将研究一个真实的大语言模型（LLM）在完整训练循环中 GPU 内存的行为。

```python
import torch
from transformers import AutoModelForCausalLM


torch.cuda.memory._record_memory_history(max_entries=100000)

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B").to("cuda")
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

for _ in range(3):
    inputs = torch.randint(0, 100, (16, 256), device="cuda")  
    loss = torch.mean(model(inputs).logits)  
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()


torch.cuda.memory._dump_snapshot("profile.pkl")
torch.cuda.memory._record_memory_history(enabled=None)

```

💡 **提示**：在进行性能分析时，限制步数。每个 GPU 内存事件都会被记录，文件可能会变得非常大。例如，上述代码会生成一个 8 MB 的文件。

以下是此示例的内存分析图：

这个图表比之前的例子更复杂，但我们仍然可以逐步分解它。注意三个尖峰，每个对应训练循环的一次迭代。让我们简化图表以便更容易理解：

1. 模型初始化（`model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B").to("cuda")`）：第一步是将模型加载到 GPU 上。模型参数（蓝色部分）占用内存，并一直保留到训练结束。
2. 前向传播（`model(inputs)`）：在前向传播过程中，激活值（每层的中间输出）被计算并存储在内存中，用于反向传播。这些激活值（橙色部分）逐层增长，直到最后一层。损失函数在橙色区域的峰值处计算。
3. 反向传播（`loss.backward()`）：梯度（黄色部分）在此阶段被计算并存储。同时，激活值不再需要而被丢弃，导致橙色区域缩小。黄色区域表示梯度计算的内存占用。
4. 优化器步骤（`optimizer.step()`）：梯度用于更新模型参数。最初，优化器本身被初始化（绿色区域）。此初始化只进行一次。之后，优化器使用梯度更新模型参数。为了更新参数，优化器会临时存储中间值（红色区域）。更新完成后，梯度（黄色）和优化器中间值（红色）都会被丢弃，释放内存。

模型初始化（`model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B").to("cuda")`）：第一步是将模型加载到 GPU 上。模型参数（蓝色部分）占用内存，并一直保留到训练结束。

前向传播（`model(inputs)`）：在前向传播过程中，激活值（每层的中间输出）被计算并存储在内存中，用于反向传播。这些激活值（橙色部分）逐层增长，直到最后一层。损失函数在橙色区域的峰值处计算。

反向传播（`loss.backward()`）：梯度（黄色部分）在此阶段被计算并存储。同时，激活值不再需要而被丢弃，导致橙色区域缩小。黄色区域表示梯度计算的内存占用。

优化器步骤（`optimizer.step()`）：梯度用于更新模型参数。最初，优化器本身被初始化（绿色区域）。此初始化只进行一次。之后，优化器使用梯度更新模型参数。为了更新参数，优化器会临时存储中间值（红色区域）。更新完成后，梯度（黄色）和优化器中间值（红色）都会被丢弃，释放内存。

至此，一次训练迭代完成。该过程在剩余迭代中重复，产生图中可见的三个内存峰值。

像这样的训练配置文件通常遵循一致的模式，这使得它们对于估算给定模型和训练循环的 GPU 内存需求非常有用。

## 📐 估算内存需求

从上述部分来看，估算 GPU 内存需求似乎很简单。所需的总内存应对应于内存配置中的最高峰值，该峰值出现在前向传播期间。在这种情况下，内存需求为（蓝色 + 绿色 + 橙色）：模型参数 + 优化器状态 + 激活值

真有这么简单吗？实际上，这里有一个陷阱。根据训练设置的不同，配置文件可能看起来不同。例如，将批次大小从 16 减少到 2 会改变情况：

```diff
- inputs = torch.randint(0, 100, (16, 256), device="cuda")  # 虚拟输入
+ inputs = torch.randint(0, 100, (2, 256), device="cuda")  # 虚拟输入

```

现在，最高峰值出现在优化器步骤期间，而不是前向传播期间。在这种情况下，内存需求变为（蓝色 + 绿色 + 黄色 + 红色）：模型参数 + 优化器状态 + 梯度 + 优化器中间值

为了泛化内存估算，我们需要考虑所有可能的峰值，无论它们出现在前向传播期间还是优化器步骤期间。模型参数 + 优化器状态 + max(梯度 + 优化器中间值, 激活值)

现在我们有了公式，让我们看看如何估算每个组成部分。

### 模型参数

模型参数是最容易估算的。模型内存 = N × P

其中：
- N 是参数数量。
- P 是精度（以字节为单位，例如 float32 为 4）。

例如，一个具有 15 亿参数且精度为 4 字节的模型需要：

在上面的例子中，模型大小为：模型内存 = 1.5 × 10^9 × 4 字节 = 6 GB

### 优化器状态

优化器状态所需的内存取决于优化器类型和模型参数。例如，AdamW 优化器为每个参数存储两个动量（一阶和二阶）。这使得优化器状态大小为：优化器状态大小 = 2 × N × P

### 激活值

激活值所需的内存更难估算，因为它包括前向传播期间计算的所有中间值。为了计算激活值内存，我们可以使用前向钩子来测量输出的大小：

```python
import torch
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-1.5B").to("cuda")

activation_sizes = []

def forward_hook(module, input, output):
    """
    用于计算每个模块激活值大小的钩子。
    """
    if isinstance(output, torch.Tensor):
        activation_sizes.append(output.numel() * output.element_size())
    elif isinstance(output, (tuple, list)):
        for tensor in output:
            if isinstance(tensor, torch.Tensor):
                activation_sizes.append(tensor.numel() * tensor.element_size())


hooks = []
for submodule in model.modules():
    hooks.append(submodule.register_forward_hook(forward_hook))


dummy_input = torch.zeros((1, 1), dtype=torch.int64, device="cuda")
model.eval()  
with torch.no_grad():
    model(dummy_input)


for hook in hooks:
    hook.remove()

print(sum(activation_sizes))  

```

对于 Qwen2.5-1.5B 模型，每个输入 Token 产生 5,065,216 个激活值。要估算输入张量的总激活值内存，请使用：激活值内存 = A × B × L × P

- A 是每个 Token 的激活值数量。
- B 是批次大小。
- L 是序列长度。

然而，直接使用这种方法并不总是实用。理想情况下，我们希望有一个启发式方法来估算激活值内存，而无需运行模型。此外，我们可以直观地看到，更大的模型有更多的激活值。这引出了一个问题：模型参数数量与激活值数量之间是否存在联系？

并非直接相关，因为每个 Token 的激活值数量取决于模型架构。然而，LLM 往往具有相似的结构。通过分析不同的模型，我们观察到参数数量和激活值数量之间存在粗略的线性关系：

![激活值与参数](/images/posts/bd6d246486c8.png)

这种线性关系使我们能够使用启发式方法估算激活值：A = 4.6894 × 10^{-4} × N + 1.8494 × 10^{6}

尽管这是一种近似方法，但它提供了一种无需对每个模型进行复杂计算即可估算激活内存的实用方式。

### 梯度

梯度更容易估算。梯度所需的内存与模型参数相同：`Gradients Memory = N × P`

### 优化器中间值

在更新模型参数时，优化器会存储中间值。这些值所需的内存与模型参数相同：`Optimizer Intermediates Memory = N × P`

### 总内存

总结来说，训练模型所需的总内存为：`Total Memory = Model Memory + Optimizer State + max(Gradients, Optimizer Intermediates, Activations)`

其中包含以下组成部分：

- 模型内存：`N × P`
- 优化器状态：`2 × N × P`
- 梯度：`N × P`
- 优化器中间值：`N × P`
- 激活值：`A × B × L × P`，使用启发式方法估算：`A = 4.6894 × 10^{-4} × N + 1.8494 × 10^{6}`

为了让计算更简便，我为你创建了一个小工具：

## 🚀 下一步

你最初了解内存使用的动机，很可能是因为某天你遇到了内存不足的问题。这篇博客是否直接为你提供了解决方案？可能没有。不过，既然你现在对内存使用的工作原理以及如何对其进行分析有了更好的理解，你就更有能力找到减少内存使用的方法。

关于在TRL中优化内存使用的具体技巧列表，你可以查看文档中的`Reducing Memory Usage`部分。不过，这些技巧并不仅限于TRL，还可以应用于任何基于PyTorch的训练过程。

## 🤝 致谢

感谢Kashif Rasul对这篇博客提出的宝贵反馈和建议。

---

> 本文由AI自动翻译，原文链接：[Visualize and understand GPU memory in PyTorch](https://huggingface.co/blog/train_memory)
> 
> 翻译时间：2026-06-03 06:51
