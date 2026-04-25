---
title: AI Agent助力Turborepo性能飙升96%
title_original: Making Turborepo 96% faster with agents, sandboxes, and humans - Vercel
  – Vercel
date: '2026-03-30'
source: Vercel Blog
source_url: https://vercel.com/blog/making-turborepo-ninety-six-percent-faster-with-agents-sandboxes-and-humans
author: ''
summary: Vercel工程师通过结合AI Agent、沙箱环境和人工工程实践，在八天内将Turborepo的任务图计算速度提升了81-91%，最高达96%。文章详细介绍了使用8个后台编码Agent自动生成优化PR的过程，包括哈希算法替换、内存分配优化等，同时指出当前无人值守Agent在上下文理解、基准测试和回归测试方面的局限性。
categories:
- 技术趋势
tags:
- Turborepo
- AI Agent
- 性能优化
- Monorepo
- Vercel
draft: false
translated_at: '2026-04-25T04:38:08.657866'
---

Turborepo 现在在我们的仓库中计算任务图的速度提升了 81-91%，且随仓库规模扩展。在我们拥有 1000 多个包的 monorepo 中，`turbo run` 现在感觉瞬间完成。首次任务执行时间现在快了 11 倍。

![](/images/posts/07a9ab777440.jpg)

![](/images/posts/9811b39e1e23.jpg)

在用一些开源 Turborepo 测试我的改动，并请 Vercel 客户在他们的仓库中试用金丝雀版本后，我发现性能提升最高可达 96%，具体取决于仓库的规模和复杂度。

这些性能提升背后的过程值得分享，因为这不是单一优化或单一技术。而是八天里混合使用 AI Agent（智能体）、Vercel Sandboxes 以及典型、枯燥的工程实践。

## Link to headingTurborepo 如何调度你的任务

每次 `turbo run` 都从分析你的 monorepo 结构、脚本和依赖关系开始，以构建一个任务图。该图决定了执行顺序，创建了并行性，并为缓存提供支持，这样你就永远不会重复做同样的工作。

![使用 Turborepo 的顺序与并行任务调度](/images/posts/e61460da63d2.jpg)

![使用 Turborepo 的顺序与并行任务调度](/images/posts/050b12ee70fa.jpg)

构建任务图是在仓库工作开始之前需要付出的开销。仓库越大，开销越高。在我们拥有 1000 个包的 monorepo 上，在 M4 Pro Max 上这个开销大约为 10 秒。我不知道你怎么想，但我认为这是不可接受的。

## Link to heading从无人值守的 Agent（智能体）开始

我想看看在没有太多指导的情况下，Agent（智能体）能对此做些什么。我在睡前从手机启动了 8 个后台编码 Agent（智能体），每个针对 Rust 代码库中我怀疑速度过慢的不同部分。

在每个提示词中，我将我感兴趣的代码库部分替换为一个新目标。我很好奇，在充满模糊性的情况下，这些 Agent（智能体）能取得什么成果，以此作为基线。

到了早上，8 个中有 3 个产生了可以转化为可交付成果的输出：

- PR #11872 减少了约 25% 的挂钟时间，通过引用进行哈希而不是克隆整个 `HashMap` 来减少分配压力。
- PR #11874 将我们的 Rust 依赖 crate 之一 `twox-hash` 替换为 `xxhash-rust`。这是一个近乎 1:1 的替换，使用了更快的哈希算法，带来了约 6% 的提升。
- PR #11878 源自一个我们尚未处理的现有 `TODO` 注释。我们需要用多源深度优先搜索（DFS）替换不必要的 Floyd-Warshall 算法。这并不在 `turbo run` 的热路径上，但我的提示词没有指定 *哪个* 热路径，对吧？公平。

PR #11872 减少了约 25% 的挂钟时间，通过引用进行哈希而不是克隆整个 `HashMap` 来减少分配压力。

PR #11874 将我们的 Rust 依赖 crate 之一 `twox-hash` 替换为 `xxhash-rust`。这是一个近乎 1:1 的替换，使用了更快的哈希算法，带来了约 6% 的提升。

