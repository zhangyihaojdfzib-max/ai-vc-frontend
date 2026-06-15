---
title: Transformers.js v3发布：WebGPU支持与120种新架构
title_original: 'Transformers.js v3: WebGPU Support, New Models & Tasks, and More…'
date: '2024-10-22'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/transformersjs-v3
author: ''
summary: Transformers.js v3正式发布，带来WebGPU支持，性能比WASM快100倍，新增多种量化格式，支持120种架构，并兼容Node.js、Deno和Bun。用户可通过NPM或CDN安装，启用WebGPU加速只需设置device参数。文章还展示了文本嵌入、语音识别和图像分类等示例，强调其在浏览器中实现高性能机器学习的潜力。
categories:
- AI基础设施
tags:
- Transformers.js
- WebGPU
- 机器学习
- 浏览器AI
- Hugging Face
draft: false
translated_at: '2026-06-15T07:20:12.407824'
---

# Transformers.js v3：WebGPU 支持、新模型与新任务等

经过一年多的开发，我们很高兴宣布 🤗 Transformers.js v3 正式发布！

亮点包括：

- WebGPU 支持（比 WASM 快 100 倍！）
- 新的量化格式（dtypes）
- 总共支持 120 种架构
- 25 个新的示例项目和模板
- Hugging Face Hub 上超过 1200 个预转换模型
- 兼容 Node.js（ESM + CJS）、Deno 和 Bun
- GitHub 和 NPM 上的新家

## 安装

你可以通过从 NPM 安装 Transformers.js v3 来开始使用：

```bash
npm i @huggingface/transformers

```

然后，通过以下方式导入库：

```js
import { pipeline } from "@huggingface/transformers";

```

或者，通过 CDN：

```js
import { pipeline } from "https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.0";

```

更多信息，请查看文档。

## WebGPU 支持

WebGPU 是一种用于加速图形和计算的新 Web 标准。该 API 使 Web 开发者能够利用底层系统的 GPU 直接在浏览器中执行高性能计算。WebGPU 是 WebGL 的继任者，提供了显著更好的性能，因为它允许与现代 GPU 进行更直接的交互。最后，它支持通用 GPU 计算，这使其非常适合机器学习！

截至 2024 年 10 月，全球 WebGPU 支持率约为 70%（根据 caniuse.com），这意味着部分用户可能无法使用该 API。

如果以下演示在你的浏览器中无法运行，你可能需要通过功能标志启用它：

- Firefox：使用 `dom.webgpu.enabled` 标志（参见此处）。
- Safari：使用 `WebGPU` 功能标志（参见此处）。
- 较旧的 Chromium 浏览器（Windows、macOS、Linux）：使用 `enable-unsafe-webgpu` 标志（参见此处）。

### 在 Transformers.js v3 中的使用

得益于我们与 ONNX Runtime Web 的合作，启用 WebGPU 加速只需在加载模型时设置 `device: 'webgpu'` 即可。让我们看一些示例！

示例：在 WebGPU 上计算文本嵌入（演示）

```js
import { pipeline } from "@huggingface/transformers";


const extractor = await pipeline(
  "feature-extraction",
  "mixedbread-ai/mxbai-embed-xsmall-v1",
  { device: "webgpu" },
);


const texts = ["Hello world!", "This is an example sentence."];
const embeddings = await extractor(texts, { pooling: "mean", normalize: true });
console.log(embeddings.tolist());





```

示例：在 WebGPU 上使用 OpenAI Whisper 执行自动语音识别（演示）

```js
import { pipeline } from "@huggingface/transformers";


const transcriber = await pipeline(
  "automatic-speech-recognition",
  "onnx-community/whisper-tiny.en",
  { device: "webgpu" },
);


const url = "https://huggingface.co/datasets/Xenova/transformers.js-docs/resolve/main/jfk.wav";
const output = await transcriber(url);
console.log(output);


```

示例：在 WebGPU 上使用 MobileNetV4 执行图像分类（演示）

