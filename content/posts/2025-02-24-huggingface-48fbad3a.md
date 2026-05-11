---
title: 远程VAE解码：降低扩散模型GPU门槛
title_original: Remote VAEs for decoding with Inference Endpoints 🤗
date: '2025-02-24'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/remote_vae
author: ''
summary: 本文介绍了Hugging Face Diffusers团队推出的远程VAE解码功能，旨在解决高分辨率图像和视频合成中VAE解码器内存消耗大的问题。通过将解码过程委托给远程推理端点，用户可以在消费级GPU上运行模型，避免设备传输开销和分块带来的图像质量损失。文章提供了SD
  v1.5、Flux和HunyuanVideo等模型的代码示例，并说明了该功能的开源、无数据追踪特性。
categories:
- AI基础设施
tags:
- VAE解码
- 推理端点
- 扩散模型
- Hugging Face
- 内存优化
draft: false
translated_at: '2026-05-11T05:59:31.180248'
---

# 使用推理端点进行远程VAE解码 🤗

（本文由hlky和Sayak撰写）

在使用潜在空间扩散模型进行高分辨率图像和视频合成时，VAE解码器会消耗相当多的内存。这使得用户很难在消费级GPU上运行这些模型，而无需承受延迟牺牲等问题。

例如，在使用卸载技术时，存在设备传输开销，导致整体推理延迟增加。分块是另一种解决方案，它允许我们在所谓的输入"分块"上进行操作。然而，这可能会对最终图像质量产生负面影响。

因此，我们希望与社区共同尝试一个想法——将解码过程委托给远程端点。

不会存储或跟踪任何数据，代码是开源的。我们对huggingface-inference-toolkit进行了一些修改，并使用自定义处理器。

这个实验性功能由Diffusers 🧨 开发。

目录：

- 入门指南代码基本示例选项生成队列
- 可用的VAE
- 使用远程VAE的优势
- 提供反馈

- 代码
- 基本示例
- 选项
- 生成
- 队列

## 入门指南

下面，我们介绍三个我们认为远程VAE推理会有帮助的使用场景。

首先，我们创建了一个用于与远程VAE交互的辅助方法。

从main安装diffusers以运行代码。pip install git+https://github.com/huggingface/diffusers@main

```python
from diffusers.utils.remote_utils import remote_decode

```

### 基本示例

这里，我们展示如何在随机张量上使用远程VAE。

```python
image = remote_decode(
    endpoint="https://q1bj3bpq6kzilnsu.us-east-1.aws.endpoints.huggingface.cloud/",
    tensor=torch.randn([1, 4, 64, 64], dtype=torch.float16),
    scaling_factor=0.18215,
)

```

![](/images/posts/3661d1eaa114.png)

Flux的用法略有不同。Flux的潜在表示是打包的，因此我们需要发送高度和宽度。

```python
image = remote_decode(
    endpoint="https://whhx50ex1aryqvw6.us-east-1.aws.endpoints.huggingface.cloud/",
    tensor=torch.randn([1, 4096, 64], dtype=torch.float16),
    height=1024,
    width=1024,
    scaling_factor=0.3611,
    shift_factor=0.1159,
)

```

![](/images/posts/4624acc6c1f7.png)

最后，HunyuanVideo的示例。

```python
video = remote_decode(
    endpoint="https://o7ywnmrahorts457.us-east-1.aws.endpoints.huggingface.cloud/",
    tensor=torch.randn([1, 16, 3, 40, 64], dtype=torch.float16),
    output_type="mp4",
)
with open("video.mp4", "wb") as f:
    f.write(video)

```

### 生成

但我们希望在真实的流水线上使用VAE来获取真实的图像，而不是随机噪声。下面的示例展示了如何使用SD v1.5实现这一点。

```python
from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16,
    variant="fp16",
    vae=None,
).to("cuda")

prompt = "草莓冰淇淋，装在时尚的现代玻璃杯中，椰子，飞溅的奶霜和蜂蜜，渐变紫色背景，流体运动，动态移动，电影级光照，神秘"

latent = pipe(
    prompt=prompt,
    output_type="latent",
).images
image = remote_decode(
    endpoint="https://q1bj3bpq6kzilnsu.us-east-1.aws.endpoints.huggingface.cloud/",
    tensor=latent,
    scaling_factor=0.18215,
)
image.save("test.jpg")

```

![](/images/posts/eb2100418ea7.jpg)

这是另一个使用Flux的示例。

```python
from diffusers import FluxPipeline

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    torch_dtype=torch.bfloat16,
    vae=None,
).to("cuda")

prompt = "草莓冰淇淋，装在时尚的现代玻璃杯中，椰子，飞溅的奶霜和蜂蜜，渐变紫色背景，流体运动，动态移动，电影级光照，神秘"

latent = pipe(
    prompt=prompt,
    guidance_scale=0.0,
    num_inference_steps=4,
    output_type="latent",
).images
image = remote_decode(
    endpoint="https://whhx50ex1aryqvw6.us-east-1.aws.endpoints.huggingface.cloud/",
    tensor=latent,
    height=1024,
    width=1024,
    scaling_factor=0.3611,
    shift_factor=0.1159,
)
image.save("test.jpg")

```

