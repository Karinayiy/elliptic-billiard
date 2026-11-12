"""Numerical checks of notes 01-03 and the Poncelet porism. Saves figures to figures/."""
import os

import matplotlib.pyplot as plt
import numpy as np

from billiards import Ellipse, periodic_caustic, simulate

E = Ellipse(2.0, np.sqrt(2.0))  # x^2/4 + y^2/2 = 1, 2025 National Paper II Q16
os.makedirs("figures", exist_ok=True)


def check_warmup():
    print("1. Warm-up (notes/01)")
    P, d = np.array([np.sqrt(2), 1.0]), np.array([-1.0, -1.0])
    Q = E.next_bounce(P, d)
    exact = np.array([(np.sqrt(2) - 4) / 3, -(1 + 2 * np.sqrt(2)) / 3])
    print(f"   Q = {Q}, exact = {exact}, error = {np.abs(Q - exact).max():.1e}")


def check_conserved(name, d0, n_bounces=2000):
    P0 = np.array([np.sqrt(2), 1.0])
    points, dirs = simulate(E, P0, d0, n_bounces)
    prods = np.array([E.focal_product(P, d) for P, d in zip(points[:-1], dirs[:-1])])
    lam = E.b**2 - prods[0]
    resid = np.array([E.caustic_residual(P, d, lam) for P, d in zip(points[:-1], dirs[:-1])])
    kind = "ellipse" if prods[0] > 0 else "hyperbola"
    print(f"   {name}: d1d2 = {prods[0]:.12f}, spread over {n_bounces} bounces = "
          f"{prods.max() - prods.min():.1e}")
    print(f"      caustic: {kind}, lambda = {lam:.6f}, max tangency residual = "
          f"{np.abs(resid).max():.1e}")
    return points, lam


def plot_orbit(ax, points, lam, title):
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(E.a * np.cos(t), E.b * np.sin(t), "k", lw=1.5)
    ax.plot(points[:, 0], points[:, 1], lw=0.3, alpha=0.6)
    if lam < E.b**2:
        A, B = np.sqrt(E.a**2 - lam), np.sqrt(E.b**2 - lam)
        ax.plot(A * np.cos(t), B * np.sin(t), "r", lw=1.2, label="caustic")
    else:
        A, B = np.sqrt(E.a**2 - lam), np.sqrt(lam - E.b**2)
        s = np.linspace(-1.5, 1.5, 200)
        for sx in (1, -1):
            ax.plot(sx * A * np.cosh(s), B * np.sinh(s), "r", lw=1.2)
    ax.plot(*E.foci.T, "k.", ms=6)
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect("equal")
    ax.set_title(title)


def check_poncelet(m, n, n_starts=12):
    lam = periodic_caustic(E, m, n)
    closes, perims = [], []
    for phi in np.linspace(0, 2 * np.pi, n_starts, endpoint=False):
        P, d = E.launch_on_caustic(lam, phi)
        points, _ = simulate(E, P, d, n)
        closes.append(np.linalg.norm(points[-1] - points[0]))
        perims.append(np.sum(np.linalg.norm(np.diff(points, axis=0), axis=1)))
    perims = np.array(perims)
    print(f"   rotation {m}/{n}: lambda = {lam:.10f}, max closing gap = "
          f"{max(closes):.1e}, perimeter = {perims.mean():.10f} "
          f"(spread {perims.max() - perims.min():.1e})")
    return lam


def plot_poncelet(ax, m, n, lam, n_starts=5):
    t = np.linspace(0, 2 * np.pi, 400)
    ax.plot(E.a * np.cos(t), E.b * np.sin(t), "k", lw=1.5)
    A, B = np.sqrt(E.a**2 - lam), np.sqrt(E.b**2 - lam)
    ax.plot(A * np.cos(t), B * np.sin(t), "r", lw=1.2)
    for phi in np.linspace(0, 2 * np.pi / n, n_starts, endpoint=False):
        P, d = E.launch_on_caustic(lam, phi)
        points, _ = simulate(E, P, d, n)
        ax.plot(points[:, 0], points[:, 1], lw=1)
    ax.set_aspect("equal")
    ax.set_title(f"rotation number {m}/{n}")
    ax.axis("off")


if __name__ == "__main__":
    check_warmup()

    print("2. Conserved d1d2 and the caustic (notes/02, 03)")
    # the warm-up direction crosses the x-axis at x = √2 - 1, between the foci
    pts_h, lam_h = check_conserved("start (√2,1), d = (-1,-1)", np.array([-1.0, -1.0]))
    pts_e, lam_e = check_conserved("start (√2,1), d = (-1,0.3)", np.array([-1.0, 0.3]))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    plot_orbit(axes[0], pts_e[:300], lam_e, "segment misses F1F2: ellipse caustic")
    plot_orbit(axes[1], pts_h[:300], lam_h, "segment crosses F1F2: hyperbola caustic")
    fig.tight_layout()
    fig.savefig("figures/caustics.png", dpi=150)

    print("3. Poncelet porism: every start closes, all perimeters equal")
    cases = [(1, 3), (1, 4), (1, 5), (2, 5)]
    lams = [check_poncelet(m, n) for m, n in cases]
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
    for ax, (m, n), lam in zip(axes, cases, lams):
        plot_poncelet(ax, m, n, lam)
    fig.tight_layout()
    fig.savefig("figures/poncelet.png", dpi=150)
    print("Figures saved to figures/")
