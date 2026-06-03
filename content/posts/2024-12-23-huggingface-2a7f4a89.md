---
title: NVIDIA LogitsProcessorZoo：精细控制语言模型生成
title_original: Controlling Language Model Generation with NVIDIA's LogitsProcessorZoo
date: '2024-12-23'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/logits-processor-zoo
author: ''
summary: 本文介绍了NVIDIA的LogitsProcessorZoo，一组模块化的logits处理器集合，用于增强Hugging Face Transformers库的文本生成控制能力。文章首先解释了logits的概念及其在语言模型生成中的作用，然后阐述了处理logits的必要性，如控制序列长度、强制关键词和引导多项选择。LogitsProcessorZoo通过直接修改概率分布，提供了比传统解码策略更精细的控制，且与generate方法完全兼容，是社区驱动创新的范例。
categories:
- AI基础设施
tags:
- NVIDIA
- LogitsProcessorZoo
- 语言模型
- 文本生成
- Hugging Face
draft: false
translated_at: '2026-06-03T06:51:05.119055'
---

# 使用 NVIDIA 的 LogitsProcessorZoo 控制语言模型生成

使用语言模型生成文本通常涉及基于概率分布选择下一个 Token。像贪心搜索这样直接的方法会选择概率最高的 Token，但这可能导致生成通用或重复的输出。为了增加多样性和可控性，更先进的解码策略（如束搜索、核采样和 Top-K 采样）被广泛使用。这些策略由 🤗 Transformers 库支持，让我们在塑造模型输出时拥有灵活性。

但如果我们想更进一步，通过直接修改概率分布来控制文本生成过程本身呢？这就是 logit 处理发挥作用的地方。Hugging Face 的 LogitsProcessor API 允许你自定义语言模型头的预测分数，从而对模型行为进行精细控制。🤗 Transformers 库不仅提供了丰富的内置 logits 处理器，还赋能社区创建和共享针对独特用例定制的自定义处理器。

接下来介绍 NVIDIA 的 LogitsProcessorZoo——一组强大且模块化的 logits 处理器集合，专为特定任务设计，例如控制序列长度、强制关键词或引导多项选择答案。NVIDIA 的库与 Hugging Face 的 generate 方法完全兼容，是 logits 处理领域社区驱动创新的绝佳范例。

在本文中，我们将探讨 NVIDIA 的 LogitsProcessorZoo 如何增强和扩展现有能力，深入分析其特性，并演示它如何优化你的 AI 工作流程。

## 语言模型中的 Logits 是什么？

来源：https://jalammar.github.io/illustrated-gpt2/

Logits 是语言模型为其词汇表中每个 Token 生成的原始、未归一化的分数。这些分数通过 softmax 函数转换为概率，指导模型选择下一个 Token。

以下示例展示了 logits 如何融入生成过程：

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


model_name = "meta-llama/Llama-3.2-1B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.bfloat16, device_map="auto")


prompt = "The capital of France is"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)


with torch.inference_mode():
    outputs = model(**inputs)
    logits = outputs.logits


last_token_logits = logits[:, -1, :]

```

这些 logits 表示模型对每个潜在下一个单词的置信度。通过 softmax，我们可以将它们转换为概率并解码为生成的文本：

```python

next_token_probs = torch.nn.functional.softmax(last_token_logits, dim=-1)


predicted_token_ids = torch.argmax(next_token_probs, dim=-1)
generated_text = tokenizer.batch_decode(predicted_token_ids, skip_special_tokens=True)
print("Generated Text:", generated_text[0])

>>> Generated Text: Paris

```

虽然这个流程展示了原始 logits 如何转换为文本，但值得注意的是 🤗 Transformers 简化了这一过程。例如，generate() 方法会自动处理这些转换，包括应用 softmax 函数和从概率分布中采样。

然而，对于采样或施加任务特定约束等常见任务，原始 logits 可能并不理想。有关在生成过程中有效处理 logits 的更多详细信息，请参阅 Hugging Face 的生成博客文章。这就是 logit 处理在定制输出以满足特定需求时变得不可或缺的原因。

## 为什么要处理 Logits？

在控制输出行为时，原始 logits 往往存在不足。例如：

- 缺乏约束：它们可能无法遵循要求的格式、语法规则或预定义结构。
- 过度泛化：模型可能优先选择通用回复，而非具体、高质量的输出。
- 任务不匹配：序列可能过早结束、过于冗长或遗漏关键细节。

Logit 处理使我们能够在生成之前通过修改这些原始分数来调整模型的行为。

## NVIDIA 的 LogitsProcessorZoo

NVIDIA 的 LogitsProcessorZoo 通过专为特定任务设计的模块化组件简化了 logits 的后处理。让我们探索其特性并了解如何使用它们。要跟着操作，请前往笔记本并尝试这些 logits 处理器。

使用以下命令安装该库：

```bash
pip install logits-processor-zoo

