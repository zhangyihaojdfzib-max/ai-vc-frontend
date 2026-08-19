---
title: Multi-Vector (Late Interaction) Embedding Models with Sentence Transformers
title_original: Multi-Vector (Late Interaction) Embedding Models with Sentence Transformers
date: '2026-08-18'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/multi-vector-encoder
author: ''
summary: '[翻译失败，原文如下]


  # Multi-Vector (Late Interaction) Embedding Models with Sentence Transformers


  Sentence Transformersis a Python library for using and tra...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-19T03:07:45.247215'
---

[翻译失败，原文如下]

# Multi-Vector (Late Interaction) Embedding Models with Sentence Transformers

Sentence Transformersis a Python library for using and training embedding and reranker models for applications like retrieval augmented generation, semantic search, and more. With the v6.0 update, it gains a fourth model type:MultiVectorEncoder, for ColBERT-style late interaction retrieval. AnyPyLatecheckpoint and anyStanford-NLP ColBERTcheckpoint loads straight into it, andcolpali-enginemodels for visual document retrieval can be used too, through the same familiar API you already use for dense, sparse, and reranker models.

Where a regular embedding model compresses a whole text into one vector, a multi-vector model keepsone vector per tokenand scores query against document with the MaxSim operator. That preserves token-level matching information that a single vector has to average away, which usually means stronger retrieval at the cost of a bigger index. It's also the state of the art for visual document retrieval, where a text query is matched against page images directly, with no OCR step in between.

In this blogpost, we'll show you how to use these models: loading the various checkpoint formats, encoding and scoring, plugging them into a search stack, running them on page images, and keeping the index affordable. Everything below runs on a plainpip install -U sentence-transformers.

- What are Multi-Vector Models?The MaxSim OperatorWhat You Gain, and What It Costs
- Installation
- Loading a ModelInspecting What a Checkpoint Configured
- Encoding Queries and Documents
- Scoring with MaxSimScore Magnitude and MeanMaxSim
- Semantic Search
- Retrieve and Rerank
- Indexing
- Visual Document Retrieval
- Audio Retrieval
- Video Retrieval
- Interpretability
- Token Pooling
- Speeding Up Inference
- Evaluating a Model
- Coming from PyLate or colpali-engine
- Supported Models
- Acknowledgements
- Additional Resources

- The MaxSim Operator
- What You Gain, and What It Costs

- Inspecting What a Checkpoint Configured

- Score Magnitude and MeanMaxSim

## What are Multi-Vector Models?

A dense embedding model reads a text and returns a single fixed-size vector. Everything the model noticed has to fit in those 384, 768, or 1024 numbers, and similarity is one dot product between two such summaries. This works remarkably well, but the compression is lossy in a specific way: a rare entity, an exact identifier, or one crucial clause in a long passage all have to compete for room in the same vector. A query with several requirements at once runs into the same wall. For "green sofa with wooden legs and rounded cushions", a single vector has to blend all four into one point, so a green sofa with the wrong legs ends up sitting close to the one you actually asked for.

A multi-vector model (also called a late-interaction or ColBERT-style model, after theColBERT paper) skips that compression. It runs the same transformer, but instead of pooling the token embeddings into one vector, it projects each token embedding down to a small dimension (classically 128) and keeps all of them. A 9-token document becomes a 9x128 matrix, not a 1x128 vector.

The interaction between query and document is then deferred until scoring time, which is where the name "late interaction" comes from. A cross-encoder interacts early: both texts go through the model together, which is accurate but leaves nothing to precompute, since every document has to be re-encoded for each new query. A bi-encoder, which is what the dense embedding model above is, barely interacts at all (one dot product between two finished summaries), and that is exactly what lets you encode a collection once and query it fast. Late interaction sits in between: documents are still encoded independently and can be indexed offline, but scoring compares every query token against every document token, which leaves far more room for the two to interact.

![Dense embedding versus multi-vector late interaction: a dense model encodes each text into one vector and scores with cosine similarity, while a multi-vector model keeps one vector per token and scores every query token against every document token with MaxSim](/images/posts/1743f5838524.gif)

### The MaxSim Operator

Scoring uses MaxSim: for each query token, take its highest similarity against any document token, then sum those maxima across the query.

MaxSim(Q,D)=∑Qi∈Qmax⁡Dj∈DQi⋅Dj\text{MaxSim}(Q, D) = \sum_{Q_i \in Q} \max_{D_j \in D} Q_i \cdot D_jMaxSim(Q,D)=Qi​∈Q∑​Dj​∈Dmax​Qi​⋅Dj​

Because the token embeddings are L2-normalized, each of those dot products is a cosine similarity in[-1, 1], so the whole sum lands within[-num_query_tokens, num_query_tokens].

You can read the operator as a soft alignment: every query token points at the one document token that best explains it, and the score is how well the document supports the query overall.

The alignment doesn't have to be lexical, since the token embeddings are contextualized. Encode "Where do penguins live?" against "Penguins inhabit Antarctica." withlightonai/mLateOnand the query tokenlivefinds its best match oninhabitat 0.94, a word it shares no characters with! That is the thing lexical retrieval cannot do, BM25 and its relatives need the term itself, so synonyms and paraphrases slip past them. Dense embedding models bridge that gap as well, of course. What late interaction adds is that it does so without giving up the other direction: when an exact match is what matters (a product code, a surname, a function name), MaxSim still has that token sitting there on its own, where a single-vector model had to average it in with everything else. It isn't one-to-one either, since several query tokens routinely settle on the same document token.

### What You Gain, and What It Costs

You gain retrieval quality, particularly on queries where one specific piece of a document is what makes it relevant, on multi-requirement queries like the sofa above where each requirement gets to find its own evidence, and on out-of-domain data where a dense model's compression was tuned for a different distribution. That compression is learned from the training queries, so the model learns to keep what they needed and drop everything else, which may include exactly what your production queries ask about. The effect grows with document length, since more text has to fit in the same fixed vector.

The cost is index size. One vector per token instead of one vector per document is a lot more vectors, only partly offset by the smaller dimension. Encoding 4,874 Natural Questions passages withlightonai/LateOnproduced 608,414 token vectors, an average of 124.8 per passage:

