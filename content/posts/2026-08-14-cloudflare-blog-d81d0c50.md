---
title: Cloudflare新功能：识别并保护MCP流量安全
title_original: How Cloudflare detects MCP traffic and helps secure it
date: '2026-08-14'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/mcp-security-updates/
author: ''
summary: Cloudflare推出新功能，用于识别经过检查的MCP流量，显示哪些用户和服务器正在产生该流量，并控制受管网络路径上的直接连接。文章分析了MCP工具调用的结构，比较了客户端、网络和服务器端三个控制位置，并展示了Cloudflare
  Gateway如何利用协议信号发现影子MCP流量，强制通过MCP Portal访问受信任的服务器，以应对AI Agent带来的安全挑战。
categories:
- AI基础设施
tags:
- MCP
- Cloudflare
- AI安全
- Agent
- 网络监控
draft: false
translated_at: '2026-08-15T03:05:09.365784'
---

大多数公司在设计资源权限时，都是以人类用户为出发点的。高级工程师或许能够部署到生产环境、查询敏感数据库或撤销其他用户的访问权限。这些特权伴随着风险，但传统上，这种风险受到两个假设的约束：工程师会运用人类判断力，且工程师只能以人类的速度行动。

看到意外结果的工程师通常会停下来重新考虑自己的操作。任何人一天内能点击、输入和审查的内容都是有限的。AI Agent（智能体）的引入改变了这两个阈值。它们的决策是非确定性的，并且可以无限次地执行相同操作（或调用相同工具），不会疲倦，也不会停下来吃午饭。一个看似合理但实际错误的决策，可能在人类察觉之前就演变成成千上万个错误操作。

今天，我们宣布推出新的Cloudflare One功能，用于识别经过检查的MCP流量，显示哪些用户和服务器正在产生该流量，并控制受管网络路径上的直接连接。结合MCP Server Portals，这些控制措施帮助管理员查看Agent（智能体）是否在使用经批准的路径，或者以某种方式绕过了它。

Model Context Protocol（MCP）服务器为Agent（智能体）提供了一种通用方式，用于发现和调用由第三方SaaS产品、内部应用程序和API支持的工具。底层权限可能很熟悉；发生变化的是由谁做出每个决策，以及一个错误决策能多快扩散。

将Agent（智能体）连接到这些工具之一可能只需一行配置。员工可以将Claude Code、Codex、Cursor、OpenCode、VS Code或任何AI框架指向MCP服务器，而无需检查其是否经过批准。由此产生的流量没有明显的特征。Model Context Protocol不使用固定的主机名，也不要求在路径中包含/mcp，因此直接连接看起来可能像任何其他HTTPS API调用。

为了解释这些控制措施如何协同工作，我们将从工具调用的结构及其暴露的信息开始。然后，我们将比较安全团队可以采取行动的三个位置：客户端内部、网络上以及MCP服务器端。接下来，我们将展示Cloudflare Gateway如何使用协议信号来发现影子MCP流量，并强制仅通过MCP Portal访问受信任的MCP服务器。

## MCP工具调用的结构

同一个MCP工具调用在系统中移动时会呈现三种形式。在客户端内部，它是使用一组参数调用工具的决定。在网络上，它是携带JSON-RPC消息的HTTP事务。在服务器端，它变成对工具处理程序的调用，该处理程序可能读取数据、更改状态或完成其他操作。

考虑一个想要了解奥斯汀天气的Agent（智能体）。远程MCP请求可能如下所示：

```
POST /mcp HTTP/1.1
Host: tools.example.com
Authorization: Bearer <access-token>
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: get_weather

{
  "jsonrpc": "2.0",
  "id": 42,
  "method": "tools/call",
  "params": {
    "name": "get_weather",
    "arguments": {
      "city": "Austin"
    }
  }
}
```

此请求中包含几个有用的信号。主机名和路径标识目的地。授权头携带用于在服务器要求时验证调用者身份的凭据。MCP-Protocol-Version头标识协议版本，而Mcp-Method和Mcp-Name在新的无状态协议中暴露操作和工具。JSON-RPC信封重复了方法，为请求提供了一个客户端可以与响应匹配的id，并在params中携带工具参数。

