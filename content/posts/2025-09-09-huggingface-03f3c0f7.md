---
title: mmBERT：高效多语言大模型，覆盖1800+语言
title_original: 'mmBERT: ModernBERT goes Multilingual'
date: '2025-09-09'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/mmbert
author: ''
summary: 本文介绍了mmBERT，这是一个基于ModernBERT架构构建的先进多语言编码器模型。它在超过1800种语言的3万亿Token文本上进行训练，通过渐进式语言纳入、三阶段训练（预训练、中期训练、衰减阶段）及逆掩码率调度等创新技术，显著提升了多语言任务的性能与效率。模型采用Gemma
  2分词器，并利用高质量数据集（如DCLM、FineWeb2）确保数据覆盖与质量，是首个超越XLM-R的多语言模型，特别针对低资源语言学习提出了有效策略。
categories:
- AI研究
tags:
- 多语言模型
- 自然语言处理
- 预训练模型
- 低资源语言
- BERT
draft: false
translated_at: '2026-02-13T04:25:11.152112'
---

# mmBERT：ModernBERT 走向多语言化

## 摘要

这篇博文介绍了 **mmBERT**，这是一个最先进的大规模多语言编码器模型，在超过 1800 种语言的 3T+ Token 文本上进行训练。相比之前的多语言模型，它在性能和速度上都有显著提升，是首个超越 XLM-R 的模型，同时还开发了有效学习低资源语言的新策略。mmBERT 基于 ModernBERT 构建，拥有极快的架构，并增加了新颖的组件以实现高效的多语言学习。

如果您有兴趣亲自尝试这些模型，本文末尾提供了一些示例代码！

## 训练数据

mmBERT 在三个不同的训练阶段，使用了一个精心策划的多语言数据集进行训练，总计超过 3T Token。我们训练数据的基础由三个主要的开源高质量网络爬取数据组成，确保了多语言覆盖率和数据质量：

**DCLM 和 Filtered DCLM** 提供了可用的最高质量英文内容，是强大英文性能的支柱（过滤后的数据来自 **Dolmino**）。该数据集代表了最先进的网络过滤技术，是一个关键组成部分。由于这些数据质量很高，我们使用的英文数据比例显著高于上一代多语言编码器模型（高达 18%）。

**FineWeb2** 提供了涵盖超过 **1,800 种语言**的广泛多语言网络内容。该数据集使我们能够实现广泛的多语言覆盖，同时在不同语系和文字体系间保持合理的质量标准。

**FineWeb2-HQ** 是 **FineWeb2 的一个过滤子集**，专注于 20 种高资源语言。这个过滤版本提供了更高质量的多语言内容，弥合了纯英文过滤数据与广泛多语言覆盖之间的差距。

训练数据还整合了来自 **Dolma**、**MegaWika v2**、**ProLong** 等的专业语料库：代码仓库（StarCoder, ProLong）、学术内容（ArXiv, PeS2o）、参考资料（Wikipedia, 教科书）和社区讨论（StackExchange），以及指令和数学数据集。

我们数据方法的关键创新在于 **渐进式语言纳入策略**，如 **图 1** 所示。在每个阶段，我们逐步从一个**更平坦的分布**（即更接近均匀分布）中采样，同时添加新的语言。这意味着像俄语这样的高资源语言开始时在数据中占比较高（例如 9%），然后在训练的最后阶段降至大约一半。我们在预训练阶段从 60 种高资源语言开始，在中期训练阶段扩展到 110 种语言，最后在衰减阶段纳入来自 FineWeb2 的所有 1,833 种语言。这使我们能够在不过度重复且保持整体数据高质量的前提下，最大化有限低资源语言数据的影响。

## 训练方案与新颖组件

mmBERT 基于 **ModernBERT** 架构构建，但针对多语言学习引入了几项关键创新：

### 架构

我们使用与 ModernBERT-base 相同的核心架构，具有 22 层和 1152 个中间维度，但改用 **Gemma 2** 分词器以更好地处理多语言文本。基础模型有 1.1 亿个非嵌入参数（由于词汇量更大，总计 3.07 亿），而小型变体有 4200 万个非嵌入参数（总计 1.4 亿）。

### 三阶段训练方法

我们的训练遵循精心设计的三阶段计划：

