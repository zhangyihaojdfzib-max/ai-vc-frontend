---
title: Vercel Sandbox防火墙新增请求代理与过滤功能
title_original: Vercel Sandbox firewall now supports request proxying and filtering
  - Vercel
date: '2026-05-11'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-sandbox-firewall-now-supports-request-proxying-and-filtering
author: ''
summary: Vercel Sandbox防火墙现已支持将特定HTTP请求转发至用户控制的代理服务器，用于日志记录、调试或请求/响应转换。新增的匹配器功能允许用户根据路径、方法、查询字符串或标头精细控制转发范围，仅对符合条件的请求进行代理。该功能以Beta版本面向Pro和Enterprise用户开放，需安装@vercel/sandbox@beta
  SDK。
categories:
- AI基础设施
tags:
- Vercel
- Sandbox
- 防火墙
- 请求代理
- 匹配器
draft: false
translated_at: '2026-05-11T05:59:53.283221'
---

Vercel Sandbox 防火墙现在支持将特定 HTTP 请求转发到您控制的代理服务器。您还可以使用匹配器将转发和凭证代理的范围限定为仅需要这些操作的请求。

### 请求代理

您现在可以通过自己的代理路由出站沙盒流量，用于记录、调试或转换请求和响应。在任何允许的域名上设置 forwardURL，防火墙就会将匹配的 HTTPS 请求转发到您的服务器。

代理服务器会收到原始请求以及用于标识来源的附加标头：

- `vercel-forwarded-host`：原始请求的 SNI
- `vercel-forwarded-scheme`：原始请求的方案
- `vercel-forwarded-port`：原始请求的端口
- `vercel-sandbox-oidc-token`：Vercel 颁发的 OIDC Token，代理服务器可用其验证请求并识别来源团队/项目/沙盒。在文档中了解更多信息

```
1import { Sandbox } from '@vercel/sandbox';2
34const sandbox = await Sandbox.create({5  networkPolicy: {6    allow: {7      "github.com": [{8        forwardURL: "https://my-custom-proxy.vercel.app/api/proxy"9      }],10      11      "*": []12    }13  }14});
```

### 匹配器

此外，您现在可以使用匹配器将请求转发或凭证代理限制为匹配特定路径、方法、查询字符串或标头的请求。这使您可以精细控制哪些请求会被转换；例如，仅将 POST 请求转发到特定的 API 路径，同时允许所有其他流量原样通过。

```
1import { Sandbox } from '@vercel/sandbox';2
345const sandbox = await Sandbox.create({6  networkPolicy: {7    allow: {8      "api.github.com": [{9        match: {10          path: { startsWith: "/v1" },11          method: ["POST"]12        },13        forwardURL: "https://my-custom-proxy.vercel.app/api/proxy"14      }],15      16      "*": []17    }18  }19});
```

这些功能目前以 Beta 版本形式提供给 Pro 和 Enterprise 套餐用户。

开始使用前请安装 `@vercel/sandbox@beta` SDK，并在文档中了解更多关于请求代理和匹配器的信息。

---

> 本文由AI自动翻译，原文链接：[Vercel Sandbox firewall now supports request proxying and filtering - Vercel](https://vercel.com/changelog/vercel-sandbox-firewall-now-supports-request-proxying-and-filtering)
> 
> 翻译时间：2026-05-11 05:59
