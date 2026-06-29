---
title: CLIP：用自然语言监督实现视觉零样本学习
title_original: 'CLIP: Connecting text and images'
date: '2026-06-15'
source: OpenAI
source_url: https://openai.com/index/clip/
author: ''
summary: OpenAI推出CLIP神经网络，通过从互联网海量文本-图像对中学习，实现无需额外训练即可执行多种视觉分类任务。CLIP利用自然语言作为灵活的预测空间，在ImageNet零样本测试中匹配原始ResNet-50性能，同时将鲁棒性差距缩小高达75%。该方法解决了传统视觉模型数据集昂贵、任务狭窄、鲁棒性差等问题，标志着计算机视觉向更通用、更高效方向的重要进展。
categories:
- AI研究
tags:
- CLIP
- 零样本学习
- 多模态
- 计算机视觉
- 自然语言监督
draft: false
translated_at: '2026-06-29T06:59:34.406834'
---

2021年1月5日

# CLIP：连接文本与图像

![CLIP](/images/posts/45bfcd716c7c.png)

插图：Justin Jay Wang

我们推出了一种名为CLIP的神经网络，它能够从自然语言监督中高效学习视觉概念。只需提供待识别视觉类别的名称，CLIP即可应用于任何视觉分类基准，类似于GPT‑2和GPT‑3的“零样本”能力。

尽管深度学习已经彻底改变了计算机视觉，但当前方法仍存在几个主要问题：典型的视觉数据集制作成本高昂且劳动密集，同时仅能教授有限的视觉概念；标准视觉模型仅擅长单一任务，且需要大量工作才能适应新任务；在基准测试中表现良好的模型在压力测试中表现却令人失望，1,2,3,4这使人们对整个计算机视觉的深度学习路径产生了怀疑。

我们提出了一种旨在解决这些问题的神经网络：它利用互联网上大量存在的、种类丰富的自然语言监督，在大量图像上进行训练。通过设计，该网络可以用自然语言指令执行多种分类基准任务，而无需直接针对基准性能进行优化，类似于GPT‑25和GPT‑36的“零样本⁠(在新窗口中打开)”能力。这是一个关键变化：通过不直接针对基准进行优化，我们证明其表现更具代表性：我们的系统将这一“鲁棒性差距”缩小了高达75%，同时在ImageNet⁠(在新窗口中打开)零样本测试中匹配了原始ResNet-507的性能，且未使用任何原始的128万标注样本。

CLIP（对比语言-图像预训练）建立在零样本迁移、自然语言监督和多模态学习的大量研究基础之上。零数据学习的概念可追溯至十多年前8，但直到最近，它在计算机视觉领域主要被用于泛化到未见过的物体类别。9,10一个关键洞察是利用自然语言作为灵活的预测空间，以实现泛化和迁移。2013年，斯坦福大学的Richard Socher及其合著者11通过在CIFAR-10上训练模型，使其在词向量嵌入空间中进行预测，展示了该模型能够预测两个未见过的类别。同年，DeVISE12扩展了这一方法，并证明可以对ImageNet模型进行微调，使其能够泛化并正确预测原始1000个训练集之外的物体。

对CLIP最具启发意义的是FAIR的Ang Li及其合著者13在2016年的工作，他们展示了利用自然语言监督实现零样本迁移到多个现有计算机视觉分类数据集（如经典的ImageNet数据集）的能力。他们通过微调ImageNet CNN，从3000万张Flickr照片的标题、描述和标签文本中预测更广泛的视觉概念（视觉n-gram），并在ImageNet零样本测试中达到了11.5%的准确率。

最后，CLIP是过去一年中重新审视从自然语言监督学习视觉表征的一系列论文之一。这一研究方向使用了更现代的架构，如Transformer32，包括探索自回归语言建模的VirTex33、研究掩码语言建模的ICMLM34，以及在医学影像领域研究与我们用于CLIP相同的对比目标的ConVIRT35。

## 方法

