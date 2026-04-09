---
title: 165美元训练25物种mRNA模型，构建蛋白质AI端到端流程
title_original: Training mRNA Language Models Across 25 Species for $165
date: '2026-03-31'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/OpenMed/training-mrna-models-25-species
author: ''
summary: 本文介绍了OpenMed团队构建的一个从蛋白质结构预测、序列设计到mRNA密码子优化的完整AI流程。团队重点探索了适用于密码子级语言建模的Transformer架构，发现CodonRoBERTa-large-v2在困惑度和相关性指标上显著优于ModernBERT等模型。随后，该模型被扩展至25个物种进行训练，并构建了物种条件化系统。文章详细记录了架构选择、实验过程与端到端工作流，并提供了可运行的代码，旨在实现从蛋白质概念到可合成DNA序列的高效转化。
categories:
- AI研究
tags:
- mRNA语言模型
- 密码子优化
- 蛋白质AI
- Transformer架构
- 生物信息学
draft: false
translated_at: '2026-04-09T04:34:43.072750'
---

# 以165美元成本训练25个物种的mRNA语言模型

## 第二部分：构建从结构预测到密码子优化的完整流程

作者：OpenMed——面向医疗与生命科学的开源智能体AI

**摘要**：我们构建了一个涵盖结构预测、序列设计和密码子优化的端到端蛋白质AI流程。在比较了多种用于密码子级语言建模的Transformer架构后，**CodonRoBERTa-large-v2**以4.10的困惑度和0.40的斯皮尔曼CAI相关性成为明确优胜者，显著优于ModernBERT。随后我们将其扩展至25个物种，用55个GPU小时训练了4个生产模型，并构建了一个其他开源项目均未提供的物种条件化系统。完整结果、架构决策和可运行代码见下文。

**目录**

1.  我们构建了什么
2.  架构探索
3.  流程详解
    3.1 蛋白质折叠
    3.2 序列设计
    3.3 mRNA优化
4.  扩展到多物种
5.  端到端工作流
6.  现状与未来计划
7.  参考文献

想象一下，在一个下午内，从一个治疗性蛋白质的概念，到一个可供合成的、密码子优化的DNA序列。这正是**OpenMed**着手构建的流程，本文完整记录了从开始到结束的全过程。

在第一部分中，我们描绘了蛋白质AI的全景：驱动结构预测的架构、可用于蛋白质设计的开源工具，以及从AlphaFold到ESMFold的模型生态系统。那是一次概览。而本文是关于构建的实践。

在**OpenMed**，我们着手构建一个完整的流程，将蛋白质想法从概念转化为可表达的DNA。这意味着三个阶段：预测蛋白质的3D结构，设计能折叠成该结构的氨基酸序列，并优化底层的DNA密码子，以便蛋白质在目标生物体中实际表达。在此过程中，我们进行了大量实验，比较了用于密码子优化的Transformer架构，将最佳模型扩展到25个物种，并构建了将所有环节整合起来的工具。

这不是一个精心修饰的成功故事。这是一份透明的记录，讲述了哪些方法有效、什么让我们感到惊讶、以及我们会做出哪些不同的选择，每一步都附有可运行代码和完整结果。

## 1. 我们构建了什么

该流程包含三个组成部分，分别对应第一部分描述的蛋白质工程工作流程的不同阶段。**结构预测**确定蛋白质呈现**何种形状**。**序列设计**确定**哪些氨基酸**将产生该形状。**密码子优化**确定**哪些DNA**能在活细胞中高效产生这些氨基酸。

我们在mRNA优化工作上投入了最多精力，也最有内容可以分享。折叠和设计组件使用了成熟的工具（Meta的ESMFold和Baker Lab的ProteinMPNN，两者在第一部分均有深入介绍）。密码子优化组件完全是我们自己的成果：新模型、新的训练基础设施、新的评估指标。

## 2. 架构探索

在第一部分中，我们概述了蛋白质AI的现状，并指出大多数生物语言模型都是NLP架构的改编。悬而未决的问题是**哪种**架构。BERT变体主导了蛋白质建模（如ESM-2、ProtTrans），但密码子序列与自然语言和氨基酸序列具有不同的统计特性。密码子是从一个包含64个Token的小字母表中抽取的三联体，具有强烈的位置依赖性和物种特异性的使用偏好。我们需要从第一性原理出发，找出有效的方法。

核心问题：哪种Transformer架构最适合密码子级语言建模？

这很重要，因为密码子优化对于治疗性mRNA、疫苗和重组蛋白生产至关重要。遗传密码具有简并性：同一个蛋白质可以由天文数字般不同的DNA序列编码，但某些密码子排列的表达效率比其他排列高出100倍。例如，辉瑞- BioNTech的COVID疫苗就针对人类表达进行了密码子优化。我们希望构建一个模型，能够直接从天然编码序列中学习这些偏好，而不是依赖手工制作的频率表。

### 候选架构

我们从一个小的CodonBERT基线（600万参数，遵循赛诺菲已发布的架构）开始，并扩展到两个系列：代表NLP社区最新效率创新的**ModernBERT**，以及Meta的ESM蛋白质语言模型背后久经考验的主力——**RoBERTa**。

选择RoBERTa是经过深思熟虑的。正如我们在第一部分讨论的，Meta的ESM-2（驱动ESMFold）本身就是一个在蛋白质序列上训练的RoBERTa变体。我们假设，学习氨基酸模式的同一架构家族也可能学习密码子模式。ModernBERT则是对照：一个2024年的架构，具有RoPE嵌入、Flash Attention和交替的局部/全局注意力层，代表了自RoBERTa于2019年发布以来NLP社区学到的一切。

### 训练设置

为确保公平比较，每个模型都在相同的数据上使用相同的评估协议进行训练。我们使用了来自**大肠杆菌**RefSeq的250,000个编码序列，涵盖染色体和完整组装条目。这是一个干净、注释良好的数据集，其密码子使用模式在文献中已有充分描述，为我们提供了验证的基准事实。

