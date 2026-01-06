import { getAllCategories, getAllPosts } from '@/lib/posts'
import CategoriesClient from './CategoriesClient'

export const metadata = {
  title: '分类浏览 | AI/VC 前沿观察',
  description: '按主题探索我们的内容库',
}

const categoryConfig: Record<string, { color: string; description: string }> = {
  'AI研究': { color: 'emerald', description: '人工智能前沿研究、大模型技术、机器学习进展' },
  'AI产品': { color: 'blue', description: 'AI 应用产品分析、商业化案例、产品策略' },
  '技术趋势': { color: 'purple', description: '科技行业宏观趋势、技术演进、行业预测' },
  'AI基础设施': { color: 'cyan', description: 'AI 基础设施、云计算、芯片、训练平台' },
  '创业': { color: 'orange', description: '创业方法论、公司建设、融资策略、团队管理' },
  'VC观点': { color: 'pink', description: '风险投资人的行业洞察、投资趋势、市场分析' },
  'VC动态': { color: 'rose', description: '风险投资行业动态、基金募集、投资案例' },
  '创业方法论': { color: 'amber', description: '创业实战方法、增长策略、运营技巧' },
  '科技趋势': { color: 'indigo', description: '科技行业发展趋势、前沿技术展望' },
  '市场分析': { color: 'teal', description: '市场研究、行业分析、竞争格局' },
  '工程实践': { color: 'slate', description: '软件工程最佳实践、技术架构、开发经验' },
  '政策监管': { color: 'red', description: 'AI 政策法规、行业监管、合规要求' },
  '未分类': { color: 'gray', description: '其他精选内容' },
}

const defaultConfig = { color: 'gray', description: '精选内容' }

export default function CategoriesPage() {
  const categories = getAllCategories()
  const totalPosts = getAllPosts().length

  const categoriesWithConfig = categories.map(cat => ({
    name: cat.name,
    count: cat.count,
    slug: cat.name,
    ...(categoryConfig[cat.name] || defaultConfig)
  }))

  return <CategoriesClient categories={categoriesWithConfig} totalPosts={totalPosts} />
}
