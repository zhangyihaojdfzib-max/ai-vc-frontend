---
title: The model that didn't exist, so you made it yourself
title_original: The model that didn't exist, so you made it yourself
date: '2026-10-08'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/building-with-ml-intern
author: ''
summary: '[翻译失败，原文如下]


  # The model that didn''t exist, so you made it yourself


  Last week, I wanted a small version of theprompt rewriterthat ships with Qwen-Ima...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-10T08:17:37.012454'
---

[翻译失败，原文如下]

# The model that didn't exist, so you made it yourself

Last week, I wanted a small version of theprompt rewriterthat ships with Qwen-Image 2.1. The official one is a 9B model that needs about 20 GB of memory and thinks for thousands of tokens before writing a single paragraph. On the Hub, I found only compressed copies of that same 9B model. So I described what I wanted toML Intern, and the next day I had a0.8B versionthat runs on a CPU. It returns valid output 99.7% of the time and uses about a quarter of the teacher's tokens. The compute for the whole project, including having the 9B model label 8,797 example requests, came to USD 16.

Over the course of the next few days, I made five more models the same way. Each one started as a message in HuggingChat with ML-intern switched on, and each one ended as a public model on the Hub with its evaluation in the model card. ML-intern plans the work, asks me for a budget before it spends anything, runs a small test before the real job, then trains, evaluates and publishes on Hugging Face hardware.

## How I prompt ML Intern

The first message is where I spend my effort. My first prompt, for thecitrusmodel shared below, was about 450 words. By my 6th project it was closer to 2,000, because each project taught me something I wanted in the next one. All seven prompts are on GitHub atyvrjsharma/ml-intern-prompts, exactly as I wrote them.

A prompt starts with the idea in one line and why I want it. Then it names the exact pieces: the dataset, the base model, the training script. Anything I have already checked goes under a heading that literally says "Verified facts, do not re-derive", so the agent spends its budget on the work instead of rediscovering what I know. For the camera-angle LoRA that section listed which trainer had just added transparent-image support, and which open GitHub issues made the fallback trainer risky.

Two lines in the prompt are critical. Thefirstasks for a baseline before any training. For example, thecitrus promptsays: "Also report the base model's zero-shot score on the same metric before training so we can see the gain." Without it you get a trained model and no idea whether it is better than what you started with. Thesecondis a smoke test with a check attached. For the image LoRAs I asked for 50 training steps, then a check that the saved weights had actually changed, before paying for the full run.

At the end of the prompt, I lay out the expected deliverables and limit the cost. I define what belongs in the model card and include a instruction like: "Cap total spend at USD 12 and ask me before exceeding it." Because ML-intern begins every task with zero dollar budget and needs permission before executing paid jobs, this spending limit stays strictly enforced. When you leave out a budget, the agent suggests a couple of paths depending on project size and asks which one you prefer.

You don't necessarily need all of that on your first attempt. For example, I didn't have theverified-factssection in mycitrusbrief and ML Intern still produced a model that more thantripled the accuracyof theQwen3.5-2Bmodel. Let me walk you through 6 things I built with Ml-Intern in just a couple of days.

## 1. A model that knows your field

A general vision model can describe a yellowing citrus leaf. However, telling you whether it is a mite problem or a magnesium deficiency, and the bio and non-bio remedies to treat the plant is very hard. Using Claude, I put together a training dataset merged from three sources hosted by theProject-AgMLorganization on the Hub. The resultingcitrus-disease-vlm-instructis a dataset containing 3,017 annotated images across 21 distinct pests, illnesses, nutritional gaps, and treatment approaches. ML-intern handled the fine-tuning of Qwen3.5-2B using these examples, making sure to benchmark the foundation model beforehand.

On the 335 test photos, the base model named the right problem 14.9% of the time. After two epochs on one A10G, the fine-tuned model got 52.8%. Compute cost, about USD 1.90.

Check out:Model·Dataset·Citrus Doctor App

## 2. A model that draws your character

Image models know plenty of characters. Huggy, drawn in the flat style of the Hugging Face brand assets, was not one of them. I asked ML-Intern for a LoRA onFLUX.2 klein base 4B, trained on 84 captioned drawings fromChunte/huggy_for_trainingdataset.

The agent saved a checkpoint every 100 steps and drew the same set of prompts with each one, which made choosing easy. Step 200 was the first where Huggy was fullyon-model. From step 500 on, Huggy's style started bleeding into prompts that had nothing to do with Huggy! The trained LoRA also works on the distilled klein model at 4 steps. Compute cost, about USD 7.60.

Check out:Model·Dataset·Huggy Generator App

## 3. A model that does a new trick

1. Camera-angle LoRAsare among the most-liked community add-ons for earlier Qwen-Image models. You can give the model a picture of an object and ask to see it 45 degrees from the left. When I checked a few days after the Qwen-Image 2.1 model release, nobody had made one, so I tasked ML-intern to build it.

