---
title: "Cost-Effectiveness Analysis"
description: "Deciding whether an infectious-disease intervention is worth its cost using incremental cost-effectiveness ratios, willingness-to-pay thresholds, and net monetary benefit."
---

# Cost-Effectiveness Analysis

Cost-effectiveness analysis (CEA) asks not just whether an intervention works but whether its health gains justify the resources it consumes.
It compares each option's extra cost against its extra health benefit, so that a fixed budget buys as much health as possible.
Economic evaluation is a standard curricular component that quantitative modeling programs often omit, leaving analysts fluent in transmission dynamics but unable to translate a model into a funding decision.

![A cost-effectiveness plane showing two intervention strategies against a willingness-to-pay threshold line through the origin.](../assets/figures/cost-effectiveness-analysis.svg)

## Costs and health effects

Every option is summarized by two numbers: its total cost $C$ and its total health effect $E$, with costs including downstream care averted or induced and effects measured on a common scale so different diseases compare.
The standard reference for these methods is Drummond et al., *Methods for the Economic Evaluation of Health Care Programmes*.

## Health-outcome metrics

Two metrics dominate.
Death is the most natural thing to count, but mortality alone captures only a fraction of a disease's burden on a population.
Much of the damage is non-fatal: acute and chronic symptoms, temporary or permanent disability, long-term sequelae such as post-infectious or "long" syndromes that persist well beyond the initial illness and any hospitalization, the reduced quality of life these impose, and the productivity and caregiving costs they push onto families and communities.
QALYs and DALYs exist precisely to capture this fuller picture, because each combines length of life with the quality of the health states lived through it, so that non-fatal morbidity is counted alongside deaths averted rather than ignored.
A **quality-adjusted life year** (QALY) is one year of life weighted by a utility between $0$ (death) and $1$ (full health), so an intervention that adds effects is credited with the *QALYs gained* relative to a comparator.
A **disability-adjusted life year** (DALY) is a year of healthy life *lost* to illness or premature death, so an intervention is instead credited with the *DALYs averted* — the mirror image of QALYs gained, both signs of more healthy time.

## The incremental cost-effectiveness ratio

Comparing two options $A$ and $B$, the extra cost per extra unit of health is the **incremental cost-effectiveness ratio**

\[
\text{ICER} = \frac{C_B - C_A}{E_B - E_A} = \frac{\Delta C}{\Delta E}.
\]

The ICER is a price: how many dollars each additional QALY costs when you switch from $A$ to $B$, and it only makes sense against a stated comparator.

## The cost-effectiveness plane and dominance

Plot each option by its incremental cost (vertical) and incremental effect (horizontal) relative to a baseline.
An option in the lower-right quadrant costs less *and* does more, so it **dominates** and is always preferred; one in the upper-left is dominated and discarded.
The interesting trade-offs live in the upper-right quadrant, where more health costs more money, and the ICER is the slope from the origin to the point.

## Willingness-to-pay and the decision rule

A decision maker sets a **willingness-to-pay** threshold $\lambda$, the most they will spend per QALY gained.
The rule is simple: adopt the switch from $A$ to $B$ when $\text{ICER} = \Delta C / \Delta E \le \lambda$.
The threshold encodes the opportunity cost of the budget, since a dollar spent here is a dollar not spent on the next-best use.

## Incremental analysis across many options

With more than two options, rank them by cost and compute each ICER against the next-less-costly option that has not been ruled out.
An option is subject to **extended dominance** when it has a higher ICER than a more-effective option further down the list; such an option is never optimal at any threshold and is removed before recomputing.
Only after discarding dominated and extended-dominated options do the ICERs increase monotonically, and you climb that sequence until the next ICER exceeds $\lambda$.

## Net monetary benefit

An algebraically equivalent framing converts health into money.
The **net monetary benefit** of an option is

\[
\text{NMB} = \lambda \, E - C ,
\]

and the option with the largest NMB at a given $\lambda$ is preferred, which avoids the awkward behavior of ratios (undefined or sign-flipping when $\Delta E$ is near zero) and makes the choice a plain maximization.

## Why infectious-disease CEA needs dynamic models

