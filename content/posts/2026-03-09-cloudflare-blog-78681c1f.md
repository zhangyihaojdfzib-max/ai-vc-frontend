---
title: 主动防御：Cloudflare推出面向API的有状态漏洞扫描器
title_original: 'Active defense: introducing a stateful vulnerability scanner for
  APIs'
date: '2026-03-09'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/vulnerability-scanner/
author: ''
summary: 本文介绍了Cloudflare新推出的Web和API漏洞扫描器测试版，旨在解决传统防御性安全措施在API安全领域的不足。文章指出，API漏洞（如失效的对象级别授权）多为逻辑缺陷，难以被基于签名的WAF检测。新扫描器采用主动、有状态的方式，通过模拟测试流量来发现此类漏洞，首先面向API
  Shield客户提供，并计划逐步扩展检测范围。
categories:
- 技术趋势
tags:
- API安全
- 漏洞扫描
- Cloudflare
- 主动防御
- BOLA
draft: false
translated_at: '2026-03-10T04:47:06.156382'
---

# 主动防御：推出面向API的有状态漏洞扫描器

2026-03-09

- John Cosgrove
- Alex Povel
- Malte Reddig

![](/images/posts/bd6c08c3e88e.png)

安全防护传统上是一场防御游戏。您需要筑起围墙、设立关卡、制定规则来拦截可疑流量。多年来，Cloudflare 一直是这一领域的领导者：我们的应用安全平台旨在实时捕获攻击，在恶意请求到达您的源站之前就在边缘将其丢弃。但对于API安全而言，仅采取防御姿态是不够的。

这就是为什么我们今天要推出 Cloudflare Web 和 API 漏洞扫描器的测试版。

我们从 OWASP API Top 10 中最普遍且最难捕获的威胁开始：**失效的对象级别授权**。我们将逐步添加更多漏洞扫描类型，包括 API 和 Web 应用程序威胁。

当今最危险的 API 漏洞并非 Web 应用防火墙可以轻易发现的通用注入攻击或畸形请求。它们是逻辑缺陷——完全符合协议和应用程序规范，但违背业务逻辑的、完全有效的 HTTP 请求。

要发现这些漏洞，您不能只是被动等待攻击。您必须主动搜寻它们。

Web 和 API 漏洞扫描器将首先面向 **API Shield** 客户提供。请继续阅读，了解为什么我们在首个版本中专注于 API 安全扫描。

## 为什么纯防御性安全会错失目标

在 Web 应用程序领域，漏洞通常看起来像语法错误。一次 **SQL 注入** 尝试看起来像是数据位置出现了代码。一次 **跨站脚本攻击** 看起来像是表单字段中的脚本标签。这些都有特征签名。

API 漏洞则不同。为了说明这一点，让我们想象一个仅与后端 API 通信的外卖移动应用。我们以订单端点为例：

端点定义：`/api/v1/orders`

| 方法 | 资源路径 | 描述 |
| :--- | :--- | :--- |
| GET | `/api/v1/orders/{order_id}` | 检查状态。返回特定订单的跟踪状态（例如，"厨房正在准备中"）。 |
| PATCH | `/api/v1/orders/{order_id}` | 更新订单。允许用户修改送达地址或添加配送说明。 |

在像 BOLA 这样的失效授权攻击中，用户 A（攻击者）请求更新属于用户 B（受害者）的已支付订单的配送地址。攻击者只需在 PATCH 请求中插入用户 B 的 `{order_id}`。

以下是一个请求示例，其中 '8821' 是用户 B 的订单 ID。请注意，用户 A 使用其自己的有效 Token 进行了完整的身份验证：

```javascript
PATCH /api/v1/orders/8821 HTTP/1.1
Host: api.example.com
Authorization: Bearer <User_A_Valid_Token>
Content-Type: application/json

{
  "delivery_address": "123 Attacker Way, Apt 4",
  "instructions": "Leave at front door, ring bell"
}

```

请求头是有效的。身份验证 Token 是有效的。数据模式是正确的。对于标准的 Web 应用防火墙来说，这个请求看起来完美无缺。如果是人工手动发送攻击请求，甚至可能骗过机器人管理方案。

现在，用户 A 将收到本该送给 B 的食物！这个漏洞之所以存在，是因为 API 端点未能验证用户 A 是否确实有权查看或更新用户 B 的数据。这是一个逻辑上的失败，而非语法错误。要修复此问题，API 开发者可以实现一个简单的检查：`if (order.userID != user.ID) throw Unauthorized;`

