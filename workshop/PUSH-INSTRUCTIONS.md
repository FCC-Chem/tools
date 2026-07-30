# Push this to GitHub

Run these from a terminal on Linux (Ubuntu/Debian). Total time: about 5 minutes.

---

## 0. One-time: install and authenticate the GitHub CLI

If `gh --version` already works, skip the install.

```bash
sudo apt update && sudo apt install gh -y
gh auth login
```

Choose: **GitHub.com** → **HTTPS** → **Login with a web browser**.
Paste the code it gives you.

Verify you're in the org:

```bash
gh api user --jq .login
gh api user/orgs --jq '.[].login'
```

The second command must list `FCC-Chem`. If it doesn't, the org name is
different from what we assumed — tell me and I'll adjust the URLs baked
into the files.

---

## 1. Create the repo and push

```bash
cd ~/Desktop/FCC-Chem-tools

git init -b main
git add .
git commit -m "Initial scaffold: template, catalog builder, two example tools, workshop materials"

gh repo create FCC-Chem/tools \
  --public \
  --source=. \
  --description "Teaching tools built by FCC Chemistry faculty, with AI." \
  --push
```

---

## 2. Turn on Pages

```bash
gh api -X POST repos/FCC-Chem/tools/pages \
  -f 'source[branch]=main' \
  -f 'source[path]=/'
```

If that returns `409 Conflict`, Pages is already on — fine, move on.

Confirm:

```bash
gh api repos/FCC-Chem/tools/pages --jq .html_url
```

Give it 1–2 minutes, then open **https://fcc-chem.github.io/tools/**

---

## 3. Turn on Discussions and set repo metadata

```bash
gh api -X PATCH repos/FCC-Chem/tools \
  -F has_discussions=true \
  -F has_issues=true \
  -F has_wiki=false \
  -F has_projects=false

gh api -X PUT repos/FCC-Chem/tools/topics \
  -f 'names[]=chemistry' \
  -f 'names[]=education' \
  -f 'names[]=teaching-tools' \
  -f 'names[]=community-college'
```

---

## 4. Allow the Action to commit the rebuilt catalog

**This one is not optional — the catalog will not update without it.**

```bash
gh api -X PUT repos/FCC-Chem/tools/actions/permissions/workflow \
  -F default_workflow_permissions=write \
  -F can_approve_pull_request_reviews=false
```

Then kick off a run to prove it works:

```bash
gh workflow run build-catalog.yml --repo FCC-Chem/tools
sleep 30
gh run list --repo FCC-Chem/tools --limit 3
```

You want to see `completed  success`.

---

## 5. Org profile page (optional, 2 min)

Makes `github.com/FCC-Chem` look like a real thing instead of an empty
shell.

```bash
cd ~/Desktop
gh repo create FCC-Chem/.github --public --clone
cd .github
mkdir -p profile
# Copy the text BELOW the "---\n---" divider in
# FCC-Chem-tools/workshop/ORG-PROFILE-README.md into profile/README.md
git add . && git commit -m "Org profile" && git push
```

---

## 6. Invite your people

```bash
gh api -X POST orgs/FCC-Chem/invitations -f email=dan@scccd.edu       -f role=direct_member
gh api -X POST orgs/FCC-Chem/invitations -f email=someone@scccd.edu   -f role=direct_member
```

Or by username, once they've sent it to you:

```bash
gh api -X PUT orgs/FCC-Chem/memberships/THEIR_USERNAME -f role=member
```

**Give everyone write access to the repo** — no pull requests, no review
gates, for the first workshop:

```bash
gh api -X PUT orgs/FCC-Chem/teams/faculty/repos/FCC-Chem/tools -f permission=push
```

That assumes a `faculty` team exists. If you didn't make one:

```bash
gh api -X POST orgs/FCC-Chem/teams -f name=faculty -f privacy=closed
```

Simpler alternative — add each person directly to the repo:

```bash
gh api -X PUT repos/FCC-Chem/tools/collaborators/THEIR_USERNAME -f permission=push
```

---

## 7. Add a second org owner

Insurance against you leaving, retiring, or losing your phone.

```bash
gh api -X PUT orgs/FCC-Chem/memberships/TRUSTED_COLLEAGUE -f role=admin
```

---

## Final check before the workshop

```bash
xdg-open https://fcc-chem.github.io/tools/
```

- [ ] Catalog page loads with 2 tool cards
- [ ] Search box filters them
- [ ] Molar mass calculator computes `Ca(NO3)2` = 164.086 g/mol
- [ ] Titration sim draws a curve, sliders move it
- [ ] Actions tab shows a green run
- [ ] `github.com/orgs/FCC-Chem/people` shows everyone as **accepted**,
      not pending

---

## Making a change later

```bash
cd ~/Desktop/FCC-Chem-tools
git pull            # important -- the bot commits index.html
# edit files
git add .
git commit -m "what changed"
git push
```

**Always `git pull` first.** The Action pushes a commit to `index.html`
after every one of your pushes, so your local copy goes stale
immediately. This is the single most likely thing to trip you up.

---

## If the org name isn't `FCC-Chem`

These strings are hardcoded in `scripts/build_catalog.py`, `README.md`,
`AGENTS.md`, `workshop/HANDOUT.md`, and both example tools' footers.
One command fixes all of them:

```bash
cd ~/Desktop/FCC-Chem-tools
grep -rl 'FCC-Chem\|fcc-chem' . --exclude-dir=.git | \
  xargs sed -i 's/FCC-Chem/YOUR-ORG/g; s/fcc-chem/your-org/g'
python3 scripts/build_catalog.py
```
