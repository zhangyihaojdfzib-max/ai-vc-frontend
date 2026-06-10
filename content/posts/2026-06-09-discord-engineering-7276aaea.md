---
title: Discord语音迁移至边缘网络之路
title_original: How We Moved Discord Voice to the Edge
date: '2026-06-09'
source: Discord Engineering
source_url: https://discord.com/blog/how-we-moved-discord-voice-to-the-edge
author: ''
summary: 本文讲述了Discord如何将语音和视频流量从全球30个城市的数据中心迁移至覆盖300多个城市的Cloudflare边缘网络，以降低延迟和丢包率。迁移后，超过80%的流量运行在新网络上，法兰克福地区延迟降低34%、丢包率降低42%。文章还介绍了迁移动机、所需技术构建以及欧洲地区质量问题的调查过程。
categories:
- 技术趋势
tags:
- 边缘计算
- 语音通信
- 网络优化
- Cloudflare
- Discord
draft: false
translated_at: '2026-06-10T06:28:33.857449'
---

在Discord，用户与最近语音服务器之间的距离至关重要。网络距离每增加一毫秒，每个数据包的延迟就会增加，一旦超过某个临界点，通话就不再感觉像朋友就在你同一个房间里。

在Discord的大部分历史中，我们能将用户连接到的最远语音服务器位于全球约30个城市，这些城市是主要云服务提供商设有数据中心的地方。如果你住在湾区或法兰克福，这没问题；但如果你住在雷克雅未克、奥克兰或其他超大规模云服务覆盖薄弱的地区，体验就不那么理想了。

去年，我们开始将Discord的语音和视频流量迁移到Cloudflare的边缘网络，该网络覆盖超过300个城市。如今，超过80%的语音和视频流量运行在该网络上，70%的地区显示出同比质量改善。法兰克福表现最为突出，与前一家供应商相比，平均延迟降低了34%，丢包率降低了42%。

这篇文章讲述了我们如何走到这一步的故事：我们为什么这样做，为了实现这一目标我们必须构建什么，以及今年早些时候我们如何调查欧洲地区的质量问题。

---

> 本文由AI自动翻译，原文链接：[How We Moved Discord Voice to the Edge](https://discord.com/blog/how-we-moved-discord-voice-to-the-edge)
> 
> 翻译时间：2026-06-10 06:28
