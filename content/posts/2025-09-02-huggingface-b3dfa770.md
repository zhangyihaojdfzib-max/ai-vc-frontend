---
title: SAIR：AI结构智能数据库加速药物研发
title_original: 'SAIR: Accelerating Pharma R&D with AI-Powered Structural Intelligence'
date: '2025-09-02'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/SandboxAQ/sair-data-accelerating-drug-discovery-with-ai
author: ''
summary: SandboxAQ发布了开源数据集SAIR，包含超过500万个AI生成的蛋白质-配体3D结构及实验效力数据，旨在解决AI药物发现中高质量3D结构数据匮乏的瓶颈。该数据集通过高性能计算生成并经过严格验证，可显著加速从苗头化合物到先导化合物的优化进程，并为缺乏实验结构的“暗靶点”提供研究基础，有望将更多药物研发工作从实验室转移至计算机模拟。
categories:
- AI产品
tags:
- AI药物发现
- 蛋白质结构预测
- 计算化学
- 生物信息学
- 开源数据集
draft: false
translated_at: '2026-02-13T04:25:47.887492'
---

# SAIR：以AI驱动的结构智能加速药物研发

今年夏天，SandboxAQ发布了**结构增强IC50数据库**，这是目前最大的共折叠3D蛋白质-配体结构数据集，其中每个结构都配有实验测量的IC₅₀标签，直接将分子结构与药物效力联系起来，并克服了训练数据长期匮乏的难题。该数据集现已在Hugging Face上提供，研究人员首次可以公开访问超过**500万个**由AI生成的高精度蛋白质-配体3D结构，每个结构都配有经过验证的经验性结合效力数据。

![image/png](/images/posts/2d233497acc2.png)

SAIR是一个开源数据集，在宽松的CC BY 4.0许可下免费公开提供，可立即用于商业和非商业的研发流程。SAIR不仅仅是一个数据集，更是一项**战略资产**，它弥合了AI驱动药物设计中长期存在的数据鸿沟。它赋能制药、生物技术和科技生物领域的领导者，加速研发进程，拓展靶点视野，并增强AI模型的能力——将更多成本高昂、耗时漫长的药物设计与优化工作从湿实验室转移到**计算机模拟**中。这意味着从苗头化合物到先导化合物的时间线缩短，先导化合物优化更高效，失败项目减少，从最初构想到临床候选药物的路径更具可预测性。

# 跨越式超越AI成就

AI和计算机辅助设计在极大加速新药开发方面潜力巨大。几十年来，科学家们一直梦想着AI能够根据描述疾病通路的提示词，识别或设计出一种强效、无毒且高效的化合物，从而将数年的药物研发工作压缩到计算机上的几分钟内。然而，这一愿景受限于AI仅凭分子结构预测关键药物特性（如效力、毒性等）的能力。

此外，传统的基于结构的药物发现往往在早期就因获取可靠的3D结构而进展缓慢。三维分子结构决定了分子的功能、动力学和相互作用，当一种潜在的候选药物预期要与人体蛋白质靶点结合时，这一点尤为重要。

X射线晶体学和冷冻电镜等实验方法需要大量的时间和投入，许多有前景的疾病靶点仍然缺乏经过实验验证的结构信息。计算机模拟有助于降低获取3D结构和预测结合亲和力的门槛。然而，早期的蛋白质折叠和对接算法（例如AlphaFold和Vina）只能预测分子和蛋白质的静态快照（而实际上，它们本质上是动态且形状可变的）。

SAIR通过汇编超过**100万个**独特的计算共折叠蛋白质-配体对，最终产生**524万个**不同的3D复合物（每对生成五种不同的共折叠结构），从而解决了这一限制。每个结构都配有来自**ChEMBL**或**BindingDB**的精选IC₅₀测量值，首次提供了高质量3D结构与药物效力之间的可扩展联系，并弥合了阻碍AI驱动药物发现的历史数据鸿沟。基于类似数据训练的深度学习亲和力模型，如Boltz-2，**已被证明**相比传统的基于第一性原理的方法，能实现高达1000倍的加速。

# 为前沿计算优化而生

创建SAIR是高性能AI计算的一项重大壮举。我们使用共折叠AI模型Boltz1，在由760个NVIDIA H100处理器组成的集群上，通过Google Cloud Platform利用NVIDIA DGX Cloud，耗费了超过**13万GPU小时**来计算SAIR数据集。

通过捕获高度细粒度的节点、算子、调度器和GPU指标，以及在基础设施和工作负载优化方面的紧密合作，NVIDIA AI Accelerator和SandboxAQ工程团队得以识别瓶颈并优化配置，实现了最高的工作负载吞吐量。

因此，两个团队在生成SAIR数据集时实现了**> 95%** 的GPU计算利用率。这使得我们能够在三周内创建SAIR——而最初的估计是三个月（加速超过4倍）——并产生了一个高度优化、原生支持GPU的计算工作流，能够与当今尖端的企业计算环境无缝集成。

# 前所未有的规模、精度与能力

