---
title: 构建无服务器、后量子安全的Matrix主服务器
title_original: Building a serverless, post-quantum Matrix homeserver
date: '2026-01-27'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/serverless-matrix-homeserver-workers/
author: ''
summary: 本文探讨如何将传统的Matrix主服务器从基于Python的Synapse架构移植到Cloudflare Workers无服务器平台。通过使用Durable
  Objects、D1、KV和R2等云原生服务替代PostgreSQL、Redis和文件存储，实现了运维简化、按需付费、全球低延迟和内置安全防护。特别指出，该架构默认启用后量子混合加密（X25519MLKEM768），为通信提供抗量子计算攻击的保护。文章强调这是一种概念验证，展示了去中心化通信系统在无服务器环境下的可行性与优势。
categories:
- AI基础设施
tags:
- 无服务器计算
- 后量子密码学
- Matrix协议
- Cloudflare Workers
- 去中心化通信
draft: false
translated_at: '2026-01-28T04:42:50.649636'
---

# 构建无服务器、后量子时代的 Matrix 主服务器

2026-01-27

- Nick Kuntz

![](/images/posts/dac02d2ad596.png)

*本文已于太平洋时间上午 11:45 更新，以澄清此处描述的使用场景是一个概念验证和个人项目。部分章节已更新以提高清晰度。

Matrix 是去中心化、端到端加密通信的黄金标准。它为全球的政府消息系统、开源社区和注重隐私的组织提供支持。

然而，对于个人开发者而言，其吸引力往往更贴近实际需求：将分散的聊天网络（如 Discord 和 Slack）桥接到一个统一的收件箱，或者仅仅是确保您的对话历史记录保存在您自己控制的基础设施上。从功能上讲，Matrix 作为一个去中心化、最终一致的状态机运行。它没有中央服务器推送更新，而是主服务器通过 HTTP 交换经过签名的 JSON 事件，并使用冲突解决算法将这些事件流合并为房间历史的统一视图。

但运行它需要付出“代价”。传统上，运营一个 Matrix 主服务器意味着要承担沉重的运维负担。您必须配置虚拟专用服务器（VPS），针对高写入负载优化 PostgreSQL，管理用于缓存的 Redis，配置反向代理，并处理 TLS 证书的轮换。它是一个有状态的、沉重的庞然大物，无论您使用得多还是少，都需要投入时间和金钱。

我们想看看是否能完全消除这种代价。

剧透：我们做到了。在这篇文章中，我们将解释如何将 Matrix 主服务器移植到 Cloudflare Workers。最终的概念验证是一个无服务器架构，其中运维工作消失，空闲时成本降至零，并且默认情况下每个连接都受到后量子密码学的保护。您可以查看源代码并直接从 Github 部署您自己的实例。

从Synapse到Workers
我们的起点是Synapse，这是一个基于Python的Matrix家庭服务器参考实现，专为传统部署设计。它使用PostgreSQL进行持久化存储，Redis用于缓存，文件系统用于媒体存储。

将其移植到Workers意味着我们需要重新审视所有曾被视为理所当然的存储假设。核心挑战在于存储。传统的家庭服务器通过中心化的SQL数据库来保证强一致性。Cloudflare的Durable Objects提供了一个强大的替代方案。这个原语为我们提供了Matrix状态解析所需的强一致性和原子性，同时仍允许应用程序在边缘运行。

我们使用Hono框架，将核心Matrix协议逻辑——事件授权、房间状态解析、加密验证——用TypeScript进行了移植。D1替代了PostgreSQL，KV替代了Redis，R2替代了文件系统，而Durable Objects则负责实时协调。

以下是映射关系：

从单体架构到无服务器架构
迁移到Cloudflare Workers为开发者带来了几个优势：部署简单、成本更低、延迟更低以及内置安全性。

**简单部署**：传统的Matrix部署需要服务器配置、PostgreSQL管理、Redis集群管理、TLS证书续订、负载均衡器配置、监控基础设施和值班轮换。使用Workers，部署只需一条命令：`wrangler deploy`。Workers处理TLS、负载均衡、DDoS防护和全球分发。

**基于使用量的成本**：传统的家庭服务器无论是否有人使用都会产生费用。Workers的定价基于请求，因此您在使用时才付费，而当所有人都休息时，成本会降至接近零。

