---
title: Cloudflare IPsec后量子加密全面可用
title_original: Post-quantum encryption for Cloudflare IPsec is generally available
date: '2026-04-30'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/post-quantum-ipsec/
author: ''
summary: Cloudflare宣布其IPsec产品中的后量子加密功能已全面可用，基于IETF混合ML-KEM标准，旨在抵御“先收后解”攻击。该实现已与Cisco和Fortinet等厂商的设备成功互操作，使企业能利用现有硬件保护广域网。文章还探讨了IPsec后量子加密比TLS晚落地的原因，以及行业如何围绕可互操作标准达成共识，以应对量子计算威胁。
categories:
- AI基础设施
tags:
- 后量子加密
- IPsec
- ML-KEM
- Cloudflare
- 网络安全
draft: false
translated_at: '2026-05-01T05:45:40.387942'
---

# Cloudflare IPsec 的后量子加密现已全面可用

2026-04-30

- Sharon Goldberg
- Amos Paul

![](/images/posts/453826352398.png)

虽然超过三分之二流向 Cloudflare 的人类生成的 TLS 流量已受到后量子密码学保护，但站点到站点网络领域的情况却截然不同。多年来，IPsec 社区一直处于互联网规模互操作性的高标准与专用硬件的特定需求之间的两难境地。这一差距如今正在缩小。

本月早些时候，我们宣布，受量子计算近期多项进展的推动，Cloudflare 已将其全面实现后量子安全的目标提前至 2029 年。为推进这一目标，我们已使 Cloudflare IPsec 中的后量子加密全面可用。

利用新的 IETF 混合 ML-KEM（FIPS 203）草案，我们已成功测试了与 Fortinet 和 Cisco 分支连接器的互操作性——这意味着您现在就可以使用已有的硬件，开始保护您的广域网（WAN）免受"先收后解"攻击。

本文解释了我们是如实现新的混合 IPsec 握手的，为何它比 TLS 对应方案晚了四年才落地，以及行业如何最终围绕一个可在互联网规模运行的标准化方案达成共识。

### Cloudflare IPsec

Cloudflare IPsec 是一种 WAN 网络即服务，通过将数据中心、分支机构和云 VPC 连接到 Cloudflare 的全球 IP Anycast 网络，取代传统网络架构。客户可获得简化的配置、高可用性（如果某个数据中心不可用，流量会自动重新路由到最近的健康节点），以及 Cloudflare 全球网络的规模优势。这是通过支持站点到站点 WAN、出站互联网连接以及与 Cloudflare One SASE 平台连接的加密 IPsec 隧道实现的。

### IPsec 中的后量子加密

Cloudflare IPsec 现在使用混合 ML-KEM（FIPS 203）实现后量子加密，以阻止"先收后解"攻击。这类攻击中，攻击者先收集数据，然后在 Q-Day 之后，当有强大的量子计算机能够破解互联网上使用的经典公钥密码学时再进行解密。随着 Q-Day 的到来比预期更快，"先收后解"攻击正成为越来越多组织关注的问题。

ML-KEM（基于模格的密钥封装机制）是一种后量子密码学算法，其数学假设目前已知不受量子计算机攻击的影响。它不需要特殊硬件或发送方与接收方之间的专用物理链路。ML-KEM 特意设计为可在标准处理器上通过软件实现，为网络流量提供后量子加密。

Draft-ietf-ipsecme-ikev2-mlkem 规定了使用混合 ML-KEM 的 IPsec 后量子加密，该方案将经典 Diffie-Hellman 的成熟安全性与 ML-KEM 的后量子安全性结合在单一、符合标准的握手中。具体来说，先运行经典 Diffie-Hellman 交换，其派生密钥加密运行 ML-KEM 的第二次交换，两者的输出混合到会话密钥中，用于保护使用封装安全载荷（ESP）协议发送的 IPsec 数据平面流量。

### 我们的可互操作实现

此前我们宣布了在 Cloudflare IPsec 产品生产环境中对 draft-ietf-ipsecme-ikev2-mlkem 实现的封闭测试版，并针对参考实现（strongswan）进行了测试。现在，我们已使该实现全面可用，并确认了与包括 Cisco 和 Fortinet 在内的多家其他供应商的互操作性，这对这一新标准来说是一个重大胜利。

