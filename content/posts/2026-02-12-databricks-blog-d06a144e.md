---
title: 统一Databricks与云成本：实现全面TCO可见性
title_original: 'Getting the Full Picture: Unifying Databricks and Cloud Infrastructure
  Costs'
date: '2026-02-12'
source: Databricks Blog
source_url: https://www.databricks.com/blog/getting-full-picture-unifying-databricks-and-cloud-infrastructure-costs
author: ''
summary: 本文探讨了在Databricks多云数据平台上实现总体拥有成本（TCO）可见性的挑战与方法。TCO由平台成本和底层云基础设施成本构成，但这两部分数据通常分散在Databricks系统表和云提供商账单中，尤其在经典计算模式下难以统一。文章详细分析了Azure和AWS上整合成本数据的复杂性，如数据源差异、时间粒度不匹配、标签解析困难等，并指出建立自动化的成本数据管道对于财务治理和投资回报率衡量至关重要。
categories:
- AI基础设施
tags:
- Databricks
- 云成本管理
- 总体拥有成本
- 数据平台
- 多云架构
draft: false
translated_at: '2026-02-13T04:34:14.037871'
---

## 理解 Databricks 的总体拥有成本

理解您在人工智能和数据投资方面的价值至关重要——然而，超过 52% 的企业未能严格衡量投资回报率 [Futurm]。要获得完整的 ROI 可见性，需要将平台使用情况和云基础设施连接起来，形成清晰的财务视图。通常，数据是可用的，但却是分散的，因为当今的数据平台必须支持日益增多的存储和计算架构。

在 Databricks 上，客户正在管理多云、多工作负载和多团队的环境。在这些环境中，拥有一致、全面的成本视图对于做出明智决策至关重要。

在 Databricks 等平台上实现成本可见性的核心是总体拥有成本这一概念。

在 Databricks 等多云数据平台上，TCO 由两个核心部分组成：

*   **平台成本**，例如计算和托管存储，是通过直接使用 Databricks 产品产生的成本。
*   **云基础设施成本**，例如虚拟机、存储和网络费用，是通过支持 Databricks 所需的底层云服务使用而产生的成本。

使用无服务器产品时，理解 TCO 会变得简单。因为计算由 Databricks 管理，云基础设施成本会捆绑到 Databricks 成本中，您可以直接在 Databricks 系统表中获得集中的成本可见性（尽管存储成本仍由云提供商收取）。

然而，理解经典计算产品的 TCO 则更为复杂。在这种情况下，客户直接通过云提供商管理计算，这意味着需要同时核对 Databricks 平台成本和云基础设施成本。在这些情况下，有两个不同的数据源需要处理：

1.  Databricks 中的系统表（AWS|AZURE|GCP）将提供操作层面的工作负载元数据和 Databricks 使用情况。
2.  云提供商的成本报告将详细说明云基础设施的成本，包括折扣。

这些数据源共同构成了完整的 TCO 视图。随着您的环境在众多集群、作业和云账户中扩展，理解这些数据集成为成本可观测性和财务治理的关键部分。

## TCO 的复杂性

衡量 Databricks TCO 的复杂性因云提供商暴露和报告成本数据的方式不同而加剧。理解如何将这些数据集与系统表连接以生成准确的成本关键绩效指标，需要深入了解云计费机制——许多专注于 Databricks 的平台管理员可能不具备这种知识。在此，我们将深入探讨如何衡量 Azure Databricks 和 AWS 上的 Databricks 的 TCO。

### Azure Databricks：利用第一方计费数据

由于 Azure Databricks 是 Microsoft Azure 生态系统中的第一方服务，与 Databricks 相关的费用会直接出现在 Azure 成本管理中，与其他 Azure 服务并列，甚至包括 Databricks 特定的标签。Databricks 成本会出现在 Azure 成本分析 UI 中，并作为成本管理数据。

然而，Azure 成本管理数据不会包含 Databricks 系统表中更深层次的工作负载元数据和性能指标。因此，许多组织寻求将 Azure 计费导出数据引入 Databricks。

然而，要完全连接这两个数据源既耗时又需要深厚的领域知识——大多数客户根本没有时间去定义、维护和复制这项工作。造成这种情况的挑战包括：

*   必须设置基础设施以实现成本数据自动导出到 ADLS，然后才能在 Databricks 中直接引用和查询。
*   Azure 成本数据是每日汇总和刷新的，这与系统表按小时级别不同——必须仔细去重并匹配时间戳。
*   连接两个数据源需要解析高基数的 Azure 标签数据，并识别正确的连接键（例如，ClusterId）。

