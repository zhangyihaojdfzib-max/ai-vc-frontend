---
title: Cloudflare CI/CD：百万仓库的构建与部署新方案
title_original: "Run CI/CD for millions of repos â\x80\x94 on your platform, on Cloudflare"
date: '2026-08-04'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/ci-workflows/
author: ''
summary: Cloudflare 推出基于 Artifacts 和 Workflows 的 CI/CD 解决方案，支持在平台上存储、构建、测试和部署代码，可扩展至数百万仓库。通过
  CI SDK，开发者可用 TypeScript 定义管道，利用沙箱环境安全执行构建、lint、测试等步骤，并支持依赖缓存和条件部署。平台可代表客户管理 CI，客户也可自定义
  Workflow，两者可共存。该方案简化了 CI/CD 配置，提升了开发体验。
categories:
- 技术趋势
tags:
- Cloudflare
- CI/CD
- Workflows
- Artifacts
- 开发者平台
draft: false
translated_at: '2026-08-05T05:30:45.747652'
---

我们正在迈向一个可以在 Cloudflare 上完全存储、构建、测试和部署代码的世界。我们通过 **Artifacts** 构建了第一部分，这是一个可扩展到数百万仓库的版本化代码存储。

我们通过构建在 **Cloudflare Workflows** 之上的 **CI SDK**，将存储、构建和部署步骤连接在一起，这样你就可以在 Cloudflare 上运行持续集成（CI）管道。你可以通过 `wrangler` 配置文件中的新 `events` 字段，将 **artifact 推送事件** 直接发送到你的 Workflow，触发其实例执行——本质上就是一个 CI 任务。

然后，直接从安装了 `@cloudflare/ci` 的 Workflow 中，你可以：

- **自动化构建**：在安全、隔离的环境中编译来自 Artifacts 仓库的代码
- **运行 linter 和类型检查**：强制执行代码风格，捕获类型错误，并标记任何潜在问题
- **缓存依赖**：运行一次 `install`，并在 CI 任务的各个步骤之间缓存依赖
- **执行单元测试**：验证代码的每个部分是否按预期工作
- **自愈**：集成 AI 审查代理，捕获构建中失败的步骤，并推送提交进行修复
- **条件部署**：仅当构建步骤成功时，自动部署你的代码

![BLOG-3435 2.png](/images/posts/7646eb71ff13.jpg)

如今，每个人都在构建平台，无论是内部的 vibe coding 平台，还是通过代码定制扩展面向客户的产品。平台现在使用 Artifacts 上的数百万个仓库来存储他们自己的代码、客户的代码，并对两者进行版本控制。但每个团队对持续集成和部署管道都有自己的需求。对于平台来说，他们可能希望为自己代码定义的 CI 任务与为客户定义的有所不同。

许多在这些平台上构建的最终客户不想为管理自己的持续集成和持续部署（CI/CD）管道而额外头疼。相反，平台可以代表客户管理构建过程：编写一次 CI/CD 管道，并将其共享到客户正在构建的所有应用程序中。平台的一些客户可能希望定义自己的 CI；如果是这样，他们可以编写自己的 Workflow，并通过动态工作流仅在自己的仓库上运行自定义 CI 任务。妙处在于，你不必做出选择：平台管理的 CI 和自定义 CI 可以同时在同一命名空间中运行。

![BLOG-3435 3.png](/images/posts/6f92873cff46.jpg)

## CI/CD 管道就是一个 Workflow

在此之前，我们已经拥有了让平台在 Cloudflare 上连接其 CI/CD 管道的所有组件。现在，我们带来了更好的开发者体验，使其变得更加简单。

CI/CD 管道——通常使用 GitHub Actions 编排——是一系列按特定顺序运行的步骤，如果任何步骤失败，则停止运行管道并报告错误。本质上，CI/CD 管道就是一个 Workflow。CI/CD 在由 YAML 文件定义时，由于其约束条件常常导致 YAML 疲劳，很快就会变得复杂。但 CI/CD 管道中的每个步骤都可以简单地转换为 Workflow 的 `step.do()`。你可以使用 TypeScript 而不是 YAML 来定义 CI/CD 管道，以获得更大的定制性和可配置性。

