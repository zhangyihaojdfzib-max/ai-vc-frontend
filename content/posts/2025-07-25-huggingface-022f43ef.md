---
title: 欢迎使用 `hf`：更快、更友好的 Hugging Face CLI
title_original: 'Say hello to `hf`: a faster, friendlier Hugging Face CLI ✨'
date: '2025-07-25'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/hf-cli
author: ''
summary: Hugging Face 宣布将其命令行工具从 `huggingface-cli` 更名为 `hf`，旨在提供更简洁、更符合人体工程学的使用体验。新版本遵循
  `hf <资源> <操作>` 的清晰模式，重构了命令结构，将常用功能如上传、下载置于根级别，并优化了身份验证等子命令的组织方式。此次更新不仅提升了日常操作的效率，也为未来功能的扩展奠定了基础。用户可通过升级
  `huggingface_hub` 库来体验新版 CLI。
categories:
- AI基础设施
tags:
- Hugging Face
- 命令行工具
- 开发者工具
- 模型管理
- 开源
draft: false
translated_at: '2026-02-27T04:37:49.370960'
---

# 欢迎使用 `hf`：更快、更友好的 Hugging Face CLI ✨

我们很高兴宣布一项期待已久的使用体验改进：Hugging Face CLI 已正式从 `huggingface-cli` 更名为 `hf`！

那么……为什么要做这个改变呢？

频繁输入 `huggingface-cli` 很快就会让人感到繁琐。更重要的是，随着时间的推移，新功能（上传、下载、缓存管理、仓库管理等）的加入使得 CLI 的命令结构变得混乱。重命名 CLI 是一个机会，可以将命令重新组织成更清晰、更一致的格式。

我们决定不重复造轮子，而是遵循一个广为人知的 CLI 模式：`hf <资源> <操作>`。这种可预测的语法使 Hugging Face CLI 更符合人体工程学且更易于探索，同时也为即将推出的功能奠定了基础。

## 开始使用

要开始体验新的 CLI，你需要安装最新版本的 `huggingface_hub`：

```
pip install -U huggingface_hub
```

并重新加载你的终端会话。要测试安装是否成功，请运行 `hf version`：

```
➜ hf version
huggingface_hub version: 0.34.0
```

接下来，让我们通过 `hf --help` 来探索新的语法：

```
➜ hf --help
usage: hf <command> [<args>]

positional arguments:
  {auth,cache,download,jobs,repo,repo-files,upload,upload-large-folder,env,version,lfs-enable-largefiles,lfs-multipart-upload}
                        hf command helpers
    auth                管理身份验证（登录、登出等）。
    cache               管理本地缓存目录。
    download            从 Hub 下载文件。
    jobs                在 Hub 上运行和管理 Jobs。
    repo                管理 Hub 上的仓库。
    repo-files          管理 Hub 上仓库中的文件。
    upload              上传文件或文件夹到 Hub。推荐用于单次提交上传。
    upload-large-folder
                        上传大型文件夹到 Hub。推荐用于可恢复的上传。
    env                 打印环境信息。
    version             打印 hf 版本信息。

options:
  -h, --help            show this help message and exit
```

如我们所见，命令按"资源"分组（`hf auth`、`hf cache`、`hf repo` 等）。我们还将 `hf upload` 和 `hf download` 放在了根级别，因为它们预计是最常用的命令。

要深入了解任何命令组，只需附加 `--help`：

```
➜ hf auth --help
usage: hf <command> [<args>] auth [-h] {login,logout,whoami,switch,list} ...

positional arguments:
  {login,logout,whoami,switch,list}
                        身份验证子命令
    login               使用来自 huggingface.co/settings/tokens 的令牌登录
    logout              登出
    whoami              查看你当前登录的 huggingface.co 账户。
    switch              在访问令牌之间切换
    list                列出所有存储的访问令牌

options:
  -h, --help            show this help message and exit
```

## 🔀 迁移

如果你习惯了 `huggingface-cli`，大多数命令看起来会很熟悉。最大的变化影响身份验证：

```bash
huggingface-cli login

hf auth login
```

```bash
huggingface-cli whoami

hf auth whoami
```

```bash
huggingface-cli logout

hf auth logout
```

所有 `auth` 命令都已与现有的 `hf auth switch`（用于在不同本地配置文件之间切换）和 `hf auth list`（用于列出本地配置文件）分组在一起。

旧的 `huggingface-cli` 仍然保持活跃且功能完整。我们保留它是为了便于过渡。如果你使用旧版 CLI 的任何命令，你会看到一个警告，指引你使用新的 CLI 等效命令：

```bash
➜ huggingface-cli whoami
⚠️  警告：'huggingface-cli whoami' 已弃用。请使用 'hf auth whoami'。
Wauplin
orgs:  huggingface,competitions,hf-internal-testing,templates,HF-test-lab,Gradio-Themes,autoevaluate,HuggingFaceM4,HuggingFaceH4,open-source-metrics,sd-concepts-library,hf-doc-build,hf-accelerate,HFSmolCluster,open-llm-leaderboard,pbdeeplinks,discord-community,llhf,sllhf,mt-metrics,DDUF,hf-inference,changelog,tiny-agents
```

## 还有一件事…… 💥 `hf jobs`

我们忍不住要推出我们的第一个专用命令：`hf jobs`。

Hugging Face Jobs 是一项新服务，让你可以使用你选择的硬件类型，在 Hugging Face 基础设施上运行任何脚本或 Docker 镜像。计费方式是"按需付费"，意味着你只需为使用的秒数付费。以下是启动你的第一个命令的方法：

```bash
hf jobs run --flavor=a10g-small ubuntu nvidia-smi
```

该 CLI 深受 Docker 熟悉命令的启发：

```bash
➜ hf jobs --help
usage: hf <command> [<args>] jobs [-h] {inspect,logs,ps,run,cancel,uv} ...

positional arguments:
  {inspect,logs,ps,run,cancel,uv}
                        huggingface.co jobs 相关命令
    inspect             显示一个或多个 Job 的详细信息
    logs                获取 Job 的日志
    ps                  列出 Jobs
    run                 运行一个 Job
    cancel              取消一个 Job
    uv                  在 HF 基础设施上运行 UV 脚本（带有内联依赖的 Python）

options:
  -h, --help            show this help message and exit
```

通过阅读指南了解更多关于 Jobs 的信息。

Hugging Face Jobs 仅对 Pro 用户以及 Team 或 Enterprise 组织开放。升级你的计划以开始使用！

---

> 本文由AI自动翻译，原文链接：[Say hello to `hf`: a faster, friendlier Hugging Face CLI ✨](https://huggingface.co/blog/hf-cli)
> 
> 翻译时间：2026-02-27 04:37