参数是最敏感的部分。它们可能包含搜索查询、源代码、客户数据或操作指令，例如创建工单或更改基础设施。工具名称说明Agent（智能体）打算调用什么；参数说明它将发送什么数据以及希望服务器执行什么操作。

如果调用成功，服务器将返回带有相同id和工具结果的JSON-RPC响应。该响应也可能包含敏感数据。请求检查可以在执行前阻止不安全操作，而响应检查和日志记录则显示工具返回给Agent（智能体）的内容。

## 控制MCP请求的三个位置

该请求为安全团队提供了三个可以观察或控制调用的位置。

### 在MCP客户端内部

客户端钩子可以在模型选择工具之后、客户端序列化请求之前运行。从这里，它可以查看目标服务器、工具名称和参数，而无需解密网络流量。

这是请求链中最早可以实施控制的阶段。客户端可以拒绝不在允许列表中的服务器，要求用户确认敏感操作，或在数据离开设备之前从参数中移除数据。它还可以覆盖本地stdio（即本地）MCP服务器，这些服务器从不产生网络流量。

这带来了标准化挑战。为了使安全团队从中受益，他们需要在员工使用的每个客户端上复制他们的控制措施。当组织同时管理客户端和设备时，客户端侧控制效果最佳，但来自单个客户端的遥测数据永远无法完整盘点MCP的使用情况。

### 在设备的网络边界

安全Web网关可以在HTTP请求离开客户端后对其进行观察。通过TLS解密，它可以将请求与用户和设备关联起来，检查目的地和协议头，并应用策略，而无需依赖特定的MCP客户端。

网络层拥有最广阔的视角来检测受管路径上的远程MCP流量。它可以识别到经批准的Portal之外服务器的直接连接，并在请求到达目的地之前阻止它们。在支持数据丢失防护扫描的地方，代理还可以检查JSON-RPC方法和参数中的敏感数据。然而，代理无法看到本地stdio调用或网络外的流量。

### 在MCP服务器调用工具之前

服务器拥有最丰富的执行上下文。它已对调用者进行了身份验证，解析了MCP消息，将get_weather解析为处理程序，并根据工具的输入模式验证了提供的参数。这是在工具运行之前可以拒绝请求的最后一点。

Agents SDK处理程序或类似的服务器中间件可以针对特定工具授权调用者、应用速率限制、检查参数并记录结果。服务器应在调用处理程序之前执行这些检查，尤其是对于写入数据或触发外部操作的工具。仅在执行后记录日志可以解释发生了什么，但无法阻止它。

Cloudflare的WriteGuard在我们内部的MCP服务器上使用了这种模式。每个工具都有风险等级和启用或禁用状态。WriteGuard可以原样放行读取操作，为允许的写入操作添加Agent（智能体）归属和审计事件，或者在其处理程序运行之前阻止关键操作。由于控制位于服务器端，最终用户无法通过切换客户端或禁用本地钩子来绕过它。

虽然服务器侧控制仅保护实现它们的服务器，但客户端和服务器具有最佳的请求深度。网络可以看到最广泛的远程连接集合。这些控制措施结合使用，可以在敏感数据离开设备之前阻止它，发现未受管的MCP流量，并在工具执行之前拒绝未经授权的操作。

网络控制点具有最广泛的覆盖范围，但它首先必须将MCP与普通HTTPS流量区分开来，用户必须运行代理，并且MCP服务器（或Portal）必须验证连接中使用了该代理。

Cloudflare One 提供了该链条中的网络组件。Cloudflare One Client 通过 Gateway 发送来自受管理设备的流量。Gateway 可以在协议层对 MCP 请求进行分类，并区分流量是来自 MCP Portal，还是超出了已批准的控制范围。管理员随后可以报告或阻止不符合批准路径的连接。该过程始于可靠地识别请求。

## URL 无法告诉你请求是否使用 MCP

我们最初查找 MCP 流量的方法，是使用 GraphQL Analytics API 在 Gateway HTTP 日志中搜索包含 `mcp` 的主机名以及 `/mcp` 或 `/sse` 等常见路径。我们的 MCP 流量检测教程包含了该查询，还解释了如何为请求体中的 `initialize`、`tools/call` 和 `resources/read` 等 MCP JSON-RPC 方法创建数据丢失防护模式。