```js
import { pipeline } from "@huggingface/transformers";


const classifier = await pipeline(
  "image-classification",
  "onnx-community/mobilenetv4_conv_small.e2400_r224_in1k",
  { device: "webgpu" },
);


const url = "https://huggingface.co/datasets/Xenova/transformers.js-docs/resolve/main/tiger.jpg";
const output = await classifier(url);
console.log(output);








```

## 新的量化格式（dtypes）

在 Transformers.js v3 之前，我们使用 `quantized` 选项来指定是否使用模型的量化（q8）或全精度（fp32）变体，分别将 `quantized` 设置为 `true` 或 `false`。现在，我们通过 `dtype` 参数增加了从更多选项中选择的能力。

可用的量化列表取决于模型，但一些常见的包括：全精度（"fp32"）、半精度（"fp16"）、8 位（"q8"、"int8"、"uint8"）和 4 位（"q4"、"bnb4"、"q4f16"）。

（例如，mixedbread-ai/mxbai-embed-xsmall-v1）

### 基本用法

示例：以 4 位量化运行 Qwen2.5-0.5B-Instruct（演示）

```js
import { pipeline } from "@huggingface/transformers";


const generator = await pipeline(
  "text-generation",
  "onnx-community/Qwen2.5-0.5B-Instruct",
  { dtype: "q4", device: "webgpu" },
);


const messages = [
  { role: "system", content: "You are a helpful assistant." },
  { role: "user", content: "Tell me a funny joke." },
];


const output = await generator(messages, { max_new_tokens: 128 });
console.log(output[0].generated_text.at(-1).content);

```

### 按模块设置 dtype

一些编码器-解码器模型，如 Whisper 或 Florence-2，对量化设置极为敏感，尤其是编码器部分。因此，我们增加了按模块选择 dtype 的能力，可以通过提供从模块名称到 dtype 的映射来实现。

示例：在 WebGPU 上运行 Florence-2（演示）

```js
import { Florence2ForConditionalGeneration } from "@huggingface/transformers";

const model = await Florence2ForConditionalGeneration.from_pretrained(
  "onnx-community/Florence-2-base-ft",
  {
    dtype: {
      embed_tokens: "fp16",
      vision_encoder: "fp16",
      encoder_model: "q4",
      decoder_model_merged: "q4",
    },
    device: "webgpu",
  },
);

```

![Florence-2 在 WebGPU 上运行](/images/posts/d727b6bd9bfe.gif)

```js
import {
  Florence2ForConditionalGeneration,
  AutoProcessor,
  AutoTokenizer,
  RawImage,
} from "@huggingface/transformers";


const model_id = "onnx-community/Florence-2-base-ft";
const model = await Florence2ForConditionalGeneration.from_pretrained(
  model_id,
  {
    dtype: {
      embed_tokens: "fp16",
      vision_encoder: "fp16",
      encoder_model: "q4",
      decoder_model_merged: "q4",
    },
    device: "webgpu",
  },
);
const processor = await AutoProcessor.from_pretrained(model_id);
const tokenizer = await AutoTokenizer.from_pretrained(model_id);


const url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg";
const image = await RawImage.fromURL(url);
const vision_inputs = await processor(image);


const task = "<MORE_DETAILED_CAPTION>";
const prompts = processor.construct_prompts(task);
const text_inputs = tokenizer(prompts);


const generated_ids = await model.generate({
  ...text_inputs,
  ...vision_inputs,
  max_new_tokens: 100,
});


const generated_text = tokenizer.batch_decode(generated_ids, {
  skip_special_tokens: false,
})[0];


const result = processor.post_process_generation(
  generated_text,
  task,
  image.size,
);
console.log(result);


```

## 120 种支持的架构

此版本将支持的架构总数增加到 120 种（查看完整列表），涵盖了广泛的输入模态和任务。值得注意的新增包括：Phi-3、Gemma 和 Gemma 2、LLaVa、Moondream、Florence-2、MusicGen、Sapiens、Depth Pro、PyAnnote 和 RT-DETR。

![Transformers.js v3 中新架构的气泡图](/images/posts/d0f8b2c8c170.png)

