---
title: 微软开源高性能内存分配器mimalloc
title_original: mimalloc: A new, high-performance, scalable memory allocator for the
  modern era - Microsoft Research
date: '2026-05-13'
source: Microsoft Research
source_url: https://www.microsoft.com/en-us/research/blog/mimalloc-a-high-performance-scalable-memory-allocator-for-the-modern-era/
author: ''
summary: 微软研究院开发的开源内存分配器mimalloc，专为高并发和大内存场景设计，可直接替代malloc和free。它采用线程本地堆和原子操作减少争用，代码仅约12K行，已在Bing、Unreal
  Engine等大型服务中显著提升性能。mimalloc支持多平台，并作为NoGIL CPython的分配器，适用于从数百GB内存服务到游戏引擎的广泛场景。
categories:
- AI基础设施
tags:
- mimalloc
- 内存分配器
- 微软研究院
- 高并发
- 开源
draft: false
translated_at: '2026-05-14T05:49:29.207001'
---

## 概览

- 当今的关键服务和应用程序通常具有高度并发性，使用数百个线程。它们还运行在大型内存规模下，通常达到数百GB，尤其是在使用大语言模型时。
- mimalloc 是一个开源、现代、可扩展的内存分配器，是 malloc 和 free 的直接替代品。它相对较小（约12K行代码），具有清晰的内部数据结构，易于构建并集成到其他项目中。它提供了有界的最坏情况分配时间（最高到操作系统原语）、有界的空间开销、低内部碎片，并且几乎完全依赖原子操作来最小化争用。
- mimalloc 可在 GitHub（在新标签页中打开）上获取，并拥有超过12K颗星。

## mimalloc

在微软研究院（MSR）的 RiSE 小组，我们从事形式化方法、编程语言和软件工程（包括新兴的 Agent（智能体）系统）的基础研究，特别关注那些可以证明正确、安全且高性能的系统。mimalloc 内存分配器最初于2020年设计，作为 RiSE 开发的先进 Lean（在新标签页中打开）和 Koka（在新标签页中打开）编程语言的快速分配器，这两种语言都使用了新颖的编译器引导引用计数（参见 Perceus）。

mimalloc 的可扩展设计也被证明在微软的大型服务中表现极其出色。通过与产品团队的密切合作，mimalloc 显著改善了诸如 Bing 等服务的响应时间。如今，mimalloc 被广泛应用于微软内外的大型服务和应用程序中。它是 NoGIL CPython 3.13+ 的分配器，已集成到 Unreal Engine 中，并用于《死亡搁浅》等游戏。

该项目在 GitHub 上开源，拥有超过12K颗星。仅其 Rust 封装每天就有超过10万次下载。

mimalloc 在广泛的场景中都很有效；从 Koka 或 Lean 等小规模应用程序，到内存占用超过500 GiB 且拥有数百个线程的大型服务。

尽管应用范围如此广泛，其代码库仍然紧凑，大约有12K行 C 代码。反映其研究起源，mimalloc 强调具有强不变量的清晰内部数据结构，使其比许多行业分配器更容易理解和推理。正如 Fred Brooks 在其著名著作《人月神话》中已经指出的那样："给我看你的流程图，隐藏你的表格，我仍然会感到困惑。给我看你的表格，我就不需要你的流程图了；那将是显而易见的。"

因此，mimalloc 已被移植到许多平台——Windows、macOS、Linux、FreeBSD、NetBSD、DragonFly 以及各种游戏主机——并且易于构建和集成到其他项目中。例如，清晰的数据结构使 Sam Gross 等人能够采用 mimalloc 作为 NoGIL CPython 的并发分配器。这种设计也使得在其之上实现循环垃圾回收相对简单。

## 快速路径

与其他可扩展分配器（如 tcmalloc 和 jemalloc）一样，mimalloc 的一个核心设计原则是每个线程维护自己的线程本地堆，我们称之为"theap"。每个 theap 拥有一组 mimalloc "页"，通常为64 KiB。每个 mimalloc 页包含固定大小的块，按大小类别组织以减少内部碎片。通过为每个线程提供自己的 theap 和一组 mimalloc 页，内存分配和释放通常无需同步即可进行。仅当线程释放由另一个线程分配的块时才需要原子操作。

此外，在实践中，大多数分配都非常小，通常小于1 KiB。对于这样的小分配，mimalloc 提供了一个快速路径，其主要分配函数如下所示：

