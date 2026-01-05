---
title: Cloudflare与Black Forest Labs合作，在Workers AI上推出FLUX.2开发版
title_original: Partnering with Black Forest Labs to bring FLUX.2 -dev- to Cloudflare
  Workers AI
date: '2025-11-25'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/flux-2-workers-ai/
author: Michelle Chen
summary: Cloudflare宣布与Black Forest Labs合作，在其推理平台Workers AI上托管开源图像生成模型FLUX.2的开发版。该模型在FLUX.1基础上增强，能生成更真实、细节更精准的图像，支持多语言提示和多参考图像输入，有效解决角色一致性和随机漂移问题。FLUX.2特别擅长理解物理世界，生成逼真的光照、材质和空间感，适用于创意摄影、电商、营销设计等场景。
categories:
- AI产品
tags:
- 图像生成
- 开源模型
- Cloudflare Workers AI
- FLUX.2
- AI推理平台
draft: false
---

近几个月来，随着谷歌的Nano Banana和OpenAI图像生成模型的崛起，我们看到闭源图像生成模型取得了飞跃。今天，我们很高兴地分享，随着Black Forest Lab的FLUX.2 [dev]的发布，一位新的开源权重竞争者回归了，并且可以在Cloudflare的推理平台Workers AI上运行。您可以在BFL关于其新模型发布的博客文章中详细了解这个新模型。

自Black Forest Lab的FLUX图像模型最早版本以来，我们一直是其忠实粉丝。我们托管的FLUX.1 [schnell]版本因其逼真的输出和高保真度的生成效果，是我们目录中最受欢迎的模型之一。当有机会托管他们新模型的授权版本时，我们立刻抓住了这个机会。FLUX.2模型继承了FLUX.1的所有最佳特性并进行了增强，能够生成更加真实、基于现实的图像，并增加了如JSON提示词等自定义支持。

我们在Workers AI上托管的FLUX.2版本有一些特定的模式，例如使用多部分表单数据来支持输入图像（最多4张512x512图像），并输出高达400万像素的图像。多部分表单数据格式允许用户将多个图像输入与典型的模型参数一起发送给我们。请查看我们的开发者文档更新日志公告，了解如何使用FLUX.2模型。

**FLUX.2有何特别之处？物理世界基础、数字世界资产和多语言支持**

FLUX.2模型对物理世界有更深入的理解，使您能够将抽象概念转化为逼真的现实。它擅长生成逼真的图像细节，并能持续输出准确的手部、面部、织物、标识和小物体，而这些往往是其他模型容易忽略的。它对物理世界的理解还能生成逼真的光照、角度和深度感知。

图1. 使用FLUX.2生成的图像，展现了巴黎一家咖啡馆中准确的光照、阴影、反射和深度感知。

这种高保真度的输出使其非常适合需要卓越图像质量的应用，例如创意摄影、电子商务产品拍摄、营销视觉设计和室内设计。因为它能够理解上下文、色调和趋势，该模型允许您通过简短的提示词创建引人入胜且具有编辑质量的数字资产。

除了物理世界，该模型还能够生成高质量的数字资产，例如设计着陆页或生成详细的信息图（参见下面的示例）。它还能够自然地理解多种语言，因此结合这两个特性——我们可以从一个法语提示词中得到一个精美的法语着陆页。

