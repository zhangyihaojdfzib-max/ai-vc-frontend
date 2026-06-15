---
title: 在Hugging Face上部署语音到语音系统指南
title_original: Deploying Speech-to-Speech on Hugging Face
date: '2024-10-22'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/s2s_endpoint
author: ''
summary: 本文详细介绍了如何将语音到语音（S2S）系统部署到Hugging Face推理端点。S2S是一个级联流水线，结合了语音活动检测、语音转文本、语言模型和文本转语音组件，支持多语言。由于运行S2S需要大量计算资源，文章推荐使用Hugging
  Face推理端点租用GPU虚拟机。作者逐步指导读者构建自定义Docker镜像，并部署到推理端点，为复杂模型流水线提供了可扩展且高效的部署方案。
categories:
- AI基础设施
tags:
- Hugging Face
- 语音到语音
- 推理端点
- Docker部署
- AI基础设施
draft: false
translated_at: '2026-06-15T07:20:17.089581'
---

# 在 Hugging Face 上部署语音到语音系统

## 简介

语音到语音（S2S）是 Hugging Face 推出的一个令人兴奋的新项目，它结合了多个先进模型，创造出一种无缝、近乎神奇的体验：你说话，系统就会用合成语音回应。

该项目实现了一个级联流水线，利用 Hugging Face 平台上 Transformers 库中可用的模型。该流水线包含以下组件：

1. 语音活动检测（VAD）
2. 语音转文本（STT）
3. 语言模型（LM）
4. 文本转语音（TTS）

更棒的是，S2S 支持多语言！目前支持英语、法语、西班牙语、中文、日语和韩语。你可以以单语言模式运行流水线，或使用 `auto` 标志进行自动语言检测。查看仓库了解更多详情。

```
> 👩🏽‍💻：这些都太棒了，但我该如何运行 S2S？
> 🤗：问得好！

```

运行语音到语音系统需要大量计算资源。即使在高性能笔记本电脑上，你也可能会遇到延迟问题，尤其是在使用最先进的模型时。虽然强大的 GPU 可以缓解这些问题，但并非每个人都有条件（或意愿！）搭建自己的硬件。

这时，Hugging Face 的推理端点（IE）就派上用场了。推理端点允许你租用配备 GPU（或其他所需硬件）的虚拟机，并且只需为系统运行的时间付费，为部署语音到语音这类高性能应用提供了理想的解决方案。

在这篇博文中，我们将逐步指导你将语音到语音系统部署到 Hugging Face 推理端点。我们将涵盖以下内容：

- 了解推理端点，以及设置 IE 的不同方式概述，包括自定义容器镜像（这是 S2S 所需要的）
- 为 S2S 构建自定义 Docker 镜像
- 将自定义镜像部署到 IE，并体验 S2S 的乐趣！

## 推理端点

推理端点提供了一种可扩展且高效的方式来部署机器学习模型。这些端点允许你以最少的设置来服务模型，并利用各种强大的硬件。推理端点非常适合部署需要高性能和可靠性的应用，而无需管理底层基础设施。

以下是几个关键特性，更多详情请查看文档：

- **简单性**：得益于 IE 对 Hugging Face 平台上模型的直接支持，你可以在几分钟内启动并运行。
- **可扩展性**：你无需担心扩展问题，因为 IE 会自动扩展，包括缩容至零，以处理不同的负载并节省成本。
- **可定制性**：你可以自定义 IE 的设置以处理新任务。更多内容见下文。

推理端点支持所有 Transformers 和 Sentence-Transformers 任务，也可以支持自定义任务。以下是 IE 的设置选项：

1. **预构建模型**：直接从 Hugging Face 平台快速部署模型。
2. **自定义处理器**：为更复杂的流水线定义自定义推理逻辑。
3. **自定义 Docker 镜像**：使用你自己的 Docker 镜像来封装所有依赖项和自定义代码。

对于较简单的模型，选项 1 和 2 非常理想，使使用推理端点部署变得非常简单。然而，对于像 S2S 这样的复杂流水线，你需要选项 3 的灵活性：使用自定义 Docker 镜像部署我们的 IE。

这种方法不仅提供了更大的灵活性，还通过优化构建过程和收集必要数据来提高性能。如果你正在处理复杂的模型流水线，或者想要优化应用部署，本指南将提供有价值的见解。

## 在推理端点上部署语音到语音系统

让我们开始吧！

### 构建自定义 Docker 镜像

为了开始创建自定义 Docker 镜像，我们首先克隆了 Hugging Face 的默认 Docker 镜像仓库。这是为推理任务部署机器学习模型的一个很好的起点。

```bash
git clone https://github.com/huggingface/huggingface-inference-toolkit

```

### 为什么要克隆默认仓库？

