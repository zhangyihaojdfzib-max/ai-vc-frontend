---
title: Token Pooling-Aware Training for Multi-Vector Embedding Models
title_original: Token Pooling-Aware Training for Multi-Vector Embedding Models
date: '2026-11-11'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/token-pooling
author: ''
summary: '[翻译失败，原文如下]


  # Token Pooling-Aware Training for Multi-Vector Embedding Models


  Multi-vector embedding models give each query token its own opportunity...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-13T09:19:17.691831'
---

[翻译失败，原文如下]

# Token Pooling-Aware Training for Multi-Vector Embedding Models

Multi-vector embedding models give each query token its own opportunity to find a match in a document. This makes them wonderfully expressive for search, but those document vectors add up quickly. A corpus with millions of documents can contain hundreds of millions of vectors!

Token pooling makes these representations smaller by merging similar token vectors. The more aggressively I compress them, however, the easier it becomes to lose something useful. Pooling-aware training teaches the encoder to preserve the information that matters when its vectors are merged, helping you retrieve better from the same storage budget.

In this post, I'll explain how pooling works, train a model for compressed retrieval with Sentence Transformers, and explore the resulting quality and storage tradeoff. Withpool_factor=4, my normally trained model retains 94.6% of its unpooled NanoBEIR nDCG@10, with a4xreduction in document vectors. Token pooling-aware training raises that retention to 97.8% at the same storage budget! Let's see how.

This post builds on pooling-aware training studied in Stefan Josef'sLearn to PoolandLightOn's pooling regularization study, which also explores targeted training and adaptive budgets. Here, I'll focus on understanding the method and putting it to work with a short, reproducible Sentence Transformers example.

![Mean NanoBEIR nDCG@10 versus stored document vectors for pool factors 2, 3, 4, and 6 and unpooled retrieval, comparing ordinary and pooling-aware training.](/images/posts/50331e8688ba.png)

Pooling-aware training improves retrieval quality at the same vector budget. Details below.

- Why Multi-Vector Retrieval Needs So Many Vectors
- Token PoolingChoosing a Pooling BudgetCalibrating Adaptive Pooling
- Token Pooling-Aware TrainingA Loss Wrapper in Sentence TransformersOptional Kernel Acceleration
- Using the Trained Model
- Evaluation Results
- Combining Compression Techniques
- References
- Code and Models

- Choosing a Pooling Budget
- Calibrating Adaptive Pooling

- A Loss Wrapper in Sentence Transformers
- Optional Kernel Acceleration

## Why Multi-Vector Retrieval Needs So Many Vectors

A single-vector embedding model compresses an entire document into one vector.Multi-vector modelssuch as ColBERT instead keep a collection of contextual token vectors, allowing different parts of a query to match different parts of a document.

For example, a query about a laptop with a long battery life can find evidence about the laptop in one part of a document and battery endurance in another. With MaxSim scoring, each query vector selects its best matching document vector, and those scores are added together:

MaxSim⁡(Q,D)=∑q∈Qmax⁡d∈Dq⊤d\operatorname{MaxSim}(Q, D) = \sum_{q \in Q} \max_{d \in D} q^\top dMaxSim(Q,D)=q∈Q∑​d∈Dmax​q⊤d

Even with the 2-bit or 4-bit residual quantization supported byFast-PLAID, storing hundreds of vectors per document adds up. At 4 bits per residual coordinate, 200 vectors of 128 dimensions require 12.8 KB of quantized residuals per document, or 12.8 GB across a million documents. Pooling each document to 50 vectors reduces that to 3.2 GB, at the same dimensionality and precision.

The useful observation is that many document vectors can be similar. Several tokens might describe closely related concepts, creating an opportunity to represent them together.

## Token Pooling

HierarchicalTokenPoolinggroups similar token embeddings usingWard hierarchical clustering. Starting with one group per token vector, it repeatedly merges the two groups that cause the smallest increase in how spread out the vectors are within their groups. This spread is measured by the sum of squared distances from each vector to its group's mean, so Ward's method favors compact groups of similar vectors.

These merges build a hierarchy of progressively larger groups, letting us choose a level of compression that fits our budget. We then represent each group by its mean and normalize the resulting vectors again, ready for MaxSim scoring.

You can make compression proportional to document length:

```python
from sentence_transformers.multi_vector_encoder.modules import HierarchicalTokenPooling

pooling = HierarchicalTokenPooling(pool_factor=4)

```

