---
title: Nous Research如何利用BotID大规模拦截自动化滥用攻击
title_original: How Nous Research used BotID to block automated abuse at scale - Vercel
date: '2025-11-07'
source: Vercel Blog
source_url: https://vercel.com/blog/how-nous-research-used-botid-to-block-automated-abuse-at-scale
author: ''
summary: AI研究实验室Nous Research在免费开放其开源模型Hermes时，遭遇了自动化脚本通过数千虚假账号发起的高并发攻击，导致服务过载与成本激增。为解决此问题，Nous在重构系统后部署了Vercel
  BotID深度分析解决方案。BotID在注册门户和聊天界面实施分层防护，成功识别并拦截了一场导致流量激增3000%的协同攻击，有效阻止了自动化滥用，保障了服务稳定性与成本控制，且未影响真实用户体验。
categories:
- AI基础设施
tags:
- 机器人防护
- AI滥用
- Vercel BotID
- 网络安全
- 开源模型
draft: false
translated_at: '2026-02-01T20:45:14.658711'
---

AI实验室Nous Research为提升可访问性，将其开源语言模型Hermes免费开放一周。几天内，自动化脚本通过数千个虚假账号发起高并发推理请求以绕过速率限制，导致服务不堪重负。

尽管已部署Cloudflare Turnstile防护，批量注册仍持续发生。这种滥用行为导致推理算力浪费和身份提供商费用激增。推广活动结束后，Nous意识到在重新推出任何免费服务前，必须部署更强大的机器人防护层。

**免费BotID深度分析**

企业版和专业版团队可在1月15日前免费使用Vercel BotID深度分析

立即阅读

## 关于Nous Research

Nous Research是一家AI研究实验室，管理多个应用型AI研究领域，包括名为Hermes的大语言模型系列。虽然任何人都可以免费下载和运行Hermes，但Nous还提供了托管聊天界面和推理API，让用户无需任何前期设置即可通过简单直接的方式与模型交互。

## 免费推广期间遭遇的意外滥用

在为期一周的Hermes免费推理推广期间，应用滥用者通过编程方式与聊天产品交互。脚本运行数据生成提示词，并将负载分散到数千个虚假账户以绕过速率限制。

尽管已部署Cloudflare Turnstile进行注册防护，这种滥用仍导致推理算力浪费和身份提供商费用激增。

## 为安全与效率重构系统

Nous借此机会重构了注册和聊天流程。在重新启动推广活动前，Nous采用了**Vercel BotID深度分析**——我们最先进的机器人防护解决方案，能精准识别模仿人类行为的机器人。BotID作为隐形验证码，可在不干扰用户体验的情况下完成验证。

他们在门户网站和聊天界面的关键检查点部署了BotID：

- **门户（认证流程）**：BotID检查在用户注册或登录前后同时运行，失败的检查将立即中止流程
- **聊天（UI层）**：为防止聊天应用遭受API式滥用，Nous实施了心跳机制。聊天客户端通过tRPC触发定期BotID检查，成功的检查结果将在后端短暂缓存。仅当存在近期人类验证记录时，推理请求才会继续执行

这种分层防护方法同时保护了入口点和持续的应用交互，确保了安全性与成本效益。

## BotID成功拦截导致流量激增3000%的协同攻击

10月16日澳大利亚东部时间中午12点左右，Nous低调重新开放免费服务而未进行营销推广。几天内，Vercel BotID检测并缓解了一场协同攻击——攻击者发现开放聊天界面后试图进行利用。

![](/images/posts/d546ee1bab04.jpg)

![](/images/posts/253547cac197.jpg)

流量峰值显示出几个关键攻击特征：

- 5-6个IP地址产生了大部分负载，辅以大量次要来源
- 大部分流量源自日本
- 3-4种不同的JA4哈希值在多次攻击尝试中具有关联性

BotID识别并拦截该流量后，攻击持续两小时直至攻击者意识到无法执行任何推理而停止。流量峰值期间，Nous聊天应用的访问量激增3000%。尽管出现数千次注册尝试，推理流量和系统可用性始终保持稳定。

值得注意的是，BotID在登录门户标记为"人类"的相同JA4指纹，后来成为聊天界面中被拦截最多的模式。这凸显了复杂攻击者如何调整攻击模式，而BotID的深度行为分析提供了超越表面防护的自适应防御。

## BotID如何在不影响真实用户的情况下防止滥用

通过在用户流程的多个节点部署Vercel BotID，Nous Research成功阻止了可能影响基础设施的大规模自动化滥用，减少了推理成本浪费，并在不牺牲安全性或用户体验的前提下维持了免费服务的应用可用性。由于BotID能自动响应，Nous无需投入宝贵时间和资源处理流量问题。现在他们可以继续安全地为全球用户提供免费开源的大语言模型托管服务。

**保护核心路径免受自动化滥用**

在高级机器人触及登录、AI推理和API等敏感路径前进行检测拦截。易于实施，难以绕过。

立即开始

---

> 本文由AI自动翻译，原文链接：[How Nous Research used BotID to block automated abuse at scale - Vercel](https://vercel.com/blog/how-nous-research-used-botid-to-block-automated-abuse-at-scale)
> 
> 翻译时间：2026-02-01 20:45
