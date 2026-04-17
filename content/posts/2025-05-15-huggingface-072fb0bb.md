---
title: Falcon-Edge：强大、通用、可微调的1.58位语言模型系列
title_original: 'Falcon-Edge: A series of powerful, universal, fine-tunable 1.58bit
  language models.'
date: '2025-05-15'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/tiiuae/falcon-edge
author: ''
summary: 本文介绍了Falcon-Edge系列语言模型，该系列基于BitNet架构，采用三元权重（{-1, 0, 1}）实现1.58位精度。模型通过单一训练过程同时生成全精度（bfloat16）和量化版本，提供10亿和30亿参数两种规模，包含基础模型和指令微调模型。Falcon-Edge旨在解决边缘设备部署的资源限制问题，其“无矩阵乘法”设计显著提升了推理速度和内存效率。在基准测试中，该系列模型表现出与同类规模模型相当甚至更优的性能，为高效AI部署提供了新范式。
categories:
- AI研究
tags:
- 语言模型
- 模型量化
- 边缘计算
- BitNet
- 低精度训练
draft: false
translated_at: '2026-04-17T04:49:37.511965'
---

# Falcon-Edge：一系列强大、通用、可微调的1.58位语言模型。

![image/png](/images/posts/b29e2971fe56.png)

在这篇博客文章中，我们将介绍Falcon-Edge系列的关键亮点和设计理念。这是一个基于BitNet架构、以三元格式提供的强大、通用且可微调的语言模型集合。

借鉴我们在BitNet方面的经验，Falcon-Edge引入并验证了一种新的预训练范式，该范式通过单一训练过程提供全范围的输出，同时生成非量化和量化的模型变体。这种全面的方法产生了一个bfloat16格式的非BitNet模型、原生的BitNet模型，以及一个专门为轻松微调而设计的预量化BitNet变体，使用户和开发者能够根据其特定应用和需求精确定制这些模型。

目前提供两种规模——10亿和30亿参数——每种规模都包含基础模型和指令微调模型。请在我们的专属Hugging Face集合中探索Falcon-Edge系列。

## 引言

大语言模型（LLM）在设计上本质上是庞大且资源密集的。随着在边缘设备上高效部署这些模型的需求增长，模型压缩的研究也在加速。最近的努力，例如DeepSeek和Llama 4的工作，探索使用降低精度的格式（低至FP8）进行训练，以提高部署的可扩展性。另一方面，许多最先进的方法强调训练后量化。与这些方法相比，BitNet引入了一种根本不同的范式：不同于仍然依赖浮点格式的降低精度训练，也不同于在全精度训练后调整权重的训练后量化，BitNet在训练期间直接使用最低可能的精度——三元权重（{-1, 0, 1}）——从而实现端到端的超高效模型设计。

这些三元权重正在为一种“无矩阵乘法”的LLM设计铺平道路，这种设计在实践中速度显著更快且内存效率极高。这种创新方法的主要挑战在于需要对BitNet模型进行预训练，这对普通用户来说计算量大且成本高昂。

## Falcon-Edge，一系列强大的模型

利用我们中心在预训练数据策略方面的经验，我们在内部数据混合上对模型进行了约1.5万亿Token的预训练。我们使用经典的WSD学习率调度器进行预训练。

我们在前Hugging Face排行榜v2基准测试上评估了我们的模型（基础版和指令版），并报告了与类似规模其他模型相比的归一化结果如下：

![image/png](/images/posts/e913c4b2f252.png)

![image/png](/images/posts/eec0d63b136e.png)

将我们的指令模型与微软新的BitNet模型进行比较的额外结果（排行榜v1）：

![image/png](/images/posts/20b816672412.png)

Falcon-Edge在排行榜v2任务上展示了与同类规模模型相当甚至更好的性能，这表明在特定领域训练强大的BitNet模型的同时，在其他任务上保持足够竞争力是可能的。

## Falcon-Edge，一系列通用模型

如果我们更仔细地查看BitNet线性层在推理时的公式（以Python代码表示）：

```python
def activation_norm_quant(x):
    scale = 127.0 / x.abs().max(dim=-1, keepdim=True).values.clamp_(min=1e-5)
    y = (x * scale).round().clamp_(-128, 127)
    return y, scale

class BitLinear(nn.Linear):
    
    def post_quant_process(self, input, input_scale, weight_scale):
        out = input / (input_scale * weight_scale)
        return out

    def forward(self, input):
        w = self.weight
        w_quant = unpack_weights(w, dtype=self.dtype)
        input_quant, input_scale = self.activation_quant(input)
        y = F.linear(input_quant.to(self.dtype), w_quant)
        y = self.post_quant_process(y, self.weight_scale, input_scale)
        if self.bias is not None:
            y += self.bias.view(1, -1).expand_as(y)
        return y

```