That's about 42x the storage of the MiniLM index, or 62 KiB per passage. However, indexes are often compressed, e.g. the same 608,414 vectors take 92 MB as afast-plaidindex, since PLAID stores a centroid id plus a quantized residual per vector rather than the vector itself. For scale, a 4096-dimensional dense model likeQwen3-Embedding-8Bwould need about 80 MB for these same 4,874 passages, so a compressed multi-vector index sits in the same territory as the dense indexes people already run.Token Poolingcuts the vector count before any of that, andRetrieve and Rerankavoids building an index at all.

PyLatecomes up throughout this post, so briefly: Sentence Transformers handled dense and sparse models but not late interaction, soLightOnbuilt PyLate on top of it to close that gap, adding the training, inference, and retrieval pieces these models need. Much of what you'll load below was trained with it, and LightOn built an ecosystem around it too, includingfast-plaid, the late-interaction index that turns up inIndexing. With v6.0 those capabilities live in Sentence Transformers itself.

With the tradeoff in mind, let's get a model running.

## Installation

Multi-vector models work with a plain install:

```bash
pip install -U sentence-transformers

```

[翻译失败，原文如下]

For ColPali-style visual document retrieval, you also need the image dependencies (seeInstallationfor all extras, andMultimodal Embedding & Reranker Modelsfor multimodal support in general):

```bash
pip install -U "sentence-transformers[image]"

```

Sentence Transformers v6.0 requirestransformersv5.x,torch2.2+, andhuggingface-hubv1.x. If you pin any of those lower, plan the upgrade first. See theMigration Guidefor the full list of breaking changes.

## Loading a Model

Loading a multi-vector model looks exactly like loading any other Sentence Transformers model:

```python
from sentence_transformers import MultiVectorEncoder

model = MultiVectorEncoder("lightonai/LateOn")

```

To find models that work, look for themulti-vectorandsentence-transformerstagson the Hub. Any model with those tags loads with the line above, whether it started life as a PyLate checkpoint, a Stanford-NLP ColBERT checkpoint, or a ColPali-family model for visual document retrieval. We're working through the ecosystem to get that tag onto every model that works, so the list keeps growing.

Underneath,MultiVectorEncoderreads each of the formats these checkpoints have been published in over the years, so PyLate and Stanford-NLP checkpoints load directly even where the tag hasn't been added yet:

```python
from sentence_transformers import MultiVectorEncoder



model = MultiVectorEncoder("lightonai/LateOn")
model = MultiVectorEncoder("mixedbread-ai/mxbai-edge-colbert-v0-17m")
model = MultiVectorEncoder("LiquidAI/LFM2.5-ColBERT-350M", trust_remote_code=True)



model = MultiVectorEncoder("colbert-ir/colbertv2.0")
model = MultiVectorEncoder("answerdotai/answerai-colbert-small-v1")


model = MultiVectorEncoder("answerdotai/ModernBERT-base")

```

Visual document retrieval models are the exception. ColPali-family checkpoints ship in colpali-engine's own format, which carries no information Sentence Transformers can use, so each one needs a small configuration added to its repository before it loads. Most of that work is done and waiting to be merged. SeeSupported Modelsfor the current state and how to load them today.

### Inspecting What a Checkpoint Configured

Multi-vector models carry a handful of recipe knobs that differ per checkpoint: marker prefixes for queries and documents, length caps, whether queries are padded out with[MASK]tokens, and which tokens are skipped when scoring documents. All of them live in the module configs, soprint(model)shows you exactly what you loaded. Here's the original ColBERTv2 checkpoint, which pads every query to exactly 32 tokens and truncates documents at 180:

```python
from sentence_transformers import MultiVectorEncoder

model = MultiVectorEncoder("colbert-ir/colbertv2.0")
print(model)
"""
MultiVectorEncoder(
  (0): Transformer({..., 'document_length': 180,
                    'query_expansion': {'strategy': 'fixed', 'attend': False, 'token': None, 'length': 32}})
  (1): Dense({'in_features': 768, 'out_features': 128, 'bias': False, ...})
  (2): MultiVectorMask({'skiplist_words': ['!', '"', '#', ...], 'skiplist_tasks': ['document'], ...})
  (3): Normalize({...})
)
"""
print(model.prompts)


```

That's the classic ColBERT pipeline: aTransformerproducing contextualized token embeddings, a token-levelDenseprojecting each of them to 128 dimensions, aMultiVectorMaskdeciding which tokens count during scoring, and a token-levelNormalize. Other checkpoints fill in different values.lightonai/GTE-ModernColBERT-v1uses the same four modules with[Q]and[D]prompts, no query expansion, and caps of 48 and 300.

You rarely need to touch any of this, since every released checkpoint configures its own. It matters when you build a model from a bare backbone, which is covered inCreating Custom Models.

One value is worth checking against your own data, though.document_lengthtruncates, so anything past it never reaches the index. For example, a 662-token passage through LateOn's cap of 300 comes back as 273 vectors, with the rest of the passage simply gone. Most of these checkpoints were trained on short passages, so if your chunks are longer than the cap, you can lift it for a single call withencode_document(..., processing_kwargs={"text": {"max_length": 512}}), keeping in mind that you would be running the model past the length it was trained on and that the index grows roughly in proportion. Multi-vector models tend to tolerate that well. OnMLDR, a long-document retrieval benchmark, the multilingual siblings of the pair above show the gap clearly:mLateOn scores 77.92 against mDenseOn's 51.59.

## Encoding Queries and Documents

Multi-vector models are asymmetric: queries and documents go through different prefixes, different length caps, and different scoring masks. Unlike many dense models, where the two are interchangeable,encode_query()andencode_document()are required to get correct embeddings:

```python
from sentence_transformers import MultiVectorEncoder

model = MultiVectorEncoder("lightonai/mLateOn")

queries = ["What is the capital of France?"]
documents = [
    "Paris is the capital of France.",
    "Berlin is the capital and largest city of Germany, by both area and population.",
]

query_embeddings = model.encode_query(queries)
document_embeddings = model.encode_document(documents)

print(query_embeddings[0].shape)

print(document_embeddings[0].shape, document_embeddings[1].shape)


```

Note what you get back: alistof 2D tensors, one per input, each of shape(num_tokens, embedding_dim). Unlike dense embeddings, you can't stack these into one rectangular tensor, because every input has its own token count. The second document is longer than the first, so it comes back as a taller matrix.

