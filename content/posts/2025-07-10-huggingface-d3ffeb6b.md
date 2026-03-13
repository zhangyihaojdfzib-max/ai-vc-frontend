---
title: Kimina-Prover：测试时强化学习提升定理证明能力
title_original: 'Kimina-Prover: Applying Test-time RL Search on Large Formal Reasoning
  Models'
date: '2025-07-10'
source: Hugging Face Blog
source_url: https://huggingface.co/blog/AI-MO/kimina-prover
author: ''
summary: 本文介绍了Numina & Kimi团队发布的最新定理证明模型Kimina-Prover-72B及其蒸馏变体。该模型的核心创新在于引入了测试时强化学习搜索框架，特别是“启用引理”模式，使模型能够递归地发现、组合并应用多个引理来构建复杂证明。此外，模型还具备错误修复能力，可解读Lean错误信息并提出针对性修复方案。这些技术使Kimina-Prover在miniF2F基准测试中达到了92.2%的最先进通过率，显著超越了先前方法。
categories:
- AI研究
tags:
- 自动定理证明
- 强化学习
- 形式化验证
- 大语言模型
- 数学推理
draft: false
translated_at: '2026-03-13T05:00:32.265216'
---

# Kimina-Prover：在大型形式推理模型上应用测试时强化学习搜索

Numina & Kimi 团队

![kimina_prover_main_result](/images/posts/f864cad33b3e.png)

我们很高兴地宣布发布 **Kimina-Prover-72B**，这是我们基于 Qwen2.5-72B[2]，使用 Kimi k1.5[1] RL 流程训练的最先进的定理证明模型。同时，我们还发布了两个蒸馏变体：**Kimina-Prover-Distill-8B** 和 **1.7B**（分别基于 Qwen3-8B 和 Qwen3-1.7B[3]）。

我们的核心创新包括：

*   **测试时强化学习搜索**：一个可训练的智能体证明框架，使模型能够基于一种新颖的“启用引理”模式，递归地发现、组合并应用多个引理来构建复杂的证明。
*   **错误修复能力**：Kimina-Prover 能够读取并解释 Lean 的错误信息，并提出针对性的修复方案，与从头开始重新生成证明相比，展现出显著更高的样本效率。

这些进步使 Kimina-Prover 能够解决具有挑战性的数学问题并超越先前的方法。如图 1 所示，在广泛使用的 miniF2F 基准测试中，Kimina-Prover 实现了 **92.2%** 的最先进通过率。

# 引言

我们专注于 Lean 4 语言中的自动定理证明（ATP），旨在自动化形式化数学证明的构建。神经定理证明领域的最新进展显著提升了 AI 系统辅助或自动化此过程的能力。值得注意的进展包括来自 Google DeepMind 的 **AlphaProof**[4]，它在国际数学奥林匹克竞赛级别的问题上展现了强大的性能。结合了强化学习的开源系统如 **DeepSeek-Prover-V2**[5] 也取得了最先进的结果。此外，像 **DSP+**[6] 这样的神经符号智能体方法表明，通过在模块化框架中利用现成的模型，无需大规模训练也能获得有竞争力的性能。

我们早期的 Kimina-Prover Preview[7] 工作介绍了一个用于 Lean 形式定理证明的大语言模型，在 miniF2F 基准上建立了新的性能基线。该模型通过大规模强化学习流程进行训练，采用了推理驱动的探索范式，并证明了更大的模型可以成为更强大的形式推理器。其结构化的推理模式实现了高效的证明搜索，并模拟了类人的问题解决策略。

在取得初步成功后，我们通过进一步的强化学习迭代继续改进模型。然而，单步推理对于解决需要长篇幅、多阶段证明的复杂问题仍然不足。为了解决这一限制，我们引入了**测试时强化学习（TTRL）搜索框架**，使模型能够自主发现、组合和重用多个中间引理。该框架通过将难题分解为可重用的子组件，支持更深层次、更长视野的推理。

TTRL 搜索的一个关键要素是**启用引理模式**，它允许模型在证明构建过程中识别并应用中间引理。这种对中间结果的结构化重用，显著扩展了模型超越单步生成的问题解决能力。

为了进一步增强鲁棒性，我们还集成了一个**错误修复机制**，该机制能够解释 Lean 的错误信息并提出针对性的修正。这使得模型能够通过迭代反馈来优化其输出，从而提高证明的可靠性和整体样本效率。

#### 新的最先进水平

所提出技术的结合显著提升了形式定理证明的性能。在 miniF2F 基准测试中，Kimina-Prover 在 pass@32 下实现了 **84.0%** 的通过率，加上单轮错误修正后达到 **86.4%**。在 pass@1024 下，通过率达到 **87.7%**。应用完整的测试时强化学习（TTRL）搜索框架后，最终通过率达到 **92.2%**，估计的通过次数上限约为 42,000。然而，这个通过预算在未来版本中可以大幅优化，因为当前采样的很大一部分被用于证明无益或冗余的引理。

值得注意的是，这些结果表明了证明器扩展行为的变化。虽然早期版本在采样预算增加时，在对数尺度上表现出近似线性的改进，但当前系统在超过 pass@1024 后显示出收益递减。这表明进一步的提升较少依赖于增加采样，而更需要更复杂的搜索策略，例如 TTRL 所引入的策略。

# 方法论

### 启用引理模式

启用引理模式旨在使模型具备识别和利用输入中提供的有用引理的能力。为了支持这一能力，在强化学习（RL）训练期间，会将一到三个形式化引理的随机子集前置到问题上下文中，让证明器接触到可能有助于构建最终证明的中间结果。这些引理通过两步流程准备：（1）一个通用 LLM 用自然语言生成候选引理；（2）然后使用我们的 **Kimina-Autoformalizer-7b** 将这些引理翻译成形式化陈述。

初步观察显示，模型倾向于较少地利用提供的引理。为了解决这个问题，我们在 RL 框架内引入了一种基于偏好的奖励塑造策略。当一个定理可以通过多条轨迹证明时，成功利用所提供引理的解决方案会被分配更高的奖励，而未利用的则受到惩罚。这种方法被证明是有效的，在训练后将引理利用率提高到了稳定的 30-40%。重要的是，这种方法不仅鼓励了引理的使用，还促进了选择性：模型学会了在引理有用时策略性地应用它们，同时忽略不相关的引理，展现出更高效、更类人的推理行为。

## TTRL 搜索

![kimina-prover-ttrl-search-fixed-fixed](/images/posts/7dbbea1e71a4.png)

**启用引理模式**允许模型将预先生成的引理作为构建证明的中间步骤。然而，我们观察到，随机采样和插入引理不足以解决需要高度结构化且深度嵌套推理的复杂问题。为了解决这一限制，我们开发了**测试时强化学习搜索框架**——一种可训练的、智能体的方法，能够系统地组织、筛选和组合大量候选引理以构建完整的证明。该框架将过程从随机探索转变为更具策略性、目标导向的搜索。

