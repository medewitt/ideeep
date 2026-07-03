---
title: "Data Structures & Choosing the Right Container"
---

# Data Structures & Choosing the Right Container

A **data structure** is just a way of organizing data in memory so that the operations you care about are cheap.
It is the practical companion to [Big-O notation](big-o-and-complexity.md): the *same* algorithm can be fast or hopelessly slow depending only on which container you store your data in.
Choosing well is often the single easiest way to turn an overnight run into a one-second one.

The key idea is that different containers make different operations cheap, and you pick the one whose cheap operation is the one you do most.

![Doing n membership tests against a list scans the whole list each time — O(n) per lookup, O(n²) total — while the same tests against a set or dictionary are O(1) each, O(n) total; at 100,000 items that is a 50,000-fold difference.](../assets/figures/data-structure-lookup.svg)

## The Four You Actually Need

For everyday scientific computing, almost everything is one of these:

| Structure | Also called | Cheap operation | Use it when… |
|-----------|-------------|-----------------|--------------|
| **Array / vector** | list, `numpy` array | read/write by position `x[i]` (`O(1)`); scan (`O(n)`) | you have an ordered sequence and mostly march through it |
| **Hash map** | dictionary, `dict`, named list, environment | look up **by key** (`O(1)`) | you look things up by a label: gene → count, id → record |
| **Hash set** | `set` | "have I seen this?" (`O(1)`) | you track membership or unique items |
| **Tree / graph** | — | hierarchical / linked relationships | phylogenies, contact networks, taxonomies |

The two that most often rescue a slow script are the **hash map** and **hash set**, because they turn a linear *search* into a constant-time *lookup*.

## The Move That Fixes Most Slow Code: List → Set

Here is the [`O(n²)` trap](big-o-and-complexity.md) in its most common disguise.
You have a collection and you keep asking "is this thing already in it?"
If the collection is a **list**, each check scans the whole list, so `n` checks cost `O(n²)`:

```python
# SLOW: `x in a_list` scans the list every time -> O(n^2) overall
seen = []
for s in samples:
    if s not in seen:          # O(n) scan, repeated n times
        seen.append(s)
```

Switch the collection to a **set** and each check becomes `O(1)`, so the whole loop drops to `O(n)` — the difference the figure above shows:

```python
# FAST: `x in a_set` is O(1) -> O(n) overall
seen = set()
for s in samples:
    if s not in seen:          # O(1) hash lookup
        seen.add(s)
```

You can watch the operation counts diverge exactly as the doubling test predicts — the list version quadruples each time `n` doubles, the set version merely doubles:

```python
def list_lookups(n):
    """n membership tests against a growing list: O(n^2)."""
    data, ops = list(range(n)), 0
    for q in range(n):
        for item in data:          # linear scan until found
            ops += 1
            if item == q:
                break
    return ops

def set_lookups(n):
    """n membership tests against a set: O(n) (each test is O(1))."""
    data = set(range(n))
    return sum(1 for q in range(n) if q in data)

print(f"{'n':>5} | {'list ops':>10} | {'set ops':>8}")
print("-" * 31)
for n in [50, 100, 200, 400]:
    print(f"{n:>5} | {list_lookups(n):>10,} | {set_lookups(n):>8,}")
```

<!-- python-output:auto -->
```text
    n |   list ops |  set ops
-------------------------------
   50 |      1,275 |       50
  100 |      5,050 |      100
  200 |     20,100 |      200
  400 |     80,200 |      400
```
<!-- /python-output:auto -->

## Hash Maps for Counting and Lookups

The other workhorse is the **hash map**: a lookup table keyed by something meaningful.
Counting k-mers, tallying species, mapping a sample ID to its metadata, or caching a codon → amino-acid table are all one-liners with a dictionary, and every lookup is `O(1)`.

```python
# Count 3-mers in a sequence -- a dict keyed by the k-mer
seq, k = "ATGATCGATCGGATCGATCGATCG", 3
counts = {}
for i in range(len(seq) - k + 1):
    kmer = seq[i:i + k]
    counts[kmer] = counts.get(kmer, 0) + 1

for kmer in sorted(counts):
    print(kmer, counts[kmer])
```

<!-- python-output:auto -->
```text
ATC 5
ATG 1
CGA 3
CGG 1
GAT 5
GGA 1
TCG 5
TGA 1
```
<!-- /python-output:auto -->

The same idea across the three languages:

```r
# R: a named list or environment is a hash map; table() counts in one call
counts <- table(substring(seq, 1:(nchar(seq) - k + 1), k:nchar(seq)))
seen <- new.env()                 # an environment is a real hash map
assign("ACGT", TRUE, envir = seen)
exists("ACGT", envir = seen)      # O(1) membership test
```

```julia
# Julia: Dict and Set are first-class and fast
counts = Dict{String,Int}()
counts[kmer] = get(counts, kmer, 0) + 1
seen = Set{String}()
push!(seen, "ACGT"); "ACGT" in seen      # O(1)
```

```python
# Python: dict/set, plus Counter for the common counting case
from collections import Counter
counts = Counter(seq[i:i+k] for i in range(len(seq) - k + 1))
```

## Trees and Graphs

Some biological data is fundamentally **linked** rather than flat, and a tree or graph is the honest representation:

- **Phylogenies** are trees; you traverse them with [recursion and dynamic programming](recursion-and-dynamic-programming.md) (Felsenstein's pruning walks a tree bottom-up).
- **Contact, food-web, and metabolic networks** are graphs; storing them as an **adjacency list** (a hash map from each node to its neighbours) keeps "who touches whom?" cheap — see [ecological networks](../math/ecological-networks.md) and [network models](../math/network-models.md).

The practical point is the same: represent the relationships directly instead of flattening them into a list you have to search over and over.

## Choosing in Practice

- **Look things up by a label?** Hash map (dict / named list).
  Not a list you search.
- **Track "have I seen this?" or "unique values"?** Hash set.
  Not a list with `x in list`.
- **Ordered data you scan or index by position?** Array / vector — and prefer a vectorized operation over a hand-written loop.
- **Hierarchies or networks?** Tree or graph (adjacency list), not a table of pairs.
- **When a script is mysteriously slow,** look for a list being searched inside a loop — swapping it for a set or dict is usually the whole fix.

## Related

- [Big-O Notation & Computational Complexity](big-o-and-complexity.md) — why the container changes the complexity
- [Recursion & Dynamic Programming](recursion-and-dynamic-programming.md) — algorithms that walk trees and tables
- [A Simulation Toolkit](simulation-toolkit.md) — where fast lookups keep inner loops cheap
- [Manipulating Data Frames](../math/manipulating-data.md) — the tabular container for analysis-ready data
- [Ecological Networks](../math/ecological-networks.md) and [Network Models](../math/network-models.md) — graphs in biology
- [Programming & Computing](../programming.md)
