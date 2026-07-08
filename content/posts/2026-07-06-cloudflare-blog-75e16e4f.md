---
title: Worker 前端缓存：一行配置即可启用
title_original: Your Worker can now have its own cache in front of it
date: '2026-07-06'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/workers-cache/
author: ''
summary: Cloudflare 推出 Workers Cache，允许在 Worker 前端配置分层缓存。通过简单的 Wrangler 配置和 Cache-Control
  标头，可缓存请求将直接由缓存响应，避免 Worker 运行和 CPU 消耗。支持 stale-while-revalidate、内容协商、多租户安全缓存键及程序化清除。缓存可跟随
  Worker 部署到任何入口点，无需额外配置区域或规则引擎。
categories:
- AI基础设施
tags:
- Cloudflare
- Workers Cache
- 边缘计算
- 缓存策略
- 服务端渲染
draft: false
translated_at: '2026-07-08T05:26:13.989963'
---

# 你的 Worker 现在可以在前面拥有自己的缓存

2026-07-06

- Dan Lapid
- Connor Harwood

![](/images/posts/7cfd6cd93935.png)

今天，我们推出了 Workers Cache：一个位于你的 Worker 前面的分层缓存，通过一行 Wrangler 配置和你已经熟悉的 Cache-Control 标头即可配置。

当 Workers Cache 启用时，每个对你的 Worker 的可缓存请求都会首先命中 Cloudflare 的缓存。如果存在新鲜的缓存响应，Cloudflare 会直接返回它——你的 Worker 不会运行，你也不需要为此支付 CPU 时间。如果缓存未命中，你的 Worker 会运行，并且如果你的响应是可缓存的，Cloudflare 会将其存储起来供下一个请求使用。来自地球上任何地方的下一个请求都可以直接从缓存中提供服务。

整个配置就是一个代码块：

```Rust
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2026-05-01",
  "cache": {
    "enabled": true
  }
}
```

之后，你可以通过 HTTP 一直以来期望的方式控制缓存——在你的响应上设置标头：

```TypeScript
return new Response(body, {
  headers: {
    "Cache-Control": "public, max-age=300, stale-while-revalidate=3600",
    "Cache-Tag": "products,product:123",
  },
});
```

当内容发生变化时，你的 Worker 会清除自己的缓存：

```TypeScript
await ctx.cache.purge({ tags: ["product:123"] });
```

这就是整个 API。无需配置区域，无需设置规则引擎，无需预置单独的缓存，也无需登录第二个产品。Worker 的代码就是配置界面，缓存会跟随 Worker 运行到任何地方——在自定义域名上、在 workers.dev 上、在服务绑定后面、在预览中、在 Workers for Platforms 租户中。一个 Worker，一个缓存，一次配置。

这就是表面部分。底层还有很多内容：跨整个网络的分层缓存、对 stale-while-revalidate 的完整支持（这样过期的响应永远不会阻塞用户）、通过 Vary 进行的内容协商、通过 ctx.props 实现的多租户安全缓存键、按标签或路径前缀进行的程序化清除，以及——我们认为最大的突破——一个位于每个 Worker 入口点（不仅仅是公共入口点）前面的缓存，并且可以按入口点控制哪些进行缓存，哪些不进行缓存。最后这一点意味着你可以将缓存直接组合到你的应用结构中：一个由入口点组成的链，缓存阶段可以插入到你想要的任何位置，由两侧的代码进行配置。我们将在下面详细介绍所有这些内容。

Workers Cache 现在对所有计划中的每个 Worker 都可用，在 Wrangler 中启用。

这是我们一直希望 Workers 拥有的缓存 API。以下是为什么花了这么长时间、它带来了哪些可能性，以及接下来会发生什么。

## 为什么服务端渲染的应用需要在前面有一个缓存

当我们在 2017 年推出 Workers 时，其宣传点是你可以通过 Cloudflare 网络运行代码，在请求到达你的源站之前对其进行转换。Worker 位于缓存和源站的前面：

这是我们当时针对的用例的正确模型。如果你想在每个请求中添加一个标头、重写 URL、进行 A/B 分流或在流量到达源站之前过滤流量，将 Worker 放在缓存和源站前面可以让你完全控制哪些内容被缓存，哪些不被缓存。客户用它构建了令人难以置信的东西。

