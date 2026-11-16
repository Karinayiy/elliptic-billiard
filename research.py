"""Section 4 experiments: how chaos appears in the tables u + v + eps*u*v = 1.

For each eps, sample orbits uniformly with respect to the invariant measure
ds dp (s = arclength, p = cos of the angle with the tangent), and measure
  * the finite-time Lyapunov exponent of each orbit,
  * the range of d1d2 (ellipse foci) along each orbit.
Writes results/sweep.npz and results/summary.csv. Run: .venv/bin/python research.py
"""
import os
import time

import numpy as np

from deformed import Table, lyapunov

A, B = 2.0, np.sqrt(2.0)  # the ellipse of 2025 National Paper II Q16
N_ORBITS = 3000
N_STEPS = 3000
CHAOS = 0.05      # FTLE threshold, inside the gap between the two populations
REGULAR = 0.01

EPS = np.array([-0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, -0.03, -0.01, -0.003, -0.001,
                0.0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 2.0, 2.5, 2.9])


def run():
    os.makedirs("results", exist_ok=True)
    rng = np.random.default_rng(2026)
    w, p = rng.uniform(0, 1, N_ORBITS), rng.uniform(-1, 1, N_ORBITS)
    p = np.clip(p, -0.999, 0.999)
    done = {}
    if os.path.exists("results/sweep.npz"):  # reuse eps values already computed
        old = np.load("results/sweep.npz")
        done = {float(e): (f, d) for e, f, d in zip(old["eps"], old["ftle"], old["drift"])}
    ftle, drift, rows = [], [], []
    for eps in EPS:
        t0 = time.time()
        if float(eps) in done:
            lam, rng_d = done[float(eps)]
        else:
            table = Table(A, B, eps)
            psi = table.arclength_sampler()(w)
            lam, rng_d = lyapunov(table, psi, np.arccos(p), N_STEPS, rng=np.random.default_rng(1))
        ftle.append(lam)
        drift.append(rng_d)
        chaotic = lam > CHAOS
        f = chaotic.mean()
        regular = lam < REGULAR
        rows.append((eps, f, np.sqrt(f * (1 - f) / N_ORBITS),
                     np.mean(lam[chaotic]) if chaotic.any() else np.nan,
                     np.median(rng_d[regular]) if regular.any() else np.nan,
                     np.mean((lam >= REGULAR) & (lam <= CHAOS))))
        print(f"eps={eps:+.3f}  chaotic={f:.4f}  mean FTLE(chaotic)={rows[-1][3]:.3f}  "
              f"median d1d2 range (regular)={rows[-1][4]:.2e}  ambiguous={rows[-1][5]:.4f}  "
              f"({time.time() - t0:.0f}s)", flush=True)
    np.savez("results/sweep.npz", eps=EPS, ftle=np.array(ftle), drift=np.array(drift), w=w, p=p)
    with open("results/summary.csv", "w") as fh:
        fh.write("eps,chaotic_fraction,std_error,mean_ftle_chaotic,median_d1d2_range_regular,ambiguous_fraction\n")
        for r in rows:
            fh.write(",".join(f"{x:.6g}" for x in r) + "\n")


if __name__ == "__main__":
    run()
