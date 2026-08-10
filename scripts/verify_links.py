#!/usr/bin/env python3
"""Verify every URL in data/entries.json actually resolves.

Usage:
  python scripts/verify_links.py            # dry run: report only
  python scripts/verify_links.py --apply    # write status live/dead back into entries.json

Classification:
  HTTP 200-399          -> live
  HTTP 401/403          -> live-with-caveat (bot-blocked; flagged BLOCKED in report, still live)
  HTTP 404+ or network  -> dead (status written as dead with --apply)

Use --ua to override the user agent for Cloudflare-heavy sites if needed.
"""
import argparse
import json
import os
import socket
import ssl
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, "data", "entries.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def check(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, url
    except (urllib.error.URLError, socket.timeout, ssl.SSLError, ConnectionError, OSError) as e:
        return -1, f"{type(e).__name__}: {e}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write status back into entries.json")
    ap.add_argument("--timeout", type=int, default=25)
    ap.add_argument("--max-workers", type=int, default=6)
    args = ap.parse_args()

    with open(ENTRIES, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    results = {}
    with ThreadPoolExecutor(max_workers=args.max_workers) as pool:
        futures = {pool.submit(check, e["url"], args.timeout): e for e in catalog}
        for fut in as_completed(futures):
            e = futures[fut]
            code, note = fut.result()
            results[e["id"]] = (code, note)

    live = blocked = dead = 0
    print(f"{'STATUS':<13} {'CODE':<6} ID / URL")
    for e in catalog:
        code, note = results[e["id"]]
        if code == -1:
            dead += 1
            st = "DEAD"
        elif 200 <= code < 400:
            live += 1
            st = "live"
        elif code in (401, 403):
            # bot-blocked: exists but refuses curl/urllib; counted live with a caveat label
            blocked += 1
            live += 1
            st = "live(blocked)"
        else:
            dead += 1
            st = "DEAD"
        extra = f" -> {note}" if note != e["url"] else ""
        print(f"{st:<13} {code:<6} {e['id']}  {e['url']}{extra}")

    print(f"\nSUMMARY: {len(catalog)} checked, {live} live ({blocked} bot-blocked/401-403), {dead} dead/failed")

    if args.apply:
        from datetime import date
        today = date.today().isoformat()
        changed = 0
        for e in catalog:
            code, _ = results[e["id"]]
            resolved = code not in (-1,) and (code < 400 or code in (401, 403))
            if not resolved:
                new = "dead"            # paywalled can rot too; keep the record
            elif e["status"] == "paywalled":
                new = "paywalled"       # resolved fine — never upgrade paywalled to live
            else:
                new = "live"
            if new != e["status"]:
                e["status"] = new
                if resolved:
                    e["last_verified"] = today
                changed += 1
            elif resolved and e["last_verified"] != today:
                e["last_verified"] = today
                changed += 1
        tmp = ENTRIES + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, ENTRIES)
        print(f"APPLIED: updated status on {changed} entries")
    elif dead > 0:
        print("NOTE: dead URLs present — fix or mark before committing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
