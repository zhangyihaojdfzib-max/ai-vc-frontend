---
title: Python Workers升级：极速冷启动、包支持与uv优先工作流
title_original: 'Python Workers redux: fast cold starts, packages, and a uv-first
  workflow'
date: '2025-12-08'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/python-workers-advancements/
author: Dominik Picheta
summary: 本文介绍了Cloudflare Python Workers的最新改进，重点包括通过内存快照技术实现远超AWS Lambda和Google Cloud
  Run的冷启动速度，支持Pyodide运行时下的广泛Python包生态，并围绕uv工具构建了简化的开发部署流程。文章展示了如何在两分钟内全球部署FastAPI应用，阐述了Python
  Workers在无服务器场景下的性能优势与免费套餐详情，为开发者提供了高效、可扩展的边缘计算解决方案。
categories:
- AI基础设施
tags:
- Python
- 无服务器计算
- Cloudflare Workers
- 冷启动优化
- 边缘计算
draft: false
translated_at: '2026-01-05T17:24:35.265Z'
---

注：本文已更新，补充了关于 AWS Lambda 的详细信息。
去年，我们宣布了对 Python Workers 的基础支持，允许 Python 开发者通过一条命令将 Python 代码部署到全球各地，并利用 Workers 平台的优势。

自那时起，我们一直致力于提升 Workers 上的 Python 开发体验。我们专注于为平台带来包支持，这一目标现已实现——它拥有极快的冷启动速度，并提供原生的 Python 开发体验。

这意味着将包集成到 Python Worker 中的方式发生了变化。我们不再提供有限的预置包集合，而是支持 Pyodide（为 Python Workers 提供支持的 WebAssembly 运行时）所支持的任何包。这包括所有纯 Python 包，以及许多依赖动态库的包。我们还围绕 `uv` 构建了工具，使包安装变得简单。

我们还实现了专用的内存快照以减少冷启动时间。与其他无服务器 Python 供应商相比，这些快照带来了显著的性能提升。在使用常见包的冷启动测试中，Cloudflare Workers 的启动速度比未启用 SnapStart 的 AWS Lambda 快 2.4 倍以上，比 Google Cloud Run 快 3 倍。

在这篇博客文章中，我们将解释 Python Workers 的独特之处，并分享我们如何实现上述成果的一些技术细节。但首先，对于那些可能不熟悉 Workers 或无服务器平台——尤其是来自 Python 背景的开发者——让我们分享一下您可能想要使用 Workers 的原因。

**2 分钟内将 Python 部署到全球**
Workers 的魅力之一在于代码简单且易于全球部署。让我们首先展示如何在不到两分钟的时间内，在全球范围内部署一个具有快速冷启动的 FastAPI 应用。

使用 FastAPI 实现一个简单的 Worker 只需几行代码：

```python
from fastapi import FastAPI
from workers import WorkerEntrypoint
import asgi

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is FastAPI on Workers"}

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        return await asgi.fetch(app, request.js_object, self.env)
```

要部署类似的应用，只需确保您已安装 `uv` 和 `npm`，然后运行以下命令：

```bash
$ uv tool install workers-py
$ pywrangler init --template \
https://github.com/cloudflare/python-workers-examples/03-fastapi
$ pywrangler deploy
```

只需少量代码和一条 `pywrangler deploy` 命令，您的应用现已部署到覆盖 125 个国家/地区、330 个位置的 Cloudflare 边缘网络。无需担心基础设施或扩展问题。

对于许多用例，Python Workers 是完全免费的。我们的免费套餐每天提供 100,000 次请求和每次调用 10 毫秒的 CPU 时间。更多信息，请查看我们文档中的定价页面。

更多示例，请查看 GitHub 上的代码仓库。继续阅读以了解更多关于 Python Workers 的信息。

**那么，您能用 Python Workers 做什么？**
现在您有了一个 Worker，几乎任何事情都是可能的。您编写代码，所以由您决定。您的 Python Worker 接收 HTTP 请求，并且可以向公共互联网上的任何服务器发出请求。

您可以设置 cron 触发器，让您的 Worker 按计划定期运行。此外，如果您有更复杂的需求，可以利用 Python Workers 的 Workflows，甚至使用 Durable Objects 来运行长连接的 WebSocket 服务器和客户端。

以下是您可以使用 Python Workers 完成的更多示例：

**更快的包冷启动**
像 Workers 这样的无服务器平台通过仅在必要时运行您的代码来为您节省成本。这意味着如果您的 Worker 没有收到请求，它可能会被关闭，并在新请求到来时需要重新启动。这通常会产生我们称之为“冷启动”的资源开销。尽可能缩短冷启动时间对于最小化最终用户的延迟非常重要。

