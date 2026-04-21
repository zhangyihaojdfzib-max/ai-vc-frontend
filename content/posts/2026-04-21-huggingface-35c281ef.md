---
title: 如何利用合成人物画像让韩国AI智能体扎根真实人口数据
title_original: How to Ground a Korean AI Agent in Real Demographics with Synthetic
  Personas
date: '2026-04-21'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/nvidia/build-korean-agents-with-nemotron-personas
author: ''
summary: 本文介绍了Nemotron-Personas-Korea数据集如何解决AI智能体因训练数据缺乏韩国文化背景而导致的本地化失效问题。该数据集基于韩国官方统计数据，生成了600万个合成虚拟人物画像，严格遵守隐私法规，为AI智能体提供了准确的人口统计学背景、语言规范和文化认知。文章通过一个构建韩国公共卫生智能体的教程，展示了如何筛选数据集、定义智能体行为并将其部署，使智能体能够理解并适应韩国的社会结构、职业模式和敬语体系，从而提升在真实场景中的表现力和可靠性。
categories:
- AI产品
tags:
- 合成数据
- AI本地化
- 韩国AI
- 人口数据
- 智能体开发
draft: false
translated_at: '2026-04-21T05:04:44.394451'
---

# 如何通过合成人物画像让韩国AI智能体扎根真实人口数据

如今驱动大多数AI智能体的模型主要基于英文网络数据进行训练。它们缺失了韩语的敬语结构、地域性职业模式以及韩国用户所期待的文化背景。一个将美国医疗工作流程应用于韩国公共卫生系统的智能体，远未达到可投入生产的水平。

Nemotron-Personas-Korea解决了这个问题。该数据集提供了600万个完全合成的虚拟人物画像，其数据基础来源于韩国统计信息服务、韩国最高法院、国民健康保险公团以及韩国农村经济研究院的官方统计数据和种子数据。NAVER Cloud在设计阶段贡献了种子数据和领域专业知识。

每个人物画像在人口统计学上都是准确的，但不包含任何个人可识别信息。其设计充分考虑了韩国的《个人信息保护法》。韩国也是少数几个发布了官方合成数据生成指南的国家之一，为使用敏感数据的合成版本来构建模型建立了治理框架。本数据集遵循了这一方法。

在本教程中，我们将使用托管API，在大约20分钟内，将一个合成人物画像转变为一个已部署的韩国智能体——从筛选数据集到进行推理。

## 面向韩国的自主数据集

![Screenshot 2026-04-20 at 5.16.08 PM](/images/posts/93c2ec84caa2.png)

Nemotron-Personas-Korea是使用NeMo Data Designer生成的，这是NVIDIA用于合成数据的开源复合AI系统。该流程将用于统计基础的**概率图模型**与用于韩语叙事生成的**Gemma-4-31B**模型配对。人口数据来自KOSIS；姓名分布数据来自韩国最高法院。

![title_diagram](/images/posts/a507044c0c43.png)

Nemotron-Personas-Korea是Nemotron-Personas系列的最新成员，该系列还覆盖了美国、日本、印度、新加坡、巴西和法国。如果您正在构建一个为韩国用户及其他市场服务的多语言智能体，您可以在同一流程中混合使用不同国家的人物画像。

## 这对自主智能体为何重要

如今大多数智能体是“身份盲”的。它们遵循指令，但对其服务对象没有任何背景认知。例如，一个使用美国预约惯例来预订韩国医院就诊的智能体，或者用“반말”称呼60岁患者的智能体，不仅感觉不对，而且会失败。

Nemotron-Personas-Korea通过为您的智能体提供韩国运营背景来改变这一现状。将一个人物画像加载到系统提示词中，智能体就会继承该人物的地区、职业、沟通规范和领域专业知识。

这适用于任何智能体框架。您可以使用NemoClaw进行部署，通过NVIDIA NIM进行生产推理，或直接调用NVIDIA API。人物画像层与框架无关，它充当一个结构良好、基于真实韩国人口数据的系统提示词。

## 教程：从合成人物画像到自主智能体

🔗 资源

- Nemotron-Personas-Korea用于训练数据生成
- NeMo Data Designer用于合成特定领域数据
- NVIDIA NemoClaw用于部署常驻智能体
- NVIDIA Developer Discord获取社区支持

### 步骤 1：加载并探索数据集

