---
title: Browser Run：为AI智能体配备浏览器，支持实时视图与人在回路
title_original: 'Browser Run: give your agents a browser'
date: '2026-04-15'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/browser-run-for-ai-agents/
author: ''
summary: Cloudflare将“Browser Rendering”升级为Browser Run，专为AI智能体设计的浏览器解决方案。新产品允许智能体在云端运行完整浏览器会话，支持实时监控、人在回路干预、Chrome
  DevTools协议直接访问、MCP客户端集成及会话录制等功能。关键升级包括并发浏览器数量从30个提升至120个，使智能体能够更高效地浏览网页、处理表单、提取数据并在遇到障碍时请求人工协助，大幅提升了AI智能体的网络交互能力与可靠性。
categories:
- AI基础设施
tags:
- AI智能体
- 浏览器自动化
- Cloudflare
- 人在回路
- WebMCP
draft: false
translated_at: '2026-04-16T05:03:11.467791'
---

# Browser Run：为您的智能体配备浏览器

2026-04-15

- Kathy Liao

![](/images/posts/51098283d8cc.png)

AI Agent（智能体）需要与网络交互。为此，它们需要一个浏览器。它们需要浏览网站、阅读页面、填写表单、提取数据并截图。它们需要观察事情是否按预期进行，并为其人类操作员提供必要时介入的途径。而且它们需要大规模地完成所有这些工作。

今天，我们将“Browser Rendering”更名为 **Browser Run**，并发布关键功能，使其成为 **AI Agent（智能体）的浏览器**。“Browser Rendering”这个名称从未完全体现产品的功能。Browser Run 允许您在 Cloudflare 的全球网络上运行完整的浏览器会话，通过代码或 AI 驱动它们，记录和回放会话，抓取页面内容，实时调试，并在您的智能体需要帮助时让人类介入。

以下是新增功能：

*   **实时视图**：实时查看您的智能体所见及所为。即时了解运行状况，当出现问题时，准确查明原因。
*   **人在回路**：当您的智能体遇到登录页面或意外边缘情况等障碍时，它可以转交给人类处理，而不是失败。人类介入、解决问题，然后交还控制权。
*   **Chrome DevTools 协议端点**：Chrome DevTools 协议是智能体控制浏览器的方式。Browser Run 现在直接暴露此协议，因此智能体可以获得对浏览器的最大控制权，并且现有的 CDP 脚本可以在 Cloudflare 上运行。
*   **MCP 客户端支持**：像 Claude Desktop、Cursor 和 OpenCode 这样的 AI 编程智能体现在可以将 Browser Run 用作其远程浏览器。
*   **WebMCP 支持**：使用网络的智能体数量将超过人类。WebMCP 允许网站声明可供智能体发现和调用的操作，使导航更加可靠。
*   **会话录制**：为调试目的捕获每个浏览器会话。当出现问题时，您将获得包含 DOM 更改、用户交互和页面导航的完整录制。
*   **更高限制**：同时运行更多任务，并发浏览器数量从 30 个增加到 120 个。

**实时视图**：实时查看您的智能体所见及所为。即时了解运行状况，当出现问题时，准确查明原因。

**人在回路**：当您的智能体遇到登录页面或意外边缘情况等障碍时，它可以转交给人类处理，而不是失败。人类介入、解决问题，然后交还控制权。

**Chrome DevTools 协议端点**：Chrome DevTools 协议是智能体控制浏览器的方式。Browser Run 现在直接暴露此协议，因此智能体可以获得对浏览器的最大控制权，并且现有的 CDP 脚本可以在 Cloudflare 上运行。

**MCP 客户端支持**：像 Claude Desktop、Cursor 和 OpenCode 这样的 AI 编程智能体现在可以将 Browser Run 用作其远程浏览器。

**WebMCP 支持**：使用网络的智能体数量将超过人类。WebMCP 允许网站声明可供智能体发现和调用的操作，使导航更加可靠。

**会话录制**：为调试目的捕获每个浏览器会话。当出现问题时，您将获得包含 DOM 更改、用户交互和页面导航的完整录制。

**更高限制**：同时运行更多任务，并发浏览器数量从 30 个增加到 120 个。

