---
title: TRL实现万亿参数模型增量同步，带宽骤降98%
title_original: 'Shipping a Trillion Parameters With a Hub Bucket: Delta Weight Sync
  in TRL'
date: '2026-05-27'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/delta-weight-sync
author: ''
summary: 本文介绍了TRL中一种高效的异步强化学习权重同步方法。传统方法需在每一步传输完整模型（如1T参数约1TB），但研究发现相邻优化步骤间约98%的bf16权重比特相同。通过仅编码并传输稀疏的delta权重（safetensors格式），并利用Hugging
  Face Hub Bucket作为共享存储，训练器与推理引擎无需直接连接。实验显示，Qwen3-0.6B模型每步数据传输从1.2GB降至20-35MB，大幅降低带宽成本与基础设施要求。
categories:
- AI基础设施
tags:
- 强化学习
- 权重同步
- TRL
- 模型训练优化
- Hugging Face
draft: false
translated_at: '2026-05-28T06:10:20.784588'
---

# 通过 Hub Bucket 传输万亿参数：TRL 中的 Delta 权重同步

太长不看版，因为你有模型要训练，我们理解这一点：

- 异步强化学习有一个不为人知的秘密：每一步，训练器都必须将整个模型传输到推理引擎。对于一个 7B 的 bf16 模型，这是 14 GB。对于一个前沿的 1T 模型检查点，这大约是 1 TB。每一步都是如此。
- 事实证明你并不需要这样做。在两个连续的强化学习优化器步骤之间，大约 99% 的 bf16 权重是比特相同的（在最坏情况下也从未低于 98%）。实际的 delta 非常小。
- 我们提交了一个 TRL PR，它将仅发生变化的部分编码为稀疏 safetensors 文件，上传到 Hugging Face Bucket，并通知 vLLM 获取它。在 Qwen3-0.6B 上，每步的数据传输量从 1.2 GB 降到了 20 到 35 MB。
- 锦上添花的是：我们运行了一个完全分离的训练流程，其中训练器在一台机器上，vLLM 位于一个 Hugging Face Space 中，Wordle 环境位于另一个 Space 中，而权重通过一个 Hub bucket 流动。无需共享集群，无需 RDMA，无需 VPN。

异步强化学习变得便宜多了。继续往下读。

## 1. 1 TB 的问题

如果你读过我们之前关于异步强化学习训练格局的文章，你已经知道关键点了。每个异步强化学习库，无论它如何拼写"actor 模型"或它的 NCCL 后端是什么颜色，最终都会遇到同一个根源：权重同步。

推理引擎运行的是第 N 步的策略。训练器刚刚完成了第 N+1 步。新的权重必须从一侧传输到另一侧，然后推理引擎才会无可救药地偏离策略。无论你运行的是同步还是异步，这都处于关键路径上：阻塞传输意味着 GPU 在浪费空闲算力，无法生成 Token。通过稀疏 delta 路径，你可以将空闲时间压缩到几秒钟，而且训练器甚至不需要等待推理引擎准备好：它只需在优化器步骤完成时发布"权重已就绪"并将权重上传到共享 bucket，而推理引擎则自行获取。

Fireworks 在他们的文章《前沿强化学习比你想象的更便宜》中给出了一个非常令人印象深刻的数字：对于一个前沿的 1T 参数检查点（fp8 格式，他们的设置），完整快照是 1024 GiB，而传统观点认为每次更新你的推理集群时都必须传输这么多数据。这个数字足以让人们开始绘制包含超大规模集群、RDMA 网络和专用跨区域链路的图表。他们测量的相邻检查点之间的平均 delta 为 20.3 GiB，占完整模型的 1.98%，并且"在连续检查点之间，超过 98% 的 bf16 格式权重保持比特等效"。

Cursor 的 Composer 2 报告讲述了一个类似的故事。他们在不同区域运行训练和推理，并通过一个共享的 S3 bucket（他们的原话）将它们连接起来，训练器在每个训练步骤都将压缩的权重差异上传到该 bucket。每个集群独立地从共享的 delta 链下载并重建，"无需与训练集群直接连接"。双方从不直接通信参数。Bucket 就是连接线。

两篇文章都同意三点，我们想慢慢重复一遍，因为这篇文章的其余部分本质上是对它们的忠实开源翻译：