但世界已经改变。Workers 不再是你附加到源站上的东西，而是成为了源站本身。像 Astro、TanStack Start、Next.js、Remix 和 SvelteKit 这样的框架都提供了 Cloudflare 适配器，可以将你的应用构建为一个 Worker。它们后面没有源站。Worker 就是服务器。

当 Worker 是源站时，原始架构就没有什么可以缓存的了。每个请求都会运行你的代码，即使响应与一秒前返回的响应逐字节相同。Workers 运行时足够快，这可以工作——它通常每秒处理数千万个请求而毫不费力——但"足够快以渲染每个请求"仍然会让你在每个页面加载时付出延迟成本，并在每次调用时付出 CPU 时间成本。而在一个服务端渲染的应用上，每个页面加载本质上都是一次渲染。

Workers Cache 翻转了架构。Cloudflare 的缓存现在位于 Worker 的前面：

缓存命中时，你的 Worker 根本不会运行。Cloudflare 返回缓存的响应，你的 CPU 计费保持为零。缓存未命中时，你的 Worker 运行一次，填充缓存，然后下一个请求——来自任何地方——都会从缓存中提供服务，而无需调用你的代码。

这就是 Workers 上服务端渲染所缺少的东西。过去你不得不在两个不尽人意的选项之间做出选择：

- 在构建时预渲染所有内容（"静态站点生成"）。页面加载速度快，但每次更改都需要完全重建和重新部署。对于一个有几千页的文档站点，这需要 5-10 分钟。对于一个大型电商网站，情况更糟——而且每次你修改任何内容时，构建都会运行。
- 在每个请求上渲染每个页面。内容是最新的，但每个页面加载都要付出渲染成本，每个访问者都要付出延迟成本。

Workers Cache 为你提供了第三个选项：按需服务端渲染，缓存渲染后的响应，在你选择的生存时间（TTL）后刷新它。对新页面的第一个请求仍然会渲染。之后的每个请求，直到缓存过期，都会像页面是静态的一样被提供服务。当缓存过期时，下一个请求会触发重新渲染——而通过 stale-while-revalidate，即使是那个请求也不需要等待。

你获得了静态站点的速度，而无需构建时间；你获得了服务端渲染的新鲜度，而无需成本。没有像增量静态再生这样的框架特定机制。只有 HTTP 缓存，按照它设计的方式工作，位于被设计为源站的代码前面。

## stale-while-revalidate 是让它感觉瞬间完成的关键部分

stale-while-revalidate 指令告诉 Cloudflare，当缓存的响应过期时，允许立即提供过期的副本，同时在后台刷新响应。Cloudflare 在今年早些时候推出了对 stale-while-revalidate 的完整支持，正是这个指令将"我们缓存你的 Worker"变成了"你 Worker 的站点感觉像静态站点"。

没有它，缓存条目过期后的第一个请求必须等待 Worker 从头开始渲染页面。用户会看到那个延迟。有了它，过期后的第一个请求会立即获得过期的页面（带有 Cf-Cache-Status: UPDATING 标头），而 Worker 在后台运行以重新填充缓存。每个用户，包括触发刷新的那个用户，都会获得缓存速度的响应。

在实践中，这看起来像：

```TypeScript
 export default {
  async fetch(request) {
    const html = await renderPage(request);
    return new Response(html, {
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        // 在 5 分钟内视为新鲜；在后台刷新运行时，
        // 最多提供过期内容一小时。
        "Cache-Control": "public, max-age=300, stale-while-revalidate=3600",
      },
    });
  },
};
```

让这一点变得清晰的心智模型：

- 新鲜窗口（max-age）：Cloudflare 提供缓存的响应。你的 Worker 不运行。
- 过期窗口（stale-while-revalidate）：Cloudflare 提供缓存的响应。你的 Worker 在后台运行以刷新它。没有用户等待。
- 两个窗口之外：Cloudflare 运行你的 Worker 以生成新鲜响应，用户等待那一次渲染。

**陈旧窗口（stale-while-revalidate）**：Cloudflare 提供缓存的响应。您的 Worker 在后台运行以刷新该响应。用户无需等待。

**两个窗口之外**：Cloudflare 运行您的 Worker 以生成新的响应，用户等待该次渲染。

