---
title: Modernizing the Video Playback Experience at Discord
title_original: Modernizing the Video Playback Experience at Discord
date: '2026-11-02'
source: Discord Engineering
source_url: https://discord.com/blog/modernizing-the-video-playback-experience-at-discord
author: ''
summary: '[翻译失败，原文如下]


  Discord is the best way to chat and game with your friends. Part of that is ensuring
  that it’s a great place to share all types of media ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-03T09:14:50.544682'
---

[翻译失败，原文如下]

Discord is the best way to chat and game with your friends. Part of that is ensuring that it’s a great place to share all types of media as well, such as pictures and video content. And that’s exactly what the Media Infrastructure team focuses on: making media awesome to share and watch on Discord!

Today, we want to talk specifically aboutvideos.With more than 90 million people using Discord every day, sharing videos with friends is a huge part of how people hang out here. Our Media Infrastructure team decided to step back and think deeply about how to make the video-watching experience even better.

We set ourselves three goals:

- Modernize the user experienceby giving it a fresh coat of paint!
- Lay a foundation for great video playback everywhere in Discord.After all, one of our engineering mantras is “Build technology to be reusable.”
- Make it fast and safe to change.We’ve got alotof great ideas planned, and we want any team to be able to improve the player without holding their breath!

This is the story of how we assessed and refactored two video players into one, cutting the player code each product maintained by up to 94%(!!), and ultimately swapping in the first version of the new player without any users noticing.

---

> 本文由AI自动翻译，原文链接：[Modernizing the Video Playback Experience at Discord](https://discord.com/blog/modernizing-the-video-playback-experience-at-discord)
> 
> 翻译时间：2026-11-03 09:14
