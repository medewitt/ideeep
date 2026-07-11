---
title: "Bayesian Bandits for Adaptive Sampling and Trial Design"
description: "Thompson sampling over four surveillance sites: keep a Beta posterior on each site's positivity, sample in proportion to the probability a site is best, and shift the testing budget toward where the signal is — the same machinery behind response-adaptive clinical trials."
---

# Bayesian Bandits for Adaptive Sampling and Trial Design

Suppose you can afford to run 1,000 tests across four surveillance sites, and you care about *finding cases* — not about estimating every site equally well.
A fixed design splits the budget evenly and never learns; a purely greedy design pours everything into whichever site looked best after the first few tests and can be fooled by noise.
A **Bayesian bandit** threads the needle: it keeps a posterior on each site's positivity, and each round it allocates the next test in proportion to the probability that a site is the best one — automatically shifting resources toward the hot site while still occasionally probing the others in case it was wrong.

![Left: after 40 rounds of adaptive allocation the posterior on the high-positivity site (C) is sharp and correctly located, while the neglected sites stay diffuse. Right: the cumulative share of the testing budget migrates toward site C as evidence accumulates, without ever fully abandoning the alternatives.](../assets/figures/bayesian-bandits.svg "fig:bandits")

This is the **multi-armed bandit** problem: each "arm" (site, treatment, ad, dose) pays off with an unknown probability, and every pull is both a chance to earn a reward *and* a chance to learn.
The tension between those two goals is the **exploration–exploitation trade-off**, and the elegant Bayesian answer to it is **Thompson sampling**.

## The setup: arms, rewards, and beliefs

We have $K$ arms (here $K=4$ sites).
Pulling arm $k$ yields a Bernoulli reward — a positive test — with unknown probability $\theta_k$.
Our goal over a horizon of $T$ pulls is to maximize the expected number of positives found, $\sum_{t} \theta_{a_t}$, where $a_t \in \{1,\dots,K\}$ is the arm chosen at step $t$.

Because each arm is a proportion, the natural belief to carry is a [Beta distribution](binomial-distribution.md), which is [conjugate](bayesian-inference.md) to the [Binomial](binomial-distribution.md) likelihood.
Start each site with a prior $\text{Beta}(\alpha_k, \beta_k)$ — a uniform $\text{Beta}(1,1)$ if you know nothing.
After observing $s_k$ positives in $n_k$ tests at that site, the posterior is simply

\[
\theta_k \mid \text{data} \;\sim\; \text{Beta}\!\left(\alpha_k + s_k,\; \beta_k + n_k - s_k\right).
\label{eq:beta-update}
\]

The two hyperparameters have a clean reading: $\alpha_k - 1$ is (prior plus observed) positives, $\beta_k - 1$ is negatives, and the posterior mean is $\hat\theta_k = \alpha_k / (\alpha_k + \beta_k)$.
The **total count** $\alpha_k + \beta_k$ is the effective sample size — how sharp the belief is.

:::spoiler Show the Beta–Binomial conjugacy derivation

Put a $\text{Beta}(\alpha,\beta)$ prior on a positivity $\theta$ and observe $s$ positives in $n$ independent tests, a $\text{Binomial}(n,\theta)$ likelihood.
Bayes' rule says the posterior is proportional to likelihood times prior:

\[
p(\theta \mid s) \;\propto\; \underbrace{\binom{n}{s}\theta^{s}(1-\theta)^{n-s}}_{\text{likelihood}} \; \underbrace{\frac{\theta^{\alpha-1}(1-\theta)^{\beta-1}}{B(\alpha,\beta)}}_{\text{prior}} .
\]

Everything that does not depend on $\theta$ — the binomial coefficient and the Beta normalizer $B(\alpha,\beta)$ — folds into the proportionality constant, leaving

\[
p(\theta \mid s) \;\propto\; \theta^{(\alpha + s) - 1}\,(1-\theta)^{(\beta + n - s) - 1} .
\]

That is the *kernel* of a Beta density with updated parameters $\alpha' = \alpha + s$ and $\beta' = \beta + n - s$.
Since a probability density must integrate to one, the missing constant is forced to be $1/B(\alpha', \beta')$, so