**全球低延迟**：一个位于us-east-1的传统Matrix家庭服务器会给亚洲或欧洲的用户增加200毫秒以上的延迟。而Workers在全球300多个地点运行。当东京的用户发送消息时，Worker就在东京执行。

**内置安全性**：Matrix家庭服务器可能是高价值目标：它们处理加密通信、存储消息历史记录并验证用户身份。传统部署需要仔细加固：防火墙配置、速率限制、DDoS缓解、WAF规则、IP信誉过滤。Workers默认提供了所有这些功能。

**后量子保护**
Cloudflare于2022年10月在所有TLS 1.3连接上部署了后量子混合密钥协商。连接到我们Worker的每个连接都会自动协商X25519MLKEM768——这是一种混合方案，结合了经典的X25519和NIST标准化的后量子算法ML-KEM。

经典密码学依赖于对传统计算机来说困难但对运行Shor算法的量子计算机来说简单的数学问题。ML-KEM基于即使在量子计算机面前也依然困难的格问题。混合方法意味着两种算法都必须失效，连接才会被攻破。

**追踪消息在系统中的路径**
了解加密发生在何处对于安全架构至关重要。当有人通过我们的家庭服务器发送消息时，实际路径如下：

发送者的客户端获取明文消息，并使用Megolm——Matrix的端到端加密——对其进行加密。然后，这个加密的有效载荷被包裹在TLS中进行传输。在Cloudflare上，该TLS连接使用X25519MLKEM768，使其具有抗量子性。

Worker终止TLS连接，但它接收到的仍然是加密的——即Megolm密文。我们将该密文存储在D1中，按房间和时间戳建立索引，并将其传递给接收者。但我们从未看到明文。消息"Hello, world"仅存在于发送者的设备和接收者的设备上。

当接收者同步时，过程逆转。他们通过另一个抗量子的TLS连接接收加密的有效载荷，然后使用其Megolm会话密钥在本地解密。

**两层独立保护**
这通过两个独立运行的加密层提供保护：

*   **传输层（TLS）** 保护传输中的数据。它在客户端加密，在Cloudflare边缘解密。使用X25519MLKEM768后，这一层现在具有后量子安全性。
*   **应用层（Megolm E2EE）** 保护消息内容。它在发送者的设备上加密，仅在接收者的设备上解密。这使用经典的Curve25519密码学。

**谁能看到什么**
任何Matrix家庭服务器运营商——无论是在VPS上运行Synapse，还是在Workers上运行此实现——都可以看到元数据：存在哪些房间、谁在房间里、消息何时发送。但基础设施链中的任何人都无法看到消息内容，因为端到端加密的有效载荷在发送者设备上就已加密，然后才进入网络。Cloudflare终止TLS连接并将请求传递给您的Worker，但两者都只能看到Megolm密文。加密房间中的媒体在上传前已在客户端加密，私钥永远不会离开用户设备。

**传统部署需要什么**
在传统的Matrix部署上实现后量子TLS，需要将OpenSSL或BoringSSL升级到支持ML-KEM的版本，正确配置密码套件偏好，测试所有Matrix应用的客户端兼容性，监控TLS协商失败，随着PQC标准的发展保持更新，并妥善处理不支持PQC的客户端。

而对于Workers，这一切都是自动的。Chrome、Firefox和Edge都支持X25519MLKEM768。使用平台TLS堆栈的移动应用也继承了这种支持。随着Cloudflare的PQC部署扩展，安全态势会自动提升——我们无需采取任何行动。

**使其成为可能的存储架构**
移植Tuwunel的一个关键见解是：不同的数据需要不同的一致性保证。我们根据各自优势使用每个Cloudflare原语。

**D1用于数据模型**
D1存储所有需要在重启后保留并支持查询的数据：用户、房间、事件、设备密钥。超过25张表覆盖了完整的Matrix数据模型。

```sql
CREATE TABLE events (
	event_id TEXT PRIMARY KEY,
	room_id TEXT NOT NULL,
	sender TEXT NOT NULL,
	event_type TEXT NOT NULL,
	state_key TEXT,
	content TEXT NOT NULL,
	origin_server_ts INTEGER NOT NULL,
	depth INTEGER NOT NULL
);
```

