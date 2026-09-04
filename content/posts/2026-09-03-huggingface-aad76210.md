---
title: 'NeoMME: an efficient Multimodal-native and Multilingual Encoder'
title_original: 'NeoMME: an efficient Multimodal-native and Multilingual Encoder'
date: '2026-09-03'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/Hcompany/neomme
author: ''
summary: '[翻译失败，原文如下]


  # NeoMME: an efficient Multimodal-native and Multilingual Encoder


  ## TL;DR


  We introduceNeoMME, a family of 260M and 800M multilingual m...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-04T07:07:16.891052'
---

[翻译失败，原文如下]

# NeoMME: an efficient Multimodal-native and Multilingual Encoder

## TL;DR

We introduceNeoMME, a family of 260M and 800M multilingual multimodal encoders. Unlike many generative visual language models,NeoMMEdoes not use a separate pretrained vision tower or a causal language model. A single bidirectional Transformer processes both text tokens and raw image patches, and we train the entire model from scratch with a masked discrete-diffusion objective.

We fine-tunedNeoMMEfor visual document retrieval using ColPali's page-image approach.NeoMME-Retriever returns dense and late-interaction embeddings in one forward pass. Both model sizes lie on the ViDoRe v3 Pareto frontier for nDCG@10 and model size. At a matched 2048×2048 image input size on an NVIDIA L40S GPU, the 260M model encodes about 51 pages per second, or about twice ColModernVBERT's throughput. Hierarchical token pooling and asymmetric quantization reduce late-interaction index storage from roughly 1.5 MB to 6 kB per page (255× smaller) while retaining more than 95% of baseline nDCG@10.

NeoMMEis available in Hugging Face Transformers. We release all model checkpoints under the Apache 2.0 license.

- 🤗NeoMMEcollection
- 📄Technical report
- 🔎Visual RAG demo

## Why another multimodal encoder?

Many recent visual document retrievers are adapted from pretrained generative visual language models. A separately pretrained vision encoder produces visual features, which a projector maps into the language model's input space. A causal decoder then processes the combined image and text representations. Retrieval, classification, and token labeling do not generate text autoregressively, so they do not require a causal decoder or the parameter and compute overhead of this architecture.

ModernBERTbrought efficient architecture and training improvements to bidirectional encoders. For visual document retrieval,ModernVBERTapplied a bidirectional ModernBERT-style text encoder while retaining a separate pretrained SigLIP2 vision tower. We wanted to push this even further by designing and training a multimodal encoder without having to carry over the parameter and compute overhead of a VLM.

NeoMME(pronounced "nee-oh-me", IPA /ˈniː.oʊ.mi/) is a multilingual, multimodal foundation encoder that generates vector representations for input text and/or images using a single Transformer encoder. It is not based on an existing pretrained vision tower, text encoder, or text decoder.

Images and text use the same computational path, soNeoMMEcan more easily support pretraining, fine-tuning, parallelization, and serving across both modalities.

## NeoMMEencoder backbone

### One Transformer for images and text

NeoMMEcomes in two sizes,260Mand800M. Both variants share the same architecture:

- Native multimodal inputs:text inputs use factorized token embeddings, while images are divided into a grid of non-overlapping 32×32 patches and projected with a small MLP. Both enter the same Transformer encoder.
- Dynamic image resolution:images keep their aspect ratio and size. This allows the model to use more tokens on a high-resolution, information-dense document page than on a smaller image with less content.
- Long bidirectional context:both models have a context length of 16,384 tokens (enough for up to two standard 3840×2160 4K UHD images). Most layers use symmetric sliding-window attention, while every sixth layer and the final layer use global attention.
- A modern encoder stack:NeoMMEuses recent encoder improvements such as grouped-query attention, query-key normalization, gated attention, 2D rotary position embeddings, and squared-ReLU MLPs, among others.
- Multilingual text:we trained a BPE tokenizer with a 131k-token vocabulary from scratch on multilingual text, code, mathematics, and machine-produced image transcripts.

### Learning from images through masked text

We pretrainNeoMMEfrom scratch as a discrete masked-diffusion text denoiser. For each text-only example, we sample a corruption rate uniformly between 0 and 1. Each eligible text token is then independently masked at that rate.

Multimodal examples use corruption rates between 0.3 and 1. The image patches remain visible whileNeoMMEreconstructs masked text. With light masking, the model can often recover a missing word from the surrounding text alone. For example, "cat" is a plausible completion of "The [MASK] sat on the mat," even without an image. But high masking forces the model to learn image-grounded descriptions with little to no signal from the non-masked input text tokens.

Pretraining mixes multilingual text, code, mathematics, natural images, and document images. Each model processes about 524 billion packed input tokens, including 290 billion tokens from text-only examples. This text budget is relatively small compared with ModernBERT's 2 trillion training token budget. Hence, we chose the NorMuon optimizer to improve data efficiency during training.

## NeoMME-Retriever

