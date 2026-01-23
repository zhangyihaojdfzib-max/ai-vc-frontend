---
title: Apache Spark® 4.1 正式发布
title_original: Introducing Apache Spark® 4.1
date: '2025-12-22'
source: Databricks Blog
source_url: https://www.databricks.com/blog/introducing-apache-sparkr-41
author: ''
summary: 本文介绍了 Apache Spark 4.1 的发布，并重点展示了 Databricks 作为统一数据、分析和 AI 平台的整体架构与生态。文章详细列举了
  Databricks 平台的核心产品模块（如数据工程、人工智能、数据科学、商业智能等）、面向各行业的解决方案、丰富的学习资源与合作伙伴网络。其核心在于通过湖仓一体架构，为企业提供一个开放、安全、高性能的数据与AI基础平台，支持从数据管理、治理到机器学习与生成式AI应用构建的全流程。
categories:
- AI基础设施
tags:
- Apache Spark
- Databricks
- 湖仓一体
- 数据平台
- AI基础设施
draft: false
translated_at: '2026-01-06T18:15:23.227Z'
---

# 介绍 Apache Spark® 4.1

## 现已在 Databricks Runtime 18.0 Beta 中提供

发布日期：2025年12月22日

作者：Sandy Ryza, Jerry Peng, Wenchen Fan, Herman van Hövell, Hyukjin Kwon, Allison Wang, Serge Rielau, DB Tsai, Xiao Li 和 Reynold Xin

- 结构化流处理中的实时模式为实时流处理实现了关键的亚秒级延迟，对于无状态工作负载甚至可达个位数毫秒。
- SQL脚本和递归CTE正式发布，极大地扩展了基于SQL的复杂数据分析能力。

Spark 4.1 亮点一览

- **Spark声明式管道（SDP）**：一个新的声明式框架，您只需定义数据集和查询，Spark会处理执行图、依赖排序、并行性、检查点和重试。使用Python和SQL编写管道，通过CLI编译和运行，并使用Spark Connect支持多语言客户端。
- **结构化流处理实时模式（RTM）**：首次官方支持结构化流查询以实时模式运行，实现连续、亚秒级延迟的处理。对于无状态任务，延迟甚至可降至个位数毫秒。Spark 4.1从无状态、单阶段的Scala查询开始，包括Kafka源以及Kafka和Foreach接收器，并为未来版本中更广泛的支持指明了方向。
- **PySpark UDF和数据源**：新的Arrow原生UDF和UDTF装饰器，可实现高效的PyArrow执行，无需Pandas转换开销；此外还有Python数据源谓词下推以减少数据移动。Spark 4.1还引入了Python工作节点日志记录，可捕获UDF日志并通过内置的表值函数暴露它们。
- **Spark Connect**：Spark ML on Connect 已针对Python客户端正式发布，具备更智能的模型缓存和内存管理。Spark 4.1还通过zstd压缩的protobuf计划、分块Arrow结果流以及增强的对大型本地关系的支持，提高了大型工作负载的稳定性。
- **SQL增强**：SQL脚本功能已正式发布并默认启用，具有改进的错误处理和更清晰的声明。VARIANT类型已正式发布，支持分解功能以加速半结构化数据的读取，此外还支持递归CTE以及新的近似数据草图（KLL和Theta）。

## Spark声明式管道

Spark声明式管道（SDP）是Apache Spark 4.1中的一个新组件，旨在让开发人员专注于数据转换，而非管理显式依赖关系和管道执行。通过使用声明式方法，开发人员现在可以定义所需的表状态以及数据如何在它们之间流动。SDP随后会处理所有执行细节，例如按正确顺序排序、实现并行性、处理检查点和管理重试。

- **声明式抽象**：SDP将开发方式从定义命令式步骤转变为使用**流式表**（由流式查询管理的表）和**物化视图**（定义为特定查询结果的表）来描述期望的结果。
- **智能图执行**：Pipeline Runner在执行前会分析整个数据流图。这使得系统能够进行整体预验证以尽早捕获模式不匹配、自动解析依赖关系，并内置处理重试和并行化。
- **Python、SQL和Spark Connect API**：可以使用Python、SQL或两者结合来定义Pipeline。SDP还公开了Spark Connect API，允许用任何语言编写客户端。`spark-pipelines`命令行界面支持从多个文件编译和执行Pipeline。

