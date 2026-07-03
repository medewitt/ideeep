---
title: "Parallelism & Concurrency"
---

# Parallelism & Concurrency

A modern laptop has 8 or more **cores**, and a [cluster node](hpc-clusters-slurm.md) has dozens.
Running work on many cores at once — **parallelism** — is how a 1,000-replicate simulation study or a set of MCMC chains finishes in an hour instead of a day.
But parallel code introduces failure modes that serial code simply does not have: results that come out **wrong** (race conditions), results that are **slower** than serial (oversubscription), and bugs that **refuse to reproduce**.

This page is about getting the speedup without the surprises — with particular attention to the thread-setting traps that bite users of Stan, `data.table`, and multithreaded math libraries.

## Cores, Processes, and Threads

Three words that are easy to blur but matter here:

- A **core** is a physical unit that executes instructions.
  `N` cores can do `N` things at literally the same time.
- A **process** is a running program with its **own private memory**.
  Two processes can't accidentally corrupt each other's data.
- A **thread** is a unit of execution *inside* a process; multiple threads **share the same memory**.
  That sharing is what makes threads fast to coordinate — and what makes them dangerous.

The one-line summary: **processes are isolated and safe; threads are shared and fast but hazardous.**

## The Easy, Safe Kind: Embarrassingly Parallel

Most parallelism in mathematical biology is the good kind: many **independent** tasks that don't need to talk to each other — 1,000 simulation replicates, 4 MCMC chains, a grid of parameter values, a bootstrap.
Each task runs on its own, and you just collect the results.
This **parallel-map** pattern is safe because nothing is shared and mutated.

```r
# R: run independent replicates across cores (furrr = purrr + future)
library(furrr)
plan(multisession, workers = 8)
results <- future_map(1:1000, run_one_replicate,
                      .options = furrr_options(seed = TRUE))  # per-worker RNG
```

```python
# Python: a process pool sidesteps the GIL for CPU-bound work
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run_one_replicate, range(1000)))
```

```julia
# Julia: independent tasks over threads
using Base.Threads
results = Vector{Float64}(undef, 1000)
@threads for i in 1:1000
    results[i] = run_one_replicate(i)     # each i writes its OWN slot -> safe
end
```

Prefer this pattern whenever you can.
If tasks are independent, parallelism is almost free of danger.

## Race Conditions: When Threads Share State

The trouble starts when parallel workers **read and write the same data**.
Because an operation as innocent as `count = count + 1` is really three steps — read, add, write — two threads can interleave so that one update is silently lost.

![Two threads each add 1 to a shared counter, but both read the same old value of 0 before either writes back, so one increment is lost and the final count is 1 instead of 2 — a race condition.](../assets/figures/race-condition.svg)

This is a **race condition**, and it has three nasty properties: the answer is **wrong**, it is **nondeterministic** (depends on timing, so it changes run to run), and it therefore often **can't be reproduced** on demand — the worst kind of bug.

The defenses, in order of preference:

1. **Don't share mutable state.** Give each worker its own output slot or return value and combine at the end (the parallel-map pattern above).
   This is by far the best option.
2. **Use a reduction.** Frameworks provide safe parallel `sum`/`+` reductions that avoid the shared-counter trap.
3. **Lock the shared resource** (a mutex) only as a last resort — it is easy to get wrong and it serializes the very code you parallelized.

A subtler cousin: even a *correct* parallel sum can give slightly **different low-order digits** each run, because [floating-point addition](floating-point-and-numerical-stability.md) is not associative and threads finish in a different order.
Round before testing for equality.

## Amdahl's Law: Why 64 Cores ≠ 64× Faster

Parallelism only speeds up the part of your program that actually runs in parallel.
If a fraction $p$ of the work is parallelizable and the rest is inherently serial, the best possible speedup on $n$ workers is

$$ \text{speedup} = \frac{1}{(1 - p) + p/n} .
$$

The serial remainder sets a hard ceiling, and the returns diminish fast:

```python
def amdahl(p, n):
    return 1 / ((1 - p) + p / n)

print(f"{'workers':>7} | {'p=0.50':>7} | {'p=0.90':>7} | {'p=0.99':>7}")
print("-" * 38)
for n in [2, 4, 8, 16, 64, 256]:
    print(f"{n:>7} | {amdahl(0.50, n):>7.2f} | {amdahl(0.90, n):>7.2f} | {amdahl(0.99, n):>7.2f}")
```

