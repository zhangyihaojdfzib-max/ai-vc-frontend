---
title: Discord推出社交SDK，助力游戏集成好友列表与语音聊天功能
title_original: "Announcing Discordâ\x80\x99s Social SDK, Helping Power Your Gameâ\x80\
  \x99s Social Experiences"
date: '2025-03-17'
source: Discord Engineering
source_url: https://discord.com/blog/announcing-discord-social-sdk-to-power-game-comms
author: ''
summary: Discord于2025年3月正式推出免费社交SDK，允许游戏开发者将Discord的社交基础设施集成到游戏中，为所有玩家（无论是否拥有Discord账户）提供统一好友列表、跨平台消息、语音聊天及深度链接游戏邀请等功能。该工具旨在通过无缝的社交体验提升玩家参与度与留存率，并借助Discord月活超2亿的庞大社区促进游戏发现。SDK已支持C++、Unreal
  Engine和Unity，早期合作伙伴包括Theorycraft Games、Facepunch Studios等。
categories:
- 技术趋势
tags:
- Discord
- 游戏开发
- 社交SDK
- 玩家社区
- 跨平台通信
draft: false
translated_at: '2026-01-17T04:21:00.983985'
---

- 开发者可为所有玩家（无论是否拥有Discord账户）提供好友列表、跨平台消息、语音聊天等功能支持
- 通过无缝的游戏中社交功能，帮助开发者提升用户参与度与留存率；借助Discord月活超2亿的生态系统扩展触达范围，促进游戏发现
- 早期合作伙伴包括Theorycraft Games、Facepunch Studios、Scopely；SDK现已面向全体开发者开放

**旧金山，2025年3月17日**——Discord今日正式推出Discord社交SDK。该工具包使各类规模的开发者都能免费利用Discord的社交基础设施，为所有玩家（无论是否拥有Discord账户）提供游戏的社交与多人体验支持。开发者不仅能借助该SDK为全体玩家提供游戏内通信与连接功能，还能为关联Discord账户的玩家带来更深度整合的沉浸式体验，同时进一步受益于Discord的社交功能以推动游戏发现与增长。

通过早期合作伙伴的游戏实践，Discord社交SDK已实现玩家连接的简化和参与度的提升，同时使游戏能突破自身边界，触达Discord月活超2亿的高活跃度社区——该社区用户每月仅在PC端数千款游戏中的总时长就超过15亿小时。社交集成功能包括：作为游戏内社交体验基础的统一好友列表、支持玩家邀请好友直接加入队伍或房间的深度链接游戏邀请，以及跨平台消息和语音聊天等通信功能。

目前已采用Discord社交SDK的早期开发者包括Theorycraft Games、Facepunch Studios、1047 Games、Scopely、Mainframe Industries、Elodie Games、腾讯游戏等。该SDK兼容C++语言，支持Unreal Engine与Unity引擎，适配Windows 11+及macOS系统，主机与移动端支持即将推出。

> "对于从独立开发者到3A大厂的所有游戏创作者而言，Discord是连接全球规模最大、参与度最高玩家社区的平台，能在游戏发布前、中、后期持续推动游戏增长。游戏发现与留存从未如此关键，我们很高兴能帮助开发者在玩家聚集地拓展游戏影响力。" ——Discord联合创始人兼首席技术官 Stanislav Vishnevskiy

> "我们在Discord上投入巨大——从组织全远程办公到培育游戏测试社区——因为我们坚信这是一个独一无二的平台。Discord社交SDK是宝贵工具，能让《SUPERVIVE》玩家无缝使用私信、房间和会话邀请等社交功能。我们很荣幸成为Discord社交SDK的早期合作伙伴，期待通过接入Discord庞大的社交图谱和创新社交工具来强化游戏内通信体验。" ——Theorycraft Games首席执行官 Joe Tung

> "在Scopely，强大的玩家社区是我们游戏的核心，也是我们一切工作的基础。《MARVEL Strike Force》玩家早已聚集在Discord上制定策略、强化联盟并相互联系。随着Discord社交连接功能即将直接集成至《MARVEL Strike Force》，我们期待为玩家打造更具吸引力、沉浸感和无缝的沟通方式，提升协同游戏体验并深化合作。" ——Scopely《MARVEL Strike Force》总经理 Ryan Jacobson

