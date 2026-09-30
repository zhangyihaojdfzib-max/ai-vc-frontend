---
title: Enterprise-managed auth for the Supabase MCP server
title_original: Enterprise-managed auth for the Supabase MCP server
date: '2026-08-24'
source: Supabase Blog
source_url: https://supabase.com/blog/enterprise-managed-auth-for-the-supabase-mcp-server
author: ''
summary: '[翻译失败，原文如下]


  Enterprise-managed auth for the Supabase MCP server is now generally available on
  Supabase Team and Enterprise plans. Built withAnthropic...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-30T08:14:54.480224'
---

[翻译失败，原文如下]

Enterprise-managed auth for the Supabase MCP server is now generally available on Supabase Team and Enterprise plans. Built withAnthropicandOkta, it moves access control for Supabase in Claude to your identity provider, so IT admins can grant, restrict, and revoke that access for the whole organization from one place.

Before, each person connecting Claude to Supabase approved their own OAuth consent, and only organization owners could authorize the connection at all. Now an admin authorizes the Supabase connector once, and every employee who signs in to Claude finds Supabase ready to use, scoped to the projects and permissions they already have.

## Access that follows each person's role#

Access is tied to the individual employee rather than the organization owner, so what someone can do through Claude matches what they can already do in Supabase:

- Developers and read-only members get working Supabase MCP access with the role they already have
- Every query and management action runs with that person's existing role and permissions in Supabase, nothing more than they'd already have signing in directly

## Manage Supabase in Claude like any other app#

Your security team already runs onboarding, offboarding, and access reviews through your identity provider, and those workflows now cover Supabase in Claude:

- Restrict Supabase MCP access to an Okta group instead of approving each connection by hand
- Offboard someone in Okta and their Supabase access in Claude goes with it
- Point a security review of AI tool usage at one centrally enforced policy instead of individual grants

Enterprise-managed auth joins SSO, project-scoped roles, and SOC 2 and HIPAA compliance as part of how enterprises run Supabase. And this is just the start, with SCIM-based provisioning for the platform on the roadmap.

## Get started#

Enterprise-managed auth is available today for organizations on a Supabase Team or Enterprise plan with Okta SSO enabled and a Claude Team or Enterprise plan.

- Get started with enterprise-managed auth

---

> 本文由AI自动翻译，原文链接：[Enterprise-managed auth for the Supabase MCP server](https://supabase.com/blog/enterprise-managed-auth-for-the-supabase-mcp-server)
> 
> 翻译时间：2026-09-30 08:14
