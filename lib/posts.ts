import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import readingTime from 'reading-time'

const postsDirectory = path.join(process.cwd(), 'content/posts')

export interface Post {
  slug: string
  title: string
  title_original?: string
  date: string
  source: string
  source_url?: string
  author?: string
  summary: string
  categories: string[]
  tags: string[]
  content: string
  readingTime: string
}

export interface PostMeta {
  slug: string
  title: string
  date: string
  source: string
  summary: string
  categories: string[]
  tags: string[]
  readingTime: string
}

// 确保目录存在
function ensureDirectoryExists() {
  if (!fs.existsSync(postsDirectory)) {
    fs.mkdirSync(postsDirectory, { recursive: true })
  }
}

// 获取所有文章的 slug
export function getPostSlugs(): string[] {
  ensureDirectoryExists()
  
  try {
    const files = fs.readdirSync(postsDirectory)
    return files
      .filter((file) => file.endsWith('.md'))
      .map((file) => file.replace(/\.md$/, ''))
  } catch {
    return []
  }
}

// 根据 slug 获取单篇文章
export function getPostBySlug(slug: string): Post | null {
  ensureDirectoryExists()
  
  const fullPath = path.join(postsDirectory, `${slug}.md`)
  
  if (!fs.existsSync(fullPath)) {
    return null
  }

  const fileContents = fs.readFileSync(fullPath, 'utf8')
  const { data, content } = matter(fileContents)
  const stats = readingTime(content)

  return {
    slug,
    title: data.title || '',
    title_original: data.title_original,
    date: data.date || '',
    source: data.source || '',
    source_url: data.source_url,
    author: data.author,
    summary: data.summary || '',
    categories: data.categories || [],
    tags: data.tags || [],
    content,
    readingTime: `${Math.ceil(stats.minutes)} 分钟`,
  }
}

// 获取所有文章元数据（用于列表页）
export function getAllPosts(): PostMeta[] {
  const slugs = getPostSlugs()
  
  const posts = slugs
    .map((slug) => {
      const post = getPostBySlug(slug)
      if (!post) return null
      
      return {
        slug: post.slug,
        title: post.title,
        date: post.date,
        source: post.source,
        summary: post.summary,
        categories: post.categories,
        tags: post.tags,
        readingTime: post.readingTime,
      }
    })
    .filter((post): post is PostMeta => post !== null)
    .sort((a, b) => (new Date(b.date).getTime() - new Date(a.date).getTime()))

  return posts
}

// 按分类获取文章
export function getPostsByCategory(category: string): PostMeta[] {
  const posts = getAllPosts()
  return posts.filter((post) => post.categories.includes(category))
}

// 获取所有分类
export function getAllCategories(): { name: string; count: number }[] {
  const posts = getAllPosts()
  const categoryCount: Record<string, number> = {}

  posts.forEach((post) => {
    post.categories.forEach((category) => {
      categoryCount[category] = (categoryCount[category] || 0) + 1
    })
  })

  return Object.entries(categoryCount)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
}

// 获取所有标签
export function getAllTags(): { name: string; count: number }[] {
  const posts = getAllPosts()
  const tagCount: Record<string, number> = {}

  posts.forEach((post) => {
    post.tags.forEach((tag) => {
      tagCount[tag] = (tagCount[tag] || 0) + 1
    })
  })

  return Object.entries(tagCount)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
}
