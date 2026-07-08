---
title: SkyPilot携手Hugging Face实现零出站数据存储
title_original: 'Run AI workloads on any cloud, store on Hugging Face: zero-egress
  storage with SkyPilot'
date: '2026-07-07'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/skypilot-hf-storage
author: ''
summary: SkyPilot与Hugging Face合作，推出零出站存储功能，允许用户在任何云服务商的GPU上运行AI工作负载，同时将模型和数据集存储在Hugging
  Face Hub上。通过hf://URL和HF_TOKEN，用户可直接挂载Hub仓库到SkyPilot任务中，无需支付跨云数据传输费用。该功能基于Xet去重技术，支持增量存储，并已集成到SkyPilot的一等后端中，支持MOUNT和COPY模式，实现高效、低成本的数据访问。
categories:
- AI基础设施
tags:
- SkyPilot
- Hugging Face
- 零出站存储
- 跨云AI工作负载
- 数据挂载
draft: false
translated_at: '2026-07-08T05:23:38.030856'
---

# 在任何云上运行AI工作负载，在Hugging Face上存储：SkyPilot实现零出站存储

对大多数团队而言，模型和数据集都存放在某个云服务商某个区域的一个存储桶中。无论是用于开发、训练还是推理，你能获取到的GPU越来越多地分布在与你数据不同的云服务商上。当这两者分离时，你仅仅为了将自己的数据读取到自己的GPU上，就需要支付跨云数据传输费用。

我们与Hugging Face合作，将这两部分连接起来：你的模型和数据集保留在Hub上，而SkyPilot则在任何拥有GPU的集群上运行计算任务（开发、训练或推理）。通过一个`hf://`URL和你已有的`HF_TOKEN`，将Hugging Face Bucket或任何Hub仓库挂载到SkyPilot任务中，然后即可在任何有容量的地方启动它。Hugging Face不收取出站费用，因此在任何云服务商上，将数据读取到这些GPU上都是免费的。

以下是新功能：

- **在任何任务中访问你的Hub数据。** `store: hf`通过一个`hf://`URL和你现有的`HF_TOKEN`，以`MOUNT`或`COPY`模式，将Hugging Face Bucket（读写）或任何模型/数据集/Space仓库（只读）挂载到SkyPilot任务中。
- **在任何云服务商的任何GPU上运行。** SkyPilot在20多个云服务商、Kubernetes、Slurm以及本地环境中寻找任务计算资源，因此同一个运行任务可以使用你预留或按需的任何GPU，无论供应商是谁。
- **读取数据无出站费用。** Hugging Face Storage不收取出站或CDN费用，因此无论SkyPilot将任务部署在哪里，它都直接从同一个存储桶中读取你的模型和数据集，无需为每个云服务商复制数据，也无需为拉取数据支付出站账单。
- **基于Xet的去重。** Buckets构建在Xet之上，因此增量检查点和模型变体仅存储和传输发生变化的块。
- **共同构建。** Hugging Face和SkyPilot联合发布了此功能，Hugging Face团队上游了`hf-mount` FUSE修复程序，使其能在非特权容器中工作。

## Hugging Face Storage现已成为SkyPilot的一等后端

SkyPilot任务已经可以通过将云对象存储（S3、GCS、Azure、R2等）挂载到本地路径来读写它们。Hugging Face Storage现在也加入了这一行列，作为`store: hf`，通过`hf://`方案访问：

```yaml
file_mounts:
  
  /checkpoints:
    source: hf://buckets/my-org/qwen-sft
    store: hf
    mode: MOUNT 
  
  /base-model:
    source: hf://Qwen/Qwen3.5-4B
    store: hf
    mode: MOUNT
  
  /data:
    source: hf://datasets/my-org/my-dataset@main
    store: hf
    mode: MOUNT

```

