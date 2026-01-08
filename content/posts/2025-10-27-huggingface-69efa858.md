---
title: 流式数据集性能提升100倍：无需下载即可高效训练大模型
title_original: 'Streaming datasets: 100x More Efficient'
date: '2025-10-27'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/streaming-datasets
author: ''
summary: 本文介绍了Hugging Face团队对datasets库流式处理功能的重大优化。通过改进后端技术，将启动请求减少100倍，数据解析速度提升10倍，流式处理速度提升2倍，并支持256个并发worker稳定运行。用户只需在load_dataset中设置streaming=True，即可无需下载直接流式读取TB级数据集进行训练，解决了大规模机器学习工作流中的数据加载瓶颈问题。
categories:
- AI基础设施
tags:
- 流式处理
- 数据集
- 机器学习
- 性能优化
- Hugging Face
draft: false
translated_at: '2026-01-08T04:44:18.214613'
---

# 流式数据集：效率提升100倍

- 
- 
- 
- 
- 
- 
- +72

![](/images/posts/311db97fa420.jpg)

![](/images/posts/c09474ce9b79.jpg)

![](/images/posts/9bc3346835fd.jpg)

![](/images/posts/8c2942a398c6.jpg)

![](/images/posts/873cedd5987b.png)

![](/images/posts/ac0e506ba48d.jpg)

![Andres Marafioti 的头像](/images/posts/e8e9ef3ca440.jpg)

![Quentin Lhoest 的头像](/images/posts/873cedd5987b.png)

![ben burtenshaw 的头像](/images/posts/a81239c48d0a.png)

![Pedro Cuenca 的头像](/images/posts/5b36678ab3e8.jpg)

![merve 的头像](/images/posts/78bab46e000b.jpg)

## 太长不看版流式处理：同样简单的 API挑战：大规模流式处理技术内幕：我们改进了什么我们如何比普通 S3 更快：Xet需要自定义流式处理管道？将流式处理推向极限开始使用并见证差异

- 太长不看版
- 流式处理：同样简单的 API
- 挑战：大规模流式处理
- 技术内幕：我们改进了什么
- 我们如何比普通 S3 更快：Xet
- 需要自定义流式处理管道？
- 将流式处理推向极限
- 开始使用并见证差异

我们提升了 `load_dataset('dataset', streaming=True)` 的性能，只需一行代码即可流式读取数据集而无需下载！

立即开始训练多 TB 规模的数据集，无需复杂设置、无需下载、没有“磁盘空间不足”或 429 “停止请求！”错误。它超级快！在使用 256 个 worker 下载数据、在 64xH100 上训练时，速度甚至超过了我们的本地 SSD。
我们改进了流式处理，使其请求数减少了 100 倍 → 数据解析速度提升 10 倍 → 每秒样本数提升 2 倍 → 在 256 个并发 worker 下实现 0 崩溃。

![数据集流式处理的可视化](/images/posts/7efd1d20b955.gif)

加载数据，尤其是在 TB 级别，是任何机器学习工作流程中的主要痛点。我们在训练 SmolLM3 时就深受其苦，一度在每次运行前必须等待 3 小时来下载足够的数据。

在 `datasets` 库中，流式处理一直是可行的，但使用海量数据集进行大规模训练仍然是一个挑战。今天，这一切都改变了 🔥。我们花了几个月时间改进后端，专注于流式数据集，使其更快、更高效。

我们具体做了什么？⤵️

## 流式处理：同样简单的 API

首先，最重要的一点：我们的更改是向后兼容的。您仍然可以使用相同的简单 `streaming=True` 标志从 Hub 流式读取任何数据集。一如既往地简单。🚀

```
from datasets import load_dataset

# 流式读取数据集而不是下载它
dataset = load_dataset("HuggingFaceM4/FineVisionMax", split="train", streaming=True)
# 获取第一个样本
print(next(iter(dataset)))

```

全球成千上万的 AI 开发者每天都在使用 `datasets`；他们应该无需任何额外工作就能获得改进的性能。

## 挑战：大规模流式处理

流式处理曾是快速了解数据集的救命稻草，但要训练模型，人们通常会将数据下载到本地，或使用 S3 等云存储服务。这就是我们训练 SmolVLM 时所做的，我们将所有数据放在 S3 上并直接从中流式读取。

