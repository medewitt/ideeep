---
title: "Diagnostic Testing and Screening"
---

# Diagnostic Testing and Screening

A diagnostic test never returns the truth—it returns a noisy signal that we must interpret in light of how common the disease is.
The same test that looks excellent in the lab can be nearly useless for screening a healthy population, and understanding why is one of the most practically important applications of [Bayes' theorem](bayesian-inference.md).

![ROC curve (left) and how positive predictive value collapses at low prevalence (right).](../assets/figures/diagnostic-testing.svg)

## Sensitivity and specificity

Two conditional [probabilities](probability-basics.md) describe how a test behaves on people whose true status we already know.
**Sensitivity** is the true-positive rate, $\text{sens} = P(\text{test}+ \mid \text{disease})$: the chance a truly diseased person tests positive.
**Specificity** is the true-negative rate, $\text{spec} = P(\text{test}- \mid \text{no disease})$: the chance a truly healthy person tests negative.
These are properties of the test itself and, unlike the quantities below, do not depend on how common the disease is.

## Prevalence and the question that matters

**Prevalence** is the [probability](random-variables.md) $P(\text{disease})$ that a randomly chosen person from the tested population actually has the disease.
A clinician holding a positive result does not want sensitivity; they want the reverse conditional, $P(\text{disease} \mid \text{test}+)$.
Getting from one to the other requires prevalence, and this is where intuition often fails.

## Bayes' theorem: predictive values

The **positive predictive value** is the probability that a person who tests positive truly has the disease.
Bayes' theorem gives

\[
\text{PPV} = P(\text{disease} \mid \text{test}+) = \frac{\text{sens}\cdot\text{prev}}{\text{sens}\cdot\text{prev} + (1-\text{spec})\cdot(1-\text{prev})}.
\]

The denominator is just the total probability of a positive test: true positives plus false positives.
The **negative predictive value** is the mirror image, the chance a negative test is correct:

\[
\text{NPV} = P(\text{no disease} \mid \text{test}-) = \frac{\text{spec}\cdot(1-\text{prev})}{\text{spec}\cdot(1-\text{prev}) + (1-\text{sens})\cdot\text{prev}}.
\]

Unlike sensitivity and specificity, both predictive values depend on prevalence.

## The base-rate effect

Consider a genuinely good test with $\text{sens}=0.95$ and $\text{spec}=0.95$, used to screen a population where the disease has prevalence $0.01$.
Out of $10{,}000$ people, about $100$ are diseased and $95$ of them test positive.
But among the $9{,}900$ healthy people, $5\%$—about $495$—also test positive.
So of $95 + 495 = 590$ positive tests, only $95$ are real, giving $\text{PPV} \approx 95/590 \approx 0.16$.
A positive result still means the disease is unlikely, purely because the disease was rare to begin with.
This base-rate effect is why screening for rare conditions demands very high specificity, and why positive screening results are confirmed with a second, independent test.

## Likelihood ratios

Likelihood ratios repackage the same information in a way that combines cleanly with prior odds.
The **positive likelihood ratio** is

\[
\text{LR}+ = \frac{P(\text{test}+ \mid \text{disease})}{P(\text{test}+ \mid \text{no disease})} = \frac{\text{sens}}{1-\text{spec}},
\]

and the negative likelihood ratio is $\text{LR}- = (1-\text{sens})/\text{spec}$.
The appeal is that posterior odds equal prior odds times the likelihood ratio: $\text{odds}(\text{disease}\mid\text{test}+) = \text{LR}+ \times \text{odds}(\text{disease})$.
For our example $\text{LR}+ = 0.95/0.05 = 19$, so a positive test multiplies the prior odds of disease by $19$.

## ROC curves and AUC

Most tests report a continuous score, and we choose a threshold above which we call the result positive.
Lowering the threshold catches more true cases (higher sensitivity) but also flags more healthy people (lower specificity), so there is always a trade-off.
The **receiver operating characteristic (ROC) curve** plots the true-positive rate against the false-positive rate as the threshold sweeps across every possible value.
The **area under the curve (AUC)** summarizes the whole curve in one number: it equals the probability that a randomly chosen diseased person scores higher than a randomly chosen healthy one.
An AUC of $0.5$ is the diagonal chance line and $1.0$ is a perfect test; the figure's test, with diseased scores $\sim\text{Normal}(1,1)$ and healthy $\sim\text{Normal}(0,1)$, gives $\text{AUC}\approx 0.76$.

## In code

### R

```r
ppv <- function(sens, spec, prev)
  (sens * prev) / (sens * prev + (1 - spec) * (1 - prev))
npv <- function(sens, spec, prev)
  (spec * (1 - prev)) / (spec * (1 - prev) + (1 - sens) * prev)

ppv(0.95, 0.95, 0.01)   # ~0.161
npv(0.95, 0.95, 0.01)   # ~0.999
```

### Python

```python
def ppv(sens, spec, prev):
    return (sens * prev) / (sens * prev + (1 - spec) * (1 - prev))

def npv(sens, spec, prev):
    return (spec * (1 - prev)) / (spec * (1 - prev) + (1 - sens) * prev)

sens, spec = 0.95, 0.95
for prev in (0.01, 0.10):
    print(prev, round(ppv(sens, spec, prev), 3), round(npv(sens, spec, prev), 4))
# 0.01 0.161 0.9995
# 0.1 0.679 0.9942

print("LR+ =", sens / (1 - spec))   # LR+ = 19.0
```

<!-- python-output:auto -->
```text
0.01 0.161 0.9995
0.1 0.679 0.9942
LR+ = 18.999999999999982
```
<!-- /python-output:auto -->

### Julia

```julia
ppv(sens, spec, prev) = (sens*prev) / (sens*prev + (1-spec)*(1-prev))
npv(sens, spec, prev) = (spec*(1-prev)) / (spec*(1-prev) + (1-sens)*prev)

println(ppv(0.95, 0.95, 0.01))   # ~0.161
println(npv(0.95, 0.95, 0.01))   # ~0.999
```

## Why it matters

Predictive values, not sensitivity and specificity, are what a patient and clinician actually experience, and they hinge on prevalence in a way that surprises even trained professionals.
The base-rate effect explains why mass screening for rare diseases produces mostly false alarms, why confirmatory testing is essential, and why the same test can be superb in a clinic yet misleading in the general public.

## Related

- [Bayesian inference](bayesian-inference.md)
- [Probability basics](probability-basics.md)
- [Hypothesis testing](hypothesis-testing.md)
- [Confidence intervals](confidence-intervals.md)
- [Normal distribution](normal-distribution.md)
- [Proper Scoring Rules](proper-scoring-rules.md)
- [Quantitative Methods](../math.md)
