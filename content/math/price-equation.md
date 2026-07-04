---
title: "The Price Equation and Evolutionary Epidemiology"
description: "Price's covariance identity partitions any change in a mean trait into selection plus transmission, and — in continuous time — into a third within-host term that reframes how pathogens evolve."
---

# The Price Equation and Evolutionary Epidemiology

Evolution by natural selection is, at bottom, bookkeeping: the mean of a trait changes because some variants leave more descendants than others, and because descendants need not resemble their ancestors exactly.
The **Price equation** is the exact statement of that bookkeeping.
It is not a model of any particular system — it assumes almost nothing — yet it cleanly separates the part of trait change due to *selection* from the part due to *transmission*, and it is the natural language for asking how a pathogen's virulence or transmissibility evolves while its epidemic unfolds.

![The Price equation partitions the change in a mean trait into two contributions. Left: selection is the covariance between fitness and trait — ancestors with a higher trait value leave more descendants, so the fitness-weighted mean shifts up. Right: a waterfall from the parental mean to the offspring mean, built by adding the selection contribution Cov(w,z)/w-bar and the transmission (mutation) contribution E(w times delta-z)/w-bar.](../assets/figures/price-two-terms.svg)

## The identity

Consider a population of ancestral entities indexed by $i$ — hosts, cells, lineages, or infections.
Each carries a value $z_i$ of some trait, and each leaves $w_i$ descendants; we call $w_i$ its **fitness**.
The descendants of ancestor $i$ carry, on average, the trait value $z_i + \Delta z_i$, where $\Delta z_i$ is the average shift between an ancestor and its own descendants (from mutation, say, or measurement of a different life stage).
Write $\bar z = \frac1N\sum_i z_i$ for the ancestral mean trait and $\bar w = \frac1N\sum_i w_i$ for the mean fitness.

