---
title: Bulk migrate your dashboards to AI/BI with Genie Code
title_original: Bulk migrate your dashboards to AI/BI with Genie Code
date: '2026-11-19'
source: Databricks Blog
source_url: https://www.databricks.com/blog/bulk-migrate-your-dashboards-aibi-genie-code
author: ''
summary: '[翻译失败，原文如下]


  - Migrate an entire folder of reports with a single command. Put your Tableau or
  Power BI files in a Unity Catalog volume, open a draft d...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-21T09:25:35.301294'
---

[翻译失败，原文如下]

- Migrate an entire folder of reports with a single command. Put your Tableau or Power BI files in a Unity Catalog volume, open a draft dashboard, and run /importBI in Genie Code. The agent finds every report, pairs workbooks with their data sources, and builds AI/BI Dashboards and metric views in the catalog and schema you choose.
- Track the batch while it runs. Reports are queued and processed in batches, reusing existing Unity Catalog tables, views, and metric views where possible. A status card shows each report as Queued, Running, or Completed, and you can stop a single report or the entire batch.
- Build a reusable semantic layer as you migrate. Promote the metric views created during migration to Unity Catalog, or ask for Unity Catalog metric views up front. Later migrations, other dashboards, Genie Agents and notebooks can then reuse the same governed definitions.

In our previous post,Migrate Your Dashboards to AI/BI with Genie Code, we walked through moving a single Tableau or Power BI report onto Databricks AI/BI with the/importBIskill in Genie Code. That one-report-at-a-time flow is perfect for a pilot — but most organizations have hundreds of reports built up over years, and migrating them individually turns a strategic modernization effort into a months-long manual grind.

Bulk migration of dashboards changes that. You can now point the migration agent at an entire folder of reports and have them converted toAI/BI Dashboardsin a single run — no more kicking off migrations report by report.

This guide is for you if:

- You've already tried/importBIon a report or two and are ready to scale up.
- You have a backlog of Tableau or Power BI reports — dozens or hundreds — that you want to move to Databricks AI/BI.
- You want a repeatable, folder-at-a-time migration process instead of a report-by-report one.

## What is bulk migration?

Bulk migration extends the Databricks AI/BI migration experience so that instead of importing one report at a time, you can process many reports together from a single command. The migration agent reads your source BI files, generates the corresponding AI/BI Dashboards on Databricks, and maps them to the target catalog and schema you specify.

This feature is now generally available, and so it's ready to use in your workspace today. Before you begin, check thatpartner-powered AI featuresare enabled at both the account and workspace levels.

## Why it matters

For teams standardizing on Databricks AI/BI, bulk migration removes the single biggest bottleneck in a large-scale dashboard migration: the sheer repetition of moving reports one at a time. By migrating an entire folder of Tableau or Power BI reports into a single run — and landing them directly in your chosen catalog and schema — you can shift a migration project from a manual backlog to a repeatable, folder-at-a-time workflow.

## A practical bulk migration playbook

The playbook below walks through a bulk migration end to end. It is grouped into three phases:

## 1. Export your BI reports

Export each Tableau or Power BI report you want to migrate to a supported file type. This includes: .twb, .twbx, .tds, .tdsx, .pbit, or .tmdl. TheTableau export documentationandPower BI report templatesguides walk you through the export.

Tip: Working with a Tableau workbook that connects to a published data source? Export that data source as well (.tds or .tdsx) and keep it next to the workbook.

## 2. Stage the files in a Unity Catalog volume

Place the BI report files you want to migrate into adirectory within a Unity Catalog volume. Keeping them together in one folder lets you migrate them in a batch. A bulk run always picks up its files from the volume; dragging files straight into the chat only works for one-off, single-report imports.

## 3. Start the bulk import from a draft dashboard

From a draft dashboard, open Genie Code and submit:

/importBI <path/to/volume/directory>

![image1.png](/images/posts/efbb77622fba.png)

Above: Running /importBI against a volume directory from a draft dashboard.

Pointing the command at the directory (rather than a single file) triggers the bulk flow across all reports in that folder.

If you prefer natural language, a request such as “Migrate every Power BI report in /Volumes/finance/bi/reports to AI/BI Dashboards” works just as well.