> Générez une page web visuellement immersive pour un service de promenade de chiens. L'image principale doit dominer l'écran, montrant un chien exubérant courant dans un parc ensoleillé, avec des touches de vert vif (#2ECC71) intégrées subtilement dans le feuillage ou les accessoires du chien. Minimisez le texte pour un impact visuel maximal.

**角色一致性——解决随机漂移问题**

FLUX.2提供具有最先进角色一致性的多参考图像编辑功能，确保身份、产品和风格在任务中保持一致。在生成式AI领域，获得高质量图像很容易。然而，两次获得完全相同的角色或产品一直是难点。这种现象被称为"随机漂移"，即生成的图像逐渐偏离原始素材。

图2. 随机漂移信息图（在FLUX.2上生成）

FLUX.2的突破之一是其多参考图像输入功能，旨在解决这一一致性挑战。您将能够更改图像的背景、光照或姿势，而不会意外改变模特的面部或产品的设计。您还可以参考其他图像或将多个图像组合在一起以创建新内容。

在代码中，Workers AI通过多部分表单数据上传支持多参考图像（最多4张）。图像输入是二进制图像，输出是base64编码的图像：

```
curl --request POST \
--url 'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT}/ai/run/@cf/black-forest-labs/flux-2-dev' \
--header 'Authorization: Bearer {TOKEN}' \
--header 'Content-Type: multipart/form-data' \
--form 'prompt=take the subject of image 2 and style it like image 1' \
--form input_image_0=@/Users/johndoe/Desktop/icedoutkeanu.png \
--form input_image_1=@/Users/johndoe/Desktop/me.png \
--form steps=25
--form width=1024
--form height=1024
```

我们也通过Workers AI绑定支持此功能：

```
const image = await fetch("http://image-url");
const form = new FormData();
const image_blob = await streamToBlob(image.body, "image/png");
form.append('input_image_0', image_blob)
form.append('prompt', 'a sunset with the dog in the original image')
const resp = await env.AI.run("@cf/black-forest-labs/flux-2-dev", {
multipart: {
body: form,
contentType: "multipart/form-data"
}
})
```

**为真实世界用例而构建**

最新的图像模型标志着向功能性商业用例的转变，超越了简单的图像质量改进。FLUX.2使您能够：

*   **创建广告变体**：使用完全相同的演员生成50个不同的广告，而他们的面部不会在画面之间变形。
*   **信赖您的产品拍摄**：将您的产品放在模特身上，或放入海滩场景、城市街道或工作室桌面上。环境会改变，但您的产品保持准确。
*   **构建动态编辑内容**：制作完整的时尚大片，其中模特在每一个镜头中看起来都完全相同，无论角度如何。

图3. 将超大号连帽衫和运动裤广告照片（由FLUX.2生成）与Cloudflare的标识结合，创建具有一致面部、织物和场景的产品渲染图。

**注：我们同样要求使用白色的Cloudflare字体，而非原始的黑色字体。Â
精细控制——JSON提示、HEX代码及更多功能！**
FLUX.2模型实现了另一项进步，允许用户通过JSON提示和指定特定十六进制代码等工具来控制图像中的微小细节。
例如，您可以发送以下JSON作为提示词（作为multipart表单输入的一部分），生成的图像将严格遵循提示：

{
"scene": "一个外星星球上熙熙攘攘、霓虹闪烁的未来主义街头市场，雨水打湿了金属地面",
"subjects": [
{
"type": "赛博朋克赏金猎人",
"description": "女性，身着哑光黑色盔甲，带有发光的蓝色镶边，手持一把已失效的能量步枪，头盔夹在臂下，雨水从她的合成头发上滴落",
"pose": "以随意但警惕的姿态站立，微微倚靠在一个发光的售货摊上",
"position": "前景"
},
{
"type": "商贩机器人",
"description": "小型、生锈的三足无人机，带有多个闪烁的红色光学传感器，从其机身上附着的托盘售卖发光的合成水果",
"pose": "轻微悬浮，向观看者递出一件物品",
"position": "中景"
}
],
"style": "黑色科幻数字绘画",
"color_palette": [
"深靛蓝",
"电光蓝",
"酸绿色"
],
"lighting": "低调、戏剧性，主要光源来自霓虹灯招牌和街灯，在潮湿表面反射",
"mood": "粗粝、紧张、氛围感强",
"background": "高耸入云的黑暗摩天大楼消失在雾中，表面滚动着广告，远处可见飞行载具（旋翼车）",
"composition": "动态偏心构图",
"camera": {
"angle": "平视角度",
"distance": "中近景",
"focus": "主体清晰对焦",
"lens": "35mm",
"f-number": "f/1.4",
"ISO": 400
},
"effects": [
"大雨效果",
"细微胶片颗粒",
"霓虹灯光反射",
"轻微色差"
]
}

更进一步，我们可以通过提供特定的十六进制代码（如#F48120），要求模型将点缀性灯光重新着色为Cloudflare橙色。
最新的FLUX.2 [dev]模型现已在Workers AI上可用——您可以通过我们的开发者文档开始使用该模型，或在我们的多模态游乐场中进行测试。

---

> 本文由AI自动翻译，原文链接：[Partnering with Black Forest Labs to bring FLUX.2 -dev- to Cloudflare Workers AI](https://blog.cloudflare.com/flux-2-workers-ai/)
> 
> 翻译时间：2026-01-05 17:26
