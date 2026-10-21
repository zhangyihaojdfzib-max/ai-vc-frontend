---
title: 'Introducing tsrs: a Port of TypeScript to Rust'
title_original: 'Introducing tsrs: a Port of TypeScript to Rust'
date: '2026-10-20'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/typescript-rust-port/
author: ''
summary: '[翻译失败，原文如下]


  Cloudflare and VoidZero are now working withMax SchwenkÂ of Owner.com ontsrs, a
  Rust port of the TypeScript compiler. We are doing this w...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-21T06:58:07.765416'
---

[翻译失败，原文如下]

Cloudflare and VoidZero are now working withMax SchwenkÂ of Owner.com ontsrs, a Rust port of the TypeScript compiler. We are doing this work in close collaboration with the TypeScript team, and incubating tsrs as part of theOxc JavaScript compiler toolchain.

Our goal is to help developers spend less time waiting for their code to be checked and more time building. Making TypeScript faster and more memory-efficient also helps bring complete development environments to more places, including right in your browser.

To be clear, we arenotÂ forking TypeScript. We believe the TypeScript team should remain in full control of the languageâs design and direction. They have maintained a long-term vision while guiding TypeScriptâs adoption across the JavaScript community. We do not want to change that.

The TypeScript team can move quite fast on many things, but for some features they may spend years intentionally exploring options and making prototypes before picking the right implementation. A Rust port has to follow those decisions closely, or it will eventually fall apart and become incompatible. We have to preserve the TypeScript language strictly based on its original implementation â and the TypeScript team should remain solely responsible for deciding what that looks like.

## Performance and memory improvements

Early benchmarks of our Rust port of TypeScript are promising:tsrsÂ is up to 8xÂ faster and uses ~70%Â less memoryÂ compared to TypeScript 7.0Â when using the same number of type check workers:

![](/images/posts/f91a5231b8bc.jpg)

As you can see, the next version of TypeScript already brings many performance improvements, making TypeScript 7.1 beta up to 2.5x faster than TypeScript 7.0. Some of these optimizations were upstreamed fromtsrs, and weâre hoping to find more.

You may have seen recent benchmarks of different TypeScript ports with various performance claims, often due to using larger machine types and different options compared to TypeScriptâs defaults. We worked with the TypeScript team to ensurethe above benchmarksÂ are comparing the same configuration.

By default, tsrs ships with an adaptive configuration dependent on the machine type that uses more memory but is even faster:

![](/images/posts/d0c99f812c42.jpg)

## Trytsrs

TypeScript in Rust aims to be a faithful port of TypeScript. You can try an experimental release by installing thetsrsÂ package from npm:

```
npm install tsrs
npx tsrs
```

## Why now?

Weâve seen many attempts at porting TypeScript to other languages over the years. Because of the complexity involved, only one of the ports succeeded: the TypeScript teamâs port of TypeScript from JavaScript to Go.

However, frontier AI models can now do large-scale ports almost independently in a matter of days. We have now seen slopforks, faithful ports, and completely re-architected versions of TypeScript in Rust or C++. There is clearly a demand for even faster TypeScript.

## Why Rust?

You might be thinking: âTypeScriptâs Go port already made TypeScript 10x faster and far more memory efficient than the previous version written in TypeScript. Why isnât that enough?â

However, itâs not just about speed. Rust offers some unique advantages:running in WebAssembly. The Rust + Wasm story has always been strong, and one of the reasons comes down to the fundamentals of Rustâs language design. When you compile a Go program to Wasm, you have to compile Goâs garbage collectorÂ along with it. But Rustâs memory management model enables straightforward memory interactions between a WebAssembly guest and host. This is one of the key things that makes Rust a much better fit for the WebAssembly use-case: memory efficiency.

CloudflareÂ Workers have supported Wasm for a long time. Just a few weeks ago we announcedsupporting native Rust in WorkersÂ with the new Emscripten target for wasm-bindgen. When you run entire software build and deployment systems in tight loops on Workers, the benefits of a small memory footprint pay off quickly. It means you can run these workloads so efficiently that itâs now possible to run fully encapsulated development systems in places where they couldnât have been run before.

This enables new possibilities when combined with agents: You are now able to run a development toolchain end-to-end in a fully sandboxed environment on Cloudflare. But with Wasm, you can also run those environments safely client-side in your browser, or on an embedded device, or an IoT application.

## How will thetsrsÂ port be maintained?

First, we are working with Theo Browne to mergetsc-rsÂ andtsrsÂ into a single package that supports all of TypeScriptâs features including Language Server ProtocolÂ (LSP) and content mappers. Second, weâve seen a lot of success with how we maintainVinextÂ in sync with its upstream, Next.js. We explained how we do this ina recent blog post:

We will apply the same process to TypeScript, taking extreme care that we donât introduce diverging behaviors from upstream TypeScript. When we come across performance improvements, weâll attempt to contribute them back to the TypeScript Go codebase so everyone wins.

Finally, we recognize that there are some differences to the upstream version of TypeScript right now, like for example the order in which diagnostics are printed. We aim to reduce those differences to a minimum by the time we publish a stable release.

## Whatâs next?

Cloudflare is already the home of many free and open source Rust tools that power the JavaScript ecosystem, such as Vite, Rolldown, Oxlint, and Oxfmt. With more than 10 million developers building on Cloudflare, we care a lot about making the underlying developer toolchain faster, more portable, and easier to run in more places. We are excited to experiment with deepertsrsÂ integrations into our stack, for example for type-aware lint rules in Oxlint.

Like with Vinext, our goal is to runtsrsÂ as a well-maintained healthy open source project â without getting in the way of TypeScript itself. The Oxc team has already begun refactoring the codebase to make it faster, use less memory, and make it maintainable. We know the TypeScript team is taking this seriously â they are experimenting with memory and performance improvements fortsc. We are excited to collaborate with the TypeScript team and the JavaScript community to build the best and fastest implementations of TypeScript together.

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Introducing tsrs: a Port of TypeScript to Rust](https://blog.cloudflare.com/typescript-rust-port/)
> 
> 翻译时间：2026-10-21 06:58