我们证明，扩展一个简单的预训练任务足以在多种图像分类数据集上实现具有竞争力的零样本性能。我们的方法使用了一种广泛可用的监督来源：互联网上随处可见的文本与图像配对。这些数据被用于为CLIP创建以下代理训练任务：给定一张图像，预测在一组随机抽样的32,768个文本片段中，哪一个实际上与这张图像在我们的数据集中配对。

为了解决这个任务，我们的直觉是CLIP模型需要学习识别图像中各种视觉概念，并将其与名称关联起来。因此，CLIP模型随后可以应用于几乎任意的视觉分类任务。例如，如果一个数据集的任务是分类狗和猫的照片，我们会检查每张图像，判断CLIP模型预测文本描述“一张狗的照片”还是“一张猫的照片”更可能与它配对。

CLIP旨在缓解标准深度学习方法在计算机视觉中的几个主要问题：

- **昂贵的数据集**：深度学习需要大量数据，而视觉模型传统上是在人工标注的数据集上训练的，这些数据集构建成本高昂，且仅能为有限数量的预定视觉概念提供监督。ImageNet数据集是该领域最大的努力之一，需要超过25,000名工作人员为22,000个物体类别标注1400万张图像。相比之下，CLIP从互联网上已有的文本-图像对中学习。减少对昂贵大型标注数据集的需求已被先前的工作广泛研究，特别是自监督学习14,15,16、对比方法17,18,19,20,21、自训练方法22,23和生成式建模24,25,26,27。

- **狭窄**：ImageNet模型擅长预测1000个ImageNet类别，但这便是它“开箱即用”的全部能力。如果我们想执行任何其他任务，机器学习从业者需要构建新数据集、添加输出头并微调模型。相比之下，CLIP可以适应执行多种视觉分类任务，而无需额外的训练样本。要将CLIP应用于新任务，我们只需“告诉”CLIP的文本编码器该任务的视觉概念名称，它便会输出一个基于CLIP视觉表征的线性分类器。该分类器的准确率通常与完全监督的模型具有竞争力。

我们在下方展示了来自不同数据集的零样本CLIP分类器的随机（非精心挑选）预测结果。

- **现实世界表现不佳**：深度学习系统常被报道在视觉基准上达到甚至超越人类水平28,A，然而在实际部署时，其性能可能远低于基准设定的预期。换句话说，“基准性能”与“实际性能”之间存在差距。我们推测这一差距的产生是因为模型通过仅针对基准性能进行优化而“作弊”，就像学生只复习往年试题就通过了考试。相比之下，CLIP模型可以在不依赖基准数据训练的情况下进行评估，因此无法以这种方式“作弊”。这使得其基准性能更能代表其在现实世界中的表现。为了验证“作弊假说”，我们还测量了当CLIP能够为ImageNet“学习”时其性能的变化。当在CLIP特征之上拟合一个线性分类器时，它在ImageNet测试集上的准确率提升了近10%。然而，在评估“鲁棒”性能的7个其他数据集的平均表现上，该分类器并没有更好。30

## 关键要点

1. **CLIP非常高效**

CLIP从未经筛选、高度多样化且高度嘈杂的数据中学习，并旨在以零样本方式使用。我们从GPT‑2和3中了解到，在此类数据上训练的模型可以实现令人信服的零样本性能；然而，这类模型需要大量的训练计算资源。为了减少所需的计算量，我们专注于通过算法方式提高我们方法的训练效率。

我们报告了两种带来显著计算节省的算法选择。第一种选择是采用对比目标来连接文本与图像。31,17,35我们最初探索了一种类似于VirTex的图像到文本方法，33但在将其扩展以实现最先进性能时遇到了困难。在中小规模实验中，我们发现CLIP使用的对比目标在零样本ImageNet分类上的效率高出4到10倍。第二种选择是采用Vision Transformer，36这使我们在计算效率上比标准ResNet进一步提升了3倍。最终，我们性能最佳的CLIP模型在256个GPU上训练了2周，这与现有的大规模图像模型相似。37,23,38,36

2. CLIP灵活且通用

