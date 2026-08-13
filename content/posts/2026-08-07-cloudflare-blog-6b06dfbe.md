---
title: Cloudflare统一AI控制平面：融合Workers AI与AI Gateway
title_original: Unifying Workers AI and AI Gateway into a single AI control plane
date: '2026-08-07'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/workers-ai-gateway-unification/
author: ''
summary: Cloudflare宣布将Workers AI和AI Gateway融合为统一控制平面，旨在通过单一入口连接任何模型提供商，同时提供可观测性、日志记录、安全性和成本管理。新方案简化了API和绑定，所有Workers
  AI用户自动获得默认网关的可观测性，无需额外配置。此举标志着模型路由和AI基础设施管理的未来趋势，强调统一入口和内置控制能力。
categories:
- AI基础设施
tags:
- Cloudflare
- AI Gateway
- Workers AI
- 模型路由
- 控制平面
draft: false
translated_at: '2026-08-13T04:23:30.548599'
---

AI Gateway和Workers AI最初是作为独立产品推出的，但随着时间的推移，我们注意到用户的使用方式正在趋同。通过AI Gateway，你可以代理请求到任何模型提供商，并获得内置的可观测性、日志记录、访问控制和安全性。在Workers AI上，我们在自己管理的GPU基础设施上托管模型，并暴露一个API端点，供你以服务形式调用推理能力。

这些产品的架构看起来不同，但对最终用户而言，它们实现的是同一个目标：通过一个精细的控制平面将你与模型连接起来。今天，我们很高兴地分享这些产品如何融合为一条统一路径的计划，这样你就可以连接到任何模型提供商（包括Workers AI），同时从单一控制平面管理可观测性、计费、安全性和日志记录。

这是我们宏大计划中的下一步——请继续阅读，了解统一控制平面对于模型路由的未来意味着什么。

## 合并绑定与API

我们一直在通过入口点——Workers绑定和REST API——暗示这些产品正变得更加统一。我们有一个AI绑定，你可以用它来调用AI Gateway和Workers AI。这里不存在单独的AI Gateway绑定和Workers AI绑定之分：所有请求都走同一条路径。几个月前，我们推出了“默认”网关的概念，这样即使你从未设置过AI Gateway，也能自动继承AI Gateway的可观测性和日志记录。当然，如果你想把应用拆分为多个项目，你仍然可以指定自己的网关。

以下是通过AI Gateway调用Workers AI时绑定调用的示例：

```javascript
export default {
  async fetch(request, env) {
    const response = await env.AI.run(
      '@cf/zai-org/glm-5.2',
      {
        messages: [
          { role: 'user', content: 'What is the capital of France?' },
        ]
      },
      {
        gateway: {
          id: 'default', // 使用'default'作为内置网关
        },
      }
    );

    return new Response(JSON.stringify(response), {
      headers: { 'Content-Type': 'application/json' },
    });
  },
};
```

我们还宣布了一个统一的REST API——`/ai/`端点，允许你通过AI Gateway对Workers AI发起类似的调用。

```bash
curl "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/zai-org/glm-5.2" \
  -H "Authorization: Bearer {api_token}" \
  -H "Content-Type: application/json" \
  -H "cf-aig-gateway-id: default" \
  -d '{
    "messages": [{"role": "user", "content": "What is the capital of France?"}],
  }'
```

这样做让我们能够统一AI Gateway和Workers AI的入口点，这样你就不需要先决定使用哪个产品：一切都是开箱即用的。

## 所有Workers AI用户自动获得可观测性和控制能力

这种融合最直接的好处之一是，你不再需要先显式创建一个AI Gateway才能开始获得推理流量的可见性。如果你从未设置过网关，只需在绑定或REST API调用中将`default`作为网关ID传入，AI Gateway会在第一次经过身份验证的请求时自动创建它。

这样一来，每个请求都会被记录完整的请求和响应负载，每个模型的Token数量都会被跟踪，而且无需任何仪表盘设置即可获得成本归属。如果之后默认网关不再满足你的需求——比如你想要自定义缓存规则或按应用拆分流量——你可以创建一个命名网关，并通过修改一个参数将请求指向它。

以下是在绑定中的使用方式。之前，你直接调用Workers AI：

```javascript
const response = await env.AI.run('@cf/zai-org/glm-5.2', {
  messages: [{ role: 'user', content: 'Hello!' }],
});
```

现在，添加第三个参数即可通过AI Gateway路由并获得完整的可观测性：

```javascript
const response = await env.AI.run(
  '@cf/zai-org/glm-5.2',
  { messages: [{ role: 'user', content: 'Hello!' }] },
  { gateway: { id: 'default' } } // 首次使用时自动创建网关
);
```