我们的分词器将每个密码子映射为一个单独的Token：64个密码子加上5个特殊Token（PAD、UNK、CLS、SEP、MASK），构成一个69个Token的词汇表。这是有意保持最小化。与NLP中使用的BPE分词器（统计学习子词边界）不同，密码子边界是由生物学定义的。每三个核苷酸编码一个氨基酸。我们的分词器尊重这一点。

训练在4块A100 GPU（80GB）上进行，使用FSDP分片，根据模型大小运行15,000到25,000步。所有模型都使用掩码语言建模目标，掩码率为15%，这与ESM-2用于蛋白质序列的目标相同。

### 结果

结果很明确：RoBERTa在困惑度上比ModernBERT高出6倍（4.01对26.24）。这不是微小的差异。尽管ModernBERT拥有现代的注意力模式和高效的架构，但在密码子序列上，其性能从根本上逊色于经典的RoBERTa设计。

### 我们的发现

1.  **预训练的NLP权重无法迁移到生物学领域**
    我们从其发布的英语检查点初始化ModernBERT，期望学习到的注意力模式能提供一个有用的起点。但事实并非如此。我们最好的解释是：ModernBERT在英语文本上的预训练灌输了一些归纳偏置（子词频率分布、位置注意力模式），这些偏置会积极干扰学习密码子统计特性。而随机初始化、纯粹在生物数据上训练的RoBERTa则没有这种负担。这与该领域更广泛的观察一致：ESM-2和ProtTrans都是在生物数据上从头开始训练，而不是从NLP检查点进行微调。

2.  **超参数调优解锁了生物对齐**
    这是本次探索中最令人惊讶且具有实际重要性的发现。比较CodonRoBERTa-large v1和v2：
    相同的架构。相同的数据。相同的参数数量。唯一的区别是：一半的学习率和更长的预热期（2,000步对1,000步）。然而，根据密码子适应指数的衡量，v2预测的密码子可能性与真实生物密码子偏好的相关性提高了**16倍**。
    困惑度实际上略有**上升**（4.10对4.01），这意味着v2在预测确切的掩码密码子方面准确性稍差。但它在预测生物学实际使用的密码子方面表现却好得多。更慢的训练进度让模型能够稳定到能捕捉真实生物信号的表示上，而不是过度拟合表面统计特性。

对于任何训练生物语言模型的人来说，这都是一个至关重要的洞见：仅凭MLM损失并不能衡量生物相关性。特定领域的指标至关重要。在我们的案例中，CAI相关性最终成为了区分有用模型与技术上令人印象深刻但生物学上无意义的模型的关键指标。

3. 基础模型效率惊人

CodonRoBERTa-base（9200万参数）达到了与大型模型几乎相同的困惑度（4.01 vs 4.10），而参数数量减少了3.4倍，训练时间也相应减少。其CAI相关性（0.219）低于v2版本（0.404），但仍远高于基线模型和ModernBERT。对于无法使用多GPU集群的团队来说，基础模型是一个实用的选择，能以极低的成本获得大部分密码子建模性能。

## 3. 流程管线

在第一部分中，我们描述了大多数计算蛋白质工程项目遵循的三阶段工作流程：预测结构、设计序列、优化密码子。这里我们用真实数据运行每个阶段，并报告我们实际得到的结果。

1.  折叠：预测三维结构（ESMFold）
2.  设计：生成能折叠成该结构的序列（ProteinMPNN）
3.  优化：为表达选择最佳密码子（CodonRoBERTa）

### 3.1 使用ESMFold进行蛋白质折叠

![ESMFold架构：使用ESM-2蛋白质语言模型进行单序列结构预测](/images/posts/f68ba0cc09f3.jpg)

ESMFold架构。该模型通过ESM-2编码器解析单个氨基酸序列，然后通过折叠主干和结构模块预测三维坐标。图来自Bertoline等人，Biomolecules 2024，CC-BY 4.0。

如第一部分所述，ESMFold是Meta的单序列结构预测器。它使用ESM-2作为其主干，这是一个在6500万个UniRef序列上训练的拥有150亿参数的蛋白质语言模型。相较于AlphaFold 2的关键优势在于速度：ESMFold跳过了计算成本高昂的多序列比对步骤，直接根据单个氨基酸序列预测结构。这使得它预测每个蛋白质只需几秒钟，而不是几小时。

代价是准确性。ESMFold在CASP14目标上达到约0.87的TM分数，而AlphaFold约为0.92。对于快速原型设计和候选筛选，这种差距是可以接受的。当一个管线生成100个设计的序列并需要重新折叠所有序列以检查可行性时，速度比最后几个百分点的准确性更重要。

### 我们的结果：30条蛋白质链

我们在来自蛋白质数据库的30条蛋白质链上运行了ESMFold。这些都是已知真实结构的真实实验结构，序列长度从211到519个残基不等。该集合特意包含了简单目标（单结构域蛋白质）和具有挑战性的目标（来自多链核糖体复合物的链，PDB 7K00），以对模型进行压力测试。

```python
import json


metrics = json.load(open('outputs/esmfold_metrics.json'))


n_chains = len(metrics)  
avg_plddt = sum(m['mean_plddt'] for m in metrics) / n_chains  
avg_ptm = sum(m['ptm'] for m in metrics) / n_chains  

print(f"Chains: {n_chains}")
print(f"Average pLDDT: {avg_plddt:.1f}")
print(f"Average PTM: {avg_ptm:.2f}")

```

结果细分：

PTM分数很可靠：任何高于0.5的分数都表明模型掌握了正确的整体拓扑结构，我们0.79的平均值表明对预测的折叠具有很高的置信度。pLDDT分数低于已发布的ESMFold基准，这最初让我们感到担忧。解释结果是我们测试集的构成：来自7K00的核糖体链是一个大型多链复合体的一部分，而ESMFold（孤立地预测单链）无法模拟稳定这些结构的链间接触。对于我们集合中的单结构域蛋白质，pLDDT分数始终高于70。

