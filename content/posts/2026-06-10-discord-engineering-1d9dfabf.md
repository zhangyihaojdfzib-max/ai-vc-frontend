---
title: Discord收紧应用访问服务器数据权限
title_original: Updated Requirements to How Apps Access Data in Servers
date: '2026-06-10'
source: Discord Engineering
source_url: https://discord.com/blog/updated-requirements-to-how-apps-access-data-in-servers
author: ''
summary: Discord宣布调整应用访问服务器数据的方式，包括成员信息、在线状态和消息内容。新规要求开发者通过年度审查和更严格的访问门槛才能获取这些数据。未完成审查的应用可能功能受限，例如从文本命令转为斜杠命令。开发者有90天过渡期进行调整或重新申请。此举旨在加强数据保护，但大多数应用运行不受影响。
categories:
- 政策监管
tags:
- Discord
- 数据访问
- 开发者政策
- 隐私保护
- 应用权限
draft: false
translated_at: '2026-06-12T06:37:58.908893'
---

即日起，我们将对应用开发者做出调整，这些调整将影响其 Discord 应用访问所添加服务器信息的方式，包括服务器成员信息、用户在线状态及消息内容。尽管大多数 Discord 应用和机器人并不使用这些信息，但我们仍将为此类数据增加更强有力的保护措施，例如年度审查和更严格的访问门槛。请继续阅读，以详细了解变更内容及其原因。

这些调整主要针对应用开发者（如果您是开发者，请前往我们的开发者帮助中心查看详细指南）。对于在 Discord 上使用应用的用户而言，简而言之：大多数应用将继续像现在一样运行，但对其可访问的数据将设置更多防护措施。此前拥有访问权限但未完成新审查流程或未获授权的应用，其功能可能会受到影响。例如，此前依赖文本命令（即机器人对消息中特定词语或短语作出反应）的应用，可能会被重新设计为使用斜杠命令（用户通过输入 /command 激活机器人）来运行。为尽量减少影响，开发者将收到通知，并获得 90 天时间保留访问权限，在此期间他们可进行必要调整或通过审查流程申请继续访问。此外，开发者可随时重新提交申请。

今天的调整仅影响开发者申请访问特定用户数据的方式和时机，而非可访问的数据本身。请继续阅读以了解变更的完整详情。

---

> 本文由AI自动翻译，原文链接：[Updated Requirements to How Apps Access Data in Servers](https://discord.com/blog/updated-requirements-to-how-apps-access-data-in-servers)
> 
> 翻译时间：2026-06-12 06:37