PR #11878 源自一个我们尚未处理的现有 `TODO` 注释。我们需要用多源深度优先搜索（DFS）替换不必要的 Floyd-Warshall 算法。这并不在 `turbo run` 的热路径上，但我的提示词没有指定 *哪个* 热路径，对吧？公平。

这些无疑是重要的成功，但回顾所有 8 个聊天会话和代码输出，也让我同样清楚地认识到，在没有适当上下文工程的情况下，当前最先进的无人值守 Agent（智能体）会在哪些方面存在不足。

- Agent（智能体）从未意识到它可以在 Turborepo 代码库本身上对改进进行基准测试。Turborepo 自用 Turborepo，因此它可以轻松构建一个二进制文件并直接在源代码上运行，以获得端到端的结果。
- Agent（智能体）会过度专注于它想到的第一个想法，并强行让它工作，而不是退后一步，抽象地思考问题（尽管聊天日志显示它试图这样做）。
- Agent（智能体）会追求它能得到的最大数字，创建微基准测试，但这些测试在实际性能方面相对毫无意义。然后它会为基准测试得出 97% 的提升，而实际提升只有 0.02%。
- Agent（智能体）从未编写过回归测试。
- Agent（智能体）从未在 `turbo` CLI 中使用过 `--profile` 标志。

Agent（智能体）从未意识到它可以在 Turborepo 代码库本身上对改进进行基准测试。Turborepo 自用 Turborepo，因此它可以轻松构建一个二进制文件并直接在源代码上运行，以获得端到端的结果。

Agent（智能体）会过度专注于它想到的第一个想法，并强行让它工作，而不是退后一步，抽象地思考问题（尽管聊天日志显示它试图这样做）。

Agent（智能体）会追求它能得到的最大数字，创建微基准测试，但这些测试在实际性能方面相对毫无意义。然后它会为基准测试得出 97% 的提升，而实际提升只有 0.02%。

Agent（智能体）从未编写过回归测试。

Agent（智能体）从未在 `turbo` CLI 中使用过 `--profile` 标志。

无人值守运行的 Agent（智能体）取得了一些不错的成果，但我能感觉到这不可持续。我们需要更强的测试和更好的验证循环。我必须更多地参与其中。

## Link to heading让性能分析对 Agent（智能体）和人类都有效

我做的第一件常规工程事情是进行性能分析。很震惊，我知道。

我在我们最大的仓库上运行了 `turbo run build --profile`，并在 Perfetto 中打开了跟踪。

![](/images/posts/9a619fcecb0c.jpg)

![](/images/posts/5d9b213c7a14.jpg)

火焰图信息丰富，但使用起来可能很慢。尽管我确实喜欢阅读火焰图并努力取得成果，但 Turborepo 还有很多事情要做。我有责任高效且有效地为 Turborepo 用户工作，使用我所能获得的最佳工具。

### Link to heading也许 Chrome Tracing JSON 不是最佳格式

Turborepo 的性能分析文件是 Chrome Trace Event 格式的 JSON 文件。