您可以通过主动发送 API 测试流量或被动监听现有 API 流量来检测这类漏洞。通过被动扫描发现这些漏洞需要上下文。去年，我们为 API Shield 推出了 **BOLA 漏洞检测**。该检测通过被动扫描客户流量中的使用异常来自动发现这些漏洞。要成功进行此类扫描，您需要知道"有效"的 API 调用是什么样的，变量参数是什么，典型用户的行为方式，以及当这些参数被操纵时 API 的行为方式。

然而，安全团队可能由于某些原因缺乏这些上下文，即使他们能够访问 API Shield 的 BOLA 漏洞检测功能。开发环境可能需要测试但缺乏用户流量。生产环境可能（幸运地）缺乏攻击流量但仍需分析，等等。在这些情况下，以及为了总体上保持主动，团队可以转向动态应用程序安全测试。通过创建专门用于安全测试的全新流量配置文件，DAST 工具可以随时在任何环境中查找漏洞。

不幸的是，传统的 DAST 工具入门门槛很高。它们通常配置困难，需要您手动上传和维护 Swagger/OpenAPI 文件，难以正确地对现代复杂的登录流程进行身份验证，并且可能完全缺乏任何 API 特定的安全测试（例如 BOLA）。

## Cloudflare 的 API 扫描优势

在上面的外卖订单示例中，我们假设攻击者能找到有效的订单进行修改。虽然在实时生产环境中，攻击者通常有途径收集此类情报，但在安全测试演练中，您必须在测试 API 的授权控制之前创建自己的对象。对于典型的 DAST 扫描来说，这可能是个问题，因为许多扫描器独立处理每个单独的请求。这种方法无法将请求按照发现失效授权漏洞所需的逻辑模式串联起来。传统的 DAST 扫描器也可能在您的安全工具和编排环境中孤立存在，导致其发现结果无法被共享或在上下文中查看。

Cloudflare 的漏洞扫描之所以不同，有几个关键原因。

首先，**安全洞察** 将把我们新扫描的结果与任何现有的 Cloudflare 安全发现结果一起列出，以提供额外的上下文。您将在一个地方看到所有的态势管理信息。

其次，**我们已经了解您 API 的输入和输出**。如果您是 API Shield 客户，Cloudflare 已经了解您的 API。我们的 **API 发现** 和 **模式学习** 功能会被动地编录您的端点并学习您的流量模式。虽然在初始版本中，您需要手动上传 OpenAPI 规范才能开始使用，但在未来的版本中，即使没有规范，您也能快速上手。

第三，由于我们位于边缘，我们可以将被动流量检查知识转化为主动情报。通过使用漏洞扫描器发送全新的 HTTP 请求，可以轻松验证 BOLA 漏洞检测风险（通过流量检查发现）。

最后，我们构建了一个全新的、有状态的 DAST 平台，如下文详述。大多数扫描器需要数小时的设置来"教会"工具如何与您的 API 通信。使用 Cloudflare，您可以有效地跳过这一步并快速开始。您提供 API 凭据，我们将使用您的 API 模式自动构建扫描计划。

## 构建自动扫描计划

API 通常使用 **OpenAPI 模式** 进行文档记录。这些模式指明了主机、方法和路径（通常称为"端点"），以及传入请求的预期参数和响应结果。为了自动构建扫描计划，我们必须首先理解任何待扫描 API 的这些 API 规范。

我们的扫描器通过从 OpenAPI 文档构建 API 调用图，然后使用攻击者和所有者上下文遍历该图来工作。所有者创建资源，攻击者随后尝试访问它们。攻击者使用自己的一套有效凭据进行完整的身份验证。如果攻击者成功读取、修改或删除了不属于自己的资源，则发现了授权漏洞。

以ID为8821的上述配送订单为例。要使服务器端资源存在，它最初需要由所有者创建，很可能是在一个没有或仅有最小依赖关系（先前必要的调用及生成的数据）的"创世"POST请求中完成。将API建模为调用图时，此类端点构成了一个没有或仅有少量入边（依赖关系）的节点。任何后续请求（例如攻击者的上述PATCH请求）都会对创世请求（POST）产生数据依赖（数据为order_id）。若未提供全部数据，PATCH请求将无法执行。

此处通过紫色箭头展示了在此API图中，为通过POST /api/v1/orders/{order_id}/note/{note_id}端点向订单添加备注而必须访问的节点。**关键在于，图中显示的所有步骤或逻辑均未在OpenAPI规范中提供！** 必须通过其他方式进行逻辑推断，而这正是我们的漏洞扫描器将自动执行的任务。

为了可靠且自动地规划跨多种API的扫描，我们必须从头开始准确建模这些端点关系。然而存在两个问题：API规范的数据质量无法保证，且即使是功能完整的模式也可能存在命名方案模糊的情况。考虑上述API的简化OpenAPI规范示例：

