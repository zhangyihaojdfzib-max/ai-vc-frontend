---
title: 'Genie One Accuracy: Why Curated Agents Need Governed Context'
title_original: 'Genie One Accuracy: Why Curated Agents Need Governed Context'
date: '2026-11-19'
source: Databricks Blog
source_url: https://www.databricks.com/blog/genie-one-accuracy-why-curated-agents-need-governed-context
author: ''
summary: '[翻译失败，原文如下]


  - Databricks Genie One is most accurate when it uses curated Genie Agents together
  with modeled knowledge, the governed business context ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-20T09:31:28.287877'
---

[翻译失败，原文如下]

- Databricks Genie One is most accurate when it uses curated Genie Agents together with modeled knowledge, the governed business context defined in Unity Catalog. Across 125 questions about a fictional insurer, Genie One scored 93–95% using curated Genie Agents together with governed business context (Metric Views, Domains/Subdomains and Pages), 83% with either agents or the governed layer alone, and 64% with tables alone.
- Agents and the governed layer fix different problems. Metric Views, Domains, Subdomains, and Pages help Genie One answer definition questions that would otherwise rely on tribal knowledge, while agents are needed for questions that require answers from unstructured data such as PDFs.
- Define each business measure once, in a certified Metric View, and use a Page to explain when it applies. In a separate change test, updating one Metric View and its Page moved all 12 related Genie One answers to the new definition without any agent edits.

Ask Finance and Underwriting whether the loss ratio improved from 2024 to 2025, and you will get two contradictory answers that are both correct. In a fictional commercial auto insurer we built for this test, Finance reported an 8.2 percentage-point deterioration, and Underwriting reported a 1.5 percentage-point improvement. Neither was wrong. Finance tracks the calendar year net of reinsurance, so an adverse reserve development on an older claim shows up in today's numbers. Underwriting looks strictly at the policy year, gross of reinsurance and excluding catastrophes, because that's the baseline used to set rates. Reserving, meanwhile, relies on a third metric entirely: the accident-year ultimate loss ratio.

![image2.png](/images/posts/0ae410f8a4f9.png)

The SQL can be perfectly correct and still produce an answer that doesn't make sense for the person asking. The challenge is knowing which business definition to apply when the same term has several valid definitions, while keeping shared facts, such as total policies written, consistent. This is the problem we wanted to explore with Genie One.

Genie One, powered byGenie Ontology(now Generally Available), brings this business context into the analytics experience. Genie Ontology learns from the work teams already do, automatically capturing business logic, calculations, and relationships from existing dashboards, queries, notebooks, and semantic models as Ontology Snippets. This learned knowledge is complemented by modeled knowledge: explicitly defined, governed business concepts represented in Unity Catalog through certified Metric Views, Domains and Subdomains, and Pages. In this study, we refer to this modeled knowledge as the “governed layer”.

Together, learned and modeled knowledge give Genie a richer understanding of how an organization works. Teams can build on the knowledge already captured from their existing assets, while using modeled knowledge to establish authoritative definitions for the business concepts where consistency and precision matter most. There is no need to model every concept upfront.

This study explores a different aspect of Genie Ontology than theTuring benchmarkdescribed in ourGenie Ontology GA announcement. While the benchmark compared the accuracy and efficiency of Genie with Genie Ontology against leading frontier agents, our study isolates the contribution of modeled knowledge: how governed Metric Views and Pages complement learned knowledge and curated agents to help Genie One interpret business definitions and deliver consistent answers.

To explore this, we built four Genie Agents, one each for Finance, Reserving, Underwriting, and Claims. They used the same tables, but each had its own team's definitions, example queries, and documents. Each did well on its own. We wanted to know what happens when Genie One becomes the entry point: does it route to the right agent and use the right definition, and what does it need to do that reliably?

We tested four configurations to find out.

- Tables only: no agents and no governed context in Unity Catalog.
- Curated agents:each agent had its team's definitions, business rules, and documents.
- Governed layer, no agents:Metric Views, certification, Domains, Subdomains and Pages in Unity Catalog, with no Genie Agents
- Curated agents with a governed layer:the same agents plus the same governed business context.

