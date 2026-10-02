---
title: 'Open TTS Leaderboard: Scalable Evaluation for Multilingual Text-to-Speech
  and Voice Cloning'
title_original: 'Open TTS Leaderboard: Scalable Evaluation for Multilingual Text-to-Speech
  and Voice Cloning'
date: '2026-09-30'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/open-tts-leaderboard
author: ''
summary: '[翻译失败，原文如下]


  # Open TTS Leaderboard: Scalable Evaluation for Multilingual Text-to-Speech and
  Voice Cloning


  ### TLDR 👉 newTTS leaderboardfocused on op...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-02T08:10:31.834234'
---

[翻译失败，原文如下]

# Open TTS Leaderboard: Scalable Evaluation for Multilingual Text-to-Speech and Voice Cloning

### TLDR 👉 newTTS leaderboardfocused on open-source and multilingual

The pace of open-source text-to-speech (TTS) model releases has been incredible. On the Hugging Face Hub (as of Sep 30, 2026) there are more than8K TTS modelsavailable 🚀

Evaluation, however, hasn't kept pace: it remains fragmented and unstandardized.The gold standard is human preference scores such as MOS or MUSHRA (more onmetrics). To this end, several arena-based leaderboards have established themselves as useful reference points for the community:

1. TTS Arena v2
2. Artificial Analysis
3. Voice Arena

These arenas compare models by presenting users with TTS outputs from two models, and asking them to choose one over the other. After collecting a sufficient number of votes, anElo scoreis computed to rank models, typically with the Bradley–Terry model (seeVoice Arena methodology).

While human preference is the ultimate decider,arenas cannot scale to keep up with the pace of TTS releases. This may partly explain why open-source models are underrepresented on arena-style leaderboards: as of Sep 30, 2026, only 16 of the 92 models onArtificial Analysisare open-weights, with a similar skew onVoice Arena. This likely reflects practical factors: adding an API model requires little more than an API key, whereas an open model must be hosted and served by the arena operator, and commercial providers have more reason to seek placement than open-source authors. Another limitation with arena-style evaluation is voter consistency: no arena can ensure that the same voters with the same criteria of “better” can consistently evaluate models over time. Even the preferences of a single person change over time (“A man cannot step into the same river twice” as famously said by Heraclitus).

To this end, we've built theOpen TTS Leaderboard, which uses objective metrics to evaluate models on complementary aspects of performance:

1. Intelligibility: word/character error rate (WER and CER) between the prompt and the generated audio's transcript, usingQwen3 ASR(top ranking open-source model on theOpen ASR Leaderboard).
2. Speed: inverse real-time factor (RTFx) for batched offline inference on an H200 GPU, and time-to-first-audio (TTFA) for quantifying streaming batch size 1 latency on an H200 GPU and CPU.
3. Speaker similarityby computing the cosine similarity (SIM) betweenWavLM speaker embeddingsof the generated audio and the reference clip.

By relying on objective metricsevaluating a model drops from a couple weeks (for collecting votes) to a couple hours⚡

Importantly, the Open TTS Leaderboard does not replace human preference ranking. ASR-based WER provides a proxy for intelligibility, while speaker similarity estimates voice identity preservation. Neither directly measures naturalness, expressiveness, or listener preference. Nevertheless, they can even inform voting-based leaderboards which models to include in their evaluations.

Our intention with this leaderboard is for it to beshaped by the community; we want to hear your feedback so the evaluations stay relevant and insightful. The next few sections give an overview of main features of the Open TTS Leaderboard.

## Multilingual + voice cloning evaluation

From the default view of the leaderboard, models are ranked by macro-average WER on the English splits ofSeed TTS Eval(paper) andCV3 Eval(zero shot) (paper).

hexgrad/Kokoro-82M,Supertone/supertonic-3, andfishaudio/s2-prolead the pack on English WER when averaged on these two splits, while the Pareto plots visualize which models strike a good balance between WER, batched inference (RTFx), and size.

English performance doesn't necessarily translate to other languages. Multiple languages can be toggled to rank models on multilingual performance. Seed TTS Eval only has audio for English and Chinese, so the other languages are simply the score on CV3 Eval (zero shot). Note that Chinese, Japanese, and Korean are character-based languages and so character error rate (CER) is reported, and the “Average WER” across languages is a macro-average across languages.

k2-fsa/OmniVoice,fishaudio/s2-pro, andFunAudioLLM/Fun-CosyVoice3-0.5B-2512are strong multilingual models.

By toggling “Voice cloning”, the models that support this functionality (on the selected languages) can be compared.

Moreover, a SIM column for speaker similarity now appears in the table, as well as two more Pareto plots for visualizing the tradeoff between SIM, batched inference, and size.

The average WER of some models, such asbosonai/higgs-tts-3-4bandopenbmb/VoxCPM2, improve under voice cloning, namely when a reference audio is provided.

## Compare and vote on TTS outputs

Numbers only tell part of the story, and as mentioned earlierhuman preference is the ultimate decider. From the “Listen” tab, you can compare the generated outputs that are behind the metrics, to find which model(s) you prefer!

Pick thelanguage/datasetyou're interested in, whether you want to comparevoice cloning, and optionally pick the models or listen to outputs from a random selection.

The “Listen” tab fills an important gap in existing TTS leaderboards: a space to explore model outputs of various models.

You can even give feedback on the generated outputs. As we collect more votes from the community, we may include this data on the leaderboard.So vote! But please login with your HF account to help us weed out spam/bots.

## Streaming performance

The “Streaming” tab compares the streaming capabilities. Models are ranked by TTFA (time-to-first-audio), which quantifies how long a user waits after probing a model in order to obtain audio that can be played. This is important for voice agents and other interactive apps.

For streaming models (✅ under “Streaming API”) it's the time until the first audio chunk arrives. For non-streaming models, it's the time until the whole utterance is generated, because playback can't start any earlier. Every model runs one audio at a time (batch size 1), on the same 50 English prompts from CV3-Eval, on the same hardware and in its default voice. We drop the first 3 runs as warm-up and report the median TTFA across the rest.

The default view compares performance on an H200 GPU. Results are also available for CPU for a small (but growing) set of models!

kyutai/pocket-ttsis a great model for streaming on both GPU and CPU!

## Conclusion

The goal of the Open TTS Leaderboard is not only to keep up with the incredible pace of TTS model releases, but to be shaped by the community; we want to hear your feedback so the evaluations stay relevant and insightful. Let us know which datasets, models, and metrics you want to see!

For now, we've focused on:

1. Open-source models, to put forward many great models that have been neglected by arena-style evaluations.
2. Multilingual, since English performance is not a suitable proxy for other languages.

We will soon open-source the evaluation scripts, much like the Open ASR Leaderboardrepo, so that you can directly provide your feedback and suggestions via GitHub Issues and PRs! Let's shape TTS evaluations together 🤗

---

> 本文由AI自动翻译，原文链接：[Open TTS Leaderboard: Scalable Evaluation for Multilingual Text-to-Speech and Voice Cloning](https://huggingface.co/blog/open-tts-leaderboard)
> 
> 翻译时间：2026-10-02 08:10
