---
title: 代码模式：用1000个Token为智能体提供完整API
title_original: 'Code Mode: give agents an entire API in 1,000 tokens'
date: '2026-02-20'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/code-mode-mcp/
author: ''
summary: 本文介绍了“代码模式”这一创新技术，旨在解决AI智能体使用外部工具时上下文窗口占用过大的矛盾。传统方式中每个工具都会消耗Token，而代码模式仅通过search()和execute()两个工具，结合类型化SDK和动态工作器，就能让智能体访问整个Cloudflare
  API，且固定占用仅约1000个Token，相比传统方式节省了99.9%的Token消耗。文章还宣布了开源相关SDK，供开发者构建自己的高效MCP服务器。
categories:
- AI基础设施
tags:
- AI智能体
- 模型上下文协议
- API集成
- 代码模式
- Cloudflare
draft: false
translated_at: '2026-02-21T04:21:01.892938'
---

# 代码模式：用 1,000 个 Token 为智能体提供完整 API

2026-02-20

- Matt Carey

![](/images/posts/688503df8561.png)

模型上下文协议已成为 AI Agent（智能体）使用外部工具的标准方式。但其核心存在一个矛盾：智能体需要许多工具来完成有用的工作，但添加的每个工具都会占用模型的上下文窗口，留给实际任务的空间就更少。

代码模式是我们首次引入的一种技术，用于减少 Agent（智能体）使用工具时的上下文窗口占用。它不再将每个操作描述为单独的工具，而是让模型根据类型化 SDK 编写代码，并在动态工作器加载器中安全地执行该代码。这段代码充当了一个紧凑的计划。模型可以探索工具操作、组合多个调用，并仅返回它需要的数据。Anthropic 在其《使用 MCP 进行代码执行》一文中也独立探索了相同的模式。

今天，我们推出一个全新的 MCP 服务器，用于整个 Cloudflare API——从 DNS 和 Zero Trust 到 Workers 和 R2——它使用了代码模式。仅通过 search() 和 execute() 这两个工具，该服务器就能够通过 MCP 提供对整个 Cloudflare API 的访问，同时仅消耗大约 1,000 个 Token。无论存在多少个 API 端点，其占用空间都保持固定。

对于像 Cloudflare API 这样的大型 API，代码模式将使用的输入 Token 数量减少了 99.9%。一个没有代码模式的等效 MCP 服务器将消耗 117 万个 Token——这超过了最先进基础模型的整个上下文窗口。

使用 tiktoken 测量的代码模式节省与原生 MCP 对比

您今天就可以开始使用这个新的 Cloudflare MCP 服务器。同时，我们还在 Cloudflare Agents SDK 中开源了一个新的代码模式 SDK，以便您可以在自己的 MCP 服务器和 AI Agent（智能体）中使用相同的方法。

### 服务器端代码模式

这个新的 MCP 服务器在服务器端应用代码模式。服务器不再导出数千个工具，而只导出两个：search() 和 execute()。两者都由代码模式驱动。以下是加载到模型上下文中的完整工具接口：

```javascript
[
  {
    "name": "search",
    "description": "Search the Cloudflare OpenAPI spec. All $refs are pre-resolved inline.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "code": {
          "type": "string",
          "description": "JavaScript async arrow function to search the OpenAPI spec"
        }
      },
      "required": ["code"]
    }
  },
  {
    "name": "execute",
    "description": "Execute JavaScript code against the Cloudflare API.",
    "inputSchema": {
      "type": "object",
      "properties": {
        "code": {
          "type": "string",
          "description": "JavaScript async arrow function to execute"
        }
      },
      "required": ["code"]
    }
  }
]
```

为了发现它能做什么，Agent（智能体）会调用 search()。它根据 OpenAPI 规范的类型化表示编写 JavaScript。Agent（智能体）可以按产品、路径、标签或任何其他元数据过滤端点，从而将数千个端点缩小到它需要的少数几个。完整的 OpenAPI 规范永远不会进入模型上下文。Agent（智能体）仅通过代码与之交互。

当 Agent（智能体）准备好行动时，它会调用 execute()。Agent（智能体）编写可以发起 Cloudflare API 请求、处理分页、检查响应并在单次执行中将操作链接在一起的代码。

这两个工具都在动态工作器隔离环境中运行生成的代码——这是一个轻量级的 V8 沙箱，没有文件系统，没有可能通过提示词注入泄露的环境变量，并且默认禁用外部获取。在需要时，可以通过出站获取处理程序明确控制出站请求。

#### 示例：保护源站免受 DDoS 攻击

