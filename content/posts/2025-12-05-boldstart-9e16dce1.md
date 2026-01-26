---
title: AWS在AI竞赛中加速追赶，发布智能体与基础设施更新
title_original: AWS takes an AI step forward - FastForward
date: '2025-12-05'
source: Boldstart Ventures
source_url: https://fastforward.boldstart.vc/aws-takes-an-ai-step-forward/
author: ''
summary: 本文回顾了AWS在re:Invent 2025大会上发布的AI相关更新，包括智能体创建工具AgentCore、S3向量存储功能以及更大的存储桶容量。文章分析了亚马逊在AI领域的战略转变，从两年前的被认为落后到如今试图通过基础设施优势与智能体叙事迎头赶上。同时，引用了分析师观点，指出AWS的更新虽全面但可能缺乏创新，并担忧其过度关注AI热潮而忽视核心企业服务。
categories:
- AI基础设施
tags:
- AWS
- 生成式AI
- 云计算
- 智能体
- 基础设施
draft: false
translated_at: '2026-01-08T04:28:40.049480'
---

# AWS在AI领域迈出一步

![特写：一位徒步者的靴子踏过崎岖地形，一只靴底的纹路清晰聚焦，背景是模糊的山地景观。](/images/posts/bc5728f0b5d0.jpg)

一年前的这周，我在AWS re:Invent大会上推出了《FastForward #1》。在这个星球上最令人分心的地方之一，置身于一场盛大会议的喧嚣中正式开启我的旅程，这真是个绝佳的起点。但我们已准备就绪，而且永远没有完美的时机。于是，我纵身一跃。

一年后，在发布了48期内容后，我重返拉斯维加斯，排着长长的出租车队伍，还被过于热心的活动安保人员找麻烦——仅仅因为我在Matt Garman的主题演讲结束后离开礼堂时，斗胆拍了一张照片。他们威胁要逮捕我并吊销我的证件，直到更冷静的头脑占了上风。我被放行，但心有余悸且颇为恼火，不过这也成了我在新闻中心向记者朋友们讲述的一个好故事。

![AWS CEO Matt Garman在re:Invent 2025上发表主题演讲。照片由亚马逊提供。](/images/posts/4c5d3f6f1f73.jpg)


但本周真正的故事并非关于我运营《FastForward》一年来的小插曲。而是关于re:Invent的主题，以及亚马逊在持续的AI竞赛中所处的位置。两年前，Adam Selipsky仍是AWS的CEO，当时业界普遍认为亚马逊已经落后。微软当时与OpenAI的紧密关系似乎让雷德蒙德（微软总部）占了上风。尽管大家都说为时尚早，但亚马逊内部似乎已弥漫着某种程度的恐慌。

六个月后，Selipsky卸任（正式离职），由AWS老将Matt Garman接替，他让公司在AI道路上走得更坚定。去年，Garman的首次主题演讲在发布AI公告前，重点强调了基础知识和亚马逊的基础设施优势。今年，“智能体”成为焦点，亚马逊呈现了一个更为连贯的AI叙事，涵盖了芯片、硬件、智能体创建工具以及亚马逊的大语言模型。但是，公司回避核心基础设施的故事，是否意味着失去了什么？

如果说认知就是一切，那么亚马逊本周在拉斯维加斯的一系列公告确实覆盖了所有基础。“这无疑帮助他们在所有关键领域迎头赶上，”Constellation Research的分析师Holger Mueller本周告诉《FastForward》。他特别喜欢诸如**更大的S3存储桶**这类更新，现在能处理高达50TB的对象，足以容纳大多数SAP ERP数据。他还强调了**S3 Vectors**的发布，该功能让客户能以亚马逊宣称的远低于独立向量数据库的成本查询向量数据。最后，他欣赏亚马逊的智能体故事，包括Amazon Bedrock **AgentCore**的更新以及为开发者、安全和DevOps推出的**新型通用智能体**的公告。

但Linthicum Research的创始人兼首席分析师David Linthicum对亚马逊的AI焦点提出了尖锐的批评。“我的总体看法是，这些公告感觉更像是‘跟风’之举，而非真正的创新。在追逐生成式AI热潮的过程中，AWS有可能忽视企业赖以生存的关键任务服务，”Linthicum说。“简而言之，AWS重新登上了AI新闻头条，但这些公告并未解决让企业夜不能寐的日常运营挑战。”

> “在追逐生成式AI热潮的过程中，AWS有可能忽视企业赖以生存的关键任务服务。”
> ~ David Linthicum，云顾问

正如Madrona Venture Group的合伙人、前AWS员工Jon Turow告诉我的那样，他并不完全认同亚马逊的方法。“传统的AWS乐高积木式方法，可能并不适合这代技术的抽象层次，”Turow特别提到了AgentCore。“开发者正在为智能体基础设施发现其他中间层次的抽象，这些抽象层次更高，同时仍可组合。”这些中间抽象层次隐藏了构建智能体的一些复杂性，而亚马逊的方法则提供了更基础但更灵活的工具。

亚马逊可能仍有很长的路要走，但至少它终于迈出了这一步——就像我去年发布这份通讯的第一期时那样。很难责怪这家公司在更全面地将AI融入产品组合时，坚持采用熟悉的方法。真正的考验在于，它能否在推进智能体的同时，不忽视使AWS取得今日成就的基础设施根基。

题图摄影：Ron Miller。

![前路漫漫，后会有期](/images/posts/ec97d1afeabe.jpg)

前路漫漫，后会有期

![感恩节科技随想](/images/posts/7cebd8b71c98.jpg)

感恩节科技随想

![AI原生者与AI跟风者](/images/posts/452f14424afe.jpg)

AI原生者与AI跟风者


> 本文由AI自动翻译，原文链接：[AWS takes an AI step forward - FastForward](https://fastforward.boldstart.vc/aws-takes-an-ai-step-forward/)
> 
> 翻译时间：2026-01-08 04:28