![](/images/posts/7b76f67ac8eb.jpg)

这是使用HunyuanVideo的示例。

```python
from diffusers import HunyuanVideoPipeline, HunyuanVideoTransformer3DModel

model_id = "hunyuanvideo-community/HunyuanVideo"
transformer = HunyuanVideoTransformer3DModel.from_pretrained(
    model_id, subfolder="transformer", torch_dtype=torch.bfloat16
)
pipe = HunyuanVideoPipeline.from_pretrained(
    model_id, transformer=transformer, vae=None, torch_dtype=torch.float16
).to("cuda")

latent = pipe(
    prompt="一只猫在草地上行走，逼真",
    height=320,
    width=512,
    num_frames=61,
    num_inference_steps=30,
    output_type="latent",
).frames

video = remote_decode(
    endpoint="https://o7ywnmrahorts457.us-east-1.aws.endpoints.huggingface.cloud/",
    tensor=latent,
    output_type="mp4",
)

if isinstance(video, bytes):
    with open("video.mp4", "wb") as f:
        f.write(video)

```

### 队列

使用远程VAE的一大优势是我们可以对多个生成请求进行排队。当当前的潜在表示正在被解码处理时，我们已经可以排队下一个请求。这有助于提高并发性。

```python
import queue
import threading
from IPython.display import display
from diffusers import StableDiffusionPipeline

def decode_worker(q: queue.Queue):
    while True:
        item = q.get()
        if item is None:
            break
        image = remote_decode(
            endpoint="https://q1bj3bpq6kzilnsu.us-east-1.aws.endpoints.huggingface.cloud/",
            tensor=item,
            scaling_factor=0.18215,
        )
        display(image)
        q.task_done()

q = queue.Queue()
thread = threading.Thread(target=decode_worker, args=(q,), daemon=True)
thread.start()

def decode(latent: torch.Tensor):
    q.put(latent)

prompts = [
    "蓝莓冰淇淋，装在时尚的现代玻璃杯中，冰块，坚果，薄荷叶，飞溅的奶霜，渐变紫色背景，流体运动，动态移动，电影级光照，神秘",
    "玻璃杯中的柠檬水，薄荷叶，水绿色和白色背景，花朵，冰块，光环，流体运动，动态移动，柔和光照，数字绘画，三分法构图，Greg rutkowski艺术风格，Coby whitmore",
    "漫画艺术，美丽，复古，柔和霓虹色，极其细致的瞳孔，精致的五官，面部打光，微笑，Artgerm，Mary Blair，Edmund Dulac，深色长发，刘海，发光，时尚风格，童话氛围，亮粉色",
    "杰作，香草蛋筒冰淇淋，装饰巧克力酱，碎坚果，巧克力片，棕色背景，金色，电影级光照，WLOP艺术风格",
    "一碗牛奶，飘落的玉米片，浆果，蓝莓，白色背景，柔和光照，复杂细节，三分法，octane渲染，体积光照",
    "冰咖啡加奶油，碎杏仁，玻璃杯装，巧克力片，冰块，湿润，木质背景，电影级光照，超写实绘画，Carne Griffiths艺术风格，octane渲染，体积光照，流体运动，动态移动，柔和色彩",
]

pipe = StableDiffusionPipeline.from_pretrained(
    "Lykon/dreamshaper-8",
    torch_dtype=torch.float16,
    vae=None,
).to("cuda")

pipe.unet = pipe.unet.to(memory_format=torch.channels_last)
pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead", fullgraph=True)

_ = pipe(
    prompt=prompts[0],
    output_type="latent",
)

for prompt in prompts:
    latent = pipe(
        prompt=prompt,
        output_type="latent",
    ).images
    decode(latent)

q.put(None)
thread.join()

```

## 可用的VAE

## 使用远程VAE的优势

以下表格展示了不同GPU的VRAM需求。内存使用百分比决定了特定GPU的用户是否需要卸载。卸载时间因CPU、RAM和HDD/NVMe而异。分块解码会增加推理时间。

## 提供反馈

如果您喜欢这个想法和功能，请帮助我们提供反馈，告诉我们如何能做得更好，以及您是否有兴趣让这类功能更原生地集成到Hugging Face生态系统中。如果这次试点进展顺利，我们计划为更多模型创建优化的VAE端点，包括能够生成高分辨率视频的模型！

### 步骤：

1. 通过此链接在Diffusers上提交一个issue。
2. 回答问题并提供您想补充的任何额外信息。
3. 点击提交！

---

> 本文由AI自动翻译，原文链接：[Remote VAEs for decoding with Inference Endpoints 🤗](https://huggingface.co/blog/remote_vae)
> 
> 翻译时间：2026-05-11 05:59