假设用户告诉他们的 Agent（智能体）：“保护我的源站免受 DDoS 攻击。” Agent（智能体）的第一步是查阅文档。它可能会调用 Cloudflare 文档 MCP 服务器，使用 Cloudflare 技能，或直接搜索网络。从文档中它了解到：在源站前放置 Cloudflare WAF 和 DDoS 防护规则。

步骤 1：搜索正确的端点
search 工具为模型提供了一个 spec 对象：完整的 Cloudflare OpenAPI 规范，其中所有 $refs 都已预先解析内联。模型据此编写 JavaScript。这里，Agent（智能体）在区域上查找 WAF 和规则集端点：

```javascript
async () => {
  const results = [];
  for (const [path, methods] of Object.entries(spec.paths)) {
    if (path.includes('/zones/') &&
        (path.includes('firewall/waf') || path.includes('rulesets'))) {
      for (const [method, op] of Object.entries(methods)) {
        results.push({ method: method.toUpperCase(), path, summary: op.summary });
      }
    }
  }
  return results;
}
```

服务器在 Workers 隔离环境中运行此代码并返回：

```javascript
[
  { "method": "GET",    "path": "/zones/{zone_id}/firewall/waf/packages",              "summary": "List WAF packages" },
  { "method": "PATCH",  "path": "/zones/{zone_id}/firewall/waf/packages/{package_id}", "summary": "Update a WAF package" },
  { "method": "GET",    "path": "/zones/{zone_id}/firewall/waf/packages/{package_id}/rules", "summary": "List WAF rules" },
  { "method": "PATCH",  "path": "/zones/{zone_id}/firewall/waf/packages/{package_id}/rules/{rule_id}", "summary": "Update a WAF rule" },
  { "method": "GET",    "path": "/zones/{zone_id}/rulesets",                           "summary": "List zone rulesets" },
  { "method": "POST",   "path": "/zones/{zone_id}/rulesets",                           "summary": "Create a zone ruleset" },
  { "method": "GET",    "path": "/zones/{zone_id}/rulesets/phases/{ruleset_phase}/entrypoint", "summary": "Get a zone entry point ruleset" },
  { "method": "PUT",    "path": "/zones/{zone_id}/rulesets/phases/{ruleset_phase}/entrypoint", "summary": "Update a zone entry point ruleset" },
  { "method": "POST",   "path": "/zones/{zone_id}/rulesets/{ruleset_id}/rules",        "summary": "Create a zone ruleset rule" },
  { "method": "PATCH",  "path": "/zones/{zone_id}/rulesets/{ruleset_id}/rules/{rule_id}", "summary": "Update a zone ruleset rule" }
]
```

完整的 Cloudflare API 规范有超过 2,500 个端点。模型将其缩小到它需要的 WAF 和规则集端点，而没有任何规范进入上下文窗口。

模型在调用特定端点之前，还可以深入了解其模式。这里它检查区域规则集上可用的阶段：

```javascript
async () => {
  const op = spec.paths['/zones/{zone_id}/rulesets']?.get;
  const items = op?.responses?.['200']?.content?.['application/json']?.schema;
  // Walk the schema to find the phase enum
  const props = items?.allOf?.[1]?.properties?.result?.items?.allOf?.[1]?.properties;
  return { phases: props?.phase?.enum };
}
```

```javascript
{
  "phases": [
    "ddos_l4", "ddos_l7",
    "http_request_firewall_custom", "http_request_firewall_managed",
    "http_response_firewall_managed", "http_ratelimit",
    "http_request_redirect", "http_request_transform",
    "magic_transit", "magic_transit_managed"
  ]
}
```

Agent（智能体）现在知道了它需要的确切阶段：用于 DDoS 防护的 ddos_l7 和用于 WAF 的 http_request_firewall_managed。

步骤 2：对 API 进行操作
Agent（智能体）切换到使用 execute。沙箱获得一个 cloudflare.request() 客户端，可以向 Cloudflare API 发起经过身份验证的调用。首先，Agent（智能体）检查区域上已存在哪些规则集：

```javascript
async () => {
  const response = await cloudflare.request({
    method: "GET",
    path: `/zones/${zoneId}/rulesets`
  });
  return response.result.map(rs => ({
    name: rs.name, phase: rs.phase, kind: rs.kind
  }));
}
```

```javascript
[
  { "name": "DDoS L7",          "phase": "ddos_l7",                        "kind": "managed" },
  { "name": "Cloudflare Managed","phase": "http_request_firewall_managed", "kind": "managed" },
  { "name": "Custom rules",     "phase": "http_request_firewall_custom",   "kind": "zone" }
]
```

Agent（智能体）发现已存在托管DDoS和WAF规则集。现在它可以通过链式调用在单次执行中检查规则并更新敏感度级别：

