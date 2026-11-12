# 01 — Next bounce point

Ellipse C: x²/a² + y²/b² = 1. Example: a² = 4, b² = 2 (2025 National Paper II, Q16).

## Example

P = (√2, 1) is on C: 2/4 + 1/2 = 1.

Ball leaves P with direction d = (−1, −1), position (√2 − t, 1 − t).
Substituting into C:

    (3/4)t² − (1 + √2/2)t = 0

The constant term is 0 because P is on C, so t = 0 is always a root.
By Vieta, the other root is t₂ = −B/A = (4 + 2√2)/3 ≈ 2.276, so

    Q = ((√2 − 4)/3, −(1 + 2√2)/3) ≈ (−0.862, −1.276)

Check: x²/4 + y²/2 = (18 − 8√2)/36 + (18 + 8√2)/36 = 1.

## General formula

P = (x₀, y₀) on C, direction d = (p, q). Substitute (x₀ + pt, y₀ + qt):

    A = p²/a² + q²/b²
    B = 2(x₀p/a² + y₀q/b²)
    C = x₀²/a² + y₀²/b² − 1 = 0

    t = −2(x₀p/a² + y₀q/b²) / (p²/a² + q²/b²)

Note: n = (x₀/a², y₀/b²) is a normal vector to C at P, so B = 2(d·n).
The same n is used for the reflection in step 2.

## Open checks (to answer myself)

1. What happens if d·n = 0? What is t, and what does it mean geometrically?
2. Can A = 0? (The code divides by A.)
3. Redo the general formula on a blank page without looking.
