# 01 · The next bounce point

> **Gaokao starting point.** 2025 National Paper II, Q16: the ellipse
> $C:\ x^2/4 + y^2/2 = 1$, a line meets $C$, and one solves by 联立 + 韦达.
> A billiard bounce is the same computation, except one root is already known.

Throughout, $C$ is the ellipse

```math
\frac{x^2}{a^2} + \frac{y^2}{b^2} = 1, \qquad a > b > 0 .
```

## 1. A worked example

Take $a^2 = 4,\ b^2 = 2$ and $P = (\sqrt2, 1)$. Then $P \in C$, since
$\tfrac{2}{4} + \tfrac{1}{2} = 1$.

The ball leaves $P$ with direction $\mathbf d = (-1,-1)$, so its position at time
$t$ is $(\sqrt2 - t,\ 1 - t)$. Substituting into $C$:

```math
\frac{(\sqrt2 - t)^2}{4} + \frac{(1-t)^2}{2} = 1
\;\Longrightarrow\;
\tfrac34\, t^2 - \Bigl(1 + \tfrac{\sqrt2}{2}\Bigr) t = 0 .
```

The constant term vanishes because $P \in C$, so $t_1 = 0$ is a root. By
Vieta's formulas,

```math
t_2 = -\frac{B}{A} = \frac{1 + \sqrt2/2}{3/4} = \frac{4 + 2\sqrt2}{3} \approx 2.276,
\qquad
Q = \Bigl(\frac{\sqrt2 - 4}{3},\ -\frac{1 + 2\sqrt2}{3}\Bigr) \approx (-0.862,\,-1.276).
```

*Check.* $\dfrac{x_Q^2}{4} + \dfrac{y_Q^2}{2} = \dfrac{18 - 8\sqrt2}{36} + \dfrac{18 + 8\sqrt2}{36} = 1.$ ✓

## 2. The general formula

Let $P = (x_0, y_0) \in C$ and $\mathbf d = (p, q) \neq \mathbf 0$. Substituting
$(x_0 + pt,\ y_0 + qt)$ into $C$ gives $At^2 + Bt + C_0 = 0$ with

```math
A = \frac{p^2}{a^2} + \frac{q^2}{b^2}, \qquad
B = 2\Bigl(\frac{x_0 p}{a^2} + \frac{y_0 q}{b^2}\Bigr), \qquad
C_0 = \frac{x_0^2}{a^2} + \frac{y_0^2}{b^2} - 1 = 0 .
```

**Proposition 1.** The line through $P$ in direction $\mathbf d$ meets $C$ again at
$Q = P + t^\ast \mathbf d$, where

```math
\boxed{\; t^\ast = -\,\frac{2\left(x_0 p/a^2 + y_0 q/b^2\right)}{p^2/a^2 + q^2/b^2} \;}
```

Write $\mathbf n = (x_0/a^2,\ y_0/b^2)$. This is half the gradient of
$x^2/a^2 + y^2/b^2$, so it is an outward **normal** to $C$ at $P$, and
$B = 2\,\mathbf d\cdot\mathbf n$. The same $\mathbf n$ gives the reflection law in
[note 02](02-caustic-theorem.md).

## 3. Degenerate cases

1. **$\mathbf d \cdot \mathbf n = 0$.** Then $B = 0$ and $t = 0$ is a double root:
   the line meets $C$ only at $P$, which is the $\Delta = 0$ (相切) case of 联立.
   The ball grazes the wall and there is no next bounce. The code raises an
   error here instead of returning $Q = P$.
2. **$A = 0$?** $A$ is a sum of squares, so it vanishes only when $p = q = 0$.
   The division in Proposition 1 is always safe.

## To do myself

- [ ] Re-derive Proposition 1 on a blank page without looking.
