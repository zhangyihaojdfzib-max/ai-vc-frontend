---
title: The next generation of MCP
title_original: The next generation of MCP
date: '2026-08-06'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/mcp-v2/
author: ''
summary: '[翻译失败，原文如下]


  Over the last year and a half, theModel Context Protocol(MCP) has become the universal
  standard for how agents interact with external ser...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-19T03:07:51.675355'
---

[翻译失败，原文如下]

Over the last year and a half, theModel Context Protocol(MCP) has become the universal standard for how agents interact with external services.Â

But one of the main criticisms of MCP was that the protocol required a stateful connection between Client and Server. This evolved from MCPâs origins and thefirst STDIO transport,designed for local applications. When MCP Servers went remote, it translated the stateful connection that worked so well locally and transposed it onto web infrastructure. Building a well-behaved MCP Server meant managing request routing to sticky sessions, holding open streams, message replay, and generally more overhead and complexity than a traditional web server. This changes now.

The latest MCP2026-07-28 specificationwas released last week, together with updated TypeScript, Python, Go, and C# SDKs. MCP is now a fully stateless protocol. The specification, interaction model and SDKs have all been rewritten to leverage this new protocol and simplify usage. This means that MCP servers can now run in just a Worker, no stateful infrastructure needed, and customers benefit from the operational simplicity and reduced cost of less moving parts.Â

## A new MCP

At Cloudflare, our journey with MCP goes back to the very beginning. In March 2025, we released our McpAgent primitive forbuilding MCP servers with Cloudflare Agents SDK. Two months later, we ran anMCP Demo Dayshowcasing customers such as Asana, Atlassian, Block, Intercom, Linear, PayPal, Sentry, Stripe, and Webflow launching their own MCP Servers along with13 Cloudflare product-specific MCP servers. A year ago, we releasedMCP Server Portals, to help enterprises securely adopt MCP in their organisations.

Cloudflare Durable Objectswere uniquely positioned to be the best place to host these new applications. They are stateful servers that combine compute, persistent transactional storage (via embedded SQLite), and real-time coordination. They scale up on demand, hibernate when not in use, and keep the stateful connection needed by MCP for Agent-to-Human interaction.

McpAgentcombined with theWorkers OAuth Providerpackage was the best place to host remote MCP servers. However, it became apparent that MCP could be simpler, more efficient, and easier to host, while keeping all capabilities we have grown to love.

This release of the MCP 2026-07-28 specification has been months of work by the whole MCP team and the SDK maintainers. In this post, we will outline the protocol changes that matter most for developers, share testimonials from customers running it in production, and explain how to start building with the new specification.

## MCP is now stateless

Earlier MCP transports began with aninitializeandinitializedexchange that would start a session. A server could assign an Mcp-Session-Id header, and every subsequent request had to find the state associated with that session. In practice this meant that autoscaling infrastructure had to preserve active sessions, deployments had to drain or migrate them, and losing an active instance could force clients to reconnect or lead to broken sessions. Serverless platforms could run MCP servers, but only by adding coordination for a protocol session that most interactions never even needed.

The new protocol removes the required handshake, theMcp-Session-Idheader, and protocol sessions from the core request path. Each request carries the protocol version, client identity, and client capabilities it needs. A client that wants to inspect a server before making another request can callserver/discover, but this is optional.

That simple detail changes how an MCP server can be deployed. A request can arrive at a server, invoke a tool, prompt, or resource, and simply return the result. There is no protocol session to store. This removes a huge part of MCP complexity, while preserving all the functionality thatâs expected from it, making MCP servers easier to deploy, scale, and maintain over time.

This new specification thus also removes the need forMcpAgent. While Durable Objects remain the right primitive when an application itself needs state, MCP itself no longer requires a Durable Object to speak the protocol. Servers can scale faster on request scoped infrastructure such as Cloudflare Workers.Â

Cloudflare's Agents SDK has supported the new specification since day one. Customers and partners have used the release candidate on Cloudflare before the specification was finalized, giving us confidence that themigration pathfromMcpAgentto the newcreateMcpHandler(see below) works with production traffic.

![BLOG-3384 2.png](/images/posts/d93aabc6b9e8.jpg)

## Elicitation no longer needs an open stream

An MCP server sometimes needs more information before it can finish a request. For example, a deployment tool may need approval before releasing to production. A design tool may need the user to choose colors. A billing tool may need confirmation before issuing a refund. MCP calls this interaction anelicitation.

Previously, server-initiated requests such aselicitation/createdepended on an open stream. Deployment of such a server requires balancing the complexity around streams, cost, and request timeouts.

