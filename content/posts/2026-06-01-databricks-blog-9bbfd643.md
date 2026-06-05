---
title: Genie Code个性化：指令、技能与MCP定制指南
title_original: Personalizing Genie Code with instructions, skills, memory, and MCP
date: '2026-06-01'
source: Databricks Blog
source_url: https://www.databricks.com/blog/personalizing-genie-code-instructions-skills-memory-and-mcp
author: ''
summary: 本文介绍了Genie Code的个性化定制功能，包括自定义指令、Agent技能、工作区技能和MCP服务器。自定义指令用于设置全局偏好，技能可捕获可重复的工作流，MCP服务器则连接外部工具如Jira、GitHub等。这些功能使Genie
  Code能适应个人和团队的工作方式，提升编码效率和协作一致性。
categories:
- AI产品
tags:
- Genie Code
- 个性化定制
- MCP服务器
- AI Agent
- 团队协作
draft: false
translated_at: '2026-06-05T06:22:58.369308'
---

*Genie Code 能够遵循您个人和团队的约定，通过指令、技能和 MCP 服务器实现。* 复用已有的内容。引入团队工作流、内部文档和外部工具，而无需将它们粘贴到每个提示词中。* 保持灵活且受管控。使用个人技能适配个人工作方式，使用工作区技能适配共享的团队工作流，并使用管理员批准的 MCP 服务器在 Agent（智能体）模式下获取可扩展的外部上下文。

当 Genie Code 了解您的团队实际运作方式时，其效果最佳：包括您的编码标准、内部工作流、共享工具以及过往决策背后的上下文。

因此，我们引入了一系列功能，使您能够根据组织和具体工作流来定制 Genie Code。指令有助于定义团队范围的偏好，技能可捕获可重复的工作流，而 MCP 服务器则能将 Genie Code 直接连接到 Jira、GitHub 和 Google Drive 等系统。

## 自定义指令

自定义指令允许您设置持久性的偏好，Genie Code 会在每次 Agent（智能体）模式会话中应用这些偏好。它们非常适合那些始终适用于您工作方式的设定：例如您偏好的编程语言、输出格式或通用风格指南。

其局限性在于指令是全局性的。如果您添加了一条 SQL 格式化规则，那么无论您是在编写 SQL 还是调试 Python，它都会被触发。对于适用于所有场景的偏好，指令是正确的工具。对于仅与特定任务相关的上下文，您需要更具针对性的方法。

对于团队级别的约定，Genie Code 还可以自动发现项目中的 `AGENTS.md` 和 `CLAUDE.md` 文件。一旦这些文件被检入仓库，Genie Code 会自动获取它们，这样团队成员就无需单独配置相同的上下文。

## Agent（智能体）技能

Agent（智能体）技能是一种教导 Genie Code 按照您的方式执行特定任务的方法。

技能是一个基于 Markdown 的包，描述了 Genie Code 在 Agent（智能体）模式下运行时可以使用的流程、模式或操作。技能可以包含指导、可复用代码和可执行脚本，所有这些都限定于特定任务，而非全局应用。

每个技能都包含一个名称和描述，帮助 Genie Code 判断何时适用。当请求与某个技能匹配时，Genie Code 会加载该技能，并使用其中包含的指导、模式和代码来做出适当的响应。

![](/images/posts/5079a2c7db6e.gif)

## 如何添加技能？

要开始使用：

1.  **打开您的技能文件夹。** 在 Genie Code 中，打开设置，导航到用户技能，然后选择打开技能文件夹。这将打开您的个人技能目录 (`/Users/{username}/.assistant/skills/`)。
2.  **创建或更新技能。** 添加一个新的 Markdown 文件。每个技能都应包含清晰的名称和描述，以便 Genie Code 知道何时适用。您可以将相关文件组织到文件夹中，并可选择包含脚本以实现更高级的工作流。

## 工作区技能

除了个人技能之外，工作区管理员可以创建工作区中所有人都能自动使用的技能。工作区技能位于 `Workspace/.assistant/skills/`。

工作区技能遵循与个人技能相同的格式，但其范围限定于团队而非个人。这使得它们非常适合那些应在整个组织中共享并一致使用的工作流——例如，一个强制实施机器学习管道命名约定的技能，一个在事件响应期间将 Genie Code 引导至正确内部操作手册的技能，或者一个将团队标准数据质量检查应用于每个新管道的技能。

