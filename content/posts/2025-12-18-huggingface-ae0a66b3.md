---
title: Transformers v5分词器重构：架构与词汇表分离
title_original: 'Tokenization in Transformers v5: Simpler, Clearer, and More Modular'
date: '2025-12-18'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/tokenizers
author: null
summary: 本文介绍了Transformers v5中对分词器的重大重构，核心在于将分词器架构设计与训练好的词汇表分离，类似于PyTorch将网络架构与权重分离的理念。这一设计使得分词器内部结构更清晰、类层次更干净，并采用单一快速的后端。用户能够更轻松地检查、定制和从头训练分词器，而不再将其视为黑盒。文章还概述了分词的基本流程、算法以及如何通过Transformers库访问和使用分词器。
categories:
- AI基础设施
tags:
- Transformers
- 分词器
- 自然语言处理
- 大语言模型
- AI开发工具
draft: false
translated_at: '2026-01-05T16:35:07.397Z'
---

Transformers v5 中的分词：更简洁、更清晰、更模块化
Transformers v5 重新设计了分词器的工作方式。这次重大的分词器重构将分词器设计与训练好的词汇表分离开来（很像 PyTorch 将神经网络架构与学习到的权重分开）。结果是，你可以更轻松地检查、定制和从头开始训练分词器。
TL;DR：这篇博客解释了分词在 Transformers 中如何工作，以及为什么 v5 是一次重大的重新设计，它拥有更清晰的内部结构、干净的类层次结构和单一快速的后端。对于任何想要理解、定制或训练特定模型分词器，而不是将其视为黑盒的人来说，这是一份实用指南。
- 什么是分词？
- 分词流程
- 分词算法
- 通过 transformers 访问分词器
- transformers 中的分词器类层次结构
- AutoTokenizer 自动选择正确的分词器类
- v5 将分词器架构与训练好的词汇表分离
- 总结
专家提示：如果你已经熟悉这些概念，并想了解 v5 中的变化，请直接跳转到“v5 将分词器架构与训练好的词汇表分离”。
在深入探讨变化之前，让我们快速了解一下分词的作用以及各个部分是如何组合在一起的。
什么是分词？
语言模型不读取原始文本。它们处理通常称为 Token ID 或输入 ID 的整数序列。分词是将原始文本转换为这些 Token ID 的过程。（可以在此处尝试分词演示场以可视化分词过程。）
分词是自然语言处理和文本处理中广泛使用的一个概念。本文特别关注使用 transformers 和 tokenizers 库的大语言模型的分词。
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("HuggingFaceTB/SmolLM3-3B")
text = "Hello world"
tokens = tokenizer(text)
print(tokens["input_ids"])
# [9906, 1917]
print(tokenizer.convert_ids_to_tokens(tokens["input_ids"]))
# ['Hello', 'Ġworld']
`Ġworld`（上方）是一个单独的 Token，它代表字符序列 " world"（包含空格）。
Token 是模型看到的最小字符串单位。它可以是一个字符、一个单词或一个子词块，如 "play" 或 "##ing"（"##" 是一种模式，如果你现在不完全理解也没关系 🤗）。词汇表将每个唯一的 Token 映射到 Token ID。
print(tokenizer.vocab)
# {'ÎĹÎľ': 106502, 'ĠPeel': 89694, '.languages': 91078, ...}
一个好的分词器能将文本压缩成尽可能少的 Token。更少的 Token 意味着在不增加模型大小的情况下，有更多可用的上下文。训练一个分词器归根结底是为你的数据集找到最佳的压缩规则。例如，如果你处理中文语料库，有时会发现非常棒的惊喜 😉。
分词流程
分词分阶段进行。每个阶段在将文本传递给下一个阶段之前对其进行转换：
| 阶段 | 目的 | 示例 |
|---|---|---|
| 标准化器 | 标准化文本（小写、Unicode 标准化、空格清理） | "HELLO World" → "hello world" |
| 预分词器 | 将文本分割成初步块 | "hello world" → ["hello", " world"] |
| 模型 | 应用分词算法（BPE、Unigram 等） | ["hello", " world"] → [9906, 1917] |
| 后处理器 | 添加特殊 Token（BOS、EOS、填充） | [9906, 1917] → [1, 9906, 1917, 2] |
| 解码器 | 将 Token ID 转换回文本 | [9906, 1917] → "hello world" |
每个组件都是独立的。你可以更换标准化器或更改算法，而无需重写其他所有部分。
你可以通过 `_tokenizer` 访问基于 Rust 的分词器。我们在本节中会更深入地探讨它。
tokenizer = AutoTokenizer.from_pretrained("google/gemma-3-270m-it")
print(f"{tokenizer._tokenizer.normalizer=}")
# Replace(...)
print(f"{tokenizer._tokenizer.pre_tokenizer=}")
# Split(...)
print(f"{tokenizer._tokenizer.model=}")
# BPE(...)
print(f"{tokenizer._tokenizer.post_processor=}")
# TemplateProcessing(...)
print(f"{tokenizer._tokenizer.decoder=}")
# Sequence(decoders=[Replace(...), ByteFallback(), Fuse()])
分词算法
以下算法主导了现代语言模型的分词器：
- 字节对编码（BPE）迭代地合并最频繁的字符对。该算法是确定性的且被广泛使用。（阅读更多关于 BPE 的信息）
tokenizer = AutoTokenizer.from_pretrained("openai/gpt-oss-20b")
print(tokenizer._tokenizer.model)
# BPE(...)
- Unigram 采用概率方法，从庞大的初始词汇表中选择最可能的分割。这比严格的 BPE 更灵活。（阅读更多关于 Unigram 的信息）
tokenizer = AutoTokenizer.from_pretrained("google-t5/t5-base")
# Unigram(...)
- WordPiece 类似于 BPE，但使用基于似然的不同合并标准。（阅读更多关于 WordPiece 的信息）
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
# WordPiece(...)
通过 transformers 访问分词器
`tokenizers` 库是一个基于 Rust 的分词引擎。它快速、高效，并且完全与语言模型无关。该库处理将文本转换为 Token ID 及转换回来的机制。`tokenizers` 库是一个通用工具，实现了分词算法，但没有实现将这些算法连接到特定语言模型的约定。
考虑当你直接使用 `tokenizers` 库与 `SmolLM3-3B` 模型时会发生什么：
from tokenizers import Tokenizer
tokenizer = Tokenizer.from_pretrained("HuggingFaceTB/SmolLM3-3B")
text = "Hello world"
encodings = tokenizer.encode(text)
print(encodings.ids)
# [9906, 1917]
print(encodings.tokens)
输出是原始的分词结果。你得到了 Token ID 和它们对应的字符串片段。仅此而已。
现在考虑缺少了什么。`SmolLM3-3B` 是一个对话模型。当你与它交互时，你通常将输入结构化为带有 "user" 和 "assistant" 等角色的对话。语言模型期望有特殊的格式化 Token 来指示这些角色。原始的 `tokenizers` 库对此没有任何概念。
你如何弥合原始分词和模型要求之间的差距？
`transformers` 库弥合了这一差距。该库主要作为一个模型定义库而闻名，但它也提供了一个分词器抽象层，包装了原始的 `tokenizers` 后端并添加了模型感知功能。
以下是使用 `transformers` 包装器进行相同分词的结果：
# 使用模型的聊天模板格式化对话
prompt = "Give me a brief explanation of gravity in simple terms."
messages = [{"role": "user", "content": prompt}]
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
)
print(text)
# <|im_start|>system
# ...
# <|im_start|>user
# Give me a brief explanation of gravity in simple terms.<|im_end|>
# <|im_start|>assistant
model_inputs = tokenizer([text], add_special_tokens=False, return_tensors="pt")
注意像 `<|im_start|>` 和 `<|im_end|>` 这样的特殊 Token 是如何在分词前应用到提示词中的。这对于模型学习新序列的开始和结束位置很有用。
`transformers` 分词器添加了原始库所缺乏的一切：
- 聊天模板应用。`apply_chat_template` 方法根据模型预期的格式格式化对话，插入正确的特殊 Token 和分隔符。
- 自动特殊 Token 插入。在模型期望的位置添加序列开始和序列结束 Token。
- 截断至上下文窗口长度。

