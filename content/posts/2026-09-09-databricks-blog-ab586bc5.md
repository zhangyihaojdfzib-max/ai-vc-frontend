---
title: 'Beyond embedding: How to secure AI/BI Dashboards for every viewer'
title_original: 'Beyond embedding: How to secure AI/BI Dashboards for every viewer'
date: '2026-09-09'
source: Databricks Blog
source_url: https://www.databricks.com/blog/beyond-embedding-how-secure-aibi-dashboards-every-viewer
author: ''
summary: '[翻译失败，原文如下]


  - One dashboard serves every viewer. A single entitlements table and the signed
  embed token''s __aibi_external_value determine which rows ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-10T07:13:52.544159'
---

[翻译失败，原文如下]

- One dashboard serves every viewer. A single entitlements table and the signed embed token's __aibi_external_value determine which rows each viewer can access, without creating a dashboard for every customer or repeating filters across queries.
- Access is granted through identity-provider groups, not manually maintained user lists. The application resolves an internal viewer's groups with an on-behalf-of token before minting the embed token.
- Default-deny and defense in depth. The pattern masks sensitive columns, refuses tokens for unentitled viewers, and uses Unity Catalog row filters to protect direct SQL access.

## The challenge

Embedding a Databricks AI/BI Dashboard in a customer-facing application is relatively straightforward: enable embedding, mint a scoped token in the backend, and render the dashboard with the client SDK. The foundational guide,How to embed Databricks AI/BI Dashboards in customer-facing applicationswalks through that process end to end.

The harder question is authorization: once a dashboard is embedded, which rows should each viewer see? A partner should see only its own data, while an internal team may see only its region. This guide shows how to enforce those rules.

This reference pattern combines several Databricks capabilities: __aibi_external_value, Unity Catalog row filters and column masks, and groups synchronized from an identity provider (IdP). It is a design pattern, not a single feature to enable.

## One rulebook, two enforcement paths

![image1.png](/images/posts/ed5ab683c86c.png)

The same entitlements table governs two paths: embedded dashboards accessed through the application, and direct SQL queries run by Databricks users.

## A concrete scenario

Consider a company that uses a shared "Open Accounts Receivable (AR) Tasks" dashboard for data across three regions: West, East, and Central. The dashboard serves two audiences.

- External operating partners, such as Acme Ops, Bolt Partners, and Core Logistics, have no Databricks login and access the dashboard through a white-label portal. Each partner should see only its own region, with contact emails masked.
- Internal teams are the company's employees, who sign in to Databricks. Finance needs access to every region, while a regional operations team sees only its own. Their access comes from identity-provider groups such as Okta or Entra ID, not from manually maintained user lists.

Five viewers share one dataset, each seeing a different slice: Acme Ops, Bolt Partners, Core Logistics, Finance, and a regional operations team. The examples below focus on Acme and Finance; the identifiers partner_acme, finance_all, and West represent those examples. Acme sees West with emails masked, while Finance sees all three regions in full, both from the same published dashboard.

## One table, one view, one dashboard

Access rules live in one place rather than being scattered across dashboards or queries. A dashboard per customer creates copies that can drift out of sync, while repeating filters in every query creates opportunities for mistakes.

The model consists of three objects:

- Base table `open_ar_tasks`holds one row per AR task, tagged with a region and a contact email.

- The entitlements table is the single source of truth for access.Each row identifies the region a scope can access and whether sensitive values should be masked. The viewer_scope column stores both external partner IDs, such as partner_acme, and internal group names, such as finance_all.

- Secured viewjoins the base table to entitlements, so a viewer sees only entitled regions, with emails masked when the flag is set.

In most deployments, an upstream entitlement system or an application-owned group-to-region mapping populates this table; it is not edited by hand for each viewer.

This avoids per-customer dashboards and filters repeated across queries. The rules live in a table that can be queried, audited, and changed without modifying the dashboard.

Applied per viewer, the secured view returns only what that viewer is entitled to:

Acme (external_value = partner_acme): West only, contact email masked.

Finance (external_value = finance_all): all three regions, contact email in full.

