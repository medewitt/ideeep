---
title: "Floating-Point Arithmetic & Numerical Stability"
---

# Floating-Point Arithmetic & Numerical Stability

A computer does not store real numbers.
It stores **floating-point** approximations — numbers with a fixed budget of binary digits — and every calculation nudges the result by a tiny rounding error.
Most of the time you never notice.
But in the calculations mathematical biologists do all day — multiplying probabilities, summing likelihoods, integrating differential equations — those tiny errors can compound until a "correct" model returns a wrong number, an infinity, or nothing at all.

This page is about recognizing those failure modes and the handful of tricks that avoid them.
The most important one — **working in log space**, and its refinement the **log-sum-exp trick** — is worth its weight in gold for anyone who computes a likelihood.

![Multiplying many probabilities underflows to exactly zero once the product drops below about 1e-308, and log(0) = -infinity breaks everything downstream; adding the log-probabilities instead keeps the value finite.](../assets/figures/floating-point-underflow.svg)

## How Computers Store Numbers

A standard **double-precision** float (`float64`, the default in R, Python, and Julia) carries about **15–17 significant decimal digits** and can represent magnitudes from roughly `1e-308` to `1e308`.
Two consequences follow immediately:

- **Precision is finite.** Numbers that need more than ~16 digits get rounded.
  `0.1` has no exact binary representation, just as `1/3` has no exact decimal one.
- **Range is finite.** A value smaller than ~`1e-308` **underflows** to exactly `0`; a value larger than ~`1e308` **overflows** to `Inf`.

The classic demonstration:

```python
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
```

<!-- python-output:auto -->
```text
0.30000000000000004
False
```
<!-- /python-output:auto -->

The sum is off in the 17th digit, and the equality test fails.

**Do not test floating-point numbers for exact equality.** Compare within a tolerance instead.

```r
# R: never `if (x == y)` for computed doubles
isTRUE(all.equal(0.1 + 0.2, 0.3))          # TRUE, uses a tolerance
abs((0.1 + 0.2) - 0.3) < 1e-9              # TRUE, explicit tolerance
```

```julia
# Julia: isapprox (the ≈ operator)
(0.1 + 0.2) ≈ 0.3                          # true
```

## Catastrophic Cancellation

Rounding error is usually harmless because it is *relative* — about 16 digits of accuracy no matter the scale.
It becomes dangerous when you **subtract two nearly equal numbers**: the leading digits cancel, and what remains is mostly rounding noise.
This is **catastrophic cancellation**, and the textbook victim is the one-pass ("computational") formula for a variance, $\sum x_i^2 - (\sum x_i)^2/n$, which subtracts two large, nearly equal sums.

```python
import numpy as np
x = np.array([1e8 + 1.0, 1e8 + 2.0, 1e8 + 3.0])

# one-pass formula: subtracts two huge, nearly-equal numbers
one_pass = (np.sum(x**2) - np.sum(x)**2 / len(x)) / (len(x) - 1)
# two-pass formula: subtract the mean first, then square
two_pass = np.sum((x - x.mean())**2) / (len(x) - 1)

print("one-pass:", one_pass)     # wrong: collapses to 0 (true value is 1.0)
print("two-pass:", two_pass)     # correct: 1.0
```

<!-- python-output:auto -->
```text
one-pass: 0.0
two-pass: 1.0
```
<!-- /python-output:auto -->

The two-pass version subtracts the mean *first*, while the numbers are still close together, so no catastrophic cancellation occurs.
The lesson generalizes: **rearrange a calculation so you never subtract two big numbers that are almost equal.** This is exactly why you should use a library's `var()`, `sd()`, or `numpy.var` rather than coding the "shortcut" formula yourself.

## Work in Log Space

Here is the failure that stops MCMC chains and phylogenetics runs cold.
A likelihood is a **product of probabilities** — one factor per site, read, observation, or individual:

$$ L = \prod_{i=1}^{n} p_i .
$$

Each $p_i$ is below 1, so the product shrinks geometrically.
After only a few hundred factors it slips below `1e-308` and **underflows to exactly `0`** — and then `log(0) = -Inf` poisons every downstream calculation (see the figure above).

The fix is to never form the product at all.
Take the logarithm of both sides and the product becomes a **sum**:

$$ \log L = \sum_{i=1}^{n} \log p_i .
$$

A sum of $n$ moderate negative numbers is perfectly well-behaved no matter how large $n$ gets.

```python
p = np.full(1000, 1e-3)                    # 1000 probabilities, each 0.001
print("product of probabilities:", np.prod(p))       # underflows to 0.0
print("sum of log-probabilities:", np.sum(np.log(p)))  # finite, usable
```

<!-- python-output:auto -->
```text
product of probabilities: 0.0
sum of log-probabilities: -6907.755278982137
```
<!-- /python-output:auto -->

