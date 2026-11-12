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

## To do myself

- [ ] Prove the hyperbola version of Lemma 1 (signed product $= -b''^2$ for
      $x^2/a''^2 - y^2/b''^2 = 1$).
- [ ] Derive $d_1 d_2 = b^2 - \lambda$. Hint: a line $\boldsymbol\nu\cdot\mathbf x = h$
      with $|\boldsymbol\nu| = 1$ is tangent to $x^2/P + y^2/Q = 1$ exactly when
      $P\nu_x^2 + Q\nu_y^2 = h^2$.
