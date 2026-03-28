---
title: 利用抽象语法树将工作流代码静态解析为可视化图表
title_original: How we use Abstract Syntax Trees (ASTs) to turn Workflows code into
  visual diagrams
date: '2026-03-27'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/workflow-diagrams/
author: ''
summary: 本文介绍了Cloudflare团队如何利用抽象语法树（AST）技术，将动态执行的Workflows代码在部署时静态解析，并生成可视化执行图表。文章阐述了动态执行模型带来的挑战，以及通过解析打包后的代码、构建中间图并最终渲染图表的完整流程。该功能旨在帮助开发者直观理解复杂工作流的执行逻辑、并行分支和依赖关系，尤其在AI智能体自动生成代码的背景下尤为重要。
categories:
- AI基础设施
tags:
- 抽象语法树
- 工作流引擎
- 代码可视化
- Cloudflare
- 静态分析
draft: false
translated_at: '2026-03-28T04:47:01.546728'
---

# 我们如何利用抽象语法树（AST）将工作流代码转化为可视化图表

2026-03-27

- AndrÃ© Venceslau
- Mia Malden

![](/images/posts/20bfb32b1b3d.png)

Cloudflare Workflows 是一个持久化执行引擎，允许您串联步骤、在失败时重试，并在长时间运行的进程中保持状态。开发者使用 Workflows 来驱动后台 Agent（智能体）、管理数据管道、构建人机协同审批系统等。

上个月，我们宣布，现在部署到 Cloudflare 的每个工作流在仪表板中都拥有一个完整的可视化图表。

我们构建此功能是因为，如今能够可视化您的应用程序比以往任何时候都更加重要。编码 Agent（智能体）正在编写您可能阅读也可能不阅读的代码。然而，所构建内容的形态仍然很重要：步骤如何连接、在哪里分支以及实际发生了什么。

如果您以前见过可视化工作流构建器生成的图表，它们通常基于声明式的内容工作：JSON 配置、YAML、拖放操作。然而，Cloudflare Workflows 就是代码。它们可以包含 `Promise`、`Promise.all`、循环、条件语句，并且/或者可以嵌套在函数或类中。这种动态执行模型使得渲染图表变得稍微复杂一些。

我们使用抽象语法树（AST）来静态推导出图表，追踪 `Promise` 和 `await` 关系，以理解哪些部分并行运行、哪些部分阻塞以及各个部分如何连接。

继续阅读以了解我们如何构建这些图表，或者部署您的第一个工作流并亲自查看图表。

以下是一个由 Cloudflare Workflows 代码生成的图表示例：

### 动态工作流执行

通常，工作流引擎可以根据动态或顺序（静态）执行顺序来执行。顺序执行可能看起来是更直观的解决方案：触发工作流 → 步骤 A → 步骤 B → 步骤 C，其中步骤 B 在引擎完成步骤 A 后立即开始执行，依此类推。

Cloudflare Workflows 遵循动态执行模型。由于工作流就是代码，步骤会在运行时遇到它们时执行。当运行时发现一个步骤时，该步骤会被传递给工作流引擎，引擎负责管理其执行。除非被 `await`，否则步骤本身并不是顺序的——引擎会并行执行所有未被 `await` 的步骤。这样，您就可以将工作流代码编写为流程控制，而无需额外的包装器或指令。以下是交接工作的方式：

1.  一个引擎（作为该实例的“监督者” Durable Object）启动。引擎负责实际工作流执行的逻辑。
2.  引擎通过动态分派触发一个用户 Worker，将控制权移交给 Workers 运行时。
3.  当运行时遇到 `step.do` 时，它将执行权交还给引擎。
4.  引擎执行该步骤，持久化结果（或在适用时抛出错误），并再次触发用户 Worker。

在这种架构下，引擎本身并不“知道”它正在执行的步骤的顺序——但对于图表来说，步骤的顺序变得至关重要。这里的挑战在于将绝大多数工作流准确地转换为对诊断有帮助的图表；随着图表处于测试阶段，我们将继续迭代和改进这些表示形式。

### 解析代码

在部署时（而非运行时）获取脚本，使我们能够完整地解析工作流，以静态生成图表。

退一步讲，以下是工作流部署的生命周期：

为了创建图表，我们在脚本被部署 Workers 的内部配置服务打包后获取它（工作流部署下的步骤 2）。然后，我们使用解析器创建一个表示工作流的抽象语法树（AST），我们的内部服务生成并遍历一个包含所有 WorkflowEntrypoints 和对工作流步骤调用的中间图。我们根据 API 上的最终结果渲染图表。

