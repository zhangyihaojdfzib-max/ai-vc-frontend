'use client'

import Link from 'next/link'
import { motion } from 'framer-motion'

interface ArticleCardProps {
  slug: string
  title: string
  summary: string
  date: string
  source: string
  category?: string
  readingTime?: string
  index?: number
}

export default function ArticleCard({
  slug,
  title,
  summary,
  date,
  source,
  category,
  readingTime,
  index = 0,
}: ArticleCardProps) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.6,
        delay: index * 0.1,
        ease: [0.22, 1, 0.36, 1],
      }}
    >
      <Link href={`/posts/${slug}`} className="group block">
        <motion.div
          className="py-10 border-b border-gray-100 transition-colors group-hover:border-emerald-200"
          whileHover={{ x: 8 }}
          transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
        >
          {/* Meta */}
          <div className="flex items-center gap-4 mb-4">
            {category && (
              <span className="text-xs font-medium text-emerald-600 bg-emerald-50 px-3 py-1 rounded-full">
                {category}
              </span>
            )}
            <span className="text-sm text-gray-400">{source}</span>
            <span className="text-sm text-gray-300">·</span>
            <span className="text-sm text-gray-400">{date}</span>
            {readingTime && (
              <>
                <span className="text-sm text-gray-300">·</span>
                <span className="text-sm text-gray-400">{readingTime}</span>
              </>
            )}
          </div>

          {/* Title */}
          <h2 className="text-2xl font-serif font-normal text-gray-900 mb-3 group-hover:text-emerald-700 transition-colors leading-tight">
            {title}
          </h2>

          {/* Summary */}
          <p className="text-gray-500 leading-relaxed line-clamp-2">
            {summary}
          </p>

          {/* Read more */}
          <motion.div
            className="mt-4 flex items-center gap-2 text-sm font-medium text-emerald-600 opacity-0 group-hover:opacity-100 transition-opacity"
            initial={{ x: -10 }}
            whileHover={{ x: 0 }}
          >
            阅读全文
            <svg
              className="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M17 8l4 4m0 0l-4 4m4-4H3"
              />
            </svg>
          </motion.div>
        </motion.div>
      </Link>
    </motion.article>
  )
}
