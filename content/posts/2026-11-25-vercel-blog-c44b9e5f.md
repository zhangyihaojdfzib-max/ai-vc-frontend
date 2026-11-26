---
title: How Cozey turns its operators into software builders on Vercel - Customers
title_original: How Cozey turns its operators into software builders on Vercel - Customers
date: '2026-11-25'
source: Vercel Blog
source_url: https://vercel.com/blog/how-cozey-turns-its-operators-into-software-builders-on-vercel
author: ''
summary: '[翻译失败，原文如下]


  - Employees outside engineering, including warehouse, finance, and support staff,
  are now building applications and deploying them to Ver...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-26T10:39:32.103624'
---

[翻译失败，原文如下]

- Employees outside engineering, including warehouse, finance, and support staff, are now building applications and deploying them to Vercel
- Finance uses an app it built to review profit and loss weekly instead of monthly
- AdoptingVercel Flagsallowed Cozey to retire a separate tool that cost approximately $80,000 annually
- Six projects, including the storefront, useAI Gateway

Employees outside engineering, including warehouse, finance, and support staff, are now building applications and deploying them to Vercel

Finance uses an app it built to review profit and loss weekly instead of monthly

AdoptingVercel Flagsallowed Cozey to retire a separate tool that cost approximately $80,000 annually

Six projects, including the storefront, useAI Gateway

Cozeyis a Canadian furniture company that makes modular sofas customers can configure for their homes. It runs its storefront and most of its back-office applications on Vercel. Warehouse, finance, and customer support employees now securely deploy their own apps on that same platform.

![Cozey Furniture](/images/posts/3147a1747325.jpg)

Cozey Furniture

## Copy link to headingTurning everyday problems into working applications

CEO Fred Aubé encourages employees to solve problems they encounter without waiting for another team to take them on. Sam Morrison, VP of Digital, saw teams reach the limits of what they could prototype in an AI chat. Employees used coding agents to build web apps. With Vercel, they could deploy an app themselves and give coworkers a link to a working tool.

In the warehouse, a coordinator built a live floor plan that shows where boxes sit and what staff are doing. Sam says engineering would not have prioritized that project. Finance built its own app to track profit and loss and now uses it to review performance every week instead of once a month.

A customer support representative built an app that uses AI to generate images of Cozey furniture in a customer’s own room. In October, Cozey planned to make the tool available to shoppers.

Sam says a new app appears almost every week.

## Copy link to headingExtending Vercel from the storefront to the business behind it

Sam estimates that the Atmosphere sofa collection alone has about 1.2 million possible configurations. Cozey worked with an agency specializing in Next.js to rebuild its storefront on Vercel. With a custom front end, the team could decide how shoppers explore those options.

Cozey usesFluid computefor functions on the storefront. It runs internalPython backendsand the Cozey Operating System, or C.O.S., on Vercel. Teams use C.O.S. to forecast orders, manage warehouse and retail operations, review finances, and track business performance. Operating margin depends in part on how quickly furniture moves from incoming containers to customer shipments.

Each C.O.S. pull request gets aVercel Preview Deployment, giving the team a working application to test before release. Cozey’s engineers reported that with caching, builds on Vercel took a couple of minutes. They also share preview links with Fred so he can try changes and give feedback.

The team uses Vercel Flags to control how new features reach users, replacing a separate tool that cost approximately $80,000 annually. After release, performance metrics on Vercel give the team a common reference for checking how applications are running.

When Cozey launched in Australia, the team had regional backend work to do. For the storefront on Vercel, Sam says, “it wasn’t even a conversation.”

## Copy link to headingManaging access as more people build

As more employees began building, Cozey needed to manage who could open their applications and who could deploy and maintain them. An employee once deployed an app that anyone on the internet could open. For internal apps that had shipped without appropriate authentication, Sam turned onaccess protection on Vercel.

“It saved us from some pretty serious privacy risks,” says Sam.

Cozey usessingle sign-onso members of its Vercel team can sign in with company credentials. The company manages team membership through groups in its employee directory withDirectory Sync.

## Copy link to headingGiving AI applications a common way to access models

As more teams built with AI, Sam saw them repeating the work of connecting to models. Six Cozey projects, including the storefront, send model requests throughVercel AI Gateway. Cozey’s engineers use it to call models from their code editors, too. Sam wants all of Cozey’s model requests to go through Gateway.

AI Gateway gives teams one interface for different model providers. If a provider is unavailable, the gateway canroute the request to another providerthat serves the same model. It adds no markup to provider token prices. Sam describes the added cost of routing requests through it as “basically $0 in additional overhead.”

The company is also developing what it calls the Agentic Mesh, a system to coordinate AI use across internal applications and customer experiences. The coordinating service is being built on AWS, with AI Gateway planned for model requests and Vercel for application deployment. It is intended to help teams decide which models to use and where to run applications, while giving engineering visibility into AI usage and costs.

## Copy link to headingWhat's next

Sam says engineering wouldn’t have prioritized a live map of the warehouse floor. The coordinator who needed to see where the boxes were could make a different call, build the map, and share it with the people moving them. When the digital team sees an idea worth taking further, it has a working app to build on.

Cozey chose a custom storefront on Vercel so it could decide how shoppers explore its furniture. Sam’s next goal is for employees outside engineering to share that control. If shoppers keep asking the same question about a sofa, the support rep who hears it could put the answer on the product page.

## Contributors

Kevin Corbett

---

> 本文由AI自动翻译，原文链接：[How Cozey turns its operators into software builders on Vercel - Customers](https://vercel.com/blog/how-cozey-turns-its-operators-into-software-builders-on-vercel)
> 
> 翻译时间：2026-11-26 10:39
