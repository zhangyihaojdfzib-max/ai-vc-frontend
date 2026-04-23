---
title: 提升Rust Workers可靠性：wasm-bindgen的panic与abort恢复机制
title_original: "Making Rust Workers reliable: panic and abort recovery in wasmâ\x80\
  \x91bindgen"
date: '2026-04-22'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/making-rust-workers-reliable/
author: ''
summary: 本文介绍了Cloudflare团队如何解决Rust Workers在WebAssembly中因panic或abort导致的沙箱污染问题。通过向wasm-bindgen项目贡献代码，实现了全面的Wasm错误恢复机制。首先支持`panic=unwind`，确保单个请求失败不影响其他请求；其次建立abort恢复机制，保证Wasm上的Rust代码在abort后不会再次执行。这些改进显著提升了Rust
  Workers在生产环境中的可靠性和状态保持能力。
categories:
- 技术趋势
tags:
- Rust
- WebAssembly
- wasm-bindgen
- Cloudflare Workers
- 错误恢复
draft: false
translated_at: '2026-04-23T05:04:51.280727'
---

# 让 Rust Workers 更可靠：wasm-bindgen 中的 panic 与 abort 恢复

2026-04-22

- Guy Bedford
- Hood Chatham
- Logan Gatlin

![](/images/posts/8e4386400eb2.png)

Rust Workers 通过将 Rust 编译为 WebAssembly 来在 Cloudflare Workers 平台上运行，但正如我们所发现的，WebAssembly 存在一些棘手的问题。当发生 panic 或意外 abort 时，运行时可能会处于未定义状态。对于 Rust Workers 的用户来说，panic 在历史上是致命的，它会污染实例，甚至可能在一段时间内导致 Worker 无法工作。

虽然我们能够检测并缓解这些问题，但 Rust Worker 仍有很小的可能性会意外失败，并导致其他请求也随之失败。Worker 中一个未处理的 Rust abort 影响单个请求，可能会升级为影响其他并行请求的更广泛故障，甚至继续影响新传入的请求。其根本原因在于 wasm-bindgen——这个生成 Rust Workers 所依赖的 Rust 到 JavaScript 绑定的核心项目——缺乏内置的恢复语义。

在本文中，我们将分享最新版本的 Rust Workers 如何处理全面的 Wasm 错误恢复，从而解决这种由 abort 引起的沙箱污染问题。这项工作已作为我们去年成立的 wasm-bindgen 组织内合作的一部分，贡献回 wasm-bindgen 项目中。首先是支持 `panic=unwind`，确保单个失败的请求永远不会污染其他请求；然后是 abort 恢复机制，保证 Wasm 上的 Rust 代码在 abort 后绝不可能再次执行。

## 初步的恢复缓解措施

我们最初尝试解决此领域的可靠性问题，重点是理解和控制在生产环境 Rust Workers 中由 Rust panic 和 abort 引起的故障。我们引入了一个自定义的 Rust panic 处理器，它在 Worker 内部跟踪故障状态，并在处理后续请求前触发完整的应用程序重新初始化。在 JavaScript 端，这需要使用基于 Proxy 的间接层来包装 Rust-JavaScript 调用边界，以确保所有入口点都被一致地封装。我们还对生成的绑定进行了针对性修改，以便在故障后正确重新初始化 WebAssembly 模块。

虽然这种方法依赖于自定义的 JavaScript 逻辑，但它证明了可靠的恢复是可以实现的，并消除了我们在实践中看到的持久性故障模式。该解决方案从 0.6 版本开始默认提供给所有 workers-rs 用户，并为后续章节中描述的更通用、已上游化的 abort 恢复机制奠定了基础。

## 使用 WebAssembly 异常处理实现 `panic=unwind`