Tables alone scored 64%. Curated agents and the governed layer each reached 83%, but they weren't good at the same things. Adding curated agents improved document-based answers. Adding the governed layer improved answers that depended on business definitions. Neither was enough on its own to cover both needs. With both in place, accuracy reached 93–95%, across two runs. The combined setup also scored 93% on loss-ratio questions and 97% on questions that required both documents and structured data.

To see whether this pattern held outside the insurance sector, we repeated the comparison using a fictional retailer. There, the governed layer raised accuracy from 54% to 82% when added to the curated agents.

![image1.png](/images/posts/aeb1e60e913e.png)

## Why Genie One can miss what an agent already knows

Genie One doesn't simply choose an agent and let it answer every question. It can use governedUnity Catalog Semanticssuch asMetric Views,Domains and subdomains, andPages, or route a question to a relevant Genie Agent. If it doesn't find a suitable match, it searches the workspace. There, it may infer which data to use from tables or volumes you use often, or from your earlier conversations.

When Genie One answers a question using its own context, it doesn't automatically inherit the instructions configured inside each agent. Those instructions apply only when Genie One routes the question to that agent. So an agent can be well curated and still contribute little if Genie One answers the question differently.

## How we built the test

### The insurance business

We created a fictional commercial auto insurer with:

- 8,000 policies and 7,482 claims.
- Claim values updated quarterly.
- Reserves for claims that had not yet been reported (incurred but not reported, or IBNR).
- Two reinsurance contracts and three catastrophe events.
- A recent increase in California injury claim costs.

The four agents shared the same underlying tables. Each also had access to its team's folder of documents, with 14 PDFs across the four folders.

We also planted two misleading documents to test robustness. One was an early draft of the reserve committee minutes reporting a $4.1 million increase in reserves; the approved minutes in the same folder reported a $5.28 million increase. The other was a vendor newsletter containing a hidden instruction to report the loss ratio as 55%, a simple prompt-injection test.

We then placed three look-alike tables next to the real definitions: analytics_loss_ratio_v2, analytics_loss_ratio_test, and a personal copy, finance_lr_calendar_quarter_net_jdoe.

The agents were configured with their teams' formulas, business rules, and SQL example questions. We tuned them on a separate set of practice questions and then froze them, using the same versions across all configurations that included agents.

There are multiple ways to make enterprise documents available to Genie, depending on where the content lives and how teams need to access it. In this experiment, we stored team-specific PDFs in Unity Catalog Volumes and made them available to the corresponding Genie Agents through content search. When information is spread across business applications such as Google Drive, SharePoint, Jira, or Confluence,Genie Searchprovides a broader enterprise search experience. It combines indexed content from connected applications with live retrieval through MCP, bringing results together with Databricks assets in a single experience. It also respects the permissions of the source systems, so users only see content they are authorized to access.

[翻译失败，原文如下]

For the governed layer, we set up:

- Metric Viewscontaining the teams' calculations: three loss-ratio definitions and the relevant team-specific versions of premium, claim frequency, and severity.
- Certificationmarking the intended Metric Views and agents as trusted and the decoy assets as deprecated.
- Domains and Subdomainsorganizing the assets around the Commercial Auto business. Shared facts lived in the main Domain, while each team's definitions, documents, and agents lived in its own Subdomain.
- Pagesproviding short, governed explanations of business terms and linked to the tables and Metric Views they described.

## The questions and scoring

The insurance benchmark contained 125 questions, each with an expected answer calculated independently in SQL.

The questions covered simple lookups, explicitly named business definitions, ambiguous questions such as "What's our loss ratio?", questions requiring an explanation, questions that the available data couldn't answer, and questions that combined documents with structured data. We also tested follow-up questions and the two planted documents.

We took several steps to make the results more meaningful. Genie One answered every question three times, with a fresh service principal for each run so earlier conversations couldn't carry over, and every answer was logged in MLflow. When a key result was close, we repeated the whole setup with a new identity. We report 95% confidence intervals from 2,000 bootstrap resamples, keeping each question's repeats together, because Genie One can recall earlier answers. Two AI judges from different model families extracted the headline number, the definition used, and the facts covered, and fixed rules decided whether each answer was right. The judges agreed on 95–99% of answers. Before each run, every agent had to answer at least 85% of its basic questions correctly on its own.

