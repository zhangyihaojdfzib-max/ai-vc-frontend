---
title: How Hugging Face Inference Endpoints, Jobs, and Buckets Power Search on Papers
  with Code
title_original: How Hugging Face Inference Endpoints, Jobs, and Buckets Power Search
  on Papers with Code
date: '2026-08-21'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/pwc-search
author: ''
summary: '[翻译失败，原文如下]


  # How Hugging Face Inference Endpoints, Jobs, and Buckets Power Search on Papers
  with Code


  3 months ago, we started arevivalofPapers wit...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T02:59:45.611800'
---

[翻译失败，原文如下]

# How Hugging Face Inference Endpoints, Jobs, and Buckets Power Search on Papers with Code

3 months ago, we started arevivalofPapers with Code(see also theannouncement tweet). Its goal is to make open AI research accessible and digestible, so that people can easily find the artifacts related to a paper, find state-of-the-art (SOTA) across the various domains of AI, share interesting research and build on top of each other's work. In other words, its goal is to power the wave of research that leads to the nextTransformer.

Of course, making AI research accessible requires a powerful search engine, so that humans and agents can quickly find relevant and related work, either through the website or thepwc searchCLI command, which agents can use via theSkill.

It's important to note that searching for research is not quite the same as searching for regular text. A useful paper search engine should find an exact title or arXiv identifier, but it should also understand a query such as “small language models for code generation” even when those words do not appear together in a paper. It needs to recognize that “the original BERT paper” is a navigational request, tolerate an incomplete title or typos, and still respond quickly when a model service is cold or temporarily unavailable.

![Search results on Papers with Code for the query DINO.](/images/posts/5d7fc466e12d.png)

ForPapers with Code, we built this as ahybrid searchsystem. This is also based on our prior experience atML6, where we developedRAG-based systems for clients. It turned out that hybrid search typically outperforms keyword- and vector-based search systems, as it combines the best of both worlds (see alsothis blogfor more info). Keyword search finds exact mentions, whereas vector search finds more fuzzy, semantically similar terms. Note thatrerankers(also called cross-encoders) can further improve the results, although they also come with additional overhead and latency.

![Hybrid retrieval outperforms keyword- and vector-only search. Figure from Microsoft,Azure AI Search: Outperforming vector search with hybrid retrieval and reranking(2023).](/images/posts/23b0926a28c8.png)

Papers with Code relies on a PostgreSQL database, hence its full-text search capabilities provide a fast lexical baseline. For dense embeddings,pgvectoris used to add semantic recall, and thereciprocal rank fusion (RRF)algorithm combines the two. Three Hugging Face services are used for the dense embeddings:

- Hugging Face Jobsgives us burstable GPU compute for embedding the paper corpus.
- Hugging Face Storage Bucketsprovides the durable handoff between our database, experiments, and Jobs.
- Hugging Face Inference Endpointsserves low-latency embeddings for live queries and incremental updates.

Today, the system maintains embeddings for more than 110,000 current papers sourced fromarXivandDaily Papers. This post explains the architecture, the design decisions behind it, and the lessons we learned while taking it to production.

## TL;DR

We deliberately split search into an offline corpus build and an online search service:

![Architecture of the offline corpus build and online hybrid search pipeline.](/images/posts/eecb46a9de7f.png)

The expensive, throughput-oriented work runs as Jobs. Durable artifacts live in a Bucket. Only the small query-embedding step sits on the request path, behind a protected Inference Endpoint, to power the online search. If that endpoint is cold, busy, or unhealthy, search immediately falls back to full-text retrieval. This separation makes the system both powerful and fast.

## Start with a strict embedding contract

Embedding pipelines often fail in subtle ways: a model revision changes, query and document prompts are mixed up, vectors are truncated differently, or an updated abstract no longer matches its stored vector.

We avoid this by treating the embedding format as a versioned API. Every paper is encoded as:

```text
normalized title + "\n\n" + normalized abstract

```

For each vector generation, we record:

- the model repository and exact revision;
- the output dimension;
- the input-format version;
- whether the input is a query or a document;
- the normalization method;
- a content hash for the source title and abstract.

Our production generation usesQwen/Qwen3-Embedding-0.6B, pinned to an exact revision, with 256-dimensional L2-normalized vectors. We selected the model with help from theMTEB leaderboard, the go-to benchmark for comparing embedding models. Note that newer embedding models like Qwen3 allow for 2 new features:

