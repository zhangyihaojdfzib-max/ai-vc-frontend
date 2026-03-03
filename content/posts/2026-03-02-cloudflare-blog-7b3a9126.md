---
title: 真正可编程的SASE平台：释放安全与网络的定制化潜力
title_original: The truly programmable SASE platform
date: '2026-03-02'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/programmable-sase/
author: ''
summary: 本文探讨了可编程性在SASE（安全访问服务边缘）平台中的真正含义，超越了传统的API和自动化工具。Cloudflare One平台通过其全球网络与开发者平台的深度融合，允许客户在边缘实时执行自定义逻辑，例如调用外部风险引擎、动态注入请求头或基于业务规则路由流量。这种设计使组织能够根据独特需求构建安全和网络架构，实现实时决策与策略增强，而无需牺牲性能或增加管理复杂度。
categories:
- 技术趋势
tags:
- SASE
- 网络安全
- 边缘计算
- 可编程性
- Cloudflare
draft: false
translated_at: '2026-03-03T04:48:14.304117'
---

# 真正可编程的SASE平台

2026-03-02

- Abe Carryl

![](/images/posts/9ac16da6527a.png)

每个组织都通过独特的视角来处理安全问题，这种视角由其工具、需求和历史所塑造。没有任何两个环境是完全相同的，也没有哪个环境能长期保持静态。我们认为，保护这些环境的平台也不应该是静态的。

Cloudflare 构建我们的全球网络时，就以可编程为设计目标，这样我们就能帮助组织释放这种灵活性和自由度。在本文中，我们将更深入地探讨可编程性的含义，以及我们的 SASE 平台 Cloudflare One 如何帮助客户利用我们的基础组件来构建其安全和网络架构，以满足其独特和定制化的需求。

## 可编程性的真正含义

"可编程性" 这个术语已被业界淡化。大多数安全供应商声称具有可编程性，因为他们拥有公共 API、有文档记录的 Terraform 提供商、Webhook 和告警功能。这很好，Cloudflare 也提供所有这些功能。

这些基础能力提供了定制化、基础设施即代码和安全运维自动化，但它们只是入门标准。使用传统的可编程性，你可以配置一个 Webhook，以便在策略触发时向 Slack 发送告警。

但可编程性的真正价值是不同的。它是指能够拦截安全事件，用外部上下文丰富它，并实时对其采取行动的能力。假设一个用户试图访问一个包含敏感财务数据的受监管应用程序。在请求完成之前，你可以查询你的学习管理系统，以验证用户是否已完成所需的合规培训。如果他们的认证已过期，或者他们从未完成培训，则访问被拒绝，并被重定向到培训门户。该策略不仅仅是触发告警——它做出了决策。

## 构建最具可编程性的 SASE 平台

Cloudflare 全球网络覆盖全球 330 多个城市，为约 95% 的互联网用户提供 50 毫秒以内的延迟服务。这个网络在每个数据中心的每台服务器上运行着所有服务。这意味着我们**行业领先的 SASE 平台**和**开发者平台**在相同的硬件上并行运行，使得我们的 Cloudflare 服务既具有可组合性，又具有可编程性。

当你使用 Cloudflare 保护你的外部 Web 资产时，你使用的网络、工具和基础组件，与你使用 Cloudflare One 保护你的用户、设备和私有网络时完全相同。这些也是你在我们的**开发者平台**上构建和部署全栈应用程序时所使用的基础组件。它们被设计成协同工作——不是因为事后集成，而是因为它们从一开始就不是分离的。

这种设计允许客户实时使用自定义逻辑扩展策略决策。你可以调用外部风险 API、注入动态标头或验证浏览器属性。你可以根据业务逻辑路由流量，而无需增加延迟或建立单独的基础设施。没有自己计算平台的独立**SASE**提供商要求你在单独的云中部署自动化，手动配置 Webhook，并接受将分离系统拼接在一起所带来的往返延迟和管理开销。使用 Cloudflare，你的 **Worker** 可以在边缘毫秒级地增强内联 SASE 服务（如 Access），以执行自定义策略。

## 可编程性释放了什么

从本质上讲，每个安全网关都基于相同的基本模型运行。流量从源流经策略，到达目的地。策略是事情变得有趣的地方，但在大多数平台中，你的选择仅限于预定义的操作：允许、阻止、隔离或隔离。

我们认为有更好的方法。如果你可以调用自定义逻辑呢？

你可以这样做，而不是仅限于预定义的操作：

*   基于用户身份声明动态注入标头
*   在允许访问之前调用外部风险引擎以获取实时裁决
*   基于位置和工作时间强制执行访问控制

如今，客户已经可以使用 Cloudflare 完成其中许多事情。并且我们正在加强我们的 **SASE** 和**开发者平台**之间的集成，使这变得更加容易。像上面列出的那些可编程性扩展，将原生集成到 Cloudflare One 中，使客户能够将实时、自定义的逻辑构建到其安全和网络策略中。在毫秒内检查请求并做出决定。或者按计划运行一个 Worker 来分析用户活动并相应地更新策略，例如根据外部系统的信号将用户添加到高风险列表中。

我们正围绕"操作"这一概念来构建此功能：包括托管操作和自定义操作。托管操作将为常见场景提供模板，例如 IT 服务管理集成、重定向和合规自动化。自定义操作允许你完全定义自己的逻辑。当 Gateway HTTP 策略匹配时，你不再局限于允许、阻止或隔离，而是可以直接调用 Cloudflare Worker。你的代码在边缘实时运行，并拥有对请求上下文的完全访问权限。

## 客户当前的构建方式

在我们改进此体验的同时，许多客户已经在以这种方式使用 Cloudflare One 和开发者平台。以下是一个简单的示例，说明了你可以利用这种可编程性做什么。