您可以指定
truncation=True
，分词器将遵循模型的最大序列长度。- 带填充的批量编码。多个输入可以通过正确的填充token和方向填充到相同长度。
- 返回格式选项。您可以请求PyTorch张量（`return_tensors="pt"`）、NumPy数组等。
`transformers` 实现了整个机器学习社区最常用的分词API（`encode`、`decode`、`convert_tokens_to_ids` 等）。

**`transformers` 中的分词器类层次结构**

`transformers` 库将分词器组织成一个类层次结构。顶层是一个定义通用接口的基类。其下方，后端类使用不同的引擎处理实际的分词工作。最底层，模型特定的类为特定模型配置后端。

**`PreTrainedTokenizerBase` 定义所有分词器的通用接口**

`PreTrainedTokenizerBase` 是 `transformers` 中所有分词器的抽象基类。它定义了每个分词器必须实现的接口。

基类处理不依赖于分词后端的功能：
- 特殊token属性。诸如 `bos_token`、`eos_token`、`pad_token` 和 `unk_token` 等属性在此定义。这些属性提供对模型用于标记序列边界和处理未知输入的特殊token的访问。
- 编码接口。`__call__` 方法、`encode` 和 `encode_plus` 方法在此定义。这些方法接受文本输入并返回token ID以及注意力掩码和其他元数据。
- 解码接口。`decode` 和 `batch_decode` 方法将token ID转换回文本。
- 序列化。`save_pretrained` 和 `from_pretrained` 方法处理下载正确的文件、读取信息、将分词器保存到磁盘等。
- 聊天模板支持。`apply_chat_template` 方法位于此处，根据存储在分词器配置中的Jinja模板格式化对话。

