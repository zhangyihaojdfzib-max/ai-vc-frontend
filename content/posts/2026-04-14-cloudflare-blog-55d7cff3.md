---
title: Cloudflare Mesh发布：为AI智能体提供安全私有网络连接
title_original: "Secure private networking for everyone: users, nodes, agents, Workers\
  \ â\x80\x94 introducing Cloudflare Mesh"
date: '2026-04-14'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/mesh/
author: ''
summary: Cloudflare正式推出Mesh服务，旨在解决AI智能体访问私有网络资源的安全难题。传统VPN、SSH等方式难以满足自主智能体的访问需求，Mesh通过集成Cloudflare
  One平台，为智能体、Workers及团队提供零信任私有网络连接。它支持从个人助手到企业编码智能体的多种工作流，并允许逐步扩展至网关策略、数据防泄漏等高级安全功能，无需复杂迁移即可实现安全可控的智能体基础设施访问。
categories:
- AI基础设施
tags:
- Cloudflare
- 私有网络
- AI智能体
- 零信任安全
- SASE
draft: false
translated_at: '2026-04-15T04:48:04.278199'
---

# 为所有人提供安全的私有网络连接：用户、节点、智能体、Workers —— Cloudflare Mesh 正式发布

2026-04-14

- Nikita Cano
- Thomas Gauvin

![](/images/posts/70ae669eee95.png)

AI 智能体已经改变了团队对私有网络访问的思考方式。您的编码智能体需要查询暂存数据库。您的生产智能体需要调用内部 API。您的个人 AI 助手需要访问您家庭网络中运行的服务。客户端不再仅仅是人类或服务。它们是智能体，自主运行，向您需要保护的基础设施发出您未明确批准的请求。

这些工作流都存在一个相同的根本问题：智能体需要访问私有资源，但实现这一点的工具是为人类而非自主软件构建的。VPN 需要交互式登录。SSH 隧道需要手动设置。将服务公开暴露存在安全风险。而且，这些方法都无法让您在智能体连接后了解其实际行为。

今天，我们推出 **Cloudflare Mesh**，将您的私有网络连接在一起，并为您的智能体提供安全访问。我们还将 Mesh 与 **Cloudflare 开发者平台** 集成，使得 **Workers**、**Durable Objects** 以及使用 Agents SDK 构建的智能体能够直接访问您的私有基础设施。

如果您正在使用 **Cloudflare One** 的 SASE 和零信任套件，您已经可以使用 Mesh。您不需要新的技术范式来保护智能体工作负载。您需要一个为智能体时代构建的 SASE，那就是 Cloudflare One。Cloudflare Mesh 是一种具有更简单设置的新体验，它利用了您已经熟悉的接入方式：**WARP Connector**（现称为 Cloudflare Mesh 节点）和 **WARP Client**（现称为 Cloudflare One Client）。它们共同为人类用户、开发者和智能体流量创建了一个私有网络。Mesh 直接集成到您现有的 Cloudflare One 部署中。您现有的 Gateway 策略、Access 规则和设备状态检查会自动应用于 Mesh 流量。

如果您是一名开发者，只想为您的智能体、服务和团队提供私有网络连接，Mesh 是您的起点。几分钟内即可完成设置，连接您的网络，并保护您的流量。由于 Mesh 运行在 **Cloudflare One** 平台上，您可以逐步扩展至更高级的功能：用于细粒度流量控制的 **Gateway** 网络、DNS 和 HTTP 策略，用于 SSH 和 RDP 会话管理的 **Access for Infrastructure**，用于安全网页访问的 **Browser Isolation**，防止敏感数据离开您网络的 **DLP**，以及用于 SaaS 安全的 **CASB**。您无需在第一天就规划好所有这些。您只需在需要时无需迁移即可使用。

## 新的智能体工作流

私有网络连接始终是关于将客户端连接到资源——通过 SSH 连接到服务器、查询数据库、访问内部 API。改变的是客户端的身份。一年前，答案是您的开发者和您的服务。今天，越来越多的是您的智能体。

