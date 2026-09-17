---
title: Unifying governance across engines and catalogs in the Open Lakehouse
title_original: Unifying governance across engines and catalogs in the Open Lakehouse
date: '2026-09-10'
source: Databricks Blog
source_url: https://www.databricks.com/blog/unifying-governance-across-engines-and-catalogs-open-lakehouse
author: ''
summary: '[翻译失败，原文如下]


  - Read restrictions and catalog labels are two new specs from Apache Iceberg™ that
  help standardize how policies are enforced across engi...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-17T07:00:30.248096'
---

[翻译失败，原文如下]

- Read restrictions and catalog labels are two new specs from Apache Iceberg™ that help standardize how policies are enforced across engines and catalogs.
- Both additions remove fragmented enforcement. Read restrictions delegate decisions to trusted engines; catalog labels make governance metadata portable across federated catalogs.
- There's now a clear model for every access pattern: centralized enforcement for untrusted engines, read restrictions for trusted ones, catalog labels for catalog-to-catalog federation.

In our previous posts, we showed how open table formats, open APIs and unified governance are coming together tocomplete the Open Lakehouse vision. We also introducedcross-engine attribute-based access control, which allows policies defined in Unity Catalog to be enforced consistently when external engines access governed data.

Now, that vision is beginning to materialize in the open. The Apache Iceberg™ community recently advanced two important additions to the Iceberg REST Catalog:read restrictionsandcatalog labels. Together, they address two distinct challenges: delegating enforcement to an external engine and making governance context portable across catalogs.

In this post we will take a closer look at both new additions to the spec: how they work, key challenges they address, future opportunities for innovation, and when to use them.

## Read restrictions: standardizing delegated enforcement

Read restrictions address a common engine-to-catalog scenario: an organization governs data in one catalog and wants to query it from various engines or tools.

For any governed query, three things must happen:

1. The catalog receives the requesting identity and relevant context, such as subjects, groups, roles, or even identity attributes such as ‘region’
2. It evaluates policy to decide whether the user may read the table and which row filters or column masks apply.
3. A trusted compute layer enforces that decision when the data is read.

When data is accessed from an engine, these responsibilities can be divided in two ways.

Withcentralized enforcement, all three steps remain within the catalog’s environment. For example, Databricks implements fine-grained access control on dedicated compute by transparently routing queries through a secure filtering fleet. And Unity Catalog’sCross-engine ABACfeature extends this governance to other engines by putting the filtering fleet behind the Iceberg REST catalog scan/plan APIs to sanitize data before an external engine such as Spark1or DuckDB processes the result.

Withdelegated enforcement,the catalog receives the requesting identity and evaluates policy, then returns the resulting row and column restrictions to an engine it trusts to enforce them. Here, trust means that the catalog can rely on the engine to enforce the restrictions and prevent users from bypassing them. Engines such as Spark and DuckDB are untrusted when users control the runtime because those users can execute arbitrary code or access the underlying data directly. A securely configured Trino deployment is an example of a trusted engine because it provides native enforcement for row filters and column masks.

Delegated enforcement requires a common contract between the catalog and engine. The Iceberg community adoptedread restrictionsto provide that contract.

### How read restrictions work

When a reader loads a table through the Iceberg REST Catalog, the catalog evaluates the applicable policies for the requesting principal and request context. It can return required column-projection actions and row-filter expressions, and the trusted engine must apply those restrictions as it reads the table.

![](/images/posts/6ac4d845a2ea.png)

Two design decisions are important to understanding the proposal’s current scope.

First, the engine does not receive the policy as the administrator defined it.Instead, it receives the outcome for a particular principal, expressed as filtering or masking instructions that it must apply. This creates a common enforcement contract between the engine and catalog. The initial spec defines a bounded vocabulary:nine predefined column-projection actionsandstandardized row-filter expressionssuch as comparisons or set membership. Many real-world enterprise policies depend on subqueries, lookup tables or custom UDFs, which cannot be expressed within the read restrictions vocabulary. This has an important implication: policies can be represented only when the catalog can reduce their result to the vocabulary defined by the standard, otherwise you lose policy semantics.

Second, the specification defines what a trusted engine must enforce, but not how the catalog establishes that trust.A claim from the client is not sufficient, so system administrators and  implementations must use security mechanisms appropriate to their environment. Iceberg community discussions have considered mechanisms such as mTLS and OAuth, but trust ultimately remains outside the protocol (Iceberg community discussion).

Read restrictions are best suited for direct engine-to-catalog access scenarios where the source catalog’s policies are simple and a trusted engine can enforce the resulting decision. Many implementation questions remain, such as how an engine securely propagates the end user’s identity and attributes, how a catalog distinguishes the user from the engine acting on the user’s behalf, and how credentials are bound to their intended recipient. As implementations emerge, we’re excited to collaborate with the Iceberg community to work through these challenges and evolve the standard.

## Catalog labels: making governance context portable

Catalog labels address a different scenario: governance across federated catalogs.

Many enterprises now connect multiple catalogs, such as Unity Catalog, Snowflake, AWS Lake Formation and Google Cloud Knowledge Catalog, through federation and open APIs. This is more complex than an engine-to-catalog integration because each catalog serves its own users, applications, and engines through distinct identity models, policy languages, and semantics.

Any unified governance solution that works at enterprise scale must:

