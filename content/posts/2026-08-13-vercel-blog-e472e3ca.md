---
title: AI SDK新增ACP元适配器，支持任意兼容Harness
title_original: Use ACP-compatible harnesses with the AI SDK harness layer - Vercel
date: '2026-08-13'
source: Vercel Blog
source_url: https://vercel.com/changelog/use-acp-compatible-harnesses-with-the-ai-sdk-harness-layer
author: ''
summary: Vercel的AI SDK harness层推出新包@ai-sdk/harness-acp，通过封装Agent Client Protocol（ACP）协议，使任何提供ACP兼容包的harness都能被集成。该元适配器替代了此前针对特定运行时的直接适配器，开发者只需配置harness映射即可使用。文章建议，对于Claude
  Code和Codex等已有直接适配器的harness，仍优先使用直接适配器以获得更紧密集成；仅当harness无直接适配器但支持ACP时，才使用此新方案。
categories:
- AI基础设施
tags:
- AI SDK
- ACP协议
- Harness适配
- Vercel
- 开发者工具
draft: false
translated_at: '2026-08-16T03:01:29.090621'
---

AI SDK 的 harness 层现在通过新的 `@ai-sdk/harness-acp` 包，支持任何兼容 Agent Client Protocol (ACP) 的 harness，并可通过 `HarnessAgent` 使用。

此前，每个 harness 适配器都封装一个特定的运行时（Claude Code、Codex、Pi、Deep Agents、OpenCode）。`@ai-sdk/harness-acp` 转而封装协议本身。它是一个元适配器：并非适配单个 harness，而是让您能够为任何提供 ACP 兼容包的 harness 构建适配器。

通过将该包传递给 `createACP` 并配置基本的 harness 映射来实现一个 harness。

```
1import { createACP } from '@ai-sdk/harness-acp';2
3export function createCodexACP() {4  return createACP({5    harnessId: 'codex-acp',6    source: {7      type: 'npm-simple',8      packageName: '@agentclientprotocol/codex-acp',9    },10    executable: 'codex-acp',11    forwardEnv: ['CODEX_API_KEY', 'OPENAI_API_KEY'],12    permissionModeMapping: {13      'allow-reads': null,14      'allow-edits': null,15      'allow-all': { type: 'session-mode', modeId: 'agent-full-access' },16    },17    authentication: {18      methodId: 'api-key',19    },20  });21}
```

基于 ACP 元 harness 为 Codex 实现的基本 ACP harness 示例

然后像其他任何 harness 一样将其传递给 `HarnessAgent`：

```
1import { HarnessAgent } from '@ai-sdk/harness/agent';2import { createCodexACP } from './codex-acp-harness';3
4const agent = new HarnessAgent({5  harness: createCodexACP(),6});
```

使用上述 Codex ACP harness 与 HarnessAgent 的基本示例

ACP 是对编码 harness 的一种抽象，但 AI SDK 的 harness 层刻意与其保持解耦。并非所有 harness 都支持 ACP，且对于某些 harness，ACP 会限制或改变其内部行为的暴露方式，因此直接适配器可能实现更紧密的集成。

对于 Claude Code 和 Codex，建议优先使用直接的 `@ai-sdk/harness-claude-code` 和 `@ai-sdk/harness-codex` 适配器，而非基于 ACP 的实现；当某个 harness 没有直接适配器但提供了 ACP 兼容包时，再使用 `@ai-sdk/harness-acp`。

请阅读 ACP harness 文档以开始使用。

---

> 本文由AI自动翻译，原文链接：[Use ACP-compatible harnesses with the AI SDK harness layer - Vercel](https://vercel.com/changelog/use-acp-compatible-harnesses-with-the-ai-sdk-harness-layer)
> 
> 翻译时间：2026-08-16 03:01
