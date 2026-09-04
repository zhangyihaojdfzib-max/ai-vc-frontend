---
title: 'Governance beyond security: knowledge, context & ontology on the lakehouse'
title_original: 'Governance beyond security: knowledge, context & ontology on the
  lakehouse'
date: '2026-09-03'
source: Databricks Blog
source_url: https://www.databricks.com/blog/governance-beyond-security-knowledge-context-ontology-lakehouse
author: ''
summary: '[翻译失败，原文如下]


  - The governance artifacts most teams treat as compliance overhead — classification
  tags, de-identification policies, data contracts, mod...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-04T07:08:00.063031'
---

[翻译失败，原文如下]

- The governance artifacts most teams treat as compliance overhead — classification tags, de-identification policies, data contracts, model cards, lineage — are the raw material of enterprise data semantics; the audit work you already do becomes your AI foundation.
- A catalog-centered agentic lifecycle lets AI agents build, test, de-identify, and deploy from curated Unity Catalog metadata, certifying both the data product and the agent through shared human gates. Production PHI never leaves the governed boundary.
- Because meaning and context live in the catalog instead of the more expensive LLM tokens, cheaper models can serve most needs with more trust.

Ask most organizations what data governance for AI means, and you’ll hear a security answer: lock it down, restrict access, pass the audit. In healthcare, security is non-negotiable — but it’s incomplete. Security tells you who can touch data. It says nothing about what the datameans, whether it can betrusted, or whether an AI model should everlearn from it.

Our Data Empowerment Program (DEP) starts from a different premise: governance isknowledge, context, and ontology; not just controls. Artifacts most teams treat as compliance overhead, such as classification tags, de-identification policies, model cards, and data contracts are raw material for enterprise data semantics.

When seen this way, you are not choosing between governance and AI, but instead, governance helps build AI. New approaches to governance need to be implemented in the AI era. The only question is whether you do the work later just to pass the audit, or now, to lay the foundation your AI runs on.

Our goal is to show that the security and governance work you already do is the foundation your AI runs on. Govern the data well enough, and AI can run on cheaper models with more trust.

## Governance must think broader across five pillars through one lens

Start with the lens that every governance artifact contributes to semantics. Every classification tag is a concept. Every model card is context. Every data contract is a shared definition. Every lineage link is a relationship. Read that way, the security stack you already run is the first draft of your ontology, and the catalog is where it lives.

Governance then stops being one thing and becomes five facets of a single discipline: the data itself and how it’s controlled, the AI built on top of it, the people who need to understand it, the products that carry it into the business, and the shared context that ties all four together. It’s the same lens, but from five fronts.

With DEP, we envision semantics through five pillars:

- Data Governance— Catalog, quality, curation, lineage, and with security & compliance built in such as PII classification, access control, HIPAA/GDPR, and AI-specific privacy risks.
- Knowledge (AI/ML) Governance— Model documentation, governance, and responsible-AI standards such as bias & fairness, explainability, human oversight, and EU AI Act readiness.
- Data Literacy— Training, self-service enablement, practitioner certification, and KPIs such as adoption rates, usage metrics, and program ROI.
- Data Management— Architecture, data engineering, and data product contracts should include schema agreements, SLAs & quality thresholds, and producer/consumer obligations.
- Ontology— Glossary, taxonomy, knowledge graph - culminates in an AI semantic layer. This includes context for LLMs, RAG grounding, and chat-query readiness.

## Operationalizing the vision through agents

Our five-pillar vision ends as only slideware unless the platform can carry it out into something operational. Once your governance artifacts live as structured, machine-readable metadata, they stop being just documentation and start being instruction sets for agents.

When we refer to "agent", we are thinking about it in two ways: “build agents” that assemble and deliver data products, and “analytic agents” that answer business questions on top of them; each bound to a single data product.

Let’s start with build agents. Build agents automate the delivery lifecycle of data products from source mapping through ETL, testing, and de-identification to a production release. Everything they need lives in Unity Catalog as governed metadata: source-to-target mappings, business definitions, classification tiers, deidentification policies, data contracts, and model cards. The platform derives from tags, comments, certified flags, lineage, and glossary-linked terms. The catalog isn’t where you just document governance; it’s the runtime the agents execute against.

Each agent works in a loop. It reads instructions from the catalog; does one concrete task such as generating pipeline code, running a test suite, producing de-identified data, or deploying a certified dataset; and then writes the evidence back as test outcomes, quality scores, lineage, or change capture data. This repeats.

![FIG 1 — CATALOG-CENTERED AGENTIC ARCHITECTURE.Unity Catalog curates the metadata. Five AI agents consume that metadata to do lifecycle work — ETL generation, testing, curation validation, de-identification, deployment — and write their results back to the catalog.](/images/posts/6d9cfa7c05cd.png)

In practice, we sequence the De-ID and Testing agents first. They eliminate the highest risks and the heaviest manual work up front. Starting where the payback is fastest helps build momentum early. As we continue through the loop, no agent acts on data the catalog doesn’t describe.

