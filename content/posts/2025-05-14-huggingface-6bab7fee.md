---
title: Kaggle与Hugging Face集成，优化模型访问体验
title_original: Improving Hugging Face Model Access for Kaggle Users
date: '2025-05-14'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/kaggle-integration
author: ''
summary: 本文宣布了Kaggle与Hugging Face平台的集成计划，旨在为AI开发者提供更便捷的模型访问体验。用户现可在两个平台间无缝跳转，直接在Kaggle
  Notebook中使用Hugging Face模型，并探索社区公开代码示例。文章详细介绍了集成功能的使用方法，包括对私有模型和许可受限模型的处理方式，并透露了未来将支持在Kaggle竞赛中离线使用Hugging
  Face模型的开发计划，强调了维护竞赛完整性的重要性。
categories:
- AI产品
tags:
- Kaggle
- Hugging Face
- 模型集成
- AI社区
- 机器学习平台
draft: false
translated_at: '2026-04-18T04:37:00.006940'
---

# 为Kaggle用户优化Hugging Face模型访问体验

Kaggle和Hugging Face用户同属一个AI社区。正因如此，我们非常高兴地宣布，我们计划让两个平台和社区更紧密地结合，以更好地服务全球AI开发者。

从今天开始，Kaggle将推出一项集成功能，直接在Kaggle平台上提升Hugging Face模型的可见性和可发现性。

## 如何开始使用

您可以在Hugging Face模型页面和Kaggle之间轻松跳转。首先访问一个Hugging Face模型页面，例如`Qwen/Qwen3-1.7B`。若要在Kaggle Notebook中使用该模型，您可以点击“使用此模型”并选择“Kaggle”，系统将自动打开一个Kaggle笔记本，其中预置了加载该模型的代码片段。您也可以在Kaggle上的Hugging Face模型页面通过点击“代码”按钮实现相同操作。

![在Kaggle上使用Hugging Face模型创建新笔记本](/images/posts/f455002e6f3d.gif)

当您在Kaggle上运行引用Hugging Face Hub托管模型的笔记本时，如果对应的Hugging Face模型页面尚不存在，我们将自动生成一个。您无需对代码进行任何特殊修改。此外，当您将笔记本公开后，它会自动显示在Kaggle模型页面的“代码”选项卡中。

您可以在Kaggle的`https://www.kaggle.com/models`一站式探索Hugging Face模型，并查看所有公开笔记本中的社区示例。随着更多Hugging Face模型在Kaggle上被使用，可供您探索和获取灵感的模型及相关代码示例数量将持续增长。

![在Kaggle上浏览Hugging Face模型](/images/posts/d1333f8a5c0a.gif)

在Kaggle浏览Hugging Face模型时，我们希望您能便捷地返回Hugging Face平台，以探索更多详细信息、元数据、Hugging Face Spaces中的社区使用案例、讨论等内容。只需在Kaggle模型页面点击“在Hugging Face中打开”即可。

## 私有模型和许可受限模型如何处理？

如果您在Kaggle笔记本中使用私有Hugging Face模型，请照常通过您的Hugging Face账户进行身份验证（在笔记本编辑器的“附加组件 > 密钥”菜单中添加您的HF_TOKEN）。Kaggle上不会生成对应的Hugging Face模型页面。

如果您想在Kaggle笔记本中访问许可受限模型，需要使用Hugging Face账户申请访问权限，并按照浏览器中Hugging Face模型页面的提示正常操作。Hugging Face提供了相关文档指导您完成此流程。除此之外，该集成功能的工作方式与非受限模型相同。

## 后续计划

我们正在积极开发一种解决方案，以便在需要离线提交笔记本的Kaggle竞赛中无缝使用Hugging Face模型。虽然这需要数月时间才能完成，但我们相信等待是值得的。

您可以阅读Kaggle关于“将AI竞赛作为GenAI评估实证严谨性的黄金标准”的立场文件，以理解我们为何必须确保这部分集成功能的正确性！简而言之——Kaggle对数据泄露及其对模型污染的影响高度敏感。我们的目标是设计此集成方案，在维护竞赛完整性及其在行业内重要作用的同时，让Kaggle参赛者能够无缝访问并使用Hugging Face的最佳模型进行构建！

我们非常期待在此期间听到您的反馈——请在此处分享您的想法和建议！

祝您在Kaggle探索愉快！

---

> 本文由AI自动翻译，原文链接：[Improving Hugging Face Model Access for Kaggle Users](https://huggingface.co/blog/kaggle-integration)
> 
> 翻译时间：2026-04-18 04:37