**Cisco：** 使用 Cisco 8000 系列安全路由器（版本 26.1.1 及更高版本）作为分支连接器的客户，现在也可以根据 draft-ietf-ipsecme-ikev2-mlkem 建立后量子 Cloudflare IPsec 隧道。

**Fortinet：** 使用 Fortinet FortiOS 7.6.6 及更高版本作为分支连接器的客户，现在可以根据 draft-ietf-ipsecme-ikev2-mlkem 建立到 Cloudflare 全球网络的后量子 Cloudflare IPsec 隧道。

### 互操作性的重要性

鉴于升级密码学很困难且可能需要数年时间，我们 2029 年全面更新至后量子密码学的目标需要集中努力。这就是为什么我们希望 IPsec 社区继续专注于开发如 draft-ietf-ipsecme-ikev2-mlkem 这样的可互操作标准。

让我们解释一下这些标准为何至关重要。IPsec 中混合 ML-KEM 的完整规范 draft-ietf-ipsecme-ikev2-mlkem 直到 2025 年底才可用。这大约比 TLS 中支持混合 ML-KEM 晚了四年。（事实上，Cloudflare 早在 2022 年就在 TLS 中启用了混合后量子密钥协商，甚至在 NIST 最终确定 ML-KEM 标准化之前，因为 TLS 社区迅速就单一、可互操作的方法达成共识并将其投入生产。如今，超过三分之二流向 Cloudflare 网络的人类生成的 TLS 流量都受到混合 ML-KEM 的保护。）

这四年的延迟部分可能归因于 IPsec 社区对量子密钥分发（QKD）的持续兴趣，如 2020 年发布的 RFC 8784 所规定。我们此前曾撰文解释为何 QKD 不是我们后量子战略的一部分：QKD 需要专用硬件和双方之间的专用物理链路，这从根本上意味着它无法在互联网规模运行。此外，QKD 不提供身份验证，因此您仍然需要后量子密码学来阻止主动攻击者。很难找到跨供应商可互操作的 QKD 实现。

美国 NSA、德国 BSI 和英国 NCSC 都警告不要仅依赖 QKD。相比之下，后量子密码学可在您已有的硬件上运行，对两端进行身份验证，并在互联网上端到端工作。

2023 年发布的 RFC 9370 为 IPsec 中的后量子密码学打开了大门，允许最多七个密钥交换与经典 Diffie-Hellman 并行运行。然而，RFC 9370 并未指定这些并行密钥交换中应使用哪些密码套件。在缺乏该规范的情况下，一些供应商在混合 ML-KEM 草案可用之前就根据 RFC 9370 发布了早期实现，定义了自己的密码套件，其中一些并非 NIST 标准化。这正是 NIST SP 800 52r2 所警告的"密码套件膨胀"。对互操作性的风险已在实践中显现：Cloudflare IPsec 尚未与 Palo Alto Networks 基于 RFC 9370 的实现实现互操作，因为该实现是在 draft-ietf-ipsecme-ikev2-mlkem 可用之前推出的。

幸运的是，我们现在有了 draft-ietf-ipsecme-ikev2-mlkem，它填补了 RFC 9370 的空白，将混合 ML-KEM 指定为可与经典 Diffie-Hellman 并行运行的密钥交换机制之一。随着行业继续围绕 draft-ietf-ipsecme-ikev2-mlkem 整合，我们希望将 Palo Alto Networks 添加到可互操作的后量子分支连接器列表中。

但实现可互操作的后量子 IPsec 标准的旅程尚未结束。虽然 draft-ietf-ipsecme-ikev2-mlkem 支持后量子加密，我们仍然需要用于后量子身份验证的 IPsec 标准，以便在 Q-Day 之后阻止量子对手对实时系统的攻击。鉴于全面后量子就绪的时间表缩短，我们希望 IPsec 社区继续专注于可互操作的 PQC 实现，而不是将注意力转移到 QKD 的特定用例上。

### 迈向可互操作的后量子互联网

在Cloudflare，我们致力于让每个人都能访问安全且后量子化的互联网，无需专用硬件，且不向客户收取额外费用。后量子化Cloudflare IPsec是我们迈向2029年实现全面后量子化安全道路上的又一步，我们正以确保持互联网在未来多年保持开放和互操作性的方式推进这一目标。

---

> 本文由AI自动翻译，原文链接：[Post-quantum encryption for Cloudflare IPsec is generally available](https://blog.cloudflare.com/post-quantum-ipsec/)
> 
> 翻译时间：2026-05-01 05:45
