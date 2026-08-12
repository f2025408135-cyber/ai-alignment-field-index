# Unified AI Alignment Field Index

A living, curated index of the AI alignment field — organized as **prerequisite tiers within topic domains**, with critique/rebuttal cross-linking, not a flat list of links.

## Why this index exists

Most existing lists (`awesome-*-alignment` repos, wiki-style sites) are flat dumps: strong on famous papers, weak on *why things connect*. This index is built differently:

- **Drawer model** — ten topic domains, each internally tiered `entry → core → deep` with explicit prerequisites.
- **Connective tissue** — every `core`/`deep` entry links to the critiques, rebuttals, and follow-ups it provoked (`related`), and to what you should read first (`prerequisites`).
- **Depth beyond the top-10** — foundational papers *and* the sub-literature around them: formal treatments, implementations, tooling.
- **Honest about the field's shape** — governance, philosophy, macrostrategy, and field infrastructure sit alongside technical ML content.
- **Verified & fresh** — every URL is fetch-confirmed before inclusion and re-checked on each audit pass; anything >12 months old is flagged for freshness review.
- **Zero fabrication** — every entry was found via live search/fetch. Nothing is included from memory.

## The ten domains

| Domain | What's inside | Entries |
|---|---|---|
| [Entry Tier](domains/entry-tier.md) | Paperclip maximizer, orthogonality, Fermi/Great Filter, analytical sci-fi, accessible intros | 26 |
| [Macrostrategy & X-Risk](domains/macrostrategy.md) | X-risk theory, timeline forecasting, differential development, longtermism ± critiques | 26 |
| [Agent Foundations & Decision Theory](domains/agent-foundations.md) | Embedded agency, CDT/EDT/UDT/FDT, corrigibility, infra-Bayesianism, Cartesian frames, logical induction | 30 |
| [Interpretability](domains/interpretability.md) | Circuits, superposition/SAEs, tracing, probing, causal scrubbing, SLT, rep engineering, tooling | 46 |
| [Scalable Oversight & RLHF](domains/oversight-rlhf.md) | RLHF failure modes, CAI/RLAIF, debate, amplification, weak-to-strong, reward hacking, sycophancy | 33 |
| [Evals & Benchmarks](domains/evals-benchmarks.md) | Dangerous capabilities, deception/scheming, autonomy, red-teaming suites, eval critiques | 32 |
| [Governance & Policy](domains/governance-policy.md) | Compute governance, international coordination, lab governance, regulation by jurisdiction, analogies | 24 |
| [Security & Red-teaming](domains/security-redteam.md) | Adversarial robustness, jailbreaks, weight security, supply chain, prompt injection | 21 |
| [Philosophy & Value Alignment](domains/philosophy-values.md) | Value specification, moral uncertainty, CEV ± critiques, pluralistic alignment, population ethics | 19 |
| [Field Infrastructure](domains/field-infrastructure.md) | Training programs, funders, research orgs, communities, career pathways | 20 |

**Total entries: 277**

## Interactive cross-link graph

[**Open the network graph**](graph.html) — a self-contained, offline-friendly interactive map of the whole index: every entry is a node, every `prerequisite` (solid, directed) and `related`/critique/rebuttal edge (dashed) is a link. 277 nodes · 634 edges · 10 domain clusters. Search by title/author/id, filter by tier and domain, click any node for its full record, or drag the graph to explore. Regenerate anytime with `python -X utf8 scripts/generate_graph.py`.

## Data

The machine-readable catalog lives in [`data/entries.json`](data/entries.json) (schema in [`CONTRIBUTING.md`](CONTRIBUTING.md)). Every `/domains/*.md` file is generated from it — edit the data, not the markdown.

## Status

In progress. Tracked in [`PROGRESS.md`](PROGRESS.md).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). No entry ships without a verified, resolving URL and an original paraphrase.

## License

MIT — see [`LICENSE`](LICENSE).
