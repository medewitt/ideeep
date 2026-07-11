# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""The 2001 UK foot-and-mouth epidemic, reimplemented illustratively.

Four panels mirroring the components of Keeling et al. (2001, Science):
  (a) the spatial transmission kernel -- strong local spread with a long fat
      tail of rare long-range "sparks", contrasted with a thin-tailed Gaussian
      kernel that has no sparks;
  (b) a spatial snapshot of one simulated epidemic on a heterogeneous farm
      landscape -- clustered local spread plus a few long-range seedings;
  (c) epidemic curves under four responses (no control, infected-premises
      culling, ring/neighbourhood culling, ring vaccination);
  (d) final epidemic size versus the detection-and-reporting delay for each
      control -- earlier and tighter response is smaller, and the
      decision-to-immunity delay makes vaccination lose to neighbourhood
      culling. Entirely synthetic: no real DEFRA data.
"""
import numpy as np
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE, INK, MUTED

apply_style()

SIDE = 20.0          # landscape side (km)
N = 700              # farms
D0 = 0.4             # kernel local scale (km)
TAIL = 1.5           # kernel tail exponent (heavy -> long-range sparks)
BETA = 0.65          # transmission scaling
LATENT = 5           # incubating days before infectious
INF_CAP = 14         # infectious days before natural removal (no-control)
VACC_DELAY = 7       # decision-to-immunity delay for vaccination


def make_landscape(seed=11):
    """Farms as points; size heterogeneity drives susceptibility and
    infectiousness together (Keeling's farm-size / species heterogeneity)."""
    rng = np.random.default_rng(seed)
    xy = rng.uniform(0, SIDE, size=(N, 2))
    size = rng.lognormal(0.0, 0.7, size=N)
    d = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1))
    K = (1.0 + (d / D0) ** 2) ** (-TAIL)               # fat-tailed kernel
    np.fill_diagonal(K, 0.0)
    return dict(xy=xy, size=size, suscept=size, infect=size, d=d, K=K)


# States: 0 susceptible, 1 incubating, 2 infectious, 3 culled, 4 immune.
def simulate(land, strategy="none", detect_delay=7, ring=1.5,
             days=200, seed=0):
    rng = np.random.default_rng(seed)
    suscept, infect, d, K = (land["suscept"], land["infect"],
                             land["d"], land["K"])
    state = np.zeros(N, dtype=int)
    latent = np.full(N, -1)          # days incubating
    infclock = np.full(N, -1)        # days infectious
    vpend = np.zeros(N, dtype=bool)  # vaccinated, awaiting immunity
    vclock = np.full(N, -1)          # days since vaccinated
    ever = np.zeros(N, dtype=bool)   # ever infected (a "case")
    culled = 0
    incidence = np.zeros(days)
    last_active = 0

    idx = rng.choice(N, size=3, replace=False)         # index cases
    state[idx] = 2
    infclock[idx] = 0
    ever[idx] = True

    for day in range(days):
        infectious = np.where(state == 2)[0]
        # 1. transmission -> susceptibles (incl. vaccinees awaiting immunity)
        if infectious.size:
            foi = BETA * suscept * (K[:, infectious] @ infect[infectious])
            new = (state == 0) & (rng.random(N) < 1.0 - np.exp(-foi))
            state[new] = 1
            latent[new] = 0
            ever[new] = True
            vpend[new] = False                          # infection pre-empts
            incidence[day] = new.sum()
        # 2. detection + response (farm detected detect_delay days after I)
        for src in np.where((state == 2) & (infclock == detect_delay))[0]:
            if strategy in ("ip", "ring", "vacc") and state[src] != 3:
                state[src] = 3
                culled += 1
            if strategy == "ring":
                near = np.where((d[src] <= ring) & (state != 3))[0]
                culled += near.size
                state[near] = 3
            elif strategy == "vacc":
                vac = np.where((d[src] <= ring) & (state == 0) & ~vpend)[0]
                vpend[vac] = True
                vclock[vac] = 0
        # 3. vaccinees reach immunity
        matured = vpend & (vclock >= VACC_DELAY)
        state[matured] = 4
        vpend[matured] = False
        # 4. no-control: infectious removed after a capped infectious period
        if strategy == "none":
            done = (state == 2) & (infclock >= INF_CAP)
            state[done] = 3
        # 5. progression E -> I
        prog = (state == 1) & (latent >= LATENT)
        state[prog] = 2
        infclock[prog] = 0
        # 6. advance clocks
        latent[state == 1] += 1
        infclock[state == 2] += 1
        vclock[vpend] += 1
        if (state == 1).any() or (state == 2).any():
            last_active = day
        else:
            break

    return dict(incidence=incidence, state=state, ever=ever,
                cases=int(ever.sum()), culled=culled, duration=last_active)