![Qwen camera angle LoRA](/images/posts/43e2e82dd7d1.gif)

ML-intern rendered 1,030 scanned household objects fromGoogle Scanned Objectsat 24 angles each, 24,722 transparent images, on a CPU job that cost a few cents. It later finalised 461 objects for training and 40 held out for testing, and 1,844 before-and-after training pairs spread evenly over 23 camera instructions.

Training ran 2,000 steps in about 90 minutes on one A100 (~USD 3.75). The whole project took about half a day and 48 jobs, counting the ones that failed on missing packages or wrong paths and had to be resubmitted by ML-Intern. Total compute cost, about USD 16.

Check out:Model·Dataset·Viewpoint Orbit App

1. Doodle-in LoRAis another cool idea. Upload a photo with a magenta scribble on it and add a short prompt naming an object. The LoRA replaces the scribble with that object while keeping the original lighting and composition consistent.

No dataset existed for this, so my prompt described how to make one. Start from a real photo in Open Images, remove one object with the LaMa inpainting model, and draw a scribble where the object used to be. The untouched photo is the target. ML-intern wrote and tested the pair-building scripts in a CPU sandbox, then ran them as GPU jobs, recording the author and license of every source photo along the way. It built 6,042 training pairs and a 160-pair test set, where 40 of the test pairs come from 23 object classes kept out of training entirely.

Before training, it measured the base model on its own and with the Viggle turbo LoRA, and checked that running edits in batches produced identical images, which made the evaluation cheaper. Training ran 2,000 steps in 1 hour 38 minutes on one A100 (~USD 4), and a comparison of the saved checkpoints on 48 test pairs picked step 500.

Paired with theViggle turbo LoRAat 6 steps the LoRA performed really well.67.5%of objects detected where they were drawn, at 4.7 seconds per edit. Objects from the 23 unseen classes landed as reliably as the rest (65.0% versus 64.2%). The project took a little over a day and 59 jobs. Total compute cost, about USD 24.

Check out:Model·Dataset·Doodle-in App

## 4. A model that fits your device

1. ThePocket Rewriterfrom the top of this post is the first one. ML-intern started by generating 8,797 short image requests with a small instruct model through Inference Providers, following a mix set in my prompt: photos, posters, logos, infographics and more, about a third of them asking for exact text in quotes, and many in languages other than English. The 9B teacher then rewrote all of them on one A100 in 2 hours 37 minutes (~USD 6.50). After filtering for quality, 1,840 examples were selected for training dataset.

![Qwen Image 2.1 Pocket Studio](/images/posts/725fd1b9c235.png)

[翻译失败，原文如下]

Training the 0.8B and 2B students took 12 and 18 minutes on an A10G (USD 0.75 for both). The 0.8B also ships as an 812 MB GGUF file for running on a CPU. The project took about 11 hours and 24 jobs. Total compute cost, about USD 16.

Check out:Pocket rewriter 0.8B Student·2B Student·Dataset·Pocket Studio App·Compare the teacher-student in Rewriter Arena

1. Agate-Preview-002-4stepis the second.Logolabs' Agate Preview 002is a 260M-parameter text-to-image model, small enough for a browser, but it needs 50 steps with guidance, which is 100 network passes per image. I asked ML-intern to distill it down to just 4 passes!

It took two runs. The first cached 155,000 training images as latents, baked the guidance into the model, then cut the step count in stages from 16 to 8 to 4, all on A100s. The 4-step student beat the teacher run at the same 4 steps on GenEval and FID, after that ML-intern exported it to ONNX for the browser. This run took about 13 hours and USD 22.

I did a second training run by asking ML-Intern to improve the 4-step student a bit more. It then made 24,000 more image pairs with the teacher at 16 steps and fine-tuned the 4-step student against them for about an hour. GenEval went from 0.509 to 0.536, against the teacher's 0.563 at 50 steps, with just 4 steps (one-fourth the compute). ML-intern re-exported the browser version. The second run took about 8 hours. Total compute cost across both runs, about USD 37.

Check out:Agate 4-step model·Dataset·Run Agate in your browser·Agate 4-step LIVE

## What it cost

These are the GPU and CPU job charges reported for each session.

## Make yours

ML-intern is inHuggingChat. Switch on ML-intern mode and paste a prompt. If you want a starting point,my example promptsare free to copy. Start from a model you wish existed and a dataset you have, or one you can describe. Give it a small budget, ask for a baseline and a smoke test, and read what comes back before you raise the cap.

If you make something with it, share it on X and tag@Gradioand@HuggingFace. We would love to see the models you make that nobody else would think to build for you.

---

> 本文由AI自动翻译，原文链接：[The model that didn't exist, so you made it yourself](https://huggingface.co/blog/building-with-ml-intern)
> 
> 翻译时间：2026-10-10 08:17
