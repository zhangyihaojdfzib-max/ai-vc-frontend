---
title: Hugging Face与谷歌云深化合作，共筑开放AI未来
title_original: Building for an Open Future - our new partnership with Google Cloud
date: '2025-11-13'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/google-cloud
author: null
summary: Hugging Face宣布与谷歌云建立全新战略合作，旨在为企业使用开放模型构建AI提供更佳平台。合作内容包括：为谷歌云客户优化模型下载体验，通过CDN网关加速访问；为Hugging
  Face客户带来谷歌云的性能、成本优势及安全技术；并推动TPU等硬件对开放模型的更好支持。双方致力于共同构建一个让每家公司都能在安全可控的基础设施上便捷使用开放模型的未来。
categories:
- AI基础设施
tags:
- Hugging Face
- 谷歌云
- 开放模型
- AI合作
- 模型部署
draft: false
translated_at: '2026-01-06T01:07:06.296Z'
---

构建开放未来——我们与谷歌云的全新合作伙伴关系

今天，我们很高兴宣布与谷歌云建立全新且更深入的合作关系，助力企业使用开放模型构建自己的AI。

"从开创性的Transformer到Gemma模型，谷歌为开放AI领域做出了许多最具影响力的贡献。我坚信未来所有企业都将构建并定制自己的AI。通过这项新的战略合作，我们让这一切在谷歌云上轻松实现。"Hugging Face的Jeff Boudier表示。

"Hugging Face一直是推动全球大小企业访问、使用和定制如今超过200万个开放模型的核心力量，我们很自豪已为社区贡献了超过1000个自有模型，"谷歌云产品管理高级总监Ryan J. Salva表示，"携手合作，我们将使谷歌云成为使用开放模型进行开发的最佳平台。"

**面向谷歌云客户的合作**

谷歌云客户在其众多领先的AI服务中使用来自Hugging Face的开放模型。在Vertex AI中，最受欢迎的开放模型只需在Model Garden中点击几下即可部署。希望对AI基础设施拥有更高控制权的客户，可以在GKE AI/ML中找到类似的模型库，或使用由Hugging Face维护的预配置环境。客户还可以通过Cloud Run GPU运行AI推理工作负载，实现无服务器开放模型部署。

共同的主线是：我们与谷歌云合作，构建无缝体验，充分利用每项服务的独特能力，为客户提供选择。

**开放模型网关——谷歌云客户的快速通道**

过去三年，谷歌云客户对Hugging Face的使用量增长了10倍，如今，这转化为每月数十PB的模型下载量和数十亿次请求。

为确保谷歌云客户在使用Hugging Face的模型和数据集进行构建时获得最佳体验，我们正携手合作，基于Hugging Face Xet优化存储与数据传输技术，以及谷歌云先进的存储和网络能力，为Hugging Face仓库创建一个CDN网关。

该CDN网关将直接在谷歌云上缓存Hugging Face的模型和数据集，从而显著缩短下载时间，并为谷歌云客户增强模型供应链的稳健性。无论您使用Vertex、GKE、Cloud Run，还是仅在Compute Engine的虚拟机中构建自己的技术栈，都将受益于更快的首次Token生成时间和简化的模型治理。

**面向Hugging Face客户的合作**

Hugging Face Inference Endpoints是只需点击几下即可从模型到部署的最简单方式。通过此次深化合作，我们将首先通过Inference Endpoints，为Hugging Face客户带来谷歌云独特的性能和成本优势。预计将有更多更新的实例可用，并且价格将有所下降！

我们将确保我们产品和工程协作的所有成果，都能轻松惠及Hugging Face上1000万AI构建者。从模型页面到部署在Vertex Model Garden或GKE上，应该只需几个步骤。安全托管在Hugging Face企业组织中的私有模型，其使用体验应如同使用公共模型一样简单。

TPU作为谷歌定制的AI加速器芯片，现已发展到第七代，其性能和软件栈成熟度持续提升。我们希望确保Hugging Face用户在使用开放模型构建AI时，能充分受益于当前及未来的TPU。得益于我们库中的原生支持，我们很高兴能让TPU像GPU一样易于用于Hugging Face模型。

此外，这项新的合作将使Hugging Face能够利用谷歌行业领先的安全技术，让Hugging Face上的数百万开放模型更加安全。借助VirusTotal、Google Threat Intelligence和Mandiant的支持，这项联合努力旨在保障您日常使用Hugging Face Hub时的模型、数据集和Spaces的安全性。

**共同构建AI的开放未来**

我们期待一个未来：每家公司都能使用开放模型构建自己的AI，并将其托管在自己安全可控的基础设施中。我们很高兴能与谷歌云共同实现这一未来。无论您使用Vertex AI Model Garden、Google Kubernetes Engine、Cloud Run还是Hugging Face Inference Endpoints，我们深入的合作都将加速这一愿景的实现。

您希望我们通过与谷歌的合作创造或改进什么？请在评论中告诉我们！


> 本文由AI自动翻译，原文链接：[Building for an Open Future - our new partnership with Google Cloud](https://huggingface.co/blog/google-cloud)
> 
> 翻译时间：2026-01-06 01:07
