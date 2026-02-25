---
title: 一周内用AI重建Next.js：vinext诞生记
title_original: How we rebuilt Next.js with AI in one week
date: '2026-02-24'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/vinext/
author: ''
summary: 本文介绍了Cloudflare工程师如何在一周内利用AI模型从零开始重建了流行的前端框架Next.js，推出了名为vinext的替代品。vinext基于Vite构建，可直接部署到Cloudflare
  Workers，解决了Next.js在无服务器生态系统中的部署难题。早期基准测试显示，其构建速度提升高达4倍，客户端包体积缩小达57%。文章探讨了Next.js的部署限制、vinext的技术实现及其性能优势，展现了AI在快速软件重构中的潜力。
categories:
- AI产品
tags:
- 前端框架
- AI编程
- Next.js
- Vite
- Cloudflare
draft: false
translated_at: '2026-02-25T04:34:50.914109'
---

# 我们如何在一周内用AI重建了Next.js

2026-02-24

- Steve Faulkner

![](/images/posts/ea055ecd709a.png)

*本文已于太平洋时间下午12:35更新，修正了构建时间基准测试中的一个拼写错误。

上周，一名工程师和一个AI模型从零开始重建了最流行的前端框架。其成果是 **vinext**（发音为"vee-next"），它是 Next.js 的一个直接替代品，基于 **Vite** 构建，可通过单一命令部署到 Cloudflare Workers。在早期基准测试中，它构建生产应用的速度提升了高达4倍，生成的客户端包体积缩小了高达57%。并且我们已经有客户在生产环境中运行它。

整个项目大约花费了价值1100美元的Token。

## Next.js的部署问题

**Next.js** 是最流行的 React 框架。数百万开发者在使用它。它支撑着生产环境中大量网站的运行，这并非没有原因。其开发者体验是一流的。

但是，当在更广泛的无服务器生态系统中使用时，Next.js 存在部署问题。其工具链完全是定制的：Next.js 在 Turbopack 上投入了大量资源，但如果你想将其部署到 Cloudflare、Netlify 或 AWS Lambda，你必须获取其构建输出，并将其重塑为目标平台实际能够运行的东西。

如果你在想："这不就是 OpenNext 做的事情吗？"，你是对的。

这确实是 **OpenNext** 被构建出来要解决的问题。包括我们 Cloudflare 在内的多家供应商，都为 OpenNext 投入了大量的工程努力。它确实有效，但很快就会遇到限制，并变成一场打地鼠游戏。

事实证明，以 Next.js 的输出为基础进行构建是一种困难且脆弱的方法。因为 OpenNext 必须对 Next.js 的构建输出进行逆向工程，这导致版本之间不可预测的变化，需要大量工作来修正。

Next.js 一直在开发一个一流的适配器 API，我们也一直在与他们就此进行合作。这仍处于早期阶段，但即使有了适配器，你仍然是在定制的 Turbopack 工具链上进行构建。而且适配器只覆盖构建和部署。在开发过程中，`next dev` 只能在 Node.js 中运行，无法接入不同的运行时。如果你的应用程序使用了特定平台的 API，如 Durable Objects、KV 或 AI 绑定，在没有变通方案的情况下，你无法在开发环境中测试这些代码。

## 介绍 vinext

如果我们不是去适配 Next.js 的输出，而是直接在 **Vite** 上重新实现 Next.js 的 API 接口会怎样？Vite 是 Next.js 之外大多数前端生态系统使用的构建工具，支撑着 Astro、SvelteKit、Nuxt 和 Remix 等框架。这是一个干净的重实现，而不仅仅是包装器或适配器。老实说，我们当时并不认为这会成功。但现在是2026年，构建软件的成本已经完全改变了。

我们取得的进展远超预期。

```Typescript
npm install vinext
```

在你的脚本中将 `next` 替换为 `vinext`，其他一切保持不变。你现有的 `app/`、`pages/` 和 `next.config.js` 可以照常工作。