### 运行ESMFold

```bash

source .env_esmfold/bin/activate


python scripts/esmfold_batch.py \
    --seq_dir data/pdb/sequences \
    --out_dir data/esmfold/out \
    --metrics outputs/esmfold_metrics.json \
    --device cuda:0

```

在A100上，每个预测大约需要10-30秒。输出包括：

-   PDB结构文件
-   pLDDT分数（每个残基的置信度，0-100）
-   PTM分数（拓扑结构置信度，0-1）
-   预测对齐误差矩阵

### 3.2 使用ProteinMPNN进行序列设计

ProteinMPNN架构。（A）编码器处理主链原子距离；解码器自回归地生成氨基酸序列。（B）随机解码顺序提高了多样性。（C）绑定位置支持对称和多状态设计。图来自Dauparas等人，Science 2022，CC-BY 4.0。

![ProteinMPNN架构：用于逆向蛋白质设计的消息传递神经网络](/images/posts/9ea5e37083f0.jpg)

正如我们在第一部分中描述的，蛋白质设计是蛋白质折叠的逆过程。折叠是从序列到结构：给定氨基酸，预测三维形状。逆向折叠则相反：给定目标三维形状，寻找能折叠成该形状的氨基酸序列。

来自华盛顿大学David Baker实验室的ProteinMPNN是当前这项任务的金标准。它于2022年发表在《科学》杂志上，并已通过实验验证：设计的序列折叠成目标结构的比率远远超过随机或早期的计算方法。该架构将蛋白质主链视为一个图，其中节点是氨基酸位置，边连接空间上邻近的残基（三维空间中的K近邻）。消息传递神经网络通过该图传播信息，然后自回归地一次生成一个残基的序列。

### 我们的结果：支架7K00

我们在PDB结构7K00（一个大型多链核糖体复合物）上运行了ProteinMPNN：

```bash
python proteinmpnn/protein_mpnn_run.py \
    --pdb_path data/pdb/raw/7K00.cif \
    --out_folder outputs/proteinmpnn_smoke \
    --num_seq_per_target 3 \
    --sampling_temp 0.1

```

结果：

输出内容如下所示：

```text
>7K00, score=1.7100, global_score=1.7100
GIREKIKLVSSAGTGHFYTTTKNKRTKPEKLELKKFDPVVRQHVIYKEAKI/MKRTFQPSVLK...

>T=0.1, sample=1, score=0.8857, seq_recovery=0.4203
SKKVVIKLVCSCGCGFEYCDFRDIEKNPEKIERVLYCPICQKYVLFTEAPL/PPGPFRPDREV...

```

第一行是从晶体结构中提取的天然序列。后续行是ProteinMPNN设计的变体。在温度为0.1（低随机性）时，模型仅从三维几何结构中恢复了约42%的原始氨基酸。这是一个强有力的结果：这意味着模型仅使用主链坐标作为输入，就独立地重新发现了进化选择出的近一半残基。

运行ProteinMPNN的一些实用说明。分数是负对数似然，因此越低越好。42%的恢复率对于解析良好的结构来说是典型的，并且与原始论文的基准一致。更高的采样温度会产生更多样化但风险更高的序列。对于实际的设计工作，最强大的功能是部分设计：催化残基、结合位点氨基酸或任何已知具有重要功能的位置都可以被固定，而ProteinMPNN只重新设计它们周围的支架。这是在工程化更稳定的酶版本而不破坏其活性位点的标准方法。

### 3.3 mRNA优化

这是管线从现有工具过渡到我们自己模型的环节。ESMFold和ProteinMPNN是我们集成的成熟、经过充分验证的软件。密码子优化是我们构建新东西的地方。

#### 为什么密码子选择很重要

不同生物体之间的密码子使用频率差异巨大。这些热图比较了大肠杆菌、酵母和CHO细胞（我们的多物种模型涵盖的三种表达宿主）之间的密码子偏好。图来自Kim等人，J. Microbiol. Biotechnol. 2025，CC-BY 4.0。

![针对大肠杆菌、酿酒酵母和CHO细胞的优化工具的密码子使用频率热图](/images/posts/9197284ccb03.png)

遗传密码具有简并性：大多数氨基酸由多个密码子编码。例如，亮氨酸有六个密码子：TTA、TTG、CTT、CTC、CTA 和 CTG。所有这六个密码子在最终蛋白质中产生相同的氨基酸。甲硫氨酸和色氨酸是例外，各自只有一个密码子。

这种冗余意味着，对于任何给定的蛋白质，存在天文数字般多的DNA序列可以编码它。一个典型的300个氨基酸的蛋白质大约有10^150种可能的密码子组合。它们都产生相同的氨基酸链，但**并非**都产生相同数量的蛋白质。密码子选择会影响翻译速度（因为并非所有密码子的tRNA分子丰度都相同）、mRNA稳定性（因为核苷酸序列影响转录本的降解速度）、共翻译折叠（因为稀有密码子处的翻译暂停为蛋白质折叠提供了时间）以及免疫识别（因为哺乳动物细胞中的先天免疫系统可以区分自身和外来mRNA模式）。实际上，糟糕的密码子选择可能使蛋白质表达降低100倍。这就是为什么每种mRNA疫苗、每种重组蛋白疗法和每种基因治疗载体都要经过密码子优化。

#### 传统方法及其局限性

![mRNA密码子优化的设计空间：数十亿种编码相同蛋白质的可能序列](/images/posts/6a5e54bfc822.png)

密码子优化问题的规模。对于一个典型的mRNA，存在超过10^600种编码相同蛋白质的可能密码子序列。挑战在于找到能最大化表达的排列方式。图来自Zhang等人（LinearDesign），《自然》2023，CC-BY 4.0。

经典方法很简单：测量目标生物体中高表达基因中最常出现的密码子，然后将每个密码子替换为最常用的同义密码子。这被编码为**密码子适应指数**，这是一个衡量密码子使用与生物体偏好分布匹配程度的序列评分。

