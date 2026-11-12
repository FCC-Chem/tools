# Orbital Overlap (Bonding Theories): instructor notes

Working title **Orbital Overlap**. Repo/hub label: **Bonding Theories**. Suggested repo `ItsDrDan/bondingtheories`, short link `games.itsdrdan.com/bonding`.

- **Courses:** CHEM 1A (default) and CHEM 1B review. Link with `?course=1A` or `?course=1B`; progress is saved separately per course on the student's device.
- **Source:** OpenStax *Chemistry 2e* §7.6 (VSEPR) and §8.1–8.4. Numbers in the game: the H₂ energy curve (74 pm, 436 kJ/mol, §8.1), real angles (NH₃ 107.3°, H₂O 104.5°, §8.2; v1 said 107°, corrected in v2 to match OpenStax), and bond lengths/energies from **Table 8.1** (H–Cl, H–Br, H–I, C–C/C=C/C≡C, C–N/C=N/C≡N, C–O/C=O/C≡O), all checked against openstax.org on 2026-11-11. Bond orders, electron counts, unpaired electrons and magnetism are **computed** from the MO filling, never typed in.
- **Current file:** `bonding-theories-v5.html` (version in the file name only). Earlier versions are kept here for comparison.
- **v5 look and topic picker:** colors match the Study Hub / MCAT hub (pastel gradient background, rainbow title, chunky cards and buttons with a solid bottom edge). Each tile has its own color (Overlap Basics blue, Hybrid Workshop green, Sigma & Pi pink, MO Builder orange), and questions take their tile's color. Tapping a tile turns on **all** of its topics (including sp³d/sp³d² and the boss molecules); the topic list sits collapsed under "Focus on specific topics" for anyone who wants to narrow it, with a "Turn all topics back on" link.
- **Art:** see `ASSETS.md` (the brief for ChatGPT). v4 picks up each file automatically from `assets/` once it exists and falls back to the drawings and brand badges until then.

## Accuracy pass (v4, Nov 11, 2026)

An independent read of every question, explanation, data table and the MO logic. Fixed:
- Carbonate: "three C=O double bonds would put **12** electrons around C" (was 10).
- XeF₂ and XeF₄ angle answers no longer say the lone pairs "squeeze" the angle (they sit symmetrically: exactly 180° and 90°); the 109.5° "ideal tetrahedral" distractor now appears only for 4-group molecules; XeF₂'s 90° distractor explains axial vs equatorial.
- SF₆ and XeF₄ now ask for the angle between **neighboring** F atoms and never offer 180° (which is a real trans angle).
- O₂ → O₂⁻: the electron goes to "the lowest MO with room (π*2p holds only 2 of 4)", not "the LUMO, half-filled".
- "Which theory?" N₂ vs N₂⁺: VB has no simple way to give a fractional bond order (instead of "can't handle odd electrons").
- "Shorter bond → better overlap → stronger" is now stated for a series of similar bonds (H–Cl/H–Br/H–I), since it isn't general (F–F is shorter but weaker than Cl–Cl).
- The sp electron-geometry question no longer offers "Bent".
- Orbital-box overfill feedback explains by bonding role instead of energy.
- Molecules with functional groups are shown by formula only (CH₃OH, CH₃NH₂, CH₃CN, HCOOH, C₃H₃N); hydrocarbons keep their names.

Checked and found correct: all MOLS/MULTI electron counts and Lewis structures, the ANGLE and Table 8.1 values, MO orderings, all 23 species' bond orders and magnetism, HOMO/LUMO choices, ranking families, orbital boxes and roles, the Mixer, skeletal σ/π counts, caffeine and aspirin, and the Bonding Sheet.
- **Links:** `?mode=daily`, `?mode=skill`, `?mode=challenge`, `?mode=faceoff` (Face-Off only once unlocked), `?mode=learn`.

## New in v3

