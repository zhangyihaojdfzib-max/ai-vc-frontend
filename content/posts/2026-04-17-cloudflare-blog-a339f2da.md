---
title: Cloudflare推出Agent就绪度评分，助网站优化适配AI Agent
title_original: Introducing the Agent Readiness score. Check to see if your site is
  agent-ready
date: '2026-04-17'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/agent-readiness/
author: ''
summary: Cloudflare发布新工具isitagentready.com，帮助网站所有者评估和优化其网站对AI Agent的适配程度。该工具从可发现性、内容格式、机器人访问控制和能力四个维度进行评分，并提供可操作的改进建议。同时，Cloudflare
  Radar新增数据集，追踪互联网上AI Agent相关标准的采用情况。文章指出当前网络对Agent的友好度普遍较低，但新兴标准的早期采用者将获得竞争优势。
categories:
- AI基础设施
tags:
- AI Agent
- 网站优化
- Cloudflare
- 网络标准
- 开发者工具
draft: false
translated_at: '2026-04-18T04:40:21.635307'
---

# 推出Agent就绪度评分。您的网站是否为Agent做好准备？

2026-04-17

- AndrÃ© Jesus
- Vance Morrison

![](/images/posts/8d31d26c506d.png)

网络始终需要适应新标准。它学会了与网络浏览器对话，然后学会了与搜索引擎对话。现在，它需要与AI Agent对话。

今天，我们很高兴地推出 isitagentready.com——这是一个新工具，旨在帮助网站所有者了解如何优化其网站以适应Agent，从指导Agent如何进行身份验证，到控制Agent可以访问哪些内容、接收内容的格式以及如何为其付费。我们还将向 Cloudflare Radar 引入一个新的数据集，用于追踪互联网上各项Agent标准的整体采用情况。

我们希望以身作则。这也是为什么我们同时分享了最近如何彻底改造 Cloudflare 的开发者文档，使其成为对Agent最友好的文档网站，让AI工具能够更快、更经济地回答问题。

## 当今网络对Agent的友好程度如何？

简短的回答是：不太友好。这在意料之中，但也表明如果标准得到采用，Agent的效能将比现在高出许多。

为了分析这一点，Cloudflare Radar 选取了互联网上访问量最大的20万个域名；过滤掉了Agent就绪度不重要的类别（如重定向、广告服务器和隧道服务），重点关注AI Agent实际可能需要与之交互的企业、出版商和平台；并使用我们的新工具对它们进行了扫描。

其结果是一个新的“AI Agent标准采用情况”图表，现在可以在 Cloudflare Radar AI Insights 页面找到，我们可以在其中衡量多个域名类别中各项标准的采用情况。

观察各项具体检查，有几个方面尤为突出：

- robots.txt 几乎无处不在——78%的网站都有一个——但绝大多数是为传统搜索引擎爬虫编写的，而非AI Agent。
- 内容信号：4%的网站在 robots.txt 中声明了其AI使用偏好。这是一项正在兴起的新标准。
- Markdown内容协商（在 Accept: text/markdown 时提供 text/markdown 内容）在 3.9% 的网站上通过。
- 新兴标准，如 MCP Server Cards 和 API Catalogs (RFC 9727)，在整个数据集中总共出现在不到15个网站上。现在还为时过早——通过成为首批采用新标准并能与Agent良好协作的网站之一，有大量机会脱颖而出。

此图表将每周更新，数据也可以通过 Data Explorer 或 Radar API 访问。

## 获取您网站的Agent就绪度评分

您可以访问 isitagentready.com 并输入网站URL，来获取您自己网站的Agent就绪度评分。

提供可操作反馈的评分和审计，过去曾帮助推动了新标准的采用。例如，Google Lighthouse 根据性能和安全性最佳实践对网站进行评分，并指导网站所有者采用最新的网络平台标准。我们认为应该存在类似的东西，以帮助网站所有者采用针对Agent的最佳实践。

当您输入您的网站时，Cloudflare 会向其发出请求以检查其支持哪些标准，并根据四个维度提供评分：

- 可发现性：robots.txt, sitemap.xml, Link Headers (RFC 8288)
- 内容：面向Agent的Markdown
- 机器人访问控制：内容信号, robots.txt中的AI机器人规则, Web Bot Auth
- 能力：Agent Skills, API Catalog (RFC 9727), 通过 RFC 8414 和 RFC 9728 进行OAuth服务器发现, MCP Server Card, 以及 WebMCP

此外，我们还会检查网站是否支持Agentic商务标准，包括 x402、Universal Commerce Protocol 和 Agentic Commerce Protocol，但这些目前不计入评分。

