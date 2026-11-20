# Sticky Molecules (Intermolecular Forces): instructor notes

Fun name **Sticky Molecules**. Repo and hub label: **Intermolecular Forces**. Repo `ItsDrDan/IMF`.

- **Courses:** CHEM 3A (default), CHEM 1A and CHEM 3B. Link with `?course=3A`, `?course=1A` or `?course=3B`. Topics and labs outside a course are hidden for that course. Progress is saved separately per course on the student's device.
- **Spec:** `CONCEPT-MAP.md` in this repo. The game follows it; where it departs, the difference is listed under "Differences from the spec" below.
- **Current file:** `index.html`, published from the working build `sticky-molecules-v24.html` (version in the file name only; working builds stay local).
- **Status:** live at https://itsdrdan.github.io/IMF/ since 2026-11-12. The values listed under "Values that still need Dr. Dan's review" had not been reviewed when it went live.

## New in v24 (2026-11-14)

- **Mixing Beaker and Solutions Lab open in CHEM 3A.** Both labs are now listed for 3A, and `?course=3A&mode=mix` / `?course=3A&mode=solutions` open them directly (for the CHEM 3A textbook, Sections 11.1 and 11.6). In 3A the Solutions Lab shows the freezing-point model only (no Raoult's law, which is beyond CHEM 3A). This also fixes 3A "Lab: mixing beaker" practice questions, which showed no lab underneath.

## New in v23 (2026-11-13)

Edits Dr. Dan left to my judgment, all applying things he had already asked for.

- **Main controls above the picture in three more labs**, as in the Energy Well and H-Bond Lab:
  - *Protein Fold Lab:* the temperature slider and the Cool and Heat buttons sit above the chain.
  - *Heating Curve Lab:* Add heat, Remove heat, Pause and the slider sit above the curve and the box of molecules.
  - *Solutions Lab:* on a narrow screen the experiment tabs and sliders come before the picture.
  - The Cell Lab and Phase Diagram Explorer are unchanged: in the first the student picks a bath and watches, and in the second the student drags the point on the picture itself.
- **Lab and round links open at the lab.** A link such as `?mode=fold` or `?mode=daily` now folds the tiles into the "Working on" bar, so the lab or round sits near the top of the page. This matters for the lab links in the CHEM 3B textbook and in Canvas. A plain link still shows the tiles.
- During a Challenge or Daily 5 the bar reads "Challenge · 10 mixed questions" or "Daily 5 · 5 questions", without tile names, because a round draws from every tile.

## New in v22 (2026-11-13)

- **H-Bond Lab: choose how many molecules.** A "Number of molecules" slider sits under the molecule buttons. It starts at 12 (8 on a phone) and goes from 4 up to what the box can hold: 26 on a wide screen and 12 or 13 on a phone, depending on its width. The readout says "room for 26" or "the box is full". The limit is set so every molecule still has a place in the crystal and the gas has room to spread.
- The choice is kept when a new prediction loads. Changing it rebuilds the box at the current temperature.

## New in v21 (2026-11-13)

A follow-up from testing v20 on a phone.

- **H-Bond Lab:** the temperature slider now sits above the box of molecules, as in the Energy Well. On a phone the slider and the box fit on one screen, so a student can watch the phase change while sliding. Before, the slider was a full screen below the box.
- Changing the temperature or the molecule while the lab is paused starts it moving again, so the picture never lags behind the readout.

## New in v20 (2026-11-13)

Four lab changes Dr. Dan asked for.

- **H-Bond Lab shows solid, liquid and gas.** Each substance follows its own melting and boiling points (water 0 and 100 °C, ammonia −78 and −33, HF −84 and 20, methanol −98 and 65, methane −182 and −162).
  - *Solid:* the molecules move onto a flat crystal layer and only vibrate. Water makes a net where a molecule in the middle has 4 hydrogen bonds. Ammonia, HF and methanol make chains, each H pointing at the next molecule's lone pair. Methane packs closely with no hydrogen bonds.
  - *Liquid:* the molecules lie in a level pool across the bottom, sliding past each other while hydrogen bonds form and break.
  - *Gas:* the molecules fill the box and no hydrogen bonds are drawn.
  - The readout beside the slider names the phase and both transition temperatures. In the liquid, water still shows more hydrogen bonds per molecule than methanol or HF (about 1.2, 0.9 and 0.8 in test runs).
- **Energy Well:** the "Shine light to add energy" slider now sits above the diagram, so on a phone it is reachable without scrolling past the picture.
- **Electron Coin-Flip shows two atoms.** Atom 1 is the coin flip. Atom 2's electrons are pushed the same way, so a δ+ side always faces a δ− side, and a dashed "attract" line between them gets thicker as the clouds get more lopsided. On an even split it reads "no pull this instant".
- **Protein Fold Lab** has three new predictions that send the student to the slider: which link lets go first, which are still holding at 60 °C, and how the shape changes from 25 to 100 °C. In this model the hydrogen bond lets go near 54 °C, the salt bridge near 59 °C and the hydrophobic core near 65 °C.
- **Seven new lab questions** in all (3 Protein Fold, 2 Coin-Flip, 2 H-Bond Lab), numbers 37 to 43 in `REVIEW-NEW-QUESTIONS.md`. Dr. Dan has not read these yet.

## New in v19 (2026-11-13)

Changes aimed at the weak points named in an honest review of the game.

- **Shorter page.** Once a student taps "Go to your question", picks a mode, opens a lab or taps Next, the tiles and modes fold into one bar: "Working on: Spot the Forces · Practice", with a "Change topics or mode" button. The question then sits near the top of the page. On a desktop-width page the question moved from about 1,260 px down to about 290 px. The achievements list is folded behind "Show all achievements".
- **Tap all that apply.** A new question type with more than one right choice, so a student cannot succeed by recognizing a single answer. It is used in "Who can hydrogen bond?" (about 4 in 10 questions: tap every molecule that can) and in the last step of "Lewis structure → all the forces" (about half: tap every force). Feedback names a wrongly tapped choice and why; a missed one gets a nudge without being named.
- **Mastery needs a re-check.** A mastered topic's dots turn yellow one week after the last unaided correct answer, and the topic stops counting as mastered until one more is answered with no hint. Due topics come up more often.
- **Nine more questions:** ion–dipole (3), sugars (3), surface tension and viscosity (3). They are numbers 28 to 36 in `REVIEW-NEW-QUESTIONS.md`. Dr. Dan read and approved them on 2026-11-13.
- **Not changed in v19:** the game is still one file. The labs were reworked in v20.

## New in v18 (2026-11-13)

- **"Dispersion, size and shape" is now in all three courses** (it was CHEM 1A only), at Dr. Dan's request. CHEM 3A and 3B get 8 of its 10 questions; the two that use the word "polarizable" stay in 1A.
- The Sticky Sheet's "Dispersion and molar mass" tables (halogens, noble gases, hydrocarbons) now show in CHEM 3B too.
- The topic's Professor Tip now names molar mass first.

## New in v17 (2026-11-13)

Dr. Dan's decisions after the v16 audit: use handbook values, keep the hint rules, and finish the open edits.

- **Handbook values.**
  - Pentane's vapor pressure at 25 °C is 512 torr (NIST Antoine equation). The old 425 torr is the value near 20 °C. The Raoult's law questions and the Solutions Lab now use 512 with hexane's 151: equal moles give 331.5 torr, and the "find the mixture" prediction uses 295 torr (mole fraction of pentane about 0.40).
  - CO₂'s critical point is 31.0 °C and 72.9 atm (was 31.1 °C and 73 atm).
  - Chlorine boils at −34 °C, 239 K (was −35 °C, 238 K).
  - The H-Bond Lab sets methanol's stickiness from its boiling point (338 K), like NH₃ and HF. The ranking water > methanol > HF > NH₃ > CH₄ = 0 still holds from −20 to 60 °C.
- **A ± key** beside the freezing or boiling point box, because the iPhone number keypad has no minus key.
- **Eighteen more questions** in the small banks: osmosis (3), protein folding (3), membranes and colloids (3), dispersion (3), fatty acids (1, arachidonic acid), heating-curve predictions (2), phase-diagram predictions (2), Protein Fold Lab (1). With v16's nine, 27 questions are new since v15; all are listed under "Values that still need Dr. Dan's review", and Dr. Dan approved them on 2026-11-13.
- **Mole fraction of an ionic solute** now says to count whole formula units.
- **Hinted answers** keep the v16 rule: 6 XP, and they do not count toward mastery.

## New in v16 (2026-11-13)

From a full audit of the game. Every correction, the tests and the open questions are in `AUDIT-2026-11-13.md`.

- **Hints in two steps.** The first hint gives the idea. The second rules out one choice, shows the setup with the last number left as "?", or gives the first item in a ranking.
- **Topic mastery.** Three in a row with no hint and no miss masters a topic. Dots on the topic buttons and a count on each tile show it.
- **Second look.** A topic missed in Practice comes back about three questions later. A second miss offers the worked example.
- **XP.** A correct answer that used a hint earns 6 XP (10 without). The streak neither grows nor resets.
- **Answer checking.** Units typed after a number and superscript exponents are read. A correctly rounded answer with too few sig figs gets a nudge and is not a miss. Wrong-method values for mole fraction and Raoult's law are no longer accepted.
- **Chemistry fixes.** HCl feedback, pair-specific boiling point hints, phase-diagram points moved off the lines, urea replaced by mannitol, fatty-acid melting points matched to the CHEM 3B book, solubility limits on the colligative problems. PH₃ left "Polar or nonpolar?" and CCl₄ vs CH₃OH left "Which boils higher?".
- **Nine new questions:** ion–dipole (2), sugars (2), surface tension and viscosity (2), Energy Well (2), Electron Coin-Flip (1).
- **Decided in v17:** pentane is now 512 torr, a hinted answer stays at 6 XP, and butane stays at 273 K. Dr. Dan read and approved the new questions on 2026-11-13.

## New in v15 (2026-11-13)

- **Energy Well shows real molecules.** Dispersion is two methane molecules, dipole–dipole is two HCl molecules, the hydrogen bond is two water molecules, and ion–dipole is a sodium ion and a water molecule, with δ+ and δ− labels.
- **Light adds the energy.** A lamp beside the pair sends beams at it, and the slider is now "Shine light to add energy". The lamp stands for any way of heating: energy the pair absorbs becomes kinetic energy.
- **The pair moves.** With no light it sits still. Below the top of the well it rattles in and out while a dot rides the curve in step. Above the top the second molecule flies off, the dotted attraction fades with distance, and the label reads "pulled apart: each one still whole".
- Students who set "reduce motion" get a still picture. The caption box keeps a fixed height so the slider does not jump.

## New in v14 (2026-11-13)

- **Mixing Beaker is animated.** The particles drop into the liquid. When the forces match, solvent molecules close in around each one, then the dashed ring, the hydrogen-bond dashes and the label appear. NaCl sinks as a lattice, splits into ions, and water closes in. Gases dip in and bubble back out. Layers and solid salt settle where they belong. Loose solvent drifts the whole time.
- **Replay the drop** button under the beaker. The drop also plays again when the beaker scrolls into view, in case it started off screen.
- A Mixing Beaker question shows its own particles waiting above its own solvent while it is locked.
- Students who set "reduce motion" on their device get the still drawing and no Replay button.
- A simulation question that is replaced before the student tries it (picking another tile makes a new question) no longer uses up the "first question is a simulation" slot.
- It is still a scripted teaching animation, not a physics model.

## New in v13 (2026-11-13)

- **Mixing Beaker shows molecules.** Every particle is drawn as a small molecule with coloured atoms and a key under the beaker: bent water, methane, fluoromethane, methanol, zigzag carbon chains for hexane and pentane (H atoms left out), and Na⁺ and Cl⁻ ions.
- **Solvation is shown.** When something mixes well, each particle sits in a dashed ring with solvent molecules around it. Water's O atoms face Na⁺ and its H atoms face Cl⁻; dashed hydrogen bonds join water to methanol; hexane chains lie around methane and pentane. A gold outline marks what was dropped in, and the loose solvent is faded so the shells stand out.
- The cases that do not mix use the same molecules: gas leaving in bubbles, a floating or sunken layer, or the salt lattice on the bottom.
- It is a still drawing, not an animation. Molecules are flat and far larger than real ones.

## New in v12 (2026-11-13)

- **Simulations are shown, not hidden.** A simulation question now has its simulation right under it from the start, greyed out with "Make your prediction first". It unlocks when the student answers. Before, the simulation only appeared after the answer, so these looked like ordinary multiple-choice questions.
- **Simulation questions come up more often.** In Practice the first question is a simulation and so is at least every third one after that. A Challenge has at least 3 simulation questions out of 10 and the Daily 5 has at least 1. A student who turns the lab topics off under "Focus on specific topics" gets none.
- **Labs keep their shape on a large screen.** The H-Bond, Heating Curve and Cell labs were drawn for a box at most about 520 px wide and then stretched sideways to fill a wider one. They now scale evenly, redraw sharper at larger sizes, and stop growing at 680 px wide.
- **H-Bond Lab caption.** For the first six seconds after the model starts it says the molecules are still finding each other. Before, it said they "move too fast for hydrogen bonds to last" even when cold, because no bonds had formed yet.
- **iPhone check:** v11 and v12 were tried in iOS Safari in Apple's iPhone 17 simulator (tiles, the pinned button, hints, wrong and right answers, a lab unlocking under its question, the temperature slider). Not yet tried on a physical phone or in the Canvas Student app.

## New in v10 (2026-11-13)

- **"Go to your question" button.** After a tile is picked, the question appears below the tiles, the topic picker and the practice modes. On a phone that is more than a screen away, and inside Canvas the embedded game is about 4,000 px tall, so nothing visible changed. A button now appears right under the tiles and jumps to the question (or to the lesson in Learn). On narrow screens it stays pinned to the bottom of the screen while the tiles are in view (v11), because the tiles alone fill more than one phone screen.
- **In Canvas (Fall 2026):** the game has its own page in CHEM 1A (listed under Study Game in Chapters 10 and 11) and in both CHEM 3A sections (Chapter 6, Chapters 7 and 10: Properties of Liquids, and Chapter 7: Solids, Liquids, and Phase Changes).
- **Phone check:** done in a browser's phone emulation with real taps (tiles, hints, answers, a lab opening under its question, dragging the phase diagram point). Not yet tried on a physical phone.

## New in v9 (2026-11-12)

Four changes Dr. Dan asked for after v8 went live.

- **Molar mass beside electron count.** Wherever size decides a comparison, the game now shows and argues both: cards read "160 g/mol · 70 electrons", and the size reason reads "has a higher molar mass (more electrons), so its dispersion forces are stronger". Hints say "Similar molar mass? Compare the type of force. Same type of force? The higher molar mass wins." The Sticky Sheet's dispersion tables gained a molar mass column. One pair was removed (CH₃F vs ethane: 34 vs 30 g/mol is not "similar molar mass").
- **Lab questions in practice.** Each lab's predictions are also practice topics, marked "lab" in the topic picker. They come up in Practice, Challenge and Daily 5. After the student answers, the lab opens under the question, already unlocked on that scenario, with a "Now test it" line.
- **Fewer buttons, clearer directions.** Daily 5 moved into the mode row (Learn, Practice, Challenge, Daily 5). All nine labs and the Thermochemistry link sit in one collapsed "Labs and more" box. A collapsed "How to use this game" box has five short directions, and the mode row has a step 2 heading.
- **Hints and feedback everywhere.** Every step of every question has a hint (the test script fails if one is missing). A wrong typed answer with no recognized slip shows the step's hint. The final "correct" message repeats the explanation.

## What students see

1. Pick one or more tiles, or narrow to specific topics. A "Go to your question" button appears under the tiles.
2. Choose Learn (Professor Tips and a worked example), Practice (hints and feedback on every wrong choice), or Challenge (10 mixed questions, no hints, then a study plan). In Practice, topics a student has never seen arrive one at a time in each tile's order, and a missed topic comes back about three questions later as a "Second look".
3. Daily 5 (in the same row) gives 2 easy, 2 medium and 1 hard question and shares the ItsDrDan day streak.
4. Lab questions come up in practice: the lab shows under the question, locked, and unlocks when the student answers. Hint and Show answer sit between the question and the lab.
6. Topic buttons show three dots and each tile shows "2 of 7 topics mastered". A topic is mastered after three answers in a row with no hint and no miss.
5. Every lab can also be opened on its own from the collapsed "Labs and more" box. There it starts with a prediction, and the controls unlock after the student answers.

## Tiles and topics

| Tile | Topic | 3A | 1A | 3B |
| --- | --- | --- | --- | --- |
| Spot the Forces | Forces vs bonds | ✓ | ✓ | ✓ |
| | Polar or nonpolar? | ✓ | ✓ | |
| | Who can hydrogen bond? | ✓ | ✓ | ✓ |
| | Strongest force | ✓ | ✓ | |
| | Lewis structure → all the forces (3 steps) | ✓ | ✓ | |
| | Ion–dipole | | ✓ | |
| | Forces in organic families | | | ✓ |
| Boiling Point Battles | Which boils higher? (pick, then say why) | ✓ | ✓ | |
| | Rank three | ✓ | ✓ | |
| | Dispersion, size and shape | ✓ | ✓ | ✓ |
| | Organic boiling points | | | ✓ |
| | Fatty acids: melting points | | | ✓ |
| Liquids & Mixing | Like dissolves like | ✓ | ✓ | ✓ |
| | Surface tension & viscosity | ✓ (recognize) | ✓ (with data) | |
| | Vapor pressure | | ✓ | |
| Phase Changes | Name the phase change | ✓ | ✓ | |
| | Heat in or heat out? | ✓ | ✓ | |
| | Read a heating curve | ✓ | ✓ | |
| | Read a phase diagram | ✓ (simple) | ✓ (full) | |
| Cells & Osmosis | Osmosis basics | ✓ | ✓ | ✓ |
| | Hypotonic, isotonic, hypertonic (3 steps) | ✓ | ✓ | ✓ |
| | Osmotic pressure, Π = iMRT | | ✓ | |
| Colligative Properties | Count the particles | | ✓ | |
| | van't Hoff factor, i | | ✓ | |
| | Concentration units | | ✓ | |
| | Freezing and boiling points (5 steps, or work backward) | | ✓ | |
| | Raoult's law | | ✓ | |
| Biomolecules | Amino acid side chains | | | ✓ |
| | Protein folding | | | ✓ |
| | DNA base pairs | | | ✓ |
| | Sugars, starch and cellulose | | | ✓ |
| | Membranes, soaps and colloids | | | ✓ |

Each tile also has lab topics (v9): hydrogen bonds and the energy well in Spot the Forces, the electron coin-flip in Boiling Point Battles, the mixing beaker in Liquids & Mixing, the heating curve and phase diagram in Phase Changes, cells in a bath in Cells & Osmosis, solutions in Colligative Properties, and protein folding in Biomolecules. They follow each lab's courses.

41 topics in all, 9 of them lab topics: 21 in 3A, 32 in 1A, 18 in 3B.

## Labs

Each is labeled on screen as a teaching model, with its simplifications stated. None is molecular dynamics. Molecules never break apart in any of them.

| Lab | Courses | Spec | What it shows | Link |
| --- | --- | --- | --- | --- |
| H-Bond Lab | all | §6.1 | 4 to 26 molecules (the student chooses; 12 to start) of H₂O, NH₃, HF, CH₃OH or CH₄ with a temperature slider. Shows a crystal layer below the melting point, a level pool of liquid, and a gas above the boiling point. Dashed hydrogen bonds form H → lone pair, flicker and break. Counter of hydrogen bonds per molecule. | `?mode=lab` |
| Energy Well | 3A, 1A | §6.3 | Potential energy curve for a pair. Raise the kinetic energy above the top of the well and the pair separates. Ion–dipole well in 1A only. Relative depths, no numbers. | `?mode=well` |
| Electron Coin-Flip | 1A | §6.5 | Two atoms of He, Ne, Ar, Kr or Xe. Flip the electrons of atom 1 left or right; atom 2's cloud is pushed the same way and the two attract. Even-split chance beside each boiling point. | `?mode=coin` |
| Mixing Beaker | 3A, 1A, 3B | §6.6 (3A textbook §11.1) | Drop a substance into water or hexane. A prediction is required before every drop. | `?mode=mix` |
| Heating Curve Lab | 3A, 1A | §6.2 | Curve beside a box of 18 water molecules. Add or remove heat; the thermometer holds on each plateau while attractions break or form. | `?mode=curve` |
| Phase Diagram Explorer | 3A, 1A | §6.4 | Drag a state point on water or CO₂ (hydrazine added in 1A). Reports each change and where it happened. Sealed-tube picture in 1A. | `?mode=diagram` |
| Solutions Lab | 3A, 1A | §6.7, §6.8 (3A textbook §11.6) | Three beakers at equal molality (ethylene glycol, NaCl, K₃PO₄) that freeze as you cool them; and (1A only) a Raoult's-law mixer for two volatile liquids. In 3A the Experiment tabs and Raoult's-law predictions are hidden, so it is the freezing-point model only. | `?mode=solutions` |
| Cell Lab | all | §6.9 | Red blood cell or plant cell in six baths, with water-in and water-out counts. Π = iMRT line and the osmosis chamber picture in 1A only. | `?mode=cell` |
| Protein Fold Lab | 3B | §2 (3B examples) | A made-up chain of 12 amino acids. Heating breaks the attractions; the peptide and disulfide bonds stay. | `?mode=fold` |

## Conventions to know

- **Feedback:** every wrong choice has its own explanation and a named slip. Every correct answer shows its explanation too.
- **Hints:** every step has one. Most have a second: it rules out one wrong choice and says why, shows the setup with the last number left as "?", or gives the first item of a ranking. Using any hint marks the answer as helped.
- **Mastery:** each topic keeps its last six results (on your own, with a hint, or missed). Three in a row on your own is "mastered". It is a count, not an estimate, and a later miss removes it. After a week with no unaided answer the topic asks for one more (yellow dots).
- **Second look:** a topic missed in Practice returns about three questions later. At most one question in three is a second look, and at most three topics wait. After a second miss a "See a worked example" button opens Learn on that topic.
- **Tap all that apply:** every right choice must be tapped and no wrong one. The question bank does not sample these (it takes single-answer and typed-number steps only).
- **Multi-step questions:** a question counts as correct only when every step is right on the first try. In Challenge a missed step shows the student's answer, the reason and the correct answer.
- **Typed numbers:** accepted within 1% of the unrounded answer, so rounding in earlier steps is not punished. E notation (`7.84E0`), `×10^` and superscripts (`×10³`) are accepted, and a unit typed after the number is ignored. A decimal comma gets a "use a period" message. Where a dilute solution puts a wrong-method value inside the 1% window (mole fraction, Raoult's law), that value is rejected. A ± key sits beside boxes that can take a negative answer.
- **Sig figs:** a numerically correct answer with the wrong number of sig figs is marked correct with a yellow "Close, but fix your sig figs" notice. Trailing zeros with no decimal point do not count (100 has 1 sig fig; `100.` has 3), so the game displays such answers as `100.`. An answer that is a correct rounding to too few sig figs (12 for 11.5) gets a nudge and is not a miss.
- **XP:** 10 for a question with no misses and no hint, plus 2 per streak step (up to +10). 6 for a correct answer that used a hint; the streak neither grows nor resets. 2 for a question finished after a miss or a reveal. Lab predictions score the same way.
- **Computed answers:** forces, electron counts, "which is higher", phase at a point, the change where an arrow crosses a line, and all numeric keys are computed from the data tables, not typed in.
- **Stats:** one anonymous row per question to the Game Stats sheet (game id `imf`), with the name of the first slip. No names, IDs or typed answers.

## Sources and values

- **OpenStax Chemistry 2e, checked on openstax.org 2026-11-12:**
  - §10.1: halogen boiling points (Table 10.1), pentane isomers 36, 27 and 9.5 °C, HCl 188 K vs F₂ 85 K, Example 10.3 (propane −42.1, dimethyl ether −24.8, ethanol 78.5 °C), ethane −89 °C and methylamine −6 °C.
  - §10.2: viscosities and surface tensions at 25 °C (Tables 10.2 and 10.3).
  - §10.4: water triple point 0.01 °C and 0.6 kPa, critical point 374 °C and 218 atm. OpenStax prints CO₂'s critical point as 31.1 °C and 7400 kPa; the game uses the handbook 31.0 °C and 72.9 atm. The phase-diagram model gives the stated phase for all 13 state points in the text and Examples 10.11 and 10.12.
- **From the spec's tables (Lecture 28, Worksheet 12, MyOpenMath):** noble gas and hydrocarbon boiling points, water ΔH<sub>fus</sub> 6.02 and ΔH<sub>vap</sub> 40.70 kJ/mol, specific heats 2.06, 4.184 and 2.02 J/(g·°C), K<sub>f</sub> 1.86 and K<sub>b</sub> 0.512, hydrazine phase points, alcohol vapor pressures, water vapor pressure table, and the corrected 13.2% even-split value for 36 electrons.
- **Heating curve:** the Lecture 28 example, 15.0 g of ice at −20.0 °C to steam at 145.0 °C. The five steps come to 0.62, 5.01, 6.28, 33.9 and 1.36 kJ, total 47.2 kJ.
- **Handbook values (v17):** pentane 512 torr at 25 °C, chlorine −34 °C (OpenStax Table 10.1 prints 238 K; the game shows 239 K), CO₂ critical point 31.0 °C and 72.9 atm.
- **Amino acid classes:** copied from Peptide Party (`ItsDrDan/aminoacids`). Cysteine is polar neutral.

### Values that still need Dr. Dan's review

These are standard values recalled from memory, not copied from a course source.

- **Boiling points not printed in OpenStax §10.1**, rounded to whole °C. Examples: octane 126, propylamine 48, acetone 56, propanal 48, 1-propanol 97, acetic acid 118, acetamide 221, CCl₄ 77, CBr₄ 190, HF 20, NH₃ −33.
- **Fatty acid melting points:** lauric 44, myristic 54, palmitic 63, stearic 69, palmitoleic 0.5, oleic 13, linoleic −5, linolenic −11, arachidonic −49 °C. Palmitoleic, oleic and arachidonic were changed in v16 to match the 3B textbook.
- **CO₂:** triple point −56.6 °C and 5.11 atm, sublimation at −78.5 °C. OpenStax §10.4 does not print these.
- **Solid–liquid slopes:** water −0.0075 °C per atm, CO₂ +0.018 °C per atm. Hydrazine's is unknown and drawn nearly vertical, with an on-screen note.
- **Vapor pressures for Raoult's law:** benzene 95.1 and toluene 28.4 torr at 25 °C; heptane 92.0 and octane 31.0 torr at 40 °C. Pentane 512 and hexane 151 torr at 25 °C (v17; the 425 torr used before is the value near 20 °C).
- **Seawater:** about 1.1 mol of dissolved particles per liter (about 28 atm at 37 °C), shown as "about".
- **Mercury's surface tension** is explained by metallic bonding.
- **Butane** is shown as 273 K (−0.5 °C) in the hydrocarbon series.
- **Mannitol** replaced urea in the osmotic pressure questions, because urea crosses the red-cell membrane.
- **Questions added in v16 and v17, written from general knowledge. Dr. Dan read all 27 on 2026-11-13 and approved them as written** (full text in `REVIEW-NEW-QUESTIONS.md`):
  - Ion–dipole: Na⁺ vs Mg²⁺; which pair is ion–dipole.
  - Sugars: what holds a sucrose crystal together; why cotton soaks up water.
  - Surface tension and viscosity: water beading on a waxed car; motor oil vs gasoline (about 5 to 12 carbons vs 20 or more).
  - Osmosis: 0.10 M vs 0.30 M glucose across a membrane; sugar on strawberries; potato in salt water.
  - Protein folding: the peptide bond; permanent waves and disulfide bonds; hydrogen bonds in a β-pleated sheet.
  - Membranes and colloids: where the tails are in a micelle; why mayonnaise stays mixed (lecithin); the surface of a lipoprotein.
  - Dispersion: where dispersion forces come from; which substances have them; hexane 69 °C vs 2,2-dimethylbutane 50 °C.
  - Fatty acids: arachidonic (20:4, −49 °C) vs stearic (18:0, 69 °C).
  - Lab predictions: Energy Well (lowest energy at the bottom of the well; cooling a separated pair), Electron Coin-Flip (neon about 25% vs argon about 19% even splits), Heating Curve (freezing releases heat; a hotter burner does not raise the boiling temperature), Phase Diagram (gas in the lower right; water boils near 120 °C at 2 atm), Protein Fold (no peptide bond breaks).

## Differences from the spec

- **Heating curve is drawn not to scale**, and says so. True to scale, warming the ice is about 1% of the width. A "Where the 47.2 kJ goes" table carries the real proportions.
- **Ice is one flat slice of the lattice.** Each molecule shows 3 hydrogen bonds; the fourth is drawn as an H pointing toward the viewer, with a note.
- **Phase diagrams use a log pressure axis** so the triple and critical points fit on one diagram. Water's leftward lean is real-scale and too slight to see; the "squeeze ice at −3 °C" prediction demonstrates it (it melts at about 401 atm).
- **Mixing Beaker, hexane column:** pentane and water replace CH₃F and hexane, because fluoromethane's solubility in hexane could not be verified. The water column has the spec's five.
- **Two extra IV fluids:** 5% glucose (isotonic) and 0.45% NaCl (hypotonic) were added to the spec's four baths.
- **Osmosis chamber** is a static picture in 1A, not an interactive piston.
- **Polar side chains:** the spec lists dipole–dipole as its own rule. The game uses Peptide Party's four interactions, and every polar pair asked about has O–H or N–H, so the answer is hydrogen bond.
- **Standalone labs have no Hint button** on their prediction step. The same predictions asked in practice do.
- **Reduce-motion checkbox** exists in the H-Bond Lab and Cell Lab. The Heating Curve Lab and Phase Diagram Explorer follow the device's reduced-motion setting only. The other labs have no continuous animation.
- **Heating-curve calculations** are not rebuilt here. The game links to the Thermochemistry game, as the spec asks.
- **The spec's two optional art touch-ups** (Critical Thinker meniscus, Surface Skater legs) are not done.

## Slips logged to Game Stats (game id `imf`)

Names from the spec's §5 table that the game uses:
`boil-breaks-bonds`, `hbond-is-covalent`, `any-h-hbonds`, `polar-bonds-polar-molecule`, `type-always-wins`, `size-ignores-type`, `vp-backwards`, `plateau-heats-up`, `endo-exo-swap`, `more-pressure-always-liquefies`, `triple-critical-swap`, `molarity-for-molality`, `forgot-i`, `i-for-molecular`, `fp-sign`, `raoult-solute-fraction`, `celsius-in-gas-law`, `tonicity-swap`.

Added in v16: `wrong-temperature` and `units` (osmotic pressure), and `polarity` now has its own feedback line. A sig-fig nudge is not logged, because it is not a miss.

`kj-vs-j` from the spec is not used, because heating-curve calculations live in the Thermochemistry game.

Added by the game:

- **Forces:** `missed-dipole`, `missed-hbond`, `forgot-dispersion`, `no-ions`, `polarity`, `dispersion-size`, `hbond-needs-lone-pair`, `hbond-h-to-h`, `heat-makes-bonds`, `well-depth`, `coin-flip`.
- **Properties and mixing:** `like-dissolves-like`, `weak-vs-strong`, `kinks-pack-poorly`, `chain-length`, `rank-order`, `rank-reversed`.
- **Phase changes:** `phase-name`, `phase-reverse`, `curve-reading`, `fus-vs-vap`, `pd-region`, `pd-crossing`, `ice-density`.
- **Osmosis:** `tonicity-class`, `osmosis-solute-moves`, `osmosis-static`, `plant-bursts`.
- **Colligative:** `ion-count`, `ion-pairing`, `identity-not-count`, `bp-sign`, `delta-not-point`, `wrong-constant`, `g-vs-kg`, `percent-solvent`, `mole-ratio`, `raoult-setup`, `raoult-swapped`, `vapor-composition`.
- **Biomolecules:** `disulfide-is-covalent`, `secondary-vs-tertiary`, `side-chain-hb`, `side-chain-salt`, `side-chain-hyd`, `dna-hb-count`, `colloid-vs-solution`.
- **General:** `concept`, and `gave-up` when a student uses Show answer.

## Achievements

21 in all, shown by course. The 15 game badges use the art in `assets/badges/`; six general ones use brand-kit badges.

| Badge | Earned by | Courses |
| --- | --- | --- |
| First Stick | First correct answer | all |
| Dispersion Detective | 8 right in Rank three, Dispersion or Fatty acids | all |
| Dipole Duo | 6 polarity questions right | 3A, 1A |
| H-Bond Hero | 6 "Who can hydrogen bond?" right | all |
| Ion Hugger | 5 right in Like dissolves like or Ion–dipole | all |
| Boiling Point Boss | 10 boiling point battles won | all |
| Vapor Escape | 5 vapor pressure questions right | 1A |
| Surface Skater | 5 surface tension and viscosity questions right | 3A, 1A |
| Phase Shifter | 8 Phase Changes questions right | 3A, 1A |
| Critical Thinker | 6 phase diagram questions right | 3A, 1A |
| Cell Saver | 8 Cells & Osmosis questions right | all |
| Salt the Roads | 5 freezing and boiling point problems right | 1A |
| Particle Counter | 8 right in Count the particles or van't Hoff factor | 1A |
| Fat Packer | 6 fatty acid questions right | 3B |
| Protein Folder | 8 right in Amino acid side chains or Protein folding | 3B |
| Lab Partner | 5 correct lab predictions | all |
| Challenge Champion, Daily Habit, On a Roll, Unbreakable, Explorer | Challenge score, Daily 5 streak, answer streaks, trying every mode | all |

## How it was tested

- **v16 and v17:** the scripts in `tools/` are the current checks (20,700 questions, typed-number cases, phase-diagram points, and 20,000 numeric answers recomputed from the printed numbers); both pass with 0 failures. See `AUDIT-2026-11-13.md`.
- **Answer keys (v15 and earlier):** a script generated 400 questions for every topic in every course (27,600 in all) and checks one correct choice per step, a hint on every step, a reason and slip on every wrong choice, and that every displayed numeric answer passes its own check and sig-fig rule.
- **Data checks:** every boiling-point pair is in the stated order with the stated reason, and every size comparison has molar mass and electron count agreeing; every Lewis drawing has the right electron count and matches its formula; every molar mass matches the atomic masses; the spec's hand-worked numbers (KBr, glucose, ethylene glycol, pentane and hexane) are reproduced.
- **Models:** the H-bond model ranks water > methanol > HF > NH₃ > CH₄ = 0 from −33 °C up; the heating-curve box returns all 18 molecules to the lattice after a full heat-and-cool cycle; all twelve cell-and-bath combinations end in the right state.
- **Browser:** every topic, Learn, Challenge, Daily 5 and every lab clicked through at desktop and phone width in all three courses, with no console errors, no sideways scrolling and no undersized buttons.

## Known limits

- **Animations were not watched in real time.** The test browser throttled animation, so the models were stepped by script. Playback speed and smoothness on real devices are unverified.
- **Small text on phones** in the phase diagram and the Protein Fold Lab picture.
- **H-Bond Lab crystals are simplified.** Each solid is one flat layer drawn so the hydrogen bonds are easy to see, not the real crystal structure, and with only 8 to 12 molecules the edge molecules have fewer bonds (frozen water averages about 2.2 per molecule though a middle molecule has 4). The gas is drawn with no hydrogen bonds at all.
- **No matched videos for the 3B biomolecule topics;** they fall back to the general intermolecular forces video.
- **The CHEM 3B Exam #3 Reference Sheet was not available** when the 3B questions were written. Examples follow the spec's description of it.

## Not done yet

- Confirm the nightly question-bank build keeps working with `tools/samplers/IMF.js` (added 2026-11-12 in `ItsDrDan/questionbank`), which lets the hub's Daily 5 draw from this game.