这并非理论。看看生态系统：提供工具访问的 **MCP（模型上下文协议）服务器** 激增，需要从私有代码库和数据库读取的编码智能体，在家庭硬件上运行的个人助手。这些模式都假设智能体能够访问其所需的资源。当这些资源被隔离在私有网络中时，智能体就束手无策了。

这导致了三种目前难以安全实现的工作流：

1.  **从移动设备访问个人智能体**。您在家中的 Mac mini 上运行 OpenClaw。您想从手机、咖啡店的笔记本电脑或工作电脑访问它。但将其暴露在公共互联网上（即使有密码保护）可能会留下一些漏洞。您的智能体拥有 shell 访问权限、文件系统访问权限以及对您家庭网络的网络访问权限。一个配置错误，任何人都可能访问到它。
2.  **让编码智能体访问您的暂存环境**。您在笔记本电脑上使用 Claude Code、Cursor 或 Codex。您要求它检查部署状态、从暂存数据库查询分析数据或从内部对象存储读取数据。但这些服务位于私有云 VPC 中，因此您的智能体无法访问它们，除非将它们暴露到互联网或将整个笔记本电脑隧道连接到 VPC。
3.  **将已部署的智能体连接到私有服务**。您正在使用 Cloudflare Workers 上的 **Agents SDK** 将智能体构建到您的产品中。这些智能体需要调用内部 API、查询数据库以及访问不在公共互联网上的服务。它们需要私有访问，但要有范围限定的权限、审计跟踪且不泄露凭据。

从移动设备访问个人智能体。您在家中的 Mac mini 上运行 OpenClaw。您想从手机、咖啡店的笔记本电脑或工作电脑访问它。但将其暴露在公共互联网上（即使有密码保护）可能会留下一些漏洞。您的智能体拥有 shell 访问权限、文件系统访问权限以及对您家庭网络的网络访问权限。一个配置错误，任何人都可能访问到它。

让编码智能体访问您的暂存环境。您在笔记本电脑上使用 Claude Code、Cursor 或 Codex。您要求它检查部署状态、从暂存数据库查询分析数据或从内部对象存储读取数据。但这些服务位于私有云 VPC 中，因此您的智能体无法访问它们，除非将它们暴露到互联网或将整个笔记本电脑隧道连接到 VPC。

将已部署的智能体连接到私有服务。您正在使用 Cloudflare Workers 上的 Agents SDK 将智能体构建到您的产品中。这些智能体需要调用内部 API、查询数据库以及访问不在公共互联网上的服务。它们需要私有访问，但要有范围限定的权限、审计跟踪且不泄露凭据。

## Cloudflare Mesh：为用户、节点和智能体构建的统一私有网络

Cloudflare Mesh 是开发者友好的私有网络连接方案。一个轻量级连接器，一个二进制文件，连接一切：您的个人设备、远程服务器、用户终端。您无需为每种模式安装单独的工具。在您的网络上安装一个连接器，所有访问模式即可工作。

连接后，您私有网络中的设备可以通过私有 IP 相互通信，流量通过 Cloudflare 覆盖 330 多个城市的全球网络进行路由，为您提供更好的网络可靠性和控制力。

现在，有了 Mesh，一个单一的解决方案就能解决我们上面提到的所有智能体场景：

*   通过在手机上安装 **Cloudflare One Client for iOS**，您可以通过 Mesh 私有网络将移动设备安全地连接到运行 OpenClaw 的本地 Mac mini。
*   通过在笔记本电脑上安装 **Cloudflare One Client for macOS**，您可以将笔记本电脑连接到您的私有网络，以便您的编码智能体能够访问暂存数据库或 API 并进行查询。
*   通过在 Linux 服务器上部署 **Mesh 节点**，您可以将外部云中的 VPC 连接在一起，让智能体能够访问外部私有网络中的资源和 MCP。

通过在手机上安装 Cloudflare One Client for iOS，您可以通过 Mesh 私有网络将移动设备安全地连接到运行 OpenClaw 的本地 Mac mini。

