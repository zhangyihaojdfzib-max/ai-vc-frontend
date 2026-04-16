---
title: AI Gateway：如何安全连接Agent与外部MCP
title_original: 'AI Gateway: How to Connect Agents to External MCPs Securely'
date: '2026-04-15'
source: Databricks Blog
source_url: https://www.databricks.com/blog/ai-gateway-how-connect-agents-external-mcps-securely
author: ''
summary: 本文介绍了Databricks AI Gateway如何解决AI Agent连接外部工具时的认证与管理难题。通过集成Unity Catalog，AI
  Gateway提供统一的治理方式，让管理员能够集中注册、权限控制和审计外部MCP服务器（如GitHub、Glean等）。它支持按用户OAuth认证，确保Agent仅访问相应用户权限内的数据，同时简化了OAuth流程，无需为每个提供商单独注册应用。文章以连接GitHub为例，演示了从创建连接到测试部署的完整步骤，帮助团队安全高效地构建上下文感知的智能体。
categories:
- AI基础设施
tags:
- AI Gateway
- MCP
- Agent
- 数据安全
- Databricks
draft: false
translated_at: '2026-04-16T05:05:20.081447'
---

作为**Agent周**的一部分，客户现在可以通过**Databricks AI Gateway**管理模型、MCP和工具，并与Unity Catalog完全集成。要提供真正的价值，Agent需要安全地连接到GitHub、Glean和Atlassian等外部工具。AI Gateway使这一过程变得简单且安全，让团队能够专注于构建Agent，而非认证基础设施。

在本文中，我们将逐步介绍如何连接外部MCP服务器并端到端地部署一个Agent，以便您能够构建能够理解并根据您的数据进行推理和行动的上下文感知Agent。

## 问题：外部MCP服务器的认证

AI Agent的能力取决于其所能访问的工具。模型上下文协议（MCP）提供了一种通用的方式来发现和与这些工具交互，在Databricks上，企业已经使用它将Agent与原生及外部MCP连接起来。

客户一再告诉我们同样的问题：认证是瓶颈。每个提供商都有自己的OAuth应用注册、自己的客户端密钥、自己的令牌刷新逻辑。密钥需要轮换，权限需要审计，并且没有集中式的方法来跟踪哪些Agent正在访问什么。本应几分钟完成的事情需要花费数周。

## 解决方案：用于外部连接的AI Gateway

**AI Gateway**通过为团队提供一种单一的、受治理的方式来将Agent连接到外部系统，从而解决了这个问题：

*   **通过Unity Catalog治理外部MCP服务器：** 每个外部MCP服务器都在Unity Catalog中注册，使其像任何其他目录对象一样可被发现和治理。管理员可以应用细粒度权限，所有活动都记录在集中式审计表中。团队还可以通过**Databricks Marketplace**从合作伙伴处安装MCP服务器。
*   **代表用户进行访问：** Agent代表最终用户行事，因此用户A的Agent只能看到用户A被允许看到的内容。这意味着Agent可以安全地访问个人电子邮件、私有代码库和受限文档，而无需使用权限过高的服务账户。管理员可以通过为每个连接限定OAuth权限来进一步限制Agent允许执行的操作，例如将GitHub连接限制为对代码库的只读访问。
*   **简化对外部系统的认证：** 托管的OAuth流程简化了认证，无需为每个提供商注册OAuth应用或管理密钥。从下拉列表中选择，Databricks会在服务器端处理完整的认证生命周期。目前支持的提供商包括Glean、GitHub、Atlassian（Jira和Confluence）、Google Drive和SharePoint，更多提供商即将推出。
*   **跨云和提供商工作：** 无论您在AWS、Azure还是GCP上运行Databricks，都能获得相同的治理和认证体验，并对GitHub、Glean和Atlassian等第三方提供商提供预配置支持。

## 工作原理

让我们逐步介绍如何将GitHub作为外部MCP服务器连接起来，并最终部署一个Agent。

**步骤 1. 创建连接。**

*   导航到 **AI Gateway** → 注册 MCP 服务器 -> 外部 MCP
*   选择您的认证模式：**按用户OAuth**（推荐——每个用户使用自己的身份认证）或**共享主体**（所有用户使用单一身份）
*   从提供商下拉列表中选择 **GitHub**
*   点击**创建**。Databricks会在后台处理OAuth应用注册、令牌交换和刷新。

![注册 MCP 服务器](/images/posts/b6e7e264fb58.gif)

**步骤 2. 测试它。** 您可以通过两种方式验证连接。在**AI Playground**中，选择一个启用了工具的模型，浏览您的外部MCP连接，选择GitHub，然后询问"在X代码库中有哪些开放的拉取请求？"

![在 AI Playground 中测试](/images/posts/a3786fe60ee0.gif)

或者直接在**代码**中使用`DatabricksMCPClient`进行测试：

```python
from databricks_mcp_client import DatabricksMCPClient

client = DatabricksMCPClient(
    host="https://<workspace>.cloud.databricks.com",
    token="<pat>",
    connection_name="github-connection"
)

# List available tools
tools = client.list_tools()
print(tools)
```

**步骤 3. 部署您的Agent。** 验证通过后，使用**Agent Bricks**进行部署。

![使用 Agent Bricks 部署](/images/posts/0972e04b793a.gif)

**步骤 4. 监控和追踪。** 一旦您的Agent上线，**MLflow Tracing**为您提供端到端的可观测性：每个请求、每个工具调用、每个MCP服务器交互，都包含完整的输入和输出。结合Unity Catalog审计日志，可以查看谁在何时通过哪个Agent访问了什么。

![监控](/images/posts/1a1326663a3c.png)

## 开始使用

不要让认证成为您的Agent无法访问所需工具的原因。开始构建能够基于内部和外部数据进行推理和行动的Agent吧。**立即开始**。

---

> 本文由AI自动翻译，原文链接：[AI Gateway: How to Connect Agents to External MCPs Securely](https://www.databricks.com/blog/ai-gateway-how-connect-agents-external-mcps-securely)
> 
> 翻译时间：2026-04-16 05:05
