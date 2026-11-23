---
title: Set budgets for projects and products in Spend Management - Vercel
title_original: Set budgets for projects and products in Spend Management - Vercel
date: '2026-11-16'
source: Vercel Blog
source_url: https://vercel.com/changelog/set-budgets-for-projects-and-products-in-spend-management
author: ''
summary: '[翻译失败，原文如下]


  ![The Spend Management page listing team, project, product, and organization budgets
  (dark)](/images/posts/4e7ce626262b.jpg)


  ![The Spend...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-23T10:32:17.312555'
---

[翻译失败，原文如下]

![The Spend Management page listing team, project, product, and organization budgets (dark)](/images/posts/4e7ce626262b.jpg)

![The Spend Management page listing team, project, product, and organization budgets (dark)](/images/posts/9874c4e437ed.jpg)

Spend Managementnow supports budgets for individual projects and products, alongside existing team budgets.

- Project budgets:Track spend for one project and optionally pause its production deployments when the budget is reached, without pausing other projects.
- Product budgets:Track spend on one product, such as Fast Data Transfer, across your team.

Project budgets:Track spend for one project and optionally pause its production deployments when the budget is reached, without pausing other projects.

Product budgets:Track spend on one product, such as Fast Data Transfer, across your team.

Only team and project budgets support automatic pausing of production deployments.

Open the newSpend Management pageto manage budgets, view spend for the current billing cycle, and see which thresholds have been reached. Vercel sends notifications at 50%, 75%, and 100% of each budget.

You can also manage budgets with theVercel CLI:

```
12vercel billing budgets list3
45vercel billing budgets set --project my-app --amount 100 --pause6
78vercel billing budgets set --product "Fast Data Transfer" --amount 50
```

List budgets and set project or product budgets with the Vercel CLI.

Spend Management is included at no additional cost for Pro teams and Enterprise teams on Flexible Commitment plans. Customers in theOrganizations private betacan also set a budget across all teams in their organization.

Learn more in theSpend Management documentation.

---

> 本文由AI自动翻译，原文链接：[Set budgets for projects and products in Spend Management - Vercel](https://vercel.com/changelog/set-budgets-for-projects-and-products-in-spend-management)
> 
> 翻译时间：2026-11-23 10:32
