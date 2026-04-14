---
title: 动态、身份感知且安全的沙盒认证
title_original: Dynamic, identity-aware, and secure Sandbox auth
date: '2026-04-13'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/sandbox-auth/
author: ''
summary: 本文介绍了为AI Agent沙盒环境引入出站Worker的新机制，以解决传统身份验证方法（如API令牌、OIDC令牌）在安全性、灵活性和集成性方面的不足。出站Worker作为程序化出口代理，允许受信任平台在沙盒向外部服务（如GitHub）发出请求时，动态注入身份凭证、记录或修改请求，从而在保障安全隔离的同时，为不可信的Agent工作负载提供细粒度、身份感知的认证控制。这提升了沙盒在速度、安全性和可控性方面的能力。
categories:
- AI基础设施
tags:
- 沙盒安全
- 身份认证
- AI Agent
- 出站Worker
- 微虚拟机
draft: false
translated_at: '2026-04-14T04:44:49.071727'
---

# 动态、身份感知且安全的沙盒认证

2026-04-13

- Mike Nomitch
- Gabi Villalonga Simón

![](/images/posts/e7f276d6ae53.png)

随着AI大语言模型以及像OpenCode和Claude Code这样的工具变得越来越强大，我们看到越来越多的用户启动沙盒化Agent来响应聊天消息、看板更新、氛围编码UI、终端会话、GitHub评论等等。

沙盒是超越简单容器的重要一步，因为它为您提供了以下几点：

- **安全性**：任何不受信任的最终用户（或恶意LLM）都可以在沙盒中运行，而不会危及主机或与其并行的其他沙盒。传统上（但并非总是）这是通过微虚拟机实现的。
- **速度**：最终用户应该能够快速启动一个新的沙盒，并快速从之前使用过的沙盒恢复状态。
- **控制**：**受信任的**平台需要能够在沙盒的**不受信任的**域内执行操作。这可能意味着在沙盒中挂载文件，或者控制哪些请求可以访问它，或者执行特定命令。

**安全性**：任何不受信任的最终用户（或恶意LLM）都可以在沙盒中运行，而不会危及主机或与其并行的其他沙盒。传统上（但并非总是）这是通过微虚拟机实现的。

**速度**：最终用户应该能够快速启动一个新的沙盒，并快速从之前使用过的沙盒恢复状态。

**控制**：**受信任的**平台需要能够在沙盒的**不受信任的**域内执行操作。这可能意味着在沙盒中挂载文件，或者控制哪些请求可以访问它，或者执行特定命令。

今天，我们很高兴为我们的**沙盒**和所有**容器**添加另一个关键的控制组件：出站Worker。这些是程序化的出口代理，允许运行沙盒的用户轻松连接到不同的服务，增加**可观测性**，并且，对于Agent来说尤为重要，增加灵活且安全的身份验证。

## 工作原理

以下是通过出站Worker将密钥添加到请求头的快速示例：

```javascript
class OpenCodeInABox extends Sandbox {
  static outboundByHost = {
    "github.com": (request, env, ctx) => {
      const headersWithAuth = new Headers(request.headers);
      headersWithAuth.set("x-auth-token", env.SECRET);
      return fetch(request, { headers: headersWithAuth });
    }
  }
}

```

每当沙盒中运行的代码向“github.com”发出请求时，该请求都会通过此处理程序进行代理。这允许您对每个请求执行任何操作，包括记录、修改或取消它。在这个例子中，我们安全地注入了一个密钥（稍后会详细说明）。该代理与任何沙盒运行在同一台机器上，可以访问分布式状态，并且可以通过简单的JavaScript轻松修改。

我们对这为沙盒带来的所有可能性感到兴奋，尤其是在Agent的身份验证方面。在深入细节之前，让我们先回顾一下传统的身份验证形式，以及为什么我们认为有更好的方法。

## Agent工作负载的常见身份验证

Agent身份验证的核心问题在于我们无法完全信任工作负载。虽然我们的LLM并非恶意（至少目前还不是），但我们仍然需要能够应用保护措施，以确保它们不会不当使用数据或执行不应执行的操作。

有几种常见的方法可以为Agent提供身份验证，但每种方法都有缺点：

**标准API令牌**是最基本的身份验证方法，通常通过环境变量或挂载的密钥文件注入到应用程序中。这可以说是最简单的方法，但也是最不安全的。您必须相信沙盒不会在某种程度上被攻破或在发出请求时意外泄露令牌。由于您无法完全信任Agent，您需要设置令牌过期和轮换机制，这可能很麻烦。

