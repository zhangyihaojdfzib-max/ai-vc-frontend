---
title: eve：为Agent构建而生的开源框架
title_original: Introducing eve
date: '2026-06-17'
source: Vercel Blog
source_url: https://vercel.com/blog/introducing-eve
author: ''
summary: Vercel推出开源Agent框架eve，旨在简化Agent的构建、运行和扩展。eve内置了持久化执行、沙箱化计算、人工审批、子Agent和评估等生产环境所需功能，让开发者只需定义Agent的能力，而无需重复搭建底层基础设施。文章类比了Next.js对Web开发的变革，认为eve将终结Agent开发中各自为政的混乱局面，推动Agent开发进入标准化时代。
categories:
- AI基础设施
tags:
- eve
- Agent框架
- 开源
- Vercel
- AI基础设施
draft: false
translated_at: '2026-06-18T06:55:04.873967'
---

今天，我们自豪地推出 **eve**，一个用于构建、运行和扩展 Agent 的开源 Agent 框架。eve 的设计理念是：构建一个 Agent 应该意味着定义它能做什么，而无需拼凑它在生产环境中运行所需的所有组件。相反，eve 已经内置了生产环境所需的一切：

- 持久化执行
- 沙箱化计算
- 人工审批
- 子 Agent
- 评估
- 以及更多

持久化执行

沙箱化计算

人工审批

子 Agent

评估

以及更多

eve 是我们自己构建和运行 Agent 所使用的框架。

如今的 Agent 正处于框架出现之前的 Web 时代，每个人都在手动重复搭建相同的底层基础设施，而这些工作无法复用到下一个项目。Next.js 终结了 Web 时代的这种局面，而 eve 正在为 Agent 做同样的事情。

## 链接到标题Agent 即目录

这是一个 eve Agent。

```
agent/
  agent.ts                   # 它运行的模型
  instructions.md            # 它是谁
  tools/
    run_sql.ts               # 它能做什么
    post_chart.ts
  skills/
    revenue-definitions.md   # 它知道什么
  subagents/
    investigator/            # 它委托给谁
  channels/
    slack.ts                 # 它在哪里运行
  schedules/
    monday-summary.ts        # 它何时自主行动
```

一个一目了然的数据分析师 Agent

每个文件描述了 Agent 的一个组件，因此，一眼望去，目录结构就能告诉你一个 Agent 是什么、做什么、在哪里运行以及何时自主行动。

### 链接到标题在几分钟内创建一个 eve Agent

每个 Agent 都从其定义开始。

```
1import { defineAgent } from "eve";
2
3export default defineAgent({
4  model: "anthropic/claude-opus-4.8",
5});
```

在一个文件中配置 Agent 及其模型

`agent.ts` 文件是你配置 Agent 本身的地方。你可以用一行代码定义模型，通过 AI Gateway 支持提供商回退，并且当你需要时，还可以使用压缩、模型选项和其他可选字段。

为你的 Agent 分配工作和个性，只需创建一个 `instructions.md` 文件，它作为系统提示词，eve 会在每次模型调用前将其前置。

```
你是一位资深数据分析师。你回答关于团队数据的问题。
- 优先使用精确数字，而非含糊其辞。如果可以计算，就计算出来。
- 说明你报告的任何数字背后的假设（日期范围、筛选条件、粒度）。
- 使用你可用的工具，而不是猜测。如果你无法从数据中回答，请直说。
```

Agent 的身份和固定规则，每次模型调用前都会前置

为你 Agent 的功能创建文件，比如用于工具和技能的 `post_chart.ts` 和 `revenue-definitions.md`，eve 会将它们连接成一个可工作的 Agent，无需任何样板代码或基础设施管理。你可以专注于 Agent 做什么，而不是它如何做。

## 链接到标题我们为什么构建 eve

我们在 Vercel 已经构建 Agent 多年，其中包括 v0。但是，一旦编码 Agent 使得构建一个 Agent 成为任何人都能做的事情，那么每个人都会去做。我们交付了数百个 Agent 和内部应用，这看起来像是一场生产力革命。

