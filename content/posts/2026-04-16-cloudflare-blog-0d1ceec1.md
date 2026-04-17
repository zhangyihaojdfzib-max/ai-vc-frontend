---
title: 通过PlanetScale与Workers部署Postgres和MySQL数据库
title_original: Deploy Postgres and MySQL databases with PlanetScale + Workers
date: '2026-04-16'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/deploy-planetscale-postgres-with-workers/
author: ''
summary: 本文介绍了Cloudflare与PlanetScale的深度整合，允许开发者直接从Cloudflare仪表板创建和管理PlanetScale的Postgres或MySQL数据库，并使用统一的Cloudflare账户进行计费。通过Hyperdrive服务，Workers可以高效连接数据库，实现连接池管理和查询缓存，从而构建快速、可靠的全栈应用程序。这一合作旨在简化开发流程，为开发者提供无缝的数据库部署和管理体验。
categories:
- AI基础设施
tags:
- Cloudflare
- PlanetScale
- 数据库部署
- Postgres
- MySQL
draft: false
translated_at: '2026-04-17T04:51:15.562093'
---

# 通过 PlanetScale + Workers 部署 Postgres 和 MySQL 数据库

2026-04-16

- Vy Ton
- Matt Silverlock

![](/images/posts/9413d1f89944.png)

去年九月，Cloudflare 宣布了与 PlanetScale 的合作，旨在让 Cloudflare Workers 能够直接访问 Postgres 和 MySQL 数据库，以构建快速的全栈应用程序。

很快，我们将进一步整合双方的技术：您将能够直接从 Cloudflare 仪表板和 API 创建 PlanetScale 的 Postgres 和 MySQL 数据库，并由您的 Cloudflare 账户统一计费。

您可以根据 Worker 应用程序的需求选择数据存储方案，并作为 Cloudflare 自助服务或企业客户，保持统一的计费系统。Cloudflare 提供的积分，例如在我们的创业计划中给予的积分，或 Cloudflare 承诺消费额度，均可用于支付 PlanetScale 数据库的费用。

## 为 Workers 准备的 Postgres 和 MySQL

像 Postgres 和 MySQL 这样的 SQL 关系型数据库是现代应用程序的基础。特别是 Postgres，凭借其丰富的工具生态系统（ORM、GUI 等）以及用于在 AI 驱动应用程序中构建向量搜索的扩展（如 pgvector），在开发者中日益流行。对于大多数需要一个强大、灵活且可扩展的数据库来支撑其应用程序的开发者来说，Postgres 是默认选择。

您现在已经可以通过 Cloudflare 仪表板连接您的 PlanetScale 账户，并直接为您的 Workers 创建 Postgres 数据库。从下个月开始，作为自助服务或企业用户，新的 Cloudflare 订阅将把新的 PlanetScale 数据库费用直接计入您的 Cloudflare 账户。

在您的 PlanetScale 账户连接后，如何通过 Cloudflare 仪表板创建 PlanetScale 数据库。Cloudflare 计费将于下个月上线。

通过我们内置的集成，PlanetScale 数据库可以自动与使用 Hyperdrive（我们的数据库连接服务）的 Workers 协同工作。Hyperdrive 服务管理数据库连接池和查询缓存，使数据库查询快速可靠。您只需在 Worker 的配置文件中添加一个绑定：

```javascript
// wrangler.jsonc 文件
{
  "hyperdrive": [
    {
      "binding": "DATABASE",
      "id": <AUTO_CREATED_ID>
    }
  ]
}

```

然后就可以通过您选择的 Postgres 客户端，在您的 Worker 中开始运行 SQL 查询：

```javascript
import { Client } from "pg";

export default {
  async fetch(request, env, ctx) {
   
    const client = new Client({ connectionString: env.DATABASE.connectionString });
    await client.connect();

    const result = await client.query("SELECT * FROM pg_tables");
    ...
}

```

## PlanetScale 开发者体验

PlanetScale 因其无与伦比的性能和可靠性，成为向 Workers 社区提供服务的必然选择。开发者可以从两种最受欢迎的关系型数据库中进行选择：Postgres 或 Vitess MySQL。PlanetScale 与 Cloudflare 一样，将性能和可靠性视为开发者平台的关键特性。凭借查询洞察、用于提升 SQL 查询性能的 Agent 驱动工作流，以及用于安全部署代码（包括数据库变更）的分支等功能，PlanetScale 的数据库开发者体验堪称一流。

Cloudflare 用户将获得完全相同的 PlanetScale 数据库开发者体验。您的 PlanetScale 数据库可以直接从 Cloudflare 部署，并通过 Hyperdrive 管理连接，这已经使您现有的区域数据库能够借助全球分布的 Workers 实现快速访问。这意味着您可以以标准的 PlanetScale 定价，访问相同的 PlanetScale 数据库集群，并享受所有功能，包括查询洞察以及使用情况和成本的详细细分。

PlanetScale Postgres 的单个节点起价为每月 5 美元。

## Workers 部署位置

对于集中式数据库，Workers 可以运行在您的主数据库旁边，通过显式的位置提示来减少延迟。默认情况下，Workers 在靠近用户请求的位置执行，这在查询中心数据库（尤其是进行多次查询时）会增加网络延迟。相反，您可以将 Worker 配置在离您的 PlanetScale 数据库最近的 Cloudflare 数据中心执行。未来，Cloudflare 可以根据您的 PlanetScale 数据库位置自动设置位置提示，并将网络延迟降低到个位数毫秒。

```javascript
{
  "placement": {
    "region": "aws:us-east-1"
  }
}

```

## 即将推出

您现在就可以通过 Cloudflare 仪表板部署一个 PlanetScale Postgres 数据库，或将现有的 PlanetScale 数据库连接到 Workers。目前所有费用仍由 PlanetScale 计收。

下个月起，新的 PlanetScale 数据库将可以计入您的 Cloudflare 账户进行计费。

我们正在与 PlanetScale 合作伙伴共同构建更多功能，例如 Cloudflare API 集成，请告诉我们您接下来希望看到什么。

---

> 本文由AI自动翻译，原文链接：[Deploy Postgres and MySQL databases with PlanetScale + Workers](https://blog.cloudflare.com/deploy-planetscale-postgres-with-workers/)
> 
> 翻译时间：2026-04-17 04:51
