---
title: "G-Estimation"
description: "G-estimation of structural nested models: the treatment-free outcome, the estimating equation, and its place among Robins' g-methods for time-varying confounding."
---

# G-Estimation

G-estimation is the third of **Robins' g-methods** — alongside the g-formula (standardization) and [inverse-probability weighting](inverse-probability-weighting.md) of marginal structural models — and the one that feels least like ordinary regression.
It estimates the parameters of a **structural nested model** by asking a clean counterfactual question: *what value of the treatment effect would make treatment look unrelated to the outcome it would have had under no treatment?* Like IPW, it is built for [time-varying confounding](inverse-probability-weighting.md); unlike IPW, it handles effect modification gracefully and is often more efficient.

![G-estimation solves for the effect ψ that makes the treatment-free outcome H(ψ) = Y − ψA unrelated to treatment given the confounder: the coefficient on H in a logistic model for A crosses zero at about −2, the true effect.](../assets/figures/gest-score.svg "fig:gest")

## The treatment-free outcome

A **structural nested mean model** parameterizes the effect of treatment as a *blip*: how much treatment shifts the mean outcome relative to never being treated.
In the simplest one-parameter form, the effect of a binary $A$ is $\psi$ per unit, and the **treatment-free (counterfactual) outcome** is

\[
H(\psi) = Y - \psi A,
\]

the outcome you would have seen under no treatment — *if* $\psi$ is the true effect.
Under no unmeasured confounding, that counterfactual outcome is independent of the treatment actually received, **conditional on the confounders** $L$: treatment was assigned based on $L$, not on the untreated potential outcome.

## The estimating equation

G-estimation turns that independence into an equation to solve.
For a candidate $\psi$, compute $H(\psi)$ and test whether it still predicts treatment given $L$ — for instance, via the coefficient on $H(\psi)$ in a logistic regression of $A$ on $L$ and $H(\psi)$.
The **g-estimate** $\hat\psi$ is the value that drives that coefficient to zero ([@fig:gest]):

\[
\hat\psi : \quad A \;\perp\; H(\psi) \mid L.
\]

Because the criterion is a single monotone function of $\psi$, a grid search or a bisection finds it immediately, and inverting the test gives a confidence interval.
The logic relies on **rank preservation** in its simplest form, but the mean-model version needs only the conditional-independence assumption above.

## One of three g-methods

On the running confounded example (true effect $-2$), g-estimation, the g-formula, and IPW all recover the truth while the naive comparison is badly biased ([@fig:gmethods]).
They differ in *what they model*:

- **g-formula** models the **outcome** (standardize predicted outcomes over the confounder distribution);
- **IPW** models the **treatment** (reweight by the inverse propensity);
- **g-estimation** also models the **treatment**, but through the structural nested model, which makes doubly-robust and effect-modification extensions natural.

![On the confounded example, the naive difference is biased toward zero while the g-formula, IPW of a marginal structural model, and g-estimation all recover the true effect of −2 — three routes to the same causal target.](../assets/figures/gest-methods.svg "fig:gmethods")

## A worked example

```python
import numpy as np
import statsmodels.api as sm

rng = np.random.default_rng(2)
n = 4000
L = rng.normal(0, 1, n)
A = rng.binomial(1, 1 / (1 + np.exp(-0.8 * L)))
Y = -2.0 * A + 1.5 * L + rng.normal(0, 1, n)     # true effect = -2

# g-estimation: find psi such that H(psi) = Y - psi*A is unrelated to A given L
def coef_on_H(psi):
    H = Y - psi * A
    return sm.Logit(A, sm.add_constant(np.c_[L, H])).fit(disp=0).params[-1]

lo, hi = -4.0, 0.0                                # bisection for the zero crossing
for _ in range(40):
    mid = (lo + hi) / 2
    if coef_on_H(mid) > 0:
        lo = mid
    else:
        hi = mid
print(f"g-estimate psi = {(lo + hi) / 2:+.2f}   (true -2.00)")
```

<!-- python-output:auto -->
```text
g-estimate psi = -1.98   (true -2.00)
```
<!-- /python-output:auto -->

The estimating equation lands on $-2$: the effect that, once subtracted off, leaves treatment and the treatment-free outcome unrelated given $L$.

## In code

### R

```r
# gesttools / DTRreg implement g-estimation of structural nested models,
# including the time-varying, multi-stage case
library(DTRreg)
fit <- DTRreg(Y, blip.mod = list(~1), treat.mod = list(A ~ L),
              tf.mod = list(~L), data = d, method = "gest")
summary(fit)     # the blip (effect) parameter psi
```

### Julia

```julia
using GLM, DataFrames
coef_on_H(psi) = coef(glm(@formula(A ~ L + H), transform(d, :Y => (y -> y .- psi .* d.A) => :H),
                         Binomial()))[end]
# bisect coef_on_H over psi to its zero crossing
```

## Why it matters

When treatment and a time-varying confounder chase each other over time — CD4 count driving HIV therapy while therapy raises CD4, disease severity driving a drug while the drug changes severity — the ordinary instinct to "adjust for the confounder" fails, and the g-methods are the correct tools.
G-estimation is the member of that family that most directly targets the causal *effect* rather than a weighted average, extends cleanly to effect modification (does the effect differ by subgroup?), and underlies the analysis of **dynamic treatment regimes** — rules that say *treat when the biomarker crosses a threshold*.
It is more demanding to implement than IPW, which is why it is less common, but on exactly the problems these methods exist for, it is often the more efficient and flexible choice.

## Related

- [Inverse Probability Weighting](inverse-probability-weighting.md)
- [Propensity Scores](propensity-scores.md)
- [Causal Inference](causal-inference.md)
- [Logistic Regression](logistic-regression.md)
- [Linear Regression](linear-regression.md)
- [Quantitative Methods](../math.md)
