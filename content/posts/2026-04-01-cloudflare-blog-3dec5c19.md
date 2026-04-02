---
title: EmDash：WordPress精神续作，用沙箱插件解决安全危机
title_original: "Introducing EmDash â\x80\x94 the spiritual successor to WordPress\
  \ that solves plugin security"
date: '2026-04-01'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/emdash-wordpress/
author: ''
summary: 本文介绍了新型开源CMS EmDash，作为WordPress的精神续作，旨在解决其核心插件安全问题。EmDash完全采用TypeScript编写，基于Astro框架，支持无服务器部署。其关键创新在于通过动态工作线程为插件提供安全沙箱环境，插件只能访问其清单中明确声明的权限，从根本上隔离了风险。文章指出WordPress插件是96%安全问题的根源，而EmDash的架构设计有望改变这一现状，同时继承WordPress的易用性和开源精神。
categories:
- 技术趋势
tags:
- WordPress
- 内容管理系统
- 开源软件
- 网络安全
- TypeScript
draft: false
translated_at: '2026-04-02T05:05:43.838047'
---

# 推出EmDash——WordPress的精神续作，解决插件安全问题

2026-04-01

- Matt "TK" Taylor
- Matt Kane

![](/images/posts/fa3b642559fd.png)

构建软件的成本已大幅降低。我们最近[在一周内用AI编码智能体重建了Next.js](https://example.com)。但在过去两个月里，我们的智能体一直在进行一个更雄心勃勃的项目：**从头开始重建WordPress开源项目**。

WordPress驱动着**超过40%的互联网**。它是一个巨大的成功，让任何人都能成为发布者，并创建了一个全球性的WordPress开发者社区。但WordPress开源项目今年将满24岁。在此期间，托管网站的方式已发生巨大变化。WordPress诞生时，AWS EC2还不存在。在这些年间，这项任务已从租用虚拟专用服务器，发展到几乎零成本地将JavaScript包上传到全球分布式网络。现在是时候升级互联网上最流行的CMS，以利用这一变化了。

我们将这个新CMS命名为EmDash。我们将其视为WordPress的精神续作。它完全用TypeScript编写。它是无服务器的，但你可以在自己的硬件或选择的任何平台上运行它。插件通过**动态工作线程**在安全沙箱中运行，解决了WordPress插件架构的根本安全问题。在底层，EmDash由**Astro**驱动，这是面向内容驱动网站的最快Web框架。

EmDash是完全开源的，采用MIT许可证，并[可在GitHub上获取](https://github.com/emdash/emdash)。虽然EmDash旨在兼容WordPress功能，但创建EmDash时未使用任何WordPress代码。这使我们能够在更宽松的MIT许可证下授权开源项目。我们希望这能让更多开发者适应、扩展和参与EmDash的开发。

作为早期开发者测试版的一部分，你现在可以将EmDash v0.1.0预览版部署到你自己的Cloudflare账户，或任何Node.js服务器：

或者，你可以在[EmDash Playground](https://playground.emdash.dev)中试用管理界面：

### WordPress的成就

WordPress的故事是开源的一次胜利，它实现了前所未有的规模化发布。很少有项目对在互联网时代成长起来的一代人产生过如此公认的影响。WordPress核心的贡献者，以及成千上万的插件和主题开发者，共同构建了一个平台，为数百万用户实现了发布的民主化；这款无处不在的软件改变了许多人的生活和生计。

WordPress将永远占有一席之地，但内容发布的世界还有更大的发展空间。十年前，拿起键盘的人们普遍学习用WordPress发布博客。今天，那个人同样可能选择Astro或另一个TypeScript框架来学习和构建。生态系统需要一个能赋能广大受众的选择，就像23年前需要WordPress一样。

EmDash致力于在WordPress创建的基础上继续发展：一个任何人都可以低成本安装和使用的开源发布堆栈，同时解决WordPress无法解决的核心问题。

### 解决WordPress插件安全危机

WordPress的插件架构从根本上是不安全的。WordPress网站**96%的安全问题**源于插件。2025年，在WordPress生态系统中发现的**高危漏洞数量超过了前两年的总和**。

为什么经过二十多年，WordPress插件安全问题仍然如此严重？

WordPress插件是一个直接挂钩到WordPress以添加或修改功能的PHP脚本。没有隔离：WordPress插件可以直接访问WordPress网站的数据库和文件系统。当你安装一个WordPress插件时，你实际上信任它可以访问几乎所有内容，并相信它能完美处理每一个恶意输入或边缘情况。

EmDash解决了这个问题。在EmDash中，每个插件都在自己独立的沙箱中运行：**一个动态工作线程**。EmDash不是直接提供对底层数据的访问，而是通过**绑定**为插件提供**能力**，这些能力基于插件在其清单中明确声明的需求。这种安全模型有严格的保证：EmDash插件只能执行其清单中明确声明的操作。在安装插件之前，你可以预先知道并信任你授予它的确切权限，类似于通过OAuth流程并授予第三方应用一组特定范围的权限。

例如，一个在内容项保存后发送邮件的插件如下所示：

```JavaScript
import { definePlugin } from "emdash";

export default () =>
  definePlugin({
    id: "notify-on-publish",
    version: "1.0.0",
    capabilities: ["read:content", "email:send"],
    hooks: {
      "content:afterSave": async (event, ctx) => {
        if (event.collection !== "posts" || event.content.status !==    "published") return;

        await ctx.email!.send({
          to: "[email protected]",
          subject: `New post published: ${event.content.title}`,
          text: `"${event.content.title}" is now live.`,
         });

        ctx.log.info(`Notified editors about ${event.content.id}`);
      },
    },
  });
```

这个插件明确请求两个能力：`content:afterSave` 以挂钩到内容生命周期，以及 `email:send` 以访问 `ctx.email` 函数。插件除了使用这些能力外，不可能做任何其他事情。它没有外部网络访问权限。如果确实需要网络访问，它可以在其定义中指定需要通信的确切主机名，并且只被授予与特定主机名通信的能力。

在所有情况下，由于插件的需求是静态、预先声明的，在安装时，总是可以清楚地知道插件请求的权限是什么。平台或管理员可以根据插件请求的权限，而不是根据已批准或安全插件的白名单，来定义允许或禁止特定用户组安装哪些插件的规则。

### 解决插件安全意味着解决市场锁定

WordPress插件安全风险如此真实，以至于WordPress.org[手动审查并批准其市场中的每个插件](https://example.com)。在撰写本文时，审查队列超过800个插件，至少需要两周时间才能处理完。WordPress插件的漏洞面如此之广，以至于在实践中，各方都依赖市场声誉、评级和评论。而且由于WordPress插件在与WordPress本身相同的执行上下文中运行，并且与WordPress代码深度交织，有人认为它们必须继承WordPress的GPL许可证。

这些现实情况结合在一起，对构建插件的开发者和托管WordPress网站的平台产生了寒蝉效应。

插件安全是这个问题的根源。当各方无法轻易互信时，市场业务提供信任。就WordPress市场而言，插件安全风险如此之大且可能发生，以至于许多客户只能通过市场合理地信任你的插件。但为了成为市场的一部分，你的代码必须以某种方式授权，迫使你在市场之外的其他地方免费提供它。你被锁定了。

EmDash插件有两个重要特性可以缓解这种市场锁定：

1.  **插件可以采用任何许可证**：它们独立于EmDash运行，不共享任何代码。这是插件作者的选择。
2.  **插件代码在安全沙箱中独立运行**：可以向EmDash站点提供插件并信任它，而EmDash站点永远看不到代码。

插件可以采用任何许可证：它们独立于EmDash运行，不共享任何代码。这是插件作者的选择。

插件代码在安全的沙盒中独立运行：插件可以提供给EmDash站点并被信任，而EmDash站点永远看不到代码。

第一部分很简单——作为插件作者，**您可以选择您想要的许可证**。就像您发布到NPM、PyPi、Packagist或任何其他注册中心时一样。这是一个面向所有人的开放生态系统，插件和主题使用什么许可证取决于社区，**而不是EmDash项目**。

第二部分是EmDash插件架构摆脱中心化市场的地方。

开发者需要依赖第三方市场对插件进行审查的程度要低得多，以便能够决定是否使用或信任它。考虑上面那个在内容保存后发送邮件的示例插件；该插件声明了三件事：

- 它仅在 `content:afterSave` 钩子上运行
- 它具有 `read:content` 能力
- 它具有 `email:send` 能力

它仅在 `content:afterSave` 钩子上运行

它具有 `read:content` 能力

它具有 `email:send` 能力

插件内部可能有成千上万行代码，但与可以访问一切并能与公共互联网通信的WordPress插件不同，添加插件的人确切知道他们授予了插件什么访问权限。清晰定义的边界允许您就安全风险做出明智的决策，并专注于与插件被赋予的能力直接相关的更具体的风险。

站点和平台越能信任安全模型提供的约束，它们就越能信任插件，并摆脱市场和声誉的中心化控制。换句话说：如果您相信您所在城市的食品安全得到强制执行，您就会勇于尝试新地方。如果您无法信任汤里可能没有订书钉，那么您在尝试每个新地方之前都会咨询谷歌，每个人开新餐馆都变得更难。

### 每个EmDash站点都内置了x402支持——为内容访问收费

网络的商业模式正面临风险，特别是对于内容创作者和发布者而言。旧的广泛提供内容、允许所有客户端免费访问以换取流量的方式，在没有人浏览网站以投放广告、客户端反而是代表用户访问网络的Agent时，就会失效。创作者需要在这个Agent的新世界中继续赚钱的方式，并构建新型网站，以满足人们Agent的需求并愿意为之付费。几十年前，一波新的创作者创建了网站，并发展成为伟大的企业（通常使用WordPress驱动），今天也存在类似的机会。

x402是一个开放的、中立的互联网原生支付标准。它允许互联网上的任何人轻松收费，任何客户端都可以按需、按使用次数付费。客户端（例如Agent）发送HTTP请求并收到HTTP 402 Payment Required状态码。作为响应，客户端按需支付访问费用，服务器可以让客户端访问所请求的内容。

EmDash内置了对x402的支持。这意味着任何拥有EmDash站点的人都可以对其内容访问收费，无需订阅，也无需任何工程工作。您只需要配置哪些内容需要付费，设置收费金额，并提供一个钱包地址。请求/响应流程最终如下所示：

每个EmDash站点都内置了面向AI时代的商业模式。

### 为WordPress托管平台解决"缩放到零"的问题

WordPress不是无服务器的：它需要配置和管理服务器，像传统的Web应用程序一样进行伸缩。为了最大化性能，并能够处理流量高峰，不可避免地需要预配置实例并运行一定量的空闲计算，或者以限制性能的方式共享资源。对于内容必须由服务器渲染且无法缓存的站点来说尤其如此。

EmDash则不同：它构建为在无服务器平台上运行，并充分利用Cloudflare开源运行时workerd的v8 isolate架构。在收到传入请求时，Workers运行时会立即启动一个isolate来执行代码并提供响应。如果没有请求，它会缩放到零。并且它**只对CPU时间（用于实际工作的时间）计费**。

您可以在任何Node.js服务器上运行EmDash——但在Cloudflare上，您可以使用Cloudflare for Platforms运行数百万个EmDash实例，每个实例都可以完全缩放到零或扩展到您需要处理的任意RPS（每秒请求数），使用的是世界上最大网站所依赖的完全相同的网络和运行时。

除了成本优化和性能优势之外，我们在Cloudflare押注这种架构的部分原因是我们相信应该提供低成本甚至免费层级，并且每个人都应该能够构建可扩展的网站。我们很高兴能帮助平台将这种架构的优势扩展到他们自己的客户，无论大小。

### 通过Astro实现现代前端主题和架构

EmDash由Astro驱动，Astro是面向内容驱动网站的Web框架。要创建EmDash主题，您需要创建一个包含以下内容的Astro项目：

- 页面：用于渲染内容的Astro路由（首页、博客文章、存档等）
- 布局：共享的HTML结构
- 组件：可复用的UI元素（导航、卡片、页脚等）
- 样式：CSS或Tailwind配置
- 种子文件：告诉CMS要创建什么内容类型和字段的JSON

页面：用于渲染内容的Astro路由（首页、博客文章、存档等）

布局：共享的HTML结构

组件：可复用的UI元素（导航、卡片、页脚等）

样式：CSS或Tailwind配置

种子文件：告诉CMS要创建什么内容类型和字段的JSON

这使得前端开发者创建主题变得熟悉，他们**越来越多地选择Astro**，对于已经接受过Astro训练的LLM也是如此。

WordPress主题虽然极其灵活，但面临着与插件类似的大量安全风险，而且您的主题越流行、越常见，就越容易成为攻击目标。主题通过集成`functions.php`来运行，这是一个包罗万象的执行环境，使您的主题既功能强大又潜在危险。EmDash主题，与动态插件一样，颠覆了这种预期。您的主题永远无法执行数据库操作。

### 一个AI原生的CMS——EmDash的MCP、CLI和技能

使用任何CMS最无趣的部分就是进行机械的内容迁移：查找和替换字符串，将自定义字段从一种格式迁移到另一种格式，重命名、重新排序和移动内容。这要么是无聊的重复性工作，要么需要一次性脚本和"一次性"插件和工具，这些通常编写和使用起来都不有趣。

EmDash设计为由您的AI Agent以编程方式管理。它提供了您的Agent所需的上下文和工具，包括：

1.  **Agent技能**：每个EmDash实例都包含**Agent技能**，向您的Agent描述EmDash可以为插件提供的能力、可以触发插件的钩子、**如何构建插件的指导**，甚至**如何将遗留的WordPress主题原生移植到EmDash**。当您给Agent一个EmDash代码库时，EmDash提供了Agent所需的一切，使其能够以您需要的方式定制您的站点。
2.  **EmDash CLI**：**EmDash CLI**使您的Agent能够以编程方式与您的本地或远程EmDash实例交互。您可以**上传媒体**、**搜索内容**、**创建和管理模式**，并执行在管理界面中可以做的同一组事情。
3.  **内置MCP服务器**：每个EmDash实例都提供自己的远程模型上下文协议（MCP）服务器，允许您执行在管理界面中可以做的同一组事情。

**Agent（智能体）技能**：每个 EmDash 实例都包含 **Agent 技能**，用于向你的 Agent 描述 EmDash 可以为插件提供的能力、可以触发插件的钩子、如何构建插件的指导，甚至**如何将传统的 WordPress 主题原生移植到 EmDash**。当你给一个 Agent 提供 EmDash 代码库时，EmDash 会提供 Agent 所需的一切，使其能够按照你的需求定制网站。

**EmDash CLI**：**EmDash CLI** 使你的 Agent 能够以编程方式与你的本地或远程 EmDash 实例进行交互。你可以**上传媒体**、**搜索内容**、**创建和管理模式**，并执行在管理界面中可以完成的相同操作。

**内置 MCP 服务器**：每个 EmDash 实例都提供自己的远程模型上下文协议服务器，允许你执行在管理界面中可以完成的相同操作。

### 可插拔的身份验证，默认使用通行密钥

EmDash 默认使用基于通行密钥的身份验证，这意味着没有密码可泄露，也无需防范暴力破解攻击。用户管理开箱即用，包含熟悉的基于角色的访问控制：管理员、编辑、作者和贡献者，每个角色的权限都严格限定为其所需操作。身份验证是可插拔的，因此你可以设置 EmDash 以与你的单点登录提供商配合工作，并根据身份提供商元数据自动配置访问权限。

### 将你的 WordPress 站点导入 EmDash

你可以通过以下两种方式导入现有的 WordPress 站点：一是进入 WordPress 管理后台并导出 WXR 文件；二是在 WordPress 站点上安装 **EmDash Exporter 插件**，该插件会配置一个仅对你开放的安全端点，并由你控制的 WordPress 应用程序密码保护。迁移内容只需几分钟，并会自动将任何附加的媒体导入 EmDash 的媒体库。

在 WordPress 上创建任何非文章或页面的自定义内容类型，通常意味着需要安装像 Advanced Custom Fields 这样的大型插件，并将结果挤入拥挤的 WordPress 文章表中。EmDash 的做法不同：你可以直接在管理面板中定义模式，这将为你创建全新的 EmDash 集合，并在数据库中单独排序。在导入时，你可以使用相同的功能，从 WordPress 中获取任何自定义文章类型，并据此创建 EmDash 内容类型。

对于定制区块，你可以使用 **EmDash Block Kit Agent 技能** 来指导你选择的 Agent 并为 EmDash 构建它们。

### 尝试一下

EmDash 目前是 v0.1.0 预览版，我们非常希望你尝试它、提供反馈，并欢迎为 **EmDash GitHub 仓库** 做出贡献。

如果你只是想体验一下，并首先了解可能实现的功能——可以在 **EmDash Playground** 中试用管理界面。

要通过 CLI 在本地创建一个新的 EmDash 站点，请运行：

```
npm create emdash@latest
```

或者，你也可以通过下面的 Cloudflare 仪表板进行同样的操作：

我们很高兴看到你构建的作品。如果你活跃于 WordPress 社区，无论是作为托管平台、插件或主题作者，还是其他角色——我们都希望听到你的声音。请发送邮件至 [email protected]，告诉我们你希望从 EmDash 项目中看到什么。

如果你想及时了解 EmDash 的重大进展，可以在此处留下你的电子邮件地址。

---

> 本文由AI自动翻译，原文链接：[Introducing EmDash â the spiritual successor to WordPress that solves plugin security](https://blog.cloudflare.com/emdash-wordpress/)
> 
> 翻译时间：2026-04-02 05:05
