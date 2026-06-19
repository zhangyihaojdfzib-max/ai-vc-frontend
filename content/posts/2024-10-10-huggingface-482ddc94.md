---
title: Gradio 5安全审计：修复漏洞，默认安全
title_original: A Security Review of Gradio 5
date: '2024-10-10'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/gradio-5-security
author: ''
summary: Gradio 5委托Trail of Bits进行独立安全审计，针对本地运行、服务器部署、分享链接及供应链等场景发现多项安全漏洞，包括CORS配置错误、SSRF、任意文件上传、竞态条件等。所有问题已在5.0版本中修复，确保机器学习应用默认遵循Web安全最佳实践，无需开发者额外配置。
categories:
- AI基础设施
tags:
- Gradio
- 安全审计
- 机器学习
- Web安全
- 漏洞修复
draft: false
translated_at: '2026-06-19T07:07:33.961326'
---

# Gradio 5 安全审查

我们对 Gradio 5 进行了审计，以确保您的机器学习应用安全无虞！

在过去几年中，Gradio（月均 PyPI 安装量超过 600 万）已成为用 Python 构建机器学习 Web 应用的默认方式。仅需几行代码，您就可以为图像生成应用、聊天机器人或任何其他类型的 ML 应用创建用户界面，并使用 Gradio 内置的分享链接或 Hugging Face Spaces 与他人分享。

```py
import gradio as gr
def generate(seed, prompt):  
    ...  
    return image
    

gr.Interface(
    generate,   
    inputs=[gr.Slider(), gr.Textbox()],  
    outputs=[gr.Image()]
).launch(share=True)  


```

我们使用 Gradio 的目标是让开发者能够构建开箱即用、适用于机器学习场景的 Web 应用。这意味着让您作为开发者能够轻松构建以下应用：

- 轻松扩展到大量并发用户
- 尽可能让更多用户可访问
- 提供一致的 UI、UX 和主题
- 在大量浏览器和设备上可靠运行

……即使您不是扩展性、可访问性或 UI/UX 方面的专家！

现在，我们将 **Web 安全** 也加入了这个列表。我们委托知名网络安全公司 Trail of Bits 对 Gradio 进行独立审计。他们发现的安全问题已在 Gradio 5 发布前全部修复。

这意味着，您使用 Gradio 5 构建的机器学习应用将在 Web 安全方面遵循最佳实践，而无需对代码进行任何重大更改。

## 为何进行安全审计？

在过去几年中，Gradio 团队一直与社区合作，在发现安全漏洞时及时修补。但随着 Gradio 的普及（目前 Hugging Face Spaces 上有超过 47 万个 Gradio 应用），确保安全性变得愈发重要。

因此，在 Gradio 5 中，我们决定采取不同的方法——对 Gradio 代码库进行 **预防性** 安全审计，以确保您使用 Gradio 5 构建的机器学习应用默认安全。

我们委托 Trail of Bits 对 Gradio 进行独立且全面的审计。他们的人工智能与应用安全专家团队在 4 种常见场景中识别出了 Gradio 代码库的安全风险：

- 本地运行的 Gradio 应用
- 部署在 Hugging Face Spaces 或其他服务器上的 Gradio 应用
- 通过内置分享链接分享的 Gradio 应用
- 源自 Gradio CI 管道的供应链漏洞

![](/images/posts/5c98013cbf48.png)

随后，我们与 Trail of Bits 密切合作，为每种风险确定了缓解策略。Gradio 的简洁易用性虽然对开发者有利，但也带来了独特的安全挑战，因为我们不希望开发者需要设置 CORS 和 CSP 策略等复杂的安全措施。

合作结束时，我们修复了 Trail of Bits 识别的所有安全风险。所有修复措施均经过 Trail of Bits 验证，并已包含在 Gradio 5.0 版本中。虽然无法证明不存在安全漏洞，但这是确保您的 Gradio 应用安全可靠的重要一步。

## 主要发现

以下概述了 Trail of Bits 发现的与上述 4 种场景相对应的主要安全漏洞。本着透明和开源精神，我们将 **完整安全报告** 公开，每个问题的更多细节可在报告中找到。

**本地运行的 Gradio 应用**

- TOB-GRADIO-1 和 TOB-GRADIO-2：服务器 CORS 策略配置错误，在已认证的 Gradio 服务器环境下，攻击者可在受害者访问其恶意网站时窃取访问令牌并接管受害者账户。

**部署在 Hugging Face Spaces 或其他服务器上的 Gradio 应用**