D1基于SQLite，这意味着我们可以用最少的改动移植Tuwunel的查询。连接、索引和聚合都按预期工作。

我们吸取了一个深刻的教训：D1的最终一致性破坏了外键约束。在写入`events`表并检查外键时，之前对`rooms`表的写入可能还不可见。我们移除了所有外键，并在应用程序代码中强制执行引用完整性。

**KV用于临时状态**
OAuth授权码存活10分钟，而刷新令牌则持续一个会话。

```javascript
// Store OAuth code with 10-minute TTL
kv.put(&format!("oauth_code:{}", code), &token_data)?
	.expiration_ttl(600)
	.execute()
	.await?;
```

KV的全球分发意味着无论用户身在何处，OAuth流程都能快速工作。

**R2用于媒体**
Matrix媒体直接映射到R2，因此您可以上传一张图片，获得一个内容寻址的URL——并且出口流量是免费的。

**Durable Objects用于原子性**
有些操作无法容忍最终一致性。当客户端认领一个一次性加密密钥时，该密钥必须被原子性地移除。如果两个客户端认领了同一个密钥，加密会话建立就会失败。

Durable Objects提供了单线程、强一致性的存储：

```rust
#[durable_object]
pub struct UserKeysObject {
	state: State,
	env: Env,
}

impl UserKeysObject {
	async fn claim_otk(&self, algorithm: &str) -> Result<Option<Key>> {
    	// 在单个DO内原子操作 - 不可能出现竞态条件
    	let mut keys: Vec<Key> = self.state.storage()
        	.get("one_time_keys")
        	.await
        	.ok()
        	.flatten()
        	.unwrap_or_default();
```

```rust
if let Some(idx) = keys.iter().position(|k| k.algorithm == algorithm) {
        let key = keys.remove(idx);
        self.state.storage().put("one_time_keys", &keys).await?;
        return Ok(Some(key));
    }
    Ok(None)
}
```
我们使用 `UserKeysObject` 进行端到端加密密钥管理，使用 `RoomObject` 处理实时房间事件（如输入指示器和已读回执），使用 `UserSyncObject` 处理设备间消息队列。其余数据流则通过 D1 处理。

**完整的端到端加密，完整的 OAuth**
我们的实现支持完整的 Matrix 端到端加密栈：设备密钥、交叉签名密钥、一次性密钥、备用密钥、密钥备份以及脱水设备。
现代 Matrix 客户端使用 OAuth 2.0/OIDC，而非传统的密码流程。我们实现了一个完整的 OAuth 提供程序，支持动态客户端注册、PKCE 授权、RS256 签名的 JWT 令牌、支持轮换的令牌刷新以及标准的 OIDC 发现端点。
```bash
curl https://matrix.example.com/.well-known/openid-configuration
```
```json
{
  "issuer": "https://matrix.example.com",
  "authorization_endpoint": "https://matrix.example.com/oauth/authorize",
  "token_endpoint": "https://matrix.example.com/oauth/token",
  "jwks_uri": "https://matrix.example.com/.well-known/jwks.json"
}
```
将 Element 或任何 Matrix 客户端指向该域名，它将自动发现一切。

**面向移动端的滑动同步**
传统的 Matrix 同步在初始连接时会传输数兆字节的数据，消耗移动设备的电量和数据流量。
滑动同步允许客户端精确请求所需内容。客户端无需下载所有内容，而是获取最近 20 个房间及其最小状态。当用户滚动时，他们请求更多范围的数据。服务器跟踪位置并仅发送增量数据。
结合边缘执行，即使在网络缓慢的情况下，移动客户端也能在 500 毫秒内连接并渲染其房间列表。

**对比**
对于一个服务于小型团队的家服务器：
| 项目 | 传统（VPS） | Workers |
| :--- | :--- | :--- |
| 月度成本（闲置） | $20-50 | <$1 |
| 月度成本（活跃） | $20-50 | $3-10 |
| 全球延迟 | 100-300ms | 20-50ms |
| 部署时间 | 数小时 | 数秒 |
| 维护 | 每周 | 无 |
| DDoS 防护 | 额外成本 | 已包含 |
| 后量子 TLS | 复杂设置 | 自动* |
*基于截至 2026 年 1 月 15 日 DigitalOcean、AWS Lightsail 和 Linode 公布的公开费率和指标。

