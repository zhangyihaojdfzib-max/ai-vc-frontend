---
title: 本地训练运行Stanford Alpaca完整指南
title_original: Train and run Stanford Alpaca on your own machine – Replicate blog
date: '2023-03-16'
source: Replicate Blog
source_url: https://replicate.com/blog/replicate-alpaca
author: ''
summary: 本文详细介绍了如何在自有机器上训练并运行Stanford Alpaca模型。Alpaca是基于Meta开源LLaMA模型微调而成的指令响应模型，性能接近ChatGPT但完全开源。文章提供了从获取LLaMA权重、转换模型格式、配置训练环境到实际训练和运行模型的完整步骤，并强调了模型仅限研究用途。作者使用Replicate的Cog工具简化了依赖配置，在4块A100
  GPU上约1.5小时即可完成训练。
categories:
- AI基础设施
tags:
- Stanford Alpaca
- LLaMA
- 模型微调
- 开源AI
- 本地部署
draft: false
translated_at: '2026-06-03T06:52:10.931452'
---

- Replicate  
- 博客  

# 在自己的机器上训练并运行 Stanford Alpaca  

- zeke  

LLaMA 是 Meta Research 推出的全新开源语言模型，其性能与闭源模型相当。与 Stable Diffusion 类似，自该模型公开发布以来，涌现了大量实验和创新。正如 Simon Willison 所言，LLaMA 易于在自己的硬件上运行，规模足够大以发挥实用价值，且开源程度足以支持自由修改。  

LLaMA 功能强大，但并非为回答问题而设计。它更像一个高级版的自动补全工具，而非对话机器人。这正是 Stanford 的 Alpaca 的用武之地。Alpaca 是 LLaMA 的微调版本，能够像 ChatGPT 一样响应指令。与 LLaMA 一样，它也是开源的。  

问题在于，Alpaca 的权重尚未发布，因此你无法直接修改它。不过，我们拥有复现所需的所有组件：LLaMA 权重、训练数据和训练脚本。  

本文将展示如何训练 Alpaca，以便你在自己的机器上进行修改。  

注意：LLaMA 及基于 LLaMA 构建的任何模型仅限研究用途，不得用于商业开发。  

## 前置条件  

- LLaMA 权重：仅限研究使用。如需申请访问权限，请填写此 Meta Research 表单。  
- GPU 机器：需要一台配备一个或多个 80GB A100 GPU 的 Linux 机器。使用更多 GPU 的机器会更快——我们使用了四块 GPU。我们在 Google Cloud 上取得了成功。你可以按照此处的说明操作。  

## 步骤 1：克隆 Alpaca 仓库  

我们创建了 Alpaca 仓库的一个分支，并添加了一个 Cog 文件，可自动为你配置所有依赖项。  

通过 SSH 登录你的 GPU 实例。运行以下命令克隆仓库：  

```
git clone https://github.com/replicate/cog_stanford_alpaca
cd cog_stanford_alpaca
```  

## 步骤 2：转换 LLaMA 权重  

LLaMA 权重目前仅限研究使用。如需申请访问权限，请填写此 Meta Research 表单。  

将下载的权重放入名为 `unconverted-weights` 的文件夹中。文件夹层级应如下所示：  

```
unconverted-weights
├── 7B
│   ├── checklist.chk
│   ├── consolidated.00.pth
│   └── params.json
├── tokenizer.model
└── tokenizer_checklist.chk
```  

使用以下命令将权重从 PyTorch 检查点转换为 transformers 兼容格式：  

```
cog run python -m transformers.models.llama.convert_llama_weights_to_hf \
  --input_dir unconverted-weights \
  --model_size 7B \
  --output_dir weights
```  

最终目录结构应如下所示：  

```
weights
├── llama-7b
└── tokenizermdki
```  

## 步骤 3：训练模型  

启动训练：  

```
cog run ./train_model.sh
```  

在四块 A100 上大约需要一个半小时，因此你可以在模型自我编程的同时去写点代码。  

## 步骤 4：运行模型  

训练完成后，你可以运行 Alpaca：  

```
$ cog predict -i prompt="Tell me something about alpacas.

Alpacas are a species of South American camelid and are closely related to llamas. They are smaller than llamas and have a finer fleece, which is used to make clothing and other crafts. Alpacas are social animals that live in herds and can come in two colors: white and brown. They are very easy to take care of and require minimal grooming.
```  

![Alpaca](/images/posts/7a4b40c656d3.webp)  

## 后续步骤  

以下是一些你可以尝试的方向：  

- 微调模型或约束解码器，以创建针对特定任务的模型。  
- 尝试不同的交互界面。你可以在哪些场景下与它对话？  
- 将模型推送到 Replicate，以便在云端运行。如果你需要 API 来构建界面，或并行运行大规模评估，这会非常方便。你需要将其设为私有，以避免权重公开。  

请记住，Alpaca 仅限非商业研究用途。最终，我们期待这类模型能以更宽松的许可协议发布，从而用于聊天机器人、编程助手等各种场景。  

开源语言模型才刚刚起步，我们迫不及待想看到你的成果。  

我们将发布更多关于开源语言模型改造的指南。在 Twitter 上关注我们，以获取最新动态。

---

> 本文由AI自动翻译，原文链接：[Train and run Stanford Alpaca on your own machine – Replicate blog](https://replicate.com/blog/replicate-alpaca)
> 
> 翻译时间：2026-06-03 06:52
