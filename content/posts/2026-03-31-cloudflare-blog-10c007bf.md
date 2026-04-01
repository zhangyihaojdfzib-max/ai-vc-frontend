---
title: Cloudflare推出可编程流量防护，支持自定义DDoS缓解逻辑
title_original: 'Introducing Programmable Flow Protection: custom DDoS mitigation
  logic for Magic Transit customers'
date: '2026-03-31'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/programmable-flow-protection/
author: ''
summary: Cloudflare宣布推出可编程流量防护测试版，专为Magic Transit企业客户设计。该系统允许客户编写自定义eBPF程序，定义基于UDP的自有或专有协议的“好”与“坏”流量规则，并部署在Cloudflare全球网络上执行。这解决了传统DDoS防护对未知UDP协议只能采取粗粒度拦截或速率限制的痛点，实现了更精准、有状态的攻击缓解，同时不影响现有标准防护措施。
categories:
- AI基础设施
tags:
- DDoS防护
- Cloudflare
- 网络安全
- eBPF
- UDP协议
draft: false
translated_at: '2026-04-01T05:17:08.467448'
---

# 推出可编程流量防护：为Magic Transit客户提供定制化DDoS缓解逻辑

2026-03-31

- Anita Tenjarla
- Alex Forster
- Cody Doucette
- Venus Xeon-Blonde

![](/images/posts/019313db49fa.png)

我们自豪地推出**可编程流量防护**：这是一个旨在让**Magic Transit**客户实施其自定义DDoS缓解逻辑，并将其部署在Cloudflare全球网络上的系统。它能为基于UDP构建的自定义和专有协议提供精确的、有状态的缓解措施。该系统经过精心设计，旨在提供最高级别的定制化和灵活性，以缓解任何规模的DDoS攻击。

可编程流量防护目前处于测试阶段，所有Magic Transit企业客户均可额外付费使用。

### 可编程流量防护是可定制的

我们现有的**DDoS缓解系统**旨在理解和保护流行、广为人知的协议免受DDoS攻击。例如，我们的**高级TCP保护**系统利用TCP协议的特定已知特性来发起质询并验证客户端的合法性。同样，我们的**高级DNS保护**会为每个客户建立DNS查询档案，以缓解DNS攻击。我们的通用DDoS缓解平台也能理解各种其他知名协议（包括NTP、RDP、SIP等）的常见模式。

然而，自定义或专有的UDP协议一直是Cloudflare DDoS缓解系统面临的挑战，因为我们的系统缺乏相关的协议知识来做出智能决策以放行或丢弃流量。

可编程流量防护解决了这一空白。现在，客户可以编写自己的**eBPF**程序，定义什么是“好”数据包和“坏”数据包，以及如何处理它们。然后，Cloudflare会在我们的整个全球网络上运行该程序。该程序可以选择丢弃或质询“坏”数据包，防止它们到达客户的源站。

### 基于UDP的攻击问题

**UDP**是一种无连接的传输层协议。与TCP不同，UDP没有握手或有状态连接。它不保证数据包会按序到达或仅到达一次。UDP优先考虑速度和简单性，因此非常适用于在线游戏、VoIP、视频流以及任何需要在客户端和服务器之间进行实时通信的应用场景。

我们的DDoS缓解系统一直能够检测和缓解针对基于UDP构建的知名协议的攻击。例如，标准的DNS协议构建在UDP之上，每个DNS数据包都有众所周知的结构。如果我们看到一个DNS数据包，我们知道如何解析它。这使得我们更容易检测和丢弃基于DNS的攻击。

不幸的是，如果我们不理解UDP数据包载荷内的协议，我们的DDoS缓解系统在缓解时可用的选项就非常有限。如果攻击者**发送大量UDP流量**，而这些流量不匹配任何已知模式或协议，Cloudflare要么完全阻止目标IP和端口的组合，要么对其应用速率限制。这是一种粗糙的“最后防线”，仅旨在保持客户网络的其余部分在线，并且它可能在几个方面带来困扰。

首先，阻止或通用的**速率限制**无法区分正常流量和恶意流量，这意味着这些缓解措施很可能会导致合法客户端经历延迟或连接丢失——这相当于替攻击者完成了他们的工作！其次，通用的速率限制可能过于严格或过于宽松，具体取决于客户。例如，一个预期接收1Gbps合法流量的客户，与一个预期接收25Gbps合法流量的客户相比，可能需要更严格的速率限制。

