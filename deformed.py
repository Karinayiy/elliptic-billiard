"""Billiards in the deformed tables  u + v + eps*u*v = 1,  u = x^2/a^2, v = y^2/b^2.

eps = 0 is the ellipse, eps -> -1 tends to the rectangle |x| <= a, |y| <= b.
Every table passes through the four vertices (+-a, 0), (0, +-b).

All functions are vectorized: states are arrays of shape (N,) or (N, 2).
The math is in notes/04-deformed-tables.md.
"""
import numpy as np


class Table:
    def __init__(self, a, b, eps):
        self.a, self.b, self.eps = a, b, eps
        self.c = np.sqrt(a**2 - b**2)
        self.foci = np.array([[-self.c, 0.0], [self.c, 0.0]])

    # --- the wall -------------------------------------------------------
    def point(self, psi):
        """Wall point at polar angle psi. Along a ray, r^2 solves a quadratic:
        eps*CS*R^2 + A*R - 1 = 0 with A = cos^2/a^2 + sin^2/b^2, CS = cos^2 sin^2/(a^2 b^2)."""
        co, si = np.cos(psi), np.sin(psi)
        A = co**2 / self.a**2 + si**2 / self.b**2
        CS = co**2 * si**2 / (self.a**2 * self.b**2)
        R = 2 / (A + np.sqrt(A**2 + 4 * self.eps * CS))
        r = np.sqrt(R)
        return np.stack([r * co, r * si], axis=-1)

    def grad(self, P):
        u = P[..., 0]**2 / self.a**2
        v = P[..., 1]**2 / self.b**2
        gx = 2 * P[..., 0] / self.a**2 * (1 + self.eps * v)
        gy = 2 * P[..., 1] / self.b**2 * (1 + self.eps * u)
        return np.stack([gx, gy], axis=-1)

    def frame(self, P):
        """Unit counterclockwise tangent and unit inward normal at wall points P."""
        g = self.grad(P)
        n = g / np.linalg.norm(g, axis=-1, keepdims=True)
        return np.stack([-n[..., 1], n[..., 0]], axis=-1), -n

    # --- one bounce -----------------------------------------------------
    def next_point(self, P, d):
        """Second intersection of the line P + t d with the wall.

        Substituting gives a quartic in t. t = 0 is a root (P is on the wall),
        so dividing by t leaves a cubic -- the same idea as Vieta for the
        ellipse, where the quadratic leaves a linear equation."""
        a2, b2, e = self.a**2, self.b**2, self.eps
        x0, y0, p, q = P[:, 0], P[:, 1], d[:, 0], d[:, 1]
        u0, u1, u2 = x0**2 / a2, 2 * x0 * p / a2, p**2 / a2
        v0, v1, v2 = y0**2 / b2, 2 * y0 * q / b2, q**2 / b2
        c0 = u1 + v1 + e * (u0 * v1 + u1 * v0)
        c1 = u2 + v2 + e * (u0 * v2 + u1 * v1 + u2 * v0)
        c2 = e * (u1 * v2 + u2 * v1)
        c3 = e * u2 * v2
        if e == 0:
            t = -c0 / c1
        else:
            # roots of c3 t^3 + c2 t^2 + c1 t + c0 via batched companion matrices
            comp = np.zeros((len(t0 := c0), 3, 3))
            comp[:, 0, :] = -np.stack([c2, c1, t0], axis=1) / c3[:, None]
            comp[:, 1, 0] = comp[:, 2, 1] = 1.0
            roots = np.linalg.eigvals(comp)
            real = np.abs(roots.imag) < 1e-7 * (1 + np.abs(roots.real))
            cand = np.where(real & (roots.real > 1e-12), roots.real, np.inf)
            t = cand.min(axis=1)
            # c3 can underflow for directions along an axis; fall back to the quadratic
            small = np.abs(c3) < 1e-14
            if small.any():
                disc = np.sqrt(np.maximum(c1**2 - 4 * c2 * c0, 0))
                with np.errstate(divide="ignore", invalid="ignore"):
                    r1 = np.where(np.abs(c2) > 1e-14, (-c1 + disc) / (2 * c2), -c0 / c1)
                    r2 = np.where(np.abs(c2) > 1e-14, (-c1 - disc) / (2 * c2), np.inf)
                cands = np.stack([r1, r2], axis=1)
                cands = np.where(cands > 1e-12, cands, np.inf)
                t = np.where(small, cands.min(axis=1), t)
        # two Newton steps on the cubic to polish the root
        for _ in range(2):
            f = ((c3 * t + c2) * t + c1) * t + c0
            df = (3 * c3 * t + 2 * c2) * t + c1
            t = t - f / df
        return P + t[:, None] * d

    def bounce(self, P, d):
        Q = self.next_point(P, d)
        g = self.grad(Q)
        n = g / np.linalg.norm(g, axis=1, keepdims=True)
        d = d - 2 * np.sum(d * n, axis=1, keepdims=True) * n
        return Q, d

    # --- phase-space coordinates (psi, alpha) -----------------------------
    def state(self, psi, alpha):
        """Wall point at polar angle psi, direction at angle alpha in (0, pi)
        from the counterclockwise tangent, pointing inward."""
        P = self.point(psi)
        T, N = self.frame(P)
        return P, np.cos(alpha)[:, None] * T + np.sin(alpha)[:, None] * N

    def coords(self, P, d):
        T, N = self.frame(P)
        psi = np.mod(np.arctan2(P[:, 1], P[:, 0]), 2 * np.pi)
        alpha = np.arctan2(np.sum(d * N, axis=1), np.sum(d * T, axis=1))
        return psi, alpha

    def step(self, psi, alpha):
        return self.coords(*self.bounce(*self.state(psi, alpha)))

    # --- measurements -----------------------------------------------------
    def focal_product(self, P, d):
        """Signed d1*d2 for the foci of the ellipse eps = 0 (unit d)."""
        c1 = d[:, 0] * (self.foci[0, 1] - P[:, 1]) - d[:, 1] * (self.foci[0, 0] - P[:, 0])
        c2 = d[:, 0] * (self.foci[1, 1] - P[:, 1]) - d[:, 1] * (self.foci[1, 0] - P[:, 0])
        return c1 * c2

    def curvature_sign_ok(self, n=4000):
        """True if the wall is strictly convex (curvature never changes sign)."""
        psi = np.linspace(0, 2 * np.pi, n, endpoint=False)
        P = self.point(psi)
        dP = np.gradient(P, psi, axis=0)
        d2P = np.gradient(dP, psi, axis=0)
        k = dP[:, 0] * d2P[:, 1] - dP[:, 1] * d2P[:, 0]
        return bool(np.all(k > 0))

    def arclength_sampler(self, n=20000):
        """Function mapping uniform numbers in [0,1) to polar angles, uniform in arclength."""
        psi = np.linspace(0, 2 * np.pi, n + 1)
        P = self.point(psi)
        s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
        return lambda w: np.interp(w * s[-1], s, psi)


