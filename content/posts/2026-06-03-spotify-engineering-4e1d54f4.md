---
title: Spotify：AI编码工具让开发者效率飙升
title_original: 'Coding Is No Longer the Constraint: Scaling Developer Experience
  to Teams and Agents at Spotify | Spotify Engineering'
date: '2026-06-03'
source: Spotify Engineering
source_url: https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint/
author: ''
summary: Spotify首席架构师分享其AI转型经验：AI编码工具采用率超99%，PR频率增长76%。通过自研后台编码Agent“Honk”和Fleet Management系统，将过去需数百团队数周的迁移工作缩短至一名工程师几天完成。文章强调，在AI
  Agent时代，强大的内部开发平台和工程实践是基础。
categories:
- AI基础设施
tags:
- AI编码
- 开发者体验
- Spotify
- Agent
- 工程效率
draft: false
translated_at: '2026-06-04T06:38:38.990629'
---

# 编码不再是瓶颈：在Spotify将开发者体验扩展到团队和Agent（智能体）

当编码不再是瓶颈时会发生什么？在Spotify，我们开始找到答案。

Spotify首席架构师兼工程副总裁Niklas Gustavsson最近分享了我们多年来在内部开发平台和工程最佳实践方面的投入如何推动我们的AI转型——使我们的团队和Agent（智能体）能够比以往更快地行动，同时也为应对未来的新挑战奠定了基础。请观看他在Code with Claude 2026上的完整演讲。

继续阅读以了解关键亮点。

## 采用率"完全疯狂"

Spotify对AI编码工具的采用率前所未有——随着去年年底Opus 4.5的发布，这一速度急剧加快。如今，超过99%的工程师每周使用AI编码工具，94%的人表示AI提高了他们的生产力，我们的拉取请求频率增长了76%，绝大多数PR由开发者与AI Agent（智能体）协作完成。

![AI工具采用率在假期期间整体下降，但橙色峰值显示Claude Code的采用率随Opus 4.5飙升](/images/posts/11e73237f5d8.png)

AI工具采用率在假期期间整体下降，但橙色峰值显示Claude Code的采用率随Opus 4.5飙升

###### "我们一直在内部推出工具来提高开发者的生产力，但从未见过像推出AI编码工具这样的采用率。"

## 我们在Agent（智能体）出现之前就开始了这段旅程

几年前，我们注意到生产代码库的增长速度是工程师数量的七倍。开发者花费越来越多的时间在维护上——升级依赖、迁移API、修补漏洞——而花在构建功能上的时间越来越少。迁移是开发者最大的挫败感来源。

我们没有要求数百个团队逐个手动更新他们的组件，而是设想了一种不同的方法。如果我们使用自动化一次性对数百甚至数千个软件组件进行更改会怎样？这个想法变成了Fleet Management，而我们为此构建的底层系统叫做Fleetshift。Fleet Management已在Spotify运行了数年。迄今为止，我们已经合并了超过250万个自动化维护PR，其中绝大多数是自动合并的，无需人工干预。

![图表显示了Spotify自动化PR的整体增长——绿色部分代表自动合并的PR](/images/posts/ef9a1080ca06.png)

图表显示了Spotify自动化PR的整体增长——绿色部分代表自动合并的PR

###### "与其逐个组件相当手动地操作，我们能否设想一种方式，将其作为改变整个组件集群的方法？"

## 认识Honk，我们的后台编码Agent（智能体）

Fleet Management对于简单更改效果很好，但复杂的代码修改——替换API调用、重构使用模式——让我们的确定性脚本达到了极限。当你在数百万行代码和数千个组件上运行脚本时，你会遇到每一个边缘情况。

随着LLM的成熟，我们看到了一个机会。如果我们不再编写越来越复杂的确定性脚本，而是使用模型来处理代码修改会怎样？

![在Code with Claude上认识Honk](/images/posts/e0a6fe54f787.png)

###### "它有一个傻傻的名字和傻傻的图标，但事实证明它是一个非常有用的工具。"

经过多次迭代，结果就是Honk，我们的后台编码Agent（智能体）。它可能有一个傻傻的名字，但我们这位羽翼丰满的编码伙伴已成为我们日常运营中不可或缺的一部分。在底层，Honk使用Agent SDK运行Claude，封装在我们自己的框架中并部署在Kubernetes Pod中，这样我们就可以在云环境中同时调度多个会话。它可以访问一组可信工具，包括在我们的CI环境中跨多个操作系统运行构建以验证其更改是否正确的能力。

![将Honk添加到Fleet Management](/images/posts/90977cfd5f6e.png)

Honk直接集成到我们的Fleet Management工具中：Fleetshift帮助人类管理编排——识别目标、调度更改、跟踪进度——而Honk位于中间进行实际的代码修改。运行迁移的团队可以一目了然地看到已创建了多少PR、已合并了多少以及哪些需要关注。我们最近一次跨后端服务的Java迁移耗时三天。

