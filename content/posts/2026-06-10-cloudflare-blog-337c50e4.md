---
title: Cloudflare新服务：安全路由公共流量至私有应用
title_original: Route public traffic to private applications with Cloudflare
date: '2026-06-10'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/private-origins-dns-routing/
author: ''
summary: Cloudflare推出Private Origins应用服务（封闭测试），允许企业将公共流量安全路由到私有源站，无需暴露公网IP或运行连接器软件。该服务将WAF、机器人管理、速率限制、缓存等安全与性能服务扩展到私有应用，支持通过Cloudflare
  Tunnel、WAN或Mesh等现有连接模式。文章指出公共与私有基础设施的界限正在模糊，私有应用同样需要现代安全防护，并介绍了四种流量组合场景。
categories:
- 技术趋势
tags:
- Cloudflare
- 私有网络
- 应用安全
- 流量路由
- Zero Trust
draft: false
translated_at: '2026-06-11T06:48:40.563078'
---

# 通过Cloudflare将公共流量路由到私有应用

2026-06-10

- Enrique Somoza
- Steve Welham
- Shruti Mittal

![](/images/posts/7fe8e1fa03ff.png)

在互联网历史的大部分时间里，公共和私有基础设施作为独立的世界运行。公共应用位于内容分发网络（CDN）和Web应用防火墙（WAF）之后。私有应用位于虚拟专用网络（VPN）、防火墙和独立运维栈之后。我们认为这种区分正在变得过时。

组织关心的许多应用并非公共网站。它们是内部API、AI Agent（智能体）后端、MCP服务器、运维工具以及从未设计为暴露在公共互联网上的服务。然而，这些应用仍然需要现代安全、性能和可编程性服务。安全性应该是到达应用的流量属性，而非应用所处位置的偶然结果。

到目前为止，将这些服务应用于私有应用通常需要公共IP、防火墙例外、连接器软件或复杂网络。因此，许多私有应用尽管需要与面向公共的应用相同的保护和控制，却未能获得WAF、机器人管理、速率限制、缓存、流量加速、重写和Workers等功能。

今天，我们面向符合条件的Enterprise客户以封闭测试形式推出Private Origins应用服务。客户现在可以安全地将流量路由到私有源站，而无需将这些源站暴露在公共互联网上。这使得Cloudflare的安全、性能和可编程性服务能够保护在私有网络上运行的应用，就像它们保护公共互联网应用一样。

WAF规则、机器人管理、速率限制、缓存、重写和Workers现在可以部署在私有源站之前，无需暴露公共IP、入站防火墙规则或在源站上运行cloudflared。

### 四个用例，一个应用层

这种路由模型建立在Cloudflare已通过Cloudflare Tunnel、Cloudflare One Client和私有网络集成支持的连接模式之上。多年来，Cloudflare Tunnel允许客户通过cloudflared将公共流量路由到私有应用。这项新功能将相同的模式扩展到现有的Cloudflare WAN或Cloudflare Mesh连接，无需在源站上运行连接器软件。

这些连接大部分通过Cloudflare的私有网络路由层进行编排，该路由层决定流量如何通过Cloudflare Tunnel、Virtual Networks、Cloudflare Mesh和其他连接模型到达私有目的地。客户可以通过API和仪表板定义其路由行为，而无需为每个产品管理独立的网络栈。

我们将Cloudflare的私有网络层直接扩展到应用服务栈中，使安全和性能代理基础设施能够将私有IP视为公共主机名的有效源站目标。因此，以前只能通过Cloudflare Tunnel、Cloudflare One、Cloudflare Mesh或Cloudflare WAN访问的相同私有IP，现在可以像公共源站一样位于Cloudflare的安全、性能和可编程性服务之后。

这也为Cloudflare产品创建了更统一的模型。Workers VPC绑定和Spectrum私有源站路由现在依赖于相同的底层私有连接层，为客户提供单一事实来源，用于控制私有流量如何在Cloudflare环境中流动。

应用流量现在根据用户来源和应用所在位置分为四种组合：

右上角的组合是Cloudflare一直以来的做法：互联网上的用户访问互联网上的应用，Cloudflare位于中间。右下角是Cloudflare One：私有网络上的用户安全地访问公共服务。

左上角是我们今天推出的功能。左下角是私有到私有，这是我们下一步要构建的方向。

### 今天推出的功能

到目前为止，将公共流量引导到私有源站通常意味着需要做出权衡。客户可以使用Cloudflare Tunnel（在源站上或附近运行我们的连接器软件cloudflared），或使用Cloudflare Load Balancing配合私有源站池进行健康检查和故障转移。在许多情况下，组织还维护着并行基础设施，如面向公共的负载均衡器、反向代理、跳之间的mTLS以及跨多层的TLS终止。因此，将Cloudflare完整的应用服务栈应用于私有应用通常需要额外的复杂性、运维开销或独立产品。Private Origins应用服务消除了这些权衡。

对于那些已经运营Cloudflare WAN（IPsec隧道、GRE隧道、CNI链路）或Cloudflare Mesh的客户来说，缺少的是一条路径。他们已经为站点到站点网络和Zero Trust构建了到Cloudflare的私有连接，并希望使用相同的连接将公共流量引导到私有源站。这正是Private Origins应用服务所提供的。

