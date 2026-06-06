---
title: Kiro IDE集成Databricks：AI开发新路径
title_original: Bring Databricks into Kiro IDE with the AI Dev Kit Power
date: '2026-06-03'
source: Databricks Blog
source_url: https://www.databricks.com/blog/bring-databricks-kiro-ide-ai-dev-kit-power
author: ''
summary: 文章介绍了将Kiro IDE连接到Databricks的两种方式：基于四条MCP服务器的轻量级路径A，以及一键安装的Databricks AI Dev
  Kit Power路径B。两者均继承Unity Catalog的权限控制，确保AI助手只能访问用户可见的数据，避免幻觉和未授权读取。路径A适合分析师和SQL开发者，路径B则开放完整Databricks平台功能。通过实时工作区元数据接地，AI辅助开发更准确、安全。
categories:
- AI基础设施
tags:
- Databricks
- Kiro IDE
- MCP
- AI辅助开发
- Unity Catalog
draft: false
translated_at: '2026-06-06T05:53:24.047180'
---

- 将Kiro IDE连接到Databricks的两条路径：四条Databricks管理的MCP服务器（Genie、SQL、Unity Catalog Functions、Vector Search），基于PAT的10分钟设置方案；或全新的Databricks AI Dev Kit Power——一键安装，包含所有必备工具和技能，四种认证方式可选。
- 基于真实工作区元数据的AI辅助开发：两条路径均继承Unity Catalog的行级、列级和基于标签的权限，因此助手使用您的实际列编写SQL，且只能看到您能看到的内容——无幻觉，无未授权读取。
- 根据覆盖范围选择：路径A是面向分析师和SQL优先开发者的最轻量级设置；路径B在IDE内开放完整的Databricks平台（pipelines、jobs、Mosaic AI、Agent Bricks、Lakebase、Asset Bundles）。

## 为何重要

当AI辅助开发助手需要猜测列名、表结构或您可读取的目录时，其效果就会大打折扣。解决方案是接地：通过模型上下文协议（MCP）将助手连接到实时工作区元数据，它编写的SQL使用您实际拥有的列，dbt模型连接真实表，每个查询都继承您已配置的Unity Catalog权限。数据不会离开平台。AI只能看到您能看到的内容。

两个里程碑刚刚实现，使这一功能在Kiro IDE中变得实用：

首先，Databricks AI Dev Kit在PR #511中增加了对Kiro的上游支持。统一安装程序将`kiro`视为与`claude`、`cursor`、`copilot`、`codex`和`gemini`同等的顶级目标。一条命令，Kiro即可在`~/.kiro/skills/`和`~/.kiro/settings/mcp.json`中获取完整工具包。

其次，Databricks AI Dev Kit Power在PR #129中已发布至Kiro Powers目录。打开Powers面板，点击Try，Power将运行完整的入门流程：安装程序、MCP连接、认证检测和技能加载。

结合平台内已内置的四条Databricks管理的远程MCP服务器，您有两种方式将Kiro连接到Databricks。两者共享一个共同成果：当助手继承真实工作区权限而非猜测模式、列和权限时，开发者能更快地交付分析、管道和Agent工作流。

## 为何选择Databricks进行AI辅助开发

上述两个里程碑使Kiro × Databricks变得实用。其重要性在于底层能力。无论选择哪条路径，有三点使Databricks成为AI辅助开发的首选基础平台。

Unity Catalog是唯一在数据层面为AI提供接地的治理层。每条MCP调用——路径A或路径B——都继承行级、列级和基于标签的权限。助手对您的数据没有特权视图；它只能看到您能看到的内容。无需管理单独访问控制层，也不存在AI针对其不应知晓的表编写查询的风险。

一份数据，一套定义。由于Databricks是湖仓一体，助手通过databricks-sql查询的表，与您的dbt模型写入的表、Genie空间暴露的表、AI/BI仪表盘读取的表是同一张表。不存在仓库到湖的同步中断问题，也无需维护独立的语义层。当助手以samples.tpch.lineitem为基础时，它使用的是与其他所有工具相同的定义。

完整的AI栈是集成的，而非拼凑而成。Mosaic AI Gateway路由模型调用。Agent Bricks编排多Agent工作流。MLflow跟踪实验和评估。Vector Search支持语义检索。Lakebase处理事务状态。所有这些都在Power中呈现，且基于同一套UC。您无需拼接五个产品，而是使用一个平台。

