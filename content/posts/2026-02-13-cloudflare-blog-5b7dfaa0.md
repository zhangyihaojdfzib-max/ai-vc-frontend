---
title: Cloudflare开源Rust优雅重启库ecdysis
title_original: 'Shedding old code with ecdysis: graceful restarts for Rust services
  at Cloudflare'
date: '2026-02-13'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/ecdysis-rust-graceful-restarts/
author: ''
summary: 本文介绍了Cloudflare开源的Rust库ecdysis，它实现了网络服务的优雅进程重启，确保在升级过程中不中断活动连接或拒绝新请求。文章阐述了传统粗暴重启方式在云服务规模下面临的连接丢失与拒绝问题，并详细说明了ecdysis的工作原理——通过父子进程间共享套接字描述符和就绪信号机制，实现零停机部署。该库已在Cloudflare生产环境运行五年，成功用于关键基础设施的升级。
categories:
- AI基础设施
tags:
- Rust
- 云服务
- 零停机部署
- 开源
- 网络基础设施
draft: false
translated_at: '2026-02-14T04:16:19.915845'
---

# 蜕旧迎新：Cloudflare Rust服务的优雅重启方案

2026-02-13

- Manuel Olguín Muñoz

![](/images/posts/0bf931c245b1.png)

ecdysis |ËekdÉsÉs|
蜕皮过程（爬行动物）或蜕去外角质层（昆虫及其他节肢动物）。

如何在不中断任何连接的情况下，升级一个每秒处理全球数百万请求的网络服务？

Cloudflare应对这一巨大挑战的解决方案之一是长期使用的`ecdysis`——一个Rust库，它实现了优雅的进程重启，确保活动连接不被丢弃，新连接不被拒绝。Â

上个月，我们开源了`ecdysis`，现在任何人都可以使用它。在Cloudflare经过五年的生产环境使用后，`ecdysis`已通过在我们的关键Rust基础设施上实现零停机升级证明了其价值，在Cloudflare全球网络的每次重启中挽救了数百万请求。

正确执行这些升级的重要性怎么强调都不为过，尤其是在Cloudflare网络的规模下。我们的许多服务执行关键任务，如流量路由、TLS生命周期管理或防火墙规则执行，必须持续运行。如果这些服务之一宕机，哪怕只是一瞬间，其连锁影响都可能是灾难性的。连接中断和请求失败会迅速导致客户性能下降和业务影响。

当这些服务需要更新时，安全补丁刻不容缓。漏洞修复需要部署，新功能必须推出。Â

简单粗暴的方法是等待旧进程停止后再启动新进程，但这会创造一段连接被拒绝、请求被丢弃的时间窗口。对于一个在单个地点每秒处理数千请求的服务，将其乘以数百个数据中心，一次短暂的重启就会在全球范围内导致数百万次失败的请求。

让我们深入探讨这个问题，以及`ecdysis`如何成为我们的解决方案——或许也将成为你的解决方案。

链接：GitHub|crates.io|docs.rs

### 为何优雅重启如此困难

正如我们提到的，重启服务的简单方法是停止旧进程并启动新进程。这对于不处理实时请求的简单服务尚可接受，但对于处理活动连接的网络服务，这种方法存在严重局限性。

首先，简单粗暴的方法会创建一个没有进程监听传入连接的时间窗口。当旧进程停止时，它会关闭其监听套接字，导致操作系统立即以`ECONNREFUSED`拒绝新连接。即使新进程立即启动，总会存在一个没有任何东西接受连接的间隙，无论是毫秒级还是秒级。对于一个每秒处理数千请求的服务，即使是100毫秒的间隙也意味着数百个连接被丢弃。

其次，停止旧进程会杀死所有已建立的连接。正在上传大文件或流式传输视频的客户端会突然断开连接。像WebSockets或gRPC流这样的长连接会在操作中途被终止。从客户端的角度来看，服务直接消失了。

在关闭旧进程之前绑定新进程似乎解决了这个问题，但也引入了额外的问题。内核通常只允许一个进程绑定到地址:端口组合，但`SO_REUSEPORT`套接字选项允许多个绑定。然而，这在进程转换期间会产生一个问题，使其不适合优雅重启。

当使用`SO_REUSEPORT`时，内核为每个进程创建独立的监听套接字，并在这些套接字之间对新连接进行负载均衡。当收到连接的初始`SYN`数据包时，内核会将其分配给其中一个监听进程。一旦初始握手完成，连接就会驻留在该进程的`accept()`队列中，直到进程接受它。如果该进程在接收此连接之前退出，该连接就会变成孤儿连接并被内核终止。GitHub的工程团队在构建其GLB Director负载均衡器时广泛记录了这个问题。

### ecdysis的工作原理

