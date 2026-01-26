---
title: Python Workflows 进入公测，Cloudflare 工作流编排支持 Python
title_original: A closer look at Python Workflows, now in beta
date: '2025-11-10'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/python-workflows/
author: Caio Nogueira
summary: Cloudflare 宣布其 Workflows 编排服务现已支持 Python 语言，结束了此前仅支持 TypeScript 的限制。Python
  在数据管道、AI/ML 和任务自动化等领域占据主导地位，此次更新让开发者能够使用熟悉的语言构建长时间运行、多步骤的应用程序。文章介绍了 Python Workflows
  的应用场景（如 LLM 训练、数据管道、AI Agent 开发），并概述了其技术实现原理，即基于 Workers 和 Durable Objects，为 Python
  用户提供符合语言习惯的持久执行 API。
categories:
- AI基础设施
tags:
- Cloudflare
- Python
- 工作流编排
- Serverless
- AI开发
draft: false
translated_at: '2026-01-06T01:18:01.093Z'
---

开发者已经可以使用 Cloudflare Workflows 在 Workers 上构建长时间运行的多步骤应用程序。现在，Python Workflows 也已到来，这意味着您可以使用自己选择的语言来编排多步骤应用程序。

通过 Workflows，您可以使用内置的错误处理和重试行为，自动化应用程序中的一系列幂等步骤。但 Workflows 最初仅支持 TypeScript。由于 Python 是数据管道、人工智能/机器学习以及任务自动化等领域事实上的首选语言——所有这些都严重依赖于编排——这给许多开发者带来了不便。

多年来，我们一直在为开发者提供在 Cloudflare 上使用 Python 构建这些应用程序的工具。2020 年，我们通过 Transcrypt 将 Python 引入 Workers，随后在 2024 年直接将 Python 集成到 workerd 中。今年早些时候，我们在 Workers 中构建了对 CPython 以及任何在 Pyodide 中构建的包（如 matplotlib 和 pandas）的支持。现在，Python Workflows 也获得了支持，因此开发者可以使用他们最熟悉的语言创建健壮的应用程序。

**为什么选择 Python 用于 Workflows？**

想象一下您正在训练一个 LLM（大语言模型）。您需要标注数据集、输入数据、等待模型运行、评估损失、调整模型，然后重复。如果没有自动化，您需要手动启动每个步骤，监控其完成，然后再启动下一个步骤。相反，您可以使用一个工作流来编排模型的训练，在前一个步骤完成后触发下一个步骤。对于任何需要的手动调整，例如评估损失并相应调整模型，您可以实现一个步骤来通知您并等待必要的输入。

考虑数据管道，这是 Python 用于数据摄取和处理的主要用例。通过一组定义好的幂等步骤来自动化数据管道，开发者可以部署一个工作流来为他们处理整个数据管道。

再举一个例子：构建 AI Agent（智能体），例如一个管理您杂货购物的智能体。每周，您输入您的食谱列表，智能体将（1）编译所需食材清单，（2）检查您前几周剩余的食材，以及（3）从您当地的杂货店订购差额部分以便取货。使用 Workflow，这可能看起来像：

```
await step.wait_for_event()
用户输入杂货清单
step.do()
编译所需食材清单
step.do()
根据剩余食材核对所需食材清单
step.do()
调用 API 下单
step.do()
进行支付
```

使用 workflows 作为在 Cloudflare 上构建 Agent（智能体）的工具，可以简化 Agent 的架构，并通过单个步骤的重试和状态持久性来提高其完成任务的几率。对 Python Workflows 的支持意味着使用 Python 构建 Agent 比以往任何时候都更容易。

**Python Workflows 如何工作**

Cloudflare Workflows 使用我们为持久执行创建的基础设施，同时为 Python 用户提供了一种符合语言习惯的方式来编写他们的工作流。此外，我们的目标是实现 JavaScript 和 Python SDK 之间的完全功能对等。这是可能的，因为 Cloudflare Workers 直接在运行时本身支持 Python。

**创建 Python Workflow**

Cloudflare Workflows 完全构建在 Workers 和 Durable Objects 之上。每个元素都在存储 Workflow 元数据和实例级信息中发挥作用。有关 Workflows 平台如何工作的更多细节，请查看这篇博客文章。

在 Workflows 控制平面的最底层是用户 Worker，即 `WorkflowEntrypoint`。当 Workflow 实例准备运行时，Workflow 引擎将通过 RPC 调用用户 worker 的 `run` 方法，在本例中，这将是一个 Python Worker。

这是官方文档提供的一个 Workflow 声明示例框架：

```
export class MyWorkflow extends WorkflowEntrypoint<Env, Params> {
    async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
        // Steps here
    }
}
```

如上所示，`run` 方法提供了一个实现了持久执行 API 的 `WorkflowStep` 参数。这是用户依赖的“至多一次”执行。这些 API 是用 JavaScript 实现的，需要在 Python Worker 的上下文中访问。

一个 `WorkflowStep` 必须跨越 RPC 屏障，这意味着引擎（调用者）将其作为 `RpcTarget` 公开。这种设置允许用户的 Workflow（被调用者）用一个存根替换该参数。然后，该存根通过 RPC 回调用引擎，从而启用 Workflows 的持久执行 API。要了解更多关于 RPC 序列化以及函数如何从调用者和被调用者传递的信息，请阅读远程过程调用文档。

所有这些对于 Python 和 JavaScript Workflows 都是成立的，因为我们并没有真正改变从 Workflows 端调用用户 Worker 的方式。然而，在 Python 的情况下，还存在另一个障碍——Python 和 JavaScript 模块之间的语言桥接。当 RPC 请求针对 Python Worker 时，有一个 JavaScript 入口点模块负责将请求代理给 Python 脚本处理，然后返回给调用者。这个过程通常涉及在处理请求之前和之后进行类型转换。