### 自动设备会话撤销

**问题**：一位客户希望为其 Cloudflare One Client 用户强制执行定期重新认证，类似于传统 VPN 要求用户每隔几小时重新认证一次。Cloudflare 预定义的会话控制是围绕每个应用程序的策略设计的，而不是全局的基于时间的过期。

**解决方案**：一个按计划运行的 Cloudflare Worker，它查询 Devices API，识别不活动时间超过指定阈值的设备，并撤销其注册，强制用户通过其身份提供商重新认证。

```JavaScript
export default {
  async scheduled(event, env, ctx) {
    const API_TOKEN = env.API_TOKEN;
    const ACCOUNT_ID = env.ACCOUNT_ID;
    const REVOKE_INTERVAL_MINUTES = parseInt(env.REVOKE_INTERVAL_MINUTES); // 重用作为不活动阈值
    const DRY_RUN = env.DRY_RUN === 'true';

    const headers = {
      'Authorization': `Bearer ${API_TOKEN}`,
      'Content-Type': 'application/json'
    };

    let cursor = '';
    let allDevices = [];

    // 使用基于游标的分页获取所有注册信息
    while (true) {
      let url = `https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/devices/registrations?per_page=100`;
      if (cursor) {
        url += `&cursor=${cursor}`;
      }

      const devicesResponse = await fetch(url, { headers });
      const devicesData = await devicesResponse.json();
      if (!devicesData.success) {
        console.error('Failed to fetch registrations:', devicesData.errors);
        return;
      }

      allDevices = allDevices.concat(devicesData.result);

      // 提取下一个游标（如果响应使用不同的字段，例如 devicesData.result_info.cursor，请调整）
      cursor = devicesData.cursor || '';
      if (!cursor) break;
    }

    const now = new Date();

    for (const device of allDevices) {
      const lastSeen = new Date(device.last_seen_at);
      const minutesInactive = (now - lastSeen) / (1000 * 60);

      if (minutesInactive > REVOKE_INTERVAL_MINUTES) {
        console.log(`Registration ${device.id} inactive for ${minutesInactive} minutes.`);

```javascript
if (DRY_RUN) {
          console.log(`模拟运行：将删除注册记录 ${device.id}`);
        } else {
          const deleteResponse = await fetch(
            `https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/devices/registrations/${device.id}`,
            { method: 'DELETE', headers }
          );
          const deleteData = await deleteResponse.json();
          if (deleteData.success) {
            console.log(`已删除注册记录 ${device.id}`);
          } else {
            console.error(`删除 ${device.id} 失败：`, deleteData.errors);
          }
        }
      }
    }
  }
};
```

为Worker配置环境密钥（API_TOKEN、ACCOUNT_ID、REVOKE_INTERVAL_MINUTES）和定时触发器（0 */4 * * * 表示每4小时执行），您就实现了会话管理的自动化。若要将这样一个简单的功能纳入供应商的产品路线图，可能需要数月时间，而要将其纳入管理界面则耗时更久。

但借助自动化的设备会话撤销功能，我们的技术专家在一个下午就与客户共同部署了这项策略。该方案已在生产环境中稳定运行数月。

我们在Cloudflare One的部署中观察到无数类似的实施案例。我们看到用户利用我们现有的重定向策略和Workers，实现了指导页面和用途说明工作流。其他用户则构建了自定义逻辑，在制定策略或路由决策前评估浏览器属性。每个案例都解决了独特的问题，否则就需要等待供应商构建与第三方系统的特定、小众集成。而现在，客户能够按照自己的时间表，使用自主掌控的逻辑，精准构建所需功能。

## 改变对话模式的可编程平台

我们相信，企业安全的未来并非试图包办一切的一体化平台，而是一个可组合、可编程的平台，为客户提供工具和灵活性，使其能够向任何方向扩展。

对于安全团队，我们期望我们的平台能改变对话模式。您无需提交功能请求并寄望于其被纳入路线图，而是可以立即构建满足您确切需求的定制解决方案。

对于我们的合作伙伴和托管安全服务提供商（MSSP），我们的平台开启了他们为其特定客户群构建和交付解决方案的能力。这意味着可以打造行业特定解决方案，或为处于特定监管环境中的客户提供能力。定制集成成为竞争优势，而不仅仅是专业服务项目。

对于我们的客户，这意味着您构建在一个易于部署、并能从根本上适应您最复杂且不断变化需求的平台上。您的安全平台与您共同成长——它不会限制您。

## 未来展望

我们才刚刚开始。在整个2026年，您将看到我们持续深化Cloudflare One与开发者平台的集成。我们计划首先在Cloudflare Gateway中创建支持动态策略执行的自定义操作。这些操作可以利用存储在您组织现有数据库中的辅助数据，而无需面对将数据迁移至Cloudflare所带来的管理或合规性挑战。这些相同的自定义操作还将支持请求增强功能，以便将Cloudflare属性传递至您的内部系统，从而在您的下游系统中实现更好的日志记录和访问决策。

与此同时，基础构建模块现已就绪。外部评估规则、自定义设备状态检查、Gateway重定向以及Workers的全部功能现已可用。如果您不确定从何开始，我们的开发者文档提供了扩展Cloudflare One的指南和参考架构。

我们构建Cloudflare的信念是安全应该极其易于使用，但我们也深知“易用”并不意味着“一刀切”。它意味着为您提供工具，以精确构建您所需的功能。我们相信，这正是SASE的未来。

---

> 本文由AI自动翻译，原文链接：[The truly programmable SASE platform](https://blog.cloudflare.com/programmable-sase/)
> 
> 翻译时间：2026-03-03 04:48
