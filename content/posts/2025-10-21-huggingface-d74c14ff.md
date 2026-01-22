---
title: 利用开源模型优化OCR流程：选型、评估与进阶应用指南
title_original: Supercharge your OCR Pipelines with Open Models
date: '2025-10-21'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/ocr-open-models
author: ''
summary: 本文探讨了视觉-语言模型（VLMs）如何革新OCR技术，使其超越传统文本识别，能够处理复杂文档元素并支持文档问答。文章对比了顶尖开源OCR模型，分析了其能力、评估基准和成本效益，并提供了本地与远程运行模型的工具指南。最后，介绍了如何利用多模态检索和视觉语言模型实现超越OCR的文档智能应用，帮助读者根据具体需求选择合适的模型并深入理解文档AI的最新进展。
categories:
- AI基础设施
tags:
- OCR
- 开源模型
- 视觉-语言模型
- 文档AI
- 多模态检索
draft: false
translated_at: '2026-01-22T04:50:14.581492'
---

# 用开源模型为你的OCR流程注入强劲动力

- 
- 
- 
- 
- 
- 
- +292

![](/images/posts/785d7e16df1c.jpg)

![](/images/posts/377bb8640be1.png)

![](/images/posts/8c2942a398c6.jpg)

![](/images/posts/ac0e506ba48d.jpg)

![](/images/posts/0b27d2d98618.jpg)

![](/images/posts/31012e332645.jpg)

![merve的头像](/images/posts/78bab46e000b.jpg)

![Aritra Roy Gosthipaty的头像](/images/posts/287c63ff9896.jpg)

![Daniel van Strien的头像](/images/posts/ed23d04248c4.jpg)

![Hynek Kydlicek的头像](/images/posts/13e0aca0c3c0.jpg)

![Andres Marafioti的头像](/images/posts/e8e9ef3ca440.jpg)

![Vaibhav Srivastav的头像](/images/posts/4402b0abc4cd.jpg)

![Pedro Cuenca的头像](/images/posts/5b36678ab3e8.jpg)

目录简介现代OCR简介模型能力顶尖开源OCR模型最新模型对比模型评估运行模型的工具本地运行远程运行超越OCR总结我们已将Chandra和OlmOCR-2添加至本篇博客，并附上了模型的OlmOCR分数 🫡

- 目录
- 现代OCR简介模型能力
- 顶尖开源OCR模型最新模型对比模型评估
- 运行模型的工具本地运行远程运行超越OCR
- 总结

- 模型能力

- 最新模型对比
- 模型评估

- 本地运行
- 远程运行
- 超越OCR

**摘要：** 强大的视觉-语言模型的兴起改变了文档AI领域。每个模型都有其独特的优势，这使得选择合适的模型变得棘手。开源权重模型提供了更好的成本效益和隐私保护。为了帮助你入门，我们整理了这份指南。

在本指南中，你将了解到：

- 当前模型的格局及其能力
- 何时应该微调模型，何时可以直接使用现成模型
- 为你的用例选择模型时需要考虑的关键因素
- 如何通过多模态检索和文档问答超越OCR

到最后，你将知道如何选择合适的OCR模型，开始用它进行构建，并对文档AI有更深入的了解。我们开始吧！

- 用开源模型为你的OCR流程注入强劲动力现代OCR简介模型能力转录处理文档中的复杂组件输出格式OCR中的位置感知模型提示顶尖开源OCR模型最新模型对比模型评估基准测试成本效益开源OCR数据集运行模型的工具本地运行远程运行超越OCR视觉文档检索器使用视觉语言模型进行文档问答总结

- 现代OCR简介模型能力转录处理文档中的复杂组件输出格式OCR中的位置感知模型提示
- 顶尖开源OCR模型最新模型对比模型评估基准测试成本效益开源OCR数据集
- 运行模型的工具本地运行远程运行
- 超越OCR视觉文档检索器使用视觉语言模型进行文档问答
- 总结

- 模型能力转录处理文档中的复杂组件输出格式OCR中的位置感知模型提示

- 转录
- 处理文档中的复杂组件
- 输出格式
- OCR中的位置感知
- 模型提示

- 最新模型对比
- 模型评估基准测试成本效益开源OCR数据集

- 基准测试
- 成本效益
- 开源OCR数据集