以下是一个使用SDP的Python API定义的Pipeline示例。它从Kafka主题摄取原始订单数据，刷新客户维度表，并将它们连接起来创建订单事实表。

基于数据依赖关系，SDP将并行执行更新`customers`和`raw_orders`的查询，然后在上游查询完成后执行更新`fact_orders`的查询。

## Structured Streaming中的实时模式（RTM）

Apache Spark 4.1是低延迟流处理的一个重要里程碑，首次在Structured Streaming中官方支持**实时模式**。随着实时模式SPIP的批准和SPARK-53736的完成，Spark现在支持专为超低延迟执行而设计的连续流查询。

### 什么是实时模式？

Spark Structured Streaming中的实时模式提供连续、低延迟的处理，实现p99延迟在个位数毫秒范围内。用户只需进行简单的配置更改即可激活此功能，无需重写代码或更换平台，并可继续使用熟悉的Structured Streaming API。

![](/images/posts/cbf39f5dc614.png)

通过如此简单的更改，用户可以获得数量级更优的延迟。

### Spark 4.1支持哪些内容？

Spark 4.1支持用Scala编写的无状态/单阶段流查询。支持的源包括Kafka，支持的接收器是Kafka Sink和ForeachSink。支持的运算符包括大多数无状态运算符和函数，例如Union和广播流-静态连接。查询仅限于Update输出模式。

关于设计和性能特性的更深入讨论，请参阅**实时模式公告博客**。

## Python UDF和数据源

Apache Spark 4.1对PySpark生态系统进行了重大改进，重点是通过原生Arrow集成提升性能，并通过改进的可调试性增强开发者体验。以下是4.1发布分支中新的Python UDF、UDTF和数据源功能的深入探讨。

### 高性能Arrow原生UDF和UDTF

Spark 4.1引入了两个新的装饰器，允许开发者绕过Pandas转换开销，直接处理PyArrow数组和批次。这对于依赖Arrow内存格式效率的用户来说是一个至关重要的进步。

#### Arrow UDF（@arrow_udf）

新的`arrow_udf`允许您定义接受和返回`pyarrow.Array`对象的标量函数。这非常适合计算密集型任务，您可以直接利用`pyarrow.compute`函数。

#### Arrow UDTF（@arrow_udtf）

用户定义表函数（UDTF）也获得了Arrow处理。`@arrow_udtf`装饰器支持向量化表函数。您的`eval`方法现在可以一次性处理整个`pyarrow.RecordBatch`，而不是逐行迭代。

### 可调试性：Python工作进程日志记录（SPARK-53754）

调试Python UDF历来很困难，因为标准日志常常丢失在执行器的stdout/stderr中。Spark 4.1引入了一项专用功能来捕获和查询这些日志。通过启用`spark.sql.pyspark.worker.logging.enabled`，您可以在UDF内部使用标准的Python日志记录模块。Spark会捕获这些日志，并通过一个新的表值函数`python_worker_logs()`按会话公开它们。

### Python数据源API：谓词下推

Python数据源API（在Spark 4.0中引入）在4.1版本中变得更加强大，增加了**谓词下推**功能。您现在可以在`DataSourceReader`中实现`pushFilters`方法。这使得您的数据源能够从查询优化器接收过滤条件（例如，`id > 100`）并在源级别处理它们；从而减少数据传输并提高查询速度。

Spark Connect在Spark 4.1中继续成熟，重点关注远程客户端的稳定性、可扩展性和功能完整性。此版本为Python客户端上的Spark ML提供了**正式发布（GA）**支持，同时进行了多项底层改进，使Spark Connect对于大型复杂工作负载更加稳健。

### Connect上的Spark ML正式发布

在Spark 4.1中，Spark Connect上的Spark ML现已正式发布，适用于Python客户端。新的模型大小估计机制允许Connect服务器智能地管理驱动程序上的模型缓存。根据估计的大小，模型会被缓存在内存中，或在需要时安全地溢出到磁盘，从而显著提高机器学习工作负载的稳定性和内存利用率。除了这一核心增强功能外，Spark 4.1还包括许多错误修复、更清晰的错误消息和扩展的测试覆盖范围，从而带来更可靠的开发者体验。

### 改进的可扩展性和稳定性

Spark 4.1引入了多项关键改进，使Spark Connect在大规模下更具弹性：

