# Orbital Overlap (Bonding Theories): instructor notes

Working title **Orbital Overlap**. Repo/hub label: **Bonding Theories**. Suggested repo `ItsDrDan/bondingtheories`, short link `games.itsdrdan.com/bonding`.

- **Courses:** CHEM 1A (default) and CHEM 1B review. Link with `?course=1A` or `?course=1B`; progress is saved separately per course on the student's device.
- **Source:** OpenStax *Chemistry 2e* §7.6 (VSEPR) and §8.1–8.4. Numbers in the game: the H₂ energy curve (74 pm, 436 kJ/mol, §8.1), real angles (NH₃ 107.3°, H₂O 104.5°, §8.2; v1 said 107°, corrected in v2 to match OpenStax), and bond lengths/energies from **Table 8.1** (H–Cl, H–Br, H–I, C–C/C=C/C≡C, C–N/C=N/C≡N, C–O/C=O/C≡O), all checked against openstax.org on 2026-11-11. Bond orders, electron counts, unpaired electrons and magnetism are **computed** from the MO filling, never typed in.
- **Current file:** `bonding-theories-v20.html` (version in the file name only). Earlier versions are kept here for comparison.
- **v20 more bond-energy problems and resonance bond order (2026-11-12):**
  - **16 new bond-energy reactions, 37 in all.** All values are recomputed with OpenStax Table 7.3. The Tro test bank uses its own values (C=O 799, C–H 414), so only its reactions were used as models; the wording is original.
    - Modeled on OpenStax Ch 7 exercises 65–66: CH₄ + I₂ (+30 kJ, a true endothermic one), C₂H₄ + 3 O₂ (−1055), 2 C₂H₆ + 7 O₂ (−2340), Cl₂ + 3 F₂ → 2 ClF₃ (−807).
    - Modeled on Tro Ch 10 items: C₂H₂ + 2 Br₂ (−228), PCl₃ + Cl₂ (−417).
    - New: C₂H₄ + Cl₂ (−151), C₂H₄ + Br₂ (−94), H₂ + O₂ → H₂O₂ (−134), CH₂O + H₂ (−52) and its reverse (+52), ethanol combustion (−1020), 2 NH₃ + 3 Cl₂ (−469), N₂ + 2 H₂ → N₂H₄ (+98), 2 HBr (+114), 2 HI (+4).
    - Every reaction is checked for balance, ΔH and electron counts.
  - **New topic, "Which structure is more stable?"** (Overlap Basics), modeled on OpenStax exercise 67. Add up all the bond energies in two isomers; the larger total is more stable. Half the items ask for both totals first.
    - Pairs: H₂N–OH 1444 vs H₃N–O 1370; ethanol 3234 vs dimethyl ether 3190; acetaldehyde 2746 vs ethenol 2670; HCN 1306 vs HNC 1281; HOCl 669 vs HClO 637.
    - Lone pairs on formal-charge atoms are set by hand. Formal charges are not drawn.
  - **New topic, "Bond strength & energy concepts"** (Overlap Basics), modeled on OpenStax exercise 64 and Tro items 21–23 and 51.
    - Which bond is strongest/weakest within a family: single/double/triple, H–X and C–X down the halogens, C–H/N–H/O–H, C–C/C–N/C–O. It uses Table 7.3, and the F–F anomaly is avoided.
    - Six concept questions: breaking bonds is endothermic, when a reaction is exothermic, why the result is an estimate, triple strongest, the definition of D, and forming 2 mol H–Cl releases 864 kJ.
  - **New topic, "Bond order with resonance"** (Sigma & Pi). Average bond order = total bonds in one structure ÷ number of equivalent positions.
    - Species: CO₃²⁻ and NO₃⁻ (4/3), NO₂⁻, O₃, formate HCO₂⁻ and benzene C–C (3/2).
    - Half the items add a bond-length/strength comparison: every bond is identical and in between a single and a double bond.
    - Answers like 4/3, 1.33 or 1⅓ are accepted (±0.011). 1.3 is not.
  - Number fields can now carry their own tolerance (`tol`). The question-bank sampler passes it on, so bank items accept 1.33 for 4/3.
