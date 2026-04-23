---
title: Tiny Agents：50行代码构建MCP驱动的智能体
title_original: 'Tiny Agents: an MCP-powered agent in 50 lines of code'
date: '2025-04-25'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/tiny-agents
author: ''
summary: 本文介绍了如何利用MCP（模型上下文协议）这一标准化API，仅用50行TypeScript代码构建一个功能完整的AI智能体。文章阐述了MCP的核心价值在于为LLM提供可连接的工具集，并展示了如何通过一个简单的while循环将MCP客户端转化为智能体。作者以实际演示为例，说明智能体如何调用文件系统和浏览器工具完成任务，并指出现代LLM原生支持工具调用是实现此简洁方案的关键。
categories:
- AI基础设施
tags:
- MCP
- 智能体
- 大语言模型
- 工具调用
- TypeScript
draft: false
translated_at: '2026-04-23T05:00:55.243334'
---

# Tiny Agents：一个仅用50行代码实现的MCP驱动智能体

**最新消息！**（2025年5月23日）如果您更喜欢Python，请查看配套文章《Python版Tiny Agents》。

在过去的几周里，我一直在深入研究MCP（模型上下文协议），以了解它为何如此备受关注。

我的简短总结是：它相当简单，但仍然非常强大：**MCP是一个用于暴露一组可连接到LLM（大语言模型）的工具的标准API**。

扩展一个推理客户端以同时充当MCP客户端，并将MCP服务器上的可用工具连接到LLM推理中，是相当简单的——在HF，我们有两个官方的客户端SDK：JS版的`@huggingface/inference`和Python版的`huggingface_hub`。

但在这样做的过程中，我有了第二个认识：

**一旦你有了一个MCP客户端，一个Agent（智能体）实际上就只是在它上面加一个while循环。**

在这篇短文中，我将引导您了解我是如何在Typescript（JS）中实现它的，您如何也能采用MCP，以及它将如何使未来的Agentic AI变得更加简单。

## 如何运行完整演示

如果您有NodeJS（带有`pnpm`或`npm`），只需在终端中运行：

```bash
npx @huggingface/mcp-client
```

或者如果使用`pnpm`：

```bash
pnpx @huggingface/mcp-client
```

这会将我的包安装到一个临时文件夹中，然后执行其命令。

您将看到您的简单Agent连接到两个不同的MCP服务器（在本地运行），加载它们的工具，然后提示您进行对话。

默认情况下，我们的示例Agent连接到以下两个MCP服务器：

*   "标准"的文件系统服务器，它可以访问您的桌面。
*   以及`Playwright MCP`服务器，它知道如何为您使用沙盒化的Chromium浏览器。

**注意：** 这有点反直觉，但目前所有的MCP服务器实际上都是本地进程（尽管远程服务器即将推出）。

我们第一个视频的输入是：

> 写一首关于Hugging Face社区的俳句，并将其写入我桌面上的一个名为"hf.txt"的文件中

现在让我们尝试这个涉及一些网页浏览的提示词：

> 在Brave Search上搜索HF推理服务提供商，并打开前3个结果

### 默认模型和提供商

在模型/提供商配对方面，我们的示例Agent默认使用：

*   "Qwen/Qwen2.5-72B-Instruct"
*   运行在`Nebius`上

这一切都可以通过环境变量进行配置！参见：

```ts
const agent = new Agent({
    provider: process.env.PROVIDER ?? "nebius",
    model: process.env.MODEL_ID ?? "Qwen/Qwen2.5-72B-Instruct",
    apiKey: process.env.HF_TOKEN,
    servers: SERVERS,
});
```

## 代码在哪里

Tiny Agent的代码位于`huggingface.js`单体仓库的`mcp-client`子包中，该仓库是我们所有JS库所在的GitHub单体仓库。

https://github.com/huggingface/huggingface.js/tree/main/packages/mcp-client

代码库使用了现代JS特性（特别是异步生成器），这使得实现变得容易得多，尤其是像LLM响应这样的异步事件。
如果您还不熟悉这些JS特性，可能需要向LLM请教一下。

## 这一切的基础：LLM中原生的工具调用支持。

让这篇博文变得非常容易的是，最近一批LLM（无论是闭源还是开源）都经过了函数调用（即工具使用）的训练。

一个工具由其名称、描述和其参数的JSONSchema表示来定义。
从某种意义上说，它是任何函数接口的不透明表示，从外部看（意味着LLM不关心函数实际是如何实现的）。

```ts
const weatherTool = {
    type: "function",
    function: {
        name: "get_weather",
        description: "Get current temperature for a given location.",
        parameters: {
            type: "object",
            properties: {
                location: {
                    type: "string",
                    description: "City and country e.g. Bogotá, Colombia",
                },
            },
        },
    },
};
```

我将在此链接的规范文档是`OpenAI的函数调用文档`。（是的……OpenAI几乎为整个社区定义了LLM标准 😅）。

推理引擎允许您在调用LLM时传递一个工具列表，LLM可以自由地调用零个、一个或多个这些工具。
作为开发者，您运行这些工具并将其结果反馈给LLM以继续生成。

