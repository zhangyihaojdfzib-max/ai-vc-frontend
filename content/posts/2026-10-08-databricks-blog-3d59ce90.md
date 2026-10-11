---
title: Biomedical Imaging's Real Bottleneck Is the Data, Not the Model
title_original: Biomedical Imaging's Real Bottleneck Is the Data, Not the Model
date: '2026-10-08'
source: Databricks Blog
source_url: https://www.databricks.com/blog/biomedical-imagings-real-bottleneck-data-not-model
author: ''
summary: '[翻译失败，原文如下]


  - What it is:A field perspective on why medical imaging AI underdelivers across
  hospitals, academia, medtech, and pharma; what a stronger...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-11T08:06:36.159212'
---

[翻译失败，原文如下]

- What it is:A field perspective on why medical imaging AI underdelivers across hospitals, academia, medtech, and pharma; what a stronger data foundation looks like across R&D.
- The challenge:Imaging is medicine's richest data but its least usable: siloed across PACS, CROs, and central labs, hard to de-identify, and rarely linked to other data modalities that power biomarkers and patient stratification. The hard part is the data, not the model.
- The takeaway:The frontier isn't a better model, it's the data foundation under it. Govern imaging in one place, make it queryable, de-identify at scale, and link it to EHR, omics, and trial data (via governed lakehouse patterns). Get the data right, and the model becomes the easy part.

## Part I — The problem

### Four sectors, one bottleneck

Hospitals and health systems generate the raw material. Radiology is the most heavily regulated corner of medical AI anywhere: of the roughly 950 AI/ML-enabled devices the FDA had authorized by mid-2024, about 723 (around 76%) were radiology tools. Almost all are narrow and human-supervised, doing triage, measurement, reconstruction, or worklist prioritization. The real difficulty in a hospital is rarely the model. It's that the data sits locked inside PACS and vendor-neutral archives built to serve images to a viewer, not to answer research questions. Pulling a cohort means extracting images from clinical systems, de-identifying them (PHI hides in DICOM headers and gets burned into the pixels), and finding the compute to use them.The model is the easy 10%.

Academic medical centers are where most of the open science happens. The field owes much of its progress to shared datasets like MIMIC-CXR (377,110 chest X-rays), The Cancer Imaging Archive, fastMRI, and the UK Biobank imaging arm, along with open tooling such as MONAI, nnU-Net, and 3D Slicer. Academia also exposes the field's credibility problem. A well-known BMJ review (Nagendran et al., 2020) of deep-learning-versus-clinician imaging studies found that of 81 studies, only a handful were prospective or tested in a real clinical setting, and code and data were unavailable in 93% and 95% of them. That reproducibility debt traces straight back to how hard imaging data is to share and re-run.

Medtech and device companies (GE HealthCare, Siemens Healthineers, Philips, Canon) build AI directly into the scanner: deep-learning reconstruction that shortens scans, dose reduction, on-device triage. Their hardest problem is generalization. An algorithm trained on one vendor's scanner, field strength, and protocol can quietly degrade on another's. Curating multi-site training data that represents the real world, then proving it to regulators through the 510(k) and PMA pathways, is both the moat and the cost.

Pharma and biotech treat imaging as a measurement instrument. Oncology trials depend on standardized response criteria like RECIST, iRECIST, and RANO, read centrally and blindly to strip out site bias, and quantitative imaging biomarkers can pick up drug response earlier than size-based measures. None of it works unless a measurement means the same thing across sites, scanners, and time, which is why RSNA's QIBA writes profiles that pin down acquisition and analysis to a stated precision. Variability is the enemy of a trial endpoint.

Four different jobs, one shared bottleneck.The pixels are everywhere, and queryable nowhere.

![Fig 1. Hospitals, academia, medtech, and pharma all converge on the same problem: the pixels are everywhere and queryable nowhere.](/images/posts/b1e4c6e83913.png)

### Why collaboration is the whole game, and why it's so hard

No single institution holds enough diverse data to build a model that generalizes. The strongest collaborative study to date makes the point. In the EXAM study (Nature Medicine, 2021), 20 institutions trained a shared model to predict COVID-19 oxygen needs from chest X-rays plus EMR data without moving any patient data between them. Only the model weights traveled, and the federated model gained, on average, 16% in AUC and 38% in generalizability over single-site models. The mechanics are less exotic than they sound: each site trains locally, a coordinator averages the model weights rather than the data (the classic federated-averaging recipe), and secure aggregation and differential privacy keep any one site's records from being reconstructed out of those weights.

