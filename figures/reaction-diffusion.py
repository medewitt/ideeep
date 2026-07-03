# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Fisher-KPP traveling wave front in 1D via explicit finite differences."""

import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()

D = 0.1
r = 1.0
L = 60.0
dx = 0.2
dt = 0.01

x = np.arange(0, L + dx, dx)
nx = x.size

# Initial condition: u=1 for x<3 else 0
u = np.where(x < 3, 1.0, 0.0)

snapshot_times = [0, 10, 20, 30, 40]
snapshots = {}

t = 0.0
max_t = max(snapshot_times)
n_steps = int(round(max_t / dt))

# record t=0
snapshots[0] = u.copy()

for step in range(1, n_steps + 1):
    lap = np.empty_like(u)
    lap[1:-1] = (u[2:] - 2 * u[1:-1] + u[:-2]) / dx**2
    # Neumann (zero-flux) boundaries
    lap[0] = (2 * u[1] - 2 * u[0]) / dx**2
    lap[-1] = (2 * u[-2] - 2 * u[-1]) / dx**2

    u = u + dt * (D * lap + r * u * (1 - u))
    t = step * dt

    for st in snapshot_times:
        if st != 0 and abs(t - st) < dt / 2:
            snapshots[st] = u.copy()

fig, ax = plt.subplots(figsize=(10, 6))
for i, st in enumerate(snapshot_times):
    ax.plot(x, snapshots[st], color=PALETTE[i % len(PALETTE)], label=f"t = {st}")

speed = 2 * np.sqrt(r * D)
ax.annotate(f"Wave speed ≈ 2√(rD) ≈ {speed:.2f}",
            xy=(0.55, 0.85), xycoords="axes fraction")

ax.set_xlabel("Position x")
ax.set_ylabel("u(x, t)")
ax.set_title("Fisher-KPP Traveling Front")
ax.legend(title="Time")

save(fig, "assets/figures/reaction-diffusion.svg")