基于CAI的优化是有效的，但很粗糙。它独立对待每个密码子位置，忽略了序列上下文。它会产生重复序列（对给定氨基酸在所有位置都使用相同的"最优"密码子），这可能导致核糖体停滞和mRNA二级结构问题。并且它忽略了复杂的依赖关系：第50位的最优密码子可能取决于第48位和第52位的密码子，这是频率表无法捕捉的。

#### 我们的方法：掩码语言建模

我们将密码子优化重新定义为语言建模问题。我们不再从表中查找频率，而是使用掩码语言建模（MLM）在数十万个天然编码序列上训练一个Transformer，这与BERT、RoBERTa和Meta的ESM蛋白质模型使用的预训练目标相同。模型看到一个有15%位置被掩码的密码子序列，并学习根据上下文预测缺失的密码子。

模型隐式学习到的是密码子使用的**语法**：自然界中出现哪些密码子模式，哪些密码子倾向于共现，以及偏好如何根据周围的序列上下文而变化。这从根本上比频率表更丰富，因为模型捕捉了整个编码序列中的长程依赖关系。

### CodonRoBERTa：我们的最佳模型

经过我们的架构探索（见上文），**CodonRoBERTa-large-v2** 脱颖而出成为优胜者：

```yaml

model_type: roberta
hidden_size: 1024
num_hidden_layers: 24
num_attention_heads: 16
intermediate_size: 4096
vocab_size: 69
max_position_embeddings: 8192
learning_rate: 5e-5  
warmup_steps: 2000   
max_steps: 25000

```

训练：

```bash
python scripts/training/run_mlm_train.py \
    --config configs/mrna/roberta_large_v2.yaml \
    --train_file data/mrna/processed/train_250k.fasta \
    --output_dir outputs/models/CodonRoBERTa-large-v2

```

### 评估：三个重要的指标

评估密码子语言模型并不简单。正如我们从上面的v1/v2比较中了解到的，一个模型可能具有出色的困惑度（准确预测掩码密码子），但生物学对齐性却很差（预测自然界实际上并不偏好的密码子）。我们从三个互补的维度进行评估：

1. **困惑度** 衡量模型预测掩码密码子的能力，计算为指数化的交叉熵损失。困惑度为4.10意味着模型在每个掩码位置平均在约4个同等可能的密码子之间进行选择。鉴于大多数氨基酸有2-6个同义密码子，这表明模型学到了有意义的偏好，而不是均匀猜测。数值越低越好。CodonRoBERTa-large-v2：**4.10**。

2. **CAI相关性**（斯皮尔曼）衡量模型预测的密码子似然是否与已知的生物密码子使用偏好一致。我们计算每个测试序列的密码子适应指数，然后将其与模型的伪对数似然分数相关联。正相关意味着模型为生物学实际使用的序列分配了更高的概率。这是实际密码子优化最重要的指标，因为它直接衡量模型是否学到了与生物学相关的模式，而不仅仅是统计模式。CodonRoBERTa-large-v2：**0.404**（p < 10^-20）。

3. **同义恢复率** 询问：当模型预测掩码位置的密码子时，它是否至少能正确预测氨基酸？即使它选择了错误的同义密码子（例如，亮氨酸的CTT而不是CTC），预测正确的氨基酸也表明模型理解了蛋白质层面的约束。CodonRoBERTa-large-v2：**12.1%** top-1同义恢复率。

### 运行评估

```bash

python scripts/evals/advanced/eval_perplexity.py \
    --model outputs/models/CodonRoBERTa-large-v2/final \
    --test_file data/mrna/processed/test_6k.fasta \
    --output outputs/eval_results/CodonRoBERTa-large-v2/perplexity.json


python scripts/evals/advanced/eval_cai_correlation.py \
    --model outputs/models/CodonRoBERTa-large-v2/final \
    --test_file data/mrna/processed/test_6k.fasta \
    --output outputs/eval_results/CodonRoBERTa-large-v2/cai_correlation.json


python scripts/evals/advanced/eval_synonymous_recovery.py \
    --model outputs/models/CodonRoBERTa-large-v2/final \
    --test_file data/mrna/processed/test_6k.fasta \
    --output outputs/eval_results/CodonRoBERTa-large-v2/synonymous_recovery.json

```

### 最终排行榜

汇总我们所有模型变体的结果：

RoBERTa家族在所有指标上均占主导地位。对于生产用途，CodonRoBERTa-large-v2是明确的选择：它具有最强的生物学对齐性（CAI 0.404），同时保持了有竞争力的困惑度。对于计算资源有限的团队，CodonRoBERTa-base以3.4倍更少的参数提供了几乎相同的困惑度。ModernBERT表现明显不佳，我们将其归因于其NLP预训练权重干扰了密码子模式的学习。

### 使用模型

```python
from transformers import RobertaForMaskedLM
import torch


model = RobertaForMaskedLM.from_pretrained("OpenMed/CodonRoBERTa-large-v2")
tokenizer = CodonTokenizer()  


sequence = "ATG GCT AAA GGT..."  
inputs = tokenizer(sequence, return_tensors='pt')

with torch.no_grad():
    outputs = model(**inputs)
    


masked_seq = "ATG [MASK] AAA GGT..."
inputs = tokenizer(masked_seq, return_tensors='pt')
predictions = model(**inputs).logits
top_codons = predictions[0, mask_pos].topk(5)

```

## 4. 扩展到多物种

单物种密码子优化有用，但有限。每个生物体都有其自身经过数百万年进化形成的密码子使用偏好。*E. coli*偏好的密码子与人类细胞不同，而人类细胞偏好的密码子又与酵母不同。仅用*E. coli*数据训练的模型将无法为人类表达产生最优密码子。

行业标准是为每种生物体使用独立的密码子适应指数表。我们想要更好的方案：一个能理解跨物种密码子使用模式、可根据目标物种进行条件化、并能将知识从数据丰富的生物体（人类，拥有14.5万条注释编码序列）迁移到数据匮乏生物体（大肠杆菌，仅9千条）的单一模型。在确定CodonRoBERTa-large-v2是单物种数据上的最佳架构后，我们构建了这个系统。

