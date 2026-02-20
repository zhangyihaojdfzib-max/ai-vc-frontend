---
title: Easel AI两款模型登陆Replicate平台：高级换脸与AI头像
title_original: Easel AI is now on Replicate – Replicate blog
date: '2025-04-16'
source: Replicate Blog
source_url: https://replicate.com/blog/easel
author: ''
summary: 本文宣布Easel AI的两款新模型——高级换脸和AI头像——正式在Replicate平台上线。高级换脸模型不仅能替换面部，还能替换全身，同时保留用户的肤色、种族特征和性别，并维持原始图像的服装、光线和风格，适用于营销、个性化内容及社交应用。AI头像模型则无需LoRA训练，仅凭提示词即可快速生成单人或多人的头像，为消息应用、交友应用和AI机器人等场景提供便利。文章还提供了两款模型的API调用示例。
categories:
- AI产品
tags:
- Replicate
- Easel AI
- AI头像生成
- 人脸替换
- AI模型平台
draft: false
translated_at: '2026-02-20T04:35:53.117818'
---

-   Replicate
-   博客

# Easel AI 现已登陆 Replicate

-   pranavsekhar

Easel AI 的两款新模型现已登陆 Replicate 平台：**高级换脸**和**AI 头像**。两款模型都快速、灵活，专为在消息、社交和创意类应用中进行生产级使用而设计。

![Easel1](/images/posts/48152a4f535a.webp)

## 高级换脸

Easel AI 的高级换脸不仅能替换面部，还能替换全身，同时保留用户的样貌特征——包括肤色、种族特征和性别。它保持原始图像的服装、光线和风格，从而获得自然的效果。以下是一些亮点。

-   可替换单张图像中的一人或两人
-   保持种族身份、肤色和身体特征
-   使用多人换脸时自动检测性别
-   保留服装、美学风格和图像细节
-   包含内置放大功能，以获得更高质量的输出

![Easel2](/images/posts/364c6cb54914.webp)

这解锁了以下应用场景：

-   **营销活动**：让用户在海报、广告或活动中看到自己，以便在社交媒体上分享
-   **个性化内容**：利用用户自拍，为贺卡、AI 故事书等提供支持
-   **社交和图像类应用**：使表情包、体育或交友类应用能够大规模地个性化图像

![Easel3](/images/posts/a44b545a48c0.webp)

点击此处运行该模型，或使用 Replicate JavaScript 客户端通过 API 运行。

```
import Replicate from "replicate";
const replicate = new Replicate();

const input = {
    swap_image: "https://replicate.delivery/pbxt/Mb44Wp0W7Xfa1Pp91zcxDzSSQQz8GusUmXQXi3GGzRxDvoCI/0_1.webp",
    hair_source: "target",
    target_image: "https://replicate.delivery/pbxt/Mb44XIUHkUrmyyH1OP5K1WmFN7SNN0eUSU16A8rBtuXe7eYV/cyberpunk_80s_example.png"
};

const output = await replicate.run("easel/advanced-face-swap", { input });

import { writeFile } from "node:fs/promises";
await writeFile("output.jpg", output);
//=> output.jpg written to disk
```

## AI 头像，无需 LoRA

创建 AI 头像通常需要上传多张图像并管理 LoRA。Easel AI 的模型省去了这一步。他们的新模型仅需一个提示词即可生成头像——无需训练或模板。Easel 的 AI 头像模型支持单人和多人模式，允许您在同一场景中生成一个或两个人物。

![Easel4](/images/posts/418021b2a110.webp)

快速头像生成为新应用解锁了可能：

-   **消息应用**：让用户创建头像，单独或与朋友一起表达自我
-   **交友应用**：展示情侣可能在一起的样子，以引发对话
-   **AI 机器人**：赋予机器人视觉形象，以加深用户参与度
-   **网红/影响者**：快速为社交帖子和营销活动生成品牌内容

![Easel5](/images/posts/7be059868188.webp)

点击此处运行该模型，或通过 API 运行。

```
import Replicate from "replicate";
const replicate = new Replicate();

const input = {
    prompt: "a guy riding a motorbike",
    face_image: "https://replicate.delivery/pbxt/MlYeEa5wsgHEWcw9jVYmFXGJQAsZia8polOhuLvjUtKlnSrt/guy.webp",
    user_gender: "male"
};

const output = await replicate.run("easel/ai-avatars", { input });

import { writeFile } from "node:fs/promises";
await writeFile("output.jpg", output);
//=> output.jpg written to disk
```

访问 easelai.com 了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Easel AI is now on Replicate – Replicate blog](https://replicate.com/blog/easel)
> 
> 翻译时间：2026-02-20 04:35
