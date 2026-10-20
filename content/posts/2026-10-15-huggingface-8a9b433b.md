---
title: Apertus 1.5 Release Notes
title_original: Apertus 1.5 Release Notes
date: '2026-10-15'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/swiss-ai/apertus-v15-release-notes
author: ''
summary: '[翻译失败，原文如下]


  # Apertus 1.5 Release Notes


  Our latest release, Apertus 1.5, extends the 8B and 70B Apertus 1.0 models with
  image/audio understanding, a...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-20T07:22:15.607734'
---

[翻译失败，原文如下]

# Apertus 1.5 Release Notes

Our latest release, Apertus 1.5, extends the 8B and 70B Apertus 1.0 models with image/audio understanding, an optional thinking mode, a four times longer context window, improved instruction-following, and better tool use. The updated8B and 70B model weightswere released to Hugging Face on July 24, 2026 under an Apache 2.0 license. Further details are now available from the projectTechnical Report, and summarized here.

Apertus 1.5 is a continued pretraining of the first generation model: adding 4 trillion tokens of text and multimodal training data to the 8B model and 2 trillion tokens to the 70B model, for a total of 19T and 17T, respectively.  As with every Apertus release, the models are fully open: openweights, opendata, openvalues, and full trainingdetails.

## Key Enhancements

- Native Multimodal Understanding:Apertus 1.5 accepts images and audio alongside text, bringing documents, diagrams, and photos into the conversation. The models can also process spoken language, though this remains experimental.
- Thinking Mode:The models can be switched into a thinking mode to reason about the input before answering, which improves performance on reasoning problems.
- Long Context:The context window grows to 262,144 tokens, a 4x increase over Apertus 1.0.
- Improved Instruction-Following:Better instruction adherence than Apertus 1.0 gives more predictable and accurate responses.
- Improved Tool Use:The models are trained for better tool integration, allowing more effective use of external tools and APIs.
- Open Values:Stronger adherence to the Apertus Charter, which brings transparency to the model’s values and principles.

## Training Process

The full Apertus 1.5 training pipeline

![Apertus 1.5 training pipeline with four stages of continued pretraining followed by SFT, long-context SFT, RLVR, DPO, and SDPO](/images/posts/b4ea70335e7f.png)

### Multimodality Through the Tokenizer

We introduce multimodality in v1.5 models in an early-fusion manner, where images and audio enter Apertus as discrete tokens in the same sequence with text tokens, instead of using a separate vision encoder. Images are tokenized with theEmu3.5tokenizer (a 512×512 image becomes 1,024 tokens) and audio withWavTokenizer(40 tokens per second). We only extend the vocabulary, so the architecture stays unchanged and training runs at text-only speed. The models understand images and audio but generate only text.

![image](/images/posts/f300ecfb6983.png)

### Pre-Training

Starting from Apertus 1.0, we continue pretraining in four stages:

1. Unpaired:text plus standalone images and audio, so the model learns the new modalities.
2. Paired:image–caption and audio–transcript pairs, so it aligns them with language.
3. Cooldown:higher-quality data with more math and code.
4. Long context:the window grows step by step from 8k to 262k tokens.

Overall, more than half of the training tokens are text-only, which preserves the language abilities of Apertus 1.0. The text data is refreshed with sources such asFineWeb2-HQ+, FinePDFs, and Nemotron-CC. All new data, multimodal included, meets the same bar as before: publicly available, permissively licensed, and with robots.txt opt-outs respected retroactively. Every source is listed inapertus-data-transparency.

### Post-Training

Post-training runs in five stages:SFT → long-context SFT → RL → DPO → charter alignment (SDPO).

1. SFTon 3.7M text samples plus image and speech data. Reasoning traces are added only to prompts the model can't already solve without them. Tool-use data is restricted to execution-verified trajectories. We release thetext SFT mixwe used on Hugging Face.
2. Long-context SFTat the full 262k window restores the long-context ability that short-context SFT erodes.
3. RL with verifiable rewards (RLVR)on about 350k math, code, instruction-following, multilingual, and vision prompts, mixing thinking on and off.
4. DPOwith judge-scored preference pairs improves chat quality, tool use, and safety. We release thepreference poolandtraining pairs.
5. SDPOaligns the model with theApertus Charterthrough judge feedback and self-distillation.

## Evaluation Results

Alongside the extended model capabilities, we also significantly expanded the scope of evaluations. Beyond the existing text-based evaluations used for Apertus 1.0, we added multimodal evaluations (image & audio), and thinking-mode evaluations.

