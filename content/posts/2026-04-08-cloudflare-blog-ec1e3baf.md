---
title: 从字节码到数据包：自动化生成触发恶意BPF的魔法包
title_original: From bytecode to bytes- automated magic packet generation
date: '2026-04-08'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/from-bpf-to-packet/
author: ''
summary: 本文探讨了如何利用符号执行和Z3定理证明器，自动化逆向分析Linux内核中恶意伯克利包过滤器（BPF）程序的方法。传统手动分析复杂BPF指令耗时耗力，而该技术能够从恶意过滤器的字节码中自动推导出触发其逻辑所需的特定网络数据包（即“魔法包”），将分析时间从数小时缩短至秒级。文章以BPFDoor后门为例，展示了该技术如何应对上百条指令的复杂BPF程序，为安全研究人员提供了高效检测和对抗隐蔽威胁的新工具。
categories:
- 技术趋势
tags:
- 网络安全
- 符号执行
- BPF
- 恶意软件分析
- 自动化
draft: false
translated_at: '2026-04-09T04:38:11.382293'
---

# 从字节码到数据包：自动化魔法包生成

2026-04-08

- Axel Boesenach

![](/images/posts/115eb8f65776.png)

Linux恶意软件通常隐藏在伯克利包过滤器（BPF）套接字程序中。这些程序是可执行逻辑的小片段，可以嵌入Linux内核以定制其处理网络流量的方式。互联网上一些最持久的威胁利用这些过滤器保持休眠状态，直到收到特定的"魔法"数据包。由于这些过滤器可能长达数百条指令，并涉及复杂的逻辑跳转，手动逆向工程是一个缓慢的过程，给安全研究人员造成了瓶颈。

为了找到更好的方法，我们研究了符号执行：一种将代码视为一系列约束而非仅仅是指令的方法。通过使用Z3定理证明器，我们可以从恶意过滤器反向推导，自动生成触发它所需的数据包。在本文中，我们将解释如何构建一个工具来自动化此过程，将数小时的手动汇编分析任务缩短至几秒钟。

## 复杂性上限

在探讨如何解构恶意过滤器之前，我们需要了解运行它们的引擎。伯克利包过滤器（BPF）是一种高效技术，允许内核根据一组字节码指令从网络栈中提取特定的数据包。

尽管许多现代开发者熟悉用于可观测性和安全的强大演进版本`eBPF`（扩展BPF），但本文重点讨论"经典"BPF。经典BPF最初为tcpdump等工具设计，使用一个仅有两个寄存器的简单虚拟机来高速评估网络流量。由于它在内核深处运行，并且可以"隐藏"用户空间工具的流量，它已成为试图构建隐蔽后门的恶意软件作者钟爱的工具。

虽然使用`LLM`（大语言模型）创建BPF指令的上下文表示已经减少了分析人员的手动开销，但即使有`LLM`提供的额外上下文，构建与验证条件相对应的网络数据包仍然可能是一项繁重的工作。

如果你的BPF程序只有大约20条指令，这通常不是问题。但正如我们在一些样本中观察到的那样，当BPF程序包含超过100条指令时，复杂性会呈指数级增长，耗时也会大大增加。

如果我们解构这个问题，可以看到它归结为读取缓冲区并检查约束，根据结果，我们要么继续执行路径，要么停止并检查最终结果。

这种具有确定性结果的问题可以通过Z3来解决。Z3是一个定理证明器，能够解决给定一组约束的问题。

## 案例A：BPFDoor

BPFDoor是一种复杂的被动式Linux后门，主要被包括Red Menshen（也称为Earth Bluecrow）在内的中国背景威胁行为者用于网络间谍活动。该恶意软件自2021年以来一直活跃，旨在在受感染的网络中保持隐蔽的立足点，主要针对电信、教育和政府部门，尤其关注亚洲和中东地区的行动。

BPFDoor使用BPF来监控所有传入流量，而无需开放特定的网络端口。

### BPFDoor示例指令

让我们关注Fortinet研究中分享的样本（82ed617816453eba2d755642e3efebfcbd19705ac626f6bc8ed238f4fc111bb0）。如果我们剖析BPF指令并添加一些注释，可以写出以下内容：

