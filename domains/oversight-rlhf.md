# Scalable Oversight & RLHF

RLHF and its failure modes, constitutional AI, debate, amplification, weak-to-strong, reward hacking.

**6 live/paywalled entries** · catalog domain id: `oversight-rlhf`

> Generated from `data/entries.json` — do not edit by hand. Run `python scripts/generate_domains.py`.

## Entry tier

No prerequisites beyond the domain's stated baseline.

_No entries yet._

## Core

The load-bearing literature of the subfield.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Deep reinforcement learning from human preferences](https://arxiv.org/abs/1706.03741) (Paul Christiano, Jan Leike, Tom B. Brown et al., 2017) | paper | core | — | Established the human-preferences-to-reward-model pipeline that all of RLHF descends from, and showed alignment-style supervision can train complex behavior without an explicit reward. |
| [Fine-Tuning Language Models from Human Preferences](https://arxiv.org/abs/1909.08593) (Daniel M. Ziegler, Nisan Stiennon, Jeffrey Wu et al., 2019) | paper | core | Deep reinforcement learning from human preferences | The bridge that took RLHF from games to language models, demonstrating that preference optimization works on text generation and setting the template for later instruction-tuning work. |
| [Learning to summarize from human feedback](https://arxiv.org/abs/2009.01325) (Nisan Stiennon, Long Ouyang, Jeff Wu et al., 2020) | paper | core | Fine-Tuning Language Models from Human Preferences | The definitive early demonstration that RLHF produces outputs humans prefer over expert-written text, and an early documented case of reward model overoptimization. |
| [Training a Helpful and Harmless Assistant with Reinforcement Learning from Human Feedback](https://arxiv.org/abs/2204.05862) (Yuntao Bai, Andy Jones, Kamal Ndousse et al., 2022) | paper | core | Training language models to follow instructions with human feedback | The reference for how safety-relevant RLHF was done at scale, including the HHH framing that defined the safety target for assistant alignment and the tension between helpfulness and harmlessness. |
| [Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) (Long Ouyang, Jeff Wu, Xu Jiang et al., 2022) | paper | core | Learning to summarize from human feedback | The recipe every commercial assistant training pipeline follows, and the paper that made RLHF the default alignment method for production language models. |

## Deep

Formal treatments, frontier research, and specialized material.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Scaling Laws for Reward Model Overoptimization](https://arxiv.org/abs/2210.10760) (Leo Gao, John Schulman, Jacob Hilton, 2022) | paper | deep | Training language models to follow instructions with human feedback | Quantified Goodhart's law in RLHF and provided the scaling-law framework labs use to predict and control how much reward optimization is safe. |
