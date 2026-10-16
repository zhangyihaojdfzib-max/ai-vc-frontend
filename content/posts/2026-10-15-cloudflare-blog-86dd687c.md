---
title: A fully programmable secure web gateway
title_original: A fully programmable secure web gateway
date: '2026-10-15'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/programmable-gateway-dlp/
author: ''
summary: '[翻译失败，原文如下]


  Every secure web gateway on the market works the same way: traffic matches a condition.
  A terminal action fires. Allow, Block, Isolate, L...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:40:54.152555'
---

[翻译失败，原文如下]

Every secure web gateway on the market works the same way: traffic matches a condition. A terminal action fires. Allow, Block, Isolate, Log. This model has been the foundation of network security for nearly 30 years, and it handles the common case well. But it has a ceiling, and customers with complex environments hit that ceiling regularly.

Earlier this year, we shared our vision to build atruly programmable SASE platform. We also outlined how the termprogrammabilityÂ has become diluted by the security industry. Most vendors claim programmability because they have public APIs, Terraform providers, webhooks, and alerting. Cloudflare offers all of those things too,Â but thatâs not enough. True programmability means running your own code â arbitrary logic that you wrote for your specific environment â inline in the policy evaluation path, at the moment a security decision is made.

Today, weâre excited to announce Cloudflare is bringing true programmability to Cloudflare Gateway and DLP (Data Loss Prevention) by integrating it with the entirety of our edge computing platform. We are releasing a new type of Gateway action,Forward, and custom validation functions, available to all Zero Trust plans. These capabilities allow you to use a Cloudflare Worker to transform and manipulate traffic, or to bring your own data to policy evaluation.

## The trade-off that every security team faces

For as long as firewalls have existed, businesses have faced a binary choice. You can maintain your own security detection engine â your own firewall, your own proxy infrastructure â with high maintenance overhead and low portability, in exchange for maximum customization. Or, you can accept the constraints of a vendor, offloading the considerable maintenance cost, at the expense of flexibility to solve problems specific to your environment.

In six years of building Cloudflare Gateway, we have heard from thousands of customers struggling with this trade-off. A security team migrating access controls for a critical internal application needs to inject HTTP headers based on JSON Web Token (JWT) claims from their identity provider. The data exists in the request context, but Gateway cannot read the JWT and write the header. So the team stands up a pool of NGINX proxies solely to perform this transformation. That infrastructure now must be patched, monitored, and secured... indefinitely.

Another team wants a Slack notification the moment an employee signs up for a new SaaS service. The policy engine can detect the sign-up event, but it can only Allow or Block. So the team builds a Logpush-to-SIEM-to-Slack pipeline with a 5 to 15 minute delay and no guarantee of delivery. And piles on yet another piece of infrastructure.

Dozens of enterprise customers have asked for warning pages that prompt users for justification before allowing access to sensitive destinations. Most then want to customize the ensuing behavior based on additional context about who the user is and the level of access requested. But serving customized, dynamic responses from a policy engine is exceedingly difficult.

We have offered customers many extension points over the years. But along with every other firewall vendor, it is impossible to build features to cover threat vectors as quickly as they can appear. However, we also recognize that the best solutions are those which are infinitely extensible to your environment.

## Why only Cloudflare can solve this problem

Cloudflare is not just a firewall, or a secure web gateway, a content delivery network, or an edge service. Cloudflare is a composable compute platform. Cloudflare Workers already allows customers to run complex logic on our network edge from any of our 330+ locations worldwide.Cloudflare GatewayÂ already evaluates and enforces security policy on user traffic at those same locations, on the same machines, in the same data centers.

Only Cloudflare runs both distributed customer computeÂ and a full-featured secure web gateway and firewall in the same globally distributed network. We have the unique opportunity and ability to combine those functions into the industryâs firstcompletelyÂ programmable and customizable SASE platform.

