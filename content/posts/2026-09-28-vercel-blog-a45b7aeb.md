---
title: Search domains without authentication - Vercel
title_original: Search domains without authentication - Vercel
date: '2026-09-28'
source: Vercel Blog
source_url: https://vercel.com/changelog/search-domains-without-authentication
author: ''
summary: '[翻译失败，原文如下]


  ![](/images/posts/0beaaf27ce9f.jpg)


  ![](/images/posts/9fe11ec588f1.jpg)


  You can now discover domain names and check availability and pr...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-12T08:53:28.734141'
---

[翻译失败，原文如下]

![](/images/posts/0beaaf27ce9f.jpg)

![](/images/posts/9fe11ec588f1.jpg)

You can now discover domain names and check availability and pricing without signing in to Vercel or providing an access token. This works through the Vercel CLI and Domains Registrar API.

With theVercel CLI, search by keyword or domain fragment:

```
vercel domains search acmesite --limit 5
```

Find domain suggestions based on the keyword “acmesite” with the Vercel CLI.

With theDomains Registrar API, check up to 200 exact domain names in one request. The response shows whether each can be registered and, when available, its registration and renewal prices:

```
curl --request POST \  --url https://api.vercel.com/v1/registrar/domains/search \  --header 'Content-Type: application/json' \  --data '{"domains":["example.com","example.dev","example.app"]}'
```

Check registration and renewal pricing for specific domains with the API.

Authentication is still required to buy or manage domains.

Try the publicdomain search, or learn how toclaim a free domain with Pro.

---

> 本文由AI自动翻译，原文链接：[Search domains without authentication - Vercel](https://vercel.com/changelog/search-domains-without-authentication)
> 
> 翻译时间：2026-10-12 08:53
