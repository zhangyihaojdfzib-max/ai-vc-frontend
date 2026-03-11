---
title: 利用Vega-Lite为多智能体系统注入可视化活力
title_original: Bringing Visualizations to Life in Multi‑Agent Systems With Vega‑Lite
date: '2026-03-10'
source: Databricks Blog
source_url: https://www.databricks.com/blog/bringing-visualizations-life-multi-agent-systems-vega-lite
author: ''
summary: 本文探讨了在多智能体系统中实现跨平台可视化交付的挑战与解决方案。文章指出，尽管智能体能够生成数据洞察，但受限于不同平台（如Microsoft Teams）的视觉语言差异，往往只能输出基础文本表格。为解决此问题，作者提出结合Databricks的Supervisor
  Agent架构、Unity Catalog Functions与Vega-Lite声明式图表规范。该方法允许开发人员集中管理可视化逻辑，生成可移植、对LLM友好的JSON图表规范，使智能体能够在保持上下文一致性的前提下，在各种应用和聊天工具中渲染高质量、受管控的可视化结果，从而将原始数据转化为可操作的视觉洞察。
categories:
- AI基础设施
tags:
- 多智能体系统
- 数据可视化
- Vega-Lite
- Databricks
- AI工程
draft: false
translated_at: '2026-03-11T04:32:24.983244'
---

## 多平台交付中的可视化挑战

您的团队努力构建了一个 Supervisor Agent（监督智能体），能够准确分析第四季度收入并识别增长驱动因素。接下来的挑战在于如何让这些洞察在利益相关者实际工作的平台（例如 Microsoft Teams）上可用。由于每个外部平台都使用独特的视觉语言，集成丰富的图形化答案可能很困难，这常常迫使智能体只能默认使用基本的文本表格。

这正是 Supervisor Agent 固有的灵活性成为显著优势的地方。Databricks 设计的智能体框架支持通过 Unity Catalog Functions 和 Model Context Protocol 等工具进行广泛的自定义。通过利用这些集成以及 Vega-Lite，开发人员可以克服特定平台的限制，创建可移植的高质量可视化。这种方法确保了 Supervisor Agent 能够提供清晰、图形化的洞察，无论目标应用程序是什么，都能保持其上下文和影响力。

## 理解 Supervisor 架构

Agent Bricks 通过一个 Supervisor Agent 来促进生产就绪的 AI，该智能体协调专门的工具来处理多领域查询。在支持的 Databricks 云和区域中，此架构允许监督者智能地委派任务：

- Genie Spaces：处理针对结构化数据的自然语言 SQL 查询。
- Knowledge Assistant agents：执行文档检索和分析（RAG）。
- Unity Catalog Functions：封装自定义业务逻辑。
- Model Context Protocol 服务器：管理第三方集成。

该系统擅长任务分解。对于像“比较各区域第四季度收入”这样的请求，Supervisor 会将定量分析路由给 Genie，同时查询 Knowledge Assistant 以获取上下文文档。

![Multi-Agent System](/images/posts/d8e38f68c7c1.png)

## 通过受管控的可视化扩展多智能体系统

数据智能体需要一种可靠的方法将原始数据转化为可操作的视觉洞察。通过将 Unity Catalog Functions 与 Vega-Lite 结合，开发人员可以生成受管控的、可移植的可视化，智能体可以将其与文本和数据一起返回。

- Unity Catalog Functions：集中管理并管控可视化逻辑，允许智能体调用一个安全、可复用的函数，该函数能从结构化数据生成图表。
- Vega-Lite：使用简洁的 JSON 规范以声明式方式描述图表，允许智能体生成可视化而无需编写命令式的绘图代码。

![Revenue](/images/posts/9dd01895699a.png)

这种方法共同使得智能体能够像返回文本一样轻松地返回受管控的可视化。与命令式图表代码相比，Vega-Lite 还可以降低实现开销，并带来额外的好处：

- 原生 API 且可移植：JSON 规范在 API、应用程序和聊天工具中能保持一致的渲染效果。
- 对 LLM 友好：紧凑的规范通常在有限的上下文窗口中更容易生成和验证。
- 自我验证：基于模式的验证支持快速修正。
- 内置最佳实践：默认设置能自动生成清晰、易于理解的图表。
- 设计安全：声明式的 JSON 避免了生成绘图代码的风险。

## Supervisor 工作流程

Supervisor Agent 协调此过程。它将检索和分析任务委派给子智能体，调用 Unity Catalog 函数进行受管控的后处理，然后组合成最终响应。

### 信息流：

