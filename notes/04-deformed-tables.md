# 04 · Breaking the ellipse

> **Gaokao starting point.** Deform the equation of 2025 National Paper II Q16
> itself. With $u = x^2/4$ and $v = y^2/2$, the ellipse is $u + v = 1$. Add one
> term:
>
> ```math
> \mathcal T_\varepsilon:\quad u + v + \varepsilon\,uv = 1 .
> ```

## 1. The family of tables

- $\varepsilon = 0$ is the ellipse. As $\varepsilon \to -1$ the equation becomes
  $(1-u)(1-v) = 0$, the **rectangle** $|x| \le 2,\ |y| \le \sqrt2$. Both ends
  are integrable billiards.
- Every table passes through the four vertices $(\pm2, 0), (0, \pm\sqrt2)$.
- **Convexity (proved).** In the scaled coordinates $X = x/a,\ Y = y/b$, the
  curvature of $X^2 + Y^2 + \varepsilon X^2Y^2 = 1$ has the sign of
  $1 - 3\varepsilon X^2Y^2$ (implicit-curve curvature formula, then substitute
  $X^2 + Y^2 = 1 - \varepsilon X^2Y^2$). For $\varepsilon \le 0$ this is
  positive. For $\varepsilon > 0$, **AM–GM** (the gaokao bound on $xy$ given
  $x + y$) gives $4X^2Y^2 \le (X^2 + Y^2)^2 = (1 - \varepsilon X^2Y^2)^2$, with
  equality on the diagonals. With $q = \varepsilon X^2Y^2$ this says
  $\varepsilon \le 4q/(1-q)^2$, an increasing function equal to $3$ at
  $q = 1/3$. So $q < 1/3$ everywhere when $\varepsilon < 3$: the table is
  **strictly convex exactly for $-1 < \varepsilon < 3$**, and at $\varepsilon = 3$
  the curvature vanishes at $X = \pm Y = \pm1/\sqrt3$.

## 2. The next bounce: Vieta becomes a cubic

Substitute $P + t\mathbf d$ into $u + v + \varepsilon uv = 1$. Now $u(t)$ and
$v(t)$ are quadratics in $t$, so we get a **quartic**. Since $P$ is on the wall,
$t = 0$ is still a root, and dividing by $t$ leaves a **cubic**

```math
c_3t^3 + c_2t^2 + c_1t + c_0 = 0, \qquad c_3 = \varepsilon u_2v_2,\ \dots
```

At $\varepsilon = 0$ we get $c_3 = c_2 = 0$, and the cubic collapses to the linear
equation $t = -c_0/c_1$: exactly Proposition 1 of note 01. For
$\varepsilon \ne 0$, the next bounce is the smallest positive real root, found
from the companion matrix and polished by Newton's method (`deformed.py`).

## 3. Exact result: when the axis orbits are stable

The ball can bounce back and forth along the major axis (length $L = 2a$) or
the minor axis ($L = 2b$). For a 2-periodic orbit hitting the wall
perpendicularly at two points with radius of curvature $R$, the linearized
two-bounce map has trace

```math
\operatorname{tr} M = 2\bigl(2(1 - L/R)^2 - 1\bigr),
```

so the orbit is stable (elliptic) iff $|\operatorname{tr} M| < 2$, i.e.
$0 < (1 - L/R)^2 < 1$.

*Derivation (mirror matrices).* Track a nearby ray by its offset $y$ and small
angle $\theta$. A flight of length $L$ is $\begin{pmatrix}1&L\\0&1\end{pmatrix}$.
Near a vertex the wall is $x = x_0 - y^2/(2R)$, so the normal tilts by $y/R$
and the ray turns by $2y/R$: $\begin{pmatrix}1&0\\-2/R&1\end{pmatrix}$. Their
product $N$ has $\det N = 1$ and $\operatorname{tr} N = 2(1 - L/R) = 2g$, and
$M = N^2$, so $\operatorname{tr} M = (\operatorname{tr} N)^2 - 2 = 4g^2 - 2$.
Stability means the eigenvalue equation $\mu^2 - (\operatorname{tr} M)\mu + 1 = 0$
has complex roots: discriminant $(\operatorname{tr} M)^2 - 4 < 0$, exactly as
for a gaokao quadratic. This is the same criterion as for a laser cavity.

