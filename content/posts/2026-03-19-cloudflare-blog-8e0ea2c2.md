---
title: Workers AI支持大模型，首发Kimi K2.5赋能智能体
title_original: 'Powering the agents: Workers AI now runs large models, starting with
  Kimi K2.5'
date: '2026-03-19'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/workers-ai-large-models/
author: ''
summary: Cloudflare宣布其Workers AI平台正式进入大模型领域，首发支持Moonshot AI的Kimi K2.5模型。该模型具备256k上下文窗口，支持多轮工具调用、视觉输入和结构化输出，专为智能体任务设计。文章指出，通过将此类前沿开源模型引入平台，开发者可以在统一的Cloudflare平台上运行完整的智能体生命周期。内部测试显示，Kimi
  K2.5在性能上可媲美大型专有模型，但成本大幅降低（例如在某个用例中成本降低了77%），有助于解决智能体规模化应用的成本障碍。
categories:
- AI基础设施
tags:
- Cloudflare
- Workers AI
- Kimi K2.5
- 大语言模型
- 智能体
draft: false
translated_at: '2026-03-20T04:50:31.801688'
---

# 赋能智能体：Workers AI 现已支持运行大模型，首发 Kimi K2.5

2026-03-19

- Michelle Chen
- Kevin Flansburg
- Ashish Datta
- Kevin Jain

![](/images/posts/e2403cf68e7f.png)

我们正致力于将 Cloudflare 打造成构建和部署 Agent（智能体）的最佳平台。但可靠的 Agent（智能体）不能仅靠提示词构建；它们需要一个稳健、协调的底层基础设施。

多年来，Cloudflare 一直在构建这些基础设施：用于状态持久化的 Durable Objects，用于长时间运行任务的 Workflows，以及用于安全执行的 Dynamic Workers 或 Sandbox 容器。像 Agents SDK 这样强大的抽象层，旨在帮助您在 Cloudflare 开发者平台之上构建 Agent（智能体）。

但这些基础设施仅提供了执行环境。Agent（智能体）仍然需要一个能够驱动它的模型。

从今天开始，Workers AI 正式进入大模型领域。我们现在在我们的 AI 推理平台上提供前沿的开源模型。我们首先在 Workers AI 上发布 **Moonshot AI 的 Kimi K2.5 模型**。Kimi K2.5 模型拥有完整的 256k 上下文窗口，并支持多轮工具调用、视觉输入和结构化输出，非常适合各种 Agent（智能体）任务。通过将前沿规模的大模型直接引入 Cloudflare 开发者平台，我们使得在单一、统一的平台上运行整个 Agent（智能体）生命周期成为可能。

Agent（智能体）的核心是驱动它的 AI 模型，该模型需要足够智能，具备高推理能力和大上下文窗口。Workers AI 现在可以运行这些模型。

## 性价比的最佳平衡点

过去几周，我们测试了将 Kimi K2.5 作为内部开发工具的引擎。在我们的 OpenCode 环境中，Cloudflare 工程师将 Kimi 作为处理 Agent（智能体）编码任务的日常工具。我们还将该模型集成到了我们的自动化代码审查流程中；您可以通过我们在 Cloudflare GitHub 仓库上的公共代码审查 Agent（智能体）Bonk 看到实际效果。在生产环境中，该模型已被证明是大型专有模型的快速、高效替代品，且质量毫不逊色。

提供 Kimi K2.5 服务最初是一项实验，但在评估了该模型的性能和成本效益后，它迅速变得至关重要。举一个说明性的例子：我们有一个对 Cloudflare 代码库进行安全审查的 Agent（智能体）。这个 Agent（智能体）每天处理超过 70 亿个 Token，使用 Kimi 后，它在一个代码库中就发现了超过 15 个已确认的问题。粗略计算一下，如果我们使用中端专有模型运行这个 Agent（智能体），仅针对这一个代码库的单一用例，我们每年将花费 240 万美元。而使用 Kimi K2.5 运行这个 Agent（智能体）的成本只是其中的一小部分：仅仅通过切换到 Workers AI，我们就将成本降低了 77%。

