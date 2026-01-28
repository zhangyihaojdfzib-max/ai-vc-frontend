---
title: Discord如何通过Zstandard字典压缩将WebSocket流量降低40%
title_original: How Discord Reduced Websocket Traffic by 40%
date: '2024-09-20'
source: Discord Engineering
source_url: https://discord.com/blog/how-discord-reduced-websocket-traffic-by-40-percent
author: ''
summary: Discord为提升移动端性能，探索减少客户端带宽使用。文章回顾了其网关连接自2017年起使用zlib压缩的历史，并重点介绍了近期采用Zstandard压缩算法的实践。Zstandard凭借更高的压缩比、更快的速度以及独特的字典功能，能针对Discord小而结构明确的网关负载进行优化。通过预交换压缩信息，字典显著提升了压缩效率，最终成功将WebSocket流量降低了40%，改善了用户体验。
categories:
- 技术趋势
tags:
- 性能优化
- 数据压缩
- WebSocket
- 移动端开发
- Discord
draft: false
translated_at: '2026-01-28T04:46:04.668432'
---

在Discord，我们始终在思考如何改进服务并提升性能。毕竟，我们的应用运行得越快，您就能越早回到朋友和对话中！

过去六个月里，我们开启了一项支持这一目标的探索，致力于减少客户端（尤其是在iOS和Android平台上）的带宽使用量，希望降低带宽使用能带来更灵敏的体验。

## 背景

当您的客户端连接到Discord时，它会通过我们称为“网关”的服务接收实时更新。自2017年底以来，客户端的网关连接一直使用zlib进行压缩，这使得消息大小缩小了2到10倍。

自那时起，**zstandard**（最初于2015年发布）已获得足够关注，成为zlib的可行替代方案。Zstandard提供更高的压缩比和更短的压缩时间，并支持**字典**：一种预先交换压缩内容信息的方式，可进一步提高压缩比并降低整体带宽使用。

我们过去曾尝试使用zstandard，但当时其收益不足以抵消成本。我们在2019年的测试仅针对桌面端，且占用了过多内存。然而，五年间可能发生很多变化！我们想再次尝试，而字典支持尤其吸引我们，特别是因为我们的大多数网关负载较小且具有明确定义的结构。

我们相信这些负载的可预测性将是应用字典来进一步减少带宽使用的完美场景。

---

> 本文由AI自动翻译，原文链接：[How Discord Reduced Websocket Traffic by 40%](https://discord.com/blog/how-discord-reduced-websocket-traffic-by-40-percent)
> 
> 翻译时间：2026-01-28 04:46
