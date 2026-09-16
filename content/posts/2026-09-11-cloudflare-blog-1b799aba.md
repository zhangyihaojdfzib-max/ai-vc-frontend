---
title: Introducing automatic remediation policies with Cloudflare CASB
title_original: Introducing automatic remediation policies with Cloudflare CASB
date: '2026-09-11'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/casb-policies/
author: ''
summary: "[翻译失败，原文如下]\n\nToday, weâ\x80\x99re making Cloudflare CASB more powerful\
  \ than ever by introducing automatic remediation policies. This means security teams\
  \ ca..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-16T07:28:47.781358'
---

[翻译失败，原文如下]

Today, weâre making Cloudflare CASB more powerful than ever by introducing automatic remediation policies. This means security teams can now design event-driven logic to revoke risky file shares and dispatch custom webhooks, without manual intervention.

When we launchedCloudflare CASB, a cloud access security broker, we wanted to provide security teams complete visibility into the posture of their SaaS applications before misconfigurations became incidents. With a quick, clientless integration, CASB surfaces risks like overshared files, dormant admin keys and tokens, OAuth apps with excessive permissions â continuously, across users in the organization.

For years,SaaS Security Posture Management(SSPM) tools such as Cloudflare CASB have functioned as a passive alarm system. Most SSPM tools tell you whatâs wrong but do not help you fix the issue, placing the burden on administrators to manage an ever-growing to-do list. A single misconfigured file-sharing policy across a Google Workspace tenant can generate thousands of findings in seconds, and even a disciplined team faces a window between detection and remediation measured in hours or days â more than enough time for a sensitive file to be downloaded, forwarded, or indexed.Â

With automatic remediation policies, CASB customers can now configure the actions that should be invoked immediately after a new finding is identified.

## Shifting from reactive to proactive

When we launchedmanual remediation actionsearlier this year, we gave security teams the ability to resolve misconfigurations directly from the Cloudflare dashboard. This removed the need for customers to log in to multiple SaaS portals to take action on the security and content findings detected by Cloudflare CASB. Still, this required a human to confirm and initiate each individual remediation â even if theyâd seen this exact finding type before.Â

CASB policies are a native automation engine built directly intoCloudflare Onethat takes action the moment a finding is detected. Security teams define their response logic once, whether that is revoking access to a file share, dispatching a webhook to your security operations center (SOC), or forwarding the event to a security orchestration, automation and response platform (SOAR). The engine handles matches automatically by executing the customer-configured action.

As an example, many organizations implement controls that prohibit files from being shared publicly. However, they may apply an exception to users and groups in their marketing department who are frequently required to collaborate with external parties. SSPMs allow their customers to be alerted of any files that are shared publicly in violation of their policy. With many solutions, this permitted behavior lands in a queue with hundreds of possible violations, forcing administrators to take action on each individual instance.Â

CASB policies are designed for exactly this scenario. Rather than waiting for a human to see and act on a finding, automation fires the moment detection happens. The public share is revoked within minutes, keeping the backlog of findings clean and clear.

## How CASB policies work

At their core, CASB policies are automated workflows that tell our scanning service what action to take when a new finding is detected. From there, the configured policy will tell CASB to either trigger a remediation action, send a webhook, or both. This gives organizations the flexibility to rely on native CASB remediation capabilities or their own internal automation services and communication channels â without having to take action in disparate platforms or create their own event processing system.

![View of the main CASB Policies page. From this view, policies can be created, updated, and deleted.](/images/posts/2ee4e2ccd464.jpg)

## How we built it

The architecture behind CASB policies is built entirely on the Cloudflare developer platform â the same platform available to every Cloudflare customer.

When a finding is detected, the findings engine enqueues an orchestration message to aCloudflare Queue. AWorkerconsumer then checks whether a policy configuration matches the incoming finding. If a match exists, it creates the corresponding job and hands it to the remediations pipeline, which runs onCloudflare Workflowsfor durable, fault-tolerant execution. That means jobs survive process restarts and retries are handled automatically.

Cloudflare Workflows also handle third-party API rate limits gracefully. If a vendor returns a rate limit error, the Workflow pauses for the appropriate backoff window and retries without dropping the job. Our target from detection to completed remediation is five minutes or less.

![System architecture diagram for CASB Policies backend system.](/images/posts/d57d79ef8ba7.jpg)

## How to create policies

To get started, navigate to the Cloudflare dashboard and create your first policy. Policies can include both a remediation and a webhook action, but at a minimum:Â

