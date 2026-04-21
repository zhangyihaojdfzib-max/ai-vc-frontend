---
title: Cloudflare内部AI工程栈：基于自有平台构建与规模化实践
title_original: "The AI engineering stack we built internally â\x80\x94 on the platform\
  \ we ship"
date: '2026-04-20'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/internal-ai-engineering-stack/
author: ''
summary: 本文介绍了Cloudflare在过去11个月中，基于其自有产品（如AI Gateway、Workers AI等）构建的内部AI工程栈。该栈已覆盖公司93%的研发人员，显著提升了开发效率与合并请求数量。文章从平台层（身份验证、路由、推理）、知识层（系统理解）和执行层（大规模质量保障）三个部分，详细阐述了其架构设计、技术选型与实施成果，展示了如何将AI深度集成到工程工作流中并实现规模化应用。
categories:
- AI基础设施
tags:
- AI工程栈
- Cloudflare
- MCP
- AI Gateway
- 内部工具
draft: false
translated_at: '2026-04-21T05:12:54.864297'
---

# 我们在自有平台上构建的内部AI工程栈

2026-04-20

- Ayush Thakur
- Scott Roe-Meschke
- Rajesh Bhatia

![](/images/posts/18e7b35ac429.png)

在过去30天里，Cloudflare研发部门93%的员工使用了基于我们自有平台基础设施构建的AI编程工具。

十一个月前，我们启动了一个重大项目：将AI真正集成到我们的工程栈中。我们需要构建内部MCP服务器、访问层以及使Agent（智能体）在Cloudflare发挥效用所必需的AI工具。我们召集了公司各团队的工程师，组建了一个名为iMARS（内部MCP Agent/Server推广小组）的攻坚团队。后续的持续工作由开发生产力团队承接，该团队也负责我们包括CI/CD、构建系统和自动化在内的许多内部工具。

以下数据展示了我们过去30天内部Agent（智能体）AI的使用情况：

- 在约6100名员工中，有**3683名内部用户**积极使用AI编程工具（占全公司的60%，占研发部门的93%）
- **4795万次**AI请求
- **295个团队**正在使用Agent（智能体）AI工具和编码助手
- 每月**2018万次**AI Gateway请求
- **2413.7亿个**Token通过AI Gateway路由
- **518.3亿个**Token在Workers AI上处理

这对内部开发速度的影响是显而易见的：我们从未见过合并请求出现如此程度的季度环比增长。

随着AI工具采用率的增长，4周滚动平均值已从每周约5600次攀升至超过8700次。3月23日当周达到了10952次，几乎是第四季度基线的两倍。

MCP服务器是起点，但团队很快意识到我们需要走得更远：重新思考标准如何编码化、代码如何审查、工程师如何入职以及变更如何在数千个代码库中传播。

本文将深入探讨过去十一个月的情况以及我们最终达成的成果。我们选择在"Agent（智能体）周"结束时发布，是因为我们内部构建的AI工程栈运行于本周我们正在交付和增强的同一批产品之上。

## 架构概览

面向工程师的工具层（OpenCode、Windsurf和其他兼容MCP的客户端）包含开源和第三方的编码助手工具。

每一层都对应我们使用的一个Cloudflare产品或工具：

我们构建的内容 | 构建所用技术
--- | ---
零信任身份验证 | Cloudflare Access
集中式LLM（大语言模型）路由、成本跟踪、BYOK和零数据保留控制 | AI Gateway
使用开放权重模型的平台内推理 | Workers AI
支持单点OAuth的MCP服务器门户 | Workers+Access
AI代码审查器CI集成 | Workers+AI Gateway
用于Agent（智能体）生成代码的沙箱执行（代码模式） | Dynamic Workers
有状态、长时间运行的Agent（智能体）会话 | Agents SDK（McpAgent、Durable Objects）
用于克隆、构建和测试的隔离环境 | Sandbox SDK——已于Agent（智能体）周正式发布
持久的多步骤工作流 | Workflows——在Agent（智能体）周期间扩展了10倍
包含16000多个实体的知识图谱 | Backstage（开源）

