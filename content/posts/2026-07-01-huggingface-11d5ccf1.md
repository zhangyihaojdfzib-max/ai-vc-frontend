---
title: Hugging Face与Cerebras联手，将Gemma 4带入实时语音AI
title_original: Hugging Face and Cerebras bring Gemma 4 to real-time voice AI
date: '2026-07-01'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/cerebras-gemma4-voice-ai
author: ''
summary: Hugging Face与Cerebras合作，将Gemma 4模型集成到实时语音AI流水线中，通过模块化、开放的语音到语音架构，显著降低延迟并提升响应稳定性。该方案结合Nvidia的语音识别、Cerebras的快速推理、Google
  DeepMind的Gemma 4语言模型以及阿里巴巴的文本转语音技术，实现了更自然的对话体验。目前已有超过9000台Reachy Mini机器人采用该流水线，展示了开放高性能AI在语音交互领域的潜力。
categories:
- AI产品
tags:
- 实时语音AI
- Gemma 4
- Cerebras
- Hugging Face
- 开源模型
draft: false
translated_at: '2026-07-06T06:50:06.322134'
---

# Hugging Face 与 Cerebras 将 Gemma 4 带入实时语音 AI

对于语音 AI 而言，延迟是一个关键参数。开发者在模型质量方面取得了巨大进步，但用户体验仍常常受限于响应时间。Hugging Face 和 Cerebras 正在改变这一体验。今天，我们展示了当开放的模块化语音 AI 架构与行业领先的推理速度相结合时，能够实现怎样的可能。

其结果是带来一种感觉上更加自然的语音到语音体验。对话不再是等待 AI 回应，而是以用户期望的人类互动般的响应性流畅进行。

## 架构：开放的级联式语音到语音堆栈

该演示构建为一个实时的语音到语音流水线。系统的每个部分都是模块化、开放且可替换的，使开发者能够轻松地将该堆栈适配于不同的助手、机器人、产品或研究项目。

这创建了一个完全开放的语音到语音循环：

```text
语音输入
  -> 使用 Nvidia 的 Parakeet 进行语音识别
  -> 在 Cerebras 上进行 Gemma 4 VLM 推理
  -> 使用阿里巴巴的 Qwen3TTS 进行文本转语音
  -> 语音响应

```

该架构汇集了开源 AI 生态系统的优势：Cerebras 提供快速推理，Google DeepMind 的 Gemma 4 31B 作为语言模型，Qwen 负责文本转语音。每一层都可以由开发者进行检查、修改和扩展。

## Cerebras 与 Hugging Face 的合作

如今，一些生产系统虽然中位延迟尚可，但在 P95 分位上仍会经历令人沮丧的数秒延迟。当工具调用或多模态步骤需要多轮交互时，这些延迟会变得更加明显。

Cerebras 帮助解决了该堆栈中最重要的瓶颈之一：语言模型的响应时间。通过使推理速度大幅提升且更加稳定，Cerebras 让 Hugging Face 流水线的其余部分得以充分发挥优势。

这种稳定性在长尾分布中尤为重要。许多系统能够提供可接受的中位响应时间，但偶尔的慢响应仍会让对话显得不可靠。

## 为真实世界交互而构建

同样的 Hugging Face 语音到语音流水线已经为 Reachy Mini 机器人提供支持，目前已有超过 9000 台机器人在实际环境中运行。对于机器人、语音助手和具身 AI 而言，响应性并非锦上添花的改进，而是让交互充满生命力的关键。

因此，使用 Cerebras 的动机不仅仅是降低成本。它带来的是低延迟、可预测的性能，以及能够大规模创建感觉自然的实时体验的能力。

此次合作反映了双方的共同信念：AI 的未来将是开放且高性能的。开源模型、开放基础设施以及突破性的推理速度，共同为下一代对话式 AI 奠定了基础。

我们邀请开发者探索该演示，尝试使用代码，并共同塑造实时语音 AI 的未来方向。

演示：Hugging Face Space

代码仓库：huggingface/speech-to-speech

---

> 本文由AI自动翻译，原文链接：[Hugging Face and Cerebras bring Gemma 4 to real-time voice AI](https://huggingface.co/blog/cerebras-gemma4-voice-ai)
> 
> 翻译时间：2026-07-06 06:50