上述 abort 恢复机制确保 Worker 能在故障后存活，但它是通过重新初始化整个应用程序来实现的。对于无状态的请求处理器来说，这没问题。但对于在内存中持有重要状态的工作负载，例如 Durable Objects，重新初始化意味着完全丢失该状态。一个请求中的单个 panic 可能会清除其他并发请求正在使用的内存状态。

在大多数原生 Rust 环境中，panic 可以被展开，允许析构函数运行，程序可以在不丢失状态的情况下恢复。在 WebAssembly 中，情况历来大不相同。通过 `wasm32-unknown-unknown` 编译到 Wasm 的 Rust 默认使用 `panic=abort`，因此 Rust Worker 内部的 panic 会突然陷入一个 `unreachable` 指令，并以 `WebAssembly.RuntimeError` 退出 Wasm 回到 JS。

为了在不丢弃实例状态的情况下从 panic 中恢复，我们需要 wasm-bindgen 为 `wasm32-unknown-unknown` 提供 `panic=unwind` 支持，这得益于 WebAssembly 异常处理提案在 2023 年获得了广泛的引擎支持。

我们首先使用 `RUSTFLAGS='-Cpanic=unwind' cargo build -Zbuild-std` 进行编译，这会用展开支持重新构建标准库，并生成具有适当 panic 展开的代码。例如：

```Rust
struct HasDropA;
struct HasDropB;
extern "C" {
    fn imported_func();
}

fn some_func() {
    let a = HasDropA;
    let b = HasDropB;
    imported_func();
}
```

编译为 WebAssembly 后：

```Rust
try
  call <imported_func>
catch_all
  call <drop_b>
  call <drop_a>
  rethrow
end
call <drop_b>
call <drop_a>
```

这确保了即使 `imported_func()` panic，析构函数仍然会运行。类似地，`std::panic::catch_unwind(|| some_func())` 编译为：

```Rust
try
  call <some_func>
  ;; set result to Ok(return value)
catch
  try
    call <std::panicking::catch_unwind::cleanup>
    ;; set result to Err(panic payload)
  catch_all
    call <core::panicking::cannot_unwind>
    unreachable
  end
end
```

要让这个机制端到端地工作，需要对 wasm-bindgen 工具链进行几处更改。WebAssembly 解析器 Walrus 不知道如何处理 try/catch 指令，因此我们为其添加了支持。描述符解释器也需要学会如何评估包含异常处理块的代码。至此，完整的应用程序就可以用 `panic=unwind` 构建了。

最后一步是修改 wasm-bindgen 生成的导出，以便在 Rust-JavaScript 边界捕获 panic，并将其作为 JavaScript `PanicError` 异常抛出。有一个微妙之处：Rust 会捕获外部异常，并在通过 `extern "C"` 函数展开时 abort，因此导出需要标记为 `extern "C-unwind"`，以明确允许跨边界展开。对于 future，panic 会用一个 `PanicError` 来拒绝 JavaScript `Promise`。

闭包需要特别注意，以确保正确检查展开安全性，这是通过一个新的 `MaybeUnwindSafe` trait 实现的，该 trait 仅在构建时使用 `panic=unwind` 时才检查 `UnwindSafe`。但这很快暴露了一个问题：许多闭包捕获的引用在展开后仍然存在，这使得它们本质上是不安全的。为了避免用户为了满足编译器要求而错误地用 `AssertUnwindSafe` 包装闭包的情况，我们添加了 `Closure::new_aborting` 变体，在无法保证展开安全的情况下，panic 时会终止而不是展开。

启用 panic 展开后：

- 导出的 Rust 函数中的 panic 会被 wasm-bindgen 捕获
- Panic 会作为 PanicError 异常抛给 JavaScript
- 异步导出会用 PanicError 拒绝其返回的 promise
- Rust 析构函数正确运行
- WebAssembly 实例保持有效且可重用

导出的 Rust 函数中的 panic 会被 wasm-bindgen 捕获

Panic 会作为 PanicError 异常抛给 JavaScript

异步导出会用 PanicError 拒绝其返回的 promise

