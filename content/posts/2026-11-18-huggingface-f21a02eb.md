---
title: 'Rumble-2-Flash: an open 0.5B speech model for 40+ languages'
title_original: 'Rumble-2-Flash: an open 0.5B speech model for 40+ languages'
date: '2026-11-18'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/rumble-2-flash
author: ''
summary: '[翻译失败，原文如下]


  # Rumble-2-Flash: an open 0.5B speech model for 40+ languages


  Today we''re open sourcingRumble-2-Flashunder the Apache 2.0 license. It''s ...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-11-19T09:43:40.709304'
---

[翻译失败，原文如下]

# Rumble-2-Flash: an open 0.5B speech model for 40+ languages

Today we're open sourcingRumble-2-Flashunder the Apache 2.0 license. It's a 0.5B-parameter speech recognition model for 40+ languages that competes with models 3-60x its size.

- Runs anywhere: native support in 🤗 Transformers and vLLM, no custom code
- 40+ languages: automatic language detection
- Output control: numbers as digits or words, fillers, verbatim repeats, forced language
- Extremely fast: an hour of audio in about half a second, with over 7,000 RTFx on full batches
- Holds up on real phone calls: on par with NVIDIA's Nemotron 3.5 Transcribe (30B) on a 302-hour call-centre benchmark

## Quickstart

```bash
uv pip install torch transformers accelerate

```

```python
from transformers import AutoProcessor, AutoModelForMultimodalLM

model_id = "Reson8/Rumble-2-Flash"
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForMultimodalLM.from_pretrained(model_id, device_map="auto")

inputs = processor.apply_transcription_request(
    audio="https://hf.co/datasets/hf-internal-testing/dummy-audio-samples/resolve/main/bcn_weather.mp3",
    language="English",  
).to(model.device, dtype=model.dtype)

output = model.generate(**inputs, max_new_tokens=512)
generated = output[:, inputs["input_ids"].shape[-1]:]
print(processor.decode(generated, return_format="transcription_only")[0])  

```

audioaccepts a local path, a URL, a NumPy array, or a list of these.

## How it's built

Rumble-2-Flash uses the Qwen3-ASR architecture for day-0 support. If your stack runs Transformers or vLLM, it runs Rumble-2-Flash, with no forked runtime ortrust_remote_code.

To find out how small a model could get before accuracy dropped off, we distilled Rumble-2, our larger production model, into it with on-policy distillation. The student doesn't train on transcripts the teacher wrote. It transcribes the audio itself, and the teacher grades that transcript token by token: at every position, it gives its own probability for what should come next, and the student learns to match it. Because the student learns from its own outputs, it gets corrected on exactly the mistakes it makes, with feedback on every token instead of one score per clip.

On-policy distillation normally requires teacher and student to share a tokenizer, and ours don't: choosing Qwen3-ASR meant taking its vocabulary too.GOLDremoves that restriction. It merges tokens where the two tokenizers split the text differently, so both models are compared over the same text. Tokens that exist in both vocabularies are compared directly, and the rest by their sorted probabilities.

![On-policy distillation with GOLD](/images/posts/680b2e13cc21.png)

![On-policy distillation with GOLD: the student transcribes, the teacher scores every token, and GOLD aligns the two tokenizers](/images/posts/997e875fda8b.png)

## Results

### Accuracy for its size

On the Open ASR Leaderboardmultilingualtrack, Rumble-2-Flash averages a6.96% error rateacross Chinese, German, French, Italian, Spanish, Portuguese, Hindi, Dutch and English. That's better than Meta's omniASR-LLM 7B, a model 15x larger, and ahead of Whisper large-v3. On theEnglishtrack it averages6.6% WER.

![The best score for its size](/images/posts/62bd4afcec8d.png)

![Average error rate against model size for open-weight models on the Open ASR Leaderboard multilingual track, including English](/images/posts/ac36d4aab79d.png)

### Speed

Rumble-2-Flash is also fast. Its throughput depends on how full the batches are: on the larger datasets in HF's Open ASR Leaderboard, where batches stay full, it reachesover 7,000 RTFx. That's an hour of audio in about half a second.

### Real phone calls

Clean audio is easy. Phone calls are compressed and noisy, and often have speakers with very different accents. OnAppTek's call-centre benchmark(302 hours of helpline calls, 14 English accents, scored with AppTek's own script), Rumble-2-Flash reaches7.86% WER, on par with NVIDIA's Nemotron 3.5 Transcribe (30B) at 7.78%. That's well ahead of Qwen3-ASR 0.6B (8.7%), from the same model family, and close to Qwen3-ASR 1.7B (7.4%), the only model in the comparison that does better.

![Real phone calls, 14 English accents](/images/posts/2dd47e2b7795.png)

![WER on the AppTek call-centre benchmark](/images/posts/8fb037bfeb8e.png)

## Try it

The weights are on the Hub atReson8/Rumble-2-Flash. It's also available through ourAPI.

We're very curious what you'll build with it. Tell us in theDiscussions tabwhat you've made, what you like, and what you'd like to see changed in a next version.

---

> 本文由AI自动翻译，原文链接：[Rumble-2-Flash: an open 0.5B speech model for 40+ languages](https://huggingface.co/blog/rumble-2-flash)
> 
> 翻译时间：2026-11-19 09:43
