---
title: "Nowcasting and Reporting Delays"
description: "Why the recent end of an epidemic curve is biased down by reporting delays, and how nowcasting reconstructs the eventual counts from the delay distribution."
---

# Nowcasting and Reporting Delays

The last few points of any epidemic curve lie.
Cases that have already happened have not all been reported yet, so the most recent days always look lower than they truly are, and a curve that seems to be turning over may just be incompletely observed.
Nowcasting is the correction: using what we know about reporting delays to reconstruct the eventual counts for recent dates before all the reports arrive.

![An epidemic curve where the observed recent counts fall away from the eventual counts because reporting for those dates is not yet complete.](../assets/figures/nowcasting.svg)

## Right truncation at the present

Every surveillance event travels through a chain of delays before it is counted: symptom onset to testing, testing to result, result to report.
The consequence is **right truncation**.
For an event that happened $d$ days ago, we have only observed the reports whose delay is shorter than $d$; the longer-delay reports are still in transit.
Far in the past $d$ is large and essentially everything has arrived, so the curve is complete.
Near the present $d$ is small and only the fastest reports are in, so the curve is dragged down, most severely on the very last day.
This is the same right-truncation bias that distorts delay-distribution estimates, discussed in [delay distributions and censoring](delay-distributions-censoring.md).

## The reporting triangle

Line-list data arrive as a two-way table indexed by **event date** and **reporting delay**: how many cases with onset on a given day were reported after 0 days, 1 day, 2 days, and so on.
For dates in the distant past every delay cell is filled, giving a full row.
For recent dates only the short-delay cells are filled, so the lower-right of the table is empty.
The filled part looks like a triangle, which is why this is called the **reporting triangle**, and nowcasting is the task of predicting the missing cells so each recent row can be summed to its eventual total.

## Nowcasting versus forecasting

The two tasks point in opposite directions in time.
**Forecasting** projects the epidemic into the future, predicting cases on dates that have not happened yet (see [epidemic forecasting](epidemic-forecasting.md)).
**Nowcasting** fills in the recent past, predicting the eventual counts for dates that have already happened but are not yet fully reported.
Nowcasting rests on a more secure footing, because those infections already exist and only their reports are pending, whereas a forecast must also anticipate new transmission.
Both matter for $R_t$: without a nowcast the naive drop in recent incidence produces a spurious dip in the [estimated reproduction number](../math/reproduction-number-rt.md) at exactly the moment decision-makers care about most.

## A worked example

Suppose the reporting-delay distribution is known: a fraction of cases is reported the same day, more over the next few days, and essentially all within a week.
Let $F(d)$ be the cumulative fraction reported within $d$ days.
For an event date that occurred $d$ days ago we expect to have observed a fraction $F(d)$ of its eventual cases, so the observed count is $O = F(d)\, C$ where $C$ is the eventual total.
Inverting gives the simplest possible nowcast, a multiplicative correction:

\[
\hat{C} = \frac{O}{F(d)}.
\]

If yesterday's date is only 60% reported and we have counted 30 cases so far, the nowcast is $30 / 0.60 = 50$.
The correction grows as $F(d)$ shrinks toward the present, which is also where it is most uncertain, so nowcasts carry wide intervals on the last day or two.

## In code

### R

```r
p <- c(0.10, 0.30, 0.30, 0.20, 0.10)     # P(delay = 0,1,2,3,4 days)
F <- cumsum(p)

T <- 30; t <- 0:(T - 1)
eventual <- round(20 * exp(0.12 * t))     # eventual counts by event date
lag <- (T - 1) - t
frac <- ifelse(lag >= length(F), 1, F[pmin(lag + 1, length(F))])
observed  <- eventual * frac              # right-truncated curve
corrected <- observed / frac              # multiplicative nowcast

tail(data.frame(t, eventual, observed = round(observed),
                corrected = round(corrected)), 5)
```

### Python

```python
import numpy as np

# Reporting-delay distribution (days from event to report), discretized.
p = np.array([0.10, 0.30, 0.30, 0.20, 0.10])   # P(delay = 0, 1, 2, 3, 4)
F = np.cumsum(p)                                # fraction reported within d days

# A growing epidemic; "today" is the last day, so recent dates are truncated.
T = 30
t = np.arange(T)
eventual = np.round(20 * np.exp(0.12 * t))      # eventual counts by event date

# Fraction of each date's cases reported by today, then correct for it.
lag = (T - 1) - t
frac = np.where(lag >= len(F), 1.0, F[np.clip(lag, 0, len(F) - 1)])
observed = eventual * frac                      # naive, right-truncated
corrected = observed / frac                     # multiplicative nowcast

print("date  eventual  observed  corrected")
for d in range(T - 5, T):
    print(f"{d:4d}  {eventual[d]:8.0f}  {observed[d]:8.0f}  {corrected[d]:9.0f}")
```

<!-- python-output:auto -->
```text
date  eventual  observed  corrected
  25       402       402        402
  26       453       408        453
  27       511       358        511
  28       576       230        576
  29       649        65        649
```
<!-- /python-output:auto -->

The observed counts fall well below the eventual totals for the last few dates, and dividing by the reported fraction recovers them.
With real, noisy reports the correction is approximate rather than exact, which is why nowcasts are reported with uncertainty.

### Julia

```julia
p = [0.10, 0.30, 0.30, 0.20, 0.10]        # P(delay = 0,1,2,3,4 days)
F = cumsum(p)

T = 30; t = 0:(T - 1)
eventual = round.(20 .* exp.(0.12 .* t))
lag = (T - 1) .- t
frac = [l >= length(F) ? 1.0 : F[min(l + 1, length(F))] for l in lag]
observed  = eventual .* frac
corrected = observed ./ frac              # multiplicative nowcast
```

## Why it matters

Acting on the raw tail of an epidemic curve invites the wrong call: a real surge can look like a plateau, and a genuine decline can be hidden by reporting that has caught up.
Nowcasting separates a true change in transmission from an artifact of incomplete reporting, which keeps the recent $R_t$ honest and gives forecasts a trustworthy starting point.
The correction is only as good as the delay distribution behind it, so estimating that distribution well, and updating it as reporting behavior shifts, is where the real work lies.

## Related

- [Delay distributions and censoring](delay-distributions-censoring.md)
- [Epidemiological intervals](epidemiological-intervals.md)
- [The Effective Reproduction Number and Forecasting](../math/reproduction-number-rt.md)
- [Epidemic Forecasting](epidemic-forecasting.md)
- [Epidemiology](../epidemiology.md)
