---
title: DNS记录顺序之惑：CNAME与A记录孰先孰后？
title_original: What came first- the CNAME or the A record
date: '2026-01-14'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/cname-a-record-order-dns-standards/
author: ''
summary: 本文探讨了2026年1月Cloudflare 1.1.1.1服务一次常规更新引发的全球DNS解析故障。故障根源在于代码优化改变了DNS响应中CNAME与A/AAAA记录的排序顺序，导致部分依赖“CNAME记录必须在前”这一隐含规则的客户端解析失败。文章深入分析了CNAME链的工作原理、代码变更细节，并揭示了DNS协议长达40年的模糊性——响应中记录的顺序并未被明确定义，而不同实现对此有不同预期。
categories:
- AI基础设施
tags:
- DNS
- Cloudflare
- 网络故障
- 协议规范
- 系统可靠性
draft: false
translated_at: '2026-01-15T04:43:27.212426'
---

# 先有CNAME还是先有A记录？

- Sebastiaan Neuteboom

2026年1月8日，一次旨在降低内存使用的1.1.1.1常规更新，意外引发了全球互联网用户的DNS解析故障浪潮。根本原因并非攻击或服务中断，而是我们DNS响应中记录顺序的微妙变化。

虽然大多数现代软件将DNS响应中的记录顺序视为无关紧要，但我们发现某些实现要求CNAME记录必须出现在所有其他记录之前。当这个顺序发生变化时，解析就开始失败。本文探讨了导致这一变化的代码修改、它为何破坏了特定的DNS客户端，以及那个让DNS响应"正确"顺序难以定义的40年协议模糊性。

所有时间戳均以协调世界时（UTC）为准。

记录重排序被引入1.1.1.1代码库

变更发布到测试环境

包含该变更的全球发布开始

发布覆盖90%服务器

发布被回滚

回滚完成，影响结束

在对缓存实现进行降低内存使用的改进时，我们引入了对CNAME记录顺序的微妙更改。该变更于2025年12月2日引入，12月10日发布到测试环境，并于2026年1月7日开始部署。

### DNS CNAME链的工作原理

当您查询像`www.example.com`这样的域名时，可能会得到一个CNAME（规范名称）记录，表明一个名称是另一个名称的别名。公共解析器（如1.1.1.1）的工作就是沿着这条别名链追踪，直到获得最终响应：

`www.example.com → cdn.example.com → server.cdn-provider.com → 198.51.100.1`

当1.1.1.1遍历此链时，它会缓存每个中间记录。链中的每个记录都有自己的TTL（生存时间），指示我们可以缓存多长时间。CNAME链中的所有TTL不必相同：

`www.example.com → cdn.example.com (TTL: 3600秒) # 仍被缓存`
`cdn.example.com → 198.51.100.1 (TTL: 300秒) # 已过期`

当CNAME链中的一个或多个记录过期时，它被视为部分过期。幸运的是，由于链的部分内容仍在缓存中，我们不必重新解析整个CNAME链——只需解析已过期的部分。在上面的例子中，我们会取仍然有效的`www.example.com → cdn.example.com`链，仅解析已过期的`cdn.example.com` A记录。完成后，我们将现有的CNAME链和新解析的记录合并为单个响应。

合并这两个链的代码正是变更发生的地方。此前，代码会创建一个新列表，插入现有的CNAME链，然后追加新记录：

```
impl PartialChain {
    /// Merges records to the cache entry to make the cached records complete.
    pub fn fill_cache(&self, entry: &mut CacheEntry) {
        let mut answer_rrs = Vec::with_capacity(entry.answer.len() + self.records.len());
        answer_rrs.extend_from_slice(&self.records); // CNAMEs first
        answer_rrs.extend_from_slice(&entry.answer); // Then A/AAAA records
        entry.answer = answer_rrs;
    }
}

```

然而，为了节省一些内存分配和复制操作，代码被更改为将CNAME追加到现有的答案列表中：

```
impl PartialChain {
        entry.answer.extend(self.records); // CNAMEs last
    }
}

```

结果，1.1.1.1返回的响应现在有时将CNAME记录放在底部，即最终解析答案之后。

### 为何造成影响

当DNS客户端收到答案部分包含CNAME链的响应时，它们也需要遵循此链来找出`www.example.com`指向`198.51.100.1`。一些DNS客户端实现通过顺序迭代记录时跟踪预期名称来处理此问题。当遇到CNAME时，更新预期名称：

```
;; QUESTION SECTION:
;; www.example.com.        IN    A

;; ANSWER SECTION:
www.example.com.    3600   IN    CNAME  cdn.example.com.
cdn.example.com.    300    IN    A      198.51.100.1

```

