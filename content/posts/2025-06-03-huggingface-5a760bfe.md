---
title: Holo1：全新GUI自动化视觉语言模型家族，驱动智能体Surfer-H
title_original: 'Holo1: New family of GUI automation VLMs powering GUI agent Surfer-H'
date: '2025-06-03'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/Hcompany/holo1
author: ''
summary: H公司发布了Holo1动作视觉语言模型家族，包括Holo1-3B和Holo1-7B两个开源模型，专门用于深度网页UI理解和精确定位。其中Holo1-7B在UI定位基准测试中达到76.2%的平均准确率，在小型模型中表现最佳。基于Holo1构建的网页原生智能体Surfer-H能够像人类一样与浏览器交互，实现高效的网页自动化。公司同时发布了包含1,639个类人UI任务的WebClick基准测试，并提供了完整的模型使用示例。
categories:
- AI研究
tags:
- GUI自动化
- 视觉语言模型
- 网页智能体
- 开源模型
- 多模态定位
draft: false
translated_at: '2026-04-07T04:43:50.585740'
---

# Holo1：驱动GUI智能体Surfer-H的全新GUI自动化视觉语言模型家族

今天，H公司发布了Holo1——一个动作视觉语言模型家族，以及在Hugging Face Hub上发布的全新多模态定位基准测试WebClick。

Surfer-H，一个像人类一样与浏览器交互的网页原生智能体，正是基于Holo1构建的。

技术报告

### Holo1

Holo1是首个专为深度网页UI理解和精确定位而设计的开源动作视觉语言模型家族。该家族包括Holo1-3B和Holo1-7B模型，其中后者在常见UI定位基准测试中达到了76.2%的平均准确率——在小型模型中位列第一。H公司已在Hugging Face上开源发布了这些模型，同时发布的还有包含1,639个类人UI任务的WebClick基准测试。

![](/images/posts/3c80f6dcfb20.png)

![](/images/posts/fca4e2a3fe17.png)

## 与Transformers一起使用

Holo1模型基于Qwen2.5-VL架构，并且与Transformers完全兼容。这里我们提供一个简单的使用示例。
您可以按如下方式加载模型和处理器。

```python
from transformers import AutoModelForImageTextToText, AutoProcessor
import torch
model = AutoModelForImageTextToText.from_pretrained(
    "Hcompany/Holo1-3B",
    torch_dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
    device_map="auto",
)

processor = AutoProcessor.from_pretrained("Hcompany/Holo1-3B")

```

加载图像并进行预处理。

```python
image_url = "https://huggingface.co/Hcompany/Holo1-3B/resolve/main/calendar_example.jpg" 


guidelines = "Localize an element on the GUI image according to my instructions and output a click position as Click(x, y) with x num pixels from the left edge and y num pixels from the top edge."
instruction = "Select July 14th as the check-out date"
messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "url": image_url,
                },
                {"type": "text", "text": f"{guidelines}\n{instruction}"},
            ],
        }
    ]


inputs = processor.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
    return_dict=True,
).to(model.device)

```

现在我们可以进行推理。

```python
generated_ids = model.generate(**inputs, max_new_tokens=128)

decoded = processor.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)



```

### Surfer-H

网页自动化是AI对企业最具实用价值的应用之一，但迄今为止，解决方案往往为了性能而牺牲了成本效益。通过在Hugging Face上提供我们的Holo1动作模型，用户现在可以实现网页自动化解决方案，在真实网页任务上达到92.2%的准确率，而每个任务的成本仅为0.13美元。

Surfer-H依赖于Holo1系列开源权重模型。它是一个用于完整网页任务自动化的模块化架构，能够执行阅读、思考、点击、滚动、输入和验证。它被设计为灵活且模块化，由三个独立组件构成：一个规划和驱动智能体行为的策略模型，一个理解视觉UI以实现精确交互的定位器模型，以及一个确认任务是否成功完成的验证器模型。与其他依赖定制API或脆弱包装器的智能体不同，Surfer-H完全通过浏览器进行操作——就像真实的用户一样。

这些解决方案共同代表了网页自动化的新前沿，在WebVoyager基准测试中实现了最先进的定位性能，并设定了成本高效网页导航的帕累托前沿：

![](/images/posts/79f0ec75eca7.png)

我们期待看到您将用Holo1构建什么！让我们在本博客文章和模型仓库的讨论区见！

### 引用

```
@misc{andreux2025surferhmeetsholo1costefficient,
      title={Surfer-H Meets Holo1: Cost-Efficient Web Agent Powered by Open Weights}, 
      author={Mathieu Andreux and Breno Baldas Skuk and Hamza Benchekroun and Emilien Biré and Antoine Bonnet and Riaz Bordie and Matthias Brunel and Pierre-Louis Cedoz and Antoine Chassang and Mickaël Chen and Alexandra D. Constantinou and Antoine d'Andigné and Hubert de La Jonquière and Aurélien Delfosse and Ludovic Denoyer and Alexis Deprez and Augustin Derupti and Michael Eickenberg and Mathïs Federico and Charles Kantor and Xavier Koegler and Yann Labbé and Matthew C. H. Lee and Erwan Le Jumeau de Kergaradec and Amir Mahla and Avshalom Manevich and Adrien Maret and Charles Masson and Rafaël Maurin and Arturo Mena and Philippe Modard and Axel Moyal and Axel Nguyen Kerbel and Julien Revelle and Mats L. Richter and María Santos and Laurent Sifre and Maxime Theillard and Marc Thibault and Louis Thiry and Léo Tronchon and Nicolas Usunier and Tony Wu},
      year={2025},
      eprint={2506.02865},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2506.02865}, 
}

```

---

> 本文由AI自动翻译，原文链接：[Holo1: New family of GUI automation VLMs powering GUI agent Surfer-H](https://huggingface.co/blog/Hcompany/holo1)
> 
> 翻译时间：2026-04-07 04:43
