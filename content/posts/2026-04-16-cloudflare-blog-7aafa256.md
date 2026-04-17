---
title: Cloudflare AI平台：统一推理层，专为智能体设计
title_original: "Cloudflareâ\x80\x99s AI Platform: an inference layer designed for\
  \ agents"
date: '2026-04-16'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/ai-platform/
author: ''
summary: Cloudflare推出统一的AI推理平台，旨在解决构建智能体时面临的多模型调用、供应商锁定、成本监控和延迟管理等挑战。该平台通过单一API接入超过12家提供商的70多个模型，支持图像、视频和语音等多模态应用，并提供集中式的成本管理和监控功能。同时，平台允许用户自带自定义模型，并具备故障自动重试等可靠性保障，帮助开发者快速构建可靠、高效的AI驱动应用。
categories:
- AI基础设施
tags:
- Cloudflare
- AI推理平台
- 智能体开发
- 多模型管理
- AI基础设施
draft: false
translated_at: '2026-04-17T04:50:40.874534'
---

# Cloudflare AI平台：专为智能体设计的推理层

2026-04-16

- 明路
- 米歇尔·陈

![](/images/posts/49b63d41df67.png)

AI模型正在快速变化：今天用于智能体编码的最佳模型，可能在三个月后就会变成来自不同提供商的完全不同的模型。除此之外，现实世界的用例通常需要调用不止一个模型。您的客户支持智能体可能使用一个快速、廉价的模型来对用户消息进行分类；使用一个大型推理模型来规划其行动；并使用一个轻量级模型来执行单个任务。

这意味着您需要能够访问所有模型，而无需在财务和运营上将自己绑定到单一提供商。您还需要建立合适的系统来监控跨提供商的成本，确保在其中一家出现故障时的可靠性，并管理延迟，无论您的用户身在何处。

无论何时使用AI进行构建，这些挑战都存在，但在构建智能体时，它们变得更加紧迫。一个简单的聊天机器人可能每个用户提示进行一次推理调用。一个智能体可能将十次调用链接在一起以完成单个任务，突然间，一个缓慢的提供商增加的就不是50毫秒，而是500毫秒。一次失败的请求不再是重试，而是突然引发一连串的下游故障。

自推出AI Gateway和Workers AI以来，我们看到了在Cloudflare上构建AI驱动应用的开发者令人难以置信的采用率，并且我们一直在快速发布更新以跟上需求！就在过去几个月里，我们更新了仪表板，添加了零设置默认网关、上游故障自动重试以及更细粒度的日志控制。今天，我们正在将Cloudflare转变为一个统一的推理层：一个API即可访问任何提供商的任何AI模型，旨在实现快速和可靠。

### 一个目录，一个统一端点

从今天开始，您可以使用与Workers AI相同的AI.run()绑定来调用第三方模型。如果您正在使用Workers，从Cloudflare托管的模型切换到OpenAI、Anthropic或任何其他提供商的模型，只需更改一行代码。

```Typescript
const response = await env.AI.run('anthropic/claude-opus-4-6',{
input: 'What is Cloudflare?',
}, {
gateway: { id: "default" },
});
```

对于那些不使用Workers的用户，我们将在未来几周内发布REST API支持，以便您可以从任何环境访问完整的模型目录。

我们也很高兴地分享，您现在可以通过一个API访问来自12家以上提供商的70多个模型——只需一行代码即可在它们之间切换，并使用一套积分进行支付。并且我们正在迅速扩展这个列表。

您可以浏览我们的模型目录，为您的用例找到最佳模型，从托管在Cloudflare Workers AI上的开源模型到主要模型提供商的专有模型。我们很高兴能够扩展对来自阿里云、AssemblyAI、字节跳动、Google、InWorld、MiniMax、OpenAI、Pixverse、Recraft、Runway和Vidu的模型的访问——这些提供商将通过AI Gateway提供他们的模型。值得注意的是，我们正在扩展我们的模型产品，以包括图像、视频和语音模型，以便您可以构建多模态应用。

通过一个API访问所有模型也意味着您可以在一个地方管理所有的AI支出。如今，大多数公司平均调用来自多个提供商的3.5个模型，这意味着没有一个提供商能够为您提供AI使用情况的整体视图。通过AI Gateway，您将获得一个集中位置来监控和管理AI支出。

通过在请求中包含自定义元数据，您可以获得关于您最关心的属性的成本细分，例如免费用户与付费用户的支出、单个客户的支出或应用中特定工作流的支出。

```Typescript
const response = await env.AI.run('@cf/moonshotai/kimi-k2.5',
      {
prompt: 'What is AI Gateway?'
      },
      {
metadata: { "teamId": "AI", "userId": 12345 }
      }
    );
```

### 自带模型

