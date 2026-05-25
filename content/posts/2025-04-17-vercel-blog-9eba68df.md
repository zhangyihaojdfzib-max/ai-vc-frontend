---
title: Vercel确认React Router高危漏洞不影响其平台
title_original: Protection against React Router vulnerability CVE-2025-31137 - Vercel
date: '2025-04-17'
source: Vercel Blog
source_url: https://vercel.com/changelog/protection-against-react-router-vulnerability-cve-2025-31137
author: ''
summary: 安全研究人员发现React Router存在高危漏洞CVE-2025-31137，可通过Host/X-Forwarded-Host标头进行URL操纵。Vercel调查后确认其平台及客户不受影响，原因包括：使用查询参数作为缓存键防止缓存投毒，以及@vercel/remix适配器阻止用户发送X-Forwarded-Host。补丁已在Remix
  2.16.3和React Router 7.4.1中发布，建议用户更新。
categories:
- 技术趋势
tags:
- React Router
- CVE-2025-31137
- 安全漏洞
- Vercel
- Remix
draft: false
translated_at: '2026-05-25T06:22:50.653753'
---

安全研究人员在审查 Remix 网页框架时，最近发现 React Router 中存在一个高危漏洞，该漏洞允许通过 `Host`/`X-Forwarded-Host` 标头进行 URL 操纵。

我们的调查确定 Vercel 及我们的客户不受影响：

- 我们使用查询参数作为缓存键的一部分，这可以防止由 `_data` 查询参数驱动的缓存投毒。
- `@vercel/remix` 适配器使用 `X-Forwarded-Host` 的方式与 Express 适配器类似，但最终用户无法向托管在 Vercel 上的函数发送 `X-Forwarded-Host`。

我们使用查询参数作为缓存键的一部分，这可以防止由 `_data` 查询参数驱动的缓存投毒。

`@vercel/remix` 适配器使用 `X-Forwarded-Host` 的方式与 Express 适配器类似，但最终用户无法向托管在 Vercel 上的函数发送 `X-Forwarded-Host`。

补丁已发布并在 Remix 2.16.3 / React Router 7.4.1 中推出。我们建议客户更新至最新版本。

了解更多关于 CVE-2025-31137 的信息。

---

> 本文由AI自动翻译，原文链接：[Protection against React Router vulnerability CVE-2025-31137 - Vercel](https://vercel.com/changelog/protection-against-react-router-vulnerability-cve-2025-31137)
> 
> 翻译时间：2026-05-25 06:22
