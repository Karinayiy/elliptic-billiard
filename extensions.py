"""Follow-up experiments for the open questions of the paper.

A. Robustness: does the chaotic fraction depend on the orbit length or the FTLE threshold?
B. Aspect ratio: how does the small-eps constant C in  fraction ~ C|eps|  depend on b/a?
C. Near the rectangle: what happens to the chaotic fraction as eps -> -1?

Writes results/ext_*.npz. Run all parts in parallel:
  for p in A0 A1 A2 A3 B0 B1 B2 B3 B4 C; do .venv/bin/python extensions.py $p & done; wait
"""
import os
import time

import numpy as np

from deformed import Table, lyapunov

A_MAJOR = 2.0
CHAOS = 0.05


def sample(n, seed=2026):
    rng = np.random.default_rng(seed)
    w, p = rng.uniform(0, 1, n), np.clip(rng.uniform(-1, 1, n), -0.999, 0.999)
    return w, p


def run_one(a, b, eps, n_orbits, n_steps):
    t0 = time.time()
    table = Table(a, b, eps)
    w, p = sample(n_orbits)
    lam, drift = lyapunov(table, table.arclength_sampler()(w), np.arccos(p), n_steps,
                          rng=np.random.default_rng(1))
    print(f"  b/a={b / a:.4f} eps={eps:+.4f} N={n_steps}: chaotic={np.mean(lam > CHAOS):.4f} "
          f"({time.time() - t0:.0f}s)", flush=True)
    return lam, drift


RATIOS = np.array([0.5, 0.6, 1 / np.sqrt(2), 0.8, 0.9])
ASP_EPS = np.array([-0.03, -0.01, -0.003, 0.003, 0.01, 0.03])
ROB_EPS = np.array([-0.1, 0.01, 0.1, 1.0])
ROB_STEPS = np.array([1000, 3000, 10000])
RECT_EPS = np.array([-0.95, -0.98, -0.99, -0.995, -0.999])


def part(name):
    """Each part runs in its own process and writes results/ext_<name>.npz."""
    if name.startswith("A"):  # robustness, one eps per process
        i = int(name[1:])
        ftle = np.array([run_one(A_MAJOR, np.sqrt(2), ROB_EPS[i], 1000, n)[0] for n in ROB_STEPS])
        np.savez(f"results/ext_{name}.npz", eps=ROB_EPS[i], steps=ROB_STEPS, ftle=ftle)
    elif name.startswith("B"):  # aspect ratio, one ratio per process
        i = int(name[1:])
        res = [run_one(A_MAJOR, A_MAJOR * RATIOS[i], e, 2000, 3000) for e in ASP_EPS]
        np.savez(f"results/ext_{name}.npz", ratio=RATIOS[i], eps=ASP_EPS,
                 ftle=np.array([r[0] for r in res]), drift=np.array([r[1] for r in res]))
    elif name == "C":  # near the rectangle
        ftle = np.array([run_one(A_MAJOR, np.sqrt(2), e, 2000, 3000)[0] for e in RECT_EPS])
        np.savez("results/ext_C.npz", eps=RECT_EPS, ftle=ftle)


if __name__ == "__main__":
    import sys
    os.makedirs("results", exist_ok=True)
    for name in sys.argv[1:]:
        part(name)