Rust 析构函数正确运行

WebAssembly 实例保持有效且可重用

该方法的完整细节以及如何在 wasm-bindgen 中使用它，请参阅最新的指南页面 [Wasm Bindgen: Catching Panics](https://rustwasm.github.io/docs/wasm-bindgen/reference/catching-panics.html)。

## Abort 恢复

即使有 `panic=unwind` 支持，abort 仍然会发生——内存不足错误就是一个常见原因。因为 abort 无法展开，所以根本不可能进行状态恢复，但我们至少可以检测并从 abort 中恢复，以便进行后续操作，避免无效状态导致后续请求出错。

Panic 展开支持给 abort 恢复带来了一个新问题。当我们从 Wasm 收到错误时，我们不知道它是来自 `extern "C-unwind"` 的外部错误，还是真正的 abort。在 WebAssembly 中，abort 可以表现为多种形式。

从技术上讲，我们有两个选择：要么标记所有明确是 abort 的错误，要么标记所有明确是展开的错误。两者都可以，但我们选择了后者。由于我们的外部异常处理已经直接使用了原始的 WAT 级别（WebAssembly 文本格式）的异常处理指令，我们发现为外部异常实现异常标签来区分它们与 abort 的非展开安全异常更容易。

借助 WebAssembly 异常处理中 `Exception.Tag` 功能的帮助，我们能够清晰区分可恢复与不可恢复的错误，从而得以集成新的中止处理器以及中止重入防护机制。

一个新的中止钩子 `set_on_abort` 可在初始化时使用，用于附加一个处理器，该处理器会根据平台嵌入的需求进行相应的恢复。

强化 panic 和中止处理对于避免无效的执行状态至关重要。WebAssembly 允许深度交错的调用栈，即 Wasm 可以调用 JavaScript，而 JavaScript 又可以在任意深度重新进入 Wasm；与此同时，多个任务可以在同一个实例中运行。此前，一个任务或嵌套栈中发生的中止并不能保证通过 JS 使更高层级的栈失效，这导致了未定义行为。我们需要谨慎确保能够保证执行模型，并且在这一领域的贡献仍在持续进行。

虽然中止绝非理想情况，而失败时的重新初始化是绝对最坏的情形，但将关键错误恢复作为最后一道防线来实现，可以确保执行的正确性，并保证未来的操作能够成功。无效状态不会持续存在，从而确保单个故障不会级联成多个故障。

## 扩展：为 wasm-bindgen 库实现中止重新初始化

在进行这项工作的过程中，我们意识到这对于由 JS 使用的、通过 wasm-bindgen 构建的库来说是一个常见问题，它们同样可以通过附加一个中止处理器来执行恢复操作而受益。

但是，当将 Wasm 构建为 ES 模块并直接导入时（例如通过 `import { func } from 'wasm-dep'`），对于一个已经链接并初始化、且处于用户 JS 应用程序中的库，在调用 `func()` 时发生 Wasm 中止，其恢复机制并不明确。

虽然这严格来说并非 Rust Workers 的使用场景，但我们的团队也支持那些运行基于 Rust 的 Wasm 库依赖项的 JS 型 Workers 用户。如果我们能同时解决这个问题，也将间接使 Cloudflare Workers 平台上的 Wasm 使用受益。

为了支持 Wasm 库使用场景的自动中止恢复，我们在 wasm-bindgen 中添加了对实验性重新初始化机制 `--reset-state-function` 的支持。这暴露了一个函数，允许 Rust 应用程序有效地请求将其内部的 Wasm 实例重置为初始状态，以供下一次调用使用，而无需生成绑定的使用者重新导入或重新创建它们。旧实例中的类实例会因其句柄变为孤立而抛出错误，但随后可以构造新的类。使用 Wasm 库的 JS 应用程序会遇到错误，但不会完全崩溃。

关于此功能的完整技术细节以及如何在 wasm-bindgen 中使用，请参阅新的 wasm-bindgen 指南章节《Wasm Bindgen: Handling Aborts》。

## 完善 Rust Wasm 异常处理生态系统

这项工作的上游贡献并未止步于 wasm-bindgen 项目。使用 `panic=unwind` 为 Wasm 构建仍然需要一个实验性的 Rust nightly 目标，因此我们也一直在努力推进 Rust 对 WebAssembly 异常处理的支持，以帮助将其引入稳定的 Rust 版本。

在 WebAssembly 异常处理规范的发展过程中，后期的一次规范变更导致了两个变体：**传统异常处理**和最终的现代**"带有 exnref" 的异常处理**。目前，Rust 的 WebAssembly 目标默认仍然生成针对传统变体的代码。虽然传统异常处理得到广泛支持，但它现在已被弃用。

现代 WebAssembly 异常处理已在以下 JS 平台版本中得到支持：

| 运行时 | 版本 | 发布日期 |
|---|---|---|
| workerd | 13.8.1 | 2025年4月28日 |
| workerd | v1.20250620.0 | 2025年6月19日 |
| Chrome | | 2025年6月28日 |
| Firefox | | 2024年10月1日 |
| Safari | | 2025年3月31日 |
| Node.js | 25.0.0 | 2025年10月15日 |

在我们调查支持矩阵时，最大的担忧最终落在了 Node.js 24 LTS 的发布计划上，这原本会导致整个生态系统直到 2028 年 4 月都停留在传统的 WebAssembly 异常处理上。

发现这一差异后，我们成功地将现代异常处理向后移植到了 Node.js 24 版本，甚至将使其在 Node.js 22 版本线上工作所需的修复也进行了向后移植，以确保对该目标的支持。这应该能使现代异常处理提案在明年成为默认目标。

在接下来的几个月里，我们将努力使向稳定的 `panic=unwind` 和现代异常处理的过渡对最终用户尽可能无感。

虽然这些对生态系统的长期投资需要时间，但它们有助于为整个 Rust WebAssembly 社区构建更坚实的基础，我们很高兴能够为这些改进做出贡献。

## 在 Rust Workers 中使用 panic unwind

从 Rust Workers 0.8.0 版本开始，我们新增了一个 `--panic-unwind` 标志，可以按照[此处的说明](instructions here)将其添加到构建命令中。

使用此标志后，panic 可以被完全恢复，并且中止恢复将使用新的中止分类和恢复钩子机制。我们强烈建议升级并尝试使用它，以获得更稳定的 Rust Workers 体验，并计划在后续版本中将 `panic=unwind` 设为默认选项。继续使用 `panic=abort` 的用户仍将受益于自 0.6.0 版本以来的先前自定义恢复包装器处理。

## 致力于 Rust Workers 的稳定性

这项工作是我们在 Rust Workers 稳定版本发布道路上持续努力的一部分。通过从根本上解决 Wasm 平台基础的这些尖锐问题，并在有意义的地方回馈生态系统，我们不仅为自己的平台，也为整个 Rust、JS 和 Wasm 生态系统构建了更坚实的基础。

我们为 Rust Workers 规划了许多未来的改进，并将很快分享关于这些额外工作的更新，包括 wasm-bindgen 泛型和自动绑定生成，我们团队的 Guy Bedford 在上个月 Wasm.io 的《Rust & JS Interoperability》演讲中已经预览了这些内容。

请在 Cloudflare Discord 的 `#rust-on-workers` 频道找到我们。我们也欢迎反馈和讨论，特别是欢迎所有新的贡献者加入 `workers-rs` 和 `wasm-bindgen` GitHub 项目。

---

> 本文由AI自动翻译，原文链接：[Making Rust Workers reliable: panic and abort recovery in wasmâbindgen](https://blog.cloudflare.com/making-rust-workers-reliable/)
> 
> 翻译时间：2026-04-23 05:04
