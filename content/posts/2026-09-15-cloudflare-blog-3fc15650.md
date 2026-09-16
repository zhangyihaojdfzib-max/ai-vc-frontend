---
title: Give every teammate and agent the right level of access to your Workers
title_original: Give every teammate and agent the right level of access to your Workers
date: '2026-09-15'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/workers-granular-authorization/
author: ''
summary: "[翻译失败，原文如下]\n\nAs more teams â\x80\x94 and now agents â\x80\x94 build applications\
  \ on Cloudflare's Developer Platform, having the right access controls is crucial\
  \ t..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-16T07:28:47.882619'
---

[翻译失败，原文如下]

As more teams â and now agents â build applications on Cloudflare's Developer Platform, having the right access controls is crucial to allow you to ship safely. After all, the last thing you want is for an agent to make a change in production, just because it was granted more access than it needs.

Now, you can give a teammate or agent access to a specific Worker, so that they can only make changes to that application and no other resources in your account. Moreover, weâre giving you four new roles, so you can limit exactly what they can do:Â

What it allows you to do

When to use it

Metadata Read-Only

View resource lists, settings, and observability data like metrics, logs, and traces, without access to product content.

When you want to give a team member or agent access to observability data, so it can debug issues.But you donât want to give them access to your source code.

Content Read-Only

Read product content, such as Worker code or D1 database content, without the ability to modify it.

When you want to give a team member or agent access to the source code.But you donât want them to be able to make any changes to your Worker.

Editor

Read and write product content, and update settings. Cannot create or delete resources.

When you want to give a team member, agent, or your CI/CD system the ability to deploy changes to your Worker.But you want to prevent them from being able to delete the Worker.

Admin

Full control over resources, including creating, renaming, deleting, and granting access to other users.

When you want to give a team member or agent full access to your Worker, including the ability to delete it.ÂBut you donât want to grant access to any other Workers or resources in your account.

The new roles are available today, for all customers. You can assign them to a specific user, so when they log into the dashboard, they will only see the Worker you have given them access to. Or, you can create an API token with the scoped access, which you can give to your agent to ensure they only have access to that one application.Â

Hereâs an example of how to create an API token with permissions per Worker:Â

![image2.png](/images/posts/e4fffd0ce377.jpg)

## Roles designed for how teams build

When defining these roles, we wanted to strike the right balance. Overly broad roles force you to grant more access than intended, undermining the principle of least privilege, while providing too many individual permissions makes it difficult to know which ones to grant. We landed on four roles that reflect the levels of access you may want to give a person or agent: enough to debug a resource without exposing its content, read the content without changing it, make changes without being able to delete the resource, or fully manage it.

We plan to use these same roles as we bring resource-level access controls to other Developer Platform products, including D1, R2, and KV. Each role can be applied at one of three scopes. For example, if you set the âmetadata read-onlyâ control, hereâs what that would look like at different levels:Â

- Developer Platform level: Access to metadata for all Developer Platform resources.
- Product level: Access to metadata for every resource of one product, such as every Worker.
- Resource level: Access to metadata for one specific resource, such as one Worker.

The role and scope determine what someone can do and which resources they can do it to. Letâs take a look at how this would look in some common Workers workflows.

### Debug without exposing source code

To debug an issue, an engineer or agent might need to look at a Workerâs settings, metrics, logs, and traces to understand what went wrong. But they do not need to see the Workerâs code or make changes to it.

Metadata Read-Onlygives them access to that information without exposing the Workerâs source code. They can query analytics through the GraphQL API, access logs, and inspect traces and other observability data. Those requests only return data for the Workers they have access to. If an agent is scoped to one Worker, it can use the Cloudflare APIs to investigate an issue without seeing data from any other Worker in the account.

![BLOG-3357_Screenshot 2026-09-11 at 1.24.17â¯PM.png](/images/posts/c7e66e1a2e35.jpg)

As we bring these roles to more Developer Platform products, we plan to preserve that separation. Someone could inspect settings and observability data for a D1 database or R2 bucket without being able to read the values in the database or the files in the bucket.

### Review code without changing itÂ

A teammate or code review agent may need to read the code running in a Worker to understand how it works, investigate a bug, or review a proposed change. But that does not mean they should be able to deploy new code or update the Workerâs settings.

Content Read-Onlyprovides that separation. It lets them retrieve and review the Workerâs code without being able to modify or deploy it. When scoped to an individual Worker, they can read only that Workerâs code, rather than the code for every Worker in the account.

![BLOG-3357_Screenshot 2026-09-11 at 12.50.36â¯PM.png](/images/posts/3d035fe06ad7.jpg)

Once supported for other Developer Platform products, Content Read-Only will work the same way: someone could read the data stored in a D1 database, KV namespace, or R2 bucket without being able to modify it.