1. 查找`www.example.com`的记录
2. 遇到`www.example.com. CNAME cdn.example.com`
3. 查找`cdn.example.com`的记录
4. 遇到`cdn.example.com. A 198.51.100.1`

查找`www.example.com`的记录

遇到`www.example.com. CNAME cdn.example.com`

查找`cdn.example.com`的记录

遇到`cdn.example.com. A 198.51.100.1`

当CNAME突然出现在底部时，这就不再有效：

```
;; QUESTION SECTION:
;; www.example.com.	       IN    A

;; ANSWER SECTION:

```

2. 忽略`cdn.example.com. A 198.51.100.1`，因为它与预期名称不匹配
3. 遇到`www.example.com. CNAME cdn.example.com`
4. 查找`cdn.example.com`的记录
5. 没有更多记录，因此响应被视为空

忽略`cdn.example.com. A 198.51.100.1`，因为它与预期名称不匹配

没有更多记录，因此响应被视为空

一个因此受损的实现是glibc中的`getaddrinfo`函数，该函数在Linux上常用于DNS解析。查看其`getanswer_r`实现，我们确实可以看到它期望在任何答案之前找到CNAME记录：

```
for (; ancount > 0; --ancount)
  {
    // ... parsing DNS records ...
    
    if (rr.rtype == T_CNAME)
      {
        /* Record the CNAME target as the new expected name. */
        int n = __ns_name_unpack (c.begin, c.end, rr.rdata,
                                  name_buffer, sizeof (name_buffer));
        expected_name = name_buffer;  // Update what we're looking for
      }
    else if (rr.rtype == qtype
             && __ns_samebinaryname (rr.rname, expected_name)  // Must match!
             && rr.rdlength == rrtype_to_rdata_length (type:qtype))
      {
        /* Address record matches - store it */
        ptrlist_add (list:addresses, item:(char *) alloc_buffer_next (abuf, uint32_t));
        alloc_buffer_copy_bytes (buf:abuf, src:rr.rdata, size:rr.rdlength);
      }
  }

```

另一个值得注意的受影响实现是三款思科以太网交换机型号中的DNSC进程。当这些交换机被配置为使用1.1.1.1时，如果收到包含重新排序CNAME的响应，它们会经历自发的重启循环。思科已发布描述此问题的服务文档。

### 并非所有实现都会受损

大多数DNS客户端没有这个问题。例如，`systemd-resolved`首先将记录解析到有序集合中：

```
typedef struct DnsAnswerItem {
        DnsResourceRecord *rr; // The actual record
        DnsAnswerFlags flags;  // Which section it came from
        // ... other metadata
} DnsAnswerItem;

typedef struct DnsAnswer {
        unsigned n_ref;
        OrderedSet *items;
} DnsAnswer;

```

在遵循CNAME链时，它可以搜索整个答案集，即使CNAME记录没有出现在顶部。

1987年发布的RFC 1034定义了DNS协议的大部分行为，本应告诉我们CNAME记录的顺序是否重要。第4.3.1节包含以下文本：

如果请求递归服务且可用，对查询的递归响应将是以下之一：

- 查询的答案，可能前面带有一个或多个CNAME RR，这些RR指定了在寻找答案过程中遇到的别名。

虽然“可能作为前言”可以被解释为要求CNAME记录出现在所有其他记录之前，但它并未使用现代RFC用来表达要求的规范性关键词，例如MUST和SHOULD。这并非RFC 1034的缺陷，而仅仅是其年代久远的结果。标准化这些关键词的RFC 2119发布于1997年，比RFC 1034晚了10年。

在我们的案例中，我们最初确实按照规范实现了CNAME优先。然而，由于RFC中语言的模糊性，我们没有任何测试来确保该行为始终保持一致。

### 细微差别：消息部分中的RRset与RR

要理解为何存在这种模糊性，我们需要理解DNS术语中一个细微但重要的区别。

RFC 1034第3.6节将资源记录集（RRset）定义为具有相同名称、类型和类别的记录集合。对于RRset，规范对排序有明确说明：

> RRset中RR的顺序并不重要，无需由域名服务器、解析器或DNS的其他部分保留。

然而，RFC 1034并未明确说明消息部分如何与RRset相关联。尽管现代DNS规范表明消息部分确实可以包含多个RRset（例如带有签名的DNSSEC响应），但RFC 1034并未用这些术语描述消息部分。相反，它将消息部分视为包含独立的资源记录（RR）。

问题在于，RFC主要在RRset的上下文中讨论排序，但并未指定消息部分内不同RRset之间的相对顺序。模糊性正源于此。

RFC 1034第6.2.1节包含一个进一步展示这种模糊性的例子。它提到资源记录（RR）的顺序也不重要：

