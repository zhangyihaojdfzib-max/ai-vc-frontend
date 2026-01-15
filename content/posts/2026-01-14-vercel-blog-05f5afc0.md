---
title: Vercel发布React最佳实践知识库，专为AI智能体优化
title_original: 'Introducing: React Best Practices - Vercel'
date: '2026-01-14'
source: Vercel Blog
source_url: https://vercel.com/blog/introducing-react-best-practices
author: ''
summary: Vercel基于十余年React与Next.js优化经验，推出专为AI Agent和LLM优化的结构化知识库“react-best-practices”。该知识库系统性地总结了40多条性能优化规则，涵盖消除异步瀑布流、包体积优化、服务器端性能等8个类别，并按影响程度从关键到渐进式排序。其核心主张是优化应从高层级问题（如消除瀑布流、减少包体积）入手，而非过早陷入微观优化。所有规则均源自真实生产代码库的优化实践，并编译为单一文档供AI智能体在代码审查和优化建议时查询使用。
categories:
- AI基础设施
tags:
- React
- 性能优化
- Vercel
- AI Agent
- Next.js
draft: false
translated_at: '2026-01-15T04:44:14.022679'
---

我们将十余年积累的 React 与 Next.js 优化经验，系统性地封装进了 `react-best-practices` 这个专为 AI Agent（智能体）和 LLM（大语言模型）优化的结构化知识库中。

![](/images/posts/581d5b898e27.png)

![](/images/posts/9e39ec7aa671.png)

![](/images/posts/77c522fd3e66.png)

![](/images/posts/a19717c6e897.png)

React 性能优化工作通常是“被动响应式”的。版本发布后，应用感觉变慢了，团队才开始追查各种表象。这种方式成本高昂，且很容易优化错方向。

十多年来，我们在众多生产代码库中反复看到相同的根本原因：

*   意外变成串行执行的异步任务
*   随时间推移不断膨胀的大型客户端包
*   进行了超出必要次数的组件重渲染

意外变成串行执行的异步任务

随时间推移不断膨胀的大型客户端包

进行了超出必要次数的组件重渲染

原因很简单：这些都不是微观层面的优化。它们会直接表现为用户的等待时间、界面卡顿以及影响每次用户会话的重复性成本。

因此，我们整理出这套 React 最佳实践框架，旨在让这些问题更容易被发现、更快速地被修复。

### 核心理念：优化顺序

大多数性能优化工作之所以失败，是因为从技术栈中过低的层级开始了。

如果一个请求瀑布流增加了 600 毫秒的等待时间，那么无论你的 `useMemo` 调用优化得多好都无济于事。如果你在每个页面上都额外加载了 300KB 的 JavaScript，那么在一个循环上节省几微秒也毫无意义。

性能问题还会不断累积。你今天引入的一个小性能衰退，就会成为未来每次用户会话的长期“税负”，直到有人偿还这笔“技术债”。

因此，本框架首先关注通常能真正改善实际指标的两项修复：

1.  消除瀑布流
2.  减少包体积

然后，它才转向服务器端性能、客户端数据获取和重渲染优化。

它涵盖了 8 个类别下的 40 多条规则，按影响程度排序，从**关键**（消除瀑布流、减少包体积）到**渐进式**（高级模式）。

## 内容概览

该知识库涵盖了八个性能优化类别：

*   消除异步瀑布流
*   包体积优化
*   服务器端性能
*   客户端数据获取
*   重渲染优化
*   渲染性能
*   高级模式
*   JavaScript 性能

消除异步瀑布流

包体积优化

服务器端性能

客户端数据获取

重渲染优化

渲染性能

JavaScript 性能

每条规则都包含一个影响评级（从**关键**到**低**），以帮助确定修复的优先级，同时还提供代码示例，展示问题所在及如何修复。

例如，下面是一个常见的阻塞未使用代码的模式：

**错误示例（阻塞了两个分支）：**

```
1async function handleRequest(userId: string, skipProcessing: boolean) {2  const userData = await fetchUserData(userId)3  4  if (skipProcessing) {5    // 立即返回，但仍需等待 userData6    return { skipped: true }7  }8  9  // 只有这个分支使用了 userData10  return processUserData(userData)11}
```

**正确示例（仅在需要时阻塞）：**

```
1async function handleRequest(2  userId: string,3  skipProcessing: boolean4) {5  if (skipProcessing) {6    return { skipped: true }7  }8
9  const userData = await fetchUserData(userId)10  return processUserData(userData)11}12

```

所有独立的规则文件最终会编译成 `AGENTS.md` 这一份单一文档，供你的智能体在审查代码或建议优化时查询。它的设计旨在确保一致性，包括由 AI 智能体执行重构时，以便团队能够在大型代码库中应用相同的决策标准。

## 这些实践是如何收集的

这些并非理论空谈。它们来源于对生产代码库进行的真实性能优化工作。

![](/images/posts/090b60de13f4.png)

![](/images/posts/6af5f90a8a87.png)

**合并循环迭代**

一个聊天页面曾对同一消息列表进行了八次独立的扫描。我们将其合并为单次遍历，当消息数量达到数千条时，这种优化效果显著。

**一个 API 在开始下一个数据库调用前，会等待前一个调用完成，即使它们彼此并不依赖。** 让它们同时运行，将总等待时间减少了一半。

**调整字体回退样式**

在自定义字体加载前使用系统字体时，标题看起来过于紧凑。调整字间距后，回退字体看起来像是精心设计的，而非显示异常。

### 在你的编码智能体中使用 `react-best-practices`

这些最佳实践也被打包成 **Agent Skills**，可安装到 Opencode、Codex、Claude Code、Cursor 及其他编码智能体中。当你的智能体发现级联的 `useEffect` 调用或繁重的客户端导入时，它可以参考这些模式并提出修复建议。

```
1npx add-skill vercel-labs/agent-skills
```

请查看 `react-best-practices` 知识库。

---

> 本文由AI自动翻译，原文链接：[Introducing: React Best Practices - Vercel](https://vercel.com/blog/introducing-react-best-practices)
> 
> 翻译时间：2026-01-15 04:44
