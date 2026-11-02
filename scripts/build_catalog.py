#!/usr/bin/env python3
"""
Scans every author folder for tools and regenerates the root index.html catalog.

Layout:

    <author>/<tool>/index.html      <- required
    <author>/<tool>/meta.json       <- optional
    <author>/<tool>/README.md       <- optional

An "author folder" is any top-level directory that does not start with . or _
and is not in SKIP_NAMES. A "tool folder" is any directory inside it that
contains an index.html.

Collections. A tool folder whose own subfolders contain index.html files is a
*collection* (e.g. itsdrdan/study-games/, which the sync workflow fills with
one game per subfolder plus a launcher page). Each subfolder becomes its own
card, attributed to the author, and the collection's index.html is offered in
the author's section header as an "open all" link rather than as a card. This
is what lets a contributor who publishes twenty games through one launcher be
counted as twenty tools, not one.

The page is grouped into one section per author, largest contributor first
(tool count, then total opens when usage counts exist, then name). Each
section shows SHOW_FIRST cards and folds the rest behind a "Show N more"
button; any search or filter unfolds everything so a match is never hidden.

Authorship is structural, not conventional. The author name is derived from the
folder, so a contributor who forgets meta.json entirely still gets a correctly
attributed card. meta.json "author" overrides the folder name when someone
wants a display name ("R. Gilley" instead of "gilley").

Nothing here can fail the build. A missing meta.json, malformed JSON, a stray
index.html at the top level, or an empty author folder all produce a warning
and keep going -- one person's bad file must never block everyone else's push.

Run:  python3 scripts/build_catalog.py
"""

import json
import os
import re
import html
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
SKIP_PREFIXES = (".", "_")
SKIP_NAMES = {"scripts", "workshop", "node_modules"}
IMAGE_EXTS = (".webp", ".png", ".jpg", ".jpeg", ".svg", ".gif")
THUMB_STEM = "thumb"   # <tool>/thumb.<ext> is picked up automatically

# =====================================================================
# Generic card icons.
#
# A tool with no image of its own gets a line icon chosen from its title,
# tags and folder name. First match wins, so the list is ordered from
# specific to general. Each icon is a 24x24 stroke path drawn in the
# card's accent color. Drop a thumb.png into the tool folder (or set
# "image" in meta.json) and the icon is replaced on the next build.
# =====================================================================
ICON_PATHS = {
    "flask":     "M9 3h6M10 3v6l-5.4 9.9A1.5 1.5 0 0 0 5.9 21h12.2a1.5 1.5 0 0 0 1.3-2.1L14 9V3M7.5 16h9",
    "balance":   "M12 4v17M7 21h10M12 6 5 8M12 6l7 2M2.5 15 5 8l2.5 7a2.5 2.5 0 0 1-5 0ZM16.5 15 19 8l2.5 7a2.5 2.5 0 0 1-5 0Z",
    "burette":   "M11 2h2v10h-2ZM13 4h1.5M13 7h1.5M13 10h1.5M9.5 12.5h5l-1 2.5h-3ZM12 16.5V18M9 22h6l-1.5-3h-3Z",
    "molecule":  "M12 5.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM5 20.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM19 20.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM12 5.5v5M12 10.5l-5.5 5.5M12 10.5l5.5 5.5",
    "piston":    "M6 8h12v13H6ZM6 13h12M12 13V4M9 4h6M9.5 17h.01M14.5 18.5h.01M12 15.8h.01M10.5 19.8h.01",
    "magnifier": "M10.5 17a6.5 6.5 0 1 0 0-13 6.5 6.5 0 0 0 0 13ZM15.5 15.5 21 21M8 10.5h5M10.5 8v5",
    "ruler":     "M3 16 16 3l5 5L8 21ZM7 12l2 2M10 9l2 2M13 6l2 2M5.5 14.5 7 16",
    "terminal":  "M3 5h18v14H3ZM7 9l3 3-3 3M12 15h5",
    "ions":      "M7 15.5a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9ZM17 17.5a4.5 4.5 0 1 0 0-9 4.5 4.5 0 0 0 0 9ZM5 11h4M7 9v4M15 13h4",
    "algebra":   "M2 14l2.5 4L9 6h12M12 11l5 7M17 11l-5 7",
    "atom":      "M12 13.2a1.2 1.2 0 1 0 0-2.4 1.2 1.2 0 0 0 0 2.4ZM3 12a9 3.5 0 1 0 18 0a9 3.5 0 1 0-18 0M7.5 4.21a9 3.5 60 1 0 9 15.58a9 3.5 60 1 0-9-15.58M7.5 19.79a9 3.5-60 1 0 9-15.58a9 3.5-60 1 0-9 15.58",
    "thermo":    "M12 3a2.5 2.5 0 0 0-2.5 2.5v8.3a4 4 0 1 0 5 0V5.5A2.5 2.5 0 0 0 12 3ZM12 18.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM12 15.5v-8M16 7h3M16 10h3",
    "redox":     "M4 8h13M14 5l3 3-3 3M20 16H7M10 13l-3 3 3 3",
    "reaction":  "M6 9a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM6 17a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5ZM6 9v3M10.5 10.5h4M12.5 8.5l2 2-2 2M19 13.5a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM4 21h16",
    "exam":      "M6 3h12v18H6ZM9 3V1.5h6V3M9 9l1.5 1.5L13 8M9 14l1.5 1.5L13 13M14.5 9H16M14.5 14H16",
    "ring":      "M12 3l7.8 4.5v9L12 21l-7.8-4.5v-9ZM12 7.5l3.9 2.25v4.5L12 16.5l-3.9-2.25v-4.5Z",
    "grid":      "M3 3h4v4H3ZM10 3h4v4h-4ZM17 3h4v4h-4ZM3 10h4v4H3ZM10 10h4v4h-4ZM17 10h4v4h-4ZM3 17h4v4H3ZM10 17h4v4h-4ZM17 17h4v4h-4Z",
    "embed":     "M3 5h18v14H3ZM7 10l-2 2 2 2M17 10l2 2-2 2M13.5 9l-3 6",
}