> 答案部分中RR的顺序差异并不重要。

然而，这个例子只展示了同一RRset内同一名称的两个A记录。它并未说明这是否适用于像CNAME和A记录这样的不同记录类型。

事实证明，这个问题不仅限于将CNAME记录放在其他记录类型之前。即使CNAME出现在其他记录之前，如果CNAME链本身顺序错乱，顺序解析仍然可能失败。考虑以下响应：

```
;; QUESTION SECTION:
;; www.example.com.              IN    A

;; ANSWER SECTION:
cdn.example.com.           3600  IN    CNAME  server.cdn-provider.com.
www.example.com.           3600  IN    CNAME  cdn.example.com.
server.cdn-provider.com.   300   IN    A      198.51.100.1

```

每个CNAME都属于不同的RRset，因为它们的所有者不同，因此关于RRset顺序不重要的声明在此并不适用。

然而，RFC 1034并未规定CNAME链必须以任何特定顺序出现。没有要求`www.example.com. CNAME cdn.example.com.`必须出现在`cdn.example.com. CNAME server.cdn-provider.com.`之前。使用顺序解析时，同样的问题会发生：

1.  查找`www.example.com`的记录
2.  忽略`cdn.example.com. CNAME server.cdn-provider.com.`，因为它与预期名称不匹配
3.  遇到`www.example.com. CNAME cdn.example.com`
4.  查找`cdn.example.com`的记录
5.  忽略`server.cdn-provider.com. A 198.51.100.1`，因为它与预期名称不匹配
6.  忽略`cdn.example.com. CNAME server.cdn-provider.com.`，因为它与预期名称不匹配
7.  忽略`server.cdn-provider.com. A 198.51.100.1`，因为它与预期名称不匹配

## 解析器应该怎么做？

RFC 1034第5节描述了解析器的行为。第5.2.2节专门说明了解析器应如何处理别名（CNAME）：

> 在大多数情况下，解析器在遇到CNAME时，只需在新名称处重新启动查询。

这表明解析器在响应中找到CNAME时，无论它出现在何处，都应重新启动查询。然而，区分不同类型的解析器很重要：

*   **递归解析器**，如1.1.1.1，是通过查询权威域名服务器来执行递归解析的完整DNS解析器。
*   **存根解析器**，如glibc的getaddrinfo，是简化的本地接口，将查询转发给递归解析器并处理响应。

RFC中关于解析器行为的章节主要是针对完整解析器编写的，而不是大多数应用程序实际使用的简化存根解析器。显然，一些存根解析器并未实现规范的某些部分，例如RFC中描述的CNAME重启逻辑。

## DNSSEC规范提供了对比

后来的DNS规范展示了定义记录排序的不同方法。定义DNSSEC协议修改的RFC 4035使用了更明确的语言：

> 当将签名的RRset放入答案部分时，域名服务器也必须将其RRSIG RR放入答案部分。RRSIG RR的包含优先级高于任何其他可能需要包含的RRset。

该规范使用了“MUST”，并明确为RRSIG记录定义了“更高的优先级”。然而，“更高的包含优先级”指的是RRSIG是否应包含在响应中，而不是它们应出现在何处。这为DNSSEC上下文中的记录包含提供了明确的实施指导，但并未强制规定记录排序的任何特定行为。

然而，对于未签名的区域，RFC 1034的模糊性仍然存在。“前言”一词指导了将近四十年的实现行为，但它从未被正式规定为一项要求。

## CNAME记录必须放在前面吗？

虽然根据我们的解读，RFC并未要求CNAME以任何特定顺序出现，但显然至少有一些广泛部署的DNS客户端依赖于此。由于使用这些客户端的系统可能更新不频繁，或者根本不更新，我们认为最好要求CNAME记录按顺序出现在任何其他记录之前。

基于在此次事件中学到的经验，我们已经恢复了CNAME的排序，并且不打算在未来更改顺序。

为防止未来发生任何事件或混淆，我们以互联网草案的形式撰写了一份提案，将在IETF进行讨论。如果就澄清后的行为达成共识，这将形成一份RFC，明确定义如何在DNS响应中正确处理CNAME，帮助我们和更广泛的DNS社区遵循协议。该提案可在https://datatracker.ietf.org/doc/draft-jabley-dnsop-ordered-answer-section找到。如果您有任何建议或反馈，我们非常乐意听取您的意见，最好通过IETF的DNSOP工作组提出。

> 本文由AI自动翻译，原文链接：[What came first- the CNAME or the A record](https://blog.cloudflare.com/cname-a-record-order-dns-standards/)
> 
> 翻译时间：2026-01-15 04:43