当我们着手设计和构建`ecdysis`时，我们为该库确定了四个关键目标：

1.  升级后旧代码可以完全关闭。
2.  新进程拥有初始化的宽限期。
3.  新代码在初始化期间崩溃是可以接受的，不应影响正在运行的服务。
4.  仅允许单个升级并行运行，以避免级联故障。

升级后旧代码可以完全关闭。

新进程拥有初始化的宽限期。

新代码在初始化期间崩溃是可以接受的，不应影响正在运行的服务。

仅允许单个升级并行运行，以避免级联故障。

`ecdysis`遵循NGINX开创的方法来满足这些要求，NGINX自早期版本以来就支持优雅升级。该方法很直接：Â

1.  父进程`fork()`一个新的子进程。
2.  子进程使用`execve()`将自己替换为新版本的代码。
3.  子进程通过与父进程共享的命名管道继承套接字文件描述符。
4.  父进程等待子进程发出就绪信号后再关闭。

父进程`fork()`一个新的子进程。

子进程使用`execve()`将自己替换为新版本的代码。

子进程通过与父进程共享的命名管道继承套接字文件描述符。

父进程等待子进程发出就绪信号后再关闭。

关键在于，套接字在整个转换过程中保持打开状态。子进程通过命名管道共享的文件描述符从父进程继承监听套接字。在子进程初始化期间，两个进程共享相同的内核底层数据结构，允许父进程继续接受和处理新的及现有的连接。一旦子进程完成初始化，它会通知父进程并开始接受连接。收到此就绪通知后，父进程立即关闭其监听套接字的副本，并继续仅处理现有连接。Â

这个过程消除了覆盖间隙，同时为子进程提供了安全的初始化窗口。会有一个短暂的时间窗口，父进程和子进程可能同时接受连接。这是有意为之的；父进程接受的任何连接都会作为排空过程的一部分被处理直到完成。

此模型还提供了所需的崩溃安全性。如果子进程在初始化期间失败（例如，由于配置错误），它直接退出即可。由于父进程从未停止监听，没有连接被丢弃，问题修复后可以重试升级。

`ecdysis`通过`Tokio`和`systemd`集成，为异步编程提供一流支持，实现了分叉模型：

-   Tokio集成：为Tokio提供原生异步流包装器。继承的套接字无需额外胶水代码即可成为监听器。对于同步服务，`ecdysis`支持无需异步运行时的操作。
-   systemd-notify支持：启用`systemd_notify`功能时，`ecdysis`会自动与systemd的进程生命周期通知集成。在服务单元文件中设置`Type=notify-reload`允许systemd正确跟踪升级。
-   systemd命名套接字：`systemd_sockets`功能使`ecdysis`能够管理系统d激活的套接字。您的服务可以同时支持套接字激活和优雅重启。

Tokio集成：为Tokio提供原生异步流包装器。继承的套接字无需额外胶水代码即可成为监听器。对于同步服务，`ecdysis`支持无需异步运行时的操作。

systemd通知支持：启用`systemd_notify`功能后，ecdysis会自动与systemd的进程生命周期通知系统集成。在服务单元文件中设置`Type=notify-reload`可使systemd正确跟踪升级过程。

systemd命名套接字：`systemd_sockets`功能使ecdysis能够管理系统d激活的套接字。您的服务可同时支持套接字激活和平滑重启。

平台说明：ecdysis依赖Unix特有的系统调用来实现套接字继承和进程管理，因此无法在Windows系统上运行。这是采用分叉方法的基础性限制。

### 安全考量

平滑重启机制引入了安全考量。分叉模型会创建一个短暂的时间窗口，期间新旧两代进程共存，两者都能访问相同的监听套接字和潜在敏感的文件描述符。

ecdysis通过以下设计应对这些关切：

分叉后执行：ecdysis遵循传统的Unix模式，先执行`fork()`随即执行`execve()`。这确保子进程从全新状态启动：拥有新的地址空间、全新代码且不继承内存。只有显式传递的文件描述符会跨越进程边界。

显式继承：仅监听套接字和通信管道会被继承。其他文件描述符通过`CLOEXEC`标志关闭。这防止敏感句柄意外泄漏。

seccomp兼容性：使用seccomp过滤器的服务必须允许`fork()`和`execve()`系统调用。这是权衡取舍：平滑重启需要这些系统调用，因此不能将其阻断。

对大多数网络服务而言，这些权衡是可接受的。分叉-执行模型的安全性已得到充分理解，并在NGINX、Apache等软件中经过数十年的实战检验。

### 代码示例

让我们看一个实际示例。这是一个支持平滑重启的简化TCP回显服务器：