1. 用户查询：“比较各区域第四季度收入，并展示表现最佳的产品。”
2. Supervisor：分解请求并委派给 Genie 和其他相关工具。
3. Supervisor：调用 Unity Catalog 函数，从结构化结果生成 Vega-Lite 规范。
4. Supervisor：将文本、数据和可视化聚合到最终响应中。
5. 客户端：内联渲染 Vega-Lite 规范。

![Information flow](/images/posts/b012517bb824.png)

### 示例 Supervisor 工具调用：

## 通过 Unity Catalog Function 实现

一种稳健的实现策略是使用 Unity Catalog 函数，该函数接受数据和图表要求作为输入，并返回有效的 Vega-Lite 规范。

## 生成器函数

UC 函数充当智能体输出和可视化之间的转换层：

- 验证输入数据（非空 JSON 数组）
- 推断模式（分类字段与定量字段）
- 根据请求选择图表类型（例如：条形图、折线图、散点图）
- 使用编码、维度和工具提示构建 Vega-Lite JSON 规范

## 客户端渲染

最后一步是为用户渲染可视化，这取决于客户端平台。

Web 应用程序：在 JavaScript 中使用 vegaEmbed() 来解析 JSON 规范并在浏览器中渲染交互式图表。

![Client‑side rendering](/images/posts/62427df33909.png)

## 实际用例和收益

金融服务、医疗保健和销售领域的团队正在探索支持 Vega-Lite 的智能体系统，以推动更快、更直观的决策。

### 用例：Teams 中的财务分析仪表板

场景：首席财务官在 Microsoft Teams 中询问：“与预测相比，我们第四季度的表现如何？请按区域和产品类别细分。”

### 多智能体工作流程：

- Supervisor：分解请求并将任务路由给 Genie 智能体和 Unity Catalog Function。
- Genie 执行：智能体 A 返回区域收入数据以及一个带有方差颜色条形的条形图的 Vega-Lite 规范。智能体 B 返回产品类别数据以及一个显示各类别对区域总额贡献的堆叠条形图规范。
- 合成：Supervisor 将这些输入组合成一个连贯的响应，其中包含叙述性洞察和交互式图表。

- 智能体 A 返回区域收入数据以及一个带有方差颜色条形的条形图的 Vega-Lite 规范。
- 智能体 B 返回产品类别数据以及一个显示各类别对区域总额贡献的堆叠条形图规范。

### 结果：

首席财务官直接在 Teams 中收到一个丰富的响应，无需导航到外部仪表板。输出包括关键驱动因素的文本摘要（例如，“第四季度整体超出预测 8%，主要由北部区域增长 15% 和软件类别增长 22% 驱动，而南部区域表现不佳，低于预测 5%”），紧接着是 Vega-Lite 图表。用户可以将鼠标悬停在条形图上，通过工具提示显示精确值，在保持对话上下文的同时实现深度探索。

### 收益：

- 即时清晰度：趋势一目了然，无需从表格中推断。
- 交互式探索：悬停状态和工具提示可按需显示精确值。
- 工作流连续性：洞察保留在 Teams 内部，而非外部 BI 工具。
- 更快的洞察时间：获得可视化答案约需 30 秒，而手动导出、制图和解释则需约 30 分钟。

## 跨用例的示例性收益

以下范围代表了早期试点观察结果，应视为方向性示例，而非通用基准：

![Quantified Benefits: Agent-Generated Visualizations](/images/posts/ae71ea956560.png)

## 结论：在多智能体系统中实现视觉智能

多智能体系统可以分析复杂的查询，但如果没有可视化，它们通常只返回文本和表格。将 Vega-Lite 与 Unity Catalog Functions 结合，使智能体能够生成受管控的、可移植的可视化，这些可视化可以在尊重数据权限的同时跨应用程序渲染。

早期部署表明，当洞察包含可视化时，获得洞察的时间显著缩短，采用率也得到提高。随着多智能体系统成为企业工作流的核心，不仅能够计算答案而且能够展示答案的能力将变得至关重要。

要开始构建，请访问 Agent Bricks 文档，并探索 Unity Catalog Functions 如何改变您的智能体生态系统。

对在您的智能体系统中实现 Vega-Lite 可视化有疑问吗？请加入 Databricks 社区论坛的讨论。

---

> 本文由AI自动翻译，原文链接：[Bringing Visualizations to Life in Multi‑Agent Systems With Vega‑Lite](https://www.databricks.com/blog/bringing-visualizations-life-multi-agent-systems-vega-lite)
> 
> 翻译时间：2026-03-11 04:32