```
void* mi_malloc( size_t size )  
{ 
  mi_theap_t* const theap = mi_get_thread_local_theap(); 
  if (size > MI_MAX_SMALL_SIZE) return mi_malloc_generic(theap,size);  // 慢速通用路径 
 
  const size_t index = (size + sizeof(void*))/sizeof(void*);           // 四舍五入大小 
  mi_page_t* const page = theap->small_pages[index];                    
 
  mi_block_t* const block = page->free;                                // 空闲列表头部 
  if (block == NULL) return mi_malloc_generic(theap,size);             // 慢速通用路径 
 
  page->free = block->next;                                            // 弹出空闲列表 
  page->used++;                                        
  return block; 
}
```

通过使用线程本地 theap，我们不需要任何原子操作或线程同步。我们还尝试最小化分支数量。特别是，线程本地 theap 永远不会是 NULL，我们用一个所有页都为空的特殊空 theap 来初始化它。这样，我们就不需要单独检查 theap 是否为 NULL。类似地，small_pages 数组中的指针永远不会是 NULL，我们再次使用特殊的空页（page->free==NULL）来避免单独检查。最后，页使用空闲列表而不是单独的 bump 指针进行初始化，避免了特殊情况，并通过简单地从空闲列表中弹出块来实现分配。在 x64 上，此代码现在转换为仅包含两个不常见分支的几条指令：

```
mi_malloc: 
  movq %rdi, %rsi             ; rsi = size
  movq _mi_theap_default@GOTTPOFF(%rip), %rax 
  movq %fs:(%rax), %rdi       ; rdi = thread local theap
  cmpq $1024, %rsi            ; size > MI_MAX_SMALL_SIZE?
  ja .LBB0_generic

  leaq 7(%rsi), %rax          ; 四舍五入到 sizeof(void*)
  andq $-8, %rax
  movq 232(%rdi,%rax), %rcx   ; rcx = heap->small_pages[index]
  movq 8(%rcx), %rax          ; block = rax = page->free
  testq %rax, %rax            ; block == NULL?
  je .LBB0_generic
  
  movq (%rax), %rdx           ; page->free = block->next
  movq %rdx, 8(%rcx)
  incw 16(%rcx)               ; page->used++
  retq 

.LBB0_generic:
  jmp _mi_malloc_generic@PLT  ; 尾调用 

```

类似地，mimalloc 为释放块提供了快速路径。在实践中，大多数块由分配该块的同一线程释放。我们可以通过检查当前线程 ID 是否与相应 mimalloc 页中存储的线程 ID 匹配来优化这种情况。如果匹配，我们可以直接将块推送到页的空闲列表上，而无需原子操作或锁：

```
void mi_free(void* p)  
{ 
  mi_page_t* const page = mi_ptr_page(p);         // 获取包含 p 的页元数据 
  if (page==NULL) return; 
 
  if (mi_thread_id() == page->thread_id) {        // 我们拥有这个页吗？ 
    mi_block_t* const block = (mi_block_t*)p; 
    block->next = page->local_free;               // 推送到 `local_free` 列表上 
    page->local_free = block;                      
    if (--page->used == 0) mi_page_free(page);    // 整个页都空闲了吗？ 
  } 
  else { 
    mi_free_cross_thread(page, p);                // 在另一个线程拥有的页中释放 
  } 
} 
```

最新 mimalloc v3 中的 mi_ptr_page 函数使用按需分配的整个内存映射来检索页元数据。在早期版本中，这通过对齐技巧更快。然而，在实践中，当全局覆盖 free 时，无效指针经常被传递给 mi_free。

使用单独的映射可以高效地检测此类情况，并在指针无效时返回 NULL。特别是，mi_ptr_page(NULL) == NULL，这通过仅测试 page 是否为 NULL 来避免额外的分支。此外，used 计数用于高效检测页中所有块何时已被释放。

当跨线程释放块时，我们进入 mi_free_cross_thread 函数——这是第一个需要原子操作的路径：

```c
void mi_free_cross_thread(mi_page_t* page, mi_block_t* block)  
{ 
  mi_block_t* tfree = mi_atomic_load(&page->thread_free);  // 线程空闲列表的头部
  do { 
    block->next = tfree;                                   // 将我们的块插入到前面
  } while (!mi_atomic_compare_and_swap(&page->thread_free, &tfree /*期望值*/, block /*新值*/))  
}
```

该块可以通过将其推入页面的线程空闲列表来释放。由于这是多线程操作，需要使用原子比较并交换操作来原子地推送该块。尽管如此，在现代硬件上，当无竞争时，此类操作是高效的，因为它们的操作与缓存一致性协议（MOESI）集成在一起。

播客系列

## AI测试与评估：来自科学与工业界的经验

了解微软如何借鉴其他领域的经验，将评估和测试作为AI治理的支柱加以推进。

## 空闲列表混乱

