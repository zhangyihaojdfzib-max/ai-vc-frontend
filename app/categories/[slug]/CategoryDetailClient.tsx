'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'

interface Post {
  slug: string
  title: string
  date: string
  source: string
  summary: string
  categories: string[]
  tags: string[]
  readingTime: string
}

interface CategoryDetailClientProps {
  categoryName: string
  posts: Post[]
}

export default function CategoryDetailClient({ categoryName, posts }: CategoryDetailClientProps) {
  return (
    <main className="min-h-screen py-24">
      <div className="max-w-4xl mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="mb-12"
        >
          <Link href="/categories" className="text-sm text-gray-500 hover:text-gray-700 mb-4 inline-block">
            ← 返回分类
          </Link>
          <h1 className="text-4xl md:text-5xl font-serif text-gray-900 mb-4">{categoryName}</h1>
          <p className="text-lg text-gray-500">共 {posts.length} 篇文章</p>
        </motion.div>

        <div className="space-y-6">
          {posts.map((post, index) => (
            <motion.article
              key={post.slug}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: index * 0.05, ease: [0.22, 1, 0.36, 1] }}
            >
              <Link href={`/posts/${post.slug}`}>
                <motion.div
                  className="p-6 rounded-xl border border-gray-100 hover:border-gray-200 bg-white hover:shadow-sm transition-all"
                  whileHover={{ y: -2 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className="flex items-center gap-3 text-sm text-gray-500 mb-3">
                    <span>{post.source}</span>
                    <span>·</span>
                    <span>{post.date}</span>
                    <span>·</span>
                    <span>{post.readingTime}</span>
                  </div>
                  <h2 className="text-xl font-medium text-gray-900 mb-3 leading-tight">{post.title}</h2>
                  <p className="text-gray-600 leading-relaxed line-clamp-2">{post.summary}</p>
                  {post.tags.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-4">
                      {post.tags.slice(0, 4).map((tag) => (
                        <span key={tag} className="px-2 py-1 text-xs bg-gray-100 text-gray-600 rounded">{tag}</span>
                      ))}
                    </div>
                  )}
                </motion.div>
              </Link>
            </motion.article>
          ))}
        </div>
      </div>
    </main>
  )
}
