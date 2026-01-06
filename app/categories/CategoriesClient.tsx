'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'

interface Category {
  name: string
  slug: string
  count: number
  color: string
  description: string
}

interface CategoriesClientProps {
  categories: Category[]
  totalPosts: number
}

const colorMap: Record<string, string> = {
  emerald: 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100',
  blue: 'bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100',
  purple: 'bg-purple-50 text-purple-700 border-purple-200 hover:bg-purple-100',
  cyan: 'bg-cyan-50 text-cyan-700 border-cyan-200 hover:bg-cyan-100',
  orange: 'bg-orange-50 text-orange-700 border-orange-200 hover:bg-orange-100',
  pink: 'bg-pink-50 text-pink-700 border-pink-200 hover:bg-pink-100',
  rose: 'bg-rose-50 text-rose-700 border-rose-200 hover:bg-rose-100',
  amber: 'bg-amber-50 text-amber-700 border-amber-200 hover:bg-amber-100',
  indigo: 'bg-indigo-50 text-indigo-700 border-indigo-200 hover:bg-indigo-100',
  teal: 'bg-teal-50 text-teal-700 border-teal-200 hover:bg-teal-100',
  slate: 'bg-slate-50 text-slate-700 border-slate-200 hover:bg-slate-100',
  red: 'bg-red-50 text-red-700 border-red-200 hover:bg-red-100',
  gray: 'bg-gray-50 text-gray-700 border-gray-200 hover:bg-gray-100',
}

export default function CategoriesClient({ categories, totalPosts }: CategoriesClientProps) {
  return (
    <main className="min-h-screen py-24">
      <div className="max-w-4xl mx-auto px-6">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="mb-16"
        >
          <h1 className="text-4xl md:text-5xl font-serif text-gray-900 mb-4">
            分类浏览
          </h1>
          <p className="text-lg text-gray-500">
            按主题探索我们的内容库 · 共 {totalPosts} 篇文章
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {categories.map((category, index) => (
            <motion.div
              key={category.name}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.05, ease: [0.22, 1, 0.36, 1] }}
            >
              <Link href={`/categories/${encodeURIComponent(category.slug)}`}>
                <motion.div
                  className={`p-6 rounded-2xl border transition-all cursor-pointer ${colorMap[category.color] || colorMap.gray}`}
                  whileHover={{ y: -4, scale: 1.02 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className="flex items-start justify-between mb-3">
                    <h2 className="text-xl font-medium">{category.name}</h2>
                    <span className="text-sm opacity-70">{category.count} 篇</span>
                  </div>
                  <p className="text-sm opacity-80 leading-relaxed">{category.description}</p>
                </motion.div>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>
    </main>
  )
}