这些都不是仅供内部使用的基础设施。上面列出的所有内容（除了Backstage）都是已交付的产品，其中许多在Agent（智能体）周期间获得了重大更新。

我们将分三个部分来阐述：

1.  **平台层**——身份验证、路由和推理如何工作（AI Gateway、Workers AI、MCP门户、代码模式）
2.  **知识层**——Agent（智能体）如何理解我们的系统（Backstage、AGENTS.md）
3.  **执行层**——我们如何在大规模下保持高质量（AI代码审查器、工程法典）

## 第一部分：平台层

### AI Gateway如何帮助我们保持安全并改善开发者体验

当你有超过3600名内部用户每天使用AI编程工具时，你需要解决跨多个客户端、用例和角色的访问和可见性问题。

一切始于**Cloudflare Access**，它处理所有身份验证和零信任策略执行。一旦通过身份验证，每个LLM（大语言模型）请求都会通过**AI Gateway**路由。这为我们提供了一个统一的管理点，用于管理提供商密钥、成本跟踪和数据保留策略。

OpenCode AI Gateway概览：每天68.846万次请求，每天105.7亿个Token，通过一个端点路由到四个提供商。

AI Gateway分析显示每月使用量在模型提供商间的分布情况。在过去一个月中，内部请求量细分如下：

提供商 | 请求数/月 | 占比
--- | --- | ---
Frontier Labs（OpenAI、Anthropic、Google） | 1338万 | 91.16%
Workers AI | 130万 | 8.84%

目前，前沿模型处理了大部分复杂的Agent（智能体）编码工作，但Workers AI已经成为组合中的重要部分，并且处理我们Agent（智能体）工程工作负载的份额正在增加。

#### 我们如何越来越多地利用Workers AI

**Workers AI**是Cloudflare的无服务器AI推理平台，在我们全球网络的GPU上运行开源模型。除了与前沿模型相比巨大的成本改进外，一个关键优势是推理与你的Workers、Durable Objects和存储位于同一网络。无需处理跨云跳转，这会导致更高的延迟、网络不稳定以及额外的网络配置管理。

上个月Workers AI使用情况：514.7亿个输入Token，3.6112亿个输出Token。

