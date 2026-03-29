---
title: 解放OpenClaw：从Claude迁移到开源模型的完整指南
title_original: Liberate your OpenClaw
date: '2026-03-27'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/liberate-your-openclaw
author: ''
summary: 本文针对Anthropic限制Claude模型在开放Agent平台访问的情况，提供了将OpenClaw等智能体迁移到开源模型的解决方案。文章详细介绍了两种迁移路径：一是通过Hugging
  Face推理提供商使用托管开源模型，推荐GLM-5等优秀模型；二是在本地硬件上运行Llama.cpp等开源库，实现完全隐私和零API成本。文章包含具体的配置步骤、命令示例和硬件建议，帮助用户快速恢复智能体运行能力。
categories:
- AI基础设施
tags:
- 开源模型
- 智能体迁移
- Hugging Face
- 本地部署
- AI工具
draft: false
translated_at: '2026-03-29T05:00:58.068054'
---

# 解放你的OpenClaw 🦀

Anthropic正在限制Pro/Max订阅用户对Claude模型在开放Agent（智能体）平台上的访问。不过别担心，Hugging Face上有许多优秀的开源模型可以让你的Agent（智能体）继续运行！大多数情况下，成本只是原来的一小部分。

如果你的访问已被切断，并且你的OpenClaw、Pi或Open Code Agent（智能体）需要恢复运行，你可以通过两种方式将它们迁移到开源模型：

1.  使用通过Hugging Face推理提供商提供的开源模型。
2.  在你自己的硬件上运行一个完全本地的开源模型。

托管路线是让你的Agent（智能体）快速恢复能力的最快途径。如果你需要隐私、零API成本以及完全控制权，本地路线则是合适的选择。

为此，只需告诉你的Claude代码、你的Cursor或你最喜欢的Agent（智能体）：`help me move my OpenClaw agents to Hugging Face models`，并附上此页面链接。

## Hugging Face推理提供商

Hugging Face推理提供商是一个开放平台，它将请求路由到开源模型的提供商。如果你想要最好的模型，或者你没有必要的硬件，这是一个正确的选择。

首先，你需要在此处创建一个Token。然后你可以像这样将该Token添加到`openclaw`：

```shell
openclaw onboard --auth-choice huggingface-api-key

```

当提示时粘贴你的Hugging Face Token，系统会要求你选择一个模型。

我们推荐`GLM-5`，因为它在`Terminal Bench`上得分优异，但这里有数千个模型可供选择。

你可以随时通过在其repo_id中输入OpenClaw配置来更新你的Hugging Face模型：

```
{
  agents: {
    defaults: {
      model: {
        primary: "huggingface/zai-org/GLM-5:fastest"
      }
    }
  }
}

```

注意：HF PRO订阅者每月可获得2美元的免费积分，适用于推理提供商的使用，了解更多信息请点击此处。

## 本地设置

本地运行模型可以为你提供完全的隐私、零API成本，以及无速率限制的实验能力。

安装Llama.cpp，这是一个用于低资源推理的完全开源库。

```shell
# on mac or linux
brew install llama.cpp

# on windows
winget install llama.cpp

```

启动一个带有内置Web UI的本地服务器：

```shell
llama-server -hf unsloth/Qwen3.5-35B-A3B-GGUF:UD-Q4_K_XL

```

这里，我们使用的是Qwen3.5-35B-A3B，它在32GB内存下运行良好。如果你有不同的需求，请查看你感兴趣的模型的硬件兼容性。有数千个模型可供选择。

如果你在llama.cpp中加载GGUF模型，请使用类似这样的OpenClaw配置：

```shell
openclaw onboard --non-interactive \                                                                                   
   --auth-choice custom-api-key \                                                                                         
   --custom-base-url "http://127.0.0.1:8080/v1" \                                                                         
   --custom-model-id "unsloth-qwen3.5-35b-a3b-gguf" \                                                                     
   --custom-api-key "llama.cpp" \                                                                                         
   --secret-input-mode plaintext \                                                                                        
   --custom-compatibility openai

```

验证服务器是否正在运行以及模型是否已加载：

```shell
curl http://127.0.0.1:8080/v1/models

```

## 你应该选择哪条路径？

如果你希望以最快的方式让OpenClaw Agent（智能体）恢复能力，请使用Hugging Face推理提供商。如果你需要隐私、完全的本地控制权并且不想支付API费用，请使用`llama.cpp`。

无论哪种方式，你都不需要一个封闭的托管模型就能让OpenClaw重新站起来！

---

> 本文由AI自动翻译，原文链接：[Liberate your OpenClaw](https://huggingface.co/blog/liberate-your-openclaw)
> 
> 翻译时间：2026-03-29 05:00