- Protobuf执行计划现在使用zstd进行压缩，提高了处理大型复杂逻辑计划时的稳定性，同时减少了网络开销。
- Arrow查询结果通过gRPC分块流式传输，提高了返回大型结果集时的稳定性。
- 通过移除之前2 GB的大小限制，扩展了对本地关系的支持，使得可以从更大的内存对象（如Pandas DataFrame或Scala集合）创建DataFrame。

这些增强功能共同使Spark Connect成为多语言客户端、交互式工作负载和分布式环境中大规模数据处理的更坚实基础。

Spark 4.1进一步扩展并完善了SQL语言功能，弥合了数据仓库和数据工程之间的差距。此版本侧重于扩展Spark SQL的过程能力，并标准化复杂数据的处理。

在4.0版本中预览后，**SQL脚本**现已**正式发布（GA）**并默认启用。这将Spark SQL转变为一个强大的可编程环境，允许您直接在SQL中编写复杂的控制流逻辑（循环、条件等）。

**4.1中的新功能**：我们引入了`CONTINUE HANDLER`用于复杂的错误恢复，以及多变量`DECLARE`语法以使代码更清晰。

**VARIANT数据类型**现已正式发布，提供了一种标准化的方式来存储半结构化数据（如JSON），而无需严格的模式。

Spark 4.1中的一个主要性能增强是**分片**。此功能会自动提取Variant列中经常出现的字段，并将它们存储为单独的、有类型的Parquet字段。这种选择性提取通过允许引擎跳过为经常查询的字段读取完整的二进制大对象，从而显著减少了I/O。

**性能基准测试**：

- 与标准VARIANT（未分片）相比，**读取性能快8倍**。
- 与将数据存储为JSON字符串相比，**读取性能快30倍**。
- 注意：启用分片可能会导致写入时间慢20-50%，这是为读取密集型分析优化的权衡。

![](/images/posts/aa979aef7bff.png)

Spark 4.1 新增了标准的 **递归公共表表达式** SQL 语法。这使得您能够完全在 SQL 内遍历层次化数据结构——例如组织架构图或图拓扑——从而简化从遗留系统的迁移。

### 新的近似数据草图

我们已将近似聚合能力扩展到 HyperLogLog 之外。Spark 4.1 新增了用于 **KLL（分位数）** 和 **Theta** 草图的原生 SQL 函数。这些函数允许以最小的内存开销，对海量数据集进行高效的近似集合操作（并集、交集）。

Apache Spark 4.1 是 Apache Spark 社区推动的又一个强劲发布周期的成果。新的 **Spark 声明式管道** 将数据工程的重点从“如何做”转向了“做什么”。结构化流处理中的 **实时模式** 提供了关键的低延迟性能，响应时间达到个位数毫秒。随着 PySpark 生态系统的不断发展，此版本引入了高性能的 Arrow 原生 UDF 和 UDTF，通过利用原生 Arrow 集成消除了序列化开销。此外，**Python 工作进程日志记录** 使得调试 UDF 变得更加容易，缓解了开发人员过去的痛点。用于机器学习的 **Spark Connect** 通过缓存和智能内存使用，以及使用 zstd 对执行计划进行 protobuf 压缩，提高了机器学习工作负载的稳定性，包括智能模型管理。最后，SQL 语言随着丰富的 **SQL 脚本逻辑控制** 而更加成熟，增加了高性能的 **VARIANT 数据类型** 和递归表表达式。

我们要感谢所有为 Spark 4.1 做出贡献的人，无论是通过提出设计、提交和分类 JIRA、审查拉取请求、编写测试、改进文档，还是在邮件列表中分享反馈。有关完整变更列表以及本文未涵盖的其他引擎级改进，请查阅官方的 **Spark 4.1.0 发布说明**。

![](/images/posts/0270af1b647d.png)

**获取 Apache Spark® 4.1：** 它是完全开源的 - 可从 spark.apache.org 下载。其许多功能已在 Databricks Runtime 17.x 中提供，现在它们随 Runtime 18.0 Beta 版开箱即用。要在托管环境中探索 Spark 4.1，请在启动集群时选择“18.0 Beta”，您将在几分钟内运行 Spark 4.1。

![](/images/posts/06157093bb52.png)

##

---

> 本文由AI自动翻译，原文链接：[Introducing Apache Spark® 4.1](https://www.databricks.com/blog/introducing-apache-sparkr-41)
> 
> 翻译时间：2026-01-06 18:00