\[
\theta \mid s \;\sim\; \text{Beta}(\alpha + s,\; \beta + n - s),
\]

which is [@eq:beta-update].
The prior and posterior live in the same family — that is what **conjugacy** means — so updating never requires an integral: you just add your positives to $\alpha$ and your negatives to $\beta$.
Crucially, the update is the same whether you feed it one test at a time or a whole batch, because independent Bernoulli increments to $\alpha$ and $\beta$ commute and add.

:::

## Thompson sampling: probability matching

Given those posteriors, how should we choose the next site?
**Thompson sampling** (posterior sampling) is almost embarrassingly simple:

1. Draw one sample $\tilde\theta_k \sim \text{Beta}(\alpha_k,\beta_k)$ from *each* arm's current posterior.
2. Pull the arm with the largest sample, $a = \arg\max_k \tilde\theta_k$.
3. Observe the reward, update that arm's posterior via [@eq:beta-update], and repeat.

The magic is that the probability an arm gets pulled equals the posterior probability that it is genuinely the best arm.
Early on, when posteriors are wide, the draws are noisy and every arm gets tried — that is **exploration**, and it is *automatic*, requiring no tuning parameter.
As evidence sharpens the posteriors, the best arm wins the draw more and more often — that is **exploitation**, and it emerges from the same one line of code.
This property is called **probability matching**.

:::spoiler Show the allocation probability and why it self-tunes

Let $w_k$ be the probability that Thompson sampling pulls arm $k$ on the next step.
By construction arm $k$ is pulled exactly when its draw exceeds every other arm's draw, so

\[
w_k \;=\; \Pr\!\Big(\tilde\theta_k > \tilde\theta_j \ \text{for all } j \neq k \;\Big|\; \text{data}\Big),
\]

with each $\tilde\theta_j$ drawn independently from its posterior.
Conditioning on the value of arm $k$'s draw and using independence, this integral is

\[
w_k \;=\; \int_0^1 p_k(\theta)\,\prod_{j \neq k} F_j(\theta)\; d\theta ,
\label{eq:alloc}
\]

where $p_k$ is arm $k$'s posterior *density* and $F_j$ is arm $j$'s posterior *CDF*.
Read [@eq:alloc] as: "the chance arm $k$'s value lands at $\theta$, times the chance all other arms fall below $\theta$, integrated over $\theta$."
This is exactly the **posterior probability that arm $k$ is optimal**, $\Pr(\theta_k = \max_j \theta_j \mid \text{data})$ — Thompson sampling *samples an arm with the probability it is best*.

Two limits make the self-tuning concrete.
When all posteriors are wide and overlapping (little data), the $F_j(\theta)$ are gentle ramps and no single arm dominates the integral, so $w_k \approx 1/K$ — near-uniform exploration.
When one arm's posterior separates cleanly above the rest, its $\prod_j F_j$ is near 1 over the region where its own density lives while the others' densities sit where the product is near 0, driving $w_k \to 1$ — exploitation.
No $\varepsilon$, no temperature, no annealing schedule: the collapse from exploring to exploiting is driven entirely by how much the data have concentrated the posteriors.

:::

There is rarely a need to evaluate the integral in [@eq:alloc] directly — that is the point.
Drawing one sample per arm and taking the argmax is a *Monte Carlo estimate* of pulling each arm with probability $w_k$, and it costs one random draw per arm.

### Measuring how well it does: regret

The yardstick for a bandit policy is **regret** — the reward you forfeited by not always pulling the truly-best arm $\theta^\* = \max_k \theta_k$:

\[
\text{Regret}(T) \;=\; \sum_{t=1}^{T} \big(\theta^\* - \theta_{a_t}\big)
\;=\; \sum_{k} \Delta_k\, N_k(T),
\qquad \Delta_k = \theta^\* - \theta_k ,
\]

