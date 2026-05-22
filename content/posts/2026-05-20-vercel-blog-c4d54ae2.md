---
title: Vercel AI网关插件：一键接入40+AI模型
title_original: Vercel AI Gateway plugin for WordPress - Vercel
date: '2026-05-20'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-ai-gateway-plugin-for-wordpress
author: ''
summary: Vercel推出AI网关WordPress插件，通过单一API密钥即可访问来自Anthropic、Google、OpenAI等40多家提供商的数百个AI模型。该插件基于WordPress
  7.0的AI客户端构建，支持多模态内容生成（文本、图像、视频）、自动故障转移、动态模型发现和统一计费。任何基于WordPress AI客户端的插件均可自动使用该连接器，无需单独集成或管理多个API密钥，大幅简化了WordPress站点的AI功能部署与管理。
categories:
- AI产品
tags:
- Vercel
- AI网关
- WordPress插件
- 多模态AI
- API集成
draft: false
translated_at: '2026-05-22T06:06:23.058544'
---

Vercel AI 网关插件通过单一 API 密钥，为任何 WordPress 站点提供来自 40 多家提供商的数百个模型。提供商包括 Anthropic、Google、OpenAI、xAI、DeepSeek、MiniMax、Moonshot AI 等。

该插件作为新版 WordPress AI 客户端的连接器实现，后者需要今天发布的 WordPress 7.0。

## 链接到标题 此功能支持的内容

- 任何 AI 驱动的插件均可自动运行。基于 WordPress AI 客户端构建的插件无需自己的提供商集成或 API 密钥即可使用该连接器。
- 一个密钥，多家提供商。在“设置 > 连接器”中管理单个 AI 网关密钥，而非为每家提供商分别管理凭据。
- 多模态内容生成。文本、结构化 JSON、图像生成与编辑以及视频，均通过同一提示词构建器完成。
- 自动故障转移。在提供商服务中断期间，AI 功能保持在线。
- 动态模型发现。无需插件更新即可使用新模型。
- 跨提供商的统一计费与可观测性，按提供商价格计费。

任何 AI 驱动的插件均可自动运行。基于 WordPress AI 客户端构建的插件无需自己的提供商集成或 API 密钥即可使用该连接器。

一个密钥，多家提供商。在“设置 > 连接器”中管理单个 AI 网关密钥，而非为每家提供商分别管理凭据。

多模态内容生成。文本、结构化 JSON、图像生成与编辑以及视频，均通过同一提示词构建器完成。

自动故障转移。在提供商服务中断期间，AI 功能保持在线。

动态模型发现。无需插件更新即可使用新模型。

跨提供商的统一计费与可观测性，按提供商价格计费。

## 链接到标题 开始使用

1. 在你的 WordPress 站点上安装 Vercel AI 网关插件
2. 在“设置 > 连接器”下添加你的 AI 网关 API 密钥

在你的 WordPress 站点上安装 Vercel AI 网关插件

在“设置 > 连接器”下添加你的 AI 网关 API 密钥

要从你自己的代码中直接调用 AI 网关：

```
1$excerpt = wp_ai_client_prompt( '为这篇文章写一个两句话的摘要：' . $post->post_content )2    ->using_provider( 'ai_gateway' )3    ->generate_text();
```

为 WordPress 博客文章编写两句话的摘要

更多详情，包括文本、结构化 JSON 输出、图像生成和视频的示例，请参阅插件文档。

---

> 本文由AI自动翻译，原文链接：[Vercel AI Gateway plugin for WordPress - Vercel](https://vercel.com/changelog/vercel-ai-gateway-plugin-for-wordpress)
> 
> 翻译时间：2026-05-22 06:06
