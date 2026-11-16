"""Make every figure in figures/. Run: .venv/bin/python figures.py"""
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
from matplotlib.patches import Polygon

from billiards import Ellipse, periodic_caustic, phase_coords, simulate

E = Ellipse(2.0, np.sqrt(2.0))  # x^2/4 + y^2/2 = 1, 2025 National Paper II Q16

INK = "#1d2433"
MUTED = "#8a8f9c"
ORBIT = "#2f6db5"
CAUSTIC = "#d1495b"
GOLD = "#e0a030"
TEAL = "#1b8a8f"
PALETTE = ["#2f6db5", "#d1495b", "#e0a030", "#1b8a8f", "#7a4fb0"]

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["STIXGeneral", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "savefig.dpi": 220,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.08,
})

T = np.linspace(0, 2 * np.pi, 600)


def draw_table(ax, lw=1.6):
    ax.plot(E.a * np.cos(T), E.b * np.sin(T), color=INK, lw=lw, zorder=5)
    ax.plot(*E.foci.T, "o", color=INK, ms=4, zorder=6)


def draw_conic(ax, lam, **kw):
    if lam < E.b**2:
        A, B = np.sqrt(E.a**2 - lam), np.sqrt(E.b**2 - lam)
        ax.plot(A * np.cos(T), B * np.sin(T), **kw)
    else:
        A, B = np.sqrt(E.a**2 - lam), np.sqrt(lam - E.b**2)
        s = np.linspace(-1.6, 1.6, 300)
        for sx in (1, -1):
            ax.plot(sx * A * np.cosh(s), B * np.sinh(s), **kw)


def bare(ax, pad=0.12):
    ax.set_aspect("equal")
    ax.set_xlim(-E.a - pad, E.a + pad)
    ax.set_ylim(-E.b - pad, E.b + pad)
    ax.axis("off")


def mirror(X, P, d):
    """Reflect point X in the line through P with direction d."""
    d = d / np.linalg.norm(d)
    v = X - P
    return P + 2 * np.dot(v, d) * d - v


def intersect(P, u, Q, v):
    s, _ = np.linalg.solve(np.column_stack([u, -v]), Q - P)
    return P + s * u


def fig_caustics():
    cases = [
        (np.array([-1.0, -0.3]), "segment misses $F_1F_2$: ellipse caustic"),
        (np.array([-1.0, -1.0]), "segment crosses $F_1F_2$: hyperbola caustic"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.9))
    for ax, (d, title) in zip(axes, cases):
        points, dirs = simulate(E, [np.sqrt(2), 1.0], d, 400)
        lam = E.b**2 - E.focal_product(points[0], dirs[0])
        for P, Q in zip(points[:-1], points[1:]):
            ax.plot(*np.array([P, Q]).T, color=ORBIT, lw=0.45, alpha=0.45)
        ax.plot(*np.array([points[0], points[1]]).T, color=GOLD, lw=2.2, zorder=7)
        draw_conic(ax, lam, color=CAUSTIC, lw=1.8, zorder=8)
        draw_table(ax)
        bare(ax)
        ax.set_title(title, color=INK)
    axes[1].annotate("warm-up segment\n$P=(\\sqrt{2},1)$, $d=(-1,-1)$",
                     xy=(1.0, 1 - (np.sqrt(2) - 1.0)), xytext=(2.3, 1.25), fontsize=9.5, color=INK,
                     arrowprops=dict(arrowstyle="->", color=INK, lw=0.8))
    fig.savefig("figures/caustics.png")
    plt.close(fig)


