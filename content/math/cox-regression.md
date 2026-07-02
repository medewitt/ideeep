---
title: "Cox Proportional Hazards Regression"
---

# Cox Proportional Hazards Regression

Cox regression relates covariates — treatment, age, viral load — to the time until an event such as death, infection, or clearance.
It is the most widely used regression model for censored time-to-event data, and its coefficients translate directly into **hazard ratios**.

## The model

Cox regression is a model for the [hazard](survival-analysis.md), the instantaneous event rate among those still at risk.
For a subject with covariate vector $x$ it assumes \[ h(t \mid x) = h_0(t)\, e^{x^\top\beta}. \] Two pieces multiply together:

- a **baseline hazard** $h_0(t)$ that captures how risk changes over time, shared by everyone;
- a **relative risk** $e^{x^\top\beta}$ that scales that baseline up or down according to the covariates.

The model is called **semiparametric** because $h_0(t)$ is left completely unspecified — we never write down a formula for it — while the covariate effect $e^{x^\top\beta}$ has a parametric (log-linear) form.
The exponential link keeps the hazard positive for any values of $\beta$, much as it does in [logistic regression](logistic-regression.md).

## Hazard ratios

The coefficients are interpreted through exponentiation.
Compare two subjects differing by one unit in covariate $x_j$ and identical otherwise.
The baseline $h_0(t)$ cancels, leaving the **hazard ratio** \[ \mathrm{HR}_j = \frac{h(t\mid x_j+1)}{h(t\mid x_j)} = e^{\beta_j}, \] a single number that does not depend on $t$.
So $e^{\beta_j}$ is the multiplicative effect of a one-unit increase in $x_j$ on the instantaneous risk:

- $e^{\beta_j} > 1$ ($\beta_j > 0$): higher hazard, shorter survival;
- $e^{\beta_j} = 1$ ($\beta_j = 0$): no effect;
- $e^{\beta_j} < 1$ ($\beta_j < 0$): lower hazard, longer survival.

## The proportional-hazards assumption

Because the baseline cancels, the hazard ratio between any two covariate profiles is **constant over time** — this is the *proportional-hazards* assumption.
Graphically, the hazard for one group is a fixed multiple of the hazard for another at every $t$; their hazard curves never cross.

The assumption can fail — for instance, a surgery with high early risk but a long-term survival benefit has a hazard ratio that starts above 1 and falls below it.
Common checks include:

- testing whether **scaled Schoenfeld residuals** trend with time (a nonzero slope signals a time-varying effect);
- inspecting $\log(-\log \hat S(t))$ plots across groups, which should be roughly parallel;
- adding a covariate-by-time interaction and testing whether it is nonzero (a [hypothesis test](hypothesis-testing.md) of proportionality).

When the assumption is untenable, remedies include stratifying on the offending variable or fitting explicitly time-varying coefficients.

## Estimation by partial likelihood

How can we estimate $\beta$ without ever specifying $h_0(t)$?
Cox's insight was the **partial likelihood**.
At each observed event time $t_i$, condition on the fact that *one* event happened among the risk set $R(t_i)$ (everyone still under observation), and ask which subject it was.
Under the model, the probability that the subject who actually failed, with covariates $x_i$, is the one to fail is \[ \frac{e^{x_i^\top\beta}}{\sum_{k \in R(t_i)} e^{x_k^\top\beta}}. \] The baseline hazard cancels from every term, so it disappears entirely.
Multiplying these contributions over all event times gives the partial likelihood \[ L(\beta) = \prod_{i:\,\text{event}} \frac{e^{x_i^\top\beta}}{\sum_{k \in R(t_i)} e^{x_k^\top\beta}}, \] which is maximized over $\beta$ by [maximum likelihood](maximum-likelihood.md) methods.
Only the *order* of the event times matters, not their spacing, which is precisely why $h_0(t)$ need never be modeled.
When events are far enough apart that the constant-hazard picture holds locally, the model connects back to the [exponential distribution](exponential-distribution.md).

## Worked example: reading a coefficient

Suppose a trial fits a single covariate `treatment` (0 = placebo, 1 = drug) and reports $\hat\beta = -0.41$.
The hazard ratio is \[ \mathrm{HR} = e^{-0.41} \approx 0.66. \] Patients on the drug face about a **34% lower** instantaneous risk of the event at any given time ($1 - 0.66 = 0.34$).

Now suppose a covariate `stage` has $\hat\beta = 0.405$, giving $\mathrm{HR} = e^{0.405} \approx 1.5$.
Each one-step increase in disease stage multiplies the hazard by $1.5$ — a **50% higher** instantaneous risk.
A 95% confidence interval that excludes $\mathrm{HR}=1$ (equivalently $\beta=0$) indicates a statistically significant effect.
Note that a hazard ratio describes the *rate* of the event, not a difference in mean survival time directly.

## In code

### R

```r
library(survival)

# Built-in ovarian cancer data: futime = time, fustat = event indicator
fit <- coxph(Surv(futime, fustat) ~ age + rx, data = ovarian)
summary(fit)          # coef, exp(coef) = hazard ratio, and p-values

# Check proportional hazards via scaled Schoenfeld residuals
cox.zph(fit)          # a small p-value flags a PH violation
```

### Python

```python
from lifelines import CoxPHFitter
from lifelines.datasets import load_rossi

df = load_rossi()     # 'week' = time, 'arrest' = event indicator
cph = CoxPHFitter()
cph.fit(df, duration_col="week", event_col="arrest")
cph.print_summary()   # coef and exp(coef) = hazard ratio per covariate

cph.check_assumptions(df)   # proportional-hazards diagnostics
```

### Julia

```julia
using Survival, DataFrames

# EventTime wraps (time, event-occurred?) for each subject
df = DataFrame(time = [4, 6, 8, 10, 12, 14],
               status = Bool[1, 0, 1, 1, 0, 1],
               x = [0, 1, 0, 1, 1, 0])
df.et = EventTime.(df.time, df.status)

model = coxph(@formula(et ~ x), df)
coef(model)                 # beta; exp.(coef(model)) gives hazard ratios
```

## Why it matters

Cox regression is the default tool for quantifying how covariates affect survival while accounting for censoring, without committing to a shape for the baseline hazard.
Its output — hazard ratios with confidence intervals — is the standard language of clinical and epidemiological reporting, from treatment effects to prognostic factors.
Understanding the proportional-hazards assumption and the partial-likelihood machinery is what lets you fit these models responsibly and know when they break.

## Related

- [Survival Analysis](survival-analysis.md)
- [Logistic Regression](logistic-regression.md)
- [Maximum Likelihood](maximum-likelihood.md)
- [Exponential Distribution](exponential-distribution.md)
- [Hypothesis Testing](hypothesis-testing.md)
- [Quantitative Methods](../math.md)
