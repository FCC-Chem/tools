# Script tool template

Copy this whole folder to `yourname/toolname/` to start a script tool.

## What's here

| File | Required | Purpose |
|---|---|---|
| `script.py` | yes | The tool |
| `meta.json` | yes | Catalog card. **`"kind": "script"` is what makes it a script tool.** |
| `SPEC.md` | strongly recommended | Plain-English contract. This is what lets AI adapt it. |
| `sample_roster.csv` | strongly recommended | Fake data with the real column structure |
| `.env.example` | if credentials needed | Template for secrets |

Script tools have no live URL — they're downloaded and run. The catalog
shows them with a **Script** badge and links to the spec and source
instead of an "Open tool" button.

## Try it right now

```bash
cd _template-script
python3 script.py
```

No flags, no setup, no credentials. It prints eight sample emails and
sends nothing.

## Rules

1. **Dry run must be the default.** Destructive or outbound actions
   require an explicit flag.
2. **Credentials from `.env`, never in the file.**
3. **Ship synthetic sample data.** Real student data never enters this repo.
4. **Write the spec.** Without it, the next instructor gets code they
   can't adapt and won't trust.
