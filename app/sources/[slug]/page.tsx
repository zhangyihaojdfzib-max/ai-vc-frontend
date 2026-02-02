import { getAllPosts, PostMeta } from '@/lib/posts'
import { notFound } from 'next/navigation'
import SourceDetailClient from './SourceDetailClient'

// 源的元数据映射（slug -> 显示信息）
const sourcesMeta: Record<string, { name: string; fullName: string; description: string; website?: string }> = {
  'first-round-review': { name: 'First Round Review', fullName: 'First Round Review', description: 'First Round Capital 的深度内容平台，提供创业者和管理者的实战经验分享。', website: 'https://review.firstround.com' },
  'ycombinator': { name: 'Y Combinator', fullName: 'Y Combinator', description: '全球最知名的创业加速器，孵化了 Airbnb、Stripe、Dropbox 等众多独角兽公司。', website: 'https://www.ycombinator.com' },
  'sequoia': { name: '红杉资本', fullName: 'Sequoia Capital', description: '全球顶级风险投资基金，投资了 Apple、Google、WhatsApp 等传奇公司。', website: 'https://www.sequoiacap.com' },
  'a16z': { name: 'a16z', fullName: 'Andreessen Horowitz', description: '硅谷顶级风投，由 Marc Andreessen 和 Ben Horowitz 创立，专注科技投资。', website: 'https://a16z.com' },
  'greylock': { name: 'Greylock', fullName: 'Greylock Partners', description: '成立于 1965 年的顶级风投，投资了 LinkedIn、Facebook、Discord 等公司。', website: 'https://greylock.com' },
  'usv': { name: 'USV', fullName: 'Union Square Ventures', description: '纽约知名风投，专注网络效应驱动的公司，投资了 Twitter、Coinbase 等。', website: 'https://www.usv.com' },
  'redpoint': { name: 'Redpoint', fullName: 'Redpoint Ventures', description: '专注技术领域的风险投资基金。', website: 'https://www.redpoint.com' },
  'lux-capital': { name: 'Lux Capital', fullName: 'Lux Capital', description: '专注科学与技术的风险投资基金。', website: 'https://www.luxcapital.com' },
  'contrary': { name: 'Contrary', fullName: 'Contrary', description: '专注大学创业者的新锐基金。', website: 'https://contrary.com' },
  'boldstart': { name: 'Boldstart', fullName: 'Boldstart Ventures', description: '专注企业软件的早期投资基金。', website: 'https://boldstart.vc' },
  'unusual-ventures': { name: 'Unusual Ventures', fullName: 'Unusual Ventures', description: '专注 B2B 的早期投资基金。', website: 'https://www.unusual.vc' },
  'nfx': { name: 'NFX', fullName: 'NFX', description: '专注网络效应的种子基金。', website: 'https://www.nfx.com' },
  'point-nine': { name: 'Point Nine', fullName: 'Point Nine Capital', description: '欧洲领先的 SaaS 投资基金。', website: 'https://www.pointnine.com' },
  
  'paul-graham': { name: 'Paul Graham', fullName: 'Paul Graham', description: 'Y Combinator 联合创始人，程序员、作家，创业教父级人物。', website: 'http://paulgraham.com' },
  'sam-altman': { name: 'Sam Altman', fullName: 'Sam Altman', description: 'OpenAI CEO，前 Y Combinator 总裁。', website: 'https://blog.samaltman.com' },
  'benedict-evans': { name: 'Benedict Evans', fullName: 'Benedict Evans', description: '科技行业分析师，前 a16z 合伙人。', website: 'https://www.ben-evans.com' },
  'fred-wilson': { name: 'Fred Wilson', fullName: 'Fred Wilson (AVC)', description: 'Union Square Ventures 联合创始人，知名博主。', website: 'https://avc.com' },
  'brad-feld': { name: 'Brad Feld', fullName: 'Brad Feld', description: 'Foundry Group 联合创始人，Techstars 联合创始人。', website: 'https://feld.com' },
  'bill-gurley': { name: 'Bill Gurley', fullName: 'Bill Gurley', description: 'Benchmark 传奇投资人，投资了 Uber 等公司。', website: 'https://abovethecrowd.com' },
  'andrew-chen': { name: 'Andrew Chen', fullName: 'Andrew Chen', description: 'a16z 普通合伙人，增长专家。', website: 'https://andrewchen.com' },
  'hunter-walk': { name: 'Hunter Walk', fullName: 'Hunter Walk', description: 'Homebrew 联合创始人，前 YouTube 产品总监。', website: 'https://hunterwalk.com' },
  'tomasz-tunguz': { name: 'Tomasz Tunguz', fullName: 'Tomasz Tunguz', description: 'Theory Ventures 创始人，数据驱动的 SaaS 投资人。', website: 'https://tomtunguz.com' },
  'saastr': { name: 'Jason Lemkin', fullName: 'SaaStr (Jason Lemkin)', description: 'SaaStr 创始人，SaaS 领域最具影响力的人物之一。', website: 'https://www.saastr.com' },
  
  'anthropic': { name: 'Anthropic', fullName: 'Anthropic', description: 'AI 安全公司，Claude AI 的创造者。', website: 'https://www.anthropic.com' },
  'deepmind': { name: 'DeepMind', fullName: 'Google DeepMind', description: 'Google 旗下 AI 研究实验室，AlphaGo 的创造者。', website: 'https://deepmind.google' },
  'google-ai': { name: 'Google AI', fullName: 'Google AI Blog', description: 'Google AI 研究博客。', website: 'https://ai.googleblog.com' },
  'openai': { name: 'OpenAI', fullName: 'OpenAI', description: 'ChatGPT 和 GPT-4 的创造者。', website: 'https://openai.com' },
  'meta-ai': { name: 'Meta AI', fullName: 'Meta AI', description: 'Meta AI 研究实验室，LLaMA 模型的创造者。', website: 'https://ai.meta.com' },
  'microsoft-research': { name: 'Microsoft Research', fullName: 'Microsoft Research', description: '微软研究院，全球顶级企业研究机构。', website: 'https://www.microsoft.com/research' },
  'nvidia-ai': { name: 'NVIDIA AI', fullName: 'NVIDIA AI Blog', description: 'NVIDIA AI 技术博客。', website: 'https://blogs.nvidia.com' },
  'huggingface': { name: 'Hugging Face', fullName: 'Hugging Face', description: '开源 AI 社区领导者，Transformers 库的创造者。', website: 'https://huggingface.co' },
  'bair': { name: 'BAIR', fullName: 'Berkeley AI Research', description: '伯克利大学 AI 研究实验室。', website: 'https://bair.berkeley.edu' },
  'berkeley-ai': { name: 'BAIR', fullName: 'Berkeley AI Research', description: '伯克利大学 AI 研究实验室。', website: 'https://bair.berkeley.edu' },
  'stanford-hai': { name: 'Stanford HAI', fullName: 'Stanford Human-Centered AI', description: '斯坦福大学人本 AI 研究院。', website: 'https://hai.stanford.edu' },
  'langchain': { name: 'LangChain', fullName: 'LangChain Blog', description: 'LLM 应用开发框架。', website: 'https://blog.langchain.dev' },
  
  'stripe-blog': { name: 'Stripe', fullName: 'Stripe Blog', description: '全球领先的支付平台。', website: 'https://stripe.com' },
  'cloudflare-blog': { name: 'Cloudflare', fullName: 'Cloudflare Blog', description: '全球领先的网络安全和性能公司。', website: 'https://www.cloudflare.com' },
  'vercel-blog': { name: 'Vercel', fullName: 'Vercel Blog', description: 'Next.js 背后的公司，前端云平台。', website: 'https://vercel.com' },
  'spotify-engineering': { name: 'Spotify', fullName: 'Spotify Engineering', description: 'Spotify 工程技术博客。', website: 'https://engineering.atspotify.com' },
  'netflix-tech': { name: 'Netflix', fullName: 'Netflix Tech Blog', description: 'Netflix 技术博客。', website: 'https://netflixtechblog.com' },
  'airbnb-engineering': { name: 'Airbnb', fullName: 'Airbnb Engineering', description: 'Airbnb 工程博客。', website: 'https://medium.com/airbnb-engineering' },
  'discord-engineering': { name: 'Discord', fullName: 'Discord Blog', description: 'Discord 官方博客。', website: 'https://discord.com/blog' },
  'databricks-blog': { name: 'Databricks', fullName: 'Databricks Blog', description: '大数据与 AI 平台。', website: 'https://www.databricks.com/blog' },
  'replicate': { name: 'Replicate', fullName: 'Replicate Blog', description: 'AI 模型部署平台。', website: 'https://replicate.com/blog' },
}

