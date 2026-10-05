---
title: 'Protected Quick Tunnels: simple accountless authentication for your next dev
  project'
title_original: 'Protected Quick Tunnels: simple accountless authentication for your
  next dev project'
date: '2026-10-02'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/protected-quick-tunnels/
author: ''
summary: '[翻译失败，原文如下]


  We launchedQuick TunnelsÂ in 2021 to give developers an easy way to share their
  latest service, application, or project running in their ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-05T08:02:29.230180'
---

[翻译失败，原文如下]

We launchedQuick TunnelsÂ in 2021 to give developers an easy way to share their latest service, application, or project running in their local development environment. A lot has changed since then, but the core use case remains the same.

Your coding agent has just finished the feature. The dev server is up onlocalhost:5173, and before you ask, the agent offers to let you try it on your phone. It runs one command and hands you a link:

```
cloudflared tunnel --url http://localhost:5173
```

That command starts aQuick Tunnel.cloudflared, Cloudflare's lightweight connector, publishes your local service at a randomtrycloudflare.comÂ URL. No account, no domain, no cost. Agents now use Quick Tunnels for the same reason people do: they are the shortest path from a local port to a URL.

The catch has always been the same. Anyone with the link can open it.

Starting withcloudflaredÂ 2026.9.3, you can add--allowed-mailÂ to the command, and your Quick Tunnel only lets in the email addresses and domains you choose. Visitors prove they own one of those addresses with a one-time PIN fromCloudflare Access.Â Nobody, on either side, needs a Cloudflare account.

## Agents made Quick Tunnels more popular than ever

Agents that write code need somewhere to show you the result. Agents that live on a Mac mini at home need to be reachable from your phone. Model Context Protocol servers on a laptop need a public endpoint before a hosted assistant can call them. Each of these needs a URL, and a Quick Tunnel produces one from a single command an agent can run by itself. There is no signup form for it to get stuck on. Add--output jsonÂ and every log line becomes a JSON object, so the agent can pick out the URL without scraping text.

Since agents took off, Cloudflare Tunnel and Quick Tunnels adoption has grown exponentially. On September 18, 2026, a link to the Quick Tunnels page climbed to the top ofHacker NewsÂ and gathered more than 800 points and 300 comments. The thread reads like a catalog of agent workflows. One person's AI had found Quick Tunnels on its own to publish a site it had just built. Another called them "insanely helpful when doing agentic work on the go."

And onecommenterÂ asked this post answers:"how long until someone's agent sets up a tunnel for the world to see one's most sensitive, private and embarrassing information or insecure work-in-progress app?"

## Control who can access your service

Pass an email address to--allowed-mail:

```
cloudflared tunnel --url http://localhost:8080 \
  --allowed-mail alice@example.com
```

Alice opens the URL, enters her email address, types in the code sent to her inbox, and reaches your app. Anyone else is stopped before a single request reaches your machine. You still don't create a DNS record, write a configuration file, or open a dashboard.

To let in more people, repeat the flag or allow an entire domain:

```
cloudflared tunnel --url http://localhost:8080 \
  --allowed-mail alice@example.com \
  --allowed-mail bob@example.com \
  --allowed-mail '*@example.com'
```

If you leave out--allowed-mail, nothing changes. Public Quick Tunnels behave exactly as they always have.

To change who can get in, stopcloudflaredÂ and start a new tunnel. Access ends for everyone the moment the process exits.

For a stable hostname or richer rules, such as identity provider groups, useCloudflare TunnelÂ with Cloudflare Access. To reach an agent at home from your own devices without any public URL and establish bidirectional connectivity, useCloudflare Mesh.

### Make it your agent's default

Because protection is a single flag, agents can use it as easily as people can. Add one line to the instructions file your coding agent reads, such asAGENTS.md:

```
When you start a Quick Tunnel, always add --allowed-mail me@example.com.
```

From then on, the previews your agent shares should open only for you. Agents don't always follow instructions, so check what it ran:cloudflaredÂ prints whether a tunnel uses email authentication and how many rules it holds, without printing the addresses.

### Start a protected tunnel from Wrangler

If you build on Workers, you can start the same kind of tunnel from the latest version ofwrangler:

```
npx wrangler tunnel quick-start http://localhost:8080 \
  --allowed-mail alice@example.com
```

Wrangler supports repeated flags, comma-separated values, and wildcard domains, and it removes--allowed-mailÂ values from its debug logs.

## Cloudflare verifies the email. Your machine decides who gets in.

![Four-step flow. A visitor opens your link, Cloudflare Access verifies their email with a one-time PIN, cloudflared on your machine checks it against your allowed emails, and only invited visitors reach your app.](/images/posts/d5dd4039ac00.jpg)

When someone opens a protected URL, they land on the Cloudflare Access sign-in page. They enter their email address, then the one-time PIN sent to that mailbox. Email sign-in is built for people using a browser.

