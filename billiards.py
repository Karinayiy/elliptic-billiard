"""Billiards inside the ellipse x^2/a^2 + y^2/b^2 = 1.

The math behind each function is in notes/.
"""
import numpy as np


def cross(u, v):
    """z-component of the 2D cross product u x v."""
    return u[0] * v[1] - u[1] * v[0]


def reflect(d, n):
    """Reflect direction d off a wall with unit normal n: d' = d - 2(d.n)n."""
    return d - 2 * np.dot(d, n) * n


class Ellipse:
    def __init__(self, a, b):
        self.a, self.b = a, b
        self.c = np.sqrt(a**2 - b**2)
        self.foci = np.array([[-self.c, 0.0], [self.c, 0.0]])

    def normal(self, P):
        """Unit outward normal at P, from the gradient (x/a^2, y/b^2)."""
        n = np.array([P[0] / self.a**2, P[1] / self.b**2])
        return n / np.linalg.norm(n)

    def next_bounce(self, P, d):
        """Where the ball leaving P in direction d hits the wall next (notes/01).

        Substituting P + t d gives A t^2 + B t = 0; the root t = 0 is P itself,
        so by Vieta the other root is t = -B/A.
        """
        A = d[0]**2 / self.a**2 + d[1]**2 / self.b**2
        B = 2 * (P[0] * d[0] / self.a**2 + P[1] * d[1] / self.b**2)
        if abs(B) < 1e-14:
            raise ValueError("d is tangent to the wall at P: no next bounce")
        Q = P + (-B / A) * d
        # pull Q back onto the ellipse so rounding errors don't pile up
        return Q / np.sqrt(Q[0]**2 / self.a**2 + Q[1]**2 / self.b**2)

    def focal_product(self, P, d):
        """Signed d1*d2: distances from the two foci to the line through P along d.

        Conserved along the orbit and equal to b^2 - lambda (notes/03).
        """
        d = d / np.linalg.norm(d)
        return cross(d, self.foci[0] - P) * cross(d, self.foci[1] - P)

    def caustic_residual(self, P, d, lam):
        """How far the line through P along d is from tangent to the confocal
        conic x^2/(a^2-lam) + y^2/(b^2-lam) = 1. Zero means tangent.

        A line nu.x = h is tangent to x^2/p + y^2/q = 1 exactly when
        p nu_x^2 + q nu_y^2 = h^2.
        """
        d = d / np.linalg.norm(d)
        nu = np.array([-d[1], d[0]])
        h = np.dot(nu, P)
        p, q = self.a**2 - lam, self.b**2 - lam
        return p * nu[0]**2 + q * nu[1]**2 - h**2

    def launch_on_caustic(self, lam, phi):
        """A starting point and direction whose orbit has the confocal ellipse
        with parameter lam (0 < lam < b^2) as its caustic.

        Take the point T at angle phi on the caustic, follow its tangent line
        backwards to the wall, and start there moving along the tangent.
        """
        A, B = np.sqrt(self.a**2 - lam), np.sqrt(self.b**2 - lam)
        T = np.array([A * np.cos(phi), B * np.sin(phi)])
        u = np.array([-A * np.sin(phi), B * np.cos(phi)])
        u /= np.linalg.norm(u)
        # T + s u on the wall: quadratic in s with negative constant term,
        # so one root is negative (behind T) -- that's where we start
        qa = u[0]**2 / self.a**2 + u[1]**2 / self.b**2
        qb = 2 * (T[0] * u[0] / self.a**2 + T[1] * u[1] / self.b**2)
        qc = T[0]**2 / self.a**2 + T[1]**2 / self.b**2 - 1
        s = (-qb - np.sqrt(qb**2 - 4 * qa * qc)) / (2 * qa)
        return T + s * u, u


def simulate(E, P, d, n_bounces):
    """Bounce n_bounces times. Returns the bounce points and, for each point,
    the direction of the segment leaving it."""
    P = np.asarray(P, dtype=float)
    d = np.asarray(d, dtype=float)
    d = d / np.linalg.norm(d)
    points, dirs = [P], [d]
    for _ in range(n_bounces):
        P = E.next_bounce(P, d)
        d = reflect(d, E.normal(P))
        points.append(P)
        dirs.append(d)
    return np.array(points), np.array(dirs)


def winding(E, points):
    """Total turning of the bounce points around the centre, in units of 2*pi
    (using the eccentric angle, so equal steps on a circle stay equal)."""
    theta = np.arctan2(points[:, 1] / E.b, points[:, 0] / E.a)
    return np.sum(np.mod(np.diff(theta), 2 * np.pi)) / (2 * np.pi)


def periodic_caustic(E, m, n, tol=1e-13):
    """lambda of the caustic whose orbits close after n bounces and m turns
    (rotation number m/n), found by bisection. Bigger lambda means a smaller
    caustic, longer chords and more turning."""
    lo, hi = 1e-9, E.b**2 - 1e-9
    while hi - lo > tol:
        mid = (lo + hi) / 2
        P, d = E.launch_on_caustic(mid, 0.0)
        points, _ = simulate(E, P, d, n)
        if winding(E, points) < m:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2