我们正在推出 **CI SDK** 中的新工具，允许你在安全、隔离的环境中运行 CI 管道中的每个步骤（例如 `build`、`lint` 和 `typecheck`），这些工具直接通过 Workflows 和 **Sandbox SDK** 构建在 Cloudflare 的开发者平台上。此外，你现在可以在推送时直接启动 CI 任务，而无需配置事件订阅、队列和队列消费者。

以前，你必须直接调用 Sandbox API，并自行管理 CI 管道中不同步骤之间的状态。SDK 允许你在自己的 Workflow 步骤中运行每个沙箱命令，提供 Cloudflare Workflows 内置的重试和超时功能。

你还可以通过缓存步骤结果（例如 `install` 步骤）来加速 CI 管道，这样就不需要为所有后续操作重新安装。依赖缓存减少了 CI/CD 管道的延迟，因为每个 CI 步骤都不需要重新运行 `install`。

![BLOG-3435 4.png](/images/posts/5b56efeb423c.jpg)

要定义你的 CI 任务，你只需要：

1. 为任何依赖项（CI 任务所需的外部包或工具）定义 `install` 步骤，例如打包器（如 `esbuild`）、linter（如 `eslint`）或测试运行器（如 `vitest`）。
2. 为 CI 任务中的每个步骤指定命令（例如 `bun run build`、`bun run test`、`bun run lint`）。依赖缓存后，每个 CI 步骤可以并行执行，从而减少整体运行的延迟。
3. 在 `deploy` 步骤中传递 `wrangler deploy`。当 CI 管道通过时，你的 Worker 将自动部署。

```
const deps: CiRunnerResult = await ci.runner({
  name: 'install',
  command: 'bun install --frozen-lockfile',
  cache: { inputs: ['package.json', 'bun.lock'] },
});

await Promise.all([
  deps.runner({ name: 'lint', command: 'bun run lint' }),
  deps.runner({ name: 'test', command: 'bun run test' }),
  deps.runner({ name: 'typecheck', command: 'bun run typecheck' }),
  deps.runner({ name: 'build', command: 'bun run build' }),
]);

await deps.runner({
  name: 'deploy',
  command: 'bun wrangler deploy',
  cloudflareCredentials: {
    accountId: this.env.CLOUDFLARE_DEPLOY_ACCOUNT_ID,
  },
});
```

在 Workflow 中编写你自己的 CI 管道，你可以随心所欲地进行定制。例如，你可以从 CI Workflow 中调用一个代理，为你的 CI 任务提供自愈功能：如果构建中的某个步骤出错，代理可以自动修复，并推送提交供你审批。

![BLOG-3435 5.png](/images/posts/27b685f1edcf.jpg)

尝试使用 Project Think 的自愈 CI Workflows 示例：https://github.com/cloudflare/ci/blob/main/examples/self-healing

## 编写你自己的 CI Workflow

要编写你自己的 CI Workflow，请从 `import { CIWorkflow } from @cloudflare/ci` 开始。从一个 `install` 步骤开始：

- 下载你的依赖项，包括 CI 步骤所需的外部工具或库（例如 `vite`、`react`）。
- 指定你的 lockfile，它用于跟踪依赖项是否已更改。
- 通过沙箱快照缓存你的依赖项，以便所有后续步骤都可以访问。快照将存储在你账户的 R2 存储桶中。

```
const deps = await ci.runner({
  name: 'install',
  command: 'bun install --frozen-lockfile',
  cache: { inputs: ['package.json', 'bun.lock'] },
});
```

然后为构建和检查定义步骤，每个步骤都在其自己的安全、隔离的沙箱环境中执行。

![BLOG-3435 6.png](/images/posts/285c7fcf8060.jpg)

默认情况下，Workflow 中的每个步骤都是独立启动的，这意味着除非另有指定，否则步骤将并发执行。并行运行每个步骤可以减少 CI 运行的延迟。为了确保所有检查在 CI 管道继续之前完成（例如，在 `deploy` 步骤开始之前完成 `build`、`lint`、`test` 和 `typecheck`），请将它们包裹在 `Promise.all()` 中：

```
await Promise.all([
   deps.runner({ name: 'lint', command: 'bun run lint' }),
   deps.runner({ name: 'test', command: 'bun run test' }),
   deps.runner({ name: 'typecheck', command: 'bun run typecheck' }),
   deps.runner({ name: 'build', command: 'bun run build' }),
]);
```

