---
title: Cloudflare推出Agent开发生命周期，重塑软件工厂
title_original: The Agent Development Lifecycle has arrived on Cloudflare
date: '2026-08-04'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/agent-development-lifecycle/
author: ''
summary: Cloudflare宣布推出Agent开发生命周期（ADLC），以取代传统SDLC，应对AI时代软件开发的挑战。文章指出，AI使代码实现变得快速廉价，但下游环节如测试、部署、维护等仍依赖人工，导致瓶颈。为此，Cloudflare发布了一系列工具，包括@cloudflare/ci、本地OpenTelemetry追踪、Cloudflare
  Agents等，让Agent能自主完成更多SDLC任务。其核心理念是构建可编程、可水平扩展、可复现的软件工厂，将人类从繁琐流程中解放，专注于创意与决策。
categories:
- 技术趋势
tags:
- Agent开发生命周期
- Cloudflare
- 软件工厂
- AI开发工具
- SDLC
draft: false
translated_at: '2026-08-05T05:30:44.591439'
---

工程经理们过去几十年一直在想办法让众多程序员在共享代码库上协同工作。这项工作可以追溯到“系统开发生命周期”（兰德公司，1975年）——如今通常被称为“软件开发生命周期”（SDLC），它定义了以下阶段：

- 规划
- 设计
- 实现
- 测试
- 部署
- 维护
- 退役

AI让原本最慢、最昂贵的步骤——实现——变成了最快、最便宜的步骤。这反过来又对下游产生了影响：让负责SDLC中所有其他步骤的人不堪重负。从被成千上万个拉取请求和问题淹没的开源维护者，到在软件交付速度呈数量级增长时拼命维持生产系统不崩溃的生产工程师，无一幸免。

我们都在努力保护我们的系统、我们的客户和我们自己免受“垃圾产出”的困扰。

![image1.png](/images/posts/05b71119432c.jpg)

答案——矛盾的是——是赋予Agent（智能体）更多权力。这才公平！你绝不会让你团队里的工程师写代码，然后指望别人去验证、合并、部署、在生产环境值守，并分类处理进来的bug。但大多数公司现在对Agent（智能体）就是这么做的。模型已经有了显著改进，Agent（智能体）运行的时间跨度更长，能够承担更大的任务。但它们尚未在SDLC的各个阶段得到均衡使用。

Cloudflare把Agent（智能体）当作我们的客户。它们可以购买域名、创建临时账户并使用整个Cloudflare API。我们知道，Agent（智能体）需要API和工具才能代表我们的客户管理完整的SDLC——而不仅仅是它的起点。

因此，今天我们推出了一系列新工具的开端，让Agent（智能体）能够超越单纯的代码生成，承担更多SDLC的工作。我们分享我们为解决自身问题而构建的东西和学到的经验：

- @cloudflare/ci——一种在数百万个代码仓库中运行CI/CD的新方式，可以自愈并生成Agent（智能体）来执行更复杂的任务，构建在Cloudflare Workflows之上。
- 本地开发中的OpenTelemetry追踪——让Agent（智能体）获得与生产环境相同的可观测性，内置于Wrangler和Cloudflare Vite插件中。
- 隆重推出：Cloudflare Agents和Agent Traces——一个围绕Agent（智能体）的OpenTelemetry追踪来观察、维护和改进Agent（智能体）的新家园。
- Cloudflare如何利用AI强制执行工程标准——我们在所有产品和系统的代码仓库及规范中强制执行最佳实践的经验。
- 我们如何构建软件工厂将Astro的GitHub问题数量降为零——我们为大型且不断增长的开源项目构建自动分类、复现、验证和修复问题的系统的经验。

不过，这里还有更大的图景。当我们审视SDLC时，即使有最好的自动化，它的假设也无法适应Agent（智能体）能编写的代码量以及软件团队为了竞争所必须保持的速度。我们认为，是时候用ADLC——Agent开发生命周期——来取代SDLC了。

## SDLC是为软件团队设计的。ADLC是为软件工厂设计的。

现在，每个人都在谈论构建“软件工厂”——即由Agent（智能体）驱动的系统，接收输入并自主构建、改进、部署和管理软件。接受一个输入，无论是生产错误、客户的bug报告，还是新功能的想法，然后将其完全委托给一个Agent（智能体）。

