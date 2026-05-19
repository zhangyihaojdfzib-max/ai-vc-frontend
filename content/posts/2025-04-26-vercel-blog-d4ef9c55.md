---
title: Vercel紧急修复React Router高危漏洞
title_original: Protection against React Router and Remix vulnerabilities - Vercel
date: '2025-04-26'
source: Vercel Blog
source_url: https://vercel.com/changelog/protection-against-react-router-and-remix-vulnerabilities-cve-2025-43864
author: ''
summary: 安全研究人员发现React Router中存在两个高危漏洞（CVE-2025-43864和CVE-2025-43865），可导致缓存投毒DoS攻击及存储型XSS。Vercel已通过Firewall剥离恶意请求标头，并主动清除CDN缓存，保护所有客户。建议用户升级至React
  Router 7.5.2并清除额外缓存层。
categories:
- 技术趋势
tags:
- React Router
- 安全漏洞
- Vercel
- 缓存投毒
- XSS
draft: false
translated_at: '2026-05-19T06:14:24.318566'
---

安全研究人员在审查Remix Web框架时，发现React Router中存在两个高危漏洞。Vercel已主动为Vercel Firewall部署缓解措施，Vercel客户现已受到保护。

CVE-2025-43864和CVE-2025-43865允许外部方通过特定请求标头修改响应，这可能导致缓存投毒拒绝服务（DoS）攻击。CVE-43865还可引发存储型跨站脚本（XSS）等漏洞。

## 链接到标题影响与分析

在获悉该漏洞后，我们立即开始分析其对Vercel平台的影响。以下是我们发现的问题及建议：

- 我们成功复现了该漏洞，并证明缓存投毒（包括存储型跨站脚本（XSS）注入）极易实施
- 唯一前提条件是客户使用了受影响版本的Remix / React Router（v7.0.0分支中早于v7.5.2的版本）以及`Cache-Control`标头
- 缓存被投毒后，影响范围可扩展至应用程序的任何访问者，无论其认证状态或任何其他请求标头如何
- 使用v7.0.0至v7.5.1之间React Router版本的Vercel客户，在Firewall缓解措施部署前均受影响
- 我们已通过Vercel Firewall从请求中剥离`X-React-Router-Spa-Mode`和`X-React-Router-Prerender-Data`标头来部署攻击缓解措施。现在，Vercel平台上的所有部署均已保护新请求。我们已与Remix / React Router团队确认了缓解方案。
- 除缓解未来请求外，我们出于谨慎考虑，已主动清除网络中的CDN响应缓存。

我们成功复现了该漏洞，并证明缓存投毒（包括存储型跨站脚本（XSS）注入）极易实施

唯一前提条件是客户使用了受影响版本的Remix / React Router（v7.0.0分支中早于v7.5.2的版本）以及`Cache-Control`标头

缓存被投毒后，影响范围可扩展至应用程序的任何访问者，无论其认证状态或任何其他请求标头如何

使用v7.0.0至v7.5.1之间React Router版本的Vercel客户，在Firewall缓解措施部署前均受影响

我们已通过Vercel Firewall从请求中剥离`X-React-Router-Spa-Mode`和`X-React-Router-Prerender-Data`标头来部署攻击缓解措施。现在，Vercel平台上的所有部署均已保护新请求。我们已与Remix / React Router团队确认了缓解方案。

除缓解未来请求外，我们出于谨慎考虑，已主动清除网络中的CDN响应缓存。

这两个问题已在React Router 7.5.2中得到修复。我们建议更新至最新版本并重新部署。

如果您使用了额外的缓存层（包括Cloudflare或其他CDN），建议单独清除这些缓存。感谢`zhero`披露该漏洞。

---

> 本文由AI自动翻译，原文链接：[Protection against React Router and Remix vulnerabilities - Vercel](https://vercel.com/changelog/protection-against-react-router-and-remix-vulnerabilities-cve-2025-43864)
> 
> 翻译时间：2026-05-19 06:14