Each call applies the model's own recipe for you.encode_queryprepends the query marker, expands the query to a fixed length if the checkpoint asks for it, and caps it at the query length.encode_documentprepends the document marker, caps at the document length, and drops any skiplisted tokens (punctuation, for most checkpoints) from the scoring mask.

The usualencode()arguments all still apply, sobatch_size,show_progress_bar,convert_to_numpy,device, and multi-process pools work the way you'd expect:

```python
document_embeddings = model.encode_document(
    documents,
    batch_size=64,
    show_progress_bar=True,
)

```

## Scoring with MaxSim

model.similarity()computes the full all-pairs MaxSim matrix:

```python
from sentence_transformers import MultiVectorEncoder

model = MultiVectorEncoder("lightonai/LateOn")

query_embeddings = model.encode_query(["Which planet is known as the Red Planet?"])
document_embeddings = model.encode_document([
    "Venus is often called Earth's twin because of its similar size and proximity.",
    "Mars, known for its reddish appearance, is often referred to as the Red Planet.",
    "Jupiter, the largest planet in our solar system, has a prominent red spot.",
    "Saturn, famous for its rings, is sometimes mistaken for the Red Planet.",
])

scores = model.similarity(query_embeddings, document_embeddings)
print(scores)


```

Mars wins, as it should. Note how close the runners-up are: Saturn also contains the literal phrase "the Red Planet", and Jupiter is a planet with a red spot, so a token-level operator has plenty to latch onto in all three. The ordering is what matters.

Scores often sit this close together, asGLIntshows by measuring the spread across a full candidate pool. MaxSim takes amaximumper query token, so a document will usually give every query token some decent best match, and scores start from a floor. Contextualized token embeddings are also anisotropic, clustering in a narrow cone rather than spreading out, so even arbitrary token pairs tend to score high.

There is alsomodel.similarity_pairwise(), for when you already have matched pairs and just want the pair scores instead of the full similarity matrix:

```python
scores = model.similarity_pairwise(query_embeddings, document_embeddings[:1])
print(scores)

[翻译失败，原文如下]

```

### Score Magnitude and MeanMaxSim

MaxSim sums over query tokens, so its magnitude scales with how many query tokens there are, which means you can't compare scores across models with different query recipes. LateOn encodes the Red Planet query above as 12 tokens. Run that same query and those same documents through ColBERTv2, which pads and truncates every query to exactly 32 tokens, and the scores land in a completely different range:

```python
model = MultiVectorEncoder("colbert-ir/colbertv2.0")

print(scores)


```

Within one model the ordering is all you need, but if you want scores on a bounded scale, switch the model's similarity function to MeanMaxSim, which divides by the query token count. Back on LateOn:

```python
model = MultiVectorEncoder("lightonai/LateOn", similarity_fn_name="meanmaxsim")


print(model.similarity(query_embeddings, document_embeddings))


```

Now every score is an average cosine similarity in[-1, 1], although you'll only see[0, 1]in practice.

## Semantic Search

If your corpus is small, exhaustive MaxSim over all of it is the simplest thing that works. Encode the corpus once, then score each query against everything:

```python
import time

from datasets import load_dataset

from sentence_transformers import MultiVectorEncoder

dataset = load_dataset("sentence-transformers/natural-questions", split="train[:5000]")

corpus = list(dict.fromkeys(dataset["answer"]))  

model = MultiVectorEncoder("lightonai/LateOn")
corpus_embeddings = model.encode_document(corpus, show_progress_bar=True)

query = "when did richmond last play in a preliminary final"
start = time.perf_counter()
query_embeddings = model.encode_query([query])
scores = model.similarity(query_embeddings, corpus_embeddings)[0]  
top_scores, top_indices = scores.topk(3)
print(f"Search took {(time.perf_counter() - start) * 1000:.1f}ms")

for score, index in zip(top_scores.tolist(), top_indices.tolist()):
    print(f"{score:.4f}  {corpus[index][:100]}")
"""
Search took 122.7ms
11.9192  Richmond Football Club Richmond began 2017 with 5 straight wins, a feat it had not achieved
11.7591  2017 AFL Grand Final The 2017 AFL Grand Final was an Australian rules football game contest
11.6710  Battle of Appomattox Court House The Battle of Appomattox Court House (Virginia, U.S.), fou
"""

```

Those 4,874 passages encoded in 20 seconds on an RTX 3090, and each search takes about 120ms end to end, most of that the MaxSim scoring against all 608,414 token vectors. This is exact, but it scales linearly in total corpus tokens and keeps every token vector in memory, so reach for it when you have a few thousand documents rather than a few million. The runnable version of this script issemantic_search.py.

Past that size you want a real late-interaction index, which Sentence Transformers doesn't ship. It doesn't need to: these indexes store whateverencode_documentproduced, so you encode here and hand the token embeddings to something built for them.Indexinghas working snippets for four of the options, and the section directly below covers how to skip the index entirely.

## Retrieve and Rerank

You can also get late-interaction quality without maintaining a late-interaction index, by using a multi-vector model as yourreranker. A fast bi-encoder narrows a large corpus to a handful of candidates, then the multi-vector model rescores only those:

```python
from datasets import load_dataset

from sentence_transformers import MultiVectorEncoder, SentenceTransformer
from sentence_transformers.util import semantic_search

dataset = load_dataset("sentence-transformers/natural-questions", split="train[:50000]")
corpus = list(dict.fromkeys(dataset["answer"]))

retriever = SentenceTransformer("jinaai/jina-embeddings-v5-text-nano-retrieval")
reranker = MultiVectorEncoder("perplexity-ai/pplx-embed-v1-late-0.6b", trust_remote_code=True)


corpus_embeddings = retriever.encode_document(corpus, convert_to_tensor=True, show_progress_bar=True)


query = "when did richmond last play in a preliminary final"
hits = semantic_search(retriever.encode_query([query], convert_to_tensor=True), corpus_embeddings, top_k=50)[0]
candidates = [corpus[hit["corpus_id"]] for hit in hits]


query_embeddings = reranker.encode_query([query])
document_embeddings = reranker.encode_document(candidates)
scores = reranker.similarity(query_embeddings, document_embeddings)[0]

for index in scores.argsort(descending=True)[:3].tolist():
    print(f"{scores[index].item():.4f}  {candidates[index][:100]}")

```

