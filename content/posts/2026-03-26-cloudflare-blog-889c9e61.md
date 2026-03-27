---
title: 一行K8s配置变更，年省600小时
title_original: A one-line Kubernetes fix that saved 600 hours a year
date: '2026-03-26'
source: Cloudflare Blog
source_url: https://blog.cloudflare.com/one-line-kubernetes-fix-saved-600-hours-a-year/
author: ''
summary: 文章介绍了作者团队在使用Kubernetes运行Atlantis（Terraform管理工具）时遇到的严重性能问题：每次重启Pod需要等待30分钟，导致每月超过50小时的工程时间被阻塞。通过深入调查，他们发现根本原因在于Kubernetes的一个安全默认配置与Atlantis持久化存储卷中数百万文件产生了性能瓶颈。最终，团队通过仅修改一行Kubernetes配置，彻底解决了重启缓慢的问题，预计每年可节省约600小时的工程时间。
categories:
- AI基础设施
tags:
- Kubernetes
- 性能优化
- DevOps
- 基础设施
- Terraform
draft: false
translated_at: '2026-03-27T05:09:43.161000'
---

# 一行Kubernetes配置变更，每年节省600小时

2026-03-26

- Braxton Schafer

![](/images/posts/1e4b31bfaf93.png)

每次重启Atlantis（我们用于规划和实施Terraform变更的工具）时，我们都要等待30分钟才能恢复运行。在此期间，所有由Atlantis管理的代码仓库都无法进行规划、实施或基础设施变更。由于凭证轮换和项目接入每月约需重启100次，这导致每月超过50小时的工程时间被阻塞，并且每次都会触发值班工程师的告警。

根本原因在于Kubernetes的一个安全默认配置——随着Atlantis使用的持久化存储卷增长到数百万个文件，该配置已悄然成为性能瓶颈。以下是我们如何定位问题并通过单行配置变更解决它的过程。

### 诡异的缓慢重启

我们使用Atlantis通过GitLab合并请求（MR）管理数十个Terraform项目，该工具负责规划与实施变更。它通过锁机制确保同一时间只有一个MR能修改项目。

Atlantis以单实例StatefulSet形式运行在Kubernetes上，依赖Kubernetes持久化存储卷（PV）在磁盘上跟踪仓库状态。每当需要接入或移除Terraform项目，或更新Terraform使用的凭证时，我们都必须重启Atlantis以加载变更——这个过程可能耗时30分钟。

最近Atlantis使用的持久化存储耗尽inode节点，迫使我们重启以扩容存储卷时，缓慢重启问题变得尤为明显。inode节点会被磁盘上的每个文件和目录条目消耗，文件系统可用inode数量由创建时传入的参数决定。我们的Kubernetes平台提供的Ceph持久化存储实现未提供向`mkfs`传递标志位的方法，因此我们只能依赖默认值：扩展文件系统是增加可用inode的唯一途径，而重启PV需要重启Pod。

我们曾考虑延长告警窗口，但这只会掩盖问题并延迟对实际故障的响应。最终我们决定深入调查耗时过长的根本原因。

### 异常行为分析

当需要滚动重启Atlantis以加载密钥变更时，我们会执行`kubectl rollout restart statefulset atlantis`，该命令会在启动新Pod前优雅终止现有Atlantis Pod。新Pod几乎立即出现，但查看时显示：

```Shell
$ kubectl get pod atlantis-0
atlantis-0                                                        0/1     
Init:0/1     0             30m
```

……那么问题出在哪里？首先自然是检查该Pod的事件。它正在等待初始化容器运行，或许Pod事件能揭示原因？

```Shell
$ kubectl events --for=pod/atlantis-0
LAST SEEN   TYPE      REASON                   OBJECT                   MESSAGE
30m         Normal    Killing                  Pod/atlantis-0   Stopping container atlantis-server
30m        Normal    Scheduled                Pod/atlantis-0   Successfully assigned atlantis/atlantis-0 to 36com1167.cfops.net
22s         Normal    Pulling                  Pod/atlantis-0   Pulling image "oci.example.com/git-sync/master:v4.1.0"
22s         Normal    Pulled                   Pod/atlantis-0   Successfully pulled image "oci.example.com/git-sync/master:v4.1.0" in 632ms (632ms including waiting). Image size: 58518579 bytes.
```

这看起来基本正常……但在调度Pod与实际开始拉取初始化容器镜像之间，为何存在如此长的延迟？遗憾的是，这是我们从Kubernetes本身能获取的全部数据。但必然存在其他信息能解释Pod实际启动耗时过长的原因。

### 深入探查

在Kubernetes中，每个节点上运行的`kubelet`组件负责协调Pod创建、挂载持久化存储卷等多项任务。根据我在Kubernetes团队的经验，`kubelet`以systemd服务形式运行，因此其日志应可在Kibana中查询。由于Pod已被调度，我们知道需要关注的主机名，且`kubelet`的日志消息包含关联对象，因此可通过过滤`atlantis`来缩小日志范围。

我们观察到Atlantis PV在Pod调度后不久即被挂载，所有密钥存储卷的挂载也未出现问题。但日志中仍存在大段未解释的时间间隔。我们看到：

