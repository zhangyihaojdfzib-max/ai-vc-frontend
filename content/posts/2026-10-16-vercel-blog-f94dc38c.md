---
title: Deleted deployments are permanently removed sooner - Vercel
title_original: Deleted deployments are permanently removed sooner - Vercel
date: '2026-10-16'
source: Vercel Blog
source_url: https://vercel.com/changelog/deleted-deployments-are-permanently-removed-sooner
author: ''
summary: '[翻译失败，原文如下]


  Deployments deleted before they are 30 days old now have a shorterrecovery periodbefore
  permanent deletion. As developers deploy more fre...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-27T07:32:57.422216'
---

[翻译失败，原文如下]

Deployments deleted before they are 30 days old now have a shorterrecovery periodbefore permanent deletion. As developers deploy more frequently on Vercel, this reduces the buildup of old deployments on the Recently Deleted page.

For successfully built deployments, the recovery period is the time you have to restore them after deletion:

When the deployment is deleted

Time to restore after deletion

By retention policy before it reaches 30 days old

Same length as the policy. A 7-day policy gives you 7 more days.

Manually, less than 1 day after creation

1 more day

Manually, at least 1 day but less than 30 days after creation

Same as its age at deletion. Delete it 3 days after creation, and you have 3 more days.

Manually or by retention policy, 30 days or more after creation

30 more days, unchanged

After this time, deployments are permanently deleted and cannot be restored. Unsuccessful deployments may be permanently deleted sooner.

Learn more in thedeployment retention documentation.

---

> 本文由AI自动翻译，原文链接：[Deleted deployments are permanently removed sooner - Vercel](https://vercel.com/changelog/deleted-deployments-are-permanently-removed-sooner)
> 
> 翻译时间：2026-10-27 07:32
