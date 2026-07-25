---
title: "Type M and Type S Errors"
description: "Design analysis beyond power: how much a statistically significant estimate exaggerates the true effect (Type M) and how often it points the wrong way (Type S), for continuous and binary outcomes."
---

# Type M and Type S Errors

Classical power analysis asks a single question: what is the chance of getting a statistically significant result?
But a significant result is not automatically a *good* result.
When a study is underpowered, the estimates that happen to clear the significance threshold are a biased, selected sample — they are systematically too big, and a worrying fraction of them have the wrong sign.
[Gelman and Carlin (2014)](https://journals.sagepub.com/doi/10.1177/1745691614551642) call the accounting of these two failure modes **design analysis**, and they name the errors after the part of the estimate they corrupt:

- a **Type M** ("magnitude") **error** — the *exaggeration ratio* — is how many times larger a significant estimate is than the true effect, on average;
- a **Type S** ("sign") **error** is the probability that a significant estimate has the *opposite sign* from the true effect.

These are the errors that survive publication.
A study reports "$p < 0.05$, effect $= 1.4$", the true effect is $0.3$, and nobody notices that the design guaranteed a fivefold overstatement.

![Left: the exaggeration ratio (Type M) climbs steeply as power falls, exceeding 2 well before power drops to 0.2, and diverging as power approaches the significance level. Right: the wrong-sign rate (Type S) rises from near zero at high power toward 50% as power collapses. Both worked examples from this page — a continuous-outcome trial and a binary-outcome case-control study — are marked; the dashed line is the conventional 80% power target, where both errors are negligible.](../assets/figures/type-m-s-errors.svg "fig:typems")

## The one number that drives everything

Fix a hypothesized true effect $A$ and the standard error $s$ that a proposed design would give (from its sample size, outcome variance, and analysis).
Everything below depends only on their ratio,

\[ d = \frac{A}{s}, \]

the true effect measured in standard errors.
A two-sided test at level $\alpha$ rejects when the estimate exceeds $z^\* s$ in absolute value, where $z^\* = \Phi^{-1}(1 - \alpha/2) \approx 1.96$.
Treating the estimate as [normal](normal-distribution.md), $\hat\theta \sim \mathcal{N}(A, s^2)$, the three design quantities are

\[ \text{power} = \Phi(d - z^\*) + \Phi(-d - z^\*), \label{eq:power} \]

\[ \text{Type S} = \frac{\Phi(-d - z^\*)}{\text{power}}, \label{eq:types} \]

\[ \text{Type M} = \frac{d\,[\Phi(d - z^\*) - \Phi(-d - z^\*)] + \varphi(z^\* - d) + \varphi(z^\* + d)}{d \cdot \text{power}}, \label{eq:typem} \]

where $\Phi$ and $\varphi$ are the standard normal CDF and density.
The two terms in the power [@eq:power] are the chance of a significant estimate with the *correct* sign and with the *wrong* sign; Type S [@eq:types] is just the wrong-sign share.
Type M [@eq:typem] is the mean absolute significant estimate divided by $A$ — the conditional expectation $\mathbb{E}[\,|\hat\theta| \mid \text{significant}\,]/|A|$ worked out for the truncated normal.

> [!NOTE]
> Gelman and Carlin's original `retrodesign` computes Type M by simulation (draw many $\hat\theta$, keep the significant ones, average $|\hat\theta|/A$).
> The closed forms above give the same answer without a random seed and use a normal reference; swap $\Phi, \varphi, z^\*$ for their $t$ counterparts when the design's degrees of freedom are small.

The behavior is stark ([@fig:typems]).
As power drops toward $\alpha$, the exaggeration ratio diverges and the sign error rate climbs toward one-half — a barely-significant study is close to a coin flip on direction and inflates whatever it does find.
At the conventional 80% power target, Type M is about $1.1$ and Type S is essentially zero, which is exactly why design analysis mostly reassures well-powered studies and indicts underpowered ones.

## Worked example 1 — a continuous outcome

A small trial estimates how much a monoclonal antibody lowers peak viral load, measured in $\log_{10}$ copies/mL.
Suppose the true reduction is a modest $A = 0.30$ $\log_{10}$, and the trial's size and outcome variance yield a standard error $s = 0.60$.
Then $d = 0.5$: power is only about $0.08$, so the study is severely underpowered.
Conditional on reaching significance, the estimate overstates the true effect by a factor of roughly $4.8$ (a reported reduction near $1.4$ $\log_{10}$ for a true $0.30$), and about $9\%$ of significant estimates would claim the antibody *raises* viral load.

## Worked example 2 — a binary outcome

For a binary outcome the effect usually lives on the log-odds-ratio scale, and the standard error comes straight from the cell counts of the $2\times2$ table via Woolf's formula, $s = \sqrt{1/a + 1/b + 1/c + 1/d}$.
Consider a small case-control study of a suspected risk factor with

| | exposed | unexposed |
|---|---|---|
| cases | 15 | 85 |
| controls | 12 | 88 |

giving an odds ratio of $1.29$, so $A = \log 1.29 = 0.258$ and $s = 0.416$, hence $d = 0.62$.
Power is about $0.10$; a significant odds ratio would exaggerate the true association nearly fourfold on the log scale, and about $5\%$ of significant results would report a protective factor as harmful (or vice versa).
The lesson generalizes: sparse $2\times2$ tables make $s$ large, push $d$ down, and turn every "significant" odds ratio into a likely overstatement.

## In code

A single `design_analysis(effect, se, alpha)` returns power, the Type S rate, and the Type M exaggeration ratio, then we feed it both examples.

### R

```r
design_analysis <- function(effect, se, alpha = 0.05) {
  d  <- abs(effect) / se
  zc <- qnorm(1 - alpha / 2)
  p_hi  <- pnorm(d - zc)           # significant, correct sign
  p_lo  <- pnorm(-zc - d)          # significant, wrong sign
  power <- p_hi + p_lo
  type_m <- (d * (p_hi - p_lo) + dnorm(zc - d) + dnorm(zc + d)) / (d * power)
  list(power = power, type_s = p_lo / power, type_m = type_m)
}

# Example 1: continuous outcome (log10 viral load reduction)
design_analysis(effect = 0.30, se = 0.60)

# Example 2: binary outcome, SE from the 2x2 table (Woolf's formula)
a <- 15; b <- 85; c <- 12; d <- 88
logor <- log((a * d) / (b * c))
se    <- sqrt(1/a + 1/b + 1/c + 1/d)
design_analysis(effect = logor, se = se)
```

### Python

```python
from math import log, sqrt
from scipy.stats import norm

def design_analysis(effect, se, alpha=0.05):
    d = abs(effect) / se
    zc = norm.ppf(1 - alpha / 2)
    p_hi = norm.cdf(d - zc)           # significant, correct sign
    p_lo = norm.cdf(-zc - d)          # significant, wrong sign
    power = p_hi + p_lo
    type_m = (d * (p_hi - p_lo) + norm.pdf(zc - d) + norm.pdf(zc + d)) / (d * power)
    return {"power": power, "type_s": p_lo / power, "type_m": type_m}

def show(label, r):
    print(f"{label:>12}: power={r['power']:.3f}  "
          f"Type S={r['type_s']*100:5.2f}%  Type M={r['type_m']:.2f}")

# Example 1: continuous outcome (log10 viral load reduction)
show("continuous", design_analysis(0.30, 0.60))

# Example 2: binary outcome, SE from the 2x2 table (Woolf's formula)
a, b, c, d = 15, 85, 12, 88
logor = log((a * d) / (b * c))
se = sqrt(1/a + 1/b + 1/c + 1/d)
show("binary", design_analysis(logor, se))
```

<!-- python-output:auto -->
```text
  continuous: power=0.079  Type S= 8.78%  Type M=4.79
      binary: power=0.095  Type S= 5.20%  Type M=3.90
```
<!-- /python-output:auto -->

### Julia

```julia
using Distributions

function design_analysis(effect, se; alpha = 0.05)
    d  = abs(effect) / se
    zc = quantile(Normal(), 1 - alpha / 2)
    p_hi  = cdf(Normal(), d - zc)        # significant, correct sign
    p_lo  = cdf(Normal(), -zc - d)       # significant, wrong sign
    power = p_hi + p_lo
    type_m = (d * (p_hi - p_lo) + pdf(Normal(), zc - d) +
              pdf(Normal(), zc + d)) / (d * power)
    (power = power, type_s = p_lo / power, type_m = type_m)
end

# Example 1: continuous outcome
design_analysis(0.30, 0.60)

# Example 2: binary outcome, SE from the 2x2 table (Woolf's formula)
a, b, c, d = 15, 85, 12, 88
logor = log((a * d) / (b * c))
se = sqrt(1/a + 1/b + 1/c + 1/d)
design_analysis(logor, se)
```

## Why it matters

Design analysis reframes what a "significant" finding is worth in the very regime where infectious-disease work often operates: small trials, rare events, sparse contingency tables, subgroup analyses, and pilot studies.
In all of these the standard error is large, $d$ is small, and [statistical significance](p-values.md) becomes a filter that admits only the luckiest, most exaggerated estimates — a mechanism behind the [winner's curse](publication-bias.md) and much of the replication crisis.
The practical move is to run [@eq:power]–[@eq:typem] *before* collecting data, using a defensible guess for the true effect: if the design implies a Type M of 4 or a Type S above a few percent, a significant result will not mean what you want it to, and the fix is a bigger study, a better outcome, or a more honest [confidence interval](confidence-intervals.md) rather than a $p$-value.

## Related

- [p-Values](p-values.md)
- [Hypothesis Testing](hypothesis-testing.md)
- [Confidence Intervals](confidence-intervals.md)
- [Statistical Inference](statistical-inference.md)
- [Publication Bias and Small-Study Effects](publication-bias.md)
- [Experimental Design](experimental-design.md)
- [Quantitative Methods](../math.md)
