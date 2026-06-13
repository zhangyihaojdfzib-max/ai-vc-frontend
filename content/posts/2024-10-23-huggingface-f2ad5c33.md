---
title: HUGS：零配置优化推理，加速开放模型部署
title_original: Introducing HUGS - Scale your AI with Open Models
date: '2024-10-23'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/hugs
author: ''
summary: Hugging Face 推出 HUGS（生成式 AI 服务），旨在简化和加速开放模型在自有基础设施上的部署。HUGS 基于 TGI 和 Transformers
  等开源技术构建，提供零配置、硬件优化的推理微服务，支持 NVIDIA、AMD GPU 及即将支持的 AWS Inferentia 和 Google TPU。它兼容
  OpenAI API，支持 Kubernetes 部署，并具备企业级合规性。早期用户反馈显示，HUGS 将部署时间从一周缩短至一小时，显著降低工程复杂性。
categories:
- AI产品
tags:
- HUGS
- 开放模型
- 推理优化
- 零配置部署
- 企业级AI
draft: false
translated_at: '2026-06-13T06:19:08.174429'
---

# 推出 HUGS——用开放模型扩展你的 AI

2025年9月更新：我们不再提供 HUGS 模型部署容器。

如需在您的基础设施中轻松部署优化的 Hugging Face 模型，请查看 Dell Enterprise Hub 和 Azure AI Foundry 中的 Hugging Face Collection。

今天，我们激动地宣布推出 Hugging Face 生成式 AI 服务，即 HUGS：经过优化、零配置的推理微服务，旨在简化和加速使用开放模型开发 AI 应用。HUGS 基于 Text Generation Inference 和 Transformers 等开源 Hugging Face 技术构建，是在您自己的基础设施中高效构建和扩展生成式 AI 应用的最佳解决方案。HUGS 经过优化，可在多种硬件加速器上运行开放模型，包括 NVIDIA GPU、AMD GPU，并将很快支持 AWS Inferentia 和 Google TPU。

## 面向开放模型的零配置优化推理

HUGS 简化了在您自己的基础设施和多种硬件上对开放模型进行优化部署的过程。开发者和组织面临的一个关键挑战是，在特定 GPU 或 AI 加速器上优化 LLM 推理工作负载的工程复杂性。借助 HUGS，我们能够以零配置的方式为最流行的开放 LLM 实现最大吞吐量部署。HUGS 提供的每种部署配置都经过全面测试和维护，开箱即用。

HUGS 模型部署提供与 OpenAI 兼容的 API，可无缝替换基于模型提供商 API 构建的现有生成式 AI 应用。只需将代码指向 HUGS 部署，即可使用托管在您自己基础设施中的开放模型为您的应用提供支持。

## 为什么选择 HUGS？

HUGS 提供了一种简单的方法，使用托管在您自己基础设施中的开放模型构建 AI 应用，具有以下优势：

- **在您的基础设施中**：在您自己的安全环境中部署开放模型。让您的数据和模型远离互联网！
- **零配置部署**：HUGS 通过零配置设置，将部署时间从数周缩短到几分钟，自动为您的 NVIDIA、AMD GPU 或 AI 加速器优化模型和服务配置。
- **硬件优化推理**：基于 Hugging Face 的 Text Generation Inference (TGI) 构建，HUGS 针对不同硬件配置进行了峰值性能优化。
- **硬件灵活性**：在多种加速器上运行 HUGS，包括 NVIDIA GPU、AMD GPU，并将很快支持 AWS Inferentia 和 Google TPU。
- **模型灵活性**：HUGS 兼容多种精选开源模型，确保您 AI 应用的灵活性和选择性。
- **行业标准 API**：使用 Kubernetes 轻松部署 HUGS，其端点与 OpenAI API 兼容，最大限度地减少代码更改。
- **企业级发行版**：HUGS 是 Hugging Face 开源技术的企业级发行版，提供长期支持、严格测试和 SOC2 合规性。
- **企业合规性**：通过包含必要的许可和服务条款，最大限度地降低合规风险。

我们向选定的 Enterprise Hub 客户提供了 HUGS 的早期访问权限：

> HUGS 极大地节省了本地部署即用型高性能模型的时间——在 HUGS 之前，这需要一周时间，现在我们可以在不到一小时内完成。对于有主权 AI 需求的客户来说，这是一个颠覆性的改变！——Henri Jouhaud，Polyconseil 首席技术官

