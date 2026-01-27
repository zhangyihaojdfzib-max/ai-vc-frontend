---
title: 远程绑定架构解析：连接本地开发与生产环境
title_original: 'Connecting to production: the architecture of remote bindings'
date: '2025-11-12'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/connecting-to-production-the-architecture-of-remote-bindings/
author: Samuel Macleod
summary: 本文深入探讨了Cloudflare Workers平台远程绑定的技术架构。文章介绍了如何通过在本地开发环境中直接绑定已部署的R2存储桶、D1数据库等远程资源，实现使用真实数据测试代码变更，而无需反复部署。该功能统一了原有的远程模式与本地开发体验，允许开发者按绑定粒度选择使用远程或本地资源，通过现有的OAuth连接简化了凭证管理，从而提升了开发效率和应用可靠性。
categories:
- AI基础设施
tags:
- Cloudflare Workers
- 远程绑定
- 本地开发
- 开发工具
- 无服务器架构
draft: false
translated_at: '2026-01-06T01:16:43.575Z'
---

远程绑定是指连接到您Cloudflare账户上已部署资源（而非本地模拟资源）的绑定——近期，我们宣布远程绑定现已全面开放使用。

通过此次发布，您现在可以在本地机器运行Worker代码时，连接到已部署的R2存储桶和D1数据库等资源。这意味着您可以直接使用真实数据和服务测试本地代码变更，无需为每次迭代执行部署操作。

在这篇博文中，我们将深入探讨实现这一功能的技术细节，以及如何打造无缝的本地开发体验。

Cloudflare Workers平台的核心优势一直是支持本地开发代码，无需在每次测试时都进行部署——尽管我们实现这一功能的方式在过去几年发生了巨大变化。

我们最初通过wrangler dev的远程模式实现这一功能。该模式会在您每次修改代码时，部署并连接到运行在Cloudflare网络上的Worker预览版本，让您在开发过程中随时进行测试。然而远程模式并不完美——它结构复杂且难以维护。开发体验也存在诸多不足：迭代速度缓慢、调试连接不稳定、缺乏多Worker场景支持。

这些问题促使我们大力投入构建完全本地的Workers开发环境，该环境于2023年中发布，并成为wrangler dev的默认模式。自此之后，我们在Wrangler、Cloudflare Vite插件（以及@cloudflare/vitest-pool-workers）和Miniflare的本地开发体验上投入了大量工作。

尽管如此，原始远程模式仍可通过标志访问：wrangler dev --remote。使用远程模式时，完全本地体验的所有开发体验优势以及我们过去几年的改进都将被绕过。那么为何人们仍在使用它？因为它提供了一项关键独特功能：在本地开发时绑定远程资源。当您使用本地模式在本地开发Worker时，所有绑定都使用本地（初始为空）数据进行模拟。这对于使用测试数据迭代应用逻辑非常理想——但有时这还不够，无论是需要跨团队共享资源、复现与真实数据相关的错误，还是仅仅希望确保应用能在生产环境中与真实资源协同工作。

鉴于此，我们看到了一个机遇：如果能把远程模式的最佳特性（即访问远程资源）引入wrangler dev，就能建立统一的Workers开发流程，支持多种使用场景，同时不让用户错过我们在本地开发方面取得的进展。这正是我们实现的目标！

自Wrangler v4.37.0起，您可以按绑定粒度选择应使用远程资源还是本地资源，只需指定remote选项即可。需要重点重申的是——您只需添加remote: true！无需复杂的API密钥和凭证管理，一切通过Wrangler与Cloudflare API的现有Oauth连接即可直接运行。

```json
{
"name": "my-worker",
"compatibility_date": "2025-01-01",
"kv_namespaces": [{
"binding": "KV",
"id": "my-kv-id",
},{
"binding": "KV_2",
"id": "other-kv-id",
"remote": true
}],
"r2_buckets": [{
"bucket_name": "my-r2-name",
"binding": "R2"
}]
}
```

细心的用户可能已经发现，某些绑定早已支持从本地开发环境访问远程资源。最突出的是AI绑定，它率先展示了通用远程绑定解决方案的雏形。自推出以来，AI绑定始终连接远程资源，因为要构建支持Workers AI所有不同模型的真正本地体验并不现实，且需要预先下载庞大的AI模型。

当我们意识到Workers内部不同产品（例如Images和Hyperdrive）都需要类似远程绑定的功能时，我们最终形成了多种解决方案拼凑的局面。现在我们已经统一为适用于所有绑定类型的单一远程绑定解决方案。

我们希望让开发者能轻松访问远程资源，且无需修改其生产环境Worker代码，因此我们确定的解决方案是：在Worker中使用远程资源时按需获取数据。

