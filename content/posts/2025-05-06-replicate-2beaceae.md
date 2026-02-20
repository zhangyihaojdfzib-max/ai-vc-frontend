---
title: 通过API运行MiniMax Speech-02：顶级文本转语音模型
title_original: Run MiniMax Speech-02 models with an API – Replicate blog
date: '2025-05-06'
source: Replicate Blog
source_url: https://replicate.com/blog/minimax-text-to-speech
author: ''
summary: 本文介绍了如何在Replicate平台上通过API运行MiniMax Speech-02系列文本转语音模型。该系列包含高质量的Speech-02-HD和更快速的Speech-02-Turbo，支持超过30种语言和语音克隆功能，可根据文本自动或手动添加情感，适用于虚拟助手、有声读物、语言学习等多种应用场景。文章还提供了使用JavaScript客户端进行语音克隆和语音合成的具体代码示例。
categories:
- AI产品
tags:
- 文本转语音
- MiniMax
- API
- 语音克隆
- AI应用
draft: false
translated_at: '2026-02-20T04:35:56.802563'
---

- Replicate
- 博客

# 通过API运行MiniMax Speech-02模型

- fofr

MiniMax推出的Speech-02系列是文本转语音模型，可让您创建具有情感表达的自然语音。该系列模型支持超过30种语言。

根据Artificial Analysis Speech Arena的评测，Speech-02-HD是当前最佳的文本转语音模型，而Speech-02-Turbo则位列第三。

通过Replicate，您只需一行代码即可运行这些模型。

## 试听MiniMax Speech-02

以下是Speech-02-HD模型朗读此博客文章改编版本的示例，以及生成该音频的预测结果。

试听此博客文章

![MiniMax Speech-02模型是当今最优秀的文本转语音模型。](/images/posts/79f0e5718273.webp)

MiniMax Speech-02模型是当今最优秀的文本转语音模型。

## 试用MiniMax Speech-02

您可以选择两种模型：适用于高质量画外音和有声读物的Speech-02-HD，以及更经济、速度更快、最适合实时应用的Speech-02-Turbo。

两种模型都支持使用克隆语音。语音克隆至少需要10秒的音频，训练耗时约30秒。每个克隆语音的音调、语速和音量均可调整，使其听起来更自然。

在我们的游乐场中试用这些模型：

- Speech-02-HD - 适用于高质量画外音和有声读物
- Speech-02-Turbo - 适用于实时应用
- 语音克隆 - 用于创建自定义语音

## 您可以构建的应用

这些模型可以帮助您创建：

- 听起来自然的虚拟助手
- 具有录音室品质音效的有声读物和画外音
- 具备地道发音的语言学习工具
- 能说多种语言的客服机器人
- 为偏好音频的用户提供无障碍内容

## 情感控制

MiniMax的情感控制系统有两种为语音添加情感的方式。自动检测模式可从您的文本中推断情感基调，而手动控制则允许您精确设置所需的情感。无论您是为娱乐、教育还是商业制作内容，这都有助于您的语音听起来自然且富有感染力。

## 语言支持

这些模型支持超过30种语言和口音。您可以使用不同的英语变体（美式、英式、澳大利亚式和印度式）、亚洲语言（普通话、粤语、日语、韩语、越南语和印尼语）以及欧洲语言（法语、德语、西班牙语、葡萄牙语、土耳其语、俄语和乌克兰语）。

## 使用JavaScript进行语音克隆和文本转语音

您可以使用我们的JavaScript客户端运行这些模型。首先，安装Node.js客户端库：

```
npm install replicate
```

将您的API令牌设置为环境变量：

```
export REPLICATE_API_TOKEN=r8_9wm**********************************
```

（您可以从您的账户获取API令牌。请妥善保管。）

导入并设置客户端：

```
import Replicate from "replicate";

const replicate = new Replicate({
  auth: process.env.REPLICATE_API_TOKEN,
});
```

首先，克隆一个语音。您需要一个MP3、M4A或WAV格式的音频文件。文件时长应在10秒到5分钟之间，大小小于20MB：

```
const cloneOutput = await replicate.run(
  "minimax/voice-cloning",
  {
    input: {
      voice_file: "path/to/your/audio.wav", // mp3, wav, or m4a
      model: "speech-02-turbo" // speech-02-hd or speech-02-turbo
    }
  }
);

const voiceId = cloneOutput.voice_id;
console.log("Cloned voice ID:", voiceId);
```

现在使用克隆的语音进行文本转语音。您可以使用`<#x#>`在单词之间添加停顿，其中x是以秒为单位的停顿时长（0.01-99.99）：

```
const input = {
  text: "Hello! <#0.5#> This is a test using my cloned voice. <#1.0#> I can add pauses between words to make the speech sound more natural.",
  voice_id: voiceId, // Use the cloned voice ID
  emotion: "happy" // Optional: happy, sad, angry, etc.
};

const output = await replicate.run("minimax/speech-02-turbo", { input });
console.log(output);
```

## 使用Python进行语音克隆和文本转语音

您可以使用我们的Python客户端运行这些模型。首先，安装客户端并设置您的API令牌：

```
pip install replicate
export REPLICATE_API_TOKEN=r8_9wm**********************************
```

以下是克隆语音并使用其进行文本转语音的方法：

```
import replicate

# Clone a voice (needs MP3, M4A, or WAV file, 10s-5min, <20MB)
clone_output = replicate.run(
    "minimax/voice-cloning",
    input={
        "voice_file": "path/to/your/audio.wav",
        "model": "speech-02-turbo"
    }
)

# Generate speech with the cloned voice
# Add pauses between words using <#x#> where x is the pause duration in seconds (0.01-99.99)
output = replicate.run(
    "minimax/speech-02-turbo",
    input={
        "text": "Hello! <#0.5#> This is a test using my cloned voice. <#1.0#> I can add pauses between words to make the speech sound more natural.",
        "voice_id": clone_output["voice_id"],
        "emotion": "happy"
    }
)
print(output)
```

## 定价

文本转语音模型根据输入和输出的Token计费。Turbo模型每百万字符收费30美元，HD模型每百万字符收费50美元。一个Token对应一个字符。

语音克隆每个语音收费3美元。

## 保持同步

通过在X上关注我们并加入我们的Discord社区，与我们的社区保持联系，获取最新动态并参与讨论。

祝您探索愉快！🎙️

---

> 本文由AI自动翻译，原文链接：[Run MiniMax Speech-02 models with an API – Replicate blog](https://replicate.com/blog/minimax-text-to-speech)
> 
> 翻译时间：2026-02-20 04:35