where $N_k(T)$ is the number of times arm $k$ was pulled and $\Delta_k$ is its *suboptimality gap*.
A policy that never learns (uniform allocation) pays regret growing *linearly* in $T$, because it keeps pulling bad arms at a fixed rate.
Thompson sampling achieves **logarithmic** regret, $\mathbb{E}[\text{Regret}(T)] = O(\log T)$ — matching the Lai–Robbins lower bound on what *any* policy can achieve — because the number of pulls it wastes on each inferior arm grows only like $\log T$.
In the survey setting, low regret means **more positives found for the same number of tests**.

## The updating process, step by step

The loop that produces [@fig:bandits] is worth spelling out, because every adaptive design in this family is a variation on it.

1. **Initialize** a posterior $\text{Beta}(\alpha_k,\beta_k)$ for each of the four sites (start uniform, or encode prior surveillance data).
2. **Sample** a plausible positivity $\tilde\theta_k$ from each posterior.
3. **Allocate** the next test (or batch of tests) to the site(s) with the highest sampled positivity.
4. **Observe** how many of those tests come back positive.
5. **Update** the chosen site's posterior: add positives to $\alpha_k$, negatives to $\beta_k$.
6. **Repeat** until the budget is spent.

Because the update in step 5 is just addition, the whole procedure is cheap enough to run on a phone in the field, and it is **fully sequential**: new data change the allocation on the very next round.
The only real design choices are the priors (step 1) and the batch size (step 3) — larger batches update less often but parallelize the field work.

> [!TIP]
> Batching changes *when* you learn, not *what* you learn.
> With batch size 1 the posterior updates after every test; with batch size 25 you place 25 tests, then update once.
> Small batches adapt faster and waste fewer tests on a lagging site; large batches are logistically simpler and lose little when arms are well-separated.
> A useful default is to re-draw the Thompson allocation for each test *within* a batch, so a single batch still spreads across sites in proportion to current belief.

## Worked example: four sites

Take four sites with true (unknown) positivities $\theta = (0.06, 0.10, 0.22, 0.09)$ — site C is the hot spot.
Start every site at $\text{Beta}(1,1)$ and run 40 rounds of 25 tests, drawing a Thompson allocation for each test.
After the first few rounds the posteriors are still wide and the budget is spread fairly evenly; by round 40 close to 80% of all tests have gone to site C, its posterior is tight around 0.22, and the neglected sites keep wide posteriors — we are confident about the winner and deliberately uncertain about the also-rans, which is exactly the right allocation of *certainty* when the goal is finding cases.
Compare that to an even split, which would have spent 250 tests on each site and found far fewer positives.

## In code

### R

A complete Thompson-sampling loop over the four sites, with per-test re-draws inside each batch.

```r
set.seed(1)
p_true <- c(A = 0.06, B = 0.10, C = 0.22, D = 0.09)  # unknown to the sampler
K <- length(p_true)
a <- rep(1, K); b <- rep(1, K)                        # Beta(1,1) priors

rounds <- 40; batch <- 25
for (t in seq_len(rounds)) {
  # Thompson sampling: each test goes to the site with the largest posterior draw
  draws  <- matrix(rbeta(batch * K, a, b), nrow = batch, byrow = TRUE)
  picks  <- max.col(draws)                            # argmax per test
  for (k in seq_len(K)) {
    n_k <- sum(picks == k)
    if (n_k > 0) {
      y_k <- rbinom(1, n_k, p_true[k])                # positives observed
      a[k] <- a[k] + y_k                              # update: add positives
      b[k] <- b[k] + n_k - y_k                        #         add negatives
    }
  }
}

post_mean <- a / (a + b)
n_tests   <- (a - 1) + (b - 1)
round(rbind(posterior_mean = post_mean, tests_used = n_tests), 3)
# site C draws most of the budget and its posterior mean sits near 0.22
```

### Python

The same loop, executed at build time so the numbers are real.

