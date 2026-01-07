---
title: 企业级左移实践：Cloudflare如何用基础设施即代码管理自身
title_original: 'Shifting left at enterprise scale: how we manage Cloudflare with
  Infrastructure as Code'
date: '2025-12-09'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/shift-left-enterprise-scale/
author: Chase Catelli
summary: 本文介绍了Cloudflare作为自身“零号客户”，如何通过“左移”原则和基础设施即代码（IaC）来大规模管理数百个内部生产账户。文章阐述了其采用Terraform、定制CI/CD流水线以及策略即代码（如OPA/Rego）的技术架构，旨在实现配置的一致性、可扩展性、可观测性和主动治理，从而在开发早期捕获错误配置，降低生产环境风险。
categories:
- 技术趋势
tags:
- 基础设施即代码
- DevSecOps
- 云安全
- Terraform
- 左移
draft: false
translated_at: '2026-01-05T17:23:08.501Z'
---

Cloudflare平台是Cloudflare自身的关键系统。我们是自己的"零号客户"——使用自家产品来保护和优化我们自己的服务。

在我们的安全部门内，一个专门的零号客户团队利用其独特地位，为产品和工程团队提供持续、高保真的反馈循环，从而推动我们产品的持续改进。我们在全球范围内进行这项工作——一个错误的配置可能在几秒钟内传播到我们的边缘网络，并导致意想不到的后果。如果你曾经在将变更推送到生产环境前犹豫不决，因为你知道一个小小的错误就可能让所有员工无法访问关键应用或导致生产服务中断，那么你就能体会这种感觉。意外后果的风险是真实存在的，这让我们夜不能寐。

这带来了一个有趣的挑战：我们如何确保数百个内部生产Cloudflare账户的安全配置保持一致，同时最大限度地减少人为错误？

虽然Cloudflare仪表板在可观测性和分析方面表现出色，但手动点击数百个账户以确保安全设置完全相同，是导致错误的根源。为了保持理智和安全，我们不再将配置视为手动点击任务，而是开始将其视为代码。我们采用了"左移"原则，将安全检查移到开发的最早阶段。

这对我们来说不是一个抽象的企业目标。这是一种在错误引发事故前捕获错误的生存机制，它要求我们的治理架构发生根本性改变。

**左移对我们的意义**
"左移"指的是将验证步骤移到软件开发生命周期（SDLC）的更早阶段。在实践中，这意味着将测试、安全审计和策略合规性检查直接集成到持续集成和持续部署（CI/CD）流水线中。通过在合并请求阶段发现问题或错误配置，我们在修复成本最低时识别问题，而不是在部署后发现它们。

当我们考虑在Cloudflare应用左移原则时，四个关键原则尤为突出：
*   **一致性**：配置必须能够轻松地在账户间复制和重用。
*   **可扩展性**：大规模的变更可以快速应用到多个账户。
*   **可观测性**：配置必须可供任何人审计其当前状态、准确性和安全性。
*   **治理**：防护措施必须是主动的——在部署前强制执行以避免事故。

**生产环境IaC运营模式**
为了支持这种模式，我们将所有生产账户过渡到使用基础设施即代码（IaC）进行管理。每一次修改都被追踪，并与用户、提交记录和内部工单关联。团队仍然使用仪表板进行分析和洞察，但关键的生产变更全部通过代码完成。

这种模式确保每一次变更都经过同行评审，并且策略（尽管由安全团队制定）由所属的工程团队自己实施。

这个架构基于两项主要技术：Terraform和定制的CI/CD流水线。

我们选择Terraform是因为其成熟的开源生态系统、强大的社区支持以及与策略即代码工具的深度集成。此外，内部使用Cloudflare Terraform Provider使我们能够积极"自食其果"，亲身体验并改进它，从而为客户提供更好的体验。

为了管理数百个账户和每天约30个合并请求的规模，我们的CI/CD流水线运行在Atlantis上，并与GitLab集成。我们还使用一个自定义的Go程序——tfstate-butler，它充当代理，安全地存储状态文件。

tfstate-butler作为Terraform的HTTP后端运行。其主要设计驱动力是安全性：它确保每个状态文件使用唯一的加密密钥，以限制任何潜在安全事件的影响范围。

所有内部账户配置都在一个集中的单体代码库中定义。各个团队拥有并部署其特定的配置，并且是该集中代码库中其负责部分的指定代码所有者，确保了责任归属。要了解更多关于此配置的信息，请查看《Cloudflare如何使用Terraform管理Cloudflare》。

**基础设施即代码数据流图**

**基线及策略即代码**
整个左移策略的关键在于为所有内部生产Cloudflare账户建立一个强大的安全基线。基线是一组在代码中定义的安全策略（策略即代码）。这个基线不仅仅是一套指导方针，而是我们在整个平台上强制执行的必要安全配置——例如，最大会话时长、必需的日志、特定的WAF配置等。

这个架构使得策略执行从手动审计转变为自动化关卡。我们通过Atlantis Conftest策略检查功能，使用开放策略代理（OPA）框架及其策略语言Rego。

**将策略定义为代码**
Rego策略定义了构成所有Cloudflare提供商资源基线的具体安全要求。我们目前维护着大约50条策略。

例如，下面是一个Rego策略，用于验证访问策略中只允许使用@cloudflare.com邮箱：
```
# validate no use of non-cloudflare email
warn contains reason if {
r := tfplan.resource_changes[_]
r.mode == "managed"
r.type == "cloudflare_access_policy"
include := r.change.after.include[_]
email_address := include.email[_]
not endswith(email_address, "@cloudflare.com")
reason := sprintf("%-40s :: only @cloudflare.com emails are allowed", [r.address])
}
warn contains reason if {
r := tfplan.resource_changes[_]
r.mode == "managed"
r.type == "cloudflare_access_policy"
require := r.change.after.require[_]
email_address := require.email[_]
not endswith(email_address, "@cloudflare.com")
reason := sprintf("%-40s :: only @cloudflare.com emails are allowed", [r.address])
}
```