**Rule of thumb: compute and store log-probabilities, not probabilities.** Multiply probabilities → *add* log-probabilities.
Divide → *subtract*.
This single habit is why every serious likelihood, Bayesian, and phylogenetic library works in log space internally.

## The Log-Sum-Exp Trick

Working in logs is easy until you have to **add probabilities that are stored as logs** — and in biology you have to do this constantly, because *summing over unobserved possibilities* is addition in probability space.
You have $\log a$ and $\log b$; you want $\log(a + b)$.
The naive route — exponentiate, add, take the log — throws away everything you gained, because $\exp(\log a)$ underflows right back to `0`.

The **log-sum-exp** trick keeps you safe.
To compute $\log \sum_i \exp(x_i)$, factor out the largest term $m = \max_i x_i$:

$$ \log \sum_i e^{x_i} = m + \log \sum_i e^{x_i - m} .
$$

Now the biggest exponent is $e^0 = 1$ and everything else is between 0 and 1 — all comfortably representable.
You get the exact same answer with no underflow.

![The log-sum-exp trick: exponentiating raw log-probabilities underflows every term to zero, so the naive sum is zero and its log is minus infinity; subtracting the maximum first slides the values into the representable range, the sum is well behaved, and adding the maximum back recovers the exact answer.](../assets/figures/log-sum-exp.svg)

```python
def logsumexp(a):
    m = np.max(a)
    return m + np.log(np.sum(np.exp(a - m)))

logw = np.array([-1000.0, -1001.5, -1003.0])   # three log-probabilities
naive = np.log(np.sum(np.exp(logw)))           # exp underflows -> log(0)
print("naive:    ", naive)                     # -inf : wrong
print("logsumexp:", logsumexp(logw))           # correct, finite
```

<!-- python-output:auto -->
```text
naive:     -inf
logsumexp: -999.7586887033428
```
<!-- /python-output:auto -->

You rarely need to write it yourself — every ecosystem ships a tested, vectorized version:

```r
# R
matrixStats::logSumExp(c(-1000, -1001.5, -1003))
```

```julia
# Julia
using LogExpFunctions
logsumexp([-1000.0, -1001.5, -1003.0])
```

```python
# Python
from scipy.special import logsumexp
logsumexp([-1000.0, -1001.5, -1003.0])
```

### Where This Shows Up in Biology

Once you recognize "log of a sum of exponentials," you see it everywhere a model **marginalizes over hidden possibilities**:

- **Phylogenetics — Felsenstein's pruning algorithm.** The likelihood of a tree sums over all unobserved ancestral states at every internal node.
  Every credible phylogenetics engine (RAxML, BEAST, MrBayes) does this sum in log space with log-sum-exp.
- **Hidden Markov Models — the forward algorithm.** Gene finding, CpG-island detection, ion-channel gating, and animal-behavior state models all sum probability over exponentially many hidden state paths; the forward recursion is log-sum-exp at each step.
- **Bayesian inference.** The log-posterior is `log-likelihood + log-prior`; the marginal likelihood (model evidence) and importance-sampling weights are normalized with log-sum-exp.
- **Mixture models and model averaging.** The density $\sum_k \pi_k f_k(x)$ — population-structure models, Gaussian mixtures for flow-cytometry gating — is a log-sum-exp over components.
- **Softmax / multinomial models.** Multinomial logistic regression and multi-class species-distribution models normalize scores with the softmax, whose denominator is a log-sum-exp.
- **Taxonomic read classification.** Naive-Bayes assignment of sequencing reads sums log-probabilities across features and normalizes with log-sum-exp.

## A Short Checklist

- **Store log-probabilities.** Add them instead of multiplying probabilities.
- **Sum in log space with log-sum-exp**, subtracting the max first — or just call your library's `logSumExp`.
- **Never compare computed floats with `==`;** use a tolerance (`all.equal`, `isapprox`, `np.isclose`).
- **Don't subtract two nearly-equal large numbers;** rearrange the formula, and prefer built-in `var`/`sd`.
- **Watch for `Inf`, `-Inf`, and `NaN`** appearing mid-computation — they are usually the fingerprint of an overflow, an underflow, or a `0/0`, not a modeling mistake.
- **Reach for stable library functions** (`log1p`, `expm1`, `logsumexp`, `softmax`) instead of composing `log`, `exp`, and subtraction by hand.

## Related

- [Big-O Notation & Computational Complexity](big-o-and-complexity.md) — the other half of "will this compute correctly and fast enough?"
- [A Simulation Toolkit](simulation-toolkit.md) — where likelihoods and log-probabilities get evaluated millions of times
- [Reproducibility](reproducibility.md) — recording tolerances and seeds so results are stable
- [MCMC](../math/mcmc.md) and [Markov Chains](../math/markov-chains.md) — samplers that live or die by log-space arithmetic
- [Computer Basics for Scientists](computer-basics.md) — how data is represented in the machine
- [Programming & Computing](../programming.md)