The multimodal evaluations are done throughMLLM-eval-suitepipeline, merging two major multimodal evaluation frameworkslmms-evalandVLMEvalKit. We also added a series of text-based benchmarks, as well as extended benchmarking for translation and multilingual capabilities, safety, and tool use. These can be found in our post-trainingevaluation repository, based onlm-evaluation-harness fork.

While still trailing frontier open-weight models, the new release has also significantly improved performance in coding and instruction following capabilities with Apertus 1.5 8B outperforming similarly sized open-weight models on IF and multilingual tasks. Thinking further improves performance on challenging reasoning-heavy benchmarks like AIME. The multimodal performance of the model is closer toGemma 4 12Band other current open-weight models. Apertus 1.5 multimodal performance is competitive in spatial understanding among open-weight models and document/chart understanding among open-source models.

We also thank our collaborators and external evaluators for their help with efficient benchmarking of Apertus capabilities. In particular, Apertus 1.5 shows strong performance on Swiss Legal tasks, being on par with leading open-weight models (blog,code). Additionally, on Last Translation Benchmark, Apertus 1.5 8B presents machine translation capabilities which matchGPT-OSS-20Band outperform models likeClaude Haiku 4.5orGoogle Translate(leaderboard,paper).

### Evaluation Cards: Apertus ❤️ EvalEval

Apertus collaborates with theEvalEval Coalitionto ensure fully transparent and reproducible benchmarking. We publish the Apertus 1.5 results in theEvery Eval Ever (EEE)schema, a shared format that records not only scores, but also who ran the evaluation, how the model was accessed, the generation settings, and how each metric should be interpreted: details that are routinely missing from leaderboards and that often explain why similar-looking scores differ.

The results are shown in the Eval Card below, which combines the run data with benchmark and model metadata into one interpretable record, and are also available throughHugging Face Community Evals. This is the same infrastructure theUK AI Security Institute uses to publish its evaluations openly. Since our text evaluations run on our public fork of lm-evaluation-harness, which EEE supports with a dedicated converter, anyone can rerun them and compare their numbers against ours under identical settings.

Structured evaluation reporting also matters beyond research. EvalEval hasmapped Evaluation Cards to AI governance requirements, including Article 55 of the EU AI Act and the GPAI Code of Practice, and found that the EEE schema can represent 56 of the 60 evaluation-reporting elements these frameworks call for. This fits how we already release Apertus: alongside the models, we publish aPublic Summaryof Training Content and, voluntarily, aCode of Practicedocument. Machine-readable evaluation records are a natural next step: making it easier for regulators, deployers, and researchers to find, interpret, and compare the evidence behind a model.

We are committed to promoting reproducible and transparent evaluation through Eval Cards and the EEE schema, and encourage other model developers to report their results in the same way, so that scores can be compared across models and organizations.

## Apertus 1.5 Reproducibility

[翻译失败，原文如下]

All recipes, ablations, and data mixtures are documented in theTechnical Report. We aim to popularize open model development by making the v1.5 training process public and accessible. Intermediate checkpoints are hosted in ourApertus 1.5 Hugging Face collection, including the base weights, SFT, RLVR and DPO, as well as our curated training data mixes/custom datasets inApertus 1.5 datasets collection. Sharing them allows researchers to investigate how each stage changes the model behavior.

The report covers numerous ablations on the effect of post-training data in different stages, where we observed that the multimodal data mixed in together with text data during SFT helps improve across all modalities. We also find that the benefits of multimodal reasoning traces survive the subsequent text-only reinforcement learning: starting from an SFT checkpoint trained with multimodal traces, RL improves mathematics more than when starting from a text-only checkpoint, and the advantage on reasoning tasks persists throughout training.

## Model Availability

Proton LumoandInfomaniak Euriaare two widely used apps that have recently integrated Apertus 1.5. These deployments are linked in theCommunity Showcaseamong others - see thisdiscussion threadfor a preview.

Access to Apertus 1.5 in the form of an API for developers has been announced by a range of providers, includingSwisscom,Infomaniak,Phoeniqs, and other companies listed in ourGeneral Availability guide. The report also provides details on how we work with external evaluators to test and prepare the models.

Technical instructions for running the models are in the model cards of the Apertus releases on Hugging Face and in ourQuickstart guide.

## How to Get Involved

Thank you for reading this blog post and being part of our community! We just celebrated five million downloads in our Hugging Face analytics 🤗 and are not slowing down. At the recentAI+X Summitin Zurich, our team announced the roadmap forApertus 2.0: sparse/MoE architecture, ~600B total parameters, extended training schedule, with agents, mathematics and coding as priorities.

