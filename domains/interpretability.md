# Interpretability

Circuits, superposition/SAEs, tracing, probing, causal abstraction, SLT, representation engineering, tooling.

**22 live/paywalled entries** · catalog domain id: `interpretability`

> Generated from `data/entries.json` — do not edit by hand. Run `python scripts/generate_domains.py`.

## Entry tier

No prerequisites beyond the domain's stated baseline.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Zoom In: An Introduction to Circuits](https://distill.pub/2020/circuits/zoom-in) (Chris Olah, Nick Cammarata, Ludwig Schubert et al., 2020) | essay | entry | — | The founding statement of the circuits paradigm that mechanistic interpretability builds on, defining the research question of decomposing networks into understandable units. |
| [A Comprehensive Mechanistic Interpretability Explainer & Glossary](https://www.lesswrong.com/posts/vnocLyeWXcAxtdDnP/a-comprehensive-mechanistic-interpretability-explainer-and) (Neel Nanda, 2022) | essay | entry | — | The community-canonical orientation text for newcomers; its conceptual framing and vocabulary are the de facto standard for how the field talks about circuits. |
| [How to use and interpret activation patching](https://arxiv.org/abs/2404.15255) (Stefan Heimersheim, Neel Nanda, 2024) | paper | entry | A Comprehensive Mechanistic Interpretability Explainer & Glossary | The most accessible introduction to patching methodology, widely used as the entry point for new interpretability researchers. |

## Core

The load-bearing literature of the subfield.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Interpretability Beyond Feature Attribution: Quantitative Testing with Concept Activation Vectors (TCAV)](https://arxiv.org/abs/1711.11279) (Been Kim, Martin Wattenberg, Justin Gilmer et al., 2018) | paper | core | — | A foundational method for concept-level probing of what internal representations encode, influential across the later linear-probing and representation analysis literature. |
| [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html) (Nelson Elhage, Neel Nanda, Catherine Olsson et al., 2021) | paper | core | Zoom In: An Introduction to Circuits | The canonical formalism for analyzing transformers mechanistically; nearly all subsequent circuit analysis (induction heads, SAE-based tracing) uses its residual-stream and QK/OV vocabulary. |
| [Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task](https://arxiv.org/abs/2210.13382) (Kenneth Li, Aspen K. Hopkins, David Bau et al., 2022) | paper | core | — | The canonical demonstration that models can learn genuine internal world models, and a milestone for probing methodology: probes plus interventions established the representation was causal. |
| [In-context Learning and Induction Heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html) (Catherine Olsson, Nelson Elhage, Neel Nanda et al., 2022) | paper | core | A Mathematical Framework for Transformer Circuits | A landmark demonstration that a general capability (in-context learning) can be traced to a specific, nameable circuit — the template for capability-level mechanistic explanation. |
| [Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small](https://arxiv.org/abs/2211.00593) (Kevin Wang, Alexandre Variengien, Arthur Conmy et al., 2022) | paper | core | A Mathematical Framework for Transformer Circuits, In-context Learning and Induction Heads | The flagship demonstration that full circuit-level explanation of a real model behavior is possible, and the paper whose methodology (path patching, head classes) defined subsequent tracing work. |
| [Toy Models of Superposition](https://arxiv.org/abs/2209.10652) (Nelson Elhage, Tristan Hume, Catherine Olsson et al., 2022) | paper | core | A Mathematical Framework for Transformer Circuits | The theoretical foundation for why dictionary learning is needed: superposition explains polysemanticity, and sparse autoencoders are the field's main attempt to disentangle the superposed features. |
| [Sparse Autoencoders Find Highly Interpretable Features in Language Models](https://arxiv.org/abs/2309.08600) (Hoagy Cunningham, Aidan Ewart, Logan Riggs et al., 2023) | paper | core | Towards Monosemanticity: Decomposing Language Models With Dictionary Learning | Brought SAEs into the mainstream as a practical tool with rigorous evaluation, showing feature-level interventions genuinely affect model outputs. |
| [Towards Monosemanticity: Decomposing Language Models With Dictionary Learning](https://transformer-circuits.pub/2023/monosemantic-features/) (Trenton Bricken, Adly Templeton, Joshua Batson et al., 2023) | paper | core | Toy Models of Superposition | The first convincing demonstration that dictionary learning resolves superposition in real language models, launching the SAE research program that dominates interpretability from 2023 on. |

## Deep

Formal treatments, frontier research, and specialized material.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Probing Classifiers: Promises, Shortcomings, and Advances](https://arxiv.org/abs/2102.12452) (Yonatan Belinkov, 2021) | paper | deep | Interpretability Beyond Feature Attribution: Quantitative Testing with Concept Activation Vectors (TCAV) | The authoritative statement of probing's methodological limitations — the paper every probing result is measured against, and the reason probe findings require causal confirmation. |
| [Against Almost Every Theory of Impact of Interpretability](https://www.alignmentforum.org/posts/LNA8mubrByG7SFacm/against-almost-every-theory-of-impact-of-interpretability-1) (Charbel-Raphaël, 2023) | essay | deep | A Comprehensive Mechanistic Interpretability Explainer & Glossary | The most-cited critique of interpretability's safety value; forces the field to articulate concrete, non-enumerative mechanisms by which interpretability could matter. |
| [Attribution Patching Outperforms Automated Circuit Discovery](https://arxiv.org/abs/2310.10348) (Aaquib Syed, Can Rager, Arthur Conmy, 2023) | paper | deep | Towards Automated Circuit Discovery for Mechanistic Interpretability | Resolved the early 'how do we find circuits' question in favor of cheap gradient-based attribution, shaping the standard pipeline for automated circuit discovery. |
| [Towards Automated Circuit Discovery for Mechanistic Interpretability](https://arxiv.org/abs/2304.14997) (Arthur Conmy, Augustine N. Mavor-Parker, Aengus Lynch et al., 2023) | paper | deep | Towards Best Practices of Activation Patching in Language Models: Metrics and Methods | The first systematic automated circuit discovery method, opening the path from hand-crafted circuit analysis to scalable, algorithmic circuit finding. |
| [Towards Best Practices of Activation Patching in Language Models: Metrics and Methods](https://arxiv.org/abs/2309.16042) (Fred Zhang, Neel Nanda, 2023) | paper | deep | Interpretability in the Wild: a Circuit for Indirect Object Identification in GPT-2 small | The methodological standard for activation patching; established that patching results are only meaningful when the experimental protocol is specified and validated. |
| [Finding Neurons in a Haystack: Case Studies with Sparse Probing](https://arxiv.org/abs/2305.01610) (Wes Gurnee, Neel Nanda, Matthew Pauly et al., 2023) | paper | deep | Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task | Bridged probing and circuit analysis by localizing concepts to specific neurons, and its finding that sparsity grows with scale bears directly on how far SAE-style decomposition can go. |
| [Language Models Represent Space and Time](https://arxiv.org/abs/2310.02207) (Wes Gurnee, Max Tegmark, 2023) | paper | deep | Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task | A landmark positive probing result showing that frontier LLMs encode structured, human-interpretable world geometry linearly, informing the linear representation hypothesis debates. |
| [AtP*: An efficient and scalable method for localizing LLM behaviour to components](https://arxiv.org/abs/2403.00745) (János Kramár, Tom Lieberum, Rohin Shah et al., 2024) | paper | deep | Towards Best Practices of Activation Patching in Language Models: Metrics and Methods | Scaled circuit localization to production-scale models; the technique behind Google DeepMind's internal interpretability work on LLM component attribution. |
| [Do Sparse Autoencoders Find "True Features"?](https://www.lesswrong.com/posts/QoR8noAB3Mp2KBA4B/do-sparse-autoencoders-find-true-features) (Demian Till, 2024) | essay | deep | Sparse Autoencoders Find Highly Interpretable Features in Language Models | A central epistemic critique of SAE-based interpretability, raising the question of what SAE features actually are before safety conclusions are drawn from them. |
| [Scaling and evaluating sparse autoencoders](https://arxiv.org/abs/2406.04093) (Leo Gao, Tom Dupré la Tour, Henk Tillman et al., 2024) | paper | deep | Sparse Autoencoders Find Highly Interpretable Features in Language Models | The reference work for how to train and evaluate SAEs at scale, including the dead-latent problem and its solutions that community tooling now standardizes on. |
| [Scaling Monosemanticity: Extracting Interpretable Features from Claude 3 Sonnet](https://transformer-circuits.pub/2024/scaling-monosemanticity/) (Adly Templeton, Tom Conerly, Jonathan Marcus et al., 2024) | paper | deep | Towards Monosemanticity: Decomposing Language Models With Dictionary Learning | Proof that SAE-based interpretability scales to frontier models, and the clearest public demonstration of safety-relevant features being extractable from a production system. |