1.  **预训练（2.3T Token）**：使用 60 种语言，掩码率为 30%，进行预热和稳定学习率阶段。
2.  **中期训练（600B Token）**：上下文长度扩展到 8192 Token，使用更高质量的数据，扩展到 110 种语言，掩码率为 15%。
3.  **衰减阶段（100B Token）**：采用逆平方根学习率衰减，纳入所有 1,833 种语言，掩码率为 5%。

### 新颖的训练技术

**逆掩码率调度**：我们不是使用固定的掩码率，而是在训练阶段逐步将掩码率从 30% → 15% → 5% 降低。这使得模型早期可以通过更高的掩码率学习基本表示，然后在后期通过更低的掩码率专注于更细微的理解。

**退火语言学习**：我们动态调整多语言数据采样的温度，从 τ=0.7 → 0.5 → 0.3。这创造了一个从偏向高资源语言到更均匀采样的进程，使模型在学习低资源语言之前能够建立强大的多语言基础。

**渐进式语言添加**：我们不是同时训练所有语言，而是在每个阶段策略性地添加语言（60 → 110 → 1,833）。这通过避免在有限的低资源数据上进行过多轮次，同时仍能实现强劲性能，从而最大化学习效率。

**模型合并**：我们在衰减阶段训练了三种不同的变体（侧重英语的、110 种语言的、所有语言的），并使用 **TIES** 合并技术将它们的长处结合到最终模型中。

## 结果

### 自然语言理解

**英语性能**：在英语 GLUE 基准测试（表 1）中，mmBERT base 取得了强劲的性能，显著优于 XLM-R（多语言 RoBERTa）base 和 mGTE base 等其他多语言模型，同时与纯英语模型保持竞争力，尽管 mmBERT 的训练数据中英语占比不到 25%。

**多语言性能**：如 **表 2** 所示，与 XLM-R 相比，mmBERT 在 XTREME 基准测试上显示出显著改进。显著的提升包括在 XNLI 分类上的强劲表现，在 TyDiQA 等问答任务上的实质性改进，以及在 PAWS-X 和 XCOPA 跨语言理解任务上的竞争性结果。

该模型在大多数类别中表现良好，但一些结构化预测任务（如 NER 和词性标注）除外，这可能是由于分词器差异影响了词边界检测。在这些类别上，它的表现与上一代模型大致相当，但可以应用于更多语言。

### 检索性能

**英语检索**：尽管 mmBERT 是为大规模多语言场景设计的，但在 MTEB v2 英语基准测试（表 3）中，mmBERT 相比之前的多语言模型显示出显著提升，甚至与 ModernBERT 等纯英语模型的能力持平！

**多语言检索**：与其他模型相比，mmBERT 在 MTEB v2 多语言基准测试中显示出持续的改进（表 4）。

**代码检索**：由于采用了现代分词器（基于 Gemma 2），mmBERT 也显示出强大的编码性能（表 5），使得 mmBERT 适用于任何类型的文本数据。唯一表现优于它的模型是 EuroBERT，该模型能够使用非公开访问的 Stack v2 数据集。

## 在衰减阶段学习语言

mmBERT 最显著的新颖特性之一是证明了低资源语言可以在短暂的训练衰减阶段被有效学习。我们通过在仅在最后 100B Token 衰减阶段引入的语言上进行测试，验证了这种方法。

**显著的性能提升**：在 TiQuaD（提格里尼亚语）和 FoQA（法罗语）上进行测试时，我们观察到当这些语言被纳入衰减阶段后，性能有实质性改进，如 **图 2** 所示。结果证明了我们渐进式语言学习方法的有效性。

**与大型模型竞争**：尽管仅在最终训练阶段接触到这些语言，mmBERT 达到的性能水平超过了更大的模型。在已有 LLM 基准测试的法罗语问答任务上，mmBERT 的表现优于 Google Gemini 2.5 Pro 和 OpenAI o3。

**快速学习机制**：衰减阶段语言学习的成功源于模型能够利用其在早期阶段建立的强大多语言基础。当接触到新语言时，模型可以快速调整现有的跨语言表示，而不是从头开始学习。

模型合并优势：通过TIES合并技术，最终的mmBERT模型在保留大部分衰退阶段改进的同时，成功融合了以英语为中心和高资源变体的优势。

## 效率提升

mmBERT通过继承自ModernBERT的架构改进，相比以往的多语言编码器模型实现了显著的效率提升：

吞吐性能：如图3所示，在不同序列长度下，mmBERT处理文本的速度明显快于现有的多语言模型。无论是小型还是基础模型，相比以往的多语言编码器都展现出大幅的速度提升。