即使有了Agent（智能体），大多数软件项目仍然受到人工介入步骤的制约。人类提示Agent（智能体），告诉它们继续，指示它们应用代码审查中的反馈，不断照看多个Agent（智能体）并给它们下达指令。在大多数软件团队中，人类仍然管理着SDLC模型中的每一步——唯一的变化是他们将每个步骤内的任务委托给了Agent（智能体）。

因此，软件工厂背后的梦想是：如果你重新构想这种方法，为构建软件的整个流程建造一座工厂会怎样？我们如何将更多人类时间转移到真正需要人类灵感、品味和判断力的事情上？这将为我们留出更多时间来设计、与客户交谈，以及拥有更大的梦想。

软件工厂必须管理SDLC中相同的步骤，但它对构建其上的平台提出了更高的要求。因为当你交出钥匙让Agent（智能体）驾驶时，每一个以前依赖人工的手动步骤都必须适应为：

- 可编程的——“点击操作”对人类来说已经是坏实践，但对Agent（智能体）来说根本行不通。每一个操作都需要Agent（智能体）可以调用、调试和依赖的API。
- 可水平扩展的——预览部署在人类构建时盯着屏幕或手动接管预发布服务器以在生产环境之前发现问题时是锦上添花。要让Agent（智能体）驱动，每个Agent（智能体）都必须拥有与生产环境匹配的自己的预览环境。
- 可复现的——如果有一个bug只能在iPhone 15上模拟4G网络时才能复现怎么办？或者只能从某个国家的IP访问时才能复现？典型的单元测试和集成测试工具在这里帮不上忙。
- 实时的、基于推送的——依赖人类查看正确的仪表盘来判断系统是否正常一直是个糟糕的方法，但这对Agent（智能体）来说完全行不通。你需要一个事件来触发Agent（智能体）去执行工作。
- 原子性的——每个变更都需要可独立测试、可发布、可观察和可回滚，而不影响无关的行为。
- 有权限控制的——你知道你可能不应该这样做，但今天你会给几个信任的工程师SSH进入生产环境的权限，以防万一真的出了大问题。你绝不可能让一个Agent（智能体）这么做——但如果没有升级和获取更多权限的能力，它怎么能做好自己的工作呢？
- 自我改进的——人类从经验中学习。第一周上线或第一次值班轮换时，人类很慢，需要跟着别人学习，但之后会变得更好更快。Agent（智能体）也需要从经验中学习的方法。

如果我们想让软件工厂对真实的生产软件安全可用，我们需要新的东西。软件工厂面临着与自动驾驶汽车等其他自主系统相同的挑战——从80%的成功率，跨越到超过99%的“几个九”的可靠性。

## 要让Agent（智能体）掌握SDLC的方向盘，你不能给它们一辆为人类设计的车

自动驾驶汽车装载了普通汽车没有的传感器和技术。激光雷达传感器、摄像头、用于运行推理的强大计算能力，以及连接到可以在需要时远程接管的中央指挥系统。

要让自动驾驶汽车达到人类驾驶水平的80%，我们可能不需要所有这些。自动驾驶在10年前就达到了大约人类水平80%的程度。但这不是要跨越的标准——标准是要比人类驾驶员更好、更安全。这就是当我们把钥匙交给机器时所期望的，以便在101号公路上以60英里/小时的速度行驶时能安心打个盹。这就是为什么自动驾驶汽车拥有专为自动驾驶而设计的技术——正是这些技术建立了信任，并处理了那些无法预先设计的边缘情况。

自动驾驶软件也是如此。问问自己——为什么你还没有让你的Agent（智能体）自动批准并合并它自己的拉取请求到你的生产服务中？你构建的东西风险越高，你的理由清单几乎肯定就越长。

当你开始深入剖析这个过程中不仅可能出现的各种灾难性错误，还包括为客户构建正确产品所必需的一切时，你会发现其复杂程度非同一般。它无法被简单地塞进GitHub Actions YAML文件中的一系列线性步骤里，也远远超出了运行传统自动化测试的范畴。即便是对仪表盘的一个微小改动，也可能跨越多个角色、专业领域和组织架构，而主观性的变更恰恰是最难测试和最难委派的。今天，这些事项中的大多数可能根本不在你的CI/CD流水线中。但如果你希望在将全部控制权交给运行软件工厂的Agent的同时，这些事项仍能顺利完成，那么它们就必须被纳入其中。

