---
title: 将GitHub CI迁移到Hugging Face Jobs
title_original: Migrating Your GitHub CI to Hugging Face Jobs
date: '2026-06-09'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/github-ci-hf-jobs
author: ''
summary: 本文介绍了如何将GitHub Actions的CI任务迁移到Hugging Face Jobs上运行，以解决GitHub托管运行器速度慢、缺乏GPU支持等问题。通过使用huggingface/jobs-actions桥接器，用户可以在HF
  Jobs上启动临时自托管运行器，实现CPU和GPU任务的灵活调度。文章详细说明了架构流程、调度器Space的创建步骤，并指出该方案可将CPU任务CI时间缩短约30%，并支持在真实GPU硬件上运行测试套件。
categories:
- AI基础设施
tags:
- GitHub Actions
- Hugging Face Jobs
- CI/CD
- GPU
- 自托管运行器
draft: false
translated_at: '2026-06-10T06:25:15.125062'
---

# 将你的 GitHub CI 迁移到 Hugging Face Jobs

如果你有一个 GitHub 仓库并启用了 GitHub Actions，你很可能使用 GitHub 托管的运行器进行 CI。这是许多项目的默认选择，因为它很简单：添加一个工作流，写入 `runs-on: ubuntu-latest`，GitHub 就会给你一台机器。

这个默认设置很方便，但也有其局限性。GitHub Actions 可能运行缓慢或因维护而停机，托管的机器是通用的，而且 GPU 访问并非大多数开源项目可以随意开启的。对于 Trackio 来说，这些限制开始变得重要。我们既需要可靠的 CPU CI 来进行基础单元测试和前端检查，也需要 GPU CI 来运行需要在真实 CUDA 硬件上执行的测试。

因此，我们构建了一个替代方案：让 GitHub Actions 负责 CI，但在 Hugging Face Jobs 上运行任务。

结果：Trackio 的 CI 现在运行在 Hugging Face Jobs 上，并实时回传日志，将 CPU 任务的 CI 时间缩短了约 30%，并启用了一套全新的在 GPU 机器上运行的测试套件！

在本文中，我们将逐步解释如何为你的 GitHub 仓库重现相同的设置。如果你正在使用 Agent（智能体），你可以将本文指向它，因为我们同时提供了 CLI 指令和面向我们人类的基于浏览器的操作说明。

让我们先快速介绍一下 Hugging Face Jobs！

## 什么是 Hugging Face Jobs？

Hugging Face Jobs 让你可以在 Hugging Face 的无服务器基础设施上运行命令或脚本，几乎可以使用任何硬件配置。一个 Job（任务）本质上包含：

- 要运行的命令
- 一个 Docker 镜像，来自 Docker Hub 或 Hugging Face Space
- 一种硬件配置，例如 CPU 或 `t4-small` 或 `h200` GPU
- 可选的环境变量和密钥

例如，你可以运行：

```bash
hf jobs run python:3.12 python -c "print('Hello world')"

```

```bash
hf jobs uv run --flavor a10g-small "https://raw.githubusercontent.com/huggingface/trl/main/trl/scripts/sft.py" 

```

这使得 Jobs 非常适合 CI。CI 任务本身就是命令驱动的，总是在干净的环境中运行，并且通常受益于选择完全合适的硬件。对于 ML 库来说，GPU 场景尤其引人注目：你可以在真实的 GPU 硬件上运行测试套件，而无需维护自己的常开运行器。

关键步骤是将 GitHub Actions 连接到 HF Jobs，我们将在下面描述。

## 架构

对于此设置，我们创建了 `huggingface/jobs-actions`，这是一个小型桥接器，可将 GitHub Actions 任务转换为在 HF Job 内部运行的临时自托管运行器。

完整流程如下所示：

1. 拉取请求触发 GitHub Actions 工作流。
2. GitHub 将任何 `runs-on` 标签不可用的任务（例如 `hf-jobs-cpu-upgrade` 或 `hf-jobs-t4-small`）加入队列，并通过 GitHub App 向调度器发送签名的 `workflow_job.queued` webhook。
3. 调度器 Space 验证 webhook，检查 `hf-jobs-*` 标签，生成一个短期的 GitHub 运行器注册令牌，并在匹配的硬件上启动一个 HF Job。
4. HF Job 启动一个临时的 GitHub Actions 运行器，并使用该一次性令牌将其注册到仓库。
5. GitHub 将待处理的工作流任务分配给该运行器；运行器执行 CI 任务，将状态报告回 GitHub，然后退出。

