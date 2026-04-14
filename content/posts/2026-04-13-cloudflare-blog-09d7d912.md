---
title: 动态Worker与Durable Objects：为AI应用配备专属数据库
title_original: 'Durable Objects in Dynamic Workers: Give each AI-generated app its
  own database'
date: '2026-04-13'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/durable-object-facets-dynamic-workers/
author: ''
summary: 本文探讨了Cloudflare Dynamic Workers与Durable Objects结合的新应用场景。Dynamic Workers允许动态加载代码到轻量级沙箱，而Durable
  Objects提供极低延迟的本地SQLite存储。文章核心在于如何让AI生成的应用代码在Dynamic Worker中运行，同时通过Durable Objects获得持久化、高性能的专属数据库，并讨论了实现中的配置、控制与安全挑战，为构建由AI生成的、具备长期状态的小型应用提供了基础设施思路。
categories:
- AI基础设施
tags:
- Cloudflare Workers
- Durable Objects
- AI应用开发
- 边缘计算
- 数据库
draft: false
translated_at: '2026-04-14T04:43:10.770987'
---

# Dynamic Workers 中的 Durable Objects：为每个 AI 生成的应用配备专属数据库

2026-04-13

- Kenton Varda

![](/images/posts/5d7d90e56f27.png)

几周前，我们发布了 **Dynamic Workers**，这是 Workers 平台的一项新功能，允许你将 Worker 代码动态加载到安全的沙箱中。Dynamic Worker Loader API 本质上提供了对 Workers 一直以来所依赖的基础计算隔离原语的直接访问：隔离体（isolates），而非容器。隔离体比容器轻量得多，因此加载速度可快 100 倍，内存占用仅为 1/10。它们如此高效，以至于可以被视为“一次性”的：启动一个来运行几行代码，然后丢弃它。就像一个安全版本的 `eval()`。

Dynamic Workers 有很多用途。在最初的公告中，我们重点介绍了如何将它们用于运行 AI Agent 生成的代码，作为工具调用的替代方案。在这个用例中，AI Agent 通过编写几行代码并执行它们，来响应用户请求执行操作。该代码是一次性的，旨在执行一次任务，并在执行后立即丢弃。

但是，如果你希望 AI 生成更持久的代码呢？如果你希望你的 AI 构建一个带有自定义 UI、可供用户交互的小型应用程序呢？如果你希望该应用程序拥有长期存在的状态呢？当然，你仍然希望它在安全的沙箱中运行。

实现这一点的一种方法是使用 Dynamic Workers，并简单地为其提供一个允许访问存储的 **RPC** API。通过使用 **绑定**，你可以为 Dynamic Worker 提供一个指向你远程 SQL 数据库的 API（或许由 Cloudflare D1 支持，或者通过 **Hyperdrive** 访问的 Postgres 数据库——这取决于你）。

但 Workers 还有一种独特且极快的存储类型，可能非常适合这个用例：**Durable Objects**。Durable Object 是一种特殊的 Worker，它有一个唯一的名称，每个名称全局只有一个实例。该实例附加了一个 SQLite 数据库，该数据库**位于本地磁盘**上，即运行 Durable Object 的机器上。这使得存储访问速度快得惊人：**延迟几乎为零**。

那么，也许你真正想要的是让你的 AI 为 Durable Object 编写代码，然后你希望在 Dynamic Worker 中运行该代码。

## 但是怎么做呢？

这带来了一个奇怪的问题。通常，要使用 Durable Objects，你必须：

1.  编写一个继承自 `DurableObject` 的类。
2.  从你的 Worker 主模块中导出它。
3.  在你的 Wrangler 配置中指定应为该类配置存储。这会创建一个 Durable Object 命名空间，指向你的类以处理传入的请求。
4.  声明一个指向你命名空间的 Durable Object 命名空间绑定（或使用 `ctx.exports`），并用它来向你的 Durable Object 发出请求。

编写一个继承自 `DurableObject` 的类。

从你的 Worker 主模块中导出它。

在你的 Wrangler 配置中指定应为该类配置存储。这会创建一个 Durable Object 命名空间，指向你的类以处理传入的请求。