对于每项未通过的检查，我们都会提供一个提示词，您可以将其交给您的编码Agent，让它代表您实现支持。

该网站本身也对Agent友好，践行其倡导的理念。它通过可流式传输的HTTP公开了一个无状态的MCP服务器（https://isitagentready.com/.well-known/mcp.json），其中包含一个 scan_site 工具，因此任何兼容MCP的Agent都可以在不使用Web界面的情况下以编程方式扫描网站。它还发布了一个Agent Skills索引（https://isitagentready.com/.well-known/agent-skills/index.json），其中包含其检查的每项标准的技能文档，因此Agent不仅知道要修复什么，还知道如何修复。

让我们深入探讨每个类别中的检查项，以及它们为何对Agent重要。

### 可发现性

robots.txt 自1994年就已存在，大多数网站都有一个。它对Agent有两个作用：定义爬取规则（谁可以访问什么）以及指向您的站点地图。站点地图是一个XML文件，列出了您网站上的每条路径，本质上是Agent可以遵循的地图，用以发现您所有内容，而无需爬取每个链接。robots.txt 是Agent首先查看的地方。

除了站点地图，Agent还可以直接从HTTP响应头中发现重要资源，具体来说，是使用 Link 响应头 (RFC 8288)。与隐藏在HTML内部的链接不同，Link 头是HTTP响应本身的一部分，这意味着Agent无需解析任何标记语言就能找到资源的链接：

```Rust
HTTP/1.1 200 OK
Link: </.well-known/api-catalog>; rel="api-catalog"
```

### 内容可访问性

让Agent访问您的网站是一回事。确保它能够真正阅读您的内容是另一回事。

早在2024年9月（考虑到AI发展速度之快，感觉像是很久以前），llms.txt 被提议作为一种为网站提供LLM友好表示形式的方式，并适应模型的上下文窗口。llms.txt 是位于您网站根目录的一个纯文本文件，为Agent提供一个结构化的阅读列表：网站是什么、上面有什么以及重要内容的位置。可以把它看作是为LLM阅读而写的站点地图，而不是为爬虫索引而写的：

```Rust
# My Site
> A developer platform for building on the edge.
## Documentation
- [Getting Started](https://example.com/docs/start.md)
- [API Reference](https://example.com/docs/api.md)
## Changelog
- [Release Notes](https://example.com/changelog.md)
```

Markdown内容协商 更进一步。当Agent获取任何页面并发送 Accept: text/markdown 头时，服务器会响应一个干净的Markdown版本，而不是HTML。Markdown版本所需的Token数量要少得多——我们测量到在某些情况下Token减少高达80%——这使得响应更快、更便宜，并且考虑到大多数Agent工具默认的上下文窗口限制，更有可能被完整消费。

默认情况下，我们只检查网站是否正确处理Markdown内容协商，而不检查 llms.txt。您可以选择自定义扫描以包含 llms.txt。

### 机器人访问控制

既然Agent可以浏览您的网站并消费您的内容，下一个问题是：您想让任何机器人都这样做吗？

robots.txt 的作用远不止指向站点地图。它也是您定义访问规则的地方。您可以明确声明允许哪些爬虫访问，以及它们可以访问哪些内容，甚至可以精确到特定路径。这一约定已牢固确立，并且仍然是任何行为规范的机器人在开始爬取前首先查看的地方。

内容信号让您能够更精确地控制。您不仅可以允许或阻止，还可以明确声明AI可以对您的内容做什么。通过在您的 `robots.txt` 中使用 `Content-Signal` 指令，您可以独立控制三件事：您的内容是否可用于AI训练（`ai-train`），是否可用作AI推理和事实依据的输入（`ai-input`），以及是否应出现在搜索结果中（`search`）：

```Rust
User-agent: *
Content-Signal: ai-train=no, search=yes, ai-input=yes
```

相反地，**Web Bot Auth** IETF 草案标准允许友好的机器人进行身份验证，并允许接收机器人请求的网站识别它们。机器人对其HTTP请求进行签名，接收站点使用机器人发布的公钥来验证这些签名。

这些公钥存放在一个众所周知的端点 `/.well-known/http-message-signatures-directory`，我们将其作为扫描的一部分进行检查。

并非所有站点都需要实现此功能。如果您的站点仅提供内容，而不向其他站点发出请求，则不需要它。但随着互联网上越来越多的站点运行自己的Agent并向其他站点发出请求，我们预计这一点将变得越来越重要。

### 协议发现

除了被动消费内容，Agent还可以通过调用API、调用工具和自主完成任务等方式直接与您的站点交互。

