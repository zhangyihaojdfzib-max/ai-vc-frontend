---
title: Cloudflare修复ACME验证逻辑漏洞，保障WAF功能
title_original: "How we mitigated a vulnerability in Cloudflareâ\x80\x99s ACME validation\
  \ logic"
date: '2026-01-19'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/acme-path-vulnerability/
author: ''
summary: 2025年10月，安全研究人员通过漏洞赏金计划报告了Cloudflare ACME验证逻辑中的一个漏洞，该漏洞导致特定ACME路径上的部分WAF功能失效。漏洞源于边缘网络处理ACME
  HTTP-01质询请求时，在某些情况下会错误地禁用WAF功能，允许本应被阻止的请求到达源站。Cloudflare已发布代码修复，仅在与有效质询令牌匹配时才禁用安全功能，确保了客户无需额外操作即受到保护，且未发现漏洞被恶意利用。
categories:
- 技术趋势
tags:
- 网络安全
- 漏洞修复
- Cloudflare
- ACME协议
- WAF
draft: false
translated_at: '2026-01-20T04:44:36.770774'
---

# 我们如何修复Cloudflare ACME验证逻辑中的一个漏洞

- Hrushikesh Deshpande
- Andrew Mitchell
- Leland Garofalo

2025年10月13日，来自FearsOff的安全研究人员发现并报告了Cloudflare ACME（自动证书管理环境）验证逻辑中的一个漏洞，该漏洞导致特定ACME相关路径上的部分WAF功能失效。该漏洞通过Cloudflare的漏洞赏金计划被报告并验证。

该漏洞的根源在于我们的边缘网络如何处理发往ACME HTTP-01质询路径（/.well-known/acme-challenge/*）的请求。

在此，我们将简要解释该协议的工作原理以及我们为修复此漏洞所采取的措施。

Cloudflare已修复此漏洞，Cloudflare客户无需采取任何行动。我们尚未发现任何恶意行为者利用此漏洞。

### ACME如何验证证书

ACME是一种用于自动化SSL/TLS证书颁发、续期和吊销的协议。当使用HTTP-01质询来验证域名所有权时，证书颁发机构（CA）期望在遵循`http://{客户域名}/.well-known/acme-challenge/{令牌值}`格式的HTTP路径上找到一个验证令牌。

如果此质询被Cloudflare管理的证书订单使用，那么Cloudflare将在此路径上响应，并向调用者提供CA给出的令牌。如果提供的令牌与Cloudflare管理的订单无关，则该请求将被传递到客户源站，因为他们可能正尝试作为其他系统的一部分完成域名验证。查看以下流程以获取更多详细信息——其他用例将在博客文章后面讨论。

### 底层逻辑缺陷

对`/.well-known/acme-challenge/*`的某些请求会导致服务于ACME质询令牌的逻辑在质询请求上禁用WAF功能，并允许质询请求继续到达源站，而实际上它本应被阻止。

此前，当Cloudflare提供HTTP-01质询令牌时，如果调用者请求的路径与我们系统中活跃质询的令牌匹配，服务于ACME质询令牌的逻辑会禁用WAF功能，因为Cloudflare将直接提供响应。这样做是因为这些功能可能会干扰CA验证令牌值的能力，并导致自动化证书订单和续期失败。

然而，在所使用的令牌与不同区域关联且并非由Cloudflare直接管理的情况下，请求将被允许继续发送到客户源站，而不会经过WAF规则集的进一步处理。

### 我们如何修复此漏洞

为了修复此问题，我们发布了一个代码变更。此代码变更仅允许在请求与主机名的有效ACME HTTP-01质询令牌匹配时，禁用该组安全功能。在这种情况下，Cloudflare有质询响应可以返回。

### Cloudflare客户受到保护

如上所述，Cloudflare已修复此漏洞，Cloudflare客户无需采取任何行动。此外，我们尚未发现任何恶意行为者利用此漏洞。

### 快速响应与漏洞透明度

一如既往，我们感谢外部研究人员负责任地披露此漏洞。我们鼓励Cloudflare社区提交任何已识别的漏洞，以帮助我们持续改进产品和平台的安全状况。

我们也认识到，您对我们的信任对于您在Cloudflare上基础设施的成功至关重要。我们以最高度的关注对待这些漏洞，并将继续尽我们所能减轻影响。我们深深感谢您对我们平台的持续信任，并致力于不仅在我们所做的一切工作中优先考虑安全，而且在问题出现时迅速、透明地采取行动。

> 本文由AI自动翻译，原文链接：[How we mitigated a vulnerability in Cloudflareâs ACME validation logic](https://blog.cloudflare.com/acme-path-vulnerability/)
> 
> 翻译时间：2026-01-20 04:44