- TOB-GRADIO-3：基于 GET 的完全读取型 SSRF，允许攻击者向任意端点发起请求并读取响应，包括用户内部网络上的端点。
- TOB-GRADIO-10：任意文件类型上传，允许攻击者在用户的 Gradio 服务器上托管 XSS 载荷。在已认证的 Gradio 服务器环境下，攻击者可利用此漏洞在受害者访问攻击者恶意网站时接管用户账户。
- TOB-GRADIO-13：竞态条件，允许攻击者将用户流量重定向到其服务器，并窃取上传的文件或聊天机器人对话。
- TOB-GRADIO-16：多个组件的后处理函数可能允许攻击者在非常简单的 Gradio 服务器配置中泄露任意文件。

TOB-GRADIO-3：基于 GET 的完全读取型 SSRF，允许攻击者向任意端点发起请求并读取响应，包括用户内部网络上的端点。

TOB-GRADIO-10：任意文件类型上传，允许攻击者在用户的 Gradio 服务器上托管 XSS 载荷。在已认证的 Gradio 服务器环境下，攻击者可利用此漏洞在攻击者恶意网站被受害者访问时接管用户账户。

TOB-GRADIO-13：竞态条件，允许攻击者将用户流量重定向到其服务器，并窃取上传的文件或聊天机器人对话。

TOB-GRADIO-16：多个组件的后处理函数可能允许攻击者在非常简单的 Gradio 服务器配置中泄露任意文件。

**通过内置分享链接分享的 Gradio 应用**

- TOB-GRADIO-19：通过 nginx 配置错误暴露未经认证的 Docker API，导致以 root 用户在 Gradio API 服务器上实现远程代码执行（RCE）。这允许攻击者在图示步骤 2 中提供恶意主机和端口，将所有 frp 隧道重定向到恶意服务器，记录所有用户流量，包括上传的文件和聊天框对话。
- TOB-GRADIO-11：frp 客户端与 frp 服务器之间通信缺乏强加密，允许能够拦截请求（上述图示步骤 6 和 7 中的请求）的攻击者读取和修改进出 frp 服务器的数据。

TOB-GRADIO-19：通过 nginx 配置错误暴露未经认证的 Docker API，导致以 root 用户在 Gradio API 服务器上实现远程代码执行（RCE）。这允许攻击者在图示步骤 2 中提供恶意主机和端口，将所有 frp 隧道重定向到恶意服务器，记录所有用户流量，包括上传的文件和聊天框对话。

TOB-GRADIO-11：frp 客户端与 frp 服务器之间通信缺乏强加密，允许能够拦截请求（上述图示步骤 6 和 7 中的请求）的攻击者读取和修改进出 frp 服务器的数据。

**源自 Gradio CI 管道的供应链漏洞**

- TOB-GRADIO-25：Gradio 仓库中的多个 GitHub Actions 工作流使用了固定到标签或分支名称而非完整提交 SHA 的第三方操作。这可能允许恶意行为者静默修改操作，从而导致篡改应用发布或泄露机密。
- 此外，一位 **GitHub 安全研究员** 报告称，如果攻击者触发工作流并巧妙转储 GitHub 运行器的内存，我们的 GitHub 操作可能允许不受信任的代码执行和机密泄露。

TOB-GRADIO-25：Gradio 仓库中的多个 GitHub Actions 工作流使用了固定到标签或分支名称而非完整提交 SHA 的第三方操作。这可能允许恶意行为者静默修改操作，从而导致篡改应用发布或泄露机密。

此外，一位 **GitHub 安全研究员** 报告称，如果攻击者触发工作流并巧妙转储 GitHub 运行器的内存，我们的 GitHub 操作可能允许不受信任的代码执行和机密泄露。

## 未来展望

我们非常感谢 Trail of Bits 对 Gradio 进行的全面安全审计，并验证了我们在 Gradio 5 中实施的缓解措施。

展望未来，我们计划继续与安全社区合作，识别并缓解 Gradio 中的安全问题。我们还在测试套件中增加了安全单元测试，专门设计了用于识别潜在漏洞的模糊测试，并在 CI 中使用 Semgrep 等静态分析工具，以检测代码中的常见安全问题并防止安全回归。

我们致力于确保在继续开发 Gradio 5（我们还有很多计划！）的过程中，优先考虑安全性，从而为让机器学习应用变得更好、更安全贡献自己的力量。

立即安装 Gradio 5：

pip install --upgrade gradio

并开始构建您的第一个 Gradio 5 应用程序。

---

> 本文由AI自动翻译，原文链接：[A Security Review of Gradio 5](https://huggingface.co/blog/gradio-5-security)
> 
> 翻译时间：2026-06-19 07:07