**Radii of curvature at the vertices.** Near $(a, 0)$, solve for $u$:
$u = (1-v)/(1+\varepsilon v) \approx 1 - (1+\varepsilon)v$. So
$x \approx a - \frac{a(1+\varepsilon)}{2b^2}y^2$ and $R = \dfrac{b^2}{a(1+\varepsilon)}$.
In the same way, $R = \dfrac{a^2}{b(1+\varepsilon)}$ at $(0, b)$.

**Theorem (axis orbits of $\mathcal T_\varepsilon$, $a^2 = 4,\ b^2 = 2$).**

```math
\operatorname{tr} M_{\text{major}} = 2\bigl(2(3 + 4\varepsilon)^2 - 1\bigr), \qquad
\operatorname{tr} M_{\text{minor}} = 2\bigl(2\varepsilon^2 - 1\bigr).
```

- The **major-axis orbit** is unstable for the ellipse ($\operatorname{tr} = 34$)
  and becomes **stable for $\varepsilon < -\tfrac12$**.
- The **minor-axis orbit** is stable for $0 < |\varepsilon| < 1$ and becomes
  **unstable for $\varepsilon > 1$**.
- **At $\varepsilon = 0$, $\operatorname{tr} M_{\text{minor}} = -2$ exactly.**
  This is a coincidence of the gaokao ellipse: $a^2 = 2b^2$ (eccentricity
  $\sqrt2/2$) means the centre of curvature at $(0, b)$ is the opposite
  vertex $(0, -b)$, so $L = R$.

The numerical Jacobian matches both formulas to four decimals for 11 values of
$\varepsilon$ (`verify.py`).

## 4. Numerical experiments

See `research.py`. For each $\varepsilon$, 3000 orbits are sampled uniformly for
the invariant measure $ds\,dp$, and each is run for 3000 bounces. An orbit is
called chaotic if its finite-time Lyapunov exponent exceeds 0.05. The
exponents fall into two clear groups (< 0.01 and > 0.1), so this threshold
sits in the gap between them.

**Results** (`results/summary.csv`):

| $\varepsilon$ | −0.9 | −0.5 | −0.1 | −0.01 | 0 | 0.01 | 0.1 | 1 | 1.2 | 1.4 | 1.5 | 2.9 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chaotic fraction | 0.82 | 0.81 | 0.41 | 0.049 | 0 | 0.047 | 0.35 | 0.74 | 0.87 | 0.95 | 0.97 | 0.99 |

- Chaos appears for every $\varepsilon \ne 0$, first as a thin layer around the
  orbits through a focus (the red separatrix of note 03's phase portrait).
- For $|\varepsilon| \le 0.03$: chaotic fraction $\approx 4.8\,|\varepsilon|^{0.98}$,
  and the range of $d_1d_2$ on regular orbits is $\approx 1.8\,|\varepsilon|^{1.00}$.
  So $d_1d_2$ breaks **linearly**: it becomes an approximate invariant.
- For $\varepsilon \le -\tfrac12$ (major-axis orbit stable) the fraction levels
  off at about 0.82. For $\varepsilon > 1$ (minor-axis orbit unstable) its growth
  steepens (0.74, 0.82, 0.87, 0.90, 0.95 at $\varepsilon = 1.0, \dots, 1.4$) and
  reaches 0.97 by $\varepsilon = 1.5$.

## Prior work (literature search, 2026-11-16)

- Delshams & Ramírez-Ros, *Nonlinearity* 9 (1996): Melnikov method for planar
  maps; symmetric entire perturbations of the ellipse are **not integrable**
  (the separatrices split). This supports what we see numerically.
- Bishop, Chenoweth, Fleurantin, Sander & Mireles James, arXiv:2602.15272
  (2026): stable/unstable manifolds in perturbed elliptical tables.
- González-Andrade et al., *Phys. Rev. E* 112 (2025): soft squircle billiard,
  a superellipse-type circle-to-square interpolation.
- No paper found with the family $u + v + \varepsilon uv = 1$ or with a
  scaling law for the chaotic fraction. The search was limited (a few web
  searches, abstracts only).

## To do myself

- [x] Derive the trace formula for 2-periodic orbits (done above).
- [x] Prove the convexity threshold $\varepsilon^\ast = 3$ completely (done above).
- [ ] Read the three papers above (at least introductions) and confirm the
      family is new.
- [ ] Re-derive both proofs above by hand.
