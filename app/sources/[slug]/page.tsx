import { getAllPosts, PostMeta } from '@/lib/posts'
import { notFound } from 'next/navigation'
import SourceDetailClient from './SourceDetailClient'

// æºçš„å…ƒæ•°æ®æ˜ å°„ï¼ˆslug -> æ˜¾ç¤ºä¿¡æ¯ï¼‰
const sourcesMeta: Record<string, { name: string; fullName: string; description: string; website?: string }> = {
  'ycombinator': { name: 'Y Combinator', fullName: 'Y Combinator', description: 'å…¨çƒæœ€çŸ¥åçš„åˆ›ä¸šåŠ é€Ÿå™¨ï¼Œå­µåŒ–äº† Airbnbã€Stripeã€Dropbox ç­‰ä¼—å¤šç‹¬è§’å…½å…¬å¸ã€‚', website: 'https://www.ycombinator.com' },
  'sequoia': { name: 'çº¢æ‰èµ„æœ¬', fullName: 'Sequoia Capital', description: 'å…¨çƒé¡¶çº§é£Žé™©æŠ•èµ„åŸºé‡‘ï¼ŒæŠ•èµ„äº† Appleã€Googleã€WhatsApp ç­‰ä¼ å¥‡å…¬å¸ã€‚', website: 'https://www.sequoiacap.com' },
  'a16z': { name: 'a16z', fullName: 'Andreessen Horowitz', description: 'ç¡…è°·é¡¶çº§é£ŽæŠ•ï¼Œç”± Marc Andreessen å’Œ Ben Horowitz åˆ›ç«‹ï¼Œä¸“æ³¨ç§‘æŠ€æŠ•èµ„ã€‚', website: 'https://a16z.com' },
  'greylock': { name: 'Greylock', fullName: 'Greylock Partners', description: 'æˆç«‹äºŽ 1965 å¹´çš„é¡¶çº§é£ŽæŠ•ï¼ŒæŠ•èµ„äº† LinkedInã€Facebookã€Discord ç­‰å…¬å¸ã€‚', website: 'https://greylock.com' },
  'usv': { name: 'USV', fullName: 'Union Square Ventures', description: 'çº½çº¦çŸ¥åé£ŽæŠ•ï¼Œä¸“æ³¨ç½‘ç»œæ•ˆåº”é©±åŠ¨çš„å…¬å¸ï¼ŒæŠ•èµ„äº† Twitterã€Coinbase ç­‰ã€‚', website: 'https://www.usv.com' },
  'redpoint': { name: 'Redpoint', fullName: 'Redpoint Ventures', description: 'ä¸“æ³¨æŠ€æœ¯é¢†åŸŸçš„é£Žé™©æŠ•èµ„åŸºé‡‘ã€‚', website: 'https://www.redpoint.com' },
  'lux-capital': { name: 'Lux Capital', fullName: 'Lux Capital', description: 'ä¸“æ³¨ç§‘å­¦ä¸ŽæŠ€æœ¯çš„é£Žé™©æŠ•èµ„åŸºé‡‘ã€‚', website: 'https://www.luxcapital.com' },
  'contrary': { name: 'Contrary', fullName: 'Contrary', description: 'ä¸“æ³¨å¤§å­¦åˆ›ä¸šè€…çš„æ–°é”åŸºé‡‘ã€‚', website: 'https://contrary.com' },
  'boldstart': { name: 'Boldstart', fullName: 'Boldstart Ventures', description: 'ä¸“æ³¨ä¼ä¸šè½¯ä»¶çš„æ—©æœŸæŠ•èµ„åŸºé‡‘ã€‚', website: 'https://boldstart.vc' },
  'unusual-ventures': { name: 'Unusual Ventures', fullName: 'Unusual Ventures', description: 'ä¸“æ³¨ B2B çš„æ—©æœŸæŠ•èµ„åŸºé‡‘ã€‚', website: 'https://www.unusual.vc' },
  'nfx': { name: 'NFX', fullName: 'NFX', description: 'ä¸“æ³¨ç½‘ç»œæ•ˆåº”çš„ç§å­åŸºé‡‘ã€‚', website: 'https://www.nfx.com' },
  'point-nine': { name: 'Point Nine', fullName: 'Point Nine Capital', description: 'æ¬§æ´²é¢†å…ˆçš„ SaaS æŠ•èµ„åŸºé‡‘ã€‚', website: 'https://www.pointnine.com' },
  
  'paul-graham': { name: 'Paul Graham', fullName: 'Paul Graham', description: 'Y Combinator è”åˆåˆ›å§‹äººï¼Œç¨‹åºå‘˜ã€ä½œå®¶ï¼Œåˆ›ä¸šæ•™çˆ¶çº§äººç‰©ã€‚', website: 'http://paulgraham.com' },
  'sam-altman': { name: 'Sam Altman', fullName: 'Sam Altman', description: 'OpenAI CEOï¼Œå‰ Y Combinator æ€»è£ã€‚', website: 'https://blog.samaltman.com' },
  'benedict-evans': { name: 'Benedict Evans', fullName: 'Benedict Evans', description: 'ç§‘æŠ€è¡Œä¸šåˆ†æžå¸ˆï¼Œå‰ a16z åˆä¼™äººã€‚', website: 'https://www.ben-evans.com' },
  'fred-wilson': { name: 'Fred Wilson', fullName: 'Fred Wilson (AVC)', description: 'Union Square Ventures è”åˆåˆ›å§‹äººï¼ŒçŸ¥ååšä¸»ã€‚', website: 'https://avc.com' },
  'brad-feld': { name: 'Brad Feld', fullName: 'Brad Feld', description: 'Foundry Group è”åˆåˆ›å§‹äººï¼ŒTechstars è”åˆåˆ›å§‹äººã€‚', website: 'https://feld.com' },
  'bill-gurley': { name: 'Bill Gurley', fullName: 'Bill Gurley', description: 'Benchmark ä¼ å¥‡æŠ•èµ„äººï¼ŒæŠ•èµ„äº† Uber ç­‰å…¬å¸ã€‚', website: 'https://abovethecrowd.com' },
  'andrew-chen': { name: 'Andrew Chen', fullName: 'Andrew Chen', description: 'a16z æ™®é€šåˆä¼™äººï¼Œå¢žé•¿ä¸“å®¶ã€‚', website: 'https://andrewchen.com' },
  'hunter-walk': { name: 'Hunter Walk', fullName: 'Hunter Walk', description: 'Homebrew è”åˆåˆ›å§‹äººï¼Œå‰ YouTube äº§å“æ€»ç›‘ã€‚', website: 'https://hunterwalk.com' },
  'tomasz-tunguz': { name: 'Tomasz Tunguz', fullName: 'Tomasz Tunguz', description: 'Theory Ventures åˆ›å§‹äººï¼Œæ•°æ®é©±åŠ¨çš„ SaaS æŠ•èµ„äººã€‚', website: 'https://tomtunguz.com' },
  'saastr': { name: 'Jason Lemkin', fullName: 'SaaStr (Jason Lemkin)', description: 'SaaStr åˆ›å§‹äººï¼ŒSaaS é¢†åŸŸæœ€å…·å½±å“åŠ›çš„äººç‰©ä¹‹ä¸€ã€‚', website: 'https://www.saastr.com' },
  
  'anthropic': { name: 'Anthropic', fullName: 'Anthropic', description: 'AI å®‰å…¨å…¬å¸ï¼ŒClaude AI çš„åˆ›é€ è€…ã€‚', website: 'https://www.anthropic.com' },
  'deepmind': { name: 'DeepMind', fullName: 'Google DeepMind', description: 'Google æ——ä¸‹ AI ç ”ç©¶å®žéªŒå®¤ï¼ŒAlphaGo çš„åˆ›é€ è€…ã€‚', website: 'https://deepmind.google' },
  'google-ai': { name: 'Google AI', fullName: 'Google AI Blog', description: 'Google AI ç ”ç©¶åšå®¢ã€‚', website: 'https://ai.googleblog.com' },
  'openai': { name: 'OpenAI', fullName: 'OpenAI', description: 'ChatGPT å’Œ GPT-4 çš„åˆ›é€ è€…ã€‚', website: 'https://openai.com' },
  'meta-ai': { name: 'Meta AI', fullName: 'Meta AI', description: 'Meta AI ç ”ç©¶å®žéªŒå®¤ï¼ŒLLaMA æ¨¡åž‹çš„åˆ›é€ è€…ã€‚', website: 'https://ai.meta.com' },
  'microsoft-research': { name: 'Microsoft Research', fullName: 'Microsoft Research', description: 'å¾®è½¯ç ”ç©¶é™¢ï¼Œå…¨çƒé¡¶çº§ä¼ä¸šç ”ç©¶æœºæž„ã€‚', website: 'https://www.microsoft.com/research' },
  'nvidia-ai': { name: 'NVIDIA AI', fullName: 'NVIDIA AI Blog', description: 'NVIDIA AI æŠ€æœ¯åšå®¢ã€‚', website: 'https://blogs.nvidia.com' },
  'huggingface': { name: 'Hugging Face', fullName: 'Hugging Face', description: 'å¼€æº AI ç¤¾åŒºé¢†å¯¼è€…ï¼ŒTransformers åº“çš„åˆ›é€ è€…ã€‚', website: 'https://huggingface.co' },
  'bair': { name: 'BAIR', fullName: 'Berkeley AI Research', description: 'ä¼¯å…‹åˆ©å¤§å­¦ AI ç ”ç©¶å®žéªŒå®¤ã€‚', website: 'https://bair.berkeley.edu' },
  'berkeley-ai': { name: 'BAIR', fullName: 'Berkeley AI Research', description: 'ä¼¯å…‹åˆ©å¤§å­¦ AI ç ”ç©¶å®žéªŒå®¤ã€‚', website: 'https://bair.berkeley.edu' },
  'stanford-hai': { name: 'Stanford HAI', fullName: 'Stanford Human-Centered AI', description: 'æ–¯å¦ç¦å¤§å­¦äººæœ¬ AI ç ”ç©¶é™¢ã€‚', website: 'https://hai.stanford.edu' },
  'langchain': { name: 'LangChain', fullName: 'LangChain Blog', description: 'LLM åº”ç”¨å¼€å‘æ¡†æž¶ã€‚', website: 'https://blog.langchain.dev' },
  
  'stripe-blog': { name: 'Stripe', fullName: 'Stripe Blog', description: 'å…¨çƒé¢†å…ˆçš„æ”¯ä»˜å¹³å°ã€‚', website: 'https://stripe.com' },
  'cloudflare-blog': { name: 'Cloudflare', fullName: 'Cloudflare Blog', description: 'å…¨çƒé¢†å…ˆçš„ç½‘ç»œå®‰å…¨å’Œæ€§èƒ½å…¬å¸ã€‚', website: 'https://www.cloudflare.com' },
  'vercel-blog': { name: 'Vercel', fullName: 'Vercel Blog', description: 'Next.js èƒŒåŽçš„å…¬å¸ï¼Œå‰ç«¯äº‘å¹³å°ã€‚', website: 'https://vercel.com' },
  'spotify-engineering': { name: 'Spotify', fullName: 'Spotify Engineering', description: 'Spotify å·¥ç¨‹æŠ€æœ¯åšå®¢ã€‚', website: 'https://engineering.atspotify.com' },
  'netflix-tech': { name: 'Netflix', fullName: 'Netflix Tech Blog', description: 'Netflix æŠ€æœ¯åšå®¢ã€‚', website: 'https://netflixtechblog.com' },
  'airbnb-engineering': { name: 'Airbnb', fullName: 'Airbnb Engineering', description: 'Airbnb å·¥ç¨‹åšå®¢ã€‚', website: 'https://medium.com/airbnb-engineering' },
  'discord-engineering': { name: 'Discord', fullName: 'Discord Blog', description: 'Discord å®˜æ–¹åšå®¢ã€‚', website: 'https://discord.com/blog' },
  'databricks-blog': { name: 'Databricks', fullName: 'Databricks Blog', description: 'å¤§æ•°æ®ä¸Ž AI å¹³å°ã€‚', website: 'https://www.databricks.com/blog' },
  'replicate': { name: 'Replicate', fullName: 'Replicate Blog', description: 'AI æ¨¡åž‹éƒ¨ç½²å¹³å°ã€‚', website: 'https://replicate.com/blog' },
}

