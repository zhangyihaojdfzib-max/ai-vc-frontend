---
title: Broadening access to Skala creates a faster path to predictive DFT
title_original: Broadening access to Skala creates a faster path to predictive DFT
date: '2026-08-20'
source: Microsoft Research
source_url: https://www.microsoft.com/en-us/research/blog/broadening-access-to-skala-creates-a-faster-path-to-predictive-dft/
author: ''
summary: '[翻译失败，原文如下]


  ![Schematic of the Skala architecture, showing how meta-GGA electronic features
  are transformed through point-wise processing and non-loc...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-08-26T02:59:37.863793'
---

[翻译失败，原文如下]

![Schematic of the Skala architecture, showing how meta-GGA electronic features are transformed through point-wise processing and non-local atomic interactions to predict density functional theory energies.](/images/posts/1469832a01a8.jpg)

## At a glance

- Skala 1.1 demonstrates the continuously improving nature of Microsoft Research’s deep-learning DFT approach: trained on 2.5× more data than its predecessor, it delivers substantially higher accuracy across key molecular simulation challenges, including thermochemistry, reaction kinetics, and molecular structure prediction.
- Skala is now available inCP2Kand is being integrated intoPsi4,FHI-aims,ORCAandVASP, bringing next-generation DFT accuracy closer to the communities that rely on these codes every day.
- Microsoft Research is also introducing a living benchmark that will track the computational performance of successive, increasingly optimized Skala releases to help the community measure and accelerate progress toward ever greater accuracy and efficiency.
- Together, these developments mark another milestone toward a future in which computational chemistry simulations are both predictive and integrated in all relevant scientific and industrial workflows.

Bringing density functional theory (DFT) to predictive accuracy is a journey, not a single breakthrough.Sinceintroducing Skala, our deep-learning exchange-correlation functional, we have continued to advance along two complementary fronts: improving accuracy and expanding accessibility across the computational chemistry ecosystem.

On the accuracy front, therelease ofSkala-1.1(opens in new tab)provides the first demonstration of the continuous-improvement paradigm underlying Skala. Trained on 2.5x more data than the first public version of Skala, the updated  model delivers substantially improved performance across key challenges in molecular simulation, including main-group thermochemistry, reaction kinetics, and molecular structure prediction.

But accuracy alone is not enough. DFT is the computational engine behind a vast range of scientific and industrial workflows, spanning chemistry, materials science, catalysis, energy technologies, and drug discovery. To have real-world impact, advanced functionals must be accessible where scientists already perform their calculations. That is why we are also expanding the Skala ecosystem through collaborations with leading electronic-structure software developers.

Today, we are announcing that Skala is available inCP2Kand is being integrated intoPsi4,FHI-aims,ORCAandVASP,  bringing next-generation DFT accuracy closer to the communities that rely on these codes every day. Alongside these integration efforts, we are introducing a living benchmark that tracks the computational performance of successive, increasingly optimized Skala releases. By providing a transparent and continuously updated reference for implementations across software packages and hardware platforms, this resource will help the community measure and accelerate progress toward ever greater accuracy and efficiency.

Together, these developments mark another milestone toward a future in which computational chemistry simulations are both predictive and accessible across a broader range of relevant scientific and industrial workflows.

Want to learn more about Skala and why DFT plays such an important role in in-silico discovery? Read alsoour first blog post(opens in new tab).

## Skala as a continuously improving functional

Unlike the traditional “functional zoo”, where new functionals accumulate without replacing older ones, Skala follows a different philosophy: each release is designed to supersede the previous one. As new data, model architectures, and training strategies become available, the model improves while maintaining the same practical computational cost.

Skala-1.1is the latest demonstration of this approach. It achieves a weighted average error of2.8 kcal/mol on GMTKN55, a widely used benchmark suite comprising 55 categories of chemistry, including thermochemistry, reaction barriers, and noncovalent interactions. This level of accuracy surpasses today’s leading global (range-separated) hybrid functionals while retaining the efficiency of a semi-local functional. Beyond energies, Skala-1.1 also provides highly accurate electron densities, dipole moments, and molecular geometries.

These advances were enabled by major expansions of theMicrosoft Research Accurate Chemistry Collection(opens in new tab)(MSR-ACC), our large-scale collection of high-accuracy quantum-chemistry reference data generated with expensive wavefunction methods. For Skala-1.1, we added new categories, including electron affinities and noncovalent clusters, increasing both the size and, crucially, the diversity of the training data. This data-driven approach allows Skala to improve systematically with each generation, moving us closer to a truly scalable and predictive DFT framework.

## Available where scientists work

To fully realize the potential of Skala’s continuously evolving approach to DFT, we need dedicated infrastructure that allows new releases to be rapidly and seamlessly integrated into the major software packages used by scientists in industry and academia. In turn, this will establish the fast feedback loop essential for accelerating Skala’s ongoing development.

We first made Skala available through ouropen-source community release(opens in new tab), built on (GPU4)PySCF(opens in new tab)andintegrated with ASE(opens in new tab). This enables researchers to evaluate and apply Skala with minimal effort while benefiting from highly optimized CPU and GPU performance.

But no single software package can meet the needs of every application or research community. Computational chemistry and materials science rely on a rich ecosystem of electronic-structure codes, each shaped over decades to tackle specific scientific and industrial challenges. Bringing Skala to this broader ecosystem has therefore been a major focus of the past year. We are fortunate to build on the remarkable foundations created by the DFT community and grateful to the many researchers and developers who are helping to make Skala available within the software platforms that scientists use every day.

Spotlight: Event Series

![Research Forum | abstract background with colorful hexagons](/images/posts/37efe5ead00f.jpg)

## Microsoft Research Forum

Join us for a continuous exchange of ideas about research in the era of general AI. Watch the latest episodes on demand.

## From community release to native integrations

In collaboration with the team of Prof. Thomas D. Kühne at theCenter for Advanced Systems Understanding (CASUS)(opens in new tab), Skala has been successfully integrated into the open-sourceCP2K(opens in new tab)package. With more than 25 years of development, CP2K is a powerhouse for DFT simulations, particularly for large-scale systems and long-timescale molecular dynamics, while also providing a rich portfolio of high-accuracy electronic-structure methods. Skala expands the frontiers of what is possible within CP2K, delivering a step change in DFT accuracy while preserving the computational efficiency needed for simulations at scale. We are excited to see how CP2K’s scale and versatility, combined with Skala’s continuously improving accuracy, will enable new scientific applications and discoveries in the years ahead.

There is more to come. Together with its vibrant developer’s community , we are actively integrating Skala into the open-sourcePsi4(opens in new tab)package, an essential platform for molecular electronic-structure research. Combined with the PySCF-based Skala Community Edition, this will make Skala available in three widely used open-source quantum chemistry packages.

[翻译失败，原文如下]

Beyond open-source software, we are working closely with leading developers behindFHI-aims(opens in new tab),ORCA(opens in new tab), andVASP(opens in new tab), with the goal of making Skala broadly accessible across the major software platforms used in computational chemistry and materials science.

## Validating accuracy across implementations: CP2K as case study

Thorough testing is essential for any new implementation. We want to ensure that Skala delivers consistent accuracy across different codes and computational settings. Together with the CP2K team, we developed a comprehensive suite of integration tests to verify that Skala produces numerically correct and reliable results. We are particularly grateful to the CASUS team, whose deep expertise in the numerical verification of computational methods was instrumental in designing and validating this testing framework.

![Figure 2: Signed errors relative to high-accuracy reference values for a representative subset of GMTKN55, comparing the CP2K and PySCF implementations of Skala-1.1 using as closely matched numerical settings as possible. The two implementations agree to within 0.1 kcal/mol MAD across the entire subset.](/images/posts/af8edc938ce9.png)

A detailed discussion of the implementation, validation strategy, and testing infrastructure for Skala in CP2K can be found in our joint paper with the CASUS team: “Molecular Implementation of the Machine-Learned Skala Exchange-Correlation Functional in CP2K through GauXC.”

## A living performance report for Skala

Accuracy and broad availability only translate into scientific impact if Skala is also fast. Today, Skala can deliver performance comparable to semi-local meta-GGAs on both CPU’s (with an overhead that disappears for molecules with more than 20-30 atoms) and GPUs, and we are committed to preserving that efficiency as it is integrated across the electronic-structure software ecosystem.

But performance is not a fixed property. New Skala releases, improvements in libraries such as GauXC, and hardware-specific optimizations continuously improve efficiency and reveal new opportunities for further gains. Capturing this progress requires more than a single benchmark snapshot.

To provide a transparent and up-to-date view of Skala’s performance, we are publishing abenchmarking harness together with a living performance report(opens in new tab)that will be updated as new optimizations become available. This report tracks performance across a range of tasks and hardware platforms, while the harness enables package developers to benchmark, validate, and improve their own Skala implementations.

![Figure 3: Computational cost of Skala on GPU and CPU, compared with a popular metaGGA functional (r2SCAN) and two hybrid functionals (B3LYP and M06-2X). On GPU, Skala 1.1 has the same cost as r2SCAN, and the hybrid functionals become more expensive for systems with more than ~1000 orbitals. On CPU, Skala has an overhead with respect to the other functionals for smaller systems, that disappears for systems with more than ~300 orbitals.](/images/posts/da176b3d30e4.png)

## Acknowledgments

Skala is the product of a truly collaborative effort across AI for Science, and we thank our engineering, project management, and business operations teams for making this work possible. We also thank MSR Accelerator for their partnership in advancing data generation efforts and accelerating software integrations that help bring Skala to the broader scientific community.

## Meet the authors

### Sebastian Ehlert

Senior Researcher

### Stefano Battaglia

### Thijs Vogels

Senior Research Software Engineer

### Jan Hermann

Principal Research Manager

### Jens Wehner

Senior Software Engineer

### Giulia Luise

### Klaas Giesbertz

### Chin-Wei Huang

### Aaron Kaplan

### Kate Milton

Senior Research Engineer

### Stephanie Marisa Lanius

Senior Data Engineer

### Derk Kooi

### P. Bernát Szabó

### Gregor Simm

### Rianne van den Berg

Senior Principal Research Manager

### Paola Gori Giorgi

---

> 本文由AI自动翻译，原文链接：[Broadening access to Skala creates a faster path to predictive DFT](https://www.microsoft.com/en-us/research/blog/broadening-access-to-skala-creates-a-faster-path-to-predictive-dft/)
> 
> 翻译时间：2026-08-26 02:59