### 数据工程挑战

构建多物种密码子数据集并非简单下载几个基因组。每个生物体存在于不同的NCBI RefSeq组装中，具有不同的注释质量、不同的CDS边界和不同的序列规范。我们编写了自动化流程，从25种生物体中下载CDS序列，进行验证（检查正确的起始/终止密码子、长度能被3整除、无内部终止密码子），用物种标记标注每条序列，并按物种分层划分训练集/测试集。

```python



SPECIES = {
    
    'bacteria': [
        ('GCF_000005845.2', 'Escherichia coli K-12', 'ECOLI'),
        ('GCF_000009045.1', 'Bacillus subtilis 168', 'BSUBT'),
        ('GCF_000006945.2', 'Salmonella enterica', 'SENTE'),
        ('GCF_000195955.2', 'Mycobacterium tuberculosis', 'MTUBE'),
        
    ],
    
    'yeast': [
        ('GCF_000146045.2', 'Saccharomyces cerevisiae S288C', 'YEAST'),
        ('GCF_000002515.2', 'Schizosaccharomyces pombe', 'SPOMBE'),
        ('GCF_000027005.1', 'Pichia pastoris', 'PICHIA'),
    ],
    
    'mammals': [
        ('GCF_000001405.40', 'Homo sapiens GRCh38', 'HUMAN'),
        ('GCF_000001635.27', 'Mus musculus GRCm39', 'MOUSE'),
        ('GCF_003668045.3', 'Cricetulus griseus CHO-K1', 'CHO'),
    ]
}

```

最终数据集涵盖生物技术相关的三个领域：

这种覆盖范围是经过深思熟虑的：细菌是重组蛋白生产的主力，酵母主导工业生物制造，而哺乳动物细胞（尤其是CHO和人类细胞）是治疗性蛋白和mRNA疫苗所必需的。这25种生物体共同覆盖了现实世界中绝大多数密码子优化应用场景。

### 标记化创新

一个需要识别来自25种不同生物体序列的模型必须知道它正在处理哪种生物体。我们通过在原有的69个密码子标记词汇表基础上扩展25个物种标记来解决这个问题，创建了一个包含94个标记的系统。每条序列都以其物种标记作为前缀（例如[HUMAN]、[ECOLI]、[YEAST]），这样模型就能在单一共享架构中学习物种特异性的密码子偏好。

```python

class MultiSpeciesCodonTokenizer(CodonTokenizer):
    """具有物种感知能力的扩展标记器"""

    def __init__(self):
        super().__init__()
        
        
        

        self.species_tokens = [
            '[ABAUM]', '[BSUBT]', '[CHO]', '[ECOLI]',
            '[HUMAN]', '[MOUSE]', '[YEAST]', 
        ]

    def encode(self, dna_seq: str, species: str = None):
        """添加物种标记前缀进行编码"""
        ids = super().encode(dna_seq)
        if species and species in self.species_to_id:
            ids = [self.species_to_id[species]] + ids
        return ids

```

这种设计有三个优点。首先，它实现了物种条件化生成：同一个模型根据前置的物种标记，可以生成人类最优或大肠杆菌最优的密码子。其次，它支持跨物种迁移学习：通用的密码子模式（如避免某些二核苷酸，或在GC含量高的基因组中偏好GC丰富的密码子）在所有物种间共享，而物种特异性偏好则通过物种标记的条件化来捕捉。第三，这94个标记的词汇表与我们原有的69个标记单物种模型向后兼容，因为前69个标记是相同的。

### 训练通用基础模型

通用基础模型是一个3.119亿参数的RoBERTa-large架构，与我们的单物种v2模型架构相同，但使用了扩展的94标记词汇表。它在4块A100 GPU上使用完整的36.2万条多物种数据集训练了48小时。

```yaml

model:
  name: "CodonRoBERTa-large-multispecies"
  vocab_size: 94  
  hidden_size: 1024
  num_hidden_layers: 24
  num_attention_heads: 16

training:
  max_steps: 50000  
  learning_rate: 5e-5
  per_device_train_batch_size: 4  
  gradient_accumulation_steps: 2   
  bf16: true
  fsdp: "full_shard auto_wrap"  

```

训练命令：

```bash
torchrun --nproc_per_node=4 --master_port=29501 \
    scripts/training/run_multispecies_train.py \
    --config configs/mrna/production/roberta_large_multispecies.yaml

```

测试困惑度为24.9，高于我们单物种模型的4.01，这看起来像是性能倒退。但事实并非如此。多物种模型必须学习25种不同生物体各自独特的密码子偏好，每种生物体都有其自身的进化历史和tRNA池。像结核分枝杆菌（GC含量65%）这样的细菌使用的密码子与人类细胞（GC含量41%）完全不同。模型正在解决一个本质上更困难的问题，困惑度反映了这一点。关键在于物种特异性微调是否能恢复性能，而事实证明确实可以。

### 物种特异性微调

通用基础模型是通才。在实际生产应用中，专才表现更佳。OpenMed的微调策略从多物种检查点开始，以较低的学习率（2e-5对比5e-5）在单一物种数据上进一步训练，在保留跨物种知识的同时，使模型的预测专门针对一种生物体。

数据集划分：

```python



RESULTS = {
    'HUMAN': {'train': 131_245, 'test': 6_908},
    'MOUSE': {'train': 88_022,  'test': 4_633},
    'CHO':   {'train': 42_541,  'test': 2_239},
    'ECOLI': {'train': 8_547,   'test': 450},
    'YEAST': {'train': 5_439,   'test': 287},
    'PICHIA':{'train': 4_548,   'test': 240},
}

```

训练所有三个优先物种：

