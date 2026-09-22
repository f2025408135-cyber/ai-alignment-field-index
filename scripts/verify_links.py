#!/usr/bin/env python3
"""Verify every URL in data/entries.json actually resolves.

Usage:
  python scripts/verify_links.py            # dry run: report only
  python scripts/verify_links.py --apply    # write status live/dead back into entries.json

Classification (transient 429/5xx are retried once with backoff):
  HTTP 200-399          -> live
  HTTP 401/403          -> live(blocked): bot-blocked but exists; still live
  429/5xx after retry   -> unknown: cannot confirm either way; status untouched on --apply
  HTTP 404+ or network  -> dead (status written as dead with --apply)
"""
import argparse
import json
import os
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRIES = os.path.join(ROOT, "data", "entries.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
TRANSIENT = {429, 500, 502, 503, 504}
RETRY_DELAY = 3.0


def _fetch(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, url
    except (urllib.error.URLError, socket.timeout, ssl.SSLError, ConnectionError, OSError) as e:
        return -1, f"{type(e).__name__}: {e}"


def check(url, timeout=25):
    code, note = _fetch(url, timeout)
    if code == -1 or code in TRANSIENT:
        # network blips and rate-limit/server errors are retried once before judging dead
        time.sleep(RETRY_DELAY)
        code2, note2 = _fetch(url, timeout)
        if code2 != -1:
            # retry answered HTTP at all (even transient) => host is up; trust the retry code
            return code2, f"{note} [retry->{code2}]"
        return code, f"{note} [retry->-1]"
    return code, note


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

    live = blocked = unknown = dead = 0
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
            blocked += 1
            live += 1
            st = "live(blocked)"
        elif code in TRANSIENT:
            unknown += 1
            st = "unknown"
        else:
            dead += 1
            st = "DEAD"
        extra = f" -> {note}" if note != e["url"] else ""
        print(f"{st:<13} {code:<6} {e['id']}  {e['url']}{extra}")

    print(f"\nSUMMARY: {len(catalog)} checked, {live} live ({blocked} bot-blocked/401-403), "
          f"{unknown} unknown(transient), {dead} dead/failed")

    if args.apply:
        from datetime import date
        today = date.today().isoformat()
        changed = 0
        for e in catalog:
            code, _ = results[e["id"]]
            if code in TRANSIENT:
                continue  # cannot confirm either way; leave status and last_verified untouched
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
    elif dead > 0 or unknown > 0:
        print("NOTE: dead/unknown URLs present — fix, retry, or mark before committing.")
        sys.exit(1)


if __name__ == "__main__":
    main()