# (icon, keywords) -- matched against title, tags and folder name, in order.
ICON_RULES = [
    ("embed",     ("canvas embed", "iframe", "wrapper")),
    ("burette",   ("titration", "acid-base", "acid base", "acids and bases", "ph scale", "ph curve", "neutralization")),
    ("balance",   ("stoichiometry", "stoich", "molar mass", "mole ", "moles", "limiting")),
    ("piston",    ("gas law", "gas laws", "pressure", "kinetic molecular")),
    ("thermo",    ("thermochem", "thermo", "heat", "calorim", "enthalpy")),
    ("redox",     ("redox", "oxidation", "reduction")),
    ("ring",      ("carbohydrate", "sugar", "saccharide")),
    ("molecule",  ("lewis", "model kit", "modeling", "vsepr", "molecular shape", "bond",
                   "organic", "functional group", "hydrocarbon", "structure")),
    ("atom",      ("quantum", "orbital", "electron config", "atomic structure")),
    ("ions",      ("ionic", "nomenclature", "naming", "polyatomic", "formula")),
    ("grid",      ("element symbol", "periodic", "element study")),
    ("algebra",   ("algebra", "rearrang", "math")),
    ("reaction",  ("reaction", "equation", "balancing", "particle", "mixture")),
    ("ruler",     ("dimensional analysis", "unit", "metric", "si prefix", "sig fig",
                   "significant", "measurement", "conversion")),
    ("exam",      ("final exam", "exam review", "readiness", "review", "quiz")),
    ("magnifier", ("mystery", "investigat", "detective", "case")),
]


def pick_icon(t):
    """Keyword match over the tool's words. Scripts always get the terminal."""
    if t["kind"] == "script":
        return "terminal"
    blob = " ".join([t["title"], " ".join(t["tags"]), t["folder"].split("/")[-1].replace("-", " ")]).lower()
    for icon, keys in ICON_RULES:
        if any(k in blob for k in keys):
            return icon
    return "flask"


def find_image(tool_dir, meta, rel, collection_dir=None, warnings=None):
    """Where a card's picture comes from, in order:

        meta.json "image"            a file inside the tool folder
        <tool>/thumb.<ext>           by convention
        <collection>/logos/<tool>.*  what the study-games sync ships

    Returns a path relative to the repository root, or "" for none.
    """
    declared = str(meta.get("image") or "").strip()
    if declared:
        cand = (tool_dir / declared)
        inside = cand.resolve().is_relative_to(tool_dir.resolve()) if hasattr(Path, "is_relative_to") else True
        if inside and cand.is_file() and cand.suffix.lower() in IMAGE_EXTS:
            return f"{rel}/{declared}"
        if warnings is not None:
            warnings.append(f'{rel}/meta.json "image": {declared} not found inside the tool folder - ignored')
    for ext in IMAGE_EXTS:
        if (tool_dir / f"{THUMB_STEM}{ext}").is_file():
            return f"{rel}/{THUMB_STEM}{ext}"
    if collection_dir is not None:
        for ext in IMAGE_EXTS:
            cand = collection_dir / "logos" / f"{tool_dir.name}{ext}"
            if cand.is_file():
                return f"{rel.rsplit('/', 1)[0]}/logos/{tool_dir.name}{ext}"
    return ""
SHOW_FIRST = 3      # cards visible per author before "Show N more"; searching or filtering shows all

STATUS_LABELS = {
    "working": ("Working", "#1f6f43"),
    "stable": ("Stable", "#1f6f43"),
    "wip": ("Work in progress", "#b26a00"),
}

# =====================================================================
# Rotating FCC unit cell hero.
#
# Geometry is physically correct: atoms touch along the face diagonal,
# so 4r = a*sqrt(2)  ->  r = a*sqrt(2)/4 = 0.35355*a.
#
# Corner atoms are rendered as solid eighth-spheres, face atoms as solid
# half-spheres -- the portion actually inside the unit cell. Each solid
# is a partial sphere shell plus flat caps, because Three.js clipping
# planes leave hollow openings.
#
# Degrades safely: if WebGL is unavailable or the CDN is blocked, the
# block hides itself and the catalog below is unaffected.
# =====================================================================
HERO = r"""    <div class="mark" id="hero">
      <canvas id="fcc" role="img" aria-label="Face-centered cubic unit cell"></canvas>
    </div>"""