声明一个指向你命名空间的 Durable Object 命名空间绑定（或使用 `ctx.exports`），并用它来向你的 Durable Object 发出请求。

这并不能自然地扩展到 Dynamic Workers。首先，有一个明显的问题：代码是动态的。你运行它时完全不需要调用 Cloudflare API。但 Durable Object 存储必须通过 API 进行配置，并且命名空间必须指向一个实现类。它不能指向你的 Dynamic Worker。

但还有一个更深层次的问题：即使你能以某种方式配置一个 Durable Object 命名空间直接指向一个 Dynamic Worker，你会愿意这样做吗？你希望你的 Agent（或用户）能够创建一个充满 Durable Objects 的整个命名空间吗？能够使用分布在世界各地的无限存储吗？

你可能不希望。你可能需要一些控制。你可能想限制或至少跟踪他们创建了多少个对象。也许你想将他们限制在只有一个对象（对于 vibe-coded 的个人应用来说可能就足够了）。你可能想添加日志记录和其他可观测性功能。指标。计费。等等。

为了实现所有这些，你真正需要的是让对这些 Durable Objects 的请求**首先**到达**你的**代码，在那里你可以处理所有“后勤”工作，**然后**将请求转发到 Agent 的代码中。你需要编写一个作为每个 Durable Object 一部分运行的**监督者**。

## 解决方案：Durable Object Facets

今天，我们以公开测试版的形式发布了一项解决此问题的功能。

**Durable Object Facets** 允许你动态加载和实例化一个 Durable Object 类，同时为其提供一个用于存储的 SQLite 数据库。使用 Facets：

-   首先，你创建一个普通的 Durable Object 命名空间，指向**你**编写的类。
-   在该类中，你将 Agent 的代码作为 Dynamic Worker 加载，并调用它。
-   Dynamic Worker 的代码可以直接实现一个 Durable Object 类。也就是说，它实际上导出一个声明为 `extends DurableObject` 的类。
-   你将这个类实例化为你自己 Durable Object 的一个“facet”。
-   该 facet 拥有自己的 SQLite 数据库，可以通过正常的 Durable Object 存储 API 使用。这个数据库与监督者的数据库是分开的，但两者作为同一个整体 Durable Object 的一部分存储在一起。

首先，你创建一个普通的 Durable Object 命名空间，指向**你**编写的类。

在该类中，你将 Agent 的代码作为 Dynamic Worker 加载，并调用它。

Dynamic Worker 的代码可以直接实现一个 Durable Object 类。也就是说，它实际上导出一个声明为 `extends DurableObject` 的类。

你将这个类实例化为你自己 Durable Object 的一个“facet”。

该 facet 拥有自己的 SQLite 数据库，可以通过正常的 Durable Object 存储 API 使用。这个数据库与监督者的数据库是分开的，但两者作为同一个整体 Durable Object 的一部分存储在一起。

## 工作原理

下面是一个动态加载和运行 Durable Object 类的应用平台的简单、完整实现：

```javascript
import { DurableObject } from "cloudflare:workers";

// 为了这个示例，我们将使用这个静态的
// 应用程序代码，但在现实世界中，这可能是由
// AI（甚至可能是人类用户）生成的。
const AGENT_CODE = `
  import { DurableObject } from "cloudflare:workers";

  // 一个简单的应用，记录它被调用了多少次
  // 并返回该次数。
  export class App extends DurableObject {
    fetch(request) {
      // 为了简单起见，我们在这里使用 storage.kv，但 storage.sql
      // 也可用。两者都由 SQLite 支持。
      let counter = this.ctx.storage.kv.get("counter") || 0;
      ++counter;
      this.ctx.storage.kv.put("counter", counter);

      return new Response("You've made " + counter + " requests.\\n");
    }
  }
