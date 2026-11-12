"""Numerical checks of every claim in notes/01-03. Run: .venv/bin/python verify.py

Each check prints PASS or FAIL; the script exits with an error if any check fails.
"""
import sys

import numpy as np

from billiards import Ellipse, periodic_caustic, simulate

E = Ellipse(2.0, np.sqrt(2.0))  # x^2/4 + y^2/2 = 1, 2025 National Paper II Q16
TOL = 1e-10
failures = []


def check(name, error, tol=TOL):
    ok = error < tol
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {error:.1e}")
    if not ok:
        failures.append(name)


def mirror(X, P, d):
    d = d / np.linalg.norm(d)
    v = X - P
    return P + 2 * np.dot(v, d) * d - v


def side(X, P, d):
    return np.sign(d[0] * (X[1] - P[1]) - d[1] * (X[0] - P[0]))


def angle(u, v):
    return np.arccos(np.clip(np.dot(u, v) / np.linalg.norm(u) / np.linalg.norm(v), -1, 1))


print("Note 01: next bounce")
P, d = np.array([np.sqrt(2), 1.0]), np.array([-1.0, -1.0])
Q = E.next_bounce(P, d)
check("Q matches ((√2-4)/3, -(1+2√2)/3)",
      np.abs(Q - [(np.sqrt(2) - 4) / 3, -(1 + 2 * np.sqrt(2)) / 3]).max())
try:
    E.next_bounce(np.array([E.a, 0.0]), np.array([0.0, 1.0]))
    check("tangent direction is refused", 1.0)
except ValueError:
    check("tangent direction is refused", 0.0)

print("Note 02: caustic theorem, every step of the proof on random orbits")
rng = np.random.default_rng(0)
gap = ang_err = 0.0
switches = outside = 0
for _ in range(300):
    phi, th = rng.uniform(0, 2 * np.pi), rng.uniform(0.05, np.pi - 0.05)
    P = np.array([E.a * np.cos(phi), E.b * np.sin(phi)])
    n = E.normal(P)
    points, _ = simulate(E, P, np.cos(th) * np.array([-n[1], n[0]]) - np.sin(th) * n, 6)
    F1, F2 = E.foci
    for A, B, C in zip(points[:-2], points[1:-1], points[2:]):
        sep_ab = side(F1, A, B - A) != side(F2, A, B - A)
        sep_bc = side(F1, B, C - B) != side(F2, B, C - B)
        switches += sep_ab != sep_bc
        if sep_ab:
            continue
        F1p, F2p = mirror(F1, A, B - A), mirror(F2, B, C - B)
        s, _ = np.linalg.solve(np.column_stack([B - A, F1p - F2]), F1p - A)
        outside += not (0 < s < 1)
        gap = max(gap, abs(np.linalg.norm(F2 - F1p) - np.linalg.norm(F2p - F1)))
        ang_err = max(ang_err,
                      abs(angle(F1p - B, F2 - B) - angle(A - B, F1 - B) - angle(A - B, F2 - B)),
                      abs(angle(F1 - B, F2p - B) - angle(C - B, F1 - B) - angle(C - B, F2 - B)))
check("Lemma 2: tangency point strictly inside the chord (violations)", outside, 0.5)
check("Lemma 3: separation never switches (violations)", switches, 0.5)
check("angle identities in step 3", ang_err)
check("|F1'F2| = |F1F2'|", gap)

print("Note 03: d1d2 conserved and equal to b^2 - lambda, 5000 bounces")
for d, kind in [((-1.0, -0.3), "ellipse"), ((-1.0, -1.0), "hyperbola")]:
    points, dirs = simulate(E, [np.sqrt(2), 1.0], d, 5000)
    prods = np.array([E.focal_product(P, v) for P, v in zip(points, dirs)])
    lam = E.b**2 - prods[0]
    resid = max(abs(E.caustic_residual(P, v, lam)) for P, v in zip(points, dirs))
    check(f"{kind} caustic: spread of d1d2", np.ptp(prods))
    check(f"{kind} caustic: every segment tangent to lambda = {lam:.4f}", resid)
check("warm-up orbit has d1d2 = 1/2 - √2",
      abs(E.focal_product(np.array([np.sqrt(2), 1.0]), np.array([-1.0, -1.0])) - (0.5 - np.sqrt(2))))

print("Poncelet porism: closing from every start, equal perimeters")
for m, k in [(1, 3), (1, 4), (2, 7), (1, 5)]:
    lam = periodic_caustic(E, m, k)
    gaps, perims = [], []
    for phi in np.linspace(0, 2 * np.pi, 24, endpoint=False):
        points, _ = simulate(E, *E.launch_on_caustic(lam, phi), k)
        gaps.append(np.linalg.norm(points[-1] - points[0]))
        perims.append(np.sum(np.linalg.norm(np.diff(points, axis=0), axis=1)))
    check(f"rotation {m}/{k}: closing gap", max(gaps))
    check(f"rotation {m}/{k}: perimeter spread (perimeter {np.mean(perims):.9f})", np.ptp(perims))
lam = periodic_caustic(E, 1, 4)
P, d = E.launch_on_caustic(lam, 0.0)
points, _ = simulate(E, P, d, 4)
check("rotation 1/4 perimeter = 4√(a²+b²) (rhombus through the vertices)",
      abs(np.sum(np.linalg.norm(np.diff(points, axis=0), axis=1)) - 4 * np.sqrt(E.a**2 + E.b**2)))

print()
if failures:
    print(f"{len(failures)} check(s) FAILED")
    sys.exit(1)
print("All checks passed.")