现在，要实际触发你的 CI Workflow，请在 Worker 的 `wrangler` 配置中添加一个 `events` 字段，与你的 Workflow 和 Artifact 绑定一起。`events` 字段是 `triggers` 字段中支持的一个新字段。

你已经可以通过 Cloudflare Queues 的事件订阅来订阅 Artifacts，并在每次有推送事件时启动构建管道。但这需要设置事件订阅、队列、消费者和队列处理器。现在，你可以直接将该事件指向一个 Workflow——每次该事件触发时，它都会触发该 Workflow 的一个实例。

将CI工作流指定为制品推送触发器的目标，即可在每次`cf.artifacts.repo.pushed`事件发生时自动触发一个工作流实例。每次CI运行都会以工作流实例的形式呈现，您可以直接在Workflows仪表板中查看其逐步执行情况和可观测性。这是一项以Artifacts为先的集成；即将推出的类型将支持来自您Cloudflare账户中各种来源的事件，以便在整个产品套件中进行编程式消费。

如果您希望为命名空间中的每个仓库运行CI工作流——例如，如果您是一个为所有客户的仓库运行CI的平台——请省略`repoName`，仅指定`namespace`过滤器。

```
{
  "triggers": {
    "events": [
      {
        "type": "cf.artifacts.repo.pushed",
        // filter是可选的。如果您不设置repoName，我们将在您Artifacts命名空间中的任何仓库的每次推送时运行相同的工作流
        "filter": {
          "namespace": "CI",
          "repoName": "my-repo"
        },
        "target": {
          "type": "workflow",
          "workflow_name": "ci-workflow"
        }
      }
    ]
  }
}
```

要完全配置您的CI工作流，请为支撑管道的每个基础设施组件添加绑定：`artifacts`、`workflows`、`containers`和`durable_objects`（+`exports`配置）绑定（用于访问您的沙箱），以及如果您使用`cache`，还需要一个`r2`绑定。R2绑定是必需的，因为您的`install`步骤沙箱的快照存储在存储桶中。

## 自愈式CI运行

要让您的CI作业实现自愈，您需要两个组件：LLM及其Agent（智能体）框架。在上面的示例中，我们使用Workers AI包含了一个`Think` Agent（智能体），用于捕获管道中的错误并代表您运行修复。您的CI作业可以在远程运行和重新运行——无需打开笔记本电脑盯着看，也无需每隔几分钟回来检查一次。相反，Cloudflare在云端处理这一切，在容器中与CI步骤一起运行您的修复Agent（智能体）。您无需时刻盯着CI作业、手动修复并重新运行管道，只需在您的Agent（智能体）完成修复后合并提交即可。

要设置一个能自愈CI管道的Agent（智能体），请为您的Think Agent（智能体）添加一个Durable Object绑定：

```
"durable_objects": {
   "bindings": [
     {
       "name": "HEALER",
       "class_name": "Healer",
     },
   ],
 },
```

通过扩展`HealingAgent`类来创建您的Think Agent（智能体）——`Healer`，该类包含一个`heal`方法供您在失败时调用。传入您希望使用的任何模型：

```
export class Healer extends HealingAgent {
 getModel() {
   return '@cf/moonshotai/kimi-k2.7-code';
 }
}
```

然后，将您的步骤包裹在`try/catch`块中，当失败时触发修复Agent（智能体）：

