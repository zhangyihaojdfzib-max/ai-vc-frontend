---
title: Enhancing Agent Retrieval with Structured Chart Extraction
title_original: Enhancing Agent Retrieval with Structured Chart Extraction
date: '2026-08-27'
source: Databricks Blog
source_url: https://www.databricks.com/blog/enhancing-agent-retrieval-structured-chart-extraction
author: ''
summary: '[翻译失败，原文如下]


  ## The Motivation


  More and more enterprises are now asking agents to work with their proprietary documents
  and answer questions about th...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-30T07:44:59.780048'
---

[翻译失败，原文如下]

## The Motivation

More and more enterprises are now asking agents to work with their proprietary documents and answer questions about their contents. However, much of the important information lives inside figures and charts. Many customers have been finding that agents struggle to answer questions that require reading and counting values in charts. For agents to work reliably in diverse enterprise settings, we need to make charts more interpretable.

How can we make a chart easier for agents to understand? We ran a simple, quick test: we asked different agents,“How many local maxima are on this chart?”

Below is a comparison of a frontier agent and Databricks Genie at answering this question. The frontier agent was passed just the image, spent 50 seconds reasoning, but still got an incorrect answer of 17. Meanwhile, Databricks Genie used a structured extraction of the chart through ai_parse_document, and got the correct answer 18.

![image12.png](/images/posts/918a1ba133a4.png)

![image4.png](/images/posts/5c67fc326e50.png)

![image10.png](/images/posts/abf21dc18870.png)

We noticed these shortcomings in ourOfficeQA Pro benchmark, where models performed worse on chart-based and multimodal questions than on questions that did not require chart understanding. We see the same gaps in customers’ information retrieval systems, particularly in financial services. A text-based retrieval system can only search the text space. A common solution is to generate a caption to describe what a chart is about; however, that may miss the data needed for fine-grained questions on the numbers inside the chart. As a result, the system may retrieve the wrong page, or retrieve the right page without having enough information to answer the question.

In this post, we show that structured extraction from charts improves both retrieval and answer quality on chart-based questions. We evaluate our approach on two datasets: a chart-heavy subset of ViDoRe V3, a benchmark for retrieval and question answering over visually rich documents, and a synthetic chart-focused dataset we call Chart-RAG. Our approach performs competitively with large single-vector and multi-vector multimodal embedding models.

![Figure 1: Answer accuracy for description-only parsing, enriched ai_parse_document with the top three retrieved images, and the strongest multimodal embedding baseline when the top five retrieved pages are used for answering. Results are averaged across three runs.](/images/posts/4f4d4848e0f4.png)

We build a chart-aware retrieval pipeline end-to-end withDatabricks’s AI functions, a set of composable functions that are optimized with state-of-the-art research techniques (seeFigure 2). We usedai_parse_documentto extract document content, including charts represented as structured JSON, andai_prep_searchto transform the content into retrieval-ready chunks, indexed with a lightweight 300M-parameter text embedding model. We created an index from the chunks usingai_searchand connected the index toGeniefor retrieval and answering.

![Figure 2: Chart extraction and retrieval pipeline implemented using Databricks AI functions.](/images/posts/569f0cbde67b.png)

## Evaluation Methodology

We compared two indexes, created using a 300-million parameter BGE text embedding model, built from the same source PDFs, differing only in chart figure representation:

- Description-only (baseline):figures represented by captions only
- JSON-enriched:chart figures represented by captions and structured chart JSON, embedded inline in the figure's chunk.

An example chart extraction:

![Grouped bar chart comparing five economic forecast scenarios for GDP growth and headline inflation in 2026 and 2027.](/images/posts/c084a62da961.png)

We evaluated 310 chart and infographic-heavy questions from theViDoRe V3 benchmark.The benchmark evaluates retrieval and answering across seven domains: employment, energy, pharmaceuticals, physics, finance, computer science, and industrial documents. For each experiment, we parsed and chunked the entire 16K-page English corpus and generated answers to every query, searching over the full index.

Although chart-focused questions were selected, many could still be answered using the surrounding text. To isolate the impact of the chart content, we created a second benchmark that focused only on chart-based questions created from three complex, chart-heavy reports (BIS Quarterly Review,IMF World Economic Outlook,J.P. Morgan Long-Term Capital Market Assumptions). We wrote 114 visually grounded questions from these 3 documents totaling 378 pages to build thesynthetic Chart-RAGdataset.

Grading:We scored each answer as Correct / Partially Correct / Incorrect using an LLM judge (gemini-3-flash) against its gold answer.

Retrieval:We report Hit Rate@10 and nDCG@10. Hit Rate@10 checks whether at least one gold page appears in the top 10 retrieved results. The questions from the ViDoRe benchmark may have multiple gold pages, each with a relevance score of 1 or 2. For Hit Rate@10, we convert graded relevance to binary relevance by allowing pages with either score to count as a hit. For nDCG@10, we keep the original graded relevance. In the Chart-RAG dataset, each query has one gold page.