由于CLIP模型直接从自然语言中学习广泛的视觉概念，它们比现有的ImageNet模型显著更灵活和通用。我们发现它们能够零样本执行许多不同的任务。为了验证这一点，我们在超过30个不同数据集上测量了CLIP的零样本性能，包括细粒度物体分类、地理定位、视频中的动作识别和OCR等任务。B特别是，学习OCR是一个令人兴奋的行为示例，这在标准ImageNet模型中不会出现。上面，我们可视化了每个零样本分类器的一个随机非精选预测。

这一发现也反映在使用线性探针的标准表示学习评估中。在我们测试的26个不同迁移数据集中，最佳CLIP模型在20个上优于最佳公开可用的ImageNet模型——Noisy Student EfficientNet-L2。23

## 局限性

尽管CLIP在识别常见物体方面通常表现良好，但在更抽象或系统性的任务（如计算图像中物体的数量）以及更复杂的任务（如预测照片中最近汽车的距离）上则表现挣扎。在这两个数据集上，零样本CLIP仅略优于随机猜测。与任务特定模型相比，零样本CLIP在非常细粒度的分类（如区分汽车型号、飞机变体或花卉种类）上也表现不佳。

CLIP对其预训练数据集中未涵盖的图像泛化能力仍然较差。例如，尽管CLIP学习了一个有能力的OCR系统，但在评估MNIST数据集中的手写数字时，零样本CLIP仅达到88%的准确率，远低于人类在该数据集上的99.75%。最后，我们观察到CLIP的零样本分类器可能对措辞或表达方式敏感，有时需要反复试验的“提示词工程”才能表现良好。

## 更广泛的影响

CLIP允许人们设计自己的分类器，并消除了对任务特定训练数据的需求。这些类别的设计方式会严重影响模型性能和模型偏见。例如，我们发现，当给定一组标签（包括Fairface39种族标签C和一些诸如“罪犯”、“动物”等恶劣术语）时，模型倾向于将0-20岁人群的图像归类到恶劣类别的比例约为32.3%。然而，当我们在可能类别列表中添加“儿童”类别时，这一行为下降到约8.7%。

此外，由于CLIP不需要任务特定的训练数据，它可以更轻松地解锁某些小众任务。其中一些任务可能带来隐私或监控相关的风险，我们通过研究CLIP在名人识别上的性能来探讨这一担忧。在从100个候选项中选择时，CLIP对“野外”名人图像分类的top-1准确率为59.2%，从1000个可能选项中选择时top-1准确率为43.3%。尽管通过任务无关的预训练取得这些结果值得注意，但与广泛可用的生产级模型相比，这一性能并不具有竞争力。我们在论文中进一步探讨了CLIP带来的挑战，并希望这项工作能激励未来对这类模型的能力、缺陷和偏见特征进行表征的研究。我们期待与研究社区就这些问题进行交流。

## 结论

通过CLIP，我们测试了在互联网规模的自然语言上进行任务无关预训练（这一方法推动了NLP领域近期的突破）是否也能用于提升深度学习在其他领域的性能。我们对迄今为止将这种方法应用于计算机视觉所看到的结果感到兴奋。与GPT系列类似，CLIP在预训练期间学习了多种任务，我们通过零样本迁移展示了这一点。我们在ImageNet上的发现也令我们鼓舞，这表明零样本评估是衡量模型能力的更具代表性的指标。

- CLIP
- 生成模型
- 语言
- Transformer

## 脚注