Modern catalogs make this approach scalable because it can auto-generate column and table descriptions for a steward to approve, classify sensitive fields automatically, and capture column-level lineage without anyone maintaining it by hand. Thehuman role shifts from authoring the metadata to approving it, which is exactly the kind of judgment work humans should be doing.

## The data & AI build lifecycle: proof & continuous context

Build agents operate within an end-to-end lifecycle designed to release two assets simultaneously: the governed data product (mapping, curation, pipeline) and the analytic agent running on top of it (semantic layer, prompt configs, eval suites).

This approach marks a fundamental shift from pipeline-centric engineering (moving data from point A to B) to context-centric engineering (making data understandable and actionable for LLMs). Rather than certifying code quality alone, the gates in this lifecycle validate semantics, context, and ownership.

Two core properties distinguish this framework from a traditional SDLC:

- It is auto-proving:Proof of trustworthiness is a natural byproduct of delivery rather than an audit fire-drill assembled after the fact.
- It continuously improves context:Production behavior feeds an AgentOps loop - turning failed queries, hallucination clusters, and user downvotes into the next sprint semantic backlog.

Human stewards serve as the accountability layer for both properties: agents propose, people approve. While managing five gates across two tracks might look like creating lengthy bottlenecks, most gates can clear in mere hours. Approvals take place directly inside standard developers' tooling. Automated test suites attach data quality results, eval scores, and lineage before a ticket is opened. A formal gate meeting is an exception to investigate, not the standard operating procedure.

![Fig 2. DATA & AI BUILD LIFECYCLE: TWO TRACKS, SHARED GATES, ONE CERTIFICATION.Two tracks in one lifecycle: the data product (Track A) and the AI agent or model built on it (Track B) move through the same five gates and earn one shared certification.](/images/posts/fea0bd83d99f.png)

## AI Certification is the engine behind the gates

[翻译失败，原文如下]

The mechanism that makes these gates objective rather than arbitrary is the AI Certification. Recorded directly in Unity Catalog, this certification acts as an automated, query-able scorecard rather than a manual legal attestation. It governs release eligibility across four core dimensions:

- Automated vs. Human Scoring:Governance, Quality, and Semantics scores compute automatically from query-able system tables, pipeline results, and evaluation runs. The Ownership score and final deployment stamp require an explicit steward signature.
- Continuous Expiration:Certification is dynamic. A schema change, contract update, or failed evaluation suite instantly revokes certification until checks to rerun and pass.
- Data-Layer Enforcement:Access controls operate via Attribute-Based Access Control (ABAC) at the data layer, not the application layer. If a user cannot query a row in SQL, no agent can retrieve it via vector search or embeddings.
- Strict Boundary Isolation:Non-production environments (SIT, regression, model testing) consume synthetic or de-identified data exclusively. This ensures production PHI never leaves the governed boundary.

## When the agent is wrong, who fixes it?

Certification and gates prove that an agent was trustworthy at release. But the question governance leaders ask isn't "how does it work"—it's "who is accountable when it gives the wrong answer?" The answer must be a specific name, not a steering committee.

To solve this, each analytic agent (e.g., a Databricks Genie Agent) is bound to a single governed data product with one designated owner. When an agent returns an incorrect result because an underlying metric was misdefined, the issue doesn't belong to the AI engineering team. Instead, it goes straight to the Data Product Owner, who corrects the catalog definition. Binding an agent to a domain-scoped, certified data product is also the single largest accuracy lever available: a focused agent querying certified metadata consistently outperforms a global model guessing across an entire enterprise estate.

Crucially, this shared metric definition is enforced rather than merely documented. Once a certified metric is defined in the catalog, the answer agent is required to compute directly from it. This turns static documentation into active runtime logic.

Accountability is held because of a firm limit on what the AI is allowed to do unattended:no agent promotes code to production, modifies policy, or operates on unclassified data without human intervention. While certification scores are calculated automatically, the final release gate always requires a human signature. If the catalog doesn't explicitly describe a data asset, the system defaults to suppression rather than guessing. At runtime, this fail-closed policy enforces clear boundaries:

- For Analytic Agents:Instead of speculating or inferring context over raw data, the agent explicitly declines to answer—returning a transparent message (e.g., "This dataset lacks active certification or semantic mapping required to process your request.")
- For Build Agents:If an unclassified schema or missing contract is detected during pipeline assembly, execution halts automatically before reaching staging environments, logging an unmapped asset flag for steward review.

Defining these guardrails on paper is easy, but making them work in practice requires replacing vague governance committees with four distinct, accountable roles:

- Data Product Owner:Accountable for a governed product's definitions and quality. They are the single point of contact when an answer is wrong.
- Data & AI Governance Engineer:Translates policy into executable catalog metadata (classifications, contracts, lineage) so rules run at runtime instead of sitting in a PDF.
- Steward:Reviews automated findings and signs off on release gates. Automation proposes; the steward decides.
- Security / IAM:Owns the classification tiers and access attributes that automatically drive de-identification and row-level entitlements.

