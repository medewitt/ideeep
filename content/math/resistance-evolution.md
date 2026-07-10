---
title: "The Evolution of Resistance"
description: "How drug resistance rises under selection and decays under a fitness cost, from mutation-selection balance to the mutant selection window."
---

# The Evolution of Resistance

Drug resistance is evolution in fast motion.
A resistant strain that was rare and disfavored becomes common within a course of treatment, because the drug reverses which strain is fitter.
The same trait that wins under drug pressure usually carries a cost when the drug is gone, so resistance frequency is a tug-of-war between selection for survival under treatment and selection against the burden of the resistance mechanism.

![Resistant-strain frequency over time: a shaded drug-on period drives a rise under selection, followed by a slow decline under a fitness cost once the drug is removed, settling toward a mutation-selection baseline.](../assets/figures/resistance-evolution.svg)

## Two strains, two fitnesses

Represent a pathogen population as a mix of a drug-sensitive strain and a resistant strain, and let $p$ be the frequency of the resistant type.
Each strain has a fitness that depends on whether the drug is present.
Without drug, resistance carries a **fitness cost** $c$: the resistant strain grows a fraction $c$ more slowly because its resistance mechanism — an efflux pump, an altered target, an inactivating enzyme — diverts resources or degrades function.
With drug at a suppressive concentration, the sensitive strain is held back instead, so resistance is favored.
Writing the per-generation multiplicative fitnesses as $w_R$ and $w_S$, one round of [selection](selection-popgen.md) updates the frequency by

\[
p' = \frac{p\, w_R}{p\, w_R + (1 - p)\, w_S}.
\]

This is the discrete replicator map for two competing types: the fitter strain's frequency grows, its odds $p/(1-p)$ multiplying by $w_R/w_S$ each generation.

## Mutation-selection balance

Even without any drug, resistant mutants are not absent.
Forward mutation supplies them at some small rate $u$ per generation, while the cost $c$ removes them, and the two forces settle at a low baseline frequency

\[
\hat{p} \approx \frac{u}{c}.
\]

For a mutation rate $u = 10^{-4}$ and a cost $c = 0.05$ this is $\hat{p} \approx 2 \times 10^{-3}$: resistance is always present at a low level, ready to be amplified the moment selection favors it.
A larger cost pushes the baseline lower; a costless resistance mechanism has no such floor and can drift to appreciable frequency on its own.

## The mutant selection window

Not every drug concentration selects for resistance.
Below the concentration that inhibits the sensitive strain, both strains grow and neither is favored.
Far above the concentration needed to inhibit even the resistant strain, both are suppressed and cannot replicate to compete.
Between these bounds lies the **mutant selection window**: concentrations high enough to suppress the sensitive strain but too low to stop the resistant one, so the resistant strain is enriched.
Dosing that lingers in this window — subtherapeutic exposure, poor adherence, or long pharmacokinetic tails — is exactly what selects resistance, which is why the window connects resistance evolution to [antimicrobial PK/PD](antimicrobial-pkpd.md).

## Reversion and compensation

When the drug is withdrawn, selection reverses and the cost $c$ drives resistance back down, but slowly, and rarely all the way to zero.
Two forces blunt the decline.
Recurrent mutation keeps replenishing resistant types toward the $u/c$ baseline, and **compensatory mutations** — secondary changes that restore fitness without losing resistance — lower the effective cost, so a resistant lineage can become nearly as fit as the sensitive one.
Once compensated, resistance persists in the population long after drug use stops, and reversion may never occur.

## A worked example

Track resistant frequency across a drug-on then drug-off period with the two-strain selection map.
During treatment the drug suppresses the sensitive strain by a fraction $k = 0.15$, so $w_R = 1$ and $w_S = 1 - k = 0.85$; the resistant odds multiply by $1/0.85 \approx 1.18$ each generation.
After the drug is removed the cost $c = 0.05$ takes over, so $w_R = 0.95$ and $w_S = 1$, and the odds multiply by $0.95$ each generation.
Starting from the mutation-selection baseline $p_0 = u/c = 0.002$, sixty generations of treatment lift resistance from a fraction of a percent to near fixation, after which it declines toward the baseline over a longer stretch — the rise is fast, the reversion slow.

## In code

### R

```r
cost <- 0.05; kill <- 0.15; u <- 1e-4
p <- u / cost                       # mutation-selection baseline
step <- function(p, wR, wS) {
  p <- p * wR / (p * wR + (1 - p) * wS)   # selection
  p + u * (1 - p)                          # recurrent mutation
}
T_on <- 60; T_end <- 220
for (t in 1:T_end) {
  fit <- if (t <= T_on) c(1, 1 - kill) else c(1 - cost, 1)
  p <- step(p, fit[1], fit[2])
}
p                                    # low again after drug-off
```

### Python

```python
u, cost, kill = 1e-4, 0.05, 0.15
p = u / cost                # mutation-selection baseline frequency
T_on, T_end = 60, 220


def step(p, wR, wS):
    p = p * wR / (p * wR + (1 - p) * wS)   # discrete selection
    return p + u * (1 - p)                 # recurrent mutation input


traj = [p]
for t in range(1, T_end + 1):
    if t <= T_on:
        wR, wS = 1.0, 1.0 - kill      # drug present: sensitive suppressed
    else:
        wR, wS = 1.0 - cost, 1.0      # drug removed: resistance costs
    p = step(p, wR, wS)
    traj.append(p)

for t in [0, 20, 40, 60, 100, 140, 180, 220]:
    print(f"t={t:3d}  resistant freq = {traj[t]:.3f}")
```

<!-- python-output:auto -->
```text
t=  0  resistant freq = 0.002
t= 20  resistant freq = 0.062
t= 40  resistant freq = 0.632
t= 60  resistant freq = 0.978
t=100  resistant freq = 0.851
t=140  resistant freq = 0.426
t=180  resistant freq = 0.089
t=220  resistant freq = 0.014
```
<!-- /python-output:auto -->

### Julia

```julia
u, cost, kill = 1e-4, 0.05, 0.15
p = u / cost
step(p, wR, wS) = (q = p * wR / (p * wR + (1 - p) * wS); q + u * (1 - q))

T_on, T_end = 60, 220
traj = [p]
for t in 1:T_end
    wR, wS = t <= T_on ? (1.0, 1.0 - kill) : (1.0 - cost, 1.0)
    global p = step(p, wR, wS)
    push!(traj, p)
end
println(round(traj[T_on + 1], digits = 3), " -> ", round(traj[end], digits = 3))
```

## Why it matters

The asymmetry between fast rise and slow reversion is the central problem of stewardship: resistance is easy to select and hard to lose, and compensatory evolution can make it effectively permanent.
That asymmetry argues for keeping drug exposure out of the mutant selection window through adequate dosing and adherence, and for limiting the population-level drug pressure that enriches resistant strains.
The same selection-versus-cost balance governs resistance to antibiotics, antivirals, antimalarials, herbicides, and insecticides, and it links to the broader treatment of pathogen evolution in [adaptive dynamics](adaptive-dynamics.md) and the [evolution of virulence](evolution-of-virulence.md).

## Related

- [Selection in Population Genetics](selection-popgen.md)
- [Antimicrobial Resistance Across Scales](amr-across-scales.md) — competitive release and the individual-versus-population tension
- [The Evolution of Virulence](evolution-of-virulence.md)
- [Genetic Drift and the Wright–Fisher Model](genetic-drift.md)
- [Antimicrobial PK/PD](antimicrobial-pkpd.md)
- [Adaptive Dynamics](adaptive-dynamics.md)
- [Quantitative Methods](../math.md)