如图2所示，我们将每个问题的**搜索范围**定义为问题本身及其相关的候选引理。TTRL搜索在每个搜索范围内追踪**引理利用分数**，以衡量每个引理对最终证明的贡献频率和效果。在每次RL训练迭代开始时，对于每个问题（即搜索范围），我们通过前置不同的引理组合来构建K = 10个输入变体。为了平衡探索与利用，**60%** 的输入使用排名靠前的引理（即利用分数最高的引理）构建，使模型专注于最有希望的证明路径。其余**40%** 的输入则由这些顶级引理加上一到四个随机选择的额外引理组成，以鼓励探索新颖且可能有用的引理组合。

为确保质量，一个**过滤机制**会剔除那些始终未能做出有意义贡献的引理：任何在50次插入尝试后仍未能达到至少τ=0.10利用分数的引理，都将从搜索池中移除。

TTRL的一个关键特性是其**递归搜索机制**。搜索范围不仅限于原始定理，也为每个引理单独维护，这使得框架能够递归地将问题分解为更小的子问题。一个并行的**子引理生成过程**贯穿始终，每当一个定理或引理在N = 128次尝试后仍未能找到证明，就会生成新的候选子引理。这种递归策略实现了推理深度的测试时扩展，显著提升了模型的有效问题解决能力。

为确保逻辑严谨性，我们处理了一种故障模式，即错误形式化的引理可能导致平凡或无效的证明。在这种情况下，模型可能利用不一致性来构建看似有效但实则不严谨的解决方案。为防止这种情况，我们引入了**否定证明过程**：对于每个新生成的引理，我们尝试证明其逻辑否定。如果被否定的陈述可被证明，则表明原始引理在逻辑上不一致，会立即被丢弃。这一步确保了整个证明构建过程的可靠性与严谨性。

## 在Kimina-Prover中实现错误修复

近期先进定理证明模型的一个关键局限是，它们缺乏基于证明助手反馈来修正证明的能力——而人类用户通常能利用这种能力。为弥补这一差距，我们开发了一个专用框架，将**错误修复能力**集成到Kimina-Prover中。

**用于错误纠正的SFT数据生成。** 通用大语言模型在解读Lean的错误信息并提出有效修正方面成功率很低。为克服这一点，我们构建了一个专门针对错误纠正的**监督微调（SFT）** 数据集。该数据集由（错误证明，Lean反馈，正确证明）形式的三元组构成。为了丰富监督信号，我们提示Claude 3.7 sonnet[8]合成逐步推理链，解释如何利用提供的反馈将错误证明转化为正确证明。最终得到一个高质量数据集，不仅包含初始和修正后的证明，还包含中间推理过程，从而促进更有效的学习。

**批量失败重放策略。** 最初，将错误纠正直接整合到强化学习（RL）循环中被证明效果不佳，因为SFT模型修复错误的成功率很低（约1%），导致奖励稀疏且训练不稳定。为解决此问题，我们设计了**批量失败重放**策略。我们不在RL迭代中立即尝试纠正错误，而是收集迭代N中所有失败的证明尝试。在随后的迭代N+1中，训练批次由这些先前失败的固定数量样本（例如500个）和提示集中的标准问题（例如另外500个）联合组成。这确保了在每个训练步骤中都能持续、大量地接触错误纠正任务，使模型能够以稳定且数据高效的方式逐步学习有效的错误处理行为。

这种训练方法使模型从失败中恢复的能力得到了可衡量的提升。模型从纠正基本语法错误，发展到解决复杂的逻辑错误，最终能在初始尝试失败时发现替代的证明策略。至关重要的是，这种能力提高了样本效率。如表2所示，我们在固定计算预算下比较了不同策略。16+16次尝试-修复策略——即16次初始证明尝试，每次后接一次错误修复尝试——取得了35.6%的成功率，优于32×1的暴力基线（通过32次独立尝试达到28.8%）。进一步将样本预算增加到32+32并配合错误纠正，成功率达到了44.1%。这些结果表明，让模型能够纠正自身错误，比重复试错更能高效利用计算资源。

## 其他改进

除了核心的TTRL搜索和错误修复，我们还开发了其他几项新技术，以增强模型的学习过程和问题解决能力。

**提示集筛选与迭代。** 有效的数据筛选对于强化学习（RL）效率至关重要。我们将初始超过30万个问题的提示集精炼为一个以竞赛为重点、约9万个问题的子集，重点关注来自NuminaMath 1.5[9]中**olympiads-ref**子集等来源的问题。在RL过程中，我们应用了**动态过滤**：持续高成功率的问题被移除以保持挑战性，而持续困难的问题则使用通用LLM分解为更简单的子问题或变体。最终的提示集结合了自动形式化的陈述（以实现广泛覆盖）、人工标注的问题（以保证质量）以及增强的变体（以进行针对性技能培养）。筛选后的提示集将开源。

**基于Lean数据的持续预训练。** 为解决大多数基础模型对Lean熟练度有限的问题，我们应用了**持续预训练（CPT）**。我们构建了一个包含60亿Token的CPT数据集，数据来源多样：包括来自GitHub等在线平台的2.6亿Token，来自我们RL流程中经编译器验证的rollout数据的55亿Token，以及额外的结构化数据（采用**状态-策略-状态**和**状态-策略-错误**格式）以增强多样性。这些结构化数据为基础模型补充了额外的领域知识。

**随机证明切割数据增强。** 为了更好地利用缺乏中间推理步骤的高质量人工标注证明，我们开发了**随机证明切割**技术。该方法通过两种变体来增强此类数据：

- 证明截断：移除证明的最后部分，模型必须完成它。
- 证明填充：随机选择一个内部块，用占位符Token`sorry`替换，模型必须重建缺失的步骤。

该策略使模型能够学习如何扩展现有的推理线并填补逻辑空白，从而有效地将人工生成的内容整合到训练过程中。

**非证明问题求解。** 许多问题以要求最终答案的形式呈现，这无法自然地框定为传统的证明任务。受CombiBench[10]评估方法的启发，我们引入了**非证明问题求解**能力，以统一答案生成与证明构建。在此设置下，模型会收到一个最终答案字段为空的问题。它在单次推理中执行两阶段过程：首先推导出正确答案，然后生成一个完整的形式化证明来论证该答案。这种方法确保模型的推理明确地以得出正确解决方案为条件。

# 证明案例示例

在此，我们提供一些由我们最新的Kimina-prover模型发现的证明案例。已解决的miniF2F问题完整列表可在GitHub上找到。

### TTRL搜索证明示例

该系统使用TTRL搜索方法，将问题递归分解为四层引理，最终生成了一个520行的形式化证明。在这个递归证明过程中，最初只有一个引理`sum_cexp_div_pow_ne_zero`有待解决。虽然这个结论的非形式化证明看起来很简单，但在Lean 4中严格证明它仍然需要很多步骤。我们的系统递归生成了额外的两层引理，并为`sum_cexp_div_pow_ne_zero`获得了一个260行的形式化证明。该证明在Mathlib v4.15下有效。

