---
title: Four AI Architecture Patterns for Regulated Industries
title_original: Four AI Architecture Patterns for Regulated Industries
date: '2026-11-19'
source: Databricks Blog
source_url: https://www.databricks.com/blog/ai-architecture-patterns-regulated-industries
author: ''
summary: '[翻译失败，原文如下]


  - Four production architecture patterns for combining agents with deterministic
  controls and human accountability.

  - A decision framework...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-20T09:31:29.141398'
---

[翻译失败，原文如下]

- Four production architecture patterns for combining agents with deterministic controls and human accountability.
- A decision framework for determining where agents may reason, generate, recommend, or act.
- Why governed data, lineage, enforcement, evaluation, and audit evidence-not the model alone-make enterprise agents deployable.

Enterprise AI cannot replace every deterministic control. These four patterns help architects decide where agents can reason, act, and remain subject to controls or human authority.

## The architectural question behind enterprise AI

Enterprises are adding agents to systems built on fixed rules and repeatable processes. Agents can reason through complex problems, but enterprise systems-especially in regulated industries-must remain controlled and auditable. The question is not which one to choose. It is how to make them work together.

We are writing this series because customers ask us the same questions: How are enterprises around the world navigating constraints similar to ours? What is the reality of enterprise AI adoption? How are other organizations approaching these nuances? How is Databricks helping solve them when the requirements are ambiguous, complex, and so specific to the institution?

We as Forward Deployed Engineers work at this boundary. We take ambiguous business problems and turn them into production-ready systems. While implementations will vary by institution and we cannot disclose specific implementation details, we can discuss generalized patterns and practices. As agents become part of large enterprise systems, two questions keep recurring:

- Where must determinism remain (e.g., when actions are irreversible or errors carry asymmetric risk)?
- Where can an agent be given authority, particularly if actions are reversible or low-cost to remediate?

The answer is not the same for every use case. Across the systems we are building and modernizing in the field, four patterns are emerging. This first article introduces the framework. The next four articles show how each pattern works in practice.

![Figure 1. A decision framework for placing agents in regulated enterprise systems.](/images/posts/b700739b6768.png)

## Pattern 1: Deterministic control and agentic reasoning

Use this pattern when outcomes must be strictly deterministic and reproducible, or when errors are irreversible and carry high remediation costs. Here,deterministicmeans the result can be reproduced under an explicit, versioned contract that records the data, rule, tolerance, configuration, and execution context together.

Financial Institutions have lots of controls. Reconciliations are a good example. The control must calculate the balances, apply an approved rule, and produce a reproducible PASS or FAIL. An agent cannot reinterpret the tolerance or turn its own explanation into a passed control. When a reconciliation fails, an agent can gather evidence, inspect lineage and batch status, compare the break with prior incidents, test a bounded set of causes, and recommend what should happen next. The deterministic control still decides whether the reconciliation passed. The agent helps explain why it failed.

The agent can investigate the control.It cannot become the control.

This pattern also applies to regulatory calculations, policy enforcement, data quality gates, and system integrity checks-anywhere the result must be precise, reproducible, and auditable.

## Pattern 2: Agentic execution and a deterministic judge

Use this pattern when more than one answer may be valid, but the result can be tested objectively.

Legacy migration or modernization is a good example. An agent can analyze an existing workload and generate a target implementation. It may not produce exactly the same implementation each time. That is not necessarily a problem. What matters is whether the result is correct.

A deterministic judge can test whether the code compiles, schemas conform, data reconciles, control totals match, governance requirements are satisfied, and performance meets the target. If the result fails, the agent receives the evidence, diagnoses the problem, corrects its work, and runs through validation again.

Passing that judge proves that the candidate satisfied the approved acceptance contract. It does not prove that the contract covers every production behavior. Test coverage, production-shaped edge cases, and periodic review still matter.

Do not make the agent deterministic when you can deterministicallyevaluate its output.

The validator is not only a control. It is the feedback loop that allows the agent to improve its result. This pattern works well for migration, code generation, transformation, testing, and remediation.

## Pattern 3: Agentic reasoning and human authority

Use this pattern when the answer requires judgment and cannot be proven correct by a deterministic test.

Financial crime investigations are one example. An agent can correlate transactions, documents, policies, relationships, and historical patterns. It can assemble evidence, identify likely explanations, surface unresolved questions, and recommend a disposition. This is also often required by regulation where a decision significantly affects a person, or when you have to justify the outcome to a regulator, auditor, court, or the affected person

But a recommendation is not a decision. When the outcome is consequential, and there is no deterministic way to establish correctness, authority must remain with an accountable person.

Human review should sit at the decision boundary,not inside every step.

The agent's reasoning must also often be explainable. Every recommendation should trace back to the evidence, sources, and tools behind it. That lets the investigator challenge the logic and lets auditors or regulators reconstruct how the agent reached its recommendation. Where regulation gives an affected person the right to an explanation, the explanation must be specific to the decision. It covers the main factors, the agent's role, and the human's role. "The model flagged it" is not enough. The investigator records the rationale for the final call, including any agent override.

The agent reduces investigative effort and improves the consistency of the evidence presented. The investigator retains responsibility for the final decision, whichmay be subjective and nuanced and not deterministic.

## Pattern 4: Agentic execution with bounded autonomy

Use this pattern when the agent needs to act, but only within an explicit operating envelope.