策略检查在每个合并请求（MR）上运行，确保配置在部署前合规。策略检查的输出直接显示在GitLab MR的评论线程中。

策略执行以两种模式运行：
*   **警告**：在MR上留下评论，但允许合并。
*   **拒绝**：直接阻止部署。

如果策略检查确定MR中应用的配置偏离了基线，输出将返回哪些资源不合规。

下面的示例显示了一个策略检查的输出，该输出识别出合并请求中的3个差异：
```
WARN - cloudflare_zero_trust_access_application.app_saas_xxx :: "session_duration" must be less than or equal to 10h
WARN - cloudflare_zero_trust_access_application.app_saas_xxx_pay_per_crawl :: "session_duration" must be less than or equal to 10h
WARN - cloudflare_zero_trust_access_application.app_saas_ms :: you must have at least one require statement of auth_method = "swk"
41 tests, 38 passed, 3 warnings, 0 failures, 0 exception
```

**处理策略例外**
我们理解例外是必要的，但它们必须与策略本身一样受到严格管理。当团队需要例外时，他们通过Jira提交请求。

一旦获得零号客户团队的批准，例外将通过向中央的exceptions.rego代码库提交拉取请求来正式化。

可以在多个层级设置例外：
**账户级**：将账户_x从策略_y中排除。
**资源类别级**：将账户_x中的所有资源_a从策略_y中排除。
**特定资源级**：将账户_x中的资源_a_1从策略_y中排除。
以下示例展示了对两个独立Cloudflare账户下五个特定应用程序的会话时长例外设置：
{
"exception_type": "session_length",
"exceptions": [
{
"account_id": "1xxxx",
"tf_addresses": [
"cloudflare_access_application.app_identity_access_denied",
"cloudflare_access_application.enforcing_ext_auth_worker_bypass",
"cloudflare_access_application.enforcing_ext_auth_worker_bypass_dev",
],
},
{
"account_id": "2xxxx",
"tf_addresses": [
"cloudflare_access_application.extra_wildcard_application",
"cloudflare_access_application.wildcard",
],
},
],
}

**挑战与经验教训**
我们的旅程并非一帆风顺。多年来，我们积累了遍布数百个账户的"点击式操作"（直接在仪表板中进行的更改）。试图将这种混乱的现状导入到一个严格的基础设施即代码系统中，感觉就像在行驶的汽车上更换轮胎。时至今日，资源导入仍然是一个持续进行的过程。
我们也遇到了自身工具的局限性。我们在Cloudflare Terraform提供商中发现了一些边界情况，只有在尝试管理如此大规模的基础设施时才会出现。这些不仅仅是小障碍，而是我们深刻认识到"自食其果"必要性的宝贵教训，这促使我们构建了更好的解决方案。
这些摩擦清晰地揭示了我们所面临的挑战，并让我们收获了三条来之不易的经验。

**经验一：高准入门槛会阻碍采用**
任何大规模基础设施即代码推广的第一个障碍，就是如何纳入现有的、手动配置的资源。我们为团队提供了两个选择：手动创建Terraform资源和导入块，或者使用cf-terraforming。
我们很快发现，不同团队对Terraform的熟练程度参差不齐，手动导入现有资源的学习曲线远比我们预期的要陡峭。
幸运的是，cf-terraforming命令行工具利用Cloudflare API自动生成必要的Terraform代码和导入语句，显著加快了迁移过程。
我们还组建了一个内部社区，让经验丰富的工程师可以指导团队了解提供商的细微差别，并帮助解决复杂的导入问题。

**经验二：配置漂移不可避免**
我们还必须解决配置漂移问题，当为了加快紧急变更而绕过基础设施即代码流程时，就会发生这种情况。虽然在事件期间直接在仪表板中进行编辑速度更快，但这会导致Terraform状态与实际状态不同步。
我们实施了一个自定义的漂移检测服务，该服务通过Cloudflare API不断比较Terraform定义的状态与实际部署的状态。当检测到漂移时，自动化系统会创建一个内部工单，并将其分配给负责的团队，并设定不同的服务级别协议进行修复。

**经验三：自动化是关键**
Cloudflare创新速度很快，因此我们的产品集和API也在不断增长。不幸的是，这意味着我们的Terraform提供商在功能上与产品保持同步方面常常滞后。
我们通过发布v5提供商解决了这个问题，该提供商基于OpenAPI规范自动生成Terraform提供商。在我们完善代码生成方法的过程中，这一转变并非没有波折，但这种方法确保了API和Terraform保持同步，减少了能力漂移的可能性。

**核心经验：主动优于被动**
通过集中管理我们的安全基线、强制进行同行评审，并在任何变更进入生产环境之前强制执行策略，我们最大限度地减少了配置错误、意外删除或策略违规的可能性。这种架构不仅有助于防止人为错误，而且实际上提高了工程速度，因为团队确信他们的变更是合规的。

我们从"零号客户"工作中获得的关键经验是：虽然Cloudflare仪表板非常适合日常操作，但要实现企业级的规模和一致的治理，则需要不同的方法。当您将Cloudflare配置视为活代码时，您就可以安全且自信地进行扩展。

对基础设施即代码有想法？欢迎继续讨论，并在 community.cloudflare.com 上分享您的经验。

---

> 本文由AI自动翻译，原文链接：[Shifting left at enterprise scale: how we manage Cloudflare with Infrastructure as Code](https://blog.cloudflare.com/shift-left-enterprise-scale/)
> 
> 翻译时间：2026-01-05 17:23
