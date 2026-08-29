---
title: Training and Finetuning Multi-Vector Embedding Models with Sentence Transformers
title_original: Training and Finetuning Multi-Vector Embedding Models with Sentence
  Transformers
date: '2026-08-26'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/train-multi-vector-encoder
author: ''
summary: '[翻译失败，原文如下]


  # Training and Finetuning Multi-Vector Embedding Models with Sentence Transformers


  Sentence Transformersis a Python library for using an...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-29T08:48:42.535169'
---

[翻译失败，原文如下]

# Training and Finetuning Multi-Vector Embedding Models with Sentence Transformers

Sentence Transformersis a Python library for using and training embedding and reranker models for a wide range of applications, such as retrieval augmented generation, semantic search, semantic textual similarity, and more. Its v6.0 update introduces a fourth model type:MultiVectorEncoder, for ColBERT-style late interaction retrieval, alongside a complete training approach for it. In this blogpost, I'll show you how to use it to finetune a multi-vector model that outperforms general-purpose retrievers on your data. This method can also train strong new multi-vector models from scratch. Everything below runs onpip install -U "sentence-transformers[train]".

Finetuning multi-vector models involves several components: the model itself, datasets, loss functions, training arguments, evaluators, and the trainer class. I'll have a look at each of these components, accompanied by practical examples of how they can be used for finetuning strong multi-vector models.

Lastly, in theEvaluationsection, I'll show you that my finetunedmulti-vector-encoder/mLateOn-medicalmodel, trained in 14.5 hours on a single RTX 3090 alongside this blogpost, easily outperforms every general-purpose retrieval model I could find on my medical retrieval evaluation: dense, sparse, lexical, and multi-vector alike.

![NDCG@10 on MIRIAD versus active parameters: the finetuned mLateOn-medical reaches the top at a fraction of the size of the strongest general-purpose models](/images/posts/ab2e72d84a66.png)

If you're interested in finetuning dense embedding models, sparse embedding models, or rerankers instead, then consider reading through my priorTraining and Finetuning Embedding Models,Training and Finetuning Sparse Embedding Models, andTraining and Finetuning Reranker Modelsblogposts.

This blogpost is abouttrainingmulti-vector models. If you want to learn how tousethem, from loading and encoding to indexing in vector databases, see the companionMulti-Vector (Late Interaction) Embedding Models with Sentence Transformersblogpost.

- What are Multi-Vector models?
- Why Finetune?
- Training Components
- ModelFinetuning an existing multi-vector modelBuilding one from a base transformerWhich starting point should you pick?
- DatasetData on the Hugging Face HubLocal DataDataset Format
- Loss Function
- Training Arguments
- Evaluator
- TrainerCallbacksMulti-Dataset Training
- EvaluationOptimizing the index
- Acknowledgements
- Additional ResourcesTraining ExamplesDocumentation

- Finetuning an existing multi-vector model
- Building one from a base transformer
- Which starting point should you pick?

- Data on the Hugging Face Hub
- Local Data
- Dataset Format

- Callbacks
- Multi-Dataset Training

- Optimizing the index

- Training Examples
- Documentation

## What are Multi-Vector models?

A dense embedding model compresses a whole text into a single vector, and similarity is one dot product between two such summaries. A multi-vector model (also called a late-interaction or ColBERT-style model) skips that compression. It keepsone small vector per tokenand scores a query against a document with the MaxSim operator, where every query token finds its best-matching document token and the scores are summed. Token-level matching preserves exactly the fine-grained signals that a single vector has to average away, which usually means stronger retrieval, at the cost of a bigger index.

The companionMulti-Vector Embedding Modelsblogpost covers the architecture, encoding, scoring, and indexing in detail, so I'll keep this section short and get to the training.

![Dense embedding versus multi-vector late interaction](/images/posts/1743f5838524.gif)

## Why Finetune?