```javascript
async () => {
  // 获取当前DDoS L7入口点规则集
  const ddos = await cloudflare.request({
    method: "GET",
    path: `/zones/${zoneId}/rulesets/phases/ddos_l7/entrypoint`
  });

  // 获取WAF托管规则集
  const waf = await cloudflare.request({
    method: "GET",
    path: `/zones/${zoneId}/rulesets/phases/http_request_firewall_managed/entrypoint`
  });
}
```

从搜索规范、检查架构到列出规则集、获取DDoS和WAF配置，整个操作仅需四次工具调用。

### Cloudflare MCP服务器

我们最初为独立产品构建了MCP服务器。需要管理DNS的Agent（智能体）？添加DNS MCP服务器。需要Workers日志？添加Workers Observability MCP服务器。每个服务器都导出固定数量的工具，这些工具映射到API操作。当工具集较小时这种方式可行，但Cloudflare API拥有超过2500个端点。任何手动维护的服务器集合都无法跟上这种规模。

Cloudflare MCP服务器简化了这一切。仅需两个工具、约1000个Token，即可覆盖API中的所有端点。当我们添加新产品时，相同的`search()`和`execute()`代码路径会自动发现并调用它们——无需定义新工具，也无需新建MCP服务器。它甚至支持GraphQL分析API。

我们的MCP服务器基于最新的MCP规范构建，符合OAuth 2.1标准，使用Workers OAuth Provider在连接时将令牌权限降级至用户批准的范围。Agent（智能体）仅获得用户明确授予的权限。

对开发者而言，这意味着您可以使用简单的Agent（智能体）循环，同时通过内置的渐进式能力发现机制，让Agent（智能体）访问完整的Cloudflare API。

### 上下文缩减方案对比

目前出现了多种减少MCP工具Token消耗的方案：

**客户端代码模式**是我们的首次实验。模型通过类型化SDK编写TypeScript代码，并在客户端的动态Worker加载器中运行。代价是要求Agent（智能体）具备安全沙箱访问权限。该模式已在Goose和Anthropic Claude SDK中以"可编程工具调用"形式实现。

**命令行接口**是另一条路径。CLI具备自文档化特性，能在Agent（智能体）探索时逐步展现能力。OpenClaw和Moltworker等工具使用MCPorter将MCP服务器转换为CLI，为Agent（智能体）提供渐进式能力展示。其局限性显而易见：Agent（智能体）需要shell环境——并非所有环境都提供此支持，且这会引入比沙箱隔离环境更广泛的攻击面。

**动态工具搜索**（如Anthropic在Claude Code中的实现）会筛选出与当前任务可能相关的小型工具集。这减少了上下文使用量，但需要维护和评估搜索函数，且每个匹配的工具仍会消耗Token。

每种方案都解决了实际问题。但对于MCP服务器而言，**服务端代码模式**综合了各方优势：无论API规模如何都保持固定Token成本、无需修改Agent（智能体）端代码、内置渐进式发现机制、在沙箱隔离环境中安全执行。Agent（智能体）只需用代码调用两个工具，其他所有操作都在服务器端完成。

### 立即开始使用

Cloudflare MCP服务器现已可用。将您的MCP客户端指向服务器URL，系统将重定向至Cloudflare进行授权并选择授予Agent（智能体）的权限。在MCP客户端中添加以下配置：

```javascript
{
  "mcpServers": {
    "cloudflare-api": {
      "url": "https://mcp.cloudflare.com/mcp"
    }
  }
}
```

对于CI/CD、自动化场景或偏好自主管理令牌的用户，可创建具有所需权限的Cloudflare API令牌。系统支持用户令牌和账户令牌，均可通过Authorization标头以Bearer令牌形式传递。

更多关于不同MCP配置设置的信息，请访问[Cloudflare MCP仓库](https://github.com/cloudflare/mcp)。

### 展望未来

代码模式解决了单一API的上下文成本问题。但Agent（智能体）很少仅与单一服务交互。开发者的Agent（智能体）可能需要同时访问Cloudflare API、GitHub、数据库和内部文档服务器。每个新增的MCP服务器都会带来我们最初面临的相同上下文窗口压力。

**Cloudflare MCP服务器门户**允许您在统一认证和访问控制的网关后组合多个MCP服务器。我们正在为所有MCP服务器构建一流的代码模式集成，无论网关后有多少服务，都能以相同的固定Token成本向Agent（智能体）提供内置渐进式发现能力。

---

> 本文由AI自动翻译，原文链接：[Code Mode: give agents an entire API in 1,000 tokens](https://blog.cloudflare.com/code-mode-mcp/)
> 
> 翻译时间：2026-02-21 04:21