前往Cloudflare AI Gateway仪表盘，你会看到每个请求：延迟分解、Token用量、错误率，以及确切的提示词和响应。对于调试模型行为或审计AI输出的团队来说，这相比盲目操作是一次巨大的升级。

## 新功能：将AI Gateway额度用于Workers AI

我们今天推出的另一项新功能是，可以将AI Gateway额度用于Workers AI。之前，你只能在外部模型提供商（如OpenAI、Anthropic）上使用AI Gateway额度，但还不能将AI Gateway额度用于Workers AI的使用。我们终于启用了系统，允许对Workers AI进行统一计费。这意味着你可以充值一个钱包，然后在OpenAI、Anthropic、Workers AI或我们支持的任何提供商之间自由分配使用。

由于我们现在为Workers AI提供预付费计费，并且希望鼓励用户使用这条新路径，如果你使用AI Gateway统一计费，我们还会为Workers AI模型提供更高的速率限制。请参阅开发者文档，了解速率限制的最新信息以及如何申请更高的速率限制。

## 即将推出：模型优先路由

当所有推理流量都流经单一控制平面后，我们就可以开始做出更智能的请求服务决策——从你想要的模型出发，而不是从你必须管理的提供商出发。提供商优先路由迫使你考虑基础设施问题：“我该调用哪个提供商？如果他们宕机了怎么办？”模型优先路由则颠覆了这一点。你只需要考虑你的需求——一个强大的推理模型、一个快速的摘要模型、一个廉价的嵌入模型——控制平面会处理提供商选择、故障转移和负载均衡。

今天，如果你想调用一个模型，你必须知道哪个提供商托管它。如果该提供商宕机或对你进行速率限制，你的应用就会中断。我们正在朝着这样一个世界迈进：你指定模型，AI Gateway处理其余一切。

这样一来，你可以请求Kimi K2.7 Code，而不必关心它来自Workers AI、Moonshot自己的API，还是托管相同权重的其他提供商。如果Workers AI有容量，你就能享受我们托管基础设施的好处。如果Workers AI已满负荷，网关会透明地将你负载均衡到另一个可以提供相同模型的提供商。如果你愿意，你仍然可以选择只使用单一提供商，但如果你关心弹性，模型优先路由能为你带来更多灵活性。我们与经过审查的提供商合作，因此模型输出的质量始终是首要任务，同时我们也能满足零数据保留（ZDR）等要求。

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/v1/chat/completions" \
  -H "Authorization: Bearer {api_token}" \
  -H "cf-aig-gateway-id: my-gateway" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kimi-k2.7-code",
    "messages": [{"role": "user", "content": "Review this function"}]
  }'
```

这也意味着默认情况下具有更好的弹性。如果某个提供商的模型版本出现问题，流量会自动转移到另一个提供商，而无需在Workers中进行应用级重试或复杂的回退逻辑。网关将模型可用性视为一个路由问题。我们希望在接下来的几个月内为所有AI Gateway和Workers AI用户启动试点。

## 下一步：智能路由

路由的下一个演进超越了简单的故障转移。我们正在构建智能路由，它能够理解你的请求内容，并在无需任何配置的情况下为任务选择正确的模型。

不再指定某个模型，你可以让网关来做决定。在底层，一个运行在 Workers AI 上的分类器会读取你的提示词，并预测它属于哪类任务（编码、研究、摘要、通用问答）、复杂度如何，以及上下文的重要性。然后，一个启发式评分器会将其映射到精选模型池中的最佳模型。对于想要掌控的团队，你仍然可以指定确切的模型。对于其他所有人来说，零配置路径意味着你可以在不维护自己的路由逻辑的情况下，获得更好的经济效益和性能。我们目前正在内部试点这一功能，并将在发布前的接下来几周内积极测试和迭代。

## 今日开始使用

如果你已经在使用 Workers AI，尝试这一功能最简单的方式就是开始将你现有的调用路由到一个默认网关。你将立即获得请求日志、Token 跟踪和成本归属，而无需改变你调用模型的任何其他方式。

如果你已经在使用 AI Gateway，将 Workers AI 加入其中就像调用一个 Workers AI 模型一样简单。为你的 AI Gateway 钱包充值，你将获得我们支持的所有提供商的统一计费，以及在 Workers AI 模型上更高的速率限制。

设置你的第一个网关，浏览 Workers AI 模型目录，今天就开始构建吧。

![BLOG-3407 2.png](/images/posts/f99b30d03b83.jpg)

- Cloudflare
- Michelle Chen
- Ming Lu

---

> 本文由AI自动翻译，原文链接：[Unifying Workers AI and AI Gateway into a single AI control plane](https://blog.cloudflare.com/workers-ai-gateway-unification/)
> 
> 翻译时间：2026-08-13 04:23