```Rust
(000) ldh [0xc]                   ; 读取偏移量12处的半字（EtherType）
(001) jeq #0x86dd, jt 2, jf 6     ; 0x86DD (IPv6) -> 指令002 否则指令006
(002) ldb [0x14]                  ; 读取偏移量20处的字节（协议）
(003) jeq #0x11, jt 4, jf 15      ; 0x11 (UDP) -> 指令004 否则丢弃
(004) ldh [0x38]                  ; 读取偏移量56处的半字（目标端口）
(005) jeq #0x35, jt 14, jf 15     ; 0x35 (DNS) -> 接受 否则丢弃
(006) jeq #0x800, jt 7, jf 15     ; 0x800 (IPv4) -> 指令007 否则丢弃
(007) ldb [23]                    ; 读取偏移量23处的字节（协议）
(008) jeq #0x11, jt 9, jf 15      ; 0x11 (UDP) -> 指令009 否则丢弃
(009) ldh [20]                    ; 读取偏移量20处的半字（分片）
(010) jset #0x1fff, jt 15, jf 11  ; 分片 -> 丢弃 否则指令011
(011) ldxb 4*([14]&0xf)           ; 加载索引（x）寄存器 ihl & 0xf
(012) ldh [x + 16]                ; 读取偏移量x+16处的半字（目标端口）
(013) jeq #0x35, jt 14, jf 15     ; 0x35 (DNS) -> 接受 否则丢弃
(014) ret #0x40000 (ACCEPT)
(015) ret #0 (DROP)
```

在上面的例子中，我们可以确定有两条路径会导致ACCEPT结果（步骤5和步骤13）。我们还可以清楚地观察到某些字节被检查，包括它们的偏移量和值。

根据这些验证，并跟踪任何符合ACCEPT路径的条件，我们应该能够自动为我们构建数据包。

### 计算最短路径

为了找到满足BPF指令中呈现条件的数据包的最短路径，我们需要跟踪那些没有以不利条件结束的路径。

我们首先创建一个小的队列。这个队列包含几个重要的数据点：

- 指向下一条指令的指针。
- 我们当前已执行的指令路径 + 下一条指令。

指向下一条指令的指针。

我们当前已执行的指令路径 + 下一条指令。

每当我们遇到检查条件的指令时，我们使用布尔值跟踪结果并将其存储在队列中，这样我们就可以在达到ACCEPT条件之前比较路径上的条件数量，并计算最短路径。用伪代码可以最好地表达为：

```Python
paths = []
queue = dequeue([(0, [0])])

while queue:
	pc, path = queue.popleft()

	if pc >= len(instructions):
            continue

instruction = instructions[pc]
	
	if instruction.class == return_instruction:
		if instruction_constant != 0:  # accept
			paths.append(path)
		continue  # drop or accept, stop parsing this instruction

if instruction.class == jump_instruction:
	if instruction.operation == unconditional_jump:
		next_pc = pc + 1 + instruction_constant
		queue.append((next_pc, path + [next_pc]))
		continue

	# Conditional jump, explore both
	pc_true = pc + 1 + instruction.jump_true
	pc_false = pc + 1 + instruction.jump_false
	
	if instruction.jump_true <= instruction.jump_false:
		queue.append((pc_true, path + [pc_true]))
		queue.append((pc_false, path + [pc_false]))
	# else: same as above but reverse order of appending
# else: sequential instruction, append to the queue
```

如果我们针对之前的BPFDoor示例执行此逻辑，将得到通往被接受数据包的最短路径：

```Rust
(000) code=0x28 jt=0 jf=0  k=0xc     ; 读取偏移量12处的半字（EtherType）
(001) code=0x15 jt=0 jf=4  k=0x86dd  ; IPv6数据包
(002) code=0x30 jt=0 jf=0  k=0x14    ; 读取偏移量20处的字节（协议）
(003) code=0x15 jt=0 jf=11 k=0x11    ; 协议号17 (UDP)
(004) code=0x28 jt=0 jf=0  k=0x38    ; 读取偏移量56处的字（目标端口）
(005) code=0x15 jt=8 jf=9  k=0x35    ; 目标端口53
(014) code=0x06 jt=0 jf=0  k=0x40000 ; 接受
```

在分析BPF指令并找出后门接受的数据包外观时，这已经是一个有用的自动化工具，用于自动解决我们的BPF约束。但是，如果我们能更进一步呢？

如果我们能创建一个小工具，以自动化方式返回预期的数据包呢？

## 运用Z3和scapy