2026年3月在Workers AI上推出的**Kimi K2.5**，是一个具有256k上下文窗口、工具调用和结构化输出能力的前沿级开源模型。正如我们在[Kimi K2.5发布文章](https://blog.cloudflare.com/kimi-k2-5-workers-ai)中所述，我们有一个安全Agent（智能体）每天在Kimi上处理超过70亿个Token。如果使用中等级别的专有模型，每年估计需要花费240万美元。但在Workers AI上，成本降低了77%。

除了安全领域，我们还使用Workers AI在CI流水线中进行文档审查，为数千个代码库生成AGENTS.md上下文文件，以及用于那些同网络延迟比峰值模型能力更重要的轻量级推理任务。

随着开源模型的不断改进，我们预计Workers AI将处理我们内部工作负载中越来越大的份额。

我们早期做对了一件事：从一开始就通过一个单一的代理Worker进行路由。我们本可以让客户端直接连接到AI Gateway，这样初始设置会更简单。但通过一个Worker进行集中化意味着我们可以在后期添加每用户归属、模型目录管理和权限执行，而无需触及任何客户端配置。下面引导部分描述的每一个功能之所以存在，都是因为我们有那个单一的瓶颈点。代理模式提供了直接连接所没有的控制平面，如果我们以后接入额外的编码助手工具，同一个Worker和发现端点将处理它们。

#### 工作原理：一个URL配置一切

整个设置始于一条命令：

```Rust
opencode auth login https://opencode.internal.domain
```

该命令触发一个链式过程，配置提供商、模型、MCP服务器、Agent（智能体）、命令和权限，而用户无需接触配置文件。

**步骤1：发现身份验证要求。** OpenCode从类似`https://opencode.internal.domain/.well-known/opencode`的URL获取`config`。

这个发现端点由一个Worker提供服务，响应中包含一个`auth`块，告诉OpenCode如何进行身份验证，以及一个包含提供商、MCP服务器、Agent（智能体）、命令和默认权限的`config`块：

```JSON
{
  "auth": {
    "command": ["cloudflared", "access", "login", "..."],
    "env": "TOKEN"
  },
  "config": {
    "provider": { "..." },
    "mcp": { "..." },
    "agent": { "..." },
    "command": { "..." },
    "permission": { "..." }
  }
}

```

第二步：通过 Cloudflare Access 进行身份验证。OpenCode 运行身份验证命令，用户通过他们在 Cloudflare 处理其他所有事务时使用的同一 SSO 进行身份验证。`cloudflared` 返回一个已签名的 JWT。OpenCode 将其存储在本地，并自动将其附加到后续的每个提供者请求中。

第三步：配置合并到 OpenCode。提供的配置是整个组织的共享默认设置，但本地配置始终具有优先权。用户可以在不影响他人的情况下，覆盖默认模型、添加自己的 Agent（智能体），或调整项目及用户范围的权限。

在代理 Worker 内部。该 Worker 是一个简单的 Hono 应用，主要做三件事：

1.  提供共享配置。配置在部署时从结构化的源文件编译而来，其中包含占位符值，例如 Worker 源站的 `{baseURL}`。在请求时，Worker 会替换这些值，因此所有提供者请求都通过 Worker 路由，而不是直接发送给模型提供者。每个提供者都有一个路径前缀（`/anthropic`、`/openai`、`/google-ai-studio/v1beta`、`/compat` 用于 Workers AI），Worker 会将其转发到相应的 AI Gateway 路由。
2.  将请求代理到 AI Gateway。当 OpenCode 发送类似 `POST /anthropic/v1/messages` 的请求时，Worker 会验证 Cloudflare Access JWT，然后在转发前重写请求头：

```Shell
移除的头部：   authorization, cf-access-token, host
添加的头部：      cf-aig-authorization: Bearer <API_KEY>
            cf-aig-metadata: {"userId": "<anonymous-uuid>"}

```

请求被发送到 AI Gateway，由其路由到适当的提供者。响应直接通过，无需任何缓冲。客户端配置中的 `apiKey` 字段为空，因为 Worker 会在服务器端注入真实的密钥。用户机器上不存在任何 API 密钥。

3.  保持模型目录最新。每小时一次的 cron 触发器会从 `models.dev` 获取当前的 OpenAI 模型列表，将其缓存在 Workers KV 中，并为每个模型注入 `store: false` 以实现零数据保留。新模型会自动获得 ZDR，无需重新部署配置。

提供共享配置。配置在部署时从结构化的源文件编译而来，其中包含占位符值，例如 Worker 源站的 `{baseURL}`。在请求时，Worker 会替换这些值，因此所有提供者请求都通过 Worker 路由，而不是直接发送给模型提供者。每个提供者都有一个路径前缀（`/anthropic`、`/openai`、`/google-ai-studio/v1beta`、`/compat` 用于 Workers AI），Worker 会将其转发到相应的 AI Gateway 路由。

将请求代理到 AI Gateway。当 OpenCode 发送类似 `POST /anthropic/v1/messages` 的请求时，Worker 会验证 Cloudflare Access JWT，然后在转发前重写请求头：

```Shell
移除的头部：   authorization, cf-access-token, host
添加的头部：      cf-aig-authorization: Bearer <API_KEY>
            cf-aig-metadata: {"userId": "<anonymous-uuid>"}

```

请求被发送到 AI Gateway，由其路由到适当的提供者。响应直接通过，无需任何缓冲。客户端配置中的 `apiKey` 字段为空，因为 Worker 会在服务器端注入真实的密钥。用户机器上不存在任何 API 密钥。

保持模型目录最新。每小时一次的 cron 触发器会从 `models.dev` 获取当前的 OpenAI 模型列表，将其缓存在 Workers KV 中，并为每个模型注入 `store: false` 以实现零数据保留。新模型会自动获得 ZDR，无需重新部署配置。

匿名用户追踪。JWT 验证后，Worker 使用 D1 进行持久存储，并用 KV 作为读取缓存，将用户的电子邮件映射到一个 UUID。AI Gateway 在 `cf-aig-metadata` 中只能看到匿名 UUID，永远不会看到电子邮件。这使我们能够进行每用户成本跟踪和使用分析，而不会向模型提供者或 Gateway 日志暴露身份信息。

配置即代码。Agent（智能体）和命令以带有 YAML 前言（frontmatter）的 Markdown 文件形式编写。一个构建脚本将它们编译成一个单一的 JSON 配置，并根据 OpenCode JSON 模式进行验证。每个新会话都会自动获取最新版本。

整体架构简单，任何人都可以使用我们的开发者平台轻松部署：一个代理 Worker、Cloudflare Access、AI Gateway，以及一个客户端可访问的自动配置一切的发现端点。用户只需运行一个命令即可完成。他们无需手动配置任何内容，笔记本电脑上没有 API 密钥，也无需手动设置 MCP 服务器连接。对我们的 Agent（智能体）工具进行更改，并更新 3,000 多人在其编码环境中获得的内容，只需执行一次 `wrangler deploy`。

### MCP 服务器门户：一次 OAuth，多个 MCP 工具

我们在[另一篇文章](https://blog.cloudflare.com/zh-cn)中描述了我们在企业规模上管理 MCP 的完整方法，包括我们如何结合使用 MCP 服务器门户、Cloudflare Access 和代码模式。以下是我们内部构建内容的简短版本。

我们的内部门户聚合了 13 个生产 MCP 服务器，这些服务器暴露了 182 多个工具，涵盖 Backstage、GitLab、Jira、Sentry、Elasticsearch、Prometheus、Google Workspace、我们内部的 Release Manager 等。这统一了访问权限并简化了一切，为我们提供了一个端点和一次 Cloudflare Access 流程来管理对每个工具的访问。

每个 MCP 服务器都建立在相同的基础上：来自 Agents SDK 的 McpAgent、用于 OAuth 的 `workers-oauth-provider` 以及用于身份验证的 Cloudflare Access。整个系统位于一个单一的单体仓库中，包含共享的身份验证基础设施、Bazel 构建、CI/CD 流水线以及用于 Backstage 注册的 `catalog-info.yaml`。添加新服务器主要是复制现有的服务器并更改其包装的 API。有关其工作原理及背后的安全架构的更多信息，请参阅[我们的企业 MCP 参考架构](https://blog.cloudflare.com/zh-cn)。

### 门户层的代码模式

MCP 是将 AI Agent（智能体）连接到工具的正确协议，但它存在一个实际问题：每个工具定义在模型开始工作之前就会消耗上下文窗口的 Token。随着 MCP 服务器和工具数量的增加，Token 开销也随之增加，在规模上，这会成为一笔真实的成本。代码模式是新兴的解决方案：模型不是预先加载每个工具模式，而是通过代码来发现和调用工具。

我们的 GitLab MCP 服务器最初暴露了 34 个独立的工具（`get_merge_request`、`list_pipelines`、`get_file_content` 等）。这 34 个工具模式每个请求大约消耗 15,000 个上下文窗口 Token。在一个 200K 的上下文窗口中，这意味着在提出问题之前就消耗了 7.5% 的预算。乘以每个请求、每位工程师、每一天，加起来数额可观。

MCP 服务器门户现在支持代码模式代理，这使我们能够集中解决这个问题，而不是逐个服务器地解决。门户不是将每个上游工具定义暴露给客户端，而是将它们压缩为两个门户级别的工具：`portal_codemode_search` 和 `portal_codemode_execute`。

在门户层这样做的好处是它可以清晰地扩展。如果没有代码模式，每个新的 MCP 服务器都会给每个请求增加更多的模式开销。有了门户级别的代码模式，即使我们在门户后面连接了更多的服务器，客户端仍然只看到两个工具。这意味着更少的上下文膨胀、更低的 Token 成本以及整体更简洁的架构。

## 第二幕：知识层

### Backstage：支撑一切的底层知识图谱

在 iMARS 团队能够构建真正有用的 MCP 服务器之前，我们需要解决一个更根本的问题：关于我们服务和基础设施的结构化数据。我们需要我们的 Agent（智能体）理解代码库之外的上下文，比如谁拥有什么、服务之间如何相互依赖、文档存放在哪里，以及服务与哪些数据库通信。

我们运行 Backstage（最初由 Spotify 构建的开源内部开发者门户）作为我们的服务目录。它是自托管的（记录一下，不是运行在 Cloudflare 产品上），它跟踪诸如以下内容：

- 2,055 个服务、167 个库和 122 个包
- 228 个带有模式定义的 API
- 544 个系统（产品），横跨 45 个领域
- 1,302 个数据库、277 个 ClickHouse 表、173 个集群
- 375 个团队和 6,389 名用户，并附有所有权映射关系
- 依赖关系图，将服务与其依赖的数据库、Kafka 主题和云资源连接起来

2,055 个服务、167 个库和 122 个包

228 个带有模式定义的 API

544 个系统（产品），横跨 45 个领域

1,302 个数据库、277 个 ClickHouse 表、173 个集群

375 个团队和 6,389 名用户，并附有所有权映射关系

依赖关系图，将服务与其依赖的数据库、Kafka 主题和云资源连接起来

我们的 Backstage MCP 服务器（13 个工具）可通过我们的 MCP 门户使用，Agent（智能体）可以查找服务的所有者、检查其依赖项、查找相关的 API 规范并获取技术洞察分数，所有这些都无需离开编码会话。

没有这种结构化数据，Agent（智能体）就如同在盲目工作。它们可以阅读眼前的代码，但无法看到其周围的系统。目录将单个代码仓库转变为一个相互连接的工程组织地图。

### AGENTS.md：让数千个代码仓库为 AI 做好准备

在推广初期，我们不断看到相同的失败模式：编码 Agent（智能体）产生的更改看起来合理，但对代码仓库来说仍然是错误的。通常问题在于本地上下文：模型不知道正确的测试命令、团队当前的约定，或者代码库的哪些部分是禁止修改的。这促使我们转向 AGENTS.md：每个代码仓库中一个简短的结构化文件，它告诉编码 Agent（智能体）代码库实际如何工作，并迫使团队将这些上下文明确化。

#### AGENTS.md 的样子

我们构建了一个系统，可以在我们的 GitLab 实例中生成 AGENTS.md 文件。由于这些文件直接位于模型的上下文窗口中，我们希望它们保持简短且信息量高。一个典型的文件如下所示：

```rust
# AGENTS.md

## 仓库信息
- 运行时：cloudflare workers
- 测试命令：`pnpm test`
- 代码检查命令：`pnpm lint`

## 如何浏览此代码库
- 所有 cloudflare workers 都在 src/workers/ 目录下，每个 worker 一个文件
- MCP 服务器定义在 src/mcp/ 目录下，每个工具在一个单独的文件中
- 测试文件与源文件对应：src/foo.ts -> tests/foo.test.ts

## 约定
- 测试：使用 Vitest 和 `@cloudflare/vitest-pool-workers`（Codex：RFC 021，RFC 042）
- API 模式：遵循内部 REST 约定（Codex：API-REST-01）

## 边界
- 请勿编辑 `gen/` 目录下的生成文件
- 更新 `config/` 前，请勿引入新的后台作业

## 依赖关系
- 依赖于：auth-service，config-service
- 被依赖：api-gateway，dashboard

```

当 Agent（智能体）读取此文件时，它不必从头开始推断代码仓库。它知道代码库是如何组织的，应遵循哪些约定以及适用哪些工程 Codex 规则。

#### 我们如何大规模生成它们

生成器流水线从我们的 Backstage 服务目录中提取实体元数据（所有权、依赖关系、系统关系），分析仓库结构以检测语言、构建系统、测试框架和目录布局，然后将检测到的技术栈映射到相关的工程 Codex 标准。然后，一个能力强大的模型会生成结构化文档，系统会打开一个合并请求，以便所属团队可以审查和完善它。

我们已通过这种方式处理了大约 3,900 个仓库。第一轮生成并不总是完美的，特别是对于多语言仓库或不寻常的构建设置，但即使是这个基线也比要求 Agent（智能体）从头推断一切要好得多。

最初的合并请求解决了引导问题，但保持这些文件的最新状态同样重要。一个过时的 AGENTS.md 可能比根本没有文件更糟。我们通过 AI 代码审查器关闭了这个循环，当仓库的变更表明 AGENTS.md 应该更新时，它可以发出标记。

## 第三幕：执行层

### AI 代码审查器

Cloudflare 的每个合并请求都会获得一次 AI 代码审查。集成很简单：团队在其流水线中添加一个 CI 组件，从那时起，每个 MR 都会自动被审查。

我们使用 GitLab 的自托管解决方案作为我们的 CI/CD 平台。审查器被实现为一个 GitLab CI 组件，团队将其包含在他们的流水线中。当 MR 被打开或更新时，CI 作业会运行一个多 Agent（智能体）审查协调器。协调器根据风险等级（轻微、轻度或完整）对 MR 进行分类，并委托给专门的审查 Agent（智能体）：代码质量、安全性、codex 合规性、文档、性能和发布影响。每个 Agent（智能体）都连接到 AI 网关以访问模型，从中央仓库拉取工程 Codex 规则，并读取仓库的 AGENTS.md 以获取代码库上下文。结果以结构化的 MR 评论形式发布回来。

一个独立的基于 Workers 的配置服务处理每个审查器 Agent（智能体）的集中模型选择，因此我们可以在不更改 CI 模板的情况下切换模型。审查过程本身在 CI 运行器中运行，每次执行都是无状态的。

### 输出格式

我们花时间完善了输出格式。审查结果被分为多个类别（安全性、代码质量、性能），以便工程师可以扫描标题，而不是阅读大段文字。每个发现都有一个严重性级别（严重、重要、建议或可选细节），这使得需要关注的内容与信息性内容一目了然。

审查器会在多次迭代中保持上下文。如果它在之前的审查轮次中标记了某个问题，而该问题后来已被修复，它会予以确认，而不是再次提出相同的问题。当某个发现映射到工程 Codex 规则时，它会引用特定的规则 ID，将 AI 建议转变为对组织标准的引用。

Workers AI 处理了审查器约 15% 的流量，主要用于文档审查任务，在这些任务中，Kimi K2.5 表现出色，成本仅为前沿模型的一小部分。像 Opus 4.6 和 GPT 5.4 这样的模型则处理安全敏感和架构复杂的审查，这些情况下推理能力最为重要。

在过去 30 天里：

- 在我们的标准 CI 流水线上，所有仓库的 AI 代码审查器覆盖率达到 100%。
- 处理了 5.47M 次 AI 网关请求
- 处理了 24.77B 个 Token

在我们的标准 CI 流水线上，所有仓库的 AI 代码审查器覆盖率达到 100%。

处理了 5.47M 次 AI 网关请求

处理了 24.77B 个 Token

我们与本文一同发布了一篇详细的技术博客文章，涵盖了审查器的内部架构，包括我们如何在模型之间路由、多 Agent（智能体）编排以及我们开发的成本优化策略。

### 工程 Codex：将工程标准作为 Agent（智能体）技能

工程 Codex 是 Cloudflare 新的内部标准系统，我们的核心工程标准存放于此。我们有一个多阶段的 AI 提炼过程，它输出一组 codex 规则（"如果你需要 X，就使用 Y。如果你正在做 Y 或 Z，你必须做 X。"）以及一个 Agent（智能体）技能，该技能使用渐进式披露和嵌套的层次信息目录，并在 Markdown 文件之间建立链接。

工程师在本地构建时可以使用此技能，例如使用"我应该如何处理我的 Rust 服务中的错误？"或"审查此 TypeScript 代码的合规性。"等提示词。我们的网络防火墙团队使用多 Agent（智能体）共识流程审核了 `rampartd`，其中每个要求都被评为合规、部分合规或不合规，并附有具体的违规细节和修复步骤，将以前需要数周手动工作的过程简化为一个结构化、可重复的流程。

在审查时，AI 代码审查器会在其反馈中引用特定的 Codex 规则。

AI 代码审查：显示分类的发现（本例中为 Codex 合规性），并指出违反 codex RFC 的情况。

这些组件单独来看都算不上特别新颖。许多公司都在运行服务目录、部署代码审查机器人或发布工程标准。真正的差异在于它们之间的连接方式。当一个Agent（智能体）能够从Backstage获取上下文、读取其正在编辑的代码库中的AGENTS.md文件，并通过同一工具链接受基于Codex规则的审查时，其生成的初稿通常就已接近可交付状态。这在六个月前是无法实现的。

## 成果看板

从启动这项计划到实现93%的研发团队采用率，用时不到一年。

公司范围内采用情况（2026年2月5日 – 4月15日）：

指标

数值

活跃用户

3,683人（占公司总人数60%）

研发团队采用率

93%

AI消息数

4,795万

有AI活动的团队数

100%

OpenCode消息数

2,708万

Windsurf消息数

43.49万

AI网关（最近30天，合计）：

请求数

2,018万

Token数

2,413.7亿

Workers AI（最近30天）：

输入Token数

514.7亿

输出Token数

3.6112亿

## 下一步：后台Agent

我们内部工程栈的下一阶段演进将包含后台Agent：这些Agent可按需启动，拥有与本地相同的可用工具（MCP门户、git、测试运行器），但完全在云端运行。该架构使用Durable Objects和Agents SDK进行编排，当任务需要完整的开发环境（如克隆代码库、安装依赖项或运行测试）时，则委托给Sandbox容器处理。Sandbox SDK已在Agent周期间正式发布。

长期运行的Agent（于Agent周期间原生集成至Agents SDK中）解决了此前需要变通方案才能处理的持久会话问题。该SDK现在支持长时间运行而不被驱逐的会话，足以让一个Agent在单次会话中克隆大型代码库、运行完整测试套件、针对失败进行迭代并提交合并请求。

这代表了一项历时十一个月的努力，其目标不仅是重新思考代码如何编写，还包括如何审查代码、如何执行标准以及如何安全地在数千个代码库中部署变更。每一层都运行在我们的客户所使用的相同产品之上。

## 开始构建

Agent周刚刚发布了您所需的一切。平台现已就绪。

```Shell
npx create-cloudflare@latest --template cloudflare/agents-starter

```

该Agent入门模板能让您快速启动。下图是当您准备扩展时的完整架构：顶层是您的工具层（聊天机器人、Web界面、命令行工具、浏览器扩展），中间是处理会话状态和编排的Agents SDK，底层是您从中调用的Cloudflare各项服务。

文档：Agents SDK · Sandbox SDK · AI Gateway · Workers AI · Workflows · Code Mode · MCP on Cloudflare

代码库：cloudflare/agents · cloudflare/sandbox-sdk · cloudflare/mcp-server-cloudflare · cloudflare/skills

想了解更多关于Cloudflare如何运用AI的信息，请阅读我们关于AI代码审查流程的文章。并查看我们在Agent周期间发布的所有内容。

我们期待了解您的构建成果。请在Discord、X和Bluesky上找到我们。

Ayush Thakur构建了AGENTS.md系统以及OpenCode基础设施的AI网关集成，Scott Roemeschke是Cloudflare开发者生产力团队的工程经理，Rajesh Bhatia领导Cloudflare的生产力平台职能。本文是Devtools团队的协作成果，并得到了来自公司内部志愿者组成的iMARS（内部MCP Agent/Server推广小组）老虎团队的大力协助。

---

> 本文由AI自动翻译，原文链接：[The AI engineering stack we built internally â on the platform we ship](https://blog.cloudflare.com/internal-ai-engineering-stack/)
> 
> 翻译时间：2026-04-21 05:12
