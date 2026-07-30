# Build a teaching tool with AI
### FCC Chemistry · 90 minutes · Everything happens in your browser

**By the end of today you will have a working tool at a real web address
you can paste into Canvas.**

Catalog: **https://fcc-chem.github.io/tools/**
Repository: **https://github.com/FCC-Chem/tools**

---

## Before we start

- [ ] Signed in to GitHub
- [ ] Accepted the invitation to **FCC-Chem**
- [ ] Have an AI assistant open in another tab — Claude, Copilot, or ChatGPT

---

## Step 1 — Pick something small

The most common mistake is picking something too big. You have 40 minutes.

**Good size:**

- A calculator that does one conversion your students always get wrong
- A visual that shows one concept changing as a slider moves
- A randomized practice problem generator
- A lookup table with search

**Too big for today:**

- Anything reading a gradebook file
- Anything sending email
- Anything with accounts or saved data

Write your idea here in one sentence:

> _____________________________________________________________________

---

## Step 2 — Get the template

1. Go to **https://github.com/FCC-Chem/tools/blob/main/_template/index.html**
2. Click the **Raw** button (top right of the file)
3. Select all (`Ctrl/Cmd + A`), copy (`Ctrl/Cmd + C`)

---

## Step 3 — The prompt

Paste this into your AI assistant. Replace the bracketed part with your idea.

```
I teach chemistry at a community college. I'm building a single-file HTML
teaching tool for my students.

Here is my starting template — keep its structure, CSS variables, and
visual style exactly as they are:

[PASTE THE TEMPLATE HERE]

Build me: [DESCRIBE YOUR TOOL IN 2-3 SENTENCES. Say what the student
types in, what they get back, and what course it's for.]

Requirements:
- One single HTML file. All CSS and JavaScript inline.
- No libraries, no npm, no build step. It must work when I double-click it.
- No localStorage or sessionStorage.
- Vanilla JavaScript only.
- Validate input and show a readable error message instead of NaN.
- Always show units in the output.
- Keep the footer link back to ../
- Comment the chemistry, not the syntax.

Give me the complete file. Don't abbreviate any section.
```

---

## Step 4 — Test it before you believe it

**This is the step people skip. Don't.**

AI writes code that runs and computes wrong. That failure is silent and it
is the one that will embarrass you in front of a class.

- [ ] Ask the AI: *"Show me the full file again with no omissions."*
- [ ] Copy it into a text editor, save as `test.html`, double-click it
- [ ] Work **three** examples by hand and check them against the tool
- [ ] Type garbage into every input. Does it fail gracefully?
- [ ] Leave every input blank. Does it crash?
- [ ] Try a number that should be impossible (negative volume, zero mass)

If any answer is wrong, paste the wrong output back to the AI and say what
it should have been. Don't try to fix the code yourself.

---

## Step 5 — Put it on the web

1. Go to **https://github.com/FCC-Chem/tools**
2. Click **Add file → Create new file**
3. In the filename box type: `yourlastname-toolname/index.html`
   - The `/` creates the folder. That's the trick.
   - Example: `nguyen-buffer-calc/index.html`
4. Paste your file into the big box
5. Scroll down, click **Commit changes**, then **Commit changes** again

Now the description file:

6. Click **Add file → Create new file** again
7. Filename: `yourlastname-toolname/meta.json` (same folder name exactly)
8. Paste this and edit it:

```json
{
  "title": "Buffer pH Calculator",
  "author": "Your Name",
  "course": "CHEM 3A",
  "description": "One sentence. This shows on the catalog card.",
  "tags": ["acid-base", "calculator"],
  "status": "working"
}
```

9. **Commit changes**

---

## Step 6 — Watch it appear

- Go to the **Actions** tab. A job is running.
- Wait about 60 seconds.
- Open **https://fcc-chem.github.io/tools/**

Your tool is on the catalog. Nobody added it to a list. The page rebuilt
itself.

Your tool's direct link, to paste into Canvas:

**https://fcc-chem.github.io/tools/yourlastname-toolname/**

---

## Step 7 — Steal from each other

- Open the catalog. Open somebody else's tool.
- Find one you could use.
- Copy its code (**Raw** → select all → copy)
- Paste into your AI: *"Adapt this for [your course]. Keep the layout and
  styling. Change [what you want different]."*
- That took ten minutes. That's the whole point of today.

---

## If you get stuck

| Problem | Fix |
|---|---|
| Page is blank | Missing `</script>` or `</html>`. Paste the file back to the AI: *"This renders blank, find the error."* |
| Nothing happens on click | Button id doesn't match the JavaScript. Paste the file back and say so. |
| 404 at the catalog URL | Wait 60 more seconds. Check the Actions tab finished green. |
| Tool missing from catalog | `meta.json` is in the wrong folder, or has a trailing comma. |
| Changes don't show | Hard refresh: `Ctrl/Cmd + Shift + R` |
| Truly stuck | Grab the ready-made folder from `_template` and ship that. Shipping beats perfect. |

---

## The four rules

1. **No student data in this repository.** Ever. It's public.
2. **No passwords or API keys.** They get scraped within minutes.
3. **No answer keys or exam content.** Public repos are permanently mirrored.
4. **Don't edit someone else's folder.** Copy it into your own.

---

## After today

- **Issues tab** — describe a tool you want. Someone may build it.
- **Discussions tab** — post what you made, ask questions.
- Next month: 30 minutes, show what you built.

> Unofficial faculty project. Not an official channel of Fresno City
> College or SCCCD.
