---
title: Vercel BotID 深度分析模式现集成已验证机器人目录
title_original: Vercel BotID now leverages Vercel's verified bot directory - Vercel
date: '2025-08-12'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-botid-now-leverages-vercels-verified-bot-directory
author: ''
summary: Vercel BotID 自 1.5.0 版本起，其深度分析模式开始利用 Vercel 官方维护的已验证机器人目录，为开发者提供更精准的机器人识别能力。该更新不仅能够实时检测已验证的机器人（如
  ChatGPT-Operator），还提供机器人的源 IP 范围、反向 DNS 及用户代理等额外上下文信息。这使得开发者可以安全地放行对业务有益的已知机器人（例如代表用户完成购买的智能体），同时有效阻止恶意机器人和复杂滥用行为。BotID
  作为一种无形的验证码，在保障用户体验的同时，帮助开发者基于机器人身份做出更精细的程序化决策。
categories:
- AI基础设施
tags:
- Vercel
- BotID
- 机器人检测
- 网络安全
- 开发者工具
draft: false
translated_at: '2026-04-06T04:54:34.584808'
---

自 inbotid@1.5.0 版本起，BotID 的深度分析模式基于 Vercel 的已知且已验证的机器人目录，为已验证的机器人提供认证信息。这使得开发者能够实时检测已验证的机器人，并根据机器人身份做出程序化决策。

这使您可以安全地允许对您的业务有益的已知机器人（例如代表用户进行购买的 Agent（智能体）机器人），同时阻止其他机器人和复杂的滥用行为。

BotID 是一种无形的验证码，可在不打扰真实用户的情况下对复杂机器人进行分类。通过此更新，使用深度分析的开发者现在可以获得关于机器人本身的额外上下文信息，例如源 IP 范围、反向 DNS 和用户代理验证，帮助团队在采取行动之前微调处理机器人的方式。

```
1import { checkBotId } from "botid/server";2 3export async function POST(request: Request) {4  const botResult = await checkBotId();5 6  const { isBot, verifiedBotName, isVerifiedBot, verifiedBotCategory } = botResult;7 8  9  const isOperator = isVerifiedBot && verifiedBotName === "chatgpt-operator";10 11  if (isBot && !isOperator) {12    return Response.json({ error: "Access denied" }, { status: 403 });13  }14 15  16  return Response.json(botResult);17}
```

允许 ChatGPT-Operator 访问的示例

开始使用 BotID 并查看 BotID 中关于已验证机器人的文档。

---

> 本文由AI自动翻译，原文链接：[Vercel BotID now leverages Vercel's verified bot directory - Vercel](https://vercel.com/changelog/vercel-botid-now-leverages-vercels-verified-bot-directory)
> 
> 翻译时间：2026-04-06 04:54
