---
title: AutoCog：用GPT-4自动生成Cog配置
title_original: AutoCog — Generate Cog configuration with GPT-4 – Replicate blog
date: '2023-04-19'
source: Replicate Blog
source_url: https://replicate.com/blog/autocog
author: ''
summary: 本文介绍了AutoCog，一个受Auto-GPT和BabyAGI启发、利用GPT-4自动为机器学习仓库生成Cog配置（cog.yaml和predict.py）的工具。其核心算法包括排序文件、调用GPT-4生成配置、运行预测并自动修复错误，最多尝试五次。文章还讨论了人在回路中的辅助作用、上下文窗口限制对提示词设计的影响，以及如何通过--continue标志实现人机协作。
categories:
- AI产品
tags:
- AutoCog
- GPT-4
- Cog配置
- 机器学习部署
- 自动化工具
draft: false
translated_at: '2026-06-02T06:34:47.678926'
---

- Replicate  
- 博客  

# AutoCog — 使用 GPT-4 生成 Cog 配置  

- andreasjansson  

Cog 让你只需少量代码就能从机器学习仓库创建 Docker 镜像。但如果连代码都不用写，岂不是更好？AutoCog 应运而生！  

受 Auto-GPT 和 BabyAGI 等工具的启发，AutoCog 利用 GPT-4 不仅编写代码，还能运行并修复代码。其算法大致如下：  

1. 向 AutoCog 提供一个机器学习仓库  
2. 根据文件对 Cog 的重要性进行排序  
3. 在 GPT-4 上下文窗口允许范围内，尽可能多地传入文件  
4. 指示 GPT-4 基于仓库中的文件创建 `cog.yaml` 和 `predict.py` 文件  
5. 创建一个 `cog predict` shell 命令，基于生成的文件运行预测  
6. 执行 `cog predict` 命令  
7. 如果失败，诊断错误并尝试修复 `cog.yaml`、`predict.py` 或 `cog predict` 命令。从上一步开始重复，最多尝试五次。  

## 人在回路中  

AutoCog 在成功时相当神奇，但很多时候它也会失败。有时它不知道确切的 Python 包版本，有时它会走上一条错误路径，导致每次尝试都让情况更糟。  

在这些情况下，你可能只想按 Ctrl-C 并自己修复。幸运的是，你的修复也不必完美，因为 AutoCog 有一个 `--continue` 标志，可以从你中断的地方继续。大多数时候，人类的一点轻微提示就足以帮助 AutoCog 找到可行的解决方案。  

## 为程序员编程  

AutoCog 本身是由人类——我——编写的。编写这样的工具就像在微观管理一位技术出色但判断力欠佳的程序员。一段时间后，你会对 GPT-4 产生同理心，并将任务分解成 GPT-4 有可能完成的小子任务。  

这些子任务包括一个提示词和解析输出的一些代码。例如，对目录中 Python 文件进行排序的提示词如下：  

```
给定以下文件路径和 README，请根据它们与推理的相关性，特别是与使用 Cog 为 Replicate 构建预测模型的相关性进行排序。按以下格式返回排序后的文件路径（确保只包含文件路径列表，不包含其他内容）：  

most_relevant.py  
second_most_relevant.py  
third_most_relevant.py  
[...]  
least_relevant.py  

以下是路径：  

{paths_list}  

路径结束。以下是 README：  

{readme_contents}  
```  

我们在将路径发送给 GPT-4 之前对其进行排序，原因是上下文窗口的长度限制。一个仓库中的 Python 代码通常超过 GPT-4 接受的 8096 个 Token，因此 AutoCog 会在将输入文件传递给 GPT-4 时进行截断。  

有限的上下文窗口是编写 AutoCog 这类工具时的主要障碍之一。提示词需要以尽可能包含更多信息的方式构建，同时不超出限制。  

## 亲自尝试  

你可以通过从 PyPI 安装 AutoCog 在自己的项目上运行它。更多使用文档请参见 GitHub README，地址为 andreasjansson/AutoCog。

---

> 本文由AI自动翻译，原文链接：[AutoCog — Generate Cog configuration with GPT-4 – Replicate blog](https://replicate.com/blog/autocog)
> 
> 翻译时间：2026-06-02 06:34
