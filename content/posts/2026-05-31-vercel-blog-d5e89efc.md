---
title: MiniMax M3模型登陆Vercel AI Gateway
title_original: MiniMax M3 on AI Gateway - Vercel
date: '2026-05-31'
source: Vercel Blog
source_url: https://vercel.com/changelog/minimax-m3-on-ai-gateway
author: ''
summary: MiniMax M3模型现已在Vercel AI Gateway上可用，该模型拥有100万Token上下文窗口和原生多模态能力，基于稀疏注意力技术构建。M3在软件工程、终端工具使用和智能体网络浏览方面有所改进，并针对多轮协作进行了优化。AI
  Gateway提供统一的API调用、使用追踪、成本管理、重试和故障转移等功能，支持零数据保留和动态提供商排序，且无加价。
categories:
- AI产品
tags:
- MiniMax
- M3
- Vercel AI Gateway
- 多模态
- 上下文窗口
draft: false
translated_at: '2026-06-01T06:54:51.398230'
---

MiniMax M3 现已在 Vercel AI Gateway 上可用。

M3 是 MiniMax 首款拥有 100 万 Token 上下文窗口和原生多模态能力的模型，基于 MiniMax 稀疏注意力（MSA）构建。

M3 在软件工程、基于终端的工具使用以及 Agent（智能体）网络浏览方面有所改进，并针对多轮协作进行了调优。

要使用 MiniMax M3，请在 AI SDK 中将模型设置为 `minimax/minimax-m3`。

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'minimax/minimax-m3',5  prompt: 'Reproduce the bug in this GitHub issue and submit a fix.',6});
```

在提示词旁传递一张图片，即可使用 M3 的多模态输入功能：

```
1import { streamText } from 'ai';2
3const result = streamText({4  model: 'minimax/minimax-m3',5  messages: [6    {7      role: 'user',8      content: [9        {10          type: 'text',11          text: 'This is a screenshot of a failing test. Identify the root cause and write the patch.',12        },13        {14          type: 'image',15          image: 'https://example.com/failing-test.png',16        },17      ],18    },19  ],20});
```

AI Gateway 提供统一的 API，用于调用模型、跟踪使用情况和成本，并配置重试、故障转移以及性能优化，以实现高于提供商正常运行时间的可用性。它包含内置的自定义报告、零数据保留支持、按延迟和成本动态排序提供商等功能。AI Gateway 反映提供商定价，无加价，且不针对推理收取平台费用，包括自带密钥（BYOK）请求。

了解更多关于 AI Gateway 的信息，查看 AI Gateway 模型排行榜，或在我们的模型游乐场中试用。

---

> 本文由AI自动翻译，原文链接：[MiniMax M3 on AI Gateway - Vercel](https://vercel.com/changelog/minimax-m3-on-ai-gateway)
> 
> 翻译时间：2026-06-01 06:54
