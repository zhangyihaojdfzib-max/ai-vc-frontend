'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { Post } from '@/lib/posts'

interface PostClientProps {
  post: Post
}

export default function PostClient({ post }: PostClientProps) {
  // 简单的 Markdown 渲染
  const renderContent = (content: string) => {
    const lines = content.split('\n')
    const elements: React.ReactNode[] = []
    let listItems: string[] = []

    const flushList = () => {
      if (listItems.length > 0) {
        elements.push(
          <ul key={`list-${elements.length}`} className="list-disc list-inside space-y-2 mb-6 text-gray-600">
            {listItems.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        )
        listItems = []
      }
    }

    lines.forEach((line, index) => {
      const trimmed = line.trim()

      if (trimmed.startsWith('## ')) {
        flushList()
        elements.push(
          <h2 key={index} className="text-2xl font-serif text-gray-900 mt-12 mb-4">
            {trimmed.replace('## ', '')}
          </h2>
        )
      } else if (trimmed.startsWith('### ')) {
        flushList()
        elements.push(
          <h3 key={index} className="text-xl font-medium text-gray-900 mt-8 mb-3">
            {trimmed.replace('### ', '')}
          </h3>
        )
      } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
        listItems.push(trimmed.replace(/^[-*] /, ''))
      } else if (trimmed.match(/^\d+\. /)) {
        listItems.push(trimmed.replace(/^\d+\. /, ''))
      } else if (trimmed.startsWith('> ')) {
        flushList()
        elements.push(
          <blockquote key={index} className="border-l-4 border-emerald-500 pl-4 italic text-gray-500 my-6">
            {trimmed.replace('> ', '')}
          </blockquote>
        )
      } else if (trimmed.startsWith('```')) {
        // 跳过代码块标记
      } else if (trimmed) {
        flushList()
        elements.push(
          <p key={index} className="text-gray-600 leading-relaxed mb-6">
            {trimmed}
          </p>
        )
      }
    })

    flushList()
    return elements
  }

  return (
    <main className="min-h-screen py-24">
      <article className="max-w-3xl mx-auto px-6">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] as const }}
          className="mb-12"
        >
          {/* Back link */}
          <Link
            href="/posts"
            className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900 mb-8 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            返回文章列表
          </Link>

          {/* Meta */}
          <div className="flex flex-wrap items-center gap-3 mb-6">
            {post.categories[0] && (
              <span className="text-sm font-medium text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">
                {post.categories[0]}
              </span>
            )}
            <span className="text-sm text-gray-400">{post.source}</span>
            <span className="text-sm text-gray-300">·</span>
            <span className="text-sm text-gray-400">{post.date}</span>
            <span className="text-sm text-gray-300">·</span>
            <span className="text-sm text-gray-400">{post.readingTime}</span>
          </div>

          {/* Title */}
          <h1 className="text-3xl md:text-4xl font-serif text-gray-900 leading-tight mb-4">
            {post.title}
          </h1>

          {/* Original title */}
          {post.title_original && (
            <p className="text-gray-400 text-sm mb-4">
              原文：{post.title_original}
            </p>
          )}

          {/* Summary */}
          {post.summary && (
            <p className="text-lg text-gray-500 leading-relaxed border-l-4 border-emerald-200 pl-4">
              {post.summary}
            </p>
          )}
        </motion.header>

        {/* Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: [0.22, 1, 0.36, 1] as const }}
          className="prose prose-lg max-w-none"
        >
          {renderContent(post.content)}
        </motion.div>

        {/* Tags */}
        {post.tags && post.tags.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="mt-12 pt-8 border-t border-gray-100"
          >
            <div className="flex flex-wrap gap-2">
              {post.tags.map((tag) => (
                <span
                  key={tag}
                  className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full"
                >
                  #{tag}
                </span>
              ))}
            </div>
          </motion.div>
        )}

        {/* Footer */}
        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-8 pt-8 border-t border-gray-100"
        >
          <p className="text-sm text-gray-400">
            本文由 AI 自动翻译
            {post.source_url && (
              <>
                ，原文链接：
                <a
                  href={post.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-emerald-600 hover:underline ml-1"
                >
                  查看原文 →
                </a>
              </>
            )}
          </p>
        </motion.footer>
      </article>
    </main>
  )
}