从 GitHub 的角度来看，这只是一个自托管运行器。从 Hugging Face 的角度来看，这只是一个启动容器来执行仓库 GitHub Actions 工作流步骤的 Job。

## 步骤 1：复制调度器 Space

你首先需要的是调度器。这是一个小型 Docker Space，用于接收 GitHub `workflow_job` webhook 事件并启动 HF Jobs 作为响应。

请先创建这个，因为 GitHub App 需要一个 webhook URL，而该 URL 来自 Space。此 Space 应位于你自己的命名空间下，或位于你具有写入权限的 Hugging Face 组织下。

#### Web 设置

前往 `huggingface/jobs-actions-dispatcher` 并点击 **Duplicate this Space**。

```text
Owner: 你的 HF 用户或组织
Name: jobs-actions-dispatcher
Hardware: cpu-upgrade

```

对于实际 CI，请使用 `cpu-upgrade`，以便调度器保持可用以接收 GitHub webhook。`cpu-basic` 可用于测试，通常也能工作，但可能会在无活动后休眠；如果在它唤醒期间 GitHub 的 webhook 到达，工作流可能会永远保持排队状态。

构建完成后，打开复制的 Space。你会看到一个显示 "Required Space secrets" 的部分，现在可以忽略它。着陆页应显示你在下一步中需要的 GitHub App webhook URL。它看起来像这样：

```text
https://YOUR-HF-NAMESPACE-jobs-actions-dispatcher.hf.space/webhook

```

#### CLI 设置

如果你更倾向于使用 Agent（智能体）或 CLI 工作流来设置调度器 Space：

```bash
export HF_NAMESPACE=your-hf-user-or-org
export SPACE_ID="$HF_NAMESPACE/jobs-actions-dispatcher"

hf repo duplicate huggingface/jobs-actions-dispatcher "$SPACE_ID" \
  --type space \
  --flavor cpu-upgrade \
  --exist-ok

```

然后设置：

```bash
export DISPATCHER_URL="https://${HF_NAMESPACE}-jobs-actions-dispatcher.hf.space"

```

## 步骤 2：创建并安装 GitHub App

接下来，从调度器 Space 本身创建并安装 GitHub App。此 App 需要权限来监听排队的工作流任务并创建临时的自托管运行器注册令牌。

打开你复制的调度器 Space：

```text
https://YOUR-HF-NAMESPACE-jobs-actions-dispatcher.hf.space

```

在设置表单中，输入其 CI 应在 HF Jobs 上运行的 GitHub 仓库：

```text
YOUR-GITHUB-ORG/YOUR-REPO

```

然后点击按钮创建 GitHub App。GitHub 会要求你为 App 选择一个名称；名称可以是任何内容，只要在你的 GitHub 账户或组织中可用即可。提交后，最终屏幕会准确告诉你如何使用 `hf` CLI 将 App 凭证上传到调度器 Space。

重要提示：你需要提供一个 **Hugging Face 令牌**，该令牌具有启动 Jobs 的权限，对应于你的个人账户或应计费 Jobs 的组织。此令牌应作为 `HF_TOKEN` 密钥保存在你的调度器 Space 中。

最后，你将在你在 Space 中输入的那个 GitHub 仓库上安装该 App。在 Trackio 的设置中，我们将其安装在 `gradio-app/trackio` 上。

### Agent（智能体）辅助设置

GitHub App 清单流程仍然基于浏览器，但 Agent（智能体）可以遵循相同的 Space 驱动路径：

```bash
export HF_NAMESPACE=your-hf-user-or-org
export GITHUB_REPO=YOUR-GITHUB-ORG/YOUR-REPO
open "https://${HF_NAMESPACE}-jobs-actions-dispatcher.hf.space"

```

将 `$GITHUB_REPO` 粘贴到 Space 中，点击 GitHub App 创建按钮，选择任何可用的 App 名称，然后按照生成的 GitHub 说明进行操作。

App 创建后，从 App 设置页面将其安装到你的仓库上。对于 GitHub 组织，安装设置位于：

```text
https://github.com/organizations/YOUR-GITHUB-ORG/settings/installations

```

## 步骤 3：最终调度器设置