1. 在相邻的两个强化学习步骤之间，大多数权重实际上并没有发生变化。
2. 如果你只发送发生变化的部分，你的带宽开销大约会减少两个数量级。
3. 如果你通过共享对象存储路由这些微小的差异，你就不再需要训练器和推理集群位于同一个数据中心。

唯一缺少的是一个你可以通过 pip install 安装的版本。所以我们写了一个。

## 2. 为什么 bf16 强化学习权重几乎总是稀疏的

在我们连接任何东西之前，有必要理解为什么整个游戏是可行的。"98% 的权重没有变化"这个说法听起来可疑，像是那种在演示中有效但在实际中会失效的数字。但事实并非如此。这源于 bf16 算术在强化学习使用的学习率下的工作方式。

一个 bf16 数字有 7 位尾数。在两个连续的 2 的幂之间，正好有 2^7 = 128 个可表示的值，因此 |w| 附近相邻 bf16 数字之间的间隔大约是 |w| · 2^(-7)。当一个更新低于该间隔的一半时，即当 |Δw| < |w|/256 时，该更新会被 bf16 转换吸收。这就是 PULSE 在其图 3 中绘制的"bf16 可见性阈值"。

现在看看 Adam 做了什么。在强化学习的学习率（例如 3×10^(-6)）下，对单个权重的更新是：Δw = -η · m̂ / (√v̂ + ε)

归一化步骤 m̂/(√v̂ + ε) 大约为 1 的量级，所以 |Δw| ≈ η ≈ 3×10^(-6)。对于大多数权重，|w| 大约在 10^(-2) 到 10^(-1) 之间（PULSE 报告代表性 LLM 权重的中位数为 0.019）。该量级下的阈值 |w|/256 大约在 4×10^(-5) 到 4×10^(-4) 之间，这比更新要大。

换句话说：优化器在低语，而 bf16 听不到。更新被四舍五入吸收，w 的字节表示没有变化，从推理引擎的角度来看，这个权重没有移动。将这一点乘以几亿个参数，你就免费获得了 >99% 的稀疏性，且零近似。

这正是 PULSE 论文（Mihai & Belilovsky, 2026）中正式提出的论点。他们定义了两个阈值。吸收界 10η 是 Adam 更新的保守最坏情况，而有效界 η 是你实际所处的区间。bf16 可见性阈值是 |w|/256。每当更新低于可见性阈值时，它就会被吸收，bf16 字节不会改变。他们的图 3 将两个边界与代表性 LLM 权重的云图绘制在一起，结论是明确的：在 η = 3×10^(-6) 时，吸收界本身已经低于模型中几乎每个权重的可见性阈值。他们在 Qwen2.5（0.5B/1.5B/7B）、Llama-3.2-3B 和 Gemma-3-4B 上进行了实证测量，一致发现平均每步稀疏性约为 99%，在 400 个训练步骤上的标准差为 0.2% 到 0.4%。最坏情况下的步骤保持在 98% 以上。所以 <1% 的变化不是一个幸运的测量结果；这是算术保证的。

我们不需要分析性地预测这一点（事实上，我们尝试从 Adam 的 m 和 v 统计量预测变化掩码，但召回率只有可怜的 30%，稍后会详细介绍）。我们只需要观察哪些字节发生了变化。这是一个每个参数的小型布尔张量，在优化器步骤附近计算。

## 3. HF Buckets 与架构

这就是故事的第二部分开始的地方，也是这篇文章从 Fireworks/Cursor 的翻译转变为 Hugging Face 相关内容的起点。

### 3.1 什么是 Bucket？

Bucket 是 Hub 上的一种仓库类型，专为高频对象存储设计。无需提交仪式，无需 PR 工作流，无需 LFS 怪癖。你可以添加文件、列出文件、下载文件。Python 接口是两个函数：

```python
from huggingface_hub import batch_bucket_files, download_bucket_files


batch_bucket_files("my-org/wordle-deltas", add=[(buffer, "deltas/step_000042.safetensors")])


download_bucket_files("my-org/wordle-deltas", files=[("deltas/step_000042.safetensors", local_path)])

```

就是这样。两个函数调用，你的权重就开始传输了。

在底层，存储桶由 Xet 提供支持，Xet 是 Hub 基于内容分块的存储层。Xet 会检查你上传的每个文件，根据其实际内容（而非固定偏移量）将其切分成块，并与存储桶中已有的内容进行去重。实际效果（在此场景下非常令人满意）是，即使我们懒得编写稀疏编码，只是每一步都上传完整的锚点，Xet 仍然只会传输发生变化的块。稀疏编码 + Xet 堆栈：我们只为变化的部分付费，且只需付费一次。