### AWS 上的 Databricks：协调市场费用和基础设施成本

在 AWS 上，虽然 Databricks 成本确实会出现在成本和使用情况报告以及 AWS 成本资源管理器中，但与 Azure 不同，成本是以更聚合的 SKU 级别表示的。此外，只有当通过 AWS 市场购买 Databricks 时，Databricks 成本才会出现在 CUR 中；否则，CUR 将仅反映 AWS 基础设施成本。

在这种情况下，对于拥有 AWS 环境的客户来说，理解如何将 AWS CUR 与系统表进行协同分析变得更为关键。这使得团队能够将基础设施支出、DBU 使用情况和折扣与集群和工作负载级别的上下文一起分析，从而在 AWS 账户和区域间创建更完整的 TCO 视图。

然而，将 AWS CUR 与系统表连接也可能具有挑战性。常见的痛点包括：

*   基础设施必须支持定期的 CUR 重新处理，因为 AWS 每天会多次刷新和替换当前月份以及任何先前有变化的计费周期的成本数据（没有主键）。
*   AWS 成本数据涵盖多种行项目类型和成本字段，需要在聚合前注意选择每种使用类型（按需、Savings Plan、预留实例）的正确有效成本。
*   将 CUR 与 Databricks 元数据连接需要仔细归因，因为基数可能不同，例如，共享的通用集群在 AWS 使用数据中表示为单行，但可能映射到系统表中的多个作业。

## 简化 Databricks TCO 计算

在生产规模的 Databricks 环境中，成本问题很快会超出总体支出的范畴。团队希望在上下文中理解成本——基础设施和平台使用如何与实际工作负载和决策相关联。常见问题包括：

*   无服务器作业的总成本与经典作业相比如何？
*   哪些集群、作业和仓库是云托管虚拟机的最大消耗者？
*   随着工作负载的扩展、转移或整合，成本趋势如何变化？

回答这些问题需要将云提供商的财务数据与 Databricks 的操作元数据结合起来。然而如上所述，团队需要维护定制的数据管道，并具备云和 Databricks 计费的详细知识库才能实现这一点。

为了支持这一需求，Databricks 正在推出**云基础设施成本现场解决方案**——一个在 Databricks 平台内自动化摄取并统一分析云基础设施和 Databricks 使用数据的开源解决方案。

通过为跨 Databricks 无服务器和经典计算环境的 TCO 分析提供统一的基础，该现场解决方案帮助组织获得更清晰的成本可见性并理解架构权衡。工程团队可以跟踪云支出和折扣，而财务团队则可以识别主要成本驱动因素的业务背景和归属。

在下一节中，我们将详细介绍该解决方案的工作原理以及如何开始使用。

![Data intelligence reshapes industries](/images/posts/a64d41133ca4.png)

## 技术解决方案详解

尽管组件名称可能不同，但面向 Azure 和 AWS 客户的云基础设施成本现场解决方案遵循相同的原则，可以分解为以下组件：

*   将成本和使用数据导出到云存储
*   使用 Lakeflow Spark 声明式管道在 Databricks 中摄取和建模数据
*   使用 AI/BI 仪表板可视化完整的 TCO（Databricks 及相关云提供商成本）

AWS 和 Azure 的现场解决方案都非常适合在单一云内运营的组织，但也可以使用 Delta Sharing 为多云 Databricks 客户组合使用。

### Azure Databricks 现场解决方案

面向 Azure Databricks 的云基础设施成本现场解决方案由以下架构组件组成：

Azure Databricks 解决方案架构

![Numbered steps align to high level steps listed below](/images/posts/a2ac7d04f6aa.png)

要部署此解决方案，管理员必须在 Azure 和 Databricks 上拥有以下权限：

-   **Azure**：创建 Azure 成本导出所需的权限。在资源组内创建以下资源的权限：
    -   存储账户
    -   容器
    -   访问连接器
    -   角色分配
-   **Databricks**：创建以下资源的权限：
    -   存储凭据
    -   外部位置

-   创建 Azure 成本导出的权限。
-   在资源组内创建以下资源的权限：
    -   存储账户
    -   容器
    -   访问连接器
    -   角色分配

-   存储账户
-   容器
-   访问连接器
-   角色分配

-   创建以下资源的权限：
    -   存储凭据
    -   外部位置

