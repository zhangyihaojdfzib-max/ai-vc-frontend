---
title: Artemis：构建主动智能安全系统，革新传统SIEM
title_original: A Proactive System of Intelligence for Security
date: '2026-04-14'
source: Tomasz Tunguz
source_url: https://www.tomtunguz.com/artemis/
author: ''
summary: 本文指出传统SIEM系统在AI驱动的现代攻击面前已显脆弱。由前亚马逊和Abnormal Security高管创立的Artemis公司，提出了一种新型主动智能安全系统。其核心依托三项技术：语义理解，将日志转化为动态环境模型；智能体检测，用多步推理智能体替代脆弱的手写规则；闭环学习，使系统能持续进化并自动维护检测机制。该平台旨在对安全数据进行自主推理，为现代安全团队提供动力。
categories:
- AI产品
tags:
- 网络安全
- SIEM
- 人工智能
- 创业公司
- 主动防御
draft: false
translated_at: '2026-04-16T04:53:02.987027'
---

在每个安全团队的核心，都存在着一个数据库。这个数据库记录着用户的每次登录、每个入站流量数据包以及每一次攻击尝试。这些在人工智能时代之前设计的SIEM系统，在自主攻击者横行的时代如同木制盾牌般脆弱。

后果正在不断加剧。深度伪造诈骗已窃取数千万资金。AI生成的钓鱼攻击绕过了传统过滤器。正如Mythos所揭示的，攻击手段的复杂程度只会日益提升。

Shachar Hirshberg与Dan Shieblers洞察到了这一机遇。Shachar曾领导亚马逊GuardDuty产品，将业务规模扩展至超过8万客户。Dan则在Abnormal Security组建并领导了60人的AI/ML团队。他们共同创立了Artemis，旨在构建一个为现代安全团队提供防御动力的数据库。短短数月内，他们已获得十余个企业生产环境部署，每小时处理超过十亿条事件。我们很高兴能在A轮融资中与他们携手合作，共同参与的还有我们的合作伙伴Felicis、Brightmind和First Round。

![Screenshot 2026-04-15 at 7.34.47 AM](/images/posts/b986f677563e.jpg)

这款新型SIEM的核心依托于三项技术：

**语义理解**。对传统SIEM而言，日志只是一串文本。它无法理解Okta中的"jdoe"与AWS中的"john.doe"是同一人，也无法识别一系列单独无害的行为可能构成攻击。Artemis将原始日志转化为客户环境的动态模型：涵盖用户、资产、关系和安全态势。

**智能体检测**。传统平台依赖脆弱的手写规则。工程师编写检测规则："若事件A、B、C按序发生，则触发警报。"这种规则可能仅有效数月。随着新服务加入、日志格式变更，规则便会失效。Artemis的检测包含多步推理智能体，能动态查询数据、执行聚合分析，并在呈现警报前根据上下文进行威胁确认推理。

**闭环学习**。传统平台随时间推移效能递减：静态检测会因数据和行为变化而退化。Artemis则持续进化：每处理一次事件或主动威胁狩猎，系统都能识别新规律。这些规律会被转化为永久性检测机制，并实现全自动的研究、验证与维护。

最终形成的平台不仅存储和检索数据，更能对数据进行自主**推理**。

如果您希望了解更多信息或加入这项使命，请查看Artemis的**开放职位**及Shachar的**文章**。

---

> 本文由AI自动翻译，原文链接：[A Proactive System of Intelligence for Security](https://www.tomtunguz.com/artemis/)
> 
> 翻译时间：2026-04-16 04:53
