# Elliptic Billiards

A ball bouncing inside an ellipse never wanders freely: every segment of its
path stays tangent to the same confocal conic (the *caustic*). This project
proves that fact, checks it numerically with a simulator written from scratch,
and then asks what happens when the table is **no longer an ellipse**: how
quickly does the hidden order break down into chaos?

The starting point is a high-school problem: the ellipse x²/4 + y²/2 = 1 from
2025 Gaokao National Paper II, Q16.

## Research question

Deform the ellipse (superellipse |x/a|^p + |y/b|^p = 1, stadium, ...). How fast
does the quantity conserved in the elliptic case (d₁d₂, the product of the
focal distances to each segment) stop being conserved, and how does this
relate to Poincaré sections and Lyapunov exponents?

Related open problem: the **Birkhoff conjecture** (roughly: the ellipse is the
only integrable convex billiard table).

## Roadmap

- [x] Warm-up: next bounce point via Vieta's formulas ([notes/01-next-bounce.md](notes/01-next-bounce.md))
- [ ] Step 0: GeoGebra exploration, conjecture the caustic
- [ ] Step 1: prove the caustic theorem (optical property, reflection trick, congruent triangles)
- [ ] Step 2: Python simulator (next bounce, normal, reflection d' = d − 2(d·n)n)
- [ ] Step 3: verify d₁d₂ conservation, Poncelet porism, equal perimeters of periodic orbits
- [ ] Step 4: deformed tables and the onset of chaos

## Layout

- `notes/` — derivations and proofs
- `LOG.md` — work log, including what was done with tutor help
