---
title: 为智能体时代重构Workflows控制平面
title_original: Rearchitecting the Workflows control plane for the agentic era
date: '2026-04-15'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/workflows-v2/
author: ''
summary: 本文介绍了为适应智能体时代工作负载变化而对Workflows控制平面进行的架构重构。随着智能体触发的工作流数量激增，原有架构面临瓶颈。文章阐述了从V1到V2的演进过程，通过引入新组件实现水平扩展，将并发实例支持从4,500个提升至50,000个，实例创建速率从每秒100个提升至300个，以支持智能体以机器速度大规模、持久化地运行工作流。
categories:
- AI基础设施
tags:
- 工作流引擎
- 智能体
- 系统架构
- 可扩展性
- 云原生
draft: false
translated_at: '2026-04-16T05:03:11.448200'
---

# 为智能体时代重构Workflows控制平面

2026-04-15

- LuÃ­s Duarte
- Mia Malden
- AndrÃ© Venceslau

![](/images/posts/4200dfa5aed1.png)

当我们最初构建Workflows（我们用于多步骤应用程序的持久化执行引擎）时，其设计面向的是一个由人类行为触发工作流的世界，例如用户注册或下单。对于像用户引导流程这样的用例，每个用户只需支持一个工作流实例——而且人的点击速度终究有限。

然而，随着时间的推移，我们实际观察到工作负载和访问模式发生了量变：由人类触发的工作流变少，而由智能体触发、以机器速度创建的工作流则越来越多。

随着智能体成为持久且自主的基础设施，代表用户运行数小时甚至数天，它们需要一个持久、异步的执行引擎来处理其工作。Workflows恰好提供了这一点：每个步骤都可以独立重试，工作流可以暂停以等待人工介入审批，并且每个实例在发生故障时都能存活而不丢失进度。

此外，工作流本身正被用于实现智能体循环，并作为管理和维持智能体存活的持久化框架。我们的Agents SDK集成加速了这一进程，使得智能体能够轻松生成工作流实例并获取实时进度。现在，单个智能体会话可以启动数十个工作流，而许多智能体并发运行意味着每秒可以创建数千个实例。随着Project Think的推出，我们预计这一速度只会继续提升。

为了帮助开发者在Workflows上扩展其智能体和应用程序，我们很高兴地宣布，我们现在支持：

- 50,000个并发实例（并行运行的工作流执行数量），原为4,500个
- 每个账户每秒创建300个实例，原为100个
- 每个工作流200万个排队实例（指已创建或唤醒并正在等待并发槽位的实例），原为100万个

50,000个并发实例（并行运行的工作流执行数量），原为4,500个

每个账户每秒创建300个实例，原为100个

每个工作流200万个排队实例（指已创建或唤醒并正在等待并发槽位的实例），原为100万个

我们基于使用数据和第一性原理重新设计了Workflows控制平面，以支持这些提升。对于控制平面的V1版本，单个Durable Object（DO）可以充当整个账户的中心注册表和协调器。对于V2版本，我们构建了两个新组件，以帮助系统水平扩展并缓解V1引入的瓶颈，然后将所有客户（连同实时流量）无缝迁移到新版本上。

## V1：Workflows的初始架构

正如我们在公开测试版博客文章中所描述的，我们完全基于自己的开发者平台构建了Workflows。从根本上说，工作流是一系列持久化的步骤，每个步骤都可以独立重试，可以执行任务、等待外部事件或休眠到预定时间。

```javascript
export class MyWorkflow extends WorkflowEntrypoint {

  async run(event, step) {
    const data = await step.do("fetch-data", async () => {
      return fetchFromAPI();
    });

    const approval = await step.waitForEvent("approval", {
      type: "approval",
      timeout: "24 hours",
    });

    await step.do("process-and-save", async () => {
      return store(transform(data));
    });
  }
}

```

为了触发每个实例、执行其逻辑并存储其元数据，我们利用了基于SQLite的Durable Objects，这是在分布式系统内进行协调和存储的简单而强大的原语。

在控制平面中，一些Durable Objects——例如执行实际工作流实例（包括其步骤、重试和休眠逻辑）的Engine——以每个实例1:1的比例启动。另一方面，Account是一个账户级别的Durable Object，负责管理该账户的所有工作流和工作流实例。

要了解更多关于V1控制平面的信息，请参阅我们的Workflows发布博客文章。

在我们将Workflows推出测试版后，我们很高兴看到客户迅速扩展了对产品的使用，但我们也意识到，使用单个Durable Object来存储所有账户级别的信息会引入瓶颈。许多客户需要每分钟创建和执行数百甚至数千个工作流实例，这在我们最初的架构中可能很快使Account不堪重负。最初的速率限制——4,500个并发槽位和每10秒创建100个实例——就是这一限制的结果。