这一个`hf://`方案覆盖了整个生命周期：从仓库中读取模型和数据集，在训练时将检查点写入Bucket，将完成的模型发布回仓库，并在推理时将其拉取到推理服务器上。大多数团队已经将他们的模型和数据集保存在Hub上，因此无需迁移步骤，也无需创建新的存储账户。

`MOUNT`使用Hugging Face的`hf-mount` FUSE后端，因此存储桶或仓库会作为本地路径出现在SkyPilot的其他FUSE挂载（gcsfuse、blobfuse2、rclone、goofys）旁边。数据获取发生在文件系统层：当你的代码发出`read()`时，驱动程序仅从Xet后端拉取那些字节，因此只有你实际访问的数据会通过网络传输，并且`hf-mount`会保留一个磁盘缓存，以便重复读取时保持本地访问。这个磁盘缓存是SkyPilot在其`MOUNT_CACHED`模式下赋予其他后端的行为，而普通的`MOUNT`则每次从存储桶流式读取，不保留任何本地数据。对于`hf`存储，`MOUNT`和`MOUNT_CACHED`行为相同，因此两种模式都会保留缓存。

由于读取是惰性的，进程可以在整个大文件下载完成之前就开始处理它，而无需等待完整副本先下载完毕。这使得GPU几乎可以立即投入工作，在数据流式传入时进行训练，而不是在数据集或检查点下载时闲置（并产生费用）。这在第一个epoch时效果最为显著，因为此时还没有任何缓存。`COPY`则采用另一种方式，通过`huggingface_hub`预先下载，没有特殊要求。

身份验证使用你已有的令牌。在你的环境中设置`HF_TOKEN`，并通过`--secret HF_TOKEN`将其传递给运行任务；SkyPilot在任务所在的任何云服务商上使用它进行挂载。无论任务落在AWS、GCP、Azure、Nebius、Lambda还是你自己的Kubernetes集群上，一个令牌即可生效，因此无需为每个云服务商管理不同的存储桶密钥。

## 无出站费用：存储不再决定你的运行地点

GPU容量很少再来自单一来源。为了获得足够的H100和H200，团队同时在多个供应商处持有预留和承诺容量（超大规模云服务商的一个区块、新型云服务商的一个集群，或许还有本地机架），并在有分配的地方运行。SkyPilot正是为此而构建：一个任务规范，在20多个云服务商、Kubernetes和本地环境中调度，落在任何空闲的预留集群上。

对象存储一直是症结所在。对象存储是区域性的且按云服务商划分，因此为位于不同供应商数据中心的GPU或推理服务器提供数据，意味着要么在每个供应商的存储桶中保留一份数据副本，要么付费将其拉取过来。大多数云服务商在数据离开其网络时收取出站费用（AWS约为0.09美元/GB），并且通常在单个云服务商的不同区域之间也收费。将基础模型拉取到每个推理节点，或从另一个云服务商的集群上迭代数据集多个epoch，会在你已经预留的GPU之上增加一笔巨额账单。团队最终将每个运行任务固定在持有数据的供应商上，而让其余容量闲置。

Hugging Face Storage消除了这个痛点：读取端。由于没有出站或CDN费用，且存储价格为12-18美元/TB/月（而AWS S3约为23美元/TB加上出站费用），同一个存储桶可以从所有这些集群访问，无论GPU在哪里运行，读取都是免费的。写回仍然需要支付你的计算云服务商的常规出站费用，与任何非云存储相同，但对于大多数AI工作来说，读取占主导地位：跨多个epoch流式传输的数据集，或拉取到每个新训练或推理节点的模型权重。因此，你不再需要将每个运行任务固定在持有数据副本的供应商上。

## 快速基准测试

为了收集一些基准数据，我们运行了一个小型微调任务：使用TRL的SFTTrainer在HuggingFaceH4/Multilingual-Thinking数据集上微调Qwen/Qwen3.5-4B，将模型从其Hub仓库以只读方式挂载，并将每个检查点写入Hugging Face Bucket。同一个SkyPilot YAML在AWS、GCP和Lambda上运行，仅更改了`--infra`。SkyPilot将每个任务放置在GPU空闲的地方，所有三个任务都读写同一个存储桶。

