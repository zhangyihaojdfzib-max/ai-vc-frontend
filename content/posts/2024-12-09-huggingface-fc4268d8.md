---
title: Hugging Face模型登陆Amazon Bedrock
title_original: Hugging Face models in Amazon Bedrock
date: '2024-12-09'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/bedrock-marketplace
author: ''
summary: 本文介绍了Hugging Face开源模型现已通过Bedrock Marketplace在Amazon Bedrock上可用，AWS客户可部署83个开源模型构建生成式AI应用。底层由SageMaker
  JumpStart管理，结合了Bedrock的全托管基础设施与高级API兼容性。文章详细演示了如何部署Google Gemma 2 27B Instruct模型，包括从模型目录选择、配置实例、接受许可协议到部署的完整流程，并展示了通过Bedrock
  Converse API调用已部署模型的方法。
categories:
- AI基础设施
tags:
- Hugging Face
- Amazon Bedrock
- 模型部署
- 开源模型
- AWS
draft: false
translated_at: '2026-06-06T05:51:28.245364'
---

# 使用 Hugging Face 模型与 Amazon Bedrock

我们很高兴地宣布，Hugging Face 的热门开源模型现已通过全新的 Bedrock Marketplace 在 Amazon Bedrock 上可用！AWS 客户现在可以通过 Bedrock Marketplace 部署 83 个开源模型，构建其生成式 AI 应用。

在底层，Bedrock Marketplace 模型端点由 Amazon SageMaker JumpStart 管理。借助 Bedrock Marketplace，您现在可以将 SageMaker JumpStart 的易用性与 Amazon Bedrock 的全托管基础设施相结合，包括与 Agent（智能体）、知识库、护栏和模型评估等高级 API 的兼容性。

在 Amazon Bedrock 中注册您的 SageMaker JumpStart 端点时，您只需支付 SageMaker 计算资源费用，常规 Amazon Bedrock API 价格同样适用。

在本博客中，我们将向您展示如何部署 Gemma 2 27B Instruct 并使用 Amazon Bedrock API 调用该模型。了解如何：

1. 部署 Google Gemma 2 27B Instruct
2. 使用 Amazon Bedrock API 发送请求
3. 清理资源

## 部署 Google Gemma 2 27B Instruct

有两种方式可以部署开源模型以与 Amazon Bedrock 配合使用：

1. 您可以从 Bedrock 模型目录部署您的开源模型。
2. 您可以通过 Amazon JumpStart 部署您的开源模型，并将其注册到 Bedrock。

两种方式类似，因此我们将引导您通过 Bedrock 模型目录完成操作。

首先，在 Amazon Bedrock 控制台中，请确保您位于 Bedrock Marketplace 可用的 14 个区域之一。然后，在导航窗格的"基础模型"部分选择"模型目录"。在这里，您可以搜索无服务器模型以及 Amazon Bedrock Marketplace 中可用的模型。按"Hugging Face"提供商筛选结果，您可以浏览 83 个可用的开源模型。

例如，让我们搜索并选择 Google Gemma 2 27B Instruct。

![model-catalog.png](/images/posts/96dd91ff2984.png)

选择模型后，将打开模型详情页面，您可以在其中查看来自模型提供商的更多信息，例如模型亮点以及包括示例 API 调用在内的使用说明。

在右上角，让我们点击"部署"。

![model-card.png](/images/posts/fa24c652db8a.png)

这将带您进入部署页面，您可以在其中选择端点名称、实例配置以及与网络配置和用于在 SageMaker 中执行部署的服务角色相关的高级设置。让我们使用默认高级设置和推荐的实例类型。

您还需要接受模型提供商的最终用户许可协议。

在右下角，让我们点击"部署"。

![model-deploy.png](/images/posts/49347971d649.png)

我们刚刚启动了 Google Gemma 2 27B Instruct 模型在 ml.g5.48xlarge 实例上的部署，该实例托管在您的 Amazon SageMaker 租户中，并与 Amazon Bedrock API 兼容！

端点部署可能需要几分钟时间。它将出现在"Marketplace 部署"页面中，您可以在导航窗格的"基础模型"部分找到该页面。

## 使用 Amazon Bedrock API 调用模型

您可以通过 UI 在 Playground 中快速测试模型。但是，要使用任何 Amazon Bedrock API 以编程方式调用已部署的模型，您需要获取端点 ARN。

从托管部署列表中，选择您的模型部署以复制其端点 ARN。

![model-arn.png](/images/posts/f8b573cef9aa.png)

您可以使用您偏好的 AWS SDK 或 AWS CLI 查询您的端点。

以下是通过 AWS SDK for Python (boto3) 使用 Bedrock Converse API 的示例：

```python
import boto3

bedrock_runtime = boto3.client("bedrock-runtime")


endpoint_arn = "arn:aws:sagemaker:<AWS::REGION>:<AWS::AccountId>:endpoint/<Endpoint_Name>"


inference_config = {
    "maxTokens": 256,
    "temperature": 0.1,
    "topP": 0.999,
}


additional_model_fields = {"parameters": {"repetition_penalty": 0.9, "top_k": 250, "do_sample": True}}
response = bedrock_runtime.converse(
    modelId=endpoint_arn,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "text": "What is Amazon doing in the field of generative AI?",
                },
            ]
        },
        ],
    inferenceConfig=inference_config,
    additionalModelRequestFields=additional_model_fields,
)
print(response["output"]["message"]["content"][0]["text"])

```

```python
"Amazon is making significant strides in the field of generative AI, applying it across various products and services. Here's a breakdown of their key initiatives:\n\n**1. Amazon Bedrock:**\n\n* This is their **fully managed service** that allows developers to build and scale generative AI applications using models from Amazon and other leading AI companies. \n* It offers access to foundational models like **Amazon Titan**, a family of large language models (LLMs) for text generation, and models from Cohere"

```

就是这样！如果您想进一步了解，请查看 Bedrock 文档。

## 清理资源

别忘了在实验结束时删除您的端点，以免产生持续费用！在您获取端点 ARN 的页面右上角，您可以通过点击"删除"来删除您的端点。

---

> 本文由AI自动翻译，原文链接：[Hugging Face models in Amazon Bedrock](https://huggingface.co/blog/bedrock-marketplace)
> 
> 翻译时间：2026-06-06 05:51