随着 AI 应用的普及，我们不仅看到了工程团队运作方式的根本性转变，也看到了个人运作方式的转变。人们拥有像 OpenClaw 这样 24/7 运行的个人 Agent（智能体）正变得越来越普遍。推理量正在急剧飙升。

个人和编码 Agent（智能体）的这种新增长意味着成本不再是次要问题；它已成为规模化扩展的主要障碍。当每位员工都有多个 Agent（智能体）每小时处理数十万个 Token 时，使用专有模型的成本计算就不再可行。企业将寻求转向提供前沿水平推理能力但无需专有价格标签的开源模型。Workers AI 旨在促进这一转变，提供从个人 Agent（智能体）的无服务器端点到为整个组织的自主 Agent（智能体）提供支持的专用实例等一切服务。

## 大模型推理技术栈

Workers AI 自两年前推出以来，就一直提供包括 LLM（大语言模型）在内的模型服务，但我们历史上优先考虑的是较小的模型。部分原因是在一段时间内，开源的 LLM（大语言模型）远远落后于前沿模型实验室的模型。随着 Kimi K2.5 等模型的出现，这种情况发生了变化，但要服务这种超大型 LLM（大语言模型），我们必须对我们的推理技术栈进行更改。我们想与您分享一些幕后工作，以支持像 Kimi 这样的模型。

我们一直在为 Kimi K2.5 开发定制内核，以优化我们服务模型的方式，该内核建立在我们专有的 Infire 推理引擎之上。定制内核提高了模型的性能和 GPU 利用率，释放了如果只是开箱即用地运行模型就无法获得的性能增益。服务大模型还可以利用多种技术和硬件配置。开发人员通常结合使用数据、张量和专家并行化技术来优化模型性能。像解耦预填充这样的策略也很重要，即将预填充和生成阶段分离到不同的机器上，以获得更好的吞吐量或更高的 GPU 利用率。实施这些技术并将其整合到推理技术栈中，需要大量的专业经验才能做好。

Workers AI 已经在服务技术方面进行了实验，以在 Kimi K2.5 上实现出色的吞吐量。当您自行托管开源模型时，很多这些优化并不是开箱即用的。使用 Workers AI 这样的平台的好处是，您不需要成为机器学习工程师、DevOps 专家或站点可靠性工程师来进行托管所需的优化：我们已经完成了困难的部分，您只需要调用一个 API。

## 超越模型 —— 针对 Agent（智能体）工作负载的平台改进

配合此次发布，我们还改进了我们的平台，并发布了几个新功能，以帮助您构建更好的 Agent（智能体）。

### 前缀缓存与缓存 Token 指标展示

当您使用 Agent（智能体）时，很可能会发送大量输入 Token 作为上下文的一部分：这可能是详细的系统提示词、工具定义、MCP 服务器工具或整个代码库。输入可以大到模型上下文窗口的极限，因此理论上，您可以发送包含近 256k 输入 Token 的请求。这需要处理大量的 Token。

当 LLM（大语言模型）处理请求时，请求被分解为两个阶段：预填充阶段处理输入 Token，输出阶段生成输出 Token。这些阶段通常是顺序进行的，输入 Token 必须完全处理后才能生成输出 Token。这意味着有时在模型进行预填充时，GPU 并未得到充分利用。

在多轮对话中，当您发送新的提示词时，客户端也会将之前的所有提示词、工具和会话上下文发送给模型。连续请求之间的差异通常只是几行新的输入；所有其他上下文已经在之前的请求中经过了预填充阶段。这就是前缀缓存发挥作用的地方。我们无需对整个请求进行预填充，而是可以缓存来自先前请求的输入张量，只对新输入的 Token 进行预填充。这节省了预填充阶段的大量时间和计算，意味着更快的首次 Token 时间（TTFT）和更高的每秒 Token 吞吐量（TPS），因为您不会被预填充阶段阻塞。

Workers AI 一直都有前缀缓存功能，但现在我们将缓存 Token 作为使用指标展示出来，并且与输入 Token 相比，对缓存 Token 提供折扣。（定价可以在模型页面上找到。）我们还提供了新的技术供您利用，以获得更高的前缀缓存命中率，从而降低成本。

### 用于提高缓存命中率的新会话亲和性头部

