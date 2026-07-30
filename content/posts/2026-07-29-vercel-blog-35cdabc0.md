---
title: Vercel新增自定义环境容量购买功能
title_original: Additional custom environments can now be purchased - Vercel
date: '2026-07-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/additional-custom-environments-can-now-be-purchased
author: ''
summary: Vercel宣布专业版和企业版团队现可直接购买额外的自定义环境容量，无需联系销售。自定义环境允许用户在预览与生产环境之间添加staging、qa等阶段，每个环境独立配置分支、变量和域名。容量以5个为一组，每月50美元。专业版每个项目默认1个，最多16个；企业版默认12个，最多22个。用户可通过控制台、API或CLI调整容量，计费自动更新。
categories:
- AI基础设施
tags:
- Vercel
- 自定义环境
- 部署工具
- 开发者体验
- 定价更新
draft: false
translated_at: '2026-07-30T05:02:21.294598'
---

专业版和企业版团队现在可以直接购买额外的自定义环境容量，无需联系销售团队。

自定义环境让您能够在 Vercel 上模拟团队的发布流程。您可以在预览环境和生产环境之间添加 `staging`、`qa` 或任意命名阶段，每个环境都拥有独立的分支追踪、环境变量和域名。

您可以通过控制台、API 或 CLI 购买或调整容量。

控制台  
项目 → 设置 → 环境 → 自定义环境

API  
POST /v1/projects/custom-environments/settings

CLI  
vercel buy addon customEnvironment <packs>

容量以每 5 个环境为一组进行销售。只要项目使用的环境数量不超过新限制，您也可以减少容量。确认变更后，计费将自动更新。

### 复制链接到标题定价与限制

自定义环境适用于专业版和企业版计划。额外容量可按每组 5 个环境每月 50 美元的价格购买。

限制

专业版  
每个项目包含 1 个自定义环境（每个项目最多 16 个）

企业版  
每个项目包含 12 个自定义环境（每个项目最多 22 个）

购买需要有效的专业版或企业版计划、计费权限以及有效的支付方式。容量按项目配置，您的团队订阅将反映所有项目中购买的环境总数。了解更多

---

> 本文由AI自动翻译，原文链接：[Additional custom environments can now be purchased - Vercel](https://vercel.com/changelog/additional-custom-environments-can-now-be-purchased)
> 
> 翻译时间：2026-07-30 05:02
