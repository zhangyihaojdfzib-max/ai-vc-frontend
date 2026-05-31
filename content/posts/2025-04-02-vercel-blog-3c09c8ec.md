---
title: Next.js中间件漏洞CVE-2025-30218披露
title_original: CVE-2025-30218 - Vercel
date: '2025-04-02'
source: Vercel Blog
source_url: https://vercel.com/changelog/cve-2025-30218
author: ''
summary: Next.js在修复CVE-2025-29927时发现并独立验证了低严重性漏洞CVE-2025-30218。该漏洞源于中间件将子请求ID发送至第三方主机，攻击者需控制第三方才能利用，实际风险较低。Vercel已通过平台缓解措施保护客户，并发布15.x修复版本及12-14.x反向移植。此次披露加速了中间件递归防护逻辑的移除，推动运行时功能对等。
categories:
- 技术趋势
tags:
- Next.js
- CVE-2025-30218
- 安全漏洞
- 中间件
- Vercel
draft: false
translated_at: '2026-05-31T06:17:02.895382'
---

在修复CVE-2025-29927的过程中，我们研究了中间件的其他潜在利用方式。我们独立验证了此低严重性漏洞，同时收到了两份独立研究人员提交的报告。

## 链接到标题摘要

为缓解CVE-2025-29927，Next.js对跨多个传入请求持久存在的`x-middleware-subrequest-id`进行了验证：

```
1 const randomBytes = new Uint8Array(8) 2 crypto.getRandomValues(randomBytes) 3 const middlewareSubrequestId = Buffer.from(randomBytes).toString('hex') 4 ;(globalThis as any)[Symbol.for('@next/middleware-subrequest-id')] = 5   middlewareSubrequestId 
```

然而，此子请求ID会被发送至所有请求，即使目标主机与Next.js应用并非同一主机。

```
1 init.headers.set( 2   'x-middleware-subrequest-id', 3   (globalThis as any)[Symbol.for('@next/middleware-subrequest-id')] 4 ) 
```

在中间件内向第三方发起fetch请求时，会将`x-middleware-subrequest-id`发送至该第三方。

## 链接到标题影响

虽然由于攻击者需要控制第三方才能利用此漏洞，实际利用可能性较低，但我们仍希望主动应对。我们已计划从中间件中移除这一递归防护逻辑——该逻辑在支持Node.js运行时的中间件新版本中已不再受支持——此次披露加速了我们实现运行时之间功能对等的进程。

Vercel客户已通过我们平台环境中实施的缓解措施获得保护。我们仍建议团队更新至最新的Next.js补丁版本或所选的反向移植版本。其他托管Next.js应用的基础设施提供商不受此影响，因为该问题仅涉及Vercel的递归防护实现。

## 链接到标题修复

本公告的发布与我们针对OSS包内漏洞披露的新内部流程保持一致，该流程基于我们对CVE-2025-29927的事后分析。我们已修复15.x版本，并为12.x至14.x版本提供了反向移植，这构成了对我们新发布的LTS政策的例外处理。

我们还主动与Next.js的新合作伙伴进行了早期披露协作。如果您是基础设施提供商并希望与我们合作，请发送邮件至partners@nextjs.org。

## 链接到标题致谢

感谢Jinseo Kim (kjsman)和ryotak的负责任的披露。这些研究人员已作为我们漏洞赏金计划的一部分获得奖励。

---

> 本文由AI自动翻译，原文链接：[CVE-2025-30218 - Vercel](https://vercel.com/changelog/cve-2025-30218)
> 
> 翻译时间：2026-05-31 06:17