## MCP 服务器

技能处理的是存在于您头脑中或团队标准中的上下文。而 MCP 服务器处理的是已经存在于其他地方的上下文。

在 2025 年初，我们在 Databricks 中引入了 MCP 支持，以受管控且可扩展的方式向 AI Agent（智能体）提供丰富的外部上下文。MCP 提供了一种标准化的方式，将工具、数据和工作流暴露给 Genie Code，而无需将这些上下文直接嵌入到提示词或指令中。

Genie Code 现在可以利用已添加到您工作区且您拥有使用权限的任何 MCP 服务器。工作区管理员控制哪些服务器可用，而用户可以根据需要从这些已批准的来源中进行选择。

对于 Google Drive、SharePoint 和 GitHub 等常用工具，Databricks 还提供了托管的 OAuth 流程（目前处于测试阶段），无需手动配置 Token 即可处理身份验证。要启用此功能，请在预览设置中打开“面向 Agent（智能体）的第三方连接器”。之后，任何用户只需点击 Genie Code 提示栏中的加号按钮，即可启用这些 MCP 服务器。

![Image](/images/posts/ece907f50b8c.png)

![Image](/images/posts/fc1578c50c32.png)

MCP 专为那些重要上下文已存在但难以从 Genie Code 访问的情况而设计。例如：

*   **内部文档系统。** 团队通常将操作手册或运维文档保存在 Confluence 等工具中。无需将章节复制到提示词中，这些内容可以被一次性暴露，并在相关时被引用。
*   **内部工具和服务。** 平台团队可能会维护用于设置、验证或部署的 API 或脚本。MCP 允许这些能力直接提供给 Genie Code，而无需反复解释或粘贴。

在这些情况下，MCP 用结构化、可复用的方法取代了手动复制粘贴，使得正确的上下文仅在需要时可用。

![GIF](/images/posts/a4da502f3d47.gif)

## 如何添加 MCP 服务器？

Databricks 支持多种类型的 MCP 服务器，包括用于 Databricks 服务的托管服务器、通过 Unity Catalog 连接的外部服务器，以及托管在 Databricks Apps 上的自定义 MCP 服务器。您可以直接从 Genie Code 设置面板访问的 MCP 市场中浏览可用的服务器。工作区管理员控制哪些服务器可用，用户可以从其拥有使用权限的服务器中进行选择。

一旦 MCP 服务器在您的工作区中可用，在 Genie Code 中使用它们就很简单了：

1.  打开 Genie Code 设置
2.  选择添加服务器
3.  从可用的 MCP 服务器类型中选择
4.  保存您的选择
5.  如果服务器需要身份验证，请按照登录提示授权连接。您的凭据将被安全存储，您无需在每个会话中重新进行身份验证。

MCP 服务器在您添加后立即可用。Genie Code 会在相关时自动访问这些服务器中的工具。

## 提示与技巧

*   **让 Genie Code 为您创建技能。** 在 Agent（智能体）模式下完成一个工作流后，只需告诉 Genie Code 将其捕获为技能；它将自动生成 Markdown 文件并保存到您的技能文件夹中。
*   **保持技能聚焦。** 每个技能文件对应一个工作流，这有助于 Genie Code 判断何时应用，也便于长期维护。名称和描述是 Genie Code 用来决定技能何时相关的依据，因此它们越具体越好。
*   **技能只是 Markdown 文件。** 这意味着它们易于共享、进行版本控制以及在团队中同步。有关可立即使用的入门示例，请参阅 Genie Code 技能演示仓库。
*   **便携式团队约定：** Genie Code 会自动检测工作区中的 `AGENTS.md` 和 `CLAUDE.md` 文件，并在无需额外设置的情况下应用它们。团队可以在不同仓库和开发环境中共享相同的约定、指令和工作流，同时无论在哪里工作，都能保持上下文一致。

## 立即尝试个性化 Genie Code

在 Agent（智能体）模式下使用 Genie Code 时，指令、技能和 MCP 服务器均可用。

要了解更多信息，请查看 Genie Code 的产品文档。

---

> 本文由AI自动翻译，原文链接：[Personalizing Genie Code with instructions, skills, memory, and MCP](https://www.databricks.com/blog/personalizing-genie-code-instructions-skills-memory-and-mcp)
> 
> 翻译时间：2026-06-05 06:22