### 证明结构

![drawing](/images/posts/dd5e6469f78b.png)

### 形式化代码

```lean4
import Mathlib

open Finset in
theorem norm_le_sum_norm_of_sum_eq_zero {N : ℕ} (hN : N > 0) (z : ℕ → ℂ)
    (hsum : ∑ i ∈ range N, z i = 0) :
    ‖z 0‖ ≤ ∑ i ∈ Icc 1 (N - 1), ‖z i‖ := by
  by_cases h : N > 1
  ·
    have h6 : ∑ i in range N, z i = z 0 + ∑ i in Icc 1 (N - 1), z i := by
      have h10 : range N = {0} ∪ Icc 1 (N - 1) := by
        ext x
        simp
        omega
      rw [h10]
      rw [sum_union]
      ·
        simp
      ·
        apply disjoint_left.mpr
        intro x hx1 hx2
        simp at hx1
        simp [hx1] at hx2
    have h3 : z 0 = - (∑ i ∈ Icc 1 (N - 1), z i) := by
      have h4 : ∑ i in range N, z i = 0 := hsum
      rw [h6] at h4
      calc
        z 0 = (z 0 + ∑ i in Icc 1 (N - 1), z i) - ∑ i in Icc 1 (N - 1), z i := by ring
        _ = (0 : ℂ) - ∑ i in Icc 1 (N - 1), z i := by rw [h4]
        _ = - (∑ i in Icc 1 (N - 1), z i) := by ring
    have h11 : ‖z 0‖ = ‖(∑ i ∈ Icc 1 (N - 1), z i : ℂ)‖ := by
      rw [h3]
      simp [norm_neg]
    have h12 : ‖(∑ i ∈ Icc 1 (N - 1), z i : ℂ)‖ ≤ ∑ i ∈ Icc 1 (N - 1), ‖z i‖ := by
      apply norm_sum_le
    linarith [h11, h12]
  ·
    have h5 : N = 1 := by
      omega
    rw [h5]
    have h6 : ∑ i in range 1, z i = 0 := by
      have h7 : N = 1 := h5
      have h8 : ∑ i in range N, z i = 0 := hsum
      rw [show N = 1 by omega] at h8
      simpa using h8
    have h7 : z 0 = 0 := by
      simp at h6
      all_goals
        try tauto
    rw [show z 0 = (0 : ℂ) by exact h7]
    simp

open Finset in
theorem sum_pow_one_half_from_two_to_N {N : ℕ} (hN : 0 < N) :
    ∑ j ∈ Icc 1 (N - 1), (1 / 2 : ℝ) ^ (j + 1) = 1 / 2 - 1 / 2 ^ N := by
  have h2 : ∀ (k : ℕ), ∑ j in Icc 1 (k), (1 / 2 : ℝ) ^ (j + 1) = 1 / 2 - 1 / 2 ^ (k + 1 : ℕ) := by
    intro k
    induction k with
    | zero =>
      simp
    | succ k ihk =>
      rw [sum_Icc_succ_top (by linarith)]
      rw [ihk]
      field_simp at *
      ring_nf
  have h4 : ∑ j in Icc 1 (N - 1), (1 / 2 : ℝ) ^ (j + 1) = 1 / 2 - 1 / 2 ^ (N : ℕ) := by
    have h5 : ∑ j in Icc 1 (N - 1), (1 / 2 : ℝ) ^ (j + 1) = 1 / 2 - 1 / 2 ^ ((N - 1 : ℕ) + 1 : ℕ) := by
      apply h2 (N - 1)
    rw [h5]
    have h6 : (N - 1 : ℕ) + 1 = N := by
      omega
    rw [h6]
  exact h4

open Complex Finset in
theorem sum_eq_zero_of_sq_add_sq_eq_geom_seq_false {N : ℕ} (hN : 0 < N) (x y : Fin N → ℝ)
    (hxsum : ∑ i : Fin N, x i = 0) (hysum : ∑ i : Fin N, y i = 0)
    (hxy : ∀ j : Fin N, (x j)^2 + (y j)^2 = (1/4)^(j.1+1)) :
    False := by
  let z : ℕ → ℂ := fun i => if h : i < N then (x ⟨i, h⟩ : ℂ) + (y ⟨i, h⟩ : ℂ) * I else 0
  have hsumz : ∑ i in range N, z i = 0 := by
    have h4 : ∑ i in range N, z i = (∑ i : Fin N, ((x i : ℂ) + (y i : ℂ) * I)) := by
      simp [z, Finset.sum_fin_eq_sum_range, Finset.sum_congr]
    rw [h4]
    simp [Complex.ext_iff, Finset.sum_congr, hxsum, hysum]
  have hz0 : ‖z 0‖ ≤ ∑ i ∈ Icc 1 (N - 1), ‖z i‖ := norm_le_sum_norm_of_sum_eq_zero hN z hsumz
  have h2 : ‖z 0‖ = (1 / 2 : ℝ) := by
    have h6 : z 0 = (x ⟨0, by omega⟩ : ℂ) + (y ⟨0, by omega⟩ : ℂ) * I := by
      have h7 : (0 : ℕ) < N := by omega
      simp [z, h7]
    rw [h6]
    have h7 : ((x ⟨0, by omega⟩ : ℝ) ^ 2 + (y ⟨0, by omega⟩ : ℝ) ^ 2) = (1 / 4 : ℝ) := by
      have h8 := hxy (⟨0, by omega⟩)
      norm_num at h8 ⊢
      nlinarith
    have h8 : ‖((x ⟨0, by omega⟩ : ℂ) + (y ⟨0, by omega⟩ : ℂ) * I)‖ = Real.sqrt ((x ⟨0, by omega⟩ : ℝ) ^ 2 + (y ⟨0, by omega⟩ : ℝ) ^ 2) := by
      simp [Complex.norm_eq_abs, Complex.abs, Complex.normSq]
      all_goals
        ring_nf
    rw [h8, h7]
    have h9 : Real.sqrt ((1 / 4 : ℝ)) = (1 / 2 : ℝ) := by
      rw [Real.sqrt_eq_iff_mul_self_eq] <;> norm_num
    rw [h9]
  have h3 : ∑ i ∈ Icc 1 (N - 1), ‖z i‖ = ∑ i ∈ Icc 1 (N - 1), (1 / 2 : ℝ) ^ (i + 1 : ℕ) := by
    apply Finset.sum_congr
    .
      rfl
    .
      intro i hi
      have h10 : i ≥ 1 := by
        have h11 : i ∈ Icc (1 : ℕ) (N - 1) := by
          simpa using hi
        simp at h11 ⊢
        omega
      have h11 : i ≤ N - 1 := by
        have h12 : i ∈ Icc (1 : ℕ) (N - 1) := by
          simpa using hi
        simp at h12 ⊢
        omega
      have h12 : i < N := by
        omega
      have h13 : z i = (x ⟨i, by omega⟩ : ℂ) + (y ⟨i, by omega⟩ : ℂ) * I := by
        have h14 : i < N := by omega
        simp [z, h14]
      have h14 : ‖z i‖ = (1 / 2 : ℝ) ^ (i + 1 : ℕ) := by
        rw [h13]
        have h14 : ((x ⟨i, by omega⟩ : ℝ) ^ 2 + (y ⟨i, by omega⟩ : ℝ) ^ 2) = (1 / 4 : ℝ) ^ (i + 1 : ℕ) := by
          have h15 := hxy (⟨i, by omega⟩)
          norm_num at h15 ⊢
          nlinarith
        have h15 : ‖((x ⟨i, by omega⟩ : ℂ) + (y ⟨i, by omega⟩ : ℂ) * I)‖ = Real.sqrt ((x ⟨i, by omega⟩ : ℝ) ^ 2 + (y ⟨i, by omega⟩ : ℝ) ^ 2) := by
          simp [Complex.norm_eq_abs, Complex.abs, Complex.normSq]
          all_goals
            ring_nf
        rw [h15]
        have h16 : Real.sqrt ((x ⟨i, by omega⟩ : ℝ) ^ 2 + (y ⟨i, by omega⟩ : ℝ) ^ 2) = (1 / 2 : ℝ) ^ (i + 1 : ℕ) := by
          have h17 : ((x ⟨i, by omega⟩ : ℝ) ^ 2 + (y ⟨i, by omega⟩ : ℝ) ^ 2) = (1 / 4 : ℝ) ^ (i + 1 : ℕ) := h14
          rw [h17]
          have h18 : Real.sqrt ((1 / 4 : ℝ) ^ (i + 1 : ℕ)) = (1 / 2 : ℝ) ^ (i + 1 : ℕ) := by
            have h19 : ((1 / 4 : ℝ) : ℝ) = (1 / 2 : ℝ) ^ (2 : ℕ) := by norm_num
            rw [h19]
            have h20 : Real.sqrt (((1 / 2 : ℝ) ^ (2 : ℕ)) ^ (i + 1 : ℕ)) = (1 / 2 : ℝ) ^ (i + 1 : ℕ) := by
              have h21 : ((1 / 2 : ℝ) ^ (2 : ℕ)) ^ (i + 1 : ℕ) = ((1 / 2 : ℝ) ^ (i + 1 : ℕ)) ^ 2 := by
                have h22 : ((1 / 2 : ℝ) ^ (2 : ℕ)) ^ (i + 1 : ℕ) = (1 / 2 : ℝ) ^ (2 * (i + 1 : ℕ) : ℕ) := by
                  rw [← pow_mul]
                  all_goals ring_nf
                have h23 : ((1 / 2 : ℝ) ^ (i + 1 : ℕ)) ^ 2 = (1 / 2 : ℝ) ^ (2 * (i + 1 : ℕ) : ℕ) := by
                  ring_nf
                rw [h22, h23]
              rw [h21]
              have h22 : Real.sqrt (((1 / 2 : ℝ) ^ (i + 1 : ℕ)) ^ 2) = (1 / 2 : ℝ) ^ (i + 1 : ℕ) := by
                rw [Real.sqrt_sq (show (1 / 2 : ℝ) ^ (i + 1 : ℕ) ≥ 0 by positivity)]
              rw [h22]
            exact h20
          exact h18
        exact h16
      linarith
  rw [h3] at hz0
  rw [h2] at hz0
  have h6 : ∑ i ∈ Icc 1 (N - 1), (1 / 2 : ℝ) ^ (i + 1 : ℕ) = (1 / 2 - 1 / 2 ^ N : ℝ) := by
    have h7 : ∑ i ∈ Icc 1 (N - 1), (1 / 2 : ℝ) ^ (i + 1 : ℕ) = (1 / 2 - 1 / 2 ^ N : ℝ) := sum_pow_one_half_from_two_to_N hN
    linarith
  rw [h6] at hz0
  have h7 : (1 / 2 ^ N : ℝ) > 0 := by
    have h10 : (1 / 2 ^ N : ℝ) > 0 := by
      have h11 : (1 / 2 ^ N : ℝ) = (1 / 2 : ℝ) ^ N := by
        ring_nf
      rw [h11]
      positivity
    linarith
  have h11 : (1 / 2 - 1 / 2 ^ N : ℝ) < (1 / 2 : ℝ) := by
    have h12 : (1 / 2 ^ N : ℝ) > 0 := h7
    linarith
  linarith
```