当部署一个 Worker 时，配置服务会打包（默认使用 `esbuild`）并压缩代码（除非另有指定）。这带来了另一个挑战——虽然 TypeScript 中的 Workflows 遵循直观的模式，但它们被压缩后的 JavaScript（JS）代码可能非常密集且难以理解。根据打包器的不同，代码的压缩方式也可能不同。

以下是一个展示 Agent（智能体）并行执行的 Workflow 代码示例：

```TypeScript
const summaryPromise = step.do(
         `summary agent (loop ${loop})`,
         async () => {
           return runAgentPrompt(
             this.env,
             SUMMARY_SYSTEM,
             buildReviewPrompt(
               'Summarize this text in 5 bullet points.',
               draft,
               input.context
             )
           );
         }
       );
        const correctnessPromise = step.do(
         `correctness agent (loop ${loop})`,
         async () => {
           return runAgentPrompt(
             this.env,
             CORRECTNESS_SYSTEM,
             buildReviewPrompt(
               'List correctness issues and suggested fixes.',
               draft,
               input.context
             )
           );
         }
       );
        const clarityPromise = step.do(
         `clarity agent (loop ${loop})`,
         async () => {
           return runAgentPrompt(
             this.env,
             CLARITY_SYSTEM,
             buildReviewPrompt(
               'List clarity issues and suggested fixes.',
               draft,
               input.context
             )
           );
         }
       );
```

使用 `rspack` 打包后，压缩代码的片段如下所示：

```JavaScript
class pe extends e{async run(e,t){de("workflow.run.start",{instanceId:e.instanceId});const r=await t.do("validate payload",async()=>{if(!e.payload.r2Key)throw new Error("r2Key is required");if(!e.payload.telegramChatId)throw new Error("telegramChatId is required");return{r2Key:e.payload.r2Key,telegramChatId:e.payload.telegramChatId,context:e.payload.context?.trim()}}),s=await t.do("load source document from r2",async()=>{const e=await this.env.REVIEW_DOCUMENTS.get(r.r2Key);if(!e)throw new Error(`R2 object not found: ${r.r2Key}`);const t=(await e.text()).trim();if(!t)throw new Error("R2 object is empty");return t}),n=Number(this.env.MAX_REVIEW_LOOPS??"5"),o=this.env.RESPONSE_TIMEOUT??"7 days",a=async(s,i,c)=>{if(s>n)return le("workflow.loop.max_reached",{instanceId:e.instanceId,maxLoops:n}),await t.do("notify max loop reached",async()=>{await se(this.env,r.telegramChatId,`Review stopped after ${n} loops for ${e.instanceId}. Start again if you still need revisions.`)}),{approved:!1,loops:n,finalText:i};const h=t.do(`summary agent (loop ${s})`,async()=>te(this.env,"You summarize documents. Keep the output short, concrete, and factual.",ue("Summarize this text in 5 bullet points.",i,r.context)))...
```

或者，使用 `vite` 打包，这里是一个压缩后的代码片段：

```JavaScript
class ht extends pe {
  async run(e, r) {
    b("workflow.run.start", { instanceId: e.instanceId });
    const s = await r.do("validate payload", async () => {
      if (!e.payload.r2Key)
        throw new Error("r2Key is required");
      if (!e.payload.telegramChatId)
        throw new Error("telegramChatId is required");
      return {
        r2Key: e.payload.r2Key,
        telegramChatId: e.payload.telegramChatId,
        context: e.payload.context?.trim()
      };
    }), n = await r.do(
      "load source document from r2",
      async () => {
        const i = await this.env.REVIEW_DOCUMENTS.get(s.r2Key);
        if (!i)
          throw new Error(`R2 object not found: ${s.r2Key}`);
        const c = (await i.text()).trim();
        if (!c)
          throw new Error("R2 object is empty");
        return c;
      }
    ), o = Number(this.env.MAX_REVIEW_LOOPS ?? "5"), l = this.env.RESPONSE_TIMEOUT ?? "7 days", a = async (i, c, u) => {
      if (i > o)
        return H("workflow.loop.max_reached", {
          instanceId: e.instanceId,
          maxLoops: o
        }), await r.do("notify max loop reached", async () => {
          await J(
            this.env,
            s.telegramChatId,
            `Review stopped after ${o} loops for ${e.instanceId}. Start again if you still need revisions.`
          );
        }), {
          approved: !1,
          loops: o,
          finalText: c
        };
      const h = r.do(
        `summary agent (loop ${i})`,
        async () => _(
          this.env,
          et,
          K(
            "Summarize this text in 5 bullet points.",
            c,
            s.context
          )
        )
      )...
```

经过压缩的代码可能会变得相当混乱——而且根据打包工具的不同，混乱的方式也多种多样。