-   存储凭据
-   外部位置

GitHub 仓库提供了更详细的设置说明；然而，从高层次来看，Azure Databricks 的解决方案包含以下步骤：

1.  **[Terraform]** 部署 Terraform 以配置依赖组件，包括一个存储账户、外部位置和卷。此步骤的目的是配置一个用于导出 Azure 计费数据的位置，以便 Databricks 可以读取。如果已存在预配置的卷，此步骤是可选的，因为 Azure 成本管理导出位置可以在下一步中配置。
2.  **[Azure]** 配置 Azure 成本管理导出，将 Azure 计费数据导出到存储账户，并确认数据成功导出。此步骤的目的是利用 Azure 成本管理的导出功能，使 Azure 计费数据以易于使用的格式（例如 Parquet）提供。
    -   已配置 Azure 成本管理导出的存储账户
    -   Azure 成本管理导出自动将成本文件传送到此位置
        ![Azure Cost Management Export automatically delivers cost files to this location](/images/posts/c3c61bdf9e90.png)
3.  **[Databricks]** 配置 Databricks Asset Bundle (DAB) 以部署 Lakeflow 作业、Spark 声明式管道和 AI/BI 仪表板。此步骤的目的是摄取和建模 Azure 计费数据，以便使用 AI/BI 仪表板进行可视化。
4.  **[Databricks]** 在 AI/BI 仪表板中验证数据并验证 Lakeflow 作业。这最后一步是实现价值的地方。客户现在拥有一个自动化流程，使他们能够查看其湖仓架构的总拥有成本！

-   此步骤的目的是配置一个用于导出 Azure 计费数据的位置，以便 Databricks 可以读取。如果已存在预配置的卷，此步骤是可选的，因为 Azure 成本管理导出位置可以在下一步中配置。

**[Azure]** 配置 Azure 成本管理导出，将 Azure 计费数据导出到存储账户，并确认数据成功导出

-   此步骤的目的是利用 Azure 成本管理的导出功能，使 Azure 计费数据以易于使用的格式（例如 Parquet）提供。

已配置 Azure 成本管理导出的存储账户

![Azure Cost Management Export automatically delivers cost files to this location](/images/posts/c3c61bdf9e90.png)

-   此步骤的目的是摄取和建模 Azure 计费数据，以便使用 AI/BI 仪表板进行可视化。

-   这最后一步是实现价值的地方。客户现在拥有一个自动化流程，使他们能够查看其湖仓架构的总拥有成本！

显示 Azure Databricks 总拥有成本的 AI/BI 仪表板

![Databricks costs are visible with associated Microsoft charge](/images/posts/3392852870e1.png)

### AWS 上的 Databricks 解决方案

AWS 上的 Databricks 解决方案由多个架构组件组成，这些组件协同工作，以摄取 AWS 成本与使用情况报告 (CUR) 2.0 数据，并使用奖牌架构将其持久化在 Databricks 中。

要部署此解决方案，必须在 AWS 和 Databricks 上具备以下权限和配置：

-   **AWS**：创建 CUR 的权限。创建 Amazon S3 存储桶的权限（或在现有存储桶中部署 CUR 的权限）。注意：该解决方案需要 AWS CUR 2.0。如果您仍有 CUR 1.0 导出，AWS 文档提供了升级所需的步骤。
-   **Databricks**：创建以下资源的权限：
    -   存储凭据
    -   外部位置

-   创建 CUR 的权限。
-   创建 Amazon S3 存储桶的权限（或在现有存储桶中部署 CUR 的权限）。
-   注意：该解决方案需要 AWS CUR 2.0。如果您仍有 CUR 1.0 导出，AWS 文档提供了升级所需的步骤。

-   创建以下资源的权限：
    -   存储凭据
    -   外部位置

-   存储凭据
-   外部位置

![Numbered steps align to high level steps listed below](/images/posts/1294d6ec424d.png)

GitHub 仓库提供了更详细的设置说明；然而，从高层次来看，AWS Databricks 的解决方案包含以下步骤。

1.  **[AWS]** AWS 成本与使用情况报告 (CUR) 2.0 设置。此步骤的目的是利用 AWS CUR 功能，使 AWS 计费数据以易于使用的格式提供。
2.  **[Databricks]** Databricks Asset Bundle (DAB) 配置。此步骤的目的是摄取和建模 AWS 计费数据，以便使用 AI/BI 仪表板进行可视化。
3.  **[Databricks]** 审查仪表板并验证 Lakeflow 作业。这最后一步是实现价值的地方。客户现在拥有一个自动化流程，使他们能够获取其湖仓架构的总拥有成本！