请注意，在后端（在推理引擎层面），工具只是以一种特殊格式的`chat_template`传递给模型，就像任何其他消息一样，然后从响应中解析出来（使用模型特定的特殊Token）以将它们暴露为工具调用。请参阅`我们的聊天模板游乐场`中的示例。

## 在InferenceClient之上实现MCP客户端

既然我们知道了在最近的LLM中工具是什么，现在让我们来实现实际的MCP客户端。

官方文档`https://modelcontextprotocol.io/quickstart/client`写得相当好。您只需要将任何对Anthropic客户端SDK的引用替换为任何其他OpenAI兼容的客户端SDK即可。（还有`allms.txt`，您可以将其输入到您选择的LLM中，以帮助您编写代码）。

提醒一下，我们使用HF的`InferenceClient`作为我们的推理客户端。

完整的`McpClient.ts`代码文件在`这里`，如果您想跟着实际代码一起看的话 🤓

我们的`McpClient`类包含：

*   一个推理客户端（适用于任何推理提供商，`huggingface/inference`支持远程和本地端点）
*   一组MCP客户端会话，每个连接的MCP服务器一个（是的，我们希望支持多个服务器）
*   以及一个可用工具列表，该列表将从连接的服务器中填充并稍作重新格式化。

```ts
export class McpClient {
    protected client: InferenceClient;
    protected provider: string;
    protected model: string;
    private clients: Map<ToolName, Client> = new Map();
    public readonly availableTools: ChatCompletionInputTool[] = [];

    constructor({ provider, model, apiKey }: { provider: InferenceProvider; model: string; apiKey: string }) {
        this.client = new InferenceClient(apiKey);
        this.provider = provider;
        this.model = model;
    }
    
    
}
```

要连接到MCP服务器，官方的`@modelcontextprotocol/sdk/client` TypeScript SDK提供了一个带有`listTools()`方法的`Client`类：

```ts
async addMcpServer(server: StdioServerParameters): Promise<void> {
    const transport = new StdioClientTransport({
        ...server,
        env: { ...server.env, PATH: process.env.PATH ?? "" },
    });
    const mcp = new Client({ name: "@huggingface/mcp-client", version: packageVersion });
    await mcp.connect(transport);

    const toolsResult = await mcp.listTools();
    debug(
        "Connected to server with tools:",
        toolsResult.tools.map(({ name }) => name)
    );

    for (const tool of toolsResult.tools) {
        this.clients.set(tool.name, mcp);
    }

    this.availableTools.push(
        ...toolsResult.tools.map((tool) => {
            return {
                type: "function",
                function: {
                    name: tool.name,
                    description: tool.description,
                    parameters: tool.inputSchema,
                },
            } satisfies ChatCompletionInputTool;
        })
    );
}
```

`StdioServerParameters`是MCP SDK中的一个接口，可以让您轻松生成一个本地进程：正如我们之前提到的，目前所有的MCP服务器实际上都是本地进程。

对于我们连接的每个MCP服务器，我们都会稍微重新格式化其工具列表，并将它们添加到`this.availableTools`中。

### 如何使用这些工具

很简单，您只需将`this.availableTools`传递给您的LLM聊天完成调用，除了您通常的消息数组之外：

```ts
const stream = this.client.chatCompletionStream({
    provider: this.provider,
    model: this.model,
    messages,
    tools: this.availableTools,
    tool_choice: "auto",
});
```

`tool_choice: "auto"`是您传递的参数，用于让LLM生成零个、一个或多个工具调用。

在解析或流式处理输出时，LLM（大语言模型）会生成一些工具调用（即一个函数名和一些JSON编码的参数），这需要您（作为开发者）进行计算。MCP客户端SDK再次让这变得非常简单；它有一个`client.callTool()`方法：

```ts
const toolName = toolCall.function.name;
const toolArgs = JSON.parse(toolCall.function.arguments);

const toolMessage: ChatCompletionInputMessageTool = {
    role: "tool",
    tool_call_id: toolCall.id,
    content: "",
    name: toolName,
};


const client = this.clients.get(toolName);
if (client) {
    const result = await client.callTool({ name: toolName, arguments: toolArgs });
    toolMessage.content = result.content[0].text;
} else {
    toolMessage.content = `Error: No session found for tool: ${toolName}`;
}

```

最后，您需要将得到的工具消息添加到您的`messages`数组中，并传回给LLM。

## 我们仅用50行代码实现的Agent（智能体）🤯

既然我们有了一个能够连接到任意MCP服务器以获取工具列表、并能向LLM推理注入和解析这些工具的MCP客户端，那么……什么是Agent（智能体）呢？

一旦您拥有一个配备了工具集的推理客户端，那么Agent（智能体）就只是在它之上运行的一个while循环。

更详细地说，一个Agent（智能体）简单来说就是以下几部分的组合：

- 一个系统提示词
- 一个LLM推理客户端
- 一个MCP客户端，用于从一堆MCP服务器中挂载一组工具
- 一些基本的控制流（见下面的while循环）