def fig_proof():
    lam = 1.15
    P0, d0 = E.launch_on_caustic(lam, 0.785)
    (A, B, C), _ = simulate(E, P0, d0, 2)
    F1, F2 = E.foci
    F1p = mirror(F1, A, B - A)
    F2p = mirror(F2, B, C - B)
    T1 = intersect(F1p, F2 - F1p, A, B - A)
    T2 = intersect(F1, F2p - F1, B, C - B)
    n = E.normal(B)

    fig, ax = plt.subplots(figsize=(6.6, 7.0))
    draw_conic(ax, lam, color=CAUSTIC, lw=1.4, ls=(0, (5, 3)), zorder=2)
    draw_table(ax)
    ax.add_patch(Polygon([F1p, B, F2], closed=True, fc=ORBIT, alpha=0.12, ec="none"))
    ax.add_patch(Polygon([F1, B, F2p], closed=True, fc=GOLD, alpha=0.18, ec="none"))
    for P, Q, c in [(F1p, F2, ORBIT), (F1, F2p, GOLD)]:
        ax.plot(*np.array([P, Q]).T, color=c, lw=1.3, ls=(0, (4, 2)))
    for P, Q, c in [(B, F1p, ORBIT), (B, F2, ORBIT), (B, F1, GOLD), (B, F2p, GOLD)]:
        ax.plot(*np.array([P, Q]).T, color=c, lw=1.1)
    for P, Q in [(F1, F1p), (F2, F2p)]:
        ax.plot(*np.array([P, Q]).T, color=MUTED, lw=0.8, ls=":")
    ax.plot(*np.array([A, B, C]).T, color=INK, lw=2.4, solid_capstyle="round", zorder=7)
    ax.plot(*np.array([B - 0.3 * n, B + 2.2 * n]).T, color=MUTED, lw=0.9, ls="--", zorder=1)
    ax.plot(*np.array([T1, T2]).T, "o", color=CAUSTIC, ms=5.5, zorder=8)
    ax.plot(*np.array([A, B, C, F1, F2, F1p, F2p]).T, "o", color=INK, ms=4.5, zorder=8)

    def label(P, text, dx, dy, fontsize=14):
        ax.annotate(text, P, xytext=(dx, dy), textcoords="offset points",
                    ha="center", va="center", fontsize=fontsize, color=INK, zorder=9)
    label(A, "$A$", 13, 2)
    label(B, "$B$", 13, 9)
    label(C, "$C$", -13, 2)
    label(F1, "$F_1$", 0, -15)
    label(F2, "$F_2$", 0, -15)
    label(F1p, "$F_1'$", 15, 5)
    label(F2p, "$F_2'$", -15, 5)
    label(T1, "$P_0$", 4, -14, fontsize=12)
    label(T2, "$Q_0$", -4, -14, fontsize=12)
    label(B + 2.2 * n, "normal at $B$", 0, 9, fontsize=10)
    ax.set_title("$\\triangle F_1'BF_2 \\cong \\triangle F_1BF_2'$ (SAS), so "
                 "$|F_1'F_2| = |F_1F_2'|$:\n$AB$ and $BC$ touch the same confocal "
                 "ellipse (dashed)", fontsize=12, color=INK)
    ax.set_xlim(-2.35, 2.35)
    ax.set_ylim(-1.6, max(F1p[1], F2p[1], (B + 2.2 * n)[1]) + 0.35)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig("figures/proof.png")
    plt.close(fig)


def fig_poncelet():
    cases = [(1, 5), (1, 4), (2, 7), (1, 3)]
    fig, axes = plt.subplots(1, 4, figsize=(14, 3.3))
    for ax, (m, k) in zip(axes, cases):
        lam = periodic_caustic(E, m, k)
        draw_conic(ax, lam, color=CAUSTIC, lw=1.2, ls=(0, (4, 2.5)))
        for j, phi in enumerate(np.linspace(0, 2 * np.pi / k, 4, endpoint=False)):
            P, d = E.launch_on_caustic(lam, phi + 0.15)
            points, _ = simulate(E, P, d, k)
            ax.plot(*points.T, color=PALETTE[j], lw=1.3, alpha=0.9)
            ax.plot(*points[:-1].T, "o", color=PALETTE[j], ms=2.5)
        draw_table(ax, lw=1.4)
        bare(ax)
        perim = np.sum(np.linalg.norm(np.diff(points, axis=0), axis=1))
        ax.set_title(f"rotation number {m}/{k}\nperimeter $= {perim:.6f}$", fontsize=11)
    fig.savefig("figures/poncelet.png")
    plt.close(fig)