- one can specify adynamic embedding size, which allows to trade-off quality with speed/storage costs. Qwen models call this "MRL" which is short forMatryoshka Representation Learning. You can learn all about ithere. We chose an embedding size of 256 to make the search fast.
- one can provide aninstruction prompt. Qwen embedding models support adocumentprompt (which we use to embed the papers) and live searches use theirqueryprompt (to embed the user query).

This contract follows an embedding from export, through GPU inference, into PostgreSQL, and finally into online retrieval.

## Jobs turn a database snapshot into a vector corpus

Full-corpus embedding is a classic batch workload. It needs a GPU for a relatively short period, benefits from high throughput, and should not consume resources between runs.Hugging Face Jobsfits that shape well: a Job is defined by a command, ahardware flavor, and optionally a Docker image, and can runuvscripts with their dependencies declared inline.

Our corpus build starts by exporting the latest version of every paper from a repeatable-read PostgreSQL snapshot. The exporter streams rows rather than loading the catalog into memory, writes bounded JSONL shards, and creates a manifest containing row counts and SHA-256 checksums.

We sync that immutable run directory to a privateStorage Bucketand mount the Bucket directly (usinghf-mount) into anl4x1Job (an NVIDIA L4 GPU, which has 24GB of VRAM). From the worker's perspective it is simply a filesystem:

```bash
hf jobs uv run \
  --flavor l4x1 \
  --timeout 6h \
  --volume hf://buckets/OWNER/pwc-paper-embeddings:/bucket \
  embed_papers_job.py \
  --input /bucket/runs/RUN_ID/input \
  --output /bucket/runs/RUN_ID/output \
  --model Qwen/Qwen3-Embedding-0.6B \
  --revision MODEL_REVISION \
  --dimensions 256 \
  --allow-matryoshka

```

The worker:

1. verifies the input manifest and every shard checksum;
2. loads the pinned model revision;
3. sorts texts by length to reduce padding;
4. callsencode_documentin batches (as noted in themodel card);
5. reduces the batch size automatically if the GPU runs out of memory;
6. truncates theMatryoshka representationto 256 dimensions and normalizes it;
7. writes float16 Parquet shards atomically; and
8. records throughput, package versions, hardware, peak VRAM, row counts, and output checksums.

Each completed shard has its own marker, so a restarted Job can skip verified work. This is useful for a large corpus: retrying should just resume work rather than overwriting existing embeddings.

In our 5,000-paper pilot, the Qwen Job encoded about 75 papers per second at 1024 dimensions on an L4 GPU. The same pass could be deterministically materialized at 512 and 256 dimensions, so we could compare the storage and retrieval trade-offs without paying for more inference.

## Buckets are the connective tissue

Storage Bucketsare mutable, S3-like object storage on the Hub, optimized for AI workloads. They can be accessed throughhf://buckets/...paths andmountedread-write in Jobs without building a separate storage integration.

For us, the Bucket is more than a place to put vectors. It is the boundary between three systems with different lifecycles:

- the production database exports source records;
- ephemeral Jobs consume those records and produce vectors;
- the importer validates the results before touching the search index.

[翻译失败，原文如下]

We organize artifacts under immutable run prefixes:

```text
runs/<run-id>/
├── input/
│   ├── manifest.json
│   └── papers-*.jsonl
└── output/
    ├── manifest.json
    ├── embeddings-*.parquet
    └── embeddings-*.complete.json

```

Buckets themselves are intentionally mutable, so immutability is an application-level rule: a run ID is never overwritten, and every artifact is covered by a manifest and checksum.

This gives us several useful properties:

- Reproducibility:we can trace a database generation back to an exact corpus snapshot, model revision, and set of artifacts.
- Safe retries:Jobs can resume from completed shards in the same run prefix.
- Cheap experiments:several models or dimensions can reuse one verified input snapshot.
- Controlled rollout:importing a generation does not activate it. We first validate coverage and build its index.
- Simple rollback:the previous generation and its artifacts remain available until the new one is proven stable.

Only after the importer rechecks schemas, checksums, dimensions, normalization, unique paper IDs, and current content hashes do we load the vectors into PostgreSQL. We then build a separateHNSWindex for the new generation and atomically mark it active only when every eligible current paper is covered (HNSW is the graph-based algorithm that enables fast vector search).

## Inference Endpoints put semantic search on the request path

Batch embeddings solve the document side of retrieval. A user query still needs to be embedded at request time using the same model contract.

We deploy the pinned model as an authenticatedInference Endpointbacked byText Embeddings Inference (TEI). The endpoint accepts the query text and returns a normalized 256-dimensional vector using the model'squeryprompt. Note that one could also leveragevLLMorSGLanghere.

![Hugging Face Inference Endpoint for the Papers with Code query embedding model.](/images/posts/46b1505cc64c.png)

