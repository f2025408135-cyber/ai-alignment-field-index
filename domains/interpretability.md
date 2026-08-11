# Interpretability

Circuits, superposition/SAEs, tracing, probing, causal abstraction, SLT, representation engineering, tooling.

**11 live/paywalled entries** · catalog domain id: `interpretability`

> Generated from `data/entries.json` — do not edit by hand. Run `python scripts/generate_domains.py`.

## Entry tier

No prerequisites beyond the domain's stated baseline.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Zoom In: An Introduction to Circuits](https://distill.pub/2020/circuits/zoom-in) (Chris Olah, Nick Cammarata, Ludwig Schubert et al., 2020) | essay | entry | — | The founding statement of the circuits paradigm that mechanistic interpretability builds on, defining the research question of decomposing networks into understandable units. |
| [A Comprehensive Mechanistic Interpretability Explainer & Glossary](https://www.lesswrong.com/posts/vnocLyeWXcAxtdDnP/a-comprehensive-mechanistic-interpretability-explainer-and) (Neel Nanda, 2022) | essay | entry | — | The community-canonical orientation text for newcomers; its conceptual framing and vocabulary are the de facto standard for how the field talks about circuits. |

## Core

The load-bearing literature of the subfield.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html) (Nelson Elhage, Neel Nanda, Catherine Olsson et al., 2021) | paper | core | Zoom In: An Introduction to Circuits | The canonical formalism for analyzing transformers mechanistically; nearly all subsequent circuit analysis (induction heads, SAE-based tracing) uses its residual-stream and QK/OV vocabulary. |
| [In-context Learning and Induction Heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html) (Catherine Olsson, Nelson Elhage, Neel Nanda et al., 2022) | paper | core | A Mathematical Framework for Transformer Circuits | A landmark demonstration that a general capability (in-context learning) can be traced to a specific, nameable circuit — the template for capability-level mechanistic explanation. |
| [Toy Models of Superposition](https://arxiv.org/abs/2209.10652) (Nelson Elhage, Tristan Hume, Catherine Olsson et al., 2022) | paper | core | A Mathematical Framework for Transformer Circuits | The theoretical foundation for why dictionary learning is needed: superposition explains polysemanticity, and sparse autoencoders are the field's main attempt to disentangle the superposed features. |
| [Sparse Autoencoders Find Highly Interpretable Features in Language Models](https://arxiv.org/abs/2309.08600) (Hoagy Cunningham, Aidan Ewart, Logan Riggs et al., 2023) | paper | core | Towards Monosemanticity: Decomposing Language Models With Dictionary Learning | Brought SAEs into the mainstream as a practical tool with rigorous evaluation, showing feature-level interventions genuinely affect model outputs. |
| [Towards Monosemanticity: Decomposing Language Models With Dictionary Learning](https://transformer-circuits.pub/2023/monosemantic-features/) (Trenton Bricken, Adly Templeton, Joshua Batson et al., 2023) | paper | core | Toy Models of Superposition | The first convincing demonstration that dictionary learning resolves superposition in real language models, launching the SAE research program that dominates interpretability from 2023 on. |

## Deep

Formal treatments, frontier research, and specialized material.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Against Almost Every Theory of Impact of Interpretability](https://www.alignmentforum.org/posts/LNA8mubrByG7SFacm/against-almost-every-theory-of-impact-of-interpretability-1) (Charbel-Raphaël, 2023) | essay | deep | A Comprehensive Mechanistic Interpretability Explainer & Glossary | The most-cited critique of interpretability's safety value; forces the field to articulate concrete, non-enumerative mechanisms by which interpretability could matter. |
| [Do Sparse Autoencoders Find "True Features"?](https://www.lesswrong.com/posts/QoR8noAB3Mp2KBA4B/do-sparse-autoencoders-find-true-features) (Demian Till, 2024) | essay | deep | Sparse Autoencoders Find Highly Interpretable Features in Language Models | A central epistemic critique of SAE-based interpretability, raising the question of what SAE features actually are before safety conclusions are drawn from them. |
| [Scaling and evaluating sparse autoencoders](https://arxiv.org/abs/2406.04093) (Leo Gao, Tom Dupré la Tour, Henk Tillman et al., 2024) | paper | deep | Sparse Autoencoders Find Highly Interpretable Features in Language Models | The reference work for how to train and evaluate SAEs at scale, including the dead-latent problem and its solutions that community tooling now standardizes on. |
| [Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet](https://transformer-circuits.pub/2024/scaling-monosemanticity/) (Adly Templeton, Tom Conerly, Jonathan Marcus et al., 2024) | paper | deep | Towards Monosemanticity: Decomposing Language Models With Dictionary Learning | Proof that SAE-based interpretability scales to frontier models, and the clearest public demonstration of safety-relevant features being extractable from a production system. |
