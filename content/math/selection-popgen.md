---
title: "Selection and Mutation–Selection Balance"
---

# Selection and Mutation–Selection Balance

Natural selection is the deterministic counterpart to [genetic drift](genetic-drift.md): instead of allele frequencies wandering by chance, they are pushed in a direction by differences in survival and reproduction.
This page shows how to turn genotype fitnesses into an allele-frequency recursion, when that recursion drives an allele to fixation versus maintains a polymorphism, and how recurrent mutation balances selection at a low equilibrium frequency.

## Fitness and the selection recursion

Consider a single biallelic locus with alleles $A$ and $a$ at frequencies $p$ and $q = 1 - p$.
Assign each genotype a relative fitness — its expected reproductive contribution — writing $w_{AA}$, $w_{Aa}$, $w_{aa}$.
Starting from [Hardy–Weinberg](hardy-weinberg.md) genotype frequencies $p^2, 2pq, q^2$ before selection, the mean fitness of the population is the weighted average \[ \bar w = p^2 w_{AA} + 2pq\, w_{Aa} + q^2 w_{aa}. \] Selection reweights each genotype by its fitness, and the frequency of $A$ in the next generation is the frequency of $A$-carrying gametes after this reweighting: \[ p' = \frac{p^2 w_{AA} + pq\, w_{Aa}}{\bar w}. \] The change in one generation is \[ \Delta p = p' - p = \frac{pq\,\bigl[\,p(w_{AA}-w_{Aa}) + q(w_{Aa}-w_{aa})\,\bigr]}{\bar w}. \] The sign of $\Delta p$ depends only on the bracketed term, and the factor $pq$ vanishes at the boundaries $p=0$ and $p=1$, which are always fixed points.

## Directional selection

Suppose one homozygote is fittest and the heterozygote is intermediate, for example $w_{AA} = 1$, $w_{Aa} = 1 - hs$, $w_{aa} = 1 - s$ with selection coefficient $s > 0$ and dominance coefficient $0 \le h \le 1$.
Then $A$ is favoured, $\Delta p > 0$ for all $0 < p < 1$, and the allele marches monotonically toward fixation at $p = 1$.
A recessive deleterious allele ($h = 0$) is removed slowly once rare, because selection acts only on the vanishingly few $aa$ homozygotes.

## Overdominance and stable polymorphism

When the heterozygote is fittest — heterozygote advantage, or overdominance — selection maintains both alleles.
Write $w_{AA} = 1 - s_1$, $w_{Aa} = 1$, $w_{aa} = 1 - s_2$ with $s_1, s_2 > 0$.
Setting $\Delta p = 0$ with $0 < p < 1$ requires the bracket to vanish, giving the interior equilibrium \[ \hat p = \frac{s_2}{s_1 + s_2}, \qquad \hat q = \frac{s_1}{s_1 + s_2}. \] This equilibrium is stable: if $p$ drifts above $\hat p$ the fitter allele becomes the rarer one and selection pushes it back.
The textbook case is the sickle-cell allele, where the heterozygote resists malaria while both homozygotes suffer.
Frequency-dependent versions of this balancing dynamic are studied in [evolutionary game theory](evolutionary-game-theory.md).

## Mutation–selection balance

A deleterious allele is never fully eliminated because mutation keeps regenerating it.
Let mutation from $A$ to $a$ occur at rate $\mu$ per generation while selection removes $a$.
The equilibrium frequency of $a$ is where mutational input equals selective removal.

For a fully recessive deleterious allele ($h = 0$, fitness $1 - s$ for $aa$), removal near equilibrium is $\approx s\hat q^2$ and input is $\approx \mu$, so \[ \mu \approx s\,\hat q^{\,2} \quad\Longrightarrow\quad \hat q \approx \sqrt{\mu/s}. \] For a dominant (or additive) deleterious allele, selection acts on the common heterozygotes, removal is $\approx s\hat q$, and \[ \hat q \approx \mu/s. \] The recessive case sits at a much higher frequency for the same $\mu$ and $s$, because deleterious recessives are shielded from selection inside heterozygotes.

## Worked example

### One generation of directional selection

