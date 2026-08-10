#!/usr/bin/env python3
"""Generate /domains/*.md from /data/entries.json.

One file per domain, grouped by tier (entry / core / deep), rendered as a table
(Resource | Type | Tier | Prerequisites | Why it matters). Live/paywalled entries only;
`dead` entries are kept in the catalog but excluded from the published markdown.
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, "data", "entries.json")
DOMAINS_DIR = os.path.join(ROOT, "domains")

DOMAINS = [
    ("entry-tier", "Entry Tier", "Intuition pumps: the thought experiments and accessible material that make alignment click."),
    ("macrostrategy", "Macrostrategy & X-Risk", "Existential risk theory, forecasting, differential development, longtermism and its critics."),
    ("agent-foundations", "Agent Foundations & Decision Theory", "Embedded agency, decision theory, corrigibility, infra-Bayesianism, Cartesian frames, logical induction."),
    ("interpretability", "Interpretability", "Circuits, superposition/SAEs, tracing, probing, causal abstraction, SLT, representation engineering, tooling."),
    ("oversight-rlhf", "Scalable Oversight & RLHF", "RLHF and its failure modes, constitutional AI, debate, amplification, weak-to-strong, reward hacking."),
    ("evals-benchmarks", "Evals & Benchmarks", "Dangerous capabilities, deception/scheming, autonomy, red-teaming suites, and eval critiques."),
    ("governance-policy", "Governance & Policy", "Compute governance, international coordination, lab governance, regulation by jurisdiction, analogies."),
    ("security-redteam", "Security & Red-teaming", "Adversarial robustness, jailbreaks, weight security, supply chain, prompt injection."),
    ("philosophy-values", "Philosophy & Value Alignment", "Value specification, moral uncertainty, CEV, pluralistic alignment, population ethics."),
    ("field-infrastructure", "Field Infrastructure", "Training programs, funders, research orgs, communities, career pathways."),
]

TIER_ORDER = [("entry", "Entry tier", "No prerequisites beyond the domain's stated baseline."),
              ("core", "Core", "The load-bearing literature of the subfield."),
              ("deep", "Deep", "Formal treatments, frontier research, and specialized material.")]


def fmt_crossrefs(ids, by_id):
    out = []
    for i in ids:
        e = by_id.get(i)
        out.append(e["title"] if e else i)
    return ", ".join(out) if out else "—"


def esc(s):
    """Escape markdown-table-breaking pipe characters in cell text."""
    return str(s).replace("|", "\\|")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="render and compare against existing files without writing; exit 1 if stale")
    args = ap.parse_args()

    with open(ENTRIES, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    by_id = {e["id"]: e for e in catalog}
    os.makedirs(DOMAINS_DIR, exist_ok=True)
    total_rendered = 0
    rendered = {}
    for dom_id, dom_title, dom_desc in DOMAINS:
        entries = [e for e in catalog if e["domain"] == dom_id and e["status"] != "dead"]
        total_rendered += len(entries)
        lines = [
            f"# {dom_title}",
            "",
            dom_desc,
            "",
            f"**{len(entries)} live/paywalled entries** · catalog domain id: `{dom_id}`",
            "",
            "> Generated from `data/entries.json` — do not edit by hand. Run `python scripts/generate_domains.py`.",
            "",
        ]
        for tier_key, tier_title, tier_desc in TIER_ORDER:
            tier_entries = sorted([e for e in entries if e["tier"] == tier_key], key=lambda e: e["year"])
            lines.append(f"## {tier_title}")
            lines.append("")
            lines.append(tier_desc)
            lines.append("")
            if not tier_entries:
                lines.append("_No entries yet._")
                lines.append("")
                continue
            lines.append("| Resource | Type | Tier | Prerequisites | Why it matters |")
            lines.append("|---|---|---|---|---|")
            for e in tier_entries:
                authors = ", ".join(esc(a) for a in e["authors"][:3])
                if len(e["authors"]) > 3:
                    authors += " et al."
                resource = f"[{esc(e['title'])}]({e['url']}) ({authors}, {e['year']})"
                pre = esc(fmt_crossrefs(e["prerequisites"], by_id))
                lines.append(f"| {resource} | {e['type']} | {e['tier']} | {pre} | {esc(e['why_it_matters'])} |")
            lines.append("")
        rendered[dom_id] = "\n".join(lines)
        if not args.check:
            with open(os.path.join(DOMAINS_DIR, f"{dom_id}.md"), "w", encoding="utf-8") as f:
                f.write(rendered[dom_id])
    if args.check:
        stale = []
        for dom_id, content in rendered.items():
            path = os.path.join(DOMAINS_DIR, f"{dom_id}.md")
            if not os.path.exists(path) or open(path, encoding="utf-8").read() != content:
                stale.append(dom_id)
        if stale:
            print(f"STALE: {', '.join(stale)} — run `python scripts/generate_domains.py`")
            sys.exit(1)
        print(f"OK: {len(DOMAINS)} domain files match data/entries.json")
        sys.exit(0)
    print(f"GENERATED {len(DOMAINS)} domain files, {total_rendered} entries rendered "
          f"(catalog has {len(catalog)} total, {sum(1 for e in catalog if e['status'] == 'dead')} dead excluded)")


if __name__ == "__main__":
    main()
