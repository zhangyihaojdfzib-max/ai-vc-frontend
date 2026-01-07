---
title: NVIDIA RTX通过LTX-2与ComfyUI升级，加速PC端4K AI视频生成
title_original: NVIDIA RTX Accelerates 4K AI Video Generation on PC With LTX-2 and
  ComfyUI Upgrades
date: '2026-01-06'
source: NVIDIA AI Blog
source_url: https://blogs.nvidia.com/blog/rtx-ai-garage-ces-2026-open-models-video-generation/
author: ''
summary: NVIDIA在CES上宣布了一系列针对RTX设备的AI升级，显著提升了PC端生成式AI的性能。通过优化PyTorch-CUDA、在ComfyUI中支持NVFP4/FP8精度，视频生成性能提升高达3倍，VRAM占用减少60%。新推出的视频生成流程结合了Lightricks的LTX-2模型和ComfyUI，使艺术家能够在本地PC上生成并升级至4K分辨率的视频，同时获得精确的控制。这些进展标志着PC端AI视频创作在速度、质量和可控性方面的重要突破。
categories:
- AI产品
tags:
- NVIDIA
- AI视频生成
- RTX
- ComfyUI
- 4K视频
draft: false
translated_at: '2026-01-06T18:15:23.228Z'
---

# NVIDIA RTX 通过LTX-2与ComfyUI升级，在PC上加速4K AI视频生成

![](/images/posts/acbf331534c8.jpg)

- 
- 
- 
- 
- Email0

2025年是PC端AI发展的突破之年。

PC级小语言模型（SLM）的准确率较2024年提升了近2倍，极大地缩小了与前沿云端大语言模型（LLM）的差距。包括Ollama、ComfyUI、llama.cpp和Unsloth在内的AI PC开发者工具已经成熟，其受欢迎程度同比增长了一倍，下载PC级模型的用户数量较2024年增长了十倍。

这些发展为生成式AI在今年获得日常PC创作者、游戏玩家和生产力用户的广泛采用铺平了道路。

在本周的CES上，NVIDIA宣布为GeForce RTX、NVIDIA RTX PRO和NVIDIA DGX Spark设备带来一系列AI升级，为开发者在PC上部署生成式AI解锁所需的性能和内存，包括：

- 通过PyTorch-CUDA优化以及ComfyUI中原生的NVFP4/FP8精度支持，视频和图像生成式AI性能提升高达3倍，VRAM占用减少60%。
- ComfyUI集成RTX视频超分辨率技术，加速4K视频生成。
- 针对Lightricks最先进的LTX-2音视频生成模型开放权重的发布，进行NVIDIA NVFP8优化。
- 新的视频生成流程，可利用Blender中的3D场景生成4K AI视频，精确控制输出。
- 通过Ollama和llama.cpp，SLM的推理性能提升高达35%。
- 为Nexa.ai的Hyperlink新视频搜索功能提供RTX加速。

这些进步将使用户能够在本地RTX AI PC提供的隐私、安全和低延迟优势下，无缝运行先进的视频、图像和语言AI工作流。

## 在RTX PC上以3倍速度生成4K视频

生成式AI可以制作令人惊叹的视频，但仅凭提示词很难控制在线工具。而尝试生成4K视频几乎是不可能的，因为大多数模型太大，无法放入PC的VRAM。

今天，NVIDIA推出了一种由RTX驱动的视频生成流程，使艺术家能够在生成视频时获得精确的控制，同时生成速度提升3倍，并升级至4K分辨率——且仅占用一小部分VRAM。

该视频流程使新兴艺术家能够创建故事板，将其转换为逼真的关键帧，然后将这些关键帧转换为高质量的4K视频。该流程分为三个蓝图，艺术家可以根据需要混合、匹配或修改：

- 一个为场景创建资源的3D对象生成器。
- 一个3D引导的图像生成器，允许用户在Blender中设置场景并从中生成逼真的关键帧。
- 一个视频生成器，根据用户的起始和结束关键帧为其视频制作动画，并使用NVIDIA RTX视频技术将其升级至4K。

这一流程的实现得益于Lightricks新发布的突破性LTX-2模型，该模型现已可供下载。

作为本地AI视频创作的一个重要里程碑，LTX-2提供的效果可与领先的云端模型相媲美，同时能生成长达20秒的4K视频，并具有令人印象深刻的视觉保真度。该模型内置音频、支持多关键帧，并具备通过可控性低秩适配增强的高级条件控制能力——为创作者提供电影级的质量和控制力，而无需依赖云端。

在底层，该流程由ComfyUI驱动。在过去的几个月里，NVIDIA与ComfyUI密切合作，在NVIDIA GPU上将性能优化了40%，最新更新增加了对NVFP4和NVFP8数据格式的支持。综合来看，使用RTX 50系列的NVFP4格式时，性能提升3倍，VRAM减少60%；使用NVFP8格式时，性能提升2倍，VRAM减少40%。

![](/images/posts/0e7e32619df1.jpg)

现在，一些顶级模型的NVFP4和NVFP8检查点可以直接在ComfyUI中使用。这些模型包括来自Lightricks的LTX-2、来自Black Forest Labs的FLUX.1和FLUX.2，以及来自阿里巴巴的Qwen-Image和Z-Image。可直接在ComfyUI中下载它们，更多模型支持即将推出。

![](/images/posts/f01896e11d9a.jpg)

视频片段生成后，使用ComfyUI中新的RTX视频节点，只需几秒钟即可将视频升级至4K。此升级器实时工作，锐化边缘并清理压缩伪影，以获得清晰的最终图像。RTX视频功能将于下个月在ComfyUI中提供。

