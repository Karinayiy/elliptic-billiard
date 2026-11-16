# 03 · The conserved quantity $d_1 d_2$

> **Gaokao starting point.** Two standard 二级结论 for $x^2/a^2 + y^2/b^2 = 1$:
> the tangent at $(x_0, y_0)$ is $x_0x/a^2 + y_0y/b^2 = 1$, and the distances
> $d_1, d_2$ from the foci to any tangent line satisfy $d_1 d_2 = b^2$.

Foci: $F_{1,2} = (\mp c, 0)$ with $c^2 = a^2 - b^2$.

## 1. The 二级结论 $d_1 d_2 = b^2$

**Lemma 1.** For every tangent line of $C$, $d_1 d_2 = b^2$.

*Proof.* At the point of tangency $(x_0, y_0)$, the tangent line is
$\frac{x_0}{a^2}x + \frac{y_0}{b^2}y - 1 = 0$. By the point-to-line distance formula,

```math
d_1 d_2
= \frac{\left|-\frac{c x_0}{a^2} - 1\right|\cdot\left|\frac{c x_0}{a^2} - 1\right|}
       {\frac{x_0^2}{a^4} + \frac{y_0^2}{b^4}}
= \frac{1 - \frac{c^2 x_0^2}{a^4}}{\frac{x_0^2}{a^4} + \frac{y_0^2}{b^4}} .
```

Substitute $y_0^2 = b^2\left(1 - x_0^2/a^2\right)$ in the denominator:

```math
\frac{x_0^2}{a^4} + \frac{1}{b^2} - \frac{x_0^2}{a^2 b^2}
= \frac{1}{b^2} - \frac{(a^2 - b^2)\,x_0^2}{a^4 b^2}
= \frac{1}{b^2}\Bigl(1 - \frac{c^2 x_0^2}{a^4}\Bigr).
```

Hence $d_1 d_2 = b^2$. (The numerator is positive since $|x_0| \le a$ and $c < a$.) $\blacksquare$

## 2. Why it is conserved

By the caustic theorem ([note 02](02-caustic-theorem.md)), every segment of an
orbit is tangent to one fixed confocal ellipse $x^2/a'^2 + y^2/b'^2 = 1$ with
the same foci. Apply Lemma 1 to that ellipse:

```math
d_1 d_2 = b'^2 = a'^2 - c^2 \quad\text{for every segment.}
```

**So $d_1 d_2$ is constant along the orbit**, and its value identifies the caustic.

## 3. Signed version: one formula for both cases

Write the confocal family as

```math
\mathcal C_\lambda:\quad \frac{x^2}{a^2 - \lambda} + \frac{y^2}{b^2 - \lambda} = 1 ,
```

an ellipse for $0 < \lambda < b^2$ and a hyperbola for $b^2 < \lambda < a^2$.
Measure $d_1, d_2$ as **signed** distances, positive on one side of the line
and negative on the other. Then for every segment

```math
\boxed{\; d_1 d_2 = b^2 - \lambda \;}
```

The product is positive when both foci are on the same side of the segment
(ellipse caustic) and negative when the segment passes between them
(hyperbola caustic).

**Example.** The warm-up orbit from $(\sqrt2, 1)$ with direction $(-1,-1)$ crosses
the $x$-axis at $x = \sqrt2 - 1$, which lies between the foci $\pm\sqrt2$. So its
caustic is a hyperbola, and the simulator gives $d_1 d_2 = \tfrac12 - \sqrt2 \approx -0.914$
on all 2000 segments, constant to about $10^{-13}$.

## 4. Proof of $d_1 d_2 = b^2 - \lambda$, both cases at once

> **Gaokao starting point.** Another 二级结论: the line $Ax + By + C = 0$ is
> tangent to $x^2/a^2 + y^2/b^2 = 1$ iff $a^2A^2 + b^2B^2 = C^2$.

**Lemma 2 (tangency condition).** Let $P, Q \ne 0$ and $|\boldsymbol\nu| = 1$.
The line $\boldsymbol\nu\cdot\mathbf x = h$ is tangent to the conic
$x^2/P + y^2/Q = 1$ iff $P\nu_x^2 + Q\nu_y^2 = h^2$.

*Proof.* If $\nu_y \neq 0$, substitute $y = (h - \nu_x x)/\nu_y$ and simplify the
discriminant of the resulting quadratic in $x$. It vanishes iff
$P\nu_x^2 + Q\nu_y^2 = h^2$. The case $\nu_y = 0$ is direct: the line is $x = \pm h$. $\blacksquare$

**Theorem.** If a line $\boldsymbol\nu\cdot\mathbf x = h$ is tangent to
$\mathcal C_\lambda$, then the signed distances from the foci satisfy $d_1 d_2 = b^2 - \lambda$.

*Proof.* The signed distance from $F_{1,2} = (\mp c, 0)$ is $\mp c\nu_x - h$, so,
using Lemma 2 with $P = a^2 - \lambda$, $Q = b^2 - \lambda$,

```math
d_1 d_2 = (-c\nu_x - h)(c\nu_x - h) = h^2 - c^2\nu_x^2
        = (a^2 - \lambda - c^2)\,\nu_x^2 + (b^2 - \lambda)\,\nu_y^2
        = (b^2 - \lambda)(\nu_x^2 + \nu_y^2) = b^2 - \lambda . \qquad\blacksquare
```

With $\lambda = 0$ this reproves Lemma 1 in one line. With $b^2 < \lambda < a^2$
it gives the hyperbola version: the product is $-(\lambda - b^2) = -b''^2$, where
$b''$ is the hyperbola's imaginary semi-axis. Combined with the caustic theorem,
**the signed $d_1d_2$ is conserved on every non-focal orbit.**
