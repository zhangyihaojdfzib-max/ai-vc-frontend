---
title: AI Gateway 推出团队级提供商白名单功能
title_original: Team-wide provider allowlist on AI Gateway - Vercel
date: '2026-05-28'
source: Vercel Blog
source_url: https://vercel.com/changelog/team-wide-provider-allowlist-on-ai-gateway
author: ''
summary: Vercel 的 AI Gateway 新增团队级别的提供商允许列表功能，允许团队限制哪些 AI 提供商可以处理请求，确保流量仅路由至已批准的供应商。该功能在网关层面强制执行，开发者或编码
  Agent 无法绕过，仅团队所有者可修改列表。启用后新提供商默认禁用，防止未经批准的供应商悄然接入。支持 AI SDK、OpenAI 和 Anthropic 等
  API 格式，与零数据保留等安全功能协同工作。
categories:
- AI基础设施
tags:
- AI Gateway
- 安全合规
- 提供商管理
- Vercel
- 团队权限
draft: false
translated_at: '2026-05-29T06:13:18.741449'
---

AI Gateway 现已支持团队级别的提供商允许列表。团队可以限制哪些提供商能够处理请求，从而确保流量仅路由至已批准的提供商。该允许列表适用于通过 AI Gateway 发出的所有请求，包括自带密钥（BYOK）流量。

受监管的团队通常会在安全与法律审批通过后，从多个维度对 AI 提供商进行审查，最终形成一套符合其组织特定需求的供应商名单。允许列表将这份已批准的供应商名单转化为路由保障：

- 执行发生在网关层面，而非请求层面。团队中的开发者无法将流量路由至组织未批准的提供商。
- 此限制同样适用于编码 Agent（智能体）。即使 Agent（智能体）忽略或修改了请求级别的提供商过滤器，AI Gateway 仍会阻止未批准的提供商。
- 仅团队所有者可以修改提供商允许列表，从而保持控制的集中性和可审计性。
- 一旦启用允许列表，新提供商默认被禁用，因此当 AI Gateway 集成新供应商时，已批准的供应商集合不会悄然扩大。

执行发生在网关层面，而非请求层面。团队中的开发者无法将流量路由至组织未批准的提供商。

此限制同样适用于编码 Agent（智能体）。即使 Agent（智能体）忽略或修改了请求级别的提供商过滤器，AI Gateway 仍会阻止未批准的提供商。

仅团队所有者可以修改提供商允许列表，从而保持控制的集中性和可审计性。

一旦启用允许列表，新提供商默认被禁用，因此当 AI Gateway 集成新供应商时，已批准的供应商集合不会悄然扩大。

## 链接到标题如何配置

![](/images/posts/faf914361edb.jpg)

![](/images/posts/74257b7af8cb.jpg)

在 AI Gateway 的“设置”选项卡中，开启“提供商允许列表”。默认情况下，所有当前提供商均被允许，因此现有流量不受影响。禁用你的团队不应使用的任何提供商。

允许列表按提供商过滤，而非按模型过滤。如果初始提供商失败，AI Gateway 会回退到同一模型的其他允许提供商。允许列表还与应用于团队的其他限制（如零数据保留（ZDR）或请求级别过滤）共同发挥作用。

例如，如果某个团队在其允许列表中禁用了 DeepSeek，并且某个请求将路由固定为仅使用 DeepSeek 提供商：

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'deepseek/deepseek-v4-pro',5  prompt,6  providerOptions: {7    gateway: {8      only: ['deepseek'],9    },10  },11});
```

移除除 DeepSeek 提供商之外的所有路由选项

由于 DeepSeek 不在允许列表中，AI Gateway 拒绝该请求。

```
1{2  "error": {3    "type": "no_providers_available",4    "message": "Your team has restricted access to this provider. Contact the owner of the account for more details. Providers considered: deepseek"5  }6}
```

访问不在允许列表中的提供商时出现的错误

提供商允许列表适用于 AI Gateway 支持的所有 API 格式，包括 AI SDK、OpenAI Chat Completions API 和 Anthropic Messages API。

阅读提供商允许列表文档以获取更多信息。有关其他账户级别的安全与合规功能，请查看零数据保留和禁止提示词训练文档。

---

> 本文由AI自动翻译，原文链接：[Team-wide provider allowlist on AI Gateway - Vercel](https://vercel.com/changelog/team-wide-provider-allowlist-on-ai-gateway)
> 
> 翻译时间：2026-05-29 06:13
