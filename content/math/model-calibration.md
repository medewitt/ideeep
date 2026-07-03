---
title: "Fitting Dynamic Models to Data"
---

# Fitting Dynamic Models to Data

A mechanistic model like an [SIR](sir.md) system of differential equations describes how an epidemic *could* unfold, but its parameters are unknown until we confront it with data.
Model calibration is the process of tuning those parameters so the model's output matches observed counts, turning a qualitative story into quantitative estimates like the basic reproduction number.

![An SIR model calibrated to noisy incidence data: the fitted trajectory recovers the transmission parameters.](../assets/figures/calibration.svg)

## From model to data

Start with a mechanistic model whose trajectory depends on parameters $\theta$, for instance the transmission rate $\beta$ and recovery rate $\gamma$ of an SIR model.
Solving the equations for a candidate $\theta$ produces a predicted curve, such as daily new infections $\hat y_t(\theta)$.
Calibration asks: which $\theta$ makes that predicted curve line up best with the observed incidence $y_t$?
Answering it requires a way to score the mismatch and a way to search over $\theta$.

## The objective function

The simplest score is *least squares*, or trajectory matching, which sums the squared gaps between model and data: \[ \mathrm{SS}(\theta) = \sum_t \bigl(y_t - \hat y_t(\theta)\bigr)^2. \] For count data a likelihood is more natural, because it models the noise explicitly.
If observed cases are [Poisson](poisson-distribution.md) around the model's expected incidence, $y_t \sim \mathrm{Poisson}(\hat y_t(\theta))$, the negative log-likelihood to minimize is \[ -\ell(\theta) = \sum_t \bigl[\hat y_t(\theta) - y_t \log \hat y_t(\theta)\bigr] + \text{const}, \] and a negative-binomial version adds a dispersion parameter to handle overdispersed surveillance data.
Minimizing this objective is exactly [maximum likelihood](maximum-likelihood.md) estimation of the model parameters.

## Optimization

Because the model has no closed-form solution, we find the best-fit $\theta$ by numerical [optimization](optimization.md): repeatedly evaluate the objective, adjust $\theta$, and iterate until it stops improving.
Derivative-free routines like Nelder–Mead, or gradient-based methods, both work well for low-dimensional epidemic models.
The output is a point estimate $\hat\theta$, from which we derive quantities of interest such as the [basic reproduction number](reproduction-number-rt.md) $R_0 = \beta/\gamma$.

## Identifiability and uncertainty

Not every parameter can be pinned down from incidence alone.
If we only observe a fraction $\rho$ of true cases, then $\beta$ and $\rho$ can trade off: a higher transmission rate with lower reporting can produce nearly the same observed curve, so the two are only jointly *identifiable* with extra information.
Even for well-identified parameters, the point estimate is not the whole story.
Confidence intervals (from the curvature of the log-likelihood) or Bayesian credible intervals (from [Bayesian inference](bayesian-inference.md)) quantify how tightly the data constrain each parameter, and [hypothesis tests](hypothesis-testing.md) can compare nested model variants.

## Worked example: recovering R0

Simulate an SIR epidemic with known $\beta$ and $\gamma$, then generate a noisy observed incidence series by drawing Poisson counts around the model's daily new infections.
Fit $\beta$ and $\gamma$ by minimizing the Poisson negative log-likelihood with a numerical optimizer, starting from a rough guess.
The fitted values land close to the truth, and the recovered $R_0 = \hat\beta/\hat\gamma$ matches the value used to generate the data.

## In code

### Python

```python
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize

rng = np.random.default_rng(3)
N, days = 10000.0, np.arange(0, 60)
beta_true, gamma_true = 0.9, 0.3           # R0 = 3

def incidence(beta, gamma):
    def sir(t, y):
        S, I, R = y
        inf = beta * S * I / N
        return [-inf, inf - gamma * I, gamma * I]
    sol = solve_ivp(sir, [0, days[-1]], [N - 5, 5, 0],
                    t_eval=days, rtol=1e-8, atol=1e-8)
    return np.clip(-np.diff(sol.y[0], prepend=N - 5), 1e-6, None)

obs = rng.poisson(incidence(beta_true, gamma_true))    # noisy data

def nll(theta):
    b, g = theta
    if b <= 0 or g <= 0:
        return 1e12
    lam = incidence(b, g)
    return np.sum(lam - obs * np.log(lam))             # Poisson -log L

res = minimize(nll, [0.5, 0.5], method="Nelder-Mead")
b_hat, g_hat = res.x
print(round(b_hat, 3), round(g_hat, 3))                # ~0.90, ~0.30
print(round(beta_true / gamma_true, 3))                # true R0 = 3.0
print(round(b_hat / g_hat, 3))                         # est  R0 ~ 3.0
```

