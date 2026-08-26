---
title: From all-or-nothing to task-based OAuth consent
title_original: From all-or-nothing to task-based OAuth consent
date: '2026-08-20'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/task-based-oauth-consent/
author: ''
summary: '[翻译失败，原文如下]


  Since June, developers have created thousands ofthird-party OAuth apps on Cloudflare,
  with more than a million authorizations since.Â Â


  ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T03:00:24.512666'
---

[翻译失败，原文如下]

Since June, developers have created thousands ofthird-party OAuth apps on Cloudflare, with more than a million authorizations since.Â Â

OAuth makes delegated access possible. It lets applications act on a userâs behalf without asking them to handle long-lived credentials or hand over a password. That model works well when an application can describe its access needs with a small set of scopes.Â

Developers use OAuth for SaaS integrations, internal tools, CLIs, and agents. Our permission model has become more granular over time to support better scoping of these different workflows. That is great for security, but it makes a purely all-or-nothing consent screen hard to justify.

Cloudflare OAuth already allows clients to request a subset of their configured scopes. But once the client made that request, the user could not narrow it any further on the consent screen. For the user on the consent screen, the experience was still an all-or-nothing one. If an application requested more access than a user was comfortable granting, their only options were to approve the full request, or deny outright.Â

![BLOG-3481 3.gif](/images/posts/47151c9cf4a0.gif)

MCP servers are a good example of this. An MCP server might request a broad set of permissions, because in theory an agent could use all of them. But most users would not want an agent to have that much access. Before this feature, the only way to handle this was for the app developer to build a custom scope selection screen before sending the user to our consent flow.

Today, weâre introducing OAuth scope customization. Client owners can mark specific scopes as optional when configuring an OAuth client, giving users the ability to grant a narrower subset of an applicationâs requested access at authorization time.

The OAuth spec already allows authorization servers to grant a narrower set of scopes than what was requested. We built on top of that flexibility to make this work cleanly for every existing app.

## More control, without overwhelming users

Our goal with introducing scope selection is to give security conscious users more flexibility to make the right choices for their use case, without turning the consent screen into a long scope checklist.Â

With scope customization:Â

- Developers can mark specific scopes on an OAuth client as required or optional
- At authorization time, users can deselect optional scopes from the requested set
- Required and optional scopes are evaluated against the scopes requested for that authorization flow
- If no optional scopes are requested, the consent experience stays the same
- By default, the consent screen still grants the full requested scope set.Â Â

![BLOG-3481 4.gif](/images/posts/1ff8ee9cec6c.gif)

## Scoping to the authorization request

One important detail is that required and optional scopes are evaluated only against the scopes requested in a specific authorization flow, not every scope configured on the client. That matters because OAuth clients do not always request their full configured scope set.

For example, a client might be configured withuser-details.read, workers-scripts.write, workers-kv-storage.write, andzone.read, while marking workers-kv-storage.write andzone.readas optional. If that client starts an authorization flow requesting all four scopes, the consent screen will evaluate all four. In that case,user-details.readand workers-scripts.write remain required, while the user can choose whether to grant workers-kv-storage.write andzone.read.

But if the client later requests only workers-scripts.write andzone.read, then only those two scopes are considered for that authorization flow.user-details.readand workers-kv-storage.write would not be shown or enforced, because they were not requested.

This keeps the consent screen focused on the task at hand, rather than every capability the application could request. It also means existing OAuth clients keep their current behavior by default: if a client does not opt into optional scopes, the consent flow remains unchanged.

## Configuring an OAuth client to use optional scopes

Developers can opt into scope customization when configuring an OAuth client. Scopes continue to be configured as they are today, and clients can now additionally specify which of those scopes are optional:Â

```
curl "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/oauth_clients" \
  --request POST \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  --header "Content-Type: application/json" \
  --data '{
    "client_name": "ACME Corp",
    "redirect_uris": [
      "https://acme.org/oauth/callback"
    ],
    "grant_types": [
      "authorization_code"
    ],
    "response_types": [
      "code"
    ],
    "token_endpoint_auth_method": "client_secret_basic",
    "scopes": [
      "user-details.read",
      "workers-scripts.write",
      "workers-kv-storage.write",
      "zone.read"
    ],
    "optional_scopes": [
      "workers-kv-storage.write",
      "zone.read"
    ]
  }'
```

In the example above, the client can request all four scopes, but the user may only opt out of theworkers-kv-storage.writeandzone.readscopes during consent.user-details:readandworkers-scripts.writeremain required if they are included in the authorization request.Â

If the client later requests onlyworkers-scripts.writeandzone.read, then only those two scopes are considered for that authorization flow.user-details.readandworkers-kv-storage.writewould not be shown or enforced because it was not requested.

![BLOG-3481 5.gif](/images/posts/c522db4ce1d2.gif)

## Building with partial grants in mind

When a user deselects any optional scopes and completes the authorization flow, the generated access token will only contain the scopes they consented to. For developers, this means you need to check the granted scope set after exchanging the authorization code, rather than assuming the full requested set of scopes was approved.

An app that handles a narrower grant gracefully, for example an agent that operates within whatever subset of permissions it receives, is one that users feel comfortable authorizing. Requesting only the permissions needed and marking the rest as optional is a good sign to users that your app respects their access decisions.

## Scopes for every Product

Over the next few weeks, we will be expanding our account & zone-level role surface to cover nearly every Cloudflare product. That means more API token roles, account membership options, and OAuth scopes, giving customers the tools to secure workloads with the right level of access.Â

## Build with Optional Scopes

Allowing developers and users to better restrict access through optional OAuth scopes is an important step toward a more flexible and trustworthy consent experience on Cloudflare. With optional scopes, developers can build more nuanced authorization flows, and users gain more control over what they approve.Â

To get started with Third Party OAuth, take a look at ourdocumentationor jump straight to the OAuth apps page in the dashboard andcreate your first OAuth app.Â

## Thank you to our amazing interns

This feature is one of the many that we built with the help of our1,111 interns. Congratulations to Miller Vargas and JosÃ© Enrique Rodriguez on your high impact contributions here. Miller is a senior at the University of Texas - Austin studying computer science and math; and JosÃ© is a senior at Universidad Panamericana studying engineering, data intelligence, and cybersecurity.

## Related tags

Follow on Social Media

- Cloudflare
- Miller Vargas
- JosÃ© Enrique RodrÃ­guez

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[From all-or-nothing to task-based OAuth consent](https://blog.cloudflare.com/task-based-oauth-consent/)
> 
> 翻译时间：2026-08-26 03:00
