---
title: Introducing Falcon ASR
title_original: Introducing Falcon ASR
date: '2026-10-07'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/tiiuae/falcon-asr
author: ''
summary: '[翻译失败，原文如下]


  # Introducing Falcon ASR


  ![Falcon ASR: Arabic and English speech recognition](/images/posts/28529ed154b3.png)


  English·العربية


  Arabic W...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-10T08:17:35.860512'
---

[翻译失败，原文如下]

# Introducing Falcon ASR

![Falcon ASR: Arabic and English speech recognition](/images/posts/28529ed154b3.png)

English·العربية

Arabic WER: 20.92% · Parameters: 1.6B · Emirati WER (TII evaluation): 22.73%

We’re introducing Falcon-ASR, our 1.6 billion parameter speech recognition model for Arabic, with a particular focus on the Emirati dialect. Developed at the Technology Innovation Institute (TII) in Abu Dhabi, it also supports English, French, Spanish and Portuguese.

In our evaluation, Falcon-ASR achieved an average word error rate of 20.92% across six Arabic test sets, compared with the best published result of 23.17% in the leaderboard snapshot we used. On our internal Emirati evaluation, it recorded the lowest word and character error rates among the systems we compared.

We also support word-level timestamps for transcriptions, linking each transcribed word to its position in the audio.

Try Falcon ASR →

## Recognising spoken Arabic

Arabic speech varies by region, speaker and setting. A model that handles a formal news broadcast may still struggle with a conversation in Emirati or with speech recorded over a phone line. Dialectal Arabic also has fewer transcribed resources than Modern Standard Arabic (MSA), which makes training and evaluation harder.

We trained Falcon-ASR on Emirati, MSA, other Gulf and Arabic dialects, and English. Our aim is to transcribe the words people use in everyday speech, including dialectal forms and changes between languages.

## Arabic benchmark results

TheOpen Universal Arabic ASR Leaderboard, maintained by the ELM Research Center, ranks systems by the equal-weight average WER across six test sets. It also reports character error rate (CER). Lower values are better for both metrics. Our Falcon-ASR evaluation follows this protocol.

![falcon-asr-arabic](/images/posts/7ed605f6861f.png)

WER = Word Error Rate; CER = Character Error Rate. A lower value indicates better performance.

We evaluated Falcon-ASR on the same six benchmarks using the leaderboard’s pinned manifests. Competitor figures are the published leaderboard averages checked on 30 September 2026. Falcon-ASR’s average WER is 2.25 percentage points better than the best published result in that snapshot.

## Evaluating Emirati speech

Public evaluation data already includes Emirati:Casablancahas a UAE subset. We complement that coverage with an internal evaluation of additional Emirati and Gulf speech, using held-out recordings and human-validated transcripts to assess transcription accuracy beyond the public UAE subset.

In our internal Emirati evaluation, Falcon-ASR achieved 22.73% WER and 10.19% CER:

![falcon-asr-emirati](/images/posts/36575dc71904.png)

Falcon-ASR has the lowest WER and CER among the systems compared here. Its WER is 4.07 percentage points below Qwen3-Omni, the next best result. The results show improved transcription accuracy at both the word and character level on this evaluation.

## Training for different recording conditions

We included background noise, overlapping speech, music, room reverberation and telephony effects, as well as variations in speed and pitch. We applied the same treatment to Emirati recordings, exposing the model to a range of conditions it may encounter in meetings, calls and other everyday recordings.

## English and other languages

Falcon-ASR also transcribes English with the same model weights. In our evaluation on the seven public English test sets used by the Hugging Face Open ASR Leaderboard, it achieved a mean WER of 5.74%.

![falcon-asr-english](/images/posts/9c9f29736ad5.png)

The model also supports French, Spanish and Portuguese. All five languages use the same weights, without requiring a language flag. The output is a transcript in the language spoken.

## Model foundation

