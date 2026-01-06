import { getAllCategories, getPostsByCategory } from '@/lib/posts'
import { notFound } from 'next/navigation'
import CategoryDetailClient from './CategoryDetailClient'

interface Props {
  params: Promise<{ slug: string }>
}

export async function generateStaticParams() {
  const categories = getAllCategories()
  return categories.map((cat) => ({
    slug: encodeURIComponent(cat.name),
  }))
}

export async function generateMetadata({ params }: Props) {
  const { slug } = await params
  const categoryName = decodeURIComponent(slug)
  return {
    title: `${categoryName} | AI/VC 前沿观察`,
    description: `浏览 ${categoryName} 分类下的所有文章`,
  }
}

export default async function CategoryPage({ params }: Props) {
  const { slug } = await params
  const categoryName = decodeURIComponent(slug)
  const posts = getPostsByCategory(categoryName)

  if (posts.length === 0) {
    notFound()
  }

  return <CategoryDetailClient categoryName={categoryName} posts={posts} />
}