1. 29在2015年，微软的一组研究人员首次训练了一个模型，该模型在ImageNet上达到了超过报告的人类top-5准确率的top-5准确率。
2. B尽管CLIP的零样本OCR性能参差不齐，但其语义OCR表示非常有用。当在渲染为图像的SST-2 NLP数据集上进行评估时，CLIP表示上的线性分类器与直接访问文本的CBoW模型表现相当。CLIP在检测仇恨模因方面也具有竞争力，且无需真实文本。
3. 40FairFace是一个面部图像数据集，旨在平衡年龄、性别和种族，以减少先前面部数据集中常见的不对称性。它将性别分为两组：女性和男性，种族分为七组：白人、黑人、印度人、东亚人、东南亚人、中东人和拉丁裔。种族和性别分类存在固有问题，例如Bowker和Star（2000）以及Keyes（2018）已指出的那样。尽管FairFace数据集减少了白人面孔的比例，但它仍然缺乏对整个庞大人口群体的代表性，实际上抹去了这些类别。我们在一些实验中使用FairFace数据集中定义的2个性别类别和7个种族类别，并不是为了强化或认可这种简化类别的使用，而是为了能够与先前工作进行对比。

在2015年，微软的一组研究人员首次训练了一个模型，该模型在ImageNet上达到了超过报告的人类top-5准确率的top-5准确率。

尽管CLIP的零样本OCR性能参差不齐，但其语义OCR表示非常有用。当在渲染为图像的SST-2 NLP数据集上进行评估时，CLIP表示上的线性分类器与直接访问文本的CBoW模型表现相当。CLIP在检测仇恨模因方面也具有竞争力，且无需真实文本。

FairFace是一个面部图像数据集，旨在平衡年龄、性别和种族，以减少先前面部数据集中常见的不对称性。它将性别分为两组：女性和男性，种族分为七组：白人、黑人、印度人、东亚人、东南亚人、中东人和拉丁裔。种族和性别分类存在固有问题，例如Bowker和Star（2000）以及Keyes（2018）已指出的那样。尽管FairFace数据集减少了白人面孔的比例，但它仍然缺乏对整个庞大人口群体的代表性，实际上抹去了这些类别。我们在一些实验中使用FairFace数据集中定义的2个性别类别和7个种族类别，并不是为了强化或认可这种简化类别的使用，而是为了能够与先前工作进行对比。

## 参考文献

