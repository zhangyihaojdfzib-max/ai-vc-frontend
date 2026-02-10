---
title: Vercel推出新令牌格式与密钥扫描，自动撤销泄露凭证
title_original: Introducing new token formats and secret scanning - Vercel
date: '2026-02-09'
source: Vercel Blog
source_url: https://vercel.com/changelog/new-token-formats-and-secret-scanning
author: ''
summary: Vercel宣布推出新的令牌格式和密钥扫描功能，以增强账户安全。新令牌格式为每种凭证类型添加了易于识别的前缀（如vcp、vci等）。通过与GitHub密钥扫描集成，当Vercel
  API凭证被意外提交到公共GitHub仓库、代码片段或npm包时，系统将自动撤销这些凭证，防止未经授权的访问。用户会在凭证暴露时收到通知，并可在仪表板中查看所有已发现的令牌和API密钥。文章建议用户定期检查、轮换长期凭证并撤销未使用的凭证。
categories:
- AI基础设施
tags:
- Vercel
- API安全
- 密钥扫描
- DevOps
- 云平台
draft: false
translated_at: '2026-02-10T04:36:06.522027'
---

![通过密钥扫描发现令牌时的令牌实体](/images/posts/63fa41a9e12d.jpg)

![通过密钥扫描发现令牌时的令牌实体](/images/posts/35670d31e2d6.jpg)

当 Vercel API 凭证被意外提交到公共 GitHub 仓库、代码片段和 npm 包时，Vercel 现在会自动撤销它们，以保护您的账户免遭未经授权的访问。

当检测到暴露的凭证时，您将收到通知，并可以在仪表板中查看所有已发现的**令牌**和**API 密钥**。此检测功能由 **GitHub 密钥扫描**提供支持，为所有 Vercel 和 **v0** 用户带来了额外的安全层。

作为此次变更的一部分，我们还更新了令牌和 API 密钥的格式，使其在视觉上易于识别。每种凭证类型现在都包含一个前缀：

- **vcp** 对应 **Vercel 个人访问令牌**
- **vci** 对应 **Vercel 集成令牌**
- **vca** 对应 **Vercel 应用访问令牌**
- **vcr** 对应 **Vercel 应用刷新令牌**
- **vck** 对应 **Vercel API 密钥**

我们建议您定期检查您的**令牌**和**API 密钥**，轮换长期有效的凭证，并撤销未使用的凭证。

**了解更多**关于账户安全的信息。

---

> 本文由AI自动翻译，原文链接：[Introducing new token formats and secret scanning - Vercel](https://vercel.com/changelog/new-token-formats-and-secret-scanning)
> 
> 翻译时间：2026-02-10 04:36
