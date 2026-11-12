# 03 — The conserved quantity d₁d₂

## Gaokao 二级结论: d₁d₂ = b² for a tangent line

For the ellipse x²/a² + y²/b² = 1 with foci F₁(−c, 0), F₂(c, 0), let d₁, d₂ be the
distances from F₁, F₂ to any tangent line. Then **d₁d₂ = b²**.

**Proof.** The tangent at (x₀, y₀) is x₀x/a² + y₀y/b² = 1 (another 二级结论).
Using the point-to-line distance formula,

    d₁d₂ = |−cx₀/a² − 1| · |cx₀/a² − 1| / (x₀²/a⁴ + y₀²/b⁴)
         = (1 − c²x₀²/a⁴) / (x₀²/a⁴ + y₀²/b⁴).

Substitute y₀² = b²(1 − x₀²/a²) into the denominator:

    x₀²/a⁴ + 1/b² − x₀²/(a²b²) = 1/b² − x₀²(a² − b²)/(a⁴b²)
                               = (1/b²)(1 − c²x₀²/a⁴).

So d₁d₂ = b². ∎

## Why this is conserved in the billiard

By the caustic theorem (note 02), every segment is tangent to the same confocal
ellipse x²/a′² + y²/b′² = 1 with the same foci F₁, F₂. Apply the 二级结论 to *that*
ellipse: for every segment,

    d₁d₂ = b′² = a′² − c².

That is the same number for every segment. **d₁d₂ is a conserved quantity of the
motion**, and its value tells you which caustic the orbit has.

## Signed version (covers the hyperbola case too)

Write the confocal family as

    x²/(a² − λ) + y²/(b² − λ) = 1.

For 0 < λ < b² this is an ellipse, and for b² < λ < a² it is a hyperbola. Use
*signed* distances (positive on one side of the line, negative on the other).
Then for every segment

    d₁d₂ = b² − λ.

It is positive when the foci are on the same side (ellipse caustic) and negative
when the segment passes between them (hyperbola caustic). The simulator checks
this numerically for both cases, and also checks directly that each segment is
tangent to the conic with λ = b² − d₁d₂.

Example: the warm-up orbit from (√2, 1) in direction (−1, −1) crosses the
x-axis at x = √2 − 1, between the foci (±√2), so its caustic is a hyperbola.
The simulator gives d₁d₂ = 1/2 − √2 ≈ −0.914 on every segment.

## Still to do myself

- [ ] Prove the hyperbola version of the 二级结论 (signed product = −b″²
      for a hyperbola x²/a″² − y²/b″² = 1).
- [ ] Derive d₁d₂ = b² − λ from the two 二级结论 above.
