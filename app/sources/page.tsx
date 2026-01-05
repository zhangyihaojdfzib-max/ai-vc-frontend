import { getAllPosts } from '@/lib/posts'
import SourcesClient from './SourcesClient'

// 源的元数据
const sourcesMeta: Record<string, { name: string; slug: string; description: string; type: 'vc' | 'investor' | 'research' | 'tech' }> = {
  'Y Combinator': { name: 'Y Combinator', slug: 'ycombinator', description: '全球最知名的创业加速器', type: 'vc' },
  'Sequoia Capital': { name: '红杉资本', slug: 'sequoia', description: '全球顶级风险投资基金', type: 'vc' },
  'Andreessen Horowitz': { name: 'a16z', slug: 'a16z', description: '硅谷顶级风投，专注科技投资', type: 'vc' },
  'Greylock Partners': { name: 'Greylock', slug: 'greylock', description: '专注早期投资的顶级基金', type: 'vc' },
  'Union Square Ventures': { name: 'USV', slug: 'usv', description: '纽约知名风投，专注网络效应', type: 'vc' },
  'Redpoint Ventures': { name: 'Redpoint', slug: 'redpoint', description: '专注技术领域的风险投资', type: 'vc' },
  'Lux Capital': { name: 'Lux Capital', slug: 'lux-capital', description: '专注科学与技术的风投', type: 'vc' },
  'Contrary': { name: 'Contrary', slug: 'contrary', description: '专注大学创业者的新锐基金', type: 'vc' },
  'Boldstart Ventures': { name: 'Boldstart', slug: 'boldstart', description: '专注企业软件的早期投资', type: 'vc' },
  'Unusual Ventures': { name: 'Unusual Ventures', slug: 'unusual-ventures', description: '专注 B2B 的早期基金', type: 'vc' },
  'NFX': { name: 'NFX', slug: 'nfx', description: '专注网络效应的种子基金', type: 'vc' },
  'Point Nine Capital': { name: 'Point Nine', slug: 'point-nine', description: '欧洲领先的 SaaS 投资基金', type: 'vc' },
  
  'Paul Graham': { name: 'Paul Graham', slug: 'paul-graham', description: 'YC 联合创始人，创业教父', type: 'investor' },
  'Sam Altman': { name: 'Sam Altman', slug: 'sam-altman', description: 'OpenAI CEO，前 YC 总裁', type: 'investor' },
  'Benedict Evans': { name: 'Benedict Evans', slug: 'benedict-evans', description: '科技行业分析师', type: 'investor' },
  'Fred Wilson': { name: 'Fred Wilson', slug: 'fred-wilson', description: 'USV 联合创始人', type: 'investor' },
  'Brad Feld': { name: 'Brad Feld', slug: 'brad-feld', description: 'Foundry Group 联合创始人', type: 'investor' },
  'Bill Gurley': { name: 'Bill Gurley', slug: 'bill-gurley', description: 'Benchmark 传奇投资人', type: 'investor' },
  'Andrew Chen': { name: 'Andrew Chen', slug: 'andrew-chen', description: 'a16z 合伙人，增长专家', type: 'investor' },
  'Hunter Walk': { name: 'Hunter Walk', slug: 'hunter-walk', description: 'Homebrew 联合创始人', type: 'investor' },
  'Tomasz Tunguz': { name: 'Tomasz Tunguz', slug: 'tomasz-tunguz', description: 'Theory Ventures 创始人', type: 'investor' },
  'SaaStr': { name: 'Jason Lemkin', slug: 'saastr', description: 'SaaStr 创始人，SaaS 专家', type: 'investor' },
  
  'Anthropic': { name: 'Anthropic', slug: 'anthropic', description: 'Claude AI 背后的公司', type: 'research' },
  'Google DeepMind': { name: 'DeepMind', slug: 'deepmind', description: 'Google 旗下 AI 研究实验室', type: 'research' },
  'Google AI': { name: 'Google AI', slug: 'google-ai', description: 'Google AI 研究博客', type: 'research' },
  'OpenAI': { name: 'OpenAI', slug: 'openai', description: 'ChatGPT 背后的公司', type: 'research' },
  'Meta AI': { name: 'Meta AI', slug: 'meta-ai', description: 'Meta AI 研究实验室', type: 'research' },
  'Microsoft Research': { name: 'Microsoft Research', slug: 'microsoft-research', description: '微软研究院', type: 'research' },
  'NVIDIA AI': { name: 'NVIDIA AI', slug: 'nvidia-ai', description: 'NVIDIA AI 技术博客', type: 'research' },
  'Hugging Face': { name: 'Hugging Face', slug: 'huggingface', description: '开源 AI 社区领导者', type: 'research' },
  'Berkeley AI Research': { name: 'BAIR', slug: 'bair', description: '伯克利 AI 研究实验室', type: 'research' },
  'Stanford HAI': { name: 'Stanford HAI', slug: 'stanford-hai', description: '斯坦福人本 AI 研究院', type: 'research' },
  'LangChain': { name: 'LangChain', slug: 'langchain', description: 'LLM 应用开发框架', type: 'research' },
  
  'Stripe': { name: 'Stripe', slug: 'stripe-blog', description: '全球领先的支付平台', type: 'tech' },
  'Cloudflare': { name: 'Cloudflare', slug: 'cloudflare-blog', description: '全球领先的网络安全公司', type: 'tech' },
  'Vercel': { name: 'Vercel', slug: 'vercel-blog', description: 'Next.js 背后的公司', type: 'tech' },
  'Spotify Engineering': { name: 'Spotify', slug: 'spotify-engineering', description: 'Spotify 工程技术博客', type: 'tech' },
  'Netflix Tech Blog': { name: 'Netflix', slug: 'netflix-tech', description: 'Netflix 技术博客', type: 'tech' },
  'Airbnb Engineering': { name: 'Airbnb', slug: 'airbnb-engineering', description: 'Airbnb 工程博客', type: 'tech' },
  'Discord': { name: 'Discord', slug: 'discord-engineering', description: 'Discord 技术博客', type: 'tech' },
  'Databricks': { name: 'Databricks', slug: 'databricks-blog', description: '大数据与 AI 平台', type: 'tech' },
  'Replicate': { name: 'Replicate', slug: 'replicate', description: 'AI 模型部署平台', type: 'tech' },
}

export default function SourcesPage() {
  const posts = getAllPosts()
  
  // 统计每个源的文章数
  const sourceCounts: Record<string, number> = {}
  posts.forEach(post => {
    const source = post.source
    sourceCounts[source] = (sourceCounts[source] || 0) + 1
  })
  
  // 构建源列表，按文章数排序
  const sources = Object.entries(sourcesMeta)
    .map(([key, meta]) => ({
      ...meta,
      originalName: key,
      count: sourceCounts[key] || 0
    }))
    .filter(s => s.count > 0)
    .sort((a, b) => b.count - a.count)
  
  return <SourcesClient sources={sources} />
}