还有第四点值得一提：Power本身由Databricks构建。没有其他数据平台能为Kiro、Cursor、Claude、Copilot、Codex和Gemini提供一键式IDE Power。MCP层是开放的，协议是开放的，集成是开放的——但封装这一切的体验是由Databricks专门根据我们客户的构建方式设计的。

## 两条路径概览

| 维度 | 路径A：托管MCP服务器 | 路径B：Databricks AI Dev Kit Power |
|------|----------------------|--------------------------------------|
| 覆盖范围 | 4台服务器：Genie、SQL、UC Functions、Vector Search | 所有必备Databricks工具和技能 |
| 获得内容 | 自然语言SQL、语义搜索、受管控的函数执行 | 路径A覆盖范围加上pipelines、jobs、dashboards、Lakebase、Mosaic AI、Agent Bricks、Asset Bundles、MLflow、模型服务、Apps |
| 托管方式 | Databricks托管（远程HTTPS） | 通过AI Dev Kit安装程序的本地Python MCP服务器 |
| 认证方式 | Shell环境中的PAT | OAuth U2M（推荐）、OAuth M2M、.databrickscfg配置文件或PAT |
| 设置方式 | 编辑~/.kiro/settings/mcp.json，导出环境变量 | 一键Power安装加引导式认证流程 |
| 适用对象 | 希望10分钟即可向数据仓库提问的分析师和SQL优先开发者 | 需要在单个IDE中获得完整Databricks覆盖范围的数据工程师和平台构建者 |

## 集成架构概览

![](/images/posts/414968758d55.png)

两条路径共享相同的后端：Unity Catalog强制策略和Databricks工作区身份。它们在覆盖范围和认证模型上有所不同。

## 路径A：连接到四条托管MCP服务器

这是最轻量级的设置。一个`mcp.json`文件、一个Databricks个人访问令牌和一个shell配置文件编辑。10分钟内，Kiro即可与Genie、SQL、Unity Catalog Functions和Vector Search通信。

### 前提条件

- 一个启用了Unity Catalog的AWS上的Databricks工作区。
- 一个Databricks个人访问令牌（PAT）或OAuth令牌，作用域限定为您计划使用的MCP服务器（`sql`、`unity-catalog`、`genie`、`vector-search`）。未使用的PAT将在90天后自动撤销。
- Kiro已安装并至少启动一次，以便`~/.kiro/`存在。
- 您的工作区主机名格式为`<workspace>.cloud.databricks.com`。

### 生成Databricks PAT

在Databricks工作区中，进入Settings、Developer、Access tokens、Manage、Generate new token。设置与团队轮换策略一致的过期时间。仅选择您需要的API作用域；最小权限原则优于"全部"的便利性。立即复制令牌。Databricks不会再次显示。

### Kiro存储MCP配置的位置

Kiro从两个作用域的JSON读取MCP配置；工作区覆盖用户设置。

- 用户作用域：`~/.kiro/settings/mcp.json`适用于每个工作区。
- 工作区作用域：`$PWD/.kiro/settings/mcp.json`仅适用于当前工作区，并覆盖用户作用域中相同键的条目。

### 从Kiro服务器目录一键安装

打开kiro.dev/docs/mcp/servers/，找到Databricks行，点击Add to Kiro。浏览器启动Kiro并打开一个包含预填充配置的确认对话框。确认后，将`databricks-sql`条目写入`~/.kiro/settings/mcp.json`。该条目引用了两个尚不存在的环境变量；我们接下来设置它们。

### 验证（或添加）databricks-sql条目

### 设置环境变量

在启动Kiro的shell配置文件（macOS上通常为`~/.zshrc`）中：

在启动Kiro之前，source该配置文件（`source ~/.zshrc`）。完全退出Kiro（macOS上为Cmd+Q）并重新打开。重新加载窗口不会重新读取环境变量；只有进程重启才会。

### 添加Genie、UC Functions和Vector Search

所有四条Databricks管理的服务器都作为远程HTTP MCP连接。即使使用占位URL，初始化握手也能成功；服务器仅在调用工具时验证资源。连接但存在故障的状态，即`tools/call`返回`RESOURCE_DOES_NOT_EXIST`或`PERMISSION_DENIED`，是最常见的故障模式。请先运行以下预检查：

