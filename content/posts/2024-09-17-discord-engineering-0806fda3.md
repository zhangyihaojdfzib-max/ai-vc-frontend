---
title: Discord推出DAVE协议：为音视频通话提供端到端加密
title_original: 'Meet DAVE: Discord’s New End-to-End Encryption for Audio & Video'
date: '2024-09-17'
source: Discord Engineering
source_url: https://discord.com/blog/meet-dave-e2ee-for-audio-video
author: ''
summary: Discord正式推出名为DAVE的端到端加密协议，用于保护其平台上的私聊、群组私聊、语音频道及Go Live直播中的音频和视频通话。此举旨在为每月约2亿用户提供更安全、私密的通信体验。文章介绍了引入端到端加密的背景、设计目标，并提供了新协议工作原理的高层次技术概述，用户将能够确认通话加密状态并验证其他成员身份。
categories:
- 技术趋势
tags:
- 端到端加密
- Discord
- 隐私安全
- 实时通信
- DAVE协议
draft: false
translated_at: '2026-01-29T04:10:19.191421'
---

去年，我们宣布正在为Discord的语音和视频通话测试新的加密协议与技术。经过大量的实验、设计、开发和审计，我们很高兴地宣布Discord的音频视频端到端加密（简称"E2EE A/V"或"E2EE"），我们将其称为DAVE协议。

Discord致力于保护每月使用我们平台的约2亿用户的隐私和数据。随着我们持续成为帮助用户在游戏和共同兴趣中深化友谊的平台，我们非常激动能推出更安全、更私密的语音和视频通话。

今天，我们将开始将私聊、群组私聊、语音频道及Go Live直播中的语音视频迁移至端到端加密系统。您将能够确认通话何时启用端到端加密，并对通话中的其他成员进行身份验证。

我们希望解释为何将端到端加密音视频引入Discord，分享我们的设计与实施目标，并提供新协议工作原理的高层次技术概述。

---

> 本文由AI自动翻译，原文链接：[Meet DAVE: Discord’s New End-to-End Encryption for Audio & Video](https://discord.com/blog/meet-dave-e2ee-for-audio-video)
> 
> 翻译时间：2026-01-29 04:10