Only the 50 candidates are ever encoded as multi-vectors, so your index stays a normal dense index and the token vectors are transient. This is the same role a cross-encoder plays in a retrieve-and-rerank stack, but a multi-vector model is considerably cheaper per candidate. You encode the documents in one batch and score them with a matrix multiplication, instead of one forward pass per query-document pair. The runnable script isretrieve_rerank.py, which prints the timings of both stages.

## Indexing

Several vector databases index and score multi-vectors natively:Qdrantsince v1.10,Weaviatesince v1.29,Vespafor years now,LanceDBsince v0.15.0, andVectorChord, which adds a MaxSim operator to Postgres that plain pgvector doesn't have.Milvusjoined them in v2.6.4, under array-of-structs rather than the unrelated feature it calls multi-vector search. If you would rather not run a server at all, LightOn'sfast-plaidis apip installaway and implements PLAID directly, andPyLatewraps it in a fuller retrieval stack.

A few others get you partway.OpenSearchandElasticsearchcan rescore candidates with MaxSim but not retrieve on it, and the Elasticsearch field is additionally in technical preview and Enterprise-tier.turbopufferhas late-interaction indexing in private beta.

The snippets below index text, but nothing in them is text-specific.encode_documenthands back the same list of token-vector matrices whether the document was a passage, a page image, an audio clip, or a video, so the ColPali-style models fromVisual Document Retrievalgo into any of these unchanged. There are simply more vectors per document, which is what makesToken Poolingworth reaching for sooner there.

fast-plaid, Qdrant, Weaviate, and Vespa all take exactly whatencode_documentreturns, so the code is the same up to the client library. Here's a working snippet for each, run against the 4,874 passages and 608,414 token vectors from theSemantic Searchexample. Each one carries the ingestion and query times it produced on one machine (RTX 3090, i7-13700K), with no tuning beyond what the code shows, to give a sense of the shape of the work. All four answer the query faster than the 98msmodel.similaritytook in that section, and three of them do it on the CPU, since fast-plaid is the only one here using the GPU.

All four returned the same three passages in the same order as the exhaustive PyTorch MaxSim earlier in this post, and the three databases reproduce its scores to four decimals! That is because their snippets score every document, which is affordable at this size and removes approximation as a variable. fast-plaid is approximate by design, so its scores differ slightly. The notes under each one say what changes when you switch to an approximate index, which is where rankings start to drift.

fast-plaidis LightOn's Rust implementation of PLAID, the index ColBERT was originally built around. There's no server to start, and it reads the tensorsencode_documenthands back without any conversion.

```python

from datasets import load_dataset
from fast_plaid import search
from sentence_transformers import MultiVectorEncoder

dataset = load_dataset("sentence-transformers/natural-questions", split="train[:5000]")
corpus = list(dict.fromkeys(dataset["answer"]))
model = MultiVectorEncoder("lightonai/LateOn")
query = "when did richmond last play in a preliminary final"

[翻译失败，原文如下]

document_embeddings = model.encode_document(corpus, batch_size=32)
query_embedding = model.encode_query(query)

fast_plaid = search.FastPlaid(index="natural-questions", device="cuda")


fast_plaid.create(documents_embeddings=document_embeddings)

results = fast_plaid.search(queries_embeddings=query_embedding.unsqueeze(0), top_k=3)  

for index, score in results[0]:
    print(f"{score:.4f}  {corpus[index][:90]}")
"""
11.8828  Richmond Football Club Richmond began 2017 with 5 straight wins, a feat it had not achieve
11.7676  2017 AFL Grand Final The 2017 AFL Grand Final was an Australian rules football game contes
11.6758  Battle of Appomattox Court House The Battle of Appomattox Court House (Virginia, U.S.), fo
"""

```

Theindexargument is a directory, not just a label, so the index is written to disk as it is built. Pointing a newFastPlaidat the same path reopens it for searching or for adding more documents, instead of rebuilding from the embeddings each time. On this corpus it occupies 92 MB, against 311.5 MB for the raw float32 vectors.

This is the only one of the four that is approximate, and it is the one place in this section where the scores do not match the exhaustive MaxSim. PLAID prunes with centroids and stores quantized residuals, so the three scores drift by a few hundredths in both directions against the 11.9192 / 11.7591 / 11.6710 computed earlier. The ranking is unaffected here, and that is the trade PLAID is making: it was designed for corpora far larger than this one, where scanning everything is not an option.

Qdrantneeds a server:docker run -p 6333:6333 qdrant/qdrant. The client also has a local mode (QdrantClient(":memory:")) that needs no server, but it's a pure-Python reimplementation, so use it for trying things out rather than for timing them.

```python

from datasets import load_dataset
from qdrant_client import QdrantClient, models
from sentence_transformers import MultiVectorEncoder

dataset = load_dataset("sentence-transformers/natural-questions", split="train[:5000]")
corpus = list(dict.fromkeys(dataset["answer"]))
model = MultiVectorEncoder("lightonai/LateOn")
query = "when did richmond last play in a preliminary final"

document_embeddings = model.encode_document(corpus, batch_size=32)
query_embedding = model.encode_query(query)

client = QdrantClient("http://localhost:6333")
client.create_collection(
    collection_name="natural-questions",
    vectors_config=models.VectorParams(
        size=model.get_embedding_dimension(),
        distance=models.Distance.COSINE,
        multivector_config=models.MultiVectorConfig(
            comparator=models.MultiVectorComparator.MAX_SIM
        ),
        
        hnsw_config=models.HnswConfigDiff(m=0),
    ),
)


client.upload_points(
    collection_name="natural-questions",
    points=[
        models.PointStruct(id=idx, vector=embedding, payload={"text": text})
        for idx, (embedding, text) in enumerate(zip(document_embeddings, corpus))
    ],
    batch_size=64,
)

results = client.query_points(
    collection_name="natural-questions",
    query=query_embedding,
    limit=3,
    with_payload=True,
).points  

for result in results:
    print(f"{result.score:.4f}  {result.payload['text'][:90]}")
"""
11.9192  Richmond Football Club Richmond began 2017 with 5 straight wins, a feat it had not achieve
11.7591  2017 AFL Grand Final The 2017 AFL Grand Final was an Australian rules football game contes
11.6710  Battle of Appomattox Court House The Battle of Appomattox Court House (Virginia, U.S.), fo
"""

```

