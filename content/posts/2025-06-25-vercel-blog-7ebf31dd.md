---
title: Vercel BotID 正式发布：无需验证码的无形机器人防护
title_original: Vercel BotID is now generally available - Vercel – Vercel
date: '2025-06-25'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-botid-is-now-generally-available
author: ''
summary: Vercel 正式推出 BotID，一种由 Kasada 提供支持的无形验证码解决方案。它专为保护公开、高价值的路由（如结账、注册、AI聊天界面和API）而设计，无需可见的验证挑战。BotID
  通过静默收集数千种信号、在每次页面加载时变异检测逻辑来区分人类与机器人，并利用全球机器学习网络实时增强防护。它提供类型安全的 SDK，支持客户端检测与服务端验证，设置简单，无需手动调优，防护数据可在防火墙仪表板中直观查看。
categories:
- AI基础设施
tags:
- Vercel
- BotID
- 机器人防护
- 网络安全
- 机器学习
draft: false
translated_at: '2026-04-17T04:53:39.366762'
---

Vercel BotID 是一种无形的验证码，无需可见的验证挑战或手动管理机器人。

BotID 是 Vercel 上全新的防护层，专为公开、高价值的路由设计，例如结账、注册、AI 聊天界面、LLM（大语言模型）驱动的端点以及易受模仿真实用户行为的复杂机器人攻击的公共 API。

与基于 IP 或启发式系统不同，BotID：

*   静默收集数千种信号以区分人类用户与机器人
*   在每次页面加载时变异这些检测，规避逆向工程和复杂的绕过手段
*   将攻击数据流式传输到全球机器学习网络中，共同为所有客户增强防护

静默收集数千种信号以区分人类用户与机器人

在每次页面加载时变异这些检测，规避逆向工程和复杂的绕过手段

将攻击数据流式传输到全球机器学习网络中，共同为所有客户增强防护

由 **Kasada** 提供支持，BotID 通过类型安全的 SDK 集成到您的应用中：

*   使用 `<BotIdClient>` 组件进行客户端检测
*   使用 `checkBotId` 函数进行服务端验证
*   自动标记被拦截会话的日志和遥测数据

使用 `<BotIdClient>` 组件进行客户端检测

使用 `checkBotId` 函数进行服务端验证

自动标记被拦截会话的日志和遥测数据

```
1import { checkBotId } from "botid/server";2
3export async function POST(req: Request) {4  const { isBot } = await checkBotId();5
6  if (isBot) {7    return new Response("Access Denied", { status: 403 });8  }9
10  const result = await expensiveOrCriticalOperation();11
12  return new Response("Success!");13}
```

设置简单，无需配置文件或调优。安装软件包、设置重写规则、挂载客户端并在服务端验证请求。

BotID 流量可在防火墙仪表板中查看，并可依据判定结果（通过或失败）、用户代理、国家/地区、IP 地址、请求路径、目标路径、JA4 摘要和主机进行筛选。

阅读**公告**或**文档**以了解更多信息，或立即试用 BotID。

开始使用 Vercel BotID

在高级机器人触及您最敏感的路由（如登录、结账、AI Agent（智能体）和 API）之前检测并阻止它们。易于实施，难以绕过。

开始使用

---

> 本文由AI自动翻译，原文链接：[Vercel BotID is now generally available - Vercel – Vercel](https://vercel.com/changelog/vercel-botid-is-now-generally-available)
> 
> 翻译时间：2026-04-17 04:53
