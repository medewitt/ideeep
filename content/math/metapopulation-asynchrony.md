---
title: "Asynchrony and the Inflationary Effect in Metapopulations"
---

# Asynchrony and the Inflationary Effect in Metapopulations

A population, or a pathogen, that cannot sustain itself anywhere can nonetheless thrive everywhere.
Two features of patchy, fluctuating landscapes make this possible: variation through *time*, which can *inflate* the abundance of an immigration-fed sink far above its deterministic value, and variation through *space*, whose *asynchrony* lets a patch at its peak rescue a neighbour that has just crashed.
(A **source** is a patch that more than replaces itself and exports the surplus; a **sink** is one that cannot replace itself and would dwindle to nothing without immigrants arriving from elsewhere.)
The same mathematics governs a beetle in a scatter of habitat fragments and measles in a network of towns, and it carries a sharp warning for disease control: keeping the *average* reproduction number below one, patch by patch, need not eliminate an infection.

![The inflationary effect in an immigration-fed sink: when the local growth rate fluctuates around a sub-replacement mean with positive temporal autocorrelation (reddened noise), abundance breaks out in outbreaks and the long-run mean sits well above the deterministic baseline, whereas white noise of the same variance leaves the mean unchanged.](../assets/figures/inflation-outbreak.svg)

## Two faces of spatiotemporal variation

A [metapopulation](metapopulations.md) is a set of local populations on discrete patches, coupled by dispersal.
Classical theory à la Levins asks only whether patches are occupied; here we care about *how many* individuals — or infections — each patch holds, and how that number is shaped by variation.

Call the local per-generation multiplier $\lambda_t$: a patch with abundance $N_t$ produces $\lambda_t N_t$ locally next generation, plus a steady trickle of immigrants $I$ from elsewhere. \[ N_{t+1} = \lambda_t\,N_t + I. \] A patch is a **sink** when its mean growth rate is sub-replacement, $\bar\lambda < 1$: left alone it dwindles to nothing, and only immigration keeps it populated.
In a *constant* environment the sink settles at the deterministic equilibrium $N^\* = I/(1-\bar\lambda)$ — set $N_{t+1}=N_t$ and solve.

Real environments are not constant, and the variation comes along two axes that this page treats in turn.
Along the **time** axis, $\lambda_t$ rises and falls from one generation to the next, and whether the good and bad spells *cluster* — their temporal autocorrelation — turns out to control the mean abundance.
Along the **space** axis, different patches peak and trough at different times, and whether their fluctuations line up — their synchrony — controls regional persistence.
The surprise is that these two axes pull in opposite directions: *positive autocorrelation in time inflates and stabilises*, while *positive correlation across space destabilises*.

## The inflationary effect

Start with a single sink and ask what temporal variation does to its long-run mean.
Iterating the recursion from the infinite past collects every past immigrant, discounted by the string of growth rates it has survived since arriving: \[ N_t = I\sum_{k\ge 0}\ \prod_{j=1}^{k}\lambda_{t-j}, \qquad \mathbb{E}[N_t] = I\sum_{k\ge 0}\ \mathbb{E}\!\left[\prod_{j=1}^{k}\lambda_{t-j}\right]. \] Everything hinges on that expected product of growth rates.

**White noise does not inflate the mean.** If the $\lambda_t$ are independent and identically distributed, the expectation of the product is the product of the expectations, $\mathbb{E}\!\left[\prod \lambda\right]=\bar\lambda^{\,k}$, and the series collapses back to the deterministic value: \[ \mathbb{E}[N] = I\sum_{k\ge 0}\bar\lambda^{\,k} = \frac{I}{1-\bar\lambda} = N^\*. \] Independent good and bad years cancel, and the average abundance is exactly what you would have predicted by plugging in the mean growth rate.