现代架构优势：效率提升主要来自两项关键技术改进：
- Flash Attention 2：优化的注意力计算机制，提升内存使用效率和速度
- 去填充技术：在处理过程中消除不必要的填充Token

序列长度扩展：与受限于512个Token的旧模型不同，mmBERT能高效处理长达8,192个Token的序列，同时保持高吞吐量。这使其适用于多语言应用中日益常见的长文档处理任务。

能效优势：更好的吞吐性能与现代架构相结合，降低了推理计算成本，使mmBERT在大规模多语言支持的生产部署中更具实用性。

这些效率改进不仅使mmBERT比以往的多语言编码器更准确，也使其在实际应用中显著更具实用性。

## 使用示例

只需几行代码即可使用这些模型！

```python
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

tokenizer = AutoTokenizer.from_pretrained("jhu-clsp/mmBERT-base")
model = AutoModelForMaskedLM.from_pretrained("jhu-clsp/mmBERT-base")

def predict_masked_token(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    mask_indices = torch.where(inputs["input_ids"] == tokenizer.mask_token_id)
    predictions = outputs.logits[mask_indices]
    top_tokens, top_indices = torch.topk(predictions, 5, dim=-1)
    return [tokenizer.decode(token) for token in top_indices[0]]


texts = [
    "The capital of France is <mask>.",
    "La capital de España es <mask>.",
    "Die Hauptstadt von Deutschland ist <mask>.",
]

for text in texts:
    predictions = predict_masked_token(text)
    print(f"Text: {text}")
    print(f"Predictions: {predictions}\n")

```

## 微调示例

### 编码器

```python
import argparse

from datasets import load_dataset
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
)
from sentence_transformers.evaluation import TripletEvaluator
from sentence_transformers.losses import CachedMultipleNegativesRankingLoss
from sentence_transformers.training_args import BatchSamplers

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--lr", type=float, default=8e-5)
    parser.add_argument("--model_name", type=str, default="jhu-clsp/mmBERT-small")
    args = parser.parse_args()
    lr = args.lr
    model_name = args.model_name
    model_shortname = model_name.split("/")[-1]

    
    model = SentenceTransformer(model_name)

    
    dataset = load_dataset(
        "sentence-transformers/msmarco-co-condenser-margin-mse-sym-mnrl-mean-v1",
        "triplet-hard",
        split="train",
    )
    dataset_dict = dataset.train_test_split(test_size=1_000, seed=12)
    train_dataset = dataset_dict["train"].select(range(1_250_000))
    eval_dataset = dataset_dict["test"]

    
    loss = CachedMultipleNegativesRankingLoss(model, mini_batch_size=16)  

    run_name = f"{model_shortname}-DPR-{lr}"
    
    args = SentenceTransformerTrainingArguments(
        
        output_dir=f"output/{model_shortname}/{run_name}",
        
        num_train_epochs=1,
        per_device_train_batch_size=512,
        per_device_eval_batch_size=512,
        warmup_ratio=0.05,
        fp16=False,  
        bf16=True,  
        batch_sampler=BatchSamplers.NO_DUPLICATES,  
        learning_rate=lr,
        
        save_strategy="steps",
        save_steps=500,
        save_total_limit=2,
        logging_steps=500,
        run_name=run_name,  
    )

    
    dev_evaluator = TripletEvaluator(
        anchors=eval_dataset["query"],
        positives=eval_dataset["positive"],
        negatives=eval_dataset["negative"],
        name="msmarco-co-condenser-dev",
    )
    dev_evaluator(model)

    
    trainer = SentenceTransformerTrainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        loss=loss,
        evaluator=dev_evaluator,
    )
    trainer.train()

    
    dev_evaluator(model)

    
    model.save_pretrained(f"output/{model_shortname}/{run_name}/final")

    
    model.push_to_hub(run_name, private=False)

if __name__ == "__main__":
    main()

```