```
let deps: CiRunnerResult;
try {
  // 安装一次，然后从共享和缓存的快照中运行独立的检查
  deps = await ci.runner({
    name: 'install',
    command: 'bun install --frozen-lockfile',
    cache: { inputs: ['package.json', 'bun.lock'] },
  });

  await Promise.all([
    deps.runner({ name: 'lint', command: 'bun run lint' }),
    deps.runner({ name: 'test', command: 'bun run test' }),
    deps.runner({ name: 'typecheck', command: 'bun run typecheck' }),
    deps.runner({ name: 'build', command: 'bun run build' }),
  ]);
} catch (failure) {
  // 这会捕获失败的Sandbox命令和普通的工作流错误。
  // 只有runner报告的失败才应被修复；其余错误重新抛出。
  if (!isCiRunnerFailure(failure)) {
    throw failure;
  }

  // 将错误传递给Agent（智能体），以便其进行修复
  const healed = await step.do(
    'heal',
    { retries: { limit: 0, delay: 0 }, timeout: '5 hours' },
    async () => {
      const healer = await getAgentByName(this.env.HEALER, event.instanceId);
      using result = await healer.heal({
        failure: enrichFailure({ failure, event, baseBranch }),
        prompt: '修复所有观察到的失败，且不削弱验证。',
      });
      // 报告修复分支、其提交以及所花费的步骤数。
      const { branch, commit, steps } = result;
      return { branch, commit, steps };
    }
  );

  // 源运行保持失败状态；其已验证的修复位于另一个分支上
  throw new CiRunFailedWithFix(failure, healed);
}

await deps.runner({
  name: 'deploy',
  command: 'bun wrangler deploy',
});
```

此示例演示了一个自愈式CI管道，但实际上，自带工作流（BYO-W）模型允许您以任何方式自定义CI作业。这可以成为添加安全规则、过滤器或条件CI步骤的地方。使用BYO-W模型，平台可以根据每个单独的使用场景，跨不同团队、客户或应用配置其CI/CD管道。

## 使用工作流的好处

通过在Cloudflare Workflow上运行您的CI管道，您将自动获得：

1. **弹性重试（持久化执行）**：如果CI作业中的任何步骤失败，它将自动重试并保持状态持久化，这意味着不会丢失任何进度。每个步骤都支持自定义重试和超时行为，因此您可以为每个步骤定义不同的失败逻辑。此外，您可以从特定步骤重新启动，例如，如果只有lint失败，您不必重新运行整个CI管道。
2. **工作流可观测性**：在Workflows仪表板中逐步检查您的CI作业，每个实例都会显示步骤及其输入、输出以及墙钟时间和CPU时间。您可以通过仪表板中的Workflows图表可视化您的CI作业，轻松查看哪些步骤是并发运行还是顺序运行。您还可以通过Workers Observability和GraphQL检查Workflows日志，以更深入地了解CI作业的运行情况。
3. **代码的力量**：通过在工作流中运行CI，您可以为任何需求编写步骤。例如，您可能希望在CI/CD管道中运行AI代码审查器。您可以通过Workflows的`step.do()`调用您的代码审查Agent（智能体）——或处理任何可以编码的自定义逻辑。其他示例可能包括将构建产物写入R2，以及在CI失败、完成或合并到主分支时发送电子邮件。

## 下一步

CI/CD管道只是一个工作流——借助CI SDK，您可以用简单的TypeScript而非僵化的YAML来定义您自己以及您客户的代码中的CI。基于Cloudflare Workflows原语，您可以定义任何您想要的逻辑，无论是像我们的Think示例那样的修复Agent（智能体），还是将构建产物写入R2。在Workflows上运行CI有助于弥合存储（通过Artifacts）、构建和部署之间的差距。作为一个平台，这使您能够轻松管理自己代码上的每一步，并代表您的客户进行管理。

申请加入Artifacts私有测试版，并通过我们的Workflows CI指南开始使用。如果您有任何功能请求或发现任何错误，请通过加入Cloudflare开发者Discord社区直接与Cloudflare团队分享您的反馈。

接下来即将推出：

1. **Workers和Workers for Platforms的直接集成**：`build.preview()`和`build.deploy()`原语，用于在推送到主分支时自动部署，并在推送到非默认分支时创建预览
2. **渐进式部署**：通过Workflows管理基于百分比的发布，以自定义您的部署进度和回滚逻辑
3. **Monorepos**：使用单个CI管道简化多Worker部署的管理
4. **触发器**：从不同来源发送推送事件，以从任何版本控制系统（不仅仅是Artifacts）对仓库运行CI作业

## 相关标签

在社交媒体上关注

- Cloudflare

## 订阅以接收新文章通知

我们绝不会分享您的电子邮件地址。

感谢订阅！请检查您的收件箱以确认。

---

> 本文由AI自动翻译，原文链接：[Run CI/CD for millions of repos â on your platform, on Cloudflare](https://blog.cloudflare.com/ci-workflows/)
> 
> 翻译时间：2026-08-05 05:30
