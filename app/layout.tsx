import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Analytics } from '@vercel/analytics/next'
import './globals.css'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import SmoothScroll from '@/components/animations/SmoothScroll'

const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
  variable: '--font-inter',
})

export const metadata: Metadata = {
  title: 'AI/VC前沿观察 | 每日AI与创投深度内容',
  description: '每日自动追踪、翻译并聚合全球顶级的AI、VC与创业领域深度内容。',
  keywords: ['AI', 'VC', '创业', '风险投资', '人工智能', '科技', '翻译'],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN" className={inter.variable}>
      <body className="font-sans antialiased bg-white text-gray-900">
        <SmoothScroll>
          <Header />
          <div className="min-h-screen pt-20">
            {children}
          </div>
          <Footer />
        </SmoothScroll>
        <Analytics />
      </body>
    </html>
  )
}