- **坚实基础**：该仓库提供了一个专为推理工作负载优化的预构建基础镜像，这提供了一个可靠的起点。
- **兼容性**：由于该镜像旨在与 Hugging Face 的部署环境保持一致，这确保了在部署你自己的自定义镜像时能够平滑集成。
- **易于定制**：该仓库提供了一个干净且结构化的环境，使得根据应用的特定需求定制镜像变得容易。

你可以在这里查看我们的所有更改

### 为语音到语音应用定制 Docker 镜像

克隆仓库后，下一步是调整镜像以支持我们的语音到语音流水线。

1. **添加语音到语音项目**

为了平滑集成项目，我们将语音到语音代码库和任何所需数据集作为子模块添加。这种方法提供了更好的版本控制，确保在构建 Docker 镜像时始终可以使用确切版本的代码和数据。

通过将数据直接包含在 Docker 容器中，我们避免了每次实例化端点时都需要下载数据，这显著减少了启动时间，并确保系统是可复现的。数据存储在 Hugging Face 仓库中，便于跟踪和版本管理。

```bash
git submodule add https://github.com/huggingface/speech-to-speech.git
git submodule add https://huggingface.co/andito/fast-unidic

```

1. **优化 Docker 镜像**

接下来，我们修改了 Dockerfile 以满足我们的需求：

- **精简镜像**：我们移除了与我们的用例无关的包和依赖项。这减小了镜像大小，并减少了推理过程中的不必要开销。
- **安装依赖**：我们将 `requirements.txt` 的安装从入口点移到了 Dockerfile 本身。这样，依赖项在构建 Docker 镜像时就会安装完成，从而加快部署速度，因为这些包在运行时无需再安装。

1. **部署自定义镜像**

完成修改后，我们构建了自定义镜像并将其推送到 Docker Hub：

```bash
DOCKER_DEFAULT_PLATFORM="linux/amd64" docker build -t speech-to-speech -f dockerfiles/pytorch/Dockerfile . 
docker tag speech-to-speech andito/speech-to-speech:latest 
docker push andito/speech-to-speech:latest

```

构建并推送 Docker 镜像后，它就可以在 Hugging Face 推理端点中使用了。通过使用这个预构建的镜像，端点可以更快地启动并更高效地运行，因为所有依赖项和数据都已预先打包在镜像中。

## 设置推理端点

使用自定义 Docker 镜像只需要稍微不同的配置，请随时查看文档。我们将介绍在 GUI 和 API 中实现此方法的方式。

前置步骤

1. 登录：https://huggingface.co/login
2. 请求访问 `meta-llama/Meta-Llama-3.1-8B-Instruct`
3. 创建细粒度 Token：https://huggingface.co/settings/tokens/new?tokenType=fineGrained
   - 选择对受限仓库的访问权限
   - 如果你使用 API，请确保选择管理推理端点的权限

![细粒度 Token](/images/posts/3039dac1b9eb.png)

- 选择对受限仓库的访问权限
- 如果你使用 API，请确保选择管理推理端点的权限

### 推理端点 GUI

1. 导航至 https://ui.endpoints.huggingface.co/new  
2. 填写相关信息  
   - 模型仓库 - andito/s2s  
   - 模型名称 - 如果不喜欢自动生成的名称，可自行重命名，例如 speech-to-speech-demo，请使用小写字母并保持简短  
   - 选择偏好的云服务商和硬件 - 我们使用了 AWS GPU L4，每小时仅需 0.80 美元，足以处理这些模型  
   - 高级配置（点击展开箭头 ➤）  
     - 容器类型 - 自定义  
     - 容器端口 - 80  
     - 容器 URL - andito/speech-to-speech:latest  
     - 密钥 - HF_TOKEN|<你的 token>  

![新推理端点](/images/posts/d8130638d552.png)  

![高级配置](/images/posts/720e13ad3275.png)  

模型仓库实际上并不重要，因为模型会在容器创建时指定并下载，但推理端点需要一个模型，因此可以随意选择一个轻量模型。  

你需要指定 HF_TOKEN，因为我们需要在容器创建阶段下载受限模型。如果使用非受限或非私有模型，则无需此操作。  

当前的 huggingface-inference-toolkit 入口点默认使用端口 5000，但推理端点期望端口 80。你需要在容器端口中匹配此设置。我们已在 Dockerfile 中设置好，但如果从头开始构建，请务必注意！  

### 推理端点 API  

以下我们将逐步介绍如何使用 API 创建端点。只需在你选择的 Python 环境中使用以下代码。  

请确保使用 0.25.1 或更高版本  

```bash  
pip install huggingface_hub>=0.25.1  
```  

使用一个可以创建端点的 token（写入或细粒度权限）  

```python  
from huggingface_hub import login  
login()  
```  