`Z3`正是解决给定一组约束问题的完美工具。该工具由微软开发，被标记为定理证明器，并提供了易于使用的函数，在底层执行非常复杂的数学运算。

我们将用于制作有效魔法数据包的另一个工具是scapy，这是一个用于交互式数据包操作的流行Python库。

鉴于我们已经有了确定被接受数据包路径的方法，剩下的就是独立解决这个问题，然后将这个解决方案转换为网络数据包中各自偏移量处的字节。

### 符号执行

探索给定程序中执行路径的一种常用技术称为符号执行。对于这种技术，我们提供可用作变量的输入，包括约束条件。通过了解成功路径的结果，我们可以编排我们的工具来找到所有这些成功路径，并以情境化的格式向我们展示最终结果。

为此，我们需要实现一个小型机器，能够跟踪诸如常量、寄存器和不同布尔运算符等状态，这些状态是正在检查的条件的结果。

```Python
class BPFPacketCrafter:
    MIN_PKT_SIZE = 64           # 最小数据包大小（以太网 + IP + UDP 头部）
    LINK_ETHERNET = "ethernet"  # DLT_EN10MB - 以以太网头部开始
    LINK_RAW = "raw"            # DLT_RAW - 直接以IP头部开始
    MEM_SLOTS = 16              # 暂存内存槽数量（M[0] 到 M[15]）

    def __init__(self, ins: list[BPFInsn], pkt_size: int = 128, ltype: str = "ethernet"):
        self.instructions = ins
        self.pkt_size = max(self.MIN_PKT_SIZE, pkt_size)
        self.ltype = ltype

        # 符号化数据包字节
        self.packet = [BitVec(f"pkt_{i}", 8) for i in range(self.pkt_size)]

        # 符号化寄存器（32位）
        self.A = BitVecVal(0, 32)  # 累加器
        self.X = BitVecVal(0, 32)  # 索引寄存器

        # 暂存内存 M[0-15]（32位字）
        self.M = [BitVecVal(0, 32) for _ in range(self.MEM_SLOTS)]
```

通过上述代码，我们已经涵盖了在符号执行期间保持状态所需的大部分机器。当然，还有更多我们需要跟踪的条件，但这些会在求解过程中处理。为了处理ADD指令，机器将BPF操作映射到Z3加法：

```Python
def _execute_ins(self, insn: BPFInsn):
    cls = insn.cls
    if cls == BPFClass.ALU:
        op = insn.op
        src_val = BitVecVal(insn.k, 32) if insn.src == BPFSrc.K else self.X
        if op == BPFOp.ADD:
            self.A = self.A + src_val
```

幸运的是，BPF指令集只是一个相对容易实现的小指令集——只需要跟踪两个寄存器绝对是一个受欢迎的约束！

这种符号执行的总体工作原理可以概括为以下抽象概述：

- 将“x”（索引）和“a”（累加器）寄存器初始化为其基本状态。
- 循环遍历从被识别为成功路径的路径中获取的指令；按原样执行非跳转指令，跟踪寄存器状态。确定是否遇到跳转指令，并检查是否应执行分支。
- 使用Z3的check()函数检查在给定约束（ACCEPT）下我们的条件是否已满足。
- 将Z3位向量数组转换为字节。
- 使用scapy根据转换后的字节构造数据包。

将“x”（索引）和“a”（累加器）寄存器初始化为其基本状态。

循环遍历从被识别为成功路径的路径中获取的指令；

- 按原样执行非跳转指令，跟踪寄存器状态。
- 确定是否遇到跳转指令，并检查是否应执行分支。

按原样执行非跳转指令，跟踪寄存器状态。

确定是否遇到跳转指令，并检查是否应执行分支。

使用Z3的check()函数检查在给定约束（ACCEPT）下我们的条件是否已满足。

将Z3位向量数组转换为字节。

使用scapy根据转换后的字节构造数据包。

如果我们查看Z3求解器构建的约束，我们可以追踪Z3为构建数据包字节所采取的执行步骤：