# Loaded at the end of <body> so the Three.js download never blocks
# rendering of the catalog itself.
HERO_SCRIPT = r"""
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
  (function () {
    var host = document.getElementById('hero');
    var canvas = document.getElementById('fcc');

    function bail() { if (host) host.style.display = 'none'; }
    if (!window.THREE || !canvas) { bail(); return; }

    var renderer;
    try {
      renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    } catch (e) { bail(); return; }

    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.outputEncoding = THREE.sRGBEncoding;

    var scene = new THREE.Scene();
    // Narrow FOV at a longer distance: less perspective distortion, so
    // the cell reads as a compact symbol rather than a wide-angle shot.
    var camera = new THREE.PerspectiveCamera(26, 1, 0.1, 100);

    // ---- lattice constants -------------------------------------
    var A = 2.0;                       // cube edge
    var R = A * Math.SQRT2 / 4;        // atomic radius, atoms touch on face diagonal
    var H = A / 2;

    var RED  = new THREE.MeshStandardMaterial({ color: 0x8f1d1d, roughness: 0.34, metalness: 0.0 });
    var GRAY = new THREE.MeshStandardMaterial({ color: 0x585c60, roughness: 0.40, metalness: 0.0 });

    // Flat caps are single-sided discs seen from either side depending
    // on the octant, so they render DoubleSide. Three.js flips the
    // normal for back faces in the shader, so lighting stays correct.
    function capMat(base) {
      var m = base.clone(); m.side = THREE.DoubleSide; return m;
    }
    var REDC = capMat(RED), GRAYC = capMat(GRAY);

    // ---- solid eighth-sphere occupying x<=0, y>=0, z>=0 ---------
    function octant(mat, capmat) {
      var g = new THREE.Group();

      g.add(new THREE.Mesh(
        new THREE.SphereGeometry(R, 44, 22, 0, Math.PI / 2, 0, Math.PI / 2), mat));

      // cap on z = 0 plane  (quadrant x<0, y>0)
      var cz = new THREE.Mesh(new THREE.CircleGeometry(R, 28, Math.PI / 2, Math.PI / 2), capmat);
      g.add(cz);

      // cap on y = 0 plane  (quadrant x<0, z>0)
      var cy = new THREE.Mesh(new THREE.CircleGeometry(R, 28, Math.PI / 2, Math.PI / 2), capmat);
      cy.rotation.x = Math.PI / 2;
      g.add(cy);

      // cap on x = 0 plane  (quadrant y>0, z>0)
      var cx = new THREE.Mesh(new THREE.CircleGeometry(R, 28, 0, Math.PI / 2), capmat);
      cx.rotation.y = -Math.PI / 2;
      g.add(cx);

      return g;
    }

    // ---- solid hemisphere, flat cap at y=0, solid toward +y -----
    function hemi(mat, capmat) {
      var g = new THREE.Group();
      g.add(new THREE.Mesh(
        new THREE.SphereGeometry(R, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), mat));
      var c = new THREE.Mesh(new THREE.CircleGeometry(R, 48), capmat);
      c.rotation.x = Math.PI / 2;
      g.add(c);
      return g;
    }

    var cell = new THREE.Group();

    // 8 corners: [sx, sy, sz, rotY, rotX]
    //
    // Base octant is (-,+,+). The cube rotation group maps it to every
    // other octant, so no mirroring -- and therefore no flipped
    // normals -- is ever needed.
    //
    // The wedge at corner (sx,sy,sz) must occupy the octant pointing
    // INTO the cell, i.e. (-sx,-sy,-sz). Getting this backwards puts
    // all eight wedges outside the cube, which still looks plausible
    // at a glance and is completely wrong.
    var CORNERS = [
      [-1,  1,  1,  Math.PI / 2,  Math.PI],   // -> (+,-,-)
      [ 1,  1,  1,  0,            Math.PI],   // -> (-,-,-)
      [ 1,  1, -1, -Math.PI / 2,  Math.PI],   // -> (-,-,+)
      [-1,  1, -1,  Math.PI,      Math.PI],   // -> (+,-,+)
      [-1, -1, -1,  Math.PI / 2,  0       ],  // -> (+,+,+)
      [ 1, -1, -1,  0,            0       ],  // -> (-,+,+)
      [ 1, -1,  1, -Math.PI / 2,  0       ],  // -> (-,+,-)
      [-1, -1,  1,  Math.PI,      0       ]   // -> (+,+,-)
    ];

    CORNERS.forEach(function (c) {
      // Wrapper carries the position and the X flip; the inner group
      // carries the Y spin. Net transform on the geometry is
      // rotX(c[4]) * rotY(c[3]), which is exactly the mapping derived
      // above. An object's own rotation never moves its own position.
      var o = octant(RED, REDC);
      o.rotation.y = c[3];
      var w = new THREE.Group();
      w.add(o);
      w.rotation.x = c[4];
      w.position.set(c[0] * H, c[1] * H, c[2] * H);
      cell.add(w);
    });

    // 6 face centers. Keep the half inside the cell, so the solid
    // points along -n and the flat cap sits flush with the face.
    var UP = new THREE.Vector3(0, 1, 0);
    [[1,0,0], [-1,0,0], [0,1,0], [0,-1,0], [0,0,1], [0,0,-1]].forEach(function (n) {
      var v = new THREE.Vector3(n[0], n[1], n[2]);
      var m = hemi(GRAY, GRAYC);
      m.quaternion.setFromUnitVectors(UP, v.clone().negate());
      m.position.copy(v).multiplyScalar(H);
      cell.add(m);
    });

    scene.add(cell);

    // ---- lighting ----------------------------------------------
    scene.add(new THREE.AmbientLight(0xffffff, 0.55));
    var key = new THREE.DirectionalLight(0xffffff, 0.85);
    key.position.set(4, 6, 7);
    scene.add(key);
    var fill = new THREE.DirectionalLight(0xffffff, 0.35);
    fill.position.set(-6, -2, -4);
    scene.add(fill);
    var rim = new THREE.DirectionalLight(0xffffff, 0.25);
    rim.position.set(-2, 5, -6);
    scene.add(rim);

    // ---- sizing -------------------------------------------------
    // The cell's bounding radius is sqrt(3)*a/2. At 26 deg vertical
    // FOV the half-height at distance d is d*tan(13 deg) = 0.2309d,
    // so d >= 1.732/0.2309 = 7.5 to fit. 8.6 leaves a margin at every
    // rotation angle.
    function resize() {
      var s = host.clientWidth || 104;
      renderer.setSize(s, s, false);
      camera.aspect = 1;
      camera.updateProjectionMatrix();
      camera.position.set(0, 0, 8.6);
      camera.lookAt(0, 0, 0);
    }
    window.addEventListener('resize', resize);
    resize();

    cell.rotation.x = 0.42;
    cell.rotation.y = 0.6;

    // ---- interaction --------------------------------------------
    var drag = false, px = 0, py = 0;
    var SPIN = 0.0055;   // radians per frame, ~19 s per revolution

    function down(x, y) { drag = true; px = x; py = y; }
    function move(x, y) {
      if (!drag) return;
      cell.rotation.y += (x - px) * 0.01;
      cell.rotation.x += (y - py) * 0.01;
      px = x; py = y;
    }
    function up() { drag = false; }

    canvas.addEventListener('mousedown', function (e) { down(e.clientX, e.clientY); });
    window.addEventListener('mousemove', function (e) { move(e.clientX, e.clientY); });
    window.addEventListener('mouseup', up);
    canvas.addEventListener('touchstart', function (e) {
      down(e.touches[0].clientX, e.touches[0].clientY);
    }, { passive: true });
    canvas.addEventListener('touchmove', function (e) {
      move(e.touches[0].clientX, e.touches[0].clientY);
    }, { passive: true });
    canvas.addEventListener('touchend', up);

    // ---- loop ----------------------------------------------------
    var reduce = window.matchMedia &&
                 window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var visible = true;
    document.addEventListener('visibilitychange', function () {
      visible = !document.hidden;
    });

    function tick() {
      requestAnimationFrame(tick);
      if (!visible) return;                       // no work in a hidden tab
      if (!drag && !reduce) cell.rotation.y += SPIN;
      renderer.render(scene, camera);
    }
    tick();
  })();
</script>
"""