```
1[2  {"ph":"M","pid":1,"name":"process_name","args":{"name":"turbo 2.8.21-canary.9"}},3  {"ph":"M","pid":1,"name":"process_labels","args":{"labels":"macos, 14 CPUs"}},4  {"ph":"M","pid":1,"name":"thread_name","tid":0,"args":{"name":"main"}},5  {"ph":"e","pid":1,"ts":8.167,"name":"enable_chrome_tracing","cat":"turborepo_lib::tracing","tid":0,"id":1,".file":"crates/turborepo-lib/src/tracing.rs",".line":325},6  {"ph":"b","pid":1,"ts":52.917,"name":"shim_run","cat":"turborepo_lib::shim","tid":0,"id":2251799813685249,".file":"crates/turborepo-lib/src/shim.rs",".line":224},7  {"ph":"b","pid":1,"ts":58.959,"name":"run_with_args","cat":"turborepo_shim::run","tid":0,"id":2251799813685249,".file":"crates/turborepo-shim/src/run.rs",".line":189},8  {"ph":"i","pid":1,"ts":77.584,"name":"event crates/turborepo-shim/src/run.rs:223","cat":"turborepo_shim::run","tid":0,"s":"t",".file":"crates/turborepo-shim/src/run.rs",".line":223},9  {"ph":"b","pid":1,"ts":78.792,"name":"repo_inference","cat":"turborepo_shim::run","tid":0,"id":2251799813685249,".file":"crates/turborepo-shim/src/run.rs",".line":251},10  {"ph":"b","pid":1,"ts":88.209,"name":"infer","cat":"turborepo_repository::inference","tid":0,"id":2251799813685249,".file":"crates/turborepo-repository/src/inference.rs",".line":76},11  {"ph":"i","pid":1,"ts":130.375,"name":"event crates/turborepo-repository/src/package_json.rs:166","cat":"turborepo_repository::package_json","tid":0,"s":"t",".file":"crates/turborepo-repository/src/package_json.rs",".line":166},12  {"ph":"b","pid":1,"ts":456.709,"name":"parse","cat":"biome_json_parser","tid":0,"id":2251799813685249,".file":"/Users/runner/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/biome_json_parser-0.5.7/src/lib.rs",".line":32},13  {"ph":"e","pid":1,"ts":546.042,"name":"parse","cat":"biome_json_parser","tid":0,"id":2251799813685249,".file":"/Users/runner/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/biome_json_parser-0.5.7/src/lib.rs",".line":32},14  {"ph":"i","pid":1,"ts":5418.584,"name":"event crates/turborepo-repository/src/package_json.rs:166","cat":"turborepo_repository::package_json","tid":0,"s":"t",".file":"crates/turborepo-repository/src/package_json.rs",".line":166},15  16]
```

一个由 Turborepo 生成的简略版 Chrome Tracing 分析文件

理论上，LLM 可以通读并解析所有这些内容，但是……嗯……你看看就知道了。函数标识符跨行分布，无关的元数据与时间数据混杂在一起，不便于 grep 搜索。我让一个 Agent 处理这个文件，看着它艰难地调用 grep，试图从不同行中拼凑出函数名，却无法成功过滤掉噪声。它在这个文件中摸索的样子，和我自己动手时如出一辙。

我与编码 Agent 协作时最喜欢的一个启发式原则是：如果某个东西对我来说设计得很糟糕，那么它对 Agent 来说也设计得很糟糕。这不一定是关于工作量的评论，更多是关于接口的。如果某个东西对我来说难以阅读，那么按理说它对 Agent 来说也难以阅读。这个想法有其局限性，但你很快就会看到它立竿见影的效果。

### 链接到标题构建对 LLM 友好的分析文件

一周前，我看到 Jarred Sumner 的一条推文，提到 Bun 发布了一个新标志：`--cpu-prof-md`。它可以将分析文件输出为 Markdown 格式，这很容易符合我对 Agent 最佳工作方式的理解。

在 #11880 中，我添加了一个新的 `turborepo-profile-md` crate，它为每个跟踪文件生成一个配套的 `.md` 文件。按自身耗时排序的热门函数、按总耗时排序的调用树、调用者/被调用者关系。全部可 grep，全部位于单行内。