```shell
vinext dev          # 带 HMR 的开发服务器
vinext build        # 生产构建
vinext deploy       # 构建并部署到 Cloudflare Workers
```

这不是对 Next.js 和 Turbopack 输出的包装。它是 API 接口的替代实现：路由、服务器端渲染、React 服务器组件、服务器操作、缓存、中间件。所有这些都作为插件构建在 Vite 之上。最重要的是，得益于 **Vite 环境 API**，Vite 的输出可以在任何平台上运行。

## 数据表现

早期基准测试结果令人鼓舞。我们使用一个共享的 33 个路由的 App Router 应用程序，将 vinext 与 Next.js 16 进行了比较。

两个框架执行相同的工作：编译、打包和准备服务器端渲染的路由。我们在 Next.js 的构建中禁用了 TypeScript 类型检查和 ESLint（Vite 在构建期间不运行这些），并使用了 `force-dynamic`，这样 Next.js 就不会花费额外时间预渲染静态路由，否则会不公平地拖慢其速度。目标是仅测量打包器和编译速度，不涉及其他。基准测试在每次合并到主分支时在 GitHub CI 上运行。

生产构建时间：

客户端包大小（gzip压缩后）：

这些基准测试衡量的是编译和打包速度，而不是生产环境下的服务性能。测试装置是一个单一的 33 个路由的应用程序，并不能代表所有生产应用程序。我们预计这些数字会随着三个项目的持续发展而变化。**完整的方法论和历史结果**是公开的。请将它们视为方向性参考，而非最终定论。

不过，这个方向是令人鼓舞的。Vite 的架构，尤其是 **Rolldown**（即将在 Vite 8 中推出的基于 Rust 的打包器），在构建性能方面具有结构性优势，在这里清晰可见。

## 部署到 Cloudflare Workers

vinext 的构建以 Cloudflare Workers 作为首要部署目标。一个命令即可让你从源代码到运行中的 Worker：

```Shell
vinext deploy
```

这会处理所有事情：构建应用程序、自动生成 Worker 配置并部署。App Router 和 Pages Router 都可以在 Workers 上运行，具备完整的客户端水合、交互式组件、客户端导航、React 状态。

对于生产缓存，vinext 包含一个 Cloudflare KV 缓存处理器，让你可以开箱即用地获得 ISR（增量静态再生）：

```Typescript
import { KVCacheHandler } from "vinext/cloudflare";
import { setCacheHandler } from "next/cache";

setCacheHandler(new KVCacheHandler(env.MY_KV_NAMESPACE));
```

**KV** 对于大多数应用程序来说是一个很好的默认选择，但缓存层被设计为可插拔的。那个 `setCacheHandler` 调用意味着你可以换入任何有意义的后端。对于具有大型缓存负载或不同访问模式的应用程序，**R2** 可能更合适。我们也在改进我们的 Cache API，以期提供一个强大且配置更少的缓存层。目标是灵活性：选择适合你应用程序的缓存策略。

当前正在运行的实时示例：

- App Router Playground
- Hacker News 克隆
- App Router 最小示例
- Pages Router 最小示例

App Router Playground

Hacker News 克隆

App Router 最小示例

Pages Router 最小示例

我们还有一个 **实时示例**，展示了 Cloudflare Agents 在 Next.js 应用程序中运行，无需像 `getPlatformProxy` 这样的变通方案，因为整个应用程序现在在开发和部署阶段都运行在 `workerd` 中。这意味着能够毫无妥协地使用 Durable Objects、AI 绑定以及所有其他 Cloudflare 特定服务。**请查看此处**。

## 框架是团队运动

当前的部署目标是 Cloudflare Workers，但这只是冰山一角。vinext 大约 95% 的部分是纯粹的 Vite。路由、模块垫片、SSR 管道、RSC 集成：这些都不是 Cloudflare 特定的。