```python  
from huggingface_hub import create_inference_endpoint, get_token  
endpoint = create_inference_endpoint(  
    "speech-to-speech-demo",  
    repository="andito/s2s",  
    framework="custom",  
    task="custom",  
    type="protected",  
    vendor="aws",  
    accelerator="gpu",  
    region="us-east-1",  
    instance_size="x1",  
    instance_type="nvidia-l4",  
    custom_image={  
        "health_route": "/health",  
        "url": "andito/speech-to-speech:latest",   
        "port": 80  
    },  
    secrets={'HF_TOKEN': get_token()}  
)  

endpoint.wait()  
```  

## 概述  

![概述](/images/posts/601f25832f50.png)  

主要组件  

- Speech To Speech：这是一个 Hugging Face 库，我们在 inference-endpoint 分支中放置了一些推理端点专用文件，该分支将很快合并到主分支。  
- andito/s2s 或任何其他仓库：这对我们来说并非必需，因为模型已在容器创建阶段包含，但推理端点需要一个模型，因此我们传入一个轻量仓库。  
- andimarafioti/speech-to-speech-toolkit：这是从 huggingface/huggingface-inference-toolkit 分支而来，帮助我们按需构建自定义容器。  

### 构建 Web 服务器  

要使用端点，我们需要构建一个小型 Web 服务。其代码位于 speech_to_speech 库的 s2s_handler.py 中（我们用于客户端），以及 speech_to_speech_inference_toolkit 的 webservice_starlette.py 中（用于构建 Docker 镜像）。通常，你只需为端点编写一个自定义处理器，但由于我们希望实现极低延迟，我们还构建了支持 WebSocket 连接而非普通请求的 Web 服务。这起初可能听起来复杂，但该 Web 服务仅需 32 行代码！  

![Web 服务代码](/images/posts/82d515c4bd15.png)  

此代码会在启动时运行 prepare_handler，初始化所有模型并进行预热。随后，每条消息将由 inference_handler.process_streaming_data 处理。  

![流式处理代码](/images/posts/614a24f3f350.png)  

该方法简单地接收来自客户端的音频数据，将其分割成小块供 VAD 使用，并提交到队列进行处理。然后检查输出处理队列（模型的语音响应！），如果有内容则返回。所有内部处理由 Hugging Face 的 speech_to_speech 库处理。  

### 自定义处理器与自定义客户端  

Web 服务接收并返回音频。但还有一个重要的缺失部分：我们如何录制和播放音频？为此，我们创建了一个连接到服务的客户端。最简单的做法是将分析分为两部分：与 Web 服务的连接以及音频的录制/播放。  

![音频客户端代码](/images/posts/2a8573612612.png)  

初始化 Web 服务客户端需要为所有消息设置一个包含 Hugging Face Token 的头部。初始化客户端时，我们定义了对常见消息（打开、关闭、错误、消息）的处理方式。这将决定客户端在服务器发送消息时的行为。  

![音频客户端消息代码](/images/posts/e42c221e84c5.png)  

可以看到，对消息的响应非常直接，其中 on_message 是唯一较为复杂的方法。该方法会判断服务器何时完成响应，并开始“监听”用户。否则，它将服务器数据放入播放队列。  

![客户端音频录制与播放](/images/posts/ccca3524c4df.png)  

客户端的音频部分有 4 个任务：  
1. 录制音频  
2. 提交音频录制  
3. 接收服务器音频响应  
4. 播放音频响应  

音频通过 audio_input_callback 方法录制，该方法将所有音频块提交到队列。然后通过 send_audio 方法发送到服务器。如果没有音频可发送，我们仍会提交一个空数组以接收服务器响应。服务器响应由我们之前提到的 on_message 方法处理。音频响应的播放由 audio_output_callback 方法处理。这里我们只需确保音频在预期范围内（我们不希望因数据包错误而损坏用户的耳膜！），并确保输出数组的大小符合播放库的预期。  

## 结论  

在本文中，我们逐步介绍了如何使用自定义 Docker 镜像在 Hugging Face 推理端点上部署语音到语音（S2S）流水线。我们构建了一个自定义容器来处理 S2S 流水线的复杂性，并演示了如何配置以实现可扩展、高效的部署。Hugging Face 推理端点使得将语音到语音等高性能应用变为现实变得更加容易，无需管理硬件或基础设施的麻烦。  

如果你有兴趣尝试或有任何问题，欢迎探索以下资源：  

- Speech-to-Speech GitHub 仓库  
- Speech-to-Speech 推理工具包  
- 基础推理工具包  
- Hugging Face 推理端点文档  

遇到问题或疑问？请在相关 GitHub 仓库中发起讨论，我们将乐意提供帮助！

---

> 本文由AI自动翻译，原文链接：[Deploying Speech-to-Speech on Hugging Face](https://huggingface.co/blog/s2s_endpoint)
> 
> 翻译时间：2026-06-15 07:20