To get a meaningful downstream evaluation of the backbone, we fine-tuneNeoMMEfor visual document retrieval using the page-image methodology introduced byColPali. While traditional text-based retrieval consists of retrieving text chunks,NeoMME-Retriever ranks document page screenshots and bypasses all the preprocessing OCR steps necessary to extract text from PDFs. Treating the pages as images preserves layout, charts, tables, font type and size, and other visual clues that cannot be captured even by a perfect OCR model.

### A dual-head design for dense and late-interaction retrieval

NeoMME-Retriever reuses theNeoMMEbackbone but adds two jointly trained heads on top of it for retrieval:

- The dense head averages the backbone's hidden state vectors into a normalized vector (mean pooling). Dense embeddings are most common today: they are compact and work naturally with approximate nearest-neighbor (ANN) techniques for fast retrieval.
- The late-interaction head projects each text token or image patch from the backbone's output hidden states to a 128-dimensional normalized vector. Compared to dense embeddings, the finer granularity preserves local matches between individual query tokens and image regions.

Omar Khattab, who introduced late-interaction in ColBERT,explains whythe term is more precise than "multi-vector." It describes the granularity and learnability of the scoring function, not simply the number of stored vectors.

To learn more about late-interaction, we recommend readingthis crash courseby Amélie Chatelain.

OneNeoMME-Retriever forward pass returns both representations, which gives you flexibility no matter your use case and infrastructure. We recommend using late-interaction embeddings in general since they are more powerful and can be used easily with open-source libraries likeNextPlaid. However, if you have a very large corpora, you can run a single forward pass withNeoMME-Retriever to get the dense embedding, retrieve a small number of documents through an ANN index, and then use late-interaction to rerank the retrieved candidates.

### Competitive retrieval at compact model sizes

We report nDCG@10 on ViDoRe v3.NeoMME-Retriever-260M reaches 0.523, the highest score among evaluated models strictly below 800M parameters. It is within 0.002 nDCG@10 of ColQwen2.5 while using about 14× fewer parameters.NeoMME-Retriever-800M reaches 0.556, within 0.009 nDCG@10 of the similarly sizedVultron Retriever Flash (0.8B). BothNeoMME-Retriever models lie on the model-size Pareto frontier.

ViDoRe v1 and v2 use nDCG@5. On both benchmarks,NeoMME-Retriever-260M outperforms ColModernVBERT and the twice-larger ColSmol-500M.NeoMME-Retriever-800M outperforms ColPali v1.3 while using 3.6 times fewer parameters.

†Scores from MTEB.‡Results from our own evaluations.

### Making high-resolution retrieval practical for late-interaction

[翻译失败，原文如下]

Late-interaction storage scales linearly with the number of vectors in the output embedding. Higher-resolution images contain more patches, so they produce larger embeddings. For example, a 2048×2048 square page produces embeddings containing 4,200 vectors withNeoMME-Retriever, or about 2.1 MB in float32. Across the ViDoRe v3 benchmark, the measured average is about 1.5 MB per document.

To reduce the storage footprint of the late-interaction index, we combine two complementary compression methods:

1. Hierarchical token poolingclusters similar document vectors in a given multi-vector embedding and replaces each cluster with its mean, hence reducing the number of vectors stored for each page.
2. Asymmetric quantizationquantizes document embeddings to int8 or binary. Because query embeddings are not stored and only generated on-the-fly, they can be kept at a higher precision.

We tested this setup on ViDoRe v3. With a pooling factor 10 and int8 queries and documents, storage decreased from about 1.5 MB to 39 kB per page, a 39× reduction, while keeping more than 99% of the baseline nDCG@10. A more aggressive configuration uses pooling factor 8, int8 queries, and binary documents. That version uses 6 kB per page (255× smaller) and keeps more than 95% of the original retrieval quality.

Users can pick a compression setting from that frontier based on storage budget and required retrieval quality.

#### Fast inference for cheaper multimodal corpus indexing

Before you can search a corpus, a retriever model must turn your documents into embeddings, which will be stored in a vector store like Qdrant, Weaviate, or Milvus. Faster encoding makes building and adding new documents to the index faster, thus reducing the GPU uptime and compute cost required.

So we measured image encoding speeds forNeoMME-Retriever against other multimodal document retrievers. We used preprocessed image tensors and calibrated the batch size separately for each model and image size. At a matched 2048×2048 input size on one NVIDIA L40S,NeoMME-Retriever-260M encodes about 51 pages per second, nearly twice ColModernVBERT's 26 pages per second. Both 260M and 800MNeoMME-Retriever models are also faster than the other models we compared on smaller input images.

### TryNeoMME-Retriever yourself!

NeoMME-Retriever (260Mand800M) returns dense and multi-vector embeddings together. The example below scores two text queries against two document-page images with MeanMaxSim late interaction and dense cosine similarity.

```bash

pip install -U accelerate "transformers @ git+https://github.com/huggingface/transformers.git@main" "sentence-transformers>=6.0.0"

```