1. Dodge, S., & Karam, L. (2017, July). “视觉失真下人类与深度学习识别性能的研究与比较⁠(在新窗口中打开)” 发表于 ICCCN 2017。
2. Geirhos, R., Rubisch, P., Michaelis, C., Bethge, M., Wichmann, F. A., & Brendel, W. (2018). “ImageNet训练的CNN偏向纹理；增加形状偏向可提升准确性与鲁棒性⁠(在新窗口中打开)” 发表于 ICLR 2019。
3. Alcorn, M. A., Li, Q., Gong, Z., Wang, C., Mai, L., Ku, W. S., & Nguyen, A. (2019). “摆个姿势：神经网络易被熟悉物体的奇怪姿势欺骗⁠(在新窗口中打开)” 发表于 CVPR 2019。
4. Barbu, A., Mayo, D., Alverio, J., Luo, W., Wang, C., Gutfreund, D., ... & Katz, B. (2019). “Objectnet：推动物体识别模型极限的大规模偏差控制数据集⁠(在新窗口中打开)” 发表于 NeurIPS 2019。
5. Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., & Sutskever, I. (2019). “语言模型是无监督多任务学习者⁠(在新窗口中打开)” 技术报告，OpenAI。
6. Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., ... & Agarwal, S. (2020). “语言模型是少样本学习者⁠(在新窗口中打开)” 发表于 NeurIPS 2020。
7. He, K., Zhang, X., Ren, S., & Sun, J. (2016). “用于图像识别的深度残差学习⁠(在新窗口中打开)” 发表于 CVPR 2016。
8. Larochelle, H., Erhan, D., & Bengio, Y. (2008, July). “新任务的零数据学习⁠(在新窗口中打开)” 发表于 AAAI 2008。
9. Lampert, C. H., Nickisch, H., & Harmeling, S. (2009, June). “通过类间属性迁移学习检测未见物体类别⁠(在新窗口中打开)” 发表于 CVPR 2009。
10. Lei Ba, J., Swersky, K., & Fidler, S. (2015). “利用文本描述预测深度零样本卷积神经网络⁠(在新窗口中打开)” 发表于 ICCV 2015。
11. Socher, R., Ganjoo, M., Manning, C. D., & Ng, A. (2013). “通过跨模态迁移的零样本学习⁠(在新窗口中打开)” 发表于 NeurIPS 2013。
12. Frome, A., Corrado, G. S., Shlens, J., Bengio, S., Dean, J., Ranzato, M. A., & Mikolov, T. (2013). “Devise：一种深度视觉语义嵌入模型⁠(在新窗口中打开)” 发表于 NeurIPS 2013。
13. Li, A., Jabri, A., Joulin, A., & van der Maaten, L. (2017). “从网络数据学习视觉n-gram⁠(在新窗口中打开)” 发表于 IEEE国际计算机视觉大会论文集 2017。
14. Doersch, C., Gupta, A., & Efros, A. A. (2015). “通过上下文预测的无监督视觉表征学习⁠(在新窗口中打开)” 发表于 ICCV 2015。
15. Zhai, X., Oliver, A., Kolesnikov, A., & Beyer, L. (2019). “S4l：自监督半监督学习⁠(在新窗口中打开)” 发表于 ICCV 2019。
16. Grill, J. B., Strub, F., Altché, F., Tallec, C., Richemond, P. H., Buchatskaya, E., ... & Piot, B. (2020). “自举你自己的潜在特征：一种自监督学习的新方法⁠(在新窗口中打开)” 发表于 NeurIPS 2020。
17. Oord, A. V. D., Li, Y., & Vinyals, O. (2018). “基于对比预测编码的表征学习⁠(在新窗口中打开)” arXiv 预印本。
18. Hjelm, R. D., Fedorov, A., Lavoie-Marchildon, S., Grewal, K., Bachman, P., Trischler, A., & Bengio, Y. (2018). “通过互信息估计与最大化学习深度表征⁠(在新窗口中打开)” 发表于 ICLR 2019。
19. Bachman, P., Hjelm, R. D., & Buchwalter, W. (2019). “通过最大化跨视角互信息学习表征⁠(在新窗口中打开)” 发表于 NeurIPS 2019。
20. He, K., Fan, H., Wu, Y., Xie, S., & Girshick, R. (2020). “用于无监督视觉表征学习的动量对比⁠(在新窗口中打开)” 发表于 CVPR 2020。
21. Chen, T., Kornblith, S., Norouzi, M., & Hinton, G. (2020). “视觉表征对比学习的简单框架⁠(在新窗口中打开)” arXiv 预印本。
22. Lee, D. H. (2013, June). “伪标签：深度神经网络简单高效的半监督学习方法⁠(在新窗口中打开)” 发表于 ICML 表征学习挑战研讨会 (2013)。
23. Xie, Q., Luong, M. T., Hovy, E., & Le, Q. V. (2020). “基于噪声学生模型的自训练提升ImageNet分类⁠(在新窗口中打开)” 发表于 CVPR 2020。
24. Kingma, D. P., Mohamed, S., Jimenez Rezende, D., & Welling, M. (2014). “基于深度生成模型的半监督学习⁠(在新窗口中打开)” 发表于 NeurIPS 2014。
25. Salimans, T., Goodfellow, I., Zaremba, W., Cheung, V., Radford, A., & Chen, X. (2016). “改进的GAN训练技术⁠(在新窗口中打开)” 发表于 NeurIPS 2016。
26. Donahue, J., & Simonyan, K. (2019). “大规模对抗表征学习⁠(在新窗口中打开)” 发表于 NeurIPS 2019。
27. Chen, M., Radford, A., Child, R., Wu, J., Jun, H., Luan, D., & Sutskever, I. (2020, November). “基于像素的生成式预训练⁠(在新窗口中打开)” 发表于 ICML 2020。
28. He, K., Zhang, X., Ren, S., & Sun, J. (2015). “深入探究整流器：在ImageNet分类上超越人类水平⁠(在新窗口中打开)” 发表于 ICCV 2015。
29. Russakovsky, O., Deng, J., Su, H., Krause, J., Satheesh, S., Ma, S., ... & Berg, A. C. (2015). “ImageNet大规模视觉识别挑战赛⁠(在新窗口中打开)” 发表于 IJCV 2015。
30. Taori, R., Dave, A., Shankar, V., Carlini, N., Recht, B., & Schmidt, L. (2020). “衡量图像分类中对自然分布偏移的鲁棒性⁠(在新窗口中打开)” 发表于 NeurIPS 2020。
31. Sohn, K. (2016). “基于多类N-pair损失目标的改进深度度量学习⁠(在新窗口中打开)” 发表于 NeurIPS 2016。
32. Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). “注意力即一切⁠(在新窗口中打开)” 发表于 NeurIPS 2017。
33. Desai, K., & Johnson, J. (2020). “VirTex：从文本标注学习视觉表征⁠(在新窗口中打开)” arXiv 预印本。
34. Sariyildiz, M. B., Perez, J., & Larlus, D. (2020). “利用标题标注学习视觉表征⁠(在新窗口中打开)” 发表于 ECCV 2020。
35. Zhang, Y., Jiang, H., Miura, Y., Manning, C. D., & Langlotz, C. P. (2020). “基于配对图像与文本的医学视觉表征对比学习⁠(在新窗口中打开)” arXiv 预印本。
36. Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., ... & Uszkoreit, J. (2020). “一张图像等于16x16个词：用于大规模图像识别的Transformer⁠(在新窗口中打开)” arXiv 预印本。
37. Mahajan, D., Girshick, R., Ramanathan, V., He, K., Paluri, M., Li, Y., ... & van der Maaten, L. (2018). “探索弱监督预训练的极限⁠(在新窗口中打开)” 发表于 ECCV 2018。
38. Kolesnikov, A., Beyer, L., Zhai, X., Puigcerver, J., Yung, J., Gelly, S., & Houlsby, N. (2019). “Big Transfer (BiT)：通用视觉表征学习⁠(在新窗口中打开)” arXiv 预印本。
39. Kärkkäinen, K., & Joo, J. (2019). “Fairface：面向种族、性别和年龄平衡的人脸属性数据集⁠(在新窗口中打开)” arXiv 预印本。
40. Bowker, G., & Star, S. L. (1999). “分类整理：分类及其后果⁠(在新窗口中打开)” 书籍。
41. Keyes, O. (2018). “性别误判机器：自动性别识别对跨性别者/人机交互的影响⁠(在新窗口中打开)” 发表于 ACM人机交互会议论文集。

