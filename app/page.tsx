import { getAllPosts } from '@/lib/posts'
import HomeClient from './HomeClient'

export default function HomePage() {
  const posts = getAllPosts()
  const featuredPosts = posts.slice(0, 5) // 取最新5篇
  
  return <HomeClient featuredPosts={featuredPosts} totalPosts={posts.length} />
}