```python
import numpy as np

rng = np.random.default_rng(20260711)
p_true = np.array([0.06, 0.10, 0.22, 0.09])   # sites A, B, C, D — unknown
sites = ["A", "B", "C", "D"]
K = len(p_true)
a = np.ones(K)          # Beta(1,1) priors: alpha = 1 + positives
b = np.ones(K)          #                   beta  = 1 + negatives

rounds, batch = 40, 25
for t in range(rounds):
    # one posterior draw per test, then send each test to its argmax site
    draws = rng.beta(a[None, :], b[None, :], size=(batch, K))
    picks = draws.argmax(axis=1)
    for k in range(K):
        n_k = int((picks == k).sum())
        if n_k:
            y_k = rng.binomial(n_k, p_true[k])   # positives found
            a[k] += y_k                          # conjugate update
            b[k] += n_k - y_k

post_mean = a / (a + b)
tests = (a - 1) + (b - 1)
for k in range(K):
    print(f"site {sites[k]}: {int(tests[k]):4d} tests, "
          f"posterior mean {post_mean[k]:.3f}")
print(f"total positives found: {int((a - 1).sum())} / {int(tests.sum())} tests")
```

<!-- python-output:auto -->
```text
site A:   58 tests, posterior mean 0.100
site B:  108 tests, posterior mean 0.136
site C:  797 tests, posterior mean 0.247
site D:   37 tests, posterior mean 0.103
total positives found: 218 / 1000 tests
```
<!-- /python-output:auto -->

### Julia

```julia
using Random, Distributions
Random.seed!(1)

p_true = [0.06, 0.10, 0.22, 0.09]          # sites A, B, C, D
K = length(p_true)
a = ones(K); b = ones(K)                   # Beta(1,1) priors

rounds, batch = 40, 25
for t in 1:rounds
    picks = [argmax(rand.(Beta.(a, b))) for _ in 1:batch]  # Thompson per test
    for k in 1:K
        n_k = count(==(k), picks)
        if n_k > 0
            y_k = rand(Binomial(n_k, p_true[k]))           # positives
            a[k] += y_k                                    # add positives
            b[k] += n_k - y_k                              # add negatives
        end
    end
end

println("posterior means: ", round.(a ./ (a .+ b), digits = 3))
println("tests per site:  ", Int.((a .- 1) .+ (b .- 1)))
```

### The allocation probability directly

If you want the exact probability each site is best — the $w_k$ of [@eq:alloc] — a few thousand joint posterior draws estimate it without evaluating the integral.
This is also how you report "there is a 94% chance site C has the highest positivity."

```python
def prob_best(a, b, draws=20000, seed=0):
    rng = np.random.default_rng(seed)
    samples = rng.beta(a, b, size=(draws, len(a)))   # joint posterior draws
    winners = samples.argmax(axis=1)
    return np.bincount(winners, minlength=len(a)) / draws

w = prob_best(a, b)
for k in range(K):
    print(f"P(site {sites[k]} is best) = {w[k]:.3f}")
```

<!-- python-output:auto -->
```text
P(site A is best) = 0.002
P(site B is best) = 0.002
P(site C is best) = 0.986
P(site D is best) = 0.010
```
<!-- /python-output:auto -->

## From surveillance to the clinic: adaptive trial design

Swap "sites" for "treatment arms" and "positive test" for "patient responded," and the identical machinery becomes **response-adaptive randomization (RAR)** — the engine of Bayesian adaptive clinical trials.
Instead of fixing a 1:1:1:1 allocation for the whole study, you update a posterior on each arm's success probability as outcomes arrive and steer *new* patients toward the arms that are winning.
The ethical appeal is direct: fewer trial participants are assigned to inferior treatments, because the allocation follows the accumulating evidence.

The clinical setting adds a few refinements to the bare bandit:

- **Tempered allocation.** Pure Thompson sampling can allocate very aggressively; trials often *temper* it, pulling arm $k$ with probability $\propto \big[\Pr(\text{arm } k \text{ best})\big]^{c}$ for some $0 < c < 1$, or clamping allocation away from 0 so every arm keeps accruing enough data for a valid final comparison.
- **Posterior stopping rules.** Rather than a fixed sample size, the trial stops for **superiority** when $\Pr(\theta_A > \theta_B \mid \text{data})$ crosses a high threshold (say 0.99), or for **futility** when it falls below a low one — a genuinely sequential design that can end early when the answer is clear.
- **Arm dropping and adding.** Multi-arm, multi-stage (platform) trials drop arms whose posterior probability of being best decays, and can add new arms mid-study, all under the same updating rule.

