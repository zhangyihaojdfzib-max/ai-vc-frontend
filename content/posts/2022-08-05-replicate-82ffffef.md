---
title: 自动化图像收集：用CLIP检索LAION数据集
title_original: Automating image collection – Replicate blog
date: '2022-08-05'
source: Replicate Blog
source_url: https://replicate.com/blog/grab-hundreds-of-images-with-clip-and-laion
author: ''
summary: 本文介绍了如何使用clip-retrieval工具从LAION-5B数据集中自动化收集图像。作者Clay展示了通过文本查询或图像相似度搜索，快速获取数百张匹配图像及其标题的方法。文章详细说明了安装配置、API调用流程，并探讨了如何将这些图像作为初始输入，引导文本到图像模型生成风格一致的变体。该方法为定制化机器学习模型提供了高效的数据采集方案。
categories:
- AI基础设施
tags:
- CLIP检索
- LAION数据集
- 图像收集
- 文本到图像
- Replicate
draft: false
translated_at: '2026-06-04T06:35:02.739383'
---

- Replicate  
- 博客  

# 自动化图像收集  

- afiaka87  

收集图像使我们能够以新颖且令人兴奋的方式定制强大的机器学习模型。例如，Replicate 上的一些文本到图像模型可以通过现有图像进行引导。当我们希望引导视觉模型朝向特定场景或美学风格时，这种能力非常有用，但这需要我们拥有自己的示例图像。  

我是 Clay，LAION 和 Replicate 团队的成员。在这篇文章中，我将向你展示如何使用名为 clip-retrieval 的 pip 包从 LAION-5B 数据集中收集数百张图像（以及对应的标题）。我们将探讨如何收集与文本描述匹配的图像，或与某些现有图像风格相似的图像。  

clip-retrieval 由 LAION 的另一位成员 Romain Beaumont 开发。它的工作原理是使用 CLIP 对 LAION 数据集中数十亿张图像和标题进行嵌入。借助 k-NN 和 autofaiss 的神奇功能，我们可以为这些嵌入创建一个内存索引，并实现相当快速的检索。如果你对这项技术层面的工作原理感兴趣，我推荐阅读 Romain 的文章《使用嵌入进行语义搜索：索引一切》。  

## 开始使用  

首先，安装 clip-retrieval：  

```
pip install clip-retrieval
```  

通过使用 `ClipRetrieval.ClipClient` 类，我们可以查询预构建的 CLIP faiss 索引。默认情况下，查询会发送到由 LAION-AI 构建的免费托管 LAION-5B knn 索引。  

我们可以设置自定义的 `num_images` 参数来指定返回的图像数量。这里我们暂时设为 400。  

```
from clip_retrieval.clip_client import ClipClient, Modality  

laion5b_search_client = ClipClient(  
    url="https://knn5.laion.ai/knn-service", # URL 可能会变化，请查看 github.com/rom1504/clip-retrieval  
    indice_name="laion5B",  
    num_images=400,  
)  
```  

## 使用文本查询 LAION-5B  

完成设置后，我们可以查询后端：  

```
results = laion5b_search_client.query(text="fresh avocado, digital art")  
```  

响应将是一个 JSON 数组，包含标题、URL 和相似度等结果。  

```
[  
  {  
    "caption": "Авокадо",  
    "url": "https://t1.ftcdn.net/jpg/00/79/43/44/240_F_79434473_qNSi5WUEi8y3oFrwPjupQvxbUIzXY7mE.jpg",  
    "id": 4540616960,  
    "similarity": 0.5977489948272705  
  } // ...更多结果  
]  
```  

![牛油果](/images/posts/ddf4c2622867.jpg)  

“fresh avocado, digital art” 的第二个结果  

由于 API 会去重结果，我们不会恰好得到 400 个结果。  

```
print(len(cat_results))  
$ 321  
```  

但 321 个结果也不算差！  

### 使用文本到图像模型获取图像的变体  

我喜欢用这种方法为各种文本到图像模型寻找良好的初始图像。初始图像可以引导文本到图像模型生成你图像的不同变体，同时受到指定提示词的影响。在某些情况下，使用初始图像甚至可以让模型运行得更快（我在之前的博客文章中也提到过初始图像）。  

我们可以使用 Replicate 轻松探索初始图像的效果。首先，在 Replicate 上进行设置：  

```
pip install replicate  
```  

