#!/usr/bin/env python3
"""
Downloads how many times each catalog card's main button ("Open tool",
"Read the spec", "View files") has been clicked, from GoatCounter, and writes
{ "<author>/<tool>": count, ... } to the file named by USAGE_FILE.

The catalog page reports each click as a GoatCounter event named
"open/<author>/<tool>". No cookies and nothing about the person is sent.

Needs two settings in GitHub (Settings -> Secrets and variables -> Actions):
  variable GOATCOUNTER_CODE   the site code, e.g. "fccchem" for fccchem.goatcounter.com
  secret   GOATCOUNTER_TOKEN  an API key with "Read statistics" permission

If either is missing, or GoatCounter can't be reached, this prints a note and
exits normally: the catalog then builds without counts, exactly as before.
"""

import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone

START = "2026-11-01T00:00:00Z"   # counting began here


def main():
    code = os.environ.get("GOATCOUNTER_CODE", "").strip()
    token = os.environ.get("GOATCOUNTER_TOKEN", "").strip()
    out = os.environ.get("USAGE_FILE", "usage.json")
    if not code or not token:
        print("GoatCounter not set up yet; building without usage counts.")
        return

    end = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
    counts, seen = {}, []
    try:
        while True:
            params = [("start", START), ("end", end.strftime("%Y-%m-%dT%H:%M:%SZ")), ("limit", "100")]
            params += [("exclude_paths", str(p)) for p in seen]
            url = f"https://{code}.goatcounter.com/api/v0/stats/hits?" + urllib.parse.urlencode(params)
            req = urllib.request.Request(url, headers={
                "Authorization": f"Bearer {token}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            for h in data.get("hits", []):
                seen.append(h.get("path_id"))
                path = str(h.get("path", "")).lstrip("/")
                if path.startswith("open/"):
                    folder = path[len("open/"):].strip("/")
                    counts[folder] = counts.get(folder, 0) + int(h.get("count") or 0)
            if not data.get("more") or not data.get("hits"):
                break
    except Exception as e:  # never block the catalog build
        print(f"::warning::Could not read GoatCounter usage ({e}); building without counts.")
        return

    with open(out, "w", encoding="utf-8") as f:
        json.dump(counts, f, indent=1, sort_keys=True)
    print(f"Usage counts for {len(counts)} tool(s) written to {out}")


if __name__ == "__main__":
    sys.exit(main())