Cloudflare 希望与其他托管服务提供商合作，为他们的客户采用此工具链（工作量很小——我们在不到30分钟内就在 **Vercel** 上完成了一个概念验证！）。这是一个开源项目，为了其长期成功，我们认为与整个生态系统的合作伙伴合作以确保持续投入非常重要。欢迎来自其他平台的 PR。如果你有兴趣添加部署目标，**请提交问题**或联系我们。

## 状态：实验性

我们想明确说明：vinext 是实验性的。它甚至还不满一周，尚未经过任何有意义的规模化流量实战测试。如果你正在为生产应用程序评估它，请谨慎行事。

尽管如此，测试套件是广泛的：超过 1,700 个 Vitest 测试和 380 个 Playwright E2E 测试，包括直接从 Next.js 测试套件和 OpenNext 的 Cloudflare 一致性套件移植的测试。我们已经针对 Next.js App Router Playground 进行了验证。覆盖了 Next.js 16 API 接口的 94%。

来自真实客户的早期结果令人鼓舞。我们一直与**National Design Studio**团队合作，该团队致力于现代化所有政府界面，我们在他们的一个测试站点**CIO.gov**上进行了合作。他们已经在生产环境中运行vinext，构建时间和打包大小都得到了显著改善。

README诚实地说明了**不支持以及未来也不会支持的功能**，以及**已知的限制**。我们希望开诚布公，而不是过度承诺。

## 关于预渲染呢？

vinext 已经开箱即用地支持**增量静态再生**。在首次请求任何页面后，它会被缓存并在后台重新验证，就像 Next.js 一样。这部分功能现在已经可用。

vinext 目前还不支持在构建时进行静态预渲染。在 Next.js 中，没有动态数据的页面会在 `next build` 过程中被渲染，并作为静态 HTML 提供。如果你有动态路由，你可以使用 `generateStaticParams()` 来枚举需要提前构建的页面。vinext 目前还不支持这个功能。

这是发布时有意为之的设计决策。它**已在路线图上**，但如果你的网站是 100% 预构建的静态内容 HTML，那么今天你可能不会从 vinext 中获得太多好处。话虽如此，如果一位工程师可以花费 **1,100 美元的 Token** 来重建 Next.js，那么你或许可以花费 10 美元迁移到一个专为静态内容设计的、基于 Vite 的框架，比如 **Astro**（它也**可以部署到 Cloudflare Workers**）。

然而，对于那些并非纯静态的网站，我们认为我们可以做得比在构建时预渲染所有内容更好。

## 引入流量感知预渲染

Next.js 会在构建期间预渲染 `generateStaticParams()` 中列出的每个页面。一个拥有 10,000 个产品页面的网站意味着在构建时需要渲染 10,000 次，即使其中 99% 的页面可能永远不会收到请求。构建时间与页面数量成线性增长。这就是为什么大型 Next.js 网站的构建时间最终会达到 30 分钟。

所以我们构建了**流量感知预渲染**。它目前是实验性的，我们计划在获得更多真实世界测试后将其设为默认功能。

想法很简单。Cloudflare 已经是您网站的反向代理。我们拥有您的流量数据。我们知道哪些页面实际上被访问过。因此，vinext 不是在部署时预渲染所有内容或什么都不预渲染，而是查询 Cloudflare 的区域分析数据，只预渲染那些重要的页面。

```javascript
vinext deploy --experimental-tpr

  Building...
  Build complete (4.2s)

  TPR (experimental): Analyzing traffic for my-store.com (last 24h)
  TPR: 12,847 unique paths â 184 pages cover 90% of traffic
  TPR: Pre-rendering 184 pages...
  TPR: Pre-rendered 184 pages in 8.3s â KV cache

  Deploying to Cloudflare Workers...

```