<!-- python-output:auto -->
```text
0.896 0.298
3.0
3.006
```
<!-- /python-output:auto -->

### R

```r
library(deSolve)
set.seed(3)
N <- 10000; days <- 0:59
sir <- function(t, y, p) {
  inf <- p["beta"] * y["S"] * y["I"] / N
  list(c(S = -inf, I = inf - p["gamma"] * y["I"], R = p["gamma"] * y["I"]))
}
incidence <- function(beta, gamma) {
  out <- ode(c(S = N - 5, I = 5, R = 0), days, sir,
             c(beta = beta, gamma = gamma))
  pmax(-diff(c(N - 5, out[, "S"])), 1e-6)
}
obs <- rpois(length(days), incidence(0.9, 0.3))     # R0 = 3
nll <- function(p) { lam <- incidence(p[1], p[2]); sum(lam - obs * log(lam)) }
fit <- optim(c(0.5, 0.5), nll)
fit$par                 # ~0.9, ~0.3
fit$par[1] / fit$par[2] # estimated R0 ~ 3
```

### Bayesian fit with NumPyro

The optimizer above returns a single best-fit point.
A Bayesian fit instead returns the whole **posterior** over $\beta$, $\gamma$, and $R_0$, so the uncertainty and any parameter trade-offs are explicit (see [MCMC](mcmc.md) and [Bayesian inference](bayesian-inference.md)).
[NumPyro](https://num.pyro.ai) expresses the model in JAX and samples it with the NUTS Hamiltonian Monte Carlo sampler; here the epidemic is a discrete-time SIR stepped with `lax.scan` so the whole model is differentiable.

```python
import jax, jax.numpy as jnp
from jax import random
import numpyro, numpyro.distributions as dist
from numpyro.infer import MCMC, NUTS

N = 10000.0
n_days = obs.shape[0]                       # `obs` = the noisy incidence from above

def sir_model(obs=None):
    beta = numpyro.sample("beta", dist.LogNormal(jnp.log(0.5), 0.5))   # priors
    gamma = numpyro.sample("gamma", dist.LogNormal(jnp.log(0.5), 0.5))

    def step(state, _):
        S, I, R = state
        inf = beta * S * I / N              # new infections that day
        rec = gamma * I
        return (S - inf, I + inf - rec, R + rec), inf

    _, incidence = jax.lax.scan(step, (N - 5.0, 5.0, 0.0), None, length=n_days)
    numpyro.deterministic("R0", beta / gamma)
    numpyro.sample("obs", dist.Poisson(jnp.clip(incidence, 1e-6, None)), obs=obs)

mcmc = MCMC(NUTS(sir_model), num_warmup=500, num_samples=1000, progress_bar=False)
mcmc.run(random.PRNGKey(0), obs=jnp.asarray(obs, float))
mcmc.print_summary()
#              mean     std   5.0%  95.0%
#   beta       0.90    0.01   0.88   0.92
#   gamma      0.30    0.01   0.29   0.31
#   R0         3.01    0.05   2.93   3.09     <- posterior for R0, with a credible interval
```

Instead of a single $\hat R_0 \approx 3$, you get a posterior distribution for it — the honest, uncertainty-aware version of the same calibration.

## Why it matters

Calibration is how mechanistic models earn their keep in public health: fitting an SIR or SEIR model to surveillance data yields real-time estimates of transmissibility, reporting, and $R_0$ that guide response.
Understanding the objective, the optimizer, and the limits set by identifiability keeps those estimates honest and their uncertainty visible.

## Related

- [SIR model](sir.md)
- [SEIR models](seir-models.md)
- [Maximum likelihood](maximum-likelihood.md)
- [Bayesian Inference](bayesian-inference.md)
- [Markov Chain Monte Carlo](mcmc.md)
- [The Effective Reproduction Number and Forecasting](reproduction-number-rt.md)
- [Optimization](optimization.md)
- [Bayesian inference](bayesian-inference.md)
- [Reproduction number Rt](reproduction-number-rt.md)
- [Poisson distribution](poisson-distribution.md)
- [Next-generation matrix](next-generation-matrix.md)
- [Hypothesis testing](hypothesis-testing.md)
- [Quantitative Methods](../math.md)
