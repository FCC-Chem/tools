# Accessibility Gap Report — GitHub Quiz App & Syllabus Sites
**Audited:** Aug 16, 2026 · prof-gilley.github.io (CHEM1A quiz engine + CHEM1A/CHEM3A syllabi)
**Standard:** WCAG 2.1 AA
**Method:** Full source review of `quiz/index.html` (engine + all rendering paths), both `syllabus/index.html` files; every color pair computed for contrast; live site diffed against local source (quiz: identical; syllabi: identical except ~12 trivial lines).

---

## 0. Broken link — fix first (not a11y, but blocking)

Both Canvas syllabi link to `prof-gilley.github.io/chem1a/syllabus/` and `/chem3a/syllabus/` — **lowercase paths 404** (GitHub Pages is case-sensitive). Working URLs are `/CHEM1A/syllabus/` and `/CHEM3A/syllabus/`. Every student following the Canvas syllabus link hits "Site not found."

---

## 1. Quiz app (`CHEM1A/quiz/index.html`) — 5 real failures

| # | Issue | WCAG | Fix |
|---|---|---|---|
| 1 | Sign-in inputs (`gLast`, `gId`, `gSection`) have `<label>` elements **not associated** — no `for` attribute. Screen readers announce unlabeled fields. | 1.3.1, 3.3.2, 4.1.2 | Add `for="gLast"` etc. (3 attrs) |
| 2 | Error line `#gateErr` and answer `#feedback` are plain divs — content changes are **never announced** to screen readers. | 4.1.3 | `role="alert"` on gateErr; `aria-live="polite"` on feedback |
| 3 | After answering, the correct choice is marked **by background color only** (green `.correct` / orange `.wrong`). Feedback text says right/wrong but not *which* choice was correct — invisible to SR and colorblind users. | 1.4.1 | Append "✓ correct answer" text (or visually-hidden span) to the keyed choice |
| 4 | **Focus is lost** after each answer: all choice buttons get `disabled` (focus drops to body), and `render()` swaps the question without moving focus. Keyboard/SR users must hunt for the Next button every item. | 2.4.3 | `nextBtn.focus()` after answer; focus the question heading on render |
| 5 | Nuclide notation `[[27\|13\|Al\|3+]]` renders visually stacked A/Z but reads as bare digits ("27 13 Al 3+") — mass/atomic number meaning is visual-only. | 1.3.1 | In `fmt()`, wrap with `aria-label`, e.g. `aria-label="aluminum-27, atomic number 13, charge 3+"` — one function, fixes every question |

**Passes (verified):** all contrast pairs (err 5.00, muted 5.85, white-on-green 6.25, ink 15.62); native `<button>` throughout (fully keyboard-operable); `lang="en"`; page title; mastery chips show "1/2" counts, not color-only; no keyboard traps. `roster-tool.html` is instructor-only — out of student scope.

All 5 fixes are in one file, ~20 lines total. Question banks (JSON) need no changes — `fmt()` handles rendering.

## 2. Syllabus sites (both courses, same template) — strong, minor fixes

This template is well above average: skip link, native `<details>/<summary>` accordions, native buttons for section nav, `aria-label` usage, meaningful alt text on **all** images, correct h1, high-contrast palette (white-on-red 6.04, footer 9.41, `.tbd` 5.64 — all pass).

| # | Issue | WCAG | Fix |
|---|---|---|---|
| 1 | Grade bar "Lab 20%" label: white bold 12.5px on coral `#E85D75` = **3.34:1 — fails** (bold text this small doesn't qualify for the 3:1 large-text allowance). Other segments pass (red 6.04, gold uses ink, green 5.03). | 1.4.3 | Darken coral for this segment or switch label to ink on light coral |
| 2 | Heading skip h2 → h4 ("RAM Pantry" section), both files | 1.3.1 | Make it h3 |
| 3 | `<th>` without `scope` — 4 tables (1A), 5 tables (3A) | 1.3.1 | Add `scope="col"` |
| 4 | `.peek` hover/focus popovers (5 per page): content shown on hover isn't dismissable or hover-persistent; likely unreachable on touch | 1.4.13 | Convert to `<details>` or click-toggle |
| 5 | Pale ✓ ticks (`#D8CCC3`, 1.51:1) in the weekly schedule — fine **if decorative**; if they convey completion state, they fail | 1.4.11 | Confirm intent; add `aria-hidden="true"` if decorative |
| 6 | Emoji in headings/nav buttons ("🥧 Grade Map", "🕵️ 5%") — SRs read emoji names aloud ("detective… 5%"); the Mystery segment is labeled *only* by emoji | 1.1.1 (minor) | `aria-hidden` the decorative emoji; give gb-mys a text label |

## 3. Scope notes

- Audit covered rendered engine + template code, not a live assistive-tech pass (NVDA/VoiceOver). The five quiz fixes are the ones such a pass would surface first.
- CHEM3A folder has additional student-facing pages (`mock-sc1`, `review/`, `r/`, `Remediation`, `final`, `gilleyum`) and CHEM1A has `grade_tracker`, `mystery`, `review/`, `r/`, `uf` — **not audited**. Same template family likely, but unverified. Say the word and I'll sweep them.
- Live = local confirmed for quiz and both syllabi (syllabi differ by ~12 trivial lines — republish after fixes to stay in sync).

## 4. Priority order

1. Fix the case-sensitive 404 syllabus links in both Canvas shells (2-minute fix, affects every student).
2. Quiz app: 5 fixes, one file (~20 lines).
3. Syllabi: coral contrast + th scope + heading skip (mechanical).
4. Decide on peek popovers, ticks, emoji labels.
5. Optional: sweep remaining github.io student pages.