```Rust
[operation_generator.go:664] "MountVolume.MountDevice succeeded for volume \"pvc-94b75052-8d70-4c67-993a-9238613f3b99\" (UniqueName: \"kubernetes.io/csi/rook-ceph-nvme.rbd.csi.ceph.com^0001-000e-rook-ceph-nvme-0000000000000002-a6163184-670f-422b-a135-a1246dba4695\") pod \"atlantis-0\" (UID: \"83089f13-2d9b-46ed-a4d3-cba885f9f48a\") device mount path \"/state/var/lib/kubelet/plugins/kubernetes.io/csi/rook-ceph-nvme.rbd.csi.ceph.com/d42dcb508f87fa241a49c4f589c03d80de2f720a87e36932aedc4c07840e2dfc/globalmount\"" pod="atlantis/atlantis-0"
[pod_workers.go:1298] "Error syncing pod, skipping" err="unmounted volumes=[atlantis-storage], unattached volumes=[], failed to process volumes=[]: context deadline exceeded" pod="atlantis/atlantis-0" podUID="83089f13-2d9b-46ed-a4d3-cba885f9f48a"
[util.go:30] "No sandbox for pod can be found. Need to start a new one" pod="atlantis/atlantis-0"
```

最后两条消息循环出现多次，直到最终观察到Pod正常启动。

由此可见`kubelet`认为Pod已准备就绪，但并未启动它，且某些操作正在超时。

### 关键线索

Pod的最低层级日志未能揭示问题本质。我们还能查看什么？在系统挂起前的最后一条消息是PV被挂载到节点。通常，如果PV挂载出现问题（例如因仍挂载在其他节点），会以事件形式向上传递。但此处仍有异常，唯一可深入排查的只剩PV本身。由于PV名称具有足够独特性，我将其作为搜索词输入Kibana……立即发现了关键信息：

```Rust
[volume_linux.go:49] Setting volume ownership for /state/var/lib/kubelet/pods/83089f13-2d9b-46ed-a4d3-cba885f9f48a/volumes/kubernetes.io~csi/pvc-94b75052-8d70-4c67-993a-9238613f3b99/mount and fsGroup set. If the volume has a lot of files then setting volume ownership could be slow, see https://github.com/kubernetes/kubernetes/issues/69699
```

还记得开头提到我们刚耗尽inode节点吗？换言之，该PV上存在海量文件。当PV挂载时，`kubelet`正在执行`chgrp -R`递归更改整个文件系统中每个文件和文件夹的所属组。难怪耗时如此之长——即使在高速闪存存储上，遍历如此巨量的条目也需要大量时间！

Pod的`spec.securityContext`中包含`fsGroup: 1`，这确保以GID 1运行的进程能访问存储卷上的文件。Atlantis以非root用户运行，若未设置此配置则无权读写PV。Kubernetes强制执行此机制的方式是：每次挂载PV时递归更新整个PV的所有权。

### 解决方案

修复过程惊人地……简单。自1.20版本起，Kubernetes在`pod.spec.securityContext`中支持名为`fsGroupChangePolicy`的附加字段。该字段默认值为`Always`，这正是我们所见行为的根源。它还有另一个选项`OnRootMismatch`，仅当PV根目录权限不正确时才更改权限。若不确定PV上的文件创建方式，请勿设置`fsGroupChangePolicy: OnRootMismatch`。我们确认PV中所有文件的所属组均不应被更改后，便设置了该字段：

```Rust
spec:
  template:
    spec:
      securityContext:
        fsGroupChangePolicy: OnRootMismatch
```

现在，Atlantis 的重启时间从最初的 30 分钟缩短到了大约 30 秒。

Kubernetes 的默认设置对于小容量数据是合理的，但随着数据增长，它们可能成为瓶颈。对我们而言，这一行针对 `fsGroupChangePolicy` 的改动，每月节省了近 50 小时的工程阻塞时间。这些时间原本是我们的团队等待基础设施变更完成所花费的，也是我们的值班工程师处理误报警报所消耗的。这个修复的诊断时间比部署时间还长，但它每年为我们找回了大约 600 小时用于高效工作的时间。

Kubernetes 的安全默认值是为小型、简单的工作负载设计的。但随着规模扩大，它们可能逐渐成为瓶颈。如果你运行的工作负载涉及大型持久卷，值得检查一下此类递归权限变更是否在悄无声息地吞噬你的重启时间。请审计你的 `securityContext` 设置，特别是 `fsGroup` 和 `fsGroupChangePolicy`。`OnRootMismatch` 自 v1.20 版本起已可用。

并非每个修复都需要惊天动地或复杂无比，通常值得问一句：“系统为什么会有这种行为？”

如果你对大规模调试基础设施问题感兴趣，我们正在招聘。欢迎加入我们的 [Cloudflare 社区](https://community.cloudflare.com/) 或 [Discord](https://discord.com/invite/cloudflaredev) 来交流技术。

---

> 本文由AI自动翻译，原文链接：[A one-line Kubernetes fix that saved 600 hours a year](https://blog.cloudflare.com/one-line-kubernetes-fix-saved-600-hours-a-year/)
> 
> 翻译时间：2026-03-27 05:09