The new protocol reworks this withMulti Round-Trip Requests (MRTR). A server can return aninput_requiredresult that describes what it needs. The client collects the answer and retries the operation with that input. The original operation can then complete, without either side preserving a transport session between those requests.

This is a breaking change from the old way of doing elicitations. However, it is operationally much simpler to implement, and we believe that it will allow more developers to make use of this capability to build rich agentic applications.Â

![BLOG-3384 3.png](/images/posts/2a5a95b77d66.jpg)

## HTTP infrastructure understands MCP

MCP requests are JSON-RPC messages sent over HTTP, but information about the request previously lived only inside the JSON body. A gateway had to parse that body to learn whether a request calledtools/list, invoked a tool, or read a resource.

The new specification requiresMcp-MethodandMcp-Nameheaders on Streamable HTTP requests. For example, a tool invocation can look like this:

```
POST /mcp HTTP/1.1
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: search
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search",
    "arguments": { "q": "otters" }
  }
}
```

A gateway, rate limiter, or Web Application Firewall can now make decisions from headers without parsing arbitrary JSON. Operators can apply different rules to different methods or record tool-level metrics using the same HTTP primitives they already use elsewhere.

The specification also addsttlMsandcacheScopehints to results fromtools/list,prompts/list,resources/list, andresources/read. Tool catalogs are deterministically ordered, allowing clients to reuse them while keeping upstream prompt caches stable across reconnects.

![BLOG-3384 .png](/images/posts/0634c140f1fa.jpg)

## Authorization continues to evolve

The new specification also tightens MCP authorization. MCP now prefers pre-registered clients when the server and client already have a relationship, thenClient ID Metadata Documents(CIMD) for dynamic registrations, with Dynamic Client Registration (DCR) as a fallback. DCR is deprecated for new implementations and is slated for removal after summer 2027.

The specification also adoptsRFC 9207issuer identification. An authorization server advertisesauthorization_response_iss_parameter_supported: trueand includes iss in successful authorization responses. The client compares it with the issuer discovered before starting the authorization flow. This prevents an authorization response from one issuer from being confused with a response from another.

[翻译失败，原文如下]

There are several less visible changes that close gaps in production deployments. MCP clients now send the canonical server URI as the RFC 8707resourcein authorization and token requests. Tokens must be issued for, and accepted only by, that audience.Workers OAuth Providerimplements all these requirements for MCP servers on Workers. Just wrap your handler functions like so:

```
import { OAuthProvider } from "@cloudflare/workers-oauth-provider";

export default new OAuthProvider({
  apiRoute: "/mcp",
  apiHandler: mcpHandler,
  defaultHandler: authorizationHandler,
  authorizeEndpoint: "/authorize",
  tokenEndpoint: "/oauth/token",
  clientIdMetadataDocumentEnabled: true,
  resourceMetadata: {
    resource: "https://mcp.example.com/mcp",
    authorization_servers: ["https://mcp.example.com"],
    scopes_supported: ["mcp:read"],
  },
});
```

## A lifecycle for a maturing standard

The technical changes are only part of this release. MCP 2026-07-28 also introduces a formal feature lifecycle.

Features are classified as Active, Deprecated, or Removed. A deprecated feature must remain available for at least 12 months before it can be removed. Roots, Sampling, Logging, Dynamic Client Registration, and the legacy HTTP+SSE transport are deprecated in this release, but existing implementations have a defined migration window.

This policy gives teams a minimum amount of time to plan upgrades rather than react to sudden removals. It also gives the core protocol room to stabilize.

New ideas can move faster through the new extensions framework without immediately becoming part of the core protocol.MCP AppsandEnterprise-Managed Authorizationare already extensions, whileTaskshave been moved over to provide a path for reliable, long-running work. Implementers can adopt those capabilities as and when needed.Â

## A new MCP with new SDKs

In November 2025, we introducedcreateMcpHandlerto our Agents SDK, built on an experimental stateless mode in the MCP TypeScript SDK. This let MCP servers that only made use of tools, prompts, and resources be deployed to a Cloudflare Worker for lower complexity, cost and easier deployments.Â

We are happy to seecreateMcpHandlergraduate intothe official MCP TypeScript SDKwith this release!

In early 2026, we also worked with MCP maintainers on replatforming the MCP TypeScript SDK from Node.js to Web Standards, helping to improve interoperability with alternative JavaScript runtimes like Bun, Deno, and Cloudflare Workers. We contributed bundling, runtime shims, and split packages in the TypeScript SDK, lowering deployment sizes and benefitting the whole ecosystem.

Customers can migrate to the new specification whilst keeping backward compatibility with older specifications. The/mcpendpoint accepts both the new protocol and stateless requests from 2025 Streamable HTTP clients, so most clients can reconnect without configuration changes.

