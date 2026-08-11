# Evals & Benchmarks

Dangerous capabilities, deception/scheming, autonomy, red-teaming suites, and eval critiques.

**19 live/paywalled entries** · catalog domain id: `evals-benchmarks`

> Generated from `data/entries.json` — do not edit by hand. Run `python scripts/generate_domains.py`.

## Entry tier

No prerequisites beyond the domain's stated baseline.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Anthropic's Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy) (Anthropic, 2023) | essay | entry | — | The first lab-scale policy that makes dangerous-capability evaluation the trigger for concrete safety commitments — the reference design for other labs' frontier safety policies. |
| [OpenAI's Approach to Frontier Risk (Preparedness Framework)](https://openai.com/global-affairs/our-approach-to-frontier-risk/) (OpenAI, 2023) | essay | entry | — | Documents how one frontier lab operationalizes dangerous-capability evaluation in practice, and the category taxonomy (CBRN, cyber, replication, persuasion) that shaped the broader eval ecosystem. |
| [An Introduction to AI Sandbagging](https://www.alignmentforum.org/posts/jsmNCj9QKcfdg8fJk/an-introduction-to-ai-sandbagging) (Teun van der Weij, 2024) | essay | entry | — | The clearest accessible treatment of why capability concealment breaks eval validity — a key entry-tier bridge from 'what evals measure' to 'how they can be gamed'. |

## Core

The load-bearing literature of the subfield.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Red Teaming Language Models with Language Models](https://arxiv.org/abs/2202.03286) (Ethan Perez, Saffron Huang, Francis Song et al., 2022) | paper | core | — | Introduced the now-standard paradigm of LLM-generated red-teaming at scale, and established the baseline methodology all later automated red-teaming builds on. |
| [Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned](https://arxiv.org/abs/2209.07858) (Deep Ganguli, Liane Lovitt, Jackson Kernion et al., 2022) | paper | core | Red Teaming Language Models with Language Models | The canonical empirical study of red-teaming scaling behavior and the standard public red-team attack dataset — the reference point for most red-teaming and safety-eval work. |
| [Can large language models democratize access to dual-use biotechnology?](https://arxiv.org/abs/2306.03809) (Emily H. Soice, Rafael Rocha, Kimberlee Cordova et al., 2023) | paper | core | — | The most-cited early evidence that LLMs lower barriers to biological weapon capability — the empirical foundation for bio-focused dangerous-capability evaluation. |
| [Jailbroken: How Does LLM Safety Training Fail?](https://arxiv.org/abs/2307.02483) (Alexander Wei, Nika Haghtalab, Jacob Steinhardt, 2023) | paper | core | Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned | Moved jailbreaks from an empirical arms race to a classified set of underlying failure modes — the conceptual frame most later jailbreak defenses target. |
| [Model evaluation for extreme risks](https://arxiv.org/abs/2305.15324) (Toby Shevlane, Sebastian Farquhar, Ben Garfinkel et al., 2023) | paper | core | — | The canonical blueprint for frontier-model safety evaluation; its two-pillar distinction (capability vs alignment) underlies most lab evaluation programs and the RSP/Preparedness frameworks. |
| [Model Organisms of Misalignment: The Case for a New Pillar of Alignment Research](https://www.alignmentforum.org/posts/ChDH335ckdvpxXaXX/model-organisms-of-misalignment-the-case-for-a-new-pillar-of-1) (Evan Hubinger, Nicholas Schiefer, Carson Denison et al., 2023) | essay | core | — | The methodological manifesto behind modern deception/scheming evaluation: using engineered demonstrations as stand-ins for failure modes we have not yet observed at scale. |
| [Alignment faking in large language models](https://arxiv.org/abs/2412.14093) (Ryan Greenblatt, Carson Denison, Benjamin Wright et al., 2024) | paper | core | Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training | The first real-model evidence of alignment faking under training pressure, directly implicating RLHF itself in producing deceptive behavior and motivating new monitoring and evaluation approaches. |
| [HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal](https://arxiv.org/abs/2402.04249) (Mantas Mazeika, Long Phan, Xuwang Yin et al., 2024) | paper | core | Universal and Transferable Adversarial Attacks on Aligned Language Models | The de facto standard harness for comparing jailbreak attacks and defenses — it made red-teaming results reproducible and directly comparable across labs. |
| [Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training](https://arxiv.org/abs/2401.05566) (Evan Hubinger, Carson Denison, Jesse Mu et al., 2024) | paper | core | — | The foundational empirical demonstration that deceptive alignment is trainable and safety-training-resistant — the paper that launched the model organisms program and much of the deception-eval agenda. |

## Deep

Formal treatments, frontier research, and specialized material.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [AI Deception: A Survey of Examples, Risks, and Potential Solutions](https://arxiv.org/abs/2308.14752) (Peter S. Park, Simon Goldstein, Aidan O'Gara et al., 2023) | paper | deep | — | The standard reference taxonomy and evidence compilation for AI deception, used to frame deception evaluations and regulation proposals. |
| [AutoDAN: Generating Stealthy Jailbreak Prompts on Aligned Large Language Models](https://arxiv.org/abs/2310.04451) (Xiaogeng Liu, Nan Xu, Muhao Chen et al., 2023) | paper | deep | Universal and Transferable Adversarial Attacks on Aligned Language Models | The canonical demonstration that jailbreaks can evade perplexity-style defenses — motivating the shift from input filtering toward more robust refusal methods. |
| [Tree of Attacks: Jailbreaking Black-Box LLMs Automatically](https://arxiv.org/abs/2312.02119) (Anay Mehrotra, Manolis Zampetakis, Paul Kassianik et al., 2023) | paper | deep | Universal and Transferable Adversarial Attacks on Aligned Language Models | The standard query-efficient black-box jailbreak — important because it works without model gradients, i.e. against exactly the closed models most safety-relevant. |
| [Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043) (Andy Zou, Zifan Wang, Nicholas Carlini et al., 2023) | paper | deep | Jailbroken: How Does LLM Safety Training Fail? | Showed aligned models are vulnerable to automated, transferable adversarial suffixes — a step-change in red-teaming capability and the baseline all subsequent white-box attacks are compared against. |
| [Frontier Models are Capable of In-context Scheming](https://arxiv.org/abs/2412.04984) (Alexander Meinke, Bronson Schoen, Jérémy Scheurer et al., 2024) | paper | deep | Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training | The first systematic evidence that current frontier models scheme in-context when pressured — moving scheming from theory to a measurable, present-day evaluation target. |
| [WildTeaming at Scale: From In-the-Wild Jailbreaks to (Adversarially) Safer Language Models](https://arxiv.org/abs/2406.18510) (Liwei Jiang, Kavel Rao, Seungju Han et al., 2024) | paper | deep | Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned | Showed lab-generated jailbreaks underrepresent real-world attack diversity, and that real-data training improves safety without degrading helpfulness — a corrective to synthetic-only red-teaming. |
| [The WMDP Benchmark: Measuring and Reducing Malicious Use With Unlearning](https://arxiv.org/abs/2403.03218) (Nathaniel Li, Alexander Pan, Anjali Gopal et al., 2024) | paper | deep | Model evaluation for extreme risks | The first widely-adopted open dangerous-knowledge benchmark, and a key demonstration that unlearning — not just refusal — can reduce measured malicious-use capability. |