- **v19 bond energies → ΔH (OpenStax §7.5, 2026-11-12):**
  - **Two new topics in the Overlap Basics tile** (the tile now reads §7.5, §8.1).
    - **Bond energies → ΔH:** four steps. (1) Count every bond in the reactants (times the coefficients) and add up ΣD broken. (2) The same for bonds formed in the products. (3) ΔH = ΣD(broken) − ΣD(formed). (4) Exothermic or endothermic.
    - **Quick ΔH from bond energies:** one typed step. It is also the 11th item in Skill Check Prep, and the question-bank sampler sends it to Daily 5 under chapter 1A-7.
  - **Data:** bond energies are OpenStax Table 7.3 (Bond Energies, kJ/mol), copied from openstax.org on 2026-11-12. Note that C=O is 741 and C≡O is 1080. The book's own examples come out right with them: H₂ + Cl₂ is −185 kJ, and the ethylene + water Check Your Learning is −35 kJ. Every bond in the reactants is broken and every bond in the products is formed, as in the OpenStax method.
  - **Reactions:** 21 gas-phase reactions, all balanced and checked by hand. 17 are exothermic (H₂ + halogens, H₂ + O₂, the Haber process, CH₄/CH₃OH/C₃H₈ combustion, hydrogenations, chlorinations, N₂H₄ + O₂, 2 H₂O₂, HCN + 2 H₂) and 4 are endothermic reverses. OpenStax's own worked example (CO + 2 H₂) and Check Your Learning reaction are left out.
  - **What students see:** each reaction shows Lewis structures. Bond counts come from the drawings, so the two can't disagree. A short D table lists the bonds in the reaction, their single/double/triple versions, and a few distractors. The full Table 7.3 opens in the Hint and in the Bonding Sheet.
  - **Targeted feedback:** forgetting the coefficient, using the "only bonds that change" shortcut where every bond is asked for (it gives the same ΔH, so the quick version accepts it), and flipping the sign (formed − broken).
  - Reaction arrows are drawn, per the style guide. The video panel shows "Intro to Thermochemistry".
- **v18 VSEPR chart in hints, and a hint for every step (2026-11-12):**
  - **VSEPR chart in the Hint box.** The illustrated chart from Lewis Structure Studio (electron groups × lone pairs, with wedge-and-dash drawings) opens inside the Hint for: Hybridize the center, Flat Lewis → real angle, Shape → groups & lone pairs, Shape around an atom, sp³d and sp³d², Hybrid table, Hybrid Mixer and How many are sp²?
    - The drawings were made by running the Lewis game's own chart code, so they match that game. Here they are drawn at one common scale, and angles read 109.5° (the Lewis chart says 109°) to match OpenStax and the rest of this game.
    - The chart is also at the bottom of the Bonding Sheet.
    - Hints stay hidden in Skill Check, Challenge and Face-Off, so the chart doesn't show there.
  - **Every step now has a hint.** The fixed-question topics (What makes a bond, Why bond strengths differ, Why hybridize?, Where π bonds come from, Restricted rotation, Resonance, LCAO pictures, MO concepts) used to fall back to "Go back to the Professor Tip above." Each now has a "how to start" hint. A check of every topic finds no step without one.