def wrap(x):
    return np.mod(x + np.pi, 2 * np.pi) - np.pi


def lyapunov(table, psi, alpha, n_steps, delta=1e-8, rng=None):
    """Finite-time Lyapunov exponents (Benettin's method) in (psi, alpha) coordinates.
    Also returns the range of d1d2 over each orbit."""
    rng = rng or np.random.default_rng(0)
    ang = rng.uniform(0, 2 * np.pi, len(psi))
    du = np.stack([np.cos(ang), np.sin(ang)], axis=1)
    total = np.zeros(len(psi))
    lo = np.full(len(psi), np.inf)
    hi = np.full(len(psi), -np.inf)
    for _ in range(n_steps):
        P, d = table.state(psi, alpha)
        prod = table.focal_product(P, d)
        lo, hi = np.minimum(lo, prod), np.maximum(hi, prod)
        p2, a2 = psi + delta * du[:, 0], np.clip(alpha + delta * du[:, 1], 1e-9, np.pi - 1e-9)
        psi, alpha = table.coords(*table.bounce(P, d))
        q_psi, q_alpha = table.step(p2, a2)
        sep = np.stack([wrap(q_psi - psi), q_alpha - alpha], axis=1)
        norm = np.linalg.norm(sep, axis=1)
        total += np.log(norm / delta)
        du = sep / norm[:, None]
    return total / n_steps, hi - lo