在V1控制平面上，这些限制是硬性上限。所有依赖于Account的操作，包括创建、更新和列出，都必须经过那个单一的DO。具有高并发工作负载的用户可能在任意时刻都有数千个实例启动和结束，导致每秒对Account的请求量高达数千次。为了解决这个问题，我们重新设计了工作流控制平面，使其能够水平扩展到更高的并发和创建速率限制。

## V2：为更高吞吐量实现水平扩展

对于新版本，我们从头开始重新思考了每一个操作，目标是优化高吞吐量的工作流。最终，Workflows应该能够扩展以支持开发者所需的任何规模——无论是每秒创建数千个实例，还是同时运行数百万个实例。我们还希望确保V2允许灵活的限额，我们可以调整并持续提高这些限额，而不是像V1限制那样设置硬性上限。经过多次设计迭代，我们为新架构确立了以下支柱：

- 给定实例存在性的唯一可信来源应该是其Engine，而非其他。在V1控制平面架构中，我们在将实例加入队列之前，缺少对其Engine是否实际存在的检查。这可能导致一种不良状态：实例可能已排队，但其对应的Engine尚未启动。
- 实例生命周期和活跃度机制必须能够按工作流水平扩展，并分布在多个区域。
- 新的Account单例应仅存储最必要的元数据，并具有恒定的最大并发请求量。

给定实例存在性的唯一可信来源应该是其Engine，而非其他。

- 在V1控制平面架构中，我们在将实例加入队列之前，缺少对其Engine是否实际存在的检查。这可能导致一种不良状态：实例可能已排队，但其对应的Engine尚未启动。
- 实例生命周期和活跃度机制必须能够按工作流水平扩展，并分布在多个区域。

在V1控制平面架构中，我们在将实例加入队列之前，缺少对其Engine是否实际存在的检查。这可能导致一种不良状态：实例可能已排队，但其对应的Engine尚未启动。

实例生命周期和活跃度机制必须能够按工作流水平扩展，并分布在多个区域。

新的Account单例应仅存储最必要的元数据，并具有恒定的最大并发请求量。

V2控制平面中有两个新的关键组件，使我们能够提升工作流的可扩展性：**SousChef**和**Gatekeeper**。第一个组件**SousChef**，是**Account**的“副手”。回顾一下，之前**Account**负责管理给定账户内所有工作流中所有实例的元数据和生命周期。引入**SousChef**是为了跟踪**特定工作流中一部分实例**的元数据和生命周期。在一个账户内，分布式的**SousChef**可以以更高效、更易管理的方式向**Account**报告。（这个设计的一个额外好处是：我们不仅已经实现了按账户隔离，而且无意中还获得了同一账户内的“按工作流”隔离，因为每个**SousChef**只负责一个特定的工作流）。

第二个组件**Gatekeeper**，是一种在账户内所有**SousChef**之间分配并发“槽位”（源自并发限制）的机制。它充当一个租赁系统。当创建一个实例时，它会被随机分配给该账户内的一个**SousChef**。然后，该**SousChef**向**Account**发出请求以触发该实例。要么授予一个槽位，要么将实例排队。一旦槽位被授予，**SousChef**就会触发实例的执行，并承担确保实例永不卡住的责任。

需要**Gatekeeper**来确保**Engine**永远不会使它们的**Account**过载（这是V1上一个紧迫的风险），因此**SousChef**与其**Account**之间的所有通信都按周期进行，每秒一次——每个周期还会批量处理所有槽位请求，确保只进行一次JSRPC调用。这确保了实例创建速率永远不会使最重要的组件**Account**过载或影响其性能（顺便提一下：如果**SousChef**数量过多，我们会进行速率限制调用，或者在不同时间段分散到不同的**SousChef**上）。此外，这种周期性特性使我们能够保持对旧实例的公平性，并通过多个**SousChef**确保最大最小公平性，让它们都能取得进展。例如，如果一个实例被唤醒，它应该比一个新创建的实例优先获得槽位，但每个**SousChef**都确保自己的实例不会卡住。

这种架构更加分布式，因此更具可扩展性。现在，当创建一个实例时，请求路径是：

1.  检查控制平面版本
2.  检查该位置是否有工作流和版本详细信息的缓存版本
    1.  如果没有，检查**Account**以获取工作流名称、唯一ID和版本，并缓存该信息
3.  仅将必要的元数据（实例负载、创建日期）存储到其自身的**Engine**上

那么，**Engine**如何告诉控制平面它现在存在呢？这发生在实例元数据设置完成后的后台。由于Durable Object上的后台操作可能会因驱逐或服务器故障而失败，我们还在创建热路径上为**Engine**设置了一个“警报”。这样，如果后台任务没有完成，警报会**确保**实例将开始运行。

**Durable Object警报**允许Durable Object实例在未来某个精确的时间点被唤醒，采用**至少一次**执行模型，并内置自动重试。我们广泛使用这种后台“任务”和警报的组合，将操作移出热路径，同时仍然确保一切按计划进行。这就是我们如何在不影响可靠性的前提下，保持**创建实例**等关键操作的快速性。

