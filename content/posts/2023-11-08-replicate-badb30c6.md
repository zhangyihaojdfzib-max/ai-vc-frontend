---
title: MusicGen-Chord：用和弦与文本提示生成多元风格音乐
title_original: Generate music from chord progressions and text prompts with MusicGen-Chord
  – Replicate blog
date: '2023-11-08'
source: Replicate Blog
source_url: https://replicate.com/blog/generate-music-from-chord-progressions-musicgen-chord
author: ''
summary: 本文介绍了基于Meta MusicGen模型改进的MusicGen-Chord模型，它能够根据文本提示、和弦进行和速度生成多种风格的音乐。模型通过将和弦信息编码为“多热”色谱图矩阵，并作为条件输入与文本提示一同引导音乐生成。文章详细解释了其工作原理、和弦输入格式（支持文本或音频），并提供了通过Replicate
  API运行的示例。该工具适用于音乐创作、伴奏制作等多种场景，展示了AI在音乐生成领域的灵活应用。
categories:
- AI产品
tags:
- 音乐生成
- AI音乐
- 和弦识别
- 生成式AI
- Replicate
draft: false
translated_at: '2026-04-11T04:22:18.369084'
---

- Replicate
- Blog

# 使用 MusicGen-Chord 根据和弦进行与文本提示生成音乐

- sakemin

MusicGen-Chord 是一个能够根据文本提示、和弦进行和速度生成任何风格音乐的模型。它基于 Meta 的 MusicGen 模型，我们将其旋律输入部分修改为可接受文本或音频形式的和弦。

例如，以下是三个不同的生成示例，每个都使用了重复的和弦进行“F:maj7 G E:min A:min”：

### “90年代欧陆舞曲，振奋人心，伊比萨风格”，140bpm

您的浏览器不支持视频标签。

### “英国吉他流行乐，The Smiths 乐队风格，1980年代”，113 bpm：

### “神圣室内合唱团，合唱风格”，基于一个微调模型：

# 工作原理

MusicGen-Chord 构建于 Meta 的 MusicGen-Melody 模型之上。MusicGen-Melody 的生成过程同时受文本提示和音频文件的条件约束。

在 MusicGen-Melody 中，音频文件会经过源分离以移除鼓和贝斯部分，然后通过在每个时间步选取色谱图中最突出的音高来提取旋律。这产生了一个独热编码的色度向量矩阵（即每个向量中除一个元素为1外，其余均为0）。

![独热编码旋律色谱图矩阵。黄色格子为1，紫色格子为0。](/images/posts/e424a1480fc7.webp)

MusicGen-Chord 重新利用了旋律输入通道，改为传入“多热”编码的和弦向量。在每个时间步，属于目标和弦的音高被设为1，其余音高设为0。例如，在下面的色谱图中，先是 Eb 和弦（Eb, G, Bb），接着是 G 和弦（D, G, B），然后是 C 小调和弦（C, Eb, G），等等。

![多热编码和弦色谱图矩阵。黄色格子为1，紫色格子为0。](/images/posts/13d3dbefcf46.webp)

与 MusicGen-Melody 类似，MusicGen-Chord 将色谱图作为额外的条件信息，连同文本提示一起传递给 MusicGen。令人有些惊讶的是，这种“技巧”效果非常好——MusicGen 能够渲染出与提示所给风格一致的和弦进行。

## 和弦输入格式

您可以通过文本（例如 `C D:min G:7 C`）或音频输入和弦。如果以文本形式输入和弦，您还可以控制速度和拍号。

`text_chords` 输入的语法是由空格分隔的和弦列表。每个和弦持续一个小节，但您可以通过用逗号分隔的方式在一个小节内添加多个和弦。和弦的定义格式为 `ROOT:TYPE`。有效的和弦类型包括 `maj`、`min`、`dim`、`aug`、`min6`、`maj6`、`min7`、`minmaj7`、`maj7`、`7`、`dim7`、`hdim7`、`sus2` 和 `sus4`。如果省略和弦类型，则默认为大调和弦。例如：

- `B:min G F# E:min`（试听）
- `G:maj7 D:min7,G:7 C:maj7 F:7 B:min7,Bb:7 A:min7,D:7`（试听）

当您传入输入音频文件时，和弦识别是使用《A Bi-Directional Transformer for Musical Chord Recognition》来完成的。

# 运行 MusicGen-Chord

您可以使用 Replicate 的 API 来运行 MusicGen-Chord。以下是一个使用 replicate Python 客户端的示例：

```
import replicate
output = replicate.run(
    "sakemin/musicgen-chord:c940ab4308578237484f90f010b2b3871bf64008e95f26f4d567529ad019a3d6",
    input={
        "prompt": "deep house",
        "text_chords": "A:min A:min E:min D:min",
        "bpm": 140,
        "time_sig": "4/4",
    }
)
print(output)  # 输出生成音频的 URL
```

当然，您也可以在网页上运行它，地址是 replicate.com/sakemin/musicgen-chord。

我们很期待看到您用 MusicGen-Chord 创作出什么作品，无论您是用于生成新音乐、为人声制作伴奏、进行混音，还是其他完全不同的用途。

请在 X 或 Discord 上告诉我们您的创作。

---

> 本文由AI自动翻译，原文链接：[Generate music from chord progressions and text prompts with MusicGen-Chord – Replicate blog](https://replicate.com/blog/generate-music-from-chord-progressions-musicgen-chord)
> 
> 翻译时间：2026-04-11 04:22
