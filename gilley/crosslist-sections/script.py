#!/usr/bin/env python3
"""
Canvas Cross-Listing — combine double sections into one shell.

Every semester you get two Canvas shells for the same course (same lecture,
different lab times). This moves the section(s) from one shell into the
other so students see a single Canvas card. Sections survive the move, so
lab-specific due dates still work via "Assign to > section".

Setup: copy .env.example to .env (next to this script) and fill in your
Canvas URL and API token. Nothing else to configure — the script reads
your current courses from the API at runtime.

Usage:
    python3 script.py                    # dry run: asks which sections, shows plan
    python3 script.py --apply            # asks which sections, then combines
    python3 script.py --term 2026FA      # specific term (default: newest found)
    python3 script.py --sections 25825,25826 --apply
                                         # skip prompts; first = destination
    python3 script.py --no-rename        # keep destination course name as-is

At the prompt you may enter either the 5-digit section number (25825) or
the Canvas course id from the URL (144600) — the script accepts both.

Safety:
    - Dry run is the default. Nothing changes without --apply.
    - Refuses to combine sections from different courses.
    - Refuses to move a section out of a course with ANY student
      submissions (they do not follow the section). --force overrides.
    - Requires typing the destination course id to confirm.
    - To UNDO (before submissions exist):
      DELETE /api/v1/sections/<section_id>/crosslist
"""

import json
import os
import re
import sys
import argparse
import urllib.request
import urllib.parse
import urllib.error

TERM_ORDER = {"SP": 0, "SU": 1, "FA": 2}
# SIS course_code pattern, e.g. CHEM-3A-25825-2026FA
CODE_RE = re.compile(
    r"^(?P<course>[A-Z]+-\d+[A-Z]*)-(?P<section>\d+)-(?P<term>\d{4}(?:SP|SU|FA))$")


# ---------------------------------------------------------------- env / http