除了实现规模扩展外，这个版本的控制平面还意味着：

*   实例列表性能更快，并且实际上与游标分页保持一致；
*   对实例的任何操作都只进行一次网络跳转（因为它可以直接访问其**Engine**，确保用户请求延迟尽可能小）；
*   我们可以确保更多实例实际上在并发时正确运行（按时运行）（如果不正确则进行纠正，确保**Engine**永远不会延迟继续执行）。

## V1 → V2 迁移

既然我们有了一个能够处理更高用户负载的工作流控制平面新版本，我们需要做“枯燥”的部分：将我们的客户和实例迁移到新系统。在Cloudflare的规模下，这本身就成了一个问题，因此“枯燥”的部分变成了最大的挑战。在工作流上线不到一年的时候，它已经积累了数百万个实例和数千名客户。此外，V1控制平面上的一些技术债务意味着排队的实例可能还没有创建自己的**Engine** Durable Object，这使问题进一步复杂化。

这样的迁移很棘手，因为客户可能在任何给定时刻都有实例在运行；我们需要一种方法，在不造成任何中断或停机的情况下，将**SousChef**和**Gatekeeper**组件添加到旧账户中。

我们最终决定将现有的**Account**（我们称之为**AccountOld**）迁移为像**SousChef**一样运行。通过持久化**Account** DO，我们保留了实例元数据，并简单地将DO转换为**SousChef** “DO”：

```JavaScript
// You might be wondering what's this SousChef class? This is the SousChef DO class!
import { SousChef } from "@repo/souschef";

class AccountOld extends DurableObject {
  constructor(state: DurableObjectState, env: Env) {
    // We added the following snippet to the end of our AccountOld DO's
    // constructor. This ensures that if we want, we can use any primitive
    // that is available on SousChef DO
    if (this.currentVersion === ControlPlaneVersions.SOUS_CHEFS) {
      this.sousChef = new SousChef(this.ctx, this.env);
      await this.sousChef.setup()
    }
  }

  async updateInstance(params: UpdateInstanceParams) {
    if (this.currentVersion === ControlPlaneVersions.SOUS_CHEFS) {
      assert(this.sousChef !== undefined, 'SousChef must exist on v2');
      return this.sousChef.updateInstance(params);
    }

    // old logic remains the same
  }

  @RequiresVersion<AccountOld>(ControlPlaneVersions.V1)
  async getMetadata() {
    // this method can only be run if 
    // this.currentVersion === ControlPlaneVersions.V1
  }
}
```

我们可以在**AccountOld**内部实例化**SousChef**类，因为跟踪实例元数据的SQL表在**SousChef**和**AccountOld** DO上是相同的。因此，我们可以直接决定使用哪个版本的代码。如果不是这种情况，我们将被迫迁移数百万个实例的元数据，这会使迁移对每个账户来说更加困难和耗时。那么，迁移是如何进行的呢？

首先，我们准备好**AccountOld** DO，以便将其切换为像**SousChef**一样运行（这意味着创建一个包含上述代码片段的版本）。然后，我们按账户启用控制平面V2，这大致同时触发了接下来的三个步骤：

- 所有新的实例创建请求现在均被路由至新的SousChefs（SousChefs在收到首个请求时创建），新实例不再流向AccountOld；
- AccountOldDOs开始自行迁移，以表现得像SousChefs；
- 新的AccountDO随相应的元数据一同启动。

所有新的实例创建请求现在均被路由至新的SousChefs（SousChefs在收到首个请求时创建），新实例不再流向AccountOld；

AccountOldDOs开始自行迁移，以表现得像SousChefs；

新的AccountDO随相应的元数据一同启动。

在所有账户迁移至新的控制平面版本后，随着其实例保留期到期，我们得以逐步淘汰AccountOldDOs。一旦AccountOlds上所有账户的所有实例均完成迁移，我们便可永久关闭这些DOs。整个迁移过程实现了零停机，真正体验到了"行驶中更换车轮"的感觉。

## 尝试使用

如果您是Workflows的新用户，请尝试我们的[入门指南](https://developers.cloudflare.com/workers/learning/getting-started/)或使用Workflows[构建您的首个持久化Agent](https://developers.cloudflare.com/workers/learning/build-your-first-durable-agent/)。

如果您的使用场景需要高于我们新默认值的限制——并发限制为50,000个槽位，账户级创建速率限制为每秒300个实例、每个工作流100个实例——请通过您的账户团队或[Workers限额申请表单](https://forms.gle/4bK5gS4Vqj8gv6tS9)联系我们。您也可以通过我们的[Discord服务器](https://discord.com/invite/cloudflaredev)提供反馈、提出功能请求，或分享您使用Workflows的方式。

---

> 本文由AI自动翻译，原文链接：[Rearchitecting the Workflows control plane for the agentic era](https://blog.cloudflare.com/workflows-v2/)
> 
> 翻译时间：2026-04-16 05:03
