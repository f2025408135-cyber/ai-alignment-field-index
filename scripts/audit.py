#!/usr/bin/env python3
"""Mechanical checks of the final audit (Section 9 of the brief).

Covers: subtopic coverage, tier spread, dedup (>90% title/url similarity), cross-link
saturation on core/deep, domain md freshness vs entries.json, PROGRESS all-done,
README counts. Originality spot-checks and last-24h URL re-verification remain manual.
"""
import json
import os
import re
import subprocess
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, "data", "entries.json")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from taxonomy import EXPECTED_SUBTOPICS  # noqa: E402

ENTRY_TIER_DOMAINS = {"entry-tier", "governance-policy", "philosophy-values", "field-infrastructure"}


def similarity(a, b, is_url=False):
    """Token-set Jaccard similarity on lowercase alnum tokens.
    For URLs, strip scheme+host first (distinct arXiv/GitHub/YouTube URLs share
    a long identical prefix; comparing full strings false-positives).
    """
    if is_url:
        s = a.split("://", 1)[-1]
        parts = s.split("/", 1)
        a = parts[1] if len(parts) > 1 else parts[0]
        s = b.split("://", 1)[-1]
        parts = s.split("/", 1)
        b = parts[1] if len(parts) > 1 else parts[0]
    ta = set(re.findall(r"[a-z0-9]+", a.lower()))
    tb = set(re.findall(r"[a-z0-9]+", b.lower()))
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


def main():
    with open(ENTRIES, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    ok = True

    def check(name, cond, detail=""):
        nonlocal ok
        mark = "PASS" if cond else "FAIL"
        if not cond:
            ok = False
        print(f"[{mark}] {name} {detail}")

    # 1. subtopic coverage
    coverage = {d: set() for d in EXPECTED_SUBTOPICS}
    for e in catalog:
        if e["status"] == "dead":
            continue
        for s in e["subtopics"]:
            coverage[e["domain"]].add(s)
    for d, subs in EXPECTED_SUBTOPICS.items():
        missing = [s for s in subs if s not in coverage[d]]
        check(f"coverage {d}", not missing, f"missing: {missing}" if missing else f"({len(coverage[d])}/{len(subs)})")

    # 2. tier spread per domain
    for d in EXPECTED_SUBTOPICS:
        tiers = {e["tier"] for e in catalog if e["domain"] == d and e["status"] != "dead"}
        check(f"tier-spread {d}", len(tiers) >= 2, f"tiers: {sorted(tiers)}")
    for d in ENTRY_TIER_DOMAINS:
        has_entry_tier = any(e["domain"] == d and e["tier"] == "entry" for e in catalog)
        check(f"entry-tier-material {d}", has_entry_tier)

    # 3. dedup: >90% title or url similarity (URLs compared by path tokens only)
    dupes = []
    for i in range(len(catalog)):
        for j in range(i + 1, len(catalog)):
            a, b = catalog[i], catalog[j]
            if similarity(a["url"], b["url"], is_url=True) > 0.90 or similarity(a["title"], b["title"]) > 0.90:
                dupes.append((a["id"], b["id"]))
    check("dedup", not dupes, f"dupes: {dupes[:5]}" if dupes else "")

    # 6. cross-link saturation on core/deep
    core_deep = [e for e in catalog if e["tier"] in ("core", "deep") and e["status"] != "dead"]
    linked = [e for e in core_deep if e["prerequisites"] or e["related"]]
    pct = (len(linked) / len(core_deep) * 100) if core_deep else 100
    check("crosslinks-core-deep", pct >= 60, f"({len(linked)}/{len(core_deep)} = {pct:.0f}%)")

    # dangling cross-refs
    ids = {e["id"] for e in catalog}
    dangling = []
    for e in catalog:
        for k in ("prerequisites", "related"):
            for i in e[k]:
                if i not in ids:
                    dangling.append((e["id"], k, i))
    check("crossref-integrity", not dangling, f"dangling: {dangling[:5]}" if dangling else "")

    # freshness flag (brief Section 2: flag anything >12 months old for a freshness check).
    # Catalog has only a year int, so the cutoff is calendar-granular and intentionally errs
    # toward flagging (anything published in or before the previous calendar year).
    cutoff = date.today().year - 1
    fresh_queue = sorted(e["id"] for e in catalog
                         if e["status"] != "dead" and e["year"] <= cutoff)
    print(f"[INFO] freshness review queue: {len(fresh_queue)} entries published in {cutoff} or earlier "
          f"(year-granular; historical canon may stay; each must be reviewed in the final pass)")
    for eid in fresh_queue[:40]:
        print(f"       {eid}")

    # 7. domains md freshness: generator --check renders and diffs WITHOUT writing (no side effects)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "generate_domains.py"), "--check"],
                       capture_output=True, text=True)
    check("domains-md-fresh", r.returncode == 0, (r.stdout or r.stderr).strip()[:300])

    # 8. PROGRESS all done
    progress_path = os.path.join(ROOT, "PROGRESS.md")
    with open(progress_path, "r", encoding="utf-8") as f:
        prog = f.read()
    rows = re.findall(r"^\| ([a-z-]+) \| (.+?) \| (not started|in progress|done) \|", prog, re.M)
    not_done = [r for r in rows if r[2] != "done"]
    check("progress-all-done", not not_done, f"pending: {[r[1][:30] for r in not_done][:5]}" if not_done else f"({len(rows)} rows)")

    # 9. README counts match
    readme_path = os.path.join(ROOT, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme = f.read()
    total = len([e for e in catalog if e["status"] != "dead"])
    per_dom = {}
    for e in catalog:
        if e["status"] != "dead":
            per_dom[e["domain"]] = per_dom.get(e["domain"], 0) + 1
    readme_total = re.search(r"\*\*Total entries: (\d+)\*\*", readme)
    check("readme-total", readme_total and int(readme_total.group(1)) == total,
          f"({readme_total.group(1) if readme_total else '?'} vs {total})")
    for d, n in per_dom.items():
        # README row: | [Title](domains/<d>.md) | <what's inside> | <count> | — skip the description cell
        m = re.search(rf"\|\s*\[[^\]]+\]\(domains/{d}\.md\)[^|]*\|[^|]*\|\s*(\d+)\s*\|", readme)
        check(f"readme-count {d}", m and int(m.group(1)) == n, f"(readme {m.group(1) if m else '?'} vs {n})")

    print("\n" + ("AUDIT: ALL MECHANICAL CHECKS PASS" if ok else "AUDIT: FAILURES PRESENT"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
