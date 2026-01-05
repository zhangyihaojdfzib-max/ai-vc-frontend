'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { PostMeta } from '@/lib/posts'

interface SourceMeta {
  name: string
  fullName: string
  description: string
  website?: string
}

interface SourceDetailClientProps {
  meta: SourceMeta
  slug: string
  posts: PostMeta[]
}

export default function SourceDetailClient({ meta, slug, posts }: SourceDetailClientProps) {
  return (
    <main className="min-h-screen py-24">
      <div className="max-w-4xl mx-auto px-6">
        {/* Header */}
        <motion.header
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="mb-16"
        >
          {/* Back link */}
          <Link
            href="/sources"
            className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-900 mb-8 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            所有内容源
          </Link>

          <div className="flex items-start justify-between">
            <div>
              <h1 className="text-4xl md:text-5xl font-serif text-gray-900 mb-2">
                {meta.name}
              </h1>
              {meta.name !== meta.fullName && (
                <p className="text-lg text-gray-400 mb-4">{meta.fullName}</p>
              )}
              <p className="text-lg text-gray-500 max-w-2xl">
                {meta.description}
              </p>
            </div>
          </div>

          {/* Stats */}
          <div className="flex items-center gap-6 mt-8 pt-8 border-t border-gray-100">
            <div>
              <div className="text-3xl font-light text-gray-900">{posts.length}</div>
              <div className="text-sm text-gray-500">已翻译文章</div>
            </div>
            {meta.website && (
              <a
                href={meta.website}
                target="_blank"
                rel="noopener noreferrer"
                className="ml-auto px-6 py-3 bg-gray-900 text-white text-sm font-medium rounded-full hover:bg-gray-800 transition-colors"
              >
                访问官网 →
              </a>
            )}
          </div>
        </motion.header>

        {/* Articles */}
        {posts.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center py-20 text-gray-500"
          >
            暂无文章，敬请期待...
          </motion.div>
        ) : (
          <div className="space-y-0">
            {posts.map((post, index) => (
              <motion.article
                key={post.slug}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{
                  duration: 0.5,
                  delay: index * 0.05,
                  ease: [0.22, 1, 0.36, 1],
                }}
              >
                <Link href={`/posts/${post.slug}`} className="group block">
                  <motion.div
                    className="py-8 border-b border-gray-100 group-hover:border-emerald-200 transition-colors"
                    whileHover={{ x: 8 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="flex flex-wrap items-center gap-3 mb-3">
                      {post.categories[0] && (
                        <span className="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded-full">
                          {post.categories[0]}
                        </span>
                      )}
                      <span className="text-sm text-gray-400">{post.date}</span>
                      <span className="text-sm text-gray-300">·</span>
                      <span className="text-sm text-gray-400">{post.readingTime}</span>
                    </div>

                    <h2 className="text-xl font-serif text-gray-900 mb-2 group-hover:text-emerald-700 transition-colors leading-tight">
                      {post.title}
                    </h2>

                    <p className="text-gray-500 text-sm leading-relaxed line-clamp-2">
                      {post.summary}
                    </p>
                  </motion.div>
                </Link>
              </motion.article>
            ))}
          </div>
        )}
      </div>
    </main>
  )
}
