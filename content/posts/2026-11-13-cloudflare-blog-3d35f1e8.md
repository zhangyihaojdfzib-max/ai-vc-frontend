---
title: Kitesurf is now open source
title_original: Kitesurf is now open source
date: '2026-11-13'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/kitesurf-open-source/
author: ''
summary: '[翻译失败，原文如下]


  WeintroducedÂKitesurf, our stateless browser for AI agents that runs entirely on
  top of Workers, in August andfollowed upÂ in September w...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-14T08:49:30.625604'
---

[翻译失败，原文如下]

WeintroducedÂKitesurf, our stateless browser for AI agents that runs entirely on top of Workers, in August andfollowed upÂ in September with WebMCP support, new APIs, and improved compatibility. On every occasion, we mentioned our commitment to open sourcing it so that developers could run their own browser engine on their own Cloudflare accounts if they want to.

That promise is now real.Kitesurf is open source on GitHubÂ under the Apache 2.0 license.Â You can read the code, run it locally, change it, and deploy your own instance to Cloudflare Workers.

## A browser built for agents

Kitesurf runs entirely on Cloudflare Workers. It parses HTML, applies CSS, executes page JavaScript, and renders screenshots without a browser container. It supports the Chrome DevTools Protocol (CDP), so you can connect clients such as Puppeteer.

Our main goal is to give AI agents a lightweight, efficient browser â one that can load websites, execute JavaScript, and interact with pages while using less CPU and memory than a full browser like Chromium, and scaling on demand across Cloudflareâs global Workers network.

Read more about why and how we built Kitesurf in our initialannouncementÂ and how to use it in Browser RunâsdeveloperÂ documentation.

## What is inside the repository?

Kitesurf builds on Cloudflareâs Developer Platform and APIs, alongside an ecosystem of open-source Rust packages compiled to WebAssembly:

- BlitzÂ provides HTML parsing, the DOM, layout, and painting.
- StyloÂ provides CSS parsing, cascading, and computed styles.
- BoaÂ runs JavaScript inside WebAssembly (as the last resort only when we canât run JavaScript in Dynamic Workers).
- LinebenderÂ libraries provide text layout and 2D graphics, andKrillaÂ generates PDF output.

These projects made Kitesurf possible. They retain their respective licenses; the repository'sNOTICEÂ documents third-party notices.

Kitesurf has three main parts: the Engine manages browser sessions and client connections, PageScript runs the page and its JavaScript, and PageRenderer draws the result.

![](/images/posts/e2d635c9873c.jpg)

All packages, the engine, its Rust core, DOM shims, renderer, andKitesurf CLIÂ live separately in folders under the repositoryâspackagesÂ directory where you can explore how all the pieces fit together.

## Run your own Kitesurf

To run Kitesurf locally, follow the repository'sbuild requirements, then clone therepository, install dependencies, and start the engine:

```
git clone https://github.com/cloudflare/kitesurf.git
cd kitesurf
pnpm install --frozen-lockfile
pnpm run dev
```

The first build compiles the Rust core and its dependencies, so give it some time. Subsequent builds reuse the build cache. Finally wrangler starts a local development server athttp://127.0.0.1:8787. Open that address to try a page in Chrome DevTools, or use it programmatically.

You can usepuppeteerÂ with a NodeJS script:

```
import puppeteer from "puppeteer-core";

const browser = await puppeteer.connect({
  browserWSEndpoint: "ws://127.0.0.1:8787/devtools/browser",
});

try {
  const page = await browser.newPage();
  await page.goto("https://example.com/");
  await page.screenshot({ path: "page.png" });
} finally {
  await browser.disconnect();
}
```

Or you can point your AI harness at the localCDPÂ port (agents love CDP) and watch it take full control of Kitesurf.

## Deploy to your Cloudflare account

When youâre done changing and testing locally, you candeploy the engine to your own accountÂ and use Kitesurf from there instead of the Browser Run managed APIs we provide. Note that a Workers Paid plan is required because Kitesurf usesDynamic WorkersÂ to create isolated Workers for pages.

From the repository root:

```
pnpm run deploy
```

## Help us make it better

As with all of our open-sourced projects, Kitesurf lives in Github and we welcome forks andcontributions.Â However, note that Kitesurf is under heavy development and we are focusing on making the engine more compatible (check outWeb Platform Test evolution), more reliable, andefficient.

Start with thecontribution guidelinesÂ if you want to contribute. Open an issue with a minimal reproduction or a proposed approach, and get vouched by a maintainer before opening a pull request. Focused fixes with tests, clear evidence, and a well-defined scope are much easier to review than large rewrites or unrelated cleanup, but all contribution does not have to be code: a small page that reproduces a rendering bug, a failing automation workflow, or a clear documentation correction can help us move forward.

## Stay tuned

Kitesurf is evolving quickly. Stay tuned for updates in theblogÂ and ourchangelog, and keep an eye on the officiallanding pageÂ for the latest on standards compatibility inWeb Platform TestsÂ page andbenchmarks.

And come chat with the team onDiscord. Weâre building a browser for agents, and weâd love your help making it better.

## Related tags

Follow on Social Media

- Cloudflare
- Celso Martinho

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Kitesurf is now open source](https://blog.cloudflare.com/kitesurf-open-source/)
> 
> 翻译时间：2026-11-14 08:49