MAX_SIMis the only comparator Qdrant offers, andhnsw_config=HnswConfigDiff(m=0)is their recommendation for late-interaction fields, since the vectors are used for rescoring rather than graph traversal. Note that Qdrant themselves suggest reserving late interaction for reranking a few hundred candidates rather than scanning a whole collection, which is theRetrieve and Rerankpattern. At 4,874 documents the full scan costs 18ms and is exact, but that doesn't extrapolate.

Weaviateneeds a server too:docker run -p 8080:8080 -p 50051:50051 cr.weaviate.io/semitechnologies/weaviate:1.34.0. Multi-vector support needs 1.29 or newer, and the embedded mode isn't available on Windows.

```python

import weaviate
from datasets import load_dataset
from sentence_transformers import MultiVectorEncoder
from weaviate.classes.config import Configure, DataType, Property
from weaviate.classes.query import MetadataQuery

dataset = load_dataset("sentence-transformers/natural-questions", split="train[:5000]")
corpus = list(dict.fromkeys(dataset["answer"]))
model = MultiVectorEncoder("lightonai/LateOn")
query = "when did richmond last play in a preliminary final"

document_embeddings = model.encode_document(corpus, batch_size=32)
query_embedding = model.encode_query(query)

client = weaviate.connect_to_local()
collection = client.collections.create(
    "Documents",
    
    vector_config=[Configure.MultiVectors.self_provided(name="colbert")],
    properties=[Property(name="text", data_type=DataType.TEXT)],
)


with collection.batch.fixed_size(batch_size=64) as batch:
    for text, embedding in zip(corpus, document_embeddings):
        batch.add_object(properties={"text": text}, vector={"colbert": embedding.tolist()})

results = collection.query.near_vector(
    near_vector=query_embedding.tolist(),
    target_vector="colbert",
    limit=3,
    return_metadata=MetadataQuery(distance=True),
)  

for result in results.objects:
    
    print(f"{-result.metadata.distance:.4f}  {result.properties['text'][:90]}")
"""
11.9192  Richmond Football Club Richmond began 2017 with 5 straight wins, a feat it had not achieve
11.7591  2017 AFL Grand Final The 2017 AFL Grand Final was an Australian rules football game contes
11.6710  Battle of Appomattox Court House The Battle of Appomattox Court House (Virginia, U.S.), fo
"""

client.close()

```

Defaults are enough here: Weaviate's dynamicefresolves to 100 for a top-3 query, and this ranking is already exact from about 32 upward. That margin is a property of the embeddings rather than of Weaviate, so it's worth confirming on your own model instead of assuming the defaults hold.

Weaviate also supports MUVERA encoding, which made ingestion 3x faster and queries 1.8x faster in our test. It cost far more accuracy than that speed is worth at this size though: the correct third passage didn't appear even in its top 50.

Vespaalso runs in a container, butpyvespastarts it for you, so there's no separatedocker run.

```python

from datasets import load_dataset
from sentence_transformers import MultiVectorEncoder
from vespa.deployment import VespaDocker
from vespa.package import (
    ApplicationPackage, Document, Field, FirstPhaseRanking, Function, RankProfile, Schema,
)

dataset = load_dataset("sentence-transformers/natural-questions", split="train[:5000]")
corpus = list(dict.fromkeys(dataset["answer"]))
model = MultiVectorEncoder("lightonai/LateOn")
query = "when did richmond last play in a preliminary final"

document_embeddings = model.encode_document(corpus, batch_size=32)
query_embedding = model.encode_query(query)

[翻译失败，原文如下]

package = ApplicationPackage(
    name="colbert",
    schema=[
        Schema(
            name="doc",
            document=Document(fields=[
                Field(name="text", type="string", indexing=["summary"]),
                Field(name="colbert", type="tensor<float>(dt{}, x[128])", indexing=["attribute"]),
            ]),
            rank_profiles=[
                RankProfile(
                    name="colbert",
                    inputs=[("query(qt)", "tensor<float>(qt{}, x[128])")],
                    functions=[Function(
                        name="max_sim",  
                        expression="sum(reduce(sum(query(qt) * attribute(colbert), x), max, dt), qt)",
                    )],
                    first_phase=FirstPhaseRanking(expression="max_sim"),
                )
            ],
        )
    ],
)
app = VespaDocker(port=8080).deploy(application_package=package)  


def to_tensor(embedding):
    return {str(token): vector for token, vector in enumerate(embedding.tolist())}


app.feed_iterable(
    ({"id": str(idx), "fields": {"text": text, "colbert": to_tensor(embedding)}}
     for idx, (text, embedding) in enumerate(zip(corpus, document_embeddings))),
    schema="doc",
)

response = app.query(body={
    "yql": "select text from doc where true",
    "ranking.profile": "colbert",
    "hits": 3,
    "input.query(qt)": to_tensor(query_embedding),
})  

for hit in response.hits:
    print(f"{hit['relevance']:.4f}  {hit['fields']['text'][:90]}")
"""
11.9192  Richmond Football Club Richmond began 2017 with 5 straight wins, a feat it had not achieve
11.7591  2017 AFL Grand Final The 2017 AFL Grand Final was an Australian rules football game contes
11.6710  Battle of Appomattox Court House The Battle of Appomattox Court House (Virginia, U.S.), fo
"""

```

Vespa asks for the most upfront structure of the four, because you're declaring a ranking pipeline rather than just an index. In exchange you get to write MaxSim out as a tensor expression and see exactly what it computes. This version puts MaxSim infirst-phaseoverwhere true, which scores all 4,874 documents and is why the output matches exhaustive MaxSim exactly. It's deliberately not what Vespa recommends at scale: theirColBERT sample appstores int8-binarized vectors and moves MaxSim intosecond-phaseto rerank a cheaper first stage.

Moving to that phased setup needs care:second-phaserescores only the best 100 candidates by default, and here that window left two of the three correct passages unscored entirely. Raisingrerank-countto cover your candidate set fixes that, though at this size the phased version still came out slower than simply scanning everything.

## Visual Document Retrieval

Late interaction is the state of the art for visual document retrieval: matching a text query against pageimages, with charts, tables, and layout intact, and no OCR step. This is what theColPalifamily of models does, and those checkpoints load and run through the same API, with therevisionpinning the open pull request that adds this one's Sentence Transformers configuration (Supported Modelshas the full list). Image documents are passed as URLs, local paths, or PIL images:

```python
from sentence_transformers import MultiVectorEncoder

model = MultiVectorEncoder("vidore/colqwen2.5-v0.2")

queries = [
    "What is the variable represented on the y-axis of the graph?",
    "Total outlay is maximum in which year?",
]
images = [
    "https://huggingface.co/datasets/sentence-transformers/example-documents/resolve/main/doc1.jpg",
    "https://huggingface.co/datasets/sentence-transformers/example-documents/resolve/main/doc2.jpg",
    "https://huggingface.co/datasets/sentence-transformers/example-documents/resolve/main/doc3.jpg",
    "https://huggingface.co/datasets/sentence-transformers/example-documents/resolve/main/doc4.jpg",
]

query_embeddings = model.encode_query(queries)
document_embeddings = model.encode_document(images)
print(query_embeddings[0].shape, document_embeddings[0].shape)


scores = model.similarity(query_embeddings, document_embeddings)
print(scores)



```

Each query retrieves its own page (the diagonal), and the second query separates much more cleanly than the first, since only one of the four pages is about outlay over time.

The code is unchanged. Underneath, the processor handles the visual prompt and the image patches, and MaxSim scores query text tokens against document image patches. A page holds many separate regions, which is exactly what makes late interaction a natural fit here, since a single vector would have to average a chart, a table, and three paragraphs into one summary. That fidelity costs index space, though. The shapes above are 755 token vectors for one page against 25 for the query, where a Natural Questions passage from earlier averaged about 125, sotoken poolingis worth reaching for earlier here than it is for text.

These are VLMs, so plan for the memory they need.The table in Supported Modelsruns from 252M to 8.8B parameters, and the small end of it stays practical on CPU where the multi-billion ones don't.

Page images are the common case, but they're not the only non-text modality. Sentence Transformers accepts text, images, audio, and video, and a checkpoint supports whichever of those its processor does, whichmodel.modalitiesreports. A single document can combine modalities too, by passing a dict like{"text": ..., "image": ...}in place of a bare value.Multimodal Embedding & Reranker Modelscovers multimodal models in Sentence Transformers more broadly, and theUsage documentationlists exactly which input formats each modality accepts.

## Audio Retrieval

vidore/colqwen-omni-v0.1is built on Qwen2.5-Omni and takes all four modalities. Retrieving a recorded conversation with it is the same two calls as retrieving a page:

```python

import torch
from datasets import Audio, load_dataset

from sentence_transformers import MultiVectorEncoder

model = MultiVectorEncoder(
    "vidore/colqwen-omni-v0.1",
    model_kwargs={"dtype": torch.bfloat16},
)
print(model.modalities)



dataset = load_dataset("eustlb/dailytalk-conversations-grouped", split="train[:20]")
dataset = dataset.cast_column("audio", Audio(sampling_rate=16_000))
audio = [row["array"] for row in dataset["audio"]]  

query_embeddings = model.encode_query(["medicine for car nausea"])
document_embeddings = model.encode_document(audio, batch_size=2)
scores = model.similarity(query_embeddings, document_embeddings)[0]

top_scores, top_indices = scores.topk(3)
for score, index in zip(top_scores.tolist(), top_indices.tolist()):
    print(f"{score:.4f}  {' / '.join(dataset[index]['texts'][:2])}")
"""
50.8902  Excuse me? Do you have anything for a carsickness? / Yes, but you look fine.
46.1028  Excuse me, could you tell me where you have got that music book? / Certainly. Let me see. Oh, it's on that shelf.
46.0514  Jeff, I'm going to the supermarket. Do you want to come with me? / I think the supermarket is closed now.
"""

```

ColQwen-Omni was trained purely on image-text pairs, so its audio retrieval is zero-shot: it never heard a training example, and there is no transcription step anywhere in the pipeline. The query saysnauseawhere the recording sayscarsickness, and it still picks the pharmacy conversation out of twenty by a wide margin.

## Video Retrieval

Video works the same way, but sample the frames or it will eat your VRAM. Itsrelease blogpostis blunt about this, that video "is very memory-intensive, so it's best suited for short clips":

```python
import torch

from sentence_transformers import MultiVectorEncoder

model = MultiVectorEncoder(
    "vidore/colqwen-omni-v0.1",
    model_kwargs={"dtype": torch.bfloat16},
)


model[0].processing_kwargs.update(
    {"video": {"max_pixels": 32 * 28 * 28, "do_sample_frames": True, "fps": 0.5}}
)

[翻译失败，原文如下]

query_embeddings = model.encode_query(["How to cook Mapo Tofu?"])
document_embeddings = model.encode_document([
    "https://huggingface.co/datasets/sentence-transformers/example-documents/resolve/main/mapo_tofu.mp4",
    "https://huggingface.co/datasets/sentence-transformers/example-documents/resolve/main/zhajiang_noodle.mp4",
], batch_size=1)
print(model.similarity(query_embeddings, document_embeddings))


```

At 1 fps and full resolution the same pair of videos produces 8,426 and 5,137 token vectors and peaks at 20.8 GB of VRAM, against 4,240 and 2,446 vectors and 12.5 GB here, for a model that occupies 9.0 GB on its own. The ranking is identical either way. Long audio wants the same treatment, and the release blogpost recommends 30-second chunks, which come to roughly 800 tokens each.

## Interpretability

Because MaxSim is a sum of per-query-token maxima, a ranking decomposes exactly: every point of a document's score belongs to one query token and one document token. That lets you answer "why did this rank here?" precisely, rather than by eye.

For image documents,sentence_transformers.multi_vector_encoder.interpretabilityoverlays that decomposition onto the page as the standard ColPali heatmap, either aggregated over the query or one map per query token. Asking "How much was spent on water resources and power?" against the outlays page from above, this is where thewatertoken went:

![MaxSim heatmap of the query token "water" overlaid on a 1971 US budget outlays page, with the brightest patch on the "Water Resources & Power" bar of the lower chart](/images/posts/d649546a05c2.png)

heatmap.pyis the runnable version, including the masking step that lines the document embedding up with the patch grid.

Text documents have no patch grid to overlay, but the same decomposition applies.text_similarity_map.pyranks a corpus and then attributes the top hit's score token by token, here on the Natural Questions corpus from earlier with the 32M-parametermxbai-edge-colbert-v0-32m:

