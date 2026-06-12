---
title: Okara用Vercel为12万企业运行AI营销代理
title_original: How Okara runs CMO agents for 120,000 companies on Vercel
date: '2026-06-11'
source: Vercel Blog
source_url: https://vercel.com/blog/how-okara-runs-cmo-agents-for-120000-companies-on-vercel
author: ''
summary: Okara是一款AI CMO，指挥八个子代理处理SEO、内容、社交媒体等营销任务，为超过12万家企业管理增长。其四人团队每天在Vercel的多供应商AI堆栈上处理40亿Token，通过AI
  Gateway集成多个模型供应商，并在Vercel Sandboxes中自动运行代理工作流。文章展示了小团队如何借助隐形基础设施服务大规模客户，实现高效分发。
categories:
- AI产品
tags:
- AI营销
- Vercel
- 多供应商AI
- 自动化代理
- 创业
draft: false
translated_at: '2026-06-12T06:37:01.682514'
---

### Link to headingOkara on Vercel

- 每天在 Vercel 的多供应商 AI 堆栈上处理 40 亿 Token
- AI CMO 积极管理超过 120,000 家企业的增长
- 八个子 Agent 处理 SEO、GEO、社交、内容、Reddit 和 Hacker News
- 新 AI 模型在发布当天即可供用户使用

每天在 Vercel 的多供应商 AI 堆栈上处理 40 亿 Token

AI CMO 积极管理超过 120,000 家企业的增长

八个子 Agent 处理 SEO、GEO、社交、内容、Reddit 和 Hacker News

新 AI 模型在发布当天即可供用户使用

Okara 是一款 AI CMO，它指挥一组专门的子 Agent 来推动营销，因此创始人无需亲力亲为。将您的网站 URL 提供给 Okara，AI CMO 就会制定营销策略、打造品牌声音，并激活 SEO、内容和社交媒体方面的 Agent，以提升知名度和销售线索，而无需招聘任何营销人员。

![](/images/posts/4f2ac4408bcc.jpg)

正如 Okara 创始人 Fatima Rizwan 所说：“你可以用一个周末的时间构建产品，然后花几个月试图让别人注意到它。”她认为，分发方式仍停留在前 AI 时代：分散在订阅和代理机构中，在获得任何回报之前，每月成本就超过 15,000 美元。

Okara 由一个四人团队构建，每天处理 40 亿 Token。该公司遵循初创公司的新模式：一个小团队构建一个平台，为数千家其他公司处理增长问题。Fatima 很快意识到，用四个人服务数十万家公司意味着基础设施必须隐形。花在基础设施上的任何时间，都是没有花在构建上的时间。

## Link to heading使用 AI Gateway 通过一个 API 密钥集成多个供应商

#### Link to heading管理单个供应商 SDK 的摩擦

Okara 的后端最初通过单独的 SDK 与八个模型供应商通信，每个 SDK 都有自己的密钥管理、图像处理和边缘情况。当他们扩展到开源模型时，这种方法完全失效了。每个新模型都意味着工程师要停止产品交付，转而编写适配器。重试逻辑、回退路由和供应商健康监控都存在于 Okara 的代码库中，需要手动维护。

大多数 AI 基础设施都会要求 Okara 继续忍受这种摩擦。这就是他们迁移到 Vercel AI Gateway 的原因。

#### Link to heading一个端点，所有供应商

AI Gateway 用单一配置取代了所有自定义集成。重试逻辑和回退处理完全从 Okara 的代码库移到了 Vercel 的路由层，包括对 Okara 隐私敏感的安全聊天提供零数据保留支持。

新模型发布当天，Okara 的团队就可以通过 Gateway 立即将其提供给用户。无需适配器，无需边缘情况测试，无需部署周期。

## Link to heading在 Vercel Sandboxes 中运行 Agent 工作流

Okara 的 SEO Agent 可以扫描问题并编写修复代码。当 Agent 在用户网站上发现技术问题时，它会启动一个 Vercel Sandbox 并在隔离环境中运行分析。分析结果会传递给一个编码 Agent，该 Agent 会打开一个包含修复方案的拉取请求，供开发者审查和合并。检测、分析、代码更改：整个循环自动运行，在一切上线之前由人类做出最终决定。

Okara 在 Vercel Sandboxes 发布当天就采用了它。Rizwan 在 X 上看到了公告，团队立即开始构建。

## Link to heading下一步计划

现在有 120,000 个网站正在使用 Okara 的 AI CMO。团队每天向生产环境交付六到七次，每次改进都在当天为客户落地。使用 Okara 的独立创始人可以获得相当于其团队规模十倍的分发能力，而无需增加人员编制或支付每月 15,000 美元的代理机构账单。

Okara 正在扩展其 Agent 套件，并向高端市场进军，以服务更大的团队。随着产品的增长，基础设施需求也在增长。更多的用户、更多的 Agent、更多的 Token。当你只有四个人却要处理 120,000 家公司的增长时，你无法承受基础设施带来的干扰。有了 Vercel，这不再是问题。

关于 Okara：Okara 是一款 AI CMO，它指挥一组专门的子 Agent，为创始人和小团队处理 SEO、内容和社交媒体。它连接到您的网站，打造品牌声音，并通过八个渠道管理分发，无需招聘营销人员。

---

> 本文由AI自动翻译，原文链接：[How Okara runs CMO agents for 120,000 companies on Vercel](https://vercel.com/blog/how-okara-runs-cmo-agents-for-120000-companies-on-vercel)
> 
> 翻译时间：2026-06-12 06:37