def fig_phase():
    cmap = LinearSegmentedColormap.from_list("caustic", [TEAL, "#c9d6df", ORBIT])
    fig, ax = plt.subplots(figsize=(10, 5.2))
    top = np.array([0.0, E.b])
    prods, coords = [], []
    for p0 in np.linspace(-0.985, 0.985, 46):
        d = np.array([p0, -np.sqrt(1 - p0**2)])
        points, dirs = simulate(E, top, d, 700)
        coords.append(phase_coords(E, points, dirs))
        prods.append(E.focal_product(top, d))
    norm = TwoSlopeNorm(vmin=min(prods), vcenter=0.0, vmax=max(prods))
    for (phi, p), c in zip(coords, prods):
        ax.plot(phi, p, ",", color=cmap(norm(c)), alpha=0.9, rasterized=True)
        ax.scatter(phi, p, s=0.6, color=cmap(norm(c)), lw=0, rasterized=True)
    # separatrix: directions pointing at a focus (d1d2 = 0)
    phis = np.linspace(0, 2 * np.pi, 800)
    wall = np.column_stack([E.a * np.cos(phis), E.b * np.sin(phis)])
    for k, F in enumerate(E.foci):
        d = F - wall
        d /= np.linalg.norm(d, axis=1)[:, None]
        _, p = phase_coords(E, wall, d)
        ax.plot(phis, p, color=CAUSTIC, lw=1.1, zorder=5,
                label="aimed at a focus ($d_1d_2 = 0$)" if k == 0 else None)
    ax.set_xlim(0, 2 * np.pi)
    ax.set_ylim(-1, 1)
    ax.set_xticks(np.arange(5) * np.pi / 2)
    ax.set_xticklabels(["$0$", "$\\pi/2$", "$\\pi$", "$3\\pi/2$", "$2\\pi$"])
    ax.set_xlabel("position on the wall: eccentric angle $\\varphi$")
    ax.set_ylabel("$p = \\cos(\\text{angle with tangent})$")
    ax.set_title("Phase portrait: every orbit lies on one curve $d_1d_2=$ const")
    sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    cb = fig.colorbar(sm, ax=ax, pad=0.015, fraction=0.035)
    cb.set_label("$d_1d_2$   (> 0 ellipse caustic, < 0 hyperbola)")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), frameon=False, fontsize=9.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.savefig("figures/phase.png")
    plt.close(fig)


def fig_conservation():
    fig, ax = plt.subplots(figsize=(8, 3.4))
    for d, c, name in [((-1.0, 0.3), ORBIT, "ellipse caustic"),
                       ((-1.0, -1.0), CAUSTIC, "hyperbola caustic (warm-up)")]:
        points, dirs = simulate(E, [np.sqrt(2), 1.0], d, 5000)
        prods = np.array([E.focal_product(P, v) for P, v in zip(points, dirs)])
        err = np.abs(prods - prods[0])
        ax.semilogy(np.arange(1, len(err)), err[1:] + 1e-17, color=c, lw=0.6, label=name)
    ax.axhline(np.finfo(float).eps, color=MUTED, lw=0.8, ls="--")
    ax.text(5000, np.finfo(float).eps * 1.6, "machine precision", ha="right",
            fontsize=9, color=MUTED)
    ax.set_xlabel("bounce number $k$")
    ax.set_ylabel("$|d_1d_2(k) - d_1d_2(0)|$")
    ax.set_ylim(1e-17, 1e-11)
    ax.set_title("$d_1d_2$ is conserved to rounding error over 5000 bounces")
    ax.legend(frameon=False, fontsize=9.5)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.savefig("figures/conservation.png")
    plt.close(fig)


