---
title: "Asynchrony and the Inflationary Effect in Metapopulations"
---

# Asynchrony and the Inflationary Effect in Metapopulations

A population — or a pathogen — that cannot sustain itself anywhere can nonetheless thrive everywhere.
Two features of patchy, fluctuating landscapes make this possible: variation through *time*, which can *inflate* the abundance of an immigration-fed sink far above its deterministic value, and variation through *space*, whose *asynchrony* lets a patch at its peak rescue a neighbour that has just crashed.
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
This is why [Earn, Rohani & Grenfell (1998)](https://doi.org/10.1126/science.280.5372.1528) could argue that anything which *synchronises* epidemics — strong shared seasonal forcing, or coordinated control — raises the risk of global fadeout, a lever that works *for* elimination rather than against it.

## Measuring asynchrony

To turn these pictures into numbers, we need to quantify how out-of-phase a set of local time series is.
Three complementary measures do most of the work.

![Measuring asynchrony. Left: the phase picture — each local epidemic is a clock hand, and the length of their vector sum, the Kuramoto order parameter r, measures coherence (r = 1 fully synchronous, r near 0 asynchronous). Right: as local epidemics are spread across the seasonal cycle, both the community synchrony index and the mean pairwise correlation fall from 1 toward their asynchronous floors.](../assets/figures/asynchrony-measures.svg)

**Mean pairwise correlation.** The simplest index averages the zero-lag [correlation](linear-regression.md) of local incidence over all pairs of patches, $\bar\rho = \frac{1}{n(n-1)}\sum_{i\ne j}\operatorname{Corr}(x_i, x_j)$.
It runs from $\approx 1$ (synchrony) down toward zero, and can even go slightly negative when epidemics are locked into anti-phase — evenly staggered oscillators of equal amplitude are correlated at exactly $-1/(n-1)$.

**Community synchrony index.** [Loreau & de Mazancourt (2008)](https://doi.org/10.1890/07-0187.1) compare the variance of the *aggregate* to the variances of the parts: \[ \varphi = \frac{\operatorname{Var}\!\left(\sum_i x_i\right)}{\left(\sum_i \sigma_i\right)^2}, \qquad \varphi\in\left[\tfrac1n,\,1\right]. \] When patches move in lockstep the aggregate fluctuates as violently as the sum of the parts and $\varphi=1$; when they are perfectly asynchronous their ups and downs cancel in the sum and $\varphi\to 1/n$ (and toward $0$ under anti-phase locking).
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

## Related

- [Metapopulations and the Levins Model](metapopulations.md)
- [Jensen's Inequality and Nonlinear Averaging](jensens-inequality.md)
- [The Effective Reproduction Number and Forecasting](reproduction-number-rt.md)
- [Stochastic Epidemics and the Gillespie Algorithm](stochastic-epidemics.md)
- [Discrete-Time Models and the Logistic Map](discrete-population-models.md)
- [Compartmental Models (SIR)](sir.md)
- [Markov Chains](markov-chains.md)
- [Quantitative Methods](../math.md)