That's the promise. The reality is that collaboration is genuinely difficult, for reasons that are structural rather than technical:

- Data heterogeneity.Different scanners, protocols, and labeling conventions mean that "the same" exam often isn't. Federated models degrade on this non-IID, acquisition-skewed data unless it's deliberately engineered around with techniques like batch-normalization averaging or site-aware harmonization.
- Privacy and governance.Every cross-institution study brings per-site IRB approvals, data-use agreements, and de-identification that has to be defensible.
- No common substrate.Consortia like MIDRC (co-led by the ACR, RSNA, and AAPM) exist precisely because intake, curation, de-identification, labeling, and sharing are so hard that they need a dedicated national effort.

Collaboration in imaging isn't a nice-to-have. It's the only path to models that work outside the building they were trained in, and it's gated almost entirely by data plumbing and governance.

### The complexity most people outside the field never see

When people say "medical images," they usually picture a chest X-ray. The reality is a zoo of formats and scales that makes general-purpose data tooling buckle.

"Medical images" isn't one thing — it's a zoo of formats and scales. Research archives reach petabytes, enough that de-identifying them at scale is its own published line of research.

There's a second kind of complexity that quietly breaks studies: the numbers themselves aren't comparable across sites. A standardized uptake value or a tumor volume measured on two scanners with two protocols are not the same measurement. This is why quantitative imaging leans on standards like QIBA profiles and the IBSI definitions for radiomics features, and why reproducibility, not raw accuracy, is usually the thing that fails.

A tool that handles a folder of JPEGs can't handle any of this, which is a big part of why imaging has lagged genomics and EHR data in becoming analytics-ready.

### Imaging is the sharpest edge of a bigger problem

What's easy to miss when the focus stays only on images: everything here is also true of the rest of R&D. Imaging is just where the pain shows up first, because the data is the biggest and the strangest.

Walk into a life-sciences R&D organization today and the real frontier isn't any single data type. It's multi-omics, the genomics, transcriptomics, proteomics, and metabolomics that each arrive with their own formats and silos. It's real-world and clinical-trial data, EHRs and registries and waveforms. It's medical affairs and the literature. The questions that actually move a program, which patients respond and why, what the image plus the molecular signature plus the outcome say together, live in the joins between these domains, not inside any one of them.

Every one of those data types carries the same affliction imaging does. It's rich, high dimensional, mostly unstructured, trapped in domain specific systems, hard to govern, and harder to link. A whole-slide image, a genomic variant call, and a trial endpoint are each hard enough on their own. The value comes from putting them in the same sentence.That's a data-foundation problem before it's ever an AI problem,and it's the one teams underestimate most.

[翻译失败，原文如下]

This isn't only a healthcare story. A recent Bain analysis of why AI budgets keep climbing while returns don't, found that data access and integration is the single biggest barrier to AI, cited by 41% of companies and named even more often by the leaders than the laggards. Their blunt version: most organizations still can't reliably get to their own data. Medicine just makes it harder to look away from.

## Part II — The foundation

This is where it gets concrete and more technical. For readers who aren't building the platform, the short version is simple: govern everything in one place, make the pixels queryable, de-identify at scale, and link imaging to the rest of the patient. The rest of this section is how.

### What the data foundation actually has to do

Strip away the sector specifics and the requirements come out the same. The platform has to:

1. Govern unstructured imaging files and their extracted metadata in one place, with access control, lineage, and auditability that hold up to a regulator's questions.
2. Process petabyte-scale, gigapixel, multi-dimensional data (2D X-ray, 3D CT/MRI volumes, 4D dynamic studies, gigapixel pathology slides) without falling over.
3. De-identify at scale, both in the headers and in the pixels.
4. Link imaging to EHR, genomics, waveforms, and text, so a single research question can touch all of them.
5. Make cross-institution sharing a configuration step, not a six-month negotiation.

That's the shape of a lakehouse.Here's how it maps in practice, using patterns that work on Databricks.

### A medallion architecture for Pixels

The mental model that makes imaging tractable is the same medallion pattern teams already use for tabular data, adapted for binary files.