```
Query: when did richmond last play in a preliminary final
Top 3 of 4874 documents by exhaustive MaxSim (191.0ms):
  12.3489  Richmond Football Club Richmond began 2017 with 5 straight wins, a feat it had not achieved since 19
  12.1771  2017 AFL Grand Final The 2017 AFL Grand Final was an Australian rules football game contested betwee
  12.0591  2018 UEFA Champions League Final The 2018 UEFA Champions League Final was the final match of the 201

  query token       best document token      sim   share
  when              since                 0.9154    7.4%
  did               had                   0.9675    7.8%
  rich              rich                  0.9764    7.9%
  mond              mond                  0.9856    8.0%
  last              to                    0.9249    7.5%
  play              game                  0.9384    7.6%
  in                the                   0.9732    7.9%
  a                 a                     0.9587    7.8%
  preliminary       preliminary           0.9394    7.6%
  final             final                 0.9654    7.8%
  --------------------------------------------------------
  3 special tokens                        2.8038   22.7%
  MaxSim score                           12.3489  100.0%

```

rich,mond,preliminary, andfinalmatched themselves, whilewhensettled onsinceandplayongame. The special tokens are worth noticing too: three of them contribute 22.7% of the score while carrying none of the query's content. Below this table the script prints the passage itself, with the winning tokens highlighted in place.

## Token Pooling

If the index footprint worries you, the most effective knob is to store fewer token vectors.HierarchicalTokenPoolingimplements thetoken poolingtechnique from Clavié, Chaffin, and Adams: it clusters each document's token vectors with Ward linkage on cosine distance and replaces each cluster with its mean, keeping roughly1 / pool_factorof the tokens. Within one document a lot of token vectors end up close to each other, so much of what you drop is redundancy rather than signal:

```python
from datasets import load_dataset

from sentence_transformers import MultiVectorEncoder
from sentence_transformers.multi_vector_encoder.modules import HierarchicalTokenPooling

dataset = load_dataset("sentence-transformers/natural-questions", split="train[:5000]")
documents = list(dict.fromkeys(dataset["answer"]))

model = MultiVectorEncoder("lightonai/LateOn")

pooling = HierarchicalTokenPooling(pool_factor=2)
document_embeddings = model.encode_document(documents, token_pooling=pooling)

```

There are three places to apply it, depending on when you want to pay for it:

```python

document_embeddings = model.encode_document(documents, token_pooling=pooling)


pooled = pooling.pool(document_embeddings)


model.append(HierarchicalTokenPooling(pool_factor=2))
model.save_pretrained("my-pooled-colbert")

```

By default, pooling applies to documents only, since queries are short and are the side you can't afford to distort. On the Natural Questions corpus from earlier, the reduction trackspool_factorclosely, and pooling all 608k token vectors took about 6 seconds:

A cluster mean is a worse match for a query token than the best of its members was, and the coarser the clusters, the more that shows. Theoriginal experimentsmeasured that cost on BEIR and found very little of it: 100.6% of the unpooled retrieval performance on average atpool_factor=2, and 99.0% atpool_factor=3. Halving your index for free is a good deal, so 2 is a reasonable place to start. How much it costs on your data is corpus-specific though, so measure it with anevaluatorbefore you settle on a factor. The runnable comparison istoken_pooling.py.

How far you can pushpool_factoris also partly a property of the model. LightOn'shierarchical pooling regularizationtrains for exactly that, shaping the embedding space so pooling costs less and reporting 99.4% retention at 5x compression. Training with that regularizer isn't in Sentence Transformers yet, but the resulting checkpoints are ordinary PyLate models, solightonai/LateOn-hpool-regularizedloads and pools like any other.

## Speeding Up Inference

Multi-vector models run through the same backend machinery as the rest of Sentence Transformers, so you gettorch(default),onnx, andopenvino, alongside half precision, Flash Attention, andtorch.compile.

On GPU, fp16 with Flash Attention is the best configuration we measured, at 2.44x the throughput of fp32 with no measurable retrieval quality loss. Flash Attention helps multi-vector models more than most, because documents are only truncated and never padded to a shared length, so your batches have widely varying sequence lengths that unpadding can exploit:

```python
from sentence_transformers import MultiVectorEncoder

model = MultiVectorEncoder(
    "lightonai/GTE-ModernColBERT-v1",
    model_kwargs={"attn_implementation": "flash_attention_2", "dtype": "float16"},
)

```

![GPU](/images/posts/1b8e5d5454d5.png)

![CPU](/images/posts/d6b5f7ea57a2.png)

Models with non-attend query expansion (attend=False, which covers the Stanford-NLP checkpoints likecolbert-ir/colbertv2.0andanswerdotai/answerai-colbert-small-v1) reject Flash Attention at load time. Flash Attention stripsattention_mask=0positions, so the[MASK]expansion tokens that MaxSim scores would never receive an attention update. Use"sdpa"for those models.

On CPU, OpenVINO is your better bet where the architecture is supported, and int8 quantization buys a further speedup at a cost of about 0.4% accuracy. SeeSpeeding up Inferencefor the full benchmark details, the export and quantization helpers, and a flowchart for picking a backend.

## Evaluating a Model

MultiVectorNanoBEIREvaluatorruns theNanoBEIRsuite of 13 small BEIR subsets with MaxSim scoring, and needs no data preparation on your side:

[翻译失败，原文如下]

```python
from sentence_transformers import MultiVectorEncoder
from sentence_transformers.multi_vector_encoder.evaluation import MultiVectorNanoBEIREvaluator

model = MultiVectorEncoder("lightonai/GTE-ModernColBERT-v1")
evaluator = MultiVectorNanoBEIREvaluator(batch_size=16)
results = evaluator(model)
print(f"{evaluator.primary_metric}: {results[evaluator.primary_metric]:.4f}")

```

This also makes it easy to check the claim from the top of this post.lightonai/LateOnandlightonai/DenseOnwere trained by LightOn on the same data with the same ModernBERT backbone and the same 149M parameters, differing only in whether they keep one vector per token or pool down to one per document. Running both over all 13 NanoBEIR datasets isolates what that choice buys:

Late interaction wins on 9 of the 13 datasets and on the mean, by roughly one NDCG point. The four it loses (ArguAna, FiQA2018, SCIDOCS, and SciFact) are the shape of the tradeoff you should expect: a real gain in retrieval quality at the same model size, paid for in index footprint, rather than a universal win on every dataset. The same pair scores 57.22 against 56.20 on the full 15-dataset BEIR, a comparable gap, so the margin is not an artifact of the small benchmark.

