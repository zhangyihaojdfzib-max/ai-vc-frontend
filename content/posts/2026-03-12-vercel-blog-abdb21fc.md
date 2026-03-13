---
title: AI Elements 1.9 发布：新增组件、智能体技能与错误修复
title_original: AI Elements 1.9 is now available - Vercel
date: '2026-03-12'
source: Vercel Blog
source_url: https://vercel.com/changelog/ai-elements-1-9
author: ''
summary: AI Elements 1.9 版本正式发布，主要引入了三项重要更新。首先，新增了AI Elements技能，可安装到用户首选的智能体（Agent）中，使其更好地理解如何构建和使用可组合的AI界面。其次，推出了新的<JSXPreview
  />组件，能够动态渲染JSX字符串，并支持在JSX可能不完整的流式传输场景中自动关闭未闭合标签，非常适合实时显示AI生成的UI。此外，还为<PromptInput
  />组件新增了一个子组件，可以捕获当前页面截图，有助于向AI模型提供视觉反馈。最后，<Conversation />组件现在包含一个可选按钮，支持将对话下载为Markdown文件。本次更新还对整个库进行了一轮错误修复。
categories:
- AI产品
tags:
- AI组件库
- 前端开发
- Vercel
- 智能体
- UI生成
draft: false
translated_at: '2026-03-13T05:02:45.162809'
---

![](/images/posts/84f73ada9895.jpg)

AI Elements 1.9 版本新增了组件、一项 Agent（智能体）技能，并对整个库进行了一轮错误修复。

AI Elements 技能

您现在可以将 AI Elements 技能安装到您首选的 Agent（智能体）中，使其更好地理解如何构建和使用可组合的 AI 界面。

```
1npx skills add vercel/ai-elements
```

<JSXPreview />

新的 `<JSXPreview />` 组件可以动态渲染 JSX 字符串，支持 JSX 可能不完整的流式传输场景。它会在流式传输过程中自动关闭未闭合的标签，非常适合实时显示 AI 生成的 UI。

```
1npx ai-elements@latest add jsx-preview
```

<PromptInputActionAddScreenshot />

一个新的 `<PromptInput />` 子组件，可以捕获当前页面的屏幕截图，有助于向 AI 模型提供视觉反馈。

```
1npx ai-elements@latest add prompt-input
```

下载对话

`<Conversation />` 组件现在包含一个可选按钮，可以将对话下载为 Markdown 文件。

阅读[文档](documentation)以开始使用。

---

> 本文由AI自动翻译，原文链接：[AI Elements 1.9 is now available - Vercel](https://vercel.com/changelog/ai-elements-1-9)
> 
> 翻译时间：2026-03-13 05:02