```
1# CPU Profile2
3| Duration | Spans | Functions |4| 21.6s    | 871   | 97        |5
6**Top 10:** `visit_recv_wait` 69.8%, `put` 30.6%, `build_http_client` 0.6%, `capture_scm_state` 0.5%, `find_untracked_files` 0.2%, `repo_index_untracked_await` 0.2%, `walk_glob` 0.2%, `cache_save` 0.1%, `parse_lockfile` 0.1%, `hash_scope` 0.1%7
8## Hot Functions (Self Time)9
10| Self%  | Self     | Total% | Total    | Function            | Location                                                 |11| 69.8%  | 15.1s    | 69.8%  | 15.1s    | `visit_recv_wait`   | `crates/turborepo-lib/src/task_graph/visitor/mod.rs:358` |12| 30.6%  | 6.6s     | 30.6%  | 6.6s     | `put`               | `crates/turborepo-cache/src/fs.rs:196`                   |13| 0.6%   | 127.0ms  | 0.6%   | 127.0ms  | `build_http_client` | `crates/turborepo-api-client/src/lib.rs:623`             |14| 0.5%   | 109.1ms  | 0.5%   | 109.1ms  | `capture_scm_state` | `crates/turborepo-lib/src/run/builder.rs:573`            |15
16## Call Tree (Total Time)17
18| Total% | Total    | Self%  | Self     | Function                    | Location                                                         |19| 69.9%  | 15.1s    | 0.0%   | 10us     | `run`                       | `crates/turborepo-lib/src/run/mod.rs:876`                        |20| 69.9%  | 15.1s    | 0.0%   | 447us    | `execute_visitor`           | `crates/turborepo-lib/src/run/mod.rs:659`                        |21| 69.8%  | 15.1s    | 0.0%   | 1.7ms    | `visit`                     | `crates/turborepo-lib/src/task_graph/visitor/mod.rs:315`         |22| 69.8%  | 15.1s    | 69.8%  | 15.1s    | `visit_recv_wait`           | `crates/turborepo-lib/src/task_graph/visitor/mod.rs:358`         |23| 30.6%  | 6.6s     | 0.0%   | 171us    | `cache worker: cache PUT`   | `crates/turborepo-cache/src/async_cache.rs:80`                   |24| 30.6%  | 6.6s     | 30.6%  | 6.6s     | `put`                       | `crates/turborepo-cache/src/fs.rs:196`                           |25| 0.6%   | 127.0ms  | 0.0%   | 8us      | `http_client_init`          | `crates/turborepo-api-client/src/shared_http_client.rs:68`       |26| 0.6%   | 127.0ms  | 0.6%   | 127.0ms  | `build_http_client`         | `crates/turborepo-api-client/src/lib.rs:623`                     |27| 0.5%   | 109.1ms  | 0.5%   | 109.1ms  | `capture_scm_state`         | `crates/turborepo-lib/src/run/builder.rs:573`                    |28

```

一个由 Turborepo 生成的简略版 Markdown 分析文件

Agent 输出质量的变化是巨大的。相同的模型、相同的代码库、相同的数据、相同的 Agent 框架。不同的格式，带来了截然不同的、更优的优化建议。分析数据终于变成了我和 Agent 都能一目了然的格式。

### 链接到标题迭代循环

有了 Markdown 分析文件，我进入了一种稳定的节奏。

1.  将 Agent 置于计划模式，指示其创建分析文件并在 Markdown 输出中查找热点
2.  审查提出的优化建议，并决定哪些值得跟进
3.  让 Agent 实现好的建议
4.  通过端到端的 hyperfine 基准测试进行验证
5.  提交 PR
6.  重复

将 Agent 置于计划模式，指示其创建分析文件并在 Markdown 输出中查找热点

审查提出的优化建议，并决定哪些值得跟进

让 Agent 实现好的建议

通过端到端的 hyperfine 基准测试进行验证

提交 PR

重复

这个循环在四天内产生了超过 20 个性能相关的 PR。成果可分为三类。我来举一些例子。

并行化是最大的类别。构建 git 索引、遍历文件系统进行 glob 匹配、解析锁文件以及加载 `package.json` 文件，这些都是可以并发运行的顺序操作。PR #11889、#11902、#11927 和 #11918 将这些热点路径并行化了。

消除内存分配减少了整个流水线中的冗余拷贝和克隆，包括 SCM 操作中基于引用的哈希（#11916）、预编译 glob 排除过滤器（#11991），以及使用共享的 HTTP 客户端而不是为每个请求构建一个新的客户端（#11929）。

减少系统调用将每个包的 git 子进程调用批处理为单个仓库范围的索引（#11887），用 `libgit2` 库调用替换了 git 子进程（#11938），然后完全用更快的 `gix-index` 替换了 `libgit2`（#11950）。