- Genie：确认存在一个 Genie 空间且您可以打开它。空间 ID 显示在 URL 中。
- UC 函数：确认该函数存在且您拥有 `EXECUTE` 权限。通过 `SELECT * FROM system.information_schema.routines WHERE routine_type = 'FUNCTION'` 列出函数。
- 向量搜索：确认在“目录”>“向量搜索”下存在一个至少包含一个可访问索引的端点。
- PAT 范围：如果用户对特定资源缺乏“可查看”权限，即使使用工作区范围的 PAT，在访问 Genie 空间或向量索引时仍可能遇到 `PERMISSION_DENIED` 错误。Genie 空间是单独共享的。

添加额外的环境变量（`DATABRICKS_GENIE_MCP_URL`、`DATABRICKS_UC_FUNCTIONS_MCP_URL`、`DATABRICKS_VECTOR_SEARCH_MCP_URL`），并将 `mcp.json` 更新为完整配置：

各服务器的 URL 格式：

服务器

URL 模式

databricks-genie

`https://<workspace-hostname>/api/2.0/mcp/genie/<genie_space_id>`

databricks-sql

`https://<workspace-hostname>/api/2.0/mcp/sql`

databricks-uc-functions

`https://<workspace-hostname>/api/2.0/mcp/functions/<catalog>/<schema>/<function_name>`

databricks-vector-search

`https://<workspace-hostname>/api/2.0/mcp/vector-search/<catalog>/<schema>/<index_name>`

退出并重新启动 Kiro。打开 Kiro 面板的“MCP 服务器”部分；四个 `databricks-*` 条目将显示为绿色状态指示器。点击任何红色条目的“重新连接”并重新检查前置条件。在聊天面板中尝试一个低风险的初始查询：“列出我有权访问的目录。”

### 路径 B：安装 Databricks AI Dev Kit Power

四个托管服务器涵盖了 SQL、语义搜索和自然语言分析，这对许多构建者来说已经足够。如果您的工作流程涉及管道、作业、模型服务、Lakebase、Asset Bundles、Mosaic AI、Agent Bricks、AI/BI 仪表板、MLflow 或 Databricks Apps，那么四个服务器的设置会让您整天都在复制粘贴回工作区 UI。

Databricks AI Dev Kit Power 解决了这个问题。一次安装。所有必要的工具和技能，四种身份验证选项，均可按需加载。

### 您将获得什么

功能范围

覆盖范围

SQL 与计算

在仓库上执行 SQL；在集群上运行 Python 或 Scala；管理计算生命周期

管道与作业

Spark 声明式管道（流表、CDC、SCD Type 2、Auto Loader）；多任务作业 DAG

Unity Catalog

表、卷、授权、标签、存储凭据、系统表、指标视图、外部 Iceberg 读取

AI/BI 仪表板

可视化、KPI、分析仪表板

Genie 空间

基于受管数据集进行自然语言数据探索

Agent Bricks

知识助手（RAG）和多 Agent 监督器

向量搜索

使用受管索引进行语义搜索和 RAG

模型服务

ML 模型、AI Agent，以及按 Token 付费的基础模型 API（FMAPI），可通过 AI 网关路由

MLflow

实验、评估、追踪仪表化、指标查询

Lakebase

为 OLTP 工作负载提供预置和自动扩展的受管 PostgreSQL

Databricks Apps

基于 Lakehouse 的全栈 Web 应用

Asset Bundles

Databricks 资源的基础设施即代码

### 一键安装

在 Kiro 内部，打开“Powers”面板，搜索 `databricks`，然后点击“尝试”。该 Power 以非交互式 Kiro 模式运行官方的 Databricks AI Dev Kit 安装程序：

安装程序下载 MCP 服务器，创建一个 `uv` 虚拟环境，并将专家技能库拉取到 `~/.kiro/skills/`。Power 将这些技能复制到其自身的 `steering/` 目录中，以便根据当前任务按需加载。Power 本身不捆绑任何内容；所有内容均从上游获取，因此技能始终保持最新。

### 四种身份验证选项

Power 的引导流程会检测现有凭据，并引导您做出正确选择。所有四种选项均有内联文档说明：

选项

说明

适用场景

A：OAuth U2M（推荐用于交互式使用）

Databricks CLI 打开浏览器，您以自身身份进行身份验证，SDK 每小时自动刷新

工作站上的单个人类开发者。最安全的交互式流程，无长期存在的密钥泄露风险

