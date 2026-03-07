---
title: Consilium：多LLM协同决策平台
title_original: 'Consilium: When Multiple LLMs Collaborate'
date: '2025-07-17'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/consilium-multi-llm
author: ''
summary: 本文介绍了作者在Gradio Agents & MCP Hackathon期间开发的多LLM协作平台Consilium。该平台通过让多个大型语言模型扮演不同专家角色，围绕复杂问题进行结构化辩论并达成共识，以提升决策质量。文章阐述了从概念构思到架构设计的全过程，包括创建可视化扑克圆桌会议界面、实现会话状态管理，以及为LLM分配角色以促进有意义的讨论。平台既可作为Gradio交互演示，也可作为MCP服务器集成到其他应用中，展示了多AI视角协作优于个体分析的潜力。
categories:
- AI产品
tags:
- 多智能体协作
- LLM应用
- Gradio
- MCP协议
- 决策系统
draft: false
translated_at: '2026-03-07T04:31:44.331241'
---

# Consilium：当多个LLM协同合作时

想象一下：四位AI专家围坐在扑克桌旁，实时讨论你最棘手的决策。这正是我在Gradio Agents & MCP Hackathon期间构建的多LLM平台——Consilium——所做的事情。它让AI模型通过结构化辩论来讨论复杂问题并达成共识。

该平台既可作为可视化的Gradio界面，也可作为MCP（模型上下文协议）服务器，直接与Cline等应用程序集成（Claude Desktop因超时设置无法调整而存在问题）。核心理念始终是让LLM通过讨论达成共识；这也是Consilium这个名字的由来。后来，又添加了多数投票和排序选择等其他决策模式，使协作更加精细。

## 从概念到架构

这并非我最初的黑客松想法。我最初想构建一个简单的MCP服务器来与我在RevenueCat中的项目对话。但当我意识到，一个让这些模型讨论问题并返回经过充分推理的答案的多LLM平台会更具吸引力时，我重新进行了考虑。

时机恰到好处。黑客松结束后不久，微软发布了他们的AI诊断协调器（MAI-DxO），本质上是一个具有不同角色（如"Dr. Challenger Agent"）的AI医生小组，用于迭代诊断患者。在他们使用OpenAI o3的设置中，他们正确解决了85.5%的医疗诊断基准案例，而执业医师的准确率仅为20%。这正好验证了Consilium所展示的：多个AI视角协作可以显著优于个体分析。

确定概念后，我需要一个既能作为MCP服务器，又能作为引人入胜的Hugging Face空间演示的东西。最初我考虑使用标准的Gradio聊天组件，但我希望我的提交作品能脱颖而出。想法是让LLM围坐在会议室桌旁，配有对话气泡，这既能捕捉协作讨论，又能使其在视觉上引人入胜。由于我未能很好地设计一个标准的表格使其真正被识别为桌子，我选择了扑克风格的圆桌会议。这种方法还让我可以通过构建自定义Gradio组件和MCP服务器来提交到两个黑客松赛道。

## 构建视觉基础

自定义的Gradio组件成为了提交作品的核心；这个扑克风格的圆桌会议，参与者围坐并显示展示其回应、思考状态和研究活动的对话气泡，立即吸引了任何访问该空间的人的注意。得益于Gradio出色的开发者体验，组件开发异常顺利，尽管我确实遇到了一个关于PyPI发布的文档空白，这促成了我对Gradio项目的首次贡献。

```python

roundtable = consilium_roundtable(
    label="AI Expert Roundtable",
    label_icon="https://huggingface.co/front/assets/huggingface_logo-noborder.svg",
    value=json.dumps({
        "participants": [],
        "messages": [],
        "currentSpeaker": None,
        "thinking": [],
        "showBubbles": [],
        "avatarImages": avatar_images
    })
)

```

事实证明，视觉设计在整个黑客松期间都非常稳健；在初始实现之后，只添加了用户自定义头像和中心桌文本等功能，而核心交互模型保持不变。

如果你有兴趣创建自己的自定义Gradio组件，你应该看看《5分钟创建自定义组件》，是的，标题没有说谎；基本设置确实只需要5分钟。

## 会话状态管理

视觉圆桌会议通过基于会话的字典系统维护状态，其中每个用户通过`user_sessions[session_id]`获得隔离的状态存储。核心状态对象跟踪`participants`、`messages`、`currentSpeaker`、`thinking`和`showBubbles`数组，这些数组通过`update_visual_state()`回调进行更新。当模型正在思考、发言或执行研究时，引擎通过向消息数组追加内容和切换发言者/思考状态，将增量状态更新推送到前端，从而创建实时视觉流，无需复杂的状态机——只需在后端处理和前端渲染之间同步直接的JSON状态变更。

## 让LLM真正讨论起来

在实现过程中，我意识到LLM之间并没有发生真正的讨论，因为它们缺乏明确的角色。它们接收了正在进行的讨论的完整上下文，但不知道如何进行有意义的参与。我引入了不同的角色来创造富有成效的辩论动态，经过几次调整后，最终如下所示：

```python
self.roles = {
    'standard': "提供具有清晰推理和证据的专家分析。",
    'expert_advocate': "你是一位充满热情的专家，倡导你的专业立场。以坚定的信念提出令人信服的证据。",
    'critical_analyst': "你是一位严谨的批评者。以分析精度识别论点中的缺陷、风险和弱点。",
    'strategic_advisor': "你是一位战略顾问。专注于实际实施、现实世界约束和可操作的见解。",
    'research_specialist': "你是一位具有深厚领域知识的研究专家。提供权威的分析和基于证据的见解。",
    'innovation_catalyst': "你是一位创新专家。挑战传统思维并提出突破性方法。"
}

```

