---
title: 推出swift-huggingface：Hugging Face的完整Swift客户端
title_original: 'Introducing swift-huggingface: The Complete Swift Client for Hugging
  Face'
date: '2025-12-05'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/swift-huggingface
author: null
summary: 本文宣布推出swift-huggingface，这是一个全新的Swift包，为Hugging Face Hub提供了完整的客户端解决方案。该库旨在解决此前swift-transformers存在的下载速度慢、缓存不共享、身份验证混乱等问题，提供了完整的Hub
  API覆盖、稳健的文件操作、与Python兼容的缓存、灵活的身份验证机制（包括TokenProvider模式和OAuth支持）以及即将到来的Xet存储后端支持，显著提升了在Swift生态中使用Hugging
  Face模型的可靠性和开发者体验。
categories:
- AI基础设施
tags:
- Swift
- Hugging Face
- 机器学习
- 客户端库
- 移动开发
draft: false
translated_at: '2026-01-06T01:00:27.739Z'
---

**推出 swift-huggingface：Hugging Face 的完整 Swift 客户端**

今天，我们宣布推出 swift-huggingface，这是一个新的 Swift 包，为 Hugging Face Hub 提供了一个完整的客户端。

您现在就可以将其作为独立包开始使用，并且它很快将集成到 swift-transformers 中，以替代其当前的 HubApi 实现。

**问题所在**

今年早些时候我们发布 swift-transformers 1.0 时，社区反馈非常明确：
- 下载速度慢且不可靠。大型模型文件（通常为几 GB）会在中途下载失败且无法恢复。开发者不得不手动下载模型并将其捆绑到应用中——这违背了动态模型加载的初衷。
- 与 Python 生态系统没有共享缓存。Python `transformers` 库将模型存储在 `~/.cache/huggingface/hub`。Swift 应用下载到的是不同位置，结构也不同。如果您已经使用 Python CLI 下载了一个模型，您还需要为 Swift 应用重新下载一遍。
- 身份验证令人困惑。Token 应该从哪里来？环境变量？文件？钥匙串？答案是“视情况而定”，而现有的实现并未清晰地说明这些选项。

**介绍 swift-huggingface**

swift-huggingface 是一次彻底的重写，专注于可靠性和开发者体验。它提供：
- 完整的 Hub API 覆盖——模型、数据集、空间、集合、讨论等
- 稳健的文件操作——进度跟踪、断点续传支持和正确的错误处理
- Python 兼容的缓存——在 Swift 和 Python 客户端之间共享已下载的模型
- 灵活的身份验证——`TokenProvider` 模式使凭据来源明确
- OAuth 支持——对需要用户身份验证的面向用户的应用提供一流支持
- Xet 存储后端支持（即将推出！）——基于分块的去重技术，显著加快下载速度

让我们看一些例子。

**使用 TokenProvider 实现灵活身份验证**

最大的改进之一是身份验证的工作方式。`TokenProvider` 模式明确了凭据的来源：

```swift
import HuggingFace

// 用于开发：从环境和标准位置自动检测
// 检查 HF_TOKEN、HUGGING_FACE_HUB_TOKEN、~/.cache/huggingface/token 等。
let client = HubClient.default

// 用于 CI/CD：明确的 Token
let client = HubClient(tokenProvider: .static("hf_xxx"))

// 用于生产应用：从钥匙串读取
let client = HubClient(tokenProvider: .keychain(service: "com.myapp", account: "hf_token"))
```

自动检测遵循与 Python `huggingface_hub` 库相同的约定：
- `HF_TOKEN` 环境变量
- `HUGGING_FACE_HUB_TOKEN` 环境变量
- `HF_TOKEN_PATH` 环境变量（指向 Token 文件的路径）
- `$HF_HOME/token` 文件
- `~/.cache/huggingface/token`（标准 HF CLI 位置）
- `~/.huggingface/token`（备用位置）

这意味着如果您已经使用 `hf auth login` 登录，swift-huggingface 将自动找到并使用该 Token。

**面向用户应用的 OAuth**

