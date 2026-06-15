---
title: Outlines-core 0.1.0发布：Rust与Python结构化生成
title_original: 'Releasing Outlines-core 0.1.0: structured generation in Rust and
  Python'
date: '2024-10-22'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/outlines-core
author: ''
summary: dottxt与Hugging Face合作发布了outlines-core 0.1.0，这是结构化生成核心算法的Rust移植版本。该版本为LLM输出提供可靠的结构化约束，支持JSON、Pydantic模型、正则表达式等格式。主要优势包括：索引编译速度提升约2倍、关注点分离便于集成到其他库、以及用Rust实现带来的可移植性。文章还介绍了结构化生成的工作原理、重要性及应用场景，并解释了用Rust重写的原因——速度、安全性和可靠性。
categories:
- AI基础设施
tags:
- 结构化生成
- Rust
- Python
- LLM
- 开源工具
draft: false
translated_at: '2026-06-15T07:19:44.346564'
---

# 发布 Outlines-core 0.1.0：Rust 和 Python 中的结构化生成

dottxt 和 Hugging Face 很高兴地宣布，我们一直在合作开发 outlines-core，这是 outlines 结构化生成核心算法的 Rust 移植版本。除了通过 outlines 从 LLM 获得可靠输出之外，这个 Rust 移植版本还为 outlines 用户提供了以下几个额外优势：

- **速度**：用户可以看到索引编译速度提升约 2 倍。
- **关注点分离**：现在更容易将结构化生成集成到其他库中。outlines-core 非常轻量。
- **可移植性**：用 Rust 实现核心算法使得可以为 Python 以外的语言创建绑定。

这些改进不仅应该提升现有 outlines 用户的性能，还应该大幅增加用户将结构化生成集成到其 LLM 工作流中的方式。outlines-core 现已公开，已集成到 outlines 中，并且 Python 绑定的 0.1.0 版本已发布。您可以在此处找到仓库。

## 结构化生成快速入门 🧑‍🎓

### 工作原理

结构化生成意味着您的 LLM 保证遵循所需的格式。这可以是 JSON、Pydantic 模型、正则表达式或上下文无关文法。关键在于结构化生成禁止生成"错误"的 Token。

让我们举一个非常简单的例子。LLM 应该生成一个布尔值，"true"或"false"。仅此而已。为了便于说明，假设 LLM 生成字符而不是 Token。因此第一个字符是 `"`，我们可以直接跳过前向传播。对于第二个字符，我们不需要从所有可能的字符中采样。LLM 只需在 `t` 或 `f` 之间选择。

![](/images/posts/4c26538a70e4.png)

之后，无论我们走哪条路径，都只有一个有效的下一个字符。如果 LLM 选择了 `t` 作为第一个字符，那么它必须跟随 `r`、`u` 和 `e`。类似地，如果它选择了 `f`，则跟随 `a`、`l`、`s`、`e`。并且无论走哪条路径，都会选择最后一个 `"` 作为最终字符。当然，背后还有更多内容，如需深入了解，我们推荐这篇 dottxt 博客和 arXiv 上的相关论文。

### 为什么重要

结构化生成的强大之处可能并不立即显而易见。许多人首先想到的用例是"太好了，现在我的 LLM 可以返回有效的 JSON，这样我就可以将其视为 API 并可靠地序列化/反序列化 JSON"。但这只是冰山一角。仔细想想，结构无处不在，甚至在您最意想不到的地方，比如 GSM8K 基准测试。

以下是结构化生成所实现的几个示例：

- 生成合成数据（也有与 Distilabel 的集成）
- 从文档和图像中提取信息
- 函数调用/构建 Agent（智能体）
- 思维链
- 确保您的 LLM 输出有效的井字棋棋盘
- 甚至生成虚拟世界！

而且，也许更令人惊讶的是，它降低了对所用特定提示词和样本数量的评估敏感性。除了结构带来的惊人技巧外，它的性能也更高。dottxt 博客有许多包含性能基准测试的好文章。

## 为什么用 Rust 重写？🦀

### 速度

当您听到"用 Rust 重写"时，可能首先想到的是性能。是的，outlines-core 也是如此。几个关键部分尚未迁移到 Rust，尽管如此，我们已经看到编译速度平均提升了 2 倍。

在 Rust 移植之前，Outlines 使用 Numba 来加速索引构建。虽然 Numba 很快（运行时性能与 Rust 相当），但 Numba 函数的 JIT 编译在首次运行时增加了延迟，这让许多用户感到沮丧。使用 Rust 意味着我们可以提前编译索引构建函数，在首次运行时不会增加任何延迟。虽然这在生产环境中并不重要（因为首次运行无论如何都可以作为部署的一部分完成），但在实验阶段它可以产生巨大差异！

### 安全性和可靠性

用 Rust 重写 Outlines 的主要原因之一是 Rust 带来的对安全性和可靠性的重视。Rust 强大的静态类型结合 Rust 的所有权模型，消除了整类错误，例如空指针解引用和并发代码中的数据竞争。这带来了更健壮、更安全的软件。

在 Outlines 的上下文中，安全性至关重要。结构化生成通常涉及复杂的数据结构和操作，尤其是在处理高性能推理引擎时。通过利用 Rust 的安全性保证，我们降低了因内存管理不当而导致的运行时错误和未定义行为的风险。

此外，Rust 的编译时检查鼓励开发人员编写更清晰、更易于维护的代码。这既改进了当前的代码库，也使未来的开发更高效。新贡献者可以更快地上手，代码也更容易审计和验证其正确性。

### 关注点分离

Outlines 的设计目标不仅仅是提供结构化生成的核心算法。除此之外，它还包含与其他库（如 transformers）的集成，这意味着该库包含许多依赖项。将核心算法与 Outlines 库分离意味着其他希望包含结构化生成的库可以通过导入一个非常轻量的库来实现。因此，我们可以设想在不久的将来，像 transformers 和 llama-cpp-python 这样的库将直接集成结构化生成。这使得 dottxt 团队能够专注于核心算法。

### 可移植性

大多数 LLM 训练是用 Python 编写的，但推理略有不同。它发生在许多不同的设备上、专用服务器上，并且使用多种编程语言编写。这就是可移植性对结构化生成也很重要的原因。通过用 Rust 编写 outlines 的核心功能，我们现在可以创建到其他语言的绑定。

例如，这个移植使得集成到 text-generation-inference 中更加顺畅。TGI 的服务器逻辑是用 Rust 编写的，我们希望尽可能避免调用 Python 代码。这也意味着像 mistral.rs 这样的库或使用 candle 实现的模型可以受益于 Outlines 的性能和能力。

未来，我们计划探索绑定到 JS/TS，使 outlines 能够在 transformers-js 中使用。或者可能是 Swift 绑定，使 outlines 能够在 Apple 设备上原生使用。但目前，重点将放在 Python 绑定上，并通过扩展对 JSON Schema 规范的支持，继续使 outlines-core 的功能集更加完整。

## 贡献

您喜欢处理结构化生成、解析器、让 LLM 只输出有效的 JSON 吗？给这个库加星，在 Twitter 上分享，加入并贡献！在 Twitter 上分享您的工作，并与 dottxt 和 Hugging Face 的社区互动。

---

> 本文由AI自动翻译，原文链接：[Releasing Outlines-core 0.1.0: structured generation in Rust and Python](https://huggingface.co/blog/outlines-core)
> 
> 翻译时间：2026-06-15 07:19