def prettify(slug):
    """'molar-mass' -> 'Molar Mass'.  Used when meta.json has no title."""
    return " ".join(w.capitalize() for w in slug.replace("_", "-").split("-") if w)


def read_meta(tool_dir, rel, warnings):
    """Never raises. A bad meta.json degrades to defaults plus a warning."""
    meta_path = tool_dir / "meta.json"
    if not meta_path.exists():
        warnings.append(f"{rel}/ has no meta.json - using folder-derived defaults")
        return {}
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if not isinstance(meta, dict):
            raise ValueError("must be a JSON object")
        return meta
    except Exception as e:
        warnings.append(f"{rel}/meta.json could not be read ({e}) - using defaults")
        return {}


def is_tool_dir(p):
    """A browser tool announces itself with index.html; a script tool has no
    index.html, so meta.json is what marks the folder as a deliberate
    contribution rather than clutter."""
    return p.is_dir() and not p.name.startswith(SKIP_PREFIXES) and (
        (p / "index.html").exists() or (p / "meta.json").exists()
    )


def is_collection(tool_dir):
    """A tool folder that itself contains tool folders with index.html.

    Asset folders (logos/, assets/) have no index.html and do not count,
    so an ordinary tool with a subfolder of images is never mistaken for
    a collection.
    """
    if not (tool_dir / "index.html").exists():
        return False
    return any(
        p.is_dir() and not p.name.startswith(SKIP_PREFIXES) and (p / "index.html").exists()
        for p in tool_dir.iterdir()
    )


def tool_entry(author_dir, tool_dir, rel, warnings, collection_dir=None):
    """Build one catalog record. Never raises."""
    meta = read_meta(tool_dir, rel, warnings)

    tags = meta.get("tags", [])
    if not isinstance(tags, list):
        tags = []

    status = str(meta.get("status", "wip")).lower()
    if status not in STATUS_LABELS:
        status = "wip"

    has_html = (tool_dir / "index.html").exists()

    # "web" tools open in the browser. "script" tools are run
    # locally and have no live URL. Declared kind wins; otherwise
    # the presence of index.html decides.
    kind = str(meta.get("kind", "")).lower()
    if kind not in ("web", "script"):
        kind = "web" if has_html else "script"
    if kind == "web" and not has_html:
        warnings.append(
            f'{rel}/ declares kind "web" but has no index.html - treating as script'
        )
        kind = "script"

    spec = next((f for f in ("SPEC.md", "spec.md") if (tool_dir / f).exists()), None)
    entry_file = str(meta.get("entry") or "")
    if not entry_file and kind == "script":
        found = sorted(
            p.name for p in tool_dir.iterdir()
            if p.is_file() and p.suffix in (".py", ".sh", ".ps1", ".rb", ".js")
        )
        entry_file = found[0] if found else ""

    # A title that ends in the author's own handle ("Gas Laws — ItsDrDan")
    # is redundant inside that author's section, so the suffix is dropped.
    title = str(meta.get("title") or prettify(tool_dir.name))
    title = re.sub(rf"\s*[—–-]\s*{re.escape(author_dir.name)}\s*$", "", title, flags=re.I).strip() or title

    t = {
        "folder": rel,
        "author_slug": author_dir.name,
        "kind": kind,
        "entry": entry_file,
        "requires": str(meta.get("requires") or ("Python 3" if kind == "script" else "")),
        "title": title,
        # Folder name is the fallback author. meta.json only overrides
        # it to provide a nicer display name.
        "author": str(meta.get("author") or prettify(author_dir.name)),
        "course": str(meta.get("course") or ""),
        "description": str(meta.get("description") or "No description yet."),
        # Optional short card text. When present, the card shows
        # "summary" and "cardTags"; the full description and tags
        # are still searched.
        "summary": str(meta.get("summary") or ""),
        "card_tags": [str(x) for x in meta.get("cardTags", [])]
                     if isinstance(meta.get("cardTags"), list) else None,
        "tags": [str(t) for t in tags],
        "status": status,
        # "pinned": true keeps this card first within its author's section.
        "pinned": meta.get("pinned") is True,
        # Optional card color, e.g. "accent": "#7563d9". Only a plain
        # #rrggbb value is accepted; anything else keeps the default.
        "accent": (str(meta.get("accent") or "")
                   if re.fullmatch(r"#[0-9a-fA-F]{6}", str(meta.get("accent") or "")) else ""),
        "has_readme": (tool_dir / "README.md").exists(),
        "spec": spec,
    }
    t["image"] = find_image(tool_dir, meta, rel, collection_dir, warnings)
    t["icon"] = "" if t["image"] else pick_icon(t)
    return t


