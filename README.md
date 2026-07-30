# FCC Chemistry — AI Tool Catalog

Teaching tools built by Fresno City College chemistry faculty, with AI assistance.

**Live catalog:** https://fcc-chem.github.io/tools/

> Unofficial faculty project. Not an official channel of Fresno City College or the State Center Community College District.

---

## What this is

A shared space where we build small, useful teaching tools and hand them to each other.

Every tool is a **single HTML file** that runs in a browser. No installation, no build step, no operating-system problems. You open a link and it works — on your Mac, Dan's PC, a student's phone.

The point isn't the tools. The point is that any of us can take someone else's tool, hand it to an AI assistant, and have it reshaped for our own course in about ten minutes.

---

## Using a tool

Go to the [catalog](https://fcc-chem.github.io/tools/) and click it. That's it. Share the link with students.

---

## Adding your own tool

Every instructor gets a folder. Everything you build lives inside it:

```
yourname/toolname/index.html
yourname/toolname/meta.json     (optional)
```

**Your folder name is your author name.** That means attribution is
structural — if you forget `meta.json` entirely, your tool still shows up
on the catalog, still credited to you. Nothing to remember.

### In the browser — no software required

1. Go to the [`_template`](_template) folder
2. Click **index.html** → the pencil icon → select all → copy
3. Back at the repo root, click **Add file → Create new file**
4. Type `yourname/toolname/index.html` — each slash creates a folder
5. Paste, then **Commit changes**
6. Optionally repeat for `meta.json` (copy from `_template/meta.json`)

Within about a minute your tool appears on the catalog page automatically. You do not edit any list.

### Adapting someone else's tool

1. Open their `index.html` on GitHub, click **Raw**, copy everything
2. Paste it into Claude, Copilot, or ChatGPT
3. Tell it what to change: *"Rewrite this for a CHEM 3A buffer calculation. Same layout, same styling."*
4. Paste the result into `yourname/newtoolname/index.html`
5. Update `meta.json`

Do not edit someone else's folder. Copy it into your own — that's what
the folders are for.

---

## `meta.json`

Entirely optional. It just makes your catalog card better.

```json
{
  "title": "Molar Mass Calculator",
  "author": "R. Gilley",
  "course": "CHEM 1A",
  "description": "One sentence. Shows on the catalog card.",
  "tags": ["stoichiometry", "calculator"],
  "status": "working"
}
```

- `author` overrides your folder name — use it for a nicer display name
- `title` overrides the tool folder name
- `status` is `working` or `wip`. Be honest — `wip` is not a failure, it's an invitation.

If `meta.json` is missing or malformed, your tool still appears with values
derived from the folder names. The build never fails because of one bad file.

---

## Rules

**Hard rules — these are not style preferences:**

1. **No student data. Ever.** No names, no student IDs, no grades, no submissions, no rosters. This repository is public. Use synthetic sample data.
2. **No credentials.** No API keys, passwords, SMTP settings, or Canvas tokens. If you commit one, it is scraped within minutes — assume it is compromised and rotate it immediately.
3. **No answer keys or live exam content.** Public repositories are permanently mirrored. Deleting does not undo it.
4. **Nothing copied from a publisher.** Textbook figures and problem sets stay out.

**Soft rules — makes life easier for everyone:**

- Your own folder, one subfolder per tool: `yourname/toolname/`
- Lowercase, hyphens instead of spaces
- Single HTML file. No npm, no build step, no framework.
- If you need a library, load it from a CDN — don't commit it
- Say what your tool assumes in a `README.md` inside the tool folder

---

## Where things live

```
tools/
├── index.html              ← auto-generated catalog, DO NOT EDIT
├── _template/              ← copy this to start
├── gilley/                 ← one folder per instructor
│   ├── molar-mass/         ← example: simple
│   │   ├── index.html
│   │   └── meta.json
│   └── titration-sim/      ← example: more involved
├── cherry/                 ← yours goes here
├── scripts/
│   └── build_catalog.py    ← regenerates index.html
├── workshop/               ← training materials
└── .github/workflows/      ← the Action that runs the build
```

`index.html` at the root is machine-generated on every push. Edits to it are overwritten.

---

## Talk to each other

- **[Discussions](https://github.com/FCC-Chem/tools/discussions)** — ideas, questions, show and tell
- **[Issues](https://github.com/FCC-Chem/tools/issues)** — "can someone build a tool that does X"

---

## Running the catalog build locally

Optional. You never need this to contribute.

```bash
python3 scripts/build_catalog.py
```