1. Cohere（来自 Cohere）发布，同时发表论文《Command-R：生产规模的检索增强生成》，作者为 Cohere。
2. Decision Transformer（来自伯克利/ Facebook/ Google）发布，同时发表论文《Decision Transformer：通过序列建模进行强化学习》，作者为 Lili Chen、Kevin Lu、Aravind Rajeswaran、Kimin Lee、Aditya Grover、Michael Laskin、Pieter Abbeel、Aravind Srinivas、Igor Mordatch。
3. Depth Pro（来自 Apple）发布，同时发表论文《Depth Pro：亚秒级锐利单目度量深度》，作者为 Aleksei Bochkovskii、Amaël Delaunoy、Hugo Germain、Marcel Santos、Yichao Zhou、Stephan R. Richter、Vladlen Koltun。
4. Florence2（来自 Microsoft）发布，同时发表论文《Florence-2：推进多种视觉任务的统一表示》，作者为 Bin Xiao、Haiping Wu、Weijian Xu、Xiyang Dai、Houdong Hu、Yumao Lu、Michael Zeng、Ce Liu、Lu Yuan。
5. Gemma（来自 Google）发布，同时发表论文《Gemma：基于 Gemini 技术与研究的开放模型》，作者为 Gemma Google 团队。
6. Gemma2（来自 Google）发布，同时发表论文《Gemma2：基于 Gemini 技术与研究的开放模型》，作者为 Gemma Google 团队。
7. Granite（来自 IBM）发布，同时发表论文《Power Scheduler：一种与批次大小和 Token 数量无关的学习率调度器》，作者为 Yikang Shen、Matthew Stallone、Mayank Mishra、Gaoyuan Zhang、Shawn Tan、Aditya Prasad、Adriana Meza Soria、David D. Cox、Rameswar Panda。
8. GroupViT（来自 UCSD、NVIDIA）发布，同时发表论文《GroupViT：从文本监督中涌现的语义分割》，作者为 Jiarui Xu、Shalini De Mello、Sifei Liu、Wonmin Byeon、Thomas Breuel、Jan Kautz、Xiaolong Wang。
9. Hiera（来自 Meta）发布，同时发表论文《Hiera：无冗余组件的层级视觉 Transformer》，作者为 Chaitanya Ryali、Yuan-Ting Hu、Daniel Bolya、Chen Wei、Haoqi Fan、Po-Yao Huang、Vaibhav Aggarwal、Arkabandhu Chowdhury、Omid Poursaeed、Judy Hoffman、Jitendra Malik、Yanghao Li、Christoph Feichtenhofer。
10. JAIS（来自 Core42）发布，同时发表论文《Jais 与 Jais-chat：以阿拉伯语为中心的基础模型与指令微调的开源生成式大语言模型》，作者为 Neha Sengupta、Sunil Kumar Sahu、Bokang Jia、Satheesh Katipomu、Haonan Li、Fajri Koto、William Marshall、Gurpreet Gosal、Cynthia Liu、Zhiming Chen、Osama Mohammed Afzal、Samta Kamboj、Onkar Pandit、Rahul Pal、Lalit Pradhan、Zain Muhammad Mujahid、Massa Baali、Xudong Han、Sondos Mahmoud Bsharat、Alham Fikri Aji、Zhiqiang Shen、Zhengzhong Liu、Natalia Vassilieva、Joel Hestness、Andy Hock、Andrew Feldman、Jonathan Lee、Andrew Jackson、Hector Xuguang Ren、Preslav Nakov、Timothy Baldwin、Eric Xing。
11. LLaVa（来自 Microsoft Research 与威斯康星大学麦迪逊分校）发布，同时发表论文《视觉指令微调》，作者为 Haotian Liu、Chunyuan Li、Yuheng Li 和 Yong Jae Lee。
12. MaskFormer（来自 Meta 与 UIUC）发布，同时发表论文《逐像素分类并非语义分割的全部所需》，作者为 Bowen Cheng、Alexander G. Schwing、Alexander Kirillov。
13. MusicGen（来自 Meta）发布，同时发表论文《简单可控的音乐生成》，作者为 Jade Copet、Felix Kreuk、Itai Gat、Tal Remez、David Kant、Gabriel Synnaeve、Yossi Adi 和 Alexandre Défossez。
14. MobileCLIP（来自 Apple）发布，同时发表论文《MobileCLIP：通过多模态强化训练实现快速图像-文本模型》，作者为 Pavan Kumar Anasosalu Vasu、Hadi Pouransari、Fartash Faghri、Raviteja Vemulapalli、Oncel Tuzel。
15. MobileNetV1（来自 Google Inc.）发布，同时发表论文《MobileNets：面向移动视觉应用的高效卷积神经网络》，作者为 Andrew G. Howard、Menglong Zhu、Bo Chen、Dmitry Kalenichenko、Weijun Wang、Tobias Weyand、Marco Andreetto、Hartwig Adam。
16. MobileNetV2（来自 Google Inc.）发布，同时发表论文《MobileNetV2：倒残差与线性瓶颈》，作者为 Mark Sandler、Andrew Howard、Menglong Zhu、Andrey Zhmoginov、Liang-Chieh Chen。
17. MobileNetV3（来自 Google Inc.）发布，同时发表论文《搜索 MobileNetV3》，作者为 Andrew Howard、Mark Sandler、Grace Chu、Liang-Chieh Chen、Bo Chen、Mingxing Tan、Weijun Wang、Yukun Zhu、Ruoming Pang、Vijay Vasudevan、Quoc V. Le、Hartwig Adam。
18. MobileNetV4（来自 Google Inc.）发布，同时发表论文《MobileNetV4——移动生态系统的通用模型》，作者为 Danfeng Qin、Chas Leichner、Manolis Delakis、Marco Fornoni、Shixin Luo、Fan Yang、Weijun Wang、Colby Banbury、Chengxi Ye、Berkin Akin、Vaibhav Aggarwal、Tenghui Zhu、Daniele Moro、Andrew Howard。
19. Moondream1 在仓库 moondream 中发布，作者为 vikhyat。
20. OpenELM（来自 Apple）发布，同时发表论文《OpenELM：具有开源训练与推理框架的高效语言模型家族》，作者为 Sachin Mehta、Mohammad Hossein Sekhavat、Qingqing Cao、Maxwell Horton、Yanzi Jin、Chenfan Sun、Iman Mirzadeh、Mahyar Najibi、Dmitry Belenko、Peter Zatloukal、Mohammad Rastegari。
21. Phi3（来自 Microsoft）发布，同时发表论文《Phi-3 技术报告：本地运行于手机的高能力语言模型》，作者为 Marah Abdin、Sam Ade Jacobs、Ammar Ahmad Awan、Jyoti Aneja、Ahmed Awadallah、Hany Awadalla、Nguyen Bach、Amit Bahree、Arash Bakhtiari、Harkirat Behl、Alon Benhaim、Misha Bilenko、Johan Bjorck、Sébastien Bubeck、Martin Cai、Caio César Teodoro Mendes、Weizhu Chen、Vishrav Chaudhary、Parul Chopra、Allie Del Giorno、Gustavo de Rosa、Matthew Dixon、Ronen Eldan、Dan Iter、Amit Garg、Abhishek Goswami、Suriya Gunasekar、Emman Haider、Junheng Hao、Russell J. Hewett、Jamie Huynh、Mojan Javaheripi、Xin Jin、Piero Kauffmann、Nikos Karampatziakis、Dongwoo Kim、Mahoud Khademi、Lev Kurilenko、James R. Lee、Yin Tat Lee、Yuanzhi Li、Chen Liang、Weishung Liu、Eric Lin、Zeqi Lin、Piyush Madan、Arindam Mitra、Hardik Modi、Anh Nguyen、Brandon Norick、Barun Patra、Daniel Perez-Becker、Thomas Portet、Reid Pryzant、Heyang Qin、Marko Radmilac、Corby Rosset、Sambudha Roy、Olatunji Ruwase、Olli Saarikivi、Amin Saied、Adil Salim、Michael Santacroce、Shital Shah、Ning Shang、Hiteshi Sharma、Xia Song、Masahiro Tanaka、Xin Wang、Rachel Ward、Guanhua Wang、Philipp Witte、Michael Wyatt、Can Xu、Jiahang Xu、Sonali Yadav、Fan Yang、Ziyi Yang、Donghan Yu、Chengruidong Zhang、Cyril Zhang、Jianwen Zhang、Li Lyna Zhang、Yi Zhang、Yue Zhang、Yunan Zhang、Xiren Zhou。
22. PVT（来自南京大学、香港大学等）发布，同时发表论文《金字塔视觉 Transformer：无需卷积的密集预测多功能骨干网络》，作者为 Wenhai Wang、Enze Xie、Xiang Li、Deng-Ping Fan、Kaitao Song、Ding Liang、Tong Lu、Ping Luo、Ling Shao。
23. PyAnnote 在仓库 pyannote/pyannote-audio 中发布，作者为 Hervé Bredin。
24. RT-DETR（来自百度）发布，同时发表论文《DETR 在实时目标检测上超越 YOLO》，作者为 Yian Zhao、Wenyu Lv、Shangliang Xu、Jinman Wei、Guanzhong Wang、Qingqing Dang、Yi Liu、Jie Chen。
25. Sapiens（来自 Meta AI）发布，同时发表论文《Sapiens：人类视觉模型的基础》，作者为 Rawal Khirodkar、Timur Bagautdinov、Julieta Martinez、Su Zhaoen、Austin James、Peter Selednik、Stuart Anderson、Shunsuke Saito。
26. ViTMAE（来自 Meta AI）发布，同时发表论文《掩码自编码器是可扩展的视觉学习器》，作者为 Kaiming He、Xinlei Chen、Saining Xie、Yanghao Li、Piotr Dollár、Ross Girshick。
27. ViTMSN（来自 Meta AI）发布，同时发表论文《用于标签高效学习的掩码孪生网络》，作者为 Mahmoud Assran、Mathilde Caron、Ishan Misra、Piotr Bojanowski、Florian Bordes、Pascal Vincent、Armand Joulin、Michael Rabbat、Nicolas Ballas。

