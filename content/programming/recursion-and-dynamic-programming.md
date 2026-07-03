---
title: "Recursion & Dynamic Programming"
---

# Recursion & Dynamic Programming

Two closely related ideas from computer science quietly power a huge fraction of computational biology.
**Recursion** is solving a problem by having it call smaller copies of itself — the natural way to walk a phylogeny or explore a branching process.
**Dynamic programming** (DP) is what you do when those smaller problems *overlap*: you solve each one once, remember the answer, and reuse it — turning an impossible exponential computation into a fast one.

If you have ever run a sequence alignment, an HMM, or a phylogenetic likelihood, you have used dynamic programming, whether you knew it or not.

## Recursion: A Function That Calls Itself

A recursive function has two parts: a **base case** that stops the recursion, and a **recursive case** that reduces the problem to something smaller.
The classic (if artificial) example is the Fibonacci numbers:

```python
def fib(n):
    if n < 2:            # base case
        return n
    return fib(n - 1) + fib(n - 2)   # recursive case
```

Recursion shines when the *data* is recursive.
A phylogenetic tree is defined recursively — a node is either a tip, or an internal node with child subtrees — so the natural way to compute anything on it is a function that calls itself on each child:

```python
# The shape of nearly every tree algorithm in phylogenetics
def postorder(node):
    if node.is_tip():
        return base_value(node)          # base case: a leaf
    results = [postorder(child) for child in node.children]
    return combine(results)              # recursive case: merge children
```

## Why Naive Recursion Can Explode

The trouble with `fib` above is that it recomputes the same values enormously many times: `fib(50)` calls `fib(48)` twice, `fib(47)` three times, and so on — an **exponential** `O(2ⁿ)` blowup (the worst row of the [Big-O](big-o-and-complexity.md) chart).
The subproblems **overlap**, and naive recursion is blind to it.

Count the calls and the explosion is undeniable:

```python
calls = {"naive": 0, "memo": 0}

def fib_naive(n):
    calls["naive"] += 1
    if n < 2:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

memo = {}
def fib_memo(n):
    calls["memo"] += 1
    if n < 2:
        return n
    if n not in memo:                       # solve each subproblem once
        memo[n] = fib_memo(n - 1) + fib_memo(n - 2)
    return memo[n]

for n in (10, 20, 30):
    calls["naive"] = calls["memo"] = 0
    memo.clear()
    fib_naive(n); fib_memo(n)
    print(f"fib({n}):  naive = {calls['naive']:>7,} calls   memoized = {calls['memo']:>3} calls")
```

<!-- python-output:auto -->
```text
fib(10):  naive =     177 calls   memoized =  19 calls
fib(20):  naive =  21,891 calls   memoized =  39 calls
fib(30):  naive = 2,692,537 calls   memoized =  59 calls
```
<!-- /python-output:auto -->

## Dynamic Programming: Solve Each Subproblem Once

**Memoization** — caching each subproblem's answer in a [hash map](data-structures.md) — is the smallest possible fix, and it collapses that exponential cost to **linear**.
That is the whole idea of dynamic programming: *when subproblems recur, compute each one only once.* DP is usually written one of two ways:

- **Top-down (memoized recursion):** keep the recursive code, add a cache, as in `fib_memo` above.
- **Bottom-up (a table):** fill a table of subproblem answers in order, each cell built from earlier ones.
  This is how alignment and HMM algorithms are usually written.

## The Canonical Example: Sequence Alignment

Global alignment (**Needleman–Wunsch**) is dynamic programming at its most visual.
Build a table whose cell $(i, j)$ holds the best possible score for aligning the first $i$ letters of one sequence with the first $j$ letters of the other.
Each cell is filled **once**, from the three neighbours it already depends on — diagonal (match/mismatch), up (a gap), or left (a gap):

$$ H_{i,j} = \max \begin{cases} H_{i-1,j-1} + s(a_i, b_j) & \text{align } a_i \text{ with } b_j \\ H_{i-1,j} + \text{gap} \\ H_{i,j-1} + \text{gap} \end{cases} $$

Once the table is full, the best alignment is recovered by **tracing back** the path of winning choices from the bottom-right corner to the top-left.

![A Needleman–Wunsch alignment matrix: each cell holds the best score for aligning the two prefixes, filled once from its upper-left, upper, and left neighbours; the red path is the optimal alignment recovered by tracing back from the bottom-right corner.](../assets/figures/dynamic-programming-alignment.svg)

Filling an `n × m` table costs `O(n·m)` — quadratic, and entirely tractable — whereas enumerating every possible alignment would be astronomically exponential.
That single change, from "try every alignment" to "fill a table once," is what makes alignment possible at all.

## Dynamic Programming Is Everywhere in Biology

The same "fill a table of overlapping subproblems, then trace back" pattern recurs across the field:

- **Sequence alignment** — Needleman–Wunsch (global) and Smith–Waterman (local), the foundation of BLAST-style search.
- **Hidden Markov Models** — the **Viterbi** algorithm (most likely hidden path) and the **forward** algorithm (total probability) fill a states × positions table; used in gene finding, profile HMMs, and base calling.
- **Phylogenetics** — **Felsenstein's pruning algorithm** computes a tree's likelihood by a post-order recursion that reuses each subtree's result exactly once, combined with the [log-sum-exp trick](floating-point-and-numerical-stability.md) for stability.
- **RNA secondary structure** — the Nussinov and Zuker algorithms fold sequences by DP over subsequences.
- **Genotype/pedigree likelihoods** — peeling algorithms sum over unobserved genotypes with the same reuse-the-subproblem structure.

Recognizing that a problem has **overlapping subproblems** is the signal to reach for dynamic programming — and it is often the difference between a calculation that finishes and one that never does.

## Related

- [Big-O Notation & Computational Complexity](big-o-and-complexity.md) — the exponential-to-linear speedup DP delivers
- [Data Structures & Choosing the Right Container](data-structures.md) — the hash map behind memoization; trees for phylogenies
- [Floating-Point Arithmetic & Numerical Stability](floating-point-and-numerical-stability.md) — log-space sums inside the forward and pruning algorithms
- [A Simulation Toolkit](simulation-toolkit.md) — recursion for branching processes and genealogies
- [Programming & Computing](../programming.md)