在标准 Python 中，启动运行时的开销很大，我们最初实现 Python Workers 时专注于让运行时快速启动。然而，我们很快意识到这还不够。即使 Python 运行时启动很快，在实际场景中，初始启动通常包括从包中加载模块，不幸的是，在 Python 中，许多流行的包可能需要几秒钟才能加载。

我们着手让冷启动变得快速，无论是否加载了包。

为了衡量真实的冷启动性能，我们建立了一个基准测试，导入常见包，以及一个使用裸 Python 运行时运行“hello world”的基准测试。标准 Lambda 能够快速启动运行时，但一旦需要导入包，冷启动时间就会急剧上升。为了优化带包的冷启动速度，您可以在 Lambda 上使用 SnapStart（我们很快会将其添加到链接的基准测试中）。这会产生存储快照的成本以及每次恢复的额外成本。Python Workers 将自动为每个 Python Worker 免费应用内存快照。

以下是加载三个常见包（`httpx`、`fastapi` 和 `pydantic`）时的平均冷启动时间：

| 平台 | 平均冷启动时间（秒） |
| :--- | :--- |
| Cloudflare Python Workers | 1.027 |
| AWS Lambda（无 SnapStart） | 2.502 |
| Google Cloud Run | 3.069 |

在这种情况下，Cloudflare Python Workers 的冷启动速度比未启用 SnapStart 的 AWS Lambda 快 2.4 倍，比 Google Cloud Run 快 3 倍。我们通过使用内存快照实现了这些低冷启动时间，在后面的部分中我们将解释我们是如何做到的。

我们定期运行这些基准测试。请访问此处获取最新数据以及我们测试方法的更多信息。

我们在架构上与其他平台不同——即，Workers 是基于隔离的。因此，我们的目标很高，我们正在规划一个零冷启动的未来。

**包支持**
多样化的包生态系统是 Python 如此出色的重要原因。这就是为什么我们一直努力确保在 Workers 中使用包尽可能简单。

我们意识到，与现有的 Python 工具链配合使用是实现出色开发体验的最佳途径。因此我们选择了 `uv` 包和项目管理器，因为它快速、成熟，并且在 Python 生态系统中势头正劲。

我们围绕 `uv` 构建了自己的工具，称为 `pywrangler`。这个工具主要执行以下操作：

`Pywrangler` 调用 `uv` 以兼容 Python Workers 的方式安装依赖项，并在本地开发或部署 Workers 时调用 `wrangler`。

实际上，这意味着您只需运行 `pywrangler dev` 和 `pywrangler deploy` 即可在本地测试您的 Worker 并部署它。

您可以使用 `pywrangler types` 为 `wrangler` 配置中定义的所有绑定生成类型提示。这些类型提示适用于 Pylance 或较新版本的 mypy。

为了生成类型，我们使用 `wrangler types` 创建 TypeScript 类型提示，然后使用 TypeScript 编译器为这些类型生成抽象语法树。最后，我们利用 TypeScript 提示（例如 JS 对象是否具有迭代器字段）来生成适用于 Pyodide 外部函数接口的 mypy 类型提示。

**使用快照减少冷启动时间**
Python 启动通常相当慢，导入 Python 模块可能触发大量工作。我们通过使用内存快照来避免在冷启动期间运行 Python 启动过程。

当 Worker 部署时，我们执行 Worker 的顶层作用域代码，然后获取内存快照并将其与您的 Worker 一起存储。每当为 Worker 启动一个新的隔离环境时，我们恢复内存快照，Worker 就准备好处理请求，无需执行任何 Python 代码进行准备。这显著改善了冷启动时间。例如，导入 `fastapi`、`httpx` 和 `pydantic` 的 Worker 在没有快照的情况下启动大约需要 10 秒。

使用快照，只需1秒。
这得益于Pyodide基于WebAssembly构建的特性。我们可以轻松捕获运行时的完整线性内存并恢复它。

**内存快照与熵**
WebAssembly运行时不需要地址空间布局随机化等安全特性，因此现代操作系统中内存快照的大多数难题不会出现。与原生内存快照类似，我们仍需在启动时谨慎处理熵，以避免使用XKCD随机数生成器（我们非常注重真正的随机性）。
通过快照保存内存，我们可能会无意中锁定随机性的种子值。在这种情况下，未来对“随机”数的多次调用将始终返回相同的数值序列。

避免这种情况尤其具有挑战性，因为Python在启动时使用了大量熵。这包括libc函数`getentropy()`和`getrandom()`，以及从`/dev/random`和`/dev/urandom`读取数据。所有这些函数在底层都共享相同的实现，即JavaScript的`crypto.getRandomValues()`函数。