Gateway and Workers were built on the same infrastructure from the beginning. When Gateway forwards traffic to a Worker, that dispatch is a local function call. There is no hairpinning. There is no additional latency from crossing a network boundary. This is the first time that customers will have absolute control over how their proxied traffic is processed, without compromise, using code that they can write and execute without maintaining any sort of infrastructure.

Standalone SASE providers without their own compute platform require you to deploy automation in a separate cloud, manually configure webhooks, and accept the round-trip latency and management overhead of stitching together disconnected systems. No other vendor in this space has a programmable edge compute platform co-located with their security gateway. As threats advance at AI-powered speed, this will provide much needed flexibility and agility for security organizations.

## Two Gateway entry points:ForwardÂ action andÂCustom Functions

A new Gateway action type calledForwardÂ and a new policy resource called aCustom FunctionÂ are two distinct ways to call a Worker from a Gateway policy. The Forward action is available in public beta today, and Custom Functions will be available before the end of the year.

### ForwardÂ action: traffic transformation and proxy

![](/images/posts/ac77fe5362ad.jpg)

You can customize HTTP traffic behavior with a newpolicy actionÂ calledForwardÂ that routes the matched HTTP request to a Worker as a proxy. Policies with theForwardÂ action are evaluated for trafficÂ allowed by HTTP policies. The first matchingForwardÂ rule will then be applied to your traffic, and the traffic will be sent to its bound Cloudflare Worker. The Worker acts as inline middleware: it receives the full headers and request body. Your logic can then choose to modify either one (or take another asynchronous action of some kind), forward the request to the origin, receive the response, can modify that too, and return the final response to the user.

```
import { WorkerEntrypoint } from "cloudflare:workers";
import type {
  GatewayMiddlewareContext,
  GatewayMiddlewareNext,
} from "@cloudflare/zt-types";

export class GatewayMiddleware extends WorkerEntrypoint {
  async handle(
    request: Request,
    context: GatewayMiddlewareContext,
    next: GatewayMiddlewareNext,
  ): Promise<Response> {
    // Read a value from the Gateway context
    const clientIP = context.srcIp;

    // Add headers before the request reaches the origin
    request.headers.set("X-Gateway-Client-IP", clientIP);

    // Forward upstream and get the response
    const response = await next(request);

    // Modify the response before it reaches the user
    response.headers.set("X-Processed-By", "gateway-middleware");

    return response;
  }
}
```

Gateway handles the TCP connections, TLS termination and re-encryption, certificate management, and HTTP version negotiation. The Worker is responsible only for the transformation logic. You get a customizable, proxy-like extension point for your existing security stack, with none of the operational cost of hosting a traditional HTTP proxy.

Your Workers also do not have to transform the request. A rule's sole purpose can be to proxy a request to a Worker that receives the full context of the matched request asynchronously: send a Slack message, write toR2, log to an external pipeline, call a webhook, update aKVÂ store. The traffic can continue to its destination, unbothered.

### Custom functions: inline policy evaluation

![](/images/posts/1fdf2826c335.jpg)

[翻译失败，原文如下]

A custom function calls out to a Worker inline during Gateway policy evaluation and returns a value. The function is then exposed as a selector in the Gateway policy builder, and the selector is evaluated against its values. The selector is usable in the condition of any network or HTTP Gateway rule, the same way a built-in selector likeSource IPÂ orContent CategoryÂ works today.

The Worker receives context about the request: source IP, destination, user identity, device posture, HTTP headers, and more, depending on the policy phase. The Worker returns a typed value (string, number, or boolean) that Gateway uses in rule conditions. The contract is simple: data in, value out.

Here is a custom function that parses a JWTAuthorizationÂ header and returns the user's role:

```
export class GatewayCustomSelector extends WorkerEntrypoint {
  async compute(ctx: GatewayContext): Promise<string> {
    const authHeader = ctx.request.headers.get("Authorization");
    if (!authHeader) return "anonymous";

    const token = authHeader.replace("Bearer ", "");
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.groups?.[0] ?? "unknown";
  }
}
```

With this function deployed, an administrator can create an HTTP policy rule:Custom Function "JWT Role" contains "finance_contractor"Â with an action of Allow. The custom function becomes part of the rule condition, evaluated alongside every other selector.