这是 Fireworks 和 Cursor 所使用的“共享 S3 存储桶”的开源等价方案，区别在于存储层已经了解内容哈希，你现有的 HF Token 已经拥有权限，并且它能与堆栈的其余部分（Spaces、数据集、模型）原生组合。

### 3.2 三个盒子

完整架构正好包含三个盒子和一个共享基础层：

- **训练器**。可以在任何地方。一个 GPU、八个 GPU、一台通过 USB 连接 H100 的笔记本电脑，我们都不会评判。拥有模型权重，运行优化器，生成稀疏增量。
- **HF 存储桶**。一个单一的仓库，两个前缀：`anchors/` 用于偶尔的完整快照，`deltas/` 用于期间的稀疏补丁。这是双方唯一达成一致的部分。
- **vLLM 部署服务器**。可以在任何地方，关键是**不一定**与训练器在同一位置。从存储桶拉取，应用增量，并提供部署。
- **环境**。以常规方式挂载到部署服务器上（HTTP、函数调用，无论你的环境支持什么）。

需要内化的特性，也是 Cursor 的论文大力推崇且在此处完全适用的：**训练器和部署服务器从不就权重进行通信**。它们交换一个包含 `{"repo_id": ..., "filename": ...}` 的小型 POST 请求，这就是整个控制平面。实际的字节传输发生在每一方与存储桶之间，并行进行，没有共享的网络结构。

这在实践中为何重要：

- 部署服务器可以在另一个区域、另一个云中，或者位于 Hugging Face Space 内的 NAT 之后。它不在乎。
- N 个推理副本可以从同一个存储桶拉取同一个增量，Xet 会在它们之间对所有字节进行去重。
- 训练器永远不需要知道存在多少个推理副本、它们在哪里，或者其中一个是否刚刚崩溃。

训练器写入。副本读取。Hub 负责管道。

## 4. 协议

现在我们可以深入细节。该协议包含四个部分：一种有线格式、一种存储桶布局、一个 30 行的 vLLM 扩展，以及一个训练器端的变化检测器。老实说，代码量比听起来要少。

### 4.1 Safetensors 作为有线格式

我们选择 `safetensors` 作为磁盘和有线格式。它已经是 Hub 上的标准检查点格式，所有合理的框架都能读取它，并且其头部携带任意字符串元数据。这个元数据字段正是我们隐藏协议的地方。

存储桶中有两种文件。

**锚点**看起来像一个正常的检查点：每个参数一个张量，完整的 bf16 权重，每 N 次同步写入一次（我们默认 N=10）。

```
anchors/step_000010.safetensors
  ├── model.layers.0.self_attn.q_proj.weight   (bf16, 完整)
  ├── model.layers.0.self_attn.k_proj.weight   (bf16, 完整)
  └── ...
元数据:
  sparse=False, model_version=10, sparsity=0.0

```

**增量**是有趣的部分。对于每个实际发生变化的参数，我们存储两个条目：一个平坦的 int32 张量（元素索引），以及一个 bf16 张量（这些索引处的值）。

```
deltas/step_000011.safetensors
  ├── model.layers.0.self_attn.q_proj.weight.indices   (int32, [num_changed])
  ├── model.layers.0.self_attn.q_proj.weight.values    (bf16,  [num_changed])
  ├── model.layers.0.mlp.gate_proj.weight.indices
  ├── model.layers.0.mlp.gate_proj.weight.values
  └── ...
元数据:
  sparse=True, model_version=11, sparsity=0.9938, changed_params=[...]

```

这种选择带来的一些好处：

- 增量是一个**文件**。你可以用 Python 中的 `safe_open(...)` 打开它，并检查其中的每个张量。没有专有的帧格式，没有长度前缀，没有版本握手。
- 元数据是自描述的。接收方读取 `sparse=True/False` 并进行分支。没有单独的清单。
- 在推理端通过 mmap 实现零拷贝，当你每隔几秒执行此操作时，这一点很重要。

节奏很简单：每 N 步创建一个锚点，期间创建增量。两者都进入同一个存储桶下的 `anchors/` 和 `deltas/` 前缀。每个新的推理副本只需要获取最新的锚点，然后重放之后的增量。

### 4.2 训练器端：来自优化器钩子的布尔掩码

