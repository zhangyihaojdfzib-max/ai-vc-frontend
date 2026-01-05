'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import TextReveal from '@/components/animations/TextReveal'
import { PostMeta } from '@/lib/posts'

interface HomeClientProps {
  featuredPosts: PostMeta[]
  totalPosts: number
}

export default function HomeClient({ featuredPosts, totalPosts }: HomeClientProps) {
  return (
    <main>
      {/* Hero Section */}
      <section className="min-h-[80vh] flex items-center justify-center px-6">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
          >
            <h1 className="text-5xl md:text-7xl font-serif font-normal tracking-tight text-gray-900 mb-8">
              AI/VC
              <span className="text-emerald-600">前沿观察</span>
            </h1>
          </motion.div>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
            className="text-xl md:text-2xl text-gray-500 font-light leading-relaxed max-w-2xl mx-auto mb-12"
          >
            每日自动追踪、翻译并聚合全球顶级的
            <br className="hidden md:block" />
            AI、VC与创业领域深度内容
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4, ease: [0.22, 1, 0.36, 1] }}
            className="flex items-center justify-center gap-4"
          >
            <Link href="/posts">
              <motion.button
                className="px-8 py-4 bg-gray-900 text-white text-sm font-medium rounded-full hover:bg-gray-800 transition-colors"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                浏览全部文章
              </motion.button>
            </Link>
            <Link href="/about">
              <motion.button
                className="px-8 py-4 text-gray-600 text-sm font-medium hover:text-gray-900 transition-colors"
                whileHover={{ x: 4 }}
              >
                了解更多 →
              </motion.button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 border-y border-gray-100 bg-gray-50/50">
        <div className="max-w-6xl mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {[
              { number: '44+', label: '信息源' },
              { number: `${totalPosts}`, label: '已翻译文章' },
              { number: '每日', label: '自动更新' },
              { number: '免费', label: '完全开放' },
            ].map((stat, index) => (
              <motion.div
                key={stat.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="text-center"
              >
                <div className="text-4xl md:text-5xl font-light text-gray-900 mb-2">
                  {stat.number}
                </div>
                <div className="text-sm text-gray-500">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Posts */}
      <section className="py-24">
        <div className="max-w-4xl mx-auto px-6">
          <TextReveal>
            <div className="flex items-center justify-between mb-16">
              <h2 className="text-3xl font-serif text-gray-900">最新文章</h2>
              <Link
                href="/posts"
                className="text-sm text-gray-500 hover:text-gray-900 transition-colors"
              >
                查看全部 →
              </Link>
            </div>
          </TextReveal>

          <div className="space-y-0">
            {featuredPosts.map((post, index) => (
              <motion.article
                key={post.slug}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{
                  duration: 0.6,
                  delay: index * 0.15,
                  ease: [0.22, 1, 0.36, 1],
                }}
              >
                <Link href={`/posts/${post.slug}`} className="group block">
                  <motion.div
                    className="py-10 border-b border-gray-100 group-hover:border-emerald-200 transition-colors"
                    whileHover={{ x: 8 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div className="flex flex-wrap items-center gap-3 mb-4">
                      {post.categories[0] && (
                        <span className="text-xs font-medium text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">
                          {post.categories[0]}
                        </span>
                      )}
                      <span className="text-sm text-gray-400">{post.source}</span>
                      <span className="text-sm text-gray-300">·</span>
                      <span className="text-sm text-gray-400">{post.date}</span>
                      <span className="text-sm text-gray-300">·</span>
                      <span className="text-sm text-gray-400">{post.readingTime}</span>
                    </div>

                    <h3 className="text-2xl font-serif text-gray-900 mb-3 group-hover:text-emerald-700 transition-colors leading-tight">
                      {post.title}
                    </h3>

                    <p className="text-gray-500 leading-relaxed line-clamp-2">
                      {post.summary}
                    </p>
                  </motion.div>
                </Link>
              </motion.article>
            ))}
          </div>
        </div>
      </section>

      {/* Sources Section */}
      <section className="py-24 bg-gray-50/50">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <TextReveal>
            <h2 className="text-3xl font-serif text-gray-900 mb-6">
              内容来源
            </h2>
            <p className="text-gray-500 mb-12">
              我们追踪全球最具影响力的 VC 和科技思想领袖
            </p>
          </TextReveal>

          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="flex flex-wrap justify-center gap-4"
          >
            {[
              'Sequoia Capital',
              'Y Combinator',
              'a16z',
              'Greylock',
              'USV',
              'Anthropic',
              'OpenAI',
              'Google AI',
              'Paul Graham',
              'Sam Altman',
            ].map((source) => (
              <span
                key={source}
                className="px-4 py-2 bg-white border border-gray-200 rounded-full text-sm text-gray-600"
              >
                {source}
              </span>
            ))}
          </motion.div>
        </div>
      </section>
    </main>
  )
}
