---
title: 'From spot fixes to measured gains: improving document extraction accuracy
  with ai_extract and MLflow Prompt Registry'
title_original: 'From spot fixes to measured gains: improving document extraction
  accuracy with ai_extract and MLflow Prompt Registry'
date: '2026-10-27'
source: Databricks Blog
source_url: https://www.databricks.com/blog/spot-fixes-measured-gains-improving-document-extraction-accuracy-aiextract-and-mlflow-prompt
author: ''
summary: '[翻译失败，原文如下]


  - You don''t have to do it all yourself:Genie Code for document processingautomates
  the core of this workflow, scoring extraction field by...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-30T08:48:00.622972'
---

[翻译失败，原文如下]

- You don't have to do it all yourself:Genie Code for document processingautomates the core of this workflow, scoring extraction field by field against your labeled data, proposing schema and instruction fixes as reviewable diffs, and re-running the eval to show before-and-after results.
- Improve ai_extract accuracy with the right lever:Use schema descriptions for field-level rules, prompts for document-level logic, precision mode for structural complexity, and citations to diagnose errors.
- Version prompts and schemas with MLflow Prompt Registry:Track extraction logic as versioned artifacts and deploy or roll back changes through aliases instead of editing pipeline code.
- Evaluate changes before promotion:Compare candidates against fixed, human-reviewed ground truth while tracking accuracy, coverage, and run-to-run variation.

Document extraction often starts with a simple loop: spot an incorrect field, adjust the prompt or schema, rerun the document, and check the result.

That approach becomes unreliable as fields and document formats multiply. A change may fix one field while introducing regressions elsewhere, work for one layout but fail on another, or appear better simply due to normal variation across LLM runs.

We saw this on a recent project that extracted roughly 40 structured fields from partner-submitted order documents across dozens of PDF layouts. Reviewers corrected and approved extracted values before they moved downstream, giving us human-reviewed ground truth for evaluation.

The challenge was not gettingai_extractto return the fields. It was improving extraction without degrading the system overall.

For example, therevisionfield sometimes returned status terms such asORIGINALinstead of arevisionnumber or blank. A small schema change cut errors for that field roughly in half. But across every field, total extraction errors increased by 9%.

The lesson was clear: improving one field does not necessarily improve the extraction system.

The pipeline already had most of the pieces needed to evaluate changes systematically. Documents landed in object storage and flowed through a Lakeflow SDP pipeline using Auto Loader. Bronze parsed documents with ai_parse_document, Silver extracted structured fields with ai_extract, and Gold published results as a materialized view. Predictions synced to Lakebase, where a Databricks App let reviewers correct and approve fields, and Lakebase CDC returned those approvals to the lakehouse.

![Figure 1. A document-extraction pipeline with human review. Prompts and schemas are hardcoded in Silver, while reviewer corrections are not yet used to evaluate extraction changes.](/images/posts/efcde7144abd.gif)

Two pieces were missing from the feedback loop. Reviewer approvals were available, but they were not assembled into a reusable evaluation dataset. At the same time, prompts and schemas were embedded directly in pipeline code, so even a small change to extraction required a code deployment.

We addressed both problems by building a workflow around three questions:What should we change? How should we version it? And what evidence is enough to promote it?

This post covers three parts of that workflow:

- Improve ai_extract with the right lever:Use schemas for field rules, global instructions for document logic, precision mode for difficult structures, and citations to diagnose errors.
- Version prompts and schemas:Store both in MLflow Prompt Registry and use aliases to deploy or roll back configurations without editing pipeline code.
- Evaluate before promotion: Compare candidates on fixed, human-reviewed ground truth, tracking accuracy, coverage, and run-to-run variation.

Together, these steps create a repeatable path from a proposed extraction change to production, with evidence that the change improves the system as a whole.

## Start with Genie Code

The rest of this post walks through the practices we recommend and why each one matters. You don't have to implement all of them on your own.Genie Code for document processingbuilds the Lakeflow job (ai_parse_document, ai_classify, and ai_extract with citations and confidence scores) and automates the core of this workflow with anevaluation and hill-climbing loop:

- Measure: Scores the current extraction field by field against your labeled table, so you can see which fields are weak.
- Improve: Proposes a fix, most often a sharper field description, as a reviewable diff that you approve before it applies.
- Re-evaluate: Re-runs the eval set after every accepted change and shows before-and-after results, so regressions are as visible as improvements.

