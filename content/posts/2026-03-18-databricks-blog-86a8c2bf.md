---
title: 从Apache Airflow迁移至Databricks Lakeflow Jobs实战指南
title_original: How to move from Apache Airflow® to Databricks Lakeflow Jobs
date: '2026-03-18'
source: Databricks Blog
source_url: https://www.databricks.com/blog/how-move-apache-airflowr-databricks-lakeflow-jobs
author: ''
summary: 本文为已在生产环境中使用Apache Airflow的团队提供了迁移至Databricks原生编排器Lakeflow Jobs的详细执行指南。文章通过对比表清晰展示了Airflow常见模式（如XComs、Sensors、动态任务映射）在Lakeflow中的对应实现方式，并推荐了增量式迁移策略。核心在于将编排逻辑内置于湖仓平台，利用Lakeflow
  Jobs的事件驱动触发器、任务参数化及数据驱动的协调模型，实现从外部调度器到数据优先编排范式的转变。
categories:
- AI基础设施
tags:
- 数据编排
- Apache Airflow
- Databricks
- Lakeflow
- 数据工程
draft: false
translated_at: '2026-03-19T04:58:17.240794'
---

在上一篇文章《从 Apache Airflow® 到 Lakeflow：数据优先的编排》中，我们围绕数据和湖仓而非外部调度器重新定义了编排。本文在此基础上展开，重点关注那些已在生产环境中运行 Airflow 并希望迁移到 Databricks 原生编排器 **Lakeflow Jobs** 的团队的执行细节。

本指南既适用于从 Airflow 迁移的实践者，也适用于生成 Lakeflow Jobs 工作流的编程 Agent（智能体）。其目标是展示当编排成为 Databricks 内部湖仓本身的一部分时，如何自然地表达这些相同的工作流。

![](/images/posts/b727d5d071ea.png)

## Airflow 到 Lakeflow Jobs 迁移对照表

下表总结了常见的 Airflow 编排模式如何对应到 Lakeflow Jobs，以及迁移是直接转换还是概念重构。

| Airflow 模式 | 主要用途 | Lakeflow Jobs 对应项 | 迁移指导 |
| :--- | :--- | :--- | :--- |
| XComs | 在任务间传递小型控制元数据 | 任务值 / UC 表 / 任务输出引用（例如，`tasks.my_query.output.updated_rows`） | 了解更多 |
| Sensors | 等待文件或条件 | 文件到达触发器 / 表更新触发器 | 用内置触发器替换轮询传感器 |
| Backfills | 为历史日期重新运行 | 作业回填 + 参数 | 将时间视为数据，使用参数化回填 |
| Branching | 条件任务执行 | 条件（if/else）任务 | 用 If-Else 任务替换 `task.branch` |
| Dynamic task mapping | 运行时扇出 | For-each 任务 | 当任务数量取决于运行时数据时使用 for‑each |

## 迁移策略：增量式，而非一次性

大多数团队采用增量式迁移，而非整体替换 Airflow。常见方法包括：

*   从自包含或事件驱动的工作流开始
*   尽早迁移文件到达和数据驱动的触发器
*   初期保持稳定的 Airflow 流水线不变
*   避免重写成熟、低风险的作业

Lakeflow Jobs 的设计旨在迁移期间共存，并在能带来最大价值的地方接管编排职责。

**检查清单**

*   **包含小型元数据的 XComs** → 任务值；**包含数据的 XComs** → Unity Catalog 表或卷。
*   **文件传感器/资产** → 文件到达或表更新触发器（数据位于 UC 中时）。
*   **执行日期宏（`ds` 等）** → 显式参数 + 回填运行。
*   **分支（`@task.branch`）** → 条件任务。
*   **动态任务映射** → for‑each 任务（当扇出是数据驱动时）。
*   （可选）通过 Python Asset Bundles 管理作业和模式，以确保环境一致性。

## Lakeflow Jobs 概述

从 Airflow 迁移时，理解塑造 **Lakeflow Jobs** 工作方式的一些核心假设是有益的：

**控制平面 vs 数据平面**
数据平面中的操作（查询、读取、写入和转换）驱动计算使用。而触发器、任务值和参数等控制平面操作则不驱动计算。

**作业是编排的单位**
*   作业封装了任务和依赖关系；跨作业的协调通常使用数据（表、文件），而非跨 DAG 信号。
*   这使设计从“DAG 与 DAG 通信”转变为“生产者写入表，消费者作业在该表变更时触发”。
*   对于需要作业间显式调用的场景，存在“运行作业”任务，但它是对数据驱动协调模型的补充，而非替代。

