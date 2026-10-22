---
title: Deploy RFD4-Proteina on Databricks
title_original: Deploy RFD4-Proteina on Databricks
date: '2026-10-21'
source: Databricks Blog
source_url: https://www.databricks.com/blog/deploy-rfd4-proteina-model-databricks
author: ''
summary: '[翻译失败，原文如下]


  - Start with Genesis Workbench, the open, modular life sciences blueprint underpinning
  the RFD4-Proteina integration on Databricks.

  - Use...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-22T06:56:02.844129'
---

[翻译失败，原文如下]

- Start with Genesis Workbench, the open, modular life sciences blueprint underpinning the RFD4-Proteina integration on Databricks.
- Use Genie Code and domain-specific agent skills to develop and extend workflows,from preparing model inputs to analyzing generated candidates.
- Execute GPU-intensive workloads with AI Runtime while connecting research data, experiment tracking, and governance on one platform.

BringRFD4-Proteinato your research data with AI-assisted development and serverless NVIDIA GPU compute.

- Get started with day-zero model support through Genesis Workbench, an open example blueprint for life sciences workflows.
- Build and adapt pipelines with Genie Code,NVIDIA BioNeMo Agent Toolkit skills, and coding-agent assistance.
- Use Databricks’ generally available AI Runtime to execute supported GPU workloads alongside enterprise data, experiment tracking, and governance.

RFD4-Proteina, an NVIDIABioNeMoopen model co-developed with the University of Washington Institute for Protein Design, helps scientists turn ideas for useful proteins into designs they can test. NVIDIA and Databricks are bringing the model intoGenesis Workbenchon AI Runtime, giving developers a path to connect protein-design workflows with their research data.

Databricks AI Runtime (AIR)provides serverless NVIDIA GPU compute for supported workloads. The planned integration connects model execution with research data and repeatable workflows on Databricks, reducing the infrastructure overhead required to evaluate and adapt a new model.

Putting a model to work requires more than downloading weights. Developers need to prepare inputs, connect scientific tools, configure execution, and track results—all while protecting proprietary data. Databricks brings these steps into a shared environment, reducing the need to assemble and maintain a separate research stack.

## Bring models to your data

RFD4-Proteina builds on the approach used in Proteina-Complexa, NVIDIA's generative model for designing protein binders that co-generates amino-acid sequences and all-atom structures in a single pass. RFD4-Proteina extends that joint generation approach with optional reward-guided search, letting researchers steer candidate design toward properties like thermostability or binding affinity.  The planned integration expands on Genesis Workbench’s existing Proteina-Complexa workflows patterns,utilizing scoring models withreward functions specific to the problem at hand. Genesis Workbench has two built-in workflows using RFD4-Proteina for your reference: Antibody Design and Vaccine Design.

![rfd4-proteina-databricks](/images/posts/ec816f632c82.gif)

Pictured: Antibody Design in Genesis Workbench with NVIDIA RFD4-Proteina

Genesis Workbenchoffers an easy way to get started: its open, modular blueprint illustrates how to connect biological models with input preparation, candidate evaluation, and downstream analysis on Databricks. Developers can reuse individual components or adapt the implementation to their own scientific methods.

Teams can store model weights in Unity Catalog volumes as governed MLflow models and reuse them across experiments. Teams can register fine-tuned models in Unity Catalog through MLflow, connecting model versions with configurations and artifacts. Access controls and network configuration should reflect where the model, scoring tools, and coding agents execute.

Using RFD4-Proteina through Genesis Workbench gives Databricks users the broader ability to connect research across disciplines: genomics analysis can inform a target, single-cell data can provide biological context, and protein-design or small-molecule workflows can support subsequent investigation. Genesis Workbench provides examples of these capabilities within a shared environment.

## Build with scientific agent skills