**Positive autocorrelation does.** When good years tend to follow good years — a *reddened* or positively autocorrelated environment — the growth rates in a product are positively correlated, so \[ \mathbb{E}\!\left[\prod_{j=1}^{k}\lambda_{t-j}\right] > \bar\lambda^{\,k}, \] because the expectation of a product of positively correlated positive quantities exceeds the product of their means.
Every term in the series is inflated, so the long-run mean rises above $N^\*$: \[ \mathbb{E}[N] > \frac{I}{1-\bar\lambda}. \] This is the **inflationary effect** of [Gonzalez & Holt (2002)](https://doi.org/10.1073/pnas.232589299), extended to networks of coupled sinks by [Roy, Holt & Barfield (2005)](https://doi.org/10.1086/431286).

The mechanism is [Jensen's inequality](jensens-inequality.md) wearing temporal clothes.
Population growth is *multiplicative*, and multiplicative accumulation is a convex function of a run of good years: a spell of $\lambda>1$ lets abundance build super-linearly, while a spell of $\lambda<1$ can only take it down to — never below — the floor that immigration keeps propped up.
Autocorrelation lengthens those runs, so the convex upside (an outbreak) is amplified far more than the concave downside is deepened.
The immigration term $I$ is the *storage* that makes this asymmetry pay: it refills the patch between outbreaks so there is always a base for the next good run to multiply, exactly the role that a seed bank or a refuge plays in the storage effect.
The signature, visible in the lead figure, is a **reddened outbreak pattern** — long quiescent stretches near the immigration floor, punctuated by sharp eruptions when a lucky run of good years compounds.

### How big is the inflation?

The size of the effect grows with the *variance* of the environment and with the *autocorrelation* $\rho$, and it is cleanest to see in an exactly solvable "good year / bad year" model.
Let the environment be a symmetric two-state [Markov chain](markov-chains.md): a good state with $\lambda_H$ and a bad state with $\lambda_L$, each occupied half the time, with probability $p$ of staying put each generation.
The lag-one autocorrelation of the growth rate is then $\rho = 2p-1$, tuning smoothly from white noise ($p=\tfrac12$, $\rho=0$) to a highly persistent environment ($p\to 1$, $\rho\to 1$).
Solving the stationary mean of $N_{t+1}=\lambda_{s_t}N_t + I$ (a $2\times2$ linear system, below) gives the curve of mean abundance against autocorrelation.

![Long-run mean abundance versus the temporal autocorrelation of the growth rate, from the exact two-state model with mean growth rate 0.8 and immigration 10. Mean abundance climbs above the deterministic baseline of 50 as autocorrelation increases, and the larger the environmental amplitude the steeper the climb — diverging at a persistence threshold where the coupled-sink system becomes self-sustaining.](../assets/figures/inflation-autocorrelation.svg)

Two things stand out.
First, inflation accelerates: with a large-amplitude environment ($\lambda$ swinging between 0.4 and 1.2, mean 0.8) an autocorrelation of only $\rho=0.5$ already triples the mean, from 50 to 150.
Second, there is a **persistence threshold**.
As $\rho$ rises the mean diverges at a finite $\rho^\*$ (here $\approx 0.62$): beyond it the runs of good years are long enough that the population sustains itself *without* immigration, and the whole metapopulation of coupled sinks flips from immigration-dependent to self-perpetuating.
This is the [Roy, Holt & Barfield (2005)](https://doi.org/10.1086/431286) result — temporal autocorrelation, not just variance, can let a network of sinks persist indefinitely on its own.

### Inflation is a covariance in time

The product argument has an exact closed form that names the mechanism outright.
Time-averaging the sink recursion $N_{t+1}=R_t N_t + I_t$ (writing the growth rate as $R_t$ and allowing immigration $I_t$ to vary) and rearranging gives the [Roy, Holt & Barfield (2005)](https://doi.org/10.1086/431286) identity (their eq. 2), \[ \bar N \;=\; \frac{\operatorname{Cov}_t(R,\,N) \;+\; \bar I}{1-\bar R}, \] where overbars denote time-averages and $\operatorname{Cov}_t(R,N)$ is the **temporal covariance** between the growth rate and the abundance in the patch.
When the growth rates are independent from one generation to the next, $\operatorname{Cov}_t(R,N)=0$ and the mean collapses to the deterministic $\bar I/(1-\bar R)$: in this discrete accounting, uncorrelated variation alone leaves the arithmetic mean untouched.
Positive autocorrelation makes the patch densest exactly when it is growing fastest — a positive $\operatorname{Cov}_t(R,N)$ — and *that covariance is the inflation*.
The proper "sink" condition in discrete time is that the *geometric* mean of $R_t$ is below one, equivalently the stochastic growth rate $\mathbb{E}[\ln R]<0$; a patch can have geometric-mean growth below replacement — doomed if closed — yet an arithmetic-mean abundance inflated well above $\bar I/(1-\bar R)$.
(In continuous time the counterpart is [Gonzalez & Holt's (2002)](https://doi.org/10.1073/pnas.232589299) harmonic-mean identity: the harmonic mean of a fluctuating sink's abundance equals its constant-environment equilibrium $N^\*$, so the arithmetic mean is always at least $N^\*$ — but in both settings the large inflation, the outbreaks, is carried by positively autocorrelated runs of good years.)

## Asynchrony and rescue

Now hold time fixed and look across space.
Suppose each town runs its own recurrent epidemic, and each town on its own is below the **critical community size** — the population, first estimated by [Bartlett (1957)](https://doi.org/10.2307/2342553) at around 250,000–500,000 for measles, below which the infection troughs to zero cases between epidemics and fades out by chance.
Whether the *region* keeps the pathogen alive depends entirely on how the local epidemics are phased relative to one another.

![A stochastic TSIR (measles-type) metapopulation of five small towns, each below the critical community size. When local epidemics are synchronous their troughs align, the pathogen fades out everywhere at once and the region goes extinct. When they are asynchronous, a town at its epidemic peak reseeds a neighbour that has just faded out — the rescue effect — and the pathogen persists regionally.](../assets/figures/metapop-asynchrony.svg)

When the towns are **synchronous** (left), their epidemics crest and crash together.
Every few years the whole region passes through a deep collective trough, and because *all* the local case counts hit zero at the same moment, there is no reservoir left to reignite anyone: the pathogen fades out globally, and the region's large *total* population counts for nothing.
When the towns are **asynchronous** (right), the troughs are staggered.
At the moment one town's chain of transmission flickers out, another is at its epidemic peak, and a handful of infected travellers reseed the faded town before its susceptibles have piled up in vain — the **rescue effect**.
The pathogen bounces around the network indefinitely even though no single town could hold it, exactly the "cities and villages" picture of measles persistence from [Bolker & Grenfell (1995)](https://doi.org/10.1098/rstb.1995.0070) and [Grenfell & Bolker (1998)](https://doi.org/10.1046/j.1461-0248.1998.00016.x).

Asynchrony is, in a sense, the spatial twin of the inflationary effect: both let coupling plus variation sustain something that local dynamics alone cannot.
But note the reversal of sign.
In *time*, positive autocorrelation (persistence of good spells) *helps* the population.
In *space*, positive correlation (synchrony of patches) *hurts* it, because synchrony removes the out-of-phase reservoir that rescue depends on.
This is why [Earn, Rohani & Grenfell (1998)](https://doi.org/10.1098/rspb.1998.0256) could argue that anything which *synchronises* epidemics — strong shared seasonal forcing, or coordinated control — raises the risk of global fadeout, a lever that works *for* elimination rather than against it.
The converse is a genuine trap for control: [Bolker & Grenfell (1996)](https://doi.org/10.1073/pnas.93.22.12648) showed that mass vaccination can *decorrelate* previously synchronised city epidemics, and that this vaccine-induced asynchrony *lessens* the chance of global extinction — so a programme can lower incidence everywhere yet make the pathogen harder to eradicate by scattering its epidemics out of phase.

## Measuring asynchrony

To turn these pictures into numbers, we need to quantify how out-of-phase a set of local time series is.
Three complementary measures do most of the work.

![Measuring asynchrony. Left: the phase picture — each local epidemic is a clock hand, and the length of their vector sum, the Kuramoto order parameter r, measures coherence (r = 1 fully synchronous, r near 0 asynchronous). Right: as local epidemics are spread across the seasonal cycle, both the community synchrony index and the mean pairwise correlation fall from 1 toward their asynchronous floors.](../assets/figures/asynchrony-measures.svg)

**Mean pairwise correlation.** The simplest index averages the zero-lag [correlation](linear-regression.md) of local incidence over all pairs of patches, $\bar\rho = \frac{1}{n(n-1)}\sum_{i\ne j}\operatorname{Corr}(x_i, x_j)$.
It runs from $\approx 1$ (synchrony) down toward zero, and can even go slightly negative when epidemics are locked into anti-phase — evenly staggered oscillators of equal amplitude are correlated at exactly $-1/(n-1)$.

**Community synchrony index.** [Loreau & de Mazancourt (2008)](https://doi.org/10.1086/589746) compare the variance of the *aggregate* to the variances of the parts: \[ \varphi = \frac{\operatorname{Var}\!\left(\sum_i x_i\right)}{\left(\sum_i \sigma_i\right)^2}, \qquad \varphi\in\left[\tfrac1n,\,1\right]. \] When patches move in lockstep the aggregate fluctuates as violently as the sum of the parts and $\varphi=1$; when they are perfectly asynchronous their ups and downs cancel in the sum and $\varphi\to 1/n$ (and toward $0$ under anti-phase locking).
The complement $1-\varphi$ is the **statistical-averaging** or **portfolio effect** — the damping of regional fluctuations that spatial asynchrony buys, the same diversification that stabilises a spread-out portfolio.

**Phase coherence.** For cleanly oscillatory epidemics it is natural to extract each series' *phase* $\theta_j(t)$ — via a Hilbert or wavelet transform — and summarise their alignment with the **Kuramoto order parameter** \[ r\,e^{i\psi} = \frac1n\sum_{j=1}^{n} e^{i\theta_j}, \qquad r\in[0,1]. \] Think of each local epidemic as a hand on a clock; $r$ is the length of the resultant when you add the hands as unit vectors.
All hands together give $r=1$ (perfect coherence); hands scattered around the dial give $r\approx 0$ (incoherence), as in the left panel above.

## From $\lambda$ to little $r$ and to $R$: the disease translation

Everything above transfers to epidemics by reading the multiplier $\lambda_t$ as a **reproduction number**.
Over one generation an infection multiplies by its effective reproduction number, so $\lambda_t \leftrightarrow R_t$, the local abundance $N_t$ becomes prevalence or incidence, and the immigration $I$ becomes **importation** — infected travellers arriving through host movement.
A *sink patch* is one that is locally subcritical, $\bar R < 1$: transmission there cannot sustain a chain on its own, and the patch only carries infection because cases keep being imported.

It pays to keep two "growth" quantities distinct, because they answer different questions.
The **epidemic growth rate** is little $r_t = \ln R_t$ (the log per-generation multiplier — see the [effective reproduction number](reproduction-number-rt.md)).
Whether a *closed* pathogen invades and grows is governed not by the arithmetic-mean reproduction number but by the **stochastic growth rate**, the geometric-mean rate \[ r_s = \mathbb{E}[\ln R_t] \ \le\ \ln \mathbb{E}[R_t], \] where the inequality is [Jensen's](jensens-inequality.md) again: temporal variance in $R$ *lowers* the growth rate that decides invasion, so averaging $R$ on its natural scale over-states a fluctuating pathogen's ability to establish.
That is the sense in which "little $r$" — the log-scale, geometric-mean rate — is the honest currency of growth under variation.

The inflationary effect is the complementary, and initially counter-intuitive, half of the story.
It concerns not the growth rate of a closed population but the **standing prevalence of an open, subcritical one**, and there variance plus *positive autocorrelation* plus importation push the long-run mean *up*.
A patch can have $\bar R < 1$, and even a negative stochastic growth rate $r_s < 0$, yet — because seasons of favourable transmission cluster (a reddened $R_t$) and because movement keeps reseeding it — carry a substantial, outbreak-prone burden of infection whose time-average dwarfs the naive $I/(1-\bar R)$.
Couple several such patches and the collective can cross the persistence threshold: the metapopulation sustains the pathogen with a **regional effective reproduction number above one even though every patch is subcritical on average**.
This is the public-health payload of [Kortessis et al. (2025)](https://doi.org/10.1086/733896): spatiotemporal heterogeneity and dispersal can hold an infection in a region that no constituent community could hold, and can do so invisibly to any surveillance that only tracks *average* transmission.

The practical corollary is a warning about thresholds.
An elimination programme that drives the *mean* reproduction number below one in every patch has not necessarily won.
If transmission is temporally autocorrelated (seasonality, weather, behavioural waves) and patches are spatially asynchronous and connected by movement, inflation and rescue can keep the pathogen endemic below the naive threshold.
To anticipate this you measure three things directly: the local reproduction-number time series $R_t$ (from incidence, via the renewal equation), *its temporal autocorrelation* — how reddened the $R_t$ spectrum is — and the *cross-patch synchrony* $\varphi$ or coherence $r$.
High redness and high asynchrony are the fingerprints of a system that will persist below where mean-field intuition says it should collapse — and, read the other way, *synchronising* control across patches (so troughs align) is a way to engineer the global fadeout that eliminates it.

## Growth-rate inflation as a covariance: watching $r$, space, and time

[Kortessis et al. (2025)](https://doi.org/10.1086/733896) fold the temporal and spatial stories into one measurable quantity built directly from local growth rates, and it is worth walking through because it makes "inflation" something you can compute from data rather than assert.
Track the per-capita growth rate of each patch, $r_i(t)$.
For an epidemic this is $r_i(t)=\beta_i(t)\,S_i/N_i-\gamma$ — the **log rate of change of cases**, little $r$ itself — positive while a local outbreak grows and negative once it burns through susceptibles.
Let $\nu_i(t)=N_i(t)/\bar N(t)$ be each patch's density (here, prevalence) relative to the metapopulation average $\bar N=\tfrac1n\sum_j N_j$.

Because movement only shuffles individuals between patches — it conserves the regional total — the growth rate of the *whole* metapopulation decomposes exactly, by the same algebra as the [Price equation](price-equation.md) of evolutionary theory, into a spatial mean plus a spatial covariance:

\[
\frac{1}{\bar N}\frac{d\bar N}{dt} \;=\; \bar r(t) \;+\; \operatorname{cov}_i\!\big(r_i(t),\,\nu_i(t)\big).
\]

The first term is the mean local growth rate across patches; the second — the spatial covariance between a patch's growth rate and its relative density — is the instantaneous inflation.
Whenever individuals are concentrated in the patches that happen to be growing fastest, $\operatorname{cov}_i(r_i,\nu_i)>0$ and the metapopulation grows faster than the average of its patches.

![Four panels from a seasonally forced SIR metapopulation of four out-of-phase patches coupled by movement. A: the local growth rate of cases r_i(t) for each patch, with the spatial mean near zero. B: the covariance in space between growth rate and relative prevalence, which pulses but stays positive — the instantaneous inflationary contribution. C: the covariance in time between growth rate and prevalence, patch by patch, positive everywhere. D: the ANOVA-style decomposition of the variance of r into pure spatial, pure temporal, and spatiotemporal components, dominated by the spatiotemporal term that drives inflation.](../assets/figures/inflation-covariance.svg)

Panel A plots $r_i(t)$ for four seasonally forced, out-of-phase patches; the spatial mean (dashed) hovers near zero, so no single patch is a runaway source.
Panel B is the **covariance in space**, $\operatorname{cov}_i(r_i(t),\nu_i(t))$ evaluated instant by instant: it pulses but stays *positive*, because diffusive movement keeps nudging infections toward whichever patch is currently in its growing season, so growth and density stay aligned.
Panel C is the **covariance in time**, $\operatorname{Cov}_t(r_i,N_i)$, computed patch by patch — the single-sink inflation of Roy et al.'s eq. 2, positive in every patch here because each patch, too, is densest when it is growing.
Panel D is the variance budget, and it is the key to why asynchrony matters.

The variance of any factor $F(x,t)$ that varies across space $x$ and time $t$ splits, ANOVA-style, into three pieces ([Kortessis et al. 2025](https://doi.org/10.1086/733896), box 1):

\[
\operatorname{Var}(F) \;=\; \sigma_S^2 + \sigma_T^2 + \sigma_{ST}^2 .
\]

- **Pure spatial**, $\sigma_S^2=\operatorname{Var}_x(\tilde F_x)$: the variance of the time-averaged spatial pattern — how patches differ on average.
- **Pure temporal**, $\sigma_T^2=\operatorname{Var}_t(\bar F_t)$: the variance of the space-averaged temporal pattern — how the whole landscape moves together.
- **Spatiotemporal**, $\sigma_{ST}^2=\mathbb{E}_t[\operatorname{Var}_x F]-\sigma_S^2$: the remainder — the shifting mosaic in which the ranking of good and bad patches itself changes over time.

Asynchrony *is* $\sigma_{ST}^2$: perfectly synchronised patches share one temporal signal and carry $\sigma_{ST}^2=0$, while asynchronous patches carry a large $\sigma_{ST}^2$.
In the out-of-phase epidemics of the figure almost the entire variance of $r$ is spatiotemporal (panel D), and it is exactly this component — not the spatial or temporal main effects — that the inflationary effect feeds on.

Kortessis et al.'s **inflationary effect** (their eq. 4) is then the time-averaged spatial covariance, measured against a reference environment in which spatiotemporal heterogeneity has been switched off by freezing each patch's growth rate at its own temporal mean $\tilde r_i$:

\[
\text{inflationary effect} \;=\; \mathbb{E}_t\!\big[\operatorname{cov}_i(r_i(t),\nu_i(t))\big] \;-\; \operatorname{cov}_i(\tilde r_i,\,\tilde\nu_i),
\]

where $\tilde\nu_i$ is the relative density the metapopulation would settle into under those frozen growth rates and the same movement.
It is positive when dispersal, averaged over the shifting mosaic, leaves individuals in better-than-average locations — which, for symmetric (fitness-independent) movement that is not too fast, it does.
Subtracting the frozen-growth reference is what isolates the contribution of $\sigma_{ST}^2$: it is the disease analogue of asking how much *extra* transmission the spatiotemporal shuffle buys the pathogen beyond what its fixed geography already provides.

### In code

We simulate the four-patch seasonally forced SIR metapopulation, then read off the covariance in space, the covariance in time, the space/time/spatiotemporal variance budget, and the inflationary effect of equation (4).

```python
import numpy as np
from scipy.integrate import solve_ivp

n, N, gamma, mu = 4, 1.0, 26.0, 1 / 50.0
R0 = 8.0 * (1 + 0.12 * np.linspace(-1, 1, n)); beta0 = R0 * (gamma + mu)
delta = 0.12 * (1 + 0.5 * np.cos(np.linspace(0, np.pi, n)))   # seasonal amplitude per patch
phases = np.linspace(0, 2 * np.pi, n, endpoint=False)         # staggered seasonal phase
m = 2.0                                                        # movement rate of infectives

def rhs(t, y):
    S, I = y[:n], y[n:2 * n]
    b = beta0 * (1 + delta * np.cos(2 * np.pi * t + phases))
    inf = b * S * I / N
    return np.concatenate([mu * N - inf - mu * S,
                           inf - (gamma + mu) * I + m * (I.mean() - I),   # movement conserves total
                           gamma * I - mu * y[2 * n:]])

S0 = np.full(n, 1 / R0.mean()); I0 = 1e-3 * (1 + 0.2 * np.cos(phases))
sol = solve_ivp(rhs, (0, 60), np.concatenate([S0, I0, N - S0 - I0]),
                t_eval=np.linspace(48, 60, 4000), rtol=1e-9, atol=1e-12, method="LSODA")
t, S, I = sol.t, sol.y[:n], sol.y[n:2 * n]

r = beta0[:, None] * (1 + delta[:, None] * np.cos(2 * np.pi * t[None, :] + phases[:, None])) * S / N - gamma
cov_space = (r * I / I.mean(0)).mean(0) - r.mean(0)             # cov_i(r_i, nu_i) at each time
cov_time = np.array([np.cov(r[i], I[i])[0, 1] for i in range(n)])
varS, varT = r.mean(1).var(), r.mean(0).var(); varST = r.var(0).mean() - varS
Aref = np.diag(r.mean(1)) + (m / n) * (np.ones((n, n)) - n * np.eye(n))   # frozen-growth reference
w, V = np.linalg.eig(Aref); nu_ref = V[:, np.argmax(w.real)].real; nu_ref /= nu_ref.mean()
cov_ref = (r.mean(1) * nu_ref).mean() - r.mean(1).mean()

print("cov in space (time-mean) :", round(float(cov_space.mean()), 3),
      " ranges", round(float(cov_space.min()), 2), "to", round(float(cov_space.max()), 2))
print("cov in time (per patch)  :", np.round(cov_time, 5))
print("var(r): space/time/space-time =", round(varS, 2), "/", round(varT, 2), "/", round(varST, 2))
print("inflationary effect (eq.4)   :", round(float(cov_space.mean() - cov_ref), 3))
```

<!-- python-output:auto -->
```text
cov in space (time-mean) : 0.289  ranges 0.05 to 0.6
cov in time (per patch)  : [3.7e-04 2.3e-04 1.1e-04 7.0e-05]
var(r): space/time/space-time = 0.04 / 0.37 / 5.96
inflationary effect (eq.4)   : 0.27
```
<!-- /python-output:auto -->

The covariance in space is positive at all times, the covariance in time is positive in every patch, and the variance of $r$ is overwhelmingly spatiotemporal — so the inflationary effect is positive: the shifting mosaic of out-of-phase outbreaks, sampled by movement, systematically concentrates infection where transmission is momentarily strongest.

### R

```r
# Spatial decomposition of a growth-rate matrix r (rows = patches, cols = time)
# and the abundance/relative-density matrix I. Mirrors the Python above.
cov_space <- colMeans(r * (I / rep(colMeans(I), each = nrow(I)))) - colMeans(r)  # cov_i(r_i, nu_i)(t)
cov_time  <- sapply(seq_len(nrow(r)), function(i) cov(r[i, ], I[i, ]))           # Roy et al. eq. 2
varS <- var(rowMeans(r)); varT <- var(colMeans(r))                              # box 1: space, time
varST <- mean(apply(r, 2, var)) - varS                                          # spatiotemporal
c(cov_space = mean(cov_space), varS = varS, varT = varT, varST = varST)
```

### Julia

```julia
using Statistics, LinearAlgebra
# r, I are (patches × time) matrices from an SIR metapopulation solve
nu        = I ./ mean(I; dims = 1)
cov_space = vec(mean(r .* nu; dims = 1)) .- vec(mean(r; dims = 1))   # cov_i(r_i, nu_i)(t)
cov_time  = [cov(r[i, :], I[i, :]) for i in 1:size(r, 1)]           # Roy et al. eq. 2
varS = var(vec(mean(r; dims = 2)))                                  # box 1: pure spatial
varT = var(vec(mean(r; dims = 1)))                                  # pure temporal
varST = mean(var(r; dims = 1)) - varS                               # spatiotemporal
(mean_cov_space = mean(cov_space), varS = varS, varT = varT, varST = varST)
```

## A worked example

Take a single sink with a good-year growth rate $\lambda_H = 1.2$ (transmission briefly supercritical) and a bad-year rate $\lambda_L = 0.4$, each occurring half the time, so the mean is $\bar\lambda = 0.8 < 1$; immigration is $I = 10$ per generation.
The deterministic prediction is $N^\* = I/(1-\bar\lambda) = 10/0.2 = 50$.

- **No autocorrelation** ($\rho = 0$, good and bad years independent): mean abundance is exactly $50$ — variance alone does nothing to the mean here.
- **Moderate autocorrelation** ($\rho = 0.5$): the mean climbs to $150$, a three-fold inflation, purely because good years now cluster.
- **Stronger autocorrelation** ($\rho = 0.6$): the mean reaches $650$, a thirteen-fold inflation, as the environment nears the persistence threshold $\rho^\* \approx 0.62$ beyond which the sink no longer needs immigration at all.

Read as an epidemic: a town where the reproduction number averages $\bar R = 0.8$ — comfortably "under control" on paper — can carry three-to-thirteen times the case burden a mean-field calculation predicts, and tip into self-sustaining transmission, once favourable-transmission spells cluster in time.

## In code

The exact two-state inflation calculation, and the community synchrony index, are both a few lines.

### Python

```python
import numpy as np

def mean_abundance(lamH, lamL, p, I=10.0):
    """Long-run mean of N_{t+1} = lambda_{s_t} N_t + I under a symmetric two-state
    (good year / bad year) Markov environment: stay-probability p gives lag-1
    autocorrelation rho = 2p - 1. Solves the 2x2 stationary system for the joint
    means u_H, u_L of abundance-in-each-state; the total mean is their sum."""
    A = np.array([[1 - p * lamH, -(1 - p) * lamL],
                  [-(1 - p) * lamH, 1 - p * lamL]])
    uH, uL = np.linalg.solve(A, [I / 2, I / 2])
    return uH + uL

lamH, lamL = 1.2, 0.4               # good year 1.2 (>1), bad year 0.4; mean 0.8 (a sink)
for rho in [0.0, 0.5, 0.6]:
    p = (rho + 1) / 2
    print(f"rho={rho:>3}: mean abundance = {mean_abundance(lamH, lamL, p):6.1f}")
print("deterministic baseline I/(1-lam_bar) =", round(10 / (1 - 0.8), 1))
```

<!-- python-output:auto -->
```text
rho=0.0: mean abundance =   50.0
rho=0.5: mean abundance =  150.0
rho=0.6: mean abundance =  650.0
deterministic baseline I/(1-lam_bar) = 50.0
```
<!-- /python-output:auto -->

```python
import numpy as np

def synchrony_index(x):
    """Loreau & de Mazancourt community synchrony: phi = Var(sum_i x_i) / (sum_i sd_i)^2.
    Rows are time, columns are patches. phi = 1 is lockstep, phi -> 1/n is asynchronous."""
    sd = x.std(axis=0)
    return x.sum(axis=1).var() / sd.sum() ** 2

t = np.arange(0, 20, 0.1)
n = 5
sync = np.stack([1 + np.cos(t) for _ in range(n)], axis=1)                    # identical phase
staggered = np.stack([1 + np.cos(t + 2 * np.pi * i / n) for i in range(n)], axis=1)  # spread phase
print("phi (synchronous)  =", round(float(synchrony_index(sync)), 3))
print("phi (asynchronous) =", round(float(synchrony_index(staggered)), 3))
print("1/n floor          =", round(1 / n, 3))
```

<!-- python-output:auto -->
```text
phi (synchronous)  = 1.0
phi (asynchronous) = 0.0
1/n floor          = 0.2
```
<!-- /python-output:auto -->

### R

```r
# Exact two-state inflation: mean of N_{t+1} = lambda_{s_t} N_t + I
mean_abundance <- function(lamH, lamL, p, I = 10) {
  A <- matrix(c(1 - p * lamH, -(1 - p) * lamH,
                -(1 - p) * lamL, 1 - p * lamL), nrow = 2)
  u <- solve(A, c(I / 2, I / 2))
  sum(u)
}
for (rho in c(0, 0.5, 0.6)) {
  p <- (rho + 1) / 2
  cat(sprintf("rho=%.1f  mean = %.1f\n", rho, mean_abundance(1.2, 0.4, p)))
}

# Community synchrony index phi = Var(row sums) / (sum of column SDs)^2
synchrony_index <- function(x) {
  var(rowSums(x)) / sum(apply(x, 2, sd))^2
}
t <- seq(0, 20, by = 0.1); n <- 5
sync      <- sapply(1:n, function(i) 1 + cos(t))
staggered <- sapply(1:n, function(i) 1 + cos(t + 2 * pi * i / n))
c(sync = synchrony_index(sync), async = synchrony_index(staggered), floor = 1 / n)
```

### Julia

```julia
using LinearAlgebra, Statistics

# Exact two-state inflation
function mean_abundance(lamH, lamL, p; I = 10.0)
    A = [1 - p*lamH   -(1 - p)*lamL;
         -(1 - p)*lamH  1 - p*lamL]
    u = A \ [I/2, I/2]
    sum(u)
end
for rho in (0.0, 0.5, 0.6)
    p = (rho + 1) / 2
    println("rho=$rho  mean = ", round(mean_abundance(1.2, 0.4, p), digits = 1))
end

# Community synchrony index
synchrony_index(x) = var(vec(sum(x, dims = 2))) / sum(std(x, dims = 1))^2
t = 0:0.1:20; n = 5
sync      = hcat([1 .+ cos.(t)               for _ in 1:n]...)
staggered = hcat([1 .+ cos.(t .+ 2π*i/n)     for i in 1:n]...)
(sync = synchrony_index(sync), async = synchrony_index(staggered), floor = 1/n)
```

## Why it matters

The inflationary effect and spatial asynchrony are the two ways that variation, filtered through dispersal, breaks the mean-field intuition that a population or pathogen persists only where it can locally replace itself.
Temporal autocorrelation inflates the standing abundance of an immigration-fed sink and can render a network of sinks self-sustaining; spatial asynchrony lets peaking patches rescue crashing ones and keeps a pathogen alive across a region of individually-too-small communities.
For ecology this reframes conservation and pest control around the *correlation structure* of the environment, not just its mean and variance.
For epidemiology it means that elimination is a property of a connected, fluctuating landscape rather than of any single community's average reproduction number: an infection can persist with $\bar R < 1$ everywhere, and — turning the same physics into a tool — deliberately synchronising control across patches can precipitate the global fadeout that ends it.
And because the effect reduces to covariances of the local growth rate $r_i(t)$ — in space, in time, and in their spatiotemporal interaction — it is not just a cautionary story but something you can estimate from surveillance data and watch move.

## Related

- [Metapopulations and the Levins Model](metapopulations.md)
- [Jensen's Inequality and Nonlinear Averaging](jensens-inequality.md)
- [The Effective Reproduction Number and Forecasting](reproduction-number-rt.md)
- [Stochastic Epidemics and the Gillespie Algorithm](stochastic-epidemics.md)
- [Spatial Moment Equations](spatial-moment-equations.md)
- [Discrete-Time Models and the Logistic Map](discrete-population-models.md)
- [Compartmental Models (SIR)](sir.md)
- [Markov Chains](markov-chains.md)
- [Quantitative Methods](../math.md)