此时，调度器 Space 应已配置完成。GitHub App 设置流程生成了将 App 凭证、webhook 密钥和 Hugging Face 令牌上传到 Space 的命令。

默认情况下，HF Jobs 在与调度器 Space 相同的命名空间下启动。如果你想将任务计费到不同的 Hugging Face 用户或组织，可以选择将 `HF_NAMESPACE` 设置为 Space 变量：

```bash
export SPACE_ID=YOUR-HF-NAMESPACE/jobs-actions-dispatcher
hf spaces variables add "$SPACE_ID" -e HF_NAMESPACE=your-billing-namespace
hf spaces restart "$SPACE_ID"

```

你在步骤 2 中设置的令牌应对应于此命名空间。

## 步骤 4：更改 runs-on

实际的工作流更改很小。不再使用：

```yaml
runs-on: ubuntu-latest

```

而是使用调度器处理的标签之一：

```yaml
runs-on: hf-jobs-cpu-upgrade

```

对于 GPU 测试，使用 GPU 标签：

```yaml
runs-on: hf-jobs-t4-small

```

对于任何你想在 HF Jobs 上运行的 GitHub Action，只需这一行更改即可！

## 步骤 5：测试一下

要从 CLI 添加一个最小的冒烟测试工作流：

```bash
mkdir -p .github/workflows
cat > .github/workflows/hf-jobs-test.yml <<'EOF'
name: HF Jobs 测试

on:
  pull_request:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  test:
    runs-on: hf-jobs-cpu-upgrade
    steps:
      - uses: actions/checkout@v4
      - run: echo "来自 Hugging Face Jobs 的问候"
EOF

git add .github/workflows/hf-jobs-test.yml
git commit -m "在 Hugging Face Jobs 上运行 CI"
git push

```

从 CLI 验证：

```bash
gh run list --repo YOUR-GITHUB-ORG/YOUR-REPO --limit 5
hf jobs ps --namespace "$HF_NAMESPACE"
hf spaces logs "$SPACE_ID"

```

你应该能够看到类似常规 GitHub Action 的日志——例如，在这个 Trackio PR #565 中。

就是这样！

关于选择正确 Docker 镜像的说明

我们首次的 CPU 设置使用了 `ubuntu:22.04`，并在每次运行时安装缺失的系统包。这虽然可行，但速度比预期慢。GitHub 的 `ubuntu-latest` 镜像默认包含大量开发者工具；而一个裸 Ubuntu 镜像则没有。

对于 Trackio，UI 测试需要 Playwright 浏览器、Node、ffmpeg、sqlite、git 以及常规的 Linux 构建依赖。Hugging Face Jobs 支持使用任何 Docker 镜像，因此我们切换到了 Microsoft Playwright 镜像，效果很好：

```text
mcr.microsoft.com/playwright:v1.60.0-jammy

```

对于 GPU 任务，我们使用了：

```text
nvidia/cuda:12.4.0-runtime-ubuntu22.04

```

## 结果

以下是 Trackio CI 的数据：

最大的收获是 GPU CI。Trackio GPU 检查在 HF Jobs 上运行，并在 45 秒内通过，按 t4-small 费率计算，该时长的成本不到 1 美分。

CPU 结果也令人鼓舞。使用正确的镜像，Linux 测试任务比 GitHub 托管的基线更快。这表明 HF Jobs 可以成为一个实用的 CI 后端，特别是对于需要自定义镜像或加速器的 ML 项目。

日志是另一个惊喜。GitHub Actions 日志很有用，但对于大型日志，Web UI 可能显得笨重。HF Jobs 日志易于从 CLI 获取：

```bash
hf jobs logs <job_id> > logs.txt

```

这使得它们易于使用本地工具或编码 Agent（智能体）进行检查。在我们的桥接器中，我们还将 GitHub Actions 任务日志镜像到 HF Job 日志中，因此任一系统都有足够的信息来调试运行。

最后，虽然 Trackio 的 CI 不需要，但 HF Jobs 还支持挂载卷，如果你需要在 CI 中快速从 Hugging Face 加载数据集或模型，这会非常有帮助。

希望这能为你提供尝试使用 HF Jobs 运行 GitHub Actions 所需的一切！

---

> 本文由AI自动翻译，原文链接：[Migrating Your GitHub CI to Hugging Face Jobs](https://huggingface.co/blog/github-ci-hf-jobs)
> 
> 翻译时间：2026-06-10 06:25
