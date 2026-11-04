---
title: Declare and optimize with UNIQUE constraints on Databricks
title_original: Declare and optimize with UNIQUE constraints on Databricks
date: '2026-11-03'
source: Databricks Blog
source_url: https://www.databricks.com/blog/declare-and-optimize-unique-constraints-databricks
author: ''
summary: '[翻译失败，原文如下]


  - Databricks UNIQUE constraints let teams declare multiple nullable or composite
  uniqueness guarantees beyond a table’s single PRIMARY KE...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-04T08:50:46.049784'
---

[翻译失败，原文如下]

- Databricks UNIQUE constraints let teams declare multiple nullable or composite uniqueness guarantees beyond a table’s single PRIMARY KEY, and reference them with foreign keys.
- Validate and continuously maintain these informational constraints before using RELY, which enables the optimizer to eliminate redundant joins and DISTINCT aggregations.
- In 10 TB TPC-DS benchmarks, UNIQUE with RELY removed over 99.99% of shuffle and delivered up to 12× faster queries.

Data teams often maintain uniqueness guarantees in their pipelines, but without a flexible way to represent all of them in the table schema, users and tools cannot discover them and the query optimizer cannot safely leverage them. Business entities often have more than one value, or combination of values, known to be unique: auserstable might useuser_idas its primary row identifier while its data model also records separate uniqueness guarantees forusername, an email address, and(workspace_id, external_user_id).

Databricks already supportsPRIMARY KEY and FOREIGN KEY constraints: a primary key identifies a table's rows, and foreign keys can reference it to describe relationships. A table can have only one primary key, however, and its columns must be non-nullable.UNIQUEconstraints, now available in Public Preview for Unity Catalog Delta tables in Databricks SQL and Databricks Runtime 18.2 and above, add a way to record the other uniqueness guarantees. A table can declare multipleUNIQUEconstraints, their columns can be nullable, and foreign keys can reference them. After you validate these constraints and mark them withRELY, the query optimizer can also use them to eliminate unnecessary joins and aggregations.

## When one primary key can't cover every unique column

PRIMARY KEYandUNIQUEboth record uniqueness, but they serve different schema roles:

## Put your pipeline’s uniqueness guarantees in the schema

The following table has a primary key and twoUNIQUEconstraints:

The two unique constraints illustrate different kinds of uniqueness.users_external_uqapplies to a column combination: each(workspace_id, external_user_id)pair must be unique even though either value may appear in other pairs.users_optional_id_uqapplies to a nullable column. The following rows show which values satisfy that guarantee:

## Record the guarantee without paying a cost on every write

Like primary and foreign key constraints on Databricks,UNIQUEconstraints are informational and are not enforced when data is written. DeclaringUNIQUE (optional_identifier), for example, does not cause a write containing duplicate non-null values to fail.

This separation lets the schema record a uniqueness guarantee maintained by an ingestion pipeline, an upstream system, or another data-quality process. The guarantee also becomes table metadata that users, tools, and applications can inspect.

## Reference a UNIQUE constraint from a foreign key

A foreign key can reference aUNIQUEconstraint in addition to a primary key. For example, the compositeUNIQUEconstraint declared above can be referenced as follows:

The referenced parent columns identify which unique constraint the foreign key targets. Child and parent columns correspond by position:workspace_idmaps toworkspace_id, andsource_user_idmaps toexternal_user_id. Their names do not need to match, but their types and positions must correspond. TheREFERENCES(parent) columns must be listed in the same order as the columns in theUNIQUEconstraint's definition; otherwise the constraint is still valid but join elimination silently won't fire.

To reference a single-columnUNIQUEconstraint, explicitly name its parent column, for example,REFERENCES users (username). If the parent column list is omitted,REFERENCES userstargets the table’s primary key instead.

## Optimize queries with RELY

By default, a unique constraint is created withNORELY. It records the intended schema semantics, but Databricks does not use it for correctness-dependent query rewrites. The following statement creates a constraint with this default:

After you have verified the data and ensured that your pipelines will continue to maintain the guarantee, you can drop and re-create the constraint withRELY:

In this example,CASCADEalso drops any foreign keys that referenceusers_username_uq, and they must be re-created after the unique constraint is added back. WithoutCASCADE,DROP CONSTRAINTuses the defaultRESTRICTbehavior and is rejected when dependent foreign keys exist.

A foreign key that references the unique constraint can also be declared withRELY:

RELYis set independently on each constraint. It does not validate existing data or enforce the constraint on future writes. It allows Databricks to assume that the constraint is valid when optimizing queries. If the data violates a relied-upon constraint, a rewrite based on that constraint can produce incorrect results. You should therefore useRELYonly for guarantees that are validated and continuously maintained.

WithRELY, unique constraints can provide the information needed for eligible join and aggregation rewrites. Eligibility also depends on other guarantees required by the query, including nullability, as the examples below illustrate. This optimization support is available onPhoton-enabled compute. Theprimary and foreign key blogdescribes constraint-based join and aggregation optimizations thatUNIQUEconstraints can also enable. Since that post was published,RELYsupport has become available for foreign keys and now forUNIQUEconstraints.

### Eliminate joins using UNIQUE and foreign key constraints

Some dashboards built on the same data need attributes fromusers, so teams often create a shared view that always joinsuser_eventswithusers. A dashboard that needs only information fromuser_eventsmay still inherit that join from the view. Its generated SQL can therefore look like the query below, even though it does not select any columns fromusers:

Although the query returns no columns fromusers, the optimizer cannot normally remove the join. An inner join could remove an event if no matching user exists, or duplicate it if multiple users have the same username.

