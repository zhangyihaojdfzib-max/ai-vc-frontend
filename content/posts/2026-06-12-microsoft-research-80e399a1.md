---
title: AI智能体发现LOTUSLITE变种，绕过主流EDR检测
title_original: Inside Project Ire’s discovery of an evasive malware sample
date: '2026-06-12'
source: Microsoft Research
source_url: https://www.microsoft.com/en-us/research/blog/ire-identifies-another-lotuslite-specimen/
author: ''
summary: Project Ire，一个基于LLM的恶意软件分类智能体，在盲测中成功识别出LOTUSLITE的一个变种。该变种与已知家族共享TTPs，但不包含任何入侵指标（IOC），导致主流EDR（如CrowdStrike、SentinelOne等）在初期均未将其标记为恶意。Ire通过反编译器生成逐函数行为报告，无需人工干预即可判定恶意软件，展示了基于行为的逆向工程在应对新型变种时的有效性。
categories:
- AI产品
tags:
- AI安全
- 恶意软件检测
- LOTUSLITE
- 逆向工程
- EDR绕过
draft: false
translated_at: '2026-06-13T06:18:51.065883'
---

## 概览

- Project Ire 识别出一个 LOTUSLITE 变种，该变种与公开家族共享 TTPs（工具、战术、程序），但不包含任何入侵指标（IOC）。
- 基于 LLM 的 Agent（智能体）在无需任何用户交互的情况下，对该样本生成逐函数的行为报告，以判定其是否为恶意软件。
- 该二进制文件以明文形式命名了一个威胁行为者；Agent（智能体）拒绝进行归因，而是专注于静态分析其行为。

我们将 Microsoft 的自主恶意软件分类 Agent（智能体）Project Ire 指向一个恶意软件样本——盲测——并要求其给出判定。该样本是 LOTUSLITE 的一个变种，LOTUSLITE 是 Acronis 最近记录的一个 Windows DLL 后门。我们手中的副本哈希值不在他们的 IOC 列表中，截至 6 月 4 日，大多数主流 EDR（CrowdStrike Falcon、SentinelOne、Sophos、Trellix、Palo Alto、ESET）仍未将其标记为恶意软件。Ire 生成了一份逐函数的行为报告——安装例程、C2 数据包布局、命令 ID、持久化机制、混淆——与 Acronis 发布的分析结果一致。仅基于反编译器的一次运行，无需任何人工先验知识。

这就是当特征匹配和人工检查力有不逮时，基于行为的、Agent（智能体）化的逆向工程所能达到的效果。共享 TTPs 但不包含入侵指标（IOC）的变种会被捕获，而不会从特征列表的缝隙中溜走。新型恶意软件分类是一个没有自动验证器的领域，需要深入调查和对软件行为的整体理解，才能浮现并确定其意图。Ire 在无上下文的情况下运行：没有来源元数据，没有遥测数据，没有分析师的提示词。它调用反编译器和二进制分析工具，构建一条可审计的证据链，并得出恶意或良性的判定。

Acronis 的威胁研究部门（TRU）发布了一篇关于 LOTUSLITE 的详细分析报告（在新标签页中打开），LOTUSLITE 是一个 DLL 后门，通过一个带有政治主题的 ZIP 文件投递，并通过重命名的腾讯酷狗启动器进行侧加载。基于基础设施的重叠以及加载器/DLL 的分离，他们以中等置信度将其归因于 Mustang Panda。在 VirusTotal 上搜索行为与该报告匹配的样本时，我们发现了一个 SHA-256 未出现在 Acronis IOC 列表中的样本。

该样本：47e51e82229e80a387c3cb100d39d3705e6360bbf9bfa1601dbc484e8d02e653（在新标签页中打开）。当我们在 5 月 28 日获取它时，VirusTotal 显示只有 1/72 的供应商将其标记。

![图 1. 文件样本 47e51e82229e80a387c3cb100d39d3705e6360bbf9bfa1601dbc484e8d02e653 于 2026 年 5 月 28 日在 VirusTotal 上的检测状态。](/images/posts/36fb94b364d8.png)

一周后，这一数字上升到 7/70。检测集群包括：Microsoft Trojan:Win32/Malgent!MSR、Kaspersky HEUR:Trojan-Dropper.Win32.Dorifel.gen、Rising Dropper.Dorifel!8.31E (CLOUD)、Cynet（评分 100）、Elastic（中等置信度）、Kingsoft、TrendMicro-HouseCall。随着 Microsoft 现在将其标记，VT 的流行威胁标签已转变为 dropper.dorifel / malgent。CrowdStrike Falcon、SentinelOne、Sophos、Trellix、Palo Alto 和 ESET 仍然漏报。VT 将文件类型列为 pedll（PE DLL），文件名为 SmartPrintScreen.Print。

![图 2. 文件样本 47e51e82229e80a387c3cb100d39d3705e6360bbf9bfa1601dbc484e8d02e653 于 2026 年 6 月 4 日在 VirusTotal 上的检测状态。](/images/posts/b19dd353a726.png)