- Bronze: raw studies first land in a restricted-access cloud object storage or Volume, where a de-identification job runs on headers and pixels before anything else; the de-identified files then form the governed bronze layer in Unity Catalog Volumes, one catalog row per file, with Auto Loader handling incremental arrival so new studies flow in continuously rather than in fragile nightly batches.
- Silver: the text-valued DICOM tags are extracted into Delta tables (binary blobs like the pixel data stay in the file), so the metadata that was trapped inside the files becomes queryable with plain SQL. This is the step that turns "a viewer can open it" into "an analyst can query it." The open-source Pixels accelerator does exactly this, cataloging files in parallel and extracting tags at scale.
- Gold: curated, analysis-ready cohorts, joined to clinical and omics tables and ready for training, BI, or a regulator-facing study.

The reason this is non-trivial is throughput. DICOM parsing libraries are single-core; the trick is to distribute them. In practice that means pandas UDFs and mapInPandas to fan parsing across a cluster, or a custom Spark data source. In work the Pixels team published, a zipdcm data source reads DICOM metadata straight out of zip archives in memory, leaving the original files compressed in place: it cataloged more than 107,000 DICOMs in about 3.5 minutes on two 8-core workers,roughly 7x faster than prior approaches. The bottleneck shifts from disk and network I/O to pure CPU parsing, which is exactly the kind of thing a cluster is good at.

![Fig 2. Pixels Architecture: an open source Databricks Solution Accelerator](/images/posts/0108fce80d3e.png)

### Governance that survives an audit

Imaging is the ultimate unstructured-data governance problem, and it's the requirement most platforms fail quietly. Unity Catalog Volumes govern the raw files in S3, ADLS, or GCS under a three-level namespace, while the extracted metadata lands in Delta. Both sit under one access-control and lineage model that reaches all the way to the models trained on the data, which is what makes it possible to answer "who touched this cohort, and what was built from it" months later. Row and column-level security and attribute-based rules let an organization expose de-identified metadata broadly while keeping the underlying pixels locked down.

De-identification is where this gets real. Header PHI is handled with format-preserving encryption so the same patient identifier always maps to the same pseudonym. That detail matters more than it looks: it means a patient's CT can still be linked to their pathology and their labs across datasets without ever exposing the real identifier. The DICOM standard's confidentiality profiles define what to strip and what to keep. The harder problem is PHI burned into the pixels, the patient name baked into an ultrasound or a scanned form. Classic tools like Presidio handle free text well but miss images. Removing that burned-in PHI is an active research problem: recent work shows vision-language models now outperform OCR-only pipelines at detecting and obscuring it (Lee et al., Radiology 2025), and production de-identification methods that pair DICOM metadata sanitization with targeted OCR on burned-in text have been validated across hundreds of thousands of images spanning ten modalities (Macdonald et al., 2024). For pixels, the Pixels teampublished a vision-language-model pipelinethat combines OCR with a VLM and runs distributed with pandas UDFs. On a balanced sample from the MIDI-B benchmark, GPT-4o and Claude 3.7 Sonnet reached roughly 100% recall and precision, the open Llama 4 Maverick hit 100% recall at a fraction of the cost, and Spark cut de-identification of 1,000 framesfrom 105 minutes to 6.The team is also exploring a leaner, VLM-only approach to push this further.

### Training and serving, on top of the same governed data

Once the pixels are queryable and governed, the ML layer stops being the hard part. Segmentation and classification models register in the same catalog as MLflow models, with their lineage back to the exact cohort they were trained on. For imaging specifically,NVIDIA MONAI and VISTA-3D(a foundation segmentation model covering 127 anatomical classes) plug in for auto-segmentation and fine-tuning, with an OHIF viewer embedded in a Databricks App so a radiologist or pathologist can review, correct, and relabel under the platform's security model.

MONAI Label's active-learning loop means each correction improves the next batch, which is how teams get out of the trap of needing a fully annotated dataset before they can start. Inference runs either as real-time GPU model serving (scale-to-zero so a rarely used model isn't burning a GPU) or as distributed batch inference across millions of studies. And because newer Pixels work ships a DICOMweb service (QIDO-RS, WADO-RS, STOW-RS), the lakehouse can sit directly in a clinical or PACS/VNA workflow rather than off to the side.

### Proving it's safe: validation, drift, and the regulatory path