归一化函数`activation_norm_quant`将激活量化为int8格式，然后通过除以`x_scale`将激活计算回半精度。由于模型是使用模拟的8位激活量化进行训练的，我们认为可以近似认为：

```python
x_quant, x_scale = activation_norm_quant(x)
x ~= (x_quant / x_scale)

```

因此，与其在训练后量化模型，不如在量化权重后注入权重缩放因子，这应该能足够好地“近似”模型的非BitNet版本：

```python
def _weight_quant(w):
    scale = 1.0 / w.abs().mean().clamp_(min=1e-05)
    u = (w * scale).round().clamp_(-1, 1)
    return u, scale

for param_name, param_value in state_dict.items():
    if _is_param_to_not_quantize(param_name):
        continue

    param_value, param_scale = _weight_quant(param_value)
    param_value = param_value / param_scale

    state_dict_quant[param_name] = param_value

```

我们通过对我们的10亿和30亿基础模型的bfloat16变体进行端到端评估来确认这一点，结果如下：

![image/png](/images/posts/c1d7cceb8d5e.png)

模型的bfloat16对应版本可以通过Hugging Face transformers直接加载，只需在`from_pretrained`函数中传递`revision="bfloat16"`参数：

```python
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer

model_id = "tiiuae/Falcon-E-1B-Base"

tokenizer = AutoTokenizer.from_pretrained(model_id, revision="prequantized")
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    revision="bfloat16"
)

```

## Falcon-Edge，一系列可微调的Bitnet模型

据我们所知，除了微软最近的发布之外，之前的BitNet发布只专注于发布最终的量化模型，使其仅可用于推理。与微软的发布类似，我们建议通过发布预量化权重来扩展BitNet模型的研究和应用可及性。这样，用户既可以在其目标领域进行微调，也可以对BitNet检查点进行持续预训练，只要将`nn.Linear`层替换为`BitnetLinear`层，并确保在训练后以BitNet格式量化模型。由于权重对应于预量化权重，如果不将`nn.Linear`层替换为`BitnetLinear`层就执行文本生成，将产生无意义的输出。

预量化权重可以通过Hugging Face的transformers库下载，只需将`revision`参数指定为`prequantized`：

```py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "tiiuae/Falcon-E-1B-Base"

tokenizer = AutoTokenizer.from_pretrained(model_id, revision="prequantized")
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    revision="prequantized"
)

```

通过这种方式，我们将帮助围绕首个强大的1位微调模型培育社区生态系统。我们为社区提供了易于上手的工具，以便他们微调自己版本的强大BitNet模型，方法是将对预量化权重执行微调所需的所有实用方法打包到一个名为`onebitllms`的Python包中，我们将在下一节介绍它。

## 介绍`onebitllms` - 一个用于1位LLM训练的轻量级Python工具包

![image/png](/images/posts/e4770a71dd19.png)

在此次发布中，我们还引入了`onebitllms`——一个轻量级的Python包，可以插入到你最喜欢的LLM微调工具中，以便微调任何预量化的BitNet模型。在撰写本文时，`onebitllms`主要提供以下功能：

-   用于将预量化模型检查点转换为BitNet训练格式的实用方法，以便将其传递给您喜欢的任何LLM（大语言模型）微调框架。我们目前已在Hugging Face的`trl`库中测试了我们的库。
-   用于将训练好的检查点量化为BitNet格式以及常规`bfloat16`格式的实用方法。
-   如需更精细的控制：提供`BareBitnetLinear`和triton内核，可注入并用于您的预训练框架。

目前，此框架仅支持全参数微调。虽然在此版本中模型尺寸相对较小，但为BitNet模型支持参数高效微调（PEFT）方法，对于即将推出的BitNet模型而言，仍然是一个令人兴奋且具有影响力的开放性问题。

要开始使用，只需通过`pip`或从源代码直接安装软件包，并查看源代码中的`examples/`文件夹。