```lean
open BigOperators Real Nat Topology Rat in
theorem sum_cexp_div_pow_ne_zero {N : ℕ} (hN : N > 0) (a : Fin N → ℝ) :
    ((∑ j : Fin N, cos (a j) / 2 ^ (j : ℕ))^2 +
     (∑ j : Fin N, sin (a j) / 2 ^ (j : ℕ))^2) > 0 := by
  by_contra h
  push_neg at h
  have h1 : (∑ j : Fin N, cos (a j) / 2 ^ (j : ℕ)) ^ 2 ≥ 0 := by
    apply sq_nonneg
  have h2 : (∑ j : Fin N, sin (a j) / 2 ^ (j : ℕ)) ^ 2 ≥ 0 := by
    apply sq_nonneg
  have h3 : (∑ j : Fin N, cos (a j) / 2 ^ (j : ℕ)) ^ 2 = 0 := by
    linarith
  have h4 : (∑ j : Fin N, sin (a j) / 2 ^ (j : ℕ)) ^ 2 = 0 := by
    linarith
  have h5 : (∑ j : Fin N, cos (a j) / 2 ^ (j : ℕ)) = 0 := by
    nlinarith
  have h6 : (∑ j : Fin N, sin (a j) / 2 ^ (j : ℕ)) = 0 := by
    nlinarith
  let x : Fin N → ℝ := fun j => cos (a j) / 2 ^ (j.1 + 1 : ℕ)
  let y : Fin N → ℝ := fun j => sin (a j) / 2 ^ (j.1 + 1 : ℕ)
  have hxsum : ∑ i : Fin N, x i = 0 := by
    have eq2 : ∑ i : Fin N, x i = (∑ i : Fin N, (cos (a i) / 2 ^ (i.1 : ℕ) : ℝ)) / 2 := by
      have eq3 : ∑ i : Fin N, x i = ∑ i : Fin N, (cos (a i) / 2 ^ (i.1 + 1 : ℕ) : ℝ) := by
        congr
      rw [eq3]
      have eq4 : ∑ i : Fin N, (cos (a i) / 2 ^ (i.1 + 1 : ℕ) : ℝ) = (∑ i : Fin N, (cos (a i) / 2 ^ (i.1 : ℕ) : ℝ)) / 2 := by
        calc
          ∑ i : Fin N, (cos (a i) / 2 ^ (i.1 + 1 : ℕ) : ℝ)
            = ∑ i : Fin N, ((cos (a i) / 2 ^ (i.1 : ℕ) : ℝ) / 2) := by
              apply Finset.sum_congr
              .
                rfl
              intro i hi
              have h12 : (cos (a i) / 2 ^ (i.1 + 1 : ℕ) : ℝ) = (cos (a i) / 2 ^ (i.1 : ℕ) : ℝ) / 2 := by
                have h11 : (2 : ℝ) ^ (i.1 + 1 : ℕ) = (2 : ℝ) ^ (i.1 : ℕ) * 2 := by
                  ring_nf
                rw [h11]
                field_simp
                all_goals ring
              exact h12
          _ = (∑ i : Fin N, (cos (a i) / 2 ^ (i.1 : ℕ) : ℝ)) / 2 := by
            simp [Finset.sum_div]
      exact eq4
    rw [eq2]
    rw [show ∑ i : Fin N, (cos (a i) / 2 ^ (i.1 : ℕ) : ℝ) = (0 : ℝ) by simpa using h5]
    all_goals norm_num
  have hysum : ∑ i : Fin N, y i = 0 := by
    have eq2 : ∑ i : Fin N, y i = (∑ i : Fin N, (sin (a i) / 2 ^ (i.1 : ℕ) : ℝ)) / 2 := by
      have eq3 : ∑ i : Fin N, y i = ∑ i : Fin N, (sin (a i) / 2 ^ (i.1 + 1 : ℕ) : ℝ) := by
        congr
      rw [eq3]
      have eq4 : ∑ i : Fin N, (sin (a i) / 2 ^ (i.1 + 1 : ℕ) : ℝ) = (∑ i : Fin N, (sin (a i) / 2 ^ (i.1 : ℕ) : ℝ)) / 2 := by
        calc
          ∑ i : Fin N, (sin (a i) / 2 ^ (i.1 + 1 : ℕ) : ℝ)
            = ∑ i : Fin N, ((sin (a i) / 2 ^ (i.1 : ℕ) : ℝ) / 2) := by
              apply Finset.sum_congr
              .
                rfl
              intro i hi
              have h12 : (sin (a i) / 2 ^ (i.1 + 1 : ℕ) : ℝ) = (sin (a i) / 2 ^ (i.1 : ℕ) : ℝ) / 2 := by
                have h11 : (2 : ℝ) ^ (i.1 + 1 : ℕ) = (2 : ℝ) ^ (i.1 : ℕ) * 2 := by
                  ring_nf
                rw [h11]
                field_simp
                all_goals ring
              exact h12
          _ = (∑ i : Fin N, (sin (a i) / 2 ^ (i.1 : ℕ) : ℝ)) / 2 := by
            simp [Finset.sum_div]
      exact eq4
    rw [eq2]
    rw [show ∑ i : Fin N, (sin (a i) / 2 ^ (i.1 : ℕ) : ℝ) = (0 : ℝ) by simpa using h6]
    all_goals norm_num
  have hxy : ∀ j : Fin N, (x j) ^ 2 + (y j) ^ 2 = (1 / 4 : ℝ) ^ (j.1 + 1 : ℕ) := by
    intro j
    have h11 : cos (a j) ^ 2 + sin (a j) ^ 2 = 1 := by
      exact Real.cos_sq_add_sin_sq (a j)
    simp [x, y]
    have h12 : (4 : ℝ) ^ (j.1 + 1 : ℕ) = (2 : ℝ) ^ (2 * (j.1 + 1 : ℕ)) := by
      have h13 : (4 : ℝ) = (2 : ℝ) ^ (2 : ℕ) := by norm_num
      rw [h13]
      rw [← pow_mul]
    have h13 : (2 : ℝ) ^ (2 * (j.1 + 1 : ℕ)) = ((2 : ℝ) ^ (j.1 + 1 : ℕ)) ^ 2 := by
      ring_nf
    field_simp [h11, h12, h13]
    all_goals
      ring_nf
  have h12 : False := sum_eq_zero_of_sq_add_sq_eq_geom_seq_false (show 0 < N by omega) x y hxsum hysum hxy
  tauto
```