对于一个拥有 100,000 个产品页面的网站，幂律分布意味着 90% 的流量通常流向 50 到 200 个页面。这些页面会在几秒钟内完成预渲染。其他所有内容则回退到按需 SSR，并在首次请求后通过 ISR 进行缓存。每次新的部署都会根据当前的流量模式刷新预渲染页面集。突然爆红的页面会被自动收录。所有这些都无需 `generateStaticParams()`，也无需将构建过程与生产数据库耦合。

## 迎接 Next.js 的挑战，但这次借助 AI

像这样的项目通常需要一个工程师团队花费数月甚至数年的时间。多家公司的多个团队都曾尝试过，其范围之广令人咋舌。我们在 Cloudflare 也曾尝试过一次！两个路由器、33+ 模块垫片、服务器渲染管道、RSC 流式传输、文件系统路由、中间件、缓存、静态导出。没有人成功完成是有原因的。

这次我们在一周内就完成了。一位工程师（实际上是工程经理）指导 AI 完成。

第一次提交是在 2 月 13 日。到当天晚上结束时，Pages Router 和 App Router 都实现了基本的 SSR 功能，同时还有中间件、服务器操作和流式传输。到第二天下午，**App Router Playground** 已经可以渲染 11 个路由中的 10 个。第三天，`vinext deploy` 就能将应用部署到 Cloudflare Workers，并实现完整的客户端水合。接下来的一周是巩固阶段：修复边界情况、扩展测试套件、将 API 覆盖率提高到 94%。

与之前的尝试相比，有什么变化？AI 变得更好了。好得多。

## 为什么这个问题适合用 AI 解决

并非每个项目都会这样进行。这个项目之所以成功，是因为几件事在正确的时间点恰好对齐。

**Next.js 规范明确。** 它拥有详尽的文档、庞大的用户群，以及多年积累的 Stack Overflow 答案和教程。其 API 表面遍布训练数据。当你要求 Claude 实现 `getServerSideProps` 或解释 `useRouter` 的工作原理时，它不会产生幻觉。它知道 Next 是如何工作的。

**Next.js 拥有精细的测试套件。** **Next.js 代码仓库**包含数千个端到端测试，覆盖了每个功能和边界情况。我们直接从他们的测试套件移植了测试（你可以在代码中看到出处）。这为我们提供了一个可以机械验证的规范。

**Vite 是一个优秀的基础。** Vite 处理了前端工具链中最困难的部分：快速的 HMR、原生 ESM、简洁的插件 API、生产环境打包。我们不需要构建一个打包器。我们只需要教会它理解 Next.js。`@vitejs/plugin-rsc` 虽然仍处于早期阶段，但它让我们无需从零开始构建 RSC 实现就获得了 React Server Components 支持。

**模型赶上了。** 我们认为即使在几个月前，这也是不可能的。早期的模型无法在如此规模的代码库中保持连贯性。新模型可以在上下文中把握完整的架构，推理模块之间如何交互，并经常生成正确的代码以保持进展势头。有时，我看到它深入 Next、Vite 和 React 的内部来找出一个 bug。最先进的模型令人印象深刻，而且它们似乎还在不断进步。

所有这些条件必须同时满足：文档齐全的目标 API、全面的测试套件、坚实的底层构建工具，以及一个真正能够处理复杂性的模型。缺少其中任何一个，效果都不会这么好。

## 我们是如何实际构建的

vinext 中几乎每一行代码都是由 AI 编写的。但更重要的是：每一行代码都通过了与人类编写代码相同的质量关卡。该项目拥有 1700+ 个 Vitest 测试、380 个 Playwright 端到端测试、通过 tsgo 进行的完整 TypeScript 类型检查，以及通过 oxlint 进行的代码检查。持续集成在每个拉取请求上运行所有这些检查。建立一套良好的防护措施对于让 AI 在代码库中高效工作至关重要。

这个过程始于一个计划。我花了几个小时在 **OpenCode** 中与 Claude 来回沟通，以定义架构：构建什么、按什么顺序、使用哪些抽象。这个计划成为了北极星。从那里开始，工作流程就很直接了：