def find_tools():
    """Walk <author>/<tool>/index.html, descending one more level into
    collections (see module docstring).

    Author comes from the directory, so attribution survives a missing or
    broken meta.json. That is the whole reason for nesting: naming
    discipline is not required for the catalog to be correct.

    Returns (tools, collections, warnings). collections maps author_slug
    to a list of {"folder", "title", "count"} launcher pages.
    """
    tools = []
    collections = {}
    warnings = []

    for author_dir in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
        if not author_dir.is_dir():
            continue
        if author_dir.name.startswith(SKIP_PREFIXES) or author_dir.name in SKIP_NAMES:
            continue

        # Catches the most likely contributor mistake: a tool committed at
        # the top level instead of inside an author folder.
        if (author_dir / "index.html").exists():
            warnings.append(
                f"{author_dir.name}/index.html sits at the author level - "
                f"tools belong in {author_dir.name}/<tool-name>/index.html - skipped"
            )
            continue

        found_any = False

        for tool_dir in sorted(author_dir.iterdir(), key=lambda p: p.name.lower()):
            if not is_tool_dir(tool_dir):
                continue
            rel = f"{author_dir.name}/{tool_dir.name}"

            if is_collection(tool_dir):
                # The launcher page is not a card; its games are.
                launcher_meta = read_meta(tool_dir, rel, warnings)
                members = [
                    p for p in sorted(tool_dir.iterdir(), key=lambda p: p.name.lower())
                    if p.is_dir() and not p.name.startswith(SKIP_PREFIXES)
                    and (p / "index.html").exists()
                ]
                for sub in members:
                    found_any = True
                    sub_rel = f"{rel}/{sub.name}"
                    t = tool_entry(author_dir, sub, sub_rel, warnings, collection_dir=tool_dir)
                    # A game inside a collection inherits the launcher's
                    # display name and accent when its own meta.json has
                    # none, so one author's section reads as one author.
                    if not (sub / "meta.json").exists() or t["author"] == prettify(author_dir.name):
                        t["author"] = str(launcher_meta.get("author") or t["author"])
                    if not t["accent"] and re.fullmatch(r"#[0-9a-fA-F]{6}", str(launcher_meta.get("accent") or "")):
                        t["accent"] = str(launcher_meta["accent"])
                    tools.append(t)
                collections.setdefault(author_dir.name, []).append({
                    "folder": rel,
                    "title": str(launcher_meta.get("title") or prettify(tool_dir.name)),
                    "count": len(members),
                })
                continue

            found_any = True
            tools.append(tool_entry(author_dir, tool_dir, rel, warnings))

        if not found_any:
            warnings.append(f"{author_dir.name}/ contains no tools - skipped")

    return tools, collections, warnings


def group_by_author(tools, collections, counts=None):
    """Order sections: most tools first, then most opened, then name A-Z.

    Display name is the most common "author" string across that person's
    cards, so one stray meta.json with a different spelling does not
    retitle the whole section.
    """
    by_slug = {}
    for t in tools:
        by_slug.setdefault(t["author_slug"], []).append(t)

    sections = []
    for slug, items in by_slug.items():
        names = {}
        for t in items:
            names[t["author"]] = names.get(t["author"], 0) + 1
        display = max(names.items(), key=lambda kv: (kv[1], -len(kv[0])))[0]
        opens = sum((counts or {}).get(t["folder"], 0) for t in items)
        # "pinned": true in meta.json puts a card first within its author's
        # section; order is otherwise unchanged.
        items.sort(key=lambda t: not t["pinned"])
        sections.append({
            "slug": slug,
            "name": display,
            "tools": items,
            "count": len(items),
            "opens": opens,
            "collections": collections.get(slug, []),
        })

    sections.sort(key=lambda s: (-s["count"], -s["opens"], s["name"].lower()))
    return sections


def load_usage():
    """Optional click counts, written by .github/scripts/fetch_usage.py.

    Returns (counts, code). counts is None when no usage file exists, which
    keeps the page exactly as it was before counting was added.
    """
    code = os.environ.get("GOATCOUNTER_CODE", "").strip().lower()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,40}", code):
        code = ""
    counts = None
    path = os.environ.get("USAGE_FILE", "")
    if path and Path(path).is_file():
        try:
            raw = json.loads(Path(path).read_text(encoding="utf-8"))
            counts = {str(k): int(v) for k, v in raw.items()}
        except (ValueError, TypeError, AttributeError) as e:
            print(f"  warning: could not read usage file ({e}) - no counts shown", file=sys.stderr)
    return counts, code


def render_card(t, counts=None):
    e = html.escape
    status_label, status_color = STATUS_LABELS[t["status"]]
    src = f"https://github.com/FCC-Chem/tools/tree/main/{e(t['folder'])}"

    # The picture band: the tool's own image, or a generic line icon.
    if t["image"]:
        art = f'<img src="{e(t["image"])}" alt="" loading="lazy">'
    else:
        art = (f'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
               f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">'
               f'<path d="{ICON_PATHS[t["icon"]]}"/></svg>')
    readme = (
        f'<a class="lnk" href="{e(t["folder"])}/README.md">Notes</a>'
        if t["has_readme"] else ""
    )

    if t["kind"] == "script":
        # No live URL: a script is downloaded and run, not opened. The
        # spec is the primary link because it is what an AI assistant
        # needs in order to adapt the script for someone else.
        spec = (
            f'<a class="lnk primary" href="{e(t["folder"])}/{e(t["spec"])}">Read the spec</a>'
            if t["spec"] else f'<a class="lnk primary" href="{src}">View files</a>'
        )
        title_html = f'<a href="{src}">{e(t["title"])}</a>'
        kind_badge = ('<span class="kind">Script'
                      + (f' · {e(t["requires"])}' if t["requires"] else "")
                      + "</span>")
        links = f'{spec}\n          <a class="lnk" href="{src}">Source</a>\n          {readme}'
    else:
        title_html = f'<a href="{e(t["folder"])}/">{e(t["title"])}</a>'
        kind_badge = ""
        links = (f'<a class="lnk primary" href="{e(t["folder"])}/">Open tool</a>\n'
                 f'          <a class="lnk" href="{src}">Source</a>\n          {readme}')

    search_blob = e(" ".join([
        t["title"], t["author"], t["course"], t["summary"], t["description"],
        " ".join(t["tags"]), t["kind"], t["requires"]
    ]).lower())

    accent_style = f' style="--accent:{t["accent"]}"' if t["accent"] else ""
    opens = (counts or {}).get(t["folder"], 0)
    opens_html = (f'\n        <div class="opens">Opened {opens:,} time{"s" if opens != 1 else ""}</div>'
                  if counts is not None and opens > 0 else "")
    return f"""      <article class="card" data-search="{search_blob}" data-status="{t['status']}" data-author="{e(t['author_slug'])}" data-kind="{t['kind']}" data-folder="{e(t['folder'])}" data-opens="{opens}" data-pinned="{1 if t['pinned'] else 0}"{accent_style}>
        <div class="thumb">{art}
          <span class="status" style="background:{status_color}">{status_label}</span>{kind_badge}
        </div>
        <h3>{title_html}</h3>
        <p class="desc">{e(t['summary'] or t['description'])}</p>{opens_html}
        <div class="links">
          {links}
        </div>
      </article>"""