**工作负载身份令牌**，例如OIDC令牌，可以解决其中一些痛点。您不是授予Agent一个具有通用权限的令牌，而是授予它一个证明其身份的令牌。现在，Agent不是直接用令牌直接访问某个服务，而是可以用身份令牌换取一个非常短期的访问令牌。OIDC令牌可以在特定Agent的工作流程完成后失效，并且过期管理更容易。工作负载身份令牌最大的缺点之一是集成的潜在不灵活性。许多服务并不原生支持OIDC，因此为了与上游服务实现有效集成，平台需要自行构建令牌交换服务。这使得采用变得困难。

**自定义代理**提供了最大的灵活性，并且可以与工作负载身份令牌结合使用。如果您能将沙盒的部分或全部出口流量通过一段受信任的代码，您就可以插入任何需要的规则。也许您的Agent正在通信的上游服务其RBAC（基于角色的访问控制）机制不完善，无法提供细粒度的权限。没问题，自己编写控制和权限规则即可！对于需要细粒度控制来锁定的Agent来说，这是一个很好的选择。然而，如何拦截沙盒的所有流量？如何建立一个动态且易于编程的代理？如何高效地代理流量？这些问题都不容易解决。

考虑到这些不完美的方法，理想的身份验证机制是什么样的？

理想情况下，它应该是：

- **零信任**。永远不会向不受信任的用户授予任何时长的令牌。
- **简单**。易于编写。不涉及复杂的令牌生成、轮换和解密系统。
- **灵活**。我们不依赖上游系统来提供我们所需的细粒度访问。我们可以应用任何想要的规则。
- **身份感知**。我们可以识别发出调用的沙盒，并为其应用特定规则。
- **可观测**。我们可以轻松收集有关正在进行的调用的信息。
- **高性能**。我们不需要往返于集中式或缓慢的真相源。
- **透明**。沙盒化的工作负载无需知晓其存在。一切正常运作。
- **动态**。我们可以随时更改规则。

**零信任**。永远不会向不受信任的用户授予任何时长的令牌。

**简单**。易于编写。不涉及复杂的令牌生成、轮换和解密系统。

**灵活**。我们不依赖上游系统来提供我们所需的细粒度访问。我们可以应用任何想要的规则。

**身份感知**。我们可以识别发出调用的沙盒，并为其应用特定规则。

**可观测**。我们可以轻松收集有关正在进行的调用的信息。

**高性能**。我们不需要往返于集中式或缓慢的真相源。

**透明**。沙盒化的工作负载无需知晓其存在。一切正常运作。

**动态**。我们可以随时更改规则。

我们相信沙盒的出站Worker符合所有这些要求。让我们看看是如何实现的。

## 实践中的出站Worker

### 基础：限制与可观测性

首先，我们来看一个非常基础的例子：记录请求并拒绝特定操作。

在这种情况下，我们将使用出站函数，它会拦截沙盒发出的所有传出HTTP请求。只需几行JavaScript代码，就可以轻松确保只允许GET请求，并记录然后拒绝任何不允许的方法。

```javascript
class MySandboxedApp extends Sandbox {
  static outbound = (req, env, ctx) => {
    // 拒绝任何非GET操作并记录
    if (req.method !== 'GET') {
      console.log(`Container making ${req.method} request to: ${req.url}`);
      return new Response('Not Allowed', { status: 405, statusText: 'Method Not Allowed'});
    }

    // 如果是GET请求则放行
    return fetch(req);
  };
}

```

此代理运行在Worker上，并与沙盒化的虚拟机运行在同一台机器上。Worker专为快速响应时间而构建，通常位于缓存的CDN流量之前，因此增加的延迟极小。

由于这是在 Workers 上运行的，我们可以直接获得可观测性。您可以在 Workers 仪表板中查看日志和出站请求，也可以将它们导出到您选择的应用性能监控工具。

### 零信任凭证注入

我们将如何使用此功能来为我们的 Agent（智能体）强制执行零信任环境？假设我们想向一个私有的 GitHub 实例发出请求，但我们绝不想让我们的 LLM（大语言模型）访问私有令牌。

我们可以使用 `outboundByHost` 来为特定域名或 IP 定义函数。在这种情况下，如果域名是 "my-internal-vcs.dev"，我们将注入一个受保护的凭证。被沙箱化的 Agent（智能体）**永远无法访问**这些凭证。

