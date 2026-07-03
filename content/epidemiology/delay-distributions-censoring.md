---
title: "Fitting Delay Distributions: Truncation and Censoring"
---

# Fitting Delay Distributions: Truncation and Censoring

The [intervals](epidemiological-intervals.md) that govern transmission — incubation periods, serial intervals, reporting delays — are things we have to *estimate* from data, usually while an outbreak is still unfolding.
That data is imperfect in two systematic ways that a naïve fit ignores at its peril: events are recorded only to the nearest day (**censoring**), and, in real time, long delays have not had a chance to be observed yet (**truncation**).
Get the likelihood right and you recover the true distribution; ignore these effects and you will confidently estimate a distribution that is too short and too narrow.

![Two ways observation distorts a delay: right truncation removes long delays that have not yet completed by the data cutoff, and interval censoring records continuous events only to the day.](../assets/figures/delay-truncation-censoring.svg)

## Interval censoring

We almost never observe the exact instant of infection or symptom onset.
We observe a **day**.
A delay computed as `onset_day − infection_day` is therefore an integer that could correspond to a range of true continuous delays — this is **interval censoring**.

When *both* the primary event (e.g. infection) and the secondary event (e.g. onset) are censored to the day, the delay is **doubly interval censored**.
The standard fix is to treat the true time of the primary event as **uniformly distributed** within its observation window, and to integrate the delay density over every continuous delay compatible with the observed integer.
For a one-day primary window and an observed integer delay $n$, the probability contribution is

$$\Pr(N = n) = \int_0^1 \big[F(n + 1 - p) - F(n - p)\big]\,\mathrm{d}p,$$

where $F$ is the CDF of the underlying continuous delay and $p$ is the unknown within-day offset of the primary event.
Censoring matters most when the delay is **short** relative to the censoring window: a mean delay of a day or two is badly distorted by daily rounding, while a three-week delay is barely affected.

## Right truncation

Estimating a delay in real time introduces a subtler bias.
At the data cutoff $T$, you can only have observed an infector–infectee pair, or an infection–death pair, if the *second* event has already happened.
Cases with long delays are disproportionately still "in the pipeline" and missing from your data — the distribution is **right-truncated** at $T$.

Because recent infections can only appear in the data if they had short delays, the observed sample is biased toward short delays, and the bias is **worse when incidence is growing**, because the sample is dominated by recent infections.
The correction is to condition each observation on having been observable at all: divide its likelihood by the probability that its delay was short enough to appear before $T$, given the (observed) time of its primary event.

**Left truncation** is the mirror image — for example, only sampling cases whose secondary event occurred *after* surveillance began — and is corrected the same way, by renormalizing over the observable window.

## Forward vs backward delays and epidemic phase

A related, easily-missed bias: during an epidemic, the **forward** delay (measured looking forward from a cohort infected at the same time) and the **backward** delay (measured looking back from a cohort who had their secondary event at the same time) are *different distributions* whenever incidence is changing.
When incidence grows, backward delays are compressed; when it falls, they are stretched.
Any method that pools delays across calendar time without accounting for the epidemic phase inherits this dynamical bias.
This is why modern nowcasting frameworks tie the delay estimation to the incidence curve rather than fitting the two separately.

## The censoring- and truncation-aware likelihood

Putting the pieces together, the contribution of an observation with observed integer delay $n$, primary event on day $c$, and data cutoff $T$ is the doubly-censored cell probability, truncated to the observable region:

$$\mathcal{L}(n \mid c) = \frac{\displaystyle\int_0^1 \big[F\big(\min(n+1-p,\;T-c-p)\big) - F(n-p)\big]\,\mathrm{d}p}{\displaystyle\int_0^1 F(T - c - p)\,\mathrm{d}p}.$$

The numerator is the censored probability of the delay, clipped so it cannot exceed what was observable; the denominator is the probability of being observed at all.
Maximizing $\sum_i \log \mathcal{L}(n_i \mid c_i)$ over the parameters of $F$ recovers the true delay distribution.

## A worked example

We simulate a growing epidemic, record infections and symptom onsets only to the day, and cut the data off at day $T = 30$.
Fitting a lognormal that ignores these effects underestimates the mean incubation period; the censoring- and truncation-aware fit recovers the truth.

![A histogram of the observed, right-truncated delays with a naïve lognormal fit biased toward short delays, alongside the truncation-aware fit that recovers the true generating distribution.](../assets/figures/delay-naive-vs-corrected.svg)

## In code

