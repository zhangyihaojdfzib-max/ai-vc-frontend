---
title: Streamdown：专为AI流式传输打造的开源Markdown渲染器
title_original: 'Introducing Streamdown: Open source Markdown for AI streaming - Vercel'
date: '2025-08-21'
source: Vercel Blog
source_url: https://vercel.com/changelog/introducing-streamdown
author: ''
summary: Vercel推出开源项目Streamdown，这是一款专为AI流式传输设计的Markdown渲染器。它能够优雅处理未终止的数据块、交互式代码块和数学公式等传统渲染器难以应对的场景。Streamdown内置Tailwind排版样式、GitHub风味Markdown、代码高亮与复制功能，以及LaTeX数学公式支持，同时通过限制外部资源确保安全性。该工具既可作为AI
  Elements的响应组件使用，也能作为独立npm包集成，旨在提升AI应用中的实时内容渲染体验。
categories:
- AI基础设施
tags:
- 开源工具
- Markdown渲染
- AI流式传输
- 前端开发
- Vercel
draft: false
translated_at: '2026-04-03T05:03:56.887028'
---

![](/images/posts/af7c9047a1dc.jpg)

![](/images/posts/dde68f738864.jpg)

Streamdown 是一款全新的开源、即插即用的 Markdown 渲染器，专为 AI 流式传输而构建。它为 AI Elements 的 `Response` 组件提供支持，但也可作为独立包使用，通过 `npm i streamdown` 为开发者提供一个完全可组合、独立管理的选项。

Streamdown 旨在处理未终止的数据块、交互式代码块、数学公式以及其他现有 Markdown 包处理不可靠的情况。

它现已发布，并内置以下功能：

*   **Tailwind 排版样式**：为标题、列表和代码块预配置的类
*   **GitHub Flavored Markdown**：表格、任务列表及其他 GFM 功能
*   **交互式代码块**：使用 Shiki 高亮，并内置复制按钮
*   **数学公式支持**：通过 `remark-math` 和 KaTeX 支持 LaTeX 表达式
*   **优雅的数据块处理**：为未终止的 Markdown 数据块提供正确的格式化
*   **安全加固**：通过限制图片和链接，安全处理不受信任的内容

您可以通过 AI Elements 开始使用：

```
1npx ai-elements@latest add message
```

或作为独立包使用：

```
1npm i streamdown
```

阅读文档，升级您的 AI 驱动流式体验。

---

> 本文由AI自动翻译，原文链接：[Introducing Streamdown: Open source Markdown for AI streaming - Vercel](https://vercel.com/changelog/introducing-streamdown)
> 
> 翻译时间：2026-04-03 05:03