当您在代理的A或AAAA记录上启用Use private network routing时，Cloudflare的WAF、速率限制、缓存、机器人管理和转换规则都会在Cloudflare网络上正常运行。唯一的区别是最后一跳：Cloudflare不是通过公共互联网到达源站，而是通过您现有的私有网络连接路由连接。

对于RFC 1918私有IPv4范围（10.x.x.x、172.16.x.x–172.31.x.x和192.168.x.x）、RFC 6598 CGNAT范围（100.64.x.x–100.127.x.x）和RFC 4193唯一本地IPv6地址（FC00::/7），该开关会自动启用，因为这些地址只能在私有网络内访问。对于只能通过私有网络或隧道访问的公共IP地址，您可以手动启用该开关。

### API的样子

对于通过API自动化部署的客户，私有路由只是标准DNS记录上的一个附加属性。

```JSON
POST /zones/{zone_id}/dns_records
{
 "type": "A",
 "name": "app.example.com",
 "content": "10.0.0.50",
 "ttl": 300,
 "proxied": true,
 "use_private_routing": true
}
```

在幕后，Cloudflare的代理平台通过查询Cloudflare的Origin API来确定将流量发送到app.example.com的位置。响应包含指示应通过私有网络路径到达目的地的元数据：

```JSON
{
 "zone_name": "example.com",
 "ipv4_addresses": ["10.0.0.50"],
 "use_private_routing": true
}
```

use_private_routing标志是关键信号。当我们的代理看到它时，不会尝试通过公共互联网直接连接到私有IP地址，而是将请求交给我们的私有网络层，然后该层通过客户现有的私有网络连接（无论是IPsec、GRE、Cloudflare Tunnel、CNI还是Cloudflare Mesh）路由连接。

### 超越HTTP：Spectrum和Workers VPC

相同的路由模型现在扩展到HTTP应用之外。源站不必是Web服务器。它可以是TCP数据库、UDP日志端点或Workers直接调用的私有API。共同点是Cloudflare位于您的流量和私有网络之间，无论协议或请求来源如何，都应用相同的安全、性能和路由层。

Spectrum（Cloudflare的第4层代理）现在可以部署在私有IP上运行的TCP和UDP服务之前。Spectrum应用无需创建负载均衡器池作为中介，可以直接在源站配置上指定virtual_network_id。当您创建Spectrum应用时，可以在私有源站IP旁边包含虚拟网络ID：

```JSON
{
 "protocol": "tcp/22",
 "dns": {
   "type": "CNAME",
   "name": "ssh.example.com"
 },
 "origin_direct": ["tcp://10.0.0.50:22"],
 "virtual_network_id": "fab9ac85-491b-44c8-b7ae-dd44d4f4672e"
}
```

当您创建或更新使用私有源站和虚拟网络的Spectrum应用时，Cloudflare会在保存配置前验证IP地址是否与Cloudflare Tunnel中的路由匹配。如果没有匹配的路由，API将拒绝请求，应用也不会被创建。保存后，Spectrum会将连接交给您的虚拟网络，该网络通过关联的隧道进行路由，其路径与您在DNS记录上启用私有网络路由时HTTP流量所使用的路径相同。在此初始版本中，Spectrum私有源站通过Cloudflare Tunnel提供支持。未来版本将增加对其他私有网络连接选项的支持。

这意味着您现在可以将Spectrum部署在任何运行于私有IP上的TCP/UDP服务之前。该服务保持私有，无需公共IP、连接器软件或负载均衡器。

Workers VPC为在Cloudflare上运行的代码形成了闭环。绑定告诉Workers运行时通过与DNS记录相同的私有路径进行路由。浏览器、移动应用、Workers和AI Agent（智能体）都通过Cloudflare访问您的私有源站：互联网流量通过DNS记录，Workers则通过绑定。

### 下一步计划

公网到私网路由目前处于封闭测试阶段，我们计划在2026年第四季度实现GA（正式发布）。

在GA之后，我们将致力于实现私网到私网的流量传输：私有网络上的用户、服务和AI Agent（智能体）安全地访问其他私有网络上的应用，而Cloudflare的应用服务则位于中间。

我们正朝着这样一种模式迈进：无论用户或源站是公网还是私网，相同的Cloudflare基础设施都能保护流量安全。

最终状态是：使用Cloudflare One Client访问wiki.company.internal的员工，能获得与访问公共API的客户相同的WAF、速率限制和机器人管理保护。消费专有内部API的AI Agent（智能体）与浏览器运行在相同的安全栈上。跨云和数据中心的服务间流量获得与互联网流量相同的控制，即使用户和服务器都不在公共互联网上。

### 立即开始

私有源站路由功能现已面向符合条件的Enterprise客户提供封闭测试。请联系您的Cloudflare客户团队申请访问权限。启用后，请遵循我们的开发者文档，其中详细介绍了完整设置流程。您需要Cloudflare One连接（IPsec、GRE、CNI或Cloudflare Mesh），并在您的私有网络中为Cloudflare的源IP范围100.64.0.0/12配置回程路由。

有问题或反馈？请在我们的社区论坛中参与讨论，或联系您的客户团队。

---

> 本文由AI自动翻译，原文链接：[Route public traffic to private applications with Cloudflare](https://blog.cloudflare.com/private-origins-dns-routing/)
> 
> 翻译时间：2026-06-11 06:48
