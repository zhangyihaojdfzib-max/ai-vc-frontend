'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { Post } from '@/lib/posts'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import rehypeRaw from 'rehype-raw'
import { useState } from 'react'

interface PostClientProps {
  post: Post
}

// Image component with error handling for missing images
function MarkdownImage({ src, alt }: { src?: string; alt?: string }) {
  const [error, setError] = useState(false)

  if (!src || error) {
    return null // Don't render broken images
  }

  return (
    <figure className="my-8">
      <img
        src={src}
        alt={alt || ''}
        className="w-full rounded-lg shadow-md"
        onError={() => setError(true)}
        loading="lazy"
      />
      {alt && <figcaption className="text-center text-sm text-gray-500 mt-2">{alt}</figcaption>}
    </figure>
  )
}

export default function PostClient({ post }: PostClientProps) {
  return (
    <main className="min-h-screen py-24">
      <article className="max-w-3xl mx-auto px-6">
        <motion.header
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] as const }}
          className="mb-12"
        >
          <Link href="/posts" className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900 mb-8 transition-colors">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            返回文章列表
          </Link>
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
          <h1 className="text-3xl md:text-4xl font-serif text-gray-900 leading-tight mb-4">
            {post.title}
          </h1>
          {post.title_original && (
            <p className="text-gray-400 text-sm mb-4">原文：{post.title_original}</p>
          )}
          {post.summary && (
            <p className="text-lg text-gray-500 leading-relaxed border-l-4 border-emerald-200 pl-4">
              {post.summary}
            </p>
          )}
        </motion.header>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: [0.22, 1, 0.36, 1] as const }}
          className="prose prose-lg max-w-none"
        >
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeRaw]}
            components={{
              // Headings
              h1: ({ children }) => (
                <h1 className="text-3xl font-serif text-gray-900 mt-12 mb-6">{children}</h1>
              ),
              h2: ({ children }) => (
                <h2 className="text-2xl font-serif text-gray-900 mt-12 mb-4">{children}</h2>
              ),
              h3: ({ children }) => (
                <h3 className="text-xl font-medium text-gray-900 mt-8 mb-3">{children}</h3>
              ),
              h4: ({ children }) => (
                <h4 className="text-lg font-medium text-gray-900 mt-6 mb-2">{children}</h4>
              ),

              // Paragraphs
              p: ({ children }) => (
                <p className="text-gray-600 leading-relaxed mb-6">{children}</p>
              ),

              // Links
              a: ({ href, children }) => (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-emerald-600 hover:text-emerald-700 underline underline-offset-2"
                >
                  {children}
                </a>
              ),

              // Images with error handling
              img: ({ src, alt }) => <MarkdownImage src={src} alt={alt} />,

              // Lists
              ul: ({ children }) => (
                <ul className="list-disc list-inside space-y-2 mb-6 text-gray-600 pl-4">{children}</ul>
              ),
              ol: ({ children }) => (
                <ol className="list-decimal list-inside space-y-2 mb-6 text-gray-600 pl-4">{children}</ol>
              ),
              li: ({ children }) => (
                <li className="leading-relaxed">{children}</li>
              ),

              // Blockquotes
              blockquote: ({ children }) => (
                <blockquote className="border-l-4 border-emerald-500 pl-4 italic text-gray-500 my-6">
                  {children}
                </blockquote>
              ),

              // Code blocks
              pre: ({ children }) => (
                <pre className="bg-gray-900 text-gray-100 rounded-lg p-4 overflow-x-auto my-6 text-sm">
                  {children}
                </pre>
              ),
              code: ({ className, children, ...props }) => {
                const isInline = !className
                if (isInline) {
                  return (
                    <code className="bg-gray-100 text-emerald-700 px-1.5 py-0.5 rounded text-sm font-mono" {...props}>
                      {children}
                    </code>
                  )
                }
                return (
                  <code className="text-gray-100 font-mono text-sm" {...props}>
                    {children}
                  </code>
                )
              },

              // Tables (GFM)
              table: ({ children }) => (
                <div className="overflow-x-auto my-6">
                  <table className="min-w-full border-collapse border border-gray-200">
                    {children}
                  </table>
                </div>
              ),
              thead: ({ children }) => (
                <thead className="bg-gray-50">{children}</thead>
              ),
              tbody: ({ children }) => (
                <tbody className="divide-y divide-gray-200">{children}</tbody>
              ),
              tr: ({ children }) => (
                <tr className="border-b border-gray-200">{children}</tr>
              ),
              th: ({ children }) => (
                <th className="px-4 py-2 text-left text-sm font-medium text-gray-900 border border-gray-200">
                  {children}
                </th>
              ),
              td: ({ children }) => (
                <td className="px-4 py-2 text-sm text-gray-600 border border-gray-200">
                  {children}
                </td>
              ),

              // Horizontal rule
              hr: () => <hr className="my-8 border-gray-200" />,

              // Strong and emphasis
              strong: ({ children }) => (
                <strong className="font-semibold text-gray-900">{children}</strong>
              ),
              em: ({ children }) => (
                <em className="italic">{children}</em>
              ),
            }}
          >
            {post.content}
          </ReactMarkdown>
        </motion.div>

        {post.tags && post.tags.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="mt-12 pt-8 border-t border-gray-100"
          >
            <div className="flex flex-wrap gap-2">
              {post.tags.map((tag) => (
                <span key={tag} className="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full">
                  #{tag}
                </span>
              ))}
            </div>
          </motion.div>
        )}

        <motion.footer
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-8 pt-8 border-t border-gray-100"
        >
          <p className="text-sm text-gray-400">
            本文由 AI 自动翻译
            {post.source_url && (
              <span>
                ，原文链接：
                <a
                  href={post.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-emerald-600 hover:underline ml-1"
                >
                  查看原文 →
                </a>
              </span>
            )}
          </p>
        </motion.footer>
      </article>
    </main>
  )
}