但在其背后，每个团队都在他们的 Agent 能做任何事情之前，反复构建和重建相同的底层基础设施，而这些工作无法从一个用例复用到下一个。每个 Agent 都是为不同的任务设计的，但它们都有相同的需求，并且相同的结构不断涌现以满足这些需求。Agent 有其固有的形态。

eve 就是将这种形态变成了一个框架。每一代软件，当足够多的人以艰难的方式构建了相同的东西后，都会迎来其抽象层，而 Agent 现在正处于这个阶段。

## 链接到标题开箱即用

Agent 在生产环境中所需的一切都随框架一起提供。

### 链接到标题每次对话的持久化会话

Agent 需要等待人类、调用慢速系统，并运行数小时、数天或数周。在 eve 中，每次对话都是一个持久化的工作流，每一步都有检查点，因此会话可以暂停，在崩溃或部署后幸存，并从中断处精确恢复。这种持久性建立在开源 Workflow SDK 之上。

### 链接到标题每个 Agent 的沙箱

你的 Agent 编写的代码应被视为不受信任的，因此 eve 将 Agent 生成的代码完全排除在你的应用运行时之外。每个 Agent 都有自己的沙箱，这是一个用于 shell 命令、脚本以及文件读写的隔离环境，在与控制 Agent 的框架不同的安全上下文中运行。这个沙箱的后端是一个适配器。部署时，它在 Vercel Sandbox 上运行。本地运行时，它在 Docker、microsandbox 或 just-bash 上运行，并且你可以为任何其他提供商编写适配器。

### 链接到标题人工审批

Agent 在真实系统上操作，其中一些操作应该需要人工批准。eve 中的任何操作都可以配置为需要审批，Agent 将在此处暂停并等待，如果需要，可以无限期等待，而不消耗任何计算资源。一旦获得批准，eve 会从中断处继续执行任务。

### 链接到标题与工具、数据和服务的安全连接

Agent 需要连接到你的后端、数据和其他第三方服务。在 eve 中，一个连接就是一个指向 MCP 服务器或任何具有兼容 OpenAPI 文档的 API 的文件。

```
1import { defineMcpClientConnection } from "eve/connections";
2
3export default defineMcpClientConnection({
4  url: "https://mcp.linear.app/sse",
5  description: "Linear 工作空间：问题、项目、周期和评论。",
6  auth: {
7    getToken: async () => ({ token: process.env.LINEAR_API_TOKEN! }),
8  },
9});
```

一个文件即可完成与 MCP 服务器的连接

eve 发现远程工具，将它们交给模型，并代理认证，而模型永远不会看到连接的 URL 或凭据。Vercel Connect 处理交互式 OAuth，内置同意和令牌刷新功能。发布时，eve Agent 可以连接到 Slack、GitHub、Snowflake、Salesforce、Notion 和 Linear，以及任何你可以通过 OAuth、API 密钥或 MCP 服务器访问的其他服务。

![连接到你已经使用的工具。](/images/posts/2f7693e2c006.jpg)

![连接到你已经使用的工具。](/images/posts/5e8f5d8a71ee.jpg)

![连接到你已经使用的工具。](/images/posts/0aebb60a337e.jpg)

![连接到你已经使用的工具。](/images/posts/9eef693aee58.jpg)

### 链接到标题同一个 Agent，所有渠道

大多数 Agent 只存在于一个地方，因为每一个新的交互界面都需要构建一个独立的集成。在 eve 中，同一个 Agent 服务于所有交互界面，每个渠道只是一个小的适配器文件。HTTP API 默认开启，并包含 Slack、Discord、Teams、Telegram、Twilio、GitHub 和 Linear，`defineChannel` 则覆盖自定义渠道。一个渠道也可以将任务移交给另一个渠道，因此一个事件 webhook 可以在 Slack 中打开一个调查线程。

### 链接到标题内置追踪和评估

