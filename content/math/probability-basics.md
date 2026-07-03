---
title: "Probability Basics"
---

# Probability Basics

Probability is the language of uncertainty, and every statistical method is built on it.
Getting the basic rules right — especially conditioning and independence — is what keeps a diagnostic-test calculation or a risk estimate from going badly wrong.

## Sample space and events

An **experiment** has a set of possible outcomes called the **sample space** $\Omega$.
An **event** is any subset $A \subseteq \Omega$.
For a single die roll, $\Omega = \{1,2,3,4,5,6\}$ and "roll even" is the event $A = \{2,4,6\}$.

A **probability** $\Pr(A)$ assigns each event a number measuring how likely it is.

## The axioms

Probability obeys three rules (Kolmogorov's axioms):

1. **Non-negativity**: $\Pr(A) \ge 0$ for every event $A$.
2. **Normalization**: $\Pr(\Omega) = 1$.
3. **Additivity**: if $A$ and $B$ are disjoint ($A \cap B = \varnothing$), then $\Pr(A \cup B) = \Pr(A) + \Pr(B)$.

Everything else follows.
The **complement** rule is immediate:

\[
\Pr(A^c) = 1 - \Pr(A).
\]

## The union (inclusion–exclusion) rule

When events can overlap, simply adding probabilities double-counts the overlap:

\[
\Pr(A \cup B) = \Pr(A) + \Pr(B) - \Pr(A \cap B).
\]

## Conditional probability

The probability of $A$ *given that* $B$ occurred rescales to the world where $B$ is true:

\[
\Pr(A \mid B) = \frac{\Pr(A \cap B)}{\Pr(B)}, \qquad \Pr(B) > 0.
\]

Rearranging gives the **multiplication rule** $\Pr(A \cap B) = \Pr(A \mid B)\,\Pr(B)$.

## Independence

Two events are **independent** if knowing one tells you nothing about the other.
Equivalently,

\[
\Pr(A \cap B) = \Pr(A)\,\Pr(B),
\]

which we write $A \perp B$.
Under independence $\Pr(A \mid B) = \Pr(A)$.

## Bayes' theorem

Flipping the direction of conditioning:

\[
\Pr(A \mid B) = \frac{\Pr(B \mid A)\,\Pr(A)}{\Pr(B)}.
\]

## Worked example: a diagnostic test

A disease has prevalence $\Pr(D) = 0.01$.
A test has sensitivity $\Pr(+ \mid D) = 0.99$ and specificity $\Pr(- \mid D^c) = 0.95$ (so the false-positive rate is $\Pr(+ \mid D^c) = 0.05$).
If someone tests positive, what is $\Pr(D \mid +)$?

First get $\Pr(+)$ by the law of total probability:

\[
\Pr(+) = \Pr(+\mid D)\Pr(D) + \Pr(+\mid D^c)\Pr(D^c) = (0.99)(0.01) + (0.05)(0.99) = 0.0594.
\]

Then apply Bayes:

\[
\Pr(D \mid +) = \frac{(0.99)(0.01)}{0.0594} \approx 0.167.
\]

Even with a "99% accurate" test, a positive result means only a **16.7%** chance of disease — because the disease is rare.
This base-rate effect is central to screening in epidemiology.

## Simulation

We estimate a probability by Monte Carlo: [simulate](../programming/simulation-toolkit.md) the process many times and take the long-run fraction.
Here we estimate $\Pr(\text{sum} = 7)$ for two fair dice (true value $6/36 \approx 0.1667$).

### R

```r
set.seed(42)
N <- 1e6
d1 <- sample(1:6, N, replace = TRUE)
d2 <- sample(1:6, N, replace = TRUE)
mean(d1 + d2 == 7)   # ~0.1667
```

### Python

```python
import numpy as np
rng = np.random.default_rng(42)
N = 1_000_000
d1 = rng.integers(1, 7, N)
d2 = rng.integers(1, 7, N)
print(np.mean(d1 + d2 == 7))   # ~0.1667
```

<!-- python-output:auto -->
```text
0.166807
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Statistics
Random.seed!(42)
N = 1_000_000
d1 = rand(1:6, N)
d2 = rand(1:6, N)
mean(d1 .+ d2 .== 7)   # ~0.1667
```

## Why it matters for statistics

Probability is the machinery under every inference.
Conditional probability and Bayes' theorem drive diagnostic reasoning and Bayesian estimation; independence justifies multiplying [likelihoods](maximum-likelihood.md) across observations; the union and complement rules underlie every calculation of error rates and [p-values](p-values.md).
Monte Carlo simulation turns a hard analytic probability into a simple counting exercise.

## Related

- [Random Variables](random-variables.md)
- [Expected Value](expected-value.md)
- [Distributions Overview](distributions-overview.md)
- [Statistical Inference](statistical-inference.md)
- [Quantitative Methods](../math.md)