For example, in February we released our Code ModeMCP Server for the entire Cloudflare APIusing this unofficial stateless mode and the (catchy)WebStandardsStreamableHTTPServerTransport. Since then, it has scaled up to thousands of requests per second and served billions of tool calls.Â

Here is the shape of a minimal server using the official SDK and theCloudflare Agents SDK:

```
import { McpServer } from "@modelcontextprotocol/server";
import { createMcpHandler } from "agents/mcp/server";
import { z } from "zod";

function createServer() {
  const server = new McpServer({
    name: "hello-server",
    version: "1.0.0",
  });

  server.registerTool(
    "hello",
    {
      description: "Return a greeting",
      inputSchema: { name: z.string().optional() },
    },
    async ({ name }) => ({
      content: [
        {
          type: "text",
          text: `Hello, ${name ?? "World"}!`,
        },
      ],
    }),
  );

  return server;
}

export default {
  fetch(request, env, ctx) {
    return createMcpHandler(createServer)(request, env, ctx);
  },
}
```

Servers that truly depend on legacy protocol sessions, server-to-client requests, or standalone streams need a more deliberate migration. They can run a strict stateless route beside the existing sessionful route, move features over, allow active sessions to drain, and then remove the legacy path during the deprecation period. OurMCP SDK v2 migration guidecovers that process. For MCP clients the process is even easier: just upgrade your version of agents, and it will just work.Â

ThecreateMcpHandlerAPI began in the Agents SDK, and will continue to live there. We will also continue to wrap the upstream handler to provide a Worker-focused interface with functional defaults and richer interaction patterns than the lower level MCP TypeScript SDK.

## Next gen MCP is already in production

David Cramer, co-founder and chief product officer atSentry, is a noted voice on boththe promise of MCPand itsearly opportunities for improvement. In his early real-world experience, the latest MCP spec delivers on that promise while addressing the early criticism.

"We built Sentry's MCP on Cloudflare's SDK. Big fans,â Cramer told us. âWe went live with this new one before the 7-28 spec was even finalized, and it didn't break prod. Big fans of that, too. This new spec cleans up a bunch of the nonsense around auth and tools, which is exactly what I wanted. Agents only get useful once the plumbing stops being the whole story."

Linearbuilds a fast, modern issue tracking and project management tool. Theyâve adopted MCP to let agents access Linear data in a simple and secure way.

âMCP is a clear example of why open standards matter,â said Tom Moor, Head of Engineering at Linear. âThe latest iteration of the spec is a great improvement that makes hosting an MCP server easier, more reliable, and at the same time adds much needed functionality. I still think MCP is massively underestimated â we built our server once on the standard and it works with whatever AI client our users want to bring. Linear's stance has always been to make your Linear data accessible wherever you need it and the shared spec makes that possible without building hundreds of integrations.â

Anthropiccreated MCP and donated it to theAgentic AI Foundation. For the team that started the protocol, the new spec is a measure of how far it has come, and of how much the community now carries it forward.

âWe donated MCP to the Agentic AI Foundation so it could become open, vendor-neutral infrastructure for the whole ecosystem. MCP is now foundational for agentic software. Itâs the layer applications build on to connect with the tools and data people rely on every day and this is the most significant advance to the protocol since launch. Clients gain meaningful performance with minimal engineering work.

Security follows the same proven standards that protect the rest of the internet. Maintainers and contributors from across the community, drawing on real production experience at enterprise scale, made that possible. We can't wait to see what developers build on MCP." said David Soria Parra, Co-creator and Lead Maintainer of MCP, and Member of Technical Staff at Anthropic.

## Long live MCP

The new MCP specification is available for both clients and servers on Cloudflare today. You can run a stateless MCP server in aCloudflare Worker, secured withWorkers OAuth Providerand connect to an MCP client in anAgent. UseCloudflare Durable Objectswhen your application actually needs coordinated state, and serve new and legacy stateless clients from the same route while users migrate.

Install the latestAgents SDKand the MCP TypeScript server SDK, follow themigration guide, or start with thecreateMcpHandlerdocumentation. You can also connect to Cloudflare'sMCP servers, which already support the new specification.

[翻译失败，原文如下]

MCP no longer needs stateful infrastructure to do useful, interactive work. Servers can run as an ordinary HTTP workload on Workers, close to users, with the scale, security, and observability primitives developers use for the rest of the web.

## Related tags

Follow on Social Media

- Cloudflare
- Matt Carey

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[The next generation of MCP](https://blog.cloudflare.com/mcp-v2/)
> 
> 翻译时间：2026-08-19 03:07
