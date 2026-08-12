#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_graph.py — build the interactive cross-link network for the index.

Reads data/entries.json and emits a single, fully self-contained `graph.html`
at the repo root: nodes = entries, edges = prerequisites (directed) + related
(undirected, deduped). No external dependencies / CDN — works offline via file://.

Usage:  python -X utf8 scripts/generate_graph.py
"""
import json
import os
import sys
from collections import Counter
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, "data", "entries.json")
OUT = os.path.join(ROOT, "graph.html")

DOMAIN_LABELS = {
    "entry-tier": "Entry Tier",
    "macrostrategy": "Macrostrategy & X-Risk",
    "agent-foundations": "Agent Foundations & Decision Theory",
    "interpretability": "Interpretability",
    "oversight-rlhf": "Scalable Oversight & RLHF",
    "evals-benchmarks": "Evals & Benchmarks",
    "governance-policy": "Governance & Policy",
    "security-redteam": "Security & Red-teaming",
    "philosophy-values": "Philosophy & Value Alignment",
    "field-infrastructure": "Field Infrastructure",
}

DOMAIN_COLORS = {
    "agent-foundations": "#4d9de0",
    "entry-tier": "#e8c35a",
    "evals-benchmarks": "#e75ba0",
    "field-infrastructure": "#8bc75e",
    "governance-policy": "#8a7ce0",
    "interpretability": "#3cc5d8",
    "macrostrategy": "#ef8a4d",
    "oversight-rlhf": "#48c9b0",
    "philosophy-values": "#c792ea",
    "security-redteam": "#e05c5c",
}

TIER_RADII = {"entry": 4.5, "core": 6.5, "deep": 8.5}


def main():
    with open(ENTRIES, encoding="utf-8") as fh:
        entries = json.load(fh)

    ids = {e["id"] for e in entries}

    # ---- nodes ----
    nodes = []
    for e in entries:
        nodes.append({
            "id": e["id"],
            "title": e["title"],
            "authors": e.get("authors") or [],
            "year": e.get("year"),
            "url": e.get("url", ""),
            "type": e.get("type", ""),
            "domain": e["domain"],
            "subtopics": e.get("subtopics") or [],
            "tier": e.get("tier", "core"),
            "summary": e.get("summary", ""),
            "why_it_matters": e.get("why_it_matters", ""),
        })

    # ---- edges ----
    edges = []
    seen_related = set()
    for e in entries:
        for p in e.get("prerequisites") or []:
            if p in ids and p != e["id"]:
                edges.append({"source": e["id"], "target": p, "type": "prereq"})
        for r in e.get("related") or []:
            if r in ids and r != e["id"]:
                key = tuple(sorted((e["id"], r)))
                if key in seen_related:
                    continue
                seen_related.add(key)
                edges.append({"source": e["id"], "target": r, "type": "related"})

    # ---- degree / stats ----
    deg = Counter()
    for ed in edges:
        deg[ed["source"]] += 1
        deg[ed["target"]] += 1
    for n in nodes:
        n["degree"] = deg.get(n["id"], 0)

    n_prereq = sum(1 for ed in edges if ed["type"] == "prereq")
    n_rel = len(edges) - n_prereq
    avg = sum(n["degree"] for n in nodes) / len(nodes)
    top = sorted(nodes, key=lambda n: n["degree"], reverse=True)
    hub = top[0]
    byid = {n["id"]: n for n in nodes}
    top_hubs = [{"id": n["id"], "title": n["title"], "degree": n["degree"]} for n in top[:6]]

    domains = []
    counts = Counter(n["domain"] for n in nodes)
    for d in sorted(DOMAIN_LABELS.keys(), key=lambda d: DOMAIN_LABELS[d]):
        if d not in counts:
            continue
        domains.append({
            "id": d,
            "label": DOMAIN_LABELS[d],
            "color": DOMAIN_COLORS[d],
            "count": counts[d],
        })

    stats = {
        "nodes": len(nodes),
        "edges": len(edges),
        "prereq": n_prereq,
        "related": n_rel,
        "avg_degree": round(avg, 1),
        "max_degree": hub["degree"],
        "hub_id": hub["id"],
        "hub_title": hub["title"],
        "isolates": sum(1 for n in nodes if n["degree"] == 0),
        "top_hubs": top_hubs,
    }

    data = {
        "nodes": nodes,
        "edges": edges,
        "domains": domains,
        "stats": stats,
        "generated": date.today().isoformat(),
    }

    data_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # Hardening for inlining into a <script> block: escape the only sequences that
    # could break out of the JS object literal / script element.
    data_json = (data_json
                 .replace("</", "<\\/")
                 .replace("\u2028", "\\u2028")
                 .replace("\u2029", "\\u2029"))

    html = TEMPLATE.replace("@@DATA_JSON@@", data_json)

    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)

    print(f"graph.html written: {len(nodes)} nodes, {len(edges)} edges "
          f"({n_prereq} prereq / {n_rel} related), avg degree {avg:.1f}, "
          f"max {hub['degree']} ({hub['id']}), {len(html):,} bytes")
    return 0


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Alignment Field Index — Cross-Link Network</title>
<meta name="description" content="Interactive network of the Unified AI Alignment Field Index: 277 entries connected by prerequisites and related-work edges.">
<style>
  :root {
    --bg: #0b0e14;
    --panel: #12161f;
    --panel-2: #171c28;
    --border: #232b3d;
    --text: #d5dcec;
    --muted: #8b94a7;
    --faint: #5c6577;
    --accent: #7aa2f7;
    --accent-2: #56d4c4;
    --danger: #e05c5c;
    --mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; }
  body {
    background: var(--bg);
    color: var(--text);
    font: 14px/1.45 ui-sans-serif, -apple-system, "Segoe UI", Roboto, Inter, Helvetica, Arial, sans-serif;
    overflow: hidden;
  }
  ::-webkit-scrollbar { width: 9px; height: 9px; }
  ::-webkit-scrollbar-thumb { background: #2c3550; border-radius: 5px; }
  ::-webkit-scrollbar-track { background: transparent; }

  /* ---------- header ---------- */
  header {
    position: relative; z-index: 30;
    display: flex; align-items: center; gap: 18px;
    padding: 10px 18px;
    background: linear-gradient(180deg, #10141d, #0d1119);
    border-bottom: 1px solid var(--border);
    flex-wrap: wrap;
  }
  .brand { display: flex; align-items: center; gap: 10px; min-width: 0; }
  .brand .logo {
    width: 30px; height: 30px; border-radius: 8px; flex: none;
    background: conic-gradient(from 210deg, #4d9de0, #e75ba0, #8bc75e, #e8c35a, #c792ea, #48c9b0, #e05c5c, #ef8a4d, #4d9de0);
    box-shadow: 0 0 14px rgba(122, 162, 247, 0.35);
  }
  .brand h1 { font-size: 15px; font-weight: 700; letter-spacing: 0.2px; white-space: nowrap; }
  .brand .sub { font-size: 11.5px; color: var(--muted); white-space: nowrap; }
  .controls { display: flex; align-items: center; gap: 8px; margin-left: auto; flex-wrap: wrap; }
  .searchwrap { position: relative; display: flex; align-items: center; }
  .searchwrap svg { position: absolute; left: 9px; width: 14px; height: 14px; stroke: var(--faint); pointer-events: none; }
  #search {
    width: 250px; max-width: 34vw;
    background: var(--panel); border: 1px solid var(--border); border-radius: 8px;
    color: var(--text); padding: 7px 10px 7px 28px; font-size: 13px; outline: none;
    transition: border-color .15s, box-shadow .15s;
  }
  #search:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(122,162,247,0.18); }
  #search.dimmed { border-color: #4a5468; }
  #matchcount { position: absolute; right: 8px; font-size: 11px; color: var(--accent); font-family: var(--mono); pointer-events: none; }
  .btn {
    background: var(--panel); color: var(--text); border: 1px solid var(--border);
    border-radius: 8px; padding: 7px 11px; font-size: 12.5px; cursor: pointer;
    transition: background .15s, border-color .15s, transform .05s; user-select: none;
    display: inline-flex; align-items: center; gap: 6px;
  }
  .btn:hover { background: var(--panel-2); border-color: #35405c; }
  .btn:active { transform: translateY(1px); }
  .btn.on { background: rgba(122,162,247,0.16); border-color: var(--accent); color: #c3d3ff; }
  .btn kbd { font-family: var(--mono); font-size: 10px; color: var(--faint); border: 1px solid var(--border); border-radius: 4px; padding: 0 4px; }

  /* ---------- stats bar ---------- */
  #statsbar {
    position: relative; z-index: 20;
    display: flex; align-items: center; gap: 16px; flex-wrap: wrap;
    padding: 7px 18px; font-size: 12px; color: var(--muted);
    background: #0d1119; border-bottom: 1px solid var(--border);
    font-family: var(--mono);
  }
  #statsbar b { color: var(--text); font-weight: 600; }
  #statsbar .sep { color: #2b3550; }
  #statsbar .live { color: var(--accent-2); }
  #statsbar .hub { color: var(--text); max-width: 320px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: inline-block; vertical-align: bottom; }

  /* ---------- canvas ---------- */
  #wrap { position: absolute; inset: 0; }
  #canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; cursor: grab; }
  #canvas.dragging { cursor: grabbing; }
  #hint {
    position: absolute; left: 18px; bottom: 46px; z-index: 5;
    font-size: 11.5px; color: var(--faint); pointer-events: none;
    background: rgba(11,14,20,0.6); padding: 5px 9px; border-radius: 7px; border: 1px solid #1a2130;
  }
  #empty {
    display: none; position: absolute; left: 50%; top: 46%; transform: translate(-50%,-50%);
    text-align: center; color: var(--faint); font-size: 14px; z-index: 5; pointer-events: none;
  }
  #empty b { display: block; font-size: 16px; color: var(--muted); margin-bottom: 6px; }

  /* ---------- tooltip ---------- */
  #tooltip {
    position: fixed; z-index: 60; max-width: 340px; pointer-events: none;
    background: rgba(16,20,30,0.96); border: 1px solid #2e3a55; border-radius: 10px;
    padding: 10px 12px; box-shadow: 0 10px 34px rgba(0,0,0,0.55);
    opacity: 0; transition: opacity .12s; backdrop-filter: blur(6px);
  }
  #tooltip.show { opacity: 1; }
  #tooltip .tt-title { font-size: 13px; font-weight: 700; color: #eef2fb; line-height: 1.35; margin-bottom: 4px; }
  #tooltip .tt-meta { font-size: 11px; color: var(--muted); margin-bottom: 6px; }
  #tooltip .tt-meta .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; vertical-align: -0.5px; }
  #tooltip .tt-sum { font-size: 12px; color: #b9c2d6; }
  #tooltip .tt-chips { margin-top: 7px; display: flex; gap: 5px; flex-wrap: wrap; }
  #tooltip .chip { font-size: 10px; font-family: var(--mono); color: var(--muted); border: 1px solid #2b3550; padding: 2px 6px; border-radius: 20px; }

  /* ---------- detail panel ---------- */
  #panel {
    position: fixed; top: 0; right: 0; bottom: 0; z-index: 50; width: 380px; max-width: 92vw;
    background: rgba(15,19,28,0.97); border-left: 1px solid var(--border);
    transform: translateX(105%); transition: transform .22s cubic-bezier(.3,.7,.3,1);
    display: flex; flex-direction: column; backdrop-filter: blur(8px);
  }
  #panel.open { transform: translateX(0); box-shadow: -18px 0 48px rgba(0,0,0,0.5); }
  #panel .p-head { padding: 14px 16px 12px; border-bottom: 1px solid var(--border); position: relative; }
  #panel .p-title { font-size: 14.5px; font-weight: 700; line-height: 1.4; padding-right: 26px; }
  #panel .p-meta { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 8px; }
  #panel .p-meta .chip {
    font-size: 10.5px; font-family: var(--mono); color: var(--muted);
    border: 1px solid #2b3550; padding: 2px 7px; border-radius: 20px; background: #10141d;
  }
  #panel .p-meta .chip.dom { color: #fff; font-weight: 600; }
  #panel #pclose {
    position: absolute; top: 10px; right: 10px; width: 26px; height: 26px; border-radius: 7px;
    background: transparent; color: var(--muted); border: 1px solid transparent; cursor: pointer; font-size: 15px; line-height: 1;
  }
  #panel #pclose:hover { background: var(--panel-2); color: var(--text); }
  #panel .p-body { flex: 1; overflow-y: auto; padding: 14px 16px 20px; }
  #panel .p-body h4 {
    font-size: 10.5px; letter-spacing: 1.2px; text-transform: uppercase; color: var(--faint);
    margin: 16px 0 7px; font-weight: 700;
  }
  #panel .p-body h4:first-child { margin-top: 0; }
  #panel .p-body p { font-size: 12.5px; color: #c3cbdd; }
  #panel .p-url {
    display: block; margin-top: 14px; padding: 9px 12px; border-radius: 9px;
    background: var(--accent); color: #0b0e14; text-decoration: none; font-weight: 700;
    font-size: 12.5px; text-align: center; transition: filter .15s;
  }
  #panel .p-url:hover { filter: brightness(1.12); }
  #panel .p-url small { display: block; font-weight: 400; opacity: 0.75; margin-top: 2px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  #panel .links { list-style: none; display: flex; flex-direction: column; gap: 5px; }
  #panel .links li {
    background: var(--panel); border: 1px solid var(--border); border-radius: 8px;
    padding: 7px 9px; font-size: 12px; cursor: pointer; display: flex; align-items: center; gap: 8px;
    transition: border-color .12s, background .12s;
  }
  #panel .links li:hover { border-color: var(--accent); background: var(--panel-2); }
  #panel .links .l-dot { width: 9px; height: 9px; border-radius: 50%; flex: none; }
  #panel .links .l-title { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  #panel .links .l-arrow { margin-left: auto; color: var(--faint); font-size: 11px; flex: none; }

  /* ---------- search dropdown ---------- */
  #results {
    position: absolute; top: calc(100% + 6px); left: 0; width: 320px; max-height: 320px; overflow-y: auto;
    background: rgba(16,20,30,0.98); border: 1px solid var(--border); border-radius: 10px;
    box-shadow: 0 14px 40px rgba(0,0,0,0.55); z-index: 40; display: none;
  }
  #results.show { display: block; }
  #results .r-item {
    padding: 8px 11px; cursor: pointer; display: flex; gap: 9px; align-items: center;
    border-bottom: 1px solid #1a2130; font-size: 12px;
  }
  #results .r-item:last-child { border-bottom: none; }
  #results .r-item:hover, #results .r-item.active { background: rgba(122,162,247,0.12); }
  #results .r-dot { width: 9px; height: 9px; border-radius: 50%; flex: none; }
  #results .r-title { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; }
  #results .r-meta { font-size: 10px; color: var(--faint); font-family: var(--mono); flex: none; }

  /* ---------- filters / legend ---------- */
  .floatpanel {
    position: fixed; z-index: 40; background: rgba(15,19,28,0.94); border: 1px solid var(--border);
    border-radius: 12px; padding: 12px 14px; backdrop-filter: blur(8px);
    box-shadow: 0 12px 36px rgba(0,0,0,0.45);
  }
  #legend { left: 18px; bottom: 18px; max-width: 300px; }
  #legend h3, #filters h3 {
    font-size: 10.5px; letter-spacing: 1.2px; text-transform: uppercase; color: var(--faint);
    margin-bottom: 9px; font-weight: 700; display: flex; align-items: center; justify-content: space-between; cursor: pointer;
  }
  #legend .lg-sec { margin-bottom: 10px; }
  #legend .lg-sec:last-child { margin-bottom: 0; }
  #legend .lg-title { font-size: 10px; color: var(--faint); margin-bottom: 5px; font-family: var(--mono); }
  #legend .lg-row { display: flex; align-items: center; gap: 7px; font-size: 11.5px; padding: 2px 0; color: var(--muted); cursor: pointer; }
  #legend .lg-row:hover { color: var(--text); }
  #legend .lg-row .dot { width: 10px; height: 10px; border-radius: 3px; flex: none; }
  #legend .lg-row .n { margin-left: auto; font-family: var(--mono); font-size: 10.5px; color: var(--faint); }
  #legend .lg-row.dim { opacity: 0.35; }
  #legend .lg-swatches { display: flex; gap: 9px; align-items: flex-end; }
  #legend .lg-swatches .sw { display: flex; flex-direction: column; align-items: center; gap: 3px; font-size: 9.5px; color: var(--faint); font-family: var(--mono); }
  #legend .edge-key { display: flex; flex-direction: column; gap: 5px; font-size: 11.5px; color: var(--muted); }
  #legend .edge-key .ek { display: flex; align-items: center; gap: 8px; }
  #legend .edge-key .ek svg { width: 34px; height: 8px; flex: none; }
  #filters { right: 18px; bottom: 18px; width: 264px; }
  #filters .tier-row { display: flex; gap: 6px; margin-bottom: 12px; }
  .tier-chip {
    flex: 1; text-align: center; padding: 6px 0; border-radius: 8px; cursor: pointer; font-size: 11.5px;
    border: 1px solid var(--border); background: var(--panel); color: var(--muted); transition: all .12s; user-select: none;
  }
  .tier-chip:hover { border-color: #35405c; color: var(--text); }
  .tier-chip.on { background: rgba(122,162,247,0.16); border-color: var(--accent); color: #c3d3ff; font-weight: 600; }
  #filters .dom-title { font-size: 10px; color: var(--faint); margin-bottom: 5px; font-family: var(--mono); }
  #domgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; max-height: 250px; overflow-y: auto; padding-right: 3px; }
  .dom-chip {
    display: flex; align-items: center; gap: 6px; font-size: 11px; padding: 5px 7px; border-radius: 7px;
    border: 1px solid var(--border); background: var(--panel); color: var(--muted); cursor: pointer; user-select: none; transition: all .12s;
    overflow: hidden;
  }
  .dom-chip .dot { width: 8px; height: 8px; border-radius: 2px; flex: none; }
  .dom-chip .dn { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .dom-chip.on { color: var(--text); border-color: #35405c; background: var(--panel-2); }
  .dom-chip.off { opacity: 0.35; }
  #filters .f-actions { display: flex; gap: 6px; margin-top: 10px; }
  #filters .f-actions .btn { flex: 1; justify-content: center; }

  #toast {
    position: fixed; left: 50%; bottom: 26px; transform: translateX(-50%) translateY(8px);
    z-index: 70; background: rgba(20,26,40,0.97); border: 1px solid #2e3a55; color: var(--text);
    padding: 9px 16px; border-radius: 10px; font-size: 12.5px; opacity: 0; pointer-events: none;
    transition: opacity .18s, transform .18s; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
  }
  #toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
  #toast b { color: var(--accent); }

  footer {
    position: fixed; right: 16px; bottom: 8px; z-index: 5; font-size: 10px; color: #3d4659;
    font-family: var(--mono); pointer-events: none;
  }

  @media (max-width: 760px) {
    .brand .sub { display: none; }
    #search { width: 150px; }
    #legend { display: none; }
  }
</style>
</head>
<body>

<header>
  <div class="brand">
    <div class="logo"></div>
    <div>
      <h1>AI Alignment Field Index — Cross-Link Network</h1>
      <div class="sub">prerequisite &amp; related-work graph · generated from data/entries.json</div>
    </div>
  </div>
  <div class="controls">
    <div class="searchwrap">
      <svg viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.2" y2="16.2"/></svg>
      <input id="search" type="text" placeholder="Search title, author, id…  ( / )" autocomplete="off" spellcheck="false">
      <span id="matchcount"></span>
      <div id="results"></div>
    </div>
    <button class="btn" id="btnFit" title="Fit graph to view (F)">⛶ Fit</button>
    <button class="btn" id="btnRelayout" title="Re-run layout">⟳ Layout</button>
    <button class="btn" id="btnFocus" title="Isolate the selected node's neighborhood">◎ Focus</button>
    <button class="btn" id="btnLegend" title="Toggle legend &amp; filters (L)">⚙ Legend</button>
  </div>
</header>

<div id="statsbar">
  <span><b id="st-nodes">0</b> nodes</span><span class="sep">·</span>
  <span><b id="st-edges">0</b> edges</span><span class="sep">·</span>
  <span><b id="st-prereq">0</b> prerequisite</span><span class="sep">·</span>
  <span><b id="st-related">0</b> related</span><span class="sep">·</span>
  <span>avg degree <b id="st-avg">–</b></span><span class="sep">·</span>
  <span>hub <span class="hub" id="st-hub">–</span></span>
  <span class="live" id="st-visible"></span>
</div>

<div id="wrap">
  <canvas id="canvas"></canvas>
  <div id="hint">drag to pan · scroll to zoom · hover a node · click for details · drag nodes to explore</div>
  <div id="empty"><b>No nodes match the current filters</b>reset filters or clear the search</div>
  <footer>MIT · scripts/generate_graph.py · data/entries.json</footer>
</div>

<div id="tooltip"></div>

<div id="panel">
  <div class="p-head">
    <div class="p-title" id="p-title"></div>
    <div class="p-meta" id="p-meta"></div>
    <button id="pclose" title="Close (Esc)">✕</button>
  </div>
  <div class="p-body" id="p-body"></div>
</div>

<div class="floatpanel" id="filters" style="display:none">
  <h3>Filters</h3>
  <div class="tier-row" id="tierrow"></div>
  <div class="dom-title">Domains — click to toggle</div>
  <div id="domgrid"></div>
  <div class="f-actions">
    <button class="btn" id="btnAll">Select all</button>
    <button class="btn" id="btnNone">Clear</button>
  </div>
</div>

<div class="floatpanel" id="legend">
  <h3>Legend</h3>
  <div class="lg-sec">
    <div class="lg-title">DOMAINS</div>
    <div id="lgdom"></div>
  </div>
  <div class="lg-sec">
    <div class="lg-title">TIER → SIZE</div>
    <div class="lg-swatches" id="lgsw"></div>
  </div>
  <div class="lg-sec">
    <div class="lg-title">EDGES</div>
    <div class="edge-key">
      <div class="ek"><svg viewBox="0 0 34 8"><line x1="1" y1="4" x2="33" y2="4" stroke="#7aa2f7" stroke-width="2"/><polygon points="33,4 28,1.6 28,6.4" fill="#7aa2f7"/></svg> prerequisite <span style="color:var(--faint)">(read this first)</span></div>
      <div class="ek"><svg viewBox="0 0 34 8"><line x1="1" y1="4" x2="33" y2="4" stroke="#5c6577" stroke-width="2" stroke-dasharray="4 3"/></svg> related / critique / rebuttal</div>
    </div>
  </div>
</div>

<div id="toast"></div>

<script>
"use strict";
/* ================= data ================= */
const DATA = @@DATA_JSON@@;

const nodes = DATA.nodes.map((n, i) => ({ ...n, idx: i, x: 0, y: 0, vx: 0, vy: 0, hidden: false }));
const links = DATA.edges;
const byId = new Map(nodes.map(n => [n.id, n]));
const domById = new Map(DATA.domains.map(d => [d.id, d]));
const tierLabel = { entry: "entry", core: "core", deep: "deep" };

const state = {
  selTiers: new Set(["entry", "core", "deep"]),
  selDoms: new Set(DATA.domains.map(d => d.id)),
  query: "",
  selected: null,
  hovered: null,
  focus: false,
  legendOpen: true,
  showLabels: false,
};

/* ================= canvas ================= */
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
const view = { x: 0, y: 0, k: 1 };
let W = 0, H = 0, DPR = Math.min(window.devicePixelRatio || 1, 2);

function resize() {
  W = canvas.clientWidth; H = canvas.clientHeight;
  canvas.width = Math.round(W * DPR); canvas.height = Math.round(H * DPR);
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  render();
}
window.addEventListener("resize", resize);

/* ================= simulation ================= */
const C = { rep: 2600, link: 0.12, cluster: 0.006, rest: 62, damp: 0.86, seedR: 430 };
let temp = 1;

// cluster centers per domain, arranged on a ring
const domCenters = new Map();
(function seed() {
  const nDom = DATA.domains.length;
  DATA.domains.forEach((d, i) => {
    const a = (i / nDom) * Math.PI * 2 - Math.PI / 2;
    domCenters.set(d.id, { x: Math.cos(a) * C.seedR * 1.25, y: Math.sin(a) * C.seedR });
  });
  nodes.forEach((n, i) => {
    const c = domCenters.get(n.domain) || { x: 0, y: 0 };
    const a = Math.random() * Math.PI * 2, r = Math.random() * 70 + 14;
    n.x = c.x + Math.cos(a) * r; n.y = c.y + Math.sin(a) * r;
    n.vx = 0; n.vy = 0;
  });
})();

function visible(n) { return !n.hidden; }

function tick() {
  const vis = nodes.filter(visible);
  // pairwise repulsion (Fr-Re)
  for (let i = 0; i < vis.length; i++) {
    const a = vis[i];
    for (let j = i + 1; j < vis.length; j++) {
      const b = vis[j];
      let dx = a.x - b.x, dy = a.y - b.y;
      let d2 = dx * dx + dy * dy;
      if (d2 < 1) { d2 = 1; dx = Math.random() - 0.5; dy = Math.random() - 0.5; }
      const d = Math.sqrt(d2);
      let f = C.rep / d2;
      if (f > 26) f = 26;
      const fx = (dx / d) * f, fy = (dy / d) * f;
      a.vx += fx; a.vy += fy; b.vx -= fx; b.vy -= fy;
    }
  }
  // springs
  for (const l of links) {
    const a = byId.get(l.source), b = byId.get(l.target);
    if (!a || !b || a.hidden || b.hidden) continue;
    const dx = b.x - a.x, dy = b.y - a.y;
    const d = Math.sqrt(dx * dx + dy * dy) || 1;
    const f = (d - C.rest) * C.link / 2 * temp;
    const fx = (dx / d) * f, fy = (dy / d) * f;
    a.vx += fx; a.vy += fy; b.vx -= fx; b.vy -= fy;
  }
  // gentle pull toward domain clusters
  for (const n of vis) {
    const c = domCenters.get(n.domain); if (!c) continue;
    const dx = c.x - n.x, dy = c.y - n.y;
    const d = Math.sqrt(dx * dx + dy * dy) || 1;
    const f = d * C.cluster * temp;
    n.vx += (dx / d) * f; n.vy += (dy / d) * f;
  }
  // integrate
  for (const n of vis) {
    n.vx *= C.damp; n.vy *= C.damp;
    const sp = Math.sqrt(n.vx * n.vx + n.vy * n.vy), mx = 7 * temp + 0.4;
    if (sp > mx) { n.vx = (n.vx / sp) * mx; n.vy = (n.vy / sp) * mx; }
    n.x += n.vx; n.y += n.vy;
  }
}

function reheat(t) { temp = Math.max(temp, t || 0.6); }

/* ================= layout helpers ================= */
function radius(n) {
  const base = TIER_R(n.tier);
  return base * (0.85 + 0.55 * Math.log2(n.degree + 2));
}
const TIER_R = t => ({ entry: 4.5, core: 6.5, deep: 8.5 })[t] || 6;

function nodeRect(n) { return radius(n) + 6; }
function hitTest(px, py) {
  const wx = (px - view.x) / view.k, wy = (py - view.y) / view.k;
  let best = null, bd = 1e9;
  for (const n of nodes) {
    if (n.hidden) continue;
    const dx = n.x - wx, dy = n.y - wy;
    const d = Math.sqrt(dx * dx + dy * dy);
    // screen-space pick tolerance: node radius + ~8px, converted to world units
    const rr = nodeRect(n) + 8 / view.k;
    if (d < rr && d < bd) { bd = d; best = n; }
  }
  return best;
}
function worldToScreen(n) { return { x: n.x * view.k + view.x, y: n.y * view.k + view.y }; }

function fitView() {
  const vis = nodes.filter(visible);
  if (!vis.length) return;
  let minX = 1e9, minY = 1e9, maxX = -1e9, maxY = -1e9;
  for (const n of vis) {
    const r = radius(n);
    if (n.x - r < minX) minX = n.x - r; if (n.x + r > maxX) maxX = n.x + r;
    if (n.y - r < minY) minY = n.y - r; if (n.y + r > maxY) maxY = n.y + r;
  }
  const pad = 70;
  const k = Math.min((W - pad * 2) / Math.max(maxX - minX, 1), (H - pad * 2) / Math.max(maxY - minY, 1), 1.6);
  view.k = Math.max(k, 0.12);
  view.x = W / 2 - ((minX + maxX) / 2) * view.k;
  view.y = H / 2 - ((minY + maxY) / 2) * view.k;
}
function focusNode(n) {
  view.k = 1.9;
  view.x = W / 2 - n.x * view.k;
  view.y = H / 2 - n.y * view.k;
}

/* ================= filters & search ================= */
function matches(n) {
  if (!state.selTiers.has(n.tier) || !state.selDoms.has(n.domain)) return false;
  if (!state.query) return true;
  const q = state.query.toLowerCase();
  return (n.title + " " + n.id + " " + n.authors.join(" ") + " " + n.subtopics.join(" ")).toLowerCase().includes(q);
}
function searchMatch(n) {
  if (!state.query) return true;
  const q = state.query.toLowerCase();
  return (n.title + " " + n.id + " " + n.authors.join(" ") + " " + n.subtopics.join(" ")).toLowerCase().includes(q);
}
function applyFilters() {
  let visC = 0;
  for (const n of nodes) {
    n.hidden = !matches(n);
    if (!n.hidden) visC++;
  }
  // if the selected node was filtered out, drop the stale selection
  if (state.selected && state.selected.hidden) {
    panel.classList.remove("open");
    state.selected = null;
  }
  const eCount = links.filter(l => {
    const a = byId.get(l.source), b = byId.get(l.target);
    return a && b && !a.hidden && !b.hidden;
  }).length;
  document.getElementById("st-visible").textContent = visC + " shown";
  document.getElementById("empty").style.display = visC ? "none" : "block";
  updateLegendDim();
  reheat(0.5);
  render();
  return { nodes: visC, edges: eCount };
}

/* ================= rendering ================= */
const col = (hex, a) => {
  const r = parseInt(hex.slice(1, 3), 16), g = parseInt(hex.slice(3, 5), 16), b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r},${g},${b},${a})`;
};

function draw() {
  ctx.save();
  ctx.setTransform(DPR * view.k, 0, 0, DPR * view.k, DPR * view.x, DPR * view.y);

  const q = state.query.toLowerCase();
  const hl = new Set();
  if (state.hovered) { hl.add(state.hovered.id); for (const l of links) { if (l.source === state.hovered.id) hl.add(l.target); if (l.target === state.hovered.id) hl.add(l.source); } }
  if (state.selected) { hl.add(state.selected.id); for (const l of links) { if (l.source === state.selected.id) hl.add(l.target); if (l.target === state.selected.id) hl.add(l.source); } }

  // edges
  ctx.lineCap = "round";
  for (const l of links) {
    const a = byId.get(l.source), b = byId.get(l.target);
    if (!a || !b || a.hidden || b.hidden) continue;
    const hot = hl.has(a.id) && hl.has(b.id) && (state.selected || state.hovered);
    const isPrereq = l.type === "prereq";
    const dc = domById.get(a.domain) || DATA.domains[0];
    let alpha = isPrereq ? 0.32 : 0.13;
    if (hot) alpha = isPrereq ? 0.85 : 0.55;
    ctx.strokeStyle = col(isPrereq ? dc.color : "#6b7590", alpha);
    ctx.lineWidth = isPrereq ? 1.4 : 1;
    ctx.setLineDash(isPrereq ? [] : [3.5, 3.5]);
    ctx.beginPath();
    ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
    ctx.stroke();
    if (isPrereq && (hot || view.k > 0.7)) {
      const dx = a.x - b.x, dy = a.y - b.y, d = Math.sqrt(dx * dx + dy * dy) || 1;
      const r = radius(b) + 4;
      const ax = b.x + (dx / d) * r, ay = b.y + (dy / d) * r;
      const ang = Math.atan2(dy, dx);
      ctx.save();
      ctx.translate(ax, ay); ctx.rotate(ang);
      ctx.fillStyle = col(dc.color, hot ? 0.95 : 0.55);
      ctx.beginPath();
      ctx.moveTo(3.4, 0); ctx.lineTo(-1.6, -2.4); ctx.lineTo(-1.6, 2.4);
      ctx.closePath(); ctx.fill();
      ctx.restore();
    }
  }
  ctx.setLineDash([]);

  // nodes
  for (const n of nodes) {
    if (n.hidden) continue;
    const dc = domById.get(n.domain) || DATA.domains[0];
    const r = radius(n);
    let alpha = 0.95;
    let show = true;
    if (state.query) { if (!searchMatch(n)) alpha = 0.07; }
    if (state.focus && state.selected && n.id !== state.selected.id && !hl.has(n.id)) alpha = 0.05;
    if (alpha < 0.03) continue;
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fillStyle = col(dc.color, alpha);
    ctx.fill();
    if (state.hovered === n || state.selected === n) {
      ctx.lineWidth = 2; ctx.strokeStyle = "#ffffff";
      ctx.shadowColor = dc.color; ctx.shadowBlur = 14 * alpha;
      ctx.stroke();
      ctx.shadowBlur = 0;
    } else if (state.query && searchMatch(n) && state.query) {
      ctx.lineWidth = 1.2; ctx.strokeStyle = col(dc.color, 0.9); ctx.stroke();
    }
    if (n.degree === 0 && view.k > 0.9) {
      ctx.lineWidth = 0.8; ctx.strokeStyle = col(dc.color, 0.5); ctx.stroke();
    }
  }
  ctx.restore();

  // labels in screen space
  drawLabels();
}

function drawLabels() {
  const fs = 11;
  ctx.save();
  ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  ctx.font = `600 ${fs}px ui-sans-serif, -apple-system, "Segoe UI", Roboto, sans-serif`;
  ctx.textAlign = "left"; ctx.textBaseline = "bottom";
  const labelSet = new Set();
  if (state.hovered) labelSet.add(state.hovered);
  if (state.selected) labelSet.add(state.selected);
  const maxLbl = Math.max(6, Math.round(24 * view.k));
  let hubs = 0;
  for (const n of nodes) {
    if (n.hidden) continue;
    if (n.degree >= 12 && hubs < maxLbl) { labelSet.add(n); hubs++; }
  }
  const q = state.query ? state.query.toLowerCase() : null;
  for (const n of nodes) {
    if (n.hidden || n.degree === 0) continue;
    if (q && searchMatch(n)) { labelSet.add(n); }
  }
  for (const n of labelSet) {
    if (n.hidden) continue;
    const s = worldToScreen(n);
    if (s.x < -200 || s.x > W + 200 || s.y < -60 || s.y > H + 60) continue;
    const label = n.title.length > 42 ? n.title.slice(0, 41) + "…" : n.title;
    const dc = domById.get(n.domain) || DATA.domains[0];
    ctx.lineWidth = 3; ctx.strokeStyle = "rgba(11,14,20,0.85)";
    ctx.strokeText(label, s.x + radius(n) + 4, s.y + fs / 2);
    ctx.fillStyle = n === state.hovered || n === state.selected ? "#ffffff" : col(dc.color, 0.95);
    ctx.fillText(label, s.x + radius(n) + 4, s.y + fs / 2);
  }
  ctx.restore();
}

function render() {
  ctx.clearRect(0, 0, W, H);
  draw();
}

/* ================= tooltip ================= */
const tooltip = document.getElementById("tooltip");
let ttX = 0, ttY = 0;
function showTooltip(n, px, py) {
  ttX = px; ttY = py;
  const dc = domById.get(n.domain);
  const yr = n.year ? " · " + n.year : "";
  const aus = n.authors && n.authors.length ? n.authors.slice(0, 3).join(", ") + (n.authors.length > 3 ? " et al." : "") + yr : yr.replace(" · ", "");
  let inDeg = 0, outDeg = 0;
  for (const l of links) { if (l.target === n.id) inDeg++; if (l.source === n.id) outDeg++; }
  tooltip.innerHTML = `
    <div class="tt-title">${esc(n.title)}</div>
    <div class="tt-meta"><span class="dot" style="background:${dc.color}"></span>${esc(dc.label)} · ${esc(n.tier)} · ${esc(n.type)}${aus ? " · " + esc(aus) : ""}</div>
    <div class="tt-sum">${esc(n.summary.slice(0, 190))}${n.summary.length > 190 ? "…" : ""}</div>
    <div class="tt-chips">
      <span class="chip">degree ${n.degree}</span>
      <span class="chip">⇠ ${inDeg} incoming</span>
      <span class="chip">⇢ ${outDeg} outgoing</span>
      ${n.subtopics.slice(0, 3).map(s => `<span class="chip">${esc(s)}</span>`).join("")}
    </div>`;
  positionTooltip(px, py);
  tooltip.classList.add("show");
}
function positionTooltip(px, py) {
  const r = tooltip.getBoundingClientRect();
  let x = px + 16, y = py + 14;
  if (x + r.width > window.innerWidth - 10) x = px - r.width - 14;
  if (y + r.height > window.innerHeight - 10) y = py - r.height - 12;
  tooltip.style.left = Math.max(6, x) + "px";
  tooltip.style.top = Math.max(6, y) + "px";
}
function hideTooltip() { tooltip.classList.remove("show"); }

const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

/* ================= detail panel ================= */
const panel = document.getElementById("panel");
function openPanel(n) {
  state.selected = n;
  const dc = domById.get(n.domain);
  document.getElementById("p-title").textContent = n.title;
  document.getElementById("p-meta").innerHTML = `
    <span class="chip dom" style="background:${dc.color}">${esc(dc.label)}</span>
    <span class="chip">${esc(n.tier)}</span>
    <span class="chip">${esc(n.type)}</span>
    <span class="chip">${n.year || "n.d."}</span>
    ${n.authors && n.authors.length ? `<span class="chip">${esc(n.authors.slice(0, 4).join(", ") + (n.authors.length > 4 ? " et al." : ""))}</span>` : ""}
    ${n.subtopics.map(s => `<span class="chip">${esc(s)}</span>`).join("")}`;
  // edge direction: {source: entry, target: prerequisite} — a node's prerequisites
  // are edges where the node is the SOURCE; its related neighbors are edges on either side.
  const prereqs = links.filter(l => l.source === n.id && l.type === "prereq").map(l => byId.get(l.target));
  const related = links.filter(l => (l.source === n.id || l.target === n.id) && l.type === "related").map(l => byId.get(l.source === n.id ? l.target : l.source));
  const body = document.getElementById("p-body");
  const linkList = (arr, label) => arr.length ? `
    <h4>${label} (${arr.length})</h4>
    <ul class="links">${arr.map(m => `
      <li data-id="${esc(m.id)}">
        <span class="l-dot" style="background:${domById.get(m.domain).color}"></span>
        <span class="l-title">${esc(m.title)}</span>
        <span class="l-arrow">→</span>
      </li>`).join("")}</ul>` : "";
  body.innerHTML = `
    <h4>What it is</h4>
    <p>${esc(n.summary) || "<span style='color:var(--faint)'>No summary.</span>"}</p>
    <h4>Why it matters</h4>
    <p>${esc(n.why_it_matters) || "<span style='color:var(--faint)'>No note.</span>"}</p>
    ${linkList(prereqs, "Read these first (prerequisites)")}
    ${linkList(related, "Related · critiques · follow-ups")}
    <a class="p-url" href="${esc(n.url)}" target="_blank" rel="noopener">Open source <small>${esc(n.url)}</small></a>`;
  body.querySelectorAll("li[data-id]").forEach(li => {
    li.addEventListener("click", () => {
      const m = byId.get(li.dataset.id);
      if (m) { openPanel(m); focusNode(m); render(); }
    });
  });
  panel.classList.add("open");
  document.getElementById("btnFocus").classList.toggle("on", state.focus);
  render();
}
function closePanel() { panel.classList.remove("open"); state.selected = null; render(); }

/* ================= search ================= */
const searchEl = document.getElementById("search");
const resultsEl = document.getElementById("results");
const matchEl = document.getElementById("matchcount");
let resultIdx = -1;
const RESULT_SHOWN = 10;

function doSearch() {
  state.query = searchEl.value.trim();
  const list = [];
  if (state.query) {
    for (const n of nodes) if (searchMatch(n)) list.push(n);
    list.sort((a, b) => (b.degree - a.degree) || a.title.localeCompare(b.title));
  }
  matchEl.textContent = state.query ? list.length : "";
  searchEl.classList.toggle("dimmed", !!state.query);
  renderResults(list);
  applyFilters();
}
function renderResults(list) {
  if (!state.query || !list.length) { resultsEl.classList.remove("show"); resultsEl.innerHTML = ""; return; }
  resultsEl.innerHTML = list.slice(0, RESULT_SHOWN).map((n, i) => `
    <div class="r-item${i === resultIdx ? " active" : ""}" data-id="${esc(n.id)}">
      <span class="r-dot" style="background:${domById.get(n.domain).color}"></span>
      <span class="r-title">${esc(n.title)}</span>
      <span class="r-meta">${esc(n.tier)} · ${n.degree}</span>
    </div>`).join("");
  resultsEl.querySelectorAll(".r-item").forEach(el => {
    el.addEventListener("mousedown", e => { e.preventDefault(); selectResult(el.dataset.id); });
  });
  resultsEl.classList.add("show");
}
function selectResult(id) {
  const n = byId.get(id); if (!n) return;
  openPanel(n); focusNode(n); reheat(0.4); render();
}
searchEl.addEventListener("input", () => { resultIdx = -1; doSearch(); });
searchEl.addEventListener("keydown", e => {
  const list = state.query ? nodes.filter(n => searchMatch(n)).sort((a, b) => b.degree - a.degree) : [];
  if (e.key === "Enter") {
    e.preventDefault();
    if (list.length) { const n = resultIdx >= 0 ? list[Math.min(resultIdx, list.length - 1)] : list[0]; selectResult(n.id); }
  } else if (e.key === "ArrowDown" && list.length) {
    e.preventDefault(); resultIdx = (resultIdx + 1) % Math.min(list.length, RESULT_SHOWN); renderResults(list);
  } else if (e.key === "ArrowUp" && list.length) {
    e.preventDefault(); resultIdx = (resultIdx - 1 + Math.min(list.length, RESULT_SHOWN)) % Math.min(list.length, RESULT_SHOWN); renderResults(list);
  } else if (e.key === "Escape") {
    searchEl.value = ""; state.query = ""; matchEl.textContent = ""; searchEl.classList.remove("dimmed");
    resultsEl.classList.remove("show"); applyFilters();
  }
});

/* ================= pointer interaction ================= */
let dragging = null, panning = false, lastPX = 0, lastPY = 0, moved = 0;
let hoveredNow = null;

canvas.addEventListener("pointerdown", e => {
  canvas.setPointerCapture(e.pointerId);
  const n = hitTest(e.clientX, e.clientY);
  lastPX = e.clientX; lastPY = e.clientY; moved = 0;
  if (n) { dragging = n; canvas.classList.add("dragging"); }
  else { panning = true; canvas.classList.add("dragging"); }
});
canvas.addEventListener("pointermove", e => {
  const dx = e.clientX - lastPX, dy = e.clientY - lastPY;
  if (dragging) {
    dragging.x = (e.clientX - view.x) / view.k;
    dragging.y = (e.clientY - view.y) / view.k;
    dragging.vx = dx / view.k; dragging.vy = dy / view.k;
    reheat(0.25);
    moved += Math.abs(dx) + Math.abs(dy);
  } else if (panning) {
    view.x += dx; view.y += dy;
    moved += Math.abs(dx) + Math.abs(dy);
  } else {
    const n = hitTest(e.clientX, e.clientY);
    if (n !== hoveredNow) {
      hoveredNow = n; state.hovered = n;
      if (n) showTooltip(n, e.clientX, e.clientY);
      else hideTooltip();
      render();
    } else if (n) positionTooltip(e.clientX, e.clientY);
  }
  lastPX = e.clientX; lastPY = e.clientY;
  if (dragging || panning) render();
});
canvas.addEventListener("pointerup", e => {
  canvas.releasePointerCapture(e.pointerId);
  const wasClick = moved < 5;
  if (dragging && wasClick) {
    const n = dragging;
    openPanel(n);
  } else if (!dragging && panning && wasClick) {
    const n = hitTest(e.clientX, e.clientY);
    if (n) { openPanel(n); }
  }
  dragging = null; panning = false; canvas.classList.remove("dragging");
});
canvas.addEventListener("pointerleave", () => { hoveredNow = null; state.hovered = null; hideTooltip(); render(); });

canvas.addEventListener("wheel", e => {
  e.preventDefault();
  const factor = Math.exp(-e.deltaY * 0.0012);
  const nk = Math.min(Math.max(view.k * factor, 0.12), 8);
  const wx = (e.clientX - view.x) / view.k, wy = (e.clientY - view.y) / view.k;
  view.x = e.clientX - wx * nk; view.y = e.clientY - wy * nk;
  view.k = nk;
  render();
}, { passive: false });

/* ================= UI controls ================= */
document.getElementById("btnFit").addEventListener("click", () => { fitView(); render(); });
document.getElementById("btnRelayout").addEventListener("click", () => { seed(); temp = 1; fitView(); render(); });
document.getElementById("btnFocus").addEventListener("click", () => {
  state.focus = !state.focus;
  document.getElementById("btnFocus").classList.toggle("on", state.focus);
  render();
});
document.getElementById("pclose").addEventListener("click", closePanel);

const legend = document.getElementById("legend");
const filters = document.getElementById("filters");
document.getElementById("btnLegend").addEventListener("click", () => {
  state.legendOpen = !state.legendOpen;
  legend.style.display = state.legendOpen ? "" : "none";
  filters.style.display = state.legendOpen ? "" : "none";
});

// tier chips
(function tierUI() {
  const row = document.getElementById("tierrow");
  ["entry", "core", "deep"].forEach(t => {
    const c = document.createElement("div");
    c.className = "tier-chip on"; c.dataset.tier = t; c.textContent = t + " (" + DATA.stats[t] + ")";
    c.addEventListener("click", () => {
      state.selTiers.has(t) ? state.selTiers.delete(t) : state.selTiers.add(t);
      c.classList.toggle("on", state.selTiers.has(t));
      if (!state.selTiers.size) { state.selTiers.add(t); c.classList.add("on"); }
      applyFilters();
    });
    row.appendChild(c);
  });
  DATA.stats.tiers = {};
  for (const n of nodes) DATA.stats.tiers[n.tier] = (DATA.stats.tiers[n.tier] || 0) + 1;
  row.querySelectorAll(".tier-chip").forEach(c => { c.textContent = c.dataset.tier + " (" + (DATA.stats.tiers[c.dataset.tier] || 0) + ")"; });
})();

// domain chips
(function domUI() {
  const grid = document.getElementById("domgrid");
  for (const d of DATA.domains) {
    const c = document.createElement("div");
    c.className = "dom-chip on"; c.dataset.dom = d.id; c.title = d.label;
    c.innerHTML = `<span class="dot" style="background:${d.color}"></span><span class="dn">${esc(d.label)}</span><span style="margin-left:auto;font-family:var(--mono);font-size:10px">${d.count}</span>`;
    c.addEventListener("click", () => {
      state.selDoms.has(d.id) ? state.selDoms.delete(d.id) : state.selDoms.add(d.id);
      c.classList.toggle("on", state.selDoms.has(d.id));
      c.classList.toggle("off", !state.selDoms.has(d.id));
      if (!state.selDoms.size) { state.selDoms.add(d.id); c.classList.add("on"); c.classList.remove("off"); }
      applyFilters();
    });
    grid.appendChild(c);
  }
  document.getElementById("btnAll").addEventListener("click", () => {
    state.selDoms = new Set(DATA.domains.map(d => d.id));
    grid.querySelectorAll(".dom-chip").forEach(c => { c.classList.add("on"); c.classList.remove("off"); });
    applyFilters();
  });
  document.getElementById("btnNone").addEventListener("click", () => {
    state.selDoms.clear();
    grid.querySelectorAll(".dom-chip").forEach(c => { c.classList.remove("on"); c.classList.add("off"); });
    applyFilters();
  });
})();

// legend domain rows (clickable like filter)
(function legendUI() {
  const lg = document.getElementById("lgdom");
  for (const d of DATA.domains) {
    const row = document.createElement("div");
    row.className = "lg-row"; row.dataset.dom = d.id;
    row.innerHTML = `<span class="dot" style="background:${d.color}"></span>${esc(d.label)}<span class="n">${d.count}</span>`;
    row.addEventListener("click", () => {
      state.selDoms.has(d.id) ? state.selDoms.delete(d.id) : state.selDoms.add(d.id);
      const chip = document.querySelector(`.dom-chip[data-dom="${d.id}"]`);
      if (chip) { chip.classList.toggle("on", state.selDoms.has(d.id)); chip.classList.toggle("off", !state.selDoms.has(d.id)); }
      applyFilters();
    });
    lg.appendChild(row);
  }
  document.getElementById("lgsw").innerHTML = ["entry", "core", "deep"].map(t =>
    `<div class="sw"><span style="width:${TIER_R(t) * 2}px;height:${TIER_R(t) * 2}px;border-radius:50%;background:#8b94a7;display:block"></span>${t}</div>`).join("");
})();

function updateLegendDim() {
  document.querySelectorAll("#lgdom .lg-row").forEach(row => {
    row.classList.toggle("dim", !state.selDoms.has(row.dataset.dom));
  });
}

/* ================= toast ================= */
let toastTimer = null;
function toast(msg) {
  const t = document.getElementById("toast");
  t.innerHTML = msg; t.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove("show"), 2600);
}

/* ================= keyboard ================= */
document.addEventListener("keydown", e => {
  const tag = document.activeElement && document.activeElement.tagName;
  if (tag === "INPUT") { if (e.key === "Escape") searchEl.blur(); return; }
  if (e.key === "/") { e.preventDefault(); searchEl.focus(); }
  else if (e.key === "Escape") { if (panel.classList.contains("open")) closePanel(); }
  else if (e.key === "f" || e.key === "F") { fitView(); render(); }
  else if (e.key === "l" || e.key === "L") {
    state.legendOpen = !state.legendOpen;
    legend.style.display = state.legendOpen ? "" : "none";
    filters.style.display = state.legendOpen ? "" : "none";
  }
});

/* ================= stats ================= */
(function statsUI() {
  const s = DATA.stats;
  document.getElementById("st-nodes").textContent = s.nodes;
  document.getElementById("st-edges").textContent = s.edges;
  document.getElementById("st-prereq").textContent = s.prereq;
  document.getElementById("st-related").textContent = s.related;
  document.getElementById("st-avg").textContent = s.avg_degree;
  document.getElementById("st-hub").textContent = s.hub_title + " (" + s.max_degree + ")";
  document.getElementById("st-hub").title = s.hub_id;
})();

/* ================= main loop ================= */
let last = performance.now();
let settledOnce = false;
function loop(now) {
  requestAnimationFrame(loop);
  const dt = Math.min((now - last) / 16.667, 3); last = now;
  if (temp > 0.002) {
    tick(); temp *= 0.996;
    render();
  } else if (!settledOnce) {
    // layout has converged — fit the final arrangement into view once
    settledOnce = true;
    fitView(); render();
  }
}
function init() {
  resize();
  fitView();
  requestAnimationFrame(loop);
  setTimeout(() => {
    if (temp > 0.02) { fitView(); render(); }
    toast(`Loaded <b>${DATA.stats.nodes}</b> entries · <b>${DATA.stats.edges}</b> cross-links`);
  }, 60);
}
init();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    sys.exit(main())
