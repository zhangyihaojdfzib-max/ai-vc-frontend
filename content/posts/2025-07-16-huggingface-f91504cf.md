---
title: Ettin套件：首个SoTA配对编码器与解码器模型
title_original: 'Ettin Suite: SoTA Paired Encoders and Decoders'
date: '2025-07-16'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ettin
author: ''
summary: 本文介绍了Ettin套件，这是首个使用相同数据、架构和训练方案训练的最先进配对编码器与解码器模型套件。通过将ModernBERT的训练方案应用于解码器模型，Ettin在1700万至10亿参数规模上均实现了超越Llama
  3.2和SmolLM2等基线的性能。该研究首次在受控条件下对掩码语言建模和因果语言建模两种目标进行公平比较，为开源模型在编码器和解码器两个类别均提供了最先进的性能基准。
categories:
- AI研究
tags:
- 语言模型
- 编码器-解码器
- 开源模型
- 预训练
- 基准测试
draft: false
translated_at: '2026-03-12T04:38:45.854349'
---

# Ettin Suite：SoTA 配对编码器与解码器

## 摘要

如果将 ModernBERT 的训练方案应用于仅解码器模型，会发生什么？结果是一个性能超越 Llama 3.2 1B 和 SmolLM2 的、最先进的解码器语言模型！

我们引入了一种新的开源数据训练方案，用于复现仅编码器的 ModernBERT 模型（并且实际上超越了它！）。然后，我们将完全相同的方案应用于仅解码器模型。这是首次，我们拥有了在同一设置下训练、但采用两种不同训练目标的两个最先进模型：掩码语言建模（MLM）和因果语言建模（CLM）。

这篇博文介绍了 **Ettin**，这是首个 **SoTA 配对的仅编码器和仅解码器模型套件**（参数规模 1700 万至 10 亿），它们使用相同的数据（2 万亿 Token）、架构和训练方案进行训练。Ettin 使得在架构之间进行真正的公平比较成为可能，并在两个类别中都为开源数据模型提供了**最先进的性能**。我们随后进一步探讨了是否可能从解码器出发得到一个有竞争力的编码器，反之亦然。

如果您有兴趣尝试这些模型，**本博文末尾提供了一些示例代码！**

## 编码器 vs 解码器：架构分野

LLM 社区在很大程度上已趋同于使用像 GPT、Llama 和 Qwen 这样的仅解码器模型。它们的生成能力令人印象深刻，但这种关注点正在分散人们对其他类别模型的注意力，例如像 BERT 这样的仅编码器模型。

然而，类似 BERT 的编码器模型仍然是生产系统中用于分类、检索和嵌入任务的骨干。对于判别式任务，它们更快、内存效率更高，并且通常更准确。关键区别在于它们的注意力模式：

*   **编码器模型**使用双向注意力，允许每个 Token 都能“看到”序列中的所有其他 Token（完全可见）。
*   **解码器模型**使用因果注意力，其中 Token 只能“看到”先前的 Token，以实现自回归生成。

虽然解码器模型经历了快速的创新，但编码器模型的发展曾一度停滞——直到最近，像 **ModernBERT** 这样的努力使其现代化。但哪种架构更好呢？以往编码器和解码器之间的比较使用了不同的数据集、架构和训练方案，因此很难判断。

以双头北欧巨人命名的 **Ettin** 提供了一个**受控的比较**，通过在相同的数据、相同的模型形状和相同的训练方案上训练两种架构。它们仅在注意力模式和训练目标上有所不同！

## 训练方案：适用于两种架构的现代技术

我们基于 ModernBERT 的方案进行构建，该方案借鉴了仅解码器模型的现代技术并将其引入编码器训练。这为训练两种架构提供了一个强大的基础。

### 规模

我们训练了六种不同的规模，参数范围从 1700 万到 10 亿。这使我们能够测试规模效应，并为您提供多种多样的模型！
无论您需要极快的设备端模型，还是功能强大但稍慢的模型，我们都能满足！

### 三阶段训练过程

我们采用全面的三阶段训练方法以最大化性能：

**阶段 1 - 预训练（1.7 万亿 Token）**：我们从高质量数据源的多样化混合开始，在较短的上下文（1024 Token）上进行训练，以建立强大的基础知识。

**阶段 2 - 上下文扩展（2500 亿 Token）**：我们使用更高质量过滤后的数据，将上下文长度增加到 8K Token，使模型能够理解更长的文档和更复杂的关系。

**阶段 3 - 衰减（1000 亿 Token）**：我们使用包括科学论文、教科书和精选内容在内的优质数据源完成训练，同时逐步降低学习率。

### 现代架构组件

我们的编码器模型获得了 ModernBERT 速度的所有优势，使其比前几代编码器快得多。

### 数据来源与质量

与 ModernBERT 不同，**我们所有的训练数据都是公开且可复现的**：

您可以继续在新数据上训练这些模型，或提出新的方案以进一步改进结果！