随着规模扩大，经济效益会进一步提升。传统部署需要进行容量规划和过度配置。Workers 可自动扩展。

**去中心化协议的未来**
我们最初将此作为一个实验：Matrix 能否在 Workers 上运行？答案是肯定的——而且这种方法也适用于其他有状态的协议。
通过将有状态的传统组件映射到 Cloudflare 的原语——Postgres 到 D1，Redis 到 KV，互斥锁到 Durable Objects——我们可以看到，复杂的应用程序并不需要复杂的基础设施。我们剥离了操作系统、数据库管理和网络配置，只留下应用程序逻辑和数据本身。
Workers 提供了拥有数据的主权，而无需承担拥有基础设施的负担。
我一直在尝试实现，并期待对此类服务感兴趣的其他人的任何贡献。
准备好基于 Workers 构建强大的实时应用程序了吗？从 [Cloudflare Workers](https://workers.cloudflare.com) 开始，并探索 [Durable Objects](https://developers.cloudflare.com/durable-objects) 来构建你自己的有状态边缘应用程序。加入我们的 [Discord 社区](https://discord.cloudflare.com)，与在边缘构建的其他开发者建立联系。

## 从 Synapse 到 Workers

我们的起点是 **Synapse**，这是一个基于 Python 的 Matrix 家服务器参考实现，专为传统部署设计。它使用 PostgreSQL 进行持久化存储，Redis 用于缓存，文件系统用于媒体存储。
将其移植到 Workers 意味着我们需要重新审视所有我们曾视为理所当然的存储假设。
挑战在于存储。传统的家服务器假设通过中心化的 SQL 数据库实现强一致性。Cloudflare 的 **Durable Objects** 提供了一个强大的替代方案。这个原语为我们提供了 Matrix 状态解析所需的强一致性和原子性，同时仍允许应用程序在边缘运行。
我们使用 Hono 框架，将核心的 Matrix 协议逻辑——事件授权、房间状态解析、加密验证——用 TypeScript 进行了移植。D1 替代了 PostgreSQL，KV 替代了 Redis，R2 替代了文件系统，而 Durable Objects 则处理实时协调。
以下是映射的实现方式：

## 从单体架构到无服务器架构

迁移到 Cloudflare Workers 为开发者带来了几个优势：部署简单、成本更低、延迟更低以及内置安全性。

**轻松部署**：传统的 Matrix 部署需要服务器配置、PostgreSQL 管理、Redis 集群管理、TLS 证书续订、负载均衡器配置、监控基础设施和值班轮换。
使用 Workers，部署只需：`wrangler deploy`。Workers 处理 TLS、负载均衡、DDoS 防护和全球分发。

**基于使用量的成本**：无论是否有人使用，传统的家服务器都会产生费用。Workers 的定价基于请求，因此您在使用时才付费，而当所有人都休息时，成本会降至接近零。

**更低的全球延迟**：位于 us-east-1 的传统 Matrix 家服务器会给亚洲或欧洲的用户增加 200 毫秒以上的延迟。而 Workers 在全球 300 多个地点运行。当东京的用户发送消息时，Worker 就在东京执行。

**内置安全性**：Matrix 家服务器可能是高价值目标：它们处理加密通信、存储消息历史记录并验证用户身份。传统部署需要仔细加固：防火墙配置、速率限制、DDoS 缓解、WAF 规则、IP 信誉过滤。
Workers 默认提供所有这些功能。

### 后量子保护
Cloudflare 于 **2022 年 10 月** 在所有 **TLS 1.3** 连接上部署了后量子混合密钥协商。连接到我们 Worker 的每个连接都会自动协商 X25519MLKEM768——这是一种混合方案，结合了经典的 X25519 和 ML-KEM（NIST 标准化的后量子算法）。
经典密码学依赖于对传统计算机来说困难但对运行 Shor 算法的量子计算机来说简单的数学问题。ML-KEM 基于即使在量子计算机面前也依然困难的格问题。混合方法意味着两种算法都必须失效，连接才会被攻破。

### 追踪消息在系统中的路径

理解加密发生在何处对于安全架构至关重要。当有人通过我们的家服务器发送消息时，以下是实际的路径：
发送者的客户端获取明文消息，并使用 Megolm——Matrix 的端到端加密——对其进行加密。然后，这个加密的有效载荷被包装在 TLS 中进行传输。在 Cloudflare 上，该 TLS 连接使用 X25519MLKEM768，使其具有抗量子性。
Worker 终止 TLS 连接，但它接收到的仍然是加密的——即 Megolm 密文。我们将该密文存储在 D1 中，按房间和时间戳建立索引，并将其传递给接收者。但我们从未看到明文。消息 "Hello, world" 仅存在于发送者的设备和接收者的设备上。
当接收者同步时，过程逆转。他们通过另一个抗量子的 TLS 连接接收加密的有效载荷，然后使用其 Megolm 会话密钥在本地解密。

### 两层独立保护

这通过两个独立运行的加密层提供保护：
*   **传输层** 保护传输中的数据。它在客户端加密，在 Cloudflare 边缘解密。使用 X25519MLKEM768，这一层现在具有后量子安全性。
*   **应用层** 保护消息内容。它在发送者的设备上加密，仅在接收者的设备上解密。这使用经典的 Curve25519 密码学。

### 谁能看到什么

任何Matrix家庭服务器运营商——无论是在VPS上运行Synapse，还是在Workers上运行此实现——都能看到元数据：存在哪些房间、房间内有哪些成员、消息的发送时间。但基础设施链中的任何人都无法看到消息内容，因为端到端加密（E2EE）的有效载荷在发送方设备上就已加密，然后才进入网络。Cloudflare会终止TLS连接并将请求传递给你的Worker，但两者都只能看到Megolm密文。加密房间中的媒体在上传前已在客户端加密，私钥永远不会离开用户设备。

### 传统部署所需的条件

在传统的Matrix部署中实现后量子TLS，需要将OpenSSL或BoringSSL升级到支持ML-KEM的版本，正确配置密码套件偏好，测试所有Matrix应用的客户端兼容性，监控TLS协商失败，随着后量子密码（PQC）标准的发展保持更新，并妥善处理不支持PQC的客户端。

而在Workers上，这一切都是自动的。Chrome、Firefox和Edge都支持X25519MLKEM768。使用平台TLS堆栈的移动应用也继承了此支持。随着Cloudflare后量子密码部署的扩展，安全态势会自动提升——我们无需采取任何行动。

## 使其成为可能的存储架构

移植Tuwunel带来的关键洞见是：不同的数据需要不同的一致性保证。我们让每个Cloudflare原语各司其职。

### D1用于数据模型

D1存储所有需要在重启后持久存在并支持查询的数据：用户、房间、事件、设备密钥。超过25张表，覆盖完整的Matrix数据模型。

```typescript
CREATE TABLE events (
	event_id TEXT PRIMARY KEY,
	room_id TEXT NOT NULL,
	sender TEXT NOT NULL,
	event_type TEXT NOT NULL,
	state_key TEXT,
	content TEXT NOT NULL,
	origin_server_ts INTEGER NOT NULL,
	depth INTEGER NOT NULL
);
```

D1基于SQLite，这意味着我们可以用最少的改动移植Tuwunel的查询。连接、索引和聚合操作都按预期工作。

我们吸取了一个深刻的教训：D1的最终一致性会破坏外键约束。在写入`events`表并检查外键时，之前对`rooms`表的写入可能尚未可见。我们移除了所有外键，并在应用代码中强制执行引用完整性。

### KV用于临时状态

OAuth授权码的有效期为10分钟，而刷新令牌则持续一个会话。

```typescript
// 存储OAuth码，TTL为10分钟
kv.put(&format!("oauth_code:{}", code), &token_data)?
	.expiration_ttl(600)
	.execute()
	.await?;
```

KV的全局分布意味着无论用户身在何处，OAuth流程都能快速工作。

### R2用于媒体

Matrix媒体直接映射到R2，因此你可以上传一张图片，获得一个内容寻址的URL——并且出口流量是免费的。

### Durable Objects用于原子性

某些操作无法容忍最终一致性。当客户端认领一个一次性加密密钥时，该密钥必须被原子性地移除。如果两个客户端认领了同一个密钥，加密会话建立就会失败。

Durable Objects提供了单线程、强一致性的存储：

```typescript
#[durable_object]
pub struct UserKeysObject {
	state: State,
	env: Env,
}

impl UserKeysObject {
	async fn claim_otk(&self, algorithm: &str) -> Result<Option<Key>> {
    	// 在单个DO内是原子的 - 不可能发生竞态条件
    	let mut keys: Vec<Key> = self.state.storage()
        	.get("one_time_keys")
        	.await
        	.ok()
        	.flatten()
        	.unwrap_or_default();

    	if let Some(idx) = keys.iter().position(|k| k.algorithm == algorithm) {
        	let key = keys.remove(idx);
        	self.state.storage().put("one_time_keys", &keys).await?;
        	return Ok(Some(key));
    	}
    	Ok(None)
	}
}
```

我们使用UserKeysObject进行端到端加密密钥管理，使用RoomObject处理实时房间事件（如输入指示器和已读回执），使用UserSyncObject处理设备间消息队列。其余数据则通过D1流转。

### 完整的端到端加密，完整的OAuth

我们的实现支持完整的Matrix端到端加密栈：设备密钥、交叉签名密钥、一次性密钥、备用密钥、密钥备份和脱水设备。

现代Matrix客户端使用OAuth 2.0/OIDC，而非传统的密码流程。我们实现了一个完整的OAuth提供程序，包括动态客户端注册、PKCE授权、RS256签名的JWT令牌、带轮换的令牌刷新以及标准的OIDC发现端点。

```typescript
curl https://matrix.example.com/.well-known/openid-configuration
{
  "issuer": "https://matrix.example.com",
  "authorization_endpoint": "https://matrix.example.com/oauth/authorize",
  "token_endpoint": "https://matrix.example.com/oauth/token",
  "jwks_uri": "https://matrix.example.com/.well-known/jwks.json"
}
```

将Element或任何Matrix客户端指向该域名，它将自动发现一切。

## 面向移动端的滑动同步

传统的Matrix同步在初始连接时会传输数兆字节的数据，消耗移动设备的电量和数据套餐。

滑动同步让客户端可以精确请求所需内容。客户端无需下载所有内容，而是获取最近20个房间及其最小状态。随着用户滚动，他们可以请求更多范围。服务器跟踪位置并仅发送增量数据。

结合边缘执行，即使在慢速网络上，移动客户端也能在500毫秒内连接并渲染其房间列表。

## 对比

对于一个服务于小型团队的家庭服务器：

| 项目 | 传统（VPS） | Workers |
| :--- | :--- | :--- |
| 月度成本（闲置） | $20-50 | $0 |
| 月度成本（活跃） | $20-50 | $3-10 |
| 全球延迟 | 100-300ms | 20-50ms |
| 部署时间 | 数小时 | 数秒 |
| 维护 | 每周 | 无 |
| DDoS防护 | 额外成本 | 包含 |
| 后量子TLS | 复杂设置 | 自动 |

*基于截至2026年1月15日DigitalOcean、AWS Lightsail和Linode公布的公开费率和指标。

随着规模扩大，经济性会进一步改善。传统部署需要进行容量规划和过度配置。Workers会自动扩展。

## 去中心化协议的未来

我们最初将此作为一个实验：Matrix能否在Workers上运行？答案是肯定的——而且这种方法也适用于其他有状态的协议。

通过将有状态的传统组件映射到Cloudflare的原语——Postgres到D1，Redis到KV，互斥锁到Durable Objects——我们可以看到复杂的应用并不需要复杂的基础设施。我们剥离了操作系统、数据库管理和网络配置，只留下应用逻辑和数据本身。

Workers提供了拥有数据的主权，而无需承担拥有基础设施的负担。

我一直在试验这个实现，并期待其他对此类服务感兴趣的人做出贡献。

准备好基于Workers构建强大的实时应用了吗？从[Cloudflare Workers](https://www.cloudflare.com/zh-cn/products/workers/)开始，并探索[Durable Objects](https://developers.cloudflare.com/durable-objects/)以构建你自己的有状态边缘应用。加入我们的[Discord社区](https://discord.com/invite/cloudflaredev)，与在边缘构建的其他开发者建立联系。

---

> 本文由AI自动翻译，原文链接：[Building a serverless, post-quantum Matrix homeserver](https://blog.cloudflare.com/serverless-matrix-homeserver-workers/)
> 
> 翻译时间：2026-01-28 04:42