def fig_deformed_phase():
    from deformed import Table, lyapunov
    cases = [0.0, -0.01, -0.1, -0.3, -0.7, 1.0]
    fig, axes = plt.subplots(2, 3, figsize=(13, 6.6), sharex=True, sharey=True)
    p0 = np.linspace(-0.97, 0.97, 33)
    psi0 = np.concatenate([np.full(33, np.pi / 2), np.full(33, 0.02)])
    alpha0 = np.arccos(np.concatenate([p0, p0]))
    for ax, eps in zip(axes.flat, cases):
        table = Table(E.a, E.b, eps)
        lam, _ = lyapunov(table, psi0, alpha0, 1500)
        chaotic = lam > 0.05
        psi, alpha = psi0.copy(), alpha0.copy()
        pts_psi, pts_p = [], []
        for _ in range(1200):
            psi, alpha = table.step(psi, alpha)
            pts_psi.append(psi)
            pts_p.append(np.cos(alpha))
        pts_psi, pts_p = np.array(pts_psi), np.array(pts_p)
        ax.scatter(pts_psi[:, chaotic].ravel(), pts_p[:, chaotic].ravel(), s=0.25,
                   color=CAUSTIC, alpha=0.35, lw=0, rasterized=True)
        ax.scatter(pts_psi[:, ~chaotic].ravel(), pts_p[:, ~chaotic].ravel(), s=0.25,
                   color=ORBIT, lw=0, rasterized=True)
        ax.set_title(f"$\\varepsilon = {eps:g}$" + ("  (ellipse)" if eps == 0 else ""), fontsize=12)
        ax.set_xlim(0, 2 * np.pi)
        ax.set_ylim(-1, 1)
        ax.set_xticks(np.arange(5) * np.pi / 2)
        ax.set_xticklabels(["$0$", "$\\pi/2$", "$\\pi$", "$3\\pi/2$", "$2\\pi$"])
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    for ax in axes[1]:
        ax.set_xlabel("polar angle $\\psi$ of the bounce point")
    for ax in axes[:, 0]:
        ax.set_ylabel("$p = \\cos\\alpha$")
    fig.suptitle("Phase portraits of $u + v + \\varepsilon uv = 1$: regular orbits (blue) "
                 "and chaotic orbits (red, Lyapunov exponent $> 0.05$)", fontsize=12.5, y=1.0)
    fig.tight_layout()
    fig.savefig("figures/deformed_phase.png")
    plt.close(fig)