一个 AI Agent（智能体）在亚马逊上搜索橙色熔岩灯，比较选项，并在需要登录完成购买时转交给人类处理

## 智能体所需的一切

让我们思考一下智能体在浏览网络时需要什么，以及每个功能如何满足这些需求：

## 1) 打开浏览器

首先，智能体需要一个浏览器。通过 Browser Run，智能体可以按需在 Cloudflare 的全球网络上启动一个无头 Chrome 实例。无需管理基础设施，无需维护 Chrome 版本。浏览器会话在靠近用户的地方打开以实现低延迟，并根据需要扩展。将 Browser Run 与 **Agents SDK** 结合使用，以构建能够浏览网络、记住一切并自主行动的长期运行智能体。

## 2) 执行操作

一旦您的智能体有了浏览器，它就需要控制它的方法。Browser Run 支持多种方法：除了现有的使用 **Puppeteer** 和 **Playwright** 的高级自动化以及用于简单任务的 **快速操作** 之外，现在还支持通过 Chrome DevTools 协议和 WebMCP 进行新的低级协议访问。让我们看看细节。

### Chrome DevTools 协议端点

**Chrome DevTools 协议** 是驱动浏览器自动化的底层协议。直接暴露 CDP 意味着不断增长的智能体工具生态系统和现有的 CDP 自动化脚本可以使用 Browser Run。当您打开 Chrome DevTools 并检查页面时，底层运行的就是 CDP。Puppeteer、Playwright 和大多数智能体框架都构建在它之上。

您使用 Browser Run 的每种方式实际上都已经通过 CDP 了。新变化在于我们现在**直接暴露 CDP 作为一个端点**。这对智能体很重要，因为 CDP 赋予智能体对浏览器最大程度的控制。智能体框架本身原生支持 CDP，现在可以直接连接到 Browser Run。CDP 还解锁了通过 Puppeteer 或 Playwright 无法使用的浏览器操作，例如 JavaScript 调试。而且，因为您处理的是原始的 CDP 消息，而不是通过高级库，所以您可以直接将消息传递给模型，以实现更节省 Token 的浏览器控制。

如果您已经有针对自托管 Chrome 运行的 CDP 自动化脚本，只需更改一行配置即可在 Browser Run 上运行。将您的 WebSocket URL 指向 Browser Run，并停止管理您自己的浏览器基础设施。

```javascript
// 之前：连接到自托管 Chrome
const browser = await puppeteer.connect({
  browserWSEndpoint: 'ws://localhost:9222/devtools/browser'
});

// 之后：连接到 Browser Run
const browser = await puppeteer.connect({
  browserWSEndpoint: 'wss://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/browser-rendering/devtools/browser',
  headers: { 'Authorization': 'Bearer <API_TOKEN>' }
});

```

CDP 端点也使 Browser Run 更易于访问。您现在可以从任何语言、任何环境连接，而无需编写 **Cloudflare Worker**。（如果您已经在使用 Workers，则无需更改。）

#### 将 Browser Run 与 MCP 客户端一起使用

既然 Browser Run 暴露了 Chrome DevTools 协议，包括 Claude Desktop、Cursor、Codex 和 OpenCode 在内的 MCP 客户端就可以将 Browser Run 用作其远程浏览器。来自 Chrome DevTools 团队的 **chrome-devtools-mcp 包** 是一个 MCP 服务器，它让您的 AI 编程助手能够访问 Chrome DevTools 的全部功能，以实现可靠的自动化、深度调试和性能分析。

以下是如何为 Claude Desktop 配置 Browser Run 的示例：

```javascript
{
  "mcpServers": {
    "browser-rendering": {
      "command": "npx",
      "args": [
        "-y",
        "chrome-devtools-mcp@latest",
        "--wsEndpoint=wss://api.cloudflare.com/client/v4/accounts/<ACCOUNT_ID>/browser-rendering/devtools/browser?keep_alive=600000",
        "--wsHeaders={\"Authorization\":\"Bearer <API_TOKEN>\"}"
      ]
    }
  }
}

```

对于其他 MCP 客户端，请参阅**将 Browser Run 与 MCP 客户端一起使用的文档**。

### WebMCP 支持