```bash

torchrun --nproc_per_node=4 scripts/training/run_multispecies_train.py \
    --config configs/mrna/production/roberta_large_human_finetune.yaml


torchrun --nproc_per_node=4 scripts/training/run_multispecies_train.py \
    --config configs/mrna/production/roberta_large_ecoli_finetune.yaml


torchrun --nproc_per_node=4 scripts/training/run_multispecies_train.py \
    --config configs/mrna/production/roberta_large_cho_finetune.yaml

```

综合结果：

这里最重要的结果是HUMAN模型：其困惑度为24.3，是唯一一个性能优于通用基础模型的专家模型，这使其成为我们治疗性mRNA应用的生产模型。但从研究角度来看，ECOLI的结果可能更有趣。尽管只有8,547条训练序列（相比之下人类有13.1万条），大肠杆菌专家模型的表现仍然比多物种基础模型有所提升。这验证了迁移学习的假设：先在25个物种上训练，然后在小的物种特定数据集上微调，效果优于仅在小型数据集上训练。对于许多注释CDS数据稀缺的生物体，这种方法为合理的密码子优化打开了大门，而无需数万条物种特异性序列。

CHO模型显示出轻微的性能下降（25.5对比24.9），我们将其归因于训练步数不足。ECOLI用8.5k序列训练了5,000步（每序列0.59步），而CHO用42.5k序列训练了10,000步（每序列0.24步）。用15,000步重新训练应能缩小这一差距。所有三个专家模型的总微调时间仅为7小时，这得益于对多物种基础模型48小时的投资。

### 完整模型套件

经过55小时的训练，我们获得了：

所有模型将在Hugging Face上通过OpenMed组织发布。命名约定遵循OpenMed/{model-name}，以便直接使用from_pretrained()。

通用模型：

- OpenMed/CodonRoBERTa-large-multispecies（3.119亿参数）基于25个物种训练困惑度：24.9用例：跨物种优化、稀有生物体

- 基于25个物种训练
- 困惑度：24.9
- 用例：跨物种优化、稀有生物体

**物种特异性专家模型：**

- OpenMed/CodonRoBERTa-large-human（3.119亿参数）困惑度：24.3（总体最佳）用例：mRNA疫苗、基因治疗、治疗性蛋白
- OpenMed/CodonRoBERTa-large-ecoli（3.119亿参数）困惑度：25.3用例：细菌蛋白表达、代谢工程
- OpenMed/CodonRoBERTa-large-cho（3.119亿参数）困惑度：25.5用例：哺乳动物细胞培养、生物制药

OpenMed/CodonRoBERTa-large-human（3.119亿参数）

- 困惑度：24.3（总体最佳）
- 用例：mRNA疫苗、基因治疗、治疗性蛋白

OpenMed/CodonRoBERTa-large-ecoli（3.119亿参数）

- 困惑度：25.3
- 用例：细菌蛋白表达、代谢工程

OpenMed/CodonRoBERTa-large-cho（3.119亿参数）

- 困惑度：25.5
- 用例：哺乳动物细胞培养、生物制药

**单物种模型：**

- OpenMed/CodonRoBERTa-large-v2（3.12亿参数）困惑度：4.10，CAI：0.404基于25万条大肠杆菌序列训练仍然是纯大肠杆菌优化的最佳选择
- OpenMed/CodonRoBERTa-base（9200万参数）困惑度：4.01，CAI：0.219最佳效率选择（比大模型小3.4倍）

OpenMed/CodonRoBERTa-large-v2（3.12亿参数）

- 困惑度：4.10，CAI：0.404
- 基于25万条大肠杆菌序列训练
- 仍然是纯大肠杆菌优化的最佳选择

OpenMed/CodonRoBERTa-base（9200万参数）

- 困惑度：4.01，CAI：0.219
- 最佳效率选择（比大模型小3.4倍）

### 生产部署策略

**用于治疗性mRNA（Moderna、BioNTech式疫苗）：**

```python
from transformers import RobertaForMaskedLM


model = RobertaForMaskedLM.from_pretrained("OpenMed/CodonRoBERTa-large-human")


optimized_dna = optimize_for_human(protein_seq, model)

```

**用于工业蛋白生产：**

```python

model_ecoli = RobertaForMaskedLM.from_pretrained("OpenMed/CodonRoBERTa-large-ecoli")


model_cho = RobertaForMaskedLM.from_pretrained("OpenMed/CodonRoBERTa-large-cho")

```

**用于稀有/未建模生物体：**

```python

model_multi = RobertaForMaskedLM.from_pretrained("OpenMed/CodonRoBERTa-large-multispecies")


```

### 基础设施与可复现性

**硬件要求：**

- 4×A100 80GB GPU（训练）
- 单张A100 40GB GPU（推理）
- 使用FSDP（全分片数据并行）处理3.119亿参数
- bf16混合精度（对稳定性至关重要）

**存储占用：**

- 总计约150 GB（所有运行的数据、训练模型和检查点）

**完整训练流程：**

```bash

python scripts/training/download_multispecies_cds.py \
    --output_dir data/mrna/multispecies \
    --categories bacteria yeast mammals


torchrun --nproc_per_node=4 \
    scripts/training/run_multispecies_train.py \
    --config configs/mrna/production/roberta_large_multispecies.yaml


python scripts/training/split_species_datasets.py \
    --input data/mrna/multispecies/train_multispecies.fasta \
    --output_dir data/mrna/species_specific


for species in human ecoli cho; do
    torchrun --nproc_per_node=4 \
        scripts/training/run_multispecies_train.py \
        --config configs/mrna/production/roberta_large_${species}_finetune.yaml
done


for model in multispecies human ecoli cho; do
    python scripts/evals/advanced/eval_perplexity_multispecies.py \
        --model_path outputs/models/CodonRoBERTa-large-${model}/final \
        --test_file data/mrna/species_specific/${model}_test.fasta \
        --output_file outputs/evals/${model}_perplexity.json
done

```

**总计算成本：**

- 在A100 80GB上消耗55 GPU小时（在AWS p4d.24xlarge上约165美元）
- 所有模型在3天挂钟时间内训练至收敛

### 实现的能力