您可以选择窗口大小。对于一个每隔几分钟更新的产品目录，`max-age=300, stale-while-revalidate=3600` 意味着访问者基本无需等待，同时您的 Worker 仍能以足够频繁的频率运行以保持内容新鲜。对于一个几乎从不更改的博客存档，`max-age=86400, stale-while-revalidate=2592000` 意味着您的 Worker 每天为每个页面运行一次。

对全新页面的首次请求是唯一需要承担完整渲染成本的请求。此后，该页面对于访问者而言表现得像静态输出，而您的 Worker 仍然掌控着页面的生成方式。

## 一个URL，多种表示：`Vary` 的作用

真实的应用程序很少向每个客户端返回相同的字节。同一个产品页面，对于浏览器可能是 HTML，对于 API 客户端可能是 JSON。同一张图片，对于支持的客户端可能是 WebP 格式，对于不支持的可能是 JPEG 格式。同一个主页，可能根据用户返回英文、法文或日文版本。

在没有缓存的情况下做到这一点很容易——您的 Worker 只需读取请求头并返回正确的内容。但在有缓存的情况下做到这一点通常会变得棘手。大多数缓存会提供两个糟糕的选择：要么不缓存具有多种表示的 URL，要么缓存一种表示并将其提供给所有用户。

Workers Cache 支持标准的 HTTP `Vary` 头，这是解决此问题的正确方法。当您的 Worker 返回一个带有 `Vary: Accept-Encoding`（或 `Accept`，或 `Accept-Language`，或任何其他请求头）的响应时，Cloudflare 会为这些头的每种不同组合存储一个单独的缓存变体——并且仅当存储的值与传入请求匹配时才返回该变体。

```TypeScript
export default {
  async fetch(request) {
    const accept = request.headers.get("Accept") ?? "";
    const wantsWebp = accept.includes("image/webp");

    const body = wantsWebp ? await fetchWebpImage() : await fetchJpegImage();

    return new Response(body, {
      headers: {
        "Content-Type": wantsWebp ? "image/webp" : "image/jpeg",
        "Cache-Control": "public, max-age=3600",
        // 为每个不同的 Accept 头值缓存一个单独的变体。
        Vary: "Accept",
      },
    });
  },
};
```

一个 URL，两个缓存的变体。发送 `Accept: image/webp,*/*` 的浏览器获取 WebP 格式。发送 `Accept: image/jpeg` 的浏览器获取 JPEG 格式。两者都来自缓存。您的 Worker 在首次请求每个变体时写入它们，之后对两者都不再运行。

