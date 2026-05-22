---
title: Chat SDK新增按钮与模态框回调URL功能
title_original: Chat SDK now supports callback URLs on buttons and modals - Vercel
date: '2026-05-20'
source: Vercel Blog
source_url: https://vercel.com/changelog/chat-sdk-now-supports-callback-urls-on-buttons-and-modals
author: ''
summary: Vercel的Chat SDK现在支持在卡片按钮和模态框上使用callbackUrl属性，允许开发者暂停工作流运行，并在用户点击按钮或提交表单时恢复。通过创建workflow
  webhook并将其URL传递给按钮或模态框，事件负载会被发送到指定端点。该功能在Slack和Teams等平台上可用，为构建审批卡片、表单交互等场景提供了更灵活的流程控制能力。
categories:
- AI基础设施
tags:
- Chat SDK
- 回调URL
- 工作流
- Vercel
- Slack集成
draft: false
translated_at: '2026-05-22T06:06:17.495757'
---

你现在可以在 Chat SDK 卡片上暂停一个 Workflow 运行，并在有人点击按钮时恢复它。同样的流程也适用于表单提交。按钮和模态框接受一个新的 `callbackUrl` 属性，事件负载会被发送到该端点。

![请求你授权发送状态报告的 Slack 审批卡片示例](/images/posts/c5ff2079dd33.jpg)

![请求你授权发送状态报告的 Slack 审批卡片示例](/images/posts/4619d69d6dc4.jpg)

要构建这样的卡片，创建一个 workflow webhook，并将其 URL 传递给你 `<Card>` 组件中每个按钮的 `callbackUrl` 属性：

```
import { createWebhook } from "workflow";import { Card, CardText, Actions, Button } from "chat";
export async function statusReport(  thread,  content: { title: string; message: string },) {
  "use workflow";
  using hook = createWebhook<{ action: "approve" | "approve-and-send" | "deny" }>();
  await thread.post(    <Card title="状态报告沟通">      <CardText>标题：{content.title}</CardText>      <CardText>消息：{content.message}</CardText>      <Actions>        <Button callbackUrl={hook.url} id="approve" style="primary">          批准        </Button>        <Button callbackUrl={hook.url} id="approve-and-send" style="primary">          批准并发送        </Button>        <Button callbackUrl={hook.url} id="deny" style="danger">          取消        </Button>      </Actions>    </Card>  );
  const { action } = await hook;  if (action === "approve" || action === "approve-and-send") {    await sendReport(content);  }
}
```

创建一个审批卡片来批准或拒绝部署

对于 `<Modal>` 组件，表单数据包含在负载中。`callbackUrl` 在大多数拥有官方适配器的平台上适用于按钮，在 Slack 和 Teams 上适用于模态框。

阅读文档或操作指南开始构建。

Chat SDK 完整指南

了解 Chat SDK 的端到端工作原理：从核心概念到构建你的第一个机器人，再到将其部署到 Slack、Teams 等平台。

阅读指南

---

> 本文由AI自动翻译，原文链接：[Chat SDK now supports callback URLs on buttons and modals - Vercel](https://vercel.com/changelog/chat-sdk-now-supports-callback-urls-on-buttons-and-modals)
> 
> 翻译时间：2026-05-22 06:06