我们使用 Ire 分析了该样本，仅通过一次工具调用使用了其基于反编译器的工具。Ire 的判定是“恶意”；您可以在 Github（在新标签页中打开）上查看完整报告。

## 关于 Ire 的校准

Ire 报告（在新标签页中打开）中一个值得注意的观察点值得首先强调。Ire 将 nfapi::nf_unRegisterDriver 和 NetFilter 命名标记为可疑，但明确未声称存在主动数据包拦截。所讨论的函数写入 Run 键；它并未安装驱动程序。这正是 LLM 驱动的分析可能出错的地方：暗示性的字符串可能会左右判定结果。一个名为 nf_unRegisterDriver 的函数听起来像是在执行内核级的工作，一个不够彻底的 Agent（智能体）会将其写入报告。下游的防御者随后会追逐一个幻影，为可能存在也可能不存在的行为构建检测规则。Ire 标记了该误导性名称，并在最终判定恶意性时将该行为作为证据的一部分加以考量。

## 比较两份报告

将 Ire 的输出与 Acronis 的报告进行比较，我们分析的样本与 LOTUSLITE 恶意软件家族的行为特征相符。两者都显示加载器/DLL 分离、承载自定义二进制协议（带有魔数 DWORD）的 HTTPS C2、通过管道的交互式 shell、目录枚举、文件原语、分块上传、HKCU 持久化以及伪装成 Google 和 Microsoft 服务的流量。表面细节有所不同——文件名、路径、魔数值——但底层行为是一致的。Ire 正确地将此样本识别为同一恶意软件家族的一部分，这是因为它能够通过反编译和逆向工程识别出这些行为，而不仅仅是基于字符串匹配。

由于该样本是一个 DLL（根据 VT 为 pedll），其安装例程的解读方式可能与初看时不同。该 DLL 将两个文件复制到 C:\ProgramData\SmartPrint\：侧加载它的加载器 EXE（其宿主进程，通过 GetModuleFileName(NULL) 获取，写入为 SmartPrintScreen.exe）以及它自身（AMPV.dll，即被分析的样本）。Run 键指向带有 –DaDaBar 参数的加载器。下次登录时，加载器运行并从安装路径侧加载 AMPV.dll。这与 Acronis 识别的模式相同，但文件名不同。

这也解释了该二进制文件奇怪的导出表面。该 DLL 导出了一长串以银行和二维码为主题的名称（Query_Bank、BankSepah_Iran、BankToman_BMI、BankofChina、qrBankInit、JpgSymbolToBMP 等），其中大部分解析为消息框或 ExitProcess。其形态暗示了一个被劫持的银行/二维码 SDK 外壳，被重新利用，以便宿主 EXE 可以通过 GetProcAddress 调用其中任何一个导出函数，并到达 LOTUSLITE 入口点。Acronis 将其命名为 DataImporterMain。Ire 报告没有呈现匹配的入口点名称，但它识别出行为形态是相同的。

Acronis 基于我们无法访问的基础设施和 TTPs，以中等置信度将恶意软件家族归因于 Mustang Panda，而我们的样本直接包含一个字面意义上的行为者名称字符串“BelievemeIamMustang-Panda”，且未加混淆。一个字符串并非作者身份的直接证据；它可能是一个开发者遗留物、一个战利品或一个故意植入的信息。虽然我们不进行归因判断，但我们注意到该二进制文件命名了 Acronis 通过其他方式命名的同一个行为者，我们将此问题留待讨论。对此发现的另一个考量是：像这样的字符串可以作为针对 LLM 驱动分析的对抗性输入，从而影响判定结果。

![](/images/posts/5c4d3fa0eed0.jpg)

## Azure AI Foundry Labs

通过这些来自 Microsoft Research 的实验性技术，一窥 AI 未来潜在的发展方向。

## 为何重要

Ire 静态逆向工程二进制文件，并从函数级到系统级识别行为，以描述软件的功能并做出判定。此样本的判定来自一次 Ire 运行，这得益于 Ire 能够揭示的具体细节：函数角色、数据包布局、命令 ID、持久化注册表键以及诱饵字符串。Ire 在其报告或证据链中从未提及 LOTUSLITE。家族映射是我们事后进行的，将 Ire 的报告与 Acronis 的报告进行了比较。Ire 足够精确地描述了行为，使得将此样本映射到 LOTUSLITE 变得直接明了。

请在我们的项目页面上关注 Project Ire 的最新发现和其他有趣的样本检测结果。

## 关于作者

### Brian Caswell

首席安全工程师

### Bob Fleck

高级安全工程师

### Mike Walker

研究经理

---

> 本文由AI自动翻译，原文链接：[Inside Project Ire’s discovery of an evasive malware sample](https://www.microsoft.com/en-us/research/blog/ire-identifies-another-lotuslite-specimen/)
> 
> 翻译时间：2026-06-13 06:18