## Where the accuracy gains came from

Here’s the overall accuracy score, followed by a breakdown by question category, measured with Genie One.

What the governed layer added.With curated agents alone, Genie One often answered definition questions on its own and never saw the formulas in the agents' instructions. Published Pages are visible to Genie One across the whole account, so the closest definitions it could find were Pages other people had written for unrelated projects. It relied on those in 49% of its answers. The governed layer provided Genie One with a better match: certified Metric Views for each calculation and our own Pages for each contested term, organized within the Commercial Auto Domain. Reliance on other projects' Pages fell to 11%, and every definition question in our benchmark came back right.

We also looked at whether Genie One routed definition questions to an agent or answered them directly.

With curated agents alone, the agents knew the answer, but Genie One answered about four in ten definition questions itself and got most of those wrong. With the governed layer, it got them right either way. We ran that setup twice from scratch with different identities, and routing shifted dramatically: Genie One handed 74% of answers to an agent in one run and 19% in the other, with about the same accuracy. Routing isn't deterministic, but with the governed layer it stopped mattering. Answering directly, Genie One read the certified Metric Views and Pages. Routing to an agent, the agent applied a formula that matched the same Metric View. Every path led to the same definition.

The planted documents didn't change any answers.No answer in any setup reported the 55% loss ratio from the injected vendor newsletter, and none used the draft reserve figure.

Without the governed layer, routing decided whether you got the right answer. The lesson is to design for whichever path Genie One takes: put each definition where every path can reach it, and test through Genie One more than once before trusting a result.

What the agents added.Without agents, document questions fell to the tables-only level. Of the 18 questions that worsened without agents, 12 required a team document, such as the litigation review, the reserve committee minutes, or an underwriting recommendation. In this setup, the agents were Genie One's only route to those documents, because the PDFs were available only through agent content search and none of the Pages linked to them. Without agents, Genie One also forecast a 2027 loss ratio for every repeat, rather than saying the data didn't cover 2027. That limitation was written in the table descriptions and the agents' instructions, but not on the Metric Views Genie One was reading, so it never saw it.

## What each part of the governed layer contributed

The comparison above adds the whole governed layer at once. To understand what each component contributed, we ran a separate series of tests, adding one component at a time.

This second experiment started with four agents whose loss-ratio formulas disagreed. From the second step onward, we moved the formulas into Metric Views and reduced each agent to a few behavior rules and two example queries. These agents were configured differently from the fully curated agents in the main comparison, so the results below shouldn't be compared directly with the earlier table.

![image3.png](/images/posts/8e6a30e6db69.png)

- Metric Views fixed the formulas.The same step also cut the agents back to a few behavior rules. Loss ratio questions went from 56% to 83%, and definition questions from 66% to 90%.
- Certification helped signal which assets to trust, but didn't independently improve accuracy.The overall score dipped from 90% (84–94%) to 83% (76–89%), but the intervals overlap, so we can't say the drop is real. At the same time, decoy-table use fell from 9% to 4% of answers, and Genie One explicitly referred to a certified definition in 22% of answers. We see certification as a useful trust signal that works alongside Domains and Pages, not as a feature that makes answers correct on its own.
- Domains and Pages, added last, helped Genie One identify which definition applied.Vague question accuracy increased to 94%, definition questions reached 100%, and decoy use dropped from 4% to zero. A Metric View tells Genie One how to calculate a number; the Domain and Pages help explain whose measure it is and how it fits into the business.

Document questions varied more between runs than the other categories. There were only 12, so changing two questions could move the score by about 15 percentage points. The original agents' instructions said where to find litigation status, and Genie One routed both litigation questions to the Claims agent and got them right. Once we trimmed those instructions, the questions usually failed until we added a Page defining "in litigation."

## The same question can have different correct answers

We also tested whether Genie One could account for the user's team when interpreting a question.

