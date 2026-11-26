---
title: 'Building on Nemotron 3.5 Parse: Open Data, Fine-Tuning, and Faster Inference'
title_original: 'Building on Nemotron 3.5 Parse: Open Data, Fine-Tuning, and Faster
  Inference'
date: '2026-11-26'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/building-on-nemotron-35-parse-open-data-fine-tunin
author: ''
summary: '[翻译失败，原文如下]


  # Building on Nemotron 3.5 Parse: Open Data, Fine-Tuning, and Faster Inference


  We recently releasedNVIDIA Nemotron 3.5 Parse, a compact ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-26T10:39:24.718678'
---

[翻译失败，原文如下]

# Building on Nemotron 3.5 Parse: Open Data, Fine-Tuning, and Faster Inference

We recently releasedNVIDIA Nemotron 3.5 Parse, a compact document model that turns page images into structured data for retrieval-augmented generation (RAG) and agents.

Now we’re building on that release withsynthetic training datasets, a fine-tuning recipe, and a DFlash2 speculator for faster inference. We’re also sharing how we trained Parse 3.5: first teaching document understanding through supervised fine-tuning, then using reinforcement learning to improve accuracy, consistency, and reliable completion.

## What Parse 3.5 produces

Parse extracts content from pages of documents into reading order, assigns content classes such as headings, paragraphs, tables, and charts, and returns bounding boxes that locate the content. Tables and charts become structured records that can power downstream document processing applications.

![An operations brief with predicted regions on the left and its structured extraction on the right.](/images/posts/377486bc12a4.png)

Figure 1. Actual model output from a synthetic operations brief, showing the connection between the page and its structured representation.

This latest version of Parse significantly extends its ability to read charts and tables, especially in more difficult and ambiguous cases. For example, bar charts or other plots that do not have any marked numeric values. The model is able to infer values by looking at the axes and height of the bar to derive these. Tables can be especially tricky because the structure is so meaningful, a shifted row or column can totally change the interpretation and meaning. These advancements have been largely powered by synthetic data generation, rendering variations of charts and tables with known ground truth and then training our model to reverse this process.

We are open-sourcingthree datasets used in the Parse 3.5 training:

- Synthetic Charts V1 — 9.98M examples:rendered charts and structured annotations for learning categories, series, and numerical values.
- Synthetic Tables V1 — 1M examples:rendered HTML tables with targets that preserve rows, columns, headers, and cell relationships.
- OCR Synthetic Multilingual v2 — 7.9M examples:synthetic document pages with Parse-format targets across varied fonts and layouts, for multilingual OCR and structured page reading.

Synthetic Charts V1 — 9.98M examples:rendered charts and structured annotations for learning categories, series, and numerical values.

Synthetic Tables V1 — 1M examples:rendered HTML tables with targets that preserve rows, columns, headers, and cell relationships.

OCR Synthetic Multilingual v2 — 7.9M examples:synthetic document pages with Parse-format targets across varied fonts and layouts, for multilingual OCR and structured page reading.

Each release includes images, annotations, generation documentation, and the training format. Use these pairs to fine-tune document models or create new variations for a target document type or language.

![A bar chart without printed bar values, alongside the released model’s extracted values of 18, 27, 39, and 54.](/images/posts/8a933e1d2ac6.png)

Figure 2. Parse recovers 18, 27, 39, and 54 from the chart geometry

## SFT teaches the capability; RLVR improves consistency

We trained Parse 3.5 with two phases of training.Supervised fine-tuning (SFT)spanning text, layout, tables, charts, and multilingual documents. Learning to predict structured targets established the general capability of reading a page and representing its contents.

We then continued withreinforcement learning with verifiable rewards (RLVR), usingGroup Relative Policy Optimization (GRPO). Rewards check the quality of sampled extractions. For example, a chart extraction can earn a better reward for recovering the correct series and values, producing a usable structure, and finishing without repeatedly generating the same content.

A difficult page can have several valid representations. These checks give the model flexibility to find a correct answer without prescribing one exact token sequence, while discouraging looping and unfinished output.

![A matched training comparison showing extraction gains after GRPO and fewer repetition flags and token-cap hits.](/images/posts/a8bf8de09fc9.png)

Figure 3. A controlled comparison of SFT and GRPO with matched evaluation settings. These are development checkpoints, separate from the final released model. Loop counts use a repetition check.Methods.

The matched comparison shows the benefit: loop-flagged outputs fall from126 to 29 pages—about 77% fewer—and outputs reaching the 9,000-token limit fall from185 to 35. Overall score improves from66.24 to 71.38, including+5.18 points in tablesand+4.15 in charts.

## Faster inference through architecture and DFlash2

A parser must generate substantial text and structure for every page. Alongside the training work, we optimized how Parse 3.5 processes images and decodes those outputs.

NaViT preprocessingadapts the input shape to the page. A visual adapter compresses the image sequence, and the text decoder consumes it as a prefix, replacing encoder–decoder cross-attention.Grouped-query attention with eight key/value heads (GQA-8)reduces the decoder’s attention-cache memory.