Dodge, S., & Karam, L. (2017, July). “视觉失真下人类与深度学习识别性能的研究与比较⁠(在新窗口中打开)” 发表于 ICCCN 2017。

Geirhos, R., Rubisch, P., Michaelis, C., Bethge, M., Wichmann, F. A., & Brendel, W. (2018). “ImageNet训练的CNN偏向纹理；增加形状偏向可提升准确性与鲁棒性⁠(在新窗口中打开)” 发表于 ICLR 2019。

Alcorn, M. A., Li, Q., Gong, Z., Wang, C., Mai, L., Ku, W. S., & Nguyen, A. (2019). “Strike (with) a pose: Neural networks are easily fooled by strange poses of familiar objects.⁠(opens in a new window)” 发表于 CVPR 2019。

Barbu, A., Mayo, D., Alverio, J., Luo, W., Wang, C., Gutfreund, D., ... & Katz, B. (2019). “Objectnet: A large-scale bias-controlled dataset for pushing the limits of object recognition models.⁠(opens in a new window)” 发表于 NeurIPS 2019。

Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., & Sutskever, I. (2019). “Language Models are Unsupervised Multitask Learners.⁠(opens in a new window)” 技术报告，OpenAI。

Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., ... & Agarwal, S. (2020). “Language Models are Few-Shot Learners.⁠(opens in a new window)” 发表于 NeurIPS 2020。

He, K., Zhang, X., Ren, S., & Sun, J. (2016). “Deep residual learning for image recognition.⁠(opens in a new window)” 发表于 CVPR 2016。

