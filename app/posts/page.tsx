import { getAllPosts } from '@/lib/posts'
import PostsClient from './PostsClient'

export default function PostsPage() {
  const posts = getAllPosts()
  
  return <PostsClient posts={posts} />
}