AI Gateway让您可以通过一个API访问所有提供商的模型。但有时您需要运行一个基于您自己的数据微调的模型，或者为您的特定用例优化的模型。为此，我们正在努力让用户能够将他们自己的模型带到Workers AI。

我们绝大部分流量来自企业客户的专用实例，他们在我们的平台上运行自定义模型，我们希望将这一功能带给更多客户。为了实现这一点，我们利用Replicate的Cog技术来帮助您容器化机器学习模型。

Cog设计得非常简单：您所需要做的就是在cog.yaml文件中写下依赖项，并在Python文件中编写您的推理代码。Cog抽象了打包ML模型的所有复杂问题，例如CUDA依赖、Python版本、权重加载等。

cog.yaml文件示例：

```XML
build:
  python_version: "3.13"
  python_requirements: requirements.txt
predict: "predict.py:Predictor"
```

predict.py文件示例，其中包含一个用于设置模型的函数和一个在收到推理请求（预测）时运行的函数：

```Python
from cog import BasePredictor, Path, Input
import torch

class Predictor(BasePredictor):
    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        self.net = torch.load("weights.pth")

    def predict(self,
            image: Path = Input(description="Image to enlarge"),
            scale: float = Input(description="Factor to scale image by", default=1.5)
    ) -> Path:
        """Run a single prediction on the model"""
        # ... pre-processing ...
        output = self.net(input)
        # ... post-processing ...
        return output
```

然后，您可以运行cog build来构建您的容器镜像，并将您的Cog容器推送到Workers AI。我们将为您部署并提供该模型，然后您可以通过常用的Workers AI API访问它。

我们正在进行一些大型项目，以便能够将此功能带给更多客户，例如面向客户的API和wrangler命令，以便您可以推送自己的容器，以及通过GPU快照实现更快的冷启动。我们一直在内部与Cloudflare团队和一些外部客户测试此功能，他们正在指导我们的愿景。如果您有兴趣成为我们的设计合作伙伴，请联系我们！很快，任何人都将能够打包他们的模型并通过Workers AI使用它。

### 通往首个Token的快速路径

如果您正在构建实时智能体，将Workers AI模型与AI Gateway结合使用尤其强大——在这种情况下，用户对速度的感知取决于首个Token的时间或智能体开始响应的速度，而不是完整响应所需的时间。即使总推理时间是3秒，将首个Token提前50毫秒获得，也会让智能体感觉敏捷还是迟钝产生天壤之别。

Cloudflare遍布全球330个城市的数据中心网络意味着AI Gateway靠近用户和推理端点，从而最大限度地减少了流式传输开始前的网络时间。

Workers AI还在其公共目录上托管开源模型，该目录现在包括专为智能体构建的大型模型，包括Kimi K2.5和实时语音模型。当您通过AI Gateway调用这些Cloudflare托管的模型时，由于您的代码和推理运行在同一全球网络上，因此无需经过公共互联网的额外跳转，从而为您的智能体提供尽可能低的延迟。

### 为可靠性而构建，具备自动故障转移功能

在构建智能体时，速度并不是用户关心的唯一因素——可靠性也很重要。智能体工作流中的每一步都依赖于其前面的步骤。可靠的推理对智能体至关重要，因为一次调用失败可能会影响整个下游链。

通过AI Gateway，如果您调用的模型在多个供应商处可用，且其中一家供应商出现故障，我们将自动路由至另一家可用供应商，无需您自行编写任何故障转移逻辑。

如果您使用Agents SDK构建长期运行的Agent（智能体），您的流式推理调用也具备连接中断的恢复能力。AI Gateway会在流式响应生成时进行缓冲，这与您Agent的生命周期无关。如果您的Agent在推理过程中被中断，它可以重新连接到AI Gateway并检索响应，而无需发起新的推理调用或为相同的输出Token重复付费。结合Agents SDK内置的检查点功能，最终用户将完全察觉不到中断。

### Replicate

Replicate团队已正式加入我们的AI平台团队，以至于我们甚至不再视自己为独立的团队。我们一直在努力推进Replicate与Cloudflare的集成工作，包括将所有Replicate模型接入AI Gateway，并将托管模型迁移至Cloudflare基础设施。很快，您将能够通过AI Gateway访问您在Replicate上喜爱的模型，并且也能将您在Replicate上部署的模型托管到Workers AI上。

### 开始使用

要开始使用，请查阅我们的[AI Gateway](https://developers.cloudflare.com/ai-gateway/)或[Workers AI](https://developers.cloudflare.com/workers-ai/)文档。通过[Agents SDK](https://developers.cloudflare.com/agents/)了解更多关于在Cloudflare上构建Agent的信息。

### 在Cloudflare TV上观看

---

> 本文由AI自动翻译，原文链接：[Cloudflareâs AI Platform: an inference layer designed for agents](https://blog.cloudflare.com/ai-platform/)
> 
> 翻译时间：2026-04-17 04:50