在Cloudflare Workers中，`crypto.getRandomValues()`在启动时始终被禁用，以便我们未来能够切换到使用内存快照。不幸的是，Python解释器不调用此函数就无法启动。而且许多包在启动时也需要熵。这些熵主要有两个用途：
1.  我们在启动时进行哈希随机化，并接受每个特定Worker具有固定哈希种子的代价。Python没有机制允许在启动后替换哈希种子。
2.  对于伪随机数生成器，我们采取以下方法：
    *   **部署时**：
        1.  使用固定的“毒化种子”初始化PRNG，然后记录PRNG状态。
        2.  将所有调用PRNG的API替换为一个覆盖层，该覆盖层会因用户错误而中止部署。
        3.  执行用户代码的顶层作用域。
        4.  捕获快照。
    *   **运行时**：
        1.  断言PRNG状态未改变。如果改变，说明我们忘记为某些方法添加覆盖层。因内部错误中止部署。
        2.  恢复快照后，在执行任何处理程序之前，重新为随机数生成器设定种子。

通过这种方式，我们可以确保Worker在运行时可以使用PRNG，但阻止它们在初始化和预快照阶段使用PRNG。

**内存快照与WebAssembly状态**
在WebAssembly上创建内存快照时，还有一个额外的困难：我们保存的内存快照仅包含WebAssembly线性内存，但Pyodide WebAssembly实例的完整状态并不包含在线性内存中。

在线性内存之外，还有两个表。
一个表存储函数指针的值。传统计算机使用“冯·诺依曼”架构，这意味着代码与数据存在于同一内存空间，因此调用函数指针就是跳转到某个内存地址。WebAssembly采用“哈佛架构”，代码位于独立的地址空间。这是WebAssembly大多数安全保证的关键，特别是为什么WebAssembly不需要地址空间布局随机化。WebAssembly中的函数指针是函数指针表的一个索引。
第二个表存储所有从Python引用的JavaScript对象。JavaScript对象不能直接存储到内存中，因为JavaScript虚拟机禁止直接获取指向JavaScript对象的指针。相反，它们被存储在一个表中，并在WebAssembly中表示为该表的索引。

我们需要确保在恢复快照后，这两个表的状态与捕获快照时的状态完全相同。

函数指针表在WebAssembly实例初始化时始终处于相同状态，并在我们加载动态库（如`numpy`等原生Python包）时由动态加载器更新。
为了处理动态加载：
*   在获取快照时，我们修补加载器以记录动态库的加载顺序、每个库的元数据在内存中的分配地址以及用于重定位的函数指针表基地址。
*   在恢复快照时，我们按相同顺序重新加载动态库，并使用修补的内存分配器将元数据放置到相同位置。我们断言当前函数指针表的大小与为动态库记录的函数指针表基地址匹配。

所有这些确保了在恢复快照后，每个函数指针的含义与获取快照时相同。

为了处理JavaScript引用，我们实现了一个相当有限的系统。如果一个JavaScript对象可以通过一系列属性访问从`globalThis`访问到，我们就记录这些属性访问路径，并在恢复快照时重放它们。如果存在任何无法通过这种方式访问的JavaScript对象的引用，我们将中止Worker的部署。这对于处理所有现有支持Pyodide的Python包来说已经足够好，这些包进行顶层导入，例如：
```python
from js import fetch
```

**使用分片减少冷启动频率**
我们Python Workers性能策略的另一个重要特征是分片。关于其实现细节，这里有非常详细的描述。简而言之，我们现在将请求路由到现有的Worker实例，而之前我们可能会选择启动一个新实例。

分片实际上首先在Python Workers中启用，并证明是其一个极佳的测试平台。Python中的冷启动成本远高于JavaScript，因此确保请求被路由到已运行的隔离实例尤为重要。

**未来展望**
这仅仅是个开始。我们有很多计划来改进Python Workers：
*   更友好的开发者工具
*   利用我们的隔离架构实现更快的冷启动
*   支持更多包
*   支持原生TCP套接字、原生WebSocket以及更多绑定

要了解更多关于Python Workers的信息，请查看[此处](https://developers.cloudflare.com/workers/languages/python/)的文档。如需帮助，请务必加入我们的[Discord](https://discord.cloudflare.com/)。


> 本文由AI自动翻译，原文链接：[Python Workers redux: fast cold starts, packages, and a uv-first workflow](https://blog.cloudflare.com/python-workers-advancements/)
> 
> 翻译时间：2026-01-05 17:24
