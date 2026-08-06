---
title: WriteGuard：为MCP服务器提供精细化写入控制
title_original: 'WriteGuard: Fine-grained controls for MCP Servers'
date: '2026-08-05'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/mcp-portal-writeguard-private-beta/
author: ''
summary: Cloudflare构建了WriteGuard，一个用于MCP服务器的策略、归因和审计层，以应对AI Agent执行写入操作带来的风险。通过集中管理工具风险等级、启用状态和标签配置，WriteGuard允许在不修改底层服务器的情况下控制Agent行为，支持只读、最小影响、受限写入和关键操作等分级管控。它还能为支持的写入操作添加Agent归因并生成脱敏审计事件，便于调查。该功能已通过私有测试版引入Cloudflare
  MCP服务器门户，旨在平衡AI能力扩展与安全治理。
categories:
- AI基础设施
tags:
- MCP
- AI安全
- Cloudflare
- Agent治理
- 写入控制
draft: false
translated_at: '2026-08-06T05:11:05.108235'
---

让我们想象一下“无尽关闭工单”的场景。

工单从中午开始被关闭。起初没人太在意。Joe把几个工单移到了“已完成”状态，而Joe正度过一个高效的下午。随后速度加快了。到下午4点，成千上万的工单已被关闭，全部出自Joe之手。

Joe是一名优秀的工程师。但Joe不是那种一小时能关上千工单的工程师。

我们得知，他在三个并发会话中运行着多个后台Agent。花了半个小时才找到问题所在：一个清理任务，其提示词范围稍微宽泛了一些。

一旦我们停止了该Agent，就需要修复工单系统的状态。Joe当天下午也确实在手动关闭工单。系统将所有变更都记录在Joe名下，无论操作者是他本人还是他的Agent，而网络日志也无法区分不同的Agent会话。从外部看，这些操作看起来完全一样。

上面的例子风险相对较低，但我们都能想象到，或读到过，更具破坏性的案例。一个有权访问合同软件的Agent可能修改协议。一个在支持队列中造成混乱的Agent可能向客户发送数百条回复。一个拥有数据库访问权限的Agent可能删除整个数据表。

在Cloudflare，我们知道不能指望每位员工都能完美配置每个Agent或监控每一次工具调用。因此，在扩展我们内部MCP服务器的写入权限之前，我们构建了WriteGuard。现在，我们通过私有测试版将这些控制功能引入Cloudflare MCP服务器门户。

## MCP基础

在解释WriteGuard之前，让我们回顾一下什么是MCP服务器，以及它如何与AI Agent协同工作。

MCP代表模型上下文协议（Model Context Protocol），是一种将AI应用连接到外部工具和数据源的流行标准。MCP服务器提供已连接客户端可以使用的工具。每个工具都有名称、描述、输入模式和执行工作的处理程序。

当Agent选择工具时，MCP客户端将工具调用发送到服务器，服务器随后与下游应用程序进行交互。

## Cloudflare的MCP

MCP是支撑Cloudflare内部Agent的关键基础设施组件。这些Agent通过OpenCode和Cloudflare OS等本地客户端，以及长期运行的Agent服务来使用MCP。我们在Cloudflare Access后面运行服务器，并通过一个内部MCP服务器门户连接它们。

当我们在四月份描述我们的内部AI工程栈时，我们的门户连接了13个MCP服务器。如今，它连接了27个，而且各团队每月都在增加更多服务器。它们最初都是只读服务器，允许团队搜索Jira、GitLab、我们的wiki和运维系统，而不会修改它们。

只读是一个很好的起点。随着模型改进和团队积累AI经验，工程、产品、设计、销售和客户成功部门的人员开始要求能够执行操作的工具。

为了避免我们自己出现“无尽关闭工单”的情况，我们希望集中控制Agent可以执行的写入操作，在下游应用程序中显示Agent标签，并建立便于调查Agent活动的审计追踪。我们不能依赖客户端控制，如技能或提示词。它们的行为因框架而异，用户也可以禁用它们。

因此，我们构建了WriteGuard。

## 介绍WriteGuard

WriteGuard是一个共享的策略、归因和审计层。

它利用每个工具的配置和请求上下文来决定如何处理。WriteGuard可以原样传递调用，为支持的写入操作添加Agent归因并生成脱敏审计事件，或者在其处理程序运行之前阻止某个操作。

下图展示了WriteGuard在我们当前内部MCP架构中的位置。

![unnamed.png](/images/posts/64b6684a0d43.jpg)

WriteGuard将工具策略与人类和Agent身份、下游归因以及集中审计相结合。它为我们提供了一个控制Agent操作并保留理解这些操作所需上下文的统一位置。

## 从可调用工具到可治理操作

WriteGuard允许我们在每个工具旁边定义策略，而无需修改底层MCP服务器。每个工具都有风险等级、启用或禁用状态以及标签配置。风险等级决定操作是否被记录以及工具调用是否被允许，并且这些等级允许按风险查询审计日志。我们支持标签功能，以便插入Agent归因标签，并使用最适合下游应用程序的文本格式，而无需在MCP服务器本身中进行任何代码更改。

| 风险等级 | 示例 |
|---------|------|
| 只读 | 搜索问题；读取合并请求（MR）；查看流水线状态 get_merge_request |
| 最小影响 | 添加表情反应；将通知标记为已读；订阅问题 |
| 受限写入 | 添加评论；创建MR；更新问题字段 create_mr_note |
| 关键 | 合并MR；触发生产部署；批量删除记录 merge_mr |

```
const sendEmailTool = {
  tool: EmailMCP.sendEmailTool,
  writeGuard: {
    riskLevel: RiskLevel.CONTAINED_WRITE,
    enabled: true,
    labeling: {
      field: "body",
      supportedFormats: [
        LabelFormat.PLAIN_TEXT,
        LabelFormat.HTML,
      ],
    },
  },
};
```

