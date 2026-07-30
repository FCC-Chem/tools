#!/usr/bin/env python3
"""
Weekly grade update emailer -- TEMPLATE

Reads a gradebook export, computes each student's current standing, and
emails them a short summary.

SAFETY MODEL -- read this before changing anything:

  * Dry run is the DEFAULT. Running this sends nothing. It prints the
    messages it would send. You must pass --send to actually send mail.
  * Credentials come from a .env file that is never committed.
  * The gradebook file is never committed. .gitignore blocks *.csv
    except sample_*.csv.

Usage:

    python3 script.py --roster sample_roster.csv            # dry run
    python3 script.py --roster sample_roster.csv --student "Rivera, Ana"
    python3 script.py --roster real_export.csv --send       # actually sends

See SPEC.md for the file format and for how to adapt this to your course.
"""

import argparse
import csv
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

# ---------------------------------------------------------------------
# COURSE SETTINGS -- edit these, or better, tell an AI assistant to.
# ---------------------------------------------------------------------
COURSE_NAME = "CHEM 1A"
INSTRUCTOR = "Your Name"
OFFICE_HOURS = "Tue/Thu 1-2pm, Science 214"

# Category weights must sum to 1.0. Verified at startup.
WEIGHTS = {
    "homework": 0.20,
    "quizzes": 0.15,
    "labs": 0.20,
    "exams": 0.45,
}

# Letter grade cutoffs, checked highest first.
CUTOFFS = [(89.5, "A"), (79.5, "B"), (69.5, "C"), (59.5, "D"), (0.0, "F")]

# Students at or below this percentage get the concern message.
CONCERN_BELOW = 70.0


# ---------------------------------------------------------------------
# Credentials -- from environment, never hardcoded.
# ---------------------------------------------------------------------
def load_env(path=".env"):
    """Minimal .env reader so the template has no pip dependencies."""
    p = Path(path)
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def smtp_settings():
    missing = [k for k in ("SMTP_HOST", "SMTP_USER", "SMTP_PASS", "FROM_EMAIL")
               if not os.environ.get(k)]
    if missing:
        sys.exit(
            "Missing credentials: " + ", ".join(missing) +
            "\nCopy .env.example to .env and fill it in. Never commit .env."
        )
    return {
        "host": os.environ["SMTP_HOST"],
        "port": int(os.environ.get("SMTP_PORT", "587")),
        "user": os.environ["SMTP_USER"],
        "password": os.environ["SMTP_PASS"],
        "from": os.environ["FROM_EMAIL"],
    }


# ---------------------------------------------------------------------
# Grade computation
# ---------------------------------------------------------------------
def pct(earned, possible):
    """Category percentage. A category with nothing graded yet is dropped
    rather than counted as a zero -- counting it as zero is the single
    most common bug in scripts like this, and it panics students in
    week 3."""
    return None if possible <= 0 else 100.0 * earned / possible


def compute(row):
    parts, used_weight = {}, 0.0
    for cat, w in WEIGHTS.items():
        try:
            earned = float(row.get(f"{cat}_earned", "") or 0)
            possible = float(row.get(f"{cat}_possible", "") or 0)
        except ValueError:
            earned = possible = 0.0
        p = pct(earned, possible)
        parts[cat] = p
        if p is not None:
            used_weight += w

    if used_weight <= 0:
        return None, parts

    # Renormalize over categories that actually have graded work.
    total = sum(WEIGHTS[c] * p for c, p in parts.items() if p is not None)
    return total / used_weight, parts


def letter(overall):
    for cut, ltr in CUTOFFS:
        if overall >= cut:
            return ltr
    return "F"


# ---------------------------------------------------------------------
# Message
# ---------------------------------------------------------------------
def build_message(name, overall, parts):
    first = name.split(",")[-1].strip() if "," in name else name.split()[0]
    lines = [
        f"Hi {first},",
        "",
        f"Here is your current standing in {COURSE_NAME}:",
        "",
        f"  Overall: {overall:.1f}%  ({letter(overall)})",
        "",
    ]
    for cat in WEIGHTS:
        p = parts.get(cat)
        lines.append(f"  {cat.capitalize():<10} " +
                     ("not yet graded" if p is None else f"{p:.1f}%"))
    lines += ["", ]

    if overall < CONCERN_BELOW:
        lines += [
            "This is below where you'll want to be. That is fixable, and",
            "earlier is much easier than later. Come see me:",
            f"  {OFFICE_HOURS}",
            "",
        ]
    else:
        lines += ["Nice work. Keep it going.", ""]

    lines += [
        "This is an automated summary. Grades in Canvas are authoritative;",
        "if something here looks wrong, tell me and I'll check it.",
        "",
        INSTRUCTOR,
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------
def load_roster(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        sys.exit(f"{path} has no data rows.")
    for req in ("name", "email"):
        if req not in rows[0]:
            sys.exit(f"{path} is missing a '{req}' column. See SPEC.md.")
    return rows


def main():
    ap = argparse.ArgumentParser(description="Weekly grade update emailer")
    ap.add_argument("--roster", default="sample_roster.csv",
                    help="CSV export (default: sample_roster.csv)")
    ap.add_argument("--student", help="Only this student. Substring match, case-insensitive.")
    ap.add_argument("--send", action="store_true",
                    help="Actually send email. Without this, prints and sends nothing.")
    args = ap.parse_args()

    if abs(sum(WEIGHTS.values()) - 1.0) > 1e-9:
        sys.exit(f"WEIGHTS must sum to 1.0, got {sum(WEIGHTS.values())}")

    rows = load_roster(args.roster)

    if args.student:
        needle = args.student.lower()
        rows = [r for r in rows if needle in r["name"].lower()]
        if not rows:
            sys.exit(f"No student matching {args.student!r}.")

    server = None
    if args.send:
        load_env()
        cfg = smtp_settings()
        print(f"Connecting to {cfg['host']}:{cfg['port']} ...")
        server = smtplib.SMTP(cfg["host"], cfg["port"])
        server.starttls()
        server.login(cfg["user"], cfg["password"])

    sent = skipped = 0
    for r in rows:
        overall, parts = compute(r)
        if overall is None:
            print(f"-- {r['name']}: nothing graded yet, skipping")
            skipped += 1
            continue

        body = build_message(r["name"], overall, parts)
        subject = f"{COURSE_NAME} grade update - {overall:.1f}% ({letter(overall)})"

        if args.send:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = cfg["from"]
            msg["To"] = r["email"]
            msg.set_content(body)
            server.send_message(msg)
            print(f"SENT  {r['email']}  {overall:.1f}%")
        else:
            print("=" * 66)
            print(f"TO:      {r['email']}")
            print(f"SUBJECT: {subject}")
            print("-" * 66)
            print(body)
        sent += 1

    if server:
        server.quit()

    print("=" * 66)
    if args.send:
        print(f"Sent {sent} message(s). Skipped {skipped}.")
    else:
        print(f"DRY RUN. {sent} message(s) would be sent, {skipped} skipped.")
        print("Nothing was emailed. Add --send when you are ready.")


if __name__ == "__main__":
    main()
