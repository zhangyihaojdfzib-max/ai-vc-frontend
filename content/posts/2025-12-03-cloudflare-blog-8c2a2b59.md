---
title: Cloudflare WAF主动防护React高危漏洞，保障客户应用安全
title_original: Cloudflare WAF proactively protects against React vulnerability
date: '2025-12-03'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/waf-rules-react-vulnerability/
author: Daniele Molteni
summary: Cloudflare针对React服务器组件（RSC）中一个CVSS评分10.0的远程代码执行漏洞（CVE-2025-55182）部署了新的WAF防护规则。该漏洞影响React
  19.0-19.2及Next.js 15-16版本，可能导致不安全反序列化和RCE攻击。Cloudflare已在免费和付费托管规则集中默认启用阻断规则，所有通过其WAF代理流量的客户均自动获得保护。尽管WAF已提供防护，Cloudflare仍强烈建议用户尽快将React更新至19.2.1、Next.js更新至最新版本。安全团队将持续监控并更新规则以应对潜在攻击变体。
categories:
- 技术趋势
tags:
- 网络安全
- React漏洞
- Web应用防火墙
- Cloudflare
- 远程代码执行
draft: false
translated_at: '2026-01-05T17:25:01.961Z'
---

Cloudflare 已部署新的防护措施，以应对 React 服务器组件（RSC）中的一个漏洞。所有 Cloudflare 客户均自动受到保护，包括免费和付费计划的用户，只要其 React 应用流量通过 Cloudflare Web 应用程序防火墙（WAF）代理即可。

Cloudflare Workers 本身对此攻击免疫。部署在 Workers 上的基于 React 的应用程序和框架不受此漏洞影响。

尽管我们的 WAF 旨在检测并阻止此攻击，我们仍强烈建议客户立即将其系统更新至最新版本的 React。

Cloudflare 已收到安全合作伙伴的警报，发现一个影响 Next.js、React Router 及其他 React 框架的远程代码执行（RCE）漏洞（安全公告 CVE-2025-55182，CVSS 评分为 10.0）。具体而言，React 版本 19.0、19.1 和 19.2，以及 Next.js 版本 15 至 16 被发现存在不安全反序列化恶意请求的问题，从而导致 RCE。

作为响应，Cloudflare 已在其网络中部署了新规则，默认操作设置为“阻止”。这些新防护措施已包含在 Cloudflare 免费托管规则集（所有免费客户可用）和标准 Cloudflare 托管规则集（所有付费客户可用）中。有关不同规则集的更多信息，请参阅我们的文档。

规则 ID 如下：
| 规则集 | 规则 ID | 默认操作 |
| Managed Ruleset | 33aa8a8a948b48b28d40450c5fb92fba | Block |
| Free Ruleset | 2b5d06e34a814a889bee9a0699702280 | Block |

专业版、商业版或企业版计划的客户应确保已启用托管规则——请按照以下步骤开启。免费计划的客户默认已启用这些规则。

我们建议客户更新至 React 19.2.1 的最新版本以及 Next.js 的最新版本（16.0.7、15.5.7、15.4.8）。

这些规则已于 2025 年 12 月 2 日星期二格林尼治标准时间下午 5:00 部署。自发布以来，截至本博客和官方 CVE 公告发布之时，我们未观察到任何攻击尝试。

Cloudflare 安全团队已与合作伙伴协作，识别了多种攻击模式，并确保新规则能有效防止任何绕过行为。在接下来的数小时和数天内，团队将持续监控潜在的攻击变体，并根据需要更新防护措施，以保护所有通过 Cloudflare 代理的流量。

> 本文由AI自动翻译，原文链接：[Cloudflare WAF proactively protects against React vulnerability](https://blog.cloudflare.com/waf-rules-react-vulnerability/)
> 
> 翻译时间：2026-01-05 17:25