### Let CI deploy without giving it full control

A CI/CD workflow only needs access to the application it deploys. It should not be able to change another Worker or delete its own and take the application offline.

With Worker-level access controls, each workflow can have its own API token with theEditor role, scoped to one Worker. If the workflow is misconfigured or its token is exposed, the impact remains contained: it can deploy changes to that Worker, but it cannot delete it or touch any other application in your account.

![BLOG-3357_Screenshot 2026-09-11 at 12.49.50â¯PM.png](/images/posts/089f9b4e94e0.jpg)

### Delete a Worker with Admin access

Adminis the highest level of access you can grant. It allows you to delete an application. You can still scope the role to an individual Worker, so that access does not extend to every Worker in the account.

![BLOG-3357_Screenshot 2026-09-11 at 12.49.00â¯PM.png](/images/posts/1fde3e7153f0.jpg)

## Routes & Custom DomainsÂ

You can addroutesorCustom Domainsto a Worker to specify which hostnames are routed to that application. For example, this configuration in your Wrangler file sends traffic forexample.comto the Worker:

```
{
  "route": {
    "pattern": "example.com/*",
    "zone_name": "example.com"
  }
}
```

Because changing that route could redirect production traffic or take the application offline, access to the Worker alone is not enough. To add, change, or remove a route or Custom Domain, you need both Editor access to the Worker and Workers Routes permission for the zone.

Requiring Workers Routes permission, rather than broader access to the zone, means someone can manage how traffic reaches a Worker without being able to change unrelated settings for the domain.

However, once a route is configured, you can continue deploying new versions of the Worker without access to the connected zone or resource, as long as the deployment does not change that connection. This allows your CI/CD system to deploy the application without also giving it access to your domains, databases, or storage.

## Workers permissions extend to Durable Objects

Durable Objects do not have their own roles or permissions. Instead, access to a Durable Object is determined by your access to the Worker that implements it. To give someone access to a Durable Object, grant them the appropriate role for that Worker.

[翻译失败，原文如下]

Metadata Read-Only gives them access to Durable Object metrics, logs, and traces, but not the data stored in the object. Because Durable Objects Data Studio can query and modify that stored data directly, accessing it requires the Editor role.

## Better errors that tell you and your agents which permissions you need

When you give someone narrowly scoped permissions, they may eventually try to perform an operation they do not have access to. When that happens, the error should tell them what permission they need, so they donât get stuck.

Instead of returning only a generic 403 Forbidden response,our APIs now include a link to the relevant API documentation, where you can see exactly which permissions are required to make the request. This way, you and your agent can figure out exactly the right level of access thatâs needed without granting broader permissions than necessary.

## Available now

Worker-level access controls are available today for all customers. You can configure them in the Cloudflare dashboard, through the API, or with Terraform.

To give a team member access to a specific Worker, go toManage Account > Members, select the member, and create a policy with the role and Worker scope they need.

![BLOG-3357_Screenshot 2026-09-11 at 1.09.21â¯PM.png](/images/posts/707a659fb7b3.jpg)

### Manage team access with user groups

If several people on the same team or project need the same access, you can create aUser Groupinstead of assigning permissions to each person individually. Assign the policy to the group, then add the relevant members. Everyone in that group will automatically inherit that policy.

## Replacing legacy permissions for WorkersÂ

Previously, we used the following roles and permissions to manage access to Workers. Now that we are rolling out a consistent set of roles across the Developer Platform, we recommend using the new roles going forward.

Legacy Role

Member/API Token

Recommended new role

Workers Platform (Read-Only)

Member

Developer Platform Content Read-Only

Workers Platform Admin

Developer Platform Admin

Workers Scripts Read

API Token

Workers Scripts Edit

Workers CI Read

Workers CI Edit

Workers Observability Read

Workers Observability Edit

Workers Observability Telemetry Edit

Workers Tail Read

There is no deprecation date for the legacy roles and permissions. Existing assignments will continue to work, and we will provide advance notice before any deprecation. That said, we recommend starting to move to the new roles, since they're the ones that support granular, resource-level access.Â

## Whatâs next?Â

Worker-level access is the first step toward a more consistent authorization model across Cloudflare's Developer Platform.

Next, we are bringing the same resource-level access controls to more Developer Platform products, including resources like KV namespaces and D1 databases. Instead of granting someone access to every bucket or every database in an account, you will be able to scope access to the specific resource they need and pair that scope with the right role.

The same roles introduced for Workers will apply across these resources.

Check out ourdeveloper docsto get started.

- Cloudflare
- Dina Kozlov

---

> 本文由AI自动翻译，原文链接：[Give every teammate and agent the right level of access to your Workers](https://blog.cloudflare.com/workers-granular-authorization/)
> 
> 翻译时间：2026-09-16 07:28