Training a model is the start, not the finish. One that looks great on a single site's scanner can quietly degrade on another's, so the real work is external validation across sites, vendors, and protocols, then monitoring for drift as scanners get upgraded and protocols change in production. MLflow handles the evaluation and tracking; the harder discipline is treating every model as a versioned asset with its cohort, metrics, and approvals attached. For anything heading toward the clinic, regulators have started to meet adaptive AI halfway. The FDA's Predetermined Change Control Plan (PCCP) lets teams pre-specify how a model can be retrained and updated without a fresh submission each time, and Good Machine Learning Practice (GMLP) sets expectations for data, validation, and monitoring. Building those guardrails into the data foundation, instead of bolting them on later, is what separates a demo from something a hospital will deploy.

### Collaboration without moving the data

There are two complementary ways to get the cross-institution diversity that EXAM showed is necessary, and they solve different problems.

[翻译失败，原文如下]

Federated learning keeps the data physically in place and moves only model weights, with federated averaging to combine them and secure aggregation plus differential privacy to keep any site's data from leaking back out. It's the right tool when data legally cannot move at all.

The lakehouse adds a second option that's often simpler in practice: Delta Sharing and Clean Rooms let institutions share governed tables and files (or run joint analysis on de-identified cohorts) without copying anything, using credential vending rather than data export. For a lot of multi-site research, "share a governed view of the cohort" is a far lighter lift than standing up a federated training ring, and the two can be mixed.

### Making imaging multimodal

This is the requirement that turns imaging from a standalone modality into part of the patient. Because the metadata is just Delta, imaging can be joined to FHIR and HL7 feeds from the EHR, to genomic variant tables, to waveforms, and to clinical text, with patient identity resolved through the pseudonymization layer. Common data models like OMOP give the observational data a shared schema to land in. On top of that, Vector Search indexes embeddings for semantic retrieval (Pixels even ships a function that maps a plain-English term to the right DICOM tag), and natural-language tools like Genie let a scientist build a cohort by asking for it instead of writing SQL.

Physiological waveforms are their own kind of data. An ECG, an arterial-pressure trace, or an IVUS or OCT pullback is a high-frequency time series sampled hundreds or thousands of times a second, usually stored in formats like WFDB rather than DICOM. The technical catch is alignment: a pullback frame or an ECG beat only means something when it's time-synced to the image and the clinical event it belongs to. Getting that right, resampling, reconciling timestamps, and storing the series next to the study, is exactly the kind of join that pays off when the question is why a patient responded, not just whether.

Embeddings also unlock something more powerful than search. Image-text models trained on paired scans and reports (the BiomedCLIP and CheXzero line of work) put images and language in a shared vector space, so systems can retrieve similar cases, flag findings without an explicit label, or ground a generative model in a patient's actual images and prior reports rather than its training data alone. That last pattern, retrieval-augmented generation over images plus reports, is what makes report drafting and case summarization trustworthy enough to show a clinician: the model can point to what it saw. It only works when the images, the reports, and their embeddings sit together under one governed roof, which is this whole piece in miniature.

This is also what the new wave of foundation models needs. Prov-GigaPath (Nature, 2024), pretrained with self-supervision on 1.3 billion tiles from 171,189 whole-slide images, only works with data that's large, diverse, governed, and multimodal. The silos can't feed it. A lakehouse can.

### The payoff: a co-scientist for the researcher, a companion for the clinician

The tangible version of all this isn't an autonomous system that replaces anyone. It's a companion, an AI co-scientist for the researcher and a co-pilot for the clinician, grounded in the institution's own governed data rather than the open internet.

For a researcher, a co-scientist agent turns a question into work. Ask it to "find treatment-naive NSCLC patients with a baseline CT, matched pathology, and EGFR status, then summarize how the lesions changed on follow-up," and it plans the steps, queries the imaging and clinical tables through a Genie space, retrieves similar cases with Vector Search, calls a segmentation endpoint to measure the lesions, and grounds its summary in the relevant literature, with every claim traceable to the data it used.

The emerging class of "AI co-scientist" systems aims exactly here: helping generate and triage hypotheses, not just answer lookups. What separates a toy from a trusted collaborator is whether it stands on governed, multimodal data.