## Test rigorously without compromising security

The lifecycle we described has a hard prerequisite hiding inside it: every one of those test and evaluation stages needs realistic data to run against – and in healthcare, you can’t test real PHI. So, the challenge becomes the need for realistic test data everywhere without compromising security.

De-identification is how we keep data analytically useful and safe. Where does the de-identification agent get its knowledge? Not from a hand-maintained spreadsheet. It works from security policies the enterprise tools already produce. The flow is three steps:

- Discover- Automated discovery scanners and InfoSec policy engines classify sensitive columns and files.
- Curate- Classifications land in the catalog as curated policy metadata; the agent reads that curation and executes.
- Execute- Ingest metadata, and produce synthetic data or de-identified source files. HIPAA Safe Harbor compliant, referentially intact, analytically capable.

![FIG 3 — DE-ID AGENT: CURATION-TO-POLICY-TO-EXECUTION.Curation-to-policy-to-execution: security tools discover, the catalog curates the de-id policy per column, a steward approves, and the agent executes — generating synthetic data from metadata and de-identifying source files. Anything unclassified is suppressed until a human classifies it.](/images/posts/787e0900f469.png)

For the security & IAM team, this is a two-way street. InfoSec policies stop being PDFs and become executable: classification tiers and retention rules drive de-identification automatically. In return, security gains a continuously updated view of sensitive data, fail-closed protection for anything newly discovered, and residual scans that generate audit evidence on every run. The access model stays the same from end to end. Because any agent data retrieval inherits the querying user's catalog grants, RAG approaches can't surface an embedding of a row the user isn't entitled to see. The same ABAC rules span SQL and vector search alike, and agents act with the querying user's entitlements, not a privileged service account. Every agent prompt is logged with the lineage used to answer it, under the same governance as the data itself.

That is the real unlock: one permission model over the data, the models, the embeddings, and the audit trail — not a data catalog stitched to a separate model registry, stitched to a separate vector store. Governance work becomes the AI foundation instead of a parallel project.

## Capture metrics, prove results, earn trust

Notice what the lifecycle has been doing this whole time: every stage, every gate, every certification has been producing metric. Roll the four certification dimensions into a single AI-readiness score per dataset, and make it operational, not aspirational. Semantics hits 100% only when every column carries a glossary-linked definition and the table has a signed data contract; Ownership hits 100% only when a named owner is responding to issues.

The outcome that follows the scoring is the business case for the whole DEP program: metrics prove the AI's results, proof earns trust, and trust is what converts a pilot into daily usage. No business user adopts an agent because the architecture diagram is elegant. They adopt it because the numbers were right last week and someone accountable fixed them when they weren't. The score explains why the numbers come out right in the first place: the higher the score, the less the model has to guess. It isn't inferring what a column means, compensating for duplicates, or hallucinating joins - because the catalog already told it.

[翻译失败，原文如下]

![FIG 4 — DATA READINESS VS. MODEL SPEND.The contrast that pays for the program: an ungoverned dataset forces frontier-model spend to compensate for missing semantics and quality — and still guesses. A certified dataset lets a cheaper model deliver reporting and basic analytics with more trust, because the intelligence lives in the catalog, not in the token bill.](/images/posts/cae4f0e2b716.png)

## Don't chase model headlines. Chase model economics.

Every week brings a bigger, more expensive model. Here's what the hype cycle misses: when the catalog already supplies the meaning, quality, and context, the model doesn't have to. Smaller or open-weights models serve most needs for reporting and analytics on governed data.

Frontier models are often used to mask underlying metadata gaps. When schemas and business rules are explicitly cataloged, smaller domain-specific models deliver identical accuracy at a fraction of the token cost.

This is a cost-to-quality choice, not a quality ceiling. Right-size the everyday work, and reserve frontier spend for the problems that truly need it, and cost never forces AI to pause. Fix the data. Right-size the model. Keep the accuracy. That's what governance roots buy an AI strategy: not cheaper AI — unstoppable AI.

## Take Action: Start with One Data Product

Don't attempt an enterprise-wide overhaul at once. Prove the model by taking one data product through the full lifecycle:

1. Scan: Enable automated discovery scanning on a single target schema.
2. Define: Set explicit certification thresholds in Unity Catalog for completeness, semantics, and quality.
3. Bind: Attach one analytic agent to the dataset along with a dedicated evaluation suite and de-identified testing path.
4. Assign: Appoint a single named Data Product Owner accountable for definitions and issue resolution.

Once the loop is running, repeat the process one certified data product at a time. Security tells you who can access your data, but governance tells you what it means and whether an AI can trust it.

Governance isn't the gate in front of a data-driven organization. Done right, it's the ground under it.

---

> 本文由AI自动翻译，原文链接：[Governance beyond security: knowledge, context & ontology on the lakehouse](https://www.databricks.com/blog/governance-beyond-security-knowledge-context-ontology-lakehouse)
> 
> 翻译时间：2026-09-04 07:08
