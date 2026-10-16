---
title: Vercel for Enterprise
title_original: Vercel for Enterprise
date: '2026-10-15'
source: Vercel Blog
source_url: https://vercel.com/blog/vercel-for-enterprise
author: ''
summary: '[翻译失败，原文如下]


  AI adoption in the enterprise is growing rapidly, and expanding beyond engineering
  users.


  In the last three months, token usage by enter...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:41:03.950407'
---

[翻译失败，原文如下]

AI adoption in the enterprise is growing rapidly, and expanding beyond engineering users.

In the last three months, token usage by enterprise companies on AI Gateway has quadrupled, andOpenAI recently reportedthat from August 2025 to June 2026, non-developer Codex users grew 189x.

Our customers call these builders citizen developers. They know their part of the business better than anyone else, and with AI they can create the software they need to ship work faster and deliver better customer experiences.

Building has never been easier, but that also means that control and governance have never been harder. Employees are using AI toolswhether they are approved or not, and if a citizen developer vibe codes a login page incorrectly, private data can reach the public internet.

Enterprise leaders have to figure out how to let everyone build, without giving up security or control.

### Copy link to headingEnterprise Apps and Agents

We built Enterprise Apps and Agents to solve these challenges at Vercel, and in June, wemade it availableto our customers. Enterprise Apps and Agents is a central control plane for governing every builder, app, agent, token, and dollar.

Today, we are expanding the platform:

- Bring Your Own Cloud(BYOC) on AWSis generally available, giving you the full Vercel developer experience, while keeping compute and data inside your AWS boundary.
- Enterprise-Managed Authorizationthrough Vercel Connect is launching in public beta, giving agents the ability to access connected services on behalf of employees through your IdP.

Bring Your Own Cloud(BYOC) on AWSis generally available, giving you the full Vercel developer experience, while keeping compute and data inside your AWS boundary.

Enterprise-Managed Authorizationthrough Vercel Connect is launching in public beta, giving agents the ability to access connected services on behalf of employees through your IdP.

## Copy link to headingA single control plane for governing enterprise AI

Enterprise Apps and Agents gives you a single deployment destination for both engineers and citizen developers, with central governance over access, providers, models, data retention, token budgets, integrations, and policies, managed through your existing IdP.

![Vercel is a central control plane for governing AI in the enterprise](/images/posts/cfd472d9d2ba.jpg)

![Vercel is a central control plane for governing AI in the enterprise](/images/posts/2d2e5411b433.jpg)

Vercel centralizes AI governance so that company policies can be applied consistently across control domains.

Control domain

Vercel controls

Deployment governance

Enterprise Managed UsersandRBAC

Access governance

Vercel Passport,Deployment Protection, andVercel Firewall

Integration and data governance

Vercel ConnectandEnterprise-Managed Authorization

Model and token governance

AI Gateway, includingUS-only inferenceandbudget controls

Apps and agents run on the same infrastructure that powers billions of production deployments, and Vercel gives you a single place forobservabilityand security monitoring across every project, throughanalytics,audit logs, and theSecurity Dashboard.

Secure Computeprovides private connectivity to enterprise systems, while BYOC on AWS lets your application functions run in your own AWS account under your permissions and network controls.

### Copy link to headingDeployment governance

Citizen developers and engineers use different tools. A marketer might use ChatGPT to build a landing page, an analyst might use Claude Code to run queries and build a report, and an engineer might use Codex, OpenCode, or fx.

No matter the harness, Vercel gives you a single deployment target, and connects to your existing IdP, so you can control who creates deployments.

#### Copy link to headingHow Klaviyo's built a secure internal app platform

Before Vercel, shipping a simple internal app at Klaviyo took two weeks of chasing IT, opening tickets for engineering, and following up with the platform team. They built an internal app-building platform on top of Enterprise Apps and Agents, and now anyone in the company can deploy an idea in three minutes. In their first two weeks on Vercel, 512 employees deployed 356 apps.

### Copy link to headingAccess governance

Controlling who can deploy doesn't protect the apps, agents, and data that make it into production.

On Vercel, you can configure every deployment to be private by default, and with Vercel Passport, you can require employees to authenticate through your IdP before they can access internal apps.

### Copy link to headingIntegration and data governance

Agents are only useful when they can access your systems and data, but that often means using long-standing environment varibles with wide-ranging permissions to your CRM, databases, Slack, and other systems.