- 本地运行
- 远程运行

- 视觉文档检索器
- 使用视觉语言模型进行文档问答

## 现代OCR简介

光学字符识别（OCR）是计算机视觉领域最早且持续时间最长的挑战之一。许多AI的早期实际应用都集中在将印刷文本转换为数字形式。

随着**视觉-语言模型**（VLMs）的兴起，OCR技术取得了显著进步。最近，许多OCR模型都是通过对现有VLM进行微调而开发的。但如今的能力已远远超越OCR：你可以通过查询检索文档，或直接回答关于文档的问题。得益于更强大的视觉特征，这些模型还能处理低质量扫描件，解释表格、图表和图像等复杂元素，并将文本与视觉信息融合，以回答跨文档的开放式问题。

最近的模型将文本转录成机器可读的格式。输入可以包括：

- 手写文本
- 各种文字，如拉丁文、阿拉伯文和日文字符
- 数学表达式
- 化学公式
- 图像/布局/页码标签

OCR模型将它们转换为机器可读的文本，这些文本可以有许多不同的格式，如HTML、Markdown等。

#### 处理文档中的复杂组件

除了文本，一些模型还能识别：

- 图像
- 图表
- 表格

有些模型知道图像在文档中的位置，提取其坐标，并将其适当地插入到文本之间。其他模型则为图像生成标题，并将其插入到图像出现的位置。如果你要将机器可读的输出输入到LLM（大语言模型）中，这尤其有用。例如AllenAI的**OlmOCR**，或PaddlePaddle的**PaddleOCR-VL**。

模型使用不同的机器可读输出格式，例如**DocTags**、**HTML**或**Markdown**（将在下一节“输出格式”中解释）。模型处理表格和图表的方式通常取决于它们使用的输出格式。有些模型将图表视为图像：保持原样。其他模型则将图表转换为markdown表格或JSON，例如，一个条形图可以按如下方式转换。

![图表渲染](/images/posts/4deeb8f13fc6.png)

同样，对于表格，单元格被转换为机器可读的格式，同时保留标题和列的上下文。

![表格渲染](/images/posts/75a65ee30b4c.png)

不同的OCR模型有不同的输出格式。简而言之，以下是现代模型常用的输出格式。
**DocTag：** DocTag是一种类似XML的文档格式，用于表达位置、文本格式、组件级信息等。下图是将一篇论文解析为DocTags的示意图。开源Docling模型采用了这种格式。

![DocTags](/images/posts/a6fa6fecec87.png)

- **HTML：** HTML是用于文档解析的最流行的输出格式之一，因为它能正确编码结构和层次信息。
- **Markdown：** Markdown是最具人类可读性的格式。它比HTML更简单，但表达能力不如HTML。例如，它无法表示分栏表格。
- **JSON：** JSON不是模型用于整个输出的格式，但可以用来表示表格或图表中的信息。

选择合适的模型取决于你计划如何使用其输出：

- **数字重建：** 要数字化重建文档，请选择具有保留布局格式（例如，DocTags或HTML）的模型。
- **LLM输入或问答：** 如果用例涉及将输出传递给LLM（大语言模型），请选择输出Markdown和图像标题的模型，因为它们更接近自然语言。
- **程序化使用：** 如果你想将输出传递给程序（如数据分析），请选择生成结构化输出（如JSON）的模型。

文档可能具有复杂的结构，例如多列文本块和浮动图形。旧的OCR模型通过检测单词，然后在后处理中手动检测页面布局来按阅读顺序呈现文本，这种方式很脆弱。而现代OCR模型则整合了布局元数据，以帮助保持阅读顺序和准确性。这种元数据被称为“锚点”，它可以以边界框的形式出现。这个过程也被称为“接地/锚定”，因为它有助于减少幻觉。

OCR模型可以接收图像和可选的文本提示词，这取决于模型架构和预训练设置。部分OCR模型支持基于提示词的任务切换，例如granite-docling可以通过提示词“将此页面转换为Docling”来解析整个页面，同时它也能处理类似“将此公式转换为LaTeX”的提示词并配合一个满是公式的页面。然而，其他模型仅针对解析整个页面进行训练，它们通过系统提示词来设定执行此任务。例如，AllenAI的OlmOCR采用一个长的条件提示词。与许多其他模型类似，OlmOCR在技术上是一个VLM（本例中是Qwen2.5VL）的OCR微调版本，因此你可以用提示词要求其他任务，但其性能将无法与其OCR能力相提并论。

