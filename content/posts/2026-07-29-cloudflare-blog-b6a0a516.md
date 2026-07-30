---
title: Cloudflare支持后量子认证保护源站连接
title_original: Post-quantum authentication to origins is now supported
date: '2026-07-29'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/post-quantum-authentication-to-origins/
author: ''
summary: Cloudflare宣布其认证源站拉取和自定义源站信任存储产品现已支持基于ML-DSA的后量子认证，用于保护Cloudflare与客户源站服务器之间的TLS连接。文章解释了源站连接的特殊性，以及为何能先于公共互联网部署后量子认证，并提供了配置方法。这是Cloudflare实现2029年完全后量子安全目标的首个里程碑，旨在防范未来量子计算机对传统凭证的破解和冒充攻击。
categories:
- 技术趋势
tags:
- 后量子密码学
- ML-DSA
- TLS认证
- Cloudflare
- 网络安全
draft: false
translated_at: '2026-07-30T05:02:06.917825'
---

Cloudflare 的认证源站拉取和自定义源站信任存储现已支持后量子认证。

本文将解释如何为源站服务器配置完全后量子安全的双向认证 TLS 连接，深入介绍构建该功能的技术细节，进行一次坦诚的自我检讨，并最终说明这项工作如何融入我们的整体后量子迁移路线图。

## 达成重要里程碑

过去几年，我们的重点一直放在部署后量子加密技术，以防范"先存储、后解密"攻击——攻击者悄悄囤积加密数据，希望未来用量子计算机进行解密。

然而，量子计算和密码分析领域的最新突破，使得行业和政府升级后量子密码学的时间表大幅提前，也促使我们将注意力转向部署后量子认证，以防范那些即将能够利用量子计算机破解传统凭证并实施冒充攻击的攻击者。

在之前的文章中，我们宣布 Cloudflare 的目标是在 2029 年实现完全后量子安全，并规划了沿途需要达成的多个里程碑。如今我们已达成首个里程碑：我们的认证源站拉取和自定义源站信任存储产品现已支持基于模块格数字签名算法（ML-DSA）签名的后量子认证，用于保护 Cloudflare 与客户源站服务器之间的连接。

## 源站连接的特殊性

当客户端访问由 Cloudflare 代理的网站时，通常涉及两条连接。第一条连接是从访客（如浏览器）到 Cloudflare。如果请求可由 Cloudflare 缓存处理或触发任何拦截规则，Cloudflare 可能直接响应。否则，Cloudflare 会建立第二条连接到客户源站服务器以获取请求内容，从而响应原始请求。

![两条连接：访客到 Cloudflare 以及 Cloudflare 到源站](/images/posts/468691df2278.jpg)

保护敏感的访客数据需要这两条连接都能抵御量子攻击。我们分别于 2022 年和 2023 年为访客到 Cloudflare（连接 1）和 Cloudflare 到源站（连接 2）启用了后量子加密支持，目前已有大量使用。

我们正在积极完善后量子认证的完整方案。对于访客到 Cloudflare 的连接，我们正与 Google 等机构在互联网工程任务组（IETF）合作开发和试验梅克尔树证书（MTC）——一种面向网络快速后量子证书的设计方案，初步部署目标定在 2027 年。而本文的主题是 Cloudflare 到源站的连接，其认证需求在多个重要方面与访客到 Cloudflare 连接有所不同。

对于这条连接，Cloudflare 是客户端。这使我们能够采用连接池等技术，将全球网络中的请求汇聚到较少量的源站服务器连接上，从而将连接建立的开销分摊到大量请求中。这使得"即插即用"式后量子签名的成本更易接受，也降低了 MTC 性能优势的必要性。

此外，由于 Cloudflare 与客户之间存在既有的信任关系（即 Cloudflare 账户），我们无需受限于公共互联网公钥基础设施（WebPKI）的约束和时间表，而是可以使用针对该用例定制的自定义 PKI，无需承担可能不适用的中间证书和证书透明度带来的开销。Cloudflare Tunnel 等解决方案也可用于保护 Cloudflare 到源站的连接，无需升级传统源站系统，只需通过后量子加密（后量子认证正在开发中）保护的隧道转发流量即可。

综上所述，Cloudflare 到源站连接的独特需求使我们能够在 WebPKI 为公共互联网提供支持之前，率先通过 ML-DSA 认证部署后量子认证。（对于继续使用 WebPKI 的客户，请放心：我们未来将在 Cloudflare 到源站连接上增加 MTC 支持。）

那么如何启用这一功能？让我们深入了解配置方法。