Withpool_factor=4, documents retain approximately one quarter of their original vectors, so longer documents can keep proportionally more capacity. By default, the first token is protected from merging and pooling applies only to document embeddings, leaving query embeddings unchanged.

### Choosing a Pooling Budget

HierarchicalTokenPoolingoffers three alternative controls:

This distinction matters when document lengths vary. Withpool_factor=4, a longer document can retain approximately one quarter of its vectors, allowing its representation to grow with its content. Withdistance_threshold, the vector count can grow when more distinct embeddings need to be preserved.

### Calibrating Adaptive Pooling

Adaptive pooling uses a shared distance threshold to merge similar embeddings more aggressively while preserving more vectors for documents with distinct content. It can be used with any multi-vector model,including one trained without a pooling-aware objective.

Rather than choosing a threshold manually, you can calibrate it for a target average vector count. Given a representative sample of your corpus incalibration_documents:

```python
from sentence_transformers import MultiVectorEncoder
from sentence_transformers.multi_vector_encoder.modules import HierarchicalTokenPooling

model = MultiVectorEncoder("lightonai/LateOn")
calibration_embeddings = model.encode_document(calibration_documents)
threshold = HierarchicalTokenPooling.calibrate_distance_threshold(calibration_embeddings, target_tokens=16)
pooling = HierarchicalTokenPooling(distance_threshold=threshold)


document_embeddings = model.encode_document(documents_to_index, token_pooling=pooling)

```

Calibration only needs document embeddings and returns a threshold you can reuse when indexing. The target is an average, so individual documents can receive more or fewer than 16 vectors. The achieved average can also change on another corpus.

## Token Pooling-Aware Training

Pooling can already be useful on an ordinary multi-vector model. The difficulty appears when a document contains a distinction that matters for retrieval, but merging its vectors makes that distinction harder to recover. The original training objective never required the model to work with these compressed representations. But, you can teach it to do exactly that.

If you've usedMatryoshka embeddings, the training principle will feel familiar. Matryoshka applies a retrieval objective at several embedding widths, teaching smaller prefixes to remain useful. Pooling-aware training applies the objective to representations with fewer token vectors.

For my example, each training batch contributes two losses:

1. Retrieval using the original document embeddings.
2. Retrieval after compressing documents to approximately one quarter of their original vectors.

I average them:

L=12Lunpooled+12Lpooled\mathcal{L} = \tfrac{1}{2}\mathcal{L}_{\mathrm{unpooled}} + \tfrac{1}{2}\mathcal{L}_{\mathrm{pooled}}L=21​Lunpooled​+21​Lpooled​

The first term teaches the model to retrieve with its full representations. The second teaches it to arrange its token embeddings so that useful matches survive pooling. Both objectives update the same encoder, giving it feedback about retrieval before and after compression.

Ward clustering makes discrete decisions about which tokens belong together. During training,HierarchicalTokenPoolinguses a straight-through estimator to pass gradients from pooled vectors back to their member tokens, without differentiating the cluster assignments. The encoder can then learn from retrieval errors made with its pooled representations.

### A Loss Wrapper in Sentence Transformers

[翻译失败，原文如下]

MultiVectorTokenPoolingLosswraps an existing multi-vector retrieval loss and applies it using your chosen poolers:

```python
from sentence_transformers import MultiVectorEncoder
from sentence_transformers.multi_vector_encoder.losses import (
    CachedMultiVectorMultipleNegativesRankingLoss,
    MultiVectorTokenPoolingLoss,
)
from sentence_transformers.multi_vector_encoder.modules import HierarchicalTokenPooling

model = MultiVectorEncoder("answerdotai/ModernBERT-base", similarity_fn_name="maxsim")
pooling = HierarchicalTokenPooling(pool_factor=4)

base_loss = CachedMultiVectorMultipleNegativesRankingLoss(model, mini_batch_size=64)
loss = MultiVectorTokenPoolingLoss(
    model,
    base_loss,
    token_poolings=[None, pooling],
    weights=[0.5, 0.5],
)

```

CachedMultiVectorMultipleNegativesRankingLosssupplies the retrieval objective. It teaches each query to score its relevant document above the negative documents in the batch. By default, it usesmodel.similarity, using the model's similarity setting (MaxSim in this example) and kernel settings. A model configured withsimilarity_fn_name="meanmaxsim"would also use MeanMaxSim during training.

Gradient caching allows the encoder to process small mini-batches while retaining a larger set of in-batch negatives. My training script uses mini-batches of 64 with a training batch size of 256.