生成如此海量的数据只是故事的一半。对其质量的信心同样重要，这就是为什么每个预测的复合物都经过了**PoseBusters**的严格验证——这是一个用于药物发现中结构相关AI基准测试的行业标准开源工具。该工具检查化学合理性和物理可能性。

最终结果是，SAIR中**97%** 的结构通过了所有检查。除了PoseBusters验证外，我们还基于SAIR的合成结构和实验IC₅₀值，对主要的亲和力预测方法（如经验性评分函数、3D CNN和图神经网络）进行了基准测试。这些研究的详细结果可在我们在bioRxiv上的**科学手稿**中查阅。

SAIR数据是基准测试新模型以及进行下游建模、筛选和设计的可靠基础。

# 照亮“暗”靶点

药物发现中一个持续存在的挑战是“暗蛋白质组”，即那些根本没有实验结构的疾病相关蛋白质。SAIR通过在实验数据稀缺的地方提供可信的AI预测复合物，照亮了这些未知领域。例如，SAIR数据集中超过**40%** 的蛋白质在蛋白质数据库（PDB）中没有任何可用的结构（无论是否带有配体）。SAIR解决了现有AI模型最大的挑战之一：由于数据稀缺导致的低泛化能力。借助SAIR，科学家们现在可以探索以前被认为“不可成药”的靶点，利用结构假设来指导虚拟筛选和先导化合物优化，这一切都基于可信的模型预测。

此外，SAIR跨靶点的广度揭示了多药理学模式，并阐明了一个单一分子如何可能与多个蛋白质相互作用。利用这种丰富的相互作用网络，您可以训练AI模型来预测脱靶效应或识别新的药物再利用机会，从而在开始任何实验室工作之前，让您的组织对化合物特性有更深入的了解。

## 访问SAIR

SAIR可在**Hugging Face**上免费获取。以下是从Hugging Face拉取SAIR、查看主表以及（可选）下载部分结构存档的快速指南。

### 1. 安装必备工具

我们使用Hub来获取文件，并使用pandas+pyarrow来读取Parquet文件。

```bash
pip install huggingface_hub pandas pyarrow

```

### 2. 身份验证

向Hugging Face进行身份验证：

```python
import huggingface_hub
huggingface_hub.login(token="your_auth_token")

```

### 3. 加载主表

这将从Hub获取文件并将其加载到DataFrame中。

```python
from huggingface_hub import hf_hub_download
import pandas as pd

parquet_path = hf_hub_download(
    repo_id="SandboxAQ/SAIR",
    filename="sair.parquet",
    repo_type="dataset"
)

df = pd.read_parquet(parquet_path)
df.head()

```

### 4. （可选）列出可用的结构存档

结构文件以多个`.tar.gz`存档的形式存放在`structures_compressed/`目录下。列出它们并选择您需要的部分。

```python
from huggingface_hub import list_repo_files

files = [f.split("/")[-1] for f in list_repo_files("SandboxAQ/SAIR", repo_type="dataset")
         if f.startswith("structures_compressed/") and f.endswith(".tar.gz")]
files[:5]

```

### 5. （可选）下载并解压结构文件

每个存档文件可能很大（≈10 GB）。请仅下载您需要的部分并在本地解压。

```python
import os, tarfile
from huggingface_hub import hf_hub_download

dest = "sair_structures"
os.makedirs(dest, exist_ok=True)

to_get = [
    "sair_structures_1006049_to_1016517.tar.gz",
    "sair_structures_100623_to_111511.tar.gz",
]

for name in to_get:
    tar_path = hf_hub_download(
        repo_id="SandboxAQ/SAIR",
        filename=f"structures_compressed/{name}",
        repo_type="dataset",
        local_dir=dest,
        local_dir_use_symlinks=False,
    )
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(dest)
    os.remove(tar_path)  

```

为了方便您使用，README文件中提供了此脚本的完整版本，包含更完善的日志记录和验证功能。欲了解更多详情，请访问SAIR主页，阅读我们在bioRxiv上的论文手稿，或观看我们与NVIDIA联合举办的25分钟网络研讨会，其中我们演示了SAIR并解释了其内部数据结构。我们还提供了详尽的文档、教程和示例基准测试，以方便使用并加速内部采用。

药物发现的未来是数据驱动、AI加速的，并建立在可扩展、高质量的结构洞察之上。虽然我们尚不具备仅凭一个提示词就能设计出有效疗法的AI，但SAIR通过提供新的数据和洞察，使研究人员更接近这一目标，甚至有可能为AI加速的研发管线节省数年时间。我们迫不及待地想看到研究人员利用SAIR构建的成果，SandboxAQ的专家们也将全程支持他们的发现过程。

### 有问题吗？

请联系作者或在SAIR数据集讨论页发帖。

作者：Arman Zaribafiyan, Georgia Channing, Zane Beckwith, 和 Rudi Plesch

---

> 本文由AI自动翻译，原文链接：[SAIR: Accelerating Pharma R&D with AI-Powered Structural Intelligence](https://huggingface.co/blog/SandboxAQ/sair-data-accelerating-drug-discovery-with-ai)
> 
> 翻译时间：2026-02-13 04:25