这些信号对于发现旧客户端流量和提供历史可见性仍然有用，但它们非常基础。它们会漏掉位于普通 URL（如 `https://tools.example.com/api`）上的 MCP 服务器，这种情况并不少见。

而且它们可能匹配到恰好在其主机名或路径中使用 `mcp` 的无关服务（可能性不大，但我们确实见过）。对于符合规范的 Streamable HTTP 客户端，协议头是更具体的信号。MCP 2025-11-25 规范要求客户端在初始化后的每个 HTTP 请求中都必须包含 `MCP-Protocol-Version`。MCP 2026-07-28 规范更进一步，要求每个 POST 请求都必须包含该头。

但这并不意味着该头是完美的检测器。旧客户端的初始请求可能不包含它，早于 2025-06-18 的协议版本未定义该头，而本地 stdio、自定义传输或不合规的流量可能永远不会携带它。它的存在是 MCP 的强正向指标；它的缺失并不能证明请求不是 MCP。

## 该协议在网络层面越来越容易被识别

传统 MCP 流程以 `initialize` 请求开始，该请求不包含 `MCP-Protocol-Version` HTTP 头，因此网络控制可能无法仅凭该头对发往未知端点的第一个请求进行分类。该信号在客户端和服务器完成初始化后才会出现。

后续的工具调用如下所示：

```
POST /api HTTP/1.1
Host: tools.example.com
Content-Type: application/json
MCP-Protocol-Version: 2025-11-25

{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_weather"}}
```

MCP 2026-07-28 规范显著改变了这一模型。核心协议是无状态的；它完全移除了 `initialize` 握手，并在每个请求上携带协议版本和操作：

```
POST /mcp HTTP/1.1
Host: tools.example.com
Content-Type: application/json
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: get_weather

{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_weather"}}
```

`Mcp-Method` 和 `Mcp-Name` 头让普通 HTTP 基础设施无需解析请求体即可识别操作。负载均衡器可以路由请求，速率限制器可以区分 `tools/list` 和 `tools/call`，安全产品可以在每个请求上获得更多信息。

这些协议信号为 Cloudflare Gateway 提供了具体的评估依据，而无需依赖 MCP 样式的 URL 列表。

## Shadow MCP 和绕过批准路径是两个不同的问题

一旦 Gateway 能够识别 MCP 流量，你就可以评估给定连接对你的安全态势意味着什么。

Shadow MCP 是指连接到组织未批准的服务器。员工在代码仓库、产品指南或同事的消息中找到该服务器，并将其直接添加到他们的 MCP 客户端中。安全团队不知道该服务器暴露了哪些工具，也不知道员工向其发送了哪些数据。

Portal 绕过则不同：它始于组织已批准并放置在 MCP Portal 中的服务器，但员工直接连接到其上游 URL，跳过了 Portal 的 Access 策略、精选工具目录、数据丢失防护和工具级审计跟踪。

Gateway 是受管理网络路径上 Shadow MCP 的主要控制点；它可以识别经过 TLS 检查的 MCP 流量，显示目的地和用户，并应用策略。Portal 绕过需要该网络控制，外加一个能够拒绝直接请求的源站，无论是通过 Access 策略、源 IP 限制，还是由 MCP 服务器本身发起的企业授权机制。

## 在 Gateway 中检测 MCP 流量

对于已经采用带 TLS 检查的 Cloudflare Gateway 的客户，我们正在添加一个检测启发式规则，为每个被检查的请求回答一个简单的问题：这是 MCP 流量吗？

对于基于会话的 Streamable HTTP 连接，MCP 客户端在初始化后发送 `MCP-Protocol-Version` 头。Gateway 检查每个经过 TLS 检查的请求上的该头，并使用基于我们每天在 Cloudflare 网络上观察到的数百万个请求的模式构建的检测逻辑对流量进行分类。该分类无需提前知道特定主机或 URL，即可识别 MCP 协商和到主机名的代理。

