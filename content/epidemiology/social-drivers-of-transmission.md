---
title: "Social and Structural Drivers of Transmission"
description: "How social, structural, and cultural forces decide who is exposed, who is susceptible, who reaches care, and who is counted — and why transmission models that ignore them are incomplete."
---

# Social and Structural Drivers of Transmission

A pathogen does not spread through an undifferentiated crowd; it spreads through a society that has already sorted people into who shares a bedroom, who rides a crowded bus to a job that cannot be done from home, and who can afford to stay home when sick.
Those social arrangements decide who is exposed, who is susceptible, who seeks care, and who is ever counted, so they shape the epidemic curve as directly as the pathogen's biology does.
A model that treats contact as random averages away exactly the structure that drives transmission ([Buckee et al., 2021, Nature](https://doi.org/10.1038/s41586-021-03694-x)).

![Two contact matrices with identical total contacts per person, where assortative mixing yields a higher basic reproduction number than proportionate mixing.](../assets/figures/social-drivers-of-transmission.svg)

## Four different things we conflate

"Risk" hides at least four distinct social processes, and confusing them misdirects control.
**Exposure** is the chance of encountering the pathogen at all, set by housing density, occupation, and mobility.
**Susceptibility** is the chance that an exposure becomes an infection, shaped by age, nutrition, comorbidity, and prior immunity — themselves patterned by social conditions.
**Access to care** determines whether an infection is treated and its onward transmission cut short, and it depends on insurance, distance, trust, and time off work.
**Reporting** decides whether a case ever enters surveillance, so that the people with the least access are also the least visible, and the data quietly understate disease exactly where it is worst ([Noppert et al., 2016, Journal of Epidemiology & Community Health](https://doi.org/10.1136/jech-2016-207967)).

## Contact structure is a social phenomenon

Transmission requires contact, and contacts are not drawn uniformly at random.
People mix **assortatively**: children with children, coworkers with coworkers, households within households.
Epidemiologists encode this in a **who-acquires-infection-from-whom (WAIFW)** or contact matrix $C$, whose entry $C_{ij}$ is the mean number of contacts a member of group $i$ has with members of group $j$ per unit time.
Under **proportionate mixing**, contacts are shared across groups only in proportion to each group's activity, and the matrix is separable, $C_{ij}\propto a_i a_j$.
Under **assortative mixing**, the diagonal is inflated because people preferentially contact their own group, and that concentration is what a homogeneous model cannot see ([Arthur et al., 2017, Philosophical Transactions of the Royal Society B](https://doi.org/10.1098/rstb.2016.0454)).

## Structural determinants are upstream causes

The contact matrix is not given by nature; it is produced by structure.
Crowded or multigenerational housing raises within-household contact, essential-worker occupations remove the option to distance, and poverty and discrimination compress people into the settings where both exposure and susceptibility are highest.
These are **upstream causes**: they act before any individual behavior, and they explain why the same pathogen produces sharply different attack rates across neighborhoods that share a climate and a virus.
Treating the resulting disparity as a fixed group attribute rather than a modifiable structural input is both scientifically wrong and ethically corrosive ([Bedson et al., 2021, Nature Human Behaviour](https://doi.org/10.1038/s41562-021-01136-2)).

## Heterogeneity concentrates transmission

When contact rates are unequal, a small high-contact group can carry a disproportionate share of transmission.
The **basic reproduction number** for a structured population is not an average of group-level reproduction numbers; it is the spectral radius (dominant eigenvalue) of the **next-generation matrix** $K$,

\[
R_0 = \rho(K), \qquad K_{ij} = q\, D\, C_{ij},
\]

where $q$ is the per-contact transmission probability and $D$ the mean infectious duration.
Because $R_0$ is an eigenvalue rather than a mean, concentrating the same total number of contacts into a high-activity core raises it, and the dominant right eigenvector tells you which group the epidemic is riding.
This is why interventions aimed at the core can lower $R_0$ far more than their population share would suggest.

## A worked example

Take two groups: a high-contact group (crowded housing or frontline work) averaging $10$ contacts per day, and a low-contact group averaging $3$.
Hold those per-person totals fixed — the row sums of $C$ stay $10$ and $3$ — and change only how the contacts are distributed.
Under **proportionate mixing** the contact matrix is $C_{\text{prop}}=\begin{psmallmatrix}2.70 & 7.30\\ 0.81 & 2.19\end{psmallmatrix}$; under **assortative mixing** the diagonal is inflated to $C_{\text{assort}}=\begin{psmallmatrix}8.0 & 2.0\\ 0.6 & 2.4\end{psmallmatrix}$.
With $q=0.04$ and $D=6$ days, the proportionate matrix gives $R_0\approx 1.17$, while the assortative matrix gives $R_0\approx 1.97$ from the very same marginal contact totals.
The leading eigenvector shifts from $[0.77, 0.23]$ to $[0.91, 0.09]$: assortativity concentrates transmission almost entirely in the high-contact group, and a model that ignored the structure would have reported the lower, misleading number.

## In code

We build $K$ for each mixing pattern and read $R_0$ off the dominant eigenvalue.

### R

```r
q <- 0.04; D <- 6
C_prop   <- matrix(c(2.70, 7.30, 0.81, 2.19), 2, 2, byrow = TRUE)
C_assort <- matrix(c(8.0,  2.0,  0.6,  2.4 ), 2, 2, byrow = TRUE)

R0 <- function(C) max(Re(eigen(q * D * C)$values))
cat("R0 proportionate:", round(R0(C_prop),   3), "\n")
cat("R0 assortative:  ", round(R0(C_assort), 3), "\n")
```

### Python

```python
import numpy as np

q, D = 0.04, 6.0  # per-contact transmission prob, mean infectious days
C_prop   = np.array([[2.70, 7.30],
                     [0.81, 2.19]])   # proportionate mixing
C_assort = np.array([[8.0,  2.0],
                     [0.6,  2.4]])    # assortative: inflated diagonal

def analyze(C):
    K = q * D * C                     # next-generation matrix
    w, V = np.linalg.eig(K)
    j = int(np.argmax(w.real))        # dominant eigenpair
    v = np.abs(V[:, j].real)
    return float(w.real[j]), v / v.sum()

for name, C in [("proportionate", C_prop), ("assortative", C_assort)]:
    R0, evec = analyze(C)
    print(f"{name:>13}: R0 = {R0:.3f}  leading eigenvector = "
          f"[{evec[0]:.2f}, {evec[1]:.2f}]")

print("row sums (contacts/person) identical:",
      C_prop.sum(1).round(1), "vs", C_assort.sum(1).round(1))
print("-> same total contacts, assortativity raises R0 and")
print("   concentrates transmission in the high-contact group")
```

<!-- python-output:auto -->
```text
proportionate: R0 = 1.174  leading eigenvector = [0.77, 0.23]
  assortative: R0 = 1.970  leading eigenvector = [0.91, 0.09]
row sums (contacts/person) identical: [10.  3.] vs [10.  3.]
-> same total contacts, assortativity raises R0 and
   concentrates transmission in the high-contact group
```
<!-- /python-output:auto -->

### Julia

```julia
using LinearAlgebra
q, D = 0.04, 6.0
C_prop   = [2.70 7.30; 0.81 2.19]
C_assort = [8.0  2.0;  0.6  2.4]

R0(C) = maximum(real, eigvals(q * D * C))
println("R0 proportionate: ", round(R0(C_prop),   digits=3))
println("R0 assortative:   ", round(R0(C_assort), digits=3))
```

## Why it matters

The same virus, the same $q$, and the same average contact rate can produce an $R_0$ of $1.2$ or $2.0$ depending only on how a society arranges contact — so a transmission model that omits social structure is not merely imprecise, it can be qualitatively wrong about whether an outbreak grows.
Worse, the omission is not neutral: because structural forces put exposure, susceptibility, poor access, and undercounting on the same people, a model blind to structure understates risk exactly where disparities are widest and can steer resources away from the groups driving and bearing transmission.
Building social and behavioral inputs into the contact matrix, rather than averaging them away, is what lets a model both predict spread and avoid amplifying the inequities that produced it ([Bedson et al., 2021, Nature Human Behaviour](https://doi.org/10.1038/s41562-021-01136-2)).

## Related

- [Qualitative and mixed methods](qualitative-and-mixed-methods.md)
- [Behavior–disease coupled models](../math/behavior-disease-coupled-models.md)
- [Networks](../math/networks.md)
- [One Health surveillance](one-health-surveillance.md)
- [Epidemiology](../epidemiology.md)
