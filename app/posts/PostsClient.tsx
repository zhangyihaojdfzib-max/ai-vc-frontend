'use client'

import { motion } from 'framer-motion'
import ArticleCard from '@/components/ui/ArticleCard'
import { PostMeta } from '@/lib/posts'

interface PostsClientProps {
  posts: PostMeta[]
}

export default function PostsClient({ posts }: PostsClientProps) {
  return (
    <main className="min-h-screen py-24">
      <div className="max-w-4xl mx-auto px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="mb-16"
        >
          <h1 className="text-4xl md:text-5xl font-serif text-gray-900 mb-4">
            全部文章
          </h1>
          <p className="text-lg text-gray-500">
            共 {posts.length} 篇来自全球顶级 VC 和科技思想领袖的深度内容
          </p>
        </motion.div>

        {/* Articles */}
        <div className="space-y-0">
          {posts.map((post, index) => (
            <ArticleCard
              key={post.slug}
              slug={post.slug}
              title={post.title}
              summary={post.summary}
              date={post.date}
              source={post.source}
              category={post.categories[0]}
              readingTime={post.readingTime}
              index={index}
            />
          ))}
        </div>
      </div>
    </main>
  )
}