That step answers one question only: does this person control this email address? It doesn't decide whether they're welcome.cloudflaredÂ makes that decision on your machine by comparing the verified address with the rules you typed.

## Where does a policy live when there is no account?

Separating those two questions is the core of the design. Authentication proves who a visitor is. Authorization decides whether that visitor gets in. Every Cloudflare product that enforces access rules keeps the authorization half in the same place: your Cloudflare account. A Quick Tunnel doesn't have one. So the hard part was never sending someone a code. It was deciding where the guest list should live.

We started with four requirements. The design had to:

- Keep Quick Tunnels accountless, because a signup step would defeat the point of a one-command tunnel.
- Leave the request path for public Quick Tunnels untouched.
- Avoid a central policy lookup on every request after a visitor signs in.
- Protect the privacy of the email addresses developers type into their terminals.

Our first idea was to put a Cloudflare Access application in front of every Quick Tunnel hostname. Access already checks visitors before traffic reachescloudflared, so reusing it looked like the shortest path. But hundreds of thousands of Quick Tunnels can be running at once, many for only a few minutes, and each would need its own application and policy. With no account to own them, we would have had to invent a new namespace and route applications dynamically, just to store a list that lives for an afternoon.

Our second idea was to build the whole flow.cloudflaredÂ would hold the rules, and a Tunnel service would send and check the codes. The authorization half of this idea was good: each connector checks its own list, which scales naturally and keeps the rules on the developer's machine. The authentication half was not. Sending a code is the easy part of email login. The hard parts are getting email delivered, stopping abuse, building secure challenges, managing sessions, and serving a sign-in page that is accessible and translated, then operating all of it safely for years. Cloudflare Access has already solved those problems.

So we kept the best half of each idea. Access verifies that the visitor controls the email address. A small authentication broker running onCloudflare WorkersÂ turns that verified identity into a short-lived, signed handoff. The broker is stateless by design. It stores no tunnel policies, no visitor sessions, and no identity records, and it never sees a tunnel's guest list.cloudflaredÂ checks the handoff and makes the authorization decision itself, in memory, against the rules you typed.

The result is the property we cared about most: your guest list never leaves your machine. Cloudflare learns that a tunnel requires email authentication. It doesn't learn who you invited.

## Following a request through a protected Quick Tunnel

[翻译失败，原文如下]

A protected tunnel is created the same accountless way as a public one. The only extra thingcloudflaredÂ sends is the authentication mode, never your rules. If the service doesn't confirm that mode,cloudflaredÂ refuses to start rather than hand you a public URL by mistake.

The first time a visitor opens the URL:

1. cloudflaredÂ sees a request with no session. It redirects the browser tologin.trycloudflare.comÂ with a random, single-use state tied to that browser and valid for 10 minutes.
2. Cloudflare Access sends a one-time PIN to the visitor's email address and verifies it.
3. The broker checks the Access identity and returns a short-lived, signed assertion bound to the tunnel hostname and to that state. The browser delivers it in a form POST, so it never lands in a URL, browser history, or logs.
4. cloudflaredÂ verifies the assertion, uses up the state, and checks the email against your rules. On a match, it creates a local session and sends the visitor to the page they asked for. Otherwise, the visitor gets a generic response that reveals nothing about the list.
5. Later requests use that session for up to four hours (less if the visitor's Access sign-in expires sooner), or until you stopcloudflared. There is no central lookup and no policy service.

The session cookie holds a random value and an expiry time, and nothing about who the visitor is.cloudflaredÂ strips authentication credentials before forwarding requests, so your app never sees them and never has to implement a login flow. If any check fails, the request never reaches your local service. A protected tunnel never falls back to public mode.

## Built by interns

Protected Quick Tunnels were shipped by two interns: Hugo Vicente on product and Alessandro Frigerio on engineering. They took it from the product requirements to the authentication broker to thecloudflaredÂ release. That's howinternshipsÂ work at Cloudflare: interns own real problems and deliver solutions to production.

## Try it on your next demo

Email protection for Quick Tunnels is free, like Quick Tunnels themselves.Install or updatecloudflared, start your local server, and add the--allowed-mailÂ flag:

```
cloudflared tunnel --url http://localhost:8080 --allowed-mail you@example.com
```

Setup details, matching rules, and limits are in theQuick Tunnels documentation.

The next time you or your agent shares what you're building, the link will only open for the people you chose.

## Related tags

Follow on Social Media

- Cloudflare
- Nikita Cano
- Hugo Vicente
- Alessandro Frigerio

## Subscribe to receive notifications of new posts

Weâll never share your email address.

Thanks for subscribing! Check your inbox to confirm.

---

> 本文由AI自动翻译，原文链接：[Protected Quick Tunnels: simple accountless authentication for your next dev project](https://blog.cloudflare.com/protected-quick-tunnels/)
> 
> 翻译时间：2026-10-05 08:02
