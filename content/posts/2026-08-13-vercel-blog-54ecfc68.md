---
title: GLM 5.2免费开放至8月27日，eve agents默认模型
title_original: GLM 5.2 free for eve agents through August 27 via Blackbox on AI Gateway
  - Vercel
date: '2026-08-13'
source: Vercel Blog
source_url: https://vercel.com/changelog/glm-5-2-free-for-eve-agents-through-august-27-via-blackbox-on-ai-gateway
author: ''
summary: Z.ai的开源权重编码模型GLM 5.2，拥有100万Token上下文窗口，现通过AI Gateway上的Blackbox AI对所有eve agents免费开放至8月27日。新创建的eve
  agents默认使用该模型，现有agents可通过修改配置或运行CLI命令切换。此优惠不适用于Fast模式。8月27日后，GLM 5.2将以标准费率继续提供服务。这一举措降低了开发者使用高性能模型的门槛，推动了AI代理的普及。
categories:
- AI产品
tags:
- GLM 5.2
- eve agents
- AI Gateway
- 免费模型
- 开源模型
draft: false
translated_at: '2026-08-15T03:05:17.191721'
---

GLM 5.2，来自Z.ai的开源权重编码模型，拥有100万Token的上下文窗口，通过AI Gateway上的Blackbox AI提供服务，对所有eve agents免费至8月27日。

新的eve agents默认使用GLM 5.2作为其默认模型。使用`npx eve@latest init my-agent`即可开始。

现有agents也可以通过修改`agent/agent.ts`中的一行代码来享受这一优惠：

```
1import { defineAgent } from "eve";2
3export default defineAgent({4  model: "zai/glm-5.2",5});
```

在agent定义中设置推广模型

或者通过CLI运行`eve set`命令：

```
eve set --model zai/glm-5.2
```

该命令会直接修改agent定义

此优惠不适用于Fast模式或`zai/glm-5.2-fast`模型变体。

8月27日之后，GLM 5.2将继续在AI Gateway上以标准提供商费率提供。

在模型游乐场中试用GLM 5.2。

---

> 本文由AI自动翻译，原文链接：[GLM 5.2 free for eve agents through August 27 via Blackbox on AI Gateway - Vercel](https://vercel.com/changelog/glm-5-2-free-for-eve-agents-through-august-27-via-blackbox-on-ai-gateway)
> 
> 翻译时间：2026-08-15 03:05