`;

// AppRunner 是你编写的一个 Durable Object，负责
// 动态加载应用程序并将请求传递给它们。
// AppRunner 的每个实例包含一个不同的应用。
export class AppRunner extends DurableObject {
  async fetch(request) {
    // 我们收到了一个 HTTP 请求，我们希望将其转发到
    // 应用中。

    // 应用本身作为一个名为 "app" 的子 facet 运行。一个 Durable
    // Object 可以有任意数量的具有不同名称的 facet（受存储限制限制），
    // 但在这个例子中我们只有一个。调用
    // this.ctx.facets.get() 来获取指向它的存根。
    let facet = this.ctx.facets.get("app", async () => {
      // 如果这个回调被调用，意味着 facet 还没有
      // 启动（或已休眠）。在这个回调中，我们可以
      // 告诉系统我们希望它加载什么代码。

      // 加载 Dynamic Worker。
      let worker = this.#loadDynamicWorker();

      // 获取我们感兴趣的导出类。
      let appClass = worker.getDurableObjectClass("App");

      return { class: appClass };
    });

// 将请求转发给 facet。
    // （或者，你也可以在这里调用 RPC 方法。）
    return await facet.fetch(request);
  }

  // 客户端可以调用的 RPC 方法，用于为此应用设置动态代码。
  setCode(code) {
    // 将代码存储在 AppRunner 的 SQLite 存储中。
    // 每段唯一的代码必须有一个唯一的 ID 才能传递给动态 Worker 加载器 API，因此我们随机生成一个。
    this.ctx.storage.kv.put("codeId", crypto.randomUUID());
    this.ctx.storage.kv.put("code", code);
  }

  #loadDynamicWorker() {
    // 像平常一样使用动态 Worker 加载器 API。使用 get() 而不是 load()，因为我们可能会多次加载同一个 Worker。
    let codeId = this.ctx.storage.kv.get("codeId");
    return this.env.LOADER.get(codeId, async () => {
      // 此 Worker 尚未加载。从我们自己的存储中加载其代码。
      let code = this.ctx.storage.kv.get("code");

      return {
        compatibilityDate: "2026-04-01",
        mainModule: "worker.js",
        modules: { "worker.js": code },
        globalOutbound: null,  // 阻止网络访问
      }
    });
  }
}

// 这是一个使用 AppRunner 的简单 Workers HTTP 处理器。
export default {
  async fetch(req, env, ctx) {
    // 获取名为 "my-app" 的 AppRunner 实例。
    // （每个名称在全球范围内恰好对应一个 Durable Object 实例。）
    let obj = ctx.exports.AppRunner.getByName("my-app");

    // 用代码初始化它。（在实际用例中，你只希望调用此方法一次，而不是在每个请求上都调用。）
    await obj.setCode(AGENT_CODE);

    // 将请求转发给它。
    return await obj.fetch(req);
  }
}

```

在此示例中：

- AppRunner 是由平台开发者（你）编写的“普通”Durable Object。
- AppRunner 的每个实例管理一个应用程序。它存储应用程序代码并按需加载。
- 应用程序本身实现并导出一个 Durable Object 类，平台期望其名为 App。
- AppRunner 使用动态 Worker 加载应用程序代码，然后将其作为 Durable Object Facet 执行。
- AppRunner 的每个实例都是一个由两个 SQLite 数据库组成的 Durable Object：一个属于父级（AppRunner 本身），另一个属于 facet（App）。这些数据库是隔离的：应用程序无法读取 AppRunner 的数据库，只能读取自己的数据库。

要运行此示例，请将上面的代码复制到文件 `worker.js` 中，与下面的 `wrangler.jsonc` 配对，并使用 `npx wrangler dev` 在本地运行。

```JSON
// 用于上述示例 worker 的 wrangler.jsonc。
{
  "compatibility_date": "2026-04-01",
  "main": "worker.js",
  "migrations": [
    {
      "tag": "v1",
      "new_sqlite_classes": [
        "AppRunner"
      ]
    }
  ],
  "worker_loaders": [
    {
      "binding": "LOADER",
    },
  ],
}

```

## 开始构建

Facet 是动态 Worker 的一项功能，现已作为 Beta 版功能，立即向 Workers 付费计划的用户开放。

查看文档以了解更多关于动态 Worker 和 Facet 的信息。

---

> 本文由AI自动翻译，原文链接：[Durable Objects in Dynamic Workers: Give each AI-generated app its own database](https://blog.cloudflare.com/durable-object-facets-dynamic-workers/)
> 
> 翻译时间：2026-04-14 04:43
