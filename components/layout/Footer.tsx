import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="border-t border-gray-100 bg-gray-50/50">
      <div className="max-w-6xl mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
          {/* Brand */}
          <div className="md:col-span-2">
            <Link href="/" className="text-xl font-semibold tracking-tight">
              AI/VC<span className="text-emerald-600">前沿观察</span>
            </Link>
            <p className="mt-4 text-gray-500 text-sm leading-relaxed max-w-md">
              每日自动追踪、翻译并聚合全球顶级的AI、VC与创业领域深度内容。
              让中文读者与英文世界同步。
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="font-medium text-gray-900 mb-4">导航</h4>
            <ul className="space-y-3 text-sm">
              <li>
                <Link href="/posts" className="text-gray-500 hover:text-gray-900 transition-colors">
                  全部文章
                </Link>
              </li>
              <li>
                <Link href="/categories" className="text-gray-500 hover:text-gray-900 transition-colors">
                  分类浏览
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-gray-500 hover:text-gray-900 transition-colors">
                  关于本站
                </Link>
              </li>
            </ul>
          </div>

          {/* Sources */}
          <div>
            <h4 className="font-medium text-gray-900 mb-4">内容来源</h4>
            <ul className="space-y-3 text-sm">
              <li className="text-gray-500">Sequoia Capital</li>
              <li className="text-gray-500">Y Combinator</li>
              <li className="text-gray-500">a16z</li>
              <li className="text-gray-500">+40 more sources</li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="mt-16 pt-8 border-t border-gray-200 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm text-gray-400">
            © 2025 AI/VC前沿观察. 内容版权归原作者所有.
          </p>
          <p className="text-sm text-gray-400">
            Powered by Next.js & DeepSeek
          </p>
        </div>
      </div>
    </footer>
  )
}
