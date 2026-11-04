---
title: Claude Platform now supports native OpenTelemetry observability in Databricks
  MLflow
title_original: Claude Platform now supports native OpenTelemetry observability in
  Databricks MLflow
date: '2026-11-03'
source: Databricks Blog
source_url: https://www.databricks.com/blog/claude-platform-now-supports-native-opentelemetry-observability-databricks-mlflow
author: ''
summary: '[翻译失败，原文如下]


  - OpenTelemetry for Claude Platform is now in Public Beta. The native OTel export
  brings Anthropic SDKs, Messages API and Claude Managed ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-04T08:50:46.721786'
---

[翻译失败，原文如下]

- OpenTelemetry for Claude Platform is now in Public Beta. The native OTel export brings Anthropic SDKs, Messages API and Claude Managed Agents into Databricks MLflow, with traces stored in Unity Catalog.
- Use trace analysis and MLflow Issues to investigate bad answers and find repeated tool calls across runs and sessions.
- Review answers with domain experts, then run evaluation with the same test cases to measure whether changes improve quality and reduce unnecessary work.

An agent can return a plausible answer while missing an important finding or reading the same source repeatedly. The answer alone won't explain why. Traces show the model and tool calls behind it, so you can investigate the failure, find related cases, and test whether a change helps.

Databricks MLflow is now asupported destinationfor native OpenTelemetry export from the Claude Platform.. With native export to Databricks MLflow, developers using the Anthropic SDKs, the Messages API and Managed Agents can send native traces to Databricks and use MLflow to debug their agents and evaluate changes.

## Native OpenTelemetry, unified in Databricks

MLflow Tracingis built on OpenTelemetry, an open standard for collecting and exporting service signals. A trace records an agent’s execution as individual steps, called spans, such as model requests and tool calls. Claude’s native instrumentation generates these spans and exports them using the OpenTelemetry Protocol.

Databricks receives the spans through Zerobus Ingest and stores them in Unity Catalog tables linked to an MLflow experiment. You can inspect Claude traces alongside traces from other instrumented services, with the same tools for debugging and evaluation. Unity Catalog controls access to the data, which you can also query with SQL. With the combination of Zerobus and Unity Catalog, enterprises can get two crucial benefits: low-latency trace ingestion at high QPS plus the ability to govern access to the sensitive data stored in agentic traces.