**推动游戏发现与生态增长**

当前游戏发现面临激烈竞争。仅五大头部系列游戏就占据总游戏时长的30%以上，前15名更是垄断60%的游戏时间[来源：Newzoo《2024年PC与主机游戏报告》]。每年有2万款新游戏上市，开发者在拥挤市场中难以获得曝光。然而，Discord活跃玩家中每月有50%会发现并尝试新游戏。

游戏的社交维度已成为发现的关键因素。随着玩家向Discord聚集——这个为游戏而生的数字客厅——他们渴望在真实友谊蓬勃发展的环境中建立活跃连接。研究显示：72%的Discord用户每周与朋友玩游戏，50%向朋友直播游戏过程，28%在观看朋友直播后一小时内启动同款游戏[来源：Discord 2024年内部数据]。当用户与至少一位朋友同玩时，游戏会话时长增长7倍，这印证了朋友间影响力与Discord独特生态系统的强大效应。

**连接游戏内外的玩家**

Discord社交SDK为开发者提供社交基础设施层，开放接入Discord天然社交社区，使高活跃度玩家能够连接、游戏并建立关系。通过游戏内直接集成的Discord功能，玩家能减少筹备时间、增加游戏时间——无论是组队同游、跨游戏协作，还是在赛后延续对话。

Discord社交SDK提供增强连接与玩家参与度的功能套件，包括：

- **统一好友列表**：
玩家可在游戏内查看Discord好友列表，在Discord中查看游戏好友列表，实现游戏内外无缝连接。

- **深度链接游戏邀请**：
玩家可直接通过游戏内统一好友列表向Discord好友发送邀请，使其精准加入队伍/房间/会话，提升玩家留存与参与度。

- **动态状态**：
玩家仅需进行游戏即可传播游戏信息。现已支持PC、主机和移动端的动态状态功能，让玩家在游戏时于Discord展示活动状态，并可配置为支持玩家资料页的一键加入游戏功能。这为游戏带来更多曝光与发现机会，同时增加多人游戏会话。

- **灵活的账户要求**：
玩家无需Discord账户即可享受游戏内统一社交体验，但也可选择关联账户，将游戏体验与Discord账户连接，获得更沉浸的体验，使游戏相关对话在非游戏时段得以延续。

此外，Discord正通过封闭测试版发布游戏内通信支持功能：

- **跨平台消息**：
玩家可在桌面端、主机和移动端持续进行游戏相关对话。

- **关联频道**：
玩家可将游戏内聊天关联至服务器中的特定Discord频道，为各类规模的公会、团队和小组提供跨游戏与Discord的持久消息空间。

- **语音聊天**：
玩家可享受当前最高质量的音频聊天，该功能采用Discord语音工具的底层技术，使其成为游戏通信的黄金标准。

开发者可通过封闭测试申请扩展使用这些功能。

**开始使用Discord社交SDK**

Discord社交SDK的发布基于公司更广泛的开发者支持计划，包括通过奖励驱动游戏发现的**Quest**功能，以及允许游戏开发者在Discord平台原生构建、发布、分发、获客和变现的**Activities**功能。

[点击此处](here)了解更多信息并开始使用Discord社交SDK。[此处](here)可下载图片与新闻资料包。

##### Discord 是一款通信平台，让您能通过语音、视频和文字功能，围绕游戏乐趣建立有意义的连接。作为专为多人在线游戏玩家打造的通信平台，Discord 拥有超过 2 亿月活跃用户的高度活跃社区，仅 PC 端每月在数千款游戏上的总游戏时长就超过 15 亿小时。Discord 总部位于旧金山，用户可在 Discord.com 免费下载，同时提供名为 Nitro 的订阅服务，提供增强的流媒体和自定义功能。


> 本文由AI自动翻译，原文链接：[Announcing Discordâs Social SDK, Helping Power Your Gameâs Social Experiences](https://discord.com/blog/announcing-discord-social-sdk-to-power-game-comms)
> 
> 翻译时间：2026-01-17 04:21
