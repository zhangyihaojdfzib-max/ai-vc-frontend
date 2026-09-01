---
title: Chat SDK now supports Slack Enterprise Grid - Vercel
title_original: Chat SDK now supports Slack Enterprise Grid - Vercel
date: '2026-08-25'
source: Vercel Blog
source_url: https://vercel.com/changelog/chat-sdk-slack-enterprise-grid
author: ''
summary: '[翻译失败，原文如下]


  Chat SDK''s Slack adapter now supportsSlack Enterprise Grid.


  Bots installed org-wide work across every workspace, with correct token reso...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-01T07:32:13.288918'
---

[翻译失败，原文如下]

Chat SDK's Slack adapter now supportsSlack Enterprise Grid.

Bots installed org-wide work across every workspace, with correct token resolution, tenant-scoped caches, and event retry deduplication.

The adapter now stores org-wide installations by enterprise ID. This matches how tokens are resolved for incoming events, slash commands, and interactive payloads.SlackInstallationrecords the new identity fields:

```
const installation = await slack.handleOAuthCallback(request);
installation.teamId; installation.enterpriseId; installation.isEnterpriseInstall; 
```

Token resolution behaves the same over HTTP webhooks and Socket Mode. Events route by the installation identity in the envelope'sauthorizationsfield, which keeps routing correct for Slack Connect shared channels.

The adapter is also hardened for multi-workspace deployments:

- User profile and mention caches are scoped per installation, so one tenant's data never resolves for another.
- API calls made with an org-wide token pass the event'steam_idautomatically, which Slack requires for workspace-scoped methods.
- Retried event deliveries are deduplicated for 24 hours, covering Slack's Delayed Events redeliveries.
- Outgoing mentions accept W-prefixed Grid user IDs alongside U-prefixed IDs.

User profile and mention caches are scoped per installation, so one tenant's data never resolves for another.

API calls made with an org-wide token pass the event'steam_idautomatically, which Slack requires for workspace-scoped methods.

Retried event deliveries are deduplicated for 24 hours, covering Slack's Delayed Events redeliveries.

Outgoing mentions accept W-prefixed Grid user IDs alongside U-prefixed IDs.

Single-workspace installations are unaffected, andgetInstallationanddeleteInstallationwork unchanged for both install types.

Read theSlack adapter documentationto get started.

---

> 本文由AI自动翻译，原文链接：[Chat SDK now supports Slack Enterprise Grid - Vercel](https://vercel.com/changelog/chat-sdk-slack-enterprise-grid)
> 
> 翻译时间：2026-09-01 07:32