**克服语言障碍**

Python workers 依赖于 Pyodide，它是 CPython 到 WebAssembly 的移植版本。Pyodide 提供了一个到 JavaScript 的外部函数接口（FFI），允许从 Python 调用 JavaScript 方法。这是允许其他绑定和 Python 包在 Workers 平台内工作的机制。因此，我们不仅使用这个 FFI 层来允许直接使用 Workflow 绑定，而且还提供 Python 中的 `WorkflowStep` 方法。换句话说，考虑到 `WorkflowEntrypoint` 是运行时的一个特殊类，`run` 方法被手动包装，以便 `WorkflowStep` 作为 `JsProxy` 公开，而不是像其他 JavaScript 对象那样进行类型转换。此外，通过从用户 Worker 的角度包装 API，我们允许自己对整体开发体验进行一些调整，而不是简单地将一个具有不同语义的 JavaScript SDK 暴露给另一种语言。

**使 Python Workflows SDK 符合 Python 习惯**

将 Workflows 移植到 Python 的一个重要部分包括公开一个 Python 用户熟悉且使用无障碍的接口，类似于我们的 JavaScript API 的做法。让我们退一步，看一段用 TypeScript 编写的 Workflow 定义代码片段。

```
import { WorkflowEntrypoint, WorkflowStep, WorkflowEvent} from 'cloudflare:workers';

export class MyWorkflow extends WorkflowEntrypoint {
    async run(event: WorkflowEvent<YourEventType>, step: WorkflowStep) {
        let state = step.do("my first step", async () => {
            // Access your properties via event.payload
            let userEmail = event.payload.userEmail
            let createdTimestamp = event.payload.createdTimestamp
            return {"userEmail": userEmail, "createdTimestamp": createdTimestamp}
        })

        step.sleep("my first sleep", "30 minutes");
        await step.waitForEvent<EventType>("receive example event", { type: "simple-event", timeout: "1 hour" })
        const developerWeek = Date.parse("22 Sept 2025 13:00:00 UTC");
        await step.sleepUntil("sleep until X times out", developerWeek)
    }
}
```

workflows API 的 Python 实现需要修改 `do` 方法。与其他语言不同，Python 不容易支持匿名回调。这种行为通常通过使用装饰器来实现，在本例中，装饰器允许我们以符合语言习惯的方式拦截方法并公开它。

换句话说，所有参数保持其原始顺序，被装饰的方法作为回调函数。
方法 `waitForEvent`、`sleep` 和 `sleepUntil` 可以保留其原始签名，只要它们的名称转换为蛇形命名法即可。

以下是实现相同工作流程的对应 Python 版本，能达到类似的行为：

```python
from workers import WorkflowEntrypoint

class MyWorkflow(WorkflowEntrypoint):
    async def run(self, event, step):
        @step.do("my first step")
        async def my_first_step():
            user_email = event["payload"]["userEmail"]
            created_timestamp = event["payload"]["createdTimestamp"]
            return {
                "userEmail": user_email,
                "createdTimestamp": created_timestamp,
            }

        await my_first_step()
        step.sleep("my first sleep", "30 minutes")

        await step.wait_for_event(
            "receive example event",
            "simple-event",
            timeout="1 hour",
        )

        developer_week = datetime(2024, 10, 24, 13, 0, 0, tzinfo=timezone.utc)
        await step.sleep_until("sleep until X times out", developer_week)
```

在设计工作流时，我们经常需要管理步骤之间的依赖关系，即使其中一些任务可以并发处理。尽管我们可能没有特意考虑，但许多工作流都具有有向无环图（DAG）的执行流程。在 Python 工作流的第一个迭代版本（即：向 Python Workers 的最小化移植）中实现并发是可行的，因为 Pyodide 会捕获 JavaScript 的 thenable 对象并将其代理为 Python 的 awaitable 对象。

因此，`asyncio.gather` 可以作为 `Promise.all` 的对应物。虽然这在 SDK 中完全可用且已准备就绪，但我们也支持声明式的方法。

装饰 `do` 方法的优势之一在于，我们基本上可以在原始 API 之上提供进一步的抽象，并让它们在入口点包装器上工作。以下是一个利用所引入的 DAG 功能的 Python API 示例：

```python
from workers import Response, WorkflowEntrypoint

class PythonWorkflowDAG(WorkflowEntrypoint):
        @step.do('dependency 1')
        async def dep_1():
            # does stuff
            print('executing dep1')

        @step.do('dependency 2')
        async def dep_2():
            # does stuff
            print('executing dep2')

        @step.do('demo do', depends=[dep_1, dep_2], concurrent=True)
        async def final_step(res1=None, res2=None):
            # does stuff
            print('something')

        await final_step()
```

这种方法使得工作流声明更加清晰，将状态管理留给工作流引擎的数据平面以及 Python workers 的工作流包装器。请注意，即使多个步骤可以以相同的名称运行，引擎也会略微修改每个步骤的名称以确保唯一性。在 Python 工作流中，一旦涉及某个依赖项的初始步骤成功完成，该依赖项即被视为已解决。

立即查看如何用 Python 编写 Workers 并创建您的第一个 Python 工作流！如果您有任何功能请求或发现任何错误，请通过加入 Discord 上的 Cloudflare 开发者社区，直接向 Cloudflare 团队分享您的反馈。


> 本文由AI自动翻译，原文链接：[A closer look at Python Workflows, now in beta](https://blog.cloudflare.com/python-workflows/)
> 
> 翻译时间：2026-01-06 01:18
