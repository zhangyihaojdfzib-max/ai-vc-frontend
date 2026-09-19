---
title: Reproducing, disclosing, and fixing the libheif vulnerability with Hacktron
  and the maintainers
title_original: Reproducing, disclosing, and fixing the libheif vulnerability with
  Hacktron and the maintainers
date: '2026-09-18'
source: Vercel Blog
source_url: https://vercel.com/blog/reproducing-disclosing-and-fixing-the-libheif-vulnerability-with-hacktron-and-the-maintainers
author: ''
summary: '[翻译失败，原文如下]


  In August 2026,Hacktronreported what looked like a remote code execution (RCE) vulnerability
  in Next.js image optimization. Their investi...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-19T06:55:39.049482'
---

[翻译失败，原文如下]

In August 2026,Hacktronreported what looked like a remote code execution (RCE) vulnerability in Next.js image optimization. Their investigation found that the vulnerable code was not in Next.js itself, but upstream inlibheif, an AVIF image decoder used by Next.js,ImageMagick,WordPress,sharp, and much of the web.

Shortly after Hacktron notified us, we worked with them to reproduce the RCE against a current Next.js build and disclose it to the maintainers of  sharp, libvips, and libheif. We then deployed a platform-wide mitigation on Vercel and started working with the maintainers on a fix.

## Copy link to headingThe dependency chain

Next.js image optimization lets applications resize and optimize images through the<Image>component (next/image). For AVIF images, the image-processing dependency chain is as follows:

- <Image>invokes/_next/image,
- /_next/imagecalls sharp
- sharp calls libvips
- libvips uses libheif to decode the image

<Image>invokes/_next/image,

/_next/imagecalls sharp

sharp calls libvips

libvips uses libheif to decode the image

![The full dependency chain of the libheif vulnerability in Next.js.](/images/posts/6c91c4ff3950.jpg)

![The full dependency chain of the libheif vulnerability in Next.js.](/images/posts/cb1aaa3bc6e6.jpg)

![The full dependency chain of the libheif vulnerability in Next.js.](/images/posts/838ecc604244.jpg)

![The full dependency chain of the libheif vulnerability in Next.js.](/images/posts/0013d2f059ea.jpg)

That meant the vulnerable code was not in Next.js, but it was still reachable through Next.js image optimization. A malicious AVIF image sent to the image optimization endpoint would invoke libheif through sharp and libvips.

As such, one obvious mitigation was to disable AVIF optimization in Next.js. Malicious AVIF images would then stop at the image optimization endpoint instead of being passed through sharp and libvips to libheif. The exploit would not propagate upstream.

However, only mitigating Next.js, without an upstream fix, posed a disclosure problem.

## Copy link to headingDisclosing the vulnerability and coordinating the upstream fix

After we worked with Hacktron to successfully reproduce the issue, we rolled out a platform-wide mitigation on Vercel and reached out to the maintainers of sharp, libvips, and libheif to disclose the vulnerability and begin working on a fix.

Here is the timeline:

- August 11-12:Hacktron reported the issue to Vercel; Hacktron and Vercel reproduced the RCE with a working proof of concept.
- August 13:Vercel applied a platform mitigation through its Image Optimization Service.
- August 19:The Next.js team met with the libvips maintainer and began coordination across sharp, libvips, and libheif.
- August 24:Next.js informed its security partners.
- August 25:Next.js published a security release that disabled AVIF optimization.

August 11-12:Hacktron reported the issue to Vercel; Hacktron and Vercel reproduced the RCE with a working proof of concept.

August 13:Vercel applied a platform mitigation through its Image Optimization Service.

August 19:The Next.js team met with the libvips maintainer and began coordination across sharp, libvips, and libheif.

August 24:Next.js informed its security partners.

August 25:Next.js published a security release that disabled AVIF optimization.

The Vercel security team contacted the maintainers of sharp and libvips by email, and opened coordination with libheif through a GitHub Security Advisory. Hacktron had also submitted vulnerability and exploit details to libheif. On August 19, the Next.js team met with the libvips maintainer and aligned on the path forward across sharp, libvips, and libheif. The libheif maintainer continued remediation through Hacktron’s GitHub Security Advisory.

On August 24, Next.js informed its security partners of the libheif vulnerability and its impact on Next.js (partner notifications are a routine part of Next.js’ security release process).

On August 25, sixdays after the August 19 meeting, the libheif maintainer releasedv1.23.2, which remediated the RCE.

## Copy link to headingVercel and Next.js mitigations

Securing Vercel and its customers was straightforward: all Next.js image optimization requests on Vercel go through a central Image Optimization Service. Therefore,we disabled AVIF optimization and resizing in that central service. Any incoming AVIF images were not passed to libheif for decoding and RCE was not possible on Vercel.

Protecting self-hosted applications required a Next.js release. On August 25,Next.js published a security releasethat had originally been planned to address a separate issue. Aftercoordinating an upstream fix, we bundled the AVIF mitigation into that release and shipped it a day earlier than planned. The release disabled AVIF optimization and resizing in Next.js; given that the patched libheif release was still propagating downstream, this was the most timely option. We also published a security advisory to communicate the issue’s severity.

## Copy link to headingOur commitment to making the web more secure

The volume of OSS vulnerabilities discovered continues to increase, and the numbers are overwhelming:

- In 2026,the CVE program has published more than 35,000 CVEs.
- Private vulnerability reports on GitHubgrew from 500 per week in January to 3,000 per week in May.
- GitHub also reported1,560 reviewed advisories in May 2026, the highest monthly volume in the advisory database’s history.

In 2026,the CVE program has published more than 35,000 CVEs.

Private vulnerability reports on GitHubgrew from 500 per week in January to 3,000 per week in May.

GitHub also reported1,560 reviewed advisories in May 2026, the highest monthly volume in the advisory database’s history.

As LLMs accelerate vulnerability research, we expect to see more upstream vulnerabilities like the libheif RCE surface across the OSS ecosystem. There have been a higher number of Next.js security releases in recent months, and we expect that trend to continue as we mitigate new vulnerabilities that both we and the research community uncover.

We are committed to proactively finding vulnerabilities before attackers, responsibly disclosing everything we find, and collaborating with researchers and maintainers on fixes.

## Copy link to headingCredit

Thanks to Hacktron for responsibly disclosing the AVIF vulnerability, working with us to reproduce the issue, and coordinating with the upstream maintainers through remediation.

We also want to thank the maintainers of sharp, libvips, and libheif. Their work on the upstream fix made coordinated remediation possible across the image processing dependency chain.

We work with a talented set of researchers to secure Next.js and other open source frameworks throughVercel's Open Source Bug Bounty. Anyone interested in contributing to the security of eligible frameworks is encouraged to participate there.

## Copy link to headingReferences

- Next.js August 2026 security release
- Upstream libheif advisory
- Vercel security release changelog
- Just a rumor of a bug is enough to find a security exploit

Next.js August 2026 security release

Upstream libheif advisory

Vercel security release changelog

Just a rumor of a bug is enough to find a security exploit

---

> 本文由AI自动翻译，原文链接：[Reproducing, disclosing, and fixing the libheif vulnerability with Hacktron and the maintainers](https://vercel.com/blog/reproducing-disclosing-and-fixing-the-libheif-vulnerability-with-hacktron-and-the-maintainers)
> 
> 翻译时间：2026-09-19 06:55
