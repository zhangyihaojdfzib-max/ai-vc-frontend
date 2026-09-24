---
title: 'Introducing Worker Previews: isolated preview environments for every change
  your agent makes'
title_original: 'Introducing Worker Previews: isolated preview environments for every
  change your agent makes'
date: '2026-09-22'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/worker-previews/
author: ''
summary: "[翻译失败，原文如下]\n\nNothing is worse than testing out a change that works in\
  \ staging, only to see it behave differently in production. Thatâ\x80\x99s why we\
  \ wanted..."
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-24T07:29:09.490547'
---

[翻译失败，原文如下]

Nothing is worse than testing out a change that works in staging, only to see it behave differently in production. Thatâs why we wanted to give you an environment thatâs as close to production as possible â so you can battle-test your changes and make sure they behave exactly as you expect them to.

Agents are helping us push more lines of code than ever before, and larger changes mean more ground needs to be tested ahead of release. Ideally, that testing is done in a waythat doesnât slow agents down, but gives them the tools to take on more of the development lifecycle.

Thatâs why today weâre launchingWorker Previews.Each Git branch gets a production-like place to run, with its own code, configuration, URL, observability, and state.

So now, for every change in your codebase, you can:

- Deploy an isolated Previewwithnpx wrangler preview, using its own variables, secrets, and bindings, separate from production configuration and traffic.
- Share a stable Preview URLfor the branch so that every push updates the same running Preview where you can send requests, click through the UI, and test runtime responses.
- Isolate Durable Objects and Containersper branch, keeping state changes, sessions, memory, migrations, and concurrent tests scoped to that Preview.
- Inspect logs, errors, metrics, and tracesfor that Preview to confirm the change works, catch failures, push a fix, and verify it before production sees it.
- Start from the Preview configuration you set, soeach Preview begins with a copy of the variables, secrets, bindings, and settings you define â just like a code branch starts frommain. We call this thebase configuration.
- Override a Previewâs configuration when needed, like pointing it at its own database or test API key for migrations â without changing production, the base, or other Previewsâ configuration.
- Serve Preview URLs on a custom domainso that auth providers, cookies, cross-origin resource sharing (CORS), and OAuth redirects work the same way they will in production.

The result is a pre-production feedback loop for every branch. Push your change to a branch, test behavior, inspect performance â before you merge to production.

This enables an Agent Development Lifecycle (ADLC) where each change is atomic, independently deployable, observable, and revisable. And it gives agents and humans the evidence they need toself-improve: catch what failed, push a fix, and verify the next deployment before it hits production.

## Every Git branch gets its own environment

When you start work on a new feature, the first thing you do is branch off ofmain. You get your own copy of the code and make your changes without affecting anything in production.

Worker Previews extend that same model beyond code. Each branch gets its own isolated environment and URL. You can run hundreds of Previews at the same time â each operating independently without affecting other Previews or production.

![ch1.png](/images/posts/f0fd94488f75.jpg)

Production and each Preview have their own configuration â served on their own URL.

When you runnpx wrangler preview, the branch gets its own copy of your Previews configuration that you have defined, running on its own URL â all under the same Worker.

In the dashboard, this works like switching branches. Click the breadcrumb next to your Worker's name (it defaults to Production) to see all your Previews:

The dashboard brings every environment into one view. Production sits alongside as many Previews as you need, so contributors can work on separate changes without fighting over a shared staging site. UnlikeWrangler environments, where each environment requires deploying and managing a separate Worker, Previews keep that isolation in one dashboard view.

Each Preview runs as a real version of your Worker. Some changes can only be validated at runtime: an API endpoint has to handle a real request and return the right response. More subjective changes, like a UI update, a new onboarding step, or a different error state, need to be experienced in context before they reach production.

## Every Preview has its own isolated and persistent state, with Durable Objects and ContainersÂ

For isolation to extend across your application, stateful resources need special treatment. The reason for that is that Durable Objects run on asingleton model. One instance is responsible for a given object ID, and that instance owns its storage.

If a Preview shared the same DO namespace as production, you wouldn't just be reading stale data â you could modify the same instance serving live traffic in real time (scary!).

That is why every time you runnpx wrangler preview, Cloudflare automatically creates a new Durable Object namespace and Container application for that Preview â so that a failed migration or a bad schema change stays contained to that branch and that branch only.

All you need to do is export the class, add its migration, and access it throughctx.exports:

```
export class Counter extends DurableObject {}

export default {
  async fetch(request, env, ctx) {
    const id = ctx.exports.Counter.idFromName("demo");
    const counter = ctx.exports.Counter.get(id);
    return counter.fetch(request);
  },
};
```

In production,ctx.exports.Counterresolves to the production namespace, while in a Preview, it resolves to that Previewâs namespace.

You now have an entire playground to experiment with. Take Sandboxes, for example, where milliseconds of improvement to startup time can make or break the experience. If you have been trying to improve cold-start performance, you can run different configurations across branches at the same time, compare their cold and warm performance side by side, and find the best setup faster.

## Test, observe, and revise each Preview (or have your agent do it)

Now that each branch runs at its own URL in an isolated environment with its own state, you can enter the feedback loop and start battle-testing every change before it reaches production.

You can send traffic to the Preview URL however you normally would â from your terminal,probe from CI, an agent, or by clicking through it yourself. Once that traffic starts flowing, every Workers Observability tool youâre already used to is available, scoped to each individual Preview.

