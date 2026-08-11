---
title: Vercel推出托管镜像，沙箱环境全面升级
title_original: Vercel Sandbox now runs on Vercel Managed Images - Vercel
date: '2026-08-10'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-sandbox-managed-images
author: ''
summary: Vercel宣布推出托管镜像（VMI），取代已弃用的Sandbox运行时。新镜像基于Ubuntu，内置Node.js、Python及多种编码Agent，默认安全且支持夜间自动更新。用户可选择通用、Node、Python、Ubuntu或Arch等不同镜像，并通过镜像摘要固定版本实现完全可复现的环境。迁移过程简单，现有代码仍兼容旧runtime属性。此举旨在提供更轻量、安全且灵活的沙箱运行环境。
categories:
- AI基础设施
tags:
- Vercel
- 托管镜像
- 沙箱
- 开发工具
- 云基础设施
draft: false
translated_at: '2026-08-11T03:38:03.966913'
---

今天我们推出Vercel托管镜像（VMI），这是一组带版本号的开源基础镜像，你可以直接使用或在此基础上进行扩展。每个镜像的源代码都存放在公共的`vercel/sandbox`仓库中。

托管镜像取代了现已弃用的Sandbox运行时。从Sandbox SDK第3版开始，新的沙箱默认使用`vercel/sandbox/universal:latest`镜像。该镜像内置了Node.js、Python、常见的编码Agent和标准工具，因此大多数用户无需构建自定义镜像或在启动时安装软件包。

通用镜像将我们的默认操作系统从Amazon Linux切换为Ubuntu，后者更轻量且在行业内应用更广泛。

### 默认安全

每个托管镜像都会获得夜间发布版本。滚动标签（如`latest`和主版本标签）会自动获取操作系统和依赖项更新，包括安全补丁以及Node.js、Python和预装编码Agent的新版本。

在每个发布版本中，依赖项会尽可能固定到特定版本，从而保证特定镜像版本的一致性。

如果你需要完全不可变、可复现的环境，请将镜像固定到镜像摘要（SHA）。固定到摘要的镜像将退出自动更新。

### 从目录中选择托管镜像

每个托管镜像针对不同的起点：

- `vercel/sandbox/universal:latest`是新的默认镜像，基于Ubuntu 26.04的滚动发布版本，包含Node.js 24、带`uv`的Python 3.14、`opencode`、`claude-code`、`codex`和`picoding` Agent，以及`git`、`vim`、`nano`、`tmux`、`ripgrep`、`jq`和`fzf`等工具。
- `vercel/sandbox/node:22`、`node:24`和`node:26`提供Ubuntu 26.04上的Node.js版本。
- `vercel/sandbox/python:3.14`提供Ubuntu 26.04上的Python。
- `vercel/sandbox/ubuntu:latest`提供基础Ubuntu 26.04，不包含额外工具。
- `vercel/sandbox/arch:latest`提供Arch Linux，定期更新，未预装Node.js或Python。其庞大的软件包仓库使其非常适合需要即时安装工具的Agent。

`vercel/sandbox/universal:latest`是新的默认镜像，基于Ubuntu 26.04的滚动发布版本，包含Node.js 24、带`uv`的Python 3.14、`opencode`、`claude-code`、`codex`和`picoding` Agent，以及`git`、`vim`、`nano`、`tmux`、`ripgrep`、`jq`和`fzf`等工具。

`vercel/sandbox/node:22`、`node:24`和`node:26`提供Ubuntu 26.04上的Node.js版本。

`vercel/sandbox/python:3.14`提供Ubuntu 26.04上的Python。

`vercel/sandbox/ubuntu:latest`提供基础Ubuntu 26.04，不包含额外工具。

`vercel/sandbox/arch:latest`提供Arch Linux，定期更新，未预装Node.js或Python。其庞大的软件包仓库使其非常适合需要即时安装工具的Agent。

### 引用镜像并从运行时迁移

沙箱可以使用你项目中任何仓库的镜像、已与你的团队共享的仓库或任何公共仓库中的镜像。

镜像通过完整路径`team-slug/project/repo:tag`来寻址，例如`vercel/sandbox/universal:latest`。SDK对`image`属性进行了类型定义，内置镜像支持自动补全，同时仍然接受任意字符串。之前的`runtime`属性已弃用但未移除，因此现有代码仍可正常工作。

Amazon Linux运行时不属于托管镜像目录，因此需要AL2023的团队可以继续使用`runtime`。托管镜像以默认的`ubuntu`或`arch`用户运行，并具有免密码sudo权限，而非`vercel-sandbox`用户。

```
1import { Sandbox } from '@vercel/sandbox';2
3const sandbox = await Sandbox.create({4  image: 'vercel/sandbox/python:3.14',5});
```

欢迎提交Issue或Pull Request来改进这些镜像，并阅读Vercel Sandbox镜像文档以开始使用。

## 贡献者

Kevin Sundstrom

---

> 本文由AI自动翻译，原文链接：[Vercel Sandbox now runs on Vercel Managed Images - Vercel](https://vercel.com/changelog/vercel-sandbox-managed-images)
> 
> 翻译时间：2026-08-11 03:38
