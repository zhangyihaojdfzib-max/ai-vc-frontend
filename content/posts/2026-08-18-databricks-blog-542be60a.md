---
title: 'Databricks Document Intelligence: pushing the frontier for complex document
  extraction'
title_original: 'Databricks Document Intelligence: pushing the frontier for complex
  document extraction'
date: '2026-08-18'
source: Databricks Blog
source_url: https://www.databricks.com/blog/databricks-document-intelligence-pushing-frontier-complex-document-extraction
author: ''
summary: '[翻译失败，原文如下]


  - Extracting fields across complex documents commonly fails on three use cases:
  long documents requiring cross-page reconciliation, long ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-19T03:07:59.062404'
---

[翻译失败，原文如下]

- Extracting fields across complex documents commonly fails on three use cases: long documents requiring cross-page reconciliation, long outputs like thousands of invoice line items, and complex schemas whose fields require reasoning and computation.
- Precision Mode pairs custom finetuned extraction models with an agentic harness that reasons in stages, spawns subagents to extract in parallel, and merges results into one output, staying robust as documents and schemas grow.
- Across six complex document benchmarks, Precision Mode beats the next best frontier model by seven points on accuracy.

Every enterprise has valuable data trapped in messy, unstructured documents. Today, Databricks Document Intelligence helps thousands of customers put their data to work, turning billions of pages into structured data that powers productionpipelines,agents, andapplications. Customers likePanasonic,EY-Parthenon, andIntercontinental Exchange (NYSE)use Document Intelligence on their most demanding workflows, processing millions of documents weekly.

When working with customers, we noticed several difficult extraction problems where existing large language model (LLM) or rules-based document extraction solutions fall short:

- Long documents.A lease whose page-1 renewal terms depend on a clause on page 80, or an agreement whose page-150 paragraph redefines a term from page 3. Existing solutions fail to resolve these cross-references.
- Large, nested outputs.A multi-page bill of lading with hundreds of SKUs, or an invoice with thousands of line items. Existing solutions drop or truncate fields as outputs grow.
- Complex schemas and reasoning.A risk classification that synthesizes three financial statements, or a contract value that applies listed discounts across every recorded price. Existing solutions fail to consistently apply the correct logic across documents.

Today, we’re excited to introduce Precision Mode in our document extraction API,ai_extract, setting a new bar for accuracy on the most complex enterprise documents and tasks.

![image3.png](/images/posts/73a226aa6195.png)

Precision Mode combines our custom-trained models for document extraction with an agentic harness to deliver reliable and accurate extraction on long documents, large outputs, and reasoning-heavy schemas. Across benchmarks spanning roughly 9,000 complex documents,Precision Mode achieves the state of the art quality, outperforming the latest frontier models on extract accuracy by a large margin.

## A New Approach to Complex Document Extraction

To push accuracy on the hardest extraction tasks, our research and engineering teams approached document extraction quality from two layers: customizing the model itself and building an effective agent harness around the model.

- We trained custom, efficient models for document extraction.Working from benchmarks built around difficult customer workloads, our research team trained custom models to find, reason over, and extract structured information from complex documents. Rather than relying on increasingly large general-purpose models, we optimized for the task we want to solve: accurate structured extraction.
- We built an extraction harness designed to overcome model failure modes.Even a strong model can struggle when it has to reason across hundreds of pages or generate thousands of fields at once. Our team built an agent harness, inspired by DatabricksMemEx, that semantically decomposes large extraction jobs, executes smaller tasks in parallel, preserves intermediate results, and reconciles them into one final structured output.

![Using an agent harness to manage long document extraction](/images/posts/213e53310cd7.png)

## Evaluation Methodology

### Benchmark Design and Dataset Composition

To validate Precision Mode, we designed our evaluation benchmarks around workloads that push existing approaches to their limits.

Concretely, we evaluated Precision Mode on roughly9,000 documentsspanning the three extraction challenges it was designed to solve. The evaluation includes documents up to 2,000 pages, invoices with thousands of line items, dense multi-page tables and charts, schemas with more than 300 deeply nested fields, and reasoning-heavy tasks that require cross-referencing information across a document.

The documents come from two sets of benchmarks:

- 10 internal datasets inspired by the most difficult customer workloads we’ve seen, spanning key industries including financial services, manufacturing, and healthcare.
- 5 public benchmarks:VAREX,RealDocBench,LongExtractBench, andLEDGER, plus a long-document stress test using theCaselaw Access Projectdataset.

Together, these datasets cover documents including 10-K filings, bills of lading, technical manuals, financial documents, clinical notes, government patent and funding applications, and more.

![Examples of complex documents included in our internal benchmark](/images/posts/1d533c8feaa7.gif)

### Baseline Design and Model Comparisons

A natural starting point for document extraction is asingle frontier-model call: pass in the document and schema, and ask the model to return the structured output. But on the dense and complex workloads we evaluate, that approach quickly breaks down. Long documents can exceed model context limits, causing inaccurate and incomplete results.

So we benchmarked against a stronger, more realistic baseline:chunk-and-merge. We split each document into smaller chunks, extract from each independently, and merge the results into a final output—the same pattern we see engineers use when a single model call isn't enough.

We tested the chunk-and-merge approach using leading GPT, Claude, and Gemini models with their default API settings. Then, we compared each against Precision Mode on extraction accuracy. ¹

## Benchmark Results

Across our benchmarks,Precision Mode reaches 94.7% accuracy, outperforming the strongest frontier model chunk-and-merge baseline, GPT-5.6 Sol, by seven points.

Particularly, on difficult long-document workloads, we observed frontier-models encounter numerous operational failure modes including chunk timeouts, truncated outputs, and incomplete final merges that did not conform to the requested schema. On the other hand, Precision Mode’s agentic approach is robust against these failure modes, and our custom-trained extraction models keep extractions efficient and accurate.

## Getting Started

For your most complex document extraction tasks, AI Extract Precision Mode is now available. Set the mode toprecisionwhen callingai_extract function, or turn on the precision mode toggle in theInformation Extraction UIon the Agents page:

![image10.gif](/images/posts/1c1c9e629aec.gif)

Try AI Extract Precision Mode

Footnotes:

¹ We define accuracy as the fraction of extracted objects that match the ground-truth object. Scoring depends on type. Primitives (booleans, floats, integers, enums) use direct match. Strings try direct match first, then fuzzy match, then an LLM judge. Arrays are scored by finding the closest pairing between predicted and expected items, then averaging across pairs. Objects are scored per field by type, then averaged across all fields.

---

> 本文由AI自动翻译，原文链接：[Databricks Document Intelligence: pushing the frontier for complex document extraction](https://www.databricks.com/blog/databricks-document-intelligence-pushing-frontier-complex-document-extraction)
> 
> 翻译时间：2026-08-19 03:07
