---
title: Cloudflare内部DNS正式全面上线
title_original: Cloudflare Internal DNS is now generally available
date: '2026-07-20'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/internal-dns/
author: ''
summary: Cloudflare宣布其Internal DNS服务正式全面上线，该服务整合了公共和私有DNS管理，通过统一平台提供权威和递归DNS解析。它解决了传统内部DNS管理分散、分裂视图复杂、安全策略不统一等问题，支持零信任架构扩展，并简化了运维。企业客户可免费使用该功能，无需额外付费。
categories:
- AI基础设施
tags:
- Cloudflare
- 内部DNS
- 零信任
- 网络基础设施
- DNS管理
draft: false
translated_at: '2026-07-24T05:30:07.825419'
---

从今天起，Cloudflare Internal DNS 正式全面上线。Cloudflare Internal DNS 在客户已用于公共 DNS、零信任、网络和应用服务的同一全球网络及控制平面上，为私有网络提供权威和递归 DNS 服务。

内部 DNS（有时也称为私有 DNS）是企业基础设施中最后一批仍与网络其他部分分开管理的组件之一。许多组织为公共 DNS 运行一个平台，为内部 DNS 运行另一个平台，并在每个云环境中使用云原生 DNS 服务，且各自叠加独立的安全策略。这些系统没有一个共享共同的控制平面。分裂视图 DNS 又增加了一层复杂性，通常需要多个 DNS 环境保持同步，以便内部和外部用户对同一主机名获得不同的解析结果。当这些系统出现偏差时，就会导致服务中断。

借助 Cloudflare Internal DNS，您可以通过单一平台管理公共和私有 DNS 资源，执行 DNS 策略，并全面了解整个 DNS 堆栈。对于企业客户，此功能已包含在 Cloudflare Gateway 中，无需额外付费。

## 客户为何采用 Internal DNS

整合 DNS 运维。公共和私有 DNS 在同一个平台上运行，拥有统一的 API、统一的审计追踪和统一的策略设置点。传统 DNS 带来的设备更新周期和扩展瓶颈将不复存在。

简化分裂视图 DNS。内部和外部解析被定义为共享区域上的不同视图，通过单一控制平面进行管理。无需维护并行系统来保持同步，因此也无需追查偏差。

将零信任扩展到 DNS。解析器策略决定哪些用户和设备针对哪个视图进行解析，并由已管理其余流量的同一 Cloudflare Gateway 执行。私有名称解析不再是零信任架构中的缺口。

现代化传统基础设施。淘汰硬件设备、传统 DNS 服务器和云锁定解析器。Cloudflare Internal DNS 运行在支撑 1.1.1.1 的基础设施上，无需上架硬件，也无需配置容量。

## 我们构建了什么

Cloudflare Internal DNS 包含两个组件：Gateway Resolver（网关解析器）和 Internal Authoritative DNS（内部权威 DNS）。权威管理区域与执行 DNS 安全和路由策略是两项不同的工作。

Gateway Resolver 处理递归解析和策略评估。该组件于 2020 年推出，由 1.1.1.1 提供公共解析能力，内置策略引擎，可根据灵活表达式过滤 DNS 查询，并将查询重定向到不同的上游源，同时提供全面的日志记录和审计，集成于单一管理界面。

Internal Authoritative DNS 为内部区域提供记录服务，该平台基于 Cloudflare 已运营超过十年、服务域名数量超过任何其他提供商的同一权威平台构建。

客户主要使用三种对象：

- 内部区域：保存私有资源的权威记录，例如特定环境的应用程序、服务端点、数据库。
- DNS 视图：将区域分组为特定用户或设备组应看到的解析上下文。这是无需并行系统即可实现分裂视图的关键。
- 解析器策略：位于 Gateway 中，将匹配的查询路由到特定视图。

区域引用允许管理员在多个视图中重复使用共享区域，而无需将记录复制到每个视图中。像 intranet.local 这样的常见区域只需定义一次，即可在需要的地方引用。这正是“不要重复自己”的配置与分裂视图通常导致的重复且易产生偏差的设置之间的区别。

### 查询如何解析

