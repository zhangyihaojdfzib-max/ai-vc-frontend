---
title: "How we rebuilt Cloudflare Workersâ\x80\x99 module registry for Node.js compatibility"
title_original: "How we rebuilt Cloudflare Workersâ\x80\x99 module registry for Node.js\
  \ compatibility"
date: '2026-09-09'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/workers-module-registry-nodejs/
author: ''
summary: "[翻译失败，原文如下]\n\nWeâ\x80\x99ve rewritten the module registry inworkerd, the\
  \ core open-source component of the Workers runtime, to be faster, more standards-comp..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-10T07:13:42.670019'
---

[翻译失败，原文如下]

Weâve rewritten the module registry inworkerd, the core open-source component of the Workers runtime, to be faster, more standards-compliant, and more closely aligned with Node.js' module registry.

Over the past few years, weâve been adding support formoreandmoreNode.js runtime APIs. The Workers runtime now supports every stable API from Node.js that you might want to use in a serverless context, and these APIs are nowenabled by default, letting you deployeven larger Node.js appsto Cloudflare (now up to 64 MiB on all plans â weâve removed the limit on compressed bundle size).

But API compatibility alone is not enough: Node.js applications also depend on how the runtime resolves, loads, and cachesmodules. ESM, CommonJS, and WebAssembly are each types of modules that you can import in your Workerâs code. The system within the runtime that handles all of this is called the module registry.

You can start using it today by enabling thenew_module_registrycompatibility flagin your Worker.

```
{
  "compatibility_flags": ["new_module_registry"]
}
```

When you enable thenew_module_registrycompatibility flag:

- import.meta.url,import.meta.main, andimport.meta.resolve()all work.
- Module specifiers are parsed and resolved as real URLs, including query strings and fragments.
- node:built-ins resolve to the same module instance no matter how you reach them.
- Import attributes (with { type: 'json' }) are correctly validated.
- require()on an ES module follows Node.js'require(esm)rules.
- Errors use consistent classes and messages regardless of which loading path triggered them.
- Modules compile lazily when first imported (statically or dynamically).
- WebAssembly modules support source phase imports.

For the full deep-dive on how this new module registry interacts with V8âs module APIs, weâve addedreference docs to workerdthat break down everything in detail. But for most people building on Workers,Â you want to understand how these changes improve compatibility and help you build. To do that, weâll dive into each of these changes in the sections below.

## How the Workers runtime loads the code you give it

When you deploy a Worker to Cloudflare,wranglerorViteâbundlesâ all of your Workerâs code from many files and dependencies into one or many modules, which are then uploaded to Cloudflare when you runwrangler deploy.

By default, Wrangler bundles nearly all of this code into a single module script. It runsesbuildunder the hood, which processes then inlines relative imports andrequire()calls for most npm dependencies into that one file. Theimportandrequire()statements are replaced with regular functions as part of the process. By the time that bundle reaches the Workers runtime (workerd), there usually isn't much of a module graph left for the Workers runtime to deal with. Most of the different modules are bundled into one file. We have seen these scripts grow to as many as multiple hundreds of thousands of lines long.

![BLOG-3480_image4.png](/images/posts/70415077c2a9.jpg)

Why is it necessary to bundle many modules into a single file before uploading server-side code to Cloudflare? It has been technically possible to upload multiple modules, and even modules of different types, in the Workers runtime for many years now. However, the runtime has not resolved modules in a way that was consistent with all the other runtimes. If, for example, your code or dependencies usedimport.meta.resolve()to resolve the path to another module, that code would fail becauseimport.meta.resolve()was not supported.

When you use theCloudflare Vite plugin,Vite 8bundles your code usingRolldown, instead of Wrangler bundling your code usingesbuild. Rolldown resolves imports and npm dependencies, converts CommonJS to ESM where necessary, and emits an entry module plus any additional chunks created through code splitting, such asdynamic imports. As a result, the Workers runtime receives a smaller, build-generated module graph rather than the applicationâs original source graph.

![BLOG-3480_image3.png](/images/posts/ba977623c4e5.jpg)

The new module registry implementation in the Workers runtime opens the door to bundlers like Rolldown to perform fewer transformations, and to rely more on the runtime to handle module resolution.