STRATS = [("none", "no control", PALETTE[3]),
          ("ip", "IP culling", PALETTE[0]),
          ("vacc", "ring vaccination", PALETTE[4]),
          ("ring", "ring culling", PALETTE[2])]


if __name__ == "__main__":
    land = make_landscape(seed=11)
    fig, axes = plt.subplots(2, 2, figsize=(11.4, 8.2))
    (axa, axb), (axc, axd) = axes

    # --- (a) the kernel ----------------------------------------------------
    dd = np.linspace(0.01, 12, 400)
    fat = (1.0 + (dd / D0) ** 2) ** (-TAIL)
    gauss = np.exp(-0.5 * (dd / 1.0) ** 2)
    axa.semilogy(dd, fat / fat[0], color=PALETTE[1], lw=2.3,
                 label="fat-tailed (local + sparks)")
    axa.semilogy(dd, gauss, color=PALETTE[0], lw=1.8, ls="--",
                 label="thin-tailed Gaussian")
    axa.set_ylim(1e-4, 1.6)
    axa.set_xlabel("distance between farms (km)")
    axa.set_ylabel(r"relative transmission $K(d)$")
    axa.set_title("(a) Spatial transmission kernel")
    axa.legend(fontsize=8, loc="upper right")
    axa.annotate("long tail =\nrare long-range sparks", xy=(8.5, 6e-3),
                 xytext=(3.4, 2.2e-3), fontsize=8, color=MUTED,
                 arrowprops=dict(arrowstyle="->", color=INK))

    # --- (b) spatial snapshot (ring culling, baseline) ---------------------
    snap = simulate(land, strategy="ring", detect_delay=4, seed=4)
    xy = land["xy"]
    ms = 6 + 26 * (land["size"] / land["size"].max())
    sus = snap["state"] == 0
    axb.scatter(xy[sus, 0], xy[sus, 1], s=ms[sus], c="#c9d2da",
                edgecolors="none", label="never infected")
    inf = snap["ever"]
    axb.scatter(xy[inf, 0], xy[inf, 1], s=ms[inf], c=PALETTE[1],
                edgecolors=INK, linewidths=0.3, label="infected farm")
    axb.set_title("(b) One epidemic on a heterogeneous landscape")
    axb.set_xlabel("km");  axb.set_ylabel("km")
    axb.set_xlim(0, SIDE); axb.set_ylim(0, SIDE)
    axb.set_aspect("equal")
    axb.legend(fontsize=8, loc="upper right", markerscale=0.9)

    # --- (c) epidemic curves by strategy -----------------------------------
    for strat, label, col in STRATS:
        res = simulate(land, strategy=strat, detect_delay=4, seed=4)
        inc = res["incidence"]
        end = min(res["duration"] + 8, len(inc))
        axc.plot(np.arange(end), inc[:end], color=col, lw=2.0,
                 label=f"{label} (cases={res['cases']}, "
                       f"culled={res['culled']})")
    axc.set_title("(c) Epidemic curves by response")
    axc.set_xlabel("day"); axc.set_ylabel("new infected farms / day")
    axc.legend(fontsize=7.6, loc="upper right")

    # --- (d) final size vs detection delay ---------------------------------
    delays = np.array([1, 3, 5, 7, 10, 14])
    reps = 12
    for strat, label, col in STRATS:
        if strat == "none":
            continue
        means = []
        for dl in delays:
            vals = [simulate(land, strategy=strat, detect_delay=int(dl),
                             seed=100 + r)["cases"] for r in range(reps)]
            means.append(np.mean(vals))
        axd.plot(delays, means, "o-", color=col, lw=2.0, ms=5, label=label)
    nc = np.mean([simulate(land, strategy="none", seed=100 + r)["cases"]
                  for r in range(reps)])
    axd.axhline(nc, color=PALETTE[3], lw=1.4, ls=":", label="no control")
    axd.set_title("(d) Slower detection $\\Rightarrow$ larger epidemic")
    axd.set_xlabel("detection + reporting delay (days)")
    axd.set_ylabel("final epidemic size (farms)")
    axd.legend(fontsize=7.6, loc="lower right")

    fig.suptitle("Foot-and-mouth 2001: heterogeneous spatial spread and the "
                 "speed of response", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    save(fig, "assets/figures/foot-and-mouth-2001.svg")
