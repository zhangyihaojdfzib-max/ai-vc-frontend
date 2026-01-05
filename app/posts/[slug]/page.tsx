import { getPostBySlug, getPostSlugs } from '@/lib/posts'
import { notFound } from 'next/navigation'
import PostClient from './PostClient'

interface PostPageProps {
  params: Promise<{ slug: string }>
}

export async function generateStaticParams() {
  const slugs = getPostSlugs()
  return slugs.map((slug) => ({ slug }))
}

export default async function PostPage({ params }: PostPageProps) {
  const { slug } = await params
  const post = getPostBySlug(slug)

  if (!post) {
    notFound()
  }

  return <PostClient post={post} />
}
