---
title: Hugging Face如何规模化机密管理
title_original: How Hugging Face Scaled Secrets Management for AI Infrastructure
date: '2025-03-31'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/scaling-secrets-management
author: ''
summary: Hugging Face为应对多云环境和团队扩张带来的机密管理挑战，从HashiCorp Vault转向Infisical。通过Infisical的Kubernetes
  Operator实现自动化机密更新与同步，结合Okta集成实现细粒度RBAC，并利用CLI工具消除本地.env文件风险。该方案提升了安全性、开发效率与基础设施一致性，支持每分钟超1000万次请求的高流量场景。
categories:
- AI基础设施
tags:
- 机密管理
- Kubernetes
- 多云架构
- 安全合规
- 开发者体验
draft: false
translated_at: '2026-04-30T05:31:09.558796'
---

# Hugging Face 如何为AI基础设施规模化机密管理

Hugging Face已成为大规模推进AI的代名词。随着超过400万开发者在Hub上部署模型，平台的快速增长迫使团队重新思考敏感配置数据——即机密——的管理方式。

去年，工程团队着手改进其机密和凭证的处理方式。在评估了HashiCorp Vault等工具后，他们最终选择了Infisical。

本案例研究详细介绍了他们迁移到Infisical的过程，解释了如何集成其强大功能，并重点展示了它如何使工程师能够更高效、更安全地工作。

## 背景

随着Hugging Face的基础设施从仅使用AWS的环境演变为包含Azure和GCP的多云环境，工程团队需要一种更敏捷、更安全、更集中的方式来管理机密。他们没有重新改造遗留系统或采用HashiCorp Vault等重量级解决方案，而是转向了Infisical，因为它具有开发者友好的工作流程、多云抽象和强大的安全能力。

他们面临的主要挑战包括：

- 由于跨环境管理不一致而导致的"机密扩散"风险增加。
- 随着团队规模扩大，权限管理变得复杂，需要与组织的SSO（Okta）集成的严格基于角色的访问控制（RBAC）。
- 本地开发困难，传统的.env文件既损害了安全性，也降低了开发者的生产力。
- 手动轮换机密的负担，在一次涉及凭证泄露的安全事件后，这一问题变得尤为突出。

此外，团队需要的解决方案需要符合基础设施即代码实践，支持按项目管理机密，并在部署过程中在自动化和手动控制之间实现良好平衡。

## 实施

Infisical的灵活架构是一个理想的解决方案。工程团队抓住机会重新审视了他们的内部项目结构，将项目拆分为独立的基础设施和应用领域。这使他们能够实现更清晰的关注点分离，并标准化机密轮换实践——这是近期安全事件后的优先事项。

通过利用之前用于从AWS配置创建Kubernetes机密的Terraform，他们发现过渡到Infisical Kubernetes Operator异常顺利。这种集成在标准化所有环境中的机密管理的同时，实现了安全改进。

### Kubernetes集成

Kubernetes是Hugging Face生产环境的核心，Infisical的Kubernetes Operator在自动化机密更新方面发挥了重要作用。该Operator持续监控Infisical中任何机密的变化，并确保这些更新被传播到相应的Kubernetes对象。每当检测到变化时，它可以自动重新加载依赖的Deployment，确保容器始终运行最新的机密。

示例：

Kubernetes中运行的应用程序需要一个新机密。可以通过Infisical的CLI或Web UI创建该机密，然后开发者在Kubernetes中创建一个InfisicalSecret资源，指定应从Infisical同步哪个机密：

```yaml
apiVersion: infisical.com/v1alpha1
kind: InfisicalSecret
metadata:
  name: my-app-secret
  namespace: production
spec:
  infisicalSecretId: "123e4567-e89b-12d3-a456-426614174000"
  targetSecretName: "my-app-k8s-secret"

```

一旦CRD被应用，Infisical Operator就会持续监控更新。当在Infisical中检测到变化时，Operator会自动更新Kubernetes机密（my-app-k8s-secret）。

更好的是，由于应用程序的Deployment将my-app-k8s-secret引用为环境变量源或挂载卷，Operator可以在机密更改时自动触发容器重新加载。

在实践中，尽管Operator能够自动触发容器重启，但Hugging Face的工程师更倾向于等待手动重新部署。这一决定是出于对部署精确控制的需要，特别是在涉及高流量（每分钟超过1000万次请求）和大量副本的情况下。

### 本地开发

对于本地开发，Infisical的CLI通过将机密直接注入开发环境来简化工作流程。这消除了对不安全的本地.env文件的需求，使本地配置与生产标准保持一致，并减少了新员工入职的摩擦。

## 安全与访问管理

安全改进是此次迁移的核心。通过将Infisical与Okta等现有身份提供商集成，Hugging Face建立了一个细粒度的RBAC系统。权限从Okta组自动映射，确保开发者保留对其项目的管理权限，而前端和后端团队则获得适当受限的读取或写入权限。

此外，机密共享功能允许Hugging Face的ML/AI研究人员之间安全地共享凭证。集中的Infisical平台还简化了审计和管理机密轮换——这是之前安全事件所凸显的必要性。

## CI/CD与基础设施集成

与CI/CD管道的无缝集成进一步增强了整体安全态势。Infisical通过使用OIDC认证和Terraform集成的GitHub Actions嵌入到部署管道中。通过在安全环境中运行自托管运行器，每次部署都符合生产级安全标准。这种集成方法最小化了风险，并确保了从本地开发到云部署的一致体验。

## 技术成果与见解

使用Infisical集中管理机密带来了切实的改进：

- 工程师不再需要花费宝贵的时间手动配置环境机密。自助服务工作流程加速了新员工入职和日常开发周期。
- 自动化审计和细粒度访问控制实现了快速事件响应，并促进了安全的"左移"方法。
- 跨云提供商、Kubernetes集群和CI/CD管道的一致集成消除了机密管理中的差异，从而增强了基础设施的安全性和可靠性。

正如Hugging Face基础设施负责人Adrien Carreira所说：

"Infisical提供了我们所需的所有功能和安全设置，以提升我们的安全态势并节省工程时间。无论你是在本地工作、在生产环境中运行Kubernetes集群，还是在CI/CD管道中操作机密，Infisical都有无缝的预构建工作流程。"

## 结论

Hugging Face迁移到Infisical展示了以技术驱动、以工程为中心的方法来管理跨多个云平台的机密如何带来显著收益。对于应对类似挑战的团队，使用Infisical是一种在保持强大安全性的同时提高工作效率的实用方法。

当安全路径成为最简单的路径时，团队可以专注于构建创新产品，而不是担心管理机密。

## 资源

对于有兴趣采用类似方法的团队：

- 安全GitOps工作流程：机密管理实用指南
- 2025年Kubernetes机密管理 - 完整指南
- 平台文档
- CLI参考

本技术案例研究改编自发布在infisical.com/customers/hugging-face的原始案例研究。

---

> 本文由AI自动翻译，原文链接：[How Hugging Face Scaled Secrets Management for AI Infrastructure](https://huggingface.co/blog/scaling-secrets-management)
> 
> 翻译时间：2026-04-30 05:31