这解决了讨论问题，但引发了一个新问题：如何确定共识或识别最强的论点？我实现了一个首席分析师系统，用户可以选择一个LLM来综合最终结果并评估是否达成共识。

我还希望用户能控制通信结构。除了默认的完整上下文共享之外，我添加了两种替代模式：

- 环形：每个LLM只接收前一个参与者的回应
- 星形：所有消息都通过首席分析师作为中央协调器流动

最后，讨论需要终点。我实现了可配置的轮次（1-5轮），测试表明更多轮次会增加达成共识的可能性（尽管计算成本更高）。

## LLM选择与研究集成

当前的模型选择包括Mistral Large、DeepSeek-R1、Meta-Llama-3.3-70B和QwQ-32B。虽然缺少像Claude Sonnet和OpenAI的o3这样著名的模型，但这反映了黑客松积分可用性和赞助商奖项考虑，而非技术限制。

```python
self.models = {
    'mistral': {
        'name': 'Mistral Large',
        'api_key': mistral_key,
        'available': bool(mistral_key)
    },
    'sambanova_deepseek': {
        'name': 'DeepSeek-R1',
        'api_key': sambanova_key,
        'available': bool(sambanova_key)
    }
    ...
}

```

对于支持函数调用的模型，我集成了一个专门的研究Agent，它作为另一个圆桌会议参与者出现。这种方法不是直接给模型网络访问权限，而是清晰地展示了外部资源的可用性，并确保所有支持函数调用的模型都能获得一致的访问。

```python
def handle_function_calls(self, completion, original_prompt: str, calling_model: str) -> str:
    """统一函数调用处理器，具备增强的研究能力"""
    
    message = completion.choices[0].message
    
    
    if not hasattr(message, 'tool_calls') or not message.tool_calls:
        return message.content
    
    
    for tool_call in message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        
        result = self._execute_research_function(function_name, arguments, calling_model_name)

```

该研究Agent（智能体）可访问五个来源：网络搜索、维基百科、arXiv、GitHub和美国证券交易委员会EDGAR数据库。我将这些工具构建在可扩展的基类架构上，以便未来扩展，同时重点关注可自由嵌入的资源。

```python
class BaseTool(ABC):
    """所有研究工具的基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.last_request_time = 0
        self.rate_limit_delay = 1.0
    
    @abstractmethod
    def search(self, query: str, **kwargs) -> str:
        """主要搜索方法 - 由子类实现"""
        pass
    
    def score_research_quality(self, research_result: str, source: str = "web") -> Dict[str, float]:
        """根据时效性、权威性、特异性、相关性评估研究质量"""
        quality_score = {
            "recency": self._check_recency(research_result),
            "authority": self._check_authority(research_result, source),
            "specificity": self._check_specificity(research_result),
            "relevance": self._check_relevance(research_result)
        }
        return quality_score

```

由于研究操作可能耗时较长，对话气泡会显示进度指示器和时间预估，以在较长时间的研究任务中保持用户参与度。

## 发现Open Floor协议

黑客马拉松结束后，Deborah Dahl向我介绍了Open Floor协议，该协议与圆桌讨论方法完美契合。该协议为跨平台Agent（智能体）通信提供了标准化的JSON消息格式。它与其他Agent（智能体）间协议的关键区别在于：所有Agent（智能体）始终保持持续的对话感知，就像围坐在同一张桌子旁。另一个我在其他协议中未见过的特点是：主持人可以动态邀请或移除参与讨论的Agent（智能体）。

该协议的交互模式直接映射到Consilium的架构：

- 委托：在Agent（智能体）间转移控制权
- 通道传递：不经修改地传递消息
- 协调：在幕后进行协调
- 编排：多个Agent（智能体）协同合作

我正在集成Open Floor协议支持，以允许用户将任何符合OFP标准的Agent（智能体）添加到他们的圆桌讨论中。您可以通过以下链接关注开发进展：https://huggingface.co/spaces/azettl/consilium_ofp

## 经验总结与未来展望

这次黑客马拉松让我接触到了之前未曾了解的多Agent（智能体）辩论研究，包括《通过多Agent（智能体）辩论鼓励大语言模型发散思维》这样的基础性研究。社区体验非常出色；所有参与者都通过Discord的反馈和协作积极相互支持。看到我的圆桌组件被集成到另一个黑客马拉松项目中，是我在Consilium开发过程中的亮点之一。

我将继续完善Consilium，通过扩展模型选择、集成Open Floor协议以及可配置的Agent（智能体）角色，该平台几乎可以支持任何能想象到的多Agent（智能体）辩论场景。

构建Consilium的经历强化了我的信念：AI的未来不仅在于更强大的单个模型，更在于能够实现有效AI协作的系统。随着专业化的小型语言模型变得更高效、更节省资源，我相信对于许多用例而言，由特定任务型SLM与专用研究Agent（智能体）组成的圆桌讨论，可能会成为通用大语言模型的有力替代方案。

---

> 本文由AI自动翻译，原文链接：[Consilium: When Multiple LLMs Collaborate](https://huggingface.co/blog/consilium-multi-llm)
> 
> 翻译时间：2026-03-07 04:31
