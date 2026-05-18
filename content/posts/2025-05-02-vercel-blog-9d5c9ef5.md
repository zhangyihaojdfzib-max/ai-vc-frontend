---
title: Vercel修复Flags SDK信息泄露漏洞
title_original: Information disclosure in Flags SDK (CVE-2025-46332) - Vercel
date: '2025-05-02'
source: Vercel Blog
source_url: https://vercel.com/changelog/information-disclosure-in-flags-sdk-cve-2025-46332
author: ''
summary: Vercel发现并修复了Flags SDK中的一个信息泄露漏洞（CVE-2025-46332），影响flags≤3.2.0和@vercel/flags≤3.1.1版本。攻击者可能获取标志名称、描述、选项及默认值，但无法访问标志提供程序或客户数据。Vercel已实施网络层自动缓解措施，并建议用户升级至flags@4.0.0以彻底修复问题。
categories:
- 技术趋势
tags:
- Vercel
- Flags SDK
- CVE-2025-46332
- 信息泄露
- 安全漏洞
draft: false
translated_at: '2026-05-18T06:14:41.016067'
---

Vercel 发现并修复了 Flags SDK 中的一个信息泄露漏洞，影响以下版本：

- flags≤ 3.2.0
- @vercel/flags≤ 3.1.1

该漏洞编号为 CVE-2025-46332。我们已针对 Vercel 上 Flags SDK 的默认配置发布了自动缓解措施。

建议升级至 flags@4.0.0（或从 @vercel/flags 迁移至 flags）以修复该问题。更多指导请参阅升级指南。

## 影响与分析

恶意行为者在特定条件下可能获取以下信息：

- 标志名称
- 标志描述
- 可用选项及其标签（例如 true、false）
- 标志默认值

标志提供程序不可访问。未暴露写入权限或额外客户数据，仅限于上述值。

## 自动缓解措施

Vercel 实施了网络层缓解措施，阻止默认标志发现端点 /.well-known/vercel/flags 被访问，从而自动保护 Vercel 部署免受此问题影响。

虽然不常见，但如果您通过自定义路径暴露了标志发现端点，也可以实施自定义 WAF 规则来限制对这些端点的访问，例如在使用以下情况时：

- Pages Router，因为原始未重写路由仍可访问，例如 /api/vercel/flags
- 微前端，因为每个应用程序可能使用不同的标志发现端点

## 建议

我们建议所有用户升级至 flags@4.0.0。Flags Explorer 将被禁用并显示警告通知，直到您升级至最新版本。

更多信息请参阅升级指南。

---

> 本文由AI自动翻译，原文链接：[Information disclosure in Flags SDK (CVE-2025-46332) - Vercel](https://vercel.com/changelog/information-disclosure-in-flags-sdk-cve-2025-46332)
> 
> 翻译时间：2026-05-18 06:14
