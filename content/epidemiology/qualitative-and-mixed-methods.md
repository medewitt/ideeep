---
title: "Qualitative and Mixed Methods in Epidemiology"
description: "How qualitative research and mixed-methods designs answer the questions of meaning, context, and mechanism that counts and rates cannot, and how to judge their rigor."
---

# Qualitative and Mixed Methods in Epidemiology

Epidemiology counts cases, estimates rates, and compares exposures, but a rate will never explain why people do what they do.
Qualitative methods recover the meaning, context, and mechanism behind the numbers, and mixed-methods designs bind the two kinds of evidence into one account.
Treated as core epidemiologic tools, they are how a study learns not just how many were infected but why transmission happened and why an intervention did or did not take hold.

![A code-saturation curve where the cumulative number of new themes rises and then plateaus as more interviews are analyzed.](../assets/figures/qualitative-and-mixed-methods.svg)

## What qualitative research answers that counts cannot

A well-run cohort can tell you that vaccine uptake in a district was 40 percent, but it cannot tell you what the other 60 percent were thinking about or what information they were weighing when they declined.
Qualitative research targets exactly this: meaning (what an illness or a control measure signifies to people), context (the household, economic, and political conditions that shape exposure), mechanism (the causal steps between a policy and a behavior), and barriers to both care-seeking and intervention uptake.
These are questions about process and reason, not frequency, and they are answered by listening in depth rather than by tabulating.
The argument that these are epidemiologic questions, answerable by epidemiologic methods, is made directly by [Stelson et al., 2025, American Journal of Epidemiology](https://doi.org/10.1093/aje/kwaf083), and the field's incompleteness without them is argued by [Lane-Fall, 2023, American Journal of Epidemiology](https://doi.org/10.1093/aje/kwad050).

## Core methods

Qualitative designs are few and well defined.
**Semi-structured interviews** follow a guide of open questions but let the participant lead, trading standardization for depth.
**Focus groups** convene six to ten people so that norms, disagreements, and shared vocabulary surface in the interaction itself.
**Participant observation** places the researcher in the setting over time, recording what people do rather than only what they say.
**Rapid qualitative appraisal** compresses these into days rather than months, using team-based fieldwork and structured debriefs to feed findings back into a live response.

## Analysis: coding, themes, and saturation

Analysis turns transcripts into structure.
A researcher reads the text and attaches **codes** — short labels marking a passage as being about, say, "cost of transport" or "distrust of clinic staff."
**Thematic analysis** groups related codes into broader themes that describe patterns across participants.
Sampling and coding continue until **saturation**, the point at which new interviews stop yielding new codes or themes, which is the qualitative counterpart to a sample-size stopping rule.

## Rigor and trustworthiness

Qualitative work is judged by trustworthiness rather than by a p-value, along four criteria.
**Credibility** asks whether the findings faithfully represent participants' accounts, **transferability** whether they plausibly extend to other settings, **dependability** whether the process is consistent and auditable, and **confirmability** whether conclusions are grounded in the data rather than the analyst's bias.
Two concrete practices support these: **investigator triangulation**, in which multiple coders analyze the same material and reconcile differences, and **member checking**, in which participants review whether the interpretation rings true.
Investigator triangulation is only meaningful if coders actually agree, which is why inter-rater reliability is measured, as below.

## Mixed-methods designs and integration

Mixed methods combine quantitative and qualitative strands deliberately, and the design names the timing and purpose.
A **convergent (triangulation)** design collects both strands in parallel and compares them to see whether they corroborate or conflict.
A **sequential explanatory** design runs the quantitative study first and then uses qualitative work to explain surprising or null results.
A **sequential exploratory** design reverses the order, using qualitative work first to generate hypotheses or build a survey instrument that the quantitative strand then tests.
The value lives in **integration** — the explicit joining of strands, not their mere co-presence — where a rate and a reason are read against each other to produce a claim neither could support alone.

## Rapid qualitative research during outbreaks

Outbreaks compress every timescale, and qualitative research adapts by going fast.
Rapid designs, deployed at scale during COVID-19 by [Vindrola-Padrós et al., 2020, Qualitative Health Research](https://doi.org/10.1177/1049732320951526), can deliver actionable findings on isolation adherence or health-worker strain within a week.
The trade-offs are real: fewer interviews, shallower analysis, and less time to reach saturation, so speed is bought with some loss of depth and certainty.
The discipline is to be explicit about that trade so that a rapid finding is used as timely guidance rather than mistaken for a settled result.

## The role of medical anthropology

In epidemic response, anthropology is often reduced to improving "message uptake," as though the only problem were getting people to accept a fixed instruction.
Its actual contribution is to reframe the response itself around local realities of trust, kinship, burial, livelihood, and power, as argued by [Stellmach et al., 2018, BMJ Global Health](https://doi.org/10.1136/bmjgh-2017-000534).
The broader anthropology of how infectious diseases emerge and how epidemics are actually controlled is synthesized by [Giles-Vernick et al., 2025, Clinical Microbiology and Infection](https://doi.org/10.1016/j.cmi.2025.04.019).
The lesson is that community engagement shapes what interventions are even possible, not merely how they are advertised.

## A worked example

Two coders independently label 20 interview excerpts for whether each mentions a **structural barrier to care** (1) or not (0).
Their agreement determines whether investigator triangulation is credible.
Cross-tabulating the two coders gives the following counts.

| | Coder B: yes | Coder B: no | Row total |
| --- | --- | --- | --- |
| **Coder A: yes** | 7 | 2 | 9 |
| **Coder A: no** | 1 | 10 | 11 |
| **Column total** | 8 | 12 | 20 |

Observed agreement is the diagonal share, $p_o = (7 + 10) / 20 = 0.85$.
Expected agreement under independence sums the products of the marginals:

\[ p_e = \frac{9}{20}\cdot\frac{8}{20} + \frac{11}{20}\cdot\frac{12}{20} = 0.18 + 0.33 = 0.51. \]

Cohen's kappa corrects the observed agreement for this chance:

\[ \kappa = \frac{p_o - p_e}{1 - p_e} = \frac{0.85 - 0.51}{1 - 0.51} \approx 0.69. \]

A kappa of about 0.69 is substantial agreement, high enough to treat the two coders' shared scheme as dependable.
A note on Cohen's kappa: pooling many items into a single measure can inflate the value structurally, so be careful when combining multiple scales.

## In code

We compute observed agreement, expected agreement, and Cohen's kappa directly from two coders' binary labels.

### R

```r
coder_a <- c(1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0)
coder_b <- c(1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0)

p_o <- mean(coder_a == coder_b)
pa <- mean(coder_a); pb <- mean(coder_b)
p_e <- pa * pb + (1 - pa) * (1 - pb)
kappa <- (p_o - p_e) / (1 - p_e)

cat(sprintf("p_o=%.2f p_e=%.2f kappa=%.2f\n", p_o, p_e, kappa))
```

### Python

```python
import numpy as np

coder_a = np.array([1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0])
coder_b = np.array([1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0])

n = coder_a.size
both_yes = int(np.sum((coder_a == 1) & (coder_b == 1)))
both_no = int(np.sum((coder_a == 0) & (coder_b == 0)))
p_o = (both_yes + both_no) / n

pa, pb = coder_a.mean(), coder_b.mean()
p_e = pa * pb + (1 - pa) * (1 - pb)
kappa = (p_o - p_e) / (1 - p_e)

labels = ["poor", "fair", "moderate", "substantial", "almost perfect"]
interp = labels[min(int(max(kappa, 0) / 0.2), 4)]

print(f"excerpts        : {n}")
print(f"both yes        : {both_yes}")
print(f"both no         : {both_no}")
print(f"observed  p_o   : {p_o:.2f}")
print(f"expected  p_e   : {p_e:.2f}")
print(f"cohen's kappa   : {kappa:.2f}")
print(f"interpretation  : {interp}")
```

<!-- python-output:auto -->
```text
excerpts        : 20
both yes        : 7
both no         : 10
observed  p_o   : 0.85
expected  p_e   : 0.51
cohen's kappa   : 0.69
interpretation  : substantial
```
<!-- /python-output:auto -->

### Julia

```julia
coder_a = [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0]
coder_b = [1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0]

p_o = sum(coder_a .== coder_b) / length(coder_a)
pa, pb = sum(coder_a)/length(coder_a), sum(coder_b)/length(coder_b)
p_e = pa * pb + (1 - pa) * (1 - pb)
kappa = (p_o - p_e) / (1 - p_e)

println("p_o=$(round(p_o, digits=2)) p_e=$(round(p_e, digits=2)) kappa=$(round(kappa, digits=2))")
```

## Why it matters

In infectious-disease epidemiology the decisive quantities often sit outside the case counts: why a community distrusts a ring-vaccination team, why contacts avoid isolation, why a burial practice sustains transmission.
Qualitative methods surface these mechanisms, mixed-methods integration ties them to the rates that measure their impact, and inter-rater reliability keeps the qualitative side auditable rather than impressionistic.
Reading an outbreak's numbers together with the reasons behind them is what turns a description of transmission into a response that can actually change it.

## Related

- [Social and structural drivers of transmission](social-drivers-of-transmission.md)
- [Risk communication and community engagement](risk-communication-and-rcce.md)
- [Outbreak investigation](outbreak-investigation.md)
- [Epidemiologic study designs](study-designs.md)
- [Epidemiology](../epidemiology.md)