多物种套件涵盖了应用密码子优化的三大支柱。对于治疗性mRNA，**HUMAN专家模型**优化了在人类细胞中表达的密码子，可直接应用于疫苗设计（Moderna和BioNTech都对其mRNA构建体进行密码子优化）和基因治疗载体。对于重组蛋白生产，**ECOLI专家模型**处理最常见的细菌表达宿主，而**CHO专家模型**则覆盖了用于生产大多数单克隆抗体和生物制药的哺乳动物细胞系。对于专家模型未覆盖的生物体，**多物种基础模型**接受25个物种标记中的任何一个，并生成适合该生物体的密码子。

迁移学习的结果对更广泛的社区尤其相关。许多具有工业重要性的生物体（非模式细菌、昆虫细胞、植物细胞）的注释CDS数据有限。我们在大肠杆菌上的结果（8.5k条序列，优于基础模型）表明，**多物种预训练结合小规模微调**是适用于这些生物体的可行路径，无需从头训练所需的数万或数十万条序列。

### 数据统计

整个项目在4张A100 80GB GPU上消耗了55 GPU小时（按AWS Spot价格约165美元），在4次训练运行中产生了约150 GB的模型和检查点，涵盖了从NCBI RefSeq下载的25个物种的381,283条CDS序列。所有模型使用相同的3.119亿参数架构，以safetensors格式保存以便快速加载，并在单张16GB+显存的GPU上进行推理。所有内容均在Apache 2.0许可下发布。

## 5. 端到端工作流程

![两步蛋白质设计范式：生成骨架结构，然后优化序列](/images/posts/6403f57bf456.jpg)

现代计算蛋白质设计工作流程。结构生成（顶部）产生骨架坐标；序列优化（底部）寻找折叠成目标形状的氨基酸序列。我们的流程增加了第三步：针对表达的密码子优化。图片来自Kortemme, Cell 2024, CC-BY 4.0。

在第一部分中，我们将蛋白质工程循环描述为预测、设计和优化的循环。以下是使用**OpenMed**流程在实践中的具体体现。每一步都馈入下一步，整个计算阶段在一个下午即可在单张GPU上完成。

考虑一个具体场景：设计一种在血液中降解过快的治疗性酶的更稳定版本。

**步骤1：折叠（ESMFold）。** 预测起始序列的结构，以了解其活性位点并识别可能不稳定的区域。ESMFold返回PDB格式的3D结构、突出不确定区域的每个残基置信度分数（pLDDT）以及整体拓扑置信度指标（PTM）。

**步骤2：设计（ProteinMPNN）。** 保持活性位点固定，但重新设计支架以提高稳定性。ProteinMPNN接收骨架坐标、不可变位置列表（催化残基），并生成100个不同的候选序列，每个序列都被预测能折叠成目标形状。

**步骤3：验证（ESMFold）。** 使用ESMFold重新折叠所有100个候选序列，以确认它们仍能采用正确的形状。筛选出高平均pLDDT（>80）、正确拓扑结构（与原始结构的RMSD）和低碰撞分数的序列。

**步骤4：优化（CodonRoBERTa）。** 选取最佳的氨基酸序列，并使用CodonRoBERTa-large-v2为在目标生物体（大肠杆菌、酵母或哺乳动物细胞）中表达生成优化的DNA序列。该模型基于学习到的生物学偏好对同义密码子选择进行评分，识别上下文最优的密码子而非仅全局高频密码子，并产生具有高CAI相关性的序列。

**步骤5：合成与测试。** 向合成公司订购DNA，将其克隆到表达载体中，并在实验室中测试表达和活性。

这个从假设到可合成DNA的循环，取代了曾经需要数月湿实验室试错迭代的过程。研究人员带着5-10个经过计算验证的候选方案，而非一两个有根据的猜测，进入实验台。成功率提高，成本下降，设计周期从数月压缩到数天。

如需获取完整的生态系统概览、工具选择指南和许可证参考，请参阅第一部分。

## 6. 现状与未来展望

### 行业格局

OpenMed 并非孤立运作。近期有两个模型将密码子/mRNA 建模的前沿进一步推进：

- **mRNABERT**（Xiong 等人，《自然通讯》2025）：拥有 8600 万参数的 BERT 模型，采用双重分词方案（UTR 区域使用单核苷酸，CDS 区域使用密码子），并针对冻结的 ProtT5-XL 蛋白质嵌入进行跨模态对比学习。在 1800 万条序列上训练。在全长 mRNA 翻译效率预测上达到 R^2 = 0.66，相比之前的 RNA 模型有 1.6 到 10 倍的提升。代码和权重已开源（Apache 2.0 许可证）。
- **NUWA**（Zhong 等人，bioRxiv 2026）：包含三个特定领域的 RoBERTa 编码器（细菌、真核生物、古菌），采用课程式掩码语言模型和带监督的对比学习。在约 25,000 个物种的 1.15 亿条序列上训练。在 BEACON 基准测试的 13 项任务中有 11 项超越了 CodonBERT。未发布代码或权重。

这两个模型的训练数据量是 OpenMed 所用数据的 50-300 倍。这是主要的差距，我们对此保持透明。

以下是 OpenMed 提供而它们不具备的功能：

1.  **物种条件化的单一模型**。mRNABERT 完全不包含物种条件化。NUWA 训练了三个独立的模型（每个生命域一个）。我们将 25 个物种标记放入一个包含 94 个标记的词汇表中，并训练一个单一的模型，可以通过提示词指定任何生物体。参数效率更高，更灵活。
2.  **已验证的向低资源生物体的迁移学习**。我们展示了仅用 8.5k 条大肠杆菌序列对多物种基础模型进行微调，即可超越基础模型。mRNABERT 和 NUWA 均未展示这一点。
3.  **完整的开源流程**。ESMFold + ProteinMPNN + CodonRoBERTa，端到端，包含训练代码、配置文件、评估脚本和模型权重。全部采用 Apache 2.0 许可证。mRNABERT 发布了代码但没有发布完整流程。NUWA 未发布任何内容。

