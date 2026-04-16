---
title: 微调MusicGen：15分钟定制任意风格音乐生成模型
title_original: Fine-tune MusicGen to generate music in any style – Replicate blog
date: '2023-10-13'
source: Replicate Blog
source_url: https://replicate.com/blog/fine-tune-musicgen
author: ''
summary: 本文介绍了如何通过Replicate平台微调Meta的MusicGen模型，使其能够生成特定风格的音乐，如16位游戏芯片音乐或合唱风格。流程由Jongmin
  Jung开发，基于AudioCraft框架，仅需9-10首曲目，在8x A40硬件上训练15分钟即可完成。文章详细说明了数据准备、自动标注、人声去除、模型选择等步骤，并提供了通过Replicate
  API或CLI启动训练的具体方法，使开发者能够轻松创建个性化的音乐生成模型。
categories:
- AI产品
tags:
- 音乐生成
- AI微调
- MusicGen
- Replicate
- AIGC
draft: false
translated_at: '2026-04-16T04:58:46.410820'
---

- Replicate
- Blog

# 微调 MusicGen 以生成任意风格的音乐

- fofr
- sakemin

如果你想生成特定风格的音乐，可以微调 MusicGen。无论是16位视频游戏芯片音乐，还是宁静的合唱风格。

使用8x A40（大显存）硬件进行完整模型训练仅需15分钟。你可以通过网页或云API运行微调后的模型，也可以下载微调后的模型权重用于其他场景。

该微调流程由Jongmin Jung（又名sake）开发。它基于Meta的AudioCraft及其内置训练器Dora。为简化训练过程，Sake加入了自动音频分块、自动标注和人声去除功能。训练后的模型还能生成超过30秒的音乐。

以下是合唱风格微调与16位视频游戏风格结合的示例（作为延续）：

您的浏览器不支持 video 标签。

## 准备音乐数据集

仅需少量曲目（9-10首）即可对MusicGen进行音乐风格微调。

每首曲目必须长于30秒。训练脚本会自动将长音频文件分割为30秒片段用于训练。

## 标注训练数据

你可以通过三种方式标注音乐：

1. 让训练脚本自动标注。将使用essentia生成流派、情绪、主题、乐器、调性和BPM信息，并应用于每个音频文件（此为默认方式）。
2. 使用`one_same_description`训练参数为所有曲目提供统一描述。此方式与自动标注协同工作，描述文本将添加在开头。
3. 为每个音频文件提供自定义描述。

若需使用自定义描述，必须为每个曲目创建同名文本文件。例如`01_A_Man_Without_Love.mp3`需对应`01_A_Man_Without_Love.txt`文件。每个文本文件内写入单行描述。

## 训练前去除人声

MusicGen对含人声的音乐处理效果不佳。基础模型完全不包含人声。若使用含歌唱或语音的曲目训练，会导致输出音效异常。默认情况下我们将去除音频文件中所有人声。

如果你的曲目不包含人声，或仍想尝试带人声训练，可通过在训练参数中设置`drop_vocals`为`false`来禁用此功能（详见下文）。

## 选择训练模型

你可以训练`small`、`medium`或`melody`模型。默认选择small模型。large模型不可训练。

如果选择small或medium模型，可通过自动延续生成超过30秒的音乐。melody模型限制为30秒。

melody模型支持基于输入旋律生成音乐。此功能仅在你选择训练melody基础模型时，才会在微调模型中可用。

## 添加Replicate API Token

开始训练任务前，需从replicate.com/account/api-tokens获取Replicate API token。

在终端中，将该token存储到名为`REPLICATE_API_TOKEN`的环境变量：

```
export REPLICATE_API_TOKEN=r8_...
```

## 创建模型

你还需要在Replicate上创建一个模型，作为训练后MusicGen版本的存储位置。访问replicate.com/create创建模型。

下例中我们将其命名为`my-name/my-model`。

## 上传训练数据

将曲目（及任何文本文件）放入文件夹并压缩为zip包。

如果使用Replicate CLI，可在训练命令中上传训练文件（见下文）。

否则需将zip文件上传至可公开访问的网络位置，如S3存储桶或GitHub Pages站点。

## 开始训练

要训练MusicGen，请在Python中运行以下命令：

```
import replicate

training = replicate.trainings.create(
    version="sakemin/musicgen-fine-tuner:8d02c56b9a3d69abd2f1d6cc1a65027de5bfef7f0d34bd23e0624ecabb65acac",
    input={
        "dataset_path": "https://my-domain/my-audio-files.zip",
    },
    destination="my-name/my-model"
)
```

如果Python不是你的首选语言，我们也支持其他多种语言。

若使用Replicate CLI，可通过以下命令上传本地数据集并开始训练：

```
replicate train sakemin/musicgen-fine-tuner \
  --destination my-name/my-model \
  dataset_path=@audio.zip
```

以上操作将使用默认参数训练small版MusicGen模型（训练参数详情见下文）。

## 监控训练进度

要跟踪训练任务进度，可访问replicate.com/trainings或通过代码检查：

```
training.reload()
print(training.status)
print("\n".join(training.logs.split("\n")[-10:]))
```

## 运行模型

模型训练完成后，可通过网页或API运行：

```
output = replicate.run(
    "my-name/my-model:abcde1234...",
    input={"prompt": "your new musical style"},
)
```

如果在训练时使用了自定义描述，请确保在提示词中复用这些描述。否则请使用最能描述新风格的提示词，或查看训练日志了解自动添加的标签。

例如，在我们的合唱微调中，使用了“sacred chamber choir, choral”描述。在提示词中复用该描述能清晰呈现风格。我们还发现仅使用部分训练描述（如‘choir’或‘choral’）可保持风格同时减弱效果强度。

至此，你已拥有无限生成个人风格音乐的生成器。

## 完整微调设置

MusicGen微调提供以下参数供你控制训练模型：

- `dataset_path`：指向zip或音频文件的URL
- `one_same_description`：所有音频数据的统一描述（默认：无）
- `auto_labeling`：为每首曲目创建流派、情绪、主题、乐器、调性、BPM等标签数据。使用essentia-tensorflow进行音乐信息检索（默认：true）
- `drop_vocals`：通过Demucs分离音源，从数据集的音频文件中去除人声轨（默认：true）
- `model_version`：要训练的模型版本，可选“melody”、“small”、“medium”（默认：“small”）
- `lr`：学习率（默认：1）
- `epochs`：训练轮数（默认：3）
- `updates_per_epoch`：单轮训练迭代次数（默认：100）。若设为None，每轮迭代次数将根据批次大小和数据集自动确定。
- `batch_size`：批次大小，必须为8的倍数（默认：16）

## 后续步骤

- 查看我们的微调示例：我们已训练了室内合唱音乐和视频游戏音乐模型。
- 探索Sakemin出色的musicgen-chord模型，该模型可基于音频和弦条件或文本和弦条件生成音乐。
- 在X和Discord上与社区分享你的微调成果。

---

> 本文由AI自动翻译，原文链接：[Fine-tune MusicGen to generate music in any style – Replicate blog](https://replicate.com/blog/fine-tune-musicgen)
> 
> 翻译时间：2026-04-16 04:58