每个页面有三个空闲列表：用于分配的空闲列表、用于已释放块的`local_free`列表，以及用于跨线程释放的块的`thread_free`（原子操作）列表。这保证了在固定次数的分配之后，空闲列表会被耗尽，从而确保我们偶尔会走较慢的通用分配路径。这也用于通过将线程本地和本地空闲列表移回主空闲列表来清理空闲列表。（注意：实际实现需要更谨慎地处理拥有线程不再分配或被长时间阻塞的情况。）

因此，mimalloc在每个（64 KiB）mimalloc页面上有三个空闲列表，这实际上意味着一个程序可以轻松拥有数千个空闲列表。这对于mimalloc的可扩展性和缓存局部性至关重要。

![一棵高度平衡的树](/images/posts/08aa8b87cfc7.png)

![一棵随机化的树](/images/posts/e9b29499a19a.jpg)

对于这种设计，我们从随机化算法中获得了灵感。例如，为了平衡一棵二叉树，我们可以使用基于权重或深度的智能策略，并执行特定的旋转来保持其平衡。这类算法通常相当复杂。然而，我们也可以简化过程，在插入时随机决定分割点，并且纯粹靠概率，我们最终也能得到足够平衡的树。

类似地，许多多线程分配器依赖复杂的并发数据结构来同步对共享空闲列表的访问。相比之下，mimalloc使用了每页的线程空闲列表，任何线程都可以通过简单的原子比较并交换操作来推送一个块。

因为有数千个这样的列表，多个线程同时向同一页面释放块的概率很低。因此，大多数推送操作都是无竞争的原子更新。

通过将这些列表按每64 KiB的mimalloc页面组织，缓存局部性得到了改善，因为分配倾向于停留在同一页面内直到该页面被填满，而不管其他页面中已释放的对象。

相比之下，考虑一种每个线程或进程只有一个空闲列表的设计。当在释放相同大小的对象的同时分配新结构时（这是树变换等工作负载中的常见模式），分配可能会重用最近释放的、散布在内存各处的块，从而导致局部性降低。

## 线程间的共享

可扩展性与线程间高效内存共享之间存在根本性的矛盾。为了达到最佳的可扩展性，我们会让每个线程独占其自己的页面，以最大限度地减少线程同步。另一方面，这可能导致内存浪费：假设一个线程有大量空闲块，而另一个线程需要分配该大小的块——如果无法共享或窃取这些页面，我们就需要分配新的内存。在另一个极端，我们可以通过单个锁在所有线程之间共享所有页面：此时内存使用是最优的，但我们不再具有可扩展性。以下基准测试结果说明了这一矛盾：

![1.1倍提交，总计56 GiB](/images/posts/85278aff023f.png)

![4倍提交，总计262 GiB](/images/posts/8700811ebcc5.png)

![1.3倍提交，总计262 GiB](/images/posts/13b4ed785679.png)

该基准测试使用Windows线程池（约800个活动线程）在固定时间内运行许多任务。这些任务在分配、释放和短暂的阻塞期之间交替进行，模拟典型的服务工作负载。在图表中，蓝线代表总存活数据，而红线代表分配器提交的总内存。理想情况是红线尽可能接近蓝线。第一个图表几乎就是这种情况，它使用了标准的系统分配器：结束时提交的内存仅比存活数据多1.1倍——这是一个极好的结果！然而，在基准测试期间，它总共只分配了56 GiB数据。

与之对比，第二个图表中的另一个高度并发的分配器在基准测试期间能够分配262 GiB——几乎是前者的4倍。然而，它提交的内存也比存活数据多了4倍。在内存占用更大的实际工作负载中，这样的比率很快就会变得不可接受。这里我们看到标准分配器的可扩展性没那么好，但展现了更好的跨线程内存共享。

最后一个图表显示了最新的mimalloc分配器。与第二个分配器一样，它在基准测试期间分配了262 GiB，同时将提交内存降低到存活数据的1.3倍，从而实现了可扩展性和线程间高效的内存共享。类似于现代线程池实现中的工作窃取，mimalloc使用了一种“页面窃取”技术，允许线程在不进行昂贵的跨线程同步的情况下获取页面的所有权。

这些改进是与微软Azure Cosmos DB团队密切合作完成的。精确的描述超出了本文的范围，但我们很快会发布一份技术报告——敬请期待。

## 关于作者

### Daan Leijen

首席研究员

---

> 本文由AI自动翻译，原文链接：[mimalloc: A new, high-performance, scalable memory allocator for the modern era - Microsoft Research](https://www.microsoft.com/en-us/research/blog/mimalloc-a-high-performance-scalable-memory-allocator-for-the-modern-era/)
> 
> 翻译时间：2026-05-14 05:49