![Fleetshift插件](/images/posts/119a988f1c81.png)

###### "过去需要数百个团队为他们的组件进行迁移，耗时数周甚至数月，现在可以由一名工程师在几天内完成。"

开发者就是开发者，他们很快找到了利用我们出奇强大、自给自足的后台编码Agent（智能体）的新方法。Honk现在可以通过Slack使用，工程师可以在对话中提及它——这是自然的上下文来源——它会飞出去处理问题，然后带着PR回来。

![鹅场的又一个普通日子：我们的内部实时仪表盘显示Spotify Fleet Management系统中的当前活动。每只鹅代表一个由Honk驱动的活跃后台编码会话。](/images/posts/4d86894cf40a.gif)

鹅场的又一个普通日子：我们的内部实时仪表盘显示Spotify Fleet Management系统中的当前活动。每只鹅代表一个由Honk驱动的活跃后台编码会话。

而随着Honk v2的推出，我们引入了多人协作：共享Agent（智能体）会话、团队项目以及通过Chirp进行的Agent（智能体）编排。我们期待一个Agent（智能体）与多个开发者和团队协作的世界，而不仅仅是与终端前的一个人协作。

## 开发者体验也适用于Agent（智能体）

Spotify最古老的工程原则之一是："我们领先世界的技术越少，前进速度就越快。"

这个理念在Spotify比AI早了很多年。通过标准化一组聚焦的技术，我们建立了更深的专业知识，消除了团队不必要的决策，并使工程师更容易在代码库中协作。Spotify的典型后端服务看起来与其他每个后端服务非常相似——相同的技术栈，大致相同的设计模式。

事实证明，这一原则对Agent（智能体）同样重要。当Claude有大量其他代码可以参考，并且这些代码保持一致时，它的表现显著更好。我们清楚地看到了这一点：在我们更碎片化的代码库中，Agent（智能体）的性能明显更差。

###### "如果Claude有大量其他代码可以查看，并且这些代码大致保持一致，Claude会做得更好。这就是我们看到的。"

这种一致性的起点是Backstage，我们的开源内部开发者门户（IDP）。在Backstage之前，Spotify有大约一百种不同的内部工具——一个用于部署，另一个用于CI，另一个用于A/B测试。它碎片化且令人困惑。Backstage将所有内容整合到一个围绕软件组件目录构建的统一视图中。如今，对于开发者需要对其组件执行的任何操作，他们都在Backstage中完成。

![团队和Agent（智能体）都可以在Backstage软件目录中找到关于任何组件的所有信息](/images/posts/3164f953f350.png)

团队和Agent（智能体）都可以在Backstage软件目录中找到关于任何组件的所有信息

事实证明，这对Agent（智能体）同样有用。我们将Backstage的功能以MCP和命令行工具的形式暴露出来，这样Claude就可以查找谁拥有某个组件、阅读其文档，或在Slack上联系负责的团队。

我们还通过名为 **Soundcheck** 和 **Golden State** 的工具，借助 Backstage 推动标准化。Golden State 为每种组件类型定义了推荐的技术与实践。Soundcheck 则提供了一个界面，团队可以在此对照这些标准对自身组件进行自评。结合静态分析与代码检查，这些标准成为了主动的护栏——当 Claude 在我们的代码库中工作，并使用我们已知对基础设施并非最优的模式时，它会立即从代码检查系统获得反馈并进行自我修正。

![Golden State 作为一段旅程](/images/posts/82fad5997bcb.png)

###### “当 Claude 在我们的代码库中工作时，它会立即获得关于是否使用了正确的技术集和设计模式的反馈。”

这种反馈循环对开发者和 Agent（智能体）同样有效，也是我们发现的、在大规模推动一致性的最有效方法之一。

## 编码不再是瓶颈

随着编码速度的提升，约束条件转向了人类决策。Spotify 一直有比构建能力更多的想法——但现在，任何人都可以在我们的客户端单体仓库中打开 Claude，在几分钟内（而非数天）构建一个功能原型。就连我们的 CEO 也在用这种方式构建原型。

###### “这让原型构建从可能需要数天或数周，变成了现在只需几分钟。”

另一方面：我们现在需要审查的 PR 增加了 76%。我们正在学习如何运用人类判断——自动合并安全的内容，将审查聚焦于最关键之处——并重新思考我们的规划与优先级排序方式，因为瓶颈已从编码转向决策。

我们多年前在 Fleet Management、Backstage 和工程标准化方面的投入，让我们占据了有利位置。我们对未来充满期待。

**Fleetshift** 和 **Honk** 作为 Spotify Portal for Backstage 的一部分提供。如果大规模编排复杂代码变更与您的组织相关，请联系我们的平台团队，获取个性化演示。

---

> 本文由AI自动翻译，原文链接：[Coding Is No Longer the Constraint: Scaling Developer Experience to Teams and Agents at Spotify | Spotify Engineering](https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint/)
> 
> 翻译时间：2026-06-04 06:38
