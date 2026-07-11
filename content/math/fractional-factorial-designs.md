---
title: "Fractional Factorial Designs"
---

# Fractional Factorial Designs

When a full $2^k$ [factorial](factorial-designs.md) has too many runs — 7 factors already means $128$ runs — a **fractional factorial** design runs only a carefully chosen subset.
Under **effect sparsity** (a few factors dominate), a fraction lets you screen many factors cheaply, at the cost of some effects being tangled together.

![Left: the $2^{3-1}$ half fraction is a geometric half of the full $2^3$ cube — the four runs selected by the generator $C=AB$ are alternating vertices, no two sharing an edge. Right: resolution measures how badly effects are aliased — III aliases main effects with two-factor interactions, IV keeps main effects clear but aliases two-factor interactions with each other, and V keeps both clear; higher resolution tangles fewer important effects at the cost of more runs.](../assets/figures/fractional-factorial-designs.svg "fig:fracfac")

## The $2^{k-p}$ fraction

A $2^{k-p}$ design uses a $1/2^{p}$ fraction of the full $2^k$ factorial.
For example, $2^{5-2}$ studies $5$ factors in just $2^{3} = 8$ runs instead of $32$.

You build the fraction by choosing $p$ **design generators**: extra factors are assigned to interaction columns of a smaller full factorial.
For a $2^{3-1}$ we start from a full $2^2$ in $A, B$ and set the third factor via the generator $C = AB$.

## The defining relation and aliasing

Each generator implies a word in the **defining relation**.
From $C = AB$, multiply both sides by $C$ (recall $C \cdot C = I$, the identity column of all $+1$):

\[
I = ABC.
\]

The defining relation lists all such words (for multiple generators, include all their products).
To find what an effect is **aliased** (confounded) with, multiply it by every word in the defining relation.
Aliased effects are estimated by the *same* contrast column, so they cannot be separated:

\[
A = A \cdot ABC = BC, \qquad B = AC, \qquad C = AB.
\]

Here each main effect is aliased with a two-factor interaction.
You estimate $A + BC$ as a single quantity; if the interaction is negligible, the estimate is "really" the main effect.

## Resolution

The **resolution** of a design is the length of the shortest word in the defining relation.
It summarizes how badly effects are confounded:

- **Resolution III** — main effects aliased with two-factor interactions ($I = ABC$).
  Cheapest screening; risky if interactions are active.
- **Resolution IV** — main effects clear of two-factor interactions, but two-factor interactions aliased with each other (shortest word has length 4).
- **Resolution V** — main effects and two-factor interactions all clear of each other; two-factor interactions only aliased with three-factor interactions (shortest word length 5).

Higher resolution costs more runs but tangles fewer important effects ([@fig:fracfac]).

## Worked example: a $2^{3-1}$ half fraction

Three factors in $4$ runs, generator $C = AB$, defining relation $I = ABC$ (Resolution III).
Start from the full $2^2$ in $A, B$ and compute $C = A \times B$:

| Run | $A$ | $B$ | $C = AB$ |
|-----|-----|-----|----------|
| 1   | $-1$ | $-1$ | $+1$ |
| 2   | $+1$ | $-1$ | $-1$ |
| 3   | $-1$ | $+1$ | $-1$ |
| 4   | $+1$ | $+1$ | $+1$ |

The four runs are therefore $(-,-,+),\ (+,-,-),\ (-,+,-),\ (+,+,+)$.

**Alias structure** (multiply each effect by $ABC$):

\[
A = BC, \qquad B = AC, \qquad C = AB.
\]

So the contrast we call "the $A$ effect" actually estimates $A + BC$, and likewise for $B$ and $C$.
Only if the two-factor interactions are small can we read the contrasts as clean main effects — the standard screening assumption.

## In code

### R

```r
library(FrF2)
# 5 factors in 8 runs: a 2^{5-2} fractional factorial
d <- FrF2(nruns = 8, nfactors = 5, randomize = FALSE)
head(d)

# Show which effects are aliased with which
aliases(lm(rnorm(8) ~ (.)^3, data = d))
# Prints the defining relation / alias chains, e.g. D = AB, E = AC, ...
```

### Python

```python
from pyDOE3 import fracfact

# 2^{3-1}: factor c is generated as c = a*b  -> low-res half fraction
d = fracfact("a b ab")
print(d)
# [[-1 -1  1]
#  [ 1 -1 -1]
#  [-1  1 -1]
#  [ 1  1  1]]   columns a, b, c=ab  (matches the worked example)
```

### Julia

```julia
# Construct the 2^{3-1} fraction by hand from sign columns
A = [-1,  1, -1,  1]
B = [-1, -1,  1,  1]
C = A .* B                 # generator C = AB
design = hcat(A, B, C)
# 4×3 matrix; rows are the runs (-,-,+), (+,-,-), (-,+,-), (+,+,+)

# Verify the defining relation I = ABC (all +1) and the aliases A=BC, etc.
all(A .* B .* C .== 1)     # true  -> I = ABC
A == B .* C                # true  -> A aliased with BC
```

## Why it matters for statistics

Fractional factorials make large screening studies affordable: they identify the vital few factors from the trivial many with a fraction of the runs.
Understanding generators, the defining relation, aliasing, and resolution tells you exactly which effects you can trust and which are confounded — essential for the early, exploratory stage of experimentation before committing resources to a focused follow-up.

## Related

- [Factorial Designs](factorial-designs.md)
- [Optimal Experimental Design](optimal-design.md)
- [Experimental Design](experimental-design.md)
- [Response Surface Methodology](response-surface.md)
- [Quantitative Methods](../math.md)