## 前沿的开源OCR模型

过去一年我们见证了新模型涌现的惊人浪潮。由于大量工作在开源领域进行，这些参与者相互借鉴并受益于彼此的工作。一个很好的例子是AllenAI发布的OlmOCR，它不仅发布了模型，还发布了用于训练的数据集。有了这些，其他人可以在新的方向上以此为基础进行构建。这个领域异常活跃，但并非总是清楚该使用哪个模型。

### 最新模型对比

为了让事情简单些，我们整理了一份非详尽对比，列出我们当前最喜欢的一些模型。以下所有模型都具备版面感知能力，可以解析表格、图表和数学公式。每个模型支持的全部语言列表详见其模型卡片，如果你感兴趣请务必查看。以下所有模型均采用开源许可证，但Chandra采用OpenRAIL许可证，而Nanonets的许可证不明确。平均分取自Chandra、OlmOCR的模型卡片，基于OlmOCR基准（仅限英语）评估得出。
本集合中的许多模型都是从Qwen2.5-VL或Qwen3-VL微调而来，因此我们在下方也提供了Qwen3-VL模型。

虽然Qwen3-VL本身是一个功能强大且多用途的视觉语言模型，经过后训练用于文档理解和其他任务，但它并未针对单一、通用的OCR提示词进行优化。相比之下，其他模型使用一个或几个专门为OCR任务设计的固定提示词进行了微调。因此，要使用Qwen3-VL，我们建议尝试不同的提示词。

这里有一个小型演示，供你尝试一些最新模型并比较它们的输出。

没有单一的最佳模型，因为每个问题都有不同的需求。表格应该用Markdown还是HTML呈现？我们应该提取哪些元素？我们应如何量化文本准确率和错误率？👀虽然存在许多评估数据集和工具，但很多并不能回答这些问题。因此我们建议使用以下基准：

1.  OmniDocBenchmark：这个广泛使用的基准因其多样化的文档类型（书籍、杂志和教科书）而脱颖而出。其评估标准设计精良，接受HTML和Markdown两种格式的表格。一种新颖的匹配算法评估阅读顺序，公式在评估前会进行标准化。大多数指标依赖于编辑距离或树编辑距离（表格）。值得注意的是，用于评估的标注并非完全由人工生成，而是通过SoTA VLM或传统OCR方法获取。
2.  OlmOCR-Bench：OlmOCR-Bench采用不同的方法：他们将评估视为一组单元测试。例如，表格评估通过检查给定表格选定单元格之间的关系来完成。他们使用来自公共来源的PDF，标注则使用多种闭源VLM完成。这个基准在英语评估上相当成功。
3.  CC-OCR（多语言）：与之前的基准相比，CC-OCR在挑选模型时不太受青睐，因为其文档质量和多样性较低。然而，它是唯一包含英语和中文以外语言评估的基准！虽然评估远非完美（图像是包含少量文字的图片），但它仍然是进行多语言评估的最佳选择。

在测试不同的OCR模型时，我们发现它们在不同文档类型、语言等方面的性能差异很大。你所在的领域可能未在现有基准中得到充分体现！为了有效利用这新一代基于VLM的OCR模型，我们建议致力于收集你任务领域中具有代表性的示例数据集，并测试几个不同的模型以比较它们的性能。

大多数OCR模型规模较小，参数量在30亿到70亿之间；你甚至可以找到参数量少于10亿的模型，例如PaddleOCR-VL。然而，成本也取决于针对专用推理框架的优化实现是否可用。例如，OlmOCR-2提供了vLLM和SGLang实现，每百万页的成本是178美元（假设在H100上，每小时2.69美元）。DeepSeek-OCR在单个40GB VRAM的A100上每天可以处理超过20万页。粗略计算，我们发现每百万页的成本与OlmOCR大致相似（尽管这取决于你的A100提供商）。如果你的使用场景不受影响，也可以选择模型的量化版本。运行开源模型的成本很大程度上取决于实例的小时费用以及模型包含的优化，但可以保证在较大规模上比许多闭源模型更便宜。

