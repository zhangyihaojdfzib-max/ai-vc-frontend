---
title: Send feedback from the Vercel MCP - Vercel
title_original: Send feedback from the Vercel MCP - Vercel
date: '2026-10-23'
source: Vercel Blog
source_url: https://vercel.com/changelog/send-feedback-from-vercel-mcp
author: ''
summary: '[翻译失败，原文如下]


  Vercel MCPnow includessubmit_feedback, a tool for sending bug reports, friction
  reports, and feature requests directly to the Vercel team...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-24T07:04:54.308508'
---

[翻译失败，原文如下]

Vercel MCPnow includessubmit_feedback, a tool for sending bug reports, friction reports, and feature requests directly to the Vercel team from your agent or harness.

Ask your agent to give feedback in plain language:

Send Vercel feedback that the deployment error didn't explain which environment variable was missing.

Your assistant can attach structured context that describes the task, the expected behavior, and what went wrong:

```
1{2  "message": "The deployment error didn't name the missing environment variable",3  "context": {4    "tool": "deploy_to_vercel",5    "task": "Deploy a preview",6    "expected": "An error identifying the missing variable",7    "actual": "Build failed without naming the variable",8    "type": "bug"9  }10}
```

The tool requires sign-in, and it sends feedback only when you ask your agent to share it.

Connect your agent to Vercel MCP and read thesubmit_feedback documentationto get started.

---

> 本文由AI自动翻译，原文链接：[Send feedback from the Vercel MCP - Vercel](https://vercel.com/changelog/send-feedback-from-vercel-mcp)
> 
> 翻译时间：2026-10-24 07:04