```lean
open BigOperators Real Nat Topology Rat in
theorem mul_cos_sub_mul_sin_eq_mul_cos_add (C S : ℝ) (h : C ^ 2 + S ^ 2 ≠ 0) :
    ∃ R α : ℝ, R > 0 ∧ ∀ x : ℝ, C * cos x - S * sin x = R * cos (x + α) := by
  have h1 : C ^ 2 + S ^ 2 > 0 := by
    by_contra h2
    push_neg at h2
    have h3 : C ^ 2 ≥ 0 := sq_nonneg C
    have h4 : S ^ 2 ≥ 0 := sq_nonneg S
    have h5 : C ^ 2 + S ^ 2 = 0 := by nlinarith
    tauto
  have h2 : ∃ R : ℝ, R > 0 ∧ R ^ 2 = C ^ 2 + S ^ 2 := by
    use Real.sqrt (C ^ 2 + S ^ 2)
    constructor
    · -- 证明 sqrt (C^2 + S^2) > 0
      apply Real.sqrt_pos.mpr
      linarith
    · -- 证明 (sqrt (C^2 + S^2)) ^ 2 = C^2 + S^2
      rw [Real.sq_sqrt]
      positivity
  rcases h2 with ⟨R, hR_pos, hR_sq⟩
  have h12 : (C / R) ^ 2 + (S / R) ^ 2 = 1 := by
    have h14 : R ≠ 0 := by linarith
    have h15 : R ^ 2 = C ^ 2 + S ^ 2 := hR_sq
    field_simp at *
    nlinarith
  have h13 : ∃ α : ℝ, Real.cos α = C / R ∧ Real.sin α = S / R := by
    have h9 : (C / R) ^ 2 + (S / R) ^ 2 = 1 := h12
    by_cases hC : C ≥ 0
    · -- C ≥ 0 的情况
      use Real.arcsin (S / R)
      constructor
      · -- 证明 cos (arcsin (S / R)) = C / R
        have h14 : Real.cos (Real.arcsin (S / R)) = Real.sqrt (1 - (S / R) ^ 2) := by
          rw [Real.cos_arcsin]
        have h15 : Real.sqrt (1 - (S / R) ^ 2) = C / R := by
          have h151 : (C / R) ^ 2 = 1 - (S / R) ^ 2 := by
            linarith
          have h161 : Real.sqrt (1 - (S / R) ^ 2) = Real.sqrt ((C / R) ^ 2) := by
            rw [show 1 - (S / R) ^ 2 = (C / R) ^ 2 by linarith]
          rw [h161]
          have h171 : Real.sqrt ((C / R) ^ 2) = C / R := by
            apply Real.sqrt_sq (show 0 ≤ C / R by
              have h211 : R > 0 := hR_pos
              apply div_nonneg
              linarith
              linarith
            )
          rw [h171]
        rw [h14, h15]
      · -- 证明 sin (arcsin (S / R)) = S / R
        have h20 : -1 ≤ S / R := by
          have h6 : (S / R) ^ 2 ≤ 1 := by nlinarith [h9]
          nlinarith [sq_nonneg (S / R - 1), sq_nonneg (S / R + 1)]
        have h21 : S / R ≤ 1 := by
          have h6 : (S / R) ^ 2 ≤ 1 := by nlinarith [h9]
          nlinarith [sq_nonneg (S / R - 1), sq_nonneg (S / R + 1)]
        have h18 : Real.sin (Real.arcsin (S / R)) = S / R := by
          apply Real.sin_arcsin
          all_goals linarith
        rw [h18]
    · -- C < 0 的情况
      have hC2 : C < (0 : ℝ) := by linarith
      have hC3 : C / R < 0 := by
        have hR_pos1 : R > 0 := hR_pos
        apply div_neg_of_neg_of_pos hC2 (by linarith)
      use Real.pi - Real.arcsin (S / R)
      constructor
      · -- 证明 cos (π - arcsin (S / R)) = C / R
        have h28 : Real.cos (Real.pi - Real.arcsin (S / R)) = - Real.sqrt (1 - (S / R) ^ 2) := by
          have h1 : Real.cos (Real.pi - Real.arcsin (S / R)) = - Real.cos (Real.arcsin (S / R)) := by
            rw [Real.cos_pi_sub]
          have h2 : Real.cos (Real.arcsin (S / R)) = Real.sqrt (1 - (S / R) ^ 2) := by
            rw [Real.cos_arcsin]
          rw [h1, h2]
        have h29 : Real.sqrt (1 - (S / R) ^ 2) = - (C / R) := by
          have h301 : (C / R) ^ 2 = 1 - (S / R) ^ 2 := by
            linarith
          have h311 : Real.sqrt (1 - (S / R) ^ 2) = Real.sqrt ((C / R) ^ 2) := by
            rw [show 1 - (S / R) ^ 2 = (C / R) ^ 2 by linarith]
          rw [h311]
          have h321 : Real.sqrt ((C / R) ^ 2) = - (C / R) := by
            have h331 : C / R < 0 := hC3
            have : Real.sqrt ((C / R) ^ 2) = - (C / R) := by
              rw [Real.sqrt_sq_eq_abs]
              rw [abs_of_neg h331]
            linarith
          linarith
        rw [h28, h29]
        all_goals nlinarith
      · -- 证明 sin (π - arcsin (S / R)) = S / R
        have h30 : Real.sin (Real.pi - Real.arcsin (S / R)) = Real.sin (Real.arcsin (S / R)) := by
          rw [Real.sin_pi_sub]
        have h31 : Real.sin (Real.arcsin (S / R)) = S / R := by
          have h20 : -1 ≤ S / R := by
            have h6 : (S / R) ^ 2 ≤ 1 := by nlinarith [h9]
            nlinarith [sq_nonneg (S / R - 1), sq_nonneg (S / R + 1)]
          have h21 : S / R ≤ 1 := by
            have h6 : (S / R) ^ 2 ≤ 1 := by nlinarith [h9]
            nlinarith [sq_nonneg (S / R - 1), sq_nonneg (S / R + 1)]
          apply Real.sin_arcsin
          all_goals linarith
        rw [h30, h31]
  rcases h13 with ⟨α, h14, h15⟩
  use R, α
  constructor
  · -- 证明 R > 0
    linarith
  · -- 证明 ∀ x : ℝ, C * cos x - S * sin x = R * cos (x + α)
    intro x
    have h21 : Real.cos (x + α) = Real.cos x * Real.cos α - Real.sin x * Real.sin α := by
      rw [Real.cos_add]
    have h22 : Real.cos α = C / R := by
      linarith [h14]
    have h23 : Real.sin α = S / R := by
      linarith [h15]
    calc
      C * Real.cos x - S * Real.sin x
        = R * (Real.cos x * (C / R) - Real.sin x * (S / R)) := by
          field_simp [show R ≠ 0 by linarith]
          all_goals ring
      _ = R * (Real.cos x * Real.cos α - Real.sin x * Real.sin α) := by
        rw [show Real.cos α = C / R by linarith [h14], show Real.sin α = S / R by linarith [h15]]
      _ = R * Real.cos (x + α) := by
        rw [h21]
```

