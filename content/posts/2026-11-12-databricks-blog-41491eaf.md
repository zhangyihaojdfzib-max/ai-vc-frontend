---
title: Eclipse Aerospace simplifies flight-data ingestion with Databricks
title_original: Eclipse Aerospace simplifies flight-data ingestion with Databricks
date: '2026-11-12'
source: Databricks Blog
source_url: https://www.databricks.com/blog/eclipse-aerospace-simplifies-flight-data-ingestion-databricks
author: ''
summary: '[翻译失败，原文如下]


  - Streamlined data access: Eclipse modernized nearly 20 years of flight telemetry
  to give service centers and engineers faster access to ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-13T09:19:35.955050'
---

[翻译失败，原文如下]

- Streamlined data access: Eclipse modernized nearly 20 years of flight telemetry to give service centers and engineers faster access to vital information.
- Improved performance & speed: Significantly boosted data processing speed, allowing large flight histories to be analyzed in minutes.
- Reduced costs & complexity: Eliminated redundant storage and multi-step processing systems, cutting operational overhead and simplifying management.

As organizations in aerospace, manufacturing, life sciences, and other data-intensive industries modernize their operations, they are bringing more sensor, telemetry, and scientific data into data platforms. But much of this data remains difficult to use at scale because it lives in specialized or proprietary formats that mainstream analytics engines cannot read directly. This creates a practical industry challenge: teams must choose between building slow, memory-intensive custom transformations, maintaining specialized connectors, or adding extra decoding stages before the data can be analyzed.

PySpark custom data sourcesoffer a simpler way forward. They let teams bring specialized formats into Spark using Python, without building a separate connector from scratch. For Eclipse Aerospace, a very light jet manufacturer and operator, partnering with Databricks offered a way to make nearly two decades of proprietary flight data more accessible to service centers and engineers without adding costly, always-on infrastructure. Databricks brought the serverless data platform and Spark integration, while Eclipse Aerospace contributed its existing flight-data decoders and aerospace expertise.

Together, Eclipse Aerospace and Databricks developed a more direct path from flight data to analytics, reducing the latency, duplication, and operational overhead of the previous multi-stage process while preserving the flexibility of Databricks Serverless.

## Eclipse Aerospace's data ingestion challenge

Eclipse Aerospace relies on Databricks to store nearly 20 years of flight data, totalling more than 3TB. It supports its service centers and engineers with data from more than a million flight hours, sourced and verified across multiple sources, including: near-real-time satellite telemetry; large bulk uploads of full flight histories; and external data sources. All of its telemetry is stored in proprietary file formats that require custom decoders, which are already developed in multiple languages, including Rust and Scala.

Before thePyspark custom data sourceswas available in Databricks Runtime 15.4 LTS, the Eclipse Aerospace team had three viable options for decoding and loading its proprietary file type into Databricks:

1. Load the files as binary types and split using Python user-defined functions (UDF)
2. Use a custom decoder in Scala on dedicated compute
3. Decode files into an intermediary file type prior to loading in Databricks

For simple custom file types, UDFs are a natural option. They trade performance for readability. However, where the message format has variable length, UDFs pose a real risk of running out of memory on long messages and could not be used. The existing Scala decoder could be used to implement a native Data Source v1/v2, but using it in Databricks required dedicated compute. Users expected to be able to upload and view data quickly, which would require keeping this compute to be always on, representing a larger cost than the other serverless options. This left the team with the final option of decoding the files into an intermediary file format, in this case, Avro, via a Rust-based decoder on AWS Lambda.

This solution was low-cost, but it:

- Introduced latency from the multi-hop ingestion pattern
- Duplicated schema logic between the Lambda decoder and the downstream Spark jobs that consumed the Avro output
- Cost the team pipeline observability; the Spark UI and job metrics only ever saw the world starting at the Avro landing zone, so engineers debugging a slow or failed ingest had to go find Lambda logs in a completely different part of the platform
- Meant paying to store both the original binary files and their Avro copies

## Why Databricks and PySpark Custom Data Sources Matter

Databricks was already Eclipse Aerospace’s platform for storing and processing flight data. The deciding advantage was the combination of Spark-native execution, the Pyspark custom data source, andDatabricks Serverless. Databricks Serverless automatically allocates and manages on-demand compute, so Eclipse Aerospace did not need to provision or keep dedicated infrastructure running. The PySpark custom data source made it possible to wrap the existing Rust decoder without building a JVM connector. Because decoding now runs inside Spark, the same platform provides the Spark UI, job metrics, and downstream Delta workflows instead of handing the critical ingest step to a separate Lambda pipeline.