通过在笔记本电脑上安装 Cloudflare One Client for macOS，您可以将笔记本电脑连接到您的私有网络，以便您的编码智能体能够访问暂存数据库或 API 并进行查询。

通过在 Linux 服务器上部署 Mesh 节点，您可以将外部云中的 VPC 连接在一起，让智能体能够访问外部私有网络中的资源和 MCP。

由于 Mesh 由 **Cloudflare One Client** 驱动，每个连接都继承了 Cloudflare One 平台的安全控制。Gateway 策略适用于 Mesh 流量。设备状态检查验证连接设备。DNS 过滤捕获可疑查询。您无需额外配置即可获得这些功能：保护人类流量的相同策略也保护您的智能体流量。

## 在 Mesh 和 Tunnel 之间选择

随着Mesh的推出，您可能会问：我应该在何时使用Mesh而非Tunnel？两者都能将外部网络私密地连接到Cloudflare，但它们用途不同。Cloudflare Tunnel是单向流量的理想解决方案，适用于Cloudflare从边缘代理流量至特定私有服务（如Web服务器或数据库）的场景。

另一方面，Cloudflare Mesh提供了一个完整的双向、多对多网络。您Mesh上的每个设备和节点都可以使用其私有IP相互访问。网络中运行的应用程序或Agent（智能体）能够发现并访问Mesh上的任何其他资源，而无需每个资源都配置独立的Tunnel。

## 借助Cloudflare网络的力量

Cloudflare Mesh让您享有网状网络的各项优势（弹性、高可扩展性、低延迟和高性能），同时通过将所有流量路由至Cloudflare，它解决了网状网络的一个关键挑战：NAT穿透。

互联网的大部分都处于NAT（网络地址转换）之后。这种机制通过映射公网报头与私有内部地址之间的流量，使得整个本地设备网络可以共享一个公网IP地址。当两个设备都位于NAT之后时，直接连接可能失败，流量不得不回退到中继服务器。如果您的自建中继基础设施覆盖点有限，相当一部分流量将经过这些中继，从而增加延迟并降低可靠性。虽然您可以尝试自托管中继服务器来弥补，但这意味着仅仅为了连接现有网络，就需要承担管理额外基础设施的负担。

Cloudflare Mesh采用了不同的方法。所有Mesh流量都通过Cloudflare的全球网络进行路由，该基础设施同样服务于互联网上一些最大规模的网站。对于跨区域或多云流量，这种方式始终优于公共互联网路由。不存在性能降级的备用路径，因为Cloudflare边缘网络本身就是路径。

通过Cloudflare路由还意味着每个数据包都会经过Cloudflare的安全防护栈。这是在Cloudflare One平台上构建Mesh的关键优势：安全不是事后附加的独立产品。通过利用这同一全球骨干网，我们可以从一开始就为每个团队提供这些核心支柱：

**50个节点和50个用户免费。** 您的整个团队和整个测试环境可共用一个私有网络，包含在每个Cloudflare账户中。

**全球边缘路由。** 330多个城市，优化的骨干网路由。没有覆盖点有限的中继服务器。没有性能降级的备用路径。

**从第一天起就具备安全控制。** Mesh运行在Cloudflare One上。网关策略、DNS过滤、DLP、流量检查和设备状态检查都在同一平台上可用。从简单的私有连接开始。当需要流量过滤时开启网关策略。当需要为SSH和RDP提供会话级控制时启用基础设施访问。当需要防止敏感数据离开网络时添加DLP。每项功能都只需一键切换。

**高可用性。** 创建启用高可用性的Mesh节点，并使用同一令牌在主动-被动模式下启动多个连接器。它们宣告相同的IP路由，因此如果一个节点故障，流量会自动故障转移。

## 通过Workers VPC与开发者平台集成

Mesh连接您跨外部云的Agent（智能体）和资源，但您也需要能够从基于Workers和Agents SDK构建的Agent（智能体）进行连接。为此，我们扩展了Workers VPC，使您的整个Mesh网络对Workers和Durable Objects可访问。