`transformers` 中的每个分词器最终都继承自 `PreTrainedTokenizerBase`。基类确保所有分词器行为一致，无论它们使用哪个后端进行实际分词。

**`TokenizersBackend` 封装 `tokenizers` 库**

`TokenizersBackend` 是大多数现代分词器的主要后端类。它继承自 `PreTrainedTokenizerBase` 并封装了基于Rust的 `tokenizers` 库。

该类在内部存储Rust分词器对象：
```python
class TokenizersBackend(PreTrainedTokenizerBase):
    def __init__(self, tokenizer_object, ...):
        self._tokenizer = tokenizer_object # The Rust tokenizer
        ...
```
当您在 `TokenizersBackend` 分词器上调用编码方法时，该类将实际的分词工作委托给Rust后端：
```python
def _batch_encode_plus(self, batch_text_or_text_pairs, ...):
    encodings = self._tokenizer.encode_batch(batch_text_or_text_pairs, ...)
    ...
```
Rust后端执行计算密集型工作，而Python包装器在其之上添加了模型感知功能。

许多模型特定的分词器继承自 `TokenizersBackend`，例如：
- `LlamaTokenizer`
- `GemmaTokenizer`

这些模型特定的类使用正确的词汇表、合并规则、特殊token和规范化设置为其各自的模型配置后端。

**`PythonBackend` 提供纯Python混入**

`PythonBackend` 继承自 `PreTrainedTokenizerBase` 并以纯Python实现分词。该类别名为 `PreTrainedTokenizer`。

纯Python后端存在有几个原因：
- 自定义分词逻辑。某些模型需要的分词行为不符合标准的 `tokenizers` 流水线。
- 遗留兼容性。较旧的模型实现可能依赖于Python特定的行为。

Python后端比Rust后端慢。对于大多数用例，推荐使用基于Rust的 `TokenizersBackend`。

继承自 `PythonBackend`（或其别名 `PreTrainedTokenizer`）的模型特定分词器包括一些较旧或专门的模型，例如：
- `CTRLTokenizer`
- `CanineTokenizer`

**`SentencePieceBackend` 处理SentencePiece模型**

`SentencePieceBackend` 继承自 `PythonBackend` 并提供与谷歌SentencePiece库的集成。SentencePiece是一个独立的分词库，许多模型都使用它，特别是那些由谷歌训练的模型。

该后端封装了一个SentencePiece处理器：
```python
class SentencePieceBackend(PythonBackend):
    def __init__(self, vocab_file, ...):
        self.sp_model = spm.SentencePieceProcessor()
        self.sp_model.Load(vocab_file)
        ...
```
使用SentencePiece分词模型的模型继承自此后端。例如：
- `SiglipTokenizer`
- `BartphoTokenizer`

`SentencePieceBackend` 继承自 `PythonBackend` 而不是直接继承自 `PreTrainedTokenizerBase`，因为它共享了许多相同的接口和填充/截断逻辑。

**`AutoTokenizer` 自动选择正确的分词器类**

