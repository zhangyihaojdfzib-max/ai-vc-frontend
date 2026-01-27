# AI-VC-Frontend 项目记忆

> 最后更新: 2026-01-27

## 项目概述

这是一个自动翻译 VC/AI 博客文章的 Next.js 网站，部署在 Vercel 上。

- **GitHub**: https://github.com/zhangyihaojdfzib-max/ai-vc-frontend
- **技术栈**: Next.js 16.1.1, TypeScript, Tailwind CSS, Python (抓取/翻译)
- **翻译 API**: DeepSeek
- **自动化**: GitHub Actions 每日定时抓取翻译

## 项目结构

```
ai-vc-frontend/
├── app/                    # Next.js 页面
│   └── posts/[slug]/       # 文章详情页
├── content/posts/          # 翻译后的 Markdown 文章 (748+篇)
├── public/images/posts/    # 下载的文章图片
├── scripts/
│   ├── main.py             # 主抓取翻译脚本
│   ├── content_extractor_v2.py  # 内容提取器
│   └── clean_articles.py   # 文章清理工具
├── data/
│   ├── sources.yaml        # RSS 源配置
│   ├── processed_urls.json # 已处理 URL
│   └── failed_urls.json    # 失败 URL
└── lib/posts.ts            # 文章读取/排序逻辑
```

## 2026-01-27 完成的工作

### 1. 文章审计与清理
- [x] 清理 12 篇文章的垃圾内容 (334 行)
- [x] 移除 817 个缺失图片引用 (186 篇文章)
- [x] 移除 9 个不该出现的 logo 图片
- [x] 修复 YAML frontmatter 解析错误
- [x] 修复 TypeScript 类型错误 (img src)
- [x] 修复 package-lock.json 缺失依赖

### 2. 排序逻辑修复
- [x] `lib/posts.ts`: 改为按发布日期排序，而非翻译时间

### 3. 抓取优先级修复
- [x] `scripts/main.py`: RSS/Sitemap 抓取时按日期排序，优先翻译新文章
- [x] 解决了"考古问题"（Discord 翻译 2024 年旧文章而非新内容）

### 4. 禁用失效 RSS 源
- Netflix Tech Blog (SSL 错误)
- Uber Engineering (406 错误)
- Figma Blog (404 错误)
- Notion Blog (404 错误)
- Linear Blog (404 错误)

## 待办事项

### 高优先级
- [ ] 修复失效的 RSS 源（查找新的 RSS URL）
- [ ] 分析用户提供的工作记录，找出更深层问题
- [ ] 验证新的抓取优先级逻辑是否生效

### 中优先级
- [ ] 实现决策树机制：
  - 先检查所有源是否有新文章（1-2天内）
  - 有新文章 → 优先翻译
  - 无新文章 → 启动考古模式
- [ ] 减少 Discord 文章占比（目前 12%，93 篇）

### 低优先级
- [ ] 为 OpenAI Blog 等反爬站点添加 Playwright 支持
- [ ] 添加更多 VC 基金博客源

## 已知问题

### RSS 源状态
| 来源 | 状态 | 问题 |
|------|------|------|
| Netflix Tech Blog | 禁用 | SSL 证书验证失败 |
| Uber Engineering | 禁用 | 406 Not Acceptable |
| Figma Blog | 禁用 | 404，RSS 地址已变 |
| Notion Blog | 禁用 | 404，域名可能改为 notion.com |
| Linear Blog | 禁用 | 404，RSS 地址已变 |
| OpenAI Blog | 禁用 | 403 Forbidden，反爬严格 |
| First Round Review | 禁用 | 404，需要 Playwright |
| Bessemer | 禁用 | RSS 失效 |

### 内容提取问题
- HuggingFace: 可能混入相关文章、评论、头像（已添加过滤）
- Databricks: 可能混入页脚垃圾内容（已添加清理）

## 关键代码位置

- **文章排序**: `lib/posts.ts:114`
- **RSS 抓取**: `scripts/main.py:489` (_fetch_rss)
- **内容提取**: `scripts/content_extractor_v2.py`
- **垃圾清理**: `scripts/main.py:42` (ContentCleaner)
- **源配置**: `data/sources.yaml`

## 常用命令

```bash
# 手动触发翻译
gh workflow run daily-translate.yml

# 检查工作流状态
gh run list --workflow=daily-translate.yml --limit 3

# 本地测试翻译（需要 DEEPSEEK_API_KEY）
PYTHONIOENCODING=utf-8 python scripts/main.py --source huggingface --max-per-source 1

# 统计文章来源分布
cd content/posts && grep -h "^source:" *.md | sed 's/source: //' | sort | uniq -c | sort -rn | head -20

# 本地构建测试
npm run build
```

## 联系方式

项目所有者: zhangyihaojdfzib-max