![Claude's native OpenTelemetry traces flow into Unity Catalog and Databricks MLflow.](/images/posts/1d064f86d47f.png)

## Connect Claude in 3 steps

### 1. Create an experiment

In Databricks, open theExperimentstab and clickCreate Experiment. UnderTrace storage location, keepUnity Catalogselected. Choose an existing catalog and schema. This creates new MLflow experiments linked to the Unity Catalog table that stores OpenTelemetry traces.Thedetailed setup guidecovers permissions and SQL warehouse requirements.

### 2. Configure native export

Set the Databricks destination using your workspace ID, region, and spans table. TheZerobus connection guideexplains how to obtain a table-scoped OAuth token.

The new native OTel integrations cover Anthropic SDKs, the Messages API, and Managed Agents. For the Anthropic SDK, install the packages below and configure an OTel tracer provider and exporter to create spans for Anthropic SDK calls. FollowClaude Platform OpenTelemetry guideto send traces from the Messages API and Claude Managed Agent your Databricks destination.

Claude Code andClaude Agent SDKalso support OpenTelemetry. To send their traces to the same destination, set these additional variables before starting your application:

### 3. Run a task and inspect the trace

Run your Claude agent, then open Traces in the experiment. Open a trace to inspect its model calls, tool activity, timing, and captured inputs and outputs. Note that inputs and outputs are captured only if you opt in by settingcontent modeto “full”.

![A native OTel trace in Databricks MLflow, with model and tool spans.](/images/posts/9e1da8e6882d.png)

## Use traces to debug and improve your Claude agents

Once Claude traces arrive in MLflow, you can use them throughout development. A trace provides a record for debugging, a case for expert review, and evidence for evaluating the next version of an agent.

### Debug an answer with its trace

An unexpected answer can come from missing context, a failed tool call, or how the model used a tool result. MLflow’sAnalyze traceaction bringsGenie Codeinto the investigation. It examines the recorded execution and helps explain where things went wrong.

Ask follow-up questions about missing context, failed tool calls, or expensive steps, to inspect the relevant context behind the explanation. This helps you decide whether to revise instructions, improve a tool, or change the context available to the agent.

![Click Analyze trace to investigate the selected Claude execution with Genie Code. The analysis identifies the missing release note and repeated read.](/images/posts/25ae647162ee.gif)

### Find recurring problems across traces and sessions

MLflow Issues, available in Beta, usesGenie Codeto identify recurring quality and operational problems. It examines responses, tool calls, timing, errors, and assessments, then groups related findings with links to the supporting traces. Examples include repeated searches that waste tokens, missing arguments that cause tool failures, and responses that don’t follow the required format.

You can schedule detection to keep this analysis running as new traces arrive. Teams can choose how often it runs, use metadata or tags to focus on particular traffic, and customize the types of problems it looks for. After a fix, an issue monitor can track whether the problem returns. MLflow creates a scorer for the issue, evaluates recent traces to establish a baseline, and scores a sample of new traces to measure its frequency over time.

![A manually authored demo issue describes repeated document reads and links to the three affected Claude traces. Issue Detection was not run for this demonstration.](/images/posts/374b54199b73.png)

### Give domain experts the traces to review

Some quality judgments require domain knowledge.MLflow Review Queuesbring that expertise into the development process through selected traces and questions tailored to the agent.

Reviewers can assess the recorded request and response, explain what is missing, and provide an expected answer. Their feedback helps developers refine the agent and establish reference answers for subsequent evaluations.

![A Claude answer awaiting expert review, with the request and response read directly from its trace.](/images/posts/8c06201fbbc1.png)

### Evaluate the change against the same cases

A change to instructions, tools, or skills can fix one failure while introducing another. Traces also make agent behavior measurable. RunMLflow Agent Evaluationon Claude traces to test whether a change to prompts, skills, tools, improve the agent or regress.

For example, the following code executes an LLM judge to examine whether an agent makes redundant tool calls.

When the original and revised agents have run against the same cases, their evaluation runs can be compared using the same judges. ClickComparein MLflow UI to see scores and responses side by side, with the underlying traces available to explain remaining failures.

![Completed evaluations of the same three cases, comparing baseline and revised instructions.](/images/posts/a85adc3843a9.jpg)

The same approach works for checks such as whether an agent followed a required workflow or used the appropriate tools.Testing and Refining Claude Code Skills with MLflowdemonstrates how these checks and their rationales can guide improvements to skills.

### Learn more and get started

The following resources cover connecting Claude to Databricks MLflow and using its traces during development:

[翻译失败，原文如下]

- Claude OpenTelemetry tracing guide: Native OpenTelemetry export configuration for Anthropic SDKs, Messages API, and Claude Managed Agents.
- Tracing in Databricks with Unity Catalog: If you’re new to tracing in Databricks, this guide covers experiment setup, trace storage, and access.
- Detect and monitor issues across MLflow traces: Recurring failure patterns, supporting trace evidence, and ongoing monitoring.
- Evaluating Claude Code skills with MLflow: Behavioral judges and a repeatable process for testing and refining skills.

The first CTA item still needs the dedicated Claude integration-guide URL before publication.

Announcements

---

> 本文由AI自动翻译，原文链接：[Claude Platform now supports native OpenTelemetry observability in Databricks MLflow](https://www.databricks.com/blog/claude-platform-now-supports-native-opentelemetry-observability-databricks-mlflow)
> 
> 翻译时间：2026-11-04 08:50
