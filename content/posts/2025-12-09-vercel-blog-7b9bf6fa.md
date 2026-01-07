---
title: Workflow DevKit框架集成原理：一次编写，多端生成
title_original: 'Inside Workflow DevKit: How framework integrations work - Vercel'
date: '2025-12-09'
source: Vercel Blog
source_url: https://vercel.com/blog/inside-workflow-devkit-how-framework-integrations-work
author: Adrian Lam Software Engineer
summary: 本文深入解析了Vercel Workflow Development Kit（WDK）如何实现与多种框架的无缝集成。其核心在于统一的两阶段模式：构建时将工作流代码编译为处理器文件，运行时自动将其暴露为HTTP端点。WDK的SWC编译器插件通过三种转换模式（客户端、步骤、工作流），将同一份源代码自动生成适配不同环境的代码，实现了“一次编写，多端运行”。文章以SvelteKit为例，具体说明了该集成模式在基于Vite的框架中的实践过程。
categories:
- AI基础设施
tags:
- Vercel
- Workflow DevKit
- 框架集成
- 编译器
- 无服务器
draft: false
translated_at: '2026-01-06T01:21:17.350Z'
---

5 分钟阅读
一个多月前，我们在 Ship AI 发布 Workflow Development Kit（WDK）时，希望它能体现我们的 Open SDK 战略，让开发者能够使用任何框架进行构建，并部署到任何平台。

发布之初，WDK 支持 Next.js 和 Nitro。如今，它已能与八个框架协同工作，包括 SvelteKit、Astro、Express 和 Hono，而 TanStack Start 和 React Router 的集成也正在积极开发中。本文将解释这些集成背后的模式及其底层工作原理。

### 每个 WDK 集成背后的模式

从表面上看，将 WDK 与 Next.js 集成，看起来与将其集成到 Express 或 SvelteKit 中完全不同。它们拥有不同的打包工具、路由系统和开发者体验。但在核心层面，每个框架的集成都遵循相同的两阶段模式。

### 构建时：生成工作流处理器

构建时阶段会将您的工作流和步骤函数编译成可执行的处理器文件。它负责打包、确定文件输出位置，并应用任何框架特定的兼容性补丁。此阶段还配置了热模块替换功能，因此开发者无需重启开发服务器即可即时看到工作流的更改。

### 运行时：将处理器暴露为端点

运行时阶段会应用工作流客户端转换，并使构建时阶段生成的处理器文件能够被应用程序的服务器访问。您的工作流无需任何手动端点配置即可通过 HTTP 访问。

这些处理器如何作为端点暴露，在不同框架间差异很大，但过程始终相同。

### WDK 的三种转换模式如何工作

魔法发生在 WDK 的 SWC 编译器插件中，该插件根据模式将同一个输入文件转换为三种不同的输出。

*   **客户端模式** 通过 Rollup 或 Vite 插件在您框架的构建过程中运行。它将工作流调用转换为 HTTP 客户端代码，并添加 `workflowId` 属性。
*   **步骤模式** 在 WDK 的 esbuild 阶段运行。它将 `"use step"` 函数转换为在服务器上执行您步骤逻辑的 HTTP 处理器。
*   **工作流模式** 同样在 esbuild 阶段运行。它将 `"use workflow"` 函数转换为在沙盒化虚拟环境中运行的编排器。

这意味着您只需编写一次代码，编译器就会自动生成客户端、步骤处理器和工作流处理器。

**自定义 Workflow DevKit 框架集成**
按照深入指南创建您自己的 Workflow DevKit 框架集成。
[了解更多]()

### 实践中的模式：SvelteKit

为了展示其工作原理，让我们看看 SvelteKit 的集成。SvelteKit 是一个构建在 Vite 之上、采用基于文件路由的框架。在 SvelteKit 应用中设置 WDK 只需一行代码。

```javascript
import { sveltekit } from "@sveltejs/kit/vite";
import { workflowPlugin } from "workflow/sveltekit";

export default {
  plugins: [sveltekit(), workflowPlugin()]
};
```

就这样！在幕后，`workflowPlugin()` 实现了两个阶段：

#### 构建时

两件事并行发生。

1.  **客户端转换（Vite + Rollup）**：来自 `@workflow/rollup` 的 `workflowTransformPlugin()` 钩入 Vite 的构建过程，并在您调用 `start(myWorkflow, [...])` 时，使用 `mode: 'client'` 的 SWC 来转换您的导入，为工作流添加 `id` 属性。
2.  **处理器生成（esbuild）**：`SvelteKitBuilder` 创建两个包（一个用于步骤，`mode: 'step'`；一个用于工作流，`mode: 'workflow'`）。它们成为 `src/routes/.well-known/workflow/v1` 目录下的 `+server.js` 文件。

#### 运行时

SvelteKit 的基于文件路由会自动发现这些生成的文件，并将它们暴露为 HTTP 端点，只要文件名为 `+server.js`。无需手动连接。

这种基于插件的方法在许多基于 Vite 的框架中都适用。例如，Astro 的集成几乎完全相同，因为它们共享 Vite 的插件系统、热模块替换和基于文件的路由。主要区别在于路由的输出位置以及需要哪些框架特定的补丁来实现兼容性。