```javascript
openapi: 3.0.0
info:
  title: Order API
  version: 1.0.0
paths:
  /api/v1/orders:
    post:
      summary: Create an order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                product:
                  type: string
                count:
                  type: integer
              required:
                - product
                - count
      responses:
        '201':
          description: Item created successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  result:
                    type: object
                    properties:
                      id:
                        type: integer
                      created_at:
                        type: integer
                  errors:
                    type: array
                    items:
                      type: string
  /api/v1/orders/{order_id}:
    patch:
      summary: Modify an order by ID
      parameters:
        - name: order_id
          in: path

```

我们可以看到POST端点返回如下响应：

```json
{
    "result": {
        "id": 8821,
        "created_at": 1741476777
    },
   "errors": []
}

```

对人类观察者而言，可以迅速明确`$.result.id`是需要注入PATCH端点`order_id`参数的值。`id`属性也可能被命名为`orderId`、`value`或其他名称，并可能被任意嵌套。对于基于启发式的方法而言，OpenAPI文档中这些任意形式的细微不一致性处理起来极为困难。

我们的扫描器利用Cloudflare自家的Workers AI平台来处理这一模糊问题领域。诸如OpenAI开源权重的gpt-oss-120b等模型足够强大，能够可靠匹配数据依赖关系，并在必要时生成逼真的伪造数据，从而有效填补OpenAPI规范的空白。借助结构化输出功能，模型会生成API调用图的表示，供扫描器遍历执行，并适时注入攻击者和所有者的凭据。

这种方法通过人工智能解决了原本需要人类智能来推断OpenAPI模式中授权和数据关系的问题。结构化输出弥合了gpt-oss自然语言世界与机器可执行指令之间的鸿沟。除了Workers AI解决规划问题外，在Workers AI上自托管意味着我们的系统能自动受益于Cloudflare高可用、全球分布式的基础架构。

### 基于成熟基础构建

构建客户愿意托付API凭据的漏洞扫描器需要可靠的基础设施。我们并未重复造轮子，而是整合了已在Cloudflare内部经过验证和部署的服务，用于扫描器平台的两个关键组件：扫描器控制平面和扫描器密钥存储。

扫描器控制平面与Temporal集成实现扫描编排，Cloudflare的其他内部服务已依赖此系统。每次扫描中执行的众多测试计划的复杂性，通过Temporal的持久执行框架得到有效管理。

整个后端采用Rust编写，该语言在Cloudflare的基础设施服务中已被广泛采用。这使我们能够复用内部库并在团队间共享架构模式。同时也为扫描器未来可能与其他Cloudflare系统（如FL2或我们的测试框架Flamingo）集成奠定了基础——这将实现扫描与边缘请求处理或测试基础设施更紧密协同的场景。

#### 通过HashiCorp Vault Transit Secret Engine保障凭据安全

扫描身份验证和授权漏洞需要处理API用户凭据。Cloudflare对此责任极为重视。

我们通过使用HashiCorp的Vault Transit Secret Engine（TSE）提供加密即服务，确保公共API层对未加密客户凭据的访问权限最小化。凭据提交后立即由TSE加密（TSE负责加密但不存储密文），随后存储在Cloudflare基础设施中。

我们的API无权解密此数据。解密仅发生在最后阶段，即测试计划向客户基础设施发起请求时。只有执行测试的Worker才有权请求解密，我们通过Rust中的严格类型和额外安全机制来强化此限制，确保对解密方法的最小化访问。

我们通过定期轮换和使用TSE进行定期重加密来进一步保障客户凭据安全，以降低风险。此流程意味着我们仅与新密文交互，原始密钥始终保持不可见状态。

## 后续计划？

我们从今天起面向所有API Shield客户开放测试版，提供BOLA漏洞扫描功能，并正在开发未来版本的其他API威胁扫描功能。通过Cloudflare API，您可以触发扫描、管理配置并以编程方式获取结果，直接集成到CI/CD流水线或安全仪表板中。API Shield客户：请查阅开发者文档，立即开始扫描端点的BOLA漏洞。

我们之所以从BOLA漏洞入手，是因为这是最难解决的API漏洞，也是客户面临的最大风险。但此扫描引擎的设计具备可扩展性。

近期，我们计划扩展扫描器能力以覆盖最流行的OWASP Web Top 10漏洞：例如SQL注入（SQLi）和跨站脚本（XSS）等经典Web漏洞。如需在功能发布时获得通知，请在此处注册等待列表，您将第一时间获知我们将引擎扩展至通用Web应用漏洞扫描的消息。

---

> 本文由AI自动翻译，原文链接：[Active defense: introducing a stateful vulnerability scanner for APIs](https://blog.cloudflare.com/vulnerability-scanner/)
> 
> 翻译时间：2026-03-10 04:47
