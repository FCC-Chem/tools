#!/usr/bin/env python3
"""
Scans every tool folder for meta.json and regenerates the root index.html catalog.

A "tool folder" is any top-level directory that:
  - does not start with . or _
  - contains an index.html

meta.json is optional. If missing or malformed, the tool still appears in the
catalog with fallback values, and a warning is printed. The build never fails
on one person's bad JSON -- that would block everyone else's push.

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


def find_tools():
    tools = []
    warnings = []

    for entry in sorted(ROOT.iterdir(), key=lambda p: p.name.lower()):
        if not entry.is_dir():
            continue
        if entry.name.startswith(SKIP_PREFIXES) or entry.name in SKIP_NAMES:
            continue
        if not (entry / "index.html").exists():
            warnings.append(f"{entry.name}/ has no index.html - skipped")
            continue

        meta = {}
        meta_path = entry / "meta.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                if not isinstance(meta, dict):
                    raise ValueError("meta.json must be a JSON object")
            except Exception as e:
                warnings.append(f"{entry.name}/meta.json could not be read ({e}) - using defaults")
                meta = {}
        else:
            warnings.append(f"{entry.name}/ has no meta.json - using defaults")

        tags = meta.get("tags", [])
        if not isinstance(tags, list):
            tags = []

        status = str(meta.get("status", "wip")).lower()
        if status not in STATUS_LABELS:
            status = "wip"

        tools.append({
            "folder": entry.name,
            "title": str(meta.get("title") or entry.name),
            "author": str(meta.get("author") or "Unknown"),
            "course": str(meta.get("course") or ""),
            "description": str(meta.get("description") or "No description yet."),
            "tags": [str(t) for t in tags],
            "status": status,
            "has_readme": (entry / "README.md").exists(),
        })

    return tools, warnings


def render_card(t):
    e = html.escape
    status_label, status_color = STATUS_LABELS[t["status"]]

    course = f'<span class="course">{e(t["course"])}</span>' if t["course"] else ""
    tags = "".join(f'<span class="tag">{e(tag)}</span>' for tag in t["tags"])
    readme = (
        f'<a class="lnk" href="{e(t["folder"])}/README.md">Notes</a>'
        if t["has_readme"] else ""
    )

    search_blob = e(" ".join([
        t["title"], t["author"], t["course"], t["description"], " ".join(t["tags"])
    ]).lower())

    return f"""      <article class="card" data-search="{search_blob}" data-status="{t['status']}">
        <div class="card-head">
          <h3><a href="{e(t['folder'])}/">{e(t['title'])}</a></h3>
          <span class="status" style="background:{status_color}">{status_label}</span>
        </div>
        <p class="desc">{e(t['description'])}</p>
        <div class="meta">
          <span class="author">{e(t['author'])}</span>
          {course}
        </div>
        <div class="tags">{tags}</div>
        <div class="links">
          <a class="lnk primary" href="{e(t['folder'])}/">Open tool</a>
          <a class="lnk" href="https://github.com/FCC-Chem/tools/tree/main/{e(t['folder'])}">Source</a>
          {readme}
        </div>
      </article>"""


def render(tools):
    built = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    if tools:
        cards = "\n".join(render_card(t) for t in tools)
        empty = ""
    else:
        cards = ""
        empty = '      <p class="empty">No tools yet. Copy <code>_template/</code> to get started.</p>'

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
  .filters {{ display:flex; gap:6px; }}
  .fbtn {{ padding:10px 16px; border:1px solid var(--border); background:#fff;
           border-radius:8px; cursor:pointer; font-size:0.9rem; font-family:inherit; }}
  .fbtn.on {{ background:var(--accent); color:#fff; border-color:var(--accent); }}
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
  .links {{ display:flex; gap:8px; flex-wrap:wrap; }}
  .lnk {{ font-size:0.85rem; text-decoration:none; color:var(--accent);
          border:1px solid var(--accent); padding:6px 12px; border-radius:6px; }}
  .lnk.primary {{ background:var(--accent); color:#fff; }}
  .lnk:hover {{ filter:brightness(1.12); }}
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

  <div class="controls">
    <input id="q" type="search" placeholder="Search tools, authors, courses…" autocomplete="off">
    <div class="filters">
      <button class="fbtn on" data-f="all">All</button>
      <button class="fbtn" data-f="working">Working</button>
      <button class="fbtn" data-f="wip">In progress</button>
    </div>
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
  var none = document.getElementById('none');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var filter = 'all';

  function apply() {{
    var term = q.value.trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (c) {{
      var okText = !term || c.dataset.search.indexOf(term) !== -1;
      var okStat = filter === 'all' || c.dataset.status === filter;
      var vis = okText && okStat;
      c.style.display = vis ? '' : 'none';
      if (vis) shown++;
    }});
    none.style.display = (shown === 0 && cards.length) ? 'block' : 'none';
  }}

  q.addEventListener('input', apply);
  document.querySelectorAll('.fbtn').forEach(function (b) {{
    b.addEventListener('click', function () {{
      document.querySelectorAll('.fbtn').forEach(function (x) {{ x.classList.remove('on'); }});
      b.classList.add('on');
      filter = b.dataset.f;
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