为了帮助用户突破GPU内存的限制，NVIDIA与ComfyUI合作改进了其内存卸载功能，即权重流式传输。启用权重流式传输后，当VRAM不足时，ComfyUI可以使用系统RAM，从而在中端RTX GPU上运行更大的模型和更复杂的多阶段节点图。

该视频生成工作流程将于下个月开放下载，而新发布的LTX-2视频模型开放权重和ComfyUI RTX更新现已可用。

## 搜索PC文件和视频的新方式

几十年来，PC上的文件搜索方式一直未变。它仍然主要依赖文件名和零散的元数据，这使得查找去年的某个文档变得异常困难。

Hyperlink——Nexa.ai的本地搜索Agent——将RTX PC转变为可搜索的知识库，能够用自然语言回答问题并提供内联引用。它可以扫描和索引文档、幻灯片、PDF和图像，因此搜索可以基于想法和内容驱动，而不是猜测文件名。所有数据都在本地处理并保留在用户的PC上，以确保隐私和安全。此外，它经过RTX加速，在RTX 5090 GPU上，每千兆字节文本和图像文件的索引时间为30秒，响应时间为3秒，相比之下，在CPU上索引文件需要每小时每千兆字节，响应时间为90秒。

在CES上，Nexa.ai发布了Hyperlink的新测试版，增加了对视频内容的支持，使用户能够搜索视频中的对象、动作和语音。这对于从寻找B-roll素材的视频艺术家，到想要找到赢得大逃杀比赛时刻以便与朋友分享的游戏玩家来说，都是理想的选择。

有兴趣尝试Hyperlink私测版的用户，请在此网页注册获取访问权限。访问权限将从本月开始陆续发放。

## 小语言模型速度提升35%

![](/images/posts/29b27e68f878.jpg)

NVIDIA与开源社区合作，利用Llama.cpp和Ollama，为RTX GPU和NVIDIA DGX Spark桌面超级计算机上的SLM带来了显著的性能提升。最新的变化尤其有利于专家混合模型，包括新的NVIDIA Nemotron 3系列开放模型。

在过去的四个月里，llama.cpp和Ollama的SLM推理性能分别提升了35%和30%。这些更新现已可用，llama.cpp的一项体验升级也加快了LLM的加载时间。

这些加速将在LM Studio的下一次更新中提供，并将很快应用于像新的MSI AI Robot应用这样的Agent应用。MSI AI Robot应用同样利用了Llama.cpp的优化，允许用户控制其MSI设备设置，并将在即将发布的版本中纳入最新更新。

## NVIDIA Broadcast 2.1为更多PC用户带来虚拟主光效果

![](/images/posts/d80d225cb158.jpg)

NVIDIA Broadcast应用程序通过AI效果提升用户PC麦克风和网络摄像头的质量，非常适合直播和视频会议。

2.1版本更新了虚拟主光效果以提升性能——使其可用于RTX 3060桌面GPU及更高型号——能够处理更多光照条件，提供更广泛的色温控制，并使用更新的HDRi基础贴图，实现专业直播中常见的双主光风格。立即下载NVIDIA Broadcast更新。

## 使用DGX Spark将家庭创意工作室转变为AI动力源

随着性能日益强大的新型AI模型每月登陆PC平台，开发者对更强大、更灵活的本地AI配置方案的兴趣持续增长。DGX Spark——一款可置于用户桌面的紧凑型AI超级计算机，能与主台式机或笔记本电脑无缝协作——让用户能够在现有PC旁进行实验、原型设计和运行高级AI工作负载。

Spark非常适合那些希望测试LLM（大语言模型）或构建Agent（智能体）工作流原型的人群，也适合希望在并行生成素材的同时仍能使用主PC进行编辑的艺术家。

在CES展会上，英伟达宣布对Spark进行重大AI性能升级，自不到三个月前发布以来，其性能提升高达2.6倍。

同时发布了新的DGX Spark应用指南，其中一份关于推测解码，另一份则指导如何使用两个DGX Spark模块对模型进行微调。

![](/images/posts/fcacb00d923f.jpg)

在Facebook、Instagram、TikTok和X上关注英伟达AI PC动态，并通过订阅RTX AI PC通讯保持信息同步。在LinkedIn和X上关注英伟达工作站。

查看关于软件产品信息的通知。

![订阅组件](/images/posts/cc130df17877.jpg)

![CES 2026与GeForce NOW](/images/posts/5455d8d0c8ec.jpg)

英伟达通过为Linux PC和亚马逊Fire TV推出新版GeForce NOW应用，将GeForce RTX游戏体验带给更多设备

![](/images/posts/57a795d27a61.jpg)

英伟达DLSS 4.5、路径追踪与G-SYNC Pulsar以增强的性能和视觉效果赋能游戏体验

![](/images/posts/a10b2458a7ae.jpg)

英伟达Rubin平台、开源模型与自动驾驶：英伟达在CES展示未来蓝图

![](/images/posts/b23d5e199312.jpg)

基于英伟达BlueField的网络安全与加速方案登陆英伟达企业AI工厂验证设计

![](/images/posts/2e071947680b.png)

英伟达DGX SuperPOD为基于Rubin架构的系统奠定基础

---

> 本文由AI自动翻译，原文链接：[NVIDIA RTX Accelerates 4K AI Video Generation on PC With LTX-2 and ComfyUI Upgrades](https://blogs.nvidia.com/blog/rtx-ai-garage-ces-2026-open-models-video-generation/)
> 
> 翻译时间：2026-01-06 17:57
