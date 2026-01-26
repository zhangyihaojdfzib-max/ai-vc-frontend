---
title: Shai-Hulud 2.0供应链攻击：npm包因账户被盗遭恶意植入
title_original: Shai-Hulud 2.0 Supply Chain Compromise  - Vercel
date: '2025-11-24'
source: Vercel Blog
source_url: https://vercel.com/changelog/shai-hulud-2-0-supply-chain-compromise
author: ''
summary: 多个npm软件包因开发者账户被接管而遭到供应链攻击。攻击者在package.json中植入隐蔽加载器，针对Bun运行时环境静默安装并执行恶意脚本。Vercel官方声明其自身系统及内部构建流程未受影响，但识别出少量客户构建引用了受感染包，已重置相关项目缓存并直接联系受影响客户提供缓解措施。事件凸显了开源软件供应链的安全风险。
categories:
- 技术趋势
tags:
- 供应链安全
- npm攻击
- 账户接管
- 恶意软件包
- Vercel
draft: false
translated_at: '2026-01-26T05:04:26.229769'
---

多个来自不同网络服务的 npm 软件包因账户接管/开发者账号被盗而遭到破坏。恶意攻击者得以在 package.json 文件中添加一个隐蔽的加载器，该加载器会定位 Bun 运行时环境，静默安装并执行恶意脚本。

我们的调查显示，没有任何 Vercel 环境受到影响，我们正在通知一小部分构建受影响的相关客户。

### 对 Vercel 客户的影响

Vercel 已立即采取措施为客户解决此问题。作为初步步骤，我们重置了所有引入了易受攻击软件包的项目的缓存，同时我们仍在继续调查是否有任何加载器成功运行。

- 截至本文发布时，**没有任何 Vercel 管理的系统或内部构建流程**受到影响。
- 初步分析**识别出**一小部分引用了受感染软件包的 Vercel 客户构建。
- 我们正在直接联系受影响的客户，并提供详细的缓解步骤。

截至本文发布时，**没有任何 Vercel 管理的系统或内部构建流程**受到影响。

初步分析**识别出**一小部分引用了受感染软件包的 Vercel 客户构建。

我们正在直接联系受影响的客户，并提供详细的缓解步骤。

我们将在调查过程中持续发布更新。

---

> 本文由AI自动翻译，原文链接：[Shai-Hulud 2.0 Supply Chain Compromise  - Vercel](https://vercel.com/changelog/shai-hulud-2-0-supply-chain-compromise)
> 
> 翻译时间：2026-01-26 05:04
