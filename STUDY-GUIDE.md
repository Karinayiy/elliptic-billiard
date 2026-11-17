# Study guide: owning this project

This is my primary independent project. Much of the first draft was written
with AI help (see `LOG.md`). This guide lists what I must be able to do
**without notes** before I show the paper to anyone: an admissions reader, a
professor, or a journal referee. Each item starts from the gaokao.

本项目是我的主要独立项目。初稿有大量 AI 协助（见 `LOG.md`）。给任何人看论文之前，
下面每一项我都必须能**脱稿**完成。

## Level 1: re-derive on a blank page (高考工具)

| # | Result | Gaokao tool | Where | Done |
|---|---|---|---|---|
| 1 | Next bounce $t^\ast = -B/A$ | 联立 + 韦达 | note 01, Prop. 1 | [ ] |
| 2 | Reflection $\mathbf d' = \mathbf d - 2(\mathbf d\cdot\hat n)\hat n$ | 向量投影 | note 01 | [ ] |
| 3 | Optical property of the ellipse | 2010 Anhui Q19, 角平分线 | note 02, Lemma 1 | [ ] |
| 4 | Caustic theorem (ellipse case) | 将军饮马 + SAS 全等 | note 02 | [ ] |
| 5 | $d_1d_2 = b^2$ for a tangent line | 二级结论 $a^2A^2 + b^2B^2 = C^2$ | note 03 | [ ] |
| 6 | Convexity exactly for $-1 < \varepsilon < 3$ | 均值不等式 AM–GM | note 04, Prop. 10 | [ ] |
| 7 | Stability of a 2-periodic orbit, $\operatorname{tr}M = 4g^2 - 2$ | 2×2 矩阵乘法, 判别式 $\Delta < 0$ | note 04, Lemma 11 | [ ] |
| 8 | Radius of curvature at a vertex, $R = b^2/(a(1+\varepsilon))$ | 泰勒/二次近似 $x \approx a - \frac{y^2}{2R}$ | Thm. 12 | [ ] |
| 9 | Why the gaokao ellipse gives $M = -I$ | $a^2 = 2b^2 \Rightarrow L = R$ | Remark 13 | [ ] |

**Test:** explain each one aloud in under 3 minutes, in English, at a
whiteboard.

## Level 2: explain the experiments

- What is a Lyapunov exponent, in one sentence? (How fast two nearby orbits
  separate: distance ≈ $e^{\lambda n}$ after $n$ bounces.)
- Why sample orbits uniformly in $ds\,dp$? (It is the invariant measure, so
  "fraction of orbits" means "fraction of phase space".)
- Why is the threshold 0.05 fair? (The exponents form two separated groups;
  Figure (c) of the extensions shows the answer barely moves between 0.02 and
  0.1, and with orbit length.)
- What does "$d_1d_2$ breaks linearly" mean, and why is it plausible?
  (First-order perturbation: an $O(\varepsilon)$ change to the wall changes
  each bounce by $O(\varepsilon)$.)
- What are the limitations? (Finite time; one family; fits over 1.5 decades;
  thresholds.)

## Level 3: questions a professor might ask

1. *What is new here, and what is classical?* Classical: Sections 2 and 3
   (Birkhoff, Poncelet, the caustic theorem). New, as far as my literature
   search shows: the family $u + v + \varepsilon uv = 1$, the axis-stability
   theorem for it, the 1:4 degeneracy of the gaokao ellipse, and the scaling
   measurements.
2. *Why this family and not superellipses?* It is algebraic of degree four,
   so the next bounce is a cubic (Vieta still works), it passes through the
   same four vertices, and its curvature can be computed exactly.
3. *What is the Birkhoff conjecture, and how is this related?* Ellipses should
   be the only integrable convex tables. Our numerics show every nearby table
   in this family has chaos, which is consistent with the conjecture but
   proves nothing.
4. *What would you do next?* A Melnikov computation for the constant $C$;
   understanding the limit $\varepsilon \to -1$.
5. *How did you use AI?* Answer honestly and specifically, as in `LOG.md`.

## My own next step (not AI-drafted)

Pick one and do it myself, then record it in `LOG.md`:

- [ ] Build the GeoGebra applet for the caustic theorem (note 02).
- [ ] Re-prove Proposition 10 (convexity) in my own words and notation.
- [ ] Read the introduction of Delshams–Ramírez-Ros (1996) and write a
      half-page summary of what a Melnikov function is.
- [ ] Run `research.py` for another aspect ratio myself and compare.
