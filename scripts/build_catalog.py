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
import html
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
SKIP_PREFIXES = (".", "_")
SKIP_NAMES = {"scripts", "workshop", "node_modules"}

STATUS_LABELS = {
    "working": ("Working", "#1f6f43"),
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


def find_tools():
    """Walk <author>/<tool>/index.html.

    Author comes from the directory, so attribution survives a missing or
    broken meta.json. That is the whole reason for nesting: naming
    discipline is not required for the catalog to be correct.
    """
    tools = []
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
            if not tool_dir.is_dir():
                continue
            if tool_dir.name.startswith(SKIP_PREFIXES):
                continue
            # A browser tool announces itself with index.html; a script
            # tool has no index.html, so meta.json is what marks the
            # folder as a deliberate contribution rather than clutter.
            if not (tool_dir / "index.html").exists() and not (tool_dir / "meta.json").exists():
                continue

            found_any = True
            rel = f"{author_dir.name}/{tool_dir.name}"
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

            tools.append({
                "folder": rel,
                "author_slug": author_dir.name,
                "kind": kind,
                "entry": entry_file,
                "requires": str(meta.get("requires") or ("Python 3" if kind == "script" else "")),
                "title": str(meta.get("title") or prettify(tool_dir.name)),
                # Folder name is the fallback author. meta.json only overrides
                # it to provide a nicer display name.
                "author": str(meta.get("author") or prettify(author_dir.name)),
                "course": str(meta.get("course") or ""),
                "description": str(meta.get("description") or "No description yet."),
                "tags": [str(t) for t in tags],
                "status": status,
                "has_readme": (tool_dir / "README.md").exists(),
                "spec": spec,
            })

        if not found_any:
            warnings.append(f"{author_dir.name}/ contains no tools - skipped")

    return tools, warnings


def render_card(t):
    e = html.escape
    status_label, status_color = STATUS_LABELS[t["status"]]
    src = f"https://github.com/FCC-Chem/tools/tree/main/{e(t['folder'])}"

    course = f'<span class="course">{e(t["course"])}</span>' if t["course"] else ""
    tags = "".join(f'<span class="tag">{e(tag)}</span>' for tag in t["tags"])
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
        t["title"], t["author"], t["course"], t["description"],
        " ".join(t["tags"]), t["kind"], t["requires"]
    ]).lower())

    return f"""      <article class="card" data-search="{search_blob}" data-status="{t['status']}" data-author="{e(t['author_slug'])}" data-kind="{t['kind']}">
        <div class="card-head">
          <h3>{title_html}</h3>
          <span class="status" style="background:{status_color}">{status_label}</span>
        </div>
        <p class="desc">{e(t['description'])}</p>
        <div class="meta">
          <span class="author">{e(t['author'])}</span>
          {course}
        </div>
        <div class="tags">{kind_badge}{tags}</div>
        <div class="links">
          {links}
        </div>
      </article>"""


def render(tools):
    built = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if tools:
        cards = "\n".join(render_card(t) for t in tools)
        empty = ""
    else:
        cards = ""
        empty = ('      <p class="empty">No tools yet. Copy <code>_template/</code> into '
                 '<code>yourname/toolname/</code> to get started.</p>')

    # Author dropdown, built from whoever actually has tools.
    seen = {}
    for t in tools:
        seen.setdefault(t["author_slug"], t["author"])
    opts = "".join(
        f'<option value="{html.escape(slug)}">{html.escape(name)}</option>'
        for slug, name in sorted(seen.items(), key=lambda kv: kv[1].lower())
    )
    author_sel = (
        f'<select id="who" aria-label="Filter by author">'
        f'<option value="all">All authors</option>{opts}</select>'
        if len(seen) > 1 else ""
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
  #who {{ padding:11px 14px; font-size:0.95rem; border:1px solid var(--border);
          border-radius:8px; font-family:inherit; background:#fff; cursor:pointer; }}
  .filters {{ display:flex; gap:6px; }}
  .fbtn, .kbtn {{ padding:10px 16px; border:1px solid var(--border); background:#fff;
           border-radius:8px; cursor:pointer; font-size:0.9rem; font-family:inherit; }}
  .fbtn.on, .kbtn.on {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:18px; }}
  .card {{ border:1px solid var(--border); border-radius:10px; padding:18px;
           background:var(--panel); display:flex; flex-direction:column; }}
  .card-head {{ display:flex; justify-content:space-between; align-items:flex-start; gap:10px; }}
  .card h3 {{ margin:0 0 8px; font-size:1.1rem; }}
  .card h3 a {{ color:var(--fg); text-decoration:none; }}
  .card h3 a:hover {{ color:var(--accent); text-decoration:underline; }}
  .status {{ color:#fff; font-size:0.68rem; font-weight:700; padding:3px 8px;
             border-radius:20px; white-space:nowrap; text-transform:uppercase;
             letter-spacing:0.03em; }}
  .desc {{ margin:0 0 12px; font-size:0.92rem; color:#333; flex:1; }}
  .meta {{ font-size:0.83rem; color:var(--muted); margin-bottom:10px; }}
  .author {{ font-weight:600; color:#444; }}
  .course:before {{ content:" · "; }}
  .tags {{ display:flex; flex-wrap:wrap; gap:5px; margin-bottom:14px; }}
  .tag {{ font-size:0.72rem; background:#e8ece9; color:#31513f;
          padding:3px 8px; border-radius:4px; }}
  .kind {{ font-size:0.72rem; background:#3a3f44; color:#fff; font-weight:600;
           padding:3px 8px; border-radius:4px; }}
  .links {{ display:flex; gap:8px; flex-wrap:wrap; }}
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
      <button class="fbtn" data-f="working">Working</button>
      <button class="fbtn" data-f="wip">In progress</button>
    </div>
{kind_sel}
  </div>

  <div class="grid" id="grid">
{cards}
{empty}
  </div>
  <p class="none" id="none">Nothing matches that search.</p>

  <footer>
    <strong>{len(tools)} tool{"s" if len(tools) != 1 else ""}</strong> · rebuilt automatically {built}<br>
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

  function apply() {{
    var term = q.value.trim().toLowerCase();
    var author = who ? who.value : 'all';
    var shown = 0;
    cards.forEach(function (c) {{
      var okText = !term || c.dataset.search.indexOf(term) !== -1;
      var okStat = filter === 'all' || c.dataset.status === filter;
      var okWho  = author === 'all' || c.dataset.author === author;
      var okKind = kind === 'all' || c.dataset.kind === kind;
      var vis = okText && okStat && okWho && okKind;
      c.style.display = vis ? '' : 'none';
      if (vis) shown++;
    }});
    none.style.display = (shown === 0 && cards.length) ? 'block' : 'none';
  }}

  q.addEventListener('input', apply);
  if (who) who.addEventListener('change', apply);
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
    tools, warnings = find_tools()

    for w in warnings:
        print(f"  warning: {w}", file=sys.stderr)

    (ROOT / "index.html").write_text(render(tools), encoding="utf-8")
    print(f"Catalog rebuilt: {len(tools)} tool(s)")
    for t in tools:
        print(f"  - {t['folder']}  ({t['author']}, {t['status']})")


if __name__ == "__main__":
    main()