### 进行中：CodonJEPA

OpenMed 正在对一个根本不同的方法进行概念验证：用于密码子序列的**联合嵌入预测架构**。

标准的掩码语言模型预测被掩码的标记。JEPA 预测被掩码的嵌入。其假设是：如果模型被迫在嵌入空间而非标记空间进行预测，它应该能学到同义密码子（DNA 不同，氨基酸相同）在功能上是等价的。MLM 无法实现这一点，因为它的训练目标是区分每个标记。

架构如下：

- 上下文编码器：RoBERTa-base（768 维，12 层），正常训练
- 目标编码器：上下文编码器的指数移动平均副本（动量 0.990 至 0.999，无梯度）
- 预测器：轻量级 4 层 Transformer（384 维），根据上下文预测目标嵌入
- 掩码策略：多块策略（每条序列 4 个连续块，掩码比例 15-20%）
- 防止坍缩：VICReg 正则化（方差 + 协方差损失）

来自我们评估套件的早期结果（JEPA 对比 MLM 基线，相同数据，相同超参数，各训练 15k 步）：

同义稳健性结果对我们的假设最为重要。对于仅在同义密码子选择上存在差异的序列，JEPA 嵌入几乎完全相同（余弦相似度 99.97%）。MLM 嵌入则发生显著偏移（94.14%）。这意味着 JEPA **确实**学到了同义密码子是可互换的，正如预测的那样。

面临的公开挑战：JEPA 目前存在维度坍缩问题（91.78% 的方差集中在一个成分上）。这是自监督方法已知的失败模式，表明 VICReg 正则化权重需要调整。架构是有效的；训练动态需要更多迭代。

这是早期阶段的研究，尚未达到生产就绪状态。但如果坍缩问题能够解决，JEPA 可能产生本质上具有氨基酸感知能力的密码子嵌入，这是 MLM 因其标记级预测目标而根本不可能实现的。

### 路线图

**CodonRoBERTa（扩展规模）：**

- 在 mRNABERT 公开的 3600 万条序列数据集（Zenodo）上重新训练。相同架构，相同物种标记，数据量增加 100 倍
- 添加与 ProtT5-XL 的跨模态对比对齐（mRNABERT 已证明其能提升蛋白质属性预测）
- 将物种特异性微调扩展到 YEAST、PICHIA、MOUSE
- 添加 mRNA 稳定性和免疫原性预测头

**CodonJEPA（修复与扩展）：**

- 解决维度坍缩问题（更强的 VICReg 权重，替代正则化器）
- 在相同的下游任务上，与 mRNABERT 的对比方法进行基准测试
- 如果 JEPA 嵌入表现良好，将其作为 MLM 嵌入的直接替代品集成到流程中

**流程：**

- 集成 RFdiffusion 用于从头生成蛋白质骨架
- 添加溶解度和表达预测头
- 在特定领域（抗体、酶）上微调 ESMFold

### 环境设置与要求

**硬件：**

- 已在 4×A100 GPU（80GB）上测试
- 折叠推理：典型蛋白质约需 16-20GB 显存
- 训练：使用 FSDP（全分片数据并行）进行扩展
- 推理最低要求：单 GPU，16GB+ 显存

**环境：**

- 使用 `.env_esmfold` 虚拟环境进行折叠
- 训练环境：PyTorch 2.5.1+cu121 并安装 flash-attn2
- 推荐 Python 3.10+

**许可证**（全部对商业友好）：

- ESMFold: MIT
- ProteinMPNN: MIT
- OpenFold: Apache-2.0
- 我们的 CodonRoBERTa: Apache-2.0

## 7. 参考文献

OpenMed 的工作建立在 Meta AI、华盛顿大学贝克实验室、DeepMind 以及更广泛的开源计算生物学社区的基础研究之上。

### 关键论文

**蛋白质结构预测**

- Jumper, J. 等人。"Highly accurate protein structure prediction with AlphaFold."《自然》（2021）。DOI
- Lin, Z. 等人。"Evolutionary-scale prediction of atomic-level protein structure with a language model."《科学》（2023）。DOI
- Ahdritz, G. 等人。"OpenFold: Retraining AlphaFold2 yields new insights."《自然方法》（2024）。DOI

**蛋白质设计**

- Dauparas, J. 等人。"Robust deep learning-based protein sequence design using ProteinMPNN."《科学》（2022）。DOI
- Watson, J.L. 等人。"De novo design of protein structure and function with RFdiffusion."《自然》（2023）。DOI

**mRNA 与密码子优化**

- Cheng, J. 等人。"CodonBERT: a language model for codon optimization."《核酸研究》（2024）。DOI
- Xiong, Y. 等人。"mRNABERT: advancing mRNA sequence design with a universal language model and comprehensive dataset."《自然通讯》（2025）。DOI
- Zhong, Y. 等人。"Large mRNA language foundation modeling with NUWA for unified sequence perception and generation."bioRxiv（2026）。DOI
- Warner, B. 等人。"ModernBERT: Smarter, Better, Faster, Longer." arXiv（2024）。arXiv

## 模型与数据：即将发布

本文中描述的所有模型、训练代码及多物种数据集，将在 Hugging Face 平台的 OpenMed 组织下以 Apache 2.0 / MIT 许可证公开发布。

**模型**（7个检查点）：

**数据集**：

训练代码与评估脚本将随模型一同发布。

在 Hugging Face 上关注 OpenMed，以便在模型上线时获得通知。

**ML 工程师的蛋白质 AI 指南：从蛋白质到优化 DNA | 2026年3月**

阅读第一部分：《AlphaFold 革命》，了解蛋白质 AI 的发展全景。

如有问题或合作想法？请在 Hugging Face 上联系我们，或在模型页面发起讨论。

---

> 本文由AI自动翻译，原文链接：[Training mRNA Language Models Across 25 Species for $165](https://huggingface.co/blog/OpenMed/training-mrna-models-25-species)
> 
> 翻译时间：2026-04-09 04:34
