#!/usr/bin/env python3
"""Generate assets/graph-thumbnail.svg + assets/badge-*.svg from data/entries.json.

A deterministic, dependency-free static render of the cross-link network for the
repo landing page: 277 nodes colored by domain, prerequisite edges (solid) and
related edges (dashed), hub labels, plus shields-style count badges. Uses the
same domain palette as graph.html so the thumbnail matches the interactive app.

Usage:  python -X utf8 scripts/generate_thumbnail.py            # write assets/*
        python -X utf8 scripts/generate_thumbnail.py --check    # diff against existing, exit 1 if stale
"""
import argparse
import json
import math
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_graph import DOMAIN_COLORS, DOMAIN_LABELS  # noqa: E402  (single source of truth)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, "data", "entries.json")
ASSETS = os.path.join(ROOT, "assets")

TIER_R = {"entry": 4.0, "core": 5.2, "deep": 6.4}
BG = "#0b0e14"
REL_EDGE = "#5c6577"
HUB_THRESHOLD = 12          # nodes with degree >= this get labels
FONT = "'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"


def layout(nodes, edges, by_id, domains):
    """Deterministic seeded scatter + force layout (matches graph.html's forces)."""
    rng = random.Random(7)
    n_dom = len(domains)
    centers = {}
    for i, d in enumerate(domains):
        a = (i / n_dom) * math.pi * 2 - math.pi / 2
        centers[d["id"]] = {"x": math.cos(a) * 300, "y": math.sin(a) * 300}
    per_dom = Counter(n["domain"] for n in nodes)
    for n in nodes:
        c = centers[n["domain"]]
        a = rng.uniform(0, math.pi * 2)
        r = rng.uniform(0, 1) ** 0.5 * (26 + 1.15 * per_dom[n["domain"]])
        n["x"] = c["x"] + math.cos(a) * r
        n["y"] = c["y"] + math.sin(a) * r
        n["vx"] = n["vy"] = 0.0
    for _ in range(200):
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                a, b = nodes[i], nodes[j]
                dx, dy = a["x"] - b["x"], a["y"] - b["y"]
                d2 = dx * dx + dy * dy or 1.0
                d = math.sqrt(d2)
                f = min(2600 / d2, 26)
                a["vx"] += (dx / d) * f; a["vy"] += (dy / d) * f
                b["vx"] -= (dx / d) * f; b["vy"] -= (dy / d) * f
        for l in edges:
            a, b = by_id[l["source"]], by_id[l["target"]]
            dx, dy = b["x"] - a["x"], b["y"] - a["y"]
            d = math.sqrt(dx * dx + dy * dy) or 1.0
            f = (d - 62) * 0.06
            a["vx"] += (dx / d) * f; a["vy"] += (dy / d) * f
            b["vx"] -= (dx / d) * f; b["vy"] -= (dy / d) * f
        for n in nodes:
            c = centers[n["domain"]]
            n["vx"] += (c["x"] - n["x"]) * 0.004
            n["vy"] += (c["y"] - n["y"]) * 0.004
            n["vx"] *= 0.86; n["vy"] *= 0.86
            sp = math.sqrt(n["vx"] ** 2 + n["vy"] ** 2)
            if sp > 6.0:
                n["vx"] = n["vx"] / sp * 6.0; n["vy"] = n["vy"] / sp * 6.0
            n["x"] += n["vx"]; n["y"] += n["vy"]
    return nodes


def radius(n):
    return TIER_R[n["tier"]] * (1 + 0.06 * math.log2(n["degree"] + 2))


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#39;"))