当 Agent 出错时，首先要问的是 Agent 实际做了什么。在 eve 中，每次运行都会产生一个追踪。每个模型调用和工具调用都按顺序出现，并带有其输入和输出，一直到 Agent 在其沙箱中运行的命令，因此你可以重放运行过程，而不是从日志中拼凑信息。

```
ai.eve.turn                      # 每次交互一个跨度
├── ai.streamText                # 模型调用
│   └── ai.streamText.doStream
└── ai.toolCall                  # run_sql，包含输入和输出
```

单次交互产生的 OpenTelemetry 跨度树

这些跨度是标准的 OpenTelemetry，可以导出到你已运行的任何追踪服务，无论是 Braintrust、Honeycomb、Datadog 还是 Jaeger。在 Vercel 上，它们会显示在可观测性下的 Agent 运行选项卡中，为你提供一个地方来监控每个会话并深入分析任何一次运行。评估让你更进一步，提供带评分的测试套件，你可以在本地运行或集成到 CI 中。

![一个会话追踪，其中一个交互已展开，显示其工具调用和待处理的审批](/images/posts/c64560d742e2.jpg)

![一个会话追踪记录，其中一轮对话已展开显示其工具调用和待审批状态](/images/posts/5e72cc56d23b.jpg)

这就剩下任何框架都无法为你编写的部分：你的Agent（智能体）实际做什么。

## 链接到标题逐个文件扩展Agent（智能体）

赋予Agent（智能体）能力最常见的方式是给它提供工具，并教会它如何通过技能来做事。如今，这意味着要构建工具、编写技能，然后将两者接入到驱动Agent（智能体）循环的任何程序中。使用eve，一个工具就是一个TypeScript文件，一项技能就是一个markdown文件。

```
1import { defineTool } from "eve/tools";2import { z } from "zod";3import { runReadOnlySql } from "../lib/sample-db";4
5export default defineTool({6  description: "对orders和customers表执行只读SQL查询。",7  inputSchema: z.object({8    sql: z.string().describe("单个只读SELECT语句。"),9  }),10  async execute({ sql }) {11    const { columns, rows } = await runReadOnlySql(sql);12    return { columns, rows: rows.slice(0, 500), truncated: rows.length > 500 };13  },14});
```

一个文件中的类型化工具，文件名即工具名

```
---description: 该团队定义收入的方式。在回答任何收入问题前加载。---
收入按订阅期限确认，扣除退款。周数以周一为锚点，采用UTC时间。从所有数字中排除试用账户和内部账户。
```

一个markdown文件中的技能，仅在相关话题出现时加载

注意缺失的部分。你无需编写所有样板代码来将这些内容接入并注册到你的Agent（智能体），eve会为你处理。

文件在目录树中的名称和位置就是其定义。eve在构建时拾取工具和技能，将它们的描述提供给模型，模型便据此执行。就像Next.js通过拥有路由功能将文件夹转化为路由一样，eve通过拥有Agent（智能体）循环将文件转化为一种能力。

### 链接到标题添加人工审批环节

要求对某个操作进行审批只是工具上的一个字段。

```
1export default defineTool({2  description: "对数据仓库执行只读SQL查询。",3  inputSchema: z.object({ sql: z.string() }),4  needsApproval: ({ toolInput }) => estimateScanGb(toolInput.sql) > 50,5  async execute({ sql }) {6    7  },8});
```

当查询预计扫描超过50GB时要求审批

现在，你可以保护那些昂贵的查询、破坏性写入，或任何你不希望在无人监督下运行的操作。

### 链接到标题让Agent（智能体）自己编写代码

你定义的工具并非能力的上限。eve为你的Agent（智能体）提供了一个带有Shell的真实计算机，因此它可以运行bash、grep以及你在终端中运行的任何其他命令。当某项任务需要尚不存在的代码时，Agent（智能体）会编写并运行它。

```
> 按地区细分上周收入并绘制图表
⦿ write_file analysis/by_region.py⦿ bash  python analysis/by_region.py
6月1日当周按地区划分的收入。AMER 210万美元，EMEA 160万美元，APAC 50万美元。图表已保存至 analysis/by_region.png。
```