- **v17 missed steps and Skill Check variety (2026-11-12):**
  - **Missed steps no longer look right.** In strict rounds (Skill Check, Challenge, Daily 5, Face-Off), a missed step used to be redrawn as a green ✓ box holding the correct answer, and the "Not quite" message was replaced by "Done." A student who typed 1 for the F₂⁻ bond order saw a green box with 0.5 in it. Grading was right; the display was misleading.
    - A missed step now shows in coral as "Step N: missed". It shows the student's answer with only the wrong boxes struck through (for example "Bond order: ~~1~~ · Unpaired electrons: 1 ✓"), the reason, then the correct answer.
    - A revealed step (Show step) shows in lavender as "answer shown".
  - **Notation pass:** a final pass formats all text before it goes on the page.
    - MO labels get subscripts: σ<sub>2s</sub>, σ*<sub>2p</sub>, π*<sub>2p</sub>. This covers text, choices and the MO diagram labels.
    - p<sub>x</sub>, p<sub>y</sub>, p<sub>z</sub> all use one style. Orbital Studio feedback used to show "p_y" and "p_z" with literal underscores, and pₓ used a Unicode subscript unlike p<sub>y</sub>/p<sub>z</sub>.
    - Any plain-text sp2/sp3/sp3d2 gets superscripts.
    - A browser scan of every topic found nothing left unformatted. It covered questions, wrong-answer feedback, hints, shown steps, Orbital Studio feedback, Learn mode and the Bonding Sheet.
  - **Typed hybridization answers superscript as you type:** sp3 → sp³, sp^2 → sp², sp3d2 → sp³d². The cursor stays in place.
  - **Skill Check Prep: one of each of ten typed question kinds per round.** It used to be 6 kinds, with bond order, hybridize-the-center and hybridize-an-atom each appearing twice. The ten kinds are:
    - count σ/π, σ/π in line drawings, "how many are sp²", shape → groups and lone pairs
    - typed bond order + unpaired electrons, typed central-atom hybridization, typed hybridization of a numbered atom
    - new: typed end-atom hybridization (C=O oxygen, C≡N nitrogen), typed "hybrids made / p left over", typed MO electron count
- **v16 end atoms and whole-bond descriptions (2026-11-12):**
  - **New Hybrid Workshop topic, "End atoms: C=O oxygen, C≡N nitrogen":** asks the hybridization of an O or N at the end of a double or triple bond, using the same rule as any atom (bonded atoms + lone pairs). For example, a C=O oxygen is 1 + 2 = 3 groups → sp², and a C≡N nitrogen is 1 + 1 = 2 → sp. About a third of these questions are typed instead of multiple choice.
    - Molecules: 15 end atoms from the game's molecules (N₂, HCN, CO₂, CH₂O, CH₃CN, HCOOH, HONO, CH₃COOH, acrylonitrile, Cl₂CO, ClNO) plus four molecules added for these two topics only: acetaldehyde, acetone, formamide and urea.
  - **New Sigma & Pi topic, "Describe a whole bond":** pick the full description of a highlighted multiple bond, for example "σ: C sp² – O sp²; π: C 2p – O 2p". There are 20 bonds: C=O, C=C, C≡C, C≡N, N≡N, N=N and N=O.
    - Wrong choices: a wrong hybrid on the end atom (O called sp³), π made from hybrids, σ and π swapped, the wrong number of π bonds, and "two σ" or "three σ".
  - Both topics are single-step, so the question-bank sampler copies them into the shared bank, and from there into the hub Daily 5. Both are in the Daily 5 "medium" tier and in Challenge.
  - **Terminal-atom convention:** these topics, Orbital boxes, Label one bond and Bond Labeler all hybridize end O and N atoms by counting groups. Tag every atom and the typed Skill Check atom questions still use only atoms bonded to 2+ others.
