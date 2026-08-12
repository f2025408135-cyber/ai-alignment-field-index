# Philosophy & Value Alignment

Value specification, moral uncertainty, CEV, pluralistic alignment, population ethics.

**15 live/paywalled entries** · catalog domain id: `philosophy-values`

> Generated from `data/entries.json` — do not edit by hand. Run `python scripts/generate_domains.py`.

## Entry tier

No prerequisites beyond the domain's stated baseline.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [When is unaligned AI morally valuable?](https://www.lesswrong.com/posts/3kN79EuT27trGexsq/when-is-unaligned-ai-morally-valuable) (Paul Christiano, 2018) | community | entry | — | A sharp moral-uncertainty argument that destabilizes a core alignment assumption — that human values are the obvious target — and introduces the moral-standing-of-AI problem to a wide audience. |

## Core

The load-bearing literature of the subfield.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Coherent Extrapolated Volition](https://intelligence.org/files/CEV.pdf) (Eliezer Yudkowsky, 2004) | essay | core | — | The canonical statement of the 'meta-value' approach to alignment: the target is not what humans currently want but what we would want under idealization — the concept nearly all later value-target debates (CAV, value lock-in, corrigibility) define themselves against. |
| [Cooperative Inverse Reinforcement Learning](https://arxiv.org/abs/1606.03137) (Dylan Hadfield-Menell, Anca Dragan, Pieter Abbeel et al., 2016) | paper | core | — | The founding formalization of assistance-game alignment — it made precise why value specification is a problem of inference and cooperation, not of writing a better reward function, and inspired a large research program. |
| [Inverse Reward Design](https://arxiv.org/abs/1711.02827) (Dylan Hadfield-Menell, Smitha Milli, Pieter Abbeel et al., 2017) | paper | core | Cooperative Inverse Reinforcement Learning | Gives a principled answer to reward misspecification: rather than naively optimizing the given reward, an aligned agent should reason about the reward-design process itself — the basis for later corrigible and uncertainty-aware reward models. |
| [Clarifying AI Alignment](https://www.alignmentforum.org/posts/ZeE7EKHTFMBs8eMxn/clarifying-ai-alignment) (Paul Christiano, 2018) | community | core | — | Set the modern pragmatic framing of alignment that most frontier labs now use — and implicitly stepped away from CEV-style ambitious targets, making it the reference point for the 'alignment as intent-following' school. |
| [Moral Uncertainty](https://global.oup.com/academic/product/moral-uncertainty-9780198722274) (William MacAskill, Krister Bykvist, Toby Ord, 2020) | book | core | — | The foundation for aligning AI under moral disagreement: if an AI must act while we are unsure what is right, MEC-style reasoning is the leading formal answer — and the book that made 'moral uncertainty' a distinct field. |
| [A Roadmap to Pluralistic Alignment](https://arxiv.org/abs/2402.05070) (Taylor Sorensen, Jared Moore, Jillian Fisher et al., 2024) | paper | core | Constitutional AI: Harmlessness from AI Feedback | The canonical articulation of why alignment should not collapse diverse human values into a single average — the paper that named and organized the pluralism research agenda. |

## Deep

Formal treatments, frontier research, and specialized material.

| Resource | Type | Tier | Prerequisites | Why it matters |
|---|---|---|---|---|
| [Coherent Aggregated Volition: A Method for Deriving Goal System Content for Advanced, Beneficial AGIs](https://stafforini.com/works/goertzel-2010-coherent-aggregated-volition/) (Ben Goertzel, 2010) | essay | deep | Coherent Extrapolated Volition | The most prominent early challenge to CEV's convergence assumption — the intellectual root of the later pluralistic-alignment movement's emphasis on aggregating diverse values. |
| [Reinforcement Learning Under Moral Uncertainty](https://arxiv.org/abs/2006.04734) (Adrien Ecoffet, Joel Lehman, 2020) | paper | deep | Moral Uncertainty | The first concrete RL implementation of moral uncertainty — proof that an agent can act under value disagreement rather than needing a single settled reward function. |
| [The Alignment Problem from a Deep Learning Perspective](https://arxiv.org/abs/2209.00626) (Richard Ngo, Lawrence Chan, Sören Mindermann, 2022) | paper | deep | AI Alignment: Why It's Hard, and Where to Start | The clearest modern statement of why value specification fails in practice: even with perfect training signals, generalization can produce systematically misaligned behavior — the canonical framing for deep-learning-era alignment work. |
| [Coherent Extrapolated Dreaming](https://www.alignmentforum.org/posts/vdXNPzuh3fwgykvKY/coherent-extrapolated-dreaming) (Alex Flint, 2022) | community | deep | Coherent Extrapolated Volition | One of the sharpest modern CEV critiques — it reframes the problem from 'what values to extrapolate' to 'what kind of thing is the subject of extrapolation,' undermining a core CEV assumption. |
| [Moral Uncertainty and the Problem of Fanaticism](https://arxiv.org/abs/2312.11589) (Jazon Szabo, Jose Such, Natalia Criado et al., 2023) | paper | deep | Moral Uncertainty | Bridges moral-uncertainty theory to AI decision-making, showing concretely how an agent with moral uncertainty should compute action choiceworthiness — the technical heart of value uncertainty in deployed systems. |
| [Collective Constitutional AI: Aligning a Language Model with Public Input](https://arxiv.org/abs/2406.07814) (Saffron Huang, Divya Siddarth, Liane Lovitt et al., 2024) | paper | deep | Constitutional AI: Harmlessness from AI Feedback | The leading demonstration that pluralistic alignment can be operationalized — collective deliberation feeding directly into model training, rather than values being fixed by a small developer team. |
| [Personalization of Large Language Models: A Survey](https://arxiv.org/abs/2411.00027) (Zhehao Zhang, Ryan A. Rossi, Branislav Kveton et al., 2024) | paper | deep | — | The technical backbone of the 'steerable/personalized' branch of pluralistic alignment: how models can adapt to individual values rather than imposing one universal default. |
| [Moral Disagreement and the Limits of AI Value Alignment: A Dual Challenge of Epistemic Justification and Political Legitimacy](https://pmc.ncbi.nlm.nih.gov/articles/PMC12628449/) (Nick Schuster, Daniel Kilov, 2025) | paper | deep | A Roadmap to Pluralistic Alignment | Grounds the technical pluralism agenda in moral and political philosophy — the argument that alignment cannot legitimately pick winners among reasonable moral views, which shapes both research and regulation debates. |