Most data engineering relies on common data formats, but some of the most valuable data remains hidden in formats thatPySparkcannot access directly, such as HDF5 for scientific data and industry standards such as ARINC 429 for aerospace data. Databricks Serverless gives teams a flexible way to unlock that data at scale, while Rust-backed implementations can deliver performance beyond a pure-Python approach.

PySpark custom data sources lets you define a read/writable file format in pure Python, usable like any other data source. Its main benefit is simplicity, letting users define functions to read and write in pure Python, as well as define important characteristics like parallelization. The Eclipse Aerospace team took this a step further: by building a Rust-backed Python package, it delivered twice the benchmarked performance of a similar PyArrow-based pure-Python data source. Compared with a native Python implementation without Arrow, it delivered nearly 20x the performance.

The followingexample code repositorywalks through a custom data source forARINC 429. The accompanying code includes design decisions beyond the scope of this article, along with benchmark tests you can run yourself.

## How this became solvable with the PySpark Custom Data Sources

Apache Spark 4.0 shipped a Python Data Source API (referenced in Databricks documentation as PySpark custom data sources) that lets you register a custom format for batch or streaming data like:

Introduced in Apache Spark 4.0 and available on Databricks, the API is generally available from Databricks Runtime 15.4 LTS and is also supported on Serverless environment 2 and later. Because the API is implemented in Python, it does not require a separate JVM connector or JAR.

The API is a simplified interface for creating native data sources, with the user implementing a few classes and registering them with:

These decoders come in two flavors: native Python, and Apache Arrow format, the latter being the much more performant choice. Apache Arrow is a "language-independent columnar memory format for flat and nested data," making it an ideal interface between different languages sharing data objects. The API takes advantage of this by allowing users to returnpyarrow.RecordBatchobjects directly, and Spark will consume them as batches rather than materializing oneInternalRowper row.

This raised the question: could Python serve as the control layer, with Rust doing the heavy lifting of decoding while maintaining the Apache Arrow format throughout?

## Solution architecture overview

The architecture behind this is a single logical connector with a decode path that's almost entirely compiled code, and a Python layer thin enough that it makes minimal change to Eclipse Aerospace's existing Rust SDK. This thin Python layer is built with PyO3/Maturin as a standalone package, imported into pipelines and used just like any other source. To ensure the best performance and separation of concerns, the team followed a few architectural principles.

[翻译失败，原文如下]

![image1.png](/images/posts/e5cb578aaf25.png)

The decoder doesn't know Spark exists.The core Rust crate has no dependency on PyO3, Arrow, or Spark and only takes bytes, returning structured records. That allowed Eclipse Aerospace to port existing decode logic largely unchanged, as the SDK did not need to be rewritten for this, only wrapped.

Arrow is the only thing that crosses the foreign function interface (FFI) boundary, and it crosses it without copying.The Rust glue layer builds an ArrowRecordBatchusingarrow-rs, then hands it to Python as apyarrow.RecordBatchvia the Arrow C Data Interface. In doing this, there is no serialization step, as no bytes are re-encoded and no per-row Python objects are built. The buffers Rust allocated are the buffers Python reads.

The PySpark layer is intentionally lightweight.It parses options, decides how to partition (oneInputPartitionper input in the reference example), and defines the schema. In PySpark custom data sources,DataSource,DataSourceReader, and their streaming equivalents all have to be serializable, so Spark can pickle the reader instance and ship it to a worker. By making the PySpark layer lightweight, theDataSourceReaderinstance that Spark pickles and ships to a worker only ever holds plain Python state (file paths, an int for batch size). The PyO3-backed Rust object is constructed insideread(), after the reader has already arrived on the worker. It's never itself part of what gets pickled.

The native code ships as a Python wheel, built with Maturin. On Databricks that wheel is a build artifact, attached to a job or notebook environment as a normal Python dependency. Because the implementation is compiled, version and architecture compatibility require care, though a proper CI/CD process can manage this as demonstrated in the example repo.

## How the connector runs in Databricks

On Databricks Serverless, the runtime path is straightforward:

1. A proprietary telemetry file lands in cloud storage.
2. A Databricks Spark read invokes the registered PySpark custom data source for the custom format.
3. Spark running on Databricks creates a serializable reader containing the input path and read options, then schedules input partitions on workers.
4. Each worker constructs the Rust decoder insideread()and passes the file bytes to the compiled decoder.
5. Rust returns Arrow RecordBatches through the Arrow C Data Interface, avoiding serialization and per-row Python objects.
6. Spark running on Databricks consumes the batches and writes the decoded data to downstream tables such as Delta.
7. Decode errors, bad records, Spark UI stages, and job metrics remain visible within the Databricks workflow.

