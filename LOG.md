# Work log

An honest record of what I did myself and what I got help with.

## 2026-10-28 — Warm-up: next bounce point

- Exercise set by my AI tutor (Claude): find the next bounce point on
  x²/4 + y²/2 = 1 from P = (√2, 1) in direction (−1, −1), then the general formula.
- Parts (1)–(4) were written out by the tutor at my request (I was away from my
  desk). Still to do on my own: the open checks in `notes/01-next-bounce.md`,
  and re-deriving the general formula without notes.

## 2026-11-12 — Repository set up

- Created this repo (README, notes, log) with the tutor's help.
  At this point the plan was that I'd write all simulation code myself.
- Changed plan the same day: I asked the tutor to draft everything it could
  and I'd revise it myself. Drafted by Claude: the answers to the checks in
  note 01, notes 02 (caustic proof) and 03 (d₁d₂), `billiards.py`, `verify.py`
  and the figures. Not yet reviewed by me. The "Still to do myself" lists in
  each note, step 0 (GeoGebra) and step 4 (deformed tables) are mine.

## 2026-11-12 — Polishing to paper quality

- I asked the tutor to make the project polished and publication-ready.
  Drafted by Claude: rigorous rewrite of notes 01–03 (new Lemmas 2 and 3 close
  gaps in the caustic proof), `figures.py` and all figures, pass/fail
  `verify.py`, and the LaTeX draft `paper/` (background and method only).
- Still mine: the hyperbola case and the signed d₁d₂ derivation, step 0, and
  all of step 4 (the paper's results section), which is the original
  contribution. Every reference in `paper/refs.bib` must be checked against
  the source before submission.

## 2026-11-15 — Section 4 and the full paper

- I asked Claude to keep going and produce the full paper PDF. Drafted by
  Claude: the hyperbola case of the caustic theorem, the one-line proof of
  d₁d₂ = b² − λ, the deformation family u + v + εuv = 1 (Claude's idea), the
  axis-orbit stability theorem, `deformed.py`, `research.py`, the sweep and
  its figures, note 04, Section 4, the discussion, the abstract and the AI
  disclosure in `paper/`. `verify.py` now has 29 checks.
- Still mine: the literature search on this family, checking every reference,
  the "To do myself" items in notes 02 and 04, and being able to explain and
  re-derive every result before showing the paper to anyone.

## 2026-11-16 — Closing the TODOs

- I asked Claude to finish the remaining TODOs. Drafted by Claude: a complete
  proof that the tables are convex exactly for −1 < ε < 3 (curvature has the
  sign of 1 − 3εX²Y², then AM–GM), a derivation of the 2-periodic trace
  formula with mirror matrices (Lemma in Section 4), a first literature search
  (three related papers added to `refs.bib`; no prior study of this family
  found), and a check of the reference list. `verify.py` now has 30 checks.
- Still mine: reading the related papers to confirm the family is new,
  re-deriving both new proofs, and checking the AI statement against the
  target journal's policy.

## 2026-11-16 (later) — Follow-up experiments

- I asked Claude to keep improving the project, which is my primary
  independent project. Drafted by Claude: Theorem 12 for every aspect ratio
  and the 1:4 resonance remark ($M = -I$ for the gaokao ellipse),
  `extensions.py` (robustness, aspect ratio, rectangle limit), the new
  figure, Section 4.4 of the paper, and `STUDY-GUIDE.md`. `verify.py` now has
  31 checks.
- Still mine: everything in `STUDY-GUIDE.md`, and one next step that I do
  myself without AI drafting.