## 配置完全后量子安全的源站连接

我们已在自定义源站信任存储和认证源站拉取产品中增加了 ML-DSA 支持（涵盖所有 FIPS 204 参数集：ML-DSA-44、ML-DSA-65 和 ML-DSA-87）。ML-DSA-44 是我们推荐大多数应用使用的选项，因为它性能最优，且达到了 NIST 类别 2 的安全强度。

### 自定义源站信任存储

当 Cloudflare 连接到配置为完全（严格）SSL 模式的客户源站服务器时，我们会根据默认信任存储对源站证书进行认证，该信任存储包含所有常用受信任的证书颁发机构（CA）以及 Cloudflare 的源站 CA。自定义源站信任存储（COTS）产品（需启用高级证书管理器）允许客户用自己控制的 CA 集替换此默认信任存储。COTS 现在允许客户上传 ML-DSA CA，这样 Cloudflare 在连接到源站时，将信任任何链接到该 CA 的源站服务器证书链。

### 认证源站拉取

为限制源站服务器上的滥用和资源消耗，客户可能希望仅处理来自 Cloudflare 服务器的请求。认证源站拉取（AOP）可用于配置 Cloudflare 向源站服务器出示客户端证书，以建立双向 TLS（mTLS）连接，使双方通信实现双向安全可信。AOP 对所有 Cloudflare 套餐级别免费提供。

AOP 支持三种配置级别：全局、区域级和主机名级。区域级和主机名级配置现在允许客户上传 ML-DSA 证书和私钥（采用 FIPS 204 种子格式），以便 Cloudflare 的 TLS 客户端在连接源站服务器时出示此证书进行身份认证。（请放心，我们没有忘记全局配置级别——只是该变更涉及面更广，将在后续优先处理。）

### 避免降级

为认证方和验证方同时增加后量子加密和认证支持，是实现完全后量子安全的必要条件，但并非充分条件。降级攻击这一棘手问题依然存在。如果验证方支持任何易受量子攻击的认证机制，那么面对能够伪造经典凭证的路径外攻击者，它们仍然存在风险。

解决方案：验证方必须移除对易受量子攻击的认证机制的信任。（这在复杂的 PKI 中更为微妙。例如，请参阅 Chromium 安全团队关于 Web 过渡的四阶段计划。）有关如何确保源站免受降级攻击的详细信息，请参阅 AOP 和 COTS 的配置指南。

### 快速入门

以下操作指南展示了如何生成 ML-DSA 证书链，并通过 Cloudflare API 配置这两个产品。如需仪表板操作说明和其他背景信息，请参阅开发者文档。

1. 生成证书

您需要 OpenSSL 3.5.0 或更高版本。私钥必须以 FIPS 204 仅种子编码格式生成，这是 Cloudflare 目前接受上传的唯一格式。

用于 COTS 的源站服务器证书链：

```
# 为源站服务器创建私有的 ML-DSA-44 CA
openssl genpkey -algorithm mldsa44 \
  -provparam ml-dsa.output_formats=seed-only \
  -out origin-ca.key
```

```bash
# 创建源站CA（证书颁发机构）
openssl req -new -x509 -key origin-ca.key \
  -out origin-ca.crt -days 10950 \
  -subj "/CN=Origin Server CA"

# 创建源站服务器证书（由源站CA签名）
openssl genpkey -algorithm mldsa44 \
  -provparam ml-dsa.output_formats=seed-only \
  -out origin-server.key

openssl req -new -key origin-server.key \
  -out origin-server.csr \
  -subj "/CN=origin.example.com"

openssl x509 -req -in origin-server.csr \
  -CA origin-ca.crt -CAkey origin-ca.key -CAcreateserial \
  -out origin-server.crt -days 5475 \
  -extfile <(printf "basicConstraints=CA:FALSE\nkeyUsage=digitalSignature\nsubjectAltName=DNS:origin.example.com\n")

```

用于AOP（已认证源站拉取）的Cloudflare客户端证书链：

```bash
# 为已认证源站拉取创建私有ML-DSA-44 CA
openssl genpkey -algorithm mldsa44 \
  -provparam ml-dsa.output_formats=seed-only \
  -out aop-ca.key

openssl req -new -x509 -key aop-ca.key \
  -out aop-ca.crt -days 10950 \
  -subj "/CN=Authenticated Origin Pull CA"

# 创建Cloudflare将出示的客户端证书（由AOP CA签名）
openssl genpkey -algorithm mldsa44 \
  -provparam ml-dsa.output_formats=seed-only \
  -out aop-client.key

openssl req -new -key aop-client.key \
  -out aop-client.csr \
  -subj "/CN=cloudflare-aop-client"

openssl x509 -req -in aop-client.csr \
  -CA aop-ca.crt -CAkey aop-ca.key -CAcreateserial \
  -out aop-client.crt -days 5475 \
  -extfile <(printf "basicConstraints=CA:FALSE\nkeyUsage=digitalSignature\n")

```

