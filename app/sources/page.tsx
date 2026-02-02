import { getAllPosts } from '@/lib/posts'
import SourcesClient from './SourcesClient'

const sourcesMeta: Record<string, { name: string; slug: string; description: string; type: 'vc' | 'investor' | 'research' | 'tech' }> = {
  // VC 基金
  'First Round Review': { name: 'First Round Review', slug: 'first-round-review', description: 'First Round Capital 的深度内容平台', type: 'vc' },
  'Y Combinator': { name: 'Y Combinator', slug: 'ycombinator', description: '全球最知名的创业加速器', type: 'vc' },
  'Sequoia Capital': { name: '红杉资本', slug: 'sequoia', description: '全球顶级风险投资基金', type: 'vc' },
  '红杉资本 (Sequoia)': { name: '红杉资本', slug: 'sequoia', description: '全球顶级风险投资基金', type: 'vc' },
  'Greylock Partners': { name: 'Greylock', slug: 'greylock', description: '专注早期投资的顶级基金', type: 'vc' },
  'Union Square Ventures': { name: 'USV', slug: 'usv', description: '纽约知名风投，专注网络效应', type: 'vc' },
  'Boldstart Ventures': { name: 'Boldstart', slug: 'boldstart', description: '专注企业软件的早期投资', type: 'vc' },
  'Unusual Ventures': { name: 'Unusual Ventures', slug: 'unusual-ventures', description: '专注 B2B 的早期基金', type: 'vc' },
  'Andreessen Horowitz (a16z)': { name: 'a16z', slug: 'a16z', description: '硅谷顶级风投，投资了 Facebook、Airbnb', type: 'vc' },

  // 知名投资人
  'Benedict Evans': { name: 'Benedict Evans', slug: 'benedict-evans', description: '科技行业分析师', type: 'investor' },
  'Fred Wilson': { name: 'Fred Wilson', slug: 'fred-wilson', description: 'USV 联合创始人', type: 'investor' },
  'Fred Wilson (AVC)': { name: 'Fred Wilson', slug: 'fred-wilson', description: 'USV 联合创始人', type: 'investor' },
  'Brad Feld': { name: 'Brad Feld', slug: 'brad-feld', description: 'Foundry Group 联合创始人', type: 'investor' },
  'Bill Gurley': { name: 'Bill Gurley', slug: 'bill-gurley', description: 'Benchmark 传奇投资人', type: 'investor' },
  'Andrew Chen': { name: 'Andrew Chen', slug: 'andrew-chen', description: 'a16z 合伙人，增长专家', type: 'investor' },
  'Hunter Walk': { name: 'Hunter Walk', slug: 'hunter-walk', description: 'Homebrew 联合创始人', type: 'investor' },
  'Tomasz Tunguz': { name: 'Tomasz Tunguz', slug: 'tomasz-tunguz', description: 'Theory Ventures 创始人', type: 'investor' },
  'Jason Lemkin (SaaStr)': { name: 'Jason Lemkin', slug: 'saastr', description: 'SaaStr 创始人，SaaS 专家', type: 'investor' },
  'Sam Altman': { name: 'Sam Altman', slug: 'sam-altman', description: 'OpenAI CEO，前 YC 总裁', type: 'investor' },

  // AI 研究
  'Anthropic': { name: 'Anthropic', slug: 'anthropic', description: 'Claude AI 背后的公司', type: 'research' },
  'OpenAI': { name: 'OpenAI', slug: 'openai', description: 'GPT 和 ChatGPT 背后的公司', type: 'research' },
  'Google DeepMind': { name: 'DeepMind', slug: 'deepmind', description: 'Google 旗下 AI 研究实验室', type: 'research' },
  'Google AI Blog': { name: 'Google AI', slug: 'google-ai', description: 'Google AI 研究博客', type: 'research' },
  'Microsoft Research': { name: 'Microsoft Research', slug: 'microsoft-research', description: '微软研究院', type: 'research' },
  'NVIDIA AI Blog': { name: 'NVIDIA AI', slug: 'nvidia-ai', description: 'NVIDIA AI 技术博客', type: 'research' },
  'Hugging Face Blog': { name: 'Hugging Face', slug: 'huggingface', description: '开源 AI 社区领导者', type: 'research' },
  'Hugging Face': { name: 'Hugging Face', slug: 'huggingface', description: '开源 AI 社区领导者', type: 'research' },
  'Berkeley AI Research (BAIR)': { name: 'BAIR', slug: 'bair', description: '伯克利 AI 研究实验室', type: 'research' },
  'LangChain': { name: 'LangChain', slug: 'langchain', description: 'LLM 应用开发框架', type: 'research' },
  'LangChain Blog': { name: 'LangChain', slug: 'langchain', description: 'LLM 应用开发框架', type: 'research' },

  // 科技公司博客
  'Stripe Blog': { name: 'Stripe', slug: 'stripe-blog', description: '全球领先的支付平台', type: 'tech' },
  'Cloudflare Blog': { name: 'Cloudflare', slug: 'cloudflare-blog', description: '全球领先的网络安全公司', type: 'tech' },
  'Vercel Blog': { name: 'Vercel', slug: 'vercel-blog', description: 'Next.js 背后的公司', type: 'tech' },
  'Spotify Engineering': { name: 'Spotify', slug: 'spotify-engineering', description: 'Spotify 工程技术博客', type: 'tech' },
  'Discord Engineering': { name: 'Discord', slug: 'discord-engineering', description: 'Discord 技术博客', type: 'tech' },
  'Databricks Blog': { name: 'Databricks', slug: 'databricks-blog', description: '大数据与 AI 平台', type: 'tech' },
  'Replicate Blog': { name: 'Replicate', slug: 'replicate', description: 'AI 模型部署平台', type: 'tech' },
}

export default function SourcesPage() {
  const posts = getAllPosts()

  const sourceCounts: Record<string, number> = {}
  posts.forEach(post => {
    const source = post.source
    sourceCounts[source] = (sourceCounts[source] || 0) + 1
  })

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