The built-inmulti-token prediction (MTP)head supplies one-token lookahead. OurDFlash2 speculatorgoes further: a small draft model proposesup to 32 tokens ahead, and Parse verifies the proposals together. In the measured 32-token configuration, it averages about14 accepted draft tokens, or roughly15 output tokens of progress per verification stepincluding the target token.

![Throughput curves comparing Parse 2.0 with Parse 3.5 base, MTP, and DFlash2.](/images/posts/3d9b95769feb.png)

Figure 4. Native single-pass throughput on one H200, BF16, using the same 2,078 pages. Parse 2.0 uses one trial per point; Parse 3.5 shows three-trial medians. Arrows show the gain from Parse 3.5 base to DFlash2.Measurement details.

In the native single-pass benchmark on one H200 in BF16, DFlash2 increased throughput7.62×at concurrency 1 and1.52×at concurrency 512, compared with Parse 3.5 with speculative decoding disabled. At 512, Parse 3.5 reaches13.48 pages/swithout speculation and20.44 pages/swith DFlash2, versus2.98for Parse 2.0. Those are4.53×and6.86×the Parse 2.0 throughput, respectively.

Fast parsing gives us room to revisit difficult regions. Start with a full-page prediction, then add focused reprocessing where the document needs it:

1. Single pass -Parse the full page once for text, layout, tables, and charts.
2. Double pass - use for dense tables and small chart details.Crop the table and chart regions found by the parser, re-parse them at higher detail, and merge the refinements into the page output.
3. Triple pass -Instead of only using the models full page parsing bounding boxes, use a second pass of the model in detection mode in order to get verification that all boxes have been accurately found and text has not been missed and re-extract any found charts or tables in a third pass

Single pass -Parse the full page once for text, layout, tables, and charts.

Double pass - use for dense tables and small chart details.Crop the table and chart regions found by the parser, re-parse them at higher detail, and merge the refinements into the page output.

Triple pass -Instead of only using the models full page parsing bounding boxes, use a second pass of the model in detection mode in order to get verification that all boxes have been accurately found and text has not been missed and re-extract any found charts or tables in a third pass

![Single-pass page parsing, double-pass crop refinement, and triple-pass refinement with an independent region detector.](/images/posts/3f6c3d7d9372.png)

Figure 5. Additional stages focus computation on difficult regions. Multiple crops can require multiple requests.

[翻译失败，原文如下]

In the published reference evaluation, double and triple pass add2.18 and 2.46 ParseBench pointsover single pass. The additional work lets applications trade some throughput for better extraction in difficult regions.Reference results and serving measurements.

## Apply the same SFT/RLVR approach to your documents

We are sharing aParse fine-tuning recipethat takes developers through paired data generation,NeMo Automodel SFT, andNeMo RL GRPO, using vLLM to generate candidate answers.

The worked example uses a synthetic dental form with anodontogram: a chart showing teeth, planned procedures, and affected tooth surfaces. Before adaptation, Parse reads the printed tooth numbers but misses the intended procedure table. SFT teaches it to associate each marked tooth with a procedure and its placement on the tooth.

![A synthetic dental page, the base model’s tooth-number transcription, and the intended tooth/procedure/surface table.](/images/posts/7612b48310c8.png)

Figure 6. A recorded recipe example: after SFT, all six chart rows match the target.Full image and native training label.

RLVR then reinforces accuracy and consistent completion. In the dental reference run, the estimated first-attempt success rate (sampled pass@1) rose from 0.00% for the base model to 95.85% after SFT and 96.58% after RLVR.

![Dental sampled pass@1: 95.85% after SFT and 96.58% after RLVR, with the y-axis shown from 90% to 100%](/images/posts/db7563f43b38.png)

Figure 7. Matched evaluation on 256 held-out forms from the same synthetic generator, with eight samples per page. Success requires natural completion, exact chart content, and error-free normalized page text.Evaluation protocol.

To adapt the recipe, supply your own image/label pairs and a verifier: checks that determine whether an extraction is correct. The includeddocument reward componentscover text fidelity, bounding boxes, tables, chart facts, and completion. Combine the components relevant to your task, add schema checks, and use completion and repetition checks to discourage looping or unfinished output.

We are excited that the community has extended and improved Parse forThai,Persian/Farsi, andArabicalready and we hope that these additional datasets and fine-tuning recipes will help encourage these efforts and future models.

We thank Denis Ovchinnikov for his work on vLLM integration and independent performance validation, Oliver Holworthy for improving the fine-tuning recipe's runtime setup and reproducibility, and Bo Liu for technical review.

---

> 本文由AI自动翻译，原文链接：[Building on Nemotron 3.5 Parse: Open Data, Fine-Tuning, and Faster Inference](https://huggingface.co/blog/nvidia/building-on-nemotron-35-parse-open-data-fine-tunin)
> 
> 翻译时间：2026-11-26 10:39