For example, you can ask Genie Code: "Evaluate the extraction against my labeled table and tell me which fields are weakest," followed by "Accuracy on the revision field could be higher. Iteratively improve the schema and instructions, re-run the evaluation, and show me the before and after."

Understanding the fundamentals still matters. It helps you judge Genie Code's proposed changes, decide when a result is good enough to promote, and extend the workflow for production, for example by versioning prompts and schemas in MLflow Prompt Registry. Each section below explains a recommended practice and notes how Genie Code can handle it for you.

## Choose the rightai_extractlever

ai_extracttakes three inputs: the parsed document, a JSON schema, and optional global instructions.

The schema and instructions serve different purposes:

- Schema:Defines output fields and field-specific extraction rules.
- Global instructions:Provide guidance that applies across the document.

The result is a structured value with one entry for each schema field. You can access individual fields directly, for example:extracted:response.revision.value.

### Put field-specific rules in the schema.

Start with the schema structure. When a field has a closed set of valid values, use an enum constraint rather than listing the allowed values in the description. Use numeric types for numbers and integers, and use nested arrays or objects for repeated structures.

Then use schema descriptions for rules that types alone cannot express, such as:

- Preserve leading zeros in identifiers such as004
- Exclude status terms such asORIGINAL,NEW, orREVISED
- Stop an identifier at the first invalid character
- Returnnullwhen a value isn't present

KEY: Keeping field rules in the schema makes the extraction contract easier to inspect and prevents the global prompt from becoming a list of unrelated exceptions.

### Use the global prompt for document-level reasoning

Reserve the global prompt for rules that apply across the document, including:

- Document or domain context
- Source priority, such as headers over footers
- Cross-field consistency rules
- Instructions for combining rows into arrays
- Document regions that should not be used as sources

For example, if entity names are mistakenly extracted from boilerplate footers or third-party contact blocks, aFORBIDDEN-SOURCESinstruction can tell the model to ignore those regions.

A useful rule is:If the rule defines one field, put it in the schema. If it defines how to interpret the document, put it in the prompt.

Automate it with Genie Code: The hill-climbing loop follows the same principle. Its proposed fixes most often sharpen a field description in the schema, and are shown as a diff for you to approve before they apply.

### Keep deterministic formatting downstream.

Not every transformation needs an LLM. Handle casing, separator removal, zero-padding, and mappings such as TELEVISION to TV with SQL or another deterministic transformation when possible.

KEY: Use the model to interpret the document; use code to normalize the output.

### Use precision mode for structural problems.

[翻译失败，原文如下]

Sometimes the instructions are clear, but the document is difficult to follow. Large schemas, repeated line items, complex tables, and multi-page layouts can make it hard to keep values aligned with the right rows.

For these cases,ai_extractversion 2.1 offers precision mode:

Precision Modebrings frontier extraction capabilities for more demanding use cases. With the prompt and schema held constant, it tends to help most on repeated structures and reduces over-extraction (the model returning a value where the correct answer is blank).

Diagnose the failure before changing the configuration:

- If the model misunderstandswhat a field means, change the prompt or schema.
- If it understands the field but struggles withthe data structure, test precision mode.

The approaches are complementary. In our testing, the schema rule corrected a field the model misunderstood, while precision mode improved extraction of fields from complex tables.

### Use citations to understand why a field is wrong.

When an extracted value is wrong, citations help show where the model found its answer:

Citations provide field-level bounding boxes that can be mapped back to element spans in the source document. This helps distinguish between two different types of errors:

- Extraction error:The model selected the wrong region, misunderstood the field, or returned a value that is not supported by the source.
- Labeling disagreement:The model extracted from the correct location, but the expected answer follows a different reviewer convention.

These require different fixes. Extraction errors may call for a change to the schema or prompt. Labeling disagreements should be resolved by defining the expected convention in the reviewer guidelines.

Confidence scores can also help prioritize human review:

Use them as a ranking signal, such as reviewing low-confidence fields first, rather than as an automatic quality gate. A high-confidence result can still be wrong.

