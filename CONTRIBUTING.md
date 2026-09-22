# Contributing

The index is data-first: **`data/entries.json` is the source of truth**, and every `/domains/*.md` file is generated from it. If you see a rendering bug, fix the generator, not the markdown.

## Entry schema

Every entry is a JSON object:

```json
{
  "id": "kebab-case-unique-slug",
  "title": "Exact title as published",
  "authors": ["Author Name", "..."],
  "year": 2024,
  "url": "https://canonical-source-url",
  "type": "paper | course | org | tool | community | book | video | essay | dataset",
  "domain": "one of: entry-tier, macrostrategy, agent-foundations, interpretability, oversight-rlhf, evals-benchmarks, governance-policy, security-redteam, philosophy-values, field-infrastructure",
  "subtopics": ["tags from that domain's subtopic list"],
  "tier": "entry | core | deep",
  "prerequisites": ["ids of entries to read first, if any"],
  "summary": "2-3 original sentences, your own paraphrase, never copied text",
  "why_it_matters": "1 sentence on significance or what it changed",
  "related": ["ids of entries that critique, extend, or respond to this one"],
  "last_verified": "YYYY-MM-DD",
  "status": "live | paywalled | dead"
}
```

## Hard rules

1. **No fabrication, ever.** Every title, author, URL, and date must come from a page you actually fetched. If you can't confirm a resource exists and resolves, you drop it.
2. **URLs must resolve.** Run `python scripts/verify_links.py` before committing; a `dead` entry is kept in the catalog but excluded from the published index.
3. **Original phrasing.** `summary` and `why_it_matters` are your own paraphrase — a few words of exact quotation is the limit.
4. **Cross-link seriously.** `prerequisites` and `related` are the point of this index. On `core`/`deep` entries, ≥60% must have them populated.
5. **`status: dead` entries stay** (so the record of "this used to be here" survives) but are flagged for removal review and excluded from the generated markdown.

## Workflow for a new subtopic

> **Tag contract:** every entry's `subtopics` must use the exact tags defined in `scripts/taxonomy.py` for its domain — the merge script rejects unknown tags at merge time. An entry lives in **exactly one domain**; if a topic is already covered in another domain (e.g. the Great Filter entries under `entry-tier`/`fermi-paradox`), do not duplicate it — reference it via `prerequisites`/`related` instead.

1. Research: 3-4 independently-phrased searches per subtopic, site-scoped (`site:arxiv.org`, `site:alignmentforum.org`, lab domains, etc.), past page one.
2. Fetch each candidate page to confirm it exists, is on-topic, and has real authors.
3. Write entries as a fragment file, merge: `python scripts/merge_entries.py data/fragments/<subtopic>.json`
4. Regenerate: `python scripts/generate_domains.py`
5. Verify links: `python scripts/verify_links.py --apply`
6. Commit message: `catalog(<domain>): <subtopic> — N entries added` (commit `entries.json` + affected domain `.md` together).

## Audit

`python scripts/audit.py` runs the mechanical checks of the final audit (coverage, tier spread, dedup, cross-link %, counts). Originality spot-checks and last-24h URL checks remain human/agent review.