- Preserve policy expressiveness.Customers must be able to define sophisticated rules, including attribute-based policies and complex subqueries, and enforce them consistently across heterogeneous systems.
- Provide clear auditability and accountability. Each catalog must be able to demonstrate compliance independently without requiring administrators to reconcile audit trails across multiple systems.
- Scale without putting another catalog service in the critical path. Permissions-aware discovery in Catalog A should not require a call to Catalog B for every user and asset. For example, most user experiences in Unity Catalog are permissions-aware, and loading the catalog explorer or providing typeahead search could otherwise require thousands of per-user decisions that aredifficult to cache, which makes the user experience slow and ties performance and availability to another service.

Catalog labels, recently adopted by the Iceberg community, is the first step towards this vision. Labels allow catalogs to exchange lightweight key-value metadata at the table and column level via Open APIs. Labels can indicate that a field contains PII, associate a dataset with a business domain, or provide semantic hints for AI models. Because the proposal is general, labels can support many use cases beyond access control, including discovery, ownership, cost attribution, AI context, and data quality.

### How catalog labels work

When a consuming catalog loads a table from a producing catalog via catalog federation, the producing catalog returns table and column-level labels.

![](/images/posts/35c45f773f83.png)

[翻译失败，原文如下]

The consuming catalog then maps the labels into its own classifications, attributes or native tag model. It then evaluates access using its native identities and policies and enforces controls within its own runtime. For example, if a producing catalog labels an ssn column pii=ssn, the consuming catalog can apply a tag-based policy that masks columns carrying that label.

Because policy enforcement remains local, the consuming catalog preserves the expressiveness of its native policies and avoids calling the producing catalog for each access decision. Each catalog also independently maintains its enforcement records and audit trail.

It is worth keeping in mind that labels are opaque key-value pairs. The standard defines no shared semantics or stable identifiers, and lineage for labels does not extend beyond the source catalog. The consuming catalog receives only the resolved key and value, not whether the label was intended for discovery, access control, cost attribution, or another purpose. Labels therefore make metadata portable, but not its meaning; enterprises still need shared conventions or explicit mappings to interpret labels consistently.

Catalog labels are best suited for catalog-to-catalog scenarios with federation between heterogeneous systems, where the consuming catalog has its own governance system and needs reusable context rather than a separate access decision for every user and request. The core idea is that governance and business context, like table metadata, should be open and portable through the Iceberg REST Catalog APIs.

## Choosing the right model

The right model depends on the destination: centralized enforcement for an untrusted engine, read restrictions for a trusted engine, and catalog labels for open metadata exchange when the destination is another catalog with its own governance system.

Centralized enforcement through scan planning

Read restrictions

Catalog labels

How it works

The source catalog evaluates and enforces policy through a secure filtering service, returning only authorized data

At query time, the catalog tells the engine what restrictions to apply for this particular user and asset - e.g. “apply mask_alphanum on column 12”

Catalogs share additional governance or business information about a given table - e.g. “column 12 has classificationpii=ssn”

Best fit

Direct access from an untrusted engine, such as a user-controlled Spark or DuckDB runtime

Direct engine-to-catalog access where the source evaluates policy and a trusted engine enforces the result

Federation between heterogeneous systems with their own identity, policy and enforcement runtime

Identity and security

Client must translate and pass identity concepts (roles, groups, etc) to the catalog. Enforcement remains within the catalog’s trusted boundary, so unauthorized data never reaches the engine.

The client must translate identity concepts (principals, roles, groups, user attributes) to something that the catalog understands and pass these attributes as part of the request context

The destination uses the identities and attributes it already understands, reducing the sensitive context exchanged between systems

Scale, performance and availability

Server-side scan planning can optimize data access, but routing governed queries through a filter fleet adds latency and an operational dependency compared with enforcement in the consuming engine.

The destination catalog can no longerreuse a cached tableacross its users because table responses become user-specific. This causes experiences like browsing, search, and autocomplete to require a per-user cache or require a separate call to the source catalog for each user action.

Governance context can be cached and refreshed so that search, browse, and other user experiences are powered natively

Governance and auditability

The source catalog retains its full native policy expressiveness and records policy evaluation and enforcement within the same trusted environment

Decisions are limited to the standard’s shared vocabulary. Audit records are split across both the source and destination systems.

The destination uses its native policy engine and maintains an end-to-end record of evaluation and enforcement

Bottom line

Use when the source catalog must guarantee that unauthorized data never reaches an untrusted engine

Use when the destination is a trusted engine and the source policies can be fully expressed with read restrictions

Use when the destination is another catalog that needs scalable governance at native speed across its users and engines

## What comes next

Read restrictions and catalog labels solve two distinct and important problems for cross-platform governance. Read restrictions give catalogs a standard way to delegate enforcement to trusted engines. Catalog labels make governance and business context portable across catalogs, just like your data is. Along with centralized enforcement throughCross-Engine ABAC, these give enterprises a practical set of options for governing data consistently across engines and catalogs.

Congratulations to the Apache Iceberg community for adopting both proposals. While there is more work ahead, this is a big milestone. We are excited to see more of the ecosystem adopt these foundational building blocks, and to continue working with the community to make unified governance across the open lakehouse a reality.

1Apache Spark’s own security guidancestates that user-submitted code runs without restrictions on its behavior and gives users control over the resources assigned to their application. A Spark extension can implement read restrictions, but the deployment qualifies as trusted only when administrators control the runtime and eliminate every path around enforcement since it lacks a table-level access control API, let alone one for fine-grained access control (Iceberg community discussion).

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Unifying governance across engines and catalogs in the Open Lakehouse](https://www.databricks.com/blog/unifying-governance-across-engines-and-catalogs-open-lakehouse)
> 
> 翻译时间：2026-09-17 07:00
