---
title: "Uncertainty, Calibration, and Conformal Prediction"
description: "Making predictions honest about what they do not know — separating the kinds of uncertainty, calibrating probabilities, and building distribution-free prediction sets with a coverage guarantee."
---

# Uncertainty, Calibration, and Conformal Prediction

A prediction without honest uncertainty is a liability, nowhere more than in health, where a confident wrong answer can cost a life.
A model that says "90% risk" should be right about nine times in ten it says so, and a forecast of next week's cases should come with an interval that actually contains the truth about as often as it claims.
This page covers three linked ideas that make predictions trustworthy: the **two kinds of uncertainty** a model faces, **calibration** so that probabilities mean what they say, and **conformal prediction**, which wraps any model in prediction sets that carry a mathematical coverage guarantee.

![Left: a reliability diagram — an over-confident classifier's predicted probabilities do not match observed frequencies (curve off the diagonal), while a calibrated model tracks it. Right: split-conformal prediction bands around a regression, calibrated to cover 90% of new points with a distribution-free guarantee, widening where the data are noisier.](../assets/figures/uncertainty-calibration-conformal.svg)

## Two kinds of uncertainty

Not all uncertainty is the same, and the distinction changes what you can do about it.
**Aleatoric** uncertainty is irreducible noise in the world — two patients with identical records can have different outcomes — and no amount of data removes it; the best a model can do is report it honestly.
**Epistemic** uncertainty is the model's own ignorance, from limited or unrepresentative data, and it *shrinks* as you collect more or move back toward where the training data lived.
The practical consequence is that a model should be *more* uncertain about a patient unlike any it trained on (high epistemic uncertainty) than about a typical one — and a model that is confidently wrong on out-of-distribution inputs, as many neural networks are, is failing to represent its epistemic uncertainty.
[Bayesian inference](bayesian-inference.md), deep ensembles, and Monte-Carlo dropout are the usual tools for estimating it.

## Calibration

A probabilistic prediction is **calibrated** if it means what it says: among all the cases a model assigns probability $p$, a fraction close to $p$ should actually be positive.
You check this with a **reliability diagram** (left of the figure): bin predictions by their stated probability and plot the observed frequency in each bin against the mean predicted probability; a calibrated model tracks the diagonal, while an **over-confident** one — predicting probabilities too close to 0 and 1 — bows away from it.
The **expected calibration error** (ECE) summarizes the gap as a weighted average distance from the diagonal.
Calibration is one half of a good forecast; the other is **sharpness** (confident, concentrated predictions), and a [proper scoring rule](proper-scoring-rules.md) like the Brier or log score rewards both at once.
When a model discriminates well but is miscalibrated, you **recalibrate** it after the fact — **Platt scaling** (fit a logistic on its scores), **isotonic regression** (a nonparametric monotone fit), or **temperature scaling** for neural networks (divide the logits by a single learned scalar) — using a held-out set, which fixes the probabilities without touching the ranking.
This is the same reasoning behind a diagnostic test's [predictive values](diagnostic-testing.md): a score is only as useful as the real-world frequency it corresponds to.

## Conformal prediction

Calibration makes a probability honest; **conformal prediction** goes further and returns a *set* of outcomes guaranteed to contain the truth with a chosen probability — for any model, with no distributional assumptions, from finite data.
The most common recipe is **split (inductive) conformal**.
Set aside a **calibration** set the model did not train on, and for each of its points compute a **nonconformity score** — how surprising the true label is under the model, e.g. the absolute residual $|y - \hat f(x)|$ for regression.
Take the $\lceil (n+1)(1-\alpha)\rceil / n$ empirical quantile $\hat q$ of those scores, and for a new input output the prediction set of all labels whose nonconformity is $\le \hat q$ — an interval $\hat f(x) \pm \hat q$ for regression, or a set of plausible classes for classification.
Under only the assumption that the data are **exchangeable**, this set satisfies a finite-sample guarantee, \[ \mathbb{P}\bigl(Y_{\text{new}} \in \hat C(X_{\text{new}})\bigr) \ge 1 - \alpha, \label{eq:coverage} \] the marginal coverage shown holding on the right of the figure, where a 90%-target band covers about 90% of held-out points.
Making the score adaptive — for instance dividing the residual by a local noise estimate — lets the interval **widen where the data are noisy** and tighten where they are clean, as the figure's band does, without breaking the guarantee.

> [!WARNING]
> The coverage guarantee [@eq:coverage] is **marginal**, averaged over all inputs, not **conditional** on a particular one — the interval for a specific unusual patient may under-cover even while the overall 90% holds.
> And the guarantee rests on **exchangeability**, which a distribution shift breaks: deploy a conformal model on a new population or a new season and its coverage can silently degrade, so the assumption must be monitored, not assumed.

## A worked example

Fit any regression model, then hold out $500$ calibration points and record each absolute residual $|y_i - \hat f(x_i)|$.
For 90% coverage ($\alpha = 0.1$), the conformal quantile is the $\lceil 501 \times 0.9\rceil = 451$st smallest of those $500$ residuals — say it is $0.62$.
Then for any new $x$, the interval $\hat f(x) \pm 0.62$ is guaranteed to contain the true $y$ at least 90% of the time over future exchangeable data — regardless of whether the model is a linear fit, a [random forest](tree-ensembles.md), or a [neural network](neural-networks.md), and regardless of the noise distribution.
The price is only a held-out calibration set and the honesty to report an interval instead of a point.

## In code

### Python

Split-conformal prediction turns any model's residuals into an interval with guaranteed coverage — here the coverage lands near the 90% target on held-out data:

```python
import numpy as np
rng = np.random.default_rng(0)

f = lambda x: np.sin(x)                          # the (already fitted) mean model
n = 1000
x = rng.uniform(0, 6, n)
y = f(x) + rng.normal(0, 0.3, n)                 # homoscedastic noise for simplicity
cal, test = slice(0, 500), slice(500, 1000)      # calibration / test split

alpha = 0.10
scores = np.abs(y[cal] - f(x[cal]))              # nonconformity = absolute residual
k = int(np.ceil((500 + 1) * (1 - alpha)))        # finite-sample quantile rank
q = np.sort(scores)[k - 1]
covered = np.abs(y[test] - f(x[test])) <= q      # is the truth inside f(x) ± q ?
print(f"interval half-width q = {q:.3f}")
print(f"target coverage {100*(1-alpha):.0f}%, achieved {100*covered.mean():.1f}%")
```

<!-- python-output:auto -->
```text
interval half-width q = 0.503
target coverage 90%, achieved 90.0%
```
<!-- /python-output:auto -->

Calibration is checked with a reliability curve and fixed by recalibration:

```python
from sklearn.calibration import calibration_curve
p_true = rng.uniform(0, 1, 3000)
labels = (rng.uniform(size=3000) < p_true).astype(int)
logit = np.log(p_true / (1 - p_true))
p_over = 1 / (1 + np.exp(-1.8 * logit))          # sharpened logits = over-confident
frac, mean_pred = calibration_curve(labels, p_over, n_bins=10)
print(f"expected calibration error (over-confident): {np.mean(np.abs(frac - mean_pred)):.3f}")
```

<!-- python-output:auto -->
```text
expected calibration error (over-confident): 0.072
```
<!-- /python-output:auto -->

The `mapie` library provides conformal prediction for scikit-learn models directly (illustrative — outside the build's libraries, so shown, not run):

```python
# no-run
from mapie.regression import MapieRegressor
mapie = MapieRegressor(my_model, method="plus").fit(X_train, y_train)
y_pred, y_interval = mapie.predict(X_test, alpha=0.1)   # 90% prediction intervals
```

### R

```r
# probably for calibration; the conformalInference / probably packages for conformal.
library(probably)
cal_plot_breaks(data, truth = outcome, estimate = .pred_pos)   # reliability diagram
# split-conformal by hand: quantile of calibration-set residuals
q <- quantile(abs(y_cal - predict(model, x_cal)), 0.9, type = 1)
```

### Julia

```julia
# ConformalPrediction.jl wraps MLJ models with conformal guarantees.
using ConformalPrediction, MLJ
conf_model = conformal_model(model; coverage = 0.9)
mach = machine(conf_model, X, y) |> fit!
predict(mach, Xnew)     # returns prediction sets / intervals
```

## Why it matters

Uncertainty is the difference between a model that informs a decision and one that misleads it.
A calibrated risk score can be compared against a treatment threshold and trusted to mean what it says; an [outbreak forecast](reproduction-number-rt.md) with valid intervals tells a public-health team how wide to plan for, not just a central guess; and conformal prediction gives even a black-box [deep-learning](neural-networks.md) model a coverage guarantee a decision-maker can rely on, without retraining it.
The recurring caution is distribution shift: calibration and conformal coverage are promises about data that look like the calibration data, and a new variant, population, or season can void them — which is why honest uncertainty is paired with monitoring, and why every model on this site is asked to say not just what it predicts, but how much it should be believed.

## Related

- [Proper Scoring Rules](proper-scoring-rules.md)
- [Diagnostic Testing and Screening](diagnostic-testing.md)
- [Bayesian Inference](bayesian-inference.md)
- [Model Interpretability and SHAP](interpretability-shap.md)
- [Overfitting, Regularization, and Cross-Validation](overfitting-regularization.md)
- [The Effective Reproduction Number and Forecasting](reproduction-number-rt.md)
- [Quantitative Methods](../math.md)