UDP数据包内容示意图。用户可以定义有效载荷，并拒绝不符合定义模式的流量。

可编程流量防护平台就是为了解决这个问题而构建的，它允许我们的客户定义什么是“好”流量，什么是“坏”流量。我们的许多客户使用我们不了解的自定义或专有UDP协议——而现在我们不需要了解了。

### 可编程流量防护的工作原理

在之前的博客文章中，我们描述了“flowtrackd”（我们的**有状态网络层DDoS缓解系统**）如何保护Magic Transit用户免受复杂的TCP和DNS攻击。我们还描述了我们如何使用**XDP**和**eBPF**等Linux技术来有效缓解常见类型的大规模DDoS攻击。

可编程流量防护以一种新颖的方式结合了这些技术。借助可编程流量防护，客户可以编写自己的eBPF程序，根据任意逻辑决定是放行、丢弃还是质询单个数据包。客户可以将程序上传到Cloudflare，Cloudflare将在发往其网络的每个数据包上执行该程序。程序在用户空间而非内核空间执行，这使得Cloudflare能够灵活地在平台上支持各种客户和用例，同时不损害安全性。可编程流量防护程序在Cloudflare所有现有DDoS缓解措施之后运行，因此用户仍能受益于我们的标准安全保护。

加载到Linux内核中的XDP eBPF程序与在可编程流量防护平台上运行的eBPF程序有许多相似之处。两种类型的程序都被编译成BPF字节码。它们都会经过一个“验证器”以确保内存安全并验证程序终止。它们也在一个快速、轻量级的虚拟机中执行，以提供隔离性和稳定性。

然而，加载到Linux内核中的eBPF程序利用了许多Linux特有的“辅助函数”来与网络栈集成、在程序执行之间维护状态以及向网络设备发送数据包。可编程流量防护在客户选择时提供相同的功能，但使用专门为实施DDoS缓解而定制的不同API。例如，我们构建了辅助函数来存储程序执行之间关于客户端的状态、执行加密验证以及向客户端发送质询数据包。借助这些辅助函数，开发人员可以利用Cloudflare平台的力量来保护自己的网络。

### 将客户知识与Cloudflare网络相结合

让我们通过一个示例来说明如何将客户的协议特定知识与Cloudflare的网络相结合，以创建强大的缓解措施。

假设一个客户在UDP端口207上托管一个在线游戏服务器。游戏引擎使用特定于该游戏的专有应用头部。Cloudflare不了解该应用头部的结构或内容。客户遭受DDoS攻击，导致游戏服务器不堪重负，玩家报告游戏延迟。攻击流量来自高度随机的源IP和端口，载荷数据也似乎是随机的。

为了缓解攻击，客户可以利用他们对应用头部的了解，部署一个可编程流量防护程序来检查数据包的有效性。在这个例子中，应用头部包含一个特定于游戏协议的令牌。因此，客户可以编写一个程序来提取令牌的最后一个字节。该程序放行所有包含正确值的数据包，并丢弃所有其他流量：

```C
#include <linux/ip.h>
#include <linux/udp.h>
#include <arpa/inet.h>

#include "cf_ebpf_defs.h"
#include "cf_ebpf_helper.h"

// 自定义应用头部
struct apphdr {
    uint8_t  version;
    uint16_t length;   // 可变长度令牌的长度
    uint8_t  token[0]; // 可变长度令牌
} __attribute__((packed));

uint64_t
cf_ebpf_main(void *state)
{
    struct cf_ebpf_generic_ctx *ctx = state;
    struct cf_ebpf_parsed_headers headers;
    struct cf_ebpf_packet_data *p;

    // 使用提供的辅助函数解析数据包头
    if (parse_packet_data(ctx, &p, &headers) != 0) {
        return CF_EBPF_DROP;
    }

    // 丢弃目标端口不是 207 的数据包
    struct udphdr *udp_hdr = (struct udphdr *)headers.udp;
    if (ntohs(udp_hdr->dest) != 207) {
        return CF_EBPF_DROP;
    }

    // 从 UDP 载荷中获取应用层头部
    struct apphdr *app = (struct apphdr *)(udp_hdr + 1);
    if ((uint8_t *)(app + 1) > headers.data_end) {
        return CF_EBPF_DROP;
    }

    // 执行内存检查以满足验证器要求
    // 并安全地访问令牌
    if ((uint8_t *)(app->token + token_len) > headers.data_end) {
        return CF_EBPF_DROP;
    }

    // 检查令牌的最后一个字节是否符合预期值
    uint8_t *last_byte = app->token + token_len - 1;
    if (*last_byte != 0xCF) {
        return CF_EBPF_DROP;
    }

    return CF_EBPF_PASS;
}
```