互联网是为人类构建的，因此如今作为 AI Agent（智能体）进行导航并不可靠。我们押注于一个未来，届时使用网络的智能体数量将超过人类。在那个世界里，网站需要对智能体友好。

这就是我们推出对 **WebMCP** 支持的原因，这是 Google Chrome 团队在 Chromium 146+ 中引入的新浏览器 API。WebMCP 允许网站直接将工具暴露给 AI Agent（智能体），声明每个页面上可供智能体发现和调用的操作。这有助于智能体更可靠地浏览网络。网站可以暴露其工具供智能体发现和调用，而不是让智能体需要自己摸索如何使用网站。

两个 API 实现了这一功能：

*   `navigator.modelContext` 允许网站注册其工具
*   `navigator.modelContextTesting` 允许智能体发现并执行这些工具

`navigator.modelContext` 允许网站注册其工具

`navigator.modelContextTesting` 允许智能体发现并执行这些工具

如今，一个访问旅游预订网站的智能体需要通过观察来理解用户界面。借助 WebMCP，网站可以声明“这是一个 `search_flights` 工具，需要输入出发地、目的地和日期。” 智能体可以直接调用它，而无需经历缓慢的截图-分析-点击循环。这使得导航更加可靠，不受用户界面潜在变化的影响。

工具是在页面上动态发现的，而非预先加载。这对于长尾网站至关重要，因为为每个可能的网站预加载一个 MCP 服务器是不可行的，并且会膨胀上下文窗口。

通过 Chrome DevTools 控制台使用 WebMCP 预订酒店，并使用 `listTools()` 发现可用工具

我们有一个实验池，其中运行着 Chrome Beta 版本的浏览器实例，您可以在新功能进入稳定版 Chrome 之前进行测试。我们还刚刚发布了 `Wrangler browser commands`，让您可以直接从 CLI 管理浏览器会话，从而在终端中直接创建、管理和查看浏览器会话。要访问启用了 WebMCP 的浏览器，请使用以下 Wrangler 命令在实验池中创建一个会话：

```javascript
npm i -g wrangler@latest
wrangler browser create --lab --keepAlive 300  

```

### 使用 Browser Run 的现有方式

虽然 CDP 和 WebMCP 是新的，但您已经可以通过 Browser Run 使用 `Puppeteer`、`Playwright` 或 `Stagehand` 进行完整的浏览器自动化。对于简单的任务，如 `capturing screenshots`、`generating PDFs` 和 `extracting markdown`，则有 `Quick Action endpoints`。

#### /crawl 端点 —— 爬取网页内容

我们最近还推出了一个 `/crawl endpoint`，允许您通过一次 API 调用爬取整个网站。提供一个起始 URL，页面就会被自动发现和抓取，然后以您首选的格式（HTML、Markdown 和结构化 JSON）返回，并带有额外的参数来控制爬取深度和范围、跳过未更改的页面以及指定要包含或排除的特定路径。

我们特意将 /crawl 构建为一个 `well-behaved crawler`。这意味着它开箱即用地尊重网站所有者的偏好，是一个 `signed agent`，具有使用 `Web Bot Auth` 进行加密签名的独特机器人 ID，使用不可定制的 `User-Agent`，并遵循 robots.txt 和 `AI Crawl Control`。它不会绕过 Cloudflare 的机器人防护或验证码。网站所有者可以选择其内容是否可访问，而 /crawl 会尊重这一选择。

```javascript
# Initiate a crawl
curl -X POST 'https://api.cloudflare.com/client/v4/accounts/{account_id}/browser-rendering/crawl' \
  -H 'Authorization: Bearer <apiToken>' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://blog.cloudflare.com/"
  }'

```

## 3) 观察

事情并不总是一开始就顺利。我们不断听到客户反馈，当他们的自动化失败时，他们不知道原因。这就是为什么我们增加了多种方式来观察正在发生的事情，以便您可以实时或事后准确地看到您的智能体所看到的内容。

### 实时视图

`Live View` 让您可以实时观看智能体的浏览器会话。无论您是在调试智能体还是运行一个长的自动化脚本，您都可以实时看到正在发生的一切。这包括页面本身，以及 DOM、控制台和网络请求。当出现问题时——预期的按钮不存在、页面需要身份验证或出现验证码——您可以立即发现。