B：OAuth M2M

Databricks 服务主体使用 `client_id` 和 `client_secret` 进行身份验证；SDK 自动签发 1 小时令牌

无头环境、CI/CD 或生产环境 Agent

C：现有的 `.databrickscfg` 配置文件

将 Power 指向您已用于 Databricks CLI 或其他工具的配置文件

您已有可用的配置文件，不想重新设置身份验证

D：个人访问令牌（旧版）

`mcp.json` 的 `env` 块中的 Bearer 令牌

不支持 OAuth 的工具，或未启用 OAuth U2M 的工作区

Power 的 `mcp.json` 在您选择选项之前默认带有 `disabled: true`；在您明确选择并配置凭据之前，不会建立任何连接。凭据检测流程是中立的。如果检测到多个凭据，所有四个选项将按顺序呈现，没有默认选项，也不会静默重用。

### 验证安装

重新启动 Kiro，打开“MCP 服务器”面板，确认 `databricks` 条目已连接（绿色）。在聊天中提问：“获取我当前的 Databricks 用户。” 这一单个调用将测试身份验证、环境变量解析和服务器启用。如果成功，则整个链路是健康的。

### 如何在两条路径之间选择

一个简单的决策树：

1. 仅运行 SQL、通过 Genie 对受管数据集提出自然语言问题以及搜索向量索引？使用路径 A。四个托管服务器正好完成这些工作，设置只需 10 分钟。
2. 编写管道、管理作业、部署 Asset Bundles、使用 Lakebase、构建 Databricks Apps 或调用 Mosaic AI / Agent Bricks？使用路径 B。完整的工具包功能范围太大，不适合作为一次性的远程 MCP 服务器进行附加。
3. 混合方案？同时运行两者。路径 A 和路径 B 不冲突。Power 写入其自己的 `mcpServers.databricks` 条目，而路径 A 的四个服务器（`databricks-genie`、`databricks-sql`、`databricks-uc-functions`、`databricks-vector-search`）是独立的键。Kiro 会在 MCP 面板中显示所有这些条目。

对于计划日常在 Kiro 中处理 Databricks 工作负载的构建者来说，路径 B 是更好的长期解决方案。如果您只有 10 分钟时间并且想与一个 SQL 仓库对话，那么路径 A 是正确的选择。

## 从构建者的视角来看

两条路径对不同的 IDE 使用者来说，体验各不相同。四种角色，四种痛点，四种解决方案。

分析工程师。您一半的时间在查询从未见过的表，另一半时间在编辑器和工作区 UI 之间复制粘贴。路径 A 在 10 分钟内解决了这个问题。Genie 和 SQL 服务器将每个查询基于真实的模式元数据；助手根据您的实际列进行编写，而不是猜测；每个结果都继承了您的 Unity Catalog 授权。您不再需要切换标签页。

数据工程师。您的工作是管道、作业、Asset Bundles 以及三者带来的跨环境升级。手动编写 `databricks.yml` 并从终端侧边栏运行 `databricks bundle deploy` 是低效的方式。路径 B 是高效的方式。Power 的管道 + 作业 + Asset Bundles 技能可以在一次对话中生成、验证和部署 IaC。Spark 声明式管道、CDC、SCD Type 2、Auto Loader——所有这些都根据您实际的 UC 表生成，并准备好提交。

AI / Agent 构建者。您正在跨三四个对模式定义不完全一致的工具来连接模型调用、评估、治理和 Agent 编排。路径 B 涵盖了完整的 Databricks AI 功能范围——用于路由和回退的 Mosaic AI 网关、用于多 Agent 监督器和知识助手的 Agent Bricks、用于评估的 MLflow、用于检索的向量搜索——所有这些都端到端地受 Unity Catalog 治理。您的 Agent 继承与其调用者相同的权限，您的评估追踪与您的训练运行位于同一个工作区。

### 平台构建者
您将Databricks资源作为代码管理，在开发/预发布/生产环境之间进行提升，并按周频率回答"是否发生漂移"的问题。路径B的资产包技能加上Unity Catalog管理技能可生成完整包，根据工作区的实际状态进行验证，并在漂移造成影响前将其显现。您无需再手动维护一套YAML和另一份文档中的配置。

### 今天即可运行的工作流
无论您选择哪条路径，本练习都使用每个Databricks工作区中可用的`samples.tpch`目录，将助手锚定在实际工作区元数据上。

