---
title: Magnetar brings faster, simpler, quantum-ready zero-knowledge proofs
title_original: Magnetar brings faster, simpler, quantum-ready zero-knowledge proofs
date: '2026-10-15'
source: Microsoft Research
source_url: https://www.microsoft.com/en-us/research/blog/proof-based-general-purpose-computing-with-magnetar/
author: ''
summary: '[翻译失败，原文如下]


  ![Magnetar proves a program''s execution and returns a small proof that anyone can
  check, with security resting only on standard hash func...'
categories:
- 未分类
tags: []
draft: false
translated_at: '2026-10-16T06:40:32.049474'
---

[翻译失败，原文如下]

![Magnetar proves a program's execution and returns a small proof that anyone can check, with security resting only on standard hash functions.](/images/posts/6542fcf2e79f.jpg)

## At a glance

- A new form of computing. Zero-knowledge proofs let you run a workload and receive, alongside the result, a short proof that the program ran correctly. Anyone can check the proof in milliseconds, without rerunning the program, without trusting whoever ran it, and without needing data on which the program was run.
- Three grand challenges have stood in the way of broad adoption: making proofs fast enough to produce, making them available to normal programs without cryptographic expertise, and resting them on cryptography that will still be trusted many decades from now.
- Magnetar makes major progress on all three challenges.It proves programs written in Rust, Go, or C, runs 10 to 39 times faster on average than the prior fastest comparable systems, and rests its security only on standard hash functions. It is the latest result of more than a decade of research at Microsoft Research on making zero-knowledge proofs practical.

## A new form of computing

Every result a computer produces comes with an implicit question: did the program run as claimed and produce correct outputs? Today, answering that question often requires a degree of trust alongside verification. We trust the operator, the vendor, the counterparty, or the agent, and we rely on contracts, audits, and logs to establish that trust.

Zero-knowledge proofs offer a fundamentally different approach to establishing trust. A program runs, and along with its output it produces a short proof, a cryptographic certificate that this program, on these inputs, produced this output. The proof is small and fast to check. Whoever receives it can confirm the result in milliseconds without rerunning the program, and can pass the proof on to anyone else who needs the same assurance. With the zero-knowledge property, the proof also reveals nothing about inputs that should stay private.

This changes what correctness means in the real world. A result no longer has to be trusted because of who produced it. It can be checked because of what accompanies it. An AI agent acting on someone’s behalf could attach a proof that each action complied with the policy it was given. Regulated financial institutions could prove that transactions were processed correctly without making their transactions public. These become possible once producing a proof is as routine as running the program.

## Three grand challenges

Zero-knowledge proofs were invented in the 1980s, and the ideas behind proving program execution have been around nearly as long. What has kept them from becoming a general tool is three challenges that have resisted being solved at the same time.

Efficiency. Producing a proof has historically taken millions of times more computation than running the program itself. Years of research have brought that overhead down, but the fastest systems have achieved their speed by making compromises elsewhere.

Generality and usability.Many proof systems require developers to manually rewrite their program as a cryptographic circuit, which is a fixed arithmetic description of that exact computation. This takes months. Every change to the application means a new circuit, and the translation is itself a frequent source of security bugs. A general-purpose alternative is to prove the execution of an ordinary processor, so that any compiled program can be proven as written. Until recently, that generality came at a steep cost in speed or security.

Security.A proof is only as strong as the cryptography beneath it. Many proof systems rest on elliptic curves, which can be broken by a sufficiently powerful quantum computer. Microsoft is addressing this problem with its Quantum Safe Program, which will move its products and services to post-quantum cryptography, a goal itrecently accelerated to 2029. Post-quantum proof systems already exist, but some rest on lattice assumptions, and most rest on new cryptographic functions invented to reduce the cost of proving. These new cryptographic functions have not faced the decades of scrutiny given to the cryptography protecting today’s internet, and some rest on mathematical conjectures about error-correcting codes that have not been proven. They have bought their speed with strong assumptions.

![Microsoft Research at BUILD 2026 | abstract pattern on a purple background](/images/posts/921376f45eb1.jpg)

## Microsoft Research at BUILD 2026

Giving developers a hands-on look at some of the many AI-based models and tools they can use to accelerate innovation, enhance their capabilities, and quickly transform ideas into prototypes.

## More than a decade of work

For more than a decade, Microsoft Research has worked on making zero-knowledge proofs and verifiable computing practical. Early research followed two approaches, both practical only for small programs.The first(opens in new tab)(opens in new tab)lets a verifier check a long computation through a short conversation with the prover using a technique calledthe sum-check protocol(opens in new tab), but this applied only to computations with a particular layered structure.The second(opens in new tab)(opens in new tab)used elliptic-curve cryptography to create very small proofs for almost any computation. But this requires a one-time trusted setup involving secret information which, if leaked, could allow anyone to forge proofs. This approach is also vulnerable to quantum computers.

In 2019, a new zero-knowledge proof system calledSpartanreturned to the sum-check approach and made it work for general-purpose programs without a trusted setup. Spartan can also be instantiated with different cryptographic building blocks. That flexibility is what later allowed the proof system to be built on hash functions alone. A sequence of results then filled in the remaining pieces:

- Phalanx(opens in new tab), in 2021, showed how to exploit repetition, such as a processor running the same instruction cycle on every step, to prove computations an order of magnitude faster than Spartan. Magnetar’s processor description is built on this idea.
- Nova(opens in new tab),HyperNova(opens in new tab),NeutronNova(opens in new tab),Neo and SuperNeo(opens in new tab)showed that stopping Spartan’s proving early, and folding the partial results together, makes it practical to prove computations of any size at far lower cost.
- Brakedown(opens in new tab), in 2021, introduced a fast hash-based commitment scheme and combined it with Spartan, giving the first Spartan variant whose security rests on standard hash functions.
- Spice(opens in new tab),Lasso(opens in new tab),Nebula(opens in new tab), and thenTwist and Shout(opens in new tab)made the memory operations at the heart of a general-purpose processor inexpensive to prove, andJolt(opens in new tab)showed that combining them with Spartan can efficiently prove the execution of a complete processor.
- Earlier this year,Vega(opens in new tab)applied this line of work to digital identity, proving facts from a government credential inunder a tenth of a second.
- More recently,BinarySpartan(opens in new tab)brought Spartan to binary fields, where a processor’s logic and standard hash functions can be efficiently expressed. BinarySpartan also relies onLigerito(opens in new tab), a Brakedown-style commitment scheme with much shorter proofs, and onring switching(opens in new tab), which makes it efficient to commit to vectors of bits.

Each of these solved a piece of the problem. Magnetar is where the pieces come together.

## Magnetar

Magnetaris a zero-knowledge virtual machine, or zkVM, and it makes major progress on all three challenges at once.

[翻译失败，原文如下]

![Figure 1. Magnetar proves a program’s execution and returns a small proof that anyone can check, with security resting only on standard hash functions.](/images/posts/71208349c380.png)

It is general-purpose.Magnetar proves the execution of RISC-V, an open processor architecture with mature compilers for every mainstream language. A developer writes a program in Rust, Go, or C, compiles it as usual, and Magnetar proves it as written. Consider what this means in practice. A business policy, a data pipeline, or an interpreter for the Ethereum Virtual Machine (EVM) is just a program, and the engineers who already maintain it can prove their executions exactly as written. As a result, proving stops being a specialist activity.

It is faster than prior systems in the same class.Magnetar proves 7.2 to 8.7 million processor instructions per second on a laptop. Across 15 benchmark programs, from cryptographic hashing to token transfers inside a small EVM interpreter, it is 10 to 39 times faster on average than the fastest existing zkVMs on the same machine, and more than 300 times faster than two others on a token-transfer benchmark. An optimized Magnetar proves 9.5–12.8 million cycles per second, which increases each speedup reported here by about 1.3×. Its proofs verify in about 12 milliseconds.

Its security rests on standard cryptography.Magnetar depends on a standard hash function such as SHA-256 or SHA-3, the same primitives that already protect every organization’s systems. It requires no elliptic curves, no lattices, no special-purpose hash functions, no trusted setup, and no unproven conjecture about error-correcting codes. Hash functions are the most thoroughly studied primitives in the cryptographic toolkit, and they are the basis of the stateless hash-based signatures that NIST standardized as its own conservative post-quantum option. For a system that must still be trustworthy in many decades to come, relying only on standard hash functions removes a cryptographic migration from the roadmap.

The same design decision pays a second dividend. Checking a Magnetar proof consists mostly of evaluating standard hash functions and binary-field arithmetic, which are exactly the operations Magnetar proves efficiently. Verifying a proof is therefore an ordinary workload for it. This is what allows Magnetar to prove computations of any size, by proving them in pieces and then combining the pieces. This also allows Magnetar to prove a long-running system such as a ledger or a blockchain.

Thetechnical papergives the full design, security analysis, and measurements.

## Looking ahead

Magnetar advances zero-knowledge proofs and verifiable computing to a stage where they can be built on the cryptography that organizations already trust, at speeds that make it usable, by engineers who write normal code. Magnetar enables a future where cryptographic proofs are a routine output of computation. We expect that technology leaders will stop askingwhether proofs of execution are practicaland focus instead onwhich resultswouldthey prefer to verify rather than taking on trust.

If you’re interested in exploring how zero-knowledge proofs can support your use case, we’d love tohear from you(opens in new tab).

## Meet the authors

### Srinath Setty

Senior Principal Researcher and Manager

---

> 本文由AI自动翻译，原文链接：[Magnetar brings faster, simpler, quantum-ready zero-knowledge proofs](https://www.microsoft.com/en-us/research/blog/proof-based-general-purpose-computing-with-magnetar/)
> 
> 翻译时间：2026-10-16 06:40