The mean trait in the descendant generation is the fitness-weighted average of the descendant trait values, \[ \bar z' = \frac{\sum_i w_i\,(z_i + \Delta z_i)}{\sum_i w_i}. \] Multiplying through by $\bar w$ and subtracting $\bar w\,\bar z$ gives, with no approximation, \[ \bar w\,\Delta\bar z \;=\; \underbrace{\operatorname{Cov}(w_i,\,z_i)}_{\text{selection}} \;+\; \underbrace{\mathbb{E}(w_i\,\Delta z_i)}_{\text{transmission}}, \] where the covariance and expectation are taken over the ancestral population with equal weight $1/N$ on each individual.
This is the **Price equation** ([Price 1970](https://doi.org/10.1038/227520a0); [Price 1972](https://doi.org/10.1111/j.1469-1809.1957.tb01874.x)).

The two terms are the whole story.
The **selection** term is the covariance between fitness and trait: if individuals with a larger $z$ tend to leave more descendants, the covariance is positive and the mean trait increases.
The **transmission** term (also called the *transmission-bias* or *fidelity* term) is the fitness-weighted average of the ancestor-to-descendant change: if descendants systematically differ from their parents — directional mutation, imperfect inheritance — the mean shifts even without any selection.
Set every $\Delta z_i = 0$ (perfect transmission) and only selection remains; make fitness independent of the trait and only transmission remains.

> [!NOTE]
> The Price equation is an *identity*, not a mechanism.
> It holds for any mapping of ancestors to descendants, with any definition of the trait, in any population — which is exactly why it is a useful accounting frame rather than a predictive model on its own.
> Its power comes from the *interpretation* of the two terms and from choosing $z$ and $w$ so those terms mean something ([Frank 2012](https://doi.org/10.1111/j.1420-9101.2012.02498.x)).

### It is exact — check it

Because the identity is exact, a few lines of code reproduce it to machine precision on any toy population.
We take eight lineages with hand-chosen traits, descendant counts, and a small transmission bias, and confirm that $\operatorname{Cov}(w,z) + \mathbb{E}(w\,\Delta z)$ equals $\bar w\,\Delta\bar z$.

![A worked example on eight lineages. Left: a genealogy strip with ancestors on top at their trait value and descendants below, their number equal to fitness and their position nudged by the mutation bias; the fitness-weighted descendant mean sits to the left of the ancestral mean. Right: the two contributions, Cov(w,z) and E(w times delta-z), sum exactly to w-bar times delta-z-bar.](../assets/figures/price-selection-differential.svg)

```python
import numpy as np

z  = np.array([2.0, 2.5, 3.0, 3.0, 3.5, 4.0, 4.5, 5.0])   # ancestor trait
w  = np.array([1,   2,   1,   3,   3,   4,   4,   5])       # number of descendants (fitness)
dz = np.full(z.size, -0.12)                                # transmission bias (mutation)

wbar, zbar = w.mean(), z.mean()
zbar_prime = (w * (z + dz)).sum() / w.sum()                # fitness-weighted descendant mean
cov  = ((w - wbar) * (z - zbar)).mean()                    # selection term
tran = (w * dz).mean()                                     # transmission term

print("Cov(w,z)      =", round(cov, 6))
print("E(w*dz)       =", round(tran, 6))
print("sum           =", round(cov + tran, 6))
print("wbar*dzbar    =", round(wbar * (zbar_prime - zbar), 6))
```

<!-- python-output:auto -->
```text
Cov(w,z)      = 1.179688
E(w*dz)       = -0.345
sum           = 0.834688
wbar*dzbar    = 0.834687
```
<!-- /python-output:auto -->

The two sides agree exactly: the covariance and the transmission bias together *are* the change in the mean.

## The selection term connects to the breeder's equation

The first term is the same selection that the [breeder's equation](quantitative-genetics.md) describes, seen from a different angle.
Dividing by $\bar w$ and dropping transmission, the change in the mean is $\Delta\bar z = \operatorname{Cov}(w_i, z_i)/\bar w = \operatorname{Cov}(w_i/\bar w,\, z_i)$ — the covariance of the trait with *relative* fitness.
Writing relative fitness as a regression on the trait turns this into a response equal to a selection differential times a heritability-like slope, which is precisely $R = h^2 S$ once $z$ is a breeding value.
The Price equation is thus the assumption-light parent of the breeder's equation: the breeder's equation is what you get when you model the covariance as a linear regression of fitness on an additively heritable trait.

The transmission term, meanwhile, is where **nonlinear averaging** lives.
Whenever descendants map to ancestors through a curved relationship, the mean of the transformed trait is not the transform of the mean, and the gap is governed by [Jensen's inequality](jensens-inequality.md) — the same convexity correction that drives the inflationary effect on the [metapopulation asynchrony page](metapopulation-asynchrony.md).

## A continuous-time Price equation

Textbook derivations, like the one above, are **discrete-time** with **non-overlapping generations**: a clean census of ancestors, then a clean census of descendants.
Epidemics do not work that way.
Infections are born (through transmission) and die (through recovery or host death) continuously, generations overlap, and the population turns over while we watch.
[Day, Parsons, Lambert & Gandon (2020)](https://doi.org/10.1098/rstb.2019.0357) derive the version of Price's equation that fits this world, and it partitions change into **three** terms rather than two.

Let $n_i$ be the number of individuals of type $i$, each with trait $z_i$, and let the mean $\bar z$ be taken over the frequencies $n_i/\sum_i n_i$.
In a short interval $\Delta t$, a type-$i$ individual produces $b_i\,\Delta t$ descendants (**birth rate** $b_i$) and survives with probability $1 - d_i\,\Delta t$ (**death rate** $d_i$); its **net reproductive rate** is $r_i = b_i - d_i$.
Descendants may be of a different type, so the average trait among the offspring of a type-$i$ parent is $z_i + \Delta z_i$; and an individual that *survives* may itself change type, at trait-rate $\dot z_i^{\,s}$.
Carrying the census forward by $\Delta t$ and taking the limit $\Delta t \to 0$ gives their equation (2.4), \[ \frac{d\bar z}{dt} \;=\; \underbrace{\operatorname{Cov}(z_i,\,r_i)}_{\text{selection}} \;+\; \underbrace{\mathbb{E}(b_i\,\Delta z_i)}_{\text{transmission}} \;+\; \underbrace{\mathbb{E}\!\big(\dot z_i^{\,s}\big)}_{\text{within-individual change}}. \]

The first two terms are the continuous-time echoes of the discrete identity: selection is now the covariance between trait and *net reproductive rate*, and transmission is the *birth-weighted* mutation bias.
The third term is genuinely new to the overlapping-generations setting: it accounts for individuals that persist but change — a trait that drifts over an individual's lifetime, or an infection whose strain composition is rewritten from within.

A detail that becomes the crux of the epidemiology: the **selection** term is driven by *both* births and deaths (it uses the net rate $r_i = b_i - d_i$), the **transmission** term is driven by births *only* (mutation happens when a new individual is made, $b_i\,\Delta z_i$), and the **within-individual** term involves *neither* — it reshuffles types among individuals who are already alive.

## The three terms as epidemiology

Now read the three terms for a pathogen.
Following [Day et al. (2020)](https://doi.org/10.1098/rstb.2019.0357), take a two-strain compartment model in which $I_i$ hosts are infected with strain $i$, susceptibles $S$ are infected at strain-specific transmission rate $\beta_i$, infections end (host death or clearance) at rate $\mu + v_i$ where $v_i$ is the **virulence**, transmission mutates to the other strain with probability $\tau_i$, and secondary infection lets one strain displace another within a host (superinfection, rate $\sigma$).
The birth and death rates of Price's equation are then \[ b_i = \beta_i S, \qquad d_i = \mu + v_i, \qquad r_i = \beta_i S - (\mu + v_i), \] and the change in the mean trait — here we track the population's **mean virulence** $\bar v$ — becomes their equation (4.15), \[ \frac{d\bar v}{dt} \;=\; \operatorname{Cov}(v_i,\,\beta_i S - v_i) \;+\; \mathbb{E}(\beta_i S\,\Delta v_i) \;+\; \mathbb{E}\!\big(\dot v_i^{\,s}\big). \]

Each term now names a distinct piece of pathogen biology.

- **Selection** — $\operatorname{Cov}(v_i,\,\beta_i S - v_i)$ — is *between-host* competition: strains differ in the net rate at which their infections spread, births $\beta_i S$ minus deaths $\mu + v_i$, and the covariance of that net rate with virulence sets whether mean virulence is pushed up or down.
- **Transmission** — $\mathbb{E}(\beta_i S\,\Delta v_i)$ — is *mutation during transmission*: it involves the birth rate $\beta_i S$ but not the death rate, because a strain's identity can only change when it makes a new infection.
- **Within-host change** — $\mathbb{E}(\dot v_i^{\,s})$ — is *within-host competition*: existing infections switch strain through secondary infection, involving neither births nor deaths, only the reshuffling of who carries what.

The figure simulates this two-strain model on a transmission-virulence trade-off ($\beta = a\sqrt{v}$, so the more transmissible strain is also the more virulent) and reads off all three terms as the epidemic runs.

![Four panels from a two-strain SIS epidemic analysed with Price's equation. A: the epidemic — susceptibles crash as the two strains sweep, then settle to an endemic level. B: mean virulence rises to a transient peak early in the epidemic, when susceptibles are abundant and the more transmissible-and-virulent strain grows fastest, then falls to the milder strain's value in the long-term endemic state. C: the three Price terms — selection, mutation, and within-host — plotted over time, together with their sum, which lies exactly on the numerically computed derivative of mean virulence. D: the selection coefficient r1 minus r2 equals (beta1 minus beta2) times S minus (v1 minus v2); it starts positive (favouring the virulent strain) and flips sign as S falls past a threshold, an epi-evolutionary feedback driven entirely by the susceptible pool.](../assets/figures/price-sir-three-terms.svg)

### Eco-evolutionary feedback

Notice that *every* term contains $S$ or $I$: selection through $\beta_i S$, transmission through $\beta_i S$, within-host change through the density of co-circulating infections.
The evolutionary equation is therefore **coupled** to the epidemiological equations for $S$ and $I$ — as the epidemic depletes susceptibles, it changes the very selection pressures acting on the pathogen, and the pathogen's evolution feeds back on the epidemic's course.
This **epi-evolutionary feedback** is the feature that traditional applications of Price's equation, with no explicit demography, simply do not have.
Casting the model in Price's form is what makes the feedback visible: it separates the *direct* action of selection from the *indirect* action of the changing host population, and it lets the two play out on comparable timescales instead of assuming evolution is infinitely slow.

### Transient evolution can oppose long-term evolution

Panel D makes the feedback concrete.
The strains differ in net rate by \[ r_1 - r_2 \;=\; (\beta_1 - \beta_2)\,S \;-\; (v_1 - v_2), \] a quantity that depends on the susceptible density $S$.
Early in an epidemic $S$ is large, the transmission advantage $(\beta_1-\beta_2)S$ dominates, and selection favours the more transmissible — hence more *virulent* — strain: mean virulence climbs to a **transient peak**.
As the epidemic burns through susceptibles, $S$ falls; once it drops below $(v_1 - v_2)/(\beta_1 - \beta_2)$ the sign flips, the shorter infectious period of the virulent strain becomes decisive, and the **milder** strain wins the long-term, endemic competition.
The short-term direction of evolution is *opposite* to the long-term one — which is why emerging epidemics can select for high virulence that later recedes ([Berngruber et al. 2013](https://doi.org/10.1371/journal.ppat.1003209)), why epidemic and endemic diseases differ in their evolutionary optima, and why the immediate and eventual evolutionary consequences of an intervention like vaccination can point in opposite directions ([Gandon & Day 2007](https://doi.org/10.1098/rsif.2006.0207)).

## Demographic stochasticity reweights the terms

In a small infected population the deterministic equations above are not the whole story: births and deaths are discrete, random events, and this **demographic stochasticity** alters selection itself.
[Day et al. (2020)](https://doi.org/10.1098/rstb.2019.0357) show that the same three-term partition is the natural way to bookkeep that effect.
Writing $AI$ for the number of infected hosts (habitat area $A$ times infected density $I$), their equation (5.2) multiplies the birth part of selection by $(1 - 1/AI)$ and the death part by $(1 + 1/AI)$, \[ \frac{d\bar z}{dt} \;=\; \operatorname{Cov}\!\Big(z,\; b - d - \tfrac{b+d}{AI}\Big) \;+\; \mathbb{E}(b\,\Delta z)\Big(1 - \tfrac{1}{AI}\Big) \;+\; \mathbb{E}\!\big(\dot z^{\,s}\big). \]

The intuition is that evolution is a change in *frequency*.
When a birth occurs the number of infections rises from $AI$ to $AI+1$, so each new infection moves the frequency by a little *less*; when a death occurs the number falls to $AI-1$, so each loss moves the frequency by a little *more*.
Births are therefore down-weighted and deaths up-weighted, and — because the within-host term changes no totals — it is untouched.

Combining the two selection pieces exposes a classic result.
The effective "measure of fitness" in the covariance is \[ b - d - \frac{b+d}{AI}, \] which is **expected fitness** $b-d$ minus a penalty proportional to $b+d$ — the rate at which birth-or-death events happen, i.e. the **variance in fitness** for a birth-death process.
Selection under drift favours high expected fitness *and* low variance in fitness, recovering the long-standing principle that demographic stochasticity selects for reduced variance in offspring number ([Gillespie 1974](https://doi.org/10.1093/genetics/76.3.601); [Parsons, Lambert, Day & Gandon 2018](https://doi.org/10.1098/rsif.2018.0135)).

![Two panels on demographic stochasticity. Left: the weights that finite population size puts on the selection term — selection on the birth (transmission) component is multiplied by 1 minus 1 over AI and falls below one, while selection on the death (virulence) component is multiplied by 1 plus 1 over AI and rises above one, so drift weakens selection on transmission and strengthens it on virulence, the two curves converging to one as the number of infected hosts AI grows. Right: the evolutionary consequence on a transmission-virulence trade-off — two strains chosen to have exactly equal deterministic net fitness but different turnover b plus d; the milder strain has the lower fitness variance, so drift selects for it, and the advantage grows as AI shrinks.](../assets/figures/price-drift-virulence.svg)

For a pathogen the asymmetry has teeth.
Transmission is a *birth* rate and virulence acts through a *death* rate, so demographic stochasticity **weakens selection on transmission** and **strengthens selection on virulence**.
Along a transmission-virulence trade-off — where a strain buys higher transmission by paying higher virulence — the penalty on transmission and the premium on avoiding a high death rate both push the same way: toward **lower virulence** ([Parsons et al. 2018](https://doi.org/10.1098/rsif.2018.0135)).
The right panel makes this vivid by pitting two strains that are *deterministically neutral* — engineered to have identical net fitness — against each other; the milder strain has the smaller $b+d$, and drift alone tips the balance in its favour, more strongly the smaller the infected population.

## In code

The continuous-time identity is worth verifying the way we verified the discrete one: simulate the two-strain epidemic, compute the three terms from their definitions, and check that they reconstruct $d\bar v/dt$.

### Python

We integrate the Day et al. two-strain model and compare the sum of the selection, mutation, and within-host terms against the exact time derivative of mean virulence.

```python
import numpy as np
from scipy.integrate import solve_ivp

mu, a = 0.02, 6.0
v1, v2 = 0.80, 0.40                       # virulence of the two strains
b1r, b2r = a*np.sqrt(v1), a*np.sqrt(v2)   # transmission via the trade-off beta = a*sqrt(v)
tau, sig = 0.01, 0.6                       # mutation prob on transmission; superinfection rate
rho12, rho21 = 1.0, 0.0                    # the more virulent strain wins within-host

def h(I1, I2):
    return (b1r*I1*(1-tau) + b2r*I2*tau, b2r*I2*(1-tau) + b1r*I1*tau)

def rhs(t, y):
    S, I1, I2 = y
    h1, h2 = h(I1, I2)
    dS = mu*(1-S) - (b1r*I1 + b2r*I2)*S
    dI1 = h1*S - (mu+v1)*I1 + sig*h1*I2*rho12 - sig*h2*I1*rho21
    dI2 = h2*S - (mu+v2)*I2 + sig*h2*I1*rho21 - sig*h1*I2*rho12
    return [dS, dI1, dI2]

sol = solve_ivp(rhs, (0, 300), [0.99, 5e-3, 5e-3], t_eval=np.linspace(0, 300, 6000),
                rtol=1e-10, atol=1e-13, method="LSODA")
S, I1, I2 = sol.y
p = I1/(I1+I2)                             # frequency of strain 1
b1, b2 = b1r*S, b2r*S
r1, r2 = b1-(mu+v1), b2-(mu+v2)
h1, h2 = h(I1, I2)
sel = p*(1-p)*(v1-v2)*(r1-r2)                                     # cov[v, r]
mut = p*b1*tau*(v2-v1) + (1-p)*b2*tau*(v1-v2)                     # E[b*dv]
wh  = (v1-v2)*(sig*h1*(1-p)*rho12 - sig*h2*p*rho21)              # E[dv^s/dt]

# exact dp/dt from the ODE, hence exact dvbar/dt = (v1-v2)*dp/dt
dI1, dI2 = np.gradient(I1, sol.t), np.gradient(I2, sol.t)
dp = (dI1*(I1+I2) - I1*(dI1+dI2)) / (I1+I2)**2
dvbar = (v1-v2)*dp
m = (sol.t > 2) & (sol.t < 298)
print("max |sum of 3 terms - dvbar/dt| :", float(np.max(np.abs((sel+mut+wh-dvbar)[m]))))
print("transient peak mean virulence   :", round(float((p*v1+(1-p)*v2).max()), 3))
print("endemic mean virulence          :", round(float((p*v1+(1-p)*v2)[-1]), 3), "(v2 =", v2, ")")
```

<!-- python-output:auto -->
```text
max |sum of 3 terms - dvbar/dt| : 6.775067564504869e-05
transient peak mean virulence   : 0.79
endemic mean virulence          : 0.421 (v2 = 0.4 )
```
<!-- /python-output:auto -->

The three terms sum to the derivative to within finite-difference error, mean virulence peaks transiently well above its endemic value, and the milder strain inherits the long run.

### R

```r
# Discrete Price identity: Cov(w, z) + E(w * dz) = wbar * dzbar
z  <- c(2.0, 2.5, 3.0, 3.0, 3.5, 4.0, 4.5, 5.0)   # ancestor trait
w  <- c(1,   2,   1,   3,   3,   4,   4,   5)      # descendants (fitness)
dz <- rep(-0.12, length(z))                       # transmission bias

wbar <- mean(w); zbar <- mean(z)
zbar_prime <- sum(w * (z + dz)) / sum(w)
cov  <- mean((w - wbar) * (z - zbar))             # selection
tran <- mean(w * dz)                              # transmission
c(sum = cov + tran, wbar_dzbar = wbar * (zbar_prime - zbar))
```

### Julia

```julia
using Statistics

# Discrete Price identity on a small population
z  = [2.0, 2.5, 3.0, 3.0, 3.5, 4.0, 4.5, 5.0]     # ancestor trait
w  = [1.0, 2, 1, 3, 3, 4, 4, 5]                    # descendants (fitness)
dz = fill(-0.12, length(z))                        # transmission bias

wbar, zbar = mean(w), mean(z)
zbar_prime = sum(w .* (z .+ dz)) / sum(w)
covwz = mean((w .- wbar) .* (z .- zbar))           # selection
tran  = mean(w .* dz)                              # transmission
(sum = covwz + tran, wbar_dzbar = wbar * (zbar_prime - zbar))
```

## Why it matters

The Price equation is the closest thing evolutionary biology has to a conservation law: an exact identity that holds for any population and any trait, and that splits change into selection plus transmission by pure bookkeeping.
Its continuous-time form is what lets that bookkeeping reach the overlapping generations of an epidemic, where it adds a third, within-host term and — crucially — couples the evolutionary equation to the demography of susceptibles and infecteds.
That coupling is where the epidemiological payoff lives: it explains why virulence can spike in an emerging epidemic and relax in an endemic one, why interventions can have opposite short- and long-term evolutionary effects, and why small, stochastic pathogen populations should drift toward lower virulence.
Read this way, Price's equation is less a formula to solve than a lens for seeing which force — between-host spread, mutation, within-host competition, or the shifting host population itself — is moving a pathogen at any moment.

## Related

- [Quantitative Genetics and the Breeder's Equation](quantitative-genetics.md) — the regression form of the selection term
- [Jensen's Inequality and Nonlinear Averaging](jensens-inequality.md) — the convexity behind the transmission term
- [Adaptive Dynamics and the Evolution of Virulence](evolution-of-virulence.md) — the trade-off that sets the direction of selection
- [Genetic Drift and the Wright–Fisher Model](genetic-drift.md) — fitness variance and small populations
- [Selection and Mutation–Selection Balance](selection-popgen.md)
- [The Next-Generation Matrix and R₀](next-generation-matrix.md)
- [Asynchrony and the Inflationary Effect in Metapopulations](metapopulation-asynchrony.md) — the same covariance decomposition, in space
- [Compartmental Models (SIR)](sir.md)
- [Quantitative Methods](../math.md)
