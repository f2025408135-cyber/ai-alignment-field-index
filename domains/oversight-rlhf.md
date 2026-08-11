# Scalable Oversight & RLHF

RLHF and its failure modes, constitutional AI, debate, amplification, weak-to-strong, reward hacking.

**16 live/paywalled entries** · catalog domain id: `oversight-rlhf`

> Generated from `data/entries.json` — do not edit by hand. Run `python scripts/generate_domains.py`.

## Entry tier

No prerequisites beyond the domain's stated baseline.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Claude's Constitution](https://www.anthropic.com/constitution) (Anthropic, 2023) | essay | entry | — | The public artifact that makes the constitutional approach concrete and auditable, and a living example of how a lab codifies value priorities. |

## Core

The load-bearing literature of the subfield.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Deep reinforcement learning from human preferences](https://arxiv.org/abs/1706.03741) (Paul Christiano, Jan Leike, Tom B. Brown et al., 2017) | paper | core | — | Established the human-preferences-to-reward-model pipeline that all of RLHF descends from, and showed alignment-style supervision can train complex behavior without an explicit reward. |
| [AI safety via debate](https://arxiv.org/abs/1805.00899) (Geoffrey Irving, Paul Christiano, Dario Amodei, 2018) | paper | core | — | One of the founding scalable oversight proposals: the idea that competition between agents can amplify a weak judge's ability to supervise superhuman tasks. |
| [Factored Cognition](https://www.alignmentforum.org/posts/DFkGStzvj3jgXibFG/factored-cognition) (Andreas Stuhlmüller, 2018) | essay | core | — | Provides the theoretical framing that both debate and iterated amplification rely on, and motivates the 'supervise the process, not the outcome' intuition in scalable oversight. |
| [Fine-Tuning Language Models from Human Preferences](https://arxiv.org/abs/1909.08593) (Daniel M. Ziegler, Nisan Stiennon, Jeffrey Wu et al., 2019) | paper | core | Deep reinforcement learning from human preferences | The bridge that took RLHF from games to language models, demonstrating that preference optimization works on text generation and setting the template for later instruction-tuning work. |
| [Learning to summarize from human feedback](https://arxiv.org/abs/2009.01325) (Nisan Stiennon, Long Ouyang, Jeff Wu et al., 2020) | paper | core | Fine-Tuning Language Models from Human Preferences | The definitive early demonstration that RLHF produces outputs humans prefer over expert-written text, and an early documented case of reward model overoptimization. |
| [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) (Yuntao Bai, Saurav Kadavath, Sandipan Kundu et al., 2022) | paper | core | Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback | The flagship demonstration of AI-supervised alignment, showing harmlessness can be scaled without per-example human safety labels, and the basis of Claude's training pipeline. |
| [Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback](https://arxiv.org/abs/2204.05862) (Yuntao Bai, Andy Jones, Kamal Ndousse et al., 2022) | paper | core | Training language models to follow instructions with human feedback | The reference for how safety-relevant RLHF was done at scale, including the HHH framing that defined the safety target for assistant alignment and the tension between helpfulness and harmlessness. |
| [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) (Long Ouyang, Jeff Wu, Xu Jiang et al., 2022) | paper | core | Learning to summarize from human feedback | The recipe every commercial assistant training pipeline follows, and the paper that made RLHF the default alignment method for production language models. |
| [Discovering Language Model Behaviors with Model-Written Evaluations](https://arxiv.org/abs/2212.09251) (Ethan Perez, Sam Ringer, Kamilė Lukošiūtė et al., 2022) | paper | core | Constitutional AI: Harmlessness from AI Feedback | Established the model-generated evaluation methodology that underlies modern behavioral evals, and documented that RLHF-style training can worsen some failure modes even as it fixes others. |

## Deep

Formal treatments, frontier research, and specialized material.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [The limits of AI safety via debate](https://www.alignmentforum.org/posts/kguLeJTt6LnGuYX4E/the-limits-of-ai-safety-via-debate) (Marius Hobbhahn, 2022) | essay | deep | AI safety via debate | The most cited alignment-community critique of debate, sharpening exactly which empirical claims debate's viability rests on. |
| [Scaling Laws for Reward Model Overoptimization](https://arxiv.org/abs/2210.10760) (Leo Gao, John Schulman, Jacob Hilton, 2022) | paper | deep | Training language models to follow instructions with human feedback | Quantified Goodhart's law in RLHF and provided the scaling-law framework labs use to predict and control how much reward optimization is safe. |
| [Continuous Adversarial Quality Assurance: Extending RLHF and Constitutional AI](https://www.alignmentforum.org/posts/QGaioedKBJE39YJeD/continuous-adversarial-quality-assurance-extending-rlhf-and) (Benaya Koren, 2023) | essay | deep | Constitutional AI: Harmlessness from AI Feedback | The key alignment-community critique of Constitutional AI, identifying where the constitutional chain can silently corrupt and what would be needed to make it robust. |
| [Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325) (Yilun Du, Shuang Li, Antonio Torralba et al., 2023) | paper | deep | AI safety via debate | The main empirical instantiation of debate ideas on contemporary LLMs, showing cross-examination between models improves truthfulness even without a trained judge. |
| [RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback](https://arxiv.org/abs/2309.00267) (Harrison Lee, Samrat Phatale, Hassan Mansoor et al., 2023) | paper | deep | Constitutional AI: Harmlessness from AI Feedback | The controlled study that established AI feedback as a practical, cost-effective replacement for human labels, central to the scalable-oversight debate. |
| [Constitutional Classifiers: Defending against Universal Jailbreaks across Thousands of Hours of Red Teaming](https://arxiv.org/abs/2501.18837) (Mrinank Sharma, Meg Tong, Jesse Mu et al., 2025) | paper | deep | Constitutional AI: Harmlessness from AI Feedback | The most prominent large-scale application of the constitutional approach to defensive filtering, and the strongest public data point on whether such filters hold against determined attackers. |