训练器需要知道哪些 bf16 元素实际发生了变化。我们通过一个微小的 `BF16ChangeDetector` 来实现，它在优化器上注册了一个步骤前和步骤后钩子：

```python
class BF16ChangeDetector:
    def __init__(self, model, optimizer):
        self._pre_step_bf16: dict[str, torch.Tensor] = {}
        self._validated_masks: dict[str, torch.Tensor] = {}
        optimizer.register_step_pre_hook(self._pre_step_hook)
        optimizer.register_step_post_hook(self._post_step_hook)

    def _pre_step_hook(self, opt, args, kwargs):
        for p in self._params:
            self._pre_step_bf16[name_of(p)] = p.detach().to(torch.bfloat16).cpu().clone()

    def _post_step_hook(self, opt, args, kwargs):
        for p in self._params:
            self._validated_masks[name_of(p)] = (
                p.detach().to(torch.bfloat16).cpu() != self._pre_step_bf16[name_of(p)]
            )

```

PR 中的实际代码有更多管道（通过 `data_ptr()` 将优化器参数对象与模型参数匹配，因为 Accelerate 将它们包装为不同的 Python 对象），但思路很简单：快照、步骤、差异。

这是事实依据。我们**尝试过**更优雅的路径，即从 Adam 的 `m` 和 `v` 统计量预测掩码，直接使用 bf16 ULP 阈值。这在原则上可行。但在实践中，召回率约为 30%，这意味着我们会交付一个缺少三分之二实际更新的增量。Adam 的归一化足够混乱，以至于分析阈值并不严格。所以我们直接比较字节。这在训练器端花费一次模型 bf16 CPU 快照的成本，我们愿意承担。

新的 `sync_weight` 流程的四个阶段是：

1.  **推理继续运行时上传**。训练器将掩码元素编码到 safetensors 缓冲区中，并将其推送到存储桶。在整个步骤中，vLLM 仍在愉快地服务旧策略。
2.  **暂停 vLLM**。一个简短的 HTTP 调用，几百毫秒。
3.  **信号/update_weights**。发送存储桶坐标。vLLM 下载、应用、返回。
4.  **恢复**。vLLM 重新上线。

日志行说明了情况：

```
Delta: 1234567/200000000 elements changed (sparsity=99.38%)
[delta_engine] uploaded user/wordle-deltas/deltas/step_000042.safetensors (27.4 MB, ...)
Weight sync: done. Total 9.4s (inference paused 1.1s)

```

重要的行是括号中的内容。推理暂停了 **1.1 秒**。剩余的 9.4 秒用于上传，而这发生在部署服务器仍在生成 Token 时。使用 NCCL，我们将整个同步时间都算作暂停时间。在这里，我们将其作为后台时间支付。

### 4.3 vLLM 端：一个 30 行的扩展

vLLM 为此提供了一个干净的抽象，称为 `WeightTransferEngine`。我们实现了一个 `DeltaWeightTransferEngine`，其 `receive_weights` 方法在精神上是：

```python
def receive_weights(self, update_info, load_weights):
    download_bucket_files(update_info.repo_id, files=[(update_info.filename, local_path)])
    with safe_open(local_path, framework="pt", device="cpu") as f:
        meta = PatchMetadata.from_metadata_dict(f.metadata())
        if not meta.sparse:
            
            for name in f.keys():
                tensor = f.get_tensor(name)
                self._bf16_snapshot[name] = tensor.clone()
                load_weights([(name, tensor)])
        else:
            
            for name in json.loads(meta.changed_params):
                indices = f.get_tensor(f"{name}.indices").long()
                values = f.get_tensor(f"{name}.values")
                snap = self._bf16_snapshot[name].flatten()
                snap[indices] = values
                self._bf16_snapshot[name] = snap.reshape(self._bf16_snapshot[name].shape)
                load_weights([(name, self._bf16_snapshot[name])])

```

我们通过 vLLM 的 `--worker-extension-cls` 标志注册它，这意味着无需 fork vLLM。你只需将 TRL 安装到与 vLLM 相同的镜像中，将 CLI 指向我们的类，即可完成。