我们需要一种能够快速、精确解析各种形式压缩代码的方法。我们决定使用来自 **JavaScript Oxidation Compiler (OXC)** 的 `oxc-parser`，它非常适合这项工作。我们首先通过在容器中运行 Rust 来测试这个想法。每个脚本 ID 都被发送到一个 **Cloudflare Queue**，之后消息被弹出并发送到容器进行处理。一旦确认这种方法可行，我们就迁移到了一个用 Rust 编写的 **Worker**。Workers 支持通过 **WebAssembly** 运行 Rust，并且这个包足够小，使得这个过程变得直接明了。

这个 Rust Worker 负责首先将压缩的 JS 代码转换为 AST 节点类型，然后将 AST 节点类型转换为仪表板上渲染的工作流的图形版本。为此，我们为每个工作流生成一个预定义**节点类型**的图，并通过一系列节点映射将其转换为我们自己的图表示。

### 渲染图表

将工作流渲染成图表版本面临两个挑战：如何正确跟踪步骤和函数之间的关系，以及如何在覆盖所有表面的同时，尽可能简单地定义工作流节点类型。

为了保证正确跟踪步骤和函数关系，我们需要同时收集函数名和步骤名。正如我们之前讨论的，引擎只掌握步骤的信息，但一个步骤可能依赖于一个函数，反之亦然。例如，开发者可能将步骤包装在函数中，或者将函数定义为步骤。他们也可能在函数内部调用来自不同**模块**的步骤，或者重命名步骤。

尽管该库通过提供 AST 帮助我们跨过了第一道障碍，但我们仍然需要决定如何解析它。一些代码模式需要额外的创造性。例如，在 **WorkflowEntrypoint** 内部，可能存在直接调用步骤、间接调用步骤或根本不调用步骤的函数。考虑 `functionA`，它包含 `console.log(await functionB(), await functionC())`，其中 `functionB` 调用了 `step.do()`。在这种情况下，`functionA` 和 `functionB` 都应该包含在工作流程图中；然而，`functionC` 则不应该。为了捕获所有包含直接或间接步骤调用的函数，我们为每个函数创建一个子图，并检查它本身是否包含步骤调用，或者它是否调用了其他可能包含步骤调用的函数。这些子图由一个函数节点表示，该节点包含其所有相关节点。如果一个函数节点是图的叶子节点，意味着它内部没有直接或间接的工作流步骤，那么它将在最终输出中被修剪掉。

我们还会检查其他模式，包括一个静态步骤列表（我们可以从中推断工作流程图）以及以多达十种不同方式定义的变量。如果你的脚本包含多个工作流，我们会遵循与为函数创建子图类似的模式，只是抽象级别更高一层。

对于每一种 AST 节点类型，我们都必须考虑它们在工作流内部可能被使用的每一种方式：循环、分支、Promise、并行、await、箭头函数……这个列表很长。即使在这些路径中，也存在数十种可能性。仅考虑循环的几种可能方式：

```TypeScript
// for...of
for (const item of items) {
	await step.do(`process ${item}`, async () => item);
}
// while
while (shouldContinue) {
	await step.do('poll', async () => getStatus());
}
// map
await Promise.all(
	items.map((item) => step.do(`map ${item}`, async () => item)),
);
// forEach
await items.forEach(async (item) => {
	await step.do(`each ${item}`, async () => item);
});
```

除了循环，如何处理分支：

```TypeScript
// switch / case
switch (action.type) {
	case 'create':
		await step.do('handle create', async () => {});
		break;
	default:
		await step.do('handle unknown', async () => {});
		break;
}

// if / else if / else
if (status === 'pending') {
	await step.do('pending path', async () => {});
} else if (status === 'active') {
	await step.do('active path', async () => {});
} else {
	await step.do('fallback path', async () => {});
}

// 三元运算符
await (cond
	? step.do('ternary true branch', async () => {})
	: step.do('ternary false branch', async () => {}));

// 空值合并运算符，步骤在右侧
const myStepResult =
	variableThatCanBeNullUndefined ??
	(await step.do('nullish fallback step', async () => 'default'));

// try/catch with finally
try {
	await step.do('try step', async () => {});
} catch (_e) {
	await step.do('catch step', async () => {});
} finally {
	await step.do('finally step', async () => {});
}
```

我们的目标是创建一个简洁的 API，能够传达开发者需要了解的信息，同时又不过度复杂化。但是，将工作流转换为图表意味着需要考虑每一种可能的模式（无论是否遵循最佳实践）和边界情况。正如我们之前讨论的，默认情况下，每个步骤与其他步骤之间并非显式顺序执行。如果一个工作流没有使用 `await` 和 `Promise.all()`，我们假设步骤将按照它们在运行时遇到的顺序执行。但如果一个工作流包含了 `await`、`Promise` 或 `Promise.all()`，我们需要一种方法来跟踪这些关系。