一个根据应用层头部中的值来过滤数据包的 eBPF 程序。

该程序利用应用特定的信息，创建比 Cloudflare 自身所能构建的更精准的缓解措施。客户现在可以将其专有知识与 Cloudflare 全球网络的能力相结合，以前所未有的方式更好地吸收和缓解大规模攻击。

### 超越防火墙：有状态跟踪与质询

许多模式检查，例如上例中执行的那种，可以通过传统防火墙完成。然而，程序提供了防火墙所不具备的有用原语，包括变量、条件执行、循环和过程调用。但真正使可编程流量保护区别于其他解决方案的，是其有状态跟踪流量的能力以及对客户端进行质询以证明其真实性的能力。重放攻击是一种能展示这些能力的常见攻击类型。

在重放攻击中，攻击者重复发送在某个时间点有效、因此符合流量预期模式的数据包，但这些数据包在应用程序的当前上下文中已不再有效。例如，攻击者可以记录一些他们有效的游戏流量，并使用脚本以极高的速率复制和发送相同的流量。

借助可编程流量保护，用户可以部署一个程序来质询可疑客户端并丢弃脚本化的流量。我们可以如下扩展我们最初的示例：

```C++

#include <linux/ip.h>
#include <linux/udp.h>
#include <arpa/inet.h>

#include "cf_ebpf_defs.h"
#include "cf_ebpf_helper.h"

uint64_t
cf_ebpf_main(void *state)
{
    // ...
 
    // 获取此源 IP 的状态（有状态跟踪）
    uint8_t status;
    if (cf_ebpf_get_source_ip_status(&status) != 0) {
        return CF_EBPF_DROP;
    }

    switch (status) {
        case NONE:
		// 向此源 IP 发出自定义质询
             issue_challenge();
             cf_ebpf_set_source_ip_status(CHALLENGED);
             return CF_EBPF_DROP;


        case CHALLENGED:
		// 检查此数据包是否通过质询
		// 使用自定义逻辑
             if (verify_challenge()) {
                 cf_ebpf_set_source_ip_status(VERIFIED);
                 return CF_EBPF_PASS;
             } else {
                 cf_ebpf_set_source_ip_status(BLOCKED);
                 return CF_EBPF_DROP;
             }


        case VERIFIED:
		// 此源 IP 已通过质询
		return CF_EBPF_PASS;

	 case BLOCKED:
		// 此源 IP 已被阻止
		return CF_EBPF_DROP;

        default:
            return CF_EBPF_PASS;
    }


    return CF_EBPF_PASS;
}

```

一个用于质询 UDP 连接并有状态管理连接的 eBPF 程序。此示例已为说明目的进行了简化。

该程序有状态地跟踪它见过的源 IP 地址，并向未知客户端发送一个包含加密质询的数据包。运行有效游戏客户端的合法客户端能够正确解答质询并返回证明，但攻击者的脚本则不能。来自攻击者的流量被标记为“已阻止”，后续数据包将被丢弃。

借助这些新能力，客户可以有状态地跟踪流量，并确保只有真实、经过验证的客户端才能向他们的源服务器发送流量。尽管我们的示例侧重于游戏，但这项技术的潜在用例可以扩展到任何基于 UDP 的协议。

### 立即开始使用

我们很高兴能为 Magic Transit Enterprise 客户提供可编程流量保护功能。请联系您的客户经理，详细了解如何启用可编程流量保护来帮助保护您的基础设施。

我们仍在积极开发该平台，并期待看到用户接下来会构建什么。如果您还不是 Cloudflare 客户，请告知我们您是否有兴趣使用 Cloudflare 来保护您的网络。加入我们的可编程流量保护 Discord 频道，与我们讨论此功能。

---

> 本文由AI自动翻译，原文链接：[Introducing Programmable Flow Protection: custom DDoS mitigation logic for Magic Transit customers](https://blog.cloudflare.com/programmable-flow-protection/)
> 
> 翻译时间：2026-04-01 05:17