```

为了演示这些处理器，我们将创建一个简单的 LLMRunner 类，该类初始化模型和分词器，并暴露一个 generate_response 方法。然后，我们将不同的处理器提供给 generate_response 方法，并观察它们的效果。

```python

class LLMRunner:
    def __init__(self, model_name="meta-llama/Llama-3.2-1B-Instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

    def generate_response(self, prompts, logits_processor_list=None, max_tokens=1000):
        if logits_processor_list is None:
            logits_processor_list = []

        for prompt in prompts:
            conversation = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
            inputs = self.tokenizer.apply_chat_template(
                conversation,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt",
                return_dict=True,
            ).to(self.model.device)

            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                min_new_tokens=1,
                logits_processor=LogitsProcessorList(logits_processor_list),
            )

            gen_output = self.tokenizer.batch_decode(
                outputs, skip_special_tokens=True, clean_up_tokenization_spaces=False
            )
            
            generated_text = gen_output[0][
                len(
                    self.tokenizer.decode(
                        inputs["input_ids"][0], skip_special_tokens=True
                    )
                ) :
            ].strip()

            print(f"Prompt: {prompt}")
            print()
            print(f"LLM response:\n{generated_text}")

runner = LLMRunner()

```

### 1. GenLengthLogitsProcessor

通过调整序列结束（EOS）Token 的可能性来控制生成序列的长度。

该处理器在生成文本的期望长度起关键作用的场景中特别有用，例如生成简洁摘要、限制冗长输出或为特定用例定制回复。例如，它可以帮助确保聊天机器人提供简短而有意义的回复，同时在需要时通过完成句子来保持语法完整性。

```py
example_prompts =[
    "Tell me a story about a kid lost in forest."
]


print(runner.generate_response(
    example_prompts,
    [GenLengthLogitsProcessor(runner.tokenizer, boost_factor=0.1, p=2, complete_sentences=True)]
))

```

LLM response:
Once upon a time, in a dense forest, there lived a young boy named Timmy. Timmy was on a family camping trip with his parents and little sister, Emma. They had been walking for hours, and the dense trees seemed to close in around them. As the sun began to set, Timmy realized he had wandered away from his family.
At first, Timmy didn't panic. He thought about calling out for his parents and Emma, but his voice was hoarse from singing campfire songs. He looked around, but the trees seemed to stretch on forever, making it impossible to see any familiar landmarks. As the darkness grew thicker, Timmy's fear began to creep in.

```py

```

```python
print(runner.generate_response(
    example_prompts,
    [GenLengthLogitsProcessor(runner.tokenizer, boost_factor=-10.0, p=0, complete_sentences=False)]
))
```

LLM 响应：
从前，在一片茂密而充满生机的森林里，住着一个名叫马克斯的小男孩。马克斯是个八岁、充满冒险精神且好奇心旺盛的孩子，他热爱在户外探索。一个阳光明媚的下午，他在森林里闲逛时，偶然发现了一条从未见过的小路。
马克斯兴奋不已，决定沿着小路走，看看它会通向何方。森林里生机勃勃，阳光透过树叶洒下，营造出一种奇幻的氛围。马克斯走了大约二十分钟，眼睛扫视着四周，寻找任何文明的迹象。
当太阳开始落山，给森林披上一层温暖的橙色光芒时，马克斯意识到自己迷路了。他没有手机，没有钱包，也无法与家人联系。恐慌开始蔓延，马克斯感到害怕又孤独。
惊慌失措的马克斯开始在森林里奔跑，心跳加速，双腿颤抖。他跌跌撞撞地来到一片空地，看到远处有一丝微弱的灯光。走近后，他看到空地中央有一座小木屋。烟囱里冒着烟，马克斯还能听到有人在轻声哼唱。
……

在上述示例中，我们使用了 `GenLengthLogitsProcessor` 来缩短和延长模型生成的响应。

### 2. CiteFromPromptLogitsProcessor

增强或削弱来自提示词的 Token，以鼓励生成相似的输出。

这在需要保留上下文的任务中尤其有价值，例如基于段落回答问题、生成包含特定细节的摘要，或在对话系统中生成一致的输出。
例如，在分析用户评论的代码片段中，该处理器确保模型生成的响应与评论内容紧密相关，例如强调对产品价格的看法。

```python
example_prompts = [
    """
    用户评论：非常柔软，色彩丰富，价格昂贵但物有所值，款式时尚。

    用户对产品价格的看法是什么？
    """,
]