```Rust
[If(Concat(pkt_12, pkt_13) == 0x800,
    pkt_14 & 0xF0 == 0x40,
    True),
 If(Concat(pkt_12, pkt_13) == 0x800, pkt_14 & 0x0F >= 5, True),
 If(Concat(pkt_12, pkt_13) == 0x800, pkt_14 & 0x0F == 5, True),
 If(Concat(pkt_12, pkt_13) == 0x86DD,
    pkt_14 & 0xF0 == 0x60,
    True),
 0x86DD == ZeroExt(16, Concat(pkt_12, pkt_13)),
 0x11 == ZeroExt(24, pkt_20),
 0x35 == ZeroExt(16, Concat(pkt_56, pkt_57))]
```

Z3显示的约束的第一部分是添加的约束，以确保在处理链路层BPF指令时我们正在构建一个有效的以太网IP数据包。“If”语句根据检测到的协议应用特定的约束：

- IPv4逻辑（0x0800）：pkt_14 & 240 == 64：字节14是IP头部的开始。0xF0掩码隔离高半字节（版本字段）以检查版本是否为4（0x40）。pkt_14 & 15 == 5：15（0x0F），隔离低半字节（IHL - 互联网头部长度）。这强制要求头部长度为5（20字节），这是没有选项时的标准大小。
- IPv6逻辑（0x86dd）：pkt_14 & 240 == 0x60：检查版本字段是否为版本6（0x60）

IPv4逻辑（0x0800）：

- pkt_14 & 240 == 64：字节14是IP头部的开始。0xF0掩码隔离高半字节（版本字段）以检查版本是否为4（0x40）。
- pkt_14 & 15 == 5：15（0x0F），隔离低半字节（IHL - 互联网头部长度）。这强制要求头部长度为5（20字节），这是没有选项时的标准大小。

pkt_14 & 240 == 64：字节14是IP头部的开始。0xF0掩码隔离高半字节（版本字段）以检查版本是否为4（0x40）。

pkt_14 & 15 == 5：15（0x0F），隔离低半字节（IHL - 互联网头部长度）。这强制要求头部长度为5（20字节），这是没有选项时的标准大小。

IPv6逻辑（0x86dd）：

- pkt_14 & 240 == 0x60：检查版本字段是否为版本6（0x60）

pkt_14 & 240 == 0x60：检查版本字段是否为版本6（0x60）

当我们查看第二部分，其中正在检查不同的值时，我们可以观察到网络数据包的值：

- 0x86DD：IPv6头部的数据包条件。
- 0x11：UDP协议号。
- 0x35：目标端口（53）。

0x86DD：IPv6头部的数据包条件。

0x11：UDP协议号。

0x35：目标端口（53）。

除了期望值之外，我们还可以看到它应该存在于给定数据包中的字节偏移量（例如pkt_12，pkt_13）。

### 制作数据包

既然我们已经确定了哪些字节应该存在于特定的偏移量处，我们就可以使用scapy将其转换为实际的网络数据包。如果我们根据之前Z3约束的字节生成一个新的数据包，我们可以清楚地看到我们的数据包会是什么样子，并将其存储以供进一步处理：

```Python
###[ Ethernet ]###
  dst       = 00:00:00:00:00:00
  src       = 00:00:00:00:00:00
  type      = IPv6                 <-- IPv6 数据包
###[ IPv6 ]###
     version   = 6
     tc        = 0
     fl        = 0
     plen      = 0
     nh        = UDP               <-- UDP 协议
     hlim      = 0
     src       = ::
     dst       = ::
###[ UDP ]###
        sport     = 0
        dport     = domain         <-- 端口 53
        len       = 0
        chksum    = 0x0
```

这些新制作的数据包反过来可以用于进一步研究，或通过扫描网络来识别这些植入物的存在。

## 亲自尝试

理解一组特定的BPF指令在做什么可能是一项繁琐且耗时的工作。使用的示例总共只有十六条指令，但我们遇到过超过200条指令的样本，要理解它们至少需要一天时间。通过使用Z3求解器，我们现在可以将这个时间减少到几秒钟，不仅可以显示被接受数据包的路径，还可以显示其数据包骨架。

我们开源了`filterforge`工具，以帮助社区自动化解构基于BPF的植入程序。您可以在我们的GitHub仓库中找到源代码及使用示例。

通过发布这项研究并分享我们用于减少分析师解析BPF指令所耗时间的工具，我们希望激发更多人开展进一步研究，拓展此类自动化形式。

---

> 本文由AI自动翻译，原文链接：[From bytecode to bytes- automated magic packet generation](https://blog.cloudflare.com/from-bpf-to-packet/)
> 
> 翻译时间：2026-04-09 04:38
