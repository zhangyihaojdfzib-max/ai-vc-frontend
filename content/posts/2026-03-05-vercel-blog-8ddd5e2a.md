---
title: Vercel AI Gateway新增提供商超时设置，加速故障转移
title_original: Customize timeouts for faster automatic failover on Vercel AI Gateway
  - Vercel
date: '2026-03-05'
source: Vercel Blog
source_url: https://vercel.com/changelog/provider-level-custom-timeouts-for-faster-failover-on-ai-gateway
author: ''
summary: Vercel AI Gateway推出按推理设置提供商超时功能，允许用户为不同AI服务提供商配置独立的超时时间（以毫秒计）。当某个提供商未在指定时间内开始响应时，网关将自动中止请求并切换到下一个可用提供商，从而实现比默认设置更快的故障转移。该功能目前处于测试阶段，主要支持自带密钥（BYOK）凭证，适用于多提供商故障转移场景，用户可结合调用顺序（order）配置来优化响应速度和可靠性。需要注意的是，部分提供商可能不支持流式取消，超时请求仍可能产生费用。
categories:
- AI基础设施
tags:
- Vercel
- AI Gateway
- 故障转移
- 超时配置
- API管理
draft: false
translated_at: '2026-03-11T04:31:43.579631'
---

AI Gateway 现已支持按推理设置**提供商超时**，可实现比提供商默认设置更快速的故障转移。如果提供商未在配置的超时时间内开始响应，AI Gateway 将中止请求并回退至下一个可用提供商。

提供商超时功能目前处于测试阶段，仅适用于 BYOK（自带密钥）凭证，系统提供商超时支持即将推出。请注意，部分提供商不支持流式取消，因此根据提供商的不同，超时请求可能仍会产生费用。

**基本用法**

在 `providerOptions.gateway` 中使用 `providerTimeouts` 按提供商设置超时时间（毫秒）。

```
123const result = streamText({4  model: 'openai/gpt-5.4',5  prompt,6  providerOptions: {7    gateway: {8      providerTimeouts: {9        byok: { openai: 15000 }, 10      },11    },12  },13});
```

**多提供商与故障转移的高级用法**

结合 `order` 使用，可同时控制提供商调用顺序和故障转移速度。

```
123const result = streamText({4  model: 'anthropic/claude-sonnet-4.6',5  prompt,6  providerOptions: {7    gateway: {8      order: ['anthropic', 'bedrock', 'vertex'],9      providerTimeouts: {10        byok: {11          anthropic: 10000,12          bedrock: 15000,13        },14      },15    },16  },17});
```

此示例首先尝试 Anthropic（10 秒超时），若超时则回退至 Bedrock（15 秒超时），最后回退至 Vertex（使用网关默认超时设置）。

更多信息，请阅读自定义提供商超时**文档**。

---

> 本文由AI自动翻译，原文链接：[Customize timeouts for faster automatic failover on Vercel AI Gateway - Vercel](https://vercel.com/changelog/provider-level-custom-timeouts-for-faster-failover-on-ai-gateway)
> 
> 翻译时间：2026-03-11 04:31
