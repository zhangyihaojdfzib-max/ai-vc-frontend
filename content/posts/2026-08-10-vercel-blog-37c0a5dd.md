---
title: deepsec一键初始化，安全审查更简单
title_original: Simplified onboarding for deepsec - Vercel
date: '2026-08-10'
source: Vercel Blog
source_url: https://vercel.com/changelog/simplified-onboarding-for-deepsec
author: ''
summary: Vercel推出的开源安全审查工具deepsec新增init命令，实现一键式仓库设置与首次安全审查。该命令自动创建隔离工作区、配置模型访问、生成代码库描述、补充扫描模式并启动AI审查，全程设置检查点，中断后可断点续跑。此举大幅降低安全审查门槛，提升开发者效率。
categories:
- AI产品
tags:
- deepsec
- 安全审查
- Vercel
- 开发者工具
- AI自动化
draft: false
translated_at: '2026-08-11T03:38:00.228151'
---

deepsec 是 Vercel 推出的开源安全审查工具，现在只需一条命令即可设置仓库并运行首次安全审查。

```
npx deepsec init
```

从仓库根目录初始化 deepsec

`init` 命令现在自动化了标准设置流程：

- 创建隔离的 `.deepsec/workspace` 目录（这是唯一添加到仓库的内容），并安装其依赖
- 通过 Vercel AI Gateway 或您自己的提供商密钥配置模型访问
- 生成代码库及其攻击面的描述，后续每次审查都依赖此描述
- 运行模式扫描，在内置模式覆盖不足的地方生成额外的扫描模式
- 启动对标记文件的 AI 审查

创建隔离的 `.deepsec/workspace` 目录（这是唯一添加到仓库的内容），并安装其依赖

通过 Vercel AI Gateway 或您自己的提供商密钥配置模型访问

生成代码库及其攻击面的描述，后续每次审查都依赖此描述

运行模式扫描，在内置模式覆盖不足的地方生成额外的扫描模式

启动对标记文件的 AI 审查

每个步骤完成后都会设置检查点。如果运行中断——无论是由于关闭进程、某一步骤失败，还是达到成本或时长限制——重新运行 `init` 都会从最后完成的步骤继续。

运行 `npx deepsec init` 开始您的首次扫描，或阅读文档了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Simplified onboarding for deepsec - Vercel](https://vercel.com/changelog/simplified-onboarding-for-deepsec)
> 
> 翻译时间：2026-08-11 03:38