加载数据集并探索其内容。每条记录都包含结构化的人口统计字段以及丰富的、自然语言描述的人物画像叙事。

```python
from datasets import load_dataset


dataset = load_dataset("nvidia/Nemotron-Personas-Korea")


print(dataset["train"].column_names)


print(dataset["train"][0])

```

### 步骤 2：筛选并选择人物画像

通过职业、地区、年龄或任何字段组合来筛选数据集，以找到与您的目标领域匹配的人物画像。这里我们将构建一个韩国公共卫生智能体。

```python


health_personas = dataset["train"].filter(
    lambda x: "보건" in x["occupation"] or "간호" in x["occupation"] or "의료" in x["occupation"]
)

print(f"Found {len(health_personas)} health personas")


persona = health_personas[0]
print(persona)

```

您可以根据地区、教育水平或人生阶段进一步细化筛选。数据集足够大，可以找到高度特定的子集。

### 步骤 3：定义您的智能体行为

这是将人物画像数据转化为智能体行为的地方。结构化字段——姓名、地区、职业、技能——成为智能体的身份。您在此基础上叠加行为指令和任务范围。结果是一个能够像特定角色和地区的韩国专业人士一样进行推理的智能体。

```python






system_prompt = f"""당신은 한국의 공중보건 상담 AI 에이전트입니다.

[신원]                              # Identity
- 이름: {persona['name']}           # Name
- 지역: {persona['region']}         # Region
- 직업: {persona['occupation']}     # Occupation
- 전문분야: {persona['skills']}      # Specialization

[행동 지침]                           # Behavior guidelines
- 한국어 존댓말을 사용하여 응답하세요.      # Use formal Korean
- 지역 보건소 및 공공 의료 체계에 대한 안내를 제공하세요.  # Guide on local clinics
- 한국 공중보건 정책과 절차를 기반으로 정확한 정보를 제공하세요.  # Follow KR health policy
- 문화적 맥락을 고려하여 상담하세요.        # Consider cultural context

[업무 범위]                           # Task scope
- 예방접종 일정 안내                    # Vaccination scheduling
- 건강검진 절차 설명                    # Health screening procedures
- 지역 보건 자원 연결                   # Connect to local health resources
- 공중보건 관련 일반 상담                # General public health consultation

"""

```

### 步骤 4：部署您的智能体

将您基于人物画像的提示词连接到模型进行推理。根据您的设置，有三种选择：

- NVIDIA API目录——最快的测试方式
- NVIDIA NIM——用于生产部署的自托管推理
- NemoClaw——部署常驻智能体的参考堆栈，可在任何地方运行，包括通过DGX Spark在RTX PC上运行

```python
from openai import OpenAI


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="nvapi-YOUR_KEY"  
)

response = client.chat.completions.create(
    model="nvidia/nemotron-nano-8b-v1",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "독감 예방접종은 언제 맞아야 하나요?"}  
    ],
    temperature=0.7,
    max_tokens=512
)

print(response.choices[0].message.content)

```

相同的工作流程适用于任何领域。更换人物画像筛选器和任务范围，您就得到了一个新的智能体：一个“금융”人物画像成为零售银行顾问，一个“교육”人物画像成为辅导助手，一个“공무원”人物画像成为政府卫生服务智能体。

## 数据基础带来的改变

以下是同一个问题——“독감 예방접종은 언제 맞아야 하나요?”——在使用和不使用人物画像基础的情况下得到的回答对比。

人物画像超越了翻译——它提供了情境化信息，从而产生一个用户会信任的智能体。

## 加入我们在首尔的构建之旅

NVIDIA Nemotron开发者日于2026年4月21日至22日（今明两天）来到首尔——这是该活动首次在GTC之外举行。为期两天的活动，包括关于自主AI和开源模型的技术讲座，以及一个动手实践的黑客松，您将有机会使用Nemotron-Personas-Korea来构建特定领域的韩国智能体和“claw”。🦞

亲临现场或通过直播加入我们。分享您的构建成果，将有机会在未来的NVIDIA教程中被展示。

---

> 本文由AI自动翻译，原文链接：[How to Ground a Korean AI Agent in Real Demographics with Synthetic Personas](https://huggingface.co/blog/nvidia/build-korean-agents-with-nemotron-personas)
> 
> 翻译时间：2026-04-21 05:04
