# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "scipy"]
# ///
"""Calibrating an SIR model to noisy incidence data."""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from _style import apply_style, save, PALETTE

apply_style()
rng = np.random.default_rng(3)

N = 10000.0
beta_true, gamma_true = 0.9, 0.3        # R0 = 3
days = np.arange(0, 60)


def incidence(beta, gamma):
    """New infections per day from the SIR model (reporting the S->I flux)."""
    def sir(t, y):
        S, I, R = y
        inf = beta * S * I / N
        return [-inf, inf - gamma * I, gamma * I]
    sol = solve_ivp(sir, [0, days[-1]], [N - 5, 5, 0],
                    t_eval=days, rtol=1e-8, atol=1e-8)
    S = sol.y[0]
    new = -np.diff(S, prepend=N - 5)     # daily new infections
    return np.clip(new, 1e-6, None)


mean_inc = incidence(beta_true, gamma_true)
obs = rng.poisson(mean_inc)              # noisy observed counts


def neg_loglik(theta):
    beta, gamma = theta
    if beta <= 0 or gamma <= 0:
        return 1e12
    lam = incidence(beta, gamma)
    return np.sum(lam - obs * np.log(lam))   # Poisson negative log-likelihood


res = minimize(neg_loglik, x0=[0.5, 0.5], method="Nelder-Mead")
beta_hat, gamma_hat = res.x
R0_true = beta_true / gamma_true
R0_hat = beta_hat / gamma_hat

print(f"beta : true {beta_true:.3f}  est {beta_hat:.3f}")
print(f"gamma: true {gamma_true:.3f}  est {gamma_hat:.3f}")
print(f"R0   : true {R0_true:.3f}  est {R0_hat:.3f}")

fig, ax = plt.subplots()
ax.scatter(days, obs, s=16, color=PALETTE[1], alpha=0.7, label="observed incidence")
ax.plot(days, incidence(beta_hat, gamma_hat), color=PALETTE[0], lw=2, label="fitted model")
ax.set_xlabel("time (days)")
ax.set_ylabel("new infections / day")
ax.set_title("SIR calibrated to noisy incidence")
ax.annotate(f"$R_0$ true = {R0_true:.2f}\n$R_0$ est = {R0_hat:.2f}",
            xy=(0.62, 0.72), xycoords="axes fraction",
            fontsize=10, color="#26323f")
ax.legend(loc="upper right")
save(fig, "assets/figures/calibration.svg")