这意味着您可以从Workers连接到您的Cloudflare Mesh网络，通过单个绑定的`fetch()`调用即可访问整个网络。这补充了Workers VPC对Cloudflare Tunnel的现有支持，让您在选择如何保护网络时有更多选择。现在，您可以在`wrangler.jsonc`文件中指定要连接的整个网络。要绑定到您的Mesh网络，请使用绑定到您账户Mesh网络的`cf1:network`保留关键字：

```Shell
"vpc_networks": [
  { "binding": "MESH", "network_id": "cf1:network", "remote": true },
  { "binding": "AWS_VPC", "tunnel_id": "350fd307-...", "remote": true }
]

```

然后，您可以在Worker或Agent（智能体）代码中使用它：

```javascript
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    // 访问Mesh上的任何内部主机，无需预先注册
    const apiResponse = await env.MESH.fetch("http://10.0.1.50/api/data");

    // 通过隧道的私有DNS解析器解析内部主机名
    const dbResponse = await env.AWS_VPC.fetch("http://internal-db.corp.local:5432");

    return new Response(await apiResponse.text());
  },
};

```

通过将开发者平台连接到您的Mesh网络，您可以构建能够安全访问私有数据库、内部API和MCP的Workers，从而构建为您的应用提供Agent（智能体）能力的跨云Agent（智能体）和MCP。同时，这也开启了一个新世界：Agent（智能体）可以自主端到端地观察您的整个技术栈，交叉引用日志并实时建议优化。

## 整体如何协同工作

Cloudflare Mesh、Workers VPC和Agents SDK共同为您的Agent（智能体）提供了一个跨越Cloudflare和外部云的统一私有网络。我们融合了连接与计算，使您的Agent（智能体）能够安全地访问其所需的资源，无论它们位于全球何处。

**Mesh节点**是您的服务器、虚拟机和容器。它们运行无头版本的Cloudflare One Client并获取一个Mesh IP。服务通过私有IP进行双向通信，流量通过Cloudflare边缘路由。

**设备**是您的笔记本电脑和手机。它们运行Cloudflare One Client并直接访问Mesh节点：SSH、数据库查询、API调用，全部通过私有IP进行。您的本地编码Agent（智能体）使用此连接访问私有资源。

**Workers上的Agent（智能体）**通过Workers VPC网络绑定访问私有服务。它们获得由MCP协调的整个网络的限定访问权限。网络强制执行Agent（智能体）可以访问的范围，MCP服务器则强制执行Agent（智能体）可以执行的操作。

## 未来展望

当前版本的Mesh为安全、统一的连接奠定了基础。但随着Agent（智能体）工作流变得更加复杂，我们正致力于超越简单的连接，构建一个更易于管理、并能更精细地感知谁（或什么）正在与您的服务通信的网络。以下是我们今年剩余时间正在构建的内容。

#### 主机名路由

我们将在今年夏季把Cloudflare Tunnel的主机名路由功能扩展到Mesh。您的Mesh节点将能够接收私有主机名（如`wiki.local`或`api.staging.internal`）的流量，而无需您管理IP列表或担心这些主机名在Cloudflare边缘如何解析。通过名称而非IP将流量路由到服务。如果您的基础设施使用动态IP、自动扩展组或临时容器，这将消除一整类的路由难题。

#### Mesh DNS

目前，您通过Mesh IP访问Mesh节点：`ssh 100.64.0.5`。这可行，但不符合您对基础设施的思考方式。您通常使用名称思考：`postgres-staging`、`api-prod`、`nikitas-openclaw`。

今年晚些时候，我们将构建Mesh DNS，使加入Mesh的每个节点和设备自动获得一个可路由的内部主机名。无需DNS配置或手动记录。添加一个名为`postgres-staging`的节点，`postgres-staging.mesh`就会从Mesh上的任何设备解析到正确的Mesh IP。

结合主机名路由，您将能够执行`ssh postgres-staging.mesh`或`curl http://api-prod.mesh:3000/health`，而无需了解或管理IP地址。

#### 身份感知路由