MultiVectorTokenPoolingLossadds the compression objective. Here,Nonemeans that one variant uses the original embeddings, whilepoolingsupplies the factor-4 variant. The two weights average their losses. Pooling variants reuse the computed token embeddings, so each additional pooler adds clustering and scoring work without requiring a separate encoder pass for that variant.

The poolers can also be customBaseTokenPoolingimplementations that preserve gradients through their input embeddings. You can adapt the training objective to the representation you want to deploy.

Replace the factor-4 pooler with your chosen deployment configuration, or include several poolers and choose weights for their losses.

The completetraining scriptincludes the dataset, trainer, validation loss, and small retrieval evaluations during training. From a checkout of the repository, run both variants locally withuv:

```bash
uv run examples/multi_vector_encoder/training/token_pooling/training_cached_contrastive.py --baseline
uv run examples/multi_vector_encoder/training/token_pooling/training_cached_contrastive.py

```

The script declares its training and kernel dependencies, so uv installs them for you. Compatible kernels are enabled automatically.

You can also train on a cloud GPU withHugging Face Jobs. Install the CLI and log in with a token that can run Jobs and upload models:

```bash
pip install -U huggingface_hub
hf auth login

hf jobs uv run \
    --flavor a10g-small \
    --timeout 4h \
    --secrets HF_TOKEN \
    -- https://raw.githubusercontent.com/huggingface/sentence-transformers/main/examples/multi_vector_encoder/training/token_pooling/training_cached_contrastive.py

```

This runs the pooling-aware variant on an A10G GPU with a four-hour time limit. PassingHF_TOKENas a secret lets the script upload the trained model to your Hub account when training finishes. To run the ordinary-loss baseline as well, repeat the command with--baselineafter the script URL.

### Optional Kernel Acceleration

You can accelerate MaxSim scoring, Ward clustering, and supported backbone operations withkernels. Install the training and kernel dependencies:

```bash
pip install -U "sentence-transformers[train,kernels]"

```

In the training example above, replace the model and pooler initialization before constructing the loss:

```python
model = MultiVectorEncoder(
    "answerdotai/ModernBERT-base",
    device="cuda",
    similarity_fn_name="maxsim",
    use_kernels=True,
)
pooling = HierarchicalTokenPooling(pool_factor=4)

```

Hierarchical poolers inherit the model's kernel settings by default, so you only need to enable kernels on the model.

Sentence Transformers selects compatible kernels for your setup and uses the existing implementation wherever a replacement isn't available. For example, thedefault MaxSim kernelscores queries against documents without building the full token similarity matrix in memory, but it does require CUDA and Triton.

The defaultWard clustering kernelconsiderably speeds up hierarchical clustering by running on CUDA instead of the CPU. We're talking about 30-150x faster than SciPy depending on the setting.

## Using the Trained Model

Let's load the pooling-aware model and retrieve with compressed document embeddings. Kernel settings aren't saved with the model, so adduse_kernels=Truewhen loading if you'd like to use them for inference too:

```python
from sentence_transformers import MultiVectorEncoder
from sentence_transformers.multi_vector_encoder.modules import HierarchicalTokenPooling

model = MultiVectorEncoder("tomaarsen/mve-ModernBERT-base-token-pooling")
pooling = HierarchicalTokenPooling(pool_factor=4)

queries = ["Which planet is known as the Red Planet?"]
documents = [
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
    "Jupiter, the largest planet in our solar system, has a prominent red spot.",
]

query_embeddings = model.encode_query(queries)
document_embeddings = model.encode_document(documents, token_pooling=pooling)

print([len(embedding) for embedding in document_embeddings])

print(model.similarity(query_embeddings, document_embeddings))






```

The pooler compresses the document embeddings after the encoder's forward pipeline, reducing the total from 58 vectors to 16 while leaving query embeddings unchanged. Mars still receives the highest similarity score, followed by Jupiter and Venus, so the ranking is preserved despite storing far fewer document vectors.

You can changepool_factorat inference to explore a different storage budget with the same trained model. For repeated use, you can also passtoken_pooling=poolingwhen initializingMultiVectorEncoderto make it the runtime default. The pooler'stasksstill control which inputs are compressed (e.g. only documents).

## Evaluation Results

To investigate, I trained two models fromanswerdotai/ModernBERT-base, each with a fresh 128-dimensional token projection:

