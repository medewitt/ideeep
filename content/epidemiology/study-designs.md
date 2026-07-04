---
title: "Epidemiologic Study Designs"
description: "How the main observational and experimental designs answer causal questions, what measures of association they yield, and where each is vulnerable to bias."
---

# Epidemiologic Study Designs

Every epidemiologic study is an argument about a cause, built from a particular way of looking at people over time.
The design decides which direction you reason in — from exposure toward outcome, or from outcome back toward exposure — and that choice fixes what you can measure and which biases you must fear.
Getting the design right is the difference between an estimate you can act on and a number that only looks like evidence.

![Schematic of study designs arranged by direction of inquiry and timing: randomized trials and cohorts follow exposure forward to outcome, case-control studies look back from outcome to exposure, and cross-sectional studies take a single snapshot.](../assets/figures/study-designs.svg)

## The two families

Studies split into two families by whether the investigator assigns the exposure.
In an **observational** study you watch exposures that people acquired on their own — a diet, a vaccine received in the community, a mosquito bite.
In an **experimental** study you assign the exposure yourself, most powerfully by randomization, which is what lets a trial claim a causal effect with the fewest assumptions (see [Causal Inference](../math/causal-inference.md)).

Within the observational family the designs differ mainly in their direction of inquiry and their timing relative to the present.

## Cross-sectional studies

A cross-sectional study is a single snapshot: exposure and outcome are measured at the same moment in a sample of the population.
It estimates **prevalence** and can reveal associations cheaply and quickly, which makes it the natural design for a seroprevalence survey after an outbreak.
Because cause and effect are observed together, it usually cannot establish which came first, so it is prone to **reverse causation** — the outcome may have changed the exposure rather than the other way around.

## Cohort studies

A cohort study starts from exposure and follows people forward to see who develops the outcome.
It reasons in the natural causal direction, exposure then outcome, and it yields the frequency measures directly: the **risk** (incidence proportion) in the exposed and the unexposed, and hence a **risk ratio** or, when person-time is tracked, a **rate ratio**.
A **prospective** cohort enrolls people and waits, while a **retrospective** cohort reconstructs an already-assembled cohort from existing records — same logic, different vantage in time.
Cohorts are the workhorse for incidence and for rare exposures, but following enough people to accrue a rare outcome is slow and expensive, and **loss to follow-up** can bias the result if dropout is related to both exposure and outcome.

## Case-control studies

A case-control study inverts the direction: it starts from the outcome, sampling people who have the disease (**cases**) and people who do not (**controls**), then looks back to compare their exposures.
This makes it efficient for **rare outcomes** and for outbreaks, where waiting for cases to accrue in a cohort would be impractical.
Because the outcome is fixed by the sampling, you cannot compute risk directly, so the measure of association is the **odds ratio**.
The main threats are **selection bias** from how controls are chosen and **recall bias**, since cases often remember past exposures more keenly than controls do.

A **nested case-control** study draws its cases and controls from inside an existing cohort, which restores a well-defined source population and reduces selection bias while keeping the efficiency of case-control sampling.
The **test-negative design** is a case-control variant widely used to estimate vaccine effectiveness: among people who present for testing with the same symptoms, it compares vaccination status between those who test positive for the pathogen and those who test negative, which helps balance health-seeking behavior across the two groups.

## Ecological studies

An ecological study compares groups rather than individuals — for example, correlating vaccination coverage against measles incidence across counties.
It is useful for generating hypotheses from routinely collected data, but an association at the group level need not hold at the individual level.
Inferring individual risk from group-level rates is the **ecological fallacy**, and it is the signature weakness of the design.

## Intervention and randomized trials

An intervention study assigns the exposure, and in a **randomized controlled trial** the assignment is by chance.
Randomization makes the treated and untreated groups exchangeable in expectation, so measured and unmeasured **confounders** are balanced and the difference in outcomes estimates the causal effect (see [Experimental Design](../math/experimental-design.md)).
Trials give the strongest causal evidence, but they are costly, sometimes unethical to run for a suspected harm, and can enroll participants unlike the general population, which limits how far the result generalizes.

## The odds ratio as a bridge

