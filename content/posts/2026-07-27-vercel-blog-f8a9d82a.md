---
title: Vercel为eve新增Slack事件钩子与会话控制
title_original: eve adds new Slack event hooks and session controls - Vercel
date: '2026-07-27'
source: Vercel Blog
source_url: https://vercel.com/changelog/eve-adds-new-slack-event-hooks-and-session-controls
author: ''
summary: Vercel为其AI代理平台eve推出三项Slack集成更新：新增onMessage钩子支持线程内无需重复提及即可持续对话，并引入ctx.isBotMentioned()和ctx.isSubscribed()辅助函数；新增ctx.cancel()和ctx.reset()会话控制功能，允许取消正在进行的回复或重置对话；新增onEvent钩子，可处理Slack
  Events API中的任意事件（如reaction_added、team_join），并通过ctx.receive()将事件分发至多个目标频道。
categories:
- AI产品
tags:
- Vercel
- eve
- Slack集成
- AI代理
- 事件钩子
draft: false
translated_at: '2026-07-30T05:17:01.527280'
---

Slack 上的 eveagents 现在可以在线程中持续回复而无需重复提及，取消正在进行的回复或完全重置对话，并对你的 Slack 应用订阅的任何事件做出反应。

## 复制链接到标题无需重复提及即可继续对话

提及不再需要承载整个对话。一旦线程拥有活跃会话，你的 Agent 可以自行回复。

新的 `onMessage` 钩子接收传入的 Slack 消息，两个辅助函数决定哪些消息需要处理：`ctx.isBotMentioned()` 检测显式提及，`ctx.isSubscribed()` 检查消息是否属于拥有活跃 eve 会话的线程：

```
1export default slackChannel({2  credentials: connectSlackCredentials("slack/my-agent"),3  async onMessage(ctx, message) {4
5    if (message.author?.isBot) return null;6
7    const isDirectMessage = message.raw.channel_type === "im";8    return isDirectMessage || ctx.isBotMentioned() || (await ctx.isSubscribed())9      ? { auth: null }10      : null;11  },12});
```

分发私信、显式提及以及活跃会话线程中的后续消息。

当路由取决于谁加入了线程时，新的 `ctx.thread.listParticipants()` 辅助函数会按首次出现顺序返回唯一的人类 Slack 用户 ID。公共频道消息需要 `message.channels` 触发事件类型和 `channels:history` 机器人作用域；私有频道还需要 `message.groups` 和 `groups:history`。

## 复制链接到标题取消一次回复或重置对话

消息钩子还接收两个与线程绑定的会话辅助函数。

`ctx.cancel()` 在保留会话的同时停止当前回复：在返回 `{ auth }` 之前调用它，以将新消息排队作为替换输入，这样在回复中途进行修正时，可以丢弃已失效的工作，Agent 会响应最新消息。

当需要重新开始对话时，`ctx.reset()` 会彻底终止拥有该线程的会话。下一条送达的消息将以全新的历史记录、状态和沙箱开始一个新会话。在你的 `onMessage` 分发逻辑中，重置命令只需三行代码：

```
1export default slackChannel({2
3  credentials: connectSlackCredentials("slack/my-agent"),4  async onMessage(ctx, message) {5
6    if (message.text.trim() !== "!new") return null;7    await ctx.reset({ reason: "Slack user requested !new" });8    await ctx.thread.post("Started a fresh conversation.");9    return null;10
11  },12});
```

终止会话，让下一条消息重新开始。

## 复制链接到标题处理任何 Events API 回调

你的 Agent 现在可以对你 Slack 应用订阅的任何事件做出反应。

新的 `onEvent` 钩子接收原始事件，例如 `reaction_added`、`team_join` 和 `channel_created`。在钩子内部，调用 `ctx.receive()` 来启动一次 Agent 回复，或多次调用以将单个事件分发到多个目标。例如，`team_join` 事件可以在你的每个欢迎频道中触发入职流程。

```
1const onboardingChannels = ["C0123ABC", "C0456DEF"];2
3export default slackChannel({4  credentials: connectSlackCredentials("slack/my-agent"),5  async onEvent({ receive }, event) {6
7    if (event.type !== "team_join") return;8
9    await Promise.all(10      onboardingChannels.map((channelId) =>11        receive({12          message: `A user joined the Slack workspace. Onboard them from this event:\n${JSON.stringify(event)}`,13          target: { channelId },14          auth: null,15        }),16      ),17    );18  },19});
```

将单个 team_join 事件分发到多个频道中的入职回复。

阅读 Slack 频道文档开始使用，或通过 `eve channels add slack` 将频道添加到你的 eve agent。

从模板启动 eve agent

选择一个模板，几分钟内完成部署，并从首次运行起在 Vercel 仪表板中调试每个 Agent 会话。

构建你的 Agent

## 贡献者

Ben Sabic

---

> 本文由AI自动翻译，原文链接：[eve adds new Slack event hooks and session controls - Vercel](https://vercel.com/changelog/eve-adds-new-slack-event-hooks-and-session-controls)
> 
> 翻译时间：2026-07-30 05:17