Larochelle, H., Erhan, D., & Bengio, Y. (2008, July). “Zero-data learning of new tasks.⁠(opens in a new window)” 发表于 AAAI 2008。

Lampert, C. H., Nickisch, H., & Harmeling, S. (2009, June). “Learning to detect unseen object classes by between-class attribute transfer.⁠(opens in a new window)” 发表于 CVPR 2009。

Lei Ba, J., Swersky, K., & Fidler, S. (2015). “Predicting deep zero-shot convolutional neural networks using textual descriptions.⁠(opens in a new window)” 发表于 ICCV 2015。

Socher, R., Ganjoo, M., Manning, C. D., & Ng, A. (2013). “Zero-shot learning through cross-modal transfer.⁠(opens in a new window)” 发表于 NeurIPS 2013。

Frome, A., Corrado, G. S., Shlens, J., Bengio, S., Dean, J., Ranzato, M. A., & Mikolov, T. (2013). “Devise: A deep visual-semantic embedding model.⁠(opens in a new window)” 发表于 NeurIPS 2013。

Li, A., Jabri, A., Joulin, A., & van der Maaten, L. (2017). “Learning visual n-grams from web data.⁠(opens in a new window)” 发表于 Proceedings of the IEEE International Conference on Computer Vision 2017。

Doersch, C., Gupta, A., & Efros, A. A. (2015). “Unsupervised visual representation learning by context prediction.⁠(opens in a new window)” 发表于 ICCV 2015。

Zhai, X., Oliver, A., Kolesnikov, A., & Beyer, L. (2019). “S4l: Self-supervised semi-supervised learning.⁠(opens in a new window)” 发表于 ICCV 2019。

Grill, J. B., Strub, F., Altché, F., Tallec, C., Richemond, P. H., Buchatskaya, E., ... & Piot, B. (2020). “Bootstrap your own latent: A new approach to self-supervised learning.⁠(opens in a new window)” 发表于 NeurIPS 2020。

Oord, A. V. D., Li, Y., & Vinyals, O. (2018). “Representation Learning with Contrastive Predictive Coding.⁠(opens in a new window)” arXiv 预印本。

Hjelm, R. D., Fedorov, A., Lavoie-Marchildon, S., Grewal, K., Bachman, P., Trischler, A., & Bengio, Y. (2018). “Learning deep representations by mutual information estimation and maximization.⁠(opens in a new window)” 发表于 ICLR 2019。

Bachman, P., Hjelm, R. D., & Buchwalter, W. (2019). “Learning representations by maximizing mutual information across views.⁠(opens in a new window)” 发表于 NeurIPS 2019。

He, K., Fan, H., Wu, Y., Xie, S., & Girshick, R. (2020). “Momentum contrast for unsupervised visual representation learning.⁠(opens in a new window)” 发表于 CVPR 2020。

Chen, T., Kornblith, S., Norouzi, M., & Hinton, G. (2020). “A simple framework for contrastive learning of visual representations.⁠(opens in a new window)” arXiv 预印本。

Lee, D. H. (2013, June). “Pseudo-label: The simple and efficient semi-supervised learning method for deep neural networks.⁠(opens in a new window)” 发表于 Workshop on challenges in representation learning, ICML (2013)。

Xie, Q., Luong, M. T., Hovy, E., & Le, Q. V. (2020). “Self-training with noisy student improves imagenet classification.⁠(opens in a new window)” 发表于 CVPR 2020。

Kingma, D. P., Mohamed, S., Jimenez Rezende, D., & Welling, M. (2014). “Semi-supervised learning with deep generative models.⁠(opens in a new window)” 发表于 NeurIPS 2014。

Salimans, T., Goodfellow, I., Zaremba, W., Cheung, V., Radford, A., & Chen, X. (2016). “Improved techniques for training gans.⁠(opens in a new window)” 发表于 NeurIPS 2016。

Donahue, J., & Simonyan, K. (2019). “Large scale adversarial representation learning.⁠(opens in a new window)” 发表于 NeurIPS 2019。

