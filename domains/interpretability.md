# Interpretability

Circuits, superposition/SAEs, tracing, probing, causal abstraction, SLT, representation engineering, tooling.

**5 live/paywalled entries** · catalog domain id: `interpretability`

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

## Deep

Formal treatments, frontier research, and specialized material.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Against Almost Every Theory of Impact of Interpretability](https://www.alignmentforum.org/posts/LNA8mubrByG7SFacm/against-almost-every-theory-of-impact-of-interpretability-1) (Charbel-Raphaël, 2023) | essay | deep | A Comprehensive Mechanistic Interpretability Explainer & Glossary | The most-cited critique of interpretability's safety value; forces the field to articulate concrete, non-enumerative mechanisms by which interpretability could matter. |