**触发器是一等公民**
*   文件到达和表更新触发器是内置功能，而非通过长时间运行的传感器实现。
*   这默认将编排从基于轮询转变为事件驱动。

这些假设解释了为什么一些 Airflow 模式可以直接转换，而另一些则被有意简化或替换。

## 迁移步骤

### 1. XComs：控制用任务值，数据用表

**Airflow：用于小型控制元数据的 XComs**
在 Apache Airflow 中，`XComs` 用于在 DAG 运行内的任务之间传递小段元数据。一个在任务间传递小值的极简 Airflow 示例：

```python
@task
def extract():
    return {"customer_id": 123, "status": "active"}

@task
def transform(customer_info):
    # use the XCom value
    customer_id = customer_info["customer_id"]
    ...
```

这对于小型 ID、值、标志和计数效果很好，但当许多任务依赖 XComs 或推送大负载时，就变得难以理解。

**Lakeflow：控制用任务值，数据用表**
在 Lakeflow Jobs 中，`task values` 扮演了控制元数据的 XCom 角色。作业和任务通常通过 `asset bundles` 定义，其实现位于笔记本或 Python 文件中。定义两个任务和一个依赖关系的 Bundle 代码片段（Python）：

```python
from databricks.asset_bundles import task, job

@task
def producer():
    # set a task value
    task.set_value("customer_id", 123)
    task.set_value("status", "active")

@task
def consumer():
    # read the task value
    cust_id = task.get_value("customer_id")
    status = task.get_value("status")
    # use them...
```

生产者笔记本：

```python
# producer notebook
task.set_value("customer_id", 123)
task.set_value("status", "active")
```

消费者笔记本：

```python
# consumer notebook
cust_id = task.get_value("customer_id")
status = task.get_value("status")
```

任务值在 Lakeflow Jobs UI 中按运行可见，并且仅限于小负载，这使其非常适合标志、计数器和 ID。对于较大的对象或可重用输出，任务应写入 `Unity Catalog` 表或视图：

```python
@task
def producer():
    # write data to a table
    spark.sql("""
        INSERT INTO my_catalog.my_schema.customers
        SELECT 123 AS customer_id, 'active' AS status
    """)

@task
def consumer():
    # read from the table
    df = spark.table("my_catalog.my_schema.customers")
    ...
```

💡**经验法则**：仅将任务值用于控制元数据；任何看起来像数据的东西都应放入表、视图或卷中。

**迁移技巧**
*   简单的 XComs → 任务值。
*   携带数据框或大型 JSON 的 XComs → 改为读写 Unity Catalog。
*   避免重现重度依赖 XCom 的 DAG；依靠湖仓作为共享状态。

### 2. 传感器和资产转为文件和表触发器

**Airflow：文件传感器和资产**
文件驱动流水线的典型 Airflow 模式：

```python
from airflow.sensors.filesystem import FileSensor

wait_for_file = FileSensor(
    task_id="wait_for_file",
    filepath="/path/to/file.csv",
    poke_interval=30,
    timeout=60*60,
)
```

这会占用一个工作节点槽进行轮询，并且当多个消费者依赖相同数据时，通常与自定义资产跟踪结合使用。

**Lakeflow：文件到达触发器**
显示文件到达触发器的代码片段：

```yaml
triggers:
  - type: file_arrival
    storage: uc_volume
    path: /Volumes/my_catalog/my_schema/my_volume/incoming/
    pattern: "*.csv"
    min_files: 1
```

笔记本实现：

```python
# notebook triggered by file arrival
df = spark.read.csv("/Volumes/my_catalog/my_schema/my_volume/incoming/")
```

平台处理触发器状态、去抖和冷却，您不再需要长时间运行的传感器或外部调度器来监视文件。

**Lakeflow：表更新触发器（资产式调度）**
当生产者写入 Unity Catalog 表时，消费者可以基于表更新触发，而非基于时间的调度。

```yaml
triggers:
  - type: table_update
    table: my_catalog.my_schema.my_table
```

💡**经验法则**：尽可能基于文件到达或表更新触发作业；仅在真正需要时才使用调度。

**迁移技巧**
*   文件传感器 → UC 位置或卷上的文件到达触发器。
*   资产注册表 → 带有表更新触发器的 Unity Catalog 表。
*   非数据事件 → 显式的外部触发器或参数。