To achieve stable measurement, we ran each configuration three times and report the results with confidence intervals.

## Structured Chart Data Improves Retrieval and Answering

![Figure 3: Answer correctness, Hit@10, and nDCG@10 for description-only and Chart-JSON-enriched retrieval across ViDoRe V3 subset and synthetic Chart-RAG datasets. Results are averaged across three runs.](/images/posts/1e4e277f1813.png)

Structured Chart JSON improvesboth answer quality and retrievalacross both datasets. The question-level analysis below shows when corrected answers coincide with better retrieval.

![Figure 4: Adding chart JSON corrected answers that were previously incorrect. Amongst those corrected answers, the figure shows how often JSON also improved retrieval (Hit@10) or ranking (nDCG@10). Results are averaged across the three runs.](/images/posts/0c89e49a5a34.png)

The following example from theChart-RAGdataset demonstrates how JSON representations improve retrieval and answer quality:

Roughly what peak level (% pts) did the Oil VIX reach toward Q1 2026?

Refers to the following chart:

![image2.png](/images/posts/6dd3dfa684df.png)

This retrieval gain may not be limited to questionsabouta chart. Extracted chart values and labels can make the page itself easier to retrieve, even when the answer doesn’t appear directly on the chart.

## Images Further Improve Answer Quality

Some questions depend on how a figure looks instead of just its values. To measure the benefit of restoring visual context, we gave the agent images corresponding to the top three retrieved text chunks with the JSON at answer time.

![Figure 5: Correct answer rates with chart JSON alone and with the top three retrieved images added at answer time. Results are averaged across three runs.](/images/posts/67b1e2593ef8.png)

Here, retrieval is unchanged. Images add 4 percentage points on the Chart-RAG dataset, and 2.6 percentage points on the ViDoRe V3 subset.

## JSON Representations are Competitive with Multimodal Embeddings

[翻译失败，原文如下]

One question is how our approach, which uses a lightweight 300-million-parameter text embedding model, compares with multimodal embedding models. We benchmarked against four alternatives: ColQwen2.5-3B, a large multi-vector multimodal embedding model that uses late-interaction scoring, Qwen3-VL-Embedding-2B, a large single-vector multimodal embedding model, and the lighter single-vector models Jina CLIP v2 (0.9B parameters) and CLIP ViT-L/14 (428M parameters). Each multimodal model embedded every page. At query time, we ranked pages using MaxSim for ColQwen2.5-3B and cosine similarity for the single-vector models, searched against the entire corpus, and passed the five highest-scoring pages to the answering VLM. We report answer correctness using five retrieved pages for two reasons. First, it provides a balanced midpoint between the best-performing depths for the ViDoRe subset and Chart-RAG datasets. Second, five pages approximate the average input context used in our approach, enabling a fair comparison. We still report nDCG@10 as the standard retrieval metric.

### ViDoRe V3:

![image11.png](/images/posts/bda0826226ce.png)

### Chart-RAG:

![image13.png](/images/posts/1fbffc58ddf6.png)

For the strongest models, retrieval on the Chart-RAG dataset is close to saturated due to the small corpus size of 378 pages. The more interesting comparison here, therefore, is answer quality.

On ViDoRe V3, chart-JSON with the top three images reaches 75.9% correctness. On Chart-RAG, the same setup reaches 75.1%. Both cases exceed the four multimodal embedding baselines while passing only three images to the model. This performance comes from a roughly 10x smaller and simpler alternative to ColQwen2.5-3B’s multi-vector, late-interaction architecture. Structured chart preprocessing can therefore provide competitive answer quality with a smaller image budget and lower indexing and retrieval overhead.

## Conclusion

Charts are a dominant form of information in enterprise documents. Making chart information easy to find and clearly interpretable is critical for retrieval agents’ accuracy. Structured chart JSON bridges the gap in the classic RAG system by adding precise values to the retrieval index and for agents to reason with. We show that structured chart JSON improves both retrieval quality and agent answer accuracy. Future work could further explore how different structured extraction representation formats impact the retrieval and answer accuracy.

The chart-JSON enrichment forai_parse_documentwill be available soon, so any document parsed will automatically include its chart values as structured text, without any changes to the function’s interface. For retrieval, we recommend pairing it withai_prep_search. This capability will also powerGenie Oneto improve answers to chart-related questions over PDFs for databricks customers.

Authors: Amrutha Srivatsav, Ivan Zhou, Jasmine Collins, Michael Bendersky, Adyasha Maharana, Erich Elsen, Xing Chen, Matei Zaharia

Try soon in ai_parse_document with ai_prep_search to build chart-aware retrieval and answering pipelines

---

> 本文由AI自动翻译，原文链接：[Enhancing Agent Retrieval with Structured Chart Extraction](https://www.databricks.com/blog/enhancing-agent-retrieval-structured-chart-extraction)
> 
> 翻译时间：2026-08-30 07:44