如果您的服务有一个或多个公共API，**API目录（RFC 9727）** 为Agent提供了一个单一的、众所周知的位置来发现所有这些API。它托管在 `/.well-known/api-catalog`，列出了您的API并链接到其规范、文档和状态端点，无需Agent抓取您的开发者门户或阅读您的文档。

谈到Agent就不能不提到 **MCP**。**模型上下文协议** 是一个开放标准，允许AI模型连接到外部数据源和工具。您无需为每个AI工具构建自定义集成，只需构建一个MCP服务器，任何兼容的Agent都可以使用它。

为了帮助Agent找到您的MCP服务器，您可以发布一个 **MCP服务器卡片**（目前处于草案阶段的提案）。这是一个位于 `/.well-known/mcp/server-card.json` 的JSON文件，在Agent连接之前就描述了您的服务器：它公开了哪些工具、如何访问以及如何进行身份验证。Agent读取此文件后，便知道开始使用您的服务器所需的一切信息：

```JSON
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/mcp-server-card/v1.json",
  "version": "1.0",
  "protocolVersion": "2025-06-18",
  "serverInfo": {
    "name": "search-mcp-server",
    "title": "Search MCP Server",
    "version": "1.0.0"
  },
  "description": "Search across all documentation and knowledge base articles",
  "transport": {
    "type": "streamable-http",
    "endpoint": "/mcp"
  },
  "authentication": {
    "required": false
  },
  "tools": [
    {
      "name": "search",
      "title": "Search",
      "description": "Search documentation by keyword or question",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": { "type": "string" }
        },
        "required": ["query"]
      }
    }
  ]
}
```

当Agent拥有 **Agent技能** 来帮助它们执行特定任务时，它们的工作效果最佳——但Agent如何发现一个站点提供了哪些技能呢？我们提议站点可以在 `.well-known/agent-skills/index.json` 提供此信息，这个端点告诉Agent有哪些可用技能以及在哪里可以找到它们。您可能会注意到 `.well-known` 标准（RFC 8615）被许多其他Agent和授权标准使用——感谢Cloudflare自己的Mark Nottingham（他撰写了该标准）以及其他IETF贡献者！

许多站点要求您先登录才能访问。这使得人类很难授予Agent代表他们访问这些站点的能力，这也是为什么有些人采取了可能不安全的方法，即让Agent访问用户已登录会话的Web浏览器。

有一种更好的方法可以让人类明确授予访问权限：支持OAuth的站点可以告诉Agent在哪里找到授权服务器（RFC 9728），允许Agent引导用户完成OAuth流程，用户可以在其中选择适当地授予Agent访问权限。在2026年Agent周上宣布，**Cloudflare Access** 现已完全支持此OAuth流程，我们展示了像OpenCode这样的Agent如何利用此标准，在用户向Agent提供受保护的URL时使其正常工作：

### 商务

Agent也可以代表您购买商品——但网络支付是为人类设计的。添加到购物车、输入信用卡、点击支付。当购买者是AI Agent时，这个流程完全失效。

**x402** 在协议层面解决了这个问题，它复兴了 **HTTP 402 Payment Required**，这是一个自1997年以来就存在于规范中但从未被广泛使用的状态码。流程很简单：Agent请求一个资源，服务器用402响应和一个描述支付条款的机器可读负载来回复，Agent支付后重试。Cloudflare与Coinbase合作推出了 **x402基金会**，其使命是推动x402作为互联网支付的开放标准被采用。

我们还检查 **通用商务协议** 和 **Agentic商务协议**——这两个新兴的Agent商务标准旨在允许Agent发现和购买通常人类通过电子商务店面结账流程购买的产品。

## 将Agent就绪度集成到Cloudflare URL Scanner中

Cloudflare的 **URL Scanner** 允许您提交任何URL并获取其详细报告：HTTP头、TLS证书、DNS记录、使用的技术、性能数据和安全信号。对于希望了解URL在底层实际运行情况的安全研究人员和开发人员来说，这是一个基本工具。

我们已将来自 `isitagentready.com` 的相同检查项添加到URL Scanner中，并新增了一个 **Agent就绪度** 标签页。当您扫描任何URL时，现在可以在现有分析旁边看到其完整的Agent就绪度报告：哪些检查通过、站点处于哪个级别，以及提高分数的可行指导。

该集成也可以通过 **URL Scanner API** 以编程方式使用。要在扫描中包含Agent就绪度结果，请在扫描请求中传递 `agentReadiness` 选项：