Finetuning multi-vector models significantly improves their retrieval performance on your specific domain: the vocabulary, the query style, and the notion of relevance all differ between web search, legal discovery, code search, and scientific literature review. Because queries and documents are matched token by token, multi-vector models pick up fine-grained domain signals that single-vector models tend to average away, and they respond very well to even modest amounts of in-domain finetuning data.

Beyond that, most released retrieval models were configured for short passages. The classic ColBERT checkpoints truncate documents at 180 or 300 tokens, and many popular dense models at 256 or 512, because their MS MARCO-style training data rarely goes beyond that. If your documents are long, these models silently discard most of every document before scoring it. On my medical evaluation with passages averaging 941 tokens, I measured that this truncation costs up to 0.24 NDCG@10, considerably more than any difference between model architectures. When you train your own model, you configure the document length thatyourdata needs.

LightOn ran into this same dynamic with code retrieval, where generalLateOnwasn't enough and they trainedLateOn-Code. Your domain, whether that's medical, legal, financial, or your company's internal documents, is not getting an official model. This blogpost shows you how to build it yourself, in a matter of hours, on a single consumer GPU.

## Training Components

Training MultiVectorEncoder models involves the following components:

1. Model: The model to finetune or the architecture to build fresh.
2. Dataset: The data used for training and evaluation.
3. Loss Function: A function that measures the model's performance and guides the optimization process.
4. Training Arguments(optional): Parameters that impact training performance, tracking, and debugging.
5. Evaluator(optional): A class for evaluating the model before, during, or after training.
6. Trainer: Brings together all training components.

Let's take a closer look at each component.

## Model

Multi-vector training gives you a real choice of starting point, and it matters more than you might expect.

### Finetuning an existing multi-vector model

If you want to further finetune an existing multi-vector model, you don't have to worry about the architecture at all:

```python
from sentence_transformers import MultiVectorEncoder


model = MultiVectorEncoder(
    "lightonai/mLateOn-unsupervised",
    model_kwargs={"torch_dtype": "float32"},
    processor_kwargs={"model_max_length": 8192},  
)

```

The checkpoint brings its own recipe along: its query and document marker tokens, its projection head, its scoring skiplist. For finetuning, you generally want to keep all of that and change only what your data demands. The first thing to check is the length configuration, since many released checkpoints cap documents at 180 to 512 tokens (seeWhy Finetune?), and my medical passages run to 1,400 tokens. The mLateOn family already serves the backbone's full 8192 token context, but if your starting checkpoint carries caps, lift them:

```python


model[0].query_length = None
model[0].document_length = None

```

With the per-task caps unset, truncation falls back to the tokenizer'smodel_max_length, which is why I configure that limit at load time above.

I made one more change, adding a punctuation skiplist that excludes punctuation tokens from document-side scoring and storage. In a 4-way ablation (none, punctuation, stopwords, both) it modestly won on quality, and it shrinks the document index by 9.6% on this data for free:

```python
import string


model[2].skiplist_words = list(string.punctuation)
model[2].resolve_with_tokenizer(model.tokenizer)  

```

### Building one from a base transformer

You can also pointMultiVectorEncoderat any base transformer, and a fresh, randomly initialized token-level projection is appended for you:

```python
from sentence_transformers import MultiVectorEncoder

model = MultiVectorEncoder("answerdotai/ModernBERT-base", model_kwargs={"torch_dtype": "float32"})







```

[翻译失败，原文如下]

That's the classic ColBERT pipeline: aTransformerproducing contextualized token embeddings, a token-levelDenseprojecting each of them down to 128 dimensions, aMultiVectorMaskdeciding which tokens count during scoring, and a token-levelNormalize. The projection starts random, so training is required before this model is useful. Interestingly, this works with strong dense embedding backbones too. A fresh projection onAlibaba-NLP/gte-modernbert-basereached within 0.03 of the existing-checkpoint starting points in my experiments, from nothing but the projection and 25k training pairs.

