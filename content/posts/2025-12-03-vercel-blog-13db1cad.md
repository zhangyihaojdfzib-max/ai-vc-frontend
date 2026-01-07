---
title: Remend：自动修复流式Markdown语法的新npm包
title_original: New npm package for automatic recovery of broken streaming markdown
  - Vercel
date: '2025-12-03'
source: Vercel Blog
source_url: https://vercel.com/changelog/new-npm-package-for-automatic-recovery-of-broken-streaming-markdown
author: Hayden Bleasel DX Engineer
summary: 本文介绍了由Vercel推出的独立npm包Remend，它专门用于解决AI模型流式输出Markdown时产生的语法不完整问题。Remend能够智能检测并自动补全未闭合的代码块、粗体/斜体标记、链接或列表等，确保在流式传输过程中获得稳定、可渲染的Markdown内容。该工具最初是Streamdown的一部分，现已独立发布，可与任何Markdown渲染器配合使用，并已在生产环境的AI应用中经过验证，能有效处理各种复杂边缘情况，提升用户体验。
categories:
- AI基础设施
tags:
- Markdown
- 流式处理
- npm包
- AI工具
- 前端开发
draft: false
translated_at: '2026-01-06T14:49:02.042Z'
---

1 分钟阅读
Remend 是一个全新的独立软件包，可为任何应用程序带来智能的不完整 Markdown 处理能力。
它曾是 Streamdown 的 Markdown 终止逻辑的一部分，现在 Remend 已是一个独立的库（npm i remend
），您可以在任何应用程序中使用。
链接到标题为何重要
AI 模型以 Token 为单位流式输出 Markdown，这常常会产生不完整的语法，导致渲染失败。例如：
未闭合的代码块
未完成的粗体/斜体标记
未终止的链接或列表
如果不进行修正，这些模式会导致渲染失败、泄露原始 Markdown 或破坏布局：
**这是粗体文本[点击这里](https://exampl`const foo = "bar
Remend 能自动检测并补全未终止的 Markdown 块，确保在流式输出期间获得干净、稳定的结果。
import remend from "remend";
const partialMarkdown = "This is **bold text";const completed = remend(partialMarkdown);
// 结果: "This is **bold text**"
随着流式输出的继续以及实际的结束标记到达，内容会无缝更新，即使用户正在浏览，也能获得流畅的体验。
它可以作为预处理程序与任何 Markdown 渲染器配合使用。例如：
import remend from "remend";import { unified } from "unified";import remarkParse from "remark-parse";import remarkRehype from "remark-rehype";import rehypeStringify from "rehype-stringify";
const streamedMarkdown = "This is **incomplete bold";
// 首先运行 Remend 以补全不完整的语法const completedMarkdown = remend(streamedMarkdown);
// 然后使用 unified 进行处理const file = await unified() .use(remarkParse) .use(remarkRehype) .use(rehypeStringify) .process(completedMarkdown);
console.log(String(file));
Remend 为 Streamdown 中的 Markdown 渲染提供支持，并已在生产环境的 AI 应用程序中经过实战检验。它包含智能规则以避免误判，并能处理复杂的边缘情况，例如：
LaTeX 块中带下划线的数学表达式
带星号/下划线的产品代码和变量名
带格式标记的列表项
链接中的嵌套括号
要开始使用，您可以通过 Streamdown 使用它，或通过以下命令独立安装：
npm i remend

---

> 本文由AI自动翻译，原文链接：[New npm package for automatic recovery of broken streaming markdown - Vercel](https://vercel.com/changelog/new-npm-package-for-automatic-recovery-of-broken-streaming-markdown)
> 
> 翻译时间：2026-01-06 04:29