Databricks Genie Code helps developers build, debug, and adapt data and ML workflows using natural language. NVIDIA BioNeMo Agent Toolkit skills add specialized instructions, scripts, and references for biological models and scientific tools, including structure prediction, protein design, molecular docking, and genomics analysis.

These skills can help a coding agent prepare inputs, invoke supported tools, inspect outputs, and assemble multi-step workflows. Developers can combine that guidance with their own data conventions, evaluation criteria, and experiment-tracking requirements.

Genesis Workbench also provides skills for Claude-based coding agents, offering another entry point: helping developers understand the blueprint, scaffold integrations for new models such asRFD4-Proteina, and tailor those integrations to a specific use case. This can accelerate the first implementation; dependency checks, testing, and scientific review remain part of the process.

A life science researcher could leverage prebuilt RFD4-Proteina workflows directly from Genesis Workbench or use Genie Code to create a Databricks Notebook for an ad-hoc experiment with a simple english prompt like:

“Design a nanobody (VHH) against PD-L1 using RFD4-Proteina framework conditioning: keep a real humanized framework (h-NbBCII10) fixed and design only the CDR loops onto the PD-1-blocking epitope. Run 8 iterations × 8 samples with ProteinMPNN on the CDRs and Boltz co-folding for binding; weight the reward toward binding (ipTM), fold confidence (pLDDT), developability (solubility, thermostability), and low anti-drug-antibody risk (MHC-II). Return the top designs with the reward trajectory and top-K complex PDBs."

Genie Code assists with implementation, while developers and researchers retain control by reviewing the code, selecting appropriate tools, and interpreting results.

## Run on managed NVIDIA GPUs

AIR simplifies access to NVIDIA acceleration without requiring teams to provision and maintain separate GPU clusters. Developers can connect a notebook to Serverless GPU compute, select an NVIDIA H100 accelerator and a supported environment, and run their workload. The documented setup includes selecting the accelerator and base environment before applying the configuration.

This reduces the work of configuring GPU infrastructure and maintaining a base software environment,though teams still need to validate model-specific libraries and dependencies.

For supported biological foundation models, teams can also adaptBioNeMo Recipesto train or fine-tune on proprietary data using AIR’s serverless GPUs. BioNeMo Recipes provide reference implementations for accelerated training with familiar frameworks such as PyTorch and Hugging Face.

Lakeflow orchestration, MLflow experiment tracking, and Unity Catalog governance connect execution to repeatable workflows and enterprise controls. Scientists can focus more on biology, while developers and platform teams spend less time managing infrastructure.

## From experimentation to deployment

An example practical model lifecycle on Databricks can include:

1. Store model weights in a governed Unity Catalog volume for reuse.
2. Generate candidate molecules on AIR, or train and fine-tune where the model and recipe support it.
3. Track parameters, metrics, and artifacts with MLflow and register deployable models in Unity Catalog.
4. Deploy compatible models to GPU Model Serving endpoints, or orchestrate batch execution when that better fits the workload.
5. Connect outputs to research workflows through Genesis Workbench examples or your own pipelines.

For supported custom-model endpoints, scale-to-zero can reduce provisioned capacity during inactivity. Cold starts add latency, and GPU capacity is not guaranteed when an endpoint scales back up. Databricks recommends disabling scale-to-zero for workloads requiring consistent availability or response times.

Teams can choose the execution pattern that fits the research task, balancing runtime, cost, and availability requirements.

[翻译失败，原文如下]

Across the workflow, teams can retain the configuration, model version, evaluation results, and artifacts needed to compare experiments. Computational evaluation supports candidate prioritization; laboratory validation remains essential.

## Get started

Explore theGenesis Workbench repositoryand begin with one target, a defined design objective, and a small experiment. Use the example implementation and available agent skills to adapt the workflow, then execute and track it on AIR before expanding.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Deploy RFD4-Proteina on Databricks](https://www.databricks.com/blog/deploy-rfd4-proteina-model-databricks)
> 
> 翻译时间：2026-10-22 06:56