```javascript
class OpenCodeInABox extends Sandbox {
  static outboundByHost = {
    "my-internal-vcs.dev": (request, env, ctx) => {
      const headersWithAuth = new Headers(request.headers);
      headersWithAuth.set("x-auth-token", env.SECRET);
      return fetch(request, { headers: headersWithAuth });
    }
  }
}

```

根据容器的身份来条件化响应也很容易。您不必为每个沙箱实例注入相同的令牌。

```javascript
 static outboundByHost = {
  "my-internal-vcs.dev": (request, env, ctx) => {
    // 注意：KV 在静态和传输过程中都是加密的
    const authKey = await env.KEYS.get(ctx.containerId);

    const requestWithAuth = new Request(request);
    requestWithAuth.headers.set("x-auth-token", authKey);
    return fetch(requestWithAuth);
  }
}

```

### 使用 Cloudflare 开发者平台

正如您可能在上一个示例中注意到的，使用出站 Workers 的另一个主要优势是，它使得集成到 Workers 生态系统中变得更加容易。以前，如果用户想要访问 R2，他们必须注入一个 R2 凭证，然后从他们的容器向公共的 R2 API 发起调用。对于 KV、Agents（智能体）、其他 Containers（容器）、其他 Worker 服务等也是如此。

现在，您只需从您的出站 Workers 中调用**任何绑定**。

```javascript
class MySandboxedApp extends Sandbox {
  static outboundByHost = {
    "my.kv": async (req, env, ctx) => {
      const key = keyFromReq(req);
      const myResult = await env.KV.get(key);
      return new Response(myResult);
    },
    "objects.cf": async (req, env, ctx) => {
      const prefix = ctx.containerId
      const path = pathFromRequest(req);
      const object = await env.R2.get(`${prefix}/${path}`);
      const myResult = await env.KV.get(key);
      return new Response(myResult);
    },
  };
}

```

我们无需解析令牌和设置策略，而是可以轻松地通过代码和我们想要的任何逻辑来条件化访问。在 R2 示例中，我们还能够使用沙箱的 ID 来进一步轻松地限定访问范围。

### 使控制动态化

网络控制也应该是动态的。在许多平台上，容器和虚拟机网络的配置是静态的，看起来像这样：

```javascript
{
  defaultEgress: "block",
  allowedDomains: ["github.com", "npmjs.org"]
}

```

这比没有好，但我们可以做得更好。对于许多沙箱，我们可能希望在启动时应用一个策略，但在执行了特定操作后，用另一个策略覆盖它。

例如，我们可以启动一个沙箱，通过 NPM 和 Github 获取我们的依赖项，然后在那之后锁定出站流量。这确保了我们在尽可能短的时间内开放网络。

为了实现这一点，我们可以使用 `outboundHandlers`，它允许我们定义任意的出站处理程序，这些处理程序可以使用 `setOutboundHandler` 方法以编程方式应用。每个处理程序也接受参数，允许您从代码中自定义行为。在这种情况下，我们将使用自定义的 "allowHosts" 策略允许某些主机名，然后关闭 HTTP。

```javascript
class MySandboxedApp extends Sandbox {
  static outboundHandlers = {
    async allowHosts(req, env, { params }) {
     const url = new URL(request.url);
     const allowedHostname = params.allowedHostnames.includes(url.hostname);

      if (allowedHostname) {
        return await fetch(newRequest);
      } else {
        return new Response(null, { status: 403, statusText: "Forbidden" });
      }
    }
    
    async noHttp(req) {
      return new Response(null, { status: 403, statusText: "Forbidden" });
    }
  }
}

async setUpSandboxes(req, env) {
  const sandbox = await env.SANDBOX.getByName(userId);
  await sandbox.setOutboundHandler("allowHosts", {
    allowedHostnames: ["github.com", "npmjs.org"]
  });
  await sandbox.gitClone(userRepoURL)
  await sandbox.exec("npm install")
  await sandbox.setOutboundHandler("noHttp");
}

```

这甚至可以进一步扩展。您的 Agent（智能体）可能会根据当时所需的工具，向最终用户提出类似“您是否允许向 cloudflare.com 发送 POST 请求？”的问题。借助动态出站 Workers，您可以轻松地即时修改沙箱规则，以提供这种级别的控制。

## 支持 TLS 与 MITM 代理

为了对请求执行除允许或拒绝之外的有用操作，您需要能够访问其内容。这意味着，如果您发出 HTTPS 请求，它们需要由 Workers 代理进行解密。