In summary: we invite you to read our report, download the models, explore the intermediate checkpoints, finetune the weights, and reproduce our evaluations. Questions that are not already covered inour publicationsorwebsite FAQare always welcome, and we would also love to hear which topics would be most useful to the community for future deep dives.

If you build with or use Apertus, please fill out theShowcase form, and reach out through the options on ourContact page. We are looking forward to highlighting more work, learning what you are building, and hearing how Apertus can be improved!

## Citation

Project Apertus, et al. “Apertus 1.5: From Open Text Models to Open Multimodal Reasoners.” arXiv:2610.15542. Preprint, arXiv, October 11, 2026.https://doi.org/10.48550/arXiv.2610.15542.

```bibtex
@misc{apertus2026apertus15opentext,
      title={Apertus 1.5: From Open Text Models to Open Multimodal Reasoners}, 
      author={Project Apertus and Yixuan Xu and Yassine Turki and Vinko Sabolčec and Valentina Pyatkin and Tommy Chu and Sven Najem-Meyer and Sean F. Carroll and Robert Smith and Raphael Kreft and Oscar Alessandro Tazza and Oleg Lavrovsky and Nicola Irmiger and Matteo Santelmo and Marian Schneider and Juan García Giraldo and Hanna Yukhymenko and Eduard Ďurech and Davit Melikidze and Dani Tamayo and Bettina Messmer and Aryan Ahadinia and Anunay Yadav and Allen Huang and Ahmad Fraij and Alessandro Bombarda and Alex Padula and Alexander Hägele and Alexander Sternfeld and Anna Hedström and Anna Kosovskaia and Arthur Wuhrmann and Arundhati Balasubramaniam and Badr Al Mahouri and Barna Pasztor and Bartosz Szostakiewicz and Bich Ngoc Doan and Bryan Schmid and Burak Sezen and Camille Challier and Clément Charmillot and Dana Shayakhmetova and Daniel Perruchoud and David Brüggemann and David Isztl and Elia Palme and Emma Anastassova and Fabian Bösch and Faruk Zahiragić and Fawzi Roberto Mohamed and Fiona Panicali and Florian Kolly and Flynn Guerra and Francesco Monti and Frederike Lübeck and Gennaro Oliva and Haofeng Yang and Haoliang Shang and Helen El Khoury and Henrique Mendonça and Jannis Vamvas and Jérome Landolt and Jessica Lam and Jingchun Xiao and Jonathan Coles and Joshua Oyebanji and Khanh Nguyen and Konstantinos Pitas and Lasse B. Strand and Li Mi and Loïc Deslarzes and Lorenzo Baggi and Lorenzo Noci and Luca Baumann and Luca Sartori and Lukas Drescher and Marco De Negri and Marco Passerini and Mark Klein and Marko Stojanovic and Martin Majsec and Matin Ansaripour and Mattea Busato and Mauro Pellonara and Max Neuwinger and Michael Graber and Michal Tešnar and Michelle Wastl and Miguel Gila and Mikolaj Boronski and Morgane Magnin and Moritz Reihs and Mukhammadali Sayfiddinov and Nathan Ranchin and Nicolas Cuveillier and Oscar Wohlfahrt and Qianqian Zou and Rada Kamysheva and Rita Sevastjanova and Roman Machacek and Sebastian Keller and Simon Matrenok and Simon Pierre and Stefano Schuppli and Suei-Wen Chen and Szabina Horváth-Mikulas and Taliesin Perez and Thilo Spinner and Thomas Kleine Buening and Tim Robinson and Tymoteusz Kwiecinski and Vilém Zouhar and Vinzenz Thoma and Xiaozhe Yao and Yannick Metz and Yuhei Fukuhara and Yusif Askari and Zixuan Chen and Alexander Ilic and Ana Klimovic and Andreas Krause and Andrei Kucharavy and Elliott Ash and Joost VandeVondele and Martin Rajman and Mennatallah El-Assady and Thomas Schulthess and Timo Kehrer and Torsten Hoefler and Antoine Bosselut and Martin Jaggi and Imanol Schlag},
      year={2026},
      eprint={2610.15542},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2610.15542}, 
}

```

---

> 本文由AI自动翻译，原文链接：[Apertus 1.5 Release Notes](https://huggingface.co/blog/swiss-ai/apertus-v15-release-notes)
> 
> 翻译时间：2026-10-20 07:22
