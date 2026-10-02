---
title: Vercel Agent now installs private packages from npm and custom registries -
  Vercel
title_original: Vercel Agent now installs private packages from npm and custom registries
  - Vercel
date: '2026-09-30'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-agent-now-installs-private-packages-from-npm-and-custom-registries
author: ''
summary: '[翻译失败，原文如下]


  Vercel Agent can install private dependencies from npm and custom registries using
  credentials stored as shared environment variables on ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-02T08:10:44.872987'
---

[翻译失败，原文如下]

Vercel Agent can install private dependencies from npm and custom registries using credentials stored as shared environment variables on Vercel.npm,pnpm, and classic Yarn running in Agent sessions authenticate as they do in Vercel builds.

To get started, add ashared environment variablefor Development or Preview:

- UseNPM_TOKENfor private packages hosted onregistry.npmjs.org.
- UseNPM_RCto configure custom or multiple registries.

UseNPM_TOKENfor private packages hosted onregistry.npmjs.org.

UseNPM_RCto configure custom or multiple registries.

Vercel Agent reads only team-shared variables, not project-scoped ones.Credential values stay outside the sandbox, so the agent cannot read them.

Learn more in theprivate dependencies docs.

---

> 本文由AI自动翻译，原文链接：[Vercel Agent now installs private packages from npm and custom registries - Vercel](https://vercel.com/changelog/vercel-agent-now-installs-private-packages-from-npm-and-custom-registries)
> 
> 翻译时间：2026-10-02 08:10
