---
title: Vercel防火墙系统绕过规则重大升级
title_original: Improvements to Vercel Firewall system bypass rules - Vercel
date: '2025-02-28'
source: Vercel Blog
source_url: https://vercel.com/changelog/improvements-to-vercel-firewall-system-bypass-rules
author: ''
summary: Vercel对其防火墙系统绕过规则进行了重要改进，为Pro和企业客户提供更灵活的流量控制。新功能包括：将支持范围从生产域名扩展到预览域名，为预览部署URL和别名增加单域名规则支持，将项目级绕过规则覆盖所有关联域名，并将规则上限从3条和5条大幅提升至25条和100条。这些改进旨在帮助在前端部署代理等场景下解决流量问题，同时Vercel仍建议用户谨慎使用，避免完全禁用防护。
categories:
- 技术趋势
tags:
- Vercel
- 防火墙
- 系统绕过规则
- DDoS防护
- 基础设施
draft: false
translated_at: '2026-06-05T06:22:40.336019'
---

系统绕过规则允许 Pro 和企业客户配置防火墙规则，以针对特定 IP 和 CIDR 范围跳过 Vercel 系统防护措施（包括 DDoS 防护）。尽管我们强烈建议不要禁用防护，但客户（尤其是在 Vercel 前部署代理的客户）可能会遇到流量问题，而部署系统绕过规则可以缓解这些问题。

系统绕过规则的改进为客户提供了对规则部署方式的额外控制，包括：

- 将支持范围从生产域名扩展到预览域名
- 为预览部署 URL 和别名增加了单域名规则支持
- 将项目级绕过规则扩展至涵盖项目关联的所有域名
- 将 Pro 和企业版的系统绕过规则上限分别从 3 条和 5 条提升至 25 条和 100 条

将支持范围从生产域名扩展到预览域名

为预览部署 URL 和别名增加了单域名规则支持

将项目级绕过规则扩展至涵盖项目关联的所有域名

将 Pro 和企业版的系统绕过规则上限分别从 3 条和 5 条提升至 25 条和 100 条

了解更多关于 Vercel 防火墙的信息。

---

> 本文由AI自动翻译，原文链接：[Improvements to Vercel Firewall system bypass rules - Vercel](https://vercel.com/changelog/improvements-to-vercel-firewall-system-bypass-rules)
> 
> 翻译时间：2026-06-05 06:22
