---
title: Vercel Blob 私有存储新增强一致性读取
title_original: Vercel Blob now supports consistent reads on private storage - Vercel
date: '2026-07-14'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-blob-now-supports-consistent-reads-on-private-storage
author: ''
summary: 'Vercel Blob 宣布支持私有存储的强一致性读取，通过传入 `useCache: false` 参数或添加 `cache=0` 查询参数，用户可获取反映最新写入内容的读取结果。该功能适用于需要实时数据的场景，如
  Agent 记忆文件、会话记录或定时生成的 JSON 报告。强一致性读取会绕过 CDN，耗时更长并产生 Fast Origin Transfer 费用。最新 SDK
  版本为 `@vercel/blob@2.6.1`。'
categories:
- AI基础设施
tags:
- Vercel Blob
- 强一致性
- 私有存储
- CDN
- SDK
draft: false
translated_at: '2026-07-15T04:54:27.332341'
---

Vercel Blob 现在支持私有存储的强一致性读取。在 `get()` 或 `presignUrl()` 中传入 `useCache: false` 参数，即可获取反映最新写入内容的读取结果。

写入新路径名的 Blob 没有现有缓存条目，因此读取会立即反映最新写入。当覆盖现有路径名的 Blob 时，读取者可能在最多 60 秒内看到缓存版本。

当读取必须反映最新写入时（例如 Agent 的记忆文件、会话记录或定时生成的 JSON 报告），请传入 `useCache: false`。这些读取会绕过 CDN，耗时比缓存读取更长，并会产生 Fast Origin Transfer 费用。

```
1import { put, get } from '@vercel/blob';
2
3await put('reports/latest.json', JSON.stringify(report), {
4    access: 'private',
5});
6
7
8let result = await get('reports/latest.json', { access: 'private' });
9
10
11
12await put('reports/latest.json', JSON.stringify(updatedReport), {
13    access: 'private',
14    allowOverwrite: true,
15});
16
17
18
19result = await get('reports/latest.json', {
20    access: 'private',
21    useCache: false,
22});
```

你也可以在不使用 SDK 的情况下绕过缓存。在底层，`useCache: false` 会向请求添加 `cache=0` 查询参数。你可以在私有 Blob URL 上自行设置该参数：

```
1curl "https://<store-id>.private.blob.vercel-storage.com/file.json?cache=0" \
2  -H "Authorization: Bearer $BLOB_READ_WRITE_TOKEN"
```

安装最新版 `@vercel/blob` SDK 以实现强一致性读取：

```
1npm install @vercel/blob@2.6.1
```

更多信息请参阅强一致性读取文档。

---

> 本文由AI自动翻译，原文链接：[Vercel Blob now supports consistent reads on private storage - Vercel](https://vercel.com/changelog/vercel-blob-now-supports-consistent-reads-on-private-storage)
> 
> 翻译时间：2026-07-15 04:54