Custom functions are not limited to HTTP traffic. Because they receive identity, device posture, and connection metadata instead of the full HTTP request, you can use them in the Gateway Network policy rule builder with arbitrary Layer 4 port and protocol traffic as well.

The Worker itself can do anything a Worker can already do â call external APIs, read from KV or D1, or invoke Workers AI. But from Gateway's perspective, the function is deterministic: data in, value out.

#### When to use a custom function or aForwardÂ action

Custom functions are designed for quick, bounded, stateless evaluations of data which can return a shaped response. You should think of their use similarly to data that can already be evaluated in Gateway selectors; that is, calculations on data that exist within a set of criteria, e.g. âPorts within this range,â or âURL paths that match this regex pattern.â The power comes from being able to extend your structured evaluations with arbitrary or internal sources of data, for which youâll see some examples below.

TheForwardÂ action requires a little more planning and preparation. It can be used for powerful transformations inline with usersâ live requests, and can manipulate them in complex ways both on the egress and return to the origin service. These should be thought of as transformation functions, something that very few enterprise security proxies even conceptualize today. Workers that use theForwardÂ action should be targeted and designed carefully to avoid adverse effects on the end userâs overall experience.

## What you can build

### Purpose justification and interstitial pages

A Worker intercepts a request to a sensitive destination and returns an interstitial page requiring the end user to provide a written justification for access. The Worker callsCloudflare KVÂ to write a session with a TTL, so the user is only prompted once per configured period. It writes the user's identity and their stated justification toCloudflare D1, creating an audit trail. Or, you can useHyperdriveÂ to write that record to any internal database you already operate.

This has been one of our most-requested features for over four years. With a Worker able to process and manipulate HTTP traffic,Â it's easy to build to your own standards.

### Dynamic HTTP header injection

A custom function parses a JWT from the request'sAuthorizationÂ header, extracts the user's role or group membership, and returns it as a selector value. A Gateway rule matches on that value and sets anX-App-RoleÂ header on the upstream request. No NGINX proxy pool. No additional infrastructure to maintain.

### File inspection and logging

When a file download matches certain criteria, a Worker can send the file to a third-party sandboxing service for detonation and analysis. Or it can write the file in its entirety toCloudflare R2Â as a permanent record for later inspection, without the file ever leaving the Cloudflare network.

### Real-time alerting on policy match

A Worker bound to a Forward policy receives traffic whenever a data loss prevention (DLP) profile matches. The Worker sends a message to a Slack channel or PagerDuty endpoint with the user's email, the rule that fired, and the destination URL.

```
export default {
  async invoke(ctx: GatewayContext, env: Env): Promise<void> {
    await fetch(env.SLACK_WEBHOOK_URL, {
      method: "POST",
      body: JSON.stringify({
        text: `DLP alert: ${ctx.identity.email} triggered "${ctx.rule.name}" accessing ${ctx.request.url}`
      })
    });
  }
}
```

### Complex evaluation logic

Traditional expression builders for firewalls are not designed for the kind of computation some organizations need at evaluation time. If you maintain internal risk scoring systems that perform behavioral analysis across multiple data sources, or if you have complex maps of users, groups, and conditional memberships where multiple criteria must be independently true, you can use a custom function as the computational extension that evaluates all of that logic and returns a single value to Gateway.

## Performance and reliability

Because Gateway and Workers services run on the same machines in the Cloudflare network, dispatching to a Worker does not introduce a network hop. The performance impact is limited to the execution time of your Worker code itself.

When a custom function fails â throws an exception, times out, or returns an unexpected value â you configure the fallback behavior per function.DefaultÂvaluesÂ are required in the custom function contract, so that itâs easy to determine behavior.

## Availability and pricing

TheForwardÂ action and its integration with Workers are available in a public betaÂ starting today, withCustom FunctionsÂ expected to be available before the end of the year. At general availability, both will be available for all customers on all plan types.