Alongside NanoBEIR,MultiVectorInformationRetrievalEvaluator,MultiVectorRerankingEvaluator,MultiVectorTripletEvaluator, andMultiVectorDistillationEvaluatorcover the usual evaluation setups on your own data. They're documented in theEvaluation API Reference.

## Coming from PyLate or colpali-engine

MultiVectorEncoderabsorbs the modeling, inference, training, and evaluation of both libraries. Every PyLate checkpoint loads directly, andSupported Modelslists the colpali-engine checkpoints along with therevisionto pass where one is still needed. If you're migrating, these are the calls that change:

One difference worth calling out: on abare(non-ColBERT) checkpoint, PyLate'sColBERT("bert-base-uncased")applies the classic recipe by default, whileMultiVectorEncoder("bert-base-uncased")builds a plain stack and leaves the prefixes, query expansion, and skiplist as explicit choices. The training loss and evaluator equivalents, and the data-handling differences, are in theMigration Guide.

Note that save compatibility is one-way in every case: PyLate, Stanford-NLP ColBERT, and colpali-engine checkpoints all load intoMultiVectorEncoder, butMultiVectorEncoder.save_pretrainedoutput isn't loadable by any of them.

## Supported Models

Models carrying themulti-vectorandsentence-transformerstagson the Hub are the list that stays current, and we're working to get those tags onto every model that works. The tables below are what we test against directly, so treat them as a starting point rather than the full set. For text retrieval in particular, any PyLate or Stanford-NLP ColBERT checkpoint loads whether or not it carries the tag yet.

Some entries need a small Sentence Transformers configuration added to their repository first, and several of those are still open pull requests at the time of writing. Where arevisionis listed below, pass it until that pull request is merged, after which the plain model name is enough:

```python
model = MultiVectorEncoder("vidore/colqwen-omni-v0.1", revision="refs/pr/N")

```

### Text Retrieval Models

These load with their trained prefix tokens, query expansion, and punctuation skiplist recovered from the saved configuration.

The NanoBEIR column reports the mean NDCG@10 (higher is better) across the 13NanoBEIR datasets, each a 50-query subsample of a BEIR dataset, as a fast proxy for English text retrieval quality. We used theMultiVectorNanoBEIREvaluatorto compute the scores for the primarily-English models. A-means the model was not evaluated on it. Note that NanoBEIR is a small benchmark, and its scores aren't a substitute for evaluating on your own data, which is always the right way to pick a model.

### Visual Document Retrieval Models

ColPali-style models embed page images as documents and text as queries.

The NanoViDoRe column reports the mean NDCG@10 (higher is better) acrossNanoViDoRe v3, a compact visual document retrieval benchmark spanning 8 subsets (computer science, energy, finance in English and French, HR, industrial, pharmaceuticals, and physics). Like with NanoBEIR, NanoViDoRe is a small benchmark which shouldn't replace evaluation on your own data.

Most of these are LoRA adapter repositories, with the adapter applied directly onto its base at load time. Some also have a-mergedsibling on the Hub (e.g.vidore/colpali-v1.3-merged) with the adapter already folded into the weights.

The three-hfentries are the transformers-native*ForRetrievalports. They load without any configuration, but use more modeling fromtransformersand less fromsentence_transformers. Generally, it's preferable to use the original models instead, as the ports score approximately the same.

## Acknowledgements

Late interaction in Sentence Transformers rests on a lot of earlier work. Thanks to Omar Khattab and Matei Zaharia forColBERT, which everything here descends from, and to the LightOn team (Antoine Chaffin, Raphael Sourty, Paulo Moura, and Amélie Chatelain) forPyLateandfast-plaid, which carried late interaction for years and shaped a good deal of the API described above.

Thanks to the ColPali team (Manuel Faysse, Hugues Sibille, Tony Wu, Bilel Omrani, Gautier Viaud, Céline Hudelot, and Pierre Colombo) forColPaliand colpali-engine, which brought late interaction to page images, and to Benjamin Clavié, Antoine Chaffin, and Griffin Adams fortoken pooling.

Thanks as well to the core MTEB team, Kenneth Enevoldsen and Roman Solomatin among many others, forMTEBand for the kind of hidden work that keeps information retrieval research running.

And thanks to everyone who trained and released the checkpoints inSupported Models. Without them this post would have had nothing to measure.

## Additional Resources

### Documentation

- Multi-Vector Encoder > Usage
- Multi-Vector Encoder > Pretrained Models
- Multi-Vector Encoder > Creating Custom Models
- Multi-Vector Encoder > Speeding up Inference
- Multi-Vector Encoder > API Reference
- Installation
- Migration Guide

### Example Scripts

- Semantic Search
- Retrieve and Rerank
- Token Pooling
- ColPali Heatmaps
- Text Similarity Maps
- NanoBEIR Evaluation

### Training

To learn how to train or finetune these models on your own data:

- Multi-Vector Encoder > Training Overview
- Multi-Vector Encoder > Loss Overview
- Multi-Vector Encoder > Training Examples
- LateOn and mLateOn training scripts: LightOn's PyLate recipes for LateOn, mLateOn, DenseOn, and mDenseOn, where the finetuning scripts show practical details like splitting a 16,384-example batch into mini-batches of 16.

### Hugging Face Hub

- Multi-vector models on the Hub
- Sentence Transformers datasets on the Hub

### Companion Blogposts

- Training and Finetuning Embedding Models with Sentence Transformers: the general training guide for text-only dense embedding models.
- Training and Finetuning Reranker Models with Sentence Transformers: Cross Encoder training, the other way to add a precise second stage.
- Training and Finetuning Sparse Embedding Models with Sentence Transformers: SPLADE and other sparse encoders, which combine well with late interaction in hybrid search.
- Multimodal Embedding & Reranker Models with Sentence Transformers: single-vector multimodal models, the dense counterpart to ColPali-style retrieval.
- Training and Finetuning Multimodal Embedding & Reranker Models with Sentence Transformers: includes a Visual Document Retrieval walkthrough with single-vector models.
- 🪆 Introduction to Matryoshka Embedding Models: shrink dense embeddings by dimension, the way token pooling shrinks multi-vector ones by count.

---

> 本文由AI自动翻译，原文链接：[Multi-Vector (Late Interaction) Embedding Models with Sentence Transformers](https://huggingface.co/blog/multi-vector-encoder)
> 
> 翻译时间：2026-08-19 03:07