- Select the vendor.Select the vendor and integration or tenant this policy should apply to.
- Select the integration.You can hand-select specific integrations or set it to apply to all integrations for the selected vendor.Â
- Choose a finding type.Select the CASB finding type that should fire the policy.Â
- Choose an action.Once a trigger is selected, the available actions for that finding type are shown. There are two categories:Run remediations.First-party actions Cloudflare performs directly against the SaaS integration API. CASB currently supports remediation actions for Microsoft and Google Workspace file/folder finding types. Note that this may requireupgrading permissionson integrations to read/write.Send webhooks.Send finding details to configuredwebhook destinationssuch as Slack, Microsoft Teams, Jira, ServiceNow, Tines, or any custom HTTP endpoint your team uses.

- Run remediations.First-party actions Cloudflare performs directly against the SaaS integration API. CASB currently supports remediation actions for Microsoft and Google Workspace file/folder finding types. Note that this may requireupgrading permissionson integrations to read/write.
- Send webhooks.Send finding details to configuredwebhook destinationssuch as Slack, Microsoft Teams, Jira, ServiceNow, Tines, or any custom HTTP endpoint your team uses.

![Interface for creating a new CASB policy.](/images/posts/81f53a247f45.jpg)

### Example webhook format

```
{
  "id": "019f1755-23d0-7097-a9b5-fb2f82edbfc9",
  "type": "casb.finding_instance.policy_dispatch",
  "metadata": {
    "actor": "",
    "time_sent": "2026-06-30T07:01:34.066Z",
    "destination": "<example web hook reciver url>",
    "version": 1
  },
  "data": {
    "object": "finding_instance",
    "action": "policy_dispatch",
    "finding": {
      "id": "865184c0-9e17-411a-aa5a-a54995d70cb0",
      "severity": "High",
      "dashboard_url": "...",
      "type_name": "File publicly accessible with view access"
    },
    "asset": {
      "id": "019f1754-cff8-74f8-bbe7-ed0e8b8ffb73",
      "name": "q3_financial_report_preview.xlsx",
      "vendor": "<example vendor name>",
      "type": "File",
      "vendor_url": "<example vendor URL>"
    },
    "dlp": {
      "profiles": []
    },
    "metadata": {
      "access": "open",
      "download_count": 0,
      "download_url": "<example vendor file URL>",
      "effective_access": "open",
      "effective_permission": "",
      "file_name": "q3_financial_report_preview.xlsx",
      "full_path": "All Files/q3_financial_report_preview.xlsx",
      "is_password_enabled": false,
      "owned_by_created_at": "2022-11-01T09:24:17-07:00",
      "owned_by_enterprise_name": "Cloudflare CASB",
      "owned_by_id": "21665592646",
      "owned_by_role": "admin",
      "owned_by_user_name": "Cloudflare CASB",
      "preview_count": 0,
      "size": 42,
      "url": "<example vendor URL"
    }
  }
}
```

## Maintaining visibility and compliance

[翻译失败，原文如下]

Each policy action produces two categories of logs, visible under Insights in Cloudflare One.Â

Admin Activity logs.These capture changes to a policy definition: who created it, who edited it, who disabled it, and when. If a policy was turned off and a risk slipped through, this audit trail surfaces a timeline of the event.

Cloud & SaaS Security policies logs.This new class of logs captures the runtime outcome of policy invocations. This includes details like which finding triggered the policy, which file was acted on, whether it succeeded or failed, and the specific error if it did not â for example, a 401 Unauthorized or an API rate limit response from the vendor.Â

For compliance use cases, the execution log is the proof of fix. It ties a specific finding, like an overshared file (e.g. Q4_Financials.pdf), to a specific automated action and event timestamp.Â

## Get started

Customers can find CASB Policies in theCloud & SaaS findingssection of the dashboard today. Connect or update your Microsoft 365 or Google Workspace integration to Read-Write permissions, and create your first remediation policy.Â

In the coming weeks, weâll also be adding support for Custom Findings to CASB. Different organizations have unique needs when it comes to detection, and we want to give customers the ability to augment or define finding logic to fit those needs.Â

New to Cloudflare One?Sign up for 50 free seatsto get started with CASB, ortalk to our teamabout a deployment at scale. For full setup instructions, visit ourdeveloper documentation.

- Cloudflare
- Abe Carryl

---

> 本文由AI自动翻译，原文链接：[Introducing automatic remediation policies with Cloudflare CASB](https://blog.cloudflare.com/casb-policies/)
> 
> 翻译时间：2026-09-16 07:28
