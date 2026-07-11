---
title: "Multiple Testing and False Discovery Rate"
---

# Multiple Testing and False Discovery Rate

Run one hypothesis test and a 5% false-positive rate is tolerable; run a million and you drown in spurious "discoveries."
Correcting for the number of tests is what keeps large-scale screens — gene expression, imaging, and especially genome-wide scans — honest.

![The worked five-test example, with sorted p-values plotted against their rank. Bonferroni compares each to a flat threshold $\alpha/m = 0.01$, which only the first two clear; Benjamini–Hochberg compares each to a sloped threshold $\frac{i}{m}\alpha$, which the first four clear. BH's rising line admits more discoveries in exchange for controlling the false discovery rate rather than the family-wise error rate.](../assets/figures/multiple-testing.svg "fig:multiple-testing")

## The problem

Suppose you perform $m$ independent tests, and in truth every null is true.
If you reject whenever [p](p-values.md) $\le \alpha$, then each test has probability $\alpha$ of a false positive, so the expected number of false positives is

\[
\mathbb{E}[\text{false positives}] = m\alpha.
\]

With $m = 1{,}000{,}000$ and $\alpha = 0.05$ that is 50,000 false alarms.
The probability of **at least one** false positive is $1 - (1-\alpha)^m$, which is essentially $1$ for even a few hundred tests.
Some form of correction is unavoidable.

## Family-wise error rate and Bonferroni

The **family-wise error rate (FWER)** is the probability of making *one or more* false rejections across the whole family of tests.
The **Bonferroni correction** controls it by testing each hypothesis at the stricter level

\[
\alpha_{\text{Bonf}} = \frac{\alpha}{m},
\]

equivalently by multiplying each p-value by $m$ and comparing to $\alpha$.
By the union bound, this guarantees $\text{FWER} \le \alpha$ regardless of dependence between tests.
It is simple and robust but conservative: when $m$ is huge, the threshold becomes so small that real but modest effects are missed.

## The false discovery rate

Bonferroni asks "what is the chance of *any* false positive?"
For large screens a gentler question is often more useful: "of the discoveries I *declare*, what fraction are false?"
That is the **false discovery rate (FDR)**, the expected proportion of false positives among rejected hypotheses:

\[
\text{FDR} = \mathbb{E}\!\left[\frac{V}{\max(R, 1)}\right],
\]

where $R$ is the number of rejections and $V$ the number of those that are truly null.
Controlling the FDR at, say, $0.10$ accepts that about 10% of your hits may be false in exchange for far more power than FWER control.

### The Benjamini–Hochberg procedure

Benjamini and Hochberg (BH) control the FDR with a simple sort-and-compare rule.
Order the p-values $p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}$.
Find the largest rank $i$ for which

\[
p_{(i)} \le \frac{i}{m}\,\alpha,
\]

and reject all hypotheses with rank $\le i$.
Under independence (and many forms of positive dependence) this guarantees $\text{FDR} \le \alpha$.
The **q-value** of a test is the smallest FDR at which it would be declared significant — the FDR analogue of a p-value.

## Why GWAS uses $5 \times 10^{-8}$

A genome-wide scan tests roughly one million effectively independent variants.
The genome-wide significance threshold is exactly Bonferroni applied to that count, $0.05 / 10^{6} = 5 \times 10^{-8}$, controlling the FWER so that a declared association is very unlikely to be a fluke — see [GWAS](gwas.md).

## Worked example

Take five p-values from five tests: $0.001,\ 0.008,\ 0.02,\ 0.04,\ 0.5$, with $m = 5$ and $\alpha = 0.05$.

**Bonferroni:** compare each to $\alpha/m = 0.01$.
Only $0.001$ and $0.008$ survive — two discoveries.

**Benjamini–Hochberg:** sorted, the thresholds $\frac{i}{m}\alpha$ are $0.01,\ 0.02,\ 0.03,\ 0.04,\ 0.05$.

| rank $i$ | $p_{(i)}$ | $\frac{i}{m}\alpha$ | $p_{(i)} \le$ threshold? |
|----------|-----------|---------------------|--------------------------|
| 1 | 0.001 | 0.01 | yes |
| 2 | 0.008 | 0.02 | yes |
| 3 | 0.020 | 0.03 | yes |
| 4 | 0.040 | 0.04 | yes |
| 5 | 0.500 | 0.05 | no |

The largest passing rank is $i = 4$, so BH rejects the first four — more discoveries than Bonferroni, at the cost of controlling only the FDR ([@fig:multiple-testing]).

## In code

### R

```r
p <- c(0.001, 0.008, 0.02, 0.04, 0.5)
p.adjust(p, method = "bonferroni")   # 0.005 0.040 0.100 0.200 1.000
p.adjust(p, method = "BH")           # 0.005 0.020 0.033 0.050 0.500
which(p.adjust(p, "BH") <= 0.05)     # 1 2 3 4
```

### Python

```python
from statsmodels.stats.multitest import multipletests
p = [0.001, 0.008, 0.02, 0.04, 0.5]

print(multipletests(p, alpha=0.05, method="bonferroni")[1])
# [0.005 0.04  0.1   0.2   1.   ]
rej, q, *_ = multipletests(p, alpha=0.05, method="fdr_bh")
print(rej)   # [ True  True  True  True False]
print(q)     # [0.005 0.02  0.0333 0.05  0.5  ]
```

<!-- python-output:auto -->
```text
[0.005 0.04  0.1   0.2   1.   ]
[ True  True  True  True False]
[0.005      0.02       0.03333333 0.05       0.5       ]
```
<!-- /python-output:auto -->

### Julia

```julia
p = [0.001, 0.008, 0.02, 0.04, 0.5]
m = length(p)

# Manual Benjamini-Hochberg
o = sortperm(p)
ps = p[o]
thresh = (1:m) ./ m .* 0.05
kmax = findlast(ps .<= thresh)          # 4
reject = falses(m); reject[o[1:kmax]] .= true
reject                                    # first four true
# Package alternative: using MultipleTesting; adjust(PValues(p), BenjaminiHochberg())
```

## Why it matters

Multiple-testing control is the reason large screens produce reproducible findings instead of a graveyard of false leads.
Choosing between FWER control (Bonferroni, when any false positive is costly) and FDR control (BH, when you can tolerate a known fraction of them among many hits) is one of the central design decisions in genomics, neuroimaging, and any high-dimensional analysis.

## Related

- [p-Values](p-values.md)
- [Hypothesis testing](hypothesis-testing.md)
- [Genome-Wide Association Studies](gwas.md)
- [Quantitative Methods](../math.md)
