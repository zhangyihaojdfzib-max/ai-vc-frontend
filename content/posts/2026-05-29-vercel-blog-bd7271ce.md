---
title: Vercel Sandbox 现已支持运行 Docker 容器
title_original: Run Docker containers inside Vercel Sandbox - Vercel
date: '2026-05-29'
source: Vercel Blog
source_url: https://vercel.com/changelog/run-docker-containers-inside-vercel-sandbox
author: ''
summary: Vercel Sandbox 新增对 Docker 的支持，允许用户在沙箱内安装 Docker、启动守护进程并运行容器化应用，而无需影响主机系统。该功能适用于将
  Redis、Postgres 等容器化服务作为测试依赖、在部署前验证镜像或预览容器应用。结合持久化沙箱，Docker 安装和镜像可在会话间保留。此外，沙箱还新增了
  FUSE 文件系统驱动和 VPN 客户端支持，进一步扩展了使用场景。
categories:
- AI基础设施
tags:
- Vercel
- Docker
- 沙箱
- 容器化
- 开发者工具
draft: false
translated_at: '2026-05-30T05:46:37.045248'
---

Vercel Sandbox 现在支持在沙箱内安装和运行 Docker。Agent（智能体）可以构建容器、安装系统包以及修改文件，而无需触碰你的主机系统。

安装 Docker，启动守护进程，并运行一个容器化应用程序：

```
1import { Sandbox } from "@vercel/sandbox";2
3const sandbox = await Sandbox.create();4await sandbox.runCommand({5  sudo: true,  6  cmd: "dnf",  7  args: ["install", "-y", "docker"]8});9
1011await sandbox.runCommand({ sudo: true, cmd: "dockerd", detached: true });12await sandbox.runCommand({13  cmd: "sh", 14  args: [ "-lc",  "until sudo docker info >/dev/null 2>&1; do sleep 1; done"] 15});16
17await sandbox.runCommand({18  cmd: "docker",  19  args: [20    "run", "--rm", "-d",21    "--name", "redis",22    "redis:alpine"  23  ]24});25await sandbox.runCommand({26  cmd: "docker",  27  args: ["exec", "redis", "redis-cli", "PING" ]28});
```

沙箱中的 Docker 对于以下场景非常有用：将 Redis 或 Postgres 等容器化服务作为测试依赖项运行、在部署前验证容器镜像，或预览从容器提供的应用程序。结合持久化沙箱，Docker 安装和拉取的镜像可以在会话之间保留。

除了增加对 Docker 的支持外，沙箱现在还支持 FUSE 文件系统驱动程序和 VPN 客户端，从而解锁了无限的可能性，让用户可以构建更多功能。

在文档中了解更多关于这些新系统规格的信息。

---

> 本文由AI自动翻译，原文链接：[Run Docker containers inside Vercel Sandbox - Vercel](https://vercel.com/changelog/run-docker-containers-inside-vercel-sandbox)
> 
> 翻译时间：2026-05-30 05:46
