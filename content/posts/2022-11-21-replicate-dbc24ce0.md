---
title: 在Replicate上训练并部署DreamBooth模型
title_original: Train and deploy a DreamBooth model on Replicate – Replicate blog
date: '2022-11-21'
source: Replicate Blog
source_url: https://replicate.com/blog/dreambooth-api
author: ''
summary: 本文介绍了如何在Replicate平台上使用DreamBooth API训练和部署个性化Stable Diffusion模型。用户只需提供最少三张图片，约20分钟即可完成训练，成本约2.50美元。文章详细说明了从获取API
  Token、上传训练数据到启动训练任务的完整流程，并强调了DreamBooth适用于人物、风格等特定对象的生成。同时，文章提及2023年8月已支持SDXL微调，可获得更高分辨率效果。
categories:
- AI产品
tags:
- DreamBooth
- Stable Diffusion
- 模型训练
- Replicate
- AI部署
draft: false
translated_at: '2026-06-03T06:52:27.309516'
---

- Replicate
- 博客

# 在 Replicate 上训练并部署 DreamBooth 模型

- bfirsh
- zeke

2024年8月更新：实验性的 DreamBooth API 已不再可用。请查看 FLUX.1 微调博客文章，了解效果更佳的替代方案。

2023年8月更新：我们已为 SDXL（最新版 Stable Diffusion）添加了微调支持。下文描述的 DreamBooth API 仍然可用，但使用 SDXL 能以更高分辨率获得更优效果。请查看 SDXL 微调博客文章开始使用，或继续阅读以使用旧的 DreamBooth API。

生成式 AI 因 DreamBooth 而备受关注。这是一种针对特定对象或风格训练 Stable Diffusion 的方法，可创建能生成这些对象或风格的专属模型版本。只需最少三张图片即可训练模型，训练过程不到半小时。

值得注意的是，DreamBooth 适用于人物，因此你可以制作一个能生成自己图像的 Stable Diffusion 版本。

![](/images/posts/684b1e342512.webp)

人们已用 DreamBooth 打造出一些神奇的产品，例如 Avatar AI 和 ProfilePicture.AI。

现在，你也可以用 DreamBooth 创建自己的项目。我们构建了一个 API，让你能在云端训练 DreamBooth 模型并运行推理。

你只需最少三张训练图片，大约需要 20 分钟（取决于使用的迭代次数）。训练一个模型大约花费 2.50 美元。

## 训练 DreamBooth 模型

首先，获取你的 API Token 并在终端中设置：

export REPLICATE_API_TOKEN=…

接下来，将训练数据整理为 data/ 目录下的一组 JPEG 文件，并压缩为 zip 包：

zip -r data.zip data

将此 zip 文件放在可通过 HTTP 访问的位置。如果你愿意，可以使用我们的 API 上传文件。运行以下三个命令：

```

    RESPONSE=$(curl -X POST -H "Authorization: Bearer $REPLICATE_API_TOKEN" https://dreambooth-api-experimental.replicate.com/v1/upload/data.zip)

    curl -X PUT -H "Content-Type: application/zip" --upload-file data.zip "$(jq -r ".upload_url" <<< "$RESPONSE")"

    SERVING_URL=$(jq -r ".serving_url" <<< $RESPONSE)
```

然后，启动训练任务：

```
    curl -X POST \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
        -d '{
                "input": {
                    "instance_prompt": "a photo of a cjw person",
                    "class_prompt": "a photo of a person",
                    "instance_data": "'"$SERVING_URL"'",
                    "max_train_steps": 2000
                },
                "model": "yourusername/yourmodel",
                "trainer_version": "cd3f925f7ab21afaef7d45224790eedbb837eeac40d22e8fefe015489ab644aa",
                "webhook_completed": "https://example.com/dreambooth-webhook"
            }' \
        https://dreambooth-api-experimental.replicate.com/v1/trainings
```

你需要设置：

- instance_prompt：用于描述训练图片的提示词，格式为 [标识符] [类别名词]，其中标识符是某个稀有 Token。在上例中，我们使用 cjw，但你可以使用任何喜欢的字符串。为获得最佳效果，请使用包含三个 Unicode 字符且不含空格的标识符。
- class_prompt：训练图片所属更广泛类别的提示词，格式为 [类别名词]。用于生成与训练数据类似的其他图片，以避免过拟合。
- instance_data：训练数据的 URL。
- max_train_steps：运行的训练步数。步数越少运行越快，但通常质量越差，反之亦然。
- model：在 Replicate 上为模型指定的名称，格式为 username/modelname。例如 bfirsh/bfirshbooth。如果模型尚不存在，Replicate 会自动创建。
- trainer_version：要使用的 DreamBooth 和 Stable Diffusion 版本。更多详情请参见下方“版本”部分。
- webhook_completed：任务完成时调用的 Webhook。（可选。）