再次强调，这只是典型、普通、枯燥的软件工程工作。我曾尝试将其变成Ralph Wiggum循环，但它反复出现太多错误。模型、框架和循环的组合根本不够可靠，而且可能太快地在我眼皮底下移动大量代码。也许如果我在做一个副业项目，我会接受这种情况，但Turborepo支撑着世界上一些最大的代码仓库。我必须既快速又负责。

### 链接到标题 你的源代码是最好的反馈循环

在这个阶段，我注意到的最有趣的模式是，代码库本身如何成为Agent最强的反馈机制。

我会指出Agent正在处理的代码中的一个性能问题。我们一起修复它。然后我问："你看到其他地方有同样可以改进的地方吗？" Agent会在整个代码库中找到更多相同模式的实例。根据改动的大小，我会要么将改动添加到PR中，要么记录下来稍后处理。

在现有代码存在草率模式的地方，Agent会以相同的风格编写新代码。一旦我纠正了一个实例，Agent就会在后续工作中遵循这个纠正。在未来的对话中，即使聊天之间没有任何记忆或上下文传递，Agent也会看到源代码中已合并的改进，并停止复现旧的模式。

随着时间的推移，我注意到Agent会在我不期望的时候自发地编写测试。我看到它创建了与我本会做的相匹配的抽象，这在以前是没有发生的。我会重新审视代码库中Agent之前表现不佳的地方，并且在模型或框架没有任何变化的情况下，它会生成更好的代码输出。

事实证明，你自己的源代码就是最好的强化学习。

### 链接到标题 在85%处遇到瓶颈

到本周结束时，Turborepo在我们最大的代码仓库上大约快了85%。在我开始之前，我随意设定了一个提升95%的目标。剩下的增益感觉触手可及。

问题变成了测量。我一直在我的MacBook上运行所有基准测试，而hyperfine报告变得越来越嘈杂。随着代码变快，系统噪声变得更加重要。系统调用、内存和磁盘I/O都有其自身的方差。

性能分析结果也很嘈杂。我已经将代码库优化到单个函数足够快的程度，以至于我笔记本电脑上的后台活动淹没了任何好的信号。

我做的改动真的快了2%吗？还是我只是碰巧遇到了一次安静的运行？我无法自信地区分真正的改进和噪声。我需要一个更安静的实验室来进行我的科学实验。

## 链接到标题 用于基准测试的Vercel Sandbox

Vercel Sandboxes是临时的Linux容器，只包含你放入其中的内容。没有后台守护进程，没有Slack通知占用CPU，没有后台程序发起网络请求。机器的资源完全专注于你正在运行的内容。

我编写了一个bash脚本来自动化整个基准测试工作流程。我将在下面提供一个完整要点 的简化版本。

```
12zig cc -target x86_64-linux-gnu ...3cargo build --release --target x86_64-unknown-linux-gnu4
56sandbox create --snapshot turbo-bench-snapshot7
89sandbox cp ./target/release/turbo-main sandbox:/usr/local/bin/turbo-main10sandbox cp ./target/release/turbo-branch sandbox:/usr/local/bin/turbo-branch11
1213sandbox exec -- hyperfine \14  --warmup 2 --runs 15 \15  'turbo-main run build --dry' \16  'turbo-branch run build --dry'17
1819sandbox exec -- turbo-main run build --profile=main-profile20sandbox exec -- turbo-branch run build --profile=branch-profile21sandbox cp sandbox:/reports/ ./local-reports/
```

Sandbox基准测试工作流程

你会注意到，在这个脚本的末尾，我将性能分析结果下载回我的笔记本电脑。然后我的Agent可以在本地检查基准测试结果和Markdown格式的性能分析数据，我就能自信地判断一个改动是真正的改进还是噪声。

一个注意事项：Vercel Sandboxes目前不保证专用硬件。比较不同Sandbox实例的报告可能没有用处。所有比较都应来自单个实例，其中两个二进制文件在相同条件下运行。

### 链接到标题 突破瓶颈

有了来自Sandbox的清晰信号，我能够看到底层改动中的真正突破，这些在我的嘈杂笔记本电脑上是不可见的。

栈分配的Git OID（#11984）