```Rust
use ecdysis::tokio_ecdysis::{SignalKind, StopOnShutdown, TokioEcdysisBuilder};
use tokio::{net::TcpStream, task::JoinSet};
use futures::StreamExt;
use std::net::SocketAddr;

#[tokio::main]
async fn main() {
    // 创建ecdysis构建器
    let mut ecdysis_builder = TokioEcdysisBuilder::new(
        SignalKind::hangup()  // 在SIGHUP信号时触发升级/重载
    ).unwrap();

    // 在SIGUSR1信号时触发停止
    ecdysis_builder
        .stop_on_signal(SignalKind::user_defined1())
        .unwrap();

    // 创建监听套接字——将被子进程继承
    let addr: SocketAddr = "0.0.0.0:8080".parse().unwrap();
    let stream = ecdysis_builder
        .build_listen_tcp(StopOnShutdown::Yes, addr, |builder, addr| {
            builder.set_reuse_address(true)?;
            builder.bind(&addr.into())?;
            builder.listen(128)?;
            Ok(builder.into())
        })
        .unwrap();

    // 生成处理连接的任务
    let server_handle = tokio::spawn(async move {
        let mut stream = stream;
        let mut set = JoinSet::new();
        while let Some(Ok(socket)) = stream.next().await {
            set.spawn(handle_connection(socket));
        }
        set.join_all().await;
    });

    // 发送就绪信号并等待关闭
    let (_ecdysis, shutdown_fut) = ecdysis_builder.ready().unwrap();
    let shutdown_reason = shutdown_fut.await;

    log::info!("Shutting down: {:?}", shutdown_reason);

    // 优雅排空连接
    server_handle.await.unwrap();
}

async fn handle_connection(mut socket: TcpStream) {
    // 此处为连接回显逻辑
}
```

关键要点：

1. `build_listen_tcp`创建将被子进程继承的监听器。
2. `ready()`向父进程发送初始化完成信号，使其可安全退出。
3. `shutdown_fut.await`阻塞直到收到升级或停止请求。该future仅在进程应关闭时返回结果——无论是因升级/重载成功执行，还是因收到关闭信号。

当向此进程发送`SIGHUP`信号时，ecdysis将执行以下操作...

...在父进程中：
- 分叉并执行二进制文件的新实例
- 将监听套接字传递给子进程
- 等待子进程调用`ready()`
- 排空现有连接后退出

...在子进程中：
- 按照与父进程相同的执行流程初始化自身，但ecdysis拥有的套接字会被继承且子进程不会重新绑定
- 通过调用`ready()`向父进程发送就绪信号
- 阻塞等待关闭或升级信号

### 大规模生产实践

自2021年起，ecdysis已在Cloudflare的生产环境中运行。它为部署在120多个国家、330多个数据中心的Rust基础设施关键服务提供支持。这些服务每日处理数十亿请求，并需要频繁更新安全补丁、功能发布和配置变更。

每次使用ecdysis进行的重启，都能避免数十万请求在简单停止/启动周期中被丢弃。在我们全球部署范围内，这意味着为数百万连接提供保护，并为客户提升了可靠性。

### ecdysis与其他方案对比

多个技术生态都存在平滑重启库。理解何时使用ecdysis及其替代方案对选择合适工具至关重要。

`tableflip`是我们启发ecdysis开发的Go语言库。它为Go服务实现了相同的分叉继承模型。如需Go方案，tableflip是绝佳选择！

`shellflip`是Cloudflare的另一个Rust平滑重启库，专为我们的Rust代理框架Oxy设计。shellflip更具针对性：它假定使用systemd和Tokio，并专注于在父子进程间传输任意应用状态。这使其非常适合复杂的有状态服务，或需要实施严格沙箱化（甚至无法自行打开套接字）的服务，但对简单场景会增加开销。

### 开始构建

ecdysis为Rust生态带来了五年生产环境锤炼的平滑重启能力。这项技术正保护着Cloudflare全球网络中数百万连接，现已开源供所有人使用！

完整文档请访问docs.rs/ecdysis，包含API参考、常见用例示例以及与`systemd`集成的步骤。

代码仓库中的`examples`目录包含可运行代码，演示了TCP监听器、Unix套接字监听器和systemd集成。

该库由Argo智能路由与Orpheus团队积极维护，并得到Cloudflare各团队的贡献。我们欢迎通过GitHub提交贡献、错误报告和功能请求。

无论您正在构建高性能代理、长期运行的API服务器，还是任何重视运行时间的网络服务，ecdysis都能为零停机运营提供基础。

开始构建：github.com/cloudflare/ecdysis

---

> 本文由AI自动翻译，原文链接：[Shedding old code with ecdysis: graceful restarts for Rust services at Cloudflare](https://blog.cloudflare.com/ecdysis-rust-graceful-restarts/)
> 
> 翻译时间：2026-02-14 04:16