// 从文章的 source 字段反向映射到 slug
const sourceNameToSlug: Record<string, string> = {
  'First Round Review': 'first-round-review',
  'Y Combinator': 'ycombinator',
  'Sequoia Capital': 'sequoia',
  'Andreessen Horowitz': 'a16z',
  'Greylock Partners': 'greylock',
  'Union Square Ventures': 'usv',
  'Redpoint Ventures': 'redpoint',
  'Lux Capital': 'lux-capital',
  'Contrary': 'contrary',
  'Boldstart Ventures': 'boldstart',
  'Unusual Ventures': 'unusual-ventures',
  'NFX': 'nfx',
  'Point Nine Capital': 'point-nine',
  'Paul Graham': 'paul-graham',
  'Sam Altman': 'sam-altman',
  'Benedict Evans': 'benedict-evans',
  'Fred Wilson (AVC)': 'fred-wilson',
  'Brad Feld': 'brad-feld',
  'Bill Gurley': 'bill-gurley',
  'Andrew Chen': 'andrew-chen',
  'Hunter Walk': 'hunter-walk',
  'Tomasz Tunguz': 'tomasz-tunguz',
  'SaaStr': 'saastr',
  'Anthropic': 'anthropic',
  'Google DeepMind': 'deepmind',
  'Google AI': 'google-ai',
  'OpenAI': 'openai',
  'Meta AI': 'meta-ai',
  'Microsoft Research': 'microsoft-research',
  'NVIDIA AI': 'nvidia-ai',
  'Hugging Face': 'huggingface',
  'Berkeley AI Research': 'bair',
  'Stanford HAI': 'stanford-hai',
  'LangChain': 'langchain',
  'Stripe': 'stripe-blog',
  'Cloudflare': 'cloudflare-blog',
  'Vercel': 'vercel-blog',
  'Spotify Engineering': 'spotify-engineering',
  'Netflix Tech Blog': 'netflix-tech',
  'Airbnb Engineering': 'airbnb-engineering',
  'Discord': 'discord-engineering',
  'Databricks': 'databricks-blog',
  'Replicate': 'replicate',
  '红杉资本 (Sequoia)': 'sequoia',
  'Andreessen Horowitz (a16z)': 'a16z',
  'Jason Lemkin (SaaStr)': 'saastr',
  'Google AI Blog': 'google-ai',
  'NVIDIA AI Blog': 'nvidia-ai',
  'Hugging Face Blog': 'huggingface',
  'Berkeley AI Research (BAIR)': 'bair',
  'LangChain Blog': 'langchain',
  'Stripe Blog': 'stripe-blog',
  'Cloudflare Blog': 'cloudflare-blog',
  'Vercel Blog': 'vercel-blog',
  'Discord Engineering': 'discord-engineering',
  'Databricks Blog': 'databricks-blog',
  'Replicate Blog': 'replicate',
}

// 反向映射：slug -> source names
const slugToSourceNames: Record<string, string[]> = {}
Object.entries(sourceNameToSlug).forEach(([name, slug]) => {
  if (!slugToSourceNames[slug]) {
    slugToSourceNames[slug] = []
  }
  slugToSourceNames[slug].push(name)
})

interface SourcePageProps {
  params: Promise<{ slug: string }>
}

export async function generateStaticParams() {
  return Object.keys(sourcesMeta).map(slug => ({ slug }))
}

export default async function SourcePage({ params }: SourcePageProps) {
  const { slug } = await params
  const meta = sourcesMeta[slug]
  
  if (!meta) {
    notFound()
  }
  
  const allPosts = getAllPosts()
  const sourceNames = slugToSourceNames[slug] || []
  
  // 筛选属于这个源的文章
  const posts = allPosts.filter(post => 
    sourceNames.some(name => post.source.includes(name) || post.source === name)
  )
  
  return <SourceDetailClient meta={meta} slug={slug} posts={posts} />
}
