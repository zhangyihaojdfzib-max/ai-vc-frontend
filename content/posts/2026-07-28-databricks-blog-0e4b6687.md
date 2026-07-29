---
title: NorthStar数周内为3000名临床医生打造排班应用
title_original: How NorthStar Anesthesia built a scheduling app for a workforce of
  3,000 clinicians in weeks
date: '2026-07-28'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-northstar-anesthesia-built-scheduling-app-workforce-3000-clinicians-weeks
author: ''
summary: NorthStar Anesthesia利用Databricks Apps，在数周内为3000名临床医生构建了一款定制排班应用，解决了商业平台隐藏休假数据、移动端不友好等痛点。该应用基于现有数据基础设施，支持颜色编码排班、设施选择、日历模式等功能，上线后日活用户从75人攀升至110人以上，显著改善了临床医生的排班体验。
categories:
- AI产品
tags:
- 排班应用
- Databricks Apps
- 医疗IT
- 移动端友好
- 临床劳动力管理
draft: false
translated_at: '2026-07-29T05:33:41.129414'
---

- NorthStar Anesthesia 在超过25个州运营临床劳动力。排班可见性对于临床医生完成工作至关重要。
- 他们的商业排班平台缺少临床医生实际需要的数据，且仪表盘移动端友好度不足，无法填补这一缺口。
- 他们利用已有的安全和数据基础设施，在数周内基于 Databricks Apps 构建并交付了一款定制排班应用。

## 引言

NorthStar Anesthesia 管理着美国超过25个州的麻醉人员配置服务，拥有约3000名医生和认证注册护士麻醉师（CRNA），他们在不同设施间轮转、值夜班和待命。这些临床医生在工作中无法稳定使用电脑，因此他们依赖手机在手术间隙查看本周的排班情况。

当公司采用新的商业排班平台时，该平台处理了大部分工作。但有一件事它刻意隐藏了：同事的休假数据。对于经常换班的劳动力来说，这带来了一个大问题。

## 仪表盘用户友好度不足

NorthStar 及其实施合作伙伴 Synaptiq 已经建立了坚实的 Databricks 基础——通过 medallion 架构统一了排班、考勤和合同数据，并用 AI/BI 仪表盘取代了旧的 Power BI 设置。最初的自然想法是用另一个仪表盘来填补排班缺口，但试点项目对最终用户并不奏效。

“由于缺乏移动端友好性——它看起来不够简洁，达不到我们想要的效果——我们转向了应用开发，”Synaptiq 的项目经理 Erin Sarosi Bell 说道。

基于 Databricks Apps 进行构建的理由很直接：数据已经就位，治理已配置完成，并且 Microsoft Entra ID SSO 可以扩展到整个临床劳动力，而无需搭建新的基础设施。

## 从需求到发布仅需数周

Synaptiq 立即投入工作，仅由一名软件工程师在短短几周内构建了一款通过 Databricks Apps 部署的 React TypeScript 应用。按临床医生类型进行颜色编码的排班视图、设施选择器、日/周/月日历模式、排班备注、按排班类型搜索和筛选——所有内容每30分钟刷新一次。关键是，这款应用展示了商业工具隐藏的休假数据。

![](/images/posts/a404ae45a42b.png)

“在几周内，我们就能构建出满足需求的产品，并快速迭代，发布了多个版本，”NorthStar 的 CTO Dan Levine 说道。“它解决了我们用户的一个巨大痛点。”

随着第一批临床医生迁移到新平台，每日独立用户数从发布时的75-80人攀升至110人以上。反馈非常直接：“数十名”用户反馈说，这款应用改变了他们的工作方式，并大大减轻了排班流程中的压力。

NorthStar 的下一步计划是：使用 AI/BI Genie 进行自然语言排班查询、推送通知，以及利用 Databricks 自动化晨间人员配置报告。

了解医疗和生命科学团队如何基于 Databricks 平台进行构建，并进一步了解 Databricks Apps。

### 在收件箱中获取最新文章

订阅我们的博客，将最新文章直接发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[How NorthStar Anesthesia built a scheduling app for a workforce of 3,000 clinicians in weeks](https://www.databricks.com/blog/how-northstar-anesthesia-built-scheduling-app-workforce-3000-clinicians-weeks)
> 
> 翻译时间：2026-07-29 05:33