`AutoTokenizer` 是加载分词器的推荐入口点。它会自动确定给定模型应使用哪个分词器类，并返回该类的实例。
```python
tokenizer = AutoTokenizer.from_pretrained("gpt2")
```
在幕后，`AutoTokenizer` 执行以下步骤：
- 下载分词器配置。`from_pretrained` 方法从Hub（或本地目录）获取 `tokenizer_config.json`。
- 识别模型类型。配置中包含标识模型类型的元数据（例如，"gpt2"、"llama"、"bert"）。
- 查找分词器类。`AutoTokenizer` 维护一个名为 `TOKENIZER_MAPPING_NAMES` 的映射，将模型类型映射到分词器类名：
```python
TOKENIZER_MAPPING_NAMES = {
    "gpt2": "GPT2Tokenizer",
    "llama": "LlamaTokenizer",
    "bert": "BertTokenizer",
    ...
}
```
- 实例化正确的类。`AutoTokenizer` 导入适当的分词器类并调用其 `from_pretrained` 方法。
- 返回配置好的分词器。您将获得一个完全配置好、模型特定的分词器，随时可用。

`AutoTokenizer` 的好处是您无需知道模型使用哪个分词器类。无论模型使用 `LlamaTokenizer`、`GPT2Tokenizer` 还是 `BertTokenizer`，相同的 `AutoTokenizer.from_pretrained("model-name")` 调用都有效。

`transformers` 中的分词器系统形成了一个分层架构：

| 层级 | 组件 | 职责 |
|---|---|---|
| 入口点 | `AutoTokenizer` | 自动选择并实例化正确的分词器类 |
| 模型特定 | `LlamaTokenizer`、`GPT2Tokenizer` 等 | 使用模型特定的架构（如规范化器、预分词器等）、特殊token和设置来配置后端 |
| 后端 | `TokenizersBackend`、`PythonBackend`、`SentencePieceBackend` | 使用特定引擎实现实际的分词 |
| 基类 | `PreTrainedTokenizerBase` | 定义通用接口和共享功能 |
| 引擎 | `tokenizers` (Rust)、`SentencePiece`、纯Python | 执行原始分词 |

**v5 将分词器架构与训练好的词汇表分离**

Transformers v5 中最重大的变化是分词器定义方式的理念转变。分词器现在的工作方式类似于PyTorch的 `nn.Module`：您首先定义架构，然后用学习到的参数填充它。

**v4 的问题：分词器不透明且紧密耦合**

在v4中，分词器是与预训练检查点文件绑定的黑盒。如果您加载 `LlamaTokenizerFast`，您无法轻松回答关于它的基本问题：
- 它是BPE还是Unigram？
- 它如何规范化文本？
- 它使用什么预分词策略？
- 特殊token是什么，它们的位置如何？
`__init__` 方法没有提供任何线索。

过去，你必须翻阅序列化文件或外部文档才能理解分词器的实际工作原理。
v4版本还为每个模型维护了两个并行实现：
- 一个“慢速”的Python分词器（`LlamaTokenizer`继承自`PreTrainedTokenizer`）
- 一个“快速”的基于Rust的分词器（`LlamaTokenizerFast`继承自`PreTrainedTokenizerFast`）。

这意味着：
- 每个模型有两个文件（例如，`tokenization_llama.py`和`tokenization_llama_fast.py`）
- 数百个模型之间存在代码重复
- 慢速和快速版本之间的行为差异，导致难以察觉的错误
- 用户对于何时使用哪种分词器感到困惑

最糟糕的是，你无法创建一个空的分词器架构。如果你想在自己的数据上训练一个LLaMA风格的分词器，没有一种简洁的方法来实例化一个“空白”的LLaMA分词器并用你的词汇表和合并规则来填充它。分词器仅作为加载的检查点存在，而不是作为可配置的模板。

**v5的解决方案：架构与参数分离**
v5将分词器架构（规范化器、预分词器、模型类型、后处理器、解码器）与训练参数（词汇表、合并规则）区分开来。这反映了PyTorch如何将模型架构与学习到的权重分离。

使用`nn.Module`，你先定义层：

```python
from torch import nn
model = nn.Sequential(
    nn.Embedding(vocab_size, embed_dim),
    nn.Linear(embed_dim, hidden_dim),
)
# 架构已定义；权重随机初始化或稍后加载
```

V5分词器遵循相同的模式：

