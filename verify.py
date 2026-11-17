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

print("Note 02: hyperbola case, on random orbits whose segments separate the foci")
gap_h = ang_h = 0.0
count_h = 0
for _ in range(300):
    phi, th = rng.uniform(0, 2 * np.pi), rng.uniform(0.05, np.pi - 0.05)
    P = np.array([E.a * np.cos(phi), E.b * np.sin(phi)])
    n = E.normal(P)
    points, _ = simulate(E, P, np.cos(th) * np.array([-n[1], n[0]]) - np.sin(th) * n, 6)
    F1, F2 = E.foci
    for A, B, C in zip(points[:-2], points[1:-1], points[2:]):
        if side(F1, A, B - A) == side(F2, A, B - A):
            continue
        count_h += 1
        F1p, F2p = mirror(F1, A, B - A), mirror(F2, B, C - B)
        gap_h = max(gap_h, abs(np.linalg.norm(F2 - F1p) - np.linalg.norm(F2p - F1)))
        ang_h = max(ang_h,
                    abs(angle(F1p - B, F2 - B) - abs(angle(A - B, F2 - B) - angle(A - B, F1 - B))),
                    abs(angle(F1 - B, F2p - B) - abs(angle(C - B, F1 - B) - angle(C - B, F2 - B))))
check(f"angle identities, hyperbola case ({count_h} bounces)", ang_h)
check("|F1'F2| = |F1F2'|, hyperbola case", gap_h)

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

print("Note 04: deformed tables u + v + eps*u*v = 1")
from deformed import Table
T0 = Table(E.a, E.b, 0.0)
check("eps = 0 reproduces the ellipse simulator",
      np.abs(T0.next_point(np.array([[np.sqrt(2), 1.0]]), np.array([[-1.0, -1.0]]) / np.sqrt(2))[0]
             - E.next_bounce(np.array([np.sqrt(2), 1.0]), np.array([-1.0, -1.0]))).max())
worst_wall = worst_inside = 0.0
for eps in (-0.95, -0.5, -0.01, 0.01, 1.0, 2.9):
    T = Table(E.a, E.b, eps)
    r = np.random.default_rng(5)
    P0, d0 = T.state(r.uniform(0, 2 * np.pi, 3000), r.uniform(0.001, np.pi - 0.001, 3000))
    Q = T.next_point(P0, d0)
    G = lambda X: X[:, 0]**2 / E.a**2 + X[:, 1]**2 / E.b**2 + eps * X[:, 0]**2 * X[:, 1]**2 / (E.a**2 * E.b**2)
    worst_wall = max(worst_wall, np.abs(G(Q) - 1).max())
    worst_inside = max(worst_inside, max((G(P0 + s * (Q - P0)) - 1).max() for s in np.linspace(0.01, 0.99, 25)))
check("next point lies on the wall", worst_wall)
check("chord interior lies inside the table (max G-1, must be < 0)", max(worst_inside, 0.0))
check("strictly convex just below eps = 3", 0.0 if Table(E.a, E.b, 2.999).curvature_sign_ok(200000) else 1.0)
def axis_trace(T, psi0, h=1e-6):
    def f(x):
        s, al = T.step(np.array([x[0]]), np.array([x[1]]))
        s, al = T.step(s, al)
        return np.array([wrap_angle(s[0] - psi0) + psi0, al[0]])
    x0, J = np.array([psi0, np.pi / 2]), np.zeros((2, 2))
    for j in range(2):
        e = np.zeros(2)
        e[j] = h
        J[:, j] = (f(x0 + e) - f(x0 - e)) / (2 * h)
    return np.trace(J)


def wrap_angle(x):
    return np.mod(x + np.pi, 2 * np.pi) - np.pi


err_major = err_minor = 0.0
for eps in (-0.9, -0.75, -0.6, -0.5, -0.3, 0.0, 0.3, 0.5, 1.0, 1.5, 2.5):
    T = Table(E.a, E.b, eps)
    err_major = max(err_major, abs(axis_trace(T, 0.0) - 2 * (2 * (3 + 4 * eps)**2 - 1)))
    err_minor = max(err_minor, abs(axis_trace(T, np.pi / 2) - 2 * (2 * eps**2 - 1)))
check("major-axis orbit: tr M = 2(2(3+4eps)^2-1)", err_major, 1e-3)
check("minor-axis orbit: tr M = 2(2 eps^2-1)", err_minor, 1e-3)

# General aspect ratio k = b^2/a^2: g_major = 1 - 2(1+eps)/k, g_minor = 1 - 2k(1+eps), tr = 4g^2 - 2.
err_gen = 0.0
for ratio in (0.5, 0.6, 0.8, 0.9):
    k = ratio**2
    for eps in (-0.5, -0.2, 0.1, 0.7):
        T = Table(2.0, 2.0 * ratio, eps)
        g_maj, g_min = 1 - 2 * (1 + eps) / k, 1 - 2 * k * (1 + eps)
        err_gen = max(err_gen, abs(axis_trace(T, 0.0) - (4 * g_maj**2 - 2)) / max(1, abs(4 * g_maj**2 - 2)),
                      abs(axis_trace(T, np.pi / 2) - (4 * g_min**2 - 2)))
check("axis traces for general b/a (16 tables, relative error)", err_gen, 1e-3)
check("curvature vanishes at eps = 3 (diagonal)", 1.0 if Table(E.a, E.b, 3.0).curvature_sign_ok(200000) else 0.0)

# Proposition (convexity): the curvature has the sign of 1 - 3*eps*X^2*Y^2 (X = x/a, Y = y/b).
bad = 0
for eps in [-0.9, -0.5, 0.5, 1.0, 2.0, 2.9, 3.5, 5.0]:
    T = Table(E.a, E.b, eps)
    psi = np.linspace(0, 2 * np.pi, 20000, endpoint=False)
    P = T.point(psi)
    dP = np.gradient(P, psi, axis=0)
    d2P = np.gradient(dP, psi, axis=0)
    k = dP[:, 0] * d2P[:, 1] - dP[:, 1] * d2P[:, 0]
    f = 1 - 3 * eps * (P[:, 0] / E.a) ** 2 * (P[:, 1] / E.b) ** 2
    keep = np.abs(f) > 1e-3
    bad += int(np.sum(np.sign(k[keep]) != np.sign(f[keep])))
check("curvature sign = sign(1 - 3 eps X^2 Y^2), 8 values of eps (mismatches)", bad, 0.5)

print()
if failures:
    print(f"{len(failures)} check(s) FAILED")
    sys.exit(1)
print("All checks passed.")