对于像 Express 或 Hono 这样没有打包工具的框架，我们改用 Nitro。Nitro 是一个服务器工具包，提供基于文件的路由、构建系统以及其他便利功能，例如可以在运行时挂载到服务器的虚拟处理器。这为裸 HTTP 服务器带来了相同的工作流能力。

### 为何需要转换框架请求对象

在创建多个框架集成时出现的一个挑战是，不同框架对于“请求”对象的形态有不同的看法。SvelteKit 向路由处理器传递一个自定义的请求对象，但我们的工作流处理器期望的是标准的 Web Request API。

我们通过向每个生成的处理器中注入一个小的转换函数来解决这个问题。

```javascript
async function convertSvelteKitRequest(request) {
  const options = {
    method: request.method,
    headers: new Headers(request.headers)
  };
  if (!['GET', 'HEAD'].includes(request.method)) {
    options.body = await request.arrayBuffer();
  };
  return new Request(request.url, options);
};
```

这个辅助函数被注入到每个工作流处理器文件中，以兼容 SvelteKit。

### 热模块替换

为了确保开发者能够快速迭代并达到理想效果，工作流必须支持热模块替换，允许开发者更改工作流并看到即时反馈，而无需重启开发服务器。

当您在 SvelteKit 中保存一个工作流文件时，会发生三件事：

1.  Vite 的 `hotUpdate` 钩子触发，并传入已更改的文件。
2.  我们检查是否存在 `"use workflow"` 或 `"use step"` 指令。
3.  如果找到，则触发 esbuild 重新构建。

```javascript
async hotUpdate({ file, read }) {
  const content = await read();

  const useWorkflowPattern = /^\s*(['"])use workflow\1;?\s*$/m;
  const useStepPattern = /^\s*(['"])use step\1;?\s*$/m;

  if (!useWorkflowPattern.test(content) && !useStepPattern.test(content)) {
    return; // 不是工作流文件，让 Vite 正常处理
  }

  await enqueue(() => builder.build()); // 使用 esbuild 排队重建：如果发生并发构建，这一点很重要
};
```

一个基于 Vite 框架中 Workflow DevKit HMR 的最小示例。

### 跨框架扩展该模式

构建多个集成后发现，框架可分为两类。

#### 基于文件路由的框架（Next.js, SvelteKit, Nuxt）

这些框架使集成变得直接。构建时阶段将工作流处理器文件输出到框架特定的目录（Next.js 是 `app/.well-known/workflow/v1`，SvelteKit 是 `src/routes/.well-known/workflow/v1`），框架会自动将它们发现为 HTTP 端点。无需手动连接，尽管每个框架在端点的定义和处理方式上需要不同的补丁。

#### HTTP 服务器框架（Express, Hono）

这些框架不附带构建系统，即它们没有打包工具，只暴露一个裸 HTTP 服务器。这就是 Nitro 的用武之地。对于这些框架，WDK 使用 esbuild 来打包工作流，然后 Nitro 将它们作为虚拟处理器挂载。在运行时，Nitro 包装您的 HTTP 服务器并注入虚拟处理器，暴露工作流端点，使其可以从您的 HTTP 服务器访问。

许多现代框架都构建在 Vite 之上（SvelteKit, Astro, Nuxt）。这意味着在插件注册、HMR 配置和客户端转换方面，大部分集成代码几乎是相同的。我们构建了一次核心的 Vite 集成，然后针对每个框架的特定路由模式进行了调整。

### 向所有框架开放工作流

构建这些集成揭示了框架选择如何可能为采用设置不必要的障碍。每一次集成都为 WDK 打开了一个完整的开发者社区，这些社区已经致力于他们选择的框架。

仅 SvelteKit 集成一项，就将工作流带给了数千名已经在该生态系统中构建的开发者。

与其强迫团队为了持久性而迁移到另一个框架，他们只需在配置文件中添加一行代码，就能将其集成到现有技术栈中。

与社区合作开发 Express、Hono 和 Astro 的集成强化了这一理念。开发者希望在他们偏好的环境中使用工作流，而不是将其作为切换环境的理由。

### 模式依然成立

自发布以来，Workflow DevKit 已在 GitHub 上获得了超过 1,300 颗星，开发者们正在所有这些框架中构建工作流。构建另外六个框架集成的过程证明了良好的抽象如何揭示模式。看似六个不同的问题，实际上是用六种不同方式解决的同一个问题。

核心模式在不同的框架中保持一致：在构建时生成工作流处理器，在运行时将这些处理器注册为 HTTP 端点。只有实现细节会因一些框架层面的特性而略有不同。

随着我们继续扩展框架支持，这一模式依然成立。对于开发者而言，这意味着他们可以将持久化工作流引入他们正在使用的任何框架。

我们开发 Workflow DevKit 的目标是让持久性成为整个生态系统中的一个语言级概念。通过这些集成，我们离这个目标更近了一步。

### 开始使用 Workflow DevKit

使用熟悉的 JavaScript 构建能够跨部署和崩溃持久运行的工作流。无需队列、调度器或额外的基础设施。

[开始使用](https://example.com)。

---

> 本文由AI自动翻译，原文链接：[Inside Workflow DevKit: How framework integrations work - Vercel](https://vercel.com/blog/inside-workflow-devkit-how-framework-integrations-work)
> 
> 翻译时间：2026-01-06 01:21