这是经过充分实践的内容协商 HTTP 标准，Workers Cache 按照 [RFC 9110](https://httpwg.org/specs/rfc9110.html) 和 [RFC 9111](https://httpwg.org/specs/rfc9111.html) 的描述实现了它。对于您可以在 `Vary` 上使用的头，没有允许列表。您列出任何需要的头，Cloudflare 会根据这些头的逐字值来键控变体。文档详细介绍了[边缘情况](https://developers.cloudflare.com/workers/cache/)——如何通过在一个网关 Worker 中规范化头来控制变体数量膨胀，为什么清除操作会一起使一个 URL 的所有变体失效，以及完全禁用缓存的唯一情况（`Vary: *`）。

## 这是您 Worker 的缓存，而非您域名的缓存

在我们讨论这一切能实现什么之前，有一个值得指出的概念性转变。

Cloudflare 一直都有缓存。它是在域名级别配置的：缓存规则、页面规则、缓存文件扩展名列表、缓存预留、分层缓存拓扑、自定义缓存键。所有这些都是在每个域名下设置的，并且历史上 Worker 要么必须适应那个域名的配置，要么绕过它。

Workers Cache 则不同。它是**您 Worker 的缓存**——它属于 Worker，而非域名。这带来了一系列重要的后果：

- **无需管理域名配置。** 缓存规则、缓存级别设置、文件扩展名列表、页面规则——这些都不适用于 Workers Cache。Worker 的 `Cache-Control` 头就是配置。
- **缓存跟随 Worker，而非主机名。** 一个绑定到 `api.example.com`、`api.example.net` 并通过服务绑定调用的 Worker，会在三者之间共享一个缓存。对 `/users/42` 的请求，无论从哪个入口进来，都会命中同一个缓存条目。
- **缓存在 `workers.dev` 上有效。** 它在**预览 URL** 中有效（每个预览都有自己的缓存，因此测试更改不会污染生产环境）。它在 **Workers for Platforms** 中有效（每个用户 Worker 都有自己的缓存，与调度器和其他租户隔离）。所有这些过去在缓存方面都是二等公民。现在不再是了。
- **清除操作限定在 Worker 的入口点范围内。** 当您调用 `ctx.cache.purge({ purgeEverything: true })` 时，您只清除了您 Worker 入口点的缓存。没有破坏您域名其他内容的风险。没有某个 Worker 的部署使另一个 Worker 数据失效的风险。

关于缓存的配置，您都在代码中完成：哪些路径需要更长的 TTL（根据路径分支并设置不同的 `max-age`），哪些请求绕过缓存（返回 `Cache-Control: private`），如何构建缓存键（控制进入 `ctx.props` 的内容，在分派前在网关 Worker 中规范化 URL）。您已经编写的 Worker 就是配置界面。

完整文档在 [Workers Cache: your Worker's cache](https://developers.cloudflare.com/workers/cache/) 中对此进行了深入探讨。

## 两层缓存，每个 Worker，无需配置

Workers Cache 默认是**区域分层**的。它有两层：

- **下层缓存**位于离用户最近的 Cloudflare 数据中心。每个为您的 Worker 处理流量的数据中心都有自己的下层缓存。
- **上层缓存**在整个网络中聚合填充。这类数据中心数量较少，每个下层缓存未命中时会向上层缓存查询。

请求首先命中下层缓存。如果命中，则直接提供响应，流程结束。如果未命中，下层缓存会向上层缓存查询。如果在上层缓存命中，则返回响应，并在返回过程中也存储在下层缓存中。只有当两层都未命中时，您的 Worker 才会实际运行——并且这次运行的响应会同时存储在这两层中。

这之所以重要，是因为**世界任何地方的首次请求**都会填充上层缓存。此后，来自任何数据中心的每个后续请求都可以从上层缓存提供服务，而无需运行您的 Worker——即使该数据中心的下层缓存之前从未见过该请求。缓存命中率将远高于使用单个平面缓存层的情况，而这正是当您的 Worker 作为源站时所需要的。

这与当前为区域提供支持的**分层缓存**拓扑结构相同，区别在于你无需手动配置。没有“为我的 Worker 开启分层缓存”的对话框。每个启用了缓存的 Worker 都会自动获得分层缓存功能。

如果你的 Worker 使用了**智能部署**，缓存会与其完美配合：首先检查分层缓存，只有当两者都未命中时，智能部署才会将执行路由到靠近你的源站。关于这些层如何交互，包括我们计划在未来文档中修复的一些粗糙边缘，我们还有更多内容要说明。

## 在靠近用户**和**靠近数据的位置运行应用

Web 性能中有一个反复出现的难题，至今无人完全解决：你希望代码在靠近用户的位置运行（因为用户与服务器之间的往返处于关键路径上），同时又希望代码在靠近数据的位置运行（因为每次数据库查询也是一次往返）。选择其一，另一个就会变慢。

我们多年来一直在追求两者兼顾。我们的网络使我们可以覆盖全球约 95% 的互联网用户，距离在 50 英里以内。**智能部署**和**部署提示**让你无需考虑云区域，就能将代码保持在靠近数据的位置。但在此之前，这两部分并未完全协同。你可以选择“靠近用户”或“靠近数据”，而如果你希望应用的两个部分同时位于正确的位置，你必须成为 Cloudflare 专家。我们知道我们可以做得更好。

**Workers 缓存**正是弥补这一差距的关键。由于缓存属于 Worker（而非区域），并且由于 Worker 之间的**服务绑定**和 `ctx.exports` 调用会经过缓存，你可以将应用构建为一个 Worker 链——每个 Worker 在其应在的位置运行——而缓存则是它们之间的连接点。

架构如下所示：

- **Worker A** 在靠近用户的位置运行。它处理每个请求中廉价且对延迟敏感的部分：身份验证、速率限制、路由、请求头标准化、渲染不依赖数据的 HTML 页面“外壳”。
- **Worker B** 在靠近数据的位置运行，借助智能部署或显式的部署提示。它执行繁重的工作：服务端渲染需要获取数据的页面、读取产品目录、生成搜索结果、聚合 API、执行昂贵的转换。
- **Workers 缓存**位于 Worker B 之前。当 Worker A 通过服务绑定调用 Worker B 时，Cloudflare 会首先检查 Worker B 的缓存。如果命中，Worker A 直接接收响应，Worker B 完全不运行——无需数据中心跳转、无需数据库查询、无需渲染工作。

缓存命中的路径变为：用户 → 靠近用户的 Worker A → Worker B 缓存命中 → 响应。仅在未命中时才需要数据跳转。你的热门页面以“用户端代码”的速度运行，而冷门页面在执行时仍能从靠近数据运行中受益。

你无需进行任何特殊架构设计即可实现这一点。将你的应用编写为两个 Worker，通过服务绑定将一个指向另一个，在 Worker B 的 `wrangler.jsonc` 文件中开启缓存，即可完成。

## 默认多租户，配合 `ctx.props`

如果你正在缓存一个返回用户特定数据的 Worker——例如，一个为不同登录用户提供不同内容的 API——你需要一种方法来确保一个用户永远不会看到另一个用户的缓存响应。标准的解决方案是“不缓存经过身份验证的请求”，Cloudflare 对 `Authorization` 请求头的自动绕过正是这样做的。但“什么都不缓存”会放弃全部性能优势。

**Workers 缓存**通过将调用方的 `ctx.props` 作为缓存键的一部分来解决这个问题。当一个 Worker 通过服务绑定调用另一个 Worker 并传递包含用户 ID、租户 ID 或任何其他标识符的 `ctx.props` 时，具有不同 props 的调用方将获得独立的缓存条目。一个用户的响应永远不会泄露到另一个用户的缓存中。

```typescript
import { WorkerEntrypoint } from "cloudflare:workers";

interface Props { userId: string; }

export default class Backend extends WorkerEntrypoint<Env, Props> {
  async fetch(request: Request): Promise<Response> {
    // ctx.props.userId 是缓存键的一部分。用户 A 和用户 B
    // 请求相同的 URL 会获得独立的缓存条目。
    const { userId } = this.ctx.props;
    const data = await loadUserData(userId);

    return new Response(JSON.stringify(data), {
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "public, max-age=300",
      },
    });
  }
}
```

典型的模式是在网关 Worker 中验证请求，剥离 `Authorization` 请求头，将已验证用户的 ID 设置到 `ctx.props` 中，然后调用已缓存的后端 Worker。网关在每个请求上运行（必须如此，以进行身份验证），但昂贵的后端仅在尚无该用户的缓存条目时运行。经过身份验证的 API 从“不可缓存”变为“按用户安全缓存”，缓存键为你完成了隔离。文档在**使用 `ctx.props` 实现多租户安全**和**每个用户的身份验证响应**示例中详细介绍了这一点。

其他 CDN 迫使你在正确性和命中率之间做出选择：按每个用户的 Token 键控缓存，或者将每个请求发送回源站进行授权。**Workers 缓存**让你可以在边缘共享缓存的 API 响应，同时保留每个请求的授权边界。据我们所知，没有其他 CDN 提供这种内置模型来处理经过身份验证的多租户 API。我们对此感到非常自豪。

## 每个 Worker 入口点之间的缓存

以下是 **Workers 缓存**中我们认为最大的突破点，也是如果你将其视为“恰好能在 Worker 前工作的 CDN 缓存”时最难看到的部分。

**Workers 缓存**位于每个 Worker 入口点之前——默认导出、每个命名的 `WorkerEntrypoint`，以及通过 `ctx.exports` 在同一 Worker 的入口点之间的每次调用。最后这一条改变了你能构建的内容。

当一个入口点通过 `ctx.exports` 调用另一个入口点时，缓存会像评估来自浏览器的请求一样评估该调用。命中时返回缓存的响应，被调用方完全不运行。未命中时运行被调用方，并将其响应以其自身的缓存键存储——键控于被调用方的入口点、路径、查询字符串和 `ctx.props`。调用方仍在每个请求上运行，但它传递给被调用方的任何内容都会被独立记忆化。

你可以按入口点决定哪些进行缓存。在你的 Wrangler 配置中，`exports` 映射允许你按名称（“default”是默认导出）为每个入口点开启或关闭缓存。选择入口点**加入**缓存其产生的响应；选择入口点**退出**以使其在每个请求上持续运行。网关或路由器入口点——任何进行身份验证、标准化或分发的入口点——应被退出，以便它始终运行，并且其自身输出永远不会从缓存中提供。

这为您提供了一个可组合的原语。您可以将一个 Worker 编写为一系列小型入口点的链——身份验证、规范化、路由、昂贵的读取、数据层——并让 Workers Cache 插入到您想要的任何位置。每个缓存的入口点都是一个记忆化单元，拥有自己的键、自己的 TTL 以及用于清除的自己的标签命名空间。任何您想配置的关于缓存的内容——何时运行、以什么为键、何时失效——都表示为普通的 Worker 代码：您调用的入口点、您转发什么请求、您传递什么 `ctx.props`、您设置什么 `Cache-Control`。

为了具体说明，这里有一个单一的 Worker，它完成了您在任何其他平台上都难以同时完成的三件事：它对每个请求进行身份验证，将昂贵的后端缓存在一个多租户安全的缓存键后面，并在数据更改时使该缓存失效。

缓存是按入口点配置的。网关必须在每个请求上运行——既是为了身份验证，也是因为缓存的网关响应会跳过该身份验证检查——因此我们在默认入口点上禁用缓存，并仅在内层入口点上启用它：

```JSON
{
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2026-05-01",
  "cache": { "enabled": true },
  "exports": {
    // 网关在每个请求上运行——不要缓存它。
    "default": { "type": "worker", "cache": { "enabled": false } },
    // 缓存昂贵的内层入口点。
    "CachedBackend": { "type": "worker", "cache": { "enabled": true } }
  }
}
```

```TypeScript
import { WorkerEntrypoint } from "cloudflare:workers";

interface Env { API_TOKEN: string; }
interface Props { userId: string; }

// 内层入口点：昂贵的工作。Workers Cache 位于其前面
// ——命中时，此代码永远不会运行。
export class CachedBackend extends WorkerEntrypoint<Env, Props> {
  async fetch(request: Request): Promise<Response> {
    // ctx.props.userId 是缓存键的一部分，因此这会为每个用户
    // 分别缓存。
    const { userId } = this.ctx.props;
    const data = await loadExpensiveData(userId);

    return new Response(JSON.stringify(data), {
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "public, max-age=300, stale-while-revalidate=3600",
        "Cache-Tag": `user:${userId}`,
      },
    });
  }

  // 使某个用户的缓存响应失效。purge() 的作用域限定在调用它的
  // 入口点内，因此它必须在 CachedBackend 内部运行——
  // 即拥有该缓存响应的入口点。
  async invalidate(userId: string): Promise<void> {
    await this.ctx.cache.purge({ tags: [`user:${userId}`] });
  }
}

// 外层入口点：在每个请求上运行以进行身份验证和路由。
// 在 Wrangler 配置（上方）中为其禁用了缓存，因此它始终
// 运行，并且身份验证检查永远不会因缓存命中而被跳过。
export default {
  async fetch(request, env, ctx): Promise<Response> {
    const userId = await authenticate(request, env);
    if (!userId) return new Response("Unauthorized", { status: 401 });

    // 在写入时使该用户的缓存失效，从拥有它的入口点进行。
    if (request.method === "POST") {
      await handleWrite(request, userId);
      await ctx.exports.CachedBackend.invalidate(userId);
      return new Response("OK");
    }

    // 对于读取：移除 Authorization（否则 Cloudflare 的自动
    // 绕过会触发，导致无法缓存），然后将经过身份验证的用户身份
    // 放在 ctx.props 中，分派到缓存的 backend。
    const forwarded = new Request(request);
    forwarded.headers.delete("Authorization");

    return ctx.exports.CachedBackend.fetch(forwarded, {
      props: { userId },
    });
  },
} satisfies ExportedHandler<Env>;
```

整个东西就是一个 Worker。一个源文件。一次部署。但有两个执行阶段——在网关处关闭缓存，在 backend 处打开缓存，仅在一个小的 `exports` 块中——并且它们之间有一个缓存，按用户键控，由写入路径失效，并在后台刷新期间提供过期内容。缓存阶段不是您后来附加的。它是程序的一个层，用代码编写。

由此组合出的模式是开放式的。相同的结构适用于：

- 缓存一个 Durable Object。将 Durable Object 包装在一个入口点后面，在响应上设置 `Cache-Control`，读取操作在命中时就不会再触及 Durable Object。写入操作直接进入 DO 并通过标签清除缓存。DO 对缓存的发生毫无察觉。
- 在 `Vary` 之前规范化 `Accept-Encoding`。外层入口点从 `request.cf.clientAcceptEncoding` 恢复原始编码（Cloudflare 的前线为了缓存效率会将其规范化），并将其转发到一个根据真实值进行 Vary 的缓存入口点。命中率保持高位；客户端获得正确的编码。
- 在缓存之前剥离跟踪参数。外层入口点规范化 URL——或者在 `ctx.exports` 调用上使用 `cf.cacheKey` 设置一个自定义缓存键——这样缓存的内层入口点只看到规范化的形式，并且 `?utm_source=anything` 会合并为单个缓存条目。

缓存一个 Durable Object。将 Durable Object 包装在一个入口点后面，在响应上设置 `Cache-Control`，读取操作在命中时就不会再触及 Durable Object。写入操作直接进入 DO 并通过标签清除缓存。DO 对缓存的发生毫无察觉。

在 `Vary` 之前规范化 `Accept-Encoding`。外层入口点从 `request.cf.clientAcceptEncoding` 恢复原始编码（Cloudflare 的前线为了缓存效率会将其规范化），并将其转发到一个根据真实值进行 Vary 的缓存入口点。命中率保持高位；客户端获得正确的编码。

在缓存之前剥离跟踪参数。外层入口点规范化 URL——或者在 `ctx.exports` 调用上使用 `cf.cacheKey` 设置一个自定义缓存键——这样缓存的内层入口点只看到规范化的形式，并且 `?utm_source=anything` 会合并为单个缓存条目。

将它们堆叠起来。一个单一的 Worker 可以有一个用于身份验证和路由的外层入口点，一个用于剥离跟踪参数和恢复编码头部的规范化入口点，一个位于 Durable Object 前面的缓存入口点，以及一个用于未经身份验证的公共 API 的独立缓存入口点——每个都由一个您无需配置、只需决定放置位置的缓存阶段连接起来。文档中的示例页面逐步介绍了其中几个端到端的例子。

我们不知道还有其他平台可以做到这一点。CDN 缓存位于源站前面。函数平台运行函数。我们不知道还有其他平台能为您提供一个位于单一可部署单元内部、应用程序各部分之间的缓存，并且每个缓存阶段都由其两侧的代码进行配置。这就是 Workers Cache。而且因为它能与平台已经提供的所有其他功能——Smart Placement、Durable Objects、服务绑定、`ctx.props`、`ctx.exports`——组合使用，您可以构建的模式是开放式的。在这篇文章中，我们只是触及了皮毛。

## 在您的框架中获得一流支持

如果您使用 Astro 进行构建，Cloudflare 适配器会为您自动配置 Workers Cache。只需将 `cacheCloudflare` 提供者添加到您的配置中：

```JavaScript
// astro.config.mjs
import { defineConfig } from "astro/config";
import cloudflare from "@astrojs/cloudflare";
import { cacheCloudflare } from "@astrojs/cloudflare/cache";

export default defineConfig({
  adapter: cloudflare(),
  output: "server",
  experimental: {
    cache: { provider: cacheCloudflare() },
    routeRules: {
      "/products/*": { maxAge: 300, swr: 3600, tags: ["products"] },
      "/blog/*":     { maxAge: 60,  swr: 86400, tags: ["blog"] },
    },
  },
});
```

该适配器启用缓存，为 Astro 生成的响应设置正确的标头，附加用于失效的 `Cache-Tag` 值，并为您提供一个 `cache.invalidate()` 辅助函数，用于在内容变更时清除标签。选择服务器渲染的 Astro 页面会自动获得上述“渲染一次、缓存、后台刷新”的流程——无需逐路由配置，也无需学习特定于框架的运行时层。

我们正在与其他框架的维护者合作，以提供相同的集成。如果您为 Cloudflare 构建框架适配器，`Workers Cache API` 正是您所期望的——基于标头的配置、程序化清除，无需建模任何平台特定的概念。

## 在与您的 Worker 相同的仪表板上查看缓存

缓存只有在您能看到其运行情况时才有用。`Workers 可观测性仪表板` 现在每次调用都会显示缓存命中信息：

您可以看到，每个 Worker：

- **缓存命中率随时间变化**。启用缓存后，您希望这个数字呈上升趋势。
- **命中、未命中、更新、旁路细分**。如果您的命中率较低，这里就是您找出原因的地方——过多的 `BYPASS` 响应（因为某些东西设置了 cookie？）、过多的 `MISS` 响应（因为缓存键的分区比您想象的要多？）、过多的 `UPDATING` 响应（因为 `max-age` 比您的流量间隔短？）。

因为所有这些信息都位于与您 Worker 的其他可观测性（日志、异常、CPU 时间、请求计数）相同的仪表板上，您无需在查看区域和 Worker 之间切换上下文来了解发生了什么。

## 计费

缓存命中不会运行您的 Worker，也不会产生 CPU 时间费用。它们会像任何其他调用一样，按标准的 `Workers 请求费率` 计为一个请求。缓存未命中和旁路按正常方式计费——请求 + CPU 时间，与没有缓存时完全相同。

| 结果 | 请求费用 | CPU 时间费用 |
| :--- | :--- | :--- |
| 缓存命中（Worker 不运行） | 标准费率 | 不计费 |
| 缓存未命中（Worker 运行） | 计费 | 计费 |
| 缓存旁路（Worker 运行） | 计费 | 计费 |
| 静态资产请求 | 标准费率 | 不计费 |
| Worker 到 Worker 调用 | 如果 Worker 运行则计费 | 计费 |

没有单独的 Workers Cache SKU，也没有按 GB 计算的缓存存储费用。分层缓存、清除、`stale-while-revalidate` 以及上述分析功能均包含在内。如果一个请求本应运行您的 Worker，而 Workers Cache 作为命中结果提供了服务，您仍需支付标准请求费率，但无需为该请求支付 CPU 时间费用。因此，该缓存命中的成本低于在您的 Worker 中渲染相同响应。

需要注意的一点是：启用缓存后，通常免费的请求——通过服务绑定或 `ctx.exports` 进行的**静态资产请求**和**Worker 到 Worker 调用**——将按标准请求费率计费，因为每个请求现在都会在您的 Worker 之前查询缓存。

## 下一步计划

我们已知接下来要做的事情：

- **通过智能放置实现更智能的协同定位**。目前，Cloudflare 分别选择上层缓存目标和智能放置目标。在完全未命中的情况下，请求可能在 Cloudflare 位置之间传输两次：一次检查上层缓存，另一次在靠近其数据的位置运行您的 Worker。我们正在努力协调这些选择，以便未命中时只需进行一次长途传输。
- **更大的响应大小限制**。上线时，无论您的账户如何，所有响应都遵循 `Free 计划` 的可缓存大小限制（512 MB）。这是暂时的——在我们完成几个部署步骤后，将应用标准的按计划缓存限制。
- **更多框架集成**。Astro 已与 Workers Cache 内置集成。我们正在与维护者合作，为其他框架添加类似的集成，包括通过 `Vinext` 集成的 `TanStack Start` 和 Next.js。
- **用于将缓存响应标记为过时的 API**。`ctx.cache.purge()` 从缓存中移除匹配的响应。我们正在研究一个 `ctx.cache.invalidate()` API，该 API 使匹配的响应表现为已过期，这样下一个请求仍然可以通过 `stale-while-revalidate` 获得快速的过时响应，同时您的 Worker 在后台刷新缓存。

## 尝试使用

Workers Cache 现已面向任何计划的所有 Worker 开放。

要开始使用，请在您的 `wrangler.jsonc` 中添加 `"cache": { "enabled": true }`，重新部署，然后开始设置 `Cache-Control` 标头。`Workers Cache 文档` 详细介绍了完整的功能面——包括**快速入门**、**缓存键**、**清除**、**组合模式与示例**以及**调试**。

Workers 曾经运行在缓存之前。现在它们也可以运行在缓存之后。使用您需要的任何一侧——或者，通过服务绑定，同时使用两侧。

我们迫不及待地想看到您构建的成果。

---

> 本文由AI自动翻译，原文链接：[Your Worker can now have its own cache in front of it](https://blog.cloudflare.com/workers-cache/)
> 
> 翻译时间：2026-07-08 05:26