- **Hybrid Mixer** (Tile 2): tap s, p and d cards into a mixer; it shows live what they make ("3 orbitals in → 3 sp² hybrids + 1 unhybridized p"), then students pick the electron-group geometry. Slips: no s / two s, forgot lone pairs, double bond counted twice, d used before all three p. Expanded-octet molecules appear only when the sp³d/sp³d² topic is turned on.
- **Ranker** (Tile 4): tap 3–4 species of the same element into order by bond order, bond length or bond strength (O₂²⁻/O₂⁻/O₂/O₂⁺ and the N, F, C, B families; bond orders always distinct). A fully reversed order is logged as `bo-length-backwards`.
- **Theory Face-Off** (boss round): unlocks after 5 right in Hybrid Workshop and 5 in MO Builder. 6 questions: liquid O₂ and the magnet (which theory explains it, how many unpaired electrons, which MO holds them), three "Which theory would you use to…" cards (shape → VSEPR, overlap names → VB, magnetism / ion bond order / delocalized π → MO, He₂ → both), a Ranker item and a HOMO/ionization item. The two new topics also live in Tile 4 for practice.
- **Skill Check Prep**: 10 typed answers, no multiple choice: σ/π counts (one line drawing), 3 bond order + unpaired electrons (no diagram given), and 4 typed hybridizations (central atom, or a numbered atom in a bigger molecule). "sp2", "sp²" and "sp^2" are all accepted. Results + study plan.
- **Daily 5**: 2 easy → 2 medium → 1 hard, weighted toward missed and unseen topics, hints allowed. Finishing it updates the **shared day streak** (`itsdrdan-daily-streak`, the same one Bridge to 1B uses) and gives +20 XP once per day.
- **Orbital boxes & roles** (Tile 2, expanded after Dr. Dan's review): questions now come from the game's molecules: 37 different atoms (every B, Be, C, N, O that is central or in a multiple bond, e.g. C in CH₂O, O in C=O of HCOOH, N in CH₃CN, middle C of allene, B in BF₃). The atom is marked "1" on the drawing. Three steps: pick the hybridization, fill the hybrid and leftover-2p boxes, then **label each orbital's job** (σ bond to H/C/N/O, lone pair, π bond to …, empty). Slips: π from a hybrid, σ or lone pair in a 2p, ↑↓ hybrid not called a lone pair. Atoms with a formal charge are left out so the electron count always works.
- **σ or π? Label & count** (Tile 2): numbered bonds (same kind share a number, shown ×n); students mark each as 1 σ / 1 σ + 1 π / 1 σ + 2 π, then count all σ and π bonds in the molecule.
- **MO reference diagram**: Bond order trends (strongest/weakest/shortest/longest) and the Ranker now show the filled MO diagram of the neutral diatomic, with the HOMO outlined, so students add or remove electrons from it instead of guessing.
- New badges: Theory Face-Off Champion (5+ of 6), Skill Check Ready (8+), Daily Habit (3-day streak), Hybrid Mixer Pro. The old "Hybrid Mixer" badge (10 Tile 2 right) is now "Hybrid Handler".

## Question bank

Prepared in the local `questionbank` clone (not pushed): `tools/samplers/bondingtheories.js`, `bondingtheories` added to the nightly build's game list, and 8 entries in `skills.json`. The sampler keeps single-step questions (multiple choice and numbers; σ/π counts become two number items) and skips the interactive diagrams. In a browser test it produced 232 items with every answer accepted by the game. It uses v3 topics, so **push it together with v3**, not before.

## New in v2

- **Bond Labeler (every bond)** (Tile 3): numbered bonds on the drawing; bonds of the same kind share a number. Students pick the σ overlap for each (and the π overlap for double/triple bonds) from a menu. Tap a number on the drawing to jump to its row. Wrong picks name the slip (π from hybrids, H hybridized, σ from 2p, wrong hybrid from forgetting lone pairs or counting a double bond as 2 groups).
- **σ/π in line drawings** (Tile 3): 18 skeletal structures drawn by the SMILES layout engine from Bond Voyage (zig-zag 109.5°/120°/180°, rings). H on carbon is hidden, so this is where the `missed-CH-bonds` slip shows up. Carbons between two collinear bonds (C≡C–, C=C=C) are written as C so they don't disappear in a straight line.
- **Boss molecules** (Tile 3, tagged "challenge", off by default): caffeine (fused rings, placed by hand: 25 σ, 4 π, 5 sp² C) and aspirin (21 σ, 5 π, 8 sp² C). Both values computed from the structure.
- **Why bond strengths differ** (Tile 1): OpenStax Table 8.1 data: H–X length vs strength, π weaker than σ (C=C 614 is less than 2 × C–C 347), more bonds → shorter, end-to-end overlap is greatest, what bond energy means.
- **Energy curve, tap version** (Tile 1): students tap the curve at the bond length (graded within ±10 pm of 74; ◀ ▶ buttons fine-tune and work by keyboard), then tap the arrow that shows the bond energy.
- Challenge now draws from line drawings, boss molecules and bond strengths too. Badges: Bond Labeler = every bond right in 3 molecules; Pi Hunter counts line drawings and boss molecules.

## What v1 includes

| Tile | Topics |
|---|---|
| Overlap Basics (§8.1) | What makes a bond · Energy curve (H₂; read A–D or tap the curve) · Overlap Gallery (s–s, s–p, p–p end-on, p–p side-on → σ/π) · Which orbitals overlap (H₂, HF, HCl, HBr, F₂, Cl₂, Br₂) · Why bond strengths differ (Table 8.1) |
| Hybrid Workshop (§8.2) | Why hybridize · Hybrid table · Hybridize the center (groups → hybrid → geometry/shape) · Flat Lewis → real angle (with wedge/dash sketch in the answer) · Orbital boxes (ground state → hybridized) · Tag every atom (multi-center molecules) · sp³d and sp³d² (tagged "expanded octet", off by default) |
| Sigma & Pi (§8.3) | Count σ and π (all H drawn) · σ/π in line drawings · Label one bond · Bond Labeler (every bond) · Where π bonds come from · Restricted rotation · Resonance & delocalized π · Boss molecules (caffeine, aspirin) |
| MO Builder (§8.4) | LCAO pictures · Which ordering? · MO Diagram Builder (count → ordering → fill AOs → fill MOs → bond order + unpaired → para/dia) · Read a diagram · Bond order trends · HOMO & ionization |

Modes: **Learn** (Professor Tips + worked example revealed one step at a time), **Practice** (hints, Show step, retry), **Challenge** (10 mixed questions across all tiles, no hints, results + study plan).

MO species: H₂, H₂⁺, H₂⁻, He₂, He₂⁺, Li₂, Be₂, B₂, B₂⁺, C₂, C₂²⁻, N₂, N₂⁺, N₂⁻, N₂²⁻, O₂, O₂⁺, O₂⁻, O₂²⁻, F₂, F₂⁺, F₂⁻, Ne₂. Li₂–N₂ use π2p below σ2p; O₂–Ne₂ use σ2p below π2p. Valence electrons only for second-row diatomics.

Organic molecules (ethane, ethene, ethyne, methanol, methylamine, formic acid, acetonitrile, hydrazine, allene, acrylonitrile, benzene, plus the line drawings, caffeine and aspirin) appear **only** for σ/π counting, hybridization and bond labels. Line drawings are labeled by molecular formula only. No functional-group naming or reactions.

## Conventions to know

- **Terminal atoms in "Tag every atom":** students tag atoms bonded to 2+ others, plus one H (to catch "H is sp³"). Terminal O/N/halogens are left out, per OpenStax convention. "Label the bond" still names a terminal O or N by its electron-group count (C=O oxygen is sp², C≡N nitrogen is sp).
- **Resonance species** (CO₃²⁻, NO₃⁻, NO₂⁻, O₃, SO₂, SO₃) are drawn as one octet contributor. They are used for central-atom hybridization and shape only, not σ/π counting.
- **On phones** the MO diagram shows one atom's orbitals plus the MOs (the other atom is identical), so the part students fill fits on screen. Desktop shows the full three-column diagram.
- **XP:** +10 for finishing a question, +5 with no slips, +5 with no help, plus a streak bonus; 2 XP after using Show step.

## Slips logged to Game Stats (game id `bondingtheories`)

From the design outline: `double-bond-two-groups`, `forgot-lone-pairs`, `shape-vs-eg`, `pi-from-hybrid`, `hybrid-count`, `hydrogen-hybridized`, `sigma-pi-total`, `missed-CH-bonds`, `charge-sign`, `wrong-ordering`, `bo-not-halved`, `included-core`, `hund-violation`, `para-dia-flip`, `ionize-wrong-mo`, `bo-length-backwards`.

Added in v1 and v2: `ignored-charge` (used the neutral count for an ion), `one-atom` (counted one atom's electrons), `aufbau` (filled a higher MO before a lower one), `flat-drawing` (read the angle off the flat Lewis drawing), `ideal-angle` (109.5° for NH₃/H₂O), `sigma-vs-pi`, `pi-from-s`, `electron-count`, `group-count`, `tag-count`, `p-overfill`, `hybrid-fill`, `sigma-from-p`, `pe-read`, `length-strength`, `pi-strength`, `overlap-direction`, `hyb-all`, `mixer-no-s`, `mixer-d-early`, `rank-order`, `rank-reversed`, `theory-choice`, `format`, `p-role`, `orbital-role`, `pi-on-single`, `missed-pi`, `count-kinds`, `gave-up` (used Show step), plus `concept`-style codes for the static multiple-choice items.

## Not in v1 yet (per the build plan)

- **v4:** art package (logo, mascot moods, tile icons, badges), study hub card, chemistry accuracy pass. v1 uses an inline SVG p-orbital mascot and brand-kit badges as stand-ins, and `meta.json` has no `logo` entry until the art exists.
- **Heteronuclear / isoelectronic** (CO, CN⁻, NO⁺, NO) is held back until checked against OpenStax §8.4 exercises and the Tro test bank.
- **Videos** open at the start of each lecture; timestamps are not mapped yet.

## To check before pushing

- Read through the worked steps for a few species per topic.
- s–p mixing wording and the N₂/O₂ ordering switch were checked against OpenStax §8.4 (it writes "s-p mixing").
- In caffeine, the ring N atoms count as 4 groups by the simple rule but are really planar; the boss question asks only about carbons to avoid that.
- Decide whether 1B should open on a different default tile.