InGenie Code: The extraction tasks Genie Code builds include citations and confidence scores. You can ask it to "Set confidence thresholds per field from the evaluation results and route low-confidence rows to review," and use the Document Parsing UI to visually debug parsing and extraction.

## Version prompts and schemas together

Reduce the friction of hardcoding prompts and schemas in notebooks by managing them as configurable, reusable definitions outside the pipeline code. A small wording change requires a code deployment, previous versions are difficult to reconstruct, and there is no evidence that the new version is better than the old one.

MLflow Prompt Registry lets you version those inputs separately from pipeline code.Version both the prompt and the schema:field descriptions influence extraction just as global instructions do. Version only the prompt, and half of your extraction logic is still traveling as an untracked code change.

Beyond the Genie Code loop: Genie Code helps you find the right prompt and schema. When you take that configuration to production, versioning it lets you promote and roll back changes without a code deployment.

A simple alias strategy might use:

- @prodfor the currently approved version
- @candidatefor the version under evaluation
- @scr_*for experimental versions being compared in parallel

The pipeline then loads the active versions by alias:

The resolved prompt and schema are then passed toai_extract.

When a candidate is approved,mlflow.genai.set_prompt_aliascan move@prodto the new version. The pipeline resolves it on the next run without changing the pipeline code. To roll back, restore both aliases to the previous recorded versions. The underlying versions remain in the registry.

This separates extraction configuration from the code that runs it. Figure 2 also adds the other missing piece: reusable ground truth.

![Figure 2. Silver reads approved prompts and schemas from the registry. Reviewer sign-offs feed a ground-truth view.](/images/posts/0ef95dd5085e.gif)

The ground-truth view pairs approved labels with source documents and predictions, creating the reference dataset for measuring changes.

## Evaluate candidates against fixed ground truth.

Version history tells you what changed. It doesn't tell you whether the change was better. Build a fixed cohort from reviewer-approved results; ours was several hundred PDFs covering a wide range of layouts. Score the production prompt and each candidate prompt against the same test set.

For every version, track metrics such as:

- Overall and field-level accuracy
- Ground-truth coverage
- Performance by document type
- Run-to-run variation

Keep both the documents and metric definitions consistent across comparisons. Otherwise, a score change could reflect a different test set or scoring rule rather than a different extraction configuration.

InGenie Code: Point Genie Code at your labeled table, such as the ground-truth view in Figure 2, and ask it to evaluate the extraction. It scores each field and re-runs the same eval set after each accepted change, so before-and-after comparisons use the same documents. The noise-floor, coverage, and verdict checks below are useful guardrails to add when you take a change to production.

### Account for normal LLM variation

A candidate scoring slightly higher once doesn't mean it is better. Run the production configuration at least 3-5 times on the frozen test set and calculate its mean accuracy and standard deviation (σ). That σ is your noise floor. Your policy might require a candidate's improvement to exceed 2σ before treating it as meaningful; anything inside that band is inconclusive rather than a win.

### Track coverage alongside accuracy

Accuracy can also be misleading if you ignore missing predictions.

Suppose you score only fields where both the model and reviewer supplied a value. A candidate that leaves difficult fields blank can appear more accurate because those misses disappear from the denominator. The reverse can also happen. When we scored therevisionfield only on documents where the reviewer supplied arevisionvalue, our fix appeared to improve accuracy by less than 3 percentage points. But when we counted all errors, including cases where the correct answer was blank, the fix cutrevisionerrors roughly in half. Most of the improvement came from correctly returning no value where one did not belong.

That is why coverage should be reported alongside accuracy. Define it explicitly, for example, as the share of non-null ground-truth fields for which the model returns a prediction. If accuracy rises but coverage falls materially, investigate before promoting the candidate.

The resulting harness follows a repeatable sequence: freeze the test set, establish the production baseline, register a candidate on a screening alias, run repeated evaluations, and compare accuracy, coverage, and stability.

![Figure 3: The evaluation sequence: freeze the test set, measure the production baseline, screen a candidate, and compare accuracy, coverage, and stability.](/images/posts/3e0f3d792369.gif)

## Summarize each evaluation as a verdict.

Once you measure accuracy, coverage, and run-to-run variation, your evaluation harness can reduce those metrics to a small set of outcomes:

