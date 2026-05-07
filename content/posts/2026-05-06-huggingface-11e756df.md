---
title: vLLM V0到V1迁移：先修复正确性再优化RL目标
title_original: 'vLLM V0 to V1: Correctness Before Corrections in RL'
date: '2026-05-06'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ServiceNow-AI/correctness-before-corrections
author: ''
summary: 文章介绍了将vLLM推理引擎从V0迁移到V1时，在强化学习（RL）训练中遇到的训练-推理不匹配问题。作者发现，V1默认返回原始logprobs而非采样器使用的已处理分布，且存在运行时默认值差异、权重更新路径和fp32精度问题。通过修复这四个问题（启用processed_logprobs、调整默认值、修正权重更新路径、使用fp32
  lm_head），V1最终在裁剪率、KL散度、熵和奖励等指标上与V0参考实现匹配。文章强调在改变RL目标前应先确保后端行为一致。
categories:
- AI基础设施
tags:
- vLLM
- 强化学习
- 推理引擎
- 训练-推理不匹配
- RL训练
draft: false
translated_at: '2026-05-07T05:31:11.214694'
---

# vLLM V0 到 V1：在RL中先修正正确性再修正目标

PipelineRL 使用 vLLM 作为推理引擎进行 rollout 生成。推理引擎采样 Token 并返回 Token 的 logprobs；训练器使用这些 logprobs 计算策略比率、KL 散度、裁剪率、熵和奖励。这些 logprobs 计算方式上的任何差异都会改变训练动态。这就是我们在 vLLM V0 到 V1 迁移过程中需要消除的训练-推理不匹配问题。

简而言之。在我们修复了四个问题后，vLLM V1 与我们的 vLLM V0 参考实现匹配：处理后的 rollout logprobs、V1 特定的运行时默认值、运行中权重更新路径，以及用于最终投影的 fp32 lm_head。我们在改变 RL 目标之前修复了后端行为。

参考运行使用 vLLM 0.8.5；V1 运行使用 vLLM 0.18.1。图 1 显示了最终结果。红色曲线是初始的 V1 尝试，绿色曲线是经过下述修复后的最终 V1 运行。

![图 1. vLLM V0 参考（蓝色）、初始 vLLM V1 尝试（红色）以及修复后（包括 fp32 lm_head）的最终 vLLM V1 运行（绿色）的训练器端指标。最终 V1 运行在裁剪率、KL 散度、熵和奖励方面接近 V0 轨迹。](/images/posts/397aaa7a283e.png)

## 迁移目标

vLLM V1 是对 V0 引擎的重大重写。因此我们的迁移目标刻意保持狭窄：

1. 验证 V1 以训练器期望的形式返回 rollout logprobs
2. 针对 V0 参考重新运行相同的工作负载
3. 仅在恢复后端一致性后评估目标层面的变化

最初出现的可见症状包括：

- clamp_log_ratio_new_old_indicator
- kl_new_old
- 熵
- 奖励

这些指标来自 GSPO 训练运行，即本次实验使用的目标。同一类不匹配问题也可能出现在 PPO、GRPO 或任何将 rollout 端 logprobs 视为优化目标一部分的在线 RL 系统中。

初始的 V1 运行清晰地显示了问题。训练器端的 logprobs 和奖励在训练早期就偏离了 V0 参考。

![图 2. 训练器在更新期间计算的当前策略 logprobs（左）和奖励（右）。初始的 vLLM V1 运行（红色）与 vLLM V0 参考（蓝色）分离。](/images/posts/4f407e0c105a.png)

同样的模式也出现在训练器指标中。在初始比较中，裁剪率是最容易读取的信号。

![图 3. vLLM V0 参考（蓝色）和初始 vLLM V1 尝试（红色）的训练器端指标。裁剪率反映了 rollout/训练器策略差距；熵和奖励显示了该差距如何传播到训练中。](/images/posts/044a6c936067.png)

## 故障模式

我们将可能的原因分为三个层面：

1. 语义不匹配：后端返回的 logprobs 含义与训练器期望的不同。
2. 推理路径不匹配：后端在缓存、调度或请求处理方面使用不同的运行时默认值，因此相同的提示词遵循不同的执行路径。
3. 目标不匹配：RL 目标需要针对残留的陈旧度或后端不匹配进行修正。

我们最初过早地怀疑了第三类。有用的诊断来自于将前两类视为后端行为问题并首先排除它们。

## V1 后端修复

### Logprob 语义

第一个问题是语义问题。vLLM V1 默认从原始模型输出返回 logprobs，即在 logits 后处理（如温度缩放、惩罚和 top-k/top-p 过滤）之前。PipelineRL 期望的是采样器使用的已处理分布中的 logprobs。

所需的设置是：

- logprobs-mode=processed_logprobs

这消除了 rollout logprobs 中明显的均值偏移。训练曲线仍然显示出与已知良好参考的差距，因此下一个问题一定出在推理路径中。

策略比率图直接显示了这一点。一旦为 V1 启用了 processed_logprobs，所有三次运行的平均策略比率都紧密地保持在 1.0 附近。这确立了均值偏差的修复。剩余的差异体现在裁剪率、KL 散度、熵和下游训练行为中。

![图 4. vLLM V0 参考（蓝色）、初始 vLLM V1 运行（红色）和修正后的 vLLM V1 运行（绿色）的 rollout/训练器策略比率与 1.0 的每步偏差，缩放因子为 10,000。](/images/posts/6c104dc1129f.png)

### 运行时默认值

早期的 V1 运行混合了引擎版本与 V1 运行时默认值：

