---
title: Box Mount now runs in Vercel Sandbox - Vercel
title_original: Box Mount now runs in Vercel Sandbox - Vercel
date: '2026-10-28'
source: Vercel Blog
source_url: https://vercel.com/changelog/box-mount-now-runs-in-vercel-sandbox
author: ''
summary: '[翻译失败，原文如下]


  Box Mount lets agents running in Vercel Sandbox read and write Box files through
  standard filesystem operations. It syncs a Box folder wi...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-29T08:15:48.694231'
---

[翻译失败，原文如下]

Box Mount lets agents running in Vercel Sandbox read and write Box files through standard filesystem operations. It syncs a Box folder with a directory inside the sandbox. Unmount before you stop the sandbox, and everything the agent wrote is in Box after the sandbox is deleted.

The contract-review example uses AI Gateway to review a synthetic contract in Vercel Sandbox and save the review back to Box. The sync process and agent run as separate sandbox users, keeping the Box credentials separate from the agent's workspace.

Box Mount is in private preview. Request access from Box, then follow theBox Mount documentationto set it up in Vercel Sandbox.

---

> 本文由AI自动翻译，原文链接：[Box Mount now runs in Vercel Sandbox - Vercel](https://vercel.com/changelog/box-mount-now-runs-in-vercel-sandbox)
> 
> 翻译时间：2026-10-29 08:15