- BETTER:Accuracy clears the predefined threshold, coverage holds, and results are stable.
- SUSPECT:Accuracy improves, but coverage falls materially.
- UNSTABLE:Results vary too much across runs.
- INCONCLUSIVE:The difference is too small to distinguish from normal variation.
- WORSE:Accuracy declines meaningfully.

These verdicts provide a consistent way to summarize an evaluation before deciding whether the candidate should be promoted to production.

## Following the revision change through

We scored each candidate three times on the same test set, counting errors in every field, relative to the original prompt and schema.

[翻译失败，原文如下]

The spot fix did what we wanted forrevision, but the model started inventing values in unrelated line-item fields such as schedule details. Editing one field's description is not a one-field experiment: the model reads the schema as a whole.

So we did not ship it.

Instead, we moved field-specific rules out of the global prompt and into schema descriptions, including the samerevisionrule. The prompt ended up at less than half its original length, and errors fell by 16% overall, withestimateerrors down by 30%.

Two fields worsened, and they went on the target list for the next round.

Precision mode told a different story. With no prompt or schema change, it cut errors by 24%, mostly by no longer inventing values in repeated line-item fields. But it barely changedrevisionerrors because that was a definition problem, and only the schema rule fixed it.

Combined, they stack: precision mode on top of the restructured prompt and schema removed another 19% of the remaining errors. Overall, errors fell by about a third (32%), andrevisionerrors by nearly two-thirds (64%).

This is the regressionGenie Code'sloop is designed to surface. Because every accepted change re-runs the full eval set, a spot fix that helps revision but hurts line-item fields appears in the before-and-after results rather than in production.

![Figure 4. Each candidate's three runs next to the original configuration in MLflow. Every run is logged with its prompt version, schema version, and engine, so each result traces back to the exact configuration that produced it.](/images/posts/94f1cc2433f7.png)

## Turn evaluation into a promotion decision.

A verdict is a starting point, not the final decision.

One earlier candidate cut estimate errors by about a third and was only INCONCLUSIVE overall. But it had also started filling in a yes/no flag on nearly every document, while reviewers had marked that field on only a handful of documents.

A severe regression in one field can preclude promotion even when aggregate metrics appear acceptable. Promotion should therefore remain human-controlled.

If a candidate is classified asBETTER, an owner can update the@prodalias and record the candidate version, evaluation metrics, author, and timestamp.

There may also be valid reasons to promote anINCONCLUSIVEchange, such as implementing an important business convention not fully captured by aggregate accuracy. In those cases, recording an override reason preserves the rationale behind the decision.

With that review and alias update, the feedback loop closes:

![Figure 5. The complete loop: reviewer approvals become ground truth, the harness evaluates a candidate, and an owner promotes an approved prompt-and-schema pair. A fresh pipeline initialization loads the new versions.](/images/posts/4d1e55e8e19d.gif)

## Build a repeatable extraction workflow.

Reliable document extraction is not about finding one perfect prompt. It is about choosing the appropriate change, tracking what changed, and testing whether the result improved.

Withai_extract, that means using schema descriptions for field-level behavior, global instructions for document-level reasoning, precision mode when structure is the bottleneck, and citations when you need to understand why an extraction failed.

MLflow Prompt Registry then gives you a versioned path for managing prompts and schemas, while a fixed evaluation test set gives you evidence for deciding what should reach production.

Together, those pieces turn prompt iteration from a series of one-off edits into a repeatable engineering workflow.

Genie Code for document processingautomates the core of this loop (measure, improve, re-evaluate), so most teams can start there, then add Prompt Registry versioning, noise-floor checks, and promotion gates as the pipeline moves to production.

Explore theDatabricks AI Functions documentationto learn more aboutai_extract, and see theMLflow Prompt Registry documentationfor prompt versioning and alias management.Try Genie Code for document processing. Open Genie Code from Jobs and Pipelines, point it at your documents and a labeled table, and ask it to evaluate and improve your extraction.

Solutions,Customers,Best Practices,Media & EntertainmentandData Science and ML

---

> 本文由AI自动翻译，原文链接：[From spot fixes to measured gains: improving document extraction accuracy with ai_extract and MLflow Prompt Registry](https://www.databricks.com/blog/spot-fixes-measured-gains-improving-document-extraction-accuracy-aiextract-and-mlflow-prompt)
> 
> 翻译时间：2026-10-30 08:48