Git索引中的每个文件都将其40字符的SHA-1哈希存储为一个堆分配的String。在我们最大的代码仓库上，仅new_from_gix_index就创建了超过10,000个独立的40字节堆分配。

```
123#[derive(Clone, Copy, PartialEq, Eq, Hash)]4pub struct OidHash([u8; 40]);5
6impl OidHash {7    pub fn from_hex_str(s: &str) -> Self {8        let mut buf = [0u8; 40];9        buf.copy_from_slice(s.as_bytes());10        Self(buf)11    }12}13
14impl std::ops::Deref for OidHash {15    type Target = str;16    fn deref(&self) -> &str {17        18        unsafe { std::str::from_utf8_unchecked(&self.0) }19    }20}
```

栈分配的OidHash类型

OidHash实现了Deref<Target=str>，因此现有的消费者无需改动即可工作，而Copy意味着克隆是在栈上进行40字节的memcpy，而不是堆分配。性能分析数据显示，new_from_gix_index的自用时间下降了15%，get_package_file_hashes_from_index下降了17%。

仓库大小

之前

之后

变化

~1,000个包

1.463s ± 0.052s

1.466s ± 0.027s

速度相同，方差降低48%

~125个包

658.6ms ± 144.6ms

592.1ms ± 62.9ms

快10%，方差降低57%

6个包

96.8ms ± 46.7ms

75.0ms ± 18.4ms

快22%，方差降低61%

在所有三种规模中，最显著的改进是运行间方差的减少，这与我们关于分配器压力减小和性能更可预测的理论相符。

消除系统调用（#11985）

每次缓存获取都执行了三个系统调用：stat(.tar)，返回ENOENT，然后stat(.tar.zst)，接着open(.tar.zst)。奇怪的模式。

经过一些挖掘，我弄清楚了.tar回退的存在是为了兼容Turborepo的Golang时代（2021-2022）的缓存工件。没有现代版本会写入未压缩的缓存条目，并且缓存条目会不断轮换。

```
12let cache_path = if uncompressed_cache_path.exists() {  3    uncompressed_cache_path4} else if compressed_cache_path.exists() {               5    compressed_cache_path6};7let mut cache_reader = CacheReader::open(&cache_path)?;  8
910let mut cache_reader = match CacheReader::open(&cache_path) {  11    Ok(reader) => reader,12    Err(CacheError::IO(ref e, _))13        if e.kind() == std::io::ErrorKind::NotFound => {14        return Ok(None);  15    }16    Err(e) => return Err(e),17};
```

消除缓存获取中的冗余系统调用

在我们最大的代码仓库上，跨越962次缓存获取，fetch的自用时间从200.5ms下降到129.6ms，减少了35%。

移动而非克隆（#11986）

访问者调度循环为大约1,700个任务中的每一个，从一个预计算映射中深度克隆一个(String, HashMap<String, String>)。由于每个任务ID在调度流中只出现一次，HashMap::remove()可以以零成本移出该值，而不是克隆。

## 链接到标题 结果

八天后，我们最大代码仓库上的"首次任务时间"从8.1秒下降到716毫秒。

v2.8.0

v2.9.0

改进

0.716s

快91%

132个包

0.361s

快81%

0.676s

0.132s

快80%

我估计如果没有Agent，这至少需要两个月的时间，但我希望这篇文章能向你展示，它们并没有替我完成工作。我一直在主导整个过程，决定分析什么，追求哪些方案，何时更换工具，以及何时改变策略。但是，我现有的工程知识、为Agent提供更好的工具以及一个干净的基准测试环境这三者的结合，让我能够以六个月前不可能达到的速度前进。

## 链接到标题 已在Turborepo 2.9中发布

这些性能提升现已稳定，可供您使用。请访问 Turborepo 2.9 发布文章，了解更多关于 Turborepo 最新动态的信息。

---

> 本文由AI自动翻译，原文链接：[Making Turborepo 96% faster with agents, sandboxes, and humans - Vercel – Vercel](https://vercel.com/blog/making-turborepo-ninety-six-percent-faster-with-agents-sandboxes-and-humans)
> 
> 翻译时间：2026-04-25 04:38