```python
from datasets import load_dataset
from pylate import losses, models, utils
from sentence_transformers import (
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
)

def main():
    
    train = load_dataset(
        path="lightonai/ms-marco-en-bge",
        name="train",
    )

    queries = load_dataset(
        path="lightonai/ms-marco-en-bge",
        name="queries",
    )

    documents = load_dataset(
        path="lightonai/ms-marco-en-bge",
        name="documents",
    )

    
    train.set_transform(
        utils.KDProcessing(queries=queries, documents=documents).transform,
    )

    
    num_train_epochs = 1
    lr = 8e-5
    batch_size = 16
    accum_steps = 1
    model_name = "jhu-clsp/mmBERT-small"
    model_shortname = model_name.split("/")[-1]

    
    run_name = f"{model_shortname}-colbert-KD-{lr}"
    output_dir = f"output/{model_shortname}/{run_name}"

    
    model = models.ColBERT(model_name_or_path=model_name)

    
    args = SentenceTransformerTrainingArguments(
        output_dir=output_dir,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=batch_size,
        fp16=False,  
        bf16=True,  
        run_name=run_name,
        logging_steps=10,
        learning_rate=lr,
        gradient_accumulation_steps=accum_steps,
        warmup_ratio=0.05,
    )

    
    train_loss = losses.Distillation(model=model)

    
    trainer = SentenceTransformerTrainer(
        model=model,
        args=args,
        train_dataset=train,
        loss=train_loss,
        data_collator=utils.ColBERTCollator(tokenize_fn=model.tokenize),
    )

    
    trainer.train()

    model.save_pretrained(f"{output_dir}/final")

if __name__ == "__main__":
    main()

```

```python
import logging

from datasets import load_dataset

from sentence_transformers import (
    SparseEncoder,
    SparseEncoderModelCardData,
    SparseEncoderTrainer,
    SparseEncoderTrainingArguments,
)
from sentence_transformers.sparse_encoder.evaluation import SparseNanoBEIREvaluator
from sentence_transformers.sparse_encoder.losses import SparseMultipleNegativesRankingLoss, SpladeLoss
from sentence_transformers.training_args import BatchSamplers

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)


model = SparseEncoder(
    "jhu-clsp/mmBERT-small",
    model_card_data=SparseEncoderModelCardData(
        language="en",
        license="apache-2.0",
    )
)


full_dataset = load_dataset("sentence-transformers/natural-questions", split="train").select(range(100_000))
dataset_dict = full_dataset.train_test_split(test_size=1_000, seed=12)
train_dataset = dataset_dict["train"]
eval_dataset = dataset_dict["test"]


loss = SpladeLoss(
    model=model,
    loss=SparseMultipleNegativesRankingLoss(model=model),
    query_regularizer_weight=5e-5,
    document_regularizer_weight=3e-5,
)

```python
run_name = "splade-distilbert-base-uncased-nq"
args = SparseEncoderTrainingArguments(
    
    output_dir=f"models/{run_name}",
    
    num_train_epochs=1,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    learning_rate=2e-5,
    warmup_ratio=0.1,
    fp16=True,  
    bf16=False,  
    batch_sampler=BatchSamplers.NO_DUPLICATES,  
    
    eval_strategy="steps",
    eval_steps=1000,
    save_strategy="steps",
    save_steps=1000,
    save_total_limit=2,
    logging_steps=200,
    run_name=run_name,  
)


dev_evaluator = SparseNanoBEIREvaluator(dataset_names=["msmarco", "nfcorpus", "nq"], batch_size=16)


trainer = SparseEncoderTrainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    loss=loss,
    evaluator=dev_evaluator,
)
trainer.train()


dev_evaluator(model)


model.save_pretrained(f"models/{run_name}/final")


model.push_to_hub(run_name)

```

```python
import logging
import traceback

import torch
from datasets import load_dataset

from sentence_transformers import SentenceTransformer
from sentence_transformers.cross_encoder import (
    CrossEncoder,
    CrossEncoderModelCardData,
    CrossEncoderTrainer,
    CrossEncoderTrainingArguments,
)
from sentence_transformers.cross_encoder.evaluation import (
    CrossEncoderNanoBEIREvaluator,
    CrossEncoderRerankingEvaluator,
)
from sentence_transformers.cross_encoder.losses import BinaryCrossEntropyLoss
from sentence_transformers.evaluation import SequentialEvaluator
from sentence_transformers.util import mine_hard_negatives


logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)


