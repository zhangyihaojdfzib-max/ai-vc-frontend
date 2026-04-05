---
title: Vercel 原生集成 SvelteKit 服务端 OpenTelemetry 追踪
title_original: Native support for SvelteKit's new OpenTelemetry spans - Vercel
date: '2025-08-18'
source: Vercel Blog
source_url: https://vercel.com/changelog/native-support-for-sveltekits-new-opentelemetry-spans
author: ''
summary: Vercel 宣布直接集成 SvelteKit 全新的服务端 OpenTelemetry 追踪模块。开发者只需在 SvelteKit 配置中启用实验性追踪功能，并配合
  Vercel OpenTelemetry 收集器进行简单配置，即可在追踪会话中获取 SvelteKit 内置的详细性能数据。该集成有助于提升应用的可观测性，便于监控和分析服务器端性能，同时也支持配置其他收集器以满足不同需求。
categories:
- AI基础设施
tags:
- Vercel
- SvelteKit
- OpenTelemetry
- 可观测性
- 性能监控
draft: false
translated_at: '2026-04-05T04:46:57.873098'
---

Vercel现已直接集成SvelteKit全新的服务端OpenTelemetry追踪模块。

要开始使用，请在SvelteKit中启用实验性追踪功能：

```
12const config = {3	kit: { 4		experimental: {5			tracing: {6				server: true,7			},8			instrumentation: {9				server: true,10			}11		}12	}13};14
15export default config;
```

并使用Vercel OpenTelemetry收集器创建追踪配置文件：

```
1import { registerOTel } from '@vercel/otel';2
3registerOTel({4	serviceName: 'my-sveltekit-app'5});
```

此后在追踪会话中生成的记录将包含SvelteKit内置的追踪模块。您也可以配置其他收集器。更多信息请参阅SvelteKit可观测性文档。

![SvelteKit集成追踪模块（绿色显示）位于Vercel基础设施追踪层下方。延迟效果仅为示意用途。](/images/posts/f93520ccb367.jpg)

---

> 本文由AI自动翻译，原文链接：[Native support for SvelteKit's new OpenTelemetry spans - Vercel](https://vercel.com/changelog/native-support-for-sveltekits-new-opentelemetry-spans)
> 
> 翻译时间：2026-04-05 04:46