Agent（智能体）在其自己的沙箱中编写并运行代码

你的Agent（智能体）可以在安全的沙箱中自主解决问题，重塑数据集、运行一次性分析，或编写任何任务所需但现有工具无法覆盖的代码。

### 链接到标题将工作委派给子Agent（智能体）

eve Agent（智能体）也可以进行委派。子Agent（智能体）是下一级的相同结构，即subagents/目录下的一个子目录，包含其自身的指令、工具和沙箱。父Agent（智能体）调用它就像调用一个工具一样。

```
1import { defineAgent } from "eve";2
3export default defineAgent({4  description: "在分析师报告之前调查数据中的异常情况。",5  model: "anthropic/claude-opus-4.8",6});
```

分析师可以委派工作的子Agent（智能体）

子Agent（智能体）从一个干净的上下文窗口开始，只拥有你赋予它的工具，完成工作后将结果返回给父Agent（智能体）。

## 链接到标题启动并与你的Agent（智能体）交互

现在到了每个开发者都期待的环节：测试他们的Agent（智能体）。过去，这意味着启动进程、提问、然后阅读日志，无法直观地看到使用了哪些工具、模型加载了什么内容，或者它为何以某种方式回答。你希望与你的Agent（智能体）对话并观察其工作，而你得到的却只是标准输出。使用eve，开发循环只需一个命令。

### 链接到标题在本地运行Agent（智能体）

要启动一个eve Agent（智能体），你需要运行其开发服务器。

在本地启动Agent（智能体），通过终端UI与之对话

```
> 上周收入是多少？
⦿ load_skill revenue-definitions⦿ run_sql  SELECT date_trunc('week', created_at) ...
6月1日当周收入为420万美元（扣除退款后），较前一周增长6%。
```

运行的每一步，都实时可见

Agent（智能体）所做的每一件事都在TUI中可见。Agent（智能体）加载了技能，执行了查询，按照团队规则进行了回答，而每一行都是持久会话中的一个检查点步骤。终端UI只是一个客户端，Agent（智能体）通过HTTP提供相同的结构化事件，因此curl、测试脚本或CI都可以驱动它并精确检查其行为。

### 链接到标题使用评估测试Agent（智能体）

与Agent（智能体）对话一次只能验证一次运行。评估测试你的Agent（智能体）就像测试你软件的其他部分一样，使用写在文件中的评分检查，就像项目中的其他所有文件一样。

```
1import { defineEval } from "eve/evals";2import { includes } from "eve/evals/expect";3
4export default defineEval({5  description: "分析师按照团队规则回答收入问题。",6  async test(t) {7    await t.send("上周收入是多少？");8    t.completed();9    t.calledTool("run_sql");10    t.check(t.reply, includes("扣除退款后"));11  },12});
```

一个检查分析师是否使用了其工具并遵循了团队定义的测试套件

你可以在本地运行eve eval，或者将其指向一个已部署的应用，这样提示词的更改或模型的切换就能在用户发现问题之前，向你展示它破坏了哪些功能。

## 链接到标题发布上线

Agent（智能体）在你的笔记本电脑上待得够久了。发布上线通常是Agent（智能体）工作结束、基础设施工作开始的步骤。使用eve，无需配置任何基础设施，因为Agent（智能体）就是一个普通的Vercel项目，它像任何其他前端或后端一样进行部署。

```
vercel deploy
```

部署Agent（智能体）

部署时，你的Agent（智能体）没有任何改变，因为eve从设计之初就考虑了适配器。发布时，eve部署到Vercel，并计划支持其他平台。相同的目录在生产环境中的运行方式与在笔记本电脑上完全相同。沙箱无需更改代码即可切换到Vercel Sandbox，你在开发环境中与之对话的Agent（智能体）现在可以通过公共URL访问。部署甚至不会中断Agent（智能体）；当你推送时，正在执行任务的会话会在其启动的版本上完成。

所有这些都不需要仪表板步骤。构建你Agent（智能体）的同一个编码Agent（智能体）可以发布它并验证其工作。

