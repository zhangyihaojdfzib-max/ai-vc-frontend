---
title: Vercel现已支持自定义平台错误页面，提升品牌体验
title_original: Vercel now supports customizing platform error pages - Vercel
date: '2026-01-23'
source: Vercel Blog
source_url: https://vercel.com/changelog/vercel-now-supports-customizing-platform-error-pages
author: ''
summary: Vercel宣布推出平台错误页面自定义功能，允许开发者替换通用错误页面，展示符合自身品牌风格的错误提示。该功能通过框架约定自动识别自定义页面，支持使用元数据Token（如请求ID和错误代码）嵌入特定请求上下文，便于问题调试与支持调查。目前该功能面向企业团队自动启用，无需额外配置，适用于Next.js等框架，可通过App
  Router或公共目录实现。
categories:
- AI基础设施
tags:
- Vercel
- 错误处理
- 前端开发
- 云平台
- Next.js
draft: false
translated_at: '2026-01-24T04:30:52.252715'
---

您现在可以为Vercel上的平台错误自定义错误页面，用您自己的品牌体验替换通用错误页面。当Vercel遇到未捕获的错误（如函数调用超时或其他平台错误）时，将显示自定义错误页面。

### 工作原理

您可以使用您框架的约定来实现自定义错误页面，Vercel将自动定位它们。例如，在Next.js中，您只需在`public`目录中放置一个`500/page.tsx`或静态的`500.html`页面。

为了用特定请求的上下文丰富错误页面，您可以使用以下元数据Token：

- `::vercel:REQUEST_ID::` - 包含Vercel请求ID
- `::vercel:ERROR_CODE::` - 特定的错误代码，例如`FUNCTION_INVOCATION_TIMEOUT`

```
1export default function CustomErrorPage() {2  return (3    <div className="flex min-h-screen flex-col items-center justify-center">4      <h1 className="text-4xl font-bold">500</h1>5      <p className="mt-4 text-lg text-gray-600">Internal Server Error</p>6      <p className="mt-2 text-sm text-gray-500">7        Request ID: ::vercel:REQUEST_ID::8      </p>9      <p className="mt-2 text-sm text-gray-500">10        Code: ::vercel:ERROR_CODE::11      </p>12      <p className="mt-2 text-sm text-gray-500">13        Something went wrong on our end. Please try again later.14      </p>15      <a href="/" className="mt-6 text-blue-600 hover:underline">16        Go back home17      </a>18    </div>19  );20}
```

我们强烈建议包含请求ID和错误代码，以帮助调试和支持调查。

此功能适用于企业团队，并在所有项目中自动启用。无需额外配置。

请参阅[文档](https://vercel.com/docs/projects/custom-error-pages)以开始使用，或参考以下实现：[使用App Router的自定义错误页面](https://vercel.com/docs/projects/custom-error-pages/app-router)或[使用公共目录的自定义错误页面](https://vercel.com/docs/projects/custom-error-pages/public-directory)。

---

> 本文由AI自动翻译，原文链接：[Vercel now supports customizing platform error pages - Vercel](https://vercel.com/changelog/vercel-now-supports-customizing-platform-error-pages)
> 
> 翻译时间：2026-01-24 04:30