在后台，这会运行 replicate/dreambooth 模型。该模型的任何输入都可以传递到 input 对象中。

API 返回以下对象：

```
{
  "id": "rrr4z55ocneqzikepnug6xezpe",
  "input": {
    "instance_prompt": "photo of a cjw person",
    "class_prompt": "photo of a person",
    "instance_data": "https://replicate.delivery/pbxt/HoUeWsrtTTCJEpKGdLKqIYTfo8nbUTSNs565MkGxEstjfwKt/data.zip",
    "max_train_steps": 2000
  },
  "model": "yourusername/yourmodel",
  "status": "starting",
  "trainer_version": "cd3f925f7ab21afaef7d45224790eedbb837eeac40d22e8fefe015489ab644aa",
  "webhook_completed": "https://example.com/dreambooth-webhook"
}
```

你可以通过调用 GET /v1/trainings/<id> 获取训练任务的状态：

```
    curl -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
      https://dreambooth-api-experimental.replicate.com/v1/trainings/rrr4z55ocneqzikepnug6xezpe
```

它返回相同的对象：

```
{
  "id": "rrr4z55ocneqzikepnug6xezpe",
  "input": {
    "instance_prompt": "photo of a cjw person",
    "class_prompt": "photo of a person",
    "instance_data": "https://replicate.delivery/pbxt/HoUeWsrtTTCJEpKGdLKqIYTfo8nbUTSNs565MkGxEstjfwKt/data.zip",
    "max_train_steps": 2000
  },
  "model": "yourusername/yourmodel",
  "status": "succeeded",
  "trainer_version": "cd3f925f7ab21afaef7d45224790eedbb837eeac40d22e8fefe015489ab644aa",
  "webhook_completed": "https://example.com/dreambooth-webhook",
  "version": "8abccf52e7cba9f6e82317253f4a3549082e966db5584e92c808ece132037776"
}
```

这与发送到 Webhook 的对象相同。

## 运行训练好的模型

训练过程成功完成后，模型会被推送到 Replicate。

你可以像使用 Replicate 上的任何其他模型一样，通过网站或 API 运行该模型。

要在网站上运行，请前往你的仪表盘，然后点击“模型”。

你的新模型默认是私有的，仅对你可见。如果你希望任何人都能查看和运行你的模型，可以在模型页面的“设置”选项卡中将其设为公开。

要将模型作为 API 运行，首先需要获取版本 ID。这可以在模型页面的“API”选项卡中找到，或者来自训练 API 响应中的 version 字段。

然后，你可以进行 API 调用：

```
    curl -X POST \
        -H "Authorization: Bearer $REPLICATE_API_TOKEN" \
        -d '{
                "input": {
                    "prompt": "painting of cjw by andy warhol",
                },
                "version": "8abccf52e7cba9f6e82317253f4a3549082e966db5584e92c808ece132037776",
            }' \
        https://api.replicate.com/v1/predictions
```

或者使用 Python：

```
import replicate
replicate.run(
    "yourusername/yourmodel:8abccf52e7cba9f6e82317253f4a3549082e966db5584e92c808ece132037776",
    input={"prompt": "painting of cjw by andy warhol"},
)
```

要了解更多关于在 Replicate 上运行模型的信息，请查看 Python 入门指南或 HTTP API 参考。

## 版本

默认情况下，DreamBooth 训练的是 Stable Diffusion 1.5 模型。该模型通常更适合 DreamBooth，因为它包含更多不同的风格。

如果你想使用其他版本，可以通过 trainer_version 选项选择不同版本。以下是支持的版本：

- Stable Diffusion 1.5：cd3f925f7ab21afaef7d45224790eedbb837eeac40d22e8fefe015489ab644aa
- 自定义检查点：9c41656f8ae2e3d2af4c1b46913d7467cd891f2c1c5f3d97f1142e876e63ed7a
- Stable Diffusion 2.1-base：d5e058608f43886b9620a8fbb1501853b8cbae4f45c857a014011c86ee614ffb

要查找其他可用版本，请查看 DreamBooth 训练器的发布说明。

## 下一步

如果你对此有任何疑问，请加入我们的 Discord 上的 #dreambooth 频道。

祝训练愉快！🚂

---

> 本文由AI自动翻译，原文链接：[Train and deploy a DreamBooth model on Replicate – Replicate blog](https://replicate.com/blog/dreambooth-api)
> 
> 翻译时间：2026-06-03 06:52