定理 sum_cos_div_two_pow_eq_mul_cos (N : ℕ) (a : ℕ → ℝ) (hN : N > 0) :
    ∃ R0 α : ℝ, R0 > 0 ∧ ∀ x : ℝ, ∑ j : Fin N, Real.cos (a j + x) / 2 ^ j.1 =
    (R0 : ℝ) * Real.cos (x + α) := by
  have h2 : ((∑ j : Fin N, Real.cos (a j) / 2 ^ (j : ℕ)) ^ 2 + (∑ j : Fin N, Real.sin (a j) / 2 ^ (j : ℕ)) ^ 2) > 0 := by
    apply sum_cexp_div_pow_ne_zero (by omega) (fun j : Fin N => a j)
  have h4 : (∑ j : Fin N, Real.cos (a j) / 2 ^ (j : ℕ)) ^ 2 + (∑ j : Fin N, Real.sin (a j) / 2 ^ (j : ℕ)) ^ 2 ≠ 0 := by
    linarith
  have h5 : ∃ R α : ℝ, R > 0 ∧ ∀ x : ℝ, (∑ j : Fin N, Real.cos (a j) / 2 ^ (j : ℕ)) * Real.cos x - (∑ j : Fin N, Real.sin (a j) / 2 ^ (j : ℕ)) * Real.sin x = R * Real.cos (x + α) := by
    apply mul_cos_sub_mul_sin_eq_mul_cos_add (∑ j : Fin N, Real.cos (a j) / 2 ^ (j : ℕ)) (∑ j : Fin N, Real.sin (a j) / 2 ^ (j : ℕ)) (by
      exact h4
    )
  rcases h5 with ⟨R0, α, hR0_pos, h_eq⟩
  use R0, α
  constructor
  .
    exact hR0_pos
  .
    intro x
    have h_eq2 : ∑ j : Fin N, Real.cos (a j + x) / 2 ^ j.1 = (∑ j : Fin N, Real.cos (a j) / 2 ^ (j : ℕ)) * Real.cos x - (∑ j : Fin N, Real.sin (a j) / 2 ^ (j : ℕ)) * Real.sin x := by
      have h8 : ∀ j : Fin N, Real.cos (a j + x) / (2 : ℝ) ^ (j : ℕ) = (Real.cos (a j) * Real.cos x - Real.sin (a j) * Real.sin x) / (2 : ℝ) ^ (j : ℕ) := by
        intro j
        have h9 : Real.cos (a j + x) = Real.cos (a j) * Real.cos x - Real.sin (a j) * Real.sin x := by
          rw [Real.cos_add]
        rw [h9]
      have h10 : ∑ j : Fin N, Real.cos (a j + x) / 2 ^ j.1 = ∑ j : Fin N, ((Real.cos (a j) * Real.cos x - Real.sin (a j) * Real.sin x) / (2 : ℝ) ^ (j : ℕ)) := by
        apply Finset.sum_congr
        .
          rfl
        .
          intro j hj
          have h9 : Real.cos (a j + x) / (2 : ℝ) ^ (j : ℕ) = (Real.cos (a j) * Real.cos x - Real.sin (a j) * Real.sin x) / (2 : ℝ) ^ (j : ℕ) := h8 j
          simpa using h9
      rw [h10]
      have h11 : ∑ j : Fin N, ((Real.cos (a j) * Real.cos x - Real.sin (a j) * Real.sin x) / (2 : ℝ) ^ (j : ℕ)) =
        (∑ j : Fin N, Real.cos (a j) / (2 : ℝ) ^ (j : ℕ)) * Real.cos x - (∑ j : Fin N, Real.sin (a j) / (2 : ℝ) ^ (j : ℕ)) * Real.sin x := by
        have h12 : ∀ j : Fin N, ((Real.cos (a j) * Real.cos x - Real.sin (a j) * Real.sin x) / (2 : ℝ) ^ (j : ℕ)) =
          (Real.cos (a j) / (2 : ℝ) ^ (j : ℕ)) * Real.cos x - (Real.sin (a j) / (2 : ℝ) ^ (j : ℕ)) * Real.sin x := by
          intro j
          ring_nf
        calc
          ∑ j : Fin N, ((Real.cos (a j) * Real.cos x - Real.sin (a j) * Real.sin x) / (2 : ℝ) ^ (j : ℕ))
            = ∑ j : Fin N, ((Real.cos (a j) / (2 : ℝ) ^ (j : ℕ)) * Real.cos x - (Real.sin (a j) / (2 : ℝ) ^ (j : ℕ)) * Real.sin x) := by
                apply Finset.sum_congr
                .
                  rfl
                .
                  intro j hj
                  specialize h12 j
                  linarith
          _ = (∑ j : Fin N, (Real.cos (a j) / (2 : ℝ) ^ (j : ℕ)) * Real.cos x) - (∑ j : Fin N, (Real.sin (a j) / (2 : ℝ) ^ (j : ℕ)) * Real.sin x) := by
              rw [Finset.sum_sub_distrib]
          _ = (∑ j : Fin N, Real.cos (a j) / (2 : ℝ) ^ (j : ℕ)) * Real.cos x - (∑ j : Fin N, Real.sin (a j) / (2 : ℝ) ^ (j : ℕ)) * Real.sin x := by
              rw [Finset.sum_mul, Finset.sum_mul]
      exact h11
    rw [h_eq2]
    specialize h_eq x
    linarith