值得一提的是：vLLM 本身正在进行一项飞行中的工作，以原生支持稀疏权重传输，即 `vllm-project/vllm#40096`。它在 `WeightTransferEngine` 基类上直接添加了 `receive_sparse_weights()` 和 `trainer_send_sparse_weights()` 方法，补丁以 `(indices, values)` 形式编码，并通过 `index_copy_()` 就地应用，完全消除了 GPU/CPU 验证的往返开销。该 PR 报告称，对于 Qwen3-1.7B 上的稀疏补丁，传输量为 **0.16 MB，耗时 0.40 ms**，而完整的密集传输则为 **942 MB，耗时 192 ms**。

我们在推理端实现中有一个诚实的注意事项：我们保留了一份模型的 CPU bf16 快照，以便能够从稀疏的 `(indices, values)` 补丁中重建完整的张量，因为当前 vLLM 中的 `load_weights` 期望的是完整张量。一旦 `#40096`（或其后续版本）落地并暴露一个就地稀疏 `load_weights` 路径，我们就可以直接在 GPU 上应用索引，并丢弃快照！

## 5. 在 Spaces 上真正部署

这是让我们颇为得意的一部分。到目前为止，我们描述的一切都可以在你的笔记本电脑上运行，但通过 Hub 存储桶路由权重的意义在于，训练器和部署服务器不必彼此靠近。因此，我们使用三台机器运行了一次完全分离的训练，它们之间没有任何网络共享：

- 一台带有一个 GPU 的机器，运行 `trainer`。
- 一个 **Hugging Face Space**（Docker SDK，L4 GPU），运行带有我们扩展类的 `vLLM`。
- 第二个 **Hugging Face Space**（CPU），运行 Wordle 环境服务器，具有 256 个并发会话容量。
- 一个位于中间的 **Hub 存储桶**。

设置这一切实际上只需要几个 `hfCLI` 调用。vLLM Space 的 `Dockerfile` 本质上是上游的 vLLM 镜像，加上 `pip install trl@...`，再加上入口点：

```dockerfile
FROM vllm/vllm-openai:latest
RUN pip install "trl @ git+https://github.com/huggingface/trl.git@delta-weight-sync"
ENV VLLM_SERVER_DEV_MODE=1
EXPOSE 7860
ENTRYPOINT ["vllm", "serve", "Qwen/Qwen3-1.7B", \
    "--host", "0.0.0.0", "--port", "7860", \
    "--worker-extension-cls", "trl.experimental.async_grpo.delta_engine.DeltaWorkerExtension", \
    "--weight-transfer-config", "{\"backend\":\"nccl\"}", \
    "--max-model-len", "32768", \
    "--gpu-memory-utilization", "0.8"]

```

将其部署为一个 Space：

```bash
hf repos create $USER/vllm-wordle-inference \
    --type space --space-sdk docker --flavor l4x1 \
    --secrets HF_TOKEN=$HF_TOKEN
hf upload $USER/vllm-wordle-inference examples/scripts/openenv/vllm_space/ --type space

```

然后从地球上任何可以通信 HTTPS 的地方启动训练：

```bash
python examples/scripts/openenv/async_wordle.py \
    --vllm-server-url https://$USER-vllm-wordle-inference.hf.space \
    --env-url https://openenv-wordle.hf.space \
    --delta-sync-repo-id $USER/wordle-deltas \
    --model Qwen/Qwen3-1.7B

```

训练器从不打开端口。Space 从未看到训练器的 IP。Wordle 环境不知道它们两个的存在。它们都通过 Hub 通信。训练在即时的 EOS 合理性检查上收敛，然后在真实的 Wordle 部署上收敛：奖励上升，delta 负载保持在 20 到 35 MB 的范围内，每次同步的推理暂停窗口大约为一秒。完整的运行日志链接在随附的 PR 中。

## 6. 这实际上解锁了什么？

有几件事，我们认为它们意义重大。

**无需集群的异步 RL 训练。** 如果你有一个 GPU 和一个 Hugging Face 账户，你现在可以进行真正的分离式训练。你的训练器在 GPU 上；你的部署集群在 Spaces 中；你的环境在另一个 Space 中；权重通过一个存储桶移动。过去，这需要要么是共置设置（带来所有吞吐量上的妥协），要么是带有共享网络的真正集群。现在不再需要了。

**免费的多副本推理。** 启动两个 vLLM Space，或者十个。它们都从同一个存储桶拉取。Xet 内容寻址存储使得连续的锚点在存储时共享数据块（这可以防止你的存储桶爆炸），而 Hub 的边缘缓存使得重复下载同一个文件变得廉价。想要一个全球分布的部署集群？现在这是一个小的 DevOps 练习，而不是一个研究项目。