The classic ColBERT tokenization tricks ([MASK]query expansion,[Q]/[D]prefix tokens, a document length cap, a punctuation skiplist) are all off by default and configurable. SeeCreating Custom Modelsfor the full set. For what it's worth, I tested[MASK]query expansion in four configurations for my domain finetune and none of them made a measurable difference, so don't feel obliged to reach for the classic recipe.

### Which starting point should you pick?

I measured this directly while preparing this blogpost, taking six starting points and training each with the identical recipe on 25k medical question-passage pairs fromMIRIAD, then evaluating on 1,000 held-out questions against a 50,000 passage corpus:

The result surprised me, and it replicated across two model families. *The-unsupervisedcheckpoints adapt to a new domain far better than their finished siblings, overtaking them despite starting lower. These checkpoints sit after large-scale contrastive pretraining but before supervised finetuning on general retrieval, so they carry all the late-interaction structure with none of the general-purpose tuning that domain training then has to undo. The finished checkpoints, by contrast, barely moved or even regressed, at every learning rate I tried.

So, if the model family you like publishes a pre-supervised checkpoint, start there. If not, a fresh projection on a strong retrieval-pretrained backbone is a close runner-up. Continuing from a fully finished checkpoint is the weakest option for domain adaptation, despite being the most natural-feeling one.

## Dataset

TheMultiVectorEncoderTrainerusesdatasets.Datasetordatasets.DatasetDictinstances for training and evaluation. You can load data from theHugging Face Datasets Hubor use local data in whatever format you prefer (e.g. CSV, JSON, Parquet, Arrow, or SQL).

Note:Lots of public datasets that work out of the box with Sentence Transformers have been tagged withsentence-transformerson the Hugging Face Hub, so you can easily find them onhttps://huggingface.co/datasets?other=sentence-transformers. Consider browsing through these to find ready-to-go datasets that might be useful for your tasks, domains, or languages.

### Data on the Hugging Face Hub

You can use theload_datasetfunction to load data from datasets on the Hub:

```python
from datasets import load_dataset

train_dataset = load_dataset("tomaarsen/miriad-4.4M-split", split="train")

print(train_dataset)
"""
Dataset({
    features: ['question', 'passage_text'],
    num_rows: 4467542
})
"""

```

This is the dataset I'll train on in this blogpost: 4.4 million medical questions fromMIRIAD, each paired with the source passage that contains its answer (averaging 941 tokens). Simple (query, relevant passage) pairs like these are the easiest retrieval training data to collect for your own domain, and as you'll see, they're all you need.

### Local Data

You can also useload_datasetfor loading local data in common file formats:

```python
from datasets import load_dataset

dataset = load_dataset("csv", data_files="my_file.csv")

dataset = load_dataset("json", data_files="my_file.json")

```

And if your local data requires pre-processing, you can usedatasets.Dataset.from_dictto initialize your dataset with a dictionary of lists:

```python
from datasets import Dataset

queries = []
documents = []



dataset = Dataset.from_dict({
    "query": queries,
    "document": documents,
})

```

### Dataset Format

It is important that your dataset format matches your loss function (or that you choose a loss function that matches your dataset format). Verifying whether a dataset format works with a loss function involves two steps:

1. If your loss function requires aLabelaccording to theLoss Overviewtable, then your dataset must have acolumn named "label" or "score". This column is automatically taken as the label.
2. All columns not named "label" or "score" are consideredInputsaccording to theLoss Overviewtable. The number of remaining columns must match the number of valid inputs for your chosen loss. The names of these columns areirrelevant, only theorder matters.

There are two multi-vector specific conventions on top of this:

- Positional query and document assignment: the first column is embedded as thequeryand all following columns asdocuments, regardless of the column names. This default can be overridden per column via the standardrouter_mappingtraining argument.
- Knowledge distillation format: one column per candidate document, i.e.(query, document_1, ..., document_N, scores)wherescoresis a list of N teacher scores per row. For KD datasets that store query and documentIDsalongside separate text datasets (e.g.lightonai/ms-marco-en-bge), you can useresolve_idsto resolve the IDs to texts on the fly.