def render_section(sec, counts=None):
    e = html.escape
    cards = "\n".join(render_card(t, counts) for t in sec["tools"])
    n = sec["count"]
    src = f"https://github.com/FCC-Chem/tools/tree/main/{e(sec['slug'])}"

    launchers = "".join(
        f'\n        <a class="sec-lnk primary" href="{e(c["folder"])}/">'
        f'Open all {c["count"]} in one page →</a>'
        for c in sec["collections"]
    )
    opens = (f' · opened {sec["opens"]:,} time{"s" if sec["opens"] != 1 else ""}'
             if counts is not None and sec["opens"] > 0 else "")

    return f"""    <section class="author-sec" id="a-{e(sec['slug'])}" data-author="{e(sec['slug'])}">
      <div class="sec-head">
        <h2>{e(sec['name'])}</h2>
        <span class="sec-count">{n} tool{"s" if n != 1 else ""}{opens}</span>
        <span class="sec-links">{launchers}
        <a class="sec-lnk" href="{src}">Folder on GitHub</a>
        </span>
      </div>
      <div class="grid">
{cards}
      </div>
      <button class="more" type="button" hidden></button>
    </section>"""


def render(sections, counts=None, gc_code=""):
    built = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    tools = [t for s in sections for t in s["tools"]]

    if sections:
        body = "\n".join(render_section(s, counts) for s in sections)
    else:
        body = ('      <p class="empty">No tools yet. Copy <code>_template/</code> into '
                '<code>yourname/toolname/</code> to get started.</p>')

    # Author dropdown doubles as a jump list: picking one hides the other
    # sections. Order matches the page (largest contributor first).
    opts = "".join(
        f'<option value="{html.escape(s["slug"])}">{html.escape(s["name"])} ({s["count"]})</option>'
        for s in sections
    )
    author_sel = (
        f'<select id="who" aria-label="Filter by author">'
        f'<option value="all">All authors</option>{opts}</select>'
        if len(sections) > 1 else ""
    )

    # Only worth showing once both kinds actually exist.
    kinds = {t["kind"] for t in tools}
    kind_sel = (
        '    <div class="filters">\n'
        '      <button class="kbtn on" data-k="all">Any type</button>\n'
        '      <button class="kbtn" data-k="web">Web tools</button>\n'
        '      <button class="kbtn" data-k="script">Scripts</button>\n'
        '    </div>'
        if len(kinds) > 1 else ""
    )

    sort_sel = (
        '    <select id="sort" aria-label="Sort tools within each author">'
        '<option value="opens" selected>Sort: most opened</option>'
        '<option value="az">Sort: A to Z</option></select>'
        if counts else ""
    )
    gc_url = f"https://{gc_code}.goatcounter.com/count" if gc_code else ""
    gc_note = (' · Clicks on each tool\'s main button are counted (no cookies, nothing about you) '
               'so the most-used tools can rise to the top.' if gc_code else "")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>FCC Chemistry — AI Tool Catalog</title>
