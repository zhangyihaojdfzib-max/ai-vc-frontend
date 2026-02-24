---
title: Vercel沙盒新增HTTP头注入功能，安全隔离API凭据
title_original: Safely inject credentials in HTTP headers with Vercel Sandbox - Vercel
date: '2026-02-23'
source: Vercel Blog
source_url: https://vercel.com/changelog/safely-inject-credentials-in-http-headers-with-vercel-sandbox
author: ''
summary: Vercel Sandbox推出新功能，可自动将API密钥等凭据通过HTTP头信息注入沙盒代码的出站请求中，而无需在沙盒虚拟机内部存储敏感信息。该功能通过配置网络策略中的`transform`实现，支持精确域名和通配符匹配，注入的头信息会完全覆盖沙盒内设置的同类头，防止凭据被窃取或篡改。此特性专为防范AI
  Agent工作流中的提示词注入等安全威胁设计，即使沙盒环境被攻破，凭据仍能得到保护。所有Pro版和企业版客户均可使用。
categories:
- AI基础设施
tags:
- Vercel
- 沙盒安全
- API密钥管理
- HTTP头注入
- AI Agent
draft: false
translated_at: '2026-02-24T04:37:22.346511'
---

Vercel Sandbox 现已能自动将 HTTP 头信息注入沙盒代码的出站请求中。这使 API 密钥和 Token 安全地保留在沙盒虚拟机边界之外，因此沙盒内运行的应用可以调用需要身份验证的服务，而无需直接接触凭据。头信息注入通过 `transform` 在网络策略中配置。当沙盒向匹配的域名发起 HTTPS 请求时，防火墙会在转发请求前添加或替换指定的头信息。

```
1const sandbox = await Sandbox.create({2  timeout: 300_000,3  networkPolicy: {4    allow: {5      "ai-gateway.vercel.sh": [{6        transform: [{ headers: { authorization: `Bearer ${process.env.AI_GATEWAY_API_KEY}` } }],7      }],8    },9  },10});11
1213const result = await sandbox.runCommand('curl', ['-s', 'https://ai-gateway.vercel.sh/v1/models']);
```

此功能专为 AI Agent（智能体）工作流设计，其中提示词注入是真实存在的威胁。即使 Agent 被攻破，也无法窃取凭据，因为凭据仅存在于虚拟机外部的层面。

![](/images/posts/73a1dde86c6b.jpg)

![](/images/posts/6accd9863383.jpg)

![](/images/posts/874485759cfe.jpg)

![](/images/posts/f68782251b0a.jpg)

注入规则适用于所有出口网络策略配置，包括开放的互联网访问。若要在允许通用流量的同时为特定服务注入凭据：

```
1const sandbox = await Sandbox.create({2  networkPolicy: {3    allow: {4      "ai-gateway.vercel.sh": [{5        transform: [{ headers: { Authorization: `Bearer ${process.env.AI_GATEWAY_API_KEY}` } }],6      }],7      "*.github.com": [{8        transform: [{ headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` } }],9      }],10      11      "*": []12    }13  }14});
```

### 实时更新

与所有网络策略设置一样，注入规则可以在沙盒运行期间更新，无需重启。这支持多阶段工作流：在设置阶段注入凭据，然后在运行不受信任的代码前移除它们：

```
12await sandbox.updateNetworkPolicy({3  allow: {4    "api.github.com": [{5      transform: [{ headers: { Authorization: `Bearer ${process.env.GITHUB_TOKEN}` } }],6    }],7  }8});9
1011
1213await sandbox.updateNetworkPolicy('deny-all');
```

### 核心亮点

-   头信息覆盖：注入应用于出站请求的 HTTP 头信息。
-   完全替换：注入的头信息会覆盖沙盒代码设置的任何同名现有头信息，防止沙盒替换其自身的凭据。
-   域名匹配：支持精确域名和通配符（例如 *.github.com）。仅当出站请求匹配时才触发注入。
-   兼容所有策略：可将注入规则与 `allow-all` 或特定域名的允许列表结合使用。

头信息覆盖：注入应用于出站请求的 HTTP 头信息。

完全替换：注入的头信息会覆盖沙盒代码设置的任何同名现有头信息，防止沙盒替换其自身的凭据。

域名匹配：支持精确域名和通配符（例如 *.github.com）。仅当出站请求匹配时才触发注入。

兼容所有策略：可将注入规则与 `allow-all` 或特定域名的允许列表结合使用。

所有 Pro 版和企业版客户均可使用。请在文档中了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Safely inject credentials in HTTP headers with Vercel Sandbox - Vercel](https://vercel.com/changelog/safely-inject-credentials-in-http-headers-with-vercel-sandbox)
> 
> 翻译时间：2026-02-24 04:37
