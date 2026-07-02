---
title: "Detecting Selection with dN/dS"
---

# Detecting Selection with dN/dS

When a pathogen evolves, some mutations rewrite its proteins and some leave them untouched.
Comparing how fast these two kinds of change accumulate turns a protein-coding gene into a detector for natural selection.

## Synonymous vs. non-synonymous substitutions

The genetic code is redundant: most amino acids are encoded by several codons, so a nucleotide change may or may not alter the protein.
A **synonymous** substitution changes the codon but not the amino acid it specifies (for example `GGA` to `GGG`, both glycine); because the protein is unchanged, it is approximately invisible to selection and evolves close to neutrally.
A **non-synonymous** substitution changes the encoded amino acid (for example `GGA` glycine to `GAA` glutamate); it alters the protein and is therefore exposed to selection, which can remove it or promote it.
The neutral background rate of synonymous change gives us a built-in control against which to measure the fate of non-synonymous change.

## Defining $d_N$, $d_S$, and $\omega$

To make the comparison fair we normalize by opportunity, because a gene has more sites where a mutation would be non-synonymous than where it would be synonymous.
Let $d_S$ be the number of synonymous substitutions per synonymous site and $d_N$ the number of non-synonymous substitutions per non-synonymous site.
The quantity of interest is their ratio, $$\omega = \frac{d_N}{d_S}.$$ Since $d_S$ estimates the neutral rate, $\omega$ measures how selection has scaled the rate of protein-changing substitutions relative to neutral expectation:

- $\omega < 1$ — **purifying** (negative) selection: most amino-acid changes are deleterious and are removed, so $d_N$ is suppressed below $d_S$.
- $\omega = 1$ — **neutral** evolution: amino-acid changes fix at the same rate as synonymous ones.
- $\omega > 1$ — **positive** (diversifying) selection: amino-acid changes are favored and fix faster than neutral, a classic signal at antigenic sites and drug-resistance loci in pathogens.

Purifying selection dominates most genes, so a gene-wide $\omega$ well below 1 is typical; values above 1 are the striking exception worth hunting for.

## Codon models and where selection hides

Simply counting differences (as below) ignores multiple hits at the same site and the structure of the genetic code, so modern analyses fit **codon-substitution models** by [maximum likelihood](maximum-likelihood.md), estimating $\omega$ as a model parameter along the branches of a phylogeny.
Averaging $\omega$ over a whole gene is conservative: a handful of positively selected codons can be swamped by many conserved ones.
**Site models** allow $\omega$ to vary across codons and test whether a subset of sites has $\omega > 1$, pinpointing, say, the antigenic residues of an influenza surface protein.
**Branch models** let $\omega$ vary across lineages, testing whether selection intensified on a particular branch — for instance, the emergence of a drug-resistant clade.
These tests compare a model that permits $\omega > 1$ against one that does not, a nested-model comparison evaluated with the framework of [hypothesis testing](hypothesis-testing.md).

## Worked example

Suppose we align two homologous pathogen sequences of 300 codons (900 nucleotides) and, using the code's structure, classify the sites and count observed differences:

- Synonymous sites: $S = 225$; observed synonymous differences: $S_d = 18$.
- Non-synonymous sites: $N = 675$; observed non-synonymous differences: $N_d = 27$.

The crude proportions of differences are $$p_S = \frac{S_d}{S} = \frac{18}{225} = 0.080, \qquad p_N = \frac{N_d}{N} = \frac{27}{675} = 0.040.$$ Taking these proportions directly as rough distances gives $$\omega = \frac{d_N}{d_S} \approx \frac{p_N}{p_S} = \frac{0.040}{0.080} = 0.5.$$ An $\omega$ of about 0.5 points to purifying selection: protein-changing substitutions accumulate at half the neutral rate, so on average amino-acid changes here are mildly deleterious.
A rigorous analysis would apply a multiple-hits correction (such as Nei–Gojobori's Jukes–Cantor step) to convert $p_N$ and $p_S$ into $d_N$ and $d_S$, but the sign of the signal, $\omega < 1$, is already clear.

## In code

The snippets reproduce the worked counts and the crude ratio, then point to library routines that add the proper corrections.

### R

```r
# Crude omega from counts (matches the worked example)
Sd <- 18; S <- 225   # synonymous diffs and sites
Nd <- 27; N <- 675   # non-synonymous diffs and sites
pS <- Sd / S; pN <- Nd / N
omega <- pN / pS
omega                 # 0.5  -> purifying selection

# Proper estimation from an alignment with seqinr's Nei-Gojobori kaks():
# library(seqinr)
# aln <- read.alignment("genes.fasta", format = "fasta")
# kaks(aln)$ka / kaks(aln)$ks   # ka = dN, ks = dS
# (ape can read/handle trees; codon-model fitting lives in tools like codeml/PAML)
```

### Python

```python
# Crude omega from counts
Sd, S = 18, 225   # synonymous diffs, sites
Nd, N = 27, 675   # non-synonymous diffs, sites
pS, pN = Sd / S, Nd / N
omega = pN / pS
print(round(omega, 3))   # 0.5 -> purifying selection

# Proper Nei-Gojobori estimation from an alignment with Biopython:
# from Bio import SeqIO
# from Bio.codonalign.codonseq import cal_dn_ds, CodonSeq
# s1 = CodonSeq(str(rec1.seq)); s2 = CodonSeq(str(rec2.seq))
# dN, dS = cal_dn_ds(s1, s2, method="NG86")
# print(dN / dS)
```

### Julia

```julia
# Crude omega from counts (manual)
Sd, S = 18, 225      # synonymous diffs, sites
Nd, N = 27, 675      # non-synonymous diffs, sites
pS, pN = Sd / S, Nd / N
omega = pN / pS
println(round(omega, digits = 3))   # 0.5 -> purifying selection

# Optional Jukes-Cantor correction before taking the ratio:
jc(p) = -3/4 * log(1 - 4/3 * p)     # multiple-hits correction
omega_corrected = jc(pN) / jc(pS)
println(round(omega_corrected, digits = 3))   # ~0.49, same conclusion
```

## Why it matters

$d_N/d_S$ converts a protein alignment into a quantitative test for natural selection, using the gene's own synonymous sites as an internal neutral yardstick.
For pathogens this is directly actionable: $\omega > 1$ flags the antigenic sites that let a virus escape immunity and the codons where drug resistance is being selected, telling surveillance and vaccine design exactly which residues are under evolutionary pressure.

## Related

- [The Molecular Clock and Phylodynamics](molecular-clock.md)
- [Maximum Likelihood Estimation](maximum-likelihood.md)
- [Hypothesis Testing](hypothesis-testing.md)
- [Coalescent Theory](coalescent-theory.md)
- [Quantitative Methods](../math.md)
