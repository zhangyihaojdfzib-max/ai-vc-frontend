import { getAllPosts, getAllCategories } from '@/lib/posts'
import HomeClient from './HomeClient'

export default function HomePage() {
  const posts = getAllPosts()
  const featuredPosts = posts.slice(0, 5)
  
  // 统计实际的源数量
  const sourcesSet = new Set(posts.map(p => p.source))
  const sources = Array.from(sourcesSet)
  
  // 统计分类数量
  const categories = getAllCategories()

  return (
    <HomeClient 
      featuredPosts={featuredPosts} 
      totalPosts={posts.length}
      totalSources={sources.length}
      topSources={sources.slice(0, 10)}
      totalCategories={categories.length}
    />
  )
}
