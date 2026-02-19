---
title: Arm发布神经超级采样技术，AI驱动移动图形新突破
title_original: Neural Super Sampling is here!
date: '2025-08-12'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/Arm/neural-super-sampling
author: ''
summary: Arm正式发布其AI驱动的神经超级采样（NSS）技术，这是一款专为未来移动设备设计的实时超分辨率解决方案。NSS通过机器学习模型，能够以低分辨率渲染画面，并在毫秒级时间内超采样至高分辨率，从而显著降低GPU工作负载（演示中降低50%）。该技术针对移动GPU中的神经加速器进行了优化，适用于移动游戏和XR等功耗敏感场景。Arm同时提供了虚幻引擎插件、开发资源及训练数据集，助力开发者立即集成与体验。
categories:
- AI产品
tags:
- 神经渲染
- 超分辨率
- 移动GPU
- Arm
- 游戏开发
draft: false
translated_at: '2026-02-19T04:40:59.912373'
---

# 神经超级采样技术现已发布！

![image/png](/images/posts/2354c7b7411b.png)

Arm推出的新一代AI驱动超分辨率解决方案——神经超级采样（NSS）正式发布，图形与游戏开发者今日即可开始体验！

## 机器学习赋能升级

NSS专为搭载Arm神经技术的未来移动设备实时性能而设计。实际延迟取决于GPU配置、分辨率和具体用例等实施因素。在下方展示的《魔法城堡》演示视频中，NSS将GPU工作负载降低了50%。在持续性能配置下，该模型以540p分辨率渲染，并在4毫秒内超采样至1080p。

## 了解我们的NSS模型

神经超级采样（NSS）是Arm开发的实时时序超采样参数预测模型，针对移动GPU中神经加速器（NX）的执行进行了优化。它通过从低分辨率时序输入重建高质量输出帧，以更低计算成本实现高分辨率渲染。NSS特别适用于移动游戏、XR及其他功耗受限的图形应用场景。

立即开始使用我们的[NSS模型](https://example.com)。

若需深入探索，请查阅以下资源：

- 💻 技术博客：[神经超级采样工作原理](https://example.com)
- 📃 白皮书：[面向未来构建：通过虚幻插件与Vulkan ML扩展体验神经超级采样](https://example.com)
- 📲 技术博客：[NSS实验指南](https://example.com)

## 模型训练过程

欢迎查看[神经图形数据集](https://example.com)：该数据集包含参考图像、图像序列以及训练、验证和测试神经超级采样算法所需的对应运动、深度等数据。

![](/images/posts/2b988a59885c.jpg)

当前版本数据集包含用于神经超级采样的有限数据，以展示NSS模型开发流程。虽然此流程尚未提供完整模型（重新）训练所需的全面数据集，但请持续关注即将发布的[神经图形模型训练平台](https://example.com)，Arm将提供用于模型训练与再训练的内容捕获与转换工具。

## 立即开始体验NSS！

NSS已通过两款插件集成至虚幻引擎：[虚幻®引擎NSS插件](https://example.com)与[支持Vulkan ML扩展的虚幻® NNE插件](https://example.com)。

关于在虚幻®引擎中使用NSS的逐步指导，请参阅我们的学习路径：

- Vulkan® ML扩展快速入门：[Vulkan® ML扩展快速入门指南](https://example.com)
- 虚幻引擎快速入门：[神经超级采样快速入门指南](https://example.com)，了解如何将NSS集成至虚幻引擎

---

> 本文由AI自动翻译，原文链接：[Neural Super Sampling is here!](https://huggingface.co/blog/Arm/neural-super-sampling)
> 
> 翻译时间：2026-02-19 04:40