Falcon-ASR builds on our Falcon3-Audio work. The architecture and training approach for Falcon3-Audio are described inCompetitive Audio-Language Models with Data-Efficient Single-Stage Training on Public Data.

## Try Falcon ASR

OurHugging Face Demo Spacelets you try Falcon-ASR and explore its transcription capabilities. API access and native applications are planned. We invite you to try the Demo with your own recordings.

## Acknowledgments

We thank the team behind the Falcon-Emirati model for their support with Arabic foundation models. Read about their latest work in theFalcon-Emirati blog post.

We also extend our sincere thanks to Mikhail Lubinets for continued support with the compute infrastructure.

# نقدّمFalcon ASR

نقدّمFalcon-ASR، نموذجنا للتعرف على الكلام العربي بحجم1.6مليار معلمة، مع اهتمام خاص باللهجة الإماراتية. طوّرنا النموذج في معهد الابتكار التكنولوجي (TII) في أبوظبي، وهو يدعم أيضًا اللغات الإنجليزية والفرنسية والإسبانية والبرتغالية.

في تقييمنا، حققFalcon-ASRمتوسط معدل خطأ في الكلمات بلغ20.92%عبر ست مجموعات اختبار باللغة العربية، مقارنةً بأفضل نتيجة منشورة بلغت23.17%في نسخة لوحة المتصدرين التي استخدمناها. وفي تقييمنا الداخلي للهجة الإماراتية، سجّل النموذج أدنى معدلات خطأ في الكلمات والأحرف بين الأنظمة التي قارناها.

ندعم أيضاً الطوابع الزمنية على مستوى الكلمات في عمليات التفريغ النصي، بحيث ترتبط كل كلمة بموضعها في التسجيل الصوتي.

جرّبواFalcon ASR←

## التعرف على العربية المنطوقة

يختلف الكلام العربي باختلاف المنطقة والمتحدث وظروف التسجيل. فقد ينجح نموذج في تفريغ نشرة إخبارية رسمية، ثم يجد صعوبة في تفريغ محادثة باللهجة الإماراتية أو تسجيل عبر الهاتف. كما أن الموارد الصوتية المفرّغة نصيًا للهجات العربية أقل من تلك المتاحة للعربية الفصحى، مما يزيد صعوبة التدريب والتقييم.

درّبناFalcon-ASRعلى اللهجة الإماراتية والعربية الفصحى ولهجات خليجية وعربية أخرى، إلى جانب الإنجليزية. وهدفنا هو تفريغ الكلمات التي يستخدمها الناس في حديثهم اليومي، بما في ذلك الصيغ اللهجية والانتقال بين اللغات.

## نتائج الاختبارات العربية

ترتّبلوحة المتصدرين المفتوحة الشاملة للتعرف على الكلام العربي، التي يديرها مركزELMللأبحاث، الأنظمة وفق متوسط معدل خطأ الكلمات عبر ست مجموعات اختبار، بوزن متساوٍ لكل مجموعة. وتعرض أيضًا معدل خطأ الأحرف (CER). وكلما انخفضت قيمة أي من المقياسين، كان الأداء أفضل. ويتبع تقييمنا للنموذج هذا البروتوكول.

![مقارنة معدلات خطأ الكلمات والأحرف في الاختبارات العربية](/images/posts/863b02c12ee3.png)

WERهو معدل خطأ الكلمات؛ وCERهو معدل خطأ الأحرف. تشير القيمة الأقل إلى أداء أفضل.

قيّمناFalcon-ASRعلى مجموعات الاختبار الست نفسها، باستخدام قوائم العينات المثبّتة في لوحة المتصدرين. وأرقام النماذج المنافسة هي المتوسطات المنشورة في اللوحة، والتي جرى التحقق منها في30سبتمبر2026. وكان متوسط خطأ الكلمات للنموذج أفضل بمقدار2.25نقطة مئوية من أفضل نتيجة منشورة في تلك النسخة.

## تقييم اللهجة الإماراتية