def thumb_svg(nodes, edges, by_id, domains, stats):
    xs = [n["x"] for n in nodes]
    ys = [n["y"] for n in nodes]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    W, H = 1280, 800
    s = min((W - 120) / (maxx - minx), (H - 220) / (maxy - miny))
    tx = W / 2 - (minx + maxx) / 2 * s
    ty = H / 2 - (miny + maxy) / 2 * s

    P = []
    P.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
             f'viewBox="0 0 {W} {H}" role="img" '
             f'aria-label="AI Alignment Field Index network — {stats["nodes"]} entries, '
             f'{stats["edges"]} cross-links">')
    P.append(f'  <rect width="{W}" height="{H}" fill="{BG}" rx="14"/>')
    P.append(f'  <text x="64" y="58" font-family="{FONT}" font-size="30" font-weight="700" '
             f'fill="#eef2fb">AI Alignment Field Index</text>')
    P.append(f'  <text x="66" y="86" font-family="{FONT}" font-size="16" fill="#8b94a7">'
             f'{stats["nodes"]} entries · {stats["edges"]} cross-links · {stats["domains"]} domains · '
             f'{stats["subtopics"]} subtopics — prerequisite &amp; related-work graph</text>')
    # edge key, right-aligned on the subtitle line
    P.append(f'  <line x1="{W - 258}" y1="82" x2="{W - 216}" y2="82" '
             f'stroke="#7aa2f7" stroke-opacity="0.6" stroke-width="2"/>')
    P.append(f'  <text x="{W - 208}" y="86" font-family="{FONT}" font-size="13" '
             f'fill="#8b94a7">prerequisite</text>')
    P.append(f'  <line x1="{W - 104}" y1="82" x2="{W - 62}" y2="82" '
             f'stroke="{REL_EDGE}" stroke-opacity="0.6" stroke-width="2" stroke-dasharray="4 4"/>')
    P.append(f'  <text x="{W - 54}" y="86" font-family="{FONT}" font-size="13" '
             f'fill="#8b94a7">related</text>')
    # graph
    P.append(f'  <g transform="translate({tx:.1f},{ty:.1f}) scale({s:.4f})">')
    for l in edges:
        a, b = by_id[l["source"]], by_id[l["target"]]
        if l["type"] == "prereq":
            stroke, op, dash = "#7aa2f7", 0.4, ""
        else:
            stroke, op, dash = REL_EDGE, 0.22, ' stroke-dasharray="4 4"'
        P.append(f'    <line x1="{a["x"]:.1f}" y1="{a["y"]:.1f}" x2="{b["x"]:.1f}" y2="{b["y"]:.1f}" '
                 f'stroke="{stroke}" stroke-opacity="{op}" stroke-width="1.1"{dash}/>')
    for n in nodes:
        r = radius(n)
        P.append(f'    <circle cx="{n["x"]:.1f}" cy="{n["y"]:.1f}" r="{r:.1f}" '
                 f'fill="{DOMAIN_COLORS[n["domain"]]}" stroke="#0b0e14" stroke-width="0.8" '
                 f'stroke-opacity="0.55"/>')
    for n in nodes:
        if n["degree"] < HUB_THRESHOLD:
            continue
        label = n["title"] if len(n["title"]) <= 34 else n["title"][:33] + "…"
        y = n["y"] - radius(n) - 6
        P.append(f'    <text x="{n["x"]:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="13" '
                 f'font-weight="600" fill="#dfe6f5" text-anchor="middle" '
                 f'paint-order="stroke" stroke="#0b0e14" stroke-width="3">{esc(label)}</text>')
    P.append("  </g>")
    # legend: two rows of five domain chips (fixed cell widths, no overflow)
    cols = 5
    cell = (W - 128) / cols
    for idx, d in enumerate(domains):
        col, row = idx % cols, idx // cols
        x = 64 + col * cell
        y = H - 78 + row * 30
        P.append(f'    <rect x="{x:.0f}" y="{y:.0f}" width="10" height="10" rx="2" fill="{d["color"]}"/>')
        P.append(f'    <text x="{x + 16:.0f}" y="{y + 9:.0f}" font-family="{FONT}" font-size="12" '
                 f'fill="#8b94a7">{esc(d["label"])}</text>')
    P.append("</svg>")
    return "\n".join(P)


def measure(text, size=11):
    """Rough per-char width estimate for badge sizing (over-estimates slightly)."""
    w = 0
    for c in text:
        if c == " ":
            w += 0.32 * size
        elif c.isupper() or c.isdigit():
            w += 0.62 * size
        else:
            w += 0.5 * size
    return w


