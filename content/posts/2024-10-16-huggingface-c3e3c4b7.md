---
title: 修复梯度累积：Transformers训练器损失计算问题
title_original: Fixing Gradient Accumulation
date: '2024-10-16'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/gradient_accumulation
author: ''
summary: 文章指出Transformers训练器在梯度累积时存在损失计算错误，导致与全批量训练结果不匹配。问题根源在于默认损失函数对跨Token级任务（如因果LM）的损失计算方式不当，正确做法应基于所有批次非填充Token总数进行归一化。Hugging
  Face团队通过两种方式修复：自动调整默认损失函数，并开放API允许用户传入自定义损失函数。相关修复已提交PR，并计划推广至更多模型。
categories:
- AI基础设施
tags:
- 梯度累积
- Transformers
- 损失函数
- Hugging Face
- 训练优化
draft: false
translated_at: '2026-06-18T06:53:05.963505'
---

# 修复梯度累积

我们的朋友Unsloth昨天分享了一个关于梯度累积的问题，该问题影响了transformers Trainer。最初的报告来自@bnjmn_marie（向他致敬！）。

梯度累积在数学上应该等同于全批量训练；然而，在开启和关闭该设置的训练运行之间，损失值并不匹配。

## 问题根源在哪里？

在每个模型的建模代码内部，transformers提供了一个"默认"损失函数，该函数是模型任务最常用的损失函数。它由建模类的用途决定：问答、Token分类、因果LM、掩码LM。

这是默认的损失函数，并非设计为可自定义：只有当`labels`和`input_ids`作为输入传递给模型时才会计算，因此用户无需自行计算损失。默认损失函数很有用，但在设计上存在局限性：对于任何不同的操作，我们期望不直接传递标签，而是让用户从模型获取logits并在模型外部使用它们来计算损失。

然而，transformers Trainer以及许多Trainer都大量利用这些方法，因为它们提供了简便性：这是一把双刃剑。提供一个简单的API，但随着用例不同而发生变化，这并不是一个经过深思熟虑的API，我们自己也感到意外。

准确地说，对于跨Token级任务（如因果LM训练）的梯度累积，正确的损失应通过梯度累积步骤中所有批次的总体损失除以这些批次中所有非填充Token的总数来计算。这与每批次损失值的平均值不同。

修复方法非常简单，请参见以下内容：

```diff
def ForCausalLMLoss(logits, labels, vocab_size, **kwargs):
    # 转换为浮点数以避免潜在精度问题
    logits = logits.float()
    # 移位，使tokens < n预测n
    shift_logits = logits[..., :-1, :].contiguous()
    shift_labels = labels[..., 1:].contiguous()

    # 展平Token
    shift_logits = shift_logits.view(-1, vocab_size)
    shift_labels = shift_labels.view(-1)
    # 启用模型并行
    shift_labels = shift_labels.to(shift_logits.device)

    num_items = kwargs.pop("num_items", None)
+        loss = nn.functional.cross_entropy(shift_logits, shift_labels, ignore_index=-100, reduction="sum")
+        loss = loss / num_items
-        loss = nn.functional.cross_entropy(shift_logits, shift_labels, ignore_index=-100)
    return loss

```

## 我们如何修复

为了解决这个问题，我们正在通过两种方式改变模型和训练的工作方式：

- 如果用户使用"默认"损失函数，在使用梯度累积时，我们将自动考虑所需的更改，以确保报告和使用正确的损失，从而解决核心问题。
- 为确保未来任何计算损失的问题不会阻碍用户，我们将开放一个API，允许用户直接向Trainer传入自己的损失函数，这样他们可以在我们内部修复问题并发布新的transformers版本之前，轻松使用自己的修复方案。

所有继承自`PreTrainedModel`的模型现在都有一个`loss_function`属性，该属性由以下任一方式确定：

- `config.loss_type`：这是为了确保任何人都可以使用自定义损失。您可以通过修改`LOSS_MAPPING`来实现：

```python
def my_super_loss(logits, labels):
    return loss = nn.functional.cross_entropy(logits, labels, ignore_index=-100)

LOSS_MAPPING["my_loss_type"] = my_super_loss

```

我们正在此PR中为最流行的模型推出第一个更改：https://github.com/huggingface/transformers/pull/34191#pullrequestreview-2372725010。随后，将发布贡献请求，以帮助将这一更改推广到其余模型，以便在下一个版本中支持大多数模型。

我们还在积极推动此PR中的第二个更改：https://github.com/huggingface/transformers/pull/34198，该更改将允许用户使用自己的损失函数，并利用每批次看到的样本数量来帮助计算损失（随着前一个更改支持更多模型，将在梯度累积期间执行正确的损失计算）。

到明天，您应该可以期待Trainer在梯度累积下正确运行。请从`main`安装以受益于该修复：

```
pip install git+https://github.com/huggingface/transformers

```

总的来说，我们对提交到问题跟踪器的错误报告响应非常迅速：https://github.com/huggingface/transformers/issues

这个问题在Transformers中存在已有一段时间，因为它主要是一个应由最终用户更新的默认设置；然而，当默认设置变得不直观时，它们必然会被更改。在这种情况下，我们在不到24小时内更新了代码并发布了修复，这正是我们针对Transformers中此类问题的目标。如果您有问题，请提交您的问题；这是让Transformers改进并更好地适应您不同用例的唯一途径。

Transformers团队 🤗

---

> 本文由AI自动翻译，原文链接：[Fixing Gradient Accumulation](https://huggingface.co/blog/gradient_accumulation)
> 
> 翻译时间：2026-06-18 06:53