## Where __aibi_external_value comes from

The backend sets this value when it mints the embed token. It authenticates as a service principal and requests a scoped token from Databricks with two values: external_viewer_id, which identifies the viewer for auditing, and external_value, which represents the viewer's scope. Databricks signs the token, and the viewer cannot modify the embedded value, which is exposed to the dashboard SQL as __aibi_external_value. Because it holds the service principal's credentials, this backend is a trusted server-side component, never the browser, with those credentials kept in a secrets manager rather than in source control.

The key detail is whose identity runs the query. Embedded queries execute under the configured publishing identity, not the viewer's Databricks identity.

For external embedding, Databricks recommends individual data permissions and granting the service principal its own data access, so queries run as the service principal. (Publishing with shared data permissions instead runs queries as the publisher's credentials.) The view then narrows that access for each viewer through __aibi_external_value. Because the query runs as the service principal, is_account_group_member() cannot identify the actual person viewing the dashboard on the embed path.

The important detail is that external_value is not limited to a partner id. It can be any scope the backend signs into the token, for example partner_acme for an external partner or finance_all for an internal group (their group name).

Because the entitlements table holds partner ids and group names in the same column, one dashboard, one view, and one filter cover both.

Because the viewer never sees or sets the signed value, the viewer cannot change it. An unknown scope matches no rows, which provides default-deny behavior.

The same view and the same filter (WHERE viewer_scope = __aibi_external_value) serve both audiences. Only the source of that scope differs:

## Grant access to groups, not people

Organizations typically manage access through groups synchronized from an identity provider. When someone joins the Finance group in Okta, their access maps to finance_all automatically, and no data table is touched. In this example, finance_all maps to every region and ops_west maps to the West region.

How does the application learn which groups belong to the viewer? It cannot rely on SQL during embedding, because the query runs as the service principal and is_account_group_member() would check the wrong identity. The application must resolve the viewer's groups in the backend, which can see the viewer, before minting the token.

One option is to run the application on Databricks Apps with user authorization enabled.

For a logged-in internal user, the platform forwards trusted identity context to the backend, including the viewer's email and an on-behalf-of (OBO) token. The backend uses that token to call SCIM /Me as the viewer and read their groups.

This approach does not require administrator rights on the service principal, because the user is reading their own record. It does require user-authorization scopes, and Apps OBO is still maturing, so validate it against the target deployment before relying on it.

If no entitled group is found, fail closed and refuse to mint a token rather than fall back to a broader identity such as the raw email.

If a viewer belongs to multiple entitled groups, resolve the result deterministically. Define a precedence order, or map several groups to one canonical scope before minting the token, so the same viewer always receives consistent access.

[翻译失败，原文如下]

External partners are simpler. With no Databricks identity, their scope is a fixed partner id assigned at login. Same token, same filter, no lookup.

One limitation to design around: a signed token carries a single external_value. If a viewer belongs to several groups with different entitlements, one token can still represent only one scope. For the common one-role-per-person case, that is fine.

For a true multi-group union, use an all-access group or the direct SQL path below, where a row filter can OR across every group. A composite scope (such as JSON) can be packed into external_value, but then the parsing and matching move into the dataset SQL and remain bound by the 1 KB payload limit.

## Hardening the guarantees

Row filtering delivers the base behavior: each viewer sees only their rows. Three additional layers strengthen the controls, and all three read from the same entitlements table.

### Mask sensitive columns per viewer

Row-level security determines which rows a viewer can access. Masking determines which columns they can see, because external partners usually do not need the same level of detail as internal teams.

The mask_pii flag, true for partners and false for internal groups, drives the masking logic in the secured view (the CASE expression in the SQL above). The same dashboard can show an internal viewer the full email while showing a partner a masked value such as ****@example.com. When masking rules span many tables and grow complex, Unity Catalog column masks and attribute-based access control (ABAC) are the better long-term home; here the view keeps the example self-contained.

### Default-deny, and prove it

An unknown scope should return no dashboard rows and should not reveal anything about the underlying data structure: no error that hints at structure, no partial data, just an empty result. Stopping earlier is cleaner still: before the backend mints a token, it checks the entitlements table and refuses any scope entitled to zero rows. Just as important, the scope is derived from the authenticated viewer, never from a client-supplied parameter, so a viewer cannot request another tenant's scope.

Gating at token issuance prevents a denied viewer from ever receiving a token, which beats relying on the SQL filter as the only guard. Logging both successful token issuance and denied requests makes authorization decisions auditable: the denied viewer simply never appears, and even if a request slipped through, an unknown scope would still return no dashboard rows. Recording the external_viewer_id and its scope in those logs lets each authorization decision be traced back to a real customer or user during an audit.

### Protect the direct SQL path

The embed controls protect the application path. A Databricks user who queries the base table directly is a separate threat. Add a Unity Catalog row filter to the base table, keyed to the querying user's identity and groups. In this direct-query path, is_account_group_member() evaluates the actual user and can combine all of their entitled groups. The publisher exception in the function below (current_user() equal to the publishing identity) is a deliberate break-glass allowance for the identity that publishes or refreshes the dashboard, not a general operator bypass. It is optional and high-risk, so include it only where justified and approve it per deployment.

A column mask for sensitive fields works the same way. These Unity Catalog controls are separate from the embed path: embedded viewers are scoped through __aibi_external_value and the entitlements view, while direct workspace queries are protected by the Unity Catalog row filter, which evaluates the caller's identity and groups. Both enforcement points use the same entitlements table.

## Before building it

On "multi-tenancy."This is pooled, logical multi-tenancy: external partners are isolated from one another, while internal employees receive group-based (role-based) access within the company's own tenant. All data remains in shared tables; the token, the view filter, and the entitlements table enforce separation. The direct-SQL row filter extends the same guarantee outside the app.

When to use this pattern.Use this pattern when external partners without Databricks accounts and internal employees need to share one dashboard. If every viewer is an internal Databricks user, basic embedding with Unity Catalog row and column security may be sufficient.

Practical constraints and gotchas.Verify the following product limits and operational details against the current documentation before publication:

- Tokens are short-lived (1 hour),so the app has to refresh them, especially for a tab left open. The client SDK makes this easy: a getNewToken callback re-fetches from the /api/token endpoint as the token nears expiry.
- Keep `external_viewer_id` + `external_value` under 1 KB combined:compact identifiers, not JSON blobs or long emails.
- Rate limit of 20 dashboard loads per second per workspacefor external embedding. Worth knowing for a large B2B portal.
- Use a non-PII `external_viewer_id`.It lands in audit logs, so a stable customer or user id beats a full name or raw email.
- Downloads are on by default.Embedded viewers can export CSV, TSV, Excel, and PNG unless a workspace admin turns downloads off. Confirm that exported results match the viewer-restricted data expected.
- Provision account-level groups for the direct-SQL path.UC row filters and masks evaluate is_account_group_member() against account-level groups, not workspace-local ones. The embed path never calls that function.
- Watch large entitlements tables.For thousands of scopes or deep hierarchies, keep the join and mask expressions simple and lean on ABAC once rules get complex.

## Key takeaways

- Keep access rules in one entitlements table, and use it for both embedded dashboards and direct-SQL protection.
- Sign a viewer or group scope into __aibi_external_value; do not rely on user-editable filters.
- Use default-deny, masking, and Unity Catalog row filters as layered controls.
- Embedding is only the first step; designing and validating the access controls is the critical work.

## Call to action

Start with the foundational guide,How to embed Databricks AI/BI Dashboards in customer-facing applications, then apply the entitlement, masking, and default-deny patterns described in this post. For the underlying governance controls, see theAI/BI embedding docsplusUnity Catalog row filters and column masksandABAC guidance.

---

> 本文由AI自动翻译，原文链接：[Beyond embedding: How to secure AI/BI Dashboards for every viewer](https://www.databricks.com/blog/beyond-embedding-how-secure-aibi-dashboards-every-viewer)
> 
> 翻译时间：2026-09-10 07:13