def load_env():
    """Read .env next to this script. Never commit the .env file."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    os.environ.setdefault(k.strip(), v.strip())
    missing = [k for k in ("CANVAS_URL", "CANVAS_API_TOKEN")
               if not os.environ.get(k)]
    if missing:
        sys.exit("Missing " + ", ".join(missing)
                 + " — copy .env.example to .env next to this script.")
    return os.environ["CANVAS_URL"].rstrip("/"), os.environ["CANVAS_API_TOKEN"]


BASE, TOKEN = None, None  # set in main()


def api(method, path, data=None):
    """One API call. Returns (parsed_json, response_headers)."""
    url = path if path.startswith("http") else BASE + path
    print(f"[DEBUG] {method} {url}")
    body = urllib.parse.urlencode(data).encode() if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", "Bearer " + TOKEN)  # never printed
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read().decode()), dict(r.headers)
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        sys.exit(f"Canvas API error {e.code} on {method} {path}:\n{detail}")
    except urllib.error.URLError as e:
        sys.exit(f"Could not reach {BASE}: {e.reason}")


def get_all_pages(path):
    """Follow Canvas Link-header pagination."""
    items, url = [], path
    while url:
        page, headers = api("GET", url)
        items.extend(page)
        url = None
        for link in headers.get("Link", "").split(","):
            if 'rel="next"' in link:
                url = link[link.find("<") + 1:link.find(">")]
                break
    return items


# ---------------------------------------------------------------- canvas ops

def get_teacher_courses():
    return get_all_pages("/api/v1/courses?enrollment_type=teacher&per_page=100")


def parse_courses(courses):
    parsed = []
    for c in courses:
        m = CODE_RE.match(c.get("course_code") or "")
        if m:
            parsed.append({
                "id": c["id"], "name": c["name"], "code": c["course_code"],
                "course": m.group("course"), "section": m.group("section"),
                "term": m.group("term"), "state": c.get("workflow_state"),
            })
    return parsed


def get_sections(course_id):
    return get_all_pages(f"/api/v1/courses/{course_id}/sections?per_page=100")


def has_submissions(course_id):
    assignments = get_all_pages(
        f"/api/v1/courses/{course_id}/assignments?per_page=100")
    return any(a.get("has_submitted_submissions") for a in assignments)


def crosslist(section_id, dest_course_id):
    result, _ = api("POST", f"/api/v1/sections/{section_id}/crosslist/{dest_course_id}")
    return result


def rename_course(course_id, new_name):
    api("PUT", f"/api/v1/courses/{course_id}", {
        "course[name]": new_name, "course[course_code]": new_name})


# ---------------------------------------------------------------- selection

def choose_shells(parsed, term, section_arg):
    """Resolve user input (section #s or course ids) to shells.

    Returns [dest, source, ...]. All must be the same course, same term.
    """
    in_term = sorted((p for p in parsed if p["term"] == term),
                     key=lambda x: (x["course"], x["section"]))
    if not in_term:
        sys.exit(f"No courses found in term {term}.")

    by_section = {p["section"]: p for p in in_term}
    by_id = {str(p["id"]): p for p in in_term}

    if section_arg:
        numbers = [s.strip() for s in section_arg.split(",") if s.strip()]
    else:
        print(f"\nYour {term} shells (use section # or course id):")
        for p in in_term:
            print(f"  section {p['section']}  {p['course']:<12} "
                  f"(course id {p['id']}, {p['state']})")
        dest_n = input("\nDestination (this shell KEEPS everything): ").strip()
        src_n = input("Merge INTO it (comma separated): ").strip()
        numbers = [dest_n] + [s.strip() for s in src_n.split(",") if s.strip()]

    if len(numbers) < 2:
        sys.exit("Need at least two entries (destination + source).")

    shells = []
    for n in numbers:
        shell = by_section.get(n) or by_id.get(n)
        if not shell:
            sys.exit(f"'{n}' matches no section number or course id in {term}. "
                     f"Sections: {', '.join(sorted(by_section))} | "
                     f"Course ids: {', '.join(sorted(by_id))}")
        shells.append(shell)

    if len({s["id"] for s in shells}) != len(shells):
        sys.exit("Same course entered twice "
                 "(a section # and its course id both count).")

    if len({s["course"] for s in shells}) > 1:
        pairs = ", ".join("{}={}".format(s["section"], s["course"]) for s in shells)
        sys.exit("REFUSING: sections belong to different courses: " + pairs
                 + ". Cross-listing different courses would merge unrelated classes.")
    return shells


# ---------------------------------------------------------------- main

def main():
    global BASE, TOKEN

    ap = argparse.ArgumentParser(
        description="Cross-list double sections into one Canvas shell.")
    ap.add_argument("--term", help="Term code, e.g. 2026FA (default: newest found)")
    ap.add_argument("--sections",
                    help="Comma-separated section #s or course ids; "
                         "FIRST is the destination. Skips the prompt.")
    ap.add_argument("--apply", action="store_true", help="Execute (default: dry run)")
    ap.add_argument("--force", action="store_true",
                    help="Proceed even if a source has submissions (DANGEROUS)")
    ap.add_argument("--no-rename", action="store_true",
                    help="Do not rename the destination course")
    args = ap.parse_args()

    BASE, TOKEN = load_env()

    parsed = parse_courses(get_teacher_courses())
    if not parsed:
        sys.exit("No courses with parseable SIS course codes found.")

    term = args.term or max((p["term"] for p in parsed),
                            key=lambda t: (int(t[:4]), TERM_ORDER.get(t[4:], -1)))
    print(f"[DEBUG] Target term: {term}")

    shells = choose_shells(parsed, term, args.sections)
    dest, sources = shells[0], shells[1:]
    combined = "{}-{}-{}".format(
        dest["course"], "/".join(s["section"] for s in shells), dest["term"])

    print(f"\n=== {dest['course']} {dest['term']} ===")
    print(f"  Destination: {dest['code']}  (id {dest['id']}, {dest['state']})")
    for s in sources:
        print(f"  Source:      {s['code']}  (id {s['id']}, {s['state']})")

    blocked = False
    for s in sources:
        print(f"[DEBUG] Checking {s['code']} for student submissions...")
        if has_submissions(s["id"]):
            print(f"  BLOCKED: {s['code']} has student submissions. They will "
                  "NOT follow the section. Use --force to override.")
            blocked = True
    if blocked and not args.force:
        sys.exit(1)

    moves = []
    for s in sources:
        for sec in get_sections(s["id"]):
            moves.append((s, sec))
            print(f"  Section to move: \"{sec['name']}\" (section id {sec['id']}) "
                  f"-> course {dest['id']}")

    if not args.no_rename:
        print(f"  Rename destination to: {combined}")

    if not args.apply:
        print("  DRY RUN — nothing changed. Re-run with --apply to execute.")
        return

    confirm = input(f"\nType the destination course id ({dest['id']}) to confirm: ")
    if confirm.strip() != str(dest["id"]):
        sys.exit("Confirmation failed. Nothing changed.")

    for s, sec in moves:
        result = crosslist(sec["id"], dest["id"])
        print(f"  Moved \"{sec['name']}\" -> now in course "
              f"{result.get('course_id')} (was {result.get('nonxlist_course_id')})")

    if not args.no_rename:
        rename_course(dest["id"], combined)
        print(f"  Renamed destination to {combined}")

    final = get_sections(dest["id"])
    print(f"  Destination now has {len(final)} sections: "
          + ", ".join('"{}"'.format(x["name"]) for x in final))
    print(f"  Verify in browser: {BASE}/courses/{dest['id']}/settings#tab-sections")


if __name__ == "__main__":
    main()
