---
title: AI视频迎来爆发期：多款媲美Sora的模型涌现
title_original: AI video is having its Stable Diffusion moment – Replicate blog
date: '2024-12-16'
source: Replicate Blog
source_url: https://replicate.com/blog/ai-video-is-having-its-stable-diffusion-moment
author: ''
summary: 本文指出，继OpenAI发布Sora技术预览后，AI视频生成领域正迎来类似Stable Diffusion的爆发时刻。文章重点介绍了当前已涌现的多款高质量视频生成模型，如Minimax
  Video-01、腾讯混元视频、Luma Ray等，它们在画质、速度、开源性等方面各有侧重。其中部分模型已开源，为社区微调和二次开发提供了可能。这些进展表明，AI视频技术正从技术演示走向实际应用，生态日趋繁荣。
categories:
- AI产品
tags:
- AI视频生成
- Sora
- 开源模型
- Replicate
- 技术趋势
draft: false
translated_at: '2026-02-26T04:32:10.955901'
---

- Replicate
- Blog

# AI视频正迎来它的Stable Diffusion时刻

- fofr

AI视频曾经表现平平：

然而10个月后，OpenAI发布了Sora：

Sora重塑了人们对视频模型的期待。其输出成果具备高分辨率、流畅度和连贯性。展示案例宛若真实影像，令人恍如跃入未来之境。

问题在于——无人能实际使用！这仅是一次技术预览。

这恰似2021年OpenAI发布DALL-E图像生成模型时的情景。那是多年来最惊艳的软件成果之一，却无人能亲身体验。

这种被压抑的需求最终催生了Stable Diffusion——我们去年曾撰文探讨过这一现象。

如今视频领域正在重演历史。Sora让所有人看到了技术可能性。

## 当前已涌现众多媲美Sora的模型

部分模型追求极致画质，部分专注生成速度，有些侧重写实风格，另一些则聚焦艺术创意。

其中不乏开源模型，社区正持续进行修改优化与二次开发。您可通过微调为其注入新风格、新物件、新角色等特性。

ELO评分源自Artificial Analysis。速度与时长数据基于生成5秒720p视频的耗时（特别说明除外）。

多数模型已在Replicate平台上线。您可通过浏览器直接体验，或调用API进行开发。以下推荐值得尝试的模型：

### Minimax Video-01

Video-01（又名海螺）在写实性与连贯性方面表现最佳。从多维度看，其品质已与Sora比肩：画面同样流畅、主体高度连贯、分辨率出色，对非常规主体也有良好处理能力。不过尚未具备Sora的全部功能特性。

支持通过文本描述或起始帧图像生成5秒720p视频。该模型为闭源产品，单次生成约需3分钟。

在Replicate运行：minimax/video-01

### 腾讯混元视频

混元视频与Sora、Minimax Video-01同属顶尖梯队，且为开源模型！

开源特性赋予无限可能：您可进行微调改造，社区已实现视频转视频功能，参数配置更灵活（分辨率、时长、步数、引导尺度等）。除5秒720p视频外，还能生成更轻量快速的540p版本。通过调整步数与分辨率，可快速进行多样化尝试。

不足之处在于生成速度慢于Video-01，但我们正持续优化加速方案。所有优化成果将保持开源。

在Replicate运行：tencent/hunyuan-video

### Luma Ray

Luma Ray（又名Dream Machine）在写实性上虽不及Minimax Video-01或混元视频，但胜在生成速度与创意表现。今年6月发布的它，堪称新一代高性能视频模型的先驱代表。

生成5秒720p视频仅需40秒。其输出控制工具更为丰富：
- 起始帧与结束帧设定
- 双视频间插值生成
- 循环视频制作

Ray 2版本即将发布。

在Replicate运行：luma/ray

### Haiper 2.0

Haiper 2.0于10月发布，支持生成4秒与6秒的720p视频。其中6秒视频生成约需5分钟。可通过文本或图像输入，生成多种宽高比的视频内容。

4K版本即将面世。

在Replicate运行：haiper-ai/haiper-video-2

### Genmo Mochi 1

Mochi 1是首个发布的高质量开源视频模型。初期运行需4张H100显卡，后经社区优化，现仅需单张4090显卡即可运行。

在Replicate运行：genmoai/mochi-1

您还可在Replicate平台微调Mochi 1：使用genmoai/mochi-1-lora-trainer进行训练，通过genmoai/mochi-1-lora运行训练后的模型。

### Lightricks LTX-Video

LTX-Video是低内存占用的开源视频模型。其速度惊人：在L40S GPU上仅需10秒即可生成3秒视频（其他模型在H100上往往需要数分钟）。

虽然速度卓越，但需注意其画质相对其他模型有所折衷。

在Replicate运行：lightricks/ltx-video

## 更多选择

尚有部分优秀模型暂未登陆Replicate：
- Kling AI
- OpenAI Sora
- 具备强大"场景成分"功能的Pika 2.0
- Runway Gen3

当然，我们仍在期待Black Forest Labs（FLUX创造者）发布备受瞩目的视频模型。

关注我们的X账号获取最新动态。

---

> 本文由AI自动翻译，原文链接：[AI video is having its Stable Diffusion moment – Replicate blog](https://replicate.com/blog/ai-video-is-having-its-stable-diffusion-moment)
> 
> 翻译时间：2026-02-26 04:32
