---
title: 微软在NSDI 2026展示大规模网络系统新进展
title_original: 'Microsoft at NSDI 2026: Advances in large-scale networked systems
  - Microsoft Research'
date: '2026-05-05'
source: Microsoft Research
source_url: https://www.microsoft.com/en-us/research/blog/microsoft-at-nsdi-2026-advances-in-large-scale-networked-systems/
author: ''
summary: 微软作为NSDI 2026的回归赞助商，共有11篇论文被接收，涵盖数据中心、广域网、AI系统和云基础设施。论文展示了DroidSpeak（跨模型KV缓存共享）、Eywa（LLM自动化协议测试）、Octopus（CXL内存池无交换机设计）、HEDGE（概率链路容量流量工程）和AVA（视觉语言模型视频分析）等创新成果，体现了微软在大规模网络系统设计与运行方面的前沿研究。
categories:
- 技术趋势
tags:
- NSDI 2026
- 大规模网络系统
- 微软研究
- 数据中心
- AI基础设施
draft: false
translated_at: '2026-05-06T05:27:33.791353'
---

大规模网络系统支撑着云计算、人工智能以及分布式应用和服务。USENIX网络系统设计与实现研讨会2026（在新标签页中打开）（NSDI '26）是一个领先的论坛，研究人员和实践者在此分享关于这些系统设计与运行的新研究、见解和进展。

微软很荣幸作为回归赞助商支持NSDI '26，这体现了我们持续致力于推进系统和网络研究、并与更广泛社区互动的承诺。微软的研究人员和工程领导也担任了程序委员会成员及其他组织角色。

今年，微软作者及合作者的11篇论文被会议接收，涵盖数据中心和广域网、人工智能系统以及云基础设施。这些论文共同展示了在构建和运行大规模网络系统方面的进展。

播客系列

## 医学领域的AI革命，再探讨

与微软的Peter Lee一同探索AI如何影响医疗保健及其对医学未来的意义。

## 技术分会

5月4日星期一，下午2:00–3:20

### DroidSpeak：跨微调模型变体的KV缓存共享（在新标签页中打开）

Yuhan Liu, Yuyang Huang, Jiayi Yao, Zhuohan Gu, Kuntai Du, Hanchen Li, Yihua Cheng, 和 Junchen Jiang，芝加哥大学；Shan Lu, Madan Musuvathi, 和 Esha Choukse，微软

DroidSpeak使具有相同架构的LLM能够跨模型共享和部分重用KV缓存，实现高达4倍的吞吐量提升和更快的响应速度，同时对输出质量影响极小。

5月4日星期一，下午3:50–5:30

### Eywa：使用LLM自动化基于模型的测试（在新标签页中打开）

Rajdeep Mondal, Rathin Singha, Todd D. Millstein, 和 George Varghese，加州大学洛杉矶分校；Ryan Beckett 和 Siva Kesava Reddy Kakarla，微软研究院

Eywa利用LLM从自然语言源自动构建协议模型，实现基于模型的测试。它在广泛使用的网络协议实现中发现了33个错误，包括16个此前未知的错误。

5月5日星期二，下午2:00–3:20

### Octopus：通过稀疏拓扑增强CXL内存池（在新标签页中打开）

Yuhong Zhong，哥伦比亚大学；Fiodar Kazhamiaka, Pantea Zardoshti, Shuwei Teng 和 Rodrigo Fonseca，微软Azure；Mark D. Hill，威斯康星大学麦迪逊分校；Daniel S. Berger，微软Azure和华盛顿大学

Octopus为解耦内存池引入了一种无交换机设计，降低了成本并可扩展至多机架内存池。在一个三服务器硬件原型上，Octopus RPC比机架内RDMA快3.2倍，比CXL交换机快2.4倍。

5月5日星期二，下午3:50–5:30

### HEDGE：基于概率链路容量的流量工程（在新标签页中打开）

Arjun Devraj，康奈尔大学；Bill Owens，NYSERNet；Umesh Krishnaswamy，微软；Ying Zhang，Meta；Rachee Singh，康奈尔大学

HEDGE通过结合链路本地和全局网络范围的弹性来缓解光网络中的波长特定故障，在链路性能波动的情况下维持稳定的容量并优化流量。它在匹配现有系统吞吐量的同时减少了网络中断。

5月6日星期三，上午9:00–10:20

### AVA：迈向基于视觉语言模型的视频分析（在新标签页中打开）

Yuxuan Yan，浙江大学；Shiqi Jiang，微软研究院；Ting Cao，清华大学；Yifan Yang，微软研究院；Qianqian Yang 和 Yuanchao Shu，浙江大学；Yuqing Yang 和 Lili Qiu，微软研究院

AVA通过将事件知识图谱与基于视觉语言模型的智能体检索相结合，支持开放式视频分析。此外，为了在超长、开放世界场景中评估视频分析，作者引入了AVA-100基准，包含8个各超过10小时的视频以及120个手动标注的多样化复杂问答对，AVA在该基准上达到了75.8%的准确率。

### 基于SmartNIC的Pyrocumulus存储优化虚拟机实时迁移（在新标签页中打开）

