---
title: Seedance 2.0视频生成模型现可通过Vercel AI Gateway直接调用
title_original: Seedance 2.0 Video Generation on AI Gateway - Vercel – Vercel
date: '2026-04-15'
source: Vercel Blog
source_url: https://vercel.com/changelog/seedance-2.0-video-now-available-on-ai-gateway
author: ''
summary: 本文宣布字节跳动最新的视频生成模型Seedance 2.0已集成至Vercel的AI Gateway平台，用户无需其他供应商账户即可直接访问。该模型提供标准版和快速版两种版本，在运动稳定性、细节处理和音频同步方面表现优异。文章重点介绍了其三大核心功能：文生视频、图生视频以及新增的多模态参考生视频，后者允许结合图像、视频和音频作为参考材料。同时，AI
  Gateway承诺不收取额外加价，价格与直接使用字节跳动供应商相同，并提供了具体的代码调用示例。
categories:
- AI产品
tags:
- 视频生成
- Seedance 2.0
- AI Gateway
- Vercel
- 多模态AI
draft: false
translated_at: '2026-04-19T04:50:43.165061'
---

您现在可以通过AI Gateway直接访问字节跳动最新的尖端视频生成模型Seedance 2.0，无需其他供应商账户。

Seedance 2.0在AI Gateway上提供两种版本：标准版和快速版。两者功能相同。标准版能生成最高质量的输出，而快速版则优先考虑生成速度和更低的成本。

Seedance 2.0在保持帧间运动稳定性和精细细节方面表现优异，即使在包含面部表情和物理交互的复杂场景中也能生成一致的输出。该模型还能原生生成同步音频，并支持多种语言和方言的语音。

除了文生视频和图生视频，Seedance 2.0新增了多模态参考生视频功能，允许您将图像、视频和音频输入作为参考材料结合到单次生成中。它还支持视频编辑、视频扩展，以及专业的摄像机运动、多镜头构图和视频内文本渲染。

要使用此模型，请在AI SDK中将模型设置为`bytedance/seedance-2.0`或`bytedance/seedance-2.0-fast`，或者在AI Gateway Playground中试用。

**文生视频**

根据文本提示词生成视频。描述场景、摄像机运动和音频，供模型生成。

```
1import { experimental_generateVideo as generateVideo } from 'ai';2
3const { videos } = await generateVideo({4  model: 'bytedance/seedance-2.0',5  prompt:6   `Black triangle sticker peels off laptop and zips across the office. It smashes7    through the window and into the San Francisco sky.`,8  aspectRatio: '16:9',9  resolution: '720p',10  duration: 5,11});
```

**图生视频**

从起始图像生成视频。模型根据文本提示词对图像进行动画处理，同时保留源帧的视觉内容。

```
1import { experimental_generateVideo as generateVideo } from 'ai';2
3const { videos } = await generateVideo({4  model: 'bytedance/seedance-2.0',5  prompt: {6    image: catImageUrl,7    text: 'The cat is celebrating a birthday with another cat.',8  },9  duration: 10,10  providerOptions: {11    bytedance: { generateAudio: true },12  },13});
```

**参考生视频**

使用图像、视频或音频参考作为源材料生成视频。您可以在单次生成中组合多种参考类型，以控制视觉风格、运动和声音。

```
1import { experimental_generateVideo as generateVideo } from 'ai';2
3const { videos } = await generateVideo({4  model: 'bytedance/seedance-2.0',5  prompt: 'Replace the cat in [Video 1] with the lion from [Image 1].',6  duration: 10,7  providerOptions: {8    bytedance: {9      referenceImages: [Image 1],10      referenceVideos: [Video 1],11      generateAudio: true,12    },13  },14});
```

AI Gateway对视频生成不收取任何加价：Seedance 2.0和2.0 Fast的价格与直接使用字节跳动供应商相同。

了解更多关于AI Gateway的信息，查看AI Gateway模型排行榜，或在我们的模型游乐场中试用。

---

> 本文由AI自动翻译，原文链接：[Seedance 2.0 Video Generation on AI Gateway - Vercel – Vercel](https://vercel.com/changelog/seedance-2.0-video-now-available-on-ai-gateway)
> 
> 翻译时间：2026-04-19 04:50