## 编码器结果：超越 ModernBERT

我们的编码器模型在所有任务和模型规模上都**超越了 ModernBERT**，同时使用了完全开源的训练数据。由于我们提供了广泛的规模选择，您现在可以在较小规模上使用 ModernBERT 风格的模型（非常适合设备端或快速推理），或者使用性能碾压竞争对手的 10 亿规模编码器。

## 解码器结果：超越 Llama 3.2 和 SmolLM2

将相同的方案应用于解码器模型产生了同样令人印象深刻的结果，我们的模型**超越或匹配了已建立的基线**，如 Llama 3.2 和 SmolLM2：

在像 SciQ 这样知识密集型的任务上，收益尤其显著，这反映了我们高质量训练数据混合的好处。这些结果表明，我们的训练方案在两种架构范式中都创造了真正强大的模型。

## 公平对决：同等条件下的编码器 vs 解码器

我们首次可以公平地比较使用相同数据和方案训练的编码器和解码器架构。结果揭示了即使在所有其他因素都受控的情况下仍然存在的基本架构优势：

### 架构特定优势依然存在

结果显示出清晰的模式：

**编码器主导分类和检索**：在 MNLI 分类任务上，即使是 1.5 亿参数的编码器（89.2）也优于 4 亿参数的解码器（88.2）。对于检索任务，差距较小但仍然明显——尤其是当解码器未使用 MNTP 训练时。

**解码器擅长生成**：在生成任务上，解码器保持持续优势，并且性能差距在更大的模型规模上实际上扩大了。

**规模并非总是关键**：在分类任务上，一个 4 亿参数的编码器击败了 10 亿参数的解码器；而在生成任务上，一个 4 亿参数的解码器击败了 10 亿参数的编码器。

### 跨目标训练效果不佳

由于缺乏新的编码器模型，像 **LLM2Vec** 这样的工作提出继续使用 MLM 对解码器进行预训练。我们现在可以测试这种策略的有效性！

我们切换了训练目标，并使用相反的目标继续训练我们的模型，额外增加了 500 亿 Token。这是我们发现的：

*   **从解码器转换的编码器**：在分类/检索任务上通常仍落后于原生编码器。
*   **从编码器转换的解码器**：比原生解码器差得多，尤其是在更大规模上。这可能是因为编码器是用 MLM 而不是像 LLM2Vec 提出的（以及我们用于从解码器转换编码器的方案中使用的）MNTP（掩码下一 Token 预测）训练的。

这表明架构选择从根本上很重要，而不仅仅是训练目标。

## 超越性能：理解模型行为

借助相同的训练数据，我们可以研究不同目标如何影响学习。例如，使用 WinoGender 基准分析性别偏见揭示了：

*   **编码器模型**更倾向于使用中性代词（60%+ 中性 vs 解码器的 30%+）。
*   两种架构都**显示出男性偏见**，但解码器稍强一些。
*   **跨目标训练**以可测量的方式影响偏见模式。

这为系统研究训练目标如何影响模型行为（超越准确性指标）打开了大门。

## 使用示例

只需几行代码即可使用这些模型！

### 编码器