- tomaarsen/mve-ModernBERT-base-token-pooling-baseline, using only the cached contrastive loss.
- tomaarsen/mve-ModernBERT-base-token-pooling, using the cached contrastive loss wrapped with the unpooled and factor-4 objectives above.

Both runs use one epoch over the same 120,000 MS MARCO triplets, seed 42, and matching initialization and optimization settings. The training token cap is 300, and short queries are expanded to at least 32 token positions to provide additional contextual query vectors. Only the loss differs between the two experiments, and I didn't run a hyperparameter search.

I evaluated both models on NanoBEIR@13, reporting mean nDCG@10 (%). The figure compares ordinary and pooling-aware training with pool factors of 2, 3, 4, and 6, alongside unpooled retrieval. The table also includes fixed caps and adaptive thresholds, showing how the training benefits transfer to other pooling settings.

For adaptive pooling, I calibrated a separate threshold for each encoder and NanoBEIR corpus, using its unpooled document embeddings to match the average vector counts under caps of 64, 32, and 16. Short documents bring those averages below their respective caps.

At the trainedpool_factor=4, nDCG@10 improves from 49.03 to 51.23, while storing 74.8% fewer document vectors than unpooled retrieval. This increases score retention from 94.6% to 97.8%, where retention is the pooled mean nDCG@10 divided by each model's own unpooled mean. Unpooled retrieval also improves, from 51.84 to 52.39.

[翻译失败，原文如下]

The gains extend to fixed caps and adaptive pooling, even though training used only the full representation and proportional pooling. At an average of 29.58 vectors per document, adaptive pooling retains 97.3% of the pooling-aware model's unpooled score while storing 84.7% fewer document vectors. The normally trained model retains 93.3% at the same budget.

## Combining Compression Techniques

If index size is your main concern, I would reach for these options in this order:

1. Embedding quantization to 4, 2, or 1 bit(s), for example viaFast-PLAID, to reduce storage per coordinate.
2. Token pooling to reduce the number of document vectors, optionally with pooling-aware fine-tuning as shown in this blog.
3. Matryoshka token embeddingsto reduce the dimensionality of each token vector, optionally with fine-tuning to preserve retrieval quality at smaller widths.

If the model's default dimensionality is larger than 128, I would consider Matryoshka truncation and fine-tuning earlier as well. These approaches can be combined, so evaluate the resulting index size and retrieval quality with your search engine and corpus.

MultiVectorMatryoshkaLosstrains token embeddings to remain useful after truncation. You can wrap it withMultiVectorTokenPoolingLossto train for both smaller dimensions and fewer document vectors, reusing the encoder's embeddings across the compression settings.

Try thecomplete training example, choose a budget that matters for your application, and compare it with a matched ordinary-loss run. The accompanyingevaluation scriptmeasures unpooled retrieval, caps of 64, 32, 16, 8, and 4 vectors, and pool factors of 2 through 6, so you can plot the quality and storage tradeoff for your own model.

With a few extra lines in the training objective, a smaller document representation becomes something the model actively learns to use. That opens up an exciting amount of room to make multi-vector retrieval more practical!

## References

- Stefan Josef.Learn to Pool: Lightweight Fine-Tuning for Flexible Multi-Vector Compression.
- Benjamin Clavié, Antoine Chaffin, and Griffin Adams.Reducing the Footprint of Multi-Vector Retrieval with Minimal Performance Impact via Token Pooling.
- Antoine Chaffin.After the party comes the free lunch: regularizing ColBERT models to enhance pooling capabilities and reduce index footprint.
- Luyu Gao, Yunyi Zhang, Jiawei Han, and Jamie Callan.Scaling Deep Contrastive Learning Batch Size under Memory Limited Setup.
- Introduction to Matryoshka Embedding Models.

## Code and Models

- Token pooling-aware training example and README
- Complete training script
- NanoBEIR evaluation script
- Example checkpoints:tomaarsen/mve-ModernBERT-base-token-poolingtomaarsen/mve-ModernBERT-base-token-pooling-baseline
- Pretrained multi-vector models compatible with Sentence Transformers
- Matryoshka-aware training for multi-vector models
- Fast-PLAID

- tomaarsen/mve-ModernBERT-base-token-pooling
- tomaarsen/mve-ModernBERT-base-token-pooling-baseline

---

> 本文由AI自动翻译，原文链接：[Token Pooling-Aware Training for Multi-Vector Embedding Models](https://huggingface.co/blog/token-pooling)
> 
> 翻译时间：2026-11-13 09:19
