# Instructions for AI assistants working in this repository

Read this before generating or modifying anything here. Claude Code, Copilot,
Cursor, and similar tools pick this file up automatically.

## What this repository is

A catalog of small, self-contained teaching tools for community college
chemistry instructors. The audience is faculty with mixed technical skill.
Portability and simplicity beat sophistication every time.

## Repository layout

Tools are namespaced by author:

```
<author>/<tool>/index.html      required
<author>/<tool>/meta.json       optional
<author>/<tool>/README.md       optional
```

The author folder is the source of truth for attribution. Never place a
tool at the top level, and never write into another author's folder --
copy into the current author's folder instead.

## Two kinds of tool

**Web tools** (`index.html`) run in the browser and are the default.
**Script tools** (`meta.json` with `"kind": "script"`) run locally and are
for things a browser cannot do: reading a gradebook file, sending mail,
calling the Canvas API.

Rules below marked WEB or SCRIPT apply only to that kind.

## Hard constraints

### WEB

- **One tool = one folder = one `index.html` file.** Do not split into
  separate `.css` or `.js` files. Do not add a build step.
- **No npm, no bundler, no framework, no package.json.** The file must work
  when opened directly from disk with a double-click.
- **No external requests at runtime** unless the tool's purpose requires it.
  Prefer zero dependencies. If a library is unavoidable, load it from
  `cdnjs.cloudflare.com` via a `<script>` tag.
- **No `localStorage` or `sessionStorage`** — keep state in JavaScript
  variables. These pages are sometimes embedded where storage is blocked.
- **Never write code that collects, transmits, or stores student data.**
  If asked to build something that handles a real gradebook, the file
  reading must happen client-side only, via `<input type="file">`, with
  nothing leaving the page. Say so explicitly in the UI.
- **Never commit credentials.** If a web tool needs an API key, it prompts
  the user for it at runtime and holds it in memory only.

### SCRIPT

- **Standard library only** unless the user explicitly asks otherwise. A
  script that needs `pip install` before it runs will not be adopted by
  the intended audience.
- **Dry run is the default.** Any action that sends mail, writes to a
  gradebook, posts to an API, or deletes anything requires an explicit
  `--send` / `--apply` / `--yes` flag. Without it, print what *would*
  happen and exit.
- **Credentials come from a `.env` file** read at runtime, never from
  literals in the source. Ship a `.env.example`. Exit with a readable
  message listing which variables are missing.
- **Ship synthetic sample data** with the real column structure. This is
  what lets the next instructor test without touching a real roster, and
  what lets an AI assistant see the schema.
- **Ship a `SPEC.md`** describing inputs, outputs, configuration, and what
  to change. For script tools this matters more than the code.
- **Ungraded work is not zero.** When computing averages, a category with
  nothing graded yet must be dropped and the remaining weights
  renormalized. Counting it as zero tells a student in week 3 that they
  are failing when they are not. This is the most common bug in grading
  scripts.
- **Validate before acting.** Check that weights sum to 1.0, that required
  columns exist, and that the roster is non-empty. Fail with a readable
  message naming the problem and the file.
- **Never write code that transmits student data anywhere** except to the
  student's own address via the user's configured mail server.

## House style

- Match the CSS variable block used in `_template/index.html`:
  `--bg --fg --muted --accent --border --panel`. Accent is `#1f6f43`.
- Semantic HTML, real `<label>` elements tied to inputs.
- Every tool ends with a footer linking back to `../` (the catalog).
- Plain vanilla JavaScript. No TypeScript, no JSX, no transpiling.
- Comments explain the chemistry or the pedagogy, not the syntax. The
  reader is a chemist, not a programmer.

## Correctness matters more than polish

This is chemistry instruction. A tool that looks good and computes wrong
is worse than no tool.

- Prefer exact numerical methods over the piecewise approximations found
  in textbooks. See `gilley-titration-sim/index.html` — it solves the
  charge-balance equation by bisection rather than switching between
  Henderson–Hasselbalch regimes, so it stays correct near the equivalence
  point and at low concentration.
- Use IUPAC standard atomic weights. Cite the source in a comment.
- Show units in the output. Always.
- Validate input and fail with a readable message, never a silent NaN.
- State the model's assumptions in the UI (temperature, ideality, activity
  coefficients) where they affect the answer.

## When adapting an existing tool

- Copy it to `<current-author>/<new-tool-name>/`. Never modify another
  person's folder.
- Folder names: all lowercase, hyphens instead of spaces.
- The catalog backlink in the footer must be `../../` -- tools sit two
  levels below the repository root.
- Update `meta.json`: `title`, `author`, `course`, `description`, `tags`,
  and `status` (`working` or `wip`). All optional; the builder falls back
  to the folder names.
- Keep the structural layout and styling. Consistency across the catalog
  is a feature — faculty recognize the shape of these pages.

## Do not touch

- `/index.html` at the repository root — build output, generated by
  `scripts/build_catalog.py` and gitignored. Never edit it, never commit
  it, never add it to a commit with `git add -f`.
- `.github/workflows/build-catalog.yml` unless explicitly asked.

## Definition of done

**WEB**

- Opens and works when double-clicked from the local filesystem
- No console errors
- Handles empty and nonsense input without crashing
- Footer links back to `../../`

**SCRIPT**

- Runs with no arguments against the shipped sample data and sends nothing
- Exits with a readable message when credentials or columns are missing
- `--help` explains every flag
- No secrets, real names, real emails, or absolute paths anywhere in the file

**BOTH**

- `meta.json` is valid JSON
- A colleague could read the code and understand what it computes