تتوافر بالفعل بيانات عامة لتقييم اللهجة الإماراتية، إذ تضم مجموعةCasablancaقسمًا خاصًا بالإمارات. ونكمّل هذه التغطية بتقييم داخلي لتسجيلات إضافية من الكلام الإماراتي والخليجي، باستخدام تسجيلات مخصّصة للاختبار ونصوص مرجعية خضعت لمراجعة بشرية، لتقييم دقة التفريغ على مواد إضافية إلى جانب البيانات الإماراتية العامة.

حققFalcon-ASRفي تقييمنا الإماراتي الداخلي معدل خطأ كلمات قدره22.73٪ومعدل خطأ أحرف قدره10.19٪:

![مقارنة معدلات خطأ الكلمات والأحرف في التقييم الإماراتي](/images/posts/c77d1b0673dc.png)

سجّلFalcon-ASRأقل معدل لخطأ الكلمات والأحرف بين الأنظمة المقارَنة هنا. وكان معدل خطأ الكلمات أقل بمقدار4.07نقطة مئوية منQwen3-Omni، صاحب النتيجة التالية. وتُظهر النتائج تحسنًا في دقة التفريغ على مستوى الكلمات والأحرف في هذا التقييم.

## التدريب على ظروف تسجيل مختلفة

ضمّنا بيانات التدريب ضوضاء خلفية وكلامًا متداخلًا وموسيقى وصدى الصوت وتأثيرات الاتصالات الهاتفية، إلى جانب تغيّرات في سرعة الكلام وحدّة الصوت. وطبّقنا المعالجة نفسها على التسجيلات الإماراتية، لتهيئة النموذج للتعامل مع ظروف مختلفة قد يواجهها في الاجتماعات والمكالمات والتسجيلات اليومية الأخرى.

## الإنجليزية واللغات الأخرى

يفرّغFalcon-ASRالكلام الإنجليزي باستخدام أوزان النموذج نفسها. وفي تقييمنا على مجموعات الاختبار الإنجليزية العامة السبع المستخدمة في لوحةHugging Faceالمفتوحة للتعرف على الكلام، بلغ متوسط معدل خطأ الكلمات5.74٪.

![معدلات خطأ الكلمات في مجموعات الاختبار الإنجليزية](/images/posts/89b0644c418a.png)

[翻译失败，原文如下]

يدعم النموذج أيضًا الفرنسية والإسبانية والبرتغالية. وتستخدم اللغات الخمس أوزانًا واحدة، دون الحاجة إلى تحديد اللغة مسبقًا. ويكون الناتج تفريغًا نصيًا باللغة المنطوقة.

## أساس النموذج

يستندFalcon-ASRإلى أعمالنا فيFalcon3-Audio. وتعرض ورقةCompetitive Audio-Language Models with Data-Efficient Single-Stage Training on Public DataبنيةFalcon3-Audioونهج تدريبه.

## تجربةFalcon ASR

يتيحعرضنا التجريبي علىHugging FaceتجربةFalcon-ASRواستكشاف قدراته في تفريغ الكلام. أما الوصول عبر واجهةAPIوالتطبيقات الأصلية فهو مخطّط له. ندعوكم إلى تجربة النموذج باستخدام تسجيلاتكم.

## شكر وتقدير

نتوجّه بجزيل الشكر إلى الفريق القائم على تطوير نموذجFalcon-Emiratiعلى دعمهم في مجال النماذج التأسيسية للغة العربية. ويمكن الاطّلاع على أحدث أعمال الفريق من خلالالمقال المنشور حولFalcon-Emirati.

كما نتقدّم بخالص الشكر والتقدير إلىMikhail Lubinetsعلى دعمه المستمر للبنية التحتية الحاسوبية.

---

> 本文由AI自动翻译，原文链接：[Introducing Falcon ASR](https://huggingface.co/blog/tiiuae/falcon-asr)
> 
> 翻译时间：2026-10-10 08:17