**一种可以用现有工具调试的线格式。** 一个 delta 是一个 safetensors 文件。你可以从 notebook 中 `safe_open` 它，列出它的键，检查索引，自己计算稀疏度。我们已经在不透明的 NCCL 流上花了足够多的时间在 tcpdump 上，因此很欣赏这一点。

**一条通往前沿规模的路径。** 20 到 35 MB 的数字是针对 Qwen3-0.6B 的。有趣的问题是，当你调高参数时，曲线会是什么样子。让我们做一下粗略计算。

以 Llama-3.1-405B 为例。在 bf16 下，它在磁盘上占用 **810 GB**。PULSE 在 RL 学习率下测量到每步平均约 99% 的稀疏度，因此实际的 delta 大约占参数的 1%。他们在部署中测量的编码在 7B 模型上达到了 **108 MB**，这是 PULSE 报告的约 **130 倍** 的缩减。线性扩展到 405B，每步的 delta 大约为 **6 GB**。

这在墙上时钟上能为你带来什么？NCCL 在集群内部很快，当然。假设一个慷慨的 100 GB/s 聚合广播带宽（多节点，RDMA，全套）。一次完整的同步是 **810 GB / 100 GB/s ≈ 8 秒** 的推理暂停，每一步。使用 delta 路径，训练器在后台将 6 GB 流式传输到存储桶，同时生成继续运行，而部署服务器实际的暂停窗口只是应用步骤，在这个规模上大约需要几秒钟。因此，即使在我们离开集群之前，delta 也将可见暂停减少了 4 倍，并将线上的字节数减少了约 130 倍。

现在离开集群。NCCL 完全不能跨云工作。一旦你想要一个在 `us-east` 的部署集群，另一个在 `eu-west`，也许一个在 Hugging Face Space 中，基于存储桶的路径就是 **唯一** 的路径。在 1 GB/s 的可用互联网带宽下，一次完整的广播需要 13 分钟；而 delta 只需 6 秒。

对于 Fireworks 框架中的 1 TB 级模型，他们自己测量的数字显示 **20.3 GiB 的 delta 对比 1024 GiB 的完整快照**，缩减了约 50 倍。PULSE 更紧凑的稀疏编码会进一步推动这一点（外推每个 delta 约 15 GB，更接近约 65 倍）。无论哪种方式，你都处于一个通过商品对象存储传输权重不再是权宜之计，而是唯一合理架构的境地。

## 7. 我们仍需处理的事项

我们并不假装这已经完成。以下是诚实的清单。

- 两个CPU bf16快照，多了一个。训练器保留一个（用于变化检测器），部署服务器保留一个（用于重建完整张量以支持vLLM的load_weights）。第一个快照我们暂时无法摆脱，除非有人找到严格的分析掩码——这比看起来要难。第二个快照将在vLLM获得稀疏load_weightsAPI后消失。PR即将提交。
- 固定锚点节奏。我们目前每NNN步转储一次完整锚点。自适应策略（“当累积漂移超过X时触发锚点”）将降低长序列运行中的锚点开销。
- 多节点FSDP2训练器。BF16ChangeDetector基于每个进程的优化器钩子构建。它应能干净地泛化到FSDP2，但我们尚未在多节点规模下进行测量。PR中有一个TODO标记，上面有我们的名字。
- 接入优化器。我们仅根据(m,v)(m, v)(m,v)预测掩码的尝试召回率较低，这意味着分析性bf16阈值的作用比教科书公式所暗示的更微妙。我们欢迎任何破解此问题的人提供建议。
- 与传输压缩叠加。稀疏safetensors和逐块gzip是正交的。我们尚未尝试将它们结合。尽管我们不期望获得巨大的压缩增益。

## 8. 尝试运行

- PR：huggingface/trl#5417。分支为delta-weight-sync。
- 完整Wordle示例：examples/scripts/openenv/async_wordle.py。
- Spaces Dockerfile：examples/scripts/openenv/vllm_space/和examples/scripts/openenv/wordle_space/。
- 背景阅读：我们的异步RL全景文章、Fireworks 1 TB文章、Cursor Composer 2报告。

---

> 本文由AI自动翻译，原文链接：[Shipping a Trillion Parameters With a Hub Bucket: Delta Weight Sync in TRL](https://huggingface.co/blog/delta-weight-sync)
> 
> 翻译时间：2026-05-28 06:10