```python
from transformers import LlamaTokenizer
# 实例化架构
tokenizer = LlamaTokenizer()
# 在自己的数据上训练以填充词汇表和合并规则
tokenizer.train(files=["my_corpus.txt"])
```

分词器类现在明确声明了其结构。查看v5中的`LlamaTokenizer`，你可以立即看到：
- 它使用BPE作为其分词模型
- 它可能在文本前添加前缀空格
- 其特殊Token（`<unk>`、`<bos>`、`<eos>`）位于特定的词汇表位置
- 它不对输入文本进行规范化
- 其解码器将元空格字符`▁`替换为空格

这种透明度在v4中是不可能的，因为相同的信息被埋藏在序列化文件中。

**一个文件，一个后端，一条推荐路径**
v5将双文件系统整合为每个模型一个文件。`LlamaTokenizer`现在继承自`TokenizersBackend`，它封装了之前作为“快速”实现暴露的基于Rust的分词器，现在成为默认后端。

之前的“慢速”Python实现明确位于`PythonBackend`之后，而`SentencePieceBackend`则保留给需要它的模型，但基于Rust的分词是首选的默认方式。

这一改变消除了：
- 慢速/快速实现之间的重复代码
- 令人困惑的`Tokenizer`与`TokenizerFast`命名约定
- 专门检查慢速-快速一致性的测试套件

用户现在有一个清晰的入口点。需要自定义的高级用户仍然可以访问底层组件，但库不再强迫每个人在两个并行实现之间导航。

**你现在可以从头开始训练特定模型的分词器**
假设你想要一个行为与LLaMA完全相同的分词器——相同的规范化、相同的预分词、相同的BPE模型类型——但训练在特定领域的语料库上（医学文本、法律文件、一种新语言）。在v4中，这需要从底层的`tokenizers`库原语手动重建分词器流水线。在v5中，你可以直接实例化架构并调用`train`：

```python
from datasets import load_dataset

# 初始化空白分词器
dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")

def get_training_corpus():
    batch = 1000
    for i in range(0, len(dataset), batch):
        yield dataset[i : i + batch]["text"]

trained_tokenizer = tokenizer.train_new_from_iterator(
    text_iterator=get_training_corpus(),
    vocab_size=32000,
    length=len(dataset),
    show_progress=True,
)

trained_tokenizer.push_to_hub("my_custom_tokenizer")
tokenizer = LlamaTokenizer.from_pretrained("my_custom_tokenizer")
```

生成的分词器将拥有你的自定义词汇表和合并规则，但会以与标准LLaMA分词器相同的方式处理文本，包括相同的空格处理、相同的特殊Token约定、相同的解码行为。

| 方面 | V4 | V5 |
|---|---|---|
| 每个模型的文件数 | 两个（`tokenization_X.py` , `tokenization_X_fast.py` ） | 一个（`tokenization_X.py` ） |
| 默认后端 | 在Python和Rust之间分割 | 首选Rust（`TokenizersBackend` ） |
| 架构可见性 | 隐藏在序列化文件中 | 在类定义中明确 |
| 从头开始训练 | 需要手动构建流水线 | `tokenizer.train(files=[...])` |
| 组件检查 | 困难，无文档说明 | 直接属性（`tokenizer.normalizer` 等） |
| 父类 | `PreTrainedTokenizer` , `PreTrainedTokenizerFast` | `TokenizersBackend` （或 `SentencePieceBackend` , `PythonBackend` ） |

从“分词器作为加载的检查点”到“分词器作为可配置的架构”的转变，使得库更加模块化、更加透明，并且更符合从业者构建机器学习系统时的思维方式。

**总结**
Transformers v5为分词带来了三项改进：
- 每个模型一个文件，而不是独立的慢速/快速实现
- 可见的架构，因此你可以检查规范化器、预分词器和解码器
- 可训练的模板，让你可以创建匹配任何模型设计的自定义分词器

`tokenizers`和Transformers之间的包装层仍然至关重要。它增加了模型感知、上下文长度、聊天模板、特殊Token等原始分词不提供的功能。V5只是让这一层更清晰、更可定制。

如果你想了解更多关于分词的信息，这里有一些资源：。


> 本文由AI自动翻译，原文链接：[Tokenization in Transformers v5: Simpler, Clearer, and More Modular](https://huggingface.co/blog/tokenizers)
> 
> 翻译时间：2026-01-05 13:15