但部署并不意味着完成。在生产环境中，Agent（智能体）需要按自己的计划与用户会面并完成工作。

## 链接到标题将Agent（智能体）介绍给你的团队

过去，让Agent（智能体）接入Slack意味着首先要构建一个Slack应用，包括应用配置、机器人Token、事件订阅、Webhook端点和签名密钥，所有这些都在Agent（智能体）说一句话之前完成。使用eve，一个频道只需一个命令。

```
eve channels add slack
```

搭建Slack频道文件

该命令会写入channels/slack.ts，这是一个像任何其他代码更改一样发布的单个文件，而你刚刚部署的Agent（智能体）现在就可以在Slack中回答了。平台功能随频道一起提供，因此审批呈现为Slack按钮，问题呈现为选择菜单，Agent（智能体）在工作时会显示输入状态指示器。通过Vercel Connect路由凭据，无需将机器人Token复制到.env文件中。再次运行该命令并指定discord或teams，同一个Agent（智能体）也会出现在那里，每个频道对应一个文件。

频道是Agent（智能体）的用户界面，会话在它们之间流转。在Slack中提出的问题可以在网页上继续，而通过HTTP到达的事件Webhook可以在Slack中开启一个调查线程，并在团队所在的平台上完成工作。

### 链接到标题让Agent（智能体）按计划运行

周一的营收报告不应等待有人来询问。一个计划就是另一个文件，包含一个cron表达式和一个处理器，让Agent（智能体）按自己的时钟启动。

```
1import { defineSchedule } from "eve/schedules";2import slack from "../channels/slack.js";3
4export default defineSchedule({5  cron: "0 9 * * 1",6  async run({ receive, waitUntil, appAuth }) {7    waitUntil(8      receive(slack, {9        message: "总结上周营收并发布到团队频道。",10        target: { channelId: "C0123ABC" },11        auth: appAuth,12      }),13    );14  },15});
```

通过Slack频道按cron计划发布周一营收报告

在Vercel上，每个计划都会部署为一个Vercel Cron Job，因此报告每周一自动发布，无需任何人记住去执行。

## 链接到标题像运行其他软件一样运行Agent（智能体）

团队依赖的Agent（智能体）是生产级软件，对其指令的更改可能像代码更改一样导致故障。由于eve Agent（智能体）是目录中的文件，它像其他代码一样存在于Git中，一个新的提示词、工具或技能就是一个带有差异、审查和历史的提交。

将`eve eval`接入CI，你编写的测试套件就成为部署门禁，对每个提交进行评分，从而让回归问题在CI中而非生产环境中被拦截。

每个提交还会获得自己的预览部署，并携带其Agent（智能体）的频道。团队可以在新版本替换日常使用的Slack机器人之前，先与它进行交互。

当某个变更以任何评估未能捕获的方式出现问题时，你可以立即将生产环境回滚到之前的版本。

## 链接到标题我们如何在Vercel上运行eve

我们在Vercel的生产环境中运行着超过一百个Agent（智能体），它们已成为公司日常运营的一部分，每个都在业务中扮演一个角色。以下是其中几个。

### 链接到标题数据分析师

Vercel内部使用最多的工具是一个Agent（智能体），每月处理超过30,000个问题。任何人都可以在Slack中向`d0`提问，并从数据仓库获得答案。每个查询都限定在提问者自身的权限范围内，因此`d0`永远不会向你展示你原本无法查看的数据表。

### 链接到标题自主销售开发代表

Lead Agent全天候运行着我们最佳销售代表的行动手册。它会在每个新线索出现时立即处理并自主跟进，确保没有线索过夜后变冷。它每年运行成本约5,000美元，回报是其32倍，并且由一名工程师兼职维护。

### 链接到标题销售驾驶舱

RevOps团队在没有工程师参与的情况下，六周内构建了Athena。它能用自然语言回答来自Snowflake和Salesforce的管道和预测问题，上线后管道覆盖率几乎翻了一番。

### 链接到标题支持工程师