有两种方式可以访问实时视图。从代码中，获取您想要检查的浏览器的 `session_id`，并在 Chrome 中打开响应中的 `devtoolsFrontendURL`。或者，从 Cloudflare 仪表板中，打开 Browser Run 部分的新“实时会话”标签页，并点击进入任何活动会话。

一个 AI 智能体预订酒店的实时视图，显示实时浏览器活动

### 会话录制

实时视图在您有空时很好用，但您不可能观看每个会话。`Session Recordings` 将 DOM 更改、鼠标和键盘事件以及页面导航捕获为结构化 JSON，以便您可以在会话结束后重放任何会话。

通过在启动浏览器时传递 `recording:true` 来启用会话录制。会话关闭后，您可以从 Cloudflare 仪表板的“运行”标签页访问录制内容，或通过 API 检索录制内容，并使用 `rrweb-player` 进行重放。接下来，我们将增加在录制过程中任何时间点检查 DOM 状态和控制台输出的能力。

一个浏览器自动化浏览 Sentry Shop 并将一件飞行员夹克添加到购物车的会话录制回放

### 仪表板重新设计

此前，`Browser Run dashboard` 仅显示浏览器会话的日志。截图、PDF、Markdown 和爬取的请求是不可见的。重新设计的仪表板改变了这一点。新的“运行”标签页显示每个请求。您可以按端点筛选，并查看详细信息，包括目标 URL、状态和持续时间。

Browser Run 仪表板的“运行”标签页，在一个视图中显示浏览器会话和快速操作（如 PDF、截图和爬取），并展开了一个爬取任务以显示其进度

## 4) 干预

智能体很好，但它们并不完美。有时它们需要人类介入。Browser Run 支持“人在回路”工作流，人类可以接管实时浏览器会话，处理自动化无法处理的事情，然后让会话继续。

### 人在回路

当自动化遇到障碍时，您不必重新开始。借助 `Human in the Loop`，您可以介入并直接与页面交互，进行点击、输入、导航、输入凭据或提交表单。这解锁了智能体无法处理的工作流。

目前，您可以通过打开任何活动会话的实时视图 URL 来介入。接下来，我们将增加一个交接流程，智能体可以发出需要帮助的信号，通知人类介入，然后在问题解决后将控制权交还给智能体。

## 5) 扩展

客户要求我们提高限制，以便他们能更快地做更多事情。

### 更高的限制

我们已经将 `default concurrent browser limit` 从 30 个增加到 120 个，提高了四倍。每个会话都可以让您从全球预热实例池中即时访问一个浏览器，因此无需等待浏览器冷启动。三月份，我们还 `increased limits for Quick Actions` 到每秒 10 个请求。如果您需要更高的限制，可以通过申请获得。

## 下一步计划

- **人在回路交接**：目前您可以通过实时视图介入浏览器会话。很快，智能体将能够在需要帮助时发出信号，以便您可以构建通知来提醒人类介入。
- **会话录制检查**：您已经可以浏览时间线并重放任何会话。很快，您还将能够检查 DOM 状态和控制台输出。
- **跟踪和浏览器日志**：无需修改代码即可访问调试信息。包括控制台日志、网络请求、计时数据。如果出现问题，您将知道问题所在。
- **直接从 Workers 进行截图、生成 PDF 和 Markdown**：通过 `REST API` 可用的相同简单任务即将来到 `Workers Bindings`。`env.BROWSER.screenshot()` 可以直接使用，无需 API 令牌。

## 开始使用

Browser Run 现已面向 Workers Free 和 Workers Paid 计划用户开放。我们今天发布的所有功能——实时视图、人工介入、会话录制以及更高的并发限制——均已就绪可用。

如果您此前已在使用 Browser Rendering，所有功能均保持不变，仅名称更新并增加了更多特性。

请查阅文档以开始使用。

---

> 本文由AI自动翻译，原文链接：[Browser Run: give your agents a browser](https://blog.cloudflare.com/browser-run-for-ai-agents/)
> 
> 翻译时间：2026-04-16 05:03