You can also name specific files instead of a whole folder: “Migrate Tableau reports Dashboard1.twb, Dashboard2.twb in /Volumes/finance/bi/reports to AI/BI Dashboards”.

Finally, you should add guidance that applies to the entire batch — for example, asking Genie Code to "build only the metric views".

## 4. Choose the target catalog and schema

The agent recognizes the batch and lists the reports it found in the volume, matching each Tableau workbook to its companion data source file on its own and checking with you if a pairing is unclear. It then prompts you for the destination catalog and schema so the migrated dashboards' metric views and SQL views land in the right place.

![image8.png](/images/posts/0144eabf88c7.png)

Above: Genie Code lists the reports it found and asks for the target catalog and schema.

After you've checked the file list and given the go-ahead, the bulk migration kicks off, and a status panel shows each report as it starts. Reports are queued and processed a few at a time, and each report reuses existing Unity Catalog tables and views where it can before creating new ones.

Note: For the current limits on the number and size of files supported in a single bulk import, always refer to the public documentation on/importBI.

## 5. Track the batch

A status card in the chat keeps a running tally of the batch, with each report marked as Queued (not started), Running, or Completed (session ended). You can stop an individual report, or halt everything still in flight, from the same card.

![image7.png](/images/posts/9743b1b6ce39.png)

Above: The status card tracks every report in the batch.

Because each report runs in its own background job, there's no need to keep the tab open — come back to the original chat in your Genie Code history at any time to see how the batch is progressing.

## 6. Review each report

Each file name on the status card links to that report's own Genie Code conversation, which opens in a separate tab. If a run stops to ask a question, answer it there, and the migration picks up where it left off.

![image5.png](/images/posts/fd95815ca891.png)

Above: A run that paused to ask for input. In this example, the published data source behind the workbook.

## 7. Follow the migration plan

As with a single-file/importBImigration, each report runs through the Genie Code planning phase — for example, parsing and assessing the workbook, enumerating the semantic layer, creating metric views, building the dashboard pages, and validating the migration.

![image2.png](/images/posts/323bb8f4a1c2.png)

Above: The migration plan for a single report, tracked step by step.

## 8. Refine and polish

Once the plan execution completes, you can view the finished AI/BI dashboard produced by the migration. You can further enhance or customize it with follow-up Genie Code prompts. Every Genie Code response can be undone as a single step, so it's safe to experiment, and you can even ask Genie Code to beautify the dashboard's look and feel.

![image6.png](/images/posts/97d15d018be1.png)

Above: A finished AI/BI dashboard produced by the bulk migration.

## 9. Validate against the original dashboard

Before you retire a source report, check that the migrated dashboard gives the same answers as the original.

[翻译失败，原文如下]

1. Capture a reference screenshot.In Tableau or Power BI, set a known filter state (for example, the last full quarter and one region) and take a screenshot in which the KPI tiles, totals and a couple of key charts are clearly readable.
2. Match the filters in AI/BI.Apply the same filters and date range to the migrated dashboard so you're comparing like with like.
3. Upload the screenshot to the report's Genie Code conversation and ask it to reconcile:“Here's a screenshot of the original report filtered to Q3 2026, EMEA. Apply the same filters to this dashboard, compare every KPI and chart total with the screenshot, and list any values that don't match along with the likely cause.”“For each mismatch, show the metric view definition or SQL behind the number and suggest a fix.”“Check that filters and parameters behave like the original: same default values, same cross-filtering, and the same handling of nulls and 'All'.”
4. Look into differences before accepting them.Gaps often stem from data freshness (an extract compared with live Unity Catalog tables), differing default filters, or calculation semantics such as distinct counts, level-of-detail expressions, or time intelligence. They don't always mean a migration error.
5. Record the sign-off.For business-critical dashboards, keep the screenshot and the reconciliation result as evidence before you switch users over.

1. “Here's a screenshot of the original report filtered to Q3 2026, EMEA. Apply the same filters to this dashboard, compare every KPI and chart total with the screenshot, and list any values that don't match along with the likely cause.”
2. “For each mismatch, show the metric view definition or SQL behind the number and suggest a fix.”
3. “Check that filters and parameters behave like the original: same default values, same cross-filtering, and the same handling of nulls and 'All'.”

