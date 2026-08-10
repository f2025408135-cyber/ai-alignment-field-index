#!/usr/bin/env python3
"""Merge a subtopic fragment into data/entries.json with schema validation.

Usage: python scripts/merge_entries.py data/fragments/<subtopic>.json
Validates required fields and enums, rejects duplicate ids/urls (exact, case-insensitive),
then writes entries.json back atomically (tmp + rename). Prints a summary.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, "data", "entries.json")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from taxonomy import EXPECTED_SUBTOPICS  # noqa: E402

DOMAINS = set(EXPECTED_SUBTOPICS)
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
    else:
        allowed = set(EXPECTED_SUBTOPICS.get(e.get("domain", ""), []))
        unknown = [s for s in e["subtopics"] if s not in allowed]
        if unknown:
            errs.append(f"entry[{idx}] subtopic tags not in taxonomy for '{e.get('domain')}': {unknown}")
    for k in ("prerequisites", "related"):
        if not isinstance(e[k], list):
            errs.append(f"entry[{idx}] '{k}' must be a list")
    if not e["summary"] or len(e["summary"]) < 20:
        errs.append(f"entry[{idx}] summary too short")
    if not e["why_it_matters"]:
        errs.append(f"entry[{idx}] why_it_matters empty")
    if not isinstance(e["year"], int) or not (1800 <= e["year"] <= 2035):
        errs.append(f"entry[{idx}] year must be int in 1800..2035")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", e["last_verified"]):
        errs.append(f"entry[{idx}] last_verified must be YYYY-MM-DD")
    if any(c.isspace() for c in e["url"]):
        errs.append(f"entry[{idx}] url contains whitespace")
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
            # replace in place so re-merges keep entry order stable (no-op on the catalog)
            for idx, c in enumerate(catalog):
                if c["id"] == e["id"]:
                    catalog[idx] = e
                    # refresh dedup sets so an update that changes url/title doesn't
                    # leave a stale value that false-positives later fragment entries
                    urls.discard(c["url"].lower())
                    titles.discard(c["title"].lower())
                    urls.add(e["url"].lower())
                    titles.add(e["title"].lower())
                    break
            updated += 1
        elif e["url"].lower() in urls:
            print(f"DUPLICATE URL: {e['url']} (id={e['id']})")
            sys.exit(1)
        elif e["title"].lower() in titles:
            print(f"DUPLICATE TITLE: {e['title']} (id={e['id']})")
            sys.exit(1)
        else:
            catalog.append(e)
            added += 1

    # rebuild dedup sets from the merged catalog so stale entries from updates don't linger
    ids = {e["id"] for e in catalog}
    urls = {e["url"].lower() for e in catalog}
    titles = {e["title"].lower() for e in catalog}
    if len(urls) != len(catalog) or len(titles) != len(catalog) or len(ids) != len(catalog):
        print("MERGE ERROR: duplicate id/url/title across merged catalog — fix before proceeding")
        sys.exit(1)

    # canonical order so re-merges are byte-stable regardless of merge history
    catalog.sort(key=lambda e: (e["domain"], e["id"]))

    save(catalog, ENTRIES)
    print(f"MERGED: {added} added, {updated} updated -> {len(catalog)} total entries in data/entries.json")


if __name__ == "__main__":
    main()