我们想改变这一点，因此在开发 nanoVLM 时，我们决定使用来自 Hub 的流式处理。很快我们发现了一个大问题：我们的测试运行在一分钟内产生了超过 100,000 个请求，导致我们的 IP 被 Hub 屏蔽了！😅 这是因为每个 DataLoader worker 都在独立初始化数据集。随着深入调查，我们发现这会产生大量冗余请求，其中许多是不必要的。我们的更改最终将启动请求减少了 100 倍。总体而言，我们的改进带来了：

- 数据文件解析时间：快 10 倍
- 启动请求：效率提升高达 100 倍
- 流式处理速度：快高达 2 倍
- 在途请求：效率提升高达 2 倍

## 技术内幕：我们改进了什么

那么，改变了什么呢？我们专注于两个阶段：启动和流式处理。

1.  启动 ⚡️
    数据文件的初始解析产生了大量请求。我们做了两项重大更改：

    *   持久化数据文件缓存：我们现在在所有 DataLoader worker 之间缓存数据文件列表。第一个 worker 从 Hub 解析文件列表。所有其他 worker 直接从本地缓存读取，几乎消除了启动请求并大幅缩短了解析时间。不再有请求风暴！
    *   优化的解析逻辑：我们还最小化了初始 worker 获取文件列表所需的 API 调用次数。我们现在尽可能高效地捆绑必要的请求，进一步减少了延迟。

2.  流式处理 🏎️
    为了改善流式处理本身的吞吐量，我们引入了两个新功能：

    *   Parquet 预取：我们为 Parquet 数据集启用了预取。这意味着当您的模型正在处理当前数据块时，datasets 库已经在后台获取下一个数据块。这使数据管道保持充盈，并确保您的 GPU 永远不会等待数据。
    *   可配置的缓冲：高级用户现在可以针对其特定的硬件和网络设置微调流式处理性能。我们提供了配置缓冲区块大小和预取量的选项，让您拥有最大控制权来优化 I/O。

这就是我们如何将流式处理时的最小请求大小从 32MiB（默认）增加到 128MiB 并配置预取的方法：

```
import pyarrow
import pyarrow.dataset

fragment_scan_options = pyarrow.dataset.ParquetFragmentScanOptions(
    cache_options=pyarrow.CacheOptions(
        prefetch_limit=1,
        range_size_limit=128 << 20
    ),
)
ds = load_dataset(parquet_dataset_id, streaming=True, fragment_scan_options=fragment_scan_options)

```

这些改进共同作用，可以将您的数据吞吐量提高一倍，让您更快、更高效地进行训练。

## 我们如何比普通 S3 更快：Xet

Hugging Face 使用 Xet：一种基于去重的存储，可实现快速去重上传和下载。与传统远程存储不同，Xet 上的数据传输更快，因为重复数据只传输一次。例如：将大规模数据集上传到 Hugging Face 利用了 Xet，从而加速了上传。数据集上传后，可以立即进行流式读取。

Parquet 的去重是通过 **Parquet 内容定义分块 (CDC)** 实现的。得益于 Parquet CDC 和 Xet 去重，在 Hugging Face 上上传数据集比在任何传统远程存储上都要快。

这得到了我们的 `pyspark_huggingface` 包的支持，这是一个用于读写 HF 数据集的 Spark 数据源。它包含 Parquet CDC 和 Xet 支持，极大地加速了 HF 上的数据传输。

## 需要自定义流式处理管道？

有些数据文件格式在 `datasets` 中不受支持，有时需要更多控制，因此我们简化了构建自定义流式处理管道的流程。这已在 LeRobot 库中用于采样视频帧，并在 WebDataset 库中用于流式读取 TAR 归档文件，经过了实战检验。

我们改进了 `huggingface_hub` 库中的 `HfFileSystem`，以高效地从远程 Hugging Face 数据集仓库读取文件并流式传输数据：

```
from huggingface_hub import HfFileSystem

path = f"hf://datasets/{dataset_id}/{path_in_repo}"
with HfFileSystem().open(path) as f:
    # 使用 .read() 或 .readline() 循环以流式传输数据
    # 或使用 .seek() 进行随机访问

```

