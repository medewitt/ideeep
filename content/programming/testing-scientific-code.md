---
title: "Testing & Verification for Scientific Code"
---

# Testing & Verification for Scientific Code

Analysis code has a dangerous property: it almost always produces *an* answer, and a wrong answer looks exactly like a right one.
A model still runs, a plot still renders, a number still prints — even when a sign is flipped or an index is off by one.
**Testing** is how you catch those silent errors before they reach a manuscript, by writing code that checks your code.

For scientific work the goal is not "100% coverage."
It is a small set of tests that would **fail loudly** if the results were wrong, so that when you refactor, add a feature, or update a package, you find out immediately instead of six months later.

## The Unit Test: Check a Known Answer

The basic building block is the **unit test**: call a function with an input whose correct output you already know, and assert you get it.
The best inputs are the ones you can work out by hand or from theory.

```python
# pytest: a function and the tests that pin down its behaviour
def prevalence(positives, n):
    return positives / n

def test_prevalence_basic():
    assert prevalence(20, 100) == 0.2

def test_prevalence_all_positive():
    assert prevalence(50, 50) == 1.0
```

The same idea in each language's standard framework:

```r
# R: testthat
test_that("prevalence is computed correctly", {
  expect_equal(prevalence(20, 100), 0.2)
  expect_equal(prevalence(50, 50), 1.0)
})
```

```julia
# Julia: the built-in Test standard library
using Test
@testset "prevalence" begin
    @test prevalence(20, 100) == 0.2
    @test prevalence(50, 50) == 1.0
end
```

Because [floating-point results are approximate](floating-point-and-numerical-stability.md), compare numbers with a **tolerance**, never `==`: `expect_equal` (R), `≈`/`isapprox` (Julia), and `pytest.approx` / `np.isclose` (Python) all exist for exactly this.

## Test the Edges, and the Bugs You Fix

The inputs that break code are rarely the typical ones.
Deliberately test the **edge cases**: an empty dataset, a single observation, a zero, a negative number, a missing value, the largest realistic input.

And every time you find a bug, **write a test that reproduces it first**, then fix it.
That "regression test" is a tripwire ensuring the bug can never silently return — a habit that pairs naturally with [debugging](debugging-and-troubleshooting.md) and the reprex.

## Property & Invariant Tests

Often you do not know the exact output, but you know something that must **always be true** — a property or invariant.
Asserting those catches a huge class of errors without a reference answer:

- A simulated **SIR/SEIR** trajectory must conserve the population: `S + I + R` stays constant.
- A vector of **probabilities** must be non-negative and sum to 1.
- A **distance matrix** must be symmetric with a zero diagonal.
- Sorting, then sorting again, changes nothing (**idempotence**).
- An estimator run on data simulated from known parameters should **recover those parameters** (on average).

An invariant test needs no oracle — just the law the code must obey:

```python
import numpy as np

def sir_step(S, I, R, beta, gamma, dt):
    dS, dI = -beta * S * I, beta * S * I - gamma * I
    return S + dS*dt, I + dI*dt, R + gamma*I*dt

S, I, R = 0.99, 0.01, 0.0
total_start = S + I + R
for _ in range(500):
    S, I, R = sir_step(S, I, R, 0.4, 0.1, 0.1)

print("population conserved:", np.isclose(S + I + R, total_start))
print("compartments non-negative:", min(S, I, R) >= 0)
```

<!-- python-output:auto -->
```text
population conserved: True
compartments non-negative: True
```
<!-- /python-output:auto -->

**Property-based testing** tools (`hypothesis` in Python, `quickcheck`/`hedgehog` in R, and Julia's macros) push this further: they generate hundreds of random inputs and check the property holds for all of them, automatically hunting for the one that breaks it.

## Testing Code That Is Random

Stochastic code — simulations, samplers, bootstraps — seems untestable: it gives a different number every run.
There are two complementary answers.

**Fix the seed for exact tests.** With the [seed pinned](randomness-and-rng.md), a stochastic function becomes deterministic, so you can assert on exact values or shapes — a *regression* test that catches any unintended change.

**Assert statistical properties for the randomness itself.** You cannot claim one run equals a fixed number, but you *can* simulate data from a known truth many times and check that the **distribution** of estimates is centred on that truth within a tolerance.
Any single run scatters; the average lands on the right answer.

![Testing stochastic code: the estimates from individual simulated runs scatter widely, but their mean lands within a small tolerance band of the known true value — so the test asserts a statistical property, not an exact value.](../assets/figures/testing-stochastic.svg)

```python
rng = np.random.default_rng(1)
true_rate = 2.0
ests = np.array([
    1.0 / rng.exponential(1 / true_rate, size=200).mean()   # estimate the rate
    for _ in range(2000)
])

print(f"mean estimate: {ests.mean():.3f}   (true value {true_rate})")
print("recovers truth within 2%:", abs(ests.mean() - true_rate) < 0.02 * true_rate)
```

<!-- python-output:auto -->
```text
mean estimate: 2.017   (true value 2.0)
recovers truth within 2%: True
```
<!-- /python-output:auto -->

This is the everyday logic of a **simulation study** turned into a pass/fail check — see [A Simulation Toolkit](simulation-toolkit.md).

## What to Test, in Practice

You do not need to test everything.
For a typical analysis, aim these tests at the parts most likely to be silently wrong:

- **Your own core functions** — the custom likelihood, the transmission step, the summary statistic.
  Not the libraries; they are already tested.
- **Data-cleaning steps** — filters, joins, and recodes, where an off-by-one or a bad join quietly drops or duplicates rows.
- **Anything numerically delicate** — [log-space](floating-point-and-numerical-stability.md) calculations, [ODE integration](numerical-methods-for-dynamical-systems.md), optimization.
- **Every bug you fix** — as a regression test.

Wire the tests into your [project workflow](project-workflow.md) so they run with one command, and — ideally — automatically on each commit, so a broken result can never quietly ship.

## Related

- [Debugging and Troubleshooting](debugging-and-troubleshooting.md) — finding the bug a test just caught
- [A Simulation Toolkit](simulation-toolkit.md) — simulate-from-known-truth is also how you test estimators
- [Randomness & Random Number Generation](randomness-and-rng.md) — seeds make stochastic tests reproducible
- [Floating-Point Arithmetic & Numerical Stability](floating-point-and-numerical-stability.md) — why tests compare with a tolerance
- [Reproducibility](reproducibility.md) and [Project Workflow](project-workflow.md) — running tests as part of the pipeline
- [Programming & Computing](../programming.md)
