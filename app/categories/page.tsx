'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'

const categories = [
  {
    name: 'AI研究',
    count: 156,
    description: '人工智能前沿研究、大模型技术、机器学习进展',
    color: 'emerald',
  },
  {
    name: 'AI产品',
    count: 89,
    description: 'AI 应用产品分析、商业化案例、产品策略',
    color: 'blue',
  },
  {
    name: 'VC观点',
    count: 124,
    description: '风险投资人的行业洞察、投资趋势、市场分析',
    color: 'purple',
  },
  {
    name: '创业',
    count: 98,
    description: '创业方法论、公司建设、融资策略、团队管理',
    color: 'orange',
  },
  {
    name: '技术趋势',
    count: 67,
    description: '科技行业宏观趋势、技术演进、行业预测',
    color: 'pink',
  },
  {
    name: 'AI基础设施',
    count: 45,
    description: 'AI 基础设施、云计算、芯片、训练平台',
    color: 'cyan',
  },
]

const colorMap: Record<string, string> = {
  emerald: 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100',
  blue: 'bg-blue-50 text-blue-700 border-blue-200 hover:bg-blue-100',
  purple: 'bg-purple-50 text-purple-700 border-purple-200 hover:bg-purple-100',
  orange: 'bg-orange-50 text-orange-700 border-orange-200 hover:bg-orange-100',
  pink: 'bg-pink-50 text-pink-700 border-pink-200 hover:bg-pink-100',
  cyan: 'bg-cyan-50 text-cyan-700 border-cyan-200 hover:bg-cyan-100',
}

export default function CategoriesPage() {
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
            分类浏览
          </h1>
          <p className="text-lg text-gray-500">
            按主题探索我们的内容库
          </p>
        </motion.div>

        {/* Categories Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {categories.map((category, index) => (
            <motion.div
              key={category.name}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.5,
                delay: index * 0.1,
                ease: [0.22, 1, 0.36, 1],
              }}
            >
              <Link href={`/categories/${encodeURIComponent(category.name)}`}>
                <motion.div
                  className={`p-6 rounded-2xl border transition-all cursor-pointer ${colorMap[category.color]}`}
                  whileHover={{ y: -4, scale: 1.02 }}
                  transition={{ duration: 0.2 }}
                >
                  <div className="flex items-start justify-between mb-3">
                    <h2 className="text-xl font-medium">{category.name}</h2>
                    <span className="text-sm opacity-70">{category.count} 篇</span>
                  </div>
                  <p className="text-sm opacity-80 leading-relaxed">
                    {category.description}
                  </p>
                </motion.div>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>
    </main>
  )
}
