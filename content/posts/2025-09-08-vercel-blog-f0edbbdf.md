---
title: Vercel应对npm供应链攻击：18个流行包被植入加密货币盗取代码
title_original: Critical npm supply chain attack response - September 8, 2025 - Vercel
date: '2025-09-08'
source: Vercel Blog
source_url: https://vercel.com/blog/critical-npm-supply-chain-attack-response-september-8-2025
author: ''
summary: 2025年9月8日，npm生态系统发生大规模供应链攻击，攻击者通过钓鱼邮件窃取维护者凭证，入侵了包括chalk、debug在内的18个流行软件包，并植入可拦截加密货币交易的恶意代码。Vercel安全团队迅速响应，识别并清除了76个受影响项目的构建缓存，通知相关客户重新构建。事件凸显了软件供应链安全的脆弱性，文章提供了依赖项审查、版本锁定等安全建议。
categories:
- AI基础设施
tags:
- 供应链安全
- npm攻击
- Vercel
- 网络安全
- 开源安全
draft: false
translated_at: '2026-03-26T05:05:34.058808'
---

2025年9月9日，在 `duckdb_admin` 账户被入侵后，此次攻击活动蔓延至与 DuckDB 相关的软件包。这些发布版本包含了相同的钱包盗取恶意软件，证实了这是针对知名 npm 维护者的一次协同攻击的一部分。

尽管 Vercel 客户未受 DuckDB 事件影响，我们仍与合作伙伴持续追踪整个 npm 生态系统的活动，以确保 Vercel 上的部署默认保持安全。

## 概述

2025年9月8日，一次供应链攻击入侵了 18 个流行的 npm 软件包，包括 `chalk`、`debug` 和 `ansi-styles`。注入的代码旨在拦截浏览器中的加密货币交易。

我们的安全和工程团队在最初的入侵中识别了所有受影响的 Vercel 项目，并清除了构建缓存。受影响的客户收到了包含具体指导的通知。在 DuckDB 事件中，没有 Vercel 客户受到影响。

## 影响

注入这些软件包的恶意代码：

- 在打包进 Web 应用程序时，于客户端浏览器中执行
- 拦截加密货币和 Web3 钱包交互
- 将支付目的地重定向至攻击者控制的地址

分析发现，有 70 个 Vercel 团队在 76 个独立项目的构建中包含了受感染的软件包版本。

## 解决方案

我们的事件响应团队：

1.  通过我们的部署依赖追踪系统识别了所有受影响的项目
2.  为所有 76 个受影响的独立项目清除了构建缓存，以防止提供恶意代码
3.  通知了受影响的客户，并提供了需要重新构建的具体项目列表

恶意软件包版本已从 npm 中移除。在我们的缓存清除后重新构建的项目使用的是干净的软件包版本。

## 时间线

- 首次报告 npm 软件包中的恶意活动
- 17:39 UTC - Vercel 事件响应启动
- 22:19 UTC - 受影响项目的构建缓存被清除

## 技术细节

此次攻击源于针对 npm 软件包维护者的钓鱼活动。攻击者使用域名 `npmjs.help`（现已被关闭），通过一封具有说服力的双因素认证更新邮件来窃取凭证：

![](/images/posts/01da7ceec292.jpg)

该邮件设定了 48 小时的截止期限以制造虚假的紧迫感，声称账户将从 2025 年 9 月 10 日起被锁定。我们强烈建议 npm 软件包作者警惕此类攻击模式，并通过直接访问 `npmjs.com` 来验证任何与安全相关的邮件，而不是点击邮件中的链接。

## 建议

对于受影响的客户：

- 重新构建我们通知邮件中列出的项目
- 审查您的依赖项更新实践
- 考虑实施软件包版本锁定

对于所有客户：

- 使用 `npm audit` 检查已知漏洞
- 在 CI/CD 流水线中实施依赖项扫描
- 考虑在生产构建中使用 `npm ci` 和 lockfiles
- 在可用的情况下启用 npm 软件包来源验证

## 预防措施

我们持续加强我们的供应链安全态势：

- 增强对可疑软件包更新的监控
- 改进工具，以便在事件期间快速使缓存失效

此次事件凸显了采用深度防御策略对于供应链安全的重要性。虽然我们无法阻止所有上游入侵，但我们可以通过快速检测和响应来最小化影响。

## 致谢

感谢 Aikido Security 的早期检测以及 npm 社区在应对受感染软件包方面的快速响应。

## 参考资料

- GitHub Advisory Database
- qik Socket Security Analysis
- DuckDB Socket Security Analysis
- Aikido blog

有关此事件的疑问，请联系 `security@vercel.com`

---

> 本文由AI自动翻译，原文链接：[Critical npm supply chain attack response - September 8, 2025 - Vercel](https://vercel.com/blog/critical-npm-supply-chain-attack-response-september-8-2025)
> 
> 翻译时间：2026-03-26 05:05
