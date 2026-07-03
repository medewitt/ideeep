---
title: "Diversity Indices"
---

# Diversity Indices

A diversity index compresses a whole community's species composition into a single number that captures both how many species are present and how evenly the individuals are spread among them.
This matters everywhere from gut microbiome surveys to host-parasite systems, because "which community is more diverse?" is really a question about the shape of the relative abundances $p_i$.

## Relative abundances

Start from counts of each species and convert them to relative abundances $p_i$, the fraction of all individuals belonging to species $i$.
By construction they are non-negative and sum to one, \[ \sum_i p_i = 1, \] so a $p_i$ is exactly the [probability](probability-basics.md) that a randomly drawn individual belongs to species $i$.
Every index below is a different summary of this abundance vector, which comes from the community's underlying [species-abundance distribution](species-abundance.md).

## Species richness

The simplest measure is species richness $S$, the count of species with $p_i > 0$.
Richness treats a species represented by a single individual exactly like a dominant one, so it ignores evenness entirely and is highly sensitive to sampling effort.

## Shannon index

The Shannon index borrows from information theory and measures the uncertainty in the species identity of a random individual: \[ H = -\sum_i p_i \ln p_i . \] It is largest when all species are equally common and zero when one species holds everything.
Because it uses the [logarithm](exponentials-and-logarithms.md), $H$ is on a log scale; exponentiating it, \[ e^{H} = \exp\!\left(-\sum_i p_i \ln p_i\right), \] returns an effective number of species — the number of equally-abundant species that would give the same $H$.
The Shannon index is also the [expected value](expected-value.md) of $-\ln p_i$ over the community.

## Simpson's index

Simpson's index is the probability that two individuals drawn at random (with replacement) belong to the same species: \[ D = \sum_i p_i^2 . \] Large $D$ means one or a few species dominate.
Two common rescalings make it increase with diversity:

- Gini–Simpson index $1 - D$, the probability that two random individuals differ in species.
- Inverse Simpson index $1/D$, again an effective number of species, but one that discounts rare species relative to $e^{H}$.

## Pielou's evenness

To separate evenness from richness, divide the Shannon index by its maximum possible value $\ln S$ (attained when all species are equally abundant): \[ J = \frac{H}{\ln S} . \] Pielou's evenness $J$ ranges from $0$ (one species dominates) to $1$ (perfectly even), and being a ratio it is comparable across communities with different $S$.

## Hill numbers unify them

The Hill numbers express all of these as one family indexed by an order $q$ that tunes how much weight common species receive: \[ {}^{q}D = \left(\sum_i p_i^{q}\right)^{1/(1-q)} . \] Each is an effective number of species, measured in the same units as richness, which makes them directly comparable.

- $q = 0$: ${}^{0}D = S$, plain richness — every species counts equally regardless of abundance.
- $q \to 1$: the limit is ${}^{1}D = e^{H}$, the exponential of Shannon — species weighted in proportion to abundance.
- $q = 2$: ${}^{2}D = 1/D = 1/\sum_i p_i^2$, the inverse Simpson number — common species weighted most.

As $q$ rises, rare species contribute less, so ${}^{q}D$ decreases: ${}^{0}D \ge {}^{1}D \ge {}^{2}D$.
Plotting ${}^{q}D$ against $q$ gives a diversity profile that summarizes a community at every weighting at once.

## Worked example

Take a community of four species with counts $40, 30, 20, 10$ (total $100$), so \[ p = (0.4,\ 0.3,\ 0.2,\ 0.1). \] Richness is $S = 4$.

Shannon index: \[ H = -\big(0.4\ln 0.4 + 0.3\ln 0.3 + 0.2\ln 0.2 + 0.1\ln 0.1\big) \approx 1.2799 . \] So the effective number of species is $e^{H} \approx 3.596$.

Simpson's index: \[ D = 0.4^2 + 0.3^2 + 0.2^2 + 0.1^2 = 0.16 + 0.09 + 0.04 + 0.01 = 0.30 . \] Hence Gini–Simpson $1 - D = 0.70$ and inverse Simpson $1/D \approx 3.333$.

Evenness: \[ J = \frac{H}{\ln S} = \frac{1.2799}{\ln 4} = \frac{1.2799}{1.3863} \approx 0.923 . \]

Collecting the Hill numbers: ${}^{0}D = 4$, ${}^{1}D = e^{H} \approx 3.60$, ${}^{2}D = 1/D \approx 3.33$ — a gentle decline, reflecting a fairly even community.

## In code

### R

```r
p <- c(40, 30, 20, 10); p <- p / sum(p)     # relative abundances

# vegan
library(vegan)
diversity(p, index = "shannon")             # 1.279854
diversity(p, index = "simpson")             # 0.70  (Gini-Simpson, = 1 - D)
diversity(p, index = "invsimpson")          # 3.333333

# manual
S <- sum(p > 0)                             # richness = 4
H <- -sum(p * log(p))                       # 1.279854
J <- H / log(S)                             # 0.9231
D <- sum(p^2)                               # 0.30
hill <- function(p, q) if (q == 1) exp(-sum(p*log(p)))
                       else sum(p^q)^(1/(1-q))
c(hill(p,0), hill(p,1), hill(p,2))          # 4.000 3.596 3.333
```

### Python

```python
import numpy as np
p = np.array([40, 30, 20, 10], float); p /= p.sum()

S = np.sum(p > 0)                    # 4
H = -np.sum(p * np.log(p))          # 1.2798542
J = H / np.log(S)                   # 0.92314
D = np.sum(p**2)                    # 0.30

def hill(p, q):
    return np.exp(-np.sum(p*np.log(p))) if q == 1 else np.sum(p**q)**(1/(1-q))

print(S, H, J, D)                   # 4 1.27985 0.92314 0.30
print([hill(p, q) for q in (0, 1, 2)])  # [4.0, 3.5955, 3.3333]
```

<!-- python-output:auto -->
```text
4 1.2798542258336674 0.9232196723355077 0.30000000000000004
[np.float64(4.0), np.float64(3.5961154666243216), np.float64(3.333333333333333)]
```
<!-- /python-output:auto -->

### Julia

```julia
p = [40, 30, 20, 10] ./ 100          # relative abundances

S = count(>(0), p)                   # 4
H = -sum(p .* log.(p))               # 1.2798542
J = H / log(S)                       # 0.92314
D = sum(p .^ 2)                      # 0.30

hill(p, q) = q == 1 ? exp(-sum(p .* log.(p))) : sum(p .^ q)^(1/(1 - q))
[hill(p, q) for q in (0, 1, 2)]      # [4.0, 3.5955, 3.3333]
```

## Why it matters

Because a single index can hide as much as it reveals, choosing an index is really choosing how much to care about rare species.
Reporting richness, a Shannon- or Simpson-based number, and an evenness measure — or better, a whole Hill-number profile — lets a microbiome or community study compare samples on a common effective-species scale and state clearly whether a treatment changed the number of species, their evenness, or both.

## Related

- [Species-Abundance Distributions and Neutral Theory](species-abundance.md)
- [Probability Basics](probability-basics.md)
- [Expected Value](expected-value.md)
- [Exponentials and Logarithms](exponentials-and-logarithms.md)
- [Quantitative Methods](../math.md)