```py
import torch

from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer
from onebitllms import replace_linear_with_bitnet_linear, quantize_to_1bit

model_id = "tiiuae/Falcon-E-1B-Base"

tokenizer = AutoTokenizer.from_pretrained(model_id, revision="prequantized")
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    revision="prequantized"
)
model = replace_linear_with_bitnet_linear(model)

trainer = SFTTrainer(
    model,
    ...
)

trainer.train()

quantize_to_1bit(output_directory)

```

我们希望这个软件包能够加速围绕三元格式LLM的研究与开发，并期待看到社区开发出许多`Falcon-Edge`的衍生版本以及其他未来强大的BitNet模型。

## 进一步探索

我们相信此次发布开启了多个有趣的方向——在所有可能的后续方向中，我们认为以下开放性问题将使BitNet模型在不久的将来产生更大的影响：

-   为BitNet架构编写更强大的GPU推理内核：借鉴`bitnet.cpp`背后的核心思想，我们希望此次发布能说服研究社区专注于开发强大的BitNet推理内核，以实现GPU上更快的推理——从而使它们在GPU上比原生模型更快。
-   支持BitNet微调的PEFT方法：这仍是一个未被探索的研究问题，可以为BitNet模型开启多种新的可能性。
-   对BitNet检查点通用性进行更严谨的研究：虽然我们观察到简单地注入权重缩放因子就能得到一个尚可的非BitNet检查点，但我们相信可以进行更多研究，以最小化BitNet检查点与其`bfloat16`对应版本之间的性能下降，从而实现完全无性能损失。
-   关于多模态BitNet模型：我们希望这些BitNet基础模型连同`onebitllms`软件包，能够作为创建首个多模态BitNet VLM（视觉语言模型）等工作的基础。
-   更优化的BitNet训练内核：为了编写我们的内核，我们决定采用两阶段方法，首先计算全局最大值，然后逐块使用它进行归一化。可以修改这种方法以编写更高效的内核。在我们的测试中，我们估计非BitNet预训练与BitNet预训练之间的开销约为20%。我们将很快发布关于BitNet引入的训练开销的更广泛数据。

## 引用

如果您发现这项工作对您的研究和工作有用，请考虑引用我们的工作，以及引用BitNet模型背后的所有基础工作：

```latex
@misc{tiionebitllms,
    title = {Falcon-E, a series of powerful, universal and fine-tunable 1.58bit language models.},
    author = {Falcon-LLM Team},
    month = {May},
    url = {https://falcon-lm.github.io/blog/falcon-edge},
    year = {2025}
}

```

```latex
@misc{ma2025bitnetb1582b4ttechnical,
      title={BitNet b1.58 2B4T Technical Report}, 
      author={Shuming Ma and Hongyu Wang and Shaohan Huang and Xingxing Zhang and Ying Hu and Ting Song and Yan Xia and Furu Wei},
      year={2025},
      eprint={2504.12285},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2504.12285}, 
}
@misc{wang2025bitnetcppefficientedgeinference,
      title={Bitnet.cpp: Efficient Edge Inference for Ternary LLMs}, 
      author={Jinheng Wang and Hansong Zhou and Ting Song and Shijie Cao and Yan Xia and Ting Cao and Jianyu Wei and Shuming Ma and Hongyu Wang and Furu Wei},
      year={2025},
      eprint={2502.11880},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2502.11880}, 
}

```

```latex
@misc{,
      title={1.58-Bit LLM: A New Era of Extreme Quantization}, 
      author={Mohamed Mekkouri and Marc Sun and Leandro von Werra and Thomas Wolf},
      year={2024},
}

```

```latex
@misc{ma2024era1bitllmslarge,
      title={The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits}, 
      author={Shuming Ma and Hongyu Wang and Lingxiao Ma and Lei Wang and Wenhui Wang and Shaohan Huang and Li Dong and Ruiping Wang and Jilong Xue and Furu Wei},
      year={2024},
      eprint={2402.17764},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2402.17764}, 
}

```

```latex
@misc{wang2023bitnetscaling1bittransformers,
      title={BitNet: Scaling 1-bit Transformers for Large Language Models}, 
      author={Hongyu Wang and Shuming Ma and Li Dong and Shaohan Huang and Huaijie Wang and Lingxiao Ma and Fan Yang and Ruiping Wang and Yi Wu and Furu Wei},
      year={2023},
      eprint={2310.11453},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2310.11453}, 
}

```

---

> 本文由AI自动翻译，原文链接：[Falcon-Edge: A series of powerful, universal, fine-tunable 1.58bit language models.](https://huggingface.co/blog/tiiuae/falcon-edge)
> 
> 翻译时间：2026-04-17 04:49