The API then performs a cosine-distance search over the active pgvector generation:

```sql
SELECT paper_id,
       embedding <=> CAST(:query_vector AS halfvec(256)) AS distance
FROM paper_embeddings
WHERE generation_id = :active_generation
ORDER BY embedding <=> CAST(:query_vector AS halfvec(256))
LIMIT 50;

```

The HNSW index keeps this lookup fast. On our 5,000-paper pilot, the 256-dimensional Qwen index achieved 0.9955 Recall@20 against exact search, with 1.31 ms p50 and 2.21 ms p95 HNSW lookup latency. Its table and index used about 27% of the storage of the 1024-dimensional version while retaining essentially the same ANN recall in that test.

The Endpoint is configured with a maximum of one replica and canscale to zerowhen idle. That is a useful cost lever, as this means you're not paying when there's no usage. However, this also means cold starts must be part of the application design rather than treated as an exceptional event, as it takes some time for the endpoint to spin up and serve traffic.

Our query client therefore has deliberately strict behavior:

- a one-second production timeout;
- a non-blocking concurrency limit;
- response dimension, finiteness, and norm validation;
- a short cache keyed by the query and embedding generation;
- a circuit breaker after repeated failures; and
- no raw query text in logs, only a normalized fingerprint.

If the endpoint is scaling up, times out, returns a malformed vector, or has no concurrency available, we skip the semantic branch immediately. Users still receive lexical results instead of waiting for an unreliable dependency.

Inference Endpoints works really reliably, and includes a nice dashboard so you can quickly see key analytics.

![Inference Endpoint analytics showing request volume, errors, latency, and replica state.](/images/posts/cd538a0aafdc.png)

## Hybrid retrieval is stronger than either branch alone

For every query, the lexical branch retrieves up to 50 candidates using weighted PostgreSQL full-text search. The semantic branch retrieves up to 50 candidates from pgvector.

We combine their ranks using weighted reciprocal rank fusion (RRF):

score(d)=∑r∈{lexical,semantic}wrk+rankr(d)\text{score}(d) = \sum_{r \,\in\, \{\text{lexical},\, \text{semantic}\}} \frac{w_r}{k + \text{rank}_r(d)}score(d)=r∈{lexical,semantic}∑​k+rankr​(d)wr​​

RRF is simple and robust, because it combines ranks rather than scores from two systems with different scales. Basically, if a paper is ranked high both by the lexical branch and the semantic branch, it has a higher chance of being ranked high by the hybrid search. We currently use equal branch weights and (k=60) (k is the "rank constant", a hyperparameter of the RRF algorithm).

Dense retrieval improves recall for conceptual queries. Full-text retrieval remains excellent for exact terminology, identifiers, and rare names. We also preserve deterministic identity behavior on top of the fused ranking:

- exact titles and arXiv IDs stay at the top;
- themethod taxonomyrecognizes navigational searches such as “the original BERT paper”;
- incomplete titles and bounded spelling mistakes use conservative trigram candidates; and
- ambiguous fuzzy matches abstain rather than forcing a bad result.

Note: hybrid search isn't always the best option, it is recommended to start with keyword search as a cheap and fast baseline, and only adding semantic and/or hybrid search when it turns out those give a reasonable boost in retrieval quality. One could further improve the search by adding a reranker after keyword/semantic/hybrid retrieval, using a model likeQwen3-Reranker.

## One Endpoint, two update paths

The large initial corpus is embedded with Jobs, but Papers with Code changes continuously. New papers arrive, abstracts are corrected, and new arXiv versions become current.

Launching a GPU Job for a handful of changed rows would add unnecessary startup and orchestration overhead. Instead, an hourly incremental process selects missing or content-changed papers and sends a bounded delta to the same TEI Endpoint, this time with thedocumentprompt.

Each run processes at most 500 papers in batches of 16. Before an embedding is written, the source row is locked and its content hash is checked again. If a paper changed during inference, that vector is discarded and picked up by the next run.

This gives us a useful division of labor:

- Jobshandle full rebuilds, new model generations, and large backfills.
- Inference Endpointshandle interactive query embeddings and small incremental document updates.
- Bucketspreserve the large-build artifacts and make those builds resumable and auditable.

The hourly path keeps the active index close to the live catalog without turning an online endpoint into an unbounded batch processor.

---

> 本文由AI自动翻译，原文链接：[How Hugging Face Inference Endpoints, Jobs, and Buckets Power Search on Papers with Code](https://huggingface.co/blog/pwc-search)
> 
> 翻译时间：2026-08-26 02:59
