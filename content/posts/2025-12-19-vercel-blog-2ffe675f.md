---
title: Vercel推出vercel.ts：以代码方式配置项目，实现类型安全与动态逻辑
title_original: 'Introducing vercel.ts: Programmatic project configuration - Vercel'
date: '2025-12-19'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-ts
author: Authors
summary: Vercel正式推出基于TypeScript的新型配置文件vercel.ts，取代传统的静态JSON配置。该方案为项目配置带来了完全的类型安全、支持动态逻辑（如访问环境变量、条件行为）以及更好的开发者体验。用户可通过代码定义高级路由、请求转换、缓存规则和定时任务等功能，并利用新的@vercel/config包增强配置能力。所有Vercel项目现均可使用.ts、.js等文件进行配置，且属性定义与原有vercel.json完全兼容，支持平滑迁移。
categories:
- 技术趋势
tags:
- Vercel
- TypeScript
- 项目配置
- 开发者工具
- 前端工程化
draft: false
---

1 分钟阅读
Vercel 现已支持 vercel.ts
，这是一种基于 TypeScript 的新型配置文件，为项目配置带来了类型安全、动态逻辑和更好的开发者体验。
vercel.ts
允许您通过定义高级路由、请求转换、缓存规则和定时任务，将配置表达为代码，超越了静态 JSON 所能表达的范围。除了完全的类型安全外，这还允许访问环境变量、共享逻辑和条件行为。
现在所有项目都可以使用 vercel.ts
（或 .js
、.mjs
、.cjs
、.mts
）进行项目配置。属性的定义方式与 vercel.json
完全相同，并且可以使用新的 @vercel/config
包进行增强。
import { type VercelConfig, routes, deploymentEnv } from '@vercel/config/v1';
export const config: VercelConfig = { framework: 'nextjs',
crons: [ { path: '/api/cleanup', schedule: '0 0 * * *' }, { path: '/api/sync-users', schedule: '*/15 * * * *' }, ],
rewrites: [ routes.rewrite('/(.*)', 'https://external-api.com', { requestHeaders: { 'proxy-header': deploymentEnv('PROXY_HEADER') } }), ],};
尝试使用演练场来探索 vercel.ts
，了解如何从现有的 vercel.json 迁移，或阅读文档和 @vercel/config 包。

---

> 本文由AI自动翻译，原文链接：[Introducing vercel.ts: Programmatic project configuration - Vercel](https://vercel.com/changelog/vercel-ts)
> 
> 翻译时间：2026-01-05 17:27