We created two identities, one for Finance and one for Underwriting. Each told Genie One its team once, and Genie One Memory retained that information. Both identities then asked the same 12 questions in new conversations: seven where the correct answer depended on the team and five that asked for straightforward facts.

Every answer explained which team's definition it was using. This shows learned and modeled knowledge working together, because Genie One combined what it remembered about each user with the definition that team had modeled. Both identities had exactly the same data access, so the difference came from the team context Genie One remembered, not from differences in what the identities could see. This was a test of business context, not access control. Remembering someone's team doesn't replace permissions or row-level security; those still need to be enforced separately.

## What happens when a business definition changes?

[翻译失败，原文如下]

Business definitions don't stay fixed. We wanted to see how much work it would take to update one without breaking the others.

Partway through, Underwriting decided its loss ratio should also include the legal cost of defending claims. We updated the Underwriting Metric View and added one sentence to its Page. We didn't change any agent instructions. Then we asked 12 questions about the Underwriting loss ratio through Genie One, with the curated agents and the governed layer in place.

Every answer used the new definition. Eight questions about definitions we didn't change stayed right. In the curated-only setup, the same change would have meant finding and editing the formula in seven places across four agents' instructions.

One caveat: the agents still held the old formula. Asked directly outside Genie One, they used it in 92% of answers with no warning and would keep doing so until someone updates each agent. Centralizing definitions reduces duplication, but any logic left in agents still needs maintenance.

## Does the same approach work outside insurance?

We repeated the main comparison with a fictional retailer. Finance, Merchandising, and Marketing each had a different definition of revenue. We asked, "Did revenue grow in 2025?"

- Merchandising, which counts everything ordered before discounts, reports growth of 13.6%.
- Finance, which counts revenue when orders ship, after discounts and refunds, says it fell 9.4%.
- Marketing, which counts completed orders before returns, says it stayed flat.

A holiday sale and a jump in clothing returns explain the gap, and all three are right.

The benchmark contained 49 questions, making this a smaller check of the pattern rather than a second full study.

The curated retail agents worked well on their own. Through Genie One, though, they got about half the questions right, because nothing in Unity Catalog said what revenue meant for each team or which tables belonged to the business. With the governed layer, definition accuracy jumped from 31% to 100%, and overall accuracy rose to 82%.

## What we recommend

Based on these experiments, keep your curated agents and add a governed layer underneath them. The key decision is where each piece of information belongs:

A few practical lessons stood out:

1. Start with definitions that mean different things to different teams, especially those that exist as tribal knowledge within a single team. Genie One already handles universally agreed-upon facts well.
2. Define each measure once. Put the official calculation in a certified Metric View rather than maintaining the same formula in several agent instructions. In our tests, Metric Views and Pages drove the gains in accuracy. In our step-by-step test, certification steered Genie One away from look-alike decoy tables, cutting their use from 9% to 4%, and Domains and Pages took it to zero.
3. Use Pages to explain the business context. Link them to the certified tables and Metric Views they describe. On each Page, define the scenarios where a calculation applies and the ones where Genie One should avoid it. A definition is more useful when Genie One can connect it to the underlying data.
4. Keep agents focused on what they do best. Team-specific documents, Domain knowledge, and behavior rules still matter. The governed layer doesn't replace that context, particularly when a question depends on information that isn't represented in tables or Metric Views.
5. Test through Genie One, not just through individual agents. An agent that answers well on its own won't help if Genie One doesn't route to it, so measure the end-to-end experience before and after each change.

To apply this to your own data, start with the terms your teams define differently, add them to a Domain/Subdomain with Metric Views and Pages, and measure the change through Genie One. TheGenie Ontology documentationexplains how the pieces fit together, andour guide to operationalizing Genie Ontology in your data stackwalks through setting them up step by step.

Best Practices

### Get the latest posts in your inbox

Subscribe to our blog and get the latest posts delivered to your inbox.

---

> 本文由AI自动翻译，原文链接：[Genie One Accuracy: Why Curated Agents Need Governed Context](https://www.databricks.com/blog/genie-one-accuracy-why-curated-agents-need-governed-context)
> 
> 翻译时间：2026-11-20 09:31