Tip:If you've connected Tableau or Power BI via a read-only MCP connection (see the cheat sheet below), Genie Code can check the numbers against the live report directly rather than reading values from a screenshot.

## Your best-practice cheat sheet

Set things up well before you run/importBIto get the most faithful migration on the first pass:

• Set up a read-only MCP connection to Tableau or Power BI so Genie Code can use the live report as the source of truth, validating results against the original rather than relying solely on the exported file, which meaningfully improves accuracy.

- Connect with your Databricks account team to get set up with the Tableau or Power BI MCP connection.

• Migrated dashboards map to Unity Catalog tables (via Lakeflow Connect, Lakehouse Federation, or existing UC tables).

- If a referenced source isn’t present, the agent may adapt to the closest available table, so confirm that each dashboard is wired to the correct source.
- You can also proactively prompt Genie Code to use the right sources.

Example:“The source tables for this report as available in dev.finance schema”

“Use prod.finance.table1, prod.finance.table2 and prod.finance.mv_revenue as the source for this report”

• Tableau imports produce dashboard-scoped (local) metric views by default, while Power BI imports produce Unity Catalog metric views.

- Once you're happy with the local ones,promote them to Unity Catalogso later migrations, other dashboards, Genie Agents, and notebooks can reuse them — or ask for Unity Catalog metric views up front in your prompt. |

• File count and size limits can change, so always refer to thepublic /importBI documentationfor the current limits.

- Bulk migration reads its inputs from a Unity Catalog volume, so stage all files there. |

## Further resources

- AI/BI and Genie One release notes (2026): the latest features and improvements in AI/BI, including updates to /importBI and Genie Code for dashboard authoring.
- Unity Catalog Semantics Patterns: tested reference patterns for building metric views in Unity Catalog — time intelligence, semi-additive measures, ranking, currency conversion, and segmentation — useful when refining or promoting the metric views created by your migration.

## Conclusion

Moving hundreds of Tableau or Power BI reports to Databricks AI/BI no longer has to mean hundreds of individual migrations. With bulk migration, you prepare a folder of reports once, run a single/importBIcommand, and let Genie Code work through the batch in the background while you review and refine each result.

If you're planning a BI modernization effort, upload a folder of reports to a Unity Catalog volume and try/importBIfrom a draft dashboard to see bulk migration in action.

### Ready to bring your Tableau and Power BI reports to AI/BI?

If you’re ready to get started, just put your report files in a Unity Catalog volume, open a draft dashboard, and run/importBIin Genie Code.

For step-by-step details, see the documentation onimporting BI files with Genie Code. If you're new to AI/BI, start with our earlier post:Migrate your Dashboards to AI/BI with Genie Code.You should also read thebulk migration product documentation.

Q: What is bulk migration for Databricks AI/BI?

A: Bulk migration allows you to process many Tableau or Power BI reports together in a single run, instead of importing one report at a time. The migration agent reads your source BI files, generates the corresponding AI/BI dashboards on Databricks, and maps them to your target catalog and schema.

Q: What file formats does bulk migration support?

A: Bulk migration supports .twb, .twbx, .tds, .tdsx, .pbit, and .tmdl file formats from Tableau and Power BI reports.

Q: Where do I need to store my BI report files for bulk migration?

A: Store all the BI report files you want to migrate in a directory within a Unity Catalog volume. You can then point the /importBI command at that directory to trigger the bulk migration workflow.

Q: How do I start a bulk migration in Genie Code?

A: From a draft dashboard, open Genie Code and submit the command /importBI <path/to/volume/directory>. You can also use natural language, such as "Migrate every Power BI report in /Volumes/finance/bi/reports to AI/BI dashboards."

Q: What do I do after the bulk migration completes?

A: After completion, you can review each migrated dashboard, compare it with the original report, and use Genie Code prompts to refine or customize the dashboard. You can also promote local metric views to Unity Catalog so they can be reused by other dashboards and applications.

Customers,Best PracticesandData Warehousing

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Bulk migrate your dashboards to AI/BI with Genie Code](https://www.databricks.com/blog/bulk-migrate-your-dashboards-aibi-genie-code)
> 
> 翻译时间：2026-11-21 09:25
