# Field Statistics

A quantitative map of the index: what the catalog contains, how the 277 entries connect, and where the 55 subtopics are thinnest.

**277 live/paywalled entries** · 10 domains · 55 subtopics · 163 prerequisite + 471 related cross-links

> Generated from `data/entries.json` — do not edit by hand. Run `python scripts/generate_stats.py`.

## Domains × tiers

| Domain | Entry | Core | Deep | Total | Share |
|---|---|---|---|---|---|
| Interpretability (`interpretability`) | 7 | 16 | 23 | **46** | 16.6% |
| Scalable Oversight & RLHF (`oversight-rlhf`) | 3 | 17 | 13 | **33** | 11.9% |
| Evals & Benchmarks (`evals-benchmarks`) | 3 | 17 | 12 | **32** | 11.6% |
| Agent Foundations & Decision Theory (`agent-foundations`) | 8 | 13 | 9 | **30** | 10.8% |
| Entry Tier (`entry-tier`) | 14 | 9 | 3 | **26** | 9.4% |
| Macrostrategy & X-Risk (`macrostrategy`) | 6 | 14 | 6 | **26** | 9.4% |
| Governance & Policy (`governance-policy`) | 12 | 5 | 7 | **24** | 8.7% |
| Security & Red-teaming (`security-redteam`) | 2 | 11 | 8 | **21** | 7.6% |
| Field Infrastructure (`field-infrastructure`) | 8 | 9 | 3 | **20** | 7.2% |
| Philosophy & Value Alignment (`philosophy-values`) | 1 | 8 | 10 | **19** | 6.9% |
| **Total** | **64** | **119** | **94** | **277** | 100% |

The catalog is a pyramid tilted toward depth: **119 core / 94 deep / 64 entry**. Interpretability is the largest domain (46), field-infrastructure the smallest (20).

## Resource types

| Type | Count |
|---|---|
| paper | 137 |
| essay | 87 |
| book | 14 |
| community | 13 |
| org | 10 |
| tool | 8 |
| course | 4 |
| video | 4 |

Primary literature (papers + essays, 224) dominates; orgs/communities/tools/courses (35) anchor the field-infrastructure domain, with 14 books and 4 videos as accessible entry points.

## Cross-link anatomy

- **163 prerequisite edges** — directed "read this first" links between entries.
- **471 related edges** — undirected critique / rebuttal / follow-up links (deduped).
- **87 cross-domain related edges** (18.5% of related) — the connective tissue that ties the ten domains together.
- **122 of 277 entries (44%) declare no prerequisites** — most are self-contained intros, orgs, or isolated critiques.
- **2 isolated nodes** — entries with neither prerequisites nor related links.

## Top cross-linked hubs

Entries with the most incident edges (prerequisites + related). They are the field's conversation centers: everything connects to them.

