---
title: "Measures of Association and Impact"
description: "From frequency measures to risk ratios, odds ratios, and attributable fractions — what each number means and when the odds ratio stops tracking the risk ratio."
---

# Measures of Association and Impact

Once a study is designed and the cases are counted, the numbers have to be turned into quantities that mean something.
Three questions organize the whole vocabulary: how common is the outcome, how much does exposure change it, and how much disease would we prevent by removing the exposure.
The answers are the frequency measures, the measures of association, and the measures of impact.

![A 2x2 table filled with cell counts and its risk ratio, odds ratio, and risk difference, beside a curve showing the odds ratio inflating above a fixed risk ratio of two as the baseline risk rises.](../assets/figures/measures-of-association-and-impact.svg)

## Frequency measures

Three measures describe how often the outcome occurs.
The **incidence proportion**, or **risk**, is the fraction of an at-risk group that develops the outcome over a period, a probability between $0$ and $1$.
The **incidence rate** divides new cases by the person-time observed, so its units are cases per person-time and it can exceed $1$; it is the right measure when follow-up varies across people.
**Prevalence** is the fraction of the population that has the outcome at a moment, and it reflects both how fast cases arise and how long they last.

For a stable condition these connect through a simple relation,

\[
\text{prevalence} \approx \text{incidence rate} \times \text{average duration},
\]

which explains why a highly infectious but short illness can have low prevalence while a mild chronic one has high prevalence.

## Measures of association

Association measures compare the outcome frequency between exposed and unexposed groups.
Write the exposed risk as $p_1$ and the unexposed risk as $p_0$.
The **risk ratio** $\text{RR} = p_1/p_0$ and the **rate ratio** (the same idea for rates) are multiplicative: an $\text{RR}$ of $3$ means the exposure triples the risk.
The **odds ratio** compares odds instead of risks,

\[
\text{OR} = \frac{p_1/(1-p_1)}{p_0/(1-p_0)},
\]

and it is the measure a case-control study returns and the quantity a logistic regression models (see [Generalized Linear Models](../math/generalized-linear-models.md)).
The **risk difference** $\text{RD} = p_1 - p_0$ is additive and stays on the scale of absolute risk, which is what patients and public-health budgets actually experience.

## When the odds ratio tracks the risk ratio

The odds ratio and the risk ratio agree only when the outcome is rare.
As $p_1$ and $p_0$ both shrink toward zero, $1-p_1$ and $1-p_0$ approach $1$ and the odds ratio collapses onto the risk ratio.
When the outcome is common, the odds ratio sits **farther from $1$** than the risk ratio, so it overstates the association if read as if it were a risk ratio.

This gap is sharpened by **non-collapsibility**: the odds ratio can change when you adjust for a covariate that is not a confounder, purely because of the nonlinear odds transformation, whereas the risk ratio and risk difference do not behave this way.
The right panel of the figure fixes the risk ratio at $2$ and shows the odds ratio climbing above it as the baseline risk rises — the same effect that makes a rare-disease case-control study interpretable and a common-outcome one treacherous.

## Measures of impact

Impact measures translate an association into disease you could prevent.
The **attributable fraction in the exposed** is the share of the exposed group's risk that the exposure is responsible for,

\[
\text{AF}_e = \frac{p_1 - p_0}{p_1} = \frac{\text{RR} - 1}{\text{RR}} ,
\]

so with $\text{RR}=3$ two-thirds of disease among the exposed is attributable to the exposure.
The **population attributable fraction** scales this to the whole population by the exposure prevalence $P_e$,

\[
\text{PAF} = \frac{P_e(\text{RR}-1)}{1 + P_e(\text{RR}-1)} ,
\]

and answers what fraction of all cases would vanish if the exposure were removed.
The **number needed to treat** (or, for a protective exposure such as a vaccine, the **number needed to vaccinate**) is the reciprocal of the risk difference, $\text{NNT} = 1/\lvert\text{RD}\rvert$: how many people you must treat or vaccinate to prevent one case.

## A worked example

