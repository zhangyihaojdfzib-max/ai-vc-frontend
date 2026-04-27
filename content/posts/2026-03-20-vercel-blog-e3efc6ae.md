---
title: Vercel Sandbox SDK新增文件权限控制功能
title_original: Sandbox SDK adds file permission control - Vercel – Vercel
date: '2026-03-20'
source: Vercel Blog
source_url: https://vercel.com/changelog/sandbox-sdk-file-permissions
author: ''
summary: Vercel Sandbox SDK 1.9.0版本引入了文件权限控制功能，允许开发者在写入文件时通过`mode`属性直接设置权限，无需额外执行`chmod`命令。这一改进简化了在沙箱内创建可执行脚本或管理访问权限的操作，减少了往返开销，提升了开发效率。
categories:
- AI基础设施
tags:
- Vercel
- Sandbox SDK
- 文件权限
- 开发工具
- 沙箱
draft: false
translated_at: '2026-04-27T05:23:54.345076'
---

Vercel Sandbox SDK 1.9.0 现在支持在写入文件时直接设置文件权限。

通过向 `writeFiles` API 传递 `mode` 属性，您可以在单次操作中定义权限。

这消除了在沙箱内创建可执行脚本或管理访问权限时，额外执行 `chmod` 的往返开销。

```
1sandbox.writeFiles([{2  path: 'run.sh',3  content: '#!/bin/bash\necho "ready"',4  mode: 0o7555}]);
```

查看文档了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Sandbox SDK adds file permission control - Vercel – Vercel](https://vercel.com/changelog/sandbox-sdk-file-permissions)
> 
> 翻译时间：2026-04-27 05:23
