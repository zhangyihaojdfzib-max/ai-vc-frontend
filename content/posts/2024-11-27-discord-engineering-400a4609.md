---
title: Discord如何用合成控制法衡量语音消息的产品影响
title_original: 'Measuring Product Impact Without A/B Testing: How Discord Used the
  Synthetic Control Method for Voice Messages'
date: '2024-11-27'
source: Discord Engineering
source_url: https://discord.com/blog/measuring-product-impact-without-a-b-testing-how-discord-used-the-synthetic-control-method-for-voice-messages
author: ''
summary: 本文介绍了Discord团队在无法进行传统A/B测试的情况下，如何利用合成控制法衡量语音消息功能因果效应的实践。由于Discord存在强烈的网络效应，用户级A/B测试会因组间相互影响而产生偏差，而按地域分组测试又会混淆其他差异。文章探讨了这些传统方法的局限性，并引出合成控制法作为一种在无法随机分组时仍能进行因果推断的替代方案，为衡量受网络效应影响的产品功能提供了新思路。
categories:
- AI产品
tags:
- 因果推断
- A/B测试
- 合成控制法
- 产品分析
- 网络效应
draft: false
translated_at: '2026-01-23T04:46:03.357194'
---

## 求助！！我们很兴奋想在Discord上测试语音消息功能，但无法进行传统的A/B测试…现在该怎么办？

请跟随我们一同踏上因果推断的探索之旅…

2023年，Discord新增了一项功能：用户可通过移动应用在文字频道、私信和群组私信中发送语音消息。团队对该功能充满期待，并好奇用户将作何反应。人们当然喜欢聆听彼此悦耳的声音，对吧？但如何衡量其因果效应呢？

![一张表情包：一个人对两条信息表现出不同情绪。看到"很兴奋想在Discord上测试语音消息"时很开心，但看到后续消息"我们无法进行传统的A/B测试"时很沮丧](/images/posts/efdd0516de7b.png)


这正是我们面临困境之处。Discord充斥着（我们强调：充斥着！）网络效应。我们通常使用A/B测试来衡量工作成果，但许多测试都会受到网络效应的影响——甚至有些功能脱离网络环境就毫无意义。当A组用户的行为影响B组用户的行为（反之亦然）时，就会产生网络效应。这可能通过引入跨组互动、违反控制组与实验组独立单位假设（SUTVA ♥️）而导致结果偏差。像语音消息这样的功能尤其容易受到网络效应影响。毕竟，这个功能只有在有人发送语音消息且有人接收时才有意义，对吧？

理想方案是按网络集群进行随机分组。但这颇具挑战性，因为遗憾的是Discord的测试平台（目前！）尚不支持集群随机化。

因此我们有几个选择：进行（效果不佳的）用户级A/B测试，或按国家进行随机分组。其思路是大多数网络集群往往以国家或语言为界，因此我们可以通过比较实验地区与控制地区来缓解网络效应。但地域测试也存在明显缺陷，因为将实验国家与控制国家进行比较时，会将所有其他差异与处理效应混为一谈。那么…有没有更好的选择呢？


> 本文由AI自动翻译，原文链接：[Measuring Product Impact Without A/B Testing: How Discord Used the Synthetic Control Method for Voice Messages](https://discord.com/blog/measuring-product-impact-without-a-b-testing-how-discord-used-the-synthetic-control-method-for-voice-messages)
> 
> 翻译时间：2026-01-23 04:46