open Real Set in
定理 sub_eq_int_mul_pi_of_cos_eq_zero :
    ∀ (θ₁ θ₂ : ℝ), cos θ₁ = 0 → cos θ₂ = 0 → ∃ m : ℤ, θ₂ - θ₁ = m * π := by
  intro θ₁ θ₂ h₁ h₂
  have h1 : ∃ k : ℤ, θ₁ = Real.pi / 2 + k * Real.pi := by
    rw [Real.cos_eq_zero_iff] at h₁
    rcases h₁ with ⟨k, hk⟩
    use k
    linarith
  rcases h1 with ⟨k, hk1⟩
  have h2 : ∃ l : ℤ, θ₂ = Real.pi / 2 + l * Real.pi := by
    rw [Real.cos_eq_zero_iff] at h₂
    rcases h₂ with ⟨l, hl⟩
    use l
    linarith
  rcases h2 with ⟨l, hl2⟩
  use l - k
  rw [hl2, hk1]
  field_simp at *
  <;> ring_nf <;> norm_num

open BigOperators Real Nat Topology Rat in
定理 imo_1969_p2 (m n : ℝ) (k : ℕ) (a : ℕ → ℝ) (y : ℝ → ℝ) (h₀ : 0 < k)
    (h₁ : ∀ x, y x = ∑ i in Finset.range k, Real.cos (a i + x) / 2 ^ i) (h₂ : y m = 0)
    (h₃ : y n = 0) : ∃ t : ℤ, m - n = t * Real.pi := by
  have h4 : y m = ∑ i in Finset.range k, Real.cos (a i + m) / 2 ^ i := by
    specialize h₁ m
    simpa using h₁
  have h5 : y n = ∑ i in Finset.range k, Real.cos (a i + n) / 2 ^ i := by
    specialize h₁ n
    simpa using h₁
  rw [h4] at h₂
  rw [h5] at h₃
  have h9 : ∃ R0 α : ℝ, R0 > 0 ∧ ∀ x : ℝ, ∑ j : Fin k, Real.cos (a j + x) / 2 ^ j.1 = R0 * Real.cos (x + α) := by
    apply sum_cos_div_two_pow_eq_mul_cos k (fun (j : ℕ) => a j) (by omega)
  rcases h9 with ⟨R0, α, hR0, h_eq3⟩
  have h10 : ∑ i in Finset.range k, Real.cos (a i + m) / 2 ^ i = R0 * Real.cos (m + α) := by
    have h11 : ∑ i in Finset.range k, Real.cos (a i + m) / 2 ^ i = ∑ j : Fin k, Real.cos (a j + m) / 2 ^ j.1 := by
      simp [Finset.sum_range]
    rw [h11]
    specialize h_eq3 m
    simpa using h_eq3
  have h11 : ∑ i in Finset.range k, Real.cos (a i + n) / 2 ^ i = R0 * Real.cos (n + α) := by
    have h12 : ∑ i in Finset.range k, Real.cos (a i + n) / 2 ^ i = ∑ j : Fin k, Real.cos (a j + n) / 2 ^ j.1 := by
      simp [Finset.sum_range]
    rw [h12]
    specialize h_eq3 n
    simpa using h_eq3
  have h10' : R0 * Real.cos (m + α) = 0 := by
    have h_eq10 : ∑ i in Finset.range k, Real.cos (a i + m) / 2 ^ i = 0 := by
      linarith [h₂, h10]
    linarith [h10, h_eq10]
  have h11' : R0 * Real.cos (n + α) = 0 := by
    have h_eq11 : ∑ i in Finset.range k, Real.cos (a i + n) / 2 ^ i = 0 := by
      linarith [h₃, h11]
    linarith [h11, h_eq11]
  have h12 : Real.cos (m + α) = 0 := by
    apply (mul_left_inj' (ne_of_gt hR0)).mp
    linarith
  have h13 : Real.cos (n + α) = 0 := by
    apply (mul_left_inj' (ne_of_gt hR0)).mp
    linarith
  have h14 : ∃ m1 : ℤ, (n + α) - (m + α) = m1 * Real.pi := by
    apply sub_eq_int_mul_pi_of_cos_eq_zero (m + α) (n + α) h12 h13
  rcases h14 with ⟨m1, hm1⟩
  use -m1
  have hm4 : (m : ℝ) - (n : ℝ) = - (m1 * Real.pi) := by
    have hm3 : (n + α : ℝ) - (m + α : ℝ) = (m1 : ℝ) * Real.pi := by
      linarith [hm1]
    nlinarith
  have hm5 : (-m1 : ℤ) * Real.pi = - (m1 * Real.pi) := by
    simp
  rw [hm5]
  linarith [hm4]

```

### 错误修复示例

在以下示例中，初始证明超时，因为直接对 `((Real.sqrt 3 / 2 : ℂ) + (1 / 2) * Complex.I) ^ 12` 应用 `simp` 导致了过高的搜索复杂度。通过分步计算中间幂次（如 $z^3$，然后 $z^6$，最后 $z^{12}$）来分解证明，显著减轻了编译器的计算负担。

## 错误修复前的证明

```lean4
import Mathlib

theorem algebra_299086 {z : ℂ} (hz : z = (Real.sqrt 3 / 2) + (1 / 2) * .I) : z ^ 2016 = 1 := by
  have h1 : z = (Real.sqrt 3 / 2) + (1 / 2) * Complex.I := hz
  -- 证明 z^12 = 1
  have h2 : z ^ 12 = 1 := by
    rw [h1]
    have h3 : ((Real.sqrt 3 / 2 : ℂ) + (1 / 2) * Complex.I) ^ 12 = 1 := by
      simp [pow_succ, pow_zero, Complex.ext_iff, Complex.I_mul_I, mul_add, add_mul, mul_comm, mul_assoc, pow_two, pow_three, pow_succ, Real.sqrt_sq]
      field_simp [Complex.ext_iff, mul_add, add_mul, pow_two, pow_three]
      <;> ring_nf <;> norm_num [Real.sqrt_sq] 
    exact h3
  calc
    z ^ 2016 = (z ^ 12) ^ 168 := by ring
    _ = 1 ^ 168 := by rw [h2]
    _ = 1 := by norm_num

```

## 错误信息

```
错误信息：
Lean 进程超时

```

## 错误修复后的证明

```lean4
import Mathlib

定理 algebra_299086 {z : ℂ} (hz : z = (Real.sqrt 3 / 2) + (1 / 2) * .I) : z ^ 2016 = 1 := by
  have h1 : z = (Real.sqrt 3 / 2) + (1 / 2) * Complex.I := by
    exact_mod_cast hz
  have h2 : z ^ 3 = Complex.I := by
    rw [h1]
    simp [pow_three, Complex.ext_iff, Complex.add_re, Complex.add_im, Complex.mul_re, Complex.mul_im, mul_add, add_mul, pow_two, mul_comm, mul_assoc]
    field_simp
    <;> ring_nf <;> norm_num
  have h3 : z ^ 6 = -1 := by
    calc
      z ^ 6 = (z ^ 3) ^ 2 := by ring
      _ = Complex.I ^ 2 := by rw [h2]
      _ = -1 := by simp [Complex.I_sq]
  have h4 : z ^ 12 = 1 := by
    calc
      z ^ 12 = (z ^ 6) ^ 2 := by ring
      _ = (-1) ^ 2 := by rw [h3]
      _ = 1 := by norm_num
  calc
    z ^ 2016 = (z ^ 12) ^ 168 := by
      ring_nf
    _ = (1) ^ 168 := by
      rw [h4]
    _ = 1 := by
      norm_num

```

# 引用

如果您想引用 Kimina-Prover，目前请随时参考我们的预览论文。完整的论文正在准备中，将很快发布。

```
@article{kimina_prover_2025,
    title = {Kimina-Prover Preview: Towards Large Formal Reasoning Models with Reinforcement Learning},
    author = {Wang, Haiming and Unsal, Mert and Lin, Xiaohan and Baksys, Mantas and Liu, Junqi and Santos, Marco Dos and Sung, Flood and Vinyes, Marina and Ying, Zhenzhe and Zhu, Zekai and Lu, Jianqiao and Saxcé, Hugues de and Bailey, Bolton and Song, Chendong and Xiao, Chenjun and Zhang, Dehao and Zhang, Ebony and Pu, Frederick and Zhu, Han and Liu, Jiawei and Bayer, Jonas and Michel, Julien and Yu, Longhui and Dreyfus-Schmidt, Léo and Tunstall, Lewis and Pagani, Luigi and Machado, Moreira and Bourigault, Pauline and Wang, Ran and Polu, Stanislas and Barroyer, Thibaut and Li, Wen-Ding and Niu, Yazhe and Fleureau, Yann and Hu, Yangyang and Yu, Zhouliang and Wang, Zihan and Yang, Zhilin and Liu, Zhengying and Li, Jia},
    year = {2025},
    url = {http://arxiv.org/abs/2504.11354},
}

```

# 参考文献

[1]Team, Kimi, et al. "Kimi k1. 5: Scaling reinforcement learning with llms." arXiv preprint arXiv:2501.12599 (2025).

[2]Qwen, et al. "Qwen2.5 Technical Report" arXiv preprint arXiv:2412.15115 (2024).

[3]Yang, An, et al. "Qwen3 technical report." arXiv preprint arXiv:2505.09388 (2025).

[4]https://deepmind.google/discover/blog/ai-solves-imo-problems-at-silver-medal-level/

[5]Ren, Z. Z., et al. "Deepseek-prover-v2: Advancing formal mathematical reasoning via reinforcement learning for subgoal decomposition." arXiv preprint arXiv:2504.21801 (2025).

[6]Cao, Chenrui, et al. "Reviving DSP for Advanced Theorem Proving in the Era of Reasoning Models." arXiv preprint arXiv:2506.11487 (2025).

[7]Wang, Haiming, et al. "Kimina-prover preview: Towards large formal reasoning models with reinforcement learning." arXiv preprint arXiv:2504.11354 (2025).

[8]https://assets.anthropic.com/m/785e231869ea8b3b/original/claude-3-7-sonnet-system-card.pdf

[9]Li, Jia, et al. "Numinamath: The largest public dataset in ai4maths with 860k pairs of competition math problems and solutions." Hugging Face repository 13 (2024): 9.

[10]Liu, Junqi, et al. "CombiBench: Benchmarking LLM capability for combinatorial mathematics." arXiv preprint arXiv:2505.03171 (2025).

---

> 本文由AI自动翻译，原文链接：[Kimina-Prover: Applying Test-time RL Search on Large Formal Reasoning Models](https://huggingface.co/blog/AI-MO/kimina-prover)
> 
> 翻译时间：2026-03-13 05:00