Vercel Connect implements connectors with scoped access, and mints tokens for each agent task, meaning agents only access the specific context they need for the job. And now, with Enterprise-Managed Authorization, when employees sign into Vercel through your IdP, agents can use connected services automatically, without a separate authorization prompt.

Connect also integrates with Passport, so individual employee permissions also apply at the integration and data layer. If someone can't see data in a source system, they can't access it through an app or agent either.

## Copy link to headingModel and token governance

The average enterprise company using Vercel AI Gateway routes across 17 different models. Without a model router, that would require integrating with multiple separate providers, spreading API keys and budget management across platforms.

![AI Gateway gives you central control over hundreds of models, including budgets for individual keys and projects.](/images/posts/e764a53ea792.jpg)

![AI Gateway gives you central control over hundreds of models, including budgets for individual keys and projects.](/images/posts/6051997e0fca.jpg)

![AI Gateway gives you central control over hundreds of models, including budgets for individual keys and projects.](/images/posts/f70229de0fc1.jpg)

![AI Gateway gives you central control over hundreds of models, including budgets for individual keys and projects.](/images/posts/fa60245c0984.jpg)

AI Gateway gives you access to hundreds of models through a single API, with no markup on cost, and Zero Data Retention keeps your data from being stored or trained on. You can also elect to route through US-only providers to maintain compliance.

#### Copy link to headingHow Mercor manages model governance at scale

Mercor connects AI labs with subject-matter experts who help train and evaluate models. Their engineers need access to hundreds of models to enable that work, but before migrating to Vercel, access was spread across direct integrations and third-party routers, making stolen credentials a huge risk, and token spend impossible to manage.

They moved their model routing to AI Gateway, and now engineers can access hundreds of models with a single, expiring secret, and they can set budgets per person or project.

In their first 10 days on AI Gateway, they processed 63 billion tokens without hitting any rate limits.

## Copy link to headingCentralized visibility and security

Vercel Observabilitygives you a single view for app and agent telemetry across every project, so you can easily manage performance and troubleshoot problems for both internal tools and customer-facing products.

TheSecurity Dashboardflags risks across your team and apps, including missing MFA, unprotected preview deployments, long-lived credentials, and framework vulnerabilities. Each finding links to the settings needed to fix it.

![The Vercel Security Dashboard provides a global view of vulnerabilities across users and projects.](/images/posts/040df9c244e3.jpg)

[翻译失败，原文如下]

![The Vercel Security Dashboard provides a global view of vulnerabilities across users and projects.](/images/posts/c2694a2c1d73.jpg)

![The Vercel Security Dashboard provides a global view of vulnerabilities across users and projects.](/images/posts/780014c49c20.jpg)

![The Vercel Security Dashboard provides a global view of vulnerabilities across users and projects.](/images/posts/b5ec786d2bd6.jpg)

## Copy link to headingBring Your Own Cloud on AWS

BYOC on AWS isgenerally available. With BYOC, application functions execute in your AWS account, within your security and network boundaries.

Meta Superintelligence Labs runs on Vercel via BYOC, giving its AI teams the ability to test and deploy ideas quickly, inside their own AWS environment. Leaders at Meta said that in their first week on Vercel, they shipped a month worth of work.

## Copy link to headingFrom idea to global scale on one platform

Vercel let's everyone in your company build safely, and makes it easy for engineers to ship the best ideas at global scale, all on a single platform.

That is how we built Vertex, our customer support agent. We were previously using a vendor, but it couldn't answer all of our customers questions. When our support team built agents and skills to cover the gaps and increase our responses times, and we realized they had laid the foundation for the experience we wanted to deliver directly to our customers.

Our GTM engineering team took that foundation and made it production ready with evals and model failover.

Today, Vertex handles 91% of our customer support cases autonomously, processing thousands of tickets a week, and it runs on the same platform where the idea started.

### Copy link to headingShip your best ideas, securely

Contact salesto learn more about enterprise governance on Vercel and get a custom demo of the platform.

### Copy link to headingResources

- Learn more aboutEnterprise Apps and Agents
- Learn how to protect internal apps withVercel Passport and your identity provider
- Read the complete guide toBring Your Own Cloud on AWS
- Deploy a secure data analyst agentin one click

Learn more aboutEnterprise Apps and Agents

Learn how to protect internal apps withVercel Passport and your identity provider

Read the complete guide toBring Your Own Cloud on AWS

Deploy a secure data analyst agentin one click

---

> 本文由AI自动翻译，原文链接：[Vercel for Enterprise](https://vercel.com/blog/vercel-for-enterprise)
> 
> 翻译时间：2026-10-16 06:41