Jiechen Zhao，多伦多大学和微软亚洲研究院；Ran Shu, Lei Qu, Ziyue Yang, 和 Rui Ma，微软亚洲研究院；Derek Chiou，微软和德克萨斯大学奥斯汀分校；Natalie Enright Jerger，多伦多大学；Peng Cheng 和 Yongqiang Xiong，微软亚洲研究院

Pyrocumulus通过FPGA SmartNIC的硬件可定制性和高效网络可访问性，结合LM协议、架构和算法设计，实现了存储优化虚拟机的快速、低开销实时迁移。

5月6日星期三，上午10:50–下午12:30

### ForestColl：异构网络架构上的吞吐量最优集体通信（在新标签页中打开）

Liangyu Zhao，华盛顿大学；Saeed Maleki，独立研究员；Yuanhong Wang，清华大学；Zezhou Wang，华盛顿大学；Ziyue Yang，微软研究院；Hossein Pourreza，微软；Arvind Krishnamurthy，华盛顿大学

ForestColl构建广播/聚合生成树作为通信调度，实现了理论上的最优性。其调度生成在多项式时间内运行且高度可扩展。它支持任何网络架构，包括交换架构和直接加速器连接。

### 通过符号引导优化从源代码进行启发式分析（在新标签页中打开）

Pantea Karimi，麻省理工学院；Siva Kesava Reddy Kakarla 和 Ryan Beckett，微软研究院；Santiago Segarra，莱斯大学；Pooria Namyar，微软研究院；Mohammad Alizadeh，麻省理工学院；Behnaz Arzani，微软研究院

MetaEase直接从源代码分析启发式方法以揭示最坏情况性能场景，无需复杂的正式建模。它在多个领域匹配或超越最先进的分析器，并揭示了真实世界系统中此前未知的性能差距。

5月6日星期三，下午2:00–3:20

### 在容器系统中利用空闲CPU资源（在新标签页中打开）

Adam Hall 和 Anirudh Sarma，佐治亚理工学院；Esha Choukse，微软Azure研究院；Umakishore Ramachandran，佐治亚理工学院；Sameh Elnikety，微软研究院

HarvestContainers在保护延迟敏感型容器免受干扰的同时，利用其空闲CPU核心运行延迟容忍型工作负载。它动态确定可安全利用的核心数量，且无需更改应用程序或操作系统。它能够实现高达75%的空闲CPU利用率，同时将尾部延迟保持在独立性能的4%以内。

5月6日星期三，下午3:50–5:30

### 使用SONiC DASH SmartSwitch在生产规模上卸载云网络服务（在新标签页中打开）

社区奖得主

Shaofeng Wu，香港中文大学和微软亚洲研究院；Zhixiong Niu，微软亚洲研究院；Riff Jiang, Lawrence Lee, Junhua Zhai, Ze Gan, Vasundhara Volam, Prabhat Aravind, Prince Sunny, Prince George, Qi Luo, Evan Langlais, Soumya Tiwari, Venkat Satish Katta, Weixi Chen, Rishiraj Hazarika, Sachin Jain, Deven Jagasia, Michal Zygmunt, Avijit Gupta, Neeraj Motwani, 和 Pranjal Shrivastava，微软；Qiang Su，香港中文大学；Anil Reddy Pannala, Kristina Moore, James Grantham, Anupam Pandey, Xin Liu, Guohan Lu, Gerald De Grace, Rishabh Tewari, Lihua Yuan, Erica Lan, Deepak Bansal, 和 Dave Maltz，微软；Yongqiang Xiong，微软亚洲研究院；Hong Xu，香港中文大学

SONiC DASH SmartSwitch通过硬件友好型流水线、统一交换架构和开放开发模式重新设计了云网络卸载，同时解决了关键的可扩展性和部署挑战。在Azure中大规模部署后，它提供了高吞吐量和连接容量，同时显著提高了功率和空间效率。

### KRAKENGUARD：迈向细粒度eBPF隔离（在新标签页中打开）

Jainil Patel，印度理工学院罗orkee分校；Lucas Graeff Buhl-Nielsen，Quantco；Adrien Ghosn，微软；Marios Kogias，伦敦帝国学院

KRAKENGUARD 在加载时通过符号执行对 eBPF 程序实施基于策略的细粒度控制，从而无需依赖粗粒度的 Linux 能力即可在多租户环境中安全使用。它能防止恶意行为、检测漏洞，并允许在强隔离保障下安全执行不可信程序。

## 来自微软的研讨会组织者

### 项目委员会

Ganesh Ananthanarayanan  
Behnaz Arzani  
Hitesh Ballani  
Ryan Beckett  
Ranveer Chandra  
Paolo Costa  
Rodrigo Fonseca  
Xenofon Foukas  
Kevin Hsieh  
Umesh Krishnaswamy（在新标签页中打开）  
Jing Liu  
Jonathan Mace  
Dave Maltz  
Sathiya Mani  
Dushyanth Narayanan  
Suman Nath  
Ram Ramjee  
Stefan Saroiu

### 指导委员会

Sujata Banerjee  
Jay Lorch

## 认识作者

### Sujata Banerjee

合作伙伴研究经理

---

> 本文由AI自动翻译，原文链接：[Microsoft at NSDI 2026: Advances in large-scale networked systems - Microsoft Research](https://www.microsoft.com/en-us/research/blog/microsoft-at-nsdi-2026-advances-in-large-scale-networked-systems/)
> 
> 翻译时间：2026-05-06 05:27