When you import a Node.js API in your worker, by default you are importing a module that is built intoworkerd. It is not bundled into your code as a polyfill. Wasm, text, and binary modules are provided to the Workers runtime as separate files too. They are referenced by specifier instead of being inlined. And if you deploy with--no-bundle, or your tooling uploads a Worker as multiple modules directly, the full module graph shows up at runtime exactly as you wrote it.

![BLOG-3480_image2.png](/images/posts/f4bc7e48520f.jpg)

In all of these cases, something has to take a specifier, work out what code it actually points to, compile it, and hand V8 a module object it can link and run. Inworkerd, that's the module registry's job.

## Why a new implementation?

The original registry resolves specifiers as filesystem-style paths, not URLs. That sounds like a minor distinction, but it ruled out a bunch of things: there was no clean way to implementimport.meta.url, relative imports didn't follow the same resolution rules asnew URL(), and protocols likenode:andcloudflare:were handled as special-cased string prefixes instead of, well, protocols.

It also compiles your entire Worker bundle up front, whether or not a given module ever gets imported, and it keeps a separate, private copy of everything per V8 isolate. Cloudflare runs multiple V8 isolate replicas of the same Worker to spread load across CPU cores, so in practice that meant compiling the exact same source more than once, with keeping multiple copies of the source in memory.

None of this is really a bug, but it made it difficult to evolve the implementation without breaking changes. The new registry starts from URLs as the specifier format and treats laziness and cache sharing as things to design in from day one. The existing registry implementation is not going anywhere. Currently, deployed Workers will continue to work as they always have.

## import.meta

Theimport.metaAPI provides information about the module, such as the module's URL, and whether it is the main entry point module:

```
export default {
  async fetch(request) {
    return new Response(`${import.meta.url}, main: ${import.meta.main}`);
  },
};
```

That prints something likefile:///bundle/index.js, main: true.Â

import.meta.mainis true only for the module configured as your Worker's entrypoint; every other module getsfalse.

import.meta.resolve()resolves a specifier against the current module without importing it:

```
import.meta.resolve('./utils.js');       // 'file:///bundle/utils.js'
import.meta.resolve('./a/../utils.js');  // 'file:///bundle/utils.js' (dot segments collapse)
import.meta.resolve('fs');               // 'node:fs' (recognizes bare node.js built-ins too)
```

It's a pure string transform, same as in Node.js and in browsers: it doesn't check that the resolved URL corresponds to a real module, and it throws aTypeErrorfor a specifier that can't be parsed as a URL at all, rather than returningnull. One detail worth knowing if you ever look closely at the output: it normalizes percent-encoding the same waynew URL()does, which means it collapses paths like./a/../b.js, but it does not decode characters that were already percent-encoded.import.meta.resolve('%66oo.js')resolves tofile:///bundle/%66oo.js, notfile:///bundle/foo.js.

## Specifiers are URLs

Relative imports now resolve the same way asnew URL(specifier, base)would, because that's literally what's happening under the hood. Full URLs work as specifiers too, not just relative paths:

```
import { helper } from 'file:///bundle/utils.js';
```

[翻译失败，原文如下]

The more interesting consequence is what happens with query strings and fragments. Per the same module-identity rules browsers use, a specifier with a different query string or fragment is treated as a genuinely distinct module instance, even when it points at the same underlying source:

```
// counter.js
let n = 0;
export function increment() {
  return ++n;
}
```

```
import { increment as incA } from './counter.js?a';
import { increment as incB } from './counter.js?b';

incA(); // 1
incA(); // 2
incB(); // 1, a separate instance with its own copy of `n`
```

./counter.js?aand./counter.js?bload the same source, but they're evaluated separately, each gets its ownimport.meta.url, and each gets its own copy of any top-level state. Importing the same specifier with the same query string again still gets you back the same instance, so this isn't a way to force re-evaluation on every import.

## Import attributes are correctly validated

```
import data from './config.json' with { type: 'json' };
```

The original module registry implementation silently ignores the import attributes in violation of the spec. It is expected that implementations throw an exception when any import attribute it does not understand is used.

jsonis the only import attribute type enabled right now, since it's the only one of the relevantTC39proposals that has reached Stage 4.textandbytesare recognized, because they track theImport TextandImport Bytesproposals, but they're rejected with a specific error instead of being silently ignored or treated as unsupported syntax:

```
import msg from './message.txt' with { type: 'text' };
// TypeError: Import attribute type "text" is not yet supported
```

Any attribute key other thantypeis now a hard error too, rather than being ignored:

```
import data from './config.json' with { type: 'json', cache: 'no' };
// TypeError: Unsupported import attribute: "cache"
```

And if the type you specify doesn't match what the module actually is:

```
import data from './utils.js' with { type: 'json' };
// TypeError: Module "./utils.js" is not of type "json"
```

## require(esm)follows Node.js' rules

If yourequire()something that turns out to be an ES module, whether that's directly inside a CommonJS module or throughrequire('node:module').createRequire(), the registry follows Node.js'require(esm)behavior:

- If the module has a string-named export called'module.exports', Node.js' actual mechanism for letting an ES module control what require() sees, that value is returned.
- Otherwise,require()returns the module's namespace object.
- The one exception isworkerd's ownnode:built-ins. They're implemented as ES modules that wrap a CommonJS-style API in a default export, so requiring one returns that default export directly.require('node:buffer').Bufferbehaves the way you'd expect; you don't get a namespace object with a.defaultyou need to unwrap yourself.

```
// utils.mjs
const impl = { hello: 'world' };
export { impl as 'module.exports' };
export default 'not this';
```

```
import { createRequire } from 'node:module';

const myRequire = createRequire(import.meta.url);
myRequire('./utils.mjs'); // { hello: 'world' }, not the module namespace
```

There's a restriction that comes along with this: if the module you're requiring, or anything in its module graph, has a top-levelawait, require()throws instead of blocking or handing back something half-finished:

```
// async-init.mjs
await Promise.resolve();
export const ready = true;
```

```
myRequire('./async-init.mjs');
// Error: Top-level await is not supported in this context for module: file:///bundle/async-init.mjs
```

This matches Node.js' ownERR_REQUIRE_ASYNC_MODULErestriction:require()has to return synchronously, and there's no reasonable value to hand back for a module that hasn't finished evaluating yet. Useimport()for anything async instead. The check holds regardless of import order too: a module doesn't becomerequire()-able just because something alreadyimport()'d and fully evaluated it earlier.

If you're requiring output from a bundler that predates Node.js'require(esm)support and sets atruthy __cjsUnwrapDefaultexport as a marker, that takes priority over both rules above and returns the default export. That's purely there so existing prebuilt bundles keep working.

## Errors are consistent, and use the right class

Regardless of whether resolution fails through a staticimport, a dynamicimport(), orrequire(), you get the same class of error with the same message shape:

```
await import('./nope.js');
// Error: Module not found: file:///bundle/nope.js

await import('https://');
// TypeError: Invalid module specifier: https://
```

"Module not found"is a plainError, since it's a failure to locate something rather than a problem with the value you passed in. A specifier that can't be parsed as a URL at all is aTypeError, matching Node.js' ownERR_INVALID_MODULE_SPECIFIER. A circular dependency that V8 can't unwind is also a plain Error, never aTypeError. This mostly matters if you're building something on top of dynamicimport(), like your own loader or a retry wrapper, since you can now branch on the error class or message reliably no matter which loading path triggered it.

## WebAssembly source phase imports

You can now import the compiled-but-not-instantiated form of a WebAssembly module directly, usingsource phase imports:

```
import source wasmModule from './add.wasm';

export default {
  async fetch() {
    const instance = await WebAssembly.instantiate(wasmModule, {});
    return new Response(String(instance.exports.add(1, 2)));
  },
};
```

or dynamically:

```
const wasmModule = await import.source('./add.wasm');
```

Either way you get aWebAssembly.Moduleback directly, instead of importing the module normally and pulling it off thedefaultexport. As source phase imports are a new feature of the language, right now this only works for WebAssembly; trying it on any other module type throws aSyntaxError, matching the behavior of Node.js and other runtimes.

## What's next

Try it out! Add the new_module_registry compatibility flag to your Worker:

```
{
  "compatibility_flags": ["new_module_registry"]
}
```

It doesn't have a default on date yet, so it won't turn on automatically for your Worker, old or new, no matter what compatibility date it's using. You will need to add the flag explicitly.

Weâd love your feedback.workerdis open source. If you run into behavior that looks like a regression rather than one of the changes described here, please file it against theworkerd repository.

## Related tags

Follow on Social Media

- Cloudflare

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[How we rebuilt Cloudflare Workersâ module registry for Node.js compatibility](https://blog.cloudflare.com/workers-module-registry-nodejs/)
> 
> 翻译时间：2026-09-10 07:13
