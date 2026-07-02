---
title: "Survival Analysis"
---

# Survival Analysis

Survival analysis models the time until an event happens: time to death, time to infection, time to clearance of a pathogen, or time to relapse.
Its defining feature is **censoring** — for some subjects the event has not occurred by the end of follow-up, so we know only that their survival time exceeds some value.

## Time-to-event data and censoring

Let $T\ge 0$ be a random time until the event of interest.
In most studies we do not observe every $T$ exactly.
A subject who is still event-free when the study ends, or who drops out, is **right-censored**: we know $T$ is larger than the last time we saw them, but not by how much.

Throwing censored subjects away, or treating their last-seen time as an event, both bias the results.
The methods below are built to use censored observations correctly — a censored subject contributes information right up to the moment they leave the risk set.

## The core functions

Everything in survival analysis can be written in terms of four interchangeable functions.

The **survival function** is the probability of surviving beyond time $t$: \[ S(t) = \Pr(T > t) = 1 - F(t), \] where $F$ is the cumulative distribution function.
It starts at $S(0)=1$ and decreases toward $0$.

The **probability density** $f(t) = -S'(t)$ describes how event times are distributed (see [derivatives](derivatives.md)).

The **hazard** is the instantaneous event rate *given survival so far*: \[ h(t) = \frac{f(t)}{S(t)} = \lim_{\Delta t \to 0} \frac{\Pr(t \le T < t+\Delta t \mid T \ge t)}{\Delta t}. \] The conditioning on $T \ge t$ is what makes the hazard the natural quantity for time-to-event data: it is the risk faced by those still at risk.

The **cumulative hazard** integrates the hazard over time (see [integrals](integrals.md)): \[ H(t) = \int_0^t h(u)\,du. \]

### The fundamental identity

These are not four independent objects.
Because $h(t) = f(t)/S(t) = -S'(t)/S(t) = -\dfrac{d}{dt}\log S(t)$, integrating both sides gives \[ H(t) = -\log S(t) \qquad\Longleftrightarrow\qquad S(t) = e^{-H(t)}. \] Know any one of $S$, $f$, $h$, or $H$ and you know all four.

## Parametric models

### The exponential model

The simplest model assumes a **constant hazard** $h(t) = \lambda$.
Then $H(t) = \lambda t$ and, by the identity above, \[ S(t) = e^{-\lambda t}, \] so event times follow the [exponential distribution](exponential-distribution.md) with rate $\lambda$.
A constant hazard means the process is memoryless: the risk of the event next month does not depend on how long a subject has already survived.

### The Weibull generalization

Real hazards often rise or fall over time (mortality climbs with age; post-surgical risk falls as patients recover).
The **Weibull** model relaxes the constant-hazard assumption to a power of time, \[ h(t) = \lambda p\, t^{\,p-1}, \] which gives an increasing hazard for shape $p>1$, a decreasing hazard for $p<1$, and reduces to the exponential when $p=1$.

## The Kaplan–Meier estimator

Often we do not want to assume any parametric form.
The **Kaplan–Meier** (product-limit) estimator is a nonparametric estimate of $S(t)$ that handles censoring automatically.

Order the distinct event times $t_1 < t_2 < \cdots$.
At each $t_i$ let $d_i$ be the number of events and $n_i$ the number **at risk** (still under observation just before $t_i$).
The estimate is a product of conditional survival probabilities: \[ \hat S(t) = \prod_{t_i \le t}\left(1 - \frac{d_i}{n_i}\right). \] The result is a right-continuous step function that drops only at observed event times.
Censored subjects never cause a drop; they simply reduce the risk set $n_i$ at later times, which is exactly how their partial information enters.

### Comparing groups: the log-rank test

To ask whether two groups (say, treated vs. control) have different survival, compare their Kaplan–Meier curves with the **log-rank test**.
At each event time it contrasts the observed number of events in a group with the number expected if the two groups shared a common hazard, then accumulates these into a single chi-squared statistic.
It is a [hypothesis test](hypothesis-testing.md) of the null that the two survival curves are the same, and it is most powerful when hazards are proportional (the assumption behind [Cox regression](cox-regression.md)).