Vertex是我们的支持Agent（智能体），全天候处理来自帮助中心、文档和Slack的工单，确保无论用户何时提问都能获得快速响应。它读取工单，找到正确答案并回复，自主解决92%的工单，其余升级到支持团队，以便他们专注于最需要关注的问题。

### 链接到标题内容Agent（智能体）

在Vercel，不仅内容团队，任何人都可以写作。`draft0`运行一个完整的审校流程，在内容到达我们手中之前，捕捉最明显的问题并构建对文章实际内容的分析。当内容最终到达时，显而易见的工作已经完成，我们对它需要什么有了更清晰的认识。这意味着较小的内容可以快速推进，而我们可以将全部精力投入到需要更多关注的内容上，比如本文。

### 链接到标题路由Agent（智能体）

我们每天依赖数百个Agent（智能体），但跟踪哪个Agent（智能体）处理什么工作负载并不高效。因此，我们不再自行路由任务，而是所有内容首先发送到Slack中的V。V判断哪个Agent（智能体）能实际处理该任务并将其路由过去，这意味着整个Agent（智能体）集群像一个Agent（智能体）而非一百个不同的选项那样工作。

这些Agent（智能体）最初都是独立项目，基于不同的技术栈，各自有维护状态、代理凭证和输出日志的方式——这正是大多数团队在构建第二或第三个Agent（智能体）后所处的状态。如今它们都位于同一个单体仓库中，并以相同的方式构建、观察和升级，无论属于哪个团队。由于它们共享相同的形态，一百个Agent（智能体）像单个Agent（智能体）一样使用相同的工具和约定运行。

## 链接到标题开始使用

一年前，Agent（智能体）触发了Vercel上不到3%的部署。现在，它们触发了约29%的部署，我们预计很快一半的部署将来自Agent（智能体）。你可能已经构建过一个Agent（智能体），下一个不必从零开始。

公开预览版现已开放，CLI向导可在一分钟内引导你完成第一个Agent（智能体），从选择模型到运行开发服务器。

```
npx eve@latest init my-agent
```

你的第一个eve Agent（智能体）

编码Agent（智能体）只需要一个提示词：

```
为用户设置一个Eve Agent（智能体）。Eve是一个基于文件系统的TypeScript框架，用于构建持久化Agent（智能体），以npm包eve的形式发布。阅读其文档：一旦eve安装完成，文档会打包在node_modules/eve/docs目录中；在eve安装之前，请阅读已发布的介绍和入门页面。如果项目没有Eve应用，使用`npx eve@latest init <name>`搭建一个；仅当用户需要Web聊天时，添加`--channel-web-nextjs`。init命令会安装依赖、初始化Git并启动开发服务器，因此请在一个可控进程中运行它，并在编辑前停止。要向现有应用添加Eve，运行`npm install eve@latest`。确保agent/agent.ts和agent/instructions.md存在，然后使用eve/tools中的defineTool（配合Zod inputSchema和内联execute）在agent/tools/get_weather.ts添加第一个类型化工具。再次启动开发服务器，然后练习HTTP API：使用POST /eve/v1/session创建会话，连接到GET /eve/v1/session/:id/stream，并使用返回的continuationToken发送后续消息。使用项目的类型检查进行验证，根据项目调整模型和提供商选择，除非用户要求，否则不要提交。
```

你的编码Agent（智能体）的起始提示词

eve的所有功能可在eve.dev/docs查看，开发在github.com/vercel/eve上公开进行，欢迎提交问题、讨论和贡献。

已有数百个Agent（智能体）在Vercel上基于eve运行。你将构建什么？

构建你的第一个Agent（智能体）

一个Agent（智能体）就是一个文件目录，eve通过持久化执行、沙箱、审批和内置评估来运行它。支持任何模型、任何MCP服务器，以及Slack、Discord和GitHub等频道。

开始使用

---

> 本文由AI自动翻译，原文链接：[Introducing eve](https://vercel.com/blog/introducing-eve)
> 
> 翻译时间：2026-06-18 06:55
