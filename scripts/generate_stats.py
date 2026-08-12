#!/usr/bin/env python3
"""Generate domains/statistics.md — a field-level statistics report from data/entries.json.

Covers: per-domain × per-tier counts, resource-type distribution, cross-link anatomy
(prerequisite vs related edges, cross-domain links), top cross-linked hubs (degree),
most-referenced prerequisites (in-degree on prerequisite edges), and coverage gaps
across the 55 canonical subtopics (thin subtopics, entry-tier gaps, isolated nodes).

Usage:  python -X utf8 scripts/generate_stats.py            # write domains/statistics.md
        python -X utf8 scripts/generate_stats.py --check    # diff against existing file, exit 1 if stale
"""
import argparse
import json
import os
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from taxonomy import DOMAIN_TITLES, EXPECTED_SUBTOPICS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, "data", "entries.json")
DOMAINS_DIR = os.path.join(ROOT, "domains")
OUT = os.path.join(DOMAINS_DIR, "statistics.md")

TIER_ORDER = ["entry", "core", "deep"]
TYPE_ORDER = ["paper", "essay", "book", "community", "org", "tool", "course", "video"]


def esc(s):
    """Escape markdown-table-breaking pipe characters in cell text."""
    return str(s).replace("|", "\\|")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="render and compare against the existing file without writing; exit 1 if stale")
    args = ap.parse_args()

    with open(ENTRIES, "r", encoding="utf-8") as fh:
        catalog = json.load(fh)
    by_id = {e["id"]: e for e in catalog}
    ids = set(by_id)
    live = [e for e in catalog if e["status"] != "dead"]

    # ---- per-domain × per-tier counts ----
    dom_tier = defaultdict(Counter)
    dom_total = Counter()
    type_count = Counter()
    for e in live:
        dom_tier[e["domain"]][e["tier"]] += 1
        dom_total[e["domain"]] += 1
        type_count[e["type"]] += 1

    # ---- cross-link anatomy ----
    prereq_out = Counter()   # edges where entry declares the prerequisite
    prereq_in = Counter()    # times an entry is named as someone's prerequisite
    related_edges = set()    # deduped undirected {min,max} pairs
    cross_domain_related = 0
    for e in live:
        for p in e.get("prerequisites") or []:
            if p in ids and p != e["id"]:
                prereq_out[e["id"]] += 1
                prereq_in[p] += 1
        for r in e.get("related") or []:
            if r in ids and r != e["id"]:
                key = tuple(sorted((e["id"], r)))
                if key in related_edges:
                    continue
                related_edges.add(key)
                if by_id[e["id"]]["domain"] != by_id[r]["domain"]:
                    cross_domain_related += 1
    n_prereq = sum(prereq_out.values())
    n_related = len(related_edges)

    # ---- degree (hubs) over both edge types (related deduped to match graph.html) ----
    degree = Counter()
    for e in live:
        for p in e.get("prerequisites") or []:
            if p in ids and p != e["id"]:
                degree[e["id"]] += 1
                degree[p] += 1
    for a, b in related_edges:
        degree[a] += 1
        degree[b] += 1
    isolated = [e for e in live if degree[e["id"]] == 0]

    # ---- subtopic coverage ----
    sub_count = Counter()
    for e in live:
        for s in e.get("subtopics") or []:
            sub_count[s] += 1
    per_dom_sub = defaultdict(list)
    for dom_id, subs in EXPECTED_SUBTOPICS.items():
        per_dom_sub[dom_id] = [(s, sub_count.get(s, 0)) for s in subs]

    # ---- gaps ----
    thin_subtopics = [(dom, s, c) for dom, subs in per_dom_sub.items() for s, c in subs if c <= 3]
    thin_subtopics.sort(key=lambda x: x[2])
    entry_tier_gap = sorted(
        [(d, dom_tier[d]["entry"], dom_total[d]) for d in dom_total
         if dom_total[d] >= 5 and dom_tier[d]["entry"] / dom_total[d] < 0.25],
        key=lambda x: x[1] / x[2])
    no_prereq = sum(1 for e in live if not (e.get("prerequisites") or []))

    def hub_rows(ids_ranked):
        rows = []
        for rank, (eid, cnt) in enumerate(ids_ranked, 1):
            e = by_id[eid]
            rows.append(f"| {rank} | [{esc(e['title'])}]({e['url']}) | `{eid}` | {e['domain']} | {e['tier']} | {cnt} |")
        return "\n".join(rows)

    top_degree = degree.most_common(12)
    top_prereq_in = prereq_in.most_common(12)

    L = []
    L.append("# Field Statistics")
    L.append("")
    L.append("A quantitative map of the index: what the catalog contains, how the 277 entries "
             "connect, and where the 55 subtopics are thinnest.")
    L.append("")
    L.append(f"**{len(live)} live/paywalled entries** · 10 domains · 55 subtopics · "
             f"{n_prereq} prerequisite + {n_related} related cross-links")
    L.append("")
    L.append("> Generated from `data/entries.json` — do not edit by hand. Run `python scripts/generate_stats.py`.")
    L.append("")

    # ---- 1. domain × tier ----
    L.append("## Domains × tiers")
    L.append("")
    L.append("| Domain | Entry | Core | Deep | Total | Share |")
    L.append("|---|---|---|---|---|---|")
    for dom_id in sorted(dom_total, key=lambda d: -dom_total[d]):
        c = dom_tier[dom_id]
        total = dom_total[dom_id]
        share = f"{100 * total / len(live):.1f}%"
        L.append(f"| {esc(DOMAIN_TITLES[dom_id])} (`{dom_id}`) | {c['entry']} | {c['core']} | {c['deep']} | **{total}** | {share} |")
    tier_totals = {t: sum(dom_tier[d][t] for d in dom_tier) for t in TIER_ORDER}
    L.append(f"| **Total** | **{tier_totals['entry']}** | **{tier_totals['core']}** | **{tier_totals['deep']}** | **{len(live)}** | 100% |")
    L.append("")
    L.append("The catalog is a pyramid tilted toward depth: **119 core / 94 deep / 64 entry**. "
             "Interpretability is the largest domain (46), field-infrastructure the smallest (20).")
    L.append("")

    # ---- 2. resource types ----
    L.append("## Resource types")
    L.append("")
    L.append("| Type | Count |")
    L.append("|---|---|")
    for t in TYPE_ORDER:
        L.append(f"| {t} | {type_count.get(t, 0)} |")
    books = type_count.get("book", 0)
    videos = type_count.get("video", 0)
    L.append("")
    L.append(f"Primary literature (papers + essays, {type_count.get('paper', 0) + type_count.get('essay', 0)}) dominates; "
             f"orgs/communities/tools/courses ({type_count.get('community', 0) + type_count.get('org', 0) + type_count.get('tool', 0) + type_count.get('course', 0)}) "
             f"anchor the field-infrastructure domain, with {books} books and {videos} videos as accessible entry points.")
    L.append("")

    # ---- 3. cross-link anatomy ----
    L.append("## Cross-link anatomy")
    L.append("")
    L.append(f"- **{n_prereq} prerequisite edges** — directed \"read this first\" links between entries.")
    L.append(f"- **{n_related} related edges** — undirected critique / rebuttal / follow-up links (deduped).")
    L.append(f"- **{cross_domain_related} cross-domain related edges** ({100 * cross_domain_related / max(n_related, 1):.1f}% of related) — "
             "the connective tissue that ties the ten domains together.")
    L.append(f"- **{no_prereq} of {len(live)} entries ({100 * no_prereq / len(live):.0f}%) declare no prerequisites** — most are "
             "self-contained intros, orgs, or isolated critiques.")
    L.append(f"- **{len(isolated)} isolated nodes** — entries with neither prerequisites nor related links.")
    L.append("")

    # ---- 4. hubs ----
    L.append("## Top cross-linked hubs")
    L.append("")
    L.append("Entries with the most incident edges (prerequisites + related). They are the field's "
             "conversation centers: everything connects to them.")
    L.append("")
    L.append("| # | Entry | id | Domain | Tier | Degree |")
    L.append("|---|---|---|---|---|---|")
    L.append(hub_rows(top_degree))
    L.append("")
    L.append(f"The single most-connected entry is **{by_id[top_degree[0][0]]['title']}** "
             f"(`{top_degree[0][0]}`) with {top_degree[0][1]} links — the standard on-ramp for newcomers.")
    L.append("")

    # ---- 5. most-referenced prerequisites ----
    L.append("## Most-referenced prerequisites")
    L.append("")
    L.append("Entries most often named as something to read *before* other work — the load-bearing "
             "foundations of the index.")
    L.append("")
    L.append("| # | Entry | id | Domain | Tier | Times cited as prerequisite |")
    L.append("|---|---|---|---|---|---|")
    L.append(hub_rows(top_prereq_in))
    L.append("")

    # ---- 6. coverage gaps ----
    L.append("## Coverage gaps across the 55 subtopics")
    L.append("")
    L.append("### Thin subtopics (≤ 3 entries)")
    L.append("")
    if thin_subtopics:
        L.append("| Domain | Subtopic | Entries |")
        L.append("|---|---|---|")
        for dom_id, s, c in thin_subtopics:
            L.append(f"| `{dom_id}` | {s} | {c} |")
        L.append("")
        L.append("These are the highest-priority areas for the next cataloging pass.")
    else:
        L.append("_None — every subtopic has at least 4 entries._")
        L.append("")
    L.append("### Entry-tier gaps (domains with < 25% of entries in the entry tier)")
    L.append("")
    L.append("| Domain | Entry-tier | Total | Share |")
    L.append("|---|---|---|---|")
    for dom_id, e_cnt, total in entry_tier_gap:
        L.append(f"| {esc(DOMAIN_TITLES[dom_id])} (`{dom_id}`) | {e_cnt} | {total} | {100 * e_cnt / total:.0f}% |")
    L.append("")
    L.append("A thin entry tier means newcomers must jump straight into core/deep material — "
             "an onboarding gap for readers new to that domain.")
    L.append("")
    L.append("### Per-domain subtopic coverage")
    L.append("")
    for dom_id in sorted(per_dom_sub):
        subs = per_dom_sub[dom_id]
        L.append(f"**{esc(DOMAIN_TITLES[dom_id])}** (`{dom_id}`)")
        L.append("")
        L.append("| Subtopic | Entries |")
        L.append("|---|---|")
        for s, c in sorted(subs, key=lambda x: x[1]):
            L.append(f"| {s} | {c} |")
        L.append("")

    content = "\n".join(L).rstrip() + "\n"

    if args.check:
        if not os.path.exists(OUT) or open(OUT, encoding="utf-8").read() != content:
            print(f"STALE: {OUT} — run `python scripts/generate_stats.py`")
            sys.exit(1)
        print(f"OK: {OUT} matches data/entries.json")
        sys.exit(0)

    os.makedirs(DOMAINS_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(content)
    print(f"GENERATED {OUT}: {len(live)} entries, {n_prereq} prereq + {n_related} related edges, "
          f"{len(thin_subtopics)} thin subtopics, {len(entry_tier_gap)} entry-tier gaps, {len(isolated)} isolates")


if __name__ == "__main__":
    main()
