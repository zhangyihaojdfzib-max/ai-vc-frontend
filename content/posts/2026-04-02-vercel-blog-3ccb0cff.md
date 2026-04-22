---
title: Workflow SDK 支持自定义类序列化，提升开发体验
title_original: Custom Class Serialization in Workflow SDK - Vercel – Vercel
date: '2026-04-02'
source: Vercel Blog
source_url: https://vercel.com/changelog/workflow-custom-class-serialization
author: ''
summary: Vercel 的 Workflow SDK 现已通过新的 `@workflow/serde` 包支持自定义类序列化功能。此前，SDK 仅支持标准
  JavaScript 类型的序列化，无法在工作流和步骤函数间传递自定义类的实例。现在，开发者只需在自定义类中实现 `WORKFLOW_SERIALIZE` 和
  `WORKFLOW_DESERIALIZE` 两个静态方法，即可定义类的序列化与反序列化逻辑。文章以 `@vercel/sandbox` 中的 `Sandbox`
  类为例，展示了如何实现该功能，从而允许将复杂的类实例作为参数或返回值在工作流中无缝传递，极大提升了开发效率和代码的可维护性。
categories:
- AI基础设施
tags:
- Workflow SDK
- 序列化
- Vercel
- 开发者工具
- JavaScript
draft: false
translated_at: '2026-04-22T05:05:51.218380'
---

Workflow SDK 现已支持自定义类序列化，允许您在工作流和步骤函数之间传递自定义类的实例。

Workflow SDK 支持序列化标准 JavaScript 类型，如基本类型、对象、数组、Date、Map、Set 等。此前不支持自定义类实例，因为序列化系统不知道如何重建它们。借助新的 `@workflow/serde` 包，您可以通过使用 `WORKFLOW_SERIALIZE` 和 `WORKFLOW_DESERIALIZE` 实现两个静态方法，来定义类的序列化与反序列化方式。

以下是我们如何在 `@vercel/sandbox` 中使用自定义序列化来极大提升开发者体验的示例：

```
1import { WORKFLOW_SERIALIZE, WORKFLOW_DESERIALIZE } from "@workflow/serde";2
3interface SerializedSandbox {4  metadata: SandboxSnapshot;5  routes: SandboxRouteData[];6}7
8export class Sandbox {9  sandbox: SandboxSnapshot;10  routes: SandboxRouteData[];11
12  13  static [WORKFLOW_SERIALIZE](instance: Sandbox): SerializedSandbox {14    return {15      metadata: instance.sandbox,16      routes: instance.routes,17    };18  }19
20  21  static [WORKFLOW_DESERIALIZE](data: SerializedSandbox): Sandbox {22    return new Sandbox({23      sandbox: data.metadata,24      routes: data.routes,25    });26  }27
28  29  30  async runCommand(31    commandOrParams: string | RunCommandParams,32    args?: string[],33    opts?: { signal?: AbortSignal },34  ): Promise<Command | CommandFinished> {35    "use step";36    37  }38}
```

`@vercel/sandbox` 如何实现工作流自定义类序列化的示例

实现后，您的类的实例可以作为参数在工作流和步骤函数之间传递，也可以作为返回值，序列化系统会自动处理转换。

```
1export async function runCode(prompt: string) {2  "use workflow";3
4  5  6  7  const sandbox = await Sandbox.create({8    resources: { vcpus: 1 },9    timeout: 5 * 60 * 1000,10    runtime: "node22",11  });12
13  14  15  16  17  const code = 'console.log("Hello World")';18  await sandbox.writeFiles([{ path: "script.js", content: code }]);19
20  const finished = await sandbox.runCommand("node", ["script.js"]);21
22  23}
```

在 Workflow DevKit 中使用序列化 `Sandbox` 类的示例用法

- 查看完整示例应用，它利用了 `@vercel/sandbox` 和 Workflow SDK。
- 阅读序列化文档以了解更多信息。

查看完整示例应用，它利用了 `@vercel/sandbox` 和 Workflow SDK。

阅读序列化文档以了解更多信息。

---

> 本文由AI自动翻译，原文链接：[Custom Class Serialization in Workflow SDK - Vercel – Vercel](https://vercel.com/changelog/workflow-custom-class-serialization)
> 
> 翻译时间：2026-04-22 05:05