来自客户端的 DNS 查询首先到达 Gateway Resolver，在此进行策略评估。之后会发生三种情况之一。如果解析器策略匹配并指向内部视图，则查询被路由到 Internal Authoritative DNS，并从匹配视图的区域中获取答案。如果策略阻止该查询，则在解析器处丢弃。否则，查询遵循公共路径，由 1.1.1.1 根据公共 DNS 层级进行解析。当内部未找到名称时，视图也可以回退到公共解析，因此单个解析器可以同时服务于私有和公共名称，而客户端无需知道具体是哪个。

### 变更如何传播

记录变更遵循一条可预测的高速路径，从输入到边缘。

每条变更都通过相同的 DNS Records API 进入，无论其源自仪表板、Terraform 还是直接 API 调用。这种统一的入口意味着无论变更如何发起，都只有一条需要审计和追溯的写入路径。变更会持久化存储在 Cloudflare 的核心数据中心以确保持久性，并在传播前进行验证。

此后，变更会复制到 Cloudflare 的全球网络，随着更新的到达，受影响的缓存条目会被失效，因此编辑后的记录在数秒内生效，而无需等待 TTL 过期。

### 开始使用

如果您是使用 Cloudflare Gateway 的企业客户，您现在即可使用 Internal DNS。打开 Cloudflare 仪表板，导航至“网络”，然后选择“内部 DNS”。

设置 Internal DNS 通常需要三个步骤：创建区域、创建视图、定义解析器策略以确定哪些用户和设备应针对该视图进行解析。

创建一个内部区域和您的第一条内部记录：

```
POST https://api.cloudflare.com/client/v4/accounts/zones
{
  "account": {
    "id": "{account_id}"
  },
  "name": "corp.internal",
  "type": "internal"
}

POST https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records
{
  "type": "A",
  "name": "db.corp.internal",
  "content": "10.0.1.50",
  "ttl": 300
}
```

然后创建一个 DNS 视图并将您的区域链接到该视图：

```
POST https://api.cloudflare.com/client/v4/accounts/{account_id}/internal_dns/views
{
  "name": "production-view",
  "zones": ["{zone_id}"]
}
```

最后，在 Zero Trust 仪表板中创建一个 Gateway 解析器策略，将匹配的流量路由到您的视图。创建一个 Gateway 位置，设置您的条件，选择“内部 DNS 视图”作为解析方法，然后选择您的视图。就这样。匹配您策略的查询现在将针对您的内部区域进行解析。

支持 Terraform，并且由于 Terraform 通过与其他方式相同的 DNS Records API 进行写入，基础设施即代码的变更遵循相同的接收和传播路径。完整的文档和端到端配置示例可在我们的开发者文档中找到。

### Internal DNS 作为 Connectivity Cloud 的一部分

Internal DNS 可与任何通过 Gateway Resolver 路由 DNS 流量的 Cloudflare 连接方法配合使用，包括 Cloudflare One Client（原 WARP）、基于 HTTPS 的 DNS (DoH)、基于 TLS 的 DNS (DoT)、端口 53 上的标准 DNS、PAC 文件部署以及 Cloudflare WAN。

对于运行 Cloudflare WAN 的组织，连接网络上的每台设备都可以通过 Cloudflare 解析内部主机名，而无需在单个设备上安装 Cloudflare One Client。其结果是，通过单一控制平面，远程用户、分支机构、数据中心和云环境都能获得一致的 DNS 体验。

更重要的是，Internal DNS 并非独立的 DNS 服务。它扩展了组织已用于通过零信任保护用户、通过 Cloudflare WAN 连接网络、加速应用程序以及保护面向互联网服务的同一 Connectivity Cloud 平台。

将私有 DNS 纳入与所有其他服务相同的全球网络仅仅是起点。DNS、网络和零信任策略的更紧密集成是下一步的发展方向——解析内部主机名、访问其背后的服务以及强制执行允许谁访问这些服务，都将通过单一平台而非多个互不关联的系统来决策。

准备好整合你的 DNS 了吗？打开仪表盘，前往“网络”，然后进入“内部 DNS”，立即创建你的第一个区域。有问题或想与其他运营者交流心得？加入 Cloudflare 社区的讨论。

## 相关标签

关注社交媒体

- Cloudflare
- Hannes Gerhart

## 订阅以接收新文章通知

我们绝不会分享你的电子邮件地址。

感谢订阅！请检查你的收件箱以确认。

---

> 本文由AI自动翻译，原文链接：[Cloudflare Internal DNS is now generally available](https://blog.cloudflare.com/internal-dns/)
> 
> 翻译时间：2026-07-24 05:30