为了实现这一点，会为每个沙箱实例创建一个唯一的临时证书颁发机构（CA）和私钥，并将该 CA 放入沙箱中。默认情况下，沙箱实例将信任此 CA，而标准容器实例可以选择信任它，例如通过调用 `sudo update-ca-certificates`。

```javascript
export class MyContainer extends Container {
  interceptHttps = true;
}

MyContainer.outbound = (req, env, ctx) => {
  // 所有 HTTP(S) 请求都将触发此钩子。
  return fetch(req);
};


```

TLS 流量由 Cloudflare 隔离的网络进程通过执行 TLS 握手进行代理。它使用一个临时的、唯一的私钥创建一个叶 CA，并使用从 ClientHello 中提取的 SNI。然后，它将在同一台机器上调用已配置的 Worker 来处理 HTTPS 请求。

我们的临时私钥和 CA 永远不会离开我们的容器运行时边车进程，也永远不会在其他容器边车进程之间共享。

有了这个机制，出站 Workers 就充当了一个真正透明的代理。沙箱不需要了解特定的协议或域名——所有 HTTP 和 HTTPS 流量都流经出站处理程序进行过滤或修改。

## 底层原理

为了在 `Container` 和 `Sandbox` 中启用上述功能，我们向 `ctx.container` 对象添加了新方法：`interceptOutboundHttp` 和 `interceptOutboundHttps`，它们可以拦截发往特定主机名（支持基本通配符匹配）、IP 范围的出站请求，也可以用于拦截所有出站请求。这些方法会与一个 `WorkerEntrypoint` 一起被调用，该入口点被设置为出站 Worker 的前门。

```javascript
export class MyWorker extends WorkerEntrypoint {
 fetch() {
   return new Response(this.ctx.props.message);
 }
}

// ... 在您的容器 DurableObject 内部 ...
this.ctx.container.start({ enableInternet: false });
const outboundWorker = this.ctx.exports.MyWorker({ props: { message: 'hello' } });
await this.ctx.container.interceptOutboundHttp('15.0.0.1:80', outboundWorker);

// 从现在开始，所有发往 15.0.0.1:80 的 HTTP 请求都将返回 "hello"
await this.waitForContainerToBeHealthy();

// 您现在可以决定返回另一个消息...
const secondOutboundWorker = this.ctx.exports.MyWorker({ props: { message: 'switcheroo' } });
await this.ctx.container.interceptOutboundHttp('15.0.0.1:80', secondOutboundWorker);
// 所有发往 15.0.0.1 的 HTTP 请求现在都显示 "switcheroo"，即使是那些在此次 interceptOutboundHttp 调用之前就已经打开的连接也是如此。

// 您甚至可以同时为IPv4和IPv6设置主机名、CIDR
await this.ctx.container.interceptOutboundHttp('example.com', secondOutboundWorker);
await this.ctx.container.interceptOutboundHttp('*.example.com', secondOutboundWorker);
await this.ctx.container.interceptOutboundHttp('123.123.123.123/23', secoundOutboundWorker);
```

所有到Worker的代理都发生在运行沙箱虚拟机的同一台本地机器上。尽管容器与Worker之间的通信是“无认证的”，但它是安全的。

这些方法可以在启动容器之前或之后的任何时间调用，甚至在连接仍然打开时也可以。发送多个HTTP请求的连接将自动获取新的入口点，因此更新出站Worker不会中断现有的TCP连接或干扰HTTP请求。

使用`wrangler dev`进行本地开发也支持出口拦截。为了实现这一点，我们会在本地容器的网络命名空间内自动生成一个辅助进程。我们称这个辅助组件为`proxy-everything`。一旦`proxy-everything`被附加，它会应用适当的TPROXY nftable规则，将匹配的流量从本地容器路由到`workerd`（Cloudflare的开源JavaScript运行时），由它来运行出站Worker。这使得本地开发体验能够镜像生产环境中的情况，从而保持测试和开发的简洁性。

## 尝试使用出站Worker

如果您尚未尝试过Cloudflare沙箱，请查看[入门指南](https://developers.cloudflare.com/workers/runtime-api/sandbox/#getting-started)。如果您是`Containers`或`Sandboxes`的当前用户，现在就可以开始使用出站Worker，只需[阅读文档](https://developers.cloudflare.com/workers/runtime-api/sandbox/outbound-workers/)并升级到`@cloudflare/[email protected]`或`@cloudflare/[email protected]`。

---

> 本文由AI自动翻译，原文链接：[Dynamic, identity-aware, and secure Sandbox auth](https://blog.cloudflare.com/sandbox-auth/)
> 
> 翻译时间：2026-04-14 04:44