- **v15 audit fixes (2026-11-12):**
  - **Scoring:** in Daily 5, Skip used to pull a new question without moving the round on, so a slot could be answered twice (a Daily 5 could show "7 / 7") and a miss could be erased. Now, in any round, Skip reveals the rest of the question, counts it as missed, and hides itself once the question is done.
  - **Orbital roles:** roles are now checked orbital by orbital. Labeling the ↑↓ hybrid "σ bond" and the ↑ hybrid "lone pair" used to pass because the roles were compared as a set.
  - **Typing:** a format slip no longer counts as wrong; it gets an info message and the streak is kept. Typed hybridizations accept "sp3 hybridized", "sp³ hybrid" and "sp3 orbitals". Numbers accept "+2", E-notation and ×10^. "1,200" is read as a thousands separator, while "2,5" still gets the decimal-comma message.
  - **XP (per STYLE-GUIDE):** 10 per independent correct answer + 2 per streak step (max +10). 2 XP for a reveal or for finishing after a miss.
  - **Daily 5:** the +20 bonus, streak and "Daily Habit" badge are tracked for this game, so another game's Daily 5 no longer blocks them. The shared hub streak is still updated. Replays don't add to the count.
  - **New badges:** On a Roll (5 in a row), Unbreakable Bond (10 in a row), Explorer (Learn, Practice, Challenge, Daily 5, Skill Check Prep).
  - **Topic changes:** during a round, a topic change is saved for after the round instead of silently ending it. In Practice, the current question stays unless its own topic is turned off. Rounds keep the sp³d/sp³d² setting they started with.
  - **Chemistry text:**
    - The I₃⁻ angle feedback no longer says "F atoms".
    - A 120° pick for XeF₂/I₃⁻ now explains equatorial vs axial positions.
    - The angle, MO-ordering and ionization Professor Tips no longer state the answer.
    - The Studio sp³ note about lone pairs shows only when there are lone pairs.
    - The "hybrids made" diagnosis checks "forgot the s orbital" first.
    - π "Label one bond" distractors explain σ vs π, and slip tags use tagSlip.
  - **OpenStax terms:** the Bonding Sheet and the shape-vs-eg slip give the OpenStax names (electron-pair geometry, molecular structure).
  - **Orbital Studio:** atoms have tap areas of about 50 px on phones (they were 22–30 px), sized so neighbors never overlap. NH₃/CH₄/H₂O stems no longer call x "the internuclear axis", and C₂H₄ says "along the C=C axis". For H₂ the first atom starts selected.
  - **Small fixes:** the miss count resets on each new question. Skips in strict rounds list the missed steps. Smooth scrolling respects reduced motion everywhere.
