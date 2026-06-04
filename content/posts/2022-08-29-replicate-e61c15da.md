---
title: 通过API运行Stable Diffusion指南
title_original: Run Stable Diffusion with an API – Replicate blog
date: '2022-08-29'
source: Replicate Blog
source_url: https://replicate.com/blog/run-stable-diffusion-with-an-api
author: ''
summary: 本文介绍了如何通过Replicate平台，无需自建GPU基础设施，即可从代码中调用Stable Diffusion模型。文章详细说明了安装Python客户端、身份验证、运行预测等步骤，并提供了示例代码。Replicate按请求运行时间收费，比自建GPU更经济高效，适合开发者将Stable
  Diffusion集成到应用或项目中。
categories:
- AI基础设施
tags:
- Stable Diffusion
- API
- Replicate
- GPU
- 机器学习
draft: false
translated_at: '2026-06-04T06:34:41.094461'
---

- Replicate  
- 博客  

# 通过 API 运行 Stable Diffusion  

- zeke  

Stable Diffusion 作为开源项目的一大亮点在于，你可以对其进行修改并基于它构建各种应用。Photoshop 插件、机器人、动画、修复人类缺陷，各种用途应有尽有。  

但是，如果你想将其集成到应用或项目中，就需要配置 GPU 并在其前面搭建一个 API。而 GPU 成本高昂，因此你不想让它们一直处于开启状态。  

Replicate 让你无需搭建任何基础设施，就能从自己的代码中运行机器学习模型。在本文中，我们将向你展示如何使用它来运行 Stable Diffusion。  

![Discord 中 stable-diffusion-bot 生成可爱兔子的截图](/images/posts/fc5afe6f8f2e.webp)  

## 安装 Python 库  

我们维护了一个开源的 Python 客户端用于调用 API。使用 pip 安装：  

```
pip install replicate
```  

此外，还有一个由社区维护的 Node.js/JavaScript 库。请参阅 GitHub 上的 replicate-js。  

## 身份验证  

```
export REPLICATE_API_TOKEN=<token>
```  

你可以免费使用 API 一段时间，但最终我们会要求你输入信用卡信息。我们仅按你的请求运行时间的秒数收费，因此通常比你自己运行 GPU 要便宜得多。  

## 运行预测  

创建一个名为 `dream.py` 的文件，并粘贴以下内容：  

```
import replicate
import webbrowser

model = replicate.models.get("stability-ai/stable-diffusion")
version = model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")
output_url = version.predict(prompt="electric sheep, neon, synthwave")[0]
print(output_url)
webbrowser.open(output_url)
```  

然后在终端中运行该脚本：  

```
python dream.py
```  

这将通过 API 创建一个预测，并在你的网页浏览器中打开生成的图像。效果可能如下所示：  

![输出图像](/images/posts/540e3a6b3820.webp)  

## 查看你的预测  

每当你在 Replicate 上运行模型时，无论是在浏览器中还是通过 API，预测结果都会被保存并与你的用户账户关联。访问你的仪表板以查看所有之前的预测。  

- 了解如何使用 Stable Diffusion 构建 Discord 机器人  
- 查看更多你可以构建的示例  
- 尝试设置 `init_image` 以实现图像到图像的生成  
- 了解更多关于 HTTP API 的工作原理  
- 使用 andreasjansson/stable-diffusion-animation 生成动画  

加入我们的 Discord，向我们展示你的作品，或寻求帮助。我们期待看到你的创作。✨

---

> 本文由AI自动翻译，原文链接：[Run Stable Diffusion with an API – Replicate blog](https://replicate.com/blog/run-stable-diffusion-with-an-api)
> 
> 翻译时间：2026-06-04 06:34