从[这里](https://replicate.com)获取你的 API 令牌，然后将其设置为环境变量。  

```
export REPLICATE_API_TOKEN=...  
```  

现在，我们可以远程运行文本到图像模型了！我使用 `afiaka87/glid-3-xl`，这是一个逼真的图像模型，接受 `prompt` 和 `init_image` 参数。`init_image` 参数方便地接受 URL，因此无需提前下载 clip-retrieval 的结果。让我们使用搜索结果的第一个图像作为初始图像：  

```
model = replicate.models.get("afiaka87/glid-3-xl")  
version = model.versions.get("d74db2a276065cf0d42fe9e2917219112ddf8c698f5d9acbe1cc353b58097dab")  
text2image_generations = list(  
    version.predict(  
        prompt="fresh avocado, digital art",  
        guidance_scale=10.0,  
        batch_size=3,  
        init_image="https://t1.ftcdn.net/jpg/00/79/43/44/240_F_79434473_qNSi5WUEi8y3oFrwPjupQvxbUIzXY7mE.jpg",  
        steps=100,  
        init_skip_fraction=0.5,  
        seed=0,  
    )  
)[  
    -1  
]  # 获取最终生成结果 - 不需要中间输出。  
print(text2image_generations)  
```  

![生成结果 1](/images/posts/d8f26e5b3f79.png)  

![生成结果 2](/images/posts/595523a58f0d.png)  

![生成结果 3](/images/posts/aa5b5226b6ed.png)  

## 使用图像查询 Laion5B  

使用 clip-retrieval 的另一个酷炫功能是，可以拿一张现有图像，尝试找到与其相似的图像。  

为此，我们需要 CLIP。让我们加载 CLIP，并附带一些辅助方法，用于将 torch 张量转换为 clip-retrieval 所需的 numpy 数组。  

你可以在官方的 `clip_retrieval.clip_client` 笔记本中找到类似的示例和用法。  

### 加载 CLIP  

```
import clip  
import torch  

model, preprocess = clip.load("ViT-L/14", device="cpu", jit=True)  

import urllib  
import io  
import numpy as np  
from PIL import Image  

def download_image(url):  
    urllib_request = urllib.request.Request(  
        url,  
        data=None,  
    )  
    with urllib.request.urlopen(urllib_request, timeout=10) as r:  
        img_stream = io.BytesIO(r.read())  
    return img_stream  

def get_image_emb(image_url):  
    with torch.no_grad():  
        image = Image.open(download_image(image_url))  
        image_emb = model.encode_image(preprocess(image).unsqueeze(0).to("cpu"))  
        image_emb /= image_emb.norm(dim=-1, keepdim=True)  
        image_emb = image_emb.cpu().detach().numpy().astype("float32")[0]  
        return image_emb  
```  

### 将图像转换为 CLIP 嵌入并传递给 clip-retrieval  

现在我们不再使用文本作为输入并将其转换为文本嵌入，而是使用图像作为输入并将其转换为图像嵌入。  

让我们以这张穿着蓝色连衣裙的模特图像为例，寻找一些相似的图像。  

![输入图像：一位穿着蓝色连衣裙的女性图像](/images/posts/72f9b93865dc.jpg)  

输入图像是一位穿着蓝色连衣裙的女性。  

```
blue_dress_image_emb = get_image_emb("https://rukminim1.flixcart.com/image/612/612/kv8fbm80/dress/b/5/n/xs-b165-royal-blue-babiva-fashion-original-imag86psku5pbx2g.jpeg?q=70")  
blue_dress_results = laion5b_search_client.query(embedding_input=blue_dress_image_emb.tolist())  
blue_dress_results  
```  

同样，响应将是一个 JSON 数组，包含标题、URL 和相似度等结果。  

```
[  
  {  
    "caption": "8c7889e0b92b Cinderella Divine 1295 Long Chiffon Grecian Royal Blue Dress Mid Length  Sleeves V Neck ...",  
    "id": 2463946620,  
    "similarity": 0.9428964853286743,  
    "url": "https://cdn.shopify.com/s/files/1/1417/0920/products/1295cd-royal-blue_cfcbd4bc-ed74-47c0-8659-c1b8691990df.jpg?v=1527650905"  
  },  
  {  
    "caption": "Classy V-Neck A-Line Floor Length Zipper-Up Mother Of the Bride Dress",  
    "id": 717054383,  
    "similarity": 0.9329575896263123,  
    "url": "http://images.ericdress.com/Upload/Image/2014/44/270-360/0e842524-2bf0-44ef-be20-e9a6478db283.jpg"  
  }  
  // ...  
]  
```  

![第一个结果：8c7889e0b92b Cinderella Divine 1295 Long Chiffon Grecian Royal Blue Dress Mid Length Sleeves V Neck](/images/posts/e888647f74b3.jpg)  

第一个结果是“Cinderella Divine 1295 Long Chiffon Grecian Royal Blue Dress Mid Length Sleeves V Neck”。  

## 总结  

使用文本和图像查询 Laion5B 只是 clip-retrieval 的几种用法之一。  

深度学习的一个关键优势是，在拥有足够数据的情况下，我们可以扩展或微调模型，以提升通用性能和/或特定任务（“下游”）性能。借助 clip-retrieval，使用你自己整理的数据来微调模型已成为可能。我们将在未来的博客文章中展示如何微调你自己的模型，并在 Replicate 上运行它们。敬请期待！  

当然，还有其他用例。如果你有任何其他酷炫的想法，欢迎通过 Replicate 的 Discord 联系我们。我们很乐意倾听！

---

> 本文由AI自动翻译，原文链接：[Automating image collection – Replicate blog](https://replicate.com/blog/grab-hundreds-of-images-with-clip-and-laion)
> 
> 翻译时间：2026-06-04 06:35
