---
title: GitHub Copilot is now available in the AI SDK harness layer - Vercel
title_original: GitHub Copilot is now available in the AI SDK harness layer - Vercel
date: '2026-09-10'
source: Vercel Blog
source_url: https://vercel.com/changelog/github-copilot-ai-sdk-harness-adapter
author: ''
summary: '[翻译失败，原文如下]


  TheAI SDK harness layernow supports GitHub Copilot through the official@ai-sdk/harness-github-copilotadapter.
  The harness layer lets your...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-20T07:20:58.950807'
---

[翻译失败，原文如下]

TheAI SDK harness layernow supports GitHub Copilot through the official@ai-sdk/harness-github-copilotadapter. The harness layer lets your application run different coding agents through the sameHarnessAgentinterface, so you can switch agents without changing your application code.

PassgithubCopilottoHarnessAgent:

```
1import { HarnessAgent } from '@ai-sdk/harness/agent';2import { githubCopilot } from '@ai-sdk/harness-github-copilot';3
4const agent = new HarnessAgent({5  harness: githubCopilot,6});
```

Create a HarnessAgent that runs GitHub Copilot.

Under the hood, the adapter uses@ai-sdk/harness-acpto connect GitHub Copilot toHarnessAgentthrough the Agent Client Protocol (ACP).

Supported harnesses now include, in addition to GitHub Copilot, Claude Code, Cline, Codex, Cursor, Deep Agents, fx, Grok Build, OpenCode, and Pi, with more coming soon.

Read theGitHub Copilot harness documentationto get started.

---

> 本文由AI自动翻译，原文链接：[GitHub Copilot is now available in the AI SDK harness layer - Vercel](https://vercel.com/changelog/github-copilot-ai-sdk-harness-adapter)
> 
> 翻译时间：2026-09-20 07:20