2. 将源站CA上传到自定义源站信任存储

```bash
CA_CERT=$(jq -Rs . < origin-ca.crt)

curl "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/acm/custom_trust_store" \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  --header "Content-Type: application/json" \
  --json "{\"certificate\": $CA_CERT}"

```

上传COTS CA会替换该区域默认的公共信任CA。请确保仅在上传后量子CA时执行此操作，以避免降级攻击。

3. 上传用于已认证源站拉取的客户端证书

以下示例使用区域级AOP。如果您偏好每主机名AOP，请改用`/origin_tls_client_auth/hostnames/certificates`端点。

```bash
CERT=$(jq -Rs . < aop-client.crt)
KEY=$(jq -Rs . < aop-client.key)

# 上传ML-DSA客户端证书
curl "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/origin_tls_client_auth" \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  --header "Content-Type: application/json" \
  --json "{\"certificate\": $CERT, \"private_key\": $KEY}"

# 启用区域级已认证源站拉取
curl -X PUT "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/origin_tls_client_auth/settings" \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  --header "Content-Type: application/json" \
  --json '{"enabled": true}'

```

4. 将SSL/TLS模式设置为完全（严格）

自定义源站信任存储仅在您的区域使用**完全（严格）**模式时生效。如果您使用不带COTS的AOP，**完全**或更高模式就足够了。

```bash
curl -X PATCH "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/settings/ssl" \
  --header "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  --header "Content-Type: application/json" \
  --json '{"value": "strict"}'

```

5. 配置您的源站服务器（在NGINX上）

如果您使用COTS（您的源站出示ML-DSA服务器证书）：

```nginx
server {
    listen 443 ssl;
    ssl_certificate     /etc/ssl/origin-server.crt;
    ssl_certificate_key /etc/ssl/origin-server.key;
    ssl_protocols       TLSv1.3;
}

```

如果您使用AOP（您的源站验证Cloudflare的客户端证书）：

```nginx
server {
    listen 443 ssl;
    ssl_client_certificate /etc/ssl/aop-ca.crt;
    ssl_verify_client      on;
}
```

如果您同时使用两者（推荐用于完整的后量子双向TLS）：

```nginx
server {
    listen 443 ssl;
    ssl_certificate        /etc/ssl/origin-server.crt;
    ssl_certificate_key    /etc/ssl/origin-server.key;
    ssl_client_certificate /etc/ssl/aop-ca.crt;
    ssl_verify_client      on;
    ssl_protocols          TLSv1.3;
}
```

6. 验证后量子握手

Cloudflare与您的源站之间的TLS握手在后台进行，因此您无法通过从外部连接到代理主机名来直接观察。请分别验证每一方。

验证COTS（源站出示ML-DSA证书）：

如果您的源站IP可直接访问（例如，在启用Cloudflare代理之前的测试期间），请直接连接到源站IP并验证证书：

```bash
openssl s_client -connect <ORIGIN_IP>:443 \
  -servername origin.example.com \
  -CAfile origin-ca.crt \
  -brief
```

在输出中查找`Signature type: mldsa44`。

如果您的源站已设置防火墙，仅接受Cloudflare IP，请检查源站服务器的TLS日志，或使用诸如`ssldump`或`tcpdump`之类的数据包捕获工具在源站上确认Cloudflare已使用ML-DSA证书协商了TLS 1.3。

验证AOP（Cloudflare出示客户端证书）：

确认直接连接到源站（没有有效的客户端证书）被拒绝：

```bash
openssl s_client -connect <ORIGIN_IP>:443 \
  -servername origin.example.com \
  -brief
```

在强制执行`ssl_verify_client on`的情况下，这应该会失败并显示SSL警报。

验证完整的Cloudflare到源站路径：

由于mTLS握手是服务器到服务器进行的，确认Cloudflare正在出示ML-DSA客户端证书的最可靠方法是检查您的源站服务器日志。例如，在NGINX中，您可以记录客户端证书序列号或主题：

```nginx
log_format pq_verify '$remote_addr - $ssl_client_serial $ssl_client_s_dn';
access_log /var/log/nginx/pq-verify.log pq_verify;
```