## Loss Function

Loss functions quantify how well a model performs for a given batch of data, allowing an optimizer to update the model weights to produce more favourable (i.e., lower) loss values. The right loss function for your task depends on the data you have and what you're trying to achieve. You can find a full list of options in theLoss Overview.

For the common case of question-answer or question-passage pairs, the workhorse is in-batch negatives training withMultiVectorMultipleNegativesRankingLoss, where every other document in the batch acts as a negative for each query. Bigger batches mean more negatives and stronger training, so in practice you'll want its GradCache variant,CachedMultiVectorMultipleNegativesRankingLoss, which decouples the effective batch size from what fits on your GPU:

```python
from sentence_transformers import MultiVectorEncoder
from sentence_transformers.multi_vector_encoder.losses import CachedMultiVectorMultipleNegativesRankingLoss

model = MultiVectorEncoder("lightonai/mLateOn-unsupervised", model_kwargs={"torch_dtype": "float32"})

loss = CachedMultiVectorMultipleNegativesRankingLoss(
    model=model,
    mini_batch_size=16,  
)

```

Themini_batch_sizeparameter bounds the memory by encoding documents in chunks of this size, while the effective contrastive batch size (128 in my run below, and in my ablations bigger batches bought nothing further) stays a free choice. GradCache guarantees identical results regardless of the chunk size, so lower it for smaller GPUs at only a wall-clock cost. When your document lengths vary a lot, consider its siblingmini_batch_num_tokens, which packs each chunk to a total token budget instead of a document count, so a chunk of unusually long documents can never spike your memory (mymini_batch_size=16at roughly 940 tokens per document corresponds tomini_batch_num_tokens=15_000).

One multi-vector specific trap is that the contrastive losses default toscale=1.0, unlike the dense embedding equivalent which defaults toscale=20.0. That 20.0 exists because a cosine similarity is a single value in [-1, 1], too narrow a range for a sharp softmax. A MaxSim score instead sums one best-match similarity per query token, so it already spans roughly [0, query_length]: a 32-token query can score up to 32. So don't copyscale=20.0over from a dense training script, since it would saturate the softmax and kill your gradients.

[翻译失败，原文如下]

For distillation from a stronger teacher, which is how the strongest general-purpose late-interaction models are trained, seeMultiVectorDistillKLDivLossand the Knowledge Distillation tab in theTraining Overviewdocumentation.

## Training Arguments

You can customize the training process using theMultiVectorEncoderTrainingArgumentsclass. This class lets you adjust parameters that can impact training speed and help you understand what's happening during training.

For more information on the most useful training arguments, check out theMulti-Vector Encoder > Training Overview > Training Arguments. It's worth reading to get the most out of your training.

Here's an example, using the values from my actual training run:

```python
from sentence_transformers import MultiVectorEncoderTrainingArguments
from sentence_transformers.base.sampler import BatchSamplers

args = MultiVectorEncoderTrainingArguments(
    
    output_dir="models/mLateOn-medical",
    
    num_train_epochs=1,
    per_device_train_batch_size=128,  
    per_device_eval_batch_size=16,
    learning_rate=1e-4,
    warmup_steps=0.05,
    prompts={"question": "[Q] ", "passage_text": "[D] "},  
    fp16=False,  
    bf16=True,  
    batch_sampler=BatchSamplers.NO_DUPLICATES,  
    
    eval_strategy="steps",
    eval_steps=0.1,
    save_strategy="steps",
    save_steps=0.05,
    logging_steps=0.01,
    run_name="mLateOn-medical",  
)

```

A few of these deserve a comment:

- prompts: training does not automatically apply the prompts stored in the model, so map them onto your training columns explicitly. Here that is the checkpoint's[Q]marker for the question column and[D]for the passage column, keeping training consistent with inference.
- max_length(deliberately not set): this argument caps tokenization duringtraining only, for when you want cheaper training than the model's full serving length. I measured what that shortcut costs on this data. Training at 512 tokens lost about 0.015 NDCG@10 for about 2x the speed, and the deficit did not shrink with more data, because the model simply never sees what got cut off. Leave it unset so training matches inference, unless you need the speedup more than the quality.
- learning_rate=1e-4: after a sweep from 5e-6 to 2e-4, I had the best luck with this higher-than-usual learning rate.

## Evaluator

To track your model's performance during training, you can pass aneval_datasetto the trainer for evaluation loss, but concrete retrieval metrics are much more informative. Sentence Transformers includes the following built-in evaluators for multi-vector models:

For domain finetuning, theMultiVectorInformationRetrievalEvaluatorbuilt from your own held-out data is the one that matters. One tip on constructing it is that the corpus should be hard enough that models can be told apart. In my case the MIRIAD questions are generated from their own source passages, which makes retrieval unusually easy. Against just the 10k gold passages, nearly every model scored above 0.97 NDCG@10. If your evaluation saturates like that, adddistractorpassages (I use deduplicated passages from the training split) until the scores spread out:

```python
from datasets import load_dataset
from sentence_transformers.multi_vector_encoder.evaluation import MultiVectorInformationRetrievalEvaluator

dataset = load_dataset("tomaarsen/miriad-4.4M-split")



corpus = {}
queries = {}
relevant_docs = {}
passage_to_id = {}
for idx, row in enumerate(dataset["eval"]):
    if row["passage_text"] not in passage_to_id:
        passage_to_id[row["passage_text"]] = f"p{len(passage_to_id)}"
        corpus[passage_to_id[row["passage_text"]]] = row["passage_text"]
    if idx < 1_000:
        queries[f"q{idx}"] = row["question"]
        relevant_docs[f"q{idx}"] = {passage_to_id[row["passage_text"]]}


seen = set(passage_to_id)
for row in dataset["train"]:
    if len(corpus) >= 200_000:
        break
    if row["passage_text"] not in seen:
        seen.add(row["passage_text"])
        corpus[f"d{len(corpus)}"] = row["passage_text"]

evaluator = MultiVectorInformationRetrievalEvaluator(
    queries=queries,
    corpus=corpus,
    relevant_docs=relevant_docs,
    name="miriad-dev",
    batch_size=16,
)


```

## Trainer

TheMultiVectorEncoderTraineris where all previous components come together. Here is the complete script that trainedmulti-vector-encoder/mLateOn-medical, the model from the introduction:

```python
import logging
import string
import traceback

from datasets import load_dataset

from sentence_transformers import (
    MultiVectorEncoder,
    MultiVectorEncoderModelCardData,
    MultiVectorEncoderTrainer,
    MultiVectorEncoderTrainingArguments,
)
from sentence_transformers.base.sampler import BatchSamplers
from sentence_transformers.multi_vector_encoder.evaluation import MultiVectorInformationRetrievalEvaluator
from sentence_transformers.multi_vector_encoder.losses import CachedMultiVectorMultipleNegativesRankingLoss

logging.basicConfig(format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S", level=logging.INFO)


def main():
    
    
    model = MultiVectorEncoder(
        "lightonai/mLateOn-unsupervised",
        model_kwargs={"torch_dtype": "float32"},
        processor_kwargs={"model_max_length": 8192},
        model_card_data=MultiVectorEncoderModelCardData(
            language="en",
            license="apache-2.0",
            model_name="mLateOn finetuned on MIRIAD medical retrieval",
        ),
    )

    
    model[0].query_length = None
    model[0].document_length = None

    
    model[2].skiplist_words = list(string.punctuation)
    model[2].resolve_with_tokenizer(model.tokenizer)

    
    train_dataset = load_dataset("tomaarsen/miriad-4.4M-split", split="train").select(range(1_000_000))

    
    loss = CachedMultiVectorMultipleNegativesRankingLoss(model=model, mini_batch_size=16)

    
    
    eval_split = load_dataset("tomaarsen/miriad-4.4M-split", split="eval")
    corpus, queries, relevant_docs, passage_to_id = {}, {}, {}, {}
    for idx, row in enumerate(eval_split):
        if row["passage_text"] not in passage_to_id:
            passage_to_id[row["passage_text"]] = f"p{len(passage_to_id)}"
            corpus[passage_to_id[row["passage_text"]]] = row["passage_text"]
        if idx < 500:
            queries[f"q{idx}"] = row["question"]
            relevant_docs[f"q{idx}"] = {passage_to_id[row["passage_text"]]}
    dev_evaluator = MultiVectorInformationRetrievalEvaluator(
        queries=queries, corpus=corpus, relevant_docs=relevant_docs, name="miriad-dev", batch_size=16
    )

    
    run_name = "mLateOn-medical"
    args = MultiVectorEncoderTrainingArguments(
        output_dir=f"models/{run_name}",
        num_train_epochs=1,
        per_device_train_batch_size=128,
        per_device_eval_batch_size=16,
        learning_rate=1e-4,
        warmup_steps=0.05,
        prompts={"question": "[Q] ", "passage_text": "[D] "},
        fp16=False,  
        bf16=True,  
        batch_sampler=BatchSamplers.NO_DUPLICATES,
        eval_strategy="steps",
        eval_steps=0.1,
        save_strategy="steps",
        save_steps=0.05,
        logging_steps=0.01,
        run_name=run_name,
    )

    
    trainer = MultiVectorEncoderTrainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        loss=loss,
        evaluator=dev_evaluator,
    )
    trainer.train()

    
    model.save_pretrained(f"models/{run_name}/final")

    
    try:
        model.push_to_hub(run_name)
    except Exception:
        logging.error(f"Error uploading model to the Hugging Face Hub:\n{traceback.format_exc()}")


if __name__ == "__main__":
    main()

```

[翻译失败，原文如下]

That's the whole recipe: a pre-supervised checkpoint, a million domain pairs, in-batch negatives, full document length, and a higher-than-usual learning rate. The run took 14.5 hours on my single RTX 3090 at a peak of 17.5 GB VRAM, and every one of those choices was the winner of a measured comparison rather than a guess.

For readers on smaller budgets, my scaling experiments put 100k pairs (75 minutes of training) within 0.012 NDCG@10 of the full million-pair run. Most of the gain comes in the first hour.

### Callbacks

The MultiVectorEncoder trainer supports varioustransformers.TrainerCallbacksubclasses, including:

- WandbCallbackfor logging training metrics to W&B ifwandbis installed
- TensorBoardCallbackfor logging training metrics to TensorBoard iftensorboardis accessible
- CodeCarbonCallbackfor tracking carbon emissions during training ifcodecarbonis installed

Enable these via thereport_totraining argument, e.g.report_to=["wandb", "codecarbon"], with the required dependencies installed. It defaults to"none", andreport_to="all"activates every integration whose dependency is installed.

Refer to theTransformers Callbacks documentationfor more information on these callbacks and how to create your own.

### Multi-Dataset Training

Typically, top-performing general-purpose models are trained on multiple datasets simultaneously. However, this approach can be challenging due to the varying formats of each dataset. Fortunately, theMultiVectorEncoderTrainerallows you to train on multiple datasets without requiring a uniform format. Additionally, it provides the flexibility to apply different loss functions to each dataset. Here are the steps to train with multiple datasets at once:

- Use a dictionary ofdatasets.Datasetinstances (or adatasets.DatasetDict) as thetrain_dataset(and optionally alsoeval_dataset).
- (Optional) Use a dictionary of loss functions mapping dataset names to losses. Only required if you wish to use different loss functions for different datasets.