将 `HfFileSystem` 传递给 torch DataLoader 会重用 `.ls()` 和 `.glob()` 的缓存结果，从而在列出数据文件时无需额外请求。

## 将流式处理推向极限

我们现在正在 nanoVLM 中使用这些流式处理增强功能来训练下一代 SmolVLM。通过这些调整，我们从流式处理中获得的性能比从集群分层硬盘设置中训练更好。事实上，流式处理现在与从本地 SSD 读取数据一样快！以前，将数据传输到本地 SSD 的过程常常使我们的训练延迟三个小时。更多详情，请查看我们的 GitHub。

## 开始使用并见证差异

这些强大的新功能已集成到 datasets 和 huggingface_hub 库中。要使用它们，只需更新您的库并查阅文档：

```
pip install --upgrade datasets huggingface_hub

```

为此，我们已将 FineVision 中的所有数据源预拼接并打乱，整合为 FineVisionMax。您可以使用这个单一的合并数据集来训练您的 VLM（视觉语言模型）——无需再手动处理多个数据集！

```
from datasets import load_dataset

# 以流式传输方式加载数据集，而非下载
dataset = load_dataset("HuggingFaceM4/FineVisionMax", split="train", streaming=True)
# 获取第一个样本
print(next(iter(dataset)))

```

您可以在 nanoVLM 中了解我们是如何大规模实现这一点的！

更多博客文章

![](/images/posts/1d688356f6c4.png)

## Parquet 内容定义分块

- 
- 

![](/images/posts/24951cefc36b.jpg)

![](/images/posts/635a8de1f1e5.png)

## 改进 Hugging Face Hub 上的 Parquet 去重

- 
- 
- 

![](/images/posts/abf50b75cd8b.jpg)

![](/images/posts/9ca93e40d5c6.jpg)

![](/images/posts/287c63ff9896.jpg)

![](/images/posts/1234e43cabb1.png)

流式传输始终是正确选择，因为神经网络的训练通常都是有状态的🚀

![](/images/posts/8c2942a398c6.jpg)

大家好，有个小问题：

流式传输适合以下场景吗：我的存储空间有限（比如 < 100GB）。训练数据集大约有 1T 的 token（实际存储占用 6TB）。

已经“流式传输”的数据集会存储在磁盘上，还是在一个分块/parquet 文件完成训练步骤后被删除？我想避免在训练过程中本地磁盘被填满的情况，因为我本地空间有限。

- 
- 1 条回复

![](/images/posts/1234e43cabb1.png)

![](/images/posts/1234e43cabb1.png)

是的，直接用流式传输，在你的情况下这根本无需犹豫，完全不会填满你的磁盘。只需确保你的网络基础设施足够快。

为了明确理解，你是将 Parquet 数据集（我确实需要把它存储在某个地方，而 Parquet 在 Hub 上已优化）上传到这里的 Hub，然后在保持稳定网络连接的情况下使用流式传输功能，对吗？

- 
- 1 条回复

![](/images/posts/ed23d04248c4.jpg)

![](/images/posts/ed23d04248c4.jpg)

是的！要获取已为流式传输优化好的 Parquet 文件，最简单的方法可能是使用 `datasets.Dataset` 的 `push_to_hub` 方法 (https://huggingface.co/docs/datasets/main/en/package_reference/main_classes#datasets.DatasetDict.push_to_hub)。

· 注册或登录以发表评论

- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- 
- +66

![](/images/posts/311db97fa420.jpg)

![](/images/posts/c09474ce9b79.jpg)

![](/images/posts/9bc3346835fd.jpg)

![](/images/posts/8c2942a398c6.jpg)

![](/images/posts/873cedd5987b.png)

![](/images/posts/ac0e506ba48d.jpg)

![](/images/posts/0936a580b0bb.jpg)

![](/images/posts/77fca4f86e60.jpg)

![](/images/posts/ed23d04248c4.jpg)

![](/images/posts/5b36678ab3e8.jpg)

![](/images/posts/e92f7a1e8d97.jpg)

![](/images/posts/6143f375a98f.jpg)

---

> 本文由AI自动翻译，原文链接：[Streaming datasets: 100x More Efficient](https://huggingface.co/blog/streaming-datasets)
> 
> 翻译时间：2026-01-08 04:44