def main():
    model_name = "jhu-clsp/mmBERT-small"

    train_batch_size = 64
    num_epochs = 1
    num_hard_negatives = 5  

    
    model = CrossEncoder(
        model_name,
        model_card_data=CrossEncoderModelCardData(
            language="en",
            license="apache-2.0",
        ),
    )
    print("模型最大长度:", model.max_length)
    print("模型标签数量:", model.num_labels)

    
    logging.info("读取 gooaq 训练数据集")
    full_dataset = load_dataset("sentence-transformers/gooaq", split="train").select(range(100_000))
    dataset_dict = full_dataset.train_test_split(test_size=1_000, seed=12)
    train_dataset = dataset_dict["train"]
    eval_dataset = dataset_dict["test"]
    logging.info(train_dataset)
    logging.info(eval_dataset)

    
    embedding_model = SentenceTransformer("sentence-transformers/static-retrieval-mrl-en-v1", device="cpu")
    hard_train_dataset = mine_hard_negatives(
        train_dataset,
        embedding_model,
        num_negatives=num_hard_negatives,  
        margin=0,  
        range_min=0,  
        range_max=100,  
        sampling_strategy="top",  
        batch_size=4096,  
        output_format="labeled-pair",  
        use_faiss=True,
    )
    logging.info(hard_train_dataset)

    
    
    
    

    
    
    loss = BinaryCrossEntropyLoss(model=model, pos_weight=torch.tensor(num_hard_negatives))

    
    nano_beir_evaluator = CrossEncoderNanoBEIREvaluator(
        dataset_names=["msmarco", "nfcorpus", "nq"],
        batch_size=train_batch_size,
    )

    
    
    
    hard_eval_dataset = mine_hard_negatives(
        eval_dataset,
        embedding_model,
        corpus=full_dataset["answer"],  
        num_negatives=30,  
        batch_size=4096,
        include_positives=True,
        output_format="n-tuple",
        use_faiss=True,
    )
    logging.info(hard_eval_dataset)
    reranking_evaluator = CrossEncoderRerankingEvaluator(
        samples=[
            {
                "query": sample["question"],
                "positive": [sample["answer"]],
                "documents": [sample[column_name] for column_name in hard_eval_dataset.column_names[2:]],
            }
            for sample in hard_eval_dataset
        ],
        batch_size=train_batch_size,
        name="gooaq-dev",
        
        
        always_rerank_positives=False,
    )

    
    evaluator = SequentialEvaluator([reranking_evaluator, nano_beir_evaluator])
    evaluator(model)

    
    short_model_name = model_name if "/" not in model_name else model_name.split("/")[-1]
    run_name = f"reranker-{short_model_name}-gooaq-bce"
    args = CrossEncoderTrainingArguments(
        
        output_dir=f"models/{run_name}",
        
        num_train_epochs=num_epochs,
        per_device_train_batch_size=train_batch_size,
        per_device_eval_batch_size=train_batch_size,
        learning_rate=2e-5,
        warmup_ratio=0.1,
        fp16=False,  
        bf16=True,  
        dataloader_num_workers=4,
        load_best_model_at_end=True,
        metric_for_best_model="eval_gooaq-dev_ndcg@10",
        
        eval_strategy="steps",
        eval_steps=1000,
        save_strategy="steps",
        save_steps=1000,
        save_total_limit=2,
        logging_steps=200,
        logging_first_step=True,
        run_name=run_name,  
        seed=12,
    )

    
    trainer = CrossEncoderTrainer(
        model=model,
        args=args,
        train_dataset=hard_train_dataset,
        loss=loss,
        evaluator=evaluator,
    )
    trainer.train()

    
    evaluator(model)

    
    final_output_dir = f"models/{run_name}/final"
    model.save_pretrained(final_output_dir)

    
    
    try:
        model.push_to_hub(run_name)
    except Exception:
        logging.error(
            f"上传模型到 Hugging Face Hub 时出错:\n{traceback.format_exc()}如需手动上传，您可以运行 "
            f"`huggingface-cli login`，然后使用 `model = CrossEncoder({final_output_dir!r})` 加载模型，"
            f"再使用 `model.push_to_hub('{run_name}')` 保存。"
        )


if __name__ == "__main__":
    main()

```

## 模型系列与链接

标准模型：

- mmBERT-small（总计1.4亿参数，非嵌入层4200万）
- mmBERT-base（总计3.07亿参数，非嵌入层1.1亿）

研究资源：

- 🤗 mmBERT 模型集合
- 📝 论文
- 🗂️ 训练数据（3万亿+ Token，完全开源）
- 💻 GitHub 仓库
- 📊 训练检查点（用于研究训练或继续预训练）

---

> 本文由AI自动翻译，原文链接：[mmBERT: ModernBERT goes Multilingual](https://huggingface.co/blog/mmbert)
> 
> 翻译时间：2026-02-13 04:25