Take $w_{AA} = 1.0$, $w_{Aa} = 0.9$, $w_{aa} = 0.8$ and a starting frequency $p = 0.3$, so $q = 0.7$.
The mean fitness is \[ \bar w = 0.3^2(1.0) + 2(0.3)(0.7)(0.9) + 0.7^2(0.8) = 0.09 + 0.378 + 0.392 = 0.86. \] The updated frequency is \[ p' = \frac{0.3^2(1.0) + (0.3)(0.7)(0.9)}{0.86} = \frac{0.09 + 0.189}{0.86} = \frac{0.279}{0.86} \approx 0.3244. \] So $\Delta p \approx +0.0244$: the favoured allele $A$ increases, and iterating this map carries it to fixation.

### A mutation–selection balance

Let a recessive lethal-ish allele have $s = 0.1$ with mutation rate $\mu = 10^{-5}$.
Then \[ \hat q \approx \sqrt{\mu/s} = \sqrt{10^{-5}/0.1} = \sqrt{10^{-4}} = 0.01. \] If instead the allele were dominant with the same $s$ and $\mu$, its equilibrium would be $\hat q \approx \mu/s = 10^{-4}$ — a hundredfold lower.

## Simulation

Iterate the selection recursion from a starting frequency and watch it approach fixation (directional) or an interior equilibrium (overdominance).

### R

```r
selection_step <- function(p, wAA, wAa, waa) {
  q <- 1 - p
  wbar <- p^2 * wAA + 2 * p * q * wAa + q^2 * waa
  (p^2 * wAA + p * q * wAa) / wbar
}

iterate <- function(p0, wAA, wAa, waa, gens = 200) {
  p <- p0
  for (i in seq_len(gens)) p <- selection_step(p, wAA, wAa, waa)
  p
}

# Directional: A fixes
iterate(0.3, 1.0, 0.9, 0.8)          # ~ 1.0 (fixation of A)

# Overdominance: stable polymorphism, phat = s2/(s1+s2)
s1 <- 0.2; s2 <- 0.3
iterate(0.05, 1 - s1, 1, 1 - s2)     # ~ 0.6 = 0.3/0.5
```

### Python

```python
import numpy as np

def selection_step(p, wAA, wAa, waa):
    q = 1 - p
    wbar = p**2 * wAA + 2 * p * q * wAa + q**2 * waa
    return (p**2 * wAA + p * q * wAa) / wbar

def iterate(p0, wAA, wAa, waa, gens=200):
    p = p0
    for _ in range(gens):
        p = selection_step(p, wAA, wAa, waa)
    return p

# Directional: A fixes
print(iterate(0.3, 1.0, 0.9, 0.8))       # ~ 1.0

# Overdominance: stable polymorphism at s2/(s1+s2)
s1, s2 = 0.2, 0.3
print(iterate(0.05, 1 - s1, 1, 1 - s2))  # ~ 0.6
```

### Julia

```julia
function selection_step(p, wAA, wAa, waa)
    q = 1 - p
    wbar = p^2*wAA + 2p*q*wAa + q^2*waa
    (p^2*wAA + p*q*wAa) / wbar
end

function iterate_sel(p0, wAA, wAa, waa; gens=200)
    p = p0
    for _ in 1:gens
        p = selection_step(p, wAA, wAa, waa)
    end
    p
end

iterate_sel(0.3, 1.0, 0.9, 0.8)            # ~ 1.0 (fixation)

s1, s2 = 0.2, 0.3
iterate_sel(0.05, 1 - s1, 1, 1 - s2)       # ~ 0.6
```

## Why it matters

Selection is the engine of adaptation, and this simple recursion is the workhorse that turns genotype fitnesses into predictions about how populations change.
It explains why some alleles sweep to fixation while others persist as protected polymorphisms, and mutation–selection balance sets the baseline burden of deleterious variation that every population carries — the quantity behind genetic load, the maintenance of disease alleles, and the evolution of dominance.

## Related

- [Genetic Drift and the Wright–Fisher Model](genetic-drift.md)
- [Hardy–Weinberg Equilibrium](hardy-weinberg.md)
- [Quantitative Genetics and the Breeder's Equation](quantitative-genetics.md)
- [Evolutionary Game Theory](evolutionary-game-theory.md)
- [Quantitative Methods](../math.md)