从今天起，所有 Cloudflare Zero Trust 客户都可以在其 Gateway HTTP 日志中看到 MCP 流量的迹象，并可以使用新的 Gateway 选择器显式阻止或允许该流量：

experimental.is_mcp == true

该选择器是一个布尔值。如果 Gateway 在 TLS 检查的请求上检测到 `MCP-Protocol-Version` 头，则该值为 `true`，管理员可以在 Allow 或 Block 策略中使用它，而无需维护自己的 MCP 样式域名列表。

直接加密流量必须先经过 TLS 解密，Gateway 才能检查这些头，而本地 stdio 服务器、网络外连接、Do Not Inspect 流量以及从未经过 Gateway 的请求仍不在该视图范围内。

## 跨网络查看 MCP 流量

今天，我们推出一个专门的 MCP 流量仪表板，显示哪些主机在你的网络中提供 MCP 流量，哪些用户产生了该流量，以及请求是通过你的 Cloudflare MCP Portal 还是完全绕过它们。

![image4.png](/images/posts/62a1385858fd.jpg)

该仪表板显示：

- 可配置时间窗口内的 MCP 请求总数、唯一用户数和唯一服务器数
- 随时间变化的 MCP 服务器及其每服务器请求计数
- 按入口分类的流量细分，将 MCP Portal 流量与直接设备客户端连接区分开来
- 在 Portal 之外看到的热门 MCP 服务器，这是最重要的 Shadow MCP 流量
- 按 MCP 请求量排名的热门用户

![image2.png](/images/posts/b00306e8e684.jpg)

管理员可以按特定服务器、用户或入口类型进行筛选，并直接导航到按相关主机或用户筛选的 Gateway HTTP 日志以进行深入调查。

![image1.png](/images/posts/81539300ed95.jpg)

## 将发现的服务器纳入 MCP Portal

MCP 发现将未知流量转化为管理员可以调查的列表。当组织批准其中一台服务器时，可以将其置于 Cloudflare MCP 服务器 Portal 之后。该 Portal 为员工提供一个受管理的端点，并在上游服务器之前放置 Access 身份验证、精选工具目录和日志记录。管理员可以通过 Gateway 路由兼容的上游调用，以应用 HTTP 策略、可预测的出站流量和数据丢失防护，无论是跨整个 Portal 还是针对单个服务器。工具活动也可以通过 Logpush 导出。发现仪表板随后可以区分使用 Portal 的请求与直接连接到同一服务器的请求。

这创建了一条从发现到治理的路径：找到服务器，决定是否批准，将已批准的使用迁移到 Portal 之后，并调查继续绕过 Portal 的流量。最后一步至关重要，因为未批准的服务器和绕过已批准服务器是两个不同的问题。

## 强制仅通过 Portal 访问

我们正在为Gateway Network和HTTP策略添加流量来源选择器，使管理员能够基于流量是否来自您的MCP门户来编写规则，以精确控制MCP流量。

当MCP门户流量通过Gateway路由时，它会携带`mcp_portal`流量来源标记，这让策略能够区分通过门户代理的请求和员工的直接连接。一个基础的强制执行规则如下：

```
experimental.is_mcp == true and not traffic.onramp in ("mcp_portal")
操作：阻止
```

![image3.png](/images/posts/ee0e0b210568.jpg)

任何检测到的、未通过门户到达的MCP流量都将被阻止；通过门户到达的流量则不受影响。对于希望在强制执行前先进行观察的组织，现在已解密的流量的HTTP日志中包含了流量来源和MCP检测信息，因此您可以在无需策略的情况下监控代理流量的行为。

## 更多MCP服务器现在可以使用受管路径

一条获批的路径只有在能够连接到员工实际需要的关键服务器时才有用。

早期的MCP规范推荐使用动态客户端注册，即客户端在没有OAuth应用的情况下向授权服务器注册自身。许多常见的OAuth提供商使用不同的模型：它们要求管理员注册一个具有固定客户端ID、客户端密钥、回调URL和作用域集合的应用。MCP 2026-07-28规范最近也弃用了动态注册。

为帮助缓解这一问题，MCP门户现在支持预注册的OAuth客户端。管理员可以配置手动OAuth凭据，将仪表板中显示的回调URL注册到上游提供商，并输入客户端凭据。门户会在可用时自动发现标准的OAuth元数据，当无法发现时，管理员可以提供授权、令牌、撤销和签发者端点。