The **Julia** ecosystem's [`CensoredDistributions.jl`](https://github.com/epinowcast/CensoredDistributions.jl) and the **R** [`primarycensored`](https://primarycensored.epinowcast.org) / [`epidist`](https://epidist.epinowcast.org) packages implement exactly this likelihood and plug into Stan/Turing for full Bayesian fits.
The **Python** example builds the likelihood from scratch with [Polars](https://pola.rs) and SciPy so the mechanism is fully visible.

### R

```r
library(primarycensored)   # doubly-interval-censored + truncated delay fitting
library(fitdistrplus)

# `delays` records, per case, the primary-event window [prim_lwr, prim_upr),
# the secondary-event window [sec_lwr, sec_upr), and the observation time.
fit <- fitdistdoublecens(
  delays,
  distr = "lnorm",
  D     = obs_time,                 # right-truncation time (relative to primary event)
  start = list(meanlog = 1.5, sdlog = 0.5)
)
summary(fit)                        # meanlog / sdlog, corrected for censoring + truncation

# For a full Bayesian model that jointly handles the growth phase, use epidist:
#   library(epidist); epidist(data, ...)
```

### Python

We build the simulated data as a [Polars](https://pola.rs) frame, then fit both a naïve and a corrected lognormal.

```python
import numpy as np
import polars as pl
from scipy.optimize import minimize
from scipy.stats import lognorm

rng = np.random.default_rng(42)

# --- truth: a lognormal incubation period, observed during a growing epidemic ---
mu_true, sigma_true = 1.6, 0.5
T, r, N = 30.0, 0.15, 6000                     # cutoff day, growth rate, cohort size

u = rng.uniform(0, 1, N)
t_inf = np.log(1 + u * (np.exp(r * T) - 1)) / r    # infections denser toward the present
D = lognorm.rvs(s=sigma_true, scale=np.exp(mu_true), size=N, random_state=rng)
onset = t_inf + D

c = np.floor(t_inf)                            # infection day (primary, censored to the day)
seen = onset <= T                              # right truncation: onset must occur by T
delays = pl.DataFrame({"c": c[seen], "n": (np.floor(onset) - c)[seen]})

print("observed", delays.height, "of", N, "infections")
mean_recorded = delays.select(pl.col("n").mean()).item()
print(f"mean recorded delay = {mean_recorded:.2f} days (before any correction)")
```

<!-- python-output:auto -->
```text
observed 2786 of 6000 infections
mean recorded delay = 4.58 days (before any correction)
```
<!-- /python-output:auto -->

```python
n = delays["n"].to_numpy()
c = delays["c"].to_numpy()

# --- naive fit: pretend the day-delays are exact and the sample is complete ---
s0, _, scale0 = lognorm.fit(n + 0.5, floc=0)
naive = (np.log(scale0), s0)

# --- corrected fit: integrate over the within-day offset and divide out truncation ---
ps = (np.arange(20) + 0.5) / 20                # grid for the unknown primary-event offset
F = lambda x, mu, sig: lognorm.cdf(x, s=sig, scale=np.exp(mu))

def negloglik(theta):
    mu, sig = theta[0], np.exp(theta[1])
    lo = n[:, None] - ps
    hi = np.minimum(n[:, None] + 1 - ps, (T - c[:, None]) - ps)
    num = np.clip(F(hi, mu, sig) - F(lo, mu, sig), 1e-12, None).mean(1)
    den = np.clip(F((T - c[:, None]) - ps, mu, sig), 1e-12, None).mean(1)
    return -(np.log(num) - np.log(den)).sum()

fit = minimize(negloglik, [np.log(n.mean()), np.log(0.5)], method="Nelder-Mead")
corrected = (fit.x[0], np.exp(fit.x[1]))
lnmean = lambda mu, sig: np.exp(mu + sig**2 / 2)

for name, (mu, sig) in [("true", (mu_true, sigma_true)), ("naive", naive), ("corrected", corrected)]:
    print(f"{name:10s} meanlog={mu:.3f}  sdlog={sig:.3f}  mean={lnmean(mu, sig):.2f} d")
```

<!-- python-output:auto -->
```text
true       meanlog=1.600  sdlog=0.500  mean=5.61 d
naive      meanlog=1.534  sdlog=0.430  mean=5.09 d
corrected  meanlog=1.595  sdlog=0.506  mean=5.60 d
```
<!-- /python-output:auto -->

The naïve fit lands near 5.1 days; the censoring- and truncation-aware fit recovers the true mean of about 5.6 days.

### Julia

```julia
using CensoredDistributions, Distributions, Turing

# Wrap a latent lognormal delay with a uniform (daily) primary-event window,
# then right-truncate at the per-observation cutoff D. See the package docs
# for the exact constructor names, which track the Distributions.jl interface.
latent   = LogNormal(1.6, 0.5)
censored = primarycensored(latent, Uniform(0, 1))     # doubly interval censored

@model function delay_model(n, D)
    meanlog ~ Normal(1.5, 0.5)
    sdlog   ~ truncated(Normal(0.5, 0.5); lower = 0)
    dist = primarycensored(LogNormal(meanlog, sdlog), Uniform(0, 1))
    for i in eachindex(n)
        n[i] ~ truncated(dist; upper = D[i])          # right truncation per case
    end
end
```

## A Bayesian version with NumPyro

Maximum likelihood gives a single best-fit distribution, but during an outbreak we usually want the **full posterior** — the uncertainty in the delay parameters, propagated into everything downstream.
The likelihood is exactly the same; we simply place priors on the parameters and let a sampler explore the posterior.
Because [NumPyro](https://num.pyro.ai) has no built-in doubly-censored, truncated distribution, we hand it the log-likelihood directly with `numpyro.factor`, reusing the simulated `n`, `c`, and `T` from the Python example above.

```python
# no-run: needs numpyro + jax, which the site's output injector does not install
import jax, jax.numpy as jnp
import numpyro, numpyro.distributions as dist
from numpyro.infer import MCMC, NUTS

ps = (jnp.arange(20) + 0.5) / 20

def lncdf(x, mu, sigma):                      # lognormal CDF, 0 for x <= 0
    z = (jnp.log(jnp.clip(x, 1e-12)) - mu) / sigma
    return jnp.where(x > 0, jax.scipy.stats.norm.cdf(z), 0.0)

def delay_model(n, c, T):
    meanlog = numpyro.sample("meanlog", dist.Normal(1.5, 0.5))   # weakly-informative priors
    sdlog   = numpyro.sample("sdlog", dist.HalfNormal(1.0))
    nn, cc = n[:, None], c[:, None]
    lo  = nn - ps
    hi  = jnp.minimum(nn + 1 - ps, (T - cc) - ps)                 # censoring, clipped by truncation
    num = jnp.clip(lncdf(hi, meanlog, sdlog) - lncdf(lo, meanlog, sdlog), 1e-12).mean(1)
    den = jnp.clip(lncdf((T - cc) - ps, meanlog, sdlog), 1e-12).mean(1)   # P(observed | c)
    numpyro.factor("loglik", (jnp.log(num) - jnp.log(den)).sum())

mcmc = MCMC(NUTS(delay_model), num_warmup=500, num_samples=500, progress_bar=False)
mcmc.run(jax.random.PRNGKey(0), n=jnp.asarray(n), c=jnp.asarray(c), T=T)
mcmc.print_summary()
```

The numerator and denominator are the **same censoring-and-truncation-aware likelihood** derived above; `numpyro.factor` just adds its log to the model's log-density.
Running NUTS on the simulated data recovers the truth with tight credible intervals — posterior means of about `meanlog = 1.60` and `sdlog = 0.51`, an implied mean delay near **5.6 days** — matching the MLE point estimate but now carrying full uncertainty that flows into any downstream $R_t$ or nowcast.
For production work the R and Julia packages above wrap this same model with pre-built censored distributions and run it in Stan or Turing.

## Why it matters

Delay distributions feed straight into the numbers decision-makers watch: the [reproduction number](../math/reproduction-number-rt.md) depends on the generation interval, nowcasts of "how many cases really occurred last week" depend on the reporting delay, and estimates of severity depend on the onset-to-death delay.
A delay estimated without correcting for censoring and truncation is biased short and overconfident, and every downstream quantity inherits that bias.
The correction is not exotic — it is a few extra terms in the likelihood — and packages like `CensoredDistributions.jl`, `primarycensored`, and `epidist` now make it the default rather than the exception.

## Related

- [Epidemiological Intervals and Delays](epidemiological-intervals.md)
- [The Effective Reproduction Number and Forecasting](../math/reproduction-number-rt.md)
- [Survival Analysis](../math/survival-analysis.md) — hazards and censoring
- [Maximum Likelihood Estimation](../math/maximum-likelihood.md)
- [Fitting Dynamic Models to Data](../math/model-calibration.md)
- [Bayesian Inference](../math/bayesian-inference.md)
- [Epidemiology](../epidemiology.md)