For infectious diseases the effect of an intervention is not confined to those who receive it.
Vaccinating some people lowers everyone's exposure through herd immunity, so the value of a program depends on its coverage — a nonlinear externality that a static per-person calculation misses entirely.
This is why infectious-disease CEA is built on dynamic [transmission models](sir.md) rather than static decision trees, a point argued for public-health economic evaluation by [Breeze et al., 2023, Health Economics](https://doi.org/10.1002/hec.4681).

## Discounting future costs and effects

Costs and health accrue over years, and both are discounted so that a QALY tomorrow counts less than one today.
With annual rate $r$, a stream $x_t$ has present value

\[
\text{PV} = \sum_{t=0}^{T} \frac{x_t}{(1+r)^t},
\]

typically applied at $r \approx 0.03$ to both costs and effects, which keeps the two on the same time footing and prevents indefinitely deferred benefits from dominating.

## Handling uncertainty

Every input — costs, utilities, transmission parameters — is itself uncertain.
**Probabilistic sensitivity analysis** assigns each input a distribution, samples them jointly many times, and re-runs the model to produce a cloud of ICERs, summarized as the probability that each option is cost-effective across a range of $\lambda$.
The case for embedding such evaluation in the training of modelers and policymakers is made by [Ofori et al., 2024, Annals of Global Health](https://doi.org/10.5334/aogh.4383), and the link between formal decision modeling and cost-effective delivery by [Zouo et al., 2024, Finance & Accounting Research Journal](https://doi.org/10.51594/farj.v6i11.1699).

## A worked example

Compare two vaccination strategies against no intervention.
Strategy A costs \$500{,}000 and gains $40$ QALYs; strategy B costs \$1{,}200{,}000 and gains $70$ QALYs; the baseline (no intervention) costs \$0 and gains $0$. The willingness-to-pay threshold is $\lambda = \$50{,}000$ per QALY.

Ranked by cost, A's ICER against baseline is $500{,}000/40 = \$12{,}500$ per QALY. B's ICER against A is $(1{,}200{,}000 - 500{,}000)/(70 - 40) = 700{,}000/30 \approx \$23{,}333$ per QALY.
Both ICERs are below $\lambda$ and increase in sequence, so B is not dominated and we climb to it; the net monetary benefit confirms B ($50{,}000 \times 70 - 1{,}200{,}000 = \$2{,}300{,}000$) beats A ($\$1{,}500{,}000$) and baseline ($\$0$).

## In code

### R

```r
# Incremental cost-effectiveness across three options
opts  <- data.frame(name = c("None", "A", "B"),
                    cost = c(0, 500000, 1200000),
                    qaly = c(0, 40, 70))
lambda <- 50000
opts   <- opts[order(opts$cost), ]
opts$icer <- c(NA, diff(opts$cost) / diff(opts$qaly))
opts$nmb  <- lambda * opts$qaly - opts$cost
print(opts)
opts$name[which.max(opts$nmb)]   # preferred strategy: "B"
```

### Python

```python
import numpy as np

names = np.array(["None", "A", "B"])
cost = np.array([0.0, 500_000.0, 1_200_000.0])
qaly = np.array([0.0, 40.0, 70.0])
lam = 50_000.0  # willingness-to-pay per QALY

order = np.argsort(cost)
names, cost, qaly = names[order], cost[order], qaly[order]

# ICER of each option vs the next-less-costly one
dcost = np.diff(cost)
dqaly = np.diff(qaly)
icer = np.concatenate(([np.nan], dcost / dqaly))

nmb = lam * qaly - cost             # net monetary benefit at lambda
best = names[np.argmax(nmb)]

print("strategy   icer        nmb")
for n, i, m in zip(names, icer, nmb):
    itxt = "     -   " if np.isnan(i) else f"{i:8.0f} "
    print(f"{n:8s} {itxt} {m:10.0f}")
print("preferred strategy:", best)
```

<!-- python-output:auto -->
```text
strategy   icer        nmb
None          -             0
A           12500     1500000
B           23333     2300000
preferred strategy: B
```
<!-- /python-output:auto -->

### Julia

```julia
names = ["None", "A", "B"]
cost  = [0.0, 500_000.0, 1_200_000.0]
qaly  = [0.0, 40.0, 70.0]
lambda = 50_000.0

icer = [NaN; diff(cost) ./ diff(qaly)]   # vs next-less-costly option
nmb  = lambda .* qaly .- cost            # net monetary benefit
best = names[argmax(nmb)]
println("ICERs: ", icer)
println("preferred strategy: ", best)    # "B"
```

## Why it matters

CEA is where a transmission model stops being an academic exercise and becomes a funding decision.
It forces the modeler to state the comparator, price a QALY, and defend a threshold, turning "the vaccine works" into "the vaccine buys health at \$23{,}000 per QALY, below what we will pay."
Because herd immunity makes value depend on coverage, this pricing can only be done honestly atop a dynamic model, which is exactly why economic evaluation belongs in a quantitative curriculum rather than beside it.

## Related

- [Sensitivity analysis](sensitivity-analysis.md)
- [Fitting dynamic models to data](model-calibration.md)
- [The SIR model](sir.md)
- [Markov chains](markov-chains.md)
- [Quantitative Methods](../math.md)
