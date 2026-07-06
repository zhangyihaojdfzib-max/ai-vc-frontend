---
title: Vercel Sandbox 新增 FUSE 支持，挂载远程存储更便捷
title_original: Vercel Sandbox now supports FUSE-based filesystems - Vercel
date: '2026-07-03'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-sandbox-now-supports-fuse-based-filesystems
author: ''
summary: Vercel Sandbox 现已支持 FUSE（用户空间文件系统），允许用户在运行的沙箱中挂载远程存储和自定义文件系统，如 S3 存储桶或网络文件系统。通过这一功能，开发者可以直接从对象存储流式传输大型数据集、在沙箱间共享状态，或针对远程源运行需要
  POSIX 路径的工具，而无需预先复制数据。文章提供了使用 mount-s3 挂载 S3 存储桶的代码示例，展示了如何通过简单的 API 调用实现远程存储的集成。
categories:
- AI基础设施
tags:
- Vercel
- FUSE
- 远程存储
- 沙箱
- S3
draft: false
translated_at: '2026-07-06T06:51:55.700559'
---

Vercel Sandbox 现在支持 FUSE，让你可以在运行的 Sandbox 中挂载远程存储和自定义文件系统。用它来将 S3 存储桶、网络文件系统或任何其他兼容 FUSE 的驱动程序挂载为常规路径。

```
1import { Sandbox } from '@vercel/sandbox';2
3const sandbox = await Sandbox.create();4
56await sandbox.runCommand({7  sudo: true,8  cmd: 'dnf',9  args: [10    'install',11    '-y',12    'fuse',13    'https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm',14  ],15});16
17const MOUNT_DIR = '/mnt/s3'18
19await sandbox.runCommand({20  sudo: true, cmd: 'mkdir', args: ['-p', MOUNT_DIR]21});22
23242526await sandbox.runCommand({27  sudo: true,28  cmd: 'mount-s3',29  args: [30    process.env.S3_BUCKET_NAME,31    MOUNT_DIR,32    '--allow-other',33  ],34  env: {35    AWS_ACCESS_KEY_ID: process.env.AWS_ACCESS_KEY_ID,36    AWS_SECRET_ACCESS_KEY: process.env.AWS_SECRET_ACCESS_KEY,37    AWS_SESSION_TOKEN: process.env.AWS_SESSION_TOKEN,38    AWS_REGION: process.env.AWS_REGION39  },40});41
4243await sandbox.runCommand({44  cmd: 'ls',45  args: ['-la', MOUNT_DIR],46  stdout: process.stdout,47});48
49await sandbox.stop();
```

在 Vercel Sandbox 中运行 s3fs

这使得你可以直接从对象存储流式传输大型数据集，通过公共文件系统在 Sandbox 之间共享状态，或者针对远程源运行需要 POSIX 路径的工具，而无需先将数据复制到 Sandbox 中。

在文档中了解更多关于远程存储挂载的信息。

---

> 本文由AI自动翻译，原文链接：[Vercel Sandbox now supports FUSE-based filesystems - Vercel](https://vercel.com/changelog/vercel-sandbox-now-supports-fuse-based-filesystems)
> 
> 翻译时间：2026-07-06 06:51