完整的`Agent.ts`代码文件在[这里](https://github.com/your-repo/Agent.ts)。

我们的Agent类简单地继承了`McpClient`：

```ts
export class Agent extends McpClient {
    private readonly servers: StdioServerParameters[];
    protected messages: ChatCompletionInputMessage[];

    constructor({
        provider,
        model,
        apiKey,
        servers,
        prompt,
    }: {
        provider: InferenceProvider;
        model: string;
        apiKey: string;
        servers: StdioServerParameters[];
        prompt?: string;
    }) {
        super({ provider, model, apiKey });
        this.servers = servers;
        this.messages = [
            {
                role: "system",
                content: prompt ?? DEFAULT_SYSTEM_PROMPT,
            },
        ];
    }
}

```

默认情况下，我们使用一个非常简单的系统提示词，灵感来源于[GPT-4.1提示指南](https://platform.openai.com/docs/guides/prompting)中分享的内容。

尽管这来自OpenAI 😈，但下面这句话尤其适用于越来越多的模型，无论是闭源还是开源的：

> 我们鼓励开发者专门使用`tools`字段来传递工具，而不是手动将工具描述注入到您的提示词中，并为工具调用编写单独的解析器，正如过去一些人所报告的那样。

也就是说，我们不需要在提示词中提供精心格式化的工具使用示例列表。`tools: this.availableTools`参数就足够了。

在Agent上加载工具实际上就是连接到我们想要的MCP服务器（并行连接，因为在JS中这样做很容易）：

```ts
async loadTools(): Promise<void> {
    await Promise.all(this.servers.map((s) => this.addMcpServer(s)));
}

```

我们添加了两个额外的工具（在MCP之外），可供LLM用于我们Agent的控制流：

```ts
const taskCompletionTool: ChatCompletionInputTool = {
    type: "function",
    function: {
        name: "task_complete",
        description: "当用户给定的任务完成时调用此工具",
        parameters: {
            type: "object",
            properties: {},
        },
    },
};
const askQuestionTool: ChatCompletionInputTool = {
    type: "function",
    function: {
        name: "ask_question",
        description: "向用户提问，以获取解决问题或澄清问题所需的更多信息。",
        parameters: {
            type: "object",
            properties: {},
        },
    },
};
const exitLoopTools = [taskCompletionTool, askQuestionTool];

```

当调用这些工具中的任何一个时，Agent将中断其循环，并将控制权交还给用户以获取新的输入。

### 完整的while循环

请看我们完整的while循环。🎉

我们Agent主while循环的核心是，我们简单地与LLM进行迭代，在工具调用和向其提供工具结果之间交替进行，并且我们一直这样做，直到LLM开始连续响应两个非工具消息。

这是完整的while循环：

```ts
let numOfTurns = 0;
let nextTurnShouldCallTools = true;
while (true) {
    try {
        yield* this.processSingleTurnWithTools(this.messages, {
            exitLoopTools,
            exitIfFirstChunkNoTool: numOfTurns > 0 && nextTurnShouldCallTools,
            abortSignal: opts.abortSignal,
        });
    } catch (err) {
        if (err instanceof Error && err.message === "AbortError") {
            return;
        }
        throw err;
    }
    numOfTurns++;
    const currentLast = this.messages.at(-1)!;
    if (
        currentLast.role === "tool" &&
        currentLast.name &&
        exitLoopTools.map((t) => t.function.name).includes(currentLast.name)
    ) {
        return;
    }
    if (currentLast.role !== "tool" && numOfTurns > MAX_NUM_TURNS) {
        return;
    }
    if (currentLast.role !== "tool" && nextTurnShouldCallTools) {
        return;
    }
    if (currentLast.role === "tool") {
        nextTurnShouldCallTools = false;
    } else {
        nextTurnShouldCallTools = true;
    }
}

```

## 后续步骤

一旦您拥有了一个运行中的MCP客户端和一种构建Agent（智能体）的简单方法，就有许多很酷的潜在后续步骤可以探索 🔥

- 尝试**其他模型**：
    - `mistralai/Mistral-Small-3.1-24B-Instruct-2503` 针对函数调用进行了优化
    - `Gemma 3 27B`、`Gemma 3 QAT` 模型是函数调用的热门选择，不过它需要我们实现工具解析，因为它不使用原生的`tools`字段（欢迎提交PR！）
- 尝试所有**推理服务提供商**：Cerebras、Cohere、Fal、Fireworks、Hyperbolic、Nebius、Novita、Replicate、SambaNova、Together等。它们各自对函数调用有不同的优化（也取决于模型），因此性能可能有所不同！
- 使用 llama.cpp 或 LM Studio 连接**本地LLM**

欢迎提交拉取请求和贡献！
再次强调，这里的一切都是**开源**的！💎❤️

---

> 本文由AI自动翻译，原文链接：[Tiny Agents: an MCP-powered agent in 50 lines of code](https://huggingface.co/blog/tiny-agents)
> 
> 翻译时间：2026-04-23 05:00