## 示例项目与模板

作为发布的一部分，我们发布了 25 个新的示例项目和模板，主要聚焦于展示 WebGPU 支持！其中包括如下所示的 Phi-3.5 WebGPU 和 Whisper WebGPU 等演示。

我们正在将所有示例项目和演示迁移至 https://github.com/huggingface/transformers.js-examples，敬请关注后续更新！

![Phi-3.5 在 WebGPU 上运行](/images/posts/d4dfcee91124.gif)

![Whisper Turbo 在 WebGPU 上运行](/images/posts/c7f37ece745a.gif)

## 超过 1200 个预转换模型

截至今日发布，社区已成功转换超过1200个模型，使其兼容Transformers.js！您可在此处查看完整可用模型列表。

若您希望转换自有模型或微调版本，可使用我们的转换脚本，操作如下：

```sh
python -m scripts.convert --quantize --model_id <模型名称或路径>
```

将生成的文件上传至Hugging Face Hub后，请记得添加transformers.js标签，以便他人轻松查找并使用您的模型！

![可用Transformers.js模型](/images/posts/c14c16d772c6.jpg)

## Node.js（ESM + CJS）、Deno及Bun兼容性

Transformers.js v3现已兼容三大主流服务端JavaScript运行时：

## NPM与GitHub新家

最后，我们欣然宣布：Transformers.js将正式以@huggingface/transformers（取代v1和v2使用的@xenova/transformers）的名义，发布至Hugging Face官方NPM组织。

同时，我们已将代码仓库迁移至Hugging Face官方GitHub组织（https://github.com/huggingface/transformers.js），这里将成为我们的新家园——欢迎前来交流！我们期待倾听您的反馈、回应您的问题，并审阅您的PR！

这是一个重要的里程碑，我们衷心感谢社区帮助我们实现这一长期目标！没有各位的支持，这一切都无法实现……感谢大家！🤗

---

> 本文由AI自动翻译，原文链接：[Transformers.js v3: WebGPU Support, New Models & Tasks, and More…](https://huggingface.co/blog/transformersjs-v3)
> 
> 翻译时间：2026-06-15 07:20