<style>
  :root {{
    --bg:#fff; --fg:#1a1a1a; --muted:#666; --accent:#1f6f43;
    --border:#e2e2e0; --panel:#f7f7f5;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
         background:var(--bg); color:var(--fg); line-height:1.5; }}
  .wrap {{ max-width:1000px; margin:0 auto; padding:36px 20px 72px; }}
  header {{ border-bottom:2px solid var(--accent); padding-bottom:16px; margin-bottom:12px;
            display:flex; align-items:center; gap:16px; }}
  .mark {{ width:104px; height:104px; flex:0 0 104px; }}
  .mark canvas {{ display:block; width:100%; height:100%; cursor:grab; }}
  .mark canvas:active {{ cursor:grabbing; }}
  .head-text {{ min-width:0; }}
  h1 {{ margin:0 0 6px; font-size:1.9rem; }}
  .tagline {{ color:var(--muted); }}
  @media (max-width:620px) {{
    header {{ gap:12px; }}
    .mark {{ width:72px; height:72px; flex:0 0 72px; }}
    h1 {{ font-size:1.4rem; }}
    .tagline {{ font-size:0.85rem; }}
  }}
  .controls {{ display:flex; gap:10px; flex-wrap:wrap; margin:22px 0 26px; }}
  #q {{ flex:1; min-width:220px; padding:11px 14px; font-size:1rem;
        border:1px solid var(--border); border-radius:8px; font-family:inherit; }}
  #who, #sort {{ padding:11px 14px; font-size:0.95rem; border:1px solid var(--border);
          border-radius:8px; font-family:inherit; background:#fff; cursor:pointer; }}
  .filters {{ display:flex; gap:6px; }}
  .fbtn, .kbtn {{ padding:10px 16px; border:1px solid var(--border); background:#fff;
           border-radius:8px; cursor:pointer; font-size:0.9rem; font-family:inherit; }}
  .fbtn.on, .kbtn.on {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
  .author-sec {{ margin:0 0 40px; }}
  .sec-head {{ display:flex; align-items:baseline; gap:14px; flex-wrap:wrap;
               border-bottom:1px solid var(--border); padding-bottom:8px; margin-bottom:16px; }}
  .sec-head h2 {{ margin:0; font-size:1.35rem; }}
  .sec-count {{ color:var(--muted); font-size:0.9rem; }}
  .sec-links {{ margin-left:auto; display:flex; gap:8px; flex-wrap:wrap; }}
  .sec-lnk {{ font-size:0.82rem; text-decoration:none; color:var(--accent);
              border:1px solid var(--accent); padding:5px 11px; border-radius:6px; }}
  .sec-lnk.primary {{ background:var(--accent); color:#fff; }}
  .sec-lnk:hover {{ filter:brightness(1.12); }}
  @media (max-width:620px) {{ .sec-links {{ margin-left:0; }} }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:18px; }}
  .more {{ display:block; width:100%; margin-top:14px; padding:10px 16px; font-family:inherit;
           font-size:0.9rem; color:var(--accent); background:var(--panel);
           border:1px dashed var(--accent); border-radius:8px; cursor:pointer; }}
  .more:hover {{ background:#eef5f0; }}
  .more[hidden] {{ display:none; }}
  .card {{ border:1px solid var(--border); border-radius:10px; padding:0 18px 18px;
           background:var(--panel); display:flex; flex-direction:column; overflow:hidden; }}
  /* Picture band: a tinted field with the tool's image or a line icon
     centered in it. Images are shown whole (contained), never cropped,
     because most are small square logos. */
  .thumb {{ position:relative; height:132px; margin:0 -18px 14px;
            display:flex; align-items:center; justify-content:center;
            color:var(--accent); background:#e8ece9;
            background:color-mix(in srgb, var(--accent) 12%, #fff);
            border-bottom:1px solid var(--border); }}
  .thumb img {{ max-height:100px; max-width:60%; object-fit:contain; border-radius:12px; }}
  .thumb svg {{ width:64px; height:64px; opacity:0.9; }}
  .thumb .status {{ position:absolute; top:10px; right:10px; }}
  .thumb .kind {{ position:absolute; bottom:10px; left:10px; }}
  .card h3 {{ margin:0 0 8px; font-size:1.1rem; }}
  .card h3 a {{ color:var(--fg); text-decoration:none; }}
  .card h3 a:hover {{ color:var(--accent); text-decoration:underline; }}
  .status {{ color:#fff; font-size:0.68rem; font-weight:700; padding:3px 8px;
             border-radius:20px; white-space:nowrap; text-transform:uppercase;
             letter-spacing:0.03em; }}
  /* Long descriptions are clamped on the card; the full text is still
     searched and still shown on the tool's own page. */
  .desc {{ margin:0 0 12px; font-size:0.92rem; color:#333;
           display:-webkit-box; -webkit-line-clamp:3; -webkit-box-orient:vertical;
           overflow:hidden; }}
  .meta {{ font-size:0.83rem; color:var(--muted); margin-bottom:10px; }}
  .author {{ font-weight:600; color:#444; }}
  .opens {{ font-size:0.8rem; color:var(--muted); margin:-4px 0 10px; }}
  .course:before {{ content:" · "; }}
  .tags {{ display:flex; flex-wrap:wrap; gap:5px; margin-bottom:14px; }}
  .tag {{ font-size:0.72rem; background:#e8ece9; color:#31513f;
          padding:3px 8px; border-radius:4px; }}
  .kind {{ font-size:0.72rem; background:#3a3f44; color:#fff; font-weight:600;
           padding:3px 8px; border-radius:4px; }}
  .links {{ display:flex; gap:8px; flex-wrap:wrap; margin-top:auto; }}
  .lnk {{ font-size:0.85rem; text-decoration:none; color:var(--accent);
          border:1px solid var(--accent); padding:6px 12px; border-radius:6px; }}
  .lnk.primary {{ background:var(--accent); color:#fff; }}
  .lnk:hover {{ filter:brightness(1.12); }}
  .start-here {{ display:flex; align-items:center; gap:16px; flex-wrap:wrap;
    background:#eef5f0; border:2px solid var(--accent); border-radius:12px;
    padding:16px 20px; margin:20px 0 6px; }}
  .start-badge {{ background:var(--accent); color:#fff; font-size:0.72rem; font-weight:700;
    letter-spacing:0.08em; text-transform:uppercase; padding:5px 11px; border-radius:20px;
    white-space:nowrap; }}
  .start-text {{ flex:1; min-width:220px; }}
  .start-text strong {{ display:block; font-size:1.05rem; margin-bottom:2px; }}
  .start-text span {{ font-size:0.88rem; color:var(--muted); }}
  .start-cta {{ background:var(--accent); color:#fff; text-decoration:none; font-weight:600;
    padding:10px 18px; border-radius:8px; font-size:0.92rem; white-space:nowrap; }}
  .start-cta:hover {{ filter:brightness(1.12); }}
  .empty {{ color:var(--muted); font-style:italic; }}
  .none {{ color:var(--muted); padding:20px 0; display:none; }}
  footer {{ margin-top:52px; padding-top:16px; border-top:1px solid var(--border);
            font-size:0.82rem; color:var(--muted); }}
  footer a {{ color:var(--accent); }}
</style>
</head>
<body>
<div class="wrap">

  <header>
{HERO}
    <div class="head-text">
      <h1>FCC Chemistry — AI Tool Catalog</h1>
      <div class="tagline">Teaching tools built by our department, with AI. Click any tool to use it.</div>
    </div>
  </header>

  <div class="start-here">
    <span class="start-badge">Start here</span>
    <div class="start-text">
      <strong>New? Build and host your first tool in 90 minutes.</strong>
      <span>The step-by-step walkthrough from the workshop — browser only, no coding, works on your phone.</span>
    </div>
    <a class="start-cta" href="workshop/walkthrough.html">Open the walkthrough →</a>
  </div>

  <div class="controls">
    <input id="q" type="search" placeholder="Search tools, authors, courses…" autocomplete="off">
    {author_sel}
    <div class="filters">
      <button class="fbtn on" data-f="all">All</button>
      <button class="fbtn" data-f="working">Working / Stable</button>
      <button class="fbtn" data-f="wip">In progress</button>
    </div>
{kind_sel}
{sort_sel}
  </div>

  <div id="catalog">
{body}
  </div>
  <p class="none" id="none">Nothing matches that search.</p>

  <footer>
    <strong>{len(tools)} tool{"s" if len(tools) != 1 else ""}</strong> from {len(sections)} author{"s" if len(sections) != 1 else ""} · rebuilt automatically {built}{gc_note}<br>
    <a href="https://github.com/FCC-Chem/tools">Source on GitHub</a> ·
    <a href="https://github.com/FCC-Chem/tools/discussions">Discussions</a> ·
    <a href="https://github.com/FCC-Chem/tools/issues/new">Request a tool</a><br>
    Unofficial faculty project. Not an official channel of Fresno City College or SCCCD.
  </footer>

</div>

<script>
(function () {{
  var q = document.getElementById('q');
  var who = document.getElementById('who');       // absent when only one author
  var none = document.getElementById('none');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var filter = 'all';
  var kind = 'all';

  var SHOW = {SHOW_FIRST};   // cards shown per author until "Show N more" is clicked
  function apply() {{
    var term = q.value.trim().toLowerCase();
    var author = who ? who.value : 'all';
    // Any search or filter unfolds every section: a match must never sit
    // behind a "Show more" button.
    var filtering = !!term || filter !== 'all' || kind !== 'all' || author !== 'all';
    var shown = 0;
    sections.forEach(function (s) {{
      var open = filtering || s.classList.contains('open');
      var vis = 0, folded = 0;
      // DOM order, so this respects the current sort.
      Array.prototype.forEach.call(s.querySelectorAll('.card'), function (c) {{
        var okText = !term || c.dataset.search.indexOf(term) !== -1;
        var okStat = filter === 'all' || c.dataset.status === filter ||
          (filter === 'working' && c.dataset.status === 'stable');
        var okWho  = author === 'all' || c.dataset.author === author;
        var okKind = kind === 'all' || c.dataset.kind === kind;
        var match = okText && okStat && okWho && okKind;
        if (match) vis++;
        var fold = match && !open && vis > SHOW;
        if (fold) folded++;
        c.style.display = (match && !fold) ? '' : 'none';
      }});
      shown += vis;
      // An author whose every card is filtered out disappears with them.
      s.style.display = vis ? '' : 'none';
      var btn = s.querySelector('.more');
      if (folded) {{
        btn.textContent = 'Show ' + folded + ' more \u25BE';
        btn.hidden = false;
      }} else if (!filtering && open && vis > SHOW) {{
        btn.textContent = 'Show fewer \u25B4';
        btn.hidden = false;
      }} else {{
        btn.hidden = true;
      }}
    }});
    none.style.display = (shown === 0 && cards.length) ? 'block' : 'none';
  }}

  var catalog = document.getElementById('catalog');
  var sections = Array.prototype.slice.call(document.querySelectorAll('.author-sec'));
  var sortSel = document.getElementById('sort');   // present only when counts exist
  // Reorders cards inside each author's section. Section order itself is
  // fixed at build time (largest contributor first).
  function resort() {{
    var byOpens = sortSel && sortSel.value === 'opens';
    sections.forEach(function (s) {{
      var grid = s.querySelector('.grid');
      var mine = Array.prototype.slice.call(grid.querySelectorAll('.card'));
      mine.slice().sort(function (a, b) {{
        var p = (+b.dataset.pinned || 0) - (+a.dataset.pinned || 0);
        if (p) return p;
        if (byOpens) {{
          var d = (+b.dataset.opens || 0) - (+a.dataset.opens || 0);
          if (d) return d;
        }}
        return cards.indexOf(a) - cards.indexOf(b);
      }}).forEach(function (c) {{ grid.appendChild(c); }});
    }});
  }}
  if (sortSel) {{ sortSel.addEventListener('change', function () {{ resort(); apply(); }}); resort(); }}

  // Count clicks on each card's main button. Sends only the tool's folder
  // name; no cookies and nothing about the person.
  var GC = {json.dumps(gc_url)};
  if (GC) {{
    catalog.addEventListener('click', function (ev) {{
      var a = ev.target.closest('.lnk.primary');
      var card = a && a.closest('.card');
      if (!card) return;
      var u = GC + '?e=true&p=' + encodeURIComponent('open/' + card.dataset.folder) +
              '&t=' + encodeURIComponent(card.querySelector('h3').textContent.trim()) +
              '&rnd=' + Math.random().toString(36).slice(2);
      try {{ fetch(u, {{ mode: 'no-cors', keepalive: true }}); }} catch (e) {{}}
    }});
  }}

  q.addEventListener('input', apply);
  if (who) who.addEventListener('change', apply);
  sections.forEach(function (s) {{
    s.querySelector('.more').addEventListener('click', function () {{
      s.classList.toggle('open');
      apply();
    }});
  }});
  apply();   // fold each section to SHOW cards on load
  document.querySelectorAll('.fbtn').forEach(function (b) {{
    b.addEventListener('click', function () {{
      document.querySelectorAll('.fbtn').forEach(function (x) {{ x.classList.remove('on'); }});
      b.classList.add('on');
      filter = b.dataset.f;
      apply();
    }});
  }});
  document.querySelectorAll('.kbtn').forEach(function (b) {{
    b.addEventListener('click', function () {{
      document.querySelectorAll('.kbtn').forEach(function (x) {{ x.classList.remove('on'); }});
      b.classList.add('on');
      kind = b.dataset.k;
      apply();
    }});
  }});
}})();
</script>
{HERO_SCRIPT}
</body>
</html>
"""


def main():
    tools, collections, warnings = find_tools()

    for w in warnings:
        print(f"  warning: {w}", file=sys.stderr)

    counts, gc_code = load_usage()
    sections = group_by_author(tools, collections, counts)
    (ROOT / "index.html").write_text(render(sections, counts, gc_code), encoding="utf-8")
    print(f"Catalog rebuilt: {len(tools)} tool(s) from {len(sections)} author(s)")
    for s in sections:
        print(f"  {s['name']} ({s['slug']}): {s['count']} tool(s)")
        for t in s["tools"]:
            print(f"    - {t['folder']}  ({t['status']})")


if __name__ == "__main__":
    main()
