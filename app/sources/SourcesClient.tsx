'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'

interface Source {
  name: string
  slug: string
  description: string
  type: 'vc' | 'investor' | 'research' | 'tech'
  originalName: string
  count: number
}

interface SourcesClientProps {
  sources: Source[]
}

const typeLabels = {
  vc: { label: 'VC 基金', color: 'emerald' },
  investor: { label: '知名投资人', color: 'blue' },
  research: { label: 'AI 研究机构', color: 'purple' },
  tech: { label: '科技公司', color: 'orange' },
}

const colorClasses: Record<string, string> = {
  emerald: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  blue: 'bg-blue-50 text-blue-700 border-blue-200',
  purple: 'bg-purple-50 text-purple-700 border-purple-200',
  orange: 'bg-orange-50 text-orange-700 border-orange-200',
}

export default function SourcesClient({ sources }: SourcesClientProps) {
  // 按类型分组
  const grouped = {
    vc: sources.filter(s => s.type === 'vc'),
    investor: sources.filter(s => s.type === 'investor'),
    research: sources.filter(s => s.type === 'research'),
    tech: sources.filter(s => s.type === 'tech'),
  }

  const totalArticles = sources.reduce((sum, s) => sum + s.count, 0)

  return (
    <main className="min-h-screen py-24">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="mb-16 text-center"
        >
          <h1 className="text-4xl md:text-5xl font-serif text-gray-900 mb-4">
            内容源
          </h1>
          <p className="text-lg text-gray-500">
            {sources.length} 个信息源 · {totalArticles} 篇已翻译文章
          </p>
        </motion.div>

        {/* 按类型展示 */}
        {(['vc', 'investor', 'research', 'tech'] as const).map((type, typeIndex) => {
          const items = grouped[type]
          if (items.length === 0) return null
          
          const { label, color } = typeLabels[type]
          
          return (
            <motion.section
              key={type}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: typeIndex * 0.1 }}
              className="mb-16"
            >
              <h2 className="text-2xl font-serif text-gray-900 mb-8">{label}</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {items.map((source, index) => (
                  <motion.div
                    key={source.slug}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: typeIndex * 0.1 + index * 0.05 }}
                  >
                    <Link href={`/sources/${source.slug}`}>
                      <motion.div
                        className={`p-6 rounded-xl border transition-all cursor-pointer ${colorClasses[color]} hover:shadow-md`}
                        whileHover={{ y: -4, scale: 1.02 }}
                        transition={{ duration: 0.2 }}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <h3 className="text-lg font-medium">{source.name}</h3>
                          <span className="text-sm opacity-70">{source.count} 篇</span>
                        </div>
                        <p className="text-sm opacity-80 leading-relaxed">
                          {source.description}
                        </p>
                      </motion.div>
                    </Link>
                  </motion.div>
                ))}
              </div>
            </motion.section>
          )
        })}
      </div>
    </main>
  )
}