- 前缀缓存，在早期运行中未设置，因此应用了 vLLM 0.18.1 的默认值
- 异步调度，在早期运行中未设置，因此应用了 vLLM 0.18.1 的默认值
- 一个临时的 disable-cascade-attn 覆盖，通过启动时的 kwarg 传递设置，且不在已提交配置的一致性配方中

对于一致性运行，我们明确做出了这些选择：

```yaml
vllm_config:
  use_v1: true
  vllm_kwargs:
    logprobs-mode: processed_logprobs
    enable-prefix-caching: false
    async-scheduling: false

```

前缀缓存值得单独说明。对于固定的模型状态，它通常是一种保持正确性的推理优化。在此在线 RL 设置中，它是 V1 相对于 V0 参考路径在缓存生命周期和重用方面的唯一差异。Actor 还需要处理重复前缀、并发请求、异步调度和运行中权重更新。

当缓存策略忽略权重更新边界时，前缀缓存命中可以重用权重更新前计算的状态。禁用前缀缓存从一致性比较中移除了一个 V1 独有的自由度。

### 运行中权重更新

权重同步也必须匹配在线 RL 更新模型。一种选择是让 V1 比 V0 更严格，在每次更新时排空请求并清除缓存。这将回答另一个问题。我们首先需要验证 V1 能够匹配现有的 V0 行为。

V0 实际所做的更接近于：

- 在引擎边界阻塞执行
- 加载新权重
- 恢复执行，而不显式使缓存状态失效

最接近的 V1 模拟是：

```python
await engine.pause_generation(mode="keep", clear_cache=False)
await engine_client.collective_rpc_async(
    "receive_weight_update",
    args=(request.model_dump_json(),),
)
await engine.resume_generation()

```

两个细节很重要：

- mode="keep" 比 wait 或 abort 更接近旧的运行中更新模型
- clear_cache=False 匹配 V0 封装器的行为，该封装器在更新时保持缓存状态不变

延迟是一个有用的运行时诊断指标。初始的 V1 路径在训练后期比修正后的 V1 运行携带更多的持久延迟。

![图 5. rollout 服务器中的权重落后于训练器策略的步数，针对 vLLM V0 参考（蓝色）、初始 vLLM V1 运行（红色）和修正后的 vLLM V1 运行（绿色）。](/images/posts/b1b2a36056a2.png)

## 剩余的差距：fp32 lm_head

上述 V1 后端修复消除了明显的迁移问题，但最终的一致性仍然需要匹配用于计算 logits 的数值路径。训练器使用 fp32 lm_head 进行最终投影。rollout 后端必须匹配该行为。

MiniMax-M1 技术报告中出现了一个密切相关的问题：他们的 RL 运行显示了一个训练/推理 Token 概率不匹配，他们追溯到 LM 输出头，并通过在 fp32 中计算该头来修复。

这很重要，因为 RL 更新直接消耗 Token logprobs。logits 的微小变化可能在策略比率、KL 散度和裁剪中变得可见。因此，最终投影精度是在线 RL 正确性的一部分。后来的 ScaleRL 论文将 fp32 logits/头计算作为其 RL 配方的一部分，并将其作为大规模 RL 的有用设计选择进行了消融实验。

包含 fp32 lm_head 路径后，奖励给出了最终一致性结果的简洁视图。在图 6 中，最终的 V1 运行跟踪了 V0 参考；初始的 V1 尝试产生了明显不同的奖励曲线。

![图6. vLLM V0参考（蓝色）、初始vLLM V1尝试（红色）以及最终采用fp32_lm_head路径的vLLM V1运行（绿色）的奖励值。加入fp32头后，最终的V1运行与V0参考保持一致。](/images/posts/4612768e0ce2.png)

## 消融实验

负面结果之所以重要，是因为它们排除了常见的解释。

- 仅处理对数概率：修复了语义对数概率的bug；但训练不匹配问题依然存在。
- 批次不变性：在另一个测试中，不匹配问题依然存在，且伴随更高的延迟、更高的裁剪率以及NCCL的复杂情况。
- 将首次V1运行视为公平基线：首次V1运行启用了多个仅V1才有的默认设置，因此这是一次混杂的迁移对比。

## 我们为何优先修复后端正确性

目标侧修正方法，如截断重要性采样、重要性比率重新加权及相关技术，都是有用的工具。如果rollout数据有意过时、异步生成，或由无法保证与训练器侧策略等效的后端产生，那么添加某种形式的修正通常是正确的做法。

这里首要的问题是推理正确性。迁移到V1后，rollout后端返回的对数概率和运行时行为打破了训练器的假设。此时添加目标侧修正会混淆两个问题：

- 推理后端是否生成了正确的对数概率？
- 在给定正确对数概率的情况下，目标函数是否仍需要离策略或异步修正？

这两个问题需要分开处理。否则，目标侧修正可能会掩盖推理后端的错误行为，从而使训练曲线更难解读。

当前的目标函数仍有改进空间。在推理一致性恢复后，下一步的改进是常规的异步/离策略清理：

- 保留rollout时显式的行为策略对数概率
- 在优化时重新计算训练器侧的旧策略对数概率
- 将后端不匹配修正与策略更新比率分离
- 跟踪修正项的ESS等诊断指标，与聚合训练器指标一同监控

这次迁移的主要教训更为具体：先修复后端正确性，再对剩余的不匹配问题添加修正。

---

> 本文由AI自动翻译，原文链接：[vLLM V0 to V1: Correctness Before Corrections in RL](https://huggingface.co/blog/ServiceNow-AI/correctness-before-corrections)
> 
> 翻译时间：2026-05-07 05:31