As each request hits the Preview, Workers Observability traces its full lifecycle in a waterfall, including fetch calls, binding operations, and handler invocations. So when something fails, you can follow exactly what happened without sorting through production traffic or signals from other changes.

Observability for Previews looks just like you're already used to for production Workers. Select your Preview from the breadcrumb and open the Observability tab to see its events, errors, and traces:

To give your agents even more control, you can have them open the Preview URL in a headless browser, click through a login flow step by step, andcapture a screenshotor record the entire session asreplayable DOM eventsâ with Browser Run.Â

Below is an example where an agent opens the Preview, captures what was rendered, and connects a failed request to Workers Observability events from the same run.

A reviewer can watch the session in real time withLive Viewor step in withHuman in the Loopwhen the automation needs judgment.

If something fails, you see it from both angles: what rendered and what happened at runtime.Â

That gives the agent enough evidence to keep the pre-production loop running autonomously: deploy, open the URL withPlaywright MCP, click through, query the traces through theWorkers Observability MCP server, patch, redeploy, and verify. Every iteration stays scoped to the branch.

## Configure a base configuration for Previews once, then override as needed

Just like you wouldn't reconfigure your code from scratch every time you branch, you shouldn't have to reconfigure your environment either.Â

[翻译失败，原文如下]

You setbase configurationfor Previews once, in apreviewsblock in yourWrangler configuration file.

```
{
  "vars": {
    "ENVIRONMENT": "production"
  },
  "r2_buckets": [
    {
      "binding": "UPLOADS",
      "bucket_name": "prod-uploads"
    }
  ],
  "previews": {
    "vars": {
      "ENVIRONMENT": "preview"
    },
    "r2_buckets": [
      {
        "binding": "UPLOADS",
        "bucket_name": "r2-staging"
      }
    ]
  }
}
```

In the dashboard under Worker â Settings, you see this inlined asProductionandPreviews Base. Once the base is set, runnpx wrangler previewfrom any branch to create a Preview. If your Worker is Git-connected throughWorkers Builds, it happens automatically on push.

You can override any setting for only one Preview â without affecting production, the base, or other Previews.

## Preview URLs on your own custom domain, protected with Cloudflare Access

To bring the whole setup even closer to production, your preview URLs can be served from your owncustom domain. If your app runs onexample.com, a Preview for a login branch could run atfeature-login.previews.example.com.

If you want to keep those URLs private, you canprotect your Previews with Cloudflare Accessand require visitors to sign in first.

## Testing the whole system before production

Weâve already been dogfooding Worker Previews inside Cloudflare, most notably to build and testCloudflareOS, our open-source platform for safely connecting agents to company systems.

CloudflareOS lets agents work with services such as Google, GitHub, and Slack throughGatekeepers, which control what those agents can access and change. That makes Gatekeeper changes especially sensitive, because a bug could expose data or permit an action that should never have been allowed.

Some of these bugs only appear when OAuth callbacks, permissions, approval flows, and application state are running together. Because testing each component separately cannot show us how the complete system will behave, we deploy an isolated Preview of CloudflareOS and its Gatekeepers for every change under review. We then run the full workflow, fix what fails, and test it again before merging.

Weâre seeing customers use Previews for the same basic reason: some problems only show themselves when the change is actually running.

"At Supermemory, we use Cloudflare heavily, and Worker Previews are exactly the kind of developer experience improvement we wanted to see. For HTTP flows, we can preview Worker changes before they reach production, including routes backed by Durable Objects, and catch issues earlier without slowing down shipping." âDhravya Shah,Founder, Supermemory

"Previews is amazing for Inspect [Rampâs coding agent]. I used it to review and test an Inspect PR on my phone that is making reviewing and testing PRs with Inspect on phones responsiveâ¦with Inspect." âDylan Garcia,Senior Staff Engineer, Ramp

## Whatâs next?

You might be thinking: Didn't Workers already have preview URLs? Itâs true, we did. We're now calling thoseVersion URLsbecause they point to specific uploaded Worker versions. Unlike Worker Previews, they don't create an isolated environment for each branch and could only point to production resources. To learn more and compare the different workflows, check outour docs.

Worker Previews is a big improvement from what we offered before, but there's still more to come. Here's what we're working on next:

- Preview multi-Worker applications.Today, aservice binding from a Previewstill calls the bound Worker's production deployment. We're working toward keeping the entire request path inside matching Previews.
- Run Queue consumers and Workflows inside each Preview.Today, Previews can send messages to Queues but cannot consume them, while isolating Workflow executions requires separate configuration. We want the entire asynchronous flow scoped to the branch automatically.
- Support long-lived Previews for staging and QA.We've heard from teams in the private beta that not every branch is short-lived â some maintain staging, QA, or per-developer environments that persist across sprints. We want to support these end-to-end, and we want to hear how you use them, so we can get it right.

Worker Previews are available now. Get started with thedocs, and if you have a feature request or run into an issue, open an issue onGitHubor join the Cloudflare Developers community onDiscord.

Acknowledgements: This project was made possible by the design and implementation efforts of Greg Brimble, Patrick OâDonnell, Matt Price, Korinne Alpers, Max Peterson, Cina Saffary, Josh Wheeler, Thomas Ankcorn, Matt Rothenberg, and Brandon Strittmatter, with leadership from Brendan Irvine-Broque and Dan Carter.

## Related tags

Follow on Social Media

- Cloudflare
- Yomna Shousha

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Introducing Worker Previews: isolated preview environments for every change your agent makes](https://blog.cloudflare.com/worker-previews/)
> 
> 翻译时间：2026-09-24 07:29