虽然过去一年开源OCR模型激增，但开放训练和评估数据集的数量并未同步增长。一个例外是AllenAI的olmOCR-mix-0225，它已被用于在Hub上训练至少72个模型——可能更多，因为并非所有模型都记录了其训练数据。

共享更多数据集可能为开源OCR模型带来更大的进步。创建这些数据集有几种有前景的方法：

*   合成数据生成（例如，isl_synthetic_ocr）
*   VLM生成的转录，通过人工或启发式方法过滤
*   使用现有OCR模型为特定领域的新模型（可能更高效）生成训练数据
*   利用现有的已校正数据集，如Medical History of British India Dataset，其中包含针对历史文档进行过大量人工校正的OCR

值得注意的是，许多此类数据集存在但未被使用。将它们作为“训练就绪”的数据集更易于获取，对开源社区具有相当大的潜力。

我们收到了许多关于如何开始使用OCR模型的问题，因此这里提供几种方法，你可以使用本地推理工具并通过Hugging Face进行远程托管。

大多数前沿模型都支持vLLM和transformers实现。你可以从模型各自的卡片中获取关于如何部署每个模型的更多信息。为了方便起见，我们在此展示如何使用vLLM进行本地推理。以下代码可能因模型而异，但对于大多数模型，它看起来如下所示。

```
vllm serve nanonets/Nanonets-OCR2-3B

```

然后你可以使用例如OpenAI客户端进行如下查询。

```
from openai import OpenAI
import base64

client = OpenAI(base_url="http://localhost:8000/v1")

model = "nanonets/Nanonets-OCR2-3B"

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

```python
def infer(img_base64):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img_base64}"},
                    },
                    {
                        "type": "text",
                        "text": "像自然阅读一样，从上述文档中提取文本。",
                    },
                ],
            }
        ],
        temperature=0.0,
        max_tokens=15000
    )
    return response.choices[0].message.content

img_base64 = encode_image(your_img_path)
print(infer(img_base64))

```

Transformers 提供了标准的模型定义，便于推理和微调。Transformers 中可用的模型要么带有官方的 transformers 实现（库内的模型定义），要么是“远程代码”实现。后者由模型所有者定义，以便于将模型加载到 transformers 接口中，这样您就无需深入了解模型实现。以下是一个使用 transformers 实现加载 Nanonets 模型的示例。

```
# 请确保安装 flash-attn 和 transformers
from transformers import AutoProcessor, AutoModelForImageTextToText

model = AutoModelForImageTextToText.from_pretrained(
    "nanonets/Nanonets-OCR2-3B", 
    torch_dtype="auto", 
    device_map="auto", 
    attn_implementation="flash_attention_2"
)
model.eval()
processor = AutoProcessor.from_pretrained("nanonets/Nanonets-OCR2-3B")