print(runner.generate_response(
    example_prompts,
    [CiteFromPromptLogitsProcessor(runner.tokenizer, example_prompts, boost_factor=5.0)],
    max_tokens=50,
))
```

LLM 响应：
根据用户评论，用户对产品价格的看法是：用户非常满意，但价格昂贵，不过产品款式时尚、柔软且色彩丰富，这是用户愿意支付的价格。

注意，生成结果引用了输入提示词。

### 3. ForceLastPhraseLogitsProcessor

强制模型在结束输出前包含特定短语。

该处理器在结构化内容生成场景中特别有用，这些场景要求一致性或遵循特定格式。它非常适合生成引用、正式报告或需要特定措辞以保持专业或组织化呈现的输出。

```python
example_prompts = [
    """
    检索自：https://en.wikipedia.org/wiki/Bulbasaur
    妙蛙种子是任天堂和Game Freak的宝可梦系列中的虚构宝可梦物种。
    由西田敦子设计，妙蛙种子是草属性和毒属性的宝可梦，首次出现在《宝可梦 红·绿》（日本以外地区为《宝可梦 红·蓝》）中作为初始宝可梦。
    此后，它出现在续作、衍生游戏、相关商品以及该系列的动画和印刷改编作品中。
    它是宝可梦动画中的核心角色，在第一季中是小智的主要宝可梦之一，后来另一位主角小遥获得了一只不同的妙蛙种子。
    它出现在各种漫画中，并在《宝可梦特别篇》中由主角小赤拥有。

    妙蛙种子是什么？
    """,
]

phrase = "\n\n参考文献："
batch_size = len(example_prompts)

print(runner.generate_response(
    example_prompts,
    [ForceLastPhraseLogitsProcessor(phrase, runner.tokenizer, batch_size)]
))
```

LLM 响应：
根据从维基百科文章检索到的信息，妙蛙种子是宝可梦系列中的一种虚构宝可梦物种。它是一种草属性和毒属性的宝可梦，出现在各种媒体形式中，包括：
    - 作为第一代宝可梦游戏（包括《宝可梦 红·蓝》）中的初始宝可梦。
    - 作为宝可梦动画中的主要角色，是小智最初的宝可梦之一。
    - 作为宝可梦漫画中的角色，由主角小赤拥有。
    - 作为其他各种宝可梦媒体（如衍生游戏和相关商品）中的角色。
    妙蛙种子也是宝可梦系列的核心角色，经常与其他宝可梦一同出现，是宝可梦世界的关键部分。
    参考文献：
    -https://en.wikipedia.org/wiki/Bulbasaur

```python
phrase = "\n\n感谢您尝试我们的RAG（检索增强生成）应用！如果您对以下内容有更多疑问"

print(runner.generate_response(example_prompts,
    [ForceLastPhraseLogitsProcessor(phrase, runner.tokenizer, batch_size)]
))
```

LLM 响应：
妙蛙种子是宝可梦系列中的一种虚构宝可梦物种。它是一种草属性和毒属性的宝可梦，以其独特的外观为特征。
感谢您尝试我们的RAG（检索增强生成）应用！如果您对妙蛙种子有更多疑问，请随时提问。

在每次生成中，我们都能够在生成结束前添加 `phrase` 字符串。

### 4. MultipleChoiceLogitsProcessor

引导模型通过选择给定选项之一来回答多项选择题。

该处理器在需要严格遵守结构化答案格式的任务中特别有用，例如测验、调查或决策支持系统。

```python
example_prompts = [
"""
我白天接到很多电话。我买新手机时，什么因素对我来说更重要？
0. 摄像头
1. 电池
2. 操作系统
3. 屏幕分辨率

答案：
""",
]

mclp = MultipleChoiceLogitsProcessor(
    runner.tokenizer,
    choices=["0", "1", "2", "3"],
    delimiter="."
)

print(runner.generate_response(example_prompts, [mclp], max_tokens=1))
```

LLM 响应：
1

在这里，我们的模型除了选项之外没有生成任何其他内容。在使用Agent（智能体）或使用模型处理多项选择题时，这是一个非常有用的特性。

## 总结

无论您是生成简洁的摘要、制作聊天机器人响应，还是解决像多项选择题这样的结构化任务，logit 处理器都提供了有效控制输出的灵活性。这使得它们在需要精确性、遵守约束或特定任务行为的场景中变得不可或缺。

如果您有兴趣进一步探索如何使用 logit 处理器控制生成，以下是一些入门资源：

- 如何使用 Transformers 生成文本 – 一份面向初学者的指南，帮助理解 🤗 Transformers 中的文本生成。
- Hugging Face：生成策略 – 了解贪婪搜索、束搜索和 top-k 采样等解码策略。
- Hugging Face：LogitsProcessor API – 深入了解 🤗 Transformers 中 logits 处理的工作原理以及如何创建自定义 logits 处理器。
- NVIDIA 的 LogitsProcessorZoo – 通过示例和用例，探索 NVIDIA 库中可用的全套 logits 处理器。

借助 NVIDIA 的 LogitsProcessorZoo 和 Hugging Face 的工具，您拥有一个强大的生态系统，可以将您的语言模型应用提升到新的水平。尝试这些库，构建自定义解决方案，并与社区分享您的创作，以突破生成式 AI 的可能性边界。

---

> 本文由AI自动翻译，原文链接：[Controlling Language Model Generation with NVIDIA's LogitsProcessorZoo](https://huggingface.co/blog/logits-processor-zoo)
> 
> 翻译时间：2026-06-03 06:51
