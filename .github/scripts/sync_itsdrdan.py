#!/usr/bin/env python3
"""
Copies Dr. Dan's games into ONE catalog entry: itsdrdan/study-games/.

    itsdrdan/study-games/index.html        launcher page (the one card in the catalog)
    itsdrdan/study-games/meta.json         catalog card text
    itsdrdan/study-games/<game>/           a copy of each game (index.html, meta.json, assets/)
    itsdrdan/study-games/logos/<game>.webp game thumbnails

The game list comes from Dr. Dan's study hub (ItsDrDan/games, data/hub.js), so a
game added to the hub shows up here automatically. Each game's files come from
its own repo, ItsDrDan/<game>.

The catalog builder treats study-games/ as a collection: each game gets its
own card in Dr. Dan's section, and the launcher is offered as an "open all" link.

Everything else in itsdrdan/ is removed. Nothing outside itsdrdan/ is touched.
If one game repo can't be fetched, its previous copy is kept.

Run from the repository root:  python3 .github/scripts/sync_itsdrdan.py
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTHOR = ROOT / "itsdrdan"
DEST = AUTHOR / "study-games"
# Short topic names for the catalog card. A game not listed here uses the
# words in parentheses in its hub title, or the title itself.
TOPICS = {
    "sigfig": "Sig figs", "metric": "Metric prefixes", "algebratrainer": "Algebra",
    "elements": "Element symbols", "polyatomic": "Polyatomic ions", "ionicformula": "Naming",
    "moles": "Moles", "stoichiometry": "Stoichiometry", "gaslaws": "Gas laws",
    "thermochemistry": "Thermochemistry", "reactions": "Reactions", "redox": "Redox",
    "quantumchemistry": "Quantum", "lewisstructures": "Lewis structures",
    "chem1bready": "1B readiness", "organic": "Functional groups",
    "functionalgroups": "Organic families", "organicreactions": "Organic reactions",
    "carbohydrates": "Carbohydrates", "finalexam": "Final exam review",
}
TEMPLATE = ROOT / ".github" / "itsdrdan" / "launcher.html"
OWNER = "https://github.com/ItsDrDan"


def clone(repo, into):
    r = subprocess.run(["git", "clone", "-q", "--depth", "1", f"{OWNER}/{repo}.git", str(into)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"::warning::Could not fetch ItsDrDan/{repo}; keeping the old copy")
        return False
    return True


def read_hub(hub_dir):
    text = (hub_dir / "data" / "hub.js").read_text(encoding="utf-8")
    data = json.loads(text[text.index("{"): text.rindex("}") + 1])
    hide = set(data.get("hide", []))
    games = []
    for g in data.get("games", []):
        gid = str(g.get("id", "")).strip()
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", gid) or gid in hide or gid in ("logos",):
            continue
        games.append({
            "id": gid,
            "title": g.get("title") or gid,
            "blurb": g.get("blurb") or "",
            "courses": [c for c in g.get("courses", []) if c in ("3A", "1A", "3B", "1B")],
            "icon": g.get("icon") or "flask",
            "hub_logo": g.get("logo") or "",
        })
    return games


def topic(g):
    if g["id"] in TOPICS:
        return TOPICS[g["id"]]
    m = re.search(r"\(([^)]+)\)", g["title"])
    return (m.group(1) if m else g["title"]).strip()


def copy_game(src, dst):
    if not (src / "index.html").is_file() or (src / "index.html").stat().st_size == 0:
        print(f"::warning::{src.name} has no index.html; keeping the old copy")
        return False
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    shutil.copy2(src / "index.html", dst / "index.html")
    meta = src / "meta.json"
    if meta.is_file():
        try:
            json.loads(meta.read_text(encoding="utf-8"))
            shutil.copy2(meta, dst / "meta.json")
        except (ValueError, UnicodeDecodeError):
            print(f"::warning::{src.name}/meta.json is not valid JSON; skipped it")
    if (src / "assets").is_dir():
        shutil.copytree(src / "assets", dst / "assets")
    return True


def icon_symbols(hub_dir, names):
    sprite = (hub_dir / "assets" / "icons.svg").read_text(encoding="utf-8")
    out = []
    for n in sorted(names):
        m = re.search(rf'<symbol id="i-{re.escape(n)}".*?</symbol>', sprite, re.S)
        if m:
            out.append(m.group(0))
    return "".join(out)


def main():
    work = Path(tempfile.mkdtemp())
    hub = work / "games"
    if not clone("games", hub):
        sys.exit("Could not fetch the study hub (ItsDrDan/games); nothing changed.")
    games = read_hub(hub)
    if not games:
        sys.exit("The study hub lists no games; nothing changed.")

    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / "logos").mkdir(exist_ok=True)
    listed = []
    for g in games:
        src = work / g["id"]
        ok = clone(g["id"], src) and copy_game(src, DEST / g["id"])
        if not ok and not (DEST / g["id"] / "index.html").exists():
            continue  # never fetched successfully; leave it off the page
        logo = hub / g["hub_logo"] if g["hub_logo"] else None
        if logo and logo.is_file():
            shutil.copy2(logo, DEST / "logos" / f"{g['id']}{logo.suffix}")
            g["logo"] = f"logos/{g['id']}{logo.suffix}"
        listed.append(g)
        print(f"== {g['id']}{'' if ok else ' (kept old copy)'}")

    # Remove games no longer on the hub, old logos, and the old one-folder-per-game layout.
    keep = {g["id"] for g in listed} | {"logos", "index.html", "meta.json"}
    for p in DEST.iterdir():
        if p.name not in keep:
            shutil.rmtree(p) if p.is_dir() else p.unlink()
    logo_keep = {Path(g["logo"]).name for g in listed if g.get("logo")}
    for p in (DEST / "logos").iterdir():
        if p.name not in logo_keep:
            p.unlink()
    for p in AUTHOR.iterdir():
        if p != DEST:
            shutil.rmtree(p) if p.is_dir() else p.unlink()

    # Launcher page.
    page_games = [{k: g[k] for k in ("id", "title", "blurb", "courses", "icon", "logo") if k in g} for g in listed]
    icons = icon_symbols(hub, {g["icon"] for g in listed if not g.get("logo")} | {"flask"})
    logo_svg = re.sub(r"<\?xml.*?\?>", "", (hub / "assets" / "logo.svg").read_text(encoding="utf-8")).strip()
    page = TEMPLATE.read_text(encoding="utf-8")
    page = page.replace("/*GAMES*/[]", json.dumps(page_games, ensure_ascii=False, indent=1).replace("</", "<\\/"))
    page = page.replace("<!--ICONS-->", icons).replace("<!--LOGO-->", logo_svg)
    (DEST / "index.html").write_text(page, encoding="utf-8")

    # The single catalog card.
    courses = [c for c in ("3A", "1A", "3B", "1B") if any(c in g["courses"] for g in listed)]
    meta = {
        "title": "Dr. Dan's Chemistry Study Games",
        "author": "Dr. Dan (ItsDrDan)",
        "summary": " · ".join(topic(g) for g in listed),
        "course": ", ".join(f"CHEM {c}" for c in courses),
        "description": f"{len(listed)} practice games in one place, sorted by course: significant figures and the mole "
                       "through stoichiometry, gas laws, thermochemistry, redox, quantum, Lewis structures, organic "
                       "reactions, carbohydrates and final exam review. Open it to pick a course and copy a game link "
                       "for Canvas.",
        # Every game title is a hidden tag, so catalog search finds this card.
        "tags": ["study games", "practice", "CHEM 3A", "CHEM 1A", "CHEM 1B", "CHEM 3B", "final exam review"]
                + [g["title"] for g in listed],
        "cardTags": ["study games"],
        "status": "working",
        "accent": "#7563d9",
        "pinned": True,
    }
    (DEST / "meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    shutil.rmtree(work, ignore_errors=True)
    print(f"Launcher lists {len(listed)} games.")


if __name__ == "__main__":
    main()