```python
from transformers import AutoTokenizer, AutoModel


tokenizer = AutoTokenizer.from_pretrained("jhu-clsp/ettin-encoder-150m")
model = AutoModel.from_pretrained("jhu-clsp/ettin-encoder-150m")

```python
def predict_masked_token(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    
    
    mask_indices = torch.where(inputs["input_ids"] == tokenizer.mask_token_id)
    predictions = outputs.logits[mask_indices]
    
    
    top_tokens = torch.topk(predictions, 5, dim=-1)
    return [tokenizer.decode(token) for token in top_tokens.indices[0]]


masked_text = "The capital of France is [MASK]."
predictions = predict_masked_token(masked_text)
print(f"Predictions: {predictions}")
```

对于分类和检索任务，请使用编码器模型：你可能也想为这些任务使用一个经过微调的版本。

### 解码器

对于文本生成任务，请使用解码器模型：

```python
from transformers import AutoTokenizer, AutoModelForCausalLM


tokenizer = AutoTokenizer.from_pretrained("jhu-clsp/ettin-decoder-150m")
model = AutoModelForCausalLM.from_pretrained("jhu-clsp/ettin-decoder-150m")


prompt = "The future of artificial intelligence is"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(inputs.input_ids, max_length=50, temperature=0.7)
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

## 微调示例

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
    parser.add_argument("--model_name", type=str, default="jhu-clsp/ettin-encoder-150m")
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
    model_name = "jhu-clsp/ettin-encoder-150m"
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
    "jhu-clsp/ettin-encoder-150m",
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
```

```python
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
    model_name = "jhu-clsp/ettin-encoder-150m"

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

# 完整训练

```bash
python trl/scripts/sft.py \
    --model_name_or_path jhu-clsp/ettin-decoder-17m \
    --dataset_name trl-lib/Capybara \
    --learning_rate 2.0e-5 \
    --num_train_epochs 1 \
    --packing \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 8 \
    --gradient_checkpointing \
    --eos_token '<|im_end|>' \
    --eval_strategy steps \
    --eval_steps 100 \
    --output_dir ettin-decoder-17m \
    --push_to_hub

```

```bash
python trl/scripts/sft.py \
    --model_name_or_path jhu-clsp/ettin-decoder-17m \
    --dataset_name trl-lib/Capybara \
    --learning_rate 2.0e-4 \
    --num_train_epochs 1 \
    --packing \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 8 \
    --gradient_checkpointing \
    --eos_token '<|im_end|>' \
    --eval_strategy steps \
    --eval_steps 100 \
    --use_peft \
    --lora_r 32 \
    --lora_alpha 16 \
    --output_dir ettin-decoder-17m \
    --push_to_hub

```

withsft.py:

```python
import argparse

from datasets import load_dataset
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer
from transformers.models.auto.modeling_auto import MODEL_FOR_IMAGE_TEXT_TO_TEXT_MAPPING_NAMES

from trl import (
    ModelConfig,
    ScriptArguments,
    SFTConfig,
    SFTTrainer,
    TrlParser,
    clone_chat_template,
    get_kbit_device_map,
    get_peft_config,
    get_quantization_config,
)


def main(script_args, training_args, model_args):
    
    
    
    quantization_config = get_quantization_config(model_args)
    model_kwargs = dict(
        revision=model_args.model_revision,
        trust_remote_code=model_args.trust_remote_code,
        attn_implementation=model_args.attn_implementation,
        torch_dtype=model_args.torch_dtype,
        use_cache=False if training_args.gradient_checkpointing else True,
        device_map=get_kbit_device_map() if quantization_config is not None else None,
        quantization_config=quantization_config,
    )

    
    config = AutoConfig.from_pretrained(model_args.model_name_or_path)
    valid_image_text_architectures = MODEL_FOR_IMAGE_TEXT_TO_TEXT_MAPPING_NAMES.values()

    if config.architectures and any(arch in valid_image_text_architectures for arch in config.architectures):
        from transformers import AutoModelForImageTextToText

        model_kwargs.pop("use_cache", None)  
        model = AutoModelForImageTextToText.from_pretrained(model_args.model_name_or_path, **model_kwargs)
    else:
        model = AutoModelForCausalLM.from_pretrained(model_args.model_name_or_path, **model_kwargs)

    
    tokenizer = AutoTokenizer.from_pretrained(
        model_args.model_name_or_path, trust_remote_code=model_args.trust_remote_code, use_fast=True
    )

    
    if tokenizer.chat_template is None:
        
        model, tokenizer = clone_chat_template(model, tokenizer, "Qwen/Qwen3-0.6B")

    
    
    
    dataset = load_dataset(script_args.dataset_name, name=script_args.dataset_config)
```

trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset[script_args.dataset_train_split],
        eval_dataset=dataset[script_args.dataset_test_split] if training_args.eval_strategy != "no" else None,
        processing_class=tokenizer,
        peft_config=get_peft_config(model_args),
    )

    trainer.train()

    
    trainer.save_model(training_args.output_dir)
    if training_args.push_to_hub:
        trainer.push_to_hub(dataset_name=script_args.dataset_name)


def make_parser(subparsers: argparse._SubParsersAction = None):
    dataclass_types = (ScriptArguments, SFTConfig, ModelConfig)
    if subparsers is not None:
        parser = subparsers.add_parser("sft", help="Run the SFT training script", dataclass_types=dataclass_types)
    else:
        parser = TrlParser(dataclass_types)
    return parser


if __name__ == "__main__":
    parser = make_parser()
    
    
    
    script_args, training_args, model_args, _ = parser.parse_args_and_config(return_remaining_strings=True)
    main(script_args, training_args, model_args)

```

## 模型系列与链接

完整的 Ettin 套件包含六个不同规模的模型（编码器和解码器均有）：

标准模型：

- ettin-encoder-17m/ettin-decoder-17m（1700万参数）
- ettin-encoder-32m/ettin-decoder-32m（3200万参数）
- ettin-encoder-68m/ettin-decoder-68m（6800万参数）
- ettin-encoder-150m/ettin-decoder-150m（1.5亿参数）
- ettin-encoder-400m/ettin-decoder-400m（4亿参数）
- ettin-encoder-1b/ettin-decoder-1b（10亿参数）

研究资源：

- 🤗 Ettin 模型集合
- 📝 论文
- 🗂️ 训练数据（2万亿+ Token，完全开源）
- 💻 GitHub 仓库
- 📊 250+ 训练检查点，用于研究训练动态或知识学习

---

> 本文由AI自动翻译，原文链接：[Ettin Suite: SoTA Paired Encoders and Decoders](https://huggingface.co/blog/ettin)
> 
> 翻译时间：2026-03-12 04:38