为了路由到相同的模型实例并利用前缀缓存，我们使用了一个新的 `x-session-affinity` 头部。当您发送此头部时，您将提高缓存命中率，从而获得更多的缓存 Token，进而实现更快的 TTFT、TPS 和更低的推理成本。

您可以通过如下方式传递新的头部信息，每个会话或每个Agent（智能体）使用唯一的字符串。像OpenCode这样的客户端已默认自动实现了此功能。我们的Agents SDK入门模板也已为您配置好了相关设置。

```shell
curl -X POST \
"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/moonshotai/kimi-k2.5" \
  -H "Authorization: Bearer {API_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "x-session-affinity: ses_12345678" \
  -d '{
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "What is prefix caching and why does it matter?"
      }
    ],
    "max_tokens": 2400,
    "stream": true
  }'

```

### 重新设计的异步API

无服务器推理确实非常困难。采用按Token付费的业务模式后，单次请求的成本更低，因为您无需为整个GPU付费来处理请求。但这需要权衡：您必须应对他人的流量和容量限制，并且无法严格保证您的请求会被处理。这并非Workers AI独有的问题——鉴于频繁出现提供商过载和服务中断的新闻报道，这显然是所有无服务器模型提供商的普遍情况。尽管我们始终致力于处理您的请求，并内置了自动扩缩容和重新平衡机制，但硬件等硬性限制使得这成为一个挑战。

对于可能超过同步速率限制的大量请求，您可以提交批量推理任务以异步方式完成。我们正在推出全新的异步API，这意味着对于异步使用场景，您将不会遇到“容量不足”的错误，并且推理将在某个时间点可靠地执行。我们的异步API更像弹性处理而非批量API，只要我们的模型实例有剩余容量，就会处理异步队列中的请求。通过内部测试，我们的异步请求通常在5分钟内执行，但这将取决于实时流量的情况。随着我们将Kimi向公众开放，我们将相应调整扩缩容策略，但异步API是确保您在持久工作流中不会遇到容量错误的最佳方式。这对于非实时用例（如代码扫描Agent或研究Agent）来说非常理想。

Workers AI之前已有异步API，但我们最近彻底重构了底层系统。我们现在采用基于拉取的系统，而非历史上基于推送的系统，这使我们能够在有容量时立即拉取队列中的请求。我们还增加了更好的控制来调节异步请求的吞吐量，实时监控GPU利用率，并在利用率较低时拉取异步请求，从而确保关键同步请求获得优先级，同时仍能高效处理异步请求。

要使用异步API，您可以按如下方式发送请求。我们还提供了一种设置事件通知的方法，以便您可以在推理完成时获知，而无需轮询请求状态。

```javascript
// (1.) 将请求推入队列
// 传递 queueRequest: true
let res = await env.AI.run("@cf/moonshotai/kimi-k2.5", {
  "requests": [{
    "messages": [{
      "role": "user",
      "content": "Tell me a joke"
    }]
  }, {
    "messages": [{
      "role": "user",
      "content": "Explain the Pythagoras theorem"
    }]
  }, ...{<add more requests in a batch>} ];
}, {
  queueRequest: true,
});


// (2.) 获取请求ID
let request_id;
if(res && res.request_id){
  request_id = res.request_id;
}
// (3.) 轮询状态
let res = await env.AI.run("@cf/moonshotai/kimi-k2.5", {
  request_id: request_id
});

if(res && res.status === "queued" || res.status === "running") {
 // 通过再次轮询重试
 ...
}
else 
 return Response.json(res); // 这将包含最终完成的响应

```

## 立即试用

立即开始在Workers AI上使用Kimi K2.5。您可以阅读我们的开发者文档，了解模型信息和定价，以及如何利用通过会话亲和性头部实现的提示词缓存和异步API。Agents SDK入门模板现在也默认使用Kimi K2.5作为其模型。您还可以通过Opencode连接到Workers AI上的Kimi K2.5。如需实时演示，请在我们的playground中尝试。

如果您对无服务器推理、机器学习优化和GPU基础设施这一系列问题感兴趣——我们正在招聘！

---

> 本文由AI自动翻译，原文链接：[Powering the agents: Workers AI now runs large models, starting with Kimi K2.5](https://blog.cloudflare.com/workers-ai-large-models/)
> 
> 翻译时间：2026-03-20 04:50
