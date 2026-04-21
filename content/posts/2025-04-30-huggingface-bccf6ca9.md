---
title: Qwen-3对话模板揭示的四大模型设计新思路
title_original: The 4 Things Qwen-3’s Chat Template Teaches Us
date: '2025-04-30'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/qwen-3-chat-template-deep-dive
author: ''
summary: 本文通过分析Qwen-3对话模板的Jinja代码，揭示了其相较于前代模型的四项重要改进：1）通过enable_thinking标志实现推理步骤的可选性，而非强制思维链；2）采用动态上下文管理机制，智能保留或修剪推理块以维持相关性；3）展示了更精细的对话结构控制；4）体现了模型设计从固定范式向灵活配置的演进。这些变化反映了大型语言模型在实用性和可控性上的进步。
categories:
- AI研究
tags:
- Qwen-3
- 对话模板
- 大语言模型
- 推理优化
- 上下文管理
draft: false
translated_at: '2026-04-21T05:06:15.844945'
---

# Qwen-3 对话模板教给我们的 4 件事

一段枯燥的 Jinja 代码片段，揭示了新 Qwen-3 模型的哪些信息。

由Qwen发布的新 Qwen-3 模型，配备了一个比其前代 Qwen-2.5 和 QwQ 复杂得多的对话模板。通过查看 Jinja 模板的差异，我们可以发现关于新模型的有趣洞见。

## 对话模板

*   Qwen-3 对话模板
*   Qwen-2.5 对话模板
*   Qwen-QwQ 对话模板

## 什么是对话模板？

**对话模板**定义了用户与模型之间对话的结构和格式化方式。该模板充当翻译器，将人类可读的对话：

```js
  [
    { role: "user", content: "Hi there!" },
    { role: "assistant", content: "Hi there, how can I help you today?" },
    { role: "user", content: "I'm looking for a new pair of shoes." },
  ]

```

转换为模型友好的格式：

```xml
<|im_start|>user
Hi there!<|im_end|>
<|im_start|>assistant
Hi there, how can I help you today?<|im_end|>
<|im_start|>user
I'm looking for a new pair of shoes.<|im_end|>
<|im_start|>assistant
<think>

</think>

```

你可以在 Hugging Face 模型页面上轻松查看给定模型的对话模板。

![](/images/posts/91df4f0bdde8.png)

Qwen/Qwen3-235B-A22B 的对话模板

让我们深入探究 Qwen-3 的对话模板，看看我们能学到什么！

## 1. 推理无需强制，可通过简单的预填充使其成为可选项

Qwen-3 的独特之处在于能够通过 `enable_thinking` 标志来切换推理。当设置为 `false` 时，模板会插入一个空的 `<think></think>` 对，告诉模型跳过逐步思考。早期的模型将 `<think>` 标签硬编码到每次生成中，无论你是否需要，都强制进行思维链推理。

```jinja

{%- if enable_thinking is defined and enable_thinking is false %}
    {{- '<think>\n\n</think>\n\n' }}
{%- endif %}

```

例如，QwQ 就在每次对话中强制进行推理。

```jinja

{%- if add_generation_prompt %}
    {{- '<|im_start|>assistant\n<think>\n' }}
{%- endif %}

```

如果 `enable_thinking` 为 `true`，模型可以自行决定是否进行思考。

你可以使用以下代码测试该模板：

```js
import { Template } from "@huggingface/jinja";
import { downloadFile } from "@huggingface/hub";

const HF_TOKEN = process.env.HF_TOKEN;

const file = await downloadFile({
  repo: "Qwen/Qwen3-235B-A22B",
  path: "tokenizer_config.json",
  accessToken: HF_TOKEN,
});
const config = await file!.json();

const template = new Template(config.chat_template);
const result = template.render({
  messages,
  add_generation_prompt: true,
  enable_thinking: false,  
  bos_token: config.bos_token,
  eos_token: config.eos_token,
});

```

## 2. 上下文管理应是动态的

Qwen-3 采用了滚动检查点系统，智能地保留或修剪推理块以维持相关上下文。旧模型为了节省 Token 而过早地丢弃了推理内容。

Qwen-3 通过反向遍历消息列表来找到最近一次非工具调用的用户回合，从而引入了“滚动检查点”。对于该索引之后的所有助手回复，它会保留完整的 `<think>` 块；而该索引之前的所有内容则会被剥离。

这为何重要：

*   在多步骤工具调用期间保持活动计划可见。
*   支持嵌套工具工作流而不丢失上下文。
*   通过修剪模型不再需要的思考内容来节省 Token。
*   防止“陈旧”的推理内容渗入新任务。

### 示例

这是一个通过 Qwen-3 和 QwQ 进行工具调用时思维链保留的示例。

![image/png](/images/posts/2febf41aad9a.png)

查看 `@huggingface/jinja` 以测试对话模板

## 3. 工具参数需要更好的序列化

以前，每个 `tool_call.arguments` 字段都会通过 `| tojson` 处理，即使它已经是 JSON 编码的字符串——这可能导致双重转义的风险。Qwen-3 会先检查类型，只在必要时进行序列化。

```jinja

{%- if tool_call.arguments is string %}
    {{- tool_call.arguments }}
{%- else %}
    {{- tool_call.arguments | tojson }}
{%- endif %}

```

## 4. 无需默认系统提示词

与许多模型一样，Qwen-2.5 系列有一个默认的系统提示词。

> 你是由阿里云创建的 Qwen。你是一个乐于助人的助手。

这很常见，因为它有助于模型回答诸如“你是谁？”这样的用户问题。

Qwen-3 和 QwQ 发布时没有这个默认的系统提示词。尽管如此，如果你询问，模型仍然可以准确地识别其创建者。

## 结论

Qwen-3 向我们展示，通过 **对话模板**，我们可以提供更好的灵活性、更智能的上下文处理和更优的工具交互。这些改进不仅提升了能力，还使 Agent（智能体）工作流更加可靠和高效。

---

> 本文由AI自动翻译，原文链接：[The 4 Things Qwen-3’s Chat Template Teaches Us](https://huggingface.co/blog/qwen-3-chat-template-deep-dive)
> 
> 翻译时间：2026-04-21 05:06