This is the key difference from the previous design: the original file is decoded as part of the Spark read rather than being copied to an intermediary Avro landing zone first.

## What impact did it have for Eclipse Aerospace

![image2.png](/images/posts/080f37a9a1ac.png)

By replacing the multi-stage Lambda and Avro workflow with a single Spark-native read, Eclipse Aerospace made flight data available faster while reducing infrastructure, storage, and operational overhead. The new Arrow-native PySpark custom data sources connector also brings decoding into Spark, improving visibility into pipeline performance and allowing schema and data quality logic to be managed in one place.

Implementing the custom data source has significantly simplified Eclipse Aerospace’s infrastructure, and the effects show up in four distinct places: latency, cost, observability, and engineering time.

Latency.Collapsing a multi-hop pipeline (upload, Lambda, decode, write Avro, read Avro, load to Delta) into a single Spark-native read removes several network hops and several points where a file sits in a queue waiting for the next stage to pick it up. The new connector can process records within a minute of file upload including startup time and can commonly process large, multi-gigabyte batches in parallel in under two minutes due to parallelism.

Cost.Removing the Lambda hop and the Avro intermediary removed a whole tier of infrastructure Eclipse Aerospace had to run, monitor, and pay for. They no longer pay to store two copies of every flight, the original binary and its Avro conversion, which on almost two decades of retained flight history is a meaningful amount of duplicated storage. This means the majority of files remain in Glacier storage on AWS, with easily repeatable decodes if the original data is ever needed again.

Observability.Because the decode step now happens inside Spark itself, it shows up in the Spark UI and standard job metrics like any other stage of a job. Eclipse Aerospace uses custom "badRecordsPath," which mimic the CSV/JSON loader, to capture misformatted data, and maintains extensive data quality pipelines that capture statistics directly from the decoder.

Engineering time.Schema logic used to be defined twice: once in the Lambda decoder that produced Avro, and again in the downstream Spark jobs that consumed it. Any change to the message format meant updating both, in two different codebases, with the risk of the two definitions drifting apart. With a single, versioned connector, the schema is defined once, next to the decode logic itself. This also means the same architectural pattern, a thin Python DataSource wrapping a Rust decoder, is now reusable for the other proprietary formats Eclipse Aerospace supports, rather than something that has to be reinvented per format.

Eclipse Aerospace's experience shows how specialized data formats can be brought into Databricks without creating a separate ingestion platform around them. By keeping the decoder in Rust, using Python as the integration layer, and passing records through Apache Arrow, the custom data source reads original files directly in Spark and remains compatible with the flexibility of Databricks Serverless.

For teams working with proprietary or industry-specific formats, the reusable pattern is simple. Engineers can keep domain-specific decoding logic close to the source format, expose it through a PySpark custom data source, and let Spark handle partitioning, execution, observability, and downstream processing.

Looking to get started? Take a look at the following:

- PySpark on Databricks
- PySpark custom data sources
- Connect to serverless compute

## Frequently asked questions

### What is a PySpark Custom Data Source?

A PySpark custom data source is a user-defined Spark data source implemented in Python. It lets teams read specialized file formats as part of a standard Spark workflow without building a separate JVM connector.

### What data ingestion problem does a custom Arrow-native PySpark Custom Data Source connector solve?

The Arrow-native PySpark custom data source connector ingests proprietary flight telemetry into Databricks without relying on a multi-stage pipeline, dedicated always-on compute, or duplicate Avro copies of the original files.

### What is Databricks Serverless?

Databricks Serverless is a fully managed compute service that lets you run workloads without provisioning or managing any infrastructure in your cloud account. Databricks automatically allocates, scales, and optimizes the compute resources for you.

### How does Databricks Serverless connect to the Arrow-native PySpark Custom Data Source connector?

The connector uses the Pyspark custom data sources to run file-reading logic inside Spark on serverless compute. Python handles the control flow, while Rust and Apache Arrow handle high-performance decoding and data transfer. This allows proprietary files to be read directly without dedicated always-on compute or an intermediary Avro pipeline. PySpark custom data sources are available in Databricks Runtime 15.4 LTS and above, or serverless environment version 2.

Manufacturing

---

> 本文由AI自动翻译，原文链接：[Eclipse Aerospace simplifies flight-data ingestion with Databricks](https://www.databricks.com/blog/eclipse-aerospace-simplifies-flight-data-ingestion-databricks)
> 
> 翻译时间：2026-11-13 09:19