Consider a Governance Intelligence module that manages access to governed enterprise data. A user describes what data they need, why they need it, and for how long. The agent interprets the request, identifies the appropriate data product, determines the minimum access required, and gathers the relevant identity, policy, ownership, classification, lineage, and usage context.

Requiring manual approval for every standard request creates delay without necessarily reducing risk. Giving the agent unrestricted authority to grant access creates an unacceptable control gap. The answer is bounded autonomy.

The operating envelope defines:

- which data products and access levels qualify for straight-through processing;
- which identity, purpose, geography, legal entity, residency, and segregation of duties rules must pass;
- the maximum duration and minimum level of access that may be granted;
- which approved Unity Catalog actions the agent may initiate;
- which sensitive, ambiguous, or exceptional requests require human approval; and
- how access is monitored, expired, revoked, and recorded for audit.

Within that envelope, the agent can interpret the request, assemble the evidence, select the approved workflow, and initiate a time-bound entitlement. Deterministic policy services validate every required condition before Unity Catalog enforces the grant.

[翻译失败，原文如下]

Do not try to constrain every decision.Constrain the operating envelope.Implementing multi-agent judge frameworks across validation cycles within this envelope can also complement human oversight with automated, multi-perspective safety checks.

If the request falls outside the envelope - for example, because it involves sensitive data, missing attributes, conflicting policies, excessive privilege, or a segregation of duties exception- the system blocks straight through execution and routes it to the appropriate data owner, steward, or risk reviewer.

## How Existing Systems Power Agentic Architecture

### Databricks platform capabilities

Databricks provides the governed foundation across the four patterns. Omnigent can compose agents and agent harnesses without making any one agent the architecture. Unity Gateway governs access to models, tools, MCP servers, and external APIs. Unity Catalog governs enterprise data and enforces approved access including residency and cross-border transfer rules. Secure connectivity reaches on-premises, cloud, and SaaS systems without bypassing these control points. MLflow preserves traces and evaluation evidence that also serve as audit records for regulators. See the attached diagram for a reference architecture showing how agent calls flow through governed control points to customer systems across on-premises, cloud, and regulated jurisdictions.

![image1.png](/images/posts/68d96cd7de4f.png)

Traditional modernization changes where and how technology runs. AI transformation changes the execution model itself. Systems that primarily followed predefined instructions can now interpret, reason, generate, and act.

That does not mean discarding the deterministic systems enterprises have spent decades building. In many cases, those systems become the foundation of the agentic architecture:

- Policy engines become control planes.
- Validation frameworks become deterministic judges.
- Acceptance criteria become agent evaluations.
- Operational limits become autonomy boundaries.
- Governed data, lineage, and audit trails provide the context and evidence agents need.

The opportunity is not simply to replace legacy systems with agents. Across all four patterns, what makes an agent deployable is the ground it stands on: governed enterprise data, verifiable lineage, enforced access, measurable quality, and a reproducible audit trail.

This is especially important in regulated industries, where a weak architectural boundary can lead to control failures, penalties, or delayed regulatory commitments. A well-designed boundary can reduce investigative effort, shorten modernization cycles, and enable high-value automation without transferring inappropriate authority to the model.

AI-native architecture is about deciding where determinism, intelligence, and authority should live.

## Choose the pattern before choosing the agent

Before designing an agentic solution, ask three questions:

- What may the agent reason about?
- What may the agent be allowed to do?
- What must remain outside the agent’s authority?

Those answers determine whether the solution needs a deterministic control, a deterministic judge, a human decision boundary, or an explicit operating envelope. The model comes after that architectural decision-not before it.

The patterns are not mutually exclusive. A production system may use a deterministic control for one decision, human authority for an exception, and bounded autonomy for an approved remediation. The important point is to make each boundary explicit.

As systems mature in production, these boundaries can adapt: deterministic judges refine their evaluation rules using accumulated usage data, while human authority boundaries can shift as feedback establishes confidence in agent reasoning.

## Continue the series

The next four articles take each pattern from architecture to implementation:

Part 2: Deterministic control and agentic reasoningHow agents can investigate exceptions around deterministic financial controls without weakening enforcement or auditability.

Part 3: Agentic execution and a deterministic judgeHow agents can generate and correct implementations while deterministic validation decides whether the result is acceptable.

Part 4: Agentic reasoning and human authorityHow Lakewatch can combine monitoring signals, bank data, and specialist network intelligence into a reviewable evidence package while an accountable investigator retains the consequential decision.

Part 5: Agentic execution with bounded autonomyA design blueprint for agents to coordinate governed data access inside a policy-defined operating envelope, with deterministic authorization, Unity Catalog enforcement, and human resolution of material exceptions.

Classify your use case using the four-pattern framework, then continue to the implementation article that matches the boundary your system requires. For regulated use cases that cross multiple patterns, contact your Databricks account team or FDE engagement manager to map the control, reasoning, and authority boundaries before selecting the agent architecture.

## About the author

Molly Nagamuthu is a Principal Forward Deployed Engineer at Databricks. She works with enterprises on complex data and AI transformation initiatives, particularly with global banks where modernization must coexist with governance, controls, and operational rigor.

In this series, Molly and other Forward Deployed Engineers share implementation patterns emerging from work in the field as enterprises move from deterministic architectures toward AI-native systems.

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Four AI Architecture Patterns for Regulated Industries](https://www.databricks.com/blog/ai-architecture-patterns-regulated-industries)
> 
> 翻译时间：2026-11-20 09:31