def fig_chaos():
    from deformed import Table
    data = np.load("results/sweep.npz")
    eps, ftle, drift = data["eps"], data["ftle"], data["drift"]
    frac = (ftle > 0.05).mean(axis=1)
    err = np.sqrt(frac * (1 - frac) / ftle.shape[1])

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12.5, 4.3),
                                   gridspec_kw={"width_ratios": [1, 1.7]})
    cmap = LinearSegmentedColormap.from_list("eps", [TEAL, INK, CAUSTIC])
    shown = [-0.95, -0.7, -0.3, 0.0, 1.0, 2.9]
    for e in shown:
        P = Table(E.a, E.b, e).point(T)
        col = INK if e == 0 else cmap((e + 1) / 4)
        ax0.plot(P[:, 0], P[:, 1], color=col, lw=2.2 if e == 0 else 1.2,
                 label=f"$\\varepsilon = {e:g}$" + (" (ellipse)" if e == 0 else ""))
    ax0.plot([-E.a, E.a, E.a, -E.a, -E.a], [-E.b, -E.b, E.b, E.b, -E.b], color=MUTED,
             lw=0.9, ls="--", label="$\\varepsilon \\to -1$ (rectangle)")
    ax0.set_aspect("equal")
    ax0.axis("off")
    ax0.legend(loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False, fontsize=9.5)
    ax0.set_title("tables $\\frac{x^2}{4} + \\frac{y^2}{2} + \\varepsilon\\,\\frac{x^2y^2}{8} = 1$")

    ax1.errorbar(eps, frac, yerr=2 * err, fmt="o-", color=CAUSTIC, ms=4, lw=1.3, capsize=2)
    for x, txt in [(0, "ellipse"), (3, "not convex\nbeyond $\\varepsilon=3$")]:
        ax1.axvline(x, color=MUTED, lw=0.8, ls=":")
    ax1.text(0.04, 0.92, "ellipse\n$\\varepsilon = 0$", color=MUTED, fontsize=9.5)
    for x, txt, dx, ha in [(-0.5, "major-axis orbit\nbecomes stable", -0.04, "right"),
                           (1.0, "minor-axis orbit\nbecomes unstable", 0.04, "left")]:
        ax1.axvline(x, color=TEAL, lw=0.9, ls="--")
        ax1.text(x + dx, 0.3, txt, color=TEAL, fontsize=9, ha=ha)
    ax1.set_xlim(-1, 3.05)
    ax1.set_ylim(0, 1)
    ax1.set_xlabel("deformation $\\varepsilon$")
    ax1.set_ylabel("fraction of phase space that is chaotic")
    ax1.set_title("Chaos appears as soon as $\\varepsilon \\neq 0$")
    for s in ("top", "right"):
        ax1.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig("figures/chaos_fraction.png")
    plt.close(fig)

    # how fast d1d2 stops being conserved
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12, 4.2))
    nz = eps != 0
    for sign, col, name in [(-1, TEAL, "$\\varepsilon < 0$"), (1, CAUSTIC, "$\\varepsilon > 0$")]:
        sel = nz & (np.sign(eps) == sign)
        x = np.abs(eps[sel])
        reg = [np.median(dr[f < 0.01]) if (f < 0.01).sum() >= 30 else np.nan
               for dr, f in zip(drift[sel], ftle[sel])]
        cha = [np.median(dr[f > 0.05]) if (f > 0.05).any() else np.nan
               for dr, f in zip(drift[sel], ftle[sel])]
        ax0.loglog(x, reg, "o-", color=col, ms=4, lw=1.2, label=f"regular orbits, {name}")
        ax0.loglog(x, cha, "s--", color=col, ms=4, lw=1.0, alpha=0.7, label=f"chaotic orbits, {name}")
        ax1.loglog(x, frac[sel], "o-", color=col, ms=4, lw=1.2, label=name)
    small = nz & (np.abs(eps) <= 0.03)
    reg_small = np.array([np.median(dr[f < 0.01]) for dr, f in zip(drift[small], ftle[small])])
    slope, icpt = np.polyfit(np.log(np.abs(eps[small])), np.log(reg_small), 1)
    xs = np.array([1e-3, 3e-2])
    ax0.loglog(xs, np.exp(icpt) * xs**slope, color=INK, lw=0.9, ls=":",
               label=f"fit: slope {slope:.2f}")
    ax0.set_xlabel("$|\\varepsilon|$")
    ax0.set_ylabel("median range of $d_1d_2$ along an orbit")
    ax0.set_title("$d_1d_2$ breaks linearly in $\\varepsilon$ on regular orbits")
    ax0.legend(frameon=False, fontsize=8.5)
    fs = nz & (np.abs(eps) <= 0.03)
    k, c = np.polyfit(np.log(np.abs(eps[fs])), np.log(frac[fs]), 1)
    ax1.loglog(xs, np.exp(c) * xs**k, color=INK, lw=0.9, ls=":", label=f"fit: slope {k:.2f}")
    ax1.set_xlabel("$|\\varepsilon|$")
    ax1.set_ylabel("chaotic fraction")
    ax1.set_title("chaotic fraction for small deformations")
    ax1.legend(frameon=False, fontsize=9.5)
    for ax in (ax0, ax1):
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig("figures/d1d2_breaking.png")
    plt.close(fig)
    print(f"   d1d2 range on regular orbits ~ |eps|^{slope:.3f} for |eps| <= 0.03")


if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    for make in (fig_caustics, fig_proof, fig_poncelet, fig_phase, fig_conservation,
                 fig_deformed_phase, fig_chaos):
        make()
        print("made", make.__name__)