### 3. 执行日期转为参数和回填运行

**Airflow：执行日期和 `ds`**
Airflow 鼓励使用执行日期进行模板化逻辑：

```sql
-- Airflow SQL template
SELECT * FROM events WHERE event_date = '{{ ds }}'
```

回填由 Airflow 的调度器和执行日期驱动；逻辑隐式依赖于调度器的时间概念。

**Lakeflow：显式参数和回填**
在 Lakeflow Jobs 中，“逻辑运行日期”应建模为参数。带参数的作业定义（bundles）：

```yaml
parameters:
  - name: run_date
    default: "2024-01-01"
```

注意：如果您想使用 Airflow 风格的 `{{ds}}` 或 `{{ execution_date }}`，也可以使用 `{{ job.trigger.time.iso_date }}`，而不是上面示例中的硬编码数据。

SQL 使用该参数：

```sql
-- Lakeflow SQL (in a notebook)
SELECT * FROM events WHERE event_date = :run_date
```

要进行回填，您可以定义一组参数值，并通过 UI 或 API 对它们运行回填，而不是依赖隐式的调度器追赶。参数定义一次，在触发回填运行时在运行时被覆盖。

💡**经验法则**：将时间视为数据；将其建模为参数，显式传递给任务，并通过参数范围驱动回填。

**迁移技巧**
*   用参数（例如 `:run_date`）替换 `{{ ds }}` 及相关宏。
*   使任务对于给定的参数集具有幂等性，以确保回填安全。
*   使用 Lakeflow 回填运行，而非重新创建调度器驱动的追赶逻辑。

### 4. 分支和动态映射转为条件和 for‑each 任务

**Airflow：分支和动态任务映射**
使用 `@task.branch` 进行分支：

```python
@task.branch
def decide_route():
    if condition:
        return "task_a"
    else:
        return "task_b"
```

使用 `expand()` 进行运行时扇出的动态任务映射：

```python
@task
def generate_ids():
    return [1, 2, 3, 4, 5]

@task
def process(id):
    ...

process.expand(id=generate_ids())
```

**Lakeflow：条件任务**

Lakeflow Jobs 使用条件任务实现数据驱动的分支

check_qualitynotebook 会发出一个任务值：

该图清晰地展示了分支，决策逻辑通过数据（任务值）而非内嵌的 Python 控制流来表达。

💡经验法则：当路径由参数或任务值的布尔表达式决定时，使用条件任务。

Lakeflow：使用 for‑each 任务实现运行时扇出

当任务数量取决于运行时数据时，使用 for‑each 任务实现扇出。

generate_itemsnotebook：

process_itemnotebook 将当前项视为 `{{input}}`（或根据语言包装器对应的运行时变量）。

💡经验法则：当扇出由运行时数据驱动时，使用 for‑each；当扇出在设计时固定时，保持任务静态。

- @task.branch → 使用任务值或参数的条件任务。
- 动态任务映射 → 由任务值或表驱动的 for‑each 任务。
- 大型迭代元数据 → 表/卷；小型 ID/索引 → 任务值。

### 5. （可选）使用 Python 资产包进行程序化生成

许多 Airflow 部署会动态生成 DAG（每个表或 SQL 文件对应一个 DAG），并通过约定和脚本来管理环境差异。Python 资产包提供了一种结构化的方式，以编程方式生成作业和相关资源。

​示例：每个 SQL 文件对应一个作业：

您可以将其与修改器结合使用，以按环境调整通知、执行身份或重试策略，从而在将作业定义保留在 Python 中的同时，集中管理标准。​

💡经验法则：使用程序化生成来编码平台约定，而非隐藏一次性变通方案。

## 后续步骤

如果您当前正在运行 Airflow，请选择一个依赖传感器、XCom 或动态任务映射的 DAG，并使用一个触发器、一个 for-each 任务和显式参数重新实现它。这通常足以内化 Lakeflow Jobs 的心智模型。

- 克隆并运行本指南中使用的完整工作示例
- 了解更多关于数据优先编排的信息
- 探索 Lakeflow Jobs 文档

克隆并运行本指南中使用的完整工作示例

了解更多关于数据优先编排的信息

探索 Lakeflow Jobs 文档

---

> 本文由AI自动翻译，原文链接：[How to move from Apache Airflow® to Databricks Lakeflow Jobs](https://www.databricks.com/blog/how-move-apache-airflowr-databricks-lakeflow-jobs)
> 
> 翻译时间：2026-03-19 04:58