// ä»Žæ–‡ç« çš„ source å­—æ®µåå‘æ˜ å°„åˆ° slug
const sourceNameToSlug: Record<string, string> = {
  'Y Combinator': 'ycombinator',
  'Sequoia Capital': 'sequoia',
  '红杉资本 (Sequoia)': 'sequoia',
  'Andreessen Horowitz': 'a16z',
  'Andreessen Horowitz (a16z)': 'a16z',
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
  'Jason Lemkin (SaaStr)': 'saastr',
  'Anthropic': 'anthropic',
  'Google DeepMind': 'deepmind',
  'Google AI': 'google-ai',
  'Google AI Blog': 'google-ai',
  'OpenAI': 'openai',
  'Meta AI': 'meta-ai',
  'Microsoft Research': 'microsoft-research',
  'NVIDIA AI': 'nvidia-ai',
  'NVIDIA AI Blog': 'nvidia-ai',
  'Hugging Face': 'huggingface',
  'Hugging Face Blog': 'huggingface',
  'Berkeley AI Research': 'bair',
  'Berkeley AI Research (BAIR)': 'bair',
  'Stanford HAI': 'stanford-hai',
  'LangChain': 'langchain',
  'LangChain Blog': 'langchain',
  'Stripe': 'stripe-blog',
  'Stripe Blog': 'stripe-blog',
  'Cloudflare': 'cloudflare-blog',
  'Cloudflare Blog': 'cloudflare-blog',
  'Vercel': 'vercel-blog',
  'Vercel Blog': 'vercel-blog',
  'Spotify Engineering': 'spotify-engineering',
  'Netflix Tech Blog': 'netflix-tech',
  'Airbnb Engineering': 'airbnb-engineering',
  'Discord': 'discord-engineering',
  'Discord Engineering': 'discord-engineering',
  'Databricks': 'databricks-blog',
  'Databricks Blog': 'databricks-blog',
  'Replicate': 'replicate',
  'Replicate Blog': 'replicate',
}

// åå‘æ˜ å°„ï¼šslug -> source names
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
  
  // ç­›é€‰å±žäºŽè¿™ä¸ªæºçš„æ–‡ç« 
  const posts = allPosts.filter(post => 
    sourceNames.some(name => post.source.includes(name) || post.source === name)
  )
  
  return <SourceDetailClient meta={meta} slug={slug} posts={posts} />
}
