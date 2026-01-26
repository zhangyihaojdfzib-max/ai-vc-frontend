---
title: Replicate利用Torch编译缓存，大幅提升模型推理启动速度
title_original: Torch compile caching for inference speed – Replicate blog
date: '2025-09-08'
source: Replicate Blog
source_url: https://replicate.com/blog/torch-compile-caching
author: ''
summary: 本文介绍了Replicate平台通过缓存`torch.compile`的编译产物，显著减少了PyTorch模型的冷启动时间。以FLUX系列模型为例，缓存后启动速度提升了50%-62%，从容器启动到首次预测成功的时间也得到改善。文章解释了`torch.compile`的工作原理及其带来的性能收益，并概述了缓存系统类似于CI/CD的工作流程，旨在帮助用户更高效地部署和运行AI模型。
categories:
- AI基础设施
tags:
- PyTorch
- 模型推理
- 性能优化
- 编译缓存
- AI部署
draft: false
translated_at: '2026-01-15T04:41:08.268813'
---

-   Replicate
-   Blog

# 用于提升推理速度的 Torch 编译缓存

-   nevillelyh
-   gandalfhz

我们现在缓存 `torch.compile` 的编译产物，以减少使用 PyTorch 的模型的启动时间。

像 `black-forest-labs/flux-kontext-dev`、`prunaai/flux-schnell` 和 `prunaai/flux.1-dev-lora` 这样的模型，现在启动速度快了 2-3 倍。

我们发布了一份关于如何使用 `torch.compile` 提升模型性能的指南，其中涵盖了更多细节。

## 什么是 torch.compile？

许多模型，特别是 FLUX 系列的模型，会应用各种 `torch.compile` 技术/技巧来提高推理速度。

首次调用编译后的函数时，会进行代码追踪和编译，这会增加开销。后续调用则运行优化后的代码，速度会显著加快。

在我们对 `black-forest-labs/flux-kontext-dev` 的推理速度测试中，编译版本比未编译版本运行速度快了 30% 以上。

## 性能提升

通过在模型容器生命周期之间缓存编译产物，我们观察到冷启动时间有了显著改善：

-   `black-forest-labs/flux-kontext-dev`: ~120s → ~60s (提速 50%)
-   `prunaai/flux-schnell`: ~150s → ~70s (提速 53%)
-   `prunaai/flux.1-dev-lora`: ~400s → ~150s (提速 62%)

对于所有使用 `torch.compile` 的模型，该缓存还改善了从容器启动到首次预测成功的时间。

![Torch Compile Cache Speedup](/images/posts/ba3f24311057.webp)

该缓存系统的工作方式类似于许多 CI/CD 缓存系统：

1.  当模型容器启动时，它会寻找缓存的编译产物
2.  如果找到，Torch 会复用它们，而不是从头开始重新编译
3.  当容器正常关闭时，它们会在需要时更新缓存
4.  缓存文件以模型版本为键，并存储在靠近 GPU 节点的位置

要了解更多关于如何使用 `torch.compile` 的信息，请查看我们自己的文档和官方的 PyTorch torch.compile 教程。


> 本文由AI自动翻译，原文链接：[Torch compile caching for inference speed – Replicate blog](https://replicate.com/blog/torch-compile-caching)
> 
> 翻译时间：2026-01-15 04:41