## Worked example: Kaplan–Meier by hand

Six patients are followed (months); a `+` marks a right-censored time: \[ 3,\quad 5,\quad 5,\quad 7^{+},\quad 9,\quad 12^{+}. \] So there are events at 3, 5 (two of them), and 9, with censoring at 7 and 12.
We build the estimate one event time at a time.

| $t_i$ | at risk $n_i$ | events $d_i$ | $1-\dfrac{d_i}{n_i}$ | $\hat S(t_i)$ |
|-------|---------------|--------------|----------------------|---------------|
| 3     | 6             | 1            | $5/6$                | $0.833$       |
| 5     | 5             | 2            | $3/5$                | $0.833\times0.6=0.500$ |
| 9     | 2             | 1            | $1/2$                | $0.500\times0.5=0.250$ |

Reading off the risk set: at $t=5$ one patient has already had the event (the one at 3), leaving $n_2=5$.
By $t=9$ the events at 3 and 5 (three patients) and the censored patient at 7 have all left, leaving only $n_3=2$ at risk.
The censored time at 7 produces **no drop** in $\hat S$; it only shrinks the later risk set.

The resulting curve is \[ \hat S(t) = \begin{cases} 1 & 0 \le t < 3,\\ 0.833 & 3 \le t < 5,\\ 0.500 & 5 \le t < 9,\\ 0.250 & t \ge 9, \end{cases} \] and because the last observation (at 12) is censored, the estimate stays at $0.250$ rather than falling to zero.

## In code

### R

```r
library(survival)

# time = follow-up time, status = 1 event, 0 censored
time   <- c(3, 5, 5, 7, 9, 12)
status <- c(1, 1, 1, 0, 1, 0)

fit <- survfit(Surv(time, status) ~ 1)
summary(fit)
# survival at t=3 -> 0.833, t=5 -> 0.500, t=9 -> 0.250 (matches the table)

# Two-group comparison with the log-rank test
grp <- c("A","A","B","A","B","B")
survdiff(Surv(time, status) ~ grp)   # chi-squared statistic and p-value
```

### Python

```python
import numpy as np
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

time   = np.array([3, 5, 5, 7, 9, 12])
status = np.array([1, 1, 1, 0, 1, 0])   # 1 = event, 0 = censored

kmf = KaplanMeierFitter()
kmf.fit(time, event_observed=status)
print(kmf.survival_function_)   # 0.833 at 3, 0.500 at 5, 0.250 at 9

grp = np.array(["A","A","B","A","B","B"])
res = logrank_test(time[grp=="A"], time[grp=="B"],
                   status[grp=="A"], status[grp=="B"])
print(res.p_value)
```

### Julia

```julia
using Survival

time   = [3, 5, 5, 7, 9, 12]
status = Bool[1, 1, 1, 0, 1, 0]   # true = event, false = censored

km = fit(KaplanMeier, time, status)
# km.survival holds the step estimates: 0.833, 0.500, 0.250
println(km.survival)
```

## Why it matters

Survival analysis is the standard toolkit whenever the outcome is *how long until* something happens and follow-up is incomplete — clinical trials, infectious-disease natural history, reliability engineering.
The survival, hazard, and cumulative-hazard functions are a single object viewed three ways, and the Kaplan–Meier estimator plus the log-rank test give an assumption-light description and comparison of survival curves that respect censoring.
These ideas are the foundation for regression models such as Cox proportional hazards.

## Related

- [Cox Proportional Hazards Regression](cox-regression.md)
- [Exponential Distribution](exponential-distribution.md)
- [Hypothesis Testing](hypothesis-testing.md)
- [Probability Basics](probability-basics.md)
- [Integrals](integrals.md)
- [Quantitative Methods](../math.md)