Traffic dispatched to your Workers is billed as standard Worker requests. The feature works with Workers Free, Workers Paid, and Workers for Enterprise with no restrictions on functionality. Workers Free does have execution time limits and daily request limits, which is worth considering as you scale the volume of Gateway traffic you send to your Workers.

## DLP custom functions for inline detection validation

Afully programmable SASE platformÂ extends beyond just Gateway.Â Our DLP offering â already integrated across Gateway, AI Gateway, Email Security, and more â now supports custom outcomes through integrations with our Compute platform, as well.

Most data security products operate by looking for data that matches known patterns. Customers can typically define regular expressions, word lists, or similar to operate these detections. They can also improve confidence in matching through the use of keywords or context analysis on the request body. But these methods have a core flaw: these types of detections canonlyÂ tell you when something matches thepatternÂ of data relevant to your organization, not whetherthis specific instanceÂ of data is indicative of data exfiltration or misuse.

As attackers become increasingly advanced, and agents can be used to ruthlessly exploit systems, improving our ability to accurately detect patterns is not enough. To improve accuracy for the data that matters, you need to know whether the data in question is actively relevant to your organization.

[翻译失败，原文如下]

To solve this problem, most solutions leverage exact data match, but this comes with its own trade-offs. Customers must prepare, maintain, and transfer reference datasets, then decide how comfortable they are allowing a vendor to manage data from their most sensitive systems.Â

Custom validation functions for DLP bridges that gap, and theyâre available starting today. These custom functions allow customers to define their own validation logic, using their own source of truth, directly inside a Cloudflare Workerâ¦ and apply iteverywhereÂ they use DLP to protect their sensitive data.

### Credential and secret verification

When a DLP detection entry is matched, an outbound Worker can be dispatched to run validation logic prior to a policy enforcement decision. If you have profiles to detect the use of GitHub secrets, but only care about active secrets, you can use a Worker to first look up the status of a detectedÂ key, return a response from the appropriate GitHub endpoint, and then decide whether or not the DLP profile should match the traffic.

```
import {
  DlpValidation,
  type DlpValidationInput,
  type DlpValidationResult,
} from "@cloudflare/zt-types";

export class DlpValidationEntrypoint extends DlpValidation {
  async validate({ excerpt, start, end }: DlpValidationInput): Promise<DlpValidationResult> {
    const bytes = Uint8Array.from(atob(excerpt), (c) => c.charCodeAt(0));
    const token = new TextDecoder().decode(bytes.slice(start, end));

    const res = await fetch("https://api.GitHub.com/user", {
      headers: {
        Authorization: `Bearer ${token}`,
        "User-Agent": "dlp-GitHub-validator",
        Accept: "application/vnd.GitHub+json",
      },
    });

    if (res.ok) return { score: 1.0 }; // token is valid and active
    if (res.status === 401) return { score: "veto" }; // token is invalid, discard
    return { score: 0 };
  }
}
```

## What's next

This is just the beginning of the fully programmable SASE platform. We are actively working on increasing the entry points from which you can dispatch custom functionality to the entire Cloudflare One suite, with Email Security coming next. That doesnât mean weâre done building: this new architecture will make it easier for us to build first-party features into all Cloudflare One services faster, more flexibly, and with improved developer experience.

Itâs also getting easier every day toprotect your Workers, agents, and their trafficÂ using Cloudflare One. If you are an Enterprise customer who would like a strategy session for implementation, a preview of the coming functionality, or to be notified about the custom functions beta, please reach out to your account team.

Your organizational security can now do anything a Cloudflare Worker can do. We can't wait to see what you build.

- Review the Gateway and Workers integration documentation
- See example Worker scripts for use in Gateway
- Teach your agent to build with Gateway and Workers
- Learn more about Custom functionsÂ for DLP

- Cloudflare
- Abe Carryl

---

> 本文由AI自动翻译，原文链接：[A fully programmable secure web gateway](https://blog.cloudflare.com/programmable-gateway-dlp/)
> 
> 翻译时间：2026-10-16 06:40