每个用户仍然需要授权对其各自上游数据源的访问，存储的客户端密钥仅用于获取更新的工具和提示词列表。

手动OAuth支持现在有助于覆盖OAuth实现的多种变体。一些提供商需要自定义请求头、个人访问令牌或显式的客户端允许列表，这些是独立的兼容性问题。我们将在未来几个月继续扩展MCP门户的OAuth支持。

## 将私有MCP服务器纳入同一门户

公共SaaS工具只是企业MCP目录的一部分。企业依赖的大多数安全信息无法从公共互联网获取；它们存在于公共或私有云基础设施中，或托管在本地，只能通过私有网络连接访问。

目前，MCP门户必须能够通过公共互联网解析并到达上游服务器。这意味着仅可通过私有网络访问的服务器——通过私有DNS或位于私有IP空间内——门户无法到达。我们正在努力让MCP门户能够通过Cloudflare Gateway路由和已用于其他私有应用的同一Cloudflare One网络连接到私有服务器。

私有服务器保留其私有主机名；门户通过Cloudflare的私有路由到达它，并将其工具与公共上游服务器一起展示；Access策略、门户日志记录和工具控制继续在同一入口处生效。

通过Gateway路由门户流量也会为其打上`mcp_portal`流量来源标记，因此Gateway策略可以区分门户请求和员工直接连接。MCP服务器的私有连接功能正在积极开发中；请关注Changelog以获取更多信息。

## Agents SDK支持新的无状态模型

几周前，MCP项目发布了2026-07-28规范，这是一次重大修订，将连接作用域的初始化替换为无状态的、每请求模型。我们在《下一代MCP》中介绍了协议变更和迁移路径。

Cloudflare Agents SDK v0.20.0同时作为客户端和服务器支持MCP 2026-07-28。对于每个连接，客户端首先通过`server/discover`探测新的无状态协议；如果服务器不支持，客户端会在同一连接上继续使用传统的`initialize`握手。现有的`addMcpServer`调用不需要单独设置协议或单独的客户端。

在服务器端，`createMcpHandler`可以从Worker提供无状态的工具、提示词、资源和引导，而无需创建传输会话或Durable Object：

```
import { McpServer } from "@modelcontextprotocol/server";
import { createMcpHandler } from "agents/mcp/server";

function createServer() {
  return new McpServer({ name: "example", version: "1.0.0" });
}

export default {
  fetch(request, env, ctx) {
    return createMcpHandler(createServer)(request, env, ctx);
  },
} satisfies ExportedHandler;
```

回退机制很重要，因为协议迁移很少会一次性完成。新客户端仍然需要访问现有服务器，新服务器也需要处理尚未迁移的客户端。在生态系统过渡期间，Agents SDK同时支持两条路径。

## 从可见性开始，然后关闭不应存在的路径

一个可行的MCP安全方案始于了解用户的流量特征、MCP使用情况，并就批准的工具集和访问方法达成一致。

首先，检查通过Gateway的MCP流量，将其目的地与组织已批准的服务器进行比较。将更多已批准的服务器迁移到MCP门户之后。

然后，强制执行您可以控制的边界。组合使用Gateway策略，将MCP检测条件与流量来源和目的地条件结合，阻止来自受管设备和站点的直接MCP连接，并在可能的情况下将自托管上游服务器限制为仅允许门户流量。

我们很快将添加更细粒度的MCP流量可见性和控制功能，包括对特定工具使用的控制，以及针对环境中所有MCP服务器（无论您的安全组织是否知晓）的新工具使用报告。

我们的MCP流量检测教程介绍了当前可用于Gateway日志的主机名、路径和JSON-RPC启发式规则。随着新信号正式可用，我们将更新文档以包含协议选择器的详细信息。

- Cloudflare
- Kenny Johnson

---

> 本文由AI自动翻译，原文链接：[How Cloudflare detects MCP traffic and helps secure it](https://blog.cloudflare.com/mcp-security-updates/)
> 
> 翻译时间：2026-08-15 03:05