您提问："`samples.tpch.lineitem`有哪些列和类型，按`l_shipdate`年份的数据分布是怎样的？"

Kiro通过单个MCP执行的查询返回实际模式（Schema）和直方图。真实的列名、真实的数据分布，无幻觉。

您提问："起草一个dbt模型，将lineitem与orders连接，并按季度和国家聚合收入。"

Kiro使用实际列名（`l_extendedprice`、`l_discount`、`o_orderdate`）生成SQL，而非猜测。因为它先查询了模式，所以知道确切的类型和粒度。

您提问："针对`samples.tpch`运行我的新聚合，并将行数与上周在`poc.gold.revenue_by_nation_qtr`中的快照进行比较。"

Kiro执行两个查询并显示差异。当某个数字看起来异常时，"显示`gold.revenue_by_nation_qtr`的血缘关系"会从`system.access.table_lineage`拉取上游表。验证通过后，Kiro为该模型生成Databricks作业JSON，并列出其涉及的所有目录和模式。

在路径B上，同一工作流可扩展为"为此作业生成资产包并部署到预发布环境"，或"创建由该聚合支持的AI/BI仪表板"，或"将其接入带有回退模型的Mosaic AI网关端点"，所有这些操作都无需离开IDE。

## 最佳实践（无论选择哪条路径）
- **最小权限认证**。为每个工作站和每个作用域集生成单独的PAT。在路径B上，交互式使用优先选择OAuth U2M而非PAT。
- **绝不提交凭据**。将`DATABRICKS_ACCESS_TOKEN`存储在shell配置文件或密钥管理器中。切勿将其放入检入源代码控制的`mcp.json`中。
- **按项目划分作用域**。将Genie空间ID和向量搜索索引路径保存在`$PWD/.kiro/settings/mcp.json`中，以便每个项目携带自己的资源绑定。
- **信任UC权限**。所有路径都强制执行Unity Catalog基于行、列和标签的授权。AI在每次调用时继承您的有效权限。无需管理单独访问控制层。
- **重启，而非重载**。Kiro在进程启动时仅读取一次环境变量。编辑shell配置文件或添加认证后，完全退出（macOS上按Cmd+Q）并重新打开。

## 故障排除
**"未找到服务器"或MCP条目显示红色状态。**

路径A：在启动Kiro的shell中检查`echo $DATABRICKS_SQL_MCP_URL`。空值意味着Kiro无法解析URL。确认工作区作用域的`mcp.json`未覆盖用户作用域的配置。验证PAT在"设置"、"开发者"、"访问令牌"中仍然有效。

路径B：从Power的入门流程重新进入凭据检测流程。如果MCP服务器返回`Invalid access token`或`401`，Power内置的401恢复钩子会暂停工具调用并重新显示认证选项。

**已连接到MCP，但工具调用返回`RESOURCE_DOES_NOT_EXIST`或`PERMISSION_DENIED`。**

最常见的路径A故障。初始化握手使用占位符URL成功，因为服务器将资源验证推迟到调用时。针对特定服务器重新运行预检检查（Genie空间存在且已与您共享，函数存在且您拥有`EXECUTE`权限，向量索引存在且您拥有"可查看"权限）。

**立即尝试。** Databricks AI开发套件Power是将完整平台——管道、作业、Lakebase、Mosaic AI、Agent Bricks以及上述所有内容——集成到Kiro中的最快方式。直接从Kiro Powers目录`github.com/kirodotdev/powers`安装，或访问`github.com/databricks-solutions/ai-dev-kit`为Kiro或任何支持的IDE（Claude、Cursor、Copilot、Codex、Gemini）安装底层工具包。对于四个Databricks管理的MCP服务器，一键安装位于`kiro.dev/docs/mcp/servers/`。

有反馈或遇到障碍？请在`databricks-solutions/ai-dev-kit`上提交问题——我们阅读每一条。

此处分享的观点和想法仅代表我们个人，并非Databricks官方政策。

### 在收件箱中获取最新文章
订阅我们的博客，最新文章将直接发送到您的收件箱。

---

> 本文由AI自动翻译，原文链接：[Bring Databricks into Kiro IDE with the AI Dev Kit Power](https://www.databricks.com/blog/bring-databricks-kiro-ide-ai-dev-kit-power)
> 
> 翻译时间：2026-06-06 05:53