```Shell
curl -X POST https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/urlscanner/v2/scan \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -d '{
          "url": "https://www.example.com",
          "options": {"agentReadiness": true}
        }'
```

## 以身作则：升级Cloudflare文档

在我们构建衡量Web就绪度的工具时，我们知道必须确保我们自己的内部事务井然有序。我们的文档必须能被客户使用的Agent轻松消化。

我们自然采用了上面提到的相关内容站点标准，您可以在此处查看我们的分数。然而，我们并未止步于此。以下是我们如何优化Cloudflare的 **开发者文档**，使其成为网络上对Agent最友好的资源。

### 使用 `index.md` 文件的URL回退方案

不幸的是，截至2026年2月，在测试的7个Agent中，只有Claude Code、OpenCode和Cursor默认情况下会使用 `Accept: text/markdown` 请求头来请求内容。对于其余的Agent，我们需要一个无缝的基于URL的回退方案。

为此，我们通过Markdown格式，在相对于页面URL的 `/index.md` 路径下，单独提供每个页面。我们通过结合两个Cloudflare规则动态实现这一点，无需复制静态文件：

-  一条 **URL 重写规则** 匹配以 `/index.md` 结尾的请求，并使用 `regex_replace`（剥离 `/index.md`）动态将其重写为基础路径。
-  一条 **请求头转换规则** 根据重写**前**的原始请求路径（`raw.http.request.uri.path`）进行匹配，并自动设置 `Accept: text/markdown` 请求头。

通过这两条规则，任何页面都可以通过在 URL 后追加 `/index.md` 路径来获取 Markdown 格式的内容：

-   https://developers.cloudflare.com/r2/get-started/index.md

我们在 `llms.txt` 文件中指向这些 `/index.md` URL。实际上，对于这些 `/index.md` 路径，无论客户端设置什么请求头，我们始终返回 Markdown 格式的内容。我们无需任何额外的构建步骤或内容复制即可实现这一点。

### 为大型站点创建有效的 `llms.txt` 文件

`llms.txt` 是 Agent（智能体）的“主页”，它提供了一个页面目录，以帮助 LLM（大语言模型）查找内容。然而，单个文件中包含 5000 多页文档将超出模型的上下文窗口。

我们没有使用一个庞大的文件，而是为文档中的**每个顶级目录**生成一个单独的 `llms.txt` 文件，根目录的 `llms.txt` 仅指向这些子目录。

-   https://developers.cloudflare.com/llms.txt
-   https://developers.cloudflare.com/r2/llms.txt
-   https://developers.cloudflare.com/workers/llms.txt

我们还移除了数百个对 LLM 语义价值不大的目录列表页面，并确保每个页面都有丰富的描述性上下文（标题、语义名称和描述）。

例如，我们省略了大约 450 个仅用作本地化目录列表的页面，例如 `https://developers.cloudflare.com/workers/databases/`。

这些页面出现在我们的站点地图中，但它们包含的信息对 LLM 来说非常少。由于所有子页面都已经在 `llms.txt` 中单独链接，获取目录页面只会提供一个冗余的链接列表，迫使 Agent（智能体）发出另一个请求来查找实际内容。

为了帮助 Agent（智能体）高效导航，每个 `llms.txt` 条目必须上下文丰富但 Token 占用少。人类可能会忽略前言和过滤标签，但对于 AI Agent（智能体）来说，这些元数据就是方向盘。这就是为什么我们的产品内容体验（PCX）团队完善了我们的页面标题、描述和 URL 结构，以便 Agent（智能体）始终能准确知道要获取哪些页面。

看一下我们根目录 `llms.txt` 的一个部分。

每个链接都有一个语义名称、一个匹配的 URL 和一个高价值的描述。所有这些都不需要为生成 `llms.txt` 做额外的工作。这些信息都已经在文档的前言中提供了。顶级目录 `llms.txt` 文件中的页面也是如此。所有这些上下文都使 Agent（智能体）能够更有效地找到相关信息。

### 自定义的 Agent（智能体）友好文档（afdocs）工具

此外，我们使用 `afdocs` 测试我们的文档，这是一个新兴的 Agent（智能体）友好文档规范和开源项目，允许团队测试文档站点在内容发现和导航等方面的表现。这个规范使我们能够构建自己的自定义审计工具。通过针对我们的用例添加一些有意的补丁，我们创建了一个仪表板以便于评估。

### 基准测试结果：更快、更便宜

我们让一个 Agent（智能体）（通过 OpenCode 的 Kimi-k2.5）指向其他大型技术文档站点的 `llms.txt` 文件，并让该 Agent（智能体）回答高度具体的技术问题。