Take a study of $1000$ exposed and $1000$ unexposed people in which $300$ of the exposed and $100$ of the unexposed develop the outcome, so the $2\times 2$ table holds $a=300$, $b=700$, $c=100$, $d=900$.
The risks are $0.30$ and $0.10$, giving a **risk ratio** of $3.0$ (exposure triples the risk), a **risk difference** of $0.20$ (an extra $20$ cases per $100$ exposed), and an **odds ratio** of $(300\times900)/(700\times100) \approx 3.86$, already noticeably above the risk ratio because this outcome is common.

The **attributable fraction in the exposed** is $(3-1)/3 \approx 0.67$, so two-thirds of disease among the exposed is due to the exposure.
With half the sample exposed, the overall risk is $0.20$ and the **population attributable fraction** is $(0.20-0.10)/0.20 = 0.50$: removing the exposure would prevent half of all cases.
The **number needed to treat** is $1/0.20 = 5$, meaning you would remove the exposure from five people to prevent one case.

## In code

We fill the table once and read every measure off it.

### R

```r
a <- 300; b <- 700; c <- 100; d <- 900

risk_exp   <- a / (a + b)
risk_unexp <- c / (c + d)
rr  <- risk_exp / risk_unexp
or  <- (a * d) / (b * c)
rd  <- risk_exp - risk_unexp
afe <- (rr - 1) / rr
risk_overall <- (a + c) / (a + b + c + d)
paf <- (risk_overall - risk_unexp) / risk_overall

c(RR = rr, OR = or, RD = rd, AFe = afe, PAF = paf, NNT = 1 / rd)
```

### Python

We use [Polars](https://pola.rs) to hold the table, then compute the measures.

```python
import polars as pl

tab = pl.DataFrame({
    "exposure": ["exposed", "unexposed"],
    "cases": [300, 100],
    "noncases": [700, 900],
})
a, c = tab["cases"]
b, d = tab["noncases"]
risk_exp = a / (a + b)
risk_unexp = c / (c + d)
risk_overall = (a + c) / (a + b + c + d)

rr = risk_exp / risk_unexp
odds_ratio = (a * d) / (b * c)
rd = risk_exp - risk_unexp
afe = (rr - 1) / rr
paf = (risk_overall - risk_unexp) / risk_overall

print(f"risk ratio       = {rr:.3f}")
print(f"odds ratio       = {odds_ratio:.3f}")
print(f"risk difference  = {rd:.3f}")
print(f"AF in exposed    = {afe:.3f}")
print(f"pop. attr. frac. = {paf:.3f}")
print(f"number needed    = {1 / rd:.1f}")
```

<!-- python-output:auto -->
```text
risk ratio       = 3.000
odds ratio       = 3.857
risk difference  = 0.200
AF in exposed    = 0.667
pop. attr. frac. = 0.500
number needed    = 5.0
```
<!-- /python-output:auto -->

### Julia

```julia
a, b, c, d = 300, 700, 100, 900

risk_exp   = a / (a + b)
risk_unexp = c / (c + d)
rr  = risk_exp / risk_unexp
or  = (a * d) / (b * c)
rd  = risk_exp - risk_unexp
afe = (rr - 1) / rr
risk_overall = (a + c) / (a + b + c + d)
paf = (risk_overall - risk_unexp) / risk_overall

(RR = rr, OR = or, RD = rd, AFe = afe, PAF = paf, NNT = 1 / rd)
```

## Why it matters

A ratio and a difference can describe the same exposure yet tell public health very different stories.
A large risk ratio for a rare outcome may move few people, while a modest risk difference for a common one can dominate the disease burden, and the population attributable fraction is what tells a program how much illness a control measure could actually erase.
Knowing when the odds ratio still stands in for the risk ratio, and when its non-collapsibility makes it a poor summary of absolute effect, is what keeps an association from being oversold — and it depends directly on the study design that produced the counts in the first place.

## Related

- [Diagnostic Testing and Screening](../math/diagnostic-testing.md)
- [Confidence Intervals](../math/confidence-intervals.md)
- [Generalized Linear Models](../math/generalized-linear-models.md)
- [Epidemiology](../epidemiology.md)
