---
title: Is Agentic now tailors its audit by site type - Vercel
title_original: Is Agentic now tailors its audit by site type - Vercel
date: '2026-09-16'
source: Vercel Blog
source_url: https://vercel.com/changelog/is-agentic-report-categories
author: ''
summary: '[翻译失败，原文如下]


  Is Agenticreports now let you view your checks through one of four site types: Docs
  & content, Business, App, or Commerce.


  For example, ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-16T07:28:53.135087'
---

[翻译失败，原文如下]

Is Agenticreports now let you view your checks through one of four site types: Docs & content, Business, App, or Commerce.

For example, the Commerce view highlights payment and checkout standards like x402, UCP, and ACP, while the App view highlights API discovery, authentication, error handling, and SDK support.

Your score stays the same in every view, and you can change views on an existing report without rescanning. Only the highlighted checks change, so you can focus on what matters for your kind of site while keeping scores comparable across sites.

To set the default view, add a single meta tag to your page's<head>:

```
<meta name="is-agentic-site-type" content="app">
```

Set the value to match your site type:

- contentfor Docs & content
- businessfor Business
- appfor App
- storefor Commerce

contentfor Docs & content

businessfor Business

appfor App

storefor Commerce

The tag only sets which view readers see first. It doesn't add points or change your score. If no type is declared, Is Agentic infers one and shows which type it chose.

Run a check atis-agentic.comor read thedocumentation.

## Contributors

Jonathan Hefner,Ben Sabic

---

> 本文由AI自动翻译，原文链接：[Is Agentic now tailors its audit by site type - Vercel](https://vercel.com/changelog/is-agentic-report-categories)
> 
> 翻译时间：2026-09-16 07:28