For a clinician, the same machinery becomes a companion that does the legwork a radiologist or oncologist would otherwise do by hand: pull the patient's priors, measure and compare lesions, surface the guideline criteria that apply, and draft the report for review. It never signs off; the human does. That isn't a limitation, it's the design. Nearly all cleared imaging AI today is human-supervised, and a companion that shows its work and cites its sources is what makes that supervision real rather than a rubber stamp.

![Fig 3. One governed foundation for all of R&D: imaging, multi-omics, clinical and real-world data, waveforms, and literature and in the same lakehouse, where the value living in the joins between domains finally becomes reachable](/images/posts/153dccfa0554.png)

What makes either one safe is the foundation underneath. Every tool the agent calls is a governed object, a Unity Catalog function, a model-serving endpoint, a Vector Search index, a Genie space, so the same access controls, lineage, and on-behalf-of identity that protect the pixels also bound what the agent can see and do. Compose specialists, a radiology agent, a genomics agent, a medical-affairs agent, under a supervisor, and the agent team mirrors the multimodal joins the data foundation already makes possible. The companion is the easy part, once the foundation is right.

### Beyond imaging: the same foundation carries the rest of R&D

The reason this matters past radiology is that the exact same architecture absorbs the rest of the R&D data estate. Multi-omics (genomics, transcriptomics, proteomics, metabolomics) lands in the same Unity Catalog alongside imaging and clinical data. It brings its own heavy formats and standards, VCF for variants, BAM and CRAM for aligned sequencing reads, the GA4GH specifications that keep them interoperable, and engines like Glow and Hail for population-scale analysis, but the lakehouse pattern is identical: govern the files, extract the queryable layer, join it to everything else.

This is also where the NVIDIA stack like BioNeMo and NIMs plugs in for sequence and structure models. Real-world and clinical-trial data, registries, and waveforms join to imaging cohorts without an export. Medical affairs and the literature become queryable text under the same governance and the same AI/BI and Genie surface. The programs that move forward, the ones answering which patients respond and why, live in the joins between these domains, and a lakehouse is the rare architecture that holds a gigapixel slide, a variant call, and a trial endpoint under one governance model and lets them be queried together.

## The bottom line

![image2.png](/images/posts/3e09e99060b9.png)

Teams building AI and GenAI on top of this kind of data keep running into the same lesson. A model can demo well in a week. What takes months after is getting the data clean, linked, de-identified, and governed enough to trust it in front of a scientist or a regulator. The data problem isn't the unglamorous part of the project. It is the project.

Seen across imaging, omics, clinical, and medical-affairs data inside the same organizations, the conclusion is simple. The frontier in medical imaging isn't a better architecture. It's a better foundation. The algorithms exist. The data exists, somewhere. What's been missing is a way to make imaging governed, queryable, linkable, and shareable, and joined to everything else a research question touches, without giving up the privacy and rigor medicine demands.

The teams that win in R&D won't be the ones chasing the model first. They'll be the ones who get the data right first and let the AI follow. Solve that, and the model becomes the easy part, the way it always was.

## Where to start

The fastest way to test this is on your own data.

[翻译失败，原文如下]

- Start with the open-source Pixels accelerator(databricks-industry-solutions/pixels) to turn a folder of DICOM into governed, queryable Delta tables and see the medallion pattern in action.
- Run it on Databricks.Spin up a workspace, point Unity Catalog Volumes at a public dataset like TCIA or MIMIC-CXR, and stand up ingestion, de-identification, and an OHIF viewer end to end before bringing in protected data.
- Go deeper on the engineeringbehind the numbers here: the 7x ingestion, VLM de-identification, and MONAI/VISTA-3D write-ups linked above.
- Scale from one cohort to the estate.Once a single study type is ingested, de-identified, and joined to one clinical table, the same pattern extends to multi-omics, real-world data, and the agentic layer on top.

If your team is building toward medical imaging or multimodal R&D on Databricks, the authors would like to hear how you're approaching it. Reach out or drop a comment, and when you're ready to move from a pilot to production, the Databricks Healthcare and Life Sciences team can help you get there.

---

> 本文由AI自动翻译，原文链接：[Biomedical Imaging's Real Bottleneck Is the Data, Not the Model](https://www.databricks.com/blog/biomedical-imagings-real-bottleneck-data-not-model)
> 
> 翻译时间：2026-10-11 08:06