def badge_svg(label, value, color):
    """Shields.io-style flat badge: label on dark, value on color."""
    pad = 6
    lw = measure(label) + pad * 2
    vw = measure(value) + pad * 2
    W = lw + vw
    P = []
    P.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="20" '
             f'viewBox="0 0 {W:.0f} 20" role="img" aria-label="{esc(label)}: {esc(value)}">')
    P.append(f'  <title>{esc(label)}: {esc(value)}</title>')
    P.append(f'  <rect width="{W:.0f}" height="20" fill="#3b4252" rx="3"/>')
    P.append(f'  <path d="M {lw:.0f} 0 H {W - 3:.0f} Q {W:.0f} 0 {W:.0f} 3 V 17 Q {W:.0f} 20 '
             f'{W - 3:.0f} 20 H {lw:.0f} Z" fill="{color}"/>')
    P.append(f'  <text x="{pad}" y="14" font-family="DejaVu Sans, Verdana, Arial, sans-serif" '
             f'font-size="11" fill="#e8ecf5">{esc(label)}</text>')
    P.append(f'  <text x="{lw + pad}" y="14" font-family="DejaVu Sans, Verdana, Arial, sans-serif" '
             f'font-size="11" fill="#ffffff" font-weight="600">{esc(value)}</text>')
    P.append("</svg>")
    return "\n".join(P)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="render and compare against existing assets without writing; exit 1 if stale")
    args = ap.parse_args()

    with open(ENTRIES, "r", encoding="utf-8") as fh:
        catalog = json.load(fh)
    ids = {e["id"] for e in catalog}
    live = [e for e in catalog if e["status"] != "dead"]

    nodes = [{"id": e["id"], "title": e["title"], "domain": e["domain"], "tier": e["tier"],
              "degree": 0, "x": 0.0, "y": 0.0, "vx": 0.0, "vy": 0.0} for e in live]
    by_id = {n["id"]: n for n in nodes}   # maps to the enriched node dicts (has x/y)

    edges = []
    seen = set()
    deg = Counter()
    for e in live:
        for p in e.get("prerequisites") or []:
            if p in ids and p != e["id"]:
                edges.append({"source": e["id"], "target": p, "type": "prereq"})
                deg[e["id"]] += 1; deg[p] += 1
        for r in e.get("related") or []:
            if r in ids and r != e["id"]:
                k = tuple(sorted((e["id"], r)))
                if k in seen:
                    continue
                seen.add(k)
                edges.append({"source": e["id"], "target": r, "type": "related"})
                deg[e["id"]] += 1; deg[r] += 1
    for n in nodes:
        n["degree"] = deg.get(n["id"], 0)

    domains = [{"id": d, "label": DOMAIN_LABELS[d], "color": DOMAIN_COLORS[d]}
               for d in DOMAIN_LABELS if any(n["domain"] == d for n in nodes)]
    layout(nodes, edges, by_id, domains)

    n_prereq = sum(1 for e in edges if e["type"] == "prereq")
    n_rel = len(edges) - n_prereq
    n_subtopics = len({s for e in live for s in (e.get("subtopics") or [])})
    stats = {
        "nodes": len(nodes),
        "edges": len(edges),
        "domains": len(domains),
        "subtopics": n_subtopics,
    }

    rendered = {
        "graph-thumbnail.svg": thumb_svg(nodes, edges, by_id, domains, stats),
        "badge-entries.svg": badge_svg("entries", str(len(nodes)), "#7aa2f7"),
        "badge-crosslinks.svg": badge_svg("cross-links", f"{len(edges)} ({n_prereq}+{n_rel})", "#56d4c4"),
        "badge-domains.svg": badge_svg("domains", str(len(domains)), "#8bc75e"),
        "badge-subtopics.svg": badge_svg("subtopics", str(n_subtopics), "#c792ea"),
    }

    if args.check:
        stale = []
        for name, content in rendered.items():
            path = os.path.join(ASSETS, name)
            if not os.path.exists(path) or open(path, encoding="utf-8").read() != content:
                stale.append(name)
        if stale:
            print(f"STALE: {', '.join(stale)} — run `python scripts/generate_thumbnail.py`")
            sys.exit(1)
        print(f"OK: {len(rendered)} assets match data/entries.json")
        sys.exit(0)

    os.makedirs(ASSETS, exist_ok=True)
    for name, content in rendered.items():
        with open(os.path.join(ASSETS, name), "w", encoding="utf-8") as fh:
            fh.write(content)
    print(f"GENERATED {len(rendered)} assets in assets/: {len(nodes)} nodes, {n_prereq}+{n_rel} edges, "
          f"{len(domains)} domains, {n_subtopics} subtopics")


if __name__ == "__main__":
    main()
