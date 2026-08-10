#!/usr/bin/env python3
"""Merge a subtopic fragment into data/entries.json with schema validation.

Usage: python scripts/merge_entries.py data/fragments/<subtopic>.json
Validates required fields and enums, rejects duplicate ids/urls (exact, case-insensitive),
then writes entries.json back atomically (tmp + rename). Prints a summary.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, "data", "entries.json")

DOMAINS = {
    "entry-tier", "macrostrategy", "agent-foundations", "interpretability",
    "oversight-rlhf", "evals-benchmarks", "governance-policy",
    "security-redteam", "philosophy-values", "field-infrastructure",
}
TYPES = {"paper", "course", "org", "tool", "community", "book", "video", "essay", "dataset"}
TIERS = {"entry", "core", "deep"}
STATUSES = {"live", "paywalled", "dead"}
REQUIRED = {"id", "title", "authors", "year", "url", "type", "domain",
            "subtopics", "tier", "prerequisites", "summary",
            "why_it_matters", "related", "last_verified", "status"}


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data, path):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)  # atomic on POSIX and Windows same-volume


def validate(e, idx):
    errs = []
    if not isinstance(e, dict):
        errs.append(f"entry[{idx}] not an object")
        return errs
    for k in REQUIRED:
        if k not in e:
            errs.append(f"entry[{idx}] missing field '{k}'")
    if errs:
        return errs
    if not e["id"] or any(c in e["id"] for c in " _/\\"):
        errs.append(f"entry[{idx}] bad id '{e['id']}' (kebab-case)")
    if not e["url"].startswith("http"):
        errs.append(f"entry[{idx}] bad url '{e['url']}'")
    if e["domain"] not in DOMAINS:
        errs.append(f"entry[{idx}] unknown domain '{e['domain']}'")
    if e["type"] not in TYPES:
        errs.append(f"entry[{idx}] unknown type '{e['type']}'")
    if e["tier"] not in TIERS:
        errs.append(f"entry[{idx}] unknown tier '{e['tier']}'")
    if e["status"] not in STATUSES:
        errs.append(f"entry[{idx}] unknown status '{e['status']}'")
    if not isinstance(e["authors"], list) or not e["authors"]:
        errs.append(f"entry[{idx}] authors must be a non-empty list")
    if not isinstance(e["subtopics"], list) or not e["subtopics"]:
        errs.append(f"entry[{idx}] subtopics must be a non-empty list")
    for k in ("prerequisites", "related"):
        if not isinstance(e[k], list):
            errs.append(f"entry[{idx}] '{k}' must be a list")
    if not e["summary"] or len(e["summary"]) < 20:
        errs.append(f"entry[{idx}] summary too short")
    if not e["why_it_matters"]:
        errs.append(f"entry[{idx}] why_it_matters empty")
    if not isinstance(e["year"], int):
        errs.append(f"entry[{idx}] year must be int")
    return errs


def main():
    if len(sys.argv) != 2:
        print("usage: merge_entries.py <fragment.json>")
        sys.exit(1)
    frag_path = sys.argv[1]
    if not os.path.exists(frag_path):
        print(f"fragment not found: {frag_path}")
        sys.exit(1)
    fragment = load(frag_path)
    if isinstance(fragment, dict):
        fragment = [fragment]
    if not isinstance(fragment, list):
        print("fragment must be a JSON list (or single object)")
        sys.exit(1)

    catalog = load(ENTRIES) if os.path.exists(ENTRIES) else []
    ids = {e["id"] for e in catalog}
    urls = {e["url"].lower() for e in catalog}
    titles = {e["title"].lower() for e in catalog}

    added = updated = 0
    for i, e in enumerate(fragment):
        errs = validate(e, i)
        if errs:
            print("VALIDATION FAILED:")
            for err in errs:
                print("  -", err)
            sys.exit(1)
        if e["id"] in ids:
            catalog = [c for c in catalog if c["id"] != e["id"]]
            updated += 1
        elif e["url"].lower() in urls:
            print(f"DUPLICATE URL: {e['url']} (id={e['id']})")
            sys.exit(1)
        elif e["title"].lower() in titles:
            print(f"DUPLICATE TITLE: {e['title']} (id={e['id']})")
            sys.exit(1)
        catalog.append(e)
        ids.add(e["id"])
        urls.add(e["url"].lower())
        titles.add(e["title"].lower())
        added += 1

    save(catalog, ENTRIES)
    print(f"MERGED: {added} added, {updated} updated -> {len(catalog)} total entries in data/entries.json")


if __name__ == "__main__":
    main()