正在构建一个让用户使用其 Hugging Face 账户登录的应用吗？swift-huggingface 包含一个完整的 OAuth 2.0 实现：

```swift
import HuggingFace

// 创建身份验证管理器
let authManager = try HuggingFaceAuthenticationManager(
    clientID: "your_client_id",
    redirectURL: URL(string: "yourapp://oauth/callback")!,
    scope: [.openid, .profile, .email],
    keychainService: "com.yourapp.huggingface",
    keychainAccount: "user_token"
)

// 用户登录（呈现系统浏览器）
try await authManager.signIn()

// 与 Hub 客户端一起使用
let client = HubClient(tokenProvider: .oauth(manager: authManager))

// Token 在需要时会自动刷新
let userInfo = try await client.whoami()
print("Signed in as: \(userInfo.name)")
```

OAuth 管理器处理钥匙串中的 Token 存储、自动刷新和安全登出。无需再手动管理 Token。

**可靠的下载**

现在，通过适当的进度跟踪和断点续传支持，下载大型模型变得简单明了：

```swift
// 带进度跟踪的下载
let progress = Progress(totalUnitCount: 0)
Task {
    for await _ in progress.publisher(for: \.fractionCompleted).values {
        print("Download: \(Int(progress.fractionCompleted * 100))%")
    }
}
let fileURL = try await client.downloadFile(
    at: "model.safetensors",
    from: "microsoft/phi-2",
    to: destinationURL,
    progress: progress
)
```

如果下载中断，您可以恢复它：

```swift
// 从上次中断处恢复
let fileURL = try await client.resumeDownloadFile(
    resumeData: savedResumeData,
    to: destinationURL,
    progress: progress
)
```

对于下载整个模型仓库，`downloadSnapshot` 会处理一切：

```swift
let modelDir = try await client.downloadSnapshot(
    of: "mlx-community/Llama-3.2-1B-Instruct-4bit",
    to: cacheDirectory,
    matching: ["*.safetensors", "*.json"], // 仅下载您需要的文件
    progressHandler: { progress in
        print("Downloaded \(progress.completedUnitCount) of \(progress.totalUnitCount) files")
    }
)
```

快照函数会跟踪每个文件的元数据，因此后续调用仅下载已更改的文件。

**与 Python 共享缓存**

还记得我们提到的第二个问题吗？“与 Python 生态系统没有共享缓存。” 现在这个问题已经解决了。

swift-huggingface 实现了与 Python 兼容的缓存结构，允许在 Swift 和 Python 客户端之间无缝共享：

```
~/.cache/huggingface/hub/
├── models--deepseek-ai--DeepSeek-V3.2/
│   ├── blobs/
│   │   └── <etag> # 实际文件内容
│   ├── refs/
│   │   └── main # 包含提交哈希
│   └── snapshots/
│       └── <commit_hash>/
│           └── config.json # 符号链接 → ../../blobs/<etag>
```

这意味着：
- **一次下载，随处使用。** 如果您已经使用 `hf` CLI 或 Python 库下载了一个模型，swift-huggingface 将自动找到它。
- **内容寻址存储。** 文件按其 ETag 存储在 `blobs/` 目录中。如果两个修订版本共享同一个文件，它只存储一次。
- **符号链接提高效率。**

快照目录包含指向数据块的符号链接，在保持清晰文件结构的同时最小化磁盘占用。

缓存位置遵循与 Python 相同的环境变量约定：
`HF_HUB_CACHE`
环境变量`HF_HOME`
环境变量 + `/hub`
`~/.cache/huggingface/hub`
（默认）

你也可以直接使用缓存：
```swift
let cache = HubCache.default
// 检查文件是否已缓存
if let cachedPath = cache.cachedFilePath(
    repo: "deepseek-ai/DeepSeek-V3.2",
    kind: .model,
    revision: "main",
    filename: "config.json"
) {
    let data = try Data(contentsOf: cachedPath)
    // 无需任何网络请求即可使用缓存文件
}
```
为防止多个进程访问同一缓存时发生竞争条件，swift-huggingface 使用了文件锁（`flock(2)`）。