<!-- python-output:auto -->
```text
workers |  p=0.50 |  p=0.90 |  p=0.99
--------------------------------------
      2 |    1.33 |    1.82 |    1.98
      4 |    1.60 |    3.08 |    3.88
      8 |    1.78 |    4.71 |    7.48
     16 |    1.88 |    6.40 |   13.91
     64 |    1.97 |    8.77 |   39.26
    256 |    1.99 |    9.66 |   72.11
```
<!-- /python-output:auto -->

Even code that is 90% parallel can never exceed a 10× speedup, no matter how many cores you throw at it.
The practical lesson: **profile to find the serial bottleneck** (see [vectorization & profiling](vectorization-and-performance.md)) before scaling out, and don't request 64 cores for a job that can't use them.

## The Oversubscription Trap (Stan, data.table, BLAS)

This is the mistake that most often makes parallel scientific code *slower* than serial, and it is worth understanding concretely.
Many libraries **already multithread internally**.
When you then run them inside your *own* parallel loop, the thread counts **multiply**: with 8 workers each spawning 8 internal threads, you get **64 threads fighting over 8 cores**, and they spend their time context-switching instead of computing.

The rule is to **parallelize at exactly one level**: either run `N` single-threaded workers, or one job with `N` internal threads — never `N × N`.

**Stan** (`rstan` / `cmdstanr`) runs one **chain per core** by default, which is the natural parallelism.
If you *also* turn on within-chain threading (`reduce_sum`, `threads_per_chain`), the total is `chains × threads_per_chain`, and you must keep that at or below your physical core count:

```r
# cmdstanr: 4 chains in parallel, 2 threads each = 8 threads on an 8-core box
fit <- mod$sample(data = dat,
                  chains = 4, parallel_chains = 4,
                  threads_per_chain = 2)     # 4 x 2 = 8, matches the cores
```

**`data.table`** uses many threads by default (`getDTthreads()`).
Inside a parallel `foreach`/`future_map`, *each worker* then launches a full set of `data.table` threads — classic oversubscription.
Pin it to one thread inside workers:

```r
library(data.table)
# inside each parallel worker:
setDTthreads(1)          # let the OUTER parallelism own the cores
```

**BLAS / OpenMP** (OpenBLAS, MKL) multithread matrix algebra automatically.
Combined with a multiprocessing loop, you again oversubscribe.
Cap the inner threads to one in each worker:

```bash
# set before launching R/Python workers, or per-worker
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
```

```r
# R equivalent, inside a worker
RhpcBLASctl::blas_set_num_threads(1)
```

When you request cores from [SLURM](hpc-clusters-slurm.md), match the library's thread count to `--cpus-per-task`, and set the inner libraries to 1 thread when the outer loop is doing the parallelizing.

## Threads, Reproducibility, and the GIL

- **Reproducibility needs per-worker seeds.** Never let parallel workers share one generator or reuse one seed; derive an independent stream for each, as on the [randomness](randomness-and-rng.md) page (`future`'s `seed = TRUE`, `SeedSequence.spawn`, L'Ecuyer-CMRG).
- **Python's GIL** means threads do *not* speed up CPU-bound pure-Python code — only one thread runs Python bytecode at a time.
  Use **processes** (`ProcessPoolExecutor`, `joblib`) for CPU-bound work; threads help only for I/O or code that drops into compiled libraries (NumPy) that release the GIL.
- **Set the thread count explicitly** (`OMP_NUM_THREADS`, `setDTthreads`, `JULIA_NUM_THREADS`, `torch.set_num_threads`) rather than trusting defaults — the default is often "all cores," which is exactly what oversubscribes.

## A Short Checklist

- **Prefer embarrassingly-parallel maps** over shared mutable state; give each worker its own output.
- **Never share a mutable variable** across threads without a reduction or lock — race conditions are silent and wrong.
- **Parallelize at one level only.** Set inner libraries (`data.table`, BLAS, Stan threads) to 1 when an outer loop owns the cores.
- **Match total threads to physical cores** (and to `--cpus-per-task` on a cluster).
- **Remember Amdahl's law** — the serial part caps the speedup; profile before scaling out.
- **Seed every worker independently** for reproducible parallel results.

## Related

- [Running Jobs on an HPC Cluster (SLURM)](hpc-clusters-slurm.md) — requesting cores and mapping them to threads
- [Vectorization, Memory & Profiling](vectorization-and-performance.md) — squeeze one core before reaching for many
- [Randomness & Random Number Generation](randomness-and-rng.md) — independent RNG streams per worker
- [Floating-Point Arithmetic & Numerical Stability](floating-point-and-numerical-stability.md) — why parallel sums vary in the last digits
- [A Simulation Toolkit](simulation-toolkit.md) — the replicate studies you'll parallelize
- [Programming & Computing](../programming.md)
