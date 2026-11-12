# 02 — The caustic theorem

Ellipse C with foci F₁, F₂ and major axis 2a. A ball moves inside C, reflecting
off the wall (angle of incidence = angle of reflection).

**Theorem.** If one segment of the path does not cross the focal segment F₁F₂,
then every segment is tangent to the same ellipse with foci F₁, F₂ (a
*confocal* ellipse, the **caustic**). If one segment crosses F₁F₂ between the
foci, every segment is tangent to the same confocal hyperbola.

This note proves the ellipse case using only gaokao tools.

---

## Tool 1 — Optical property (光学性质)

At any point B on C, the tangent line makes equal angles with BF₁ and BF₂.
Equivalently, the normal at B bisects ∠F₁BF₂.

**Gaokao example: 2010 Anhui Q19** (文/理 paper not confirmed). The ellipse
through A(2, 3) with foci on the x-axis and e = 1/2 is x²/16 + y²/12 = 1, with
F₁ = (−2, 0), F₂ = (2, 0). The problem asks for the bisector of ∠F₁AF₂, and the
answer is 2x − y − 1 = 0.

Check that this is the normal: the normal direction at A is
(x₀/a², y₀/b²) = (2/16, 3/12) = (1/8, 1/4) ∝ (1, 2), and the line through (2, 3)
with direction (1, 2) is y − 3 = 2(x − 2), i.e. 2x − y − 1 = 0. ✓

So light from F₁ reflects off the wall straight to F₂. For billiards, it means
the reflection at B, which swaps the incoming and outgoing directions, also
swaps the directions BF₁ and BF₂.

## Tool 2 — 将军饮马 and tangency

**Lemma.** Let ℓ be a line with F₁, F₂ on the same side. Reflect F₁ across ℓ to
F₁′. Then for every point P on ℓ,

    PF₁ + PF₂ = PF₁′ + PF₂ ≥ F₁′F₂,

with equality exactly at P₀ = F₁′F₂ ∩ ℓ (将军饮马). Hence the ellipse with foci
F₁, F₂ and major axis **2a′ = F₁′F₂** touches ℓ at P₀ and nowhere else. Every
other point of ℓ has PF₁ + PF₂ > 2a′, so it lies outside that ellipse. So ℓ is
tangent to it.

In words: **the confocal ellipse tangent to ℓ has major axis F₁′F₂.**

## Proof of the theorem (ellipse case)

Take two consecutive segments AB and BC, bouncing at B. Suppose line AB does
not separate F₁, F₂. (Then BC doesn't either; one can show this, or see it in
the simulation.)

- Reflect F₁ across line AB to get F₁′. By Tool 2, the confocal ellipse tangent
  to AB has 2a′ = F₁′F₂.
- Reflect F₂ across line BC to get F₂′. By Tool 2, the confocal ellipse tangent
  to BC has 2a″ = F₁F₂′.

We show F₁′F₂ = F₁F₂′ using triangles F₁′BF₂ and F₁BF₂′.

1. **BF₁′ = BF₁** (reflection across AB keeps distances to points on AB).
2. **BF₂ = BF₂′** (reflection across BC).
3. **∠F₁′BF₂ = ∠F₁BF₂′.** The reflection gives ∠F₁′BA = ∠ABF₁, so

       ∠F₁′BF₂ = ∠ABF₁ + ∠ABF₂.

   In the same way, ∠CBF₂′ = ∠CBF₂, so

       ∠F₁BF₂′ = ∠CBF₁ + ∠CBF₂.

   The normal at B is a mirror line that swaps ray BA ↔ ray BC (billiard
   reflection) and ray BF₁ ↔ ray BF₂ (Tool 1). Mirrors keep angles, so
   ∠ABF₁ = ∠CBF₂ and ∠ABF₂ = ∠CBF₁. The two sums are equal.

By SAS, △F₁′BF₂ ≅ △F₁BF₂′, so **F₁′F₂ = F₁F₂′**, i.e. 2a′ = 2a″.

So AB and BC are tangent to the same confocal ellipse. Repeat at every bounce,
and every segment is tangent to it. ∎

## Still to do myself

- [ ] Draw the figure for the proof, either by hand or in GeoGebra.
- [ ] Check the angle step in step 3 carefully for a picture where F₁ is
      inside ∠ABC and for one where it isn't. Does the argument still hold?
- [ ] Hyperbola case: if AB crosses F₁F₂, F₁ and F₂ are on opposite sides of
      AB. Redo Tool 2 with |PF₁ − PF₂| in place of PF₁ + PF₂.
- [ ] Why can't a segment "switch" from the ellipse case to the hyperbola case?
