---
title: Discord所有语音视频通话全面实现端到端加密
title_original: Every Voice and Video Call on Discord Is Now End-to-End Encrypted
date: '2026-05-18'
source: Discord Engineering
source_url: https://discord.com/blog/every-voice-and-video-call-on-discord-is-now-end-to-end-encrypted
author: ''
summary: Discord宣布已完成所有语音和视频通话（舞台频道除外）的端到端加密（E2EE）迁移，该加密默认启用，无需用户手动开启。文章回顾了从2023年试验DAVE协议到2026年完成全平台部署的历程，强调在保持用户体验的同时实现了大规模加密，体现了团队对用户隐私的长期承诺。
categories:
- 技术趋势
tags:
- Discord
- 端到端加密
- DAVE协议
- 隐私保护
- 实时通信
draft: false
translated_at: '2026-05-19T06:15:17.708400'
---

2023年8月，我们曾分享过正在Discord上为语音和视频通话试验端到端加密（E2EE）。那篇博文简短且刻意低调，但它代表着一份真正的承诺——我们深知这需要数年时间才能实现。

自那以后，我们走过了相当漫长的历程。2024年9月，Stephen Birardain推出了DAVE协议：一套经过审计的开放端到端音频与视频加密协议。我们开始在桌面端和移动端迁移通话，并着手证明E2EE能在Discord的规模下运行，同时不损害用户对我们所期望的体验。2025年，Clément Brisset将DAVE扩展至所有剩余平台，包括网页浏览器、游戏主机、对Discord机器人/应用的支持，以及我们的Social SDK，从而填补了此前部分通话未能完全加密的缺口。2026年3月初，我们完成了这一迁移。

如今，端到端加密已成为Discord上所有语音和视频通话（舞台频道除外）的标配，无需用户主动选择开启。

我为团队所取得的成就感到自豪，并想谈谈这背后的付出及其重要意义。

---

> 本文由AI自动翻译，原文链接：[Every Voice and Video Call on Discord Is Now End-to-End Encrypted](https://discord.com/blog/every-voice-and-video-call-on-discord-is-now-end-to-end-encrypted)
> 
> 翻译时间：2026-05-19 06:15