```javascript
const value = await env.KV.get("some-key")
```

以上代码片段展示了访问env.KV键值命名空间中"some-key"值的操作，该数据在本地不可用，需要通过网络获取。

那么要实现这一需求，我们该如何着手？例如，如何将用户在Worker中调用env.KV.put('key', 'value')的操作实际存储到远程KV存储中？最直接的解决方案或许是使用Cloudflare API。我们本可以在本地用存根对象完全替换env对象，通过发起API调用将env.KV.put()转换为PUT http:///accounts/{account_id}/storage/kv/namespaces/{namespace_id}/values/{key_name}。

这对KV、R2、D1等具有成熟HTTP API的绑定会很有效，但实现和维护将相当复杂。我们必须复制整个绑定API接口，并将绑定的每个可能操作转换为等效的API调用。此外，某些绑定操作没有等效的API调用，无法通过此策略支持。

相反，我们意识到已经有一个现成的API可供使用——正是我们在生产环境中使用的API！

**生产环境中绑定的底层工作原理**

Workers平台上的大多数绑定本质上都可归结为服务绑定。服务绑定是两个Worker之间的链接，允许它们通过HTTP或JSRPC进行通信（稍后会讨论JSRPC）。

例如，KV绑定被实现为您的编写Worker与平台Worker之间的服务绑定，通过HTTP通信。KV绑定的JS API在Workers运行时中实现，并将env.KV.get()等调用转换为对实现KV服务的Worker的HTTP调用。

（示意图展示生产环境中KV绑定的简化工作原理模型）

您可能会注意到这里存在天然的异步网络边界——位于运行时转换env.KV.get()调用与实现KV服务的Worker之间。我们意识到可以利用这个天然网络边界来实现远程绑定。无需生产运行时将env.KV.get()转换为HTTP调用，我们可以让本地运行时（workerd）将env.KV.get()转换为HTTP调用，然后直接发送给KV服务，绕过生产运行时。这正是我们的实现方案！

（示意图展示运行本地的Worker通过单个远程代理客户端与远程代理服务器通信，进而连接远程KV资源）

上图展示了运行本地的Worker使用远程KV绑定的情况。现在它不再由本地KV模拟处理，而是由远程代理客户端处理。该Worker随后与连接真实远程KV资源的远程代理服务器通信，最终使本地Worker能够无缝与远程KV数据交互。

每个绑定都可以独立选择由远程代理客户端处理（全部连接到同一远程代理服务器）或由本地模拟处理，从而实现高度动态的工作流：部分绑定在本地模拟，其他绑定则连接真实远程资源，如下例所示：

（示意图及配置展示运行在您计算机上的Worker绑定到3个不同资源——两个本地资源（KV和R2），一个远程资源（KV_2））

以上部分讨论的是基于HTTP连接的绑定（如KV和R2），但现代绑定使用JSRPC。

这意味着我们需要一种方法，让本地运行的 workerd 能够通过 JSRPC 与生产环境运行时实例通信。幸运的是，一个并行项目正在推进以实现这一目标，详情可见 Capân Web 博客。我们通过让本地 workerd 实例与远程运行时实例之间使用 Capân Web 通过 WebSocket 进行通信来实现集成，从而使基于 JSRPC 的绑定得以工作。这包括较新的绑定（如图像绑定），以及指向您自己 Workers 的 JSRPC 服务绑定。

**与 Vite、Vitest 及 JavaScript 生态系统的远程绑定**

我们不想将这个令人兴奋的新功能仅限于 `wrangler dev`。我们希望在我们的 Cloudflare Vite 插件和 vitest-pool-workers 包中支持它，同时也允许 JavaScript 生态系统中的任何其他潜在工具和用例从中受益。

为了实现这一点，`wrangler` 包现在导出了诸如 `startRemoteProxySession` 这样的实用工具，允许不依赖 `wrangler dev` 的工具也能支持远程绑定。您可以在官方远程绑定文档中找到更多详细信息。

**直接使用 `wrangler dev` 即可！** 自 Wrangler v4.37.0（@cloudflare/vite-plugin v1.13.0，@cloudflare/vitest-pool-workers v0.9.0）起，远程绑定已在所有项目中可用，并且可以通过在您的 Wrangler 配置文件的绑定定义中添加 `remote: true` 来按绑定逐个启用。

> 本文由AI自动翻译，原文链接：[Connecting to production: the architecture of remote bindings](https://blog.cloudflare.com/connecting-to-production-the-architecture-of-remote-bindings/)
> 
> 翻译时间：2026-01-06 01:16