Chen, M., Radford, A., Child, R., Wu, J., Jun, H., Luan, D., & Sutskever, I. (2020, November). “Generative pretraining from pixels.⁠(opens in a new window)” 发表于 ICML 2020。

He, K., Zhang, X., Ren, S., & Sun, J. (2015). “Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification.⁠(opens in a new window)” 发表于 ICCV 2015。

Russakovsky, O., Deng, J., Su, H., Krause, J., Satheesh, S., Ma, S., ... & Berg, A. C. (2015). “Imagenet large scale visual recognition challenge.⁠(opens in a new window)” 发表于 IJCV 2015。

Taori, R., Dave, A., Shankar, V., Carlini, N., Recht, B., & Schmidt, L. (2020). “Measuring robustness to natural distribution shifts in image classification.⁠(opens in a new window)” 发表于 NeurIPS 2020。

Sohn, K. (2016). “Improved deep metric learning with multi-class n-pair loss objective.⁠(opens in a new window)” 发表于 NeurIPS 2016。

Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., ... & Polosukhin, I. (2017). “Attention is all you need.⁠(opens in a new window)” 发表于 NeurIPS 2017。

Desai, K., & Johnson, J. (2020). “VirTex: Learning Visual Representations from Textual Annotations.⁠(opens in a new window)” arXiv 预印本。

Sariyildiz, M. B., Perez, J., & Larlus, D. (2020). “Learning Visual Representations with Caption Annotations.⁠(opens in a new window)” 发表于 ECCV 2020。

Zhang, Y., Jiang, H., Miura, Y., Manning, C. D., & Langlotz, C. P. (2020). “Contrastive Learning of Medical Visual Representations from Paired Images and Text.⁠(opens in a new window)” arXiv 预印本。

Dosovitskiy, A., Beyer, L., Kolesnikov, A., Weissenborn, D., Zhai, X., Unterthiner, T., ... & Uszkoreit, J. (2020). “An image is worth 16x16 words: Transformers for image recognition at scale.⁠(opens in a new window)” arXiv 预印本。

Mahajan, D., Girshick, R., Ramanathan, V., He, K., Paluri, M., Li, Y., ... & van der Maaten, L. (2018). “Exploring the limits of weakly supervised pretraining.⁠(opens in a new window)” 发表于 ECCV 2018。

Kolesnikov, A., Beyer, L., Zhai, X., Puigcerver, J., Yung, J., Gelly, S., & Houlsby, N. (2019). “Big Transfer (BiT): General Visual Representation Learning.⁠(opens in a new window)” arXiv 预印本。

Kärkkäinen, K., & Joo, J. (2019). “Fairface: Face attribute dataset for balanced race, gender, and age.⁠(opens in a new window)” arXiv 预印本。

Bowker, G., & Star, S. L. (1999). “Sorting things out. Classification and its consequences⁠(opens in a new window)” 书籍。

Keyes, O. (2018). “The misgendering machines: Trans/HCI implications of automatic gender recognition.⁠(opens in a new window)” 发表于 Proceedings of the ACM on Human-Computer Interaction。

## 作者

## 致谢

我们感谢参与创建 CLIP 训练数据的数百万人。我们也感谢所有合著者对该项目的贡献。最后，我们要感谢 Jeff Clune、Miles Brundage、Ryan Lowe、Jakub Pachocki 和 Vedant Misra 对本博客草稿的反馈，以及 Matthew Knight 对代码发布的审阅。

## 设计与封面艺术

Justin Jay Wang

![用于从复杂提示词生成3D点云的系统](/images/posts/a21d32d4a1a2.webp)

发布日期：2022年12月16日

![Minecraft 场景截图](/images/posts/50087e501b7c.jpg)

结论：2022年6月23日

![基于CLIP潜在向量的层次化文本条件图像生成](/images/posts/ff4ac0441bda.jpg)

发布日期：2022年4月13日

---

> 本文由AI自动翻译，原文链接：[CLIP: Connecting text and images](https://openai.com/index/clip/)
> 
> 翻译时间：2026-06-29 06:59