目前，我们在内部MCP monorepo中以TypeScript定义此配置。随着私有测试版在未来几个月内推出，服务器所有者将能够通过Cloudflare MCP服务器门户配置相同的策略。每个MCP服务器都将有一个基线Access策略，以及针对单个工具的WriteGuard控制。

## 保留人员身份，添加Agent标识

我们的内部MCP服务器使用Cloudflare Access和OAuth来识别用户。因此，使用这些服务器的Agent以该员工的权限运行。如果Joe不能关闭某个特定问题，Joe的Agent也不能关闭它。

我们保留了这种模式，而不是引入独立的Agent账户。Agent账户会创建第二套需要管理的权限，并使与Agent负责人的关联变得不那么清晰。然而，这一决定的权衡是，下游应用程序看到的是Joe的凭据，但看不到操作背后标识Agent的任何信息。

WriteGuard将MCP客户端和会话上下文添加到人类身份中，将每次写入标识为代表特定人员行事的Agent会话。值得注意的是，即使一切正常，这种归因也极其有用。它帮助人类和其他Agent理解变更并决定如何响应。

## 让机器速度的活动可查询

可见标签解释了单个操作，并在下游应用程序中提供了有用的上下文，但它们无法提供全局视图。由于Agent重复操作的速度远快于人类，我们还需要跨所有MCP服务器的集中审计。

WriteGuard将每次调用分类为成功、失败或阻止，然后异步将脱敏事件发送到内部审计Worker。该事件省略被视为机密或敏感的键值。它包含服务器、工具、风险等级、结果、用户、客户端和持续时间。

这使得Agent活动可以在我们所有启用MCP的系统中进行查询。

![我们的内部WriteGuard仪表板，包含示例数据。](/images/posts/74a732492ba4.jpg)

该仪表板补充了MCP服务器门户提供的请求日志。门户日志显示工具调用，而WriteGuard增加了语义工具分类、Agent上下文以及来自后端服务器的结果。

我们将审计日志设为异步，因此不会为Agent等待的响应增加延迟。

## WriteGuard实战：GitLab

在本文前面，我们提到了来自GitLab MCP服务器的三个工具：get_merge_request、create_mr_note和merge_mr。让我们逐一跟踪它们经过WriteGuard的过程。

### 读取合并请求

假设一位工程师要求一个Agent总结一个提议的代码变更，该Agent调用了`get_merge_request`工具。WriteGuard将该工具分类为READ_ONLY，并允许该调用原样通过。

### 向合并请求添加评论

现在，工程师要求Agent在合并请求（MR）上留下评论，Agent调用了`create_mr_note`工具。

该工具被分类为CONTAINED_WRITE。WriteGuard使用GitLab支持的格式，将Agent归属信息添加到配置的备注字段中，然后调用工具处理器。它还会异步记录一条经过脱敏处理的审计事件，其中包含用户、工具、结果和Agent身份上下文。

![来自GitLab create_mr_note工具的截图示例。](/images/posts/3f61517852f4.jpg)

![来自GitLab create_mr_note工具的审计日志示例。](/images/posts/a8d84fc753c6.jpg)

### 合并代码

假设一位工程师要求一个Agent帮助审查一个合并请求。为了提供帮助，Agent超出了请求范围，未经要求就调用了`merge_mr`工具。

由于Cloudflare的合并操作通常会触发部署流水线，我们要求必须有人员参与其中。因此，我们将`merge_mr`工具分类为CRITICAL风险级别，并在WriteGuard中配置为禁用该工具。

如果被调用，WriteGuard会在其处理器运行之前阻止该请求，并记录此次尝试。

![WriteGuard审计仪表板中被阻止的merge_mr调用。](/images/posts/cd35892141cd.jpg)

## 超越单服务器示例

这些工具使用相同的服务器、身份流程和下游API，但WriteGuard在其代码运行之前对每个工具的处理方式都不同。

仅针对GitLab，我们本可以将这些控制直接构建到服务器中。但我们还需要为Jira、我们的内部维基、Google Workspace以及我们添加的每个新MCP服务器提供相同的功能。在每个服务器中重新实现这些功能将需要更多工作，并产生不一致的行为。

因此，我们将WriteGuard构建为一个共享层，它只需要针对每个工具进行配置，即可通过门户连接的所有MCP服务器上工作。

## 从内部推广到私有测试版

我们为Cloudflare自己的MCP服务器构建了WriteGuard，因为我们需要超越只读工具，同时不失去对后续写入操作的控制。私有测试版将该架构引入MCP服务器门户，提供了一种对写入工具进行分类、在执行前阻止工具、添加Agent归属信息以及检查跨连接服务器的写入活动的方法。

该测试版将从小范围开始，并随着时间的推移逐步扩展，最终实现全面可用。我们希望验证风险模型如何映射到客户工具、哪些下游应用需要归属格式，以及在广泛提供WriteGuard之前，客户需要什么样的审计交付保证。

如果您的组织正在向MCP服务器添加写入工具，并希望与我们一同测试这些控制措施，请注册WriteGuard私有测试版。

## 相关标签

在社交媒体上关注

- Cloudflare
- Scott Roe-Meschke
- Kenny Johnson

## 订阅以接收新帖通知

我们绝不会分享您的电子邮件地址。

感谢订阅！请检查您的收件箱以确认。

---

> 本文由AI自动翻译，原文链接：[WriteGuard: Fine-grained controls for MCP Servers](https://blog.cloudflare.com/mcp-portal-writeguard-private-beta/)
> 
> 翻译时间：2026-08-06 05:11