The reason a case-control study can stand in for a cohort is a simple algebraic fact: when the outcome is **rare**, the odds ratio approximates the risk ratio.
For exposed risk $p_1$ and unexposed risk $p_0$,

\[
\text{OR} = \frac{p_1/(1-p_1)}{p_0/(1-p_0)} \;\longrightarrow\; \frac{p_1}{p_0} = \text{RR}
\quad\text{as}\quad p_1, p_0 \to 0 .
\]

So a case-control study, which can only return an odds ratio, recovers the risk ratio a cohort would have found — provided the disease is rare enough that the odds and the risk nearly coincide.

## A worked example

Imagine a foodborne outbreak investigated two ways.
As a **cohort**, you follow $10{,}000$ people who ate a suspect food and $10{,}000$ who did not; $200$ of the exposed fall ill (risk $0.020$) against $50$ of the unexposed (risk $0.005$).
The risk ratio is $0.020/0.005 = 4.0$: eating the food quadruples the risk.

Now analyze the same scenario as a **case-control** study using the $250$ cases and a comparison of well people, filling the $2\times 2$ table with $a=200$ exposed cases, $b=9800$ exposed non-cases, $c=50$ unexposed cases, and $d=9950$ unexposed non-cases.
The odds ratio is $ad/bc = (200 \times 9950)/(9800 \times 50) \approx 4.06$, which lands within a whisker of the risk ratio of $4.0$ because the illness is rare in both groups.

## In code

We build the $2\times 2$ table once and compute both measures from it.

### R

```r
a <- 200; b <- 9800; c <- 50; d <- 9950   # exposed/unexposed x case/non-case

risk_exp   <- a / (a + b)
risk_unexp <- c / (c + d)
rr <- risk_exp / risk_unexp
or <- (a * d) / (b * c)

c(risk_exp = risk_exp, risk_unexp = risk_unexp, RR = rr, OR = or)
```

### Python

We use [Polars](https://pola.rs) to hold the table and derive the measures.

```python
import polars as pl

tab = pl.DataFrame({
    "exposure": ["exposed", "unexposed"],
    "cases": [200, 50],
    "noncases": [9800, 9950],
})
tab = tab.with_columns(
    risk=(pl.col("cases") / (pl.col("cases") + pl.col("noncases")))
)
a, c = tab["cases"]
b, d = tab["noncases"]
risk_exp, risk_unexp = tab["risk"]

rr = risk_exp / risk_unexp
odds_ratio = (a * d) / (b * c)
print(f"risk exposed   = {risk_exp:.4f}")
print(f"risk unexposed = {risk_unexp:.4f}")
print(f"risk ratio     = {rr:.3f}")
print(f"odds ratio     = {odds_ratio:.3f}")
```

<!-- python-output:auto -->
```text
risk exposed   = 0.0200
risk unexposed = 0.0050
risk ratio     = 4.000
odds ratio     = 4.061
```
<!-- /python-output:auto -->

The odds ratio comes out just above the risk ratio, the small gap you expect for a rare outcome.

### Julia

```julia
a, b, c, d = 200, 9800, 50, 9950

risk_exp   = a / (a + b)
risk_unexp = c / (c + d)
rr = risk_exp / risk_unexp
or = (a * d) / (b * c)

(risk_exp = risk_exp, risk_unexp = risk_unexp, RR = rr, OR = or)
```

## Why it matters

The design you choose is the first and often the largest determinant of whether an outbreak investigation or an effectiveness study yields a trustworthy number.
A cohort measures risk directly but needs time and cases; a case-control study buys speed for a rare outcome at the price of working in odds and guarding against recall and selection bias; a trial buys the cleanest causal claim at the price of cost and generalizability.
Reading a study well means reading its design first, because the design tells you which biases to interrogate before you believe the estimate — a companion page on measures of association and impact turns these tables into the risk ratios, odds ratios, and attributable fractions you report.

## Related

- [Causal Inference](../math/causal-inference.md)
- [Experimental Design](../math/experimental-design.md)
- [Epidemiological Intervals and Delays](epidemiological-intervals.md)
- [Logistic Regression](../math/logistic-regression.md)
- [Epidemiology](../epidemiology.md)
