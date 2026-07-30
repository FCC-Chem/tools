# Spec: Weekly grade update emailer

**This file matters more than the code.** Paste it, plus `script.py` and
`sample_roster.csv`, into an AI assistant and it can rebuild the whole thing
for your course. The code alone is not enough — it doesn't say what any of
it is *for*.

---

## What it does

1. Reads a gradebook CSV
2. Computes each student's weighted percentage and letter grade
3. Prints (or emails) a short summary with a per-category breakdown
4. Adds a "come see me" paragraph for anyone below a threshold

Also does single-student lookup for office hours:

```bash
python3 script.py --roster export.csv --student "Rivera"
```

---

## Input format

CSV with a header row. Required columns:

| Column | Meaning |
|---|---|
| `name` | Student name, any format |
| `email` | Where the message goes |

Then, for each grade category, a pair of columns:

| Column | Meaning |
|---|---|
| `homework_earned` | Points the student has |
| `homework_possible` | Points assigned so far |

Same pattern for `quizzes`, `labs`, `exams`. See `sample_roster.csv`.

**Blank or zero `_possible` means "not graded yet."** Those categories are
dropped from the average and the remaining weights are renormalized —
*not* counted as zeros. Counting ungraded work as zero is the most common
bug in scripts like this, and it tells a student in week 3 that they're
failing when they aren't.

---

## Configuration (top of `script.py`)

| Setting | What to change it to |
|---|---|
| `COURSE_NAME` | Your course |
| `INSTRUCTOR` | Your name, as it should appear in the signature |
| `OFFICE_HOURS` | Days, times, room |
| `WEIGHTS` | Your category weights. **Must sum to 1.0** — the script checks and refuses to run otherwise. |
| `CUTOFFS` | Your letter grade cutoffs |
| `CONCERN_BELOW` | Percentage that triggers the concern paragraph |

---

## Credentials

Never in the file. Copy `.env.example` to `.env` and fill it in:

```
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=you@scccd.edu
SMTP_PASS=your-app-password
FROM_EMAIL=you@scccd.edu
```

`.gitignore` blocks `.env`. Do not remove that line.

Most institutions require an **app password**, not your normal login, and
many block SMTP entirely from off-campus. Check before workshop day.

---

## Safety behavior

- **Dry run is the default.** No `--send` flag, no mail leaves your machine.
- Refuses to start if `WEIGHTS` don't sum to 1.0
- Refuses to start if required CSV columns are missing
- Skips students with nothing graded rather than emailing them a 0%

---

## Adapting this to your course

Paste this file, `script.py`, and `sample_roster.csv` into your AI
assistant, then say something like:

> Adapt this for my course. I teach CHEM 3A. My weights are 30% homework,
> 20% labs, 50% exams — no quiz category. My Canvas export has columns
> named `Student`, `SIS Login ID`, and one column per assignment instead
> of the earned/possible pairs. Rewrite it to handle that, keep the
> dry-run default, and show me the full file.

The two things that make this work are the sample CSV (so the AI can see
the real column structure) and this spec (so it knows the *intent*, not
just the syntax).

---

## Before you trust it

- [ ] Run on `sample_roster.csv` first — no flags
- [ ] Hand-check three students against Canvas with a calculator
- [ ] Check the student with an ungraded category — are they dropped, not zeroed?
- [ ] Run on your real export, still no `--send`, and read the output
- [ ] Send to **yourself only**: `--student "Your Name" --send`
- [ ] Only then run it for the class

A grade email that's wrong doesn't just fail — it reaches students before
you find out.

---

## Rules

- **Never commit a real roster.** `.gitignore` blocks `*.csv` except `sample_*.csv`.
- **Never commit `.env`.** Anything pushed to a public repo is scraped within minutes.
- **Never paste real student data into an AI chat.** Use the sample file.