为了让Agent能够驱动整个流程，我们需要一种更好的方式来编排这些动态的步骤序列。我们认为，这就是Workflow，它具备生成容器、Agent和浏览器的能力。一个Workflow可以设置特性开关并为测试用户启用它们，调查日志和追踪信息，在变更逐步推出时观察生产指标，并执行安全交付所需的一切其他操作。

## CI/CD流水线只是一个Workflow。但Workflow的潜力远不止于CI/CD流水线。

Cloudflare Workflows允许你将多个步骤串联起来，自动重试失败的任务，并将状态持久化数分钟、数小时甚至数周。它们旨在将复杂且动态的业务流程编码为逻辑清晰、易于理解的程序。这篇博客文章将阐述为什么Workflows与Artifacts相结合，能够从根本上简化CI/CD流水线的定义和触发。例如：

```javascript
import { CIWorkflow } from `@cloudflare/ci`

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

然而，Workflows并不仅限于一系列线性步骤。它们可以被动态定义，并且可以生成Agent或其他Workflows。这个示例展示了一个Workflow，它审查过去一天的新数据。该Workflow完全控制Agent被提示的时间和方式，并能在步骤之间传递上下文：

```javascript
import { WorkflowEntrypoint, type WorkflowEvent, type WorkflowStep } from 'cloudflare:workers';
import { init } from '@flue/runtime';
import { Reviewer } from './agents/reviewer.ts';
import { collectFindings } from './shared/nightly.ts';

type Params = { date: string };

export class NightlyReview extends WorkflowEntrypoint {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    const findings = await step.do('collect findings', () => collectFindings(event.payload.date));

    const agent = init(Reviewer, { id: `nightly-${event.payload.date}` });

    const receipt = await step.do('dispatch review', () =>
      agent.dispatch(`Review these findings:\n${findings}`),
    );

    const review = await step.do('read review', async () => {
      const reply = await agent.read(receipt);
      return { text: reply.text, data: reply.data };
    });

    // ...
  }
}
```

一旦你看到了这种模式，并且像Cloudflare一样“深谙Workflow之道”，你就会开始思考：我还能让Workflow为我处理哪些其他事情？还有哪些受制于人工瓶颈的步骤，我可以委托给Workflow + Flue agents这个组合来完成？

## 完整的ADLC，构建于Cloudflare技术栈之上

凭借Workflows编排复杂步骤的能力，以及Artifacts作为代码的存储层，当你审视SDLC的各个阶段时，你会发现，Agent在Cloudflare上拥有掌控软件构建、交付和维护全流程所需的一切：

## 构建你的软件工厂的基元

当下，处于技术前沿的人们正在构建未来的软件工厂。最终，软件工厂将像Agent和AI一样，成为人们构建软件的常态方式。但对于大多数人和大多数组织而言，我们尚未达到那个阶段。

我们希望改变这一现状。

为此，我们一直在思考的问题是：我们如何让一切变得简单易用，让互联网上的每个人都能从这样的范式转变中受益？我们能够向所有人——从最小的初创公司到全球最大的平台——开放哪些基础层的基元？

在这种情况下，我们认为基元已经就绪。要将它们连接起来，并持续构建我们自己的软件工厂并从中学习，还有更多工作要做。但就在今天，我们已经准备好，让你在Cloudflare上构建你的“制造机器的机器”。从@cloudflare/ci开始，构建一个Agent，看看你能让SDLC的多少环节实现自动化。

## 相关标签

关注社交媒体

- Cloudflare
- Brendan Irvine-Broque

## 订阅以接收新文章通知

我们绝不会分享您的电子邮件地址。

感谢订阅！请查看您的收件箱以确认。

---

> 本文由AI自动翻译，原文链接：[The Agent Development Lifecycle has arrived on Cloudflare](https://blog.cloudflare.com/agent-development-lifecycle/)
> 
> 翻译时间：2026-08-05 05:30
