---
title: "Experimental Design"
---

# Experimental Design

How data are collected determines what conclusions they can support.
Good experimental design is what lets epidemiologists move from "associated with" toward "causes," and recognizing sources of bias is essential when a true experiment is impossible.

## Experimental vs. observational studies

- In an **experiment**, the investigator actively assigns the exposure or treatment (ideally at random).
  This breaks the link between exposure and confounders and licenses causal claims.
- In an **observational study**, exposure is merely observed as it occurs.
  Associations may be real but can be distorted by confounding, so causal interpretation demands caution.

## Principles of good experiments

- **Randomization** — random assignment balances known *and unknown* confounders across groups in expectation, so differences in outcome can be attributed to the treatment.
- **Control** — a comparison group (placebo or standard care) isolates the treatment effect from background trends.
- **Replication** — multiple independent units per condition let us estimate [variability](measures-of-variability.md) and gain power.
- **Blocking** — grouping similar units (e.g., by age band or site) and randomizing within blocks removes nuisance variation and sharpens comparisons.

## Observational designs

- **Retrospective** (e.g., case-control): start from outcome and look back at exposures.
- **Prospective** (e.g., cohort): enroll by exposure status and follow forward for outcomes.
- **Sample survey**: measure a [population](statistical-inference.md) cross-section at a point in time (see [survey sampling](survey-sampling.md)).

## Sources of bias

- **Non-response bias** — those who decline differ systematically from responders.
- **Self-selection bias** — participants choose their own exposure/group.
- **Measurement error** — mismeasured exposure or outcome (recall, instrument).
- **Cohort effects** — birth-cohort differences masquerade as age or time effects.
- **Omitted-variable bias / confounding** — a common cause of exposure and outcome is ignored.
- **Temporality** — unclear whether exposure preceded outcome.
- **Spatial dependence** — nearby units share unmeasured influences, violating independence.
- **Spillover / interference** — one unit's treatment affects another's outcome (e.g., herd immunity).
- **Compliance** — assigned treatment differs from treatment received.

## Randomization in code

Randomly assign $n=10$ subjects to treatment vs. control.

### R

```r
set.seed(1)
subjects <- 1:10
assignment <- sample(rep(c("treat", "control"), each = 5))  # random labels
data.frame(subject = subjects, group = assignment)
```

### Python

```python
import numpy as np
rng = np.random.default_rng(1)
labels = np.array(["treat"] * 5 + ["control"] * 5)
rng.shuffle(labels)                     # random assignment
print(list(zip(range(1, 11), labels)))
```

### Julia

```julia
using Random
Random.seed!(1)
labels = vcat(fill("treat", 5), fill("control", 5))
shuffle!(labels)                        # random assignment
foreach(println, zip(1:10, labels))
```

## Why it matters for statistics

Design decides which biases the analysis can and cannot fix: no statistical adjustment recovers information a flawed design never captured.
Randomization and control are what make inferred effects causal, and naming the biases of observational studies guides both honest interpretation and better analysis.

## Related

- [Factorial designs](factorial-designs.md)
- [Fractional factorial designs](fractional-factorial-designs.md)
- [Optimal experimental design](optimal-design.md)
- [Response surface methodology](response-surface.md)
- [Survey sampling](survey-sampling.md)
- [Hypothesis testing](hypothesis-testing.md)
- [Statistical inference](statistical-inference.md)
- [Confidence intervals](confidence-intervals.md)
- [Quantitative Methods](../math.md)