The relied-upon constraints rule out both possibilities. TheUNIQUEconstraint guarantees at most one matching user, while the foreign key guarantees that a match exists. Becauseuser_events.usernameis alsoNOT NULL, every event has exactly one match. The join therefore cannot change the result, and the optimizer can readevent_iddirectly fromuser_events.

The earlier primary and foreign key blog demonstrates the relatedLEFT OUTER JOINcase, which needs only the at-most-one guarantee. ThisINNER JOINexample also needs the foreign key to establish that a match exists.

WithNORELYconstraints, the optimized plan retains the join:

When both constraints useRELY, the optimizer can know that every event has exactly one matching user and remove the join:

In this example,user_events.usernameisNOT NULL, but the optimization also applies when it is nullable: Databricks will remove the join and add anIS NOT NULLfilter on theuser_events.usernameto preserve the inner join's handling of nulls.

We benchmarked this optimization on the TPC-DS SF10000 dataset, which represents a 10 TB scale factor. On the 28.8-billion-rowstore_salestable joined to the 65-million-rowcustomertable, we declaredcustomer.c_customer_skasUNIQUEand defined a foreign key fromstore_sales.ss_customer_sk. WithRELYon both constraints, Databricks eliminated the join, removed more than 99.99% of shuffle, and reduced median engine execution time from 23.6 seconds to 3.0 seconds - a 7.9x speedup.

### Skip DISTINCT when values are already unique

[翻译失败，原文如下]

BI tools and query builders often addDISTINCTdefensively because joins may produce duplicate rows. When the selected values are already unique,DISTINCTremoves nothing, but it can still require an aggregation and shuffle unless the optimizer can prove that the operation is unnecessary. A relied-uponUNIQUEconstraint can provide that proof.

Consider auser_identifierstable with these two constraints:

- UNIQUE (user_id) RELY, whereuser_idisNOT NULL
- UNIQUE (optional_identifier) RELY, whereoptional_identifieris nullable

The table contains the following data, which satisfies both constraints:

Foruser_id, the optimizer can use the uniqueness and non-null guarantees together:

The optimized plan contains no aggregation:

The aggregation is gone because the relied-upon constraint establishes that everyuser_idis already distinct.

The equivalent query overoptional_identifiershows why the optimizer also considers nullability:

The optimized plan retains the aggregation:

Both constraints useRELY, but the nullable constraint permits the twoNULLrows shown above. SQLDISTINCTmust collapse those rows into one, so the aggregation is still necessary.

NullableUNIQUEconstraints can still enable the optimization when the query supplies the missing non-null guarantee:

The optimizer can remove the aggregation:

The filter removes the values that may repeat under nullableUNIQUEsemantics. The remaining values are guaranteed to be distinct, so Databricks can again avoid the aggregation.

We benchmarked this optimization on the same TPC-DS SF10000 dataset, which represents a 10 TB scale factor. On the 28.8-billion-rowstore_salestable, we declared(ss_item_sk, ss_ticket_number)as a compositeUNIQUEconstraint and ran aDISTINCTquery over those columns. WithRELY, Databricks eliminated theDISTINCTaggregation, removed more than 99.99% of shuffle, and reduced median engine execution time from 33.7 seconds to 2.8 seconds - a 12.0x speedup.

## Validate your data before optimizer uses a constraint

### Find duplicate and orphaned rows

Before usingRELY, check that the data satisfies the guarantee. For a nullableUNIQUEconstraint, exclude rows containingNULLbecauseUNIQUEpermits those rows to repeat. This query finds duplicate non-null identifiers:

For a compositeUNIQUEconstraint, group by every constrained column and add anIS NOT NULLcondition for each nullable column. You can also find child rows with no matching parent by using a left anti join:

These checks validate the current data. Your ingestion or data-quality pipeline must continue to maintain the guarantees after you enableRELY.

### Confirm the declared constraints

After declaring or re-creating a constraint, you can confirm its definition in several ways:

- SHOW CREATE TABLE
- DESCRIBE TABLE EXTENDED
- Unity CatalogINFORMATION_SCHEMArelations:TABLE_CONSTRAINTSKEY_COLUMN_USAGECONSTRAINT_TABLE_USAGECONSTRAINT_COLUMN_USAGEREFERENTIAL_CONSTRAINTS

- TABLE_CONSTRAINTS
- KEY_COLUMN_USAGE
- CONSTRAINT_TABLE_USAGE
- CONSTRAINT_COLUMN_USAGE
- REFERENTIAL_CONSTRAINTS

SeeConstraints on Databricksand theCONSTRAINT clausefor complete create, alter, inspect, and drop syntax.

### Roll out UNIQUE and RELY incrementally

You can adoptUNIQUEincrementally:

1. Declare existing uniqueness guarantees with the defaultNORELY.
2. Reference unique keys from foreign keys where the relationship is part of the schema.
3. Validate and continuously maintain uniqueness and referential integrity in your data pipelines.
4. UseRELYon theUNIQUEconstraint only after verifying uniqueness, and on the foreign key only after verifying that every applicable child value has a matching parent row.
5. Compare plans withEXPLAINto confirm eligible rewrites.

## Conclusion

UNIQUEconstraints let a table record multiple uniqueness guarantees in addition to its single, non-nullablePRIMARY KEY, and the constrained columns can be nullable. Foreign keys can reference aUNIQUEconstraint as well as a primary key.UNIQUEconstraints are informational by default; after validation,RELYlets Databricks use them to optimize eligible joins andDISTINCTqueries.

Data Warehousing

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Declare and optimize with UNIQUE constraints on Databricks](https://www.databricks.com/blog/declare-and-optimize-unique-constraints-databricks)
> 
> 翻译时间：2026-11-04 08:50