```yaml

resources:
  accelerators: H100:1 

file_mounts:
  /base-model:
    source: hf://Qwen/Qwen3.5-4B 
    store: hf
    mode: MOUNT
  /checkpoints:
    source: hf://buckets/my-org/qwen-sft 
    store: hf
    mode: MOUNT

run: |
  python train.py --model /base-model --output_dir /checkpoints

```

我们测量的结果：

- **模型在每个云服务商上免费加载。** 惰性读取仅拉取`from_pretrained`访问的内容，因此大约30秒即可准备就绪（速度高达500 MB/s）。由于Hugging Face不收取出站费用，这次拉取没有成本；如果模型存放在S3中，每次从另一个云服务商读取到GPU都将产生出站费用（AWS上为0.09美元/GB）。
- **检查点直接流式传输到存储桶**，速度高达约170 MB/s（每个权重文件8.43 GB），并在GPU实例终止后持久保存。

按云服务商划分，检查点写入存储桶的速度为：

## 基于Xet的存储：检查点和模型变体的去重

Hugging Face Buckets构建在Xet之上，它使用内容定义的块划分将文件分割成约64 KB的块，并仅存储每个唯一块一次。由于边界跟随内容变化，编辑仅更改其触及的块，其余块被识别为已存储。这在几个方面带来了好处：

- **增量检查点与适配器检查点**：当冻结层、训练适配器或在保存之间保留大部分权重不变时，仅上传发生变更的数据块，而非整个检查点。
- **共享基础模型的变体**：同一基础模型的微调版本与量化版本存在大量重叠，因此共享的数据块在所有版本中仅存储一次。
- **追加数据集**：对话记录或推理输出等日志通过向大型 Parquet 文件追加行来增长。现有行组保持字节级一致，因此仅传输新增行：在 Hugging Face 的测试中，向一个 10 万行的表追加 1 万行仅传输约 10 MB，而非完整的约 106 MB。（若原地编辑或删除行，请使用 `use_content_defined_chunking=True` 保持变更局部化。）
- **重复上传跳过已存储内容**：在我们的测试中，重新上传存储桶中已有的 8.43 GB 数据块仅需约 8 秒，而首次上传需 24 秒，因为仅传输数据块哈希值。同一机制使服务端 `hf buckets cp` 命令在仓库与存储桶之间通过引用复制，而非重新传输字节。

实际节省量取决于工件重叠程度，但去重是自动完成的：照常写入检查点，仅新数据块会离开机器。

## 开始使用

```bash
pip install "skypilot[huggingface]"
hf auth login  

```

向任意 SkyPilot 任务添加 `hf://` 挂载点并启动。`MOUNT` 需要基于 glibc 2.34+ 和 `/dev/fuse` 的基础镜像。

## 共同构建：Hugging Face 与 SkyPilot

最初的 `store: hf` 支持由 Nikhil Jha 贡献。Hugging Face 团队持续推进，并上游了 `hf-mount` 的 FUSE 修复，使其能在非特权容器（许多 Kubernetes 集群的默认配置）中挂载。SkyPilot 团队将其集成至存储后端。整个链路均为开源：SkyPilot、Hugging Face 的 `hf-mount` 以及 `huggingface_hub` 客户端。

## 资源

- SkyPilot 存储文档
- Hugging Face 存储桶指南
- hf-mount
- Xet：内容定义分块与去重
- SkyPilot Slack 社区

---

> 本文由AI自动翻译，原文链接：[Run AI workloads on any cloud, store on Hugging Face: zero-egress storage with SkyPilot](https://huggingface.co/blog/skypilot-hf-storage)
> 
> 翻译时间：2026-07-08 05:23
