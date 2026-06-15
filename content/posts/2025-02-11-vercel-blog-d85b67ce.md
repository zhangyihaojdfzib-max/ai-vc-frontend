---
title: Vercel默认存档方式升级为split-tgz，上传提速30%
title_original: Split-tgz is now the default CLI archive deployment behavior - Vercel
date: '2025-02-11'
source: Vercel Blog
source_url: https://vercel.com/changelog/split-tgz-is-now-the-default-cli-archive-deployment-behavior
author: ''
summary: Vercel宣布将split-tgz存档部署设为CLI默认行为，取代原有tgz选项。该功能专为包含数千个文件的大型项目设计，可带来高达30%的上传速度提升，并有效避免文件上传大小限制。此前split-tgz需通过`--archive=split-tgz`参数手动启用，现已集成至默认tgz行为中，独立选项随之弃用。这一变化进一步优化了开发者的部署体验，尤其适用于大规模项目。
categories:
- 技术趋势
tags:
- Vercel
- CLI部署
- 存档优化
- 上传速度
- split-tgz
draft: false
translated_at: '2026-06-15T07:20:26.610593'
---

存档部署适用于从CLI部署包含数千个文件的大型项目。

我们此前发布了split-tgz存档部署作为新的存档选项：vercel deploy --archive=split-tgz。这一新功能可提供高达30%的上传速度提升，并避免文件上传大小限制。

我们已验证了split-tgz的稳定性，并将其设为tgz的默认行为。这意味着独立的split-tgz选项现已弃用，因为split-tgz的功能和优势已作为默认tgz选项的基础。

了解更多关于CLI存档部署的信息。

---

> 本文由AI自动翻译，原文链接：[Split-tgz is now the default CLI archive deployment behavior - Vercel](https://vercel.com/changelog/split-tgz-is-now-the-default-cli-archive-deployment-behavior)
> 
> 翻译时间：2026-06-15 07:20