:::spoiler Show the two-arm superiority probability

For a head-to-head trial with a treatment arm and a control, put independent Beta posteriors on the two response rates, $\theta_A \sim \text{Beta}(\alpha_A,\beta_A)$ and $\theta_B \sim \text{Beta}(\alpha_B,\beta_B)$.
The decision quantity is the posterior probability that the treatment beats control:

\[
\Pr(\theta_A > \theta_B \mid \text{data})
\;=\; \int_0^1 \int_0^{\theta_A} p_A(\theta_A)\,p_B(\theta_B)\; d\theta_B \, d\theta_A
\;=\; \int_0^1 p_A(\theta)\,F_B(\theta)\; d\theta ,
\]

which is exactly the two-arm case of the allocation integral [@eq:alloc] — arm $A$ "wins" when its draw exceeds arm $B$'s.
There is a classical closed form as a sum,

\[
\Pr(\theta_B > \theta_A) \;=\; \sum_{i=0}^{\alpha_B - 1} \frac{B(\alpha_A + i,\ \beta_A + \beta_B)}{(\beta_B + i)\,B(1 + i,\ \beta_B)\,B(\alpha_A,\ \beta_A)},
\]

for integer parameters, but in practice you estimate it with a handful of Monte Carlo draws — the same `prob_best` routine above with two arms.
A trial declares superiority when this probability exceeds a pre-specified threshold chosen (by simulation) to control the frequentist type-I error at the desired level.

:::

Response-adaptive randomization has real history: the 1980s **ECMO** trial for newborns used a "play-the-winner" adaptive rule and assigned all but one infant to the treatment that was working, and modern **platform trials** — I-SPY 2 in breast cancer, REMAP-CAP in pneumonia and COVID-19 — run many arms under exactly this Bayesian-updating framework, dropping and adding treatments as posteriors evolve.
The survey-sampling bandit and the adaptive trial are the *same algorithm* pointed at different rewards.

> [!WARNING]
> Adaptivity is not free.
> Response-adaptive randomization can confound the treatment effect with **time drift** (patient characteristics changing over the trial), inflates variance for the arms it starves, and complicates the final analysis — the allocation depends on the data, so naive standard errors are wrong.
> Real trials fix the operating characteristics (type-I error, power, expected sample size) by **simulation** before enrolling anyone, and often block on calendar time to protect against drift.
> The same cautions apply to surveillance: a bandit optimized to *find* cases produces a biased estimate of each site's true prevalence, because it deliberately under-samples the quiet sites.

## Why it matters

The Bayesian bandit turns a static allocation problem into a learning loop: carry a posterior on each option, act in proportion to the probability each option is best, and let the data reshape the allocation.
For [surveillance](../epidemiology/surveillance-systems.md) it means finding more cases per test by concentrating limited diagnostic capacity where the signal is, without a human re-deciding the split each week.
For clinical research it means trials that expose fewer patients to worse treatments and can stop as soon as the evidence is decisive.
The whole apparatus rests on two ideas this site returns to again and again — [conjugate updating](bayesian-inference.md) to make learning cheap, and [posterior probabilities](bayesian-inference.md) as the currency of decisions — which is what lets one short loop serve both the field epidemiologist and the trialist.

## Related

- [Bayesian Inference](bayesian-inference.md) — the priors, likelihood, and posterior the bandit updates
- [Binomial Distribution](binomial-distribution.md) — the Beta–Binomial conjugate pair at the core
- [Survey Sampling](survey-sampling.md) — fixed designs the bandit adapts away from
- [Optimal Experimental Design](optimal-design.md) — allocating effort to learn most efficiently
- [Experimental Design](experimental-design.md) — randomization, bias, and study structure
- [Markov Chain Monte Carlo](mcmc.md) — sampling posteriors when conjugacy fails
- [Diagnostic Testing and Screening](diagnostic-testing.md) — what a "positive" means
- [Quantitative Methods](../math.md)