**前后对比**
以下是使用旧版 HubApi 下载模型快照的情况：
```swift
// 之前：swift-transformers 中的 HubApi
let hub = HubApi()
let repo = Hub.Repo(id: "mlx-community/Llama-3.2-1B-Instruct-4bit")
// 无进度跟踪，无法恢复，错误被吞没
let modelDir = try await hub.snapshot(
    from: repo,
    matching: ["*.safetensors", "*.json"]
) { progress in
    // 进度对象存在但并非总是准确
    print(progress.fractionCompleted)
}
```
而使用 swift-huggingface 的相同操作：
```swift
// 之后：swift-huggingface
    to: cacheDirectory,
    matching: ["*.safetensors", "*.json"],
        // 每个文件的准确进度
        print("\(progress.completedUnitCount)/\(progress.totalUnitCount) files")
    }
)
```
API 相似，但实现完全不同——它基于 `URLSession` 下载任务构建，具备适当的委托处理、恢复数据支持和元数据跟踪。

**不止于下载**
但等等，还有更多！swift-huggingface 包含一个完整的 Hub 客户端：
```swift
// 列出热门模型
let models = try await client.listModels(
    filter: "library:mlx",
    sort: "trending",
    limit: 10
)
// 获取模型详情
let model = try await client.getModel("mlx-community/Llama-3.2-1B-Instruct-4bit")
print("Downloads: \(model.downloads ?? 0)")
print("Likes: \(model.likes ?? 0)")
// 处理集合
let collections = try await client.listCollections(owner: "huggingface", sort: "trending")
// 管理讨论
let discussions = try await client.listDiscussions(kind: .model, "username/my-model")
```
这还不是全部！swift-huggingface 提供了与 Hugging Face 推理服务提供商交互所需的一切，让你的应用能够即时访问数百个机器学习模型，这些模型由世界一流的推理服务提供商提供支持：
```swift
import HuggingFace
// 创建客户端（使用从环境变量自动检测的凭证）
let client = InferenceClient.default
// 根据文本提示词生成图像
let response = try await client.textToImage(
    model: "black-forest-labs/FLUX.1-schnell",
    prompt: "A serene Japanese garden with cherry blossoms",
    provider: .hfInference,
    width: 1024,
    height: 1024,
    numImages: 1,
    guidanceScale: 7.5,
    numInferenceSteps: 50,
    seed: 42
)
// 保存生成的图像
try response.image.write(to: URL(fileURLWithPath: "generated.png"))
```
请查看 README 以获取支持功能的完整列表。

**下一步计划**
我们正在积极从两个方面推进：
1.  **与 swift-transformers 集成**。我们正在进行一个拉取请求，旨在用 swift-huggingface 替换 `HubApi`。这将为所有使用 swift-transformers、mlx-swift-lm 及更广泛生态系统的用户带来可靠的下载体验。如果你维护一个基于 Swift 的库或应用，并希望采用 swift-huggingface，请联系我们——我们很乐意提供帮助。
2.  **通过 Xet 实现更快的下载**。我们正在添加对 Xet 存储后端的支持，该后端支持基于数据块的去重，并能显著加快大型模型的下载速度。更多信息即将发布。

**尝试一下**
将 swift-huggingface 添加到你的项目中：
```swift
dependencies: [
    .package(url: "https://github.com/huggingface/swift-huggingface.git", from: "0.4.0")
]
```
我们期待你的反馈。如果你曾对 Swift 中的模型下载感到困扰，请尝试一下并告诉我们效果如何。你的使用体验报告将帮助我们确定下一步改进的优先级。

**资源**
感谢 swift-transformers 社区的反馈，这些反馈塑造了这个项目，也感谢所有提交问题并分享经验的人。这是为你们而做的。❤️


> 本文由AI自动翻译，原文链接：[Introducing swift-huggingface: The Complete Swift Client for Hugging Face](https://huggingface.co/blog/swift-huggingface)
> 
> 翻译时间：2026-01-06 01:00
