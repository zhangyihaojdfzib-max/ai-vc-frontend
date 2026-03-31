---
title: Nx包供应链攻击：恶意脚本窃取开发者凭证
title_original: 's1ngularity: supply chain attack in Nx packages - Vercel'
date: '2025-08-27'
source: Vercel Blog
source_url: https://vercel.com/changelog/s1ngularity-supply-chain-attack-in-nx-packages
author: ''
summary: 2025年8月26日起，攻击者利用被盗npm令牌发布了Nx及其生态库的恶意版本。这些包包含postinstall脚本，安装时会使用大语言模型扫描用户文件系统，窃取密钥和凭证并上传至攻击者创建的GitHub仓库。Vercel默认构建环境不受影响，但使用自定义构建流程并安装了特定CLI工具的用户可能面临风险。Nx团队已从npm移除受感染包，并建议开发者检查本地及其他CI环境。
categories:
- AI基础设施
tags:
- 供应链攻击
- npm安全
- 开发安全
- 凭证窃取
- 构建安全
draft: false
translated_at: '2026-03-31T05:06:05.646765'
---

威胁行为者向 npm 注册表发布了 Nx 包及其部分支持库的修改版本，目的是窃取开发者和服务的凭证。

Vercel 上的构建默认不受此漏洞影响。请访问 GitHub 安全公告，检查您的本地或其他 CI 环境是否受到影响。

## 摘要

从 2025 年 8 月 26 日美国东部时间下午 6:32 开始，攻击者利用被盗的 npm 令牌，向 npm 注册表发布了 Nx 包及部分 Nx 生态库的恶意版本。Nx 团队已将这些受感染的包从 npm 注册表中移除，移除工作于同日美国东部时间晚上 10:44 结束。

受影响的包包含一个 `postinstall` 脚本，该脚本在安装受影响的包时，会使用 LLM（大语言模型）扫描用户的文件系统，以窃取密钥和凭证。被窃取的密钥会以编码字符串的形式发布到脚本将在受害者 GitHub 账户中创建的 GitHub 仓库中。更多信息，请访问 Nx 团队在 GitHub 上的安全公告。

## 对 Vercel 客户的影响

默认情况下，Vercel 客户不受影响，只有在他们利用构建容器的灵活性采取了特定步骤时，才可能受到受感染的 Nx 包的影响。

要使 `postinstall` 脚本从 Vercel 构建中窃取数据，需要满足以下四个条件：

1.  脚本使用 GitHub CLI (`gh`) 获取 GitHub 令牌。GitHub CLI 默认未安装在 Vercel 的构建容器中。若要在您的构建中使用 GitHub CLI，必须将其作为用户自定义构建过程的一部分进行安装。
2.  脚本要求调用 GitHub CLI 的机器上存在 GitHub 身份验证令牌。Vercel 构建容器默认不包含客户的 GitHub 令牌。若要在您的构建中使用 GitHub 令牌，必须将其作为用户自定义构建过程的一部分添加到构建容器中。
3.  脚本依赖于机器上至少安装了 Claude Code (`claude`)、Gemini (`gemini`) 或 Q (`q`) CLI 其中之一。Vercel 构建容器默认未安装任何这些 CLI。若要在您的构建中使用这些 CLI，必须将其作为用户自定义构建过程的一部分进行安装。
4.  构建必须安装了受感染的 Nx 或 Nx 生态包版本。

我们未在 Vercel 上发现任何符合此模式的构建。我们建议您评估可能受此攻击影响的其他环境，包括本地环境和云端环境。

## 解决方案

新的构建将无法下载受影响的包。Nx 团队已从 npm 中移除受影响的包，并且我们已经清除了在构建期间依赖项中包含受影响包的任何项目的构建缓存。

此外，我们已经通知了在构建期间安装了一个或多个恶意包的少数用户。Vercel 团队所有者应检查来自 security@vercel.com 的标题为 "s1ngularity: supply chain attack in Nx packages" 的电子邮件。

## 参考资料

-   Nx 团队的 GitHub 安全公告

---

> 本文由AI自动翻译，原文链接：[s1ngularity: supply chain attack in Nx packages - Vercel](https://vercel.com/changelog/s1ngularity-supply-chain-attack-in-nx-packages)
> 
> 翻译时间：2026-03-31 05:06