-   此步骤的目的是利用 AWS CUR 功能，使 AWS 计费数据以易于使用的格式提供。

-   此步骤的目的是摄取和建模 AWS 计费数据，以便使用 AI/BI 仪表板进行可视化。

-   这最后一步是实现价值的地方。客户现在拥有一个自动化流程，使他们能够获取其湖仓架构的总拥有成本！

![Databricks costs are visible with associated AWS charge](/images/posts/8a559e6a3969.png)

## 实际应用场景

正如 Azure 和 AWS 解决方案所展示的，此类解决方案支持许多实际应用场景，例如：

-   在优化了 CPU 和/或内存使用率低的作业后，识别并计算总成本节约。
-   识别在未预留的虚拟机类型上运行的工作负载。
-   识别网络和/或本地存储成本异常高的工作负载。

作为一个实际例子，一家拥有数千个工作负载的大型组织的 FinOps 从业者可能被要求通过寻找成本达到一定数额但 CPU 和/或内存利用率较低的工作负载，来寻找易于实现的优化机会。由于该组织的总拥有成本信息现在通过云基础设施成本现场解决方案呈现，该从业者可以将这些数据与节点时间线系统表（AWS、AZURE、GCP）关联，以呈现此信息，并在优化完成后准确量化成本节约。最重要的问题取决于每个客户的业务需求。例如，通用汽车使用此类解决方案来回答上述许多问题以及更多问题，以确保他们从其湖仓架构中获得最大价值。

## 关键要点

实施云基础设施成本现场解决方案后，组织可以获得一个单一的、可信的总拥有成本视图，该视图结合了 Databricks 和相关的云基础设施支出，消除了跨平台手动成本对账的需要。使用该解决方案可以回答的问题示例包括：

-   我的 Databricks 使用成本在云提供商和 Databricks 之间的细分情况如何？
-   运行一个工作负载的总成本是多少，包括虚拟机、本地存储和网络成本？
-   一个工作负载在无服务器计算上运行与在经典计算上运行时的总成本差异是多少？

平台和FinOps团队可以直接在Databricks中按工作区、工作负载和业务部门深入分析完整成本，从而更轻松地将使用情况与预算、责任模型和FinOps实践对齐。由于所有底层数据都以治理表的形式提供，团队可以构建自己的成本应用程序——仪表板、内部应用或使用内置AI助手如Databricks Genie——加速洞察生成，并将FinOps从定期报告工作转变为持续运行的运营能力。

## 后续步骤与资源

立即从GitHub部署Cloud Infra Cost Field Solution（链接在此，支持AWS和Azure），全面掌握您的Databricks总支出。实现全面可视后，您可以优化Databricks成本，包括考虑采用无服务器方案以实现自动化基础设施管理。

作为本解决方案一部分创建的仪表板和流水线，提供了一种快速有效的方法，可开始将Databricks支出与其他基础设施成本一并分析。然而，每个组织的费用分配和解读方式不同，因此您可以根据需要进一步定制模型和转换逻辑。常见的扩展包括：将基础设施成本数据与额外的Databricks系统表（AWS|AZURE|GCP）关联以提高归因准确性；在使用实例池时构建逻辑以分离或重新分配共享虚拟机成本；以不同方式建模虚拟机预留实例；或纳入历史回填以支持长期成本趋势分析。与任何超大规模云成本模型一样，除了默认实现之外，流水线仍有大量定制空间，以适应内部报告、标记策略和FinOps要求。

Databricks交付解决方案架构师（DSA）加速各组织的数据与AI计划。他们提供架构领导力，优化平台的成本与性能，提升开发者体验，并推动项目成功执行。DSA弥合初始部署与生产级解决方案之间的差距，与数据工程、技术负责人、高管及其他利益相关者等各类团队紧密合作，确保提供定制化解决方案并加速实现价值。若希望获得DSA在您数据与AI旅程中提供的定制执行计划、战略指导和支持，请联系您的Databricks客户团队。

## 下一步是什么？

---

> 本文由AI自动翻译，原文链接：[Getting the Full Picture: Unifying Databricks and Cloud Infrastructure Costs](https://www.databricks.com/blog/getting-full-picture-unifying-databricks-and-cloud-infrastructure-costs)
> 
> 翻译时间：2026-02-13 04:34