> 我们尝试使用 HUGS 在 GCP 上使用 L4 GPU 部署 Gemma 2——我们无需摆弄库、版本和参数，它开箱即用。HUGS 让我们有信心扩展内部对开放模型的使用！——Ghislain Putois，Orange 研究工程师

## 工作原理

使用 HUGS 非常简单。以下是入门方法：

注意：根据您选择的部署方式，您需要访问相应的订阅或市场产品。

### 在哪里找到 HUGS

HUGS 可通过多个渠道获取：

1. **云服务提供商 (CSP) 市场**：您可以在 Amazon Web Services (AWS) 和 Google Cloud Platform (GCP) 上找到并部署 HUGS。Microsoft Azure 支持即将推出。
2. **DigitalOcean**：HUGS 原生集成在 DigitalOcean 中，作为一项新的 1-Click Models 服务提供，由 Hugging Face HUGS 和 GPU Droplets 提供支持。
3. **Enterprise Hub**：如果您的组织已升级到 Enterprise Hub，请联系我们的销售团队以获取 HUGS 访问权限。

有关每个平台的具体部署说明，请参阅上面链接的相关文档。

### 定价

HUGS 根据每个容器的运行时间提供按需定价，DigitalOcean 上的部署除外。

- **AWS Marketplace 和 Google Cloud Platform Marketplace**：每个容器每小时 1 美元，无最低费用（计算使用量由 CSP 单独计费）。在 AWS 上，您有 5 天免费试用期，可免费测试 HUGS。
- **DigitalOcean**：由 Hugging Face HUGS 提供支持的 1-Click Models 在 DigitalOcean 上免费提供——需支付常规 GPU Droplets 计算费用。
- **Enterprise Hub**：我们为 Enterprise Hub 组织提供自定义 HUGS 访问权限。请联系我们的销售团队了解更多信息。

### 运行推理

HUGS 基于 Text Generation Inference (TGI)，提供无缝的推理体验。有关详细说明和示例，请参阅在 HUGS 上运行推理指南。HUGS 利用与 OpenAI 兼容的 Messages API，允许您使用熟悉的工具和库（如 cURL、huggingface_hub SDK 和 openai SDK）发送请求。

```py
from huggingface_hub import InferenceClient

ENDPOINT_URL="REPLACE" 

client = InferenceClient(base_url=ENDPOINT_URL, api_key="-")

chat_completion = client.chat.completions.create(
    messages=[
        {"role":"user","content":"什么是深度学习？"},
    ],
    temperature=0.7,
    top_p=0.95,
    max_tokens=128,
)

```

## 支持的模型和硬件

HUGS 支持不断增长的开放模型和硬件平台生态系统。请参阅我们的支持模型和支持硬件页面以获取最新信息。

我们今天推出 13 个流行的开放 LLM：

- meta-llama/Llama-3.1-8B-Instruct
- meta-llama/Llama-3.1-70B-Instruct
- meta-llama/Llama-3.1-405B-Instruct-FP8
- NousResearch/Hermes-3-Llama-3.1-8B
- NousResearch/Hermes-3-Llama-3.1-70B
- NousResearch/Hermes-3-Llama-3.1-405B-FP8
- NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO
- mistralai/Mixtral-8x7B-Instruct-v0.1
- mistralai/Mistral-7B-Instruct-v0.3
- mistralai/Mixtral-8x22B-Instruct-v0.1
- google/gemma-2-27b-it
- google/gemma-2-9b-it
- Qwen/Qwen2.5-7B-Instruct

有关支持的模型 x 硬件的详细视图，请查看文档。

## 立即开始使用 HUGS

HUGS 让您能够轻松利用开放模型的力量，在您自己的基础设施中实现零配置的优化推理。借助 HUGS，您可以掌控您的 AI 应用，并轻松地将使用封闭模型构建的概念验证应用过渡到您自行托管的开放模型。

立即开始，在 AWS、Google Cloud 或 DigitalOcean 上部署 HUGS！

---

> 本文由AI自动翻译，原文链接：[Introducing HUGS - Scale your AI with Open Models](https://huggingface.co/blog/hugs)
> 
> 翻译时间：2026-06-13 06:19
