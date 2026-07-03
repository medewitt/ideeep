---
title: "Causal Inference"
---

# Causal Inference

Association is easy to measure, but causation is what we act on.
Causal inference is the set of ideas that lets us move from "$X$ is associated with $Y$" toward "$X$ causes $Y$" — a distinction that is central in epidemiology and public health, where deliberate experiments are often impossible or unethical.

## Correlation is not causation

Two things can move together without either one causing the other.
The classic culprit is a **confounder**: a common cause of both the exposure and the outcome.

Ice-cream sales and drowning deaths rise and fall together across the year, but eating ice cream does not drown anyone.
Hot weather is the confounder: it drives people both to buy ice cream and to swim, and swimming is what leads to drownings.
Similarly, early studies found coffee drinkers had more lung cancer — but coffee drinkers also smoked more, and smoking is the common cause of both the coffee habit and the cancer.
Once you hold the confounder fixed, the spurious association shrinks or disappears.
The lesson is that a raw correlation mixes the effect you care about with the effects of everything the exposure travels with.

## Simpson's paradox

Confounding can do more than inflate an association — it can flip its sign entirely.

![Simpson's paradox: within each group the trend is negative, but pooling the groups (ignoring the confounder) flips it positive.](../assets/figures/simpsons-paradox.svg)

Suppose that within every age group, more exercise lowers cardiovascular risk.
But in this sample older people happen to exercise more and also carry a higher baseline risk simply because they are older.
If you ignore age and pool everyone together, the high-risk, high-exercise older people dominate one end of the cloud, and the overall trend appears to say that more exercise *raises* risk.
Age is the confounder, and conditioning on it — looking within each age group — recovers the true protective within-group effect.
The paradox is a vivid reminder that the answer can depend entirely on which variable you decide to hold fixed.

## The counterfactual (potential-outcomes) idea

To speak precisely about causation we imagine, for each unit, two **potential outcomes**.
Let $Y(1)$ be the outcome that unit would have under treatment and $Y(0)$ the outcome it would have under control.
The **individual causal effect** is the difference $Y(1) - Y(0)$.

The catch is that we only ever get to observe one of the two: a person is either treated or not, so one potential outcome is always missing.
This is the **fundamental problem of causal inference** — the individual effect is never directly observable.
What we can hope to estimate is an average, the **average treatment effect**:

\[
\text{ATE} = \mathbb{E}[Y(1) - Y(0)].
\]

The tempting shortcut is the naive difference in observed group means,

\[
\mathbb{E}[Y \mid \text{treated}] - \mathbb{E}[Y \mid \text{control}].
\]

This equals the ATE only when treatment is independent of the potential outcomes, written $\{Y(0), Y(1)\} \perp T$.
When sicker people are more likely to be treated, the two groups differ before treatment even acts, and the naive difference confuses that pre-existing gap with the treatment's effect.

## What randomization buys

Flipping a coin to assign treatment is precisely what makes $\{Y(0), Y(1)\} \perp T$ hold by design.
Under [random assignment](experimental-design.md) the treated and control groups are **exchangeable**: measured *and* unmeasured confounders are balanced between them in expectation.
Because nothing systematically separates the groups except the treatment itself, the naive difference in means becomes an unbiased estimate of the ATE.
This is why the **randomized controlled trial** is the gold standard for causal claims — the design, not a clever model, is what removes confounding.

## When you cannot randomize

Most epidemiological questions cannot be settled by a trial, so we lean on observational strategies, each buying identification with an assumption.

- **Adjust for measured confounders.** Stratify or fit a [regression](linear-regression.md) that includes the confounders, estimating the effect within levels of them.
- **Find a natural experiment.** Use an [instrumental variable](instrumental-variables.md) — a factor that shifts the exposure but affects the outcome only through it; [Mendelian randomization](mendelian-randomization.md) is the genetic special case, using inherited variants as the instrument.
- **Other quasi-experimental designs.** Matching pairs treated and control units on their covariates; difference-in-differences compares changes over time between an exposed and an unexposed group; regression discontinuity exploits a sharp cutoff that assigns treatment.

The Achilles' heel of every adjustment method is the assumption of **no unmeasured confounding** — that you have measured and controlled for every common cause.
This assumption cannot be checked from the data, which is why careful studies report a **sensitivity analysis** asking how strong an unmeasured confounder would have to be to overturn the conclusion.

## A worked example: confounding and adjustment

Here a confounder $Z$ raises both the chance of treatment and the outcome.
The naive difference in means is therefore biased upward, but a regression that includes $Z$ recovers the true effect of $2$.

```r
set.seed(1)
n  <- 5000
Z  <- rnorm(n)                                  # confounder
T  <- rbinom(n, 1, plogis(1.5 * Z))             # P(treat) rises with Z
Y  <- 2 * T + 3 * Z + rnorm(n)                  # true treatment effect = 2

naive <- mean(Y[T == 1]) - mean(Y[T == 0])      # biased (~3.4)
adj   <- coef(lm(Y ~ T + Z))["T"]               # ~2.0
c(naive = naive, adjusted = adj)
```

```python
import numpy as np

rng = np.random.default_rng(1)
n = 5000
true_effect = 2.0

Z = rng.normal(size=n)                                   # confounder
p = 1 / (1 + np.exp(-1.5 * Z))                           # P(treat) rises with Z
T = rng.binomial(1, p)
Y = true_effect * T + 3 * Z + rng.normal(size=n)         # true effect = 2

# naive difference in means (ignores Z) -> biased
naive = Y[T == 1].mean() - Y[T == 0].mean()

# adjust for Z via least squares: Y ~ 1 + T + Z, take the T coefficient
X = np.column_stack([np.ones(n), T, Z])
beta, *_ = np.linalg.lstsq(X, Y, rcond=None)
adjusted = beta[1]

print(f"true effect     = {true_effect:.3f}")   # true effect     = 2.000
print(f"naive estimate  = {naive:.3f}")         # naive estimate  = 3.404  (biased)
print(f"adjusted (T+Z)  = {adjusted:.3f}")      # adjusted (T+Z)  = 1.998  (~true)
print(f"naive bias      = {naive - true_effect:.3f}")  # naive bias  = 1.404
```

```julia
using Random, GLM, DataFrames

Random.seed!(1)
n = 5000
Z = randn(n)                                     # confounder
p = 1 ./ (1 .+ exp.(-1.5 .* Z))                  # P(treat) rises with Z
T = Float64.(rand(n) .< p)
Y = 2 .* T .+ 3 .* Z .+ randn(n)                 # true effect = 2

naive = mean(Y[T .== 1]) - mean(Y[T .== 0])      # biased
adj   = coef(lm(@formula(Y ~ T + Z), DataFrame(; Y, T, Z)))[2]  # ~2.0
println((naive = naive, adjusted = adj))
```

The naive estimate lands well above the truth because treated units also tend to have high $Z$; putting $Z$ in the model closes that path and returns the true effect.

## Why it matters

Policy and clinical decisions are causal questions — will this drug lower mortality, will this intervention reduce disease?
Getting the causal structure right — which variables are confounders to adjust for, which are colliders to leave alone, and what estimand you are actually after — matters far more than the sophistication of the model fitted on top of it.

## Related

- [Instrumental Variables](instrumental-variables.md)
- [Mendelian Randomization](mendelian-randomization.md)
- [Experimental Design](experimental-design.md)
- [Linear Regression](linear-regression.md)
- [Hypothesis Testing](hypothesis-testing.md)
- [Quantitative Methods](../math.md)
