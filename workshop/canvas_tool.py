"""canvas_tool.py — FCC Chem starter script.
THE THREE TOKEN RULES: never in a repo, never hardcoded,
never in an AI chat. Leaked = revoke in Canvas immediately.
This script reads the token from .env — it contains no secret,
so the script itself is safe to paste into an AI chat."""
import os, sys
from pathlib import Path
import requests

# --- load .env from this script's folder ---
env = Path(__file__).resolve().parent / ".env"
if not env.exists():
    sys.exit("No .env found next to this script — do Phase 1 first.")
for line in env.read_text().splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

TOKEN = os.environ.get("CANVAS_TOKEN")
URL = os.environ.get("CANVAS_URL", "https://scccd.instructure.com").rstrip("/")
COURSE = os.environ.get("SANDBOX_COURSE_ID")
if not TOKEN or "paste-your" in TOKEN or not COURSE:
    sys.exit("Fill in CANVAS_TOKEN and SANDBOX_COURSE_ID in .env first.")
H = {"Authorization": "Bearer " + TOKEN}

# --- Section 1: connectivity proof (a read — changes nothing) ---
r = requests.get(URL + "/api/v1/courses/" + COURSE, headers=H)
r.raise_for_status()
print("Connected to:", r.json()["name"])

# --- Section 2: list assignments ---
r = requests.get(URL + "/api/v1/courses/" + COURSE + "/assignments",
                 headers=H, params={"per_page": 50})
r.raise_for_status()
assignments = r.json()
if not assignments:
    sys.exit("No assignments here yet — create one in Canvas, then rerun.")
for i, a in enumerate(assignments):
    print("[" + str(i) + "]", a["name"], "· due:", a.get("due_at") or "none")

# --- Section 3: dry run, confirm, then change ONE due date ---
pick = input("\nNumber of the assignment to change"
             " (dept sandbox: ONLY the one with your name), or Enter to quit: ").strip()
if pick == "":
    sys.exit("Stopped after the read-only sections. Nothing was changed.")
a = assignments[int(pick)]
new_due = input("New due date (YYYY-MM-DD): ").strip() + "T23:59:00Z"
print("\nDRY RUN — this is what the script is ABOUT to do:")
print("  course:    ", COURSE)
print("  assignment:", a["name"])
print("  due date:  ", a.get("due_at") or "none", " ->", new_due)
if input('Type YES to make this change for real: ').strip() != "YES":
    sys.exit("Cancelled. Nothing was changed.")
r = requests.put(URL + "/api/v1/courses/" + COURSE + "/assignments/" + str(a["id"]),
                 headers=H, json={"assignment": {"due_at": new_due}})
r.raise_for_status()
print("Done. Refresh the assignment in Canvas and look at the due date.")
