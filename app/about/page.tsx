'use client'

import { motion } from 'framer-motion'

export default function AboutPage() {
  return (
    <main className="min-h-screen py-24">
      <div className="max-w-3xl mx-auto px-6">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="mb-16"
        >
          <h1 className="text-4xl md:text-5xl font-serif text-gray-900 mb-4">
            关于本站
          </h1>
          <p className="text-lg text-gray-500">
            让中文读者与英文世界同步
          </p>
        </motion.div>

        {/* Content */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
          className="prose prose-lg max-w-none"
        >
          <section className="mb-12">
            <h2 className="text-2xl font-serif text-gray-900 mb-4">我们的使命</h2>
            <p className="text-gray-600 leading-relaxed mb-4">
              AI/VC前沿观察 致力于打破中英文信息壁垒，将全球顶级风险投资人、AI 研究机构和科技思想领袖的深度内容，以高质量的中文翻译形式呈现给中文读者。
            </p>
            <p className="text-gray-600 leading-relaxed">
              我们相信，及时获取一手信息对于创业者、投资人和科技从业者至关重要。通过自动化的内容管道，我们每日追踪、翻译并聚合最有价值的行业洞察。
            </p>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-serif text-gray-900 mb-4">内容来源</h2>
            <p className="text-gray-600 leading-relaxed mb-4">
              我们追踪的信息源包括但不限于：
            </p>
            <div className="grid grid-cols-2 gap-4 my-6">
              <div className="bg-gray-50 rounded-xl p-4">
                <h3 className="font-medium text-gray-900 mb-2">顶级 VC</h3>
                <p className="text-sm text-gray-500">
                  Sequoia, a16z, Y Combinator, Greylock, Benchmark 等
                </p>
              </div>
              <div className="bg-gray-50 rounded-xl p-4">
                <h3 className="font-medium text-gray-900 mb-2">AI 研究机构</h3>
                <p className="text-sm text-gray-500">
                  OpenAI, Anthropic, Google DeepMind, Meta AI 等
                </p>
              </div>
              <div className="bg-gray-50 rounded-xl p-4">
                <h3 className="font-medium text-gray-900 mb-2">知名投资人</h3>
                <p className="text-sm text-gray-500">
                  Paul Graham, Sam Altman, Benedict Evans 等
                </p>
              </div>
              <div className="bg-gray-50 rounded-xl p-4">
                <h3 className="font-medium text-gray-900 mb-2">科技博客</h3>
                <p className="text-sm text-gray-500">
                  Stratechery, Not Boring, The Generalist 等
                </p>
              </div>
            </div>
          </section>

          <section className="mb-12">
            <h2 className="text-2xl font-serif text-gray-900 mb-4">技术实现</h2>
            <p className="text-gray-600 leading-relaxed mb-4">
              本站采用全自动化的内容管道：
            </p>
            <ul className="space-y-2 text-gray-600">
              <li className="flex items-start gap-2">
                <span className="text-emerald-600 mt-1">•</span>
                <span><strong>内容抓取</strong>：通过 RSS 和 Sitemap 自动追踪信息源更新</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-600 mt-1">•</span>
                <span><strong>正文提取</strong>：使用 Trafilatura 智能提取文章正文</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-600 mt-1">•</span>
                <span><strong>AI 翻译</strong>：基于 DeepSeek 大模型进行高质量翻译</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-emerald-600 mt-1">•</span>
                <span><strong>自动发布</strong>：通过 GitHub Actions 每日自动更新</span>
              </li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-serif text-gray-900 mb-4">版权声明</h2>
            <p className="text-gray-600 leading-relaxed">
              本站所有翻译内容的原文版权归原作者所有。我们仅提供翻译服务，旨在促进知识传播。如有任何版权问题，请联系我们。
            </p>
          </section>
        </motion.div>
      </div>
    </main>
  )
}