| # | Entry | id | Domain | Tier | Degree |
|---|---|---|---|---|---|
| 1 | [AI Alignment: Why It's Hard, and Where to Start](https://intelligence.org/2016/12/28/ai-alignment-why-its-hard-and-where-to-start/) | `ai-alignment-why-hard` | entry-tier | core | 19 |
| 2 | [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) | `constitutional-ai` | oversight-rlhf | core | 15 |
| 3 | [Model evaluation for extreme risks](https://arxiv.org/abs/2305.15324) | `model-evaluation-extreme-risks` | evals-benchmarks | core | 14 |
| 4 | [The Case for Strong Longtermism](https://www.globalprioritiesinstitute.org/wp-content/uploads/The-Case-for-Strong-Longtermism-GPI-Working-Paper-June-2021-2-2.pdf) | `greaves-macaskill-strong-longtermism` | macrostrategy | core | 14 |
| 5 | [Jailbroken: How Does LLM Safety Training Fail?](https://arxiv.org/abs/2307.02483) | `jailbroken-safety-failure` | evals-benchmarks | core | 13 |
| 6 | [Anthropic's Responsible Scaling Policy](https://www.anthropic.com/responsible-scaling-policy) | `anthropic-responsible-scaling-policy` | evals-benchmarks | entry | 13 |
| 7 | [Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043) | `universal-transferable-attacks` | evals-benchmarks | deep | 12 |
| 8 | [A Comprehensive Mechanistic Interpretability Explainer & Glossary](https://www.lesswrong.com/posts/vnocLyeWXcAxtdDnP/a-comprehensive-mechanistic-interpretability-explainer-and) | `comprehensive-mechanistic-interpretability-explainer` | interpretability | entry | 12 |
| 9 | [Computing Power and the Governance of Artificial Intelligence](https://arxiv.org/abs/2402.08797) | `computing-power-governance-ai` | governance-policy | core | 11 |
| 10 | [Functional Decision Theory: A New Theory of Instrumental Rationality](https://arxiv.org/abs/1710.05060) | `fdt-yudkowsky-soares` | agent-foundations | core | 10 |
| 11 | [The Superintelligent Will: Motivation and Instrumental Rationality in Advanced Artificial Agents](https://nickbostrom.com/superintelligentwill.pdf) | `superintelligent-will` | entry-tier | core | 10 |
| 12 | [Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training](https://arxiv.org/abs/2401.05566) | `sleeper-agents` | evals-benchmarks | core | 10 |

The single most-connected entry is **AI Alignment: Why It's Hard, and Where to Start** (`ai-alignment-why-hard`) with 19 links — the standard on-ramp for newcomers.

## Most-referenced prerequisites

Entries most often named as something to read *before* other work — the load-bearing foundations of the index.

| # | Entry | id | Domain | Tier | Times cited as prerequisite |
|---|---|---|---|---|---|
| 1 | [Jailbroken: How Does LLM Safety Training Fail?](https://arxiv.org/abs/2307.02483) | `jailbroken-safety-failure` | evals-benchmarks | core | 6 |
| 2 | [A Comprehensive Mechanistic Interpretability Explainer & Glossary](https://www.lesswrong.com/posts/vnocLyeWXcAxtdDnP/a-comprehensive-mechanistic-interpretability-explainer-and) | `comprehensive-mechanistic-interpretability-explainer` | interpretability | entry | 6 |
| 3 | [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) | `constitutional-ai` | oversight-rlhf | core | 6 |
| 4 | [The Great Filter: Are We Almost Past It?](https://mason.gmu.edu/~rhanson/greatfilter.html) | `great-filter-hanson` | entry-tier | entry | 4 |
| 5 | [AGI Safety Fundamentals (BlueDot Impact)](https://bluedot.org/courses) | `agi-safety-fundamentals` | field-infrastructure | entry | 4 |
| 6 | [The Case for Strong Longtermism](https://www.globalprioritiesinstitute.org/wp-content/uploads/The-Case-for-Strong-Longtermism-GPI-Working-Paper-June-2021-2-2.pdf) | `greaves-macaskill-strong-longtermism` | macrostrategy | core | 4 |
| 7 | [Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training](https://arxiv.org/abs/2401.05566) | `sleeper-agents` | evals-benchmarks | core | 3 |
| 8 | [Universal and Transferable Adversarial Attacks on Aligned Language Models](https://arxiv.org/abs/2307.15043) | `universal-transferable-attacks` | evals-benchmarks | deep | 3 |
| 9 | [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html) | `mathematical-framework-transformer-circuits` | interpretability | core | 3 |
| 10 | [Towards Monosemanticity: Decomposing Language Models With Dictionary Learning](https://transformer-circuits.pub/2023/monosemantic-features/) | `towards-monosemanticity` | interpretability | core | 3 |
| 11 | [Anthropic Bias: Observation Selection Effects in Science and Philosophy](https://www.oxfordmartin.ox.ac.uk/publications/anthropic-bias-observation-selection-effects-in-science-and-philosophy) | `bostrom-anthropic-bias` | macrostrategy | core | 3 |
| 12 | [Existential Risks: Analyzing Human Extinction Scenarios and Related Hazards](https://www.jetpress.org/volume9/risks.html) | `bostrom-existential-risks-2002` | macrostrategy | core | 3 |

## Coverage gaps across the 55 subtopics

### Thin subtopics (≤ 3 entries)

| Domain | Subtopic | Entries |
|---|---|---|
| `philosophy-values` | value-specification | 3 |

These are the highest-priority areas for the next cataloging pass.
### Entry-tier gaps (domains with < 25% of entries in the entry tier)

| Domain | Entry-tier | Total | Share |
|---|---|---|---|
| Philosophy & Value Alignment (`philosophy-values`) | 1 | 19 | 5% |
| Scalable Oversight & RLHF (`oversight-rlhf`) | 3 | 33 | 9% |
| Evals & Benchmarks (`evals-benchmarks`) | 3 | 32 | 9% |
| Security & Red-teaming (`security-redteam`) | 2 | 21 | 10% |
| Interpretability (`interpretability`) | 7 | 46 | 15% |
| Macrostrategy & X-Risk (`macrostrategy`) | 6 | 26 | 23% |

A thin entry tier means newcomers must jump straight into core/deep material — an onboarding gap for readers new to that domain.

### Per-domain subtopic coverage

**Agent Foundations & Decision Theory** (`agent-foundations`)

| Subtopic | Entries |
|---|---|
| cartesian-frames | 4 |
| embedded-agency | 5 |
| corrigibility | 5 |
| infra-bayesianism | 5 |
| logical-induction | 5 |
| decision-theory | 6 |

**Entry Tier** (`entry-tier`)

| Subtopic | Entries |
|---|---|
| fermi-paradox | 4 |
| thought-experiments | 7 |
| sci-fi | 7 |
| introductions | 9 |

**Evals & Benchmarks** (`evals-benchmarks`)

| Subtopic | Entries |
|---|---|
| dangerous-capabilities | 5 |
| eval-critiques | 5 |
| deception | 6 |
| autonomy | 8 |
| red-teaming | 8 |

**Field Infrastructure** (`field-infrastructure`)

| Subtopic | Entries |
|---|---|
| training | 4 |
| funders | 4 |
| orgs | 4 |
| communities | 4 |
| careers | 4 |

**Governance & Policy** (`governance-policy`)

| Subtopic | Entries |
|---|---|
| compute-governance | 4 |
| analogies | 4 |
| international | 5 |
| lab-governance | 5 |
| regulation | 6 |

**Interpretability** (`interpretability`)

| Subtopic | Entries |
|---|---|
| circuits | 5 |
| probing | 5 |
| slt | 5 |
| superposition-saes | 6 |
| tracing | 6 |
| causal-abstraction | 6 |
| rep-engineering | 6 |
| tooling | 7 |

**Macrostrategy & X-Risk** (`macrostrategy`)

| Subtopic | Entries |
|---|---|
| great-filter | 4 |
| differential-development | 4 |
| xrisk-theory | 5 |
| forecasting | 5 |
| longtermism | 8 |

**Scalable Oversight & RLHF** (`oversight-rlhf`)

| Subtopic | Entries |
|---|---|
| debate | 4 |
| weak-to-strong | 4 |
| process-outcome | 4 |
| reward-hacking | 4 |
| amplification | 5 |
| rlhf | 6 |
| constitutional-ai | 6 |

**Philosophy & Value Alignment** (`philosophy-values`)

| Subtopic | Entries |
|---|---|
| value-specification | 3 |
| moral-uncertainty | 4 |
| cev | 4 |
| pluralism | 4 |
| population-ethics | 4 |

**Security & Red-teaming** (`security-redteam`)

| Subtopic | Entries |
|---|---|
| adversarial-robustness | 4 |
| weights | 4 |
| supply-chain | 4 |
| prompt-injection | 4 |
| jailbreaks | 5 |