Each training/evaluation batch will only contain samples from one of the datasets. The order in which batches are sampled from the multiple datasets is defined by theMultiDatasetBatchSamplersenum, which can be passed to theMultiVectorEncoderTrainingArgumentsviamulti_dataset_batch_sampler. Valid options are:

- MultiDatasetBatchSamplers.ROUND_ROBIN: Round-robin sampling from each dataset until one is exhausted. With this strategy, it's likely that not all samples from each dataset are used, but each dataset is sampled from equally.
- MultiDatasetBatchSamplers.PROPORTIONAL(default): Sample from each dataset in proportion to its size. With this strategy, all samples from each dataset are used and larger datasets are sampled from more frequently.

## Evaluation

To find out where the finetuned model stands, I evaluated it against over 50 retrieval model configurations across four architecture families on the MIRIAD evaluation set, built exactly as in theEvaluatorsection above, with 1,000 held-out medical questions searching 200,000 unique passages (the 10k gold passages hidden among 190k deduplicated distractors from the training split). This corpus is four times the size of the 50,000-passage one fromWhich starting point should you pick?, so scores are not comparable between the two tables.

The headline results, with the full table in the collapsible below:

The finetuned model tops the table, beating the strongest zero-shot model of any architecture by +0.062 NDCG@10. In other words, the strongest zero-shot model returns the right passage as the very first hit for 75.8% of the queries, while the finetuned model does so for 84.9%, cutting the rank-1 error by more than a third.

The architecture pattern is just as clear, with the top of the table exclusively late interaction. On long documents, one vector per token beats one vector per document, even at matched training and matched backbones. DenseOn and LateOn share training data and architecture except for the head, and the late-interaction sibling wins by +0.12, with the multilingual pair (mDenseOn and mLateOn) replicating this at +0.13. Scale doesn't rescue single vectors either.Qwen3-Embedding-4B, the strongest dense model with roughly 33x the active (non-embedding) parameters of mine, still stops 0.13 short, and the 8B version scores lower than the 4B.

BM25 also performs surprisingly well, beating every sparse model, every truncation-capped multi-vector model, and all but three dense models: the multi-billionQwen3-Embedding-4Band8B, andvoyage-4-nano, which reads its full 32k token context to edge past by just 0.006. Don't expect that to transfer to your own data though. MIRIAD's questions are generated from the passages, so the lexical overlap between a query and its gold passage is far larger than in typical retrieval, and BM25's unlimited context length lets it use every one of those overlapping words while most neural checkpoints truncate. A BM25 baseline is cheap and always worth running, just don't count on this margin.

The full field at a glance, sorted by score and colored by architecture family.

![Sorted NDCG@10 on the MIRIAD 200k benchmark for every evaluated model, colored by architecture family](/images/posts/6b503eb79d4d.png)

Models marked@Nare evaluated with their document length cap lifted to N tokens, since their native caps (180 to 512 tokens) would otherwise truncate the 941-token average passages. For every multi-vector model this lift was worth +0.08 to +0.24 NDCG@10 over the as-served row, and even the dense DenseOn gained +0.03 from the same treatment.

Note that this does not mean thatmulti-vector-encoder/mLateOn-medicalis the strongest model onalldomains. It's simply the strongest inmydomain. This is totally fine, as I just need this model to work well on my data.

Don't underestimate the power of finetuning multi-vector models on your domain. Fourteen and a half hours on a single consumer GPU produced a model that no general-purpose retriever comes close to on this data, and the recipe is a single script with no teacher model and no mined negatives!

### Optimizing the index

The fair objection to multi-vector retrieval is index size, and this domain is close to the worst case for it. Storing one vector per token, my model needs about 878 vectors per passage, so the 200,000-passage corpus takes roughly 45 GB at fp16, where a dense model needs well under 1 GB. Document length is what makes that gap so wide. The Natural Questions passages in thecompanion postaverage about 125 token vectors each, seven times fewer, so a corpus of short passages starts from a far smaller index than this one does. TheHierarchicalTokenPoolingmodule compresses exactly this by clustering each document's token embeddings and storing the cluster means, keeping roughly1 / pool_factorof the vectors:

```python
from sentence_transformers.multi_vector_encoder.modules import HierarchicalTokenPooling

pooling = HierarchicalTokenPooling(pool_factor=4)
document_embeddings = model.encode_document(passages, token_pooling=pooling)

```

I measured it post-hoc on the finished model, with no pooling-aware training, and on long documents it is remarkably cheap.

![Embedding size for the 200,000-passage corpus versus NDCG@10, with the token pooling trajectory sweeping the multi-vector index into dense-model territory](/images/posts/bdf48936a5a4.png)

The solid points are uncompressed embeddings, so that every family is counted the same way and scored with exact search. You would not deploy any of them like that, though. Dense indexes routinely use int8 or binary quantization with rescoring, sparse indexes compress their postings, and multi-vector indexes use PLAID-style residual compression. Don't read those points as the disk you need to buy, but as relative storage cost.

[翻译失败，原文如下]

Token pooling is the solid line. Halving the vector count costs 0.0033 NDCG@10 and leaves rank-1 accuracy untouched, and keeping only a quarter of them, at 11.2 GB, still scores 0.8991. The curve keeps going (I measured out to a tenth of the vectors, still at 0.8765) but there is little reason to push pooling that far once quantization is on the table, which is what the dashed line below is about.

The dashed line is what a real deployment might look like. I gave Omar Khattab early access to the model and the benchmark, and he measured these configurations withfast-plaidat 1-bit residual quantization, using compact 17-bit centroid ids and 18-bit document ids instead of its ordinary unpacked 64-bit integers, plus document-side pruning:

That first row is 13x smaller than the raw embeddings, for 0.0155 NDCG@10. That is a far better trade than anywhere on the pooling curve. Quantization shrinks each vector while pooling and pruning cut how many you keep, so they compose, and quantization is the one to reach for first. Push further and the last row lands at 1.45 GB,smallerthan the fp16 embeddings ofQwen3-Embedding-8B(1.64 GB), while scoring 0.0895 higher. The objection that multi-vector indexes are too big does not survive a properly configured index.

The pruning here is naive, meant only to establish that token reduction works on top of quantization, so read the bottom two rows as a floor rather than the frontier. If you would rather not hand-tune quantization at all, theIndexingsection of the companion post covers fast-plaid, Qdrant, Weaviate, and Vespa.

Multi-vector retrieval is only as expensive as its index. The raw embeddings for this corpus are 45 GB, and a properly configured index is at least 7x smaller at nearly the same accuracy. The index deserves as much of your attention as the checkpoint.

## Acknowledgements

Thanks toOmar Khattabfor measuring the quantized and pruned index configurations inOptimizing the index, and for the discussions around late-interaction index costs.

## Additional Resources

### Training Examples

These pages have training examples with explanations as well as links to training scripts. You can use them to get familiar with the multi-vector training loop:

- MIRIAD: domain-specific training on medical retrieval, an earlier and simpler cousin of this blogpost's recipe
- MS MARCO: contrastive and knowledge distillation recipes
- Multimodal: ColPali-style visual document retrieval training
- PEFT Adapters: parameter-efficient finetuning with LoRA

### Documentation

For further learning, you may also want to explore the following resources on Sentence Transformers:

- Installation
- Quickstart
- Usage
- Creating Custom Models
- Pretrained Models
- Training Overview(This blogpost is a distillation of the Training Overview documentation)
- Loss Overview
- API Reference

And here is an advanced page that might interest you:

- Distributed Training

And the companion blogpost, covering everything aboutusingthese models:

- Multi-Vector (Late Interaction) Embedding Models with Sentence Transformers

---

> 本文由AI自动翻译，原文链接：[Training and Finetuning Multi-Vector Embedding Models with Sentence Transformers](https://huggingface.co/blog/train-multi-vector-encoder)
> 
> 翻译时间：2026-08-29 08:48