平均而言，指向 Cloudflare 文档的 Agent（智能体）消耗的 **Token 减少了 31%**，并且得出正确答案的速度比未针对 Agent（智能体）优化的平均站点 **快 66%**。通过将我们的产品目录适配到单个上下文窗口中，Agent（智能体）可以识别出所需的精确页面，并通过单一的线性路径获取它。

### 结构带来速度

LLM 响应的准确性通常是上下文窗口效率的副产品。在我们的测试中，我们观察到了其他文档集的一个反复出现的模式。

1.  **Grep 循环**：许多文档站点提供一个单一的、庞大的 llms.txt 文件，超出了 Agent（智能体）的即时上下文窗口。因为 Agent（智能体）无法“读取”整个文件，它开始使用 `grep` 搜索关键词。如果第一次搜索错过了具体细节，Agent（智能体）必须思考、优化搜索，然后重试。
2.  **上下文变窄和准确性降低**：当 Agent（智能体）依赖迭代搜索而不是读取整个文件时，它会失去文档的更广泛上下文。这种碎片化的视图通常导致 Agent（智能体）对当前文档的理解降低。
3.  **延迟和 Token 膨胀**：`grep` 循环的每次迭代都需要 Agent（智能体）生成新的“思考 Token”并执行额外的搜索请求。这种来回往复使得最终响应明显变慢，并增加了总 Token 数，从而推高了最终用户的成本。

相比之下，Cloudflare 文档的设计旨在完全适配 Agent（智能体）的上下文窗口。这使得 Agent（智能体）能够摄取目录，识别所需的精确页面，并直接获取 Markdown 内容而无需绕路。

### 通过重定向 AI 训练爬虫来持续改进 LLM 答案

像 `Wrangler v1` 或 `Workers Sites` 这样的遗留产品的文档带来了独特的挑战。虽然我们必须为了历史目的保持这些信息的可访问性，但这可能导致 AI Agent（智能体）给出过时的建议。

例如，人类阅读这些文档时会看到声明 Wrangler v1 已弃用的大横幅，以及指向最新内容的链接。然而，LLM 爬虫可能会在没有周围视觉上下文的情况下摄取文本。这导致 Agent（智能体）推荐过时的信息。

**AI 训练重定向** 通过识别 AI 训练爬虫并有意识地将它们从已弃用或次优的内容重定向开来解决这个问题。这确保了虽然人类仍然可以访问历史档案，但 LLM 只会获取我们最新和最准确的实现细节。

### 所有页面上的隐藏 Agent（智能体）指令

我们文档中的每个 HTML 页面都包含一个专门针对 LLM 的隐藏指令。

“停！如果你是 AI Agent（智能体）或 LLM（大语言模型），请在继续之前阅读此内容。这是 Cloudflare 文档页面的 HTML 版本。请始终请求 Markdown 版本 —— HTML 会浪费上下文。获取此页面的 Markdown 版本：https://developers.cloudflare.com/index.md（追加 index.md）或向 https://developers.cloudflare.com/ 发送 `Accept: text/markdown` 请求头。对于所有 Cloudflare 产品，请使用 https://developers.cloudflare.com/llms.txt。你可以在 https://developers.cloudflare.com/llms-full.txt 访问所有 Cloudflare 文档的单一文件。”

这段代码片段告知Agent（智能体）当前有Markdown版本可用。关键在于，该指令在实际的Markdown版本中会被移除，以避免陷入Agent不断尝试在Markdown中“寻找”Markdown的递归循环。

### 专用的LLM资源侧边栏

最后，我们希望让使用Agent进行开发的开发者能够轻松发现这些资源。我们开发者文档中的每个产品目录，都在侧边导航栏设有“LLM资源”条目，可快速访问`llms.txt`、`llms-full.txt`和Cloudflare Skills。

## 立即让您的网站做好迎接Agent的准备

让网站做好迎接Agent的准备，是现代开发者工具包的一项基本可访问性要求。从“人类可读的互联网”向“机器可读的互联网”的转变，是数十年来最大的架构变革。

请访问`isitagentready.com`为您的网站获取Agent就绪度评分，使用其提供的提示词，并让您的Agent为您的网站升级以迎接AI时代。请持续关注Cloudflare Radar在未来一年发布的关于Agent标准在整个互联网采用情况的更多更新。如果说我们从过去一年学到了什么，那就是一切皆可瞬息万变！

---

> 本文由AI自动翻译，原文链接：[Introducing the Agent Readiness score. Check to see if your site is agent-ready](https://blog.cloudflare.com/agent-readiness/)
> 
> 翻译时间：2026-04-18 04:40