def infer(image_url, model, processor, max_new_tokens=4096):
    prompt = """像自然阅读一样，从上述文档中提取文本。以 HTML 格式返回表格。以 LaTeX 表示法返回公式。如果文档中有图像且没有图像标题，请在 <img></img> 标签内添加图像的简短描述；否则，将图像标题放在 <img></img> 标签内。水印应包裹在括号中。例如：<watermark>OFFICIAL COPY</watermark>。页码应包裹在括号中。例如：<page_number>14</page_number> 或 <page_number>9/22</page_number>。对于复选框，优先使用 ☐ 和 ☑。"""
    image = Image.open(image_path)
    messages = [
        {"role": "system", "content": "你是一个有用的助手。"},
        {"role": "user", "content": [
            {"type": "image", "image": image_url},
            {"type": "text", "text": prompt},
        ]},
    ]
    text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = processor(text=[text], images=[image], padding=True, return_tensors="pt").to(model.device)
    
    output_ids = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
    generated_ids = [output_ids[len(input_ids):] for input_ids, output_ids in zip(inputs.input_ids, output_ids)]
    
    output_text = processor.batch_decode(generated_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return output_text[0]

result = infer(image_path, model, processor, max_new_tokens=15000)
print(result)

```

MLX 是一个面向 Apple Silicon 的开源机器学习框架。MLX-VLM 构建在 MLX 之上，旨在轻松服务视觉语言模型。您可以在此处探索所有 MLX 格式可用的 OCR 模型。它们也提供量化版本。您可以按如下方式安装 MLX-VLM。

```
pip install -U mlx-vlm

```

```
wget https://huggingface.co/datasets/merve/vlm_test_images/resolve/main/throughput_smolvlm.png

python -m mlx_vlm.generate --model ibm-granite/granite-docling-258M-mlx --max-tokens 4096 --temperature 0.0 --prompt "将此图表转换为 JSON。" --image throughput_smolvlm.png 

```

用于托管部署的推理端点
您可以在 Hugging Face 推理端点上部署与 vLLM 或 SGLang 兼容的 OCR 模型，可以通过模型仓库的“部署”选项，或直接通过推理端点界面进行部署。推理端点在完全托管的、具备 GPU 加速、自动扩缩容和监控功能的环境中提供尖端模型服务，无需手动管理基础设施。

以下是一个使用 vLLM 作为推理引擎部署 nanonets 的简单方法。

1.  导航到模型仓库 nanonets/Nanonets-OCR2-3B
2.  点击“部署”按钮并选择“HF 推理端点”

![推理端点](/images/posts/a8517f7431e4.png)

1.  在几秒钟内配置部署设置

![推理端点](/images/posts/01a585c41b74.png)

1.  端点创建后，您可以使用我们在上一节中提供的 OpenAI 客户端代码片段来调用它。

您可以在此处了解更多信息。

用于批量推理的 Hugging Face Jobs

对于许多 OCR 应用，您希望进行高效的批量推理，即以尽可能廉价和高效的方式在数千张图像上运行模型。一个好的方法是使用 vLLM 的离线推理模式。如上所述，vLLM 支持许多基于 VLM 的最新 OCR 模型，它可以高效地对图像进行批处理并大规模生成 OCR 输出。

为了使其更加简便，我们创建了 uv-scripts/ocr，这是一个与 Hugging Face Jobs 配合使用的、开箱即用的 OCR 脚本集合。这些脚本让您无需自己的 GPU 即可在任何数据集上运行 OCR。只需将脚本指向您的输入数据集，它将：

-   使用多种不同的开源 OCR 模型处理数据集列中的所有图像
-   将 OCR 结果作为新的 Markdown 列添加到数据集中
-   将包含 OCR 结果的更新数据集推送到 Hub

例如，要在 100 张图像上运行 OCR：

```
hf jobs uv run --flavor l4x1 \
  https://huggingface.co/datasets/uv-scripts/ocr/raw/main/nanonets-ocr.py \
  your-input-dataset your-output-dataset \
  --max-samples 100

```

这些脚本会自动处理所有 vLLM 配置和批处理，使得无需设置基础设施即可进行批量 OCR。

如果您对文档 AI 而不仅仅是 OCR 感兴趣，以下是我们的一些推荐。

#### 视觉文档检索器

视觉文档检索是指给定一个文本查询时，检索出最相关的前 k 个文档。如果您以前使用过检索器模型，区别在于您可以直接在一堆 PDF 文件上进行搜索。除了单独使用它们，您还可以将它们与视觉语言模型结合来构建多模态 RAG 管道（了解如何操作请点击此处）。您可以在 Hugging Face Hub 上找到所有相关模型。

视觉文档检索器有两种类型：单向量模型和多向量模型。单向量模型内存效率更高但性能稍逊；而多向量模型内存占用更大但性能更强。这些模型大多都集成了 vLLM 和 transformers，因此您可以使用它们索引文档，然后通过向量数据库轻松进行搜索。

#### 使用视觉语言模型进行文档问答

如果您手头的任务只需要基于文档回答问题，可以使用一些在训练任务中包含文档任务的视觉语言模型。我们观察到用户尝试将文档转换为文本，然后将输出传递给 LLM，但如果您的文档布局复杂，并且转换后的文档以 HTML 等形式输出图表，或者图像标题不正确，LLM 就会遗漏信息。相反，将您的文档和查询输入到像 Qwen3-VL 这样的先进视觉语言模型中，以避免遗漏任何上下文。

在这篇博文中，我们旨在为您概述如何选择 OCR 模型、现有的尖端模型及其能力，以及帮助您入门 OCR 的工具。如果您想了解更多关于 OCR 和视觉语言模型的信息，我们鼓励您阅读以下资源。

-   视觉语言模型详解
-   视觉语言模型 2025 年更新
-   关于 PP-OCR-v5 的博客
-   教程：在 Grounded OCR 上微调 Kosmos2.5
-   教程：在 DocVQA 上微调 Florence-2
-   使用 Core ML 和 dots.ocr 在设备端实现 SOTA OCR

更多博客文章

![](/images/posts/57c18bf76f3f.png)

## Smol2Operator：用于计算机使用的训练后 GUI Agent（智能体）

-
-
-
-
-   +1

![](/images/posts/a69384612bd4.png)

![](/images/posts/78bab46e000b.jpg)

![](/images/posts/dc8511e60da5.jpg)

![](/images/posts/4402b0abc4cd.jpg)

![](/images/posts/57c02494e0b8.png)

## Gemma 3n 现已完全融入开源生态系统！

-
-
-
-
-   +4

![](/images/posts/287c63ff9896.jpg)

![](/images/posts/5b36678ab3e8.jpg)

![](/images/posts/dc8511e60da5.jpg)

![](/images/posts/4402b0abc4cd.jpg)

要是上周就有这个就好了！我上周花时间学习并测试了所有这些模型以及额外的模型，我想指出一个更正。OlmOCR 并非仅支持英语的模型，事实上，在我的阿拉伯语语料库上，它在所有 VLM 和非 VLM 框架中都取得了最佳结果。

-
-
-
-   6 条回复

![](/images/posts/2b67df64c3a7.png)

![](/images/posts/78bab46e000b.jpg)

![](/images/posts/2b67df64c3a7.png)

你测试了哪些 VLM？

![](/images/posts/b3ef056e6ca0.jpg)

总结得很棒！别忘了，DeepSeek OCR 也支持 Grounded OCR！

![](/images/posts/61190997e9b3.png)

想知道为什么比较中没有包含 minerU 2.5 模型？MinerU2.5-2509-1.2B

![](/images/posts/1ffd57c1b408.jpg)

非常有帮助的分析。布局感知能力和成本优势确实突出。感谢分享！

![](/images/posts/f4f352087b1c.jpg)

卓越的见解和基准测试分析。我将使用这里的数据集进行评估。

![](/images/posts/106861fcab87.png)

LightOnOCR-1B 非常适合加入本次比较，作为一个表现出色、超越其体量的强者：

-   🎯性能：在其规模上，在 OlmOCR 基准测试中取得了最先进的结果——击败了 DeepSeek-OCR，与 dots.ocr 持平（尽管体积小了 3 倍），与 PaddleOCR-VL 表现相当，并超过 Qwen3-VL-2B 16 分
-   ⚡速度：比 dots.ocr 快 6 倍，比 PaddleOCR-VL-0.9B 快 2 倍，比 DeepSeekOCR 快 1.73 倍
-   💸效率：在单个 H100 上每秒处理 5.71 页（约每天 493,000 页），每 1,000 页成本 < $0.01
-   🧠端到端：完全可微分，无需外部 OCR 流程——易于针对特定领域进行微调以改进
-   🧾多功能：可处理表格、收据、表单、多栏布局和数学符号
-   🌍紧凑变体：提供 32k 和 16k 词汇表选项，针对欧洲语言进行了优化

![bench](/images/posts/bd9479bb5bef.png)

· 注册或登录以发表评论

-
-
-
-
-
-
-
-
-
-
-
-
-   +286

![](/images/posts/785d7e16df1c.jpg)

![](/images/posts/377bb8640be1.png)

![](/images/posts/8c2942a398c6.jpg)

![](/images/posts/ac0e506ba48d.jpg)

![](/images/posts/0b27d2d98618.jpg)

![](/images/posts/31012e332645.jpg)

![](/images/posts/7440861c1fd8.jpg)

![](/images/posts/4e1cfa4fde04.png)

![](/images/posts/5fccaeadb224.jpg)

![](/images/posts/25b209f83d7f.png)

![](/images/posts/c93e8dc76332.jpg)

---

> 本文由AI自动翻译，原文链接：[Supercharge your OCR Pipelines with Open Models](https://huggingface.co/blog/ocr-open-models)
> 
> 翻译时间：2026-01-22 04:50
