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
  mtime: number
}

function ensureDirectoryExists() {
  if (!fs.existsSync(postsDirectory)) {
    fs.mkdirSync(postsDirectory, { recursive: true })
  }
}

// 将日期转换为字符串
function formatDate(date: unknown): string {
  if (!date) return ''
  if (date instanceof Date) {
    return date.toISOString().split('T')[0]
  }
  return String(date)
}

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
    title: String(data.title || ''),
    title_original: data.title_original ? String(data.title_original) : undefined,
    date: formatDate(data.date),
    source: String(data.source || ''),
    source_url: data.source_url ? String(data.source_url) : undefined,
    author: data.author ? String(data.author) : undefined,
    summary: String(data.summary || ''),
    categories: Array.isArray(data.categories) ? data.categories.map(String) : [],
    tags: Array.isArray(data.tags) ? data.tags.map(String) : [],
    content,
    readingTime: `${Math.ceil(stats.minutes)} 分钟`,
  }
}

export function getAllPosts(): PostMeta[] {
  const slugs = getPostSlugs()

  const posts = slugs
    .map((slug) => {
      const post = getPostBySlug(slug)
      if (!post) return null
      
      // 获取文件修改时间
      const fullPath = path.join(process.cwd(), 'content/posts', `${slug}.md`)
      const stat = fs.statSync(fullPath)
      const mtime = stat.mtimeMs || 0

      return {
        slug: post.slug,
        title: post.title,
        date: post.date,
        source: post.source,
        summary: post.summary,
        categories: post.categories,
        tags: post.tags,
        readingTime: post.readingTime,
        mtime,
      }
    })
    .filter((post): post is PostMeta => post !== null)
    .sort((a, b) => {
      const dateA = new Date(a.date).getTime()
      const dateB = new Date(b.date).getTime()
      if (dateA !== dateB) return dateB - dateA
      // 同一天的文章按文件修改时间降序（最新翻译的排前面）
      return (b.mtime || 0) - (a.mtime || 0)
    })

  return posts
}

export function getPostsByCategory(category: string): PostMeta[] {
  const posts = getAllPosts()
  return posts.filter((post) => post.categories.includes(category))
}

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