我们决定跟踪执行顺序，其中每个节点都有一个 `starts:` 和 `resolves:` 字段。`starts` 和 `resolves` 索引告诉我们一个 Promise 何时开始执行，以及相对于第一个开始执行但没有立即、随后结束的 Promise，它何时结束。这与图表 UI 中的垂直定位相关（即，所有 `starts:1` 的步骤将处于同一行）。如果步骤在声明时就被 `await`，那么 `starts` 和 `resolves` 将是未定义的，工作流将按照步骤在运行时出现的顺序执行。

在解析过程中，当我们遇到一个未被 `await` 的 `Promise` 或 `Promise.all()` 时，该节点（或多个节点）会被标记一个入口编号，并体现在 `starts` 字段中。如果我们遇到对该 Promise 的 `await`，入口编号会加一，并保存为出口编号（即 `resolves` 字段的值）。这使我们能够知道哪些 Promise 同时运行，以及它们相对于彼此何时完成。

```TypeScript
export class ImplicitParallelWorkflow extends WorkflowEntrypoint<Env, Params> {
 async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
   const branchA = async () => {
     const a = step.do("task a", async () => "a"); //开始于1
     const b = step.do("task b", async () => "b"); //开始于1
     const c = await step.waitForEvent("task c", { type: "my-event", timeout: "1 hour" }); //开始于1 完成于2
     await step.do("task d", async () => JSON.stringify(c)); //开始于2 完成于3
     return Promise.all([a, b]); //完成于3
   };

   const branchB = async () => {
     const e = step.do("task e", async () => "e"); //开始于1
     const f = step.do("task f", async () => "f"); //开始于1
     return Promise.all([e, f]); //完成于2
   };

   await Promise.all([branchA(), branchB()]);

   await step.sleep("final sleep", 1000);
 }
}
```

您可以在图表中看到步骤的对齐情况：

在考虑了所有这些模式之后，我们确定了以下节点类型列表：

```Rust
| StepSleep
| StepDo
| StepWaitForEvent
| StepSleepUntil
| LoopNode
| ParallelNode
| TryNode
| BlockNode
| IfNode
| SwitchNode
| StartNode
| FunctionCall
| FunctionDef
| BreakNode;
```

以下是针对不同行为的API输出示例：

函数调用：

```JSON
{
  "functions": {
    "runLoop": {
      "name": "runLoop",
      "nodes": []
    }
  }
}
```

if条件分支到step.do：

```JSON
{
  "type": "if",
  "branches": [
    {
      "condition": "loop > maxLoops",
      "nodes": [
        {
          "type": "step_do",
          "name": "notify max loop reached",
          "config": {
            "retries": {
              "limit": 5,
              "delay": 1000,
              "backoff": "exponential"
            },
            "timeout": 10000
          },
          "nodes": []
        }
      ]
    }
  ]
}
```

包含step.do和waitForEvent的并行节点：

```JSON
{
  "type": "parallel",
  "kind": "all",
  "nodes": [
    {
      "type": "step_do",
      "name": "correctness agent (loop ${...})",
      "config": {
        "retries": {
          "limit": 5,
          "delay": 1000,
          "backoff": "exponential"
        },
        "timeout": 10000
      },
      "nodes": [],
      "starts": 1
    },
...
    {
      "type": "step_wait_for_event",
      "name": "wait for user response (loop ${...})",
      "options": {
        "event_type": "user-response",
        "timeout": "unknown"
      },
      "starts": 3,
      "resolves": 4
    }
  ]
}
```

### 下一步计划

最终，这些工作流图表的目标是成为一个全功能的调试工具。这意味着您将能够：

- 实时跟踪图中的执行过程
- 发现错误、等待人工介入审批，并为测试跳过步骤
- 在本地开发中访问可视化图表

实时跟踪图中的执行过程

发现错误、等待人工介入审批，并为测试跳过步骤

在本地开发中访问可视化图表

请在您的工作流概览页面上查看这些图表。如果您有任何功能请求或发现任何错误，请通过加入 Discord 上的 Cloudflare 开发者社区，直接向 Cloudflare 团队分享您的反馈。

---

> 本文由AI自动翻译，原文链接：[How we use Abstract Syntax Trees (ASTs) to turn Workflows code into visual diagrams](https://blog.cloudflare.com/workflow-diagrams/)
> 
> 翻译时间：2026-03-28 04:47