通过Cloudflare发送请求后，检查日志。您应该会看到您上传的`aop-client.crt`证书的序列号。

对于密钥协商，请确保您的源站TLS库支持`X25519MLKEM768`，并且在您的配置中优先使用它。后量子密钥协商将在源站服务器日志或数据包捕获中显示为协商组。

## 枯燥的细节

实现此功能涉及两个主要系统：我们的控制平面服务（允许客户管理其TLS设置并上传证书）和数据平面服务（负责根据客户配置建立与源站服务器的TLS连接）。

### 控制平面

与为Cloudflare的API和仪表板提供动力的许多其他服务一样，为Cloudflare的SSL/TLS产品提供配置的服务在一组关键数据中心内以**高可用性设置**运行。该服务负责处理SSL/TLS设置更新，并将其推送到我们的**全球分布式键值存储**，以便在处理实时请求时数据平面服务可以使用这些设置。

为AOP和COTS启用ML-DSA支持需要更新此服务以支持解析和验证ML-DSA证书。这听起来很简单，但有一个问题：该服务是用Go编写的，但Go的标准X.509和TLS库尚不支持ML-DSA。我们转而实现了Cloudflare的**CIRCL**库中的**必要功能**以打补丁支持。这是一个相对简单的更改，但为每个需要后量子身份验证支持的服务重复此操作将是一项重大任务。

幸运的是，**Go 1.27**（预计2026年8月发布）将包含原生ML-DSA支持，并将允许我们移除CIRCL依赖。其他基于Go的服务随后将能够通过简单的版本更新无缝引入ML-DSA支持。

### 数据平面

控制平面更改到位后，客户就可以为AOP和COTS产品上传ML-DSA证书。下一步是更新我们负责与客户源站交互的数据平面服务，以**实际使用**这些证书。

我们在之前的博客文章中讨论过我们的开源代理框架Pingora，特别是我们如何基于Pingora构建了一个服务，用于处理与这些源站的所有连接。这个服务被直白地命名为Pingora Origin，它负责确保每秒数百万次发往源站的请求能够安全可靠地到达最终目的地。

确保请求安全的任务通常由TLS提供商承担，但你可能不知道，后量子安全（或者说后量子认证）在这方面并无不同。同样可能令人失望的是，抵御量子攻击并不需要借助激光和超导约瑟夫森结等奇异物质形态；你只需要更新BoringSSL即可。如今，BoringSSL名副其实：过去几年间，没有出现过任何CVE或重大变更。事实上，我们过于依赖这种稳定性，以至于不得不承认：我们将Pingora Origin的BoringSSL更新推迟了四年，而是维护了一个内部分支，根据需要打补丁添加额外功能。这种做法一直运行良好，但当后量子认证支持于2026年4月加入BoringSSL时，我们认定这次更新值得承受不便。

此时，我们多么希望能说：“这次更新完美无缺，毫无问题！”但自然还是出现了一些小插曲。在四年的代码变更中，有一个提交启用了对TLS证书中KeyUsage规则的强制执行。这一变更符合规范，但正如我们之前所见，互联网并不以遵循RFC著称。结果是，尽管我们测试了数周，并以非常缓慢的发布节奏逐步推广以寻找此类回归问题，仍有少量客户的证书在变更后被判定为无效，导致了2026年6月10日的一次事件。我们迅速回滚了变更，并在打补丁以保留对技术上无效KeyUsage的RSA证书的支持后，完全后量子安全的TLS到源站连接现已上线并可供使用。

## 我们才刚刚开始

ML-DSA支持在TLS库中日益普及，常规的软件更新将为许多应用程序带来后量子认证支持。（请保持您的库更新！）备受期待的Go 1.27（2026年8月）将原生支持ML-DSA，使基于Go的服务只需简单的版本更新即可添加后量子认证。

随着这些变更在整个生态系统中传播，我们也将升级我们的系统。请参阅Cloudflare产品中的PQC，了解Cloudflare产品和服务中后量子加密和认证支持的最新跟踪信息。

## 相关标签

关注社交媒体

- Cloudflare
- Luke Valenta
- Kevin Guthrie

## 订阅以接收新文章通知

我们绝不会分享您的电子邮件地址。

感谢订阅！请检查您的收件箱以确认。

---

> 本文由AI自动翻译，原文链接：[Post-quantum authentication to origins is now supported](https://blog.cloudflare.com/post-quantum-authentication-to-origins/)
> 
> 翻译时间：2026-07-30 05:02
