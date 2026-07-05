---
title: "Genomic Surveillance"
description: "Linking pathogen genome sequences to epidemiologic metadata to detect outbreaks, reconstruct transmission, and act on resistance in near real time."
---

# Genomic Surveillance

Two patients infected by the same chain carry pathogens whose genomes differ by only a handful of mutations, while unrelated infections differ by many.
Genomic surveillance turns that fact into a tool: sequence the pathogen, count the differences, and read who is linked to whom.
The power comes not from the sequence alone but from joining it to metadata such as date, place, and host, so that a phylogeny becomes an epidemiologic map.

![A pairwise SNP-distance heatmap among sampled genomes, with low-distance blocks on the diagonal outlined as transmission clusters.](../assets/figures/genomic-surveillance.svg)

## The end-to-end workflow

A genomic-surveillance system is a pipeline, not a single assay.
A clinical or environmental sample is collected, its nucleic acid extracted, and the pathogen sequenced, most often on Illumina short-read platforms for accuracy or Oxford Nanopore for portable, real-time reads.
Raw reads are quality-controlled and assembled into a consensus genome, which is aligned against a reference and against other samples.
Phylogenetic reconstruction then places each genome on a tree, and the tree is only useful once each tip is annotated with its collection date, location, and host.
That last step, integration with [surveillance metadata](surveillance-systems.md), is what separates genomic epidemiology from sequencing for its own sake ([Hill et al., 2021, Trends in Parasitology](https://consensus.app/papers/details/b580a796765159219179e4863343ba7e/?utm_source=claude_desktop)).

## SNP distances and transmission clusters

The simplest link measure is the single-nucleotide polymorphism (SNP) distance: the number of aligned positions at which two genomes differ.
Isolates within a recent transmission chain sit within a few SNPs of one another, so a distance threshold separates plausible links from background diversity.
A common rule is **single-linkage clustering**: two isolates join the same cluster if they are within the threshold of *any* current cluster member, chaining links together transitively.
The threshold is pathogen-specific and calibrated to the substitution rate, or [molecular clock](../math/molecular-clock.md), and to the expected timescale of transmission.
Clusters defined this way are hypotheses about who infected whom, to be confirmed with classical [outbreak investigation](outbreak-investigation.md), not proofs on their own.

## Genotype to phenotype

Sequence also encodes function, so the same data that place an isolate on a tree can predict its **antimicrobial resistance** phenotype.
Known resistance determinants, point mutations in target genes or acquired resistance genes, are looked up against curated databases to infer which drugs will fail.
This genotype-to-phenotype inference is fast and scalable, but it is only as complete as the catalogue of known mechanisms, so a susceptible prediction is weaker evidence than a resistant one.
Layering resistance onto the transmission tree shows not just that a cluster is spreading but whether a resistant lineage is the one gaining ground.

## Established systems and tools

Genomic surveillance is already operational, not hypothetical.
For foodborne disease, the United States runs **PulseNet** and the FDA's **GenomeTrakr**, national networks that routinely sequence enteric pathogens and match isolates across states to detect multi-jurisdiction outbreaks faster than interviews alone ([Gensheimer et al., 2024, Journal of Public Health Management & Practice](https://consensus.app/papers/details/512507a1850859689bdc463c5ba04301/?utm_source=claude_desktop)).
For pathogens with faster clocks, **Nextstrain-style** workflows continuously ingest new genomes and render updated phylogenies for public health teams.
These systems share a design: standardized sequencing, shared reference databases, and automated cluster detection wired directly into response.

## Retrospective versus prospective

A retrospective study sequences an outbreak after it ends and explains what happened.
Prospective, **actionable** surveillance sequences as cases arrive and changes what happens next: closing a contaminated production line, flagging a resistant clone, or redirecting contact tracing this week.
The scientific content can be identical, but the value depends on turnaround, because a cluster detected months late informs the literature while one detected in days informs control ([Stockdale et al., 2022, Nature Microbiology](https://consensus.app/papers/details/17ea70c5760d59d79e155de7f759c77e/?utm_source=claude_desktop)).
Building prospective capacity is largely an operational problem of speed, integration, and trust, distinct from the analysis itself.

## The workforce and governance gap

The binding constraint is rarely the sequencer; it is people, computing, and agreements.
Consensus calling, alignment, and phylogenetics demand bioinformatics skills and high-performance computing that many surveillance settings lack, and training provision is unevenly distributed across regions and institutions ([Matimba et al., 2026, Frontiers in Public Health](https://consensus.app/papers/details/62fd70c777265b4095488e1d8d1267f4/?utm_source=claude_desktop)).
Sequences are also only comparable when metadata follow shared standards, and only useful globally when data are shared equitably rather than trapped by legal or political friction.
Closing this gap is a stated priority: sustained investment in the genomics and bioinformatics workforce is what turns hardware into a functioning surveillance system ([Onywera et al., 2023, The Lancet Infectious Diseases](https://consensus.app/papers/details/0347c1547c2b549bb5dae9d0d2a7f806/?utm_source=claude_desktop)).
This is why applied, surveillance-oriented training differs from generic bioinformatics coursework: it centers metadata, turnaround, and public-health decisions, not algorithms in isolation.

## A worked example

Consider six toy isolates, each a 20-nucleotide aligned fragment.
Sequences A, B, and C differ from one another by only one or two SNPs; D and E differ from each other by one SNP but by many from the first three; F stands alone.
Computing all pairwise Hamming distances gives a 6-by-6 matrix, and applying single-linkage at a threshold of **at most 2 SNPs** merges A, B, and C into one cluster and D, E into a second, while F remains a singleton.
The threshold is doing the real work: loosen it and the two clusters would eventually chain together, tighten it and A-B-C would fragment.

## In code

The Python below builds the SNP-distance matrix for the six fixed sequences and forms clusters by single-linkage at a threshold of two SNPs.

### R

```r
seqs <- c(
  A = "ACGTACGTACGTACGTACGT",
  B = "ACGTACGTACGTACGTACGA",
  C = "ACGTACGTACGTACGTACTA",
  D = "TGCATGCATGCATGCATGCA",
  E = "TGCATGCATGCATGCATGCT",
  F = "GGGGCCCCTTTTAAAACGCG"
)
m <- do.call(rbind, strsplit(seqs, ""))
d <- as.matrix(dist(m, method = "manhattan")) / 1  # Hamming for equal-length
# Single-linkage clusters at <= 2 SNPs:
cl <- cutree(hclust(as.dist(d), method = "single"), h = 2)
print(cl)
```

### Python

```python
import numpy as np

names = ["A", "B", "C", "D", "E", "F"]
seqs = [
    "ACGTACGTACGTACGTACGT",  # A
    "ACGTACGTACGTACGTACGA",  # B: 1 SNP from A
    "ACGTACGTACGTACGTACTA",  # C: 2 SNPs from A
    "TGCATGCATGCATGCATGCA",  # D
    "TGCATGCATGCATGCATGCT",  # E: 1 SNP from D
    "GGGGCCCCTTTTAAAACGCG",  # F: singleton
]
S = np.array([list(s) for s in seqs])

# Pairwise Hamming (SNP) distances.
n = len(seqs)
D = np.array([[int((S[i] != S[j]).sum()) for j in range(n)] for i in range(n)])

# Single-linkage clustering at a threshold of <= 2 SNPs.
threshold = 2
cluster = list(range(n))
for i in range(n):
    for j in range(i + 1, n):
        if D[i, j] <= threshold:
            lo, hi = sorted((cluster[i], cluster[j]))
            cluster = [lo if c == hi else c for c in cluster]

print("SNP distance matrix:")
print(D)
print("cluster labels:", [cluster[k] for k in range(n)])
for k, name in enumerate(names):
    print(name, "-> cluster", cluster[k])
```

<!-- python-output:auto -->
```text
SNP distance matrix:
[[ 0  1  2 20 19 16]
 [ 1  0  1 19 20 16]
 [ 2  1  0 19 20 16]
 [20 19 19  0  1 14]
 [19 20 20  1  0 14]
 [16 16 16 14 14  0]]
cluster labels: [0, 0, 0, 3, 3, 5]
A -> cluster 0
B -> cluster 0
C -> cluster 0
D -> cluster 3
E -> cluster 3
F -> cluster 5
```
<!-- /python-output:auto -->

### Julia

```julia
names = ["A","B","C","D","E","F"]
seqs = ["ACGTACGTACGTACGTACGT","ACGTACGTACGTACGTACGA",
        "ACGTACGTACGTACGTACTA","TGCATGCATGCATGCATGCA",
        "TGCATGCATGCATGCATGCT","GGGGCCCCTTTTAAAACGCG"]
S = permutedims(hcat(collect.(seqs)...))
n = length(seqs)
D = [sum(S[i, :] .!= S[j, :]) for i in 1:n, j in 1:n]  # Hamming distances
# Single-linkage at <= 2 SNPs then chains links transitively.
println(D)
```

## Why it matters

A pathogen genome carries a record of transmission that interviews cannot recover, and joining it to date, place, and host turns that record into an outbreak map with resistance annotated on it.
Made prospective, the same analysis stops chains and guides treatment in the window where action still changes the trajectory.
The remaining barrier is human and institutional, so investing in bioinformatics skills, computing, and equitable data sharing is what decides whether genomic surveillance stays retrospective science or becomes routine public-health practice.

## Related

- [Phylodynamics](../math/phylodynamics.md)
- [The molecular clock](../math/molecular-clock.md)
- [Coalescent theory](../math/coalescent-theory.md)
- [Diagnostics and surveillance](../diagnostics.md)
- [Epidemiology](../epidemiology.md)
