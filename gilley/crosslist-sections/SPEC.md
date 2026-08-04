# Spec: Cross-list double sections

**This file matters more than the code.** Paste it plus `script.py` into an
AI assistant and it can rebuild or adapt the whole thing for your courses.

---

## The problem

Every semester you're assigned two sections of the same course — one
lecture, two lab times — and Canvas gives you two separate course shells.
That means posting everything twice and students hunting across two cards.

## What it does

1. Pulls your teacher courses from the Canvas API (nothing hard-coded)
2. Parses section number and term out of each SIS course code
   (`CHEM-3A-25825-2026FA` → course `CHEM-3A`, section `25825`, term `2026FA`)
3. Lists your newest term's shells and asks which to combine — you may
   answer with section numbers (25825) or Canvas course ids from the URL
4. Cross-lists the source section(s) into the destination shell and
   renames it (`CHEM-3A-25825/25826-2026FA`)

Students end up on one Canvas card. Sections survive the move, so
lab-specific due dates still work via "Assign to > section".

## Safety rails (do not remove when adapting)

- **Dry run by default.** `--apply` required to change anything, plus
  typing the destination course id to confirm.
- **Refuses different courses.** Entering a CHEM-1A and a CHEM-3A section
  aborts — prevents merging unrelated classes.
- **Refuses if the source has student submissions.** Submissions do NOT
  follow a cross-listed section. Cross-list before the semester starts,
  while shells are unpublished. `--force` exists; you almost never want it.
- **Build content in the destination shell only.** Content in the vacated
  shell stays behind.

## Undo

Before submissions exist: `DELETE /api/v1/sections/<section_id>/crosslist`
returns the section to its original shell.

## Configuration

`.env` next to the script (copy `.env.example`):

| Variable | Meaning |
|---|---|
| `CANVAS_URL` | e.g. `https://scccd.instructure.com` |
| `CANVAS_API_TOKEN` | Canvas > Account > Settings > + New Access Token |

## What to change for your institution

- `CODE_RE` — the SIS course-code pattern. SCCCD uses
  `SUBJ-NUM-SECTION-TERM` (e.g. `CHEM-3A-25825-2026FA`). If your codes
  differ, adjust the regex; everything else adapts automatically.
- `TERM_ORDER` — season codes used to sort terms (`SP` < `SU` < `FA`).

## Permissions

Requires the `manage_sections_edit` Canvas permission (SCCCD teacher role
has it). If you get a 401/403 on the cross-list call, your district
requires the merge to be done by Canvas admins — ask them instead.