```python
from typing import Any, Literal

import requests
import torch
from PIL import Image
from sentence_transformers.util import cos_sim, mean_maxsim

from transformers import BatchFeature, NeoMMEForRetrieval, NeoMMEProcessor


def encode(
    messages: list[list[dict[str, Any]]],
    task: Literal["query", "document"],
) -> BatchFeature:
    return processor.apply_chat_template(
        messages,
        task=task,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
        processor_kwargs={"padding": "longest"},
    )


model_name = "Hcompany/NeoMME-260M-Retriever"
processor = NeoMMEProcessor.from_pretrained(model_name)
model = NeoMMEForRetrieval.from_pretrained(model_name, device_map="auto")


image_urls = [
    "https://github.com/tonywu71/colpali-cookbooks/blob/6ef1332da6bcb48c7ef1f19b25bfa555be7031a8/examples/data/shift_kazakhstan.jpg?raw=true",
    "https://github.com/tonywu71/colpali-cookbooks/blob/6ef1332da6bcb48c7ef1f19b25bfa555be7031a8/examples/data/energy_electricity_generation.jpg?raw=true",
]
documents = [Image.open(requests.get(url, stream=True).raw) for url in image_urls]


queries = [
    "Quelle partie de la production pétrolière du Kazakhstan provient de champs en mer ?",
    "Which hour of the day had the highest overall electricity generation in 2019?",
]

document_messages = [
    [{"role": "user", "content": [{"type": "image", "image": document}]}] for document in documents
]
query_messages = [[{"role": "user", "content": query}] for query in queries]

inputs_documents = encode(document_messages, "document").to(model.device)
inputs_text = encode(query_messages, "query").to(model.device)

with torch.inference_mode():
    document_outputs = model(**inputs_documents)
    query_outputs = model(**inputs_text)

late_scores = mean_maxsim(
    query_outputs.embeddings,
    document_outputs.embeddings,
    a_mask=inputs_text["attention_mask"],
    b_mask=inputs_documents["attention_mask"],
)
dense_scores = cos_sim(query_outputs.dense_embeddings, document_outputs.dense_embeddings)


print(late_scores, dense_scores)

```

### Fine-tuning with Sentence Transformers

We provide separatedenseandlate-interactioncheckpoints for fine-tuning withSentence Transformers v6. Following the same pattern as text encoders such as ModernBERT, Sentence Transformers loads the backbone throughNeoMMEModelrather than the dual-headNeoMMEForRetrievalclass. Sentence Transformers currently supports one retrieval head per model, so each checkpoint lets you fine-tune the dense or late-interaction head independently. To train both heads together, useNeoMMEForRetrievalwith a customTrainer.

### From retrieval to visual RAG

Visual document retrieval can be used as the first stage of a visual retrieval-augmented generation (RAG) system. Unlike text RAG, which retrieves extracted text chunks, visual RAG retrieves the original page images and sends them to a visual language model. The model can then use tables, plots, diagrams, and page layout that text extraction may flatten or omit. Here is how visual RAG works:

1. Indexing: Convert each PDF page to an image, generate an embedding with a retrieval model, and store the embeddings in a vector store.
2. Retrieval: Generate an embedding for the user's query with the same model and retrieve the top-k most relevant pages.
3. Generation: Append the images after the query in the chat message (e.g.,{query}{img_1}{img_2}...{img_k}) and send it to a VLM to generate the answer.

You can test visual RAG directly withNeoMME-Retriever in our HF Space: 🤗tonywu71/neomme-retriever-demo.

## Conclusion

NeoMMEreplaces separate pretrained image and text encoders with one long-context bidirectional Transformer. We train it from scratch to process both multilingual text tokens and raw 32×32 image patches.

NeoMME-Retriever is a fine-tuned version ofNeoMMEfor visual document retrieval. One forward pass produces both dense and late-interaction representations. The 260M model outperforms all evaluated models strictly below 800M parameters and, at a matched 2048×2048 input size, encodes pages at about 2× ColModernVBERT's throughput. To reduce the large storage footprint of late-interaction embeddings for high-resolution documents, we experimented with hierarchical token pooling and asymmetric quantization and managed to reduce the late-interaction embeddings from roughly 1.5 MB to 6 kB per page, a 255× compression, while retaining more than 95% of the baseline nDCG@10.

We release allNeoMMEmodel checkpoints and a day-zero Hugging Face Transformers implementation to allow practitioners to build efficient multimodal and multilingual representation models on top of our work.

## Acknowledgements

NeoMMEbegan as a side quest between two good friends. We worked with limited time and compute, and we decided to share the results so the community can build on them. We thank H Company for supporting the work and providing the compute used to trainNeoMME.

## Citation

[翻译失败，原文如下]

```bibtex
@misc{lac2026neommesingletowermultimodalnativemultilingual,
      title={NeoMME: A Single-Tower Multimodal-Native Multilingual Foundation Encoder for Efficient Fine-Tuning and Inference},
      author={Aurélien Lac and Tony Wu},
      year={2026},
      eprint={2609.01657},
      archivePrefix={arXiv},
      primaryClass={cs.IR},
      url={https://arxiv.org/abs/2609.01657},
}

```

---

> 本文由AI自动翻译，原文链接：[NeoMME: an efficient Multimodal-native and Multilingual Encoder](https://huggingface.co/blog/Hcompany/neomme)
> 
> 翻译时间：2026-09-04 07:07