如今，Mesh节点已能向Cloudflare边缘进行身份验证，但它们在网络层共享同一身份。设备通过Cloudflare One客户端以用户身份进行验证，但节点尚未携带可供Gateway策略区分的独立、可路由身份。

我们想要改变这一现状。目标是为Mesh实现身份感知路由，让每个节点、每台设备乃至每个Agent（智能体）都拥有可供策略评估的独立身份。您将不再基于IP范围编写规则，而是根据连接对象来制定规则。

这对Agent（智能体）尤为重要。当前，当运行在Workers上的Agent（智能体）通过VPC绑定调用工具时，目标服务只能识别到Worker发出的请求。它无法知晓是哪个Agent（智能体）在调用、由谁授权，或授予了何种权限范围。在Mesh侧，当您笔记本电脑上的本地编程Agent（智能体）访问临时环境服务时，Gateway能识别您的设备身份，却无法识别Agent（智能体）身份。

我们正在构建一种让Agent（智能体）在网络中携带自身身份的模型：

- 主体/授权人：执行操作的人类授权者（平台团队的Nikita）
- Agent（智能体）：执行操作的AI系统（部署助手，会话#abc123）
- 权限范围：允许Agent（智能体）执行的操作（仅可读取部署信息、触发回滚，不可进行其他操作）

主体/授权人：执行操作的人类授权者（平台团队的Nikita）

Agent（智能体）：执行操作的AI系统（部署助手，会话#abc123）

权限范围：允许Agent（智能体）执行的操作（仅可读取部署信息、触发回滚，不可进行其他操作）

这将使您能够制定如下策略：允许Nikita的Agent（智能体）执行读取操作，但写入操作需由Nikita本人执行。Agent（智能体）流量可与人类流量分开过滤。即使不触及Nikita的权限，也可单独撤销某个Agent（智能体）的网络访问权。

实现此功能的基础设施已就绪：Mesh节点通过单节点令牌配置，设备通过单用户身份验证，Workers VPC绑定则限定每项服务的访问范围。目前缺失的环节是让策略层能识别这些身份，使Gateway能基于身份信息做出路由和访问决策。这正是我们正在构建的功能。

#### 容器化Mesh

当前Mesh节点运行于虚拟机和裸机Linux服务器。但现代基础设施正日益容器化：Kubernetes Pod、Docker Compose堆栈、临时CI/CD运行器。我们正在构建Mesh Docker镜像，让您能在任何容器化环境中添加Mesh节点。

这意味着您可以在Docker Compose堆栈中加入Mesh边车容器，并为堆栈中的所有服务提供私有网络访问。在临时集群容器中运行的微服务，可通过Mesh访问生产环境VPC中的数据库，而双方均无需公开端点。

这对于需要在构建和测试期间访问私有基础设施的CI/CD流水线同样实用：您的GitHub Actions运行器拉取Mesh容器镜像，加入您的网络，针对临时环境运行集成测试，然后销毁。整个过程无需管理VPN凭证或维护持久隧道——容器退出时节点即自动消失。

我们预计Mesh Docker镜像将于今年晚些时候发布。

## 立即开始

在我们持续完善这些身份与路由功能的同时，安全统一的网络基础现已就绪。您只需几分钟即可开始桥接云端资源并保护您的Agent（智能体）。

开始使用Cloudflare Mesh：请访问Cloudflare控制面板中的网络> Mesh。50个节点及50名用户以内免费使用。

使用Agents SDK和Workers VPC构建Agent（智能体）：安装Agents SDK（`npm i agents`），按照Workers VPC快速入门指南操作，并构建具有私有后端访问权限的远程MCP服务器。

已在使用Cloudflare One？Mesh可与您现有设置无缝协作。您的Gateway策略、设备状态检查和访问规则将自动应用于Mesh流量。请参阅Mesh文档添加您的首个节点。

#### 在Cloudflare TV上观看

---

> 本文由AI自动翻译，原文链接：[Secure private networking for everyone: users, nodes, agents, Workers â introducing Cloudflare Mesh](https://blog.cloudflare.com/mesh/)
> 
> 翻译时间：2026-04-15 04:48