- **v14 Face-Off fixes:** the "Which theory?" He₂ item had "Both VB and MO" as its key, which fought the tip ("bond order → MO") and marked MO answers wrong; it now asks which theory gives He₂ a bond order of 0 (MO). Strict rounds (Face-Off, Challenge, Skill Check, Daily 5) count a question only when every step is right; the end-of-question message now says which step was missed, and the results list shows "2 of 3 steps right; missed step 2" on multi-step misses, with a one-line note that every step must be right.
- **v13 Orbital Studio:** a truer 3D view. The z direction is foreshortened (cabinet-style) with mild perspective: atoms behind the page (−z) draw smaller and closer in, like a dash; atoms in front (+z) draw a little larger, like a wedge. C2H4 is viewed looking down onto its molecular plane (the textbook picture), so the two ends are symmetric and the 120° trigonal layout reads clearly: back H's small and tucked behind the upper p_y lobes, front H's larger and lower. The axis gizmo follows each molecule's view.
- **v12 Orbital Studio:** true 3D depth while building. Atoms and lobes are drawn back to front by their z position, so an atom behind the plane (for example the back H's in C2H4) sits behind a p lobe instead of on top of it. Each atom stays above its own lobes, and atoms can still be tapped or dropped onto when they sit behind a lobe. In the overlap-labeling step all atoms stay on top so the numbered markers are easy to read.
- **v11 Orbital Studio:** the 90° marks are gone from the diagram. Instead, most Studio items now have a step 3 angle question: the angle between the two π bonds of a triple bond (90°), between p_y and the sp² plane in C2H4 (90°), and between hybrids in BeH2 (180°) and CH4/NH3/H2O (109.5°). Diatomics without hybrids keep two steps. σ bonds now show real overlap: hybrid and p lobes stretch along the bond until they meet the partner's lobe or the H 1s sphere, and the lobe facing the partner is drawn in the same (blue) phase so the overlap reads as in phase. An orbital that does not point at the partner (for example p_y on F in HF) stays short and shows no overlap.
- **v10 Orbital Studio:** π bonds are drawn as arcs joining the same-side lobes of the two p orbitals (p_y arcs green, p_z arcs purple, matching the y and z axis arrows), with a right-angle "90°" mark on atoms that have both p_y and p_z, so the two π bonds of a triple bond read as perpendicular. Arcs appear live while building (dashed) and solid in the labeling step. Removing orbitals: an Eraser card (drag onto an atom or tap), a red × on each orbital chip, and dropping the same card on an atom again; a one-line note under the cards says so.
- **v9 rounds:** Challenge now draws from every tile (2 Overlap Basics, 3 Hybrid Workshop, 3 Sigma & Pi, 2 MO Builder) and any topic can come up, including the Orbital Studio, Bond Labeler, Hybrid Mixer, Ranker and MO concepts (sp³d/sp³d² only when that topic is on). Skill Check Prep (typed answers only) is now 2 σ/π counts, 1 "How many are sp²?", 1 "Shape → groups & lone pairs", 2 bond order + unpaired, 2 typed central-atom hybridization, 2 typed atom hybridization.
- **v8: Orbital Studio (3D)** (Sigma & Pi tile, on by default): a 3D view with x (right, the internuclear axis for linear molecules), y (up) and z (toward the student). Step 1: drag orbital cards (s, pₓ, p_y, p_z, sp, sp², sp³) onto each atom, or tap an atom then a card; lobes appear pointing in 3D, hybrids aimed at neighbors and lone pairs. Adding s to one H gives every H its 1s. Step 2: the overlaps glow and get numbers; students mark each σ (on the axis) or π (above/below). Molecules: H₂, HF, HCl, F₂, BeH₂, CH₄, NH₃, H₂O, C₂H₄ (molecule in the xz plane, so the π p is p_y), C₂H₂, HCN, N₂. Halogens in HF/HCl/F₂ use the half-filled p along x (OpenStax §8.1, no hybrids). For N₂ and the N of HCN, both sp + p_y + p_z and pₓ + p_y + p_z are accepted. Slips named: H hybridized, s used on a non-H atom, wrong hybrid (lone pairs / double bond counted twice), hybrids added to a halogen diatomic, missing π p orbital, π p in the wrong direction, a p already used by the hybrids, σ vs π.
- **v7:** the Skill Check bond-order questions ("Use MO theory for O₂…") now show an empty MO diagram students can tap to fill as a scratch pad (not graded; Clear button; paper still works). The typed bond order and unpaired electrons are what's graded. The bond-order-trends hint now points at the neutral reference diagram instead of "on paper".
- **v6 additions** (question types modeled on OpenStax Ch 8 exercises and the Tro 6e Ch 11 test bank; all wording original, no items copied):
  - Hybrid Workshop: **How many are sp²?** (count sp / sp² / sp³ central atoms, or species with a π bond, from formulas), **Shape → groups & lone pairs** (hybridization + molecular shape → bonded atoms and lone pairs), **Shape around an atom** (VSEPR shape and hybridization of one interior atom in a bigger molecule). New "Why hybridize?" cards: why carbon can't use sp³d, why PF₅ exists but NF₅ doesn't.
  - Sigma & Pi: N₂ "three π bonds?" and allene's perpendicular CH₂ planes; a third boss molecule, **acetaminophen (Tylenol)**: 20 σ, 4 π, 7 sp² C.
  - Overlap Basics: why C≡C (839) isn't 3 × C–C (347).
  - MO Builder: **Which is paramagnetic?** (pick from 4 species), **Order the MOs** (increasing energy, Li₂–N₂ vs O₂–Ne₂), **MO concepts** (odd/even electrons and magnetism, 5 + 5 AOs → 10 MOs, why bonding MOs are lower, F₂²⁺ has BO 2, N₂²⁺ diamagnetic vs O₂⁴⁺ paramagnetic, H vs H₂ and O vs O₂ ionization energy, B₂ uses all three 2p).
  - New molecules: BeH₂, CS₂, Cl₂CO, ClNO, NH₂⁻ (Lewis/central atom); I₃⁻, ICl₄⁻, BrCl₃ (expanded octet); HONO, N₂F₂, N₂F₄, CH₃COOH (interior atoms). Molecules with F are left out of the bond-label questions (terminal-halogen hybridization is a convention call).
  - Still held back: CO, CN⁻, NO (heteronuclear MO). Tro has them but OpenStax Ch 8 doesn't.
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
