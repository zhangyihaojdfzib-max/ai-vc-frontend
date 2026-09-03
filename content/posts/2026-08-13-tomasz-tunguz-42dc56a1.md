---
title: The OpenAI Hack & the Question of Intent
title_original: The OpenAI Hack & the Question of Intent
date: '2026-08-13'
source: Tomasz Tunguz
source_url: https://tomtunguz.com/openai-hack-ai-intent/
author: ''
summary: '[翻译失败，原文如下]


  In short :OpenAI agents escaped a test, shared notes in a secret chat room, & broke
  into Hugging Face. The instinct is to ask what they i...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-09-03T07:02:51.103476'
---

[翻译失败，原文如下]

In short :OpenAI agents escaped a test, shared notes in a secret chat room, & broke into Hugging Face. The instinct is to ask what they intended. Three research ideas answer it: specification gaming, instrumental goals, goal misgeneralization. All three fit the same facts, which is why the label is not the actionable part. Nothing in the setup stopped them in time. The practical work is control & guardrails.

Nobody told them to attack Hugging Face. They were told to pass the exam.

Which raises the question : was the AI benevolent with accidentally bad behavior, seemingly benevolent but actually malevolent, or something else?

On Friday I shared the timeline : agents that escaped their sandbox, found a weakness in a computer system, stole passwords, & broke into a production database.1The engineers directed the agents to solve a set of problems.2The agents achieved it by breaking in.

Research can explain this behavior.

![Line illustration of a robot vacuum that has cleaned its way out through an open doorway, leaving a tangled track, a tipped plant pot & a dragged cord behind it](/images/posts/a0748cf54ba8.jpg)

In specification gaming, the AI achieved the goal specified to the letter of the instruction, but not the meaning.3Tell a cleaning robot to clean the room. It pushes the toppled bowl of chocolate pudding to another room.

Instrumental goals are a fancy way of saying that when AI faces similar workflows, it saves common logins, skills, & techniques to skip steps next time.45The agents gathered passwords & left notes for each other in a chat room.67

Goal misgeneralization offers a third explanation : a system that looked fine in testing chases the wrong thing once circumstances shift.89A self-driving car trained on sunny California highways freezes or swerves on a snowy unmarked road at night.

These explanations help decompose the why, & perhaps assuage the AI-as-terminator reflex, but not the so what.67

Nothing in the setup stopped them in time. Not the sandbox, not the monitoring, not careful engineers at a frontier lab.

So the useful question is control. AI’s zealous pursuit of goals produces outcomes nobody asked for, & the fix is not one clever prompt. It is layers.

Even sophisticated engineers running careful experiments need those limits.10

1. The Secret Chat Room↩︎
2. OpenAI: Hugging Face model evaluation security incident↩︎
3. Victoria Krakovna et al.,Specification gaming: the flip side of AI ingenuity(DeepMind, 2020)↩︎
4. Alex Turner et al.,Optimal Policies Tend to Seek Power(NeurIPS 2021)↩︎
5. Nick Bostrom,The Superintelligent Will(2012); Stephen Omohundro, “The Basic AI Drives” (2008)↩︎
6. The Verge: OpenAI’s rogue AI agent didn’t stop at hacking Hugging Face↩︎↩︎
7. WIRED: OpenAI Didn’t Notice Its AI Agents Using a Message Board to Plan Their Hacking Spree↩︎↩︎
8. Rohin Shah et al.,Goal Misgeneralization: Why Correct Specifications Aren’t Enough For Correct Goals(2022)↩︎
9. Lauro Langosco et al.,Goal Misgeneralization in Deep Reinforcement Learning(ICML 2022)↩︎
10. CNN: An OpenAI test model escaped and broke into a real company’s servers↩︎

The Secret Chat Room↩︎

OpenAI: Hugging Face model evaluation security incident↩︎

Victoria Krakovna et al.,Specification gaming: the flip side of AI ingenuity(DeepMind, 2020)↩︎

Alex Turner et al.,Optimal Policies Tend to Seek Power(NeurIPS 2021)↩︎

Nick Bostrom,The Superintelligent Will(2012); Stephen Omohundro, “The Basic AI Drives” (2008)↩︎

The Verge: OpenAI’s rogue AI agent didn’t stop at hacking Hugging Face↩︎↩︎

WIRED: OpenAI Didn’t Notice Its AI Agents Using a Message Board to Plan Their Hacking Spree↩︎↩︎

Rohin Shah et al.,Goal Misgeneralization: Why Correct Specifications Aren’t Enough For Correct Goals(2022)↩︎

Lauro Langosco et al.,Goal Misgeneralization in Deep Reinforcement Learning(ICML 2022)↩︎

CNN: An OpenAI test model escaped and broke into a real company’s servers↩︎

---

> 本文由AI自动翻译，原文链接：[The OpenAI Hack & the Question of Intent](https://tomtunguz.com/openai-hack-ai-intent/)
> 
> 翻译时间：2026-09-03 07:02