1.  定义一个任务（"实现 `next/navigation` 垫片，包含 `usePathname`、`useSearchParams`、`useRouter`"）。
2.  让 AI 编写实现和测试。
3.  运行测试套件。
4.  如果测试通过，合并。如果不通过，将错误输出给 AI，让它迭代。
5.  重复。

我们甚至为代码审查接入了 AI Agent。当打开一个 PR 时，一个 Agent 会审查它。当收到审查意见时，另一个 Agent 会处理它们。反馈循环大部分是自动化的。

它并非每次都完美工作。有些 PR 就是错的。AI 会自信地实现一些看起来正确但与实际 Next.js 行为不符的东西。我必须定期进行纠正。架构决策、优先级排序、判断 AI 何时走入死胡同：这些都是我的工作。当你给 AI 提供良好的方向、良好的上下文和良好的防护措施时，它可以非常高效。但人类仍然需要掌舵。

在浏览器层面测试中，我使用`agent-browser`来验证实际渲染输出、客户端导航和水合行为。单元测试会遗漏许多细微的浏览器问题，而这种方法成功捕捉到了它们。

在整个项目过程中，我们在OpenCode中运行了超过800次会话。总成本：约1100美元的Claude API Token。

## 这对软件意味着什么

为什么我们的技术栈有这么多层？这个项目迫使我深入思考这个问题，并考虑AI如何影响答案。

软件中的大多数抽象存在是因为人类需要帮助。我们无法在脑海中容纳整个系统，因此构建了分层结构来为我们管理复杂性。每一层都让下一个人的工作更轻松。这就是为什么最终会出现框架之上的框架、封装库、数千行胶水代码。

AI没有这种限制。它可以在上下文中容纳整个系统并直接编写代码。它不需要中间框架来保持组织性。它只需要一个规范和一个构建基础。

目前尚不清楚哪些抽象是真正基础性的，哪些只是人类认知的辅助工具。这条界线在未来几年将发生巨大变化。但vinext提供了一个数据点。我们获取了一个API合约、一个构建工具和一个AI模型，然后AI编写了中间的所有代码。不需要中间框架。我们认为这种模式将在许多软件中重复出现。我们多年来构建的层级结构并非都能留存下来。

## 致谢

感谢Vite团队。`Vite`是整个项目的基础。`@vitejs/plugin-rsc`虽处于早期阶段，但它让我获得了RSC支持而无需从头构建，否则这将成为阻碍因素。当我将该插件推入未经测试的领域时，Vite维护者反应迅速且提供了帮助。

我们还要感谢`Next.js`团队。他们花费数年时间构建了一个框架，提高了React开发的标准。他们的API文档如此完善、测试套件如此全面，是该项目得以实现的重要原因。没有他们设定的标准，vinext就不会存在。

## 尝试使用

vinext包含一个`Agent Skill`，可为您处理迁移工作。它兼容Claude Code、OpenCode、Cursor、Codex等数十种AI编码工具。安装后，打开您的Next.js项目并指示AI进行迁移：

```javascript
npx skills add cloudflare/vinext
```

然后在任何支持的工具中打开您的Next.js项目并输入：

```javascript
migrate this project to vinext
```

该技能会处理兼容性检查、依赖安装、配置生成和开发服务器启动。它了解vinext支持的功能，并会标记需要手动处理的内容。

如果您更喜欢手动操作：

```javascript
npx vinext init    # 迁移现有Next.js项目
npx vinext dev     # 启动开发服务器
npx vinext deploy  # 部署到Cloudflare Workers
```

源代码位于github.com/cloudflare/vinext。欢迎提交问题、PR和反馈。

---

> 本文由AI自动翻译，原文链接：[How we rebuilt Next.js with AI in one week](https://blog.cloudflare.com/vinext/)
> 
> 翻译时间：2026-02-25 04:34
