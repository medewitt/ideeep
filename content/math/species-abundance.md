---
title: "Species-Abundance Distributions and Neutral Theory"
---

# Species-Abundance Distributions and Neutral Theory

Almost every community — trees in a plot, bacteria in a gut, insects in a light trap — has a few very common species and a long tail of rare ones.
The species-abundance distribution (SAD) captures that lopsided shape, and neutral theory offers a startlingly simple null model for how it arises without invoking any differences between species.

![Left: a rank-abundance curve from a neutral community ($J=500$, immigration $m=0.1$ from a 50-species metacommunity) is steep even though every species is ecologically identical — a few dominate and a long tail sits near one individual. Right: the two classic SAD forms binned by $\log_2$ abundance — Fisher's log-series (singletons the richest class, a monotone decline) versus Preston's log-normal (an interior bell-shaped mode).](../assets/figures/species-abundance.svg "fig:sad")

## The species-abundance distribution

A SAD describes how the individuals in a community are partitioned among its species: how many species have one individual, how many have two, and so on.
It is the empirical counterpart of the relative abundances $p_i$ used to compute [diversity indices](diversity-indices.md).
Two visualizations dominate.

- A histogram of species binned by abundance (often by $\log_2$ abundance) shows the many-rare, few-common hollow curve.
- A rank-abundance curve plots each species' abundance (usually on a log axis) against its rank from most to least common, so a steep curve signals dominance and a shallow one signals evenness.

### Classic forms

Two distributions recur across taxa and are worth knowing as reference shapes from the broader [catalog of distributions](distributions-overview.md).

- Fisher's log-series: the expected number of species with $n$ individuals is $\alpha\, x^{n}/n$, where $0 < x < 1$ and Fisher's $\alpha$ is a diversity parameter.
It predicts that singletons are the most species-rich abundance class — a steep, rare-species-heavy community.
- Preston's log-normal: abundances are normally distributed on a log scale, so binning by $\log_2$ abundance gives a bell-shaped curve with an interior mode.
Large, well-sampled communities tend to look log-normal; sparsely sampled ones look log-series because the mode is hidden below the detection limit.

## The species–area relationship

Richness grows with the area sampled, and remarkably often as a power law: \[ S = c A^{z}, \] equivalently $\log S = \log c + z \log A$, a straight line on log–log axes.
The exponent $z$ is typically around $0.2$–$0.35$ for contiguous habitats, meaning each doubling of area adds only a modest fraction of new species.
The species–area relationship makes richness comparisons meaningful only at a fixed scale, and it links local SADs to regional diversity.

## Hubbell's neutral theory

The unified neutral theory of biodiversity assumes ecological equivalence: every individual, regardless of species, has the same per-capita chance of birth, death, and dispersal.
Under that assumption no species has an advantage, so community composition wanders purely by chance — a demographic random walk directly analogous to [genetic drift](genetic-drift.md), with species playing the role of alleles.
A local community loses species by this drift and regains them by immigration from a much larger metacommunity, which is itself shaped by a balance between speciation and drift.

### The biodiversity number

The whole metacommunity is governed by a single dimensionless parameter, the fundamental biodiversity number \[ \theta = 2 J_M \nu, \] where $J_M$ is the metacommunity size and $\nu$ the per-birth speciation rate.
Large $\theta$ means a diverse metacommunity with many species and a heavy tail of rare ones; small $\theta$ means a few dominant species.
Neutral theory predicts that the metacommunity SAD is Fisher's log-series with $\theta$ playing the role of Fisher's $\alpha$, and that local communities sampled through limited dispersal look log-normal-like — recovering both classic forms from one mechanism.

### Null models, not the last word

The point of neutral theory is that it is a null model for community assembly: it shows how much structure — realistic SADs, species–area curves, turnover — can emerge from drift and dispersal alone, with no niche differences.
When real data depart from the neutral prediction, that gap is the signal that selection, niches, or environmental filtering are doing real work.
Neutral and niche processes are complementary lenses, not rivals.

## Worked example

A neutral local community of $J$ individuals is easy to simulate with a Moran-style update: at each step one random individual dies and is replaced, with probability $m$ by an immigrant drawn from the metacommunity and otherwise by the offspring of a random local individual.
Suppose we track $J = 500$ individuals with immigration $m = 0.1$ drawn from a $50$-species metacommunity.
Because deaths and births are unbiased across species, abundances drift; common species tend to stay common by sheer sampling inertia while rare species blink in and out.
After many steps the rank-abundance curve is steep — a handful of species dominate and a long tail sits near one individual — the log-series-like shape neutral theory predicts, even though every species was ecologically identical ([@fig:sad]).

## Simulation

### R

```r
set.seed(1)
neutral <- function(J = 500, S_meta = 50, m = 0.1, steps = 20000) {
  comm <- sample(S_meta, J, replace = TRUE)          # local community
  meta <- rep(1/S_meta, S_meta)                      # even metacommunity
  for (t in seq_len(steps)) {
    comm[sample(J, 1)] <- if (runif(1) < m)
      sample(S_meta, 1, prob = meta) else comm[sample(J, 1)]
  }
  sort(as.integer(table(comm)), decreasing = TRUE)   # rank-abundance
}
ab <- neutral()
plot(ab, log = "y", type = "b", xlab = "rank", ylab = "abundance")
head(ab)   # e.g. 96 71 60 ... : few common, long rare tail
```

### Python

```python
import numpy as np
rng = np.random.default_rng(1)

def neutral(J=500, S_meta=50, m=0.1, steps=20000):
    comm = rng.integers(0, S_meta, J)
    for _ in range(steps):
        if rng.random() < m:
            comm[rng.integers(J)] = rng.integers(S_meta)     # immigrant
        else:
            comm[rng.integers(J)] = comm[rng.integers(J)]    # local birth
    counts = np.bincount(comm)
    return np.sort(counts[counts > 0])[::-1]                 # rank-abundance

ab = neutral()
print(ab[:6])   # few common species, long tail of rare ones
# import matplotlib.pyplot as plt; plt.semilogy(ab, 'o-')
```

<!-- python-output:auto -->
```text
[48 45 41 28 27 24]
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, StatsBase
Random.seed!(1)

function neutral(; J=500, S_meta=50, m=0.1, steps=20000)
    comm = rand(1:S_meta, J)
    for _ in 1:steps
        comm[rand(1:J)] = rand() < m ? rand(1:S_meta) : comm[rand(1:J)]
    end
    sort(collect(values(countmap(comm))), rev=true)   # rank-abundance
end

ab = neutral()
println(ab[1:6])   # few common, many rare
```

## Why it matters

Species-abundance distributions and the species–area relationship are among the most general empirical patterns in ecology, and any theory of biodiversity has to reproduce them.
Neutral theory matters because it sets the null expectation: it tells you how diverse a community should look if nothing but drift and dispersal were operating, so departures pinpoint where niche differences, selection, or host filtering actually shape a microbiome or community.

## Related

- [Diversity Indices](diversity-indices.md)
- [Genetic Drift and the Wright–Fisher Model](genetic-drift.md)
- [Probability Basics](probability-basics.md)
- [Distributions Overview](distributions-overview.md)
- [Quantitative Methods](../math.md)
